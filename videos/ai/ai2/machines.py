"""Turing machines for Part 2: a table of rules, a tape and a head (Turing 1936).

A machine is a dict {(state, symbol read): (symbol to write, move L/R, next state)}; state 'H' halts. Two kinds of
machine appear: a small one that adds one to a binary number (drawn step by step), and the busy-beaver champions,
the machines with n states that run longest before halting from a blank tape: Brady's 4-state machine (107 steps)
and Marxen and Buntrock's 5-state machine (47,176,870 steps; proved the longest by the bbchallenge collaboration in
2024, checked in Coq).
"""

from __future__ import annotations

import numpy as np
from numba import njit


def parse(table: str) -> dict:
    """The standard text form, e.g. '1RB1LB_1LA0LC_1RZ1LD_1RD0RA': per state, the action on reading 0 then 1;
    state Z (or H) halts."""
    rules = {}
    for i, part in enumerate(table.split("_")):
        st = "ABCDEFG"[i]
        for sym in (0, 1):
            a = part[3 * sym: 3 * sym + 3]
            if a[2] in "ZH" or a == "---":
                rules[(st, sym)] = (int(a[0]) if a[0] != "-" else 1, a[1] if a[1] != "-" else "R", "H")
            else:
                rules[(st, sym)] = (int(a[0]), a[1], a[2])
    return rules


BB4 = "1RB1LB_1LA0LC_1RZ1LD_1RD0RA"  # Brady (1983)
BB5 = "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA"  # Marxen & Buntrock (1990)

# binary increment: the head starts on the rightmost digit, state A carries
INCREMENT = {("A", 1): (0, "L", "A"), ("A", 0): (1, "R", "B"), ("A", "_"): (1, "R", "B"),
             ("B", 0): (0, "R", "B"), ("B", 1): (1, "R", "B"), ("B", "_"): ("_", "L", "H")}


def run_small(rules: dict, tape: list, head: int, state="A", max_steps=10_000) -> list[dict]:
    """Every configuration of a run (tape, head, state), for drawing; blanks are '_' or 0."""
    tape = list(tape)
    hist = [{"tape": list(tape), "head": head, "state": state}]
    for _ in range(max_steps):
        if state == "H":
            break
        if head < 0:
            tape.insert(0, "_" if "_" in tape else 0)
            head = 0
        if head >= len(tape):
            tape.append("_" if "_" in tape else 0)
        sym = tape[head]
        write, move, nxt = rules[(state, sym)]
        tape[head] = write
        head += 1 if move == "R" else -1
        state = nxt
        hist.append({"tape": list(tape), "head": head, "state": state})
    return hist


def _encode(rules: dict):
    """(write, move, next) arrays indexed [state, symbol]; next -1 halts."""
    states = sorted({s for s, _ in rules})
    idx = {s: i for i, s in enumerate(states)}
    W = np.zeros((len(states), 2), np.int64)
    M = np.zeros((len(states), 2), np.int64)
    N = np.zeros((len(states), 2), np.int64)
    for (s, b), (w, m, n) in rules.items():
        W[idx[s], b] = w
        M[idx[s], b] = 1 if m == "R" else -1
        N[idx[s], b] = -1 if n == "H" else idx[n]
    return W, M, N


@njit(cache=True)
def _run(W, M, N, size, max_steps, snap_every, snaps, snap_head):
    tape = np.zeros(size, np.int8)
    head = size // 2
    st = 0
    steps = 0
    k = 0
    lo, hi = head, head
    while st >= 0 and steps < max_steps:
        if snap_every > 0 and steps % snap_every == 0 and k < snaps.shape[0]:
            snaps[k] = tape
            snap_head[k] = head
            k += 1
        b = tape[head]
        tape[head] = W[st, b]
        head += M[st, b]
        st = N[st, b]
        steps += 1
        if head < lo:
            lo = head
        if head > hi:
            hi = head
    ones = 0
    for i in range(size):
        ones += tape[i]
    return steps, ones, lo, hi, k, tape


def run_big(table: str, max_steps=10**9, size=40_000, n_snaps=0, snap_every=0):
    W, M, N = _encode(parse(table))
    snaps = np.zeros((max(n_snaps, 1), size), np.int8)
    heads = np.zeros(max(n_snaps, 1), np.int64)
    steps, ones, lo, hi, k, tape = _run(W, M, N, size, max_steps, snap_every, snaps, heads)
    return {"steps": int(steps), "ones": int(ones), "lo": int(lo) - size // 2, "hi": int(hi) - size // 2,
            "snaps": snaps[:k], "heads": heads[:k] - size // 2, "tape": tape}
