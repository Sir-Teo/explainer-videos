"""Synthetic fit fixtures and source wiring checks, not new warehouse trials."""
import ast
import hashlib
import json
from pathlib import Path
import re
import runpy
import unittest

import numpy as np

from videos.ai.ai29.agent_fit import agent_decay_fit, agent_fit_curve

PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai29'


class AgentFitContracts(unittest.TestCase):
    def test_free_amplitude_is_retained_not_unit_curve(self):
        ns = np.array([1, 2, 3, 5, 8, 12, 20, 30, 45, 60])
        expected_amplitude, expected_p = .73, .97  # synthetic known curve
        fit = agent_decay_fit(ns, expected_amplitude * expected_p ** ns)
        self.assertAlmostEqual(fit['amplitude'], expected_amplitude, places=12)
        self.assertAlmostEqual(fit['decay'], expected_p, places=12)
        xx, yy = agent_fit_curve(ns, fit)
        np.testing.assert_allclose(yy, expected_amplitude * expected_p ** xx)
        self.assertGreater(np.max(np.abs(yy - expected_p ** xx)), .2)

    def test_only_measured_domain_and_original_mask(self):
        ns = np.array([1., 10., 20., 60.])
        success = .8 * .96 ** ns
        success[-1] = .01  # excluded by the original >.02 fit mask
        fit = agent_decay_fit(ns, success)
        self.assertAlmostEqual(fit['amplitude'], .8)
        xx, yy = agent_fit_curve(ns, fit)
        self.assertEqual(xx[0], 1.)
        self.assertEqual(xx[-1], 60.)
        self.assertTrue(np.all(xx > 0))
        self.assertTrue(np.isfinite(yy).all())

    def test_bad_or_unidentifiable_fit_rejected(self):
        for ns, values in [([0, 1], [.5, .4]), ([1, 2], [np.nan, .2]),
                           ([1, 2], [.01, .02]), ([1, 1], [.4, .3]),
                           ([1, 2], [1.1, .3])]:
            with self.subTest(ns=ns, values=values), self.assertRaises(ValueError):
                agent_decay_fit(ns, values)

    def test_scene_uses_derived_curve_and_effective_decay_label(self):
        tree = ast.parse((PART / 's06_compound.py').read_text())
        measured = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'measured')
        calls = [n for n in ast.walk(measured) if isinstance(n, ast.Call)]
        self.assertTrue(any(isinstance(n.func, ast.Name) and n.func.id == 'agent_decay_fit' for n in calls))
        curve_calls = [n for n in calls if isinstance(n.func, ast.Name) and n.func.id == 'curve']
        self.assertEqual(len(curve_calls), 1)
        self.assertEqual([ast.unparse(x) for x in curve_calls[0].args[1:3]], ['xx', 'yy'])
        self.assertIn('effective decay', ast.unparse(measured))
        fit = next(n for n in ast.walk(measured) if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'fit' for t in n.targets))
        en = ast.literal_eval(fit.value)
        self.assertIn('not measured single-step reliability', en)
        self.assertIn('free amplitude', en)
        zh_table = runpy.run_path(str(PART / 'zh_lines.py'))['ZH']
        matches = [value for prefix, value in zh_table.items() if en.startswith(prefix)]
        self.assertEqual(len(matches), 1)
        self.assertIn('不是测得的单步可靠性', matches[0])
        for row in json.loads((PART / 'narration_zh.json').read_text())['lines'].values():
            if row['en'].startswith('Our warehouse agent shows'):
                self.assertIn(en, row['en'])
                self.assertIn(matches[0], row['zh'])
                self.assertEqual(re.findall("<bookmark mark='([^']+)'", row['en']),
                                 re.findall("<bookmark mark='([^']+)'", row['zh']))


if __name__ == '__main__':
    unittest.main()
