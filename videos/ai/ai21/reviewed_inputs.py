"""Read reviewed Part 21 result bytes; never import or invoke a producer.

An independent operator must supply .cache/ai21/render-manifest.json after
checking provenance, numerical outputs and source compatibility. The manifest
is an assertion about identified bytes, not scientific evidence by itself.
This source module supplies no data, result manifest or acceptance record.
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
_MANIFEST = ".cache/ai21/render-manifest.json"
_MAX_BYTES = 256 * 1024 * 1024
_SOURCES = frozenset(f"videos/ai/ai21/{name}.py" for name in
                     ("compute", "exact", "train2d", "fewstep", "discrete", "textlm"))
_PRODUCTS = frozenset(("mix", "forward", "tweedie", "sde", "solvers", "schedules", "edmtargets", "transport",
                       "discrete", "denoiser", "solvers_net", "ablate", "flow", "fewstep", "distill", "guidance",
                       "glyphs", "textlm"))
_UPSTREAM = {"tf": ".cache/ai13/tf.json", "scoreboard": ".cache/ai1/scoreboard.json"}


class ReviewedInputError(RuntimeError):
    """Missing, incompatible or unreviewed input; no computation was attempted."""


def _require(condition, message):
    if not condition:
        raise ReviewedInputError(message)

def _read(relative, limit=_MAX_BYTES):
    """Read one regular file through directory descriptors, without following links."""
    path = PurePosixPath(relative)
    _require(not path.is_absolute() and path.parts and all((p not in ('.', '..') for p in path.parts)), 'Invalid reviewed-input path')
    _require(hasattr(os, 'O_NOFOLLOW') and hasattr(os, 'O_DIRECTORY'), 'Reviewed inputs require no-symlink directory reads on this platform')
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
        _require(stat.S_ISREG(before.st_mode), f'Input is not a regular file: {relative}')
        _require(before.st_size <= limit, f'Reviewed input exceeds its size bound: {relative}')
        chunks, size = ([], 0)
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, limit + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            _require(size <= limit, f'Reviewed input grew beyond its size bound: {relative}')
        after = os.fstat(descriptor)
        signature = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        _require(signature(before) == signature(after) and size == before.st_size, f'Reviewed input changed during its read: {relative}')
        return b''.join(chunks)
    except OSError as error:
        raise ReviewedInputError(f'Cannot read reviewed input: {relative}') from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if directory is not None:
            os.close(directory)

def _pairs(pairs):
    out = {}
    for key, value in pairs:
        _require(key not in out, f'Duplicate JSON key: {key}')
        out[key] = value
    return out

def _finite_json(value):
    if isinstance(value, float):
        _require(math.isfinite(value), 'Nonfinite JSON number')
    elif isinstance(value, dict):
        for child in value.values():
            _finite_json(child)
    elif isinstance(value, list):
        for child in value:
            _finite_json(child)

def _json(data):
    try:
        out = json.loads(data, object_pairs_hook=_pairs, parse_constant=lambda _: _require(False, 'Nonfinite JSON constant'))
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ReviewedInputError('Invalid reviewed JSON') from error
    _require(isinstance(out, dict), 'Reviewed JSON must contain an object')
    try:
        _finite_json(out)
    except RecursionError as error:
        raise ReviewedInputError('Reviewed JSON nesting is too deep') from error
    return out

def _digest(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None

def _verified(relative, identity):
    _require(isinstance(identity, dict) and _digest(identity.get('sha256')), 'Missing file digest')
    size = identity.get('bytes')
    _require(type(size) is int and 0 < size <= _MAX_BYTES, 'Invalid reviewed file size')
    data = _read(relative, size)
    _require(len(data) == size and hashlib.sha256(data).hexdigest() == identity['sha256'], f'Reviewed file identity mismatch: {relative}')
    return data

def _absent(relative):
    try:
        os.lstat(_ROOT / relative)
    except FileNotFoundError:
        return
    except OSError as error:
        raise ReviewedInputError(f'Cannot establish absent sibling: {relative}') from error
    raise ReviewedInputError(f'Unexpected reviewed-input sibling: {relative}')

def _arrays(data, declared):
    _require(isinstance(declared, dict), 'NPZ array declarations are required')
    try:
        with np.load(io.BytesIO(data), allow_pickle=False) as archive:
            _require(len(archive.files) == len(set(archive.files)) and set(archive.files) == declared.keys(), 'NPZ array inventory mismatch')
            out = {}
            for name, spec in declared.items():
                _require(isinstance(spec, dict) and isinstance(spec.get('dtype'), str), 'Invalid array dtype declaration')
                shape = spec.get('shape')
                _require(isinstance(shape, list) and all((type(x) is int and x >= 0 for x in shape)), 'Invalid array shape declaration')
                dtype = np.dtype(spec['dtype'])
                _require(not dtype.hasobject, 'Object arrays are forbidden')
                array = archive[name]
                _require(array.dtype == dtype and list(array.shape) == shape and (not array.dtype.hasobject), f'Array dtype/shape mismatch: {name}')
                if array.dtype.kind in 'fc':
                    _require(bool(np.isfinite(array).all()), f'Nonfinite array: {name}')
                out[name] = array.copy()
            return out
    except ReviewedInputError:
        raise
    except (ValueError, TypeError, OverflowError, OSError, EOFError, KeyError, zipfile.BadZipFile) as error:
        raise ReviewedInputError('Invalid reviewed NPZ') from error

def _manifest():
    _require(os.environ.get("AI21_QUICK") != "1", "Quick fixtures are not reviewed Part 21 render inputs")
    data = _json(_read(_MANIFEST, 1024 * 1024))
    _require(type(data.get("schema_version")) is int and data["schema_version"] == 1
             and data.get("part") == "ai21", "Unsupported Part 21 render-manifest schema")
    sources = data.get("compatibility_sources")
    _require(isinstance(sources, dict) and sources.keys() == _SOURCES,
             "Manifest must pin all six Part 21 scientific sources")
    for relative, digest in sources.items():
        _require(_digest(digest) and hashlib.sha256(_read(relative)).hexdigest() == digest,
                 f"Incompatible scientific source: {relative}")
    products, upstream = data.get("products"), data.get("upstream", {})
    _require(isinstance(products, dict) and products.keys() <= _PRODUCTS, "Unsupported Part 21 product")
    _require(isinstance(upstream, dict) and upstream.keys() <= _UPSTREAM.keys(), "Unsupported upstream input")
    return products, upstream


def _review(entry, recipe):
    _require(isinstance(entry, dict), "Missing reviewed product descriptor")
    review = entry.get("review")
    _require(isinstance(review, dict) and review.get("accepted") is True and review.get("recipe") == recipe,
             f"Input has not been accepted with recipe {recipe}")
    _require(_digest(review.get("producer_sha256")), "Missing actual producer source identity")
    inputs = review.get("input_sha256")
    _require(isinstance(inputs, dict) and bool(inputs)
             and all(isinstance(k, str) and k and _digest(v) for k, v in inputs.items()),
             "Missing original input/provenance identities")


def load(name):
    """Return the requested reviewed JSON/NPZ data, or fail without any writes."""
    _require(isinstance(name, str) and name in _PRODUCTS, "Unsupported Part 21 product name")
    products, _ = _manifest()
    entry = products.get(name)
    recipe = "euler-common-start-v1" if name in {"solvers", "solvers_net"} else "original-recipe"
    _review(entry, recipe)
    prefix = f".cache/ai21/{name}"
    out = _json(_verified(prefix + ".json", entry.get("json")))
    _require("npz" in entry, "Manifest must declare NPZ descriptor or explicit null")
    if entry["npz"] is None:
        _absent(prefix + ".npz")
    else:
        arrays = _arrays(_verified(prefix + ".npz", entry["npz"]), entry["npz"].get("arrays"))
        _require(out.keys().isdisjoint(arrays), "JSON/NPZ fields collide")
        out.update(arrays)
    return out


def load_upstream(name):
    """Read only the reviewed historical JSON metadata used by the text scoreboard."""
    _require(isinstance(name, str) and name in _UPSTREAM, "Unsupported Part 21 upstream name")
    _, upstream = _manifest()
    entry = upstream.get(name)
    _review(entry, "historical-original")
    return _json(_verified(_UPSTREAM[name], entry.get("json")))


def validate_captions(language):
    """Require entry-wise Chinese caption composition; never alter the shared table."""
    if language != "zh":
        return
    delta = _json(_read("videos/ai/ai21/text_zh_reviewed.json"))
    shared = _json(_read("videos/ai/ai_text_zh.json"))
    _require(delta.keys() == {"strings", "phrases", "patterns"}, "Invalid Part 21 caption delta")
    for category in ("strings", "phrases"):
        entries = delta[category]
        _require(isinstance(entries, dict) and isinstance(shared.get(category), dict), "Invalid caption mapping")
        for key, value in entries.items():
            _require(isinstance(key, str) and isinstance(value, str)
                     and shared[category].get(key) == value, f"Compose reviewed Part 21 caption: {key}")
    patterns, existing = delta["patterns"], shared.get("patterns")
    _require(isinstance(patterns, list) and isinstance(existing, list), "Invalid caption patterns")
    for row in patterns:
        _require(isinstance(row, list) and len(row) == 2 and all(isinstance(v, str) for v in row),
                 "Invalid Part 21 caption pattern")
        matches = [old for old in existing if isinstance(old, list) and len(old) == 2 and old[0] == row[0]]
        _require(matches == [row], f"Compose reviewed Part 21 caption pattern: {row[0]}")
