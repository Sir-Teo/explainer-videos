"""The fast Pebble-32 emulator: the instruction set's meaning, one instruction at a time.

    m = Machine(program.image, tape=b"some input")
    m.run()                      # until halt (or max_steps)
    m.output, m.steps, m.regs

The gate-level CPU of Part 6 must agree with this machine after every program (``tests/test_cs_pebble_*.py``
co-simulate the two); the pipelines, caches and out-of-order core of Act II must leave the same architectural state.
``trace=True`` records, per step, the pc, the instruction word, and the register and memory writes, which is what
the scenes draw.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .isa import IO_BASE, IO_CONSOLE, IO_CYCLES, IO_TAPE, MASK, NREGS, OPS, decode, sext


class MachineError(RuntimeError):
    pass


@dataclass
class Step:
    pc: int
    word: int
    reg: tuple[int, int] | None = None  # (register, new value)
    mem: tuple[int, int, int] | None = None  # (address, size, value)
    taken: bool | None = None  # branches: was it taken?


@dataclass
class Machine:
    image: bytes = b""
    tape: bytes = b""
    mem_size: int = 1 << 20
    pc: int = 0
    trace: bool = False
    regs: list[int] = field(default_factory=lambda: [0] * NREGS)

    def __post_init__(self):
        self.mem = bytearray(self.mem_size)
        self.mem[: len(self.image)] = self.image
        self.regs[2] = self.mem_size  # sp: the stack starts at the top of memory and grows down
        self.halted = False
        self.steps = 0
        self.output = bytearray()
        self.tape_pos = 0
        self.log: list[Step] = []
        self.counts: dict[str, int] = {}
        self._dec: dict[int, tuple] = {}

    # -- memory -----------------------------------------------------------------
    def load(self, addr: int, size: int, signed_: bool = False) -> int:
        addr &= MASK
        if addr >= IO_BASE:
            if addr == IO_TAPE:
                if self.tape_pos < len(self.tape):
                    self.tape_pos += 1
                    return self.tape[self.tape_pos - 1]
                return MASK
            if addr == IO_CYCLES:
                return self.steps & MASK
            raise MachineError(f"load from unmapped device {addr:#010x} at pc {self.pc:#x}")
        if addr + size > self.mem_size:
            raise MachineError(f"load from {addr:#x} outside memory at pc {self.pc:#x}")
        if size == 4:
            if addr & 3:
                raise MachineError(f"misaligned word load from {addr:#x} at pc {self.pc:#x}")
            return int.from_bytes(self.mem[addr:addr + 4], "little")
        v = self.mem[addr]
        return (v - 256) & MASK if signed_ and v & 0x80 else v

    def store(self, addr: int, size: int, value: int) -> None:
        addr &= MASK
        if addr >= IO_BASE:
            if addr == IO_CONSOLE:
                self.output.append(value & 0xFF)
                return
            raise MachineError(f"store to unmapped device {addr:#010x} at pc {self.pc:#x}")
        if addr + size > self.mem_size:
            raise MachineError(f"store to {addr:#x} outside memory at pc {self.pc:#x}")
        if size == 4:
            if addr & 3:
                raise MachineError(f"misaligned word store to {addr:#x} at pc {self.pc:#x}")
            self.mem[addr:addr + 4] = (value & MASK).to_bytes(4, "little")
        else:
            self.mem[addr] = value & 0xFF
        self._dec.pop(addr & ~3, None)  # code may be written as data (Part 6): forget its decoding

    def word(self, addr: int) -> int:
        return int.from_bytes(self.mem[addr:addr + 4], "little")

    # -- execution --------------------------------------------------------------
    def _decoded(self, pc: int):
        d = self._dec.get(pc)
        if d is None:
            if pc & 3 or pc + 4 > self.mem_size:
                raise MachineError(f"bad pc {pc:#x}")
            w = self.word(pc)
            op = (w >> 26) & 0x3F
            if op not in OPS:
                raise MachineError(f"illegal instruction {w:#010x} at pc {pc:#x}")
            i = decode(w)
            d = (i.op, i.rd, i.rs1, i.rs2, i.imm, w)
            self._dec[pc] = d
        return d

    def step(self) -> None:
        if self.halted:
            return
        pc = self.pc
        op, rd, rs1, rs2, imm, w = self._decoded(pc)
        R = self.regs
        a, b = R[rs1], R[rs2]
        nxt = pc + 4
        wr = None  # register write
        rec = Step(pc, w) if self.trace else None
        if op == "add":
            wr = a + b
        elif op == "addi":
            wr = a + imm
        elif op == "sub":
            wr = a - b
        elif op == "and":
            wr = a & b
        elif op == "andi":
            wr = a & (imm & MASK)
        elif op == "or":
            wr = a | b
        elif op == "ori":
            wr = a | (imm & MASK)
        elif op == "xor":
            wr = a ^ b
        elif op == "xori":
            wr = a ^ (imm & MASK)
        elif op in ("sll", "slli"):
            wr = a << ((b if op == "sll" else imm) & 31)
        elif op in ("srl", "srli"):
            wr = a >> ((b if op == "srl" else imm) & 31)
        elif op in ("sra", "srai"):
            wr = sext(a, 32) >> ((b if op == "sra" else imm) & 31)
        elif op == "slt":
            wr = int(sext(a, 32) < sext(b, 32))
        elif op == "slti":
            wr = int(sext(a, 32) < imm)
        elif op == "sltu":
            wr = int(a < b)
        elif op == "sltiu":
            wr = int(a < (imm & MASK))
        elif op == "lw":
            wr = self.load(a + imm, 4)
        elif op == "lb":
            wr = self.load(a + imm, 1, signed_=True)
        elif op == "lbu":
            wr = self.load(a + imm, 1)
        elif op in ("sw", "sb"):
            size = 4 if op == "sw" else 1
            self.store(a + imm, size, b)
            if rec:
                rec.mem = ((a + imm) & MASK, size, b & (MASK if size == 4 else 0xFF))
        elif op in ("beq", "bne", "blt", "bge", "bltu", "bgeu"):
            if op == "beq":
                t = a == b
            elif op == "bne":
                t = a != b
            elif op == "blt":
                t = sext(a, 32) < sext(b, 32)
            elif op == "bge":
                t = sext(a, 32) >= sext(b, 32)
            elif op == "bltu":
                t = a < b
            else:
                t = a >= b
            if t:
                nxt = pc + 4 * imm
            if rec:
                rec.taken = t
        elif op == "jal":
            wr = pc + 4
            nxt = pc + 4 * imm
        elif op == "jalr":
            wr = pc + 4
            nxt = (a + imm) & MASK & ~3
        elif op == "lui":
            wr = imm << 10
        elif op == "halt":
            self.halted = True
            nxt = pc
        else:  # pragma: no cover - decode rejects unknown opcodes
            raise MachineError(f"unimplemented {op}")
        if wr is not None and rd:
            R[rd] = wr & MASK
            if rec:
                rec.reg = (rd, R[rd])
        self.pc = nxt & MASK
        self.steps += 1
        self.counts[op] = self.counts.get(op, 0) + 1
        if rec:
            self.log.append(rec)

    def run(self, max_steps: int = 50_000_000) -> "Machine":
        step = self.step
        for _ in range(max_steps):
            if self.halted:
                return self
            step()
        if not self.halted:
            raise MachineError(f"no halt after {max_steps} steps (pc {self.pc:#x})")
        return self


def run(program, tape: bytes = b"", **kw) -> Machine:
    """Assemble-and-run convenience: ``program`` is an assembled :class:`~explainer.cs.pebble.asm.Program` or raw
    image bytes."""
    image = getattr(program, "image", program)
    max_steps = kw.pop("max_steps", 50_000_000)
    return Machine(image=image, tape=tape, **kw).run(max_steps)
