"""Turing machines, one tape or several (Part 1; reused by Parts 6, 12, 25 and 26).

    m = TM.parse("1RB1LB_1LA1RZ")                 # the standard text form of a 2-symbol, 1-tape machine
    r = run(m, max_steps=100, record=True)       # r.steps, r.halted, r.state, r.tape(), r.history

    m = TM(rules=[("A", ("1", "_"), ("=", "1"), ("R", "R"), "A"), ...], start="A", tapes=2)

A rule is (state, symbols read, symbols written, moves, next state), one entry per tape.  ``"*"`` in a read pattern
matches any symbol and ``"="`` in a write keeps the symbol read; moves are ``L``, ``R`` or ``S`` (stay).  Rules are
tried in order, so a specific rule listed before a wildcard one takes precedence.  The blank is ``"_"``; the halting
states are ``H``, ``Z`` (the busy-beaver convention), ``accept`` and ``reject``.  Tapes are infinite both ways.

:func:`run_fast` runs a 2-symbol, 1-tape machine in compiled code (numba), for the busy beavers' tens of millions of
steps, keeping snapshots of the tape for the space-time picture.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

BLANK = "_"
HALT = ("H", "Z", "accept", "reject", "halt")


@dataclass
class TM:
    rules: list
    start: str = "A"
    tapes: int = 1
    name: str = ""

    def __post_init__(self):
        norm = []
        for st, rd, wr, mv, nx in self.rules:
            rd, wr, mv = (rd,) if isinstance(rd, str) else tuple(rd), (wr,) if isinstance(wr, str) else tuple(wr), \
                (mv,) if isinstance(mv, str) else tuple(mv)
            if not len(rd) == len(wr) == len(mv) == self.tapes:
                raise ValueError(f"rule {st, rd} does not have one entry per tape")
            norm.append((st, rd, wr, mv, nx))
        self.rules = norm
        self._by_state: dict[str, list] = {}
        for r in norm:
            self._by_state.setdefault(r[0], []).append(r)

    @property
    def states(self) -> list[str]:
        out = []
        for r in self.rules:
            for s in (r[0], r[4]):
                if s not in out:
                    out.append(s)
        return out

    def match(self, state: str, syms: tuple):
        for r in self._by_state.get(state, ()):
            if all(p == "*" or p == s for p, s in zip(r[1], syms)):
                return r
        return None

    @staticmethod
    def parse(table: str, name: str = "") -> "TM":
        """The standard text form of a 2-symbol machine, e.g. '1RB1LB_1LA1RZ': per state (A, B, ...), the action on
        reading 0 then on reading 1; Z halts; '---' is an undefined transition (the machine halts there).  The
        blank is 0 (written '_' on our tapes)."""
        rules = []
        for i, part in enumerate(table.split("_")):
            st = "ABCDEFG"[i]
            for sym in (0, 1):
                a = part[3 * sym: 3 * sym + 3]
                read = BLANK if sym == 0 else "1"
                if a == "---":
                    continue
                write = BLANK if a[0] == "0" else "1"
                nxt = "H" if a[2] in "ZH" else a[2]
                rules.append((st, read, write, a[1], nxt))
        return TM(rules, "A", 1, name or table)

    def table_text(self) -> list[tuple[str, str, str, str, str]]:
        """Single-tape rules as 5 strings, for a RuleTable."""
        return [(st, rd[0], wr[0], mv[0], nx) for st, rd, wr, mv, nx in self.rules]


@dataclass
class Result:
    steps: int
    halted: bool
    state: str
    tapes: list[dict] = field(default_factory=list)
    heads: list[int] = field(default_factory=list)
    history: list = field(default_factory=list)  # (state, heads, tuple of tape strings with offsets, rule index)

    def tape(self, i: int = 0, lo: int | None = None, hi: int | None = None) -> str:
        t = self.tapes[i]
        keys = [k for k, v in t.items() if v != BLANK]
        if lo is None:
            lo = min(keys + [self.heads[i]])
        if hi is None:
            hi = max(keys + [self.heads[i]])
        return "".join(t.get(k, BLANK) for k in range(lo, hi + 1))

    def ones(self, i: int = 0) -> int:
        return sum(1 for v in self.tapes[i].values() if v == "1")


def run(tm: TM, inputs=("",), max_steps: int = 100_000, record: bool = False, heads=None) -> Result:
    """Run from the input strings (one per tape; the heads start on their first cells, or at ``heads``)."""
    if isinstance(inputs, str):
        inputs = (inputs,)
    inputs = list(inputs) + [""] * (tm.tapes - len(inputs))
    tapes = [{i: c for i, c in enumerate(s) if c != BLANK} for s in inputs]
    hs = list(heads) if heads is not None else [0] * tm.tapes
    state = tm.start
    hist = []
    steps = 0

    def snap(rule_ix):
        hist.append((state, tuple(hs), tuple(dict(t) for t in tapes), rule_ix))

    while steps < max_steps and state not in HALT:
        syms = tuple(t.get(h, BLANK) for t, h in zip(tapes, hs))
        r = tm.match(state, syms)
        if r is None:  # no rule: the machine stops (and is said to halt)
            break
        if record:
            snap(tm.rules.index(r))
        _, _, wr, mv, nx = r
        for k in range(tm.tapes):
            w = syms[k] if wr[k] == "=" else wr[k]
            if w == BLANK:
                tapes[k].pop(hs[k], None)
            else:
                tapes[k][hs[k]] = w
            hs[k] += {"L": -1, "R": 1, "S": 0}[mv[k]]
        state = nx
        steps += 1
    if record:
        snap(None)
    halted = state in HALT or tm.match(state, tuple(t.get(h, BLANK) for t, h in zip(tapes, hs))) is None
    return Result(steps, halted, state, tapes, hs, hist)


def window(hist_entry, tape: int, lo: int, hi: int) -> str:
    """One tape of a recorded configuration, cells lo..hi."""
    t = hist_entry[2][tape]
    return "".join(t.get(k, BLANK) for k in range(lo, hi + 1))


def spacetime(res: Result, lo: int, hi: int, tape: int = 0) -> np.ndarray:
    """A recorded run as an array: row = step, column = cell lo..hi; 0 blank, 1 '1', 2 other symbols; the head's
    cell is 3 (drawn in the head's colour)."""
    rows = []
    for st, hs, tps, _ in res.history:
        t = tps[tape]
        row = [0 if t.get(k, BLANK) == BLANK else (1 if t.get(k) == "1" else 2) for k in range(lo, hi + 1)]
        if lo <= hs[tape] <= hi:
            row[hs[tape] - lo] = 3
        rows.append(row)
    return np.array(rows, np.int8)


# ---------------------------------------------------------------------------
# The fast path: 2-symbol, 1-tape machines in compiled code
# ---------------------------------------------------------------------------
def _arrays(tm: TM):
    states = [s for s in tm.states if s not in HALT]
    idx = {s: i for i, s in enumerate(states)}
    W = np.zeros((len(states), 2), np.int64)
    M = np.zeros((len(states), 2), np.int64)
    N = np.full((len(states), 2), -1, np.int64)
    for st, rd, wr, mv, nx in tm.rules:
        b = 0 if rd[0] == BLANK else 1
        W[idx[st], b] = 0 if wr[0] == BLANK else 1
        M[idx[st], b] = 1 if mv[0] == "R" else -1
        N[idx[st], b] = -1 if nx in HALT else idx[nx]
    return W, M, N


def _numba_run():
    from numba import njit

    @njit(cache=True)
    def go(W, M, N, size, max_steps, snap_every, n_snaps, snaps, heads, sbounds):
        tape = np.zeros(size, np.int8)
        head = size // 2
        st = 0
        steps = 0
        k = 0
        lo = head
        hi = head
        while steps < max_steps:
            b = tape[head]
            nx = N[st, b]
            tape[head] = W[st, b]
            head += M[st, b]
            steps += 1
            if head < lo:
                lo = head
            if head > hi:
                hi = head
            if head < 1 or head >= size - 1:
                return steps, -2, k, tape, lo, hi
            if snap_every > 0 and steps % snap_every == 0 and k < n_snaps:
                snaps[k, :] = tape
                heads[k] = head
                sbounds[k, 0] = lo
                sbounds[k, 1] = hi
                k += 1
            if nx < 0:
                return steps, 1, k, tape, lo, hi
            st = nx
        return steps, 0, k, tape, lo, hi

    return go


_GO = None


def run_fast(tm: TM, max_steps: int, size: int = 1 << 16, snap_every: int = 0, n_snaps: int = 0):
    """Run a 2-symbol machine from a blank tape for at most ``max_steps``.  Returns a dict: steps, halted, ones,
    the final tape (trimmed), and ``n_snaps`` snapshots of the tape every ``snap_every`` steps (rows of the
    space-time picture) with the head's position and the visited range at each."""
    global _GO
    if _GO is None:
        _GO = _numba_run()
    W, M, N = _arrays(tm)
    snaps = np.zeros((max(n_snaps, 1), size), np.int8)
    heads = np.zeros(max(n_snaps, 1), np.int64)
    sb = np.zeros((max(n_snaps, 1), 2), np.int64)
    steps, status, k, tape, lo, hi = _GO(W, M, N, size, max_steps, snap_every, n_snaps, snaps, heads, sb)
    if status == -2:
        raise RuntimeError("the head ran off the simulated tape: give a larger size")
    return {"steps": int(steps), "halted": status == 1, "ones": int(tape.sum()), "tape": tape[lo:hi + 1].copy(),
            "lo": int(lo - size // 2), "hi": int(hi - size // 2),
            "snaps": snaps[:k] if n_snaps else None, "snap_heads": heads[:k] - size // 2,
            "snap_bounds": sb[:k] - size // 2}


# ---------------------------------------------------------------------------
# The busy-beaver champions
# ---------------------------------------------------------------------------
CHAMPIONS = {  # n: (machine, steps S(n), ones Sigma(n) of this machine, who, year)
    1: ("1RZ---", 1, 1, "trivial", 1962),
    2: ("1RB1LB_1LA1RZ", 6, 4, "Rad\\'o", 1962),
    3: ("1RB1RZ_1LB0RC_1LC1LA", 21, 5, "Lin and Rad\\'o", 1965),
    4: ("1RB1LB_1LA0LC_1RZ1LD_1RD0RA", 107, 13, "Brady", 1983),
    5: ("1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA", 47_176_870, 4098, "Marxen and Buntrock", 1990),
}
