"""Part 25's instrument: undecidable problems, run as far as they can be run.

    pcp_solve(dominoes, max_len, first=None)      bounded breadth-first search for a Post correspondence match
    tm_to_mpcp(tm, w)                             Sipser's construction: a TM and input -> modified PCP dominoes
    wang_tile(tiles, n, m, ...)                   backtracking: can these Wang tiles fill an n x m rectangle?
    pebble_quine(), python_quine()                programs that print their own source
    fractran(program, n, steps)                   Conway's FRACTRAN; PRIMEGAME produces the primes
    collatz(n)                                    trajectory length and peak
    complexity_proxies(data)                      zlib, bz2 and lzma sizes: upper bounds on Kolmogorov complexity
    pell(D)                                       the least solution of x^2 - D y^2 = 1, by continued fractions
    hat_polygon()                                 the 2023 aperiodic monotile, as 13 vertices on the kite grid

Each is checked in tests/test_cs25_computability.py.
"""

from __future__ import annotations

import bz2
import lzma
import math
import zlib
from collections import deque
from fractions import Fraction


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value

# --------------------------------------------------------------------------------------------------- PCP


def pcp_search(dominoes, max_len=12, first=None, max_nodes=2_000_000):
    """Shortest nonempty match, or an explicit bounded-search status.

    Nodes count dequeued residual states, including the initial empty root.
    Exhaustion of the reachable finite residual graph proves no match; a depth
    or node cutoff does not. ``first`` specifies modified PCP, not ordinary PCP.
    Residual-state merging preserves shortest distance by breadth-first order.
    """
    _integer(max_len, "max_len"); _integer(max_nodes, "max_nodes")
    dominoes = list(dominoes)
    if any(not isinstance(d, (tuple, list)) or len(d) != 2 or
           any(not isinstance(w, str) or not w for w in d) for d in dominoes):
        raise ValueError("dominoes must be pairs of nonempty strings")
    if first is not None:
        _integer(first, "first")
        if first >= len(dominoes): raise ValueError("first is outside the domino set")
    q = deque([(None, (), 0)])
    seen, nodes, depth_cut = set(), 0, False
    while q:
        if nodes == max_nodes:
            return dict(match=None, nodes=nodes, status="node-limit", reached=len(seen))
        over, seq, depth = q.popleft(); nodes += 1
        if depth == max_len:
            depth_cut = True
            continue
        starts = [first] if over is None and first is not None else range(len(dominoes))
        for i in starts:
            t, b = dominoes[i]
            if over is not None:
                side, s = over
                t, b = (s + t, b) if side == "t" else (t, s + b)
            if t == b:
                return dict(match=list(seq + (i,)), nodes=nodes, status="matched", reached=len(seen))
            if t.startswith(b): new = ("t", t[len(b):])
            elif b.startswith(t): new = ("b", b[len(t):])
            else: continue
            if new not in seen:
                seen.add(new); q.append((new, seq + (i,), depth + 1))
    return dict(match=None, nodes=nodes, status="depth-limit" if depth_cut else "exhausted", reached=len(seen))


def pcp_solve(dominoes, max_len=12, first=None, max_nodes=2_000_000):
    """Compatibility tuple; use pcp_search to distinguish exhaustion and cutoff."""
    r = pcp_search(dominoes, max_len, first, max_nodes)
    return r["match"], r["nodes"]


def _tm_domain(rules, start, accept, w, alphabet):
    symbols = set(alphabet) | {"_"}
    states = {start, accept} | {q for q, _ in rules} | {r for r, _, _ in rules.values()}
    if (not isinstance(w, str) or not w or not set(w) <= symbols or
        any(not isinstance(c, str) or len(c) != 1 or c == "#" for c in states | symbols) or
        states & symbols):
        raise ValueError("nonempty input; disjoint one-character states/tape alphabet; # reserved")
    if any(q == accept or a not in symbols or b not in symbols or mv not in ("L", "R")
           for (q, a), (r, b, mv) in rules.items()):
        raise ValueError("invalid transition or outgoing accept transition")


def tm_to_mpcp(rules, start, accept, w, alphabet):
    """Sipser's construction (Theorem 5.15) for a one-tape TM given as {(state, sym): (new_state, write, move)}.
    States and symbols are single characters; '#' separates configurations and '_' is the blank. The first domino
    is forced. A match spells out the accepting computation history. This
    didactic model REJECTS a left move off cell zero; it never clamps the head.
    The input is nonempty, states and tape symbols are disjoint, and missing
    transitions reject. A separate standard reduction converts MPCP to PCP.
    """
    _tm_domain(rules, start, accept, w, alphabet)
    tape = set(alphabet) | {"_"}
    D = [("#", "#" + start + w + "#")]
    for (q, a), (r, b, mv) in rules.items():
        if mv == "R":
            D.append((q + a, b + r))
        else:
            for c in sorted(tape):
                D.append((c + q + a, r + c + b))
    for a in sorted(tape):
        D.append((a, a))
    D.append(("#", "#"))
    D.append(("#", "_#"))
    for a in sorted(tape):
        D.append((a + accept, accept))
        D.append((accept + a, accept))
    D.append((accept + "##", "#"))
    return D


def run_tm_trace(rules, start, accept, w, max_steps=100):
    """Full configurations and status for the restricted model of tm_to_mpcp."""
    _integer(max_steps, "max_steps")
    alphabet = set(w) | {a for _, a in rules} | {b for _, b, _ in rules.values()}
    _tm_domain(rules, start, accept, w, alphabet)
    tape, head, q = list(w) or ["_"], 0, start
    hist, configs, steps = [], [], 0
    while True:
        hist.append(("".join(tape[:head]) + q + "".join(tape[head:])).rstrip("_"))
        configs.append(dict(state=q, head=head, tape="".join(tape)))
        if q == accept: status = "accepted"; break
        if (q, tape[head]) not in rules: status = "rejected-missing-rule"; break
        if steps == max_steps: status = "step-limit"; break
        r, b, mv = rules[(q, tape[head])]
        if mv == "L" and head == 0: status = "rejected-left-boundary"; break
        tape[head] = b
        q = r; steps += 1
        if mv == "R":
            head += 1
            if head == len(tape):
                tape.append("_")
        else:
            head -= 1
    return dict(history="#" + "#".join(hist) + "#", configurations=configs, steps=steps, status=status)


def run_tm_history(rules, start, accept, w, max_steps=100):
    """Compatibility string; truncation/rejection status is in run_tm_trace."""
    return run_tm_trace(rules, start, accept, w, max_steps)["history"]


# --------------------------------------------------------------------------------------------------- Wang tiles


def wang_tile(tiles, n, m, limit=5_000_000, periodic=False):
    """Fill an n-row by m-column rectangle with Wang tiles (N, E, S, W colours; neighbours must match on shared
    edges), row by row with backtracking. With ``periodic``, also match left/right and top/bottom edges (a torus,
    which tiles the plane periodically). Returns (grid of tile indices or None, nodes tried, complete): complete is
    True when the search finished, so None then means no tiling exists."""
    _integer(n, "rows", 1); _integer(m, "columns", 1); _integer(limit, "limit")
    if type(periodic) is not bool: raise ValueError("periodic must be bool")
    tiles = list(tiles)
    if any(len(t) != 4 or any(type(c) is not int or c < 0 for c in t) for t in tiles):
        raise ValueError("tiles must have four nonnegative integer colors")
    grid = [[None] * m for _ in range(n)]
    nodes = [0]
    cutoff = [False]

    def ok(r, c, t):
        N, E, S, W = tiles[t]
        if c > 0 and tiles[grid[r][c - 1]][1] != W:
            return False
        if r > 0 and tiles[grid[r - 1][c]][2] != N:
            return False
        if periodic:
            if c == m - 1 and (W if m == 1 else tiles[grid[r][0]][3]) != E:
                return False
            if r == n - 1 and (N if n == 1 else tiles[grid[0][c]][0]) != S:
                return False
        return True

    def go(k):
        if k == n * m:
            return True
        r, c = divmod(k, m)
        for t in range(len(tiles)):
            if nodes[0] == limit:
                cutoff[0] = True
                return False
            nodes[0] += 1
            if ok(r, c, t):
                grid[r][c] = t
                if go(k + 1):
                    return True
                grid[r][c] = None
                if cutoff[0]: return False
        return False
    found = go(0)
    return (grid if found else None), nodes[0], not cutoff[0]


# Jeandel and Rao (2015): 11 tiles in 5 colours (0-4), the smallest aperiodic set. Each tile is (N, E, S, W).
JEANDEL_RAO_ENWS = [(2, 4, 2, 1), (2, 2, 2, 0), (1, 1, 3, 1), (1, 2, 3, 2), (3, 1, 3, 3), (0, 1, 3, 1), (0, 0, 0, 1),
                    (3, 1, 0, 2), (0, 2, 1, 2), (1, 2, 1, 4), (3, 3, 1, 2)]     # as in Labbe's slabbe package: E, N, W, S
JEANDEL_RAO = [(t[1], t[0], t[3], t[2]) for t in JEANDEL_RAO_ENWS]


# --------------------------------------------------------------------------------------------------- quines


def python_quine() -> str:
    return "s = 's = %r\\nprint(s %% s)'\nprint(s % s)\n"


PEBBLE_HEAD = """// A quine in the Pebble language: it prints its own source, character for character.
var d: [NNNN]int;
fn printnum(n: int) {
    var digits: [12]char;
    var k: int = 0;
    if n == 0 { putc('0'); return; }
    while n > 0 { digits[k] = '0' + n % 10; n = n / 10; k = k + 1; }
    while k > 0 { k = k - 1; putc(digits[k]); }
}
fn main() {
"""
PEBBLE_TAIL = """    var i: int = 0;
    while d[i] != 64 { putc(d[i]); i = i + 1; }
    var k: int = 0;
    while k < NNNN {
        putc(' '); putc(' '); putc(' '); putc(' '); putc('d'); putc('[');
        printnum(k);
        putc(']'); putc(' '); putc('='); putc(' ');
        printnum(d[k]);
        putc(';'); putc(10);
        k = k + 1;
    }
    i = i + 1;
    while i < NNNN { putc(d[i]); i = i + 1; }
}
"""


def pebble_quine() -> str:
    """The template is HEAD + '@' + TAIL; the program is HEAD + one assignment per template character + TAIL. The
    tail prints the head from the data, then the assignments, then the tail."""
    n = len(PEBBLE_HEAD) + 1 + len(PEBBLE_TAIL)
    while True:
        head = PEBBLE_HEAD.replace("NNNN", str(n))
        tail = PEBBLE_TAIL.replace("NNNN", str(n))
        tmpl = head + "@" + tail
        if len(tmpl) == n:
            break
        n = len(tmpl)
    assert "@" not in head + tail
    body = "".join(f"    d[{k}] = {ord(ch)};\n" for k, ch in enumerate(tmpl))
    return head + body + tail


def pebble_backward_quine() -> str:
    """Exercise 5: reconstruct the source in a bounded buffer, then reverse it."""
    head = PEBBLE_HEAD.replace("// A quine in the Pebble language: it prints its own source, character for character.",
                              "// This Pebble program prints its own source bytes backwards.")
    head = head.replace("fn printnum", "var out: [32768]int;\nvar used: int = 0;\n"
                        "fn emit(c: int) { out[used] = c; used = used + 1; }\nfn printnum")
    head = head.replace("putc(", "emit(")
    tail = PEBBLE_TAIL.replace("putc(", "emit(")
    tail = tail.rsplit("}", 1)[0] + "    while used > 0 { used = used - 1; putc(out[used]); }\n}\n"
    n = len(head) + 1 + len(tail)
    while True:
        h, t = head.replace("NNNN", str(n)), tail.replace("NNNN", str(n))
        template = h + "@" + t
        if len(template) == n: break
        n = len(template)
    assert "@" not in h + t
    src = h + "".join(f"    d[{i}] = {ord(c)};\n" for i, c in enumerate(template)) + t
    assert src.isascii() and len(src) <= 32768
    return src


# --------------------------------------------------------------------------------------------------- FRACTRAN, Collatz


PRIMEGAME = [Fraction(17, 91), Fraction(78, 85), Fraction(19, 51), Fraction(23, 38), Fraction(29, 33),
             Fraction(77, 29), Fraction(95, 23), Fraction(77, 19), Fraction(1, 17), Fraction(11, 13),
             Fraction(13, 11), Fraction(15, 2), Fraction(1, 7), Fraction(55, 1)]


def fractran_run(program, n, steps, *, trace=None):
    """First-applicable positive rational rewrite; outputs exclude initial n.

    Optional mutable trace receives every selected instruction index. A budget
    exhaustion is distinct from absence of an applicable instruction.
    """
    _integer(n, "start", 1); _integer(steps, "steps")
    program = [Fraction(f) for f in program]
    if any(f <= 0 for f in program): raise ValueError("instructions must be positive rationals")
    out, executed = [], 0
    for s in range(1, steps + 1):
        for i, f in enumerate(program):
            if (n * f.numerator) % f.denominator == 0:
                n = n * f.numerator // f.denominator
                if trace is not None: trace.append(i)
                executed = s
                break
        else:
            return dict(outputs=out, steps=executed, final=n, status="halted")
        if n & (n - 1) == 0:
            out.append((s, n.bit_length() - 1))
    return dict(outputs=out, steps=executed, final=n, status="step-limit")


def fractran(program, n, steps):
    return fractran_run(program, n, steps)["outputs"]


def collatz(n, max_steps=10_000_000):
    """Bounded positive-integer trajectory; no general termination is assumed."""
    _integer(n, "start", 1); _integer(max_steps, "max_steps")
    steps, peak = 0, n
    while n != 1:
        if steps == max_steps: raise TimeoutError("Collatz step budget exhausted")
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        peak = max(peak, n)
        steps += 1
    return steps, peak


# --------------------------------------------------------------------------------------------------- complexity


def complexity_proxies(data: bytes) -> dict:
    """Container byte lengths; plain-C bounds need bits and fixed decoding costs."""
    if not isinstance(data, bytes): raise ValueError("data must be bytes")
    return {"raw": len(data), "zlib": len(zlib.compress(data, 9)), "bz2": len(bz2.compress(data, 9)),
            "lzma": len(lzma.compress(data, preset=9 | lzma.PRESET_EXTREME))}


def pi_digits(n):
    """n digits INCLUDING leading 3, by integer Machin with guard digits.

    The producer independently certifies the entire requested prefix; this
    routine's fixed guard digits alone are not a rounding certificate.
    """
    _integer(n, "digits")
    if n == 0: return ""
    def arctan_inv(x, unity):
        s = term = unity // x
        x2, k, sign = x * x, 3, -1
        while term:
            term //= x2
            s += sign * (term // k)
            sign, k = -sign, k + 2
        return s
    unity = 10 ** (n + 10)
    pi = 4 * (4 * arctan_inv(5, unity) - arctan_inv(239, unity))
    import sys
    old = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)
    try:
        return str(pi)[:n]
    finally:
        sys.set_int_max_str_digits(old)


def thue_morse(n):
    _integer(n, "length")
    return "".join(str(bin(i).count("1") % 2) for i in range(n))


# --------------------------------------------------------------------------------------------------- Pell


def pell(D, *, certificate=None):
    """Least solution with y>0 for positive nonsquare D; squares return None.

    Minimality uses the standard theorem that the least positive Pell solution
    is a convergent of sqrt(D). Optional certificate retains every convergent.
    """
    _integer(D, "D", 1)
    a0 = math.isqrt(D)
    if a0 * a0 == D:
        return None
    m, d, a = 0, 1, a0
    p_prev, p = 1, a0
    q_prev, q = 0, 1
    convergents = [(m, d, a, p, q)]
    while p * p - D * q * q != 1:
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d
        p_prev, p = p, a * p + p_prev
        q_prev, q = q, a * q + q_prev
        convergents.append((m, d, a, p, q))
    if certificate is not None: certificate.update(D=D, convergents=convergents)
    return p, q


# --------------------------------------------------------------------------------------------------- the hat


def hat_polygon():
    """The 'hat' (Smith, Myers, Kaplan and Goodman-Strauss, 2023), Tile(1, sqrt 3): 13 vertices on the hexagonal
    lattice (as in Kaplan's hatviz), edges of length 1, sqrt 3 and one of 2; a union of 8 kites of area sqrt 3."""
    import numpy as np
    H = [(0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1), (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2)]
    return np.array([(x + 0.5 * y, math.sqrt(3) / 2 * y) for x, y in H], float)


def shoelace(P):
    if len(P) < 3 or any(len(p) != 2 or any(not math.isfinite(float(c)) for c in p) for p in P):
        raise ValueError("at least three finite plane vertices required")
    s = 0.0
    for (x1, y1), (x2, y2) in zip(P, list(P[1:]) + [P[0]]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2
