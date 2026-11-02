"""Regression cases for the FD statistic shown on Part22's log-coordinate plot.

Extract only the pure statistics helper; do not import Manim or numeric producers.
"""
import ast
import math
from pathlib import Path
import unittest

SOURCE = Path(__file__).with_name('s09_sd3.py')
if not SOURCE.exists():
    SOURCE = Path(__file__).resolve().parents[1] / 'videos/ai/ai22/s09_sd3.py'
node = next(node for node in ast.parse(SOURCE.read_text()).body
            if isinstance(node, ast.FunctionDef) and node.name == 'fd_log_summary')
namespace = {'math': math}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), namespace)
summarize = namespace['fd_log_summary']


class TimestepFDSummaryTests(unittest.TestCase):
    def test_line_is_arithmetic_mean_before_log_not_geometric_mean(self):
        measured = [[1, 10], [4, 40], [10, 100]]
        summary = summarize(measured)
        self.assertEqual(summary['mean'], (5, 50))
        for actual, expected in zip(summary['log_mean'], (math.log10(5), math.log10(50))):
            self.assertAlmostEqual(actual, expected)
        old_geometric_coordinate = math.fsum(math.log10(row[0]) for row in measured) / 3
        self.assertGreater(abs(summary['log_mean'][0] - old_geometric_coordinate), .1)

    def test_band_is_observed_seed_range_and_order_independent(self):
        measured = [[1, 90], [9, 30], [5, 60]]
        summary = summarize(measured)
        self.assertEqual(summary['low'], (1, 30))
        self.assertEqual(summary['high'], (9, 90))
        self.assertEqual(summary['mean'], (5, 60))
        self.assertEqual(summary, summarize(measured[::-1]))
        self.assertEqual(summary['log_low'], (0., math.log10(30)))
        self.assertEqual(summary['log_high'], (math.log10(9), math.log10(90)))

    def test_invalid_log_domain_rejected_without_clamping(self):
        for value in (0, -1, float('nan'), float('inf'), -float('inf')):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize([[1, 2], [3, value], [5, 6]])

    def test_three_complete_seed_rows_required(self):
        for values in ([], [[], [], []], [[1], [2]], [[1], [2, 3], [4]]):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    summarize(values)

    def test_finite_mean_does_not_overflow_for_finite_positive_inputs(self):
        summary = summarize([[1e308], [1e308], [1e308]])
        self.assertEqual(summary['mean'], (1e308,))
        self.assertEqual(summary['log_mean'], (308.,))


if __name__ == '__main__':
    unittest.main()
