"""Limits of instruction-level parallelism (Part 8), in the manner of David Wall's 1991 study.

    tr = trace(program.image, tape=b"...")            # the program's correct path, from the emulator
    schedule(tr, width=4, window=128).ipc             # an oracle machine's instructions per cycle

The oracle schedules every instruction of the trace as early as its constraints allow, with no fetch limits:

* data: an instruction starts when its source registers are ready (unit latencies: ALU and multiply 1, load 2,
  divide 16); with ``rename=False`` it also waits for the false dependences (a write may not finish before an
  earlier read of the same register has happened, nor before an earlier write of it)
* memory: ``memory="perfect"`` makes a load wait only for the last earlier store to the same word;
  ``"conservative"`` for every earlier store's address; ``"none"`` for nothing at all (an upper bound)
* control: ``branches="perfect"`` ignores them; a predictor object makes every mispredicted branch a barrier
  (nothing younger starts until it has resolved, plus ``penalty`` cycles of refill); ``"barrier"`` treats every
  branch so (no speculation)
* resources: at most ``width`` instructions start in a cycle, and instruction i cannot start before instruction
  i - ``window`` has started (a sliding window of ``window`` instructions)
* ``value_prediction``: a set of load pcs whose values are predicted correctly, so their consumers need not wait
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .emu import Machine
from .isa import decode
from .pipe import BRANCH, LOADS, STORES, dest, sources

LAT = {"alu": 1, "mul": 1, "div": 16, "load": 2, "store": 1, "branch": 1, "jump": 1}


def kind(op: str) -> str:
    if op in LOADS:
        return "load"
    if op in STORES:
        return "store"
    if op in BRANCH:
        return "branch"
    if op in ("jal", "jalr"):
        return "jump"
    if op in ("div", "rem"):
        return "div"
    if op in ("mul", "mulh"):
        return "mul"
    return "alu"


@dataclass
class Trace:
    pc: np.ndarray
    kind: list
    srcs: list
    dst: np.ndarray
    addr: np.ndarray  # memory word address (byte address // 4), -1 for others
    taken: np.ndarray
    load_value: np.ndarray  # the value a load produced (for value-prediction studies)

    def __len__(self):
        return len(self.pc)


def trace(image: bytes, tape: bytes = b"", mem_size: int = 1 << 20, max_steps: int = 50_000_000) -> Trace:
    m = Machine(image, tape=tape, mem_size=mem_size)
    pcs, kinds, srcs, dsts, addrs, tk, vals = [], [], [], [], [], [], []
    cache: dict[int, tuple] = {}
    while not m.halted and m.steps < max_steps:
        pc = m.pc
        d = cache.get(pc)
        if d is None:
            ins = decode(m.word(pc))
            d = (ins, kind(ins.op), sources(ins), dest(ins))
            cache[pc] = d
        ins, k, s, ds = d
        a = -1
        if k in ("load", "store"):
            a = ((m.regs[ins.rs1] + ins.imm) & 0xFFFF_FFFF) // 4
        m.step()
        if k == "store":
            cache.pop(a * 4, None)  # code may be written as data
        pcs.append(pc)
        kinds.append(k)
        srcs.append(tuple(r for r in s if r))
        dsts.append(ds)
        addrs.append(a)
        tk.append(m.pc != pc + 4)
        vals.append(m.regs[ds] if k == "load" and ds else 0)
    return Trace(np.array(pcs, np.int64), kinds, srcs, np.array(dsts, np.int64), np.array(addrs, np.int64),
                 np.array(tk, bool), np.array(vals, np.int64))


@dataclass
class Schedule:
    cycles: int
    instructions: int
    start: np.ndarray

    @property
    def ipc(self) -> float:
        return self.instructions / max(self.cycles, 1)


def mispredicted(tr: Trace, predictor) -> np.ndarray:
    """Which branches the predictor gets wrong, trained in program order (Part 7's accuracy study)."""
    out = np.zeros(len(tr), bool)
    for i, k in enumerate(tr.kind):
        if k == "branch":
            t = bool(tr.taken[i])
            out[i] = predictor.predict(int(tr.pc[i])) != t
            predictor.update(int(tr.pc[i]), t)
    return out


def schedule(tr: Trace, width: int | None = None, window: int | None = None, rename: bool = True,
             memory: str = "perfect", branches="perfect", penalty: int = 3, latency: dict | None = None,
             value_prediction: set | None = None, limit: int | None = None) -> Schedule:
    lat = dict(LAT, **(latency or {}))
    n = len(tr) if limit is None else min(limit, len(tr))
    if branches == "perfect":
        wrong = None
    elif branches == "barrier":
        wrong = np.array([k in ("branch", "jump") for k in tr.kind[:n]])
    else:
        wrong = mispredicted(tr, branches)
    ready = [0] * 16  # when each register's value is available
    last_read = [0] * 16
    written = [0] * 16
    store_done: dict[int, int] = {}
    store_addr_known = 0  # conservative: the latest earlier store's address time
    floor = 0  # control barrier
    used: dict[int, int] = {}
    start = np.zeros(n, np.int64)
    finish_max = 0
    vp = value_prediction or set()
    for i in range(n):
        k = tr.kind[i]
        t = floor
        for r in tr.srcs[i]:
            if ready[r] > t:
                t = ready[r]
        d = int(tr.dst[i])
        if not rename and d:
            t = max(t, last_read[d], written[d] - lat[k] + 1)
        if k == "load":
            if memory == "perfect":
                t = max(t, store_done.get(int(tr.addr[i]), 0))
            elif memory == "conservative":
                t = max(t, store_addr_known)
        if window is not None and i >= window:
            t = max(t, int(start[i - window]))
        if width is not None:
            while used.get(t, 0) >= width:
                t += 1
            used[t] = used.get(t, 0) + 1
        start[i] = t
        f = t + lat[k]
        if f > finish_max:
            finish_max = f
        for r in tr.srcs[i]:
            if t > last_read[r]:
                last_read[r] = t
        if d:
            ready[d] = t if (k == "load" and int(tr.pc[i]) in vp) else f
            written[d] = f
        if k == "store":
            store_done[int(tr.addr[i])] = f
            store_addr_known = max(store_addr_known, t + 1)
        if wrong is not None and wrong[i]:
            floor = max(floor, f + penalty)
    return Schedule(int(finish_max), n, start)
