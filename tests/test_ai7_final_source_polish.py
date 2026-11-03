"""Synthetic source/family regression only; no scientific or rendered acceptance."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class FinalSourcePolish(unittest.TestCase):
    def test_all_five_vi_complete_state_fades_preserve_duration(self):
        tree = ast.parse((ROOT / 'videos/ai/ai7/s17_vi.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'VI')
        found = []
        for method in cls.body:
            if not isinstance(method, ast.FunctionDef):
                continue
            for call in ast.walk(method):
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and call.func.attr == 'clear_scene':
                    self.assertEqual(ast.unparse(call.func.value), 'self')
                    self.assertEqual(call.args, [])  # no retained objects / incomplete named groups
                    self.assertEqual([(k.arg, ast.literal_eval(k.value)) for k in call.keywords], [('run_time', 1.5)])
                    found.append(method.name)
        self.assertEqual(found, ['fit', 'derive', 'cavi', 'reparam', 'amortize'])

    def test_actual_clear_scene_covers_mixed_families_and_clears_updaters(self):
        # Actual Manim objects and actual helper body; no renderer or scene data.
        import numpy as np
        from manim import Dot, FadeOut, Group, ImageMobject, VGroup
        image = ImageMobject(np.zeros((2, 2, 3), dtype=np.uint8))
        child = Dot()
        group = Group(image, VGroup(child))
        stray = Dot()
        for obj in (image, child, stray):
            obj.add_updater(lambda mob: None)
        plays = []
        scene = SimpleNamespace(mobjects=[group, stray], play=lambda *a, **kw: plays.append((a, kw)))
        tree = ast.parse((ROOT / 'explainer/voiceover.py').read_text())
        method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'clear_scene')
        scope = {'FadeOut': FadeOut}
        exec(compile(ast.Module([method], type_ignores=[]), 'actual-clear-scene', 'exec'), scope)
        scope['clear_scene'](scene, run_time=1.5)
        self.assertEqual(len(plays), 1)
        animations, kwargs = plays[0]
        self.assertEqual(kwargs, {'run_time': 1.5})
        self.assertEqual([a.mobject for a in animations], [group, stray])
        self.assertTrue(all(isinstance(a, FadeOut) for a in animations))
        self.assertTrue(all(not obj.updaters for obj in group.get_family() + stray.get_family()))

    def test_outro_credit_has_exact_bilingual_mapping(self):
        tree = ast.parse((ROOT / 'videos/ai/ai7/s18_outro.py').read_text())
        text = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Constant)
                    and isinstance(n.value, str) and n.value.startswith('Text: Project Gutenberg'))
        self.assertIn('Methods implemented with NumPy and SciPy;', text)
        self.assertNotIn('Every method is written out in numpy', text)
        table = json.loads((ROOT / 'videos/ai/ai_text_zh.json').read_text())['strings']
        self.assertIn(text, table)
        self.assertIn('方法使用NumPy和SciPy实现', table[text])
        self.assertEqual(text.count('\\'), table[text].count('\\'))
        from explainer import lang, zh_text
        with patch.object(lang, 'LANG', 'zh'), patch.object(zh_text, '_TABLE', {'strings': table}):
            self.assertEqual(zh_text.translate(text), table[text])


if __name__ == '__main__':
    unittest.main()
