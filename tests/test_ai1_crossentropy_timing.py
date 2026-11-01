"""Actual supplied CE word cues and installed frame clock; no audio/model/render I/O."""
import ast
import copy
import gzip
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np
from test_ai1_entropy_prefix_timing import actual_tracker, compile_nodes, function, Shape, Clock, tag

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/qa/evidence/ai1-crossentropy-narrated-timing-repair'
SOURCE = ROOT / 'videos/ai/ai1/s08_cross_entropy.py'
DIAGNOSTIC_SHA = '0f461bd770ccf3baeb8ec1cdf1cdb8b9430b82ea9e86d1a17ad7d473b56e92ad'


def diagnostic():
    return json.loads(gzip.decompress((EVIDENCE / 'exact-diagnostic.json.gz').read_bytes()))


def tree(before=False):
    return ast.parse(gzip.decompress((EVIDENCE / 'source-before.py.gz').read_bytes()) if before else SOURCE.read_bytes())


class Row(Shape):
    def __init__(self, name, tex):
        super().__init__(name)
        self.tex_strings = tex
        self.parts = [Shape(name + ':' + s) for s in tex]
    def __iter__(self):
        return iter(self.parts)
    def __len__(self):
        return len(self.parts)


class Part(Shape):
    def __len__(self):
        return 1


class CEClock(Clock):
    def play(self, *animations, run_time=None, **kwargs):
        if run_time is None:
            # The supplied exact preflight observes the decomposition's Write=2s.
            run_time = 2. if any(a[0] == 'Write' for a in animations) else 1.
        return super().play(*animations, run_time=run_time, **kwargs)


def shared_step(scene):
    shared = ast.parse((ROOT / 'explainer/analysis/__init__.py').read_text())
    rows_node = next(n for n in function(tree(), 'gibbs').body
                     if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                     and n.targets[0].id == 'rows')
    ns = dict(D=r'-D_{\mathrm{KL}}(p \,\|\, q)', colors={},
              cmath=lambda *tex, **kw: Row('row-' + '|'.join(tex), list(tex)))
    compile_nodes([rows_node], ns, 'actual-four-Gibbs-row-terms')
    rows = ns['rows']
    for r in rows:
        r.parts = [Part(r.name + ':' + s) for s in r.tex_strings]
    scope = dict(scene=scene, rows=rows, whys=[Shape('why' + str(i)) for i in range(4)],
                 keep=4, top=2.6, buff=.3, extra=[0.] * 4, offs=[0.] * 4,
                 UP=np.array([0., 1., 0.]), highlight=True, C=SimpleNamespace(EPS='yellow'), MathTex=Row)
    for name in ['FadeOut', 'FadeIn', 'Write', 'TransformMatchingTex', 'ShowPassingFlash']:
        scope[name] = lambda *args, _name=name, **kw: (_name, tag(args), tag(kw))
    scope['Underline'] = lambda m, **kw: Shape('underline-' + m.name)
    compile_nodes([function(shared, 'changed_parts'), function(function(shared, 'ladder'), 'step')],
                  scope, 'actual-shared-ladder-branch-and-changed-terms')
    return scope['step']


def wait_node(n, mark):
    return (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
            and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == 'wait_until'
            and n.value.args[0].value == mark)


def run_span(method, start, end, fps=60, phase=0., before=False, rounded=True, tail=False):
    d = diagnostic()
    index = 3 if method == 'decompose' else 4
    block, occurrence = d['narration_blocks'][index], d['exact_narration_occurrences'][index]
    aligned = d['per_utterance_word_alignment_and_duration'][occurrence['key']]
    scene = CEClock(fps, rounded)
    vo = actual_tracker(block, occurrence, aligned, scene)
    scene.renderer.time = (vo.mark_time(start) if start else 0.) + phase / fps
    scene.parts = Shape('existing-parts')
    ns = dict(config=SimpleNamespace(frame_rate=fps), self=scene, vo=vo, step=shared_step(scene),
              rows=[Shape('decompose-row0'), Shape('decompose-row1')])
    for key in ['b1', 'b2', 't1', 't2']:
        ns[key] = Shape(key)
    ns['nums'] = [Shape('number' + str(i)) for i in range(3)]
    for key in ['FadeOut', 'FadeIn', 'Write', 'TransformMatchingTex', 'GrowFromCenter', 'LaggedStart']:
        ns[key] = lambda *args, _key=key, **kw: (_key, tag(args), tag(kw))
    tr = tree(before)
    helpers = [n for n in tr.body if isinstance(n, ast.FunctionDef)
               and n.name in {'_bookmark_run_times', '_bookmark_ladder_step'}]
    body = next(n for n in function(tr, method).body if isinstance(n, ast.With)).body
    first = next(i for i, n in enumerate(body) if wait_node(n, start)) + 1 if start else 0
    last = len(body) if tail else next(i for i, n in enumerate(body) if wait_node(n, end))
    compile_nodes(helpers + body[first:last], ns, 'actual-CrossEntropy-cue-span')
    return scene, vo, ns, aligned


class CrossEntropyTiming(unittest.TestCase):
    def test_exact_source_diagnostic_all_nine_blocks_22_cues_and_master_identities(self):
        raw = gzip.decompress((EVIDENCE / 'exact-diagnostic.json.gz').read_bytes())
        self.assertEqual(hashlib.sha256(raw).hexdigest(), DIAGNOSTIC_SHA)
        d = json.loads(raw)
        self.assertEqual(d['source_sha256'], '149412abb320476bf16ba2abb7c632d4f40b707274b576eb12c77b9265f9948f')
        self.assertEqual(hashlib.sha256(gzip.decompress((EVIDENCE / 'source-before.py.gz').read_bytes())).hexdigest(), d['source_sha256'])
        self.assertEqual(len(d['narration_blocks']), 9)
        self.assertEqual(len(d['all_bookmark_requests']), 22)
        self.assertEqual([m['key'] for m in d['speech_masters']], [o['key'] for o in d['exact_narration_occurrences']])
        by_start = {}
        for block, occ in zip(d['narration_blocks'], d['exact_narration_occurrences']):
            aligned = d['per_utterance_word_alignment_and_duration'][occ['key']]
            vo = actual_tracker(block, occ, aligned, CEClock(60))
            self.assertEqual(vo.duration, block['duration'])
            by_start[round(block['start'], 8)] = (block, vo)
        mismatches = []
        for request in d['all_bookmark_requests']:
            block, vo = by_start[round(request['block_start'], 8)]
            actual = vo.mark_time(request['mark'])
            expected = request['target_seconds'] - block['start']
            if abs(actual - expected) > 1e-8:
                mismatches.append((round(block['start'], 2), request['mark'], round(actual, 2), round(expected, 2)))
            else:
                self.assertAlmostEqual(block['start'] + actual, request['target_seconds'])
        # The raw proper name is one token; the supplied spoken alignment splits
        # Kullback Leibler. Preserve this host-vs-repository target discrepancy
        # explicitly, rather than silently modifying its metadata or timing.
        self.assertEqual(mismatches, [(43.26, 'c', 14.5, 15.97)])
        for master in d['speech_masters']:
            self.assertRegex(master['sha256'], r'^[0-9a-f]{64}$')
            self.assertGreater(master['bytes'], 0)
        # These remain supplied metadata; no local/remote audio file is opened.

    def test_actual_original_spans_reproduce_all_three_observed_overruns(self):
        for method, start, end, late in [('decompose', None, 'a', 1.36), ('gibbs', 'c', 'd', .55), ('gibbs', 'c', 'e', 1.15)]:
            s, vo, _, _ = run_span(method, start, end, 100, before=True, rounded=False)
            self.assertAlmostEqual(s.renderer.time - vo.mark_time(end), late, places=10)
        s, _, _, _ = run_span('gibbs', 'c', 'e', 100, before=True, rounded=False)
        self.assertEqual([e['requested'] for e in s.events], [.6, 1.2, .5, .6, 1.2, .8])

    def test_actual_adaptive_spans_and_animation_order_at_frame_phases(self):
        for method, start, end in [('decompose', None, 'a'), ('gibbs', 'c', 'd'), ('gibbs', 'd', 'e')]:
            for fps in [15, 30, 60]:
                for phase in [0., .49, 1.]:
                    with self.subTest(method=method, start=start, end=end, fps=fps, phase=phase):
                        s, vo, _, _ = run_span(method, start, end, fps, phase)
                        old, _, _, _ = run_span(method, start, end, fps, phase, before=True)
                        self.assertLessEqual(s.renderer.time, vo.mark_time(end) - 1 / fps + 1e-10)
                        self.assertTrue(all(e['requested'] >= 1 / fps for e in s.events))
                        self.assertEqual([e['args'] for e in s.events], [e['args'] for e in old.events])
                        self.assertEqual([e['kwargs'] for e in s.events], [e['kwargs'] for e in old.events])
                        self.assertNotIn('play', s.__dict__)

    def test_retained_proof_rows_have_reading_time_after_completion(self):
        for fps in [15, 30, 60]:
            for phase in [0., .49, 1.]:
                s, vo, _, aligned = run_span('gibbs', 'c', None, fps, phase, tail=True)
                self.assertGreaterEqual(aligned['duration'] - s.renderer.time, 1.5)
                s, vo, _, aligned = run_span('decompose', None, 'a', fps, phase)
                # Original row remains alongside its copied decomposition through the block.
                self.assertGreaterEqual(aligned['duration'] - s.renderer.time, 1.5)

    def test_ladder_adapter_restores_class_and_instance_play_after_exception(self):
        helpers = [n for n in tree().body if isinstance(n, ast.FunctionDef)
                   and n.name in {'_bookmark_run_times', '_bookmark_ladder_step'}]
        for override in [False, True]:
            for failing in [False, True]:
                s = CEClock(60)
                if override:
                    s.play = lambda *a, **kw: None
                original = s.__dict__.get('play')
                ns = compile_nodes(helpers, dict(config=SimpleNamespace(frame_rate=60)), 'actual-local-adapter')
                vo = SimpleNamespace(mark_time=lambda _: 10., elapsed=lambda: 0.)
                def step(index):
                    for v in [.6, 1.2, .5]:
                        s.play(('stage', ()), run_time=v)
                        if failing:
                            raise RuntimeError('expected interruption')
                    return index
                if failing:
                    with self.assertRaisesRegex(RuntimeError, 'expected interruption'):
                        ns['_bookmark_ladder_step'](s, step, 1, vo, 'd', .6, 1.2, .5)
                else:
                    self.assertEqual(ns['_bookmark_ladder_step'](s, step, 1, vo, 'd', .6, 1.2, .5), 1)
                self.assertEqual('play' in s.__dict__, override)
                if override:
                    self.assertIs(s.play, original)

    def test_generous_and_physically_impossible_cues_remain_distinct(self):
        helper = function(tree(), '_bookmark_run_times')
        for fps in [15, 30, 60]:
            ns = compile_nodes([helper], dict(config=SimpleNamespace(frame_rate=fps)), 'actual-budget')
            for nominal in [(1., 2.), (.6, 1.2, .5), (.6, 1.2, .8)]:
                good = SimpleNamespace(mark_time=lambda _: 30., elapsed=lambda: 0.)
                self.assertEqual(ns['_bookmark_run_times'](good, 'a', *nominal), nominal)
                missed = SimpleNamespace(mark_time=lambda _: 0., elapsed=lambda: 1.)
                self.assertEqual(ns['_bookmark_run_times'](missed, 'a', *nominal), (1/fps,) * len(nominal))

    def test_entire_non_timing_source_AST_and_nine_voiceovers_are_exact(self):
        class Reverse(ast.NodeTransformer):
            def visit_FunctionDef(self, n):
                return None if n.name in {'_bookmark_run_times', '_bookmark_ladder_step'} else self.generic_visit(n)
            def visit_Assign(self, n):
                return None if any(isinstance(t, ast.Name) and t.id == 'intro_times' for t in n.targets) else self.generic_visit(n)
            def visit_Call(self, n):
                if isinstance(n.func, ast.Name) and n.func.id == '_bookmark_ladder_step':
                    return ast.Call(func=ast.Name(id='step', ctx=ast.Load()), args=[n.args[2]], keywords=[])
                if isinstance(n.func, ast.Attribute) and n.func.attr == 'play':
                    n.keywords = [k for k in n.keywords if not(k.arg == 'run_time' and isinstance(k.value, ast.Subscript)
                                  and isinstance(k.value.value, ast.Name) and k.value.value.id == 'intro_times')]
                return self.generic_visit(n)
        self.assertEqual(ast.dump(Reverse().visit(copy.deepcopy(tree())), include_attributes=False), ast.dump(tree(True), include_attributes=False))
        voices = lambda t: [ast.dump(n.args[0], include_attributes=False) for n in ast.walk(t)
                            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover']
        self.assertEqual(voices(tree()), voices(tree(True)))
        self.assertEqual(len(voices(tree())), 9)


if __name__ == '__main__':
    unittest.main()
