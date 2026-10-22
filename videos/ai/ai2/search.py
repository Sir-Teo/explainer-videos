"""Search for Part 2: shortest paths on grids, and the sliding-tile puzzles.

* :func:`grid_search` is best-first search on a grid of free and blocked cells with sixteen move directions (the
  eight neighbours and the eight knight-like steps), each costing its Euclidean length, so a path's cost is never
  less than the straight-line distance. ``f = wg * g + wh * h`` with ``h`` the Euclidean distance to the goal:
  Dijkstra's algorithm (wh = 0), A* (wg = wh = 1), weighted A* (wh > 1) and greedy best-first search (wg = 0).
  It records the order in which cells are expanded, for drawing the frontier as it spreads.
* The 8-puzzle: permutations ranked by their Lehmer code, a breadth-first sweep of all 181,440 reachable states,
  and A* with no heuristic, with the misplaced-tile count and with the Manhattan distance.
* The 15-puzzle: IDA* (Korf 1985) with the misplaced tiles, the Manhattan distance, or an additive 5-5-5 pattern
  database (Culberson & Schaeffer 1998; Korf & Felner 2002), built here by breadth-first search.
"""

from __future__ import annotations

import numpy as np
from numba import njit

# ---------------------------------------------------------------------------
# Grids
# ---------------------------------------------------------------------------
MOVES = np.array([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1),
                  (1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)], np.int64)


@njit(cache=True)
def _heap_push(hk, hv, n, key, val):
    i = n
    hk[i] = key
    hv[i] = val
    while i > 0:
        p = (i - 1) // 2
        if hk[p] <= hk[i]:
            break
        hk[p], hk[i] = hk[i], hk[p]
        hv[p], hv[i] = hv[i], hv[p]
        i = p
    return n + 1


@njit(cache=True)
def _heap_pop(hk, hv, n):
    key, val = hk[0], hv[0]
    n -= 1
    hk[0] = hk[n]
    hv[0] = hv[n]
    i = 0
    while True:
        l = 2 * i + 1
        if l >= n:
            break
        c = l
        if l + 1 < n and hk[l + 1] < hk[l]:
            c = l + 1
        if hk[i] <= hk[c]:
            break
        hk[c], hk[i] = hk[i], hk[c]
        hv[c], hv[i] = hv[i], hv[c]
        i = c
    return key, val, n


@njit(cache=True)
def _passable(free, r, c, dr, dc):
    H, W = free.shape
    r2, c2 = r + dr, c + dc
    if r2 < 0 or r2 >= H or c2 < 0 or c2 >= W or not free[r2, c2]:
        return False
    ar, ac = abs(dr), abs(dc)
    if ar == 1 and ac == 1:  # a diagonal step may not cut a corner
        return free[r + dr, c] and free[r, c + dc]
    if ar == 2:  # (2, 1): the line crosses (sign, 0) and (sign, dc)
        s = dr // 2
        return free[r + s, c] and free[r + s, c + dc]
    if ac == 2:
        s = dc // 2
        return free[r, c + s] and free[r + dr, c + s]
    return True


@njit(cache=True)
def grid_search(free, sr, sc, gr, gc, wg, wh, moves):
    """Best-first search; returns (expanded, cost, order, parent, g). ``order[r, c]`` is the step at which the cell
    was expanded (-1 never); ties in f go to the larger g (the deeper node), as usual."""
    H, W = free.shape
    N = H * W
    g = np.full(N, np.inf)
    parent = np.full(N, -1, np.int64)
    closed = np.zeros(N, np.bool_)
    order = np.full((H, W), -1, np.int64)
    cap = N * moves.shape[0] + 16
    hk = np.empty(cap)
    hv = np.empty(cap, np.int64)
    n = 0
    s = sr * W + sc
    goal = gr * W + gc
    g[s] = 0.0
    h0 = np.hypot(sr - gr, sc - gc)
    n = _heap_push(hk, hv, n, wh * h0, s)
    step = 0
    while n > 0:
        key, u, n = _heap_pop(hk, hv, n)
        if closed[u]:
            continue
        closed[u] = True
        r, c = u // W, u % W
        order[r, c] = step
        step += 1
        if u == goal:
            return step, g[u], order, parent, g
        for k in range(moves.shape[0]):
            dr, dc = moves[k, 0], moves[k, 1]
            if not _passable(free, r, c, dr, dc):
                continue
            v = (r + dr) * W + (c + dc)
            if closed[v]:
                continue
            ng = g[u] + np.hypot(dr, dc)
            if ng < g[v] - 1e-12:
                g[v] = ng
                parent[v] = u
                h = np.hypot(r + dr - gr, c + dc - gc)
                f = wg * ng + wh * h
                n = _heap_push(hk, hv, n, f - 1e-7 * ng, v)
    return step, np.inf, order, parent, g


def path_cells(parent: np.ndarray, W: int, sr: int, sc: int, gr: int, gc: int) -> list[tuple[int, int]]:
    out, u = [], gr * W + gc
    while u != -1:
        out.append((int(u // W), int(u % W)))
        if u == sr * W + sc:
            break
        u = int(parent[u])
    return out[::-1]


def random_grid(rng, H=48, W=80, n_blocks=26, max_len=14) -> np.ndarray:
    """Free cells with random wall segments (horizontal or vertical bars, a cell thick)."""
    free = np.ones((H, W), bool)
    for _ in range(n_blocks):
        L = int(rng.integers(5, max_len))
        if rng.random() < 0.5:
            r, c = int(rng.integers(2, H - 2)), int(rng.integers(0, W - L))
            free[r, c:c + L] = False
        else:
            r, c = int(rng.integers(0, H - L)), int(rng.integers(2, W - 2))
            free[r:r + L, c] = False
    return free


# ---------------------------------------------------------------------------
# The 8-puzzle: states are permutations of 0..8 (0 the blank), position-major, ranked by the Lehmer code
# ---------------------------------------------------------------------------
FACT9 = np.array([1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880], np.int64)
GOAL8 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0], np.int64)  # the blank last


@njit(cache=True)
def rank9(p):
    r = 0
    for i in range(9):
        smaller = 0
        for j in range(i + 1, 9):
            if p[j] < p[i]:
                smaller += 1
        r += smaller * FACT9[8 - i]
    return r


@njit(cache=True)
def unrank9(r):
    p = np.empty(9, np.int64)
    used = np.zeros(9, np.bool_)
    for i in range(9):
        f = FACT9[8 - i]
        k = r // f
        r = r % f
        cnt = -1
        for v in range(9):
            if not used[v]:
                cnt += 1
                if cnt == k:
                    p[i] = v
                    used[v] = True
                    break
    return p


@njit(cache=True)
def bfs8(goal):
    """Distance (in moves) of every permutation from ``goal``; -1 for the unreachable half."""
    dist = np.full(362880, -1, np.int64)
    q = np.empty(362880, np.int64)
    s = rank9(goal)
    dist[s] = 0
    q[0] = s
    head, tail = 0, 1
    while head < tail:
        u = q[head]
        head += 1
        p = unrank9(u)
        b = 0
        for i in range(9):
            if p[i] == 0:
                b = i
        br, bc = b // 3, b % 3
        for k in range(4):
            dr = (1, -1, 0, 0)[k]
            dc = (0, 0, 1, -1)[k]
            r2, c2 = br + dr, bc + dc
            if r2 < 0 or r2 > 2 or c2 < 0 or c2 > 2:
                continue
            j = r2 * 3 + c2
            p[b], p[j] = p[j], p[b]
            v = rank9(p)
            p[b], p[j] = p[j], p[b]
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q[tail] = v
                tail += 1
    return dist


@njit(cache=True)
def h8(p, kind):
    """0: no heuristic; 1: misplaced tiles; 2: Manhattan distance (goal: 1..8 in order, blank last)."""
    if kind == 0:
        return 0
    h = 0
    for i in range(9):
        t = p[i]
        if t == 0:
            continue
        if kind == 1:
            if t != i + 1:
                h += 1
        else:
            gi = t - 1
            h += abs(i // 3 - gi // 3) + abs(i % 3 - gi % 3)
    return h


@njit(cache=True)
def astar8(start, kind):
    """A* on the 8-puzzle toward GOAL8; returns (nodes expanded, solution length)."""
    g = np.full(362880, 10_000, np.int64)
    closed = np.zeros(362880, np.bool_)
    cap = 362880 * 4 + 8
    hk = np.empty(cap)
    hv = np.empty(cap, np.int64)
    n = 0
    s = rank9(start)
    goal = rank9(GOAL8)
    g[s] = 0
    n = _heap_push(hk, hv, n, float(h8(start, kind)), s)
    expanded = 0
    while n > 0:
        key, u, n = _heap_pop(hk, hv, n)
        if closed[u]:
            continue
        closed[u] = True
        if u == goal:
            return expanded, g[u]
        expanded += 1
        p = unrank9(u)
        b = 0
        for i in range(9):
            if p[i] == 0:
                b = i
        br, bc = b // 3, b % 3
        for k in range(4):
            dr = (1, -1, 0, 0)[k]
            dc = (0, 0, 1, -1)[k]
            r2, c2 = br + dr, bc + dc
            if r2 < 0 or r2 > 2 or c2 < 0 or c2 > 2:
                continue
            j = r2 * 3 + c2
            p[b], p[j] = p[j], p[b]
            v = rank9(p)
            hv_ = h8(p, kind)
            p[b], p[j] = p[j], p[b]
            if closed[v]:
                continue
            ng = g[u] + 1
            if ng < g[v]:
                g[v] = ng
                n = _heap_push(hk, hv, n, ng + hv_ - 1e-3 * ng, v)
    return expanded, -1


def effective_branching(N: float, d: int) -> float:
    """b* with N + 1 = 1 + b* + b*^2 + ... + b*^d (Nilsson), by bisection."""
    if d <= 0:
        return float("nan")
    lo, hi = 1.0, max(2.0, N)
    for _ in range(200):
        b = (lo + hi) / 2
        s = sum(b ** k for k in range(d + 1))
        if s < N + 1:
            lo = b
        else:
            hi = b
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
# The 15-puzzle: IDA* with three heuristics
# ---------------------------------------------------------------------------
GROUPS = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]], np.int64)  # 5-5-5 partition


def goal_pos15() -> np.ndarray:
    """Where each tile belongs: tile t (1..15) at position t - 1, the blank at 15."""
    gp = np.empty(16, np.int64)
    for t in range(1, 16):
        gp[t] = t - 1
    gp[0] = 15
    return gp


@njit(cache=True)
def _pdb_index(pos, group):
    """Positions (0..15) of a group's five tiles as one number in [0, 16^5)."""
    k = 0
    for i in range(group.shape[0]):
        k = k * 16 + pos[group[i]]
    return k


@njit(cache=True)
def build_pdb(group):
    """Additive pattern database for the tiles in ``group``: the fewest moves *of those tiles* that bring them home,
    other tiles ignored and blank moves free. Breadth-first over (tile positions, blank position), cost layer by cost
    layer, then the minimum over the blank. Returns a uint8 table indexed by :func:`_pdb_index`."""
    m = group.shape[0]
    S = 16 ** (m + 1)
    dist = np.full(S, 255, np.uint8)
    cur = np.empty(6_000_000, np.int64)
    nxt = np.empty(6_000_000, np.int64)
    # the goal: tile t at t - 1, the blank at 15
    key = 0
    for i in range(m):
        key = key * 16 + (group[i] - 1)
    key = key * 16 + 15
    dist[key] = 0
    cur[0] = key
    ncur = 1
    cost = 0
    occ = np.zeros(16, np.int64)  # occupant: 0 nobody, i + 1 the group's i-th tile
    pos = np.empty(m, np.int64)
    while ncur > 0:
        # within a layer, blank moves cost nothing: flood the layer first
        head = 0
        while head < ncur:
            u = cur[head]
            head += 1
            b = u % 16
            rest = u // 16
            for i in range(m - 1, -1, -1):
                pos[i] = rest % 16
                rest //= 16
            occ[:] = 0
            for i in range(m):
                occ[pos[i]] = i + 1
            br, bc = b // 4, b % 4
            for k in range(4):
                r2 = br + (1, -1, 0, 0)[k]
                c2 = bc + (0, 0, 1, -1)[k]
                if r2 < 0 or r2 > 3 or c2 < 0 or c2 > 3:
                    continue
                j = r2 * 4 + c2
                if occ[j] == 0:  # the blank swaps with a tile outside the group: free
                    v = (u // 16) * 16 + j
                    if dist[v] == 255:
                        dist[v] = cost
                        cur[ncur] = v
                        ncur += 1
        nn = 0
        for idx in range(ncur):
            u = cur[idx]
            b = u % 16
            rest = u // 16
            for i in range(m - 1, -1, -1):
                pos[i] = rest % 16
                rest //= 16
            occ[:] = 0
            for i in range(m):
                occ[pos[i]] = i + 1
            br, bc = b // 4, b % 4
            for k in range(4):
                r2 = br + (1, -1, 0, 0)[k]
                c2 = bc + (0, 0, 1, -1)[k]
                if r2 < 0 or r2 > 3 or c2 < 0 or c2 > 3:
                    continue
                j = r2 * 4 + c2
                if occ[j] > 0:  # a group tile slides into the blank: costs one
                    t = occ[j] - 1
                    v = 0
                    for i in range(m):
                        v = v * 16 + (b if i == t else pos[i])
                    v = v * 16 + j
                    if dist[v] == 255:
                        dist[v] = cost + 1
                        nxt[nn] = v
                        nn += 1
        cur, nxt = nxt, cur
        ncur = nn
        cost += 1
    out = np.full(16 ** m, 255, np.uint8)
    for k in range(S):
        if dist[k] < out[k // 16]:
            out[k // 16] = dist[k]
    return out


@njit(cache=True)
def _h15(pos, kind, gpos, pdbs, groups):
    h = 0
    if kind == 0:
        for t in range(1, 16):
            if pos[t] != gpos[t]:
                h += 1
    elif kind == 1:
        for t in range(1, 16):
            h += abs(pos[t] // 4 - gpos[t] // 4) + abs(pos[t] % 4 - gpos[t] % 4)
    else:
        for gi in range(groups.shape[0]):
            h += pdbs[gi, _pdb_index(pos, groups[gi])]
    return h


@njit  # no cache: numba's cache of recursive functions can crash on reload
def _ida_dfs(pos, board, g, bound, prev, kind, gpos, pdbs, groups, counter, limit):
    counter[0] += 1
    h = _h15(pos, kind, gpos, pdbs, groups)
    f = g + h
    if f > bound:
        return f
    if h == 0:
        return -1  # solved
    if counter[0] > limit:
        return 10_000
    b = pos[0]
    br, bc = b // 4, b % 4
    best = 10_000
    for k in range(4):
        r2 = br + (1, -1, 0, 0)[k]
        c2 = bc + (0, 0, 1, -1)[k]
        if r2 < 0 or r2 > 3 or c2 < 0 or c2 > 3:
            continue
        j = r2 * 4 + c2
        if j == prev:
            continue
        t = board[j]
        board[b], board[j] = t, 0
        pos[t], pos[0] = b, j
        r = _ida_dfs(pos, board, g + 1, bound, b, kind, gpos, pdbs, groups, counter, limit)
        board[j], board[b] = t, 0
        pos[t], pos[0] = j, b
        if r == -1:
            return -1
        if r < best:
            best = r
    return best


@njit  # no cache: numba's cache of recursive functions can crash on reload
def ida15(board0, kind, gpos, pdbs, groups, limit):
    """IDA* on the 15-puzzle. ``board0[i]`` is the tile at position i. Returns (nodes generated, solution length),
    the length -1 if the node limit was hit first."""
    board = board0.copy()
    pos = np.empty(16, np.int64)
    for i in range(16):
        pos[board[i]] = i
    counter = np.zeros(1, np.int64)
    bound = _h15(pos, kind, gpos, pdbs, groups)
    while True:
        r = _ida_dfs(pos, board, 0, bound, -1, kind, gpos, pdbs, groups, counter, limit)
        if r == -1:
            return counter[0], bound
        if counter[0] > limit or r >= 10_000:
            return counter[0], -1
        bound = r


def scramble15(rng, steps: int) -> np.ndarray:
    """A 15-puzzle position made by a random walk of the blank from the goal (no immediate reversals)."""
    board = np.array(list(range(1, 16)) + [0], np.int64)
    b, prev = 15, -1
    for _ in range(steps):
        r, c = divmod(b, 4)
        opts = [(r + dr) * 4 + (c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= r + dr < 4 and 0 <= c + dc < 4 and (r + dr) * 4 + (c + dc) != prev]
        j = opts[int(rng.integers(len(opts)))]
        board[b], board[j] = board[j], 0
        prev, b = b, j
    return board
