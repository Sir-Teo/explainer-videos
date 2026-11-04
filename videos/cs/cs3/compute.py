"""Precompute everything numerical in Part 3 of *Computer Science, Built* ("Logic from Switches").

    python -m videos.cs.cs3.compute              # everything missing (about a minute)
    python -m videos.cs.cs3.compute --force bdd

Results are cached in ``.cache/cs3/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every circuit here is
built as a netlist in ``explainer/cs/pebble/hdl.py`` and checked against its specification on every input.

Items:
    cmos       the CMOS inverter's transfer curve (square-law transistors, solved point by point): the switching
               threshold, the gain, the noise margins
    post       the five properties of Post's lattice for each of the 16 two-input gates; which gate sets are complete
    nandmin    the fewest NAND gates that compute each of the 16 two-input functions, by exhaustive search
    kmap       a four-variable function: its prime implicants (Quine-McCluskey) and a minimal cover
    parity     the DNF of parity: 2^(n-1) terms, against a tree of n - 1 XORs
    bdd        reduced ordered BDDs of x1 x2 + x3 x4 + ... under a good and a bad variable order: their sizes
    counting   Shannon's counting argument: functions of n inputs against circuits of s gates, and the size most
               functions need
    glitch     a static hazard: f = a b + (not a) c with unit gate delays, every time step, before and after the fix
    blocks     the blocks Pebble needs (comparator, parity tree, priority encoder, barrel shifter, multiplexer,
               decoder), built, verified exhaustively, and counted: gates, NANDs, depth
"""

from __future__ import annotations

import itertools
import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.pebble.hdl import Circuit, exhaustive, unpack

CACHE = Cache("cs3")
load = CACHE.load


# ---------------------------------------------------------------------------
# the CMOS inverter
# ---------------------------------------------------------------------------
def _ids(vgs, vds, vt=0.3, k=1.0, lam=0.06):
    if vgs <= vt:
        return 0.0
    ov = vgs - vt
    if vds < ov:
        return k * (ov * vds - vds * vds / 2) * (1 + lam * vds)
    return k / 2 * ov * ov * (1 + lam * vds)


def inverter_vout(vin, vdd=1.0, vt=0.3):
    lo, hi = 0.0, vdd
    for _ in range(80):  # the n current rises with vout, the p current falls: bisect on their difference
        mid = (lo + hi) / 2
        d = _ids(vin, mid, vt) - _ids(vdd - vin, vdd - mid, vt)
        if d > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def compute_cmos() -> dict:
    vin = np.linspace(0, 1, 801)
    vout = np.array([inverter_vout(v) for v in vin])
    gain = np.gradient(vout, vin)
    vm = float(vin[np.argmin(np.abs(vout - vin))])
    steep = np.where(gain < -1)[0]
    vil, vih = float(vin[steep[0]]), float(vin[steep[-1]])
    voh, vol = float(np.interp(vil, vin, vout)), float(np.interp(vih, vin, vout))
    # the current drawn from the supply: only while both transistors conduct
    idd = np.array([_ids(v, inverter_vout(v)) for v in vin])
    assert abs(vm - 0.5) < 0.01 and vil < vm < vih
    return {"vin": vin, "vout": vout, "gain": gain, "idd": idd, "vm": vm, "vil": vil, "vih": vih, "voh": voh,
            "vol": vol, "nml": vil - vol, "nmh": voh - vih, "max_gain": float(-gain.min())}


# ---------------------------------------------------------------------------
# Post's lattice for two-input gates
# ---------------------------------------------------------------------------
NAMES = {0b0000: "0", 0b1111: "1", 0b1000: "AND", 0b1110: "OR", 0b0111: "NAND", 0b0001: "NOR", 0b0110: "XOR",
         0b1001: "XNOR", 0b1100: "x", 0b1010: "y", 0b0011: "NOT x", 0b0101: "NOT y", 0b1011: "x => y",
         0b1101: "y => x", 0b0100: "x AND NOT y", 0b0010: "NOT x AND y"}  # bit 2x + y is f(x, y)


def tt_fn(tt):
    """tt bit i is f(x, y) for i = 2x + y."""
    return lambda x, y: (tt >> (2 * x + y)) & 1


def properties(tt) -> dict:
    f = tt_fn(tt)
    pts = list(itertools.product((0, 1), repeat=2))
    p0 = f(0, 0) == 0
    p1 = f(1, 1) == 1
    mono = all(f(*a) <= f(*b) for a in pts for b in pts if a[0] <= b[0] and a[1] <= b[1])
    selfdual = all(f(1 - x, 1 - y) == 1 - f(x, y) for x, y in pts)
    affine = any(all(f(x, y) == (c ^ (a & x) ^ (b & y)) for x, y in pts) for a, b, c in itertools.product((0, 1),
                                                                                                         repeat=3))
    return {"0-preserving": p0, "1-preserving": p1, "monotone": mono, "self-dual": selfdual, "affine": affine}


def complete(tts) -> bool:
    """Post (1941): complete exactly when, for each of the five properties, some gate lacks it."""
    props = [properties(t) for t in tts]
    return all(any(not p[k] for p in props) for k in props[0])


def compute_post() -> dict:
    rows = []
    for tt in sorted(NAMES, key=lambda t: NAMES[t]):
        p = properties(tt)
        rows.append({"tt": tt, "name": NAMES[tt], **p, "complete": complete([tt])})
    alone = [r["name"] for r in rows if r["complete"]]
    assert sorted(alone) == ["NAND", "NOR"]
    sets = []
    for names in (("AND", "OR"), ("AND", "NOT x"), ("OR", "NOT x"), ("XOR", "AND"), ("XOR", "AND", "1"),
                  ("x => y",), ("x => y", "0"), ("AND", "OR", "XOR"), ("XOR", "XNOR")):
        tts = [t for n in names for t in NAMES if NAMES[t] == n]
        sets.append({"gates": list(names), "complete": complete(tts),
                     "trapped": [k for k in properties(0) if all(properties(t)[k] for t in tts)]})
    return {"rows": rows, "alone": alone, "sets": sets}


# ---------------------------------------------------------------------------
# minimal NAND circuits for two-input functions
# ---------------------------------------------------------------------------
def compute_nandmin(max_gates=6) -> dict:
    X, Y = 0b1100, 0b1010  # bit i = value at (x, y) with i = 2x + y
    best = {X: 0, Y: 0}
    witness = {X: [], Y: []}
    frontier = {(X, Y): []}
    for g in range(1, max_gates + 1):
        nxt = {}
        for wires, gates in frontier.items():
            ws = list(wires)
            for i in range(len(ws)):
                for j in range(i, len(ws)):
                    out = (~(ws[i] & ws[j])) & 0b1111
                    if out in ws:
                        continue
                    new = tuple(sorted(ws + [out]))
                    if new in nxt:
                        continue
                    nxt[new] = gates + [(ws[i], ws[j], out)]
                    if out not in best:
                        best[out] = g
                        witness[out] = nxt[new]
        frontier = nxt
        if len(best) == 16:
            break
    rows = [{"tt": t, "name": NAMES[t], "nands": best[t], "circuit": witness[t]} for t in sorted(best,
                                                                                                key=lambda t: (best[t], NAMES[t]))]
    got = {r["name"]: r["nands"] for r in rows}
    assert got["NOT x"] == 1 and got["AND"] == 2 and got["OR"] == 3 and got["XOR"] == 4
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Karnaugh map and Quine-McCluskey
# ---------------------------------------------------------------------------
def quine_mccluskey(minterms, n):
    terms = {(m, 0) for m in minterms}  # (value bits, mask of dashes)
    primes = set()
    while terms:
        used, nxt = set(), set()
        tl = sorted(terms)
        for a in tl:
            for b in tl:
                if a < b and a[1] == b[1]:
                    diff = a[0] ^ b[0]
                    if diff and diff & (diff - 1) == 0:
                        nxt.add((a[0] & ~diff, a[1] | diff))
                        used.update((a, b))
        primes |= terms - used
        terms = nxt
    return sorted(primes)


def covers(p, m):
    v, mask = p
    return (m & ~mask) == v


def term_str(p, n, names="ABCD"):
    v, mask = p
    out = []
    for k in range(n):
        bit = 1 << (n - 1 - k)
        if mask & bit:
            continue
        out.append(names[k] + ("" if v & bit else "'"))
    return "".join(out) or "1"


def compute_kmap() -> dict:
    n = 4
    minterms = [0, 2, 4, 5, 6, 7, 8, 10, 13, 15]
    primes = quine_mccluskey(minterms, n)
    # the smallest cover, by brute force over subsets of the primes
    best = None
    for r in range(1, len(primes) + 1):
        for sub in itertools.combinations(primes, r):
            if all(any(covers(p, m) for p in sub) for m in minterms):
                best = list(sub)
                break
        if best:
            break
    f = lambda m: m in minterms  # noqa: E731
    assert all(f(m) == any(covers(p, m) for p in best) for m in range(16))
    return {"minterms": minterms, "primes": [[p[0], p[1], term_str(p, n)] for p in primes],
            "cover": [[p[0], p[1], term_str(p, n)] for p in best], "dnf_terms": len(minterms)}


# ---------------------------------------------------------------------------
# parity: DNF against a tree
# ---------------------------------------------------------------------------
def compute_parity() -> dict:
    rows = []
    for n in range(2, 13):
        minterms = [m for m in range(2 ** n) if bin(m).count("1") % 2 == 1]
        rows.append({"n": n, "dnf_terms": len(minterms), "literals": len(minterms) * n, "xors": n - 1,
                     "depth": math.ceil(math.log2(n))})
        assert len(minterms) == 2 ** (n - 1)
    # no two odd minterms are adjacent, so none merges: every minterm is a prime implicant
    assert len(quine_mccluskey([m for m in range(16) if bin(m).count("1") % 2], 4)) == 8
    return {"rows": rows}


# ---------------------------------------------------------------------------
# binary decision diagrams
# ---------------------------------------------------------------------------
class BDD:
    def __init__(self):
        self.unique = {}
        self.nodes = [None, None]  # 0 and 1 are the terminals

    def mk(self, var, lo, hi):
        if lo == hi:
            return lo
        key = (var, lo, hi)
        if key not in self.unique:
            self.unique[key] = len(self.nodes)
            self.nodes.append(key)
        return self.unique[key]

    def build(self, table, order):
        """table: truth table indexed by the bits of the input (bit i is variable i); order: variables top first."""
        n = len(order)

        def go(level, fixed):
            if level == n:
                idx = sum(b << v for v, b in fixed.items())
                return int(table[idx])
            v = order[level]
            lo = go(level + 1, {**fixed, v: 0})
            hi = go(level + 1, {**fixed, v: 1})
            return self.mk(v, lo, hi)

        return go(0, {})

    def size(self, root):
        seen, stack = set(), [root]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            if u > 1:
                _, lo, hi = self.nodes[u]
                stack += [lo, hi]
        return len(seen)


def pairs_table(k):
    n = 2 * k
    idx = np.arange(2 ** n)
    bits = [(idx >> v) & 1 for v in range(n)]
    out = np.zeros(2 ** n, dtype=np.uint8)
    for j in range(k):
        out |= (bits[2 * j] & bits[2 * j + 1]).astype(np.uint8)
    return out


def bdd_struct(bdd, root):
    """Nodes reachable from root: (id, var, lo, hi), for drawing."""
    out, seen, stack = [], set(), [root]
    while stack:
        u = stack.pop()
        if u in seen or u <= 1:
            continue
        seen.add(u)
        v, lo, hi = bdd.nodes[u]
        out.append([u, v, lo, hi])
        stack += [lo, hi]
    return out


def compute_bdd() -> dict:
    rows = []
    small = {}
    for k in range(1, 8):
        t = pairs_table(k)
        good = list(range(2 * k))
        bad = [2 * j for j in range(k)] + [2 * j + 1 for j in range(k)]
        b1, b2 = BDD(), BDD()
        r1, r2 = b1.build(t, good), b2.build(t, bad)
        s1, s2 = b1.size(r1), b2.size(r2)
        assert s1 == 2 * k + 2 and s2 == 2 ** (k + 1)
        rows.append({"k": k, "vars": 2 * k, "good": s1, "bad": s2})
        if k == 3:
            small = {"good": bdd_struct(b1, r1), "bad": bdd_struct(b2, r2), "good_order": good, "bad_order": bad,
                     "root_good": r1, "root_bad": r2}
    return {"rows": rows, "k3": small}


# ---------------------------------------------------------------------------
# Shannon's counting argument
# ---------------------------------------------------------------------------
def compute_counting() -> dict:
    rows = []
    for n in range(2, 31):
        log_f = 2.0 ** n  # log2 of the number of n-input functions
        s = 1
        while s * math.log2(16 * (n + s) ** 2) < log_f:  # circuits of s gates: at most (16 (n + s)^2)^s
            s += 1
        rows.append({"n": n, "log2_functions": log_f, "s_needed": s, "two_n_over_n": 2 ** n / n})
    # for n = 4, the curves: log2 #circuits of size s, against log2 #functions = 16
    curve = [{"s": s, "log2_circuits": s * math.log2(16 * (4 + s) ** 2)} for s in range(0, 9)]
    return {"rows": rows, "curve4": curve}


# ---------------------------------------------------------------------------
# a glitch
# ---------------------------------------------------------------------------
def simulate_hazard(fixed: bool, steps=10):
    """f = a b + (not a) c (+ b c when fixed), b = c = 1, a falls from 1 to 0 at t = 1; every gate has delay 1."""
    a = [1] + [0] * steps
    na, g1, g2, g3, f = [0], [1], [0], [1], [1]
    for t in range(1, steps + 1):
        na.append(1 - a[t - 1])
        g1.append(a[t - 1] & 1)
        g2.append(na[t - 1] & 1)
        g3.append(1)
        f.append(g1[t - 1] | g2[t - 1] | (g3[t - 1] if fixed else 0))
    return {"a": a, "not_a": na, "ab": g1, "nac": g2, "bc": g3, "f": f}


def compute_glitch() -> dict:
    before, after = simulate_hazard(False), simulate_hazard(True)
    assert 0 in before["f"][1:] and all(v == 1 for v in after["f"])
    return {"before": before, "after": after}


# ---------------------------------------------------------------------------
# the blocks Pebble needs
# ---------------------------------------------------------------------------
def mux2(c, s, a, b):
    """s ? b : a."""
    return c.or_(c.and_(c.not_(s), a), c.and_(s, b))


def comparator(n=4):
    c = Circuit(f"{n}-bit comparator")
    a, b = c.input("a", n), c.input("b", n)
    eq_so_far = None
    lt = None
    for i in reversed(range(n)):  # from the top bit down
        e = c.xnor(a[i], b[i])
        l_ = c.and_(c.not_(a[i]), b[i])
        if eq_so_far is None:
            lt, eq_so_far = l_, e
        else:
            lt = c.or_(lt, c.and_(eq_so_far, l_))
            eq_so_far = c.and_(eq_so_far, e)
    c.output("lt", lt)
    c.output("eq", eq_so_far)
    return c


def parity_tree(n=8):
    c = Circuit(f"{n}-bit parity tree")
    x = c.input("x", n)
    layer = list(x)
    while len(layer) > 1:
        layer = [c.xor(layer[i], layer[i + 1]) if i + 1 < len(layer) else layer[i] for i in range(0, len(layer), 2)]
    c.output("p", layer[0])
    return c


def parity_chain(n=8):
    c = Circuit(f"{n}-bit parity chain")
    x = c.input("x", n)
    p = x[0]
    for i in range(1, n):
        p = c.xor(p, x[i])
    c.output("p", p)
    return c


def priority_encoder(n=8):
    c = Circuit(f"{n}-to-{n.bit_length() - 1} priority encoder")
    x = c.input("x", n)
    k = n.bit_length() - 1
    # one-hot of the highest set bit
    hot, none_above = [None] * n, None
    for i in reversed(range(n)):
        hot[i] = x[i] if none_above is None else c.and_(x[i], none_above)
        none_above = c.not_(x[i]) if none_above is None else c.and_(none_above, c.not_(x[i]))
    outs = []
    for b in range(k):
        terms = [hot[i] for i in range(n) if (i >> b) & 1]
        o = terms[0]
        for t in terms[1:]:
            o = c.or_(o, t)
        outs.append(o)
    c.output("y", outs)
    c.output("valid", c.not_(none_above))
    return c


def barrel_shifter(n=8):
    c = Circuit(f"{n}-bit barrel shifter (left)")
    x = c.input("x", n)
    k = n.bit_length() - 1
    s = c.input("s", k)
    zero = c.const(0)
    cur = list(x)
    for st in range(k):
        d = 1 << st
        cur = [mux2(c, s[st], cur[i], cur[i - d] if i - d >= 0 else zero) for i in range(n)]
    c.output("y", cur)
    return c


def decoder(k=3):
    c = Circuit(f"{k}-to-{2 ** k} decoder")
    a = c.input("a", k)
    na = [c.not_(w) for w in a]
    outs = []
    for v in range(2 ** k):
        lits = [a[i] if (v >> i) & 1 else na[i] for i in range(k)]
        o = lits[0]
        for l_ in lits[1:]:
            o = c.and_(o, l_)
        outs.append(o)
    c.output("y", outs)
    return c


def mux_n(k=3):
    c = Circuit(f"{2 ** k}-to-1 multiplexer")
    d = c.input("d", 2 ** k)
    s = c.input("s", k)
    layer = list(d)
    for st in range(k):
        layer = [mux2(c, s[st], layer[2 * i], layer[2 * i + 1]) for i in range(len(layer) // 2)]
    c.output("y", layer[0])
    return c


def check(c, spec):
    """Evaluate on every input pattern and compare with spec(inputs) -> outputs, all as integer arrays."""
    ins = exhaustive(c)
    out = c.evaluate(ins)
    n_vec = 2 ** sum(len(w) for w in c.inputs.values())
    iv = {k: sum(unpack(w, n_vec).astype(np.int64) << i for i, w in enumerate(ws)) for k, ws in ins.items()}
    ov = {k: sum(unpack(w, n_vec).astype(np.int64) << i for i, w in enumerate(ws)) for k, ws in out.items()}
    want = spec(iv)
    for k, v in want.items():
        assert np.array_equal(ov[k], v), (c.name, k)
    return n_vec


def block_row(c, spec):
    n_vec = check(c, spec)
    nand = c.to_nand()
    check(nand, spec)
    cnt = {k: v for k, v in c.counts().items() if k not in ("INPUT", "CONST0", "CONST1")}
    return {"name": c.name, "gates": int(sum(cnt.values())), "counts": cnt, "depth": c.depth(),
            "nands": nand.counts().get("NAND", 0), "nand_depth": nand.depth(), "vectors": n_vec}


def compute_blocks() -> dict:
    def popc(v):
        return np.array([bin(int(x)).count("1") for x in v])

    rows = [
        block_row(comparator(4), lambda i: {"lt": (i["a"] < i["b"]).astype(int), "eq": (i["a"] == i["b"]).astype(int)}),
        block_row(comparator(8), lambda i: {"lt": (i["a"] < i["b"]).astype(int), "eq": (i["a"] == i["b"]).astype(int)}),
        block_row(parity_chain(8), lambda i: {"p": popc(i["x"]) % 2}),
        block_row(parity_tree(8), lambda i: {"p": popc(i["x"]) % 2}),
        block_row(priority_encoder(8), lambda i: {"y": np.array([int(x).bit_length() - 1 if x else 0 for x in i["x"]]),
                                                  "valid": (i["x"] > 0).astype(int)}),
        block_row(barrel_shifter(8), lambda i: {"y": (i["x"] << i["s"]) & 0xFF}),
        block_row(decoder(3), lambda i: {"y": 1 << i["a"]}),
        block_row(mux_n(3), lambda i: {"y": (i["d"] >> i["s"]) & 1}),
    ]
    return {"rows": rows}


# ---------------------------------------------------------------------------
# The Frontier chapter (videos/cs/SYLLABUS.md 1.1): exact circuit sizes
# ---------------------------------------------------------------------------
def compute_census() -> dict:
    """The exact minimum number of two-input gates (any of the ten non-trivial ones) for every 3-input function.
    Breadth-first over circuits: a circuit is the set of functions its wires compute, so level s holds every
    distinct set reachable with s gates, and a function's cost is the first level at which it appears."""
    n = 3
    full = (1 << (1 << n)) - 1
    xs = [sum(1 << r for r in range(1 << n) if r >> i & 1) for i in range(n)]
    ops = [lambda a, b: a & b, lambda a, b: a | b, lambda a, b: a ^ b, lambda a, b: full & ~(a & b),
           lambda a, b: full & ~(a | b), lambda a, b: full & ~(a ^ b), lambda a, b: a & ~b & full,
           lambda a, b: ~a & b & full, lambda a, b: (a | ~b) & full, lambda a, b: (~a | b) & full]
    cost = {0: 0, full: 0, **{x: 0 for x in xs}}
    level, states = {frozenset(xs)}, []
    s = 0
    while len(cost) < 1 << (1 << n):
        s += 1
        nxt = set()
        for st in level:
            ws = list(st)
            for i in range(len(ws)):
                for j in range(i + 1, len(ws)):
                    for op in ops:
                        f = op(ws[i], ws[j])
                        if f in st:
                            continue
                        cost.setdefault(f, s)
                        nxt.add(st | {f})
        level = nxt
        states.append(len(level))
    hist = [sum(1 for v in cost.values() if v == k) for k in range(max(cost.values()) + 1)]
    a, b, c = xs[0], xs[1], xs[2]
    named = {"x xor y xor z": a ^ b ^ c, "majority": (a & b) | (a & c) | (b & c), "x and y and z": a & b & c,
             "if x then y else z": (a & b) | (full & ~a & c)}
    return {"hist": hist, "states": states, "named": {k: cost[v] for k, v in named.items()},
            # published: the largest exact costs for 4 and 5 inputs (Knuth, TAOCP 7.1.2, 2005-08; the last
            # 5-input holdouts settled by computer in 2019) and the number of functions
            "known": [(3, "4", "256"), (4, "7", "65{,}536"), (5, "12", "4.3 \\times 10^{9}"),
                      (6, "?", "1.8 \\times 10^{19}")]}


ITEMS = {
    "cmos": compute_cmos, "post": compute_post, "nandmin": compute_nandmin, "kmap": compute_kmap,
    "parity": compute_parity, "bdd": compute_bdd, "counting": compute_counting, "glitch": compute_glitch,
    "blocks": compute_blocks, "census": compute_census,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
