"""Part 39's instruments: quorums, CRDTs, partitioning, transactions, the tail, and MapReduce."""
from __future__ import annotations

import unittest

from explainer.cs.dist import scale as S
from explainer.cs.dist.mapreduce import run_job


class Quorums(unittest.TestCase):
    def test_strict_quorums_never_stale(self):
        self.assertEqual(S.pbs(3, 2, 2, 0.0, 5000), 0.0)
        self.assertGreater(S.pbs(3, 1, 1, 0.0, 5000), 0.3)
        self.assertLess(S.pbs(3, 1, 1, 50.0, 5000), 0.02)


class Crdts(unittest.TestCase):
    def test_counter_monotonicity_contract(self):
        a, b = S.GCounter(2, 0), S.GCounter(2, 1)
        a.inc(3)
        b.inc(2)
        a.merge(b)
        a.merge(b)
        self.assertEqual(a.value(), 5)
        with self.assertRaises(ValueError):
            a.inc(-1)
        with self.assertRaises(ValueError):
            a.merge(S.GCounter(3, 0))
        with self.assertRaises(ValueError):
            S.PNCounter(2, 0).dec(-1)

    def test_crdts_converge_naive_does_not(self):
        for k in ("gcounter", "pncounter", "orset", "lww"):
            r = S.crdt_converge(k, trials=100)
            self.assertEqual(r["converged"], r["trials"], k)
        self.assertLess(S.crdt_converge("naive-set", trials=100)["converged"], 50)


class Partitioning(unittest.TestCase):
    def test_vnodes_balance_and_minimal_movement(self):
        self.assertLess(S.ring_load(10, 200, 20000)["max_over_mean"], S.ring_load(10, 1, 20000)["max_over_mean"])
        m = S.moved_fraction(10, keys=20000)
        self.assertGreater(m["modulo"], 0.8)
        for k in ("ring", "jump", "rendezvous"):
            self.assertLess(m[k], 0.15)

    def test_chord_logarithmic(self):
        a, b = S.chord_hops(64, 500)["mean"], S.chord_hops(4096, 500)["mean"]
        self.assertLess(b, a + 6)


class Tail(unittest.TestCase):
    def test_fanout_amplifies_and_hedging_helps(self):
        t = {r["fanout"]: r for r in S.tail(fanouts=(1, 100), trials=10000)}
        self.assertAlmostEqual(t[100]["frac_slow"], 0.634, delta=0.06)
        h = {r["fanout"]: r for r in S.tail(fanouts=(100,), trials=60000, hedge_at=30)}
        self.assertLess(h[100]["p99"], t[100]["p99"])


class MapReduce(unittest.TestCase):
    def test_job_with_crash_is_correct(self):
        text = (b"the whale and the sea and the ship " * 300) + b"call me ishmael " * 50
        from explainer.cs.pebble import programs as PR
        ref = [(ln.split()[0], int(ln.split()[1])) for ln in PR.job_reference(text).decode().splitlines()]
        for kw in ({}, {"crash": (2, 0.06)}, {"slow": {1: 5.0}}):
            r = run_job(text, workers=4, maps=8, reduces=3, **kw)
            self.assertEqual(r["top"], ref, kw)


if __name__ == "__main__":
    unittest.main()
