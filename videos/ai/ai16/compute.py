"""Precompute everything numerical in Part 16 of the AI series ("Sparsity").

    python -m videos.ai.ai16.compute              # everything missing (Part 1's books, Part 11's characters,
                                                  # Part 13's transformer)
    python -m videos.ai.ai16.compute --force moe

Results are cached in ``.cache/ai16/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The long items train
many small models in a pool of single-threaded worker processes (``AI16_WORKERS``, default 2) and keep each finished
run as it comes (``CACHE.partial``), so an interrupted run resumes; every run is seeded.

Items:
    lm_runs    every character transformer this part trains (about 2.5 CPU-hours): dense models of the mixture's
               active and total size, the mixture of experts three ways (no balancing, Switch's auxiliary loss,
               DeepSeek's loss-free bias), fine-grained and shared experts, a capacity limit, upcycling, mixture-of-
               depths; three seeds for the main comparisons, two for the rest; weights kept in .cache/ai16/models/
    moe        the mixture against the dense models (curves, held-out bits, the scoreboard's passage), every seed
    balance    each expert's share of the work through training, under the three rules
    fine       coarse, fine-grained and fine-grained-plus-shared experts at the same active and total size
    capacity   tokens dropped and bits lost against the capacity factor, for each router; training with a limit
    parallel   the experts spread over four devices: each device's load, and the all-to-all traffic
    upcycle    a dense model turned into a mixture halfway, against both kept as they were
    special    what the experts learn: where each character goes, mutual information, the same across seeds
    mod        mixture-of-depths: compute per token against held-out bits
    gradcheck  the router's gradient through top-k gates, derived and checked by finite differences
    mix1991    Jacobs, Jordan, Nowlan and Hinton's competing experts on a curve, trained (the gate's regions)
    accounting DeepSeek-V3's and Mixtral's parameters counted from their published configurations
    recall     sparse attention trained on a recall task: full, a sliding window, block selection, a learned indexer
    lottery    iterative magnitude pruning with rewinding (the lottery ticket) against random re-initialization
    prune24    2:4 sparsity on our dense model: magnitude, Wanda, unstructured, and after a short retraining
    actsparse  how many of the feed-forward activations are near zero, and the bits lost when they are skipped
    topk       sparse attention in Part 13's transformer: the attention mass in the top k keys; bits per character
               when each query keeps k keys, by score or as a window
    row        one query of that transformer, for the picture of what a window, NSA's blocks and DSA's top k keep
    configs    mixture-of-experts models as published (facts.py)
    scoreboard the series' scoreboard as Parts 1, 13 and 14 left it, with this part's mixture and dense model
"""

from __future__ import annotations

import math
import os

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai16")
load = CACHE.load
MODELS = CACHE.dir / "models"


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def workers() -> int:
    return int(os.environ.get("AI16_WORKERS", 2))


# ---------------------------------------------------------------------------
# The character transformers
# ---------------------------------------------------------------------------
# d = 64, 2 layers, 4 heads, 64 characters of context; the mixture: 8 experts of hidden 128, 2 per token, so a token
# uses the arithmetic of a dense hidden layer of 256 while the layer holds 1,024
DENSE_ACTIVE = dict(ffn="dense", hidden=256)
DENSE_TOTAL = dict(ffn="dense", hidden=1024)
DENSE_HALF = dict(ffn="dense", hidden=128)  # one expert's size: the model that gets upcycled
MOE = dict(ffn="moe", E=8, k=2, he=128, gate="sigmoid", balance="bias")  # DeepSeek-V3's router
MOE_NONE = dict(ffn="moe", E=8, k=2, he=128, gate="softmax", balance="none")  # Mixtral's gate, unbalanced
MOE_AUX = dict(ffn="moe", E=8, k=2, he=128, gate="softmax", balance="aux", aux=0.01)  # Switch's loss, its strength
FINE = dict(ffn="moe", E=32, k=8, he=32, gate="sigmoid", balance="bias")  # each expert cut in four
SHARED = dict(ffn="moe", E=31, k=7, he=32, shared=1, hs=32, gate="sigmoid", balance="bias")  # DeepSeekMoE
MOE_CF = dict(MOE, cf=1.0)
DENSE_L3 = dict(ffn="dense", hidden=256, layers=3)
DENSE_L4 = dict(ffn="dense", hidden=256, layers=4)
MOD_50 = dict(ffn="dense", hidden=256, layers=4, mod_layers=(1, 3), mod_cap=0.5)
MOD_12 = dict(ffn="dense", hidden=256, layers=4, mod_layers=(1, 3), mod_cap=0.125)

SEEDS3, SEEDS2 = (0, 1, 2), (0, 1)
RUNS = [  # (name, cfg, seeds, record the routing tables for the replay)
    ("dense_active", DENSE_ACTIVE, SEEDS3, False),
    ("moe", MOE, SEEDS3, True),
    ("dense_total", DENSE_TOTAL, SEEDS3, False),
    ("none", MOE_NONE, SEEDS3, True),
    ("aux", MOE_AUX, SEEDS3, True),
    ("fine", FINE, SEEDS2, True),
    ("shared", SHARED, SEEDS2, True),
    ("moe_cf", MOE_CF, SEEDS2, False),
    ("dense_half", DENSE_HALF, SEEDS2, False),
    ("dense_l3", DENSE_L3, SEEDS2, False),
    ("dense_l4", DENSE_L4, SEEDS2, False),
    ("mod50", MOD_50, SEEDS2, False),
    ("mod12", MOD_12, SEEDS2, False),
]
UP_AT = 1000  # the dense model is upcycled halfway through its 2,000 steps


def model_path(key: str):
    return MODELS / f"{key}.pt"


def _specs():
    from videos.ai.ai16 import runs as R

    out = []
    for name, cfg, seeds, route in RUNS:
        for s in seeds:
            key = f"{name}_s{s}"
            sp = dict(key=key, cfg=cfg, seed=s, steps=R.STEPS, route=route and s == 0, save=str(model_path(key)))
            if name == "dense_half":
                sp.update(save_at=UP_AT, save_mid=str(model_path(f"{key}_mid")))
            out.append(sp)
    ups = [dict(key=f"upcycled_s{s}", cfg=MOE, seed=s, steps=R.STEPS - UP_AT, start_step=UP_AT,
                schedule_steps=R.STEPS, upcycle=str(model_path(f"dense_half_s{s}_mid")),
                snaps=(0, 50, 100, 200, 400, 600, R.STEPS - UP_AT), save=str(model_path(f"upcycled_s{s}")))
           for s in SEEDS2]
    return out, ups


def _run(spec):
    from videos.ai.ai16 import runs as R

    out = R.train(spec)
    out["key"] = spec["key"]
    return out


def compute_lm_runs():
    import time

    from videos.ai.ai16 import runs as R

    first, ups = _specs()
    part = CACHE.partial("lm_runs", dict(v=3, steps=R.STEPS, runs=[[n, c, list(s)] for n, c, s, _ in RUNS]))
    t0 = time.time()
    for phase in (first, ups):
        todo = [s for s in phase if s["key"] not in part or not model_path(s["key"]).exists()]
        for sp, res in R.pool_map(_run, todo, workers()):
            part[sp["key"]] = res
            print(f"    {sp['key']}: {res['final']:.3f} bits ({res['seconds'] / 60:.1f} min; "
                  f"{(time.time() - t0) / 60:.0f} min so far)", flush=True)
    out = {k: part[k] for k in [s["key"] for s in first + ups]}
    return dict(runs=out)


def runs() -> dict:
    return load("lm_runs")["runs"]


def saved(key: str):
    """A trained model of lm_runs, in evaluation mode."""
    import torch

    from videos.ai.ai16 import runs as R

    r = runs()[key]
    m = R.build(r["cfg"])
    m.load_state_dict(torch.load(model_path(key), weights_only=True))
    m.eval()
    return m


def _stack(key, seeds, field="curve"):
    R = runs()
    return np.array([R[f"{key}_s{s}"][field] for s in seeds], float)


# display characters for the routing tables (the commonest, by kind)
SHOW = "etaoinshrdlucmwfgypbvk TAIHS.,'\"-?!"
CLASSES = [("vowels", "aeiou"), ("consonants", "bcdfghjklmnpqrstvwxyz"), ("capitals", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
           ("spaces", " \n"), ("punctuation", ".,;:'\"!?-()")]


def compute_moe():
    """The mixture against the two dense models: curves (every seed), held-out bits, the scoreboard's passage; the
    replay of the first seed's training (each layer's routing tables at the checkpoints, and the loads)."""
    from videos.ai.ai16 import runs as R

    Rn = runs()
    _, _, K, _, chars = R.lm_data()
    out = dict(names=["dense_active", "moe", "dense_total"], seeds=list(SEEDS3), steps=R.STEPS)
    for n in out["names"]:
        out[f"{n}_curve"] = _stack(n, SEEDS3)
        out[f"{n}_valid"] = [Rn[f"{n}_s{s}"]["valid_bits"] for s in SEEDS3]
        out[f"{n}_passage"] = [Rn[f"{n}_s{s}"]["passage_bits"] for s in SEEDS3]
        out[f"{n}_counts"] = Rn[f"{n}_s0"]["counts"]
        out[f"{n}_flops"] = Rn[f"{n}_s0"]["flops"]
        out[f"{n}_seconds"] = [Rn[f"{n}_s{s}"]["seconds"] for s in SEEDS3]
    r0 = Rn["moe_s0"]
    out["route_steps"] = r0["route_steps"]
    show = [c for c in SHOW if c in chars]
    idx = [chars.index(c) for c in show]
    A = np.asarray(r0["routes"], float)  # snaps, layers, K, E
    out["route_chars"] = show
    out["routes"] = A[:, :, idx, :] / np.maximum(A[:, :, idx, :].sum(-1, keepdims=True), 1)
    out["loads"] = np.asarray(r0["loads"], float)  # time, layers, E
    out["load_every"] = R.LOAD_EVERY
    # verdicts: the mixture against the dense model with the same arithmetic, seed by seed
    out["wins_active"] = int(sum(m < d for m, d in zip(out["moe_valid"], out["dense_active_valid"])))
    out["wins_total"] = int(sum(m < d for m, d in zip(out["moe_valid"], out["dense_total_valid"])))
    return out


def compute_speed():
    """Milliseconds per training step on one CPU core for the three models of the comparison, interleaved and
    repeated (the fastest of five tries each), so that other work on the machine biases none of them."""
    import time

    import torch
    import torch.nn.functional as F

    from videos.ai.ai16 import runs as R

    torch.set_num_threads(1)
    tr, va, K, _, _ = R.lm_data()
    cfgs = dict(dense_active=DENSE_ACTIVE, moe=MOE, dense_total=DENSE_TOTAL)
    models = {k: R.build(dict(c, vocab=K)) for k, c in cfgs.items()}
    opts = {k: torch.optim.AdamW(m.parameters(), lr=1e-3) for k, m in models.items()}
    g = rng(5)
    best = {k: float("inf") for k in cfgs}
    for _ in range(5):
        for k, m in models.items():
            x, y = R.windows(tr, g.integers(0, len(tr) - 70, R.BATCH), 64)
            t0 = time.perf_counter()
            for _ in range(10):
                loss = F.cross_entropy(m(x).reshape(-1, K), y.reshape(-1))
                opts[k].zero_grad()
                loss.backward()
                opts[k].step()
            best[k] = min(best[k], (time.perf_counter() - t0) / 10)
    return best


def compute_balance():
    from videos.ai.ai16 import runs as R

    Rn = runs()
    out = dict(modes=["none", "aux", "moe"], seeds=list(SEEDS3), E=8, load_every=R.LOAD_EVERY)
    for mode in out["modes"]:
        L = np.array([Rn[f"{mode}_s{s}"]["loads"] for s in SEEDS3], float)  # seeds, time, layers, E
        out[f"{mode}_loads"] = L
        tail = L[:, -10:].mean(1)  # seeds, layers, E: the last 200 steps
        out[f"{mode}_busiest"] = (tail.max(-1) * 8).tolist()  # in multiples of a fair share
        out[f"{mode}_starved"] = (tail < 0.25 / 8).sum(-1).tolist()  # experts getting under a quarter of a fair share
        out[f"{mode}_maxvio"] = (L.max(-1) * 8 - 1).mean(1).tolist()  # Wang et al.'s MaxVio, averaged over training
        out[f"{mode}_valid"] = [Rn[f"{mode}_s{s}"]["valid_bits"] for s in SEEDS3]
        out[f"{mode}_curve"] = _stack(mode, SEEDS3)
    out["bias_hist"] = np.asarray(Rn["moe_s0"]["bias"], float)  # time, layers, E
    for mode in out["modes"]:
        b = np.asarray(out[f"{mode}_busiest"])
        out[f"{mode}_busiest_mean"] = float(b.mean())
    return out


def compute_fine():
    Rn = runs()
    names = ["moe", "fine", "shared"]
    out = dict(names=names, seeds=list(SEEDS2))
    for n in names:
        out[f"{n}_valid"] = [Rn[f"{n}_s{s}"]["valid_bits"] for s in SEEDS2]
        out[f"{n}_curve"] = _stack(n, SEEDS2)
        out[f"{n}_counts"] = Rn[f"{n}_s0"]["counts"]
        out[f"{n}_flops"] = Rn[f"{n}_s0"]["flops"]
        c = Rn[f"{n}_s0"]["cfg"]
        out[f"{n}_cfg"] = dict(E=c["E"], k=c["k"], he=c["he"], shared=c["shared"])
        out[f"{n}_combos"] = math.comb(c["E"], c["k"])
    out["moe_valid_all"] = [Rn[f"moe_s{s}"]["valid_bits"] for s in SEEDS3]
    return out


CFS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 0.0]  # 0: no limit


def compute_capacity():
    """Each router at each capacity factor (imposed after training): the share of token-slots dropped, and held-out
    bits; and the mixture trained with a capacity factor of 1 against without."""
    import torch

    from videos.ai.ai16 import runs as R

    tr, va, K, _, _ = R.lm_data()
    torch.set_num_threads(2)
    out = dict(cfs=CFS, modes=["none", "aux", "moe"], seeds=list(SEEDS3))
    starts = np.linspace(0, len(va) - 66, 32).astype(int)
    x, _ = R.windows(va, starts, 64)
    for mode in out["modes"]:
        drops, bits = [], []
        for s in SEEDS3:
            m = saved(f"{mode}_s{s}")
            dr, bt = [], []
            for cf in CFS:
                for L in m.moes():
                    L.cf_eval = cf
                with torch.no_grad():
                    m(x)
                dr.append(float(np.mean([L.dropped for L in m.moes()])))
                bt.append(R.lm_bits(m, va, 64, 200))
                m.train(False)
            drops.append(dr)
            bits.append(bt)
            print(f"    capacity {mode} s{s}: drops {np.round(dr, 3)}", flush=True)
        out[f"{mode}_drops"], out[f"{mode}_bits"] = drops, bits
    Rn = runs()
    out["cf_train_valid"] = [Rn[f"moe_cf_s{s}"]["valid_bits"] for s in SEEDS2]
    out["nocf_train_valid"] = [Rn[f"moe_s{s}"]["valid_bits"] for s in SEEDS2]
    out["cf_train_drops"] = np.array([Rn[f"moe_cf_s{s}"]["drops"] for s in SEEDS2], float).mean(-1)  # seeds, time
    return out


def compute_parallel():
    """Expert parallelism, simulated with our routers: the 8 experts on 4 devices (2 each).  Each device's share of
    the token-slots at the end of training (the busiest sets the pace), and the all-to-all's bytes per token."""
    Rn = runs()
    D = 4
    out = dict(devices=D, modes=["none", "aux", "moe"])
    for mode in out["modes"]:
        per = []
        for s in SEEDS3:
            L = np.asarray(Rn[f"{mode}_s{s}"]["loads"], float)[-10:].mean(0)  # layers, E
            dev = L.reshape(L.shape[0], D, -1).sum(-1)  # layers, devices
            per.append(dev.tolist())
        per = np.asarray(per)
        out[f"{mode}_dev"] = per
        out[f"{mode}_slowdown"] = float((per.max(-1) * D).mean())  # the busiest device against a fair share
    # bytes per token per MoE layer (each of k copies sent out, and the result sent back), 16-bit, for our model and
    # DeepSeek-V3 (dispatched in FP8, combined in BF16, Sec. 3.3 of its report)
    from videos.ai.ai16 import facts as F

    c = F.DSV3_CONFIG
    out["ours_bytes"] = 2 * 2 * 64 * 2 * (1 - 1 / D)
    out["ours_flops"] = 2 * 2 * 64 * 128 * 2  # 2 experts, 2 matrices of 64 x 128, 2 FLOPs per multiply-add
    out["v3_bytes"] = c["k"] * c["d"] * (1 + 2)
    out["v3_flops"] = 2 * 3 * c["d"] * c["moe_ffn"] * c["k"]  # the routed experts' work (the shared one stays home)
    out["v3_intensity"] = out["v3_flops"] / out["v3_bytes"]
    from videos.ai.ai17.specs import GPUS

    out["h800_flops"] = GPUS["H100"]["fp8"]  # H800: H100's arithmetic, a cut-down NVLink
    out["ib"], out["nvlink"] = F.DSV3_ROUTING["ib"], F.DSV3_ROUTING["nvlink"]
    out["ridge_ib"] = out["h800_flops"] / out["ib"]
    out["ridge_nvlink"] = out["h800_flops"] / out["nvlink"]
    return out


def compute_upcycle():
    Rn = runs()
    out = dict(seeds=list(SEEDS2), at=UP_AT)
    out["up_curve"] = _stack("upcycled", SEEDS2)
    out["half_curve"] = _stack("dense_half", SEEDS2)
    out["moe_curve"] = _stack("moe", SEEDS2)
    out["active_curve"] = _stack("dense_active", SEEDS2)
    for k in ("upcycled", "dense_half", "moe", "dense_active"):
        out[f"{k}_valid"] = [Rn[f"{k}_s{s}"]["valid_bits"] for s in SEEDS2]
        out[f"{k}_flops"] = Rn[f"{k}_s0"]["flops"]
    out["half_counts"] = Rn["dense_half_s0"]["counts"]
    # total training compute, in FLOPs per token times steps
    out["compute_up"] = UP_AT * out["dense_half_flops"] + (2000 - UP_AT) * out["moe_flops"]
    out["compute_moe"] = 2000 * out["moe_flops"]
    out["compute_half"] = 2000 * out["dense_half_flops"]
    return out


def _mi(a, b, na, nb):
    """Mutual information (bits) between two integer sequences."""
    J = np.zeros((na, nb))
    np.add.at(J, (a, b), 1)
    J /= J.sum()
    pa, pb = J.sum(1, keepdims=True), J.sum(0, keepdims=True)
    nz = J > 0
    return float((J[nz] * np.log2(J[nz] / (pa @ pb)[nz])).sum())


def compute_special():
    """What the experts learn, in the mixture (every seed, both layers): the mutual information between an expert's
    being chosen and the current, previous and next character, against the same with the characters shuffled; the
    share of each kind of character each expert takes; and the routing table of the commonest characters."""
    import torch

    from videos.ai.ai16 import runs as R

    tr, va, K, _, chars = R.lm_data()
    g = rng(16)
    starts = np.linspace(0, len(va) - 66, 256).astype(int)
    x, y = R.windows(va, starts, 64)
    out = dict(seeds=list(SEEDS3), modes=["moe", "fine"], classes=[c for c, _ in CLASSES])
    cls_of = np.full(K, -1)
    for j, (_, cs) in enumerate(CLASSES):
        for ch in cs:
            if ch in chars:
                cls_of[chars.index(ch)] = j
    show = [c for c in SHOW if c in chars]
    out["route_chars"] = show
    for mode in out["modes"]:
        seeds = SEEDS3 if mode == "moe" else SEEDS2
        for s in seeds:
            m = saved(f"{mode}_s{s}")
            with torch.no_grad():
                m(x, probe=True)
            cur = x.reshape(-1).numpy()
            nxt = y.reshape(-1).numpy()
            prv = np.concatenate([[0], cur[:-1]])
            for li, L in enumerate(m.moes()):
                E, k = L.c.E, L.c.k
                top = L.top.reshape(-1, k).numpy()
                ex = top.reshape(-1)
                rep = lambda v: np.repeat(v, k)  # noqa: E731
                res = dict(cur=_mi(ex, rep(cur), E, K), nxt=_mi(ex, rep(nxt), E, K), prv=_mi(ex, rep(prv), E, K),
                           shuf=_mi(ex, rep(g.permutation(cur)), E, K), H=float(np.log2(E)))
                C = np.zeros((len(CLASSES), E))
                ok = cls_of[rep(cur)] >= 0
                np.add.at(C, (cls_of[rep(cur)][ok], ex[ok]), 1)
                res["classes"] = (C / C.sum(1, keepdims=True)).tolist()
                T = np.zeros((len(show), E))
                for i, ch in enumerate(show):
                    sel = rep(cur) == chars.index(ch)
                    T[i] = np.bincount(ex[sel], minlength=E) / max(sel.sum(), 1)
                res["table"] = T.tolist()
                out[f"{mode}_s{s}_l{li}"] = res
            print(f"    special {mode} s{s}: " + ", ".join(
                f"layer {li + 1} cur {out[f'{mode}_s{s}_l{li}']['cur']:.2f} next {out[f'{mode}_s{s}_l{li}']['nxt']:.2f}"
                for li in range(len(m.moes()))), flush=True)
    return out


def compute_mod():
    Rn = runs()
    names = ["dense_active", "dense_l3", "dense_l4", "mod50", "mod12"]
    out = dict(names=names, seeds=list(SEEDS2))
    for n in names:
        out[f"{n}_flops"] = Rn[f"{n}_s0"]["flops"]
        out[f"{n}_valid"] = [Rn[f"{n}_s{s}"]["valid_bits"] for s in SEEDS2]
        out[f"{n}_curve"] = _stack(n, SEEDS2)
        if n.startswith("mod"):
            out[f"{n}_causal"] = [Rn[f"{n}_s{s}"]["valid_bits_causal"] for s in SEEDS2]
            out[f"{n}_causal_frac"] = [float(np.mean(Rn[f"{n}_s{s}"]["causal_frac"])) for s in SEEDS2]
            out[f"{n}_cap"] = Rn[f"{n}_s0"]["cfg"]["mod_cap"]
    # which tokens the routed blocks take: the share of each kind of character chosen, in mod12 (seed 0), top-k
    import torch

    from videos.ai.ai16 import runs as R

    _, va, K, _, chars = R.lm_data()
    starts = np.linspace(0, len(va) - 66, 128).astype(int)
    x, _ = R.windows(va, starts, 64)
    m = saved("mod12_s0")
    with torch.no_grad():
        m(x)
    keep = np.mean([b.keep.numpy() for b in m.blocks if b.routed], 0).reshape(-1)  # share of routed blocks taking it
    cur = x.reshape(-1).numpy()
    share = {}
    for name, cs in CLASSES:
        sel = np.isin(cur, [chars.index(c) for c in cs if c in chars])
        share[name] = float(keep[sel].mean()) if sel.any() else 0.0
    out["mod12_class_share"] = share
    out["mod12_example"] = "".join(chars[i] for i in x[3].tolist())
    out["mod12_example_keep"] = np.array([b.keep[3].numpy() for b in m.blocks if b.routed], float)
    return out




# ---------------------------------------------------------------------------
# Small exact experiments
# ---------------------------------------------------------------------------
def compute_gradcheck():
    from videos.ai.ai16 import toys

    return toys.compute_gradcheck()


def compute_mix1991():
    from videos.ai.ai16 import toys

    return toys.compute_mix1991()


def compute_accounting():
    """Parameters counted from the published configurations, matrix by matrix."""
    from videos.ai.ai16 import facts as F

    c = F.DSV3_CONFIG
    d, H = c["d"], c["heads"]
    attn = (d * c["q_lora"] + c["q_lora"] + c["q_lora"] * H * (c["nope"] + c["rope"])
            + d * (c["kv_lora"] + c["rope"]) + c["kv_lora"] + c["kv_lora"] * H * (c["nope"] + c["v"]) + H * c["v"] * d)
    expert = 3 * d * c["moe_ffn"]  # SwiGLU: gate, up, down
    dense_ffn = 3 * d * c["ffn"]
    router = c["routed"] * d + c["routed"]  # weights and the balancing bias
    norms = 2 * d
    n_moe = c["layers"] - c["dense_layers"]
    emb = c["vocab"] * d
    parts = dict(embed=emb, head=emb, attention=c["layers"] * (attn + norms) + d,
                 dense_ffn=c["dense_layers"] * dense_ffn, routed=n_moe * c["routed"] * expert,
                 shared=n_moe * c["shared"] * expert, router=n_moe * router)
    total = sum(parts.values())
    active = (parts["head"] + parts["attention"] + parts["dense_ffn"] + parts["shared"] + parts["router"]
              + n_moe * c["k"] * expert)
    v3 = dict(parts=parts, total=total, active=active, active_with_embed=active + emb, attn_layer=attn, expert=expert,
              n_moe=n_moe, mtp=c["mtp_params"])
    assert abs(total - 671e9) / 671e9 < 0.01, total
    assert abs(active + emb - 37e9) / 37e9 < 0.03, active
    m = F.MIXTRAL_CONFIG
    d = m["d"]
    attn = d * m["heads"] * m["head_dim"] * 2 + 2 * d * m["kv_heads"] * m["head_dim"]
    expert = 3 * d * m["ffn"]
    per = attn + m["experts"] * expert + m["experts"] * d + 2 * d
    total = m["layers"] * per + 2 * m["vocab"] * d + d
    active = m["layers"] * (attn + m["k"] * expert + m["experts"] * d + 2 * d) + 2 * m["vocab"] * d + d
    mx = dict(total=total, active=active, attn_layer=attn, expert=expert)
    assert abs(total - 46.7e9) / 46.7e9 < 0.01 and abs(active - 12.9e9) / 12.9e9 < 0.01, (total, active)
    return dict(v3=v3, mixtral=mx)


def compute_configs():
    from videos.ai.ai16 import facts as F

    rows = []
    for key, name, date, total, active, E, k, sh, src in F.MODELS:
        yr = int(date[:4]) + (int(date[5:7]) - 0.5) / 12
        rows.append(dict(key=key, name=name, date=date, year=yr, total=total, active=active, experts=E, k=k, shared=sh,
                         frac=(active / total) if active else None, expert_frac=(k + sh) / (E + sh), src=src))
    return dict(rows=rows)


# ---------------------------------------------------------------------------
# Sparse attention, trained on a recall task
# ---------------------------------------------------------------------------
RECALL_KEYS = 8  # keys each query may use, in every sparse pattern
RECALL_STEPS, RECALL_LR, RECALL_BATCH = 1000, 3e-3, 64
RECALL_IDX_STEPS, RECALL_IDX_WARM = 500, 200


def _recall_cfg(attn):
    from videos.ai.ai16 import recall as Q

    return dict(vocab=Q.VOCAB, ctx=Q.T, ffn="dense", hidden=256, attn=attn, attn_k=RECALL_KEYS, block=4)


def compute_recall():
    """Full attention, a sliding window of 8 keys, block selection (blocks of 4: the query's own and the one whose
    mean key it scores highest) and a learned indexer (8 keys; started from the full model, its indexer first
    trained to match the full attention, then trained sparse), two seeds each; and the full models with each
    pattern imposed after training, untrained for it."""
    import torch

    from videos.ai.ai16 import recall as Q
    from videos.ai.ai16 import runs as R

    part = CACHE.partial("recall", dict(v=3, keys=RECALL_KEYS, steps=RECALL_STEPS, idx=RECALL_IDX_STEPS))
    snaps = tuple(range(0, RECALL_STEPS + 1, 50))
    specs = [dict(key=f"{a}_s{s}", task="recall", cfg=_recall_cfg(a), seed=s, steps=RECALL_STEPS, lr=RECALL_LR,
                  batch=RECALL_BATCH, snaps=snaps, save=str(MODELS / f"recall_{a}_s{s}.pt"))
             for a in ("full", "window", "blocks") for s in SEEDS2]
    todo = [sp for sp in specs if sp["key"] not in part]
    for sp, res in R.pool_map(_run, todo, workers()):
        part[sp["key"]] = res
        print(f"    recall {sp['key']}: {res['final']:.3f} ({res['seconds'] / 60:.1f} min)", flush=True)
    idx = [dict(key=f"index_s{s}", task="recall", cfg=_recall_cfg("index"), seed=s, steps=RECALL_IDX_STEPS,
                lr=RECALL_LR, batch=RECALL_BATCH, init=str(MODELS / f"recall_full_s{s}.pt"), warm_index=RECALL_IDX_WARM,
                snaps=tuple(range(0, RECALL_IDX_STEPS + 1, 25)), save=str(MODELS / f"recall_index_s{s}.pt"))
           for s in SEEDS2]
    todo = [sp for sp in idx if sp["key"] not in part]
    for sp, res in R.pool_map(_run, todo, workers()):
        part[sp["key"]] = res
        print(f"    recall {sp['key']}: {res['final']:.3f} ({res['seconds'] / 60:.1f} min)", flush=True)
    out = dict(keys=RECALL_KEYS, steps=RECALL_STEPS, idx_steps=RECALL_IDX_STEPS, idx_warm=RECALL_IDX_WARM,
               seeds=list(SEEDS2), T=Q.T, facts=Q.FACTS, fill=Q.FILL, modes=["full", "window", "blocks", "index"])
    for a in out["modes"]:
        out[f"{a}_curve"] = np.array([part[f"{a}_s{s}"]["curve"] for s in SEEDS2], float)
        out[f"{a}_acc"] = [part[f"{a}_s{s}"]["final"] for s in SEEDS2]
    out["index_kl"] = np.array([part[f"index_s{s}"]["index_kl"] for s in SEEDS2], float)
    # each pattern imposed on the full models, untrained for it
    torch.set_num_threads(2)
    for a in ("window", "blocks", "topk"):
        acc = []
        for s in SEEDS2:
            m = R.build(_recall_cfg(a))
            m.load_state_dict(torch.load(MODELS / f"recall_full_s{s}.pt", weights_only=True))
            acc.append(Q.accuracy(m, seed=99, n=256))
        out[f"imposed_{a}_acc"] = acc
    # one query of the full model (seed 0, last layer): its attention, and the keys each pattern keeps
    g = np.random.default_rng(7)
    x, y, w = Q.batch(g, 1)
    pick = {}
    for a in ("full", "window", "blocks", "index"):
        m = R.build(_recall_cfg(a))
        m.load_state_dict(torch.load(MODELS / f"recall_{a}_s0.pt", weights_only=True), strict=False)
        m.eval()
        with torch.no_grad():
            z = m(x, probe=True)
        at = m.blocks[-1].attn.last
        qpos = int(np.nonzero(w[0].numpy())[0][5])
        pick[a] = dict(p=at["p"][0, :, qpos].numpy(), m=at["m"][0, :, qpos].numpy() if at["m"].shape[0] > 1 else
                       at["m"][0, :, qpos].numpy(), right=bool(z[0, qpos].argmax() == y[0, qpos]))
    out["example_tokens"] = x[0].numpy()
    out["example_q"] = qpos
    tok = x[0].numpy()
    key = int(tok[qpos]) - Q.ASK0
    out["example_answer_pos"] = int(1 + np.nonzero((tok[1:1 + Q.FACTS] - Q.FACT0) // Q.NV == key)[0][0])  # the fact
    for a, d_ in pick.items():
        out[f"example_{a}_p"] = d_["p"]
        out[f"example_{a}_m"] = d_["m"].astype(float)
        out[f"example_{a}_right"] = d_["right"]
    return out


# ---------------------------------------------------------------------------
# Pruning
# ---------------------------------------------------------------------------
def compute_lottery():
    from videos.ai.ai16 import lottery as Lt

    part = CACHE.partial("lottery", dict(v=1, steps=Lt.STEPS, rounds=Lt.ROUNDS, rewind=Lt.REWIND, rate=list(Lt.RATE)))
    out = dict(seeds=list(SEEDS2), rounds=Lt.ROUNDS, rewind=Lt.REWIND, steps=Lt.STEPS, rate=list(Lt.RATE))
    for s in SEEDS2:
        key = f"s{s}"
        if key not in part:
            part[key] = Lt.run(s)
        r = part[key]
        for k in ("dense", "ticket", "reinit", "random", "remain", "zeros", "first_by_slot", "params"):
            out[f"{k}_s{s}"] = r[k]
        out[f"mask_img_s{s}"] = np.array(r["mask_img"], float)
    return out


def compute_prune24():
    """2:4 sparsity on our dense transformer (the one with the mixture's arithmetic), every seed."""
    import copy

    import torch

    from videos.ai.ai16 import prune as P
    from videos.ai.ai16 import runs as R

    torch.set_num_threads(2)
    tr, va, K, _, _ = R.lm_data()
    methods = ["magnitude_24", "wanda_24", "unstructured", "random_24"]
    out = dict(methods=methods, seeds=list(SEEDS3), ft_steps=P.FT_STEPS)
    g = rng(24)
    xc, _ = R.windows(tr, g.integers(0, len(tr) - 66, 64), 64)  # calibration: 64 windows of training text
    for s in SEEDS3:
        base = saved(f"dense_active_s{s}")
        out[f"dense_s{s}"] = R.lm_bits(base, va, 64, 200)
        norms = P.input_norms(base, xc)
        for meth in methods:
            m = copy.deepcopy(base)
            mk = P.masks(m, meth, norms, seed=s)
            P.apply(m, mk)
            out[f"{meth}_s{s}"] = R.lm_bits(m, va, 64, 200)
            out[f"{meth}_kept_s{s}"] = float(sum(v.sum() for v in mk.values()) / sum(v.numel() for v in mk.values()))
            if meth in ("magnitude_24", "wanda_24"):
                torch.manual_seed(s)
                curve = P.finetune(m, mk, s)
                out[f"{meth}_ft_s{s}"] = curve[-1][1]
                out[f"{meth}_ft_curve_s{s}"] = curve
                assert all(float((L.weight[mk[n] == 0]).abs().max()) == 0 for n, L in P.linears(m))  # still 2:4
            print(f"    prune24 s{s} {meth}: {out[f'{meth}_s{s}']:.3f}"
                  + (f" -> {out[f'{meth}_ft_s{s}']:.3f} retrained" if f"{meth}_ft_s{s}" in out else ""), flush=True)
        # the picture: one row of the first feed-forward matrix, its weights and which survive 2:4 by magnitude
        W = base.blocks[0].ffn.w1.weight.detach()[:6, :32]
        out[f"example_w_s{s}"] = W.numpy()
        out[f"example_m_s{s}"] = P.mask_nm(W.abs()).numpy()
    # what the dense model's own retraining for the same steps does (a fair yardstick for the retrained 2:4 model)
    return out


def compute_actsparse():
    """How sparse the feed-forward activations of our transformers are, and what zeroing the small ones costs."""
    import torch

    from videos.ai.ai16 import prune as P
    from videos.ai.ai16 import runs as R

    torch.set_num_threads(2)
    tr, va, K, _, _ = R.lm_data()
    g = rng(31)
    xc, _ = R.windows(tr, g.integers(0, len(tr) - 66, 32), 64)
    fracs = [0.0, 0.25, 0.5, 0.75, 0.9, 0.95]
    out = dict(fracs=fracs, seeds=list(SEEDS3), cuts=[0.01, 0.05, 0.1])
    edges = np.linspace(-0.25, 1.5, 71)
    for s in SEEDS3:
        m = saved(f"dense_active_s{s}")
        acts = P.gelu_acts(m, xc)
        out[f"hist_s{s}"] = np.array([np.histogram(a.reshape(-1), edges)[0] for a in acts])
        out[f"small_s{s}"] = [[float((np.abs(a) < c).mean()) for c in out["cuts"]] for a in acts]
        out[f"neg_s{s}"] = [float((a < 0).mean()) for a in acts]
        bits = []
        for f in fracs:
            thr = [float(np.quantile(np.abs(a), f)) for a in acts]
            bits.append(P.sparsify_bits(m, va, 64, f, thr))
        out[f"bits_s{s}"] = bits
        print(f"    actsparse s{s}: " + " ".join(f"{100 * f:.0f}%:{b:.3f}" for f, b in zip(fracs, bits)), flush=True)
    out["edges"] = edges
    from videos.ai.ai16 import lottery as Lt  # noqa: F401  (the ReLU network's zeros come from the lottery item)

    L = load("lottery")
    out["relu_zeros"] = [L[f"zeros_s{s}"] for s in SEEDS2]
    return out


# ---------------------------------------------------------------------------
# The scoreboard
# ---------------------------------------------------------------------------
def compute_scoreboard():
    """The series' scoreboard as Parts 1, 13 and 14 left it (read through their compute), with Part 16's rows: the
    mixture of experts and the dense model with the same arithmetic per character (mean of three seeds)."""
    from videos.ai.ai13.compute import load as load13
    from videos.ai.ai14.compute import load as load14

    S14, B = load14("scoreboard"), load14("scoreboard_base")
    rows = [dict(label=r["label"], bits=r["bits"], kind=r["kind"], part=r["part"]) for r in S14["rows"]]
    rows.append(dict(label="Part 13's transformer (characters)", bits=float(load13("tf")["passage_bits"]), kind="lm",
                     part=13))
    rows.append(dict(label="the series' model", bits=float(B["bits"]), kind="lm", part=14, params=int(B["params"])))
    M = load("moe")
    rows.append(dict(label="Part 16: dense, same arithmetic", bits=float(np.mean(M["dense_active_passage"])), kind="lm",
                     part=16, key="dense16", params=int(M["dense_active_counts"]["total"])))
    rows.append(dict(label="Part 16: mixture of experts", bits=float(np.mean(M["moe_passage"])), kind="lm", part=16,
                     key="moe16", params=int(M["moe_counts"]["total"]), active=int(M["moe_counts"]["active"])))
    rows.append(dict(label="Part 16: dense, same parameters", bits=float(np.mean(M["dense_total_passage"])), kind="lm",
                     part=16, key="dense16t", params=int(M["dense_total_counts"]["total"])))
    return dict(rows=rows, chars=S14["chars"], tf_params=int(load13("tf")["n_params"]))


# ---------------------------------------------------------------------------
def compute_topk():
    import torch
    import torch.nn.functional as F

    from videos.ai.ai13 import compute as c11

    torch.set_num_threads(2)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    va = data["valid"]
    T = c11.CTX
    g = rng(5)
    starts = g.integers(0, len(va) - T - 1, 24)
    x = torch.stack([va[s:s + T] for s in starts])
    y = torch.stack([va[s + 1:s + T + 1] for s in starts])
    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)
    ks = [1, 2, 4, 8, 16, 32, 64]

    def rot(t):
        a, b = t[..., : c11.DH // 2], t[..., c11.DH // 2:]
        return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)

    def run(keep=None, mode="all", mass=None):
        h = model.emb(x)
        B = len(x)
        causal = torch.ones(T, T, dtype=torch.bool).tril()
        for li, blk in enumerate(model.blocks):
            q, k, v = blk.qkv(blk.n1(h)).view(B, T, 3, c11.HEADS, c11.DH).permute(2, 0, 3, 1, 4)
            q, k = rot(q), rot(k)
            s = (q @ k.transpose(-1, -2)) / math.sqrt(c11.DH)
            s = s.masked_fill(~causal, float("-inf"))
            if mode == "topk":
                kth = torch.topk(s, min(keep, T), -1).values[..., -1:]
                s = s.masked_fill(s < kth, float("-inf"))
            elif mode == "window":
                win = causal & ~torch.ones(T, T, dtype=torch.bool).tril(-keep)
                s = s.masked_fill(~win, float("-inf"))
            p = torch.softmax(s, -1)
            if mass is not None:
                srt = torch.sort(p[:, :, 128:], -1, descending=True).values.cumsum(-1)
                mass[li] = np.stack([srt[..., k_ - 1].mean((0, 2)).numpy() for k_ in ks], -1)  # head, k
            a = (p @ v).transpose(1, 2).reshape(B, T, -1)
            h = h + blk.o(a)
            h = h + blk.f2(F.gelu(blk.f1(blk.n2(h))))
        z = model.out(model.nf(h))
        ce = F.cross_entropy(z[:, 128:].reshape(-1, z.shape[-1]), y[:, 128:].reshape(-1))
        return float(ce) / math.log(2)

    with torch.no_grad():
        mass = {}
        full = run(mass=mass)
        out = dict(ks=ks, full=full, mass=np.stack([mass[i] for i in range(c11.LAYERS)]))
        kk = [4, 8, 16, 32, 64]
        out["kk"] = kk
        out["bits_topk"] = [run(k_, "topk") for k_ in kk]
        out["bits_window"] = [run(k_, "window") for k_ in kk]
    print("    full {:.3f}; top-k {}; window {}".format(full, np.round(out["bits_topk"], 3), np.round(out["bits_window"], 3)))
    assert out["bits_topk"][-1] - full < 0.05  # 64 keys chosen by score: almost nothing lost
    assert out["bits_topk"][1] < out["bits_window"][1]  # chosen by score beats the most recent, at k = 8
    return out


# ---------------------------------------------------------------------------
NROW, KEEP, BLOCK = 48, 8, 8


def compute_row():
    import torch
    import torch.nn.functional as F

    from videos.ai.ai13 import compute as c11

    torch.set_num_threads(2)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    va = data["valid"]
    T = c11.CTX
    starts = rng(13).integers(0, len(va) - T - 1, 48)
    x = torch.stack([va[s:s + T] for s in starts])
    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)

    def rot(t):
        a, b = t[..., : c11.DH // 2], t[..., c11.DH // 2:]
        return torch.cat([a * cos - b * sin, a * sin + b * cos], -1)

    rows = []  # layer, batch, head: the last query's weights over all T keys
    with torch.no_grad():
        h = model.emb(x)
        B = len(x)
        causal = torch.ones(T, T, dtype=torch.bool).tril()
        for blk in model.blocks:
            q, k, v = blk.qkv(blk.n1(h)).view(B, T, 3, c11.HEADS, c11.DH).permute(2, 0, 3, 1, 4)
            q, k = rot(q), rot(k)
            s = ((q @ k.transpose(-1, -2)) / math.sqrt(c11.DH)).masked_fill(~causal, float("-inf"))
            p = torch.softmax(s, -1)
            rows.append(p[:, :, -1].numpy())
            h = h + blk.o((p @ v).transpose(1, 2).reshape(B, T, -1))
            h = h + blk.f2(F.gelu(blk.f1(blk.n2(h))))
    best = None
    for li, P in enumerate(rows):
        for b in range(P.shape[0]):
            for hh in range(P.shape[1]):
                r = P[b, hh]
                strip = r[-NROW:]
                if strip.sum() < 0.85:  # the picture shows only the last 48 keys: they must hold nearly all of it
                    continue
                top, win = np.sort(strip)[-KEEP:].sum(), strip[-KEEP:].sum()
                if strip.max() > 0.4 or top < 0.6:  # spread over several keys, most of it in a few
                    continue
                far = int((np.argsort(-strip)[:KEEP] < NROW - KEEP).sum())
                score = top - win + 0.02 * far
                if best is None or score > best[0]:
                    best = (score, li, b, hh)
    _, li, b, hh = best
    r = rows[li][b, hh].astype(float)
    strip = r[-NROW:]
    text = "".join(chars[i] for i in x[b, -NROW:].tolist())  # the last 48 keys; the last one is the query's own character
    top = np.argsort(-strip)[:KEEP]
    blocks = strip.reshape(-1, BLOCK).sum(1)
    chosen = np.argsort(-blocks)[:2]
    nsa = np.zeros(NROW, bool)
    for c in chosen:
        nsa[c * BLOCK:(c + 1) * BLOCK] = True
    nsa[-KEEP:] = True
    out = dict(layer=li, head=hh, text=text, weights=strip, strip_mass=float(strip.sum()),
               window=float(strip[-KEEP:].sum()), topk=float(strip[top].sum()), top=np.sort(top),
               blocks=blocks, chosen=np.sort(chosen), nsa=float(strip[nsa].sum()), nsa_keys=int(nsa.sum()))
    print("    layer {} head {}: strip {:.2f}; window {:.2f}, NSA {:.2f} ({} keys), top-{} {:.2f}; {!r}".format(
        li + 1, hh + 1, out["strip_mass"], out["window"], out["nsa"], out["nsa_keys"], KEEP, out["topk"], text))
    assert out["topk"] > out["window"]
    return out


ITEMS = {
    "lm_runs": compute_lm_runs,
    "moe": compute_moe,
    "speed": compute_speed,
    "balance": compute_balance,
    "fine": compute_fine,
    "capacity": compute_capacity,
    "parallel": compute_parallel,
    "upcycle": compute_upcycle,
    "special": compute_special,
    "mod": compute_mod,
    "gradcheck": compute_gradcheck,
    "mix1991": compute_mix1991,
    "accounting": compute_accounting,
    "configs": compute_configs,
    "recall": compute_recall,
    "lottery": compute_lottery,
    "prune24": compute_prune24,
    "actsparse": compute_actsparse,
    "topk": compute_topk,
    "row": compute_row,
    "scoreboard": compute_scoreboard,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
