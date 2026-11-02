"""Actual helper geometry/animation and bilingual contracts; no producer or render.

Only three drawing functions are AST-loaded. Rectangle stand-ins replace text,
so the tests need Manim but no TeX, original datasets, weights or caches.
"""
import ast
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

import manim as m
from manim.animation.animation import prepare_animation
import numpy as np

from explainer.zh_templates import Translator, source_startswith, sources, table
from tools.text_zh_add import validate_input

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "videos/ai/ai18"


def helpers():
    nodes = [n for n in ast.parse((PART / "common.py").read_text()).body
             if isinstance(n, ast.FunctionDef) and n.name in {"gantt", "fill_gantt", "log2_axis"}]
    env = {name: getattr(m, name) for name in (
        "Line", "VGroup", "Rectangle", "GREY_C", "GREY_B", "GREY_D", "GREY_E", "BLACK", "WHITE",
        "YELLOW", "LEFT", "UP", "DOWN", "UL", "DL", "Succession", "Wait", "GrowFromEdge", "linear")}
    env.update(label=lambda *a, **k: m.Rectangle(width=.4, height=.2),
               MathTex=lambda *a, **k: m.Rectangle(width=.4, height=.2),
               KIND_C={"F": m.BLUE, "B": m.RED, "W": m.GREEN}, GPU=m.BLUE)
    exec(compile(ast.Module(nodes, type_ignores=[]), str(PART / "common.py"), "exec"), env)
    return SimpleNamespace(**env)


class ReviewedSource(unittest.TestCase):
    def test_number_axis_tracks_ticks_after_transforms_and_extrapolates(self):
        ticks = (-40, -30, -24, -14, 0, 16)
        axis = helpers().log2_axis(ticks=ticks)
        for scale, delta in ((1., [.3, -2., 0]), (.7, [.8, .4, 0]), (1.4, [-1., 0, 0])):
            axis.scale(scale).shift(delta)
            for i, exponent in enumerate(ticks):
                self.assertAlmostEqual(axis.x(exponent), axis[1 + 2*i].get_center()[0], places=12)
            unit = (axis.x(18) - axis.x(-40)) / 58
            self.assertAlmostEqual(axis.x(-126), axis.x(-40) - 86 * unit, places=12)

    def test_pipeline_reveal_respects_wall_clock_start_end_and_growth(self):
        h = helpers()
        # Three unequal operations, including idle time and an early finish.
        chart = h.gantt([(0, 'F', 0, 0, 0, 2), (0, 'B', 0, 0, 3, 4),
                         (0, 'W', 0, 0, 7, 10)], 1, 10, numbers=False)
        captured = {}
        def play(*animations, **kwargs):
            captured.update(animations=[prepare_animation(a) for a in animations], kwargs=kwargs)
        scene = SimpleNamespace(add=lambda *a: None, remove=lambda *a: None, play=play,
                                get_mobject_family_members=lambda: [])
        original_width = chart.rects[0].width
        h.fill_gantt(scene, chart, run_time=4)
        self.assertNotIn('run_time', captured['kwargs'])
        cursor, first, middle, last = captured['animations']
        self.assertEqual(cursor.get_run_time(), 4)
        np.testing.assert_allclose([a.get_run_time() for a in (first, middle, last)], [.8, 1.6, 4])
        # The second operation begins at wall-clock1.2s, finishes at1.6s;
        # it must not be stretched until the cursor reaches4s.
        self.assertAlmostEqual(middle.animations[0].get_run_time(), 1.2)
        self.assertAlmostEqual(middle.animations[1].get_run_time(), .4)
        first._setup_scene(scene)
        first.begin()
        first.interpolate(.5)
        self.assertAlmostEqual(chart.rects[0].width, original_width / 2, places=10)
        first.finish()
        self.assertAlmostEqual(chart.rects[0].width, original_width, places=10)

    def test_chunk_pair_labels_match_the_drawn_causal_cells(self):
        method = next(n for n in ast.walk(ast.parse((PART / "s14_context.py").read_text()))
                      if isinstance(n, ast.FunctionDef) and n.name == "balance")
        assignment = next(n for n in method.body if isinstance(n, ast.Assign)
                          and any(getattr(t, 'id', None) == 'contiguous_work' for t in n.targets))
        env = dict(p=4, n=8, contiguous=[i // 2 for i in range(8)])
        exec(compile(ast.Module([assignment], type_ignores=[]), "drawn-cell-count", "exec"), env)
        # Enumerate all visible causal (query,key) cells independently.
        counts = [0] * 4
        balanced = [0] * 4
        for query in range(8):
            owner = min(query, 7-query)
            for key in range(query + 1):
                counts[query // 2] += 1
                balanced[owner] += 1
        self.assertEqual(env['contiguous_work'], counts)
        self.assertEqual(counts, [3, 7, 11, 15])
        self.assertEqual(balanced, [9] * 4)

    def test_narration_identity_bookmarks_and_template_translation(self):
        nar = json.loads((PART / "narration_zh.json").read_text())
        bookmark = re.compile(r"<bookmark mark=['\"]([^'\"]+)['\"]/>")
        translate = Translator('ai18')
        for key, entry in nar['lines'].items():
            self.assertEqual(key, hashlib.sha1(' '.join(entry['en'].split()).encode()).hexdigest()[:12])
            self.assertEqual(bookmark.findall(entry['en']), bookmark.findall(entry['zh']))
            self.assertEqual(translate(entry['en']), entry['zh'])
        zh = table('ai18')['ZH']
        for source in sources('ai18'):
            self.assertTrue(any(source_startswith(source.get('en') or source['tpl'], key) for key in zh))

    def test_caption_delta_is_guarded_and_composes_without_overwrite(self):
        proposal = json.loads((PART / 'reviewed_caption_delta.json').read_text())
        base = json.loads((ROOT / 'videos/ai/ai_text_zh.json').read_text())
        self.assertEqual(proposal['target'], 'videos/ai/ai_text_zh.json')
        merged = dict(base['strings'])
        seen = set()
        for op in proposal['operations']:
            self.assertEqual((op['table'], op['operation'], op['expected_absent']), ('strings', 'add', True))
            self.assertNotIn(op['key'], seen)
            seen.add(op['key'])
            if op['key'] in merged:
                self.assertEqual(merged[op['key']], op['value'], 'caption conflict: stop integration')
            else:
                merged[op['key']] = op['value']
        for key, value in base['strings'].items():
            self.assertEqual(merged[key], value)
        additions = validate_input(json.loads((PART / 'text_zh_add.json').read_text()))
        for op in proposal['operations']:
            if op['key'] in additions['strings']:
                self.assertEqual(additions['strings'][op['key']], op['value'])


if __name__ == '__main__':
    unittest.main()
