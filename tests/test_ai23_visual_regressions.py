"""Source guards for independently recreated Part 23 visual fixes."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'videos/ai/ai23'
def body(file, method):
    tree = ast.parse((ROOT / file).read_text())
    node = next(x for x in ast.walk(tree) if isinstance(x, ast.FunctionDef) and x.name == method)
    return ast.unparse(node)

class VisualRegressions(unittest.TestCase):
    def test_first_frequency_label_moves_away_from_axis(self):
        source = body('s09_sampling.py', 'tones')
        self.assertIn('DR if f == min(tones)', source)
        self.assertIn('UL if f < fs / 2 else UR', source)

    def test_rotated_labels_are_anchored_above_grid(self):
        source = body('s15_clip.py', 'pairs')
        self.assertIn('word.scale_to_fit_height(1.0)', source)
        self.assertIn('grid.get_top()[1], 0], UP, buff=0.12', source)
        self.assertIn('words.add(word)', source)

    def test_diagonal_survives_heatmap_transitions(self):
        source = body('s15_clip.py', 'learning')
        self.assertIn('diag.set_z_index(3)', source)
        self.assertIn('self.bring_to_front(diag)', source)
        self.assertIn('np.max(L[:, 1])', source)
        self.assertNotIn('np.percentile(L[:, 1], 98)', source)
        self.assertNotIn('min(p_[1], lax.ax.y_range[1])', source)

    def test_negative_empirical_bound_is_not_shown_positive(self):
        source = body('s15_clip.py', 'bound')
        self.assertIn('abs(float(e.mean()))', source)
        self.assertIn('base_y + e.mean() * sy / 2', source)
        self.assertIn('base_y + lowest * sy', source)
        self.assertIn('Create(zero)', source)

    def test_vq_highlight_does_not_recolour_images(self):
        source = body('s07_vq.py', 'cures')
        self.assertIn('scale_factor=1.05', source)
        self.assertIn('SurroundingRectangle(cols[-1]', source)
        self.assertNotIn('Indicate(cols[-1]', source)

if __name__ == '__main__':
    unittest.main()
