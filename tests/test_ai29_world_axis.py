"""The world-model prediction-error plot must have quantitative axis labels."""
import ast
from pathlib import Path
import unittest

class WorldAxisLabels(unittest.TestCase):
    def test_imagination_plot_labels_both_axes(self):
        path = Path(__file__).resolve().parents[1] / 'videos/ai/ai29/s12_world.py'
        tree = ast.parse(path.read_text())
        fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'imagine')
        calls = [ast.unparse(n) for n in ast.walk(fn) if isinstance(n, ast.Call)]
        self.assertTrue(any(c.startswith('ax.x_axis.add_numbers(') for c in calls))
        self.assertTrue(any(c.startswith('ax.y_axis.add_numbers(') for c in calls))
        self.assertTrue(any('len(pe)' in c and 'range(' in c for c in calls))
        self.assertTrue(any('ystep' in c and 'ymax' in c and 'range(' in c for c in calls))

if __name__ == '__main__':
    unittest.main()
