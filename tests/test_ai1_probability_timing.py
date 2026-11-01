"""Actual cached-speech cue budgets, without models, audio writes or renders."""
import ast
import copy
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
from types import SimpleNamespace
import unittest


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
                return self.generic_visit(node)
            def visit_Assign(self, node):
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    if node.value.func.id == "_bookmark_run_times":
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


if __name__ == "__main__":
    unittest.main()
