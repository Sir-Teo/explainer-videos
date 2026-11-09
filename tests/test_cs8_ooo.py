"""Part 8: the out-of-order core agrees with the emulator in every configuration; memory-order violations are caught
and repaired; exceptions stay precise; Spectre leaks a secret through a bounds check and both mitigations stop it;
the limit study orders its idealizations as it should."""

from __future__ import annotations

import unittest

from explainer.cs.pebble import assemble, run
from explainer.cs.pebble import predict as PR
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.limits import schedule, trace
from explainer.cs.pebble.ooo import Cache, OutOfOrder
from explainer.cs.pebble.randprog import random_program

CONFIGS = [
    {"disambiguation": "conservative"},
    {"disambiguation": "speculative"},
    {"disambiguation": "wait-table", "width": 2, "rob_size": 16, "iq_size": 8, "lsq_size": 6},
    {"width": 8, "rob_size": 256, "iq_size": 128},
    {"perfect_prediction": True},
    {"cache": "yes"},
]


def same(core, ref) -> bool:
    return (core.regs == ref.regs and bytes(core.mem) == bytes(ref.mem) and core.output == ref.output
            and core.committed == ref.steps)


class Agrees(unittest.TestCase):
    def test_random_programs(self):
        for seed in range(120):
            p = assemble(random_program(seed, mext=seed % 2 == 0))
            ref = run(p)
            for cfg in CONFIGS:
                kw = dict(cfg)
                if kw.get("cache"):
                    kw["cache"] = Cache()
                core = OutOfOrder(p.image, predictor=PR.Tournament(), **kw).run()
                self.assertTrue(same(core, ref), (seed, cfg))

    def test_job_on_a_paragraph(self):
        tape = b"It is a truth universally acknowledged, that a single man in possession of a good fortune, " \
               b"must be in want of a wife."
        p = assemble(P.JOB_V0)
        ref = run(p, tape=tape)
        for kw in ({"predictor": PR.Tournament()}, {"perfect_prediction": True}):
            core = OutOfOrder(p.image, tape=tape, **kw).run()
            self.assertTrue(same(core, ref))
            self.assertGreater(core.ipc, 1.0)

    def test_precise_division_by_zero(self):
        src = "li a0, 11\nli s0, 0x800\nsw a0, 0(s0)\nli a1, 0\ndiv a2, a0, a1\nsw a0, 4(s0)\nhalt"
        core = OutOfOrder(assemble(src).image).run()
        self.assertIn("division by zero", core.error)
        self.assertEqual(int.from_bytes(core.mem[0x800:0x804], "little"), 11)
        self.assertEqual(int.from_bytes(core.mem[0x804:0x808], "little"), 0)

    def test_memory_order_violation(self):
        src = """
        li   s0, 0x800
        li   a0, 1000
        li   a1, 1000
        div  a2, a0, a1       # 1, after sixteen cycles
        slli a2, a2, 2
        add  a3, s0, a2       # 0x804: the store's address is known late
        li   a4, 77
        sw   a4, 0(a3)
        lw   a5, 4(s0)        # the same word: a speculative load runs before the store and is wrong
        halt
        """
        p = assemble(src)
        ref = run(p)
        spec = OutOfOrder(p.image, disambiguation="speculative").run()
        cons = OutOfOrder(p.image, disambiguation="conservative").run()
        for c in (spec, cons):
            self.assertTrue(same(c, ref))
            self.assertEqual(c.regs[8], 77)
        self.assertGreaterEqual(spec.stats["violations"], 1)
        self.assertEqual(cons.stats["violations"], 0)

    def test_histogram_with_cache_misses(self):
        from videos.cs.cs8.compute import histogram_image

        src, img = histogram_image(n=200)
        ref = run(assemble(src))  # the emulator, on the same image
        from explainer.cs.pebble.emu import Machine

        m = Machine(img)
        while not m.halted:
            m.step()
        for mode in ("conservative", "speculative", "wait-table"):
            c = OutOfOrder(img, predictor=PR.Tournament(), disambiguation=mode, cache=Cache()).run()
            self.assertEqual(c.regs, m.regs, mode)
            self.assertEqual(bytes(c.mem[0x1000:0x1100]), bytes(m.mem[0x1000:0x1100]), mode)
        self.assertGreater(ref.steps, 0)

    def test_partial_forwarding(self):
        src = "li s0, 0x800\nli a0, 0x11223344\nsw a0, 0(s0)\nli a1, 0x99\nsb a1, 1(s0)\nlw a2, 0(s0)\n" \
              "lbu a3, 1(s0)\nlb a4, 1(s0)\nhalt"
        p = assemble(src)
        self.assertTrue(same(OutOfOrder(p.image).run(), run(p)))


class Spectre(unittest.TestCase):
    def test_probe_timings_exclude_fence_training_barriers(self):
        from videos.cs.cs8.compute import _spectre

        plain, plain_rounds = _spectre(b"P")
        fenced, fenced_rounds = _spectre(b"P", "fence")
        self.assertEqual(bytes(plain.output), b"P")
        self.assertEqual(len(plain_rounds), 1)
        self.assertEqual(len(fenced_rounds), 1)
        self.assertEqual(len(fenced_rounds[0]), 255)
        self.assertEqual(plain_rounds[0][ord("P") - 1], 5)
        self.assertEqual(set(fenced_rounds[0]), {63})
        # Equal probe times select line 1 in the actual attack's decoder.
        self.assertEqual(list(fenced.output), [1])

    def test_leak_and_mitigations(self):
        secret = b"Pebble"
        leaked = OutOfOrder(P.spectre_image(secret), cache=Cache(), timer="cycles", predictor=PR.TwoBit(),
                            training="commit").run()
        self.assertEqual(bytes(leaked.output), secret)
        for mit in ("fence", "mask"):
            core = OutOfOrder(P.spectre_image(secret, mit), cache=Cache(), timer="cycles", predictor=PR.TwoBit(),
                              training="commit").run()
            self.assertNotEqual(bytes(core.output), secret)
        core = OutOfOrder(P.spectre_image(secret), cache=Cache(), timer="cycles", predictor=PR.TwoBit(),
                          training="commit", secure=True).run()
        self.assertNotEqual(bytes(core.output), secret)

    def test_secure_core_agrees(self):
        for seed in range(60):
            p = assemble(random_program(seed, mext=seed % 2 == 0))
            self.assertTrue(same(OutOfOrder(p.image, predictor=PR.Tournament(), secure=True).run(), run(p)), seed)


class Limits(unittest.TestCase):
    def test_orderings(self):
        tr = trace(assemble(P.fib(14)).image)
        ideal = schedule(tr).ipc
        self.assertGreaterEqual(ideal, schedule(tr, rename=False).ipc)
        self.assertGreaterEqual(ideal, schedule(tr, memory="conservative").ipc)
        pred = schedule(tr, branches=PR.Tournament()).ipc
        self.assertGreater(pred, schedule(tr, branches="barrier").ipc)
        self.assertGreaterEqual(schedule(tr, width=8).ipc, schedule(tr, width=2).ipc)
        self.assertLessEqual(schedule(tr, width=2).ipc, 2.0)


if __name__ == "__main__":
    unittest.main()
