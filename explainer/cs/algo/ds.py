"""Data structures for Part 17, each counting the work it does.

Hashing:
    birthday(n, m)                       exact probability of a collision; the 1 - exp(-n^2 / 2m) approximation
    Universal(p, m, rng)                 h(x) = ((a x + b) mod p) mod m, a random member of the Carter-Wegman family
    chain_lengths(keys, m, h)            bucket sizes under chaining
    LinearProbing / DoubleHashing / RobinHood / Uniform
                                         open addressing; .insert(key) and .find(key) return probe counts
    Cuckoo(m, rng)                       two tables, two hash functions; .insert returns kicks, or None on failure
    fks(keys, rng)                       two-level perfect hashing: the space it takes
Trees:
    BST, AVL, LLRB (left-leaning red-black), Treap, SkipList, Splay
                                         every one counts comparisons and rotations; .height(), .depths()
    BTree(t)                             nodes visited per search; height
Heaps:
    BinaryHeap, PairingHeap, FibHeap     link/compare counts for insert, decrease-key and delete-min
Others:
    UnionFind(n, rank, compress)         find path lengths; inverse Ackermann
    Trie                                 nodes, and a radix (compressed) count
    RankSelect                           fixed 512/64-bit rank directory; select is not implemented
    PersistentBST                        path copying: nodes copied per insert
"""

from __future__ import annotations

import bisect
import math
import random


# ---------------------------------------------------------------------------------------------------------- hashing
def birthday(n: int, m: int) -> tuple[float, float]:
    """(exact, approximate) probability that n keys hashed uniformly into m buckets collide somewhere."""
    p = 1.0
    for i in range(n):
        p *= (m - i) / m
    return 1 - p, 1 - math.exp(-n * (n - 1) / (2 * m))


class Universal:
    """h(x) = ((a x + b) mod p) mod m with a in [1, p), b in [0, p): for x != y, Pr[h(x) = h(y)] <= 1/m."""

    def __init__(self, p: int, m: int, rng: random.Random):
        self.p, self.m = p, m
        self.a, self.b = rng.randrange(1, p), rng.randrange(0, p)

    def __call__(self, x: int) -> int:
        return ((self.a * x + self.b) % self.p) % self.m


def chain_lengths(keys, m: int, h) -> list[int]:
    b = [0] * m
    for k in keys:
        b[h(k)] += 1
    return b


class OpenAddressing:
    """A table of m slots.  ``insert`` and ``find`` return the number of slots probed."""

    def __init__(self, m: int, h1, h2=None):
        self.m, self.h1, self.h2 = m, h1, h2
        self.t = [None] * m
        self.n = 0

    def seq(self, k):
        raise NotImplementedError

    def insert(self, k) -> int:
        for i, s in enumerate(self.seq(k), start=1):
            if self.t[s] is None:
                self.t[s] = k
                self.n += 1
                return i
            if self.t[s] == k:
                return i
        raise RuntimeError("table full")

    def find(self, k) -> int:
        for i, s in enumerate(self.seq(k), start=1):
            if self.t[s] is None or self.t[s] == k:
                return i
        return self.m

    def clusters(self) -> list[int]:
        """Lengths of the runs of occupied slots (cyclically)."""
        occ = [x is not None for x in self.t]
        if all(occ):
            return [self.m]
        start = occ.index(False)
        runs, run = [], 0
        for i in range(1, self.m + 1):
            if occ[(start + i) % self.m]:
                run += 1
            elif run:
                runs.append(run)
                run = 0
        return runs


class LinearProbing(OpenAddressing):
    def seq(self, k):
        s = self.h1(k)
        for i in range(self.m):
            yield (s + i) % self.m


class DoubleHashing(OpenAddressing):
    def seq(self, k):
        s, d = self.h1(k), 1 + 2 * (self.h2(k) % (self.m // 2))  # odd: coprime with a power of two
        for i in range(self.m):
            yield (s + i * d) % self.m


class Uniform(OpenAddressing):
    """Uniform probing: every key probes its own random permutation of the slots (the model of Yao's conjecture)."""

    def seq(self, k):
        r = random.Random(hash((k, 0x5bd1e995)))
        perm = list(range(self.m))
        r.shuffle(perm)
        yield from perm


class RobinHood:
    """Linear probing that, on a collision, lets the key farther from home take the slot (Celis 1986).  Same
    average probes as linear probing; far smaller variance."""

    def __init__(self, m: int, h):
        self.m, self.h = m, h
        self.t = [None] * m
        self.n = 0

    def insert(self, k) -> int:
        i, d, probes = self.h(k), 0, 0
        while True:
            probes += 1
            if self.t[i] is None:
                self.t[i] = (k, d)
                self.n += 1
                return probes
            kk, dd = self.t[i]
            if kk == k:
                return probes
            if dd < d:
                self.t[i] = (k, d)
                k, d = kk, dd
            i, d = (i + 1) % self.m, d + 1

    def displacements(self) -> list[int]:
        return [x[1] for x in self.t if x is not None]


class Cuckoo:
    """Cuckoo hashing (Pagh & Rodler 2001): every key lives in T1[h1] or T2[h2]; lookups probe two slots."""

    def __init__(self, m: int, rng: random.Random, p: int = (1 << 61) - 1, max_kicks: int = 500):
        self.m, self.max_kicks = m, max_kicks
        self.h = [Universal(p, m, rng), Universal(p, m, rng)]
        self.t = [[None] * m, [None] * m]

    def find(self, k) -> bool:
        return self.t[0][self.h[0](k)] == k or self.t[1][self.h[1](k)] == k

    def insert(self, k):
        if self.find(k):
            return 0
        side = 0
        for kicks in range(self.max_kicks):
            s = self.h[side](k)
            k, self.t[side][s] = self.t[side][s], k
            if k is None:
                return kicks
            side ^= 1
        return None


def fks(keys, rng: random.Random, p: int = (1 << 61) - 1) -> dict:
    """Fredman-Komlos-Szemeredi (1984): n buckets, then bucket i of size b gets a collision-free table of b^2 slots,
    retrying its hash until it is collision-free.  Returns the total space and the retries."""
    n = len(keys)
    while True:
        h = Universal(p, n, rng)
        buckets = [[] for _ in range(n)]
        for k in keys:
            buckets[h(k)].append(k)
        space = sum(len(b) ** 2 for b in buckets)
        if space <= 4 * n:
            break
    retries = 0
    for b in buckets:
        if len(b) <= 1:
            continue
        while True:
            g = Universal(p, len(b) ** 2, rng)
            if len({g(k) for k in b}) == len(b):
                break
            retries += 1
    return {"n": n, "space": n + space, "retries": retries, "max_bucket": max(len(b) for b in buckets)}


# ------------------------------------------------------------------------------------------------------------ trees
class Node:
    __slots__ = ("key", "left", "right", "h", "red", "pri", "size")

    def __init__(self, key, pri=0.0):
        self.key, self.left, self.right = key, None, None
        self.h, self.red, self.pri, self.size = 1, True, pri, 1


def _height(t) -> int:
    if t is None:
        return 0
    stack, best = [(t, 1)], 0
    while stack:
        n, d = stack.pop()
        best = max(best, d)
        for c in (n.left, n.right):
            if c is not None:
                stack.append((c, d + 1))
    return best


def _depths(t) -> list[int]:
    out, stack = [], ([(t, 0)] if t is not None else [])
    while stack:
        n, d = stack.pop()
        out.append(d)
        for c in (n.left, n.right):
            if c is not None:
                stack.append((c, d + 1))
    return out


class Counted:
    """Shared counters: comparisons and rotations."""

    def __init__(self):
        self.cmp = 0
        self.rot = 0
        self.root = None

    def height(self) -> int:
        return _height(self.root)

    def depths(self) -> list[int]:
        return _depths(self.root)

    def search(self, k) -> int:
        """Nodes visited (comparisons) to find k."""
        n, c = self.root, 0
        while n is not None:
            c += 1
            if k == n.key:
                return c
            n = n.left if k < n.key else n.right
        return c

    def rot_left(self, h):
        self.rot += 1
        x = h.right
        h.right, x.left = x.left, h
        return x

    def rot_right(self, h):
        self.rot += 1
        x = h.left
        h.left, x.right = x.right, h
        return x


class BST(Counted):
    def insert(self, k):
        if self.root is None:
            self.root = Node(k)
            return
        n = self.root
        while True:
            self.cmp += 1
            if k == n.key:
                return
            nxt = n.left if k < n.key else n.right
            if nxt is None:
                if k < n.key:
                    n.left = Node(k)
                else:
                    n.right = Node(k)
                return
            n = nxt


class AVL(Counted):
    """Adelson-Velsky & Landis (1962): the heights of siblings differ by at most one."""

    @staticmethod
    def _h(n):
        return n.h if n is not None else 0

    def _fix(self, n):
        n.h = 1 + max(self._h(n.left), self._h(n.right))

    def _rr(self, n):
        x = self.rot_right(n)
        self._fix(n)
        self._fix(x)
        return x

    def _rl(self, n):
        x = self.rot_left(n)
        self._fix(n)
        self._fix(x)
        return x

    def _ins(self, n, k):
        if n is None:
            return Node(k)
        self.cmp += 1
        if k == n.key:
            return n
        if k < n.key:
            n.left = self._ins(n.left, k)
        else:
            n.right = self._ins(n.right, k)
        self._fix(n)
        b = self._h(n.left) - self._h(n.right)
        if b > 1:
            if self._h(n.left.left) < self._h(n.left.right):
                n.left = self._rl(n.left)
            return self._rr(n)
        if b < -1:
            if self._h(n.right.right) < self._h(n.right.left):
                n.right = self._rr(n.right)
            return self._rl(n)
        return n

    def insert(self, k):
        self.root = self._ins(self.root, k)


class LLRB(Counted):
    """Sedgewick's left-leaning red-black tree (2008): a 2-3 tree, each 3-node drawn as a red left link."""

    @staticmethod
    def _red(n):
        return n is not None and n.red

    def _ins(self, h, k):
        if h is None:
            return Node(k)
        self.cmp += 1
        if k < h.key:
            h.left = self._ins(h.left, k)
        elif k > h.key:
            h.right = self._ins(h.right, k)
        else:
            return h
        if self._red(h.right) and not self._red(h.left):
            x = self.rot_left(h)
            x.red, h.red = h.red, True
            h = x
        if self._red(h.left) and self._red(h.left.left):
            x = self.rot_right(h)
            x.red, h.red = h.red, True
            h = x
        if self._red(h.left) and self._red(h.right):
            h.red, h.left.red, h.right.red = True, False, False
        return h

    def insert(self, k):
        self.root = self._ins(self.root, k)
        self.root.red = False

    def black_height(self) -> int:
        n, b = self.root, 0
        while n is not None:
            b += 0 if n.red else 1
            n = n.left
        return b


class Treap(Counted):
    """Seidel & Aragon (1989): a BST on keys, a heap on random priorities: the shape of a random BST, always."""

    def __init__(self, rng: random.Random):
        super().__init__()
        self.rng = rng

    def _ins(self, n, k):
        if n is None:
            return Node(k, self.rng.random())
        self.cmp += 1
        if k == n.key:
            return n
        if k < n.key:
            n.left = self._ins(n.left, k)
            if n.left.pri > n.pri:
                n = self.rot_right(n)
        else:
            n.right = self._ins(n.right, k)
            if n.right.pri > n.pri:
                n = self.rot_left(n)
        return n

    def insert(self, k):
        self.root = self._ins(self.root, k)


class Splay(Counted):
    """Sleator & Tarjan (1985): after every access, rotate the node to the root (zig, zig-zig, zig-zag).
    ``access`` returns the cost: one plus the number of rotations."""

    def _splay(self, root, k):
        if root is None:
            return None
        header = Node(None)
        lt = rt = header
        t = root
        while True:
            self.cmp += 1
            if k < t.key:
                if t.left is None:
                    break
                if k < t.left.key:
                    t = self.rot_right(t)
                    if t.left is None:
                        break
                rt.left = t
                rt = t
                t = t.left
                self.rot += 1
            elif k > t.key:
                if t.right is None:
                    break
                if k > t.right.key:
                    t = self.rot_left(t)
                    if t.right is None:
                        break
                lt.right = t
                lt = t
                t = t.right
                self.rot += 1
            else:
                break
        lt.right, rt.left = t.left, t.right
        t.left, t.right = header.right, header.left
        return t

    def access(self, k) -> int:
        before = self.rot
        self.root = self._splay(self.root, k)
        return 1 + self.rot - before

    def insert(self, k):
        if self.root is None:
            self.root = Node(k)
            return
        self.root = self._splay(self.root, k)
        if self.root.key == k:
            return
        n = Node(k)
        if k < self.root.key:
            n.left, n.right, self.root.left = self.root.left, self.root, None
        else:
            n.right, n.left, self.root.right = self.root.right, self.root, None
        self.root = n


class SkipList:
    """Pugh (1990): each element is promoted to the next level with probability 1/2."""

    def __init__(self, rng: random.Random, p: float = 0.5, max_level: int = 32):
        self.rng, self.p, self.max = rng, p, max_level
        self.head = [None] * max_level
        self.level = 1
        self.nodes = {}

    def _lvl(self) -> int:
        l = 1
        while self.rng.random() < self.p and l < self.max:
            l += 1
        return l

    def insert(self, k):
        upd = [None] * self.max
        x = None
        for i in range(self.level - 1, -1, -1):
            nxt = self.head[i] if x is None else self.nodes[x][i]
            while nxt is not None and nxt < k:
                x = nxt
                nxt = self.nodes[x][i]
            upd[i] = x
        lvl = self._lvl()
        self.level = max(self.level, lvl)
        self.nodes[k] = [None] * lvl
        for i in range(lvl):
            if upd[i] is None:
                self.nodes[k][i], self.head[i] = self.head[i], k
            else:
                self.nodes[k][i], self.nodes[upd[i]][i] = self.nodes[upd[i]][i], k

    def search(self, k) -> int:
        """Links followed to find k."""
        steps, x = 0, None
        for i in range(self.level - 1, -1, -1):
            nxt = self.head[i] if x is None else self.nodes[x][i]
            while nxt is not None and nxt < k:
                steps += 1
                x = nxt
                nxt = self.nodes[x][i]
            steps += 1
            if nxt == k:
                return steps
        return steps

    def levels(self) -> list[int]:
        return [len(v) for v in self.nodes.values()]


class BTree:
    """A B-tree of minimum degree t (Bayer & McCreight 1970): every node but the root holds t-1 .. 2t-1 keys."""

    class _N:
        __slots__ = ("keys", "kids")

        def __init__(self):
            self.keys, self.kids = [], []

    def __init__(self, t: int):
        self.t = t
        self.root = self._N()

    def _split(self, x, i):
        t = self.t
        y = x.kids[i]
        z = self._N()
        mid = y.keys[t - 1]
        z.keys, y.keys = y.keys[t:], y.keys[:t - 1]
        if y.kids:
            z.kids, y.kids = y.kids[t:], y.kids[:t]
        x.keys.insert(i, mid)
        x.kids.insert(i + 1, z)

    def insert(self, k):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = self._N()
            s.kids = [r]
            self.root = s
            self._split(s, 0)
        x = self.root
        while True:
            i = bisect.bisect_left(x.keys, k)
            if i < len(x.keys) and x.keys[i] == k:
                return
            if not x.kids:
                x.keys.insert(i, k)
                return
            if len(x.kids[i].keys) == 2 * self.t - 1:
                self._split(x, i)
                if k > x.keys[i]:
                    i += 1
                elif k == x.keys[i]:
                    return
            x = x.kids[i]

    def height(self) -> int:
        h, x = 1, self.root
        while x.kids:
            h, x = h + 1, x.kids[0]
        return h

    def nodes(self) -> int:
        c, st = 0, [self.root]
        while st:
            x = st.pop()
            c += 1
            st.extend(x.kids)
        return c


# ------------------------------------------------------------------------------------------------------------ heaps
class BinaryHeap:
    """A min-heap with decrease-key through a position map; counts comparisons."""

    def __init__(self):
        self.a, self.pos, self.cmp = [], {}, 0

    def _sw(self, i, j):
        a = self.a
        a[i], a[j] = a[j], a[i]
        self.pos[a[i][1]], self.pos[a[j][1]] = i, j

    def _up(self, i):
        while i > 0:
            p = (i - 1) // 2
            self.cmp += 1
            if self.a[p][0] <= self.a[i][0]:
                break
            self._sw(i, p)
            i = p

    def _down(self, i):
        n = len(self.a)
        while True:
            l, r, s = 2 * i + 1, 2 * i + 2, i
            if l < n:
                self.cmp += 1
                if self.a[l][0] < self.a[s][0]:
                    s = l
            if r < n:
                self.cmp += 1
                if self.a[r][0] < self.a[s][0]:
                    s = r
            if s == i:
                return
            self._sw(i, s)
            i = s

    def insert(self, item, key):
        self.a.append((key, item))
        self.pos[item] = len(self.a) - 1
        self._up(len(self.a) - 1)

    def decrease(self, item, key):
        i = self.pos[item]
        self.a[i] = (key, item)
        self._up(i)

    def pop(self):
        top = self.a[0]
        last = self.a.pop()
        del self.pos[top[1]]
        if self.a:
            self.a[0] = last
            self.pos[last[1]] = 0
            self._down(0)
        return top[1], top[0]

    def __len__(self):
        return len(self.a)


class PairingHeap:
    """Fredman, Sedgewick, Sleator & Tarjan (1986): a heap-ordered multiway tree; delete-min pairs the children."""

    class _N:
        __slots__ = ("key", "item", "kids", "parent")

        def __init__(self, key, item):
            self.key, self.item, self.kids, self.parent = key, item, [], None

    def __init__(self):
        self.root, self.nodes, self.cmp, self.n = None, {}, 0, 0

    def _link(self, a, b):
        if a is None:
            return b
        if b is None:
            return a
        self.cmp += 1
        if b.key < a.key:
            a, b = b, a
        b.parent = a
        a.kids.append(b)
        return a

    def insert(self, item, key):
        x = self._N(key, item)
        self.nodes[item] = x
        self.root = self._link(self.root, x)
        self.n += 1

    def decrease(self, item, key):
        x = self.nodes[item]
        x.key = key
        if x is self.root:
            return
        x.parent.kids.remove(x)
        x.parent = None
        self.root = self._link(self.root, x)

    def pop(self):
        r = self.root
        kids = r.kids
        for c in kids:
            c.parent = None
        pairs = [self._link(kids[i], kids[i + 1] if i + 1 < len(kids) else None) for i in range(0, len(kids), 2)]
        root = None
        for p in reversed(pairs):
            root = self._link(p, root)
        self.root = root
        del self.nodes[r.item]
        self.n -= 1
        return r.item, r.key

    def __len__(self):
        return self.n


class FibHeap:
    """Educational lazy melding and cascading cuts; counts actual key comparisons.

    Python lists and list.remove do not implement the constant-time pointer
    operations needed for theoretical Fibonacci-heap time bounds.
    """

    class _N:
        __slots__ = ("key", "item", "parent", "kids", "mark")

        def __init__(self, key, item):
            self.key, self.item, self.parent, self.kids, self.mark = key, item, None, [], False

    def __init__(self):
        self.roots, self.min, self.nodes = [], None, {}
        self.cmp = self.links = self.cuts = 0

    def insert(self, item, key):
        x = self._N(key, item)
        self.nodes[item] = x
        self.roots.append(x)
        if self.min is None:
            self.min = x
        else:
            self.cmp += 1
            if key < self.min.key:
                self.min = x

    def _cut(self, x):
        p = x.parent
        p.kids.remove(x)
        x.parent, x.mark = None, False
        self.roots.append(x)
        self.cuts += 1
        return p

    def decrease(self, item, key):
        x = self.nodes[item]
        x.key = key
        p = x.parent
        if p is not None:
            self.cmp += 1
        if p is not None and key < p.key:
            p = self._cut(x)
            while p.parent is not None:
                if not p.mark:
                    p.mark = True
                    break
                p = self._cut(p)
        self.cmp += 1
        if key < self.min.key:
            self.min = x

    def pop(self):
        z = self.min
        self.roots.remove(z)
        for c in z.kids:
            c.parent = None
            self.roots.append(c)
        del self.nodes[z.item]
        if not self.roots:
            self.min = None
            return z.item, z.key
        by_rank = {}
        for x in self.roots:
            d = len(x.kids)
            while d in by_rank:
                y = by_rank.pop(d)
                self.cmp += 1
                if y.key < x.key:
                    x, y = y, x
                y.parent = x
                y.mark = False
                x.kids.append(y)
                self.links += 1
                d += 1
            by_rank[d] = x
        self.roots = list(by_rank.values())
        self.min = None
        for x in self.roots:
            if self.min is None:
                self.min = x
            else:
                self.cmp += 1
                if x.key < self.min.key:
                    self.min = x
        return z.item, z.key

    def __len__(self):
        return len(self.nodes)


def dijkstra(adj, src, heap_cls):
    """Dijkstra's algorithm with the given heap; returns distances and the heap (for its counters)."""
    h = heap_cls()
    dist = {src: 0}
    h.insert(src, 0)
    done = set()
    while len(h):
        u, d = h.pop()
        done.add(u)
        for v, w in adj[u]:
            nd = d + w
            if v in done:
                continue
            if v not in dist:
                dist[v] = nd
                h.insert(v, nd)
            elif nd < dist[v]:
                dist[v] = nd
                h.decrease(v, nd)
    return dist, h


# ----------------------------------------------------------------------------------------------------- union-find
class UnionFind:
    def __init__(self, n: int, rank: bool = True, compress: bool = True):
        self.p = list(range(n))
        self.r = [0] * n
        self.rank, self.compress = rank, compress
        self.steps = 0

    def find(self, x: int) -> int:
        root = x
        while self.p[root] != root:
            self.steps += 1
            root = self.p[root]
        if self.compress:
            while self.p[x] != root:
                self.p[x], x = root, self.p[x]
        return root

    def union(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.rank:
            if self.r[a] < self.r[b]:
                a, b = b, a
            self.p[b] = a
            if self.r[a] == self.r[b]:
                self.r[a] += 1
        else:
            self.p[b] = a
        return True

    def max_depth(self) -> int:
        best = 0
        for x in range(len(self.p)):
            d = 0
            while self.p[x] != x:
                x = self.p[x]
                d += 1
            best = max(best, d)
        return best


def ackermann(m: int, n: int) -> int:
    """A(m, n) for small arguments (the two-argument Ackermann-Peter function)."""
    if m == 0:
        return n + 1
    if m == 1:
        return n + 2
    if m == 2:
        return 2 * n + 3
    if m == 3:
        return 2 ** (n + 3) - 3
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))


def log_star(n: float) -> int:
    k = 0
    while n > 1:
        n = math.log2(n)
        k += 1
    return k


# ------------------------------------------------------------------------------------------------------ strings etc
class Trie:
    def __init__(self):
        self.root = {}
        self.nodes = 1

    def insert(self, w: str):
        n = self.root
        for c in w:
            if c not in n:
                n[c] = {}
                self.nodes += 1
            n = n[c]
        n["$"] = n.get("$", 0) + 1

    def radix_nodes(self) -> int:
        """Nodes after compressing every chain of single-child, non-terminal nodes (a radix tree)."""
        def walk(n, top):
            kids = [k for k in n if k != "$"]
            keep = top or len(kids) != 1 or "$" in n
            return (1 if keep else 0) + sum(walk(n[k], False) for k in kids)
        return walk(self.root, True)


class RankSelect:
    """Educational fixed 512/64-bit rank directory; select is not implemented.

    Directory entries and a bounded 64-bit population count illustrate rank.
    This fixed layout is not an asymptotic o(n)-bit construction, and Python
    container memory is not the packed-bit estimate returned below.
    """

    def __init__(self, bits: list[int]):
        if any(b not in (0, 1) for b in bits):
            raise ValueError("rank bit vector must contain only zeroes and ones")
        self.bits = list(bits)
        self.n = len(bits)
        self.words = [sum(b << i for i, b in enumerate(bits[j:j + 64])) for j in range(0, self.n, 64)]
        self.super, self.block = [], []
        c = 0
        for w, word in enumerate(self.words):
            if w % 8 == 0:
                self.super.append(c)
            self.block.append(c - self.super[-1])
            c += word.bit_count()
        self.total = c

    def rank(self, i: int) -> int:
        """Ones in bits[0:i], including both valid boundary positions 0 and n."""
        if not isinstance(i, int) or not 0 <= i <= self.n:
            raise ValueError("rank position must be an integer in [0, n]")
        if i == self.n:
            return self.total
        w, r = divmod(i, 64)
        return self.super[w // 8] + self.block[w] + (self.words[w] & ((1 << r) - 1)).bit_count()

    def overhead_bits(self) -> int:
        """Logical packed directory estimate, excluding Python object overhead."""
        return len(self.super) * max(32, self.n.bit_length()) + len(self.block) * 9


class PersistentBST:
    """Path copying (Driscoll, Sarnak, Sleator & Tarjan 1989): every insert copies the path to the new leaf; every
    old version stays searchable."""

    def __init__(self):
        self.versions = [None]
        self.copied = 0

    def insert(self, k):
        def ins(n):
            self.copied += 1
            if n is None:
                return (k, None, None)
            key, l, r = n
            if k < key:
                return (key, ins(l), r)
            if k > key:
                return (key, l, ins(r))
            return n
        self.versions.append(ins(self.versions[-1]))

    @staticmethod
    def contains(v, k) -> bool:
        while v is not None:
            if k == v[0]:
                return True
            v = v[1] if k < v[0] else v[2]
        return False
