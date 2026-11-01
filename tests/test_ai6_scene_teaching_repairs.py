"""Bounded fixtures from actual Part6 consumers, without scenes or data producers."""
import ast
import math
from pathlib import Path
import re
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1] / "videos/ai/ai6"


def tree(module):
    return ast.parse((ROOT / module).read_text())


def method(module, name):
    return next(n for n in ast.walk(tree(module)) if isinstance(n, ast.FunctionDef) and n.name == name)


def execute(nodes, **scope):
    scope = dict(np=np, math=math, **scope)
    exec(compile(ast.Module(nodes, type_ignores=[]), "actual-ai6-consumer-fixture", "exec"), scope)
    return scope


def assigned(node, name):
    return isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)


class WhiteningGeometry(unittest.TestCase):
    @staticmethod
    def geometry(covariance, means):
        node = next(n for n in tree("s09_lda.py").body
                    if isinstance(n, ast.FunctionDef) and n.name == "whitening_geometry")
        return execute([node])["whitening_geometry"](covariance, means)

    def test_diagonal_whitening_and_normal_pullback_are_distinct_operations(self):
        covariance = np.diag([4., 1.])
        delta = np.array([2., 1.])
        g = self.geometry(covariance, [np.zeros(2), delta])
        np.testing.assert_allclose(g["W"], np.diag([.5, 1.]))
        np.testing.assert_allclose(g["W"] @ covariance @ g["W"].T, np.eye(2))
        np.testing.assert_allclose(g["normal"], np.linalg.solve(covariance, delta))
        self.assertFalse(np.allclose(g["normal"], g["delta_z"]))
        inverse = np.linalg.inv(covariance)
        self.assertFalse(np.allclose(inverse @ covariance @ inverse.T, np.eye(2)))

    def test_rotated_covariance_uses_same_affine_map_for_contours_and_means(self):
        angle = .37
        rotation = np.array([[math.cos(angle), -math.sin(angle)],
                             [math.sin(angle), math.cos(angle)]])
        covariance = rotation @ np.diag([.3, 2.7]) @ rotation.T
        means = np.array([[3., -2.], [4.2, -.7]])
        g = self.geometry(covariance, means)
        np.testing.assert_allclose(g["after"], g["before"] @ g["W"].T)
        np.testing.assert_allclose(g["W"] @ covariance @ g["W"].T, np.eye(2), atol=1e-14)
        whitened_centres = g["centres"] @ g["W"].T
        for contour, centre in zip(g["after"], whitened_centres):
            np.testing.assert_allclose(np.linalg.norm(contour - centre, axis=1), 1., atol=1e-14)
        np.testing.assert_allclose(g["normal"], np.linalg.solve(covariance, means[1] - means[0]), atol=1e-14)
        translated = self.geometry(covariance, means + [18., -9.])
        np.testing.assert_allclose(translated["before"], g["before"], atol=1e-14)
        np.testing.assert_allclose(translated["normal"], g["normal"], atol=1e-14)

    def test_rejects_undefined_whitening_instead_of_fabricating_round_clouds(self):
        means = [[0., 0.], [1., 1.]]
        for covariance in [np.zeros((2, 2)), np.diag([-1., 1.]), [[1., .3], [0., 1.]],
                           [[np.nan, 0.], [0., 1.]], np.eye(3)]:
            with self.subTest(covariance=covariance), self.assertRaises(ValueError):
                self.geometry(covariance, means)
        with self.assertRaises(ValueError):
            self.geometry(np.eye(2), [[1., 1.], [1., 1.]])

    def test_eigen_implication_conditions_the_vector_not_just_positive_maximum(self):
        rows = next(n.value for n in method("s09_lda.py", "eigen").body if assigned(n, "rows"))
        antecedent = ast.literal_eval(rows.elts[1].args[0])
        self.assertIn(r"\mathbf{w}\in\operatorname{argmax}", antecedent)
        scatter = np.eye(2)
        between = np.diag([1., 0.])
        maximum = 1.
        stationary_minimum = np.array([0., 1.])
        # Positive max J does not make an arbitrary stationary vector a maximizer.
        self.assertEqual(stationary_minimum @ between @ stationary_minimum, 0.)
        self.assertFalse(np.allclose(between @ stationary_minimum,
                                     maximum * scatter @ stationary_minimum))
        for maximizer in [np.array([1., 0.]), np.array([-3., 0.])]:
            quotient = (maximizer @ between @ maximizer) / (maximizer @ scatter @ maximizer)
            self.assertEqual(quotient, maximum)
            np.testing.assert_allclose(between @ maximizer, maximum * scatter @ maximizer)


class ConsumerGeometryAndOutcomes(unittest.TestCase):
    def test_actual_svm_curves_retain_true_losses_and_exponential_boundary(self):
        names = {"m", "hingec", "logc", "exp_m", "expc"}
        nodes = [n for n in method("s12_svm.py", "hinge").body
                 if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
        calls = []
        def curve(ax, xs, ys, *args, **kwargs):
            calls.append((np.asarray(xs), np.asarray(ys)))
            return object()
        execute(nodes, ax=None, curve=curve, GOLD="gold", C=type("Colors", (), {"TRUE_P": "blue"}))
        m, hinge = calls[0]
        np.testing.assert_allclose(hinge, np.maximum(0, 1 - m))
        self.assertAlmostEqual(hinge[0], 3.5)
        np.testing.assert_allclose(np.diff(hinge[m < 0]), -np.diff(m[m < 0]))
        np.testing.assert_allclose(calls[1][1], np.log2(1 + np.exp(-m)))
        self.assertGreater(calls[1][1][0], 3.2)
        ex, ey = calls[2]
        self.assertAlmostEqual(ex[0], -math.log(4))
        self.assertAlmostEqual(ey[0], 4.)
        np.testing.assert_allclose(ey, np.exp(-ex))
        self.assertTrue(np.all(ey <= 4. + 1e-14))

    def test_contest_distinguishes_higher_equal_lower_and_nonfinite(self):
        node = next(n for n in method("s18_contest.py", "board").body
                    if isinstance(n, ast.If) and any(assigned(x, "line_s") for x in ast.walk(n)))
        for left, right, phrase in [(.81, .8, "higher"), (.8, .8, "tie"), (.79, .8, "Boosted trees score higher"),
                                    (np.nan, .8, "unavailable"), (.8, np.inf, "unavailable")]:
            with self.subTest(left=left, right=right):
                self.assertIn(phrase, execute([node], lr70=left, xgb70=right)["line_s"])

    def test_logistic_narrates_legitimate_tied_and_weaker_feature_results(self):
        node = next(n for n in method("s06_logistic.py", "result").body
                    if isinstance(n, ast.If) and any(assigned(x, "comparison") for x in ast.walk(n)))
        for acc70, phrase in [(.9, "higher"), (.8, "tie"), (.7, "lower")]:
            self.assertIn(phrase, execute([node], lg={"acc70": acc70, "acc2": .8})["comparison"])

    def test_adaboost_never_zero_and_reached_zero_are_different_observations(self):
        body = method("s15_adaboost.py", "curves").body
        nodes = [n for n in body if any(assigned(n, k) for k in ["z0", "te_z", "best", "keeps"])]
        nodes += [next(n for n in body if isinstance(n, ast.If) and any(assigned(x, "say") for x in ast.walk(n)))]
        never = execute(nodes, tr=np.array([.3, .2, .1]), te=np.array([.25, .2, .3]), n=3)["say"]
        self.assertIn("never reaches zero", never)
        self.assertNotIn("None", never)
        improved = execute(nodes, tr=np.array([.1, 0., 0.]), te=np.array([.2, .2, .1]), n=3)["say"]
        self.assertIn("hits zero at round 2", improved)
        self.assertIn("lowest observed held-out error", improved)
        self.assertIn("final value after 3 rounds is 10.0 percent", improved)
        nonmonotone = execute(nodes, tr=np.array([.1, 0., 0., 0.]), te=np.array([.2, .2, .1, .15]), n=4)["say"]
        self.assertIn("10.0 percent at round 3", nonmonotone)
        self.assertIn("final value after 4 rounds is 15.0 percent", nonmonotone)
        self.assertNotIn("keeps falling", nonmonotone)
        unchanged = execute(nodes, tr=np.array([0., 0., 0.]), te=np.array([.1, .2, .2]), n=3)["say"]
        self.assertIn("more rounds don't improve it", unchanged)

    def test_stable_unbounded_logloss_values_fit_the_actual_display_range(self):
        body = method("s17_metrics.py", "scores").body
        nodes = [n for n in body if assigned(n, "loss_top") or assigned(n, "lls")]
        recorded = []
        def hbars(rows, **kwargs):
            recorded.append((rows, kwargs))
        specs = [("small", "small", "blue"), ("extreme", "extreme", "pink")]
        execute(nodes, c={"small": {"logloss": .2}, "extreme": {"logloss": 1000.}}, specs=specs, hbars=hbars)
        rows, options = recorded[0]
        self.assertEqual(rows[1][1], 1000.)
        self.assertGreater(options["hi"], 1000.)


class LocalChineseNarration(unittest.TestCase):
    @staticmethod
    def contest_spoken(rows):
        """Evaluate the actual scalar verdict/VO nodes, never the scene or loader."""
        source = tree("s18_contest.py")
        helper = next(n for n in source.body
                      if isinstance(n, ast.FunctionDef) and n.name == "board_leaders")
        board = method("s18_contest.py", "board")
        names = {"a2", "lo2", "hi2", "leaders70", "winner_s", "best70", "best_mean",
                 "tree70", "xgb70", "lr70", "line_s"}
        nodes = [helper]
        for node in board.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                targets = target.elts if isinstance(target, ast.Tuple) else [target]
                if all(isinstance(t, ast.Name) and t.id in names for t in targets):
                    nodes.append(node)
            elif (isinstance(node, ast.If)
                  and any(assigned(n, "winner_s") or assigned(n, "line_s") for n in ast.walk(node))):
                nodes.append(node)
        scope = execute(nodes, rows=rows)
        argument = next(n.args[0] for n in ast.walk(board)
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                        and n.func.attr == "voiceover")
        english = eval(compile(ast.Expression(argument), "actual-contest-voiceover", "eval"), scope)
        return english, [r["key"] for r in scope["leaders70"]]

    @staticmethod
    def contest_rows(lr=.9953365384615385, svm=.9953365384615385, lasso=.993798076923077):
        return [{"key": key, "name": name, "2": {"cv": .8}, "70": {"cv": score}}
                for key, name, score in [
                    ("lr", "logistic regression", lr),
                    ("svm_rbf", "Gaussian-kernel SVM", svm),
                    ("lasso", "lasso", lasso),
                    ("tree", "one tree (depth 4)", .9297077228327228),
                    ("xgb", "gradient boosting (100)", .9827621336996337),
                ]]

    def translated_contest(self, rows):
        from explainer.zh_templates import Translator
        english, leaders = self.contest_spoken(rows)
        # Load the real complete module: a later ZH.update must not resurrect the
        # old single-winner template after an earlier dictionary was repaired.
        chinese = Translator("ai6")(english)
        self.assertIsNotNone(chinese)
        self.assertNotRegex(chinese, r"\{[^{}]+\}")
        bookmarks = lambda s: re.findall(r"<bookmark mark=['\"]([^'\"]+)['\"]/>", s)
        self.assertEqual(bookmarks(english), ["a", "b", "c"])
        self.assertEqual(bookmarks(chinese), bookmarks(english))
        return english, chinese, leaders

    def test_actual_contest_two_way_top_tie_survives_late_translation_updates(self):
        english, chinese, leaders = self.translated_contest(self.contest_rows())
        self.assertEqual(leaders, ["lr", "svm_rbf"])
        self.assertIn("2 procedures tie", english)
        self.assertIn("2种流程并列", chinese)
        self.assertIn("99.5%", chinese)
        self.assertNotIn("最高的是逻辑回归", chinese)

    def test_actual_contest_unique_mean_is_not_tied_by_display_rounding(self):
        _, chinese, leaders = self.translated_contest(self.contest_rows(lr=.99536, svm=.99534))
        self.assertEqual(leaders, ["lr"])
        self.assertIn("逻辑回归", chinese)
        self.assertIn("99.5%", chinese)
        self.assertNotIn("并列", chinese)

    def test_actual_contest_three_way_top_tie_retains_every_leader_and_count(self):
        _, chinese, leaders = self.translated_contest(self.contest_rows(lasso=.9953365384615385))
        self.assertEqual(leaders, ["lr", "svm_rbf", "lasso"])
        self.assertIn("3种流程并列", chinese)
        self.assertIn("99.5%", chinese)

    def test_new_outcome_sentences_translate_without_reversing_the_observation(self):
        from explainer.zh_templates import Translator
        tr = Translator("ai6")
        for english, chinese in [
            ("Logistic regression and boosted trees tie on mean accuracy in these folds.", "打平"),
            ("Boosted trees score higher than logistic regression in these folds.", "提升树得分高于"),
            ("Here the seventy-rate model scores lower than the two-rate model; more features need not help.", "得分更低"),
            ("A finite paired logistic-versus-boosting comparison is unavailable here.", "没有可用"),
        ]:
            with self.subTest(english=english):
                self.assertIn(chinese, tr(english))

    def test_actual_whitening_narration_keeps_the_pullback_bookmark_in_chinese(self):
        from explainer.zh_templates import Translator
        argument = next(n.args[0] for n in ast.walk(method("s09_lda.py", "fisher"))
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                        and n.func.attr == "voiceover" and isinstance(n.args[0], ast.JoinedStr))
        english = eval(compile(ast.Expression(argument), "actual-whitening-voiceover", "eval"),
                       dict(acc=.82, like_lr="."))
        chinese = Translator("ai6")(english)
        self.assertIsNotNone(chinese)
        bookmarks = lambda s: re.findall(r"<bookmark mark=['\"]([^'\"]+)['\"]/>", s)
        self.assertEqual(bookmarks(english), ["w", "pull", "a", "b", "c"])
        self.assertEqual(bookmarks(chinese), bookmarks(english))
        self.assertIn("逆平方根", chinese)
        self.assertIn("法向量映回原坐标", chinese)

    def test_actual_never_zero_sentence_has_a_computed_chinese_template(self):
        from explainer.zh_templates import Translator
        branch = next(n for n in method("s15_adaboost.py", "curves").body
                      if isinstance(n, ast.If) and any(assigned(x, "say") for x in ast.walk(n)))
        english = execute([branch], z0=None, n=3, tr=np.array([.2, .1, .1]),
                          te=np.array([.3, .2, .25]), best=2, keeps=False)["say"]
        chinese = Translator("ai6")(english)
        self.assertIsNotNone(chinese)
        self.assertIn("从未到零", chinese)
        self.assertNotIn("None", chinese)


if __name__ == "__main__":
    unittest.main()
