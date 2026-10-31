"""Part4 tail mathematics and outcome guards; no scene imports or data loads."""

import ast
import math
import unittest
from pathlib import Path


PART = Path(__file__).resolve().parents[1] / "videos/ai/ai4"


def helpers(filename, names):
    tree = ast.parse((PART / filename).read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    env = {"math": math}
    exec(compile(ast.Module(nodes, type_ignores=[]), filename, "exec"), env)
    return env


class QuadraticOutcomeTests(unittest.TestCase):
    def test_rate_mismatch_and_unavailable_are_not_called_close(self):
        f = helpers("s15_quadratic.py", ["rate_comparison"])["rate_comparison"]
        self.assertIn("within one millionth", f(1e-8))
        self.assertIn("0.500000", f(.5))
        self.assertNotIn("match", f(.5))
        self.assertIn("unavailable", f(float("nan")))

    def test_escape_fit_distinguishes_both_mismatch_directions(self):
        f = helpers("s15_quadratic.py", ["escape_comparison"])["escape_comparison"]
        self.assertIn("within ten percent", f(24.5, 24.))
        self.assertIn("larger", f(100., 24.))
        self.assertIn("smaller", f(1., 24.))
        self.assertIn("too few resolved", f(float("nan"), 24.))

    def test_capped_and_unknown_counts_are_not_converged(self):
        f = helpers("s15_quadratic.py", ["threshold_summary"])["threshold_summary"]
        record = dict(status="converged", first_hit_step=7, iterations=7, cap=10)
        self.assertIn("after 7 updates", f(record))
        record.update(status="capped", first_hit_step=None, iterations=10)
        self.assertIn("not reached", f(record))
        record.update(status="unknown")
        self.assertIn("unresolved", f(record))
        self.assertNotIn("after", f(record))

    def test_norm_and_objective_factors_are_different(self):
        # For the extremal SPD eigenvector at the optimal step, norm contracts
        # by q and the quadratic by q squared, not the same factor.
        kappa = 9.
        eta = 2 / (1 + kappa)
        q = (kappa - 1) / (kappa + 1)
        self.assertAlmostEqual(abs(1 - eta), q)
        self.assertAlmostEqual(.5 * (1 - eta) ** 2 / .5, q * q)
        strings = [n.value for n in ast.walk(ast.parse((PART / "s15_quadratic.py").read_text()))
                   if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertTrue(any("objective contracts by at most $q^2$" in s for s in strings))


class ConstraintTests(unittest.TestCase):
    def test_free_intercept_constraint_excludes_unbounded_incomplete_dual(self):
        # x=(1,2), y=(-1,+1): primal w=2,b=-3 gives both margins one
        # and objective2. alpha=(2t,t) has w_alpha=0 and dual3t, but
        # violates the intercept stationarity sum(alpha*y)=0.
        self.assertEqual((-1 * (2 * 1 - 3), 2 * 2 - 3), (1, 1))
        self.assertEqual(.5 * 2**2, 2)
        for t in (1., 10., 100.):
            alpha = (2 * t, t)
            w_alpha = -alpha[0] + 2 * alpha[1]
            self.assertEqual(sum(alpha) - .5 * w_alpha**2, 3 * t)
            self.assertNotEqual(-alpha[0] + alpha[1], 0)
        strings = [n.value for n in ast.walk(ast.parse((PART / "s17_kkt.py").read_text()))
                   if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertTrue(any(r"\sum_i\alpha_i y_i=0" in s for s in strings))

    def test_degenerate_margin_can_have_zero_multiplier(self):
        # Duplicate positive point: all margins active, valid alpha=(2,2,0).
        xs, ys, alpha = (1., 2., 2.), (-1., 1., 1.), (2., 2., 0.)
        margins = [y * (2 * x - 3) for x, y in zip(xs, ys)]
        self.assertEqual(margins, [1., 1., 1.])
        self.assertEqual(sum(a * y for a, y in zip(alpha, ys)), 0)
        self.assertEqual(sum(a * y * x for a, y, x in zip(alpha, ys, xs)), 2)
        self.assertEqual(sum(a > 0 for a in alpha), 2)
        self.assertEqual(sum(m == 1 for m in margins), 3)
        self.assertEqual([a * (m - 1) for a, m in zip(alpha, margins)], [0., 0., 0.])

    def test_solver_failure_and_large_residual_never_pass_as_optimal(self):
        f = helpers("s17_kkt.py", ["svm_checks_pass", "svm_solver_verdict"])
        d = {"solvers": {k: {"success": True} for k in ("primal", "dual")},
             "tolerances": dict(feasibility=1e-6, stationarity=1e-4, complementarity=1e-6),
             "residuals": {k: 1e-10 for k in ("primal_feasibility", "dual_nonnegative", "dual_equality",
                                             "duality_gap", "stationarity_w", "stationarity_b", "complementarity")}}
        self.assertTrue(f["svm_checks_pass"](d))
        d["solvers"]["dual"]["success"] = False
        self.assertFalse(f["svm_checks_pass"](d))
        self.assertIn("not certified", f["svm_solver_verdict"](d))
        d["solvers"]["dual"]["success"] = True
        d["residuals"]["dual_equality"] = .01
        self.assertFalse(f["svm_checks_pass"](d))
        d["residuals"]["dual_equality"] = float("nan")
        self.assertFalse(f["svm_checks_pass"](d))

    def test_separator_handles_vertical_horizontal_and_missing_intersection(self):
        f = helpers("s17_kkt.py", ["clipped_separator"])["clipped_separator"]
        box = (-2., 2., -3., 3.)
        for w, b, level in [((1., 0.), 0., 1.), ((0., 1.), 0., 2.), ((1., 2.), -.4, .7)]:
            points = f(w, b, level, box)
            self.assertEqual(len(points), 2)
            for x, y in points:
                self.assertAlmostEqual(w[0] * x + w[1] * y + b, level)
                self.assertTrue(box[0] <= x <= box[1] and box[2] <= y <= box[3])
        self.assertIsNone(f((1., 0.), 0., 5., box))
        self.assertIsNone(f((0., 0.), 0., 1., box))

    def test_nonconvex_domain_must_include_values_below_old_display_floor(self):
        # An admissible x for the Lagrangian infimum proves q(6)<=-6.1875.
        x, mu = 1.5, 6.
        value = x**4 - 3 * x**2 + x + mu * (.5 - x)
        self.assertEqual(value, -6.1875)
        method = next(n for n in ast.walk(ast.parse((PART / "s17_kkt.py").read_text()))
                      if isinstance(n, ast.FunctionDef) and n.name == "pictures")
        self.assertNotIn("np.clip", ast.unparse(method))

    def test_entropy_and_kl_conventions_and_solver_status(self):
        f = helpers("s16_lagrange.py", ["solver_agreement"])["solver_agreement"]
        self.assertIn("not report success", f(False, 1e-12, 1e-4))
        self.assertIn("agrees within", f(True, 1e-8, 1e-4))
        self.assertIn("outside", f(True, .2, 1e-4))
        self.assertIn("unavailable", f(True, float("nan"), 1e-4))
        source = (PART / "s16_lagrange.py").read_text()
        self.assertIn(r"\beta = 1/T", source)
        self.assertIn("not inverse temperature", source)
        # A positive KL penalty is a temperature: raising beta flattens the
        # reward-induced odds, unlike multiplying scores by inverse temperature.
        odds = lambda beta: math.exp((2. - 0.) / beta)
        self.assertGreater(odds(.5), odds(1.))


class ImplicitOutcomeTests(unittest.TestCase):
    def test_faster_slower_and_missing_gradient_rates(self):
        f = helpers("s18_implicit.py", ["gradient_rate_comparison"])["gradient_rate_comparison"]
        self.assertIn("faster", f(.1, .9))
        self.assertIn("slower", f(.9, .1))
        self.assertIn("within 0.15", f(.45, .4))
        self.assertIn("unavailable", f(float("nan"), .4))

    def test_fixed_point_cap_and_comparison_floor_are_not_accuracy_certificates(self):
        env = helpers("s18_implicit.py", ["fixed_point_summary", "comparison_floor", "loss_comparison"])
        record = dict(status="capped", iterations=2, cap=2, residual=.4)
        self.assertIn("hit its cap", env["fixed_point_summary"](record))
        record["status"] = "nonfinite"
        self.assertIn("unavailable", env["fixed_point_summary"](record))
        record["status"] = "converged"
        self.assertIn("met its residual tolerance", env["fixed_point_summary"](record))
        self.assertIn("numerically zero", env["comparison_floor"]([0., 1e-12]))
        self.assertIn("unavailable", env["comparison_floor"]([float("nan")]))
        self.assertIn("higher", env["loss_comparison"](.1, .2))
        self.assertIn("lower", env["loss_comparison"](.2, .1))
        self.assertIn("equal", env["loss_comparison"](.1, .1))


if __name__ == "__main__":
    unittest.main()
