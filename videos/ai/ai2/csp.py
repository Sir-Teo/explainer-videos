"""Constraint satisfaction for Part 2: Sudoku as 81 variables with domains 1..9 and 'all different' in every row,
column and box.

* :func:`make_puzzle`: a full grid by randomized backtracking, then clues removed one at a time (random order)
  while the solution stays unique.
* :func:`ac3`: arc consistency (Mackworth 1977): revise each arc (X, Y) by deleting values of X that no value of Y
  supports, re-queueing X's other neighbours when X's domain shrinks. Records every deletion, to replay it.
* :func:`backtrack`: depth-first search over assignments, counted, in four versions: plain (cells in reading order,
  check only against assigned neighbours), forward checking, forward checking with the minimum-remaining-values
  ordering, and maintaining arc consistency (MAC) with MRV.
"""

from __future__ import annotations

import numpy as np

CELLS = [(r, c) for r in range(9) for c in range(9)]


def _peers():
    out = []
    for r, c in CELLS:
        ps = set()
        for k in range(9):
            ps.add((r, k))
            ps.add((k, c))
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(3):
            for j in range(3):
                ps.add((br + i, bc + j))
        ps.discard((r, c))
        out.append(sorted(9 * a + b for a, b in ps))
    return out


PEERS = _peers()


def count_solutions(grid, limit=2) -> int:
    """Solutions of a grid (0 = empty), up to ``limit``, by MRV backtracking with bitmasks."""
    g = list(grid)
    found = [0]

    def cand(i):
        used = 0
        for p in PEERS[i]:
            if g[p]:
                used |= 1 << g[p]
        return [v for v in range(1, 10) if not used >> v & 1]

    def go():
        if found[0] >= limit:
            return
        best, bc = None, None
        for i in range(81):
            if g[i] == 0:
                c = cand(i)
                if best is None or len(c) < len(bc):
                    best, bc = i, c
                    if len(c) <= 1:
                        break
        if best is None:
            found[0] += 1
            return
        for v in bc:
            g[best] = v
            go()
            g[best] = 0

    go()
    return found[0]


def make_puzzle(rng, min_clues=22):
    g = [0] * 81

    def fill(i):
        if i == 81:
            return True
        used = {g[p] for p in PEERS[i]}
        for v in rng.permutation(9) + 1:
            if v not in used:
                g[i] = int(v)
                if fill(i + 1):
                    return True
        g[i] = 0
        return False

    fill(0)
    solution = g[:]
    puzzle = g[:]
    for i in rng.permutation(81):
        if sum(1 for x in puzzle if x) <= min_clues:
            break
        keep = puzzle[i]
        puzzle[i] = 0
        if count_solutions(puzzle) != 1:
            puzzle[i] = keep
    return puzzle, solution


def domains_of(puzzle):
    return [({puzzle[i]} if puzzle[i] else set(range(1, 10))) for i in range(81)]


def ac3(D, log=None) -> bool:
    """Make every arc consistent, in place. Returns False if a domain empties. ``log`` gets (cell, value removed)."""
    queue = [(i, j) for i in range(81) for j in PEERS[i]]
    inq = set(queue)
    head = 0
    while head < len(queue):
        i, j = queue[head]
        head += 1
        inq.discard((i, j))
        # 'all different': a value of i is unsupported only when j's domain is exactly that value
        if len(D[j]) == 1:
            v = next(iter(D[j]))
            if v in D[i]:
                D[i].discard(v)
                if log is not None:
                    log.append((i, v))
                if not D[i]:
                    return False
                for k in PEERS[i]:
                    if k != j and (k, i) not in inq:
                        queue.append((k, i))
                        inq.add((k, i))
    return True


def backtrack(puzzle, kind: str, node_limit=5_000_000):
    """Count the assignments tried (nodes) until the first solution. kind: plain, fc, mrv, mac."""
    nodes = [0]
    D = domains_of(puzzle)
    if kind == "mac":
        ac3(D)
    elif kind in ("fc", "mrv"):
        for i in range(81):
            if puzzle[i]:
                for p in PEERS[i]:
                    D[p].discard(puzzle[i])
    assign = list(puzzle)

    def consistent(i, v):
        return all(assign[p] != v for p in PEERS[i])

    def pick():
        if kind in ("mrv", "mac"):
            best, bs = None, 10
            for i in range(81):
                if not assign[i] and len(D[i]) < bs:
                    best, bs = i, len(D[i])
            return best
        for i in range(81):
            if not assign[i]:
                return i
        return None

    def go():
        i = pick()
        if i is None:
            return True
        if nodes[0] > node_limit:
            return False
        vals = sorted(D[i]) if kind != "plain" else range(1, 10)
        for v in vals:
            if kind == "plain" and not consistent(i, v):
                continue
            nodes[0] += 1
            assign[i] = v
            if kind == "plain":
                if go():
                    return True
            else:
                saved = [set(d) for d in D]
                D[i] = {v}
                ok = True
                if kind == "mac":
                    ok = ac3(D)
                else:
                    for p in PEERS[i]:
                        if not assign[p]:
                            D[p].discard(v)
                            if not D[p]:
                                ok = False
                                break
                if ok and go():
                    return True
                D[:] = saved
            assign[i] = 0
        return False

    ok = go()
    return nodes[0], ok, assign
