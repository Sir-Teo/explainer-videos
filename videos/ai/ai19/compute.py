"""Precompute everything numerical in Part 19 of the AI series ("Inference").

    python -m videos.ai.ai19.compute              # everything missing (trains two small drafters; about 1.5 h)
    python -m videos.ai.ai19.compute --force rounding

Results are cached in ``.cache/ai19/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are the
series' own: the novels model (``explainer.ai.novels``, Parts 18, 27 and 30 use it too) and Part 13's character
transformer.  Timings are of the machine that runs this, on one thread, measured with ``engine.interleaved_min``
(every configuration in turn, shuffled, many rounds, the fastest kept), so a busy machine slows them less; each item
records the load average it saw.  Long items save their pieces as they go (``CACHE.partial``, checkpoints), so a
killed run resumes.

Items:
    roof        this machine's roof on one thread: the fastest matrix product, and the memory's read bandwidth; and a
                stack of weight matrices too big for the caches (192 MB) multiplied by batches of 1 ... 512 vectors:
                matrix-vector products becoming matrix-matrix products
    phases      the novels model on the inference engine (engine.py): prefill of prompts of 1 ... 256 tokens, decode
                steps for batches of 1 ... 256, decode against context length, a sliding window, and a cached prefix
    kv          the key-value cache per token for our model and published ones (MHA, GQA, MLA, sliding windows),
                against context length
    economics   batch size against speed per user and cost per token: measured on our model; and modelled for an
                H100 serving Llama 3.1 8B (published sizes), at DeepSeek's rental price of 2 USD per GPU-hour
    serving     a server simulated with the measured costs: static batches, continuous batching, chunked prefill, and
                prefill and decode on separate workers; latency and throughput
    paging      a key-value memory pool: blocks reserved at the maximum length, contiguous first-fit, pages of 1 ...
                256 tokens; how many conversations fit; prefixes shared in a radix tree
    exact       speculative sampling checked to be exact: one character of Part 13's transformer (200,000 samples),
                and the first two tokens of the novels model with a two-token draft (the joint distribution)
    drafters    two drafters trained for the novels model, a two-layer model of its own and an EAGLE-style head on the
                big model's features; acceptance during training; speculative decoding runs: accepted tokens per pass
                against the formula, and time on this machine
    rounding    the novels model's weights rounded to 2 ... 8 bits: the error against Delta^2/12, and the loss, with one
                scale per tensor, per row, per group of 64 or 32
    outliers    the inputs of every linear layer: channel by channel, how large; activations rounded too (W8A8, W4A8,
                W4A4) plainly, with SmoothQuant, and with LLM.int8()'s outlier channels kept aside
    gptq        GPTQ (Optimal Brain Surgeon, column by column) and AWQ against rounding, at 4 and 3 bits, on three
                calibration sets; one row's GPTQ, step by step
    rotation    the residual stream rotated (QuaRot's Hadamard, random rotations, and one learned as SpinQuant does,
                its training replayed), at 4-bit weights and activations
    formats     MXFP4 and NVFP4 bit by bit on a block of our weights; the model in each format against 4-bit integers
    kvquant     the key-value cache rounded to 8, 4, 3 and 2 bits: per token, per channel (KIVI), rotated, FP8
    flash       attention tile by tile with an online softmax, on Part 13's real queries, keys and values, against the
                plain formula; memory traffic of both (FlashAttention's theorem, counted); split-KV decoding checked
    grammar     constrained decoding with an automaton's token masks on the novels model, against unconstrained
                sampling; how masking reweights a small language (Part 13's character model)
    frontier    bandwidth bounds on devices, the cost of long chains of thought, prices per token (published)
"""

from __future__ import annotations

import math
import time

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai19")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def threads(n: int = 1) -> None:
    import torch

    torch.set_num_threads(n)


def base():
    """The series' novels model (trains it first if missing: explainer.ai.novels)."""
    from explainer.ai import novels as N

    return N.load_base()


def count(model) -> dict:
    """The novels model's sizes: the matrices a decode step reads (blocks and head; the embedding is a lookup)."""
    c = model.count()
    return dict(total=int(c["total"]), body=int(c["body"]), head=int(c["head"]), read=int(c["compute"]))


# ---------------------------------------------------------------------------
# The roof of this machine, and matrix-vector products becoming matrix products
# ---------------------------------------------------------------------------
STACK = dict(n=2048, layers=12)  # 12 matrices of 2048 x 2048 in fp32: 192 MB, far more than any cache here
BATCHES = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]


def compute_roof():
    import torch

    from videos.ai.ai19.engine import interleaved_min, loadavg

    threads(1)
    la = loadavg()
    g = torch.Generator().manual_seed(17)
    out = dict(threads=1, loadavg_before=la)
    # peak arithmetic: fp32 matrix products
    mats = {n: (torch.randn(n, n, generator=g), torch.randn(n, n, generator=g)) for n in (256, 512, 1024, 2048)}
    r = interleaved_min(list(mats), lambda n: torch.mm(*mats[n]), rounds=7, min_time=0.1)
    out["gemm"] = [[n, 2 * n ** 3 / r[n][0], 2 * n ** 3 / r[n][1]] for n in mats]
    out["peak"] = max(x[1] for x in out["gemm"])
    del mats
    # memory: reading 256 MB (a sum), and copying it
    x = torch.randn(64 * 2 ** 20, generator=g)  # 256 MB
    y = torch.empty_like(x)
    r = interleaved_min(["read", "copy"], lambda k: x.sum() if k == "read" else y.copy_(x), rounds=9, min_time=0.2)
    out["read_bw"] = x.numel() * 4 / r["read"][0]
    out["copy_bw"] = 2 * x.numel() * 4 / r["copy"][0]
    out["bw"] = max(out["read_bw"], out["copy_bw"])
    del x, y
    # the stack: a batch of b vectors through 12 weight matrices (each read once per pass)
    n, L = STACK["n"], STACK["layers"]
    Ws = [torch.randn(n, n, generator=g) / math.sqrt(n) for _ in range(L)]
    xs = {b: torch.randn(b, n, generator=g) for b in BATCHES}

    def run(b):  # as a linear layer does it: y = x W^T
        h = xs[b]
        for W in Ws:
            h = torch.nn.functional.linear(h, W)
        return h

    r = interleaved_min(BATCHES, run, rounds=11, min_time=0.15)
    t = np.array([r[b][0] for b in BATCHES])
    tmed = np.array([r[b][1] for b in BATCHES])
    flops = np.array([2.0 * L * n * n * b for b in BATCHES])
    nbytes = np.array([4.0 * L * n * n + 2 * 4.0 * L * n * b for b in BATCHES])  # weights once, activations in/out
    out.update(stack_n=n, stack_layers=L, stack_mb=4.0 * L * n * n / 1e6, batches=BATCHES, stack_t=t, stack_tmed=tmed,
               stack_flops=flops, stack_bytes=nbytes, stack_rate=flops / t, stack_tps=np.array(BATCHES) / t,
               stack_intensity=flops / nbytes)
    pred = np.maximum(nbytes / out["bw"], flops / out["peak"])
    out["stack_pred"] = pred
    out["knee_pred"] = 2 * out["peak"] / out["bw"]  # fp32: intensity ~ b / 2, equal to the ridge P / beta at b = 2P/beta
    # the measured knee: where the time per pass has doubled from batch 1
    out["knee_meas"] = float(np.interp(2 * t[0], t, BATCHES)) if t[-1] > 2 * t[0] else float(BATCHES[-1])
    out["loadavg_after"] = loadavg()
    print(f"    peak {out['peak'] / 1e9:.0f} GFLOP/s; read {out['read_bw'] / 1e9:.1f} GB/s; "
          f"knee at batch {out['knee_meas']:.0f} (roofline {out['knee_pred']:.0f})", flush=True)
    return out


# ---------------------------------------------------------------------------
# Prefill and decode on the novels model
# ---------------------------------------------------------------------------
PREFILL_T = [1, 2, 4, 8, 16, 32, 64, 128, 256]
DECODE_B = [1, 2, 4, 8, 16, 32, 64, 128, 256]
CTXS = [128, 256, 512, 1024, 2048]
CTX_B = [1, 8, 32]


def compute_phases():
    import torch

    from videos.ai.ai19 import engine as E

    threads(1)
    model = base()
    out = dict(threads=1, loadavg_before=E.loadavg(), sizes=count(model))
    w = E.heldout(4, 64)
    out["check"] = E.check(model, w[:, :64])  # prefill + decode steps against the full forward
    assert out["check"] < 1e-3
    eng = E.Engine(model, max_len=max(CTXS) + 1)
    cfg = model.cfg
    kv_tok = 2 * cfg.layers * cfg.d * 4  # bytes of keys and values per token (fp32)
    out["kv_per_token"] = kv_tok
    caches = {}

    with torch.inference_mode():
        # prefill: a prompt of T tokens in one pass, batch 1
        pre = {T: (torch.zeros(1, T, dtype=torch.long), eng.new_cache(1, T)) for T in PREFILL_T}

        def prefill(T):
            ids, c = pre[T]
            c.len = 0
            eng.forward(ids, c, logits="last")

        r = E.interleaved_min(PREFILL_T, prefill, rounds=9, min_time=0.05)
        out["prefill_t"] = np.array([r[T][0] for T in PREFILL_T])
        out["prefill_tmed"] = np.array([r[T][1] for T in PREFILL_T])
        del pre

        # decode: one step for a batch of B sequences, each with ctx tokens already cached
        def setup(key):
            B, ctx, win = key
            if key not in caches:
                caches.clear()
                caches[key] = (torch.zeros(B, 1, dtype=torch.long), eng.new_cache(B, ctx + 1, fill=True))

        def step(key):
            B, ctx, win = key
            ids, c = caches[key]
            c.len = ctx
            if win:  # a sliding window: attend to the last `win` positions only (a ring buffer would hold just these)
                eng.window = win
            eng.forward(ids, c, logits="last")
            eng.window = 0

        eng.window = 0
        keys = [(B, 128, 0) for B in DECODE_B]
        r = _interleave_cached(keys, setup, step, rounds=9)
        out["decode_t"] = np.array([r[k][0] for k in keys])
        out["decode_tmed"] = np.array([r[k][1] for k in keys])
        keys = [(B, ctx, 0) for B in CTX_B for ctx in CTXS]
        r = _interleave_cached(keys, setup, step, rounds=7)
        out["ctx_t"] = np.array([[r[(B, ctx, 0)][0] for ctx in CTXS] for B in CTX_B])
        keys = [(8, ctx, 128) for ctx in CTXS]
        r = _interleave_cached(keys, setup, step, rounds=7)
        out["win_t"] = np.array([r[k][0] for k in keys])
        caches.clear()

        # a cached prefix: prefill the last 32 tokens of a 256-token prompt, the first 224 already in the cache
        c = eng.new_cache(1, 256)
        ids = torch.zeros(1, 256, dtype=torch.long)

        def pref(k):
            c.len = 0 if k == "full" else 224
            eng.forward(ids if k == "full" else ids[:, 224:], c, logits="last")

        r = E.interleaved_min(["full", "suffix"], pref, rounds=9, min_time=0.05)
        out["prefix_full_t"], out["prefix_suffix_t"] = r["full"][0], r["suffix"][0]

    n = out["sizes"]["read"]
    out.update(prefill_T=PREFILL_T, decode_B=DECODE_B, ctxs=CTXS, ctx_B=CTX_B, window=128)
    out["prefill_tps"] = np.array(PREFILL_T) / out["prefill_t"]
    out["decode_tps"] = np.array(DECODE_B) / out["decode_t"]
    # arithmetic intensity: FLOPs per byte of weights (and cache) read, 4-byte numbers
    out["prefill_flops"] = 2.0 * n * np.array(PREFILL_T)
    out["prefill_bytes"] = 4.0 * n + 0.0 * np.array(PREFILL_T)
    attn = lambda B, ctx: 4.0 * cfg.layers * cfg.d * ctx * B  # noqa: E731  (q.k and p.v for every cached position)
    out["decode_flops"] = np.array([2.0 * n * B + attn(B, 128) for B in DECODE_B])
    out["decode_bytes"] = np.array([4.0 * n + kv_tok * 128 * B for B in DECODE_B])
    out["ctx_bytes"] = np.array([[4.0 * n + kv_tok * ctx * B for ctx in CTXS] for B in CTX_B])
    out["loadavg_after"] = E.loadavg()
    print(f"    decode {out['decode_tps'][0]:.0f} tokens/s at batch 1, {out['decode_tps'][-1]:.0f} at "
          f"{DECODE_B[-1]}; prefill {out['prefill_tps'][-1]:.0f} tokens/s", flush=True)
    return out


def _interleave_cached(keys, setup, step, rounds=7, min_time=0.05, seed=0):
    """interleaved_min for configurations that each need their own (large) cache: built at each visit."""
    from videos.ai.ai19.engine import interleaved_min

    return interleaved_min(keys, step, rounds=rounds, min_time=min_time, seed=seed, setup=setup)


# ---------------------------------------------------------------------------
ITEMS = {
    "roof": compute_roof,
    "phases": compute_phases,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
