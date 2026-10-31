"""Small exact regressions for Part 2; no production benchmarks or scene loads."""

import ast
import inspect
import re
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

from videos.ai.ai2 import compute, local, logic, sat


def python_function(function):
    return getattr(function, "py_func", function)


class TourBudgetTests(unittest.TestCase):
    def setUp(self):
        self.D = local.dist_matrix(np.array([[0, 0], [10, 0], [12, 7], [8, 12], [0, 10], [-3, 4]], float))
        self.tour = np.array([0, 2, 4, 1, 3, 5], np.int64)

    def instrument(self, function, *args):
        """Count the real score calls and candidate delta lines independently."""
        function = python_function(function)
        source, start = inspect.getsourcelines(function)
        delta = next((start + i for i, line in enumerate(source) if "delta = D[" in line), None)
        events = {"deltas": 0, "full": 0}
        original = python_function(local.tour_len)

        def score(t, d):
            events["full"] += 1
            return original(t, d)

        def trace(frame, event, arg):
            if frame.f_code is function.__code__:
                if event == "line" and frame.f_lineno == delta:
                    events["deltas"] += 1
                return trace
            return None

        previous = sys.gettrace()
        with patch.object(local, "tour_len", score):
            sys.settrace(trace)
            try:
                result = function(*args)
            finally:
                sys.settrace(previous)
        return result, events

    def test_two_opt_never_overruns_and_keeps_best_evaluated_move(self):
        for budget in (1, 2, 4, 9, 10, 25):
            with self.subTest(budget=budget):
                t = self.tour.copy()
                (value, count), events = self.instrument(local.two_opt_climb, t, self.D, budget)
                self.assertEqual(count, events["full"] + events["deltas"])
                self.assertLessEqual(count, budget)
                self.assertEqual(value, local.tour_len(t, self.D))
                self.assertLessEqual(value, local.tour_len(self.tour, self.D))
        # Exhaust the first sweep exactly: its best candidate must be retained.
        t = self.tour.copy()
        value, count = local.two_opt_climb(t, self.D, 10)
        self.assertEqual(count, 10)
        self.assertEqual(value, 58)

    def test_annealing_counts_evaluations_not_no_op_draws(self):
        counts = np.zeros(1, np.int64)
        trace = np.zeros((4, 4))
        (value, tour), events = self.instrument(local.anneal, self.tour.copy(), self.D, 30., .9, 5, 4, 17, 0,
                                                np.zeros((1, 6), np.int64), trace, 13, counts)
        self.assertEqual(counts[0], 13)
        self.assertEqual(counts[0], events["full"] + events["deltas"])
        self.assertEqual(value, local.tour_len(tour, self.D))
        self.assertEqual(trace[-1, 2], value)
        self.assertTrue(np.isfinite(trace).all())

    def test_zero_moves_and_single_initial_evaluation_are_safe(self):
        trace, counts = np.zeros((200, 4)), np.zeros(1, np.int64)
        value, _ = local.anneal(self.tour.copy(), self.D, 30., .9, 0, 200, 17, 0,
                               np.zeros((1, 6), np.int64), trace, 1, counts)
        self.assertEqual(counts[0], 1)
        self.assertEqual(value, 71)
        self.assertTrue(np.isfinite(trace).all())

    def test_ga_charges_initialization_and_final_trace_includes_result(self):
        for budget in (1, 2, 4, 5, 8, 11):
            with self.subTest(budget=budget):
                best, counts = np.zeros(5, np.int64), np.zeros(1, np.int64)
                value, events = self.instrument(local.genetic, self.D, 4, 4, .5, 1, best,
                                                np.zeros((1, 6), np.int64), np.array([-1], np.int64), budget, counts)
                self.assertEqual(counts[0], events["full"])
                self.assertEqual(counts[0], budget)
                self.assertEqual(best[-1], value)
                self.assertTrue(np.all(np.diff(best) <= 0))

    def test_numba_execution_matches_python_budget_and_result(self):
        # These really compile the production kernels when JIT is enabled.
        for budget in (1, 10, 23):
            t, u = self.tour.copy(), self.tour.copy()
            self.assertEqual(local.two_opt_climb(t, self.D, budget),
                             python_function(local.two_opt_climb)(u, self.D, budget))
            np.testing.assert_array_equal(t, u)
        args = (self.tour.copy(), self.D, 30., .9, 5, 4, 17, 0, np.zeros((1, 6), np.int64), np.zeros((4, 4)))
        counts = np.zeros(1, np.int64)
        value, tour = local.anneal(*args, 13, counts)
        self.assertEqual(counts[0], 13)
        self.assertEqual(value, local.tour_len(tour, self.D))
        trace, counts = np.zeros(4, np.int64), np.zeros(1, np.int64)
        value = local.genetic(self.D, 4, 3, .5, 1, trace, np.zeros((1, 6), np.int64),
                              np.array([-1], np.int64), 8, counts)
        self.assertEqual(counts[0], 8)
        self.assertEqual(trace[-1], value)


class ResolutionTests(unittest.TestCase):
    def test_factoring_required_unsatisfiable_clauses_refute(self):
        kb = [frozenset({logic.lit(s, "P", "x"), logic.lit(s, "P", "y")}) for s in (True, False)]
        result = logic.refute(kb, [], max_clauses=64)
        self.assertTrue(result["found"])
        self.assertTrue(any(c.get("rule") == "factor" for c in result["clauses"]))
        self.assertEqual(result["clauses"][result["proof"][-1]]["text"], "□")
        for i in result["proof"]:
            record = result["clauses"][i]
            for parent in record["parents"] or []:
                self.assertLess(parent, i)

    def test_initial_empty_clause_refutes_for_both_input_locations(self):
        for kb, goal in (([frozenset()], []), ([], [frozenset()])):
            result = logic.refute(kb, goal, strategy="support")
            self.assertTrue(result["found"])
            self.assertEqual(result["levels"], 0)
            self.assertEqual(result["proof"], [0])

    def test_factor_must_unify_same_sign_literals_and_respect_occurs_check(self):
        for clause in (frozenset({logic.lit(True, "P", "A"), logic.lit(False, "P", "x")}),
                       frozenset({logic.lit(True, "P", "x"), logic.lit(True, "P", ("f", ("x",)))})):
            self.assertEqual(logic.factors(clause), [])

    def test_satisfiable_saturation_and_resource_limit_are_not_refutations(self):
        unit = frozenset({logic.lit(True, "P", "A")})
        result = logic.refute([unit], [])
        self.assertFalse(result["found"])
        self.assertEqual(result["status"], "saturated")
        result = logic.refute([unit], [], max_clauses=1)
        self.assertFalse(result["found"])
        self.assertEqual(result["status"], "limit")

    def test_new_support_revisits_previously_skipped_pairs(self):
        # Q versus not-Q is skipped before a later goal-derived Q promotes it.
        q, p = logic.lit(True, "Q"), logic.lit(True, "P")
        result = logic.refute([frozenset({q}), frozenset({logic.lit(False, "Q")}),
                               frozenset({logic.lit(False, "P"), q})],
                              [frozenset({p})], strategy="support")
        self.assertTrue(result["found"])

    def test_pending_factor_inherits_support_from_duplicate_derivation(self):
        c = frozenset({logic.lit(True, "P", "x"), logic.lit(True, "P", "y")})
        result = logic.refute([c], [c], strategy="support", max_clauses=20)
        factors = [r for r in result["clauses"] if r.get("rule") == "factor"]
        self.assertEqual(len(factors), 1)
        self.assertTrue(factors[0]["goal"])

    def test_unary_factoring_proof_has_valid_scene_layout(self):
        from manim import Square
        from videos.ai.ai2 import s09_logic

        kb = [frozenset({logic.lit(s, "P", "x"), logic.lit(s, "P", "y")}) for s in (True, False)]
        result = logic.refute(kb, [], max_clauses=64)
        # Exercise layout geometry without LaTeX, rendering, or loading any data.
        with patch.object(s09_logic, "clause_box", side_effect=lambda *a, **kw: Square(.5)):
            boxes, row = s09_logic.proof_layout(result["clauses"], result["proof"])
        self.assertEqual(set(boxes), set(result["proof"]))
        for i in result["proof"]:
            for parent in result["clauses"][i]["parents"] or []:
                self.assertGreater(row[i], row[parent])

    def test_self_resolution_standardizes_variables_apart(self):
        c = frozenset({logic.lit(True, "P", "x"), logic.lit(False, "P", ("f", ("x",)))})
        derived = logic.resolvents(c, c, 0)
        self.assertTrue(any("f(f(" in logic.show_clause(r) for r, _ in derived))

    def test_existing_first_order_unit_resolution(self):
        result = logic.refute([frozenset({logic.lit(True, "P", "x")})],
                              [frozenset({logic.lit(False, "P", "A")})], strategy="support")
        self.assertTrue(result["found"])


class SatCensoringTests(unittest.TestCase):
    def test_actual_solver_has_distinct_sat_unsat_unknown_statuses(self):
        single = np.array([[1, 2, 3]], np.int64)
        all_signs = np.array([[a, b, c] for a in (1, -1) for b in (2, -2) for c in (3, -3)], np.int64)
        self.assertEqual(sat.solve_dpll(single, 3)[0], 1)
        self.assertEqual(sat.solve_dpll(all_signs, 3)[0], 0)
        self.assertEqual(sat.solve_dpll(single, 3, max_decisions=0)[0], -1)

    def test_unknowns_bound_probability_and_do_not_enter_completion_median(self):
        result = compute.summarize_sat_runs([1, 0, -1], [2, 4, 100])
        self.assertAlmostEqual(result["psat"], 1/3)
        self.assertAlmostEqual(result["psat_upper"], 2/3)
        self.assertEqual(result["unknown"], 1)
        self.assertEqual(result["median"], 3)
        self.assertEqual(result["observed_median"], 4)
        self.assertEqual(result["resolved_psat"], .5)

    def test_all_unknowns_do_not_invent_completed_work(self):
        result = compute.summarize_sat_runs([-1, -1], [100, 100])
        self.assertEqual((result["psat"], result["psat_upper"]), (0, 1))
        for key in ("median", "mean", "q90", "resolved_psat"):
            self.assertIsNone(result[key])

    def test_missing_crossing_does_not_wrap_to_last_interval(self):
        self.assertIsNone(compute.sat_crossing([3, 4, 5], [.9, .8, .7], .5))
        self.assertIsNone(compute.sat_crossing([3, 4, 5], [.3, .2, .1], .5))
        self.assertEqual(compute.sat_crossing([3, 4, 5], [.9, .5, .1], .5), 4)
        self.assertEqual(compute.sat_crossing([3, 4, 5], [.9, .5, .1], .1), 5)

    def test_censored_sweep_does_not_fit_crossing_width_or_peak(self):
        class Pieces(dict):
            def finish(self):
                pass
        with patch.object(compute, "Partial", return_value=Pieces()), \
                patch.object(sat, "solve_dpll", side_effect=[(1, 1), (0, 2), (-1, 100)] * 3):
            result = compute.compute_sat3(ns=(3,), alphas=(1., 2., 3.), per=(3,))
        self.assertEqual(result["unknown_3"], [1, 1, 1])
        self.assertEqual(result["runs_3"][0]["statuses"], [1, 0, -1])
        self.assertEqual(result["max_decisions"], 10**9)
        self.assertEqual(result["median_3"], [1.5] * 3)
        self.assertTrue(result["censored_3"])
        for key in ("cross_3", "width_3", "peak_3"):
            self.assertIsNone(result[key])


class NarrationTranslationTests(unittest.TestCase):
    def setUp(self):
        from explainer.zh_templates import Translator, sources
        self.translate = Translator("ai2")
        self.sources = sources("ai2")

    def spoken(self, needle, values=None):
        row = next(r for r in self.sources if needle in r.get("en", r.get("tpl", "")))
        if "en" in row:
            return row["en"]
        return eval(compile(ast.parse(row["tpl"], mode="eval"), "actual-ai2-narration", "eval"),
                    {"__builtins__": {"__import__": __import__}}, values or {})

    def check_translation(self, english):
        result = self.translate(english)
        self.assertIsNotNone(result)
        self.assertRegex(result, r"[\u4e00-\u9fff]")
        self.assertNotIn("{", result)
        self.assertEqual(re.findall(r"<bookmark[^>]+/>", english), re.findall(r"<bookmark[^>]+/>", result))
        return result

    def test_dominance_qualifications_survive_translation(self):
        english = self.spoken("How much does the better", {"dd": 24,
                              "last": {"astar_h0": 10000, "astar_h1": 5000, "astar_h2": 1000},
                              "ebf": {"astar_h0": 1.5, "astar_h1": 1.3, "astar_h2": 1.1}})
        translated = self.check_translation(english)
        self.assertIn("一致", translated)
        self.assertIn("边界", translated)
        self.assertNotIn("绝不会更多", translated)

    def test_actual_tsp_comparison_recursively_translates_its_verdict(self):
        values = {"d": {"budget": 2000000, "nn_lengths": [9000], "nn2opt_lengths": [8000]}, "opt": 7542,
                  "order": [("annealing", 7800), ("restarted hill climbing", 7900), ("the genetic algorithm", 9500)],
                  "min": min}
        values["verdict"] = self.spoken("On the same budget", values)
        values["hits"] = "Annealing never found the optimum itself."
        translated = self.check_translation(self.spoken("Is the cooling", values))
        self.assertIn("初始化", translated)
        self.assertIn("不代表相同CPU时间", translated)
        self.assertNotIn("candidate-cost", translated)
        self.assertNotIn("looked at", translated)

    def test_factoring_and_resource_cap_survive_translation(self):
        translated = self.check_translation(self.spoken("In 1965 Alan Robinson"))
        self.assertIn("因子化", translated)
        self.assertIn("资源上限", translated)

    def test_both_censored_and_missing_window_verdicts_translate(self):
        for needle in ("Some runs reached", "The sampled ratios do not bracket"):
            self.check_translation(self.spoken(needle))

    def test_hardness_main_recursively_translates_both_result_branches(self):
        results = [self.spoken("Some runs are truncated"), self.spoken("For {n1} variables, the median peaks",
                   {"n1": 200, "pk": 4.2, "med": np.array([1, 20000, 3]), "lo_side": 1, "hi_side": 3})]
        for result in results:
            self.check_translation(self.spoken("The transition is also where", {"result": result}))


class ResolutionStoppingReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The actual default family example is small (~3s) and writes no cache.
        cls.result = compute.compute_resolution()

    def actual_outcomes(self, sat_record, sos_record):
        """Execute the actual scene's branches, without its rendering/data loads."""
        path = Path(__file__).resolve().parents[1] / "videos/ai/ai2/s09_logic.py"
        tree = ast.parse(path.read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Logic")
        fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "explosion")
        branches = [n for n in fn.body if isinstance(n, ast.If) and any(
            isinstance(a, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("sat_verdict", "sos_verdict")
                                             for t in a.targets) for a in ast.walk(n))]
        self.assertEqual(len(branches), 2)
        values = {"sat": sat_record, "sos": sos_record}
        exec(compile(ast.Module(body=branches, type_ignores=[]), str(path), "exec"),
             {"__builtins__": {}}, values)
        return values

    def test_default_capped_run_is_recorded_without_claiming_a_proof(self):
        from videos.ai.ai2.s09_logic import resolution_outcome_label

        sat = self.result["explode_saturate"]
        support = self.result["explode_support"]
        self.assertEqual(self.result["schema_version"], 3)
        self.assertFalse(sat["found"])
        self.assertEqual(sat["status"], "limit")
        self.assertEqual(sat["made"], sat["clause_cap"])
        self.assertEqual(sat["proof_len"], 0)
        self.assertTrue(support["found"])
        self.assertEqual(support["status"], "refuted")
        self.assertGreater(support["proof_len"], 0)
        capped = self.actual_outcomes(sat, support)["sat_verdict"]
        self.assertIn("without finding a refutation", capped)
        self.assertIn("unresolved", capped)
        self.assertNotIn("before finding", capped)
        self.assertNotIn("found a refutation after", capped)
        self.assertIn("cap reached; no proof", resolution_outcome_label(sat, "all pairs"))

    def test_all_stopping_branches_and_main_narration_translate(self):
        from explainer.zh_templates import Translator, sources

        translate = Translator("ai2")
        sat, support = self.result["explode_saturate"], self.result["explode_support"]
        cases = [sat, support, dict(sat, status="saturated", made=12)]
        for record in cases:
            outcomes = self.actual_outcomes(record, record)
            for branch in ("sat_verdict", "sos_verdict"):
                english = outcomes[branch]
                chinese = translate(english)
                self.assertIsNotNone(chinese)
                self.assertNotIn("{", chinese)
                self.assertNotIn("level-by-level", chinese)
                self.assertNotIn("set-of-support", chinese)
                if not record["found"]:
                    self.assertIn("未找到反驳证明", chinese)
        source = next(r["tpl"] for r in sources("ai2") if "Completeness is not efficiency." in r.get("tpl", ""))
        spoken = eval(compile(ast.parse(source, mode="eval"), "actual-ai2-explosion", "eval"),
                      {"__builtins__": {}}, self.actual_outcomes(sat, support))
        chinese = translate(spoken)
        self.assertIsNotNone(chinese)
        self.assertEqual(re.findall(r"<bookmark[^>]+/>", spoken), re.findall(r"<bookmark[^>]+/>", chinese))
        self.assertIn("达到记录4000个子句的上限", chinese)
        self.assertIn("证明用到", chinese)
        self.assertNotIn("{", chinese)


class CacheRevisionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.cache = compute.SchemaCache("ai2")
        self.cache.dir = Path(temp.name)
        self.current = {"schema_version": compute.CACHE_SCHEMAS["resolution"],
                        "prop": {"status": "refuted"}, "fol": {"status": "refuted"},
                        "explode_saturate": {"status": "limit", "clause_cap": 4000},
                        "explode_support": {"status": "refuted", "clause_cap": 4000}}
        self.calculate = Mock(return_value=self.current)
        self.cache.items = {"resolution": self.calculate}
        self.cache.save("resolution", {"prop": {}, "fol": {}})

    def test_normal_load_replaces_legacy_cache(self):
        self.assertFalse(self.cache.current("resolution"))
        self.assertEqual(self.cache.load("resolution"), self.current)
        self.calculate.assert_called_once_with()
        self.assertTrue(self.cache.current("resolution"))

    def test_cli_does_not_skip_legacy_cache(self):
        with patch.object(sys, "argv", ["compute.py", "resolution"]):
            self.cache.main(self.cache.items)
        self.calculate.assert_called_once_with()
        self.assertTrue(self.cache.current("resolution"))

    def test_current_cache_is_reused(self):
        self.cache.save("resolution", self.current)
        self.assertEqual(self.cache.load("resolution"), self.current)
        self.calculate.assert_not_called()

    def test_cached_only_rejects_real_legacy_marker_without_computing(self):
        from tools.qa_series import StaleDataError, require_current_cache

        before = self.cache.path("resolution").read_bytes()
        with patch.object(compute, "CACHE", self.cache):
            with self.assertRaisesRegex(StaleDataError, "ai2/resolution"):
                require_current_cache(compute, "ai2", self.cache.path("resolution"), "resolution")
        self.calculate.assert_not_called()
        self.assertEqual(self.cache.path("resolution").read_bytes(), before)

    def test_resolution_v2_marker_without_stopping_metadata_is_stale(self):
        legacy = {"schema_version": 2, "prop": {"status": "refuted"}, "fol": {"status": "refuted"},
                  "explode_saturate": {"found": False, "made": 4000, "levels": 3, "proof_len": 0},
                  "explode_support": {"found": True, "made": 2823, "levels": 8, "proof_len": 15}}
        self.cache.save("resolution", legacy)
        self.assertFalse(self.cache.current("resolution"))
        self.assertEqual(self.cache.load("resolution"), self.current)
        self.calculate.assert_called_once_with()

    def test_old_partial_parameters_are_incompatible(self):
        self.cache.partial("sat3", {"ns": [3]})["3/1"] = {"psat": 0}
        new = self.cache.partial("sat3", {"ns": [3], "schema_version": compute.CACHE_SCHEMAS["sat3"]})
        self.assertNotIn("3/1", new)
