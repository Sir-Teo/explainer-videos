import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / "videos/ai/ai7/scoreboard_recap.py"
SPEC = importlib.util.spec_from_file_location("scoreboard_recap", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ScoreboardRecapTests(unittest.TestCase):
    def rows(self):
        return {"rows": [{"key": "infini", "bits": 2.0274944483516433},
                         {"key": "best", "bits": 2.3229342233716612},
                         {"key": "kn", "bits": 2.040215092338357}]}

    def test_order_and_values_unchanged(self):
        source = self.rows()
        before = repr(source)
        actual = MODULE.recap_rows(source)
        self.assertEqual([r[0] for r in actual], ["best", "kn", "infini"])
        for key, _, bits in actual:
            self.assertEqual(bits, next(r["bits"] for r in source["rows"] if r["key"] == key))
        self.assertEqual(before, repr(source))

    def test_missing_and_duplicate_rejected(self):
        for rows in [self.rows()["rows"][:-1], self.rows()["rows"] + [self.rows()["rows"][0]]]:
            with self.assertRaises(ValueError):
                MODULE.recap_rows({"rows": rows})

    def test_invalid_scores_rejected(self):
        for value in [float("nan"), float("inf"), -1, True, "2.0"]:
            source = self.rows()
            source["rows"][0]["bits"] = value
            with self.assertRaises(ValueError):
                MODULE.recap_rows(source)

    def test_discloses_comparison_limits(self):
        for phrase in ["different starting positions", "passage-selected", "validation-selected", "Not a matched-cohort"]:
            self.assertIn(phrase, MODULE.COHORT_NOTE)


if __name__ == "__main__":
    unittest.main()
