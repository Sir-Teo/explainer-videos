"""Pebble-32 at gate level: the single-cycle CPU of Part 6, built from the blocks of Parts 3–5.

    cpu = build_cpu(control="table")        # or "minimized": the control unit as a PLA or as minimized logic
    m = GateMachine(cpu, program.image, tape=b"...")
    m.run()                                 # every instruction a clock cycle of the whole netlist
    m.regs, m.output, m.steps

One clock cycle does a whole instruction.  The instruction word arrives from memory at the address in ``pc``; the
control unit decodes its opcode into the signals that steer the datapath; the register file is read; Part 4's ALU
computes; memory is read or written at the ALU's result; the result (or the loaded word, or ``pc + 4``) is written
back; and ``pc`` loads the next address.  Memory itself is outside the netlist, as RAM chips are outside a
processor: the netlist has an address and data bus to it.  Because a single-cycle machine reads memory within the
cycle, each cycle evaluates the netlist twice: once to learn the data address, then again with the loaded word on
the bus (the address does not depend on the loaded word, so this is exactly a combinational memory).

``GateMachine`` is checked against the emulator (:mod:`.emu`) on random programs and on real ones
(``tests/test_cs6_cpu.py``): same registers, memory, output and step count.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import blocks as B
from .fast import Fast
from .hdl import Circuit
from .isa import IO_BASE, IO_CONSOLE, IO_CYCLES, IO_TAPE, MASK, NREGS, OPS
from .logic import Literals, min_cover, sop
from .seq import Seq

ALU = {name: k for k, name in enumerate(B.ALU_OPS)}
WB = {"alu": 0, "load": 1, "link": 2, "lui": 3}

# the control signals, in the order the control word is drawn
SIGNALS = ("rw", "imm", "aop0", "aop1", "aop2", "aop3", "sf", "jf", "ld", "st", "byte", "sgn", "wb0", "wb1", "br",
           "bz", "bn", "jal", "jalr", "halt")
SIGNAL_INFO = {
    "rw": "write a register", "imm": "ALU's second input is the immediate", "aop0": "ALU operation (4 bits)",
    "sf": "S format: registers in the rs1, rs2 fields", "jf": "22-bit immediate (J format)", "ld": "load",
    "st": "store", "byte": "byte-sized memory access", "sgn": "sign-extend the loaded byte",
    "wb0": "what is written back (2 bits)", "br": "conditional branch", "bz": "branch tests the zero flag",
    "bn": "branch on the opposite", "jal": "jump", "jalr": "jump to a register", "halt": "stop",
}


def control_word(op: str) -> dict[str, int]:
    """What each instruction asks of the datapath: the truth table of the control unit, one row per opcode."""
    f = OPS[next(k for k, (m, _) in OPS.items() if m == op)][1]
    s = dict.fromkeys(SIGNALS, 0)
    aop = "add"
    wb = "alu"
    if f == "R":
        s["rw"] = 1
        aop = op
    elif op in ("addi", "andi", "ori", "xori", "slti", "sltiu", "slli", "srli", "srai"):
        s["rw"], s["imm"] = 1, 1
        aop = {"addi": "add", "andi": "and", "ori": "or", "xori": "xor", "slti": "slt", "sltiu": "sltu",
               "slli": "sll", "srli": "srl", "srai": "sra"}[op]
    elif op in ("lw", "lb", "lbu"):
        s["rw"], s["imm"], s["ld"] = 1, 1, 1
        s["byte"] = int(op != "lw")
        s["sgn"] = int(op == "lb")
        wb = "load"
    elif op in ("sw", "sb"):
        s["imm"], s["st"], s["sf"] = 1, 1, 1
        s["byte"] = int(op == "sb")
    elif op in ("beq", "bne", "blt", "bge", "bltu", "bgeu"):
        s["br"], s["sf"] = 1, 1
        aop = {"beq": "sub", "bne": "sub", "blt": "slt", "bge": "slt", "bltu": "sltu", "bgeu": "sltu"}[op]
        s["bz"] = int(op in ("beq", "bne"))
        s["bn"] = int(op in ("bne", "bge", "bgeu"))
    elif op == "jal":
        s["rw"], s["jf"], s["jal"] = 1, 1, 1
        wb = "link"
    elif op == "jalr":
        s["rw"], s["imm"], s["jalr"] = 1, 1, 1
        wb = "link"
    elif op == "lui":
        s["rw"], s["jf"] = 1, 1
        wb = "lui"
    elif op == "halt":
        s["halt"] = 1
    for i in range(4):
        s[f"aop{i}"] = (ALU[aop] >> i) & 1
    s["wb0"], s["wb1"] = WB[wb] & 1, WB[wb] >> 1
    return s


def control_table() -> dict[int, dict[str, int]]:
    """The base instruction set only: the gate-level CPU leaves the M extension (Part 7) illegal."""
    from .isa import M_EXT

    return {code: control_word(m) for code, (m, _) in sorted(OPS.items()) if m not in M_EXT}


def build_control(c: Circuit, op: list[int], style: str = "table") -> tuple[dict[str, int], dict]:
    """The control unit on the 6 opcode bits.

    ``table``: a decoder line per defined opcode (an AND of six literals) and an OR of the lines where each signal is
    1: a ROM, or a PLA with one product term per opcode.  ``minimized``: each signal as a minimized sum of products
    with the undefined opcodes as don't-cares, product terms shared between signals.  Either way ``ill`` is exact:
    1 for every undefined opcode."""
    table = control_table()
    lits = Literals(c, op)
    defined = set(table)
    info = {}
    if style == "table":
        lines = {code: sop(c, [(code, 0)], lits) for code in table}
        out = {}
        for sig in SIGNALS:
            ones = [lines[k] for k, w in table.items() if w[sig]]
            out[sig] = B.tree(c, c.or_, ones) if ones else c.const(0)
        out["ill"] = c.not_(B.tree(c, c.or_, list(lines.values())))
        info["terms"] = len(lines)
    else:
        products: dict = {}
        out = {}
        dc = set(range(64)) - defined
        nterms = 0
        for sig in SIGNALS:
            on = {k for k, w in table.items() if w[sig]}
            terms = min_cover(on, dc, 6)
            nterms += len(terms)
            out[sig] = sop(c, terms, lits, products)
        out["ill"] = sop(c, min_cover(dc, set(), 6), lits, products)
        info["terms"] = len(products)
    return out, info


def _prefix_and(c: Circuit, xs: list[int]) -> list[int]:
    """P[i] = x[0] and ... and x[i], Kogge–Stone style: log2 n levels."""
    P = list(xs)
    d = 1
    while d < len(P):
        P = [P[i] if i < d else c.and_(P[i], P[i - d]) for i in range(len(P))]
        d *= 2
    return P


def build_cpu(control: str = "table", adder: str = "kogge-stone") -> Seq:
    s = Seq(f"Pebble-32, single cycle ({control} control)")
    c = s.c
    instr = c.input("instr", 32)
    rdata = c.input("rdata", 32)
    pc = s.reg("pc", 32)
    zero = c.const(0)
    blocks: dict[str, tuple[int, int]] = {}

    def mark(name, start):
        blocks[name] = (start, len(c.kinds))

    # --- decode ---------------------------------------------------------------------------------------------
    t0 = len(c.kinds)
    op = instr[26:32]
    fa, fb, fc = instr[22:26], instr[18:22], instr[14:18]
    ctl, cinfo = build_control(c, op, control)
    mark("control", t0)

    # --- register file (Part 5): two read ports, one write port ------------------------------------------------
    t0 = len(c.kinds)
    ra = B.mux2_bus(c, ctl["sf"], fb, fa)  # S format: rs1 is in the first field
    rb = B.mux2_bus(c, ctl["sf"], fc, fb)
    regs = [None] + [s.reg(f"r{r}", 32) for r in range(1, NREGS)]

    def read(addr):
        layer = [regs[r] if regs[r] is not None else [zero] * 32 for r in range(NREGS)]
        for st in range(4):
            layer = [B.mux2_bus(c, addr[st], layer[2 * j], layer[2 * j + 1]) for j in range(len(layer) // 2)]
        return layer[0]

    A, Bv = read(ra), read(rb)
    mark("register read", t0)

    # --- immediates and the ALU (Part 4) ----------------------------------------------------------------------
    t0 = len(c.kinds)
    imm18 = instr[0:18] + [instr[17]] * 14
    imm22 = instr[0:22] + [instr[21]] * 10
    imm = B.mux2_bus(c, ctl["jf"], imm18, imm22)
    alu_b = B.mux2_bus(c, ctl["imm"], Bv, imm)
    mark("immediate", t0)
    t0 = len(c.kinds)
    y = c.embed(B.alu(32, adder), a=A, b=alu_b, op=[ctl["aop0"], ctl["aop1"], ctl["aop2"], ctl["aop3"]])
    Y, zflag = y["y"], y["zero"][0]
    mark("ALU", t0)

    # --- next pc ----------------------------------------------------------------------------------------------
    t0 = len(c.kinds)
    carry = _prefix_and(c, pc[2:])
    pc4 = pc[:2] + [c.not_(pc[2]) if i == 0 else c.xor(pc[2 + i], carry[i - 1]) for i in range(30)]
    off = [zero, zero] + imm[:30]
    tgt = c.embed(B.prefix_adder(32, adder), a=pc, b=off, cin=zero)["s"]
    cond = B.mux2(c, ctl["bz"], Y[0], zflag)
    taken = c.and_(ctl["br"], c.xor(cond, ctl["bn"]))
    jump = c.or_(taken, ctl["jal"])
    nxt = B.mux2_bus(c, jump, pc4, tgt)
    nxt = B.mux2_bus(c, ctl["jalr"], nxt, [zero, zero] + Y[2:])
    stop = c.or_(ctl["halt"], ctl["ill"])
    nxt = B.mux2_bus(c, stop, nxt, pc)
    s.set_next("pc", nxt)
    mark("next pc", t0)

    # --- memory and write-back ----------------------------------------------------------------------------------
    t0 = len(c.kinds)
    o0, o1 = Y[0], Y[1]
    bytes_ = [rdata[8 * k:8 * k + 8] for k in range(4)]
    lo = B.mux2_bus(c, o0, bytes_[0], bytes_[1])
    hi = B.mux2_bus(c, o0, bytes_[2], bytes_[3])
    byte = B.mux2_bus(c, o1, lo, hi)
    fill = c.and_(ctl["sgn"], byte[7])
    ldv = B.mux2_bus(c, ctl["byte"], rdata, byte + [fill] * 24)
    luiv = [zero] * 10 + instr[0:22]
    w0 = B.mux2_bus(c, ctl["wb0"], Y, ldv)
    w1 = B.mux2_bus(c, ctl["wb0"], pc4, luiv)
    wd = B.mux2_bus(c, ctl["wb1"], w0, w1)
    we = c.and_(ctl["rw"], c.not_(ctl["ill"]))
    nwa = [c.not_(x) for x in fa]
    for r in range(1, NREGS):
        sel = B.tree(c, c.and_, [fa[i] if (r >> i) & 1 else nwa[i] for i in range(4)] + [we])
        s.set_next(f"r{r}", B.mux2_bus(c, sel, regs[r], wd))
    mark("write-back", t0)

    c.output("pc", pc)
    c.output("addr", Y)
    c.output("wdata", Bv)
    for sig in ("ld", "st", "byte", "halt", "ill"):
        c.output(sig, ctl[sig])
    c.output("we", we)
    c.output("wd", wd)
    c.output("taken", taken)
    s.blocks = blocks
    s.control_info = cinfo
    return s


# ---------------------------------------------------------------------------
# running programs on it
# ---------------------------------------------------------------------------
@dataclass
class GateMachine:
    """Pebble at gate level, with memory and the devices of :mod:`.isa` around it.  Mirrors :class:`.emu.Machine`."""

    cpu: Seq
    image: bytes = b""
    tape: bytes = b""
    mem_size: int = 1 << 20
    trace: bool = False
    fast: Fast | None = None
    log: list = field(default_factory=list)

    def __post_init__(self):
        self.f = self.fast or Fast(self.cpu)
        self.f.reset(1)
        self.mem = bytearray(self.mem_size)
        self.mem[: len(self.image)] = self.image
        self.f.set("r2", self.mem_size)  # sp, as the emulator sets it
        self.steps = 0
        self.halted = False
        self.error = None
        self.output = bytearray()
        self.tape_pos = 0

    @property
    def regs(self) -> list[int]:
        return [0] + [int(self.f.get(f"r{r}")[0]) for r in range(1, NREGS)]

    @property
    def pc(self) -> int:
        return int(self.f.get("pc")[0])

    def _read(self, addr: int, byte: bool) -> int:
        if addr >= IO_BASE:
            if addr == IO_TAPE:
                if self.tape_pos < len(self.tape):
                    self.tape_pos += 1
                    return self.tape[self.tape_pos - 1]
                return MASK
            if addr == IO_CYCLES:
                return self.steps & MASK
            raise RuntimeError(f"load from unmapped device {addr:#010x}")
        a = addr & ~3
        return int.from_bytes(self.mem[a:a + 4], "little")

    def step(self) -> None:
        pc = self.pc
        word = int.from_bytes(self.mem[pc:pc + 4], "little")
        f = self.f
        o = f.eval({"instr": word, "rdata": 0})
        rdata = 0
        addr = int(o["addr"][0])
        if o["ld"][0]:
            rdata = self._read(addr, bool(o["byte"][0])) & MASK
        o = f.eval({"instr": word, "rdata": rdata}, commit=True)
        if o["ill"][0]:
            self.error = f"illegal instruction {word:#010x} at pc {pc:#x}"
            self.halted = True
            return
        if o["st"][0]:
            v = int(o["wdata"][0])
            if addr >= IO_BASE:
                if addr == IO_CONSOLE:
                    self.output.append(v & 0xFF)
                else:
                    raise RuntimeError(f"store to unmapped device {addr:#010x}")
            elif o["byte"][0]:
                self.mem[addr] = v & 0xFF
            else:
                self.mem[addr:addr + 4] = v.to_bytes(4, "little")
        if self.trace:
            self.log.append({"pc": pc, "word": word, "we": int(o["we"][0]), "wd": int(o["wd"][0]),
                             "taken": int(o["taken"][0]), "addr": addr})
        self.steps += 1
        if o["halt"][0]:
            self.halted = True

    def run(self, max_steps: int = 10_000_000) -> "GateMachine":
        for _ in range(max_steps):
            if self.halted:
                return self
            self.step()
        raise RuntimeError(f"no halt after {max_steps} steps")


def critical_path(cpu: Seq, samples: int = 2048, seed: int = 0) -> dict:
    """Depth (the longest path, in gates) and the settled delay (``hdl.settle``, which sees through false paths) on
    random register contents and random valid instructions."""
    c = cpu.c
    rng = np.random.default_rng(seed)
    vals = {name: rng.integers(0, 1 << min(len(ws), 62), samples, dtype=np.int64) for name, ws in c.inputs.items()}
    for name, ws in c.inputs.items():
        if len(ws) == 32:
            vals[name] = rng.integers(0, 1 << 32, samples, dtype=np.int64)
    from .isa import M_EXT

    codes = np.array(sorted(k for k, (m, _) in OPS.items() if m not in M_EXT), dtype=np.int64)
    vals["instr"] = (vals["instr"] & ((1 << 26) - 1)) | (codes[rng.integers(0, len(codes), samples)] << 26)
    t = c.settle(vals)
    return {"depth": c.depth(), "settle_max": int(np.max(t)), "settle_mean": float(np.mean(t))}
