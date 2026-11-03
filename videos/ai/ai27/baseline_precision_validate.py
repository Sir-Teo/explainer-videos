"""Independent NumPy checks for opt-in streamed baseline precision runs.

No Torch, model or producer imports. Per-topic raw gradients are checked while
alive; later verification checks compact receipts, not discarded gradients.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import numpy as np

KINDS = ("none", "shifted", "shared", "value", "group")
ALGORITHM = "float32 G_r-cG_1 then float64 cosine and squared-length reductions"
PROTOCOL = "ai27-baseline-stream-v2"
SOURCE_PATHS = ("videos/ai/ai27/compute.py", "videos/ai/ai27/post.py",
                "videos/ai/ai27/baseline_precision.py", "videos/ai/ai27/baseline_precision_tools.py",
                "videos/ai/ai27/baseline_precision_validate.py", "explainer/ai/novels.py", "explainer/lm/pocket.py")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def object_digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def safe_run(cache_dir, run_id):
    if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", run_id):
        raise ValueError("Explicit baseline run ID must be 1..64 letters/digits/underscores/hyphens")
    parent = Path(cache_dir) / "baseline-runs"
    path = parent / run_id
    if path.is_symlink() or path.resolve().parent != parent.resolve():
        raise ValueError("Baseline run must be a direct non-symlink child of baseline-runs")
    return path


def close(a, b, *, square=False):
    return math.isfinite(float(a)) and math.isfinite(float(b)) and math.isclose(
        float(a), float(b), abs_tol=1e-10 if square else 5e-6, rel_tol=5e-5)


def independent_topic(gr, g1, constants, *, chunk=65536):
    """FP32 pointwise operations first, chunked independent FP64 Gram reductions."""
    batches = len(gr)
    if batches < 2 or len(g1) != batches or chunk < 1:
        raise ValueError("At least two matched gradient batches are required")
    size = gr[0].size
    for array in (*gr, *g1):
        if array.dtype != np.float32 or array.shape != (size,) or not np.isfinite(array).all():
            raise ValueError("Expected finite FP32 vectors of equal shape")
    metrics, hashes = {}, {}
    for kind in KINDS:
        if len(constants[kind]) != batches or not all(math.isfinite(c) for c in constants[kind]):
            raise ValueError("Invalid baseline constants")
        gram = np.zeros((batches, batches), dtype=np.float64)
        hs = [hashlib.sha256() for _ in range(batches)]
        for start in range(0, size, chunk):
            end = min(start + chunk, size)
            vectors = []
            for b in range(batches):
                # Two separate FP32 ufuncs: no early FP64 promotion or fused operation.
                scaled = np.multiply(np.float32(constants[kind][b]), g1[b][start:end], dtype=np.float32)
                value = np.subtract(gr[b][start:end], scaled, dtype=np.float32)
                if not np.isfinite(value).all():
                    raise ValueError("Nonfinite FP32 affine vector")
                hs[b].update(value.tobytes())
                vectors.append(value.astype(np.float64))
            block = np.stack(vectors)
            gram += block @ block.T
        norms = np.sqrt(np.maximum(np.diag(gram), 0))
        pairs = [float(gram[i, j] / (max(norms[i], 1e-8) * max(norms[j], 1e-8)))
                 for i in range(batches) for j in range(i + 1, batches)]
        squares = [float(x) for x in np.diag(gram)]
        metrics[kind] = {"pairs": pairs, "squares": squares,
                         "cos": math.fsum(pairs) / len(pairs), "sq": math.fsum(squares) / batches}
        hashes[kind] = [h.hexdigest() for h in hs]
    return {"metrics": metrics, "affine_sha256": hashes}


def validate_live(primary, independent):
    if primary["affine_sha256"] != independent["affine_sha256"]:
        raise ValueError("Torch/NumPy FP32 affine bits differ")
    for kind in KINDS:
        p, q = primary["metrics"][kind], independent["metrics"][kind]
        for result in (p, q):
            if (not result["pairs"] or not result["squares"]
                    or any(not math.isfinite(x) or not -1-1e-12 <= x <= 1+1e-12 for x in result["pairs"])
                    or any(not math.isfinite(x) or x < 0 for x in result["squares"])):
                raise ValueError("Invalid cosine/squared-length domain")
        if any(len(result["affine_sha256"][kind]) != len(result["metrics"][kind]["squares"])
               or any(not re.fullmatch(r"[a-f0-9]{64}", h) for h in result["affine_sha256"][kind])
               for result in (primary, independent)):
            raise ValueError("Invalid affine-vector hash binding")
        for key in ("pairs", "squares"):
            if len(p[key]) != len(q[key]) or not all(close(a, b, square=key == "squares")
                                                     for a, b in zip(p[key], q[key])):
                raise ValueError("Independent metric comparison failed: " + kind + "/" + key)
        if not close(p["cos"], q["cos"]) or not close(p["sq"], q["sq"], square=True):
            raise ValueError("Independent topic reduction failed")


def aggregate(original, receipts, key):
    result = dict(original)
    for kind in KINDS:
        cos = [row[key]["metrics"][kind]["cos"] for row in receipts]
        sq = [row[key]["metrics"][kind]["sq"] for row in receipts]
        result[kind + "_cos_by_q"] = cos
        result[kind + "_cos"] = math.fsum(cos) / len(cos)
        result[kind + "_sq"] = math.fsum(sq) / len(sq)
    return result


def verify_run(run_dir, *, allow_synthetic=False, root=None, require_audit=True):
    """Verify sealed receipts; does NOT replay discarded raw gradients."""
    run_dir = Path(run_dir)
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema_version") != 2 or manifest.get("protocol") != PROTOCOL or manifest.get("status") != "complete":
        raise ValueError("Unknown/incomplete baseline protocol")
    if manifest.get("run_kind") != "original-baseline" and not (
            allow_synthetic and manifest.get("run_kind") == "synthetic-control"):
        raise ValueError("Synthetic or unknown baseline run is not renderable")
    if manifest.get("algorithm") != ALGORITHM or manifest.get("validation_mode") != "independent-numpy-live-per-topic":
        raise ValueError("Unrecognized precision algorithm/validation mode")
    root = Path(root) if root is not None else Path(__file__).resolve().parents[3]
    sources = manifest.get("sources", {})
    if set(sources) != set(SOURCE_PATHS) or any(digest(root / path) != sha for path, sha in sources.items()):
        raise ValueError("Source manifest differs from this checkout")
    if manifest.get("retained_gradients") is not False:
        raise ValueError("This streamed protocol does not attest retained raw gradients")
    if not manifest.get("input_pins") or not manifest.get("runtime"):
        raise ValueError("Missing model/runtime provenance")
    runtime = manifest["runtime"]
    if (set(runtime) != {"python", "torch", "numpy", "torch_threads"}
            or any(not isinstance(runtime[k], str) or not runtime[k] for k in ("python", "torch", "numpy"))
            or type(runtime["torch_threads"]) is not int or not 1 <= runtime["torch_threads"] <= 2):
        raise ValueError("Invalid runtime provenance")
    if manifest["run_kind"] == "original-baseline":
        required_inputs = {".cache/novels/base.pt", ".cache/novels/base.json", ".cache/novels/tokenizer.json",
                           ".cache/ai27/sft.pt", ".cache/ai27/rm.pt"}
        if set(manifest["input_pins"]) != required_inputs:
            raise ValueError("Missing/unexpected original model input provenance")
        for pin in manifest["input_pins"].values():
            if (set(pin) != {"bytes", "sha256"} or type(pin["bytes"]) is not int or pin["bytes"] < 1
                    or not isinstance(pin["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", pin["sha256"])):
                raise ValueError("Invalid model input hash/size")
    for rel, sha in manifest["artifacts"].items():
        if rel not in {"baselines.json", "baselines_f64.json"} and not re.fullmatch(r"topics/[0-9]{3}\.json", rel):
            raise ValueError("Unexpected run artifact")
        if (run_dir / rel).is_symlink() or digest(run_dir / rel) != sha:
            raise ValueError("Run artifact hash mismatch: " + rel)
    original = json.loads((run_dir / "baselines.json").read_text())
    candidate = json.loads((run_dir / "baselines_f64.json").read_text())
    if (original.get("kinds") != list(KINDS) or not original.get("topics")
            or original.get("batches", 0) < 2 or original.get("n", 0) < 1):
        raise ValueError("Invalid baseline metadata")
    expected_paths = {"baselines.json", "baselines_f64.json"} | {
        f"topics/{i:03d}.json" for i in range(len(original["topics"]))}
    if set(manifest["artifacts"]) != expected_paths:
        raise ValueError("Missing/extra topic artifact")
    receipts = [json.loads((run_dir / f"topics/{i:03d}.json").read_text()) for i in range(len(original["topics"]))]
    if manifest.get("topic_receipt_count") != len(receipts):
        raise ValueError("Topic count mismatch")
    if manifest["run_kind"] == "original-baseline" and (original["topics"] != ["sea", "river", "ship", "sun", "face", "town"]
            or original["batches"] != 6 or original["n"] != 16 or original["shift"] != 5.0):
        raise ValueError("Fresh original run changed the declared recipe")
    original_comparisons = []
    parameter_order = None
    for i, row in enumerate(receipts):
        if (row.get("schema_version") != 2 or row.get("index") != i or row.get("topic") != original["topics"][i]
                or row.get("batches") != original["batches"] or row.get("n") != original["n"]
                or row.get("live_validation") != "passed" or row.get("raw_unchanged") is not True
                or object_digest(row["sampling"]) != row["sampling_sha256"]):
            raise ValueError("Topic identity/provenance mismatch")
        if parameter_order is None:
            parameter_order = row["parameters"]
        if (manifest["run_kind"] == "original-baseline" and sum(math.prod(p["shape"]) for p in parameter_order) != 6843648):
            raise ValueError("Unexpected original parameter count")
        if row["parameters"] != parameter_order or object_digest(parameter_order) != row["parameter_order_sha256"]:
            raise ValueError("Parameter order changed")
        rewards = [np.array(x["values"], dtype=x["dtype"]) for x in row["rewards"]]
        if len(rewards) != original["batches"] or any(a.shape != (original["n"],) or not np.isfinite(a).all() for a in rewards):
            raise ValueError("Reward shape/values differ")
        if float(np.mean(rewards)) != original["question_mean"][i]:
            raise ValueError("Question reward mean differs from original")
        constants = {"none": [0.] * len(rewards), "shifted": [-original["shift"]] * len(rewards),
                     "shared": [original["shared"]] * len(rewards),
                     "value": [original["question_mean"][i]] * len(rewards),
                     "group": [float(x.mean()) for x in rewards]}
        if row["constants"] != constants:
            raise ValueError("Baseline constants changed")
        if set(row["raw_gradient_sha256"]) != {"G_r", "G_1"} or any(
                len(values) != original["batches"] or any(not re.fullmatch(r"[a-f0-9]{64}", v) for v in values)
                for values in row["raw_gradient_sha256"].values()):
            raise ValueError("Invalid raw-gradient hash binding")
        if len(row["sampling"]) != original["batches"] or any(
                len(batch["output_ids"]) != original["n"] or not batch["prompt_ids"]
                or any(not ids or any(type(token) is not int or token < 0 for token in ids) for ids in batch["output_ids"])
                for batch in row["sampling"]):
            raise ValueError("Invalid sampled token capture")
        if manifest["run_kind"] == "original-baseline" and [b["seed"] for b in row["sampling"]] != [
                30000 + 100 * i + b for b in range(original["batches"])]:
            raise ValueError("Original sampling seeds changed")
        validate_live(row["primary"], row["independent"])
        for kind in KINDS:
            p = row["independent"]["metrics"][kind]
            if len(p["pairs"]) != original["batches"] * (original["batches"] - 1) // 2 or len(p["squares"]) != original["batches"]:
                raise ValueError("Metric shape mismatch")
            if not close(p["cos"], math.fsum(p["pairs"]) / len(p["pairs"])) or not close(
                    p["sq"], math.fsum(p["squares"]) / len(p["squares"]), square=True):
                raise ValueError("Metric aggregation mismatch")
    if float(np.mean(original["question_mean"])) != original["shared"]:
        raise ValueError("Shared reward mean differs")
    for kind in KINDS:
        native_cos = [row["native_fp32"][kind]["cos"] for row in receipts]
        native_sq = [row["native_fp32"][kind]["sq"] for row in receipts]
        if (original[kind + "_cos_by_q"] != native_cos or original[kind + "_cos"] != float(np.mean(native_cos))
                or original[kind + "_sq"] != float(np.mean(native_sq))):
            raise ValueError("Original FP32 result did not match its captured native values")
        original_comparisons.append({"kind": kind,
            "cos_passed": all(close(a, row["independent"]["metrics"][kind]["cos"]) for a, row in zip(native_cos, receipts)),
            "sq_passed": all(close(a, row["independent"]["metrics"][kind]["sq"], square=True) for a, row in zip(native_sq, receipts))})
    independent = aggregate(original, receipts, "independent")
    metrics = {kind + suffix for kind in KINDS for suffix in ("_cos", "_cos_by_q", "_sq")}
    for key, value in original.items():
        if key not in metrics and candidate.get(key) != value:
            raise ValueError("Candidate changed original metadata")
    original_sha = digest(run_dir / "baselines.json")
    if (candidate.get("schema_version") != 2 or candidate.get("algorithm") != ALGORITHM
            or candidate.get("gradient_dtype") != "float32" or candidate.get("reduction_dtype") != "float64"
            or candidate.get("original_cache_sha256") != original_sha):
        raise ValueError("Candidate protocol/hash mismatch")
    for kind in KINDS:
        for suffix in ("_cos", "_cos_by_q", "_sq"):
            key = kind + suffix
            a, b = candidate[key], independent[key]
            if suffix == "_cos_by_q":
                if len(a) != len(b) or not all(close(x, y) for x, y in zip(a, b)):
                    raise ValueError("Candidate question metrics differ")
            elif not close(a, b, square=suffix == "_sq"):
                raise ValueError("Candidate metric differs")
        if not all(-1 <= x <= 1 for x in [candidate[kind + "_cos"], *candidate[kind + "_cos_by_q"]]) or candidate[kind + "_sq"] < 0:
            raise ValueError("Candidate metric outside domain")
    binding = {"schema_version": 2, "protocol": PROTOCOL, "status": "passed",
               "manifest_sha256": digest(manifest_path), "original_sha256": original_sha,
               "candidate_sha256": digest(run_dir / "baselines_f64.json"),
               "validation_mode": "independent-numpy-live-per-topic",
               "later_raw_gradient_replay_available": False,
               "original_fp32_comparison_status": "passed" if all(c["cos_passed"] and c["sq_passed"] for c in original_comparisons) else "failed",
               "original_fp32_comparisons": original_comparisons}
    if require_audit:
        audit = json.loads((run_dir / "baselines_f64.audit.json").read_text())
        if any(audit.get(k) != v for k, v in binding.items()):
            raise ValueError("Audit missing/failed/mismatched")
    return candidate, binding


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--synthetic-control", action="store_true", help="Verify tests only; never enables the scene reader")
    args = parser.parse_args()
    _, binding = verify_run(args.run_dir, allow_synthetic=args.synthetic_control)
    print(json.dumps(binding, indent=2))


if __name__ == "__main__":
    main()
