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


# ------------------------------------------------------------------------------------------------- checking
def freivalds(A, B, C, rounds=1, rng=None) -> bool:
    """True if A B = C passes ``rounds`` random 0/1 tests (always true when A B = C)."""
    rng = rng or np.random.default_rng()
    n = C.shape[1]
    for _ in range(rounds):
        r = rng.integers(0, 2, size=n)
        if not np.array_equal(A @ (B @ r), C @ r):
            return False
    return True


def schwartz_zippel_trial(p, q, nvars, S, rng) -> bool:
    """Evaluate two polynomials (callables) at a random point of S^nvars: do they agree?"""
    x = [rng.randrange(S) for _ in range(nvars)]
    return p(*x) == q(*x)


def det_mod(M, p):
    """Determinant of an integer matrix modulo a prime, by Gaussian elimination."""
    M = [[x % p for x in row] for row in M]
    n, det = len(M), 1
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
    matching exists (no false positives; a false negative has probability at most n/p)."""
    T = [[0] * n for _ in range(n)]
    for u, v in edges:
        x = rng.randrange(1, p)
        a, b = min(u, v), max(u, v)
        T[a][b] = x
        T[b][a] = -x
    return det_mod(T, p) != 0


def has_perfect_matching_exact(n, edges) -> bool:
    """Exact check by search over vertex 0's partners (small graphs only)."""
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
    """A file as a number, modulo p (Rabin's fingerprint)."""
    return int.from_bytes(data, "big") % p


# ------------------------------------------------------------------------------------------------- cutting
def karger(n, edges, rng):
    """One run of random contraction: returns the size of the cut found."""
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
    return pow(a, n - 1, n) == 1


def mr_liar(a, n) -> bool:
    """Is a a strong liar for odd composite n (Miller-Rabin passes)?"""
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
    if n < 4:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    rng = rng or random.Random()
    return all(mr_liar(rng.randrange(2, n - 1), n) for _ in range(rounds))


def carmichaels(limit):
    """Carmichael numbers below limit, by Korselt's criterion."""
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
    while True:
        n = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if miller_rabin(n, 40, rng):
            return n


# ------------------------------------------------------------------------------------------------- walks
def random_2sat(n, m, rng, satisfiable=True):
    """m random 2-clauses on n variables; if satisfiable, all satisfied by a hidden assignment."""
    hidden = [rng.random() < 0.5 for _ in range(n)]
    out = []
    while len(out) < m:
        a, b = rng.sample(range(n), 2)
        c = ((a, rng.random() < 0.5), (b, rng.random() < 0.5))
        if not satisfiable or any(hidden[v] == s for v, s in c):
            out.append(c)
    return out


def walk_sat(n, clauses, rng, max_steps, k_restart=None):
    """Papadimitriou's walk (2-SAT) or Schoening's (3-SAT, restarting every 3n steps): flip a random variable of an
    unsatisfied clause.  Returns the number of flips until satisfied, or None."""
    steps = 0
    while steps < max_steps:
        x = [rng.random() < 0.5 for _ in range(n)]
        for _ in range(k_restart or max_steps):
            bad = [c for c in clauses if not any(x[v] == s for v, s in c)]
            if not bad:
                return steps
            v, _ = rng.choice(rng.choice(bad))
            x[v] = not x[v]
            steps += 1
            if steps >= max_steps:
                return None
    return None


def planted_3sat(n, m, rng):
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
        self.m, self.k, self.bits = m, k, np.zeros(m, dtype=bool)
        self.key = key

    def _idx(self, item: bytes):
        import hashlib
        h = hashlib.blake2b(item, digest_size=16, key=self.key).digest()
        a, b = int.from_bytes(h[:8], "little"), int.from_bytes(h[8:], "little") | 1
        return [(a + i * b) % self.m for i in range(self.k)]

    def add(self, item):
        self.bits[self._idx(item)] = True

    def __contains__(self, item):
        return bool(self.bits[self._idx(item)].all())


def bloom_theory(n, m, k):
    return (1 - math.exp(-k * n / m)) ** k


# ------------------------------------------------------------------------------------------------- streams
def reservoir(stream, k, rng):
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
    u = np.unique(hashes)
    if len(u) < k:
        return float(len(u))
    kth = np.partition(u, k - 1)[k - 1]
    return (k - 1) / (float(kth) / 2.0 ** 64)


def ams_f2(items, counts: dict, k: int, groups: int, rng) -> float:
    """Alon, Matias and Szegedy (1996): Z = sum of s(x) over the stream, s a random +-1; Z^2 estimates F2.  The mean
    of k copies in each of ``groups`` groups, then the median of the group means."""
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
    p = (1 << 61) - 1
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
    return 1 - (1 - s ** rows) ** bands


# ------------------------------------------------------------------------------------------------- the probabilistic method
def moser_tardos(n, clauses, rng):
    """Resample the variables of a violated clause until none is violated.  Returns the number of resamplings."""
    x = [rng.random() < 0.5 for _ in range(n)]
    by_var: dict = {}
    for i, c in enumerate(clauses):
        for v, _ in c:
            by_var.setdefault(v, []).append(i)
    bad = {i for i, c in enumerate(clauses) if not any(x[v] == s for v, s in c)}
    steps = 0
    while bad:
        i = min(bad)
        for v, _ in clauses[i]:
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
