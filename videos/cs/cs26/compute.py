"""Precompute everything numerical in Part 26 of *Computer Science, Built* ("P versus NP").

    python -m videos.cs.cs26.compute              # everything missing
    python -m videos.cs.cs26.compute --force web

Results are cached in ``.cache/cs26/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/complexity.py`` (tested in tests/test_cs26_complexity.py).

Items:
    hook       finding against checking: a planted 3-colourable graph of 60 vertices, solved by CDCL and checked
    growth     n^2, n^3, 2^n and n! at a microsecond a step
    savitch    CANYIELD by midpoint recursion on paths: calls and depth against BFS's visited set
    tableau    Cook-Levin tableaux for a tiny NTM: variables and clauses against the time bound; a decoded run
    web        one 3-SAT formula through the reductions: independent set, clique, vertex cover, 3-colouring, subset sum
    phase      the random 3-SAT phase transition with our solver: P(satisfiable) and median conflicts by ratio
    solvers    DPLL against CDCL at the threshold, by n
    selfreduce a satisfying assignment found with yes/no questions only
    knapsack   pseudo-polynomial subset-sum DP against the number of digits; meet in the middle for comparison
    pratt      a Pratt certificate for 2^61 - 1, and a factoring certificate
    games      TQBF evaluation and generalized geography: positions evaluated
    famous     Schur numbers S(3) = 13 and S(4) = 44 by our solver; Pythagorean triples colourable up to n
    formulas   the exact De Morgan formula size of all 256 Boolean functions of 3 inputs (parity needs 9)
"""

from __future__ import annotations

import itertools
import math
import random
import statistics
import time

from explainer.ai.cache import Cache
from explainer.cs.algo import complexity as X

CACHE = Cache("cs26")
load = CACHE.load

WEB = [[1, 2, -3], [-1, 3, 4], [-2, -3, -4], [1, -2, 4], [-1, 2, 3]]


def compute_hook() -> dict:
    rng = random.Random(26)
    n, p = 60, 0.12
    col = [rng.randrange(3) for _ in range(n)]
    edges = [(u, v) for u, v in itertools.combinations(range(n), 2) if col[u] != col[v] and rng.random() < p]
    V = list(range(n))
    nv, cl, var = X.coloring_cnf(V, edges, 3)
    t = time.perf_counter()
    model, st = X.cdcl(nv, cl)
    t_find = time.perf_counter() - t
    c = X.decode_coloring(V, model, var, 3)
    t = time.perf_counter()
    for _ in range(1000):
        ok = all(c[u] != c[v] for u, v in edges)
    t_check = (time.perf_counter() - t) / 1000
    brute_years = 3 ** n * t_check / (3600 * 24 * 365.25)
    return {"n": n, "edges": len(edges), "find_s": t_find, "check_s": t_check, "ok": ok,
            "conflicts": st["conflicts"], "decisions": st["decisions"], "brute_years": brute_years,
            "colouring": [c[v] for v in V], "edge_list": edges}


def compute_growth() -> dict:
    rows = []
    for n in (10, 20, 30, 40, 50, 60, 100):
        rows.append({"n": n, "n2": n ** 2 * 1e-6, "n3": n ** 3 * 1e-6, "2n": 2 ** n * 1e-6,
                     "fact": math.factorial(n) * 1e-6})
    return {"rows": rows, "age_universe_s": 13.8e9 * 365.25 * 24 * 3600}


def compute_savitch() -> dict:
    rows = []
    for n in (4, 8, 16):
        adj = {i: {i + 1} for i in range(n - 1)}
        adj[n - 1] = set()
        t = time.perf_counter()
        ok, calls, depth = X.savitch(adj, 0, n - 1, n)
        rows.append({"n": n, "ok": ok, "calls": calls, "depth": depth, "bfs_memory": n,
                     "savitch_memory": depth * 3, "seconds": time.perf_counter() - t})
    return {"rows": rows}


NTM = {"states": ["q", "a"], "start": "q", "accept": "a", "blank": "_", "alphabet": ["0", "1", "_"],
       "delta": {("q", "0"): [("q", "0", 1)], ("q", "1"): [("q", "1", 1), ("a", "1", 1)]}}


def compute_tableau() -> dict:
    rows = []
    for k in range(2, 9):
        w = "0" * (k - 1) + "1"
        T = k + 2
        nv, cl, info = X.cook_levin(NTM, w, T)
        t = time.perf_counter()
        model, st = X.cdcl(nv, cl)
        rows.append({"n": k, "T": T, "vars": nv, "clauses": len(cl), "sat": model is not None,
                     "seconds": time.perf_counter() - t})
    w = "0010"
    nv, cl, info = X.cook_levin(NTM, w, 6)
    model, _ = X.cdcl(nv, cl)
    tab = [[c if isinstance(c, str) else c[0] + c[1] for c in row] for row in X.decode_tableau(model, info)]
    nv2, cl2, _ = X.cook_levin(NTM, "0000", 6)
    no, _ = X.cdcl(nv2, cl2)
    return {"rows": rows, "w": w, "tableau": tab, "legal": info["legal"], "per_position": info["per_position"][:3],
            "rejects_0000": no is None, "vars": nv, "clauses": len(cl)}


def compute_web() -> dict:
    n, cl = 4, WEB
    model, _ = X.cdcl(n, cl)
    sols = [a for a in itertools.product([False, True], repeat=n) if X.check([False] + list(a), cl)]
    verts, edges, lit, k = X.sat_to_is(cl)
    S = X.is_from_model(cl, model)
    clique_edges = X.is_to_clique(verts, edges)
    C = X.is_to_vc(verts, S)
    V3, E3 = X.sat_to_3col(n, cl)
    nv, ccl, var = X.coloring_cnf(V3, E3, 3)
    cm, _ = X.cdcl(nv, ccl)
    colour = X.decode_coloring(V3, cm, var, 3)
    names = {colour["T"]: "T", colour["F"]: "F", colour["B"]: "B"}
    mapped = [False] + [colour[f"x{v}"] == colour["T"] for v in range(1, n + 1)]
    nums, target = X.sat_to_subset_sum(n, cl)
    chosen = X.subset_from_model(n, cl, model, nums)
    # one unsatisfiable formula through the colouring, to show the other direction
    bad = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
    V4, E4 = X.sat_to_3col(2, bad)
    nv4, c4, _ = X.coloring_cnf(V4, E4, 3)
    bm, _ = X.cdcl(nv4, c4)
    return {"n": n, "clauses": cl, "model": model[1:], "solutions": len(sols),
            "is": {"verts": [list(v) for v in verts], "edges": [[list(a), list(b)] for a, b in edges],
                   "lits": [lit[v] for v in verts], "k": k, "chosen": [list(v) for v in S],
                   "clique_edges": len(clique_edges), "cover": len(C)},
            "col": {"vertices": len(V3), "edges": len(E3), "cnf_vars": nv, "cnf_clauses": len(ccl),
                    "colour": {v: names[c] for v, c in colour.items()}, "mapped": mapped[1:],
                    "mapped_ok": X.check(mapped, cl), "bad_colourable": bm is not None},
            "ss": {"nums": {k_: str(v).zfill(n + len(cl)) for k_, v in nums.items()}, "target": str(target),
                   "chosen": chosen, "sum": str(sum(nums[x] for x in chosen))}}


def compute_selfreduce() -> dict:
    """Find an assignment for WEB using only yes/no answers from the solver (n + 1 calls)."""
    n, cl = 4, [list(c) for c in WEB]
    calls = 1
    assert X.cdcl(n, cl)[0] is not None
    steps, fixed = [], []
    for v in range(1, n + 1):
        trial = cl + [[v]] + [[u] if b else [-u] for u, b in fixed]
        calls += 1
        ok = X.cdcl(n, trial)[0] is not None
        b = ok
        steps.append({"var": v, "value": True, "kept": ok})
        fixed.append((v, b))
    model = [False] + [b for _, b in fixed]
    assert X.check(model, cl)
    return {"steps": steps, "model": model[1:], "calls": calls}


def compute_phase() -> dict:
    rng = random.Random(3)
    ratios = [3.0, 3.5, 3.8, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.7, 5.0, 5.5, 6.0]
    out = {}
    for n in (50, 100, 150):
        rows = []
        for r in ratios:
            m = round(r * n)
            sat, confl = 0, []
            trials = 40 if n < 150 else 20
            for _ in range(trials):
                model, st = X.cdcl(n, X.random_ksat(n, m, 3, rng))
                sat += model is not None
                confl.append(st["conflicts"])
            rows.append({"ratio": r, "p_sat": sat / trials, "median_conflicts": statistics.median(confl)})
        out[str(n)] = rows
    return {"ratios": ratios, "by_n": out}


def compute_solvers() -> dict:
    rng = random.Random(9)
    rows = []
    for n in (20, 30, 40, 50, 60):
        m = round(4.26 * n)
        dn, cd, dt, ct = [], [], [], []
        for _ in range(10):
            f = X.random_ksat(n, m, 3, rng)
            t = time.perf_counter()
            try:
                _, nodes = X.dpll(n, f, max_nodes=3_000_000)
            except RuntimeError:
                nodes = None
            dt.append(time.perf_counter() - t)
            t = time.perf_counter()
            _, st = X.cdcl(n, f)
            ct.append(time.perf_counter() - t)
            dn.append(nodes)
            cd.append(st["decisions"] + st["conflicts"])
        rows.append({"n": n, "dpll_nodes": statistics.median([d for d in dn if d is not None] or [0]),
                     "dpll_s": statistics.median(dt), "cdcl_steps": statistics.median(cd),
                     "cdcl_s": statistics.median(ct)})
    return {"rows": rows}


def compute_knapsack() -> dict:
    rng = random.Random(4)
    rows = []
    n = 30
    for digits in (2, 3, 4, 5, 6):
        w = [rng.randrange(10 ** (digits - 1), 10 ** digits) for _ in range(n)]
        target = sum(rng.sample(w, n // 2))
        t = time.perf_counter()
        reach = 1
        for x in w:
            reach |= reach << x
        ok = bool(reach >> target & 1)
        dp_s = time.perf_counter() - t
        rows.append({"digits": digits, "W": target, "dp_s": dp_s, "found": ok})
    # the same instance size by meet in the middle (independent of the number of digits)
    w = [rng.randrange(10 ** 11, 10 ** 12) for _ in range(30)]
    target = sum(rng.sample(w, 15))
    t = time.perf_counter()
    A = {}
    for mask in range(1 << 15):
        s = sum(w[i] for i in range(15) if mask >> i & 1)
        A[s] = mask
    found = False
    for mask in range(1 << 15):
        s = sum(w[15 + i] for i in range(15) if mask >> i & 1)
        if target - s in A:
            found = True
            break
    mitm_s = time.perf_counter() - t
    return {"n": n, "rows": rows, "mitm_digits": 12, "mitm_s": mitm_s, "mitm_found": found}


def compute_pratt() -> dict:
    p = 2 ** 61 - 1
    cert = X.pratt(p)
    ok, checks = X.verify_pratt(cert)

    def flat(c, d=0, out=None):
        out = [] if out is None else out
        out.append({"p": c["p"], "g": c.get("g"), "depth": d})
        for f in c.get("factors", []):
            flat(f, d + 1, out)
        return out

    N = 1000000007 * 998244353
    return {"p": str(p), "ok": ok, "checks": checks, "tree": flat(cert), "factors_of_pm1": X._factor(p - 1),
            "N": str(N), "N_factors": [1000000007, 998244353]}


def compute_games() -> dict:
    rng = random.Random(8)
    rows = []
    for n in (4, 8, 12, 16):
        quants = [("E" if i % 2 == 0 else "A", i + 1) for i in range(n)]
        f = X.random_ksat(n, 2 * n, 3, rng)
        val, nodes = X.tqbf(quants, f)
        rows.append({"n": n, "value": val, "nodes": nodes, "full_tree": 2 ** (n + 1) - 1})
    adj = {0: [1, 2], 1: [3, 4], 2: [4, 5], 3: [6], 4: [6, 7], 5: [7], 6: [0, 8], 7: [8], 8: []}
    win, positions = X.geography(adj, 0)
    grng = random.Random(2)
    grows = []
    for nv in (8, 12, 16, 20):
        g = {v: [u for u in range(nv) if u != v and grng.random() < 0.25] for v in range(nv)}
        t = time.perf_counter()
        w2, pos = X.geography(g, 0)
        grows.append({"n": nv, "first_wins": w2, "positions": pos, "seconds": time.perf_counter() - t})
    return {"tqbf": rows, "geo": {"adj": {str(k): v for k, v in adj.items()}, "first_wins": win,
                                   "positions": positions}, "geo_random": grows}


def compute_famous() -> dict:
    out = {}
    for n, k in ((13, 3), (14, 3), (44, 4)):
        t = time.perf_counter()
        model, st = X.cdcl(*X.schur_cnf(n, k))
        out[f"schur_{n}_{k}"] = {"sat": model is not None, "conflicts": st["conflicts"],
                                 "seconds": time.perf_counter() - t}
        if model is not None and n == 44:
            var = lambda i, c: (i - 1) * k + c + 1  # noqa: E731
            out["schur_44_colouring"] = [next(c for c in range(k) if model[var(i, c)]) for i in range(1, n + 1)]
    t = time.perf_counter()
    model, st = X.cdcl(*X.schur_cnf(45, 4), max_conflicts=200_000)
    out["schur_45_4"] = {"status": st["status"], "conflicts": st["conflicts"], "seconds": time.perf_counter() - t}
    py = []
    for n in (500, 1000, 2000, 3000):
        nv, cl = X.pythagorean_cnf(n)
        t = time.perf_counter()
        model, st = X.cdcl(nv, cl, max_conflicts=200_000)
        py.append({"n": n, "triples": len(cl) // 2, "status": st["status"], "conflicts": st["conflicts"],
                   "seconds": time.perf_counter() - t})
    out["pythagorean"] = py
    out["pythagorean_7825_triples"] = len(X.pythagorean_cnf(7825)[1]) // 2
    return out


def compute_formulas() -> dict:
    """De Morgan formulas over x1..x3: leaves are literals, internal nodes AND / OR; size = number of leaves.
    L(f) by dynamic programming over sizes: a formula of size s splits into sizes a + (s - a)."""
    n = 3
    full = (1 << (1 << n)) - 1
    lits = []
    for i in range(n):
        t = 0
        for x in range(1 << n):
            if x >> i & 1:
                t |= 1 << x
        lits += [t, full ^ t]
    best = {}
    by_size = {1: set(lits)}
    for f in lits:
        best[f] = 1
    s = 1
    while len(best) < (1 << (1 << n)) and s < 12:
        s += 1
        new = set()
        for a in range(1, s // 2 + 1):
            A, B = by_size.get(a, ()), by_size.get(s - a, ())
            for f in A:
                for g in B:
                    for h in (f & g, f | g):
                        if h not in best:
                            new.add(h)
        for h in new:
            best[h] = s
        by_size[s] = new
    # constants: 0 and 1 count as x & ~x and x | ~x (size 2)
    hist = {}
    for f in range(1 << (1 << n)):
        hist.setdefault(best.get(f), 0)
        hist[best.get(f)] += 1
    parity = 0
    for x in range(1 << n):
        if bin(x).count("1") % 2:
            parity |= 1 << x
    majority = sum(1 << x for x in range(1 << n) if bin(x).count("1") >= 2)
    return {"n": n, "hist": {str(k): v for k, v in sorted(hist.items(), key=lambda kv: (kv[0] is None, kv[0]))},
            "parity": best.get(parity), "majority": best.get(majority), "max": max(best.values()),
            "functions": len(best)}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
