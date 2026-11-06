import unittest

from explainer.cs.data import columnar, log, stream


class Log(unittest.TestCase):
    def test_compaction_keeps_state(self):
        self.assertTrue(log.compaction_demo(500, 20)["same_state"])

    def test_sticky_moves_less(self):
        r = log.rebalance_demo()
        self.assertLess(r["moved_sticky"], r["moved_range"])

    def test_assignment_covers(self):
        a = log.assign(10, ["x", "y", "z"])
        self.assertEqual(sorted(p for v in a.values() for p in v), list(range(10)))


class Stream(unittest.TestCase):
    def test_watermark_tradeoff(self):
        ev = stream.make_events(n=1000)
        fast = stream.run_windows(ev, watermark_lag=0.0)
        slow = stream.run_windows(ev, watermark_lag=60.0)
        self.assertLess(fast["complete"], slow["complete"])
        self.assertLess(fast["mean_latency"], slow["mean_latency"])

    def test_snapshot_exact(self):
        self.assertTrue(stream.barrier_snapshot(stream.make_events(n=1200), crash_at=900)["exact_with_snapshots"])

    def test_windows(self):
        self.assertEqual(stream.tumbling(12.0, 10), [(10, 20)])
        self.assertEqual(len(stream.sliding(12.0, 10, 5)), 2)
        self.assertEqual(stream.sessions([1, 2, 10], 3), [(1, 5), (10, 13)])


class Columnar(unittest.TestCase):
    def test_dremel_roundtrip(self):
        d = columnar.dremel_example()
        want = [[[kw for kw in ch["keywords"]] for ch in b["chapters"]] for b in d["records"]]
        self.assertEqual(columnar.reassemble(d["levels"]), want)

    def test_dictionary_smaller(self):
        w = ("the whale the sea a ship the whale " * 500).split()
        e = columnar.encode_words(w)
        self.assertLess(e["dictionary"], e["plain"])

    def test_pushdown(self):
        self.assertEqual(columnar.pushdown(n=100_000, group=10_000, lo=42_000, hi=43_000)["read"], 1)


if __name__ == "__main__":
    unittest.main()
