"""Planning summaries and actual bilingual scene branches, without search/render jobs."""
import ast
import math
import re
import unittest
from pathlib import Path

import numpy as np

from explainer.zh_templates import Translator


SOURCE = Path(__file__).resolve().parents[1] / "videos/ai/ai2/s11_plans.py"
TREE = ast.parse(SOURCE.read_text())
HELPER = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == "planner_summary")
HELPER_SCOPE = {"math": math}
exec(compile(ast.Module(body=[HELPER], type_ignores=[]), str(SOURCE), "exec"), HELPER_SCOPE)
planner_summary = HELPER_SCOPE["planner_summary"]
METHOD = next(n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef) and n.name == "planners")
WITH = next(n for n in METHOD.body if isinstance(n, ast.With))


def completed(n=7, bfs=10, hmax=5, ff=6, bfs_len=4, hmax_len=4, ff_len=6):
    return dict(n=n, bfs=bfs, hmax=hmax, ff=ff, bfs_len=bfs_len, hmax_len=hmax_len, ff_len=ff_len)


class PlanningCensoringTests(unittest.TestCase):
    def test_lengths_use_same_solved_cases_and_work_keeps_unfinished_attempts(self):
        rows = [completed(), completed(bfs=100, bfs_len=-1, hmax_len=-1, ff_len=8),
                completed(bfs_len=2, ff_len=-1), {"n": 7, "ff": 0, "ff_len": 0}]
        out = planner_summary(rows)
        self.assertEqual(out["paired_solved"], 1)
        self.assertEqual((out["paired_bfs_length"], out["paired_ff_length"]), (4, 6))
        self.assertEqual(out["all"]["bfs"], {"attempted": 3, "solved": 2, "unresolved": 1,
                                           "not_run_or_unknown": 1, "mean_expanded": 40})
        self.assertEqual(out["all"]["ff"]["solved"], 3)
        self.assertEqual(out["all"]["ff"]["unresolved"], 1)

    def test_missing_work_unknown_lengths_and_stale_capped_lengths_are_not_successes(self):
        rows = [{"n": 7, "bfs_len": 4}, {"n": 7, "bfs": 20},
                dict(completed(), bfs_status="capped"),
                {"n": 7, "bfs": -1, "bfs_len": 4},
                {"n": 7, "bfs": float("nan"), "bfs_len": 4},
                {"n": 7, "bfs": True, "bfs_len": 4}]
        out = planner_summary(rows)
        self.assertEqual(out["all"]["bfs"]["attempted"], 2)
        self.assertEqual(out["all"]["bfs"]["solved"], 0)
        self.assertEqual(out["all"]["bfs"]["unresolved"], 2)
        self.assertEqual(out["all"]["bfs"]["not_run_or_unknown"], 4)
        self.assertIsNone(out["paired_bfs_length"])

    def test_zero_length_already_solved_task_is_valid_but_missing_fields_are_not(self):
        out = planner_summary([completed(n=4, bfs=0, hmax=0, ff=0, bfs_len=0, hmax_len=0, ff_len=0)])
        self.assertEqual(out["paired_solved"], 1)
        self.assertEqual((out["paired_bfs_length"], out["paired_ff_length"]), (0, 0))
        for rows in ([], [{"n": 7}], [{"n": 7, "bfs": 10, "bfs_len": -1}]):
            out = planner_summary(rows)
            self.assertEqual(out["paired_solved"], 0)
            self.assertIsNone(out["paired_ff_length"])

    def test_comparison_stays_at_largest_bfs_attempted_size(self):
        rows = [completed(n=6), completed(n=7, bfs_len=-1),
                {"n": 8, "ff": 99, "ff_len": 100}]
        out = planner_summary(rows)
        self.assertEqual(out["n_bfs"], 7)
        self.assertEqual(out["paired_solved"], 0)
        self.assertIsNone(out["paired_bfs_length"])

    def test_actual_scene_branches_and_bookmarks_translate_without_render_or_cache_access(self):
        # Execute the actual scene's setup and narration expression with geometry
        # stand-ins. This also exercises empty/single-point plots and cost branches.
        class Mob(list):
            width = 1
            def __init__(self, *args, **kwargs):
                super().__init__(args)
                self.text = args[0] if args and isinstance(args[0], str) else ""
            def add(self, item): self.append(item); return self
            def arrange(self, *args, **kwargs): return self
            def move_to(self, *args, **kwargs): return self
            def next_to(self, *args, **kwargs): return self
            def to_corner(self, *args, **kwargs): return self
            def scale_to_fit_width(self, *args, **kwargs): return self
        class Plot(Mob):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs); self.ax = self
            def c2p(self, x, y): return (x, y)
        fixtures = [[], [{"n": 7}], [completed()], [completed(bfs_len=-1, hmax_len=-1)],
                    [{"n": 7, "ff": 1, "ff_len": 0}],
                    [completed(bfs=0, hmax=0, ff=0, bfs_len=0, hmax_len=0, ff_len=0)],
                    [{"n": 7, "bfs": 30, "bfs_len": None}],
                    [completed(bfs=3_000_001, bfs_len=-1)]]
        translate = Translator("ai2")
        for rows in fixtures:
            with self.subTest(rows=rows):
                scope = {"np": np, "math": math, "planner_summary": planner_summary,
                         "load": lambda name: {"rows": rows, "towers": [1, 3, 13, 73, 501, 4051, 37633]},
                         "VGroup": Mob, "MathTex": Mob, "label": Mob, "axes": Plot, "curve": Mob,
                         "Dot": Mob, "legend": Mob, "history_card": Mob, "note": Mob}
                scope.update({k: k for k in ("GREY_A", "GREY_B", "GCOST", "PATH", "FAIL", "HIST", "RIGHT", "DOWN", "UP", "DL")})
                exec(compile(ast.Module(body=METHOD.body[:METHOD.body.index(WITH)], type_ignores=[]),
                             "actual-planning-scene-setup", "exec"), scope)
                english = eval(compile(ast.Expression(WITH.items[0].context_expr.args[0]),
                                       "actual-planning-narration", "eval"), scope)
                chinese = translate(english)
                self.assertIsNotNone(chinese)
                self.assertNotIn("{", chinese)
                self.assertNotIn("-1.0", english)
                self.assertNotIn("-1.0", scope["cost"].text)
                self.assertNotRegex(chinese, r"No |On random|Greedy search|Every recorded|Some recorded")
                self.assertEqual(re.findall(r"<bookmark[^>]+/>", english),
                                 re.findall(r"<bookmark[^>]+/>", chinese))
                self.assertEqual(len(re.findall(r"<bookmark[^>]+/>", english)), 4)
                self.assertIn("如果解出", chinese)
                if not any(c["attempted"] for c in scope["counts"].values()):
                    self.assertIn("不把它们推断为成功", chinese)
                if any(c["unresolved"] for c in scope["counts"].values()):
                    self.assertIn("包含这些未完成尝试", chinese)
                if not scope["paired"]:
                    self.assertIn("无法给出可比较", chinese)
                self.assertGreaterEqual(10 ** scope["ymax"], scope["largest"])


if __name__ == "__main__":
    unittest.main()
