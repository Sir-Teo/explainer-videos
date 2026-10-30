"""Synthetic memory tests for Part 15, and the small models that take them.

    MQAR    multi-query associative recall (Arora et al., Zoology, 2023): N key-value pairs, then the keys again in a
            new order; the model must answer each with its value
    ruler   three RULER-style tasks (Hsieh et al. 2024) on a stream of filler: one needle; one needle among several
            look-alikes (multi-key); and variable tracking (a value passed along a chain of names)

A run is a pure function of its settings and seed (``train_mqar``, ``train_ruler``), so runs can go to separate
processes (``spawn``) and be cached piece by piece (``CACHE.partial``).
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn.functional as F

from videos.ai.ai15.mixers import Net

# ---------------------------------------------------------------------------
# MQAR
# ---------------------------------------------------------------------------
NK, NV = 32, 32  # key and value vocabularies (keys 0..31, values 32..63)
VOC = NK + NV
D = 64
MIXERS = {  # name: layers
    "softmax": ["softmax", "softmax"],
    "linear": ["linear", "linear"],
    "mamba2": ["mamba2", "mamba2"],
    "delta": ["delta", "delta"],
    "gdn": ["gdn", "gdn"],
    "hybrid": ["gdn", "softmax"],
}


def mqar_batch(g: np.random.Generator, n: int, N: int):
    keys = np.stack([g.permutation(NK)[:N] for _ in range(n)])
    vals = g.integers(0, NV, (n, N)) + NK
    order = np.stack([g.permutation(N) for _ in range(n)])
    pairs = np.stack([keys, vals], 2).reshape(n, 2 * N)
    qk = np.take_along_axis(keys, order, 1)
    ans = np.take_along_axis(vals, order, 1)
    x = np.concatenate([pairs, qk], 1)
    y = np.full(x.shape, -100)
    y[:, 2 * N:] = ans
    return torch.tensor(x), torch.tensor(y)


def mqar_model(mixer: str, dk: int, seed: int) -> Net:
    torch.manual_seed(seed)
    return Net(VOC, D, MIXERS[mixer], dk, mlp=2 * D, chunk=64)


def train_mqar(mixer: str, dk: int, N: int, seed: int, steps: int = 1000, batch: int = 32, lr: float = 3e-3,
               eval_every: int = 50, replay: bool = False, threads: int = 1) -> dict:
    """Train one model on MQAR with N pairs; recall (answers right) on a fixed batch along the way, and at the end
    on 1,024 fresh lists.  ``replay``: also keep, at every evaluation, which answers of one fixed list are right."""
    torch.set_num_threads(threads)
    m = mqar_model(mixer, dk, seed)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.1)
    g = np.random.default_rng(1000 * seed + N)
    xe, ye = mqar_batch(np.random.default_rng(20_000 + N), 256, N)
    curve, picks = [], []
    t0 = time.time()
    for step in range(steps + 1):
        if step % eval_every == 0:
            with torch.no_grad():
                p, mk = m(xe).argmax(-1), ye >= 0
                curve.append((step, float((p[mk] == ye[mk]).float().mean())))
                if replay:
                    picks.append((p[0, 2 * N:] == ye[0, 2 * N:]).int().tolist())
        if step == steps:
            break
        x, y = mqar_batch(g, batch, N)
        loss = F.cross_entropy(m(x).reshape(-1, VOC), y.reshape(-1), ignore_index=-100)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        sched.step()
    with torch.no_grad():
        x, y = mqar_batch(np.random.default_rng(10_000 + N), 1024, N)
        p = m(x).argmax(-1)
        mk = y >= 0
        acc = float((p[mk] == y[mk]).float().mean())
    out = dict(mixer=mixer, dk=dk, N=N, seed=seed, acc=acc, curve=curve, params=m.n_params(),
               state=max(mx.state_numbers(3 * N) for mx in m.mix), seconds=time.time() - t0)
    if replay:
        out["picks"] = picks
        xr = xe[0].tolist()
        out["example"] = xr
    return out


# ---------------------------------------------------------------------------
# RULER-style tasks
# ---------------------------------------------------------------------------
# vocabulary: filler words 0..63, names 64..95, numbers 96..127, and markers
FILL, NAMES, NUMS = 64, 32, 32
IS, ASK, EQ = 128, 129, 130
RVOC = 131
TASKS = ("needle", "multikey", "vartrack")


def ruler_example(g: np.random.Generator, task: str, T: int):
    """One sequence of length T and the position whose next token is the answer (and the answer)."""
    x = list(g.integers(0, FILL, T))  # filler
    ask_len = 3
    body = T - ask_len
    if task == "needle":  # "name is number" somewhere; at the end "ask name" -> number
        name, num = int(g.integers(0, NAMES)) + FILL, int(g.integers(0, NUMS)) + FILL + NAMES
        p = int(g.integers(0, body - 3))
        x[p:p + 3] = [name, IS, num]
        q, ans = name, num
    elif task == "multikey":  # four needles with different names; ask for one of them
        names = g.permutation(NAMES)[:4] + FILL
        nums = g.integers(0, NUMS, 4) + FILL + NAMES
        slots = np.sort(g.choice(np.arange(0, body - 3, 3), 4, replace=False))
        for s, a, b in zip(slots, names, nums):
            x[s:s + 3] = [int(a), IS, int(b)]
        j = int(g.integers(0, 4))
        q, ans = int(names[j]), int(nums[j])
    else:  # vartrack: "A is 7", later "B = A", later "C = B"; ask C -> 7
        names = g.permutation(NAMES)[:3] + FILL
        num = int(g.integers(0, NUMS)) + FILL + NAMES
        slots = np.sort(g.choice(np.arange(0, body - 3, 3), 3, replace=False))
        x[slots[0]:slots[0] + 3] = [int(names[0]), IS, num]
        x[slots[1]:slots[1] + 3] = [int(names[1]), EQ, int(names[0])]
        x[slots[2]:slots[2] + 3] = [int(names[2]), EQ, int(names[1])]
        q, ans = int(names[2]), num
    x[body:] = [ASK, q, IS]
    return x, ans


def ruler_batch(g, n, T, tasks=TASKS):
    xs, ys = [], []
    for i in range(n):
        x, a = ruler_example(g, tasks[i % len(tasks)], T)
        xs.append(x)
        ys.append(a)
    return torch.tensor(xs), torch.tensor(ys)


RULER_MIXERS = {"softmax": ["softmax", "softmax"], "gdn": ["gdn", "gdn"], "hybrid": ["gdn", "softmax"],
                "mamba2": ["mamba2", "mamba2"]}


def train_ruler(mixer: str, seed: int, T: int = 128, steps: int = 1500, batch: int = 32, lr: float = 2e-3,
                dk: int = 16, eval_lengths=(128, 256, 512, 1024), eval_n: int = 192, eval_every: int = 100,
                threads: int = 1) -> dict:
    """Train on a mix of the three tasks at length T; accuracy on each task at each length (longer than trained)."""
    torch.set_num_threads(threads)
    torch.manual_seed(seed)
    m = Net(RVOC, D, RULER_MIXERS[mixer], dk, mlp=2 * D, chunk=64)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.1)
    g = np.random.default_rng(500 + seed)
    xe, ye = ruler_batch(np.random.default_rng(31), 96, T)
    curve = []
    t0 = time.time()
    for step in range(steps + 1):
        if step % eval_every == 0:
            with torch.no_grad():
                curve.append((step, float((m(xe)[:, -1].argmax(-1) == ye).float().mean())))
        if step == steps:
            break
        x, y = ruler_batch(g, batch, T)
        loss = F.cross_entropy(m(x)[:, -1], y)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        sched.step()
    acc = {}
    with torch.no_grad():
        for L in eval_lengths:
            for task in TASKS:
                x, y = ruler_batch(np.random.default_rng(7000 + L), eval_n, L, tasks=(task,))
                hits = 0
                for i in range(0, eval_n, 32):
                    hits += int((m(x[i:i + 32])[:, -1].argmax(-1) == y[i:i + 32]).sum())
                acc[f"{task}_{L}"] = hits / eval_n
    return dict(mixer=mixer, seed=seed, T=T, curve=curve, acc=acc, params=m.n_params(), seconds=time.time() - t0)


def chance(task: str) -> float:
    return 1.0 / NUMS
