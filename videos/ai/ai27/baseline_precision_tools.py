"""Opt-in streamed original-baseline capture, FP64 derivation and live audit.

    AI27_THREADS=1 python -m videos.ai.ai27.baseline_precision_tools run --run-id NAME

Requires existing models/tokenizer; never trains or regenerates prerequisites.
Every run is new and non-overwriting. Raw gradients are discarded after each
independent topic check; later verification checks compact receipts only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import sys
import time
import numpy as np
import torch
from torch.nn import functional as F
from .baseline_precision_validate import (ALGORITHM, KINDS, PROTOCOL, SOURCE_PATHS, aggregate,
                                         canonical, digest, independent_topic, object_digest,
                                         safe_run, validate_live, verify_run)

INPUT_PATHS = (".cache/novels/base.pt", ".cache/novels/base.json", ".cache/novels/tokenizer.json",
               ".cache/ai27/sft.pt", ".cache/ai27/rm.pt")


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation preserves failed/incomplete runs and every old artifact.
    with path.open("x") as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + "\n")


def array_hash(array):
    return hashlib.sha256(array.tobytes()).hexdigest()


def torch_metrics(gr, g1, constants):
    result = {"metrics": {}, "affine_sha256": {}}
    with torch.no_grad():
        for kind in KINDS:
            vectors, hashes = [], []
            for b, c in enumerate(constants[kind]):
                value = torch.from_numpy(np.array(gr[b], copy=True)) - c * torch.from_numpy(np.array(g1[b], copy=True))
                if value.dtype != torch.float32 or not torch.isfinite(value).all():
                    raise ValueError("Expected finite FP32 affine vector")
                hashes.append(array_hash(value.numpy()))
                vectors.append(value.to(torch.float64))
            pairs = [float(F.cosine_similarity(vectors[i], vectors[j], dim=0, eps=1e-8))
                     for i in range(len(vectors)) for j in range(i + 1, len(vectors))]
            squares = [float(v @ v) for v in vectors]
            result["metrics"][kind] = {"pairs": pairs, "squares": squares,
                                       "cos": math.fsum(pairs) / len(pairs), "sq": math.fsum(squares) / len(squares)}
            result["affine_sha256"][kind] = hashes
    return result


class StreamRun:
    """Consumes read-only topic views synchronously; retains no gradient arrays."""
    def __init__(self, run_dir, *, root, input_pins, run_kind="original-baseline"):
        if run_kind not in {"original-baseline", "synthetic-control"}:
            raise ValueError("Unknown run kind")
        self.path, self.root = Path(run_dir), Path(root)
        self.path.mkdir(parents=True, exist_ok=False)
        self.sources = {path: digest(self.root / path) for path in SOURCE_PATHS}
        self.input_pins = dict(input_pins)
        self.run_kind = run_kind
        self.artifacts, self.rows = {}, []
        self.started = time.monotonic()
        write_new(self.path / "started.json", {"schema_version": 2, "protocol": PROTOCOL, "run_kind": run_kind,
                                             "status": "incomplete", "input_pins": self.input_pins,
                                             "sources": self.sources})

    def __call__(self, event):
        torch_rng = torch.get_rng_state().clone()
        numpy_rng = np.random.get_state()
        python_rng = random.getstate()
        index = len(self.rows)
        if event["index"] != index:
            raise ValueError("Topic callback skipped/repeated/reordered")
        gr, g1 = event["G_r"], event["G_1"]
        if len(gr) != event["batches"] or len(event["samples"]) != event["batches"]:
            raise ValueError("Topic batch shape differs")
        count = sum(math.prod(p["shape"]) for p in event["parameters"])
        if self.run_kind == "original-baseline" and (count != 6843648 or event["batches"] != 6 or event["n"] != 16):
            raise ValueError("Original baseline protocol is six batches of sixteen at 6843648 parameters")
        if any(a.dtype != np.float32 or a.shape != (count,) or a.flags.writeable for a in (*gr, *g1)):
            raise ValueError("Capture requires detached read-only FP32 vectors")
        raw_before = {"G_r": [array_hash(a) for a in gr], "G_1": [array_hash(a) for a in g1]}
        primary = torch_metrics(gr, g1, event["constants"])
        independent = independent_topic(gr, g1, event["constants"])
        validate_live(primary, independent)
        raw_after = {"G_r": [array_hash(a) for a in gr], "G_1": [array_hash(a) for a in g1]}
        if raw_before != raw_after:
            raise ValueError("Read-only captured gradients changed")
        row = {"schema_version": 2, "index": index, "topic": event["topic"], "batches": event["batches"],
               "n": event["n"], "parameters": event["parameters"],
               "parameter_order_sha256": object_digest(event["parameters"]),
               "sampling": event["samples"], "sampling_sha256": object_digest(event["samples"]),
               "rewards": [{"dtype": str(a.dtype), "values": a.tolist()} for a in event["rewards"]],
               "constants": event["constants"], "raw_gradient_sha256": raw_before,
               "native_fp32": event["native"], "primary": primary, "independent": independent,
               "live_validation": "passed", "raw_unchanged": True}
        rel = f"topics/{index:03d}.json"
        write_new(self.path / rel, row)
        self.artifacts[rel] = digest(self.path / rel)
        if (not torch.equal(torch_rng, torch.get_rng_state())
                or python_rng != random.getstate()
                or any(not np.array_equal(a, b) for a, b in zip(numpy_rng, np.random.get_state()))):
            raise ValueError("Capture/derivation changed RNG state")
        self.rows.append(row)  # compact metrics + token/reward data only; no gradient references

    def finish(self, original):
        if [r["topic"] for r in self.rows] != original["topics"] or not self.rows:
            raise ValueError("Incomplete topic coverage")
        if self.run_kind == "original-baseline" and len(self.rows) != 6:
            raise ValueError("Original recipe requires six topics")
        if any(digest(self.root / p) != h for p, h in self.sources.items()):
            raise ValueError("Sources changed during run")
        candidate = aggregate(original, self.rows, "primary")
        candidate.update(schema_version=2, algorithm=ALGORITHM, gradient_dtype="float32", reduction_dtype="float64")
        write_new(self.path / "baselines.json", original)
        candidate["original_cache_sha256"] = digest(self.path / "baselines.json")
        write_new(self.path / "baselines_f64.json", candidate)
        for name in ("baselines.json", "baselines_f64.json"):
            self.artifacts[name] = digest(self.path / name)
        manifest = {"schema_version": 2, "protocol": PROTOCOL, "status": "complete", "run_kind": self.run_kind,
                    "algorithm": ALGORITHM, "validation_mode": "independent-numpy-live-per-topic",
                    "retained_gradients": False, "sources": self.sources, "input_pins": self.input_pins,
                    "runtime": {"python": platform.python_version(), "torch": torch.__version__,
                                "numpy": np.__version__, "torch_threads": torch.get_num_threads()},
                    "topic_receipt_count": len(self.rows), "artifacts": self.artifacts,
                    "elapsed_seconds": time.monotonic() - self.started}
        write_new(self.path / "manifest.json", manifest)
        _, binding = verify_run(self.path, root=self.root, allow_synthetic=self.run_kind == "synthetic-control",
                                require_audit=False)
        # Audit is the LAST completion marker. Failed/partial runs remain unrenderable.
        write_new(self.path / "baselines_f64.audit.json", binding)
        verify_run(self.path, root=self.root, allow_synthetic=self.run_kind == "synthetic-control")
        return candidate


def prerequisites(root):
    """Check before importing the producer, whose helpers can otherwise train."""
    pins = {}
    for rel in INPUT_PATHS:
        p = Path(root) / rel
        if not p.is_file():
            raise FileNotFoundError(f"Existing prerequisite missing: {p}; no automatic generation is allowed")
        pins[rel] = {"bytes": p.stat().st_size, "sha256": digest(p)}
    return pins


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["run"])
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    output = safe_run(root / ".cache/ai27", args.run_id)
    if output.exists():
        raise FileExistsError("Refusing to overwrite existing/failed run")
    inputs = prerequisites(root)
    threads = int(os.environ.get("AI27_THREADS", "1"))
    if not 1 <= threads <= 2:
        raise ValueError("Precision runner permits one or two Torch threads")
    torch.set_num_threads(threads)
    torch.set_num_interop_threads(1)
    from . import compute
    # Recheck at every loader boundary. Missing prerequisites may never trigger training.
    original_base, original_tok = compute.N.load_base, compute.N.tokenizer
    original_train, original_texts = compute.N.train_base, compute.N._texts
    metadata = {rel: ((root / rel).stat().st_size, (root / rel).stat().st_mtime_ns) for rel in INPUT_PATHS}
    def guarded(fn):
        def call(*a, **kw):
            if any(not (root / rel).is_file() or ((root / rel).stat().st_size, (root / rel).stat().st_mtime_ns) != sig
                   for rel, sig in metadata.items()):
                raise ValueError("Prerequisite input missing/changed")
            return fn(*a, **kw)
        return call
    def forbidden(*a, **kw):
        raise RuntimeError("Precision capture forbids prerequisite generation or training")
    compute.N.train_base, compute.N._texts = forbidden, forbidden
    compute.N.load_base, compute.N.tokenizer = guarded(original_base), guarded(original_tok)
    try:
        run = StreamRun(output, root=root, input_pins=inputs)
        result = compute.compute_baselines(observer=run)
        if prerequisites(root) != inputs:
            raise ValueError("Prerequisites changed during capture")
        run.finish(result)
        print(json.dumps({"status": "passed", "run": str(output), "select": "AI27_BASELINE_RUN=" + args.run_id}))
    finally:
        compute.N.load_base, compute.N.tokenizer = original_base, original_tok
        compute.N.train_base, compute.N._texts = original_train, original_texts


if __name__ == "__main__":
    main()
