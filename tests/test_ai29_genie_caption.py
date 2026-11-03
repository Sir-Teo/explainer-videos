"""Keep the bilingual Project Genie card concise without changing its claim."""
import ast
from pathlib import Path
import unittest

class GenieCaption(unittest.TestCase):
    def test_project_genie_card_retains_scope_and_time(self):
        path = Path(__file__).resolve().parents[1] / 'videos/ai/ai29/s14_genie.py'
        fn = next(n for n in ast.walk(ast.parse(path.read_text()))
                  if isinstance(n, ast.FunctionDef) and n.name == 'worlds')
        calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == 'history_card']
        card = next(n for n in calls if len(n.args) > 1 and isinstance(n.args[1], ast.Constant)
                    and n.args[1].value == 'Project Genie')
        text = ast.unparse(card.args[2])
        self.assertIn('部分美国订阅用户可用', text)
        self.assertIn('60', text)
        self.assertIn('some subscribers in the US', text)

if __name__ == '__main__':
    unittest.main()
