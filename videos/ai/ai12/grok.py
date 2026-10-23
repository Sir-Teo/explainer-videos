"""Grokking on (a + b) mod 97 (Power et al. 2022), measured: the replayed run, weight decay swept, and the Fourier
circuit in the learned number vectors (Nanda et al. 2023).

The network: each number a learned vector of 64; the two vectors side by side into 256 ReLU units, then a score for
each of the 97 answers. Full-batch AdamW (learning rate 0.003, betas 0.9 and 0.98) on 40% of the 97 x 97 table.
"""

from __future__ import annotations

import math

import numpy as np

P, FRAC, DIM, HID, LR = 97, 0.4, 64, 256, 3e-3
WDS = [0.0, 0.1, 0.3, 1.0, 3.0]
SEEDS = (0, 1, 2)
MAX_STEPS = 6000


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def split():
    g = rng(2022)  # Power et al., 2022
    pairs = np.array([(a, b) for a in range(P) for b in range(P)])
    labels = (pairs[:, 0] + pairs[:, 1]) % P
    idx = g.permutation(len(pairs))
    n_tr = int(FRAC * len(pairs))
    return pairs, labels, idx[:n_tr], idx[n_tr:]


def build(seed):
    import torch

    torch.manual_seed(seed)
    emb = torch.nn.Embedding(P, DIM)
    net = torch.nn.Sequential(torch.nn.Linear(2 * DIM, HID), torch.nn.ReLU(), torch.nn.Linear(HID, P))
    return emb, net


def fourier_share(E: np.ndarray, top: int = 5) -> tuple[np.ndarray, float]:
    """The number vectors' energy by frequency (the discrete Fourier transform along the 97 numbers, summed over the
    64 coordinates), and the share of it in the ``top`` strongest frequencies."""
    F = (np.abs(np.fft.rfft(E - E.mean(0), axis=0)) ** 2).sum(1)[1:]  # frequencies 1 ... 48
    return F, float(np.sort(F)[::-1][:top].sum() / F.sum())


def run(wd: float, seed: int, steps: int = MAX_STEPS, replay: bool = False, stop_after: int | None = 300):
    """One run. ``replay``: also keep the number vectors at many moments, and the tangent kernel's distance from its
    starting value (Fort et al. 2020's kernel distance, on 128 fixed examples)."""
    import torch

    from . import charlm

    charlm.threads()
    pairs, labels, tr, te = split()
    X, Y = torch.tensor(pairs), torch.tensor(labels)
    trt, tet = torch.tensor(tr), torch.tensor(te)
    emb, net = build(seed)
    params = [*emb.parameters(), *net.parameters()]
    opt = torch.optim.AdamW(params, lr=LR, weight_decay=wd, betas=(0.9, 0.98))

    def f(i):
        return net(emb(X[i]).reshape(len(i), -1))

    probe = torch.tensor(np.concatenate([tr[:64], te[:64]]))

    def kernel():
        rows = []
        for i in probe:
            out = f(i[None])[0, Y[i]]
            g = torch.autograd.grad(out, params)
            rows.append(torch.cat([x.reshape(-1) for x in g]))
        J = torch.stack(rows)
        return (J @ J.T).detach().numpy()

    K0 = kernel() if replay else None
    curve, snaps, snap_steps, kd, kd_steps = [], [], [], [], []
    snap_at = set(range(0, 1001, 25)) | set(range(1000, steps + 1, 100))
    kd_at = set(np.unique(np.round(np.geomspace(1, steps, 40)).astype(int)).tolist())
    t_train = t_test = None
    for step in range(steps + 1):
        if replay and step in snap_at:
            snaps.append(emb.weight.detach().numpy().copy())
            snap_steps.append(step)
        if replay and step in kd_at:
            K = kernel()
            kd.append(1 - float((K * K0).sum() / (np.linalg.norm(K) * np.linalg.norm(K0))))
            kd_steps.append(step)
        if step % 25 == 0 or step < 25:
            with torch.no_grad():
                ltr = f(trt)
                lte = f(tet)
                a_tr = float((ltr.argmax(1) == Y[trt]).float().mean())
                a_te = float((lte.argmax(1) == Y[tet]).float().mean())
                l_tr = float(torch.nn.functional.cross_entropy(ltr, Y[trt]))
                l_te = float(torch.nn.functional.cross_entropy(lte, Y[tet]))
                wn = float(sum((p ** 2).sum() for p in params).sqrt())
            curve.append((max(step, 1), a_tr, a_te, wn, l_tr, l_te))
            if t_train is None and a_tr > 0.99:
                t_train = step
            if t_test is None and a_te > 0.95:
                t_test = step
            if stop_after is not None and t_test is not None and step >= t_test + stop_after and not replay:
                break
        if step == steps:
            break
        loss = torch.nn.functional.cross_entropy(f(trt), Y[trt])
        opt.zero_grad()
        loss.backward()
        opt.step()
    out = dict(curve=np.array(curve), t_train=t_train, t_test=t_test, steps=step)
    if replay:
        out.update(snaps=np.array(snaps), snap_steps=np.array(snap_steps), kd=np.array(kd), kd_steps=np.array(kd_steps))
        with torch.no_grad():  # the whole table's scores at the end, for the circuit check
            allp = torch.arange(P * P)
            out["logits"] = f(allp).numpy().reshape(P, P, P)
    return out


def compute(cache):
    part = cache.partial("grok", dict(P=P, frac=FRAC, dim=DIM, hid=HID, lr=LR, wds=WDS, seeds=SEEDS, max=MAX_STEPS, v=1))
    for wd in WDS:
        for s in SEEDS:
            key = f"{wd}_{s}"
            if key not in part:
                r = run(wd, s)
                part[key] = dict(curve=r["curve"].tolist(), t_train=r["t_train"], t_test=r["t_test"], steps=r["steps"])
                print(f"    weight decay {wd}, seed {s}: memorized at {r['t_train']}, generalized at {r['t_test']}",
                      flush=True)
    pairs, labels, tr, te = split()
    main = run(1.0, 0, replay=True)
    nowd = run(0.0, 0, replay=True)
    out = dict(P=P, n_train=len(tr), n_test=len(te), dim=DIM, hid=HID, lr=LR, wds=WDS, seeds=list(SEEDS),
               max_steps=MAX_STEPS)
    out["wd"], out["nowd"] = main["curve"], nowd["curve"]
    out["t_train_wd"], out["t_test_wd"] = main["t_train"], main["t_test"]
    out["t_train_nowd"], out["t_test_nowd"] = nowd["t_train"], nowd["t_test"]
    out["sweep_train"] = np.array([[part[f"{wd}_{s}"]["t_train"] or np.nan for s in SEEDS] for wd in WDS], float)
    out["sweep_test"] = np.array([[part[f"{wd}_{s}"]["t_test"] or np.nan for s in SEEDS] for wd in WDS], float)
    for wd in WDS:
        out[f"sweep_curve{wd}"] = np.array(part[f"{wd}_0"]["curve"])
    # the number vectors, through training: spectrum by frequency, and the share in the five strongest
    snaps = main["snaps"]
    spec = np.array([fourier_share(E)[0] for E in snaps])
    out["snap_steps"], out["spectrum"] = main["snap_steps"], spec
    out["share5"] = np.array([fourier_share(E)[1] for E in snaps])
    out["share5_nowd"] = np.array([fourier_share(E)[1] for E in nowd["snaps"]])
    out["spectrum_nowd_end"] = fourier_share(nowd["snaps"][-1])[0]
    F = spec[-1]
    key = np.argsort(F)[::-1][:5] + 1
    out["key_freqs"] = np.sort(key)
    E = snaps[-1]
    _, _, vt = np.linalg.svd(E - E.mean(0), full_matrices=False)
    out["emb_xy"] = (E - E.mean(0)) @ vt[:2].T
    out["snap_xy"] = np.stack([(S - S.mean(0)) @ vt[:2].T for S in snaps])
    # each key frequency's own circle: the projection of the number vectors on the cos and sin of k a
    a = np.arange(P)
    circles = []
    for k in out["key_freqs"]:
        c, s_ = np.cos(2 * math.pi * k * a / P), np.sin(2 * math.pi * k * a / P)
        Ec = E - E.mean(0)
        u, v = c @ Ec, s_ @ Ec  # the directions in the 64 dimensions that carry cos and sin of frequency k
        circles.append(np.stack([Ec @ u / np.linalg.norm(u), Ec @ v / np.linalg.norm(v)], 1))
    out["circles"] = np.array(circles)
    # the circuit check: how much of the final scores is the key frequencies' cos(w (a + b - c))
    Lg = main["logits"]
    A_, B_, C_ = np.meshgrid(a, a, a, indexing="ij")
    Lc = Lg - Lg.mean(2, keepdims=True)
    basis = [np.cos(2 * math.pi * k * (A_ + B_ - C_) / P) for k in out["key_freqs"]]
    M = np.stack([b.reshape(-1) for b in basis], 1)
    coef, *_ = np.linalg.lstsq(M, Lc.reshape(-1), rcond=None)
    out["circuit_r2"] = float(1 - ((Lc.reshape(-1) - M @ coef) ** 2).sum() / (Lc ** 2).sum())
    out["kd"], out["kd_steps"] = main["kd"], main["kd_steps"]
    out["kd_nowd"] = nowd["kd"]
    return out
