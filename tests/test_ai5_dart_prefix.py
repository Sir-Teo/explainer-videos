"""Exercise the actual display-prefix helper without loading scene data or models."""
import ast
from pathlib import Path
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "videos/ai/ai5/s13_montecarlo.py"


def actual_prefix():
    tree = ast.parse(SOURCE.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "set_dart_prefix")
    scope = {}
    exec(compile(ast.Module([node], type_ignores=[]), str(SOURCE), "exec"), scope)
    return scope["set_dart_prefix"]


class Dot:
    def __init__(self, index):
        self.index, self.opacity, self.calls = index, 1, 0

    def set_opacity(self, opacity):
        self.opacity = opacity
        self.calls += 1


class Dots(list):
    pass


class DartPrefixTests(unittest.TestCase):
    def test_replay_rewinds_and_subsequent_prefix_matches_live_total(self):
        update = actual_prefix()
        dots = Dots(Dot(i) for i in range(1500))
        for count in [0, 1, 24, 1, 2, 7, 24, 25, 1499, 1500, 1501, 4000]:
            with self.subTest(count=count):
                self.assertIs(update(dots, count), dots)
                self.assertEqual([d.index for d in dots if d.opacity], list(range(min(count, 1500))))

    def test_fractional_animation_and_unchanged_count_do_not_reveal_future_darts(self):
        update = actual_prefix()
        dots = Dots(Dot(i) for i in range(31))
        update(dots, 7.999)
        self.assertEqual(sum(d.opacity for d in dots), 7)
        calls = [d.calls for d in dots]
        update(dots, 7.1)
        self.assertEqual([d.calls for d in dots], calls)
        update(dots, 8)
        self.assertEqual([d.calls - old for d, old in zip(dots, calls)], [int(i == 7) for i in range(31)])

    def test_empty_and_outside_counts_are_bounded(self):
        update = actual_prefix()
        for size in [0, 1, 3]:
            dots = Dots(Dot(i) for i in range(size))
            for count in [-30, 0, 100, -1]:
                update(dots, count)
                self.assertEqual(sum(d.opacity for d in dots), min(max(count, 0), size))


if __name__ == "__main__":
    unittest.main()
