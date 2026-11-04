"""Netlists and a bit-parallel gate simulator: the bottom of Pebble (built on screen in Part 3).

    c = Circuit("full adder")
    a, b, cin = c.input("a"), c.input("b"), c.input("cin")
    s1 = c.xor(a, b)
    c.output("sum", c.xor(s1, cin))
    c.output("cout", c.or_(c.and_(a, b), c.and_(s1, cin)))
    vals = c.evaluate(exhaustive(c))      # every input pattern at once
    c.counts(), c.depth(), c.to_nand().counts()

A wire is an integer; a gate reads wires that already exist, so creation order is a topological order and evaluation
is one pass.  Values are numpy ``uint64`` arrays: bit j of word k is the wire's value in test vector 64 k + j, so one
pass evaluates 64 input patterns per machine word (``exhaustive`` packs all 2^n patterns of a small circuit).
Multi-bit signals are lists of wires, least significant bit first.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

ONES = np.uint64(0xFFFF_FFFF_FFFF_FFFF)
KINDS = ("CONST0", "CONST1", "INPUT", "NAND", "AND", "OR", "NOT", "XOR", "NOR", "XNOR", "BUF")


@dataclass
class Circuit:
    name: str = "circuit"
    kinds: list[str] = field(default_factory=list)
    args: list[tuple[int, ...]] = field(default_factory=list)
    inputs: dict[str, list[int]] = field(default_factory=dict)
    outputs: dict[str, list[int]] = field(default_factory=dict)

    # -- building -------------------------------------------------------------------
    def _new(self, kind: str, *ins: int) -> int:
        for w in ins:
            if not 0 <= w < len(self.kinds):
                raise ValueError(f"{self.name}: wire {w} does not exist yet")
        self.kinds.append(kind)
        self.args.append(tuple(ins))
        return len(self.kinds) - 1

    def input(self, name: str, width: int = 1):
        ws = [self._new("INPUT") for _ in range(width)]
        self.inputs[name] = ws
        return ws[0] if width == 1 else ws

    def output(self, name: str, wires) -> None:
        self.outputs[name] = [wires] if isinstance(wires, int) else list(wires)

    def const(self, bit: int) -> int:
        return self._new("CONST1" if bit else "CONST0")

    def nand(self, a, b):
        return self._new("NAND", a, b)

    def and_(self, a, b):
        return self._new("AND", a, b)

    def or_(self, a, b):
        return self._new("OR", a, b)

    def not_(self, a):
        return self._new("NOT", a)

    def xor(self, a, b):
        return self._new("XOR", a, b)

    def nor(self, a, b):
        return self._new("NOR", a, b)

    def xnor(self, a, b):
        return self._new("XNOR", a, b)

    def buf(self, a):
        return self._new("BUF", a)

    def embed(self, sub: "Circuit", **inputs) -> dict[str, list[int]]:
        """Copy ``sub``'s gates into this circuit, its inputs wired to ``inputs[name]`` (wires here); returns its
        outputs as lists of wires.  How a CPU uses Part 4's ALU as one block."""
        m: dict[int, int] = {}
        for name, ws in sub.inputs.items():
            src = inputs[name]
            src = [src] if isinstance(src, int) else list(src)
            if len(src) != len(ws):
                raise ValueError(f"{sub.name}: input {name} is {len(ws)} bits, got {len(src)}")
            m.update(zip(ws, src))
        for i, (kind, ins) in enumerate(zip(sub.kinds, sub.args)):
            if kind != "INPUT":
                m[i] = self._new(kind, *[m[w] for w in ins])
        return {name: [m[w] for w in ws] for name, ws in sub.outputs.items()}

    # -- evaluation -----------------------------------------------------------------
    def evaluate(self, values: dict) -> dict[str, list[np.ndarray]]:
        """``values[name]`` is a list (one per bit of the input, LSB first) of uint64 arrays, or for a 1-bit input a
        single array.  Returns each output as a list of uint64 arrays (bit-parallel)."""
        k = None
        val: list = [None] * len(self.kinds)
        for name, ws in self.inputs.items():
            v = values[name]
            v = [v] if len(ws) == 1 and not isinstance(v, list) else v
            for w, x in zip(ws, v):
                val[w] = np.asarray(x, dtype=np.uint64)
                k = val[w].shape
        zero = np.zeros(k or (1,), np.uint64)
        for i, (kind, ins) in enumerate(zip(self.kinds, self.args)):
            if kind == "INPUT":
                continue
            if kind == "CONST0":
                val[i] = zero
            elif kind == "CONST1":
                val[i] = zero | ONES
            elif kind == "NAND":
                val[i] = ~(val[ins[0]] & val[ins[1]])
            elif kind == "AND":
                val[i] = val[ins[0]] & val[ins[1]]
            elif kind == "OR":
                val[i] = val[ins[0]] | val[ins[1]]
            elif kind == "NOT":
                val[i] = ~val[ins[0]]
            elif kind == "XOR":
                val[i] = val[ins[0]] ^ val[ins[1]]
            elif kind == "NOR":
                val[i] = ~(val[ins[0]] | val[ins[1]])
            elif kind == "XNOR":
                val[i] = ~(val[ins[0]] ^ val[ins[1]])
            elif kind == "BUF":
                val[i] = val[ins[0]]
        return {n: [val[w] for w in ws] for n, ws in self.outputs.items()}

    def evaluate_ints(self, values: dict[str, int]) -> dict[str, int]:
        """One input pattern, as integers (bit i of an input's integer is its wire i)."""
        packed = {n: [np.uint64(ONES if (values[n] >> i) & 1 else 0) for i in range(len(ws))]
                  for n, ws in self.inputs.items()}
        out = self.evaluate(packed)
        return {n: sum((int(v.item()) & 1) << i for i, v in enumerate(vs)) for n, vs in out.items()}

    # -- measuring --------------------------------------------------------------------
    def counts(self) -> dict[str, int]:
        c: dict[str, int] = {}
        for k in self.kinds:
            if k not in ("INPUT", "CONST0", "CONST1", "BUF"):
                c[k] = c.get(k, 0) + 1
        return c

    def size(self) -> int:
        return sum(self.counts().values())

    def levels(self) -> list[int]:
        """Each wire's depth in gates from the inputs (inputs and constants are level 0)."""
        lv = [0] * len(self.kinds)
        for i, (kind, ins) in enumerate(zip(self.kinds, self.args)):
            if ins:
                lv[i] = max(lv[w] for w in ins) + (0 if kind == "BUF" else 1)
        return lv

    def depth(self) -> int:
        lv = self.levels()
        return max((lv[w] for ws in self.outputs.values() for w in ws), default=0)

    def pruned(self) -> "Circuit":
        """The same circuit without gates that no output depends on (building helpers often leave a few)."""
        live = set()
        stack = [w for ws in self.outputs.values() for w in ws]
        while stack:
            w = stack.pop()
            if w in live:
                continue
            live.add(w)
            stack.extend(self.args[w])
        n = Circuit(self.name)
        m: dict[int, int] = {}
        for name, ws in self.inputs.items():
            new = n.input(name, len(ws))
            new = [new] if isinstance(new, int) else new
            m.update(zip(ws, new))
        for i, (kind, ins) in enumerate(zip(self.kinds, self.args)):
            if kind == "INPUT" or i not in live:
                continue
            m[i] = n._new(kind, *[m[w] for w in ins])
        for name, ws in self.outputs.items():
            n.output(name, [m[w] for w in ws])
        return n

    def settle(self, values: dict[str, np.ndarray]) -> np.ndarray:
        """Floating-mode delay, one input pattern per array element: the time (in unit gate delays) at which every
        output has its final value.  A gate whose output is forced by one input (a 0 into AND or NAND, a 1 into OR or
        NOR) settles one delay after the earliest such input; otherwise one delay after its last input.  Unlike
        ``depth()``, this sees through false paths, such as the ripple path of a carry-skip adder."""
        v: list = [None] * len(self.kinds)
        t: list = [None] * len(self.kinds)
        size = None
        for name, ws in self.inputs.items():
            x = np.asarray(values[name], dtype=np.int64)
            size = x.shape
            for i, w in enumerate(ws):
                v[w] = (x >> i) & 1
                t[w] = np.zeros(size, np.int64)
        big = 1 << 40
        for i, (kind, ins) in enumerate(zip(self.kinds, self.args)):
            if kind == "INPUT":
                continue
            if kind in ("CONST0", "CONST1"):
                v[i] = np.full(size, int(kind == "CONST1"), np.int64)
                t[i] = np.zeros(size, np.int64)
                continue
            a = [v[w] for w in ins]
            ta = [t[w] for w in ins]
            if kind == "BUF":
                v[i], t[i] = a[0], ta[0]
                continue
            if kind == "NOT":
                v[i], t[i] = 1 - a[0], ta[0] + 1
                continue
            if kind in ("AND", "NAND", "OR", "NOR"):
                ctl = 0 if kind in ("AND", "NAND") else 1
                forced = [np.where(x == ctl, tx, big) for x, tx in zip(a, ta)]
                early = np.minimum(forced[0], forced[1])
                late = np.maximum(ta[0], ta[1])
                t[i] = np.where(early < big, early, late) + 1
                r = (a[0] & a[1]) if ctl == 0 else (a[0] | a[1])
                v[i] = r if kind in ("AND", "OR") else 1 - r
                continue
            r = a[0] ^ a[1]
            v[i] = r if kind == "XOR" else 1 - r
            t[i] = np.maximum(ta[0], ta[1]) + 1
        out = np.zeros(size, np.int64)
        for ws in self.outputs.values():
            for w in ws:
                out = np.maximum(out, t[w])
        return out

    def to_nand(self) -> "Circuit":
        """The same function from NAND gates alone (Part 3's completeness proof, as a rewrite)."""
        n = Circuit(self.name + " (NAND only)")
        m: dict[int, int] = {}
        for name, ws in self.inputs.items():
            new = n.input(name, len(ws))
            new = [new] if isinstance(new, int) else new
            m.update(zip(ws, new))
        for i, (kind, ins) in enumerate(zip(self.kinds, self.args)):
            if kind == "INPUT":
                continue
            a = [m[w] for w in ins]
            if kind in ("CONST0", "CONST1"):
                m[i] = n.const(kind == "CONST1")
            elif kind == "NAND":
                m[i] = n.nand(*a)
            elif kind == "NOT":
                m[i] = n.nand(a[0], a[0])
            elif kind == "AND":
                t = n.nand(*a)
                m[i] = n.nand(t, t)
            elif kind == "OR":
                m[i] = n.nand(n.nand(a[0], a[0]), n.nand(a[1], a[1]))
            elif kind == "NOR":
                t = n.nand(n.nand(a[0], a[0]), n.nand(a[1], a[1]))
                m[i] = n.nand(t, t)
            elif kind in ("XOR", "XNOR"):
                t = n.nand(*a)
                x = n.nand(n.nand(a[0], t), n.nand(a[1], t))
                m[i] = x if kind == "XOR" else n.nand(x, x)
            elif kind == "BUF":
                m[i] = a[0]
        for name, ws in self.outputs.items():
            n.output(name, [m[w] for w in ws])
        return n


def exhaustive(c: Circuit) -> dict[str, list[np.ndarray]]:
    """Every input pattern of a small circuit (at most 24 input bits), packed 64 per word: pattern p sets input bit j
    (counting all inputs in order) to bit j of p."""
    bits = [(n, i) for n, ws in c.inputs.items() for i in range(len(ws))]
    nb = len(bits)
    if nb > 24:
        raise ValueError(f"{nb} input bits is too many to enumerate")
    total = 1 << nb
    words = max(1, total // 64)
    p = np.arange(words * 64, dtype=np.uint64)
    out: dict[str, list] = {n: [None] * len(ws) for n, ws in c.inputs.items()}
    for j, (n, i) in enumerate(bits):
        b = ((p >> np.uint64(j)) & np.uint64(1)).reshape(words, 64)
        out[n][i] = (b << np.arange(64, dtype=np.uint64)).sum(axis=1, dtype=np.uint64)
    return out


def unpack(v: np.ndarray, n: int) -> np.ndarray:
    """The first n test vectors' bits of a packed wire value, as 0/1 integers."""
    v = np.asarray(v, dtype=np.uint64)
    bits = (v[:, None] >> np.arange(64, dtype=np.uint64)) & np.uint64(1)
    return bits.reshape(-1)[:n].astype(np.int64)


def simulate(c: Circuit, values: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Run many input patterns given as integer arrays (one element per pattern, bit i = wire i of that input) and
    return each output as a uint64 array.  Patterns are packed 64 to a machine word, so this is bit-parallel too."""
    V = len(next(iter(values.values())))
    words = (V + 63) // 64
    pad = words * 64 - V
    packed = {}
    shifts = np.arange(64, dtype=np.uint64)
    for name, ws in c.inputs.items():
        x = np.concatenate([np.asarray(values[name], dtype=np.uint64), np.zeros(pad, np.uint64)])
        bits = []
        for i in range(len(ws)):
            b = ((x >> np.uint64(i)) & np.uint64(1)).reshape(words, 64)
            bits.append((b << shifts).sum(axis=1, dtype=np.uint64))
        packed[name] = bits if len(ws) > 1 else bits[0]
    out = c.evaluate(packed)
    res = {}
    for name, vs in out.items():
        acc = np.zeros(words * 64, np.uint64)
        for i, w in enumerate(vs):
            w = np.broadcast_to(np.asarray(w, np.uint64), (words,))
            b = ((w[:, None] >> shifts) & np.uint64(1)).reshape(-1)
            acc |= b << np.uint64(i)
        res[name] = acc[:V]
    return res
