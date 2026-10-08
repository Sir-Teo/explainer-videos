"""Download and freeze the real data behind "Inside the Open Frontier".

    python -m videos.open_models.fetch              # download everything, rebuild data.json
    python -m videos.open_models.fetch --offline    # rebuild data.json from the cached raw files

What is fetched (all public, no login):

* Artificial Analysis, ``/models/open-source``: the Intelligence Index of every
  open-weights model (and the open-vs-proprietary progress timeline embedded in
  the same page).  This is what picks the three models: the top three open-weights
  models by the index on ``AS_OF``.
* Hugging Face, for each of the three models: ``config.json``, the safetensors
  index, and the JSON *header* of every weight shard.  A safetensors file starts
  with an 8-byte length and a JSON table of every tensor's name, dtype, shape and
  byte offsets, so HTTP range requests give the exact shape of all ~775,000
  tensors without downloading the 1-3 TB of weights.
* A handful of small tensors read straight out of the shards with range requests
  (a few MB in total): MiMo's learned attention-sink logits, every model's router
  balancing biases, Kimi K3's Kimi-Delta-Attention decay parameters and
  attention-residual pseudo-queries, and one 32-number block of 4-bit expert
  weights from Kimi K3 and from MiMo.

Raw downloads are cached in ``.cache/open_models/raw``; the compact ``data.json``
next to this file is committed, so the video renders offline.  Scenes never
download anything.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import struct
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW = Path(os.environ.get("EXPLAINER_CACHE", ROOT / ".cache")) / "open_models" / "raw"
OUT = Path(__file__).with_name("data.json")

AS_OF = dt.date(2026, 10, 8)
UA = "explainer-videos/0.1 (+https://github.com/sir-teo/explainer-videos)"
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
AA_OPEN = "https://artificialanalysis.ai/models/open-source"
HF = "https://huggingface.co"

# key -> (Hugging Face repo, name on the Artificial Analysis leaderboard)
MODELS = {
    "mimo": ("XiaomiMiMo/MiMo-V2.6-Pro-RL", "MiMo-V2.6-Pro"),
    "glm": ("zai-org/GLM-5.3", "GLM-5.3 (Max)"),
    "kimi": ("moonshotai/Kimi-K3", "Kimi K3 (Max)"),
}


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def http_get(url: str, rng: tuple[int, int] | None = None, ua: str = UA, tries: int = 5) -> bytes:
    headers = {"User-Agent": ua}
    if rng is not None:
        headers["Range"] = f"bytes={rng[0]}-{rng[1]}"
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as r:
                body = r.read()
            if rng is not None and len(body) != rng[1] - rng[0] + 1:
                raise IOError(f"short range read: {len(body)} bytes")
            return body
        except Exception as e:  # noqa: BLE001 (network: retry with backoff)
            if k == tries - 1:
                raise
            print(f"  retry {k + 1} {url} ({e})", flush=True)
            time.sleep(2 ** (k + 1))
    raise AssertionError


def cached(path: Path, fetch, offline: bool) -> bytes:
    if path.exists():
        return path.read_bytes()
    if offline:
        sys.exit(f"--offline but {path} is not cached")
    data = fetch()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)
    return data


# ---------------------------------------------------------------------------
# Artificial Analysis
# ---------------------------------------------------------------------------
def _json_array_after(s: str, key: str) -> list:
    """Bracket-match the JSON array that follows ``"key":`` in the page's RSC payload."""
    i = s.index(f'"{key}":[') + len(key) + 3
    depth, j = 0, i
    for j in range(i, len(s)):
        c = s[j]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
    return json.loads(s[i:j + 1])


def leaderboard(offline: bool) -> dict:
    raw = cached(RAW / "aa_open_source.html", lambda: http_get(AA_OPEN, ua=BROWSER_UA), offline).decode("utf-8", "ignore")
    s = raw.replace('\\"', '"').replace("\\\\", "\\")
    version = re.search(r"Intelligence Index (v\d+\.\d+(?:\.\d+)?) incorporates (\d+) evaluations: ([^<]+?)</", s)
    open_models = _json_array_after(s, "initialModels")
    rows = []
    for m in open_models:
        if m.get("intelligenceIndex") is None:
            continue
        rows.append({
            "name": m["name"], "creator": m["creator"]["name"], "score": round(m["intelligenceIndex"], 2),
            "release": m.get("releaseDate"), "params_b": m.get("parameters"),
            "active_b": m.get("inferenceParametersActiveBillions"), "context": m.get("contextWindowTokens"),
            "weights": m.get("modelWeightsSourceUrl"), "reasoning": m.get("isReasoning"),
        })
    rows.sort(key=lambda r: -r["score"])
    # The "Open Source Progress" chart: every model with a release date and an open/proprietary label.
    progress = []
    i = s.index('"anchor":{"id":"#open-source-progress"}')
    for m in _json_array_after(s[i:], "models"):
        if m.get("intelligenceIndex") is None or not m.get("releaseDate"):
            continue
        progress.append({"name": m["shortName"], "release": m["releaseDate"], "score": round(m["intelligenceIndex"], 2),
                         "open": m["openSourceCategorization"] != "proprietary"})
    progress.sort(key=lambda r: r["release"])
    evals = [e.strip() for e in html.unescape(version.group(3)).split(",")] if version else []
    return {"source": AA_OPEN, "version": version.group(1) if version else None, "evaluations": evals,
            "open": rows, "progress": progress}


# ---------------------------------------------------------------------------
# Hugging Face: configs, shard headers, small tensors
# ---------------------------------------------------------------------------
def repo_dir(repo: str) -> Path:
    return RAW / repo.replace("/", "__")


def hf_file(repo: str, name: str, offline: bool) -> bytes:
    return cached(repo_dir(repo) / name.replace("/", "__"), lambda: http_get(f"{HF}/{repo}/resolve/main/{name}"), offline)


def shard_header(repo: str, shard: str, offline: bool) -> dict:
    url = f"{HF}/{repo}/resolve/main/{shard}"

    def fetch():
        n = struct.unpack("<Q", http_get(url, (0, 7)))[0]
        hdr = http_get(url, (8, 8 + n - 1))
        return json.dumps({"n": n, "header": json.loads(hdr)}).encode()

    return json.loads(cached(repo_dir(repo) / "headers" / f"{shard}.json", fetch, offline))


class Weights:
    """Lazy view of a sharded safetensors checkpoint on the Hub."""

    def __init__(self, repo: str, offline: bool):
        self.repo, self.offline = repo, offline
        self.index = json.loads(hf_file(repo, "model.safetensors.index.json", offline))["weight_map"]
        shards = sorted(set(self.index.values()))
        with ThreadPoolExecutor(8) as pool:
            heads = list(pool.map(lambda sh: shard_header(repo, sh, offline), shards))
        self.headers = dict(zip(shards, heads))
        self.tensors = {}
        for sh, h in self.headers.items():
            for name, meta in h["header"].items():
                if name != "__metadata__":
                    self.tensors[name] = dict(meta, shard=sh)

    def read(self, name: str, rows: tuple[int, int] | None = None) -> np.ndarray:
        """Read a whole tensor (or a slice of leading rows) with one range request."""
        meta = self.tensors[name]
        sh = meta["shard"]
        base = 8 + self.headers[sh]["n"]
        a, b = meta["data_offsets"]
        shape = list(meta["shape"])
        itemsize = {"F32": 4, "BF16": 2, "F8_E4M3": 1, "U8": 1}[meta["dtype"]]
        if rows is not None:
            row_bytes = int(np.prod(shape[1:])) * itemsize
            a, b = a + rows[0] * row_bytes, a + rows[1] * row_bytes
            shape[0] = rows[1] - rows[0]
        key = f"{name}" + (f"@{rows[0]}-{rows[1]}" if rows else "")
        raw = cached(repo_dir(self.repo) / "tensors" / f"{key}.bin",
                     lambda: http_get(f"{HF}/{self.repo}/resolve/main/{sh}", (base + a, base + b - 1)), self.offline)
        dtype = meta["dtype"]
        if dtype == "F32":
            arr = np.frombuffer(raw, "<f4")
        elif dtype == "BF16":
            arr = (np.frombuffer(raw, "<u2").astype(np.uint32) << 16).view(np.float32)
        else:
            arr = np.frombuffer(raw, np.uint8)
        return arr.reshape(shape)


# ---------------------------------------------------------------------------
# Parameter accounting from tensor shapes
# ---------------------------------------------------------------------------
def logical_params(name: str, meta: dict) -> int:
    """Number of model parameters a stored tensor represents.

    * MXFP4 (``U8``, two 4-bit numbers per byte): the stored width is half the
      logical width; the ``*_scale`` companions are block scales, not parameters.
    * FP8 block scales (``*_scale_inv``) are not parameters either.
    """
    n = int(np.prod(meta["shape"]))
    if name.endswith(("weight_scale", "weight_scale_inv")):
        return 0
    if meta["dtype"] == "U8":
        return 2 * n
    return n


def categorize(key: str, name: str, cfg: dict) -> str:
    n = name.replace("language_model.", "")
    layer = re.search(r"model\.layers\.(\d+)\.", n)
    if n.startswith(("visual.", "vision_tower.", "mm_projector.", "speech_embeddings")):
        return "vision_audio"
    if n.startswith("model.mtp.") or (layer and int(layer.group(1)) >= cfg["num_hidden_layers"]):
        return "mtp"
    if "embed_tokens" in n:
        return "embedding"
    if "lm_head" in n:
        return "unembedding"
    if ".experts." in n and "shared_experts" not in n:
        return "routed_experts"
    if "routed_expert_" in n:
        return "latent_projection"
    if "shared_experts" in n:
        return "shared_experts"
    if ".gate.weight" in n or "e_score_correction_bias" in n:
        return "router"
    if ".indexer." in n:
        return "indexer"
    if "_res_proj" in n or "_res_norm" in n:
        return "attention_residuals"
    if ".self_attn." in n:
        return "attention"
    if ".mlp." in n:
        return "dense_ffn"
    if "norm" in n:
        return "norms"
    return "other"


def tally(key: str, w: Weights, cfg: dict) -> dict:
    cats: dict[str, int] = {}
    storage: dict[str, int] = {}
    for name, meta in w.tensors.items():
        c = categorize(key, name, cfg)
        cats[c] = cats.get(c, 0) + logical_params(name, meta)
        a, b = meta["data_offsets"]
        storage[meta["dtype"]] = storage.get(meta["dtype"], 0) + (b - a)
    return {"by_category": dict(sorted(cats.items(), key=lambda kv: -kv[1])), "total": sum(cats.values()),
            "storage_bytes": storage, "n_tensors": len(w.tensors)}


# ---------------------------------------------------------------------------
# 4-bit numbers (MXFP4: E2M1 elements, one E8M0 power-of-two scale per 32)
# ---------------------------------------------------------------------------
FP4_E2M1 = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6, -0.0, -0.5, -1, -1.5, -2, -3, -4, -6])


def mxfp4_block(packed_row: np.ndarray, scale_row: np.ndarray, block: int) -> dict:
    """Decode block ``block`` (32 numbers) of one packed row: low nibble first."""
    bytes_ = packed_row[16 * block:16 * (block + 1)]
    codes = np.empty(32, dtype=np.uint8)
    codes[0::2], codes[1::2] = bytes_ & 0x0F, bytes_ >> 4
    exp = int(scale_row[block]) - 127
    return {"codes": codes.tolist(), "elements": FP4_E2M1[codes].tolist(), "scale_exp": exp,
            "values": (FP4_E2M1[codes] * 2.0 ** exp).tolist()}


# ---------------------------------------------------------------------------
# Per-model extraction
# ---------------------------------------------------------------------------
def config_summary(key: str, cfg: dict) -> dict:
    if key == "kimi":
        t = cfg["text_config"]
        la = t["linear_attn_config"]
        n = t["num_hidden_layers"]
        full = set(x - 1 for x in la["full_attn_layers"])  # the config lists layers 1-based
        return {
            "layers": n, "hidden": t["hidden_size"], "vocab": t["vocab_size"], "heads": t["num_attention_heads"],
            "layer_types": ["mla" if i in full else "kda" for i in range(n)],
            "kv_lora_rank": t["kv_lora_rank"], "q_lora_rank": t["q_lora_rank"], "qk_nope_head_dim": t["qk_nope_head_dim"],
            "qk_rope_head_dim": t["qk_rope_head_dim"], "v_head_dim": t["v_head_dim"], "mla_use_nope": t["mla_use_nope"],
            "kda_heads": la["num_heads"], "kda_head_dim": la["head_dim"], "kda_conv": la["short_conv_kernel_size"],
            "kda_gate_lower_bound": la["gate_lower_bound"],
            "experts": t["num_experts"], "experts_per_token": t["num_experts_per_token"],
            "shared_experts": t["num_shared_experts"], "expert_ffn": t["moe_intermediate_size"],
            "latent_dim": t["routed_expert_hidden_size"], "dense_layers": t["first_k_dense_replace"],
            "dense_ffn": t["intermediate_size"], "router": t["moe_router_activation_func"],
            "activation": t["hidden_act"], "situ_beta_gate": t["activation_situ_beta"],
            "situ_beta_up": t["activation_situ_linear_beta"], "attn_res_block": t["attn_res_block_size"],
            "context": t["max_position_embeddings"],
        }
    if key == "glm":
        n = cfg["num_hidden_layers"]
        return {
            "layers": n, "hidden": cfg["hidden_size"], "vocab": cfg["vocab_size"], "heads": cfg["num_attention_heads"],
            "kv_lora_rank": cfg["kv_lora_rank"], "q_lora_rank": cfg["q_lora_rank"], "qk_nope_head_dim": cfg["qk_nope_head_dim"],
            "qk_rope_head_dim": cfg["qk_rope_head_dim"], "v_head_dim": cfg["v_head_dim"],
            "index_heads": cfg["index_n_heads"], "index_head_dim": cfg["index_head_dim"], "index_topk": cfg["index_topk"],
            "indexer_types": cfg["indexer_types"], "mlp_layer_types": cfg["mlp_layer_types"],
            "experts": cfg["n_routed_experts"], "experts_per_token": cfg["num_experts_per_tok"],
            "shared_experts": cfg["n_shared_experts"], "expert_ffn": cfg["moe_intermediate_size"],
            "dense_layers": cfg["first_k_dense_replace"], "dense_ffn": cfg["intermediate_size"],
            "router": cfg["scoring_func"], "routed_scaling": cfg["routed_scaling_factor"],
            "mtp_layers": cfg["num_nextn_predict_layers"], "rope_theta": cfg["rope_parameters"]["rope_theta"],
            "context": cfg["max_position_embeddings"],
        }
    n = cfg["num_hidden_layers"]
    return {
        "layers": n, "hidden": cfg["hidden_size"], "vocab": cfg["vocab_size"], "heads": cfg["num_attention_heads"],
        "kv_heads": cfg["num_key_value_heads"], "swa_kv_heads": cfg["swa_num_key_value_heads"],
        "head_dim": cfg["head_dim"], "v_head_dim": cfg["v_head_dim"], "window": cfg["sliding_window"],
        "layer_types": ["swa" if x else "global" for x in cfg["hybrid_layer_pattern"]],
        "rope_fraction": cfg["partial_rotary_factor"], "rope_theta_global": cfg["rope_theta"],
        "rope_theta_swa": cfg["swa_rope_theta"], "sink_swa": cfg["add_swa_attention_sink_bias"],
        "sink_global": cfg["add_full_attention_sink_bias"], "value_scale": cfg["attention_value_scale"],
        "experts": cfg["n_routed_experts"], "experts_per_token": cfg["num_experts_per_tok"], "shared_experts": 0,
        "expert_ffn": cfg["moe_intermediate_size"], "dense_ffn": cfg["intermediate_size"],
        "dense_layers": sum(1 for x in cfg["moe_layer_freq"] if not x), "router": cfg["scoring_func"],
        "context": cfg["max_position_embeddings"],
    }


def active_params(key: str, t: dict, c: dict) -> int:
    """Parameters touched per text token: everything in the language model except
    the routed experts it was not sent to (and the vision/audio encoders and the
    speculative-decoding MTP layers, which do not run per generated token)."""
    cats = t["by_category"]
    k_over_n = c["experts_per_token"] / c["experts"]
    skip = {"vision_audio", "mtp", "routed_experts"}
    return int(sum(v for k, v in cats.items() if k not in skip) + k_over_n * cats["routed_experts"])


def extract(key: str, offline: bool) -> dict:
    repo, aa_name = MODELS[key]
    print(f"{key}: {repo}", flush=True)
    cfg = json.loads(hf_file(repo, "config.json", offline))
    text_cfg = cfg.get("text_config", cfg)
    w = Weights(repo, offline)
    t = tally(key, w, text_cfg)
    c = config_summary(key, cfg)
    out = {"repo": repo, "aa_name": aa_name, "config": c, "params": t, "active": active_params(key, t, c)}
    pre = "language_model." if key == "kimi" else ""

    # Router balancing biases ("e_score_correction_bias"): one per expert per MoE layer.
    bias_names = sorted((n for n in w.tensors if n.endswith("gate.e_score_correction_bias")),
                        key=lambda n: int(re.search(r"layers\.(\d+)\.", n).group(1)))
    bias_names = [n for n in bias_names if int(re.search(r"layers\.(\d+)\.", n).group(1)) < text_cfg["num_hidden_layers"]]
    with ThreadPoolExecutor(8) as pool:
        biases = list(pool.map(w.read, bias_names))
    out["router_bias"] = {
        "layers": [int(re.search(r"layers\.(\d+)\.", n).group(1)) for n in bias_names],
        "std": [float(np.std(b)) for b in biases],
        "min": [float(np.min(b)) for b in biases], "max": [float(np.max(b)) for b in biases],
        "example_layer": int(re.search(r"layers\.(\d+)\.", bias_names[len(bias_names) // 2]).group(1)),
        "example": [round(float(x), 5) for x in biases[len(bias_names) // 2]],
    }

    if key == "mimo":
        sinks = sorted((n for n in w.tensors if n.startswith("model.layers.") and n.endswith("attention_sink_bias")),
                       key=lambda n: int(re.search(r"layers\.(\d+)\.", n).group(1)))
        with ThreadPoolExecutor(8) as pool:
            vals = list(pool.map(w.read, sinks))
        out["sink_bias"] = {"layers": [int(re.search(r"layers\.(\d+)\.", n).group(1)) for n in sinks],
                            "values": [[round(float(x), 4) for x in v] for v in vals]}
        # One block of 32 real 4-bit weights: expert 0, layer 5, up projection, row 0.
        name = "model.layers.5.mlp.experts.0.up_proj.weight"
        out["fp4_block"] = dict(mxfp4_block(w.read(name, (0, 1))[0], w.read(name + "_scale", (0, 1))[0], 0),
                                tensor=name, row=0, block=0)

    if key == "kimi":
        kda = [i for i, tp in enumerate(c["layer_types"]) if tp == "kda"]
        names = [f"{pre}model.layers.{i}.self_attn.{p}" for i in kda for p in ("A_log", "dt_bias")]
        with ThreadPoolExecutor(8) as pool:
            arrs = dict(zip(names, pool.map(w.read, names)))
        H, D, gmin = c["kda_heads"], c["kda_head_dim"], c["kda_gate_lower_bound"]
        # Per-channel log-retention at rest (decay logit z = its bias), Kimi K3's bounded gate:
        #   g = g_min * sigmoid(exp(A_h) * z),   alpha = exp(g)   (report eq. 5)
        logs = []
        for i in kda:
            A = arrs[f"{pre}model.layers.{i}.self_attn.A_log"][:H]  # stored padded to 128; first H are the heads
            z = arrs[f"{pre}model.layers.{i}.self_attn.dt_bias"].reshape(H, D)
            g = gmin / (1 + np.exp(-np.exp(A)[:, None] * z))
            logs.append(g)
        g = np.stack(logs)  # (layers, heads, channels)
        half_life = np.log(2) / -g  # tokens until a stored association fades to half
        edges = np.logspace(-1, 4, 51)
        hist, _ = np.histogram(np.clip(half_life, edges[0], edges[-1] * 0.999), edges)
        out["kda_decay"] = {
            "formula": "alpha = exp(g_min * sigmoid(exp(A_log[h]) * dt_bias[h, c])), half-life = ln 2 / -log(alpha)",
            "layers": kda, "half_life_edges": edges.tolist(), "half_life_hist": hist.tolist(),
            "median_half_life": float(np.median(half_life)),
            "frac_over_100": float(np.mean(half_life > 100)), "frac_under_1": float(np.mean(half_life < 1)),
            "per_layer_median": [float(np.median(h)) for h in half_life],
            "example_head": [round(float(x), 3) for x in np.sort(half_life[len(kda) // 2, 0])],
        }
        # Attention-residual pseudo-queries: one learned d-vector per sublayer (norm weight * projection).
        q = []
        for i in range(c["layers"]):
            for part in ("self_attention", "mlp"):
                q.append(w.read(f"{pre}model.layers.{i}.{part}_res_norm.weight").astype(np.float64)
                         * w.read(f"{pre}model.layers.{i}.{part}_res_proj.weight")[0].astype(np.float64))
        Q = np.stack(q)
        Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
        out["attn_res_queries"] = {"norms": np.linalg.norm(Q, axis=1).round(3).tolist(),
                                   "cosine": (Qn @ Qn.T).round(3).tolist()}
        name = f"{pre}model.layers.12.block_sparse_moe.experts.0.w1.weight"
        out["fp4_block"] = dict(mxfp4_block(w.read(name + "_packed", (0, 1))[0], w.read(name + "_scale", (0, 1))[0], 0),
                                tensor=name, row=0, block=0)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    data = {"as_of": AS_OF.isoformat(), "leaderboard": leaderboard(args.offline), "models": {}}
    top3 = [r["name"] for r in data["leaderboard"]["open"][:3]]
    assert top3 == [aa for _, aa in MODELS.values()], top3
    for key in MODELS:
        data["models"][key] = extract(key, args.offline)
    OUT.write_text(json.dumps(data, separators=(",", ":")))
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1e3:.0f} kB)")
    for key, m in data["models"].items():
        print(f"  {key}: {m['params']['total'] / 1e9:.1f}B total, {m['active'] / 1e9:.1f}B active, "
              f"{m['params']['n_tensors']:,} tensors")


if __name__ == "__main__":
    main()
