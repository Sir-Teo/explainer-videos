"""Precompute everything numerical in Part 7 of *Computer Science, Built* ("Pipelines").

    python -m videos.cs.cs7.compute              # everything missing (some minutes: predictors on long traces)
    python -m videos.cs.cs7.compute --force job

Results are cached in ``.cache/cs7/<name>.json``; scenes call ``load(name)``.  The pipeline is
``explainer/cs/pebble/pipe.py`` (cycle by cycle, checked against the emulator), the predictors ``predict.py``, the
technology (gate delay, flip-flops, memory) ``tech.py``.

Items:
    stages      the delay of each pipeline stage, from the netlists of Parts 4-6 and the memory; the clock
    ironlaw     the Job's first chapter on the single-cycle machine and on the pipeline; the MIPS myth (decimal
                printing by subtraction against div and rem)
    charts      pipeline charts (which instruction is in which stage, cycle by cycle) for the scenes
    hazards     CPI and its stall breakdown on the Job and the benchmarks, for each pipeline configuration;
                structural hazards: the divider, and a single memory port
    predictors  every predictor on the branch traces of the benchmarks and the Job; the 1-bit/2-bit FSMs on a loop
    perceptron  perceptron weights over branch history for chosen branches (the heatmap)
    btbras      recursive Fibonacci with no BTB, a BTB, and a BTB with a return-address stack
    depth       the optimal pipeline depth: the model against measured hazard rates; clock history
    sorted      the sorted-array puzzle on Pebble's pipeline and timed on this machine, with branchless versions
    amdahl      Amdahl's law curves; the Job's search share
    job         the Job, version 0, on the pipeline: CPI on passages, a fitted bubble model checked on a long
                passage, the corpus projection: ledger row 1
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.pebble import assemble, run
from explainer.cs.pebble import blocks as B
from explainer.cs.pebble import isa as I
from explainer.cs.pebble import predict as PR
from explainer.cs.pebble import programs as P
from explainer.cs.pebble import seq as S
from explainer.cs.pebble import tech
from explainer.cs.pebble.pipe import Pipeline

CACHE = Cache("cs7")
load = CACHE.load
BEST = PR.Tournament  # the predictor of the ledger's pipeline


def pebble7(image, tape=b"", mem_size=1 << 20, record=0, predictor=None, **kw) -> Pipeline:
    """The ledger's pipeline: forwarding, a 512-entry BTB, a 16-entry return-address stack, a tournament predictor."""
    return Pipeline(image, tape=tape, mem_size=mem_size, record=record,
                    predictor=BEST() if predictor is None else predictor, **kw).run()


def job_chapter() -> str:
    from videos.cs.cs6.compute import novels

    pp = novels()[1342]
    i = pp.index("It is a truth universally acknowledged")
    j = pp.index("Mr. Bennet was among the earliest")
    return pp[i:j].rstrip()


# ---------------------------------------------------------------------------
# stage delays and the clock
# ---------------------------------------------------------------------------
def _out_depth(c, name) -> int:
    lv = c.levels()
    return max(lv[w] for w in c.outputs[name])


def compute_stages() -> dict:
    alu = B.alu(32)
    rng = np.random.default_rng(1)
    n = 4096
    vals = {"a": rng.integers(0, 1 << 32, n, dtype=np.int64), "b": rng.integers(0, 1 << 32, n, dtype=np.int64),
            "op": rng.integers(0, 10, n)}
    vals["a"][:16], vals["b"][:16], vals["op"][:16] = 0xFFFFFFFF, 1, 0  # a carry the whole way
    alu_t = int(np.max(alu.settle(vals)))
    rf = S.register_file()
    read = _out_depth(rf.c, "a")
    mult = B.tree_multiplier(32, "dadda")
    mv = {"a": rng.integers(0, 1 << 32, 1024, dtype=np.int64), "b": rng.integers(0, 1 << 32, 1024, dtype=np.int64)}
    mul_t = int(np.max(mult.settle(mv)))
    adder = B.prefix_adder(32)
    target = int(np.max(adder.settle({"a": vals["a"], "b": vals["b"], "cin": np.zeros(n, np.int64)})))
    from videos.cs.cs6.compute import load as load6

    ctl = 8  # the PLA's depth: an AND tree of six literals and an OR tree of up to 34 terms (Part 6)
    single = load6("cpu")["settle_max"]
    mux = 3  # a 2-way multiplexer, AND then OR after the inverted select
    G, M = tech.GATE_PS, tech.MEM_PS
    stages = {
        "IF": {"mem": M, "gates": mux, "note": "instruction memory; the next-pc multiplexer"},
        "ID": {"mem": 0, "gates": max(ctl, read) + 2, "note": "decode and register read, in parallel; hazard check"},
        "EX": {"mem": 0, "gates": 2 * mux + alu_t, "note": "forwarding and operand multiplexers, then the ALU"},
        "MEM": {"mem": M, "gates": 2 * mux, "note": "data memory; byte select and sign extension"},
        "WB": {"mem": 0, "gates": 2 * mux + 2, "note": "the write-back multiplexer; register file setup"},
    }
    for v in stages.values():
        v["ps"] = v["mem"] + v["gates"] * G
    longest = max(v["ps"] for v in stages.values())
    period = longest + tech.FF_PS
    single_ps = tech.single_cycle_period_ps(single)
    return {"stages": stages, "alu_gates": alu_t, "read_gates": read, "mul_gates": mul_t, "target_gates": target,
            "period_ps": period, "mhz": tech.mhz(period), "single_ps": single_ps, "single_mhz": tech.mhz(single_ps),
            "clock_ratio": single_ps / period, "ff_ps": tech.FF_PS, "gate_ps": G, "mem_ps": M,
            "mul_fits": mul_t * G + 2 * mux * G <= longest}


# ---------------------------------------------------------------------------
# the iron law, and the MIPS myth
# ---------------------------------------------------------------------------
def compute_ironlaw() -> dict:
    st = load("stages")
    tape = P.job_tape(job_chapter())
    e = run(assemble(P.JOB_V0), tape=tape)
    q = pebble7(assemble(P.JOB_V0).image, tape=tape)
    rows = {
        "single": {"instructions": e.steps, "cpi": 1.0, "period_ps": st["single_ps"]},
        "pipeline": {"instructions": q.retired, "cpi": q.cpi, "period_ps": st["period_ps"]},
    }
    for r in rows.values():
        r["seconds"] = r["instructions"] * r["cpi"] * r["period_ps"] * 1e-12
    myth = {}
    for use_div in (False, True):
        p = assemble(P.decimal(2000, use_div))
        m = pebble7(p.image, mem_size=1 << 16)
        secs = m.cycles * st["period_ps"] * 1e-12
        myth["div" if use_div else "subtract"] = {"instructions": m.retired, "cycles": m.cycles, "cpi": m.cpi,
                                                  "seconds": secs, "mips": m.retired / secs / 1e6,
                                                  "divide_stalls": m.stats["divide"]}
    return {"rows": rows, "speedup": rows["single"]["seconds"] / rows["pipeline"]["seconds"], "myth": myth,
            "myth_numbers": 2000}


# ---------------------------------------------------------------------------
# pipeline charts for the scenes
# ---------------------------------------------------------------------------
CHART_PROGRAMS = {
    "ideal": "li a0, 1\nli a1, 2\naddi a2, zero, 3\naddi a3, zero, 4\naddi a4, zero, 5\naddi a5, zero, 6\nhalt",
    "forward": "li a0, 5\nadd a1, a0, a0\nsub a2, a1, a0\nand a3, a2, a1\nor a4, a3, a2\nhalt",
    "loaduse": "li s0, 0x400\nlw a0, 0(s0)\nadd a1, a0, a0\nsw a1, 4(s0)\nhalt",
    "branch": "li a0, 3\nloop: addi a0, a0, -1\nbne a0, zero, loop\naddi a1, zero, 7\nhalt",
    "divide": "li a0, 1000\nli a1, 7\ndiv a2, a0, a1\nadd a3, a2, a2\naddi a4, zero, 1\nhalt",
}


def _chart(src, cycles=40, forwarding=True, predictor=None, btb=512):
    p = assemble(src)
    q = Pipeline(p.image, mem_size=4096, record=cycles, forwarding=forwarding, predictor=predictor,
                 btb_entries=btb).run(10000)
    info = {str(k): {"pc": v[0], "text": I.disasm(v[1], v[0], p.addr_labels) if (v[1] >> 26) in I.OPS else "?",
                     "flushed": v[2]} for k, v in q.seqinfo.items()}
    return {"chart": q.chart, "seq": info, "cycles": q.cycles, "retired": q.retired, "stats": q.stats}


def compute_charts() -> dict:
    out = {k: _chart(v) for k, v in CHART_PROGRAMS.items()}
    out["noforward"] = _chart(CHART_PROGRAMS["forward"], forwarding=False)
    out["branch_predicted"] = _chart(CHART_PROGRAMS["branch"], predictor=PR.TwoBit())
    # the Job's inner loop, a few entries scanned
    tape = b"It is a truth universally acknowledged, that a single man in possession of a good fortune"
    p = assemble(P.JOB_V0)
    q = Pipeline(p.image, tape=tape, record=100000, predictor=BEST()).run()
    scan = p.labels["scan"]
    fetched = [c for c, r in enumerate(q.chart) if r["IF"] is not None and q.seqinfo[r["IF"]][0] == scan
               and not q.seqinfo[r["IF"]][2]]
    # a run of entries that differ in length: one scan-loop trip every 7 cycles, four times running
    i = next(k for k in range(len(fetched) - 4) if all(fetched[k + j + 1] - fetched[k + j] == 7 for j in range(4)))
    first = fetched[i]
    sub = q.chart[first:first + 26]
    seqs = {s for r in sub for k in ("IF", "ID", "EX", "MEM", "WB") for s in [r[k]] if s is not None}
    info = {str(s): {"pc": q.seqinfo[s][0], "text": I.disasm(q.seqinfo[s][1], q.seqinfo[s][0], p.addr_labels),
                     "flushed": q.seqinfo[s][2]} for s in seqs}
    out["scan"] = {"chart": sub, "seq": info}
    return out


# ---------------------------------------------------------------------------
# hazards: CPI breakdowns
# ---------------------------------------------------------------------------
CONFIGS = {
    "no forwarding, no prediction": dict(forwarding=False, predictor=None, btb_entries=0, ras_depth=0),
    "forwarding": dict(forwarding=True, predictor=None, btb_entries=0, ras_depth=0),
    "+ BTB, 2-bit": dict(forwarding=True, predictor="2bit", btb_entries=512, ras_depth=0),
    "+ tournament, RAS": dict(forwarding=True, predictor="best", btb_entries=512, ras_depth=16),
}


def benchmarks() -> dict[str, tuple[str, bytes]]:
    rng = np.random.default_rng(7)
    data = rng.integers(0, 256, 3000)
    return {
        "insertion sort": (P.insertion_sort(rng.integers(-10 ** 6, 10 ** 6, 250)), b""),
        "sieve": (P.sieve(8000), b""),
        "threshold, random": (P.threshold(data, 2), b""),
        "threshold, sorted": (P.threshold(np.sort(data), 2), b""),
        "Fibonacci (recursive)": (P.fib(18), b""),
        "correlated branches": (P.correlated(6000), b""),
        "the Job, chapter 1": (P.JOB_V0, P.job_tape(job_chapter())),
    }


def _pred(name):
    return {"2bit": PR.TwoBit, "best": BEST}.get(name, lambda: None)()


def compute_hazards() -> dict:
    out = {}
    for bname, (src, tape) in benchmarks().items():
        img = assemble(src).image
        rows = {}
        for cname, cfg in CONFIGS.items():
            c = dict(cfg)
            c["predictor"] = _pred(c["predictor"])
            q = Pipeline(img, tape=tape, mem_size=1 << 20, **c).run()
            s = q.stats
            n = q.retired
            rows[cname] = {"cpi": q.cpi, "instructions": n, "cycles": q.cycles,
                           "parts": {"base": 1.0 + 4 / n, "load-use": s["load_use"] / n, "data (no forwarding)":
                                     s["raw"] / n, "branches": s["branch_flush"] / n,
                                     "jumps": (s["jump_redirect"] + s["jalr_flush"]) / n, "divide": s["divide"] / n},
                           "mispredicts": s["mispredicts"], "branches": s["branches"]}
        out[bname] = rows
    # structural hazards
    dep = "li a0, 1000000\nli a1, 3\n" + "div a0, a0, a1\n" * 8 + "halt"
    ind = "li a0, 1000000\nli a1, 3\n" + "".join(f"div a{2 + (k % 3)}, a0, a1\naddi t{k % 3}, t{k % 3}, 1\n"
                                                for k in range(8)) + "halt"
    st = {}
    for name, src in (("eight dependent divides", dep), ("divides between other work", ind)):
        q = Pipeline(assemble(src).image, mem_size=4096).run()
        st[name] = {"cycles": q.cycles, "instructions": q.retired, "divide_stalls": q.stats["divide"]}
    # a single memory port: every load or store would also stall a fetch
    tape = P.job_tape(job_chapter())
    e = run(assemble(P.JOB_V0), tape=tape)
    mem_ops = sum(e.counts.get(k, 0) for k in ("lw", "lb", "lbu", "sw", "sb"))
    st["one memory port, the Job"] = {"memory_fraction": mem_ops / e.steps}
    return {"benchmarks": out, "structural": st, "configs": list(CONFIGS)}


# ---------------------------------------------------------------------------
# predictors on traces
# ---------------------------------------------------------------------------
def trace_of(src, tape=b"") -> tuple[list, dict, int]:
    p = assemble(src)
    m = run(p, tape=tape, trace=True)
    tr, back = [], {}
    for s in m.log:
        if s.taken is not None:
            tr.append((s.pc, bool(s.taken)))
            if s.pc not in back:
                back[s.pc] = I.decode(s.word).imm < 0
    return tr, back, m.steps


def compute_predictors() -> dict:
    table = {}
    names = None
    for bname, (src, tape) in benchmarks().items():
        tr, back, steps = trace_of(src, tape)
        row = {}
        for p in PR.all_predictors(back):
            t = time.time()
            acc = PR.accuracy(p, tr)
            row[p.name] = {"accuracy": acc, "mpki": (1 - acc) * len(tr) / steps * 1000, "seconds": time.time() - t}
        names = list(row)
        table[bname] = {"rows": row, "branches": len(tr), "instructions": steps}
    # the 1-bit and 2-bit counters on a loop of ten
    pattern = [k % 10 != 9 for k in range(40)]
    fsm = {}
    for p in (PR.OneBit(), PR.TwoBit()):
        states, preds = [], []
        for t in pattern:
            states.append(int(p.t[0]))
            preds.append(bool(p.predict(0)))
            p.update(0, t)
        fsm[p.name] = {"states": states, "predictions": preds}
    return {"table": table, "predictors": names, "fsm": fsm, "pattern": pattern}


def compute_perceptron() -> dict:
    out = {}
    for bname, pick in (("correlated branches", "b_no"), ("the Job, chapter 1", "scan"),
                        ("insertion sort", "inner")):
        src, tape = benchmarks()[bname]
        p = assemble(src)
        tr, _, _ = trace_of(src, tape)
        pc_counts: dict[int, int] = {}
        for pc, _ in tr:
            pc_counts[pc] = pc_counts.get(pc, 0) + 1
        if bname == "correlated branches":
            target = p.labels["b_no"] - 8  # branch B: the beqz two instructions before the label
        elif bname == "insertion sort":
            target = p.labels["inner"] + 8  # bge a0, a1
        else:
            target = p.labels["scan"] + 8  # bne t1, a1, next
        per = PR.Perceptron(h=16)
        two = PR.TwoBit()
        right_p = right_2 = n = 0
        for pc, t in tr:
            if pc == target:
                right_p += per.predict(pc) == t
                right_2 += two.predict(pc) == t
                n += 1
            per.update(pc, t)
            two.update(pc, t)
        out[bname] = {"weights": per.weights(target).tolist(), "pc": target,
                      "text": I.disasm(int.from_bytes(p.image[target:target + 4], "little"), target, p.addr_labels),
                      "perceptron": right_p / max(n, 1), "two_bit": right_2 / max(n, 1), "count": n,
                      "theta": per.theta}
    return out


def compute_btbras() -> dict:
    img = assemble(P.fib(18)).image
    out = {}
    for name, kw in (("no BTB", dict(btb_entries=0, ras_depth=0)), ("BTB", dict(btb_entries=512, ras_depth=0)),
                     ("BTB and return stack", dict(btb_entries=512, ras_depth=16))):
        q = Pipeline(img, mem_size=1 << 16, predictor=BEST(), **kw).run()
        out[name] = {"cycles": q.cycles, "cpi": q.cpi, "jalr": q.stats["jalr"], "jalr_miss": q.stats["jalr_miss"],
                     "jump_redirect": q.stats["jump_redirect"], "mispredicts": q.stats["mispredicts"],
                     "instructions": q.retired}
    return out


# ---------------------------------------------------------------------------
# the optimal depth
# ---------------------------------------------------------------------------
def compute_depth() -> dict:
    st = load("stages")
    hz = load("hazards")["benchmarks"]["the Job, chapter 1"]["+ tournament, RAS"]
    L = st["single_ps"] - tech.FF_PS  # all the work of one instruction, in ps
    o = tech.FF_PS
    b = hz["mispredicts"] / hz["instructions"]  # events whose cost grows with the depth
    ks = np.arange(1, 81)
    t = (L / ks + o) * (1 + b * (ks - 1))
    kstar = float(np.sqrt(L * (1 - b) / (b * o)))
    history = [  # approximate top clock rates of desktop processors (vendor specifications)
        (1993, 66, "Pentium"), (1995, 200, "Pentium Pro"), (1997, 300, "Pentium II"), (1999, 600, "Pentium III"),
        (2000, 1500, "Pentium 4"), (2002, 3060, "Pentium 4"), (2004, 3800, "Pentium 4 (Prescott)"),
        (2006, 2930, "Core 2"), (2008, 3200, "Core i7"), (2011, 3500, "Core i7"), (2013, 3900, "Core i7"),
        (2017, 4700, "Core i7"), (2020, 5300, "Core i9"), (2022, 5800, "Core i9"), (2023, 6000, "Core i9")]
    stages = [("Pentium (1993)", 5), ("Pentium 4, Willamette (2000)", 20), ("Pentium 4, Prescott (2004)", 31),
              ("Core 2 (2006)", 14)]
    return {"L_ps": L, "o_ps": o, "b": b, "k": ks.tolist(), "time_ps": t.tolist(), "kstar": kstar,
            "t_at_5": float((L / 5 + o) * (1 + b * 4)), "t_at_kstar": float(np.min(t)), "history": history,
            "stages": stages}


# ---------------------------------------------------------------------------
# the sorted-array puzzle
# ---------------------------------------------------------------------------
C_SRC = r"""
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 32768
static unsigned char data[N];
static int cmp(const void *a, const void *b) { return *(const unsigned char *)a - *(const unsigned char *)b; }
__attribute__((noinline)) long branchy(int reps) {
    long sum = 0;
    for (int r = 0; r < reps; r++)
        for (int i = 0; i < N; i++)
            if (data[i] >= 128) sum += data[i];
    return sum;
}
__attribute__((noinline)) long branchless(int reps) {
    long sum = 0;
    for (int r = 0; r < reps; r++)
        for (int i = 0; i < N; i++) {
            long x = data[i];
            sum += x & -(long)(x >= 128);
        }
    return sum;
}
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
int main(int argc, char **argv) {
    int reps = atoi(argv[1]);
    srand(1);
    for (int i = 0; i < N; i++) data[i] = rand() & 255;
    double t0 = now(); long a = branchy(reps); double t1 = now(); long b = branchless(reps); double t2 = now();
    qsort(data, N, 1, cmp);
    double t3 = now(); long c = branchy(reps); double t4 = now(); long d = branchless(reps); double t5 = now();
    printf("%f %f %f %f %ld %ld %ld %ld\n", t1 - t0, t2 - t1, t4 - t3, t5 - t4, a, b, c, d);
    return 0;
}
"""


def _host_cpu() -> str:
    try:
        for ln in Path("/proc/cpuinfo").read_text().splitlines():
            if ln.startswith("model name"):
                return ln.split(":", 1)[1].strip()
    except OSError:
        pass
    return "this machine"


def compute_sorted() -> dict:
    rng = np.random.default_rng(3)
    data = rng.integers(0, 256, 3000)
    peb = {}
    for name, d, br in (("random", data, False), ("sorted", np.sort(data), False), ("random, branchless", data, True),
                        ("sorted, branchless", np.sort(data), True)):
        q = pebble7(assemble(P.threshold(d, 2, br)).image, mem_size=1 << 16)
        peb[name] = {"cycles": q.cycles, "cpi": q.cpi, "instructions": q.retired, "mispredicts": q.stats["mispredicts"],
                     "branches": q.stats["branches"], "sum": q.regs[3]}
    host = {"cpu": _host_cpu()}
    with tempfile.TemporaryDirectory() as td:
        c = Path(td) / "s.c"
        c.write_text(C_SRC)
        exe = Path(td) / "s"
        flags = ["-O1", "-fno-if-conversion", "-fno-if-conversion2", "-fno-tree-vectorize", "-fno-tree-loop-vectorize"]
        try:
            subprocess.run([os.environ.get("CC", "cc"), *flags, "-o", str(exe), str(c)], check=True,
                           capture_output=True)
            runs = []
            for _ in range(5):
                out = subprocess.run([str(exe), "300"], capture_output=True, text=True, check=True).stdout.split()
                runs.append([float(x) for x in out[:4]])
            med = np.median(np.array(runs), axis=0)
            host.update({"random": med[0], "random_branchless": med[1], "sorted": med[2], "sorted_branchless": med[3],
                         "ratio": med[0] / med[2], "flags": " ".join(flags), "reps": 300, "n": 32768,
                         "sums_agree": len(set(out[4:])) == 1})
        except (OSError, subprocess.SubprocessError) as err:
            host["error"] = str(err)
    return {"pebble": peb, "host": host}


def compute_amdahl() -> dict:
    ns = np.logspace(0, 3, 61)
    curves = {str(p): (1 / ((1 - p) + p / ns)).tolist() for p in (0.5, 0.9, 0.95, 0.99)}
    from videos.cs.cs6.compute import load as load6

    share = load6("job")["corpus"]["share"]
    cyc = load6("job")["corpus"]["cycles"]
    p = share["scan"] / cyc
    return {"n": ns.tolist(), "curves": curves, "job_scan_share": p, "job_limit": 1 / (1 - p)}


# ---------------------------------------------------------------------------
# the Job on the pipeline: ledger row 1
# ---------------------------------------------------------------------------
FEATURES = ("bytes", "letters", "caps", "words", "distinct", "scanned", "same_length", "matched")


def compute_job() -> dict:
    from videos.cs.cs6.compute import load as load6
    from videos.cs.cs6.compute import novels

    st = load("stages")
    books = novels()
    keys = list(books)
    rng = np.random.default_rng(11)
    prog = assemble(P.JOB_V0)
    rows = []
    for k in range(24):
        b = books[keys[int(rng.integers(len(keys)))]]
        L = int(rng.integers(400, 4000))
        o = int(rng.integers(0, len(b) - L))
        tape = P.job_tape(b[o:o + L])
        q = pebble7(prog.image, tape=tape)
        f = P.job_features(tape)
        rows.append({"bytes": L, "instructions": q.retired, "cycles": q.cycles, "bubbles": q.bubbles,
                     "stats": q.stats, "features": {k_: f[k_] for k_ in FEATURES}})
    X = np.array([[1.0] + [r["features"][k_] for k_ in FEATURES] for r in rows])
    y = np.array([r["bubbles"] for r in rows], float)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    # check the model where it matters: a passage four times longer than any used to fit it
    b = books[2701]
    o = len(b) // 3
    tape = P.job_tape(b[o:o + 16000])
    t = time.time()
    q = pebble7(prog.image, tape=tape)
    f = P.job_features(tape)
    pred = float(coef @ np.array([1.0] + [f[k_] for k_ in FEATURES]))
    check = {"bytes": len(tape), "bubbles": q.bubbles, "predicted": pred, "error": pred / q.bubbles - 1,
             "instructions": q.retired, "cpi": q.cpi, "seconds": time.time() - t}
    corpus = load6("job")["corpus"]
    fc = corpus["features"]
    bubbles = float(coef @ np.array([1.0] + [fc[k_] for k_ in FEATURES]))
    cycles = corpus["cycles"] + 4 + bubbles
    cpi = cycles / corpus["cycles"]
    seconds = cycles * st["period_ps"] * 1e-12
    row0 = load6("job")["ledger"][0]
    ledger = [row0, {"part": 7, "label": r"a pipeline", "seconds": seconds, "cycles": cycles, "cpi": cpi,
                     "clock_mhz": st["mhz"]}]
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(ledger, indent=1))
    passage_cpi = [r["cycles"] / r["instructions"] for r in rows]
    return {"samples": rows, "coef": dict(zip(["const", *FEATURES], coef.tolist())), "check": check,
            "corpus": {"instructions": corpus["cycles"], "bubbles": bubbles, "cycles": cycles, "cpi": cpi,
                       "seconds": seconds}, "ledger": ledger, "passage_cpi": [min(passage_cpi), max(passage_cpi)],
            "speedup": row0["seconds"] / seconds}


def _branch_acc(pred, tr, target):
    right = n = 0
    for pc, t in tr:
        if pc == target:
            right += pred.predict(pc) == t
            n += 1
        pred.update(pc, t)
    return right / max(n, 1)


def compute_frontier() -> dict:
    """The Frontier chapter: how close do real predictors come to the limit of what history can tell them?"""
    src, tape = benchmarks()["the Job, chapter 1"]
    tr, _, steps = trace_of(src, tape)
    tage = []
    for b in (6, 8, 10, 12, 14, 16):
        bits = 2 * (1 << 12) + 5 * (3 + 9 + 1) * (1 << b)  # base 2-bit table; per entry: counter, tag, useful bit
        tage.append({"index_bits": b, "kb": bits / 8 / 1024, "accuracy": PR.accuracy(PR.Tage(bits=b), tr)})
    perc = []
    for e in (64, 256, 1024, 4096):
        perc.append({"entries": e, "kb": e * 25 / 1024, "accuracy": PR.accuracy(PR.Perceptron(entries=e), tr)})
    ppm = PR.PPM(confidence=1)
    ppm_acc = PR.accuracy(ppm, tr)
    contexts = sum(len(c) for c in ppm.c)
    single = []
    for h in (0, 1, 2, 4, 6, 8, 12, 16, 24, 32):
        acc_in, ent = PR.in_sample(tr, h)
        single.append({"h": h, "online": PR.accuracy(PR.Unlimited(h), tr), "hindsight": acc_in, "entropy": ent})
    # the perceptron's blind spot: a branch that is the exclusive-or of two earlier ones
    psrc = P.parity(6000)
    ptr, _, _ = trace_of(psrc)
    target = assemble(psrc).labels["b_no"] - 8
    parity = {}
    for p in (PR.TwoBit(), PR.GShare(), PR.Tage(), PR.Perceptron(h=16), PR.PPM(confidence=1)):
        parity[p.name] = _branch_acc(p, ptr, target)
    per = PR.Perceptron(h=16)
    for pc, t in ptr:
        per.update(pc, t)
    return {"branches": len(tr), "instructions": steps, "tage": tage, "perceptron": perc,
            "ppm": {"accuracy": ppm_acc, "contexts": contexts, "lengths": list(ppm.lengths)}, "single": single,
            "parity": parity, "parity_weights": per.weights(target).tolist()}


ITEMS = {
    "stages": compute_stages, "ironlaw": compute_ironlaw, "charts": compute_charts, "hazards": compute_hazards,
    "predictors": compute_predictors, "perceptron": compute_perceptron, "btbras": compute_btbras,
    "depth": compute_depth, "sorted": compute_sorted, "amdahl": compute_amdahl, "job": compute_job,
    "frontier": compute_frontier,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
