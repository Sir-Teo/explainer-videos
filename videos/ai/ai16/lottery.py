"""The lottery ticket, found by iterative magnitude pruning with rewinding (Frankle & Carbin 2019; Frankle et al. 2020).

A small ReLU network reads the last three characters (one-hot) and guesses the next: 501 inputs, two hidden layers
of 128, 167 outputs.  Train it; remove the 20% smallest weights of each hidden layer (10% of the output layer);
rewind the survivors to their values early in training (step ``REWIND``) and train again; repeat.  Against it: the
same masks with fresh random weights ("re-initialized"), and random masks of the same sparsity ("random pruning").
"""

from __future__ import annotations

import math

import numpy as np

CTX3, H1, H2 = 3, 128, 128
STEPS, BATCH, LR, REWIND = 1000, 512, 2e-3, 50
ROUNDS = 8
RATE = (0.2, 0.2, 0.1)  # the share of the remaining weights pruned per round, by layer


def _data():
    from videos.ai.ai16.runs import lm_data

    tr, va, K, _, _ = lm_data()
    return tr, va, K


def _net(K, seed):
    import torch

    torch.manual_seed(seed)
    return torch.nn.Sequential(torch.nn.Linear(CTX3 * K, H1), torch.nn.ReLU(), torch.nn.Linear(H1, H2), torch.nn.ReLU(),
                               torch.nn.Linear(H2, K))


def _layers(net):
    return [net[0], net[2], net[4]]


def _x(seq, pos, K):
    import torch

    x = torch.zeros(len(pos), CTX3 * K)
    for j in range(CTX3):
        x[torch.arange(len(pos)), j * K + torch.from_numpy(seq[pos - CTX3 + j])] = 1.0
    return x


def bits(net, va, K, n=40_000):
    import torch
    import torch.nn.functional as F

    pos = np.arange(CTX3, CTX3 + n)
    with torch.no_grad():
        z = net(_x(va, pos, K))
        return float(F.cross_entropy(z, torch.from_numpy(va[pos]))) / math.log(2)


def train(state, masks, seed, tr, va, K, record=False):
    """Train from ``state`` (a list of weight tensors, already the initial values) with ``masks`` applied throughout;
    returns the final weights, the weights at REWIND, held-out bits, and (``record``) the share of hidden units that
    are exactly zero, through training."""
    import torch
    import torch.nn.functional as F

    torch.set_num_threads(1)
    net = _net(K, 0)
    with torch.no_grad():
        for L, (w, b), m in zip(_layers(net), state, masks):
            L.weight.copy_(w * m)
            L.bias.copy_(b)
    opt = torch.optim.Adam(net.parameters(), lr=LR)
    g = np.random.default_rng(500 + seed)
    rew, zeros = None, []
    for step in range(STEPS + 1):
        if step == REWIND:
            rew = [(L.weight.detach().clone(), L.bias.detach().clone()) for L in _layers(net)]
        if step == STEPS:
            break
        pos = g.integers(CTX3, len(tr) - 1, BATCH)
        x = _x(tr, pos, K)
        h1 = torch.relu(net[0](x))
        z = net[4](torch.relu(net[2](h1)))
        loss = F.cross_entropy(z, torch.from_numpy(tr[pos]))
        opt.zero_grad()
        loss.backward()
        opt.step()
        with torch.no_grad():
            for L, m in zip(_layers(net), masks):
                L.weight.mul_(m)
        if record and step % 25 == 0:
            with torch.no_grad():
                h2 = torch.relu(net[2](h1))
                zeros.append((step, float((h1 == 0).float().mean()), float((h2 == 0).float().mean())))
    final = [(L.weight.detach().clone(), L.bias.detach().clone()) for L in _layers(net)]
    return final, rew, bits(net, va, K), zeros


def prune(final, masks, rates):
    """Keep the largest-magnitude surviving weights of each layer: remove ``rate`` of those still there."""
    import torch

    out = []
    for (w, _), m, r in zip(final, masks, rates):
        alive = w[m.bool()].abs()
        n_cut = int(round(r * alive.numel()))
        thr = torch.kthvalue(alive, n_cut).values if n_cut > 0 else torch.tensor(-1.0)
        out.append(((w.abs() > thr) & m.bool()).float())
    return out


def run(seed: int, part=None) -> dict:
    """One seed's whole experiment (``part``: a dict-like to keep finished rounds in, so a killed run resumes)."""
    import torch

    tr, va, K = _data()
    torch.manual_seed(seed)
    net = _net(K, seed)
    init = [(L.weight.detach().clone(), L.bias.detach().clone()) for L in _layers(net)]
    full = [torch.ones_like(w) for w, _ in init]
    final, rew, b0, zeros = train(init, full, seed, tr, va, K, record=True)
    out = dict(dense=b0, zeros=zeros, ticket=[], reinit=[], random=[], remain=[], mask_img=[])
    tmask, gen = full, torch.Generator().manual_seed(77 + seed)
    for r in range(1, ROUNDS + 1):
        tmask = prune(final, tmask, RATE)
        final, _, bt, _ = train(rew, tmask, seed, tr, va, K)
        ri = _net(K, 1000 + seed + r)
        fresh = [(L.weight.detach().clone(), L.bias.detach().clone()) for L in _layers(ri)]
        _, _, br, _ = train(fresh, tmask, seed, tr, va, K)
        rmask = []
        for m in tmask:
            keep = int(m.sum())
            perm = torch.randperm(m.numel(), generator=gen)[:keep]
            rm = torch.zeros(m.numel())
            rm[perm] = 1.0
            rmask.append(rm.view_as(m))
        _, _, bm, _ = train(rew, rmask, seed, tr, va, K)
        remain = float(sum(m.sum() for m in tmask) / sum(m.numel() for m in tmask))
        out["ticket"].append(bt)
        out["reinit"].append(br)
        out["random"].append(bm)
        out["remain"].append(remain)
        # the second layer's mask, as a picture (its top-left 48 x 48 weights), round by round
        out["mask_img"].append(tmask[1].numpy()[:48, :48].astype(int).tolist())
        print(f"    seed {seed} round {r}: {100 * remain:.1f}% left; ticket {bt:.3f}, reinit {br:.3f}, random {bm:.3f}",
              flush=True)
    # the first hidden layer's surviving weights per input position (which of the three characters it reads)
    out["first_by_slot"] = [float(tmask[0].numpy().reshape(H1, CTX3, K)[:, j].mean()) for j in range(CTX3)]
    out["params"] = int(sum(w.numel() for w, _ in init))
    return out
