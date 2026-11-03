"""The simulated agent disclaimer remains visible and clearly scoped."""
import ast
from pathlib import Path
import unittest

class TraceCaveat(unittest.TestCase):
    def test_disclaimer_is_bilingual_and_two_lines(self):
        src = (Path(__file__).resolve().parents[1] / 'videos/ai/ai29/s04_loop.py').read_text()
        tree = ast.parse(src)
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'trace')
        tag = next(n for n in ast.walk(fn) if isinstance(n, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == 'tag' for t in n.targets))
        text = ast.unparse(tag.value)
        self.assertIn('simulated agent', text)
        self.assertIn('not a language model', text)
        self.assertIn('模拟智能体', text)
        self.assertIn('并非语言模型', text)
        self.assertIn(r'\\\\', text)

if __name__ == '__main__':
    unittest.main()
