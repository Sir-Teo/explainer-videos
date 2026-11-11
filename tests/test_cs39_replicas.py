"""Tests for Part 39's replica, service, clock and history instruments."""

import unittest

from explainer.cs.dist import clocks, history, replicas, service


class TestReplicas(unittest.TestCase):
    def test_lww(self):
        rows = replicas.lww_pairs(skews_ms=(0, 250), seconds=200)
        self.assertEqual(rows[0]["inversions"], 0.0)
        self.assertGreater(rows[1]["inversions"], 0.0)
        self.assertAlmostEqual(rows[0]["concurrent"], rows[1]["concurrent"])

    def test_merkle_finds_all(self):
        for kwargs in ({"fanout": 1}, {"leaf": 0}, {"keys": 0}):
            with self.assertRaises(ValueError):
                replicas.merkle_sync(**kwargs)
        m = replicas.merkle_sync(keys=1 << 12, diffs=(0, 1, 7, 50))
        for r in m["rows"]:
            self.assertTrue(r["found_all"])
        self.assertEqual(m["rows"][0]["merkle_bytes"], 16)
        self.assertLess(m["rows"][1]["merkle_bytes"], m["rows"][1]["naive_bytes"])

    def test_rga_converges(self):
        for s in range(40):
            self.assertTrue(replicas.edit_session("rga", seed=s)["converged"])
        d = replicas.rga_demo()
        self.assertEqual(d["rga"]["a"], "the fat cat ran")
        self.assertEqual(d["rga"]["a"], d["rga"]["b"])
        self.assertNotEqual(d["naive"]["a"], d["naive"]["b"])

    def test_rga_local_semantics(self):
        r = replicas.Rga(1)
        for k, ch in enumerate("abc"):
            r.local_insert(k, ch)
        r.local_insert(1, "X")
        r.local_delete(0)
        self.assertEqual(r.text(), "Xbc")

    def test_hot(self):
        h = replicas.hot_shards(shards=20, keys=20000, requests=200000, zipf_s=(0.0, 1.2))
        self.assertLess(h["rows"][0]["max_over_mean"], 1.2)
        self.assertGreater(h["rows"][1]["max_over_mean"], h["rows"][1]["salted_max_over_mean"])


class TestService(unittest.TestCase):
    def test_balance_order(self):
        r = {p: service.balance(p, servers=20, load=0.9, jobs=20000)["p99"]
             for p in ("random", "two choices", "shortest queue")}
        self.assertGreater(r["random"], r["two choices"])
        self.assertGreater(r["two choices"], r["shortest queue"])

    def test_availability(self):
        a = service.availability(trials=200000)
        self.assertAlmostEqual(a["series"][2]["up"], 0.999 ** 10)
        self.assertLess(a["corr"]["same_rack"], a["corr"]["three_racks"])

    def test_detector_tradeoff(self):
        d = service.detector(hours=1.0)
        fp = [r["false_per_hour"] for r in d["fixed"]]
        self.assertEqual(fp, sorted(fp, reverse=True))

    def test_chain(self):
        c = service.call_chain(depths=(1, 5), trials=20000)
        self.assertLess(c[1]["p99"], c[1]["sum_of_p99"])


class TestClocksHistory(unittest.TestCase):
    def test_hlc(self):
        h = clocks.hlc_trace(events=4000)
        self.assertEqual(h["schemes"]["hlc"]["violations"], 0.0)
        self.assertGreater(h["schemes"]["physical"]["violations"], 0.0)
        self.assertLessEqual(h["schemes"]["hlc"]["max_drift_ms"], h["eps_ms"] + 1e-9)

    def test_history(self):
        c = history.campaign(txns=400)
        self.assertEqual(c["serializable"]["cyclic_components"], 0)
        self.assertGreater(c["stale replica"]["cyclic_components"], 0)


if __name__ == "__main__":
    unittest.main()
