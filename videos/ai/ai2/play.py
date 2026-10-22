"""Game search for Part 2: minimax and alpha-beta, counted; and a Samuel-style learner of an evaluation function.

Connect Four uses Part 26's bitboards and perfect solver (``videos/ai/ai26/c4.py``, after Pascal Pons).

* :func:`ttt_counts`: the whole game tree of tic-tac-toe, by minimax and by alpha-beta.
* :func:`uniform_counts`: alpha-beta on uniform trees (b children everywhere, depth d, random leaf values) with the
  best child always first, against Knuth and Moore's count b^ceil(d/2) + b^floor(d/2) - 1 of leaves.
* :func:`c4_count`: depth-limited negamax on Connect Four, without pruning, with alpha-beta in a random order, best-
  looking first (a static evaluation), or truly best first (an oracle that knows every child's value).
* :class:`Samuel`: a linear evaluation of Connect Four positions over a few hand-chosen features, learned from
  self-play the way Samuel's checkers player learned (1959): after each of its moves, the learning player (Alpha)
  nudges its evaluation of its previous position toward the score that the search now backs up; when Alpha beats
  the frozen player (Beta), Beta takes Alpha's weights.
"""

from __future__ import annotations

import math

import numpy as np
from numba import njit

from videos.ai.ai26 import c4

# ---------------------------------------------------------------------------
# Tic-tac-toe
# ---------------------------------------------------------------------------
LINES3 = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def _ttt_winner(b):
    for a, c, d in LINES3:
        if b[a] and b[a] == b[c] == b[d]:
            return b[a]
    return 0


def ttt_counts() -> dict:
    """Positions visited by minimax over the full tree of tic-tac-toe, and by alpha-beta (natural order, and the
    centre and corners first). Values from X's side: +1 win, 0 draw, -1 loss."""
    cnt = {"n": 0}

    def mm(b, p):
        cnt["n"] += 1
        w = _ttt_winner(b)
        if w:
            return w
        if 0 not in b:
            return 0
        vals = []
        for i in range(9):
            if b[i] == 0:
                b[i] = p
                vals.append(mm(b, -p))
                b[i] = 0
        return max(vals) if p == 1 else min(vals)

    def ab(b, p, a, be, order):
        cnt["n"] += 1
        w = _ttt_winner(b)
        if w:
            return w
        if 0 not in b:
            return 0
        if p == 1:
            v = -2
            for i in order:
                if b[i] == 0:
                    b[i] = p
                    v = max(v, ab(b, -p, a, be, order))
                    b[i] = 0
                    a = max(a, v)
                    if a >= be:
                        break
            return v
        v = 2
        for i in order:
            if b[i] == 0:
                b[i] = p
                v = min(v, ab(b, -p, a, be, order))
                b[i] = 0
                be = min(be, v)
                if a >= be:
                    break
        return v

    out = {}
    cnt["n"] = 0
    out["value"] = mm([0] * 9, 1)
    out["minimax"] = cnt["n"]
    cnt["n"] = 0
    v = ab([0] * 9, 1, -2, 2, list(range(9)))
    out["ab_natural"] = cnt["n"]
    cnt["n"] = 0
    v2 = ab([0] * 9, 1, -2, 2, [4, 0, 2, 6, 8, 1, 3, 5, 7])
    out["ab_centre"] = cnt["n"]
    assert v == v2 == out["value"]
    # complete games (leaves of the tree) and how they end
    games = {"x": 0, "o": 0, "draw": 0}

    def count_games(b, p):
        w = _ttt_winner(b)
        if w or 0 not in b:
            games["x" if w == 1 else "o" if w == -1 else "draw"] += 1
            return
        for i in range(9):
            if b[i] == 0:
                b[i] = p
                count_games(b, -p)
                b[i] = 0

    count_games([0] * 9, 1)
    out["games"] = games
    return out


# ---------------------------------------------------------------------------
# Uniform trees: the best case of alpha-beta
# ---------------------------------------------------------------------------
def uniform_counts(bs=(2, 3, 4, 5), depths=range(1, 9), seed=0) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    for b in bs:
        for d in depths:
            n_leaves = b ** d
            leaves = rng.permutation(n_leaves).astype(float)  # distinct values
            # exact values bottom-up; level k holds b^k nodes; the root maximizes
            vals = [None] * (d + 1)
            vals[d] = leaves
            for k in range(d - 1, -1, -1):
                ch = vals[k + 1].reshape(-1, b)
                vals[k] = ch.max(1) if k % 2 == 0 else ch.min(1)
            counted = {"leaves": 0, "nodes": 0}

            def ab(k, idx, a, be):
                counted["nodes"] += 1
                if k == d:
                    counted["leaves"] += 1
                    return vals[d][idx]
                kids = [idx * b + j for j in range(b)]
                kids.sort(key=lambda c: -vals[k + 1][c] if k % 2 == 0 else vals[k + 1][c])  # best first
                if k % 2 == 0:
                    v = -math.inf
                    for c in kids:
                        v = max(v, ab(k + 1, c, a, be))
                        a = max(a, v)
                        if a >= be:
                            break
                    return v
                v = math.inf
                for c in kids:
                    v = min(v, ab(k + 1, c, a, be))
                    be = min(be, v)
                    if a >= be:
                        break
                return v

            v = ab(0, 0, -math.inf, math.inf)
            assert v == vals[0][0]
            kk = b ** math.ceil(d / 2) + b ** (d // 2) - 1
            rows.append({"b": b, "d": d, "leaves": counted["leaves"], "formula": kk, "all": n_leaves})
            assert counted["leaves"] == kk, (b, d, counted["leaves"], kk)
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Connect Four: depth-limited negamax, counted
# ---------------------------------------------------------------------------
@njit(cache=True)
def static_eval(pos, mask):
    """A simple evaluation: (mover's cells that would complete four) - (opponent's)."""
    return float(c4.popcount(c4.winning_cells(pos, mask)) - c4.popcount(c4.winning_cells(pos ^ mask, mask)))


@njit  # no cache: numba's cache of recursive functions can crash on reload
def c4_search(pos, mask, moves, depth, alpha, beta, prune, order_kind, counter, seed):
    """Negamax to ``depth``. order_kind 0: a fresh pseudo-random order at every node; 1: best-looking first (children
    sorted by the static evaluation after the move)."""
    counter[0] += 1
    if moves == 42:
        return 0.0
    if depth == 0:
        return static_eval(pos, mask)
    cols = np.empty(7, np.int64)
    keys = np.empty(7, np.float64)
    n = 0
    for c in range(7):
        if c4.can_play(mask, c):
            cols[n] = c
            if order_kind == 1:
                if c4.is_winning_move(pos, mask, c):
                    keys[n] = -1e6
                else:
                    p2, m2 = c4.play(pos, mask, c)
                    keys[n] = static_eval(p2, m2) + 0.01 * abs(c - 3)  # low is good for us
            else:
                h = (counter[0] * 6364136223846793005 + seed * 1442695040888963407 + c * 2654435761) & 0x7FFFFFFF
                keys[n] = float(h)
            n += 1
    idx = np.argsort(keys[:n])
    best = -1e9
    for k in range(n):
        c = cols[idx[k]]
        if c4.is_winning_move(pos, mask, c):
            v = 1000.0 + depth
        else:
            p2, m2 = c4.play(pos, mask, c)
            v = -c4_search(p2, m2, moves + 1, depth - 1, -beta, -alpha, prune, order_kind, counter, seed)
        if v > best:
            best = v
        if prune:
            if v > alpha:
                alpha = v
            if alpha >= beta:
                break
    return best


class Oracle:
    """Alpha-beta with the truly best move first: each child's exact depth-limited value is known in advance
    (memoized negamax), so the search walks the minimal tree."""

    def __init__(self):
        self.memo = {}

    def value(self, pos, mask, moves, depth):
        key = (pos, mask, depth)
        if key in self.memo:
            return self.memo[key]
        if moves == 42:
            v = 0.0
        elif depth == 0:
            v = static_eval(np.int64(pos), np.int64(mask))
        else:
            v = -1e9
            for c in range(7):
                if not c4.can_play(np.int64(mask), c):
                    continue
                if c4.is_winning_move(np.int64(pos), np.int64(mask), c):
                    w = 1000.0 + depth
                else:
                    p2, m2 = c4.play(np.int64(pos), np.int64(mask), c)
                    w = -self.value(int(p2), int(m2), moves + 1, depth - 1)
                v = max(v, w)
        self.memo[key] = v
        return v

    def search(self, pos, mask, moves, depth, alpha, beta, counter):
        counter[0] += 1
        if moves == 42:
            return 0.0
        if depth == 0:
            return static_eval(np.int64(pos), np.int64(mask))
        kids = []
        for c in range(7):
            if not c4.can_play(np.int64(mask), c):
                continue
            if c4.is_winning_move(np.int64(pos), np.int64(mask), c):
                kids.append((1000.0 + depth, c, None))
            else:
                p2, m2 = c4.play(np.int64(pos), np.int64(mask), c)
                kids.append((-self.value(int(p2), int(m2), moves + 1, depth - 1), c, (int(p2), int(m2))))
        kids.sort(key=lambda t: -t[0])
        best = -1e9
        for exact, c, child in kids:
            if child is None:
                v = exact
            else:
                v = -self.search(child[0], child[1], moves + 1, depth - 1, -beta, -alpha, counter)
            best = max(best, v)
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return best


# ---------------------------------------------------------------------------
# A Samuel-style learner for Connect Four
# ---------------------------------------------------------------------------
def _windows() -> np.ndarray:
    """The 69 lines of four cells on the 7 x 6 board, as bitmasks (column c, row r is bit 7c + r)."""
    out = []
    for c in range(7):
        for r in range(6):
            for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
                cells = [(c + k * dc, r + k * dr) for k in range(4)]
                if all(0 <= x < 7 and 0 <= y < 6 for x, y in cells):
                    out.append(sum(1 << (7 * x + y) for x, y in cells))
    return np.array(out, np.int64)


WINDOWS = _windows()
FEATURES = ["one in a line", "two in a line", "three in a line", "centre column", "safe threats"]
N_FEAT = len(FEATURES)
CENTRE = np.int64(((1 << 6) - 1) << (7 * 3))


@njit(cache=True)
def features(pos, mask, windows):
    """From the side to move: (mine - theirs) for open lines of four holding one, two or three of one side's stones
    and none of the other's; stones in the centre column; empty cells that would complete four and are not directly
    playable (threats the opponent can't simply block next move)."""
    opp = pos ^ mask
    f = np.zeros(5)
    for i in range(windows.shape[0]):
        w = windows[i]
        a = c4.popcount(pos & w)
        b = c4.popcount(opp & w)
        if b == 0 and a > 0:
            f[a - 1] += 1.0
        elif a == 0 and b > 0:
            f[b - 1] -= 1.0
    f[3] = c4.popcount(pos & CENTRE) - c4.popcount(opp & CENTRE)
    play = c4.possible(mask)
    f[4] = c4.popcount(c4.winning_cells(pos, mask) & ~play) - c4.popcount(c4.winning_cells(opp, mask) & ~play)
    return f


@njit(cache=True)
def value(pos, mask, w, windows):
    return np.tanh(np.dot(w, features(pos, mask, windows)))


@njit  # no cache: numba's cache of recursive functions can crash on reload
def negamax_w(pos, mask, moves, depth, alpha, beta, w, windows, counter):
    """Alpha-beta to ``depth`` with the evaluation tanh(w . features); a win is 1, a loss -1, a draw 0 (a quicker
    win scores a hair more). Returns (value, best column)."""
    counter[0] += 1
    if moves == 42:
        return 0.0, -1
    for c in range(7):
        if c4.can_play(mask, c) and c4.is_winning_move(pos, mask, c):
            return 1.0 + 0.001 * depth, c
    if depth == 0:
        return value(pos, mask, w, windows), -1
    best, bc = -2.0, -1
    for i in range(7):
        c = c4.ORDER[i]
        if not c4.can_play(mask, c):
            continue
        p2, m2 = c4.play(pos, mask, c)
        v, _ = negamax_w(p2, m2, moves + 1, depth - 1, -beta, -alpha, w, windows, counter)
        v = -v
        if v > best:
            best, bc = v, c
        if v > alpha:
            alpha = v
        if alpha >= beta:
            break
    return best, bc


def play_game(wa, wb, depth, opening, windows=WINDOWS, learn=None) -> int:
    """One game: ``opening`` columns first, then player A (weights wa) and B (wb) alternate, A moving at the first
    position after the opening. ``learn``: (lr, grads list) to make A learn as it plays (Samuel's rule). Returns +1 if
    A wins, -1 if B wins, 0 for a draw."""
    b = c4.Board.from_moves(opening)
    if c4.last_mover_won(b):
        return 0  # (never happens with short openings)
    a_turn = True
    prev_feat = None
    cnt = np.zeros(1, np.int64)
    while True:
        if b.full():
            result = 0
            break
        w = wa if a_turn else wb
        v, c = negamax_w(np.int64(b.pos), np.int64(b.mask), b.moves, depth, -2.0, 2.0, w, windows, cnt)
        if learn is not None and a_turn:
            lr, log = learn
            f = features(np.int64(b.pos), np.int64(b.mask), windows)
            if prev_feat is not None:
                pv = math.tanh(float(np.dot(wa, prev_feat)))
                delta = max(-1.0, min(1.0, v)) - pv  # backed-up score now minus the static score then
                wa += lr * delta * (1 - pv * pv) * prev_feat
                log.append(delta)
            prev_feat = f
        nb = b.play(int(c))
        if c4.last_mover_won(nb):
            result = 1 if a_turn else -1
            b = nb
            break
        b = nb
        a_turn = not a_turn
    if learn is not None and prev_feat is not None:
        lr, log = learn
        pv = math.tanh(float(np.dot(wa, prev_feat)))
        delta = result - pv
        wa += lr * delta * (1 - pv * pv) * prev_feat
        log.append(delta)
    return result


def match(wa, wb, depth, openings) -> float:
    """A's score against B (win 1, draw 1/2) over the openings (an even number of plies each), each played twice:
    A moving first after the opening, then B."""
    s = 0.0
    for op in openings:
        s += (play_game(wa, wb, depth, list(op)) + 1) / 2
        s += (1 - play_game(wb, wa, depth, list(op))) / 2
    return s / (2 * len(openings))


def random_openings(rng, n, plies=4) -> list[list[int]]:
    out = []
    while len(out) < n:
        b = c4.Board()
        seq = []
        ok = True
        for _ in range(plies):
            c = int(rng.integers(7))
            if not c in b.legal():
                ok = False
                break
            b = b.play(c)
            seq.append(c)
            if c4.last_mover_won(b):
                ok = False
                break
        if ok:
            out.append(seq)
    return out
