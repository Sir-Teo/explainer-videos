"""Actual cached-speech cue budgets, without models, audio writes or renders."""
import ast
import copy
from contextlib import contextmanager
from functools import lru_cache
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import re
from types import SimpleNamespace
import types
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/qa/evidence/ai1-probability-narrated-timing-repair"
SOURCE = ROOT / "videos/ai/ai1/s02_probability.py"
DIAGNOSTIC = json.loads(gzip.decompress((EVIDENCE / "readable-diagnostic.json.gz").read_bytes()))
BEFORE = gzip.decompress((EVIDENCE / "source-before.py.gz").read_bytes()).decode()
MARK = re.compile(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>")


def marks(block):
    """The English tracker uses whitespace tokens, with marks removed first."""
    result = {}
    for match in MARK.finditer(block["raw"]):
        prefix = MARK.sub("", block["raw"][:match.start()])
        index = len(prefix.split())
        result[match[1]] = block["words"][index][1] - block["start"]
    return result


def actual_span(tree, name, block_index, start_mark, end_mark):
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)
    blocks = [n for n in ast.walk(method) if isinstance(n, ast.With)]
    body = blocks[block_index].body
    def is_wait(node, mark):
        return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "wait_until"
                and node.value.args[0].value == mark)
    first = next(i for i, n in enumerate(body) if is_wait(n, start_mark)) + 1 if start_mark else 0
    last = next(i for i, n in enumerate(body) if is_wait(n, end_mark))
    return body[first:last]


def run_span(tree, spec, fps, phase=0):
    name, local_block, global_block, start_mark, end_mark, expected = spec
    block = DIAGNOSTIC["schedule-report.json"]["narration"][global_block]
    cue = marks(block)
    now = [(cue[start_mark] if start_mark else 0) + phase / fps]
    events = []
    def play(*args, run_time=1):
        events.append(("play", args, run_time))
        now[0] += math.ceil(run_time * fps - 1e-10) / fps
    def morph(scene, a, b, run_time=1.4):
        events.append(("morph", (a, b), run_time))
        now[0] += math.ceil(run_time * fps - 1e-10) / fps
    scope = {"config": SimpleNamespace(frame_rate=fps), "vo": SimpleNamespace(
        elapsed=lambda: now[0], mark_time=lambda mark: cue[mark]),
        "self": SimpleNamespace(play=play), "morph": morph,
        "g": SimpleNamespace(bars=list(range(27)), labels="labels"), "DOWN": "DOWN",
        "books": "books", "more": "more", "eqs": list(range(4)), "out": ["out"], "hi": 0,
        "pt": [0, 1, 2]}
    for key in ["names", "b_h", "b_h_l", "cell3", "rays3", "c3l", "b3", "b3_l", "cells",
                "lit_cell", "b_w", "num", "head", "box"]:
        scope[key] = key
    for key in ["FadeIn", "FadeOut", "LaggedStart", "GrowFromEdge", "GrowFromCenter",
                "TransformFromCopy", "Create", "VGroup"]:
        scope[key] = lambda *args, _key=key, **kw: (_key, args, kw)
    helper = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_bookmark_run_times"]
    nodes = helper + actual_span(tree, name, local_block, start_mark, end_mark)
    exec(compile(ast.Module(nodes, type_ignores=[]), "actual-probability-span", "exec"), scope)
    return now[0], cue[end_mark], events


SPECS = [
    ("frequencies", 0, 1, "a", "b", ["play"]),
    ("chain_rule", 0, 6, "b", "c", ["play", "morph", "play", "play"]),
    ("chain_rule", 1, 7, None, "a", ["play", "morph", "play"]),
]


@lru_cache(maxsize=1)
def reading_hold_sources():
    """Read installed timing rules without importing/rendering Manim scenes."""
    package = Path(importlib.util.find_spec("manim").origin).parent
    scene = ast.parse((package / "scene/scene.py").read_text())
    creation = ast.parse((package / "animation/creation.py").read_text())
    voiceover = ast.parse((ROOT / "explainer/voiceover.py").read_text())
    write = next(n for n in creation.body if isinstance(n, ast.ClassDef) and n.name == "Write")
    find = lambda tree, name: next(n for n in ast.walk(tree)
                                   if isinstance(n, ast.FunctionDef) and n.name == name)
    return (find(scene, "get_time_progression"), find(scene, "validate_run_time"),
            find(write, "_set_default_config_from_length"), find(voiceover, "voiceover"),
            find(voiceover, "_strip_bookmarks"), next(n for n in voiceover.body
                if isinstance(n, ast.ClassDef) and n.name == "VoiceoverTracker"))


def reading_hold_case(fps, phase, *, apply_hold=True, residual_audio=None):
    """Run the actual post-c numeric reveal/context exit/hold on cached speech.

    Animation geometry is mocked. Frame progression/minimum durations and
    voiceover exit are installed source, not a renderer or speech provider.
    Synthetic longer speech tests residual credit; it is not observed Chinese.
    """
    from explainer import lang
    progression, validate, write_default, context, strip, tracker = reading_hold_sources()
    cfg = type("Config", (dict,), {"__getattr__": dict.__getitem__})(frame_rate=fps, progress_bar="none")
    env = {"np": np, "config": cfg, "tqdm": lambda times, **kw: times,
           "platform": platform, "logger": SimpleNamespace(warning=lambda *a: None)}
    quantizer = ast.ClassDef(name="Quantizer", bases=[], keywords=[], decorator_list=[],
                            body=copy.deepcopy([progression, validate, write_default]))
    future = ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)
    exec(compile(ast.fix_missing_locations(ast.Module([future, quantizer], type_ignores=[])),
                 "installed-frame-timing", "exec"), env)
    quant = env["Quantizer"]()
    quant.renderer = SimpleNamespace(skip_animations=False)
    # Actual cached numeric-constructor fixture has 31 point-bearing members;
    # see ai1-probability-numeric-dwell-source-repair/write-defaults.json.gz.
    write_time, _ = quant._set_default_config_from_length(
        SimpleNamespace(family_members_with_points=lambda: [None] * 31), None, None)
    tree = ast.parse(SOURCE.read_text())
    chain = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "chain_rule")
    block = next(n for n in chain.body if isinstance(n, ast.With))
    last_cue = next(i for i, n in enumerate(block.body)
                    if isinstance(n, ast.Expr) and ast.unparse(n) == "vo.wait_until('c')")
    tail = copy.deepcopy(block.body[last_cue + 1:])
    hold = copy.deepcopy([n for n in chain.body
        if (isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == "num_hold_remaining")
        or (isinstance(n, ast.If) and ast.unparse(n.test) == "num_hold_remaining > 0")])
    cached = DIAGNOSTIC["schedule-report.json"]["narration"][6]
    cue = marks(cached)["c"]
    scene = SimpleNamespace(renderer=SimpleNamespace(time=0.0), _narration=[])
    def advance(duration):
        duration = quant.validate_run_time(duration, advance)
        scene.renderer.time += len(quant.get_time_progression(duration, "no-render")) / fps
    scene.wait = advance
    finished = []
    def play(*args, **kw):
        advance(kw.get("run_time", write_time))
        if any(a == ("Write", ("num",), {}) for a in args):
            finished.append(scene.renderer.time)
    scene.play = play
    scene._add_narration = lambda *a: None
    duration = cached["duration"]
    if residual_audio is not None:
        # Same frame-quantized post-c morph+Write completion as the actual tail.
        completion = cue + phase / fps
        for request in (1.2, write_time):
            completion += len(quant.get_time_progression(request, "no-render")) / fps
        duration = completion + residual_audio
    utterance = SimpleNamespace(duration=duration, audio_path="not-opened-existing-master",
        words=[SimpleNamespace(text=w, start=s-cached["start"], end=e-cached["start"])
               for w, s, e in cached["words"]])
    english = SimpleNamespace(clean=lambda s: lang.clean(s, "en"),
                              tokens=lambda s: lang.tokens(s, "en"),
                              translate=lambda s, *_: s)
    env.update(contextmanager=contextmanager, lang=english, Path=Path,
               inspect=SimpleNamespace(getfile=lambda _: str(SOURCE)),
               tts=SimpleNamespace(synthesize=lambda _: utterance), _BOOKMARK=MARK)
    exec(compile(ast.fix_missing_locations(ast.Module(
        [copy.deepcopy(future), copy.deepcopy(strip), copy.deepcopy(tracker), copy.deepcopy(context)],
        type_ignores=[])), "actual-voiceover-cached-metadata", "exec"), env)
    scene.voiceover = types.MethodType(env["voiceover"], scene)
    env.update(self=scene, eqs=[0, 1, 2, 3], num="num",
               Write=lambda *a, **kw: ("Write", a, kw),
               morph=lambda self, *a, run_time=1.4, **kw: advance(run_time))
    with scene.voiceover(cached["raw"]):
        scene.renderer.time = cue + phase / fps
        exec(compile(ast.fix_missing_locations(ast.Module(tail, type_ignores=[])),
                     "actual-numeric-reveal-tail", "exec"), env)
    assert len(finished) == 1
    existing = scene.renderer.time - finished[0]
    before = scene.renderer.time
    if apply_hold:
        exec(compile(ast.fix_missing_locations(ast.Module(hold, type_ignores=[])),
                     "actual-adaptive-reading-hold", "exec"), env)
    return existing, scene.renderer.time-finished[0], scene.renderer.time-before


class ProbabilityTiming(unittest.TestCase):
    def test_verified_diagnostic_source_and_all_eleven_masters(self):
        raw = gzip.decompress((EVIDENCE / "readable-diagnostic.json.gz").read_bytes())
        self.assertEqual(len(raw), 69858)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         "7f773060879f7b8c4b83262fd37bc207e462c6fda9a4c35389697aeb5f8eee5e")
        self.assertEqual(hashlib.sha256(BEFORE.encode()).hexdigest(),
                         DIAGNOSTIC["source_snapshot"]["sha256"])
        blocks = DIAGNOSTIC["schedule-report.json"]["narration"]
        masters = DIAGNOSTIC["real-audio-ready.json"]["utterances"]
        self.assertEqual(len(blocks), 11)
        self.assertEqual(len(masters), 11)
        self.assertAlmostEqual(sum(m["duration"] for m in masters), 159.28)
        for block, master in zip(blocks, masters):
            self.assertEqual(block["text"], master["spoken"])
            self.assertEqual(block["duration"], master["duration"])
            self.assertRegex(master["float_master_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(sum(len(marks(b)) for b in blocks), 18)

    def test_old_actual_spans_reproduce_all_three_reported_overruns(self):
        tree = ast.parse(BEFORE)
        for spec, late in zip(SPECS, [.15, 1.94, .46]):
            end, cue, events = run_span(tree, spec, 100)
            self.assertAlmostEqual(end - cue, late, places=10)
            self.assertEqual([e[0] for e in events], spec[-1])

    def test_actual_scene_spans_fit_measured_cues_with_adverse_frame_phases(self):
        tree = ast.parse(SOURCE.read_text())
        for fps in [15, 30, 60]:
            for phase in [0, .49, 1]:
                for spec in SPECS:
                    with self.subTest(fps=fps, phase=phase, span=spec[0:4]):
                        end, cue, events = run_span(tree, spec, fps, phase)
                        self.assertLessEqual(end, cue - 1 / fps + 1e-10)
                        self.assertEqual([e[0] for e in events], spec[-1])
                        self.assertTrue(all(e[2] >= 1 / fps for e in events))
                        # Actual tightest chain step remains about half a second.
                        self.assertGreater(min(e[2] for e in events), .47)

    def test_generous_cues_keep_nominal_durations_and_unavoidable_gaps_stay_positive(self):
        tree = ast.parse(SOURCE.read_text())
        helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_bookmark_run_times")
        for fps in [15, 30, 60]:
            scope = {"config": SimpleNamespace(frame_rate=fps)}
            exec(compile(ast.Module([helper], type_ignores=[]), "actual-budget", "exec"), scope)
            fn = scope["_bookmark_run_times"]
            for preferred in [(2.5,), (1., 1.2, 1.3, 1.), (.8, 1.4, 1.)]:
                generous = SimpleNamespace(mark_time=lambda _: 30., elapsed=lambda: 0.)
                self.assertEqual(fn(generous, "cue", *preferred), preferred)
                missed = SimpleNamespace(mark_time=lambda _: 0., elapsed=lambda: 1.)
                self.assertEqual(fn(missed, "cue", *preferred), (1 / fps,) * len(preferred))

    def test_entire_scene_preserves_math_audio_bookmarks_and_reveal_order(self):
        class RemoveTiming(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                if node.name == "_bookmark_run_times":
                    return None
                previous = getattr(self, "method", None)
                self.method = node.name
                result = self.generic_visit(node)
                self.method = previous
                return result
            def visit_Assign(self, node):
                if (getattr(self, "method", None) == "chain_rule"
                        and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
                    expected = {
                        "num_readable_at": "num_readable_at = self.renderer.time",
                        "num_hold_remaining": "num_hold_remaining = 1.5 - (self.renderer.time - num_readable_at)",
                    }.get(node.targets[0].id)
                    if expected:
                        assert ast.dump(node) == ast.dump(ast.parse(expected).body[0])
                        return None
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    if node.value.func.id == "_bookmark_run_times":
                        return None
                return self.generic_visit(node)
            def visit_If(self, node):
                if (getattr(self, "method", None) == "chain_rule"
                        and ast.unparse(node.test) == "num_hold_remaining > 0"):
                    expected = ast.parse("if num_hold_remaining > 0:\n    self.wait(num_hold_remaining)").body[0]
                    assert ast.dump(node) == ast.dump(expected)
                    return None
                return self.generic_visit(node)
            def visit_Call(self, node):
                if ((isinstance(node.func, ast.Attribute) and node.func.attr == "play")
                        or (isinstance(node.func, ast.Name) and node.func.id == "morph")):
                    node.keywords = [k for k in node.keywords if k.arg != "run_time"]
                return self.generic_visit(node)
        old, new = ast.parse(BEFORE), ast.parse(SOURCE.read_text())
        self.assertEqual(ast.dump(RemoveTiming().visit(copy.deepcopy(old))),
                         ast.dump(RemoveTiming().visit(copy.deepcopy(new))))
        for name in ["construct", "card", "unit_bar", "conditional", "pull", "show_pull", "chain_state", "ladder"]:
            a = [n for n in ast.walk(old) if isinstance(n, ast.FunctionDef) and n.name == name]
            b = [n for n in ast.walk(new) if isinstance(n, ast.FunctionDef) and n.name == name]
            self.assertEqual([ast.dump(n) for n in a], [ast.dump(n) for n in b])

    def test_finished_numeric_result_gets_reading_dwell_at_actual_frame_rates(self):
        for fps in (15, 30, 60):
            for phase in (0, .49, 1):
                with self.subTest(fps=fps, phase=phase):
                    existing, held, added = reading_hold_case(fps, phase)
                    self.assertGreaterEqual(held, 1.5 - 1e-10)
                    self.assertLessEqual(held, 1.5 + 1/fps + 1e-9)
                    self.assertLessEqual(existing, .2 + 1e-9)
                    self.assertGreater(added, 1.3)
                    self.assertLessEqual(added, 1.5-existing + 1/fps + 1e-9)

    def test_numeric_dwell_credits_residual_speech_and_existing_context_padding(self):
        for fps in (15, 30, 60):
            for phase in (0, .49, 1):
                for residual in (0, .35, 1, 1.5, 2, 4):
                    with self.subTest(fps=fps, phase=phase, residual=residual):
                        existing, held, added = reading_hold_case(fps, phase, residual_audio=residual)
                        self.assertGreaterEqual(held, 1.5 - 1e-10)
                        if existing >= 1.5:
                            self.assertEqual(added, 0)
                            self.assertEqual(held, existing)
                        else:
                            self.assertLessEqual(added, 1.5-existing + 1/fps + 1e-9)


if __name__ == "__main__":
    unittest.main()
