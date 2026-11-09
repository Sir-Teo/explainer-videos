"""Part 9: the cache simulator and its analyses agree with brute force; a hierarchy charges the right latencies;
the memory trace is the emulator's."""

from __future__ import annotations

import itertools
import random
import unittest
from unittest import mock

import numpy as np

from explainer.cs.pebble import assemble
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.cache import (Hierarchy, SetAssoc, belady, memtrace, miss_curve, stack_distances,
                                       three_c)


def brute_distances(lines):
    out = []
    for t, ln in enumerate(lines):
        prev = [i for i in range(t) if lines[i] == ln]
        if not prev:
            out.append(-1)
        else:
            out.append(len(set(lines[prev[-1] + 1:t])))
    return out


def brute_opt(lines, cap):
    """Optimal misses by trying every eviction choice (tiny inputs only)."""
    best = [None]

    def go(t, cache, misses):
        if best[0] is not None and misses >= best[0]:
            return
        if t == len(lines):
            best[0] = misses
            return
        ln = lines[t]
        if ln in cache:
            go(t + 1, cache, misses)
            return
        if len(cache) < cap:
            go(t + 1, cache | {ln}, misses + 1)
            return
        for v in cache:
            go(t + 1, (cache - {v}) | {ln}, misses + 1)

    go(0, frozenset(), 0)
    return best[0]


class Analyses(unittest.TestCase):
    def test_stack_distances(self):
        rng = random.Random(3)
        for _ in range(50):
            lines = [rng.randrange(8) for _ in range(rng.randrange(1, 60))]
            self.assertEqual(list(stack_distances(lines)), brute_distances(lines))

    def test_miss_curve_is_fully_associative_lru(self):
        rng = random.Random(4)
        lines = [rng.randrange(40) if rng.random() < 0.7 else rng.randrange(400) for _ in range(3000)]
        d = stack_distances(lines)
        for cap in (1, 4, 16, 64):
            c = SetAssoc(cap * 64, line=64, ways=cap)
            misses = sum(not c.access(ln * 64) for ln in lines)
            self.assertAlmostEqual(miss_curve(d, [cap])[0], misses / len(lines))

    def test_belady_is_optimal(self):
        rng = random.Random(5)
        for _ in range(40):
            lines = [rng.randrange(6) for _ in range(rng.randrange(1, 14))]
            for cap in (1, 2, 3):
                self.assertEqual(belady(lines, cap), brute_opt(lines, cap))
        lines = [rng.randrange(100) for _ in range(5000)]
        d = stack_distances(lines)
        for cap in (8, 32):
            self.assertLessEqual(belady(lines, cap), round(miss_curve(d, [cap])[0] * len(lines)))

    def test_three_c(self):
        rng = random.Random(6)
        lines = [rng.randrange(300) for _ in range(4000)]
        r = three_c(lines, sets=8, ways=4)
        self.assertEqual(r["compulsory"], len(set(lines)))
        self.assertEqual(r["compulsory"] + r["capacity"] + r["conflict"], r["misses"])
        # a direct-mapped cache conflicts on two lines mapping to one set
        r = three_c([0, 8, 0, 8, 0, 8], sets=8, ways=1)
        self.assertEqual((r["compulsory"], r["capacity"], r["conflict"]), (2, 0, 4))


class Caches(unittest.TestCase):
    def test_plru_refills_the_invalidated_physical_way(self):
        for invalidated in range(4):
            with self.subTest(invalidated=invalidated):
                c = SetAssoc(4 * 64, ways=4, policy="plru")
                for line in range(4):
                    c.access(line * 64)
                c.flush_line(invalidated * 64)
                c.access(4 * 64)
                self.assertEqual(set(c.ways_of[0].values()), set(range(4)))
                self.assertEqual(c.ways_of[0][4], invalidated)
                for line in range(5, 25):
                    c.access(line * 64)
                    self.assertEqual(len(set(c.ways_of[0].values())), 4)

    def test_plru_with_two_ways_is_lru(self):
        rng = random.Random(7)
        a, b = SetAssoc(4 * 2 * 64, ways=2, policy="lru"), SetAssoc(4 * 2 * 64, ways=2, policy="plru")
        for _ in range(5000):
            x = rng.randrange(64) * 64
            self.assertEqual(a.access(x), b.access(x))

    def test_writeback_and_writethrough(self):
        wb = SetAssoc(64 * 2, line=64, ways=2, write="back")
        for a in (0, 64, 128, 192):
            wb.access(a, write=True)
        self.assertEqual(wb.writebacks, 2)
        wt = SetAssoc(64 * 2, line=64, ways=2, write="through", allocate=False)
        wt.access(0, write=True)
        self.assertFalse(wt.present(0))
        self.assertEqual(wt.write_throughs, 1)

    def test_hierarchy_latency(self):
        h = Hierarchy([SetAssoc(1024, ways=2, hit=4), SetAssoc(8192, ways=4, hit=12)], dram=100)
        self.assertEqual(h.access(0), 4 + 12 + 100)
        self.assertEqual(h.access(4), 4)
        for k in range(1, 4):  # evict line 0 from L1 (one set, two ways) but not from L2
            h.access(k * 512)
        self.assertEqual(h.access(0), 4 + 12)

    def test_stride_prefetch(self):
        plain = Hierarchy([SetAssoc(4096, ways=4, hit=4)], dram=100)
        pre = Hierarchy([SetAssoc(4096, ways=4, hit=4)], dram=100, prefetch="stride")
        t0 = sum(plain.access(a) for a in range(0, 64 * 200, 64))
        t1 = sum(pre.access(a) for a in range(0, 64 * 200, 64))
        self.assertLess(t1, t0 / 2)


class Scans(unittest.TestCase):
    def test_compute_command_refreshes_legacy_but_reuses_current_data(self):
        import json
        import tempfile
        from pathlib import Path
        from explainer.ai.cache import Cache
        from videos.cs.cs9 import compute as C

        fresh = {"scalar_words": 8, "rows": [{"final_dirty_lines": 2}]}
        with tempfile.TemporaryDirectory() as d:
            cache = Cache("cs9")
            cache.dir = Path(d)
            cache.path("pebbles").write_text(json.dumps({"rows": [{"words": 42240}]}))
            producer = mock.Mock(return_value=fresh)
            with mock.patch.object(C, "CACHE", cache), mock.patch.object(C, "ITEMS", {"pebbles": producer}):
                C.main([])
                first = cache.path("pebbles").read_bytes()
                C.main(["pebbles"])
                self.assertEqual(cache.path("pebbles").read_bytes(), first)
            producer.assert_called_once()
            self.assertEqual(json.loads(first), fresh)

    def test_predicted_scan_reads_match_the_emulator(self):
        from videos.cs.cs9.compute import scan_ends

        tape = (" ".join(chr(97 + i) for i in range(26)) + " a z aa ab az zz z").encode()
        program = assemble(P.JOB_V0)
        actual = memtrace(program.image, tape=tape)
        length_pc = program.labels["scan"] + 4
        ends = scan_ends(tape)
        expected = [P.TABLE + 12 * i + 4 for end in ends for i in range(int(end) + 1)]
        self.assertEqual(actual.addr[actual.pc == length_pc].tolist(), expected)
        self.assertEqual(int(ends[0]), -1)
        self.assertEqual(int(ends[1]), 0)

    def test_legacy_projection_data_is_rejected_without_computation(self):
        import json
        import tempfile
        from pathlib import Path
        from explainer.ai.cache import Cache
        from videos.cs.cs9 import compute as C

        for name, old in [("scans", {"rows": [{"kb": 32, "keep_front": 0.7}]}),
                          ("pebbles", {"rows": [{"words": 42240}]}),
                          ("job_memory", {"windows": []}),
                          ("job", {"clocks": {"this machine": {}}})]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                cache = Cache("cs9")
                cache.dir = Path(d)
                path = cache.path(name)
                original = json.dumps(old)
                path.write_text(original)
                with mock.patch.object(C, "CACHE", cache):
                    with self.assertRaisesRegex(RuntimeError, "Legacy cs9/" + name):
                        C.load(name)
                self.assertEqual(path.read_text(), original)

    def test_pinned_prefix_comparator_is_a_feasible_min_upper_bound(self):
        from videos.cs.cs9.compute import pinned_scan_misses

        rng = random.Random(81)
        cases = [[1] * 30, [0] * 20, [-1] * 10, [8, -1, 0, 5, 2, 8]]
        cases += [[rng.randrange(12) for _ in range(30)] for _ in range(10)]
        for ends in cases:
            seq = [ln for end in ends for ln in range(end + 1)]
            for cap in (1, 2, 4, 16):
                resident = set()
                misses = 0
                for ln in seq:
                    if ln not in resident:
                        misses += 1
                        resident.add(ln)
                    self.assertLessEqual(len(resident), cap)
                    if ln >= cap - 1:
                        resident.remove(ln)  # transient slot, explicitly discarded
                self.assertEqual(pinned_scan_misses(np.array(ends), cap), (len(seq), misses))
                self.assertLessEqual(belady(seq, cap), misses)

    def test_abstract_corpus_table_and_pool_do_not_alias(self):
        from videos.cs.cs9.compute import TABLE, window_events

        words = [f"w{i:05d}".encode() for i in range(40000)]
        words.append(words[0])
        lines, is_pool = window_events(words, 40000, 1)
        self.assertTrue(is_pool.any())
        # The corpus projection relocates the pool beyond the entire grown
        # table; otherwise unrelated objects become the same simulated line.
        self.assertGreater(int(lines[is_pool].min()), (TABLE + 12 * 40000 - 1) // 64)

    def test_prefix_scan_misses_are_lru(self):
        from videos.cs.cs9.compute import lru_scan_misses

        rng = random.Random(8)
        for _ in range(100):
            ends = [rng.randrange(30) for _ in range(rng.randrange(1, 40))]
            lines = [l for e in ends for l in range(e + 1)]
            d = stack_distances(lines)
            for cap in (1, 3, 8, 20):
                acc, mis = lru_scan_misses(np.array(ends), cap)
                self.assertEqual(acc, len(lines))
                self.assertEqual(mis, round(miss_curve(d, [cap])[0] * len(lines)))


class Trace(unittest.TestCase):
    def test_memtrace_counts(self):
        src = P.fib(10)
        p = assemble(src)
        t = memtrace(p.image)
        from explainer.cs.pebble.limits import trace

        tr = trace(p.image)
        n = sum(1 for k in tr.kind if k in ("load", "store"))
        self.assertEqual(len(t), n)
        self.assertTrue(np.all(t.addr < (1 << 20)))


if __name__ == "__main__":
    unittest.main()
