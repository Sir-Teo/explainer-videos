"""Precompute everything numerical in Part 13 of *Computer Science, Built* ("The Compiler").

    python -m videos.cs.cs13.compute              # everything missing
    python -m videos.cs.cs13.compute --force passes

Results are cached in ``.cache/cs13/<name>.json``; scenes call ``load(name)``.  The compiler is
``explainer/cs/lang/compiler/`` (check, lower, ir, interp, ssa, opt, codegen, driver, analysis, fuzz, superopt),
tested in tests/test_cs13_compiler.py.  Pebble numbers come from the emulator (instructions), the Part 7 pipeline
and the Part 8 out-of-order core (cycles); "this machine" numbers time gcc on the C Job of Part 10.

Items:
    pipeline   the Job through every stage: characters, tokens, tree, IR, SSA, machine code, bytes
    semantic   struct layouts, lookup's symbol table, and four type errors
    ir         three-address code and the control-flow graph of a small function
    dom        its dominators (iterations), dominator tree and dominance frontiers
    ssa        the same function in SSA form: φs at the frontiers
    dataflow   liveness, reaching definitions and available expressions, iteration by iteration
    opts       constant propagation and value numbering on small examples, before and after
    passes     the Job (array and list) with each pass switched on in turn: instructions, code size
    loops      the Job's natural loops; what LICM hoists; strength reduction's before and after
    isel       IR against the Pebble instructions chosen for it
    regalloc   interference and colouring of the small function; spills as registers shrink; chordality
    sched      list scheduling and branch prediction on Part 7's pipeline
    job        compiled against hand-written on the emulator and on Part 8's core; ledger row 5
    gcc        the C Job of Part 10 at gcc -O0 … -O3 on this machine
    fuzz       random programs, every level against the interpreter
    superopt   finite-test candidates separately proved by z3; incomplete search, no minimality certificate
    llvm       the same small function through clang: LLVM IR in SSA form and at -O2; LLVM's -O2 pass count
"""

from __future__ import annotations

import copy
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path

from explainer.ai.cache import Cache

COMPILER_ITEMS = frozenset(("pipeline", "semantic", "ir", "dom", "ssa", "dataflow", "opts", "passes",
                            "loops", "isel", "regalloc", "sched", "job", "fuzz"))


def compiler_data_revision():
    """Bind compiler measurements to this producer and the compiler implementation."""
    import hashlib
    from explainer.cs.lang.compiler import opt
    digest = hashlib.sha256()
    for source in [Path(__file__), *sorted(Path(opt.__file__).parent.glob("*.py"))]:
        digest.update(source.name.encode())
        digest.update(b"\0")
        digest.update(source.read_bytes())
    return digest.hexdigest()


def cache_current(name):
    path = CACHE.path(name)
    if not path.exists():
        return False
    if name not in COMPILER_ITEMS:
        return True
    try:
        return json.loads(path.read_text()).get("_compiler_data_revision") == compiler_data_revision()
    except (OSError, ValueError, AttributeError):
        return False


class CompilerCache(Cache):
    def save(self, name, out):
        if name in COMPILER_ITEMS:
            out = dict(out, _compiler_data_revision=compiler_data_revision())
        return super().save(name, out)

    def load(self, name):
        from explainer.cache_lock import cache_lock
        if name in COMPILER_ITEMS and not cache_current(name):
            with cache_lock(self.path(name)):
                if not cache_current(name):
                    self.save(name, ITEMS[name]())
        return super().load(name)

    def main(self, items, doc=None):
        # The regular CLI also checks revisions before declaring an item cached.
        import argparse
        from explainer.cache_lock import cache_lock
        parser = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("names", nargs="*", default=list(items))
        parser.add_argument("--force", action="store_true")
        args = parser.parse_args()
        self.items = items
        self.dir.mkdir(parents=True, exist_ok=True)
        for name in args.names:
            with cache_lock(self.path(name)):
                if self.path(name).exists() and cache_current(name) and not args.force:
                    print(f"  cached  {name}", flush=True)
                    continue
                start = time.monotonic()
                print(f"  compute {name} ...", flush=True)
                self.save(name, items[name]())
                print(f"  done    {name} in {time.monotonic() - start:.0f}s", flush=True)


CACHE = CompilerCache("cs13")


def load(name):
    # Resolve the instance dynamically: cached-only QA rejects stale input before upgrade.
    return CACHE.load(name)

DEMO = r"""
fn total(a: *int, n: int) -> int {
    var s: int = 0;
    var i: int = 0;
    while i < n {
        if a[i] > 0 { s = s + a[i]; } else { s = s - 1; }
        i = i + 1;
    }
    return s;
}

fn main() -> int {
    var xs: [6]int;
    xs[0] = 3; xs[1] = -2; xs[2] = 7; xs[3] = 0; xs[4] = -5; xs[5] = 4;
    return total(&xs[0], 6);
}
"""

CONST = r"""
fn f(x: int) -> int {
    var a: int = 4;
    var b: int = a * 8;
    var c: int = 0;
    if b > 16 { c = x + b; } else { c = x - 1; }
    return c * 2;
}

fn main() -> int { return f(10); }
"""

GVN = r"""
fn g(p: *int, i: int) -> int {
    var x: int = p[i] + i * 4;
    var y: int = i * 4 + 1;
    return x + y;
}

fn main() -> int { var a: [4]int; a[1] = 5; return g(&a[0], 1); }
"""


def _module(src, rotate=False):
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import check as C
    from explainer.cs.lang.compiler import lower as L
    prog = P.parse(src)
    return L.lower(prog, C.check(prog), rotate=rotate)


def _func_view(f) -> dict:
    return {"name": f.name, "params": f.params,
            "blocks": [{"label": b.label, "ins": [str(i) for i in b.ins], "succs": b.succs()} for b in f.blocks]}


def _tapes(n=6, lo=1500, hi=4000, seed=13):
    import numpy as np

    from explainer.cs.pebble import programs as PR
    from videos.cs.cs6.compute import novels
    books = novels()
    keys = sorted(books)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        b = books[keys[int(rng.integers(len(keys)))]]
        L = int(rng.integers(lo, hi))
        o = int(rng.integers(0, len(b) - L))
        out.append(PR.job_tape(b[o:o + L]))
    return out


def _chapter():
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs7.compute import job_chapter
    return PR.job_tape(job_chapter())


# ---------------------------------------------------------------------------
def compute_pipeline() -> dict:
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.lang.compiler import ssa as S

    toks = P.lex(P.JOB)
    prog = P.parse(P.JOB)
    m = _module(P.JOB, True)
    ir = sum(f.count() for f in m.funcs)
    blocks = sum(len(f.blocks) for f in m.funcs)
    phis = 0
    for f in m.funcs:
        st = {}
        S.to_ssa(f, st)
        phis += st["phis"]
    c = D.compile_program(P.JOB, 3)
    asm_lines = [l for l in c.asm.splitlines() if l.startswith("        ")]
    code_words = c.program.labels["_brk"] // 4
    return {"chars": len(P.JOB), "tokens": len(toks) - 1, "nodes": P.count_nodes(prog), "ir": ir, "blocks": blocks,
            "phis": phis, "ir_optimized": c.stats["ir_final"], "asm": code_words,
            "listing_lines": len(asm_lines), "bytes": code_words * 4,
            "code_count_scope": "32-bit instruction words before _brk, including the small runtime; "
                                "listing_lines counts indented source lines and is a different statistic",
            "functions": [f.name for f in m.funcs]}


def compute_semantic() -> dict:
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import check as C

    info = C.check(P.parse(P.JOB))
    info2 = C.check(P.parse(P.JOB_ARRAY))
    layouts = {}
    for i, name in ((info, "Node"), (info2, "Entry")):
        s = i.structs[name]
        layouts[name] = {"size": s.size, "fields": [[f, off, str(t)] for f, (off, t) in s.fields.items()]}
    syms = {k: str(v) for k, v in info.locals["lookup"].items()}
    errors = {}
    for src in ("fn main() -> int { var x: int = null; return 0; }",
                "fn main() -> int { return y; }",
                "fn main() -> int { var p: *int = null; return p.length; }",
                "fn f(a: int) -> int { return a; } fn main() -> int { return f(1, 2); }"):
        try:
            C.check(P.parse(src))
            errors[src] = "ok"
        except C.TypeError_ as e:
            errors[src] = str(e)
    return {"layouts": layouts, "lookup_symbols": syms, "globals": {k: str(v) for k, v in info.globals.items()},
            "errors": errors}


def compute_ir() -> dict:
    m = _module(DEMO)
    f = m.func("total")
    return {"source": DEMO.strip().splitlines()[:8], "func": _func_view(f), "count": f.count()}


def compute_dom() -> dict:
    from explainer.cs.lang.compiler import ssa as S
    m = _module(DEMO)
    f = m.func("total")
    idom, passes = S.dominators(f)
    df = S.frontiers(f, idom)
    big = _module(__import__("explainer.cs.lang.pebble_lang", fromlist=["JOB"]).JOB, True)
    rows = []
    for g in big.funcs:
        _, p = S.dominators(g)
        rows.append({"func": g.name, "blocks": len(g.blocks), "passes": p})
    return {"idom": idom, "passes": passes, "tree": S.dom_tree(idom), "frontiers": {k: sorted(v) for k, v in df.items()},
            "job": rows}


def compute_ssa() -> dict:
    from explainer.cs.lang.compiler import ssa as S
    m = _module(DEMO)
    f = m.func("total")
    before = _func_view(f)
    st = {}
    S.to_ssa(f, st)
    after = _func_view(f)
    phis = [(b.label, str(i)) for b in f.blocks for i in b.ins if i.op == "phi"]
    return {"before": before, "after": after, "phis": phis, "stats": st}


def compute_dataflow() -> dict:
    from explainer.cs.lang.compiler import analysis as AN
    m = _module(DEMO)
    f = m.func("total")
    IN, OUT, trace, rounds = AN.liveness(f)
    live = {"in": {k: sorted(v) for k, v in IN.items()}, "out": {k: sorted(v) for k, v in OUT.items()},
            "trace": [[l, sorted(i), sorted(o)] for l, i, o in trace], "visits": rounds}
    IN2, OUT2, tr2, r2 = AN.reaching(f)
    reach = {"in": {k: sorted(f"{d[2]}@{d[0]}" for d in v) for k, v in IN2.items()}, "updates": len(tr2),
             "visits": r2}
    IN3, OUT3, tr3, r3 = AN.available(f)
    avail = {"in": {k: [f"{a[1][0]} {a[0]} {a[1][1]}" for a in v] for k, v in IN3.items()}, "updates": len(tr3),
             "visits": r3}
    return {"liveness": live, "reaching": reach, "available": avail, "blocks": [b.label for b in f.blocks]}


def compute_opts() -> dict:
    from explainer.cs.lang.compiler import opt as O
    from explainer.cs.lang.compiler import ssa as S
    out = {}
    m = _module(CONST)
    f = m.func("f")
    S.to_ssa(f)
    out["sccp_before"] = _func_view(f)
    st = {}
    O.copyprop(f)
    O.sccp(f, st)
    O.copyprop(f)
    O.dce(f)
    from explainer.cs.lang.compiler.driver import thread_jumps
    out["sccp_after"] = _func_view(f)
    out["sccp_stats"] = st
    m = _module(GVN)
    g = m.func("g")
    S.to_ssa(g)
    O.copyprop(g)
    out["gvn_before"] = _func_view(g)
    n = O.gvn(g)
    O.dce(g)
    out["gvn_after"] = _func_view(g)
    out["gvn_removed"] = n
    return out


CONFIGS = [
    ("-O0: every value in memory", dict(level=0)),
    ("registers: graph colouring", dict(level=1)),
    ("+ loop inversion", dict(level=1, rotate=True)),
    ("+ SSA, copy propagation", dict(level=2, passes=("copyprop",))),
    ("+ constant propagation (SCCP)", dict(level=2, passes=("copyprop", "sccp", "copyprop"))),
    ("+ value numbering (GVN)", dict(level=2, passes=("copyprop", "sccp", "copyprop", "strength", "gvn"))),
    ("+ loop-invariant code motion", dict(level=2, passes=("copyprop", "sccp", "copyprop", "strength", "gvn",
                                                           "licm"))),
    ("+ induction-variable strength reduction", dict(level=2)),
    ("+ inlining", dict(level=3)),
]


def compute_passes() -> dict:
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.pebble import programs as PR
    from explainer.cs.pebble.asm import assemble
    from explainer.cs.pebble.emu import Machine

    tape = _chapter()
    ref = PR.job_reference(tape)
    hand = Machine(image=assemble(PR.JOB_V0).image, tape=tape).run(10 ** 9).steps
    rows = []
    for label, cfg in CONFIGS:
        r = {"label": label}
        for name, src in (("array", P.JOB_ARRAY), ("list", P.JOB)):
            c = D.compile_program(src, cfg["level"], passes=cfg.get("passes"), rotate=cfg.get("rotate"))
            m = D.run(c, tape)
            assert bytes(m.output) == ref, (label, name)
            r[name] = m.steps
            r[name + "_words"] = c.stats["code_words"] - 12     # the runtime's 12 words are not compiled code
        rows.append(r)
        print(r)
    return {"rows": rows, "hand": hand, "bytes": len(tape)}


def compute_loops() -> dict:
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.lang.compiler import opt as O
    from explainer.cs.lang.compiler import ssa as S

    m = _module(P.JOB_ARRAY, True)
    f = m.func("word")
    S.to_ssa(f)
    for p in ("copyprop", "sccp", "copyprop", "strength", "gvn"):
        getattr(O, p)(f, {}) if p == "sccp" else getattr(O, p)(f)
    loops = [{"header": h, "blocks": sorted(b), "latches": l} for h, b, l in O.natural_loops(f)]
    before = _func_view(f)
    st = {}
    O.licm(f, st)
    after_licm = _func_view(f)
    O.ivsr(f, st)
    O.sccp(f, {})
    O.copyprop(f)
    O.dce(f)
    after = _func_view(f)
    # the scan loop, as machine code, with and without strength reduction
    snippets = {}
    for label, passes in (("without", ("copyprop", "sccp", "copyprop", "strength", "gvn", "licm", "dce")),
                          ("with", None)):
        c = D.compile_program(P.JOB_ARRAY, 2, passes=passes)
        a = c.asm
        s = a.index("word:")
        e = a.index("printnum:")
        snippets[label] = [l.strip() for l in a[s:e].splitlines()]
    return {"loops": loops, "before": before, "after_licm": after_licm, "after": after, "stats": st,
            "asm": snippets}


def compute_isel() -> dict:
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import codegen as G
    from explainer.cs.lang.compiler import driver as D

    m = _module(P.JOB)
    f = m.func("same")
    ir = _func_view(f)
    mf = G.select(copy.deepcopy(f))
    pairs = []
    for b, mb in zip(f.blocks, mf.blocks):
        pairs.append({"label": b.label, "ir": [str(i) for i in b.ins],
                      "mi": [f"{x.op} {x.rd or ''} {', '.join(x.rs)} {x.imm if x.imm is not None else ''} "
                             f"{x.label or ''}".split() for x in mb.ins]})
    c = D.compile_program(P.JOB, 2)
    a = c.asm
    s = a.index("same:")
    e = a.index("lookup:")
    return {"ir": ir, "pairs": pairs, "asm": [l.strip() for l in a[s:e].splitlines()]}


def compute_regalloc() -> dict:
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import analysis as AN
    from explainer.cs.lang.compiler import codegen as G
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.lang.compiler import opt as O
    from explainer.cs.lang.compiler import ssa as S

    # the small function's interference graph, at the IR level, in SSA
    m = _module(DEMO, True)
    f = m.func("total")
    S.to_ssa(f)
    O.optimize(f)
    g = AN.interference_ssa(f)
    ok, order, _ = AN.is_chordal(g)
    col = AN.color_peo(g, order)
    demo = {"nodes": sorted(g), "edges": sorted({tuple(sorted((a, b))) for a in g for b in g[a]}),
            "colors": col, "chordal": ok, "omega": AN.max_clique_chordal(g), "func": _func_view(f)}
    # chordality of every Job function, in SSA and after leaving it
    chord = []
    hole = None
    for name in ("same", "lookup", "printnum", "report", "main"):
        mm = _module(P.JOB, True)
        ff = mm.func(name)
        S.to_ssa(ff)
        O.optimize(ff)
        gs = AN.interference_ssa(ff)
        cs = AN.is_chordal(gs)[0]
        S.from_ssa(ff)
        gn = AN.interference_ssa(ff)
        cn = AN.is_chordal(gn)[0]
        if not cn and hole is None:
            h = AN.find_hole(gn, 6)
            if h:
                hole = {"func": name, "cycle": h}
        chord.append({"func": name, "ssa_nodes": len(gs), "ssa_chordal": cs, "omega": AN.max_clique_chordal(gs),
                      "after_nodes": len(gn), "after_chordal": cn})
    # spills as the register file shrinks (the Job, -O2)
    from explainer.cs.pebble import programs as PR
    tape = _chapter()
    ref = PR.job_reference(tape)
    sweep = []
    for k in (13, 10, 8, 6, 5, 4):
        # keep the callee-saved registers (values live across calls need them) and drop caller-saved ones
        regs = [r for r in G.ALLOCATABLE if r not in G.CALLEE_SAVED][:k - 3] + G.CALLEE_SAVED
        c = _compile_with_regs(P.JOB, regs)
        mm2 = D.run(c, tape)
        assert bytes(mm2.output) == ref
        sweep.append({"k": k, "spills": c.stats["spills"], "steps": mm2.steps})
    return {"demo": demo, "chordal": chord, "hole": hole, "sweep": sweep}


def _compile_with_regs(src, regs):
    """Compile at -O2 with only the given registers allocatable (keeping s-registers for values across calls)."""
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import check as C
    from explainer.cs.lang.compiler import codegen as G
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.lang.compiler import lower as L
    from explainer.cs.pebble.asm import assemble

    prog = P.parse(src)
    m = L.lower(prog, C.check(prog), rotate=True)
    D.middle(m, 2)
    parts = [G.RUNTIME]
    spills = 0
    for f in m.funcs:
        mf = G.select(f)
        G.allocate(mf, k_regs=list(regs))
        G.cleanup(mf)
        parts.append(G.emit(mf))
        spills += mf.stats["spills"]
    parts.append(G.data_section(m.globals))
    asm = "\n".join(parts)
    return D.Compiled(asm, assemble(asm), m, {"spills": spills})


def compute_sched() -> dict:
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import analysis as AN
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.pebble import pipe
    from explainer.cs.pebble import predict as PD
    from explainer.cs.pebble import programs as PR
    from explainer.cs.pebble.asm import assemble

    tape = _tapes(1, 3000, 3001)[0]
    ref = PR.job_reference(tape)
    rows = []
    for name, src in (("array", P.JOB_ARRAY), ("list", P.JOB)):
        c = D.compile_program(src, 2)
        sasm, fixed = AN.schedule_asm(c.asm)
        for label, img in (("as compiled", c.program), ("scheduled", assemble(sasm))):
            for pred_name, pred in (("not taken", None), ("two-bit", PD.TwoBit()), ("tournament", PD.Tournament())):
                p = pipe.run(img, tape, predictor=pred)
                assert bytes(p.output) == ref
                rows.append({"job": name, "code": label, "predictor": pred_name, "cycles": p.cycles,
                             "instructions": p.retired, "cpi": p.cpi, "load_use": p.stats["load_use"],
                             "flush": p.stats["branch_flush"], "fixed": fixed})
    for pred_name, pred in (("not taken", None), ("two-bit", PD.TwoBit()), ("tournament", PD.Tournament())):
        p = pipe.run(assemble(PR.JOB_V0), tape, predictor=pred)
        rows.append({"job": "hand", "code": "hand-written", "predictor": pred_name, "cycles": p.cycles,
                     "instructions": p.retired, "cpi": p.cpi, "load_use": p.stats["load_use"],
                     "flush": p.stats["branch_flush"], "fixed": 0})
    return {"rows": rows, "bytes": len(tape)}


def compute_job() -> dict:
    """Instructions on the emulator over the Part 7 chapter, and cycles on Part 8's core over passages; ledger row
    5 prices the compiled Job (-O2, the array version: the same algorithm and data as row 3's hand-written program)
    at row 3's cost per hand-written cycle."""
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.pebble import jobv1
    from explainer.cs.pebble import programs as PR
    from explainer.cs.pebble.asm import assemble
    from explainer.cs.pebble.emu import Machine
    from videos.cs.cs8.compute import core

    tape = _chapter()
    ref = PR.job_reference(tape)
    emu = {"hand-written (Part 6)": Machine(image=assemble(PR.JOB_V0).image, tape=tape).run(10 ** 9).steps}
    from explainer.cs.pebble.link import load as lload
    _, exe = jobv1.build()
    mm = lload(exe, [], tape)
    mm.run(10 ** 9)
    assert bytes(mm.output) == ref
    emu["hand-written, linked (Part 11)"] = mm.steps
    for name, src in (("array", P.JOB_ARRAY), ("list", P.JOB)):
        for lv in (0, 1, 2, 3):
            c = D.compile_program(src, lv)
            m = D.run(c, tape)
            assert bytes(m.output) == ref
            emu[f"{name} -O{lv}"] = m.steps
    # cycles on the out-of-order core
    rows = []
    hand_img = assemble(PR.JOB_V0).image
    imgs = {lv: D.compile_program(P.JOB_ARRAY, lv).program.image for lv in (0, 2)}
    for t in _tapes(6, 1200, 2600):
        r = {"bytes": len(t)}
        h = core(hand_img, t)
        r["hand"] = h.cycles
        for lv, img in imgs.items():
            q = core(img, t)
            assert bytes(q.output) == PR.job_reference(t)
            r[f"O{lv}"] = q.cycles
            r[f"O{lv}_instr"] = q.committed
        r["hand_instr"] = h.committed
        rows.append(r)
        print(r)
    ratio = sum(r["O2"] for r in rows) / sum(r["hand"] for r in rows)
    ratio0 = sum(r["O0"] for r in rows) / sum(r["hand"] for r in rows)
    led = json.loads((Cache("cs10").dir / "ledger.json").read_text())[:5]
    row3 = led[3]
    seconds = row3["seconds"] * ratio
    led.append({"part": 13, "label": r"compiled, one core", "seconds": seconds, "cycles": row3["cycles"] * ratio,
                "clock_mhz": row3["clock_mhz"], "ratio_to_row3": ratio, "o0_seconds": row3["seconds"] * ratio0})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {"emulator": emu, "core": rows, "ratio": ratio, "ratio_o0": ratio0, "ledger": led,
            "chapter_bytes": len(tape)}


def compute_gcc() -> dict:
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs10.compute import JOB_C
    from videos.cs.cs6.compute import novels

    book = novels()[1342]
    tape = PR.job_tape(book)
    rows = []
    with tempfile.TemporaryDirectory() as d:
        src, txt = Path(d) / "job.c", Path(d) / "pp.txt"
        src.write_text(JOB_C)
        txt.write_bytes(tape)
        for lv in ("-O0", "-O1", "-O2", "-O3"):
            exe = Path(d) / f"job{lv}"
            subprocess.run(["gcc", lv, "-march=native", "-pthread", "-o", str(exe), str(src)], check=True)
            best = None
            for _ in range(3):
                out = subprocess.run([str(exe), str(txt), "1", "0"], check=True, capture_output=True,
                                     text=True).stdout.splitlines()
                s = sum(map(float, out[0].split()))
                best = s if best is None else min(best, s)
            asm = subprocess.run(["gcc", lv, "-march=native", "-S", "-o", "-", str(src)], capture_output=True,
                                 text=True).stdout
            find = asm.split("find:")[1].split(".size")[0] if "find:" in asm else ""
            rows.append({"level": lv, "seconds": best,
                         "find_lines": sum(1 for l in find.splitlines() if l.startswith("\t") and
                                           not l.strip().startswith("."))})
            print(rows[-1])
    ver = subprocess.run(["gcc", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    return {"rows": rows, "bytes": len(tape), "gcc": ver}


def compute_fuzz() -> dict:
    from explainer.cs.lang.compiler import fuzz as F

    from collections import Counter

    ran = stuck = 0
    bad = []
    excluded = []
    t = time.time()
    sizes = []
    for seed in range(240):
        src = F.program(1000 + seed, funcs=3)
        sizes.append(src.count("\n"))
        r = F.differential(src, max_steps=3_000_000)
        if r["ok"] is None:
            stuck += 1
            excluded.append({"seed": 1000 + seed, "reason": r["ref"]})
            continue
        ran += 1
        if not r["ok"]:
            bad.append(seed)
    sample = F.program(1000, funcs=2).splitlines()
    return {"ran": ran, "stuck": stuck, "mismatches": bad, "seconds": time.time() - t,
            "lines": sum(sizes) / len(sizes), "sample": sample[:40],
            "reference_exclusions": excluded,
            "exclusion_counts": dict(Counter(row["reason"] for row in excluded)),
            "sampling": {"first_seed": 1000, "count": 240, "reference_step_limit": 3_000_000,
                         "compiled_step_limit": 24_000_000, "levels": [0, 1, 2, 3]},
            "historical_claim_scope": "The following source-coded development anecdotes are not findings of this run; "
                                      "directed load-hoisting regressions are separately documented and tested.",
            "found_during_development": [
                {"what": "a parameter assigned in the entry block was not renamed into SSA, so copy propagation "
                         "replaced uses that came before the assignment", "pass": "SSA construction",
                 "found_by": "seed 54 of the first run", "programs_failing": 9},
                {"what": "the interpreter assumed division by zero gives -1, as RISC-V does; Pebble traps",
                 "pass": "the reference semantics", "found_by": "the first run", "programs_failing": 73}]}


def compute_superopt() -> dict:
    import z3

    from explainer.cs.lang.compiler import superopt as SO

    s32 = SO.s32
    one = lambda: z3.BitVecVal(1, 32)
    zero = lambda: z3.BitVecVal(0, 32)
    targets = [
        ("x != 0", lambda x: int(x != 0), lambda x: z3.If(x != 0, one(), zero()), 1),
        ("x < 0", lambda x: int(s32(x) < 0), lambda x: z3.If(x < 0, one(), zero()), 1),
        ("x & (x - 1)", lambda x: x & (x - 1), lambda x: x & (x - 1), 1),
        ("x == y", lambda x, y: int(x == y), lambda x, y: z3.If(x == y, one(), zero()), 2),
        ("|x|", lambda x: abs(s32(x)), lambda x: z3.If(x < 0, -x, x), 1),
        ("sign(x)", lambda x: (s32(x) > 0) - (s32(x) < 0),
         lambda x: z3.If(x > 0, one(), z3.If(x < 0, -one(), zero())), 1),
        ("x / 2 (signed)", lambda x: int(s32(x) / 2), lambda x: x / 2, 1),
        ("min(x, y)", lambda x, y: min(s32(x), s32(y)), lambda x, y: z3.If(x < y, x, y), 2),
    ]
    rows = []
    for name, f, spec, ar in targets:
        t = time.time()
        n, progs = SO.search(f, ar, max_len=4 if name.startswith("min") else 3, limit=3)
        proofs = [SO.prove(p, spec, ar) for p in progs]
        good = [p for p, (ok, _) in zip(progs, proofs) if ok]
        rows.append({"name": name, "length": n, "found": len(progs), "proved": len(good),
                     "program": SO.show(good[0]) if good else None, "seconds": time.time() - t})
        print(rows[-1])
    rules = []
    for name, lhs, rhs in (
            ("x * 8 → x << 3", lambda x: x * 8, lambda x: x << 3),
            ("x / 2 → x >> 1", lambda x: x / 2, lambda x: x >> 1),
            ("x / 2 → (x + (x >>u 31)) >> 1", lambda x: x / 2, lambda x: (x + z3.LShR(x, 31)) >> 1),
            ("x + 1 > x → 1", lambda x: z3.If(x + 1 > x, one(), zero()), lambda x: one()),
            ("(x * 3) / 3 → x", lambda x: (x * 3) / 3, lambda x: x)):
        ok, cex = SO.check_rule(lhs, rhs)
        rules.append({"rule": name, "holds": ok, "counterexample": cex})
    return {"targets": rows, "rules": rules}


TOTAL_C = r"""
int total(int *a, int n) {
    int s = 0;
    for (int i = 0; i < n; i = i + 1) {
        if (a[i] > 0) s = s + a[i]; else s = s - 1;
    }
    return s;
}
"""


def compute_llvm() -> dict:
    """The same function through clang: LLVM IR after mem2reg (SSA, as ours), and at -O2; LLVM's -O2 pass list."""
    def clean(txt):
        out = []
        for l in txt.splitlines():
            if l.startswith(("define", "  ", "}")) or re.match(r"^\d+:", l):
                l = re.sub(r",? !\w+(\.\w+)? !\d+", "", l.split(";")[0]).rstrip()
                l = l.replace(" dso_local", "").replace(" noundef", "").replace(" #0", "").replace(
                    " local_unnamed_addr", "").replace(" nocapture", "").replace(" readonly", "")
                out.append(l)
        return out
    with tempfile.TemporaryDirectory() as d:
        c, ll0 = Path(d) / "total.c", Path(d) / "t0.ll"
        c.write_text(TOTAL_C)
        subprocess.run(["clang", "-O0", "-Xclang", "-disable-O0-optnone", "-emit-llvm", "-S", "-o", str(ll0), str(c)],
                       check=True)
        ssa = subprocess.run(["opt", "-passes=mem2reg", "-S", str(ll0)], check=True, capture_output=True,
                             text=True).stdout
        o2 = subprocess.run(["clang", "-O2", "-fno-vectorize", "-fno-unroll-loops", "-emit-llvm", "-S", "-o", "-",
                             str(c)], check=True, capture_output=True, text=True).stdout
        pipe = subprocess.run(["opt", "-O2", "-print-pipeline-passes", str(ll0), "-o", "/dev/null"],
                              capture_output=True, text=True).stdout
        ver = subprocess.run(["clang", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    flat = re.sub(r"<[^<>]*>", "", pipe)
    while re.search(r"<[^<>]*>", flat):
        flat = re.sub(r"<[^<>]*>", "", flat)
    names = [n for n in re.split(r"[,()]", flat) if n.strip() and not n.startswith(("function", "cgscc", "loop",
                                                                                    "devirt", "require",
                                                                                    "invalidate"))]
    return {"ssa": clean(ssa), "o2": clean(o2), "passes": len(names), "distinct": len(set(names)),
            "version": ver}


ITEMS = {
    "pipeline": compute_pipeline, "semantic": compute_semantic, "ir": compute_ir, "dom": compute_dom,
    "ssa": compute_ssa, "dataflow": compute_dataflow, "opts": compute_opts, "passes": compute_passes,
    "loops": compute_loops, "isel": compute_isel, "regalloc": compute_regalloc, "sched": compute_sched,
    "job": compute_job, "gcc": compute_gcc, "fuzz": compute_fuzz, "superopt": compute_superopt, "llvm": compute_llvm,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
