"""Finite scientific checks for the dependency-free HMM schematic."""
from pathlib import Path
import ast
import json
import math
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from videos.ai.ai23.acoustic_math import schematic_feature_density


class AcousticContracts(unittest.TestCase):
    def test_density_mass_and_moments(self):
        x = np.linspace(-4, 4, 16001)
        y = schematic_feature_density(x)
        self.assertTrue(np.isfinite(y).all())
        self.assertTrue((y >= 0).all())
        self.assertAlmostEqual(float(np.trapezoid(y, x)), 1, places=10)
        self.assertAlmostEqual(float(np.trapezoid(x*y, x)), -0.04, places=10)
        self.assertAlmostEqual(float(np.trapezoid(x*x*y, x)), 0.1765, places=10)

    def test_cropped_plot_is_not_renormalized(self):
        a, b = -1.1, 1.1
        x = np.linspace(a, b, 16001)
        cdf = lambda z, mean, sd: (1 + math.erf((z-mean)/(sd*math.sqrt(2))))/2
        expected = sum(w*(cdf(b,m,s)-cdf(a,m,s)) for w,m,s in [(0.6,-0.3,0.25),(0.4,0.35,0.3)])
        self.assertAlmostEqual(float(np.trapezoid(schematic_feature_density(x), x)), expected, places=8)
        self.assertLess(expected, 1)

    def test_best_path_can_change_the_word_decision(self):
        # Joint path likelihood contributions, not per-word normalized paths.
        priors = np.array([0.5, 0.5])
        paths = [(0.3, 0.3), (0.4,)]
        marginal = priors * [sum(q) for q in paths]
        best_path = priors * [max(q) for q in paths]
        np.testing.assert_allclose(marginal, [0.30, 0.20])
        np.testing.assert_allclose(best_path, [0.15, 0.20])
        self.assertNotEqual(int(marginal.argmax()), int(best_path.argmax()))

    def test_actual_hmm_source_and_chinese_contract(self):
        from explainer.zh_templates import Translator
        from explainer.lang import BOOKMARK
        path = ROOT/'videos/ai/ai23/s11_audrey.py'
        tree = ast.parse(path.read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Audrey')
        fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'hmm')
        self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'load' for n in ast.walk(fn)))
        literals = [n.value for n in ast.walk(fn) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertIn(r'P(X\mid W)=\sum_Q P(X,Q\mid W)', literals)
        expr = next(n.args[0] for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        en = ast.literal_eval(expr)
        zh = Translator('ai23')(en)
        self.assertIsNotNone(zh)
        self.assertEqual(BOOKMARK.findall(en), BOOKMARK.findall(zh))
        for text in ['音素内部', '概率密度', '除以状态先验', '并不是第一种']:
            self.assertIn(text, zh)
        tables = [json.loads((ROOT/p).read_text())['strings'] for p in ['videos/ai/ai23/text_zh_add.json','videos/ai/ai_text_zh.json']]
        for key in [s for s in literals if any(t in s for t in ['illustrative acoustic states:', 'Gaussian-mixture density', 'word likelihood:', '2012 joint review:'])]:
            self.assertIn(key, tables[0])
            self.assertEqual(tables[0][key], tables[1][key])


if __name__ == '__main__':
    unittest.main(verbosity=2)
