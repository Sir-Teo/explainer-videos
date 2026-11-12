"""Lab 17: differential machine learning in one dimension: train on payoffs and on their pathwise slopes."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import bs

TITLE = "Learn a price from payoffs, with and without their derivatives"
GOAL = ("Draw a starting price and one path each; the label is that path's payoff (pure noise around the price). "
        "Fit a small model to the payoffs alone, then to payoffs and pathwise deltas (Huge and Savine's "
        "differential regression), and compare the learned price and delta with Black-Scholes.")
TASKS = [
    "Cut the sample to 256 paths. Which fit survives?",
    "Raise the polynomial degree to 12 without the derivative labels. What does the delta do?",
    "Replace the polynomial by a small network (explainer.quant.house.deep.train_differential, needs torch).",
]


def basis(x, degree):
    """Polynomial features of the standardized spot and their derivatives with respect to the spot."""
    z = (x - 100.0) / 20.0
    P = np.stack([z ** j for j in range(degree + 1)], axis=1)
    dP = np.stack([j * z ** (j - 1) / 20.0 if j else np.zeros_like(z) for j in range(degree + 1)], axis=1)
    return P, dP


def fit(x, y, dy, degree, lam):
    """Least squares on values, plus lam times least squares on derivatives (lam = 0: values only)."""
    P, dP = basis(x, degree)
    scale = y.std() / dy.std()
    A = P.T @ P + lam * scale ** 2 * dP.T @ dP + 1e-8 * np.eye(degree + 1)
    b = P.T @ y + lam * scale ** 2 * dP.T @ dy
    return np.linalg.solve(A, b)


def run(seed=0):
    K, T, sigma, n, degree = 100.0, 1.0, 0.2, 1024, 7
    rng = np.random.default_rng(seed)
    S0 = rng.uniform(60, 140, n)
    ST = S0 * np.exp(-0.5 * sigma ** 2 * T + sigma * np.sqrt(T) * rng.standard_normal(n))
    y = np.maximum(ST - K, 0)  # one payoff per starting point
    dy = (ST > K) * ST / S0  # its pathwise derivative with respect to the starting point
    grid = np.linspace(65, 135, 141)
    P, dP = basis(grid, degree)
    truth, delta = bs.price(grid, K, T, sigma), bs.greeks(grid, K, T, sigma)["delta"]
    lab, err = labs.Lab(), {}
    for name, lam in (("payoffs only", 0.0), ("payoffs + pathwise deltas", 1.0)):
        w = fit(S0, y, dy, degree, lam)
        err[name] = (np.sqrt(np.mean((P @ w - truth) ** 2)), np.sqrt(np.mean((dP @ w - delta) ** 2)), w)
        lab.row(name, f"price RMSE {err[name][0]:.3f}   delta RMSE {err[name][1]:.4f}")
    a, b = err["payoffs only"], err["payoffs + pathwise deltas"]
    mid = len(grid) // 2  # spot 100
    lab.row("At the money: delta", f"Black-Scholes {delta[mid]:.3f}   payoffs only {(dP @ a[2])[mid]:.3f}   "
                                   f"with pathwise deltas {(dP @ b[2])[mid]:.3f}")
    lab.note = "Each path gives a payoff and, for free, its slope. The slope label carries most of the information."
    assert b[0] < 0.6 * a[0] and b[1] < 0.4 * a[1]

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].scatter(S0, y, s=3, color=labs.MUTED, alpha=0.5, label="one payoff per path")
    ax[0].plot(grid, truth, color=labs.INK, lw=2.4, label="Black-Scholes")
    ax[0].plot(grid, P @ a[2], color=labs.LOSS, label="payoffs only")
    ax[0].plot(grid, P @ b[2], color=labs.GAIN, label="with pathwise deltas")
    ax[0].set(title="The learned price", xlabel="spot", ylabel="value", ylim=(-3, 45))
    ax[0].legend(fontsize=8)
    ax[1].plot(grid, delta, color=labs.INK, lw=2.4, label="Black-Scholes delta")
    ax[1].plot(grid, dP @ a[2], color=labs.LOSS, label="payoffs only")
    ax[1].plot(grid, dP @ b[2], color=labs.GAIN, label="with pathwise deltas")
    ax[1].set(title="The learned delta", xlabel="spot", ylim=(-0.3, 1.3))
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
