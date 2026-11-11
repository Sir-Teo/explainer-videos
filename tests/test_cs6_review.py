"""Regression checks for CS6's cached-only entry and directed overflow example."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from explainer.cs.pebble import assemble, run
from videos.cs.cs6 import compute as c


class Review(unittest.TestCase):
    def test_block_counts_exclude_storage_inputs(self):
        data = c.load("cpu")
        self.assertEqual(sum(data["blocks"].values()), data["gates"])
        self.assertEqual(data["blocks"]["register read"], 3416 - 15 * 32)
        self.assertEqual(data["flip_flops"], 16 * 32)

    def test_cached_only_cpu_entry_cannot_upgrade_stale_data(self):
        from tools.qa_series import StaleDataError, require_current_cache

        with TemporaryDirectory() as tmp:
            cache = type(c.CACHE)("cs6")
            cache.dir = Path(tmp)
            stale = b'{"blocks":{"register read":3416}}'
            cache.path("cpu").write_bytes(stale)
            original = cache.load

            def guarded(name):
                require_current_cache(c, "cs6", cache.path(name), name)
                return original(name)

            with patch.object(c, "CACHE", cache), patch.object(cache, "load", guarded):
                with patch.object(c, "compute_cpu") as producer:
                    with self.assertRaises(StaleDataError):
                        c.load("cpu")
                    producer.assert_not_called()
            self.assertEqual(cache.path("cpu").read_bytes(), stale)

    def test_stale_isa_rejected_before_upgrade_in_cached_only_mode(self):
        from tools.qa_series import StaleDataError, require_current_cache

        with TemporaryDirectory() as tmp:
            cache = type(c.CACHE)("cs6")
            cache.dir = Path(tmp)
            old = b'{"rv":[["stop","halt","ecall to an OS"]]}'
            cache.path("isa").write_bytes(old)
            original = cache.load

            def guarded(name):
                require_current_cache(c, "cs6", cache.path(name), name)
                return original(name)

            with patch.object(c, "CACHE", cache), patch.object(cache, "load", guarded):
                with patch.object(c, "compute_isa") as producer:
                    with self.assertRaises(StaleDataError):
                        c.load("isa")
                    producer.assert_not_called()
            self.assertEqual(cache.path("isa").read_bytes(), old)

            # Normal loading may upgrade; subsequent guarded reads must reuse it.
            with patch.object(c, "CACHE", cache):
                upgraded = c.load("isa")
                row = next(r for r in upgraded["rv"] if r[0] == "stop / environment call")
                self.assertIn("trap", row[2])
                self.assertEqual(upgraded["n_ops"], 34)
                require_current_cache(c, "cs6", cache.path("isa"), "isa")
                with patch.object(cache, "load", guarded), patch.object(c, "compute_isa") as producer:
                    self.assertEqual(c.load("isa"), upgraded)
                    producer.assert_not_called()
                self.assertEqual(json.loads(cache.path("isa").read_text()), upgraded)

    def test_directed_boundary_pair_exposes_divide_mutant(self):
        from explainer.cs.pebble.emu import Machine

        p = assemble("li a0, 0x80000000\nli a1, -1\ndiv a2, a0, a1\nhalt")
        reference = run(p)
        Mutant = c._mutant_class()
        mutant = Mutant(p.image)
        mutant.bug = "div of -2^31 by -1 returns 0"
        mutant.run()
        self.assertEqual(reference.regs[5], 0x80000000)
        self.assertEqual(mutant.regs[5], 0)
        self.assertEqual(reference.steps, mutant.steps)
        # The neighbouring dividend is not an overflow and must remain unchanged.
        q = assemble("li a0, 0x80000001\nli a1, -1\ndiv a2, a0, a1\nhalt")
        expected = Machine(q.image).run()
        actual = Mutant(q.image)
        actual.bug = mutant.bug
        actual.run()
        self.assertEqual(expected.regs[5], 0x7FFFFFFF)
        self.assertEqual(actual.regs, expected.regs)


if __name__ == "__main__":
    unittest.main()
