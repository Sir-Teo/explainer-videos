"""Tests for Part 50's instruments (explainer/cs/ops)."""

from __future__ import annotations

import math
import random
import unittest

from explainer.cs.ops import chaos, observe, overload, profile, reliability, slo


class Reliability(unittest.TestCase):
    def test_laws(self):
        self.assertAlmostEqual(reliability.evaluate(("series", [0.99, 0.99])), 0.9801)
        self.assertAlmostEqual(reliability.evaluate(("parallel", [0.99, 0.99])), 0.9999)
        # 2 of 3 by the DP equals the closed form 3a^2 - 2a^3
        a = 0.9
        self.assertAlmostEqual(reliability.evaluate(("kofn", 2, [a] * 3)), 3 * a * a - 2 * a ** 3)

    def test_nines(self):
        self.assertAlmostEqual(reliability.downtime(0.999)["per_month_min"], 43.2)
        self.assertAlmostEqual(reliability.nines(0.9999), 4.0)

    def test_lever(self):
        rows = {r["case"]: r["up"] for r in reliability.mttr_lever()}
        self.assertAlmostEqual(rows["fail half as often"], rows["repair twice as fast"])

    def test_renewal(self):
        r = reliability.renewal(years=400)
        self.assertLess(abs(r["measured"] - r["formula"]), 0.001)

    def test_common_mode(self):
        rows = reliability.common_mode(trials=200_000)
        self.assertAlmostEqual(rows[0]["exact"], rows[0]["independent"])
        self.assertTrue(all(x["exact"] >= y["exact"] for x, y in zip(rows, rows[1:])))


class Slo(unittest.TestCase):
    def test_thresholds(self):
        t = slo.thresholds()
        self.assertAlmostEqual(t[0]["burn"], 14.4)
        self.assertAlmostEqual(t[1]["burn"], 6.0)

    def test_rules(self):
        r = {x["rule"]: x for x in slo.score()["rules"]}
        best = r["multiwindow, multi-burn-rate"]
        self.assertEqual(best["missed"], [])
        self.assertEqual(best["needless"], 0)
        self.assertGreater(r["error rate > 0.1% over 10 minutes"]["needless"], 0)
        self.assertTrue(r["burn > 14.4 over 1 hour"]["missed"])


class Overload(unittest.TestCase):
    def test_jitter_finishes(self):
        for s in ("full jitter", "equal jitter", "decorrelated jitter"):
            self.assertEqual(overload.contention(s, clients=20)["finished"], 20)

    def test_metastable(self):
        self.assertIsNone(overload.overload("retries")["recovered_s"])
        self.assertIsNotNone(overload.overload("none")["recovered_s"])
        self.assertIsNotNone(overload.overload("budget")["recovered_s"])

    def test_bulkhead(self):
        b = overload.bulkhead(True)
        self.assertGreater(min(b["share"]["A"]), 0.95)

    def test_hedging(self):
        rows = overload.hedging(trials=20_000)
        self.assertLess(rows[1]["p99"], rows[0]["p99"])


class Observe(unittest.TestCase):
    def test_ddsketch_guarantee(self):
        rng = random.Random(0)
        xs = sorted(rng.lognormvariate(3, 1.5) for _ in range(20_000))
        d = observe.DDSketch(0.01)
        for x in xs:
            d.add(x)
        for q in (0.5, 0.9, 0.99, 0.999):
            true = xs[int(q * (len(xs) - 1))]
            self.assertLessEqual(abs(d.quantile(q) - true) / true, 0.0101)

    def test_critical_path_tiles(self):
        e = observe.example_trace()
        segs = e["critical"]
        self.assertAlmostEqual(sum(b - a for _, a, b in segs), e["total"])
        for (_, _, b), (_, a, _) in zip(segs, segs[1:]):
            self.assertAlmostEqual(a, b)

    def test_omission(self):
        r = observe.coordinated_omission(seconds=80)
        self.assertLess(r["closed loop"]["p99"], 10)
        self.assertGreater(r["true"]["p99"], 1000)

    def test_mva_bound(self):
        r = observe.mva(150, 0.01, 1.0)
        self.assertLessEqual(r["X"], 100.0 + 1e-9)

    def test_change_point(self):
        c = observe.change_point(perms=200)
        self.assertLessEqual(abs(c["found"] - c["at"]), 2)
        self.assertLess(c["p"], 0.01)


class Profile(unittest.TestCase):
    def test_flame_widths(self):
        f = profile.flame({"a;b": 3, "a;c": 1, "d": 4})
        roots = [r for r in f if r["depth"] == 0]
        self.assertAlmostEqual(sum(r["w"] for r in roots), 1.0)
        a = next(r for r in f if r["name"] == "a")
        self.assertAlmostEqual(a["w"], 0.5)

    def test_guest_profile_small(self):
        g = profile.guest_profile(chars=1500, interval=101)
        self.assertGreater(g["samples"], 50)
        top = g["rows"][0]
        self.assertTrue(top["stack"].startswith("main"))
        self.assertLess(abs(top["z"]), 5)


class Chaos(unittest.TestCase):
    def test_configs_order(self):
        e = chaos.service_experiment()["runs"]
        self.assertLess(e["naive"]["good"], e["timeouts and retry"]["good"])
        self.assertLessEqual(e["timeouts and retry"]["good"], e["retry, ejection and hedging"]["good"])

    def test_raft_safe(self):
        r = chaos.raft_chaos(seconds=30)
        self.assertEqual(r["violations"], 0)
        self.assertGreater(r["available"], 0.9)


if __name__ == "__main__":
    unittest.main()

_ = math
