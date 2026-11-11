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
import argparse
import functools
import hashlib
import json
from pathlib import Path
from fractions import Fraction
from fractions import Fraction as F
from . import measurement_references as R

import numpy as np

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, locked_item
from explainer.cs.algo import optim as O

SOURCE_FILES = (Path(__file__), Path(O.__file__), Path(R.__file__))
SCHEMAS = {name: 2 for name in ('lp', 'simplex', 'duality', 'kleeminty', 'ellipsoid', 'interior',
                               'tu', 'ip', 'approx', 'tsp', 'gw', 'online', 'mw', 'convex', 'frontier')}


def source_signature():
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in SOURCE_FILES}


def cache_current(name, path=None):
    path = CACHE.path(name) if path is None else path
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text())
    except (ValueError, OSError):
        return False
    return data.get('schema') == SCHEMAS[name] and data.get('source_sha256') == source_signature()


class OptimizationCache(Cache):
    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if not cache_current(name, self.path(name)):
            self.save(name, ITEMS[name]())
        return super().load(name)

    def main(self, items, doc=None):
        parser = argparse.ArgumentParser(description=doc)
        parser.add_argument('names', nargs='*', default=list(items))
        parser.add_argument('--force', action='store_true')
        arguments = parser.parse_args()
        if any(name not in items for name in arguments.names):
            parser.error('unknown producer; choose from ' + ', '.join(items))
        self.items = items
        for name in arguments.names:
            with cache_lock(self.path(name)):
                if not arguments.force and cache_current(name):
                    print(f'  cached  {name}', flush=True)
                    continue
                print(f'  compute {name} ...', flush=True)
                self.save(name, items[name]())
                print(f'  done    {name}', flush=True)


CACHE = OptimizationCache("cs23")
load = CACHE.load

C3 = [5, 4, 3]
A3 = [[2, 3, 1], [4, 1, 2], [3, 4, 2]]
B3 = [5, 11, 8]


def _measure(operation, function, repeats=3):
    samples, hashes, output = [], [], None
    for _ in range(repeats):
        start = time.perf_counter()
        output = function()
        samples.append(time.perf_counter() - start)
        hashes.append(R.digest(output))
    assert len(set(hashes)) == 1
    return output, min(samples), dict(operation=operation, samples=samples, repeats=repeats,
                                      statistic='minimum', seconds=min(samples), output_sha256=hashes,
                                      validation='output hashes and independent references checked after timers')


def compute_lp() -> dict:
    vertices = O.vertices_3d(A3, B3)
    faces = O.hull_faces_3d(vertices)
    exact_vertices = R.halfplane_vertices(A3, B3, nonnegative=True)
    assert len(vertices) == len(exact_vertices) == 6
    assert all(any(np.allclose(v, list(map(float, exact)), atol=1e-10, rtol=0)
                   for exact in exact_vertices) for v in vertices)
    values = [sum(c * x for c, x in zip(C3, v)) for v in vertices]
    index = int(np.argmax(values))
    assert max(sum(F(c) * x for c, x in zip(C3, v)) for v in exact_vertices) == 13
    from scipy.optimize import linprog
    supply, demand, cost = [30, 40], [20, 25, 25], [[4, 6, 9], [5, 3, 8]]
    objective = [cost[i][j] for i in range(2) for j in range(3)]
    capacity = [[int(k // 3 == i) for k in range(6)] for i in range(2)]
    destinations = [[int(k % 3 == j) for k in range(6)] for j in range(3)]
    result = linprog(objective, A_ub=capacity, b_ub=supply, A_eq=destinations, b_eq=demand, method='highs')
    assert result.success
    ship = [[round(float(result.x[3 * i + j]), 6) for j in range(3)] for i in range(2)]
    assert all(sum(ship[i]) <= supply[i] for i in range(2))
    assert all(sum(ship[i][j] for i in range(2)) == demand[j] for j in range(3))
    alpha, beta = [0, -1], [4, 4, 9]
    assert all(alpha[i] + beta[j] <= cost[i][j] for i in range(2) for j in range(3))
    dual = sum(a * s for a, s in zip(alpha, supply)) + sum(b * d for b, d in zip(beta, demand))
    total = sum(F(amount) * cost[i][j] for i, row in enumerate(ship) for j, amount in enumerate(row))
    assert total == dual == 365
    naive = sum(min(cost[i][j] for i in range(2)) * demand[j] for j in range(3))
    transport = dict(supply=supply, demand=demand, cost=cost, ship=ship, total=float(total), naive=naive,
                     exact_dual=dict(supply=alpha, demand=beta, value=dual))
    active = [{i for i, (row, bound) in enumerate(list(zip(A3, B3)) + [([-int(j == k) for j in range(3)], 0) for k in range(3)])
               if sum(F(a) * x for a, x in zip(row, v)) == bound} for v in exact_vertices]
    true_edges = [(i, j) for i in range(len(exact_vertices)) for j in range(i + 1, len(exact_vertices))
                  if len(active[i] & active[j]) >= 2]
    return dict(c=C3, A=A3, b=B3, vertices=vertices, faces=faces, values=values,
                opt=vertices[index], opt_value=values[index], transport=transport,
                exact_vertices=[[str(x) for x in v] for v in exact_vertices],
                exact_vertex_order_edges=true_edges,
                reference_scope='All six vertices independently enumerated by exact rational plane intersections. Transport primal shipment and exact signed supply/demand dual both equal365; capacity-ignoring355 is a lower observation, not a feasible shipment.')


def compute_simplex() -> dict:
    out = {}
    for rule in ("dantzig", "bland"):
        r = O.simplex(C3, A3, B3, rule=rule, exact=True)
        out[rule] = {"path": r["path"], "pivots": r["pivots"], "value": r["value"], "certificate": R.lp_certificate(C3, A3, B3, r, exact=True)}
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
    basis_certificates = []
    augmented = [[F(v) for v in row] + [F(int(i == j)) for j in range(m)] for i, row in enumerate(A3)]
    costs = list(map(F, C3)) + [F(0)] * m
    for index, tableau in enumerate(tabs):
        basis = tableau['basis']
        matrix = [[row[j] for j in basis] for row in augmented]
        expected = [[F(0)] * (n + m + 1) for _ in range(m)]
        for column in range(n + m + 1):
            rhs = [F(v) for v in B3] if column == n + m else [row[column] for row in augmented]
            solution = R.solve_exact(matrix, rhs)
            for i, value in enumerate(solution):
                expected[i][column] = value
        actual = [[F(v) for v in row] for row in tableau['T']]
        assert actual == expected
        dual = R.solve_exact(list(map(list, zip(*matrix))), [costs[j] for j in basis])
        expected_z = [sum(dual[i] * augmented[i][j] for i in range(m)) - costs[j] for j in range(n + m)]
        expected_z.append(sum(dual[i] * B3[i] for i in range(m)))
        assert list(map(F, tableau['z'])) == expected_z
        point = [F(0)] * n
        for i, variable in enumerate(basis):
            if variable < n:
                point[variable] = actual[i][-1]
        assert all(abs(float(a) - b) < 1e-12 for a, b in zip(point, out['dantzig']['path'][index]))
        basis_certificates.append(dict(basis=basis, point=[str(x) for x in point],
                                       objective=str(expected_z[-1]), reduced_costs=[str(x) for x in expected_z[:-1]]))
    out['basis_certificates'] = basis_certificates
    out['reference_scope'] = 'All tableau columns and reduced costs independently reconstructed from exact basis systems; both actual instrument paths have separate exact primal/dual certificates.'
    out["tableaux"] = tabs
    return out



def compute_duality() -> dict:
    result = O.simplex(C3, A3, B3, exact=True)
    certificate = R.lp_certificate(C3, A3, B3, result, exact=True)
    y = result['duals']
    family = []
    for multipliers in ([F(3), F(0), F(0)], [F(0), F(0), F(5, 3)],
                         [F(0), F(5, 4), F(0)], [F(1), F(0), F(1)]):
        feasible = min(multipliers) >= 0 and all(sum(A3[i][j] * multipliers[i] for i in range(3)) >= C3[j] for j in range(3))
        bound = sum(a * b for a, b in zip(multipliers, B3))
        family.append(dict(y=list(map(float, multipliers)), bound=float(bound), feasible=feasible,
                           y_exact=[str(x) for x in multipliers], bound_exact=str(bound)))
    shadow, perturbations = [], []
    for i in range(3):
        bounds = list(B3)
        bounds[i] += 1
        changed = O.simplex(C3, A3, bounds, exact=True)
        checked = R.lp_certificate(C3, A3, bounds, changed, exact=True)
        delta = changed['value_exact'] - result['value_exact']
        shadow.append(float(delta))
        perturbations.append(dict(resource=i, b=bounds, finite_change_exact=str(delta), certificate=checked))
    x = result['x']
    slack = [B3[i] - sum(A3[i][j] * x[j] for j in range(3)) for i in range(3)]
    reduced = [sum(A3[i][j] * y[i] for i in range(3)) - C3[j] for j in range(3)]
    assert all(abs(a * b) < 1e-12 for a, b in zip(slack, y))
    assert all(abs(a * b) < 1e-12 for a, b in zip(reduced, x))
    return dict(x=x, value=result['value'], y=y, family=family, shadow=shadow, slack=slack, reduced=reduced,
                certificate=certificate, perturbations=perturbations,
                reference_scope='Exact primal/dual feasibility and complementary slackness; every one-unit resource perturbation independently certified. Finite changes need not equal an infinitesimal shadow price across a basis change.')


def compute_kleeminty() -> dict:
    rows, cube_trials = [], []
    for n in range(2, 13):
        c, A, b = O.klee_minty(n)
        row = dict(n=n)
        for rule in ('dantzig', 'bland', 'steepest'):
            result = O.simplex(c, A, b, rule=rule, exact=True)
            certificate = R.lp_certificate(c, A, b, result, exact=True)
            assert result['value_exact'] == 5 ** n
            assert len(result['path']) == result['pivots'] + 1
            path = []
            for point in result['path']:
                assert all(value == int(value) for value in point)
                point = tuple(map(int, point))
                assert min(point) >= 0
                assert all(sum(a * x for a, x in zip(constraint, point)) <= bound
                           for constraint, bound in zip(A, b))
                assert all(point[j] == 0 or sum(A[j][i] * point[i] for i in range(n)) == b[j]
                           for j in range(n))
                path.append(point)
            assert len(set(path)) == len(path)
            objectives = [sum(a * x for a, x in zip(c, point)) for point in path]
            assert all(after > before for before, after in zip(objectives, objectives[1:]))
            if rule == 'dantzig':
                assert result['pivots'] == 2 ** n - 1
            row[rule] = result['pivots']
            cube_trials.append(dict(n=n, rule=rule, pivots=result['pivots'],
                                    vertices_checked=len(path), path_sha256=R.digest(path), certificate=certificate))
        rows.append(row)
    c, A, b = O.klee_minty(3)
    vertices = O.vertices_3d(A, b)
    exact_vertices = R.halfplane_vertices(A, b, nonnegative=True)
    assert len(vertices) == len(exact_vertices) == 8
    assert all(any(np.allclose(vertex, list(map(float, exact)), atol=1e-10, rtol=0)
                   for exact in exact_vertices) for vertex in vertices)
    path = O.simplex(c, A, b, exact=True)['path']
    rng = np.random.default_rng(1)
    perturbed, perturbation_trials = [], []
    dimension = 10
    c, A, b = O.klee_minty(dimension)
    for sigma in (0.0, 1e-4, 1e-3, 1e-2, 1e-1, 0.3):
        pivots, unbounded = [], 0
        for trial in range(20 if sigma else 1):
            matrix = (np.array(A, float) * (1 + sigma * rng.standard_normal((dimension, dimension)))).tolist()
            result = O.simplex(c, matrix, b)
            certificate = R.lp_certificate(c, matrix, b, result)
            if result['status'] == 'optimal':
                pivots.append(result['pivots'])
            else:
                assert result['status'] == 'unbounded'
                unbounded += 1
            perturbation_trials.append(dict(sigma=sigma, trial=trial, c=c, A=matrix, b=b,
                                             pivots=result['pivots'], status=result['status'], certificate=certificate))
        assert pivots
        perturbed.append(dict(sigma=sigma, mean=float(np.mean(pivots)), max=max(pivots),
                              optimal_trials=len(pivots), unbounded_trials=unbounded))
    random_rows, random_trials = [], []
    random_rng = random.Random(2)
    for n in (5, 10, 20, 40, 80):
        pivots = []
        for trial in range(20):
            c2, A2, b2 = O.random_lp(n, 2 * n, random_rng)
            result = O.simplex(c2, A2, b2)
            certificate = R.lp_certificate(c2, A2, b2, result)
            assert result['status'] == 'optimal'
            pivots.append(result['pivots'])
            random_trials.append(dict(n=n, trial=trial, c=c2, A=A2, b=b2,
                                       pivots=result['pivots'], certificate=certificate))
        random_rows.append(dict(n=n, m=2 * n, mean=float(np.mean(pivots)), max=max(pivots), trials=20))
    return dict(rows=rows, cube_vertices=vertices, cube_faces=O.hull_faces_3d(vertices), cube_path=path,
                cube_trials=cube_trials, perturbed=perturbed, perturbation_trials=perturbation_trials,
                perturbed_n=dimension, random=random_rows, random_trials=random_trials,
                reference_scope='All33 displayed rule/dimension trials use exact arithmetic, distinct feasible integer cube vertices, increasing objectives and exact primal/dual certificates. All201 floating random/perturbed LPs are independently checked by HiGHS. The multiplicative zero-preserving Dantzig experiment is separate from additive-Gaussian two-phase shadow-vertex smoothed analysis.')


def compute_ellipsoid() -> dict:
    A = np.array([[1.0, 1.0], [-1.0, 2.0], [-2.0, -1.0], [1.0, -2.0]])
    target = np.array([2.2, 1.5])
    normal_indices = [0, 2, 3]
    normal_weights = R.solve_exact([[F(A[i, j]) for i in normal_indices] for j in range(2)]
                                   + [[1, 1, 1]], [0, 0, 1])
    assert min(normal_weights) > 0
    trials = []
    for width in (0.25, 1.0, 0.1, 0.01, 1e-3, 1e-4, 1e-5, 1e-6):
        b = A @ target + width * np.linalg.norm(A, axis=1)
        vertices = R.halfplane_vertices(A.tolist(), b.tolist())
        assert len(vertices) == 4
        norm2 = [sum(x * x for x in point) for point in vertices]
        assert max(norm2) <= 36
        exact_target = [F(float(v)) for v in target]
        assert all(sum(F(a) * x for a, x in zip(row, exact_target)) < F(bound)
                   for row, bound in zip(A.tolist(), b.tolist()))
        point, steps, trail = O.ellipsoid_feasible(A, b, R=6.0, log=True)
        assert point is not None and np.max(A @ point - b) <= 0
        determinants = [float(np.linalg.det(shape)) for _, shape in trail]
        assert min(determinants) > 0
        ratios = [math.sqrt(after / before) for before, after in zip(determinants, determinants[1:])]
        assert all(ratio <= math.exp(-1 / 6) * (1 + 1e-8) for ratio in ratios)
        trials.append(dict(width=width, b=b.tolist(), x=point.tolist(), steps=steps,
                           trail=[dict(c=center.tolist(), P=shape.tolist()) for center, shape in trail],
                           enclosure=dict(radius=6, maximum_vertex_norm2_exact=str(max(norm2)),
                                          exact_vertices=[[str(v) for v in point] for point in vertices],
                                          positive_normal_indices=normal_indices,
                                          positive_normal_weights=[str(w) for w in normal_weights]),
                           volume_ratios=ratios, maximum_float_constraint_violation=float(np.max(A @ point - b))))
    main = trials[0]
    return dict(A=A.tolist(), b=main['b'], target=target.tolist(), x=main['x'],
                steps=main['steps'], trail=main['trail'],
                rows=[dict(width=trial['width'], steps=trial['steps']) for trial in trials[1:]],
                shrink2d=math.exp(-1 / 6), exact_arithmetic_area_factor=4 / (3 * math.sqrt(3)),
                trials=trials,
                reference_scope='Eight exact bounded-region/enclosure certificates, including every displayed width. All returned centres and shapes are finite numerical observations; observed determinant area ratios are distinct from the exp(-1/6) theoretical upper bound. A finite budget is not an infeasibility certificate.')


def compute_interior() -> dict:
    A = [[1, 2], [3, 1], [-1, 0], [0, -1], [1, -1], [-1, 3]]
    b, c = [8, 9, 0, 0, 2, 9], [1, 1]
    ts = [0.02 * 1.5 ** k for k in range(36)]
    path, total = O.barrier_path(c, A, b, ts=ts, x0=[0.5, 0.5])
    from scipy.optimize import linprog
    reference = linprog([-1, -1], A_ub=A, b_ub=b, method='highs')
    assert reference.success and abs(-reference.fun - 5) < 1e-10
    optimum, dual = [F(2), F(3)], [F(2, 5), F(1, 5), F(0), F(0), F(0), F(0)]
    assert all(sum(F(a) * x for a, x in zip(row, optimum)) <= bound for row, bound in zip(A, b))
    assert all(sum(dual[i] * A[i][j] for i in range(len(A))) == c[j] for j in range(2))
    assert sum(dual[i] * b[i] for i in range(len(A))) == 5
    points = []
    for t, x, steps in path:
        certificate = R.barrier_certificate(c, A, b, t, x, [3, 4],
                                             [[0, '1/3', 0, '1/3', 0, 0], ['1/2', 0, '1/2', 0, 0, 0]])
        assert F(certificate['primal_exact']) <= 5 <= F(certificate['upper_exact'])
        points.append(dict(t=t, x=x.tolist(), steps=steps, gap=certificate['gap_upper'],
                           central_gap_target=len(b) / t, certificate=certificate))
    return dict(A=A, b=b, c=c, path=points, total_newton=total, opt=[2.0, 3.0], opt_value=5.0,
                exact_optimum=['2', '3'], exact_dual=[str(x) for x in dual],
                reference_scope='Exact primal/dual optimum5; every approximate Newton point has a residual-corrected exact rational objective upper bound over a proven box. m/t is retained separately as the ideal central-point target.')


def compute_tu() -> dict:
    from scipy.optimize import linprog
    import networkx as nx
    edges = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 2)]
    M = O.bipartite_incidence(edges, 3, 3)
    tu, witness = O.is_totally_unimodular(M)
    small_certificate = R.minor_certificate(M, tu, witness)
    triangle = np.array([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
    tu_triangle, witness_triangle = O.is_totally_unimodular(triangle)
    triangle_certificate = R.minor_certificate(triangle, tu_triangle, witness_triangle)
    triangle_lp = linprog(-np.ones(3), A_ub=triangle, b_ub=np.ones(3),
                          bounds=[(0, 1)] * 3, method='highs-ds')
    triangle_dual = R.matching_lp_certificate(3, [(0, 1), (1, 2), (0, 2)], [1, 1, 1], triangle_lp)
    rng = np.random.default_rng(3)
    fractional_bipartite, fractional_general, trials = 0, 0, []
    for trial in range(100):
        left = right = 8
        E = [(i, j) for i in range(left) for j in range(right) if rng.random() < 0.4]
        matrix = O.bipartite_incidence(E, left, right)
        weights = rng.integers(1, 20, len(E)).tolist()
        result = linprog(-np.array(weights), A_ub=matrix, b_ub=np.ones(left + right),
                         bounds=[(0, 1)] * len(E), method='highs-ds')
        global_edges = [(i, left + j) for i, j in E]
        certificate = R.matching_lp_certificate(left + right, global_edges, weights, result)
        fractional_bipartite += int(np.any(np.abs(result.x - np.round(result.x)) > 1e-7))
        graph = nx.Graph()
        graph.add_weighted_edges_from((u, v, weight) for (u, v), weight in zip(global_edges, weights))
        matching = nx.max_weight_matching(graph, weight='weight')
        matching_value = sum(graph[u][v]['weight'] for u, v in matching)
        assert F(certificate['value_exact']) == matching_value
        n = 16
        general_edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]
        general_matrix = np.zeros((n, len(general_edges)), int)
        for k, (u, v) in enumerate(general_edges):
            general_matrix[u, k] = general_matrix[v, k] = 1
        general_weights = rng.integers(1, 20, len(general_edges)).tolist()
        general_result = linprog(-np.array(general_weights), A_ub=general_matrix, b_ub=np.ones(n),
                                 bounds=[(0, 1)] * len(general_edges), method='highs-ds')
        general_certificate = R.matching_lp_certificate(n, general_edges, general_weights, general_result)
        fractional_general += int(np.any(np.abs(general_result.x - np.round(general_result.x)) > 1e-7))
        general_graph = nx.Graph()
        general_graph.add_weighted_edges_from((u, v, weight) for (u, v), weight in zip(general_edges, general_weights))
        integer_matching = nx.max_weight_matching(general_graph, weight='weight')
        integer_value = sum(general_graph[u][v]['weight'] for u, v in integer_matching)
        assert F(general_certificate['value_exact']) >= integer_value
        trials.append(dict(trial=trial, bipartite=dict(E=global_edges, weights=weights,
                                                      certificate=certificate, matching_value=matching_value,
                                                      matching=[list(edge) for edge in matching]),
                           general=dict(E=general_edges, weights=general_weights,
                                        certificate=general_certificate, integer_matching_value=integer_value,
                                        matching=[list(edge) for edge in integer_matching])))
    assert fractional_bipartite == 0
    return dict(edges=edges, M=M.tolist(), tu=tu, small_minor_certificate=small_certificate,
                tri=triangle.tolist(), tu_tri=tu_triangle, tri_witness_det=witness_triangle[2],
                triangle_minor_certificate=triangle_certificate, triangle_dual_certificate=triangle_dual,
                tri_lp=triangle_lp.x.tolist(), tri_lp_value=-triangle_lp.fun,
                frac_bipartite=fractional_bipartite, frac_general=fractional_general,
                trials=100, matching_trials=trials,
                reference_scope='Every minor of the two small displayed integer matrices checked by independent permutation determinants. All200 weighted degree-relaxation LPs have exact reconstructed primal/dual certificates; bipartite values also match independent integer weighted matching. No full minor enumeration of the large random matrices is claimed.')


def compute_ip() -> dict:
    rng = random.Random(11)
    values = [rng.randint(10, 60) for _ in range(8)]
    weights = [rng.randint(5, 40) for _ in range(8)]
    capacity = 80
    best, choice, nodes, tree = O.branch_and_bound_knapsack(values, weights, capacity, log=True)
    root, root_solution = O.knapsack_lp_bound(values, weights, capacity, {})
    root_certificate = R.fractional_knapsack_certificate(values, weights, capacity, root, root_solution)
    assert best == R.knapsack_reference(values, weights, capacity)
    assert sum(weights[i] * take for i, take in choice.items()) <= capacity
    for node in tree:
        node['bound_exact'] = str(node['bound'])
        if not math.isfinite(node['bound']):
            assert node['bound'] == -math.inf
            node['bound'], node['bound_status'] = None, 'infeasible'
    rows, trials = [], []
    for n in (20, 40, 80, 160):
        node_counts, gaps = [], []
        for trial in range(10):
            v = [rng.randint(10, 100) for _ in range(n)]
            w = [rng.randint(10, 100) for _ in range(n)]
            cap = sum(w) // 3
            optimum, selected, visited, _ = O.branch_and_bound_knapsack(v, w, cap)
            bound, fractional = O.knapsack_lp_bound(v, w, cap, {})
            certificate = R.fractional_knapsack_certificate(v, w, cap, bound, fractional)
            assert optimum == R.knapsack_reference(v, w, cap)
            assert sum(w[i] * take for i, take in selected.items()) <= cap
            assert sum(v[i] * take for i, take in selected.items()) == optimum
            node_counts.append(visited)
            gaps.append(bound / optimum - 1)
            trials.append(dict(n=n, trial=trial, values=v, weights=w, capacity=cap,
                               optimum=optimum, choice=selected, nodes=visited,
                               fractional_certificate=certificate, gap_exact=str(gaps[-1])))
        rows.append(dict(n=n, nodes_mean=float(np.mean(node_counts)), nodes_max=max(node_counts),
                         subsets=2 ** n, gap=float(np.mean(gaps))))
    correlated_rng = random.Random(5)
    w = [correlated_rng.randint(100, 1000) for _ in range(20)]
    v = [weight + 100 for weight in w]
    cap = sum(w) // 2
    optimum, dp_seconds, dp_trial = _measure('integer capacity DP, n20', lambda: O.knapsack_dp(v, w, cap))
    assert optimum == R.knapsack_reference(v, w, cap)
    timings, approximations = [dp_trial], []
    for epsilon in (0.9, 0.5, 0.2, 0.1, 0.05, 0.02):
        (value, work), seconds, trial = _measure(f'value-scaling FPTAS epsilon={epsilon}',
                                                lambda epsilon=epsilon: O.knapsack_fptas(v, w, cap, epsilon))
        assert F(str(1)) - F(str(epsilon)) <= F(value, optimum) <= 1
        timings.append(trial)
        approximations.append(dict(eps=epsilon, ratio=value / optimum, value=value,
                                   table=work, seconds=seconds,
                                   table_scope='n*V upper model of DP work, not allocated-memory entries'))
    return dict(vals=values, wts=weights, cap=capacity, best=best, x=choice, nodes=nodes,
                tree=tree, root=float(root), root_exact=str(root), root_certificate=root_certificate,
                rows=rows, integer_trials=trials, fptas=approximations, fptas_n=20,
                dp_seconds=dp_seconds, dp_cap=cap, fptas_opt=optimum,
                fptas_instance=dict(values=v, weights=w, capacity=cap), timed_trials=timings,
                reference_scope='All41 exact integer optima independently checked by vectorized arbitrary-precision capacity DP. Every root fractional bound has an exact Lagrangian certificate. FPTAS outputs meet the exact guarantee; all timing inputs are prepared before the clock and checked after it.')


def compute_approx() -> dict:
    rng = random.Random(21)

    def cover_case(n, edges, seed):
        opt, optimal = O.vertex_cover_exact(n, edges)
        matching = O.vertex_cover_matching(n, edges, seed=seed)
        lp, point, rounded = O.vertex_cover_lp(n, edges)
        assert opt == R.vertex_cover_reference(n, edges)
        for cover in (optimal, matching, rounded):
            assert all(u in cover or v in cover for u, v in edges)
        assert len(matching) <= 2 * opt and len(rounded) <= 2 * lp + 1e-8
        certificate = R.vertex_cover_certificate(n, edges, lp, point)
        return dict(n=n, E=edges, seed=seed, opt=opt, opt_set=sorted(optimal),
                    matching=len(matching), matching_set=sorted(matching), lp=lp, x=point.tolist(),
                    rounded=len(rounded), rounded_set=sorted(rounded), half=int(np.sum(np.abs(point - .5) < 1e-8)),
                    certificate=certificate)

    vc = []
    for _ in range(100):
        edges = [(i, j) for i in range(16) for j in range(i + 1, 16) if rng.random() < .25]
        assert edges
        vc.append(cover_case(16, edges, rng.randint(0, 999)))
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3), (5, 6), (6, 7), (7, 8), (8, 6), (1, 4), (7, 4)]
    draw = cover_case(9, edges, 3)
    draw['matching'] = draw.pop('matching_set')
    draw['rounded'] = draw.pop('rounded_set')

    def set_case(universe, sets):
        greedy, exact = O.set_cover_greedy(universe, sets), O.set_cover_exact(universe, sets)
        optimum = R.set_cover_reference(universe, sets, exact)
        assert len(exact) == optimum
        assert set().union(*(sets[i] for i in greedy)) >= set(universe)
        harmonic = sum(F(1, k) for k in range(1, len(universe) + 1))
        assert len(greedy) <= harmonic * optimum
        return dict(n=len(universe), universe=universe, sets=[sorted(v) for v in sets],
                    greedy=len(greedy), greedy_choice=greedy, opt=optimum, exact_choice=exact,
                    maxsize=max(map(len, sets)), harmonic_bound=str(harmonic))

    traps = []
    for k in range(2, 8):
        universe, sets, claimed = O.harmonic_bad_set_cover(k)
        row = set_case(universe, sets)
        assert row['opt'] == claimed == 2
        traps.append(dict(k=k, **row))
    random_cases = []
    for _ in range(60):
        universe = list(range(30))
        sets = [set(rng.sample(universe, rng.randint(2, 8))) for _ in range(18)]
        sets.append(set(universe) - set().union(*sets) or {0})
        random_cases.append(set_case(universe, sets))
    return dict(vc=vc, draw=draw, setcover=traps, random_setcover=random_cases,
                reference_scope='All101 vertex-cover optima independently checked by vectorized mask enumeration and exact LP primal/dual certificates; all66 set-cover optima checked by separate subset-union DP. Full instances and feasible choices retained.')


def compute_tsp() -> dict:
    rng = random.Random(34)

    def small_case(points):
        optimum, tour = O.held_karp(points)
        assert abs(optimum - R.tsp_reference(points)) < 1e-9
        double, tree = O.double_tree(points)
        christofides, tree2, matching, odd = O.christofides(points)
        assert tree == tree2
        nearest = O.nearest_neighbour_tour(points)
        improved, moves = O.two_opt(points, nearest)
        tours = dict(tour=tour, double_tree=double, christofides=christofides, nn=nearest, two_opt=improved)
        certificate = R.tour_certificate(points, tours, optimum, tree, matching, odd)
        assert abs(certificate['lengths']['tour'] - optimum) < 1e-9
        lengths = certificate['lengths']
        lengths['opt'] = optimum
        return dict(P=points, opt=optimum, **tours, mst=tree, matching=list(matching), odd=odd,
                    moves=moves, lengths=lengths, certificate=certificate)

    points = [(round(rng.uniform(0, 10), 3), round(rng.uniform(0, 6), 3)) for _ in range(13)]
    draw = small_case(points)
    cases = [small_case([(rng.random(), rng.random()) for _ in range(12)]) for _ in range(40)]
    summary = {}
    for name in ('double_tree', 'christofides', 'nn', 'two_opt'):
        ratios = [case['lengths'][name] / case['opt'] for case in cases]
        summary[name] = dict(mean=float(np.mean(ratios)), max=max(ratios))
    big, timings = [], []
    for n in (100, 300):
        points = [(rng.random(), rng.random()) for _ in range(n)]
        nearest = O.nearest_neighbour_tour(points)
        (improved, moves), seconds, timing = _measure(f'two_opt_{n}', lambda: O.two_opt(points, nearest))
        timings.append(timing)
        assert sorted(improved) == list(range(n))
        before = sum(math.dist(points[nearest[i]], points[nearest[(i + 1) % n]]) for i in range(n))
        after = sum(math.dist(points[improved[i]], points[improved[(i + 1) % n]]) for i in range(n))
        assert after <= before + 1e-9
        big.append(dict(n=n, P=points, nn_tour=nearest, two_opt_tour=improved, nn=before, two_opt=after,
                        moves=moves, seconds=seconds, bhh=.7124 * math.sqrt(n)))
    points = [(rng.random(), rng.random()) for _ in range(15)]
    (optimum, tour), seconds, timing = _measure('held_karp_15', lambda: O.held_karp(points))
    timings.append(timing)
    assert abs(optimum - R.tsp_reference(points)) < 1e-9
    assert sorted(tour) == list(range(15))
    return dict(draw=draw, summary=summary, trials=len(cases), cases=cases, big=big, t_hk15=seconds,
                held_karp_timing_instance=dict(P=points, optimum=optimum, tour=tour), timed_trials=timings,
                reference_scope='All42 small TSP optima independently checked by backward subset recurrence;41 complete approximation cases checked against Kruskal MST and blossom matching. Euclidean lengths use floating arithmetic.0.7124sqrt(n) is an asymptotic numerical prediction for uniform planar points, not a finite-instance certificate. Three repeated timing groups exclude generation and validation.')


def compute_gw() -> dict:
    graph_rng, cut_rng = random.Random(41), random.Random(42)
    n = 12
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if graph_rng.random() < 0.35]
    exact, mask = O.maxcut_exact(n, E)
    assert exact == R.maxcut_reference(n, E)
    V3, local3 = O.gw_vectors(n, E, dim=3, iters=4000)
    V, local = O.gw_vectors(n, E)
    certificate3 = R.sdp_dual_certificate(n, E, V3)
    certificate = R.sdp_dual_certificate(n, E, V)
    assert F(certificate['upper_exact']) >= exact
    rounds = O.gw_round(V, E, trials=500)
    assert all(0 <= cut <= exact for cut in rounds)
    rows = []
    for trial in range(30):
        m = 16
        edges = [(i, j) for i in range(m) for j in range(i + 1, m) if graph_rng.random() < 0.4]
        optimum, exact_mask = O.maxcut_exact(m, edges)
        assert optimum == R.maxcut_reference(m, edges)
        vectors, objective = O.gw_vectors(m, edges)
        dual = R.sdp_dual_certificate(m, edges, vectors)
        assert F(dual['upper_exact']) >= optimum
        rounded = O.gw_round(vectors, edges, trials=200, seed=100 + trial)
        random_cuts = []
        for _ in range(200):
            side = [cut_rng.getrandbits(1) for _ in range(m)]
            random_cuts.append(sum(side[u] != side[v] for u, v in edges))
        assert all(0 <= cut <= optimum for cut in rounded + random_cuts)
        rows.append(dict(n=m, E=edges, exact=optimum, exact_mask=exact_mask,
                         sdp=dual['upper'], sdp_local=objective, sdp_certificate=dual,
                         vectors=vectors.tolist(), gw_samples=rounded,
                         gw_mean=float(np.mean(rounded)), gw_best=max(rounded),
                         random_samples=random_cuts, random_mean=float(np.mean(random_cuts)),
                         edges=len(edges)))
    alpha, theta = O.gw_alpha()
    from scipy.optimize import brentq
    theta_reference = brentq(lambda x: math.tan(x / 2) - x, 2, 2.8)
    alpha_reference = 2 * theta_reference / (math.pi * (1 - math.cos(theta_reference)))
    assert abs(alpha - alpha_reference) < 1e-8
    return dict(n=n, E=E, exact=exact, exact_mask=mask, V3=V3.tolist(), vectors=V.tolist(),
                sdp3=certificate3['upper'], sdp3_local=local3, sdp3_certificate=certificate3,
                sdp=certificate['upper'], sdp_local=local, sdp_certificate=certificate,
                rounds=rounds, rows=rows, alpha=alpha, theta=theta,
                alpha_reference=alpha_reference, theta_reference=theta_reference,
                reference_scope='31 independent exhaustive cuts; exact rational PSD dual bounds are separate from local projected-gradient observations. Random cuts use one label per vertex. Finite sample means do not establish the universal GW theorem.')


def compute_online() -> dict:
    from collections import Counter
    B = 10
    deterministic = [dict(days=d, cost=O.ski_rental(B, d), opt=min(d, B)) for d in range(1, 31)]
    q = F(B - 1, B)
    weights = [q ** (B - j) for j in range(1, B + 1)]
    probabilities = [w / sum(weights) for w in weights]
    ratio = 1 / (1 - q ** B)
    rng = random.Random(51)
    randomized = []
    for days in range(1, 31):
        costs = [O.ski_rental(B, days, 'random', rng) for _ in range(4000)]
        expectation = sum(probability * (days if days < j else j - 1 + B)
                          for j, probability in enumerate(probabilities, 1))
        assert expectation / min(days, B) <= ratio
        possible = {days if days < j else j - 1 + B for j in range(1, B + 1)}
        assert set(costs) <= possible
        randomized.append(dict(days=days, cost=float(np.mean(costs)), opt=min(days, B),
                               exact_cost=float(expectation), exact_cost_fraction=str(expectation),
                               histogram=dict(sorted(Counter(costs).items())), trials=4000,
                               samples_sha256=R.digest(costs)))
    from videos.cs.cs9.compute import chapter_trace
    trace = chapter_trace()
    pages = (trace.addr // 64).tolist()
    rows = []
    policies = ('lru', 'fifo', 'marking', 'random', 'opt')
    for k in (8, 16, 32, 64, 96):
        row = dict(k=k, seeds={})
        for index, policy in enumerate(policies):
            seed = 5200 + 100 * k + index
            row[policy] = O.paging(pages, k, policy, rng=random.Random(seed))
            assert row[policy] == R.paging_reference(pages, k, policy, seed)
            row['seeds'][policy] = seed
        assert all(row['opt'] <= row[policy] <= len(pages) for policy in policies)
        rows.append(row)
    adversaries = []
    for k in (4, 8, 16):
        requests = list(range(k + 1)) * 200
        lru = O.paging(requests, k, 'lru')
        assert lru == len(requests)
        adversaries.append(dict(k=k, requests=len(requests), lru=lru,
                                opt=O.paging(requests, k, 'opt'),
                                marking=O.paging(requests, k, 'marking', rng=random.Random(5300 + k))))
        for policy in ('lru', 'opt', 'marking'):
            assert adversaries[-1][policy] == R.paging_reference(requests, k, policy, 5300 + k)
    import hashlib, inspect
    return dict(B=B, det=deterministic, rnd=randomized, requests=len(pages), distinct=len(set(pages)),
                rows=rows, adv=adversaries, e_ratio=math.e / (math.e - 1),
                discrete_ratio=float(ratio), discrete_ratio_exact=str(ratio),
                buy_day_probabilities=[str(x) for x in probabilities], trace_pages=pages,
                trace_provenance=dict(function_sha256=hashlib.sha256(inspect.getsource(chapter_trace).encode()).hexdigest(),
                                      pages_sha256=R.digest(pages),
                                      scope='Full Job first-chapter data-access trace only; instruction fetches excluded. Addresses map to64-byte lines. Initially empty fully associative cache, unit misses; OPT uses offline next-use preprocessing.'),
                reference_scope='Exact discrete ski expectation for a season chosen independently of the random buy day; e/(e-1) is the continuous/large-B limit. Paging has independent full-trace verification in the numerical audit; policy random streams are separate.')


def compute_mw() -> dict:
    from scipy.optimize import linprog
    from scipy.special import softmax
    rng = np.random.default_rng(61)
    n, rounds = 10, 20000
    probabilities = np.full(n, .5)
    probabilities[3] = .45
    losses = (rng.random((rounds, n)) < probabilities).astype(float)
    rows = []
    captured = None
    for horizon in (100, 300, 1000, 3000, 10000, 20000):
        eta = math.sqrt(8 * math.log(n) / horizon)
        algorithm, best, history = O.hedge(losses[:horizon], eta)
        cumulative = np.vstack((np.zeros(n), np.cumsum(losses[:horizon - 1], axis=0)))
        expected_history = softmax(-eta * cumulative, axis=1)
        expected_loss = float(np.sum(expected_history * losses[:horizon]))
        assert np.allclose(history, expected_history, atol=1e-11, rtol=0)
        assert abs(algorithm - expected_loss) < 1e-8
        assert best == losses[:horizon].sum(0).min()
        bound = math.log(n) / eta + eta * horizon / 8
        assert algorithm - best <= bound + 1e-8
        rows.append(dict(T=horizon, eta=eta, algorithm=algorithm, best_loss=best,
                         regret=algorithm - best, bound=bound, history_sha256=R.digest(history)))
        if horizon == 3000:
            captured = history[::30].tolist()
    matrix = np.array([[.6, .2, .8], [.3, .7, .4], [.9, .1, .5]])
    primal = linprog([0, 0, 0, -1], A_ub=np.c_[-matrix.T, np.ones(3)], b_ub=np.zeros(3),
                     A_eq=[[1, 1, 1, 0]], b_eq=[1], bounds=[(0, 1)] * 3 + [(None, None)], method='highs')
    dual = linprog([0, 0, 0, 1], A_ub=np.c_[matrix, -np.ones(3)], b_ub=np.zeros(3),
                   A_eq=[[1, 1, 1, 0]], b_eq=[1], bounds=[(0, 1)] * 3 + [(None, None)], method='highs')
    assert primal.success and dual.success
    # Exact3x3 support equilibrium; independent of both numerical LPs.
    payoff = [[F(str(v)) for v in row] for row in matrix.tolist()]
    p = R.solve_exact([*[list(column) + [F(-1)] for column in zip(*payoff)], [F(1)] * 3 + [F(0)]], [0, 0, 0, 1])
    q = R.solve_exact([*[row + [F(-1)] for row in payoff], [F(1)] * 3 + [F(0)]], [0, 0, 0, 1])
    assert min(p[:3] + q[:3]) >= 0 and p[3] == q[3]
    value = float(p[3])
    assert abs(-primal.fun - value) < 1e-9 and abs(dual.fun - value) < 1e-9
    game = []
    for horizon in (10, 100, 1000, 10000):
        lo, hi, row, column = O.mw_zero_sum(matrix, horizon, return_column=True)
        assert min(row) >= 0 and min(column) >= 0
        assert abs(sum(row) - 1) < 1e-10 and abs(sum(column) - 1) < 1e-10
        assert abs(lo - min(row @ matrix)) < 1e-12 and abs(hi - max(matrix @ column)) < 1e-12
        assert lo <= value + 1e-10 and hi >= value - 1e-10
        game.append(dict(T=horizon, eta=math.sqrt(math.log(3) / horizon), lo=lo, hi=hi,
                         row_distribution=row.tolist(), column_distribution=column.tolist()))
    return dict(n=n, seed=61, loss_probabilities=probabilities.tolist(), losses=losses.astype(int).tolist(),
                rows=rows, weights=captured, best=int(np.argmin(losses[:3000].sum(0))), game=game,
                game_value=value, game_p=primal.x[:3].tolist(), M=matrix.tolist(),
                rps=[[.5, 1, 0], [0, .5, 1], [1, 0, .5]],
                exact_equilibrium=dict(p=list(map(str, p[:3])), q=list(map(str, q[:3])), value=str(p[3])),
                reference_scope='Each Horizon retunes eta and is independently checked against vectorized softmax of prefix cumulative losses and the Hoeffding expected-loss regret bound. Game lower/upper bounds come from feasible empirical row/column distributions; an exact rational equilibrium separately certifies the value. Finite gaps are observations, not exact convergence.')


def compute_convex() -> dict:
    from scipy.special import logsumexp
    Aa = np.array([[1, 0.75], [1, -0.75], [-1, 0]])

    def f(x):
        return float(logsumexp(Aa @ np.asarray(x) - 0.1))

    def derivatives(x):
        z = Aa @ x - 0.1
        probability = np.exp(z - logsumexp(z))
        gradient = Aa.T @ probability
        hessian = Aa.T @ (np.diag(probability) - np.outer(probability, probability)) @ Aa
        return gradient, hessian

    x0 = np.array([-1.5, 3.0])
    gradient_path, x = [x0.tolist()], x0.copy()
    for _ in range(60):
        g, _ = derivatives(x)
        step = 1.0
        for _ in range(100):
            if f(x - step * g) <= f(x) - 0.3 * step * float(g @ g):
                break
            step *= 0.7
        else:
            raise RuntimeError('gradient line-search budget exhausted')
        x = x - step * g
        gradient_path.append(x.tolist())
    newton_path, x = [x0.tolist()], x0.copy()
    for _ in range(12):
        g, H = derivatives(x)
        direction = -np.linalg.solve(H, g)
        step = 1.0
        for _ in range(100):
            if f(x + step * direction) <= f(x) + 0.3 * step * float(g @ direction):
                break
            step *= 0.7
        else:
            raise RuntimeError('Newton line-search budget exhausted')
        x = x + step * direction
        newton_path.append(x.tolist())
    optimum = np.array([-math.log(2) / 2, 0.0])
    value = math.log(2 * math.sqrt(2)) - 0.1
    g, H = derivatives(optimum)
    assert np.linalg.norm(g) < 1e-12 and abs(f(optimum) - value) < 1e-12
    assert np.allclose(np.linalg.eigvalsh(H), [0.28125, 1.0])
    raw_gradient = [f(x) - value for x in gradient_path]
    raw_newton = [f(x) - value for x in newton_path]
    assert min(raw_gradient + raw_newton) >= -1e-12
    gradient_error = [max(0.0, x) for x in raw_gradient]
    newton_error = [max(0.0, x) for x in raw_newton]
    return dict(gd=gradient_path, newton=newton_path, gd_err=gradient_error, newton_err=newton_error,
                xstar=optimum.tolist(), fstar=value,
                gradient_steps_to_1e10=next(i for i, e in enumerate(gradient_error) if e <= 1e-10),
                newton_steps_to_1e10=next(i for i, e in enumerate(newton_error) if e <= 1e-10),
                hessian_eigenvalues=[0.28125, 1.0],
                reference_scope='Stable log-sum-exp; independent analytic optimum(-log(2)/2,0) with value log(2sqrt(2))-.1. Stationary gradient and convexity certify the global minimum. Only sub-roundoff negative plotted gaps are clamped; finite iteration counts are observations, not universal rate guarantees.')


def compute_frontier() -> dict:
    from scipy.spatial import HalfspaceIntersection, ConvexHull
    import networkx as nx

    def sample(n, rng):
        rejected = 0
        while True:
            N = rng.standard_normal((n, 3))
            N /= np.linalg.norm(N, axis=1, keepdims=True)
            bounded = R.boundedness_certificate(N)
            if bounded is not None:
                break
            rejected += 1
            assert rejected < 1000
        intersection = HalfspaceIntersection(np.c_[N, -np.ones(n)], np.zeros(3))
        V = intersection.intersections
        active = [frozenset(f) for f in intersection.dual_facets]
        assert np.isfinite(V).all() and len(V) == len(active)
        tolerance = 1e-8
        assert np.max(N @ V.T - 1) <= tolerance
        for vertex, indices in zip(V, active):
            assert len(indices) == 3
            assert np.max(np.abs(N[list(indices)] @ vertex - 1)) <= tolerance
        assert set().union(*active) == set(range(n))
        edges = [(a, b) for a in range(len(V)) for b in range(a + 1, len(V))
                 if len(active[a] & active[b]) == 2]
        graph = nx.Graph()
        graph.add_nodes_from(range(len(V)))
        graph.add_edges_from(edges)
        assert nx.is_connected(graph) and all(degree == 3 for _, degree in graph.degree())
        assert len(V) == 2 * n - 4 and len(edges) == 3 * n - 6
        assert len(V) - len(edges) + n == 2
        reference = R.diameter_reference(len(V), edges)
        assert nx.diameter(graph) == reference['diameter']
        eccentricity = nx.eccentricity(graph)
        u = max(eccentricity, key=lambda k: (eccentricity[k], -k))
        distance = nx.single_source_shortest_path_length(graph, u)
        v = max(distance, key=lambda k: (distance[k], -k))
        path = nx.shortest_path(graph, u, v)
        assert len(path) - 1 == reference['diameter']
        return dict(N=N.tolist(), V=V.tolist(), active=[sorted(f) for f in active],
                    edges=[list(edge) for edge in edges], path=path,
                    facets=n, vertices=len(V), diam=reference['diameter'],
                    boundedness=bounded, reference=reference, rejected=rejected,
                    numerical_tolerance=tolerance)

    rng = np.random.default_rng(71)
    rows, samples = [], []
    for n in (8, 16, 32, 64, 128):
        trials = [sample(n, rng) for _ in range(20)]
        samples.extend(trials)
        diameters = [trial['diam'] for trial in trials]
        rows.append(dict(n=n, facets=n, hirsch=n - 3, mean_diam=float(np.mean(diameters)),
                         max_diam=max(diameters), trials=20,
                         rejected=sum(trial['rejected'] for trial in trials)))
    draw = sample(24, np.random.default_rng(5))
    draw['faces'] = [list(map(int, face)) for face in ConvexHull(np.array(draw['V'])).simplices]
    return dict(rows=rows, draw=draw, samples=samples,
                sampling_scope='Independent normal directions, conditioned on an exact boundedness certificate; rejection counts retained. Vertices/active planes/adjacency use floating Qhull with stated tolerance. Every diameter is checked by independent all-source BFS; these finite3D observations do not imply a general Hirsch bound.')


def _checked_producer(name, function):
    @functools.wraps(function)
    def checked():
        signature = source_signature()
        start = time.perf_counter()
        data = function()
        total = time.perf_counter() - start
        assert source_signature() == signature, 'producer source changed during execution'
        data.update(schema=SCHEMAS[name], source_sha256=signature, protocol=R.protocol(),
                    producer_wall_seconds=total,
                    producer_wall_scope='includes generation and post-timer references; not an algorithm benchmark',
                    validation='independent finite references and producer certificates executed outside algorithm timers')
        data.setdefault('timed_trials', [])
        json.dumps(data, default=float, allow_nan=False)
        return data
    return checked


ITEMS = {k[8:]: _checked_producer(k[8:], v) for k, v in list(globals().items()) if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
