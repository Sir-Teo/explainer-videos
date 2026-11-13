"""Lab 20: train a discriminator to its optimum p/(p + q), then let two players follow their gradients on xy."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, sigmoid

TITLE = "The adversarial game: the optimal discriminator and the spiral"
GOAL = ("Train a logistic discriminator between samples of p = N(0, 1) and q = N(1.5, 1) with the series' autodiff and "
        "compare it with D* = p/(p + q) and its value with -log 4 + 2 JS; then run simultaneous, alternating and "
        "extragradient steps on min_x max_y xy and compare each radius with its eigenvalue.")
TASKS = [
    "Move q to N(4, 1). How close does the value get to its ceiling of 0, and what happens to the gradient of log(1 - D) under q?",
    "Add the penalty -gamma/2 y^2 to the y player's objective (gamma = 0.5) and find which methods now converge.",
    "Replace extragradient by optimistic steps, x - 2 eta g_t + eta g_(t-1), and compare its contraction per step.",
]


def norm_pdf(x, mu):
    return np.exp(-0.5 * (x - mu) ** 2) / np.sqrt(2 * np.pi)


def game_grads(x, y):
    """dV/dx and dV/dy for V = xy, by reverse-mode autodiff."""
    xt, yt = Tensor(x, requires_grad=True), Tensor(y, requires_grad=True)
    (xt * yt).backward()
    return float(xt.grad), float(yt.grad)


def run(seed=0):
    rng = np.random.default_rng(seed)
    theta, n = 1.5, 4000
    real, fake = rng.standard_normal(n), theta + rng.standard_normal(n)
    feats = lambda x: np.column_stack([np.ones_like(x), x, x * x])

    # the discriminator ascends V(D, G) = E_p log D + E_q log(1 - D); its logit is a + b x + c x^2
    w = Tensor(np.zeros(3), requires_grad=True)
    Fr, Ff = Tensor(feats(real)), Tensor(feats(fake))
    for _ in range(1500):
        w.grad[:] = 0
        value = sigmoid(Fr @ w).log().mean() + sigmoid(-(Ff @ w)).log().mean()
        value.backward()
        w.data += 0.25 * w.grad
    a, b, c = w.data
    # fresh samples, so the value is not flattered by the fit
    real2, fake2 = rng.standard_normal(n), theta + rng.standard_normal(n)
    D = lambda x: 1 / (1 + np.exp(-(feats(x) @ w.data)))
    v_hat = np.log(D(real2)).mean() + np.log(1 - D(fake2)).mean()
    grid = np.linspace(-8, 10, 20001)
    p, q = norm_pdf(grid, 0), norm_pdf(grid, theta)
    m = (p + q) / 2
    js = 0.5 * np.trapezoid(p * np.log(p / m), grid) + 0.5 * np.trapezoid(q * np.log(q / m), grid)
    v_star = -np.log(4) + 2 * js
    xs = np.linspace(-2.5, 4, 200)
    d_star = norm_pdf(xs, 0) / (norm_pdf(xs, 0) + norm_pdf(xs, theta))
    d_gap = np.abs(D(xs) - d_star).max()

    # the game min_x max_y xy, both players following their own gradient
    eta, T = 0.2, 60
    start = rng.standard_normal(2)
    start /= np.linalg.norm(start)
    paths = {}
    for name in ("simultaneous", "alternating", "extragradient"):
        x, y = start
        path = [(x, y)]
        for _ in range(T):
            gx, gy = game_grads(x, y)
            if name == "simultaneous":
                x, y = x - eta * gx, y + eta * gy
            elif name == "alternating":
                x = x - eta * gx
                y = y + eta * game_grads(x, y)[1]
            else:  # look ahead half a step, then step with the gradient found there
                hx, hy = game_grads(x - eta * gx, y + eta * gy)
                x, y = x - eta * hx, y + eta * hy
            path.append((x, y))
        paths[name] = np.array(path)
    radius = {k: np.linalg.norm(v, axis=1) for k, v in paths.items()}
    rate_sim = radius["simultaneous"][1:] / radius["simultaneous"][:-1]
    rate_eg = radius["extragradient"][1:] / radius["extragradient"][:-1]
    eg_theory = np.sqrt((1 - eta ** 2) ** 2 + eta ** 2)

    lab = labs.Lab()
    lab.row("discriminator's logit a + b x + c x^2", f"{a:.3f} {b:+.3f} x {c:+.3f} x^2   (optimal {theta ** 2 / 2:.3f} {-theta:+.3f} x)")
    lab.row("largest |D - D*| on [-2.5, 4]", f"{d_gap:.3f}")
    lab.row("value V(D, G) on fresh samples", f"{v_hat:.4f}   (-log 4 + 2 JS = {v_star:.4f},  -log 4 = {-np.log(4):.4f})")
    lab.row("simultaneous: growth per step", f"{rate_sim.mean():.6f}   (sqrt(1 + eta^2) = {np.sqrt(1 + eta ** 2):.6f})")
    lab.row(f"simultaneous: radius after {T} steps", f"{radius['simultaneous'][-1]:.2f} x the start")
    lab.row("alternating: radius stays within", f"{radius['alternating'].min():.3f} to {radius['alternating'].max():.3f}")
    lab.row("extragradient: shrink per step", f"{rate_eg.mean():.6f}   (theory {eg_theory:.6f})")
    lab.note = ("A discriminator trained to its optimum reports the Jensen-Shannon divergence between data and generator; "
                "but when both players step at once the game's field rotates, and plain gradient steps spiral away from "
                "the equilibrium they circle.")

    assert abs(b + theta) < 0.2 and abs(a - theta ** 2 / 2) < 0.2 and abs(c) < 0.1, "the logit is log p/q"
    assert d_gap < 0.06, "the trained discriminator is p/(p + q)"
    assert abs(v_hat - v_star) < 0.05 and v_hat > -np.log(4) + 0.3, "its value is -log 4 + 2 JS"
    assert np.allclose(rate_sim, np.sqrt(1 + eta ** 2), atol=1e-12), "simultaneous steps grow by sqrt(1 + eta^2)"
    assert abs(radius["simultaneous"][-1] - (1 + eta ** 2) ** (T / 2)) < 1e-9
    assert radius["alternating"].max() < 1.25 and radius["alternating"].min() > 0.8, "alternating steps orbit"
    assert np.allclose(rate_eg, eg_theory, atol=1e-12) and eg_theory < 1, "extragradient spirals in"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(xs, norm_pdf(xs, 0), color=labs.MUTED, ls="--", lw=1.2, label="data p = N(0, 1)")
    ax[0].plot(xs, norm_pdf(xs, theta), color=labs.MUTED, ls=":", lw=1.2, label="generator q = N(1.5, 1)")
    ax[0].plot(xs, d_star, color=labs.GOLD, lw=3, alpha=0.6, label="D* = p/(p + q)")
    ax[0].plot(xs, D(xs), color=labs.BLUE, label="trained discriminator")
    ax[0].set(title="The discriminator at its optimum", xlabel="x", ylabel="density, or D(x)")
    ax[0].legend(loc="upper right")
    for name, color in (("simultaneous", labs.RED), ("alternating", labs.BLUE), ("extragradient", labs.GREEN)):
        ax[1].plot(*paths[name].T, color=color, lw=1.3, label=name)
    ax[1].plot(0, 0, "o", color=labs.GOLD, ms=6)
    ax[1].plot(*start, "o", color=labs.INK, ms=4)
    ax[1].set(title=f"min max xy, {T} steps of size {eta}", xlabel="x (minimizes)", ylabel="y (maximizes)", aspect="equal")
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
