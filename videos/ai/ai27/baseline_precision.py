"""Read the independently accepted precision derivative of a baseline experiment.

The original ``baselines.json`` remains unchanged. This reader never generates
experiments or falls back to an unreviewed original/candidate.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


def _load_legacy_baseline_metrics(cache_dir: Path) -> dict:
    """Require a passing audit bound to both the original and FP64 derivative."""
    original_path = cache_dir / "baselines.json"
    candidate_path = cache_dir / "baselines_f64.json"
    audit_path = cache_dir / "baselines_f64.audit.json"
    for path in (original_path, candidate_path, audit_path):
        if not path.is_file():
            raise FileNotFoundError(
                f"{path} missing; restore the reviewed baseline precision bundle "
                "or derive and independently audit a new candidate before rendering."
            )
    original_bytes = original_path.read_bytes()
    candidate_bytes = candidate_path.read_bytes()
    audit = json.loads(audit_path.read_text())
    candidate = json.loads(candidate_bytes)
    original_sha = hashlib.sha256(original_bytes).hexdigest()
    candidate_sha = hashlib.sha256(candidate_bytes).hexdigest()
    checks = audit.get("checks", [])
    required_checks = {f"{kind}_{suffix}" for kind in ("none", "shifted", "shared", "value", "group")
                       for suffix in ("cos", "cos_by_q", "sq")}
    required_checks.update({"original_gate_still_failed", "native_replay_exact", "pointwise_bits_exact",
                            "original_baseline_unchanged_after_replay",
                            "original_failed_gate_unchanged_after_replay"})
    check_names = {check.get("name") for check in checks}
    if (audit.get("case") != "baselines_f64" or audit.get("status") != "passed" or not checks
            or not required_checks.issubset(check_names)
            or not all(check.get("passed") is True for check in checks)
            or audit.get("original_sha256") != original_sha
            or audit.get("candidate_sha256") != candidate_sha
            or candidate.get("original_cache_sha256") != original_sha
            or candidate.get("gradient_dtype") != "float32"
            or candidate.get("reduction_dtype") != "float64"
            or candidate.get("algorithm") != "float32 G_r-cG_1 then float64 cosine and squared-length reductions"
            or not audit.get("failed_report_sha256")
            or audit["failed_report_sha256"] != candidate.get("original_failed_gate_sha256")):
        raise ValueError("Baseline precision audit is absent, failed, or belongs to different inputs")
    original = json.loads(original_bytes)
    metric_keys = {f"{kind}_{suffix}" for kind in original["kinds"]
                   for suffix in ("cos", "cos_by_q", "sq")}
    for key, value in original.items():
        if key not in metric_keys and candidate.get(key) != value:
            raise ValueError(f"Baseline precision derivative changed non-metric input {key!r}")
    for kind in original["kinds"]:
        cos = candidate[f"{kind}_cos"]
        by_q = candidate[f"{kind}_cos_by_q"]
        square = candidate[f"{kind}_sq"]
        if (len(by_q) != len(original["topics"])
                or not all(math.isfinite(value) and -1 <= value <= 1 for value in [cos, *by_q])
                or not math.isfinite(square) or square < 0):
            raise ValueError(f"Invalid baseline precision metrics for {kind!r}")
    return candidate


def load_baseline_metrics(cache_dir: Path, *, run_id: str | None = None) -> dict:
    """Legacy v1 by default; select a verified v2 run explicitly, never fall back."""
    import os
    selected = os.environ.get("AI27_BASELINE_RUN") if run_id is None else run_id
    if selected is None:
        return _load_legacy_baseline_metrics(cache_dir)
    from .baseline_precision_validate import safe_run, verify_run
    result, _ = verify_run(safe_run(cache_dir, selected))
    return result
