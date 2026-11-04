"""The Coverage Board's verdicts (explainer.stats.board): kept within 3 Monte Carlo standard errors of nominal; for
an interval, low coverage is broken and high is conservative; for a test, a high false-alarm rate is broken."""

import math
import unittest

from explainer.stats.board import BROKEN, CONSERVATIVE, KEPT, Row, verdict


class BoardTests(unittest.TestCase):
    def test_interval_verdicts(self):
        se = math.sqrt(0.95 * 0.05 / 10_000)
        self.assertEqual(verdict("coverage", 0.95, 0.95 + 2.9 * se, 10_000), KEPT)
        self.assertEqual(verdict("coverage", 0.95, 0.95 - 3.1 * se, 10_000), BROKEN)
        self.assertEqual(verdict("coverage", 0.95, 0.95 + 3.1 * se, 10_000), CONSERVATIVE)

    def test_test_verdicts_point_the_other_way(self):
        se = math.sqrt(0.05 * 0.95 / 10_000)
        self.assertEqual(verdict("size", 0.05, 0.05 + 3.1 * se, 10_000), BROKEN)
        self.assertEqual(verdict("size", 0.05, 0.05 - 3.1 * se, 10_000), CONSERVATIVE)

    def test_row_uses_the_rule(self):
        r = Row(part=8, method="z", setting="n = 5", kind="coverage", nominal=0.95, achieved=0.88, reps=10_000)
        self.assertEqual(r.verdict, BROKEN)


if __name__ == "__main__":
    unittest.main()
