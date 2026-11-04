"""Part 9: the cache simulator and its analyses agree with brute force; a hierarchy charges the right latencies;
the memory trace is the emulator's."""

from __future__ import annotations

import itertools
import random
import unittest

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
