"""Part 7 cache lineage and structure; status/current never run producers.

Ordinary load retains the series' registered-producer fallback. Cached-only
loads fail before execution or preservation writes. Legacy bytes are never
upgraded into evidence of a generation whose inputs were not observed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from contextlib import nullcontext as _no_lock
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import threading
import time
import uuid
import zipfile
import zlib

import numpy as np

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, cache_signature
from . import contracts

SCHEMA_VERSION = 1
REQUIRED = contracts.REQUIRED
ITEM_DEPENDENCIES = contracts.ITEM_DEPENDENCIES


class CacheValidationError(ValueError):
    """Missing, legacy, malformed or stale data needs an explicit preparation step."""


def digest(path):
    p = Path(path)
    before = p.stat()
    h = hashlib.sha256()
    with p.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    after = p.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise CacheValidationError(f"File changed while fingerprinting: {p}")
    return h.hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     default=float, allow_nan=False).encode()).hexdigest()


def same(a, b):
    return canonical(a) == canonical(b)


def read_json(path):
    def invalid(value):
        raise ValueError(f"Nonfinite JSON number: {value}")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), parse_constant=invalid, object_pairs_hook=unique)


def cached_only():
    return os.environ.get("EXPLAINER_CACHED_ONLY", "").strip().lower() in ("1", "true", "yes")


def array_manifest(arrays):
    return {key: dict(shape=list(a.shape), dtype=a.dtype.str)
            for key, a in sorted(arrays.items())}


def partial_parameters(params):
    if (not isinstance(params, dict) or type(params.get("order")) is not int
            or type(params.get("valid")) is not int
            or params["order"] != contracts.BAYESOPT["order"]
            or params["valid"] != contracts.BAYESOPT["valid"]):
        raise CacheValidationError("Bayesopt partial parameters do not match the declared objective")
    return json.loads(json.dumps(dict(parameters=params, configuration=contracts.BAYESOPT),
                                default=float, allow_nan=False))


def validate_public_book(path, book_id):
    """Bounded Gutenberg identity/body sanity check, not an upstream generation attestation."""
    path = Path(path)
    if not path.is_file() or not 30_000 <= path.stat().st_size <= 16 * 1024 * 1024:
        raise CacheValidationError(f"Part7 book {book_id}: missing/empty or implausibly sized public text: {path}")
    text = path.read_text(encoding="utf-8-sig", errors="strict").replace("\r", "")
    head = text[:12_000]
    start = re.search(r"\*\*\* ?START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK[^\n]*\n", text)
    end = re.search(r"\*\*\* ?END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK", text)
    identity = re.search(rf"(?:ebook|etext)\s*#?\s*{book_id}\b", head, re.I)
    if (not start or not end or end.start() <= start.end() or not identity
            or re.search(r"<html|<!doctype\s+html", text[:4096], re.I) or "\0" in text):
        raise CacheValidationError(f"Part7 book {book_id}: invalid Gutenberg identity/body; existing bytes left untouched")
    body = text[start.end():end.start()]
    if len(body) < 30_000 or len(re.findall(r"[a-zA-Z]+", body)) < 5000:
        raise CacheValidationError(f"Part7 book {book_id}: body is too short; existing bytes left untouched")
    return dict(book_id=book_id, bytes=path.stat().st_size, sha256=digest(path),
                validation="Gutenberg ID/START/END, non-HTML UTF8 body >=30000chars/5000words")


class ContractPartial:
    """Resumable pieces bound to the complete generation lineage and parameters."""
    def __init__(self, cache, name, params, lineage, *, force=False):
        self.cache, self.name, self.lineage = cache, name, lineage
        self.path = cache.dir / f"{name}.partial.json"
        self.params = partial_parameters(params)
        self.done = {}
        if self.path.exists():
            reason = None
            try:
                prior = read_json(self.path)
                if force:
                    reason = "explicit force starts a fresh item; no prior pieces reused"
                elif not (isinstance(prior, dict) and set(prior) == {"schema_version", "lineage", "params", "done", "done_sha256"}
                          and type(prior["schema_version"]) is int and prior["schema_version"] == SCHEMA_VERSION
                          and same(prior["lineage"], lineage) and same(prior["params"], self.params)
                          and isinstance(prior["done"], dict)
                          and prior["done_sha256"] == canonical(prior["done"])
                          and all(self.valid_piece(k, v) for k, v in prior["done"].items())):
                    reason = "legacy, malformed or incompatible partial; no lineage inferred"
                else:
                    self.done = prior["done"]
            except (OSError, ValueError, TypeError, KeyError):
                reason = "unreadable or malformed partial; no pieces reused"
            if reason:
                cache._preserve(name, [self.path], reason, remove=True)

    def valid_piece(self, key, value):
        return self.name == "bayesopt" and contracts.bayesopt_piece(key,value)

    def __contains__(self, key):
        return key in self.done

    def __getitem__(self, key):
        return self.done[key]

    def __setitem__(self, key, value):
        if cached_only():
            raise CacheValidationError("Cached-only execution cannot write a partial")
        self.cache._assert_lineage(self.name, self.lineage)
        plain = json.loads(json.dumps(value, default=float, allow_nan=False))
        if not self.valid_piece(key, plain):
            raise CacheValidationError(f"{self.name}/{key}: malformed checkpoint piece")
        self.done[key] = plain
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(dict(schema_version=SCHEMA_VERSION, lineage=self.lineage,
                                      params=self.params, done=self.done, done_sha256=canonical(self.done)), allow_nan=False))
        tmp.replace(self.path)

    def finish(self):
        # The final item is not yet published when a producer calls finish.
        # Keep the expensive pieces until the JSON+NPZ commit succeeds.
        self.cache._assert_lineage(self.name, self.lineage)


class SchemaCache(Cache):
    @property
    def repo_root(self):
        return getattr(self, "_repo_root", Path(__file__).resolve().parents[3])

    @repo_root.setter
    def repo_root(self, value):
        self._repo_root = Path(value)

    def _source_hashes(self):
        paths = ("videos/ai/ai7/compute.py", "videos/ai/ai7/contracts.py", "videos/ai/ai7/cache_contract.py",
                 "videos/ai/ai7/infini.py", "videos/ai/ai1/compute.py", "videos/ai/ai5/compute.py",
                 "videos/ai/ai6/compute.py", "videos/ai/ai6/contracts.py", "videos/ai/ai6/cache_contract.py",
                 "explainer/ai/cache.py", "explainer/cache_lock.py")
        return {p:digest(self.repo_root/p) for p in paths}

    def bind(self, items):
        """Bind the loaded producer set before source files can drift in a long process."""
        if set(items) != set(REQUIRED):
            raise ValueError("Part 7 producer inventory differs from its contract")
        sources = self._source_hashes()
        if getattr(self, "_bound_sources", sources) != sources:
            raise CacheValidationError("Part 7 loaded producer/helper sources changed; restart the process")
        self.items = items
        self._bound_sources = sources

    def recipe(self, name):
        if name not in REQUIRED:
            raise KeyError(name)
        sources = self._source_hashes()
        if getattr(self, "_bound_sources", sources) != sources:
            raise CacheValidationError("Part 7 loaded producer/helper sources changed; restart the process")
        return dict(item=name, schema_version=SCHEMA_VERSION, sources=sources,
                    runtime=contracts.runtime_identity(), scope="Part7 producer/contracts/suffix index and used Part1/5/6/cache helpers")

    def _file_identity(self, paths):
        out = {}
        for path in paths:
            p = Path(path)
            if not p.is_file() or not p.stat().st_size:
                raise CacheValidationError(f"Part 7 prerequisite missing/empty: {p}; prepare Part1 corpus explicitly")
            out[str(p.relative_to(self.dir.parent))] = dict(bytes=p.stat().st_size, sha256=digest(p))
        return out

    def _upstream_status(self, part, name):
        """Only pure contracts may be imported here, never a producer module."""
        if part == "ai6":
            from videos.ai.ai6.cache_contract import SchemaCache as UpstreamCache
            upstream = UpstreamCache("ai6")
            upstream.dir, upstream.repo_root = self.dir.parent / "ai6", self.repo_root
            status = upstream.status(name)
            if status["status"] != "current":
                raise CacheValidationError(f"Part6/{name} is {status['status']}: {status['reason']}")
            return
        p = self.dir.parent / part / (name + ".json")
        data, _, _ = self._read_payload(p)
        # Part1 predates observed lineage. This is structural/current-byte scope,
        # not a retrospective claim about its original consumed inputs.
        if name == "raw":
            rows = data.get("rows")
            best = data.get("best")
            valid = (isinstance(rows,list) and rows and contracts.integer(best,0,len(rows)-1)
                     and all(isinstance(r,dict) and contracts.scalar(r.get("test"),0) for r in rows)
                     and contracts.scalar(data.get("best_bits"),0)
                     and np.isclose(data["best_bits"],rows[best]["test"]))
        else:
            valid = contracts.board_rows(data.get("rows")) and isinstance(data.get("passage"),str)
        if not valid:
            raise CacheValidationError(f"Existing Part1/{name} prerequisite is malformed")

    def dependencies(self, name):
        if name not in REQUIRED:
            raise KeyError(name)
        files, cohort = {}, None
        if name in contracts.PAGES_ITEMS:
            self._upstream_status("ai6", "pages")
            p = self.dir.parent / "ai6/pages.json"
            data, _, _ = self._read_payload(p)
            paths = [p,p.with_suffix(".npz")]
            files.update(self._file_identity(paths))
            y, test = np.asarray(data["y"]),np.asarray(data["test"],bool)
            cohort = dict(n_pages=len(y),n_train=int((~test).sum()),n_test=int(test.sum()),
                          labels_sha256=canonical(y.tolist()),split_sha256=canonical(test.tolist()),
                          vocabulary_sha256=canonical(data["vocab"]),protocol=data["protocol"])
        for text in contracts.TEXT_INPUTS.get(name, ()):
            p = self.dir.parent / "ai1" / (text + ".txt")
            files.update(self._file_identity([p]))
            with p.open("rb") as stream:
                prefix = stream.read(4096)
            if b"\0" in prefix or re.search(br"<html|<!doctype\s+html",prefix,re.I):
                raise CacheValidationError(f"Malformed existing text prerequisite: {p}")
        if name == "lda":
            for book_id in contracts.BOOK_IDS:
                p = self.dir.parent / "ai1/books" / f"{book_id}.txt"
                validate_public_book(p,book_id)
                files.update(self._file_identity([p]))
        for item in contracts.PART1_ITEMS.get(name, ()):
            self._upstream_status("ai1",item)
            p = self.dir.parent / "ai1" / (item + ".json")
            files.update(self._file_identity([p]+([p.with_suffix(".npz")] if p.with_suffix(".npz").exists() else [])))
        for dependency in ITEM_DEPENDENCIES.get(name, ()):
            status = self.status(dependency)
            if status["status"] != "current":
                raise CacheValidationError(f"{name}: prerequisite {dependency} is {status['status']}: {status['reason']}")
            p = self.path(dependency)
            files.update(self._file_identity([p]+([p.with_suffix(".npz")] if p.with_suffix(".npz").exists() else [])))
        return dict(files=files,cohort=cohort,
                    upstream_scope="Part6 schema/currentness; Part1 observed existing bytes/structure only; no legacy lineage inferred")

    def lineage(self, name):
        return dict(recipe=self.recipe(name), dependencies=self.dependencies(name))

    def _assert_lineage(self, name, expected):
        if not same(self.lineage(name), expected):
            raise CacheValidationError(f"{name}: source/runtime/prerequisite identity changed; no publication")

    @staticmethod
    def _read_payload(path):
        d = read_json(path)
        if not isinstance(d, dict):
            raise ValueError("Completed JSON must be a dictionary")
        meta = d.pop("_cache", None)
        arrays = {}
        npz = path.with_suffix(".npz")
        if npz.exists():
            # Explicitly own the stream even if a corrupt ZIP raises in np.load's constructor.
            with npz.open("rb") as stream:
                with np.load(stream, allow_pickle=False) as archive:
                    if len(archive.files) != len(set(archive.files)):
                        raise ValueError("Duplicate NPZ entries")
                    for key in archive.files:
                        a = archive[key]
                        if key in d or a.dtype.kind not in "biuf" or a.dtype.hasobject:
                            raise ValueError("Duplicate or nonnumeric/object array")
                        arrays[key] = a
                        d[key] = a
        return d, meta, arrays

    def status(self, name):
        """Pure validation: no producer import/call, locks, cache writes or migration."""
        result = dict(item=name, status="missing", reason="completed JSON is absent")
        if name not in REQUIRED:
            return dict(item=name, status="unknown", reason="unknown Part7 item")
        p = self.path(name)
        if not p.exists():
            return result
        try:
            signature = cache_signature(p)
            raw = read_json(p)
            if not isinstance(raw, dict):
                return dict(item=name, status="malformed", reason="completed JSON is not a dictionary")
            meta = raw.pop("_cache", None)
            if meta is None:
                return dict(item=name, status="legacy", reason="no observed generation lineage; original bytes untouched")
            if not isinstance(meta, dict) or type(meta.get("schema_version")) is not int:
                return dict(item=name, status="malformed", reason="invalid cache metadata/version type")
            if meta["schema_version"] != SCHEMA_VERSION:
                return dict(item=name, status="stale", reason="unsupported schema version")
            lineage = self.lineage(name)
            data, _, arrays = self._read_payload(p)
            required = contracts.required_arrays(name, data)
            if not required <= arrays.keys():
                return dict(item=name, status="malformed", reason=f"required NPZ arrays missing: {sorted(required - arrays.keys())}")
            expected = dict(schema_version=SCHEMA_VERSION, origin="observed-producer-generation",
                            lineage=lineage, observed_reads=lineage["dependencies"]["files"], payload_sha256=canonical(raw),
                            arrays_sha256=digest(p.with_suffix(".npz")) if p.with_suffix(".npz").exists() else None,
                            arrays=array_manifest(arrays))
            if not same(meta, expected):
                return dict(item=name, status="stale", reason="source/runtime/input/payload/array identity mismatch")
            if not contracts.valid_structure(name, data, lineage["dependencies"]["cohort"]):
                return dict(item=name, status="malformed", reason="required fields, shapes, finite values or cohort inconsistent")
            if signature != cache_signature(p):
                return dict(item=name, status="stale", reason="payload changed during validation")
            self._assert_lineage(name, lineage)
            return dict(item=name, status="current", reason="observed lineage, exact integrity and bounded structure match")
        except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError, EOFError,
                OverflowError, zipfile.BadZipFile, zlib.error) as exc:
            return dict(item=name, status="stale", reason=f"{type(exc).__name__}: {exc}")

    def current(self, name):
        return self.status(name)["status"] == "current"

    def _preserve(self, name, paths, reason, *, remove=False):
        if cached_only():
            raise CacheValidationError("Cached-only validation cannot preserve/migrate cache files")
        paths = [p for p in paths if p.exists()]
        if not paths:
            return
        folder = self.dir / "preserved" / (name + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "-" + uuid.uuid4().hex[:8])
        folder.mkdir(parents=True)
        rows = []
        for p in paths:
            target = folder / p.name
            before = digest(p)
            shutil.copy2(p, target)
            if digest(target) != before or digest(p) != before:
                raise CacheValidationError("Preservation byte verification failed; original not removed")
            rows.append(dict(original=str(p), retained=target.name, bytes=target.stat().st_size, sha256=before))
        (folder / "receipt.json").write_text(json.dumps(dict(reason=reason, files=rows), indent=2))
        if remove:
            for p in paths:
                p.unlink()

    def _produce(self, name, producer, *, force=False):
        if cached_only():
            raise CacheValidationError(f"ai7/{name}: cached-only execution prohibits generation")
        with cache_lock(self.path(name)):
            # Ordinary first-use compatibility may prepare registered local
            # item dependencies; corpus prerequisites never download on load.
            for dependency in ITEM_DEPENDENCIES.get(name, ()):
                self.load(dependency)
            lineage = self.lineage(name)
            active = getattr(self, "_active", None)
            if active is None:
                self._active = active = {}
            if name in active:
                raise CacheValidationError(f"Recursive producer for {name}")
            active[name] = dict(lineage=lineage, force=force, partial=None,
                                observed_reads={}, thread=threading.get_ident())
            try:
                out = producer()
                self._assert_lineage(name, lineage)
                self.save(name, out)
            finally:
                active.pop(name, None)

    def require_inputs(self, name):
        """Read-only prerequisite preflight; missing corpus is never prepared here."""
        return self.dependencies(name)

    def read_text(self, kind):
        base = kind.removesuffix("27")
        if base not in ("train", "valid", "passage"):
            raise KeyError(kind)
        p = self.dir.parent / "ai1" / (base + ".txt")
        text = self._consume_text(p)
        return contracts.to27(text) if kind.endswith("27") else text

    def read_book(self, book_id):
        if book_id not in contracts.BOOK_IDS:
            raise KeyError(book_id)
        p = self.dir.parent / "ai1/books" / f"{book_id}.txt"
        validate_public_book(p, book_id)
        return self._consume_text(p, errors="replace")

    def _consume_text(self, path, *, errors="strict"):
        before = self._file_identity([path])
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != next(iter(before.values()))["sha256"]:
            raise CacheValidationError("Text changed between snapshot and read")
        if not raw or b"\0" in raw or re.search(br"<html|<!doctype\s+html", raw[:4096], re.I):
            raise CacheValidationError(f"Invalid existing text input: {path}")
        text = raw.decode("utf-8", errors=errors).replace("\r\n", "\n").replace("\r", "\n")
        self._record_reads(before)
        return text

    def read_pages(self):
        self._upstream_status("ai6", "pages")
        p = self.dir.parent / "ai6/pages.json"
        return self._consume_payload(p)

    def read_part1(self, name):
        if name not in ("raw", "scoreboard"):
            raise KeyError(name)
        self._upstream_status("ai1", name)
        return self._consume_payload(self.dir.parent / "ai1" / (name + ".json"))

    def _consume_payload(self, path):
        paths = [path] + ([path.with_suffix(".npz")] if path.with_suffix(".npz").exists() else [])
        before = self._file_identity(paths)
        data, _, _ = self._read_payload(path)
        if not same(before, self._file_identity(paths)):
            raise CacheValidationError("Upstream payload changed during read")
        self._record_reads(before)
        return data

    def _record_reads(self, observed):
        for active in tuple(getattr(self, "_active", {}).values()):
            if active["thread"] != threading.get_ident():
                continue
            required = active["lineage"]["dependencies"]["files"]
            for key, value in observed.items():
                if key not in required:
                    raise CacheValidationError(f"Undeclared dependency read during generation: {key}")
                if not same(value, required[key]):
                    raise CacheValidationError(f"Consumed input differs from generation snapshot: {key}")
                active["observed_reads"][key] = value

    def load(self, name):
        if name not in REQUIRED:
            raise KeyError(name)
        status = self.status(name)
        # Do this before taking a lock, which otherwise creates a lock file.
        if status["status"] != "current" and cached_only():
            raise CacheValidationError(f"ai7/{name}: {status['status']}: {status['reason']}; prepare data explicitly")
        with cache_lock(self.path(name)):
            if not self.current(name):
                if cached_only():
                    raise CacheValidationError(f"ai7/{name}: changed before cached-only load")
                if not self.items:
                    self.bind(importlib.import_module("videos.ai.ai7.compute").ITEMS)
                self._produce(name, self.items[name])
            # Preserve the common loader's instrumentation and downstream API.
            # Callers receive mutable arrays/dicts. Do not mistake a mutated
            # prior return value for the published bytes just validated above.
            self._loaded.pop(name, None)
            self._loaded_signatures.pop(name, None)
            value = super().load(name)
            paths = [self.path(name)] + ([self.path(name).with_suffix(".npz")] if self.path(name).with_suffix(".npz").exists() else [])
            self._record_reads(self._file_identity(paths))
            return value

    def partial(self, name, params):
        active = getattr(self, "_active", {}).get(name)
        if active is None or active["thread"] != threading.get_ident() or name != "bayesopt":
            raise CacheValidationError("Part7 resumable pieces require their active registered generation")
        if active["partial"] is None:
            active["partial"] = ContractPartial(self, name, params, active["lineage"], force=active["force"])
        elif not same(active["partial"].params, partial_parameters(params)):
            raise CacheValidationError("Partial parameters changed inside one generation")
        return active["partial"]

    def save(self, name, out):
        active = getattr(self, "_active", {}).get(name)
        if active is None or active["thread"] != threading.get_ident() or cached_only():
            raise CacheValidationError("Completed Part7 cache can be published only by its observed producer run")
        lineage = active["lineage"]
        self._assert_lineage(name, lineage)
        if not same(active["observed_reads"], lineage["dependencies"]["files"]):
            raise CacheValidationError(f"{name}: expected prerequisite bytes were not read by this generation")
        if not isinstance(out, dict) or "_cache" in out or not contracts.valid_structure(name, out, lineage["dependencies"]["cohort"]):
            raise CacheValidationError(f"{name}: malformed producer output; prior completed bytes untouched")
        arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
        if not contracts.required_arrays(name, out) <= arrays.keys():
            raise CacheValidationError(f"{name}: producer omitted required top-level arrays")
        rest = json.loads(json.dumps({k: v for k, v in out.items() if k not in arrays}, default=float, allow_nan=False))
        self.dir.mkdir(parents=True, exist_ok=True)
        p = self.path(name); npz = p.with_suffix(".npz"); tmp = p.with_suffix(".tmp.npz")
        if arrays:
            np.savez_compressed(tmp, **arrays)
        meta = dict(schema_version=SCHEMA_VERSION, origin="observed-producer-generation", lineage=lineage, observed_reads=active["observed_reads"],
                    payload_sha256=canonical(rest), arrays_sha256=digest(tmp) if arrays else None,
                    arrays=array_manifest(arrays))
        marker = p.with_suffix(".tmp.json")
        marker.write_text(json.dumps(dict(rest, _cache=meta), ensure_ascii=False, indent=1, allow_nan=False))
        self._assert_lineage(name, lineage)
        # Never overwrite the only remaining bytes of an old/legacy result.
        self._preserve(name, [p, npz], "completed bytes replaced by a new observed producer generation")
        p.unlink(missing_ok=True)
        if arrays:
            tmp.replace(npz)
        else:
            npz.unlink(missing_ok=True)
        marker.replace(p)
        self._loaded.pop(name, None); self._loaded_signatures.pop(name, None)
        partial = self.dir / f"{name}.partial.json"
        self._preserve(name, [partial], "completed item atomically published; resumable proof retained", remove=True)

    def main(self, items, doc=None):
        self.bind(items)
        parser = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("names", nargs="*")
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--check", action="store_true", help="pure status; no producers or writes")
        args = parser.parse_args()
        names = args.names or list(items)
        if any(name not in items for name in names):
            raise KeyError("Unknown Part7 item")
        if args.check:
            statuses = [self.status(name) for name in names]
            print(json.dumps(statuses, indent=2))
            if any(s["status"] != "current" for s in statuses):
                raise SystemExit(1)
            return
        if cached_only() and args.force:
            raise CacheValidationError("Cached-only CLI cannot force generation")
        for name in names:
            with cache_lock(self.path(name)) if not cached_only() else _no_lock():
                if self.current(name) and not args.force:
                    print(f"  cached  {name}", flush=True)
                    continue
                start = time.monotonic()
                self._produce(name, items[name], force=args.force)
                print(f"  done    {name} in {time.monotonic()-start:.1f}s", flush=True)
