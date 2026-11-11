import unittest

from explainer.cs.design import cases


class Cases(unittest.TestCase):
    def test_base62(self):
        self.assertEqual(cases.base62(0), "0")
        self.assertEqual(cases.base62(61), "Z")
        self.assertEqual(cases.base62(62), "10")
        with self.assertRaises(ValueError):
            cases.base62(-1)
        self.assertEqual(cases.shortener(ns=(62**3,))["rows"][0]["length"], 3)
        r = cases.feed_cost(users=100, threshold=0)
        self.assertEqual(len(r["hybrid"]), 1)
        self.assertEqual(r["hybrid"][0]["push_writes"], 0)

    def test_ledger_invariant(self):
        self.assertEqual(cases.ledger(800)["sum"], 0)
        self.assertEqual(cases.ledger(800)["double_charges"], 0)
        self.assertGreater(cases.ledger(800, idempotent=False)["double_charges"], 0)

    def test_ot_converges(self):
        r = cases.ot_experiment(trials=2000)
        self.assertEqual(r["converged_transformed"], 1.0)
        self.assertLess(r["converged_naive"], 0.3)
        self.assertEqual(cases.ot_experiment(trials=100, start="")["converged_transformed"], 1)

    def test_bloom(self):
        r = cases.bloom_check(n=50_000)
        self.assertAlmostEqual(r["false_positive"], r["theory"], delta=0.005)

    def test_batched_beats_greedy(self):
        r = cases.dispatch(rounds=20)
        self.assertLess(r["batched_mean"], r["greedy_mean"])


if __name__ == "__main__":
    unittest.main()
