"""Portable contract checks with explicitly synthetic temporary capsules.

Only source text is read from the checkout. No experiment data, producer, model,
scene stack or private evidence is imported; the test-only trust anchor is for
these fixtures, never an alternate production admission interface.
"""
import ast
import hashlib
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
SOURCE = ROOT / "videos/ai/ai11/contracts.py"


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def actual_reader(root):
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    tree.body = [node for node in tree.body
                 if not isinstance(node, ast.ImportFrom) or node.module != "explainer.paths"]
    namespace = {"_REPO_ROOT": root, "__name__": "synthetic_contract_reader"}
    exec(compile(tree, str(SOURCE), "exec"), namespace)
    return namespace


class SyntheticCapsule:
    def __init__(self, root):
        self.root = root
        self.ns = actual_reader(root)
        n = self.ns
        generated = {}
        epoch = {}
        for path in sorted(n["_SOURCE_PATHS"]):
            # Read code as bytes only, to exercise the actual three fixed pins.
            blob = ((ROOT / path).read_bytes() if path in n["_OWN_SOURCES"]
                    else f"synthetic source fixture: {path}\n".encode())
            self.write(path, blob, readonly=False)
            generated[path] = sha(blob)
            epoch[path] = self.artifact(n["_CAPSULE"] + "recipe-sources/" + path, blob)
        originals = {}
        for path in sorted(n["_INPUT_PATHS"]):
            descriptor = self.artifact(path, f"synthetic input: {path}\n".encode())
            originals[path] = {k: descriptor[k] for k in ("bytes", "sha256")}
        runtime = {"python": "synthetic recorded Python", "packages":
                   {key: "synthetic recorded version" for key in ("manim", "numpy", "pillow", "scipy", "torch")}}
        self.manifest = {
            "schema": n["_SCHEMA"], "generation_baseline": n["_BASELINE"], "kind": n["_KIND"],
            "correction_patch_sha256": n["_PATCH"], "generation_source_hashes": generated,
            "current_source_hashes": {p: h for p, h in generated.items() if p != n["_CAPTION_PATH"]},
            "presentation_only_current_exclusion": [n["_CAPTION_PATH"]], "epoch_sources": epoch,
            "original_inputs": originals, "products": {}, "runtime": runtime, "limits": n["_LIMITS"],
            "source_reviews": {key: self.artifact(n["_CAPSULE"] + "reviews/" + key, b"synthetic review fixture\n")
                               for key in ("INDEPENDENT-REVIEW.md", "TORCH-SYNTHETIC-REVIEW.md")}}
        for item in ("race", "ns", "schedule"):
            buffer = io.BytesIO()
            np.savez_compressed(buffer, fixture_array=np.array([[1., np.nan], [3., 4.]]))
            self.manifest["products"][item] = {
                "dependencies": [] if item == "race" else ["race"],
                "files": {"json": self.artifact(n["_PRODUCTS"] + item + ".json", b'{"fixture": "synthetic only"}'),
                          "npz": self.artifact(n["_PRODUCTS"] + item + ".npz", buffer.getvalue())},
                "review": self.artifact(n["_CAPSULE"] + "reviews/" + item + ".md", b"synthetic result review\n")}
        for item in ("race", "ns", "schedule"):
            self.set_receipt(item, self.receipt(item))
        self.seal()

    def write(self, path, blob, readonly=True):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target.chmod(0o644)
        target.write_bytes(blob)
        target.chmod(0o444 if readonly else 0o644)

    def artifact(self, path, blob):
        self.write(path, blob)
        return {"path": path, "bytes": len(blob), "sha256": sha(blob)}

    def receipt(self, item):
        n, m = self.ns, self.manifest
        threads = {p: "1" for p in ("AI11_THREADS", "AI11_WORKERS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                    "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")}
        originals = {p: d["sha256"] for p, d in m["original_inputs"].items()}
        reservation = {"source_hashes": m["generation_source_hashes"].copy(), "original_input_hashes": originals,
                       "harness_sha256": sha(b"synthetic wrapper"), "plan_sha256": sha(b"synthetic plan"),
                       "dependency_map_sha256": sha(b"synthetic dependency map"),
                       "python": m["runtime"]["python"], "threads": threads}
        result = {"stage": "completed", "kind": "SOAP-v3-corrected-scientific-candidate; not original or historical outcomes",
                  "item": item, "preserved_completed_pieces": None,
                  "producer_sha256": n["_OWN_SOURCES"]["videos/ai/ai11/compute.py"],
                  "source_hashes": {p: m["generation_source_hashes"][p] for p in n["_RECEIPT_SOURCES"]},
                  "source_baseline": n["_BASELINE"], "seed_policy": "unchanged deterministic source constants; see original compute.py",
                  "parent_clearance": "synthetic fixture authorization; no scientific run",
                  "correction_patch_sha256": n["_PATCH"], "elapsed_seconds": 1., "peak_rss_kib": 1,
                  "runtime": {k: v for k, v in m["runtime"]["packages"].items() if k != "torch"},
                  "threads": threads, "files": [{"path": f".cache/ai11/{item}.{ext}",
                      **{k: m["products"][item]["files"][ext][k] for k in ("bytes", "sha256")}} for ext in ("json", "npz")],
                  "upstream_cache_reads": [], "original_input_hashes": originals,
                  "harness_sha256": reservation["harness_sha256"], "torch": m["runtime"]["packages"]["torch"],
                  "network_access": "blocked within process", "free_disk_bytes": 1, "reservation_fingerprints": reservation}
        if item != "race":
            for target in (result, reservation):
                target["candidate_dependency_hashes"] = {f".cache/ai11/race.{ext}": m["products"]["race"]["files"][ext]["sha256"]
                                                        for ext in ("json", "npz")}
                target["race_receipt_sha256"] = m["products"]["race"]["receipt"]["sha256"]
            result["upstream_cache_reads"] = [".cache/ai11/race.json", ".cache/ai11/race.npz"]
        return result

    def set_receipt(self, item, receipt):
        self.manifest["products"][item]["receipt"] = self.artifact(
            self.ns["_CAPSULE"] + "receipts/" + item + ".json", json.dumps(receipt).encode())

    def seal(self):
        blob = json.dumps(self.manifest, sort_keys=True).encode()
        self.write(self.ns["_MANIFEST_PATH"], blob)
        # Only the synthetic test execution receives a substituted fixture anchor.
        self.ns["_MANIFEST_SHA256"] = sha(blob)
        self.ns["_MANIFEST_BYTES"] = len(blob)

    def read(self, item="ns"):
        return self.ns["load_corrected"](item)

    def saved_receipt(self, item):
        return json.loads((self.root / self.manifest["products"][item]["receipt"]["path"]).read_bytes())


class FrozenContract(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.fixture = SyntheticCapsule(self.root)

    def fails(self, pattern=None):
        return self.assertRaisesRegex(self.fixture.ns["ContractError"], pattern or ".")

    def test_synthetic_roundtrips_all_three_preserve_values_no_writes(self):
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob("*") if p.is_file()}
        for item in ("race", "ns", "schedule"):
            result = self.fixture.read(item)
            self.assertEqual(set(result), {"fixture", "fixture_array"})
            self.assertEqual(result["fixture"], "synthetic only")
            np.testing.assert_array_equal(result["fixture_array"], [[1., np.nan], [3., 4.]])
        self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob("*") if p.is_file()})

    def test_production_anchor_signature_no_override_and_missing_manifest(self):
        empty = self.root / "absent"
        empty.mkdir()
        ns = actual_reader(empty)
        self.assertEqual(ns["_MANIFEST_BYTES"], 19550)
        self.assertEqual(ns["_MANIFEST_SHA256"], "ccc740688b8b295fab7685206df2aea745aa7cf5598888b4ef0dc9d420be7eba")
        with self.assertRaises(ns["ContractError"]):
            ns["load_corrected"]("race")
        self.assertEqual(list(empty.iterdir()), [])
        anchored = actual_reader(self.root)
        with self.assertRaises(anchored["ContractError"]):
            anchored["load_corrected"]("race")  # fixture is not the production capsule
        tree = ast.parse(SOURCE.read_text())
        load = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "load_corrected")
        self.assertEqual([arg.arg for arg in load.args.args], ["name"])
        self.assertIsNone(load.args.kwarg)
        self.assertEqual(load.args.kwonlyargs, [])
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                modules = [node.module or ""] if isinstance(node, ast.ImportFrom) else [a.name for a in node.names]
                self.assertFalse(any("compute" in x or "charopt" in x or "torch" in x or "cache" in x for x in modules))
            if isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, {"environ", "getenv", "write_text", "write_bytes", "mkdir", "unlink"})

    def test_bad_names_fail_before_any_io(self):
        with mock.patch.object(Path, "resolve", side_effect=AssertionError("unexpected IO")):
            for value in ("", "quad", "../race", "race.json", None, ["race"]):
                with self.subTest(value=value), self.fails("Unknown"):
                    self.fixture.read(value)

    def test_anchor_and_duplicate_or_malformed_json_fail_before_decode(self):
        f = self.fixture
        for blob in (b"{}", b"{", b'{"schema":1,"schema":2}'):
            with self.subTest(blob=blob):
                f.write(f.ns["_MANIFEST_PATH"], blob)
                f.ns["_MANIFEST_SHA256"] = sha(blob)
                f.ns["_MANIFEST_BYTES"] = len(blob)
                with self.fails(), mock.patch.object(np, "load", side_effect=AssertionError("decoded before validation")):
                    f.read()

    def test_descriptor_size_and_format_mismatch_rejected_before_open(self):
        f = self.fixture
        path = sorted(f.ns["_INPUT_PATHS"])[0]
        identity = f.manifest["original_inputs"][path]
        for expected in ({**identity, "bytes": identity["bytes"] + 1},
                         {**identity, "bytes": -1}, {**identity, "bytes": True},
                         {**identity, "sha256": "malformed"}, {"bytes": identity["bytes"]}):
            with self.subTest(expected=expected), self.fails(), mock.patch.object(
                    Path, "open", side_effect=AssertionError("mismatch must not open/read")):
                f.ns["_read"](path, expected=expected, retain=True)
        descriptor = f.manifest["products"]["ns"]["files"]["json"]
        f.write(descriptor["path"], b"x" * (descriptor["bytes"] + 1))
        with self.fails("size mismatch"), mock.patch.object(
                Path, "open", side_effect=AssertionError("oversize artifact must not open/read")):
            f.ns["_artifact"](descriptor, descriptor["path"], retain=True)

    def test_production_manifest_oversize_rejected_before_open(self):
        f = self.fixture
        f.write(f.ns["_MANIFEST_PATH"], b"x" * 19551)
        actual = actual_reader(self.root)
        with self.assertRaisesRegex(actual["ContractError"], "size mismatch"), mock.patch.object(
                Path, "open", side_effect=AssertionError("oversize manifest must not open/read")):
            actual["load_corrected"]("ns")

    def test_retained_read_rejects_growth_before_appending_beyond_declared_bytes(self):
        f = self.fixture
        path = sorted(f.ns["_INPUT_PATHS"])[0]
        identity = f.manifest["original_inputs"][path]
        original = (self.root / path).read_bytes()
        observed = []
        with (self.root / path).open("rb") as real:
            class GrowingStream(io.BytesIO):
                def fileno(self):
                    return real.fileno()

                def read(self, size=-1):
                    chunk = super().read(size)
                    observed.append((size, len(chunk)))
                    return chunk
            oversized = GrowingStream(original + b"extra bytes are never retained")
            with mock.patch.object(Path, "open", return_value=oversized), self.fails("grew while read"):
                f.ns["_read"](path, expected=identity, retain=True)
            self.assertEqual(observed, [(len(original) + 1, len(original) + 1)])

    def test_actual_source_inputs_epoch_and_other_product_tamper_all_block_decode(self):
        f = self.fixture
        paths = ["videos/ai/ai11/charopt.py", "explainer/ai/cache.py", sorted(f.ns["_INPUT_PATHS"])[0],
                 next(iter(f.manifest["epoch_sources"].values()))["path"],
                 f.manifest["products"]["schedule"]["files"]["npz"]["path"],
                 f.manifest["products"]["race"]["receipt"]["path"],
                 f.manifest["products"]["race"]["review"]["path"],
                 f.manifest["source_reviews"]["TORCH-SYNTHETIC-REVIEW.md"]["path"]]
        for path in paths:
            saved = (self.root / path).read_bytes()
            f.write(path, saved + b"tamper")
            with self.subTest(path=path), self.fails(), mock.patch.object(np, "load", side_effect=AssertionError("decode")):
                f.read("ns")
            f.write(path, saved, readonly=path not in f.ns["_SOURCE_PATHS"])

    def test_manifest_schema_scope_exclusion_sets_and_own_recipe_cannot_be_weakened(self):
        f = self.fixture
        mutations = [lambda m: m.update(schema="other"), lambda m: m.update(generation_baseline="0" * 40),
                     lambda m: m.update(correction_patch_sha256="0" * 64), lambda m: m.update(extra=True),
                     lambda m: m.update(limits=[]), lambda m: m.update(presentation_only_current_exclusion=[]),
                     lambda m: m["current_source_hashes"].pop("explainer/ai/cache.py"),
                     lambda m: m["generation_source_hashes"].update({"videos/ai/ai11/charopt.py": "0" * 64})]
        original = json.dumps(f.manifest)
        for mutate in mutations:
            f.manifest = json.loads(original)
            mutate(f.manifest)
            f.seal()
            with self.subTest(mutate=mutate), self.fails():
                f.read()

    def test_only_current_presentation_table_can_differ_from_epoch(self):
        f = self.fixture
        f.write(f.ns["_CAPTION_PATH"], b"synthetic new presentation table", readonly=False)
        self.assertEqual(f.read()["fixture"], "synthetic only")
        f.write(f.manifest["epoch_sources"][f.ns["_CAPTION_PATH"]]["path"], b"changed epoch")
        with self.fails():
            f.read()

    def test_paths_namespace_symlinks_writable_and_missing_artifacts_rejected(self):
        f = self.fixture
        original = json.dumps(f.manifest)
        for path in ("/tmp/escape", "../escape", ".cache/ai11/race.json", f.ns["_PRODUCTS"] + "../race.json"):
            f.manifest = json.loads(original)
            f.manifest["products"]["race"]["files"]["json"]["path"] = path
            f.seal()
            with self.subTest(path=path), self.fails("path"):
                f.read()
        f.manifest = json.loads(original)
        f.seal()
        path = self.root / sorted(f.ns["_INPUT_PATHS"])[0]
        saved = path.read_bytes()
        path.chmod(0o644)
        with self.fails("read-only"):
            f.read()
        path.unlink()
        with self.fails():
            f.read()
        target = self.root / "synthetic-target"
        target.write_bytes(saved)
        target.chmod(0o444)
        path.symlink_to(target)
        with self.fails("Symlink"):
            f.read()

    def test_completion_and_reservation_tamper_fail_even_with_test_reanchoring(self):
        f = self.fixture
        original = f.saved_receipt("ns")
        mutations = [lambda r: r.update(stage="reserved"), lambda r: r.update(item="race"),
                     lambda r: r.update(producer_sha256="0" * 64), lambda r: r.update(correction_patch_sha256="0" * 64),
                     lambda r: r["source_hashes"].pop("videos/ai/ai11/charopt.py"),
                     lambda r: r["reservation_fingerprints"]["source_hashes"].pop(f.ns["_CAPTION_PATH"]),
                     lambda r: r["original_input_hashes"].update({next(iter(r["original_input_hashes"])): "0" * 64}),
                     lambda r: r["candidate_dependency_hashes"].update({".cache/ai11/race.json": "0" * 64}),
                     lambda r: r.update(race_receipt_sha256="0" * 64), lambda r: r.update(upstream_cache_reads=[]),
                     lambda r: r["files"][0].update(path=".cache/ai11/ns-other.json"),
                     lambda r: r["reservation_fingerprints"].update(harness_sha256="0" * 64),
                     lambda r: r["runtime"].update(numpy="changed"), lambda r: r["threads"].update(AI11_WORKERS="2"),
                     lambda r: r.update(elapsed_seconds=float("nan"))]
        for mutate in mutations:
            receipt = json.loads(json.dumps(original))
            mutate(receipt)
            f.set_receipt("ns", receipt)
            f.seal()
            with self.subTest(mutate=mutate), self.fails():
                f.read()

    def test_lifecycle_mutation_during_streaming_read_rejected(self):
        f = self.fixture
        real_fstat = f.ns["os"].fstat
        calls = 0
        def changed_fstat(fd):
            nonlocal calls
            calls += 1
            info = real_fstat(fd)
            if calls == 2:
                values = list(info)
                values[6] += 1
                return type(info)(values)
            return info
        with mock.patch.object(f.ns["os"], "fstat", side_effect=changed_fstat), self.fails("changed"):
            f.read()

    def test_decode_uses_only_hashed_bytes_and_pickle_disabled(self):
        f = self.fixture
        real_decode = f.ns["_decode"]
        real_load = np.load
        expected = (self.root / f.manifest["products"]["ns"]["files"]["npz"]["path"]).read_bytes()
        def at_decode(metadata, archive):
            f.write(f.manifest["products"]["ns"]["files"]["npz"]["path"], b"later path contents")
            self.assertEqual(archive, expected)
            return real_decode(metadata, archive)
        def load_spy(file, **kwargs):
            self.assertIsInstance(file, io.BytesIO)
            self.assertIs(kwargs["allow_pickle"], False)
            return real_load(file, **kwargs)
        f.ns["_decode"] = at_decode
        with mock.patch.object(np, "load", side_effect=load_spy):
            self.assertEqual(f.read()["fixture"], "synthetic only")
        with self.fails():
            f.read()  # no cached acceptance on the next call

    def test_decoder_rejects_bad_metadata_npz_overlap_duplicate_and_object_arrays(self):
        decode, error = self.fixture.ns["_decode"], self.fixture.ns["ContractError"]
        buffer = io.BytesIO()
        np.savez(buffer, array=np.array([1, 2]))
        valid = buffer.getvalue()
        for blob in (b"{}", b"[]", b"null", b'{"x":1,"x":2}'):
            with self.subTest(blob=blob), self.assertRaises((error, ValueError)):
                decode(blob, valid)
        with self.assertRaises(error):
            decode(b'{"array": 1}', valid)
        with self.assertRaises((error, ValueError)):
            decode(b'{"fixture": 1}', b"malformed synthetic archive")
        for values in ({}, {"array": np.array([{"untrusted": True}], dtype=object)}):
            buffer = io.BytesIO()
            np.savez(buffer, **values)
            with self.assertRaises((error, ValueError)):
                decode(b'{"fixture": 1}', buffer.getvalue())
        payload = io.BytesIO()
        np.save(payload, np.array([1, 2]))
        buffer = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(buffer, "w") as archive:
                archive.writestr("array.npy", payload.getvalue())
                archive.writestr("array.npy", payload.getvalue())
        with self.assertRaises(error):
            decode(b'{"fixture": 1}', buffer.getvalue())
        with self.assertRaises(error):
            decode(b'{"fixture": 1}', payload.getvalue())


if __name__ == "__main__":
    unittest.main()
