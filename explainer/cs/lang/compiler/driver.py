"""The Pebble compiler, end to end (Part 13): source text to an assembled Pebble program.

    out = compile_program(JOB, level=2)
    out.asm, out.program.image, out.stats
    m = run(out, tape)          # the emulator, with the compiled program

Levels:
    0   no optimization: every value in its own stack slot
    1   register allocation (graph colouring) on the code as lowered
    2   loops inverted; SSA, then copy propagation, SCCP, strength reduction, GVN, LICM, DCE; out of SSA;
        register allocation
    3   level 2 with inlining of small functions first

``passes`` overrides the level's pass list (for the pass-by-pass measurements).  ``target="os"`` (Part 31) compiles
for a user process under PebbleOS: ``getc`` and ``putc`` become calls into a small library that buffers them over
the ``read`` and ``write`` system calls, and ``main`` returning makes the ``exit`` call instead of halting.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field

from explainer.cs.lang import pebble_lang as P
from explainer.cs.lang.compiler import check as C
from explainer.cs.lang.compiler import codegen as G
from explainer.cs.lang.compiler import lower as L
from explainer.cs.lang.compiler import opt as O
from explainer.cs.lang.compiler import ssa as S
from explainer.cs.lang.compiler.ir import Module


@dataclass
class Compiled:
    asm: str
    program: object
    module: Module
    stats: dict = field(default_factory=dict)
    mfuncs: list = field(default_factory=list)


def thread_jumps(f) -> int:
    """Retarget branches to blocks that only jump onward, then delete those blocks."""
    fwd = {b.label: b.ins[0].k for b in f.blocks[1:] if len(b.ins) == 1 and b.ins[0].op == "br"
           and not any(i.op == "phi" for i in b.ins)}
    phis_at = {b.label for b in f.blocks if any(i.op == "phi" for i in b.ins)}

    def final(l, seen=()):
        while l in fwd and l not in seen and fwd[l] not in phis_at:
            seen += (l,)
            l = fwd[l]
        return l
    n = 0
    for b in f.blocks:
        t = b.ins[-1]
        if t.op == "br":
            new = final(t.k)
            n += new != t.k
            t.k = new
        elif t.op == "cbr":
            new = tuple(final(x) for x in t.k)
            n += new != t.k
            t.k = new
    from explainer.cs.lang.compiler.ir import remove_unreachable
    remove_unreachable(f)
    return n


def middle(m: Module, level: int, passes=None, stats=None) -> Module:
    stats = stats if stats is not None else {}
    if level >= 3:
        stats["inlined"] = O.inline(m)
    if level >= 2 or passes:
        for f in m.funcs:
            st = {}
            S.to_ssa(f, st)
            stats["phis"] = stats.get("phis", 0) + st.get("phis", 0)
            counts = O.optimize(f, passes or O.PIPELINE, stats)
            for k, v in counts.items():
                stats[k] = stats.get(k, 0) + v
            S.from_ssa(f)
    for f in m.funcs:
        thread_jumps(f)
    return m


def to_syscalls(m: Module) -> None:
    """getc and putc as calls to the user library (``__getc``, ``__putc``), for a process under PebbleOS."""
    from explainer.cs.lang.compiler.ir import I
    for f in m.funcs:
        for b in f.blocks:
            b.ins = [I("call", i.dst, [], "__getc") if i.op == "getc" else
                     I("call", None, list(i.args), "__putc") if i.op == "putc" else i for i in b.ins]


def compile_program(src: str | P.Program, level: int = 2, passes=None, rotate: bool | None = None,
                    target: str = "bare", origin: int = 0) -> Compiled:
    from explainer.cs.pebble.asm import assemble

    prog = P.parse(src) if isinstance(src, str) else copy.deepcopy(src)
    info = C.check(prog)
    m = L.lower(prog, info, rotate=level >= 2 if rotate is None else rotate)
    if target == "os":
        to_syscalls(m)
    stats: dict = {"ir_lowered": sum(f.count() for f in m.funcs)}
    middle(m, level, passes, stats)
    stats["ir_final"] = sum(f.count() for f in m.funcs)
    if target == "os":
        from explainer.cs.os.ulib import ULIB
        parts = [f".org {origin:#x}", ULIB]
    else:
        parts = [G.RUNTIME]
    mfs = []
    for f in m.funcs:
        mf = G.select(f)
        G.allocate(mf, spill_all=(level == 0))
        if level >= 1:
            G.cleanup(mf)
        parts.append(G.emit(mf))
        mfs.append(mf)
    parts.append(G.data_section(m.globals))
    asm = "\n".join(parts)
    prog_ = assemble(asm)
    stats["spills"] = sum(mf.stats["spills"] for mf in mfs)
    stats["words"] = len(prog_.image) // 4
    stats["code_words"] = (prog_.labels["_brk"]) // 4 if "_brk" in prog_.labels else None
    return Compiled(asm, prog_, m, stats, mfs)


def run(c: Compiled, tape: bytes = b"", **kw):
    from explainer.cs.pebble.emu import Machine
    max_steps = kw.pop("max_steps", 200_000_000)
    return Machine(image=c.program.image, tape=tape, **kw).run(max_steps)
