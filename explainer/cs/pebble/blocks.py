"""Arithmetic blocks for Pebble, as netlists (built on screen in Part 4, "Arithmetic").

Every builder returns a ``Circuit`` (``hdl.py``) with inputs ``a``, ``b`` (n bits, least significant first) and,
for adders, ``cin``; outputs ``s`` and ``cout`` (adders), ``p`` (multipliers), or ``y`` and flags (the ALU).

    ripple_adder(n)                    n full adders in a chain: depth about 2n
    prefix_adder(n, "kogge-stone")     carries by a parallel prefix of (generate, propagate) pairs: depth O(log n)
                 "brent-kung", "sklansky", "ripple"
    carry_select_adder(n, sizes)       blocks computed for both carries, chosen by the real one
    carry_skip_adder(n, k)             ripple blocks with a bypass when a whole block propagates
    array_multiplier(n)                rows of adders: depth O(n)
    tree_multiplier(n, "wallace"|"dadda")   carry-save 3:2 compression of the partial products: depth O(log n)
    alu(n)                             Pebble's ALU: add sub and or xor sll srl sra slt sltu

The carry operator.  For bits i..j define G (the block generates a carry) and P (it propagates one).  Joining a high
block (g, p) to the low block below it (g', p'):

    (g, p) o (g', p') = (g + p g', p p')

is associative, so the carries c_i = G[i-1 .. 0] are the prefix "sums" of the pairs (g_k, p_k), and any parallel
prefix network computes them.  The networks differ in depth, gate count and fan-out (``PREFIX``).
"""

from __future__ import annotations

from .hdl import Circuit

ALU_OPS = ("add", "sub", "and", "or", "xor", "sll", "srl", "sra", "slt", "sltu")


# ---------------------------------------------------------------------------
# one bit
# ---------------------------------------------------------------------------
def half_adder(c: Circuit, a: int, b: int):
    return c.xor(a, b), c.and_(a, b)


def full_adder(c: Circuit, a: int, b: int, cin: int):
    """sum = a xor b xor cin; carry = majority(a, b, cin) = a b + (a xor b) cin."""
    p = c.xor(a, b)
    return c.xor(p, cin), c.or_(c.and_(a, b), c.and_(p, cin))


def mux2(c: Circuit, s: int, a: int, b: int) -> int:
    """s ? b : a."""
    return c.or_(c.and_(c.not_(s), a), c.and_(s, b))


def tree(c: Circuit, op, xs: list) -> int:
    """Combine wires pairwise, level by level: depth log2 of the count, not the count."""
    xs = list(xs)
    while len(xs) > 1:
        xs = [op(xs[i], xs[i + 1]) if i + 1 < len(xs) else xs[i] for i in range(0, len(xs), 2)]
    return xs[0]


def mux2_bus(c: Circuit, s: int, a: list, b: list) -> list:
    ns = c.not_(s)
    return [c.or_(c.and_(ns, x), c.and_(s, y)) for x, y in zip(a, b)]


# ---------------------------------------------------------------------------
# adders
# ---------------------------------------------------------------------------
def _adder_io(name: str, n: int):
    c = Circuit(name)
    a, b = c.input("a", n), c.input("b", n)
    cin = c.input("cin")
    a = [a] if isinstance(a, int) else a
    b = [b] if isinstance(b, int) else b
    return c, a, b, cin


def ripple_chain(c: Circuit, a: list, b: list, cin: int):
    s, carry = [], cin
    for x, y in zip(a, b):
        si, carry = full_adder(c, x, y, carry)
        s.append(si)
    return s, carry


def ripple_adder(n: int) -> Circuit:
    c, a, b, cin = _adder_io(f"{n}-bit ripple-carry adder", n)
    s, cout = ripple_chain(c, a, b, cin)
    c.output("s", s)
    c.output("cout", cout)
    return c


def prefix_levels(n: int, kind: str) -> list[list[tuple[int, int]]]:
    """The combining steps of a parallel prefix network on n positions: each level is a list of (i, j), meaning
    "node i absorbs node j" (j < i), all of one level happening at once.  After the last level node i holds the
    combination of positions i, i-1, ..., 0."""
    levels: list[list[tuple[int, int]]] = []
    if kind == "ripple":
        return [[(i, i - 1)] for i in range(1, n)]
    if kind == "kogge-stone":
        d = 1
        while d < n:
            levels.append([(i, i - d) for i in range(d, n)])
            d *= 2
        return levels
    if kind == "sklansky":
        lv = 0
        while (1 << lv) < n:
            levels.append([(i, ((i >> lv) << lv) - 1) for i in range(n) if (i >> lv) & 1])
            lv += 1
        return levels
    if kind == "brent-kung":
        d = 1
        while d < n:  # up-sweep: a tree of spans 2, 4, 8, ...
            step = [(i, i - d) for i in range(2 * d - 1, n, 2 * d)]
            if step:
                levels.append(step)
            d *= 2
        d //= 2
        while d >= 1:  # down-sweep: fill in the positions between
            step = [(i, i - d) for i in range(3 * d - 1, n, 2 * d)]
            if step:
                levels.append(step)
            d //= 2
        return levels
    raise ValueError(kind)


PREFIX = ("ripple", "brent-kung", "sklansky", "kogge-stone")


def prefix_carries(c: Circuit, g: list, p: list, kind: str) -> list:
    """Group generates G[i..0] for every i, by the chosen prefix network."""
    G, P = list(g), list(p)
    for level in prefix_levels(len(g), kind):
        newG, newP = list(G), list(P)
        for i, j in level:
            newG[i] = c.or_(G[i], c.and_(P[i], G[j]))
            newP[i] = c.and_(P[i], P[j])
        G, P = newG, newP
    return G


def prefix_adder(n: int, kind: str = "kogge-stone") -> Circuit:
    c, a, b, cin = _adder_io(f"{n}-bit {kind} adder", n)
    p = [c.xor(x, y) for x, y in zip(a, b)]
    g = [c.and_(x, y) for x, y in zip(a, b)]
    g[0] = c.or_(g[0], c.and_(p[0], cin))  # fold the carry-in into position 0
    G = prefix_carries(c, g, p, kind)
    carries = [cin] + G[:-1]
    c.output("s", [c.xor(pi, ci) for pi, ci in zip(p, carries)])
    c.output("cout", G[-1])
    return c.pruned()


def carry_select_adder(n: int, sizes: list[int] | None = None) -> Circuit:
    """Each block beyond the first computes its sum twice, for carry-in 0 and 1; the real carry picks one.  Growing
    block sizes (1, 2, 3, ...) balance the ripple inside a block against the chain of selections: depth O(sqrt n)."""
    if sizes is None:
        sizes, k = [], 1
        while sum(sizes) < n:
            sizes.append(min(k, n - sum(sizes)))
            k += 1
    c, a, b, cin = _adder_io(f"{n}-bit carry-select adder", n)
    s, carry, lo = [], cin, 0
    zero, one = c.const(0), c.const(1)
    for k, w in enumerate(sizes):
        aa, bb = a[lo:lo + w], b[lo:lo + w]
        if k == 0:
            blk, carry = ripple_chain(c, aa, bb, carry)
            s += blk
        else:
            s0, c0 = ripple_chain(c, aa, bb, zero)
            s1, c1 = ripple_chain(c, aa, bb, one)
            s += mux2_bus(c, carry, s0, s1)
            carry = c.or_(c0, c.and_(carry, c1))  # c1 >= c0, so this is the multiplexer
        lo += w
    c.output("s", s)
    c.output("cout", carry)
    return c.pruned()


def carry_skip_adder(n: int, k: int = 4) -> Circuit:
    """Ripple blocks of k bits; if every bit of a block propagates, a multiplexer passes the block's carry-in straight
    out (Harris and Harris's carry-skip, or carry-bypass, adder).  The
    longest path through the gates still ripples (so ``depth()`` barely improves), but no input pattern exercises
    it: a false path.  ``settle()`` measures the real delay."""
    c, a, b, cin = _adder_io(f"{n}-bit carry-skip adder", n)
    s, carry = [], cin
    for lo in range(0, n, k):
        aa, bb = a[lo:lo + k], b[lo:lo + k]
        ps = [c.xor(x, y) for x, y in zip(aa, bb)]
        blk, cout = ripple_chain(c, aa, bb, carry)
        s += blk
        P = ps[0]
        for q in ps[1:]:
            P = c.and_(P, q)
        carry = mux2(c, P, cout, carry)  # all propagate: the carry-in passes straight through
    c.output("s", s)
    c.output("cout", carry)
    return c.pruned()


# ---------------------------------------------------------------------------
# multipliers
# ---------------------------------------------------------------------------
def _mult_io(name: str, n: int):
    c = Circuit(name)
    a, b = c.input("a", n), c.input("b", n)
    return c, a, b


def array_multiplier(n: int) -> Circuit:
    """Partial products a_i b_j, added one row at a time by ripple adders: the schoolbook method in gates."""
    c, a, b = _mult_io(f"{n}x{n} array multiplier", n)
    zero = c.const(0)
    acc = [c.and_(a[i], b[0]) for i in range(n)] + [zero]  # running sum, n + 1 bits, aligned at bit 0
    out = [acc[0]]
    acc = acc[1:]
    for j in range(1, n):
        row = [c.and_(a[i], b[j]) for i in range(n)]
        s, cout = ripple_chain(c, acc[:n], row, zero)
        out.append(s[0])
        acc = s[1:] + [cout]
    out += acc
    c.output("p", out[:2 * n])
    return c.pruned()


def dadda_heights(h: int) -> list[int]:
    d = [2]
    while d[-1] < h:
        d.append(d[-1] * 3 // 2)
    return d[:-1]


def tree_multiplier(n: int, kind: str = "wallace", final: str = "kogge-stone") -> Circuit:
    """All n^2 partial-product bits at once, reduced column by column with full adders (3 bits in, 2 out: a sum in
    this column and a carry in the next) until every column holds at most two bits, then one fast adder.
    Wallace (1964) compresses as much as possible at every level; Dadda (1965) only as much as needed, which uses
    fewer gates for the same number of levels.  Returns the circuit; ``c.stages`` is the number of 3:2 levels."""
    c, a, b = _mult_io(f"{n}x{n} {kind} multiplier", n)
    cols: list[list[int]] = [[] for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            cols[i + j].append(c.and_(a[i], b[j]))
    stages = 0
    targets = dadda_heights(max(len(x) for x in cols)) if kind == "dadda" else None
    while max(len(x) for x in cols) > 2:
        stages += 1
        new: list[list[int]] = [[] for _ in range(2 * n + 1)]
        if kind == "wallace":
            for k, col in enumerate(cols):
                i = 0
                while len(col) - i >= 3:
                    s, cy = full_adder(c, col[i], col[i + 1], col[i + 2])
                    new[k].append(s)
                    new[k + 1].append(cy)
                    i += 3
                if len(col) - i == 2:  # Wallace: any pair left over goes through a half adder
                    s, cy = half_adder(c, col[i], col[i + 1])
                    new[k].append(s)
                    new[k + 1].append(cy)
                    i += 2
                new[k].extend(col[i:])
        else:
            d = targets.pop()
            for k in range(len(cols)):
                col = list(cols[k])
                # bits already arriving from the column below count towards this column's height
                while len(col) + len(new[k]) > d:
                    if len(col) + len(new[k]) - d >= 2 and len(col) >= 3:
                        s, cy = full_adder(c, col.pop(), col.pop(), col.pop())
                    else:
                        s, cy = half_adder(c, col.pop(), col.pop())
                    new[k].append(s)
                    new[k + 1].append(cy)
                new[k].extend(col)
        cols = new[:2 * n]
    zero = c.const(0)
    x = [col[0] if len(col) > 0 else zero for col in cols]
    y = [col[1] if len(col) > 1 else zero for col in cols]
    # the final carry-propagate adder
    p = [c.xor(u, v) for u, v in zip(x, y)]
    g = [c.and_(u, v) for u, v in zip(x, y)]
    if final == "ripple":
        carry, s = zero, []
        for u, v in zip(x, y):
            si, carry = full_adder(c, u, v, carry)
            s.append(si)
    else:
        G = prefix_carries(c, g, p, final)
        s = [p[0]] + [c.xor(p[i], G[i - 1]) for i in range(1, 2 * n)]
    c.output("p", s)
    out = c.pruned()
    out.stages = stages
    return out


# ---------------------------------------------------------------------------
# Pebble's ALU
# ---------------------------------------------------------------------------
def shifter(c: Circuit, x: list, s: list, right: int, arith: int) -> list:
    """Logical left, logical right or arithmetic right shift, in log2 n stages of multiplexers.  A right shift is a
    left shift of the bit-reversed word, so one barrel serves both (reverse, shift, reverse)."""
    n = len(x)
    fill = c.and_(arith, x[-1])  # the bit shifted in: 0, or the sign for sra
    nright = c.not_(right)
    cur = [c.or_(c.and_(nright, x[i]), c.and_(right, x[n - 1 - i])) for i in range(n)]
    fillbit = c.and_(right, fill)
    for st, sb in enumerate(s):
        d = 1 << st
        ins = [cur[i - d] if i - d >= 0 else fillbit for i in range(n)]
        cur = [mux2(c, sb, cur[i], ins[i]) for i in range(n)]
    return [c.or_(c.and_(nright, cur[i]), c.and_(right, cur[n - 1 - i])) for i in range(n)]


def alu(n: int = 32, adder: str = "kogge-stone") -> Circuit:
    """Pebble's ALU: ``op`` (4 bits) indexes ``ALU_OPS``.  One adder does add, sub, slt and sltu: subtraction is
    a + not b + 1; slt is the sign of a - b corrected by overflow; sltu is the borrow, not carry-out."""
    c = Circuit(f"{n}-bit ALU")
    a, b = c.input("a", n), c.input("b", n)
    op = c.input("op", 4)
    code = {name: k for k, name in enumerate(ALU_OPS)}

    def is_op(name):
        k = code[name]
        return tree(c, c.and_, [op[i] if (k >> i) & 1 else c.not_(op[i]) for i in range(4)])

    sel = {name: is_op(name) for name in ALU_OPS}
    sub = c.or_(c.or_(sel["sub"], sel["slt"]), sel["sltu"])
    bb = [c.xor(x, sub) for x in b]
    p = [c.xor(x, y) for x, y in zip(a, bb)]
    g = [c.and_(x, y) for x, y in zip(a, bb)]
    g[0] = c.or_(g[0], c.and_(p[0], sub))
    G = prefix_carries(c, g, p, adder)
    carries = [sub] + G[:-1]
    s = [c.xor(pi, ci) for pi, ci in zip(p, carries)]
    cout = G[-1]
    overflow = c.xor(carries[-1], cout)
    lt = c.xor(s[-1], overflow)
    ltu = c.not_(cout)
    k = max(1, (n - 1).bit_length())
    sh = shifter(c, a, b[:k], right=c.or_(sel["srl"], sel["sra"]), arith=sel["sra"])
    res = []
    for i in range(n):
        terms = [
            c.and_(c.or_(sel["add"], sel["sub"]), s[i]),
            c.and_(sel["and"], c.and_(a[i], b[i])),
            c.and_(sel["or"], c.or_(a[i], b[i])),
            c.and_(sel["xor"], c.xor(a[i], b[i])),
            c.and_(c.or_(c.or_(sel["sll"], sel["srl"]), sel["sra"]), sh[i]),
        ]
        if i == 0:
            terms += [c.and_(sel["slt"], lt), c.and_(sel["sltu"], ltu)]
        res.append(tree(c, c.or_, terms))
    zero_flag = tree(c, c.or_, res)
    c.output("y", res)
    c.output("zero", c.not_(zero_flag))
    c.output("overflow", c.and_(c.or_(sel["add"], sel["sub"]), overflow))
    return c.pruned()


def alu_spec(a, b, op, n: int = 32):
    """The reference: what Pebble's emulator computes for each ALU op, on integer arrays (numpy, unsigned)."""
    import numpy as np

    a = np.asarray(a, dtype=np.int64)
    b = np.asarray(b, dtype=np.int64)
    op = np.asarray(op, dtype=np.int64)
    mask = (1 << n) - 1
    sa = np.where(a >> (n - 1) & 1, a - (1 << n), a)
    sb = np.where(b >> (n - 1) & 1, b - (1 << n), b)
    k = (n - 1).bit_length()
    sh = b & ((1 << k) - 1)
    outs = {
        "add": (a + b) & mask, "sub": (a - b) & mask, "and": a & b, "or": a | b, "xor": a ^ b,
        "sll": (a << sh) & mask, "srl": a >> sh, "sra": (sa >> sh) & mask,
        "slt": (sa < sb).astype(np.int64), "sltu": (a < b).astype(np.int64),
    }
    y = np.zeros_like(a)
    for k_, name in enumerate(ALU_OPS):
        y = np.where(op == k_, outs[name], y)
    return y
