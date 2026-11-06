"""statkit.chains -- the coupling and mixing lab (Part 44 of *Statistics, Built*, "Martingales, Markov Chains and
Brownian Motion").

* **Markov's chain:** transition counts and their MLE for a two-state sequence, the stationary law, and the variance of a
  block count under the chain against independence (Markov 1913, on *Eugene Onegin*).
* **Mixing:** total variation distances max_x ||P^t(x, .) - pi||_TV computed exactly for finite chains (the lazy walk on
  a cycle; the lazy walk on the hypercube, lumped by Hamming weight); mixing times; spectral gaps; coupling times;
  Bayer & Diaconis's (1992) exact distance of a 52-card deck from uniform after k riffle shuffles, from the Eulerian
  numbers.
* **Martingales:** gambler's ruin probabilities and durations; likelihood-ratio (betting) paths and Ville's bound;
  Azuma-Hoeffding and McDiarmid bounds; Polya's urn.
* **Random walks and Brownian motion:** Polya's recurrence by simulation; the Levy-Ciesielski construction with Schauder
  functions; quadratic variation; Dickey-Fuller statistics under a random walk; the LIL envelope.
* **MCMC output:** batch-means and autocorrelation-corrected standard errors; the AR(1) least-squares fit.

Tested in ``tests/test_stats_kit_chains.py``.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# Markov's two-state chain
# ---------------------------------------------------------------------------------------------------------------
def two_state_fit(bits) -> dict:
    """Transition counts n_ab and the MLE p_ab = n_ab / n_a. for a 0/1 sequence, with the stationary probability of 1
    and the lag-one correlation r = p_11 - p_01."""
    x = np.asarray(bits, int)
    a, b = x[:-1], x[1:]
    n = np.array([[np.sum((a == i) & (b == j)) for j in (0, 1)] for i in (0, 1)], float)
    P = n / n.sum(1, keepdims=True)
    pi1 = P[0, 1] / (P[0, 1] + P[1, 0])
    return {"counts": n, "P": P, "pi1": float(pi1), "r": float(P[1, 1] - P[0, 1]), "share1": float(x.mean())}


def block_count_variance(p: float, r: float, m: int) -> float:
    """Var of the number of 1s in m consecutive steps of a stationary two-state chain with P(1) = p and lag-one
    correlation r (autocorrelation r^k at lag k): m p q [1 + 2 sum_{k<m} (1 - k/m) r^k]."""
    k = np.arange(1, m)
    return float(m * p * (1 - p) * (1 + 2 * np.sum((1 - k / m) * r ** k)))


# ---------------------------------------------------------------------------------------------------------------
# Total variation and mixing
# ---------------------------------------------------------------------------------------------------------------
def tv(p, q) -> float:
    return float(0.5 * np.sum(np.abs(np.asarray(p, float) - np.asarray(q, float))))


def stationary(P) -> np.ndarray:
    P = np.asarray(P, float)
    w, v = np.linalg.eig(P.T)
    i = int(np.argmin(np.abs(w - 1)))
    pi = np.real(v[:, i])
    return pi / pi.sum()


def lazy_cycle(n: int) -> np.ndarray:
    """The lazy random walk on Z_n: stay with probability 1/2, else step to a neighbour."""
    P = np.zeros((n, n))
    for i in range(n):
        P[i, i] += 0.5
        P[i, (i + 1) % n] += 0.25
        P[i, (i - 1) % n] += 0.25
    return P


def lazy_hypercube_weight(d: int) -> np.ndarray:
    """The lazy walk on {0, 1}^d (pick a coordinate, set it to a fair coin), lumped by Hamming weight k = 0..d.  From the
    all-zeros start, its distance from uniform equals the lumped chain's distance from Binomial(d, 1/2)."""
    P = np.zeros((d + 1, d + 1))
    for k in range(d + 1):
        P[k, k] += 0.5
        if k < d:
            P[k, k + 1] += 0.5 * (d - k) / d
        if k > 0:
            P[k, k - 1] += 0.5 * k / d
    return P


def distance_curve(P, pi, ts, starts=None) -> np.ndarray:
    """d(t) = max over starting states of ||P^t(x, .) - pi||_TV, for each t in ``ts`` (increasing)."""
    P = np.asarray(P, float)
    pi = np.asarray(pi, float)
    n = len(pi)
    starts = list(range(n)) if starts is None else list(starts)
    out, M, t_prev = [], np.eye(n)[starts], 0
    for t in ts:
        for _ in range(int(t) - t_prev):
            M = M @ P
        t_prev = int(t)
        out.append(max(tv(M[i], pi) for i in range(len(starts))))
    return np.array(out)


def mixing_time(P, pi, eps: float = 0.25, t_max: int = 1_000_000, starts=None) -> int:
    P = np.asarray(P, float)
    n = len(pi)
    starts = list(range(n)) if starts is None else list(starts)
    M = np.eye(n)[starts]
    for t in range(1, t_max + 1):
        M = M @ P
        if max(tv(M[i], pi) for i in range(len(starts))) <= eps:
            return t
    return -1


def spectral_gap(P) -> float:
    """1 - lambda_2 for a reversible chain (the second largest eigenvalue modulus): its inverse is the relaxation time."""
    w = np.sort(np.abs(np.linalg.eigvals(np.asarray(P, float))))[::-1]
    return float(1 - w[1])


def coupling_time_cycle(n: int, reps: int, rng: np.random.Generator) -> np.ndarray:
    """Two lazy walkers on Z_n started opposite each other; at each step a fair coin decides which one moves (one
    step left or right), so the gap does a simple random walk until they meet: the classical coupling."""
    out = np.empty(reps)
    for r in range(reps):
        gap, t = n // 2, 0
        while gap % n != 0:
            gap += rng.choice((-1, 1))
            t += 1
        out[r] = t
    return out


def _eulerian(n: int) -> list:
    """Eulerian numbers A(n, k), k = 1..n: permutations of n with exactly k rising sequences (k - 1 descents)."""
    A = [1]
    for m in range(2, n + 1):
        B = [0] * m
        for k in range(m):
            left = A[k - 1] if 0 <= k - 1 < len(A) else 0
            here = A[k] if k < len(A) else 0
            B[k] = (k + 1) * here + (m - k) * left
        A = B
    return A


def riffle_tv(n: int, k: int) -> float:
    """Bayer & Diaconis (1992): after k GSR riffle shuffles, a permutation with r rising sequences has probability
    C(2^k + n - r, n) / 2^{kn}; the total variation distance from uniform, exactly (big integers)."""
    A = _eulerian(n)
    fact = math.factorial(n)
    denom = 2 ** (k * n)
    total = Fraction(0)
    for r, a in enumerate(A, start=1):
        num = math.comb(2 ** k + n - r, n) if 2 ** k + n - r >= n else 0
        total += a * abs(Fraction(num, denom) - Fraction(1, fact))
    return float(total / 2)


def polya_return(d: int, steps: int, reps: int, rng: np.random.Generator) -> float:
    """The share of simple random walks on Z^d that revisit the origin within ``steps`` steps."""
    hits = 0
    for _ in range(reps):
        axis = rng.integers(0, d, steps)
        sign = rng.choice((-1, 1), steps)
        pos = np.zeros((steps, d), int)
        pos[np.arange(steps), axis] = sign
        path = np.cumsum(pos, axis=0)
        hits += bool(np.any(np.all(path == 0, axis=1)))
    return hits / reps


# ---------------------------------------------------------------------------------------------------------------
# Martingales
# ---------------------------------------------------------------------------------------------------------------
def ruin(p: float, a: int, b: int) -> dict:
    """Gambler's ruin: start at a, step +1 w.p. p, -1 w.p. q, stop at 0 or b.  P(reach b) and the expected duration."""
    q = 1 - p
    if abs(p - q) < 1e-12:
        return {"win": a / b, "duration": float(a * (b - a))}
    s = q / p
    win = (1 - s ** a) / (1 - s ** b)
    dur = a / (q - p) - b / (q - p) * win
    return {"win": float(win), "duration": float(dur)}


def betting_paths(x, p0: float, p1: float) -> np.ndarray:
    """Wealth (likelihood ratio) paths L_n = prod (p1/p0)^{x} ((1-p1)/(1-p0))^{1-x} for 0/1 rows of ``x``: a
    nonnegative martingale with mean 1 under p0."""
    x = np.asarray(x, float)
    step = x * math.log(p1 / p0) + (1 - x) * math.log((1 - p1) / (1 - p0))
    return np.exp(np.cumsum(step, axis=-1))


def azuma(t: float, c) -> float:
    """Azuma-Hoeffding: P(|M_n - M_0| >= t) <= 2 exp(-t^2 / (2 sum c_k^2)) for differences bounded by c_k."""
    c = np.asarray(c, float)
    return float(min(1.0, 2 * math.exp(-t * t / (2 * np.sum(c * c)))))


def mcdiarmid(t: float, c) -> float:
    """McDiarmid: P(|f - E f| >= t) <= 2 exp(-2 t^2 / sum c_i^2) for f with bounded differences c_i."""
    c = np.asarray(c, float)
    return float(min(1.0, 2 * math.exp(-2 * t * t / np.sum(c * c))))


def polya_urn(steps: int, reps: int, rng: np.random.Generator, a: int = 1, b: int = 1) -> np.ndarray:
    """Polya's urn: start with a red and b blue; draw one, return it with another of its colour.  The red share is a
    martingale converging to a Beta(a, b) limit.  Returns the share paths (reps x steps)."""
    out = np.empty((reps, steps))
    for r in range(reps):
        red, tot = a, a + b
        for s in range(steps):
            if rng.random() < red / tot:
                red += 1
            tot += 1
            out[r, s] = red / tot
    return out


# ---------------------------------------------------------------------------------------------------------------
# Random walks and Brownian motion
# ---------------------------------------------------------------------------------------------------------------
def schauder(t, n: int, k: int) -> np.ndarray:
    """The Schauder tent for level n >= 1, k = 0..2^{n-1}-1: the integral of the Haar function, peak 2^{-(n+1)/2}."""
    t = np.asarray(t, float)
    a = k / 2 ** (n - 1)
    m = (k + 0.5) / 2 ** (n - 1)
    b = (k + 1) / 2 ** (n - 1)
    h = 2 ** ((n - 1) / 2)
    return np.where((t >= a) & (t <= m), h * (t - a), np.where((t > m) & (t <= b), h * (b - t), 0.0))


def levy_ciesielski(levels: int, t, rng: np.random.Generator, Z=None) -> list:
    """Brownian motion on [0, 1] as Z_0 t + sum_n sum_k Z_{n,k} S_{n,k}(t): the partial sums after each level."""
    t = np.asarray(t, float)
    if Z is None:
        Z = [rng.standard_normal(1)] + [rng.standard_normal(2 ** (n - 1)) for n in range(1, levels + 1)]
    B = Z[0][0] * t
    out = [B.copy()]
    for n in range(1, levels + 1):
        for k in range(2 ** (n - 1)):
            B = B + Z[n][k] * schauder(t, n, k)
        out.append(B.copy())
    return out


def quadratic_variation(path) -> dict:
    d = np.diff(np.asarray(path, float))
    return {"qv": float(np.sum(d * d)), "tv": float(np.sum(np.abs(d)))}


def dickey_fuller(n: int, reps: int, rng: np.random.Generator) -> dict:
    """Under a driftless random walk y_t = y_{t-1} + e_t (y_0 = 0), regress y_t on y_{t-1} with no constant:
    n (rho_hat - 1) and the t statistic, whose limits are functionals of Brownian motion."""
    e = rng.standard_normal((reps, n))
    y = np.cumsum(e, axis=1)
    ylag = np.concatenate([np.zeros((reps, 1)), y[:, :-1]], axis=1)
    sxx = np.sum(ylag ** 2, axis=1)
    sxy = np.sum(ylag * y, axis=1)
    rho = sxy / sxx
    resid = y - rho[:, None] * ylag
    s2 = np.sum(resid ** 2, axis=1) / (n - 1)
    t = (rho - 1) / np.sqrt(s2 / sxx)
    return {"n_rho": n * (rho - 1), "t": t}


def lil_envelope(n) -> np.ndarray:
    n = np.asarray(n, float)
    return np.sqrt(2 * n * np.log(np.log(np.maximum(n, 3.0))))


# ---------------------------------------------------------------------------------------------------------------
# MCMC output and the AR(1)
# ---------------------------------------------------------------------------------------------------------------
def batch_means_se(x, n_batches: int = 30) -> float:
    """The batch-means standard error of the mean of a stationary chain."""
    x = np.asarray(x, float)
    b = len(x) // n_batches
    m = x[: b * n_batches].reshape(n_batches, b).mean(1)
    return float(m.std(ddof=1) / math.sqrt(n_batches))


def ar1_ols(y) -> dict:
    """Least squares for y_t = phi y_{t-1} + e_t: phi_hat with its usual SE (justified by the martingale CLT)."""
    y = np.asarray(y, float)
    a, b = y[:-1], y[1:]
    phi = float(np.sum(a * b) / np.sum(a * a))
    r = b - phi * a
    s2 = float(np.sum(r * r) / (len(b) - 1))
    return {"phi": phi, "se": math.sqrt(s2 / np.sum(a * a))}


def rwm_normal(n: int, step: float, rng: np.random.Generator, x0: float = 0.0) -> np.ndarray:
    """Random-walk Metropolis for N(0, 1), vectorized proposals."""
    x = np.empty(n)
    cur = x0
    z = rng.standard_normal(n) * step
    u = np.log(rng.random(n))
    for i in range(n):
        prop = cur + z[i]
        if u[i] < 0.5 * (cur * cur - prop * prop):
            cur = prop
        x[i] = cur
    return x
