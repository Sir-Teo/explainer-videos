"""Part 37's transport instruments: reliable delivery, TCP on a bottleneck, the theory, and the layers above."""
from __future__ import annotations

import math
import random
import unittest

from explainer.cs.net import app, cc, rdt
from explainer.cs.net.tcp import Flow, dumbbell, jain, mathis


class AppEdges(unittest.TestCase):
    def test_guess_probabilities(self):
        self.assertAlmostEqual(app.kaminsky_odds(1, 0, 2), .75)
        self.assertAlmostEqual(app.kaminsky_odds(2, 0, 2, 3), 1 - (3 / 4)**6)
        self.assertGreater(app.kaminsky_odds(64, 0, 1), 0)
        self.assertEqual(app.kaminsky_odds(0, 0, 0), 0)
        self.assertEqual(app.kaminsky_odds(0, 0, 1), 1)

    def test_empty_and_full_caches_and_pages(self):
        self.assertEqual(app.lru_hit_rate([], 0), 0)
        self.assertEqual(app.che([.8, .2], 0), 0)
        self.assertEqual(app.che([.8, .2], 2), 1)
        self.assertAlmostEqual(app.che([.5, .5], 1), .5)
        for objects in ([], [0, 0]):
            self.assertEqual(app.page_load(objects, 0, .1, 100, "quic", random.Random(0))["page"], 0)
        with self.assertRaises(ValueError):
            app.page_load([1], 1, .1, 100, "quic", random.Random(0))


class Reliable(unittest.TestCase):
    def test_protocols_deliver_in_order_under_loss(self):
        ch = lambda s: rdt.Channel(delay=0.05, rate=1000, loss=0.05, dup=0.02, reorder=0.1, seed=s)  # noqa: E731
        for p in ("go-back-n", "selective-repeat"):
            self.assertTrue(rdt.run(p, 1500, window=16, channel=ch(1))["correct"])

    def test_alternating_bit_needs_fifo(self):
        ok = [rdt.run("stop-and-wait", 300, seq_bits=1, channel=rdt.Channel(loss=0.1, seed=s))["correct"]
              for s in range(5)]
        self.assertTrue(all(ok))
        bad = [rdt.run("stop-and-wait", 300, seq_bits=1, channel=rdt.Channel(loss=0.1, reorder=0.2, seed=s))["correct"]
               for s in range(5)]
        self.assertFalse(any(bad))

    def test_selective_repeat_needs_twice_the_window(self):
        ch = lambda: rdt.Channel(loss=0.1, seed=5)  # noqa: E731
        self.assertTrue(rdt.run("selective-repeat", 1500, window=4, seq_bits=3, channel=ch())["correct"])
        self.assertFalse(rdt.run("selective-repeat", 1500, window=5, seq_bits=3, channel=ch())["correct"])

    def test_window_utilization_formula(self):
        for W in (1, 8, 32):
            r = rdt.run("go-back-n" if W > 1 else "stop-and-wait", 1500, window=W,
                        channel=rdt.Channel(delay=0.05, rate=1000))
            self.assertAlmostEqual(r["utilization"], rdt.utilization(0.001, 0.1, W), delta=0.02)


class Tcp(unittest.TestCase):
    def test_reno_fills_a_bdp_buffer_and_shares_fairly(self):
        r = dumbbell([Flow("reno", rtt=0.1)], mbps=10, duration=30)
        self.assertGreater(r["utilization"], 0.95)
        r = dumbbell([Flow("reno", rtt=0.1), Flow("reno", rtt=0.1, start=5)], mbps=10, duration=60)
        self.assertGreater(jain(f["mbps"] for f in r["flows"]), 0.98)

    def test_mathis(self):
        r = dumbbell([Flow("reno", rtt=0.1)], mbps=100, buffer=8000, loss=1e-3, duration=200, warmup=40)
        self.assertAlmostEqual(r["flows"][0]["mbps"] / mathis(0.1, 1e-3), 1.0, delta=0.25)

    def test_bbr_ignores_random_loss(self):
        reno = dumbbell([Flow("reno", rtt=0.1)], mbps=10, duration=30, loss=0.01)["flows"][0]["mbps"]
        bbr = dumbbell([Flow("bbr", rtt=0.1)], mbps=10, duration=30, loss=0.01)["flows"][0]["mbps"]
        self.assertGreater(bbr, 3 * reno)


class Theory(unittest.TestCase):
    def test_only_aimd_is_fair_and_efficient(self):
        r = {k: cc.chiu_jain(k, steps=200) for k in ("AIMD", "AIAD", "MIMD")}
        self.assertGreater(r["AIMD"]["fairness"], 0.99)
        self.assertLess(r["AIAD"]["fairness"], 0.9)
        self.assertLess(r["MIMD"]["fairness"], 0.9)

    def test_proportional_fairness(self):
        n = cc.num_dual({"long": ["L1", "L2"], "a": ["L1"], "b": ["L2"]}, {"L1": 1.0, "L2": 1.0})
        self.assertAlmostEqual(n["x"]["long"], 1 / 3, delta=0.01)
        self.assertAlmostEqual(n["x"]["a"], 2 / 3, delta=0.01)


class Above(unittest.TestCase):
    def test_dns_cache_and_odds(self):
        res = app.Resolver({"moby.example": ("10.4.0.2", 300)})
        self.assertEqual(res.resolve("moby.example", 0)[1], 3)
        self.assertTrue(res.resolve("moby.example", 10)[2])
        self.assertFalse(res.resolve("moby.example", 400)[2])
        self.assertLess(app.kaminsky_odds(16, 16, 100, 650), app.kaminsky_odds(16, 0, 100, 1))

    def test_quic_avoids_head_of_line_blocking(self):
        rng = random.Random(1)
        objs = [30] + [8] * 40
        h2 = sum(app.page_load(objs, 0.05, 0.1, 1000, "http2", rng)["mean_object"] for _ in range(60))
        q = sum(app.page_load(objs, 0.05, 0.1, 1000, "quic", rng)["mean_object"] for _ in range(60))
        self.assertLess(q, h2)

    def test_lru_matches_che(self):
        rng = random.Random(2)
        n, s = 2000, 1.0
        w = [1 / (k ** s) for k in range(1, n + 1)]
        tot = sum(w)
        probs = [x / tot for x in w]
        reqs = rng.choices(range(n), probs, k=200_000)
        for size in (50, 200):
            self.assertAlmostEqual(app.lru_hit_rate(reqs, size), app.che(probs, size), delta=0.02)
        _ = math


if __name__ == "__main__":
    unittest.main()
