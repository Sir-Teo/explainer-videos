"""The consumer (Agora, Part 5): what someone wants, and what their choices reveal about it.

Two halves, which Afriat's theorem joins.

**Preferences and demand.**  :class:`Preference` holds one of the standard two-good forms (Cobb-Douglas, CES,
perfect substitutes, perfect complements, quasilinear) with its utility, marginal rate of substitution, indifference
curves and the bundle it buys on a straight budget line (corners included).  :func:`best_on_frontier` finds the best
point on any budget frontier, kinked or not, by search, for the quantity-discount and tax-schedule budgets of
chapter 6.  :func:`lexicographic_rank` is the ordering no utility number can represent.

**Revealed preference.**  From observed prices ``P`` (n x k) and chosen bundles ``X`` (n x k), with any number of goods:

* :func:`direct` and :func:`closure`: x_i is directly revealed preferred to x_j when x_j was affordable when x_i was
  chosen (p_i.x_i >= p_i.x_j); the transitive closure (Warshall's algorithm) gives the revealed preference R;
* :func:`warp_violations`, :func:`sarp_violations`, :func:`garp_violations`: Samuelson's weak axiom (1938),
  Houthakker's strong axiom (1950) and the generalized axiom (Afriat 1967, named by Varian 1982);
* :func:`ccei`: Afriat's critical cost efficiency index (1972), the largest e such that the data satisfy GARP when
  every budget is shrunk to a share e of itself; 1 - e is the share of income "left on the table";
* :func:`houtman_maks`: the largest subset of choices that satisfies GARP (by search, for small n);
* :func:`afriat`: Afriat's inequalities U_j <= U_i + lambda_i p_i.(x_j - x_i) solved as a linear programme; when
  they have a solution the data are rationalized by the concave, increasing, piecewise-linear utility
  u(x) = min_i U_i + lambda_i p_i.(x - x_i) (:func:`afriat_utility`);
* :func:`revealed_worse` and :func:`revealed_better` (two goods): Varian's (1982) bounds on the indifference curve
  through an observed bundle, from the data alone;
* :func:`bronars`: the power of the test, the chance that a consumer choosing at random on the same budgets
  violates GARP (Bronars 1987);
* :func:`becker_demand`: Becker's (1962) consumers who choose at random on their budget line, and whose market demand
  still slopes down.

Plain numpy and scipy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

import numpy as np

# ---------------------------------------------------------------------------------------------------------------
# preferences and demand (two goods, x and y)


@dataclass
class Preference:
    """A two-good preference.  ``kind``: 'cobb-douglas' (share a on x), 'ces' (weight a on x, elasticity of
    substitution sigma), 'substitutes' (u = a x + b y), 'complements' (u = min(x / a, y / b)), 'quasilinear'
    (u = a log x + y)."""

    kind: str
    a: float = 0.5
    b: float = 1.0
    sigma: float = 1.0
    meta: dict = field(default_factory=dict)

    def u(self, x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        k, a, b = self.kind, self.a, self.b
        if k == "cobb-douglas" or (k == "ces" and abs(self.sigma - 1) < 1e-12):
            return np.power(np.maximum(x, 0), a) * np.power(np.maximum(y, 0), 1 - a)
        if k == "ces":
            r = (self.sigma - 1) / self.sigma
            with np.errstate(divide="ignore", invalid="ignore"):
                return np.power(a * np.power(np.maximum(x, 1e-300), r) + (1 - a) * np.power(np.maximum(y, 1e-300), r),
                                1 / r)
        if k == "substitutes":
            return a * x + b * y
        if k == "complements":
            return np.minimum(x / a, y / b)
        if k == "quasilinear":
            with np.errstate(divide="ignore"):
                return a * np.log(np.maximum(x, 1e-300)) + y
        raise ValueError(k)

    def mrs(self, x, y):
        """The marginal rate of substitution, MU_x / MU_y: how many y the consumer would give for one more x."""
        x, y = float(x), float(y)
        k, a, b = self.kind, self.a, self.b
        if k == "cobb-douglas" or (k == "ces" and abs(self.sigma - 1) < 1e-12):
            return a / (1 - a) * y / x
        if k == "ces":
            return a / (1 - a) * (y / x) ** (1 / self.sigma)
        if k == "substitutes":
            return a / b
        if k == "complements":
            return np.inf if y / b > x / a else (0.0 if y / b < x / a else np.nan)
        if k == "quasilinear":
            return a / x
        raise ValueError(k)

    def demand(self, px: float, py: float, m: float) -> tuple[float, float]:
        """The bundle bought with income m at prices px, py (corners included; ties in 'substitutes' split)."""
        k, a, b = self.kind, self.a, self.b
        if k == "cobb-douglas" or (k == "ces" and abs(self.sigma - 1) < 1e-12):
            return a * m / px, (1 - a) * m / py
        if k == "ces":
            s = self.sigma
            wx, wy = a ** s * px ** (1 - s), (1 - a) ** s * py ** (1 - s)
            return m * wx / (wx + wy) / px, m * wy / (wx + wy) / py
        if k == "substitutes":
            bx, by = a / px, b / py
            if abs(bx - by) < 1e-12:
                return m / (2 * px), m / (2 * py)
            return (m / px, 0.0) if bx > by else (0.0, m / py)
        if k == "complements":
            t = m / (a * px + b * py)
            return a * t, b * t
        if k == "quasilinear":
            x = a * py / px
            if px * x >= m:
                return m / px, 0.0
            return x, (m - px * x) / py
        raise ValueError(k)

    def indifference(self, level: float, xs) -> np.ndarray:
        """y on the indifference curve u(x, y) = level, for each x in xs (nan where there is none)."""
        xs = np.asarray(xs, float)
        k, a, b = self.kind, self.a, self.b
        with np.errstate(divide="ignore", invalid="ignore"):
            if k == "cobb-douglas" or (k == "ces" and abs(self.sigma - 1) < 1e-12):
                return np.power(level / np.power(xs, a), 1 / (1 - a))
            if k == "ces":
                r = (self.sigma - 1) / self.sigma
                inner = (level ** r - a * np.power(xs, r)) / (1 - a)
                out = np.power(inner, 1 / r)
                return np.where(inner > 0, out, np.nan)
            if k == "substitutes":
                return np.where(level - a * xs >= 0, (level - a * xs) / b, np.nan)
            if k == "complements":
                return np.where(xs >= a * level, b * level, np.nan)
            if k == "quasilinear":
                return level - a * np.log(xs)
        raise ValueError(k)


def best_on_frontier(pref: Preference, xs, ys) -> dict:
    """The best point of a budget frontier given as points (xs[i], ys[i]) (kinked, non-convex, anything): utility is
    evaluated at every point and the largest kept.  Pass a fine grid."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    u = pref.u(xs, ys)
    i = int(np.nanargmax(u))
    return {"x": float(xs[i]), "y": float(ys[i]), "u": float(u[i]), "i": i}


def lexicographic_rank(bundles) -> list[int]:
    """Order two-good bundles lexicographically (more x is better; y breaks ties).  A complete, transitive ordering
    that no real-valued utility function represents (Debreu): returns the indices from worst to best."""
    b = [tuple(map(float, z)) for z in bundles]
    return sorted(range(len(b)), key=lambda i: (b[i][0], b[i][1]))


# ---------------------------------------------------------------------------------------------------------------
# revealed preference (any number of goods)


def _arrays(P, X):
    P, X = np.asarray(P, float), np.asarray(X, float)
    if P.shape != X.shape or P.ndim != 2:
        raise ValueError("P and X must both be n x k")
    return P, X


def direct(P, X, e: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """``(R0, P0)``: R0[i, j] when e p_i.x_i >= p_i.x_j (x_i directly revealed preferred to x_j at efficiency e),
    P0[i, j] when the inequality is strict."""
    P, X = _arrays(P, X)
    C = P @ X.T                      # C[i, j] = p_i . x_j
    own = e * np.diag(C)[:, None]
    tol = 1e-9 * np.maximum(1.0, np.abs(C))
    return own >= C - tol, own > C + tol


def closure(R0: np.ndarray) -> np.ndarray:
    """The transitive closure of a relation (Warshall's algorithm, vectorized)."""
    R = np.array(R0, bool, copy=True)
    for k in range(len(R)):
        R |= np.outer(R[:, k], R[k, :])
    return R


def garp_violations(P, X, e: float = 1.0) -> list[tuple[int, int]]:
    """Pairs (i, j) with x_i revealed preferred to x_j although x_j is strictly directly revealed preferred to x_i:
    GARP says there are none."""
    R0, P0 = direct(P, X, e)
    R = closure(R0)
    bad = R & P0.T
    np.fill_diagonal(bad, False)
    return [tuple(map(int, ij)) for ij in np.argwhere(bad)]


def warp_violations(P, X) -> list[tuple[int, int]]:
    """Pairs i < j of distinct bundles each directly revealed preferred to the other (Samuelson 1938)."""
    P, X = _arrays(P, X)
    R0, _ = direct(P, X)
    out = []
    for i, j in combinations(range(len(X)), 2):
        if R0[i, j] and R0[j, i] and not np.allclose(X[i], X[j]):
            out.append((i, j))
    return out


def sarp_violations(P, X) -> list[tuple[int, int]]:
    """Pairs of distinct bundles each revealed preferred to the other through a chain (Houthakker 1950)."""
    P, X = _arrays(P, X)
    R0, _ = direct(P, X)
    R = closure(R0)
    out = []
    for i, j in combinations(range(len(X)), 2):
        if R[i, j] and R[j, i] and not np.allclose(X[i], X[j]):
            out.append((i, j))
    return out


def ccei(P, X, tol: float = 1e-10) -> float:
    """Afriat's critical cost efficiency index: the largest e in [0, 1] at which the data satisfy GARP.  The
    candidates are the ratios p_i.x_j / p_i.x_i, so a bisection over them is exact."""
    P, X = _arrays(P, X)
    if not garp_violations(P, X, 1.0):
        return 1.0
    C = P @ X.T
    r = (C / np.diag(C)[:, None]).ravel()
    cand = np.unique(np.concatenate([[0.0], r[(r > 0) & (r < 1)], [1.0]]))
    # the relations change only at these ratios; find the last one just below which the data still pass
    lo, hi = 0, len(cand) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if garp_violations(P, X, cand[mid] - tol):
            hi = mid - 1
        else:
            lo = mid
    if lo == len(cand) - 1:
        return 1.0
    # between two consecutive ratios nothing changes: the supremum is the upper one if the gap passes, else the lower
    gap = 0.5 * (cand[lo] + cand[lo + 1])
    return float(cand[lo + 1]) if not garp_violations(P, X, gap) else float(cand[lo])


def houtman_maks(P, X) -> list[int]:
    """The largest subset of observations that satisfies GARP, by search from the largest size down (fine for the
    dozen or so choices of a classroom experiment)."""
    P, X = _arrays(P, X)
    n = len(X)
    for size in range(n, 0, -1):
        for keep in combinations(range(n), size):
            k = list(keep)
            if not garp_violations(P[k], X[k]):
                return k
    return []


def afriat(P, X) -> dict | None:
    """Afriat's inequalities as a linear programme: find U_i and lambda_i >= 1 with
    U_j <= U_i + lambda_i p_i.(x_j - x_i) for all i, j.  Returns ``{"U", "lam"}``, or None when there is no solution
    (which, by Afriat's theorem, happens exactly when GARP fails)."""
    from scipy.optimize import linprog

    P, X = _arrays(P, X)
    n = len(X)
    A, b = [], []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            row = np.zeros(2 * n)
            row[j] += 1.0                     # U_j
            row[i] -= 1.0                     # - U_i
            row[n + i] = -float(P[i] @ (X[j] - X[i]))   # - lambda_i p_i.(x_j - x_i)
            A.append(row)
            b.append(0.0)
    bounds = [(None, None)] * n + [(1.0, None)] * n
    c = np.concatenate([np.zeros(n), np.ones(n)])     # the smallest multipliers that work
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    if not res.success:
        return None
    U, lam = res.x[:n], res.x[n:]
    return {"U": U - U.min(), "lam": lam}


def afriat_utility(P, X, sol: dict):
    """The utility function Afriat's solution builds: u(x) = min_i U_i + lambda_i p_i.(x - x_i), for an array of
    bundles (m x k).  Concave, increasing, and maximized on each observed budget at the observed choice."""
    P, X = _arrays(P, X)
    U, lam = np.asarray(sol["U"]), np.asarray(sol["lam"])

    def u(Z):
        Z = np.atleast_2d(np.asarray(Z, float))
        vals = U[None, :] + lam[None, :] * (Z @ P.T - np.sum(P * X, axis=1)[None, :])
        return vals.min(axis=1)

    return u


def revealed_worse(P, X, k: int) -> list[int]:
    """The observations i whose whole budget set {x: p_i.x <= p_i.x_i} is revealed worse than x_k (x_k R x_i, k
    included): their union bounds the indifference curve through x_k from below."""
    R0, _ = direct(P, X)
    R = closure(R0)
    return [int(i) for i in range(len(R)) if R[k, i] or i == k]


def revealed_better(P, X, k: int) -> np.ndarray:
    """Two goods: the corners of the monotone convex hull of the bundles revealed preferred to x_k (x_i R x_k, k
    included) -- with convex, monotone preferences, every bundle in it is at least as good as x_k (Varian 1982).
    Returned as the hull's lower-left boundary, from the top-left to the bottom-right."""
    P, X = _arrays(P, X)
    R0, _ = direct(P, X)
    R = closure(R0)
    pts = np.array([X[i] for i in range(len(X)) if R[i, k] or i == k], float)
    pts = pts[np.lexsort((pts[:, 1], pts[:, 0]))]
    hull: list[np.ndarray] = []
    for p in pts:                                   # lower convex chain, then keep only its decreasing part
        while len(hull) >= 2:
            o, a = hull[-2], hull[-1]
            if (a[0] - o[0]) * (p[1] - o[1]) - (a[1] - o[1]) * (p[0] - o[0]) <= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    out = [hull[0]]
    for p in hull[1:]:
        if p[1] < out[-1][1]:
            out.append(p)
    return np.array(out)


def random_on_budgets(P, m, rng, n: int | None = None) -> np.ndarray:
    """One random consumer: on each budget (prices P[i], income m[i]) spend a share drawn uniformly from the simplex
    (two goods: a point uniform on the budget line)."""
    P = np.asarray(P, float)
    m = np.asarray(m, float)
    sh = rng.dirichlet(np.ones(P.shape[1]), len(P))
    return sh * m[:, None] / P


def bronars(P, m, reps: int = 2000, seed: int = 1987) -> dict:
    """Bronars's (1987) power: how often a consumer choosing at random on the same budgets violates GARP, with the
    distribution of their CCEIs.  A test passed by people but also by random choosers says nothing."""
    rng = np.random.default_rng(seed)
    P = np.asarray(P, float)
    viol, scores = 0, []
    for _ in range(reps):
        Xr = random_on_budgets(P, m, rng)
        bad = bool(garp_violations(P, Xr))
        viol += bad
        scores.append(ccei(P, Xr) if bad else 1.0)
    scores = np.array(scores)
    return {"power": viol / reps, "ccei_mean": float(scores.mean()), "ccei": scores,
            "share_above_95": float(np.mean(scores > 0.95)), "share_above_90": float(np.mean(scores > 0.90))}


def becker_demand(prices, m: float, people: int, seed: int = 1962) -> dict:
    """Becker's (1962) "irrational" households: each spends a uniformly random share of income m on x, whatever the
    price.  Mean demand for x at each price is (1/2) m / p: it slopes down although nobody maximizes anything."""
    rng = np.random.default_rng(seed)
    prices = np.asarray(prices, float)
    shares = rng.random(people)
    q = shares[None, :] * m / prices[:, None]
    return {"prices": prices, "mean": q.mean(axis=1), "each": q, "theory": 0.5 * m / prices}


# ---------------------------------------------------------------------------------------------------------------
# kinked budgets: a tax credit and the earnings people choose


def eitc(z, phase_in_end: float = 8580.0, rate_in: float = 0.34, plateau_end: float = 15740.0,
         rate_out: float = 0.16):
    """The earned income tax credit's schedule (defaults: one child, 2008 dollars, Saez 2010, table 1): the credit
    rises at ``rate_in`` per dollar earned, stays at its maximum on the plateau, then is withdrawn at ``rate_out``."""
    z = np.asarray(z, float)
    top = rate_in * phase_in_end
    c = np.where(z <= phase_in_end, rate_in * z, top - rate_out * np.maximum(z - plateau_end, 0.0))
    return np.maximum(c, 0.0)


def earnings_choice(potential, elasticity: float, credit=eitc, grid=None) -> np.ndarray:
    """Each person, with potential earnings n, chooses earnings z to maximize z + credit(z) - effort, with the
    isoelastic effort cost n/(1 + 1/e) (z/n)^(1 + 1/e): without a credit they earn exactly n, and a marginal net
    reward r moves them to n r^e.  Elasticity 0: everyone earns n.  Solved on a grid, so kinks are exact."""
    n = np.asarray(potential, float)
    if elasticity <= 0:
        return n.copy()
    grid = np.arange(0.0, 80000.0, 10.0) if grid is None else np.asarray(grid, float)
    k = 1.0 + 1.0 / elasticity
    cred = credit(grid)
    out = np.empty_like(n)
    for lo in range(0, len(n), 500):
        nn = n[lo:lo + 500, None]
        val = grid[None, :] + cred[None, :] - nn / k * np.power(grid[None, :] / nn, k)
        out[lo:lo + 500] = grid[np.argmax(val, axis=1)]
    return out


# ---------------------------------------------------------------------------------------------------------------
# random utility: a binary logit, the workhorse of discrete-choice demand (McFadden)


def logit_fit(X, y, iters: int = 50) -> dict:
    """Maximum likelihood for P(y = 1) = 1 / (1 + exp(-X b)) by Newton's method; returns the coefficients, their
    standard errors (inverse information) and the log likelihood."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (y - p)
        H = (X * (p * (1 - p))[:, None]).T @ X
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-12:
            break
    p = 1 / (1 + np.exp(-X @ b))
    H = (X * (p * (1 - p))[:, None]).T @ X
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    ll = float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return {"b": b, "se": se, "loglik": ll}

