"""Synthetic Recall chronology checks, with no scene imports, scientific inputs or rendering.

    python videos/ai/ai15/test_recall_replay_boundary.py
"""

import ast
from pathlib import Path
import unittest

import numpy as np


source = Path(__file__).with_name("s12_recall.py")
tree = ast.parse(source.read_text())
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "replay_prefix")
namespace = {"np": np}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), "exec"), namespace)
replay_prefix = namespace["replay_prefix"]


class ReplayChronologyTests(unittest.TestCase):
    def test_step_zero_never_exposes_future_learning(self):
        steps = np.array([0, 50, 100, 150])
        for future in ([1.0, 0.0, 1.0], [0.0, 0.5, 0.9], [0.5, 0.75, 1.0]):
            xs, ys = replay_prefix(steps, np.array([0.125, *future]), 0)
            np.testing.assert_array_equal(xs, [0, 0])
            np.testing.assert_array_equal(ys, [0.125, 0.125])

    def test_every_checkpoint_shows_only_its_real_history(self):
        steps = np.array([0, 50, 100, 150, 200])
        # A future peak must remain absent until the checkpoint that actually records it.
        values = np.array([0.0, 0.125, 0.25, 1.0, 0.5])
        for checkpoint in range(1, len(steps)):
            with self.subTest(checkpoint=checkpoint):
                xs, ys = replay_prefix(steps, values, checkpoint)
                np.testing.assert_array_equal(xs, steps[:checkpoint + 1])
                np.testing.assert_array_equal(ys, values[:checkpoint + 1])
                self.assertEqual(xs[-1], steps[checkpoint])

    def test_between_checkpoints_matches_the_displayed_counter(self):
        steps = np.array([0, 50, 100])
        values = np.array([0.1, 0.6, 0.9])
        for position in (0.0, 0.1, 0.49, 0.51, 0.99, 1.01, 1.49, 1.51, 1.99, 2.0):
            with self.subTest(position=position):
                xs, ys = replay_prefix(steps, values, position)
                counter_index = min(int(round(position)), len(steps) - 1)
                self.assertEqual(xs[-1], steps[counter_index])
                self.assertEqual(ys[-1], values[counter_index])


if __name__ == "__main__":
    unittest.main(verbosity=2)
