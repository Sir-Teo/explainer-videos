"""Actual narration/translation regressions for published and planned scopes."""
from pathlib import Path
import ast
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class RoadmapContracts(unittest.TestCase):
    def method(self, file, name):
        tree = ast.parse((ROOT/'videos/ai/ai23'/file).read_text())
        return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)

    def narration(self, method):
        from explainer.zh_templates import Translator
        from explainer.lang import BOOKMARK
        expr = next(n.args[0] for n in ast.walk(method) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        en = ast.literal_eval(expr)
        zh = Translator('ai23')(en)
        self.assertIsNotNone(zh)
        self.assertEqual(BOOKMARK.findall(en), BOOKMARK.findall(zh))
        return en, zh

    def test_only_four_direct_methods_are_data_free(self):
        for file, method in [('s01_hook.py','question'),('s13_whisper.py','roads'),('s18_outro.py','payoffs'),('s18_outro.py','next_time')]:
            fn = self.method(file, method)
            self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'load' for n in ast.walk(fn)))
            self.narration(fn)
        fn = self.method('s12_ctc.py','problem')
        self.assertTrue(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'load' for n in ast.walk(fn)))

    def test_published_result_retains_decoding_resource_and_task_limits(self):
        en, zh = self.narration(self.method('s13_whisper.py','roads'))
        for value in ['external Transformer language model', 'segment timestamps', 'translates into English']:
            self.assertIn(value, en)
        for value in ['外部Transformer语言模型', '片段时间戳', '译成英语']:
            self.assertIn(value, zh)
        self.assertNotIn('December 2022', en)
        self.assertNotIn('times the words', en)

    def test_roadmap_is_a_plan_and_contrastive_example_is_qualified(self):
        en, zh = self.narration(self.method('s01_hook.py','question'))
        self.assertIn('will demonstrate', en)
        self.assertNotIn('computer making', en)
        self.assertIn('计划演示', json.loads((ROOT/'videos/ai/ai_text_zh.json').read_text())['strings']['planned demonstrations in this part:'])
        self.assertNotIn('制作这段视频的电脑', zh)
        en, zh = self.narration(self.method('s18_outro.py','next_time'))
        self.assertIn('in contrastive learning', en)
        self.assertIn('self-distillation', en)
        self.assertIn('在对比学习中', zh)
        self.assertIn('自蒸馏', zh)

    def test_ctc_does_not_erase_hidden_path_hmm_training(self):
        en, zh = self.narration(self.method('s12_ctc.py','problem'))
        self.assertIn('HMM training itself could use hidden alignments', en)
        self.assertIn('HMM训练本身也能处理隐藏对齐', zh)
        self.assertNotIn('old systems needed each frame labelled', en)


if __name__ == '__main__':
    unittest.main(verbosity=2)
