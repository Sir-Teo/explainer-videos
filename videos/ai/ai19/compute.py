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


def plain(x):
    """Nested containers with numpy inside, as JSON-able Python (top-level arrays go to the .npz instead)."""
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


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
STACK = dict(n=4096, layers=12)  # 12 matrices of 4096 x 4096 in fp32: 805 MB, more than a processor's caches hold


def largest_cache() -> int:
    """The processor's largest cache in bytes, as the system reports it (0 if it doesn't say)."""
    import subprocess
    import sys

    keys = (["hw.l3cachesize", "hw.l2cachesize", "hw.perflevel0.l2cachesize"] if sys.platform == "darwin" else
            ["LEVEL3_CACHE_SIZE", "LEVEL2_CACHE_SIZE"])
    best = 0
    for k in keys:
        cmd = ["sysctl", "-n", k] if sys.platform == "darwin" else ["getconf", k]
        try:
            v = subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
            best = max(best, int(v or 0))
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
    return best
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
    # memory: reading 512 MiB (a sum), and copying it: more than the caches, so this is the memory's speed
    out["cache_bytes"] = largest_cache()
    x = torch.randn(128 * 2 ** 20, generator=g)  # 512 MiB
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
    # the best streaming rate seen: a batch of one is itself a read of the whole stack
    out["stack_bw1"] = float(nbytes[0] / t[0])
    out["bw"] = max(out["bw"], out["stack_bw1"])
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
# The key-value cache, priced
# ---------------------------------------------------------------------------
def kv_bytes(cfg: dict, ctx, bytes_per=2, kind="gqa"):
    """Bytes of keys and values for one sequence of ``ctx`` tokens (DeepSeek-V2, Table 1): MHA 2 n_h d_h l, GQA
    2 n_g d_h l, MLA (d_c + d_R) l; a sliding window (gpt-oss: every other layer) caps those layers at the window."""
    ctx = np.asarray(ctx, float)
    L = cfg["layers"]
    if kind == "mla":
        return (cfg["kv_lora_rank"] + cfg["rope_dim"]) * L * ctx * bytes_per
    if kind == "mha_mla":  # DeepSeek-V3's attention without the compression: 128 heads of 192 (keys) + 128 (values)
        return cfg["heads"] * (cfg["nope_dim"] + cfg["rope_dim"] + cfg["v_dim"]) * L * ctx * bytes_per
    heads = cfg["heads"] if kind == "mha" else cfg["kv_heads"]
    per = 2 * heads * cfg["head_dim"] * bytes_per
    if kind == "window":
        return per * (L / 2 * ctx + L / 2 * np.minimum(ctx, cfg["window"]))
    return per * L * ctx


def compute_kv():
    from videos.ai.ai19 import facts as F

    model = base()
    c = model.cfg
    ctxs = np.unique(np.round(np.logspace(np.log10(256), np.log10(1_048_576), 41))).astype(float)
    ours = dict(layers=c.layers, heads=c.heads, kv_heads=c.heads, head_dim=c.d // c.heads)
    L70, V3, OSS = F.LLAMA31_70B, F.DSV3, F.GPT_OSS_120B
    rows = {  # name: (bytes per token at 16 bits, weights in bytes at 16 bits)
        "ours": (float(kv_bytes(ours, 1, 4, "mha")), 4.0 * count(model)["total"]),
        "llama70_mha": (float(kv_bytes(L70, 1, 2, "mha")), 2 * L70["params"]),
        "llama70": (float(kv_bytes(L70, 1, 2, "gqa")), 2 * L70["params"]),
        "dsv3_mha": (float(kv_bytes(V3, 1, 2, "mha_mla")), 2 * V3["total"]),
        "dsv3": (float(kv_bytes(V3, 1, 2, "mla")), 2 * V3["total"]),
        "oss_full": (float(kv_bytes(OSS, 1, 2, "gqa")), None),
    }
    out = dict(ctxs=ctxs, per_token={k: v[0] for k, v in rows.items()}, weights={k: v[1] for k, v in rows.items()})
    out["curve_llama70"] = kv_bytes(L70, ctxs, 2, "gqa")
    out["curve_llama70_mha"] = kv_bytes(L70, ctxs, 2, "mha")
    out["curve_dsv3"] = kv_bytes(V3, ctxs, 2, "mla")
    out["curve_dsv3_mha"] = kv_bytes(V3, ctxs, 2, "mha_mla")
    out["curve_oss"] = kv_bytes(OSS, ctxs, 2, "window")
    out["curve_oss_full"] = kv_bytes(OSS, ctxs, 2, "gqa")
    # the context at which one sequence's cache outweighs the model (16-bit weights)
    out["cross_llama70"] = 2 * L70["params"] / rows["llama70"][0]
    out["cross_llama70_mha"] = 2 * L70["params"] / rows["llama70_mha"][0]
    out["mla_ratio"] = rows["dsv3_mha"][0] / rows["dsv3"][0]
    out["gqa_ratio"] = rows["llama70_mha"][0] / rows["llama70"][0]
    out["mla_groups"] = (V3["kv_lora_rank"] + V3["rope_dim"]) / (2 * 128)  # DeepSeek-V2: like GQA with 2.25 groups
    # sliding windows and sparse attention: keys and values a decode step reads, per sequence, at each context
    G3 = F.GEMMA3
    out["read_full"] = kv_bytes(OSS, ctxs, 2, "gqa")
    out["read_oss"] = kv_bytes(OSS, ctxs, 2, "window")
    gem = dict(layers=6, kv_heads=OSS["kv_heads"], head_dim=OSS["head_dim"])  # Gemma 3's 5:1 pattern on gpt-oss sizes
    per = 2 * gem["kv_heads"] * gem["head_dim"] * 2 * OSS["layers"]
    out["read_gemma_pattern"] = per * (ctxs / 6 + 5 / 6 * np.minimum(ctxs, G3["window"]))
    out["read_dsa"] = kv_bytes(OSS, np.minimum(ctxs, F.DSV32["topk"]), 2, "gqa")  # top-2048 of the full cache
    # measured on our model: decode time against the cache it reads (phases)
    ph = load("phases")
    out["meas_ctx_bytes"] = np.asarray(ph["ctx_bytes"])
    out["meas_ctx_t"] = np.asarray(ph["ctx_t"])
    return out


# ---------------------------------------------------------------------------
# Batch size, speed per user, and cost
# ---------------------------------------------------------------------------
def roofline_step(N, W_bytes, kv_tok, L, attn_dim, ctx, B, peak, bw):
    """A decode step's time by the roofline: max(bytes moved / bandwidth, FLOPs / peak), for a batch of B sequences
    of ``ctx`` tokens.  FLOPs: 2N per token plus 4 * layers * (query heads x head dim) per cached position."""
    flops = 2.0 * N * B + 4.0 * L * attn_dim * ctx * B
    nbytes = W_bytes + kv_tok * ctx * B
    return np.maximum(nbytes / bw, flops / peak), flops, nbytes


def compute_economics():
    from videos.ai.ai17.specs import GPUS
    from videos.ai.ai19 import facts as F

    ph = load("phases")
    B = np.asarray(ph["decode_B"], float)
    t = np.asarray(ph["decode_t"])
    out = dict(meas_B=B, meas_user=1 / t, meas_total=B / t)
    H = GPUS["H100"]
    m = F.LLAMA31_8B
    kv_tok = 2 * m["layers"] * m["kv_heads"] * m["head_dim"] * 2
    W = 2 * m["params"]
    price = F.DSV32["gpu_hour"]  # USD per GPU-hour: the rental price DeepSeek costed its own service at
    cap = 0.9 * H["mem"]  # leave a tenth of the memory for activations and the rest
    out.update(price=price, kv_tok=kv_tok, weights=W, mem=H["mem"], peak=H["tensor"], bw=H["bw"])
    for ctx in (1024, 8192, 32768, 131072):
        bmax = int((cap - W) // (kv_tok * ctx))
        Bs = np.unique(np.concatenate([2 ** np.arange(0, 12), [bmax]]))
        Bs = Bs[(Bs >= 1) & (Bs <= bmax)].astype(float)
        tt, fl, nb = roofline_step(m["params"], W, kv_tok, m["layers"], m["heads"] * m["head_dim"], ctx, Bs,
                                   H["tensor"], H["bw"])
        tps = Bs / tt
        out[f"c{ctx}"] = plain(dict(B=Bs, t=tt, user=1 / tt, total=tps, cost=price / 3600 / tps * 1e6, bmax=bmax,
                                    mfu=fl / tt / H["tensor"], bwu=nb / tt / H["bw"]))
    # the batch at which the roofline model turns compute-bound (short contexts)
    out["ridge"] = H["tensor"] / H["bw"]
    return out


# ---------------------------------------------------------------------------
# Serving, simulated with this machine's measured costs
# ---------------------------------------------------------------------------
WORK = dict(n=400, p_med=200, o_med=100, seed=0)


def compute_serving():
    from videos.ai.ai19 import serve as S

    ph = load("phases")
    cost, err = S.fit_cost(ph)
    bmax = 32
    # load the server at ~70% of what continuous batching can sustain (a full batch, typical context)
    mean_out = 100 * math.exp(0.9 ** 2 / 2)
    step = cost.step(bmax, bmax * 260, 0)
    cap_rps = bmax / step / mean_out
    rate = round(0.7 * cap_rps, 1)
    reqs = S.workload(WORK["n"], rate, WORK["seed"], WORK["p_med"], WORK["o_med"])
    out = dict(cost=[cost.a, cost.b, cost.c, cost.p], fit_err=err, rate=rate, bmax=bmax, cap_rps=cap_rps,
               prompt_mean=float(np.mean([r.prompt for r in reqs])), out_mean=float(np.mean([r.out for r in reqs])))
    runs = {"static": S.run_static(reqs, cost, bmax), "continuous": S.run_continuous(reqs, cost, bmax),
            "chunked": S.run_continuous(reqs, cost, bmax, chunk=256)}
    out["one"] = plain({k: S.metrics(v) for k, v in runs.items()})
    # the picture: eight slots, a burst of requests, both ways (the first seconds)
    small = S.workload(40, 2 * rate, 3, WORK["p_med"], WORK["o_med"])
    tr_s, tr_c = [], []
    S.run_static(small, cost, 8, trace=tr_s)
    S.run_continuous(small, cost, 8, trace=tr_c)
    out["gantt_static"] = np.array([(a, b, c, ["prefill", "decode", "idle"].index(k), r) for a, b, c, k, r in tr_s])
    out["gantt_cont"] = np.array([(a, b, c, ["prefill", "decode", "idle"].index(k), r) for a, b, c, k, r in tr_c])
    out["gantt_arrive"] = np.array([r.arrive for r in small])
    # four workers: each one doing everything, against one prefilling and three decoding
    rate4 = round(4 * 0.6 * cap_rps, 1)
    reqs4 = S.workload(WORK["n"] * 2, rate4, WORK["seed"] + 1, WORK["p_med"], WORK["o_med"])
    co, ch = [], []
    for part in S.split_round_robin(reqs4, 4):
        co += S.run_continuous(part, cost, bmax * 2)
        ch += S.run_continuous(part, cost, bmax * 2, chunk=256)
    dis = S.run_disaggregated(reqs4, cost, bmax * 2, 10e9, ph["kv_per_token"], n_dec=3)
    out["rate4"] = rate4
    out["four"] = plain({"colocated": S.metrics(co), "chunked": S.metrics(ch), "disaggregated": S.metrics(dis)})
    out["gap_hist"] = plain({k: np.histogram(np.concatenate([r.gaps for r in v if r.gaps]) * 1e3, bins=40,
                                       range=(0, 80))[0] for k, v in (("colocated", co), ("disaggregated", dis))})
    one = out["one"]
    print(f"    rate {rate}/s: throughput static {one['static']['throughput']:.0f}, continuous "
          f"{one['continuous']['throughput']:.0f} tokens/s; ttft p50 {one['static']['ttft'][0]:.2f} vs "
          f"{one['continuous']['ttft'][0]:.3f} s", flush=True)
    return out


def compute_paging():
    from videos.ai.ai19 import serve as S
    from videos.ai.ai19 import facts as F

    ph = load("phases")
    cost, _ = S.fit_cost(ph)
    pool, max_len = 16384, 2048
    reqs = S.workload(400, 30.0, 1, p_med=200, o_med=150)  # more demand than the memory allows: it is the limit
    out = dict(pool=pool, max_len=max_len, block=F.VLLM["block"])
    for mode in ("reserve", "contiguous", "paged"):
        rr, ser, pre, snap = S.memory_sim(reqs, cost, pool, mode, block=16, max_len=max_len, snap_t=10.0)
        m = S.metrics(rr)
        out[mode] = plain(dict(throughput=m["throughput"], running=float(ser[:, 1].mean()),
                               used=float(ser[:, 2].mean() / pool), alloc=float(ser[:, 3].mean() / pool),
                               preempted=pre, ttft=m["ttft"], latency=m["latency"]))
        out[f"snap_{mode}"] = np.array(snap)
        out[f"series_{mode}"] = ser[:: max(1, len(ser) // 400)]
    blocks = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    out["blocks"] = blocks
    out["block_waste"] = S.block_waste([r.prompt + r.out for r in reqs], blocks)
    out["lengths"] = np.array([r.prompt + r.out for r in reqs])
    # shared prefixes: multi-turn conversations with one system prompt
    order, sys_t = S.chat_workload()
    caps = [0, 1024, 4096, 16384, 65536, 10 ** 9]
    out["prefix_caps"] = caps
    out["prefix"] = plain([S.prefix_sim(order, c) for c in caps])
    out["prefix_system"] = len(sys_t)
    out["prefix_full_t"], out["prefix_suffix_t"] = ph["prefix_full_t"], ph["prefix_suffix_t"]
    print(f"    concurrent: reserve {out['reserve']['running']:.1f}, paged {out['paged']['running']:.1f}; "
          f"prefix cache saves {100 * out['prefix'][-1]['saved']:.0f}% of prefill", flush=True)
    return out


# ---------------------------------------------------------------------------
# Speculative decoding: exact, and how fast
# ---------------------------------------------------------------------------
def compute_exact():
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai19 import spec as SP

    threads(2)
    # (1) one character of Part 13's transformer, drafted by a counting model on the last two characters
    c13.load("tf")
    model, chars, enc, data = c13.load_tf()
    K = len(chars)
    tr, ps = data["train"].numpy(), data["passage"]
    idx = tr[:-2] * K * K + tr[1:-1] * K + tr[2:]
    counts = np.bincount(idx, minlength=K ** 3).reshape(K, K, K).astype(np.float64) + 0.05
    draft_p = counts / counts.sum(-1, keepdims=True)
    g = rng(2023)  # Leviathan, Kalman & Matias; Chen et al. (2023)

    def target_probs(ctx):
        with torch.no_grad():
            return torch.softmax(model(ctx[None, -c13.CTX:])[0], -1).numpy().astype(np.float64)

    for _ in range(400):  # a place where the big model hesitates, so the comparison has something to show
        s0 = int(g.integers(c13.CTX, len(ps) - 10))
        ctx = ps[s0 - c13.CTX:s0]
        p = target_probs(ctx)[-1]
        if p.max() < 0.4 and np.sort(p)[-8:].sum() > 0.7:
            break
    q = draft_p[tuple(ctx[-2:].numpy())]
    q = q / q.sum()
    N = 200_000
    x = g.choice(K, N, p=q)
    acc = g.random(N) < np.minimum(1, p[x] / q[x])
    resid = np.maximum(p - q, 0)
    resid /= resid.sum()
    y = np.where(acc, x, g.choice(K, N, p=resid))
    emp = np.bincount(y, minlength=K) / N
    direct = np.bincount(g.choice(K, N, p=p), minlength=K) / N
    top = np.argsort(-p)[:8]
    out = dict(N=N, tv=0.5 * float(np.abs(emp - p).sum()), tv_direct=0.5 * float(np.abs(direct - p).sum()),
               tv_draft=0.5 * float(np.abs(q - p).sum()), beta=float(np.minimum(p, q).sum()), p_top=p[top],
               q_top=q[top], emp_top=emp[top], top_chars=[chars[int(i)] for i in top],
               context="".join(chars[int(i)] for i in ctx[-60:]))
    # (2) two tokens of the novels model, drafted by our small model, checked jointly
    base_m = base()
    d = load("drafters")  # the draft model is trained there
    draft = SP.load_draft(CACHE.dir)
    from videos.ai.ai19.engine import heldout

    w = heldout(64, 96)
    best = None
    with torch.inference_mode():  # a held-out context where the first token is uncertain
        for i in range(len(w)):
            pz = torch.softmax(base_m(w[i:i + 1, :64])[0, -1].double(), -1)
            if pz.max() < 0.35 and (best is None or pz.max() > best[0]):
                best = (float(pz.max()), i)
    ctx2 = w[best[1], :64].tolist()
    jt = SP.joint_test(base_m, draft, ctx2, N=60_000, seed=19)
    from explainer.ai import novels as NV

    jt["context"] = NV.decode(ctx2[-24:])
    jt["top_text"] = [[NV.decode([a]), NV.decode([b])] for a, b in jt["top"]]
    out["joint"] = plain(jt)
    out["drafter_alpha"] = d["draft"]["evals"][-1][2]
    print(f"    one char: TV {out['tv']:.4f} (direct sampling {out['tv_direct']:.4f}); two tokens: spec "
          f"{jt['tv_spec']:.3f}, direct {jt['tv_direct']:.3f}, unchecked {jt['tv_naive']:.3f}", flush=True)
    return out


SPEC_K = [1, 2, 3, 4, 6]


def compute_drafters():
    """Train both drafters (resumably), then run speculative decoding with each on held-out openings."""
    import torch

    from videos.ai.ai19 import spec as SP
    from videos.ai.ai19.engine import heldout, interleaved_min, loadavg

    threads(2)
    base_m = base()
    for p in base_m.parameters():
        p.requires_grad_(False)
    ev = heldout(8, 256, seed=0)
    part = CACHE.partial("drafters", dict(draft=SP.DRAFT_RUN, eagle=SP.EAGLE_RUN, cfg=SP.DRAFT_CFG, k=SPEC_K, v=2))
    if "draft" not in part or not (CACHE.dir / "draft.pt").exists():
        part["draft"] = plain(SP.train_draft(CACHE.dir, base_m, ev))
    if "eagle" not in part or not (CACHE.dir / "eagle.pt").exists():
        part["eagle"] = plain(SP.train_eagle(CACHE.dir, base_m, ev))
    draft, eagle = SP.load_draft(CACHE.dir), SP.load_eagle(CACHE.dir, base_m)
    threads(1)  # time on one thread, like the rest of the part
    dec = SP.Decoder(base_m, draft, eagle, max_len=320)
    prompts = [w[:48].tolist() for w in heldout(12, 64, seed=0)]
    n_new = 96
    configs = [("plain", 0, 1.0)] + [(m, k, 1.0) for m in ("draft", "eagle") for k in SPEC_K] + \
              [("draft", 4, 0.0), ("eagle", 4, 0.0), ("plain", 0, 0.0)]
    if "runs" not in part:
        res = {}
        for mode, k, temp in configs:
            toks, rounds, betas = 0, [], []
            for j, pr in enumerate(prompts):
                if mode == "plain":
                    o = dec.plain(pr, n_new, temp=temp, seed=j)
                else:
                    o, rr, bb = dec.speculative(pr, n_new, k, temp=temp, seed=j, mode=mode)
                    rounds += rr
                    betas += bb
                toks += len(o)
            key = f"{mode}_{k}_{temp:g}"
            res[key] = dict(tokens=toks, rounds=len(rounds), accepted=[a for _, a in rounds],
                            beta=float(np.mean(betas)) if betas else 1.0)
        part["runs"] = res
    if "timing" not in part:
        # time per token, each configuration timed in turn (interleaved), the fastest of several rounds
        sub = prompts[:4]
        la = loadavg()

        def gen(c):
            mode, k, temp = c
            for j, pr in enumerate(sub):
                if mode == "plain":
                    dec.plain(pr, n_new, temp=temp, seed=j)
                else:
                    dec.speculative(pr, n_new, k, temp=temp, seed=j, mode=mode)

        tc = [("plain", 0, 1.0)] + [(m, k, 1.0) for m in ("draft", "eagle") for k in (1, 2, 4, 6)]
        r = interleaved_min(tc, gen, rounds=5, min_time=0.0)
        part["timing"] = dict(configs=[list(c) for c in tc], t=[r[c][0] for c in tc], tmed=[r[c][1] for c in tc],
                              tokens=len(sub) * n_new, loadavg=la)
    # costs of the pieces on this machine: a check of k + 1 tokens against one step
    E = dec.E
    with torch.inference_mode():
        c = E.new_cache(1, 320, fill=True)
        dc = dec.D.new_cache(1, 320, fill=True)

        def piece(kk):
            what, n = kk
            if what == "target":
                c.len = 100
                E.forward(torch.zeros(1, n, dtype=torch.long), c, logits="last")
            else:
                dc.len = 100
                dec.D.forward(torch.zeros(1, n, dtype=torch.long), dc, logits="last")

        pk = [("target", n) for n in (1, 2, 3, 4, 5, 7)] + [("draft", 1)]
        r = interleaved_min(pk, piece, rounds=9, min_time=0.05)
    out = dict(draft=plain(part["draft"]), eagle=plain(part["eagle"]), runs=plain(part["runs"]),
               timing=plain(part["timing"]), k=SPEC_K,
               n_new=n_new, n_prompts=len(prompts),
               piece_target=[r[("target", n)][0] for n in (1, 2, 3, 4, 5, 7)], piece_n=[1, 2, 3, 4, 5, 7],
               piece_draft=r[("draft", 1)][0])
    for m in ("draft", "eagle"):
        a = part[m]["evals"][-1][2]
        out[f"alpha_{m}"] = a
    return out


# ---------------------------------------------------------------------------
# Quantization
# ---------------------------------------------------------------------------
def _setup_quant(n_eval=48):
    from videos.ai.ai19.engine import heldout

    threads(2)
    m = base()
    for p in m.parameters():
        p.requires_grad_(False)
    return m, heldout(n_eval, 256)


def compute_rounding():
    from videos.ai.ai19 import quant as Q
    from videos.ai.ai19.engine import loss

    model, ev = _setup_quant()
    names = Q.linear_names(model)
    Ws = {n: model.get_submodule(n).weight.detach().numpy().astype(np.float64) for n in names}
    part = CACHE.partial("rounding", dict(v=1))
    if "fp32" not in part:
        part["fp32"] = loss(model, ev)
    grans = ["tensor", "row", 64, 32]
    bitlist = [2, 3, 4, 5, 6, 8]
    for gname in grans:
        for b in bitlist:
            key = f"{gname}_{b}"
            if key not in part:
                part[key] = loss(Q.weight_only(model, lambda n, W: Q.rtn(W, b, gname)), ev)
                print(f"    {key}: {part[key]:.4f}", flush=True)
    out = dict(fp32=part["fp32"], grans=[str(g) for g in grans], bits=bitlist,
               loss={str(g): [part[f"{g}_{b}"] for b in bitlist] for g in grans})
    # the error against Delta^2 / 12, all block weights, per row and per tensor
    for gname in ("row", "tensor", 64):
        meas, pred = [], []
        for b in range(2, 9):
            e2 = sum(float(((W - Q.rtn(W, b, gname)) ** 2).sum()) for W in Ws.values())
            d2 = sum(float((Q.scales_of(W, b, gname) ** 2).sum()) / 12 for W in Ws.values())
            meas.append(e2)
            pred.append(d2)
        nw = sum(W.size for W in Ws.values())
        out[f"mse_{gname}"] = np.array(meas) / nw
        out[f"pred_{gname}"] = np.array(pred) / nw
    out["mse_bits"] = list(range(2, 9))
    out["bpw"] = {str(g): [Q.bits_per_weight(b, g, 256) for b in bitlist] for g in grans}
    # one layer's weights and the levels of 4 bits with one scale for the whole tensor and one per row
    W = Ws["blocks.2.mlp.down"]
    h, e = np.histogram(W.ravel(), bins=90)
    out.update(hist=h, hist_edges=e, hist_layer="blocks.2.mlp.down", hist_amax=float(np.abs(W).max()),
               row_amax=np.abs(W).max(1), n_weights=int(sum(W.size for W in Ws.values())))
    out["row_example"] = W[0, :48]
    out["row_example_q"] = Q.rtn(W, 4, "row")[0, :48]
    return out


def compute_outliers():
    import torch

    from videos.ai.ai19 import quant as Q
    from videos.ai.ai19.engine import calibration, loss

    model, ev = _setup_quant()
    cal = calibration(32, seed=1)
    stats = Q.collect(model, cal)
    names = Q.linear_names(model)
    ratio = {n: float(stats[n]["amax"].max() / np.median(stats[n]["amax"])) for n in names}
    worst = max(names, key=lambda n: ratio[n])
    # the residual stream between blocks: its channels' largest values
    resid = []

    def hook(_m, _i, o):
        resid.append(o.detach().abs().reshape(-1, o.shape[-1]).amax(0).numpy())

    hs = [b.register_forward_hook(hook) for b in model.blocks]
    with torch.inference_mode():
        model(cal[:8, :-1])
    for h in hs:
        h.remove()
    part = CACHE.partial("outliers", dict(v=1))
    if "fp32" not in part:
        part["fp32"] = loss(model, ev)
    for ab in (8, 6, 4):
        for method in ("plain", "smooth", "keep"):
            key = f"w8a{ab}_{method}"
            if key not in part:
                part[key] = loss(Q.w_a(model, 8, ab, stats, method=method), ev)
                print(f"    {key}: {part[key]:.4f}", flush=True)
    out = dict(fp32=part["fp32"], loss={k: part[k] for k in part.done if k.startswith("w8")}, ratio=ratio, worst=worst,
               profile=stats[worst]["amax"], profile_qkv=stats["blocks.0.attn.qkv"]["amax"],
               profile_down=stats["blocks.5.mlp.down"]["amax"], resid=np.array(resid))
    out["names"] = names
    # SmoothQuant's scales on the worst layer: activations' and weights' ranges before and after
    W = model.get_submodule(worst).weight.detach().numpy().astype(np.float64)
    s = Q.smooth_scales(stats[worst]["amax"], W, 0.5)
    out.update(sq_act_before=stats[worst]["amax"], sq_act_after=stats[worst]["amax"] / s,
               sq_w_before=np.abs(W).max(0), sq_w_after=np.abs(W * s).max(0))
    return out


def compute_gptq():
    from videos.ai.ai19 import quant as Q
    from videos.ai.ai19.engine import calibration, loss

    model, ev = _setup_quant()
    names = Q.linear_names(model)
    Ws = {n: model.get_submodule(n).weight.detach().numpy().astype(np.float64) for n in names}
    part = CACHE.partial("gptq", dict(v=1))
    if "fp32" not in part:
        part["fp32"] = loss(model, ev)
    for b in (4, 3):
        for gname in ("row", 64):
            key = f"rtn_{b}_{gname}"
            if key not in part:
                part[key] = loss(Q.weight_only(model, lambda n, W: Q.rtn(W, b, gname)), ev)
    seeds = (1, 2, 3)
    for sd in seeds:
        stats = None
        for b in (4, 3):
            for gname in ("row", 64):
                for meth in ("gptq", "awq"):
                    key = f"{meth}_{b}_{gname}_s{sd}"
                    if key in part:
                        continue
                    if stats is None:
                        stats = Q.collect(model, calibration(32, seed=sd))
                    if meth == "gptq":
                        fn = lambda n, W: Q.gptq(W, stats[n]["H"], b, gname)  # noqa: E731
                        part[key] = loss(Q.weight_only(model, fn), ev)
                    else:
                        alphas = {}

                        def fn(n, W):
                            Wq, a = Q.awq(W, stats[n]["H"], stats[n]["amean"], b, gname)
                            alphas[n] = a
                            return Wq

                        part[key] = loss(Q.weight_only(model, fn), ev)
                        part[key + "_alpha"] = float(np.mean(list(alphas.values())))
                    print(f"    {key}: {part[key]:.4f}", flush=True)
    out = dict(fp32=part["fp32"], seeds=list(seeds), res={k: v for k, v in part.done.items()})
    # one layer, at 3 bits: the output error on the calibration inputs, for each method
    stats = Q.collect(model, calibration(32, seed=1))
    lay = "blocks.1.attn.qkv"
    W, H = Ws[lay], stats[lay]["H"]
    out["layer"] = lay
    out["layer_err"] = {f"{m}_{b}": Q.out_err(W, Q.rtn(W, b) if m == "rtn" else Q.gptq(W, H, b) if m == "gptq" else
                                             Q.awq(W, H, stats[lay]["amean"], b)[0], H)
                        for m in ("rtn", "gptq", "awq") for b in (4, 3)}
    out["layer_err_all"] = {n: [Q.out_err(Ws[n], Q.rtn(Ws[n], 3), stats[n]["H"]),
                                Q.out_err(Ws[n], Q.gptq(Ws[n], stats[n]["H"], 3), stats[n]["H"])] for n in names}
    # one row of 16 weights, GPTQ step by step (its inputs' second moment restricted to those 16 inputs)
    w16, H16 = W[:4, :16], H[:16, :16]
    Qr, trace = Q.gptq(w16, H16, 3, "row", trace_row=0)
    out.update(trace=trace, trace_w=w16[0], trace_q=Qr[0], trace_rtn=Q.rtn(w16, 3)[0],
               trace_err_rtn=Q.out_err(w16[:1], Q.rtn(w16, 3)[:1], H16), trace_err_gptq=Q.out_err(w16[:1], Qr[:1], H16))
    return out


def compute_rotation():
    import torch

    from videos.ai.ai19 import quant as Q
    from videos.ai.ai19.engine import calibration, loss

    model, ev = _setup_quant()
    d = model.cfg.d
    hid = model.cfg.hidden
    g = rng(19)
    Hd = Q.hadamard(d) * g.choice([-1.0, 1.0], d)[:, None]  # a randomized Hadamard: random signs, then Hadamard
    Rd = Q.random_orthogonal(hid, 7)  # the down projection's input (688 is no power of two): a random rotation
    rot = Q.rotate(model, Hd)
    with torch.inference_mode():
        x = calibration(2, seed=5)[:, :-1]
        same = float((rot(x) - model(x)).abs().max())  # computational invariance
    cal = calibration(32, seed=1)
    stats = Q.collect(model, cal)
    # how peaked the inputs of the first block's attention are, before and after the rotation
    acts = {}

    def grab(name):
        def f(_m, inp, _o):
            acts[name] = inp[0].detach().reshape(-1, inp[0].shape[-1]).numpy()
        return f

    with torch.inference_mode():
        h1 = model.blocks[3].attn.qkv.register_forward_hook(grab("orig"))
        model(cal[:2, :-1])
        h1.remove()
        h2 = rot.blocks[3].attn.qkv.register_forward_hook(grab("rot"))
        rot(cal[:2, :-1])
        h2.remove()
    out = dict(invariance=same, crest=Q.crest(acts["orig"]), crest_rot=Q.crest(acts["rot"]),
               act_row=acts["orig"][100], act_row_rot=acts["rot"][100])
    part = CACHE.partial("rotation", dict(v=1))
    if "fp32" not in part:
        part["fp32"] = loss(model, ev)
    jobs = {
        "w4a4_plain": lambda: Q.w_a(model, 4, 4),
        "w4a4_smooth": lambda: Q.w_a(model, 4, 4, stats, method="smooth"),
        "w4a4_hadamard": lambda: Q.w_a(rot, 4, 4, down_R=Rd),
        "w4a8_plain": lambda: Q.w_a(model, 4, 8),
        "w4a8_hadamard": lambda: Q.w_a(rot, 4, 8, down_R=Rd),
        "w4a16_plain": lambda: Q.w_a(model, 4, 0),
        "w4a16_hadamard": lambda: Q.w_a(rot, 4, 0, down_R=Rd),
    }
    for sd in (11, 12, 13):
        jobs[f"w4a4_random{sd}"] = (lambda sd=sd: Q.w_a(Q.rotate(model, Q.random_orthogonal(d, sd)), 4, 4, down_R=Rd))
    for k, fn in jobs.items():
        if k not in part:
            part[k] = loss(fn(), ev)
            print(f"    {k}: {part[k]:.4f}", flush=True)
    # SpinQuant, small: learn the residual rotation R = R0 cayley(A) by gradient descent on the quantized model's loss
    if "spin" not in part:
        part["spin"] = plain(_learn_rotation(model, Hd, Rd, ev, steps=100))
    Rl = np.asarray(part["spin"]["R"])
    if "w4a4_learned" not in part:
        part["w4a4_learned"] = loss(Q.w_a(Q.rotate(model, Rl), 4, 4, down_R=Rd), ev)
    out.update(fp32=part["fp32"], loss={k: v for k, v in part.done.items() if k.startswith("w4")},
               spin={k: v for k, v in part["spin"].items() if k != "R"})
    return out


def _learn_rotation(model, R0, Rd, ev, steps=100, lr=3e-4, batch=8, bits=4):
    """SpinQuant, small (Liu et al. 2024): R = R0 C(A), C the Cayley map of a skew-symmetric A (so R stays a rotation),
    trained by Adam on the loss of the network with weights and activations rounded to ``bits`` (the rounding passed
    straight through for the gradient), on calibration windows.  Every 20 steps, the held-out loss of that rotation."""
    import torch
    import torch.nn.functional as F_

    from explainer.lm import pocket
    from videos.ai.ai19 import quant as Q
    from videos.ai.ai19.engine import calibration, loss

    torch.manual_seed(0)
    fm = Q.fold_norms(model)
    d = fm.cfg.d
    A = torch.zeros(d, d, requires_grad=True)
    opt = torch.optim.Adam([A], lr=lr)
    R0t, Rdt = torch.as_tensor(R0, dtype=torch.float32), torch.as_tensor(Rd, dtype=torch.float32)
    I = torch.eye(d)
    cal = calibration(64, seed=2)
    g = torch.Generator().manual_seed(0)
    fw, fa = Q.fake_w, Q.fake_act

    def rotation():
        S = A - A.T
        return R0t @ torch.linalg.solve(I + S, I - S)

    def forward(x, R):
        h = fm.emb(x) @ R
        for b in fm.blocks:
            a = b.attn
            B, T, D = h.shape
            u = b.n1(h)
            qkv = fa(u, bits) @ fw(a.qkv.weight @ R, bits).T
            q, k, v = qkv.view(B, T, 3, a.h, a.hd).permute(2, 0, 3, 1, 4)
            q, k = pocket.apply_rope(q, a.cos, a.sin), pocket.apply_rope(k, a.cos, a.sin)
            y = F_.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, D)
            h = h + fa(y, bits) @ fw(R.T @ a.out.weight, bits).T
            u = b.n2(h)
            gt = fa(u, bits) @ fw(b.mlp.gate.weight @ R, bits).T
            up = fa(u, bits) @ fw(b.mlp.up.weight @ R, bits).T
            z = (F_.silu(gt) * up) @ Rdt
            h = h + fa(z, bits) @ fw(R.T @ b.mlp.down.weight @ Rdt, bits).T
        return (fm.norm(h) @ (fm.head.weight @ R).T)

    curve, evals = [], []
    t0 = time.time()
    for step in range(steps + 1):
        if step % 20 == 0 or step == steps:
            with torch.no_grad():
                Rn = rotation().numpy().astype(np.float64)
            evals.append([step, loss(Q.w_a(Q.rotate(model, Rn), bits, bits, down_R=Rd), ev[:16])])
            print(f"    rotation step {step}: held-out loss {evals[-1][1]:.4f} ({time.time() - t0:.0f}s)", flush=True)
        if step == steps:
            break
        ix = torch.randint(0, len(cal), (batch,), generator=g)
        w = cal[ix]
        logits = forward(w[:, :-1], rotation())
        l_ = F_.cross_entropy(logits.reshape(-1, logits.shape[-1]), w[:, 1:].reshape(-1))
        opt.zero_grad()
        l_.backward()
        opt.step()
        curve.append([step, float(l_.detach())])
    with torch.no_grad():
        R = rotation().numpy().astype(np.float64)
    orth = float(np.abs(R @ R.T - np.eye(d)).max())
    return dict(curve=curve, evals=evals, R=R, orth_err=orth, steps=steps, lr=lr, batch=batch,
                seconds=time.time() - t0, moved=float(np.linalg.norm(R - R0) / np.linalg.norm(R0)))


def compute_formats():
    from videos.ai.ai19 import formats as FM
    from videos.ai.ai19 import quant as Q
    from videos.ai.ai19.engine import loss

    model, ev = _setup_quant()
    names = Q.linear_names(model)
    Ws = {n: model.get_submodule(n).weight.detach().numpy().astype(np.float64) for n in names}
    part = CACHE.partial("formats", dict(v=1))
    if "fp32" not in part:
        part["fp32"] = loss(model, ev)
    jobs = {"int4_row": lambda W: Q.rtn(W, 4, "row"), "int4_g32": lambda W: FM.int4_scaled(W, 32, "fp16"),
            "int4_g16e4m3": lambda W: FM.int4_scaled(W, 16, "e4m3"), "mxfp4": FM.mxfp4, "nvfp4": FM.nvfp4,
            "int3_row": lambda W: Q.rtn(W, 3, "row")}
    for k, fn in jobs.items():
        if k not in part:
            part[k] = loss(Q.weight_only(model, lambda n, W: fn(W)), ev)
            print(f"    {k}: {part[k]:.4f}", flush=True)
    bpw = dict(int4_row=4 + 16 / 256, int4_g32=4 + 16 / 32, int4_g16e4m3=4 + 8 / 16, mxfp4=4 + 8 / 32,
               nvfp4=4 + 8 / 16, int3_row=3 + 16 / 256)
    # relative error of every format on all the weights, and how often MXFP4 clamps a block's largest value
    rel = {}
    allW = np.concatenate([W.ravel() for W in Ws.values()])
    for k, fn in jobs.items():
        err = np.concatenate([(fn(W) - W).ravel() for W in Ws.values()])
        rel[k] = float(np.sqrt((err ** 2).mean() / (allW ** 2).mean()))
    clipped = np.concatenate([FM.mxfp4(W, detail=True)[1]["clipped"] for W in Ws.values()])
    # one block of 32 weights, bit by bit, both ways
    lay = "blocks.3.attn.qkv"
    W = Ws[lay]
    pick = int(np.argmax([FM.mxfp4(W[r:r + 1, :32], detail=True)[1]["clipped"][0] for r in range(W.shape[0])]))
    pick = 0 if pick < 0 else pick
    blk = W[pick, :32]
    mx, dm = FM.mxfp4(blk[None], detail=True)
    nv, dn = FM.nvfp4(W, detail=True)
    rowblocks = W.shape[1] // 16
    nvb = nv[pick, :16]
    g_ = float(dn["tensor_scale"])
    s16 = float(dn["block_scale"][pick * rowblocks])
    out = dict(fp32=part["fp32"], loss={k: part[k] for k in jobs}, bpw=bpw, rel=rel, clipped_share=float(clipped.mean()),
               layer=lay, row=pick, block=blk, mx_shared_exp=int(dm["shared_exp"][0]),
               mx_scale_bits=FM.bits(int(dm["shared_exp"][0]) + 127, 8),
               mx_codes=[FM.bits(c, 4) for c in dm["codes"][0]], mx_values=mx[0], mx_clipped=bool(dm["clipped"][0]),
               nv_tensor_scale=g_, nv_block_scale=s16, nv_scale_bits=FM.e4m3_bits(s16),
               nv_codes=[FM.bits(c, 4) for c in dn["codes"][pick * rowblocks]], nv_values=nvb)
    # gpt-oss-120b: its expert weights in MXFP4, the rest in 16 bits (model card, Table 1)
    from videos.ai.ai19 import facts as F

    o = F.GPT_OSS_120B
    out["oss_bytes"] = o["mlp"] * o["mxfp4_bits"] / 8 + (o["attn"] + o["embed"]) * 2
    out["oss_bf16"] = o["total"] * 2
    return out


def compute_kvquant():
    import torch

    from videos.ai.ai19 import quant as Q
    from videos.ai.ai19.engine import Engine, heldout, loss

    threads(2)
    model = base()
    ev = heldout(32, 256)
    dh = model.cfg.d // model.cfg.heads
    Hh = torch.as_tensor(Q.hadamard(dh), dtype=torch.float32)

    def make(method, bits):
        q = 2 ** (bits - 1) - 1

        def per_token(x):
            s = x.abs().amax(-1, keepdim=True).clamp_min(1e-8) / q
            return torch.clamp(torch.round(x / s), -q - 1, q) * s

        def per_channel(x, G=32):  # along tokens, in groups of G, a scale per channel (KIVI's keys)
            B, H, T, D = x.shape
            pad = (-T) % G
            xp = torch.nn.functional.pad(x, (0, 0, 0, pad))
            xg = xp.view(B, H, (T + pad) // G, G, D)
            s = xg.abs().amax(3, keepdim=True).clamp_min(1e-8) / q
            return (torch.clamp(torch.round(xg / s), -q - 1, q) * s).view(B, H, T + pad, D)[:, :, :T]

        def fp8(x):
            s = x.abs().amax(-1, keepdim=True).clamp_min(1e-8) / 448.0
            return (x / s).to(torch.float8_e4m3fn).to(torch.float32) * s

        def f(x, which, layer):
            if method == "token":
                return per_token(x)
            if method == "kivi":
                return per_channel(x) if which == "k" else per_token(x)
            if method == "rot":
                return per_token(x @ Hh) @ Hh.T
            if method == "fp8":
                return fp8(x)
            raise ValueError(method)
        return f

    part = CACHE.partial("kvquant", dict(v=1))
    if "fp32" not in part:
        part["fp32"] = loss(Engine(model), ev)
    keys = [("token", b) for b in (8, 4, 3, 2)] + [("kivi", b) for b in (4, 3, 2)] + [("rot", b) for b in (4, 3, 2)]
    keys += [("fp8", 8)]
    for meth, b in keys:
        k = f"{meth}_{b}"
        if k not in part:
            part[k] = loss(Engine(model, kv_quant=make(meth, b)), ev)
            print(f"    kv {k}: {part[k]:.4f}", flush=True)
    # what the keys and values look like: one head's magnitudes, tokens by channels
    seen = {}

    def grab(x, which, layer):
        seen[(which, layer)] = x[0].abs().numpy()
        return x

    with torch.inference_mode():
        Engine(model, kv_quant=grab).full(ev[:1, :-1])
    chan = {l: float(seen[("k", l)].mean(1).max(-1).max() / np.median(seen[("k", l)].mean(1))) for l in range(6)}
    lay = max(chan, key=chan.get)
    head = int(np.argmax(seen[("k", lay)].mean(1).max(-1)))
    out = dict(fp32=part["fp32"], loss={k: v for k, v in part.done.items() if k != "fp32"}, layer=lay, head=head,
               k_map=seen[("k", lay)][head][:96], v_map=seen[("v", lay)][head][:96], chan_ratio=chan,
               kv_bits_fp32=32)
    return out


# ---------------------------------------------------------------------------
# FlashAttention and Flash-Decoding
# ---------------------------------------------------------------------------
def compute_flash():
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai19 import attn as A
    from videos.ai.ai19 import facts as F

    threads(2)
    c13.load("tf")
    model, chars, enc, data = c13.load_tf()
    x = data["passage"][:c13.CTX][None]
    layer, head = 1, 0
    with torch.no_grad():  # the real queries, keys and values of one head of Part 13's transformer
        T = x.shape[1]
        th = torch.tensor(c13.rope_freqs(), dtype=torch.float32)
        ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
        cos, sin = torch.cos(ang), torch.sin(ang)
        h = model.emb(x)
        for b in model.blocks[:layer]:
            h = b(h, cos, sin)[0]
        b = model.blocks[layer]
        q, k, v = b.qkv(b.n1(h)).view(1, T, 3, c13.HEADS, c13.DH).permute(2, 0, 3, 1, 4)

        def rot(t):
            a, bb = t[..., : c13.DH // 2], t[..., c13.DH // 2:]
            return torch.cat([a * cos - bb * sin, a * sin + bb * cos], -1)

        q, k = rot(q), rot(k)
    Q_, K_, V_ = (t[0, head].double().numpy() for t in (q, k, v))
    ref = A.plain_attention(Q_, K_, V_)
    tiled = A.flash_attention(Q_, K_, V_, 32, 32)
    row = 200
    s = Q_[row, :row + 1] @ K_[:row + 1].T / math.sqrt(Q_.shape[1])
    trace, sm = A.online_softmax_trace(s, 32)
    out = dict(T=T, d=int(Q_.shape[1]), dev=float(np.abs(tiled - ref).max()), row=row, scores=s, trace=trace,
               softmax=sm, softmax_dev=float(np.abs(sm - A.softmax_rows(s[None])[0]).max()),
               tf32_dev=float(np.abs(A.flash_attention(Q_.astype(np.float32), K_.astype(np.float32),
                                                       V_.astype(np.float32), 32, 32) - ref).max()))
    # Flash-Decoding: the last query against all the keys, in 8 chunks, combined
    o, parts = A.split_kv_decode(Q_[-1], K_, V_, 8)
    out["split_dev"] = float(np.abs(o - ref[-1]).max())
    out["split_m"] = [float(m) for m, _, _ in parts]
    out["split_l"] = [float(l_) for _, l_, _ in parts]
    # memory traffic for one head, 16-bit numbers, H100's shared memory per SM as the fast memory
    M = F.H100_SMEM // 2
    Ns = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
    for d in (64, 128):
        out[f"io_std_{d}"] = [A.io_standard(N, d) for N in Ns]
        out[f"io_flash_{d}"] = [A.io_flash_formula(N, d, M) for N in Ns]
        out[f"io_count_{d}"] = [A.io_flash_counted(N, d, M) for N in Ns[:6]]
        out[f"blocks_{d}"] = list(A.flash_blocks(M, d))
    out.update(Ns=Ns, M=M)
    assert out["io_count_128"] == out["io_flash_128"][:6] and out["dev"] < 1e-10 and out["split_dev"] < 1e-10
    # how much of an H100 a decode step's attention can use: blocks of work per (sequence, head, split)
    out["occ_heads"] = 32  # Llama 3.1 8B's query heads
    out["occ_splits"] = [1, 2, 4, 8, 16]
    out["occ"] = [A.occupancy(1 * 32 * sp, F.H100_SMS) for sp in out["occ_splits"]]
    out["occ_b8"] = [A.occupancy(8 * 32 * sp, F.H100_SMS) for sp in out["occ_splits"]]
    return out


# ---------------------------------------------------------------------------
# Constrained decoding
# ---------------------------------------------------------------------------
def compute_grammar():
    import torch

    from explainer.ai import novels as NV
    from videos.ai.ai13 import compute as c13
    from videos.ai.ai19 import grammar as G
    from videos.ai.ai19.engine import Engine

    threads(1)
    model = base()
    eng = Engine(model, max_len=512)
    auto = G.Automaton(G.RECORD)
    t0 = time.time()
    strings = G.token_strings()
    index, order = G.build_index(auto, strings)
    t_index = time.time() - t0
    pid = NV.encode(G.PROMPT)
    nl = {i for i, s in enumerate(strings) if s and "\n" in s}
    n = 200
    un, co = [], []
    t0 = time.time()
    lens_un = []
    for sd in range(n):
        ids = G.generate(eng, pid, 32, sd, stop_newline=lambda t: t in nl)
        lens_un.append(len(ids))
        un.append(NV.decode(ids).split("\n")[0])
    t_un = time.time() - t0
    t0 = time.time()
    lens = []
    for sd in range(n):
        ids = G.generate(eng, pid, 40, sd, index=index, order=order, auto=auto)
        lens.append(len(ids))
        co.append(NV.decode(ids))
    t_co = time.time() - t0
    valid_un = [bool(G.RECORD_RE.fullmatch(s)) for s in un]
    valid_co = [bool(G.RECORD_RE.fullmatch(s)) for s in co]
    allowed = (index >= 0).sum(1)
    out = dict(n=n, prompt=G.PROMPT, states=len(order), vocab=len(strings), t_index=t_index,
               allowed=allowed, valid_un=int(sum(valid_un)), valid_co=int(sum(valid_co)), samples_un=un[:12],
               samples_co=co[:12], tokens_co=int(sum(lens)), tokens_un=int(sum(lens_un)), t_un=t_un, t_co=t_co,
               start_allowed=[strings[i] for i in np.where(index[0] >= 0)[0]])
    # the state after '{"name": "' and a capital: how many tokens may continue the name
    S = auto.run(auto.start, '{"name": "S')
    out["mid_allowed"] = int((index[order.index(S)] >= 0).sum())
    # how masking reweights: Part 13's character model choosing among five names
    c13.load("tf")
    tf, chars, enc, data = c13.load_tf()
    ps = "".join(chars[int(i)] for i in data["passage"])
    k = ps.find("Spade", 600)
    ctx = ps[max(0, k - 200):k]

    def probs_at(prefix):
        with torch.no_grad():
            z = tf(enc(ctx + prefix)[None, -c13.CTX:])[0, -1]
        p = torch.softmax(z, -1).numpy()
        return {c: float(pp) for c, pp in zip(chars, p)}

    ex, mk = G.masked_vs_exact(probs_at)
    out.update(names=G.NAMES, exact=[ex[nm] for nm in G.NAMES], masked=[mk[nm] for nm in G.NAMES], name_ctx=ctx[-60:])
    print(f"    valid records: {out['valid_un']} of {n} unconstrained, {out['valid_co']} constrained; "
          f"{len(order)} automaton states", flush=True)
    return out


# ---------------------------------------------------------------------------
# The frontier: devices, long thinking, prices
# ---------------------------------------------------------------------------
def compute_frontier():
    from videos.ai.ai17.specs import GPUS
    from videos.ai.ai19 import facts as F

    rf, ph = load("roof"), load("phases")
    devices = [("this computer, one core", rf["read_bw"], None)] + [(n, bw, mem) for n, bw, mem, _ in F.DEVICES]
    ap, l8, oss = F.APPLE_ON_DEVICE, F.LLAMA31_8B, F.GPT_OSS_20B
    models = [  # name, bytes read per token, bytes held
        ("Apple's 3B, 2 bits", ap["params"] * ap["bits"] / 8, ap["params"] * ap["bits"] / 8),
        ("gpt-oss-20b, MXFP4", oss["active"] * 4.25 / 8, oss["ckpt_gib"] * 2 ** 30),
        ("Llama 3.1 8B, 4 bits", l8["params"] * 4.25 / 8, l8["params"] * 4.25 / 8),
        ("Llama 3.1 70B, 4 bits", F.LLAMA31_70B["params"] * 4.25 / 8, F.LLAMA31_70B["params"] * 4.25 / 8),
    ]
    bound = [[(bw / mb if (mem is None or held <= 0.75 * mem) else 0.0) for _, mb, held in models]
             for _, bw, mem in devices]
    ours_bytes = 4.0 * ph["sizes"]["read"]
    out = dict(devices=[d[0] for d in devices], bw=[d[1] for d in devices], models=[m[0] for m in models],
               model_bytes=[m[1] for m in models], bound=bound, ours_bound=rf["read_bw"] / ours_bytes,
               ours_meas=float(ph["decode_tps"][0]), ours_bytes=ours_bytes)
    # long chains of thought: cost per answer for Llama 3.1 8B on an H100 (the roofline model of `economics`) as the
    # answer grows from the prompt to n tokens; the batch shrinks as the caches grow
    ec = load("economics")
    H = GPUS["H100"]
    kv_tok, W = ec["kv_tok"], ec["weights"]
    cap = 0.9 * H["mem"]
    res = {}
    for n in (1000, F.R1_0528["tokens_old"], F.R1_0528["tokens_new"], F.R1_0528["max_len"]):
        ctx = np.arange(500, 500 + n, 50, dtype=float)
        avg = ctx.mean()
        bmax = max(1, int((cap - W) // (kv_tok * (500 + n))))  # the batch whose caches fit at the end
        tt, _, _ = roofline_step(l8["params"], W, kv_tok, l8["layers"], l8["heads"] * l8["head_dim"], ctx, bmax,
                                 H["tensor"], H["bw"])
        secs = float(tt.sum() * 50)  # one sequence: time to write n tokens at this batch
        gpu_s_per_answer = secs / bmax
        res[str(n)] = dict(n=n, bmax=bmax, seconds=secs, usd=gpu_s_per_answer / 3600 * F.DSV32["gpu_hour"],
                           per_mtok=gpu_s_per_answer / 3600 * F.DSV32["gpu_hour"] / n * 1e6, avg_ctx=avg)
    out["thinking"] = plain(res)
    # prices: the fall of the cheapest OpenAI model at least as good as GPT-3 (list prices), as a rate per year
    yrs = np.array([p[0] for p in F.PRICES])
    usd = np.array([p[2] for p in F.PRICES])
    slope = np.polyfit(yrs, np.log10(usd), 1)[0]
    out.update(price_years=yrs, price_usd=usd, price_names=[p[1] for p in F.PRICES], price_fall=float(10 ** -slope),
               price_total=float(usd[0] / usd[-1]))
    return out


# ---------------------------------------------------------------------------
ITEMS = {
    "roof": compute_roof,
    "phases": compute_phases,
    "kv": compute_kv,
    "economics": compute_economics,
    "serving": compute_serving,
    "paging": compute_paging,
    "drafters": compute_drafters,
    "exact": compute_exact,
    "rounding": compute_rounding,
    "outliers": compute_outliers,
    "gptq": compute_gptq,
    "rotation": compute_rotation,
    "formats": compute_formats,
    "kvquant": compute_kvquant,
    "flash": compute_flash,
    "grammar": compute_grammar,
    "frontier": compute_frontier,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
