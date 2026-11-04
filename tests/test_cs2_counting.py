"""Computer Science, Built, Part 2: the searches and counts behind the scenes, and the problem answers."""

import itertools
import math
import unittest

from videos.cs.cs2 import compute as c


class Part2(unittest.TestCase):
    def test_puzzle_invariant_splits_positions_in_half(self):
        for rows, cols in ((2, 2), (2, 3)):
            n = rows * cols
            solved = tuple(list(range(1, n)) + [0])
            reach = c.bfs(solved, rows, cols)
            self.assertEqual(len(reach), math.factorial(n) // 2)
            for p in itertools.permutations(range(n)):
                self.assertEqual(p in reach, c.invariant(p, rows, cols) == 0)

    def test_problem_2_and_6(self):
        swapped = (2, 1, 3, 4, 5, 6, 7, 8, 0)
        self.assertEqual(c.invariant(swapped, 3, 3), 1)
        d = c.bfs((1, 2, 3, 4, 5, 6, 7, 0), 2, 4)
        self.assertEqual(len(d), 20160)
        self.assertEqual(max(d.values()), 36)
        self.assertEqual(sum(1 for v in d.values() if v == 36), 1)

    def test_jugs_and_tromino(self):
        out = c.compute_jugs()
        self.assertEqual(len(out["path"]) - 1, 6)
        self.assertEqual(out["path"][-1]["state"], [3, 4])
        self.assertEqual(len(c.tromino(3, (5, 2))), 21)

    def test_counts(self):
        self.assertEqual([c.derangements(n) for n in range(7)], [1, 0, 1, 2, 9, 44, 265])
        self.assertEqual(len(c.dyck(4)), 14)
        self.assertEqual(c.labels([6, 2, 9, 4, 10, 1, 7, 3, 8, 5])[0][8], 4)

    def test_problem_5(self):
        self.assertEqual([x for x in range(140) if x % 4 == 1 and x % 5 == 2 and x % 7 == 3], [17])


if __name__ == "__main__":
    unittest.main()
