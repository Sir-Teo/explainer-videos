"""Pebble-32, the instruction set of the computer *Computer Science, Built* builds (videos/cs/SYLLABUS.md, 2.1).

A clean 32-bit RISC in the RISC-V mould, small enough to draw: sixteen 32-bit registers (``r0`` is always 0),
byte-addressed little-endian memory, every instruction one 32-bit word whose top six bits are its opcode, and four
formats:

    R   | op:6 | rd:4  | rs1:4 | rs2:4 | 0:14          |   add rd, rs1, rs2
    I   | op:6 | rd:4  | rs1:4 | imm:18 (signed)       |   addi rd, rs1, imm    lw rd, imm(rs1)    jalr rd, imm(rs1)
    S   | op:6 | rs1:4 | rs2:4 | imm:18 (signed)       |   sw rs2, imm(rs1)     beq rs1, rs2, label
    J   | op:6 | rd:4  | imm:22 (signed)               |   jal rd, label        lui rd, imm

Branch and jump offsets count instructions (target = pc + 4 * imm), so ``jal`` reaches 8 MiB either way and a
branch 512 KiB.  ``lui`` puts its 22 bits in the top of the register (``rd = imm << 10``); with ``ori`` (which takes
the low 10 bits) any 32-bit constant takes two instructions, the assembler's ``li``.

Where Pebble-32 differs from RV32I, and why (the comparison card in Part 6): sixteen registers, not thirty-two (4-bit
fields leave room for 18-bit immediates); one opcode per instruction, no ``funct`` fields (the decoder is a table a
viewer can read); immediates in one contiguous field, not scattered (RISC-V scatters them to keep the sign bit in
one place for the hardware; we draw ours); offsets in instructions, not half-words (no compressed instructions);
a ``halt`` instruction until Part 31 gives the machine an operating system to return to.

Later parts add the extensions the syllabus lists, with their opcodes reserved here: ``mul mulh div rem``
(Part 4's multiplier and divider, wired into the CPU in Part 7), ``ecall eret csrr csrw`` (Part 31), ``cas amoadd``
(Parts 10 and 33).  Opcode 0 is illegal, so a jump into zeroed memory stops the machine.
"""

from __future__ import annotations

from dataclasses import dataclass

NREGS = 16
WORD = 32
MASK = 0xFFFF_FFFF

# register names: number -> ABI name (the calling convention is Part 11's)
REG_NAMES = ["zero", "ra", "sp", "a0", "a1", "a2", "a3", "a4", "a5", "t0", "t1", "t2", "t3", "s0", "s1", "s2"]
REG_NUM = {n: i for i, n in enumerate(REG_NAMES)} | {f"r{i}": i for i in range(NREGS)} | {"fp": 13}

# opcode -> (mnemonic, format)
OPS = {
    1: ("add", "R"), 2: ("sub", "R"), 3: ("and", "R"), 4: ("or", "R"), 5: ("xor", "R"), 6: ("sll", "R"),
    7: ("srl", "R"), 8: ("sra", "R"), 9: ("slt", "R"), 10: ("sltu", "R"),
    11: ("addi", "I"), 12: ("andi", "I"), 13: ("ori", "I"), 14: ("xori", "I"), 15: ("slti", "I"),
    16: ("sltiu", "I"), 17: ("slli", "I"), 18: ("srli", "I"), 19: ("srai", "I"),
    20: ("lw", "I"), 21: ("lb", "I"), 22: ("lbu", "I"),
    23: ("sw", "S"), 24: ("sb", "S"),
    25: ("beq", "S"), 26: ("bne", "S"), 27: ("blt", "S"), 28: ("bge", "S"), 29: ("bltu", "S"), 30: ("bgeu", "S"),
    31: ("jal", "J"), 32: ("jalr", "I"), 33: ("lui", "J"),
    63: ("halt", "J"),
}
RESERVED = {34: "mul", 35: "mulh", 36: "div", 37: "rem", 48: "ecall", 49: "eret", 50: "csrr", 51: "csrw",
            52: "cas", 53: "amoadd"}
OPCODE = {m: op for op, (m, _) in OPS.items()}
FORMAT = {m: f for _, (m, f) in OPS.items()}
BASE = tuple(m for _, (m, _) in sorted(OPS.items()))

IMM_BITS = {"R": 0, "I": 18, "S": 18, "J": 22}

# memory-mapped devices (the top page of the address space)
IO_BASE = 0xFFFF_0000
IO_CONSOLE = 0xFFFF_0000  # store a byte: it is printed
IO_TAPE = 0xFFFF_0004  # load: the next byte of the input, or -1 (0xFFFFFFFF) at its end
IO_CYCLES = 0xFFFF_0008  # load: instructions executed so far (low 32 bits)


def sext(v: int, bits: int) -> int:
    """Sign-extend the low ``bits`` of v."""
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


def signed(v: int) -> int:
    return sext(v, 32)


@dataclass(frozen=True)
class Instr:
    op: str
    rd: int = 0
    rs1: int = 0
    rs2: int = 0
    imm: int = 0

    @property
    def fmt(self) -> str:
        return FORMAT[self.op]


def encode(ins: Instr) -> int:
    op = OPCODE[ins.op]
    f = ins.fmt
    bits = IMM_BITS[f]
    if bits:
        lo, hi = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
        if not lo <= ins.imm <= hi:
            raise ValueError(f"{ins.op}: immediate {ins.imm} does not fit in {bits} signed bits")
    for r in (ins.rd, ins.rs1, ins.rs2):
        if not 0 <= r < NREGS:
            raise ValueError(f"{ins.op}: no register r{r}")
    if f == "R":
        return op << 26 | ins.rd << 22 | ins.rs1 << 18 | ins.rs2 << 14
    if f == "I":
        return op << 26 | ins.rd << 22 | ins.rs1 << 18 | (ins.imm & 0x3FFFF)
    if f == "S":
        return op << 26 | ins.rs1 << 22 | ins.rs2 << 18 | (ins.imm & 0x3FFFF)
    return op << 26 | ins.rd << 22 | (ins.imm & 0x3FFFFF)


def decode(word: int) -> Instr:
    op = (word >> 26) & 0x3F
    if op not in OPS:
        raise ValueError(f"illegal instruction {word:#010x} (opcode {op})")
    m, f = OPS[op]
    a, b, c = (word >> 22) & 0xF, (word >> 18) & 0xF, (word >> 14) & 0xF
    if f == "R":
        return Instr(m, rd=a, rs1=b, rs2=c)
    if f == "I":
        return Instr(m, rd=a, rs1=b, imm=sext(word, 18))
    if f == "S":
        return Instr(m, rs1=a, rs2=b, imm=sext(word, 18))
    return Instr(m, rd=a, imm=sext(word, 22))


def fields(word: int) -> list[tuple[str, int, int, int]]:
    """The bit fields of an encoded instruction, for drawing: (name, high bit, low bit, value)."""
    op = (word >> 26) & 0x3F
    f = OPS[op][1] if op in OPS else "R"
    out = [("op", 31, 26, op)]
    if f == "R":
        out += [("rd", 25, 22, (word >> 22) & 0xF), ("rs1", 21, 18, (word >> 18) & 0xF),
                ("rs2", 17, 14, (word >> 14) & 0xF), ("0", 13, 0, word & 0x3FFF)]
    elif f == "I":
        out += [("rd", 25, 22, (word >> 22) & 0xF), ("rs1", 21, 18, (word >> 18) & 0xF),
                ("imm", 17, 0, sext(word, 18))]
    elif f == "S":
        out += [("rs1", 25, 22, (word >> 22) & 0xF), ("rs2", 21, 18, (word >> 18) & 0xF),
                ("imm", 17, 0, sext(word, 18))]
    else:
        out += [("rd", 25, 22, (word >> 22) & 0xF), ("imm", 21, 0, sext(word, 22))]
    return out


def disasm(word: int, pc: int | None = None, labels: dict[int, str] | None = None) -> str:
    """One instruction as assembly text (branch targets as labels when ``labels`` maps addresses to names)."""
    i = decode(word)
    R = REG_NAMES

    def target(imm):
        if pc is None:
            return str(imm)
        t = pc + 4 * imm
        return (labels or {}).get(t, f"{t:#x}")

    if i.op == "halt":
        return "halt"
    if i.fmt == "R":
        return f"{i.op} {R[i.rd]}, {R[i.rs1]}, {R[i.rs2]}"
    if i.op in ("lw", "lb", "lbu", "jalr"):
        return f"{i.op} {R[i.rd]}, {i.imm}({R[i.rs1]})"
    if i.fmt == "I":
        return f"{i.op} {R[i.rd]}, {R[i.rs1]}, {i.imm}"
    if i.op in ("sw", "sb"):
        return f"{i.op} {R[i.rs2]}, {i.imm}({R[i.rs1]})"
    if i.fmt == "S":
        return f"{i.op} {R[i.rs1]}, {R[i.rs2]}, {target(i.imm)}"
    if i.op == "jal":
        return f"jal {R[i.rd]}, {target(i.imm)}"
    return f"lui {R[i.rd]}, {i.imm}"
