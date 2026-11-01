"""Part 5 decoding identities and metric checks; no model/producer imports.

The v3 judge preserves the prompt/continuation token boundary. Its nats per
Unicode character are a new measurement convention, not the historical v2 run.
"""
from __future__ import annotations

import hashlib
from importlib.metadata import version
import json
import math
import os
from pathlib import Path
import time

METRIC_VERSION = 3
GPT2_REVISION = "607a30d783dfa663caf39e06633721c8d4cfcd7e"
GPT2_FILES = ("config.json", "model.safetensors", "tokenizer.json", "tokenizer_config.json",
              "vocab.json", "merges.txt", "generation_config.json")
METRIC = dict(version=METRIC_VERSION, unit="nats per continuation Unicode character",
              tokenization="encode prompt and continuation separately without added special tokens; concatenate IDs",
              scoring="all continuation tokens conditioned on prompt; reject empty/over-context inputs",
              diversity="distinct generator-token bigrams pooled within each prompt",
              repetition="fraction of generator-token 4-grams seen earlier in the same continuation")


def file_identity(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Decoding prerequisite missing: {path}; prepare it explicitly before computing Part 5")
    before = path.stat()
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    after = path.stat()
    if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"Decoding prerequisite changed while fingerprinting: {path}")
    return dict(bytes=after.st_size, sha256=h.hexdigest())


def snapshot_dir(hub_dir=None):
    if hub_dir is None:
        hub_dir = os.environ.get("HF_HUB_CACHE") or os.environ.get("HUGGINGFACE_HUB_CACHE")
        if hub_dir is None:
            hub_dir = Path(os.environ.get("HF_HOME", Path.home() / ".cache/huggingface")) / "hub"
    return Path(hub_dir) / "models--openai-community--gpt2" / "snapshots" / GPT2_REVISION


def judge_identity(hub_dir=None):
    """Pinned public GPT-2 assets only, also usable by the temperature recipe."""
    hf = snapshot_dir(hub_dir)
    return dict(repository="openai-community/gpt2", revision=GPT2_REVISION,
                files={p: file_identity(hf / p) for p in GPT2_FILES})


def cache_identity(repo_root, config, hub_dir=None):
    """Pure filesystem identity API for SchemaCache, before tokenizer/model imports.

    ``config`` is the decoder's full public experiment constants. Missing inputs
    raise, never train/rebuild/download. The root cache can include this JSON in
    its item recipe and compare it before reusing completed results.
    """
    root = Path(repo_root)
    paths = [".cache/novels/base.pt", ".cache/novels/base.json", ".cache/novels/tokenizer.json",
             ".cache/novels/train.npy", ".cache/novels/valid.npy", ".cache/ai1/train.txt", ".cache/ai1/valid.txt",
             "videos/ai/ai5/decoding.py", "videos/ai/ai5/decoding_contract.py", "explainer/ai/novels.py",
             "explainer/lm/pocket.py"]
    files = {p: file_identity(root / p) for p in paths}
    base = json.loads((root / ".cache/novels/base.json").read_text())
    run = base.get("run", {})
    expected = dict(d=256, layers=6, heads=8, seq=256, vocab=4096)
    model = run.get("model", {})
    if (base.get("steps") != 2929 or base.get("diverged") is not False
            or any(model.get(k) != v for k, v in expected.items())
            or run.get("tokens") != 24_000_000 or run.get("batch") != 32):
        raise ValueError("Decoding needs the completed 2929-step novels base with its reviewed configuration")
    packages = {p: version(p) for p in ("torch", "transformers", "tokenizers", "numpy")}
    return dict(schema_version=METRIC_VERSION, metric=json.loads(json.dumps(METRIC)),
                config=json.loads(json.dumps(config)), files=files,
                judge=judge_identity(hub_dir),
                runtime=packages)


def prompt_identity(ids, texts):
    value = json.dumps(dict(ids=[[int(v) for v in row] for row in ids], texts=list(texts)),
                       ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(value.encode()).hexdigest()


def valid_piece(key, value, prompts):
    if not isinstance(value, dict):
        return False
    def finite(x, low=0, high=math.inf):
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and low <= x <= high
    if not finite(value.get("nll")) or not finite(value.get("rep"), 0, 1):
        return False
    if key == "human":
        return isinstance(value.get("text"), str) and bool(value["text"])
    greedy = key == "greedy0.0"
    if not (value.get("div") is None if greedy else finite(value.get("div"), 0, 1)):
        return False
    return (finite(value.get("kept"), 1)
            and isinstance(value.get("nll_prompt"), list) and len(value["nll_prompt"]) == prompts
            and all(finite(x) for x in value["nll_prompt"])
            and isinstance(value.get("examples"), list) and bool(value["examples"])
            and isinstance(value.get("ex_prompt"), list) and bool(value["ex_prompt"])
            and all(isinstance(x, str) and x for x in value["examples"] + value["ex_prompt"]))


def checked_partial(cache, contract, keys, prompts):
    """Caller holds decoding item lock; preserve incompatible/invalid old bytes."""
    path = cache.dir / "decoding.partial.json"
    normalized = json.loads(json.dumps(contract))
    if path.exists():
        raw = path.read_bytes()
        try:
            data = json.loads(raw)
            okay = (isinstance(data, dict) and data.get("params") == normalized
                    and isinstance(data.get("done"), dict)
                    and all(k in {"human", *keys} and valid_piece(k, v, prompts)
                            for k, v in data["done"].items()))
        except (ValueError, TypeError):
            okay = False
        if not okay:
            dest = path.with_name(f"decoding.partial.stale-v3-{hashlib.sha256(raw).hexdigest()[:16]}-{time.time_ns()}.json")
            path.replace(dest)
            print(f"  preserved incompatible decoding partial: {dest}", flush=True)
    return cache.partial("decoding", normalized)


def comparison(rows, kinds, target=0.85):
    """Finite interpolation only within observed ranges, with honest cohort scope."""
    import numpy as np
    pts = {}
    for kind in kinds:
        points = sorted((float(v["div"]), float(v["nll"])) for k, v in rows if k == kind)
        if not points or not all(math.isfinite(a) and math.isfinite(b) and 0 <= a <= 1 and b >= 0 for a, b in points):
            raise ValueError(f"Invalid decoding comparison points: {kind}")
        pts[kind] = points
    at = {k: float(np.interp(target, [p[0] for p in ps], [p[1] for p in ps]))
          for k, ps in pts.items() if ps[0][0] <= target <= ps[-1][0]}
    return dict(at=at, all_rules=len(at) == len(pts), best=min(at, key=at.get) if at else None,
                spread=max(at.values())-min(at.values()) if at else None)



def judge_verdict(greedy, sampled):
    values = [float(greedy), *map(float, sampled)]
    if len(values) < 2 or not all(math.isfinite(v) and v >= 0 for v in values):
        raise ValueError("Judge verdict requires finite nonnegative measured surprises")
    best = min(values[1:])
    if greedy < best:
        return "Greedy decoding has the lowest surprise in this run"
    if greedy == best:
        return "Greedy decoding ties the lowest surprise in this run"
    return "A sampled setting has lower surprise than greedy decoding in this run"
