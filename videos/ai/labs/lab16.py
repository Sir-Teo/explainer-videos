"""Lab 16: check the router's gradient through a top-k gate three ways, then balance a lopsided router with a bias."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, log_softmax, sigmoid

TITLE = "The router's gradient, and balance without a loss"
GOAL = ("For one token and eight random linear experts, compare the router's gradient from the film's formula, from "
        "the series' autodiff and from finite differences, for Mixtral's softmax gate and DeepSeek-V3's sigmoid gate. "
        "Then route 512 tokens a step through a router that plays favourites, and let the loss-free bias even it out.")
TASKS = [
    "Set K_TOP = 1 with the softmax gate (a renormalized top-1 gate). What is the gradient, and why does Switch keep "
    "the raw probability instead?",
    "Raise GAMMA from 0.01 to 0.2. Does the busiest expert's load settle closer to a fair share or further from it?",
    "Replace the bias by capacity alone: keep the unbalanced router and find the capacity factor that drops under 1% "
    "of the token slots.",
]
E, K_TOP, D = 8, 2, 6
GAMMA, STEPS, BATCH = 0.01, 600, 512


def gates(s, chosen, kind):
    """The gates of the chosen experts as a Tensor: a softmax over the chosen scores, or sigmoids rescaled to add to 1."""
    if kind == "softmax":
        return log_softmax(s[chosen]).exp()
    sg = sigmoid(s[chosen])
    return sg / sg.sum()


def formula(s, chosen, u, kind):
    """dL/ds_j = g_j (u_j - u_bar) for chosen experts (times 1 - sigma_j for the sigmoid gate), 0 otherwise."""
    out = np.zeros(E)
    if kind == "softmax":
        g = np.exp(s[chosen] - s[chosen].max())
        g /= g.sum()
        out[chosen] = g * (u - g @ u)
    else:
        sg = 1 / (1 + np.exp(-s[chosen]))
        g = sg / sg.sum()
        out[chosen] = (1 - sg) * g * (u - g @ u)
    return out


def loads(scores, bias):
    """Each expert's share of the token slots when the top k are chosen by score + bias."""
    pick = np.argsort(-(scores + bias), axis=1)[:, :K_TOP]
    return np.bincount(pick.ravel(), minlength=E) / pick.size, pick


def dropped_by_buffers(pick, c):
    """Fill each expert's buffer of ceil(c k N / E) slots in token order and count the slots that do not fit."""
    cap, used, lost = int(np.ceil(c * pick.size / E)), np.zeros(E, int), 0
    for e in pick.ravel():
        if used[e] < cap:
            used[e] += 1
        else:
            lost += 1
    return lost / pick.size


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the router's gradient: formula, autodiff, finite differences
    A = rng.standard_normal((E, D, D))
    x, target = rng.standard_normal(D), rng.standard_normal(D)
    s0 = rng.standard_normal((E, D)) @ x
    chosen = np.argsort(-s0)[:K_TOP]
    Y = A[chosen] @ x  # the chosen experts' outputs, one row each

    def loss(s, kind):
        y = gates(s, chosen, kind) @ Tensor(Y)
        return ((y - target) ** 2).sum() * 0.5, y

    grads = {}
    for kind in ("softmax", "sigmoid"):
        s = Tensor(s0, requires_grad=True)
        L, y = loss(s, kind)
        L.backward()
        u = Y @ (y.data - target)  # u_i: how hard expert i's output pushes the loss
        fd = np.zeros(E)
        for i in range(E):
            h = np.zeros(E)
            h[i] = 1e-6
            fd[i] = (loss(Tensor(s0 + h), kind)[0].data - loss(Tensor(s0 - h), kind)[0].data) / 2e-6
        ana = formula(s0, chosen, u, kind)
        scale = max(np.abs(fd).max(), 1e-12)
        grads[kind] = (fd, ana, s.grad)
        lab.row(f"{kind} gate: formula against finite differences", f"{np.abs(ana - fd).max() / scale:.1e} (relative)")
        lab.row(f"{kind} gate: autodiff against finite differences", f"{np.abs(s.grad - fd).max() / scale:.1e} (relative)")
        assert np.abs(ana - fd).max() / scale < 1e-5 and np.abs(s.grad - fd).max() / scale < 1e-5, kind
        rest = np.setdiff1d(np.arange(E), chosen)
        assert np.all(s.grad[rest] == 0) and np.abs(fd[rest]).max() < 1e-9, "an unchosen score gets no gradient"
        if K_TOP > 1:
            assert np.count_nonzero(s.grad) == K_TOP, "every chosen score learns"
    lab.row("scores with any gradient", f"{np.count_nonzero(grads['softmax'][2])} of {E}   (k = {K_TOP})")

    # 2. a router that plays favourites, balanced by a bias that only steers the choice
    favour = np.linspace(1.2, -1.2, E)
    draw = lambda: favour + rng.standard_normal((BATCH, E))  # noqa: E731
    bias, trace = np.zeros(E), []
    for _ in range(STEPS):
        f, _ = loads(draw(), bias)
        trace.append(E * f.max() - 1)  # MaxVio: the busiest expert's excess over a fair share
        bias -= GAMMA * np.sign(f - 1 / E)
    test = favour + rng.standard_normal((20 * BATCH, E))
    out = {}
    for name, b in (("no balancing", np.zeros(E)), ("loss-free bias", bias)):
        f, pick = loads(test, b)
        drop = np.maximum(0, f - 1 / E).sum()
        out[name] = dict(f=f, maxvio=E * f.max() - 1, drop=drop, sim=dropped_by_buffers(pick, 1.0))
        lab.row(f"{name}: busiest expert", f"{E * f.max():.2f} x a fair share   MaxVio {out[name]['maxvio']:.2f}")
        lab.row(f"{name}: slots dropped at c = 1", f"{drop:.1%} by the formula   {out[name]['sim']:.1%} filling buffers")
        lab.row(f"{name}: E sum f_i^2", f"{E * (f ** 2).sum():.3f}   (Switch's penalty when P = f; at least 1)")
        assert abs(drop - out[name]["sim"]) < 2e-3, "dropped share = sum of max(0, f_i - c/E)"
    a, b = out["no balancing"], out["loss-free bias"]
    assert a["maxvio"] > 0.5 and a["drop"] > 0.15, "the unbalanced router overloads its favourites"
    assert b["maxvio"] < 0.1 and b["drop"] < 0.03, "the bias brings every expert near its fair share"
    assert E * (b["f"] ** 2).sum() < E * (a["f"] ** 2).sum()
    lab.note = ("A router learns only from the experts it tried: the unchosen scores have gradient exactly zero. A bias "
                "added to the scores only when choosing spreads the load, and a capacity factor of 1 then drops almost "
                "nothing.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    fd, ana, auto = grads["softmax"]
    w = 0.27
    for k, (vals, color, name) in enumerate(((fd, labs.GREY, "finite differences"), (ana, labs.GOLD, "g_j (u_j - u_bar)"),
                                             (auto, labs.BLUE, "autodiff"))):
        ax[0].bar(np.arange(E) + (k - 1) * w, vals, w, color=color, label=name)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title=f"The router's gradient, softmax gate: {K_TOP} of {E} scores learn", xlabel="expert",
              ylabel="dL/ds")
    ax[0].set_xticks(range(E), [f"{i}*" if i in chosen else str(i) for i in range(E)])
    ax[0].legend(title="* = chosen", loc="best")
    ax[1].bar(np.arange(E) - 0.2, E * a["f"], 0.4, color=labs.RED, label="no balancing")
    ax[1].bar(np.arange(E) + 0.2, E * b["f"], 0.4, color=labs.GREEN, label="loss-free bias")
    ax[1].axhline(1, color=labs.MUTED, ls="--", lw=1, label="fair share = capacity at c = 1")
    ax[1].set(title="Each expert's load, in fair shares", xlabel="expert", ylabel="share of token slots x E",
              ylim=(0, 1.25 * E * a["f"].max()))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
