"""The compiler's intermediate representation (Part 13, chapter 4): three-address code in basic blocks.

Values are virtual registers, written ``%name``, or integer constants.  An instruction is one :class:`I`:

    %d = const k           %d = copy a            %d = bin op a b        %d = un op a      (op: neg, not)
    %d = load a  (size, offset)                   store a v  (size, offset)
    %d = gaddr name        %d = faddr slot        (the address of a global, of a stack slot)
    %d = call f a b ...    %d = getc              putc a
    %d = phi a b ...  [from L1 L2 ...]
    br L                   cbr a L1 L2            ret [a]

``bin`` ops: add sub mul div rem and or xor shl shr sar, and the comparisons lt le gt ge eq ne ltu leu gtu geu, which
produce 0 or 1.  A :class:`Block` ends in exactly one of br, cbr, ret.  A :class:`Func` has its blocks in order (the
first is the entry), its parameters, and its stack slots (arrays, structs, and locals whose address is taken).
"""
from __future__ import annotations

from dataclasses import dataclass, field

PURE = {"const", "copy", "bin", "un", "gaddr", "faddr", "phi"}
SIDE = {"store", "call", "getc", "putc", "br", "cbr", "ret"}
TERM = {"br", "cbr", "ret"}
COMMUTE = {"add", "mul", "and", "or", "xor", "eq", "ne"}
CMP = {"lt", "le", "gt", "ge", "eq", "ne", "ltu", "leu", "gtu", "geu"}


def is_var(x) -> bool:
    return isinstance(x, str)


@dataclass
class I:
    op: str
    dst: str | None = None
    args: list = field(default_factory=list)
    k: object = None

    def uses(self) -> list:
        return [a for a in self.args if is_var(a)]

    def __str__(self) -> str:
        a = " ".join(str(x) for x in self.args)
        if self.op == "const":
            return f"{self.dst} = {self.k}"
        if self.op == "copy":
            return f"{self.dst} = {a}"
        if self.op == "bin":
            sym = {"add": "+", "sub": "-", "mul": "*", "div": "/", "rem": "%", "and": "&", "or": "|", "xor": "^",
                   "shl": "<<", "shr": ">>u", "sar": ">>", "lt": "<", "le": "<=", "gt": ">", "ge": ">=",
                   "eq": "==", "ne": "!=", "ltu": "<u", "leu": "<=u", "gtu": ">u", "geu": ">=u"}[self.k]
            return f"{self.dst} = {self.args[0]} {sym} {self.args[1]}"
        if self.op == "un":
            return f"{self.dst} = {'-' if self.k == 'neg' else '!'}{a}"
        if self.op == "load":
            size, off = self.k
            return f"{self.dst} = load{'b' if size == 1 else ''} [{self.args[0]}{'+' + str(off) if off else ''}]"
        if self.op == "store":
            size, off = self.k
            return f"store{'b' if size == 1 else ''} [{self.args[0]}{'+' + str(off) if off else ''}] = {self.args[1]}"
        if self.op == "gaddr":
            return f"{self.dst} = &{self.k}"
        if self.op == "faddr":
            return f"{self.dst} = &frame.{self.k}"
        if self.op == "call":
            return (f"{self.dst} = " if self.dst else "") + f"call {self.k}({', '.join(map(str, self.args))})"
        if self.op == "getc":
            return f"{self.dst} = getc()"
        if self.op == "putc":
            return f"putc({a})"
        if self.op == "phi":
            return f"{self.dst} = φ(" + ", ".join(f"{v}:{l}" for v, l in zip(self.args, self.k)) + ")"
        if self.op == "br":
            return f"br {self.k}"
        if self.op == "cbr":
            return f"if {a} br {self.k[0]} else {self.k[1]}"
        if self.op == "ret":
            return f"ret {a}".rstrip()
        return f"{self.op} {self.dst} {a} {self.k}"


@dataclass
class Block:
    label: str
    ins: list = field(default_factory=list)

    @property
    def term(self) -> I:
        return self.ins[-1]

    def succs(self) -> list:
        t = self.ins[-1] if self.ins else None
        if t is None or t.op == "ret":
            return []
        if t.op == "br":
            return [t.k]
        if t.op == "cbr":
            return list(dict.fromkeys(t.k))
        return []


@dataclass
class Func:
    name: str
    params: list
    blocks: list
    slots: dict = field(default_factory=dict)       # name -> (size, align)
    returns_value: bool = True

    def block(self, label) -> Block:
        for b in self.blocks:
            if b.label == label:
                return b
        raise KeyError(label)

    def labels(self) -> dict:
        return {b.label: b for b in self.blocks}

    def preds(self) -> dict:
        p = {b.label: [] for b in self.blocks}
        for b in self.blocks:
            for s in b.succs():
                p[s].append(b.label)
        return p

    def instructions(self):
        for b in self.blocks:
            yield from b.ins

    def count(self) -> int:
        return sum(len(b.ins) for b in self.blocks)

    def __str__(self) -> str:
        out = [f"fn {self.name}({', '.join(self.params)})"]
        for b in self.blocks:
            out.append(f"{b.label}:")
            out += [f"    {i}" for i in b.ins]
        return "\n".join(out)


@dataclass
class Module:
    funcs: list
    globals: dict                  # name -> (size, align, initial int or None)
    info: object = None

    def func(self, name) -> Func:
        for f in self.funcs:
            if f.name == name:
                return f
        raise KeyError(name)

    def __str__(self):
        return "\n\n".join(str(f) for f in self.funcs)


def remove_unreachable(f: Func) -> int:
    seen, stack = set(), [f.blocks[0].label]
    lab = f.labels()
    while stack:
        l = stack.pop()
        if l in seen:
            continue
        seen.add(l)
        stack += lab[l].succs()
    dead = [b for b in f.blocks if b.label not in seen]
    f.blocks = [b for b in f.blocks if b.label in seen]
    if dead:
        live = {b.label for b in f.blocks}
        for b in f.blocks:
            for i in b.ins:
                if i.op == "phi":
                    keep = [(v, p) for v, p in zip(i.args, i.k) if p in live]
                    i.args = [v for v, _ in keep]
                    i.k = [p for _, p in keep]
    return len(dead)


def rpo(f: Func) -> list:
    """Blocks in reverse postorder from the entry."""
    lab = f.labels()
    seen, order = set(), []

    def dfs(l):
        seen.add(l)
        for s in lab[l].succs():
            if s not in seen:
                dfs(s)
        order.append(l)
    import sys
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 10000))
    dfs(f.blocks[0].label)
    sys.setrecursionlimit(old)
    return order[::-1]
