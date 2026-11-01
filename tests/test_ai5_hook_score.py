"""Hook score/time/narration contracts without scene imports or production loads."""
import ast
import json
import math
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

import numpy as np

from explainer.zh_templates import Translator


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "videos/ai/ai5/s01_hook.py"
OVERLAY = json.loads((ROOT / "tests/fixtures/ai5-hook-score-overlay.json").read_text())


class Part5HookScoreTests(unittest.TestCase):
    def test_actual_field_time_reaches_zero_and_stays_in_interval(self):
        tree = ast.parse(SOURCE.read_text())
        field = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "field")
        expression = next(n.value for n in field.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == "tt" for t in n.targets))
        for tracker, expected in [(0, 5), (25, 2.5), (50, 0), (100, 0), (-10, 5)]:
            result = eval(compile(ast.Expression(expression), "actual-Hook-field-time", "eval"),
                          {"np": np}, {"T": 5, "n": 50, "t": SimpleNamespace(get_value=lambda: tracker)})
            self.assertEqual(result, expected)

    def test_exact_score_is_finite_at_zero_with_positive_blob_variance(self):
        tree = ast.parse(SOURCE.read_text())
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "score_at")
        env = {"np": np, "math": math}
        exec(compile(ast.Module([node], type_ignores=[]), "actual-Hook-score_at", "exec"), env)
        x, data = np.array([[0., 0.], [1., .5]]), np.zeros((1, 2))
        for t in [0, .01, .06, 2.5, 5]:
            variance = math.exp(-t) * .03 ** 2 + 1 - math.exp(-t)
            score = env["score_at"](data, x, t)
            np.testing.assert_allclose(score, -x / variance)
            self.assertTrue(np.isfinite(score).all())

    def test_actual_two_voiceovers_translate_with_bookmarks_and_score_semantics(self):
        tr = Translator("ai5")
        tr.zh = {**tr.zh, **OVERLAY["ZH_updates"]}
        tree = ast.parse(SOURCE.read_text())
        vos = [n.args[0].value for n in ast.walk(tree) if isinstance(n, ast.Call)
               and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover"]
        for row in OVERLAY["voiceovers"]:
            en = vos[row["voiceover_index"]]
            self.assertEqual(en, row["en"])
            zh = tr(en)
            self.assertEqual(zh, row["zh"])
            self.assertEqual(re.findall(r"<bookmark[^>]+/>", en),
                             re.findall(r"<bookmark[^>]+/>", row["old_en"]))
            self.assertEqual(re.findall(r"<bookmark[^>]+/>", en),
                             re.findall(r"<bookmark[^>]+/>", zh))
        self.assertIn("only score directions", vos[0])
        self.assertIn("position divided by two, plus the score", vos[0])
        self.assertIn("computed exactly", vos[1])
        self.assertIn("other drift term is already known", vos[1])


if __name__ == "__main__":
    unittest.main()
