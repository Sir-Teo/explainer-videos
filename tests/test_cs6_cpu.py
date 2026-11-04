"""Part 6: the gate-level Pebble CPU agrees with the emulator; the compiled evaluator agrees with the slow one; the
Job's cycle formula is exact."""

from __future__ import annotations

import unittest

import numpy as np

from explainer.cs.pebble import assemble, run
from explainer.cs.pebble import blocks as B
from explainer.cs.pebble import cpu as C
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.fast import Fast
from explainer.cs.pebble.hdl import Circuit, simulate
from explainer.cs.pebble.randprog import random_program

_CPU = {}


def machine(style="table"):
    if style not in _CPU:
        s = C.build_cpu(style)
        _CPU[style] = (s, Fast(s))
    return _CPU[style]


class FastEvaluator(unittest.TestCase):
    def test_matches_python_evaluation(self):
        alu = B.alu(16)
        f = Fast(alu)
        rng = np.random.default_rng(0)
        n = 300
        a, b = rng.integers(0, 1 << 16, n), rng.integers(0, 1 << 16, n)
        op = rng.integers(0, 10, n)
        f.reset(n)
        got = f.eval({"a": a, "b": b, "op": op})["y"].astype(np.int64)
        want = simulate(alu, {"a": a, "b": b, "op": op})["y"].astype(np.int64)
        self.assertTrue(np.array_equal(got, want))
        self.assertTrue(np.array_equal(got, B.alu_spec(a, b, op, 16)))

    def test_embed_copies_a_block(self):
        c = Circuit("two adders")
        x, y, z = c.input("x", 8), c.input("y", 8), c.input("z", 8)
        add = B.prefix_adder(8)
        s1 = c.embed(add, a=x, b=y, cin=c.const(0))["s"]
        s2 = c.embed(add, a=s1, b=z, cin=c.const(0))["s"]
        c.output("s", s2)
        v = {"x": np.arange(50), "y": np.arange(50) * 3, "z": np.full(50, 7)}
        self.assertTrue(np.array_equal(simulate(c, v)["s"].astype(np.int64), (np.arange(50) * 4 + 7) % 256))


class GateLevelCpu(unittest.TestCase):
    def check(self, src, style="table", tape=b"", mem_size=8192):
        s, f = machine(style)
        p = assemble(src)
        e = run(p, tape=tape, mem_size=mem_size)
        g = C.GateMachine(s, p.image, tape=tape, mem_size=mem_size, fast=f).run(200_000)
        self.assertEqual(g.regs, e.regs)
        self.assertEqual(g.steps, e.steps)
        self.assertEqual(bytes(g.mem), bytes(e.mem))
        self.assertEqual(bytes(g.output), bytes(e.output))
        return g

    def test_random_programs_both_control_units(self):
        for style in ("table", "minimized"):
            for seed in range(25):
                with self.subTest(style=style, seed=seed):
                    self.check(random_program(seed), style)

    def test_euclid_and_hello(self):
        from videos.cs.cs1.compute import EUCLID_ASM

        self.assertEqual(self.check(EUCLID_ASM).regs[3], 21)
        self.assertEqual(bytes(self.check(P.HELLO).output), b"Hello from Pebble!\n")

    def test_self_modifying_code_runs_as_written(self):
        self.assertEqual(self.check(P.SELFMOD).regs[4], 31)

    def test_job_on_a_sentence(self):
        tape = b"The cat saw the dog. The dog saw the cat; the end."
        g = self.check(P.JOB_V0, tape=tape, mem_size=1 << 20)
        self.assertEqual(bytes(g.output), P.job_reference(tape))

    def test_illegal_opcode_stops(self):
        s, f = machine()
        image = (0).to_bytes(4, "little")  # opcode 0 is illegal
        g = C.GateMachine(s, image, mem_size=64, fast=f).run(10)
        self.assertIsNotNone(g.error)


class Programs(unittest.TestCase):
    def test_job_cycle_formula_is_exact(self):
        prog = assemble(P.JOB_V0)
        rng = np.random.default_rng(2)
        words = [b"the", b"a", b"cat", b"Dog", b"tea", b"ate", b"x", b"apple", b"apply", b"I"]
        for k in range(12):
            n = int(rng.integers(0, 60))
            parts = [words[int(i)] for i in rng.integers(0, len(words), n)]
            seps = [b" ", b", ", b".\n", b"--", b"\xe2\x80\x99"]
            tape = b"".join(w + seps[int(rng.integers(0, len(seps)))] for w in parts)
            if k % 3 == 0:
                tape = tape.rstrip(b" ,.\n-\xe2\x80\x99")
            m = run(prog, tape=tape)
            self.assertEqual(bytes(m.output), P.job_reference(tape))
            self.assertEqual(m.steps, P.job_cycles(P.job_features(tape)), tape)

    def test_turing_machine_interpreter(self):
        from explainer.cs.turing import CHAMPIONS, TM

        for n in (2, 3, 4):
            t, S, ones, _, _ = CHAMPIONS[n]
            m = run(assemble(P.tm_program(TM.parse(t))))
            self.assertEqual((m.regs[3], m.regs[4]), (S, ones))


if __name__ == "__main__":
    unittest.main()
