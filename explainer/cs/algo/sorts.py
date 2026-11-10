"""Sorting and selection, instrumented (Part 16).

Every comparison sort takes a list and returns ``(sorted_list, stats)`` where ``stats["cmp"]`` counts comparisons
between elements; quicksort/selection charge one logical three-way partition comparison per nonpivot key, not individual Python predicates. Other counters use the stated less-than/less-or-equal key tests. Some also count moves, swaps or recursion depth.  Each is
written for clarity first and checked against ``sorted`` in tests/test_cs16_sorts.py.

    out, st = merge_sort(xs)              # st["cmp"], st["levels"]: the work at each level of the recursion tree
    out, st = quicksort(xs, pivot="random", rng=random.Random(1))
    ford_johnson_worst(n)                 # the worst case of merge insertion, by the formula and by exhaustion
"""
from __future__ import annotations

import heapq
import itertools
import math
import random
from functools import cmp_to_key


class Count:
    """A comparison counter: ``c.lt(a, b)``."""
    __slots__ = ("n",)

    def __init__(self):
        self.n = 0

    def lt(self, a, b):
        self.n += 1
        return a < b

    def le(self, a, b):
        self.n += 1
        return a <= b


# -- elementary sorts ---------------------------------------------------------------------------------------------
def inversions(xs) -> int:
    """Pairs i < j with xs[i] > xs[j], by merge sort, O(n log n)."""
    def go(a):
        if len(a) <= 1:
            return a, 0
        m = len(a) // 2
        l, x = go(a[:m])
        r, y = go(a[m:])
        out, i, j, inv = [], 0, 0, x + y
        while i < len(l) and j < len(r):
            if r[j] < l[i]:
                out.append(r[j])
                inv += len(l) - i
                j += 1
            else:
                out.append(l[i])
                i += 1
        out += l[i:] + r[j:]
        return out, inv
    return go(list(xs))[1]


def insertion_sort(xs):
    a = list(xs)
    c = Count()
    moves = 0
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and c.lt(x, a[j]):
            a[j + 1] = a[j]
            moves += 1
            j -= 1
        a[j + 1] = x
    return a, {"cmp": c.n, "moves": moves}


def binary_insertion_sort(xs):
    a = []
    c = Count()
    for x in xs:
        lo, hi = 0, len(a)
        while lo < hi:
            m = (lo + hi) // 2
            if c.lt(x, a[m]):
                hi = m
            else:
                lo = m + 1
        a.insert(lo, x)
    return a, {"cmp": c.n}


def merge_sort(xs):
    """Top-down; ``levels[d]`` is the number of elements merged at depth d (n at every full level)."""
    c = Count()
    levels: dict[int, int] = {}

    def go(a, d):
        if len(a) <= 1:
            return a
        m = len(a) // 2
        l, r = go(a[:m], d + 1), go(a[m:], d + 1)
        out, i, j = [], 0, 0
        while i < len(l) and j < len(r):
            if c.le(l[i], r[j]):
                out.append(l[i])
                i += 1
            else:
                out.append(r[j])
                j += 1
        out += l[i:] + r[j:]
        levels[d] = levels.get(d, 0) + len(a)
        return out
    out = go(list(xs), 0)
    return out, {"cmp": c.n, "levels": [levels[k] for k in sorted(levels)]}


def heapsort(xs):
    """Floyd's bottom-up heapify, then n − 1 extractions; counts the comparisons of each phase."""
    a = list(xs)
    n = len(a)
    c = Count()

    def sift(i, n):
        while True:
            l = 2 * i + 1
            if l >= n:
                return
            m = l
            if l + 1 < n and c.lt(a[l], a[l + 1]):
                m = l + 1
            if c.lt(a[i], a[m]):
                a[i], a[m] = a[m], a[i]
                i = m
            else:
                return
    for i in range(n // 2 - 1, -1, -1):
        sift(i, n)
    build = c.n
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    return a, {"cmp": c.n, "build": build}


def quicksort(xs, pivot="random", rng=None, cutoff=0):
    """Lomuto-free, three-way partition (equal keys grouped).  ``pivot``: "first", "random" or "median3".
    Counts one logical three-way comparison per nonpivot element per partition.
    Median-of-three also counts the actual insertion-sort comparisons on its three sampled keys.
    These are key-comparison model counts, not host Python predicate/instruction counts."""
    import sys
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 4 * len(xs) + 1000))
    rng = rng or random.Random(0)
    c = Count()
    depth = [0]
    pivot_comparisons = [0]

    def choose(a):
        if pivot == "first":
            return a[0]
        if pivot == "random":
            return a[rng.randrange(len(a))]
        x, y, z = a[0], a[len(a) // 2], a[-1]
        ordered, stats = insertion_sort((x, y, z))
        c.n += stats["cmp"]
        pivot_comparisons[0] += stats["cmp"]
        return ordered[1]

    def go(a, d):
        depth[0] = max(depth[0], d)
        if len(a) <= 1:
            return a
        p = choose(a)
        lo, eq, hi = [], [], []
        for x in a:
            c.n += 1
            if x < p:
                lo.append(x)
            elif x > p:
                hi.append(x)
            else:
                eq.append(x)
        c.n -= 1                     # the pivot is not compared with itself
        return go(lo, d + 1) + eq + go(hi, d + 1)
    out = go(list(xs), 0)
    return out, {"cmp": c.n, "depth": depth[0], "pivot_cmp": pivot_comparisons[0],
                 "partition_cmp": c.n - pivot_comparisons[0]}


def quicksort_expected(n: int) -> float:
    """Exact expected comparisons of random-pivot quicksort on distinct keys: 2(n+1)H_n − 4n."""
    H = sum(1 / k for k in range(1, n + 1))
    return 2 * (n + 1) * H - 4 * n


def ford_johnson(xs):
    """Merge insertion (Ford and Johnson 1959): pair up, sort the winners recursively, insert the losers by binary
    search in the order given by the Jacobsthal numbers."""
    c = Count()

    def binsert(chain, x, hi):
        lo = 0
        while lo < hi:
            m = (lo + hi) // 2
            if c.lt(x, chain[m]):
                hi = m
            else:
                lo = m + 1
        chain.insert(lo, x)

    def go(items):
        n = len(items)
        if n <= 1:
            return list(items)
        pairs = []
        for i in range(0, n - 1, 2):
            a, b = items[i], items[i + 1]
            pairs.append((a, b) if c.lt(b, a) else (b, a))      # (larger, smaller)
        straggler = items[-1] if n % 2 else None
        big = go([p[0] for p in pairs])
        # pair each larger element with its smaller partner (identities kept by index)
        partner = {}
        pool = list(pairs)
        order = []
        for x in big:
            k = next(i for i, p in enumerate(pool) if p[0] is x or p[0] == x)
            order.append(pool.pop(k))
        chain = [order[0][1]] + [p[0] for p in order]
        pend = [(p[1], p[0]) for p in order[1:]]                # (to insert, its larger partner)
        if straggler is not None:
            pend.append((straggler, None))
        # insertion order: groups bounded by Jacobsthal numbers t_k = (2^(k+1) + (-1)^k) / 3
        idx = []
        t_prev, k = 1, 2
        while len(idx) < len(pend):
            t = (2 ** (k + 1) + (-1) ** k) // 3
            for j in range(min(t, len(pend) + 1), t_prev, -1):
                idx.append(j - 2)
            t_prev, k = t, k + 1
        for j in idx:
            x, partner_big = pend[j]
            hi = chain.index(partner_big) if partner_big is not None else len(chain)
            binsert(chain, x, hi)
        return chain
    out = go(list(xs))
    return out, {"cmp": c.n}


def ford_johnson_formula(n: int) -> int:
    """Worst-case comparisons of merge insertion: sum over k = 1..n of ceil(log2(3k/4))."""
    return sum(math.ceil(math.log2(3 * k / 4)) for k in range(1, n + 1))


def lower_bound(n: int) -> int:
    return math.ceil(math.log2(math.factorial(n))) if n > 1 else 0


def worst_case(sort, n: int) -> int:
    return max(sort(list(p))[1]["cmp"] for p in itertools.permutations(range(n)))


# -- beating n log n --------------------------------------------------------------------------------------------
def counting_sort(xs, k: int):
    cnt = [0] * k
    for x in xs:
        cnt[x] += 1
    out = []
    for v, m in enumerate(cnt):
        out += [v] * m
    return out, {"passes": 2, "k": k}


def radix_sort(xs, bits=8, width=32):
    """LSD radix sort on non-negative ints, ``bits`` per pass."""
    a = list(xs)
    mask = (1 << bits) - 1
    passes = 0
    for shift in range(0, width, bits):
        buckets = [[] for _ in range(1 << bits)]
        for x in a:
            buckets[(x >> shift) & mask].append(x)
        a = [x for b in buckets for x in b]
        passes += 1
    return a, {"passes": passes}


def timsort_cmp(xs) -> int:
    """Comparisons made by Python's own sort (Timsort; CPython 3.12: powersort's merge policy)."""
    c = Count()
    sorted(xs, key=cmp_to_key(lambda a, b: -1 if c.lt(a, b) else (1 if a != b else 0)))
    return c.n


# -- selection ----------------------------------------------------------------------------------------------------
def quickselect(xs, k, rng=None):
    """Uniform pivots; one logical three-way comparison per nonpivot key.

    Distinct-key expectation formulas refer to this partition model, not Python predicates.
    """
    if not 0 <= k < len(xs):
        raise ValueError("selection rank outside the input")
    rng = rng or random.Random(0)
    c = Count()
    a = list(xs)
    while True:
        if len(a) == 1:
            return a[0], {"cmp": c.n}
        p = a[rng.randrange(len(a))]
        lo = [x for x in a if x < p]
        eq = [x for x in a if x == p]
        hi = [x for x in a if x > p]
        c.n += len(a) - 1
        if k < len(lo):
            a = lo
        elif k < len(lo) + len(eq):
            return p, {"cmp": c.n}
        else:
            k -= len(lo) + len(eq)
            a = hi


def median_of_medians(xs,k):
    """Groups of five with actual small-group insertion-sort comparisons.

    Partition cost is one logical three-way key comparison per nonpivot key.
    Counts deliberately exclude Python predicates, moves and bookkeeping operations.
    """
    if not 0<=k<len(xs):raise ValueError("selection rank outside the input")
    group=Count();partition=[0]
    def small_sort(a):
        a=list(a)
        for i in range(1,len(a)):
            x=a[i];j=i-1
            while j>=0 and group.lt(x,a[j]):a[j+1]=a[j];j-=1
            a[j+1]=x
        return a
    def select(a,k):
        if len(a)<=5:return small_sort(a)[k]
        medians=[]
        for i in range(0,len(a),5):
            g=small_sort(a[i:i+5]);medians.append(g[len(g)//2])
        p=select(medians,len(medians)//2)
        lo=[x for x in a if x<p];eq=[x for x in a if x==p];hi=[x for x in a if x>p]
        partition[0]+=len(a)-1
        if k<len(lo):return select(lo,k)
        if k<len(lo)+len(eq):return p
        return select(hi,k-len(lo)-len(eq))
    value=select(list(xs),k)
    return value,dict(cmp=group.n+partition[0],group_cmp=group.n,partition_cmp=partition[0])


# -- decision trees -------------------------------------------------------------------------------------------------
def decision_tree(sort, n: int):
    """For every permutation of range(n), the sequence of comparisons ``sort`` makes, as (i, j, outcome) on values.
    Returns {permutation: [(a, b, a<b), ...]}."""
    out = {}
    for p in itertools.permutations(range(n)):
        log = []

        class K:
            __slots__ = ("v",)

            def __init__(self, v):
                self.v = v

            def __lt__(self, o):
                r = self.v < o.v
                log.append((self.v, o.v, r))
                return r

            def __le__(self, o):
                r = self.v <= o.v
                log.append((self.v, o.v, r))
                return r

            def __gt__(self, o):
                return o.__lt__(self)
        sort([K(v) for v in p])
        out[p] = log
    return out


# -- amortization ---------------------------------------------------------------------------------------------------
def dynamic_array(n: int, factor: float = 2.0):
    """Appends into an array that grows by ``factor`` when full: total element copies, and whether a new block could
    ever pass the aggregate-size necessary condition for fitting in all previously freed blocks.
    This ignores adjacency, fragmentation and other allocations; it is not a reuse guarantee."""
    cap, size, copies = 1, 0, 0
    freed = 0
    reuse = []
    for _ in range(n):
        if size == cap:
            new = max(cap + 1, int(cap * factor))
            reuse.append(new <= freed)
            freed += cap
            copies += size
            cap = new
        size += 1
    return {"copies": copies, "per_append": copies / n, "final_cap": cap, "could_reuse": sum(reuse),
            "growths": len(reuse)}


# -- external sorting ----------------------------------------------------------------------------------------------
def replacement_selection(xs, m: int):
    """Run lengths produced by replacement selection with a heap of m records (Knuth: 2m on average for random input)."""
    it = iter(xs)
    heap = [(0, x) for x in itertools.islice(it, m)]
    heapq.heapify(heap)
    runs, run, cur, last = [], 0, 0, None
    for x in it:
        r, v = heapq.heappop(heap)
        if r != cur:
            runs.append(run)
            run, cur = 0, r
        run += 1
        heapq.heappush(heap, (r if x >= v else r + 1, x))
    while heap:
        r, v = heapq.heappop(heap)
        if r != cur:
            runs.append(run)
            run, cur = 0, r
        run += 1
    runs.append(run)
    return runs
