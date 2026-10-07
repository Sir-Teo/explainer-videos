"""Probes of GPT-2 small (124M parameters, OpenAI 2019) via Hugging Face.

Every function returns plain Python / numpy data so results can be cached as
JSON and played back by scenes without torch.
"""

from __future__ import annotations

import warnings
from functools import lru_cache

import numpy as np

warnings.filterwarnings("ignore")


@lru_cache(maxsize=None)
def load(name: str = "gpt2"):
    import torch
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast

    torch.set_grad_enabled(False)
    tok = GPT2TokenizerFast.from_pretrained("openai-community/gpt2")
    model = GPT2LMHeadModel.from_pretrained(f"openai-community/{name}", attn_implementation="eager").eval()
    return tok, model


def tokenize(text: str) -> tuple[list[int], list[str]]:
    tok, _ = load()
    ids = tok(text).input_ids
    return ids, [tok.decode([i]) for i in ids]


def single_id(word: str) -> int:
    ids, pieces = tokenize(word)
    if len(ids) != 1:
        raise ValueError(f"{word!r} is not a single GPT-2 token: {pieces}")
    return ids[0]


def decode(i: int) -> str:
    tok, _ = load()
    return tok.decode([int(i)])


def forward(ids: list[int], name: str = "gpt2"):
    import torch

    _, model = load(name)
    return model(torch.tensor([ids]), output_attentions=True, output_hidden_states=True)


def top_k(probs, k: int) -> list[tuple[str, float]]:
    idx = np.argsort(-probs)[:k]
    return [(decode(i), float(probs[i])) for i in idx]


def next_token(text: str, k: int = 8, name: str = "gpt2") -> dict:
    ids, _ = tokenize(text)
    logits = forward(ids, name).logits[0, -1].numpy().astype(np.float64)
    p = np.exp(logits - logits.max())
    p /= p.sum()
    idx = np.argsort(-p)[:k]
    return {
        "tokens": [decode(i) for i in idx],
        "probs": [float(p[i]) for i in idx],
        "logits": [float(logits[i]) for i in idx],
        "argmax": decode(int(np.argmax(p))),
    }


def greedy(text: str, steps: int, k: int = 8) -> list[dict]:
    """Greedy decoding, recording the top-k distribution at every step."""
    out = []
    for _ in range(steps):
        d = next_token(text, k)
        d["prompt"] = text
        out.append(d)
        text += d["argmax"]
    return out


def residual_stream(ids: list[int]) -> np.ndarray:
    """Residual stream before each block and before the final norm: (n_layer + 1, T, d)."""
    import torch

    _, model = load()
    hs = model(torch.tensor([ids]), output_hidden_states=True).hidden_states
    # HF applies ln_f to the last entry; recompute the raw residual after the last block.
    acts = {}

    def grab(m, i, o):
        o = o[0] if isinstance(o, tuple) else o
        acts["x"] = o[0] if o.dim() == 3 else o

    h = model.transformer.h[-1].register_forward_hook(grab)
    model(torch.tensor([ids]))
    h.remove()
    raw = [t[0].numpy() for t in hs[:-1]] + [acts["x"].numpy()]
    return np.stack(raw)


def logit_lens(text: str, target: str, k: int = 3) -> list[dict]:
    """Decode the last position's residual stream after every layer."""
    import torch

    _, model = load()
    ids, _ = tokenize(text)
    tid = single_id(target)
    res = residual_stream(ids)
    rows = []
    for layer, x in enumerate(res):
        logits = model.lm_head(model.transformer.ln_f(torch.tensor(x[-1]))).numpy().astype(np.float64)
        p = np.exp(logits - logits.max())
        p /= p.sum()
        rows.append({
            "layer": layer,
            "top": top_k(p, k),
            "target_rank": int((logits > logits[tid]).sum()) + 1,
            "target_prob": float(p[tid]),
        })
    return rows


def attention(ids: list[int], layer: int, head: int) -> np.ndarray:
    return forward(ids).attentions[layer][0, head].numpy()


def qk_scores(ids: list[int], layer: int, head: int) -> np.ndarray:
    """Pre-softmax scores q.k / sqrt(d_head) for one head (causal entries only meaningful)."""
    import torch

    _, model = load()
    res = residual_stream(ids)
    blk = model.transformer.h[layer]
    x = blk.ln_1(torch.tensor(res[layer]))
    q, k, _ = blk.attn.c_attn(x).split(768, dim=-1)
    dh = 64
    q, k = q[:, head * dh : (head + 1) * dh], k[:, head * dh : (head + 1) * dh]
    return (q @ k.T / np.sqrt(dh)).numpy()


def head_scores(ids: list[int], period: int) -> tuple[np.ndarray, np.ndarray]:
    """(previous-token score, induction score) for every head, on a sequence that
    repeats with the given period."""
    att = forward(ids).attentions
    n_layer, n_head = len(att), att[0].shape[1]
    prev, ind = np.zeros((n_layer, n_head)), np.zeros((n_layer, n_head))
    T = len(ids)
    for L in range(n_layer):
        A = att[L][0].numpy()
        prev[L] = np.mean([A[:, i, i - 1] for i in range(2, T)], axis=0)
        ind[L] = np.mean([A[:, i, i - period + 1] for i in range(period + 1, T)], axis=0)
    return prev, ind


def token_losses(ids: list[int]) -> list[float]:
    """-log p(actual next token) at every position."""
    logits = forward(ids).logits[0].numpy().astype(np.float64)
    out = []
    for i in range(len(ids) - 1):
        lg = logits[i]
        lse = lg.max() + np.log(np.exp(lg - lg.max()).sum())
        out.append(float(lse - lg[ids[i + 1]]))
    return out


def mlp_activations(text: str, layer: int) -> np.ndarray:
    """GELU outputs of one MLP layer at every position: (T, 3072)."""
    import torch

    _, model = load()
    ids, _ = tokenize(text)
    acts = {}

    def grab(m, i, o):  # must return None: a returned value would replace the output
        acts["a"] = o[0].numpy()

    h = model.transformer.h[layer].mlp.act.register_forward_hook(grab)
    model(torch.tensor([ids]))
    h.remove()
    return acts["a"]


def generate(text: str, n: int, name: str = "gpt2") -> str:
    tok, model = load(name)
    x = tok(text, return_tensors="pt").input_ids
    g = model.generate(x, max_new_tokens=n, do_sample=False, pad_token_id=tok.eos_token_id)
    return tok.decode(g[0][x.shape[1]:])


def param_breakdown(name: str = "gpt2") -> dict:
    _, model = load(name)
    t = model.transformer
    n = lambda m: int(sum(p.numel() for p in m.parameters()))  # noqa: E731
    blk = t.h[0]
    return {
        "token_embedding": n(t.wte),
        "position_embedding": n(t.wpe),
        "attention_per_layer": n(blk.attn),
        "mlp_per_layer": n(blk.mlp),
        "norms_per_layer": n(blk.ln_1) + n(blk.ln_2),
        "per_layer": n(blk),
        "n_layer": len(t.h),
        "final_norm": n(t.ln_f),
        "total": n(model),
        "d_model": int(t.wte.weight.shape[1]),
        "vocab": int(t.wte.weight.shape[0]),
        "context": int(t.wpe.weight.shape[0]),
        "n_head": int(model.config.n_head),
    }


def sample(text: str, n: int, temperature: float, seed: int = 0, name: str = "gpt2") -> str:
    """Sample ``n`` tokens at the given temperature (0 = greedy), reproducibly."""
    import torch

    tok, model = load(name)
    ids = tok(text, return_tensors="pt").input_ids
    g = torch.Generator().manual_seed(seed)
    for _ in range(n):
        logits = model(ids).logits[0, -1].double()
        if temperature == 0:
            nxt = logits.argmax()[None]
        else:
            nxt = torch.multinomial((logits / temperature).softmax(-1), 1, generator=g)
        ids = torch.cat([ids, nxt[None]], dim=1)
    return tok.decode(ids[0][len(tok(text).input_ids):])
