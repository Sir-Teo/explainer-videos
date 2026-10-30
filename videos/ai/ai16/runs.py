"""Training runs for Part 16, each a plain function of a JSON-able spec, so a pool of single-threaded workers (started
with ``spawn``, safe on macOS) can train them side by side and ``compute.py`` can cache each one as it finishes.

    out = train(dict(cfg=dict(ffn="moe", E=8, k=2, he=128, gate="sigmoid", balance="bias"), seed=0, steps=2400))

The data are Part 11's characters of the thirty novels (``char_data``), read in windows of ``ctx`` characters.
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np

STEPS, BATCH, LR, WARM = 2400, 32, 3e-3, 100
SNAPS = (0, 50, 100, 200, 400, 800, 1600, 2400)  # replay checkpoints
LOAD_EVERY = 20
EVAL_WINDOWS = 96  # held-out windows for the curves (96 x 64 characters)

_DATA = {}


def lm_data():
    """Part 11's characters (train, held-out, vocabulary size), the scoreboard's passage in the same code, and the
    characters themselves."""
    if "lm" not in _DATA:
        from videos.ai.ai1 import compute as c1
        from videos.ai.ai11.compute import char_data

        tr, va, K = char_data()
        texts = {k: c1.text(k) for k in ("train", "valid")}
        chars = sorted(set("".join(texts.values())))
        idx = {ch: i for i, ch in enumerate(chars)}
        ps = np.array([idx[ch] for ch in c1.text("passage")])
        assert len(chars) == K
        _DATA["lm"] = (np.asarray(tr, np.int64), np.asarray(va, np.int64), K, ps, chars)
    return _DATA["lm"]


def windows(seq, starts, T):
    import torch

    idx = np.asarray(starts)[:, None] + np.arange(T + 1)[None]
    w = torch.from_numpy(np.asarray(seq)[idx])
    return w[:, :-1], w[:, 1:]


def lm_bits(model, seq, T, n=None, stride=None, **kw):
    """Bits per character.  Without ``stride``: ``n`` fixed windows, every position scored.  With it: windows ``stride``
    apart over the whole sequence, each scored on its last ``stride`` characters (the first window whole)."""
    import torch
    import torch.nn.functional as F

    model.eval()
    tot, cnt = 0.0, 0
    with torch.no_grad():
        if stride is None:
            starts = np.linspace(0, len(seq) - T - 2, n).astype(int)
            for i in range(0, len(starts), 32):
                x, y = windows(seq, starts[i:i + 32], T)
                z = model(x, **kw)
                tot += float(F.cross_entropy(z.reshape(-1, z.shape[-1]), y.reshape(-1), reduction="sum"))
                cnt += y.numel()
        else:
            starts = list(range(0, len(seq) - T - 1, stride))
            for i in range(0, len(starts), 32):
                ss = starts[i:i + 32]
                x, y = windows(seq, ss, T)
                z = model(x, **kw)
                ce = F.cross_entropy(z.reshape(-1, z.shape[-1]), y.reshape(-1), reduction="none").view(len(ss), T)
                keep = torch.zeros_like(ce, dtype=torch.bool)
                keep[:, T - stride:] = True
                if i == 0:
                    keep[0] = True
                tot += float(ce[keep].sum())
                cnt += int(keep.sum())
    model.train()
    return tot / cnt / math.log(2)


def route_counts(model, va, T, K):
    """For each MoE layer: how often each current character's tokens go to each expert (every one of its k slots),
    on a fixed stretch of held-out text: layers x K x E counts; and the first choice only."""
    import torch

    starts = np.linspace(0, len(va) - T - 2, 64).astype(int)
    x, _ = windows(va, starts, T)
    model.eval()
    with torch.no_grad():
        model(x, probe=True)
    model.train()
    cur = x.reshape(-1).numpy()
    allc, first = [], []
    for m in model.moes():
        top = m.top.reshape(-1, m.c.k).numpy()
        A = np.zeros((K, m.c.E))
        np.add.at(A, (np.repeat(cur, m.c.k), top.reshape(-1)), 1)
        Fc = np.zeros((K, m.c.E))
        np.add.at(Fc, (cur, top[:, 0]), 1)
        allc.append(A)
        first.append(Fc)
    return np.array(allc), np.array(first)


def build(cfg: dict):
    from videos.ai.ai16.nets import Cfg, Net

    return Net(Cfg(**cfg))


def lr_at(step, steps, warm=WARM):
    if step < warm:
        return (step + 1) / warm
    t = (step - warm) / max(1, steps - warm)
    return 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * t))


def train(spec: dict) -> dict:
    """One training run.  ``spec``: cfg (Net config), seed, steps, lr, batch, task ('lm' or 'recall'), init (a saved
    state to start from), upcycle (a saved dense state to upcycle from), start_step (where the schedule resumes),
    save (where to keep the final weights), save_at (a step at which to also save them), snaps (replay steps),
    route (record routing tables), warm_index (steps of indexer warm-up against the dense attention)."""
    import torch
    import torch.nn.functional as F

    torch.set_num_threads(int(spec.get("threads", 1)))
    seed = int(spec.get("seed", 0))
    torch.manual_seed(seed)
    task = spec.get("task", "lm")
    if task == "lm":
        tr, va, K, ps, _ = lm_data()
    else:
        from videos.ai.ai16 import recall as R

        K = R.VOCAB
    cfg = dict(spec["cfg"])
    cfg.setdefault("vocab", K)
    from videos.ai.ai16.nets import Cfg, Net, upcycle

    if spec.get("upcycle"):
        dcfg = dict(cfg, ffn="dense", hidden=cfg["he"], gate="softmax", balance="none")
        dense = Net(Cfg(**{k: v for k, v in dcfg.items()}))
        dense.load_state_dict(torch.load(spec["upcycle"], weights_only=True))
        model = upcycle(dense, Cfg(**cfg), noise=0.01, seed=seed)
    else:
        model = Net(Cfg(**cfg))
        if spec.get("init"):
            missing = model.load_state_dict(torch.load(spec["init"], weights_only=True), strict=False)
            assert all(("attn.i" in k) or ("bias" in k) for k in missing.missing_keys), missing
    T = model.c.ctx
    steps, B = int(spec.get("steps", STEPS)), int(spec.get("batch", BATCH))
    lr = float(spec.get("lr", LR))
    total = int(spec.get("schedule_steps", steps))
    off = int(spec.get("start_step", 0))
    decay = [p for n, p in model.named_parameters() if p.dim() >= 2 and "router" not in n]
    other = [p for n, p in model.named_parameters() if p.dim() < 2 or "router" in n]
    opt = torch.optim.AdamW([dict(params=decay, weight_decay=0.1), dict(params=other, weight_decay=0.0)], lr=lr,
                            betas=(0.9, 0.95))
    g = np.random.default_rng(1000 + seed)
    snaps = set(spec.get("snaps", SNAPS))
    out = dict(curve=[], loads=[], drops=[], bias=[], routes=[], route_steps=[], mod_frac=[], index_kl=[])
    counts = model.counts()
    out.update(counts=counts, flops=model.flops(), cfg=model.c.to_dict())

    def evaluate(step):
        if task == "lm":
            b = lm_bits(model, va, T, EVAL_WINDOWS)
        else:
            b = R.accuracy(model, seed=99, n=256)
        out["curve"].append((off + step, b))
        if spec.get("route") and model.moes():
            A, Fc = route_counts(model, va, T, K)
            out["routes"].append(A)
            out["route_steps"].append(off + step)

    t0 = time.time()
    warm_index = int(spec.get("warm_index", 0))
    for step in range(steps + 1):
        if step in snaps or step == steps:
            evaluate(step)
        if step == spec.get("save_at"):
            torch.save(model.state_dict(), spec["save_mid"])
        if step == steps:
            break
        f = lr_at(off + step, total)
        for gr in opt.param_groups:
            gr["lr"] = lr * f
        if task == "lm":
            x, y = windows(tr, g.integers(0, len(tr) - T - 2, B), T)
        else:
            x, y, w = R.batch(g, B)
        z = model(x, index_target=step < warm_index)
        if task == "lm":
            loss = F.cross_entropy(z.reshape(-1, z.shape[-1]), y.reshape(-1))
        else:
            loss = (F.cross_entropy(z.reshape(-1, z.shape[-1]), y.reshape(-1), reduction="none") * w.reshape(-1)).sum() / w.sum()
        if step < warm_index:  # indexer warm-up: the model is frozen, only the indexer learns
            loss = loss.detach()
        total_loss = loss + model.extra_loss()
        opt.zero_grad(set_to_none=True)
        total_loss.backward()
        if step < warm_index:
            for n_, p in model.named_parameters():
                if "attn.i" not in n_:
                    p.grad = None
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        moes = model.moes()
        if moes and model.c.balance == "bias":
            for m in moes:
                m.update_bias()
        if step % LOAD_EVERY == 0:
            if moes:
                out["loads"].append([m.load.numpy().copy() for m in moes])
                out["drops"].append([m.dropped for m in moes])
                if model.c.balance == "bias":
                    out["bias"].append([m.bias.numpy().copy() for m in moes])
            if model.c.mod_layers:
                out["mod_frac"].append([float(b.keep.float().mean()) for b in model.blocks if b.routed])
            if model.c.attn == "index":
                out["index_kl"].append((step, float(sum(b.attn.index_kl for b in model.blocks)) / len(model.blocks)))
    out["seconds"] = time.time() - t0
    out["final"] = out["curve"][-1][1]
    if task == "lm":
        out["valid_bits"] = lm_bits(model, va, T, 400)
        out["passage_bits"] = lm_bits(model, ps, T, stride=T // 2)
        if model.c.mod_layers:
            out["valid_bits_causal"] = lm_bits(model, va, T, 400, causal_mod=True)
            model.eval()
            with __import__("torch").no_grad():
                starts = np.linspace(0, len(va) - T - 2, 64).astype(int)
                x, _ = windows(va, starts, T)
                model(x, causal_mod=True)
            out["causal_frac"] = [float(b.keep.float().mean()) for b in model.blocks if b.routed]
            model.train()
    if spec.get("save"):
        Path(spec["save"]).parent.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), spec["save"])
    for k_ in ("loads", "drops", "bias", "routes"):
        out[k_] = np.asarray(out[k_]).tolist() if len(out[k_]) else []
    return out


def pool_map(fn, specs, workers=2):
    """Run ``fn`` over ``specs`` in single-threaded worker processes (spawned: safe with torch on macOS); yields
    (spec, result) as each finishes."""
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor, as_completed

    if workers <= 1 or len(specs) <= 1:
        for s in specs:
            yield s, fn(s)
        return
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(fn, s): s for s in specs}
        for f in as_completed(futs):
            yield futs[f], f.result()
