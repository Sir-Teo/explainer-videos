"""Small arithmetic witnesses for teaching corrections, without science caches."""
import ast
import hashlib
import json
from pathlib import Path
import re
import unittest

import numpy as np
from tools.text_zh_add import validate_input

PART = Path(__file__).resolve().parents[1] / "videos/ai/ai17"


def method(module, name):
    return next(n for n in ast.walk(ast.parse((PART / module).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


class TeachingCorrections(unittest.TestCase):
    def test_on_screen_additions_match_integration_tool_schema(self):
        table = validate_input(json.loads((PART / "text_zh_add.json").read_text()))
        self.assertEqual(table["strings"][r"\text{input reads per MAC}"], r"\text{每次MAC的输入读取数}")

    def test_normal_rounding_bound_for_declared_formats(self):
        # Load only the actual pure quantizer and format constants, never imports,
        # Cache, compute_formats, weights or producer dispatch.
        tree = ast.parse((PART / "compute.py").read_text())
        nodes = [n for n in tree.body if
                 (isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "FORMATS" for t in n.targets)) or
                 (isinstance(n, ast.FunctionDef) and n.name == "quantize")]
        env = {"np": np}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "pure-format-witness", "exec"), env)
        # Hand-sized normal examples around half-way cases and a binade boundary.
        values = np.array([1., 1.03125, 1.0625, 1.25, 1.5, 1.75, 1.9375, 2.])
        for name in ("FP32", "TF32", "BF16", "FP16", "E4M3", "E5M2", "E2M1"):
            m = env["FORMATS"][name][1]
            error = np.abs(env["quantize"](values, name) - values) / values
            self.assertTrue(np.all(error <= 2. ** -(m + 1)), name)

    def test_limits_derivation_does_not_read_weight_experiment(self):
        calls = [n for n in ast.walk(method("s10_formats.py", "derive")) if isinstance(n, ast.Call)]
        self.assertFalse(any(getattr(n.func, "id", None) == "load" for n in calls))

    def test_systolic_display_names_mac_units(self):
        calls = [n for n in ast.walk(method("s09_systolic.py", "count"))
                 if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "cmath"]
        row = next(n for n in calls if n.args and isinstance(n.args[0], ast.Constant)
                   and n.args[0].value == r"\text{input reads per MAC}")
        self.assertEqual(ast.literal_eval(row.args[2]), r"\frac{2nK}{n^2 K}")
        # Two input reads per PE-term amortize across n cells, while each MAC
        # contributes two FLOPs: they must not share the same numeric unit.
        for n in (1, 2, 4, 8):
            k = 3
            input_reads, macs = 2 * n * k, n * n * k
            self.assertEqual(input_reads / macs, 2 / n)
            self.assertEqual(input_reads / (2 * macs), 1 / n)

    def test_bilingual_corrected_records_keep_identity_and_bookmarks(self):
        table = json.loads((PART / "narration_zh.json").read_text())
        bookmark = re.compile(r"<bookmark mark=['\"]([^'\"]+)['\"]/>")
        self.assertEqual(len(table["lines"]), 84)
        for key, entry in table["lines"].items():
            self.assertEqual(key, hashlib.sha1(" ".join(entry["en"].split()).encode()).hexdigest()[:12])
            self.assertEqual(bookmark.findall(entry["en"]), bookmark.findall(entry["zh"]))
        rounding = next(d for d in table["lines"].values() if d["en"].startswith("Two numbers describe a format."))
        self.assertIn("negative of the quantity M plus one", rounding["en"])
        self.assertIn("负（M加1）", rounding["zh"])


if __name__ == "__main__":
    unittest.main()
