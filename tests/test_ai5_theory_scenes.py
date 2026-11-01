"""Part 5 teaching branches and private translation proposals; no scene/data imports."""
import ast
from collections import Counter
import json
import math
from pathlib import Path
import re
import string
import unittest
from unittest.mock import patch

import numpy as np

from explainer.zh_templates import Translator, _parts


ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "videos/ai/ai5"
OVERLAY = json.loads((ROOT / "tests/fixtures/ai5-theory-translation-overlay.json").read_text())


def helpers():
    tree = ast.parse((PART / "s15_mcmc.py").read_text())
    names = {"halfspace_summary", "flow_summary", "mixing_summary"}
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    env = {"math": math}
    exec(compile(ast.Module(nodes, type_ignores=[]), "actual-ai5-teaching-helpers", "exec"), env)
    return env


def rare_helpers():
    tree = ast.parse((PART / "s13_montecarlo.py").read_text())
    names = {"estimate_comparison", "direct_estimate_summary", "direct_rug_samples"}
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    env = {"math": math, "np": np}
    exec(compile(ast.Module(nodes, type_ignores=[]), "actual-ai5-rare-event-helpers", "exec"), env)
    return env


def identity(field, spec="", conversion=None):
    return ast.dump(ast.parse(field, mode="eval"), include_attributes=False), spec, conversion


class Part5TheorySceneTests(unittest.TestCase):
    def setUp(self):
        self.h = helpers()
        self.tr = Translator("ai5")
        self.tr.zh = {**self.tr.zh, **OVERLAY["ZH_updates"]}
        self.tr.phrases = {**self.tr.phrases, **OVERLAY["PHRASES"]}

    def translated(self, english):
        result = self.tr(english)
        self.assertIsNotNone(result, english)
        self.assertRegex(result, r"[\u4e00-\u9fff]")
        self.assertNotRegex(result, r"\{[^{}]+\}")
        self.assertEqual(re.findall(r"<bookmark[^>]+/>", english),
                         re.findall(r"<bookmark[^>]+/>", result))
        return result

    def test_density_distance_decrease_increase_equal_and_missing(self):
        f = self.h["flow_summary"]
        for args, word in [((1.2, .2), "降"), ((.2, 1.2), "升"), ((.2, .2), "保持"),
                           ((math.nan, .2), "不可用"), ((.2, math.inf), "不可用")]:
            with self.subTest(args=args):
                self.assertIn(word, self.translated(f(*args)))

    def test_halfspace_uses_actual_reference_without_success_threshold(self):
        f = self.h["halfspace_summary"]
        for actual in [.05, .665, .99]:
            text = f(actual, .664836346531934)
            self.assertNotIn("close", text)
            self.assertNotIn("short", text)
            self.assertIn("66.5", text)
            self.assertIn("66.5", self.translated(text))
        self.assertIn("不可用", self.translated(f(math.nan, .665)))

    def test_genuine_rare_rug_preserves_real_positions_and_all_hits(self):
        h = rare_helpers()
        z = np.zeros(500)
        z[10], z[450] = 4.789, 5.123
        indices = np.r_[np.arange(400), 450]
        shown, hits = h["direct_rug_samples"](z, indices, 500, 2)
        np.testing.assert_array_equal(shown, z[indices])
        np.testing.assert_array_equal(shown[hits], [4.789, 5.123])
        np.testing.assert_array_equal(hits, [10, 400])
        shown, hits = h["direct_rug_samples"](np.zeros(500), np.arange(400), 500, 0)
        self.assertEqual(len(shown), 400)
        self.assertEqual(len(hits), 0)
        with self.assertRaises(ValueError):
            h["direct_rug_samples"](z, np.arange(400), 500, 2)
        with self.assertRaises(ValueError):
            h["direct_rug_samples"](z, indices, 500, 1)

    def test_direct_and_weighted_estimate_zero_under_over_equal_translate(self):
        h = rare_helpers()
        for hits, estimate, word in [(0, 0., "没有命中"), (1, .1, "低于"),
                                      (4, .4, "高于"), (2, .2, "等于")]:
            result = h["direct_estimate_summary"](hits, 10, estimate, .2)
            self.assertIn(word, self.translated(result))
            self.assertNotIn("factor", result)
        for estimate, word in [(.1, "低于"), (.3, "高于"), (.2, "等于"), (math.nan, "不可用")]:
            self.assertIn(word, self.translated(h["estimate_comparison"](estimate, .2)))

    def test_mixing_rank_ties_reversal_and_missing_do_not_infer_rejection(self):
        spread = {"ula0.3": .56, "mala0.3": .342}
        for values, rank_term, comparison in [
                ((10, 8, 30, 2), "最多", "少于"),
                ((30, 8, 30, 30), "并列", "相同"),
                ((40, 8, 30, 50), "不是最多", "多于"),
                ((math.nan, 8, 30, 2), "不完整", "不可用")]:
            hops = dict(zip(("rwm0.7", "ula0.05", "ula0.3", "mala0.3"), values))
            result = self.h["mixing_summary"](hops, spread, .341416513049)
            chinese = [self.translated(x) for x in result]
            self.assertIn(rank_term, chinese[0])
            self.assertIn(comparison, chinese[2])
            self.assertIn("0.341", chinese[1])
            self.assertNotIn("refused", " ".join(result))
            self.assertNotIn("removes the bias", " ".join(result))
        result = self.h["mixing_summary"](dict.fromkeys(hops, 0),
                                                {"ula0.3": math.nan, "mala0.3": math.nan}, math.nan)
        self.assertIn("不可用", self.translated(result[1]))
        self.assertIn("不可用", self.translated(result[3]))

    def test_actual_changed_voiceovers_and_fields_translate_recursively(self):
        hops = {"rwm0.7": 70, "ula0.05": 13, "ula0.3": 228, "mala0.3": 6}
        rank, variance, comparison, corrected = self.h["mixing_summary"](
            hops, {"ula0.3": .56, "mala0.3": .342}, .341416513)
        values = dict(s=1.25, m=[4671, 0, 0, 0, 0, 184, 0, 10.5], n=5000,
                      i50=5, i200=7, th=[0]*7+[.0046866],
                      d={"hist_err": [.038], "fp_err": [.0004]},
                      f={"mle_nvar": [2.02]}, need={"hoeffding": 600, "exact": 262},
                      occupancy=self.h["halfspace_summary"](.65, .6648363465),
                      distance=self.h["flow_summary"](1.19, .23),
                      verdict=self.h["halfspace_summary"](.59, .6648363465),
                      rank=rank, variance=variance, comparison=comparison, corrected=corrected,
                      proxy_note="It is below one, so it cannot be a finite-sample weight count.",
                      true=.00003167, hits=0, plain=0., is_est=.000031,
                      direct_verdict=rare_helpers()["direct_estimate_summary"](0, 5000, 0., .00003167),
                      weighted_verdict=rare_helpers()["estimate_comparison"](.000031, .00003167), lam=.371,
                      H=1.6136)
        for row in OVERLAY["voiceover_handoff"]:
            tree = ast.parse((PART / row["file"]).read_text())
            vos = [n.args[0] for n in ast.walk(tree) if isinstance(n, ast.Call)
                   and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover"]
            node = vos[row["voiceover_index"]]
            source = node.value if isinstance(node, ast.Constant) else ast.unparse(node)
            self.assertEqual(source, row["en_source"])
            self.assertEqual(re.findall(r"<bookmark[^>]+/>", source),
                             re.findall(r"<bookmark[^>]+/>", row["old_source"]))
            local_values = dict(values)
            if row["file"] == "s07_maxent.py" and row["voiceover_index"] == 3:
                local_values["verdict"] = "the highest of them reaches 1.6135, just under"
            english = eval(compile(ast.Expression(node), "actual-ai5-voiceover", "eval"),
                           {"math": math}, local_values)
            chinese = self.translated(english)
            self.assertNotIn("unavailable", chinese)
            self.assertNotIn("For occupancy", chinese)
            if row["file"] == "s19_fokker.py" and row["voiceover_index"] == 3:
                self.assertIn("exact bin-average density", english)
                self.assertIn("both normalized on the shown window", english)
                self.assertNotIn("comparison points", english)
                self.assertIn("分箱平均密度", chinese)
                self.assertIn("窗口内归一化", chinese)
            if row["file"] == "s07_maxent.py" and row["voiceover_index"] == 3:
                self.assertIn("p(k+1)/p(k)", chinese)
                self.assertIn("1.45", chinese)
                self.assertIn("较高一面的概率更大", chinese)
            if isinstance(node, ast.JoinedStr):
                expected = Counter()
                for kind, value in _parts(node):
                    if kind == "name":
                        item = list(string.Formatter().parse("{" + value + "}"))[0]
                        expected[identity(item[1], item[2], item[3])] += 1
                actual = Counter(identity(f, s, c) for _, f, s, c in string.Formatter().parse(row["zh"])
                                 if f is not None)
                self.assertEqual(expected, actual)

    def test_actual_population_proxy_note_and_slice_tolerance_branches(self):
        for filename, name, cases in [
                ("s13_montecarlo.py", "proxy_note", [
                    ({"th": [.005], "i200": 0}, "小于1"),
                    ({"th": [1.0], "i200": 0}, "近似"),
                    ({"th": [5.0], "i200": 0}, "近似")]),
                ("s03_gauss.py", "verdict", [
                    ({"good": True}, "0.03"), ({"good": False}, "容差")])]:
            node = next(n.value for n in ast.walk(ast.parse((PART / filename).read_text()))
                        if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
            for values, expected in cases:
                text = eval(compile(ast.Expression(node), "actual-ai5-result-branch", "eval"), {}, values)
                self.assertIn(expected, self.translated(text))

    def test_caption_numeric_templates_keep_math_and_number_order(self):
        from explainer import lang, zh_text
        for en, zh in OVERLAY["strings"].items():
            self.assertEqual(zh_text._NUM.findall(en), zh_text._NUM.findall(zh), en)
            self.assertEqual(re.findall(r"\$[^$]+\$", en), re.findall(r"\$[^$]+\$", zh), en)
        with patch.object(lang, "LANG", "zh"), patch.object(zh_text, "_TABLE", OVERLAY), \
                patch.object(zh_text, "_BY_NUMBERS", None):
            result = zh_text.translate(r"visits with $x<0$: \ $91.2\%$ \\ target mass there: \ $66.5\%$")
            self.assertIn("91.2", result)
            self.assertIn("访问占比", result)
            result = zh_text.translate(r"target $\mathrm{Var}(x\mid x<0)$: \ $0.342$")
            self.assertIn("目标", result)
            self.assertIn("0.342", result)

    def test_all_new_literal_branches_and_proxy_notes_translate(self):
        for key in OVERLAY["ZH_updates"]:
            if not key.startswith(('f"', "f'")):
                self.translated(key)


if __name__ == "__main__":
    unittest.main()
