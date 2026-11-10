"""Independent output checks and explicit measurement protocols for Part 18."""
from __future__ import annotations

import functools
import itertools
import math
import platform
import sys
from collections import Counter


def protocol(repeats=3):
    return dict(timer='time.perf_counter', repeats=repeats, statistic='minimum',
                python=platform.python_version(), implementation=platform.python_implementation(),
                platform=platform.platform(), scope='single shared host; complete stated operation; no causal hardware attribution')


def list_allocation_bytes(value):
    """Reachable Python list/int allocation, deduplicated by identity; excludes graph-generation temporaries."""
    seen = set()
    def visit(obj):
        key = id(obj)
        if key in seen:
            return 0
        seen.add(key)
        return sys.getsizeof(obj) + (sum(visit(x) for x in obj) if isinstance(obj, list) else 0)
    return visit(value)


def euler_certificate(adj, circuit):
    """Compare both directed incidences, including two incidences per self-loop."""
    assert circuit is not None
    expected = Counter((u, v) for u, vs in adj.items() for v in vs)
    actual = Counter()
    for u, v in zip(circuit, circuit[1:]):
        actual[u, v] += 1
        actual[v, u] += 1
    assert actual == expected
    assert not expected or circuit[0] == circuit[-1]
    return dict(edges=sum(expected.values()) // 2, traversed=len(circuit) - 1 if circuit else 0,
                verified='complete undirected incidence multiset and closed endpoints')


def allpairs_agree(reference, result):
    assert result is not None
    finite = unreachable = 0
    for u, row in enumerate(reference):
        for v, value in enumerate(row):
            actual = result[u].get(v, math.inf)
            if value == math.inf:
                assert actual == math.inf
                unreachable += 1
            else:
                assert math.isclose(actual, value, rel_tol=1e-11, abs_tol=1e-9)
                finite += 1
    return dict(finite_pairs=finite, unreachable_pairs=unreachable, total_pairs=finite + unreachable)


def tree_certificate(n, tree, total):
    assert len(tree) == max(0, n - 1)
    neighbours = {u: [] for u in range(n)}
    for u, v, _ in tree:
        neighbours[u].append(v)
        neighbours[v].append(u)
    reached = {0} if n else set()
    work = list(reached)
    while work:
        for v in neighbours[work.pop()]:
            if v not in reached:
                reached.add(v)
                work.append(v)
    assert len(reached) == n
    assert math.isclose(sum(w for _, _, w in tree), total, rel_tol=1e-12, abs_tol=1e-10)
    return dict(vertices=n, edges=len(tree), connected=True, total=total)


def flow_certificate(cap, source, sink, value, paths, side):
    """Recover a feasible antisymmetric net flow, valid even with antiparallel arcs."""
    vertices = set(cap) | {v for row in cap.values() for v in row}
    assert source in side and sink not in side
    net = Counter()
    for path, amount in paths:
        assert path[0] == source and path[-1] == sink and amount > 0
        for u, v in zip(path, path[1:]):
            net[u, v] += amount
            net[v, u] -= amount
    for u in vertices:
        for v in vertices:
            assert net[u, v] <= cap.get(u, {}).get(v, 0)
        divergence = sum(net[u, v] for v in vertices)
        assert divergence == (value if u == source else -value if u == sink else 0)
    cut = sum(c for u in side for v, c in cap.get(u, {}).items() if v not in side)
    assert cut == value
    return dict(value=value, cut_capacity=cut, directed_edges=sum(len(row) for row in cap.values()),
                capacity_and_conservation=True,
                net_edges=[[u, v, net[u, v]] for u, row in cap.items() for v in row])


def tsp_reference(matrix):
    """Independent suffix recursion; small instances additionally checked by full permutation enumeration."""
    n = len(matrix)
    if n <= 1:
        return 0
    @functools.lru_cache(None)
    def finish(current, remaining):
        if not remaining:
            return matrix[current][0]
        return min(matrix[current][nxt] + finish(nxt, remaining ^ (1 << nxt))
                   for nxt in range(1, n) if remaining & (1 << nxt))
    value = finish(0, (1 << n) - 2)
    if n <= 8:
        brute = min(sum(matrix[tour[k]][tour[(k + 1) % n]] for k in range(n))
                    for rest in itertools.permutations(range(1, n)) for tour in [(0, *rest)])
        assert math.isclose(value, brute, rel_tol=1e-12, abs_tol=1e-12)
    return value


def pagerank_certificate(adj, rank, residuals, damping=.85, tolerance=1e-12):
    """Check the final vector with a NumPy scatter operator, separate from the Python iteration loop."""
    import numpy as np
    nodes = list(adj)
    index = {u: i for i, u in enumerate(nodes)}
    vector = np.array([rank[u] for u in nodes])
    assert np.all(vector >= 0) and abs(float(vector.sum()) - 1) < 1e-11
    dangling = sum(rank[u] for u in nodes if not adj[u])
    targets, contributions = [], []
    for u in nodes:
        for v in adj[u]:
            targets.append(index[v])
            contributions.append(damping * rank[u] / len(adj[u]))
    updated = np.full(len(nodes), ((1 - damping) + damping * dangling) / len(nodes))
    updated += np.bincount(targets, weights=contributions, minlength=len(nodes))
    residual = float(np.abs(updated - vector).sum())
    assert residuals and residuals[-1] < tolerance and residual < tolerance
    return dict(mass=float(vector.sum()), damping=damping, tolerance=tolerance,
                iterations=len(residuals), last_iterate_change=residuals[-1],
                stationarity_l1=residual, stationary_error_bound=residual / (1 - damping),
                scope='numerical fixed-point residual bound for this damped finite graph, not a relevance-quality metric')
