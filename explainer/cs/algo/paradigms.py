"""The great paradigms (Part 19): greedy, divide and conquer, dynamic programming, search.

Every function counts the work the scenes plot: comparisons, digit products, scalar multiplications, butterflies,
table cells, search nodes.  Pure Python unless a function says otherwise (the FFT multiplier uses numpy).
"""

from __future__ import annotations

import cmath
import heapq
import math
import random
from functools import lru_cache

import numpy as np


# ------------------------------------------------------------------------------------------------- greedy
def activity_selection(intervals, rule="finish"):
    """Greedy interval scheduling.  ``rule``: 'finish' (earliest finish, optimal), 'start' (earliest start),
    'shortest' or 'fewest' (fewest conflicts): the classic wrong rules.  Returns the chosen intervals."""
    if rule == "finish":
        order = sorted(intervals, key=lambda iv: iv[1])
    elif rule == "start":
        order = sorted(intervals, key=lambda iv: iv[0])
    elif rule == "shortest":
        order = sorted(intervals, key=lambda iv: iv[1] - iv[0])
    elif rule == "fewest":
        def conflicts(iv):
            return sum(1 for j in intervals if j is not iv and j[0] < iv[1] and iv[0] < j[1])
        order = sorted(intervals, key=conflicts)
    else:
        raise ValueError(rule)
    if rule == "finish":
        chosen = []
        last_finish = -math.inf
        for iv in order:
            if iv[0] >= last_finish:
                chosen.append(iv)
                last_finish = iv[1]
        return chosen
    chosen = []
    for iv in order:
        if all(iv[1] <= c[0] or c[1] <= iv[0] for c in chosen):
            chosen.append(iv)
    return sorted(chosen)


def max_compatible(intervals):
    """The true optimum by DP over intervals sorted by finish (weights 1): a check on the greedy."""
    ivs = sorted(intervals, key=lambda iv: iv[1])
    best = [0] * (len(ivs) + 1)
    import bisect
    finishes = [iv[1] for iv in ivs]
    for i, (s, f) in enumerate(ivs):
        j = bisect.bisect_right(finishes, s, 0, i)
        best[i + 1] = max(best[i], best[j] + 1)
    return best[-1]


def huffman(freq):
    """Huffman code lengths for a {symbol: weight} table (ties broken by insertion order)."""
    if any(not math.isfinite(w) or w < 0 for w in freq.values()):
        raise ValueError("Huffman weights must be finite and nonnegative")
    if not freq:
        return {}
    heap = [(w, i, {s: 0}) for i, (s, w) in enumerate(freq.items())]
    heapq.heapify(heap)
    k = len(heap)
    if k == 1:
        return {s: 1 for s in freq}
    while len(heap) > 1:
        w1, _, a = heapq.heappop(heap)
        w2, _, b = heapq.heappop(heap)
        merged = {s: d + 1 for s, d in a.items()}
        merged.update({s: d + 1 for s, d in b.items()})
        heapq.heappush(heap, (w1 + w2, k, merged))
        k += 1
    return heap[0][2]


def _coin_inputs(amount, coins):
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("amount must be a nonnegative integer")
    coins = list(coins)
    if any(not isinstance(c, int) or c <= 0 for c in coins):
        raise ValueError("coin denominations must be positive integers")
    return coins


def coin_greedy(amount, coins):
    coins = _coin_inputs(amount, coins)
    out = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c
            out.append(c)
    return out if amount == 0 else None


def coin_dp(amount, coins):
    coins = _coin_inputs(amount, coins)
    best = [0] + [math.inf] * amount
    take = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a], take[a] = best[a - c] + 1, c
    if math.isinf(best[amount]):
        return None
    out = []
    while amount > 0:
        out.append(take[amount])
        amount -= take[amount]
    return out


def greedy_max_weight(elements, weight, independent):
    """Maximum-weight independent-set greedy; skip negative weights.

    It is optimal for matroids; arbitrary independence systems need not be.
    This chooses an independent set, not a mandatory full basis.
    """
    chosen = []
    for e in sorted(elements, key=weight, reverse=True):
        if weight(e) < 0:
            continue
        if independent(chosen + [e]):
            chosen.append(e)
    return chosen


def forest_independent(n):
    def ok(edges):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for u, v, _ in edges:
            a, b = find(u), find(v)
            if a == b:
                return False
            parent[a] = b
        return True
    return ok


def matching_independent(edges):
    seen = set()
    for u, v, _ in edges:
        if u in seen or v in seen:
            return False
        seen.update((u, v))
    return True


def max_weight_matching_brute(edges):
    """Exact maximum-weight matching by search (small graphs only)."""
    best = 0.0
    edges = sorted((e for e in edges if e[2] >= 0), key=lambda e: -e[2])

    def go(i, used, w):
        nonlocal best
        best = max(best, w)
        rest = sum(e[2] for e in edges[i:])
        if w + rest <= best:
            return
        for j in range(i, len(edges)):
            u, v, x = edges[j]
            if u not in used and v not in used:
                go(j + 1, used | {u, v}, w + x)
    go(0, frozenset(), 0.0)
    return best


# ------------------------------------------------------------------------------------------------- multiplication
def to_digits(x, base=10):
    """Little-endian digit list."""
    if not isinstance(x, int) or x < 0 or not isinstance(base, int) or base < 2:
        raise ValueError("require a nonnegative integer and integer base at least two")
    if x == 0:
        return [0]
    out = []
    while x:
        x, r = divmod(x, base)
        out.append(r)
    return out


def from_digits(ds, base=10):
    x = 0
    for d in reversed(ds):
        x = x * base + d
    return x


def school_mul(a, b, count=None):
    """Grade-school multiplication of little-endian digit lists; ``count[0]`` += digit products."""
    out = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
            if count is not None:
                count[0] += 1
    return out


def _carry(ds, base=10):
    out, c = [], 0
    for d in ds:
        c += d
        out.append(c % base)
        c //= base
    if c < 0:
        raise ValueError("the represented value must be nonnegative")
    while c:
        out.append(c % base)
        c //= base
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def _add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def _sub(a, b):
    return [a[i] - (b[i] if i < len(b) else 0) for i in range(len(a))]


def karatsuba(a, b, count=None, cutoff=1):
    """Karatsuba on (uncarried) little-endian digit lists: three half-size products instead of four."""
    if not isinstance(cutoff, int) or cutoff < 1:
        raise ValueError("cutoff must be a positive integer")
    n = max(len(a), len(b))
    if n <= cutoff:
        return school_mul(a, b, count)
    a = a + [0] * (n - len(a))
    b = b + [0] * (n - len(b))
    m = n // 2
    a0, a1, b0, b1 = a[:m], a[m:], b[:m], b[m:]
    z0 = karatsuba(a0, b0, count, cutoff)
    z2 = karatsuba(a1, b1, count, cutoff)
    z1 = _sub(_sub(karatsuba(_add(a0, a1), _add(b0, b1), count, cutoff), z0 + [0] * 0), z2)
    out = [0] * (2 * n + 1)
    for i, x in enumerate(z0):
        out[i] += x
    for i, x in enumerate(z1):
        out[i + m] += x
    for i, x in enumerate(z2):
        out[i + 2 * m] += x
    return out


def mul_count(n, method):
    """Digit products to multiply two n-digit numbers (n a power of two): n^2 or 3^lg n."""
    if method == "school":
        return n * n
    k = int(round(math.log2(n)))
    return 3 ** k


# ------------------------------------------------------------------------------------------------- Strassen
def strassen(A, B, cutoff=64, count=None):
    """Strassen's seven products (numpy blocks; n a power of two).  ``count`` = [mults, adds] at scalar level for
    the recursion above the cutoff, with the cutoff blocks done by numpy and counted as n^3 mults."""
    A, B = np.asarray(A), np.asarray(B)
    if (A.ndim != 2 or B.ndim != 2 or A.shape != B.shape or A.shape[0] != A.shape[1]
            or not A.shape[0] or A.shape[0] & (A.shape[0] - 1) or not isinstance(cutoff, int) or cutoff < 1):
        raise ValueError("require equal square power-of-two matrices and positive integer cutoff")
    n = A.shape[0]
    if n <= cutoff:
        if count is not None:
            count[0] += n ** 3
            count[1] += n ** 2 * (n - 1)
        return A @ B
    m = n // 2
    A11, A12, A21, A22 = A[:m, :m], A[:m, m:], A[m:, :m], A[m:, m:]
    B11, B12, B21, B22 = B[:m, :m], B[:m, m:], B[m:, :m], B[m:, m:]
    M1 = strassen(A11 + A22, B11 + B22, cutoff, count)
    M2 = strassen(A21 + A22, B11, cutoff, count)
    M3 = strassen(A11, B12 - B22, cutoff, count)
    M4 = strassen(A22, B21 - B11, cutoff, count)
    M5 = strassen(A11 + A12, B22, cutoff, count)
    M6 = strassen(A21 - A11, B11 + B12, cutoff, count)
    M7 = strassen(A12 - A22, B21 + B22, cutoff, count)
    if count is not None:
        count[1] += 18 * m * m
    C = np.empty_like(A)
    C[:m, :m] = M1 + M4 - M5 + M7
    C[:m, m:] = M3 + M5
    C[m:, :m] = M2 + M4
    C[m:, m:] = M1 - M2 + M3 + M6
    return C


def strassen_counts(n, cutoff=1):
    """Scalar multiplications and additions for n x n (n = 2^k), recursing to ``cutoff``."""
    if n <= cutoff:
        return n ** 3, n ** 2 * (n - 1)
    m, a = strassen_counts(n // 2, cutoff)
    return 7 * m, 7 * a + 18 * (n // 2) ** 2


# ------------------------------------------------------------------------------------------------- FFT
def dft(a, count=None):
    n = len(a)
    out = []
    for k in range(n):
        s = 0j
        for j in range(n):
            s += a[j] * cmath.exp(-2j * math.pi * j * k / n)
        out.append(s)
    if count is not None:
        count[0] += n * n
    return out


def fft(a, count=None, invert=False):
    """Recursive radix-2 Cooley–Tukey; ``count[0]`` += butterflies (one complex multiply each)."""
    if len(a) == 0:
        return []
    if len(a) & (len(a) - 1):
        raise ValueError("radix-two FFT length must be a power of two")
    n = len(a)
    if n == 1:
        return list(a)
    even = fft(a[0::2], count, invert)
    odd = fft(a[1::2], count, invert)
    sign = 1 if invert else -1
    out = [0j] * n
    for k in range(n // 2):
        t = cmath.exp(sign * 2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + n // 2] = even[k] - t
    if count is not None:
        count[0] += n // 2
    return out


def ifft(a):
    n = len(a)
    return [x / n for x in fft(a, invert=True)]


def bit_reverse(i, bits):
    r = 0
    for _ in range(bits):
        r = (r << 1) | (i & 1)
        i >>= 1
    return r


def poly_mul_fft(p, q):
    """Coefficients of p*q by evaluating at roots of unity, multiplying pointwise, interpolating."""
    if not p or not q:
        return []
    n = 1
    while n < len(p) + len(q) - 1:
        n *= 2
    fp = fft(list(p) + [0] * (n - len(p)))
    fq = fft(list(q) + [0] * (n - len(q)))
    r = ifft([x * y for x, y in zip(fp, fq)])
    return [round(x.real) for x in r[:len(p) + len(q) - 1]]


def fft_bigmul(x, y, chunk=4):
    """Experimental floating-FFT candidate for nonnegative integer multiplication.

    Supported decimal chunks are 1..4 digits. Floating arithmetic does not give
    a uniform exactness guarantee: callers must verify against exact arithmetic.
    The course checks every timed end-to-end product outside the timed region.
    """
    if (not isinstance(x, int) or not isinstance(y, int) or min(x, y) < 0
            or not isinstance(chunk, int) or not 1 <= chunk <= 4):
        raise ValueError("require nonnegative integers and decimal chunk in1..4")
    import sys
    sys.set_int_max_str_digits(0)          # these are huge numbers on purpose
    sx, sy = str(x), str(y)
    def split(s):
        s = s[::-1]
        return np.array([int(s[i:i + chunk][::-1]) for i in range(0, len(s), chunk)], dtype=np.float64)
    a, b = split(sx), split(sy)
    n = 1
    while n < len(a) + len(b):
        n *= 2
    c = np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(b, n), n)
    c = np.rint(c[:len(a) + len(b)])
    if not np.all(np.isfinite(c)) or np.min(c) < 0 or np.max(c) >= 2 ** 63:
        raise ArithmeticError("FFT coefficients cannot be safely carried as int64")
    c = c.astype(np.int64)
    base = 10 ** chunk
    out, carry = [], 0
    for v in c.tolist():
        carry += v
        out.append(carry % base)
        carry //= base
    while carry:
        out.append(carry % base)
        carry //= base
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return int(str(out[-1]) + "".join(str(d).zfill(chunk) for d in reversed(out[:-1])))


@lru_cache(None)
def _is_prime(n):
    if not isinstance(n, int) or n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % p for p in range(3, math.isqrt(n) + 1, 2))


def ntt(a, mod=998244353, root=3, invert=False):
    """Number-theoretic transform over Z/mod (mod = 119 * 2^23 + 1): the FFT with exact arithmetic."""
    if not _is_prime(mod) or not isinstance(root, int):
        raise ValueError("require a prime modulus and integer root")
    if len(a) == 0:
        return []
    n = len(a)
    if n & (n - 1) or (mod - 1) % n:
        raise ValueError("transform length must be a power of two dividing mod-1")
    omega = pow(root, (mod - 1) // n, mod)
    if pow(omega, n, mod) != 1 or (n > 1 and pow(omega, n // 2, mod) == 1):
        raise ValueError("root does not induce the required transform order")
    a = [x % mod for x in a]
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        w = pow(root, (mod - 1) // length, mod)
        if invert:
            w = pow(w, mod - 2, mod)
        for i in range(0, n, length):
            wn = 1
            for k in range(length // 2):
                u, v = a[i + k], a[i + k + length // 2] * wn % mod
                a[i + k], a[i + k + length // 2] = (u + v) % mod, (u - v) % mod
                wn = wn * w % mod
        length <<= 1
    if invert:
        inv = pow(n, mod - 2, mod)
        a = [x * inv % mod for x in a]
    return a


def chudnovsky(digits, *, certificate=None):
    """Return floor(pi *10**digits), certified by an integer interval.

    Consecutive alternating Chudnovsky partial sums bracket the positive series;
    floor(sqrt(10005)*10**precision) and its successor bracket the square root.
    Increase precision until both induced pi bounds have the same integer part.
    Optional certificate receives the two matching floors, terms and guard digits.
    """
    if not isinstance(digits, int) or digits < 0:
        raise ValueError("decimal places must be a nonnegative integer")
    C3_24 = 640320 ** 3 // 24

    def bs(a, b):
        if b - a == 1:
            if a == 0:
                P = Q = 1
            else:
                P = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
                Q = a * a * a * C3_24
            T = P * (13591409 + 545140134 * a)
            if a & 1:
                T = -T
            return P, Q, T
        m = (a + b) // 2
        P1, Q1, T1 = bs(a, m)
        P2, Q2, T2 = bs(m, b)
        return P1 * P2, Q1 * Q2, Q2 * T1 + P1 * T2

    guard = 10
    while True:
        terms = (digits + guard) // 14 + 2
        P, Q, T = bs(0, terms)
        step_den = terms ** 3 * C3_24
        numerator = T * step_den
        next_term = P * (6 * terms - 5) * (2 * terms - 1) * (6 * terms - 1)
        next_term *= 13591409 + 545140134 * terms
        successor = numerator + (-next_term if terms & 1 else next_term)
        lower_s, upper_s = sorted((numerator, successor))
        denominator = Q * step_den
        scale = 10 ** (digits + guard)
        root = math.isqrt(10005 * scale * scale)
        lower = 426880 * root * denominator // (10 ** guard * upper_s)
        upper = 426880 * (root + 1) * denominator // (10 ** guard * lower_s)
        if lower == upper:
            if certificate is not None:
                certificate.update(terms=terms, guard_digits=guard,
                                   lower_floor=lower, upper_floor=upper,
                                   alternating_series_and_integer_sqrt=True)
            return lower
        guard += 10



# ------------------------------------------------------------------------------------------------- closest pair
def closest_brute(pts):
    best, pair, n = math.inf, None, 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.dist(pts[i], pts[j])
            n += 1
            if d < best:
                best, pair = d, (pts[i], pts[j])
    return best, pair, n


def closest_pair(pts):
    """Shamos–Hoey divide and conquer.  Returns (distance, pair, distance computations, most strip comparisons
    made by any one point)."""
    px = sorted(pts)
    stats = {"dist": 0, "strip_max": 0}

    def rec(p):
        if len(p) <= 3:
            best, pair, n = closest_brute(p)
            stats["dist"] += n
            return best, pair, sorted(p, key=lambda q: q[1])
        m = len(p) // 2
        xm = p[m][0]
        dl, pl, yl = rec(p[:m])
        dr, pr, yr = rec(p[m:])
        best, pair = (dl, pl) if dl <= dr else (dr, pr)
        ys, i, j = [], 0, 0
        while i < len(yl) or j < len(yr):
            if j >= len(yr) or (i < len(yl) and yl[i][1] <= yr[j][1]):
                ys.append(yl[i])
                i += 1
            else:
                ys.append(yr[j])
                j += 1
        strip = [q for q in ys if abs(q[0] - xm) < best]
        for a in range(len(strip)):
            k = 0
            for b in range(a + 1, len(strip)):
                if strip[b][1] - strip[a][1] >= best:
                    break
                k += 1
                stats["dist"] += 1
                d = math.dist(strip[a], strip[b])
                if d < best:
                    best, pair = d, (strip[a], strip[b])
            stats["strip_max"] = max(stats["strip_max"], k)
        return best, pair, ys
    best, pair, _ = rec(px)
    return best, pair, stats["dist"], stats["strip_max"]


# ------------------------------------------------------------------------------------------------- DP
def fib_naive_calls(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("size must be a nonnegative integer")
    calls = [0]

    def f(k):
        calls[0] += 1
        return k if k < 2 else f(k - 1) + f(k - 2)
    return f(n), calls[0]


def fib_memo_calls(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("size must be a nonnegative integer")
    calls = [0]
    memo = {}

    def f(k):
        calls[0] += 1
        if k in memo:
            return memo[k]
        memo[k] = k if k < 2 else f(k - 1) + f(k - 2)
        return memo[k]
    return f(n), calls[0]


def edit_distance(a, b):
    """Wagner–Fischer: the table and an optimal alignment (list of ops: '=', 'sub', 'ins', 'del')."""
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    ops, i, j, path = [], n, m, [(n, m)]
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            ops.append("=" if a[i - 1] == b[j - 1] else "sub")
            i, j = i - 1, j - 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            ops.append("del")
            i -= 1
        else:
            ops.append("ins")
            j -= 1
        path.append((i, j))
    return D, ops[::-1], path[::-1]


def lcs(a, b):
    n, m = len(a), len(b)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            L[i + 1][j + 1] = L[i][j] + 1 if a[i] == b[j] else max(L[i][j + 1], L[i + 1][j])
    out, i, j = [], n, m
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return L[n][m], out[::-1]


def knapsack(items, W):
    """0/1 knapsack, O(nW): items [(weight, value)].  Returns (best value, chosen indices, cells filled)."""
    n = len(items)
    V = [[0] * (W + 1) for _ in range(n + 1)]
    for i, (w, v) in enumerate(items, 1):
        row, prev = V[i], V[i - 1]
        for c in range(W + 1):
            row[c] = prev[c] if w > c else max(prev[c], prev[c - w] + v)
    chosen, c = [], W
    for i in range(n, 0, -1):
        if V[i][c] != V[i - 1][c]:
            chosen.append(i - 1)
            c -= items[i - 1][0]
    return V[n][W], chosen[::-1], (n + 1) * (W + 1)


def knapsack_greedy(items, W):
    """By value per weight: a natural greedy that fails."""
    total, c = 0, W
    for w, v in sorted(items, key=lambda it: -it[1] / it[0]):
        if w <= c:
            c -= w
            total += v
    return total


def matrix_chain(dims):
    """Cheapest parenthesization of A1 … An with Ai of size dims[i-1] x dims[i].  Returns (cost, bracket string)."""
    if len(dims) < 2:
        return 0, ""
    if any(d <= 0 for d in dims):
        raise ValueError("matrix dimensions must be positive")
    n = len(dims) - 1
    C = [[0] * n for _ in range(n)]
    S = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            C[i][j] = math.inf
            for k in range(i, j):
                c = C[i][k] + C[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if c < C[i][j]:
                    C[i][j], S[i][j] = c, k

    def br(i, j):
        return f"A{i + 1}" if i == j else f"({br(i, S[i][j])}{br(S[i][j] + 1, j)})"
    return C[0][n - 1], br(0, n - 1)


def chain_cost(dims, order):
    """Cost of left-to-right multiplication (no reordering), for comparison."""
    r, c, total = dims[0], dims[1], 0
    for k in range(2, len(dims)):
        total += r * c * dims[k]
        c = dims[k]
    return total


def optimal_bst(p, knuth=False):
    """Optimal BST for access probabilities p[0..n-1] (successful searches only).  Returns (expected cost,
    inner-loop iterations): O(n^3) plainly, O(n^2) with Knuth's root-monotonicity speedup."""
    n = len(p)
    pre = [0.0]
    for x in p:
        pre.append(pre[-1] + x)
    E = [[0.0] * (n + 1) for _ in range(n + 2)]
    R = [[0] * (n + 1) for _ in range(n + 2)]
    it = 0
    for i in range(1, n + 1):
        E[i][i] = p[i - 1]
        R[i][i] = i
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            w = pre[j] - pre[i - 1]
            lo, hi = (R[i][j - 1], R[i + 1][j]) if knuth else (i, j)
            best, br = math.inf, lo
            for r in range(lo, hi + 1):
                it += 1
                c = (E[i][r - 1] if r > i else 0) + (E[r + 1][j] if r < j else 0)
                if c < best:
                    best, br = c, r
            E[i][j], R[i][j] = best + w, br
    return E[1][n], it


def tree_mis(children, root, weight):
    """Maximum-weight independent set on a rooted tree by iterative postorder.

    The empty independent set is allowed. Reject cycles/shared children; every
    reachable vertex has exactly one parent except the root. No recursion limit
    or process-wide interpreter setting is changed.
    """
    seen, values, todo = set(), {}, [(root, False)]
    while todo:
        v, finished = todo.pop()
        if finished:
            take, skip = weight[v], 0
            for c in children.get(v, []):
                t, s = values[c]
                take += s
                skip += max(t, s)
            values[v] = take, skip
        else:
            if v in seen:
                raise ValueError("children must describe a rooted tree")
            seen.add(v)
            todo.append((v, True))
            todo.extend((c, False) for c in reversed(children.get(v, [])))
    return max(values[root])


def tree_mis_brute(n, edges, weight):
    best = 0
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    for mask in range(1 << n):
        ok = True
        s = 0
        for v in range(n):
            if mask >> v & 1:
                if any(mask >> u & 1 for u in adj[v]):
                    ok = False
                    break
                s += weight[v]
        if ok:
            best = max(best, s)
    return best


# ------------------------------------------------------------------------------------------------- search
def queens(n, bitmask=True):
    """Count n-queens solutions by backtracking; returns (solutions, nodes visited)."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("size must be a nonnegative integer")
    nodes = [0]
    if bitmask:
        full = (1 << n) - 1

        def go(cols, d1, d2):
            nodes[0] += 1
            if cols == full:
                return 1
            total = 0
            free = full & ~(cols | d1 | d2)
            while free:
                bit = free & -free
                free ^= bit
                total += go(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1)
            return total
        return go(0, 0, 0), nodes[0]
    placed = []

    def go2(r):
        nodes[0] += 1
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if all(c != pc and abs(c - pc) != r - pr for pr, pc in enumerate(placed)):
                placed.append(c)
                total += go2(r + 1)
                placed.pop()
        return total
    return go2(0), nodes[0]


def queens_brute_count(n):
    """Placements a no-pruning search would examine: n^n (one queen per row)."""
    return n ** n


class DLX:
    """Knuth's Algorithm X with dancing links (2000): exact cover.  ``updates`` counts link changes."""

    def __init__(self, ncols, rows):
        self.L, self.R, self.U, self.D, self.C, self.S, self.row_of = [], [], [], [], [], [], []
        self.updates = 0
        self.nodes = 0
        for i in range(ncols + 1):
            self.L.append(i - 1)
            self.R.append(i + 1)
            self.U.append(i)
            self.D.append(i)
            self.C.append(i)
            self.row_of.append(-1)
        self.L[0], self.R[ncols] = ncols, 0
        self.S = [0] * (ncols + 1)
        for r, cols in enumerate(rows):
            first = None
            for c in cols:
                c += 1
                k = len(self.L)
                self.C.append(c)
                self.row_of.append(r)
                self.U.append(self.U[c])
                self.D.append(c)
                self.D[self.U[c]] = k
                self.U[c] = k
                self.S[c] += 1
                if first is None:
                    first = k
                    self.L.append(k)
                    self.R.append(k)
                else:
                    self.L.append(self.L[first])
                    self.R.append(first)
                    self.R[self.L[first]] = k
                    self.L[first] = k

    def cover(self, c):
        L, R, U, D, C, S = self.L, self.R, self.U, self.D, self.C, self.S
        R[L[c]], L[R[c]] = R[c], L[c]
        self.updates += 2
        i = D[c]
        while i != c:
            j = R[i]
            while j != i:
                D[U[j]], U[D[j]] = D[j], U[j]
                S[C[j]] -= 1
                self.updates += 2
                j = R[j]
            i = D[i]

    def uncover(self, c):
        L, R, U, D, C, S = self.L, self.R, self.U, self.D, self.C, self.S
        i = U[c]
        while i != c:
            j = L[i]
            while j != i:
                S[C[j]] += 1
                D[U[j]] = U[D[j]] = j
                self.updates += 2
                j = L[j]
            i = U[i]
        R[L[c]] = L[R[c]] = c
        self.updates += 2

    def solve(self, limit=1):
        if not isinstance(limit, int) or limit < 1:
            raise ValueError("solution limit must be positive")
        self.nodes = self.updates = 0
        sols, cur = [], []

        def go():
            self.nodes += 1
            if self.R[0] == 0:
                sols.append(list(cur))
                return len(sols) >= limit
            c, best = 0, math.inf
            j = self.R[0]
            while j != 0:
                if self.S[j] < best:
                    c, best = j, self.S[j]
                j = self.R[j]
            self.cover(c)
            r = self.D[c]
            while r != c:
                cur.append(self.row_of[r])
                j = self.R[r]
                while j != r:
                    self.cover(self.C[j])
                    j = self.R[j]
                stopped = go()
                j = self.L[r]
                while j != r:
                    self.uncover(self.C[j])
                    j = self.L[j]
                cur.pop()
                if stopped:
                    self.uncover(c)
                    return True
                r = self.D[r]
            self.uncover(c)
            return False
        go()
        return sols


def _sudoku_grid(grid):
    if not isinstance(grid, str) or len(grid) != 81 or any(c not in "0123456789." for c in grid):
        raise ValueError("Sudoku grid must contain81 digits or dots")
    g = [0 if c == "." else int(c) for c in grid]
    units = [[9*r+c for c in range(9)] for r in range(9)]
    units += [[9*r+c for r in range(9)] for c in range(9)]
    units += [[9*(br+r)+bc+c for r in range(3) for c in range(3)]
              for br in (0,3,6) for bc in (0,3,6)]
    for unit in units:
        values = [g[i] for i in unit if g[i]]
        if len(set(values)) != len(values):
            return None
    return g


def sudoku_rows(grid):
    """Exact-cover rows for a 9x9 sudoku (string of 81 digits, 0 or . for blanks): 324 columns."""
    g = _sudoku_grid(grid)
    if g is None:
        raise ValueError("inconsistent Sudoku givens")
    rows, meaning = [], []
    for r in range(9):
        for c in range(9):
            ch = grid[9 * r + c]
            ds = [int(ch)] if ch not in "0." else range(1, 10)
            for d in ds:
                b = 3 * (r // 3) + c // 3
                rows.append([9 * r + c, 81 + 9 * r + d - 1, 162 + 9 * c + d - 1, 243 + 9 * b + d - 1])
                meaning.append((r, c, d))
    return rows, meaning


def solve_sudoku(grid):
    if _sudoku_grid(grid) is None:
        return None, 0, 0, 0
    rows, meaning = sudoku_rows(grid)
    x = DLX(324, rows)
    sols = x.solve(limit=2)
    out = None
    if sols:
        g = [0] * 81
        for k in sols[0]:
            r, c, d = meaning[k]
            g[9 * r + c] = d
        out = "".join(map(str, g))
    return out, x.nodes, x.updates, len(sols)


def sudoku_naive(grid):
    """Plain backtracking, cells in reading order: (solution, nodes)."""
    g = _sudoku_grid(grid)
    if g is None:
        return None, 0
    nodes = [0]

    def ok(i, d):
        r, c = divmod(i, 9)
        for k in range(9):
            if g[9 * r + k] == d or g[9 * k + c] == d:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for rr in range(br, br + 3):
            for cc in range(bc, bc + 3):
                if g[9 * rr + cc] == d:
                    return False
        return True

    def go(i):
        nodes[0] += 1
        while i < 81 and g[i]:
            i += 1
        if i == 81:
            return True
        for d in range(1, 10):
            if ok(i, d):
                g[i] = d
                if go(i + 1):
                    return True
                g[i] = 0
        return False
    solved = go(0)
    return ("".join(map(str, g)) if solved else None), nodes[0]


# ------------------------------------------------------------------------------------------------- max subarray
def maxsub_cubic(a):
    if not a:
        raise ValueError("maximum subarray requires a nonempty sequence")
    best = a[0]
    n = len(a)
    for i in range(n):
        for j in range(i, n):
            s = 0
            for k in range(i, j + 1):
                s += a[k]
            best = max(best, s)
    return best


def maxsub_quadratic(a):
    if not a:
        raise ValueError("maximum subarray requires a nonempty sequence")
    best = a[0]
    for i in range(len(a)):
        s = 0
        for j in range(i, len(a)):
            s += a[j]
            if s > best:
                best = s
    return best


def maxsub_divide(a, lo=0, hi=None):
    if not a or lo < 0 or (hi is not None and (hi > len(a) or hi <= lo)):
        raise ValueError("maximum subarray requires a nonempty valid interval")
    if hi is None:
        hi = len(a)
    if hi - lo == 1:
        return a[lo]
    mid = (lo + hi) // 2
    best = max(maxsub_divide(a, lo, mid), maxsub_divide(a, mid, hi))
    s, left = 0, -math.inf
    for i in range(mid - 1, lo - 1, -1):
        s += a[i]
        left = max(left, s)
    s, right = 0, -math.inf
    for i in range(mid, hi):
        s += a[i]
        right = max(right, s)
    return max(best, left + right)


def maxsub_kadane(a):
    if not a:
        raise ValueError("maximum subarray requires a nonempty sequence")
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
