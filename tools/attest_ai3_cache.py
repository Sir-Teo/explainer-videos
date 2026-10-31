#!/usr/bin/env python3
"""Explicitly attest the eight completed, formerly unversioned Part 3 caches.

Requires exact expected artifacts, frozen producer and successful generation logs.
Never computes, rewrites payloads, or silently upgrades arbitrary legacy caches.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import json
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from explainer.cache_lock import cache_lock
from videos.ai.ai3 import cache_integrity as integrity


def attest(cache_dir, root, producer_source, completion_receipt, expected_artifacts,
           main_log, independent_log):
    cache_dir, root = Path(cache_dir), Path(root)
    producer_source = Path(producer_source)
    frozen_hash = integrity.digest(producer_source)
    integrity._expect(frozen_hash == integrity.ORIGINAL_PRODUCER, "not the declared frozen producer")
    completion_receipt, expected_artifacts = Path(completion_receipt), Path(expected_artifacts)
    completion = json.loads(completion_receipt.read_text())
    expected = json.loads(expected_artifacts.read_text())
    integrity._expect(completion["producer_sha256"] == frozen_hash == expected["producer_sha256"], "producer evidence mismatch")
    logs = {"main": Path(main_log), "independent": Path(independent_log)}
    log_bytes = {k: p.read_bytes() for k, p in logs.items()}
    log_text = {k: b.decode("utf-8") for k, b in log_bytes.items()}
    # Predeclare and validate every expectation before publishing any sidecar.
    evidence = {}
    current_source = root / "videos/ai/ai3/compute.py"
    with ExitStack() as stack:
        for name in sorted(integrity.ITEMS):
            stack.enter_context(cache_lock(cache_dir / f"{name}.json"))
        before = {}
        for name in sorted(integrity.ITEMS):
            artifacts = integrity.inspect_payload(name, cache_dir)
            pair = {key: expected["items"][name][key] for key in ("json_sha256", "npz_sha256")}
            integrity._expect(artifacts == pair, f"{name}: expected artifact mismatch")
            integrity._expect(pair["json_sha256"] == completion["cache_json_sha256"][name], f"{name}: completion hash mismatch")
            integrity._expect(integrity.recipe(name, current_source) == integrity.recipe(name, producer_source), f"{name}: current producer algorithm drift")
            integrity.dependencies(name, cache_dir, root)  # ensure every required dependency resolves before writes
            which = "independent" if name == "highdim" else "main"
            lines = log_text[which].splitlines()
            start = next((i for i, line in enumerate(lines) if line.strip() == f"compute {name} ..."), None)
            end = next((i for i, line in enumerate(lines) if line.strip().startswith(f"done    {name} in ")), None)
            integrity._expect(start is not None and end is not None and start < end, f"{name}: successful generation log missing")
            evidence[name] = {"original_producer_sha256": frozen_hash,
                "expected_artifacts": pair,
                "completion_receipt_sha256": integrity.digest(completion_receipt),
                "expected_artifacts_receipt_sha256": integrity.digest(expected_artifacts),
                "generation_log": {"sha256": hashlib.sha256(log_bytes[which]).hexdigest(),
                    "start_line": start + 1, "start_text": lines[start], "end_line": end + 1, "end_text": lines[end]},
                "origin_scope": "Explicit later attestation matching frozen producer and published completion/run evidence; not producer-written generation metadata.",
                "consumed_input_gap": "Original consumed dependency hashes were not recorded by this producer. Current dependency observations cannot establish those historical bytes."}
            for suffix in (".json", ".npz"):
                path = cache_dir / f"{name}{suffix}"
                before[str(path)] = None if not path.exists() else {"sha256": integrity.digest(path), "size": path.stat().st_size, "mtime_ns": path.stat().st_mtime_ns}
        published = {}
        for name in sorted(integrity.ITEMS):
            integrity.publish(name, cache_dir, root, current_source, origin="postproduction-attestation", evidence=evidence[name])
            p = integrity.sidecar_path(cache_dir, name)
            published[name] = {"path": str(p), "sha256": integrity.digest(p)}
        after = {}
        for key in before:
            path = Path(key)
            after[key] = None if not path.exists() else {"sha256": integrity.digest(path), "size": path.stat().st_size, "mtime_ns": path.stat().st_mtime_ns}
        integrity._expect(before == after, "payload changed during attestation")
    return {"observed_utc": datetime.now(timezone.utc).isoformat(), "origin": "postproduction-attestation",
            "sidecars": published, "payloads_before": before, "payloads_after": after,
            "payload_bytes_sizes_mtimes_unchanged": True, "producer_guard_activation": "not performed by migration tool",
            "consumption_scope": "Current dependency observations and later source/run evidence; original consumed-input lineage not retroactively asserted."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=ROOT / ".cache/ai3")
    parser.add_argument("--root", type=Path, default=ROOT)
    for flag in ("producer-source", "completion-receipt", "expected-artifacts", "main-log", "independent-log", "output-receipt"):
        parser.add_argument("--" + flag, type=Path, required=True)
    args = parser.parse_args()
    receipt = attest(args.cache_dir, args.root, args.producer_source, args.completion_receipt,
                     args.expected_artifacts, args.main_log, args.independent_log)
    args.output_receipt.parent.mkdir(parents=True, exist_ok=True)
    args.output_receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print("Attested eight items; payload bytes and mtimes preserved; no producer guard changed or computation invoked.")


if __name__ == "__main__":
    main()
