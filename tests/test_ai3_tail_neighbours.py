"""Exercise the scene's projected cosine ranking without importing Manim/data loaders."""
import ast
from pathlib import Path
import unittest

import numpy as np


class ProjectedNeighbourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'videos/ai/ai3/s13_words.py'
        module = ast.parse(path.read_text())
        node = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == 'projected_neighbours')
        namespace = {'np': np}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), namespace)
        cls.neighbours = staticmethod(namespace['projected_neighbours'])

    def test_actual_query_excluded_under_exact_ties_and_invalid_rows(self):
        vectors = np.array([[1., 0.], [1., 0.], [0., 0.], [np.nan, 1.], [0., 1.], [1., 0.]])
        vocab = ['first', 'query', 'zero', 'invalid', 'orthogonal', 'last']
        self.assertEqual(self.neighbours(vectors, vocab, 'query', 2, 8), ['first', 'last', 'orthogonal'])

    def test_truncation_can_make_query_direction_unavailable(self):
        vectors = np.array([[0., 1.], [1., 0.], [0., 2.]])
        vocab = ['query', 'other', 'aligned']
        self.assertEqual(self.neighbours(vectors, vocab, 'query', 1), [])
        self.assertEqual(self.neighbours(vectors, vocab, 'query', 2), ['aligned', 'other'])


if __name__ == '__main__':
    unittest.main()
