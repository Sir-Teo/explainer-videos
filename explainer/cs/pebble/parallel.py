"""Parallel algorithms and their models for Part 10: work and span, schedules, scans, sorting networks, networks.

    d = Dag.random(200, seed=1)            # a computation: unit-time nodes, edges from inputs to uses
    d.work(), d.span(), d.critical_path()
    greedy(d, p)                           # a greedy (list) schedule on p processors: makespan, and who ran what
    steal(fork_join_tree(depth), p)        # randomized work stealing (Blumofe and Leiserson): makespan and steals

    hillis_steele(xs), blelloch(xs)        # parallel prefix sums, step by step, with operation counts
    bitonic(n), odd_even_merge(n), transposition(n)    # sorting networks as lists of comparators (i, j), i < j
    layers(net), sorts_all_01(net, n), sorts_all_perms(net, n)

    TOPOLOGIES: ring, mesh, torus, hypercube, tree, fat tree, complete;  diameter(g), bisection(g) (exact, by search)

Brent's theorem: any greedy schedule on p processors finishes by T1/p + T_inf.  The proof the scenes give: a step is
*complete* if all p processors are busy, else *incomplete*.  There are at most T1/p complete steps (each does p units
of work), and every incomplete step runs every ready node, so it shortens the longest remaining path by one: at most
T_inf incomplete steps.  ``greedy`` is checked against the bound in tests/test_cs10_parallel.py.
"""

from __future__ import annotations

import itertools
import random
from collections import deque
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# work and span
# ---------------------------------------------------------------------------
@dataclass
class Dag:
    n: int
    preds: list[list[int]]
    cost: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.cost:
            self.cost = [1] * self.n
        self.succs = [[] for _ in range(self.n)]
        for v, ps in enumerate(self.preds):
            for u in ps:
                self.succs[u].append(v)

    @classmethod
    def random(cls, n: int, width: int = 8, fan: int = 2, seed: int = 1) -> "Dag":
        """A layered random computation: nodes in order, each using up to ``fan`` of the ``width`` nodes before it."""
        rng = random.Random(seed)
        preds = []
        for v in range(n):
            lo = max(0, v - width)
            k = min(fan, v - lo)
            preds.append(sorted(rng.sample(range(lo, v), rng.randint(0, k))) if k else [])
        return cls(n, preds)

    @classmethod
    def reduction(cls, n: int) -> "Dag":
        """Summing n numbers as a balanced tree: n leaves, n - 1 additions."""
        preds = [[] for _ in range(n)]
        level = list(range(n))
        while len(level) > 1:
            nxt = []
            for a, b in zip(level[::2], level[1::2]):
                preds.append([a, b])
                nxt.append(len(preds) - 1)
            if len(level) % 2:
                nxt.append(level[-1])
            level = nxt
        return cls(len(preds), preds)

    def work(self) -> int:
        return sum(self.cost)

    def depths(self) -> list[int]:
        """Finish time of each node with unlimited processors (nodes are numbered in a topological order)."""
        fin = [0] * self.n
        for v in range(self.n):
            fin[v] = self.cost[v] + max((fin[u] for u in self.preds[v]), default=0)
        return fin

    def span(self) -> int:
        return max(self.depths(), default=0)

    def critical_path(self) -> list[int]:
        fin = self.depths()
        v = max(range(self.n), key=lambda k: fin[k])
        path = [v]
        while self.preds[v]:
            v = max(self.preds[v], key=lambda u: fin[u])
            path.append(v)
        return path[::-1]


def greedy(d: Dag, p: int, priority=None) -> dict:
    """A greedy schedule of unit-cost nodes: at every step run up to ``p`` ready nodes (lowest priority value first;
    by default node order).  Returns the makespan, the steps (lists of nodes), and the complete/incomplete counts."""
    assert all(c == 1 for c in d.cost), "unit-cost nodes"
    key = priority or (lambda v: v)
    left = [len(ps) for ps in d.preds]
    ready = sorted((v for v in range(d.n) if left[v] == 0), key=key)
    steps = []
    done = 0
    while done < d.n:
        run, ready = ready[:p], ready[p:]
        steps.append(run)
        done += len(run)
        new = []
        for v in run:
            for s in d.succs[v]:
                left[s] -= 1
                if left[s] == 0:
                    new.append(s)
        ready = sorted(ready + new, key=key)
    complete = sum(len(s) == p for s in steps)
    return {"makespan": len(steps), "steps": steps, "complete": complete, "incomplete": len(steps) - complete}


# ---------------------------------------------------------------------------
# work stealing
# ---------------------------------------------------------------------------
def fork_join_tree(depth: int) -> Dag:
    """A fork-join computation: each internal task spawns two halves and then joins them (like a parallel recursive
    sum).  Node order is topological: forks, then leaves, then joins."""
    preds: list[list[int]] = []

    def build(k, parent):
        me = len(preds)
        preds.append([parent] if parent is not None else [])
        if k == 0:
            return me, me
        _, l_end = build(k - 1, me)
        _, r_end = build(k - 1, me)
        preds.append([l_end, r_end])
        return me, len(preds) - 1

    build(depth, None)
    # renumber in a topological order (the construction appends a join after both its subtrees: already fine)
    return Dag(len(preds), preds)


def steal(d: Dag, p: int, seed: int = 1) -> dict:
    """Randomized work stealing on unit-cost nodes.  Each processor keeps a deque; it works at the bottom (newest
    first); a node that becomes ready is pushed on the bottom of the deque of the processor that enabled it.  An idle
    processor spends the step trying to steal the top (oldest) node of a random victim, which it runs the step
    after.  Returns the makespan and the
    number of steal attempts and successes."""
    rng = random.Random(seed)
    left = [len(ps) for ps in d.preds]
    dq = [deque() for _ in range(p)]
    for v in range(d.n):
        if left[v] == 0:
            dq[0].append(v)
    done = steps = attempts = steals = 0
    while done < d.n:
        steps += 1
        took = []
        busy = [bool(dq[q]) for q in range(p)]
        for q in range(p):
            if busy[q]:
                took.append((q, dq[q].pop()))
        got = []
        for q in range(p):
            if not busy[q]:
                attempts += 1
                if p > 1:
                    victim = rng.randrange(p - 1)
                    victim += victim >= q
                    if dq[victim]:
                        got.append((q, dq[victim].popleft()))
                        steals += 1
        for q, v in got:  # a stolen node runs from the thief's deque next step
            dq[q].append(v)
        for q, v in took:
            done += 1
            for s in d.succs[v]:
                left[s] -= 1
                if left[s] == 0:
                    dq[q].append(s)
    return {"makespan": steps, "attempts": attempts, "steals": steals}


# ---------------------------------------------------------------------------
# parallel prefix
# ---------------------------------------------------------------------------
def hillis_steele(xs: list, op=lambda a, b: a + b) -> dict:
    """Inclusive scan in log2 n steps: at step k every element adds the one 2^k to its left.  n log n operations."""
    cur = list(xs)
    levels = [cur]
    ops = 0
    d = 1
    while d < len(xs):
        cur = [cur[i] if i < d else op(cur[i - d], cur[i]) for i in range(len(cur))]
        ops += len(cur) - d
        levels.append(cur)
        d *= 2
    return {"levels": levels, "ops": ops, "result": cur}


def blelloch(xs: list, op=lambda a, b: a + b, identity=0) -> dict:
    """Blelloch's work-efficient exclusive scan (1990), for n a power of two: an up-sweep builds partial sums in a
    tree, a down-sweep pushes prefixes back down.  2(n - 1) operations, 2 log2 n steps."""
    n = len(xs)
    if n < 1 or n & (n - 1):
        raise ValueError("Blelloch scan needs a nonempty power-of-two input")
    a = list(xs)
    up = [list(a)]
    ops = 0
    d = 1
    while d < n:
        for i in range(2 * d - 1, n, 2 * d):
            a[i] = op(a[i - d], a[i])
            ops += 1
        up.append(list(a))
        d *= 2
    a[n - 1] = identity
    down = [list(a)]
    d = n // 2
    while d >= 1:
        for i in range(2 * d - 1, n, 2 * d):
            t = a[i - d]
            a[i - d] = a[i]
            # The parent prefix precedes this left-subtree total. Associativity
            # permits regrouping, not swapping operands (e.g. concatenation).
            a[i] = op(a[i], t)
            ops += 1
        down.append(list(a))
        d //= 2
    return {"up": up, "down": down, "ops": ops, "result": a}


# ---------------------------------------------------------------------------
# sorting networks
# ---------------------------------------------------------------------------
def bitonic(n: int) -> list[tuple[int, int]]:
    """Batcher's bitonic sorter (1968) for n a power of two, every comparator putting the smaller value on the lower
    wire (the standard form that avoids reversed comparators: the first stage of each merge compares mirror images)."""
    assert n & (n - 1) == 0
    net = []
    k = 2
    while k <= n:
        for base in range(0, n, k):  # merge two sorted halves of size k/2: first compare mirror positions
            for i in range(k // 2):
                net.append((base + i, base + k - 1 - i))
        j = k // 4
        while j >= 1:
            for base in range(0, n, 2 * j):
                for i in range(j):
                    net.append((base + i, base + i + j))
            j //= 2
        k *= 2
    return net


def odd_even_merge(n: int) -> list[tuple[int, int]]:
    """Batcher's odd-even merge sort (1968) for n a power of two (Knuth 5.3.4, Algorithm M's comparators)."""
    assert n & (n - 1) == 0
    net = []
    p = 1
    while p < n:
        k = p
        while k >= 1:
            for j in range(k % p, n - k, 2 * k):
                for i in range(min(k, n - j - k)):
                    if (i + j) // (2 * p) == (i + j + k) // (2 * p):
                        net.append((i + j, i + j + k))
            k //= 2
        p *= 2
    return net


def transposition(n: int) -> list[tuple[int, int]]:
    """Odd-even transposition sort: n rounds of neighbour comparators, alternately on even and odd pairs."""
    return [(i, i + 1) for r in range(n) for i in range(r % 2, n - 1, 2)]


def insertion(n: int) -> list[tuple[int, int]]:
    """The insertion-sort network: for each new wire, bubble it down past every earlier one."""
    return [(j - 1, j) for i in range(1, n) for j in range(i, 0, -1)]


def apply(net, xs) -> list:
    a = list(xs)
    for i, j in net:
        if a[i] > a[j]:
            a[i], a[j] = a[j], a[i]
    return a


def layers(net) -> list[list[tuple[int, int]]]:
    """Group comparators into parallel layers (each as early as its wires allow): the depth is the layer count."""
    at: dict[int, int] = {}
    out: list[list] = []
    for i, j in net:
        k = max(at.get(i, 0), at.get(j, 0))
        if k == len(out):
            out.append([])
        out[k].append((i, j))
        at[i] = at[j] = k + 1
    return out


def sorts_all_01(net, n: int) -> tuple[bool, list | None]:
    """The 0-1 principle's test: does the network sort all 2^n inputs of zeros and ones?  Returns (ok, a failing
    input).  Vectorised as bitmasks: wire w's value across all inputs is one big integer."""
    N = 1 << n
    wires = []
    for w in range(n):
        m = 0
        for x in range(N):
            if (x >> w) & 1:
                m |= 1 << x
        wires.append(m)
    for i, j in net:
        a, b = wires[i], wires[j]
        wires[i], wires[j] = a & b, a | b  # min, max on 0-1 values
    # sorted: wire w holds 1 exactly when at least n - w of the inputs' bits are 1
    bad = 0
    for w in range(n - 1):
        bad |= wires[w] & ~wires[w + 1]
    if not bad:
        return True, None
    x = (bad & -bad).bit_length() - 1
    return False, [(x >> w) & 1 for w in range(n)]


def sorts_all_perms(net, n: int) -> bool:
    want = list(range(n))
    return all(apply(net, p) == want for p in itertools.permutations(range(n)))


# best known sizes and depths of sorting networks, n = 1 .. 12 (Knuth 5.3.4; optimal sizes for n <= 10 proved by
# Codish, Cruz-Filipe, Frank and Schneider-Kamp 2014; depths for n <= 16 by Bundala and Zavodny 2014)
BEST_SIZE = {1: 0, 2: 1, 3: 3, 4: 5, 5: 9, 6: 12, 7: 16, 8: 19, 9: 25, 10: 29, 11: 35, 12: 39}
BEST_DEPTH = {1: 0, 2: 1, 3: 3, 4: 3, 5: 5, 6: 5, 7: 6, 8: 6, 9: 7, 10: 7, 11: 8, 12: 8}


# ---------------------------------------------------------------------------
# interconnection networks
# ---------------------------------------------------------------------------
def ring(n):
    return {v: {(v - 1) % n, (v + 1) % n} for v in range(n)}


def mesh(k, wrap=False):
    g = {}
    for r in range(k):
        for c in range(k):
            nb = set()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr, cc = r + dr, c + dc
                if wrap:
                    rr, cc = rr % k, cc % k
                if 0 <= rr < k and 0 <= cc < k and (rr, cc) != (r, c):
                    nb.add(rr * k + cc)
            g[r * k + c] = nb
    return g


def hypercube(d):
    return {v: {v ^ (1 << b) for b in range(d)} for v in range(1 << d)}


def complete(n):
    return {v: set(range(n)) - {v} for v in range(n)}


def tree(n):
    """A binary tree with the n processors at the leaves and n - 1 switches above them (switches numbered from n)."""
    g = {v: set() for v in range(2 * n - 1)}
    level = list(range(n))
    nxt_id = n
    while len(level) > 1:
        nxt = []
        for a, b in zip(level[::2], level[1::2]):
            s = nxt_id
            nxt_id += 1
            g[s] |= {a, b}
            g[a].add(s)
            g[b].add(s)
            nxt.append(s)
        level = nxt
    return g


def diameter(g, nodes=None) -> int:
    nodes = list(g) if nodes is None else nodes
    best = 0
    for s in nodes:
        dist = {s: 0}
        q = deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        best = max(best, max(dist[t] for t in nodes))
    return best


def bisection(g, n: int) -> int:
    """The bisection width, exactly: the fewest links cut by any split of the n processors (nodes 0 .. n-1) into two
    halves.  For graphs with switch nodes (the tree), the switches are placed on whichever side cuts fewer links,
    by exhaustive choice too (small trees only)."""
    procs = list(range(n))
    extra = [v for v in g if v >= n]
    edges = {(min(u, v), max(u, v)) for u in g for v in g[u]}
    best = None
    for half in itertools.combinations(procs[1:], n // 2 - 1):
        side = set((0,) + half)
        if extra:
            for mask in range(1 << len(extra)):
                s2 = side | {extra[i] for i in range(len(extra)) if mask >> i & 1}
                cut = sum((u in s2) != (v in s2) for u, v in edges)
                best = cut if best is None else min(best, cut)
        else:
            cut = sum((u in side) != (v in side) for u, v in edges)
            best = cut if best is None else min(best, cut)
    return best
