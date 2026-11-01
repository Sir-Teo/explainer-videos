"""Actual local roadmap scheduling against observed narrated-production gaps.

The 60fps diagnostic receipt reports relative target times below; its source
was 927fba6 / Hook419e40d8. No speech, renderer, model or producer is loaded.
"""
import ast
import math
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]


def duration(index, now, marks, fps):
    tree = ast.parse((ROOT / "videos/ai/ai1/s01_hook.py").read_text())
    question = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "question")
    loop = next(n for n in ast.walk(question) if isinstance(n, ast.For))
    nodes = [n for n in loop.body if
             (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "reveal_time"
                                               for t in n.targets)) or isinstance(n, ast.If)]
    scope = dict(k=index, vo=SimpleNamespace(mark_time=lambda mark: marks["abcdef".index(mark)],
                                            elapsed=lambda: now),
                 m=SimpleNamespace(cols=[None] * 6), config=SimpleNamespace(frame_rate=fps))
    exec(compile(ast.Module(nodes, type_ignores=[]), "actual-roadmap-schedule", "exec"), scope)
    return scope["reveal_time"]


class RoadmapTiming(unittest.TestCase):
    # Actual production targets minus block_start130.8666666666655.
    marks = [3.16, 4.04, 5.16, 5.96, 7.64, 9.00]

    def test_measured_short_gaps_prevent_fixed_duration_backlog(self):
        old_now = self.marks[0]
        old_lateness = []
        for mark in self.marks:
            old_now = max(old_now, mark)
            old_lateness.append(old_now - mark)
            old_now += 1.2
        self.assertGreater(max(old_lateness), .79)
        for fps in [15, 30, 60]:
            now = self.marks[0]
            for index, target in enumerate(self.marks):
                now = max(now, target)
                self.assertLessEqual(now - target, 1 / fps + 1e-12)
                seconds = duration(index, now, self.marks, fps)
                # Conservatively round a play upward to a whole encoded frame.
                now += math.ceil(seconds * fps - 1e-10) / fps
                if index < 5:
                    self.assertLessEqual(now, self.marks[index + 1] + 1e-12)

    def test_generous_gaps_and_last_act_retain_original_reveal_length(self):
        marks = [2., 5., 8., 11., 14., 17.]
        for index in range(6):
            self.assertEqual(duration(index, marks[index], marks, 60), 1.2)

    def test_frame_floor_remains_positive_for_already_missed_or_subframe_mark(self):
        for now in [4.04, 4.05, 10.]:
            self.assertEqual(duration(0, now, self.marks, 60), 1 / 60)
        # A physically impossible sub-frame gap is not claimed to be synchronized.

    def test_actual_production_checkpoint_requests_allow_frame_rounding(self):
        # Actual first request was 10ms before the target. Preserve that frame phase.
        now = 134.0166666666667 - 130.8666666666655
        starts = []
        for index, target in enumerate(self.marks):
            if target - now > 1 / 60:
                now += math.floor((target - now) * 60 + 1e-9) / 60
            starts.append(now)
            now += math.ceil(duration(index, now, self.marks, 60) * 60 - 1e-10) / 60
        self.assertLessEqual(max(abs(a - b) for a, b in zip(starts, self.marks)), 1 / 60 + 1e-12)


if __name__ == "__main__":
    unittest.main()
