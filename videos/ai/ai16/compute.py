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


ITEMS = {
    "lm_runs": compute_lm_runs,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
