import unittest

from explainer.cs.cloud import control, cost, durability, packing


class Packing(unittest.TestCase):
    def test_optimum_and_heuristics(self):
        items = [0.6, 0.2, 0.2, 0.4, 0.4, 0.2]
        self.assertEqual(packing.optimum(items), 2)
        self.assertGreaterEqual(len(packing.next_fit(items)), 2)
        self.assertEqual(len(packing.ffd(items)), 2)

    def test_next_fit_bad(self):
        r = packing.next_fit_bad(200)
        self.assertGreater(r["ratio"], 1.9)

    def test_partition(self):
        self.assertTrue(packing.partition_reduction((3, 1, 1, 2, 2, 1))["partition_exists"])
        self.assertFalse(packing.partition_reduction((3, 3, 3, 1))["partition_exists"])


class Control(unittest.TestCase):
    def test_erlang(self):
        self.assertAlmostEqual(control.erlang_c(2, 1.0), 1 / 3)
        self.assertAlmostEqual(control.erlang_c(1, 0.5), 0.5)

    def test_reconcile(self):
        r = control.reconcile()["series"]
        self.assertEqual(r["level"][-1], 5)
        self.assertLess(r["edge"][-1], 5)

    def test_plan_order(self):
        steps = control.plan_example()["steps"]
        names = [n for _, n in steps]
        self.assertLess(names.index("queue"), names.index("service"))
        self.assertEqual(steps[-1], ("destroy", "old-cache"))


class Durability(unittest.TestCase):
    def test_simulation_matches(self):
        r = durability.simulate(trials=1500)
        self.assertAlmostEqual(r["simulated_years"] / r["exact_years"], 1, delta=0.1)

    def test_single_copy(self):
        self.assertAlmostEqual(durability.mttdl(1, 1, 0.02)["p_loss_year"], 0.02, places=6)


class Cost(unittest.TestCase):
    def test_breakeven(self):
        r = cost.serverless_vs_server()
        self.assertGreater(r["breakeven_rps"], 10)


if __name__ == "__main__":
    unittest.main()
