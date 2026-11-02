"""Portable loader checks using only synthetic temporary cache-format fixtures.

No scene, producer, model, private cache or scientific outcome is imported/read.
"""
import ast
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "videos/ai/ai11/common.py"


def loader(root):
    """Execute the actual owned loader/constants, without importing the scene stack."""
    tree = ast.parse(COMMON.read_text())
    nodes = [n for n in tree.body
             if isinstance(n, ast.FunctionDef) and n.name == "load"
             or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
                and t.id in {"_CORRECTED_ITEMS", "_CACHE_ITEMS"} for t in n.targets)]
    namespace = dict(json=json, np=np, _REPO_ROOT=root,
                     _load_corrected=mock.Mock(side_effect=RuntimeError("frozen manifest required")))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "<actual-part11-cache-reader>", "exec"), namespace)
    return namespace["load"], namespace


def pair(root, name="quad", metadata=None, arrays=None):
    """A generic synthetic Cache.save-compatible pair, not measured results."""
    directory = root / ".cache/ai11"
    directory.mkdir(parents=True, exist_ok=True)
    text = directory / f"{name}.json"
    archive = directory / f"{name}.npz"
    text.write_text(json.dumps({"fixture": "synthetic", "labels": ["a", "b"]}
                               if metadata is None else metadata), encoding="utf-8")
    np.savez_compressed(archive, **({"array": np.array([[1., np.nan], [3., 4.]])}
                                  if arrays is None else arrays))
    return text, archive


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class CacheOnlyGuard(unittest.TestCase):
    def test_corrected_products_delegate_without_legacy_io_even_with_existing_pairs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            read, namespace = loader(root)
            self.assertEqual(namespace["_CORRECTED_ITEMS"], {"race", "ns", "schedule"})
            self.assertFalse(namespace["_CORRECTED_ITEMS"] & namespace["_CACHE_ITEMS"])
            for name in namespace["_CORRECTED_ITEMS"]:
                pair(root, name)
            before = snapshot(root)
            with mock.patch.object(Path, "is_file", side_effect=AssertionError("unexpected existence check")), \
                 mock.patch.object(Path, "read_text", side_effect=AssertionError("unexpected metadata read")), \
                 mock.patch.object(np, "load", side_effect=AssertionError("unexpected array read")):
                for name in ["race", "ns", "schedule"]:
                    with self.subTest(name=name), self.assertRaisesRegex(RuntimeError, "frozen manifest required"):
                        read(name)
            self.assertEqual(namespace["_load_corrected"].call_args_list,
                             [mock.call(name) for name in ("race", "ns", "schedule")])
            namespace["_load_corrected"].side_effect = None
            namespace["_load_corrected"].return_value = {"fixture": "admitted synthetic"}
            self.assertEqual(read("ns"), {"fixture": "admitted synthetic"})
            self.assertEqual(snapshot(root), before)

    def test_other_eleven_names_roundtrip_unchanged_values_without_writes_or_certification(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            read, namespace = loader(root)
            self.assertEqual(namespace["_CACHE_ITEMS"], {
                "race3d", "quad", "river", "noise", "temperature", "eos", "adamview",
                "decay", "natgrad", "equilibrium", "spikes"})
            for name in sorted(namespace["_CACHE_ITEMS"]):
                pair(root, name)
            before = snapshot(root)
            for name in sorted(namespace["_CACHE_ITEMS"]):
                result = read(name)
                self.assertEqual(set(result), {"fixture", "labels", "array"})
                self.assertEqual(result["fixture"], "synthetic")
                self.assertEqual(result["labels"], ["a", "b"])
                np.testing.assert_array_equal(result["array"], [[1., np.nan], [3., 4.]])
            self.assertEqual(snapshot(root), before)  # includes no lock/temp/generated files
            self.assertIn("do not establish input or recipe provenance", read.__doc__)

    def test_missing_or_incomplete_pairs_never_generate_or_create_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            read, _ = loader(root)
            with self.assertRaisesRegex(FileNotFoundError, "cache-only"):
                read("quad")
            self.assertEqual(list(root.iterdir()), [])
            metadata, archive = pair(root)
            for missing in [archive, metadata]:
                contents = missing.read_bytes()
                missing.unlink()
                before = snapshot(root)
                with self.assertRaises(FileNotFoundError):
                    read("quad")
                self.assertEqual(snapshot(root), before)
                missing.write_bytes(contents)

    def test_unknown_and_traversal_names_fail_before_io(self):
        with tempfile.TemporaryDirectory() as temporary:
            read, _ = loader(Path(temporary))
            with mock.patch.object(Path, "is_file", side_effect=AssertionError("unexpected path access")):
                for name in ["", "../quad", "quad/../race", "quad.json", "other", None, ["quad"]]:
                    with self.subTest(name=name), self.assertRaises(ValueError):
                        read(name)

    def test_malformed_or_empty_json_rejected_without_array_reads(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            read, _ = loader(root)
            metadata, _ = pair(root)
            for payload in ["{", "[]", "{}", "42", "null"]:
                metadata.write_text(payload)
                with mock.patch.object(np, "load", side_effect=AssertionError("unexpected array read")):
                    with self.subTest(payload=payload), self.assertRaises(ValueError):
                        read("quad")

    def test_corrupt_empty_wrong_format_and_duplicate_npz_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            read, _ = loader(root)
            _, archive = pair(root)
            archive.write_bytes(b"malformed synthetic archive")
            with self.assertRaises(ValueError):
                read("quad")
            np.savez(archive)
            with self.assertRaisesRegex(ValueError, "nonempty and unique"):
                read("quad")
            with archive.open("wb") as file:
                np.save(file, np.array([1, 2]))
            with self.assertRaisesRegex(ValueError, "NPZ archive"):
                read("quad")
            payload = io.BytesIO()
            np.save(payload, np.array([1, 2]))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(archive, "w") as file:
                    file.writestr("duplicate.npy", payload.getvalue())
                    file.writestr("duplicate.npy", payload.getvalue())
            with self.assertRaisesRegex(ValueError, "nonempty and unique"):
                read("quad")

    def test_json_array_overlap_is_not_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            read, _ = loader(root)
            pair(root, metadata={"array": "synthetic scalar"}, arrays={"array": np.array([1, 2])})
            before = snapshot(root)
            with self.assertRaisesRegex(ValueError, "must not overlap"):
                read("quad")
            self.assertEqual(snapshot(root), before)

    def test_untrusted_pickle_payload_is_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            read, _ = loader(root)
            pair(root, arrays={"payload": np.array(["untrusted synthetic object"], dtype=object)})
            original = np.load
            with mock.patch.object(np, "load", wraps=original) as observed:
                with self.assertRaisesRegex(ValueError, "allow_pickle=False"):
                    read("quad")
            self.assertIs(observed.call_args.kwargs["allow_pickle"], False)

    def test_source_has_no_producer_cache_alias_or_environment_bypass(self):
        tree = ast.parse(COMMON.read_text())
        self.assertFalse(any(isinstance(n, ast.ImportFrom) and n.module == "compute" for n in tree.body))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "load")
        self.assertFalse(any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(fn)))
        self.assertFalse(any(isinstance(n, ast.Name) and n.id in {"Cache", "compute", "os", "importlib"}
                             for n in ast.walk(fn)))


if __name__ == "__main__":
    unittest.main()
