"""Independent finite references and measurement protocol for Part 23."""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import platform
from collections import deque
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog


def protocol():
    return dict(timer="time.perf_counter", python=platform.python_version(), numpy=np.__version__,
                platform=platform.platform(),
                scope="shared-host observations; generation and independent validation are outside algorithm timers; producer wall time is not an algorithm benchmark")


def vertex_cover_reference(n, edges):
    """Enumerate all masks simultaneously, independently of combination search."""
    masks = np.arange(1 << n, dtype=np.uint64)
    feasible = np.ones(len(masks), dtype=bool)
    for u, v in edges:
        feasible &= (masks & ((1 << u) | (1 << v))) != 0
    return min(int(mask).bit_count() for mask in masks[feasible])


def paging_reference(requests, capacity, policy, seed=0):
    """List-based policy simulator; OPT uses queues of future positions."""
    import random
    from collections import defaultdict
    rng = random.Random(seed)
    future = defaultdict(deque)
    for i, page in enumerate(requests):
        future[page].append(i)
    resident, marked, faults = [], set(), 0
    for i, page in enumerate(requests):
        future[page].popleft()
        if page in resident:
            if policy == 'lru':
                resident.remove(page)
                resident.append(page)
            if policy == 'marking':
                marked.add(page)
            continue
        faults += 1
        if capacity == 0:
            continue
        if len(resident) == capacity:
            if policy == 'opt':
                victim = max(resident, key=lambda v: future[v][0] if future[v] else math.inf)
            elif policy == 'random':
                victim = rng.choice(resident)
            elif policy == 'marking':
                if len(marked) == capacity:
                    marked.clear()
                victim = rng.choice(sorted(set(resident) - marked))
            else:
                victim = resident[0]
            resident.remove(victim)
        resident.append(page)
        if policy == 'marking':
            marked.add(page)
    return faults


def vertex_cover_certificate(n, edges, value, point):
    """Exact half-integral cover and equal fractional-matching dual."""
    x = [F(float(v)).limit_denominator(2) for v in point]
    assert all(abs(float(a) - b) < 1e-8 for a, b in zip(x, point))
    assert min(x, default=F(0)) >= 0 and all(x[u] + x[v] >= 1 for u, v in edges)
    incidence = np.zeros((n, len(edges)))
    for j, (u, v) in enumerate(edges):
        incidence[u, j] = incidence[v, j] = 1
    result = linprog(-np.ones(len(edges)), A_ub=incidence, b_ub=np.ones(n), bounds=(0, None), method='highs')
    assert result.success
    y = [F(float(v)).limit_denominator(2) for v in result.x]
    assert min(y, default=F(0)) >= 0
    assert all(sum(y[j] for j, e in enumerate(edges) if i in e) <= 1 for i in range(n))
    assert sum(x) == sum(y) and abs(float(sum(x)) - value) < 1e-8
    return dict(primal=[str(v) for v in x], dual=[str(v) for v in y], exact_value=str(sum(x)))


def set_cover_reference(universe, sets, feasible_choice):
    """Subset-union DP with an independently verified incumbent cardinality."""
    universe = sorted(set(universe))
    position = {v: i for i, v in enumerate(universe)}
    encoded = [sum(1 << position[v] for v in set(s) if v in position) for s in sets]
    full = (1 << len(universe)) - 1
    cover = 0
    for i in feasible_choice:
        cover |= encoded[i]
    assert cover == full and len(set(feasible_choice)) == len(feasible_choice)
    best = len(feasible_choice)
    unions = [0] * (1 << len(sets))
    for mask in range(1, len(unions)):
        count = mask.bit_count()
        if count >= best:
            continue
        bit = mask & -mask
        unions[mask] = unions[mask ^ bit] | encoded[bit.bit_length() - 1]
        if unions[mask] == full:
            best = count
    return best


def tsp_reference(points):
    """Backward subset recurrence, separate from the instrument's forward DP."""
    from functools import lru_cache
    n = len(points)
    distances = [[math.dist(a, b) for b in points] for a in points]

    @lru_cache(None)
    def finish(last, remaining):
        if not remaining:
            return distances[last][0]
        choices = []
        bits = remaining
        while bits:
            bit = bits & -bits
            bits ^= bit
            node = bit.bit_length() - 1
            choices.append(distances[last][node] + finish(node, remaining ^ bit))
        return min(choices)
    return finish(0, ((1 << n) - 1) ^ 1) if n else 0.0


def tour_certificate(points, tours, optimum, tree, matching, odd):
    """Tour feasibility, independent Kruskal MST and blossom matching weights."""
    import networkx as nx
    n = len(points)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_weighted_edges_from((i, j, math.dist(points[i], points[j]))
                                 for i in range(n) for j in range(i + 1, n))
    expected_tree = nx.minimum_spanning_tree(graph, algorithm='kruskal')
    tree_weight = sum(math.dist(points[u], points[v]) for u, v in tree)
    assert len(tree) == n - 1 and nx.is_tree(nx.Graph(tree))
    assert abs(tree_weight - expected_tree.size(weight='weight')) < 1e-9
    degrees = [sum(i in edge for edge in tree) for i in range(n)]
    assert sorted(odd) == [i for i, d in enumerate(degrees) if d % 2]
    expected_matching = nx.min_weight_matching(graph.subgraph(odd), weight='weight')
    assert sorted(v for e in matching for v in e) == sorted(odd)
    match_weight = sum(math.dist(points[u], points[v]) for u, v in matching)
    assert abs(match_weight - sum(graph[u][v]['weight'] for u, v in expected_matching)) < 1e-9
    lengths = {}
    for name, tour in tours.items():
        assert sorted(tour) == list(range(n))
        lengths[name] = sum(math.dist(points[tour[i]], points[tour[(i + 1) % n]]) for i in range(n))
        assert lengths[name] >= optimum - 1e-9
    assert lengths['double_tree'] <= 2 * optimum + 1e-9
    assert lengths['christofides'] <= 1.5 * optimum + 1e-9
    assert lengths['two_opt'] <= lengths['nn'] + 1e-9
    return dict(lengths=lengths, mst_weight=tree_weight, matching_weight=match_weight,
                scope='Floating Euclidean distances; exact combinatorial enumeration, with1e-9 comparisons; independent Kruskal and blossom references.')


def digest(value):
    def normalize(v):
        if isinstance(v, F):
            return dict(numerator=str(v.numerator), denominator=str(v.denominator))
        if isinstance(v, np.ndarray):
            return dict(dtype=str(v.dtype), shape=list(v.shape), sha256=hashlib.sha256(v.tobytes()).hexdigest())
        if isinstance(v, np.generic):
            return v.item()
        if isinstance(v, dict):
            return {str(k): normalize(x) for k, x in sorted(v.items(), key=lambda kv: str(kv[0]))}
        if isinstance(v, (list, tuple)):
            return [normalize(x) for x in v]
        if isinstance(v, set):
            return sorted((normalize(x) for x in v), key=str)
        return v
    return hashlib.sha256(json.dumps(normalize(value), sort_keys=True, allow_nan=False).encode()).hexdigest()


def solve_exact(matrix, rhs):
    """Rational Gaussian elimination, independently of the tableau instrument."""
    assert len(matrix) == len(rhs) and all(len(row) == len(matrix) for row in matrix)
    A = [[F(float(x)) if isinstance(x, (float, np.floating)) else F(x) for x in row] + [F(y)]
         for row, y in zip(matrix, rhs)]
    n = len(A)
    for k in range(n):
        pivot = next((i for i in range(k, n) if A[i][k]), None)
        if pivot is None:
            raise ValueError("singular certificate system")
        A[k], A[pivot] = A[pivot], A[k]
        value = A[k][k]
        A[k] = [x / value for x in A[k]]
        for i in range(n):
            if i != k:
                multiplier = A[i][k]
                A[i] = [x - multiplier * y for x, y in zip(A[i], A[k])]
    return [row[-1] for row in A]


def lp_certificate(c, A, b, result, exact=False):
    """Independent HiGHS comparison plus primal/dual feasibility and equality checks."""
    reference = linprog(-np.asarray(c, float), A_ub=np.asarray(A, float),
                        b_ub=np.asarray(b, float), bounds=[(0, None)] * len(c), method="highs")
    status = result["status"]
    if status == "unbounded":
        assert reference.status == 3
        return dict(status=status, highs_status=reference.status)
    assert status == "optimal" and reference.success
    if exact:
        x, y = list(map(F, result["x_exact"])), list(map(F, result["duals_exact"]))
        AA, bb, cc = [[F(v) for v in row] for row in A], list(map(F, b)), list(map(F, c))
        assert min(x, default=F(0)) >= 0 and min(y, default=F(0)) >= 0
        assert all(sum(a * v for a, v in zip(row, x)) <= bound for row, bound in zip(AA, bb))
        assert all(sum(AA[i][j] * y[i] for i in range(len(bb))) >= cc[j] for j in range(len(cc)))
        primal, dual = sum(a * v for a, v in zip(cc, x)), sum(a * v for a, v in zip(bb, y))
        assert primal == dual == result["value_exact"]
        assert abs(float(primal) + reference.fun) <= 1e-7 * max(1, abs(float(primal)))
        return dict(status=status, value_exact=str(primal), primal=[str(v) for v in x],
                    dual=[str(v) for v in y], highs_value=float(-reference.fun), exact=True)
    AA, bb, cc = np.asarray(A, float), np.asarray(b, float), np.asarray(c, float)
    x, y = np.asarray(result["x"], float), np.asarray(result["duals"], float)
    assert np.isfinite(x).all() and np.isfinite(y).all()
    tolerance = 1e-7 * max(1.0, float(np.max(np.abs(bb), initial=0)), abs(result["value"]))
    assert np.min(x, initial=0) >= -tolerance and np.min(y, initial=0) >= -tolerance
    assert np.max(AA @ x - bb, initial=0) <= tolerance
    assert np.min(AA.T @ y - cc, initial=0) >= -tolerance
    assert abs(float(cc @ x) - float(bb @ y)) <= tolerance
    assert abs(result["value"] + reference.fun) <= tolerance
    return dict(status=status, highs_value=float(-reference.fun), value=result["value"],
                primal_dual_gap=float(bb @ y - cc @ x), tolerance=tolerance, exact=False)


def halfplane_vertices(A, b, nonnegative=False):
    """Exact small fixed-dimensional vertex enumeration from binary-rational inputs."""
    dimension = len(A[0])
    AA, bb = [[F(v) for v in row] for row in A], list(map(F, b))
    if nonnegative:
        AA += [[-F(int(j == i)) for j in range(dimension)] for i in range(dimension)]
        bb += [F(0)] * dimension
    vertices = set()
    for indices in itertools.combinations(range(len(AA)), dimension):
        try:
            point = solve_exact([AA[i] for i in indices], [bb[i] for i in indices])
        except ValueError:
            continue
        if all(sum(a * x for a, x in zip(row, point)) <= bound for row, bound in zip(AA, bb)):
            vertices.add(tuple(point))
    return sorted(vertices)


def minor_certificate(matrix, verdict, witness):
    """Independent Leibniz expansion for every minor of the small displayed matrix."""
    M = [[int(x) for x in row] for row in matrix]
    m, n = len(M), len(M[0])
    counts, violations = {}, []
    for size in range(1, min(m, n) + 1):
        for rows in itertools.combinations(range(m), size):
            for columns in itertools.combinations(range(n), size):
                determinant = 0
                for permutation in itertools.permutations(range(size)):
                    inversions = sum(permutation[i] > permutation[j]
                                     for i in range(size) for j in range(i + 1, size))
                    product = math.prod(M[rows[i]][columns[permutation[i]]] for i in range(size))
                    determinant += (-1 if inversions % 2 else 1) * product
                counts[str(determinant)] = counts.get(str(determinant), 0) + 1
                if determinant not in (-1, 0, 1):
                    violations.append((rows, columns, determinant))
    assert verdict == (not violations)
    if witness is not None:
        assert (tuple(witness[0]), tuple(witness[1]), witness[2]) in violations
    return dict(minors_checked=sum(counts.values()), determinants=counts,
                violations=[dict(rows=r, columns=c, determinant=d) for r, c, d in violations])


def matching_lp_certificate(vertices, edges, weights, result):
    """Exact primal/dual equality for a proposed half-integral degree-relaxation LP.

    HiGHS supplies a candidate. Half-integral reconstruction must independently
    satisfy nonnegative degree/capacity constraints and dual edge inequalities.
    """
    assert result.success

    def halves(values):
        out = [F(round(2 * float(x)), 2) for x in values]
        assert all(abs(float(a) - float(b)) <= 1e-7 for a, b in zip(out, values))
        return out

    x = halves(result.x)
    y = halves(-result.ineqlin.marginals)
    z = halves(-result.upper.marginals)
    assert len(x) == len(z) == len(edges) == len(weights) and len(y) == vertices
    assert all(0 <= value <= 1 for value in x) and min(y + z, default=F(0)) >= 0
    degree = [F(0)] * vertices
    for value, (u, v), weight, slack in zip(x, edges, weights, z):
        degree[u] += value
        degree[v] += value
        assert y[u] + y[v] + slack >= weight
    assert max(degree, default=F(0)) <= 1
    primal = sum(value * weight for value, weight in zip(x, weights))
    dual = sum(y) + sum(z)
    assert primal == dual and abs(float(primal) + result.fun) <= 1e-7 * max(1, abs(float(primal)))
    return dict(value_exact=str(primal), primal=[str(v) for v in x],
                degree_dual=[str(v) for v in y], capacity_dual=[str(v) for v in z],
                proof="exact nonnegative primal/dual feasibility and equal objectives")


def boundedness_certificate(normals):
    """Exact positive tetrahedron puts zero inside conv(N), excluding recession rays.

    A numerical LP only proposes four normals. Exact binary-rational input values,
    affine independence and strictly positive barycentric weights prove the claim.
    None means uncertified, not a proof of unboundedness.
    """
    N = np.asarray(normals, float)
    assert N.ndim == 2 and N.shape[1] == 3 and np.isfinite(N).all()
    equality = np.vstack([N.T, np.ones(len(N))])
    result = linprog(np.zeros(len(N)), A_eq=equality, b_eq=[0, 0, 0, 1],
                     bounds=[(0, None)] * len(N), method="highs")
    if not result.success:
        return None
    indices = np.flatnonzero(result.x > 1e-9).tolist()
    if len(indices) != 4:
        return None
    try:
        weights = solve_exact(equality[:, indices], [0, 0, 0, 1])
    except ValueError:
        return None
    if min(weights) <= 0:
        return None
    exact = [[F(float(x)) for x in row] for row in N[indices]]
    assert sum(weights) == 1
    assert all(sum(weights[i] * exact[i][j] for i in range(4)) == 0 for j in range(3))
    return dict(indices=indices, normals=[[str(x) for x in row] for row in exact],
                positive_weights=[str(x) for x in weights],
                proof="exact affinely independent positive tetrahedron around zero")


def positive_ldl(matrix):
    """Exact positive Schur-complement pivots certify positive definiteness."""
    A = [list(row) for row in matrix]
    pivots = []
    for k in range(len(A)):
        pivot = A[k][k]
        if pivot <= 0:
            return None
        pivots.append(pivot)
        for i in range(k + 1, len(A)):
            for j in range(i, len(A)):
                A[j][i] = A[i][j] = A[i][j] - A[i][k] * A[j][k] / pivot
    return pivots


def upward_float(value):
    result = float(value)
    return math.nextafter(result, math.inf) if F(result) < value else result


def sdp_dual_certificate(n, edges, vectors):
    """Certify Diag(lambda)-L/4 positive definite, hence MAX-CUT<=sum(lambda).

    The finite projected-gradient objective is a separate local primal observation.
    Approximate eigenvalues propose shifts; exact rational LDL proves feasibility.
    """
    if n == 0:
        assert not edges
        return dict(upper=0.0, upper_exact="0", diagonal=[], positive_pivots=[])
    C = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j in edges:
        assert 0 <= i < n and 0 <= j < n and i != j
        C[i][i] += F(1, 4)
        C[j][j] += F(1, 4)
        C[i][j] -= F(1, 4)
        C[j][i] -= F(1, 4)
    numeric = np.array(C, float)
    V = np.asarray(vectors, float)
    assert V.ndim == 2 and V.shape[0] == n and V.shape[1] > 0 and np.isfinite(V).all()
    lam = np.sum((numeric @ V) * V, axis=1)
    eigenvalue = float(np.linalg.eigvalsh(np.diag(lam) - numeric)[0])
    shift = max(0.0, -eigenvalue) + 1e-9
    for _ in range(12):
        candidate = [F(float(x + shift)) for x in lam]
        S = [[(candidate[i] if i == j else F(0)) - C[i][j] for j in range(n)] for i in range(n)]
        pivots = positive_ldl(S)
        if pivots is not None:
            break
        shift = max(shift * 10, 1e-8)
    else:
        raise ArithmeticError("failed to construct a certified SDP dual bound")
    upper = sum(candidate)
    return dict(upper=upward_float(upper), upper_exact=str(upper),
                diagonal=[str(x) for x in candidate], positive_pivots=[str(x) for x in pivots],
                proof="exact rational positive definiteness of Diag(lambda)-L/4")


def knapsack_reference(values, weights, capacity):
    """Independent vectorized capacity DP with arbitrary-precision integer values."""
    assert len(values) == len(weights) and capacity >= 0 and all(w > 0 for w in weights)
    dp = np.zeros(capacity + 1, dtype=object)
    for value, weight in zip(values, weights):
        if weight <= capacity:
            dp[weight:] = np.maximum(dp[weight:], dp[:-weight] + int(value))
    return int(dp[capacity])


def fractional_knapsack_certificate(values, weights, capacity, bound, solution):
    """Exact feasible fractional solution and equal Lagrangian upper bound."""
    x = [F(solution[i]) for i in range(len(values))]
    assert all(0 <= value <= 1 for value in x)
    used = sum(weight * value for weight, value in zip(weights, x))
    assert used <= capacity
    fractional = [i for i, value in enumerate(x) if 0 < value < 1]
    assert len(fractional) <= 1
    if fractional:
        i = fractional[0]
        multiplier = F(values[i], weights[i])
    else:
        multiplier = max((F(v, w) for v, w, value in zip(values, weights, x) if value == 0), default=F(0))
    assert multiplier >= 0
    primal = sum(value * take for value, take in zip(values, x))
    dual = multiplier * capacity + sum(max(F(0), v - multiplier * w) for v, w in zip(values, weights))
    assert primal == dual == F(bound)
    return dict(bound_exact=str(primal), solution=[str(value) for value in x],
                capacity_multiplier=str(multiplier), used_weight_exact=str(used),
                proof="exact fractional feasibility and equal Lagrangian objective upper bound")


def maxcut_reference(n, edges):
    """Vectorized exhaustive masks, distinct from the instrument's scalar search."""
    assert 0 <= n <= 20
    masks = np.arange(1 << max(0, n - 1), dtype=np.uint32)
    counts = np.zeros(len(masks), dtype=np.int32)
    for i, j in edges:
        counts += ((masks >> i) ^ (masks >> j)) & 1
    return int(counts.max())


def diameter_reference(vertices, edges):
    """All-source BFS independent of the producer's NetworkX diameter/path calls."""
    adjacency = [set() for _ in range(vertices)]
    for u, v in edges:
        assert 0 <= u < vertices and 0 <= v < vertices and u != v
        adjacency[u].add(v)
        adjacency[v].add(u)
    eccentricities, distances = [], []
    for start in range(vertices):
        distance = [-1] * vertices
        distance[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    queue.append(v)
        assert min(distance) >= 0
        eccentricities.append(max(distance))
        distances.append(distance)
    return dict(diameter=max(eccentricities, default=0), eccentricities=eccentricities,
                distance_matrix_sha256=digest(distances), sources=vertices,
                edges=sum(map(len, adjacency)) // 2)


def barrier_certificate(c, A, b, t, point, upper, upper_multipliers):
    """Exact finite objective bound for an approximate barrier point in a proven box.

    Nonnegative row combinations prove x<=upper; explicit -identity rows prove x>=0.
    With y_i=1/(t*s_i), residual r=A^T y-c, the bound is
    b^T y + sum max(0,-r_i)*upper_i. It remains valid away from the exact central point.
    """
    A, b, c = [[F(x) for x in row] for row in A], list(map(F, b)), list(map(F, c))
    x, t, upper = [F(float(x)) for x in point], F(float(t)), list(map(F, upper))
    n, m = len(c), len(b)
    assert len(A) == m and all(len(row) == n for row in A)
    assert len(x) == len(upper) == len(upper_multipliers) == n
    for j, multipliers in enumerate(upper_multipliers):
        z = [F(x) for x in multipliers]
        assert len(z) == m and min(z) >= 0
        assert all(sum(z[i] * A[i][k] for i in range(m)) == int(k == j) for k in range(n))
        assert sum(z[i] * b[i] for i in range(m)) == upper[j]
    for j in range(n):
        assert any(b[i] == 0 and all(A[i][k] == -int(k == j) for k in range(n)) for i in range(m))
    slack = [b[i] - sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]
    assert t > 0 and min(slack) > 0
    y = [1 / (t * s) for s in slack]
    residual = [sum(A[i][j] * y[i] for i in range(m)) - c[j] for j in range(n)]
    bound = sum(b[i] * y[i] for i in range(m)) + sum(max(F(0), -residual[j]) * upper[j] for j in range(n))
    primal = sum(c[j] * x[j] for j in range(n))
    assert bound >= primal
    return dict(primal_exact=str(primal), upper_exact=str(bound), gap_upper=upward_float(bound - primal),
                gap_upper_exact=str(bound - primal), ideal_central_gap=float(F(m) / t),
                residual=[str(r) for r in residual],
                proof="exact positive slack and residual-corrected Lagrangian bound over the certified nonnegative box")
