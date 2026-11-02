"""Bounded synthetic tests: no renderer, producer, model, corpus or network needed."""

import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from contextlib import ExitStack
import warnings
import zipfile

import numpy as np


spec = importlib.util.spec_from_file_location("part15_cache_inputs", Path(__file__).with_name("cache_inputs.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CacheInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / ".cache" / "ai15"
        self.contract = {"schema": 1, "items": {}}
        self.reader = module.ReadOnlyInputs(self.root, self.contract)

    def put(self, suffix, raw):
        self.directory.mkdir(parents=True, exist_ok=True)
        (self.directory / f"sample.{suffix}").write_bytes(raw)
        self.contract["items"].setdefault("sample", {})[suffix] = {
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()
        }

    def arrays(self, values):
        stream = io.BytesIO()
        np.savez(stream, **values)
        self.put("npz", stream.getvalue())
        self.contract["items"]["sample"]["arrays"] = {
            key: {"shape": list(value.shape), "dtype": value.dtype.str} for key, value in values.items()
        }

    def test_missing_input_fails_without_creating_any_directory(self):
        self.contract["items"]["sample"] = {"json": {"bytes": 2, "sha256": "0" * 64}}
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_correction_gates_precede_all_filesystem_access(self):
        with ExitStack() as stack:
            for method in ["read_bytes", "resolve", "is_symlink", "is_file", "exists"]:
                stack.enter_context(patch.object(Path, method, side_effect=AssertionError("filesystem access")))
            for name in ["selfcache", "scoreboard"]:
                with self.subTest(name=name), self.assertRaises(module.CacheInputError):
                    module.load(name)

    def test_exact_approved_json_and_arrays_load_without_mutation(self):
        self.put("json", b'{"label":"synthetic"}')
        values = {"x": np.arange(6, dtype=np.float32).reshape(2, 3)}
        self.arrays(values)
        before = {p.name: p.read_bytes() for p in self.directory.iterdir()}
        loaded = self.reader.load("sample")
        np.testing.assert_array_equal(loaded["x"], values["x"])
        self.assertEqual(loaded["label"], "synthetic")
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir()})

    def test_changed_input_is_rechecked_on_every_load(self):
        self.put("json", b'{"value":1}')
        self.assertEqual(self.reader.load("sample")["value"], 1)
        (self.directory / "sample.json").write_bytes(b'{"value":2}')
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")

    def test_symlink_root_is_not_silently_resolved(self):
        link = self.root / "alias"
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(module.CacheInputError):
            module.ReadOnlyInputs(link, self.contract)

    def test_oversized_input_is_rejected_before_read(self):
        self.put("json", b'{}')
        (self.directory / "sample.json").write_bytes(b' ' * 256)
        with patch.object(Path, "open", side_effect=AssertionError("oversized read")):
            with self.assertRaises(module.CacheInputError):
                self.reader.load("sample")

    def test_duplicate_and_nonfinite_json_rejected_even_when_hash_matches(self):
        for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":[1e999]}']:
            with self.subTest(raw=raw):
                self.put("json", raw)
                with self.assertRaises(module.CacheInputError):
                    self.reader.load("sample")

    def test_invalid_names_and_unknown_items_cannot_escape_contract(self):
        for name in ["../other", "/absolute", "sample.json", "unknown", [], None]:
            with self.subTest(name=name), self.assertRaises(module.CacheInputError):
                self.reader.load(name)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_symlink_file_and_directory_are_rejected(self):
        self.put("json", b'{}')
        path = self.directory / "sample.json"
        target = self.root / "other.json"
        target.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(target)
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")
        path.unlink()
        self.directory.rmdir()
        external = self.root / "external"
        external.mkdir()
        (external / "sample.json").write_bytes(b'{}')
        self.directory.symlink_to(external, target_is_directory=True)
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")

    def test_unlisted_sidecars_and_missing_approved_arrays_fail(self):
        self.put("json", b'{}')
        p = self.directory / "sample.npz"
        p.write_bytes(b"unlisted")
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")
        self.arrays({"x": np.arange(2)})
        p.unlink()
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")

    def test_object_arrays_and_schema_drift_fail(self):
        self.put("json", b'{}')
        self.arrays({"x": np.array([object()], dtype=object)})
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")
        self.arrays({"x": np.arange(2, dtype=np.int64)})
        self.contract["items"]["sample"]["arrays"]["x"]["shape"] = [1, 2]
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")

    def test_duplicate_zip_members_and_json_array_collisions_fail(self):
        self.put("json", b'{"x":0}')
        self.arrays({"x": np.arange(2)})
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")
        self.put("json", b'{}')
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("nested/x.npy", b"invalid")
        self.put("npz", stream.getvalue())
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")
        stream = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(stream, "w") as archive:
                archive.writestr("x.npy", b"first")
                archive.writestr("x.npy", b"second")
        self.put("npz", stream.getvalue())
        with self.assertRaises(module.CacheInputError):
            self.reader.load("sample")


if __name__ == "__main__":
    unittest.main(verbosity=2)
