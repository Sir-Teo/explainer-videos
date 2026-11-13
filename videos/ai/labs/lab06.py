"""Lab 6: fit a logistic regression by Newton's method and by gradient descent, and count the correct digits."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Newton against gradient descent on logistic regression"
GOAL = ("Simulate two overlapping classes with correlated features, check the gradient X'(p - y)/n against the series' "
        "autodiff, then minimize the cross-entropy by Newton's method (weighted least squares) and by gradient descent.")
TASKS = [
    "Raise the features' correlation rho from 0.8 to 0.98. Which method's step count changes, and why?",
    "Move the class means apart (shift = 6) until a line separates the sample. Watch the weights' norm grow with every Newton step.",
    "Add a ridge penalty lam/2 |w|^2 to the loss, the gradient and the Hessian, and plot the weights' norm against lam.",
]


def loss_and_grad(X, y, w):
    """The mean cross-entropy in nats and its gradient, by reverse-mode autodiff."""
    wt = Tensor(w, requires_grad=True)
    z = Tensor(X) @ wt
    loss = ((z.exp() + 1.0).log() - z * y).mean()
    loss.backward()
    return float(loss.data), wt.grad


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, d, rho, shift = 400, 5, 0.8, 0.5
    cov = rho * np.ones((d, d)) + (1 - rho) * np.eye(d)
    y = (rng.random(n) < 0.5).astype(float)
    X = rng.multivariate_normal(np.zeros(d), cov, n) + shift * np.outer(y - 0.5, np.linspace(1, -1, d))
    X = np.column_stack([np.ones(n), X])
    sigmoid = lambda z: 1 / (1 + np.exp(-z))

    # the formula of chapter 5 against the autodiff of Part 4
    w0 = 0.3 * rng.standard_normal(d + 1)
    _, g_auto = loss_and_grad(X, y, w0)
    g_formula = X.T @ (sigmoid(X @ w0) - y) / n
    grad_gap = np.abs(g_auto - g_formula).max()

    def hessian(w):
        p = sigmoid(X @ w)
        return (X * (p * (1 - p))[:, None]).T @ X / n

    # Newton = iteratively reweighted least squares
    w, newton = np.zeros(d + 1), []
    for _ in range(12):
        newton.append(w.copy())
        _, g = loss_and_grad(X, y, w)
        w = w - np.linalg.solve(hessian(w), g)
    w_star = w
    f_star, g_star = loss_and_grad(X, y, w_star)
    eigs = np.linalg.eigvalsh(hessian(w_star))
    digits = [-np.log10(max(np.abs(v - w_star).max(), 1e-16)) for v in newton]
    newton_steps = next(k for k, v in enumerate(newton) if np.abs(v - w_star).max() < 1e-10)

    # gradient descent with the safe step 1/L, L = the largest eigenvalue of X'X/(4n)
    step = 1 / (np.linalg.eigvalsh(X.T @ X / (4 * n))[-1])
    w, gd_gap = np.zeros(d + 1), []
    for _ in range(1500):
        f, g = loss_and_grad(X, y, w)
        gd_gap.append(f - f_star)
        w = w - step * g
    gd_gap = np.array(gd_gap)
    gd_steps = int(np.argmax(gd_gap < 1e-6)) if (gd_gap < 1e-6).any() else len(gd_gap)
    newton_gap = np.array([loss_and_grad(X, y, v)[0] - f_star for v in newton])

    lab = labs.Lab()
    lab.row("gradient: autodiff against X'(p - y)/n", f"largest difference {grad_gap:.1e}")
    lab.row("Hessian X'SX/n at the minimum", f"eigenvalues {eigs[0]:.4f} to {eigs[-1]:.3f}   (all positive: convex)")
    lab.row("Newton: correct digits after each step", "  ".join(f"{v:.1f}" for v in digits[:newton_steps + 1]))
    lab.row("Newton: steps to 10 correct digits", f"{newton_steps}")
    lab.row("gradient descent: steps to a loss gap of 1e-6", f"{gd_steps}" + ("+" if gd_steps == len(gd_gap) else ""))
    lab.row("cross-entropy at the minimum", f"{f_star / np.log(2):.3f} bits per example")
    lab.note = ("Newton's correct digits roughly double with every step once it is close, so a handful of weighted "
                "least-squares fits do what gradient descent needs hundreds of steps for.")

    assert grad_gap < 1e-12, "autodiff agrees with the derived gradient"
    assert eigs[0] > 0 and np.abs(g_star).max() < 1e-12, "a convex loss, minimized"
    assert newton_steps <= 8, "Newton converges in a handful of steps"
    late = [k for k in range(1, newton_steps) if 1.0 < digits[k] < 7.0]
    assert late and all(digits[k + 1] > 1.6 * digits[k] for k in late), "quadratic convergence: the digits double"
    assert gd_steps > 20 * newton_steps, "gradient descent needs far more steps"
    assert np.all(np.diff(gd_gap) < 1e-12), "with step 1/L gradient descent never goes uphill"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].semilogy(np.arange(len(gd_gap)) + 1, np.maximum(gd_gap, 1e-16), color=labs.BLUE, label="gradient descent, step 1/L")
    ax[0].semilogy(np.arange(len(newton_gap)) + 1, np.maximum(newton_gap, 1e-16), "o-", color=labs.GOLD, label="Newton (IRLS)")
    ax[0].set(xscale="log", title="Loss above the minimum", xlabel="step (log scale)", ylabel="nats per example", ylim=(1e-16, 2))
    ax[0].legend()
    k = np.arange(newton_steps + 1)
    ax[1].bar(k, digits[:newton_steps + 1], color=labs.GOLD, width=0.6)
    for i in k:
        ax[1].text(i, max(digits[i], 0) + 0.3, f"{digits[i]:.1f}", ha="center", color=labs.INK, fontsize=9)
    ax[1].set(title="Newton: correct digits of the weights", xlabel="Newton steps taken", ylabel="correct decimal digits")
    lab.fig = fig
    return lab
