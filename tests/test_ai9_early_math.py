"""Synthetic metric-unit and finite-budget narration regressions; no scene/cache imports."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
import numpy as np

PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai9'

def method(file, name):
    return next(n for n in ast.walk(ast.parse((PART / file).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)

def assigned(fn, name, env):
    expr = next(n.value for n in ast.walk(fn) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return eval(compile(ast.Expression(expr), '<actual-source-expression>', 'eval'), env)

class EarlyMathQualifications(unittest.TestCase):
    def test_gradient_comparison_preserves_distinct_absolute_and_relative_units(self):
        # Deliberately unequal absolute(.5) and relative(.75) discrepancies.
        env = dict(np=np, flat=lambda g: g, g_ad=np.array([.5, 1.]),
                   g_bp=np.array([1., 1.]), g_fd=np.array([.5, 4.]))
        fn = method('compute.py', 'compute_xor')
        absolute, relative = (assigned(fn, n, env) for n in ('err_bp', 'err_fd'))
        self.assertEqual((absolute, relative), (.5, .75))
        fn = method('s05_backprop.py', 'check')
        label = assigned(fn, 'agree', dict(d={'err_bp': absolute, 'err_fd': relative},
                         sci=lambda v, precision: f'{v:.2f}', label=lambda s, **kw: s,
                         C=SimpleNamespace(BITS='unused')))
        self.assertIn('$0.50$ (absolute)', label)
        self.assertIn('$0.75$ \\ (relative)', label)

    def test_unsolved_starts_are_reported_as_budget_observations(self):
        fn = method('s04_xor.py', 'hidden')
        unsolved = assigned(fn, 'caveat', {'solved': 7, 'starts': 20})
        self.assertIn('7 of 20', unsolved)
        self.assertIn('fixed training budget', unsolved)
        self.assertIn('did not reach it in that budget', unsolved)
        self.assertNotIn('local minimum', unsolved)
        solved = assigned(fn, 'caveat', {'solved': 20, 'starts': 20})
        self.assertIn('All 20', solved)

if __name__ == '__main__':
    unittest.main()
