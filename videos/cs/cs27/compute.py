"""Precompute everything numerical in Part 27 of *Computer Science, Built* ("Proofs and Randomness").

    python -m videos.cs.cs27.compute              # everything missing
    python -m videos.cs.cs27.compute --force zk

Results are cached in ``.cache/cs27/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/proofs.py`` (tested in tests/test_cs27_proofs.py).

Items:
    amplify    majority-vote error against repetitions; Adleman's union bound in numbers
    equality   fingerprints: bits sent and the measured error, against n deterministic bits
    switching  random restrictions of a random 3-DNF: decision-tree depth against the switching-lemma bound
    gni        the graph non-isomorphism protocol: an honest prover always wins, a bluffer half the time
    sumcheck   an honest transcript for #SAT, and a cheating prover's survival against the bound
    zk         zero-knowledge 3-colouring: a cheater's survival by round; real against simulated transcripts
    blr        the linearity test's rejection probability against the distance from linear
    maxsat     random assignments against local search on MAX-3SAT
    vc         FPT vertex cover: search-tree nodes and Buss's kernel against brute force
    permanent  Ryser's permanent against Bareiss's determinant: time by n
    finegrained orthogonal vectors and 3SUM: quadratic time measured
    planted    planted clique in G(n, 1/2): how often the degree heuristic recovers it, by clique size
    oneway     multiplying two primes against factoring the product with Pollard's rho, by size
    unique     unique games with a planted labelling and an eps fraction of corrupted edges: propagation's value
    pit        Schwartz--Zippel on the Vandermonde identity: a true identity always passes, a false one rarely
    williams   Williams' reduction: random 3-SAT on 24 variables as orthogonal vectors, against the CDCL answer
"""

from __future__ import annotations

import itertools
import math
import random
import statistics
import time

from explainer.ai.cache import Cache
from explainer.cs.algo import proofs as P
from explainer.cs.algo import complexity as X

CACHE = Cache("cs27")
load = CACHE.load

WEB = [[1, 2, -3], [-1, 3, 4], [-2, -3, -4], [1, -2, 4], [-1, 2, 3]]


def compute_amplify() -> dict:
    rows = []
    for k in (1, 3, 5, 11, 21, 51, 101, 201):
        rows.append({"k": k, "error": P.binom_tail(k, 1 / 3, k // 2 + 1)})
    adl = []
    for n in (10, 20, 50, 100):
        k = 1
        while P.binom_tail(k, 1 / 3, k // 2 + 1) >= 2.0 ** -(n + 1):
            k += 2
        adl.append({"n": n, "runs": k, "error": P.binom_tail(k, 1 / 3, k // 2 + 1),
                    "union": 2.0 ** n * P.binom_tail(k, 1 / 3, k // 2 + 1)})
    return {"rows": rows, "adleman": adl}


def compute_equality() -> dict:
    rng = random.Random(1)
    n = 1000
    q = P.next_prime(n * n)
    x = [rng.randrange(2) for _ in range(n)]
    y = x[:]
    y[rng.randrange(n)] ^= 1
    trials = 20000
    wrong = sum(P.fingerprint_eq(x, y, q, rng)[0] for _ in range(trials))
    small_q = P.next_prime(2 * n)
    wrong_small = sum(P.fingerprint_eq(x, y, small_q, rng)[0] for _ in range(trials))
    rows = []
    for e in (3, 6, 9, 12):
        nn = 10 ** e
        bits = 2 * (2 * math.ceil(math.log2(nn)) + 1)
        rows.append({"n": nn, "det_bits": nn, "rand_bits": bits})
    return {"n": n, "q": q, "trials": trials, "wrong": wrong, "bound": n / q, "small_q": small_q,
            "wrong_small": wrong_small, "bound_small": n / small_q, "rows": rows}


def compute_switching() -> dict:
    rng = random.Random(2)
    n, terms, width = 14, 20, 3
    f = P.dnf_random(n, terms, width, rng)
    rows = []
    for p in (0.02, 0.04, 0.066, 0.1, 0.2):
        hist = {}
        trials = 1500
        for _ in range(trials):
            rho = P.random_restriction(n, p, rng)
            g = P.restrict(f, rho)
            free = [v for v in range(n) if v not in rho]
            if len(free) > 10:
                d = 99
            else:
                d = P.dt_depth(P.truth_table(g, free), len(free))
            hist[d] = hist.get(d, 0) + 1
        ge = {s: sum(c for d, c in hist.items() if d >= s) / trials for s in (1, 2, 3)}
        rows.append({"p": p, "hist": {str(k): v for k, v in sorted(hist.items())}, "ge": ge,
                     "bound": {s: min(1.0, (5 * p * width) ** s) for s in (1, 2, 3)}})
    # one restriction to draw
    rho = P.random_restriction(n, 0.2, random.Random(11))
    g = P.restrict(f, rho)
    ex = {"rho": {str(k): v for k, v in rho.items()},
          "after": [[[v, b] for v, b in t] for t in g] if isinstance(g, list) else g}
    return {"n": n, "terms": terms, "width": width, "dnf": [[[v, b] for v, b in t] for t in f], "rows": rows,
            "example": ex}


def compute_gni() -> dict:
    rng = random.Random(3)
    G0 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]                   # a 5-cycle
    G1 = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]                   # a triangle with a tail
    G2 = [(0, 2), (2, 4), (4, 1), (1, 3), (3, 0)]                   # another 5-cycle
    honest = [P.gni_round(G0, G1, 5, rng) for _ in range(200)]
    bluff = [P.gni_round(G0, G2, 5, rng) for _ in range(2000)]
    rate = sum(a == b for b, a in bluff) / len(bluff)
    return {"G0": G0, "G1": G1, "G2": G2, "honest_rate": sum(a == b for b, a in honest) / len(honest),
            "bluff_rate": rate, "after_k": [{"k": k, "survive": 0.5 ** k} for k in (1, 5, 10, 20)]}


def compute_sumcheck() -> dict:
    rng = random.Random(4)
    n, p = 4, 97
    true = P.count_sat(WEB, n)
    ok, _, log = P.sumcheck(WEB, n, p, true, rng)
    trials = 3000
    surv = sum(P.sumcheck(WEB, n, p, true + 1, rng, cheat=True)[0] for _ in range(trials)) / trials
    deg = len(WEB)
    bound = 1 - (1 - deg / p) ** n
    big = P.next_prime(10 ** 6)
    surv_big = sum(P.sumcheck(WEB, n, big, true + 1, rng, cheat=True)[0] for _ in range(300)) / 300
    return {"n": n, "p": p, "clauses": WEB, "true": true, "honest_ok": ok, "log": log, "trials": trials,
            "cheat_survive": surv, "bound": bound, "big_p": big, "cheat_survive_big": surv_big,
            "big_bound": 1 - (1 - deg / big) ** n}


def compute_zk() -> dict:
    rng = random.Random(5)
    # the Petersen graph is 3-colourable
    outer = [(i, (i + 1) % 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    spokes = [(i, 5 + i) for i in range(5)]
    edges = outer + inner + spokes
    V = list(range(10))
    nv, cl, var = X.coloring_cnf(V, edges, 3)
    model, _ = X.cdcl(nv, cl)
    col = [next(c for c in range(3) if model[var(v, c)]) for v in V]
    m = len(edges)
    bad = col[:]
    u, v = edges[0]
    bad[v] = bad[u]
    nbad = sum(1 for a, b in edges if bad[a] == bad[b])
    trials = 2000
    caught_at = [P.zk_colouring(10, edges, bad, 200, rng)[0] for _ in range(trials)]
    surv = []
    for k in (1, 5, 10, 20, 50, 100):
        emp = sum(1 for c in caught_at if c is None or c > k) / trials
        surv.append({"k": k, "empirical": emp, "theory": (1 - nbad / m) ** k})
    _, real = P.zk_colouring(10, edges, col, 6000, rng)
    sim = P.zk_simulate(6000, rng)
    pairs = [(a, b) for a in range(3) for b in range(3) if a != b]
    dist = {"real": [sum(1 for r in real if r == pr) / len(real) for pr in pairs],
            "sim": [sum(1 for r in sim if r == pr) / len(sim) for pr in pairs], "pairs": pairs}
    return {"edges": edges, "colouring": col, "bad": bad, "m": m, "bad_edges": nbad, "survive": surv,
            "dist": dist, "rounds_for_1e9": math.ceil(math.log(1e-9) / math.log(1 - 1 / m))}


def compute_blr() -> dict:
    rng = random.Random(6)
    n = 8
    N = 1 << n
    a = 0b10110101
    lin = [bin(a & x).count("1") & 1 for x in range(N)]
    rows = []
    for t in (0, 4, 8, 16, 32, 48, 64, 96, 128):
        for _ in range(2 if t else 1):
            f = lin[:]
            for x in rng.sample(range(N), t):
                f[x] ^= 1
            d = P.distance_to_linear(f, n)
            rows.append({"flipped": t, "distance": d, "reject": P.blr_rejection(f, n)})
    return {"n": n, "rows": rows}


def compute_maxsat() -> dict:
    rng = random.Random(7)
    rows = []
    for ratio in (4.0, 5.0, 6.0, 8.0):
        n = 100
        m = int(ratio * n)
        rnd, ws = [], []
        for _ in range(5):
            cl = X.random_ksat(n, m, 3, rng)
            for _ in range(20):
                a = [False] + [rng.random() < 0.5 for _ in range(n)]
                rnd.append(sum(any(a[abs(l)] == (l > 0) for l in c) for c in cl) / m)
            best, _ = P.walksat(n, cl, rng, flips=4000)
            ws.append(best / m)
        rows.append({"ratio": ratio, "random": statistics.mean(rnd), "walksat": statistics.mean(ws)})
    return {"rows": rows}


def compute_vc() -> dict:
    rng = random.Random(8)
    rows = []
    n = 40
    for k in (4, 6, 8, 10, 12):
        cover = rng.sample(range(n), k)
        others = [v for v in range(n) if v not in cover]
        edges = set()
        for v in others:
            for u in rng.sample(cover, min(2, k)):
                edges.add((min(u, v), max(u, v)))
        for u, w in itertools.combinations(cover, 2):
            if rng.random() < 0.3:
                edges.add((u, w))
        edges = sorted(edges)
        t = time.perf_counter()
        c, nodes = P.vc_branch(edges, k)
        bt = time.perf_counter() - t
        ker = P.buss_kernel(edges, k)
        rows.append({"k": k, "edges": len(edges), "found": c is not None, "nodes": nodes, "bound": 2 ** (k + 1) - 1,
                     "seconds": bt, "brute_subsets": math.comb(n, k),
                     "kernel_edges": len(ker[1]) if ker else None, "forced": len(ker[0]) if ker else None})
    return {"n": n, "rows": rows}


def compute_permanent() -> dict:
    rng = random.Random(9)
    rows = []
    for n in (8, 10, 12, 14, 16, 18, 20):
        A = [[rng.randrange(0, 2) for _ in range(n)] for _ in range(n)]
        t = time.perf_counter()
        pm = P.permanent_ryser(A)
        tp = time.perf_counter() - t
        t = time.perf_counter()
        d = P.det_bareiss(A)
        td = time.perf_counter() - t
        rows.append({"n": n, "perm": pm, "perm_s": tp, "det": d, "det_s": td})
    big = []
    for n in (50, 100, 200):
        A = [[rng.randrange(0, 2) for _ in range(n)] for _ in range(n)]
        t = time.perf_counter()
        P.det_bareiss(A)
        big.append({"n": n, "det_s": time.perf_counter() - t})
    return {"rows": rows, "det_big": big}


def compute_finegrained() -> dict:
    rng = random.Random(10)
    ov, ts = [], []
    for n in (500, 1000, 2000, 4000):
        A = [rng.getrandbits(64) | (1 << 63) for _ in range(n)]
        B = [rng.getrandbits(64) | (1 << 63) for _ in range(n)]
        t = time.perf_counter()
        P.ov_brute(A, B)
        ov.append({"n": n, "seconds": time.perf_counter() - t})
        xs = [rng.randrange(-10 ** 9, 10 ** 9) | 1 for _ in range(n)]        # all odd: no triple sums to 0
        t = time.perf_counter()
        r = P.three_sum(xs)
        ts.append({"n": n, "seconds": time.perf_counter() - t, "found": r is not None})
    return {"ov": ov, "three_sum": ts}


def compute_planted() -> dict:
    n, trials = 1000, 20
    rows = []
    for k in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120):
        ok = 0
        for s in range(trials):
            adj, S = P.planted_clique(n, k, random.Random(1000 * k + s))
            ok += P.degree_recover(adj, k) == S
        rows.append({"k": k, "rate": ok / trials})
    return {"n": n, "trials": trials, "rows": rows, "sqrt_nlogn": math.sqrt(n * math.log(n)),
            "two_log": 2 * math.log2(n)}


def compute_oneway() -> dict:
    rows = []
    for bits in (24, 32, 40, 48, 56, 64, 72, 80):
        mul, fac, steps = [], [], []
        for s in range(5):
            rng = random.Random(100 * bits + s)
            p = P.next_prime(rng.getrandbits(bits // 2) | (1 << (bits // 2 - 1)))
            q = P.next_prime(rng.getrandbits(bits // 2) | (1 << (bits // 2 - 1)))
            t = time.perf_counter()
            for _ in range(1000):
                N = p * q
            mul.append((time.perf_counter() - t) / 1000)
            t = time.perf_counter()
            f, st = P.pollard_rho(N, random.Random(s))
            fac.append(time.perf_counter() - t)
            steps.append(st)
            assert f in (p, q)
        rows.append({"bits": bits, "mul_s": statistics.median(mul), "factor_s": statistics.median(fac),
                     "steps": statistics.median(steps)})
    return {"rows": rows}


def compute_unique() -> dict:
    n, m, k = 3000, 9000, 7
    rows = []
    for eps in (0.0, 0.01, 0.03, 0.05, 0.1, 0.2):
        edges, planted = P.ug_instance(n, m, k, eps, random.Random(5))
        roots = random.Random(1).sample(range(n), 10)
        best = max(P.ug_value(edges, P.ug_propagate(n, edges, k, r), k) for r in roots)
        rnd = statistics.mean(P.ug_value(edges, [random.Random(s).randrange(k) for _ in range(n)], k)
                              for s in range(5))
        rows.append({"eps": eps, "planted": P.ug_value(edges, planted, k), "propagate": best, "random": rnd})
    return {"n": n, "m": m, "k": k, "rows": rows}


def compute_williams() -> dict:
    n, m = 24, 101
    rows = []
    for s in range(6):
        cl = X.random_ksat(n, m, 3, random.Random(700 + s))
        t = time.perf_counter()
        A, B = P.sat_to_ov(cl, n)
        tb = time.perf_counter() - t
        t = time.perf_counter()
        ov = P.ov_brute(A, B)
        to = time.perf_counter() - t
        model, st = X.cdcl(n, cl)
        rows.append({"seed": 700 + s, "build_s": tb, "ov_s": to, "ov": ov, "sat": model is not None,
                     "conflicts": st.get("conflicts")})
    return {"n": n, "m": m, "N": 1 << (n // 2), "rows": rows}


def compute_pit() -> dict:
    n, trials = 10, 5000
    rows = []
    for p in (101, 1009, 10007, 1000003):
        rng = random.Random(p)
        t = time.perf_counter()
        good = sum(P.vandermonde_test([rng.randrange(p) for _ in range(n)], p) for _ in range(trials))
        dt = (time.perf_counter() - t) / trials
        bad = sum(P.vandermonde_test([rng.randrange(p) for _ in range(n)], p, wrong=True) for _ in range(trials))
        rows.append({"p": p, "true_pass": good / trials, "false_pass": bad / trials, "bound": n * (n - 1) / 2 / p,
                     "seconds": dt})
    return {"n": n, "trials": trials, "terms": math.factorial(n), "degree": n * (n - 1) // 2, "rows": rows}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
