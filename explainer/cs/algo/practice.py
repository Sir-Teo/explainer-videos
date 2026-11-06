"""Part 24's instrument: the everyday tools of real code, each counting its own work.

    prefix_sums(a), range_sum(P, l, r), diff_apply(n, updates), integral_image(img), box_sum(I, r0, c0, r1, c1)
    Fenwick(n): add(i, v), prefix(i), lowbit(i), responsibility(i); counts the nodes each operation touches
    SegTree(a, op): query(l, r), update(i, v); LazySegTree(a): range_add(l, r, v), range_sum(l, r); node counts
    SparseTable(a): query(l, r) in O(1) by idempotence; lca_euler(tree, root) and BinaryLift(tree, root)
    cartesian_tree(a): parent array (RMQ on a is LCA on this tree)
    sliding_max(a, k, trace), next_greater(a), largest_rectangle(h)
    binary_search_answer(lo, hi, ok), galloping(a, x), ternary_max(f, lo, hi)
    popcount, lowbit, gray, submasks(m), transitive_closure_bits(adj), lcs_bitparallel(a, b), lcs_dp(a, b)
    subset_sum_mitm(a, t), subset_sum_brute(a, t), SqrtDecomp(a), mo_distinct(a, queries)

Everything here is plain Python and is checked against brute force in tests/test_cs24_practice.py; the timings that
depend on the machine (layouts, SIMD, hashing, sorting) are C programs in videos/cs/cs24/compute.py.
"""

from __future__ import annotations

import bisect
import math
from collections import deque

# --------------------------------------------------------------------------------------------------- prefix sums


def prefix_sums(a):
    P = [0]
    for x in a:
        P.append(P[-1] + x)
    return P


def range_sum(P, l, r):
    """Sum of a[l..r] inclusive, from the prefix sums P."""
    return P[r + 1] - P[l]


def diff_apply(n, updates):
    """Apply 'add v to a[l..r]' updates in O(1) each with a difference array; one prefix sum at the end."""
    D = [0] * (n + 1)
    for l, r, v in updates:
        D[l] += v
        D[r + 1] -= v
    out, s = [], 0
    for i in range(n):
        s += D[i]
        out.append(s)
    return out


def integral_image(img):
    """I[r][c] = sum of img[0..r-1][0..c-1] (Viola and Jones, 2001; Crow, 1984)."""
    R, C = len(img), len(img[0])
    I = [[0] * (C + 1) for _ in range(R + 1)]
    for r in range(R):
        row = 0
        for c in range(C):
            row += img[r][c]
            I[r + 1][c + 1] = I[r][c + 1] + row
    return I


def box_sum(I, r0, c0, r1, c1):
    """Sum of img[r0..r1][c0..c1] inclusive: four lookups."""
    return I[r1 + 1][c1 + 1] - I[r0][c1 + 1] - I[r1 + 1][c0] + I[r0][c0]


# --------------------------------------------------------------------------------------------------- Fenwick


def lowbit(i: int) -> int:
    return i & -i


class Fenwick:
    """Fenwick's binary indexed tree (1994), 1-based. Node i holds the sum of a(i - lowbit(i), i]."""

    def __init__(self, n: int):
        self.n = n
        self.t = [0] * (n + 1)
        self.touched = 0

    @staticmethod
    def responsibility(i: int) -> tuple[int, int]:
        return i - lowbit(i) + 1, i

    def add(self, i: int, v) -> list[int]:
        path = []
        while i <= self.n:
            self.t[i] += v
            path.append(i)
            i += lowbit(i)
        self.touched += len(path)
        return path

    def prefix(self, i: int):
        s, path = 0, []
        while i > 0:
            s += self.t[i]
            path.append(i)
            i -= lowbit(i)
        self.touched += len(path)
        self.last_path = path
        return s

    def range(self, l: int, r: int):
        return self.prefix(r) - self.prefix(l - 1)


# --------------------------------------------------------------------------------------------------- segment trees


class SegTree:
    """Iterative-free recursive segment tree over any monoid (op, identity); counts the nodes each query visits."""

    def __init__(self, a, op=lambda x, y: x + y, ident=0):
        self.n = len(a)
        self.op, self.id = op, ident
        self.t = [ident] * (4 * self.n)
        self.visits = 0
        self._build(1, 0, self.n - 1, a)

    def _build(self, k, lo, hi, a):
        if lo == hi:
            self.t[k] = a[lo]
            return
        m = (lo + hi) // 2
        self._build(2 * k, lo, m, a)
        self._build(2 * k + 1, m + 1, hi, a)
        self.t[k] = self.op(self.t[2 * k], self.t[2 * k + 1])

    def query(self, l, r, cover=None):
        """op over a[l..r]; if cover is a list, the canonical covering nodes (k, lo, hi) are appended to it."""
        return self._q(1, 0, self.n - 1, l, r, cover)

    def _q(self, k, lo, hi, l, r, cover):
        self.visits += 1
        if r < lo or hi < l:
            return self.id
        if l <= lo and hi <= r:
            if cover is not None:
                cover.append((k, lo, hi))
            return self.t[k]
        m = (lo + hi) // 2
        return self.op(self._q(2 * k, lo, m, l, r, cover), self._q(2 * k + 1, m + 1, hi, l, r, cover))

    def update(self, i, v):
        self._u(1, 0, self.n - 1, i, v)

    def _u(self, k, lo, hi, i, v):
        self.visits += 1
        if lo == hi:
            self.t[k] = v
            return
        m = (lo + hi) // 2
        if i <= m:
            self._u(2 * k, lo, m, i, v)
        else:
            self._u(2 * k + 1, m + 1, hi, i, v)
        self.t[k] = self.op(self.t[2 * k], self.t[2 * k + 1])


class LazySegTree:
    """Range add, range sum, with lazy propagation: an update is O(log n) because pushes are deferred."""

    def __init__(self, a):
        self.n = len(a)
        self.s = [0] * (4 * self.n)
        self.lz = [0] * (4 * self.n)
        self.visits = 0
        self._build(1, 0, self.n - 1, a)

    def _build(self, k, lo, hi, a):
        if lo == hi:
            self.s[k] = a[lo]
            return
        m = (lo + hi) // 2
        self._build(2 * k, lo, m, a)
        self._build(2 * k + 1, m + 1, hi, a)
        self.s[k] = self.s[2 * k] + self.s[2 * k + 1]

    def _push(self, k, lo, hi):
        if self.lz[k]:
            m = (lo + hi) // 2
            for c, a, b in ((2 * k, lo, m), (2 * k + 1, m + 1, hi)):
                self.s[c] += self.lz[k] * (b - a + 1)
                self.lz[c] += self.lz[k]
            self.lz[k] = 0

    def range_add(self, l, r, v, k=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        self.visits += 1
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self.s[k] += v * (hi - lo + 1)
            self.lz[k] += v
            return
        self._push(k, lo, hi)
        m = (lo + hi) // 2
        self.range_add(l, r, v, 2 * k, lo, m)
        self.range_add(l, r, v, 2 * k + 1, m + 1, hi)
        self.s[k] = self.s[2 * k] + self.s[2 * k + 1]

    def range_sum(self, l, r, k=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        self.visits += 1
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.s[k]
        self._push(k, lo, hi)
        m = (lo + hi) // 2
        return self.range_sum(l, r, 2 * k, lo, m) + self.range_sum(l, r, 2 * k + 1, m + 1, hi)


# --------------------------------------------------------------------------------------------------- RMQ and LCA


class SparseTable:
    """O(n log n) preprocessing; a minimum query is two overlapping power-of-two windows (min is idempotent)."""

    def __init__(self, a):
        self.a = list(a)
        n = len(a)
        self.lg = [0] * (n + 1)
        for i in range(2, n + 1):
            self.lg[i] = self.lg[i // 2] + 1
        self.t = [list(range(n))]  # indices of minima
        j = 1
        while (1 << j) <= n:
            prev = self.t[-1]
            half = 1 << (j - 1)
            row = []
            for i in range(n - (1 << j) + 1):
                x, y = prev[i], prev[i + half]
                row.append(x if self.a[x] <= self.a[y] else y)
            self.t.append(row)
            j += 1

    def argmin(self, l, r):
        j = self.lg[r - l + 1]
        x, y = self.t[j][l], self.t[j][r - (1 << j) + 1]
        return x if self.a[x] <= self.a[y] else y

    def query(self, l, r):
        return self.a[self.argmin(l, r)]

    def cells(self):
        return sum(len(r) for r in self.t)


def euler_tour(children, root):
    """Euler tour of a rooted tree: (order of visits, depth at each visit, first visit index of each node)."""
    order, depth, first = [], [], {}
    stack = [(root, 0, 0)]
    while stack:
        v, d, i = stack.pop()
        if i == 0:
            first[v] = len(order)
        order.append(v)
        depth.append(d)
        ch = children.get(v, [])
        if i < len(ch):
            stack.append((v, d, i + 1))
            stack.append((ch[i], d + 1, 0))
    return order, depth, first


class EulerLCA:
    def __init__(self, children, root):
        self.order, self.depth, self.first = euler_tour(children, root)
        self.st = SparseTable(self.depth)

    def lca(self, u, v):
        a, b = sorted((self.first[u], self.first[v]))
        return self.order[self.st.argmin(a, b)]


class BinaryLift:
    """up[j][v] = the 2^j-th ancestor of v; LCA by lifting the deeper node, then both, by powers of two."""

    def __init__(self, parent, root):
        self.n = len(parent)
        self.depth = [0] * self.n
        order = [root]
        kids = {}
        for v, p in enumerate(parent):
            if v != root:
                kids.setdefault(p, []).append(v)
        for v in order:
            for c in kids.get(v, []):
                self.depth[c] = self.depth[v] + 1
                order.append(c)
        self.L = max(1, (self.n).bit_length())
        self.up = [[root if v == root else parent[v] for v in range(self.n)]]
        for j in range(1, self.L):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(self.n)])
        self.steps = 0

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        d = self.depth[u] - self.depth[v]
        j = 0
        while d:
            if d & 1:
                u = self.up[j][u]
                self.steps += 1
            d >>= 1
            j += 1
        if u == v:
            return u
        for j in range(self.L - 1, -1, -1):
            if self.up[j][u] != self.up[j][v]:
                u, v = self.up[j][u], self.up[j][v]
                self.steps += 1
        return self.up[0][u]


def cartesian_tree(a):
    """Parent array of the min-Cartesian tree (root has parent -1), built in O(n) with a stack."""
    parent = [-1] * len(a)
    st = []
    for i, x in enumerate(a):
        last = -1
        while st and a[st[-1]] > x:
            last = st.pop()
        if st:
            parent[i] = st[-1]
        if last != -1:
            parent[last] = i
        st.append(i)
    return parent


# --------------------------------------------------------------------------------------------------- monotonic structures


def sliding_max(a, k, trace=False):
    """Maximum of every window of k, by a deque of indices whose values decrease. O(n): each index enters and
    leaves once. With trace, also the deque after each step."""
    dq, out, tr = deque(), [], []
    pops = 0
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
            pops += 1
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
            pops += 1
        if i >= k - 1:
            out.append(a[dq[0]])
        if trace:
            tr.append(list(dq))
    return (out, tr, pops) if trace else out


def next_greater(a):
    """For each i, the index of the next element greater than a[i], or -1: one stack, O(n)."""
    res = [-1] * len(a)
    st = []
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = i
        st.append(i)
    return res


def largest_rectangle(h):
    """Largest rectangle under a histogram (the classic monotonic-stack problem): (area, left, right, height)."""
    st, best = [], (0, 0, -1, 0)
    for i in range(len(h) + 1):
        x = h[i] if i < len(h) else 0
        start = i
        while st and st[-1][1] >= x:
            j, y = st.pop()
            area = y * (i - j)
            if area > best[0]:
                best = (area, j, i - 1, y)
            start = j
        st.append((start, x))
    return best


def largest_rectangle_brute(h):
    best = 0
    for i in range(len(h)):
        m = h[i]
        for j in range(i, len(h)):
            m = min(m, h[j])
            best = max(best, m * (j - i + 1))
    return best


# --------------------------------------------------------------------------------------------------- searching


def binary_search_answer(lo, hi, ok):
    """Smallest x in [lo, hi] with ok(x), for a monotone predicate (False...False True...True); calls counted."""
    calls = 0
    while lo < hi:
        m = (lo + hi) // 2
        calls += 1
        if ok(m):
            hi = m
        else:
            lo = m + 1
    return lo, calls


def ship_within_days(w, days):
    """The least capacity that ships the packages w, in order, within `days` days (an interview classic)."""
    def ok(cap):
        d, load = 1, 0
        for x in w:
            if load + x > cap:
                d += 1
                load = 0
            load += x
        return d <= days
    return binary_search_answer(max(w), sum(w), ok)


def galloping(a, x, start=0):
    """Exponential search from `start` (Bentley and Yao, 1976): O(log d) for an answer d places away."""
    probes = 0
    if start >= len(a) or a[start] >= x:
        return start, 1
    step = 1
    i = start
    while i + step < len(a) and a[i + step] < x:
        i += step
        step *= 2
        probes += 1
    lo, hi = i + 1, min(len(a), i + step + 1)
    j = bisect.bisect_left(a, x, lo, hi)
    probes += max(1, math.ceil(math.log2(max(2, hi - lo))))
    return j, probes


def ternary_max(f, lo, hi, iters=100):
    for _ in range(iters):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    return (lo + hi) / 2


# --------------------------------------------------------------------------------------------------- bits


def popcount(x: int) -> int:
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


def gray(i: int) -> int:
    return i ^ (i >> 1)


def submasks(m: int):
    """Every submask of m, largest first, by s = (s - 1) & m."""
    s = m
    while True:
        yield s
        if s == 0:
            return
        s = (s - 1) & m


def transitive_closure_bits(adj):
    """Warshall's algorithm with each row a Python int used as a bitset: n^3 / w word operations."""
    n = len(adj)
    R = [sum(1 << j for j in range(n) if adj[i][j]) | (1 << i) for i in range(n)]
    for k in range(n):
        bk = 1 << k
        rk = R[k]
        for i in range(n):
            if R[i] & bk:
                R[i] |= rk
    return R


def transitive_closure_plain(adj):
    n = len(adj)
    R = [[bool(adj[i][j]) or i == j for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            if R[i][k]:
                Rk, Ri = R[k], R[i]
                for j in range(n):
                    if Rk[j]:
                        Ri[j] = True
    return R


def lcs_dp(a, b):
    m = len(b)
    prev = [0] * (m + 1)
    for x in a:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            cur[j] = prev[j - 1] + 1 if x == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[m]


def lcs_bitparallel(a, b):
    """Length of the longest common subsequence, a row of the DP per word operation (Allison and Dix, 1986;
    Crochemore et al., 2001): V' = (V + (V & M)) | (V & ~M)."""
    m = len(b)
    full = (1 << m) - 1
    match = {}
    for j, c in enumerate(b):
        match[c] = match.get(c, 0) | (1 << j)
    V = full
    for x in a:
        M = match.get(x, 0)
        U = V & M
        V = ((V + U) | (V & ~M)) & full
    return m - popcount(V)


# --------------------------------------------------------------------------------------------------- meet in the middle, sqrt


def subset_sums(a):
    s = [0]
    for x in a:
        s = s + [v + x for v in s]
    return s


def subset_sum_mitm(a, t):
    """Is some subset of a summing to t? Two halves of 2^(n/2) sums each, one sorted, binary search (Horowitz and
    Sahni, 1974). Returns (found, work) where work counts sums generated plus searches."""
    h = len(a) // 2
    L, R = subset_sums(a[:h]), sorted(subset_sums(a[h:]))
    work = len(L) + len(R)
    for v in L:
        j = bisect.bisect_left(R, t - v)
        work += 1
        if j < len(R) and R[j] == t - v:
            return True, work
    return False, work


def subset_sum_brute(a, t):
    s = subset_sums(a)
    return t in s, len(s)


class SqrtDecomp:
    """Blocks of about sqrt(n): point update O(1), range sum O(sqrt n)."""

    def __init__(self, a):
        self.a = list(a)
        self.B = max(1, int(math.isqrt(len(a))))
        self.blocks = [sum(self.a[i:i + self.B]) for i in range(0, len(a), self.B)]
        self.touched = 0

    def update(self, i, v):
        self.blocks[i // self.B] += v - self.a[i]
        self.a[i] = v

    def query(self, l, r):
        s = 0
        while l <= r and l % self.B:
            s += self.a[l]
            l += 1
            self.touched += 1
        while l + self.B - 1 <= r:
            s += self.blocks[l // self.B]
            l += self.B
            self.touched += 1
        while l <= r:
            s += self.a[l]
            l += 1
            self.touched += 1
        return s


def mo_distinct(a, queries):
    """Number of distinct values in each a[l..r], offline, by Mo's order (blocks of sqrt n, then r).
    Returns (answers, pointer moves)."""
    n = len(a)
    B = max(1, int(math.isqrt(n)))
    order = sorted(range(len(queries)), key=lambda q: (queries[q][0] // B,
                                                       queries[q][1] if (queries[q][0] // B) % 2 == 0 else -queries[q][1]))
    cnt, distinct = {}, 0
    L, R = 0, -1
    moves = 0
    ans = [0] * len(queries)

    def add(i):
        nonlocal distinct
        cnt[a[i]] = cnt.get(a[i], 0) + 1
        if cnt[a[i]] == 1:
            distinct += 1

    def rem(i):
        nonlocal distinct
        cnt[a[i]] -= 1
        if cnt[a[i]] == 0:
            distinct -= 1
    for q in order:
        l, r = queries[q]
        while R < r:
            R += 1
            add(R)
            moves += 1
        while L > l:
            L -= 1
            add(L)
            moves += 1
        while R > r:
            rem(R)
            R -= 1
            moves += 1
        while L < l:
            rem(L)
            L += 1
            moves += 1
        ans[q] = distinct
    return ans, moves
