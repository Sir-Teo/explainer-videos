"""Prevent overstating text-only voice pipeline latency and information loss."""
import ast
import json
from pathlib import Path
import unittest

from explainer.lang import BOOKMARK, key
from explainer.zh_templates import Translator

ROOT = Path(__file__).resolve().parents[1]


class CascadeClaims(unittest.TestCase):
    def test_source_and_both_translation_paths(self):
        path = ROOT / 'videos/ai/ai23/s17_omni.py'
        tree = ast.parse(path.read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Omni')
        fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'cascade')
        en = next(n.args[0].value for n in ast.walk(fn) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        self.assertIn('can stream partial results', en)
        self.assertIn('may be lost', en)
        zh = Translator('ai23')(en)
        self.assertIn('流式', zh)
        self.assertEqual(BOOKMARK.findall(en), BOOKMARK.findall(zh))
        lines = json.loads((ROOT / 'videos/ai/ai23/narration_zh.json').read_text())['lines']
        self.assertEqual(lines[key(en)]['en'], en)
        self.assertEqual(lines[key(en)]['zh'], zh)
        label = next(n.value for n in ast.walk(fn) if isinstance(n, ast.Constant)
                     and isinstance(n.value, str) and n.value.startswith('a text-only cascade:'))
        for name in ['videos/ai/ai23/text_zh_add.json', 'videos/ai/ai_text_zh.json']:
            table = json.loads((ROOT / name).read_text())['strings']
            self.assertIn('流式', table[label])


if __name__ == '__main__':
    unittest.main()
