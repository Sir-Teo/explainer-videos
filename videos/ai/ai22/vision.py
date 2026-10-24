"""Part 22, chapters 1-2: a small vision transformer, replayed, and against a convolutional network of the same size.

    vit      the vision transformer of chapter 1 (its weights, ``vit.pt``, are REPA's teacher in chapter 4)
    vitcnn   ViT against a CNN with about as many weights, at equal steps and batches, on 3, 7 and 20 training fonts
"""

from __future__ import annotations

import numpy as np

from videos.ai.ai22.compute import CACHE, GL, NP, P, dataset, patches, steps, threads

D, H, L = 64, 4, 3


def vit_net(D=D, H=H, L=L):
    import torch
    import torch.nn as nn

    class ViT(nn.Module):
        """Patches of 4 x 4 pixels as 25 tokens, a summary token in front, learned positions (from zero), pre-norm
        transformer layers, a final layer norm; the summary token's last vector names the letter."""

        def __init__(self):
            super().__init__()
            self.embed = nn.Linear(P * P, D)
            self.cls = nn.Parameter(torch.zeros(1, 1, D))
            self.pos = nn.Parameter(torch.zeros(1, NP + 1, D))  # from zero, so what we see later is all learned
            self.layers = nn.ModuleList([nn.TransformerEncoderLayer(D, H, 4 * D, dropout=0.0, batch_first=True,
                                                                    norm_first=True) for _ in range(L)])
            self.nf = nn.LayerNorm(D)
            self.head = nn.Linear(D, 26)

        def tokens(self, x, keep=False):
            h = torch.cat([self.cls.expand(len(x), -1, -1), self.embed(patches(x))], 1) + self.pos
            maps = []
            for lyr in self.layers:
                if keep:
                    a = lyr.norm1(h)
                    _, w = lyr.self_attn(a, a, a, need_weights=True, average_attn_weights=False)
                    maps.append(w)
                h = lyr(h)
            return self.nf(h), maps

        def features(self, x):
            """The 25 patch tokens of the last layer: REPA's target in chapter 4."""
            return self.tokens(x)[0][:, 1:]

        def forward(self, x):
            return self.head(self.tokens(x)[0][:, 0])

    return ViT()


def cnn_net():
    import torch.nn as nn

    # 20x20 -> 10x10 -> 5x5, then global average pooling: about as many weights as the ViT (and 1.3x its arithmetic)
    return nn.Sequential(nn.Unflatten(1, (1, GL)), nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                         nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                         nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.Conv2d(128, 64, 3, padding=1), nn.ReLU(),
                         nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(64, 26))


def macs(net, x) -> int:
    """Multiply-adds of one forward pass of one picture, counted by PyTorch."""
    import torch
    from torch.utils.flop_counter import FlopCounterMode

    with FlopCounterMode(display=False) as fc, torch.no_grad():
        net(x[:1])
    return int(fc.get_total_flops() // 2)


def augment(x, g):
    import torch

    s = torch.randint(-2, 3, (2,), generator=g)  # nudge the letters about: where a stroke is now matters
    x = torch.roll(x, shifts=(int(s[0]), int(s[1])), dims=(1, 2))
    return x + 0.05 * torch.randn(x.shape, generator=g)


def train_classifier(net, X, Y, Xte, Yte, n_steps, seed, batch=64, lr=2e-3, every=None, on_check=None):
    """AdamW, one-cycle schedule, shifted and noised letters; test accuracy every ``every`` steps."""
    import torch
    import torch.nn.functional as F

    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=0.05)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=n_steps, pct_start=0.1)
    g = torch.Generator().manual_seed(seed)
    curve = []

    def test_acc():
        net.eval()
        with torch.no_grad():
            a = float((net(Xte).argmax(1) == Yte).float().mean())
        net.train()
        return a

    for st in range(n_steps + 1):
        if on_check is not None:
            on_check(st, net)
        if every and st % every == 0:
            curve.append((st, test_acc()))
        if st == n_steps:
            break
        i = torch.randint(0, len(X), (batch,), generator=g)
        loss = F.cross_entropy(net(augment(X[i], g)), Y[i])
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    net.eval()
    return curve, test_acc()


def pos_similarity(m):
    """Each patch position's learned vector against every other's (cosine, after removing the mean): (25, 25)."""
    pe = m.pos.detach()[0, 1:].numpy()
    pe = pe - pe.mean(0)
    pe = pe / np.maximum(np.linalg.norm(pe, axis=1, keepdims=True), 1e-9)
    return pe @ pe.T


def near_far(sim):
    n = int(round(np.sqrt(len(sim))))
    r, c = np.divmod(np.arange(len(sim)), n)
    dist = np.abs(r[:, None] - r[None]) + np.abs(c[:, None] - c[None])
    return float(sim[dist == 1].mean()), float(sim[dist >= 4].mean())


# ---------------------------------------------------------------------------
def compute_vit():
    import torch

    threads()
    torch.manual_seed(2020)  # Dosovitskiy et al., An Image Is Worth 16x16 Words
    imgs, labels, test, n_fonts, _ = dataset()
    X, Y = torch.tensor(imgs[~test], dtype=torch.float32), torch.tensor(labels[~test])
    Xte, Yte = torch.tensor(imgs[test], dtype=torch.float32), torch.tensor(labels[test])
    m = vit_net()
    n = steps(3000)
    checks = sorted({0, n // 60, n // 20, n // 8, n // 3, n})
    watch = np.where(test)[0][[0, 3 * 4, 3 * 8, 3 * 16, 3 * 6 + 1, 3 * 17 + 2, 3 * 22, 3 * 25 + 1]]  # A E I Q G R W Z
    replay = []

    def on_check(st, net):
        if st not in checks:
            return
        net.eval()
        with torch.no_grad():
            p = torch.softmax(net(torch.tensor(imgs[watch], dtype=torch.float32)), 1).numpy()
            acc = float((net(Xte).argmax(1) == Yte).float().mean())
        net.train()
        sim = pos_similarity(net)
        nr, fr = near_far(sim)
        replay.append(dict(step=st, acc=acc, pred=p.argmax(1).tolist(), conf=p.max(1).tolist(), sim=sim, near=nr, far=fr))
        print(f"    vit step {st}: held-out accuracy {acc:.3f}; position similarity near {nr:.2f} far {fr:.2f}", flush=True)

    curve, acc = train_classifier(m, X, Y, Xte, Yte, n, seed=0, batch=128, every=max(1, n // 30), on_check=on_check)
    torch.save(m.state_dict(), CACHE.dir / "vit.pt")
    with torch.no_grad():
        ex = np.where(test)[0][[0, 3 * 4, 3 * 8, 3 * 16]]  # A, E, I, Q from an unseen font
        _, maps = m.tokens(torch.tensor(imgs[ex], dtype=torch.float32), keep=True)
        cls_att = maps[-1].mean(1)[:, 0, 1:].reshape(-1, GL // P, GL // P).numpy()  # heads averaged
        # how far each head looks: the attention-weighted distance between patch centres, over the held-out letters
        _, maps = m.tokens(Xte, keep=True)
    rr, cc = np.divmod(np.arange(NP), GL // P)
    dpx = P * np.sqrt((rr[:, None] - rr[None]) ** 2 + (cc[:, None] - cc[None]) ** 2)  # pixels
    att_dist = []
    for w in maps:  # (B, H, 26, 26)
        a = w[:, :, 1:, 1:].numpy()
        a = a / np.maximum(a.sum(-1, keepdims=True), 1e-12)
        att_dist.append((a * dpx[None, None]).sum(-1).mean((0, 2)).tolist())  # per head
    sim = pos_similarity(m)
    nr, fr = near_far(sim)
    out = dict(acc=acc, n_test_fonts=4, n_fonts=n_fonts, n_train=int(len(X)), steps=n, D=D, H=H, L=L,
               cls_att=cls_att, ex_imgs=imgs[ex], ex_labels=labels[ex], pos_sim=sim, near=nr, far=fr,
               n_params=int(sum(p.numel() for p in m.parameters())), curve=np.array(curve), att_dist=np.array(att_dist),
               watch_imgs=imgs[watch], watch_labels=labels[watch], checks=checks,
               replay_acc=[r["acc"] for r in replay], replay_pred=np.array([r["pred"] for r in replay]),
               replay_conf=np.array([r["conf"] for r in replay]), replay_sim=np.array([r["sim"] for r in replay]),
               replay_near=[r["near"] for r in replay], replay_far=[r["far"] for r in replay])
    print(f"    accuracy on unseen fonts {acc:.1%}; attention distance by layer (px): "
          f"{[round(float(np.mean(d)), 1) for d in att_dist]}", flush=True)
    return out


def load_vit():
    """The trained vision transformer (computed first if missing), frozen."""
    import torch

    if not (CACHE.dir / "vit.pt").exists() or not CACHE.path("vit").exists():
        CACHE.save("vit", compute_vit())
    m = vit_net()
    m.load_state_dict(torch.load(CACHE.dir / "vit.pt"))
    m.eval()
    for p_ in m.parameters():
        p_.requires_grad_(False)
    return m


# ---------------------------------------------------------------------------
SIZES = (3, 7, 20)  # training fonts
SEEDS = (0, 1, 2)


def compute_vitcnn():
    """Inductive bias at equal budget: the same steps, batch, optimizer, schedule and augmentation; about as many
    weights; trained on 3, 7 or all 20 training fonts (the same random fonts for both, per seed); tested on the four
    held-out fonts."""
    import torch

    threads()
    imgs, labels, test, n_fonts, font = dataset()
    Xte, Yte = torch.tensor(imgs[test], dtype=torch.float32), torch.tensor(labels[test])
    train_fonts = np.unique(font[~test])
    n = steps(1500)
    part = CACHE.partial("vitcnn", dict(sizes=SIZES, seeds=SEEDS, steps=n, D=D, L=L))
    for seed in SEEDS:
        for k in SIZES:
            chosen = np.sort(np.random.default_rng(100 + seed).permutation(train_fonts)[:k])
            idx = np.where(np.isin(font, chosen))[0]
            X, Y = torch.tensor(imgs[idx], dtype=torch.float32), torch.tensor(labels[idx])
            for kind in ("vit", "cnn"):
                key = f"{kind}_k{k}_s{seed}"
                if key in part:
                    continue
                torch.manual_seed(1000 * seed + k)
                net = vit_net() if kind == "vit" else cnn_net()
                curve, acc = train_classifier(net, X, Y, Xte, Yte, n, seed=seed, batch=64, every=max(1, n // 15))
                part[key] = dict(acc=acc, curve=curve, params=int(sum(p.numel() for p in net.parameters())),
                                 macs=macs(net, Xte), n_train=int(len(idx)))
                print(f"    {key}: held-out accuracy {acc:.3f}", flush=True)
    out = dict(sizes=list(SIZES), seeds=list(SEEDS), steps=n, batch=64)
    for kind in ("vit", "cnn"):
        out[f"{kind}_params"] = part[f"{kind}_k20_s0"]["params"]
        out[f"{kind}_macs"] = part[f"{kind}_k20_s0"]["macs"]
        out[f"{kind}_acc"] = np.array([[part[f"{kind}_k{k}_s{s}"]["acc"] for s in SEEDS] for k in SIZES])
        out[f"{kind}_curve"] = np.array([[np.array(part[f"{kind}_k{k}_s{s}"]["curve"])[:, 1] for s in SEEDS] for k in SIZES])
    out["curve_steps"] = np.array(part["vit_k20_s0"]["curve"])[:, 0]
    out["n_train"] = [part[f"vit_k{k}_s0"]["n_train"] for k in SIZES]
    print(f"    ViT {out['vit_acc'].mean(1).round(3)}, CNN {out['cnn_acc'].mean(1).round(3)} at {SIZES} fonts", flush=True)
    return out
