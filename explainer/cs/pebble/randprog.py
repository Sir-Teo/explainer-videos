"""Random Pebble-32 programs that always halt: the co-simulation workload (every layer of Pebble must agree with the
emulator on them; ``tests/test_cs6_cpu.py``).

Registers start from random constants; ALU, shift, compare, load, store, branch and jump instructions follow in
random order.  Branches and jumps only go forward, so every program terminates; memory instructions use ``s0`` as a
base pointer into a data area that no other instruction may overwrite.
"""

from __future__ import annotations

import numpy as np

R_OPS = ("add", "sub", "and", "or", "xor", "sll", "srl", "sra", "slt", "sltu")
M_OPS = ("mul", "mulh", "div", "rem")
I_OPS = ("addi", "andi", "ori", "xori", "slti", "sltiu", "slli", "srli", "srai")
BRANCH = ("beq", "bne", "blt", "bge", "bltu", "bgeu")
FREE = [r for r in range(1, 16) if r not in (2, 13)]  # all but sp and the base pointer s0
NAMES = ["zero", "ra", "sp", "a0", "a1", "a2", "a3", "a4", "a5", "t0", "t1", "t2", "t3", "s0", "s1", "s2"]


def random_program(seed: int, length: int = 60, data: int = 0x800, mext: bool = False) -> str:
    """``mext``: also multiplies and divides (divisors forced odd, so never zero)."""
    rng = np.random.default_rng(seed)
    R = NAMES

    def reg(dest=False):
        if dest:
            return R[int(rng.choice(FREE + [0]))]  # writes to zero must be ignored
        return R[int(rng.integers(0, 16))]

    lines = [f"        li s0, {data}"]
    for r in FREE:
        lines.append(f"        li {R[r]}, {int(rng.integers(-2**31, 2**31))}")
    pending = []  # labels to place: (line index at which to place, name)
    k = 0
    for i in range(length):
        while pending and pending[0][0] <= i:
            lines.append(f"{pending.pop(0)[1]}:")
        kind = rng.choice(["r", "i", "lui", "mem", "branch", "jal", "jalr"], p=[.3, .25, .05, .2, .12, .04, .04])
        if kind == "r" and mext and rng.random() < 0.3:
            op = rng.choice(M_OPS)
            if op in ("div", "rem"):
                lines.append("        ori  t3, t3, 1")
                lines.append(f"        {op} {reg(True)}, {reg()}, t3")
            else:
                lines.append(f"        {op} {reg(True)}, {reg()}, {reg()}")
        elif kind == "r":
            lines.append(f"        {rng.choice(R_OPS)} {reg(True)}, {reg()}, {reg()}")
        elif kind == "i":
            op = rng.choice(I_OPS)
            imm = int(rng.integers(0, 32)) if op in ("slli", "srli", "srai") else int(rng.integers(-2**17, 2**17))
            lines.append(f"        {op} {reg(True)}, {reg()}, {imm}")
        elif kind == "lui":
            lines.append(f"        lui {reg(True)}, {int(rng.integers(-2**21, 2**21))}")
        elif kind == "mem":
            op = rng.choice(["lw", "sw", "lb", "lbu", "sb"])
            off = int(rng.integers(-64, 64)) * 4 if op in ("lw", "sw") else int(rng.integers(-256, 256))
            if op in ("lw", "lb", "lbu"):
                lines.append(f"        {op} {reg(True)}, {off}(s0)")
            else:
                lines.append(f"        {op} {reg()}, {off}(s0)")
        elif kind == "branch":
            name = f"L{k}"
            k += 1
            pending.append((i + int(rng.integers(1, 5)), name))
            pending.sort()
            lines.append(f"        {rng.choice(BRANCH)} {reg()}, {reg()}, {name}")
        elif kind == "jal":
            name = f"L{k}"
            k += 1
            pending.append((i + int(rng.integers(1, 4)), name))
            pending.sort()
            lines.append(f"        jal {reg(True)}, {name}")
        else:  # jalr through a register loaded with a label's address
            name = f"L{k}"
            k += 1
            pending.append((i + 2, name))
            pending.sort()
            lines.append(f"        la t2, {name}")
            lines.append(f"        jalr {reg(True)}, 0(t2)")
    for _, name in pending:
        lines.append(f"{name}:")
    lines.append("        halt")
    return "\n".join(lines) + "\n"
