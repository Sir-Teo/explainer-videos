"""Optimization for Part 23 of *Computer Science, Built*: the simplex method (tableau, with a pivot log), duality,
Klee-Minty cubes, the ellipsoid method, a log-barrier interior-point method, total unimodularity, branch and bound,
approximation algorithms (vertex cover, set cover, metric TSP, knapsack FPTAS), Goemans-Williamson MAX-CUT, online
algorithms (ski rental, paging) and multiplicative weights.

Everything counts its work: pivots, ellipsoid steps, Newton steps, branch-and-bound nodes, page faults.  Exact answers
for small instances (brute force, Held-Karp, enumeration) are here too, so that every ratio the part quotes is measured
against the truth.
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

import numpy as np

# --------------------------------------------------------------------------------------------------- simplex

def simplex(c, A, b, rule: str = "dantzig", exact: bool = False, max_pivots: int = 100000):
    """Maximize c.x subject to A x <= b, x >= 0, with b >= 0 (so the slack basis is feasible).  Tableau simplex.
    ``rule``: "dantzig" (largest coefficient), "bland" (smallest index) or "steepest" (largest improvement).
    Returns dict: x, value, pivots, path (the vertex after each pivot, in the original variables), basis, duals."""
    m, n = len(A), len(c)
    num = Fraction if exact else float
    T = [[num(v) for v in A[i]] + [num(1 if j == i else 0) for j in range(m)] + [num(b[i])] for i in range(m)]
    z = [num(-v) for v in c] + [num(0)] * m + [num(0)]
    basis = [n + i for i in range(m)]
    path = [tuple(0.0 for _ in range(n))]
    pivots = 0
    eps = 0 if exact else 1e-12
    while pivots < max_pivots:
        cand = [j for j in range(n + m) if z[j] < -eps]
        if not cand:
            break
        if rule == "bland":
            e = min(cand)
        elif rule == "steepest":
            best, e = None, None
            for j in cand:
                rows = [(T[i][-1] / T[i][j], i) for i in range(m) if T[i][j] > eps]
                if not rows:
                    e = j
                    break
                t, _ = min(rows)
                gain = -z[j] * t
                if best is None or gain > best:
                    best, e = gain, j
        else:
            e = min(cand, key=lambda j: (z[j], j))
        rows = [(T[i][-1] / T[i][e], basis[i], i) for i in range(m) if T[i][e] > eps]
        if not rows:
            return {"status": "unbounded", "pivots": pivots, "path": path}
        _, _, r = min(rows)
        pv = T[r][e]
        T[r] = [v / pv for v in T[r]]
        for i in range(m):
            if i != r and T[i][e] != 0:
                f = T[i][e]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[r])]
        f = z[e]
        z = [a - f * bb for a, bb in zip(z, T[r])]
        basis[r] = e
        pivots += 1
        x = [0.0] * n
        for i, bv in enumerate(basis):
            if bv < n:
                x[bv] = float(T[i][-1])
        path.append(tuple(x))
    x = [num(0)] * n
    for i, bv in enumerate(basis):
        if bv < n:
            x[bv] = T[i][-1]
    duals = [z[n + i] for i in range(m)]
    return {"status": "optimal", "x": [float(v) for v in x], "value": float(z[-1]), "pivots": pivots, "path": path,
            "basis": basis, "duals": [float(v) for v in duals], "x_exact": x, "value_exact": z[-1]}


def klee_minty(n: int, eps: Fraction = Fraction(1, 3)):
    """The Klee-Minty cube in the form max x_n s.t. eps x_{j-1} <= x_j <= 1 - eps x_{j-1}, rewritten for simplex with
    the standard deformed product: max sum 2^{n-j} x_j, s.t. 2 sum_{i<j} 2^{j-i} x_i + x_j <= 5^j.  Dantzig's rule
    visits all 2^n vertices.  Returns (c, A, b)."""
    c = [2 ** (n - 1 - j) for j in range(n)]
    A, b = [], []
    for j in range(n):
        row = [2 ** (j - i + 1) if i < j else (1 if i == j else 0) for i in range(n)]
        A.append(row)
        b.append(5 ** (j + 1))
    return c, A, b


def random_lp(n, m, rng):
    """A random bounded feasible LP: max c.x, A x <= b with positive data."""
    A = [[rng.uniform(0.1, 1.0) for _ in range(n)] for _ in range(m)]
    b = [rng.uniform(1.0, 2.0) * n for _ in range(m)]
    c = [rng.uniform(0.1, 1.0) for _ in range(n)]
    return c, A, b


def vertices_3d(A, b):
    """All vertices of {x >= 0, A x <= b} in 3D, by intersecting every triple of planes."""
    P = [(list(row), float(v)) for row, v in zip(A, b)] + [([-1 if k == i else 0 for k in range(3)], 0.0)
                                                           for i in range(3)]
    out = []
    for (a1, b1), (a2, b2), (a3, b3) in itertools.combinations(P, 3):
        M = np.array([a1, a2, a3], float)
        if abs(np.linalg.det(M)) < 1e-12:
            continue
        x = np.linalg.solve(M, np.array([b1, b2, b3]))
        if all(np.dot(a, x) <= bb + 1e-9 for a, bb in P):
            if not any(np.allclose(x, y) for y in out):
                out.append(x)
    return [tuple(map(float, v)) for v in out]


def hull_faces_3d(V):
    from scipy.spatial import ConvexHull
    H = ConvexHull(np.array(V))
    return [list(map(int, s)) for s in H.simplices]


# --------------------------------------------------------------------------------------------------- ellipsoid

def ellipsoid_feasible(A, b, R: float = 10.0, max_steps: int = 10000, log: bool = False):
    """Find x with A x <= b (2D or more) by the central-cut ellipsoid method, starting from the ball of radius R.
    Returns (x or None, steps, log of (centre, shape matrix) per step)."""
    A = np.asarray(A, float)
    b = np.asarray(b, float)
    n = A.shape[1]
    x = np.zeros(n)
    P = np.eye(n) * R * R
    trail = [(x.copy(), P.copy())]
    for step in range(max_steps):
        viol = A @ x - b
        k = int(np.argmax(viol))
        if viol[k] <= 0:
            return x, step, trail
        a = A[k]
        Pa = P @ a
        g = Pa / math.sqrt(a @ Pa)
        x = x - g / (n + 1)
        P = (n * n / (n * n - 1.0)) * (P - (2.0 / (n + 1)) * np.outer(g, g))
        if log:
            trail.append((x.copy(), P.copy()))
    return None, max_steps, trail


# ---------------------------------------------------------------------------------------- interior point

def barrier_path(c, A, b, ts=None, x0=None, newton_tol=1e-10):
    """Central path of max c.x s.t. A x <= b: x*(t) = argmin -t c.x - sum log(b - A x), traced by damped Newton from a
    strictly feasible x0.  Returns (list of (t, x, Newton steps)), total Newton steps."""
    c = np.asarray(c, float)
    A = np.asarray(A, float)
    b = np.asarray(b, float)
    x = np.asarray(x0, float) if x0 is not None else np.zeros(A.shape[1])
    ts = ts if ts is not None else [0.5 * 1.6 ** k for k in range(28)]
    out, total = [], 0
    for t in ts:
        steps = 0
        for _ in range(100):
            s = b - A @ x
            g = -t * c + A.T @ (1.0 / s)
            H = A.T @ np.diag(1.0 / s ** 2) @ A
            dx = -np.linalg.solve(H, g)
            lam2 = float(-g @ dx)
            if lam2 / 2 < newton_tol:
                break
            step = 1.0
            while np.any(b - A @ (x + step * dx) <= 0):
                step *= 0.5
            f0 = -t * c @ x - np.sum(np.log(s))
            while True:
                xn = x + step * dx
                if -t * c @ xn - np.sum(np.log(b - A @ xn)) <= f0 - 0.25 * step * lam2 or step < 1e-12:
                    break
                step *= 0.5
            x = xn
            steps += 1
        total += steps
        out.append((t, x.copy(), steps))
    return out, total


# ---------------------------------------------------------------------------------- total unimodularity

def is_totally_unimodular(M, max_k: int | None = None):
    """Brute force: every square submatrix has determinant 0, 1 or -1.  Exponential; for small matrices.  Returns
    (bool, a witness submatrix (rows, cols, det) if not)."""
    M = np.asarray(M, int)
    m, n = M.shape
    K = min(m, n) if max_k is None else max_k
    for k in range(1, K + 1):
        for R in itertools.combinations(range(m), k):
            for C in itertools.combinations(range(n), k):
                d = round(np.linalg.det(M[np.ix_(R, C)]))
                if d not in (-1, 0, 1):
                    return False, (R, C, d)
    return True, None


def bipartite_incidence(edges, nl, nr):
    M = np.zeros((nl + nr, len(edges)), int)
    for k, (u, v) in enumerate(edges):
        M[u, k] = 1
        M[nl + v, k] = 1
    return M


# --------------------------------------------------------------------------------------- integer programming

def knapsack_lp_bound(vals, wts, cap, fixed):
    """Fractional knapsack bound given fixed decisions (dict i -> 0/1).  Returns (bound, x)."""
    rem = cap - sum(wts[i] for i, v in fixed.items() if v == 1)
    if rem < 0:
        return -math.inf, None
    val = sum(vals[i] for i, v in fixed.items() if v == 1)
    x = {i: float(v) for i, v in fixed.items()}
    free = sorted((i for i in range(len(vals)) if i not in fixed), key=lambda i: -vals[i] / wts[i])
    for i in free:
        if wts[i] <= rem:
            x[i] = 1.0
            rem -= wts[i]
            val += vals[i]
        else:
            x[i] = rem / wts[i]
            val += vals[i] * x[i]
            rem = 0
            for j in free[free.index(i) + 1:]:
                x[j] = 0.0
            break
    for i in free:
        x.setdefault(i, 0.0)
    return val, x


def branch_and_bound_knapsack(vals, wts, cap, log: bool = False):
    """0/1 knapsack by best-first branch and bound with the LP bound.  Returns (best value, choice, nodes, tree log)."""
    import heapq
    best, best_x = 0, None
    root_b, _ = knapsack_lp_bound(vals, wts, cap, {})
    heap = [(-root_b, 0, {})]
    nodes = 0
    tree = []
    uid = 0
    while heap:
        nb, _, fixed = heapq.heappop(heap)
        bound = -nb
        nodes += 1
        if bound <= best + 1e-9:
            if log:
                tree.append({"fixed": dict(fixed), "bound": bound, "fate": "pruned"})
            continue
        bnd, x = knapsack_lp_bound(vals, wts, cap, fixed)
        frac = [i for i, v in x.items() if 1e-9 < v < 1 - 1e-9]
        if not frac:
            val = sum(vals[i] for i, v in x.items() if v > 0.5)
            if val > best:
                best, best_x = val, {i: int(v > 0.5) for i, v in x.items()}
            if log:
                tree.append({"fixed": dict(fixed), "bound": bnd, "fate": "integral", "value": val})
            continue
        if log:
            tree.append({"fixed": dict(fixed), "bound": bnd, "fate": "branch", "on": frac[0]})
        i = frac[0]
        for v in (1, 0):
            f2 = dict(fixed)
            f2[i] = v
            b2, _ = knapsack_lp_bound(vals, wts, cap, f2)
            if b2 > best + 1e-9:
                uid += 1
                heapq.heappush(heap, (-b2, uid, f2))
            elif log:
                tree.append({"fixed": f2, "bound": b2, "fate": "pruned"})
    return best, best_x, nodes, tree


def knapsack_dp(vals, wts, cap):
    best = [0] * (cap + 1)
    for v, w in zip(vals, wts):
        for c in range(cap, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[cap]


def knapsack_fptas(vals, wts, cap, eps):
    """Ibarra-Kim: scale values down by K = eps vmax / n, solve exactly by DP over (scaled) value.  Returns (value of
    the chosen set in the true values, table size)."""
    n = len(vals)
    vmax = max(v for v, w in zip(vals, wts) if w <= cap)
    K = eps * vmax / n
    sv = [int(v // K) for v in vals]
    V = sum(sv)
    INF = math.inf
    minw = [0] + [INF] * V
    choice = [[] for _ in range(V + 1)]
    for i in range(n):
        for s in range(V, sv[i] - 1, -1):
            if minw[s - sv[i]] + wts[i] < minw[s]:
                minw[s] = minw[s - sv[i]] + wts[i]
                choice[s] = choice[s - sv[i]] + [i]
    s = max(s for s in range(V + 1) if minw[s] <= cap)
    return sum(vals[i] for i in choice[s]), (n * V)


# ------------------------------------------------------------------------------------------ approximation

def vertex_cover_exact(n, edges):
    best = None
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(u in s or v in s for u, v in edges):
                return k, s
    return best


def vertex_cover_matching(n, edges, seed=0):
    rng = random.Random(seed)
    E = list(edges)
    rng.shuffle(E)
    cover = set()
    for u, v in E:
        if u not in cover and v not in cover:
            cover |= {u, v}
    return cover


def vertex_cover_lp(n, edges):
    from scipy.optimize import linprog
    A = np.zeros((len(edges), n))
    for k, (u, v) in enumerate(edges):
        A[k, u] = A[k, v] = -1
    r = linprog(np.ones(n), A_ub=A, b_ub=-np.ones(len(edges)), bounds=[(0, 1)] * n, method="highs")
    x = r.x
    return float(r.fun), x, {i for i in range(n) if x[i] >= 0.5 - 1e-9}


def set_cover_greedy(universe, sets):
    U = set(universe)
    chosen = []
    while U:
        k = max(range(len(sets)), key=lambda i: len(U & sets[i]))
        chosen.append(k)
        U -= sets[k]
    return chosen


def set_cover_exact(universe, sets):
    U = set(universe)
    for k in range(1, len(sets) + 1):
        for C in itertools.combinations(range(len(sets)), k):
            if set().union(*(sets[i] for i in C)) >= U:
                return list(C)


def harmonic_bad_set_cover(k: int):
    """The classic instance where greedy pays H_k-ish: two 'rows' cover everything optimally; greedy is lured by columns
    of sizes 2, 4, 8, ...  Universe of size 2(2^k - 1).  Returns (universe, sets, optimum = 2)."""
    U = list(range(2 * (2 ** k - 1)))
    top = set(range(2 ** k - 1))
    bot = set(range(2 ** k - 1, 2 * (2 ** k - 1)))
    sets = [top, bot]
    start = 0
    for j in range(k):
        size = 2 ** j
        cols = set(range(start, start + size)) | set(range(2 ** k - 1 + start, 2 ** k - 1 + start + size))
        sets.append(cols)
        start += size
    return U, sets, 2


# --------------------------------------------------------------------------------------------------- TSP

def tour_length(P, tour):
    return sum(math.dist(P[tour[i]], P[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))


def held_karp(P):
    """Exact TSP by Held-Karp dynamic programming, O(2^n n^2).  Returns (length, tour)."""
    n = len(P)
    D = [[math.dist(P[i], P[j]) for j in range(n)] for i in range(n)]
    INF = math.inf
    dp = {(1, 0): 0.0}
    par = {}
    for mask in range(1, 1 << n):
        if not mask & 1:
            continue
        for j in range(n):
            if not mask & (1 << j) or (mask, j) not in dp:
                continue
            cur = dp[(mask, j)]
            for k in range(1, n):
                if mask & (1 << k):
                    continue
                nm = mask | (1 << k)
                v = cur + D[j][k]
                if v < dp.get((nm, k), INF):
                    dp[(nm, k)] = v
                    par[(nm, k)] = j
    full = (1 << n) - 1
    best, last = min((dp[(full, j)] + D[j][0], j) for j in range(1, n))
    tour = [0] * n
    mask, j = full, last
    for pos in range(n - 1, 0, -1):
        tour[pos] = j
        pj = par[(mask, j)]
        mask ^= 1 << j
        j = pj
    return best, tour


def mst_prim(P):
    n = len(P)
    inside = [False] * n
    best = [math.inf] * n
    par = [-1] * n
    best[0] = 0
    edges = []
    for _ in range(n):
        u = min((i for i in range(n) if not inside[i]), key=lambda i: best[i])
        inside[u] = True
        if par[u] >= 0:
            edges.append((par[u], u))
        for v in range(n):
            if not inside[v]:
                d = math.dist(P[u], P[v])
                if d < best[v]:
                    best[v], par[v] = d, u
    return edges


def double_tree(P):
    edges = mst_prim(P)
    adj = {i: [] for i in range(len(P))}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    tour, seen, st = [], set(), [0]
    while st:
        u = st.pop()
        if u in seen:
            continue
        seen.add(u)
        tour.append(u)
        for v in sorted(adj[u], reverse=True):
            if v not in seen:
                st.append(v)
    return tour, edges


def min_weight_perfect_matching(P, nodes):
    """Exact, by DP over subsets (|nodes| <= ~20)."""
    nodes = list(nodes)
    k = len(nodes)
    from functools import lru_cache

    @lru_cache(None)
    def go(mask):
        if mask == 0:
            return 0.0, ()
        i = (mask & -mask).bit_length() - 1
        best = (math.inf, ())
        rest = mask & ~(1 << i)
        m = rest
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            v, pr = go(rest & ~(1 << j))
            v += math.dist(P[nodes[i]], P[nodes[j]])
            if v < best[0]:
                best = (v, pr + ((nodes[i], nodes[j]),))
        return best
    return go((1 << k) - 1)[1]


def christofides(P):
    """Christofides-Serdyukov: MST + min-weight perfect matching on odd vertices + Euler tour + shortcuts."""
    edges = mst_prim(P)
    deg = [0] * len(P)
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    odd = [i for i in range(len(P)) if deg[i] % 2]
    M = min_weight_perfect_matching(P, odd)
    multi = {i: [] for i in range(len(P))}
    for u, v in list(edges) + list(M):
        multi[u].append(v)
        multi[v].append(u)
    # Hierholzer
    st, circ = [0], []
    adj = {i: list(v) for i, v in multi.items()}
    while st:
        u = st[-1]
        if adj[u]:
            v = adj[u].pop()
            adj[v].remove(u)
            st.append(v)
        else:
            circ.append(st.pop())
    tour, seen = [], set()
    for u in circ:
        if u not in seen:
            seen.add(u)
            tour.append(u)
    return tour, edges, M, odd


def two_opt(P, tour):
    tour = list(tour)
    n = len(tour)
    improved, moves = True, 0
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n if i else n - 1):
                a, b, c, d = P[tour[i]], P[tour[i + 1]], P[tour[j]], P[tour[(j + 1) % n]]
                if math.dist(a, c) + math.dist(b, d) < math.dist(a, b) + math.dist(c, d) - 1e-12:
                    tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                    improved = True
                    moves += 1
    return tour, moves


def nearest_neighbour_tour(P):
    n = len(P)
    tour, left = [0], set(range(1, n))
    while left:
        u = tour[-1]
        v = min(left, key=lambda j: math.dist(P[u], P[j]))
        tour.append(v)
        left.remove(v)
    return tour


# ------------------------------------------------------------------------------------------- MAX-CUT

def maxcut_exact(n, edges):
    best, bs = -1, None
    for mask in range(1 << (n - 1)):
        c = sum(1 for u, v in edges if ((mask >> u) ^ (mask >> v)) & 1)
        if c > best:
            best, bs = c, mask
    return best, bs


def gw_vectors(n, edges, dim=None, iters=3000, lr=0.05, seed=0):
    """The Goemans-Williamson SDP by the Burer-Monteiro low-rank method: unit vectors v_i in R^k minimizing
    sum over edges of v_i . v_j (i.e. maximizing sum (1 - v_i.v_j)/2), by projected gradient.  Returns (V, SDP value)."""
    k = dim or max(3, int(math.ceil(math.sqrt(2 * n))) + 1)
    rng = np.random.default_rng(seed)
    V = rng.standard_normal((n, k))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    E = np.array(edges)
    for it in range(iters):
        G = np.zeros_like(V)
        np.add.at(G, E[:, 0], V[E[:, 1]])
        np.add.at(G, E[:, 1], V[E[:, 0]])
        V = V - lr * G
        V /= np.linalg.norm(V, axis=1, keepdims=True)
    val = float(np.sum((1 - np.sum(V[E[:, 0]] * V[E[:, 1]], axis=1)) / 2))
    return V, val


def gw_round(V, edges, trials=200, seed=1):
    rng = np.random.default_rng(seed)
    E = np.array(edges)
    vals = []
    for _ in range(trials):
        r = rng.standard_normal(V.shape[1])
        side = V @ r >= 0
        vals.append(int(np.sum(side[E[:, 0]] != side[E[:, 1]])))
    return vals


def gw_alpha():
    th = np.linspace(1e-4, math.pi, 200001)
    f = 2 * th / (math.pi * (1 - np.cos(th)))
    k = int(np.argmin(f))
    return float(f[k]), float(th[k])


# ------------------------------------------------------------------------------------------ online algorithms

def ski_rental(B, days, strategy="break_even", rng=None):
    """Rent costs 1 a day, buying costs B.  Returns the cost of the strategy when the season lasts ``days``."""
    if strategy == "break_even":
        buy_day = B
    elif strategy == "random":
        # Karlin et al.: buy on day j with probability proportional to (1 - 1/B)^(B - j)
        ws = [(1 - 1 / B) ** (B - j) for j in range(1, B + 1)]
        tot = sum(ws)
        u, acc, buy_day = rng.random() * tot, 0.0, B
        for j, w in enumerate(ws, start=1):
            acc += w
            if u <= acc:
                buy_day = j
                break
    else:
        raise ValueError(strategy)
    if days < buy_day:
        return days
    return (buy_day - 1) + B


def paging(trace, k, policy, rng=None):
    """Page faults of a cache of k pages: "lru", "fifo", "random", "marking" (randomized), or "opt" (Belady)."""
    faults = 0
    if policy == "opt":
        nxt = [0] * len(trace)
        last = {}
        for i in range(len(trace) - 1, -1, -1):
            nxt[i] = last.get(trace[i], math.inf)
            last[trace[i]] = i
        cs = set()
        nextuse = {}
        for i, p in enumerate(trace):
            if p in cs:
                nextuse[p] = nxt[i]
                continue
            faults += 1
            if len(cs) >= k:
                ev = max(cs, key=lambda q: nextuse[q])
                cs.remove(ev)
            cs.add(p)
            nextuse[p] = nxt[i]
        return faults
    if policy == "marking":
        cs, marked = set(), set()
        for p in trace:
            if p in cs:
                marked.add(p)
                continue
            faults += 1
            if len(cs) >= k:
                if len(marked) == len(cs):
                    marked = set()
                ev = rng.choice(sorted(cs - marked))
                cs.remove(ev)
            cs.add(p)
            marked.add(p)
        return faults
    from collections import OrderedDict
    od = OrderedDict()
    for p in trace:
        if p in od:
            if policy == "lru":
                od.move_to_end(p)
            continue
        faults += 1
        if len(od) >= k:
            if policy == "random":
                ev = rng.choice(list(od))
                del od[ev]
            else:
                od.popitem(last=False)
        od[p] = True
    return faults


# ------------------------------------------------------------------------------------- multiplicative weights

def hedge(losses, eta):
    """Hedge / multiplicative weights over n experts with losses in [0, 1] (T x n array).  Returns (algorithm's
    cumulative expected loss, best expert's loss, the weight history)."""
    L = np.asarray(losses, float)
    T, n = L.shape
    w = np.ones(n)
    alg = 0.0
    hist = []
    for t in range(T):
        p = w / w.sum()
        hist.append(p.copy())
        alg += float(p @ L[t])
        w *= np.exp(-eta * L[t])
    return alg, float(L.sum(0).min()), np.array(hist)


def mw_zero_sum(M, T, eta=None):
    """Approximate the value of the zero-sum game with payoff matrix M (row player maximizes, entries in [0, 1]) by
    letting the row player run multiplicative weights against a best-responding column player.  Returns (lower,
    upper) bounds on the value, and the averaged row strategy."""
    M = np.asarray(M, float)
    m, n = M.shape
    eta = eta or math.sqrt(math.log(m) / T)
    w = np.ones(m)
    avg_p = np.zeros(m)
    avg_q = np.zeros(n)
    for _ in range(T):
        p = w / w.sum()
        j = int(np.argmin(p @ M))
        avg_p += p
        avg_q[j] += 1
        w *= np.exp(eta * M[:, j])
    avg_p /= T
    avg_q /= T
    return float(np.min(avg_p @ M)), float(np.max(M @ avg_q)), avg_p
