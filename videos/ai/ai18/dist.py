"""Processes on this computer as a small cluster, through PyTorch's own distributed stack (``torch.distributed`` with
the gloo backend, which runs on any CPU, macOS or Linux).

    out = run(w_collectives, 4, sizes, reps)       # a list: each rank's result

Workers live in this module so that the ``spawn`` start method (the only safe one with torch on macOS) can import
them; each writes its result as JSON, which ``run`` collects.  Every worker uses one thread.
"""

from __future__ import annotations

import json
import math
import os
import socket
import tempfile
import time

import numpy as np
import torch
import torch.distributed as dist
import torch.nn.functional as F


def _init(rank: int, p: int, port: int) -> None:
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = str(port)
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    torch.set_num_threads(1)
    dist.init_process_group("gloo", rank=rank, world_size=p)


def _done(d: str, rank: int, res: dict) -> None:
    with open(os.path.join(d, f"{rank}.json"), "w") as f:
        json.dump(res, f)
    dist.barrier()
    dist.destroy_process_group()


def run(fn, p: int, *args) -> list:
    import torch.multiprocessing as mp

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    with tempfile.TemporaryDirectory() as d:
        mp.start_processes(fn, args=(p, port, d) + tuple(args), nprocs=p, start_method="spawn")
        out = []
        for r in range(p):
            with open(os.path.join(d, f"{r}.json")) as f:
                out.append(json.load(f))
    return out


# ---------------------------------------------------------------------------
# Collectives, timed
# ---------------------------------------------------------------------------
def w_collectives(rank, p, port, d, sizes, reps):
    """Point-to-point (ranks 0 and 1), all-reduce, reduce-scatter and all-gather, for each size in bytes; every rank
    records its own time for every repetition; the sums are checked."""
    _init(rank, p, port)
    res = {"pingpong": [], "all_reduce": [], "reduce_scatter": [], "all_gather": [], "ok": True}
    for n in sizes:
        m = max(n // 4, 1)
        buf = torch.zeros(m)
        best = float("inf")
        for _ in range(reps):
            dist.barrier()
            if rank == 0:
                t = time.perf_counter()
                dist.send(buf, 1)
                dist.recv(buf, 1)
                best = min(best, (time.perf_counter() - t) / 2)
            elif rank == 1:
                dist.recv(buf, 0)
                dist.send(buf, 0)
        res["pingpong"].append(best)
    for n in sizes:
        m = max(n // 4 // p * p, p)  # elements, a multiple of p
        ts = {"all_reduce": [], "reduce_scatter": [], "all_gather": []}
        for r_ in range(reps):
            x = torch.full((m,), float(rank + 1)) + torch.arange(m, dtype=torch.float32) % 7
            dist.barrier()
            t = time.perf_counter()
            dist.all_reduce(x)
            ts["all_reduce"].append(time.perf_counter() - t)
            if r_ == 0:
                want = p * (p + 1) / 2 + p * (torch.arange(m, dtype=torch.float32) % 7)
                res["ok"] &= bool(torch.allclose(x, want))
            chunks = [torch.full((m // p,), float(rank + 1)) for _ in range(p)]
            out = torch.empty(m // p)
            dist.barrier()
            t = time.perf_counter()
            dist.reduce_scatter(out, chunks)
            ts["reduce_scatter"].append(time.perf_counter() - t)
            if r_ == 0:
                res["ok"] &= bool(torch.allclose(out, torch.full_like(out, p * (p + 1) / 2)))
            parts = [torch.empty(m // p) for _ in range(p)]
            mine = torch.full((m // p,), float(rank))
            dist.barrier()
            t = time.perf_counter()
            dist.all_gather(parts, mine)
            ts["all_gather"].append(time.perf_counter() - t)
            if r_ == 0:
                res["ok"] &= all(bool((q_ == k).all()) for k, q_ in enumerate(parts))
        for k, v in ts.items():
            res[k].append(v)
    _done(d, rank, res)


# ---------------------------------------------------------------------------
# Data parallelism and ZeRO-3 / FSDP, against one process
# ---------------------------------------------------------------------------
TINY = dict(d=32, layers=2, heads=2, seq=64)
DP_STEPS, DP_BATCH = 6, 16
ADAM = dict(lr=3e-3, b1=0.9, b2=0.95, eps=1e-8, wd=0.1)


def tiny_model():
    from explainer.lm import pocket

    torch.manual_seed(0)
    return pocket.PocketGPT(pocket.Config(vocab=4096, **TINY))


def dp_batches():
    from explainer.ai import novels as N

    tr, _ = N.token_arrays()
    g = np.random.default_rng(1818)
    T = TINY["seq"]
    out = []
    for _ in range(DP_STEPS):
        ix = g.integers(0, len(tr) - T - 1, DP_BATCH)
        out.append(torch.from_numpy(np.stack([tr[i:i + T + 1] for i in ix]).astype(np.int64)))
    return out


def units(model):
    """The model cut into the units ZeRO-3 / FSDP gathers one at a time: the embedding, each block, the head."""
    return [("emb", model.emb)] + [(f"blocks.{i}", b) for i, b in enumerate(model.blocks)] + \
        [("final", torch.nn.ModuleDict({"norm": model.norm, "head": model.head}))]


def flat(params) -> torch.Tensor:
    return torch.cat([p.detach().reshape(-1) for p in params])


def adamw(x, g, m, v, t):
    """AdamW on flat tensors, element by element (so a shard updates exactly as its piece of the whole)."""
    a = ADAM
    m.mul_(a["b1"]).add_(g, alpha=1 - a["b1"])
    v.mul_(a["b2"]).addcmul_(g, g, value=1 - a["b2"])
    mh = m / (1 - a["b1"] ** t)
    vh = v / (1 - a["b2"] ** t)
    x.mul_(1 - a["lr"] * a["wd"]).addcdiv_(mh, vh.sqrt().add_(a["eps"]), value=-a["lr"])


def loss_of(model, x):
    lg = model(x[:, :-1])
    return F.cross_entropy(lg.flatten(0, 1), x[:, 1:].flatten())


def reference_run() -> dict:
    """One process, the whole batch: the run the distributed versions must reproduce."""
    torch.set_num_threads(1)
    model = tiny_model()
    params = [p for _, u in units(model) for p in u.parameters()]
    x = flat(params)
    m, v = torch.zeros_like(x), torch.zeros_like(x)
    losses = []
    for t, b in enumerate(dp_batches(), 1):
        torch.nn.utils.vector_to_parameters(x, params)
        for p_ in params:
            p_.grad = None
        loss = loss_of(model, b)
        loss.backward()
        g = torch.cat([p_.grad.reshape(-1) for p_ in params])
        adamw(x, g, m, v, t)
        losses.append(float(loss))
    return dict(x=x, losses=losses, n=int(x.numel()))


def w_dp(rank, p, port, d, mode):
    """mode 'dp': every rank keeps everything and all-reduces the gradients.  mode 'zero3': every rank keeps a 1/p
    shard of each unit's parameters, gradients and Adam moments; a unit's parameters are all-gathered when the
    forward pass reaches it and again when the backward pass does (they are freed in between, as FSDP does), and its
    gradients are reduce-scattered."""
    _init(rank, p, port)
    from torch.func import functional_call

    model = tiny_model()
    us = units(model)
    batches = dp_batches()
    per = DP_BATCH // p
    sent = 0.0  # elements this rank sends, counted as a ring sends them
    t_comm = 0.0
    losses = []
    if mode == "dp":
        params = [p_ for _, u in us for p_ in u.parameters()]
        x = flat(params)
        m, v = torch.zeros_like(x), torch.zeros_like(x)
        for t, b in enumerate(batches, 1):
            torch.nn.utils.vector_to_parameters(x, params)
            for p_ in params:
                p_.grad = None
            loss = loss_of(model, b[rank * per:(rank + 1) * per])
            loss.backward()
            g = torch.cat([p_.grad.reshape(-1) for p_ in params])
            t0 = time.perf_counter()
            dist.all_reduce(g)
            t_comm += time.perf_counter() - t0
            sent += 2 * (p - 1) / p * g.numel()
            g /= p
            adamw(x, g, m, v, t)
            lv = torch.tensor([float(loss)])
            dist.all_reduce(lv)
            losses.append(float(lv) / p)
        full = x
        persistent = 4 * x.numel()  # parameters, gradients, two Adam moments (FP32 each)
        transient = 0
    else:
        names = [[n for n, _ in u.named_parameters()] for _, u in us]
        shapes = [[p_.shape for _, p_ in u.named_parameters()] for _, u in us]
        sizes = [sum(int(np.prod(s)) for s in sh) for sh in shapes]
        padded = [int(math.ceil(n / p) * p) for n in sizes]
        shards = []
        for (_, u), n, P_ in zip(us, sizes, padded):
            f_ = torch.cat([flat(u.parameters()), torch.zeros(P_ - n)])
            shards.append(f_.reshape(p, -1)[rank].clone().requires_grad_())
        moments = [(torch.zeros_like(s_.detach()), torch.zeros_like(s_.detach())) for s_ in shards]
        stats = {"sent": 0.0, "comm": 0.0, "peak": 0}

        def gather(k):
            parts = [torch.empty_like(shards[k]) for _ in range(p)]
            t0 = time.perf_counter()
            dist.all_gather(parts, shards[k].detach())
            stats["comm"] += time.perf_counter() - t0
            stats["sent"] += (p - 1) / p * padded[k]
            stats["peak"] = max(stats["peak"], padded[k])
            return torch.cat(parts)[:sizes[k]]

        def as_dict(k, vec):
            out, o = {}, 0
            for nm, sh in zip(names[k], shapes[k]):
                c = int(np.prod(sh))
                out[nm] = vec[o:o + c].view(sh)
                o += c
            return out

        def apply(k, inp, vec, tgt=None):
            mod = us[k][1]
            if k == len(us) - 1:
                lg = functional_call(mod["head"], {"weight": as_dict(k, vec)["head.weight"]},
                                     (functional_call(mod["norm"], {"weight": as_dict(k, vec)["norm.weight"]},
                                                      (inp,)),))
                return F.cross_entropy(lg.flatten(0, 1), tgt.flatten())
            return functional_call(mod, as_dict(k, vec), (inp,))

        class Unit(torch.autograd.Function):
            @staticmethod
            def forward(ctx, inp, shard, k, tgt):
                vec = gather(k)
                with torch.no_grad():
                    y = apply(k, inp, vec, tgt)
                del vec  # freed: only this rank's shard stays
                ctx.save_for_backward(inp)
                ctx.k, ctx.tgt = k, tgt
                return y

            @staticmethod
            def backward(ctx, gy):
                (inp,) = ctx.saved_tensors
                k = ctx.k
                vec = gather(k).requires_grad_()
                xin = inp.detach().requires_grad_(inp.is_floating_point())
                with torch.enable_grad():
                    y = apply(k, xin, vec, ctx.tgt)
                    wrt = [vec] + ([xin] if xin.requires_grad else [])
                    gs = torch.autograd.grad(y, wrt, gy)
                gfull = torch.cat([gs[0], torch.zeros(padded[k] - sizes[k])])
                out = torch.empty_like(shards[k].detach())
                t0 = time.perf_counter()
                dist.reduce_scatter(out, list(gfull.reshape(p, -1)))
                stats["comm"] += time.perf_counter() - t0
                stats["sent"] += (p - 1) / p * padded[k]
                return (gs[1] if xin.requires_grad else None), out, None, None

        for t, b in enumerate(batches, 1):
            xb = b[rank * per:(rank + 1) * per]
            h = xb[:, :-1]
            for k in range(len(us) - 1):
                h = Unit.apply(h, shards[k], k, None)
            loss = Unit.apply(h, shards[-1], len(us) - 1, xb[:, 1:])
            for s_ in shards:
                s_.grad = None
            loss.backward()
            with torch.no_grad():
                for k in range(len(us)):
                    adamw(shards[k], shards[k].grad / p, *moments[k], t)
            lv = torch.tensor([float(loss)])
            dist.all_reduce(lv)
            losses.append(float(lv) / p)
        sent, t_comm = stats["sent"], stats["comm"]
        with torch.no_grad():
            full = torch.cat([gather(k) for k in range(len(us))])
        persistent = 4 * sum(s_.numel() for s_ in shards)
        transient = stats["peak"]
    ref_n = int(full.numel())
    res = dict(mode=mode, p=p, losses=losses, sent_per_step=sent / len(batches), comm_seconds=t_comm,
               persistent_elems=persistent, transient_elems=transient, n=ref_n)
    if rank == 0:
        torch.save(full, os.path.join(d, "params.pt"))
        res["params"] = full.tolist()
    _done(d, rank, res)


# ---------------------------------------------------------------------------
# Megatron tensor parallelism on one block
# ---------------------------------------------------------------------------
TP = dict(d=64, heads=4, seq=32, batch=2)


class _F(torch.autograd.Function):
    """Megatron's f: the identity going forward, an all-reduce of the gradient going back."""

    @staticmethod
    def forward(ctx, x):
        return x

    @staticmethod
    def backward(ctx, g):
        g = g.clone()
        dist.all_reduce(g)
        _F.calls += 1
        return g


class _G(torch.autograd.Function):
    """Megatron's g: an all-reduce going forward, the identity going back."""

    @staticmethod
    def forward(ctx, x):
        x = x.clone()
        dist.all_reduce(x)
        _G.calls += 1
        return x

    @staticmethod
    def backward(ctx, g):
        return g


_F.calls = 0
_G.calls = 0


def tp_block():
    from explainer.lm import pocket

    torch.manual_seed(7)
    cfg = pocket.Config(vocab=64, d=TP["d"], layers=2, heads=TP["heads"], seq=TP["seq"])
    blk = pocket.Block(cfg)
    for p_ in blk.parameters():
        if p_.dim() == 2:
            torch.nn.init.normal_(p_, std=1 / math.sqrt(p_.shape[1]))
    g = torch.Generator().manual_seed(8)
    x = torch.randn(TP["batch"], TP["seq"], TP["d"], generator=g)
    gy = torch.randn(TP["batch"], TP["seq"], TP["d"], generator=g)
    return blk, x, gy


def tp_reference() -> dict:
    blk, x, gy = tp_block()
    x = x.clone().requires_grad_()
    y = blk(x)
    y.backward(gy)
    return dict(y=y.detach(), gx=x.grad, grads={n: p_.grad for n, p_ in blk.named_parameters()})


def w_tp(rank, p, port, d):
    """One transformer block split across p ranks: attention by heads (Q, K, V by rows, the output projection by
    columns), the SwiGLU MLP by hidden units (gate and up by rows, down by columns).  Each half of the block is
    f, the local part, then g: one all-reduce forward and one back."""
    _init(rank, p, port)
    from explainer.lm.pocket import apply_rope

    blk, x, gy = tp_block()
    D, H = TP["d"], TP["heads"]
    hd, hl = D // H, H // p
    heads = list(range(rank * hl, (rank + 1) * hl))
    rows = [c * D + h * hd + j for c in range(3) for h in heads for j in range(hd)]
    cols = [h * hd + j for h in heads for j in range(hd)]
    hid = blk.mlp.gate.weight.shape[0]
    hrows = list(range(rank * hid // p, (rank + 1) * hid // p))
    W = {"qkv": blk.attn.qkv.weight.detach()[rows].clone().requires_grad_(),
         "out": blk.attn.out.weight.detach()[:, cols].clone().requires_grad_(),
         "gate": blk.mlp.gate.weight.detach()[hrows].clone().requires_grad_(),
         "up": blk.mlp.up.weight.detach()[hrows].clone().requires_grad_(),
         "down": blk.mlp.down.weight.detach()[:, hrows].clone().requires_grad_()}
    n1, n2 = blk.n1, blk.n2
    xin = x.clone().requires_grad_()
    B, T = x.shape[0], x.shape[1]
    # attention, local heads
    a = _F.apply(n1(xin))
    q, k, v = (a @ W["qkv"].t()).view(B, T, 3, hl, hd).permute(2, 0, 3, 1, 4)
    q, k = apply_rope(q, blk.attn.cos, blk.attn.sin), apply_rope(k, blk.attn.cos, blk.attn.sin)
    o = F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, hl * hd)
    h1 = xin + _G.apply(o @ W["out"].t())
    # MLP, local hidden units
    b = _F.apply(n2(h1))
    y = h1 + _G.apply((F.silu(b @ W["gate"].t()) * (b @ W["up"].t())) @ W["down"].t())
    fwd_calls = _G.calls
    y.backward(gy)
    ref = tp_reference()
    err_y = float((y.detach() - ref["y"]).abs().max())
    err_gx = float((xin.grad - ref["gx"]).abs().max())
    gref = {"qkv": ref["grads"]["attn.qkv.weight"][rows], "out": ref["grads"]["attn.out.weight"][:, cols],
            "gate": ref["grads"]["mlp.gate.weight"][hrows], "up": ref["grads"]["mlp.up.weight"][hrows],
            "down": ref["grads"]["mlp.down.weight"][:, hrows]}
    err_w = max(float((W[k_].grad - gref[k_]).abs().max()) for k_ in W)
    scale = float(ref["y"].abs().max())
    local = sum(w.numel() for w in W.values())
    full = sum(p_.numel() for n_, p_ in blk.named_parameters() if p_.dim() == 2)
    res = dict(p=p, err_y=err_y, err_gx=err_gx, err_w=err_w, y_scale=scale, fwd_allreduce=fwd_calls,
               bwd_allreduce=_F.calls, act_elems=B * T * D, local_weights=local, full_weights=full)
    _done(d, rank, res)


# ---------------------------------------------------------------------------
# Context parallelism: ring attention
# ---------------------------------------------------------------------------
RA = dict(T=256, heads=2, hd=32)


def ra_qkv():
    g = torch.Generator().manual_seed(9)
    return [torch.randn(1, RA["heads"], RA["T"], RA["hd"], generator=g) for _ in range(3)]


def w_ring_attention(rank, p, port, d):
    """Causal attention over a sequence split into p blocks, one per rank: the key-value blocks travel round the
    ring, and each rank folds each block into its output with the online softmax (running max and sum)."""
    _init(rank, p, port)
    Q, K, V = ra_qkv()
    L = RA["T"] // p
    sl = slice(rank * L, (rank + 1) * L)
    q, kv = Q[:, :, sl], torch.cat([K[:, :, sl], V[:, :, sl]], 1)
    scale = 1 / math.sqrt(RA["hd"])
    m = torch.full((1, RA["heads"], L, 1), -float("inf"))
    l_ = torch.zeros_like(m)
    o = torch.zeros_like(q)
    blocks = 0
    for s in range(p):
        j = (rank - s) % p  # whose keys and values this rank holds now
        if j <= rank:
            k, v = kv[:, :RA["heads"]], kv[:, RA["heads"]:]
            sc = (q @ k.transpose(-2, -1)) * scale
            if j == rank:
                sc = sc.masked_fill(~torch.ones(L, L, dtype=torch.bool).tril(), -float("inf"))
            mn = torch.maximum(m, sc.amax(-1, keepdim=True))
            pexp = torch.exp(sc - mn)
            corr = torch.exp(m - mn)
            l_ = l_ * corr + pexp.sum(-1, keepdim=True)
            o = o * corr + pexp @ v
            m = mn
            blocks += 1
        if s < p - 1:
            nxt = torch.empty_like(kv)
            reqs = [dist.isend(kv.contiguous(), (rank + 1) % p), dist.irecv(nxt, (rank - 1) % p)]
            for r_ in reqs:
                r_.wait()
            kv = nxt
    out = o / l_
    ref = F.scaled_dot_product_attention(Q, K, V, is_causal=True)[:, :, sl]
    res = dict(rank=rank, err=float((out - ref).abs().max()), blocks=blocks, sent_elems=(p - 1) * kv.numel())
    _done(d, rank, res)
