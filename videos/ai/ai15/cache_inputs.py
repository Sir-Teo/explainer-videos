"""Read-only, content-pinned inputs for Part 15 scenes; never run a producer."""

from __future__ import annotations

import hashlib
import io
import json
import math
from pathlib import Path
import re
import zipfile

import numpy as np


class CacheInputError(RuntimeError):
    """A scene input is absent or outside the reviewed input contract."""


BLOCKED = frozenset({"selfcache", "scoreboard"})


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CacheInputError("Duplicate JSON keys are not valid scene inputs")
        result[key] = value
    return result


def _json(raw):
    def invalid(value):
        raise CacheInputError("Nonfinite JSON numbers are not valid scene inputs")

    try:
        result = json.loads(raw, object_pairs_hook=_pairs, parse_constant=invalid)
        def finite(value):
            if isinstance(value, float) and not math.isfinite(value):
                raise CacheInputError("Nonfinite JSON numbers are not valid scene inputs")
            if isinstance(value, dict):
                for child in value.values():
                    finite(child)
            elif isinstance(value, list):
                for child in value:
                    finite(child)
        finite(result)
        return result
    except (ValueError, UnicodeError) as exc:
        raise CacheInputError("Invalid scene-input JSON") from exc


class ReadOnlyInputs:
    """Read only the exact files declared by a reviewed contract.

    ``root`` is the repository root. No directory creation, locks, pickles,
    generated fallback, environment opt-out or scientific imports are used.
    """

    def __init__(self, root, contract):
        root = Path(root).absolute()
        if any(parent.is_symlink() for parent in (root, *root.parents)):
            raise CacheInputError("Symlink repository roots or ancestors are not accepted")
        self.root = root.resolve()
        self.contract = contract

    def _bytes(self, name, suffix, entry):
        relative = Path(".cache") / "ai15" / f"{name}.{suffix}"
        path = self.root
        for part in relative.parts:
            path = path / part
            if path.is_symlink():
                raise CacheInputError(f"Symlink not accepted for {relative.as_posix()}")
        if not path.is_file():
            raise CacheInputError(f"Required reviewed input missing: {relative.as_posix()}")
        if path.stat().st_size != entry["bytes"]:
            raise CacheInputError(f"Incompatible reviewed input: {relative.as_posix()}")
        with path.open("rb") as stream:
            raw = stream.read(entry["bytes"] + 1)
        if len(raw) != entry["bytes"] or hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise CacheInputError(f"Incompatible reviewed input: {relative.as_posix()}")
        return raw

    def load(self, name):
        # These outcomes have a separate scientific correction and publication gate.
        # In particular, never accept the legacy selfcache merely because it exists.
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", name):
            raise CacheInputError("Invalid scene-input name")
        if name in BLOCKED:
            raise CacheInputError(
                f"{name} is blocked pending separate corrected-source and numerical-input review; "
                "no historical or unchecked corrected cache is accepted"
            )
        if self.contract.get("schema") != 1 or name not in self.contract.get("items", {}):
            raise CacheInputError(f"No reviewed input contract for {name}")
        item = self.contract["items"][name]
        result = _json(self._bytes(name, "json", item["json"]))
        if not isinstance(result, dict):
            raise CacheInputError("A scene input must be a JSON object")
        if "npz" not in item:
            # An unlisted array sidecar must not silently change a JSON-only item.
            sidecar = self.root / ".cache" / "ai15" / f"{name}.npz"
            if sidecar.exists() or sidecar.is_symlink():
                raise CacheInputError(f"Unexpected array sidecar for {name}")
            return result
        raw = self._bytes(name, "npz", item["npz"])
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                members = archive.namelist()
                expected = {f"{key}.npy" for key in item["arrays"]}
                if len(members) != len(set(members)) or set(members) != expected:
                    raise CacheInputError("Unexpected or duplicate NPZ members")
                if any("/" in member or "\\" in member for member in members):
                    raise CacheInputError("Nested NPZ paths are not accepted")
            with np.load(io.BytesIO(raw), allow_pickle=False) as arrays:
                for key, spec in item["arrays"].items():
                    array = arrays[key]
                    if key in result or array.dtype.hasobject:
                        raise CacheInputError("Object arrays or duplicate array/JSON keys are not accepted")
                    if list(array.shape) != spec["shape"] or array.dtype.str != spec["dtype"]:
                        raise CacheInputError(f"Incompatible array schema for {name}/{key}")
                    result[key] = array
        except (ValueError, OSError, zipfile.BadZipFile, KeyError) as exc:
            raise CacheInputError(f"Invalid reviewed arrays for {name}") from exc
        return result


def load(name):
    # Check the scientific gate before reading even the local contract.
    if isinstance(name, str) and name in BLOCKED:
        raise CacheInputError(
            f"{name} is blocked pending separate corrected-source and numerical-input review; "
            "no historical or unchecked corrected cache is accepted"
        )
    contract = _json(Path(__file__).with_name("cache_inputs.json").read_bytes())
    return ReadOnlyInputs(Path(__file__).resolve().parents[3], contract).load(name)
