"""The Job in hardware (Part 60): a pipelined word-hashing and counting unit, as a netlist.

The datapath is Part 3's gates (``explainer/cs/pebble/hdl.py``) and Part 4's adders (``blocks.py``) between Part 5's
edge-triggered registers (``seq.Seq``), stepped clock by clock by the HDL simulator.  One byte enters per cycle:

    stage 1  classify   is the byte a letter (A-Z or a-z)?  Its 5-bit letter code (byte & 31: a = A = 1 ... z = 26)
                        is the lower-cased letter.  Every other byte (digits, punctuation, UTF-8 bytes >= 0x80) is a
                        separator, exactly as ``programs.job_words`` (the regex [a-z]+ on the lower-cased tape) sees it.
    stage 2  hash       a rolling hash of the current word, h <- 33 h + code (mod 2^32; Bernstein's "djb2", seeded with
                        5381), in two of Part 4's Kogge-Stone adders ((h << 5) + h, then + code); a separator after a
                        letter marks the word's end and hands its hash on, and resets h.
    stage 3  emit       on a word boundary, the hash leaves as a table index (its low bits folded with its top k bits:
                        i = (h xor h >> (32 - k)) mod 2^k) and a 32-bit tag (the hash itself).
    stage 4  count      the table entry at that index is read (a memory: a Python array, read combinationally from the
                        stage-3 register and written at the clock edge, like Part 5's register file); the tag is
                        compared at gate level; on a match the count goes through an incrementer, on an empty entry
                        the word claims it with count 1, and on a different tag the word is lost and an overflow
                        counter (a register) goes up by one.

The table is direct-mapped and never probes, so two words whose indices coincide cannot both be counted (the second
is "lost": counted in the overflow register), and two words whose full 32-bit hashes coincide are silently merged.
``run`` reports both against the software Job (``programs.job_words``/``job_reference``).  Consecutive words end at
least two cycles apart (a letter, then a separator), so a read never sees a stale entry.

Timing uses the series' one technology (``explainer/cs/pebble/tech.py``: a gate delay, flip-flop overheads, and a
memory access): the clock is set by the slowest stage, and the count stage includes the table's read.  Throughput is
one byte per cycle per lane; ``lanes`` copies of the unit (each with its own table, run bit-parallel by the
simulator) split the text at word boundaries and are merged at the end.
"""

from __future__ import annotations

import json
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np

from explainer.cs.pebble import tech
from explainer.cs.pebble.blocks import mux2_bus, prefix_adder, tree
from explainer.cs.pebble.hdl import Circuit
from explainer.cs.pebble.programs import TOP, job_reference, job_tape, job_words
from explainer.cs.pebble.seq import Seq

HASH_BITS = 32
COUNT_BITS = 24
H0 = 5381
INDEX_BITS = 12           # 4,096 entries x 57 bits (29 KB): the SRAM size tech.MEM_PS assumes; for a short text
NOVEL_INDEX_BITS = 20     # 1,048,576 entries (7.1 MB) for the thirty novels: 1 ns for that is optimistic
LATENCY = 4               # cycles from a word's last separator entering to its count being written
MASK = (1 << HASH_BITS) - 1
REPO = Path(__file__).resolve().parents[3]


def _bus(w) -> list[int]:
    return [w] if isinstance(w, int) else list(w)


# ---------------------------------------------------------------------------
# the reference, in Python
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1 << 20)
def word_hash(w: bytes) -> int:
    h = H0
    for ch in w:
        h = (h * 33 + (ch & 31)) & MASK
    return h


def slot(h: int, k: int = INDEX_BITS) -> int:
    return (h ^ (h >> (HASH_BITS - k))) & ((1 << k) - 1)


def table_model(words: list[bytes], k: int = INDEX_BITS) -> dict:
    """What one lane's table must hold after these words: the first word to reach a slot owns it; later words with
    the same tag add to it; words with another tag are lost (overflow)."""
    owner: dict[int, int] = {}
    count: dict[int, int] = {}
    overflow = 0
    # Equivalent to replaying the words one by one: a slot's owner is decided by first appearances, and Counter
    # keeps words in the order they first appear.
    for w, n in Counter(words).items():
        h = word_hash(w)
        i = slot(h, k)
        if i not in owner:
            owner[i], count[i] = h, n
        elif owner[i] == h:
            count[i] += n
        else:
            overflow += n
    return {"slots": {i: (owner[i], count[i]) for i in owner}, "overflow": overflow}


# ---------------------------------------------------------------------------
# the stages, as circuits
# ---------------------------------------------------------------------------
def _consts(c: Circuit, value: int, width: int) -> list[int]:
    zero, one = c.const(0), c.const(1)
    return [one if (value >> i) & 1 else zero for i in range(width)]


def le_const(c: Circuit, x: list[int], K: int) -> int:
    """x <= K for a constant K, from the low bit up: at each bit the higher bit decides if it differs."""
    res = c.const(1)
    for i, xi in enumerate(x):
        nx = c.not_(xi)
        res = c.or_(nx, res) if (K >> i) & 1 else c.and_(nx, res)
    return res


def classify_stage() -> Circuit:
    c = Circuit("stage 1: classify")
    byte = _bus(c.input("byte", 8))
    low = byte[:5]
    letter = tree(c, c.and_, [c.not_(byte[7]), byte[6], tree(c, c.or_, low), le_const(c, low, 26)])
    c.output("letter", letter)
    c.output("code", [c.and_(letter, b) for b in low])
    return c.pruned()


def hash_stage(bits: int = HASH_BITS) -> Circuit:
    c = Circuit("stage 2: rolling hash")
    h = _bus(c.input("h", bits))
    inword = c.input("inword")
    letter = c.input("letter")
    code = _bus(c.input("code", 5))
    zero = c.const(0)
    add = prefix_adder(bits, "kogge-stone")
    s = c.embed(add, a=[zero] * 5 + h[:bits - 5], b=h, cin=zero)["s"]          # 33 h = (h << 5) + h
    u = c.embed(add, a=s, b=code + [zero] * (bits - 5), cin=zero)["s"]         # ... + code
    c.output("h_next", mux2_bus(c, letter, _consts(c, H0, bits), u))
    c.output("inword_next", c.buf(letter))
    c.output("end", c.and_(inword, c.not_(letter)))
    c.output("hash_out", [c.buf(w) for w in h])
    return c.pruned()


def emit_stage(k: int = INDEX_BITS, bits: int = HASH_BITS) -> Circuit:
    if not 1 <= k < bits:
        raise ValueError("the index needs 1 <= k < 32 bits")
    c = Circuit("stage 3: emit")
    end = c.input("end")
    h = _bus(c.input("hash", bits))
    c.output("emit", c.buf(end))
    c.output("index", [c.xor(h[i], h[i + bits - k]) for i in range(k)])
    c.output("tag", [c.buf(w) for w in h])
    return c.pruned()


def count_stage(bits: int = HASH_BITS, cbits: int = COUNT_BITS) -> Circuit:
    c = Circuit("stage 4: count")
    emit = c.input("emit")
    tag = _bus(c.input("tag", bits))
    rd_valid = c.input("rd_valid")
    rd_tag = _bus(c.input("rd_tag", bits))
    rd_count = _bus(c.input("rd_count", cbits))
    ovf = _bus(c.input("ovf", cbits))
    zero, one = c.const(0), c.const(1)
    eq = tree(c, c.and_, [c.xnor(x, y) for x, y in zip(tag, rd_tag)])
    live = c.and_(emit, rd_valid)
    hit = c.and_(live, eq)
    miss = c.and_(live, c.not_(eq))
    claim = c.and_(emit, c.not_(rd_valid))
    inc = prefix_adder(cbits, "kogge-stone")
    plus1 = c.embed(inc, a=rd_count, b=[zero] * cbits, cin=one)["s"]
    c.output("we", c.or_(hit, claim))
    c.output("wd_count", mux2_bus(c, hit, _consts(c, 1, cbits), plus1))
    c.output("miss", c.buf(miss))
    c.output("ovf_next", c.embed(inc, a=ovf, b=[zero] * cbits, cin=miss)["s"])
    return c.pruned()


def stages(k: int = INDEX_BITS) -> dict[str, Circuit]:
    return {"classify": classify_stage(), "hash": hash_stage(), "emit": emit_stage(k), "count": count_stage()}


def unit(k: int = INDEX_BITS) -> Seq:
    """The whole pipeline as one synchronous circuit.  Inputs: ``byte`` and the table's read port (``rd_valid``,
    ``rd_tag``, ``rd_count``, addressed by register ``s3_index``); outputs: the write port (``we``, ``wd_count``;
    the address and tag being those in ``s3_index``/``s3_tag``) and ``miss``."""
    st = stages(k)
    s = Seq("word-counting unit")
    c = s.c
    byte = _bus(c.input("byte", 8))
    rd_valid = c.input("rd_valid")
    rd_tag = _bus(c.input("rd_tag", HASH_BITS))
    rd_count = _bus(c.input("rd_count", COUNT_BITS))
    # stage 1
    l1, c1 = s.reg("s1_letter", 1), s.reg("s1_code", 5)
    o = c.embed(st["classify"], byte=byte)
    s.set_next("s1_letter", o["letter"])
    s.set_next("s1_code", o["code"])
    # stage 2
    h, inword = s.reg("h", HASH_BITS, H0), s.reg("inword", 1)
    e2, h2 = s.reg("s2_end", 1), s.reg("s2_hash", HASH_BITS)
    o = c.embed(st["hash"], h=h, inword=inword, letter=l1, code=c1)
    s.set_next("h", o["h_next"])
    s.set_next("inword", o["inword_next"])
    s.set_next("s2_end", o["end"])
    s.set_next("s2_hash", o["hash_out"])
    # stage 3
    e3, _i3, t3 = s.reg("s3_emit", 1), s.reg("s3_index", k), s.reg("s3_tag", HASH_BITS)
    o = c.embed(st["emit"], end=e2, hash=h2)
    s.set_next("s3_emit", o["emit"])
    s.set_next("s3_index", o["index"])
    s.set_next("s3_tag", o["tag"])
    # stage 4
    ovf = s.reg("overflow", COUNT_BITS)
    o = c.embed(st["count"], emit=e3, tag=t3, rd_valid=rd_valid, rd_tag=rd_tag, rd_count=rd_count, ovf=ovf)
    s.set_next("overflow", o["ovf_next"])
    c.output("we", o["we"])
    c.output("wd_count", o["wd_count"])
    c.output("miss", o["miss"])
    return s


# ---------------------------------------------------------------------------
# timing and area
# ---------------------------------------------------------------------------
STAGE_FLIP_FLOPS = {"classify": 1 + 5, "hash": HASH_BITS + 1 + 1 + HASH_BITS, "emit": None, "count": COUNT_BITS}


def timing(k: int = INDEX_BITS) -> dict:
    """Gates per stage (by kind), critical-path depth per stage, and the clock: every stage's logic must settle in
    one period (gate delays from ``tech.GATE_PS``, plus ``tech.FF_PS`` for the registers); the count stage also reads
    the table (``tech.MEM_PS``)."""
    st = stages(k)
    rows = {}
    for name, c in st.items():
        mem = tech.MEM_PS if name == "count" else 0.0
        ff = STAGE_FLIP_FLOPS[name] if name != "emit" else 1 + k + HASH_BITS
        rows[name] = {"counts": c.counts(), "gates": c.size(), "nand_gates": c.to_nand().size(), "depth": c.depth(),
                      "flip_flops": ff, "mem_ps": mem, "ps": mem + c.depth() * tech.GATE_PS}
    longest = max(r["ps"] for r in rows.values())
    critical = max(rows, key=lambda n: rows[n]["ps"])
    period = longest + tech.FF_PS
    logic = max(r["depth"] for r in rows.values()) * tech.GATE_PS + tech.FF_PS
    return {"stages": rows, "critical_stage": critical, "critical_depth": rows[critical]["depth"],
            "max_logic_depth": max(r["depth"] for r in rows.values()), "period_ps": period,
            "clock_mhz": tech.mhz(period), "logic_only_period_ps": logic, "logic_only_mhz": tech.mhz(logic),
            "gates": sum(r["gates"] for r in rows.values()),
            "flip_flops": sum(r["flip_flops"] for r in rows.values()), "table_entries": 1 << k,
            "table_bits": (1 << k) * (1 + HASH_BITS + COUNT_BITS), "gate_ps": tech.GATE_PS, "ff_ps": tech.FF_PS,
            "mem_ps": tech.MEM_PS, "bytes_per_cycle": 1}


# ---------------------------------------------------------------------------
# the simulation
# ---------------------------------------------------------------------------
def split_lanes(tape: bytes, lanes: int) -> list[bytes]:
    """Cut the tape into ``lanes`` pieces at separators (a cut never falls inside a word)."""
    cuts, n = [0], len(tape)
    for i in range(1, lanes):
        p = max(cuts[-1], i * n // lanes)
        while 0 < p < n and bytes(tape[p - 1:p]).isalpha():  # ASCII letters only, as the Job reads them
            p += 1
        cuts.append(p)
    cuts.append(n)
    return [tape[a:b] for a, b in zip(cuts, cuts[1:])]


def run(tape: bytes, lanes: int = 1, k: int = INDEX_BITS, trace_cycles: int = 64) -> dict:
    """The unit, cycle by cycle at gate level, on ``tape`` (each lane its own piece and its own table), then the
    lanes' tables merged by tag.  Checked against the software Job and against ``table_model``."""
    t0 = time.perf_counter()
    pieces = split_lanes(tape, lanes)
    L = len(pieces)
    T = max(len(p) for p in pieces) + 1 + LATENCY  # a closing separator, then the pipeline drains
    feed = np.zeros((T, L), np.int64)
    for j, p in enumerate(pieces):
        feed[:len(p), j] = np.frombuffer(p, np.uint8)
        feed[len(p), j] = 0x20
    s = unit(k)
    s.reset(L)
    size = 1 << k
    valid = np.zeros((L, size), bool)
    tags = np.zeros((L, size), np.int64)
    counts = np.zeros((L, size), np.int64)
    ln = np.arange(L)
    emitted: list[list[int]] = [[] for _ in range(L)]
    trace = []
    for t in range(T):
        idx = s.state["s3_index"].astype(np.int64)
        tag = s.state["s3_tag"].astype(np.int64)
        emit = s.state["s3_emit"].astype(bool)
        for j in np.flatnonzero(emit):
            emitted[j].append(int(tag[j]))
        if t < trace_cycles:
            trace.append({"t": t, "byte": int(feed[t, 0]), "s1_letter": int(s.state["s1_letter"][0]),
                          "s1_code": int(s.state["s1_code"][0]), "h": int(s.state["h"][0]),
                          "s2_end": int(s.state["s2_end"][0]), "s3_emit": int(emit[0]), "s3_index": int(idx[0]),
                          "s3_tag": int(tag[0])})
        out = s.step({"byte": feed[t], "rd_valid": valid[ln, idx].astype(np.int64), "rd_tag": tags[ln, idx],
                      "rd_count": counts[ln, idx]})
        we = out["we"].astype(bool)
        if t < trace_cycles:
            trace[-1].update({"we": int(we[0]), "miss": int(out["miss"][0]), "wd_count": int(out["wd_count"][0])})
        w = np.flatnonzero(we)
        valid[w, idx[w]] = True
        tags[w, idx[w]] = tag[w]
        counts[w, idx[w]] = out["wd_count"][w]
    sim_seconds = time.perf_counter() - t0
    overflow = s.state["overflow"].astype(np.int64)
    # checks: the hashes, each lane's table, and the merged counts against the software Job
    lane_words = [job_words(p) for p in pieces]
    hashes_ok = all(emitted[j] == [word_hash(w) for w in lane_words[j]] for j in range(L))
    tables_ok = True
    for j in range(L):
        m = table_model(lane_words[j], k)
        hw = {int(i): (int(tags[j, i]), int(counts[j, i])) for i in np.flatnonzero(valid[j])}
        tables_ok &= hw == m["slots"] and int(overflow[j]) == m["overflow"]
    merged: dict[int, int] = {}
    for j in range(L):
        for i in np.flatnonzero(valid[j]):
            merged[int(tags[j, i])] = merged.get(int(tags[j, i]), 0) + int(counts[j, i])
    words = job_words(tape)
    return {**compare(merged, words, int(overflow.sum()), job_reference(tape)), "bytes": len(tape), "lanes": L,
            "index_bits": k, "cycles": T, "cycles_per_lane_byte": T / max(1, max(len(p) for p in pieces)),
            "hashes_match": hashes_ok, "tables_match_model": bool(tables_ok), "overflow_per_lane": overflow.tolist(),
            "occupied": int(valid.sum()), "trace": trace, "sim_seconds": sim_seconds,
            "seconds": time.perf_counter() - t0}


def compare(merged: dict[int, int], words: list[bytes], overflow: int, reference: bytes, top: int = TOP,
            ref: Counter | None = None) -> dict:
    """The hardware's counts (keyed by hash) against the software Job's (``words`` = ``job_words(tape)``, and
    ``reference`` = ``job_reference(tape)``, the Job's printed top list).  Names are attached by hashing the
    reference's words: the hardware itself only ever holds hashes."""
    ref = ref if ref is not None else Counter(words)
    by_hash: dict[int, list[bytes]] = {}
    for w in ref:
        by_hash.setdefault(word_hash(w), []).append(w)
    merges = {h: ws for h, ws in by_hash.items() if len(ws) > 1}
    exact = sum(1 for w in ref if merged.get(word_hash(w), 0) == ref[w])
    counted = sum(merged.values())
    # the hardware's top list, names attached (ties by first appearance, as the Job breaks them)
    order = {w: i for i, w in enumerate(ref)}
    named = [(by_hash[h][0], n) for h, n in merged.items() if h in by_hash]
    best = sorted(named, key=lambda x: (-x[1], order[x[0]]))[:top]
    report = b"".join(w + b" " + str(n).encode() + b"\n" for w, n in best)
    return {"words": len(words), "distinct": len(ref), "exact_words": exact, "inexact_words": len(ref) - exact,
            "counted_occurrences": counted, "lost_occurrences": len(words) - counted, "overflow": overflow,
            "hash_merges": len(merges), "merged_words": sorted(w.decode() for ws in merges.values() for w in ws),
            "top_exact": report == reference, "top": report.decode(), "accounted": counted + overflow == len(words)}


def _novel_tapes() -> dict[int, bytes]:
    from videos.cs.cs6.compute import novels

    return {n: job_tape(t) for n, t in novels().items()}


def short_text() -> bytes:
    """Chapter 1 of Pride and Prejudice, as Part 6 cut it (4,709 bytes)."""
    from videos.cs.cs6.compute import novels

    pp = novels()[1342]
    i = pp.index("It is a truth universally acknowledged")
    j = pp.index("Mr. Bennet was among the earliest")
    return job_tape(pp[i:j].rstrip())


@lru_cache(maxsize=1)
def corpus() -> dict:
    """The thirty novels as one stream (a newline between books), its words, their counts and the Job's report."""
    tapes = _novel_tapes()
    tape = b"\n".join(tapes.values())
    words = job_words(tape)
    return {"books": len(tapes), "bytes": sum(len(t) for t in tapes.values()), "tape": tape, "words": words,
            "ref": Counter(words), "reference": job_reference(tape)}


def novels_model(k: int = NOVEL_INDEX_BITS, lanes=(1, 4, 16, 64)) -> dict:
    """The thirty novels through the same unit, by its functional model (``table_model`` is checked against the
    gate-level netlist in ``run``): what one table of 2^k entries counts exactly, and per lane count, the cycles
    including a merge of the lanes' occupied entries (one per cycle) into one table."""
    t0 = time.perf_counter()
    cp = corpus()
    tape, words, ref, reference = cp["tape"], cp["words"], cp["ref"], cp["reference"]
    out = {"books": cp["books"], "bytes": cp["bytes"], "stream_bytes": len(tape), "index_bits": k, "lanes": []}
    for L in lanes:
        pieces = split_lanes(tape, L)
        merged: dict[int, int] = {}
        overflow = occupied = 0
        for p in pieces:
            m = table_model(job_words(p) if L > 1 else words, k)
            overflow += m["overflow"]
            occupied += len(m["slots"])
            for h, n in m["slots"].values():
                merged[h] = merged.get(h, 0) + n
        cmp = compare(merged, words, overflow, reference, ref=ref)
        cmp.pop("merged_words")
        cmp.pop("top")
        stream = max(len(p) for p in pieces) + 1 + LATENCY
        merge = occupied if L > 1 else 0
        out["lanes"].append({"lanes": L, "stream_cycles": stream, "merge_cycles": merge, "cycles": stream + merge,
                             "occupied": occupied, **cmp})
    out["seconds"] = time.perf_counter() - t0
    return out


def table_sweep(ks=(12, 14, 16, 18, 20, 22)) -> list[dict]:
    """One lane on the thirty novels, for several table sizes: what a direct-mapped table loses."""
    rows = []
    for k in ks:
        r = novels_model(k, lanes=(1,))["lanes"][0]
        rows.append({"index_bits": k, "entries": 1 << k, "kbytes": (1 << k) * (1 + HASH_BITS + COUNT_BITS) / 8 / 1024,
                     **{x: r[x] for x in ("distinct", "exact_words", "inexact_words", "lost_occurrences", "words",
                                          "hash_merges", "top_exact", "occupied")}})
    return rows


def job_on_novels(k: int = NOVEL_INDEX_BITS, lanes=(1, 4, 16, 64), model: dict | None = None) -> dict:
    """The Job's time on the thirty novels at the unit's clock: cycles / clock, per lane count."""
    tm = timing(k)
    model = model or novels_model(k, lanes)
    f = tm["clock_mhz"] * 1e6
    rows = [{**r, "seconds": r["cycles"] / f, "gbytes_per_second": model["bytes"] / (r["cycles"] / f) / 1e9}
            for r in model["lanes"]]
    return {"bytes": model["bytes"], "clock_mhz": tm["clock_mhz"], "period_ps": tm["period_ps"], "index_bits": k,
            "gates": tm["gates"], "lanes": rows}


def ledger(source: str | None = None) -> list[dict]:
    """The latest ledger copy before Part 60: Part 55's (rows 0-20) if it exists, else Part 50's (rows 0-19)."""
    for name in ([source] if source else ["cs55", "cs50"]):
        p = REPO / ".cache" / name / "ledger.json"
        if p.exists():
            return [r for r in json.loads(p.read_text()) if r["part"] != 60]
    raise FileNotFoundError("no ledger copy (run Part 50's or Part 55's compute)")


def ledger_row(job: dict | None = None) -> dict:
    """Ledger row 21: the thirty novels through one word-counting unit at one byte per cycle (and with parallel
    lanes, each its own unit and table, merged at the end).  Returns the row; ``ledger_with_row`` appends it."""
    job = job or job_on_novels()
    one = job["lanes"][0]
    return {"part": 60, "label": r"a word-counting unit, \ one byte per cycle", "seconds": one["seconds"],
            "cycles": one["cycles"], "clock_mhz": job["clock_mhz"], "gates": job["gates"],
            "lost_occurrences": one["lost_occurrences"], "top_exact": one["top_exact"],
            "lanes": {str(r["lanes"]): r["seconds"] for r in job["lanes"]}}


def ledger_with_row(row: dict | None = None, source: str | None = None) -> list[dict]:
    led = ledger(source)
    return led + [row or ledger_row()]
