"""Lab 24: estimate a known mutual information with InfoNCE, and watch the estimate stop at log N."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, cross_entropy

TITLE = "InfoNCE: a lower bound with a ceiling"
GOAL = ("Draw correlated Gaussian pairs in 20 dimensions whose mutual information is known (2 or 5 nats), train a "
        "two-parameter critic with the series' autodiff to pick each x's partner out of N candidates, and compare "
        "log N minus the loss with the true information and with log N.")
TASKS = [
    "Set the true information to 10 nats. How many candidates would a batch need before the estimate could reach it?",
    "Replace the critic by the plain dot product x . y (drop the |y|^2 term). How much of the bound is lost at N = 512?",
    "Make all 2N embeddings of a batch equal and compute the NT-Xent loss at temperatures 0.1 and 1. Why does the temperature not matter there?",
]

D = 20


def pairs(rng, n, rho):
    x = rng.standard_normal((n, D))
    return x, rho * x + np.sqrt(1 - rho ** 2) * rng.standard_normal((n, D))


def rho_for(info):
    """The per-coordinate correlation that gives I(X; Y) = info nats: I = -(D/2) log(1 - rho^2)."""
    return np.sqrt(1 - np.exp(-2 * info / D))


def logits(x, y, a, b):
    """The critic f(x_i, y_j) = a x_i . y_j - b |y_j|^2 for every pair of a batch (a, b numbers or Tensors)."""
    return a * Tensor(x @ y.T) - b * Tensor((y * y).sum(1)[None, :])


def estimate(rng, rho, a, b, n, batches):
    out = []
    for _ in range(batches):
        x, y = pairs(rng, n, rho)
        out.append(np.log(n) - float(cross_entropy(logits(x, y, a, b), np.arange(n)).data))
    return float(np.mean(out)), float(np.max(out))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    Ns = [2, 8, 32, 128, 512]
    curves, trained, history = {}, {}, None
    for info in (2.0, 5.0):
        rho = rho_for(info)
        a_star, b_star = rho / (1 - rho ** 2), rho ** 2 / (2 * (1 - rho ** 2))  # log p(y|x)/p(y), up to c(x)
        # train the critic at N = 128 by gradient descent on the N-way cross-entropy
        a, b, trace = Tensor(0.0, requires_grad=True), Tensor(0.0, requires_grad=True), []
        for step in range(300):
            x, y = pairs(rng, 128, rho)
            loss = cross_entropy(logits(x, y, a, b), np.arange(128))
            a.grad[...] = 0
            b.grad[...] = 0
            loss.backward()
            a.data -= 0.02 * a.grad
            b.data -= 0.02 * b.grad
            trace.append(np.log(128) - float(loss.data))
        trained[info] = (float(a.data), float(b.data), a_star, b_star)
        if info == 2.0:
            history = trace
        curves[info] = [estimate(rng, rho, float(a.data), float(b.data), n, 8 if n > 200 else 24 if n > 100 else 100) for n in Ns]
        best = estimate(rng, rho, a_star, b_star, 512, 8)[0]
        lab.row(f"I = {info:g} nats: trained critic (a, b)", f"({a.data:.3f}, {b.data:.3f})   optimal ({a_star:.3f}, {b_star:.3f})")
        lab.row(f"I = {info:g} nats: estimate at N = " + ", ".join(map(str, Ns)), "  ".join(f"{m:.2f}" for m, _ in curves[info]))
        lab.row(f"I = {info:g} nats: the ceiling log N", "  ".join(f"{np.log(n):.2f}" for n in Ns) + f"   (optimal critic at 512: {best:.2f})")
        assert abs(a.data - a_star) < 0.25 * a_star and abs(b.data - b_star) < 0.5 * b_star + 0.03, "the critic learns the density ratio"
        assert all(top <= np.log(n) + 1e-9 for (_, top), n in zip(curves[info], Ns)), "no batch certifies more than log N"
        assert all(m < info + 0.1 for m, _ in curves[info]), "and the estimate is a lower bound on I"
        assert all(q[0] > p[0] for p, q in zip(curves[info], curves[info][1:])), "more candidates, tighter bound"
        assert abs(curves[info][-1][0] - best) < 0.15, "the trained critic is as good as the optimal one"
    assert curves[2.0][-1][0] > 1.6, "with log N well above I the bound is nearly tight"
    assert curves[5.0][1][0] < np.log(8) and curves[5.0][-1][0] < 4.7, "with I above log N it is capped"

    # what collapse costs a contrastive loss: 2N equal embeddings give log(2N - 1), whatever the temperature
    n, tau = 64, 0.2
    z = np.tile(rng.standard_normal(8), (2 * n, 1))
    z /= np.linalg.norm(z, axis=1, keepdims=True)
    sim = z @ z.T / tau
    np.fill_diagonal(sim, -np.inf)
    partner = np.concatenate([np.arange(n, 2 * n), np.arange(n)])
    ntxent = float(np.mean(np.log(np.exp(sim).sum(1)) - sim[np.arange(2 * n), partner]))
    lab.row("NT-Xent at a collapsed encoder, N = 64", f"{ntxent:.4f}   (log(2N - 1) = {np.log(2 * n - 1):.4f})")
    assert abs(ntxent - np.log(2 * n - 1)) < 1e-9
    lab.note = ("Picking the partner out of N candidates can certify at most log N nats: InfoNCE measures 2 nats well "
                "with a batch of 512 and cannot see 5 nats with a batch of 8, which is why contrastive methods want "
                "large batches.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(Ns, np.log(Ns), color=labs.MUTED, ls="--", label="the ceiling log N")
    for info, color in ((2.0, labs.BLUE), (5.0, labs.GOLD)):
        ax[0].axhline(info, color=color, ls=":", lw=1.2)
        ax[0].plot(Ns, [m for m, _ in curves[info]], "o-", color=color, label=f"estimate, true I = {info:g} nats (dotted)")
    ax[0].set(xscale="log", title="log N - loss against the number of candidates", xlabel="candidates N", ylabel="nats")
    ax[0].set_xticks(Ns, [str(n) for n in Ns])
    ax[0].legend(loc="upper left")
    ax[1].plot(np.arange(1, 301), history, color=labs.BLUE, lw=1, alpha=0.5, label="each batch of 128")
    smooth = np.convolve(history, np.ones(20) / 20, mode="valid")
    ax[1].plot(np.arange(20, 301), smooth, color=labs.BLUE, label="mean of the last 20")
    ax[1].axhline(2.0, color=labs.GOLD, ls=":", label="true I = 2 nats")
    ax[1].axhline(np.log(128), color=labs.MUTED, ls="--", label="log 128")
    ax[1].set(title="Training the critic (I = 2 nats, N = 128)", xlabel="step", ylabel="log N - loss (nats)")
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
