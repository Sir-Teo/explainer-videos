"""The House's martingale tools (Part 4, *Martingales and Measure*): fair games, measured and tested.

* :func:`doubling`: the "martingale" betting system (double after each loss), with a finite bankroll;
* :func:`gamblers_ruin`: the chance a walk from ``a`` hits ``b`` before 0, fair or biased;
* :func:`doob_decomposition`: a process split into a predictable drift and a martingale;
* :func:`likelihood_ratio`: the Radon–Nikodym density process of one coin against another (a martingale under the
  first);
* :func:`stable_mcculloch`: McCulloch's (1986) quantile estimator of a stable law's (alpha, beta, scale, location);
* :func:`return_probability`: Mantegna and Stanley's (1995) probability of return to the origin across time scales;
* :class:`EProcess`: testing by betting (Ville 1939; Shafer and Vovk; Ramdas et al. 2023): an e-process for "the
  increments have conditional mean zero", anytime-valid by Ville's inequality P(sup E >= 1/alpha) <= alpha.  The
  House's e-value monitor (used again in Part 26).
"""

from __future__ import annotations

import numpy as np
from scipy import interpolate


# ---------------------------------------------------------------------------
def doubling(wins, base: float = 1.0, bankroll: float = 1023.0, target: float | None = None) -> dict:
    """Play the doubling system on the outcomes ``wins`` (bool per round, even-money bets): bet ``base``; after a loss
    double the bet; after a win go back to ``base``.  A bet larger than the bankroll can't be placed: the player
    stakes what is left and, if that loses, is ruined.  Stops at ruin, or when wealth reaches ``target``.
    Returns the wealth path (starting at ``bankroll``), ``ruined`` and the round it stopped."""
    w = float(bankroll)
    bet = base
    path = [w]
    for i, win in enumerate(np.asarray(wins, bool)):
        stake = min(bet, w)
        if win:
            w += stake
            bet = base
        else:
            w -= stake
            bet = 2 * bet
        path.append(w)
        if w <= 0:
            return {"wealth": np.array(path), "ruined": True, "stopped": i + 1}
        if target is not None and w >= target:
            return {"wealth": np.array(path), "ruined": False, "stopped": i + 1}
    return {"wealth": np.array(path), "ruined": False, "stopped": len(path) - 1}


def gamblers_ruin(a: int, b: int, p: float = 0.5) -> float:
    """P(a walk started at ``a`` with up-probability ``p`` hits ``b`` before 0)."""
    if np.isclose(p, 0.5):
        return a / b
    q = (1 - p) / p
    return (1 - q ** a) / (1 - q ** b)


# ---------------------------------------------------------------------------
def doob_decomposition(x, predicted_increment) -> dict:
    """``x_n = x_0 + A_n + M_n`` with ``A_n = sum_{k<=n} E[x_k - x_{k-1} | F_{k-1}]`` (given as
    ``predicted_increment[k-1]``, known one step ahead) and ``M`` the martingale part."""
    x = np.asarray(x, float)
    p = np.asarray(predicted_increment, float)
    A = np.concatenate([[0.0], np.cumsum(p[: len(x) - 1])])
    M = x - x[0] - A
    return {"A": A, "M": M}


def likelihood_ratio(heads, p: float, q: float) -> np.ndarray:
    """dQ/dP on the first n tosses, for a coin with P(heads) = p under P and q under Q: a P-martingale with mean 1."""
    h = np.asarray(heads, bool)
    step = np.where(h, q / p, (1 - q) / (1 - p))
    return np.concatenate([[1.0], np.cumprod(step)])


# ---------------------------------------------------------------------------
# McCulloch (1986), "Simple consistent estimators of stable distribution parameters": tables of
# nu_alpha = (x95 - x05) / (x75 - x25) and nu_beta = (x95 + x05 - 2 x50) / (x95 - x05) against (alpha, beta).
_NU_A = np.array([2.439, 2.5, 2.6, 2.7, 2.8, 3.0, 3.2, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 25.0])
_NU_B = np.array([0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0])
_ALPHA = np.array([
    [2.000, 2.000, 2.000, 2.000, 2.000, 2.000, 2.000],
    [1.916, 1.924, 1.924, 1.924, 1.924, 1.924, 1.924],
    [1.808, 1.813, 1.829, 1.829, 1.829, 1.829, 1.829],
    [1.729, 1.730, 1.737, 1.745, 1.745, 1.745, 1.745],
    [1.664, 1.663, 1.663, 1.668, 1.676, 1.676, 1.676],
    [1.563, 1.560, 1.553, 1.548, 1.547, 1.547, 1.547],
    [1.484, 1.480, 1.471, 1.460, 1.448, 1.438, 1.438],
    [1.391, 1.386, 1.378, 1.364, 1.337, 1.318, 1.318],
    [1.279, 1.273, 1.266, 1.250, 1.210, 1.184, 1.150],
    [1.128, 1.121, 1.114, 1.101, 1.067, 1.027, 0.973],
    [1.029, 1.021, 1.014, 1.004, 0.974, 0.935, 0.874],
    [0.896, 0.892, 0.887, 0.883, 0.855, 0.823, 0.769],
    [0.818, 0.812, 0.806, 0.801, 0.780, 0.756, 0.691],
    [0.698, 0.695, 0.692, 0.689, 0.676, 0.656, 0.595],
    [0.593, 0.590, 0.588, 0.586, 0.579, 0.563, 0.513]])
_BETA = np.array([
    [0.000, 2.160, 1.000, 1.000, 1.000, 1.000, 1.000],
    [0.000, 1.592, 3.390, 1.000, 1.000, 1.000, 1.000],
    [0.000, 0.759, 1.800, 1.000, 1.000, 1.000, 1.000],
    [0.000, 0.482, 1.048, 1.694, 1.000, 1.000, 1.000],
    [0.000, 0.360, 0.760, 1.232, 2.229, 1.000, 1.000],
    [0.000, 0.253, 0.518, 0.823, 1.575, 1.000, 1.000],
    [0.000, 0.203, 0.410, 0.632, 1.244, 1.906, 1.000],
    [0.000, 0.165, 0.332, 0.499, 0.943, 1.560, 1.000],
    [0.000, 0.136, 0.271, 0.404, 0.689, 1.230, 2.195],
    [0.000, 0.109, 0.216, 0.323, 0.539, 0.827, 1.917],
    [0.000, 0.096, 0.190, 0.284, 0.472, 0.693, 1.759],
    [0.000, 0.082, 0.163, 0.243, 0.412, 0.601, 1.596],
    [0.000, 0.074, 0.147, 0.220, 0.377, 0.546, 1.482],
    [0.000, 0.064, 0.128, 0.191, 0.330, 0.478, 1.362],
    [0.000, 0.056, 0.112, 0.167, 0.285, 0.428, 1.274]])
# nu_c = (x75 - x25) / scale, as a function of (alpha, beta)
_A_GRID = np.array([2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5])
_B_GRID = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
_NU_C = np.array([
    [1.908, 1.908, 1.908, 1.908, 1.908],
    [1.914, 1.915, 1.916, 1.918, 1.921],
    [1.921, 1.922, 1.927, 1.936, 1.947],
    [1.927, 1.930, 1.943, 1.961, 1.987],
    [1.933, 1.940, 1.962, 1.997, 2.043],
    [1.939, 1.952, 1.988, 2.045, 2.116],
    [1.946, 1.967, 2.022, 2.106, 2.211],
    [1.955, 1.984, 2.067, 2.188, 2.333],
    [1.965, 2.007, 2.125, 2.294, 2.491],
    [1.980, 2.040, 2.205, 2.435, 2.696],
    [2.000, 2.085, 2.311, 2.624, 2.973],
    [2.040, 2.149, 2.461, 2.886, 3.356],
    [2.098, 2.244, 2.676, 3.265, 3.912],
    [2.189, 2.392, 3.004, 3.844, 4.775],
    [2.337, 2.635, 3.542, 4.808, 6.247],
    [2.588, 3.073, 4.534, 6.636, 9.144]])


def stable_mcculloch(x) -> dict:
    """McCulloch's quantile estimates of a stable law's index ``alpha`` (2 is Gaussian), skewness ``beta``, scale and
    location (the median, a robust stand-in).  Fast, and good enough to compare markets and time scales."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    q05, q25, q50, q75, q95 = np.percentile(x, [5, 25, 50, 75, 95])
    nu_a = (q95 - q05) / (q75 - q25)
    nu_b = (q95 + q05 - 2 * q50) / (q95 - q05)
    na = float(np.clip(nu_a, _NU_A[0], _NU_A[-1]))
    nb = float(np.clip(abs(nu_b), _NU_B[0], _NU_B[-1]))
    alpha = float(interpolate.RegularGridInterpolator((_NU_A, _NU_B), _ALPHA)([na, nb])[0])
    beta = float(np.sign(nu_b) * min(interpolate.RegularGridInterpolator((_NU_A, _NU_B), _BETA)([na, nb])[0], 1.0))
    a_ = float(np.clip(alpha, 0.5, 2.0))
    nu_c = float(interpolate.RegularGridInterpolator((_A_GRID[::-1], _B_GRID), _NU_C[::-1])([a_, min(abs(beta), 1.0)])[0])
    scale = (q75 - q25) / nu_c
    return {"alpha": alpha, "beta": beta, "scale": float(scale), "loc": float(q50), "nu_alpha": float(nu_a)}


def return_probability(r, horizons, width: float | None = None) -> dict:
    """Mantegna and Stanley (1995): the density of h-period sums at zero, P_h(0), for each h in ``horizons``
    (non-overlapping sums of the demeaned returns ``r``).  For a stable law P_h(0) ~ h^(-1/alpha): a Gaussian gives a
    slope of -1/2 on log-log axes.  ``width``: the half-width of the bin around zero, as a fraction of each scale's
    standard deviation (default 0.1)."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)] - np.nanmean(r)
    w = 0.1 if width is None else width
    p0 = []
    for h in horizons:
        n = len(r) // h
        s = r[: n * h].reshape(n, h).sum(axis=1)
        eps = w * s.std()
        p0.append(np.mean(np.abs(s) <= eps) / (2 * eps))
    hz = np.asarray(horizons, float)
    p0 = np.asarray(p0)
    slope, icpt = np.polyfit(np.log(hz), np.log(p0), 1)
    return {"h": hz, "p0": p0, "slope": float(slope), "alpha": float(-1 / slope), "intercept": float(icpt)}


# ---------------------------------------------------------------------------
class EProcess:
    """Testing by betting: the null is that each increment ``x_t`` (already scaled so that |x_t| < 1, e.g.
    x_t = r_t / c) has conditional mean zero.  A gambler starting with 1 stakes a fraction ``lam`` of wealth on
    each round, ``W_t = W_{t-1}(1 + lam_t x_t)``; under the null W is a nonnegative martingale, so by Ville's
    inequality P(W ever reaches 1/alpha) <= alpha, whenever one looks.  This class mixes a grid of constant bets
    (positive and negative), each with equal starting weight, which is itself an e-process.

    ``predict``, if given, is a sign known before each round (e.g. yesterday's return): the bet is then on
    ``sign_t * x_t``, which tests "no predictability from that sign"."""

    def __init__(self, lams=(-0.5, -0.25, -0.1, -0.05, 0.05, 0.1, 0.25, 0.5)):
        self.lams = np.asarray(lams, float)
        self.log_w = np.zeros(len(self.lams))
        self.history = [1.0]

    def update(self, x: float) -> float:
        if not abs(x) < 1:
            raise ValueError("scale the increments so that |x| < 1")
        self.log_w += np.log1p(self.lams * x)
        v = float(np.mean(np.exp(self.log_w)))
        self.history.append(v)
        return v

    def run(self, xs) -> np.ndarray:
        for x in np.asarray(xs, float):
            self.update(x)
        return np.asarray(self.history)

    @property
    def value(self) -> float:
        return self.history[-1]

    def rejected(self, alpha: float = 0.05) -> bool:
        return max(self.history) >= 1 / alpha
