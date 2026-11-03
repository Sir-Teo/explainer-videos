"""Guard FAST's baseline label placement against the neighboring claim card."""
import ast
from pathlib import Path
import unittest


class FastLabelPlacement(unittest.TestCase):
    def test_baseline_label_is_right_aligned_to_its_marker(self):
        source = Path(__file__).resolve().parents[1] / 'videos/ai/ai29/s17_fast.py'
        tree = ast.parse(source.read_text())
        sweep = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'sweep')
        assignment = next(n for n in ast.walk(sweep) if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == 'nbl' for t in n.targets))
        value = assignment.value
        self.assertIsInstance(value, ast.Call)
        self.assertEqual(value.func.attr, 'align_to')
        self.assertEqual([ast.unparse(a) for a in value.args], ['nb', 'RIGHT'])
        self.assertIn('per-step bins', ast.unparse(value))

    def test_repeat_metric_is_training_same_joint_not_all_tokens_or_test_data(self):
        import hashlib
        import json
        import re
        root = Path(__file__).resolve().parents[1]
        source = (root / 'videos/ai/ai29/s17_fast.py').read_text()
        tree = ast.parse(source)
        naive = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'naive')
        call = next(n for n in ast.walk(naive) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        en = eval(compile(ast.Expression(call.args[0]), 'naive-narration', 'eval'),
                  {'n_tok': 350, 'rep': .46, 'near': .75})
        self.assertIn('smooth training motions', en)
        self.assertIn('same-joint values repeat', en)
        self.assertNotIn('nearly all the same', en)
        key = hashlib.sha1(' '.join(en.split()).encode()).hexdigest()[:12]
        row = json.loads((root / 'videos/ai/ai29/narration_zh.json').read_text())['lines'][key]
        self.assertEqual(row['en'], en)
        self.assertIn('训练动作', row['zh'])
        self.assertIn('同一关节', row['zh'])
        marks = lambda t: re.findall(r"<bookmark mark='([^']+)'/>", t)
        self.assertEqual(marks(en), marks(row['zh']))
        producer = (root / 'videos/ai/ai29/compute.py').read_text()
        self.assertIn('qtr[:, 1:] == qtr[:, :-1]', producer)


if __name__ == '__main__':
    unittest.main()
