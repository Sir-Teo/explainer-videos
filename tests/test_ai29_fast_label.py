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


if __name__ == '__main__':
    unittest.main()
