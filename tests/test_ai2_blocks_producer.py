"""Exercise Blocks data orchestration with capped searches, without real search/cache jobs."""
import unittest
from unittest.mock import patch

from videos.ai.ai2 import compute, plan


class BlocksProducerTests(unittest.TestCase):
    def produce(self, bfs_plan, hmax_plan):
        calls = []

        class FixtureBlocks:
            def __init__(self, names):
                self.n = len(names)

            def state(self, towers):
                return 0

            def goal(self, towers):
                return 1

            def F(self, *fact):
                return 1

            def count_states(self, initial):
                return self.n

            def bfs(self, initial, goal):
                # Historical three-block demonstrations stay cheap and complete.
                if self.n == 3:
                    return [], 0
                calls.append((self.n, "bfs"))
                return bfs_plan, 101

            def best_first(self, initial, goal, kind, greedy=False):
                calls.append((self.n, kind, greedy))
                return (hmax_plan, 202) if kind == "max" else ([0], 303)

        with patch.object(plan, "Blocks", FixtureBlocks), \
                patch.object(plan, "random_towers", side_effect=lambda generator, n: [[i] for i in range(n)]), \
                patch.object(plan, "towers_count", side_effect=lambda n: n), \
                patch.object(compute, "rng", return_value=object()), \
                patch.object(compute.CACHE, "load", side_effect=AssertionError("must not load real data")), \
                patch.object(compute.CACHE, "save", side_effect=AssertionError("must not save real data")):
            result = compute.compute_blocks(per_n=1)
        self.assertEqual([row["n"] for row in result["rows"]], list(range(4, 11)))
        self.assertEqual(sum(call[1] == "bfs" for call in calls), 4)
        self.assertEqual(sum(call[1] == "max" for call in calls), 4)
        self.assertEqual(sum(call[1] == "ff" for call in calls), 7)
        for row in result["rows"]:
            self.assertEqual((row["ff"], row["ff_len"]), (303, 1))
            if row["n"] <= 7:
                self.assertEqual((row["bfs"], row["hmax"]), (101, 202))
            else:
                self.assertNotIn("bfs_len", row)
                self.assertNotIn("hmax_len", row)
        return result["rows"][:4]

    def test_bfs_cap_does_not_reject_completed_hmax_or_discard_work(self):
        rows = self.produce(None, [0, 1])
        self.assertTrue(all((row["bfs_len"], row["hmax_len"]) == (-1, 2) for row in rows))

    def test_hmax_cap_does_not_reject_completed_bfs_or_discard_work(self):
        rows = self.produce([0, 1], None)
        self.assertTrue(all((row["bfs_len"], row["hmax_len"]) == (2, -1) for row in rows))

    def test_both_capped_searches_remain_unresolved(self):
        rows = self.produce(None, None)
        self.assertTrue(all((row["bfs_len"], row["hmax_len"]) == (-1, -1) for row in rows))

    def test_equal_completed_plans_including_zero_length_are_retained(self):
        for solution in ([], [0, 1]):
            with self.subTest(solution=solution):
                rows = self.produce(solution, solution)
                self.assertTrue(all(row["bfs_len"] == row["hmax_len"] == len(solution) for row in rows))

    def test_disagreement_between_completed_plans_still_rejected(self):
        for bfs, hmax in (([], [0]), ([0, 1], [0])):
            with self.subTest(bfs=bfs, hmax=hmax):
                with self.assertRaises(AssertionError):
                    self.produce(bfs, hmax)


if __name__ == "__main__":
    unittest.main()
