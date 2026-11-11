"""The machines of Part 1: Turing machines programmed by hand, a single-tape simulation of a multitape machine, a
small universal machine of our own, Minsky's counter machines, and two cellular automata.

Every machine here is checked in ``tests/test_cs1_machines.py``: the palindrome machines against Python's ``s ==
s[::-1]``, the single-tape simulation against the multitape run it simulates, the universal machine against the
machines it simulates, the two-counter compilation against the three-counter program.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from explainer.cs.turing import BLANK, HALT, TM, run

# ---------------------------------------------------------------------------
# Programs written by hand
# ---------------------------------------------------------------------------
# unary addition: 111+11 -> 11111.  Turn the + into a 1, run to the end, erase the last 1.
UNARY_ADD = TM([
    ("A", "1", "1", "R", "A"),
    ("A", "+", "1", "R", "B"),
    ("B", "1", "1", "R", "B"),
    ("B", "_", "_", "L", "C"),
    ("C", "1", "_", "S", "H"),
], start="A", name="unary addition")

# palindromes on one tape: cross off the first symbol, run to the far end, check and cross off the last, run back.
PALINDROME = TM([
    ("start", "_", "_", "S", "accept"),
    ("start", "0", "_", "R", "have0"),
    ("start", "1", "_", "R", "have1"),
    ("have0", "0", "0", "R", "have0"),
    ("have0", "1", "1", "R", "have0"),
    ("have0", "_", "_", "L", "want0"),
    ("have1", "0", "0", "R", "have1"),
    ("have1", "1", "1", "R", "have1"),
    ("have1", "_", "_", "L", "want1"),
    ("want0", "0", "_", "L", "back"),
    ("want0", "1", "1", "S", "reject"),
    ("want0", "_", "_", "S", "accept"),
    ("want1", "1", "_", "L", "back"),
    ("want1", "0", "0", "S", "reject"),
    ("want1", "_", "_", "S", "accept"),
    ("back", "0", "0", "L", "back"),
    ("back", "1", "1", "L", "back"),
    ("back", "_", "_", "R", "start"),
], start="start", name="palindromes, one tape")

# palindromes on two tapes: copy the input to tape 2, rewind tape 1, compare forwards against backwards.
PALINDROME2 = TM([
    ("copy", ("0", "_"), ("0", "0"), ("R", "R"), "copy"),
    ("copy", ("1", "_"), ("1", "1"), ("R", "R"), "copy"),
    ("copy", ("_", "_"), ("_", "_"), ("L", "S"), "rewind"),
    ("rewind", ("0", "*"), ("=", "="), ("L", "S"), "rewind"),
    ("rewind", ("1", "*"), ("=", "="), ("L", "S"), "rewind"),
    ("rewind", ("_", "*"), ("=", "="), ("R", "L"), "compare"),
    ("compare", ("0", "0"), ("=", "="), ("R", "L"), "compare"),
    ("compare", ("1", "1"), ("=", "="), ("R", "L"), "compare"),
    ("compare", ("_", "_"), ("=", "="), ("S", "S"), "accept"),
    ("compare", ("0", "1"), ("=", "="), ("S", "S"), "reject"),
    ("compare", ("1", "0"), ("=", "="), ("S", "S"), "reject"),
], start="copy", tapes=2, name="palindromes, two tapes")


# ---------------------------------------------------------------------------
# One tape simulating many (the robustness theorem, Sipser's construction)
# ---------------------------------------------------------------------------
def single_tape_cost(tm: TM, inputs, max_steps=10**6) -> dict:
    """Run a k-tape machine and count the head moves of the single-tape machine that simulates it.

    The single tape holds the k tapes side by side, ``#w1#w2#...#wk#``, each head marked on its symbol.  Each simulated
    step costs one sweep right across the whole tape (to read the k marked symbols) and one sweep back (to write and
    move the marks); a virtual head stepping onto a ``#`` first shifts everything to its right one cell (a sweep to
    the end and back).  Returns the multitape steps, the single-tape moves, and the moves per step."""
    res = run(tm, inputs, max_steps=max_steps, record=True)
    k = tm.tapes
    seg = [max(1, len(s)) if isinstance(s, str) else 1 for s in (inputs if not isinstance(inputs, str) else (inputs,))]
    seg += [1] * (k - len(seg))
    span = [[0, seg[t] - 1] for t in range(k)]  # the cells region t occupies, in its own coordinates
    moves = 0
    per_step = []
    for i in range(len(res.history) - 1):
        total = sum(b - a + 2 for a, b in span) + 1  # the regions and their # separators
        cost = 2 * total
        nxt = res.history[i + 1][1]
        for t in range(k):
            h = nxt[t]
            if h > span[t][1]:  # grow region t to the right: shift what follows it
                right = sum(b - a + 2 for a, b in span[t + 1:])
                cost += 2 * (right + 1)
                span[t][1] = h
            if h < span[t][0]:
                right = sum(b - a + 2 for a, b in span[t:])
                cost += 2 * (right + 1)
                span[t][0] = h
        moves += cost
        per_step.append(cost)
    return {"steps": res.steps, "moves": moves, "per_step": per_step, "halted": res.halted, "state": res.state}


# ---------------------------------------------------------------------------
# A universal machine
# ---------------------------------------------------------------------------
def encode(tm: TM) -> str:
    """<M>: a 2-symbol, 1-tape machine as a string.  States are numbered in unary (the start state is 1, halting is
    the empty string); each rule is ``state|read|write|move|next#`` with symbols 0 and 1 (0 is the blank)."""
    order = [s for s in tm.states if s not in HALT]
    order.remove(tm.start)
    order.insert(0, tm.start)
    num = {s: "1" * (i + 1) for i, s in enumerate(order)} | {h: "" for h in HALT}
    out = []
    for st in order:
        for st_, rd, wr, mv, nx in tm.rules:
            if st_ == st:
                r = "0" if rd[0] == BLANK else "1"
                w = "0" if wr[0] == BLANK else "1"
                out.append(f"{num[st]}|{r}|{w}|{mv[0]}|{num[nx]}#")
    return "".join(out)


# The universal machine U: three tapes.  Tape 1 holds ^<M>$ (read only), tape 2 is M's tape, tape 3 holds M's state in
# unary after a ^.  Each of M's steps: find the rule whose state matches tape 3 and whose read symbol matches tape 2
# (scanning the rules left to right), apply its write and move to tape 2, copy its next state onto tape 3, rewind.
_ = "*"
UTM = TM([
    # is M's state empty (it halted)?  otherwise step tape 1 onto the first rule
    ("check", (_, _, "^"), ("=", "=", "="), ("S", "S", "R"), "check2"),
    ("check2", (_, _, "_"), ("=", "=", "="), ("S", "S", "S"), "H"),
    ("check2", (_, _, "1"), ("=", "=", "="), ("R", "S", "S"), "match"),
    # compare the rule's state (unary) with tape 3's, one 1 at a time
    ("match", ("1", _, "1"), ("=", "=", "="), ("R", "S", "R"), "match"),
    ("match", ("|", _, "_"), ("=", "=", "="), ("R", "S", "S"), "symbol"),
    ("match", ("$", _, _), ("=", "=", "="), ("S", "S", "S"), "H"),
    ("match", (_, _, _), ("=", "=", "="), ("S", "S", "S"), "skip"),
    # the state matches: does the read symbol match what M's head sees?
    ("symbol", ("0", "_", _), ("=", "=", "="), ("R", "S", "S"), "sep1"),
    ("symbol", ("1", "1", _), ("=", "=", "="), ("R", "S", "S"), "sep1"),
    ("symbol", (_, _, _), ("=", "=", "="), ("S", "S", "S"), "skip"),
    # not this rule: skip past its #, rewind tape 3 to M's state, try the next
    ("skip", ("#", _, _), ("=", "=", "="), ("R", "S", "S"), "rewind3"),
    ("skip", (_, _, _), ("=", "=", "="), ("R", "S", "S"), "skip"),
    ("rewind3", (_, _, "^"), ("=", "=", "="), ("S", "S", "R"), "match"),
    ("rewind3", (_, _, _), ("=", "=", "="), ("S", "S", "L"), "rewind3"),
    # apply the rule: write, move, then copy the next state onto tape 3
    ("sep1", ("|", _, _), ("=", "=", "="), ("R", "S", "S"), "write"),
    ("write", ("0", _, _), ("=", "_", "="), ("R", "S", "S"), "sep2"),
    ("write", ("1", _, _), ("=", "1", "="), ("R", "S", "S"), "sep2"),
    ("sep2", ("|", _, _), ("=", "=", "="), ("R", "S", "S"), "move"),
    ("move", ("L", _, _), ("=", "=", "="), ("R", "L", "S"), "sep3"),
    ("move", ("R", _, _), ("=", "=", "="), ("R", "R", "S"), "sep3"),
    ("sep3", ("|", _, _), ("=", "=", "="), ("R", "S", "S"), "erase"),
    ("erase", (_, _, "^"), ("=", "=", "="), ("S", "S", "R"), "copy"),
    ("erase", (_, _, _), ("=", "=", "_"), ("S", "S", "L"), "erase"),
    ("copy", ("1", _, _), ("=", "=", "1"), ("R", "S", "R"), "copy"),
    ("copy", ("#", _, _), ("=", "=", "="), ("L", "S", "S"), "rewind"),
    # back to the start of tape 1 and tape 3
    ("rewind", ("^", _, "^"), ("=", "=", "="), ("S", "S", "S"), "check"),
    ("rewind", ("^", _, _), ("=", "=", "="), ("S", "S", "L"), "rewind"),
    ("rewind", (_, _, "^"), ("=", "=", "="), ("L", "S", "S"), "rewind"),
    ("rewind", (_, _, _), ("=", "=", "="), ("L", "S", "L"), "rewind"),
], start="check", tapes=3, name="U")


def run_universal(tm: TM, tape: str = "", max_steps: int = 10**7, record: bool = False):
    """U running <M> on ``tape``: returns U's result; M's tape is U's tape 2."""
    return run(UTM, ("^" + encode(tm) + "$", tape, "^1"), max_steps=max_steps, record=record)


# ---------------------------------------------------------------------------
# Counter machines (Minsky 1961, 1967): a few bowls of pebbles and a numbered list of instructions
# ---------------------------------------------------------------------------
@dataclass
class CM:
    """A program: a list of ('inc', r, next) | ('dec', r, next if r>0, next if r=0) | ('halt',)."""
    prog: list
    counters: int

    def run(self, regs, max_steps=10**8, record=False):
        regs = list(regs) + [0] * (self.counters - len(regs))
        pc, steps, hist = 0, 0, []
        while steps < max_steps:
            if record:
                hist.append((pc, tuple(regs)))
            ins = self.prog[pc]
            if ins[0] == "halt":
                return {"regs": regs, "steps": steps, "history": hist}
            if ins[0] == "inc":
                regs[ins[1]] += 1
                pc = ins[2]
            else:
                if regs[ins[1]] > 0:
                    regs[ins[1]] -= 1
                    pc = ins[2]
                else:
                    pc = ins[3]
            steps += 1
        raise RuntimeError("counter machine did not halt")


# r0 := r0 + r1 (r1 emptied) on three counters, then r2 := r0 (r0 emptied): add, and move the sum
ADD3 = CM([("dec", 1, 1, 2), ("inc", 0, 0), ("dec", 0, 3, 4), ("inc", 2, 2), ("halt",)], 3)

PRIMES = (2, 3, 5, 7)


def compile_two_counters(cm: CM) -> CM:
    """Minsky's theorem as a compiler: any k-counter program as a 2-counter one.  Counter A (0) holds the Gödel number
    2^r0 3^r1 5^r2 ...; counter B (1) is scratch.

    inc ri: multiply A by p_i: move A into B, then for each pebble of B put p_i pebbles back in A.
    dec ri: divide A by p_i if it can: take pebbles from A in groups of p_i, one pebble into B per full group.  If A
    empties at a group boundary, A was divisible (r_i > 0): move the quotient back and continue at the instruction's
    "nonzero" exit.  If A runs out mid-group, r_i was 0: put back the partial group, then p_i per pebble of B, and
    continue at the "zero" exit.  An unconditional jump is inc B followed by dec B (both exits the same)."""
    if cm.counters > len(PRIMES):
        raise ValueError("too many counters")
    A, B = 0, 1
    code: list = []  # instructions with symbolic targets (labels)
    labels: dict = {}

    def lab(name):
        labels[name] = len(code)

    def jmp(target, tag):
        code.append(("inc", B, f"{tag}.j"))
        lab(f"{tag}.j")
        code.append(("dec", B, target, target))

    for i, ins in enumerate(cm.prog):
        lab(("ins", i))
        if ins[0] == "halt":
            code.append(("halt",))
            continue
        p = PRIMES[ins[1]]
        t = f"i{i}"
        if ins[0] == "inc":
            lab(f"{t}.m1")
            code.append(("dec", A, f"{t}.m2", f"{t}.b1"))
            lab(f"{t}.m2")
            code.append(("inc", B, f"{t}.m1"))
            lab(f"{t}.b1")
            code.append(("dec", B, f"{t}.b2", ("ins", ins[2])))
            for k in range(p):
                lab(f"{t}.b{k + 2}")
                code.append(("inc", A, f"{t}.b{k + 3}" if k < p - 1 else f"{t}.b1"))
        else:
            nz, z = ("ins", ins[2]), ("ins", ins[3])
            for k in range(p):
                lab(f"{t}.t{k}")
                fail = f"{t}.div" if k == 0 else f"{t}.f{k}"
                code.append(("dec", A, f"{t}.t{k + 1}" if k < p - 1 else f"{t}.put", fail))
            lab(f"{t}.put")
            code.append(("inc", B, f"{t}.t0"))
            lab(f"{t}.div")
            code.append(("dec", B, f"{t}.d2", nz))
            lab(f"{t}.d2")
            code.append(("inc", A, f"{t}.div"))
            for k in range(1, p):
                lab(f"{t}.f{k}")
                for j in range(k):
                    nxt = f"{t}.f{k}.{j + 1}"
                    code.append(("inc", A, nxt))
                    lab(nxt)
                jmp(f"{t}.r", f"{t}.f{k}")
            lab(f"{t}.r")
            code.append(("dec", B, f"{t}.r1", z))
            for k in range(p):
                lab(f"{t}.r{k + 1}")
                code.append(("inc", A, f"{t}.r{k + 2}" if k < p - 1 else f"{t}.r"))

    def res(x):
        return labels[x]

    out = []
    for ins in code:
        if ins[0] == "inc":
            out.append(("inc", ins[1], res(ins[2])))
        elif ins[0] == "dec":
            out.append(("dec", ins[1], res(ins[2]), res(ins[3])))
        else:
            out.append(ins)
    return CM(out, 2)


def godel(regs) -> int:
    v = 1
    for p, r in zip(PRIMES, regs):
        v *= p ** r
    return v


def ungodel(a: int, k: int) -> list[int]:
    out = []
    for p in PRIMES[:k]:
        r = 0
        while a % p == 0:
            a //= p
            r += 1
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# Cellular automata
# ---------------------------------------------------------------------------
def elementary(rule: int, width: int, steps: int, init=None, seed=None) -> np.ndarray:
    """An elementary cellular automaton (Wolfram's numbering) on a ring of ``width`` cells: rows = generations."""
    table = np.array([(rule >> i) & 1 for i in range(8)], np.int8)
    if init is None:
        row = np.zeros(width, np.int8)
        if seed is None:
            row[-1] = 1
        else:
            row = np.random.default_rng(seed).integers(0, 2, width).astype(np.int8)
    else:
        row = np.asarray(init, np.int8)
    out = np.zeros((steps, width), np.int8)
    for t in range(steps):
        out[t] = row
        idx = 4 * np.roll(row, 1) + 2 * row + np.roll(row, -1)
        row = table[idx]
    return out


GOSPER_GUN = [(5, 1), (5, 2), (6, 1), (6, 2), (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (9, 13), (3, 14),
              (9, 14), (6, 15), (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18), (3, 21), (4, 21), (5, 21),
              (3, 22), (4, 22), (5, 22), (2, 23), (6, 23), (1, 25), (2, 25), (6, 25), (7, 25), (3, 35), (4, 35),
              (3, 36), (4, 36)]


def life(h: int, w: int, steps: int, cells=GOSPER_GUN) -> np.ndarray:
    """Conway's Game of Life on an h x w grid with dead borders: frames[t] is generation t."""
    g = np.zeros((h, w), np.int8)
    for r, c in cells:
        g[r, c] = 1
    frames = np.zeros((steps, h, w), np.int8)
    for t in range(steps):
        frames[t] = g
        n = sum(np.roll(np.roll(g, dr, 0), dc, 1) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc)
        g = ((n == 3) | ((g == 1) & (n == 2))).astype(np.int8)
        g[0, :] = g[-1, :] = 0
        g[:, 0] = g[:, -1] = 0
    return frames
