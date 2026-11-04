"""Precompute everything numerical in Part 6 of *Computer Science, Built* ("The Stored-Program Computer").

    python -m videos.cs.cs6.compute              # everything missing (a few minutes: the CPU is compiled once)
    python -m videos.cs.cs6.compute --force job

Results are cached in ``.cache/cs6/<name>.json``; scenes call ``load(name)``.  The CPU is
``explainer/cs/pebble/cpu.py``: Pebble-32 as one netlist of gates and flip-flops, run cycle by cycle by the compiled
evaluator (``fast.py``) and checked against the instruction-level emulator.

Items:
    isa        Pebble-32's formats and opcodes, example encodings bit by bit, and the comparison with RV32I
    control    the control unit's truth table (34 opcodes x 20 signals) and its two implementations
    cpu        the whole CPU counted: gates by block, NAND equivalents, flip-flops, depth and settled delay
    cosim      random programs on the gate-level CPU and on the emulator: identical state after every one
    programs   sum, Euclid, hello, the self-modifying sum, traced at gate level
    assembler  two passes over a small program: the symbol table, then the encoded listing
    tm         a Turing-machine interpreter in Pebble assembly, running the 2-, 3- and 4-state busy beavers
    job        the Job, version 0: a paragraph at gate level and a chapter on the emulator (identical); its exact
               cycle count for all thirty novels; ledger row 0
"""

from __future__ import annotations

import hashlib
import json
import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.pebble import assemble, run
from explainer.cs.pebble import cpu as C
from explainer.cs.pebble import isa as I
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.fast import Fast
from explainer.cs.pebble.randprog import random_program

CACHE = Cache("cs6")
load = CACHE.load
GATE_PS = 10  # one gate delay, as in Part 5's timing chapter
_CPU: dict = {}


def cpu(style: str = "table"):
    if style not in _CPU:
        s = C.build_cpu(style)
        _CPU[style] = (s, Fast(s))
    return _CPU[style]


def gate_run(src: str | bytes, tape: bytes = b"", mem_size: int = 1 << 20, trace: bool = False, style="table",
             max_steps: int = 10_000_000):
    s, f = cpu(style)
    image = src if isinstance(src, bytes) else assemble(src).image
    return C.GateMachine(s, image, tape=tape, mem_size=mem_size, fast=f, trace=trace).run(max_steps)


# ---------------------------------------------------------------------------
# the instruction set
# ---------------------------------------------------------------------------
EXAMPLES = [  # (source in context, which word, as shown)
    ("add a2, a0, a1", 0, "add a2, a0, a1"),
    ("addi a0, a0, -1", 0, "addi a0, a0, -1"),
    ("lw t0, 8(sp)", 0, "lw t0, 8(sp)"),
    ("sw t0, 8(sp)", 0, "sw t0, 8(sp)"),
    ("loop: addi a0, a0, -1\n addi a1, a1, 1\n bne a0, zero, loop", 2, "bne a0, zero, loop"),
    ("jal ra, f\n .space 396\nf: halt", 0, "jal ra, f"),
    ("lui t0, 74565", 0, "lui t0, 74565"),
]


def compute_isa() -> dict:
    ex = []
    for src, k, shown in EXAMPLES:
        w = int.from_bytes(assemble(src).image[4 * k:4 * k + 4], "little")
        ex.append({"src": shown, "word": w, "bits": format(w, "032b"), "fields": I.fields(w),
                   "fmt": I.FORMAT[I.decode(w).op]})
    ops = [{"code": k, "op": m, "fmt": f} for k, (m, f) in sorted(I.OPS.items()) if m not in I.M_EXT]
    rv = [  # (aspect, Pebble-32, RV32I), the comparison card
        ("registers", "16, r0 = 0", "32, x0 = 0"),
        ("register field", "4 bits", "5 bits"),
        ("opcode", "6 bits, one per instruction", "7 bits + funct3 + funct7"),
        ("immediates", "one contiguous field, 18 or 22 bits", "12 or 20 bits, scattered"),
        ("branch reach", r"$\pm$512 KiB", r"$\pm$4 KiB"),
        ("formats", "R, I, S, J", "R, I, S, B, U, J"),
        ("multiply, divide", "Part 7 (reserved)", "the M extension"),
        ("stop", r"\texttt{halt}", r"\texttt{ecall} to an OS"),
    ]
    return {"examples": ex, "ops": ops, "rv": rv, "reserved": I.RESERVED, "n_ops": len(ops)}


# ---------------------------------------------------------------------------
# control
# ---------------------------------------------------------------------------
def compute_control() -> dict:
    table = C.control_table()
    rows = [{"code": k, "op": I.OPS[k][0], "bits": [table[k][s] for s in C.SIGNALS]} for k in table]
    info = {}
    for style in ("table", "minimized"):
        s, _ = cpu(style)
        a, b = s.blocks["control"]
        info[style] = {"gates": b - a, "terms": s.control_info["terms"]}
    # microcode: the same table as a control store, one word per opcode
    store_bits = len(table) * len(C.SIGNALS)
    return {"signals": list(C.SIGNALS), "info_text": C.SIGNAL_INFO, "rows": rows, "styles": info,
            "store_words": len(table), "store_bits": store_bits, "word_bits": len(C.SIGNALS)}


# ---------------------------------------------------------------------------
# the whole CPU, counted
# ---------------------------------------------------------------------------
def compute_cpu() -> dict:
    s, f = cpu("table")
    blocks = {k: b - a for k, (a, b) in s.blocks.items()}
    cp = C.critical_path(s, samples=4096)
    nand = s.c.to_nand().size()
    logic_ps = cp["settle_max"] * GATE_PS
    period_ps = logic_ps + 40 + 30  # clock-to-Q and setup, as in Part 5
    s2, _ = cpu("minimized")
    return {"gates": s.c.size(), "counts": s.c.counts(), "blocks": blocks, "flip_flops": s.flip_flops,
            "nand": nand, "transistors_logic": 4 * nand, "transistors_ff": 24 * s.flip_flops,
            "depth": cp["depth"], "settle_max": cp["settle_max"], "settle_mean": cp["settle_mean"],
            "logic_ps": logic_ps, "period_ps": period_ps, "fmax_ghz": 1000 / period_ps,
            "gates_minimized": s2.c.size(), "compiled": f.compiled,
            "compare": [("Pebble-32 logic (NAND2 equivalents x 4)", 4 * nand), ("MOS 6502 (1975)", 3510),
                        ("Intel 8086 (1978)", 29000), ("Intel 80386 (1985)", 275000),
                        ("Apple M1 (2020), whole chip", 16_000_000_000)]}


# ---------------------------------------------------------------------------
# co-simulation
# ---------------------------------------------------------------------------
def compute_cosim(n: int = 300) -> dict:
    out = {}
    for style in ("table", "minimized"):
        s, f = cpu(style)
        agree = steps = 0
        t = time.time()
        for seed in range(n):
            p = assemble(random_program(seed))
            e = run(p, mem_size=8192)
            g = gate_run(p.image, mem_size=8192, style=style, max_steps=20000)
            ok = e.regs == g.regs and bytes(e.mem) == bytes(g.mem) and e.steps == g.steps and e.pc == g.pc
            agree += ok
            steps += e.steps
        out[style] = {"programs": n, "agree": agree, "instructions": steps, "seconds": time.time() - t}
    mix = {}
    for seed in range(50):
        m = run(assemble(random_program(seed)), mem_size=8192)
        for k, v in m.counts.items():
            mix[k] = mix.get(k, 0) + v
    return {"styles": out, "mix": mix, "example": random_program(7).split("\n")[:24]}


# ---------------------------------------------------------------------------
# programs, traced at gate level
# ---------------------------------------------------------------------------
def _trace(src: str, regs=(3, 4, 9), mem_size=4096, tape=b"", max_rows=400) -> dict:
    p = assemble(src)
    g = gate_run(p.image, tape=tape, mem_size=mem_size, trace=True)
    e = run(p, tape=tape, mem_size=mem_size, trace=True)
    lines = p.source_lines
    cur = [0] * 16
    cur[2] = mem_size
    rows = []
    for k, (lg, le) in enumerate(zip(g.log, e.log)):
        if le.reg:
            cur[le.reg[0]] = le.reg[1]
        if k < max_rows:
            rows.append({"pc": lg["pc"], "line": lines.get(lg["pc"], 0), "word": lg["word"],
                         "regs": [cur[r] for r in regs], "taken": lg["taken"], "wd": lg["wd"], "we": lg["we"]})
    same = g.regs == e.regs and g.steps == e.steps and bytes(g.output) == bytes(e.output)
    return {"source": src.strip("\n").split("\n"), "listing": [[a, w, s_] for a, w, s_ in p.listing],
            "rows": rows, "steps": g.steps, "regs": g.regs, "output": bytes(g.output).decode(errors="replace"),
            "same": same, "labels": p.labels}


def compute_programs() -> dict:
    from videos.cs.cs1.compute import EUCLID_ASM

    out = {"sum": _trace(P.SUM, regs=(3, 4)), "euclid": _trace(EUCLID_ASM, regs=(3, 4, 9)),
           "hello": _trace(P.HELLO, regs=(9, 3)), "selfmod": _trace(P.SELFMOD, regs=(4, 5, 9)),
           "array": _trace(P.ARRAY_SUM, regs=(3, 9, 10), max_rows=40)}
    # the self-modifying load: its word before and after each rewrite
    p = assemble(P.SELFMOD)
    e = run(p, trace=True, mem_size=4096)
    load = p.labels["load"]
    words = [s.mem[2] for s in e.log if s.mem and s.mem[0] == load]
    out["selfmod"]["load_words"] = [int.from_bytes(p.image[load:load + 4], "little")] + words
    out["selfmod"]["load_addr"] = load
    return out


# ---------------------------------------------------------------------------
# the assembler, two passes
# ---------------------------------------------------------------------------
def compute_assembler() -> dict:
    src = P.SUM
    p = assemble(src)
    pseudo = []
    for s_ in ("li a0, 10", "li t0, 74565", "mv a0, a1", "j loop", "bnez a0, loop", "call f", "ret", "la t0, msg"):
        name = next((n for n in ("loop", "f", "msg") if s_.endswith(n)), None)
        prog = assemble(f" {s_}\n{name}: halt" if name else f" {s_}")
        n_words = 2 if s_.startswith(("li", "la")) else 1
        pseudo.append({"src": s_, "out": [I.disasm(int.from_bytes(prog.image[k:k + 4], "little"), k,
                                                     prog.addr_labels) for k in range(0, 4 * n_words, 4)]})
    return {"source": src.strip("\n").split("\n"), "labels": p.labels,
            "listing": [[a, w, s_, I.disasm(w, a, p.addr_labels)] for a, w, s_ in p.listing], "pseudo": pseudo}


# ---------------------------------------------------------------------------
# a Turing machine on Pebble
# ---------------------------------------------------------------------------
def compute_tm() -> dict:
    from explainer.cs.turing import CHAMPIONS, TM

    out = {}
    for n in (2, 3, 4):
        t, S, ones, who, year = CHAMPIONS[n]
        src = P.tm_program(TM.parse(t))
        e = run(assemble(src))
        g = gate_run(src) if n <= 3 else None
        out[str(n)] = {"table": t, "steps": e.regs[3], "ones": e.regs[4], "want": [S, ones],
                       "pebble_steps": e.steps, "gate_same": (g.regs == e.regs and g.steps == e.steps) if g else None}
    out["source"] = P.TM_INTERP.strip("\n").split("\n")
    return out


# ---------------------------------------------------------------------------
# the Job, version 0
# ---------------------------------------------------------------------------
def novels() -> dict[int, str]:
    import videos.ai.ai1.compute as A

    out = {}
    for n in A.BOOKS:
        raw = A._download(A.GUTENBERG.format(n=n), A.BOOK_DIR / f"{n}.txt").read_text(encoding="utf-8",
                                                                                       errors="replace")
        out[n] = A.clean(A.strip_gutenberg(raw))
    return out


def compute_job() -> dict:
    import videos.ai.ai1.compute as A

    books = novels()
    pp = books[1342]
    i = pp.index("It is a truth universally acknowledged")
    j = pp.index("Mr. Bennet was among the earliest")  # the start of chapter 2
    chapter = pp[i:j].rstrip()
    para = chapter[:chapter.index("\n", 600)] if "\n" in chapter[600:] else chapter[:800]
    prog = assemble(P.JOB_V0)
    out = {}
    # a paragraph, gate by gate, and on the emulator
    tape = P.job_tape(para)
    t = time.time()
    g = gate_run(prog.image, tape=tape)
    tg = time.time() - t
    e = run(prog, tape=tape)
    out["paragraph"] = {"text": para, "bytes": len(tape), "steps": g.steps, "same": g.steps == e.steps and bytes(
        g.output) == bytes(e.output) and g.regs == e.regs, "output": bytes(g.output).decode(), "seconds": tg,
        "formula": P.job_cycles(P.job_features(tape))}
    # a chapter on the emulator
    tape = P.job_tape(chapter)
    t = time.time()
    e = run(prog, tape=tape)
    out["chapter"] = {"bytes": len(tape), "steps": e.steps, "output": bytes(e.output).decode(),
                      "reference": bytes(e.output) == P.job_reference(tape), "seconds": time.time() - t,
                      "formula": P.job_cycles(P.job_features(tape)), "counts": e.counts}
    # the formula checked on random passages, then applied to all thirty novels
    rng = np.random.default_rng(6)
    checks = []
    keys = list(books)
    for k in range(20):
        b = books[keys[int(rng.integers(len(keys)))]]
        L = int(rng.integers(200, 6000))
        o = int(rng.integers(0, len(b) - L))
        tp = P.job_tape(b[o:o + L])
        m = run(prog, tape=tp)
        checks.append([len(tp), m.steps, P.job_cycles(P.job_features(tp))])
    out["checks"] = checks
    full = P.job_tape("\n".join(books[n] for n in A.BOOKS))
    f = P.job_features(full)
    cyc = P.job_cycles(f)
    words = 3 * f["words"] - 4 * (f["words"] - f["distinct"]) + 9 * f["distinct"]
    share = {"scan": 6 * f["scanned"] + 9 * f["same_length"] + 8 * f["matched"],
             "read": 8 * f["bytes"] + f["caps"] + 4 * f["letters"] + (f["bytes"] - f["letters"]) + 4 * f["words"]}
    share["other"] = cyc - share["scan"] - share["read"]
    top = P.job_reference(full).decode()
    out["corpus"] = {"features": f, "cycles": cyc, "per_byte": cyc / f["bytes"], "share": share, "top": top,
                     "sha": hashlib.sha256(full).hexdigest()[:12], "books": len(books)}
    from explainer.cs.pebble import tech

    period = tech.single_cycle_period_ps(load("cpu")["settle_max"]) * 1e-12
    clocks = {"Z3 relays (5.3 Hz)": 5.3, "ENIAC (5,000 additions per second)": 5000.0, "1 GHz": 1e9,
              "single cycle": 1 / period}
    out["projections"] = {k: cyc / hz for k, hz in clocks.items()}
    out["clock_mhz"] = 1e-6 / period
    out["ledger"] = [{"part": 6, "label": r"Pebble, single cycle", "seconds": cyc * period, "cycles": cyc,
                      "clock_mhz": 1e-6 / period, "cycles_per_byte": cyc / f["bytes"]}]
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(out["ledger"], indent=1))
    return out


ITEMS = {
    "isa": compute_isa, "control": compute_control, "cpu": compute_cpu, "cosim": compute_cosim,
    "programs": compute_programs, "assembler": compute_assembler, "tm": compute_tm, "job": compute_job,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
