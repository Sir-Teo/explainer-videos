"""Part 7: the pipeline agrees with the emulator; its cycle count is instructions + 4 + the bubbles it reports;
predictors behave as designed; the M extension."""

from __future__ import annotations

import ctypes
import unittest

from explainer.cs.pebble import assemble, run
from explainer.cs.pebble import predict as PR
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.pipe import Pipeline
from explainer.cs.pebble.randprog import random_program


def i32(v):
    return ctypes.c_int32(v).value


class MExtension(unittest.TestCase):
    def test_against_python(self):
        for a, b in [(-7, 2), (7, -2), (-7, -2), (123456789, 9876), (-(1 << 31), -1), (5, 7), (0, 3)]:
            src = f"li a0, {a}\nli a1, {b}\nmul a2, a0, a1\nmulh a3, a0, a1\ndiv a4, a0, a1\nrem a5, a0, a1\nhalt"
            m = run(assemble(src))
            q = int(a / b) if not (a == -(1 << 31) and b == -1) else a
            self.assertEqual(i32(m.regs[5]), i32(a * b & 0xFFFFFFFF))
            self.assertEqual(i32(m.regs[6]), (a * b) >> 32)
            self.assertEqual(i32(m.regs[7]), i32(q & 0xFFFFFFFF))
            self.assertEqual(i32(m.regs[8]), i32((a - q * b) & 0xFFFFFFFF))


class PipelineAgrees(unittest.TestCase):
    def check(self, image, tape=b"", mem_size=8192, **kw):
        e = run(image, tape=tape, mem_size=mem_size)
        q = Pipeline(image, tape=tape, mem_size=mem_size, **kw).run(5_000_000)
        self.assertEqual(q.regs, e.regs)
        self.assertEqual(bytes(q.mem), bytes(e.mem))
        self.assertEqual(bytes(q.output), bytes(e.output))
        self.assertEqual(q.retired, e.steps)
        self.assertEqual(q.cycles, q.retired + 4 + q.bubbles)
        return q

    def test_random_programs(self):
        configs = [dict(), dict(forwarding=False), dict(predictor=PR.TwoBit()), dict(predictor=PR.GShare()),
                   dict(predictor=PR.Perceptron(), btb_entries=0, ras_depth=0)]
        for k, cfg in enumerate(configs):
            for seed in range(30):
                with self.subTest(cfg=k, seed=seed):
                    self.check(assemble(random_program(seed, mext=True)).image, **cfg)

    def test_job_on_a_paragraph(self):
        tape = b"It is a truth universally acknowledged, that a single man in possession of a good fortune."
        q = self.check(assemble(P.JOB_V0).image, tape=tape, mem_size=1 << 20, predictor=PR.Tournament())
        self.assertEqual(bytes(q.output), P.job_reference(tape))

    def test_forwarding_removes_all_but_load_use(self):
        src = "li a0, 1\nadd a1, a0, a0\nadd a2, a1, a1\nadd a3, a2, a2\nhalt"
        q = Pipeline(assemble(src).image, mem_size=4096).run()
        self.assertEqual(q.stats["load_use"] + q.stats["raw"], 0)
        q = Pipeline(assemble(src).image, mem_size=4096, forwarding=False).run()
        self.assertGreater(q.stats["raw"], 0)
        src = "li s0, 0x400\nlw a0, 0(s0)\nadd a1, a0, a0\nhalt"
        q = Pipeline(assemble(src).image, mem_size=4096).run()
        self.assertEqual(q.stats["load_use"], 1)

    def test_precise_division_by_zero(self):
        src = "li s0, 0x400\nli a0, 11\nsw a0, 0(s0)\nli a1, 0\ndiv a2, a0, a1\nsw a0, 4(s0)\nhalt"
        q = Pipeline(assemble(src).image, mem_size=4096).run()
        self.assertIn("division by zero", q.error)
        self.assertEqual(int.from_bytes(q.mem[0x400:0x404], "little"), 11)
        self.assertEqual(int.from_bytes(q.mem[0x404:0x408], "little"), 0)

    def test_self_modifying_code_goes_stale(self):
        self.assertEqual(run(assemble(P.SELFMOD)).regs[4], 31)
        # predicted, the loop refetches the load before the store that rewrites it lands; unpredicted, every trip
        # mispredicts and the flush refetches the new word, so it works by accident
        self.assertNotEqual(Pipeline(assemble(P.SELFMOD).image, predictor=PR.TwoBit()).run().regs[4], 31)
        self.assertEqual(Pipeline(assemble(P.SELFMOD).image).run().regs[4], 31)


class Predictors(unittest.TestCase):
    def test_loop_and_alternation(self):
        loop = [(0x40, k % 10 != 9) for k in range(2000)]  # taken nine times, then not
        alt = [(0x80, k % 2 == 0) for k in range(2000)]  # taken, not, taken, ...
        self.assertGreater(PR.accuracy(PR.TwoBit(), loop), PR.accuracy(PR.OneBit(), loop))
        self.assertLess(PR.accuracy(PR.TwoBit(), alt), 0.6)
        for p in (PR.GShare(), PR.Tage(), PR.Perceptron()):
            self.assertGreater(PR.accuracy(p, alt), 0.98, p.name)

    def test_perceptron_finds_the_correlated_branch(self):
        import numpy as np

        rng = np.random.default_rng(0)
        trace = []
        for _ in range(4000):
            x = bool(rng.integers(2))
            trace.append((0x100, x))
            for j in range(4):
                trace.append((0x200 + 4 * j, bool(rng.integers(2))))  # noise
            trace.append((0x300, x))  # repeats the outcome five branches back
        p = PR.Perceptron()
        PR.accuracy(p, trace)
        w = p.weights(0x300)
        self.assertEqual(int(np.argmax(np.abs(w[1:]))) + 1, 5)


if __name__ == "__main__":
    unittest.main()
