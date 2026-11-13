"""Lab 9: backpropagate through a 2-2-1 network three ways, then train it on XOR from twenty random starts."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, sigmoid

TITLE = "Backpropagation on XOR, checked three ways"
GOAL = ("Compute the nine gradients of a 2-2-1 tanh network by the series' autodiff, by the delta equations and by finite "
        "differences; then train on XOR from twenty random starts and count how many find a solution.")
TASKS = [
    "Give the hidden layer 4 units instead of 2. How many of the twenty starts get stuck now?",
    "Replace tanh by relu in the hidden layer (in both forward passes and in the delta equations). Do the three gradients still agree, and how many starts solve XOR?",
    "Remove the hidden layer and train the single unit on AND, OR and XOR. Which of the three can it learn, and why?",
]

X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
Y = np.array([0.0, 1.0, 1.0, 0.0])


def init(rng, hidden=2):
    return dict(W1=rng.normal(0, 1.0, (2, hidden)), b1=rng.normal(0, 0.5, hidden), W2=rng.normal(0, 1.0, (hidden, 1)), b2=np.zeros(1))


def forward(p, x=X):
    h = np.tanh(x @ p["W1"] + p["b1"])
    return h, 1 / (1 + np.exp(-((h @ p["W2"])[:, 0] + p["b2"][0])))


def loss_np(p):
    q = np.clip(forward(p)[1], 1e-12, 1 - 1e-12)
    return float(-(Y * np.log(q) + (1 - Y) * np.log(1 - q)).mean())


def grad_autodiff(p):
    """The loss and its gradients by the series' reverse-mode autodiff."""
    t = {k: Tensor(v, requires_grad=True) for k, v in p.items()}
    q = sigmoid((Tensor(X) @ t["W1"] + t["b1"]).tanh() @ t["W2"] + t["b2"])
    y = Y[:, None]
    loss = -((q.log() * y) + ((1 - q).log() * (1 - y))).mean()
    loss.backward()
    return float(loss.data), {k: t[k].grad.copy() for k in p}


def grad_delta(p):
    """The delta equations by hand: delta2 = q - y at a sigmoid output with cross-entropy, delta1 = W2 delta2 (.) tanh'."""
    h, q = forward(p)
    d2 = (q - Y) / len(X)
    d1 = np.outer(d2, p["W2"][:, 0]) * (1 - h ** 2)
    return dict(W1=X.T @ d1, b1=d1.sum(0), W2=(h.T @ d2)[:, None], b2=np.array([d2.sum()]))


def grad_numeric(p, eps=1e-6):
    g = {k: np.zeros_like(v) for k, v in p.items()}
    for k, v in p.items():
        for idx in np.ndindex(v.shape):
            up, down = ({kk: vv.copy() for kk, vv in p.items()} for _ in range(2))
            up[k][idx] += eps
            down[k][idx] -= eps
            g[k][idx] = (loss_np(up) - loss_np(down)) / (2 * eps)
    return g


def run(seed=0):
    rng = np.random.default_rng(seed)
    flat = lambda g: np.concatenate([g[k].ravel() for k in ("W1", "b1", "W2", "b2")])
    p = init(rng)
    g_ad, g_bp, g_fd = flat(grad_autodiff(p)[1]), flat(grad_delta(p)), flat(grad_numeric(p))
    err_bp, err_fd = np.abs(g_ad - g_bp).max(), np.abs(g_ad - g_fd).max()

    starts, steps, lr = 20, 600, 1.0
    curves, solved, nets = [], [], []
    for _ in range(starts):
        p = init(rng)
        losses = []
        for _ in range(steps):
            loss, g = grad_autodiff(p)
            losses.append(loss)
            for k in p:
                p[k] -= lr * g[k]
        curves.append(losses)
        solved.append(bool(((forward(p)[1] > 0.5) == (Y > 0.5)).all()))
        nets.append(p)
    solved = np.array(solved)
    final = np.array([c[-1] for c in curves])

    # one unit, no hidden layer: try every line w1 x1 + w2 x2 + b > 0 on a grid of weights
    w = np.linspace(-2, 2, 41)
    w1, w2, b = np.meshgrid(w, w, w, indexing="ij")
    fires = w1[..., None] * X[:, 0] + w2[..., None] * X[:, 1] + b[..., None] > 0
    best_line = (fires == (Y > 0.5)).mean(-1).max()

    lab = labs.Lab()
    lab.row("nine gradients: autodiff against the delta equations", f"largest difference {err_bp:.1e}")
    lab.row("nine gradients: autodiff against finite differences", f"largest difference {err_fd:.1e}")
    lab.row("starts that solve XOR", f"{solved.sum()} of {starts}")
    lab.row("final loss of the solved starts", f"at most {final[solved].max():.4f} nats" if solved.any() else "none solved")
    lab.row("final loss of the stuck starts", f"at least {final[~solved].min():.3f} nats" if (~solved).any() else "none stuck")
    lab.row("best of 68,921 single units (lines) on XOR", f"{best_line:.0%} of the four points")
    lab.note = ("The chain rule run backwards gives the same nine numbers as differencing the loss; with them a hidden "
                "layer of two units can learn XOR, though not from every start, and no single unit can.")

    assert err_bp < 1e-12 and err_fd < 1e-7, "three ways to the same gradient"
    assert solved.any(), "a hidden layer can represent and learn XOR"
    assert np.median(final[solved]) < 0.05, "the solved starts drive the loss toward zero"
    assert solved.all() or np.median(final[~solved]) > 0.3, "the stuck starts sit on a plateau with a point wrong"
    assert best_line <= 0.75, "no line separates XOR"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for c, ok in zip(curves, solved):
        ax[0].plot(np.arange(1, steps + 1), c, color=labs.GOLD if ok else labs.RED, lw=1.1, alpha=0.8)
    ax[0].plot([], [], color=labs.GOLD, label=f"solved ({solved.sum()})")
    ax[0].plot([], [], color=labs.RED, label=f"stuck ({(~solved).sum()})")
    ax[0].set(xscale="log", yscale="log", title="Twenty starts on XOR", xlabel="gradient-descent step", ylabel="cross-entropy (nats)")
    ax[0].legend(loc="lower left")
    best = nets[int(np.argmin(final))]
    u = np.linspace(-0.4, 1.4, 121)
    gx, gy = np.meshgrid(u, u)
    q = forward(best, np.column_stack([gx.ravel(), gy.ravel()]))[1].reshape(gx.shape)
    ax[1].contourf(gx, gy, q, levels=np.linspace(0, 1, 11), cmap="cividis", alpha=0.9)
    ax[1].contour(gx, gy, q, levels=[0.5], colors=[labs.INK], linewidths=1.5)
    ax[1].scatter(X[:, 0], X[:, 1], c=[labs.GOLD if t else labs.BLUE for t in Y], s=120, edgecolors=labs.BG, linewidths=1.5, zorder=3)
    ax[1].set(title="One solved network (white: output 0.5)", xlabel="input 1", ylabel="input 2", aspect="equal")
    ax[1].grid(False)
    lab.fig = fig
    return lab
