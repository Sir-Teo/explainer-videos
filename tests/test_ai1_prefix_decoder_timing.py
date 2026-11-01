"""Speech-word decoder regression: actual nested AST, tracker and installed timing APIs; no output I/O."""
import ast
import copy
from contextlib import contextmanager
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from types import SimpleNamespace
import types
import unittest

import numpy as np
import test_ai1_entropy_prefix_timing as timing

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'videos/ai/ai1/s05_prefix.py'
EVIDENCE = ROOT / 'docs/qa/evidence/ai1-entropy-prefix-narrated-timing-repair'
BEFORE = gzip.decompress((EVIDENCE / 'prefix-source-after.py.gz').read_bytes()).decode()
DIAGNOSTIC = timing.diagnostic('prefix')
BLOCK = DIAGNOSTIC['narration_blocks'][3]
KEY = '86a8352c7e3815ea'
ALIGNED = DIAGNOSTIC['per_utterance_word_alignment_and_duration'][KEY]
MARKS = [('c_right1', 3), ('c_right2', 4), ('c_left', 5), ('c_leaf', 6),
         ('a_left', 11), ('a_leaf', 12), ('b_right', 13), ('b_left', 14),
         ('b_leaf', 15), ('f_path', 16), ('f_leaf', 19)]
LEAF_TIMES = dict(c=3.29, a=6.14, b=7.86, f=10.13)


def decoder_block(tree):
    method = timing.function(tree, 'prefix')
    return next(n for n in ast.walk(method) if isinstance(n, ast.With)
                and ast.literal_eval(n.items[0].context_expr.args[0]).startswith('Watch it decode.'))


def source(before=False):
    return ast.parse(BEFORE if before else SOURCE.read_text())


def group_timing_class():
    path = Path(importlib.util.find_spec('manim').origin).parent / 'animation/composition.py'
    tree = ast.parse(path.read_text())
    cls = ast.ClassDef(name='InstalledGroupTiming', bases=[], keywords=[], decorator_list=[],
                      body=[timing.function(tree, n) for n in ['build_animations_with_timings', 'init_run_time']])
    return timing.compile_nodes([cls], dict(np=np), 'installed-AnimationGroup-timing')['InstalledGroupTiming']


class Animation:
    def __init__(self, kind, target=None, children=(), lag_ratio=0):
        self.kind, self.target, self.children = kind, target, list(children)
        self.run_time = 1.
        if self.children:
            self.timing = group_timing_class()()
            self.timing.animations, self.timing.lag_ratio = self.children, lag_ratio
            self.run_time = self.timing.init_run_time(None)
    def set_color(self, color):
        return self


class Object:
    def __init__(self, name):
        self.name = name
    def copy(self):
        return Object(self.name)
    def set_stroke(self, *args, **kwargs):
        return self
    @property
    def animate(self):
        return Animation('bit', self)


class Group:
    def __init__(self, *members):
        self.members = list(members)
    def __getitem__(self, index):
        return self.members[index]
    def __iter__(self):
        return iter(self.members)
    def add(self, *members):
        self.members.extend(members)
        return self
    def arrange(self, *args, **kwargs):
        return self
    def next_to(self, *args, **kwargs):
        return self


class DecoderClock(timing.Clock):
    def __init__(self, fps, phase):
        super().__init__(fps)
        self.phase, self.visible, self.calls, self._narration = phase, [], [], []
    def _add_narration(self, *args):
        # Controlled sub-frame arrival overhead, not a claim about the host renderer.
        self.renderer.time += self.phase / self.fps
    def play(self, *animations, run_time=1., **kwargs):
        start = self.renderer.time
        self.advance(run_time)
        end = self.renderer.time
        symbol = self.namespace.get('sym')
        def capture(animation, offset, duration):
            if animation.children:
                mx = animation.timing.max_end_time
                for child in animation.timing.anims_with_timings:
                    capture(child['anim'], offset + duration * child['start'] / mx,
                            duration * (child['end'] - child['start']) / mx)
            elif animation.kind in {'letter', 'edge', 'bit'}:
                # First positive-alpha frame and first fully settled frame/hold.
                onset = start + (int(np.floor(offset * self.fps + 1e-10)) + 1) / self.fps
                settled = start + np.ceil((offset + duration) * self.fps - 1e-10) / self.fps
                self.visible.append(dict(kind=animation.kind, target=animation.target.name, symbol=symbol,
                                         reveal_call_start=start + offset, visible_onset=float(onset),
                                         fully_visible=float(settled)))
        for animation in animations:
            capture(animation, 0., run_time)
        self.calls.append(dict(symbol=symbol, start=start, end=end, requested=run_time,
                               top_kinds=[a.kind for a in animations]))


def run_decoder(fps=60, phase=0., before=False):
    tree = source(before)
    small = next(ast.literal_eval(n.value) for n in tree.body
                 if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SMALL' for t in n.targets))
    scene = DecoderClock(fps, phase)
    voice = ast.parse((ROOT / 'explainer/voiceover.py').read_text())
    language = ast.parse((ROOT / 'explainer/lang.py').read_text())
    english = timing.compile_nodes([timing.function(language, n) for n in ['clean', 'tokens']],
                                   dict(re=re, LANG='en'), 'real-English-cleaning')
    utterance = SimpleNamespace(duration=ALIGNED['duration'], audio_path='not-opened',
                                words=[SimpleNamespace(text=w, start=s, end=e) for w, s, e in ALIGNED['tokens']])
    def metadata_only(clean):
        assert clean == BLOCK['text']
        return utterance
    scope = dict(contextmanager=contextmanager, re=re, Path=Path,
                 inspect=SimpleNamespace(getfile=lambda _: str(SOURCE)), _BOOKMARK=timing.MARK,
                 lang=SimpleNamespace(LANG='en', clean=english['clean'], tokens=english['tokens'],
                                      translate=lambda text, *_: text),
                 tts=SimpleNamespace(synthesize=metadata_only))
    tracker = next(n for n in voice.body if isinstance(n, ast.ClassDef) and n.name == 'VoiceoverTracker')
    timing.compile_nodes([timing.function(voice, '_strip_bookmarks'), tracker,
                          timing.function(voice, 'voiceover')], scope, 'actual-Voiceover-context-and-tracker')
    scene.voiceover = types.MethodType(scope['voiceover'], scene)
    bits = Group(*[Object('bit/' + str(i)) for i in range(sum(len(small[x]) for x in 'cabf'))])
    edges = {code[:i]: Object('edge/' + code[:i]) for code in small.values() for i in range(1, len(code) + 1)}
    scope.update(self=scene, config=SimpleNamespace(frame_rate=fps), SMALL=small, VGroup=Group,
                 tree=SimpleNamespace(edges=edges, leaves={x: Object('leaf/' + x) for x in small}),
                 bits=bits, out=Group(), WHITE='white', RIGHT='right', C=SimpleNamespace(TRUE_P='true'),
                 letter=lambda sym, **kw: Object('letter/' + sym),
                 Create=lambda obj: Animation('edge', obj),
                 FadeIn=lambda obj: Animation('letter' if isinstance(obj, Object) and obj.name.startswith('letter/') else 'bits', obj),
                 FadeOut=lambda obj: Animation('clear', obj), Indicate=lambda obj, **kw: Animation('pulse', obj),
                 AnimationGroup=lambda *children: Animation('group', children=children),
                 LaggedStart=lambda *children, lag_ratio: Animation('lagged', children=children, lag_ratio=lag_ratio))
    scene.namespace = scope
    helpers = [n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name in {'_bookmark_run_times', '_decoder_wait_until'}]
    timing.compile_nodes(helpers + [decoder_block(tree)], scope, 'actual-nested-Prefix-decoder-AST')
    return scene, scope


class PrefixDecoderTiming(unittest.TestCase):
    def test_same_verified_old_decoder_ast_words_and_conditional_master_identity(self):
        old_production = timing.source_tree('prefix', before=True)
        self.assertEqual(ast.dump(decoder_block(old_production), include_attributes=False),
                         ast.dump(decoder_block(source(True)), include_attributes=False))
        new_raw = ast.literal_eval(decoder_block(source()).items[0].context_expr.args[0])
        self.assertEqual(timing.MARK.sub('', new_raw), BLOCK['raw'])
        self.assertEqual(len(ALIGNED['tokens']), 23)
        self.assertEqual(timing.MARK.findall(new_raw), [m for m, _ in MARKS])
        clock, scope = run_decoder()
        _, indices = scope['_strip_bookmarks'](new_raw)
        self.assertEqual(list(indices.items()), MARKS)
        master = next(m for m in DIAGNOSTIC['speech_masters'] if m['key'] == KEY)
        self.assertEqual(master['bytes'], 1189520)
        self.assertEqual(master['sha256'], '099dffe6f458b46652cecea65727f19d16191a1e99107085fb158b546834488f')
        self.assertEqual(ALIGNED['duration'], 12.39)

    def test_original_nested_loop_reproduces_early_complete_prefixes(self):
        scene, _ = run_decoder(before=True)
        letters = [e for e in scene.visible if e['kind'] == 'letter']
        self.assertEqual(''.join(e['symbol'] for e in letters if e['fully_visible'] <= 5.75), 'cab')
        self.assertEqual(''.join(e['symbol'] for e in letters if e['fully_visible'] <= 7.76), 'cabf')
        self.assertTrue(all(e['fully_visible'] < LEAF_TIMES[e['symbol']] for e in letters))

    def test_word_anchored_visible_onsets_completions_and_retained_reading_time(self):
        for fps in [15, 30, 60]:
            for phase in [0., .49, 1.]:
                with self.subTest(fps=fps, phase=phase):
                    scene, _ = run_decoder(fps, phase)
                    letters = [e for e in scene.visible if e['kind'] == 'letter']
                    self.assertEqual([e['symbol'] for e in letters], list('cabf'))
                    for event in letters:
                        cue = LEAF_TIMES[event['symbol']]
                        self.assertGreaterEqual(event['reveal_call_start'], cue - 1e-10)
                        self.assertGreater(event['visible_onset'], cue - 1e-10)
                        self.assertGreaterEqual(event['fully_visible'], cue + .6 - 1e-10)
                        self.assertLessEqual(event['fully_visible'], cue + .6 + 2/fps + 1e-9)
                        self.assertGreaterEqual(ALIGNED['duration'] - event['fully_visible'], 1.5)
                    self.assertEqual(''.join(e['symbol'] for e in letters if e['fully_visible'] <= 5.75), 'c')
                    self.assertEqual(''.join(e['symbol'] for e in letters if e['fully_visible'] <= 7.75), 'ca')

    def test_direction_edges_bits_and_five_edge_phrase_remain_in_code_order(self):
        for fps in [15, 30, 60]:
            for phase in [0., .49, 1.]:
                scene, scope = run_decoder(fps, phase)
                edges = [e for e in scene.visible if e['kind'] == 'edge']
                bits = [e for e in scene.visible if e['kind'] == 'bit']
                self.assertEqual([e['target'] for e in bits], ['bit/' + str(i) for i in range(11)])
                self.assertEqual([e['target'] for e in edges],
                                 ['edge/' + scope['SMALL'][sym][:i] for sym in 'cabf'
                                  for i in range(1, len(scope['SMALL'][sym]) + 1)])
                starts = {'c': [1.37, 2.01, 2.65], 'a': [5.26], 'b': [6.82, 7.30]}
                ends = {'c': [2.01, 2.65, 3.29], 'a': [6.14], 'b': [7.30, 7.86]}
                for sym in 'cab':
                    found = [e for e in edges if e['symbol'] == sym]
                    for event, begin, end in zip(found, starts[sym], ends[sym]):
                        self.assertGreaterEqual(event['reveal_call_start'], begin - 1e-10)
                        self.assertLessEqual(event['fully_visible'], end - 1/fps + 1e-9)
                five = [e for e in edges if e['symbol'] == 'f']
                self.assertEqual(len(five), 5)
                self.assertTrue(all(a['visible_onset'] < b['visible_onset'] for a, b in zip(five, five[1:])))
                self.assertGreaterEqual(five[0]['reveal_call_start'], 8.53 - 1e-10)
                self.assertLessEqual(five[-1]['fully_visible'], 10.13 - 1/fps + 1e-9)

    def test_exact_word_wait_fixes_real_tracker_sub_sixtieth_early_return(self):
        helper = timing.function(source(), '_decoder_wait_until')
        for fps in [15, 30, 60]:
            scene = DecoderClock(fps, 0.)
            scene.renderer.time = 1. - .01
            tracker = SimpleNamespace(mark_time=lambda _: 1., elapsed=lambda: scene.renderer.time)
            # RealTracker.wait_until has a1/60 threshold; demonstrate the late fix
            # is needed rather than merely calling that method at the new marks.
            d = timing.actual_tracker(BLOCK, DIAGNOSTIC['exact_narration_occurrences'][3], ALIGNED, scene)
            d.mark_time = lambda _: 1.
            d.wait_until('cue')
            self.assertLess(scene.renderer.time, 1.)
            ns = timing.compile_nodes([helper], {}, 'actual-exact-word-wait')
            ns['_decoder_wait_until'](scene, tracker, 'cue')
            self.assertGreaterEqual(scene.renderer.time, 1.)
            self.assertLessEqual(scene.renderer.time, 1. + 1/fps)
            scene.renderer.time = 2.
            ns['_decoder_wait_until'](scene, tracker, 'cue')
            self.assertEqual(scene.renderer.time, 2.)  # Already late cannot become synchronized.

    def test_only_owned_decoder_span_and_wait_helper_change_geometry_stays_exact(self):
        old, new = source(True), source()
        old_block, new_block = decoder_block(old), decoder_block(new)
        # Outside the complete newly tested decoder With and its tiny exact-wait
        # helper, the entire module (including McMillan repair) must stay exact.
        class Normalize(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                return None if node.name == '_decoder_wait_until' else self.generic_visit(node)
            def visit_With(self, node):
                if node is new_block:
                    return copy.deepcopy(old_block)
                return self.generic_visit(node)
        self.assertEqual(ast.dump(Normalize().visit(new), include_attributes=False),
                         ast.dump(old, include_attributes=False))
        old_loop = next(n for n in old_block.body if isinstance(n, ast.For))
        new_loop = next(n for n in new_block.body if isinstance(n, ast.For))
        self.assertEqual(ast.dump(old_loop.iter), ast.dump(new_loop.iter))
        assignments = lambda loop, name: next(n for n in loop.body if isinstance(n, ast.Assign)
                                             and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
        for name in ['c', 'path', 'o']:
            self.assertEqual(ast.dump(assignments(old_loop, name)), ast.dump(assignments(new_loop, name)))
        leaf_play = lambda loop: next(n for n in loop.body if isinstance(n, ast.Expr)
                                     and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
                                     and n.value.func.attr == 'play' and isinstance(n.value.args[0], ast.Call)
                                     and isinstance(n.value.args[0].func, ast.Name)
                                     and n.value.args[0].func.id == 'FadeIn')
        self.assertEqual(ast.dump(leaf_play(old_loop)), ast.dump(leaf_play(new_loop)))
        self.assertEqual(ast.dump(old_loop.body[-1]), ast.dump(new_loop.body[-1]))


if __name__ == '__main__':
    unittest.main()
