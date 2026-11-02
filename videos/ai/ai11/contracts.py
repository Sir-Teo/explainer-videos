"""Read-only admission of the separately reviewed, frozen SOAP-V3 outcomes.

This fixed contract permits retained outcome consumption, not reproduction from
current captions, official SOAP equivalence, causal gains, or render acceptance.
Missing or changed evidence fails closed; this module never prepares products.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import os
from pathlib import PurePosixPath
import stat

import numpy as np

from explainer.paths import ROOT as _REPO_ROOT

_MANIFEST_PATH = ".cache/ai11/contracts/soap-v3-v1/manifest.json"
_MANIFEST_BYTES = 19550
_MANIFEST_SHA256 = "ccc740688b8b295fab7685206df2aea745aa7cf5598888b4ef0dc9d420be7eba"
_SCHEMA = "ai11-frozen-soap-v3-consumer-v1"
_BASELINE = "3cfc87e211ba1b56d133f9b8e57a8f739b4e10bb"
_PATCH = "90d0011d236985aa70b488d0b7ea43f8b1200d7bfb319edb89399bc0b26809c5"
_CAPTION_PATH = "videos/ai/ai_text_zh.json"
_ITEMS = frozenset({"race", "ns", "schedule"})
_CAPSULE = ".cache/ai11/contracts/soap-v3-v1/"
_PRODUCTS = ".cache/ai11/corrected-soap-v3-v1/"
_SOURCE_PATHS = frozenset(['CLAUDE.md', 'explainer/ai/__init__.py', 'explainer/ai/autodiff.py', 'explainer/ai/cache.py', 'explainer/ai/games.py', 'explainer/ai/lecture.py', 'explainer/ai/novels.py', 'explainer/ai/viz.py', 'explainer/analysis/__init__.py', 'explainer/cache_lock.py', 'explainer/lang.py', 'explainer/lm/pocket.py', 'explainer/tts.py', 'explainer/voiceover.py', 'explainer/zh_templates.py', 'explainer/zh_text.py', 'manim.cfg', 'pyproject.toml', 'requirements-lock.txt', 'tools/build.py', 'tools/collect_text.py', 'tools/make.py', 'tools/qa_series.py', 'videos/ai/ai1/compute.py', 'videos/ai/ai11/charopt.py', 'videos/ai/ai11/compute.py', 'videos/ai/ai11/nets.py', 'videos/ai/ai6/cache_contract.py', 'videos/ai/ai6/compute.py', 'videos/ai/ai6/contracts.py', 'videos/ai/ai9/compute.py', 'videos/ai/ai_text_zh.json'])
_INPUT_PATHS = frozenset(['.cache/ai1/books/1342.txt', '.cache/ai1/books/1400.txt', '.cache/ai1/books/158.txt', '.cache/ai1/books/46.txt', '.cache/ai1/books/98.txt', '.cache/ai1/passage.txt', '.cache/ai1/raw.json', '.cache/ai1/scoreboard.json', '.cache/ai1/train.txt', '.cache/ai1/valid.txt', '.cache/ai6/pages.json', '.cache/ai6/pages.npz'])
_OWN_SOURCES = {'videos/ai/ai11/charopt.py': '263864b969cd1a2ff73f1df5c4e71ed98a2bf4d1f1d80d59e16f6e5fb304bc05', 'videos/ai/ai11/compute.py': 'a28bb32905c2918e122c71db241b8c526cc73890b994ebd08a801a88133b84bb', 'videos/ai/ai11/nets.py': '42c2d263d31e7fef1609c0f049e5d64fe69df91081b9524efc0ad7890f84d878'}
_RECEIPT_SOURCES = frozenset(['explainer/ai/cache.py', 'explainer/cache_lock.py', 'videos/ai/ai1/compute.py', 'videos/ai/ai11/charopt.py', 'videos/ai/ai11/compute.py', 'videos/ai/ai11/nets.py', 'videos/ai/ai6/cache_contract.py', 'videos/ai/ai6/compute.py', 'videos/ai/ai6/contracts.py', 'videos/ai/ai9/compute.py'])
_LIMITS = ['Frozen outcome consumption, not current-caption-source reproduction', 'No full official SOAP-reference equivalence or causal correction performance claim', 'NS current-top-n metrics are not persistent modes or full-spectrum convergence', 'Actual listening, continuous playback and production acceptance are outside this contract']
_KIND = 'Previously prepared, separately reviewed SOAP-V3 candidate outcomes; no new generation'


class ContractError(RuntimeError):
    """The fixed frozen-outcome contract could not be established."""


def _require(condition, message):
    if not condition:
        raise ContractError(message)


def _keys(value, expected, label):
    _require(isinstance(value, dict) and set(value) == set(expected),
             f"Invalid {label} fields")


def _sha(value):
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def _json(blob):
    return json.loads(blob, object_pairs_hook=_unique_object)


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _read(relative, *, expected=None, retain=False, readonly=True):
    """Hash one regular, root-contained, read-only file, checking its lifecycle.

    Inputs/sources stream through the hash. Only evidence and requested product
    bytes are retained within the prechecked declared length; decoded data can
    never come from a later path re-read.
    """
    if expected is not None:
        _keys(expected, {"bytes", "sha256"}, "file identity")
        _require(type(expected["bytes"]) is int and expected["bytes"] >= 0
                 and _sha(expected["sha256"]), "Invalid file identity")
    _require(not retain or expected is not None, "Retained reads require an exact declared identity")
    _require(isinstance(relative, str) and relative == str(PurePosixPath(relative))
             and not PurePosixPath(relative).is_absolute()
             and ".." not in PurePosixPath(relative).parts, "Invalid contract path")
    root = _REPO_ROOT.resolve(strict=True)
    path = root / relative
    cursor = root
    for part in PurePosixPath(relative).parts:
        cursor = cursor / part
        _require(not cursor.is_symlink(), f"Symlink is not admitted: {relative}")
    _require(path.resolve(strict=True).is_relative_to(root), "Contract path escapes root")
    before = path.stat()
    _require(stat.S_ISREG(before.st_mode) and (not readonly or not before.st_mode & 0o222),
             f"Contract artifact must be a read-only regular file: {relative}")
    if expected is not None:
        _require(before.st_size == expected["bytes"],
                 f"Contract artifact size mismatch: {relative}")
    limit = before.st_size
    digest = hashlib.sha256()
    received = 0
    chunks = [] if retain else None
    with path.open("rb") as stream:
        _require(_identity(before) == _identity(os.fstat(stream.fileno())),
                 f"Contract artifact changed before read: {relative}")
        for chunk in iter(lambda: stream.read(min(1024 * 1024, limit - received + 1)), b""):
            received += len(chunk)
            _require(received <= limit, f"Contract artifact grew while read: {relative}")
            digest.update(chunk)
            if retain:
                chunks.append(chunk)
        after = os.fstat(stream.fileno())
    _require(_identity(before) == _identity(after) == _identity(path.stat()),
             f"Contract artifact changed while read: {relative}")
    _require(not path.is_symlink() and path.resolve(strict=True) == root / relative,
             f"Contract artifact path changed: {relative}")
    if expected is not None:
        _require(received == expected["bytes"] and digest.hexdigest() == expected["sha256"],
                 f"Contract artifact identity mismatch: {relative}")
    return (b"".join(chunks) if retain else None), digest.hexdigest()


def _artifact(descriptor, path, *, retain=False):
    _keys(descriptor, {"path", "bytes", "sha256"}, "artifact")
    _require(descriptor["path"] == path, "Unexpected contract artifact path")
    return _read(path, expected={k: descriptor[k] for k in ("bytes", "sha256")}, retain=retain)[0]


def _receipt(receipt, item, manifest):
    dependent = item != "race"
    fields = {"stage", "kind", "item", "preserved_completed_pieces", "producer_sha256",
              "source_hashes", "source_baseline", "seed_policy", "parent_clearance",
              "correction_patch_sha256", "elapsed_seconds", "peak_rss_kib", "runtime", "threads",
              "files", "upstream_cache_reads", "original_input_hashes", "harness_sha256",
              "torch", "network_access", "free_disk_bytes", "reservation_fingerprints"}
    dependency_fields = {"candidate_dependency_hashes", "race_receipt_sha256"} if dependent else set()
    _keys(receipt, fields | dependency_fields, "completion receipt")
    _require(receipt["stage"] == "completed" and receipt["item"] == item
             and receipt["kind"] == "SOAP-v3-corrected-scientific-candidate; not original or historical outcomes"
             and receipt["source_baseline"] == _BASELINE
             and receipt["correction_patch_sha256"] == _PATCH
             and receipt["producer_sha256"] == _OWN_SOURCES["videos/ai/ai11/compute.py"],
             "Receipt does not describe the completed corrected recipe")
    generated = manifest["generation_source_hashes"]
    _require(receipt["source_hashes"] == {p: generated[p] for p in _RECEIPT_SOURCES},
             "Completion source pins differ from frozen epoch")
    originals = {p: d["sha256"] for p, d in manifest["original_inputs"].items()}
    _require(receipt["original_input_hashes"] == originals, "Completion input pins differ")
    reservation = receipt["reservation_fingerprints"]
    _keys(reservation, {"source_hashes", "original_input_hashes", "harness_sha256", "plan_sha256",
                        "dependency_map_sha256", "python", "threads"} | dependency_fields,
          "reservation")
    _require(reservation["source_hashes"] == generated and reservation["original_input_hashes"] == originals,
             "Reservation source/input pins differ")
    threads = {p: "1" for p in ("AI11_THREADS", "AI11_WORKERS", "OMP_NUM_THREADS",
                                "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")}
    runtime = manifest["runtime"]
    _require(receipt["threads"] == reservation["threads"] == threads
             and reservation["python"] == runtime["python"]
             and receipt["runtime"] == {k: v for k, v in runtime["packages"].items() if k != "torch"}
             and receipt["torch"] == runtime["packages"]["torch"], "Recorded generation runtime differs")
    _require(_sha(receipt["harness_sha256"])
             and receipt["harness_sha256"] == reservation["harness_sha256"]
             and _sha(reservation["plan_sha256"]) and _sha(reservation["dependency_map_sha256"]),
             "Reservation recipe fingerprints differ")
    _require(receipt["network_access"] == "blocked within process"
             and receipt["seed_policy"] == "unchanged deterministic source constants; see original compute.py"
             and isinstance(receipt["parent_clearance"], str) and bool(receipt["parent_clearance"]),
             "Invalid generation lifecycle record")
    for key in ("elapsed_seconds", "peak_rss_kib", "free_disk_bytes"):
        _require(type(receipt[key]) in (int, float) and math.isfinite(receipt[key]) and receipt[key] >= 0,
                 "Invalid generation completion measurement")
    files = [{"path": f".cache/ai11/{item}.{ext}",
              **{k: manifest["products"][item]["files"][ext][k] for k in ("bytes", "sha256")}}
             for ext in ("json", "npz")]
    _require(receipt["files"] == files, "Completion outputs differ from frozen products")
    expected_reads = [".cache/ai11/race.json", ".cache/ai11/race.npz"] if dependent else []
    _require(receipt["upstream_cache_reads"] == expected_reads, "Unexpected generation dependencies")
    if dependent:
        dependencies = {f".cache/ai11/race.{ext}": manifest["products"]["race"]["files"][ext]["sha256"]
                        for ext in ("json", "npz")}
        race_receipt = manifest["products"]["race"]["receipt"]["sha256"]
        _require(receipt["candidate_dependency_hashes"] == reservation["candidate_dependency_hashes"] == dependencies
                 and receipt["race_receipt_sha256"] == reservation["race_receipt_sha256"] == race_receipt,
                 "Dependent product does not bind the frozen race")
    pieces = receipt["preserved_completed_pieces"]
    if pieces is not None:
        _keys(pieces, {"path", "bytes", "sha256", "meaning"}, "historical partial record")
        _require(isinstance(pieces["path"], str) and type(pieces["bytes"]) is int and pieces["bytes"] > 0
                 and _sha(pieces["sha256"]) and isinstance(pieces["meaning"], str),
                 "Invalid historical partial record")
        # This is a hashed historical record, not a current filesystem dependency.


def _decode(metadata, archive):
    data = _json(metadata)
    _require(isinstance(data, dict) and bool(data), "Frozen metadata must be a nonempty JSON object")
    arrays = np.load(io.BytesIO(archive), allow_pickle=False)
    _require(isinstance(arrays, np.lib.npyio.NpzFile), "Frozen arrays must be an NPZ archive")
    with arrays:
        keys = arrays.files
        _require(bool(keys) and len(keys) == len(set(keys)), "Frozen NPZ keys must be nonempty and unique")
        _require(not set(data).intersection(keys), "Frozen JSON and NPZ keys must not overlap")
        data.update({key: arrays[key] for key in keys})
    return data


def load_corrected(name: str) -> dict:
    """Validate the entire anchored capsule, then read one retained outcome pair.

    The recorded runtime is generation history. Admission does not assert current
    runtime equivalence, new training, official SOAP equivalence, or rendering QA.
    """
    if not isinstance(name, str) or name not in _ITEMS:
        raise ContractError("Unknown corrected Part 11 product")
    try:
        blob, digest = _read(_MANIFEST_PATH,
                             expected={"bytes": _MANIFEST_BYTES, "sha256": _MANIFEST_SHA256}, retain=True)
        _require(digest == _MANIFEST_SHA256, "Frozen manifest anchor mismatch")
        manifest = _json(blob)
        _keys(manifest, {"schema", "generation_baseline", "kind", "correction_patch_sha256",
                         "generation_source_hashes", "current_source_hashes", "presentation_only_current_exclusion",
                         "epoch_sources", "original_inputs", "products", "source_reviews", "runtime", "limits"},
              "manifest")
        _require(manifest["schema"] == _SCHEMA and manifest["generation_baseline"] == _BASELINE
                 and manifest["correction_patch_sha256"] == _PATCH and manifest["kind"] == _KIND
                 and manifest["limits"] == _LIMITS, "Unsupported frozen contract scope")
        generation = manifest["generation_source_hashes"]
        current = manifest["current_source_hashes"]
        _keys(generation, _SOURCE_PATHS, "generation source pins")
        _keys(current, _SOURCE_PATHS - {_CAPTION_PATH}, "current source pins")
        _require(all(_sha(value) for value in generation.values())
                 and current == {p: h for p, h in generation.items() if p != _CAPTION_PATH}
                 and manifest["presentation_only_current_exclusion"] == [_CAPTION_PATH]
                 and all(current[p] == h for p, h in _OWN_SOURCES.items()),
                 "Invalid current generation source boundary")
        _keys(manifest["epoch_sources"], _SOURCE_PATHS, "epoch sources")
        for path, digest in current.items():
            _read(path, expected={"bytes": manifest["epoch_sources"][path]["bytes"], "sha256": digest},
                  readonly=False)
        for path, descriptor in manifest["epoch_sources"].items():
            _require(descriptor["sha256"] == generation[path], "Epoch source identity differs")
            _artifact(descriptor, _CAPSULE + "recipe-sources/" + path)
        _keys(manifest["original_inputs"], _INPUT_PATHS, "original inputs")
        for path, identity in manifest["original_inputs"].items():
            _read(path, expected=identity)
        _keys(manifest["runtime"], {"python", "packages"}, "generation runtime")
        _keys(manifest["runtime"]["packages"], {"manim", "numpy", "pillow", "scipy", "torch"}, "generation packages")
        _require(isinstance(manifest["runtime"]["python"], str)
                 and all(isinstance(v, str) and v for v in manifest["runtime"]["packages"].values()),
                 "Invalid recorded generation runtime")
        _keys(manifest["products"], _ITEMS, "frozen products")
        requested = {}
        receipts = {}
        for item in sorted(_ITEMS):
            product = manifest["products"][item]
            _keys(product, {"dependencies", "files", "receipt", "review"}, "product")
            _require(product["dependencies"] == ([] if item == "race" else ["race"]), "Invalid product dependencies")
            _keys(product["files"], {"json", "npz"}, "product files")
            for ext, descriptor in product["files"].items():
                value = _artifact(descriptor, f"{_PRODUCTS}{item}.{ext}", retain=item == name)
                if item == name:
                    requested[ext] = value
            receipts[item] = _json(_artifact(product["receipt"], f"{_CAPSULE}receipts/{item}.json", retain=True))
            _artifact(product["review"], f"{_CAPSULE}reviews/{item}.md")
        _keys(manifest["source_reviews"], {"INDEPENDENT-REVIEW.md", "TORCH-SYNTHETIC-REVIEW.md"}, "source reviews")
        for filename, descriptor in manifest["source_reviews"].items():
            _artifact(descriptor, _CAPSULE + "reviews/" + filename)
        for item, receipt in receipts.items():
            _receipt(receipt, item, manifest)
        return _decode(requested["json"], requested["npz"])
    except ContractError:
        raise
    except (OSError, ValueError, TypeError, KeyError, EOFError) as error:
        raise ContractError(f"Frozen Part 11 contract unavailable or invalid: {error}") from error
