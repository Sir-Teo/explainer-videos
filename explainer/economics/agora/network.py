"""Agora's economy as a network (Part 63): the Island's sectors linked by an input-output table, and the graphs that
carry shocks, money, information and influence.

* **Leontief** (:func:`island_table`, :func:`leontief`): the Island's eight sectors, the Leontief inverse as a sum over
  supply paths, Domar weights (sales over GDP), upstreamness.
* **Production networks** (:func:`ces_prices`, :func:`gdp_response`): sectors produce with labour and intermediate
  inputs under a constant elasticity of substitution; prices solve a fixed point; real GDP's response to a sector's
  productivity shock against Hulten's first-order rule (after Baqaee and Farhi).
* **Play it** (:func:`which_failure`): five Island firms; which one's failure costs the economy most?
* **Granularity** (:func:`granular`): aggregate volatility from firm shocks with Zipf-sized against equal firms
  (after Gabaix); a star against a ring of sectors (after Acemoglu, Carvalho, Ozdaglar and Tahbaz-Salehi).
* **The O-ring** (:func:`oring`): Kremer's production function and sorting by skill.
* **Financial networks** (:func:`clearing`, :func:`contagion`): the Eisenberg-Noe clearing vector; a ring against a
  complete network of banks for small and large shocks.
* **Weak ties** (:func:`weak_ties`): new information against willingness to pass it on.
* **Diffusion** (:func:`diffusion`): seeding a village network at central, random or peripheral households.
* **Key players** (:func:`key_player`): Bonacich centrality and the player whose removal cuts activity most.
* **Network formation** (:func:`formation`): Jackson and Wolinsky's connections model, stable against efficient.

numpy and scipy only.
"""

from __future__ import annotations

import itertools

import numpy as np

# ---------------------------------------------------------------------------------------------------------------
# the Island's input-output table

SECTORS = ("farms", "energy", "chips", "metals", "factories", "transport", "services", "retail")
# share of each sector's costs paid to each supplier (rows: buyers, columns: suppliers); the rest is labour
SHARES = np.array([
    #  farm  energ chips metal fact  trans serv  retail
    [0.10, 0.10, 0.00, 0.02, 0.08, 0.05, 0.05, 0.00],   # farms
    [0.00, 0.20, 0.02, 0.08, 0.05, 0.05, 0.05, 0.00],   # energy
    [0.00, 0.10, 0.10, 0.10, 0.05, 0.03, 0.10, 0.00],   # chips
    [0.00, 0.25, 0.00, 0.15, 0.05, 0.08, 0.05, 0.00],   # metals
    [0.02, 0.08, 0.10, 0.20, 0.10, 0.06, 0.08, 0.00],   # factories
    [0.00, 0.25, 0.02, 0.02, 0.08, 0.05, 0.08, 0.00],   # transport
    [0.01, 0.05, 0.05, 0.00, 0.02, 0.03, 0.15, 0.01],   # services
    [0.15, 0.05, 0.01, 0.00, 0.20, 0.10, 0.10, 0.05],   # retail
])
CONSUMPTION = np.array([0.05, 0.05, 0.02, 0.00, 0.10, 0.05, 0.45, 0.28])


def island_table() -> dict:
    return {"sectors": list(SECTORS), "shares": SHARES.tolist(), "consumption": CONSUMPTION.tolist(),
            "labour_share": (1 - SHARES.sum(1)).tolist()}


def leontief(max_len: int = 6) -> dict:
    """Domar weights lambda' = beta' (I - Omega)^(-1): each sector's sales over GDP, where Omega is the matrix of
    input shares and beta the consumption shares.  The inverse is the sum of Omega's powers, the paths of length k
    through the supply chain; the partial sums show how much of each weight arrives through longer chains."""
    n = len(SECTORS)
    L = np.linalg.inv(np.eye(n) - SHARES)
    lam = CONSUMPTION @ L
    partial, P, acc = [], np.eye(n), np.zeros(n)
    for k in range(max_len + 1):
        acc = acc + CONSUMPTION @ P
        partial.append(acc.copy())
        P = P @ SHARES
    # upstreamness (Antras et al.): 1 + average number of steps from final use
    sales = lam
    up = np.linalg.solve(np.eye(n) - (SHARES * sales[:, None] / sales[None, :]).T, np.ones(n))
    return {"inverse": L.tolist(), "domar": lam.tolist(), "partial": [p.tolist() for p in partial],
            "sum_domar": float(lam.sum()), "upstreamness": up.tolist()}


def ces_prices(logA, theta: float = 0.5, omega=None, labour=None, tol: float = 1e-13) -> np.ndarray:
    """Unit-cost prices with the wage as numeraire: p_i = (1/A_i) [a_i^(1/theta)... ] in the share form
    p_i^(1 - theta) = A_i^(theta - 1) (l_i + sum_j w_ij p_j^(1 - theta)), with shares at the baseline (all prices 1).
    theta is the elasticity of substitution between a sector's inputs (labour and each intermediate);
    theta = 1 is Cobb-Douglas."""
    Om = SHARES if omega is None else np.asarray(omega)
    lab = (1 - Om.sum(1)) if labour is None else np.asarray(labour)
    A = np.exp(np.asarray(logA, float))
    if abs(theta - 1) < 1e-9:
        # log p = -log A + Om log p
        return np.exp(np.linalg.solve(np.eye(len(A)) - Om, -np.log(A)))
    p = np.ones(len(A))
    for _ in range(20000):
        new = (A ** (theta - 1) * (lab + Om @ p ** (1 - theta))) ** (1 / (1 - theta))
        if np.max(np.abs(new - p)) < tol:
            p = new
            break
        p = new
    return p


def log_gdp(logA, theta: float = 0.5, sigma_c: float = 1.0) -> float:
    """Real GDP with labour the only primary factor (supplied inelastically, wage = 1): log Y = -log P_c, with a
    consumption price index of elasticity sigma_c over the baseline shares."""
    p = ces_prices(logA, theta)
    if abs(sigma_c - 1) < 1e-9:
        return float(-(CONSUMPTION @ np.log(p)))
    return float(-np.log((CONSUMPTION @ p ** (1 - sigma_c)) ** (1 / (1 - sigma_c))))


def gdp_response(sector: str = "energy", shocks=None, thetas=(0.2, 1.0, 1.5)) -> dict:
    """Real GDP's change when one sector's productivity changes by each of ``shocks`` (log points), for several
    elasticities of substitution, against Hulten's first-order prediction: the sector's Domar weight times the
    shock."""
    shocks = np.linspace(-0.6, 0.3, 37) if shocks is None else np.asarray(shocks, float)
    i = SECTORS.index(sector)
    lam = leontief()["domar"][i]
    out = {"shocks": shocks.tolist(), "hulten": (lam * shocks).tolist(), "domar": lam, "sector": sector}
    for th in thetas:
        ys = []
        for s in shocks:
            a = np.zeros(len(SECTORS))
            a[i] = s
            ys.append(log_gdp(a, th))
        out[f"theta_{th:g}"] = ys
    return out


def which_failure(shock: float = -0.5, theta: float = 0.15) -> dict:
    """The Play-it: a productivity loss of ``shock`` log points at one sector at a time, with inputs that are hard to
    substitute (theta); the GDP loss for each, against what its Domar weight alone predicts."""
    lam = np.array(leontief()["domar"])
    rows = []
    for i, s in enumerate(SECTORS):
        a = np.zeros(len(SECTORS))
        a[i] = shock
        rows.append({"sector": s, "domar": float(lam[i]), "hulten": float(lam[i] * shock),
                     "loss": float(log_gdp(a, theta)), "loss_cd": float(log_gdp(a, 1.0))})
    return {"rows": rows, "shock": shock, "theta": theta}


# ---------------------------------------------------------------------------------------------------------------
# granularity and network shape


def granular(ns=(10, 30, 100, 300, 1000, 3000, 10000), zipf: float = 1.0, sigma: float = 0.12, seed: int = 63) -> dict:
    """Aggregate volatility from independent firm shocks of standard deviation sigma: GDP growth is the sales-
    weighted average, so its standard deviation is sigma x sqrt(sum of squared sales shares).  With equal firms it
    falls as 1/sqrt(n); with Zipf-sized firms it falls far more slowly (Gabaix).  Also a star network of sectors
    (one supplier to all) against a ring (each supplies the next), with Domar weights from the Leontief inverse."""
    rng = np.random.default_rng(seed)
    rows = []
    for n in ns:
        sizes = (np.arange(1, n + 1)) ** (-1.0 / zipf)
        sh = sizes / sizes.sum()
        rows.append({"n": n, "equal": float(sigma / np.sqrt(n)), "zipf": float(sigma * np.sqrt((sh ** 2).sum())),
                     "top10_share": float(sh[:10].sum())})
    # simulate one Zipf economy's GDP growth
    n = 1000
    sizes = np.arange(1, n + 1) ** (-1.0 / zipf)
    sh = sizes / sizes.sum()
    g = rng.normal(0, sigma, (40, n)) @ sh
    ge = rng.normal(0, sigma, (40, n)).mean(1)
    k, a = 20, 0.5
    star = np.zeros((k, k))
    star[1:, 0] = a
    ring = np.zeros((k, k))
    for i in range(k):
        ring[i, (i + 1) % k] = a
    beta = np.full(k, 1 / k)
    out_shapes = {}
    for name, Om in (("star", star), ("ring", ring)):
        lam = beta @ np.linalg.inv(np.eye(k) - Om)
        out_shapes[name] = {"domar": lam.tolist(), "vol": float(sigma * np.sqrt((lam ** 2).sum()))}
    return {"rows": rows, "sim_zipf": g.tolist(), "sim_equal": ge.tolist(), "shapes": out_shapes, "sigma": sigma}


# ---------------------------------------------------------------------------------------------------------------
# the O-ring


def oring(n: int = 400, team: int = 4, seed: int = 63) -> dict:
    """Kremer's O-ring: a team's output is proportional to the product of its members' chances of not making a
    mistake, q_1 x ... x q_n.  Because each worker's skill multiplies the others', sorting by skill (the best with the
    best) gives more total output than mixing; wages rise more than proportionally with skill."""
    rng = np.random.default_rng(seed)
    q = np.clip(rng.beta(18, 2, n), 0.5, 0.999)
    srt = np.sort(q)[::-1].reshape(-1, team)
    mix = rng.permutation(q).reshape(-1, team)
    out_sorted = float(np.prod(srt, axis=1).sum())
    out_mixed = float(np.prod(mix, axis=1).sum())
    # in a sorted equilibrium the wage of skill q is proportional to q^team (Kremer's result for equal teams)
    grid = np.linspace(0.8, 0.999, 50)
    return {"sorted": out_sorted, "mixed": out_mixed, "gain": out_sorted / out_mixed - 1, "q": q.tolist(),
            "grid": grid.tolist(), "wage": (grid ** team).tolist(), "team": team,
            "one_weak": float(0.99 ** (team - 1) * 0.6 / 0.99 ** team)}


# ---------------------------------------------------------------------------------------------------------------
# financial networks


def clearing(L, assets, tol: float = 1e-12) -> dict:
    """The Eisenberg-Noe clearing vector: bank i owes L_ij to bank j; it pays min(total owed, outside assets plus what
    it receives), shared pro rata among its creditors.  Solved by iterating the monotone map from full payment."""
    L = np.asarray(L, float)
    pbar = L.sum(1)
    Pi = np.divide(L, pbar[:, None], out=np.zeros_like(L), where=pbar[:, None] > 0)
    p = pbar.copy()
    for _ in range(10000):
        new = np.minimum(pbar, np.maximum(np.asarray(assets, float) + Pi.T @ p, 0.0))
        if np.max(np.abs(new - p)) < tol:
            p = new
            break
        p = new
    return {"payments": p.tolist(), "owed": pbar.tolist(), "defaults": (p < pbar - 1e-9).tolist(),
            "shortfall": float((pbar - p).sum())}


def contagion(n: int = 10, owed: float = 10.0, buffer: float = 1.0, shocks=None) -> dict:
    """Acemoglu, Ozdaglar and Tahbaz-Salehi's comparison: n banks each owe ``owed`` in total, either all to the next
    bank (a ring) or spread evenly over all the others (complete); each holds outside assets of owed + buffer.  Bank 0
    loses a shock; count the defaults and the total shortfall.  Small shocks: the complete network absorbs them.
    Large shocks: it spreads them to everyone."""
    shocks = np.linspace(0, 40, 41) if shocks is None else np.asarray(shocks, float)
    ring = np.zeros((n, n))
    for i in range(n):
        ring[i, (i + 1) % n] = owed
    comp = np.full((n, n), owed / (n - 1))
    np.fill_diagonal(comp, 0)
    out = {"shocks": shocks.tolist()}
    for name, L in (("ring", ring), ("complete", comp)):
        d, s = [], []
        for x in shocks:
            a = np.full(n, buffer)
            a[0] -= x
            r = clearing(L, a)
            d.append(int(sum(r["defaults"])))
            s.append(r["shortfall"])
        out[name] = {"defaults": d, "shortfall": s}
    return out


# ---------------------------------------------------------------------------------------------------------------
# social networks


def weak_ties(strength=None) -> dict:
    """Granovetter's argument as two curves: the chance that a contact knows of a job you have not heard of falls with
    the tie's strength (strong ties move in your circles); the chance they pass it on rises with it.  Their product,
    the value of a tie for finding work, peaks at moderately weak ties."""
    s = np.linspace(0, 1, 101) if strength is None else np.asarray(strength, float)
    novel = 0.8 * np.exp(-2.5 * s)
    passes = 0.15 + 0.85 * s
    value = novel * passes
    return {"strength": s.tolist(), "novel": novel.tolist(), "passes": passes.tolist(), "value": value.tolist(),
            "peak": float(s[int(np.argmax(value))])}


def village(n: int = 200, k: int = 6, p_rewire: float = 0.08, seed: int = 63) -> np.ndarray:
    """A village network: households on a ring of neighbourhoods, each linked to its k nearest, with a few long links
    (Watts-Strogatz), plus a handful of well-connected households."""
    rng = np.random.default_rng(seed)
    A = np.zeros((n, n), bool)
    for i in range(n):
        for d in range(1, k // 2 + 1):
            j = (i + d) % n
            if rng.random() < p_rewire:
                j = int(rng.integers(n))
            if j != i:
                A[i, j] = A[j, i] = True
    hubs = rng.choice(n, 6, replace=False)
    for h in hubs:
        for j in rng.choice(n, 18, replace=False):
            if j != h:
                A[h, j] = A[j, h] = True
    return A


def diffusion(n: int = 200, seeds: int = 5, q: float = 0.12, rounds: int = 8, reps: int = 300, seed: int = 63) -> dict:
    """Information about a loan product enters a village through ``seeds`` households and passes each round from every
    informed household to each neighbour with probability q.  Seeding by eigenvector centrality, at random, and at the
    least central households: the share informed after each round (after Banerjee, Chandrasekhar, Duflo and
    Jackson)."""
    rng = np.random.default_rng(seed)
    A = village(n, seed=seed)
    w, v = np.linalg.eigh(A.astype(float))
    cent = np.abs(v[:, -1])
    deg = A.sum(1)
    rules = {"most central": np.argsort(-cent)[:seeds], "at random": None,
             "least central": np.argsort(cent)[:seeds]}
    out = {"rounds": list(range(rounds + 1)), "degree_mean": float(deg.mean())}
    for name, pick in rules.items():
        curves = np.zeros(rounds + 1)
        for _ in range(reps):
            informed = np.zeros(n, bool)
            informed[pick if pick is not None else rng.choice(n, seeds, replace=False)] = True
            curves[0] += informed.mean()
            for t in range(1, rounds + 1):
                tries = A[informed].sum(0)
                p_hear = 1 - (1 - q) ** tries
                informed = informed | (rng.random(n) < p_hear)
                curves[t] += informed.mean()
        out[name] = (curves / reps).tolist()
    return out


def key_player(delta: float = 0.2) -> dict:
    """Ballester, Calvo-Armengol and Zenou: each player's effort x = a + delta x (sum of neighbours' efforts), so
    x = (I - delta G)^(-1) a, the Bonacich centrality.  The key player is the one whose removal cuts total effort the
    most.  Here a hub with seven loosely attached followers (the most links) is joined to a tight clique of five: the
    key player sits in the clique."""
    n = 13
    G = np.zeros((n, n))
    for j in range(1, 8):
        G[0, j] = G[j, 0] = 1
    clique = range(8, 13)
    for i, j in itertools.combinations(clique, 2):
        G[i, j] = G[j, i] = 1
    G[0, 8] = G[8, 0] = 1
    a = np.ones(n)

    def total(keep):
        idx = np.flatnonzero(keep)
        sub = G[np.ix_(idx, idx)]
        return float(np.linalg.solve(np.eye(len(idx)) - delta * sub, a[idx]).sum())
    keep = np.ones(n, bool)
    base = total(keep)
    drop = []
    for i in range(n):
        k2 = keep.copy()
        k2[i] = False
        drop.append(base - total(k2))
    x = np.linalg.solve(np.eye(n) - delta * G, a)
    return {"G": G.tolist(), "effort": x.tolist(), "degree": G.sum(1).tolist(), "drop": drop, "total": base,
            "key": int(np.argmax(drop)), "most_links": int(np.argmax(G.sum(1))), "delta": delta}


def formation(n: int = 4, delta: float = 0.6, costs=None) -> dict:
    """Jackson and Wolinsky's connections model with n players: each gets delta^d from every player at distance d and
    pays c per own link.  For each link cost, the efficient networks (highest total payoff) and whether the star and
    the complete network are pairwise stable."""
    costs = np.linspace(0.05, 1.2, 24) if costs is None else np.asarray(costs, float)
    pairs = list(itertools.combinations(range(n), 2))

    def payoffs(edges, c):
        A = np.zeros((n, n), bool)
        for i, j in edges:
            A[i, j] = A[j, i] = True
        D = np.full((n, n), np.inf)
        for s in range(n):
            D[s, s] = 0
            frontier, d = [s], 0
            while frontier:
                d += 1
                nxt = []
                for u in frontier:
                    for w_ in np.flatnonzero(A[u]):
                        if D[s, w_] == np.inf:
                            D[s, w_] = d
                            nxt.append(w_)
                frontier = nxt
        benefit = np.where(np.isfinite(D) & (D > 0), delta ** np.where(np.isfinite(D), D, 0), 0.0).sum(1)
        return benefit - c * A.sum(1)

    def stable(edges, c, eps=1e-12):
        """Pairwise stability: nobody gains by cutting a link of their own, and no absent link would make one end
        strictly better off without making the other worse off."""
        u = payoffs(list(edges), c)
        for e in edges:
            u2 = payoffs([x for x in edges if x != e], c)
            if u2[e[0]] > u[e[0]] + eps or u2[e[1]] > u[e[1]] + eps:
                return False
        for e in pairs:
            if e in set(edges):
                continue
            u2 = payoffs(list(edges) + [e], c)
            di, dj = u2[e[0]] - u[e[0]], u2[e[1]] - u[e[1]]
            if (di > eps and dj >= -eps) or (dj > eps and di >= -eps):
                return False
        return True
    star = [(0, j) for j in range(1, n)]
    complete = pairs
    rows = []
    for c in costs:
        best, best_val = None, -np.inf
        for r in range(len(pairs) + 1):
            for edges in itertools.combinations(pairs, r):
                v = payoffs(list(edges), c).sum()
                if v > best_val + 1e-12:
                    best, best_val = list(edges), v
        rows.append({"c": float(c), "efficient_links": len(best), "efficient_value": float(best_val),
                     "star_value": float(payoffs(star, c).sum()), "complete_value": float(payoffs(complete, c).sum()),
                     "star_stable": stable(star, c), "complete_stable": stable(complete, c),
                     "empty_value": 0.0})
    return {"rows": rows, "n": n, "delta": delta}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "itertools", "annotations")]
