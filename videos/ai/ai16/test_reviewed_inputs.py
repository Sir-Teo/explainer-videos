"""Bounded synthetic contracts for the read-only Part 16 scene loader.

Run this file directly with Python (also under -O). Fixtures are temporary,
invented schema examples; no scenes, real caches, scientific models or renderer
are imported, generated or evaluated.
"""

import builtins
import copy
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import numpy as np

_PATH = Path(__file__).with_name("reviewed_inputs.py")
_SPEC = importlib.util.spec_from_file_location("part16_synthetic_input_contracts", _PATH)
inputs = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(inputs)


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ReviewedInputs(unittest.TestCase):
    def setUp(self):
        self.directory = self.enterContext(tempfile.TemporaryDirectory())
        self.root = Path(self.directory)
        self.enterContext(mock.patch.object(inputs, "_ROOT", self.root))
        sources = {}
        for relative in inputs._SOURCES:
            data = ("# synthetic source fixture: " + Path(relative).name + "\n").encode()
            self.write(relative, data)
            sources[relative] = digest(data)
        self.manifest = {"schema_version": 1, "part": "ai16", "compatibility_sources": sources, "products": {}}
        self.product("configs", {"fixture": "synthetic"})

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def save_manifest(self):
        self.write(inputs._MANIFEST, json.dumps(self.manifest).encode())

    def product(self, name, data, arrays=None):
        raw = json.dumps(data).encode()
        self.write(f".cache/ai16/{name}.json", raw)
        descriptor = None
        if arrays is not None:
            buffer = io.BytesIO()
            np.savez_compressed(buffer, **arrays)
            payload = buffer.getvalue()
            self.write(f".cache/ai16/{name}.npz", payload)
            descriptor = {"bytes": len(payload), "sha256": digest(payload),
                          "arrays": {k: {"dtype": str(v.dtype), "shape": list(v.shape)} for k, v in arrays.items()}}
        self.manifest["products"][name] = {
            "json": {"bytes": len(raw), "sha256": digest(raw)}, "npz": descriptor,
            "review": {"accepted": True, "recipe": "within-window-v2" if name == inputs._SPECIAL else "original-recipe",
                       "producer_sha256": digest(b"synthetic producer"),
                       "input_sha256": {"fixture": digest(b"synthetic input")}}}
        self.save_manifest()

    def files(self):
        return {str(p.relative_to(self.root)): digest(p.read_bytes()) for p in self.root.rglob("*")
                if p.is_file() and not p.is_symlink()}

    def fails(self, name="configs"):
        before = self.files()
        with self.assertRaises(inputs.ReviewedInputError):
            inputs.load(name)
        self.assertEqual(self.files(), before)

    def special(self):
        """Synthetic constant-label population with k distinct, equally used experts."""
        population = 256 * 63
        result = {"schema_version": 2, "version": inputs._SPECIAL, "status": "historical-pending-review",
                  "seeds": [0, 1, 2], "modes": ["moe", "fine"],
                  "seeds_by_mode": {"moe": [0, 1, 2], "fine": [0, 1]}, "seed_counts": {"moe": 3, "fine": 2},
                  "classes": list(inputs._CLASSES), "route_chars": ["?"],
                  "sampling": {"window_count": 256, "context": 64, "retained_positions": list(range(1, 64)),
                               "excluded_positions": [0], "matched_tokens": population, "original_tokens": 256 * 64}}
        for mode, seeds in result["seeds_by_mode"].items():
            experts, choices = (8, 2) if mode == "moe" else (32, 8)
            counts = [population if i < choices else 0 for i in range(experts)]
            probability = [v / (population * choices) for v in counts]
            for seed in seeds:
                for layer in range(2):
                    result[f"{mode}_s{seed}_l{layer}"] = {
                        "mode": mode, "seed": seed, "layer": layer, "model_key": f"{mode}_s{seed}",
                        "checkpoint_sha256": digest(f"synthetic {mode} {seed}".encode()),
                        "E": experts, "k": choices, "token_count": population, "slot_count": population * choices,
                        "cur": 0.0, "nxt": 0.0, "prv": 0.0, "shuf": 0.0, "H": math.log2(choices),
                        "classes": [[0.0] * experts for _ in range(4)] + [probability[:]],
                        "class_counts": [[0] * experts for _ in range(4)] + [counts[:]],
                        "class_token_counts": [0, 0, 0, 0, population],
                        "class_slot_counts": [0, 0, 0, 0, population * choices],
                        "table": [probability[:]], "route_counts": [counts[:]],
                        "route_char_token_counts": [population], "route_char_slot_counts": [population * choices]}
        return result

    def test_valid_json_returns_fresh_values_without_writes(self):
        before = self.files()
        data = inputs.load("configs")
        self.assertEqual(data, {"fixture": "synthetic"})
        data["fixture"] = "changed in caller"
        self.assertEqual(inputs.load("configs"), {"fixture": "synthetic"})
        self.assertEqual(self.files(), before)

    def test_missing_manifest_has_no_fallback(self):
        (self.root / inputs._MANIFEST).unlink()
        self.fails()

    def test_manifest_version_part_and_source_inventory(self):
        original = copy.deepcopy(self.manifest)
        for change in [lambda d: d.update(schema_version=True), lambda d: d.update(schema_version=2),
                       lambda d: d.update(part="another-part"), lambda d: d.update(compatibility_sources={}),
                       lambda d: d["compatibility_sources"].pop(next(iter(inputs._SOURCES)))]:
            with self.subTest(change=change):
                self.manifest = copy.deepcopy(original)
                change(self.manifest)
                self.save_manifest()
                self.fails()

    def test_source_missing_or_mismatched(self):
        path = self.root / next(iter(inputs._SOURCES))
        path.write_bytes(b"changed source")
        self.fails()
        path.unlink()
        self.fails()

    def test_disallowed_names_and_legacy_do_not_load(self):
        self.write(".cache/ai16/special.json", b"{}")
        for name in ["special", "lm_runs", "../configs", "/configs", "configs.json", None, 1]:
            with self.subTest(name=name):
                self.fails(name)

    def test_unsupported_manifest_product(self):
        self.manifest["products"]["special"] = self.manifest["products"]["configs"]
        self.save_manifest()
        self.fails()

    def test_missing_product_and_explicit_npz_declaration(self):
        self.manifest["products"] = {}
        self.save_manifest()
        self.fails()
        self.product("configs", {})
        del self.manifest["products"]["configs"]["npz"]
        self.save_manifest()
        self.fails()

    def test_review_recipe_and_provenance_required(self):
        original = copy.deepcopy(self.manifest)
        for field, value in [("accepted", False), ("accepted", "true"), ("recipe", "original-recipe-pending"),
                             ("producer_sha256", "missing"), ("input_sha256", {}),
                             ("input_sha256", {"fixture": "bad"})]:
            with self.subTest(field=field, value=value):
                self.manifest = copy.deepcopy(original)
                self.manifest["products"]["configs"]["review"][field] = value
                self.save_manifest()
                self.fails()
        self.manifest = copy.deepcopy(original)
        del self.manifest["products"]["configs"]["review"]
        self.save_manifest()
        self.fails()

    def test_json_size_digest_corruption_and_missing(self):
        path = self.root / ".cache/ai16/configs.json"
        path.write_bytes(b"different")
        self.fails()
        path.unlink()
        self.fails()
        self.product("configs", {})
        for field, value in [("bytes", True), ("bytes", -1), ("sha256", "not-a-digest")]:
            self.manifest["products"]["configs"]["json"][field] = value
            self.save_manifest()
            self.fails()

    def test_strict_json_rejects_duplicates_nonfinite_and_nonobjects(self):
        for raw in [b'{"x":1,"x":2}', b'{"nested":{"x":1,"x":2}}', b'{"x":NaN}',
                    b'{"x":Infinity}', b'{"x":1e999}', b'[]', b'not json']:
            with self.subTest(raw=raw):
                self.write(".cache/ai16/configs.json", raw)
                self.manifest["products"]["configs"]["json"] = {"bytes": len(raw), "sha256": digest(raw)}
                self.save_manifest()
                self.fails()

    def test_required_npz_and_array_contracts(self):
        self.product("configs", {}, {"x": np.arange(6, dtype=np.int64).reshape(2, 3)})
        before = self.files()
        data = inputs.load("configs")
        np.testing.assert_array_equal(data["x"], np.arange(6).reshape(2, 3))
        data["x"][:] = 0
        self.assertEqual(int(inputs.load("configs")["x"].sum()), 15)
        self.assertEqual(self.files(), before)
        original = copy.deepcopy(self.manifest)
        for change in [lambda d: d.update(arrays={}),
                       lambda d: d["arrays"]["x"].update(shape=[6]),
                       lambda d: d["arrays"]["x"].update(shape=[True, 3]),
                       lambda d: d["arrays"]["x"].update(dtype="float64")]:
            with self.subTest(change=change):
                self.manifest = copy.deepcopy(original)
                change(self.manifest["products"]["configs"]["npz"])
                self.save_manifest()
                self.fails()
        self.manifest = original
        self.save_manifest()
        (self.root / ".cache/ai16/configs.npz").unlink()
        self.fails()

    def test_npz_objects_nonfinite_and_key_collisions(self):
        for arrays in [{"x": np.array([object()], dtype=object)}, {"x": np.array([np.nan])},
                       {"x": np.array([np.inf])}]:
            with self.subTest(dtype=arrays["x"].dtype):
                self.product("configs", {}, arrays)
                self.fails()
        self.product("configs", {"x": 1}, {"x": np.array([2])})
        self.fails()

    def test_unexpected_npz_and_partial_siblings(self):
        for suffix in [".npz", ".partial.json", ".tmp.json", ".tmp.npz"]:
            with self.subTest(suffix=suffix):
                path = self.write(".cache/ai16/configs" + suffix, b"unexpected")
                self.fails()
                path.unlink()

    def test_symlink_and_nonregular_inputs_are_rejected(self):
        path = self.root / ".cache/ai16/configs.json"
        data = path.read_bytes()
        path.unlink()
        target = self.write("synthetic-target", data)
        path.symlink_to(target)
        self.fails()
        path.unlink()
        path.mkdir()
        self.fails()

    def test_parent_directory_symlink_is_rejected(self):
        path = self.root / "videos/ai/ai16"
        target = path.with_name("synthetic-source-target")
        path.rename(target)
        path.symlink_to(target, target_is_directory=True)
        self.fails()

    def test_fresh_verification_after_manifest_or_data_changes(self):
        inputs.load("configs")
        self.manifest["products"]["configs"]["review"]["accepted"] = False
        self.save_manifest()
        self.fails()
        self.product("configs", {"fixture": "new synthetic fixture"})
        self.assertEqual(inputs.load("configs")["fixture"], "new synthetic fixture")
        (self.root / ".cache/ai16/configs.json").write_bytes(b"changed after successful call")
        self.fails()

    def test_parser_uses_the_verified_bytes_not_a_second_path_read(self):
        original = inputs._verified

        def replace_after_read(relative, identity):
            data = original(relative, identity)
            if relative.endswith("configs.json"):
                (self.root / relative).write_bytes(b"unreviewed replacement")
            return data

        with mock.patch.object(inputs, "_verified", replace_after_read):
            self.assertEqual(inputs.load("configs"), {"fixture": "synthetic"})
        self.fails()

    def test_input_changing_during_descriptor_read_is_rejected(self):
        path = self.root / ".cache/ai16/configs.json"
        inode = path.stat().st_ino
        original = inputs.os.read
        changed = False

        def changing_read(descriptor, count):
            nonlocal changed
            data = original(descriptor, count)
            if not changed and inputs.os.fstat(descriptor).st_ino == inode:
                changed = True
                with path.open("ab") as stream:
                    stream.write(b"x")
            return data

        with mock.patch.object(inputs.os, "read", changing_read):
            with self.assertRaises(inputs.ReviewedInputError):
                inputs.load("configs")
        self.assertTrue(changed)

    def test_corrected_special_requires_its_own_reviewed_input(self):
        self.write(".cache/ai16/special.json", b"{}")
        self.fails(inputs._SPECIAL)
        fixture = self.special()
        self.product(inputs._SPECIAL, fixture)
        before = self.files()
        self.assertEqual(inputs.load(inputs._SPECIAL), fixture)
        self.assertEqual(self.files(), before)
        self.assertEqual(inputs.load(inputs._SPECIAL)["status"], "historical-pending-review")

    def test_special_protocol_and_identity_mismatches(self):
        original = self.special()
        changes = [lambda d: d.update(version="special"), lambda d: d.update(schema_version=1),
                   lambda d: d.update(seeds=[False, 1, 2]), lambda d: d["seeds_by_mode"].update(fine=[0, 1, 2]),
                   lambda d: d["sampling"].update(matched_tokens=16384),
                   lambda d: d["sampling"].update(retained_positions=list(range(64))),
                   lambda d: d.pop("fine_s1_l1"), lambda d: d.update(moe_s0_l2=d["moe_s0_l0"]),
                   lambda d: d["moe_s0_l0"].update(token_count=16384),
                   lambda d: d["moe_s0_l0"].update(slot_count=1),
                   lambda d: d["fine_s0_l0"].update(E=8),
                   lambda d: d["moe_s0_l0"].update(seed=True),
                   lambda d: d["moe_s0_l0"].update(model_key="another_model")]
        for change in changes:
            with self.subTest(change=change):
                data = copy.deepcopy(original)
                change(data)
                self.product(inputs._SPECIAL, data)
                self.fails(inputs._SPECIAL)

    def test_special_shape_count_probability_and_entropy_mismatches(self):
        original = self.special()
        changes = [lambda r: r.update(classes=[]), lambda r: r["route_counts"][0].__setitem__(0, -1),
                   lambda r: r["route_char_slot_counts"].__setitem__(0, 1),
                   lambda r: r["table"][0].__setitem__(0, 0.25), lambda r: r.update(H=9),
                   lambda r: r.update(cur=r["H"] + 1), lambda r: r.update(cur=-1)]
        for change in changes:
            with self.subTest(change=change):
                data = copy.deepcopy(original)
                change(data["moe_s0_l0"])
                self.product(inputs._SPECIAL, data)
                self.fails(inputs._SPECIAL)
        self.product(inputs._SPECIAL, original, {"extra": np.array([1])})
        self.fails(inputs._SPECIAL)

    def test_import_and_load_do_not_enter_scientific_modules(self):
        original = builtins.__import__

        def guarded(name, *args, **kwargs):
            if name == "torch" or name == "explainer" or name.startswith(("explainer.", "videos.")):
                raise AssertionError("Scientific/scene import attempted")
            return original(name, *args, **kwargs)

        spec = importlib.util.spec_from_file_location("isolated_part16_import_contract", _PATH)
        module = importlib.util.module_from_spec(spec)
        before = self.files()
        with mock.patch.object(builtins, "__import__", guarded):
            spec.loader.exec_module(module)
            module._ROOT = self.root
            self.assertEqual(module.load("configs"), {"fixture": "synthetic"})
        self.assertEqual(self.files(), before)

    def test_non_chinese_caption_check_is_a_noop(self):
        before = self.files()
        inputs.validate_captions("en")
        self.assertEqual(self.files(), before)

    def test_chinese_captions_do_not_fall_back_if_public_table_is_missing(self):
        before = self.files()
        with self.assertRaises(inputs.ReviewedInputError):
            inputs.validate_captions("zh")
        self.assertEqual(self.files(), before)

    def test_chinese_captions_require_installed_exact_strings_and_patterns(self):
        local = {"strings": {"synthetic label": "示例标签"}, "patterns": [[r"fixture (\d+)", r"示例 \1"]]}
        self.write("videos/ai/ai16/text_zh_reviewed.json", json.dumps(local).encode())
        self.write("videos/ai/ai_text_zh.json", json.dumps(local).encode())
        before = self.files()
        inputs.validate_captions("zh")
        self.assertEqual(self.files(), before)
        for shared in [{"strings": {}, "patterns": local["patterns"]},
                       {"strings": local["strings"], "patterns": []},
                       {"strings": local["strings"], "patterns": local["patterns"] + [[r"fixture (\d+)", "wrong"]]},
                       {"strings": local["strings"], "patterns": [["(", "invalid regex"]]}]:
            self.write("videos/ai/ai_text_zh.json", json.dumps(shared).encode())
            before = self.files()
            with self.assertRaises(inputs.ReviewedInputError):
                inputs.validate_captions("zh")
            self.assertEqual(self.files(), before)


if __name__ == "__main__":
    unittest.main()
