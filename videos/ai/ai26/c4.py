"""Connect Four for Part 26: the rules on bitboards, a perfect solver, and plain Monte Carlo tree search.

The board is 7 columns of 6. A position is two 64-bit integers, after Pascal Pons's solver
(http://blog.gamesolver.org): ``mask`` has a bit for every stone, ``pos`` for the stones of the player to move.
Column c holds bits 7c .. 7c+5 (bit 7c+6 is a sentinel), so a stone's neighbours are 1 (up), 7 (right), 6 and 8
(the diagonals) bits away, and four in a row is four shifts.

The solver is negamax with alpha-beta pruning, a transposition table, centre-first move ordering refined by how many
threats a move makes, and a null-window search for the exact score (all after Pons). The score of a position is
positive if the player to move wins: (43 - stones at the end) / 2 for a win as early as possible, 0 for a draw.
"""

from __future__ import annotations

import numpy as np
from numba import njit

W, H = 7, 6
H1 = H + 1
SIZE = W * H
BOTTOM = sum(1 << (c * H1) for c in range(W))
BOARD = BOTTOM * ((1 << H) - 1)
ORDER = np.array([3, 2, 4, 1, 5, 0, 6], dtype=np.int64)  # centre first
MIN_SCORE = -(SIZE // 2) + 3
MAX_SCORE = (SIZE + 1) // 2 - 3


@njit(cache=True)
def top_mask(c):
    return np.int64(1) << np.int64(H - 1 + c * H1)


@njit(cache=True)
def bottom_mask(c):
    return np.int64(1) << np.int64(c * H1)


@njit(cache=True)
def column_mask(c):
    return np.int64((1 << H) - 1) << np.int64(c * H1)


@njit(cache=True)
def alignment(p):
    m = p & (p >> 7)  # horizontal
    if m & (m >> 14):
        return True
    m = p & (p >> 6)  # diagonal /
    if m & (m >> 12):
        return True
    m = p & (p >> 8)  # diagonal \
    if m & (m >> 16):
        return True
    m = p & (p >> 1)  # vertical
    if m & (m >> 2):
        return True
    return False


@njit(cache=True)
def can_play(mask, c):
    return (mask & top_mask(c)) == 0


@njit(cache=True)
def play(pos, mask, c):
    """Drop a stone in column c; returns the position from the other player's side."""
    pos2 = pos ^ mask
    mask2 = mask | (mask + bottom_mask(c))
    return pos2, mask2


@njit(cache=True)
def is_winning_move(pos, mask, c):
    p = pos | ((mask + bottom_mask(c)) & column_mask(c))
    return alignment(p)


@njit(cache=True)
def popcount(m):
    c = 0
    while m:
        m &= m - 1
        c += 1
    return c


@njit(cache=True)
def winning_cells(p, mask):
    """Empty cells (anywhere, not only playable) that would complete four for the stones ``p``."""
    BOARDM = np.int64(0)
    for c in range(W):
        BOARDM |= np.int64((1 << H) - 1) << np.int64(c * H1)
    # vertical
    r = (p << 1) & (p << 2) & (p << 3)
    # horizontal
    q = (p << 7) & (p << 14)
    r |= q & (p << 21)
    r |= q & (p >> 7)
    q = (p >> 7) & (p >> 14)
    r |= q & (p << 7)
    r |= q & (p >> 21)
    # diagonal 1
    q = (p << 6) & (p << 12)
    r |= q & (p << 18)
    r |= q & (p >> 6)
    q = (p >> 6) & (p >> 12)
    r |= q & (p << 6)
    r |= q & (p >> 18)
    # diagonal 2
    q = (p << 8) & (p << 16)
    r |= q & (p << 24)
    r |= q & (p >> 8)
    q = (p >> 8) & (p >> 16)
    r |= q & (p << 8)
    r |= q & (p >> 24)
    return r & (BOARDM ^ mask)


@njit(cache=True)
def possible(mask):
    BOT = np.int64(0)
    for c in range(W):
        BOT |= np.int64(1) << np.int64(c * H1)
    BRD = BOT * np.int64((1 << H) - 1)
    return (mask + BOT) & BRD


@njit(cache=True)
def non_losing_moves(pos, mask):
    """Moves that don't hand the opponent an immediate win (0 if every move loses)."""
    pm = possible(mask)
    opp_win = winning_cells(pos ^ mask, mask)
    forced = pm & opp_win
    if forced:
        if forced & (forced - 1):  # two threats: lost
            return np.int64(0)
        pm = forced
    return pm & ~(opp_win >> 1)  # never play just below an opponent's winning cell


@njit(cache=True)
def tt_key(pos, mask):
    return pos + mask


@njit(cache=True)
def negamax(pos, mask, moves, alpha, beta, tt_keys, tt_vals, counter):
    counter[0] += 1
    nxt = non_losing_moves(pos, mask)
    if nxt == 0:
        return -((SIZE - moves) // 2)
    if moves >= SIZE - 2:
        return 0
    mn = -((SIZE - 2 - moves) // 2)
    if alpha < mn:
        alpha = mn
        if alpha >= beta:
            return alpha
    mx = (SIZE - 1 - moves) // 2
    key = tt_key(pos, mask)
    slot = key % tt_keys.shape[0]
    if tt_keys[slot] == key:
        mx = tt_vals[slot] + MIN_SCORE - 1
    if beta > mx:
        beta = mx
        if alpha >= beta:
            return beta
    # order the moves: more threats created first, ties centre first
    cols = np.empty(W, np.int64)
    scores = np.empty(W, np.int64)
    n = 0
    for i in range(W):
        c = ORDER[i]
        mv = nxt & column_mask(c)
        if mv:
            s = popcount(winning_cells(pos | mv, mask))
            j = n
            while j > 0 and scores[j - 1] < s:
                cols[j] = cols[j - 1]
                scores[j] = scores[j - 1]
                j -= 1
            cols[j] = c
            scores[j] = s
            n += 1
    for k in range(n):
        p2, m2 = play(pos, mask, cols[k])
        s = -negamax(p2, m2, moves + 1, -beta, -alpha, tt_keys, tt_vals, counter)
        if s >= beta:
            return s
        if s > alpha:
            alpha = s
    tt_keys[slot] = key
    tt_vals[slot] = alpha - MIN_SCORE + 1
    return alpha


@njit(cache=True)
def half(x):
    """x / 2 rounded toward zero (C's integer division, which the search's bounds assume)."""
    return -((-x) // 2) if x < 0 else x // 2


@njit(cache=True)
def solve_tt(pos, mask, moves, tt_keys, tt_vals, counter):
    """The exact score of the position for the player to move."""
    for c in range(W):
        if can_play(mask, c) and is_winning_move(pos, mask, c):
            return (SIZE + 1 - moves) // 2
    lo = -((SIZE - moves) // 2)
    hi = (SIZE + 1 - moves) // 2
    while lo < hi:  # null-window searches narrow [lo, hi] onto the score
        med = lo + half(hi - lo)
        if med <= 0 and half(lo) < med:
            med = half(lo)
        elif med >= 0 and half(hi) > med:
            med = half(hi)
        r = negamax(pos, mask, moves, med, med + 1, tt_keys, tt_vals, counter)
        if r <= med:
            hi = r
        else:
            lo = r
    return lo


class Solver:
    """A perfect player: ``score(moves)`` for the side to move, ``move_scores(moves)`` for each column."""

    def __init__(self, log2_size: int = 23):
        n = (1 << log2_size) + 9  # an odd-ish size spreads keys
        self.keys = np.zeros(n, np.int64)
        self.vals = np.zeros(n, np.int8)
        self.counter = np.zeros(1, np.int64)

    def reset(self):
        self.keys[:] = 0

    def score(self, pos: int, mask: int, moves: int) -> int:
        return int(solve_tt(np.int64(pos), np.int64(mask), moves, self.keys, self.vals, self.counter))

    def move_scores(self, pos: int, mask: int, moves: int) -> np.ndarray:
        """Score of each legal column from the mover's side (NaN if full)."""
        out = np.full(W, np.nan)
        for c in range(W):
            if not can_play(mask, c):
                continue
            if is_winning_move(pos, mask, c):
                out[c] = (SIZE + 1 - moves) // 2
                continue
            p2, m2 = play(pos, mask, c)
            out[c] = -self.score(int(p2), int(m2), moves + 1)
        return out


# ---------------------------------------------------------------------------
# A position as an object, for search and for drawing
# ---------------------------------------------------------------------------
class Board:
    __slots__ = ("pos", "mask", "moves", "history")

    def __init__(self, pos=0, mask=0, moves=0, history=()):
        self.pos, self.mask, self.moves, self.history = pos, mask, moves, tuple(history)

    @classmethod
    def from_moves(cls, seq) -> "Board":
        b = cls()
        for c in seq:
            b = b.play(int(c))
        return b

    def legal(self) -> list[int]:
        return [c for c in range(W) if not self.mask & (1 << (H - 1 + c * H1))]

    def wins_with(self, c: int) -> bool:
        p = self.pos | ((self.mask + (1 << (c * H1))) & (((1 << H) - 1) << (c * H1)))
        return _align(p)

    def play(self, c: int) -> "Board":
        return Board(self.pos ^ self.mask, self.mask | (self.mask + (1 << (c * H1))), self.moves + 1,
                     self.history + (c,))

    def full(self) -> bool:
        return self.moves == SIZE

    def grid(self) -> np.ndarray:
        """6 x 7 array, row 0 at the bottom: +1 first player's stones, -1 second player's, 0 empty."""
        g = np.zeros((H, W), np.int8)
        mover = 1 if self.moves % 2 == 0 else -1  # the player to move: first player if an even number played
        for c in range(W):
            for r in range(H):
                bit = 1 << (c * H1 + r)
                if self.mask & bit:
                    g[r, c] = mover if self.pos & bit else -mover
        return g

    def planes(self) -> np.ndarray:
        """The network's input: the mover's stones, the opponent's (2 x 6 x 7)."""
        out = np.zeros((2, H, W), np.float32)
        for c in range(W):
            for r in range(H):
                bit = 1 << (c * H1 + r)
                if self.mask & bit:
                    out[0 if self.pos & bit else 1, r, c] = 1.0
        return out


def _align(p: int) -> bool:
    for s in (7, 6, 8, 1):
        m = p & (p >> s)
        if m & (m >> (2 * s)):
            return True
    return False


def last_mover_won(b: Board) -> bool:
    """Whether the player who just moved has four in a row (their stones are ``pos ^ mask``)."""
    return _align(b.pos ^ b.mask)


# ---------------------------------------------------------------------------
# Plain Monte Carlo tree search: UCT with random playouts
# ---------------------------------------------------------------------------
class UCTNode:
    __slots__ = ("board", "parent", "move", "children", "untried", "N", "W", "terminal", "value")

    def __init__(self, board: Board, parent=None, move=None):
        self.board, self.parent, self.move = board, parent, move
        self.children: list[UCTNode] = []
        self.N, self.W = 0, 0.0
        if parent is not None and last_mover_won(board):
            self.terminal, self.value, self.untried = True, 1.0, []  # a win for the player who moved into it
        elif board.full():
            self.terminal, self.value, self.untried = True, 0.5, []
        else:
            self.terminal, self.value, self.untried = False, None, board.legal()


def random_playout(b: Board, rng) -> float:
    """Play random moves to the end; 1 if the player who moved *into* ``b`` wins, 0 if they lose, 1/2 a draw."""
    who = b.moves % 2  # the side to move at b; the player who moved into b is the other one
    while True:
        if b.full():
            return 0.5
        legal = b.legal()
        for c in legal:  # take an immediate win when there is one: a "smart" random playout
            if b.wins_with(c):
                return 0.0 if b.moves % 2 == who else 1.0
        b = b.play(legal[rng.integers(len(legal))])


def uct_search(root_board: Board, sims: int, rng, c: float = 1.4) -> UCTNode:
    root = UCTNode(root_board)
    for _ in range(sims):
        node = root
        while not node.terminal and not node.untried and node.children:  # selection
            lnN = np.log(node.N)
            node = max(node.children, key=lambda ch: ch.W / ch.N + c * np.sqrt(lnN / ch.N))
        if not node.terminal and node.untried:  # expansion
            m = node.untried.pop(rng.integers(len(node.untried)))
            node = UCTNode(node.board.play(m), node, m)
            node.parent.children.append(node)
        v = node.value if node.terminal else random_playout(node.board, rng)  # simulation
        while node is not None:  # backup: v is from the view of the player who moved into ``node``
            node.N += 1
            node.W += v
            v = 1.0 - v
            node = node.parent
    return root


def uct_move(b: Board, sims: int, rng) -> int:
    for c in b.legal():
        if b.wins_with(c):
            return c
    root = uct_search(b, sims, rng)
    return max(root.children, key=lambda ch: ch.N).move
