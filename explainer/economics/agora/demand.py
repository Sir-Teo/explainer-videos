"""Demand (Agora, Part 6): what a price change does to what people buy, and to how well off they are.

**Four functions, one consumer.**  A demand *system* holds the four functions of duality for one preference over any
number of goods: Marshallian demand ``x(p, m)``, the indirect utility ``v(p, m)``, the expenditure function
``e(p, u)`` and Hicksian (compensated) demand ``h(p, u)``.  :class:`CobbDouglas`, :class:`CES`, :class:`StoneGeary`
(the linear expenditure system, Stone 1954) and :class:`AIDS` (Deaton and Muellbauer 1980) have them in closed form;
:func:`duality_errors` checks the identities that tie them (e(p, v(p, m)) = m, Shephard's lemma h = de/dp, Roy's
identity x = -v_p / v_m) numerically, for any system.

**A price change, taken apart.**  :func:`slutsky_matrix` (S = D_p x + D_m x x', by central differences),
:func:`elasticities`, and :func:`decompose`, which splits the move from the old bundle to the new into a substitution
effect and an income effect, with Hicks's compensation (back to the old indifference curve) or Slutsky's (just enough
money to buy the old bundle).

**When demand slopes up.**  :class:`Diet`, a household that must eat ``need`` calories from a cheap staple and a
tastier, dearer food (the subsistence model behind Jensen and Miller 2008): three zones, and Giffen behaviour in the
middle one.  :func:`voucher_experiment` runs their design on simulated households (random price cuts, three survey
rounds, arc percent changes, county-by-round fixed effects) and :func:`local_elasticity` their kernel-weighted
regressions across the staple's share of calories.

**Welfare.**  :func:`cv`, :func:`ev`, :func:`cs`: compensating and equivalent variation and Marshall's surplus for a
change of prices; :func:`willig_gap`, Willig's (1976) approximation to the gap between them; :class:`LinearDemand`,
Hausman's (1981) exact surplus for a linear demand curve, found by integrating Roy's identity back to the expenditure
function, with the exact and approximate deadweight loss of a tax; :func:`virtual_price`, the price at which demand
for a good not yet sold would be zero (Hicks 1940; Hausman 1996).

**Price indices as welfare.**  :func:`coli` (Konüs 1924), :func:`laspeyres`, :func:`paasche`, and :func:`feenstra`,
the CES index's correction for goods that come and go.

**Engel curves and demand systems.**  :func:`working_leser` fits w = a + b log m; :func:`hamilton_drift` reads the
cost of living's mismeasurement from how the food Engel curve shifts (Hamilton 2001; Costa 2001);
:func:`aids_fit` estimates the AIDS by iterated least squares, unrestricted or with homogeneity and symmetry imposed,
with Wald tests of both.

**Integrability.**  :func:`loop_income` follows compensated income around a closed loop of prices: with a demand
system that comes from a preference it returns to where it started; when the Slutsky matrix is not symmetric it does
not, and by Green's theorem the gap is the asymmetry times the area of the loop (a money pump, as in Part 5).

Plain numpy and scipy.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# ---------------------------------------------------------------------------------------------------------------
# demand systems: the four functions


class System:
    """A demand system: Marshallian ``x(p, m)``, indirect utility ``v(p, m)``, expenditure ``e(p, u)``, Hicksian
    ``h(p, u)``.  Subclasses give closed forms; ``h`` defaults to Shephard's lemma by central differences."""

    n: int = 2

    def x(self, p, m):
        raise NotImplementedError

    def v(self, p, m):
        raise NotImplementedError

    def e(self, p, u):
        raise NotImplementedError

    def h(self, p, u):
        return grad(lambda q: self.e(q, u), p)

    def shares(self, p, m):
        p = np.asarray(p, float)
        return p * self.x(p, m) / m


def grad(f, p, rel=1e-6):
    """The gradient of a scalar function of prices, by central differences."""
    p = np.asarray(p, float)
    g = np.zeros_like(p)
    for i in range(len(p)):
        d = rel * max(abs(p[i]), 1e-8)
        up, dn = p.copy(), p.copy()
        up[i] += d
        dn[i] -= d
        g[i] = (f(up) - f(dn)) / (2 * d)
    return g


@dataclass
class CobbDouglas(System):
    """u = prod x_i^a_i with sum a_i = 1: each good gets the share a_i of income, whatever the prices."""

    a: tuple = (0.6, 0.4)

    def __post_init__(self):
        self.a_ = np.asarray(self.a, float) / np.sum(self.a)
        self.n = len(self.a_)

    def x(self, p, m):
        return self.a_ * m / np.asarray(p, float)

    def v(self, p, m):
        return m * np.prod((self.a_ / np.asarray(p, float)) ** self.a_)

    def e(self, p, u):
        return u * np.prod((np.asarray(p, float) / self.a_) ** self.a_)

    def h(self, p, u):
        return self.a_ * self.e(p, u) / np.asarray(p, float)


@dataclass
class CES(System):
    """u = (sum alpha_i x_i^r)^(1/r), r = (sigma - 1) / sigma: the elasticity of substitution is sigma for every pair.
    With two goods and alpha = (a, 1 - a) this is Part 5's ``Preference('ces', a, sigma=...)``."""

    alpha: tuple = (0.5, 0.5)
    sigma: float = 0.5

    def __post_init__(self):
        self.al = np.asarray(self.alpha, float)
        self.n = len(self.al)
        assert abs(self.sigma - 1) > 1e-9, "sigma = 1 is Cobb-Douglas"

    def index(self, p):
        """The CES price index: the cost of one unit of utility."""
        s = self.sigma
        return np.sum(self.al ** s * np.asarray(p, float) ** (1 - s)) ** (1 / (1 - s))

    def x(self, p, m):
        p = np.asarray(p, float)
        s = self.sigma
        return self.al ** s * p ** (-s) * m / np.sum(self.al ** s * p ** (1 - s))

    def v(self, p, m):
        return m / self.index(p)

    def e(self, p, u):
        return u * self.index(p)

    def h(self, p, u):
        p = np.asarray(p, float)
        return self.al ** self.sigma * (p / self.index(p)) ** (-self.sigma) * u


@dataclass
class StoneGeary(System):
    """The linear expenditure system (Stone 1954): u = prod (x_i - gamma_i)^beta_i.  The household first buys the
    committed quantities gamma, then splits what is left in the shares beta: Engel curves are straight lines that do
    not pass through the origin, so a good with a large committed quantity is a necessity."""

    beta: tuple = (0.3, 0.7)
    gamma: tuple = (2.0, 0.0)

    def __post_init__(self):
        self.b = np.asarray(self.beta, float) / np.sum(self.beta)
        self.g = np.asarray(self.gamma, float)
        self.n = len(self.b)

    def x(self, p, m):
        p = np.asarray(p, float)
        return self.g + self.b * (m - p @ self.g) / p

    def v(self, p, m):
        p = np.asarray(p, float)
        return (m - p @ self.g) * np.prod((self.b / p) ** self.b)

    def e(self, p, u):
        p = np.asarray(p, float)
        return p @ self.g + u * np.prod((p / self.b) ** self.b)

    def h(self, p, u):
        p = np.asarray(p, float)
        return self.g + self.b / p * u * np.prod((p / self.b) ** self.b)


@dataclass
class AIDS(System):
    """The Almost Ideal Demand System (Deaton and Muellbauer 1980).  log e(p, u) = log a(p) + u b(p), with
    log a(p) = alpha0 + sum alpha_k log p_k + 1/2 sum gamma_kj log p_k log p_j and b(p) = beta0 prod p_k^beta_k, so
    budget shares are w_i = alpha_i + sum_j gamma_ij log p_j + beta_i log(m / a(p)).  Adding up: sum alpha = 1,
    sum_i gamma_ij = 0, sum beta = 0; homogeneity: sum_j gamma_ij = 0; symmetry: gamma_ij = gamma_ji.  A ``gamma``
    that is not symmetric gives shares that no preference produces (see :func:`loop_income`); the expenditure
    function is then built from its symmetric part, and only ``x`` and ``shares`` use ``gamma`` as given."""

    alpha: tuple = (0.4, 0.35, 0.25)
    beta: tuple = (-0.1, 0.0, 0.1)
    gamma: tuple = ((-0.1, 0.05, 0.05), (0.05, -0.1, 0.05), (0.05, 0.05, -0.1))
    alpha0: float = 0.0
    beta0: float = 1.0

    def __post_init__(self):
        self.al = np.asarray(self.alpha, float)
        self.be = np.asarray(self.beta, float)
        self.ga = np.asarray(self.gamma, float)
        self.n = len(self.al)

    def log_a(self, p):
        lp = np.log(np.asarray(p, float))
        gs = (self.ga + self.ga.T) / 2
        return self.alpha0 + self.al @ lp + 0.5 * lp @ gs @ lp

    def b_(self, p):
        return self.beta0 * np.prod(np.asarray(p, float) ** self.be)

    def shares(self, p, m):
        lp = np.log(np.asarray(p, float))
        return self.al + self.ga @ lp + self.be * (np.log(m) - self.log_a(p))

    def x(self, p, m):
        return self.shares(p, m) * m / np.asarray(p, float)

    def v(self, p, m):
        return (np.log(m) - self.log_a(p)) / self.b_(p)

    def e(self, p, u):
        return float(np.exp(self.log_a(p) + u * self.b_(p)))

    def h(self, p, u):
        return self.x(p, self.e(p, u))

    def symmetric(self) -> bool:
        return bool(np.allclose(self.ga, self.ga.T))

    def elasticities(self, p, m):
        """Exact Marshallian price elasticities, expenditure elasticities and Hicksian price elasticities."""
        lp = np.log(np.asarray(p, float))
        w = self.shares(p, m)
        gs = (self.ga + self.ga.T) / 2
        dloga = self.al + gs @ lp           # d log a / d log p_j
        n = self.n
        E = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                E[i, j] = -(i == j) + (self.ga[i, j] - self.be[i] * dloga[j]) / w[i]
        eta = 1 + self.be / w
        H = E + np.outer(eta, w)
        return {"marshall": E, "income": eta, "hicks": H, "shares": w}


# ---------------------------------------------------------------------------------------------------------------
# identities, the Slutsky matrix, elasticities, decompositions


def duality_errors(sys: System, p, m) -> dict:
    """The largest error in each identity of duality at (p, m), relative to the size of the quantity checked."""
    p = np.asarray(p, float)
    u = sys.v(p, m)
    x = sys.x(p, m)
    h = sys.h(p, u)
    sh = grad(lambda q: sys.e(q, u), p)                       # Shephard: de/dp = h
    vp = grad(lambda q: sys.v(q, m), p)
    dm = 1e-6 * m
    vm = (sys.v(p, m + dm) - sys.v(p, m - dm)) / (2 * dm)
    roy = -vp / vm                                            # Roy: x = -v_p / v_m
    rel = lambda a, b: float(np.max(np.abs(a - b)) / max(np.max(np.abs(b)), 1e-12))  # noqa: E731
    return {"e(p, v(p, m)) = m": abs(sys.e(p, u) - m) / m,
            "v(p, e(p, u)) = u": abs(sys.v(p, sys.e(p, u)) - u) / max(abs(u), 1e-12),
            "h(p, v(p, m)) = x(p, m)": rel(h, x),
            "Shephard: de/dp = h": rel(sh, h),
            "Roy: -v_p / v_m = x": rel(roy, x)}


def slutsky_matrix(sys: System, p, m, rel=1e-6) -> np.ndarray:
    """S_ij = dx_i/dp_j + x_j dx_i/dm, by central differences.  For a system that comes from a preference, S is
    symmetric and negative semidefinite, and S p = 0."""
    p = np.asarray(p, float)
    n = len(p)
    x = sys.x(p, m)
    J = np.zeros((n, n))
    for j in range(n):
        d = rel * p[j]
        up, dn = p.copy(), p.copy()
        up[j] += d
        dn[j] -= d
        J[:, j] = (sys.x(up, m) - sys.x(dn, m)) / (2 * d)
    dm = rel * m
    xm = (sys.x(p, m + dm) - sys.x(p, m - dm)) / (2 * dm)
    return J + np.outer(xm, x)


def slutsky_report(S: np.ndarray, p) -> dict:
    """Symmetry, negative semidefiniteness and S p = 0, as numbers."""
    Ssym = (S + S.T) / 2
    ev = np.linalg.eigvalsh(Ssym)
    scale = max(np.max(np.abs(S)), 1e-12)
    return {"asymmetry": float(np.max(np.abs(S - S.T)) / scale), "eigenvalues": ev,
            "nsd": bool(ev.max() <= 1e-6 * scale), "Sp": float(np.max(np.abs(S @ np.asarray(p, float))) / scale)}


def elasticities(sys: System, p, m) -> dict:
    """Marshallian price elasticities, income elasticities, Hicksian price elasticities (by the Slutsky equation in
    elasticity form, eps^h_ij = eps_ij + w_j eta_i) and budget shares, by central differences."""
    p = np.asarray(p, float)
    n = len(p)
    x = sys.x(p, m)
    w = p * x / m
    E = np.zeros((n, n))
    for j in range(n):
        d = 1e-6 * p[j]
        up, dn = p.copy(), p.copy()
        up[j] += d
        dn[j] -= d
        E[:, j] = (sys.x(up, m) - sys.x(dn, m)) / (2 * d) * p[j] / x
    dm = 1e-6 * m
    eta = (sys.x(p, m + dm) - sys.x(p, m - dm)) / (2 * dm) * m / x
    return {"marshall": E, "income": eta, "hicks": E + np.outer(eta, w), "shares": w}


def decompose(sys: System, i: int, p0, p1, m, how: str = "hicks") -> dict:
    """Split the response to a change of prices p0 -> p1 into a substitution and an income effect.

    A is the old bundle, C the new; B is the bundle bought at the new prices with *compensated* income: Hicks's
    compensation gives just enough to reach the old utility (B = h(p1, u0)), Slutsky's just enough to buy the old
    bundle (B = x(p1, p1.A)).  Substitution is B - A, income C - B; ``i`` picks the good whose numbers are reported."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    A = sys.x(p0, m)
    C = sys.x(p1, m)
    if how == "hicks":
        u0 = sys.v(p0, m)
        m_comp = sys.e(p1, u0)
    elif how == "slutsky":
        m_comp = float(p1 @ A)
    else:
        raise ValueError(how)
    B = sys.x(p1, m_comp)
    return {"A": A, "B": B, "C": C, "m_comp": m_comp, "compensation": m_comp - m,
            "substitution": B[i] - A[i], "income": C[i] - B[i], "total": C[i] - A[i]}


# ---------------------------------------------------------------------------------------------------------------
# the subsistence diet: when demand slopes up


@dataclass
class Diet:
    """A household that must eat ``need`` calories a week from a staple (cheap calories, little taste) and a fancy
    food (taste, dear calories), after spending a share ``other_share`` of its budget on other foods (oil,
    vegetables) that bring ``other_kcal`` calories a dollar; otherwise it follows a Stone-Geary taste over the two,
    u = beta log(s - s0) + (1 - beta) log f, with a committed s0 of the staple.

    Three zones (Jensen and Miller 2008, conditions C1-C4):

    * *deprived*: income cannot buy ``need`` calories even as staple alone; all of it goes on the staple, whose
      demand then has elasticity -1;
    * *subsistence*: the calorie constraint binds, and the bundle is where the budget line meets the calorie line;
      a dearer staple forces the household to give up fancy food and replace its calories with more staple:
      the price elasticity of the staple is r / (1 - r) > 0, r the fancy food's calories per dollar relative to the
      staple's (Giffen behaviour);
    * *standard*: the taste optimum has calories to spare, and demand slopes down as usual.

    Goods are (staple, fancy); prices ``ps``, ``pf``; calories per unit ``cs``, ``cf``."""

    cs: float = 1400.0
    cf: float = 700.0
    need: float = 14000.0
    beta: float = 1 / 6
    s0: float = 3.0
    other_share: float = 0.0
    other_kcal: float = 0.0

    def taste(self, s, f):
        s, f = np.asarray(s, float), np.asarray(f, float)
        with np.errstate(divide="ignore", invalid="ignore"):
            return self.beta * np.log(np.maximum(s - self.s0, 1e-300)) + (1 - self.beta) * np.log(np.maximum(f, 1e-300))

    def other_calories(self, m):
        return self.other_share * m * self.other_kcal

    def calories(self, s, f, m=0.0):
        return self.cs * np.asarray(s, float) + self.cf * np.asarray(f, float) + self.other_calories(m)

    def choose(self, ps, pf, m) -> dict:
        """The bundle (staple, fancy) and the zone."""
        cs, cf = self.cs, self.cf
        K = self.need - self.other_calories(m)
        m = m * (1 - self.other_share)
        if m <= 0:
            return {"s": 0.0, "f": 0.0, "zone": "deprived"}
        if m * cs / ps <= K:
            return {"s": m / ps, "f": 0.0, "zone": "deprived"}
        # the taste optimum (Stone-Geary), at a corner when the committed staple is not affordable
        free = m - ps * self.s0
        if free > 0:
            s = self.s0 + self.beta * free / ps
            f = (1 - self.beta) * free / pf
        else:
            s, f = m / ps, 0.0
        if cs * s + cf * f >= K:
            return {"s": s, "f": f, "zone": "standard"}
        D = pf * cs - ps * cf
        s = (K * pf - m * cf) / D
        f = (m * cs - K * ps) / D
        return {"s": s, "f": f, "zone": "subsistence"}

    def staple(self, ps, pf, m) -> float:
        return self.choose(ps, pf, m)["s"]

    def calorie_share(self, ps, pf, m) -> float:
        b = self.choose(ps, pf, m)
        return self.cs * b["s"] / self.calories(b["s"], b["f"], m)

    def elasticity(self, ps, pf, m, rel=1e-5) -> float:
        d = rel * ps
        up, dn = self.staple(ps + d, pf, m), self.staple(ps - d, pf, m)
        return (up - dn) / (2 * d) * ps / self.staple(ps, pf, m)

    def giffen_elasticity(self, ps, pf) -> float:
        """The staple's price elasticity in the subsistence zone: r / (1 - r)."""
        r = (self.cf / pf) / (self.cs / ps)
        return r / (1 - r)

    def zone_bounds(self, ps, pf) -> tuple:
        """The incomes at which the household leaves the deprived zone and enters the standard one."""
        from scipy.optimize import brentq

        th, ko = self.other_share, self.other_kcal
        lo = self.need / ((1 - th) * self.cs / ps + th * ko)

        def gap(m):
            free = m * (1 - th) - ps * self.s0
            s = self.s0 + self.beta * free / ps
            f = (1 - self.beta) * free / pf
            return self.cs * s + self.cf * f + th * m * ko - self.need

        hi = brentq(gap, max(lo, ps * self.s0 / (1 - th)) + 1e-9, 1e6)
        return lo, hi

    def with_need(self, need: float) -> "Diet":
        return Diet(self.cs, self.cf, need, self.beta, self.s0, self.other_share, self.other_kcal)


def arc_pct(a, b):
    """The arc percent change from a to b: 100 (b - a) / ((a + b) / 2), as Jensen and Miller compute every change."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return 100 * (b - a) / ((a + b) / 2)        # nan where both are zero (no fish either time)


def voucher_experiment(diet: Diet, households: int, counties: int, cuts, ps: float, pf: float, median: float,
                       sigma: float, need_sd: float, report_sd: float, income_sd: float, seed: int) -> dict:
    """Jensen and Miller's design on simulated households.

    Each household has an income (lognormal: ``median``, ``sigma``) and a calorie need (``need_sd`` around the
    diet's); within each county it is assigned at random to a control group or a voucher worth one of ``cuts`` off
    the staple's price.  Three rounds: before the vouchers, while they are used, after.  Income moves a little
    between rounds (``income_sd``) and consumption is reported with error (``report_sd``, multiplicative).  The
    regression is theirs: the arc percent change in the staple on the arc percent change in its price, with
    county-by-round fixed effects, two changes per household; standard errors clustered by household."""
    rng = np.random.default_rng(seed)
    n = households
    county = np.arange(n) % counties
    arm = np.zeros(n, int)
    for c in range(counties):
        idx = np.flatnonzero(county == c)
        arm[rng.permutation(idx)] = np.arange(len(idx)) % (len(cuts) + 1)
    cut = np.array([0.0, *cuts])[arm]
    m0 = median * np.exp(sigma * rng.standard_normal(n))
    need = diet.need * np.exp(need_sd * rng.standard_normal(n))
    inc = m0[:, None] * np.exp(income_sd * rng.standard_normal((n, 3)))
    price = np.column_stack([np.full(n, ps), ps - cut, np.full(n, ps)])
    S = np.zeros((n, 3))
    F = np.zeros((n, 3))
    zone = []
    elas = np.zeros(n)
    for k in range(n):
        d = diet.with_need(need[k])
        for t in range(3):
            b = d.choose(price[k, t], pf, inc[k, t])
            S[k, t], F[k, t] = b["s"], b["f"]
        zone.append(d.choose(ps, pf, inc[k, 0])["zone"])
        elas[k] = d.elasticity(ps, pf, inc[k, 0])
    true_S = S.copy()
    S_rep = S * np.exp(report_sd * rng.standard_normal((n, 3)))
    F_rep = F * np.exp(report_sd * rng.standard_normal((n, 3)))
    share0 = diet.cs * S_rep[:, 0] / (diet.cs * S_rep[:, 0] + diet.cf * F_rep[:, 0] + diet.other_calories(inc[:, 0]))
    # two changes per household: rounds 1 -> 2 (price falls), 2 -> 3 (price returns)
    dS = np.concatenate([arc_pct(S_rep[:, 0], S_rep[:, 1]), arc_pct(S_rep[:, 1], S_rep[:, 2])])
    dF = np.concatenate([arc_pct(F_rep[:, 0], F_rep[:, 1]), arc_pct(F_rep[:, 1], F_rep[:, 2])])
    dP = np.concatenate([-100 * cut / ps, 100 * cut / ps])
    hh = np.concatenate([np.arange(n), np.arange(n)])
    cell = np.concatenate([county * 2, county * 2 + 1])
    return {"dS": dS, "dF": dF, "dP": dP, "hh": hh, "cell": cell, "share0": np.concatenate([share0, share0]),
            "share0_hh": share0, "arm": arm, "cut": cut, "income": m0, "need": need, "zone": np.array(zone),
            "elasticity": elas, "S": true_S, "F": F, "S_reported": S_rep, "F_reported": F_rep}


def fe_regression(y, x, cell, cluster, w=None) -> dict:
    """y on x with fixed effects for ``cell``; weights ``w``; standard error clustered by ``cluster``."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    w = np.ones_like(y) if w is None else np.asarray(w, float)
    keep = np.isfinite(y) & np.isfinite(x) & (w > 0)
    y, x, w, cell, cluster = y[keep], x[keep], w[keep], np.asarray(cell)[keep], np.asarray(cluster)[keep]
    yd, xd = y.copy(), x.copy()
    for c in np.unique(cell):
        k = cell == c
        sw = w[k].sum()
        yd[k] -= (w[k] * y[k]).sum() / sw
        xd[k] -= (w[k] * x[k]).sum() / sw
    sxx = (w * xd * xd).sum()
    b = (w * xd * yd).sum() / sxx
    r = yd - b * xd
    g = {}
    for c, s in zip(cluster, w * xd * r):
        g[c] = g.get(c, 0.0) + s
    se = np.sqrt(sum(v * v for v in g.values())) / sxx
    return {"b": float(b), "se": float(se), "n": int(len(y))}


def local_elasticity(exp: dict, grid, bandwidth: float = 0.10) -> dict:
    """Jensen and Miller's figure 2: at each initial staple calorie share on ``grid``, the fixed-effects regression
    restricted to households within ``bandwidth`` of it, weighted by a biweight kernel."""
    b, lo, hi = [], [], []
    for g in grid:
        z = (exp["share0"] - g) / bandwidth
        w = np.where(np.abs(z) < 1, (1 - z ** 2) ** 2, 0.0)
        r = fe_regression(exp["dS"], exp["dP"], exp["cell"], exp["hh"], w)
        b.append(r["b"])
        lo.append(r["b"] - 1.96 * r["se"])
        hi.append(r["b"] + 1.96 * r["se"])
    return {"grid": np.asarray(grid, float), "b": np.array(b), "lo": np.array(lo), "hi": np.array(hi)}


# ---------------------------------------------------------------------------------------------------------------
# welfare


def cv(sys: System, p0, p1, m) -> float:
    """Compensating variation: the money the household must be given *after* the change to be as well off as before,
    e(p1, u0) - m (positive for a loss)."""
    return float(sys.e(np.asarray(p1, float), sys.v(np.asarray(p0, float), m)) - m)


def ev(sys: System, p0, p1, m) -> float:
    """Equivalent variation: the money that, taken away *instead of* the change, hurts as much, m - e(p0, u1)
    (positive for a loss)."""
    return float(m - sys.e(np.asarray(p0, float), sys.v(np.asarray(p1, float), m)))


def cs(sys: System, i: int, p0, p1, m, steps: int = 4001) -> float:
    """Marshall's surplus lost when good i's price moves from p0[i] to p1[i] (others fixed): the area to the left of
    the ordinary demand curve between the two prices."""
    p0 = np.asarray(p0, float)
    a, b = p0[i], float(np.asarray(p1, float)[i])
    ps = np.linspace(a, b, steps)
    q = []
    for pi in ps:
        p = p0.copy()
        p[i] = pi
        q.append(sys.x(p, m)[i])
    return float(np.trapezoid(q, ps))


def willig_gap(eta: float, A: float, m: float) -> float:
    """Willig's (1976) approximation: (CV - A) / A is about eta A / (2 m), and (A - EV) / A the same, for a loss A
    of Marshall's surplus, income m and income elasticity eta."""
    return eta * A / (2 * m)


@dataclass
class LinearDemand:
    """x = alpha p + delta m + c (alpha < 0): a straight demand curve that shifts with income.  Hausman (1981):
    integrating Roy's identity gives the expenditure function e(p, k) = k exp(delta p) - (alpha p + alpha / delta +
    c) / delta, the constant k indexing utility, so exact welfare follows from the estimated curve."""

    alpha: float = -2.0
    delta: float = 0.01
    c: float = 10.0

    def x(self, p, m):
        return self.alpha * p + self.delta * m + self.c

    def k(self, p, m):
        a, d, c = self.alpha, self.delta, self.c
        return np.exp(-d * p) * (m + (a * p + a / d + c) / d)

    def e(self, p, k):
        a, d, c = self.alpha, self.delta, self.c
        return k * np.exp(d * p) - (a * p + a / d + c) / d

    def h(self, p, k):
        return self.x(p, self.e(p, k))

    def cv(self, p0, p1, m):
        return float(self.e(p1, self.k(p0, m)) - m)

    def ev(self, p0, p1, m):
        return float(m - self.e(p0, self.k(p1, m)))

    def cs(self, p0, p1, m):
        a, d, c = self.alpha, self.delta, self.c
        return float(a / 2 * (p1 ** 2 - p0 ** 2) + (d * m + c) * (p1 - p0))

    def tax(self, p0, t, m) -> dict:
        """A tax t per unit, fully passed on (p0 -> p0 + t).  Deadweight loss: exact, CV less the revenue the
        compensated household would pay, CV - t h(p1, u0); Marshall's, the loss of surplus less the revenue actually
        paid, CS - t x(p1, m)."""
        p1 = p0 + t
        k0 = self.k(p0, m)
        exact = self.cv(p0, p1, m) - t * self.h(p1, k0)
        approx = self.cs(p0, p1, m) - t * self.x(p1, m)
        return {"cv": self.cv(p0, p1, m), "ev": self.ev(p0, p1, m), "cs": self.cs(p0, p1, m),
                "revenue": float(t * self.x(p1, m)), "dwl_exact": float(exact), "dwl_marshall": float(approx),
                "dwl_error": float((approx - exact) / exact)}


def virtual_price(alpha: float, intercept: float) -> float:
    """The price at which a linear demand q = intercept + alpha p falls to zero (Hicks's virtual price for a good not
    yet on sale)."""
    return -intercept / alpha


# ---------------------------------------------------------------------------------------------------------------
# price indices as welfare


def coli(sys: System, p0, p1, u) -> float:
    """Konüs's true cost-of-living index: e(p1, u) / e(p0, u)."""
    return float(sys.e(np.asarray(p1, float), u) / sys.e(np.asarray(p0, float), u))


def laspeyres(p0, p1, x0) -> float:
    """The cost of the old basket at new prices over its cost at old prices: an upper bound to the COLI at u0."""
    return float(np.asarray(p1, float) @ x0 / (np.asarray(p0, float) @ x0))


def paasche(p0, p1, x1) -> float:
    """The cost of the new basket at new prices over its cost at old prices: a lower bound to the COLI at u1."""
    return float(np.asarray(p1, float) @ x1 / (np.asarray(p0, float) @ x1))


def feenstra(lambda0: float, lambda1: float, sigma: float) -> float:
    """The CES price index's variety correction (Feenstra 1994): multiply the index over continuing goods by
    (lambda1 / lambda0)^(1 / (sigma - 1)), lambda_t the share of period-t spending on goods sold in both periods.
    New goods (lambda1 < 1) lower the cost of living, more so the less substitutable they are."""
    return float((lambda1 / lambda0) ** (1 / (sigma - 1)))


# ---------------------------------------------------------------------------------------------------------------
# Engel curves


def working_leser(w, m) -> dict:
    """w = a + b log m by least squares; the income elasticity at share w is 1 + b / w (Working 1943, Leser 1963)."""
    w, lm = np.asarray(w, float), np.log(np.asarray(m, float))
    X = np.column_stack([np.ones_like(lm), lm])
    coef, *_ = np.linalg.lstsq(X, w, rcond=None)
    r = w - X @ coef
    s2 = r @ r / (len(w) - 2)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return {"a": float(coef[0]), "b": float(coef[1]), "se_b": float(se[1]),
            "eta_at": lambda share: 1 + coef[1] / share}


def hamilton_drift(w, m_measured, year, rel_food) -> dict:
    """Hamilton's (2001) method: food shares on log measured real income, the log relative price of food and a
    dummy for each year.  If the deflator overstates the rise in the cost of living, households with the same
    measured real income are richer in later years and spend a smaller share on food: the year dummies fall, and
    each one divided by b (both negative) is the cumulative bias in log points.  The relative price of food must vary
    within a year (across regions), or its effect cannot be told apart from the year dummies."""
    w = np.asarray(w, float)
    years = sorted(set(np.asarray(year).tolist()))
    D = np.column_stack([(np.asarray(year) == y).astype(float) for y in years[1:]])
    X = np.column_stack([np.ones_like(w), np.log(m_measured), np.asarray(rel_food, float), D])
    coef, *_ = np.linalg.lstsq(X, w, rcond=None)
    b = coef[1]
    d = coef[3:]
    bias = d / b
    return {"a": float(coef[0]), "b": float(b), "g": float(coef[2]), "years": years, "dummies": np.r_[0.0, d],
            "cumulative_bias": np.r_[0.0, bias]}


# ---------------------------------------------------------------------------------------------------------------
# AIDS estimation


def aids_fit(W, logP, logm, restrict: str = "none", alpha0: float = 0.0, iters: int = 50) -> dict:
    """Estimate the AIDS by iterated least squares (Blundell and Robin 1999): given current parameters, log a(p) is
    known and the share equations are linear; re-estimate and repeat.  The first n - 1 equations are estimated (the
    last follows from adding up) as one stacked system by generalized least squares with the residual covariance;
    ``restrict``: 'none', 'homogeneity' (sum_j gamma_ij = 0) or 'symmetry' (homogeneity and gamma_ij = gamma_ji).
    Returns the parameters of all n equations and Wald statistics for the restrictions (from the unrestricted fit)."""
    W, logP, logm = np.asarray(W, float), np.asarray(logP, float), np.asarray(logm, float)
    N, n = W.shape
    k = n + 2   # regressors per equation: 1, log p_1..log p_n, log(m / a)
    gam = np.zeros((n, n))
    al = W.mean(axis=0)
    be = np.zeros(n)

    def loga(al, gam):
        gs = (gam + gam.T) / 2
        return alpha0 + logP @ al + 0.5 * np.einsum("ti,ij,tj->t", logP, gs, logP)

    def constraints(kind):
        R, r = [], []
        if kind in ("homogeneity", "symmetry"):
            for i in range(n - 1):
                row = np.zeros((n - 1) * k)
                row[i * k + 1: i * k + 1 + n] = 1.0
                R.append(row)
                r.append(0.0)
        if kind == "symmetry":
            for i in range(n - 1):
                for j in range(i + 1, n - 1):
                    row = np.zeros((n - 1) * k)
                    row[i * k + 1 + j] = 1.0
                    row[j * k + 1 + i] = -1.0
                    R.append(row)
                    r.append(0.0)
        return (np.array(R), np.array(r)) if R else (None, None)

    def gls(Z, Y, Sinv, R=None, r=None):
        # stacked system with the same regressors in every equation: (Sinv kron Z'Z) beta = (Sinv kron Z') y
        ZZ = Z.T @ Z
        A = np.kron(Sinv, ZZ)
        c = (Z.T @ Y @ Sinv).T.reshape(-1)    # equation-major
        Ainv = np.linalg.inv(A)
        bu = Ainv @ c
        if R is None:
            return bu, Ainv
        M = R @ Ainv @ R.T
        br = bu - Ainv @ R.T @ np.linalg.solve(M, R @ bu - r)
        return br, Ainv

    Y = W[:, : n - 1]
    for _ in range(iters):
        la = loga(al, gam)
        Z = np.column_stack([np.ones(N), logP, logm - la])
        B0 = np.linalg.lstsq(Z, Y, rcond=None)[0]
        res = Y - Z @ B0
        Sig = res.T @ res / N
        Sinv = np.linalg.inv(Sig)
        R, r = constraints(restrict)
        bvec, Ainv = gls(Z, Y, Sinv, R, r)
        Bm = bvec.reshape(n - 1, k)
        al_new = np.r_[Bm[:, 0], 1 - Bm[:, 0].sum()]
        gam_new = np.zeros((n, n))
        gam_new[: n - 1] = Bm[:, 1: 1 + n]
        gam_new[n - 1] = -gam_new[: n - 1].sum(axis=0)
        be_new = np.r_[Bm[:, -1], -Bm[:, -1].sum()]
        done = np.max(np.abs(gam_new - gam)) < 1e-10 and np.max(np.abs(be_new - be)) < 1e-10
        al, gam, be = al_new, gam_new, be_new
        if done:
            break
    # Wald tests from the unrestricted system at the final a(p)
    la = loga(al, gam)
    Z = np.column_stack([np.ones(N), logP, logm - la])
    B0 = np.linalg.lstsq(Z, Y, rcond=None)[0]
    res = Y - Z @ B0
    Sig = res.T @ res / N
    bu, Ainv = gls(Z, Y, np.linalg.inv(Sig))
    tests = {}
    for kind in ("homogeneity", "symmetry"):
        R, r = constraints(kind)
        d = R @ bu - r
        stat = float(d @ np.linalg.solve(R @ Ainv @ R.T, d))
        from scipy.stats import chi2

        tests[kind] = {"wald": stat, "df": int(len(r)), "p": float(chi2.sf(stat, len(r)))}
    est = AIDS(alpha=tuple(al), beta=tuple(be), gamma=tuple(map(tuple, gam)), alpha0=alpha0)
    return {"model": est, "alpha": al, "beta": be, "gamma": gam, "tests": tests, "restrict": restrict}


# ---------------------------------------------------------------------------------------------------------------
# integrability: going round a loop of prices


def loop_income(share_fn, path_logp: np.ndarray) -> np.ndarray:
    """Compensated log income along a path of log prices: d log m = sum_i w_i(p, m) d log p_i, integrated by the
    midpoint rule.  ``share_fn(p, m)`` gives budget shares.  For a system that comes from a preference this is
    log e(p, u0) and returns to its start when the path closes; otherwise the end differs from the start."""
    L = np.asarray(path_logp, float)
    out = np.zeros(len(L))
    lm = 0.0
    for t in range(1, len(L)):
        mid = (L[t] + L[t - 1]) / 2
        w = share_fn(np.exp(mid), np.exp(lm))
        lm_half = lm + 0.5 * w @ (L[t] - L[t - 1])
        w = share_fn(np.exp(mid), np.exp(lm_half))
        lm = lm + w @ (L[t] - L[t - 1])
        out[t] = lm
    return out


def circle_path(center, radius, steps: int = 721, n: int = 3) -> np.ndarray:
    """A circle in the (log p_1, log p_2) plane, counter-clockwise, the other prices fixed at 1."""
    t = np.linspace(0, 2 * np.pi, steps)
    L = np.zeros((steps, n))
    L[:, 0] = center[0] + radius * np.cos(t)
    L[:, 1] = center[1] + radius * np.sin(t)
    return L


# ---------------------------------------------------------------------------------------------------------------
# the Island's household survey


@dataclass
class Survey:
    """A simulated household survey for demand-system estimation: ``villages`` x ``months`` price cells, ``per_cell``
    households each, total spending lognormal, shares from a planted AIDS plus noise."""

    truth: AIDS
    villages: int = 20
    months: int = 12
    per_cell: int = 25
    price_sd: float = 0.15
    m_median: float = 300.0
    m_sigma: float = 0.5
    share_sd: float = 0.03
    seed: int = 0
    data: dict = field(default_factory=dict)

    def draw(self) -> dict:
        rng = np.random.default_rng(self.seed)
        n = self.truth.n
        cells = self.villages * self.months
        village_level = rng.normal(0, self.price_sd, (self.villages, n))
        month_level = rng.normal(0, self.price_sd, (self.months, n))
        logP, logm, W, cell = [], [], [], []
        for v in range(self.villages):
            for t in range(self.months):
                lp = village_level[v] + month_level[t] + rng.normal(0, self.price_sd / 2, n)
                for _ in range(self.per_cell):
                    lm = np.log(self.m_median) + self.m_sigma * rng.standard_normal()
                    w = self.truth.shares(np.exp(lp), np.exp(lm))
                    e = rng.normal(0, self.share_sd, n)
                    e -= e.mean()                              # noise that keeps the shares adding to one
                    logP.append(lp)
                    logm.append(lm)
                    W.append(w + e)
                    cell.append(v * self.months + t)
        self.data = {"logP": np.array(logP), "logm": np.array(logm), "W": np.array(W), "cell": np.array(cell),
                     "cells": cells}
        return self.data
