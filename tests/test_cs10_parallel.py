"""Part 10's instruments: MESI coherence, the store-buffering litmus test, schedules, scans, sorting networks."""

import itertools
import random
import platform
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from explainer.cs.pebble import parallel as Pa
from explainer.cs.pebble.coherence import MESI, litmus_sb


class TestMESI(unittest.TestCase):
    def test_invariant_and_values(self):
        """Random reads and writes by four cores: never two writable copies, and every read sees the last write."""
        rng = random.Random(3)
        m = MESI(cores=4, sets=4, ways=2)
        last = {}
        for t in range(20000):
            core = rng.randrange(4)
            addr = rng.randrange(24) * 64
            if rng.random() < 0.3:
                m.access(core, addr, write=True, value=t)
                last[addr] = t
            else:
                m.access(core, addr)
                self.assertEqual(m.read_value(core, addr), last.get(addr, 0))
            m.check()

    def test_transitions(self):
        m = MESI(cores=2)
        self.assertIn("Exclusive", m.access(0, 0))
        self.assertIn("silently", m.access(0, 0, write=True))
        self.assertEqual(m.state(0, 0), "M")
        self.assertIn("supplies", m.access(1, 0))
        self.assertEqual((m.state(0, 0), m.state(1, 0)), ("S", "S"))
        self.assertIn("invalidate", m.access(1, 0, write=True))
        self.assertEqual((m.state(0, 0), m.state(1, 0)), ("I", "M"))


class TestLitmus(unittest.TestCase):
    def test_sc_forbids_both_zero(self):
        self.assertNotIn("r0=0, r1=0", litmus_sb("sc", trials=20000))

    def test_tso_allows_it(self):
        self.assertGreater(litmus_sb("tso", trials=20000).get("r0=0, r1=0", 0), 0.01)


class TestSchedules(unittest.TestCase):
    def test_brent(self):
        for seed in range(20):
            d = Pa.Dag.random(300, width=10, fan=3, seed=seed)
            t1, tinf = d.work(), d.span()
            for p in (1, 2, 3, 4, 8, 16):
                g = Pa.greedy(d, p)
                self.assertLessEqual(g["makespan"], t1 / p + tinf)
                self.assertGreaterEqual(g["makespan"], max(t1 / p, tinf))
                self.assertLessEqual(g["incomplete"], tinf)

    def test_critical_path(self):
        d = Pa.Dag.random(100, seed=4)
        path = d.critical_path()
        self.assertEqual(len(path), d.span())
        for a, b in zip(path, path[1:]):
            self.assertIn(a, d.preds[b])

    def test_stealing_finishes(self):
        d = Pa.fork_join_tree(8)
        for p in (1, 2, 4, 8):
            s = Pa.steal(d, p, seed=p)
            self.assertGreaterEqual(s["makespan"], max(d.work() / p, d.span()))
        self.assertEqual(Pa.steal(d, 1)["makespan"], d.work())


class TestScan(unittest.TestCase):
    def test_noncommutative_scan_preserves_operand_order(self):
        xs = list("abcdefgh")
        expected = ["".join(xs[:i]) for i in range(len(xs))]
        self.assertEqual(Pa.blelloch(xs, op=lambda a, b: a + b, identity="")["result"], expected)
        # Generate/propagate composition is also associative but not commutative.
        gp = [(0, 1), (1, 0), (0, 0), (0, 1), (1, 0), (0, 1), (0, 0), (1, 0)]
        compose = lambda lo, hi: (hi[0] | hi[1] & lo[0], hi[1] & lo[1])
        cur, expected = (0, 1), []
        for pair in gp:
            expected.append(cur)
            cur = compose(cur, pair)
        self.assertEqual(Pa.blelloch(gp, op=compose, identity=(0, 1))["result"], expected)

    def test_blelloch_rejects_empty_or_non_power_of_two(self):
        for xs in ([], [1, 2, 3]):
            with self.assertRaises(ValueError):
                Pa.blelloch(xs)

    def test_scans(self):
        rng = random.Random(1)
        xs = [rng.randrange(100) for _ in range(64)]
        incl = list(itertools.accumulate(xs))
        self.assertEqual(Pa.hillis_steele(xs)["result"], incl)
        b = Pa.blelloch(xs)
        self.assertEqual(b["result"], [0] + incl[:-1])
        self.assertEqual(b["ops"], 2 * (len(xs) - 1))


class TestNetworks(unittest.TestCase):
    def test_sorters(self):
        for n in (2, 4, 8):
            for net in (Pa.bitonic(n), Pa.odd_even_merge(n)):
                self.assertTrue(Pa.sorts_all_perms(net, n))
        for n in range(2, 8):
            self.assertTrue(Pa.sorts_all_perms(Pa.transposition(n), n))
            self.assertTrue(Pa.sorts_all_perms(Pa.insertion(n), n))

    def test_zero_one_principle(self):
        """For small n, the 0-1 test and the permutation test agree on every network with one comparator removed."""
        for n in (4, 5, 6):
            net = Pa.transposition(n)
            for k in range(len(net)):
                broken = net[:k] + net[k + 1:]
                ok01, bad = Pa.sorts_all_01(broken, n)
                self.assertEqual(ok01, Pa.sorts_all_perms(broken, n))
                if not ok01:
                    self.assertNotEqual(Pa.apply(broken, bad), sorted(bad))

    def test_depth(self):
        self.assertEqual(len(Pa.layers(Pa.bitonic(8))), 6)
        self.assertEqual(len(Pa.bitonic(8)), 24)
        self.assertEqual(len(Pa.odd_even_merge(8)), 19)


class TestTopologies(unittest.TestCase):
    def test_bisection(self):
        self.assertEqual(Pa.bisection(Pa.ring(8), 8), 2)
        self.assertEqual(Pa.bisection(Pa.hypercube(3), 8), 4)
        self.assertEqual(Pa.bisection(Pa.mesh(4), 16), 4)
        self.assertEqual(Pa.bisection(Pa.mesh(4, wrap=True), 16), 8)
        self.assertEqual(Pa.bisection(Pa.tree(8), 8), 1)
        self.assertEqual(Pa.diameter(Pa.hypercube(4)), 4)


class TestCompiledDemonstrations(unittest.TestCase):
    def test_counter_variants_check_actual_compiled_counts(self):
        from videos.cs.cs10 import compute as C

        for mode in range(5):
            with self.subTest(mode=mode):
                output = C._run_c(C.ATOMICS, [4, mode], extra=["-DN=20000"])[0]
                count, _ = output.split()
                if mode:
                    self.assertEqual(int(count), 80000)
                else:
                    self.assertGreater(int(count), 0)
                    self.assertLessEqual(int(count), 80000)

    @unittest.skipUnless(platform.machine().lower() in ("x86_64", "amd64"), "x86 mfence experiment")
    def test_compiled_litmus_counts_and_fenced_outcome(self):
        from videos.cs.cs10 import compute as C

        for fence in (False, True):
            output = C._run_c(C.LITMUS, [20000], extra=["-DFENCE"] if fence else [])[0]
            counts = list(map(int, output.split()))
            self.assertEqual(sum(counts), 20000)
            if fence:
                self.assertEqual(counts[0], 0)


class TestMeasurementCache(unittest.TestCase):
    def test_read_only_legacy_measurements_are_rejected_unchanged(self):
        import json
        from explainer.ai.cache import Cache
        from videos.cs.cs10 import compute as C

        for name in ("litmus", "atomics", "split", "workspan"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                cache = Cache("cs10")
                cache.dir = Path(d)
                cache.path(name).write_text(json.dumps({"rows": []}))
                original = cache.path(name).read_bytes()
                with mock.patch.object(C, "CACHE", cache):
                    self.assertFalse(C.cache_current(name))
                    with self.assertRaisesRegex(RuntimeError, "Legacy cs10/" + name):
                        C.load(name)
                self.assertEqual(cache.path(name).read_bytes(), original)

    def test_compute_refreshes_legacy_and_reuses_current_measurement(self):
        import json
        from explainer.ai.cache import Cache
        from videos.cs.cs10 import compute as C

        with tempfile.TemporaryDirectory() as d:
            cache = Cache("cs10")
            cache.dir = Path(d)
            cache.path("atomics").write_text(json.dumps({"rows": []}))
            fresh = {"rows": [], "access_schema": "defined-atomics-v1"}
            producer = mock.Mock(return_value=fresh)
            with mock.patch.object(C, "CACHE", cache), mock.patch.object(C, "ITEMS", {"atomics": producer}):
                C.main([])
                C.main(["atomics"])
                self.assertEqual(C.load("atomics"), fresh)
            producer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
