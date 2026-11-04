"""statkit.estimation: the tank factory game and small tools for point estimation (Part 9 of *Statistics, Built*).

    from explainer.stats.kit.estimation import tank_game, TANK_ESTIMATORS
    tank_game(lambda s: s.max(1) * 7 / 6 - 1, N=300, k=6)        # grade any estimator of N

An estimator here is a function of a (reps, k) array of captured serial numbers that returns one estimate per row,
so whole simulation studies run as array operations.  ``model`` changes how the factory numbers and how tanks get
captured, so a recipe can be graded on the model it assumed and on ones it did not.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

TANK_ESTIMATORS: dict[str, Callable[[np.ndarray], np.ndarray]] = {
    "mom": lambda s: 2 * s.mean(1) - 1,  # the method of moments
    "max": lambda s: s.max(1).astype(float),  # the maximum likelihood estimator
    "umvue": lambda s: s.max(1) * (1 + 1 / s.shape[1]) - 1,  # the maximum plus the average gap
    "range": lambda s: (s.max(1) - s.min(1)) * (s.shape[1] + 1) / (s.shape[1] - 1) - 1,  # unknown starting serial
}


def capture(rng: np.random.Generator, N: int, k: int, reps: int, weights=None, offset: int = 0) -> np.ndarray:
    """``reps`` factories of ``N`` tanks numbered offset + 1 .. offset + N; ``k`` captured from each without
    replacement, uniformly or with probabilities proportional to ``weights``.  Returns a (reps, k) int array."""
    if weights is None:
        # argsort of uniforms: a uniformly random k-subset per row, vectorized
        idx = np.argpartition(rng.random((reps, N)), k - 1, axis=1)[:, :k]
    else:
        p = np.asarray(weights, float)
        p = p / p.sum()
        idx = np.array([rng.choice(N, k, replace=False, p=p) for _ in range(reps)])
    return idx + 1 + offset


def tank_game(estimator: Callable[[np.ndarray], np.ndarray], N: int = 300, k: int = 6, reps: int = 10_000, seed: int = 0,
              model: str = "uniform") -> dict:
    """Grade an estimator of N on ``reps`` simulated factories.

    ``model``: ``"uniform"`` (the textbook assumption), ``"newer"`` (tanks with higher serials are up to three times as
    likely to be captured) or ``"offset"`` (serials start at 1,001, not 1).  Returns the bias, SD and RMSE with Monte
    Carlo standard errors, and the estimates themselves."""
    rng = np.random.Generator(np.random.PCG64(seed))
    if model == "uniform":
        s = capture(rng, N, k, reps)
    elif model == "newer":
        s = capture(rng, N, k, reps, weights=np.linspace(1, 3, N))
    elif model == "offset":
        s = capture(rng, N, k, reps, offset=1000)
    else:
        raise ValueError(f"unknown model {model!r}")
    est = np.asarray(estimator(s), float)
    err = est - N
    sd = est.std(ddof=1)
    mse = np.mean(err ** 2)
    return {"bias": float(err.mean()), "bias_mcse": float(sd / np.sqrt(reps)), "sd": float(sd),
            "rmse": float(np.sqrt(mse)), "rmse_mcse": float(np.std(err ** 2, ddof=1) / np.sqrt(reps) / (2 * np.sqrt(mse))),
            "estimates": est, "reps": reps}


def umvue_sd(N: int, k: int) -> float:
    """The exact SD of m(1 + 1/k) - 1 for k of N serials captured without replacement."""
    return float(np.sqrt((N - k) * (N + 1) / (k * (k + 2))))


def mom_sd(N: int, k: int) -> float:
    """The exact SD of 2 xbar - 1."""
    return float(np.sqrt((N + 1) * (N - k) / (3 * k)))


def newton(score: Callable[[float], float], dscore: Callable[[float], float], x0: float, tol: float = 1e-12,
           max_iter: int = 50) -> list[float]:
    """Newton's method for score(x) = 0; returns the whole path, starting point first."""
    path = [float(x0)]
    x = float(x0)
    for _ in range(max_iter):
        x_new = x - score(x) / dscore(x)
        path.append(float(x_new))
        if abs(x_new - x) < tol:
            break
        x = x_new
    return path


def observed_information(loglik: Callable[[float], float], theta: float, h: float | None = None) -> float:
    """-l''(theta) by a central second difference: the curvature that gives the MLE's standard error 1/sqrt(J)."""
    h = h or 1e-4 * max(1.0, abs(theta))
    return float(-(loglik(theta + h) - 2 * loglik(theta) + loglik(theta - h)) / h ** 2)
