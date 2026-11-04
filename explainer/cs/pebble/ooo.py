"""Pebble's out-of-order core, simulated cycle by cycle (Part 8).

    core = OutOfOrder(program.image, tape=b"...", width=4, rob_size=128)
    core.run()
    core.cycles, core.committed, core.ipc, core.regs, core.output, core.stats

The machine of Hennessy and Patterson's chapter 3, in the form every modern core takes:

    fetch     up to ``width`` instructions a cycle, along the predicted path (direction predictor, return-address
              stack, last-target buffer for other ``jalr``); at most one taken branch a cycle
    rename    after ``fe_depth`` cycles of decoding, each instruction gets a reorder-buffer entry; its sources are
              looked up in the register alias table (RAT), which names the in-flight instruction that will produce
              each register, so only true (read-after-write) dependences remain
    issue     an instruction leaves the issue queue (``iq_size`` entries, oldest first) once its operands are ready
              and a unit is free: ``width`` ALUs, a multiplier, an unpipelined divider (16 cycles), two memory ports
    complete  results are broadcast to waiting instructions (the common data bus of Tomasulo, 1967); a mispredicted
              branch squashes everything younger and redirects fetch
    commit    up to ``width`` a cycle, in program order from the head of the reorder buffer (Smith and Pleszkun,
              1985): only here are registers, memory and devices changed, so exceptions are precise

Memory: stores wait in the store queue until they commit; a load takes its value from the youngest older store to the
same bytes (store-to-load forwarding) or from memory.  ``disambiguation`` says what a load does about older stores
whose addresses are still unknown: "conservative" waits for them; "speculative" goes ahead, and if one of them turns
out to write the bytes it read, the load and everything after it are squashed and refetched (a memory-order
violation); "wait-table" is speculative except for loads that have violated before (the Alpha 21264's scheme).

The machine computes every value itself, on the correct path and on the wrong one: wrong-path loads really read memory
and really fill the optional data cache (``cache``), which is what Spectre exploits.  Device accesses (tape, console,
the cycle counter) happen only at the head of the reorder buffer, and a read of the cycle counter is serializing
(like x86's ``rdtscp`` followed by ``lfence``): from the moment it is renamed, nothing younger issues until it has
committed.  Two model-only devices serve the Part 8 experiments: storing an
address to ``IO_FLUSH`` evicts its cache line (x86's ``clflush``; 0xFFFFFFFF empties the cache), and with
``timer="cycles"`` the counter reads the cycle number instead of the instruction count.

The direction predictor is trained in program order on the correct path, as in Part 7's accuracy study: the emulator
first records the program's correct path, and a fetched instruction on that path is trained with its true outcome
(equivalent to a predictor whose speculative history is repaired perfectly).  With ``training="commit"`` the core
instead trains it as branches commit, for programs whose control flow depends on timing (the Spectre experiment).

``secure=True`` is the simplest secure-speculation scheme (in the spirit of NDA and STT, 2019): a load that completes
while an older branch is still unresolved keeps its value to itself until every older branch has executed, so nothing
that depends on a speculatively loaded value can run, and the value can leave no footprint.  The core is checked against the
emulator (tests/test_cs8_ooo.py): the same registers, memory, output and instruction count on every program.
"""

from __future__ import annotations

import heapq
from array import array
from dataclasses import dataclass, field

from .emu import Machine, MachineError, mext
from .isa import IO_BASE, IO_CONSOLE, IO_CYCLES, IO_TAPE, MASK, NREGS, OPS, decode, sext
from .pipe import BRANCH, LOADS, STORES, alu, dest, sources, taken

IO_FLUSH = IO_BASE + 0x0C  # model only: store an address to flush its cache line (like clflush); 0xFFFFFFFF: all
DIV_CYCLES = 16


class Cache:
    """A set-associative data cache with LRU replacement; ``access`` returns the latency and fills the line."""

    def __init__(self, size=32 * 1024, line=64, ways=8, hit=2, miss=60):
        self.line, self.ways, self.hit, self.miss = line, ways, hit, miss
        self.sets = size // (line * ways)
        self.flush()

    def flush(self):
        self.tags = [[] for _ in range(self.sets)]

    def flush_line(self, addr: int):
        ln = addr // self.line
        s = self.tags[ln % self.sets]
        if ln in s:
            s.remove(ln)

    def present(self, addr: int) -> bool:
        ln = addr // self.line
        return ln in self.tags[ln % self.sets]

    def access(self, addr: int) -> int:
        ln = addr // self.line
        s = self.tags[ln % self.sets]
        if ln in s:
            s.remove(ln)
            s.append(ln)
            return self.hit
        s.append(ln)
        if len(s) > self.ways:
            s.pop(0)
        return self.miss


@dataclass(eq=False)
class Uop:
    seq: int
    pc: int
    word: int
    k: int | None  # index on the correct path, or None on a wrong path
    ins: object = None
    op: str = "?"
    rd: int = 0
    pred: int = 0  # the next pc fetch guessed
    srcs: list = field(default_factory=list)  # (arch reg, producer Uop or None)
    vals: list = field(default_factory=list)
    left: int = 0  # operands still awaited
    consumers: list = field(default_factory=list)
    state: int = 0  # 0 renamed, 1 issued, 2 complete
    result: int | None = None
    addr: int | None = None
    size: int = 0
    sdata: int | None = None  # a store's data
    nxt: int = 0  # the computed next pc
    exc: str | None = None
    squashed: bool = False
    fwd_from: object = None  # the store a load took its value from (None: memory)
    ras: tuple = ()  # the return-address stack after this instruction was fetched (for repair on a squash)
    t: list = field(default_factory=lambda: [-1] * 5)  # cycles: fetched, renamed, issued, complete, committed


class OutOfOrder:
    def __init__(self, image: bytes, tape: bytes = b"", mem_size: int = 1 << 20, width: int = 4, rob_size: int = 128,
                 iq_size: int = 64, lsq_size: int = 48, fe_depth: int = 3, predictor=None, mem_latency: int = 2,
                 disambiguation: str = "wait-table", cache: Cache | None = None, timer: str = "retired",
                 record: int = 0, max_cycles: int = 200_000_000, perfect_prediction: bool = False,
                 training: str = "path", secure: bool = False, record_start: int = 0, occupancy: bool = False):
        self.image, self.tape, self.mem_size = image, tape, mem_size
        self.width, self.rob_size, self.iq_size, self.lsq_size = width, rob_size, iq_size, lsq_size
        self.fe_depth, self.predictor, self.mem_latency = fe_depth, predictor, mem_latency
        self.disamb, self.cache, self.timer, self.record = disambiguation, cache, timer, record
        self.max_cycles, self.perfect, self.training = max_cycles, perfect_prediction, training
        self.secure, self.record_start = secure, record_start
        self.occupancy = array("H") if occupancy else None  # reorder-buffer entries in use, each cycle
        self.mem = bytearray(mem_size)
        self.mem[: len(image)] = image
        self.regs = [0] * NREGS
        self.regs[2] = mem_size
        self.output = bytearray()
        self.tape_pos = 0
        self.cycles = self.committed = 0
        self.halted = False
        self.error = None
        self.stats = {"mispredicts": 0, "squashed": 0, "violations": 0, "rob_full": 0, "iq_full": 0,
                      "lsq_full": 0, "branches": 0, "forwarded": 0, "wrong_path_loads": 0}
        self.timeline: list[Uop] = []
        if training == "path":
            self._path()
        else:  # "commit": the core trains the predictor itself, in order (for programs whose control flow
            self.path = array("I")  # depends on timing, which the emulator cannot reproduce)

    # -- the correct path, from the emulator (for training the predictor only) ------------------------------
    def _path(self):
        m = Machine(self.image, tape=self.tape, mem_size=self.mem_size)
        pcs = array("I")
        try:
            while not m.halted and m.steps < self.max_cycles:
                pcs.append(m.pc)
                m.step()
        except MachineError:
            pass
        pcs.append(m.pc)
        self.path = pcs

    # -- memory, as committed -----------------------------------------------------------------------------
    def _read(self, addr: int, size: int, signed_: bool) -> int:
        if size == 4:
            return int.from_bytes(self.mem[addr:addr + 4], "little")
        v = self.mem[addr]
        return (v - 256) & MASK if signed_ and v & 0x80 else v

    def _device_load(self, addr: int) -> int:
        if addr == IO_TAPE:
            if self.tape_pos < len(self.tape):
                self.tape_pos += 1
                return self.tape[self.tape_pos - 1]
            return MASK
        if addr == IO_CYCLES:
            return (self.cycles if self.timer == "cycles" else self.committed) & MASK
        raise MachineError(f"load from unmapped device {addr:#010x}")

    def _check(self, u: Uop) -> str | None:
        a = u.addr
        if a >= IO_BASE:
            return None
        if a + u.size > self.mem_size:
            return f"{'load' if u.op in LOADS else 'store'} at {a:#x} outside memory"
        if u.size == 4 and a & 3:
            return f"misaligned word access at {a:#x}"
        return None

    # -- the machine ----------------------------------------------------------------------------------------
    def run(self) -> "OutOfOrder":
        W = self.width
        self.rob: list[Uop] = []  # oldest first
        self.sq: list[Uop] = []  # stores in flight, oldest first
        self.lq: list[Uop] = []  # loads in flight, oldest first
        self.rat: list[Uop | None] = [None] * NREGS
        self.fq: list[tuple[int, Uop]] = []  # (cycle it may be renamed, uop)
        self.iq = 0
        self.ready: list[tuple[int, int, Uop]] = []  # heap by seq
        self.waking: dict[int, list[Uop]] = {}
        self.pending_mem: list[Uop] = []  # loads ready but blocked by memory ordering
        self.div_free = 0
        self.fetch_pc, self.fetch_k = 0, (0 if self.training == "path" else None)
        self.fetch_stall = 0  # fetch resumes at this cycle
        self.trained = -1
        self.seq = 0
        self.ras: list[int] = []
        self.jtarget: dict[int, int] = {}
        self.wait_table: set[int] = set()
        self.barriers: list[Uop] = []  # renamed reads of the cycle counter: nothing younger issues past them
        self.unresolved: list[Uop] = []  # (secure) branches and jalrs renamed but not yet executed, oldest first
        self.parked: list[Uop] = []  # (secure) loads complete but not yet allowed to pass their value on
        self._dec: dict[int, tuple] = {}
        while not self.halted:
            if self.cycles >= self.max_cycles:
                raise RuntimeError("no halt")
            self._commit(W)
            if self.halted:
                break
            self._wake()
            self._issue(W)
            self._rename(W)
            self._fetch(W)
            if self.occupancy is not None:
                self.occupancy.append(len(self.rob))
            self.cycles += 1
        return self

    @property
    def ipc(self) -> float:
        return self.committed / max(self.cycles, 1)

    # -- fetch ----------------------------------------------------------------------------------------------
    def _decode(self, pc: int):
        d = self._dec.get(pc)
        if d is None:
            if pc & 3 or pc + 4 > self.mem_size:
                return None
            w = int.from_bytes(self.mem[pc:pc + 4], "little")
            if (w >> 26) & 0x3F not in OPS:
                d = (w, None)
            else:
                d = (w, decode(w))
            self._dec[pc] = d
        return d

    def _fetch(self, W: int):
        if self.cycles < self.fetch_stall or self.fetch_pc is None:
            return
        if len(self.fq) >= 4 * W:
            return
        for _ in range(W):
            pc = self.fetch_pc
            d = self._decode(pc)
            k = self.fetch_k
            if d is None:  # a wrong path ran off the program: wait for the squash
                self.fetch_pc = None
                return
            w, ins = d
            u = Uop(self.seq, pc, w, k, ins)
            self.seq += 1
            u.t[0] = self.cycles
            nxt = pc + 4
            actual = self.path[k + 1] if k is not None and k + 1 < len(self.path) else None
            if ins is None:
                u.op = "?"
                u.exc = f"illegal instruction {w:#010x}"
            else:
                u.op = op = ins.op
                if op in BRANCH:
                    target = pc + 4 * ins.imm
                    if self.perfect and actual is not None:
                        guess = actual == target
                    elif self.predictor is not None:
                        guess = self.predictor.predict(pc)
                    else:
                        guess = False
                    if k is not None and k > self.trained and self.predictor is not None and actual is not None:
                        self.predictor.update(pc, actual == target)
                    nxt = target if guess else pc + 4
                elif op == "jal":
                    nxt = pc + 4 * ins.imm
                    if ins.rd == 1:
                        self._push(pc + 4)
                elif op == "jalr":
                    if self.perfect and actual is not None:
                        nxt = actual
                    elif ins.rs1 == 1 and ins.rd == 0 and self.ras:
                        nxt = self.ras.pop()
                    else:
                        nxt = self.jtarget.get(pc, pc + 4)
                    if ins.rd == 1:
                        self._push(pc + 4)
                elif op == "halt":
                    nxt = None
            if k is not None:
                self.trained = max(self.trained, k)
            u.pred = nxt if nxt is not None else pc
            u.ras = tuple(self.ras)
            self.fq.append((self.cycles + self.fe_depth, u))
            if k is not None and (actual is None or nxt != actual):
                self.fetch_k = None  # from here on, the wrong path
            elif k is not None:
                self.fetch_k = k + 1
            if nxt is None:
                self.fetch_pc = None
                return
            self.fetch_pc = nxt
            if nxt != pc + 4:  # one taken branch a cycle
                return

    def _push(self, ret: int):
        self.ras.append(ret)
        if len(self.ras) > 16:
            self.ras.pop(0)

    # -- rename and dispatch --------------------------------------------------------------------------------
    def _rename(self, W: int):
        n = 0
        while self.fq and n < W and self.fq[0][0] <= self.cycles:
            u = self.fq[0][1]
            if len(self.rob) >= self.rob_size:
                self.stats["rob_full"] += 1
                return
            if self.iq >= self.iq_size:
                self.stats["iq_full"] += 1
                return
            mem_op = u.op in LOADS or u.op in STORES
            if mem_op and len(self.sq) + len(self.lq) >= self.lsq_size:
                self.stats["lsq_full"] += 1
                return
            self.fq.pop(0)
            n += 1
            u.t[1] = self.cycles
            ins = u.ins
            if ins is not None:
                u.rd = dest(ins)
                for r in sources(ins):
                    p = self.rat[r] if r else None
                    if p is not None and p.state < 2:
                        u.srcs.append((r, p))
                        p.consumers.append(u)
                        u.left += 1
                    elif p is not None:
                        u.srcs.append((r, p))
                    else:
                        u.srcs.append((r, None))
                if u.op in LOADS:  # a read of the cycle counter is serializing from the moment it is renamed
                    r, p = u.srcs[0]
                    base = 0 if r == 0 else (self.regs[r] if p is None else (p.result if p.state == 2 else None))
                    if base is not None and (base + ins.imm) & MASK == IO_CYCLES:
                        self.barriers.append(u)
                if u.rd:
                    self.rat[u.rd] = u
            self.rob.append(u)
            if self.secure and (u.op in BRANCH or u.op == "jalr"):
                self.unresolved.append(u)
            if u.op in STORES:
                self.sq.append(u)
            elif u.op in LOADS:
                self.lq.append(u)
            if self.record and len(self.timeline) < self.record and u.seq >= self.record_start:
                self.timeline.append(u)
            if ins is None or u.op == "halt":
                u.state = 2
                u.t[3] = self.cycles
                continue
            self.iq += 1
            if u.left == 0:
                heapq.heappush(self.ready, (u.seq, id(u), u))

    # -- wakeup -----------------------------------------------------------------------------------------------
    def _wake(self):
        if self.secure:
            self._release()
        for u in self.waking.pop(self.cycles, ()):
            if u.squashed:
                continue
            if self.secure and u.op in LOADS and self._shadowed(u):
                self.parked.append(u)  # complete, but its value stays put until no older guess is pending
                continue
            self._broadcast(u)

    def _shadowed(self, u: Uop) -> bool:
        for b in self.unresolved:
            if b.squashed or b.state == 2:
                continue
            return b.seq < u.seq
        return False

    def _release(self):
        self.unresolved = [b for b in self.unresolved if not b.squashed and b.state < 2]
        if not self.parked:
            return
        keep = []
        for u in self.parked:
            if u.squashed:
                continue
            if self._shadowed(u):
                keep.append(u)
            else:
                self._broadcast(u)
        self.parked = keep

    def _broadcast(self, u: Uop):
        u.state = 2
        u.t[3] = self.cycles
        for c in u.consumers:
            if not c.squashed:
                c.left -= 1
                if c.left == 0 and c.state == 0:
                    heapq.heappush(self.ready, (c.seq, id(c), c))
        if u.op in BRANCH or u.op == "jalr":
            self._resolve(u)
        if u.op in STORES and self.disamb != "conservative":
            self._check_order(u)

    def _value(self, u: Uop, i: int) -> int:
        r, p = u.srcs[i]
        if r == 0:
            return 0
        return p.result if p is not None else self.regs[r]

    def _resolve(self, u: Uop):
        if u.nxt != u.pred:
            self.stats["mispredicts"] += 1
            self._squash_after(u)
            self.fetch_pc = u.nxt
            self.fetch_k = None if u.k is None else u.k + 1
            self.fetch_stall = self.cycles + 1
        if u.op == "jalr":
            self.jtarget[u.pc] = u.nxt

    def _check_order(self, s: Uop):
        """A store's address is now known: did a younger load already read those bytes from elsewhere?"""
        hi = s.addr + s.size
        for x in self.lq:
            if x.seq <= s.seq or x.state == 0 or x.addr is None:
                continue
            if x.addr < hi and s.addr < x.addr + x.size and (x.fwd_from is None or x.fwd_from.seq < s.seq):
                self.stats["violations"] += 1
                self.wait_table.add(x.pc)
                self._squash_from(x)
                self.fetch_pc = x.pc
                self.fetch_k = x.k
                self.fetch_stall = self.cycles + 1
                return

    # -- squash -------------------------------------------------------------------------------------------------
    def _squash_after(self, u: Uop):
        self._squash(lambda x: x.seq > u.seq)
        self.ras = list(u.ras)

    def _squash_from(self, u: Uop):
        self._squash(lambda x: x.seq >= u.seq)
        self.ras = list(u.ras)

    def _squash(self, gone):
        keep = []
        for x in self.rob:
            if gone(x):
                x.squashed = True
                self.stats["squashed"] += 1
                if x.state == 0 and x.op not in ("?", "halt"):
                    self.iq -= 1
            else:
                keep.append(x)
        self.rob = keep
        self.sq = [x for x in self.sq if not x.squashed]
        self.lq = [x for x in self.lq if not x.squashed]
        for _, x in self.fq:
            x.squashed = True
        self.fq = []
        self.pending_mem = [x for x in self.pending_mem if not x.squashed]
        self.barriers = [x for x in self.barriers if not x.squashed]
        self.rat = [None] * NREGS
        for x in self.rob:
            if x.rd:
                self.rat[x.rd] = x

    # -- issue and execute ----------------------------------------------------------------------------------------
    def _issue(self, W: int):
        alus, mem_ports, mul = W, 2, 1
        issued = 0
        retry = []
        # loads that were waiting for memory ordering first, oldest first
        cand = sorted(self.pending_mem, key=lambda x: x.seq)
        self.pending_mem = []
        while cand or self.ready:
            if issued >= W + 2:
                break
            if cand and (not self.ready or cand[0].seq < self.ready[0][0]):
                u = cand.pop(0)
            else:
                u = heapq.heappop(self.ready)[2]
            if u.squashed or u.state != 0:
                continue
            if self.barriers and u.seq > self.barriers[0].seq:
                retry.append(u)
                continue
            op = u.op
            if op in LOADS or op in STORES:
                if mem_ports == 0:
                    retry.append(u)
                    continue
                if op in LOADS:
                    r = self._load(u)
                    if r == "wait":
                        self.pending_mem.append(u)
                        continue
                    mem_ports -= 1
                else:
                    self._store(u)
                    mem_ports -= 1
            elif op in ("div", "rem"):
                if self.div_free > self.cycles:
                    retry.append(u)
                    continue
                self.div_free = self.cycles + DIV_CYCLES
                self._execute(u, DIV_CYCLES)
            elif op in ("mul", "mulh"):
                if mul == 0:
                    retry.append(u)
                    continue
                mul -= 1
                self._execute(u, 1)
            else:
                if alus == 0:
                    retry.append(u)
                    continue
                alus -= 1
                self._execute(u, 1)
            issued += 1
        self.pending_mem.extend(x for x in cand if not x.squashed)  # not reached this cycle
        for u in retry:
            if not u.squashed:
                heapq.heappush(self.ready, (u.seq, id(u), u))

    def _finish(self, u: Uop, lat: int):
        u.state = 1
        u.t[2] = self.cycles
        self.iq -= 1
        self.waking.setdefault(self.cycles + lat, []).append(u)

    def _execute(self, u: Uop, lat: int):
        ins = u.ins
        a = self._value(u, 0) if u.srcs else 0
        b = self._value(u, 1) if len(u.srcs) > 1 else 0
        op = u.op
        u.nxt = u.pc + 4
        if op in BRANCH:
            self.stats["branches"] += 1
            if taken(op, a, b):
                u.nxt = (u.pc + 4 * ins.imm) & MASK
        elif op == "jal":
            u.result = (u.pc + 4) & MASK
            u.nxt = (u.pc + 4 * ins.imm) & MASK
        elif op == "jalr":
            u.result = (u.pc + 4) & MASK
            u.nxt = (a + ins.imm) & MASK & ~3
        elif op in ("div", "rem") and b == 0:
            u.exc = "division by zero"
            u.result = 0
        else:
            v = mext(op, a, b) if op in ("mul", "mulh", "div", "rem") else alu(op, a, b, ins.imm, u.pc)
            u.result = None if v is None else v & MASK
        self._finish(u, lat)

    def _load(self, u: Uop):
        ins = u.ins
        if u.addr is None:
            u.addr = (self._value(u, 0) + ins.imm) & MASK
            u.size = 4 if u.op == "lw" else 1
            u.exc = self._check(u)
        if u.addr >= IO_BASE:  # devices: only at the head, and a barrier
            if self.rob[0] is not u:
                return "wait"
            try:
                u.result = self._device_load(u.addr)
            except MachineError as e:
                u.exc, u.result = str(e), 0
            if u.addr == IO_CYCLES and u not in self.barriers:
                # not recognised at rename (its base was not yet known): discard and redo younger work
                self._squash_after(u)
                self.fetch_pc = u.pc + 4
                self.fetch_k = None if u.k is None else u.k + 1
                self.fetch_stall = self.cycles + 1
                self.barriers.insert(0, u)
            self._finish(u, 1)
            return "ok"
        if u.exc:
            u.result = 0
            self._finish(u, 1)
            return "ok"
        conservative = self.disamb == "conservative" or (self.disamb == "wait-table" and u.pc in self.wait_table)
        src = None
        for s in reversed(self.sq):
            if s.seq >= u.seq:
                continue
            if s.addr is None:
                if conservative:
                    return "wait"
                continue
            if s.addr < u.addr + u.size and u.addr < s.addr + s.size:
                src = s
                break
        if src is not None:
            covers = src.addr <= u.addr and u.addr + u.size <= src.addr + src.size
            if not covers or src.sdata is None:
                return "wait"  # a partial overlap, or the data is not ready: wait for the store
            raw = src.sdata if src.size == 4 else src.sdata & 0xFF
            off = u.addr - src.addr
            v = (raw >> (8 * off)) & (MASK if u.size == 4 else 0xFF)
            if u.op == "lb" and v & 0x80:
                v = (v - 256) & MASK
            u.result = v
            u.fwd_from = src
            self.stats["forwarded"] += 1
            self._finish(u, self.mem_latency)
            return "ok"
        u.result = self._read(u.addr, u.size, u.op == "lb")
        u.fwd_from = None
        lat = self.cache.access(u.addr) if self.cache is not None else self.mem_latency
        if u.k is None:
            self.stats["wrong_path_loads"] += 1
        self._finish(u, lat)
        return "ok"

    def _store(self, u: Uop):
        ins = u.ins
        a = self._value(u, 0)
        u.addr = (a + ins.imm) & MASK
        u.size = 4 if u.op == "sw" else 1
        u.sdata = self._value(u, 1) & MASK
        u.exc = self._check(u)
        self._finish(u, 1)

    # -- commit -------------------------------------------------------------------------------------------------
    def _commit(self, W: int):
        n = 0
        while self.rob and n < W:
            u = self.rob[0]
            if u.state < 2:
                return
            if u.exc:
                self.error = f"{u.exc} at pc {u.pc:#x}"
                self.halted = True
                return
            self.rob.pop(0)
            if self.sq and self.sq[0] is u:
                self.sq.pop(0)
            elif self.lq and self.lq[0] is u:
                self.lq.pop(0)
            n += 1
            u.t[4] = self.cycles
            op = u.op
            if op == "halt":
                self.committed += 1
                self.halted = True
                return
            if op in BRANCH and self.training == "commit" and self.predictor is not None:
                self.predictor.update(u.pc, u.nxt != u.pc + 4)
            if op in STORES:
                if u.addr >= IO_BASE:
                    if u.addr == IO_CONSOLE:
                        self.output.append(u.sdata & 0xFF)
                    elif u.addr == IO_FLUSH:
                        if self.cache is not None:
                            if u.sdata == MASK:
                                self.cache.flush()
                            else:
                                self.cache.flush_line(u.sdata)
                    else:
                        self.error = f"store to unmapped device {u.addr:#010x} at pc {u.pc:#x}"
                        self.halted = True
                        return
                elif u.size == 4:
                    self.mem[u.addr:u.addr + 4] = u.sdata.to_bytes(4, "little")
                else:
                    self.mem[u.addr] = u.sdata & 0xFF
                self._dec.pop(u.addr & ~3, None)
                if self.cache is not None and u.addr < IO_BASE:
                    self.cache.access(u.addr)
            if u.rd and u.result is not None:
                self.regs[u.rd] = u.result
                if self.rat[u.rd] is u:
                    self.rat[u.rd] = None
            if self.barriers and self.barriers[0] is u:
                self.barriers.pop(0)
            self.committed += 1
