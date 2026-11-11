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

def _graph(n, edges):
    n = _integer(n, "vertices")
    out = []
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("edges must contain two endpoints")
        u, v = (_integer(x, "endpoint") for x in edge)
        if u >= n or v >= n or u == v:
            raise ValueError("edges require distinct valid endpoints")
        out.append((u, v))
    return n, out


def _points(points):
    points = [tuple(map(float, point)) for point in points]
    if points and (len(points[0]) == 0 or any(len(point) != len(points[0]) for point in points)):
        raise ValueError("points require a common positive dimension")
    if not all(math.isfinite(v) for point in points for v in point):
        raise ValueError("point coordinates must be finite")
    return points



def _integer(value, name, minimum=0):
    import operator
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be an integer")
    try:
        value = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _knapsack_instance(vals, wts, cap):
    vals = [_integer(v, "value") for v in vals]
    wts = [_integer(w, "weight", 1) for w in wts]
    cap = _integer(cap, "capacity")
    if len(vals) != len(wts):
        raise ValueError("values and weights must have equal length")
    return vals, wts, cap


def _determinant_bareiss(matrix):
    """Exact integer determinant by fraction-free elimination."""
    A = [list(row) for row in matrix]
    n = len(A)
    if n == 0:
        return 1
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if A[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            A[k], A[pivot_row] = A[pivot_row], A[k]
            sign = -sign
        pivot = A[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = A[i][j] * pivot - A[i][k] * A[k][j]
                quotient, remainder = divmod(numerator, previous)
                assert remainder == 0
                A[i][j] = quotient
            A[i][k] = 0
        previous = pivot
    return sign * A[-1][-1]


# --------------------------------------------------------------------------------------------------- simplex

def simplex(c, A, b, rule: str = "dantzig", exact: bool = False, max_pivots: int = 100000):
    """Maximize c.x subject to A x <= b, x >= 0, with b >= 0 (so the slack basis is feasible).  Tableau simplex.
    ``rule``: "dantzig" (largest coefficient), "bland" (smallest index) or "steepest" (largest improvement).
    Returns dict: x, value, pivots, path (the vertex after each pivot, in the original variables), basis, duals."""
    if rule not in ("dantzig", "bland", "steepest"):
        raise ValueError("unknown pivot rule")
    max_pivots = _integer(max_pivots, "max_pivots")
    c, A, b = list(c), [list(row) for row in A], list(b)
    m, n = len(A), len(c)
    if len(b) != m or any(len(row) != n for row in A):
        raise ValueError("incompatible simplex dimensions")
    if not all(math.isfinite(v) for v in [*c, *b, *(v for row in A for v in row)]):
        raise ValueError("simplex inputs must be finite")
    if any(v < 0 for v in b):
        raise ValueError("this slack-basis simplex requires b >= 0; no Phase I is implemented")
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
    return {"status": "iteration_limit" if any(v < -eps for v in z[:-1]) else "optimal", "x": [float(v) for v in x], "value": float(z[-1]), "pivots": pivots, "path": path,
            "basis": basis, "duals": [float(v) for v in duals], "duals_exact": duals, "x_exact": x, "value_exact": z[-1]}


def klee_minty(n: int, eps: Fraction = Fraction(1, 3)):
    """Fixed power-coefficient Klee-Minty variant, indexed from zero:
    max sum_j 2**(n-1-j)*x_j, with x>=0 and
    2*sum_{i<j}2**(j-i)*x_i+x_j <= 5**(j+1).
    Dantzig's rule visits all2**n vertices in exact arithmetic. The legacy eps
    argument is retained only at its default value; this variant does not use it.
    """
    n = _integer(n, "dimension", 1)
    if eps != Fraction(1, 3):
        raise ValueError("this fixed Klee-Minty variant does not parameterize eps")
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
    A, b = [list(row) for row in A], list(b)
    if len(A) != len(b) or any(len(row) != 3 for row in A):
        raise ValueError("3D vertex enumeration requires compatible three-column constraints")
    if not all(math.isfinite(x) for x in [*b, *(v for row in A for v in row)]):
        raise ValueError("vertex-enumeration data must be finite")
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
    """Central cuts in dimension>=2, initially enclosing the sought region in B(0,R).
    None means the budget was exhausted (or a contradictory constant was found),
    and is not a general infeasibility certificate."""
    A, b = np.asarray(A, float), np.asarray(b, float)
    if A.ndim != 2 or A.shape[1] < 2 or b.shape != (A.shape[0],):
        raise ValueError("ellipsoid requires compatible dimensions, n>=2")
    if not np.isfinite(A).all() or not np.isfinite(b).all() or not math.isfinite(R) or R <= 0:
        raise ValueError("ellipsoid data must be finite and R positive")
    max_steps = _integer(max_steps, "max_steps")
    n = A.shape[1]
    x, P = np.zeros(n), np.eye(n) * R * R
    if not np.isfinite(P).all():
        raise ValueError("initial squared radius must be finite")
    trail = [(x.copy(), P.copy())]
    for step in range(max_steps + 1):
        violation = A @ x - b
        if len(b) == 0 or np.max(violation) <= 0:
            return x, step, trail
        if step == max_steps:
            break
        k = int(np.argmax(violation))
        a = A[k]
        if not np.any(a):
            return None, step, trail
        Pa = P @ a
        denominator = float(a @ Pa)
        if not math.isfinite(denominator) or denominator <= 0:
            raise RuntimeError("ellipsoid numerical shape breakdown")
        g = Pa / math.sqrt(denominator)
        x = x - g / (n + 1)
        P = (n * n / (n * n - 1.0)) * (P - (2.0 / (n + 1)) * np.outer(g, g))
        P = (P + P.T) / 2
        if not np.isfinite(x).all() or not np.isfinite(P).all():
            raise RuntimeError("ellipsoid numerical overflow")
        if log:
            trail.append((x.copy(), P.copy()))
    return None, max_steps, trail


# ---------------------------------------------------------------------------------------- interior point

def barrier_path(c, A, b, ts=None, x0=None, newton_tol=1e-10):
    """Damped Newton log-barrier trace from a strictly feasible initial point.
    Numerical failure or a Newton/line-search budget raises instead of certifying convergence."""
    c, A, b = np.asarray(c, float), np.asarray(A, float), np.asarray(b, float)
    if c.ndim != 1 or not len(c) or A.ndim != 2 or A.shape[1] != len(c) or b.shape != (len(A),):
        raise ValueError("incompatible barrier dimensions")
    x = np.zeros(len(c)) if x0 is None else np.asarray(x0, float).copy()
    if x.shape != c.shape or not all(np.isfinite(a).all() for a in (c, A, b, x)):
        raise ValueError("barrier inputs must be finite")
    if not math.isfinite(newton_tol) or newton_tol <= 0 or np.any(b - A @ x <= 0):
        raise ValueError("barrier requires positive tolerance and strictly feasible x0")
    ts = list(ts) if ts is not None else [0.5 * 1.6 ** k for k in range(28)]
    if any(not math.isfinite(t) or t <= 0 for t in ts):
        raise ValueError("barrier parameters must be finite and positive")
    out, total = [], 0
    for t in ts:
        steps = 0
        for iteration in range(100):
            s = b - A @ x
            g = -t * c + A.T @ (1.0 / s)
            H = A.T @ ((1.0 / s ** 2)[:, None] * A)
            try:
                dx = -np.linalg.solve(H, g)
            except np.linalg.LinAlgError as exc:
                raise RuntimeError("singular barrier Hessian") from exc
            decrement = float(-g @ dx)
            if not np.isfinite(dx).all() or not math.isfinite(decrement) or decrement < -1e-12:
                raise RuntimeError("barrier numerical breakdown")
            if decrement / 2 < newton_tol:
                break
            f0 = -t * c @ x - np.sum(np.log(s))
            step = 1.0
            for backtrack in range(80):
                xn = x + step * dx
                slack = b - A @ xn
                if np.all(slack > 0):
                    objective = -t * c @ xn - np.sum(np.log(slack))
                    if math.isfinite(objective) and objective <= f0 - 0.25 * step * decrement:
                        break
                step *= 0.5
            else:
                raise RuntimeError("barrier line-search budget exhausted")
            if np.array_equal(xn, x):
                raise RuntimeError("barrier line search cannot make numerical progress")
            x = xn
            steps += 1
        else:
            raise RuntimeError("barrier Newton budget exhausted")
        total += steps
        out.append((t, x.copy(), steps))
    return out, total


# ---------------------------------------------------------------------------------- total unimodularity

def is_totally_unimodular(M, max_k: int | None = None):
    """Exact small-integer minor search. Return (False, witness) on an obstruction,
    (True, None) after all sizes, or (None, None) after an inconclusive partial search."""
    import operator
    M = np.asarray(M, object)
    if M.ndim != 2:
        raise ValueError("TU requires a rectangular integer matrix")
    try:
        rows = [[operator.index(v) for v in row] for row in M]
    except TypeError as exc:
        raise ValueError("TU requires exact integer entries") from exc
    m, n = M.shape
    full = min(m, n)
    K = full if max_k is None else _integer(max_k, "max_k")
    if K > full:
        raise ValueError("max_k exceeds the matrix dimensions")
    for k in range(1, K + 1):
        for R in itertools.combinations(range(m), k):
            for C in itertools.combinations(range(n), k):
                d = _determinant_bareiss([[rows[i][j] for j in C] for i in R])
                if d not in (-1, 0, 1):
                    return False, (R, C, d)
    return (True if K == full else None), None


def bipartite_incidence(edges, nl, nr):
    nl, nr = _integer(nl, "left vertices"), _integer(nr, "right vertices")
    edges = [tuple(_integer(v, "endpoint") for v in edge) for edge in edges]
    if any(len(edge) != 2 or edge[0] >= nl or edge[1] >= nr for edge in edges):
        raise ValueError("bipartite endpoints must belong to their respective sides")
    M = np.zeros((nl + nr, len(edges)), int)
    for k, (u, v) in enumerate(edges):
        M[u, k] = 1
        M[nl + v, k] = 1
    return M


# --------------------------------------------------------------------------------------- integer programming

def knapsack_lp_bound(vals, wts, cap, fixed):
    """Exact fractional upper bound for nonnegative integer values/positive weights."""
    vals, wts, cap = _knapsack_instance(vals, wts, cap)
    fixed = {_integer(i, "item index"): _integer(v, "decision") for i, v in fixed.items()}
    if any(i >= len(vals) or v not in (0, 1) for i, v in fixed.items()):
        raise ValueError("fixed decisions require valid indices and zero or one")
    rem = cap - sum(wts[i] for i, v in fixed.items() if v)
    if rem < 0:
        return -math.inf, None
    value = Fraction(sum(vals[i] for i, v in fixed.items() if v))
    x = {i: Fraction(v) for i, v in fixed.items()}
    free = sorted((i for i in range(len(vals)) if i not in fixed),
                  key=lambda i: (-Fraction(vals[i], wts[i]), i))
    for i in free:
        take = Fraction(min(wts[i], rem), wts[i])
        x[i] = take
        value += vals[i] * take
        rem -= wts[i] * take
    return value, x


def branch_and_bound_knapsack(vals, wts, cap, log: bool = False):
    """Exact integer 0/1 best-first search, with exact rational pruning bounds."""
    import heapq
    vals, wts, cap = _knapsack_instance(vals, wts, cap)
    best, best_x = 0, {i: 0 for i in range(len(vals))}
    root, _ = knapsack_lp_bound(vals, wts, cap, {})
    heap = [(-root, 0, {})]
    nodes, uid, tree = 0, 0, []
    while heap:
        negative_bound, _, fixed = heapq.heappop(heap)
        bound = -negative_bound
        nodes += 1
        if bound <= best:
            if log:
                tree.append({"fixed": dict(fixed), "bound": bound, "fate": "pruned"})
            continue
        bound, x = knapsack_lp_bound(vals, wts, cap, fixed)
        fractional = [i for i, v in x.items() if v not in (0, 1)]
        if not fractional:
            choice = {i: int(v) for i, v in x.items()}
            assert sum(wts[i] * v for i, v in choice.items()) <= cap
            value = sum(vals[i] * v for i, v in choice.items())
            if value > best:
                best, best_x = value, choice
            if log:
                tree.append({"fixed": dict(fixed), "bound": bound, "fate": "integral", "value": value})
            continue
        i = fractional[0]
        if log:
            tree.append({"fixed": dict(fixed), "bound": bound, "fate": "branch", "on": i})
        for decision in (1, 0):
            child = dict(fixed)
            child[i] = decision
            child_bound, _ = knapsack_lp_bound(vals, wts, cap, child)
            if child_bound > best:
                uid += 1
                heapq.heappush(heap, (-child_bound, uid, child))
            elif log:
                tree.append({"fixed": child, "bound": child_bound, "fate": "pruned"})
    return best, best_x, nodes, tree


def knapsack_dp(vals, wts, cap):
    vals, wts, cap = _knapsack_instance(vals, wts, cap)
    best = [0] * (cap + 1)
    for value, weight in zip(vals, wts):
        for capacity in range(cap, weight - 1, -1):
            best[capacity] = max(best[capacity], best[capacity - weight] + value)
    return best[cap]


def knapsack_fptas(vals, wts, cap, eps):
    """Value scaling for the integer domain. Return true value and n*V work model;
    the second result is not an allocated-memory measurement."""
    vals, wts, cap = _knapsack_instance(vals, wts, cap)
    try:
        epsilon = eps if isinstance(eps, Fraction) else Fraction(str(eps))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("epsilon must be in (0, 1]") from exc
    if not 0 < epsilon <= 1:
        raise ValueError("epsilon must be in (0, 1]")
    items = [(v, w) for v, w in zip(vals, wts) if w <= cap and v > 0]
    if not items:
        return 0, 0
    n = len(items)
    scale = epsilon * max(v for v, _ in items) / n
    scaled = [int(Fraction(v) // scale) for v, _ in items]
    V = sum(scaled)
    minw = [0] + [cap + 1] * V
    choice = [()] * (V + 1)
    for i, (_, weight) in enumerate(items):
        for s in range(V, scaled[i] - 1, -1):
            candidate = minw[s - scaled[i]] + weight
            if candidate < minw[s]:
                minw[s] = candidate
                choice[s] = choice[s - scaled[i]] + (i,)
    s = max(s for s in range(V + 1) if minw[s] <= cap)
    assert len(set(choice[s])) == len(choice[s])
    return sum(items[i][0] for i in choice[s]), n * V


# ------------------------------------------------------------------------------------------ approximation

def vertex_cover_exact(n, edges):
    n, edges = _graph(n, edges)
    best = None
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(u in s or v in s for u, v in edges):
                return k, s
    return best


def vertex_cover_matching(n, edges, seed=0):
    n, edges = _graph(n, edges)
    rng = random.Random(seed)
    E = list(edges)
    rng.shuffle(E)
    cover = set()
    for u, v in E:
        if u not in cover and v not in cover:
            cover |= {u, v}
    return cover


def vertex_cover_lp(n, edges):
    n, edges = _graph(n, edges)
    if not edges:
        return 0.0, np.zeros(n), set()
    from scipy.optimize import linprog
    A = np.zeros((len(edges), n))
    for k, (u, v) in enumerate(edges):
        A[k, u] = A[k, v] = -1
    r = linprog(np.ones(n), A_ub=A, b_ub=-np.ones(len(edges)), bounds=[(0, 1)] * n, method="highs")
    if not r.success:
        raise RuntimeError("vertex-cover LP solver failed: " + r.message)
    x = r.x
    return float(r.fun), x, {i for i in range(n) if x[i] >= 0.5 - 1e-9}


def set_cover_greedy(universe, sets):
    U, sets = set(universe), [set(s) for s in sets]
    if U - set().union(*sets):
        raise ValueError("set family does not cover the universe")
    chosen = []
    while U:
        i = max(range(len(sets)), key=lambda k: len(U & sets[k]))
        chosen.append(i)
        U -= sets[i]
    return chosen


def set_cover_exact(universe, sets):
    U, sets = set(universe), [set(s) for s in sets]
    if U - set().union(*sets):
        raise ValueError("set family does not cover the universe")
    for k in range(len(sets) + 1):
        for chosen in itertools.combinations(range(len(sets)), k):
            if set().union(*(sets[i] for i in chosen)) >= U:
                return list(chosen)


def harmonic_bad_set_cover(k: int):
    """The classic instance where greedy pays H_k-ish: two 'rows' cover everything optimally; greedy is lured by columns
    of sizes 2, 4, 8, ...  Universe of size 2(2^k - 1).  Returns (universe, sets, optimum = 2)."""
    k = _integer(k, "trap size", 2)
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
    P, tour = _points(P), [_integer(i, "tour index") for i in tour]
    if any(i >= len(P) for i in tour):
        raise ValueError("tour indices must refer to input points")
    return sum(math.dist(P[tour[i]], P[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))


def held_karp(P):
    """Exact TSP by Held-Karp dynamic programming, O(2^n n^2).  Returns (length, tour)."""
    P = _points(P)
    if len(P) <= 1:
        return 0.0, list(range(len(P)))
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
    P = _points(P)
    if not P:
        return []
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
    P = _points(P)
    if not P:
        return [], []
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
    P, nodes = _points(P), list(nodes)
    nodes = [_integer(i, "matching index") for i in nodes]
    if len(nodes) % 2 or len(set(nodes)) != len(nodes) or any(i >= len(P) for i in nodes):
        raise ValueError("matching requires an even number of distinct valid nodes")
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
    P = _points(P)
    if not P:
        return [], [], (), []
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
    P, tour = _points(P), [_integer(i, "tour index") for i in tour]
    if sorted(tour) != list(range(len(P))):
        raise ValueError("two-opt requires a permutation of all points")
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
    P = _points(P)
    if not P:
        return []
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
    n, edges = _graph(n, edges)
    if n == 0:
        return 0, 0
    best, bs = -1, None
    for mask in range(1 << (n - 1)):
        c = sum(1 for u, v in edges if ((mask >> u) ^ (mask >> v)) & 1)
        if c > best:
            best, bs = c, mask
    return best, bs


def gw_vectors(n, edges, dim=None, iters=3000, lr=0.05, seed=0):
    """Projected-gradient unit vectors and their local primal objective.
    This nonconvex finite solve does not certify an SDP optimum or MAX-CUT upper bound."""
    n, edges = _graph(n, edges)
    k = max(3, int(math.ceil(math.sqrt(2 * n))) + 1) if dim is None else _integer(dim, "dimension", 1)
    iters = _integer(iters, "iterations")
    if not math.isfinite(lr) or lr < 0:
        raise ValueError("learning rate must be finite and nonnegative")
    rng = np.random.default_rng(seed)
    V = rng.standard_normal((n, k))
    if n:
        V /= np.linalg.norm(V, axis=1, keepdims=True)
    E = np.asarray(edges, dtype=int).reshape(-1, 2)
    for _ in range(iters):
        G = np.zeros_like(V)
        np.add.at(G, E[:, 0], V[E[:, 1]])
        np.add.at(G, E[:, 1], V[E[:, 0]])
        V = V - lr * G
        norms = np.linalg.norm(V, axis=1, keepdims=True)
        if not np.isfinite(V).all() or np.any(norms == 0):
            raise RuntimeError("projected-gradient normalization failed")
        V /= norms
    value = float(np.sum((1 - np.sum(V[E[:, 0]] * V[E[:, 1]], axis=1)) / 2))
    return V, value


def gw_round(V, edges, trials=200, seed=1):
    V = np.asarray(V, float)
    if V.ndim != 2 or V.shape[1] == 0 or not np.isfinite(V).all() or np.any(np.linalg.norm(V, axis=1) == 0):
        raise ValueError("rounding requires finite nonzero vectors")
    _, edges = _graph(len(V), edges)
    trials = _integer(trials, "trials", 1)
    E = np.asarray(edges, dtype=int).reshape(-1, 2)
    rng, values = np.random.default_rng(seed), []
    for _ in range(trials):
        side = V @ rng.standard_normal(V.shape[1]) >= 0
        values.append(int(np.sum(side[E[:, 0]] != side[E[:, 1]])))
    return values


def gw_alpha():
    th = np.linspace(1e-4, math.pi, 200001)
    f = 2 * th / (math.pi * (1 - np.cos(th)))
    k = int(np.argmin(f))
    return float(f[k]), float(th[k])


# ------------------------------------------------------------------------------------------ online algorithms

def ski_rental(B, days, strategy="break_even", rng=None):
    """Rent costs 1 a day, buying costs B.  Returns the cost of the strategy when the season lasts ``days``."""
    B, days = _integer(B, "buy cost", 1), _integer(days, "season length")
    if rng is None:
        rng = random.Random()
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
    k = _integer(k, "cache capacity")
    if policy not in ("opt", "marking", "lru", "fifo", "random"):
        raise ValueError("unknown paging policy")
    trace = list(trace)
    if k == 0:
        return len(trace)
    if rng is None:
        rng = random.Random()
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
    """Cumulative expected loss and normalized distributions for losses in [0,1]."""
    L = np.asarray(losses, float)
    if L.ndim != 2 or L.shape[1] == 0 or not np.isfinite(L).all() or np.any((L < 0) | (L > 1)):
        raise ValueError("losses must be a finite T by n array in [0,1], with n>0")
    if not math.isfinite(eta) or eta <= 0:
        raise ValueError("eta must be finite and positive")
    T, n = L.shape
    logw = np.zeros(n)
    algorithm, history = 0.0, []
    for losses_t in L:
        w = np.exp(logw - logw.max())
        distribution = w / w.sum()
        history.append(distribution.copy())
        algorithm += float(distribution @ losses_t)
        with np.errstate(over='raise', invalid='raise'):
            logw -= eta * (losses_t - losses_t.min())
            logw -= logw.max()
    return algorithm, float(L.sum(0).min()), np.array(history).reshape(T, n)


def mw_zero_sum(M, T, eta=None, *, return_column=False):
    """Finite empirical primal/dual game bounds; row payoffs lie in [0,1]."""
    M = np.asarray(M, float)
    if M.ndim != 2 or min(M.shape) == 0 or not np.isfinite(M).all() or np.any((M < 0) | (M > 1)):
        raise ValueError("payoffs must be a nonempty finite matrix in [0,1]")
    T = _integer(T, "rounds", 1)
    m, n = M.shape
    eta = math.sqrt(math.log(m) / T) if eta is None else float(eta)
    if not math.isfinite(eta) or eta < 0:
        raise ValueError("eta must be finite and nonnegative")
    logw, avg_p, avg_q = np.zeros(m), np.zeros(m), np.zeros(n)
    for _ in range(T):
        w = np.exp(logw - logw.max())
        distribution = w / w.sum()
        j = int(np.argmin(distribution @ M))
        avg_p += distribution
        avg_q[j] += 1
        with np.errstate(over='raise', invalid='raise'):
            logw += eta * (M[:, j] - M[:, j].max())
            logw -= logw.max()
    avg_p /= T
    avg_q /= T
    result = (float(np.min(avg_p @ M)), float(np.max(M @ avg_q)), avg_p)
    return (*result, avg_q) if return_column else result
