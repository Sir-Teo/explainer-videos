"""Actual Surprise speech-cue regressions, with no model/audio/render imports."""
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
EVIDENCE = ROOT / "docs/qa/evidence/ai1-surprise-narrated-timing-repair"
SOURCE = ROOT / "videos/ai/ai1/s03_surprise.py"
read = lambda name: gzip.decompress((EVIDENCE / (name + ".gz")).read_bytes())
DIAGNOSTIC = json.loads(read("exact-diagnostic.json"))
COMPACT = json.loads(read("compact-requests.json"))["Surprise"]
BEFORE = read("source-before.py").decode()
MARK = re.compile(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>")


def marks(block):
    return {m[1]: block["words"][len(MARK.sub("", block["raw"][:m.start()]).split())][1] - block["start"]
            for m in MARK.finditer(block["raw"])}


class Object:
    """Only method-chain identity needed by the actual animation expressions."""
    @property
    def animate(self):
        return self
    def set_opacity(self, value):
        return self
    def scale(self, value):
        return self
    def to_corner(self, *args, **kwargs):
        return self


def run(tree, method, block_index, global_block, start_mark, stop_mark, fps, phase=0):
    f = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == method)
    block = [n for n in ast.walk(f) if isinstance(n, ast.With)][block_index]
    def is_wait(n, mark):
        return (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == "wait_until"
                and n.value.args[0].value == mark)
    first = next(i for i, n in enumerate(block.body) if is_wait(n, start_mark)) + 1 if start_mark else 0
    last = next(i for i, n in enumerate(block.body) if is_wait(n, stop_mark)) + 1
    cues = marks(DIAGNOSTIC["report"]["narration"][global_block])
    now = [(cues[start_mark] if start_mark else 0) + phase / fps]
    requests, events = [], []
    def wait_until(mark):
        requests.append({"mark": mark, "target": cues[mark], "arrival": max(now[0], cues[mark]),
                         "late": max(0., now[0] - cues[mark]), "lead": cues[mark] - now[0]})
        gap = cues[mark] - now[0]
        if gap > 1 / 60:
            now[0] += math.ceil(gap * fps - 1e-10) / fps
    def play(*args, run_time=1.):
        events.append({"kind": "play", "duration": run_time})
        now[0] += math.ceil(run_time * fps - 1e-10) / fps
    def morph(scene, a, b, run_time=1.4):
        events.append({"kind": "morph", "duration": run_time})
        now[0] += math.ceil(run_time * fps - 1e-10) / fps
    scope = {"config": SimpleNamespace(frame_rate=fps), "vo": SimpleNamespace(
        elapsed=lambda: now[0], mark_time=lambda mark: cues[mark], wait_until=wait_until),
        "self": SimpleNamespace(play=play), "morph": morph, "DOWN": 0, "UR": 0,
        "eqs": list(range(6)), "units": Object(), "frac_dots": [0, 1],
        "d": {"rest": 0, "axes": [0, 1], "unit": Object(), "ax": 0, "line": 0}}
    # The integer-step animation iterates over each existing stack.
    class Units(Object):
        def __iter__(self):
            return iter([[0, 1], [2]])
    scope["units"] = Units()
    for key in ["seg_x", "bx", "bx_l", "seg_y", "by", "by_l", "stack_a", "stack_b", "st_l",
                "additive", "int_dots", "ax", "bent", "xl", "yl", "axl", "tail"]:
        scope[key] = key
    for key in ["FadeIn", "FadeOut", "Create", "GrowFromEdge", "TransformFromCopy",
                "LaggedStart", "VGroup", "ReplacementTransform"]:
        scope[key] = lambda *args, _key=key, **kw: (_key, args, kw)
    helper = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_bookmark_run_times"]
    exec(compile(ast.Module(helper + block.body[first:last], type_ignores=[]), "actual-surprise-span", "exec"), scope)
    return requests, events


class SurpriseTiming(unittest.TestCase):
    def test_exact_diagnostics_and_all_eight_selected_utterances(self):
        self.assertEqual(len(read("exact-diagnostic.json")), 104451)
        self.assertEqual(hashlib.sha256(read("exact-diagnostic.json")).hexdigest(),
                         "b1d79845b80fb776c0d8a3a881770b3e92c1b3f9f17ae2cebc3b1f4356bb8544")
        self.assertEqual(len(read("compact-requests.json")), 13158)
        self.assertEqual(hashlib.sha256(read("compact-requests.json")).hexdigest(),
                         "2cd32f4024aed88336aa7867c8ee1e8229d3082cadfb8865d5083cb657041eb4")
        self.assertEqual(hashlib.sha256(BEFORE.encode()).hexdigest(), DIAGNOSTIC["source_sha256"])
        blocks = DIAGNOSTIC["report"]["narration"]
        self.assertEqual(len(blocks), 8)
        self.assertAlmostEqual(sum(b["duration"] for b in blocks), 145.45)
        self.assertEqual(sum(len(marks(b)) for b in blocks), 22)
        for block, occurrence in zip(blocks, DIAGNOSTIC["exact_narration_occurrences"]):
            self.assertEqual(block["raw"], occurrence["raw"])
            alignment = DIAGNOSTIC["per_utterance_word_alignment_and_duration"][occurrence["key"]]
            self.assertEqual(block["duration"], alignment["duration"])
            self.assertEqual(block["text"], alignment["spoken"])
        for request, compact in zip(DIAGNOSTIC["all_bookmark_requests"], COMPACT["all_bookmark_requests"]):
            self.assertEqual(request["mark"], compact[1])
            for value, expected in zip([request["block_start"], request["target_seconds"],
                                        request["actual_seconds"], request["late_seconds"]],
                                       [compact[0], compact[2], compact[3], compact[4]]):
                self.assertAlmostEqual(value, expected, places=10)

    def test_old_actual_sequential_calls_reproduce_all_four_overruns_including_backlog(self):
        tree = ast.parse(BEFORE)
        requests, events = run(tree, "derive", 0, 3, "b", "e", 100)
        self.assertEqual([r["mark"] for r in requests], ["c", "d", "e"])
        for request, expected in zip(requests, [1.16, .5, 1.98]):
            self.assertAlmostEqual(request["late"], expected, places=10)
        intro, _ = run(tree, "curve", 0, 5, None, "a", 100)
        self.assertAlmostEqual(intro[0]["late"], 2.51, places=10)

    def test_actual_repaired_sequence_hits_all_cues_with_rounding_and_adverse_phase(self):
        tree = ast.parse(SOURCE.read_text())
        for fps in [15, 30, 60]:
            for phase in [0, .49, 1]:
                for args in [("derive", 0, 3, "b", "e"), ("curve", 0, 5, None, "a")]:
                    with self.subTest(fps=fps, phase=phase, span=args[0]):
                        requests, events = run(tree, *args, fps, phase)
                        self.assertTrue(all(r["late"] == 0 for r in requests))
                        self.assertTrue(all(r["lead"] >= 1 / fps - 1e-10 for r in requests))
                        self.assertTrue(all(e["duration"] >= 1 / fps for e in events))
                        self.assertGreater(min(e["duration"] for e in events), .29)
                        if args[0] == "derive":
                            # The old d lateness was inherited from c, not a short c→d gap.
                            self.assertEqual([e["duration"] for e in events[4:7]], [1., 2., .5])

    def test_preferred_lengths_remain_when_possible_and_impossible_deadlines_are_positive(self):
        tree = ast.parse(SOURCE.read_text())
        helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_bookmark_run_times")
        for fps in [15, 30, 60]:
            scope = {"config": SimpleNamespace(frame_rate=fps)}
            exec(compile(ast.Module([helper], type_ignores=[]), "actual-surprise-budget", "exec"), scope)
            for preferred in [(1.4, .8, .8, 1.2), (1., 2.), (1., 2., 1.)]:
                ample = SimpleNamespace(mark_time=lambda _: 30., elapsed=lambda: 0.)
                self.assertEqual(scope["_bookmark_run_times"](ample, "cue", *preferred), preferred)
                missed = SimpleNamespace(mark_time=lambda _: 0., elapsed=lambda: 1.)
                self.assertEqual(scope["_bookmark_run_times"](missed, "cue", *preferred),
                                 (1 / fps,) * len(preferred))

    def test_entire_scene_ast_preserves_voice_geometry_math_and_animation_order(self):
        class RemoveTiming(ast.NodeTransformer):
            def visit_FunctionDef(self, n):
                return None if n.name == "_bookmark_run_times" else self.generic_visit(n)
            def visit_Assign(self, n):
                if isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name):
                    if n.value.func.id == "_bookmark_run_times":
                        return None
                return self.generic_visit(n)
            def visit_Call(self, n):
                if ((isinstance(n.func, ast.Attribute) and n.func.attr == "play")
                        or (isinstance(n.func, ast.Name) and n.func.id == "morph")):
                    n.keywords = [k for k in n.keywords if k.arg != "run_time"]
                return self.generic_visit(n)
        before, after = ast.parse(BEFORE), ast.parse(SOURCE.read_text())
        self.assertEqual(ast.dump(RemoveTiming().visit(copy.deepcopy(before))),
                         ast.dump(RemoveTiming().visit(copy.deepcopy(after))))
        for name in ["construct", "card", "intuition", "rules", "skyline"]:
            a = next(n for n in ast.walk(before) if isinstance(n, ast.FunctionDef) and n.name == name)
            b = next(n for n in ast.walk(after) if isinstance(n, ast.FunctionDef) and n.name == name)
            self.assertEqual(ast.dump(a), ast.dump(b))


if __name__ == "__main__":
    unittest.main()
