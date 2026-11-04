"""Pebble's five-stage pipeline, simulated cycle by cycle (Part 7).

    p = Pipeline(program.image, tape=b"...", predictor=predict.TwoBit(), forwarding=True)
    p.run()
    p.cycles, p.retired, p.stats, p.regs, p.output

Five instructions are in flight at once, one per stage, with a pipeline register between each pair of stages:

    IF   fetch the word at pc; guess the next pc (branch target buffer, predictor, return-address stack)
    ID   decode; read the register file (written in the first half of the cycle, read in the second);
         stall a load's immediate consumer; redirect fetch for a jal the BTB missed
    EX   the ALU, with operands forwarded from EX/MEM and MEM/WB; resolve branches and jalr; on a wrong guess,
         flush the two younger instructions and refetch
    MEM  loads and stores (and the devices of isa.py)
    WB   write the register file

The pipeline is checked against the emulator (tests/test_cs7_pipeline.py): the same registers, memory, output and
instruction count on every program, and a cycle count equal to (instructions + 4) plus the bubbles it reports.
One deliberate gap: an instruction is fetched before an older store in MEM has written memory, so code that
rewrites itself a few instructions ahead runs stale words, as on a real pipeline without an instruction fence.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .isa import IO_BASE, IO_CONSOLE, IO_CYCLES, IO_TAPE, MASK, NREGS, OPS, decode, sext

BRANCH = ("beq", "bne", "blt", "bge", "bltu", "bgeu")
DIVIDES = ("div", "rem")
DIV_CYCLES = 16  # Part 4's radix-4 SRT divider: two quotient bits a cycle, not pipelined
LOADS = ("lw", "lb", "lbu")
STORES = ("sw", "sb")


def sources(i) -> tuple[int, ...]:
    """The registers an instruction reads (and needs by EX)."""
    if i.op in ("jal", "lui", "halt"):
        return ()
    if i.fmt == "R" or i.op in BRANCH or i.op in STORES:
        return (i.rs1, i.rs2)
    return (i.rs1,)


def dest(i) -> int:
    if i.op in BRANCH or i.op in STORES or i.op == "halt":
        return 0
    return i.rd


def alu(op: str, a: int, b: int, imm: int, pc: int) -> int | None:
    """The value an instruction writes (loads: the address; branches: None)."""
    if op in ("add", "addi"):
        return a + (b if op == "add" else imm)
    if op == "sub":
        return a - b
    if op in ("and", "andi"):
        return a & (b if op == "and" else imm & MASK)
    if op in ("or", "ori"):
        return a | (b if op == "or" else imm & MASK)
    if op in ("xor", "xori"):
        return a ^ (b if op == "xor" else imm & MASK)
    if op in ("sll", "slli"):
        return a << ((b if op == "sll" else imm) & 31)
    if op in ("srl", "srli"):
        return a >> ((b if op == "srl" else imm) & 31)
    if op in ("sra", "srai"):
        return sext(a, 32) >> ((b if op == "sra" else imm) & 31)
    if op == "slt":
        return int(sext(a, 32) < sext(b, 32))
    if op == "slti":
        return int(sext(a, 32) < imm)
    if op == "sltu":
        return int(a < b)
    if op == "sltiu":
        return int(a < (imm & MASK))
    if op in LOADS or op in STORES:
        return (a + imm) & MASK
    if op in ("jal", "jalr"):
        return pc + 4
    if op == "lui":
        return imm << 10
    if op in ("mul", "mulh", "div", "rem"):
        from .emu import mext

        return mext(op, a, b)
    return None


def taken(op: str, a: int, b: int) -> bool:
    if op == "beq":
        return a == b
    if op == "bne":
        return a != b
    if op == "blt":
        return sext(a, 32) < sext(b, 32)
    if op == "bge":
        return sext(a, 32) >= sext(b, 32)
    if op == "bltu":
        return a < b
    return a >= b


@dataclass
class Slot:
    """One instruction in flight."""

    seq: int
    pc: int
    word: int
    ins: object = None
    pred: int = 0  # the next pc IF guessed
    a: int = 0
    b: int = 0
    value: int | None = None  # the result (or the address, for memory instructions)
    store: int = 0
    illegal: bool = False
    exc: str | None = None  # an exception raised in EX, taken when the instruction reaches WB (precise)
    left: int | None = None  # cycles a divide still occupies EX


class BTB:
    """A direct-mapped branch target buffer: pc -> (kind, target)."""

    def __init__(self, entries: int = 512):
        self.n = entries
        self.tab: dict[int, tuple[int, str, int]] = {}

    def get(self, pc: int):
        e = self.tab.get((pc >> 2) % self.n)
        return (e[1], e[2]) if e and e[0] == pc else None

    def put(self, pc: int, kind: str, target: int):
        self.tab[(pc >> 2) % self.n] = (pc, kind, target)


@dataclass
class Pipeline:
    image: bytes = b""
    tape: bytes = b""
    mem_size: int = 1 << 20
    predictor: object = None  # explainer.cs.pebble.predict.*; None: predict not taken
    forwarding: bool = True
    btb_entries: int = 512  # 0: no BTB, so a taken branch or jump is always a redirect
    ras_depth: int = 16  # 0: no return-address stack
    record: int = 0  # keep a chart of the first `record` cycles
    stats: dict = field(default_factory=dict)

    def __post_init__(self):
        self.mem = bytearray(self.mem_size)
        self.mem[: len(self.image)] = self.image
        self.regs = [0] * NREGS
        self.regs[2] = self.mem_size
        self.pc = 0
        self.ifid = self.idex = self.exmem = self.memwb = None
        self.cycles = 0
        self.retired = 0
        self.seq = 0
        self.halted = False
        self.error = None
        self.output = bytearray()
        self.tape_pos = 0
        self.btb = BTB(self.btb_entries) if self.btb_entries else None
        self.ras: list[int] = []
        self.stats = {"load_use": 0, "raw": 0, "branch_flush": 0, "jump_redirect": 0, "jalr_flush": 0,
                      "divide": 0, "branches": 0, "mispredicts": 0, "jalr": 0, "jalr_miss": 0}
        self.chart: list[dict] = []
        self.counts: dict[str, int] = {}

    # -- memory ---------------------------------------------------------------
    def load(self, addr: int, size: int, signed_: bool) -> int:
        if addr >= IO_BASE:
            if addr == IO_TAPE:
                if self.tape_pos < len(self.tape):
                    self.tape_pos += 1
                    return self.tape[self.tape_pos - 1]
                return MASK
            if addr == IO_CYCLES:
                return self.retired & MASK
            raise RuntimeError(f"load from unmapped device {addr:#x}")
        if size == 4:
            return int.from_bytes(self.mem[addr:addr + 4], "little")
        v = self.mem[addr]
        return (v - 256) & MASK if signed_ and v & 0x80 else v

    def store(self, addr: int, size: int, value: int) -> None:
        if addr >= IO_BASE:
            if addr == IO_CONSOLE:
                self.output.append(value & 0xFF)
                return
            raise RuntimeError(f"store to unmapped device {addr:#x}")
        if size == 4:
            self.mem[addr:addr + 4] = (value & MASK).to_bytes(4, "little")
        else:
            self.mem[addr] = value & 0xFF

    # -- one clock cycle --------------------------------------------------------
    def step(self) -> None:
        st = self.stats
        rec = {"IF": None, "ID": None, "EX": None, "MEM": None, "WB": None, "events": []} if \
            self.cycles < self.record else None
        # IF reads memory before this cycle's store lands (see the module docstring)
        fetch_word = int.from_bytes(self.mem[self.pc:self.pc + 4], "little") if self.pc + 4 <= self.mem_size else 0

        # WB: write the register file (first half of the cycle)
        wb = self.memwb
        if wb is not None:
            if rec is not None:
                rec["WB"] = wb.seq
            if wb.illegal or wb.exc:
                self.error = (f"illegal instruction {wb.word:#010x}" if wb.illegal else wb.exc) + f" at pc {wb.pc:#x}"
                self.halted = True
                self.memwb = None
                self.cycles += 1
                return
            d = dest(wb.ins)
            if d and wb.value is not None:
                self.regs[d] = wb.value & MASK
            self.retired += 1
            self.counts[wb.ins.op] = self.counts.get(wb.ins.op, 0) + 1
            if wb.ins.op == "halt":
                self.halted = True
                self.cycles += 1
                if rec is not None:
                    self.chart.append(rec)
                return

        # MEM
        mem = self.exmem
        new_memwb = None
        if mem is not None:
            if rec is not None:
                rec["MEM"] = mem.seq
            op = mem.ins.op if mem.ins else None
            if op in LOADS:
                mem.value = self.load(mem.value, 4 if op == "lw" else 1, op == "lb")
            elif op in STORES:
                self.store(mem.value, 4 if op == "sw" else 1, mem.store)
            new_memwb = mem

        # EX, with forwarding from EX/MEM (the instruction one ahead) and MEM/WB (two ahead)
        ex = self.idex
        new_exmem = None
        flush_to = None
        ex_hold = False
        if ex is not None:
            if rec is not None:
                rec["EX"] = ex.seq
            i = ex.ins
            if not ex.illegal:
                srcs = sources(i)
                vals = [ex.a, ex.b]
                for k, r in enumerate(srcs):
                    if r == 0:
                        continue
                    if self.forwarding:
                        if mem is not None and mem.ins and dest(mem.ins) == r and mem.ins.op not in LOADS:
                            vals[k] = mem.value  # EX/MEM -> EX
                            if rec is not None:
                                rec["events"].append(("fwd", mem.seq, ex.seq, "EX/MEM"))
                        elif wb is not None and wb.ins and dest(wb.ins) == r:
                            vals[k] = wb.value  # MEM/WB -> EX
                            if rec is not None:
                                rec["events"].append(("fwd", wb.seq, ex.seq, "MEM/WB"))
                a, b = vals[0], vals[1]
                if ex.left is None:  # the first cycle in EX: operands are final here
                    try:
                        v = alu(i.op, a, b, i.imm, ex.pc)
                    except Exception as err:  # division by zero
                        v, ex.exc = None, str(err)
                    ex.value = None if v is None else v & MASK
                    ex.left = DIV_CYCLES - 1 if i.op in DIVIDES else 0
                if i.op in STORES:
                    ex.store = b
                actual = ex.pc + 4
                if i.op in BRANCH:
                    t = taken(i.op, a, b)
                    st["branches"] += 1
                    if self.predictor is not None:
                        self.predictor.update(ex.pc, t)
                    if t:
                        actual = (ex.pc + 4 * i.imm) & MASK
                        if self.btb:
                            self.btb.put(ex.pc, "br", actual)
                    if actual != ex.pred:
                        st["mispredicts"] += 1
                        flush_to = actual
                        st["branch_flush"] += 1 + (self.ifid is not None)
                elif i.op == "jalr":
                    st["jalr"] += 1
                    actual = (a + i.imm) & MASK & ~3
                    if self.btb:
                        self.btb.put(ex.pc, "ret" if (i.rs1 == 1 and i.rd == 0) else "jalr", actual)
                    if actual != ex.pred:
                        st["jalr_miss"] += 1
                        flush_to = actual
                        st["jalr_flush"] += 1 + (self.ifid is not None)
            new_exmem = ex
            if ex.left:
                ex.left -= 1
                ex_hold = True
                new_exmem = None
                st["divide"] += 1

        # ID: decode, read registers, detect the load-use (or, without forwarding, any RAW) hazard
        idd = self.ifid
        stall = False
        redirect_to = None
        new_idex = None
        if idd is not None and flush_to is None and not ex_hold:
            if rec is not None:
                rec["ID"] = idd.seq
            if not idd.illegal:
                i = idd.ins
                srcs = [r for r in sources(i) if r]
                if self.forwarding:
                    if ex is not None and ex.ins and ex.ins.op in LOADS and dest(ex.ins) in srcs:
                        stall = True
                        st["load_use"] += 1
                else:
                    producers = [s for s in (ex, mem) if s is not None and s.ins]
                    if any(dest(s.ins) in srcs for s in producers):
                        stall = True
                        st["raw"] += 1
                if not stall:
                    idd.a = self.regs[i.rs1]
                    idd.b = self.regs[i.rs2]
                    if i.op == "jal":
                        target = (idd.pc + 4 * i.imm) & MASK
                        if self.btb:
                            self.btb.put(idd.pc, "jal", target)
                        if i.rd == 1 and self.ras_depth:
                            self._push(idd.pc + 4)
                        if idd.pred != target:
                            redirect_to = target
                            st["jump_redirect"] += 1
                    elif i.op == "jalr" and i.rd == 1 and self.ras_depth:
                        self._push(idd.pc + 4)
            if not stall:
                new_idex = idd
            if stall and rec is not None:
                rec["events"].append(("stall", idd.seq))

        # IF
        new_ifid = None
        if ex_hold:  # a divide occupies EX: everything behind it waits (a structural hazard)
            new_ifid, new_idex = self.ifid, ex
            if rec is not None:
                rec["IF"] = self.seq
                rec["events"].append(("busy", ex.seq))
        elif flush_to is not None:
            if rec is not None:
                rec["events"].append(("flush", [s.seq for s in (self.ifid,) if s] + [self.seq]))
            self.seq += 1  # the instruction fetched this cycle is thrown away too
            self.pc = flush_to
            new_ifid = None
            new_idex = None
        elif stall:
            new_ifid = self.ifid  # hold IF/ID and pc; a bubble goes down the pipe
            new_idex = None
            if rec is not None:
                rec["IF"] = self.seq
        elif redirect_to is not None:
            if rec is not None:
                rec["events"].append(("flush", [self.seq]))
            self.seq += 1
            self.pc = redirect_to
        else:
            slot = Slot(self.seq, self.pc, fetch_word)
            if rec is not None:
                rec["IF"] = self.seq
            self.seq += 1
            opc = (fetch_word >> 26) & 0x3F
            if opc not in OPS:
                slot.illegal = True
                slot.pred = self.pc + 4
            else:
                slot.ins = decode(fetch_word)
                slot.pred = self._guess(self.pc, slot.ins)
            self.pc = slot.pred
            new_ifid = slot

        self.ifid, self.idex, self.exmem, self.memwb = new_ifid, new_idex, new_exmem, new_memwb
        self.cycles += 1
        if rec is not None:
            self.chart.append(rec)

    def _push(self, addr: int) -> None:
        self.ras.append(addr)
        if len(self.ras) > self.ras_depth:
            self.ras.pop(0)

    def _guess(self, pc: int, ins) -> int:
        e = self.btb.get(pc) if self.btb else None
        if e is None:
            return pc + 4
        kind, target = e
        if kind == "jal":
            return target
        if kind == "ret" and self.ras:
            return self.ras.pop()
        if kind in ("jalr", "ret"):
            return target
        if self.predictor is not None and self.predictor.predict(pc):
            return target
        return pc + 4

    def run(self, max_cycles: int = 200_000_000) -> "Pipeline":
        for _ in range(max_cycles):
            if self.halted:
                break
            self.step()
        else:
            raise RuntimeError("no halt")
        return self

    @property
    def bubbles(self) -> int:
        s = self.stats
        return s["load_use"] + s["raw"] + s["branch_flush"] + s["jump_redirect"] + s["jalr_flush"] + s["divide"]

    @property
    def cpi(self) -> float:
        return self.cycles / max(self.retired, 1)


def run(program, tape: bytes = b"", **kw) -> Pipeline:
    image = getattr(program, "image", program)
    max_cycles = kw.pop("max_cycles", 200_000_000)
    return Pipeline(image=image, tape=tape, **kw).run(max_cycles)
