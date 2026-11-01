"""Actual cached-word cue timing with installed frame progression, no scenes or audio I/O."""
import ast
import copy
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import re
from types import SimpleNamespace
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/qa/evidence/ai1-entropy-prefix-narrated-timing-repair'
MARK = re.compile(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>")
CASES = {
    'entropy': ('s04_entropy.py', '8206578d645fdeb4bfcea0e790f306d1ad7bb2e2ff279fbc338357d4843a570c',
                85346, 'f25fa6d23e03bac6ac9d8dfe99bcffd23d0eee7d1e640bf0f53216b262394b9c'),
    'prefix': ('s05_prefix.py', 'f04891be193facd72a452da6883c8903d9b74b922925c18c6db2d5fc7035049d',
               117579, 'cd2d5105756b7a202c936c459f35e1b15460817fa1edfd0339c778969eaa234c'),
}
SPECS = [('entropy', 'coin', 3, None, 'a', None),
         ('entropy', 'uniqueness', 6, 'd', 'e', 4),
         ('prefix', 'mcmillan', 6, 'd', 'e', 1)]


def diagnostic(name):
    return json.loads(gzip.decompress((EVIDENCE / (name + '-exact-diagnostic.json.gz')).read_bytes()))


def source_tree(name, before=False):
    raw = (gzip.decompress((EVIDENCE / (name + '-source-before.py.gz')).read_bytes()).decode()
           if before else (ROOT / 'videos/ai/ai1' / CASES[name][0]).read_text())
    return ast.parse(raw)


def function(tree, name):
    return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)


def compile_nodes(nodes, scope, label):
    future = ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0)
    exec(compile(ast.fix_missing_locations(ast.Module([future] + copy.deepcopy(nodes), type_ignores=[])),
                 label, 'exec'), scope)
    return scope


def actual_tracker(block, occurrence, aligned, scene):
    """Execute the real English token cleanup and tracker, using only supplied word metadata."""
    language = ast.parse((ROOT / 'explainer/lang.py').read_text())
    ns = dict(re=re, LANG='en')
    compile_nodes([function(language, 'tokens'), function(language, 'clean')], ns, 'actual-English-token-cleanup')
    voice = ast.parse((ROOT / 'explainer/voiceover.py').read_text())
    scope = dict(re=re, _BOOKMARK=MARK, lang=SimpleNamespace(clean=ns['clean'], tokens=ns['tokens']))
    tracker = next(n for n in voice.body if isinstance(n, ast.ClassDef) and n.name == 'VoiceoverTracker')
    compile_nodes([function(voice, '_strip_bookmarks'), tracker], scope, 'actual-cached-word-tracker')
    clean, indices = scope['_strip_bookmarks'](block['raw'])
    assert clean == block['text'] == occurrence['text'] == aligned['text']
    words = [SimpleNamespace(text=w, start=s, end=e) for w, s, e in aligned['tokens']]
    return scope['VoiceoverTracker'](scene, SimpleNamespace(duration=aligned['duration'], words=words), indices, 0.)


def installed_quantizer(fps):
    scene_path = Path(importlib.util.find_spec('manim').origin).parent / 'scene/scene.py'
    tree = ast.parse(scene_path.read_text())
    nodes = [function(tree, name) for name in ['get_time_progression', 'validate_run_time']]
    cls = ast.ClassDef(name='InstalledQuantizer', bases=[], keywords=[], body=nodes, decorator_list=[])
    class Config(dict):
        __getattr__ = dict.__getitem__
    scope = dict(np=np, config=Config(frame_rate=fps, progress_bar='none'),
                 tqdm=lambda values, **kw: values, platform=platform,
                 logger=SimpleNamespace(warning=lambda *a, **kw: None))
    compile_nodes([cls], scope, 'installed-Manim-frame-functions')
    q = scope['InstalledQuantizer']()
    q.renderer = SimpleNamespace(skip_animations=False)
    return q


class Shape:
    """Only the layout interface used by the actual shared ladder; no camera/animation execution."""
    def __init__(self, name, y=0.):
        self.name, self.y, self.height = name, y, .5
    @property
    def animate(self):
        return self
    def set_y(self, value):
        self.y = value
        return self
    def get_y(self):
        return self.y
    def copy(self):
        return Shape(self.name + '-copy', self.y)
    def set_color(self, value):
        return self


def tag(value):
    if isinstance(value, Shape):
        return value.name
    if isinstance(value, np.ndarray):
        return tag(value.tolist())
    if isinstance(value, (list, tuple)):
        return tuple(tag(v) for v in value)
    if isinstance(value, dict):
        return {k: tag(v) for k, v in value.items()}
    return value


class Clock:
    def __init__(self, fps, rounded=True):
        self.renderer = SimpleNamespace(time=0.)
        self.fps, self.rounded, self.quantizer = fps, rounded, installed_quantizer(fps)
        self.events = []
    def advance(self, seconds):
        if self.rounded:
            seconds = self.quantizer.validate_run_time(seconds, self.advance)
            self.renderer.time += len(self.quantizer.get_time_progression(seconds, 'no-output fixture')) / self.fps
        else:
            self.renderer.time += seconds
    def play(self, *animations, run_time=None, **kwargs):
        if run_time is None:
            # The long literal coin formula has an observed installed Write default of2s;
            # Create/FadeIn default to1s. A separate bounded real-Mobject proof records this.
            run_time = 2. if any(a[0] == 'Write' and a[1] == ('coin-formula',) for a in animations) else 1.
        start = self.renderer.time
        self.advance(run_time)
        self.events.append(dict(args=tag(animations), kwargs=tag(kwargs), requested=run_time,
                                start=start, end=self.renderer.time))
    def wait(self, seconds):
        self.advance(seconds)


def actual_ladder_step(scene):
    shared = ast.parse((ROOT / 'explainer/analysis/__init__.py').read_text())
    step = function(function(shared, 'ladder'), 'step')
    rows = [Shape('row' + str(i)) for i in range(6)]
    whys = [Shape('why' + str(i)) for i in range(6)]
    ns = dict(scene=scene, rows=rows, whys=whys, keep=3, top=2.4, buff=.5,
              extra=[0.] * 6, offs=[0.] * 6, UP=np.array([0., 1., 0.]), highlight=True,
              changed_parts=lambda old, new: [Shape('changed-' + new.name)], C=SimpleNamespace(EPS='yellow'))
    for name in ['FadeOut', 'FadeIn', 'Write', 'TransformMatchingTex', 'ShowPassingFlash']:
        ns[name] = lambda *args, _name=name, **kw: (_name, tag(args), tag(kw))
    ns['Underline'] = lambda m, **kw: Shape('underline-' + m.name)
    compile_nodes([step], ns, 'actual-shared-ladder-step')
    return ns['step']


def span(spec, fps, phase=0., before=False, rounded=True):
    name, method, block_index, start_mark, end_mark, step_index = spec
    d = diagnostic(name)
    block = d['narration_blocks'][block_index]
    occurrence = d['exact_narration_occurrences'][block_index]
    aligned = d['per_utterance_word_alignment_and_duration'][occurrence['key']]
    scene = Clock(fps, rounded)
    vo = actual_tracker(block, occurrence, aligned, scene)
    scene.renderer.time = (vo.mark_time(start_mark) if start_mark else 0.) + phase / fps
    scope = dict(config=SimpleNamespace(frame_rate=fps), self=scene, vo=vo, step=actual_ladder_step(scene))
    for key in ['f', 'ax', 'xl', 'yl', 'axl', 'curve']:
        scope[key] = 'coin-formula' if key == 'f' else key
    for key in ['Write', 'Create', 'FadeIn']:
        scope[key] = lambda *args, _key=key, **kw: (_key, tag(args), tag(kw))
    tree = source_tree(name, before)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name in {'_bookmark_run_times', '_bookmark_ladder_step'}]
    body = next(n for n in ast.walk(function(tree, method)) if isinstance(n, ast.With)).body
    def wait(node, mark):
        return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == 'wait_until'
                and node.value.args[0].value == mark)
    first = next(i for i, n in enumerate(body) if wait(n, start_mark)) + 1 if start_mark else 0
    last = next(i for i, n in enumerate(body) if wait(n, end_mark))
    compile_nodes(nodes + body[first:last], scope, 'actual-Entropy-Prefix-cue-span')
    return scene, vo, scope, aligned


class EntropyPrefixTiming(unittest.TestCase):
    def test_exact_diagnostics_word_targets_and_provided_master_metadata(self):
        for name, (_, before_sha, size, expected) in CASES.items():
            raw = gzip.decompress((EVIDENCE / (name + '-exact-diagnostic.json.gz')).read_bytes())
            self.assertEqual((len(raw), hashlib.sha256(raw).hexdigest()), (size, expected))
            d = json.loads(raw)
            before = gzip.decompress((EVIDENCE / (name + '-source-before.py.gz')).read_bytes())
            self.assertEqual(hashlib.sha256(before).hexdigest(), before_sha)
            self.assertEqual(d['source_sha256'], before_sha)
            n = 11 if name == 'entropy' else 8
            self.assertEqual(len(d['narration_blocks']), n)
            self.assertEqual(len(d['exact_narration_occurrences']), n)
            by_start = {}
            durations = []
            for block, occurrence in zip(d['narration_blocks'], d['exact_narration_occurrences']):
                aligned = d['per_utterance_word_alignment_and_duration'][occurrence['key']]
                vo = actual_tracker(block, occurrence, aligned, Clock(60))
                self.assertEqual(vo.duration, block['duration'])
                by_start[round(block['start'], 8)] = (block, vo)
                durations.append(vo.duration)
            self.assertEqual(len(d['all_bookmark_requests']), 28 if name == 'entropy' else 19)
            for request in d['all_bookmark_requests']:
                block, vo = by_start[round(request['block_start'], 8)]
                self.assertAlmostEqual(block['start'] + vo.mark_time(request['mark']), request['target_seconds'])
            if name == 'entropy':
                self.assertEqual(d['speech_masters']['utterances'], n)
                self.assertAlmostEqual(sum(durations), d['speech_masters']['native_speech_seconds'])
                self.assertRegex(d['speech_masters']['sha256'], r'^[0-9a-f]{64}$')
            else:
                self.assertEqual([m['key'] for m in d['speech_masters']],
                                 [m['key'] for m in d['exact_narration_occurrences']])
                for master in d['speech_masters']:
                    self.assertRegex(master['sha256'], r'^[0-9a-f]{64}$')

    def test_original_actual_spans_reproduce_three_reported_late_cues(self):
        for spec, late in zip(SPECS, [.96, 1.56, .11]):
            scene, vo, _, _ = span(spec, 100, before=True, rounded=False)
            self.assertAlmostEqual(scene.renderer.time - vo.mark_time(spec[4]), late, places=10)
            self.assertEqual([e['requested'] for e in scene.events],
                             [2., 1.] if spec[1] == 'coin' else [.6, 1.2, .8])

    def test_adaptive_actual_calls_fit_with_installed_frame_rounding_and_adverse_phase(self):
        for spec in SPECS:
            for fps in [15, 30, 60]:
                for phase in [0, .49, 1]:
                    with self.subTest(spec=spec, fps=fps, phase=phase):
                        scene, vo, _, _ = span(spec, fps, phase)
                        self.assertLessEqual(scene.renderer.time, vo.mark_time(spec[4]) - 1/fps + 1e-10)
                        self.assertTrue(all(e['requested'] >= 1/fps for e in scene.events))
                        old, _, _, _ = span(spec, fps, phase, before=True)
                        self.assertEqual([e['args'] for e in scene.events], [e['args'] for e in old.events])
                        self.assertEqual([e['kwargs'] for e in scene.events], [e['kwargs'] for e in old.events])
                        self.assertNotIn('play', scene.__dict__)

    def test_retained_settled_formula_and_coin_states_have_reading_time(self):
        for spec in SPECS:
            for fps in [15, 30, 60]:
                for phase in [0, .49, 1]:
                    scene, vo, scope, aligned = span(spec, fps, phase)
                    vo.wait_until(spec[4])
                    if spec[1] == 'coin':
                        # Fair-coin inset is unchanged until the next spoken cue.
                        self.assertGreaterEqual(vo.mark_time('b') - scene.renderer.time, 1.5)
                    else:
                        # Actual helper's next step retains the preceding row; even
                        # its final new formula has >=1.5s residual speech afterward.
                        current = spec[5]
                        self.assertIn(current, range(max(0, current + 1 - 3 + 1), current + 1))
                        scope['step'](current + 1)
                        self.assertGreaterEqual(aligned['duration'] - scene.renderer.time, 1.5)

    def test_ladder_adapter_restores_class_and_instance_play_on_success_and_exception(self):
        for name in CASES:
            tree = source_tree(name)
            nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                     and n.name in {'_bookmark_run_times', '_bookmark_ladder_step'}]
            for override in [False, True]:
                for failing in [False, True]:
                    scene = Clock(60)
                    marker = object()
                    if override:
                        original = lambda *a, **kw: scene.events.append((a, kw))
                        scene.play = original
                    else:
                        original = scene.play
                    vo = SimpleNamespace(mark_time=lambda _: 10., elapsed=lambda: 0.)
                    scope = compile_nodes(nodes, dict(config=SimpleNamespace(frame_rate=60)), 'actual-adapter')
                    def step(index):
                        self.assertEqual(index, 4)
                        for i in range(3):
                            scene.play(('stage', i), run_time=[.6, 1.2, .8][i], marker=marker)
                            if failing:
                                raise RuntimeError('expected fixture interruption')
                        return marker
                    if failing:
                        with self.assertRaisesRegex(RuntimeError, 'fixture interruption'):
                            scope['_bookmark_ladder_step'](scene, step, 4, vo, 'e')
                    else:
                        self.assertIs(scope['_bookmark_ladder_step'](scene, step, 4, vo, 'e'), marker)
                    if override:
                        self.assertIs(scene.play, original)
                        self.assertTrue(all(event[1]['marker'] is marker for event in scene.events))
                    else:
                        self.assertNotIn('play', scene.__dict__)
                        self.assertIs(scene.play.__func__, original.__func__)

    def test_generous_and_physically_impossible_cues_are_not_conflated(self):
        for name in CASES:
            helper = function(source_tree(name), '_bookmark_run_times')
            for fps in [15, 30, 60]:
                ns = compile_nodes([helper], dict(config=SimpleNamespace(frame_rate=fps)), 'actual-budget')
                good = SimpleNamespace(mark_time=lambda _: 30., elapsed=lambda: 0.)
                self.assertEqual(ns['_bookmark_run_times'](good, 'a', .6, 1.2, .8), (.6, 1.2, .8))
                late = SimpleNamespace(mark_time=lambda _: 0., elapsed=lambda: 1.)
                times = ns['_bookmark_run_times'](late, 'a', .6, 1.2, .8)
                self.assertEqual(times, (1/fps,) * 3)
                self.assertGreater(1. + sum(times), late.mark_time('a'))

    def test_entire_source_preserves_all_non_timing_AST_and_voiceovers(self):
        for name in CASES:
            old, new = source_tree(name, True), source_tree(name)
            # The separately covered word-anchored decoder replaces exactly one
            # With block. Keep this original v8 timing guard strict everywhere else.
            if name == 'prefix':
                def decoder(tree):
                    return next(n for n in ast.walk(tree) if isinstance(n, ast.With)
                                and isinstance(n.items[0].context_expr, ast.Call)
                                and isinstance(n.items[0].context_expr.func, ast.Attribute)
                                and n.items[0].context_expr.func.attr == 'voiceover'
                                and isinstance(n.items[0].context_expr.args[0], ast.Constant)
                                and n.items[0].context_expr.args[0].value.startswith('Watch it decode.'))
                old_decoder, new_decoder = decoder(old), decoder(new)
                self.assertEqual(MARK.sub('', new_decoder.items[0].context_expr.args[0].value),
                                 old_decoder.items[0].context_expr.args[0].value)
                class RestoreOnlyDecoder(ast.NodeTransformer):
                    def visit_FunctionDef(self, node):
                        return None if node.name == '_decoder_wait_until' else self.generic_visit(node)
                    def visit_With(self, node):
                        return copy.deepcopy(old_decoder) if node is new_decoder else self.generic_visit(node)
                new = RestoreOnlyDecoder().visit(new)
            class RemoveOnlyOwnedTiming(ast.NodeTransformer):
                def visit_FunctionDef(self, node):
                    if node.name in {'_bookmark_run_times', '_bookmark_ladder_step'}:
                        return None
                    return self.generic_visit(node)
                def visit_Assign(self, node):
                    if (len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                            and node.targets[0].id == 'coin_times'):
                        self_outer.assertEqual(ast.unparse(node.value), "_bookmark_run_times(vo, 'a', 2.0, 1.0)")
                        return None
                    return self.generic_visit(node)
                def visit_Call(self, node):
                    if isinstance(node.func, ast.Name) and node.func.id == '_bookmark_ladder_step':
                        self_outer.assertEqual([ast.unparse(a) for a in node.args[:2]], ['self', 'step'])
                        self_outer.assertEqual(ast.unparse(node.args[3]), 'vo')
                        self_outer.assertEqual(ast.literal_eval(node.args[4]), 'e')
                        self_outer.assertEqual(ast.literal_eval(node.args[2]), 4 if name == 'entropy' else 1)
                        return ast.copy_location(ast.Call(func=ast.Name(id='step', ctx=ast.Load()),
                                                         args=[node.args[2]], keywords=[]), node)
                    if isinstance(node.func, ast.Attribute) and node.func.attr == 'play':
                        kept = []
                        for k in node.keywords:
                            if (k.arg == 'run_time' and isinstance(k.value, ast.Subscript)
                                    and isinstance(k.value.value, ast.Name) and k.value.value.id == 'coin_times'):
                                self_outer.assertIn(ast.literal_eval(k.value.slice), [0, 1])
                            else:
                                kept.append(k)
                        node.keywords = kept
                    return self.generic_visit(node)
            self_outer = self
            self.assertEqual(ast.dump(RemoveOnlyOwnedTiming().visit(copy.deepcopy(new)), include_attributes=False),
                             ast.dump(old, include_attributes=False))
            voices = lambda t: [ast.dump(n.args[0], include_attributes=False) for n in ast.walk(t)
                                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                                and n.func.attr == 'voiceover']
            self.assertEqual(voices(old), voices(new))
            self.assertEqual(len(voices(new)), 11 if name == 'entropy' else 8)


if __name__ == '__main__':
    unittest.main()
