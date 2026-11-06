import unittest

from explainer.cs.people import colour, experiments, hci


class Hci(unittest.TestCase):
    def test_fitts_is_linear_in_id(self):
        f = hci.fitts_experiment(trials=150)
        self.assertGreater(f["r2"], 0.95)
        self.assertGreater(f["b"], 0)

    def test_nielsen_landauer(self):
        self.assertAlmostEqual(hci.nielsen_landauer(0.31)[5]["found"], 1 - 0.69 ** 5)

    def test_klm(self):
        self.assertAlmostEqual(hci.klm("HMPB"), 0.4 + 1.35 + 1.1 + 0.1)


class Colour(unittest.TestCase):
    def test_reference_values(self):
        L, a, b = colour.oklab("#ff0000")              # Ottosson's published value for sRGB red
        self.assertAlmostEqual(L, 0.62796, places=4)
        self.assertAlmostEqual(a, 0.22486, places=4)
        self.assertAlmostEqual(colour.oklab("#ffffff")[0], 1.0, places=6)
        self.assertAlmostEqual(colour.lab("#ffffff")[0], 100.0, places=2)
        self.assertAlmostEqual(colour.contrast("#000000", "#ffffff"), 21.0)

    def test_cvd_keeps_greys(self):
        for k in colour.CVD:
            self.assertEqual(colour.simulate("#808080", k), "#808080")


class Experiments(unittest.TestCase):
    def test_sample_size(self):
        s = experiments.sample_size(0.05, 0.05)
        self.assertAlmostEqual(s["n_per_arm"] / s["rule_16"], 1, delta=0.05)

    def test_peeking_inflates(self):
        r = experiments.peeking(days=20, trials=800)
        self.assertGreater(r["fpr_peeking"][-1], 0.12)
        self.assertLess(r["fpr_final_only"], 0.08)

    def test_cuped(self):
        r = experiments.cuped(n=5000, trials=200)
        self.assertAlmostEqual(r["ratio"], r["theory"], delta=0.12)


if __name__ == "__main__":
    unittest.main()
