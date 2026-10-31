"""Bounded integrity contracts for Part 3's eight formerly unversioned items.

Sidecars bind bytes and current recipe/dependency observations, not historical
proof of consumed inputs. Legacy attestation is always an explicit operation.
No function here invokes a producer, downloads a model, or changes payloads.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
import os
import zipfile
from pathlib import Path

import numpy as np

from explainer.cache_lock import cache_lock

ITEMS = frozenset(("einsum", "project", "letters", "power", "image", "depth", "galorectl", "highdim"))
VERSION = 1
ORIGINAL_PRODUCER = "2b03a02de9ae201a9955f6a88ed56f6433b5d0602186c5a3978cd4d565a616e2"


class IntegrityError(ValueError):
    """A payload or explicit attestation does not satisfy its bounded contract."""


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def sidecar_path(cache_dir, name):
    if name not in ITEMS:
        raise IntegrityError(f"unsupported integrity item: {name}")
    return Path(cache_dir) / "_integrity" / f"{name}.json"


def _expect(condition, message):
    if not condition:
        raise IntegrityError(message)


def _source_nodes(source):
    nodes = {}
    for node in ast.parse(Path(source).read_text()).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            nodes[node.name] = node
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for part in ast.walk(target):
                    if isinstance(part, ast.Name):
                        nodes[part.id] = node
    return nodes


def recipe(name, producer_source):
    """Canonical AST closure avoids invalidating data for validator-only edits.

    Includes local helpers/constants reachable through global names, excluding
    cache plumbing. External library versions and input files are separate.
    """
    _expect(name in ITEMS, "unknown recipe")
    nodes = _source_nodes(producer_source)
    pending, seen, contract = [f"compute_{name}"], set(), {}
    while pending:
        key = pending.pop()
        if key in seen or key in {"CACHE", "load", "ai1"} or key not in nodes:
            continue
        seen.add(key)
        node = nodes[key]
        contract[key] = ast.dump(node, include_attributes=False)
        pending.extend(n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load))
    _expect(f"compute_{name}" in contract, "missing producer function")
    return {"contract_version": VERSION, "producer_ast_sha256": json_digest(contract),
            "producer_symbols": sorted(contract), "numpy_version": np.__version__}


def _gpt2_files():
    # Local resolution only; never call the Hub or load any model.
    base = Path(os.environ.get("HF_HUB_CACHE", str(Path(os.environ.get("HF_HOME", str(Path.home() / ".cache/huggingface"))) / "hub")))
    repo = base / "models--openai-community--gpt2"
    ref = repo / "refs/main"
    if ref.is_file():
        revision = ref.read_text().strip()
        _expect(bool(revision) and Path(revision).name == revision, "invalid local GPT-2 revision")
    else:
        choices = list((repo / "snapshots").glob("*"))
        _expect(len(choices) == 1, "GPT-2 local revision missing or ambiguous")
        revision = choices[0].name
    files = {f"hf:openai-community/gpt2@{revision}/{name}": repo / "snapshots" / revision / name
             for name in ("config.json", "model.safetensors")}
    return files


def dependencies(name, cache_dir, root):
    """Hashes of dependencies observed now; never called original consumed inputs."""
    root, cache_dir = Path(root), Path(cache_dir)
    paths = {}
    if name == "letters":
        paths.update({f"ai1/bigram{suffix}": cache_dir.parent / "ai1" / f"bigram{suffix}"
                      for suffix in (".json", ".npz")})
        paths["source:ai1/compute.py"] = root / "videos/ai/ai1/compute.py"
    if name == "power":
        paths.update({f"ai3/letters{suffix}": cache_dir / f"letters{suffix}" for suffix in (".json", ".npz")})
        paths.update(_gpt2_files())
    if name == "galorectl":
        paths.update({f"novels/{name}": cache_dir.parent / "novels" / name
                      for name in ("train.npy", "valid.npy", "tokenizer.json")})
        paths.update({f"source:{name}": root / name for name in ("explainer/ai/novels.py", "explainer/lm/pocket.py")})
    result = {key: digest(path) if path.is_file() else None for key, path in sorted(paths.items())}
    # Bigram NPZ is optional; its JSON contains the currently used joint table.
    _expect(all(value is not None for key, value in result.items() if key != "ai1/bigram.npz"), "missing dependency")
    if name in ("power", "galorectl"):
        result["package:torch"] = importlib.metadata.version("torch")
    if name == "power":
        result["package:transformers"] = importlib.metadata.version("transformers")
    return result


def _finite(value):
    if isinstance(value, dict):
        return all(isinstance(k, str) and _finite(v) for k, v in value.items())
    if isinstance(value, list):
        return all(_finite(v) for v in value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return math.isfinite(value)
    return isinstance(value, str)


def _vector(v, length, nonnegative=True):
    _expect(isinstance(v, (list, np.ndarray)) and len(v) == length, "vector length")
    a = np.asarray(v)
    _expect(a.dtype.kind in "fiu" and a.ndim == 1 and np.isfinite(a).all(), "numeric vector")
    _expect(not nonnegative or np.all(a >= 0), "negative vector")
    return a


def _keys(value, keys):
    _expect(isinstance(value, dict) and set(value) == set(keys.split()), "payload fields")


def validate_payload(name, data, arrays):
    """Cheap structure and arithmetic checks, no factorization or experiment rerun."""
    _expect(isinstance(data, dict) and _finite(data), "malformed or nonfinite JSON")
    shapes = {
        "letters": dict(M=(26, 26), S=(26,), U=(26, 26), Vt=(26, 26), recon=(26, 26, 26), err=(26,), ca_s=(5,), ca_row=(26,), ca_col=(26,)),
        "image": dict(img=(180, 288), recon=(7, 180, 288), S=(180,)),
        "depth": {f"len{gain}": (41,) for gain in (.8, 1., 1.2)},
        "highdim": {f"{kind}{d}": (bins,) for d in (2, 3, 10, 100, 768) for kind, bins in (("angles", 36), ("norms", 40))},
    }.get(name, {})
    _expect(set(arrays) == set(shapes), "missing or unexpected array keys")
    for key, shape in shapes.items():
        a = arrays[key]
        _expect(a.shape == shape and a.dtype.kind in "fiu" and np.isfinite(a).all(), f"invalid array {key}")
    if name == "einsum":
        _keys(data, "shapes macs_left macs_right path heads n dh macs_scores macs_values macs_proj")
        _expect(data["shapes"] == [1000, 20, 1000, 20], "chain dimensions")
        a, b, c, d = data["shapes"]
        _expect(data["macs_left"] == a*b*c+a*c*d and data["macs_right"] == b*c*d+a*b*d, "chain costs")
        _expect((data["heads"], data["n"], data["dh"]) == (12, 1024, 64), "attention dimensions")
        _expect(data["macs_scores"] == data["macs_values"] == 12*1024*1024*64 and data["macs_proj"] == 4*1024*768*768, "attention costs")
        _expect(data["path"] == [[1, 2], [0, 1]], "contraction path")
    elif name == "project":
        _keys(data, "rows eps")
        _expect(len(data["rows"]) == 13 and data["eps"] == np.finfo(float).eps, "QR sample count or precision")
        for n, row in zip(range(2, 15), data["rows"]):
            _keys(row, "n kappa cgs mgs householder err_normal err_qr")
            _expect(row["n"] == n and row["kappa"] > 0 and all(v >= 0 for v in row.values()), "QR row")
    elif name == "letters":
        _keys(data, "total ca_share ca_left5 ca_vowels_left")
        _expect(data["total"] > 0 and 0 <= data["ca_share"] <= 1, "CA summary")
        left = data["ca_left5"]
        _expect(len(left) == 5 and len(set(left)) == 5 and all(x in "abcdefghijklmnopqrstuvwxyz" and len(x) == 1 for x in left), "CA letters")
        _expect(data["ca_vowels_left"] == int(sorted(left) == sorted("aeiou")), "CA vowel flag")
        S = arrays["S"]
        _expect(np.all(S >= 0) and np.all(np.diff(S) <= 1e-12), "singular values")
        _expect(np.allclose((arrays["U"] * S) @ arrays["Vt"], arrays["M"], rtol=1e-8, atol=1e-10), "SVD factorization")
        _expect(np.allclose(arrays["err"], [np.sqrt(np.sum(S[k:]**2)) for k in range(1, 27)], rtol=1e-7, atol=1e-9), "rank errors")
        _expect(np.isclose(data["total"], np.linalg.norm(arrays["M"])), "matrix norm")
    elif name == "power":
        _keys(data, "gpt2 letters")
        for key, steps in (("gpt2", 60), ("letters", 30)):
            row = data[key]; _keys(row, "lam ratio sin rq pred_tan rq_err rate_measured")
            lam = _vector(row["lam"], 8)
            _expect(lam[0] > 0 and np.all(np.diff(lam) <= 1e-10), "eigenvalue order")
            _expect(np.isclose(row["ratio"], lam[1]/lam[0]) and 0 <= row["rate_measured"] <= 1, "power rate")
            for field in ("sin", "rq", "pred_tan", "rq_err"):_vector(row[field], steps+1)
            _expect(max(row["sin"]) <= 1+1e-10, "angle sine")
            _expect(np.allclose(row["rq_err"], np.abs(np.asarray(row["rq"])-lam[0])/lam[0]), "Rayleigh errors")
    elif name == "image":
        _keys(data, "ranks err tail total shape storage pixels energy")
        ranks = [1, 2, 4, 8, 16, 32, 64]
        _expect(data["ranks"] == ranks and data["shape"] == [180, 288] and data["pixels"] == 180*288, "image shape/ranks")
        _expect(data["storage"] == [k*(180+288+1) for k in ranks], "rank storage")
        _expect(arrays["img"].dtype == np.uint8 and arrays["recon"].dtype == np.uint8, "image dtype")
        S = arrays["S"];_expect(np.all(S>=0) and np.all(np.diff(S)<=1e-10), "image spectrum")
        for field in ("err", "tail", "energy"):_vector(data[field], 7)
        _expect(np.allclose(data["err"], data["tail"], rtol=1e-8, atol=1e-8), "Eckart-Young errors")
        _expect(np.allclose(data["tail"], [np.linalg.norm(S[k:]) for k in ranks]), "tail norms")
        _expect(np.isclose(data["total"], np.linalg.norm(S)) and np.all(np.asarray(data["energy"])<=1+1e-10), "image norm/energy")
    elif name == "depth":
        _keys(data, "n layers gains sigma0.8 rate0.8 sigma1.0 rate1.0 sigma1.2 rate1.2")
        _expect(data["n"] == 256 and data["layers"] == 40 and data["gains"] == [.8, 1., 1.2], "depth recipe")
        for gain in data["gains"]:
            v = _vector(arrays[f"len{gain}"], 41)
            _expect(v[0] == 1 and data[f"sigma{gain}"] > 0 and np.isclose(data[f"rate{gain}"], v[-1]**(1/40)), "depth rate")
    elif name == "galorectl":
        _keys(data, "runs best_lr")
        lrs = (.001, .003, .01); best=data["best_lr"]
        _expect(best in lrs, "control selected LR")
        expected = {f"adamsplit_{lr:g}_0" for lr in lrs} | {f"adamsplit_{best:g}_{seed}" for seed in (1, 2)}
        _expect(set(data["runs"]) == expected, "control run coverage")
        for key, row in data["runs"].items():
            _keys(row, "method lr seed curve val dW opt_numbers weights")
            _expect(row["method"] == "adamsplit" and key == f"adamsplit_{row['lr']:g}_{row['seed']}", "control identity")
            _vector(row["curve"], len(range(0, 600, 5)))  # producer stores curve[::5]
            _expect(row["val"] >= 0 and row["weights"] > 0 and row["opt_numbers"] == 2*row["weights"], "Adam state")
            _expect(len(row["dW"]) == 10, "block matrix summaries")
            for stats in row["dW"].values():
                _keys(stats, "stable eff rank")
                _expect(0 < stats["stable"] <= stats["rank"]+1e-8 and 0 < stats["eff"] <= stats["rank"]+1e-8, "update ranks")
        _expect(best == min(lrs, key=lambda lr:data["runs"][f"adamsplit_{lr:g}_0"]["val"]), "control LR selection")
    elif name == "highdim":
        dims=[2,3,10,100,768];vd=[2,3,5,10,20,50,100,200,500,768,1000,2000,4096]
        _keys(data, "dims angle_sd2 angle_sd3 angle_sd10 angle_sd100 angle_sd768 var_dims cos_var norm_sd shell n_dirs worst_cos worst_angle")
        _expect(data["dims"] == dims and data["var_dims"] == vd and data["n_dirs"] == 10000, "dimension recipe")
        _vector(data["cos_var"],len(vd));_vector(data["norm_sd"],len(vd))
        _expect(data["shell"] == {str(d):1-.99**d for d in dims}, "shell volumes")
        for d in dims:
            _expect(0 <= data[f"angle_sd{d}"] <= 180, "angle deviation")
            for kind in ("angles","norms"):
                a=arrays[f"{kind}{d}"]
                _expect(a.dtype.kind in "iu" and np.all(a>=0) and a.sum()<=20000, "histogram counts")
            _expect(arrays[f"angles{d}"].sum()==20000,"angle sample count")
        _expect(0<=data["worst_cos"]<=1 and np.isclose(data["worst_angle"], np.degrees(np.arccos(data["worst_cos"]))), "worst angle")
    else:
        raise IntegrityError("unknown payload")


def inspect_payload(name, cache_dir):
    p=Path(cache_dir)/f"{name}.json";z=p.with_suffix(".npz")
    raw=p.read_bytes();data=json.loads(raw)
    arrays={}
    if z.exists():
        # Own the stream even if NumPy rejects a truncated ZIP during opening.
        with z.open("rb") as stream:
            with np.load(stream,allow_pickle=False) as archive:
                arrays={k:archive[k] for k in archive.files}
    validate_payload(name,data,arrays)
    return {"json_sha256":hashlib.sha256(raw).hexdigest(),"npz_sha256":digest(z) if z.exists() else None}


def _atomic_json(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(".tmp.json")
    try:
        tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+"\n")
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)


def observe_generation(name, cache_dir, root, producer_source):
    """Capture what exists before a normal producer; never create dependencies."""
    observation = {"recipe_before": recipe(name, producer_source)}
    try:
        observation["dependencies_before"] = dependencies(name, cache_dir, root)
        observation["status"] = "complete-before-observation"
    except (OSError, ValueError, importlib.metadata.PackageNotFoundError) as error:
        # A fresh producer may legitimately create its missing prerequisites.
        # Do not misrepresent a later hash as an observed consumed-input hash.
        observation.update(status="incomplete-before-observation", dependencies_before=None,
                           reason=type(error).__name__ + ": " + str(error))
    return observation


def publish(name, cache_dir, root, producer_source, *, origin, evidence=None, generation=None):
    """Caller holds item lock. Dependencies are observed at publication only."""
    _expect(origin in ("postproduction-attestation","producer-save"),"metadata origin")
    artifacts=inspect_payload(name,cache_dir)
    if origin=="postproduction-attestation":
        _expect(isinstance(evidence,dict) and evidence.get("original_producer_sha256")==ORIGINAL_PRODUCER,"legacy evidence required")
        _expect(artifacts==evidence.get("expected_artifacts"),"legacy artifact hash mismatch")
    current_recipe = recipe(name, producer_source)
    current_dependencies = dependencies(name, cache_dir, root)
    if generation is not None:
        _expect(generation["recipe_before"] == current_recipe, "producer recipe changed during generation")
        if generation["dependencies_before"] is not None:
            _expect(generation["dependencies_before"] == current_dependencies, "dependencies changed during generation")
    value={"integrity_version":VERSION,"item":name,"origin":origin,"observed_utc":datetime.now(timezone.utc).isoformat(),
           "artifacts":artifacts,"recipe":current_recipe,"dependencies_observed_now":current_dependencies,
           "dependency_scope":"Observed at publication; not proof of original consumed inputs.",
           "producer_source_at_publication_sha256":digest(producer_source),"evidence":evidence,
           "generation_observation":generation,
           "generation_scope":"Before/after stability observation when loader/CLI owns generation; direct save has publication observation only. This does not instrument every dependency read."}
    _atomic_json(sidecar_path(cache_dir,name),value)
    return value


def current(name, cache_dir, root, producer_source):
    """Read-only, fail-closed check serialized with producer/attestation writes."""
    try:
        with cache_lock(Path(cache_dir)/f"{name}.json"):
            value=json.loads(sidecar_path(cache_dir,name).read_text())
            if not isinstance(value, dict):return False
            if value.get("integrity_version")!=VERSION or value.get("item")!=name:return False
            if value.get("origin") not in ("postproduction-attestation","producer-save"):return False
            if value.get("origin")=="postproduction-attestation":
                evidence=value.get("evidence")
                if not isinstance(evidence, dict):return False
                if evidence.get("original_producer_sha256")!=ORIGINAL_PRODUCER:return False
                if evidence.get("expected_artifacts")!=value.get("artifacts"):return False
            # Equal letters payload bytes can outlive their own bigram lineage.
            if name == "power" and not current("letters", cache_dir, root, producer_source):return False
            return (value.get("artifacts")==inspect_payload(name,cache_dir)
                    and value.get("recipe")==recipe(name,producer_source)
                    and value.get("dependencies_observed_now")==dependencies(name,cache_dir,root))
    except (OSError,ValueError,KeyError,TypeError,IndexError,OverflowError,EOFError,SyntaxError,
            zipfile.BadZipFile,importlib.metadata.PackageNotFoundError):
        return False
