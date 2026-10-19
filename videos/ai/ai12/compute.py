"""Precompute everything numerical in Part 12 of the AI series ("The Mathematics of Scale").

    python -m videos.ai.ai12.compute              # everything missing (Part 1's books: .cache/ai1)
    python -m videos.ai.ai12.compute --force grok

Results are cached in ``.cache/ai12/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

The workhorse: a character model like Part 11's (8 characters of context, 16-number vectors, two hidden layers of
width n with a residual connection), on Part 1's books, scored in bits per character on held-out text.

Items:
    lazy      how much the hidden features change in training, as the width grows, under plain gradient descent with
              the neural-tangent step sizes: the lazy, kernel-like regime of very wide networks
    mup       learning-rate sweeps at widths 32, 256 and 2,048, in the standard parametrization and in muP: the
              best learning rate drifts with width in one, and stays put in the other
    scaling   held-out loss against model size at a fixed, generous number of steps, and a power-law fit
    isoflop   Chinchilla's experiment in miniature: three compute budgets, each split between model size and training
              tokens in six ways; the best size for each budget
    grok      grokking: a network learning (a + b) mod 97 from 40% of the table: training accuracy at once, test
              accuracy thousands of steps later; with and without weight decay
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai12")
load = CACHE.load

CTX, EMB = 8, 16


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


_data = {}


def char_data():
    if not _data:
        from videos.ai.ai11.compute import char_data as cd

        _data["d"] = cd()
    return _data["d"]


def build(width, mup=False, base=64):
    """The character model at a given width; with mup, the output is scaled by base/width and starts at zero."""
    import torch

    tr, va, K = char_data()
    emb = torch.nn.Embedding(K, EMB)
    h1 = torch.nn.Linear(CTX * EMB, width)
    h2 = torch.nn.Linear(width, width)
    out = torch.nn.Linear(width, K)
    mult = base / width if mup else 1.0
    if mup:
        torch.nn.init.zeros_(out.weight)
    mods = dict(emb=emb, h1=h1, h2=h2, out=out)

    def logits(ctx):
        h = torch.tanh(h1(emb(ctx).reshape(len(ctx), -1)))
        h = torch.tanh(h2(h)) + h
        return out(h) * mult

    return mods, logits


def train(width, lr, steps, mup=False, base=64, batch=256, seed=0, log_every=None, record_init=False):
    import torch

    torch.set_num_threads(1)
    torch.manual_seed(seed)
    tr, va, K = char_data()
    tr_t, va_t = torch.tensor(tr), torch.tensor(va)
    mods, logits = build(width, mup, base)
    if mup:  # Adam in muP: the hidden matrix's learning rate scales like base / width; the output is already scaled
        groups = [dict(params=[mods["emb"].weight, mods["h1"].weight, mods["h1"].bias, mods["h2"].bias, mods["out"].weight,
                               mods["out"].bias], lr=lr),
                  dict(params=[mods["h2"].weight], lr=lr * base / width)]
    else:
        groups = [dict(params=[p for m in mods.values() for p in m.parameters()], lr=lr)]
    opt = torch.optim.Adam(groups)
    init = {k: m.weight.detach().clone() for k, m in mods.items()} if record_init else None

    def windows(seq, pos):
        return torch.stack([seq[pos - CTX + j] for j in range(CTX)], 1)

    def bits(seq, n=60_000):
        with torch.no_grad():
            pos = torch.arange(CTX, min(len(seq), n))
            return float(torch.nn.functional.cross_entropy(logits(windows(seq, pos)), seq[pos])) / math.log(2)

    g = rng(seed + 7)
    curve = []
    for k in range(1, steps + 1):
        pos = torch.tensor(g.integers(CTX, len(tr), batch))
        loss = torch.nn.functional.cross_entropy(logits(windows(tr_t, pos)), tr_t[pos])
        if not torch.isfinite(loss):
            return dict(final=float("nan"), curve=np.array(curve), moved=None)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if log_every and k % log_every == 0:
            curve.append((k, bits(va_t)))
    final = bits(va_t)
    moved = None
    if record_init:
        moved = {k: float((m.weight.detach() - init[k]).norm() / init[k].norm()) for k, m in mods.items() if k != "emb"}
    n_params = sum(p.numel() for m in mods.values() for p in m.parameters())
    return dict(final=final, curve=np.array(curve), moved=moved, n_params=n_params)


# ---------------------------------------------------------------------------
def compute_lazy():
    """Plain gradient descent, with step sizes that keep a wide network stable (the neural-tangent scaling: the
    hidden and output matrices' rates shrink like 1/width): how much the hidden features change in training."""
    import torch

    torch.set_num_threads(1)
    tr, va, K = char_data()
    tr_t, va_t = torch.tensor(tr), torch.tensor(va)

    def windows(seq, pos):
        return torch.stack([seq[pos - CTX + j] for j in range(CTX)], 1)

    probe = windows(va_t, torch.arange(CTX, CTX + 2000))
    widths = [32, 64, 128, 256, 512, 1024, 2048]
    moved, feat, finals = [], [], []
    for w in widths:
        torch.manual_seed(0)
        mods, logits = build(w)
        emb, h1, h2 = mods["emb"], mods["h1"], mods["h2"]

        def features():
            with torch.no_grad():
                h = torch.tanh(h1(emb(probe).reshape(len(probe), -1)))
                return torch.tanh(h2(h)) + h

        f0, w0 = features(), h2.weight.detach().clone()
        eta = 0.5
        opt = torch.optim.SGD([dict(params=[*emb.parameters(), *h1.parameters()], lr=0.004),
                               dict(params=[*h2.parameters(), *mods["out"].parameters()], lr=eta * 64 / w)])
        g = rng(7)
        for k in range(800):
            pos = torch.tensor(g.integers(CTX, len(tr), 256))
            loss = torch.nn.functional.cross_entropy(logits(windows(tr_t, pos)), tr_t[pos])
            opt.zero_grad()
            loss.backward()
            opt.step()
        with torch.no_grad():
            pos = torch.arange(CTX, 60_000)
            finals.append(float(torch.nn.functional.cross_entropy(logits(windows(va_t, pos)), va_t[pos])) / math.log(2))
        feat.append(float((features() - f0).norm() / f0.norm()))
        moved.append(float((h2.weight.detach() - w0).norm() / w0.norm()))
        print(f"    width {w}: features changed {feat[-1]:.4f}, hidden matrix moved {moved[-1]:.5f}, "
              f"held-out {finals[-1]:.3f} bits", flush=True)
    feat, moved = np.array(feat), np.array(moved)
    slope = float(np.polyfit(np.log(widths), np.log(feat), 1)[0])
    slope_w = float(np.polyfit(np.log(widths), np.log(moved), 1)[0])
    assert -0.7 < slope < -0.25 and feat[-1] < feat[0] / 2.5, (slope, feat)
    assert max(finals) < 4.0  # still learning (from 6.4 bits at the start), while its features move less and less
    return dict(widths=widths, moved=feat, slope=slope, weights_moved=moved, slope_weights=slope_w, finals=finals, eta=eta)


# ---------------------------------------------------------------------------
LRS = [10 ** x for x in np.linspace(-3.5, -0.5, 13)]


def compute_mup():
    out = {}
    widths = [32, 256, 2048]
    for mode in ("sp", "mup"):
        for w in widths:
            finals = []
            for lr in LRS:
                r = train(w, lr, steps=800, mup=(mode == "mup"))
                finals.append(r["final"])
            out[f"{mode}{w}"] = np.array(finals)
            best = LRS[int(np.nanargmin(finals))]
            print(f"    {mode} width {w}: best lr {best:.2e}, loss {np.nanmin(finals):.3f}", flush=True)
    bests = {m: [math.log10(LRS[int(np.nanargmin(out[f'{m}{w}']))]) for w in widths] for m in ("sp", "mup")}
    drift = {m: max(v) - min(v) for m, v in bests.items()}
    best_loss = {m: [float(np.nanmin(out[f"{m}{w}"])) for w in widths] for m in ("sp", "mup")}
    for m in ("sp", "mup"):
        for w in widths:
            print(f"    {m} {w}: " + " ".join(f"{v:.3f}" for v in out[f"{m}{w}"]), flush=True)
    assert drift["mup"] <= drift["sp"], drift
    assert best_loss["mup"][-1] < best_loss["sp"][-1]  # in muP the widest model learns the most
    return dict(widths=widths, lrs=np.array(LRS), bests=bests, drift=drift, best_loss=best_loss, **out)


# ---------------------------------------------------------------------------
def compute_scaling():
    widths = [8, 16, 32, 64, 128, 256, 512]
    finals, params = [], []
    for w in widths:
        r = train(w, lr=3e-3 * math.sqrt(64 / max(w, 64)), steps=3000)
        finals.append(r["final"])
        params.append(r["n_params"])
        print(f"    width {w}: {r['n_params']} params, {r['final']:.3f} bits", flush=True)
    finals, params = np.array(finals), np.array(params)
    # L(N) = E + A N^-alpha: for each alpha on a grid, E and A by least squares (the model is linear in them)
    best = None
    for alpha in np.linspace(0.05, 2.0, 400):
        M = np.stack([np.ones_like(params, dtype=float), params ** -alpha], 1)
        (E, A), *_ = np.linalg.lstsq(M, finals, rcond=None)
        if A <= 0 or E <= 0:
            continue
        res = float(np.sum((M @ np.array([E, A]) - finals) ** 2))
        if best is None or res < best[0]:
            best = (res, float(E), float(alpha), float(A))
    res, E, alpha, A = best
    assert res / np.sum((finals - finals.mean()) ** 2) < 0.02  # the curve explains the points
    return dict(widths=widths, params=params, finals=finals, E=float(E), alpha=float(alpha), A=float(A))


# ---------------------------------------------------------------------------
def compute_isoflop():
    budgets = [3e11, 1e12, 3e12]  # training FLOPs, about 6 x parameters x tokens
    widths = [16, 32, 64, 128, 256, 512]
    batch = 256
    out = dict(budgets=budgets, widths=widths)
    best_n = []
    for C in budgets:
        finals, ns, toks = [], [], []
        for w in widths:
            mods_params = train(w, 1e-3, steps=1)["n_params"]
            steps = int(C / (6 * mods_params * batch))
            if steps < 50:
                finals.append(float("nan"))
                ns.append(mods_params)
                toks.append(steps * batch)
                continue
            r = train(w, lr=3e-3 * math.sqrt(64 / max(w, 64)), steps=steps)
            finals.append(r["final"])
            ns.append(mods_params)
            toks.append(steps * batch)
            print(f"    C={C:.0e} width {w}: {steps} steps, {r['final']:.3f}", flush=True)
        out[f"finals{C:.0e}"] = np.array(finals)
        out[f"params{C:.0e}"] = np.array(ns)
        out[f"tokens{C:.0e}"] = np.array(toks)
        best_n.append(ns[int(np.nanargmin(finals))])
    out["best_n"] = best_n
    assert best_n[-1] >= best_n[0]  # bigger budgets want bigger models
    return out


# ---------------------------------------------------------------------------
P = 97


def compute_grok():
    import torch

    torch.set_num_threads(2)
    g = rng(2022)  # Power et al., 2022
    pairs = np.array([(a, b) for a in range(P) for b in range(P)])
    labels = (pairs[:, 0] + pairs[:, 1]) % P
    idx = g.permutation(len(pairs))
    n_tr = int(0.4 * len(pairs))
    tr, te = idx[:n_tr], idx[n_tr:]
    X = torch.tensor(pairs)
    Y = torch.tensor(labels)
    out = {}
    for name, wd in (("wd", 1.0), ("nowd", 0.0)):
        torch.manual_seed(0)
        emb = torch.nn.Embedding(P, 128)
        net = torch.nn.Sequential(torch.nn.Linear(256, 512), torch.nn.ReLU(), torch.nn.Linear(512, P))
        params = [*emb.parameters(), *net.parameters()]
        opt = torch.optim.AdamW(params, lr=1e-3, weight_decay=wd, betas=(0.9, 0.98))

        def f(i):
            return net(emb(X[i]).reshape(len(i), -1))

        curve, snaps = [], {}
        snap_steps = (1, 100, 300, 1000, 2000, 3000, 3500, 4000, 5000, 8000, 12000)
        for step in range(1, 12001):
            if name == "wd" and step in snap_steps:
                snaps[step] = emb.weight.detach().numpy().copy()
            loss = torch.nn.functional.cross_entropy(f(torch.tensor(tr)), Y[tr])
            opt.zero_grad()
            loss.backward()
            opt.step()
            if step % 50 == 0 or step < 50:
                with torch.no_grad():
                    a_tr = float((f(torch.tensor(tr)).argmax(1) == Y[tr]).float().mean())
                    a_te = float((f(torch.tensor(te)).argmax(1) == Y[te]).float().mean())
                    wn = float(sum((p ** 2).sum() for p in params).sqrt())
                curve.append((step, a_tr, a_te, wn))
        out[name] = np.array(curve)
        c = out[name]
        t_tr = int(c[np.argmax(c[:, 1] > 0.99), 0]) if (c[:, 1] > 0.99).any() else None
        t_te = int(c[np.argmax(c[:, 2] > 0.95), 0]) if (c[:, 2] > 0.95).any() else None
        out[f"t_train_{name}"], out[f"t_test_{name}"] = t_tr, t_te
        print(f"    {name}: train 99% at {t_tr}, test 95% at {t_te}", flush=True)
        if name == "wd":
            E = emb.weight.detach().numpy()
            # the learned embedding: its main Fourier frequencies (the network does arithmetic on a circle)
            F = np.abs(np.fft.rfft(E - E.mean(0), axis=0)).sum(1)
            out["fourier"] = F
            u, s, vt = np.linalg.svd(E - E.mean(0), full_matrices=False)
            out["emb_xy"] = (E - E.mean(0)) @ vt[:2].T
            # the same two directions, applied to the vectors as they were during training: watch the circles form
            out["snap_steps"] = list(snap_steps)
            out["snap_xy"] = np.stack([(snaps[k] - snaps[k].mean(0)) @ vt[:2].T for k in snap_steps])
    assert out["t_test_wd"] is not None and out["t_test_wd"] > 3 * out["t_train_wd"]
    return dict(**out, n_train=n_tr, n_test=len(te), P=P)


ITEMS = {
    "lazy": compute_lazy,
    "mup": compute_mup,
    "scaling": compute_scaling,
    "isoflop": compute_isoflop,
    "grok": compute_grok,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
