"""Plot-domain regression from public METR facts; no renderer or synthetic acceptance."""
import ast
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / 'videos/ai/ai29/s07_doubling.py'
TREE = ast.parse(SCENE.read_text())
FUNCTION = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'horizon_plot_bounds')
NS = {'math': math}
exec(compile(ast.Module(body=[FUNCTION], type_ignores=[]), str(SCENE), 'exec'), NS)


class MetrPlotContracts(unittest.TestCase):
    def test_domain_contains_every_ci_and_both_horizons(self):
        facts = json.loads((ROOT / 'tests/fixtures/ai29_metr_20261103.json').read_text())
        rows = [dict(lo=r[3], hi=r[4], p80=r[5]) for r in facts['rows']]
        for mixed in (False, True):
            lo, hi = NS['horizon_plot_bounds'](rows, mixed)
            self.assertEqual((lo, hi), (-7, 12))
            for row in rows:
                for key in ('lo', 'hi', 'p80') if mixed else ('lo', 'hi'):
                    self.assertLessEqual(lo, math.log2(row[key]))
                    self.assertGreaterEqual(hi, math.log2(row[key]))
        with self.assertRaises(ValueError):
            NS['horizon_plot_bounds']([dict(lo=0, hi=1)])

    def test_semantics_and_no_upper_interval_truncation(self):
        text = SCENE.read_text()
        self.assertIn('self.plot(include80=True)', text)
        self.assertIn(r'$50\%$ and $80\%$ time horizons', text)
        self.assertIn('model-row bootstrap', text)
        self.assertNotIn('min(math.log2(r["hi"])', text)
        self.assertIn('RIGHT if r["name"] == "GPT-2" else LEFT', text)
        self.assertNotIn('every doubling is a halving of the error per step', text)
        self.assertIn('do not directly measure per-step error', text)


    def test_continuous_hazard_rate_and_task_crossing_qualification(self):
        text = SCENE.read_text()
        self.assertIn(r'constant-hazard model: \\ rate $\lambda$ per minute', text)
        self.assertIn('continuous constant-failure-rate model', text)
        self.assertNotIn('same chance $\\lambda$', text)
        self.assertNotIn('same small chance in every minute', text)
        self.assertNotIn('success falls off with length', text)
        self.assertEqual(text.count('task-level crossings across heterogeneous tasks'), 3)
        self.assertEqual(text.count('a per-minute failure mechanism.'), 3)
        captions = json.loads((ROOT / 'videos/ai/ai29/text_zh_add.json').read_text())
        captions = captions.get('strings', captions)
        shared = json.loads((ROOT / 'videos/ai/ai_text_zh.json').read_text())['strings']
        key = r'constant-hazard model: \\ rate $\lambda$ per minute'
        self.assertIn('速率', captions[key])
        self.assertEqual(captions[key], shared[key])
        nar = json.loads((ROOT / 'videos/ai/ai29/narration_zh.json').read_text())
        row = next(v for v in nar['lines'].values() if v['en'].startswith('Half the time is a low bar'))
        self.assertIn('continuous constant-failure-rate', row['en'])
        self.assertIn('恒定失败率', row['zh'])
        self.assertIn('not evidence of a per-minute failure mechanism', row['en'])
        self.assertIn('并不能证明实际存在某种每分钟失败机制', row['zh'])


if __name__ == '__main__':
    unittest.main()
