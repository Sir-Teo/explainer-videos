"""Exercise actual retrieval scene branches without importing models or loading data."""
import ast
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / 'videos/ai/ai3/s18_netflix.py'


def source_nodes():
    tree = ast.parse(SCENE.read_text())
    helpers = [n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name in ('retrieval_display_data', 'retrieval_cohort_summary')]
    netflix = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Netflix')
    towers = next(n for n in netflix.body if isinstance(n, ast.FunctionDef) and n.name == 'towers')
    return helpers, towers


def result(warm=(3, 5, .4, .1), cold=(2, 4, .2, .3)):
    wu, wt, wr, wp = warm
    cu, ct, cr, cp = cold
    return dict(curve=[[1, 1, wr, cr], [100, .5, wr, cr]], recall_warm=wr, recall_cold=cr,
                pop_warm=wp, pop_cold=cp,
                evaluation=dict(warm=dict(evaluated_users=wu, eligible_targets=wt),
                                cold=dict(evaluated_users=cu, eligible_targets=ct)))


class RetrievalSceneTests(unittest.TestCase):
    def run_actual_scene(self, data):
        records = dict(curves=[], baselines=[], labels=[], legends=[], narration=[])

        class Object:
            def __init__(self, *args, **kwargs):
                pass

            def __getattr__(self, name):
                if name.startswith('get_'):
                    return lambda *a, **k: np.zeros(3)
                return lambda *a, **k: self

            def c2p(self, *coordinates):
                self_test.assertTrue(np.isfinite(coordinates).all(), coordinates)
                return np.r_[coordinates[:2], 0.]

        self_test = self

        def axes(xrange, yrange, **kwargs):
            self.assertTrue(np.isfinite(xrange + yrange).all())
            group = Object()
            group.ax = Object()
            return group

        def curve(ax, x, y, color, width):
            records['curves'].append((np.asarray(x), np.asarray(y)))
            return Object()

        def baseline(start, end, **kwargs):
            self.assertTrue(np.isfinite(start).all() and np.isfinite(end).all())
            records['baselines'].append((start, end))
            return Object()

        def text(value, **kwargs):
            records['labels'].append(value)
            return Object()

        def legend(rows, **kwargs):
            records['legends'].append(rows)
            return Object()

        class Scene:
            def play(self, *args, **kwargs):
                pass

            def wait(self, *args, **kwargs):
                pass

            def clear_scene(self):
                pass

            @contextmanager
            def voiceover(self, words):
                records['narration'].append(words)
                yield SimpleNamespace(wait_until=lambda mark: None)

        ns = dict(np=np, load=lambda name: data, axes=axes, curve=curve, DashedLine=baseline,
                  label=text, note=text, MathTex=text, legend=legend,
                  fmt_int=lambda v: f'{int(v):,}', TT='green', POP='grey',
                  GREY_A='greyA', GREY_B='greyB', C=SimpleNamespace(TRUE_P='blue', MODEL_Q='orange', BITS='yellow'))
        for name in ('RoundedRectangle', 'Rectangle', 'VGroup', 'Arrow', 'Dot', 'FadeIn', 'Create'):
            ns[name] = Object
        for name, vec in [('DOWN', [0, -1, 0]), ('UP', [0, 1, 0]), ('RIGHT', [1, 0, 0])]:
            ns[name] = np.array(vec, float)
        helpers, towers = source_nodes()
        definition = ast.ClassDef(name='ActualScene', bases=[ast.Name(id='Scene', ctx=ast.Load())],
                                  keywords=[], body=[towers], decorator_list=[])
        ns['Scene'] = Scene
        module = ast.fix_missing_locations(ast.Module(body=helpers + [definition], type_ignores=[]))
        exec(compile(module, str(SCENE), 'exec'), ns)
        ns['ActualScene']().towers()
        return records, ns

    def test_empty_cohorts_have_no_curves_baselines_or_loss_verdict(self):
        empty = (0, 0, float('nan'), float('nan'))
        r, _ = self.run_actual_scene(result(empty, empty))
        self.assertEqual((len(r['curves']), len(r['baselines']), len(r['legends'])), (0, 0, 0))
        words = r['narration'][0]
        self.assertEqual(words.count('recall is unavailable'), 2)
        self.assertIn('0 evaluated users have 0 eligible held-out targets', words)
        self.assertNotIn('Neither beats', words)
        self.assertNotIn('nan', words.lower())
        self.assertTrue(any('no eligible held-out targets' in s for s in r['labels']))

    def test_only_eligible_warm_cohort_is_plotted_and_compared(self):
        r, _ = self.run_actual_scene(result(cold=(0, 0, float('nan'), float('nan'))))
        self.assertEqual((len(r['curves']), len(r['baselines'])), (1, 1))
        self.assertEqual(len(r['legends'][0]), 2)
        words = r['narration'][0]
        self.assertIn('For known users, macro recall reaches 0.40', words)
        self.assertIn('The two towers beat popularity for this cohort.', words)
        self.assertIn('For new users, recall is unavailable', words)
        self.assertNotIn('nan', words.lower())

    def test_zero_counts_override_finite_stale_measurements(self):
        r, _ = self.run_actual_scene(result(warm=(0, 0, .9, .1), cold=(2, 0, .8, .2)))
        self.assertEqual((len(r['curves']), len(r['baselines'])), (0, 0))
        self.assertEqual(r['narration'][0].count('recall is unavailable'), 2)
        self.assertNotIn('beat popularity for this cohort', r['narration'][0])

    def test_finite_model_without_baseline_has_no_comparison(self):
        r, _ = self.run_actual_scene(result(warm=(0, 0, float('nan'), float('nan')),
                                           cold=(2, 4, .2, float('nan'))))
        self.assertEqual((len(r['curves']), len(r['baselines'])), (1, 0))
        self.assertIn('two-tower recall is 0.20 on 2 users and 4 eligible targets', r['narration'][0])
        self.assertIn('popularity recall is unavailable. No comparison', r['narration'][0])
        self.assertNotIn('beat popularity for this cohort', r['narration'][0])

    def test_nonfinite_model_omits_curve_but_keeps_finite_baseline(self):
        r, _ = self.run_actual_scene(result(warm=(3, 5, float('nan'), .1),
                                           cold=(2, 4, float('nan'), float('nan'))))
        self.assertEqual((len(r['curves']), len(r['baselines'])), (0, 1))
        self.assertIn('two-tower recall is unavailable on 3 users and 5 eligible targets', r['narration'][0])
        self.assertIn('both recall measurements are unavailable', r['narration'][0])
        self.assertNotIn('nan', r['narration'][0].lower())

    def test_available_cohorts_keep_both_curves_and_truthful_comparisons(self):
        r, ns = self.run_actual_scene(result())
        self.assertEqual((len(r['curves']), len(r['baselines'])), (2, 2))
        self.assertEqual(len(r['legends'][0]), 4)
        self.assertIn('The two towers beat popularity for this cohort.', r['narration'][0])
        self.assertIn('The two towers do not beat popularity for this cohort.', r['narration'][0])
        data = result()
        data['curve'][0][2] = float('nan')
        display = ns['retrieval_display_data'](data)
        self.assertTrue(display['warm']['show_curve'])
        self.assertTrue(np.isnan(display['warm']['values'][0]))


if __name__ == '__main__':
    unittest.main()
