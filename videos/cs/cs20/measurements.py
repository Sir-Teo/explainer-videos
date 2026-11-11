"""Independent references and explicit measurement scope for Part 20."""
from __future__ import annotations

import hashlib
import math
import platform
from pathlib import Path

import numpy as np


def protocol():
    import ctypes
    pools = []
    for path in (Path(np.__file__).parent.parent / 'numpy.libs').glob('*blas*.so'):
        library = ctypes.CDLL(str(path))
        for symbol in ('scipy_openblas_get_num_threads64_', 'openblas_get_num_threads64_', 'openblas_get_num_threads'):
            try:
                query = getattr(library, symbol)
                query.restype = ctypes.c_int
                pools.append(dict(library=path.name, query=symbol, configured_threads=query()))
                break
            except AttributeError:
                continue
    return dict(timer='time.perf_counter', python=platform.python_version(), platform=platform.platform(),
                numpy=np.__version__, numpy_build=getattr(np.__config__, 'CONFIG', {}), native_threadpools=pools,
                scope='shared host observation; no causal hardware or universal speed claim',
                validation='timed outputs checked after stopping the timer; references prepared outside it')


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def digest_array(array):
    array = np.ascontiguousarray(array)
    h = hashlib.sha256(str((array.shape, array.dtype.str)).encode())
    h.update(array.tobytes())
    return h.hexdigest()


def exact_product_reference(a, b):
    """Full int64 product reference under an absolute intermediate bound, outside BLAS timers."""
    ai, bi = np.asarray(a, dtype=np.int64), np.asarray(b, dtype=np.int64)
    bound = a.shape[1] * int(np.max(np.abs(ai))) * int(np.max(np.abs(bi)))
    assert bound < 2**53
    return ai @ bi, bound


def fingerprint_reference(data, prime):
    """Horner's rule on 4KiB blocks with a leading sentinel, avoiding the giant-integer implementation."""
    result = 1
    for start in range(0, len(data), 4096):
        block = data[start:start + 4096]
        result = (result * pow(256, len(block), prime) + int.from_bytes(block, 'big') % prime) % prime
    return result


def minimum_cut_reference(n, edges):
    """Independent deterministic Stoer-Wagner reference for the unweighted multigraph."""
    import networkx as nx
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for u, v in edges:
        if graph.has_edge(u, v):
            graph[u][v]['weight'] += 1
        else:
            graph.add_edge(u, v, weight=1)
    if n < 2 or not nx.is_connected(graph):
        return 0, []
    value, partition = nx.stoer_wagner(graph)
    side = set(partition[0])
    assert sum((u in side) != (v in side) for u, v in edges) == value
    return int(value), sorted(side)


def prime_by_trial_division(n):
    """Independent small-number oracle, used for the finite liar-rate inventory."""
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def hll_reference(hashes, precision):
    """Scalar suffix/rank reference, independent of the vectorized leading-zero algorithm."""
    m = 1 << precision
    registers = [0] * m
    for value in hashes:
        value = int(value)
        index = value >> (64 - precision)
        suffix = value & ((1 << (64 - precision)) - 1)
        rank = 65 - precision - suffix.bit_length()
        registers[index] = max(registers[index], rank)
    alpha = {16: .673, 32: .697, 64: .709}.get(m, .7213 / (1 + 1.079 / m))
    estimate = alpha * m * m / sum(2.**-r for r in registers)
    zeros = registers.count(0)
    if estimate <= 2.5 * m and zeros:
        estimate = m * math.log(m / zeros)
    return estimate, registers


def check_assignment(clauses, assignment):
    assert all(any(assignment[v] == sign for v, sign in clause) for clause in clauses)
