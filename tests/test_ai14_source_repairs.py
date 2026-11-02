"""Synthetic scene/narration and cache-contract checks without models or scene imports."""
from __future__ import annotations

import ast
import json
import hashlib
from pathlib import Path
import re
import tempfile
import types
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "videos" / "ai" / "ai14"


class ScientificCacheContractTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.calls = []
        tree = ast.parse((PART / "common.py").read_text())
        body = [node for node in tree.body if
                (isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "_SCIENTIFIC_ITEMS"
                    for target in node.targets)) or
                (isinstance(node, ast.FunctionDef) and node.name == "load")]
        self.namespace = dict(_json=json, _hashlib=hashlib, np=np,
                              _CACHE=types.SimpleNamespace(path=lambda name: self.root / (name + ".json")),
                              _load=lambda name: self.calls.append(name) or {"loaded": name})
        exec(compile(ast.Module(body=body, type_ignores=[]), "<cache contract>", "exec"), self.namespace)
        self.load = self.namespace["load"]

    def save(self, name, data):
        (self.root / (name + ".json")).write_text(json.dumps(data), encoding="utf-8")

    def test_missing_scientific_items_never_reach_the_generating_loader(self):
        for name in sorted(self.namespace["_SCIENTIFIC_ITEMS"]):
            with self.subTest(name=name), self.assertRaises(FileNotFoundError):
                self.load(name)
        self.assertEqual(self.calls, [])

    def test_unversioned_or_incompatible_probes_fail_before_loading(self):
        for data in ({}, {"probe_protocol": "older"}, []):
            self.save("lineage", data)
            with self.assertRaises(ValueError):
                self.load("lineage")
        self.assertEqual(self.calls, [])

    def test_approved_v1_missing_fit_marker_is_preserved_byte_for_byte(self):
        data = {"probe_protocol": "exact-length-batches-v1", "cloze_gpt": 0.25,
                "probe_gpt": 0.5, "gpt_sample": "synthetic fixture"}
        self.save("lineage", data)
        before = (self.root / "lineage.json").read_bytes()
        self.assertEqual(self.load("lineage"), data)
        self.assertEqual((self.root / "lineage.json").read_bytes(), before)
        self.assertNotIn("probe_fit_protocol", self.load("lineage"))
        self.assertEqual(self.calls, [])

    def test_null_unknown_or_v2_fit_at_default_path_is_rejected(self):
        for fit in (None, "older-fit", "fp64-lbfgs-probe-v2"):
            self.save("lineage", {"probe_protocol": "exact-length-batches-v1", "probe_fit_protocol": fit})
            with self.assertRaisesRegex(ValueError, "fit does not match"):
                self.load("lineage")
        self.assertEqual(self.calls, [])

    def test_v1_rejects_v2_only_metadata_with_missing_or_explicit_fp32_marker(self):
        for marker in (False, True):
            for key in ("probe_fit", "candidate_provenance"):
                for value in (None, {"head_dtype": "float64"}):
                    data = {"probe_protocol": "exact-length-batches-v1", key: value}
                    if marker:
                        data["probe_fit_protocol"] = "fp32-lbfgs-probe-v1"
                    self.save("lineage", data)
                    with self.subTest(marker=marker, key=key, value=value), self.assertRaisesRegex(
                        ValueError, "v2-only fit/provenance metadata"
                    ):
                        self.load("lineage")
        self.assertEqual(self.calls, [])

    def test_every_repeat_row_and_snapshot_requires_the_matched_cohort(self):
        for name in ("icl", "icl_base", "gpt_xs", "gpt_s", "gpt_m", "gpt_l"):
            key = "rows" if name.startswith("icl") else "snaps"
            good = {"repeat_protocol": "matched-all-words-v1"}
            for rows in (None, [], [good, {}], [good, {"repeat_protocol": "older"}], [False]):
                self.save(name, {key: rows})
                with self.subTest(name=name, rows=rows), self.assertRaises(ValueError):
                    self.load(name)
        self.assertEqual(self.calls, [])

    def test_valid_contracts_pass_through_without_changing_the_result(self):
        for name in sorted(self.namespace["_SCIENTIFIC_ITEMS"]):
            data = {"probe_protocol": "exact-length-batches-v1", "probe_fit_protocol": "fp32-lbfgs-probe-v1"}
            data["rows" if name.startswith("icl") else "snaps"] = [
                {"repeat_protocol": "matched-all-words-v1"}]
            self.save(name, data)
            self.assertEqual(self.load(name), data)
        self.assertEqual(self.calls, [])

    def test_malformed_scientific_metadata_fails_closed(self):
        (self.root / "family.json").write_text("{unfinished", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.load("family")
        self.assertEqual(self.calls, [])

    def test_scientific_arrays_are_read_without_the_generating_loader(self):
        data = {"snaps": [{"repeat_protocol": "matched-all-words-v1"}]}
        self.save("gpt_m", data)
        np.savez(self.root / "gpt_m.npz", example=np.array([2, 5, 9]))
        result = self.load("gpt_m")
        np.testing.assert_array_equal(result.pop("example"), [2, 5, 9])
        self.assertEqual(result, data)
        self.assertEqual(self.calls, [])

    def test_arrays_cannot_replace_validated_protocol_metadata(self):
        self.save("lineage", {"probe_protocol": "exact-length-batches-v1", "probe_fit_protocol": "fp32-lbfgs-probe-v1"})
        np.savez(self.root / "lineage.npz", probe_protocol=np.array("older"))
        with self.assertRaises(ValueError):
            self.load("lineage")
        self.assertEqual(self.calls, [])

    def test_legacy_npz_cannot_add_fit_or_provenance_metadata_after_validation(self):
        self.save("lineage", {"probe_protocol": "exact-length-batches-v1"})
        for key in ("probe_fit_protocol", "probe_fit", "candidate_provenance", "repeat_protocol"):
            np.savez(self.root / "lineage.npz", **{key: np.array("incompatible")})
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "protocol metadata"):
                self.load("lineage")
        self.assertEqual(self.calls, [])

    def v2_fixture(self):
        self.save("lineage", dict(probe_protocol="exact-length-batches-v1", probe_classes=2,
                                  probe_n_train=4, probe_n_test=2, probe_gpt=0.25, cloze_gpt=0.75))
        data = dict(probe_protocol="exact-length-batches-v1", probe_fit_protocol="fp64-lbfgs-probe-v2",
                    probe_classes=2, probe_n_train=4, probe_n_test=2, probe_gpt=0.5,
                    candidate_provenance=dict(parent_lineage_sha256=hashlib.sha256(
                        (self.root / "lineage.json").read_bytes()).hexdigest()),
                    probe_fit=dict(normalization_dtype="float32", head_dtype="float64", seed=0,
                                   optimizer="LBFGS", lr=1.0, wd=1e-3, max_iter=1000, max_eval=1250,
                                   tolerance_grad=1e-9, tolerance_change=1e-12, history_size=100,
                                   line_search_fn="strong_wolfe", acceptance_gradient_inf=1e-6,
                                   threads=1, accuracy="micro", cohort_sha256="a" * 64,
                                   train_class_counts=[2, 2], test_class_counts=[1, 1]))
        return data

    def test_explicit_v2_uses_separate_artifact_and_default_stays_v1(self):
        data = self.v2_fixture()
        self.save("lineage_probe_v2", data)
        self.assertEqual(self.load("lineage")["probe_gpt"], 0.25)
        self.assertEqual(self.load("lineage", probe_fit_protocol="fp64-lbfgs-probe-v2"), data)
        self.assertEqual(self.load("lineage")["cloze_gpt"], 0.75)
        self.assertEqual(self.calls, [])

    def test_missing_v2_does_not_fall_back_to_available_v1(self):
        self.v2_fixture()
        with self.assertRaisesRegex(FileNotFoundError, "lineage_probe_v2"):
            self.load("lineage", probe_fit_protocol="fp64-lbfgs-probe-v2")
        self.assertEqual(self.calls, [])

    def test_missing_v1_does_not_fall_forward_to_available_v2(self):
        self.save("lineage_probe_v2", self.v2_fixture())
        (self.root / "lineage.json").unlink()
        with self.assertRaises(FileNotFoundError):
            self.load("lineage")
        with self.assertRaises(FileNotFoundError):
            self.load("lineage", probe_fit_protocol="fp64-lbfgs-probe-v2")
        self.assertEqual(self.calls, [])

    def test_v2_requires_its_exact_parent_and_matching_cohort(self):
        for change in ("parent", "probe_classes", "probe_n_train", "probe_n_test"):
            data = self.v2_fixture()
            if change == "parent":
                data["candidate_provenance"]["parent_lineage_sha256"] = "b" * 64
            else:
                data[change] += 1
            self.save("lineage_probe_v2", data)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.load("lineage", probe_fit_protocol="fp64-lbfgs-probe-v2")
        self.assertEqual(self.calls, [])

    def test_v2_rejects_missing_or_incompatible_feature_and_fit_markers(self):
        for key, value in (("probe_protocol", "old-padded"), ("probe_fit_protocol", None),
                           ("probe_fit_protocol", "fp32-lbfgs-probe-v1")):
            data = self.v2_fixture()
            data[key] = value
            self.save("lineage_probe_v2", data)
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.load("lineage", probe_fit_protocol="fp64-lbfgs-probe-v2")
        data.pop("probe_fit_protocol")
        self.save("lineage_probe_v2", data)
        with self.assertRaises(ValueError):
            self.load("lineage", probe_fit_protocol="fp64-lbfgs-probe-v2")
        self.assertEqual(self.calls, [])

    def test_v2_rejects_incompatible_controls_or_incomplete_cohort_metadata(self):
        for key, value in (("head_dtype", "float32"), ("threads", 2), ("acceptance_gradient_inf", 1e-9),
                           ("cohort_sha256", "missing"), ("train_class_counts", [2, 1]),
                           ("test_class_counts", [2, -1]), ("test_class_counts", [True, 1])):
            data = self.v2_fixture()
            data["probe_fit"][key] = value
            self.save("lineage_probe_v2", data)
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.load("lineage", probe_fit_protocol="fp64-lbfgs-probe-v2")
        self.assertEqual(self.calls, [])

    def test_reserved_v2_item_and_unknown_selectors_never_generate(self):
        for name, selector in (("lineage_probe_v2", "fp32-lbfgs-probe-v1"),
                               ("lineage", "unknown"), ("published", "fp64-lbfgs-probe-v2")):
            with self.subTest(name=name, selector=selector), self.assertRaises(ValueError):
                self.load(name, probe_fit_protocol=selector)
        self.assertEqual(self.calls, [])

    def test_only_probe_method_selects_optional_fit(self):
        tree = ast.parse((PART / "s14_ours.py").read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "OurLineage")
        selected = []
        for method in (n for n in cls.body if isinstance(n, ast.FunctionDef)):
            for call in (n for n in ast.walk(method) if isinstance(n, ast.Call)):
                if isinstance(call.func, ast.Name) and call.func.id == "load":
                    if any(k.arg == "probe_fit_protocol" for k in call.keywords):
                        selected.append(method.name)
        self.assertEqual(selected, ["probe"])
        default = next(n for n in cls.body if isinstance(n, ast.Assign) and
                       any(isinstance(t, ast.Name) and t.id == "probe_fit_protocol" for t in n.targets))
        self.assertEqual(ast.literal_eval(default.value), "fp32-lbfgs-probe-v1")

    def test_published_source_derivations_keep_the_existing_loader(self):
        self.assertEqual(self.load("published"), {"loaded": "published"})
        self.assertEqual(self.calls, ["published"])


def assignments(method, names, env):
    tree = ast.parse((PART / "s15_icl.py").read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Emergence")
    fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == method)
    body = [n for n in fn.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
    exec(compile(ast.Module(body=body, type_ignores=[]), "<isolated narrative assignments>", "exec"), env)
    return env


class FamilyRangeTests(unittest.TestCase):
    def claim(self, scores, base=None):
        rows = [dict(name=nm, fewshot=[s]) for nm, s in zip(("gpt_xs", "gpt_s", "gpt_m", "gpt_l"), scores)]
        if base is not None:
            rows.append(dict(name="base", fewshot=[base]))
        return assignments("few_shot", {"fam", "sz", "spread", "v2"}, dict(rows=rows, shots=[8]))["v2"]

    def test_nonmonotonic_intermediate_models_determine_range(self):
        self.assertIn("span about 80 points", self.claim([0.5, 0.9, 0.1, 0.51]))

    def test_base_is_excluded_from_family_range(self):
        self.assertIn("span about 20 points", self.claim([0.5, 0.6, 0.4, 0.51], base=1.0))

    def test_rounded_range_is_approximate_rather_than_a_false_upper_bound(self):
        text = self.claim([0.5, 0.534, 0.51, 0.52])
        self.assertIn("span about 3 points", text)
        self.assertNotIn("within", text)

    def test_endpoint_improvement_claim_remains_an_endpoint_comparison(self):
        self.assertIn("largest of the family beats the smallest by 10 points", self.claim([0.5, 0.9, 0.1, 0.6]))


class CopyingBranchTests(unittest.TestCase):
    def lead(self, passers):
        rows = [dict(name=nm, acc1=0.1, acc2=0.6 if nm in passers else 0.1,
                     loss1=1.0, loss2=1.0) for nm in ("XS", "S", "M", "L", "base")]
        tree = ast.parse((PART / "s15_icl.py").read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Emergence")
        fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "copying")
        body = [n for n in fn.body if
                (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in {"jumps", "copiers"}
                                                 for t in n.targets))
                or (isinstance(n, ast.If) and isinstance(n.test, ast.Name) and n.test.id == "copiers")]
        env = dict(rows=rows, tag_of=lambda r: r["name"], who_of=lambda r: r["name"])
        exec(compile(ast.Module(body=body, type_ignores=[]), "<isolated copying branches>", "exec"), env)
        return env["lead"]

    def test_first_passing_model_does_not_imply_later_models_pass(self):
        self.assertEqual(self.lead({"XS"}),
                         "Model XS is the first in this list to show copying on this test.")
        self.assertEqual(self.lead({"S", "L"}),
                         "Model S is the first in this list to show copying on this test.")

    def test_all_and_base_only_claims_require_their_actual_cohorts(self):
        self.assertEqual(self.lead({"XS", "S", "M", "L", "base"}), "Every one of our models copies.")
        self.assertIn("only the series' own model", self.lead({"base"}))
        self.assertEqual(self.lead(set()), "")


def translator():
    """Execute the existing text-only helper without importing the explainer package."""
    tree = ast.parse((ROOT / "explainer" / "zh_templates.py").read_text())
    tree.body = [n for n in tree.body
                 if not (isinstance(n, ast.ImportFrom) and n.module == "explainer.paths")
                 and not (isinstance(n, ast.FunctionDef) and n.name == "table")]
    tables = {}
    for n in ast.parse((PART / "zh_lines.py").read_text()).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            tables[n.targets[0].id] = ast.literal_eval(n.value)
    ns = dict(video_dir=lambda video: PART, table=lambda video: tables)
    exec(compile(ast.fix_missing_locations(tree), "<text-only translation helper>", "exec"), ns)
    return ns["Translator"]("ai14")


class BilingualWordingTests(unittest.TestCase):
    def test_rounded_scores_and_loss_drops_are_approximate_not_upper_bounds(self):
        tr = translator()
        for score in (0.5531, 0.5779):
            text = assignments("few_shot", {"best0", "v0"}, {"rows": [{"fewshot": [score]}]})["v0"]
            self.assertIn("about", text)
            self.assertNotIn("at most", text)
            self.assertNotIn("up to", text)
            self.assertIn("约", tr(text))
        tree = ast.parse((PART / "s15_icl.py").read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Emergence")
        fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "copying")
        values = [n.value for n in ast.walk(fn) if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "verdict" for t in n.targets)]
        env = dict(first=dict(acc1=0.1, acc2=0.6), who_of=lambda r: "model S",
                   jumps={"S": 0.0}, drop=0.2044)
        text = next(s for value in values if (s := eval(compile(ast.Expression(value), "<copy claim>", "eval"), env))
                    .startswith("None of our models"))
        self.assertIn("about 0.20 nats", text)
        self.assertNotIn("at most", text)
        self.assertIn("约为0.20", tr(text))

    def test_summary_reports_test_bounds_without_a_universal_size_threshold(self):
        env = assignments("verdict", {"t1", "t2", "t3"}, dict(grows=True, copies=False, fs=False))
        tr = translator()
        self.assertIn("twenty points", env["t2"])
        self.assertIn("five points", env["t3"])
        self.assertIn("20个百分点", tr(env["t2"]))
        self.assertIn("5个百分点", tr(env["t3"]))
        tree = ast.parse((PART / "s15_icl.py").read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Emergence")
        fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "verdict")
        call = next(n for n in ast.walk(fn) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover")
        text = eval(compile(ast.Expression(call.args[0]), "<isolated summary wording>", "eval"), env)
        translated = tr(text)
        self.assertIn("do not set a universal parameter threshold", text)
        self.assertIn("普遍适用的参数门槛", translated)
        self.assertEqual(re.findall(r"<bookmark mark='(.*?)'/>", text), ["a", "f", "g", "b"])
        self.assertEqual(re.findall(r"<bookmark mark='(.*?)'/>", translated), ["a", "f", "g", "b"])

    def test_all_cloze_and_probe_outcomes_translate_with_run_scoped_claims(self):
        tree = ast.parse((PART / "s14_ours.py").read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "OurLineage")
        for method, names in (("cloze", ("b_", "g_")), ("probe", ("pb", "pg"))):
            fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == method)
            branch = next(n for n in fn.body if isinstance(n, ast.If) and any(
                isinstance(a, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "verdict" for t in a.targets)
                for a in ast.walk(n)))
            for a, b in ((0.8, 0.5), (0.5, 0.8), (0.5, 0.51)):
                env = dict(zip(names, (a, b)), pct=lambda v: f"{100 * v:.1f}")
                exec(compile(ast.Module(body=[branch], type_ignores=[]), "<isolated task interpretation>", "exec"), env)
                text = env["verdict"]
                self.assertTrue("this run" in text or "this held-out test" in text or "one run" in text
                                or "does not isolate" in text)
                self.assertNotIn("objective hardly matters", text)
                self.assertNotIn("learning from every token seems", text)
                self.assertNotIn("They tie", text)
                translated = translator()(text)
                self.assertIsNotNone(translated, text)
                self.assertNotIn("{", translated)

    def test_loss_gap_is_not_a_memorization_test_in_either_language(self):
        tree = ast.parse((PART / "s14_ours.py").read_text())
        fit = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "fit" for t in n.targets))
        for gap in (-0.6, -0.04, 0.04, 0.6):
            env = {"gap": gap}
            exec(compile(ast.Module(body=[fit], type_ignores=[]), "<isolated loss interpretation>", "exec"), env)
            text = env["fit"]
            self.assertIn("not", text)
            self.assertIn("memorization", text)
            self.assertEqual("within a tenth" in text, abs(gap) < 0.1)
            if abs(gap) >= 0.1:
                self.assertIn(f"{gap:.2f}", text)
            translated = translator()(text)
            self.assertIsNotNone(translated)
            self.assertIn("检验", translated)
            self.assertNotIn("它开始记住", translated)

    def test_factual_timeline_lines_translate_with_original_bookmarks(self):
        tr = translator()
        expected_marks = {"s02_transformer.py": ["a", "b"], "s16_outro.py": list("abcdef")}
        for filename in expected_marks:
            tree = ast.parse((PART / filename).read_text())
            text = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Constant)
                        and isinstance(n.value, str) and "By late 2019" in n.value)
            translated = tr(text)
            self.assertIsNotNone(translated)
            self.assertIn("2019年末", translated)
            self.assertEqual(re.findall(r"<bookmark mark='(.*?)'/>", text), expected_marks[filename])
            self.assertEqual(re.findall(r"<bookmark mark='(.*?)'/>", translated), expected_marks[filename])

    def test_spread_placeholder_translates_without_stale_endpoint_value(self):
        tr = translator()
        source = FamilyRangeTests().claim([0.5, 0.9, 0.1, 0.51])
        translated = tr(source)
        self.assertIsNotNone(translated)
        self.assertIn("80个百分点", translated)
        self.assertNotIn("{", translated)

    def test_both_copying_outcomes_translate_without_circuit_claim(self):
        tr = translator()
        tree = ast.parse((PART / "s15_icl.py").read_text())
        verdicts = [n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "verdict" for t in n.targets)]
        env = dict(first=dict(acc1=0.1, acc2=0.6), who_of=lambda r: "model S",
                   jumps={"S": 0.0}, drop=0.2)
        for node in verdicts:
            text = eval(compile(ast.Expression(node), "<synthetic copying verdict>", "eval"), env)
            translated = tr(text)
            self.assertIsNotNone(translated)
            self.assertNotIn("{", translated)
            self.assertNotIn("hasn't formed", text)
            self.assertNotIn("还没有形成", translated)
            self.assertTrue("separate analysis" in text or "doesn't tell us whether" in text)

    def test_nonmonotonic_copying_lead_and_summary_translate(self):
        tr = translator()
        for text in ("Model S is the first in this list to show copying on this test.",
                     "At least one model shows copying on this test."):
            self.assertIsNotNone(tr(text))


class ProtocolClarityTests(unittest.TestCase):
    def test_owned_caption_entries_resolve_in_the_shared_table(self):
        owned = json.loads((PART / "text_zh_add.json").read_text())["strings"]
        shared = json.loads((ROOT / "videos" / "ai" / "ai_text_zh.json").read_text())["strings"]
        for key, value in owned.items():
            with self.subTest(caption=key):
                self.assertEqual(shared.get(key), value)

    def test_budget_equation_is_explicitly_approximate(self):
        tree = ast.parse((PART / "s14_ours.py").read_text())
        equation = next(n for n in ast.walk(tree) if isinstance(n, ast.Call)
                        and isinstance(n.func, ast.Name) and n.func.id == "cmath"
                        and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == "C")
        self.assertEqual(ast.literal_eval(equation.args[1]), r"\approx")
        self.assertEqual(ast.literal_eval(equation.args[3]), r"\approx")

    def test_fewshot_axis_and_narration_disclose_requested_window(self):
        source = (PART / "s15_icl.py").read_text()
        self.assertIn('xlabel=r"requested examples, $k$"', source)
        self.assertIn("long prompts are left-truncated", source)
        self.assertIn("Long prompts can retain different context for the real and N/A queries.", source)

    def test_new_owned_caption_translations_cover_literal_source_strings(self):
        translations = json.loads((PART / "text_zh_add.json").read_text())["strings"]
        needles = ["illustrative outcomes, not proportions", r"each, \ the same approximate",
                   "same model,", "requested examples,"]
        checked = set()
        for name in ["s04_bert.py", "s14_ours.py", "s15_icl.py"]:
            for n in ast.walk(ast.parse((PART / name).read_text())):
                if isinstance(n, ast.Constant) and isinstance(n.value, str):
                    for needle in needles:
                        if n.value.startswith(needle):
                            self.assertIn(n.value, translations)
                            self.assertRegex(translations[n.value], "[一-鿿]")
                            checked.add(needle)
        self.assertEqual(checked, set(needles))


if __name__ == "__main__":
    unittest.main()
