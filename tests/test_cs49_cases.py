import unittest

from explainer.cs.design import cases


class Cases(unittest.TestCase):
    def test_base62(self):
        self.assertEqual(cases.base62(0), "0")
        self.assertEqual(cases.base62(61), "Z")
        self.assertEqual(cases.base62(62), "10")

    def test_ledger_invariant(self):
        self.assertEqual(cases.ledger(800)["sum"], 0)
        self.assertEqual(cases.ledger(800)["double_charges"], 0)
        self.assertGreater(cases.ledger(800, idempotent=False)["double_charges"], 0)

    def test_ot_converges(self):
        r = cases.ot_experiment(trials=2000)
        self.assertEqual(r["converged_transformed"], 1.0)
        self.assertLess(r["converged_naive"], 0.3)

    def test_bloom(self):
        r = cases.bloom_check(n=50_000)
        self.assertAlmostEqual(r["false_positive"], r["theory"], delta=0.005)

    def test_batched_beats_greedy(self):
        r = cases.dispatch(rounds=20)
        self.assertLess(r["batched_mean"], r["greedy_mean"])


if __name__ == "__main__":
    unittest.main()
