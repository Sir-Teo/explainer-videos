"""Small, deterministic computations behind the schematic parts of the video.

Everything here is cheap (milliseconds) and seeded, so scenes call it directly.
Nothing here imitates a real model's activations: these are the textbook
mechanisms (associative memories, quantile balancing, attention sinks, gated
activations) run on synthetic inputs, and the narration says so.  The real
numbers (configs, parameter counts, learned weights) come from ``data.json``.
"""

from __future__ import annotations

import json
from functools import lru_cache
from math import comb
from pathlib import Path

import numpy as np

DATA = Path(__file__).with_name("data.json")


@lru_cache(maxsize=1)
def data() -> dict:
    return json.loads(DATA.read_text())


def model(key: str) -> dict:
    return data()["models"][key]


def cfg(key: str) -> dict:
    return model(key)["config"]


# ---------------------------------------------------------------------------
# Softmax with and without an attention sink (MiMo, gpt-oss style)
# ---------------------------------------------------------------------------
def softmax(x) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    e = np.exp(x - x.max())
    return e / e.sum()


def sink_softmax(logits, sink: float) -> tuple[np.ndarray, float]:
    """Weights over the real tokens, and the mass absorbed by the sink logit."""
    z = np.append(np.asarray(logits, dtype=float), sink)
    p = softmax(z)
    return p[:-1], float(p[-1])


# ---------------------------------------------------------------------------
# Associative memories: linear attention vs. the delta rule
# ---------------------------------------------------------------------------
def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def write_linear(S, k, v):
    return S + np.outer(v, k)


def write_delta(S, k, v, beta=1.0, alpha=None):
    """S <- (decay) then S + beta (v - S k) k^T.  ``alpha`` is a per-key-channel retention."""
    if alpha is not None:
        S = S * np.asarray(alpha)[None, :]
    return S + beta * np.outer(v - S @ k, k)


def reassignment_curve(d=64, n_keys=16, max_writes=320, trials=20, seed=0) -> dict:
    """A memory that must keep facts *up to date*: ``n_keys`` keys are reassigned
    fresh random values over and over (like variables in a program).  At the end,
    read every key and compare with its latest value (cosine), for the plain sum
    (linear attention) and the delta rule."""
    rng = np.random.default_rng(seed)
    ws = np.unique(np.round(np.geomspace(n_keys, max_writes, 12)).astype(int))
    out = {"writes": ws.tolist(), "linear": [], "delta": [], "d": d, "n_keys": n_keys}
    for w in ws:
        cl, cd = [], []
        for _ in range(trials):
            K = unit(rng.normal(size=(n_keys, d)))
            order = np.concatenate([np.arange(n_keys), rng.integers(0, n_keys, w - n_keys)])
            latest = np.zeros((n_keys, d))
            Sl, Sd = np.zeros((d, d)), np.zeros((d, d))
            for i in order:
                v = unit(rng.normal(size=d))
                latest[i] = v
                Sl, Sd = write_linear(Sl, K[i], v), write_delta(Sd, K[i], v)
            for S, acc in ((Sl, cl), (Sd, cd)):
                acc.append(np.mean(np.sum(unit(K @ S.T) * latest, axis=1)))
        out["linear"].append(float(np.mean(cl)))
        out["delta"].append(float(np.mean(cd)))
    return out


def overwrite_demo() -> dict:
    """2-D memory: store k1 -> v1 and k2 -> v2, then overwrite k1 -> v1'.  The plain
    sum returns a blend of old and new; the delta rule returns the new value."""
    k1, k2 = unit([1.0, 0.25]), unit([0.35, 1.0])
    v1, v2, v1b = np.array([1.2, 0.9]), np.array([-1.0, 0.6]), np.array([0.3, -1.1])
    S = {"linear": np.zeros((2, 2)), "delta": np.zeros((2, 2))}
    steps = {"linear": [], "delta": []}
    for k, v in ((k1, v1), (k2, v2), (k1, v1b)):
        S["linear"] = write_linear(S["linear"], k, v)
        S["delta"] = write_delta(S["delta"], k, v)
        for r in S:
            steps[r].append(S[r].copy())
    return {"k1": k1, "k2": k2, "v1": v1, "v2": v2, "v1b": v1b, "steps": steps,
            "read_linear": steps["linear"][-1] @ k1, "read_delta": steps["delta"][-1] @ k1}


# ---------------------------------------------------------------------------
# Expert routing and Kimi K3's Quantile Balancing
# ---------------------------------------------------------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def route(scores, bias, k):
    """Top-k on biased scores; returns chosen indices (m x k) and per-expert loads."""
    chosen = np.argsort(-(scores + bias), axis=1)[:, :k]
    loads = np.bincount(chosen.ravel(), minlength=scores.shape[1])
    return chosen, loads


def qb_update(scores, bias, k):
    """One Quantile Balancing step (Kimi K3 report, eqs. 13-14)."""
    m, n = scores.shape
    q = m * k // n
    biased = scores + bias
    cutoff = -np.sort(-biased, axis=1)[:, k]  # (k+1)-th largest biased score per token
    margins = scores - cutoff[:, None]
    new = -np.sort(margins, axis=0)[::-1][q]  # minus the (q+1)-th largest margin of each expert
    return new - new.mean()


def expert_vectors(n, d=16, skew=1.5, seed=0):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n, d)) / np.sqrt(d), np.linspace(skew, -skew, n)  # some experts are more popular


def synthetic_batch(m, E, pop, seed=0):
    """Router scores (sigmoid) of a fresh batch of m random tokens for fixed experts."""
    X = np.random.default_rng(seed).normal(size=(m, E.shape[1]))
    return sigmoid(X @ E.T * 2.0 + pop[None, :])


def balancing_demo(m=8192, n=16, k=2, steps=20, gamma=0.01, seed=0) -> dict:
    """Loads per step for the fixed-step sign update (DeepSeek-V3) and for QB.
    Each step routes a fresh batch with the bias computed from the previous one."""
    E, pop = expert_vectors(n, seed=seed)

    def batch(t):
        return synthetic_batch(m, E, pop, seed=seed * 1000 + 1 + t)

    target = m * k / n
    out = {"target": target, "sign": [], "qb": []}
    b_sign, b_qb = np.zeros(n), np.zeros(n)
    for t in range(steps):
        s = batch(t)
        _, ls = route(s, b_sign, k)
        _, lq = route(s, b_qb, k)
        out["sign"].append(ls.tolist())
        out["qb"].append(lq.tolist())
        b_sign = b_sign + gamma * np.sign(target - ls)
        b_qb = qb_update(s, b_qb, k)
    out["imbalance_sign"] = [float(np.max(x) / target) for x in out["sign"]]
    out["imbalance_qb"] = [float(np.max(x) / target) for x in out["qb"]]
    return out


def qb_figure_example() -> dict:
    """The report's Figure 5 setting: 8 tokens, 4 experts, top-1, target load 2."""
    s = np.array([
        [0.92, 0.55, 0.30, 0.10], [0.88, 0.60, 0.35, 0.20], [0.80, 0.72, 0.40, 0.15], [0.75, 0.50, 0.70, 0.25],
        [0.60, 0.85, 0.30, 0.20], [0.55, 0.80, 0.45, 0.35], [0.50, 0.78, 0.65, 0.40], [0.70, 0.40, 0.66, 0.62],
    ])
    b0 = np.zeros(4)
    _, before = route(s, b0, 1)
    b1 = qb_update(s, b0, 1)
    chosen_after, after = route(s, b1, 1)
    return {"scores": s, "before": before.tolist(), "bias": b1, "after": after.tolist(),
            "chosen_before": route(s, b0, 1)[0][:, 0].tolist(), "chosen_after": chosen_after[:, 0].tolist()}


def expert_combinations() -> dict:
    return {key: comb(cfg(key)["experts"], cfg(key)["experts_per_token"]) for key in ("mimo", "glm", "kimi")}


# ---------------------------------------------------------------------------
# Gated activations
# ---------------------------------------------------------------------------
def swiglu_diag(x):
    x = np.asarray(x, dtype=float)
    return x * sigmoid(x) * x


def situ_diag(x, b1=4.0, b2=25.0):
    x = np.asarray(x, dtype=float)
    return b1 * np.tanh(x / b1) * sigmoid(x) * b2 * np.tanh(x / b2)


# ---------------------------------------------------------------------------
# Memory per token of context (KV cache), from the real configs
# ---------------------------------------------------------------------------
BF16 = 2


def kv_cache() -> dict:
    """Bytes of cache per token of context (BF16 keys/values; DSA indexer keys in FP8,
    as in DeepSeek-V3.2), plus the part that does not grow with context."""
    m, g, k = cfg("mimo"), cfg("glm"), cfg("kimi")
    n_ga = m["layer_types"].count("global")
    n_swa = m["layer_types"].count("swa")
    kv_dim = m["head_dim"] + m["v_head_dim"]
    mimo = {"per_token": n_ga * m["kv_heads"] * kv_dim * BF16,
            "fixed": n_swa * m["swa_kv_heads"] * kv_dim * BF16 * m["window"],
            "all_global_per_token": m["layers"] * m["kv_heads"] * kv_dim * BF16}
    latent = g["kv_lora_rank"] + g["qk_rope_head_dim"]
    glm = {"per_token": g["layers"] * latent * BF16 + g["indexer_types"].count("full") * g["index_head_dim"],
           "fixed": 0, "latent": latent,
           "mha_per_token": g["layers"] * g["heads"] * (g["qk_nope_head_dim"] + g["qk_rope_head_dim"] + g["v_head_dim"]) * BF16,
           "per_layer_mha": g["heads"] * (g["qk_nope_head_dim"] + g["qk_rope_head_dim"] + g["v_head_dim"])}
    n_mla = k["layer_types"].count("mla")
    n_kda = k["layer_types"].count("kda")
    kimi = {"per_token": n_mla * (k["kv_lora_rank"] + k["qk_rope_head_dim"]) * BF16,
            "fixed": n_kda * k["kda_heads"] * k["kda_head_dim"] ** 2 * 4,  # FP32 recurrent state
            "n_mla": n_mla, "n_kda": n_kda}
    return {"mimo": mimo, "glm": glm, "kimi": kimi}


def cache_gb(entry: dict, tokens: float) -> float:
    return (entry["per_token"] * tokens + entry["fixed"]) / 1e9


def swa_reach(window: int, layers: int) -> int:
    """How far back information can travel through ``layers`` sliding-window layers."""
    return layers * (window - 1)


if __name__ == "__main__":
    np.set_printoptions(precision=3, suppress=True)
    print("reassign", {k: np.round(v, 3) if isinstance(v, list) else v for k, v in reassignment_curve().items()})
    o = overwrite_demo()
    print("overwrite: linear reads", o["read_linear"], "delta reads", o["read_delta"], "new value", o["v1b"])
    b = balancing_demo()
    print("imbalance sign", np.round(b["imbalance_sign"], 2))
    print("imbalance qb  ", np.round(b["imbalance_qb"], 2))
    f = qb_figure_example()
    print("figure-5 example", f["before"], "->", f["after"], "bias", np.round(f["bias"], 3))
    print("combinations", {k: f"{v:.3e}" for k, v in expert_combinations().items()})
    print("kv", kv_cache())
    print("sink: nothing relevant", sink_softmax([0.1, -0.2, 0.0, 0.3, -0.1, 0.2], 2.0))
    print("situ max", situ_diag(np.linspace(-10, 100, 1001)).max(), "swiglu at 100", swiglu_diag(100))
