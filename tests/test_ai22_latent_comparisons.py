"""Scientific regression cases: all channel comparisons, ties, invalid metrics."""
import ast
import math
from pathlib import Path
import unittest
source = Path(__file__).resolve().parents[1] / 'videos/ai/ai22/s04_latent.py'
node = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'reconstruction_comparison')
namespace = {'math': math}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), namespace)
compare = namespace['reconstruction_comparison']

class LatentComparisonTests(unittest.TestCase):
    def fixture(self):
        return {(10,1):.3,(5,4):.1,(5,2):.2,(5,1):.25,(2,16):.12,(2,4):.2,(1,64):.15,(1,16):.22}
    def test_all_four_within_grid_comparisons(self):
        rm=self.fixture()
        self.assertTrue(compare(rm)[0])
        rm[(5,2)]=.3  # 1x1 and2x2 still improve; the5x5 comparison doesnot.
        self.assertFalse(compare(rm)[0])
    def test_equal_scalar_counts_distinguish_wins_and_ties(self):
        self.assertEqual(compare(self.fixture())[2:],(1,2,0))
        self.assertEqual(compare({c:.2 for c in self.fixture()})[2:],(0,0,3))
    def test_invalid_rmse_rejected(self):
        for value in [-.1,float('nan'),float('inf')]:
            rm=self.fixture();rm[(5,2)]=value
            with self.assertRaises(ValueError):compare(rm)

if __name__ == '__main__':unittest.main()
