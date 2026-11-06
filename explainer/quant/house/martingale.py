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


# ---------------------------------------------------------------------------
# Part 4, expanded: conditional expectation, the martingale transform, stopping, convergence, measure, betting
# ---------------------------------------------------------------------------
def cond_exp(x, labels, p=None) -> np.ndarray:
    """E[X | G], with G generated by the partition ``labels`` (one block label per world): the P-weighted average
    of ``x`` on each block, repeated over the block (Kolmogorov's definition on a partition)."""
    x = np.asarray(x, float)
    labels = np.asarray(labels)
    p = np.ones_like(x) if p is None else np.asarray(p, float)
    out = np.empty_like(x)
    for b in np.unique(labels):
        m = labels == b
        out[m] = (p[m] * x[m]).sum() / p[m].sum()
    return out


def martingale_transform(H, dM) -> np.ndarray:
    """(H . M)_n = sum_{k<=n} H_k dM_k: the stake H_k, fixed before step k, times the fair increment dM_k."""
    return np.concatenate([[0.0], np.cumsum(np.asarray(H, float) * np.asarray(dM, float))])


def system_stakes(system: str, wins, base: float = 1.0, limit: float = np.inf) -> np.ndarray:
    """The stake a betting system places before each even-money round, given the outcomes ``wins`` (bool, shape
    (rounds,) or (sessions, rounds)).  Every stake depends only on earlier outcomes (it is predictable).  Systems:
    "flat", "martingale" (double after a loss), "dalembert" (+1 after a loss, -1 after a win), "fibonacci" (one step
    up the sequence after a loss, two down after a win), "labouchere" (the line 1 2 3 4: stake first + last; a win
    crosses them out, a loss appends the stake), "oscar" (Oscar's grind: aim to win one unit per series, raising the
    stake by one after a win, never past what completes the series).  Stakes are capped at ``limit``."""
    W = np.atleast_2d(np.asarray(wins, bool))
    n, T = W.shape
    H = np.empty((n, T))
    if system == "flat":
        H[:] = base
    elif system == "martingale":
        h = np.full(n, base)
        for t in range(T):
            H[:, t] = np.minimum(h, limit)
            h = np.where(W[:, t], base, 2 * h)
    elif system == "dalembert":
        h = np.full(n, base)
        for t in range(T):
            H[:, t] = np.minimum(h, limit)
            h = np.where(W[:, t], np.maximum(h - base, base), h + base)
    elif system == "fibonacci":
        fib = [1.0, 1.0]
        while len(fib) < T + 3:
            fib.append(fib[-1] + fib[-2])
        fib = np.array(fib)
        k = np.zeros(n, int)
        for t in range(T):
            H[:, t] = np.minimum(base * fib[k], limit)
            k = np.where(W[:, t], np.maximum(k - 2, 0), k + 1)
    elif system == "labouchere":
        start = np.array([1.0, 2.0, 3.0, 4.0]) * base
        cap = len(start) + T + 1
        line = np.zeros((n, cap))
        line[:, :4] = start
        lo, hi = np.zeros(n, int), np.full(n, 3)
        rows = np.arange(n)
        for t in range(T):
            stake = np.where(hi > lo, line[rows, lo] + line[rows, hi], line[rows, lo])
            H[:, t] = np.minimum(stake, limit)
            w = W[:, t]
            lo = np.where(w, lo + 1, lo)
            hi = np.where(w, hi - 1, hi)
            app = ~w
            hi = np.where(app, hi + 1, hi)
            line[rows[app], hi[app]] = H[app, t]
            done = hi < lo  # the line is crossed out: start a new one
            if done.any():
                line[done] = 0.0
                line[done, :4] = start
                lo[done], hi[done] = 0, 3
    elif system == "oscar":
        h = np.full(n, base)
        series = np.zeros(n)
        for t in range(T):
            need = base - series
            H[:, t] = np.minimum(np.minimum(h, need), limit)
            gain = np.where(W[:, t], H[:, t], -H[:, t])
            series += gain
            h = np.where(W[:, t], H[:, t] + base, H[:, t])
            fin = series >= base - 1e-12
            series[fin], h[fin] = 0.0, base
    else:
        raise ValueError(f"unknown system {system!r}")
    return H if np.ndim(wins) > 1 else H[0]


def first_passage_survival(n) -> np.ndarray:
    """P(tau_1 > n) for a fair +-1 walk from 0, tau_1 the first time it reaches +1: by the reflection principle it is
    P(S_n in {0, 1}) = C(n, floor(n/2)) / 2^n, about sqrt(2 / (pi n))."""
    from scipy.special import gammaln

    n = np.asarray(n, float)
    m = np.floor(n / 2)
    return np.exp(gammaln(n + 1) - gammaln(m + 1) - gammaln(n - m + 1) - n * np.log(2))


def pattern_wait(pat, m: int = 2) -> int:
    """Expected i.i.d. draws (``m`` equally likely symbols) until ``pat`` first appears: the sum of m^k over the k for
    which the pattern's first k symbols equal its last k (Conway's leading numbers; Li 1980, by optional stopping on
    a casino of fair gamblers)."""
    return sum(m ** k for k in range(1, len(pat) + 1) if pat[:k] == pat[-k:])


def penney_odds(a: str, b: str, m: int = 2) -> float:
    """P(pattern ``b`` appears before ``a``) in fair i.i.d. draws (Conway's formula with correlations
    c(x, y) = sum over k of m^k when x's last k symbols are y's first k)."""
    def c(x, y):
        return sum(m ** k for k in range(1, min(len(x), len(y)) + 1) if x[-k:] == y[:k])

    aa, ab, ba, bb = c(a, a), c(a, b), c(b, a), c(b, b)
    # odds for b against a are (aa - ab) : (bb - ba)
    return (aa - ab) / ((aa - ab) + (bb - ba))


def polya_urn(n_draws: int, red: int = 1, blue: int = 1, n_urns: int = 1, seed=0) -> np.ndarray:
    """Polya's urn: draw a ball, return it with another of the same colour.  The red fraction after each draw,
    shape (n_urns, n_draws + 1): a bounded martingale, so it converges (to a Beta(red, blue) limit)."""
    rng = np.random.default_rng(seed)
    R = np.full(n_urns, float(red))
    tot = float(red + blue)
    out = np.empty((n_urns, n_draws + 1))
    out[:, 0] = R / tot
    for k in range(n_draws):
        R += rng.random(n_urns) < R / tot
        tot += 1
        out[:, k + 1] = R / tot
    return out


def upcrossings(x, a: float, b: float) -> dict:
    """Completed upcrossings of [a, b] by the path ``x``, and the upcrossing trader's wealth: buy one unit when the
    path is at or below a, sell when it is at or above b (a predictable stake).  Doob: (b - a) U_n <= (H.M)_n +
    (x_n - a)^-."""
    x = np.asarray(x, float)
    hold, U, H = False, 0, np.zeros(len(x) - 1)
    starts, ends = [], []
    for k in range(len(x) - 1):
        if not hold and x[k] <= a:
            hold = True
            starts.append(k)
        elif hold and x[k] >= b:
            hold = False
            U += 1
            ends.append(k)
        H[k] = 1.0 if hold else 0.0
    if hold and x[-1] >= b:
        U += 1
        ends.append(len(x) - 1)
    return {"U": U, "H": H, "wealth": martingale_transform(H, np.diff(x)), "starts": starts, "ends": ends}


def esscher_tilt(x, target: float):
    """Esscher (1932): weights w proportional to e^(theta x) on the sample ``x`` (log returns), with theta chosen so
    that E_Q[e^x] = e^target (every asset earns the riskless rate under Q).  Returns (theta, w), w summing to one."""
    from scipy.optimize import brentq

    x = np.asarray(x, float)

    def w(th):
        v = np.exp(th * (x - x.mean()))
        return v / v.sum()

    th = brentq(lambda t: np.log(w(t) @ np.exp(x)) - target, -200, 200, xtol=1e-12)
    return th, w(th)


def hellinger_affinity(p, q) -> np.ndarray:
    """sqrt(p q) + sqrt((1 - p)(1 - q)) for coins p and q; Kakutani: the infinite products of the coins are
    equivalent when the product of these affinities is positive, and mutually singular when it is zero."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    return np.sqrt(p * q) + np.sqrt((1 - p) * (1 - q))


def ecf_alpha(x, t=None) -> dict:
    """Koutrouvelis (1980): for a symmetric stable law |phi(t)| = exp(-|c t|^alpha), so log(-log |phi(t)|^2) is a
    line in log t with slope alpha.  Fit it on the empirical characteristic function of the standardized sample."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    z = (x - np.median(x)) / (np.percentile(x, 75) - np.percentile(x, 25))
    t = np.linspace(0.1, 1.0, 10) if t is None else np.asarray(t, float)
    phi = np.abs(np.exp(1j * np.outer(t, z)).mean(axis=1))
    y = np.log(-np.log(phi ** 2))
    slope, icpt = np.polyfit(np.log(t), y, 1)
    return {"alpha": float(slope), "intercept": float(icpt), "t": t, "y": y, "phi": phi}


class ONSBettor:
    """Testing by betting with an online-Newton-step stake (Cutkosky and Orabona 2018, as used by Waudby-Smith and
    Ramdas): wealth W_t = prod (1 + lam_t x_t) with lam_t chosen from the past only, |lam_t| <= 1/2.  Under the null
    that x_t has conditional mean zero (and |x_t| < 1) W is a nonnegative martingale: anytime-valid by Ville."""

    def __init__(self, shape=()):
        self.lam = np.zeros(shape)
        self.A = np.ones(shape)
        self.logw = np.zeros(shape)

    def update(self, x):
        x = np.asarray(x, float)
        self.logw = self.logw + np.log1p(self.lam * x)
        z = x / (1 + self.lam * x)
        self.A = self.A + z * z
        self.lam = np.clip(self.lam + 2 / (2 - np.log(3)) * z / self.A, -0.5, 0.5)
        return np.exp(self.logw)


class AGrapaBettor:
    """The approximate growth-rate adaptive bet (aGRAPA, Waudby-Smith and Ramdas): lam_t = mu_hat / (var_hat +
    mu_hat^2) from the past, clipped to [-1/2, 1/2]; the Kelly fraction of a small edge, estimated."""

    def __init__(self, shape=(), prior_var=0.25):
        self.n = np.zeros(shape)
        self.s1 = np.zeros(shape)
        self.s2 = np.full(shape, prior_var)
        self.logw = np.zeros(shape)

    def update(self, x):
        x = np.asarray(x, float)
        mu = self.s1 / (self.n + 1)
        m2 = self.s2 / (self.n + 1)
        lam = np.clip(mu / np.maximum(m2, 1e-8), -0.5, 0.5)
        self.logw = self.logw + np.log1p(lam * x)
        self.n = self.n + 1
        self.s1 = self.s1 + x
        self.s2 = self.s2 + x * x
        return np.exp(self.logw)


def betting_cs(x, grid, alpha: float = 0.05, lo: float = 0.0, hi: float = 1.0) -> dict:
    """A continuous-mean confidence sequence for bounded observations.

    Assume E[X_t | F_{t-1}] = mu for one common mu and lo <= X_t <= hi.
    Predictable, nonnegative stakes bet on both signs of (X_t - m)/(hi-lo),
    without clipping or candidate-dependent normalization. Each direction has
    error budget alpha/2. Its wealth is monotone in m, so rounding the grid
    crossings OUTWARD encloses the continuous inversion, even when mu is not
    on the supplied grid. Endpoints lo and hi are always included.

    Stakes use a past-only variance estimate; their choice affects power, not
    validity. This is the predictable betting construction of Waudby-Smith and
    Ramdas (2024), rather than a claim that market returns have a constant mean.
    """
    x = np.asarray(x, float)
    grid = np.asarray(grid, float)
    if not (np.isfinite(lo) and np.isfinite(hi) and lo < hi and 0 < alpha < 1):
        raise ValueError("require finite lo < hi and 0 < alpha < 1")
    if x.ndim != 1 or not np.isfinite(x).all() or np.any((x < lo) | (x > hi)):
        raise ValueError("observations must be a finite vector within [lo, hi]")
    if (grid.ndim != 1 or not len(grid) or not np.isfinite(grid).all()
            or np.any((grid < lo) | (grid > hi))):
        raise ValueError("mean grid must be a nonempty finite vector within [lo, hi]")
    grid = np.unique(np.r_[lo, grid, hi])
    log_up, log_dn = np.zeros(len(grid)), np.zeros(len(grid))
    threshold = np.log(2 / alpha)
    running_sum, squared_errors = 0.0, 0.25
    lower_so_far, upper_so_far = lo, hi
    lower, upper = np.empty(len(x)), np.empty(len(x))
    for t, v in enumerate(x):
        variance_forecast = squared_errors / (t + 1)
        stake = min(0.5, np.sqrt(2 * threshold / ((t + 1) * variance_forecast)))
        centered = (v - grid) / (hi - lo)
        log_up += np.log1p(stake * centered)
        log_dn += np.log1p(-stake * centered)
        # W_up decreases in m; W_dn increases in m. Keep the rejected neighbour
        # as an outer bracket, so finite grid resolution cannot cause undercoverage.
        survives_up = np.flatnonzero(log_up < threshold)
        survives_dn = np.flatnonzero(log_dn < threshold)
        lower_so_far = max(lower_so_far, grid[max(int(survives_up[0]) - 1, 0)])
        upper_so_far = min(upper_so_far, grid[min(int(survives_dn[-1]) + 1, len(grid) - 1)])
        lower[t], upper[t] = ((lower_so_far, upper_so_far) if lower_so_far <= upper_so_far
                            else (np.nan, np.nan))
        normalized = (v - lo) / (hi - lo)
        forecast = running_sum / t if t else 0.5
        squared_errors += (normalized - forecast) ** 2
        running_sum += normalized
    return {"lower": lower, "upper": upper}


def e_bh(e, alpha: float = 0.1) -> np.ndarray:
    """Wang and Ramdas (2022): reject the k* largest e-values, k* = max{k : e_(k) >= K / (alpha k)}; controls the
    false discovery rate at alpha under any dependence.  Returns the indices rejected."""
    e = np.asarray(e, float)
    K = len(e)
    order = np.argsort(e)[::-1]
    ok = np.flatnonzero(e[order] >= K / (alpha * np.arange(1, K + 1)))
    return order[: ok.max() + 1] if len(ok) else order[:0]
