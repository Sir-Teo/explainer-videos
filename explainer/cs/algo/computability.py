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

# --------------------------------------------------------------------------------------------------- PCP


def pcp_solve(dominoes, max_len=12, first=None, max_nodes=2_000_000):
    """Breadth-first search over the 'overhang' (what one row has beyond the other). Returns (sequence of indices or
    None, nodes expanded). With ``first``, the match must begin with that domino (the modified problem)."""
    starts = [first] if first is not None else range(len(dominoes))
    q = deque()
    seen = set()
    for i in starts:
        t, b = dominoes[i]
        if t.startswith(b) or b.startswith(t):
            over = ("t", t[len(b):]) if len(t) >= len(b) else ("b", b[len(t):])
            if over[1] == "":
                return [i], 1
            q.append((over, [i]))
            seen.add(over)
    nodes = 0
    while q:
        (side, s), seq = q.popleft()
        nodes += 1
        if nodes > max_nodes or len(seq) >= max_len:
            if nodes > max_nodes:
                break
            continue
        for i, (t, b) in enumerate(dominoes):
            top, bot = (s + t, b) if side == "t" else (t, s + b)
            if top.startswith(bot):
                new = ("t", top[len(bot):])
            elif bot.startswith(top):
                new = ("b", bot[len(top):])
            else:
                continue
            if new[1] == "":
                return seq + [i], nodes
            if new not in seen:
                seen.add(new)
                q.append((new, seq + [i]))
    return None, nodes


def tm_to_mpcp(rules, start, accept, w, alphabet):
    """Sipser's construction (Theorem 5.15) for a one-tape TM given as {(state, sym): (new_state, write, move)}.
    States and symbols are single characters; '#' separates configurations and '_' is the blank. The first domino
    is forced. A match spells out the accepting computation history."""
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


def run_tm_history(rules, start, accept, w, max_steps=100):
    """The computation history the match should spell: '#c0#c1#...#'."""
    tape, head, q = list(w) or ["_"], 0, start
    hist = []
    for _ in range(max_steps):
        hist.append(("".join(tape[:head]) + q + "".join(tape[head:])).rstrip("_"))
        if q == accept:
            break
        a = tape[head]
        r, b, mv = rules[(q, a)]
        tape[head] = b
        q = r
        if mv == "R":
            head += 1
            if head == len(tape):
                tape.append("_")
        else:
            head = max(0, head - 1)
    return "#" + "#".join(hist) + "#"


# --------------------------------------------------------------------------------------------------- Wang tiles


def wang_tile(tiles, n, m, limit=5_000_000, periodic=False):
    """Fill an n-row by m-column rectangle with Wang tiles (N, E, S, W colours; neighbours must match on shared
    edges), row by row with backtracking. With ``periodic``, also match left/right and top/bottom edges (a torus,
    which tiles the plane periodically). Returns (grid of tile indices or None, nodes tried, complete): complete is
    True when the search finished, so None then means no tiling exists."""
    grid = [[None] * m for _ in range(n)]
    nodes = [0]

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
            nodes[0] += 1
            if nodes[0] > limit:
                return False
            if ok(r, c, t):
                grid[r][c] = t
                if go(k + 1):
                    return True
                grid[r][c] = None
        return False
    found = go(0)
    return (grid if found else None), nodes[0], found or nodes[0] <= limit


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
    for _ in range(3):  # N appears in the text, so fix the point where the length is stable
        pass
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


# --------------------------------------------------------------------------------------------------- FRACTRAN, Collatz


PRIMEGAME = [Fraction(17, 91), Fraction(78, 85), Fraction(19, 51), Fraction(23, 38), Fraction(29, 33),
             Fraction(77, 29), Fraction(95, 23), Fraction(77, 19), Fraction(1, 17), Fraction(11, 13),
             Fraction(13, 11), Fraction(15, 2), Fraction(1, 7), Fraction(55, 1)]


def fractran(program, n, steps):
    """Run FRACTRAN from n; yields (step, value) each time the value is a power of two (PRIMEGAME's output)."""
    out = []
    for s in range(1, steps + 1):
        for f in program:
            if (n * f.numerator) % f.denominator == 0:
                n = n * f.numerator // f.denominator
                break
        else:
            return out
        if n & (n - 1) == 0:
            out.append((s, n.bit_length() - 1))
    return out


def collatz(n):
    steps, peak = 0, n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        peak = max(peak, n)
        steps += 1
    return steps, peak


# --------------------------------------------------------------------------------------------------- complexity


def complexity_proxies(data: bytes) -> dict:
    return {"raw": len(data), "zlib": len(zlib.compress(data, 9)), "bz2": len(bz2.compress(data, 9)),
            "lzma": len(lzma.compress(data, preset=9 | lzma.PRESET_EXTREME))}


def pi_digits(n):
    """n decimal digits of pi by Machin's formula with integers."""
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
    return "".join(str(bin(i).count("1") % 2) for i in range(n))


# --------------------------------------------------------------------------------------------------- Pell


def pell(D):
    """Least positive solution of x^2 - D y^2 = 1, from the continued fraction of sqrt(D)."""
    a0 = math.isqrt(D)
    if a0 * a0 == D:
        return None
    m, d, a = 0, 1, a0
    p_prev, p = 1, a0
    q_prev, q = 0, 1
    while p * p - D * q * q != 1:
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d
        p_prev, p = p, a * p + p_prev
        q_prev, q = q, a * q + q_prev
    return p, q


# --------------------------------------------------------------------------------------------------- the hat


def hat_polygon():
    """The 'hat' (Smith, Myers, Kaplan and Goodman-Strauss, 2023), Tile(1, sqrt 3): 13 vertices on the hexagonal
    lattice (as in Kaplan's hatviz), edges of length 1, sqrt 3 and one of 2; a union of 8 kites of area sqrt 3."""
    import numpy as np
    H = [(0, 0), (-1, -1), (0, -2), (2, -2), (2, -1), (4, -2), (5, -1), (4, 0), (3, 0), (2, 2), (0, 3), (0, 2), (-1, 2)]
    return np.array([(x + 0.5 * y, math.sqrt(3) / 2 * y) for x, y in H], float)


def shoelace(P):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(P, list(P[1:]) + [P[0]]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2
