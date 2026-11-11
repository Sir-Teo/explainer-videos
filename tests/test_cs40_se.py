"""Tests for Part 40's software-engineering instruments (explainer/cs/se)."""

import unittest

from explainer.cs.se import kwic, process, repo, testing


class TestKwic(unittest.TestCase):
    def test_both_designs_agree_and_hiding_wins(self):
        e = kwic.experiment()
        self.assertEqual(len(e["index"]), 31)
        for r in e["rows"]:
            self.assertTrue(r["d1"]["same_output"] and r["d2"]["same_output"], r["change"])
            self.assertLessEqual(r["d2"]["n"], r["d1"]["n"])
        self.assertEqual([r["d2"]["n"] for r in e["rows"]], [1, 1, 1, 1])


class TestRepo(unittest.TestCase):
    def test_sccs(self):
        comps = repo.sccs(["a", "b", "c", "d"], {"a": ["b"], "b": ["c"], "c": ["a"], "d": ["a"]})
        self.assertIn(sorted(["a", "b", "c"]), [sorted(c) for c in comps])
        self.assertIn(["d"], comps)

    def test_ngram_entropy_prefers_repetition(self):
        rep = ["a", "b", "c"] * 400
        rnd = [str(i % 37 * 7919 % 101) for i in range(1200)]
        self.assertLess(repo._ngram_entropy(rep[:900], rep[900:]), repo._ngram_entropy(rnd[:900], rnd[900:]))


class TestTesting(unittest.TestCase):
    def test_square_is_not_a_rectangle(self):
        self.assertIsNone(testing.property_test(lambda: testing.Rectangle(1, 1), testing.rect_property)["failed_after"])
        sq = testing.property_test(lambda: testing.Square(1), testing.rect_property)
        self.assertEqual(sq["shrunk"], (0, 1))

    def test_polluter_found(self):
        self.assertEqual(testing.find_polluter()["found"], "test_polluter")

    def test_flaky_order_dependence(self):
        f = testing.flaky_campaign(runs=60)
        rows = {r["test"]: r for r in f["rows"]}
        self.assertEqual(rows["test_victim"]["isolated_fail_rate"], 0.0)
        self.assertGreater(rows["test_victim"]["fail_rate"], 0.2)

    def test_mutation_tool_kills_on_a_tiny_module(self):
        import sys
        import types
        m = types.ModuleType("tiny_mod")
        src = "def f(x):\n    return x + 1 if x > 0 else 0\n"
        exec(src, m.__dict__)
        sys.modules["tiny_mod"] = m
        import inspect
        inspect.getsource = (lambda orig: (lambda o: src if o is m else orig(o)))(inspect.getsource)
        r = testing.mutation_run("tiny_mod", lambda mod: mod.f(3) == 4 and mod.f(-1) == 0)
        self.assertGreater(r["killed"], 0)
        self.assertLessEqual(r["killed"], r["mutants"])

    def test_fuzz_counts_add_up(self):
        f = testing.fuzz_asm(trials=300)
        self.assertEqual(f["accepted"] + f["rejected"] + f["crashed"], 300)


class TestProcess(unittest.TestCase):
    def test_schedule_keeps_remainder_tasks(self):
        r = process.schedule(tasks=5, median=3, sigma=0, parallel=2, trials=10)
        self.assertEqual(r["plan"], 9)
        self.assertEqual(r["p50"], 9)
        self.assertEqual(r["on_time"], 1)
        self.assertEqual(process.schedule(tasks=2, median=3, sigma=0, parallel=4, trials=10)["p50"], 3)
        with self.assertRaises(ValueError):
            process.schedule(parallel=0)

    def test_brooks_law_condition(self):
        base = process.brooks()
        self.assertLess(process.brooks(add_at=2, add=4), base)
        self.assertGreater(process.brooks(add_at=18, add=4), base)

    def test_schedule_on_time_falls_with_parallel_streams(self):
        a = process.schedule(trials=20000)["on_time"]
        b = process.schedule(trials=20000, parallel=4)["on_time"]
        self.assertLess(b, a)

    def test_littles_law(self):
        k = process.kanban(8, days=1500)
        self.assertAlmostEqual(k["little"], k["cycle_time"], delta=0.15 * k["cycle_time"])

    def test_channels(self):
        self.assertEqual(process.channels(12), 66)


if __name__ == "__main__":
    unittest.main()
