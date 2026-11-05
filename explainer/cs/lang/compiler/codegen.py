"""The back end (Part 13, chapters 11–13): instruction selection, register allocation, frames, and Pebble assembly.

* :func:`select` tiles each IR instruction with Pebble instructions, greedily and largest tile first (maximal
  munch): constants that fit become immediates (``addi``, ``slti``, ``lw d, off(base)``), a comparison that only
  feeds a branch becomes the branch itself (``blt``, ``bge``…), the devices are reached through ``zero``.  The result
  is machine code over virtual registers, :class:`MI`.
* :func:`allocate` is Chaitin's graph colouring (1981) with Briggs's optimistic select (1994): build the
  interference graph from liveness, simplify nodes of degree < k, push the rest optimistically, colour in reverse,
  spill what cannot be coloured and try again.  Physical registers are precoloured nodes; a call interferes with
  every caller-saved register, so values live across calls land in s0–s2 or on the stack.  Colours are chosen
  biased towards a move partner's, which deletes most copies without a separate coalescing pass.
* :func:`emit` lays out the frame (spill slots, the IR's stack slots, saved s-registers and ``ra``), writes the
  prologue and epilogue, and prints assembly for :mod:`explainer.cs.pebble.asm`.
* ``-O0`` is the same pipeline with every virtual register spilled before allocation: each value lives in its own
  stack slot, loaded before every use and stored after every definition, as an unoptimizing compiler does.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from explainer.cs.lang.compiler.ir import Func, I, is_var

ALLOCATABLE = ["t0", "t1", "t2", "t3", "a5", "a4", "a3", "a2", "a1", "a0", "s0", "s1", "s2"]
CALLER_SAVED = {"t0", "t1", "t2", "t3", "a0", "a1", "a2", "a3", "a4", "a5", "ra"}
CALLEE_SAVED = ["s0", "s1", "s2"]
ARGS = ["a0", "a1", "a2", "a3", "a4", "a5"]
PHYS = set(ALLOCATABLE) | {"zero", "ra", "sp"}
IO_CONSOLE, IO_TAPE = -65536, -65532        # 0xFFFF0000 and 0xFFFF0004 as signed 18-bit immediates


def fits(v: int, bits: int = 18) -> bool:
    return -(1 << (bits - 1)) <= v < (1 << (bits - 1))


@dataclass
class MI:
    """One machine instruction over registers that may still be virtual.  ``form`` says how to print it."""
    op: str
    rd: str | None = None
    rs: list = field(default_factory=list)
    imm: object = None
    label: str | None = None
    clobbers: tuple = ()
    form: str = ""

    def defs(self) -> list:
        return ([self.rd] if self.rd else []) + list(self.clobbers)

    def uses(self) -> list:
        return list(self.rs)

    def is_move(self) -> bool:
        return self.op == "mv"


@dataclass
class MBlock:
    label: str
    ins: list = field(default_factory=list)
    succs: list = field(default_factory=list)


@dataclass
class MFunc:
    name: str
    blocks: list
    slots: dict
    has_call: bool = False
    spill_slots: dict = field(default_factory=dict)
    colors: dict = field(default_factory=dict)
    stats: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# instruction selection
# ---------------------------------------------------------------------------
class Selector:
    def __init__(self, f: Func):
        self.f = f
        self.n = 0
        self.uses: dict = {}
        for b in f.blocks:
            for i in b.ins:
                for a in i.uses():
                    self.uses[a] = self.uses.get(a, 0) + 1

    def tmp(self) -> str:
        self.n += 1
        return f"%s{self.n}"

    def reg(self, out: list, v) -> str:
        """An operand in a register: constants are materialized (0 is the zero register)."""
        if is_var(v):
            return v
        if v == 0:
            return "zero"
        t = self.tmp()
        out.append(MI("li", t, [], v, form="li") if not fits(v) else MI("addi", t, ["zero"], v, form="ri"))
        return t

    def run(self) -> MFunc:
        f = self.f
        mb = []
        order = [b.label for b in f.blocks]
        for bi, b in enumerate(f.blocks):
            out: list = []
            nxt = order[bi + 1] if bi + 1 < len(order) else None
            if bi == 0:
                for p, a in zip(f.params, ARGS):
                    out.append(MI("mv", p, [a], form="mv"))
            fused = set()
            ins = b.ins
            for k, i in enumerate(ins):
                if id(i) in fused:
                    continue
                if (i.op == "bin" and i.k in CMP_BRANCH and k + 1 < len(ins) and ins[k + 1].op == "cbr"
                        and ins[k + 1].args[0] == i.dst and self.uses.get(i.dst) == 1):
                    self.branch(out, i, ins[k + 1], nxt)
                    fused.add(id(ins[k + 1]))
                    continue
                self.one(out, i, nxt)
            mb.append(MBlock(b.label, out, b.succs()))
        has_call = any(m.op == "call" for blk in mb for m in blk.ins)
        return MFunc(f.name, mb, dict(f.slots), has_call)

    def branch(self, out, cmp: I, cbr: I, nxt):
        a, b = cmp.args
        yes, no = cbr.k
        op, swap = CMP_BRANCH[cmp.k]
        ra, rb = self.reg(out, a), self.reg(out, b)
        if swap:
            ra, rb = rb, ra
        if yes == nxt:                                      # branch on the opposite condition, fall into yes
            op, ra, rb, yes, no = INVERT[op], ra, rb, no, yes
            out.append(MI(op, None, [ra, rb], label=yes, form="br"))
            return
        out.append(MI(op, None, [ra, rb], label=yes, form="br"))
        if no != nxt:
            out.append(MI("j", label=no, form="j"))

    def one(self, out, i: I, nxt):
        op = i.op
        if op in ("copy", "const"):
            v = i.args[0] if op == "copy" else i.k
            if is_var(v):
                out.append(MI("mv", i.dst, [v], form="mv"))
            elif fits(v):
                out.append(MI("addi", i.dst, ["zero"], v, form="ri"))
            else:
                out.append(MI("li", i.dst, [], v, form="li"))
        elif op == "bin":
            self.binary(out, i)
        elif op == "un":
            a = self.reg(out, i.args[0])
            if i.k == "neg":
                out.append(MI("sub", i.dst, ["zero", a], form="rr"))
            else:
                out.append(MI("sltiu", i.dst, [a], 1, form="ri"))
        elif op == "load":
            size, off = i.k
            base = i.args[0]
            if not is_var(base) and fits(base + off):
                base, off = "zero", base + off
            base = self.reg(out, base)
            out.append(MI("lw" if size == 4 else "lbu", i.dst, [base], off, form="mem"))
        elif op == "store":
            size, off = i.k
            base, v = i.args
            if not is_var(base) and fits(base + off):
                base, off = "zero", base + off
            base = self.reg(out, base)
            v = self.reg(out, v)
            out.append(MI("sw" if size == 4 else "sb", None, [base, v], off, form="store"))
        elif op == "gaddr":
            out.append(MI("la", i.dst, [], label=i.k, form="la"))
        elif op == "faddr":
            out.append(MI("faddr", i.dst, ["sp"], i.k, form="faddr"))
        elif op == "getc":
            out.append(MI("lw", i.dst, ["zero"], IO_TAPE, form="mem"))
        elif op == "putc":
            v = self.reg(out, i.args[0])
            out.append(MI("sb", None, ["zero", v], IO_CONSOLE, form="store"))
        elif op == "call":
            regs = [self.reg(out, a) for a in i.args]
            for r, a in zip(regs, ARGS):
                out.append(MI("mv", a, [r], form="mv"))
            out.append(MI("call", None, ARGS[:len(regs)], label=i.k, clobbers=tuple(sorted(CALLER_SAVED)),
                          form="call"))
            if i.dst:
                out.append(MI("mv", i.dst, ["a0"], form="mv"))
        elif op == "br":
            if i.k != nxt:
                out.append(MI("j", label=i.k, form="j"))
        elif op == "cbr":
            a = self.reg(out, i.args[0])
            yes, no = i.k
            if yes == nxt:
                out.append(MI("beq", None, [a, "zero"], label=no, form="br"))
            else:
                out.append(MI("bne", None, [a, "zero"], label=yes, form="br"))
                if no != nxt:
                    out.append(MI("j", label=no, form="j"))
        elif op == "ret":
            if i.args:
                v = i.args[0]
                if is_var(v):
                    out.append(MI("mv", "a0", [v], form="mv"))
                else:
                    out.append(MI("addi", "a0", ["zero"], v, form="ri") if fits(v) else MI("li", "a0", [], v,
                                                                                         form="li"))
            out.append(MI("ret", None, ["a0"] if i.args else [], form="ret"))
        else:
            raise NotImplementedError(op)

    def binary(self, out, i: I):
        a, b = i.args
        k = i.k
        if not is_var(a) and k in ("add", "mul", "and", "or", "xor", "eq", "ne") and is_var(b):
            a, b = b, a
        imm_ops = {"add": "addi", "and": "andi", "or": "ori", "xor": "xori", "shl": "slli", "shr": "srli",
                   "sar": "srai", "lt": "slti", "ltu": "sltiu"}
        rr_ops = {"add": "add", "sub": "sub", "mul": "mul", "div": "div", "rem": "rem", "and": "and", "or": "or",
                  "xor": "xor", "shl": "sll", "shr": "srl", "sar": "sra", "lt": "slt", "ltu": "sltu"}
        if k == "sub" and not is_var(b) and fits(-b):
            out.append(MI("addi", i.dst, [self.reg(out, a)], -b, form="ri"))
            return
        if k in imm_ops and not is_var(b) and fits(b):
            out.append(MI(imm_ops[k], i.dst, [self.reg(out, a)], b, form="ri"))
            return
        if k in rr_ops:
            out.append(MI(rr_ops[k], i.dst, [self.reg(out, a), self.reg(out, b)], form="rr"))
            return
        ra, rb = self.reg(out, a), self.reg(out, b)
        if k in ("gt", "gtu"):
            out.append(MI("slt" if k == "gt" else "sltu", i.dst, [rb, ra], form="rr"))
        elif k in ("le", "leu"):
            t = self.tmp()
            out.append(MI("slt" if k == "le" else "sltu", t, [rb, ra], form="rr"))
            out.append(MI("xori", i.dst, [t], 1, form="ri"))
        elif k in ("ge", "geu"):
            t = self.tmp()
            out.append(MI("slt" if k == "ge" else "sltu", t, [ra, rb], form="rr"))
            out.append(MI("xori", i.dst, [t], 1, form="ri"))
        elif k == "eq":
            t = ra if rb == "zero" else self.tmp()
            if rb != "zero":
                out.append(MI("xor", t, [ra, rb], form="rr"))
            out.append(MI("sltiu", i.dst, [t], 1, form="ri"))
        elif k == "ne":
            t = ra if rb == "zero" else self.tmp()
            if rb != "zero":
                out.append(MI("xor", t, [ra, rb], form="rr"))
            out.append(MI("sltu", i.dst, ["zero", t], form="rr"))
        else:
            raise NotImplementedError(k)


# comparison -> (branch, swap operands)
CMP_BRANCH = {"lt": ("blt", False), "ge": ("bge", False), "gt": ("blt", True), "le": ("bge", True),
              "eq": ("beq", False), "ne": ("bne", False), "ltu": ("bltu", False), "geu": ("bgeu", False),
              "gtu": ("bltu", True), "leu": ("bgeu", True)}
INVERT = {"blt": "bge", "bge": "blt", "beq": "bne", "bne": "beq", "bltu": "bgeu", "bgeu": "bltu"}


def select(f: Func) -> MFunc:
    return Selector(f).run()


# ---------------------------------------------------------------------------
# liveness and interference
# ---------------------------------------------------------------------------
def _tracked(r) -> bool:
    return r is not None and r not in ("zero", "sp")


def liveness(mf: MFunc):
    lab = {b.label: b for b in mf.blocks}
    lin = {b.label: set() for b in mf.blocks}
    lout = {b.label: set() for b in mf.blocks}
    ud = {}
    for b in mf.blocks:
        use, d = set(), set()
        for m in b.ins:
            for r in m.uses():
                if _tracked(r) and r not in d:
                    use.add(r)
            for r in m.defs():
                if _tracked(r):
                    d.add(r)
        ud[b.label] = (use, d)
    changed = True
    while changed:
        changed = False
        for b in reversed(mf.blocks):
            out = set()
            for s in b.succs:
                out |= lin[s]
            inn = ud[b.label][0] | (out - ud[b.label][1])
            if out != lout[b.label] or inn != lin[b.label]:
                lout[b.label], lin[b.label] = out, inn
                changed = True
    return lin, lout


def interference(mf: MFunc):
    lin, lout = liveness(mf)
    adj: dict = {}
    moves: dict = {}

    def edge(a, b):
        if a == b or not _tracked(a) or not _tracked(b):
            return
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    for b in mf.blocks:
        live = set(lout[b.label])
        for m in reversed(b.ins):
            ds = [r for r in m.defs() if _tracked(r)]
            for r in m.uses():
                if _tracked(r):
                    adj.setdefault(r, set())
            for d in ds:
                adj.setdefault(d, set())
                for l in live:
                    if m.is_move() and l == m.rs[0]:
                        continue
                    edge(d, l)
            if m.is_move() and _tracked(m.rs[0]):
                moves.setdefault(m.rd, set()).add(m.rs[0])
                moves.setdefault(m.rs[0], set()).add(m.rd)
            for d in ds:
                live.discard(d)
            for r in m.uses():
                if _tracked(r):
                    live.add(r)
    return adj, moves


def loop_depths(mf: MFunc) -> dict:
    """Blocks inside loops (a crude depth: the number of back edges whose span contains the block)."""
    order = [b.label for b in mf.blocks]
    pos = {l: i for i, l in enumerate(order)}
    depth = {l: 0 for l in order}
    for b in mf.blocks:
        for s in b.succs:
            if pos[s] <= pos[b.label]:
                for l in order[pos[s]:pos[b.label] + 1]:
                    depth[l] += 1
    return depth


# ---------------------------------------------------------------------------
# colouring
# ---------------------------------------------------------------------------
def color(mf: MFunc, k_regs=ALLOCATABLE, no_spill=frozenset()):
    adj, moves = interference(mf)
    nodes = [n for n in adj if n not in PHYS]
    K = len(k_regs)
    depth = loop_depths(mf)
    cost = {n: 0.0 for n in nodes}
    for b in mf.blocks:
        w = 10 ** min(depth[b.label], 4)
        for m in b.ins:
            for r in m.uses() + m.defs():
                if r in cost:
                    cost[r] += w
    deg = {n: len(adj[n]) for n in nodes}
    removed = set()
    stack = []
    work = set(nodes)
    while work:
        low = [n for n in work if deg[n] < K]
        if low:
            n = min(low, key=lambda x: (deg[x], x))
        else:
            n = min(work, key=lambda x: (float("inf") if x in no_spill else cost[x] / max(deg[x], 1), x))
        work.discard(n)
        removed.add(n)
        stack.append(n)
        for m in adj[n]:
            if m in deg:
                deg[m] -= 1
    colors = {r: r for r in PHYS}
    spills = []
    while stack:
        n = stack.pop()
        taken = {colors[m] for m in adj[n] if m in colors}
        ok = [r for r in k_regs if r not in taken]
        if not ok:
            spills.append(n)
            continue
        pref = [colors[m] for m in moves.get(n, ()) if m in colors and colors[m] in ok]
        colors[n] = pref[0] if pref else ok[0]
    return {n: c for n, c in colors.items() if n not in PHYS}, spills, adj


def spill_rewrite(mf: MFunc, spills: list, fresh) -> set:
    """Each spilled register gets a stack slot; every use loads into a fresh register, every def stores one."""
    new_regs = set()
    for s in spills:
        mf.spill_slots[s] = len(mf.spill_slots)
    sp = set(spills)
    for b in mf.blocks:
        out = []
        for m in b.ins:
            pre, post = [], []
            rs = []
            for r in m.rs:
                if r in sp:
                    t = fresh()
                    new_regs.add(t)
                    pre.append(MI("lw", t, ["sp"], ("spill", r), form="mem"))
                    rs.append(t)
                else:
                    rs.append(r)
            m.rs = rs
            if m.rd in sp:
                t = fresh()
                new_regs.add(t)
                post.append(MI("sw", None, ["sp", t], ("spill", m.rd), form="store"))
                m.rd = t
            out += pre + [m] + post
        b.ins = out
    return new_regs


def coalesce(mf: MFunc, k_regs=ALLOCATABLE, protect=frozenset()) -> int:
    """Conservative coalescing: merge the two ends of a move when they do not interfere and the merge cannot make
    the graph harder to colour: Briggs's test (fewer than k neighbours of significant degree) for two virtual
    registers, George's test (every neighbour of the virtual register already interferes with, or is of low degree
    than, the physical one) when one end is physical."""
    K = len(k_regs)
    merged = 0
    while True:
        adj, moves = interference(mf)
        alias = {}
        done = set()
        for b in mf.blocks:
            for m in b.ins:
                if not m.is_move():
                    continue
                a, c = m.rd, m.rs[0]
                if not (_tracked(a) and _tracked(c)) or a == c or a in done or c in done:
                    continue
                if a in PHYS and c in PHYS:
                    continue
                if c in adj.get(a, ()):
                    continue
                if a in PHYS or c in PHYS:
                    phys, v = (a, c) if a in PHYS else (c, a)
                    if phys not in k_regs or v in protect:
                        continue
                    if all(t in adj.get(phys, ()) or len(adj.get(t, ())) < K or t in PHYS
                           for t in adj.get(v, ())):
                        alias[v] = phys
                        done |= {v, phys}
                    continue
                if a in protect or c in protect:
                    continue
                nb = (adj.get(a, set()) | adj.get(c, set())) - {a, c}
                if sum(1 for t in nb if t in PHYS or len(adj.get(t, ())) >= K) < K:
                    alias[c] = a
                    done |= {a, c}
        if not alias:
            return merged
        merged += len(alias)
        for b in mf.blocks:
            keep = []
            for m in b.ins:
                if m.rd in alias:
                    m.rd = alias[m.rd]
                m.rs = [alias.get(r, r) for r in m.rs]
                if m.is_move() and m.rd == m.rs[0]:
                    continue
                keep.append(m)
            b.ins = keep


def remat_candidates(mf: MFunc) -> dict:
    """Registers defined once, by an instruction that can be recomputed anywhere (a constant or an address)."""
    defs: dict = {}
    for b in mf.blocks:
        for m in b.ins:
            for d in m.defs():
                defs.setdefault(d, []).append(m)
    out = {}
    for r, ms in defs.items():
        if r in PHYS or len(ms) != 1:
            continue
        m = ms[0]
        if m.form in ("la", "li") or (m.form == "ri" and m.op == "addi" and m.rs == ["zero"]) or m.form == "faddr":
            out[r] = m
    return out


def allocate(mf: MFunc, spill_all: bool = False, k_regs=ALLOCATABLE) -> MFunc:
    counter = [0]

    def fresh():
        counter[0] += 1
        return f"%r{counter[0]}"
    no_spill: set = set()
    rounds = 0
    total_spills = 0
    if spill_all:
        vregs = sorted({r for b in mf.blocks for m in b.ins for r in m.uses() + m.defs() if r not in PHYS})
        no_spill |= spill_rewrite(mf, vregs, fresh)
        total_spills = len(vregs)
    merged = 0
    remats = 0
    while True:
        rounds += 1
        if not spill_all:
            merged += coalesce(mf, k_regs, frozenset(no_spill))
        colors, spills, adj = color(mf, k_regs, frozenset(no_spill))
        if not spills:
            break
        rm = remat_candidates(mf)
        re = [r for r in spills if r in rm]
        st = [r for r in spills if r not in rm]
        if re:
            remats += len(re)
            no_spill |= rematerialize(mf, {r: rm[r] for r in re}, fresh)
        total_spills += len(st)
        if st:
            no_spill |= spill_rewrite(mf, st, fresh)
        if rounds > 20:
            raise RuntimeError("register allocation did not converge")
    mf.colors = colors
    mf.stats.update(rounds=rounds, spills=total_spills, remat=remats, coalesced=merged, nodes=len(colors),
                    edges=sum(len(v) for k, v in adj.items() if k not in PHYS) // 2)
    return mf


def rematerialize(mf: MFunc, which: dict, fresh) -> set:
    """Instead of spilling a constant or an address, recompute it right before each use."""
    new = set()
    for b in mf.blocks:
        out = []
        for m in b.ins:
            if m.rd in which and m is which[m.rd]:
                continue
            rs = []
            for r in m.rs:
                if r in which:
                    t = fresh()
                    new.add(t)
                    d = which[r]
                    out.append(MI(d.op, t, list(d.rs), d.imm, d.label, form=d.form))
                    rs.append(t)
                else:
                    rs.append(r)
            m.rs = rs
            out.append(m)
        b.ins = out
    return new


# ---------------------------------------------------------------------------
# frames and assembly
# ---------------------------------------------------------------------------
def cleanup(mf: MFunc) -> int:
    """After allocation: drop moves whose ends got the same register, forward branches through blocks that only
    jump (or are empty and fall through), drop jumps to the next block, and delete blocks nothing reaches."""
    col = lambda r: mf.colors.get(r, r)
    for b in mf.blocks:
        b.ins = [m for m in b.ins if not (m.is_move() and col(m.rd) == col(m.rs[0]))]
    removed = 0
    while True:
        order = [b.label for b in mf.blocks]
        fwd = {}
        for k, b in enumerate(mf.blocks):
            if k == 0:
                continue
            if not b.ins and k + 1 < len(order):
                fwd[b.label] = order[k + 1]
            elif len(b.ins) == 1 and b.ins[0].form == "j":
                fwd[b.label] = b.ins[0].label

        def final(l):
            seen = set()
            while l in fwd and l not in seen:
                seen.add(l)
                l = fwd[l]
            return l
        changed = False
        for k, b in enumerate(mf.blocks):
            for m in b.ins:
                if m.form in ("br", "j") and m.label in fwd:
                    new = final(m.label)
                    if new != m.label:
                        m.label = new
                        changed = True
            nxt = order[k + 1] if k + 1 < len(order) else None
            if b.ins and b.ins[-1].form == "j" and b.ins[-1].label == nxt:
                b.ins.pop()
                changed = True
            # a conditional branch over an unconditional jump: invert it
            if (len(b.ins) >= 2 and b.ins[-1].form == "j" and b.ins[-2].form == "br" and b.ins[-2].label == nxt):
                br, j = b.ins[-2], b.ins[-1]
                br.op, br.label = INVERT[br.op], j.label
                b.ins.pop()
                changed = True
        # recompute successors, delete unreachable blocks
        reach, stack = set(), [mf.blocks[0].label]
        lab = {b.label: (k, b) for k, b in enumerate(mf.blocks)}
        while stack:
            l = stack.pop()
            if l in reach:
                continue
            reach.add(l)
            k, b = lab[l]
            falls = not b.ins or b.ins[-1].form not in ("j", "ret")
            for m in b.ins:
                if m.form in ("br", "j"):
                    stack.append(m.label)
            if falls and k + 1 < len(mf.blocks):
                stack.append(mf.blocks[k + 1].label)
        if len(reach) < len(mf.blocks):
            removed += len(mf.blocks) - len(reach)
            mf.blocks = [b for b in mf.blocks if b.label in reach]
            changed = True
        if not changed:
            break
    return removed


def emit(mf: MFunc) -> str:
    col = lambda r: mf.colors.get(r, r)
    used_s = sorted({col(r) for b in mf.blocks for m in b.ins for r in m.defs() if col(r) in CALLEE_SAVED})
    # frame: [0 .. spills) [slots) [saved s) [ra]
    off = 0
    spill_off = {}
    for s, k in mf.spill_slots.items():
        spill_off[s] = off
        off += 4
    slot_off = {}
    for name, (size, align) in mf.slots.items():
        off = (off + align - 1) // align * align
        slot_off[name] = off
        off += size
    off = (off + 3) // 4 * 4
    save_off = {}
    for r in used_s:
        save_off[r] = off
        off += 4
    if mf.has_call:
        save_off["ra"] = off
        off += 4
    frame = (off + 15) // 16 * 16
    lines = [f"{mf.name}:"]
    if frame:
        lines.append(f"        addi sp, sp, -{frame}")
        for r, o in save_off.items():
            lines.append(f"        sw   {r}, {o}(sp)")

    def epilogue():
        e = []
        for r, o in save_off.items():
            e.append(f"        lw   {r}, {o}(sp)")
        if frame:
            e.append(f"        addi sp, sp, {frame}")
        return e
    count_moves = 0
    for b in mf.blocks:
        lines.append(f"{mf.name}.{b.label}:")
        for m in b.ins:
            rd = col(m.rd) if m.rd else None
            rs = [col(r) for r in m.rs]
            imm = m.imm
            if isinstance(imm, tuple) and imm[0] == "spill":
                imm = spill_off[imm[1]]
            f = m.form
            if f == "mv":
                if rd == rs[0]:
                    count_moves += 1
                    continue
                lines.append(f"        mv   {rd}, {rs[0]}")
            elif f == "ri":
                lines.append(f"        {m.op:<4} {rd}, {rs[0]}, {imm}")
            elif f == "rr":
                lines.append(f"        {m.op:<4} {rd}, {rs[0]}, {rs[1]}")
            elif f == "li":
                lines.append(f"        li   {rd}, {imm}")
            elif f == "la":
                lines.append(f"        la   {rd}, {m.label}")
            elif f == "mem":
                lines.append(f"        {m.op:<4} {rd}, {imm}({rs[0]})")
            elif f == "store":
                lines.append(f"        {m.op:<4} {rs[1]}, {imm}({rs[0]})")
            elif f == "faddr":
                lines.append(f"        addi {rd}, sp, {slot_off[imm]}")
            elif f == "br":
                lines.append(f"        {m.op:<4} {rs[0]}, {rs[1]}, {mf.name}.{m.label}")
            elif f == "j":
                lines.append(f"        j    {mf.name}.{m.label}")
            elif f == "call":
                lines.append(f"        call {m.label}")
            elif f == "ret":
                lines += epilogue()
                lines.append("        ret")
            else:
                raise NotImplementedError(f)
    mf.stats.update(frame=frame, saved=used_s, coalesced_moves=count_moves)
    return "\n".join(lines)


RUNTIME = """
_start: call main
        halt
alloc:  la   t0, _brk
        lw   t1, 0(t0)
        bnez t1, _have
        la   t1, _heap
_have:  addi a0, a0, 3
        andi a0, a0, -4
        add  t2, t1, a0
        sw   t2, 0(t0)
        mv   a0, t1
        ret
"""


def data_section(globals_: dict) -> str:
    out = ["        .align 4", "_brk:   .word 0"]
    for name, (size, align, init) in globals_.items():
        out.append(f"        .align {max(align, 4)}")
        if init is not None and size == 4:
            out.append(f"{name}: .word {init}")
        else:
            out.append(f"{name}: .space {size}")
    out += ["        .align 16", "_heap:"]
    return "\n".join(out)
