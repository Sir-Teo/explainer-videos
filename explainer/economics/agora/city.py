"""Agora's city (Part 37): Schelling's checkerboard; von Thünen's rings; the monocentric city of Alonso, Muth and
Mills, closed, with housing built from land and capital; agglomeration with workers who sort, estimated across towns
and from movers; Zipf's law and Gibrat's proportional growth with a floor (Gabaix 1999); Krugman's core and
periphery (1991) with its tomahawk; a Rosen-Roback system of towns, read for quality of life, misallocation and the
incidence of a place-based subsidy; and a small quantitative spatial model on a line, after Ahlfeldt, Redding, Sturm
and Wolf (2015), divided by a wall.

numpy and scipy only.  Distances are in kilometres; the monocentric city's money is in thousands of dollars a year.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

_OFFSETS = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)]


# --- Schelling's checkerboard ----------------------------------------------------------------------------------------
def _neighbour_counts(g: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    a, b = (g == 1).astype(int), (g == 2).astype(int)
    ca, cb = np.zeros_like(a), np.zeros_like(b)
    for dr, dc in _OFFSETS:
        ca += np.roll(np.roll(a, dr, 0), dc, 1)
        cb += np.roll(np.roll(b, dr, 0), dc, 1)
    return ca, cb


def like_share(g: np.ndarray) -> float:
    """The mean, over occupied squares with at least one neighbour, of the share of neighbours of the same kind
    (eight neighbours, on a board whose edges wrap round)."""
    ca, cb = _neighbour_counts(g)
    tot = ca + cb
    occ = (g > 0) & (tot > 0)
    own = np.where(g == 1, ca, cb)
    return float(np.mean(own[occ] / tot[occ]))


def schelling(n: int = 40, empty: float = 0.1, threshold: float = 1 / 3, seed: int = 0, rounds: int = 60,
              keep_frames: bool = True, share: float = 0.5) -> dict:
    """Two kinds of coin (a share ``share`` of the first) on an ``n`` by ``n`` board with a share ``empty`` of squares
    empty.  A coin is
    content if at least ``threshold`` of its occupied neighbours are its own kind (a coin with no neighbours is
    content).  Each round the discontented coins, in random order, move to a random empty square where they would be
    content, if there is one.  Stops when everyone is content or after ``rounds`` rounds.

    Returns the boards after each round (``frames``, 0 empty, 1 and 2 the kinds), the like-share and the number of
    discontented coins by round, the moves made, and whether the board settled."""
    rng = np.random.default_rng(seed)
    cells = n * n
    n_agents = cells - int(round(empty * cells))
    flat = np.zeros(cells, dtype=np.int8)
    order = rng.permutation(cells)
    n_a = int(round(n_agents * share))
    flat[order[:n_a]] = 1
    flat[order[n_a: n_agents]] = 2
    g = flat.reshape(n, n)
    ca, cb = _neighbour_counts(g)
    counts = {1: ca, 2: cb}

    def share_at(r, c, t):
        tot = ca[r, c] + cb[r, c]
        return 1.0 if tot == 0 else counts[t][r, c] / tot

    def bump(r, c, t, d):
        for dr, dc in _OFFSETS:
            counts[t][(r + dr) % n, (c + dc) % n] += d

    frames = [g.copy()] if keep_frames else []
    like, unhappy_n, moves = [like_share(g)], [], 0
    settled = False
    for _ in range(rounds):
        occ = np.argwhere(g > 0)
        unhappy = [(int(r), int(c)) for r, c in occ if share_at(r, c, int(g[r, c])) < threshold]
        unhappy_n.append(len(unhappy))
        if not unhappy:
            settled = True
            break
        rng.shuffle(unhappy)
        for r, c in unhappy:
            t = int(g[r, c])
            if share_at(r, c, t) >= threshold:
                continue
            em = np.argwhere(g == 0)
            own = counts[t][em[:, 0], em[:, 1]].astype(float)
            tot = (ca + cb)[em[:, 0], em[:, 1]].astype(float)
            dr = np.abs(em[:, 0] - r)
            dc = np.abs(em[:, 1] - c)
            adj = (np.minimum(dr, n - dr) <= 1) & (np.minimum(dc, n - dc) <= 1)
            own -= adj
            tot -= adj
            ok = np.where(tot > 0, own / np.maximum(tot, 1), 1.0) >= threshold
            if not ok.any():
                continue
            r1, c1 = em[rng.choice(np.flatnonzero(ok))]
            g[r, c] = 0
            bump(r, c, t, -1)
            g[r1, c1] = t
            bump(r1, c1, t, +1)
            moves += 1
        like.append(like_share(g))
        if keep_frames:
            frames.append(g.copy())
    if not settled:
        occ = np.argwhere(g > 0)
        settled = not any(share_at(r, c, int(g[r, c])) < threshold for r, c in occ)
    return {"frames": [f.tolist() for f in frames], "like": like, "unhappy": unhappy_n, "moves": moves,
            "settled": settled, "final_like": like[-1], "rounds": len(like) - 1, "n": n, "threshold": threshold}


def schelling_sweep(thresholds, seeds=(0, 1, 2), n: int = 30, empty: float = 0.1, rounds: int = 60) -> dict:
    """The final like-share, averaged over ``seeds``, for each tolerance threshold, and the share of runs that
    settled."""
    like, settled = [], []
    for th in thresholds:
        rs = [schelling(n, empty, th, s, rounds, keep_frames=False) for s in seeds]
        like.append(float(np.mean([r["final_like"] for r in rs])))
        settled.append(float(np.mean([r["settled"] for r in rs])))
    return {"thresholds": list(map(float, thresholds)), "like": like, "settled": settled}


# --- von Thünen's isolated state -------------------------------------------------------------------------------------
def thunen(crops: list[dict], x: np.ndarray) -> dict:
    """Land around one market town.  Each crop has a yield per hectare, a price and a production cost per ton at
    market, and a freight cost per ton-kilometre; its bid rent at distance ``x`` is yield (price - cost - freight x).
    Land goes to the highest bidder, and lies idle where every bid is negative.  Returns each crop's bid-rent curve,
    the winning crop at each distance (-1 idle), and the rings as (name, from, to)."""
    x = np.asarray(x, float)
    bids = np.array([c["yield"] * (c["price"] - c["cost"] - c["freight"] * x) for c in crops])
    win = np.argmax(bids, axis=0)
    win = np.where(bids.max(axis=0) > 0, win, -1)
    rings, start = [], 0
    for k in range(1, len(x) + 1):
        if k == len(x) or win[k] != win[start]:
            if win[start] >= 0:
                rings.append((crops[win[start]]["name"], float(x[start]), float(x[k - 1])))
            start = k
    return {"x": x.tolist(), "bids": bids.tolist(), "rent": np.maximum(bids.max(axis=0), 0).tolist(),
            "winner": win.tolist(), "rings": rings}


# --- the monocentric city -------------------------------------------------------------------------------------------
def _mono_profile(u, x, y, t, alpha, theta, i, A):
    k = alpha ** alpha * (1 - alpha) ** (1 - alpha)
    net = np.maximum(y - t * x, 1e-9)
    p = (k * net / u) ** (1 / alpha)                     # floor rent per square metre a year
    h = alpha * net / p                                  # floor space per household
    S = (p * A * (1 - theta) / i) ** (1 / theta)         # capital per square metre of land: the height of buildings
    far = A * S ** (1 - theta)                           # floor space per square metre of land
    r = theta * p * far                                  # land rent per square metre a year
    D = far / h * 1e6                                    # households per square kilometre
    return p, h, S, far, r, D


def monocentric(N: float = 1.0e6, y: float = 60.0, t: float = 1.0, alpha: float = 0.25, theta: float = 0.25,
                i: float = 0.06, A: float = 1.0, r_ag: float = 1e-4, x_max: float = 60.0, n: int = 1200) -> dict:
    """A closed city of ``N`` households with income ``y`` (thousands of dollars a year) who commute to one centre at
    ``t`` a kilometre a year.  Utility c^(1-alpha) h^alpha over goods and floor space; floor space is built from land
    and capital with output per square metre of land A S^(1-theta) (S, capital per square metre, measures height;
    ``i`` is capital's yearly cost).  Land at the edge is worth ``r_ag`` a square metre a year in farming.

    Spatial equilibrium: everyone gets the same utility, so floor rents fall with distance exactly enough to pay for
    the commute; developers build up where floor rents are high.  Returns the profiles along x (floor rent, floor
    space per household, height, floor-area ratio, land rent, households per square kilometre), the edge, utility
    and the share of households within 8 km of the centre."""
    x = np.linspace(0.0, x_max, n)

    def pop(u):
        p, h, S, far, r, D = _mono_profile(u, x, y, t, alpha, theta, i, A)
        inside = r >= r_ag
        return float(np.trapezoid(np.where(inside, D * 2 * np.pi * x, 0.0), x))

    lo, hi = 1e-3, 1e3
    logu = brentq(lambda lu: pop(np.exp(lu)) - N, np.log(lo), np.log(hi), xtol=1e-12)
    u = float(np.exp(logu))
    p, h, S, far, r, D = _mono_profile(u, x, y, t, alpha, theta, i, A)
    inside = r >= r_ag
    edge = float(x[inside][-1]) if inside.any() else 0.0
    dens = np.where(inside, D, 0.0)
    within8 = float(np.trapezoid(np.where(x <= 8, dens * 2 * np.pi * x, 0), x) / N)
    return {"x": x.tolist(), "p": np.where(inside, p, np.nan).tolist(), "h": np.where(inside, h, np.nan).tolist(),
            "S": np.where(inside, S, np.nan).tolist(), "far": np.where(inside, far, np.nan).tolist(),
            "r": np.where(inside, r, np.nan).tolist(), "D": dens.tolist(), "edge": edge, "u": u,
            "centre_density": float(dens[0]), "within8": within8, "params": {"N": N, "y": y, "t": t, "alpha": alpha,
                                                                            "theta": theta, "i": i, "A": A}}


# --- agglomeration and sorting ---------------------------------------------------------------------------------------
def agglomeration_panel(n_towns: int = 60, n_workers: int = 60000, gamma: float = 0.03, sort: float = 0.3,
                        sd_ability: float = 0.3, move: float = 0.2, seed: int = 0) -> dict:
    """Towns differ in density; productivity rises with density at elasticity ``gamma``.  Workers differ in ability,
    and abler workers choose denser towns (a logit with taste ``sort`` times ability times log density).  In a second
    year a share ``move`` of workers move to a town drawn at random.  log wage = ability + town productivity + noise.

    Two estimates of gamma: across towns, the slope of the mean log wage on log density, which also picks up who
    lives where; and from movers, the change in a mover's log wage on the change in density, which differences
    ability away."""
    rng = np.random.default_rng(seed)
    d = rng.normal(0, 1, n_towns)
    d -= d.mean()
    logA = gamma * d + rng.normal(0, 0.005, n_towns)
    a = rng.normal(0, sd_ability, n_workers)
    util = sort * np.outer(a, d) + rng.gumbel(size=(n_workers, n_towns))
    town1 = np.argmax(util, axis=1)
    movers = rng.random(n_workers) < move
    town2 = town1.copy()
    town2[movers] = rng.integers(0, n_towns, movers.sum())
    w1 = a + logA[town1] + rng.normal(0, 0.1, n_workers)
    w2 = a + logA[town2] + rng.normal(0, 0.1, n_workers)
    cnt = np.bincount(town1, minlength=n_towns)
    mean_w = np.bincount(town1, weights=w1, minlength=n_towns) / np.maximum(cnt, 1)
    mean_a = np.bincount(town1, weights=a, minlength=n_towns) / np.maximum(cnt, 1)
    keep = cnt > 0
    naive = float(np.polyfit(d[keep], mean_w[keep], 1)[0])
    sorting = float(np.polyfit(d[keep], mean_a[keep], 1)[0])
    real = movers & (town2 != town1)
    dd, dw = d[town2[real]] - d[town1[real]], w2[real] - w1[real]
    fe = float(np.sum(dd * (dw - dw.mean())) / np.sum(dd * (dd - dd.mean())))
    return {"d": d.tolist(), "mean_w": mean_w.tolist(), "mean_a": mean_a.tolist(), "count": cnt.tolist(),
            "naive": naive, "sorting": sorting, "movers": fe, "n_movers": int(real.sum()), "gamma": gamma,
            "mover_dd": dd[:400].tolist(), "mover_dw": dw[:400].tolist()}


# --- Zipf and Gibrat --------------------------------------------------------------------------------------------------
def zipf_fit(sizes, top: int | None = None) -> dict:
    """Rank-size regression with Gabaix and Ibragimov's correction: log(rank - 1/2) on log size over the ``top``
    largest.  Returns the exponent zeta (minus the slope), its standard error zeta (2/n)^(1/2), the intercept, and the
    points."""
    s = np.sort(np.asarray(sizes, float))[::-1]
    if top:
        s = s[:top]
    n = len(s)
    rank = np.arange(1, n + 1)
    b, c = np.polyfit(np.log(s), np.log(rank - 0.5), 1)
    zeta = -float(b)
    return {"zeta": zeta, "se": zeta * np.sqrt(2.0 / n), "intercept": float(c), "n": n, "size": s.tolist(),
            "rank": rank.tolist()}


def gibrat(n: int = 20000, T: int = 3000, sigma: float = 0.2, floor: float = 0.05, seed: int = 0,
           track: int = 6) -> dict:
    """Gibrat's law with a floor (Gabaix 1999): each period every town's size, relative to the mean, is multiplied by
    an independent shock with no drift; a town that would fall below ``floor`` times the mean stays at the floor.
    Growth is independent of size, and the steady state is a power law with exponent 1 / (1 - floor), close to one
    when the floor is low.  Returns the final sizes, the exponent fitted on the largest tenth, the paths of
    ``track`` towns, and the spread of growth rates by size quintile (near equal: Gibrat)."""
    rng = np.random.default_rng(seed)
    s = np.ones(n)
    paths = []
    for _ in range(T):
        s = s * np.exp(rng.normal(-sigma ** 2 / 2, sigma, n))
        s = np.maximum(s, floor * s.mean())
        s /= s.mean()
        paths.append(s[:track].copy())
    s0 = s.copy()
    s1 = np.maximum(s0 * np.exp(rng.normal(-sigma ** 2 / 2, sigma, n)), floor * s0.mean())
    g = np.log(s1 / s0)
    q = np.quantile(s0, [0.2, 0.4, 0.6, 0.8])
    bins = np.digitize(s0, q)
    big = s0 > floor * s0.mean() * 1.0001
    sd_by_q = [float(np.std(g[(bins == k) & big])) if np.any((bins == k) & big) else float("nan") for k in range(5)]
    fit = zipf_fit(s0, top=n // 10)
    return {"sizes": s0.tolist(), "zeta": fit["zeta"], "se": fit["se"], "theory": 1.0 / (1.0 - floor),
            "paths": np.array(paths)[:: max(1, T // 300)].tolist(), "growth_sd_by_quintile": sd_by_q}


# --- Krugman's core and periphery -----------------------------------------------------------------------------------
def cp_solve(lam: float, T: float, mu: float = 0.4, sigma: float = 5.0, tol: float = 1e-13,
             max_iter: int = 20000) -> dict:
    """Krugman (1991) as in Fujita, Krugman and Venables (1999, ch. 5): two regions, farmers (1 - mu, split evenly,
    immobile, wage 1) and manufacturing workers (mu, a share ``lam`` in region 1), varieties with elasticity
    ``sigma``, iceberg cost ``T``.  Solves incomes, price indices and nominal wages by damped iteration; real wages
    are omega = w G^(-mu)."""
    w1 = w2 = 1.0
    for _ in range(max_iter):
        Y1 = mu * lam * w1 + (1 - mu) / 2
        Y2 = mu * (1 - lam) * w2 + (1 - mu) / 2
        G1 = (lam * w1 ** (1 - sigma) + (1 - lam) * (w2 * T) ** (1 - sigma)) ** (1 / (1 - sigma))
        G2 = (lam * (w1 * T) ** (1 - sigma) + (1 - lam) * w2 ** (1 - sigma)) ** (1 / (1 - sigma))
        n1 = (Y1 * G1 ** (sigma - 1) + Y2 * G2 ** (sigma - 1) * T ** (1 - sigma)) ** (1 / sigma)
        n2 = (Y1 * G1 ** (sigma - 1) * T ** (1 - sigma) + Y2 * G2 ** (sigma - 1)) ** (1 / sigma)
        if abs(n1 - w1) + abs(n2 - w2) < tol:
            w1, w2 = n1, n2
            break
        w1, w2 = 0.5 * w1 + 0.5 * n1, 0.5 * w2 + 0.5 * n2
    return {"w1": w1, "w2": w2, "G1": G1, "G2": G2, "Y1": Y1, "Y2": Y2, "omega1": w1 * G1 ** (-mu),
            "omega2": w2 * G2 ** (-mu)}


def cp_gap(T: float, lams, mu: float = 0.4, sigma: float = 5.0) -> list:
    """The real-wage gap omega1 - omega2 against region 1's share of manufacturing (the 'wiggle' diagram)."""
    out = []
    for lam in lams:
        e = cp_solve(float(np.clip(lam, 1e-6, 1 - 1e-6)), T, mu, sigma)
        out.append(e["omega1"] - e["omega2"])
    return out


def cp_break(mu: float = 0.4, sigma: float = 5.0) -> float:
    """The break point: the trade cost below which the symmetric spread of industry is unstable (Fujita, Krugman
    and Venables 1999, eq. 5.27): T^(sigma-1) = (rho + mu)(1 + mu) / ((rho - mu)(1 - mu)), rho = (sigma - 1)/sigma."""
    rho = (sigma - 1) / sigma
    return float(((rho + mu) * (1 + mu) / ((rho - mu) * (1 - mu))) ** (1 / (sigma - 1)))


def cp_sustain(mu: float = 0.4, sigma: float = 5.0) -> float:
    """The sustain point: the trade cost below which all industry in one region is an equilibrium (no worker
    gains by leaving), found as the root of omega2/omega1 = 1 at full agglomeration."""
    def f(T):
        e = cp_solve(1 - 1e-9, T, mu, sigma)
        return e["omega2"] / e["omega1"] - 1.0
    return float(brentq(f, 1.0001, 6.0, xtol=1e-10))


def cp_tomahawk(Ts, mu: float = 0.4, sigma: float = 5.0, n_lam: int = 81) -> dict:
    """For each trade cost, the equilibria in region 1's share of industry and whether each is stable: the symmetric
    spread (0.5), full agglomeration (0 and 1, an equilibrium when nobody gains by leaving) and interior ones where
    the gap changes sign.  Stable interior points are where the gap falls through zero."""
    lams = np.linspace(0, 1, n_lam)
    out = []
    for T in Ts:
        gap = np.array(cp_gap(T, lams, mu, sigma))
        eq = []
        for k in range(1, n_lam - 1):
            if abs(lams[k] - 0.5) < 1e-9:
                eq.append((0.5, bool(gap[k + 1] < gap[k - 1])))
            elif gap[k - 1] * gap[k] < 0 and abs(lams[k] - 0.5) > 1e-9 and abs(lams[k - 1] - 0.5) > 1e-9:
                lo, hi = lams[k - 1], lams[k]
                root = brentq(lambda z: cp_gap(T, [z], mu, sigma)[0], lo, hi, xtol=1e-8)
                eq.append((float(root), bool(gap[k] < gap[k - 1])))
        if gap[-1] > 0:
            eq += [(1.0, True), (0.0, True)]
        out.append({"T": float(T), "eq": sorted(eq)})
    return {"T": list(map(float, Ts)), "points": out, "break": cp_break(mu, sigma), "sustain": cp_sustain(mu, sigma)}


# --- Rosen and Roback: a system of towns ---------------------------------------------------------------------------
def roback(a, q, eta, c=None, b: float = 0.3, alpha: float = 0.3, N: float = 1.0) -> dict:
    """Towns j with productivity ``a`` (log), amenity ``q`` (log utility) and housing supply elasticity ``eta``.
    Labour demand: log w = a - b log N; housing: log r = c + (log N - log N0) / eta, a supply curve through the rent
    ``c`` at the average town's size N0 = N / J, steeper where ``eta`` is low; utility log w - alpha log r + q is the
    same everywhere (workers are free to move), and populations add up to ``N``.  Output in town j is
    exp(a) N^(1-b) / (1 - b).  Returns log populations, wages, rents, the common utility, total output and the
    quality of life read back from wages and rents (alpha log r - log w, demeaned), which equals the amenity."""
    a, q, eta = (np.asarray(v, float) for v in (a, q, eta))
    c = np.zeros_like(a) if c is None else np.asarray(c, float)
    n0 = np.log(N / len(a))

    def logN(v):
        return (a - alpha * c + alpha * n0 / eta + q - v) / (b + alpha / eta)

    v = brentq(lambda v: np.log(np.sum(np.exp(logN(v)))) - np.log(N), -50, 50, xtol=1e-13)
    n = logN(v)
    lw, lr = a - b * n, c + (n - n0) / eta
    Y = float(np.sum(np.exp(a) * np.exp(n) ** (1 - b) / (1 - b)))
    return {"logN": n.tolist(), "N": np.exp(n).tolist(), "logw": lw.tolist(), "logr": lr.tolist(), "v": float(v),
            "output": Y, "qol": (alpha * lr - lw - np.mean(alpha * lr - lw)).tolist()}


def roback_shock(a, q, eta, j: int, da: float = 0.0, dq: float = 0.0, deta: float | None = None, **kw) -> dict:
    """Town ``j`` gains ``da`` of productivity or ``dq`` of amenity (or a new supply elasticity ``deta``): the changes
    in its log wage, rent and population, in everyone's utility, and in total output."""
    base = roback(a, q, eta, **kw)
    a2, q2, e2 = np.array(a, float), np.array(q, float), np.array(eta, float)
    a2[j] += da
    q2[j] += dq
    if deta is not None:
        e2[j] = deta
    new = roback(a2, q2, e2, **kw)
    return {"dlogw": new["logw"][j] - base["logw"][j], "dlogr": new["logr"][j] - base["logr"][j],
            "dlogN": new["logN"][j] - base["logN"][j], "dv": new["v"] - base["v"],
            "doutput": new["output"] / base["output"] - 1, "base": base, "new": new}


# --- a quantitative spatial model on a line -------------------------------------------------------------------------
def qsm_line(J: int = 61, half: float = 6.0, cbd: float = 1.5, sub: float = -3.5, wall: bool = False,
             west_H: float | None = None,
             eps: float = 6.83, nu: float = 0.25, beta: float = 0.75, alpha: float = 0.8, lam: float = 0.07,
             delta: float = 0.36, damp: float = 0.3, tol: float = 1e-10, max_iter: int = 20000) -> dict:
    """A city of ``J`` blocks on a line from -``half`` to ``half`` km, its old centre of business at ``cbd`` (east of
    0, where a wall can run) and a smaller western centre at ``sub``. After Ahlfeldt, Redding, Sturm and Wolf
    (2015): workers choose where to live and where to work with Frechet tastes (shape ``eps``); commuting costs
    exp(nu |x_i - x_j| / eps) in utility; residents spend 1 - ``beta`` of income on floor space; firms produce
    with labour (share ``alpha``) and floor space; productivity is a fundamental (higher near the centre) times
    the surrounding employment to the power ``lam``, which decays with distance at ``delta``. Each block has one
    unit of residential and one of commercial floor. With ``wall`` the city is cut at 0: only the western blocks
    are solved, as a closed city of ``west_H`` workers, with no commuting to the east and no spillovers from it.
    Returns residential and commercial floor prices and their average (``floor``: one unit of each per block),
    residents, workers and wages by block. Price levels are not comparable between a divided and an integrated
    city, so compare changes relative to an average, as :func:`wall_experiment` does."""
    x = np.linspace(-half, half, J)
    if wall:
        x = x[x < 0]
    n = len(x)
    H = 1.0 if west_H is None else west_H
    afund = 1.0 + 1.5 * np.exp(-((x - cbd) / 1.0) ** 2) + 0.3 * np.exp(-((x - sub) / 1.0) ** 2)
    dist = np.abs(x[:, None] - x[None, :])
    dcost = np.exp(-nu * dist)                           # (d_ij)^(-eps), with nu = eps * kappa
    decay = np.exp(-delta * dist)
    w, Q = np.ones(n), np.ones(n)
    for it in range(max_iter):
        num = (w[None, :] ** eps) * dcost * (Q[:, None] ** (-(1 - beta) * eps))
        pi = num / num.sum()
        HR, HM = H * pi.sum(1), H * pi.sum(0)
        v = (pi * w[None, :]).sum(1) / pi.sum(1)
        A = afund * (decay @ HM) ** lam
        w_new = alpha * A * (1.0 / np.maximum(HM, 1e-300)) ** (1 - alpha)
        Q_new = (1 - beta) * v * HR
        err = np.max(np.abs(np.log(w_new / w))) + np.max(np.abs(np.log(Q_new / Q)))
        w = np.exp((1 - damp) * np.log(w) + damp * np.log(w_new))
        Q = np.exp((1 - damp) * np.log(Q) + damp * np.log(Q_new))
        if err < tol:
            break
    Y = A * HM ** alpha
    q = (1 - alpha) * Y
    return {"x": x.tolist(), "Q": Q.tolist(), "q": q.tolist(), "floor": (0.5 * (Q + q)).tolist(), "HR": HR.tolist(),
            "HM": HM.tolist(),
            "w": w.tolist(), "A": A.tolist(), "iterations": it + 1, "converged": bool(err < tol)}


def wall_experiment(**kw) -> dict:
    """The city integrated, then divided (the western blocks alone, with the same residents), then reunited: the
    change in each western block's log floor price on division and on reunification, relative to the western
    average, against its distance to the old centre."""
    I = qsm_line(**kw)
    x = np.array(I["x"])
    west = x < 0
    D = qsm_line(wall=True, west_H=float(np.sum(np.array(I["HR"])[west])), **kw)
    fi, fd = np.log(np.array(I["floor"])[west]), np.log(np.array(D["floor"]))
    div = fd - fi
    div -= div.mean()
    cbd = kw.get("cbd", 1.5)
    emp_east = float(np.sum(np.array(I["HM"])[~west]))
    return {"x": x[west].tolist(), "dist": (cbd - x[west]).tolist(), "division": div.tolist(),
            "reunification": (-div).tolist(), "integrated": I, "divided": D, "jobs_east": emp_east,
            "slope": float(np.polyfit(cbd - x[west], div, 1)[0])}
