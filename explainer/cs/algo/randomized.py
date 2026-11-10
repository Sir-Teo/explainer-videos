"""Randomness as a resource (Part 20): the algorithms whose error rates and costs the scenes measure.

Checking (Freivalds; Schwartz-Zippel and the Tutte matrix; fingerprints), cutting (Karger, Karger-Stein), primes
(Fermat, Miller-Rabin), walks (2-SAT, Schoening), balls into bins, Bloom filters, streams (reservoir, Misra-Gries,
Count-Min, HyperLogLog, KMV, AMS), similarity (MinHash, banded LSH), the probabilistic method (Moser-Tardos), and
derandomization (conditional expectations, RANDU).
"""

from __future__ import annotations

import math
import random
from collections import Counter

import numpy as np



def _int_at_least(value, lower, name):
    import operator
    try:
        value = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer at least {lower}") from exc
    if value < lower:
        raise ValueError(f"{name} must be at least {lower}")
    return value


def _graph(n, edges):
    n = _int_at_least(n, 0, "n")
    edges = list(edges)
    checked = []
    for u, v in edges:
        u, v = _int_at_least(u, 0, "vertex"), _int_at_least(v, 0, "vertex")
        if u >= n or v >= n or u == v:
            raise ValueError("edges must join two distinct vertices in range(n)")
        checked.append((u, v))
    return n, checked


def _clauses(n, clauses):
    n = _int_at_least(n, 0, "n")
    checked = []
    for clause in clauses:
        row = []
        for v, sign in clause:
            v = _int_at_least(v, 0, "variable")
            if v >= n or not isinstance(sign, (bool, np.bool_)):
                raise ValueError("literals require a variable in range(n) and a Boolean sign")
            row.append((v, bool(sign)))
        if not row:
            raise ValueError("an empty clause is unsatisfiable")
        checked.append(tuple(row))
    return n, checked


def _integer_entry(x):
    import operator
    try:
        return operator.index(x)
    except TypeError as exc:
        raise ValueError("matrix entries must be integers") from exc


def _prime_modulus(p):
    # These seven bases deterministically classify all integers below 2**64.
    p = _int_at_least(p, 2, "prime modulus")
    if p >= 1 << 64:
        raise ValueError("prime modulus must be below 2**64")
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if p == q:
            return p
        if p % q == 0:
            raise ValueError("modulus must be prime")
    d, exponent = p - 1, 0
    while d % 2 == 0:
        d //= 2
        exponent += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % p == 0:
            continue
        x = pow(base, d, p)
        if x in (1, p - 1):
            continue
        for _ in range(exponent - 1):
            x = x * x % p
            if x == p - 1:
                break
        else:
            raise ValueError("modulus must be prime")
    return p


# ------------------------------------------------------------------------------------------------- checking
def freivalds(A, B, C, rounds=1, rng=None) -> bool:
    """Exact integer Freivalds check; independent uniform bit vectors give error <= 2**-rounds.

    Integer-valued finite floats are accepted as the exact integers they represent.
    Bounded int64/float64 paths are used only when every dot-product intermediate is
    provably exact; larger integers use Python arithmetic. Fractional inputs are rejected.
    """
    rounds = _int_at_least(rounds, 1, "rounds")
    arrays = [np.asarray(M) for M in (A, B, C)]
    if any(M.ndim != 2 for M in arrays):
        raise ValueError("A, B and C must be matrices")
    A, B, C = arrays
    if A.shape[1] != B.shape[0] or C.shape != (A.shape[0], B.shape[1]):
        raise ValueError("matrix dimensions do not match A @ B = C")
    bounds = []
    for M in arrays:
        if M.dtype.kind in "iub":
            pass
        elif M.dtype.kind == "f":
            if not np.all(np.isfinite(M)) or not np.all(M == np.trunc(M)):
                raise ValueError("Freivalds requires exact integer entries")
        elif M.dtype.kind == "O":
            import numbers
            if any(not isinstance(x, numbers.Integral) for x in M.flat):
                raise ValueError("Freivalds requires exact integer entries")
        else:
            raise ValueError("Freivalds requires exact integer entries")
        bounds.append(max(abs(int(M.min())), abs(int(M.max()))) if M.size else 0)
    a, b, c = bounds
    n, k = B.shape[1], A.shape[1]
    bound = max(a, b, c, n * b, k * a * n * b, n * c)
    if all(M.dtype.kind == "f" for M in arrays) and bound <= 2**53:
        arrays = [M.astype(np.float64, copy=False) for M in arrays]
    elif bound <= np.iinfo(np.int64).max:
        arrays = [M.astype(np.int64, copy=False) for M in arrays]
    else:
        arrays = [np.array([int(x) for x in M.flat], dtype=object).reshape(M.shape) for M in arrays]
    A, B, C = arrays
    rng = rng if rng is not None else np.random.default_rng()
    for _ in range(rounds):
        r = rng.integers(0, 2, size=n)
        if not np.array_equal(A @ (B @ r), C @ r):
            return False
    return True


def schwartz_zippel_trial(p, q, nvars, S, rng) -> bool:
    """Sample independently from {0,...,S-1}; degree/|S| requires a field and a nonzero difference."""
    nvars, S = _int_at_least(nvars, 0, "nvars"), _int_at_least(S, 1, "S")
    x = [rng.randrange(S) for _ in range(nvars)]
    return p(*x) == q(*x)


def det_mod(M, p):
    """Determinant of an integer matrix modulo a prime, by Gaussian elimination."""
    p = _prime_modulus(p)
    M = [[_integer_entry(x) % p for x in row] for row in M]
    n, det = len(M), 1
    if any(len(row) != n for row in M):
        raise ValueError("determinant requires a square matrix")
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c]), None)
        if piv is None:
            return 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        det = det * M[c][c] % p
        inv = pow(M[c][c], p - 2, p)
        for r in range(c + 1, n):
            f = M[r][c] * inv % p
            if f:
                M[r] = [(a - f * b) % p for a, b in zip(M[r], M[c])]
    return det % p


def tutte_has_perfect_matching(n, edges, rng, p=2_147_483_647) -> bool:
    """Lovasz (1979): substitute random values into the Tutte matrix; a nonzero determinant means a perfect
    matching exists. Sampling each edge value uniformly in the prime field gives false-negative probability at most n/p."""
    n, edges = _graph(n, edges)
    p = _prime_modulus(p)
    if p == 2:
        raise ValueError("this teaching API accepts odd prime fields")
    if n % 2:
        return False
    T = [[0] * n for _ in range(n)]
    for u, v in edges:
        x = rng.randrange(p)
        a, b = min(u, v), max(u, v)
        T[a][b] = x
        T[b][a] = -x
    return det_mod(T, p) != 0


def has_perfect_matching_exact(n, edges) -> bool:
    """Exact check by search over vertex 0's partners (small graphs only)."""
    n, edges = _graph(n, edges)
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def go(left):
        if not left:
            return True
        u = min(left)
        for v in adj[u] & left:
            if v != u and go(left - {u, v}):
                return True
        return False
    return n % 2 == 0 and go(frozenset(range(n)))


def fingerprint(data: bytes, p: int) -> int:
    """Length-preserving byte encoding modulo p; a leading sentinel distinguishes initial zero bytes.

    Fixed primes have collisions; a randomized-prime probability claim requires its
    sampling model and a separate finite prime-count bound.
    """
    p = _prime_modulus(p)
    if not isinstance(data, bytes):
        raise ValueError("fingerprint input must be bytes")
    return int.from_bytes(b"\x01" + data, "big") % p


# ------------------------------------------------------------------------------------------------- cutting
def karger(n, edges, rng):
    """One run of random contraction: returns the size of the cut found."""
    n, edges = _graph(n, edges)
    if n < 2:
        return 0
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    order = list(edges)
    rng.shuffle(order)                 # contracting in a random order = contracting a random edge each step
    left = n
    for u, v in order:
        if left == 2:
            break
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            left -= 1
    return sum(1 for u, v in edges if find(u) != find(v))


def karger_trace(n, edges, rng):
    """The contraction sequence for drawing: a list of (u, v) super-vertex merges, and the final two groups."""
    n, edges = _graph(n, edges)
    groups = {v: {v} for v in range(n)}
    order = list(edges)
    rng.shuffle(order)
    owner = {v: v for v in range(n)}
    merges = []
    for u, v in order:
        if len(groups) == 2:
            break
        a, b = owner[u], owner[v]
        if a != b:
            merges.append((a, b))
            for x in groups[a]:
                owner[x] = b
            groups[b] |= groups.pop(a)
    return merges, [sorted(g) for g in groups.values()]


def karger_stein(n, edges, rng):
    """Karger and Stein (1996): contract to n/sqrt(2) + 1, recurse twice, keep the better."""
    n, edges = _graph(n, edges)
    if n < 2:
        return 0
    # A disconnected graph has cut zero and contraction cannot reach its target.
    seen = {0}
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    todo = [0]
    while todo:
        for v in adj[todo.pop()]:
            if v not in seen:
                seen.add(v); todo.append(v)
    if len(seen) != n:
        return 0

    def contract(vs, es, t):
        parent = {v: v for v in vs}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        order = list(es)
        rng.shuffle(order)
        left = len(vs)
        for u, v in order:
            if left <= t:
                break
            a, b = find(u), find(v)
            if a != b:
                parent[a] = b
                left -= 1
        nv = {find(v) for v in vs}
        ne = [(find(u), find(v)) for u, v in es if find(u) != find(v)]
        return nv, ne

    def go(vs, es):
        if len(vs) <= 6:
            best = math.inf
            for _ in range(12):
                _, ne = contract(vs, es, 2)
                best = min(best, len(ne))
            return best
        t = int(math.ceil(1 + len(vs) / math.sqrt(2)))
        return min(go(*contract(vs, es, t)), go(*contract(vs, es, t)))
    return go(set(range(n)), list(edges))


# ------------------------------------------------------------------------------------------------- primes
def fermat_liar(a, n) -> bool:
    n = _int_at_least(n, 2, "n")
    return pow(a, n - 1, n) == 1


def mr_liar(a, n) -> bool:
    """Is a a strong liar for odd composite n (Miller-Rabin passes)?"""
    n = _int_at_least(n, 3, "n")
    if n % 2 == 0:
        raise ValueError("strong-liar test requires odd n")
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def miller_rabin(n, rounds=40, rng=None) -> bool:
    n = _int_at_least(n, 0, "n")
    rounds = _int_at_least(rounds, 1, "rounds")
    if n < 4:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    rng = rng or random.Random()
    return all(mr_liar(rng.randrange(2, n - 1), n) for _ in range(rounds))


def carmichaels(limit):
    """Carmichael numbers below limit, by Korselt's criterion."""
    limit = _int_at_least(limit, 0, "limit")
    spf = list(range(limit))
    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, limit, i):
                if spf[j] == j:
                    spf[j] = i
    out = []
    for n in range(3, limit, 2):
        if spf[n] == n:
            continue
        m, ps, ok = n, [], True
        while m > 1:
            p = spf[m]
            m //= p
            if m % p == 0:
                ok = False
                break
            ps.append(p)
        if ok and len(ps) >= 2 and all((n - 1) % (p - 1) == 0 for p in ps):
            out.append(n)
    return out


def random_prime(bits, rng):
    """Return a 40-round probable prime, not an independently certified prime."""
    bits = _int_at_least(bits, 2, "bits")
    while True:
        n = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if miller_rabin(n, 40, rng):
            return n


# ------------------------------------------------------------------------------------------------- walks
def random_2sat(n, m, rng, satisfiable=True):
    """m random 2-clauses on n variables; if satisfiable, all satisfied by a hidden assignment."""
    n, m = _int_at_least(n, 0, "n"), _int_at_least(m, 0, "m")
    if m and n < 2:
        raise ValueError("2-SAT generator requires at least two variables")
    hidden = [rng.random() < 0.5 for _ in range(n)]
    out = []
    while len(out) < m:
        a, b = rng.sample(range(n), 2)
        c = ((a, rng.random() < 0.5), (b, rng.random() < 0.5))
        if not satisfiable or any(hidden[v] == s for v, s in c):
            out.append(c)
    return out


def walk_sat(n, clauses, rng, max_steps, k_restart=None, *, statistics=None):
    """Return flips to a satisfying assignment within the budget, or None (not an UNSAT proof)."""
    n, clauses = _clauses(n, clauses)
    max_steps = _int_at_least(max_steps, 0, "max_steps")
    restart = max(1, max_steps) if k_restart is None else _int_at_least(k_restart, 1, "k_restart")
    if statistics is not None and not isinstance(statistics, dict):
        raise ValueError("statistics must be a dictionary")
    attempts = 0
    steps = 0
    def finish(found):
        if statistics is not None:
            statistics.update(attempts=attempts, flips=steps, found=found)
        return steps if found else None
    while True:
        attempts += 1
        x = [rng.random() < 0.5 for _ in range(n)]
        for _ in range(restart):
            bad = [c for c in clauses if not any(x[v] == sign for v, sign in c)]
            if not bad:
                return finish(True)
            if steps == max_steps:
                return finish(False)
            v, _ = rng.choice(rng.choice(bad))
            x[v] = not x[v]
            steps += 1
        # Check the last flip before restarting or exhausting the budget.
        if all(any(x[v] == sign for v, sign in c) for c in clauses):
            return finish(True)
        if steps == max_steps:
            return finish(False)


def planted_3sat(n, m, rng):
    n, m = _int_at_least(n, 0, "n"), _int_at_least(m, 0, "m")
    if m and n < 3:
        raise ValueError("3-SAT generator requires at least three variables")
    hidden = [rng.random() < 0.5 for _ in range(n)]
    out = []
    while len(out) < m:
        vs = rng.sample(range(n), 3)
        c = tuple((v, rng.random() < 0.5) for v in vs)
        if any(hidden[v] == s for v, s in c):
            out.append(c)
    return out


# ------------------------------------------------------------------------------------------------- bins
def max_load(n, choices, rng):
    """n balls into n bins, each to the least loaded of ``choices`` random bins (numpy, sequential for d > 1)."""
    n, choices = _int_at_least(n, 0, "n"), _int_at_least(choices, 1, "choices")
    if n == 0:
        return 0
    if choices == 1:
        return int(np.bincount(rng.integers(0, n, n), minlength=n).max())
    load = np.zeros(n, dtype=np.int32)
    picks = rng.integers(0, n, (n, choices))
    for row in picks:
        b = row[np.argmin(load[row])]
        load[b] += 1
    return int(load.max())


# ------------------------------------------------------------------------------------------------- Bloom
class Bloom:
    """m bits, k hashes by double hashing from two 64-bit halves of a keyed BLAKE2 digest."""

    def __init__(self, m, k, key=b"part20"):
        m, k = _int_at_least(m, 1, "m"), _int_at_least(k, 1, "k")
        self.m, self.k = m, k
        self._packed = np.zeros((m + 7) // 8, dtype=np.uint8)
        self.key = key

    def _idx(self, item: bytes):
        import hashlib
        h = hashlib.blake2b(item, digest_size=16, key=self.key).digest()
        a, b = int.from_bytes(h[:8], "little"), int.from_bytes(h[8:], "little") | 1
        return [(a + i * b) % self.m for i in range(self.k)]

    @property
    def bits(self):
        """Unpacked diagnostic view; storage uses ceil(m/8) bytes."""
        return np.unpackbits(self._packed, bitorder="little")[:self.m].astype(bool)

    def add(self, item):
        idx = np.array(self._idx(item), dtype=np.int64)
        np.bitwise_or.at(self._packed, idx // 8, (1 << (idx % 8)).astype(np.uint8))

    def __contains__(self, item):
        idx = np.array(self._idx(item), dtype=np.int64)
        return bool(((self._packed[idx // 8] >> (idx % 8)) & 1).all())


def bloom_theory(n, m, k):
    """Independent uniform-hash asymptotic approximation; double hashing is measured separately."""
    n, m, k = _int_at_least(n, 0, "n"), _int_at_least(m, 1, "m"), _int_at_least(k, 1, "k")
    return (1 - math.exp(-k * n / m)) ** k


# ------------------------------------------------------------------------------------------------- streams
def reservoir(stream, k, rng):
    k = _int_at_least(k, 0, "k")
    out = []
    for i, x in enumerate(stream):
        if i < k:
            out.append(x)
        else:
            j = rng.randrange(i + 1)
            if j < k:
                out[j] = x
    return out


def misra_gries(stream, k):
    """k - 1 counters; every item with frequency > n/k survives, each count undercounted by at most n/k."""
    k = _int_at_least(k, 1, "k")
    c: dict = {}
    for x in stream:
        if x in c:
            c[x] += 1
        elif len(c) < k - 1:
            c[x] = 1
        else:
            for y in list(c):
                c[y] -= 1
                if c[y] == 0:
                    del c[y]
    return c


def _h64(items, seed):
    """64-bit hashes of byte strings (keyed BLAKE2), as a numpy array."""
    import hashlib
    key = seed.to_bytes(8, "little")
    return np.array([int.from_bytes(hashlib.blake2b(x, digest_size=8, key=key).digest(), "little") for x in items],
                    dtype=np.uint64)


def hyperloglog(hashes: np.ndarray, b: int) -> float:
    """Flajolet, Fusy, Gandouet and Meunier (2007), with the small-range correction; m = 2^b registers."""
    b = _int_at_least(b, 4, "b")
    if b > 18:
        raise ValueError("supported HyperLogLog precision is 4 through 18")
    hashes = np.asarray(hashes)
    if hashes.ndim != 1 or hashes.dtype != np.dtype("uint64"):
        raise ValueError("hashes must be a one-dimensional uint64 array")
    m = 1 << b
    idx = (hashes >> np.uint64(64 - b)).astype(np.int64)
    rest = (hashes << np.uint64(b)) | np.uint64(1 << (b - 1))     # keep a 1 so the rank is bounded
    # rank: position of the leftmost 1 in the remaining 64 - b bits
    lz = np.zeros(len(hashes), dtype=np.int64)
    x = rest.copy()
    for s in (32, 16, 8, 4, 2, 1):
        mask = (x >> np.uint64(64 - s)) == 0
        lz[mask] += s
        x[mask] <<= np.uint64(s)
    rank = lz + 1
    reg = np.zeros(m, dtype=np.int64)
    np.maximum.at(reg, idx, rank)
    alpha = 0.7213 / (1 + 1.079 / m) if m >= 128 else {16: 0.673, 32: 0.697, 64: 0.709}[m]
    est = alpha * m * m / np.sum(2.0 ** -reg)
    zeros = int(np.sum(reg == 0))
    if est <= 2.5 * m and zeros:
        est = m * math.log(m / zeros)
    return float(est)


def kmv(hashes: np.ndarray, k: int) -> float:
    """k minimum values (Bar-Yossef et al. 2002): (k - 1) / (k-th smallest hash as a fraction of 2^64)."""
    k = _int_at_least(k, 2, "k")
    hashes = np.asarray(hashes)
    if hashes.ndim != 1 or hashes.dtype != np.dtype("uint64"):
        raise ValueError("hashes must be a one-dimensional uint64 array")
    u = np.unique(hashes)
    if len(u) < k:
        return float(len(u))
    kth = np.partition(u, k - 1)[k - 1]
    return (k - 1) / (float(kth) / 2.0 ** 64)


def ams_f2(items, counts: dict, k: int, groups: int, rng) -> float:
    """Alon, Matias and Szegedy (1996): Z = sum of s(x) over the stream, s a random +-1; Z^2 estimates F2.  The mean
    of k copies in each of ``groups`` groups, then the median of the group means."""
    k, groups = _int_at_least(k, 1, "k"), _int_at_least(groups, 1, "groups")
    if any(not isinstance(v, (int, np.integer)) or v < 0 for v in counts.values()):
        raise ValueError("counts must be nonnegative integers")
    keys = list(counts)
    vals = np.array([counts[x] for x in keys], dtype=np.float64)
    ests = []
    for _ in range(groups):
        s = rng.choice([-1.0, 1.0], size=(k, len(keys)))
        z = s @ vals
        ests.append(float(np.mean(z * z)))
    return float(np.median(ests))


def minhash_sig(shingles: set, nperm: int, seed: int = 1) -> np.ndarray:
    """MinHash signature: for each of nperm hash functions (a x + b mod p on 64-bit shingle hashes), the minimum."""
    nperm = _int_at_least(nperm, 1, "nperm")
    p = (1 << 61) - 1
    if not shingles:
        return np.full(nperm, p, dtype=object)
    rng = np.random.default_rng(seed)
    a = rng.integers(1, p, nperm, dtype=np.int64).astype(object)
    b = rng.integers(0, p, nperm, dtype=np.int64).astype(object)
    xs = [hash_shingle(s) for s in shingles]
    return np.array([min((ai * x + bi) % p for x in xs) for ai, bi in zip(a, b)], dtype=object)


def hash_shingle(s) -> int:
    import hashlib
    return int.from_bytes(hashlib.blake2b(" ".join(s).encode(), digest_size=7).digest(), "little")


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 1.0


def lsh_probability(s, rows, bands):
    """Ideal independent minwise-permutation model; affine hashes are an empirical approximation."""
    rows, bands = _int_at_least(rows, 1, "rows"), _int_at_least(bands, 1, "bands")
    if not 0 <= s <= 1:
        raise ValueError("similarity must lie in [0, 1]")
    return 1 - (1 - s ** rows) ** bands


# ------------------------------------------------------------------------------------------------- the probabilistic method
def moser_tardos(n, clauses, rng, *, initial=None, max_resamplings=1_000_000):
    """Resample the variables of a violated clause until none is violated.  Returns the number of resamplings."""
    n, clauses = _clauses(n, clauses)
    max_resamplings = _int_at_least(max_resamplings, 0, "max_resamplings")
    x = [rng.random() < 0.5 for _ in range(n)] if initial is None else list(initial)
    if len(x) != n or any(not isinstance(v, (bool, np.bool_)) for v in x):
        raise ValueError("initial assignment must contain n Booleans")
    by_var: dict = {}
    for i, c in enumerate(clauses):
        for v, _ in c:
            by_var.setdefault(v, []).append(i)
    bad = {i for i, c in enumerate(clauses) if not any(x[v] == s for v, s in c)}
    steps = 0
    while bad:
        if steps == max_resamplings:
            raise RuntimeError("resampling budget exhausted; satisfiability is unresolved")
        i = min(bad)
        for v in {v for v, _ in clauses[i]}:
            x[v] = rng.random() < 0.5
        steps += 1
        touched = {j for v, _ in clauses[i] for j in by_var[v]}
        for j in touched:
            if any(x[v] == s for v, s in clauses[j]):
                bad.discard(j)
            else:
                bad.add(j)
    return steps, x


def ramsey_expected(n, k):
    """Expected number of monochromatic K_k in a random 2-colouring of K_n."""
    return math.comb(n, k) * 2.0 ** (1 - math.comb(k, 2))


# ------------------------------------------------------------------------------------------------- derandomization
def maxcut_conditional(n, edges):
    """Place vertices one by one on the side that cuts more edges to those already placed: at least m/2."""
    n, edges = _graph(n, edges)
    side = {}
    for v in range(n):
        a = sum(1 for u, w in edges if (u == v and w in side and side[w] == 0) or (w == v and u in side and side[u] == 0))
        b = sum(1 for u, w in edges if (u == v and w in side and side[w] == 1) or (w == v and u in side and side[u] == 1))
        side[v] = 1 if a >= b else 0
    return sum(1 for u, w in edges if side[u] != side[w]), side


def randu(seed, n):
    """IBM's RANDU (1960s): x <- 65539 x mod 2^31."""
    out, x = [], seed
    for _ in range(n):
        x = 65539 * x % (1 << 31)
        out.append(x)
    return out
