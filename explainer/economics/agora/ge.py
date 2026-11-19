"""General equilibrium (Agora, Part 9): a whole economy of traders, and the prices that clear every market at once.

**Traders.**  :class:`Trader` holds an endowment and Cobb-Douglas, CES or Leontief preferences, with its demand at any
prices in closed form; :func:`excess` sums an economy's excess demand (Walras's law holds identically).

**The Edgeworth box** (two traders, two goods, Cobb-Douglas).  :func:`cd_indifference`, :func:`contract_curve`,
:func:`lens_ends` (where the contract curve leaves the lens of mutual gains), :func:`box_equilibrium` (the competitive
price and allocation in closed form), :func:`offer_curve`, and the core of the replicated economy:
:func:`blocks` (can a coalition of ``s`` copies of one trader and ``t`` of the other improve on an allocation?) and
:func:`core_interval` (the part of the contract curve no coalition of up to ``r`` of each type blocks; Edgeworth's
conjecture and Debreu and Scarf's theorem say it shrinks to the competitive allocation).

**Existence and computation.**  :func:`sperner_labels` and :func:`sperner_walk` (three goods: the price simplex cut
into small triangles, each corner labelled by a good in excess supply, and Scarf's door-to-door walk to a triangle
with all three labels, an approximate equilibrium); :func:`tatonnement` (Walras's auctioneer, dp/dt = z(p));
:func:`newton` (Newton's method on excess demand with a numeraire); :func:`scarf_excess` and :func:`scarf_path`
(Scarf's 1960 economy, where the auctioneer's prices circle the equilibrium for ever).

**Production.**  :func:`crusoe` (one person as consumer, worker and firm: the planner's choice and the market's, with
the wage that decentralizes it).

**Anything goes.**  :func:`quasilinear_three` (two traders whose excess demand crosses zero three times) and
:func:`equilibria_2good` (every equilibrium of a two-good economy, by sign changes).

**Time and uncertainty.**  :func:`arrow_debreu` (traders, today and two states tomorrow: complete markets in Arrow
securities) and :func:`bond_only` (the same economy with only a riskless bond: consumption moves across time, but
risk is not shared), with :func:`certain_equivalent` to compare them.

**Planning.**  :func:`kantorovich` (the most complete sets a set of machines can make, by linear programming, with the
dual prices, Kantorovich's "resolving multipliers", that decentralize the plan).

**Misallocation.**  :func:`misallocation` (plants with different productivities and distortions: output against the
allocation that equalizes marginal products, and Hsieh and Klenow's lognormal formula).

**Indivisibilities.**  :func:`top_trading_cycles` (Shapley and Scarf's housing market, solved by Gale's top trading
cycles).

Plain numpy and scipy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, linprog, minimize_scalar


# ---------------------------------------------------------------------------------------------------------------
# traders


@dataclass(frozen=True)
class Trader:
    """A trader with endowment ``e`` and preferences over the goods.

    ``kind`` is ``"cd"`` (u = sum a_i log x_i, the a_i summing to one), ``"ces"`` (u = (sum a_i x_i^rho)^(1/rho),
    elasticity of substitution 1 / (1 - rho)) or ``"leontief"`` (u = min_i x_i / a_i over the goods with a_i > 0).
    """

    a: tuple
    e: tuple
    kind: str = "cd"
    rho: float = 0.0
    name: str = ""

    def __post_init__(self):
        assert self.kind in ("cd", "ces", "leontief"), self.kind
        assert len(self.a) == len(self.e)

    @property
    def n(self) -> int:
        return len(self.e)

    def wealth(self, p) -> float:
        return float(np.dot(p, self.e))

    def demand(self, p) -> np.ndarray:
        """Demand at prices ``p`` (a zero price for a desired good gives an infinite demand for it)."""
        p = np.asarray(p, float)
        a = np.asarray(self.a, float)
        m = float(np.dot(p, self.e))
        with np.errstate(divide="ignore", invalid="ignore"):
            if self.kind == "cd":
                x = np.where(a > 0, a * m / p, 0.0)
            elif self.kind == "ces":
                s = 1.0 / (1.0 - self.rho)
                w = np.where(a > 0, a ** s * p ** (1 - s), 0.0)
                x = np.where(a > 0, a ** s * p ** (-s) * m / w.sum(), 0.0)
            else:
                x = a * m / float(np.dot(p, a))
        return x

    def utility(self, x) -> float:
        x = np.asarray(x, float)
        a = np.asarray(self.a, float)
        with np.errstate(divide="ignore", invalid="ignore"):
            if self.kind == "cd":
                return float(np.sum(np.where(a > 0, a * np.log(x), 0.0)))
            if self.kind == "ces":
                return float(np.sum(a * x ** self.rho) ** (1.0 / self.rho))
            return float(np.min(x[a > 0] / a[a > 0]))


def excess(traders, p) -> np.ndarray:
    """Aggregate excess demand z(p) = sum of demands minus sum of endowments."""
    p = np.asarray(p, float)
    return sum(t.demand(p) for t in traders) - sum(np.asarray(t.e, float) for t in traders)


# ---------------------------------------------------------------------------------------------------------------
# the Edgeworth box: two Cobb-Douglas traders, two goods.  Allocations are written in A's coordinates.


def cd_indifference(a: float, u: float, x1):
    """Good 2 on the Cobb-Douglas indifference curve a log x1 + (1 - a) log x2 = u."""
    x1 = np.asarray(x1, float)
    return np.exp((u - a * np.log(x1)) / (1.0 - a))


def _cd_u(a, x1, x2):
    return a * np.log(x1) + (1 - a) * np.log(x2)


def contract_curve(A: Trader, B: Trader, x1):
    """A's good 2 on the contract curve, where the two marginal rates of substitution are equal, at A's good 1."""
    X = np.add(A.e, B.e)
    kA, kB = A.a[0] / A.a[1], B.a[0] / B.a[1]
    x1 = np.asarray(x1, float)
    return kB * x1 * X[1] / (kA * (X[0] - x1) + kB * x1)


def lens_ends(A: Trader, B: Trader) -> tuple[float, float]:
    """A's good 1 where the contract curve meets A's and B's indifference curves through the endowment: the
    individually rational stretch of the contract curve (the core of the two-trader economy) lies between."""
    X = np.add(A.e, B.e)
    uA0, uB0 = _cd_u(A.a[0], *A.e), _cd_u(B.a[0], *B.e)

    def gA(x):
        return _cd_u(A.a[0], x, contract_curve(A, B, x)) - uA0

    def gB(x):
        return _cd_u(B.a[0], X[0] - x, X[1] - contract_curve(A, B, x)) - uB0

    eps = 1e-9 * X[0]
    xw = box_equilibrium(A, B)["xA"][0]
    return brentq(gA, eps, xw), brentq(gB, xw, X[0] - eps)


def box_equilibrium(A: Trader, B: Trader) -> dict:
    """The competitive equilibrium of the box: the price of good 1 in units of good 2, and the allocation."""
    p = (A.a[0] * A.e[1] + B.a[0] * B.e[1]) / ((1 - A.a[0]) * A.e[0] + (1 - B.a[0]) * B.e[0])
    P = np.array([p, 1.0])
    return {"p": float(p), "xA": A.demand(P).tolist(), "xB": B.demand(P).tolist()}


def offer_curve(T: Trader, ps):
    """A trader's demands (good 1, good 2) as the relative price of good 1 runs over ``ps``."""
    out = np.array([T.demand([p, 1.0]) for p in np.atleast_1d(ps)])
    return out[:, 0], out[:, 1]


def blocks(A: Trader, B: Trader, x1: float, s: int, t: int) -> float:
    """How much better ``s`` copies of A can make themselves, with ``t`` copies of B kept as well off as at the
    contract-curve allocation with A's good 1 at ``x1``, trading only among themselves (equal treatment within each
    type).  Positive means the coalition blocks the allocation."""
    X = np.add(A.e, B.e)
    xA = np.array([x1, float(contract_curve(A, B, x1))])
    xB = X - xA
    uA, uB = _cd_u(A.a[0], *xA), _cd_u(B.a[0], *xB)
    R = s * np.asarray(A.e, float) + t * np.asarray(B.e, float)

    def value(lb1):
        b1 = np.exp(lb1)
        b2 = cd_indifference(B.a[0], uB, b1)
        a1, a2 = (R[0] - t * b1) / s, (R[1] - t * b2) / s
        with np.errstate(divide="ignore", invalid="ignore"):
            v = A.a[0] * np.log(a1) + (1 - A.a[0]) * np.log(a2)
        return np.where((a1 > 0) & (a2 > 0), v, -1e300)

    hi = np.log(R[0] / t)
    grid = np.linspace(hi - 25.0, hi - 1e-9, 2001)
    vals = value(grid)
    k = int(np.argmax(vals))
    lo_, hi_ = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    res = minimize_scalar(lambda g: -float(value(np.array([g]))[0]), bounds=(lo_, hi_), method="bounded",
                          options={"xatol": 1e-13})
    return float(max(-res.fun, vals[k]) - uA)


def core_interval(A: Trader, B: Trader, r: int, tol: float = 1e-7) -> tuple[float, float]:
    """A's good 1 at the two ends of the core of the ``r``-fold replicated box economy: the stretch of the contract
    curve that no coalition of at most ``r`` copies of each trader can block."""
    lo0, hi0 = lens_ends(A, B)
    xw = box_equilibrium(A, B)["xA"][0]

    def blocked(x):
        return any(blocks(A, B, x, s, t) > tol for s in range(1, r + 1) for t in range(1, r + 1) if s != t)

    def edge(inside, outside):
        if not blocked(outside):
            return outside
        for _ in range(40):
            mid = 0.5 * (inside + outside)
            if blocked(mid):
                outside = mid
            else:
                inside = mid
        return inside

    return edge(xw, lo0), edge(xw, hi0)


# ---------------------------------------------------------------------------------------------------------------
# existence: Sperner's lemma on the price simplex (three goods), and Scarf's walk


def simplex_point(v, N: int) -> np.ndarray:
    i, j = v
    return np.array([i, j, N - i - j], float) / N


def sperner_labels(z_of_p, N: int) -> dict:
    """Label every grid point (i, j) of the price simplex (p = (i, j, N - i - j) / N) with the first good whose price
    is positive and which is not in excess demand.  The labelling obeys Sperner's rule: a point on the face where
    good k's price is zero never gets label k."""
    labels = {}
    for i in range(N + 1):
        for j in range(N + 1 - i):
            p = simplex_point((i, j), N)
            with np.errstate(divide="ignore", invalid="ignore"):
                z = np.asarray(z_of_p(p), float)
            ok = [k for k in range(3) if p[k] > 0 and z[k] <= 1e-12]
            labels[(i, j)] = ok[0] if ok else int(np.argmax(p))
    return labels


def _triangles(N):
    tris = []
    for i in range(N):
        for j in range(N - i):
            tris.append(((i, j), (i + 1, j), (i, j + 1)))
            if i + j <= N - 2:
                tris.append(((i + 1, j), (i, j + 1), (i + 1, j + 1)))
    return tris


def sperner_walk(labels: dict, N: int) -> dict:
    """Scarf's door-to-door walk.  Doors are edges labelled {0, 1}.  Enter through the first door on the face where
    good 3's price is zero, leave each room by its other door, and stop in a room with all three labels.
    Returns the rooms visited, the last room, and its centre (an approximate equilibrium price vector)."""
    tris = _triangles(N)
    by_edge: dict = {}
    for t in tris:
        for a in range(3):
            e = frozenset((t[a], t[(a + 1) % 3]))
            by_edge.setdefault(e, []).append(t)

    def is_door(e):
        return {labels[v] for v in e} == {0, 1}

    start = None
    for i in range(N, 0, -1):          # along the face i + j = N, from (N, 0) towards (0, N)
        e = frozenset(((i, N - i), (i - 1, N - i + 1)))
        if is_door(e):
            start = e
            break
    room, came = by_edge[start][0], start
    path = [room]
    for _ in range(4 * len(tris)):
        if {labels[v] for v in room} == {0, 1, 2}:
            break
        doors = [frozenset((room[a], room[(a + 1) % 3])) for a in range(3)]
        out = [d for d in doors if is_door(d) and d != came][0]
        nxt = [t for t in by_edge[out] if t != room]
        if not nxt:
            raise RuntimeError("walked out of the simplex: the labelling is not a Sperner labelling")
        room, came = nxt[0], out
        path.append(room)
    centre = np.mean([simplex_point(v, N) for v in room], axis=0)
    return {"path": [[list(v) for v in t] for t in path], "room": [list(v) for v in room],
            "p": centre.tolist(), "rooms": len(path)}


# ---------------------------------------------------------------------------------------------------------------
# dynamics and computation


def tatonnement(z_of_p, p0, T: float = 20.0, n: int = 400, speed: float = 1.0) -> dict:
    """Walras's auctioneer: raise each price in proportion to its excess demand, dp/dt = speed * z(p).  By Walras's
    law the length of the price vector is conserved."""
    p0 = np.asarray(p0, float)
    sol = solve_ivp(lambda t, p: speed * np.asarray(z_of_p(p), float), (0, T), p0, t_eval=np.linspace(0, T, n),
                    rtol=1e-9, atol=1e-11)
    return {"t": sol.t.tolist(), "p": sol.y.T.tolist()}


def newton(z_of_p, p0, numeraire: int = 0, tol: float = 1e-12, maxit: int = 50, h: float = 1e-7) -> dict:
    """Newton's method on excess demand: fix one price at 1 and solve the other markets' clearing conditions (Walras's
    law clears the last).  Records each iterate and the largest excess demand there."""
    p = np.asarray(p0, float) / p0[numeraire]
    free = [k for k in range(len(p)) if k != numeraire]
    hist = []
    for _ in range(maxit):
        z = np.asarray(z_of_p(p), float)
        hist.append({"p": p.tolist(), "err": float(np.max(np.abs(z)))})
        if hist[-1]["err"] < tol:
            break
        J = np.empty((len(free), len(free)))
        for c, k in enumerate(free):
            dp = p.copy()
            dp[k] += h * p[k]
            J[:, c] = (np.asarray(z_of_p(dp), float)[free] - z[free]) / (h * p[k])
        step = np.linalg.solve(J, -z[free])
        lam = 1.0
        while np.any(p[free] + lam * step <= 0):
            lam *= 0.5
        p[free] = p[free] + lam * step
    return {"p": p.tolist(), "iterations": len(hist) - 1, "history": hist}


def scarf_excess(p) -> np.ndarray:
    """Scarf's (1960) economy: three traders, three goods; trader i owns one unit of good i and wants goods i and
    i + 1 in equal amounts (u_i = min(x_i, x_{i+1})).  Its only equilibrium is equal prices."""
    p = np.asarray(p, float)
    z = -np.ones(3)
    for i in range(3):
        j = (i + 1) % 3
        x = p[i] / (p[i] + p[j])
        z[i] += x
        z[j] += x
    return z


def scarf_path(p0, T: float = 60.0, n: int = 1200) -> dict:
    """The tatonnement path from ``p0`` in Scarf's economy, with its two conserved quantities (the sum of squared
    prices and their product): the path is a closed orbit around the equilibrium."""
    out = tatonnement(scarf_excess, p0, T=T, n=n)
    P = np.array(out["p"])
    out["norm"] = np.sum(P ** 2, axis=1).tolist()
    out["product"] = np.prod(P, axis=1).tolist()
    return out


# ---------------------------------------------------------------------------------------------------------------
# production: the Robinson Crusoe economy


def crusoe(A: float, alpha: float, hours: float, b: float) -> dict:
    """Crusoe has ``hours`` a day, makes coconuts c = A L^alpha, and has utility b log c + (1 - b) log(leisure).
    The planner's choice, and the market's: Crusoe the firm hires labour at wage w (coconuts are the numeraire) and
    pays out its profit to Crusoe the consumer, who supplies labour.  They coincide."""
    L_plan = alpha * b * hours / (alpha * b + 1 - b)

    def labour_gap(w):
        Ld = (alpha * A / w) ** (1 / (1 - alpha))
        profit = A * Ld ** alpha - w * Ld
        leisure = (1 - b) * (w * hours + profit) / w
        return Ld - (hours - leisure)

    w = brentq(labour_gap, 1e-6, 1e6)
    L = (alpha * A / w) ** (1 / (1 - alpha))
    c = A * L ** alpha
    return {"plan": {"L": L_plan, "c": A * L_plan ** alpha, "leisure": hours - L_plan},
            "market": {"w": w, "L": L, "c": c, "leisure": hours - L, "profit": c - w * L,
                       "mpl": alpha * A * L ** (alpha - 1)},
            "mrs": (1 - b) / b * c / (hours - L)}


# ---------------------------------------------------------------------------------------------------------------
# anything goes: multiple equilibria


def quasilinear_three(r: float | None = None) -> dict:
    """Two traders: A has u = x - y^(-8) / 8 and endowment (2, r); B has u = y - x^(-8) / 8 and endowment (r, 2).
    With r = 2^(8/9) - 2^(1/9) the excess demand for good 2 is zero at three relative prices of good 1: 1/2, 1, 2.
    Returns the excess demand for good 2 (per unit of good 2's price) as a function of q = p1 / p2."""
    if r is None:
        r = 2 ** (8 / 9) - 2 ** (1 / 9)

    def z2(q):
        q = np.asarray(q, float)
        return q ** (1 / 9) - q ** (8 / 9) + r * (q - 1)

    return {"r": r, "z2": z2, "equilibria": [0.5, 1.0, 2.0]}


def equilibria_2good(z1, lo: float = 1e-3, hi: float = 1e3, n: int = 2000) -> list[float]:
    """Every relative price q = p1 / p2 in [lo, hi] where the excess demand for good 1, ``z1(q)``, crosses zero."""
    qs = np.geomspace(lo, hi, n)
    zs = np.array([z1(q) for q in qs])
    roots = []
    for k in range(n - 1):
        if zs[k] == 0:
            roots.append(float(qs[k]))
        elif zs[k] * zs[k + 1] < 0:
            roots.append(float(brentq(z1, qs[k], qs[k + 1])))
    return roots


# ---------------------------------------------------------------------------------------------------------------
# time and uncertainty: contingent claims and Arrow securities


def _crra(c, g):
    c = np.asarray(c, float)
    return np.log(c) if g == 1 else (c ** (1 - g) - 1) / (1 - g)


def _crra_inv(u, g):
    return float(np.exp(u)) if g == 1 else float((u * (1 - g) + 1) ** (1 / (1 - g)))


def _lifetime(c0, cs, probs, beta, g):
    return float(_crra(c0, g) + beta * np.dot(probs, _crra(cs, g)))


def certain_equivalent(c0, cs, probs, beta, g) -> float:
    """The constant consumption, today and in every state tomorrow, that is as good as (c0, cs)."""
    return _crra_inv(_lifetime(c0, cs, probs, beta, g) / (1 + beta), g)


def arrow_debreu(e0, E, probs, beta: float, gammas) -> dict:
    """Traders with ``e0[i]`` today and ``E[i][s]`` tomorrow in state s (probabilities ``probs``), each maximizing
    u(c0) + beta * sum_s probs_s u(c_s) with relative risk aversion ``gammas[i]``.  Complete markets: one Arrow
    security per state, paying one unit of the good in that state only, priced q_s in today's good.  Returns the
    prices, the allocation, the securities each trader buys, and certainty equivalents (with autarky's)."""
    e0, E, pr = np.asarray(e0, float), np.asarray(E, float), np.asarray(probs, float)
    n, S = E.shape

    def plan(i, q):
        g = gammas[i]
        w = e0[i] + float(q @ E[i])
        k = (beta * pr / q) ** (1 / g)          # c_s = k_s c0
        c0 = w / (1 + float(q @ k))
        return c0, k * c0

    def z(lq):
        q = np.exp(lq)
        return np.array([sum(plan(i, q)[1][s] for i in range(n)) - E[:, s].sum() for s in range(S)])

    from scipy.optimize import fsolve  # noqa: PLC0415
    q = np.exp(fsolve(z, np.log(beta * pr), xtol=1e-14))
    plans = [plan(i, q) for i in range(n)]
    c0 = np.array([p_[0] for p_ in plans])
    C = np.array([p_[1] for p_ in plans])
    return {"q": q.tolist(), "c0": c0.tolist(), "c": C.tolist(), "securities": (C - E).tolist(),
            "bond_price": float(q.sum()),
            "ce": [certain_equivalent(c0[i], C[i], pr, beta, gammas[i]) for i in range(n)],
            "ce_autarky": [certain_equivalent(e0[i], E[i], pr, beta, gammas[i]) for i in range(n)]}


def bond_only(e0, E, probs, beta: float, gammas) -> dict:
    """The same economy with one asset only, a riskless bond paying one unit in every state, in zero net supply: the
    bond's price that clears its market, each trader's holding, the allocation and certainty equivalents.  The bond
    moves consumption between today and tomorrow, but not between the states: risk is not shared."""
    e0, E, pr = np.asarray(e0, float), np.asarray(E, float), np.asarray(probs, float)
    n = len(e0)

    def holding(i, qb):
        g = gammas[i]
        lo = -E[i].min() * (1 - 1e-9)
        hi = e0[i] / qb * (1 - 1e-9)

        def foc(b):
            return -qb * (e0[i] - qb * b) ** (-g) + beta * float(pr @ ((E[i] + b) ** (-g)))
        return brentq(foc, lo, hi)

    qb = brentq(lambda q: sum(holding(i, q) for i in range(n)), 1e-4, 1e4)
    b = np.array([holding(i, qb) for i in range(n)])
    c0 = e0 - qb * b
    C = E + b[:, None]
    return {"q_bond": float(qb), "b": b.tolist(), "c0": c0.tolist(), "c": C.tolist(),
            "ce": [certain_equivalent(c0[i], C[i], pr, beta, gammas[i]) for i in range(n)]}


# ---------------------------------------------------------------------------------------------------------------
# planning: Kantorovich's linear programme


def kantorovich(rates, kit) -> dict:
    """Machines i = 1..m can make part j at ``rates[i][j]`` units a day; a complete set needs ``kit[j]`` of each
    part.  Choose the share of each machine's day on each part to make the most complete sets.  Returns the plan,
    the number of sets, and the dual prices: the value of a day on each machine and of a unit of each part (Kantorovich's
    resolving multipliers).  Every machine works only on parts whose value per day on it equals the day's value."""
    R = np.asarray(rates, float)
    k = np.asarray(kit, float)
    m, n = R.shape
    # variables: t_ij (m*n), then z; maximize z
    c = np.zeros(m * n + 1)
    c[-1] = -1.0
    A_ub, b_ub = [], []
    for i in range(m):                                      # each machine's day: sum_j t_ij <= 1
        row = np.zeros(m * n + 1)
        row[i * n:(i + 1) * n] = 1.0
        A_ub.append(row)
        b_ub.append(1.0)
    for j in range(n):                                      # parts: k_j z - sum_i r_ij t_ij <= 0
        row = np.zeros(m * n + 1)
        for i in range(m):
            row[i * n + j] = -R[i, j]
        row[-1] = k[j]
        A_ub.append(row)
        b_ub.append(0.0)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=[(0, None)] * (m * n + 1), method="highs")
    assert res.status == 0, res.message
    t = res.x[:-1].reshape(m, n)
    duals = -np.asarray(res.ineqlin.marginals)
    machine_value, part_value = duals[:m], duals[m:]
    return {"plan": t.tolist(), "sets": float(res.x[-1]), "output": (R * t).sum(axis=0).tolist(),
            "machine_value": machine_value.tolist(), "part_value": part_value.tolist(),
            "value_per_day": (R * part_value[None, :]).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# misallocation: equal marginal products, and what their dispersion costs


def misallocation(log_A, log_tfpr, sigma: float = 3.0) -> dict:
    """An industry of plants that make varieties of one good (elasticity of substitution ``sigma`` between them),
    with labour only: plant i's physical productivity A_i and its revenue productivity TFPR_i, which with equal
    marginal products would be the same everywhere.  Output relative to the efficient allocation of the same labour,
    computed directly, and Hsieh and Klenow's formula for lognormal TFPR independent of A:
    log(Y_eff / Y) = (sigma / 2) var(log TFPR)."""
    A = np.exp(np.asarray(log_A, float))
    tau = np.exp(np.asarray(log_tfpr, float))
    e = (sigma - 1) / sigma

    def output(L):
        return float(np.sum((A * L) ** e) ** (1 / e))

    # revenue p_i y_i = Y^(1/sigma) y_i^e, so MRPL_i = e Y^(1/sigma) A_i^e L_i^(e-1); with MRPL_i proportional to
    # tau_i, L_i is proportional to A_i^(sigma-1) tau_i^(-sigma)
    L = A ** (sigma - 1) * tau ** (-sigma)
    L /= L.sum()
    Le = A ** (sigma - 1)
    Le /= Le.sum()
    gain = output(Le) / output(L) - 1
    return {"gain": gain, "lognormal": float(np.exp(sigma / 2 * np.var(np.log(tau))) - 1),
            "sd_log_tfpr": float(np.std(np.log(tau)))}


# ---------------------------------------------------------------------------------------------------------------
# indivisibilities: the housing market


def top_trading_cycles(prefs) -> dict:
    """Shapley and Scarf's (1974) housing market: islander i owns hut i and ranks all huts (``prefs[i]``, best first).
    Gale's top trading cycles: each points at the owner of the best remaining hut; trade along every cycle; remove
    and repeat.  Returns the assignment and the cycles, round by round; the result is in the core."""
    n = len(prefs)
    left = set(range(n))
    assign = {}
    rounds = []
    while left:
        point = {i: next(h for h in prefs[i] if h in left) for i in left}
        seen, cycles = set(), []
        for s in sorted(left):
            if s in seen:
                continue
            path, x = [], s
            while x not in path and x not in seen:
                path.append(x)
                x = point[x]
            if x in path:
                cyc = path[path.index(x):]
                cycles.append(cyc)
            seen.update(path)
        for cyc in cycles:
            for i in cyc:
                assign[i] = point[i]
            left -= set(cyc)
        rounds.append({"pointing": {int(k): int(v) for k, v in point.items()}, "cycles": cycles})
    return {"assign": [assign[i] for i in range(n)], "rounds": rounds}
