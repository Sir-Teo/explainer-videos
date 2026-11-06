"""Precompute everything numerical in Part 23 of *Computer Science, Built* ("Optimization").

    python -m videos.cs.cs23.compute              # everything missing
    python -m videos.cs.cs23.compute --force tsp

Results are cached in ``.cache/cs23/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/optim.py`` (tested in tests/test_cs23_optim.py).

Items:
    lp        Chvatal's three-product LP: its polytope, vertices and optimum
    simplex   the simplex walk on it, with the tableau at every pivot
    duality   the dual, a family of bounds, shadow prices, complementary slackness
    kleeminty pivots on Klee-Minty cubes for three rules; the 3D cube; perturbed cubes; random LPs
    ellipsoid a 2D ellipsoid run; steps against the target's size
    interior  the central path of a 2D LP; Newton steps against precision
    tu        bipartite incidence matrices are totally unimodular; the triangle is not
    ip        knapsack by branch and bound (a small tree, and node counts); the FPTAS
    approx    vertex cover by matching and by LP rounding; greedy set cover
    tsp       Held-Karp, double tree, Christofides, nearest neighbour and 2-opt
    gw        Goemans-Williamson against exact MAX-CUT
    online    ski rental; paging policies on the Job's memory trace (Part 9)
    mw        multiplicative weights: regret against T, and a zero-sum game
    convex    gradient descent against Newton's method
    frontier  the Hirsch bound on random 3D polytopes
"""

from __future__ import annotations

import math
import random
import time
from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.algo import optim as O

CACHE = Cache("cs23")
load = CACHE.load

C3 = [5, 4, 3]
A3 = [[2, 3, 1], [4, 1, 2], [3, 4, 2]]
B3 = [5, 11, 8]


def compute_lp() -> dict:
    V = O.vertices_3d(A3, B3)
    F = O.hull_faces_3d(V)
    vals = [sum(c * x for c, x in zip(C3, v)) for v in V]
    k = int(np.argmax(vals))
    # a transportation problem (Kantorovich, Hitchcock 1941): two plants, three stores, cost per unit shipped
    from scipy.optimize import linprog
    sup, dem = [30, 40], [20, 25, 25]
    cost = [[4, 6, 9], [5, 3, 8]]
    cvec = [cost[i][j] for i in range(2) for j in range(3)]
    A_ub = [[1 if k // 3 == i else 0 for k in range(6)] for i in range(2)]
    A_eq = [[1 if k % 3 == j else 0 for k in range(6)] for j in range(3)]
    r = linprog(cvec, A_ub=A_ub, b_ub=sup, A_eq=A_eq, b_eq=dem, method="highs")
    ship = [[round(float(r.x[3 * i + j]), 6) for j in range(3)] for i in range(2)]
    naive = sum(min(cost[i][j] for i in range(2)) * dem[j] for j in range(3))  # ignores the plants' capacity
    transport = {"supply": sup, "demand": dem, "cost": cost, "ship": ship, "total": round(float(r.fun), 6),
                 "naive": naive}
    return {"c": C3, "A": A3, "b": B3, "vertices": V, "faces": F, "values": vals, "opt": V[k], "opt_value": vals[k],
            "transport": transport}


def compute_simplex() -> dict:
    out = {}
    for rule in ("dantzig", "bland"):
        r = O.simplex(C3, A3, B3, rule=rule, exact=True)
        out[rule] = {"path": r["path"], "pivots": r["pivots"], "value": r["value"]}
    # tableaux after each pivot, as strings of exact fractions, for Dantzig
    m, n = len(A3), len(C3)
    T = [[Fraction(v) for v in A3[i]] + [Fraction(int(j == i)) for j in range(m)] + [Fraction(B3[i])] for i in range(m)]
    z = [Fraction(-v) for v in C3] + [Fraction(0)] * (m + 1)
    basis = [n + i for i in range(m)]
    tabs = []

    def snap(e=None, r=None):
        tabs.append({"T": [[str(v) for v in row] for row in T], "z": [str(v) for v in z], "basis": list(basis),
                     "enter": e, "leave_row": r})
    snap()
    while True:
        cand = [j for j in range(n + m) if z[j] < 0]
        if not cand:
            break
        e = min(cand, key=lambda j: (z[j], j))
        rows = [(T[i][-1] / T[i][e], basis[i], i) for i in range(m) if T[i][e] > 0]
        _, _, r = min(rows)
        tabs[-1]["enter"], tabs[-1]["leave_row"] = e, r
        pv = T[r][e]
        T[r] = [v / pv for v in T[r]]
        for i in range(m):
            if i != r and T[i][e] != 0:
                f = T[i][e]
                T[i] = [a - f * b for a, b in zip(T[i], T[r])]
        f = z[e]
        z = [a - f * b for a, b in zip(z, T[r])]
        basis[r] = e
        snap()
    out["tableaux"] = tabs
    return out


def compute_duality() -> dict:
    r = O.simplex(C3, A3, B3, exact=True)
    y = r["duals"]
    # a family of dual-feasible multipliers and the bounds they prove
    fam = []
    for yy in ([3, 0, 0], [0, 0, 5 / 3], [0, 1.25, 0], [1, 0, 1]):
        feas = all(sum(A3[i][j] * yy[i] for i in range(3)) >= C3[j] - 1e-12 for j in range(3))
        fam.append({"y": yy, "bound": sum(a * b for a, b in zip(yy, B3)), "feasible": feas})
    # shadow prices: raise each b by 1, re-solve
    shadow = []
    for i in range(3):
        b2 = list(B3)
        b2[i] += 1
        shadow.append(O.simplex(C3, A3, b2, exact=True)["value"] - r["value"])
    x = r["x"]
    slack = [B3[i] - sum(A3[i][j] * x[j] for j in range(3)) for i in range(3)]
    reduced = [sum(A3[i][j] * y[i] for i in range(3)) - C3[j] for j in range(3)]
    return {"x": x, "value": r["value"], "y": y, "family": fam, "shadow": shadow, "slack": slack, "reduced": reduced}


def compute_kleeminty() -> dict:
    rows = []
    for n in range(2, 13):
        c, A, b = O.klee_minty(n)
        row = {"n": n}
        for rule in ("dantzig", "bland", "steepest"):
            row[rule] = O.simplex(c, A, b, rule=rule, exact=n <= 9)["pivots"]
        rows.append(row)
    # the 3D cube, squashed for drawing: eps x_{j-1} <= x_j <= 1 - eps x_{j-1}
    c, A, b = O.klee_minty(3)
    V = O.vertices_3d(A, b)
    path = O.simplex(c, A, b, exact=True)["path"]
    # perturbation: multiply every entry of A by (1 + sigma g), g standard normal
    rng = np.random.default_rng(1)
    pert = []
    n = 10
    c, A, b = O.klee_minty(n)
    for sigma in (0.0, 1e-4, 1e-3, 1e-2, 1e-1, 0.3):
        ps = []
        for _ in range(20 if sigma else 1):
            Ap = (np.array(A, float) * (1 + sigma * rng.standard_normal((n, n)))).tolist()
            r = O.simplex(c, Ap, b)
            ps.append(r["pivots"])
        pert.append({"sigma": sigma, "mean": float(np.mean(ps)), "max": int(max(ps))})
    # random LPs
    rnd = []
    prng = random.Random(2)
    for n in (5, 10, 20, 40, 80):
        ps = []
        for _ in range(20):
            c2, A2, b2 = O.random_lp(n, 2 * n, prng)
            ps.append(O.simplex(c2, A2, b2)["pivots"])
        rnd.append({"n": n, "m": 2 * n, "mean": float(np.mean(ps)), "max": int(max(ps))})
    return {"rows": rows, "cube_vertices": V, "cube_faces": O.hull_faces_3d(V), "cube_path": path, "perturbed": pert,
            "perturbed_n": 10, "random": rnd}


def compute_ellipsoid() -> dict:
    A = np.array([[1.0, 1.0], [-1.0, 2.0], [-2.0, -1.0], [1.0, -2.0]])
    target = np.array([2.2, 1.5])
    w = 0.25
    b = A @ target + w * np.linalg.norm(A, axis=1)
    b = np.array([A[k] @ target + w * np.linalg.norm(A[k]) for k in range(4)])
    x, steps, trail = O.ellipsoid_feasible(A, b, R=6.0, log=True)
    tr = [{"c": t[0].tolist(), "P": t[1].tolist()} for t in trail]
    rows = []
    for w2 in (1.0, 0.1, 0.01, 1e-3, 1e-4, 1e-5, 1e-6):
        b2 = np.array([A[k] @ target + w2 * np.linalg.norm(A[k]) for k in range(4)])
        _, s2, _ = O.ellipsoid_feasible(A, b2, R=6.0)
        rows.append({"width": w2, "steps": s2})
    shrink = math.exp(-1 / (2 * 3))
    return {"A": A.tolist(), "b": b.tolist(), "target": target.tolist(), "x": x.tolist(), "steps": steps, "trail": tr,
            "rows": rows, "shrink2d": shrink}


def compute_interior() -> dict:
    A = [[1.0, 2.0], [3.0, 1.0], [-1.0, 0.0], [0.0, -1.0], [1.0, -1.0], [-1.0, 3.0]]
    b = [8.0, 9.0, 0.0, 0.0, 2.0, 9.0]
    c = [1.0, 1.0]
    ts = [0.02 * 1.5 ** k for k in range(36)]
    path, total = O.barrier_path(c, A, b, ts=ts, x0=[0.5, 0.5])
    from scipy.optimize import linprog
    r = linprog([-1, -1], A_ub=A, b_ub=b, method="highs")
    pts = [{"t": t, "x": x.tolist(), "steps": s, "gap": len(b) / t} for t, x, s in path]
    return {"A": A, "b": b, "c": c, "path": pts, "total_newton": total, "opt": r.x.tolist(), "opt_value": -r.fun}


def compute_tu() -> dict:
    from scipy.optimize import linprog
    edges = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 2)]
    M = O.bipartite_incidence(edges, 3, 3)
    tu, _ = O.is_totally_unimodular(M)
    tri = np.array([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
    tu_tri, wit = O.is_totally_unimodular(tri)
    r = linprog(-np.ones(3), A_ub=tri, b_ub=np.ones(3), bounds=[(0, 1)] * 3, method="highs")
    # random bipartite graphs with random weights: is the matching LP's optimum integral?
    rng = np.random.default_rng(3)
    frac_bip, frac_gen = 0, 0
    for _ in range(100):
        nl = nr = 8
        E = [(i, j) for i in range(nl) for j in range(nr) if rng.random() < 0.4]
        Mb = O.bipartite_incidence(E, nl, nr)
        wv = rng.integers(1, 20, len(E))
        rr = linprog(-wv, A_ub=Mb, b_ub=np.ones(nl + nr), bounds=[(0, 1)] * len(E), method="highs-ds")
        frac_bip += int(np.any(np.abs(rr.x - np.round(rr.x)) > 1e-7))
        n = 16
        Eg = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]
        Mg = np.zeros((n, len(Eg)), int)
        for k, (u, v) in enumerate(Eg):
            Mg[u, k] = Mg[v, k] = 1
        wg = rng.integers(1, 20, len(Eg))
        rg = linprog(-wg, A_ub=Mg, b_ub=np.ones(n), bounds=[(0, 1)] * len(Eg), method="highs-ds")
        frac_gen += int(np.any(np.abs(rg.x - np.round(rg.x)) > 1e-7))
    return {"edges": edges, "M": M.tolist(), "tu": tu, "tri": tri.tolist(), "tu_tri": tu_tri,
            "tri_witness_det": wit[2] if wit else None, "tri_lp": r.x.tolist(), "tri_lp_value": -r.fun,
            "frac_bipartite": frac_bip, "frac_general": frac_gen, "trials": 100}


def compute_ip() -> dict:
    rng = random.Random(11)
    vals = [rng.randint(10, 60) for _ in range(8)]
    wts = [rng.randint(5, 40) for _ in range(8)]
    cap = 80
    best, x, nodes, tree = O.branch_and_bound_knapsack(vals, wts, cap, log=True)
    root, _ = O.knapsack_lp_bound(vals, wts, cap, {})
    rows = []
    for n in (20, 40, 80, 160):
        ns = []
        gaps = []
        for _ in range(10):
            v = [rng.randint(10, 100) for _ in range(n)]
            w = [rng.randint(10, 100) for _ in range(n)]
            cp = sum(w) // 3
            b, _, nd, _ = O.branch_and_bound_knapsack(v, w, cp)
            lb, _ = O.knapsack_lp_bound(v, w, cp, {})
            ns.append(nd)
            gaps.append(lb / b - 1)
        rows.append({"n": n, "nodes_mean": float(np.mean(ns)), "nodes_max": int(max(ns)), "subsets": 2 ** n,
                     "gap": float(np.mean(gaps))})
    # FPTAS on a strongly correlated instance (value = weight + 100), the hard kind for knapsack heuristics
    frng = random.Random(5)
    w = [frng.randint(100, 1000) for _ in range(20)]
    v = [x + 100 for x in w]
    cp = sum(w) // 2
    t0 = time.perf_counter()
    opt = O.knapsack_dp(v, w, cp)
    t_dp = time.perf_counter() - t0
    fp = []
    for eps in (0.9, 0.5, 0.2, 0.1, 0.05, 0.02):
        t0 = time.perf_counter()
        val, size = O.knapsack_fptas(v, w, cp, eps)
        fp.append({"eps": eps, "ratio": val / opt, "table": size, "seconds": time.perf_counter() - t0})
    return {"vals": vals, "wts": wts, "cap": cap, "best": best, "x": x, "nodes": nodes, "tree": tree, "root": root,
            "rows": rows, "fptas": fp, "fptas_n": 20, "dp_seconds": t_dp, "dp_cap": cp, "fptas_opt": opt}


def compute_approx() -> dict:
    rng = random.Random(21)
    vc = []
    for _ in range(100):
        n = 16
        E = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.25]
        if not E:
            continue
        opt, _ = O.vertex_cover_exact(n, E)
        mt = len(O.vertex_cover_matching(n, E, seed=rng.randint(0, 999)))
        lp, xx, cov = O.vertex_cover_lp(n, E)
        vc.append({"opt": opt, "matching": mt, "lp": lp, "rounded": len(cov),
                   "half": int(np.sum(np.abs(xx - 0.5) < 1e-6))})
    # a small drawing instance
    n = 9
    E = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3), (5, 6), (6, 7), (7, 8), (8, 6), (1, 4), (7, 4)]
    opt, sopt = O.vertex_cover_exact(n, E)
    mt = O.vertex_cover_matching(n, E, seed=3)
    lp, xx, cov = O.vertex_cover_lp(n, E)
    sc = []
    for k in range(2, 8):
        U, S, o = O.harmonic_bad_set_cover(k)
        g = O.set_cover_greedy(U, S)
        sc.append({"k": k, "n": len(U), "greedy": len(g), "opt": o})
    rs = []
    for _ in range(60):
        U = list(range(30))
        S = [set(rng.sample(U, rng.randint(2, 8))) for _ in range(18)]
        S.append(set(U) - set().union(*S) or {0})
        if set().union(*S) != set(U):
            continue
        g = O.set_cover_greedy(U, S)
        e = O.set_cover_exact(U, S)
        rs.append({"greedy": len(g), "opt": len(e), "maxsize": max(len(s) for s in S)})
    return {"vc": vc, "draw": {"n": n, "E": E, "opt": opt, "opt_set": sorted(sopt), "matching": sorted(mt),
                               "lp": lp, "x": xx.tolist(), "rounded": sorted(cov)},
            "setcover": sc, "random_setcover": rs}


def compute_tsp() -> dict:
    rng = random.Random(34)
    P = [(round(rng.uniform(0, 10), 3), round(rng.uniform(0, 6), 3)) for _ in range(13)]
    opt, tour = O.held_karp(P)
    dt, mst = O.double_tree(P)
    ch, mst2, M, odd = O.christofides(P)
    nn = O.nearest_neighbour_tour(P)
    to, mv = O.two_opt(P, nn)
    draw = {"P": P, "opt": opt, "tour": tour, "double_tree": dt, "mst": mst, "christofides": ch, "matching": list(M),
            "odd": odd, "nn": nn, "two_opt": to, "lengths": {"opt": opt, "double_tree": O.tour_length(P, dt),
                                                            "christofides": O.tour_length(P, ch),
                                                            "nn": O.tour_length(P, nn), "two_opt": O.tour_length(P, to)}}
    ratios = {"double_tree": [], "christofides": [], "nn": [], "two_opt": []}
    for _ in range(40):
        Q = [(rng.random(), rng.random()) for _ in range(12)]
        o, _ = O.held_karp(Q)
        ratios["double_tree"].append(O.tour_length(Q, O.double_tree(Q)[0]) / o)
        ratios["christofides"].append(O.tour_length(Q, O.christofides(Q)[0]) / o)
        n0 = O.nearest_neighbour_tour(Q)
        ratios["nn"].append(O.tour_length(Q, n0) / o)
        ratios["two_opt"].append(O.tour_length(Q, O.two_opt(Q, n0)[0]) / o)
    summ = {k: {"mean": float(np.mean(v)), "max": float(max(v))} for k, v in ratios.items()}
    big = []
    for n in (100, 300):
        Q = [(rng.random(), rng.random()) for _ in range(n)]
        n0 = O.nearest_neighbour_tour(Q)
        t0 = time.perf_counter()
        t2, mvs = O.two_opt(Q, n0)
        big.append({"n": n, "nn": O.tour_length(Q, n0), "two_opt": O.tour_length(Q, t2), "moves": mvs,
                    "seconds": time.perf_counter() - t0, "bhh": 0.7124 * math.sqrt(n)})
    t0 = time.perf_counter()
    O.held_karp([(rng.random(), rng.random()) for _ in range(15)])
    t_hk15 = time.perf_counter() - t0
    return {"draw": draw, "summary": summ, "trials": 40, "big": big, "t_hk15": t_hk15}


def compute_gw() -> dict:
    rng = random.Random(41)
    n = 12
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.35]
    ex, mask = O.maxcut_exact(n, E)
    V3, sdp3 = O.gw_vectors(n, E, dim=3, iters=4000)
    V, sdp = O.gw_vectors(n, E)
    rr = O.gw_round(V, E, trials=500)
    rows = []
    for _ in range(30):
        m = 16
        Eg = [(i, j) for i in range(m) for j in range(i + 1, m) if rng.random() < 0.4]
        e2, _ = O.maxcut_exact(m, Eg)
        Vg, s2 = O.gw_vectors(m, Eg)
        r2 = O.gw_round(Vg, Eg, trials=200)
        rand = [sum(1 for u, v in Eg if rng.random() < 0.5) for _ in range(200)]
        rows.append({"exact": e2, "sdp": s2, "gw_mean": float(np.mean(r2)), "gw_best": int(max(r2)),
                     "random_mean": float(np.mean(rand)), "edges": len(Eg)})
    a, th = O.gw_alpha()
    return {"n": n, "E": E, "exact": ex, "V3": V3.tolist(), "sdp3": sdp3, "sdp": sdp, "rounds": rr, "rows": rows,
            "alpha": a, "theta": th}


def compute_online() -> dict:
    B = 10
    det = [{"days": d, "cost": O.ski_rental(B, d), "opt": min(d, B)} for d in range(1, 31)]
    rng = random.Random(51)
    rnd = []
    for d in range(1, 31):
        cs = [O.ski_rental(B, d, "random", rng) for _ in range(4000)]
        rnd.append({"days": d, "cost": float(np.mean(cs)), "opt": min(d, B)})
    from videos.cs.cs9.compute import chapter_trace
    t = chapter_trace()
    pages = (t.addr // 64).tolist()          # 64-byte lines as 'pages': a small cache of k lines
    distinct = len(set(pages))
    rows = []
    for k in (8, 16, 32, 64, 96):
        row = {"k": k}
        for pol in ("lru", "fifo", "marking", "random", "opt"):
            row[pol] = O.paging(pages, k, pol, rng=rng)
        rows.append(row)
    adv = []
    for k in (4, 8, 16):
        tr = list(range(k + 1)) * 200
        adv.append({"k": k, "requests": len(tr), "lru": O.paging(tr, k, "lru"), "opt": O.paging(tr, k, "opt"),
                    "marking": O.paging(tr, k, "marking", rng=rng)})
    return {"B": B, "det": det, "rnd": rnd, "requests": len(pages), "distinct": distinct, "rows": rows, "adv": adv,
            "e_ratio": math.e / (math.e - 1)}


def compute_mw() -> dict:
    rng = np.random.default_rng(61)
    n = 10
    T = 20000
    p = np.full(n, 0.5)
    p[3] = 0.45
    L = (rng.random((T, n)) < p).astype(float)
    rows = []
    for TT in (100, 300, 1000, 3000, 10000, 20000):
        eta = math.sqrt(8 * math.log(n) / TT)
        a, best, hist = O.hedge(L[:TT], eta)
        rows.append({"T": TT, "regret": a - best, "bound": math.sqrt(TT * math.log(n) / 2)})
    a, best, hist = O.hedge(L[:3000], math.sqrt(8 * math.log(n) / 3000))
    weights = hist[::30].tolist()
    M = np.array([[0.5, 1, 0], [0, 0.5, 1], [1, 0, 0.5]])
    M2 = np.array([[0.6, 0.2, 0.8], [0.3, 0.7, 0.4], [0.9, 0.1, 0.5]])
    from scipy.optimize import linprog
    # exact value of M2: max v s.t. p M2 >= v
    r = linprog([0, 0, 0, -1], A_ub=np.c_[-M2.T, np.ones(3)], b_ub=np.zeros(3), A_eq=[[1, 1, 1, 0]], b_eq=[1],
                bounds=[(0, 1)] * 3 + [(None, None)], method="highs")
    game = []
    for TT in (10, 100, 1000, 10000):
        lo, hi, pp = O.mw_zero_sum(M2, TT)
        game.append({"T": TT, "lo": lo, "hi": hi})
    return {"n": n, "rows": rows, "weights": weights, "best": 3, "game": game, "game_value": -r.fun,
            "game_p": r.x[:3].tolist(), "M": M2.tolist(), "rps": M.tolist()}


def compute_convex() -> dict:
    # Boyd and Vandenberghe's example 9.20, with the second coordinate stretched by 4 to make it ill-conditioned
    Aa = np.array([[1, 0.75], [1, -0.75], [-1, 0]])

    def f(x):
        return math.log(sum(math.exp(a @ x - 0.1) for a in Aa))

    def grad(x):
        e = np.array([math.exp(a @ x - 0.1) for a in Aa])
        s = e.sum()
        return Aa.T @ e / s, Aa, e / s

    def hess(x):
        g, Aa, p = grad(x)
        return Aa.T @ (np.diag(p) - np.outer(p, p)) @ Aa
    x0 = np.array([-1.5, 3.0])
    gd, x = [x0.tolist()], x0.copy()
    for _ in range(60):
        g, _, _ = grad(x)
        t = 1.0
        while f(x - t * g) > f(x) - 0.3 * t * g @ g:
            t *= 0.7
        x = x - t * g
        gd.append(x.tolist())
    nt, x = [x0.tolist()], x0.copy()
    for _ in range(12):
        g, _, _ = grad(x)
        dx = -np.linalg.solve(hess(x), g)
        t = 1.0
        while f(x + t * dx) > f(x) + 0.3 * t * g @ dx:
            t *= 0.7
        x = x + t * dx
        nt.append(x.tolist())
    fopt = f(nt[-1])
    return {"gd": gd, "newton": nt, "gd_err": [f(p) - fopt for p in gd], "newton_err": [f(p) - fopt for p in nt],
            "xstar": nt[-1], "fstar": fopt}


def compute_frontier() -> dict:
    from scipy.spatial import HalfspaceIntersection
    import networkx as nx
    rng = np.random.default_rng(71)
    rows = []
    for n in (8, 16, 32, 64, 128):
        diams = []
        for _ in range(20):
            N = rng.standard_normal((n, 3))
            N /= np.linalg.norm(N, axis=1, keepdims=True)
            hs = np.c_[N, -np.ones(n)]
            hi = HalfspaceIntersection(hs, np.zeros(3))
            facets = [frozenset(f) for f in hi.dual_facets]
            G = nx.Graph()
            G.add_nodes_from(range(len(facets)))
            for a in range(len(facets)):
                for b in range(a + 1, len(facets)):
                    if len(facets[a] & facets[b]) >= 2:
                        G.add_edge(a, b)
            diams.append(nx.diameter(G))
        rows.append({"n": n, "facets": n, "hirsch": n - 3, "mean_diam": float(np.mean(diams)), "max_diam": int(max(diams))})
    # one polytope to draw: 24 random facets, and a longest shortest path on its graph of vertices
    from scipy.spatial import ConvexHull
    r2 = np.random.default_rng(5)
    N = r2.standard_normal((24, 3))
    N /= np.linalg.norm(N, axis=1, keepdims=True)
    hi = HalfspaceIntersection(np.c_[N, -np.ones(24)], np.zeros(3))
    V = hi.intersections
    facets = [frozenset(f) for f in hi.dual_facets]
    G = nx.Graph()
    G.add_nodes_from(range(len(V)))
    for a in range(len(V)):
        for b in range(a + 1, len(V)):
            if len(facets[a] & facets[b]) >= 2:
                G.add_edge(a, b)
    ecc = nx.eccentricity(G)
    u = max(ecc, key=lambda k: (ecc[k], -k))
    dist = nx.single_source_shortest_path_length(G, u)
    v = max(dist, key=lambda k: (dist[k], -k))
    path = nx.shortest_path(G, u, v)
    faces = [list(map(int, f)) for f in ConvexHull(V).simplices]
    draw = {"V": V.tolist(), "faces": faces, "edges": [list(map(int, e)) for e in G.edges()], "path": path,
            "facets": 24, "vertices": len(V), "diam": len(path) - 1}
    return {"rows": rows, "draw": draw}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
