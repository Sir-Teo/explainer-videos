"""Read operator-reviewed Part 16 inputs without importing scientific producers.

The operator supplies ``.cache/ai16/render-manifest.json``. Its schema is::

    {"schema_version": 1, "part": "ai16",
     "compatibility_sources": {"videos/ai/ai16/compute.py": "<SHA256>", ...},
     "products": {"<allowed name>": {
         "json": {"bytes": 123, "sha256": "<SHA256>"},
         "npz": null,
         "review": {"accepted": true, "recipe": "original-recipe",
                    "producer_sha256": "<SHA256>",
                    "input_sha256": {"<input label>": "<SHA256>"}}}}}

An NPZ descriptor additionally declares ``arrays: {key: {dtype, shape}}``.
Approval is the operator's assertion about the identified bytes, not proof of
scientific reproducibility. No manifest, data, model or computation is supplied
by this module. All failures stop the read; there is no generation or fallback.
"""

from __future__ import annotations

import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
_MANIFEST = ".cache/ai16/render-manifest.json"
_MAX_BYTES = 256 * 1024 * 1024
_SOURCES = frozenset(f"videos/ai/ai16/{name}.py" for name in
                     ("compute", "runs", "nets", "recall", "prune", "lottery", "facts"))
_PRODUCTS = frozenset(("accounting", "actsparse", "balance", "capacity", "configs", "fine", "gradcheck",
                       "lottery", "mix1991", "mod", "moe", "parallel", "prune24", "recall", "row",
                       "scoreboard", "special_within_window_v2", "speed", "topk", "upcycle"))
_SPECIAL = "special_within_window_v2"
_CLASSES = ["vowels", "consonants", "capitals", "spaces", "punctuation"]


class ReviewedInputError(RuntimeError):
    """Missing, incompatible or unapproved input; no computation was attempted."""


def _require(condition, message):
    # These checks must remain active under python -O.
    if not condition:
        raise ReviewedInputError(message)


def _read(relative, limit=_MAX_BYTES):
    """Read one regular file through directory descriptors, without following links."""
    path = PurePosixPath(relative)
    _require(not path.is_absolute() and path.parts and all(p not in (".", "..") for p in path.parts),
             "Invalid reviewed-input path")
    _require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY"),
             "Reviewed inputs require no-symlink directory reads on this platform")
    directory = None
    descriptor = None
    try:
        directory = os.open(_ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        for part in path.parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        before = os.fstat(descriptor)
        _require(stat.S_ISREG(before.st_mode), f"Input is not a regular file: {relative}")
        _require(before.st_size <= limit, f"Reviewed input exceeds its size bound: {relative}")
        chunks, size = [], 0
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, limit + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            _require(size <= limit, f"Reviewed input grew beyond its size bound: {relative}")
        after = os.fstat(descriptor)
        signature = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        _require(signature(before) == signature(after) and size == before.st_size,
                 f"Reviewed input changed during its read: {relative}")
        return b"".join(chunks)
    except OSError as error:
        raise ReviewedInputError(f"Cannot read reviewed input: {relative}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if directory is not None:
            os.close(directory)


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        _require(key not in out, f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def _finite_json(value):
    if isinstance(value, float):
        _require(math.isfinite(value), "Nonfinite JSON number")
    elif isinstance(value, dict):
        for child in value.values():
            _finite_json(child)
    elif isinstance(value, list):
        for child in value:
            _finite_json(child)


def _json(data):
    try:
        out = json.loads(data, object_pairs_hook=_pairs,
                         parse_constant=lambda _: (_require(False, "Nonfinite JSON constant")))
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ReviewedInputError("Invalid reviewed JSON") from error
    _require(isinstance(out, dict), "Reviewed JSON must contain an object")
    try:
        _finite_json(out)
    except RecursionError as error:
        raise ReviewedInputError("Reviewed JSON nesting is too deep") from error
    return out


def _digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _verified(relative, identity):
    _require(isinstance(identity, dict) and _digest(identity.get("sha256")), "Missing file digest")
    size = identity.get("bytes")
    _require(type(size) is int and 0 < size <= _MAX_BYTES, "Invalid reviewed file size")
    data = _read(relative, size)
    _require(len(data) == size and hashlib.sha256(data).hexdigest() == identity["sha256"],
             f"Reviewed file identity mismatch: {relative}")
    return data


def _manifest():
    data = _json(_read(_MANIFEST, 1024 * 1024))
    _require(type(data.get("schema_version")) is int and data["schema_version"] == 1 and data.get("part") == "ai16",
             "Unsupported Part 16 render-manifest schema")
    sources = data.get("compatibility_sources")
    _require(isinstance(sources, dict) and sources.keys() == _SOURCES,
             "Manifest must pin every required Part 16 scientific source")
    for relative, digest in sources.items():
        _require(_digest(digest) and hashlib.sha256(_read(relative)).hexdigest() == digest,
                 f"Incompatible scientific source: {relative}")
    products = data.get("products")
    _require(isinstance(products, dict) and products.keys() <= _PRODUCTS,
             "Manifest contains an unsupported product")
    return products


def _absent(relative):
    try:
        os.lstat(_ROOT / relative)
    except FileNotFoundError:
        return
    except OSError as error:
        raise ReviewedInputError(f"Cannot establish absent sibling: {relative}") from error
    raise ReviewedInputError(f"Unexpected reviewed-input sibling: {relative}")


def _arrays(data, declared):
    _require(isinstance(declared, dict), "NPZ array declarations are required")
    try:
        with np.load(io.BytesIO(data), allow_pickle=False) as archive:
            _require(len(archive.files) == len(set(archive.files)) and set(archive.files) == declared.keys(),
                     "NPZ array inventory mismatch")
            out = {}
            for name, spec in declared.items():
                _require(isinstance(spec, dict) and isinstance(spec.get("dtype"), str), "Invalid array dtype declaration")
                shape = spec.get("shape")
                _require(isinstance(shape, list) and all(type(x) is int and x >= 0 for x in shape),
                         "Invalid array shape declaration")
                dtype = np.dtype(spec["dtype"])
                _require(not dtype.hasobject, "Object arrays are forbidden")
                array = archive[name]
                _require(array.dtype == dtype and list(array.shape) == shape and not array.dtype.hasobject,
                         f"Array dtype/shape mismatch: {name}")
                if array.dtype.kind in "fc":
                    _require(bool(np.isfinite(array).all()), f"Nonfinite array: {name}")
                out[name] = array.copy()
            return out
    except ReviewedInputError:
        raise
    except (ValueError, TypeError, OverflowError, OSError, EOFError, KeyError, zipfile.BadZipFile) as error:
        raise ReviewedInputError("Invalid reviewed NPZ") from error


def _number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def _count(value):
    return type(value) is int and value >= 0


def _rows(row, probabilities, counts, tokens, slots, length, experts, choices):
    ps, cs, ts, ss = (row.get(k) for k in (probabilities, counts, tokens, slots))
    _require(all(isinstance(x, list) and len(x) == length for x in (ps, cs, ts, ss)), "Special vector shape mismatch")
    for p, c, t, s in zip(ps, cs, ts, ss):
        _require(isinstance(p, list) and isinstance(c, list) and len(p) == len(c) == experts,
                 "Special matrix shape mismatch")
        _require(_count(t) and t <= row["token_count"] and _count(s) and s == t * choices
                 and all(_count(x) and x <= t for x in c) and sum(c) == s,
                 "Special population counts are inconsistent")
        _require(all(_number(x) and 0 <= x <= 1 for x in p), "Invalid Special probability")
        expected = [x / s if s else 0 for x in c]
        _require(all(abs(a - b) <= 1e-10 for a, b in zip(p, expected)), "Special probabilities disagree with counts")


def _special(data):
    _require(type(data.get("schema_version")) is int and data["schema_version"] == 2 and data.get("version") == _SPECIAL,
             "Corrected Special schema/version required")
    cohorts = {"moe": [0, 1, 2], "fine": [0, 1]}
    integer_list = lambda value: isinstance(value, list) and all(type(x) is int for x in value)
    _require(data.get("seeds") == [0, 1, 2] and data.get("modes") == ["moe", "fine"]
             and integer_list(data["seeds"]) and data.get("seeds_by_mode") == cohorts
             and all(integer_list(data["seeds_by_mode"][mode]) for mode in cohorts)
             and data.get("seed_counts") == {"moe": 3, "fine": 2},
             "Corrected Special seed cohorts required")
    sampling = data.get("sampling")
    _require(isinstance(sampling, dict) and sampling.get("window_count") == 256 and sampling.get("context") == 64
             and sampling.get("retained_positions") == list(range(1, 64)) and sampling.get("excluded_positions") == [0]
             and integer_list(sampling["retained_positions"]) and integer_list(sampling["excluded_positions"])
             and sampling.get("matched_tokens") == 16128 and sampling.get("original_tokens") == 16384,
             "Corrected Special within-window population required")
    chars = data.get("route_chars")
    _require(data.get("classes") == _CLASSES and isinstance(chars, list) and chars
             and all(isinstance(x, str) and len(x) == 1 for x in chars) and len(set(chars)) == len(chars),
             "Invalid Special category/character inventory")
    expected = {f"{mode}_s{seed}_l{layer}" for mode, seeds in cohorts.items() for seed in seeds for layer in range(2)}
    actual = {k for k in data if re.match(r"(?:moe|fine)_s", k)}
    _require(actual == expected, "Corrected Special requires exactly ten model/block rows")
    for mode, seeds in cohorts.items():
        experts, choices = (8, 2) if mode == "moe" else (32, 8)
        for seed in seeds:
            for layer in range(2):
                row = data[f"{mode}_s{seed}_l{layer}"]
                _require(isinstance(row, dict) and row.get("mode") == mode and type(row.get("seed")) is int
                         and row["seed"] == seed and type(row.get("layer")) is int and row["layer"] == layer,
                         "Special model/block identity mismatch")
                for name, value in (("E", experts), ("k", choices), ("token_count", 16128), ("slot_count", 16128 * choices)):
                    _require(type(row.get(name)) is int and row[name] == value, "Special token/slot/configuration mismatch")
                _require(row.get("model_key") == f"{mode}_s{seed}" and _digest(row.get("checkpoint_sha256")),
                         "Special checkpoint identity metadata required")
                _require(all(_number(row.get(k)) and row[k] >= 0 for k in ("cur", "nxt", "prv", "shuf", "H")),
                         "Invalid Special information values")
                _require(row["H"] <= math.log2(experts) + 1e-10
                         and all(row[k] <= row["H"] + 1e-10 for k in ("cur", "nxt", "prv", "shuf")),
                         "Special information exceeds its entropy bound")
                _rows(row, "classes", "class_counts", "class_token_counts", "class_slot_counts", 5, experts, choices)
                _rows(row, "table", "route_counts", "route_char_token_counts", "route_char_slot_counts",
                      len(chars), experts, choices)


def load(name):
    """Return fresh, verified inputs or raise; never compute, save, rename or fall back."""
    _require(isinstance(name, str) and name in _PRODUCTS, "Unsupported Part 16 scene product")
    products = _manifest()
    product = products.get(name)
    _require(isinstance(product, dict), f"No reviewed manifest entry for {name}")
    review = product.get("review")
    recipe = "within-window-v2" if name == _SPECIAL else "original-recipe"
    _require(isinstance(review, dict) and review.get("accepted") is True and review.get("recipe") == recipe
             and _digest(review.get("producer_sha256")), f"Missing accepted review/recipe metadata for {name}")
    inputs = review.get("input_sha256")
    _require(isinstance(inputs, dict) and inputs and all(isinstance(k, str) and k and _digest(v) for k, v in inputs.items()),
             "Reviewed input provenance digests required")
    _require("npz" in product, "Manifest must explicitly declare NPZ or null")
    relative = f".cache/ai16/{name}"
    for suffix in (".partial.json", ".tmp.json", ".tmp.npz"):
        _absent(relative + suffix)
    descriptor = product["npz"]
    if descriptor is None:
        _absent(relative + ".npz")
    else:
        _require(name != _SPECIAL and isinstance(descriptor, dict), "Corrected Special is a JSON-only product")
    data = _json(_verified(relative + ".json", product.get("json")))
    if descriptor is not None:
        arrays = _arrays(_verified(relative + ".npz", descriptor), descriptor.get("arrays"))
        _require(not (data.keys() & arrays.keys()), "JSON/NPZ key collision")
        data.update(arrays)
    if name == _SPECIAL:
        _special(data)
    return data


def validate_captions(language):
    """Require reviewed Chinese captions to be installed in the shared table; do not mutate it."""
    if language != "zh":
        return
    local = _json(_read("videos/ai/ai16/text_zh_reviewed.json", 32 * 1024 * 1024))
    shared = _json(_read("videos/ai/ai_text_zh.json", 32 * 1024 * 1024))
    for table in (local, shared):
        _require(isinstance(table.get("strings"), dict) and isinstance(table.get("patterns"), list),
                 "Invalid reviewed caption table")
        _require(all(isinstance(k, str) and isinstance(v, str) for k, v in table["strings"].items()),
                 "Invalid exact caption entry")
        for pair in table["patterns"]:
            _require(isinstance(pair, list) and len(pair) == 2 and all(isinstance(x, str) for x in pair),
                     "Invalid caption pattern entry")
            try:
                re.compile(pair[0])
            except re.error as error:
                raise ReviewedInputError("Invalid reviewed caption regex") from error
    _require(all(shared["strings"].get(k) == v for k, v in local["strings"].items()),
             "Install the reviewed Part 16 exact captions in the shared table")
    for pattern, replacement in local["patterns"]:
        matches = [value for key, value in shared["patterns"] if key == pattern]
        _require(matches and all(value == replacement for value in matches),
                 "Install the reviewed Part 16 caption patterns without conflicting replacements")
