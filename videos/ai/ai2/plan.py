"""STRIPS planning for Part 2: the blocks world with a one-handed robot (pick-up, put-down, stack, unstack), as in
Fikes & Nilsson's STRIPS (1971) and Sussman's anomaly (1973).

A state is a set of true facts (a bitmask); an action has preconditions, an add list and a delete list. Everything
not mentioned stays as it is: the STRIPS assumption, which sidesteps the frame problem. Search: breadth-first
(blind), A* with h_max (admissible), and greedy best-first with the relaxed-plan heuristic h_FF (Hoffmann & Nebel
2001), where the relaxation ignores every delete list (Bonet & Geffner's HSP, 2001).
"""

from __future__ import annotations

import heapq
import itertools
from collections import deque
from math import comb, factorial


class Blocks:
    def __init__(self, names):
        self.names = list(names)
        n = len(self.names)
        self.facts: dict[tuple, int] = {}
        for x in range(n):
            for y in range(n):
                if x != y:
                    self._f(("on", x, y))
        for x in range(n):
            self._f(("ontable", x))
            self._f(("clear", x))
            self._f(("holding", x))
        self._f(("handempty",))
        F = self.F
        self.actions = []  # (name, pre, add, delete) as bitmasks
        for x in range(n):
            self.actions.append((("pickup", x), F("clear", x) | F("ontable", x) | F("handempty"), F("holding", x),
                                 F("clear", x) | F("ontable", x) | F("handempty")))
            self.actions.append((("putdown", x), F("holding", x), F("clear", x) | F("ontable", x) | F("handempty"),
                                 F("holding", x)))
            for y in range(n):
                if x == y:
                    continue
                self.actions.append((("stack", x, y), F("holding", x) | F("clear", y),
                                     F("on", x, y) | F("clear", x) | F("handempty"), F("holding", x) | F("clear", y)))
                self.actions.append((("unstack", x, y), F("on", x, y) | F("clear", x) | F("handempty"),
                                     F("holding", x) | F("clear", y), F("on", x, y) | F("clear", x) | F("handempty")))
        self.nf = len(self.facts)
        self.bits = [[i for i in range(self.nf) if pre >> i & 1] for _, pre, _, _ in self.actions]
        self.adds = [[i for i in range(self.nf) if add >> i & 1] for _, _, add, _ in self.actions]

    def _f(self, key):
        self.facts[key] = len(self.facts)

    def F(self, *key) -> int:
        return 1 << self.facts[tuple(key)]

    def state(self, towers) -> int:
        """Towers as lists of block indices, bottom first; the hand empty."""
        s = self.F("handempty")
        for t in towers:
            s |= self.F("ontable", t[0])
            for a, b in zip(t, t[1:]):
                s |= self.F("on", b, a)
            s |= self.F("clear", t[-1])
        return s

    def goal(self, towers) -> int:
        """The 'on' and 'ontable' facts of the towers (a partial state)."""
        g = 0
        for t in towers:
            g |= self.F("ontable", t[0])
            for a, b in zip(t, t[1:]):
                g |= self.F("on", b, a)
        return g

    def successors(self, s):
        for k, (name, pre, add, dele) in enumerate(self.actions):
            if s & pre == pre:
                yield k, (s & ~dele) | add

    def show(self, k) -> str:
        name = self.actions[k][0]
        return f"{name[0]}({', '.join(self.names[i] for i in name[1:])})"

    # -- relaxed-plan heuristics: ignore delete lists --------------------------------------------------------------
    def h_relaxed(self, s, g, kind="ff") -> float:
        INF = float("inf")
        cost = [0.0 if s >> i & 1 else INF for i in range(self.nf)]
        best = [None] * self.nf
        agg = max if kind == "max" else sum
        changed = True
        while changed:
            changed = False
            for k in range(len(self.actions)):
                pre = self.bits[k]
                c = agg((cost[i] for i in pre), default=0.0) if kind == "max" else sum(cost[i] for i in pre)
                if c == INF:
                    continue
                c += 1.0
                for i in self.adds[k]:
                    if c < cost[i]:
                        cost[i] = c
                        best[i] = k
                        changed = True
        goals = [i for i in range(self.nf) if g >> i & 1]
        if any(cost[i] == INF for i in goals):
            return INF
        if kind == "max":
            return max((cost[i] for i in goals), default=0.0)
        if kind == "add":
            return sum(cost[i] for i in goals)
        # FF: collect the supporting actions of a relaxed plan, each counted once
        plan, stack, seen = set(), list(goals), set()
        while stack:
            i = stack.pop()
            if i in seen or s >> i & 1:
                continue
            seen.add(i)
            k = best[i]
            plan.add(k)
            stack.extend(self.bits[k])
        return float(len(plan))

    # -- search --------------------------------------------------------------------------------------------------
    def bfs(self, s0, g, limit=3_000_000):
        if s0 & g == g:
            return [], 0
        parent = {s0: None}
        q = deque([s0])
        expanded = 0
        while q:
            s = q.popleft()
            expanded += 1
            for k, t in self.successors(s):
                if t not in parent:
                    parent[t] = (s, k)
                    if t & g == g:
                        return self._path(parent, t), expanded
                    q.append(t)
            if expanded > limit:
                break
        return None, expanded

    def best_first(self, s0, g, kind="max", greedy=False, limit=2_000_000):
        h0 = self.h_relaxed(s0, g, kind)
        tie = itertools.count()
        open_ = [(h0 if greedy else h0, next(tie), 0, s0)]
        gbest = {s0: 0}
        parent = {s0: None}
        expanded = 0
        closed = set()
        while open_:
            f, _, gs, s = heapq.heappop(open_)
            if s in closed:
                continue
            closed.add(s)
            if s & g == g:
                return self._path(parent, s), expanded
            expanded += 1
            if expanded > limit:
                break
            for k, t in self.successors(s):
                ng = gs + 1
                if t in closed or ng >= gbest.get(t, 1 << 30):
                    continue
                gbest[t] = ng
                parent[t] = (s, k)
                h = self.h_relaxed(t, g, kind)
                if h == float("inf"):
                    continue
                heapq.heappush(open_, (h if greedy else ng + h, next(tie), ng, t))
        return None, expanded

    def _path(self, parent, s):
        out = []
        while parent[s] is not None:
            s, k = parent[s]
            out.append(k)
        return out[::-1]

    def count_states(self, s0) -> int:
        seen = {s0}
        q = deque([s0])
        while q:
            s = q.popleft()
            for _, t in self.successors(s):
                if t not in seen:
                    seen.add(t)
                    q.append(t)
        return len(seen)


def towers_count(n: int) -> int:
    """Arrangements of n labelled blocks into towers on a table: sum over k towers of the Lah numbers
    L(n, k) = C(n-1, k-1) n! / k!."""
    if n == 0:
        return 1
    return sum(comb(n - 1, k - 1) * factorial(n) // factorial(k) for k in range(1, n + 1))


def random_towers(rng, n: int) -> list[list[int]]:
    perm = [int(x) for x in rng.permutation(n)]
    cuts = sorted(int(x) for x in rng.choice(range(1, n), size=int(rng.integers(0, n)), replace=False)) if n > 1 else []
    out, last = [], 0
    for c in cuts + [n]:
        out.append(perm[last:c])
        last = c
    return [t for t in out if t]
