"""Lab 21: run the forward process, check Tweedie's formula, and train a noise-guesser that learns the score."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Guessing the noise is learning the score"
GOAL = ("On a three-bump mixture in one dimension, where the score at every noise level is known, check the forward "
        "process's closed form, check Tweedie's formula by quadrature, and train a small network to guess the noise: "
        "its loss must stay a fixed constant above its squared error against the exact score.")
TASKS = [
    "Change the noise level from step 300 to step 50 and to step 800. Where is the constant C largest, and why is the score hardest to learn at low noise?",
    "Train the network to guess the clean point x0 instead of the noise, and convert its output to a score with Tweedie's formula.",
    "Use the exact score in 50 DDIM steps from noise (the widget's update) and compare the samples' histogram with the mixture.",
]

W = np.array([0.3, 0.4, 0.3])  # the data: a mixture of three narrow Gaussians
MU = np.array([-1.5, 0.2, 1.4])
S = np.array([0.15, 0.25, 0.15])


def marginal(x, a, b):
    """The density of a x0 + b eps and its score, both exact."""
    var = a * a * S ** 2 + b * b
    comp = W * np.exp(-0.5 * (x[:, None] - a * MU) ** 2 / var) / np.sqrt(2 * np.pi * var)
    p = comp.sum(1)
    return p, (comp * (a * MU - x[:, None]) / var).sum(1) / p


def sample_data(rng, n):
    k = rng.choice(3, n, p=W)
    return MU[k] + S[k] * rng.standard_normal(n)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the forward chain, step by step, against one jump
    betas = np.linspace(1e-4, 0.02, 1000)
    abar = np.cumprod(1 - betas)
    t = 300
    a, b = np.sqrt(abar[t - 1]), np.sqrt(1 - abar[t - 1])
    x0 = sample_data(rng, 20000)
    x = x0.copy()
    for beta in betas[:t]:
        x = np.sqrt(1 - beta) * x + np.sqrt(beta) * rng.standard_normal(len(x))
    slope = (x @ x0) / (x0 @ x0)
    left = np.var(x - slope * x0)
    lab.row(f"after {t} steps: slope of x_t on x_0", f"{slope:.4f}   (sqrt(abar) = {a:.4f})")
    lab.row(f"after {t} steps: leftover variance", f"{left:.4f}   (1 - abar = {b * b:.4f})")
    assert abs(slope - a) < 0.02 and abs(left - b * b) < 0.02, "the forward chain has the closed form"

    # 2. Tweedie: the posterior mean by brute-force quadrature against (x + sigma^2 score) / alpha
    xs = np.linspace(-2.2, 2.2, 221)
    g = np.linspace(-4, 4, 8001)
    prior = (W * np.exp(-0.5 * (g[:, None] - MU) ** 2 / S ** 2) / np.sqrt(2 * np.pi * S ** 2)).sum(1)
    like = np.exp(-0.5 * (xs[:, None] - a * g[None]) ** 2 / (b * b))
    brute = (like * prior * g).sum(1) / (like * prior).sum(1)
    _, score = marginal(xs, a, b)
    tweedie = (xs + b * b * score) / a
    gap = np.abs(brute - tweedie).max()
    lab.row("Tweedie: largest gap to the brute-force posterior mean", f"{gap:.1e}")
    assert gap < 1e-6, "Tweedie's formula"

    # 3. a network that guesses the noise: 1 -> 24 -> 24 -> 1, tanh, trained with Adam on the series' autodiff
    h = 24
    params = [Tensor(v, requires_grad=True) for v in (
        rng.standard_normal((1, h)), np.zeros(h), rng.standard_normal((h, h)) / np.sqrt(h), np.zeros(h),
        rng.standard_normal((h, 1)) / np.sqrt(h), np.zeros(1))]

    def net(v):
        w1, b1, w2, b2, w3, b3 = params
        return ((((Tensor(v[:, None]) @ w1 + b1).tanh() @ w2 + b2).tanh()) @ w3 + b3)

    ev_x0, ev_eps = sample_data(rng, 40000), rng.standard_normal(40000)
    ev_x = a * ev_x0 + b * ev_eps
    best = -b * marginal(ev_x, a, b)[1]  # E[eps | x] = -sigma * score
    const = float(np.mean((ev_eps - best) ** 2))  # what no network can remove

    def losses():
        out = net(ev_x).data[:, 0]
        return float(np.mean((out - ev_eps) ** 2)), float(np.mean((out - best) ** 2))

    m = [np.zeros_like(p.data) for p in params]
    v2 = [np.zeros_like(p.data) for p in params]
    steps, lr, curve = 1200, 0.01, []
    for k in range(steps + 1):
        if k % 100 == 0:
            curve.append((k, *losses()))
        bx0, be = sample_data(rng, 256), rng.standard_normal(256)
        for p in params:
            p.grad[:] = 0
        loss = ((net(a * bx0 + b * be) - be[:, None]) ** 2).mean()
        loss.backward()
        for i, p in enumerate(params):
            m[i] = 0.9 * m[i] + 0.1 * p.grad
            v2[i] = 0.999 * v2[i] + 0.001 * p.grad ** 2
            p.data -= lr * (m[i] / (1 - 0.9 ** (k + 1))) / (np.sqrt(v2[i] / (1 - 0.999 ** (k + 1))) + 1e-8)
    curve = np.array(curve)
    gaps = curve[:, 1] - curve[:, 2]
    lab.row("noise-guessing loss, start to end", f"{curve[0, 1]:.3f} to {curve[-1, 1]:.3f}")
    lab.row("error against the exact score's noise guess", f"{curve[0, 2]:.3f} to {curve[-1, 2]:.4f}")
    lab.row("their difference at every checkpoint", f"{gaps.min():.3f} to {gaps.max():.3f}   (constant C = {const:.3f})")
    lab.note = ("The network never sees a score, only noisy points and the noise that was added; its loss is the error "
                "against the exact score plus a constant, so driving the loss down drives the network to the score.")
    assert curve[-1, 2] < 0.1 * curve[0, 2] and curve[-1, 2] < 0.02, "the noise-guesser has learned the score"
    assert np.abs(gaps - const).max() < 0.04 * max(1.0, curve[0, 2]), "Vincent: the two losses differ by a constant"
    assert curve[-1, 1] > const - 0.01, "no network beats the posterior mean"

    fig, ax = labs.figure(2, size=(11, 4.2))
    p, sc = marginal(xs, a, b)
    ax[0].fill_between(xs, 0, p / p.max(), color=labs.MUTED, alpha=0.25, label="density of x_t (scaled)")
    ax[0].plot(xs, -b * sc, color=labs.GOLD, lw=3, alpha=0.7, label="exact: -sigma x score")
    ax[0].plot(xs, net(xs).data[:, 0], color=labs.BLUE, label="network's noise guess")
    ax[0].set(title=f"The best noise guess at step {t}", xlabel="noisy point x_t", ylabel="guess of the noise")
    ax[0].legend(loc="upper left")
    ax[1].plot(curve[:, 0], curve[:, 1], "o-", color=labs.BLUE, ms=3, label="noise-guessing loss (trainable from data)")
    ax[1].plot(curve[:, 0], curve[:, 2], "o-", color=labs.GREEN, ms=3, label="error against the exact score")
    ax[1].axhline(const, color=labs.GOLD, ls="--", label=f"the constant C = {const:.3f}")
    ax[1].set(title="Two losses, one constant apart", xlabel="training step", ylabel="mean squared error", yscale="log")
    ax[1].legend(loc="center right")
    lab.fig = fig
    return lab
