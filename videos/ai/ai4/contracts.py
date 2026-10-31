"""Small, explicit numerical/reporting contracts for Part 4; no production jobs at import."""
from __future__ import annotations

import hashlib
import json
import math
import platform
import struct
import urllib.request
from datetime import datetime, timezone

import numpy as np


def stopping(values, threshold, cap, *, criterion, greater=False):
    """First observed success, including the last permitted iteration, or an explicit censored result."""
    values = np.asarray(values, dtype=float)
    finite = np.isfinite(values)
    hits = np.flatnonzero(finite & ((values > threshold) if greater else (values < threshold)))
    first = int(hits[0]) if len(hits) else None
    return dict(status="nonfinite" if not finite.all() else ("converged" if first is not None else "capped"),
                first_hit_step=first, iterations=len(values) - 1, cap=int(cap), threshold=float(threshold),
                residual=float(values[-1]), criterion=criterion)


def solver_record(result, residuals):
    return dict(success=bool(result.success), status=int(getattr(result, "status", 0 if result.success else -1)),
                message=str(result.message), iterations=int(getattr(result, "nit", 0)),
                residuals={k: float(v) for k, v in residuals.items()})


def fixed_point(W, u, tol=1e-12, max_iter=2000):
    """Return an iterate and its actual fixed-point residual; cap != convergence."""
    z = np.zeros(len(u))
    for k in range(max_iter):
        z = np.tanh(W @ z + u)
        residual = float(np.max(np.abs(np.tanh(W @ z + u) - z)))
        if not np.isfinite(residual):
            return z, dict(status="nonfinite", iterations=k + 1, cap=max_iter, tolerance=tol, residual=residual)
        if residual < tol:
            return z, dict(status="converged", iterations=k + 1, cap=max_iter, tolerance=tol, residual=residual)
    residual = float(np.max(np.abs(np.tanh(W @ z + u) - z)))
    return z, dict(status="converged" if residual < tol else "capped", iterations=max_iter,
                   cap=max_iter, tolerance=tol, residual=residual)


def solve_summary(records):
    return dict(count=len(records), converged=sum(r["status"] == "converged" for r in records),
                capped=sum(r["status"] == "capped" for r in records),
                nonfinite=sum(r["status"] == "nonfinite" for r in records),
                max_residual=max((r["residual"] for r in records), default=0.0),
                cap=records[0]["cap"] if records else None, tolerance=records[0]["tolerance"] if records else None)


def benchmark_context():
    import os
    import torch
    try:
        from threadpoolctl import threadpool_info
        native_threadpools = threadpool_info()
    except ImportError:
        native_threadpools = dict(status="unavailable", reason="optional threadpoolctl is not installed")
    return dict(scope="Observed local wall time; fixed-order warmed repetitions, not a universal speed bound",
                native_threadpools=native_threadpools,
                platform=platform.platform(), processor=platform.processor(), numpy=np.__version__,
                torch=torch.__version__, torch_threads=torch.get_num_threads(),
                environment={k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")})


MODEL_HEADERS = {
    "gpt2": dict(repo="openai-community/gpt2", revision="607a30d783dfa663caf39e06633721c8d4cfcd7e",
                 files=["model.safetensors"], historical=124_439_808),
    "qwen3_4b": dict(repo="Qwen/Qwen3-4B-Base", revision="906bfd4b4dc7f14ee4320094d8b41684abff8539",
                    files=[f"model-{i:05}-of-00003.safetensors" for i in range(1, 4)], historical=4_022_468_096),
}


def read_range(url, start, end, *, opener=None):
    """Never consume a full weight response if a server ignores the bounded Range."""
    import re
    request = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end - 1}", "Accept-Encoding": "identity"})
    with (opener or urllib.request.urlopen)(request, timeout=30) as response:
        match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", response.headers.get("Content-Range", ""))
        if response.status != 206 or match is None or tuple(map(int, match.groups()[:2])) != (start, end - 1):
            raise ValueError("server did not honor exact header byte range")
        if int(match[3]) < end:
            raise ValueError("invalid Content-Range total")
        raw = response.read(end - start + 1)
        if len(raw) != end - start:
            raise ValueError("short/oversized header response")
        return raw


def bounded_json(url, *, limit=2 * 1024 * 1024, opener=None):
    with (opener or urllib.request.urlopen)(url, timeout=30) as response:
        raw = response.read(limit + 1)
        if len(raw) > limit:
            raise ValueError("metadata size limit exceeded")
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def parameter_headers(model, *, opener=None):
    """Canonical pinned tensor headers, with declared tied-output/buffer exclusions; no weights loaded."""
    spec = MODEL_HEADERS[model]
    base = f"https://huggingface.co/{spec['repo']}/resolve/{spec['revision']}/"
    config, config_sha = bounded_json(base + "config.json", opener=opener)
    tied = config.get("tie_word_embeddings", config.get("model_type") == "gpt2")
    index, index_sha = None, None
    if len(spec["files"]) > 1:
        index, index_sha = bounded_json(base + "model.safetensors.index.json", opener=opener)
        if set(index["weight_map"].values()) != set(spec["files"]):
            raise ValueError("canonical shard manifest mismatch")
    total, seen, excluded, files = 0, set(), [], []
    for filename in spec["files"]:
        prefix = read_range(base + filename, 0, 8, opener=opener)
        length = struct.unpack("<Q", prefix)[0]
        if not 2 <= length <= 8 * 1024 * 1024:
            raise ValueError("unsafe safetensors header length")
        raw = read_range(base + filename, 8, 8 + length, opener=opener)
        header = json.loads(raw)
        for key, tensor in header.items():
            if key == "__metadata__":
                continue
            if key in seen:
                raise ValueError("duplicate tensor across shards")
            seen.add(key)
            shape = tensor["shape"]
            if not isinstance(shape, list) or not all(type(n) is int and n >= 0 for n in shape):
                raise ValueError("invalid tensor shape")
            if index is not None and index["weight_map"].get(key) != filename:
                raise ValueError("header tensor does not match canonical shard index")
            if (model == "gpt2" and (key.endswith(".attn.bias") or key.endswith(".attn.masked_bias"))) or (tied and key == "lm_head.weight"):
                excluded.append(key)
                continue
            total += math.prod(shape)
        files.append(dict(path=filename, header_sha256=hashlib.sha256(raw).hexdigest(), header_bytes=length))
    if index is not None and seen != set(index["weight_map"]):
        raise ValueError("canonical index has missing tensors")
    if total <= 0:
        raise ValueError("empty parameter header set")
    return int(total), dict(source="pinned-safetensors-headers", repo=spec["repo"], revision=spec["revision"],
                            files=files, config_sha256=config_sha, index_sha256=index_sha,
                            tied_weight_policy="declared tied lm_head counted once; GPT2 causal-mask buffers excluded",
                            excluded=excluded, error=None, historical_date=None,
                            observed_utc=datetime.now(timezone.utc).isoformat())


def parameter_counts():
    out, provenance = {}, {}
    for model, spec in MODEL_HEADERS.items():
        try:
            out[model], provenance[model] = parameter_headers(model)
        except Exception as exc:
            out[model] = spec["historical"]
            provenance[model] = dict(source="historical-fallback", repo=spec["repo"], revision=spec["revision"],
                                     files=[], error=f"{type(exc).__name__}: {exc}", historical_date="2026-10-23",
                                     historical_scope="literal retained from original source; not newly measured or independently authenticated",
                                     tied_weight_policy="original unique-parameter convention")
            print(f"  params/{model}: {type(exc).__name__}; retained historical count (not a new measurement)", flush=True)
    return dict(**out, provenance=provenance)
