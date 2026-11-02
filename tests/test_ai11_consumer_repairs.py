"""Consumer regressions on extracted source AST and tiny synthetic fixtures.
No scene/model imports, scientific generation or renderer execution.
"""
import ast
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest
import numpy as np
from test_ai11_source_repairs import translator
ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai11'


def tree(file):
    return ast.parse((PART / file).read_text())

def method(file, fn):
    return next((n for n in ast.walk(tree(file)) if isinstance(n, ast.FunctionDef) and n.name == fn))

def evaluate(node, scope):
    return eval(compile(ast.Expression(node), '<candidate-expression>', 'eval'), dict(scope))

def assignment(file, fn, name, scope):
    n = next((n.value for n in ast.walk(method(file, fn)) if isinstance(n, ast.Assign) and any((isinstance(t, ast.Name) and t.id == name for t in n.targets))))
    return evaluate(n, scope)

def block(file, fn, name, scope):
    node = next((n for n in method(file, fn).body if isinstance(n, ast.If) and any((isinstance(q, ast.Assign) and any((isinstance(t, ast.Name) and t.id == name for t in q.targets)) for q in ast.walk(n)))))
    env = dict(scope)
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<candidate-branch>', 'exec'), env)
    return env[name]

def voice(file, fn, scope={}):
    node = next((n.args[0] for n in ast.walk(method(file, fn)) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and (n.func.attr == 'voiceover')))
    return evaluate(node, scope)

def fixtures():
    for at_edge, fe in [(True, 1520), (False, -1), (True, 0)]:
        s = dict(at_edge=at_edge, fe=fe, med={0.05: 39.0, 0.1: 20.0}, e0=0.05, e1=0.1)
        for name in ('said1', 'said2'):
            s[name] = assignment('s06_eos.py', 'edge', name, s)
        yield ('EdgeOfStability', voice('s06_eos.py', 'edge', s))
    yield ('EdgeOfStability', voice('s06_eos.py', 'takeaway'))
    for small in [True, False]:
        s = dict(m100=0.13 if small else 0.8, m1000=0.16, f1=0.95)
        s['said1'] = assignment('s07_adam.py', 'sign', 'said1', s)
        yield ('Adam', voice('s07_adam.py', 'sign', s))
    yield ('Adam', voice('s07_adam.py', 'lion'))
    for sep, gap in [(True, 0.1), (False, 0.1), (False, -0.1)]:
        for helps in [True, False]:
            for ea, el in [(True, True), (True, False), (False, True), (False, False)]:
                s = dict(sep=sep, gap=gap, helps=helps, ea=ea, el=el, wd_lo=0.0, wd_hi=3.0)
                s['verdict'] = block('s08_decay.py', 'grids', 'verdict', s)
                for name in ('etxt', 'said1', 'said2'):
                    s[name] = assignment('s08_decay.py', 'grids', name, s)
                yield ('Decay', voice('s08_decay.py', 'grids', s))
    yield ('Shampoo', voice('s10_shampoo.py', 'soap'))
    yield ('Muon', voice('s11_muon.py', 'recipe', dict(med=0.16)))
    yield ('Schedule', voice('s14_schedule.py', 'shapes'))
    yield ('Frontier', voice('s17_frontier.py', 'reality'))
    for diffs in [[0.004] * 3, [-0.02] * 3, [0.02, 0.03, 0.04], [-0.02, 0.03, -0.01]]:
        s = dict(diffs=diffs, spread=0.001, drop=0.1)
        s['verdict'] = block('s14_schedule.py', 'charmodel', 'verdict', s)
        yield ('Schedule', voice('s14_schedule.py', 'charmodel', s))
    yield ('ScheduleFree', voice('s15_free.py', 'average', dict(gap_cloud=0.49, gap_avg=0.154)))
    for gain, cd in [(0.1, 0.2), (0.1, 0.0), (0.1, -0.2), (0.0, 0.2), (-0.1, 0.2)]:
        s = dict(gain=gain, cooldown_gain=cd, e_end=2.0, c_end=2.1)
        s['share'] = assignment('s15_free.py', 'ema', 'share', s)
        s['said1'] = assignment('s15_free.py', 'ema', 'said1', s)
        yield ('ScheduleFree', voice('s15_free.py', 'ema', s))
    for gaps in [[-0.02] * 3, [0.005] * 3, [0.02, 0.03, 0.04], [-0.02, 0.02, 0.03], [-0.02, 0.05, -0.03]]:
        s = dict(gaps=gaps, mb=2.0, S=4000, Sm=4000, f_sf=2.1, f_cos=2.2, f_wsd=2.3, edge='')
        s['verdict'] = block('s15_free.py', 'measure', 'verdict', s)
        yield ('ScheduleFree', voice('s15_free.py', 'measure', s))

class FakeObject:

    def __init__(self, **kw):
        self.paths = []

    def start_new_path(self, p):
        self.paths.append([np.asarray(p)])
        return self

    def add_points_as_corners(self, ps):
        self.paths[-1].extend((np.asarray(p) for p in ps))
        return self

class FakeAxes:

    def c2p(self, x, y):
        return np.array([x, y, 0.0])

class FakeTracker:

    def __init__(self, t):
        self.t = t

    def get_value(self):
        return self.t

def replay_functions():
    nodes = [method('common.py', fn) for fn in ('curve_prefix', 'growing')]
    env = dict(np=np, VMobject=FakeObject, ValueTracker=FakeTracker, always_redraw=lambda fn: fn())
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<actual-candidate-replay>', 'exec'), env)
    return env

class ConsumerRepairs(unittest.TestCase):

    def test_replay_at_zero_between_and_after_cached_samples(self):
        fn = replay_functions()['curve_prefix']
        ax = FakeAxes()
        xs = [0, 40, 80]
        ys = [0, 8, 12]
        for t, expected in [(-1, []), (0, [[0, 0, 0], [0, 0, 0]]), (20, [[0, 0, 0], [0, 0, 0], [20, 4, 0]]), (100, [[0, 0, 0], [0, 0, 0], [40, 8, 0], [80, 12, 0]])]:
            got = fn(ax, xs, ys, t, 'x')
            np.testing.assert_allclose([p for path in got.paths for p in path], expected)
        got = fn(ax, [0, 40], [1, 100], 20, 'x', f=np.log10)
        np.testing.assert_allclose(got.paths[-1][-1], [20, 1, 0])

    def test_replay_breaks_at_nonfinite_gaps(self):
        fn = replay_functions()['curve_prefix']
        ax = FakeAxes()
        got = fn(ax, [0, 10, 20, 30, 40], [1, 2, np.nan, 4, 6], 35, 'x')
        self.assertEqual(len(got.paths), 2)
        np.testing.assert_allclose(got.paths[0][-1], [10, 2, 0])
        np.testing.assert_allclose(got.paths[1][-1], [35, 5, 0])
        got = fn(ax, [0, 10, 20], [1, np.inf, 3], 15, 'x')
        self.assertEqual(len(got.paths), 1)
        self.assertEqual(got.paths[0][-1][0], 0)
        self.assertEqual(len(fn(ax, [], [], 0, 'x').paths), 0)
        got = replay_functions()['growing'](ax, [0, 40], [0, 8], FakeTracker(20), 'x')
        np.testing.assert_allclose(got.paths[-1][-1], [20, 4, 0])

    def test_eos_uses_common_prefix(self):
        fn = next((n for n in ast.walk(method('s06_eos.py', 'edge')) if isinstance(n, ast.FunctionDef) and n.name == 'upto'))
        env = replay_functions()
        env.update(lc={0.1: np.array([[0, 2, 3], [40, 4, 9]])}, t=FakeTracker(20))
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<actual-eos-prefix>', 'exec'), env)
        got = env['upto'](FakeAxes(), 0.1, 'x', 2)
        np.testing.assert_allclose(got.paths[-1][-1], [20, 6, 0])

    def test_full_cloud_statistics_ignore_viewport_filter(self):
        fn = method('s15_free.py', 'average')
        nodes = [n for n in fn.body if isinstance(n, ast.Assign) and any((isinstance(t, ast.Name) and t.id in {'cl', 'visible', 'avg', 'gap_cloud', 'gap_avg'} for t in n.targets))]
        cloud = np.array([[0.0, 0.0], [0.5, 0.5], [4.0, 0.0]])
        env = dict(np=np, d={'cloud1': cloud, 'w_star': np.zeros(2)}, w1=[-1, 1], w2=[-1, 1])
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<actual-average-analysis>', 'exec'), env)
        self.assertEqual(len(env['visible']), 2)
        self.assertEqual(len(env['cl']), 3)
        np.testing.assert_allclose(env['avg'][-1], cloud.mean(0))
        self.assertAlmostEqual(env['gap_cloud'], np.sqrt((cloud ** 2).sum(1).mean()))

    def test_counterexample_verdicts(self):
        s = dict(sa=np.array([2.0] * 3), sl=np.array([3.0] * 3), none=2.5)
        s['helps'] = assignment('s08_decay.py', 'grids', 'helps', s)
        self.assertTrue(s['helps'])
        self.assertIn('At least one', assignment('s08_decay.py', 'grids', 'said1', s))
        for gaps in [[-0.02, 0.02, 0.03], [-0.02, 0.05, -0.03]]:
            self.assertIn('vary', block('s15_free.py', 'measure', 'verdict', dict(gaps=gaps)))
        for cd in [0, -0.1]:
            s = dict(gain=0.1, cooldown_gain=cd, e_end=2.0, c_end=2.1)
            s['share'] = assignment('s15_free.py', 'ema', 'share', s)
            self.assertIsNone(s['share'])
            text = assignment('s15_free.py', 'ema', 'said1', s)
            self.assertNotIn('%', text)
            self.assertIn('does not improve', text)
        verdict = block('s14_schedule.py', 'charmodel', 'verdict', dict(diffs=[0.004] * 3, spread=0.001))
        self.assertIn('comparison tolerance', verdict)

    def test_all_new_narration_branches_translate(self):
        tr = translator()
        for scene, en in fixtures():
            with self.subTest(scene=scene, en=en):
                zh = tr(en)
                self.assertIsNotNone(zh, en)
                self.assertEqual(re.findall('<bookmark mark=[\'\\"]([^\'\\"]+)[\'\\"]/>', en), re.findall('<bookmark mark=[\'\\"]([^\'\\"]+)[\'\\"]/>', zh))
                self.assertNotRegex(zh, '\\{[^{}]+\\}')
                self.assertNotIn('The averaged weights improve', zh)
                self.assertNotIn('Across the tested learning rates', zh)
                self.assertNotIn('the comparisons vary across lengths', zh)

    def test_true_warmup_interval_and_metric_units(self):
        ramp = next((n.value for n in ast.walk(method('s14_schedule.py', 'shapes')) if isinstance(n, ast.Assign) and any((isinstance(t, ast.Name) and t.id == 'ramp' for t in n.targets))))
        self.assertNotIn('WARMUP * 4', ast.unparse(ramp))
        self.assertIn('WARMUP', ast.unparse(ramp))
        self.assertIn('sixty', voice('s14_schedule.py', 'shapes'))
        self.assertIn('times eta in entry RMS', voice('s11_muon.py', 'recipe', {'med': 0.16}))
        self.assertIn('large-batch', voice('s10_shampoo.py', 'soap'))
        self.assertIn('modified SOAP or KL-SOAP', voice('s17_frontier.py', 'reality'))

    def test_conditional_eos_and_rounded_adam_fraction(self):
        self.assertIn('Training can approach', voice('s06_eos.py', 'takeaway'))
        s = dict(m100=0.13, m1000=0.16, f1=0.9998626708984375)
        s['said1'] = assignment('s07_adam.py', 'sign', 'said1', s)
        en = voice('s07_adam.py', 'sign', s)
        self.assertIn('about 100%', en)
        self.assertIn('大约100%', translator()(en))


class CaptionRuntime(unittest.TestCase):
    def test_actual_translation_replacements_have_valid_chinese_tex_commands(self):
        # Execute the production translator, without importing Manim or scenes.
        tree = ast.parse((ROOT/'explainer/zh_text.py').read_text())
        tree.body = [n for n in tree.body if not (isinstance(n,ast.ImportFrom)
                     and (n.module == 'manim' or n.module.startswith('explainer')))]
        scope = {'lang': SimpleNamespace(LANG='zh')}
        exec(compile(tree, '<production on-screen translator>', 'exec'),scope)
        data = json.loads((ROOT/'videos/ai/ai_text_zh.json').read_text())
        local = json.loads((PART/'text_zh_add.json').read_text())
        data['strings'].update(local['strings'])
        data.setdefault('patterns',[]).extend(local.get('patterns',[]))
        scope['_TABLE'],scope['_BY_NUMBERS'] = data,None
        env = dict(e={'late_median0.05':39.89795}, med=.15044026,s={'lr':.008})
        samples = []
        node = next(n for n in ast.walk(method('s06_eos.py','takeaway'))
                    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='takeaway_card')
        samples.append(evaluate(node.args[1],env))
        for file,fn,target in [('s11_muon.py','recipe','why02'),('s14_schedule.py','charmodel','tag')]:
            expr = next(n.value for n in ast.walk(method(file,fn)) if isinstance(n,ast.Assign)
                        and any(isinstance(t,ast.Name) and t.id==target for t in n.targets))
            call = next(n for n in ast.walk(expr) if isinstance(n,ast.Call)
                        and isinstance(n.func,ast.Name) and n.func.id in {'label','note'})
            samples.append(evaluate(call.args[0],env))
        for en in samples:
            zh=scope['translate'](en)
            self.assertRegex(zh,r'[一-鿿]')
            self.assertNotRegex(zh,r'(?<!\\)\\[^\x00-\x7f]')

        # Check all owned exact captions too, beyond the selected numeric fixtures.
        for en in local['strings']:
            zh = scope['translate'](en)
            self.assertNotRegex(zh,r'(?<!\\)\\[^\x00-\x7f]')

    def test_author_credit_is_not_replaced_by_cloud_measurements(self):
        entries=json.loads((PART/'text_zh_add.json').read_text())['strings']
        credit=r'Polyak \& Juditsky (1992), \ Ruppert (1988): \ the running mean'
        self.assertIn('1992',entries[credit]);self.assertIn('1988',entries[credit])
        self.assertNotIn('0.49',entries[credit]);self.assertNotIn('0.154',entries[credit])
        expr=next(n.value for n in method('s15_free.py','average').body if isinstance(n,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='cap' for t in n.targets))
        while isinstance(expr.func,ast.Attribute):expr=expr.func.value
        en=evaluate(expr.args[0],dict(gap_cloud=.4898767494,gap_avg=.1537284135))
        self.assertIn('$0.49$',entries[en]);self.assertIn('$0.154$',entries[en])


if __name__ == '__main__':unittest.main()
