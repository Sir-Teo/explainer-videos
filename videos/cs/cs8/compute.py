"""Precompute everything numerical in Part 8 of *Computer Science, Built* ("Out of Order").

    python -m videos.cs.cs8.compute              # everything missing (some minutes: the core on long traces)
    python -m videos.cs.cs8.compute --force job

Results are cached in ``.cache/cs8/<name>.json``; scenes call ``load(name)``.  The out-of-order core is
``explainer/cs/pebble/ooo.py`` (checked against the emulator in tests/test_cs8_ooo.py), the oracle scheduler of the
limit study ``limits.py``.  Unless an item says otherwise, the core is 4 wide with a 128-entry reorder buffer, a
64-entry issue queue, a 48-entry load/store queue, three cycles of decode, and Part 7's tournament predictor.

Items:
    hook        the Job's first chapter on Part 7's pipeline, on the core with an issue queue of one (in order), and
                out of order; reorder-buffer occupancy over the run; one cache miss, in order and out of order
    dataflow    four trips round the Job's scan loop as a dataflow graph: latencies, earliest start times, the
                critical path, and schedules at widths 1, 2, 4 and unlimited
    rename      true and false dependences counted on the Job's trace; the limit with and without renaming; a
                renaming example
    scoreboard  the textbook example (Hennessy and Patterson) on a CDC 6600-style scoreboard and on Tomasulo's
                algorithm, cycle by cycle
    rob         recorded timelines: four trips round the scan loop, and the precise divide by zero
    limits      Wall's study repeated on the Job: each idealization removed in turn; IPC against width and window
    sweep       the core's IPC on the Job against width and reorder-buffer size
    speculate   the core on the Job with no prediction, 2-bit, tournament and a perfect predictor: mispredictions,
                squashed work, wrong-path loads; a recorded misprediction
    memory      memory disambiguation three ways on the Job; a memory-order violation, recorded
    spectre     the bounds-check-bypass attack: every probe line's time in every round, the leaked bytes; the
                mitigations and their cost
    vliw        the scan loop list-scheduled into four-wide bundles, and software-pipelined
    risc        the Job's instruction mix; loads an x86 instruction could fold into a memory operand
    smt         two threads sharing one window (oracle scheduler): throughput against one thread
    job         the Job on the core: passages, a fitted model checked on a long passage, the corpus projection:
                ledger row 2
    frontier    value prediction in the limit study; the cost of secure speculation; the Spectre gadget against it
"""

from __future__ import annotations

import json
import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.pebble import assemble, run
from explainer.cs.pebble import predict as PR
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.isa import IO_CYCLES, decode
from explainer.cs.pebble.limits import LAT, Trace, schedule, trace
from explainer.cs.pebble.ooo import Cache as DCache
from explainer.cs.pebble.ooo import OutOfOrder
from explainer.cs.pebble.pipe import dest, sources

CACHE = Cache("cs8")
load = CACHE.load
BEST = PR.Tournament


def core(image, tape=b"", predictor=None, **kw) -> OutOfOrder:
    """The ledger's out-of-order core: 4 wide, a 128-entry ROB, a tournament predictor."""
    return OutOfOrder(image, tape=tape, predictor=BEST() if predictor is None else predictor, **kw).run()


def chapter_tape() -> bytes:
    from videos.cs.cs7.compute import job_chapter

    return P.job_tape(job_chapter())


def job_image() -> bytes:
    return assemble(P.JOB_V0).image


_TRACE = {}


def chapter_trace() -> Trace:
    if "t" not in _TRACE:
        _TRACE["t"] = trace(job_image(), tape=chapter_tape())
    return _TRACE["t"]


def _slice(tr: Trace, a: int, b: int) -> Trace:
    return Trace(tr.pc[a:b], tr.kind[a:b], tr.srcs[a:b], tr.dst[a:b], tr.addr[a:b], tr.taken[a:b],
                 tr.load_value[a:b])


def _text(image: bytes, pc: int) -> str:
    from explainer.cs.pebble.isa import disasm

    return disasm(int.from_bytes(image[pc:pc + 4], "little"), pc)


def _uop(u, image) -> dict:
    return {"seq": u.seq, "pc": u.pc, "text": _text(image, u.pc) if u.ins is not None else "?", "t": list(u.t),
            "squashed": u.squashed, "correct": u.k is not None, "op": u.op}


# ---------------------------------------------------------------------------
# the hook: in order against out of order
# ---------------------------------------------------------------------------
MISS = """
        li   s0, 0x40000
        li   s1, 0x800
        lw   a0, 0(s0)        # a cache miss: sixty cycles
        add  a1, a0, a0       # needs it
        addi a2, zero, 1
        addi a3, zero, 2
        add  a4, a2, a3
        sw   a4, 0(s1)
        addi a5, a4, 3
        sw   a5, 4(s1)
        lw   t0, 0(s1)
        add  t1, t0, a5
        sw   t1, 8(s1)
        addi t2, t1, 1
        halt
"""


def compute_hook() -> dict:
    from videos.cs.cs7.compute import load as load7

    img, tape = job_image(), chapter_tape()
    pipe = load7("ironlaw")["rows"]["pipeline"]
    ino = core(img, tape, iq_size=1)
    ooo = core(img, tape, occupancy=True)
    occ = np.frombuffer(ooo.occupancy, np.uint16)
    hist = np.bincount(occ, minlength=129)
    miss = {}
    p = assemble(MISS)
    for name, kw in (("in order", {"iq_size": 1}), ("out of order", {})):
        c = OutOfOrder(p.image, cache=DCache(), record=40, perfect_prediction=True, **kw).run()
        miss[name] = {"cycles": c.cycles, "timeline": [_uop(u, p.image) for u in c.timeline if not u.squashed]}
    return {"instructions": ooo.committed, "pipeline": {"cpi": pipe["cpi"], "cycles": pipe["cpi"] * pipe["instructions"],
                                                   "ipc": 1 / pipe["cpi"]}, "in_order": {
        "cycles": ino.cycles, "ipc": ino.ipc}, "ooo": {"cycles": ooo.cycles, "ipc": ooo.ipc, "stats": ooo.stats},
        "occupancy": {"hist": hist.tolist(), "mean": float(occ.mean()), "median": float(np.median(occ)),
                      "full": float((occ >= 128).mean()), "sample": occ[20000:20600].tolist()},
        "miss": miss}


# ---------------------------------------------------------------------------
# dataflow: four trips round the scan loop
# ---------------------------------------------------------------------------
def _scan_window(tr: Trace, trips: int = 4) -> int:
    """Where the trace first makes ``trips`` consecutive trips of the six-instruction scan (lengths differ)."""
    labels = assemble(P.JOB_V0).labels
    scan = labels["scan"]
    pcs = tr.pc
    want = [scan, scan + 4, scan + 8, labels["next"], labels["next"] + 4, labels["next"] + 8]
    n = len(want) * trips
    start = len(pcs) // 3
    for i in range(start, len(pcs) - n):
        if pcs[i] == scan and all(pcs[i + j] == want[j % 6] for j in range(n)):
            return i
    raise RuntimeError("no scan window")


def compute_dataflow() -> dict:
    tr = chapter_trace()
    img = job_image()
    i0 = _scan_window(tr, 4)
    n = 24
    sub = _slice(tr, i0, i0 + n)
    nodes, edges = [], []
    last = {}
    for i in range(n):
        for r in sub.srcs[i]:
            if r in last:
                edges.append([last[r], i, int(r)])
        if sub.dst[i]:
            last[int(sub.dst[i])] = i
        nodes.append({"text": _text(img, int(sub.pc[i])), "kind": sub.kind[i], "lat": LAT[sub.kind[i]]})
    asap = schedule(sub).start.tolist()
    finish = [asap[i] + nodes[i]["lat"] for i in range(n)]
    # the critical path: walk back from the instruction that finishes last
    end = int(np.argmax(finish))
    path = [end]
    while True:
        cur = path[-1]
        preds = [e[0] for e in edges if e[1] == cur and finish[e[0]] == asap[cur]]
        if not preds:
            break
        path.append(preds[0])
    path.reverse()
    widths = {}
    for w in (1, 2, 4, 8):
        s = schedule(sub, width=w)
        widths[str(w)] = {"cycles": s.cycles, "start": s.start.tolist()}
    s = schedule(sub)
    widths["inf"] = {"cycles": s.cycles, "start": s.start.tolist()}
    # the same window in order (each instruction starts no earlier than the one before it): Part 7's pipeline
    t, inorder = 0, []
    fin = {}
    for i in range(n):
        st = max([t] + [fin.get(e[0], 0) for e in edges if e[1] == i])
        inorder.append(st)
        fin[i] = st + nodes[i]["lat"]
        t = st + 1
    return {"nodes": nodes, "edges": edges, "asap": asap, "critical": path, "widths": widths,
            "in_order": {"start": inorder, "cycles": max(fin.values())}, "trips": 4}


# ---------------------------------------------------------------------------
# renaming
# ---------------------------------------------------------------------------
RENAME_SRC = [
    ("lw", "a0", ["s0"], "lw   a0, 0(s0)"),
    ("add", "a1", ["a0", "a0"], "add  a1, a0, a0"),
    ("lw", "a0", ["s1"], "lw   a0, 0(s1)"),
    ("add", "a2", ["a0", "a0"], "add  a2, a0, a0"),
    ("add", "a1", ["a1", "a2"], "add  a1, a1, a2"),
]


def compute_rename() -> dict:
    tr = chapter_trace()
    raw = war = waw = 0
    last_w: dict[int, int] = {}
    read_since: dict[int, bool] = {}
    for i in range(len(tr)):
        for r in tr.srcs[i]:
            if r in last_w:
                raw += 1
            read_since[r] = True
        d = int(tr.dst[i])
        if d:
            if read_since.get(d):
                war += 1
            if d in last_w:
                waw += 1
            last_w[d] = i
            read_since[d] = False
    lim = {"renamed": schedule(tr).ipc, "not renamed": schedule(tr, rename=False).ipc}
    # the example: dependences and the renamed form
    deps = []
    for j, (_, d, ss, _) in enumerate(RENAME_SRC):
        for i in range(j):
            di, si = RENAME_SRC[i][1], RENAME_SRC[i][2]
            if di in ss and not any(RENAME_SRC[k][1] == di for k in range(i + 1, j)):
                deps.append([i, j, "RAW", di])
            if d in si and not any(RENAME_SRC[k][1] == d for k in range(i + 1, j)):
                deps.append([i, j, "WAR", d])
            if d == di and not any(RENAME_SRC[k][1] == d for k in range(i + 1, j)):
                deps.append([i, j, "WAW", d])
    rat, free, renamed = {}, iter(range(20, 64)), []
    for op, d, ss, _ in RENAME_SRC:
        srcs = [rat.get(s, s) for s in ss]
        p = f"p{next(free)}"
        rat[d] = p
        renamed.append({"op": op, "dst": p, "srcs": srcs, "rat": dict(rat)})
    return {"counts": {"raw": raw, "war": war, "waw": waw, "instructions": len(tr)}, "limit": lim,
            "example": [s for *_, s in RENAME_SRC], "deps": deps, "renamed": renamed}


# ---------------------------------------------------------------------------
# scoreboard and Tomasulo on the textbook example
# ---------------------------------------------------------------------------
TEXTBOOK = [  # Hennessy and Patterson's example (L.D F6 ... ADD.D F6,F8,F2), in Pebble's registers
    ("lw", "a1", [], "lw   a1, 0(s0)"),
    ("lw", "a2", [], "lw   a2, 4(s1)"),
    ("mul", "a0", ["a2", "a3"], "mul  a0, a2, a3"),
    ("sub", "a4", ["a1", "a2"], "sub  a4, a1, a2"),
    ("div", "a5", ["a0", "a1"], "div  a5, a0, a1"),
    ("add", "a1", ["a4", "a2"], "add  a1, a4, a2"),
]
TEXTBOOK_LAT = {"lw": 1, "add": 2, "sub": 2, "mul": 10, "div": 40}
SB_UNIT = {"lw": "integer", "add": "add", "sub": "add", "mul": "mult", "div": "divide"}
SB_UNITS = {"integer": 1, "add": 1, "mult": 2, "divide": 1}


def scoreboard(prog=TEXTBOOK, lat=TEXTBOOK_LAT) -> list[dict]:
    """The CDC 6600's scoreboard as Hennessy and Patterson tell it: issue (in order, when a unit is free and no
    active instruction writes the same register), read operands (when no earlier active instruction will still write
    them), execute, write result (once no earlier instruction still has to read the old value)."""
    n = len(prog)
    st = [{"issue": None, "read": None, "exec": None, "write": None, "unit": None} for _ in range(n)]
    busy = {u: [] for u in SB_UNITS}  # unit -> instructions holding it
    c = 0
    nxt = 0
    while any(s["write"] is None for s in st):
        c += 1
        done_now = []
        # write result
        for i in range(n):
            s = st[i]
            if s["exec"] is not None and s["exec"] < c and s["write"] is None:
                d = prog[i][1]
                war = any(st[j]["issue"] is not None and (st[j]["read"] is None or st[j]["read"] >= c)
                          and d in prog[j][2] for j in range(i))
                if not war:
                    s["write"] = c
                    done_now.append(i)
        # execute completes
        for i in range(n):
            s = st[i]
            if s["read"] is not None and s["exec"] is None and s["read"] + lat[prog[i][0]] <= c:
                s["exec"] = s["read"] + lat[prog[i][0]]
        # read operands
        for i in range(n):
            s = st[i]
            if s["issue"] is not None and s["issue"] < c and s["read"] is None:
                ok = True
                for r in prog[i][2]:
                    for j in range(i):
                        if prog[j][1] == r and st[j]["issue"] is not None and (st[j]["write"] is None
                                                                              or st[j]["write"] >= c):
                            ok = False
                if ok:
                    s["read"] = c
        # issue
        if nxt < n:
            op, d, _, _ = prog[nxt]
            u = SB_UNIT[op]
            waw = any(prog[j][1] == d and st[j]["issue"] is not None and (st[j]["write"] is None or st[j]["write"] >= c)
                      for j in range(nxt))
            if len(busy[u]) < SB_UNITS[u] and not waw:
                st[nxt]["issue"] = c
                st[nxt]["unit"] = u
                busy[u].append(nxt)
                nxt += 1
        for u in busy:  # a unit is free the cycle after its instruction writes
            busy[u] = [i for i in busy[u] if st[i]["write"] is None or st[i]["write"] > c]
    return st


TOMA_RS = {"load": 3, "add": 3, "mult": 2}
TOMA_KIND = {"lw": "load", "add": "add", "sub": "add", "mul": "mult", "div": "mult"}


def tomasulo(prog=TEXTBOOK, lat=TEXTBOOK_LAT) -> dict:
    """Tomasulo's algorithm (the IBM 360/91): issue in order into a free reservation station, renaming each source to
    the station that will produce it; execute when both operands have arrived; broadcast on the one common data bus,
    which every station and the register file watch.  Returns the cycles and, cycle by cycle, the stations."""
    n = len(prog)
    st = [{"issue": None, "start": None, "exec": None, "write": None, "rs": None} for _ in range(n)]
    reg_tag: dict[str, int] = {}  # register -> instruction that will write it
    waits: list[dict] = [{} for _ in range(n)]  # source register -> producing instruction (None: value in hand)
    rs_use = {k: [] for k in TOMA_RS}
    names = {k: [f"{k.capitalize()}{j + 1}" for j in range(v)] for k, v in TOMA_RS.items()}
    snaps = []
    nxt, c = 0, 0
    while any(s["write"] is None for s in st):
        c += 1
        # write result: one broadcast a cycle, oldest first
        cand = [i for i in range(n) if st[i]["exec"] is not None and st[i]["exec"] < c and st[i]["write"] is None]
        bus = None
        woke = set()
        if cand:
            i = min(cand)
            st[i]["write"] = c
            bus = i
            for j in range(n):
                for r, p in waits[j].items():
                    if p == i:
                        waits[j][r] = None
                        woke.add(j)  # it may start next cycle
            for r in [r for r, p in reg_tag.items() if p == i]:
                del reg_tag[r]
        # execute
        for i in range(n):
            s = st[i]
            if s["issue"] is not None and s["start"] is None and s["issue"] < c and all(
                    p is None for p in waits[i].values()) and i not in woke:
                s["start"] = c
            if s["start"] is not None and s["exec"] is None and s["start"] + lat[prog[i][0]] - 1 <= c:
                s["exec"] = s["start"] + lat[prog[i][0]] - 1
        # issue
        if nxt < n:
            op, d, srcs, _ = prog[nxt]
            k = TOMA_KIND[op]
            if len(rs_use[k]) < TOMA_RS[k]:
                free = [nm for nm in names[k] if nm not in [st[i]["rs"] for i in rs_use[k]]]
                st[nxt]["issue"] = c
                st[nxt]["rs"] = free[0]
                waits[nxt] = {r: reg_tag.get(r) for r in srcs}
                reg_tag[d] = nxt
                rs_use[k].append(nxt)
                nxt += 1
        snaps.append({"cycle": c, "bus": bus, "stations": {st[i]["rs"]: {
            "i": i, "waits": {r: (None if p is None else st[p]["rs"]) for r, p in waits[i].items()},
            "running": st[i]["start"] is not None} for k in rs_use for i in rs_use[k]},
            "regs": {r: st[p]["rs"] for r, p in reg_tag.items()}})
        for k in rs_use:  # a station is free once its result is broadcast
            rs_use[k] = [i for i in rs_use[k] if st[i]["write"] is None or st[i]["write"] > c]
    return {"status": st, "snaps": snaps}


def compute_scoreboard() -> dict:
    sb = scoreboard()
    tm = tomasulo()
    return {"program": [p[3] for p in TEXTBOOK], "latency": TEXTBOOK_LAT, "scoreboard": sb,
            "tomasulo": tm["status"], "snaps": tm["snaps"], "units": SB_UNITS, "stations": TOMA_RS,
            "sb_cycles": max(s["write"] for s in sb), "tm_cycles": max(s["write"] for s in tm["status"])}


# ---------------------------------------------------------------------------
# the reorder buffer, recorded
# ---------------------------------------------------------------------------
DIVZERO = """
        li   a0, 11
        li   s0, 0x800
        sw   a0, 0(s0)
        li   a1, 0
        div  a2, a0, a1      # divide by zero
        addi a3, a0, 1
        add  a4, a3, a3
        sw   a4, 4(s0)       # must never reach memory
        addi a5, a4, 1
        halt
"""


def _record_scan(trips=4, **kw):
    """A recording of the core in the scan loop: find a window of consecutive trips, start recording there."""
    img, tape = job_image(), chapter_tape()
    probe = core(img, tape, record=200000, **kw)
    labels = assemble(P.JOB_V0).labels
    tl = [u for u in probe.timeline]
    scan = labels["scan"]
    want = [scan, scan + 4, scan + 8, labels["next"], labels["next"] + 4, labels["next"] + 8]
    good = [u for u in tl if not u.squashed]
    for a in range(len(good) // 2, len(good) - 6 * trips):
        if all(good[a + j].pc == want[j % 6] for j in range(6 * trips)):
            seq0 = good[a].seq
            seq1 = good[a + 6 * trips - 1].seq
            return [_uop(u, img) for u in tl if seq0 <= u.seq <= seq1]
    raise RuntimeError("no window")


def compute_rob() -> dict:
    p = assemble(DIVZERO)
    c = OutOfOrder(p.image, record=40).run()
    return {"scan": _record_scan(4), "divzero": {"timeline": [_uop(u, p.image) for u in c.timeline],
                                                  "error": c.error, "cycles": c.cycles,
                                                  "mem": [int.from_bytes(c.mem[0x800 + 4 * k:0x804 + 4 * k], "little")
                                                          for k in range(2)]}}


# ---------------------------------------------------------------------------
# Wall's limit study on the Job
# ---------------------------------------------------------------------------
def compute_limits() -> dict:
    tr = chapter_trace()
    t0 = time.time()
    ideal = schedule(tr)
    steps = [
        ("the oracle", {}),
        ("no renaming", {"rename": False}),
        ("memory: wait for every store", {"memory": "conservative"}),
        ("branches: a tournament predictor", {"branches": BEST()}),
        ("branches: no speculation", {"branches": "barrier"}),
    ]
    each = [{"name": nm, "ipc": schedule(tr, **kw).ipc} for nm, kw in steps]
    curves = {}
    for win in (32, 128, 512, 2048, None):
        row = []
        for w in (1, 2, 4, 8, 16, 32, 64):
            row.append(schedule(tr, width=w, window=win, branches=BEST()).ipc)
        curves[str(win or "inf")] = row
    perfect_br = {}
    for win in (128, 2048):
        perfect_br[str(win)] = [schedule(tr, width=w, window=win).ipc for w in (1, 2, 4, 8, 16, 32, 64)]
    return {"instructions": len(tr), "ideal": ideal.ipc, "ideal_cycles": ideal.cycles, "each": each,
            "widths": [1, 2, 4, 8, 16, 32, 64], "curves": curves, "perfect_branches": perfect_br,
            "seconds": time.time() - t0}


def compute_sweep() -> dict:
    img, tape = job_image(), chapter_tape()
    out = []
    for w in (1, 2, 4, 8):
        for rob in (16, 32, 64, 128, 256, 512):
            c = core(img, tape, width=w, rob_size=rob, iq_size=max(8, rob // 2), lsq_size=max(8, rob * 3 // 8))
            out.append({"width": w, "rob": rob, "ipc": c.ipc, "cycles": c.cycles})
    perfect = [core(img, tape, width=w, rob_size=512, iq_size=256, lsq_size=192, perfect_prediction=True).ipc
               for w in (1, 2, 4, 8)]
    return {"runs": out, "perfect_512": perfect}


# ---------------------------------------------------------------------------
# speculation
# ---------------------------------------------------------------------------
def compute_speculate() -> dict:
    img, tape = job_image(), chapter_tape()
    rows = {}
    for name, kw in (("always taken", {"predictor": PR.Always()}), ("2-bit", {"predictor": PR.TwoBit()}),
                     ("tournament", {}), ("perfect", {"perfect_prediction": True})):
        c = core(img, tape, **kw)
        rows[name] = {"cycles": c.cycles, "ipc": c.ipc, "stats": c.stats, "committed": c.committed}
    # one misprediction, recorded: the bne of the scan loop when a same-length entry turns up
    probe = core(img, tape, record=60000)
    labels = assemble(P.JOB_V0).labels
    bne = labels["scan"] + 8
    tl = probe.timeline
    for idx, u in enumerate(tl):
        if u.pc == bne and not u.squashed and u.k is not None and any(
                x.squashed and x.seq > u.seq for x in tl[idx + 1: idx + 6]) and idx > len(tl) // 2:
            window = [_uop(x, img) for x in tl[max(0, idx - 8): idx + 40]]
            break
    else:
        window = []
    return {"rows": rows, "mispredict": {"branch_seq": u.seq if window else None, "timeline": window}}


# ---------------------------------------------------------------------------
# memory disambiguation
# ---------------------------------------------------------------------------
VIOLATION = """
        li   s0, 0x800
        li   a0, 1000
        li   a1, 1000
        div  a2, a0, a1       # 1, after sixteen cycles
        slli a2, a2, 2
        add  a3, s0, a2       # 0x804: the store's address is known late
        li   a4, 77
        sw   a4, 0(a3)
        lw   a5, 4(s0)        # the same word
        addi t0, a5, 1
        halt
"""


HIST_N = 1500


def histogram_image(n: int = HIST_N, buckets: int = 64, seed: int = 3) -> tuple[str, bytes]:
    """Count samples into buckets, the samples one per cache line so that every one misses: the store's address
    depends on a load that takes sixty cycles, and the next sample's load comes right after it."""
    src = f"""
        li   s0, 0x20000      # the samples, one per 64-byte line
        li   s1, 0x1000       # the counts
        li   s2, {0x20000 + 64 * n}
loop:   lbu  a0, 0(s0)        # a sample: a cache miss
        slli a0, a0, 2
        add  a0, a0, s1
        lw   t0, 0(a0)        # count[sample]
        addi t0, t0, 1
        sw   t0, 0(a0)        # its address waits for the miss
        addi s0, s0, 64
        bne  s0, s2, loop
        halt
"""
    img = bytearray(assemble(src).image)
    img.extend(bytes(0x20000 + 64 * n - len(img)))
    vals = np.random.default_rng(seed).integers(0, buckets, n)
    for i, v in enumerate(vals):
        img[0x20000 + 64 * i] = int(v)
    return src, bytes(img)


def compute_memory() -> dict:
    img, tape = job_image(), chapter_tape()
    rows = {}
    for mode in ("conservative", "speculative", "wait-table"):
        c = core(img, tape, disambiguation=mode)
        rows[mode] = {"cycles": c.cycles, "ipc": c.ipc, "stats": c.stats}
    tr = chapter_trace()
    loads = sum(1 for k in tr.kind if k == "load")
    stores = sum(1 for k in tr.kind if k == "store")
    hsrc, himg = histogram_image()
    hist = {}
    for mode in ("conservative", "speculative", "wait-table"):
        c = core(himg, disambiguation=mode, cache=DCache())
        hist[mode] = {"cycles": c.cycles, "ipc": c.ipc, "violations": c.stats["violations"],
                      "forwarded": c.stats["forwarded"], "squashed": c.stats["squashed"]}
    p = assemble(VIOLATION)
    demo = {}
    for mode in ("conservative", "speculative"):
        c = OutOfOrder(p.image, disambiguation=mode, record=40).run()
        demo[mode] = {"cycles": c.cycles, "violations": c.stats["violations"], "a5": c.regs[8],
                      "timeline": [_uop(u, p.image) for u in c.timeline]}
    return {"rows": rows, "loads": loads, "stores": stores, "instructions": len(tr), "demo": demo,
            "histogram": {"n": HIST_N, "modes": hist, "source": hsrc}}


# ---------------------------------------------------------------------------
# Spectre
# ---------------------------------------------------------------------------
class TimedCore(OutOfOrder):
    """Log completed counter reads with their instruction address, including barriers."""

    def _load(self, u):
        result = super()._load(u)
        if result == "ok" and u.addr == IO_CYCLES:
            self.reads.append((u.pc, u.result))
        return result


def _spectre(secret, mitigation=None, secure=False, predictor=None):
    program = assemble(P.spectre(len(secret), mitigation))
    probe_sites = [pc for pc, word, _ in program.listing
                   if program.labels["time"] <= pc < program.labels["slower"] and decode(word).op == "lw"]
    assert len(probe_sites) == 2
    c = TimedCore(P.spectre_image(secret, mitigation), cache=DCache(), timer="cycles",
                  predictor=predictor or PR.TwoBit(), training="commit", secure=secure)
    c.reads = []
    c.run()
    # The fence adds counter reads in the training calls. Select the two actual
    # probe-measurement instructions instead of slicing every counter read.
    probe_reads = [(pc, value) for pc, value in c.reads if pc in probe_sites]
    assert len(probe_reads) == 2 * 255 * len(secret)
    assert all(pc == probe_sites[i % 2] for i, (pc, _) in enumerate(probe_reads))
    r = [value for _, value in probe_reads]
    per = 2 * 255
    rounds = []
    for k in range(len(secret)):
        blk = r[k * per:(k + 1) * per]
        rounds.append([blk[2 * j + 1] - blk[2 * j] for j in range(255)])
    return c, rounds


def compute_spectre() -> dict:
    secret = b"PEBBLE"
    c, rounds = _spectre(secret)
    out = {"secret": secret.decode(), "leaked": bytes(c.output).decode("latin-1"), "cycles": c.cycles,
           "rounds": rounds, "stats": c.stats}
    mit = {}
    for m in (None, "fence", "mask"):
        cc, rr = _spectre(secret, m)
        mit[str(m)] = {"output": list(cc.output), "cycles": cc.cycles, "fast": [int(np.argmin(x)) + 1 for x in rr]}
    cc, rr = _spectre(secret, secure=True)
    mit["secure"] = {"output": list(cc.output), "cycles": cc.cycles, "fast": [int(np.argmin(x)) + 1 for x in rr]}
    out["mitigations"] = mit
    # the victim's own cost: a benign loop calling it, with each guard
    out["victim_cost"] = _victim_cost()
    return out


def _victim_cost(n=2000) -> dict:
    res = {}
    for m in (None, "fence", "mask"):
        guard = {"fence": "        lw   t3, 8(a5)\n",
                 "mask": "        sltu t3, a0, t2\n        sub  t3, zero, t3\n        and  a0, a0, t3\n"}.get(m, "")
        src = f"""
        li   s0, {P.SPECTRE_ARRAY1}
        li   s1, {P.SPECTRE_SIZE}
        li   s2, {P.SPECTRE_PROBE}
        li   a5, 0xffff0000
        li   t0, {n}
        li   a3, 0
loop:   andi a0, t0, 15
        call victim
        add  a3, a3, t3
        addi t0, t0, -1
        bnez t0, loop
        halt
victim: lw   t2, 0(s1)
        bgeu a0, t2, out
{guard}        add  t3, s0, a0
        lbu  t3, 0(t3)
        slli t3, t3, 6
        add  t3, t3, s2
        lbu  t3, 0(t3)
out:    ret
"""
        img = bytearray(assemble(src).image)
        img.extend(bytes(max(0, P.SPECTRE_SIZE + 4 - len(img))))
        img[P.SPECTRE_SIZE:P.SPECTRE_SIZE + 4] = (16).to_bytes(4, "little")
        c = core(bytes(img), cache=DCache(), timer="cycles")
        res[str(m)] = {"cycles": c.cycles, "per_call": c.cycles / n, "ipc": c.ipc}
    return res


# ---------------------------------------------------------------------------
# VLIW: list scheduling and software pipelining of the scan loop
# ---------------------------------------------------------------------------
SCAN = [  # one trip, with the loop's own dependences (names: the registers the loop carries)
    ("beq  a2, s1, insert", "branch", ["a2"], None),
    ("lw   t1, 4(t0)", "load", ["t0"], "t1"),
    ("bne  t1, a1, next", "branch", ["t1"], None),
    ("addi t0, t0, 12", "alu", ["t0"], "t0"),
    ("addi a2, a2, 1", "alu", ["a2"], "a2"),
    ("j    scan", "jump", [], None),
]


def compute_vliw(width=4) -> dict:
    lat = {"branch": 1, "load": 2, "alu": 1, "jump": 1}
    # one trip as a basic block (the VLIW way, without unrolling): ops in dependence order, bundles of width
    n = len(SCAN)
    prod = {}
    start = [0] * n
    for i, (_, k, srcs, d) in enumerate(SCAN):
        t = 0
        for r in srcs:
            if r in prod:
                t = max(t, prod[r])
        start[i] = t
        if d:
            prod[d] = t + lat[k]
    # a jump ends the block; branches must not move above the load they test (they do not here)
    start[5] = max(start)  # the jump goes in the last bundle
    # the addis write t0 and a2, which the lw and beq read: they may share a bundle (reads see old values) but not
    # go earlier than their readers
    start[3] = max(start[3], start[1])
    start[4] = max(start[4], start[0])
    bundles = {}
    for i, t in enumerate(start):
        bundles.setdefault(t, []).append(i)
    block_len = max(start) + 1
    # software pipelining: the initiation interval is bounded by resources and by the loop-carried recurrence
    res_mii = -(-n // width)
    rec_mii = 1  # t0 -> t0 and a2 -> a2, one cycle each
    ii = max(res_mii, rec_mii)
    # a modulo schedule: each op at the earliest time not before its block time whose column modulo II still has a
    # free slot (the modulo reservation table); branches stay after the load they test
    mstart, mrt = [], {}
    for i, t in enumerate(start):
        while mrt.get(t % ii, 0) >= width:
            t += 1
        mrt[t % ii] = mrt.get(t % ii, 0) + 1
        mstart.append(t)
    if mstart[5] < mstart[2]:
        mstart[5] = mstart[2]
    kernel = {}
    for i, t in enumerate(mstart):
        kernel.setdefault(t % ii, []).append([i, t // ii])
    return {"ops": [s[0] for s in SCAN], "start": start, "bundles": {str(k): v for k, v in bundles.items()},
            "block_cycles": block_len, "slots": block_len * width, "nops": block_len * width - n, "width": width,
            "res_mii": res_mii, "rec_mii": rec_mii, "ii": ii, "stages": max(t // ii for t in mstart) + 1,
            "mstart": mstart,
            "kernel": {str(k): v for k, v in kernel.items()}}


# ---------------------------------------------------------------------------
# RISC against CISC: what the Job's trace looks like
# ---------------------------------------------------------------------------
def compute_risc() -> dict:
    tr = chapter_trace()
    mix = {}
    for k in tr.kind:
        mix[k] = mix.get(k, 0) + 1
    # a load whose value is used once, by the very next instruction, which then overwrites or discards it: an x86
    # instruction could take that operand from memory directly (add r, [m])
    fold = 0
    n = len(tr)
    for i in range(n - 1):
        if tr.kind[i] == "load" and tr.dst[i]:
            d = int(tr.dst[i])
            if d in tr.srcs[i + 1]:
                # dead after: overwritten by i+1 or by a later write before any read (check a short horizon)
                dead = int(tr.dst[i + 1]) == d
                j = i + 2
                while not dead and j < min(n, i + 12):
                    if d in tr.srcs[j]:
                        break
                    if int(tr.dst[j]) == d:
                        dead = True
                    j += 1
                fold += dead
    # compare-and-branch: Pebble's branches compare two registers in one instruction; x86 needs cmp + jcc (fused)
    img = job_image()
    code_bytes = len(assemble(P.JOB_V0).image)
    return {"mix": mix, "instructions": n, "foldable_loads": fold, "loads": mix.get("load", 0),
            "code_bytes": code_bytes, "static_instructions": code_bytes // 4, "image": len(img)}


# ---------------------------------------------------------------------------
# simultaneous multithreading, in the oracle scheduler
# ---------------------------------------------------------------------------
def smt(trs: list, width: int, window: int, predictor=BEST, penalty: int = 3, starts: bool = False):
    """Several threads share ``width`` issue slots a cycle; each has ``window`` instructions of the shared window and
    its own branch barriers (a misprediction stalls only its own thread).  Returns the total instructions per cycle."""
    from explainer.cs.pebble.limits import mispredicted

    states = []
    for tr in trs:
        states.append({"tr": tr, "wrong": mispredicted(tr, predictor()), "ready": [0] * 16, "store": {}, "floor": 0,
                       "start": np.zeros(len(tr), np.int64), "i": 0})
    used: dict[int, int] = {}
    finish = 0
    total = sum(len(t) for t in trs)
    while any(s["i"] < len(s["tr"]) for s in states):
        for s in states:
            i = s["i"]
            tr = s["tr"]
            if i >= len(tr):
                continue
            k = tr.kind[i]
            t = s["floor"]
            for r in tr.srcs[i]:
                t = max(t, s["ready"][r])
            if k == "load":
                t = max(t, s["store"].get(int(tr.addr[i]), 0))
            if i >= window:
                t = max(t, int(s["start"][i - window]))
            while used.get(t, 0) >= width:
                t += 1
            used[t] = used.get(t, 0) + 1
            s["start"][i] = t
            f = t + LAT[k]
            finish = max(finish, f)
            d = int(tr.dst[i])
            if d:
                s["ready"][d] = f
            if k == "store":
                s["store"][int(tr.addr[i])] = f
            if s["wrong"][i]:
                s["floor"] = max(s["floor"], f + penalty)
            s["i"] = i + 1
    if starts:
        return total / finish, [st["start"] for st in states]
    return total / finish


def compute_smt() -> dict:
    from videos.cs.cs6.compute import novels

    a = chapter_trace()
    b_text = novels()[2701]
    o = len(b_text) // 2
    b = trace(job_image(), tape=P.job_tape(b_text[o:o + 5000]))
    n = min(len(a), len(b))
    a, b = _slice(a, 0, n), _slice(b, 0, n)
    out = {}
    for w, win in ((4, 128), (8, 256)):
        one_a = schedule(a, width=w, window=win, branches=BEST()).ipc
        one_b = schedule(b, width=w, window=win, branches=BEST()).ipc
        two = smt([a, b], w, win // 2)
        out[f"{w}/{win}"] = {"one_a": one_a, "one_b": one_b, "two": two}
    # a picture of the issue slots: 24 cycles from the middle of a short stretch, alone and shared
    m = 6000
    a6, b6 = _slice(a, 0, m), _slice(b, 0, m)
    alone = schedule(a6, width=4, window=128, branches=BEST()).start
    _, both = smt([a6, b6], 4, 64, starts=True)
    c0 = int(alone[m // 2])
    slots_alone = [int(((alone >= c) & (alone < c + 1)).sum()) for c in range(c0, c0 + 24)]
    c1 = int(both[0][m // 2])
    slots_both = [[int(((x >= c) & (x < c + 1)).sum()) for x in both] for c in range(c1, c1 + 24)]
    return {"instructions": n, "configs": out, "slots_alone": slots_alone, "slots_both": slots_both}


# ---------------------------------------------------------------------------
# the Job on the core: ledger row 2
# ---------------------------------------------------------------------------
FEATURES = ("bytes", "letters", "caps", "words", "distinct", "scanned", "same_length", "matched")


def compute_job() -> dict:
    from videos.cs.cs6.compute import load as load6
    from videos.cs.cs6.compute import novels
    from videos.cs.cs7.compute import load as load7

    books = novels()
    keys = list(books)
    rng = np.random.default_rng(11)
    img = job_image()
    rows = []
    for _ in range(24):
        b = books[keys[int(rng.integers(len(keys)))]]
        L = int(rng.integers(400, 4000))
        o = int(rng.integers(0, len(b) - L))
        tape = P.job_tape(b[o:o + L])
        q = core(img, tape)
        f = P.job_features(tape)
        rows.append({"bytes": L, "instructions": q.committed, "cycles": q.cycles, "stats": q.stats,
                     "features": {k_: f[k_] for k_ in FEATURES}})
    X = np.array([[1.0] + [r["features"][k_] for k_ in FEATURES] for r in rows])
    y = np.array([r["cycles"] for r in rows], float)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    b = books[2701]
    o = len(b) // 3
    tape = P.job_tape(b[o:o + 16000])
    t = time.time()
    q = core(img, tape)
    f = P.job_features(tape)
    pred = float(coef @ np.array([1.0] + [f[k_] for k_ in FEATURES]))
    check = {"bytes": len(tape), "cycles": q.cycles, "predicted": pred, "error": pred / q.cycles - 1,
             "instructions": q.committed, "ipc": q.ipc, "seconds": time.time() - t}
    corpus = load6("job")["corpus"]
    fc = corpus["features"]
    cycles = float(coef @ np.array([1.0] + [fc[k_] for k_ in FEATURES]))
    clock = load7("stages")["mhz"]
    seconds = cycles / (clock * 1e6)
    ledger = json.loads((Cache("cs7").dir / "ledger.json").read_text())[:2]
    ledger.append({"part": 8, "label": r"out of order", "seconds": seconds, "cycles": cycles,
                   "ipc": corpus["cycles"] / cycles, "clock_mhz": clock})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(ledger, indent=1))
    ipcs = [r["instructions"] / r["cycles"] for r in rows]
    return {"samples": rows, "coef": dict(zip(["const", *FEATURES], coef.tolist())), "check": check,
            "corpus": {"instructions": corpus["cycles"], "cycles": cycles, "ipc": corpus["cycles"] / cycles,
                       "seconds": seconds}, "ledger": ledger, "passage_ipc": [min(ipcs), max(ipcs)],
            "speedup": ledger[1]["seconds"] / seconds, "clock_mhz": clock}


# ---------------------------------------------------------------------------
# the Frontier: value prediction and secure speculation
# ---------------------------------------------------------------------------
def _value_predictable(tr: Trace, confidence: int = 2) -> tuple[np.ndarray, np.ndarray]:
    """A last-value and stride predictor per load pc with a confidence counter: which loads it would predict (and
    whether it would be right)."""
    last: dict[int, int] = {}
    stride: dict[int, int] = {}
    conf: dict[int, int] = {}
    used = np.zeros(len(tr), bool)
    right = np.zeros(len(tr), bool)
    for i, k in enumerate(tr.kind):
        if k != "load":
            continue
        pc = int(tr.pc[i])
        v = int(tr.load_value[i])
        if pc in last:
            guess = last[pc] + stride.get(pc, 0)
            ok = guess == v
            if conf.get(pc, 0) >= confidence:
                used[i] = True
                right[i] = ok
            conf[pc] = min(conf.get(pc, 0) + 1, 15) if ok else 0
            stride[pc] = v - last[pc]
        last[pc] = v
    return used, right


def _schedule_vp(tr: Trace, used, right, width, window, predictor, penalty=3) -> float:
    """``schedule`` with value prediction: a confidently predicted load's consumers start at once if the guess was
    right; a wrong guess is a misprediction (everything younger waits for the load, plus the penalty)."""
    from explainer.cs.pebble.limits import mispredicted

    wrong = mispredicted(tr, predictor())
    ready = [0] * 16
    store_done: dict[int, int] = {}
    floor = 0
    used_slots: dict[int, int] = {}
    start = np.zeros(len(tr), np.int64)
    fmax = 0
    for i in range(len(tr)):
        k = tr.kind[i]
        t = floor
        for r in tr.srcs[i]:
            t = max(t, ready[r])
        if k == "load":
            t = max(t, store_done.get(int(tr.addr[i]), 0))
        if window and i >= window:
            t = max(t, int(start[i - window]))
        while used_slots.get(t, 0) >= width:
            t += 1
        used_slots[t] = used_slots.get(t, 0) + 1
        start[i] = t
        f = t + LAT[k]
        fmax = max(fmax, f)
        d = int(tr.dst[i])
        if d:
            ready[d] = t if (used[i] and right[i]) else f
        if k == "store":
            store_done[int(tr.addr[i])] = f
        if wrong[i]:
            floor = max(floor, f + penalty)
        if used[i] and not right[i]:
            floor = max(floor, f + penalty)
    return len(tr) / max(fmax, 1)


class _Oracle:
    """A predictor that is never wrong (for ``mispredicted``): it replays the trace's own outcomes."""

    def __init__(self, tr: Trace):
        self.out = iter(bool(t) for k, t in zip(tr.kind, tr.taken) if k == "branch")
        self.nxt = None

    def predict(self, pc):
        self.nxt = next(self.out)
        return self.nxt

    def update(self, pc, taken):
        pass


def compute_frontier() -> dict:
    tr = chapter_trace()
    loads = sum(1 for k in tr.kind if k == "load")
    none = np.zeros(len(tr), bool)
    thresholds = {}
    for conf in (1, 2, 4, 8, 15):
        u, r = _value_predictable(tr, conf)
        thresholds[str(conf)] = {"predicted": int(u.sum()), "correct": int((u & r).sum()),
                                 "ipc": _schedule_vp(tr, u, r, 8, 256, BEST)}
    used, right = _value_predictable(tr, 8)
    vp = {}
    for w, win in ((4, 128), (8, 256), (16, 1024)):
        base = _schedule_vp(tr, none, none, w, win, BEST)
        with_vp = _schedule_vp(tr, used, right, w, win, BEST)
        oracle = _schedule_vp(tr, np.array([k == "load" for k in tr.kind]),
                              np.array([k == "load" for k in tr.kind]), w, win, BEST)
        vp[f"{w}/{win}"] = {"base": base, "vp": with_vp, "oracle": oracle}
    img, tape = job_image(), chapter_tape()
    plain = core(img, tape)
    sec = core(img, tape, secure=True)
    c, rr = _spectre(b"PEBBLE", secure=True)
    # with perfect branches, where the dataflow is the limit
    perfect = {"base": schedule(tr, width=8, window=256).ipc}
    perfect["vp"] = _schedule_vp(tr, used, right, 8, 256, lambda: _Oracle(tr))
    return {"loads": loads, "predicted": int(used.sum()), "correct": int((used & right).sum()), "vp": vp,
            "thresholds": thresholds, "perfect_branches": perfect,
            "secure": {"plain_cycles": plain.cycles, "secure_cycles": sec.cycles, "plain_ipc": plain.ipc,
                       "secure_ipc": sec.ipc, "cost": sec.cycles / plain.cycles - 1,
                       "spectre_output": list(c.output)}}


ITEMS = {
    "hook": compute_hook, "dataflow": compute_dataflow, "rename": compute_rename, "scoreboard": compute_scoreboard,
    "rob": compute_rob, "limits": compute_limits, "sweep": compute_sweep, "speculate": compute_speculate,
    "memory": compute_memory, "spectre": compute_spectre, "vliw": compute_vliw, "risc": compute_risc,
    "smt": compute_smt, "job": compute_job, "frontier": compute_frontier,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
