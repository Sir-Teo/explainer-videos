"""Pebble's core (explainer/cs/pebble): the ISA's encodings, the emulator's semantics, the assembler, and the gate
simulator, each checked against something that does not share its code (Python integer arithmetic, hand-computed
results, exhaustive truth tables)."""

import random
import unittest

import numpy as np

from explainer.cs.pebble import AsmError, Instr, MachineError, assemble, decode, disasm, encode, run
from explainer.cs.pebble.hdl import Circuit, exhaustive, unpack
from explainer.cs.pebble.isa import FORMAT, IMM_BITS, MASK, OPS, sext

M32 = 1 << 32


def s32(v):
    v &= MASK
    return v - M32 if v >> 31 else v


class EncodingTests(unittest.TestCase):
    def test_every_instruction_round_trips(self):
        rng = random.Random(1)
        for _, (op, f) in OPS.items():
            for _ in range(200):
                bits = IMM_BITS[f]
                imm = rng.randint(-(1 << (bits - 1)), (1 << (bits - 1)) - 1) if bits else 0
                if op == "halt":
                    ins = Instr("halt")
                elif f == "R":
                    ins = Instr(op, rd=rng.randrange(16), rs1=rng.randrange(16), rs2=rng.randrange(16))
                elif f == "I":
                    ins = Instr(op, rd=rng.randrange(16), rs1=rng.randrange(16), imm=imm)
                elif f == "S":
                    ins = Instr(op, rs1=rng.randrange(16), rs2=rng.randrange(16), imm=imm)
                else:
                    ins = Instr(op, rd=rng.randrange(16), imm=imm)
                w = encode(ins)
                self.assertEqual(w >> 26, [k for k, v in OPS.items() if v[0] == op][0])
                self.assertEqual(decode(w), ins)
                self.assertTrue(disasm(w))

    def test_immediate_out_of_range_is_rejected(self):
        with self.assertRaises(ValueError):
            encode(Instr("addi", rd=1, rs1=1, imm=1 << 17))
        with self.assertRaises(ValueError):
            decode(0)  # opcode 0 is illegal: a jump into zeroed memory stops the machine


class AluTests(unittest.TestCase):
    """Every ALU instruction against Python's integers, on random and edge-case operands."""

    REF = {
        "add": lambda a, b: a + b, "sub": lambda a, b: a - b, "and": lambda a, b: a & b, "or": lambda a, b: a | b,
        "xor": lambda a, b: a ^ b, "sll": lambda a, b: a << (b & 31), "srl": lambda a, b: (a & MASK) >> (b & 31),
        "sra": lambda a, b: s32(a) >> (b & 31), "slt": lambda a, b: int(s32(a) < s32(b)),
        "sltu": lambda a, b: int((a & MASK) < (b & MASK)),
    }

    def test_register_register(self):
        rng = random.Random(2)
        edge = [0, 1, 2, 31, 32, 0x7FFF_FFFF, 0x8000_0000, MASK, MASK - 1, 12345]
        for op, ref in self.REF.items():
            pairs = [(a, b) for a in edge for b in edge] + [(rng.getrandbits(32), rng.getrandbits(32))
                                                           for _ in range(300)]
            for a, b in pairs:
                src = f"li a0, {a}\nli a1, {b}\n{op} a2, a0, a1\nhalt\n"
                m = run(assemble(src), mem_size=4096)
                self.assertEqual(m.regs[5], ref(a, b) & MASK, (op, a, b))

    def test_immediates_sign_extend(self):
        for op, ref in (("addi", lambda a, i: a + i), ("slti", lambda a, i: int(s32(a) < i)),
                        ("sltiu", lambda a, i: int((a & MASK) < (i & MASK))), ("xori", lambda a, i: a ^ (i & MASK)),
                        ("andi", lambda a, i: a & (i & MASK)), ("ori", lambda a, i: a | (i & MASK))):
            for a in (0, 5, MASK, 0x8000_0000):
                for i in (-131072, -1, 0, 7, 131071):
                    m = run(assemble(f"li a0, {a}\n{op} a1, a0, {i}\nhalt"), mem_size=4096)
                    self.assertEqual(m.regs[4], ref(a, i) & MASK, (op, a, i))

    def test_r0_stays_zero(self):
        m = run(assemble("addi zero, zero, 5\nli zero, 77\nadd a0, zero, zero\nhalt"), mem_size=4096)
        self.assertEqual(m.regs[0], 0)
        self.assertEqual(m.regs[3], 0)


class ProgramTests(unittest.TestCase):
    def test_sum_and_listing(self):
        p = assemble("""
                li   a0, 10          # n
                li   a1, 0           # sum
        loop:   add  a1, a1, a0
                addi a0, a0, -1
                bnez a0, loop
                halt
        """)
        m = run(p)
        self.assertEqual(m.regs[4], 55)
        self.assertEqual(m.steps, 4 + 3 * 10 + 1)
        self.assertEqual(p.labels["loop"], 16)

    def test_euclid(self):
        src = """
                li   a0, {a}
                li   a1, {b}
        loop:   beqz a1, done
                # a0, a1 = a1, a0 mod a1   (mod by repeated subtraction: no divider until Part 4)
        mod:    bltu a0, a1, swap
                sub  a0, a0, a1
                j    mod
        swap:   mv   t0, a0
                mv   a0, a1
                mv   a1, t0
                j    loop
        done:   halt
        """
        import math

        rng = random.Random(3)
        for _ in range(60):
            a, b = rng.randint(1, 5000), rng.randint(1, 5000)
            self.assertEqual(run(assemble(src.format(a=a, b=b))).regs[3], math.gcd(a, b))

    def test_memory_bytes_words_and_data(self):
        p = assemble("""
                la   t0, data
                lw   a0, 0(t0)
                lb   a1, 4(t0)
                lbu  a2, 4(t0)
                li   a3, 0x1234ABCD
                sw   a3, 8(t0)
                lw   a4, 8(t0)
                sb   a3, 12(t0)
                lbu  a5, 12(t0)
                halt
                .align 4
        data:   .word -2
                .byte 0xF0, 1, 2, 3
                .space 8
        """)
        m = run(p)
        self.assertEqual(m.regs[3], (-2) & MASK)
        self.assertEqual(m.regs[4], (-16) & MASK)
        self.assertEqual(m.regs[5], 0xF0)
        self.assertEqual(m.regs[7], 0x1234ABCD)
        self.assertEqual(m.regs[8], 0xCD)

    def test_io_echo_uppercase(self):
        p = assemble("""
                .equ TAPE, 0xFFFF0004
                .equ CONSOLE, 0xFFFF0000
                li   s0, TAPE
                li   s1, CONSOLE
                li   t1, 'a'
                li   t2, 'z'
        next:   lw   a0, 0(s0)
                bltz a0, done
                blt  a0, t1, out
                bgt  a0, t2, out
                addi a0, a0, -32
        out:    sb   a0, 0(s1)
                j    next
        done:   halt
        """)
        m = run(p, tape=b"Call me Ishmael.")
        self.assertEqual(bytes(m.output), b"CALL ME ISHMAEL.")

    def test_recursion_on_the_stack(self):
        p = assemble("""
                li   a0, 10
                call fact
                halt
        fact:   addi sp, sp, -8         # a frame: the return address and n
                sw   ra, 4(sp)
                sw   a0, 0(sp)
                li   t0, 1
                bgt  a0, t0, rec
                li   a0, 1
                j    out
        rec:    addi a0, a0, -1
                call fact
                lw   t0, 0(sp)
                # a0 = a0 * t0 by repeated addition (Pebble has no multiplier yet)
                mv   t1, a0
                li   a0, 0
        mul:    beqz t0, out
                add  a0, a0, t1
                addi t0, t0, -1
                j    mul
        out:    lw   ra, 4(sp)
                addi sp, sp, 8
                ret
        """)
        self.assertEqual(run(p).regs[3], 3628800)

    def test_trace_records_writes_and_branches(self):
        p = assemble("li a0, 2\nloop: addi a0, a0, -1\nbnez a0, loop\nsw a0, 64(zero)\nhalt")
        m = run(p, trace=True)
        taken = [s.taken for s in m.log if s.taken is not None]
        self.assertEqual(taken, [True, False])
        self.assertEqual(m.log[-2].mem, (64, 4, 0))

    def test_errors(self):
        with self.assertRaises(AsmError):
            assemble("frob a0, a1")
        with self.assertRaises(AsmError):
            assemble("x: nop\nx: nop")
        with self.assertRaises(MachineError):
            run(assemble("j 0x400"), mem_size=4096)  # into zeroed memory: opcode 0 is illegal
        with self.assertRaises(MachineError):
            run(assemble("loop: j loop"), max_steps=1000)


class GateTests(unittest.TestCase):
    def full_adder(self):
        c = Circuit("full adder")
        a, b, cin = c.input("a"), c.input("b"), c.input("cin")
        s1 = c.xor(a, b)
        c.output("sum", c.xor(s1, cin))
        c.output("cout", c.or_(c.and_(a, b), c.and_(s1, cin)))
        return c

    def test_full_adder_truth_table(self):
        for circ in (self.full_adder(), self.full_adder().to_nand()):
            out = circ.evaluate(exhaustive(circ))
            s, co = unpack(out["sum"][0], 8), unpack(out["cout"][0], 8)
            for p in range(8):
                a, b, cin = p & 1, p >> 1 & 1, p >> 2 & 1
                self.assertEqual(s[p] + 2 * co[p], a + b + cin)
        self.assertEqual(set(self.full_adder().to_nand().counts()), {"NAND"})

    def test_ripple_adder_exhaustive_8_bits(self):
        c = Circuit("ripple")
        a, b = c.input("a", 8), c.input("b", 8)
        carry = c.const(0)
        out = []
        for i in range(8):
            t = c.xor(a[i], b[i])
            out.append(c.xor(t, carry))
            carry = c.or_(c.and_(a[i], b[i]), c.and_(t, carry))
        c.output("s", out + [carry])
        vals = c.evaluate(exhaustive(c))
        bits = [unpack(v, 1 << 16) for v in vals["s"]]
        got = sum(b << i for i, b in enumerate(bits))
        p = np.arange(1 << 16)
        self.assertTrue(np.array_equal(got, (p & 255) + (p >> 8)))
        self.assertEqual(c.depth(), 17)  # the carry ripples: two gate levels per bit, plus the first xor
        self.assertEqual(c.evaluate_ints({"a": 200, "b": 100})["s"], 300)


if __name__ == "__main__":
    unittest.main()
