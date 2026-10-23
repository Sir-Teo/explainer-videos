"""Precompute everything numerical in Part 24 of the AI series ("Learning Without Labels").

    python -m videos.ai.ai24.compute                 # everything missing (MNIST through Part 10's checked download)
    python -m videos.ai.ai24.compute --force dino
    AI24_SCALE=0.02 python -m videos.ai.ai24.compute # a smoke test of every code path (into .cache/ai24_quick/)

Results are cached in ``.cache/ai24/<name>.json`` (+ ``.npz``); each training run's larger arrays (its test features,
its replay snapshots) in ``.cache/ai24/runs/``; a few trained encoders in ``.cache/ai24/models/``. Every model is
trained here, on the CPU, on one torch thread (``AI24_THREADS``), seeded. Every item made of several runs saves each
run as it finishes (``CACHE.partial``), so a killed computation resumes where it stopped. About two and a half hours
on a busy 4-core machine, all told; each run takes two to five minutes.

The budget (ssl.py): every method trains the same encoder for ``STEPS`` updates of 256 encoder passes (128 digits in
two views, or 256 in one), with the same optimizer, schedule and views; the same seed gives every method the same
starting encoder. Every method, the masked ones included, trains the same three-layer convolutional network.

    views       augmented views of ten test digits (the full recipe and the crop alone)
    baselines   raw pixels, and untrained encoders (three seeds): what a representation has to beat
    infonce     the InfoNCE bound on correlated Gaussians whose mutual information is known: the estimate against
                the batch size N, never above log N
    pretext     rotation prediction (Gidaris et al. 2018), three seeds; its replay; rotation accuracy by digit
    supervised  the same encoder trained with the labels, three seeds
    simclr      SimCLR at five temperatures (0.2: three seeds; 0.05, 0.1, 0.5, 1: two each), and with crops only;
                the main run's nearest neighbours replayed; truncated embeddings; how the softmax weighs negatives
    moco        MoCo (a queue of 4,096 keys, a momentum encoder), three seeds
    sphere      three encoders whose embedding has three numbers (SimCLR, the naive siamese net, SimSiam): 600 test
                digits on the sphere, replayed through training
    collapse    the naive siamese net, SimSiam with and without the stop-gradient, BYOL: collapse measured
    redundancy  Barlow Twins (the cross-correlation matrix replayed), VICReg, VICReg without its variance term
    dino        DINO, and DINO without centering or without sharpening: the teacher's entropy and the KL to the student
    mae         a masked autoencoder on the same network (75% of 49 patches hidden, three seeds; 50% and 90%, one
                each); reconstructions replayed
    beit        a BEiT-style model predicting the k-means codes of hidden patches, three seeds
    jepa        I-JEPA (predict the target encoder's map of hidden blocks), three seeds
    matryoshka  SimCLR with the Matryoshka loss on nested prefixes, three seeds: accuracy of truncated embeddings
    curation    an unbalanced unlabelled pool against one curated by retrieval (DINOv2's recipe), two seeds each
    halves      two encoders that each see only half of every digit, trained apart: does what they learn align?
    finetune    every method's network fine-tuned whole from 100 labels, against training from scratch
    compare     every method side by side: linear probe, k-NN, ten labels per class, effective rank; CKA and mutual
                nearest neighbours between the representations
"""

from __future__ import annotations

import math
import os
import time

import numpy as np
import torch
import torch.nn.functional as F

from explainer.ai.cache import Cache
from videos.ai.ai24 import ssl as S

CACHE = Cache("ai24")
if S.SCALE != 1.0:  # a quick smoke test of every code path: its own cache, never the real one
    CACHE.dir = CACHE.dir.parent / "ai24_quick"
load = CACHE.load
RUNS = CACHE.dir / "runs"
MODELS = CACHE.dir / "models"
SEEDS = (0, 1, 2)
TAUS = (0.05, 0.1, 0.2, 0.5, 1.0)
MAIN_TAU = 0.2
NESTED = (2, 4, 8, 16, 32, 64, 128)
log = S.log


def threads():
    torch.set_num_threads(int(os.environ.get("AI24_THREADS", "1")))


def tolist(x):
    if isinstance(x, dict):
        return {k: tolist(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [tolist(v) for v in x]
    if isinstance(x, torch.Tensor):
        x = x.detach().numpy()
    if isinstance(x, np.ndarray):
        return x.tolist() if x.dtype.kind in "iub" else np.round(x.astype(np.float64), 5).tolist()
    if isinstance(x, np.floating):
        return float(x)
    if isinstance(x, np.integer):
        return int(x)
    return x


def replay_steps(steps: int, n: int = 12) -> list[int]:
    """Snapshot steps for a replay: dense early, where most of the change happens."""
    return sorted(set([0] + [int(round(v)) for v in np.geomspace(max(4, steps / 200), steps, n - 1)]))


def save_model(m, key: str) -> None:
    MODELS.mkdir(parents=True, exist_ok=True)
    tmp = MODELS / f"{key}.tmp.pt"
    torch.save(m.state_dict(), tmp)
    tmp.replace(MODELS / f"{key}.pt")


# ---------------------------------------------------------------------------
# One training run, kept as a piece of its item
# ---------------------------------------------------------------------------
def run(part, key: str, name: str, seed: int, kw: dict | None = None, extra=None, record=None, record_at=None,
        pool=None, half=None, few=True, keep_model=False):
    """Train method ``name`` (``kw`` its options) from seed ``seed`` and measure it; the numbers become piece ``key``
    of the partial item ``part``, its arrays (test features, snapshots) go to runs/<key>.npz. ``extra(m)`` -> (dict
    of numbers, dict of arrays) adds item-specific measurements of the trained model."""
    npz = RUNS / f"{key}.npz"
    if key in part and npz.exists() and (not keep_model or (MODELS / f"{key}.pt").exists()):
        with np.load(npz) as z:
            return part[key], {k: z[k] for k in z.files}
    t0 = time.time()
    torch.manual_seed(seed)
    m = S.make(name, **(kw or {}))
    tr = S.train(m, seed, pool=pool, record=record, record_at=record_at, half=half)
    res, feat = S.evaluate(m, few=few, half=half)
    arrays = {"feat": feat.numpy().astype(np.float16)}
    for i, r in enumerate(tr.pop("rec")):
        for k, v in r.items():
            arrays.setdefault(f"rec_{k}", []).append(np.asarray(v))
    arrays = {k: (np.stack(v) if isinstance(v, list) else v) for k, v in arrays.items()}
    piece = {"name": name, "seed": seed, "kw": {k: v for k, v in (kw or {}).items() if k != "codebook"},
             "params": S.n_params(m), "final": res, **tr}
    if extra is not None:
        nums, arrs = extra(m)
        piece["extra"] = nums
        arrays.update({f"x_{k}": np.asarray(v) for k, v in arrs.items()})
    if keep_model:
        save_model(m, key)
    RUNS.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(RUNS / f"{key}.tmp.npz", **arrays)
    (RUNS / f"{key}.tmp.npz").replace(npz)
    part[key] = tolist(piece)
    log(f"{key}: linear {res['linear']:.4f}  k-NN {res['knn']:.4f}  rank {res['rank']:.1f}  "
        f"({tr['secs']:.0f}s train, {time.time() - t0:.0f}s all)")
    return part[key], arrays


def finals(pieces: dict, keys) -> dict:
    """Mean, min and max over runs of each final number."""
    out = {}
    for f in ("linear", "knn", "rank", "spread", "align_h", "unif_h", "align_z", "unif_z", "rank_z"):
        v = [pieces[k]["final"][f] for k in keys if f in pieces[k]["final"]]
        if v:
            out[f] = [float(np.mean(v)), float(np.min(v)), float(np.max(v))]
    fw = [np.mean(pieces[k]["final"]["few"]) for k in keys if "few" in pieces[k]["final"]]
    if fw:
        out["few"] = [float(np.mean(fw)), float(np.min(fw)), float(np.max(fw))]
    return out


def z_extras(m, nested=None):
    """Numbers every run with an embedding gets: the singular values of its unit vectors on the 2,000 test digits
    (the collapse spectrum), and the k-NN accuracy of each prefix of the embedding (for Matryoshka)."""
    D = S.data()
    z = S.features(m.embed, D["xte"][:2000], module=m)
    sv = torch.linalg.svdvals(F.normalize(z, dim=1).double())
    nums, arrs = {}, {"spectrum": sv.numpy()}
    if nested:
        ztr = S.features(m.embed, D["xtr"], module=m)
        zte = S.features(m.embed, D["xte"], module=m)
        acc = []
        for k in nested:
            if k <= z.shape[1]:
                acc.append(S.knn(ztr[:, :k], D["ytr"], zte[:, :k], D["yte"]))
        nums["prefix_dims"] = [k for k in nested if k <= z.shape[1]]
        nums["prefix_knn"] = acc
    return nums, arrs


# ---------------------------------------------------------------------------
# Views and baselines
# ---------------------------------------------------------------------------
def first_of_each(y: torch.Tensor) -> list[int]:
    return [int(torch.nonzero(y == c)[0]) for c in range(10)]


def u8(x) -> np.ndarray:
    return (np.clip(np.asarray(x, np.float32), 0, 1) * 255).round().astype(np.uint8)


def compute_views():
    threads()
    D = S.data()
    ids = first_of_each(D["yte"])
    x = S.fl(D["xte"][ids])
    g = torch.Generator().manual_seed(3)
    full = torch.stack([S.augment(x, g) for _ in range(8)]).squeeze(2)
    light = torch.stack([S.augment(x, g, light=True) for _ in range(8)]).squeeze(2)
    return {"ids": ids, "full": u8(full.numpy()), "light": u8(light.numpy()), "orig": D["xte"][ids].numpy(),
            "grid": D["xte"][:64].numpy(), "grid_y": D["yte"][:64].numpy(), "n_train": len(D["xtr"]), "n_test": len(D["xte"]),
            "steps": S.STEPS, "batch": S.B}


def compute_baselines():
    """Raw pixels, and the encoders before any training: linear probe, k-NN, ten labels per class."""
    threads()
    D = S.data()
    ftr, fte = D["xtr"].reshape(len(D["xtr"]), -1).float() / 255, D["xte"].reshape(len(D["xte"]), -1).float() / 255
    out = {"pixels": {"linear": S.linear_probe(ftr, D["ytr"], fte, D["yte"]), "knn": S.knn(ftr, D["ytr"], fte, D["yte"]),
                      "few": S.few_label(ftr, D["ytr"], fte, D["yte"]), "rank": S.eff_rank(fte[:2000]), "dim": 784}}
    log(f"pixels: {out['pixels']}")
    RUNS.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(RUNS / "pixels.npz", feat=fte[:2000].numpy().astype(np.float16))
    rows = []
    for s in SEEDS:
        torch.manual_seed(s)
        m = S.make("supervised")  # an untrained encoder (its head is never used)
        res, feat = S.evaluate(m, extra_embed=False)
        rows.append(res)
        np.savez_compressed(RUNS / f"random_cnn_s{s}.npz", feat=feat.numpy().astype(np.float16))
        log(f"untrained, seed {s}: linear {res['linear']:.4f} k-NN {res['knn']:.4f}")
    out["random_cnn"] = rows
    return out


# ---------------------------------------------------------------------------
# InfoNCE on Gaussians with known mutual information
# ---------------------------------------------------------------------------
def gaussian_pairs(n, d, rho, g):
    x = torch.randn(n, d, generator=g)
    y = rho * x + math.sqrt(1 - rho ** 2) * torch.randn(n, d, generator=g)
    return x, y


def compute_infonce():
    """X, Y in R^20, each coordinate pair correlated (rho), so I(X; Y) = -10 log(1 - rho^2) nats exactly. A separable
    critic f(x, y) = g(x).h(y) is trained with InfoNCE at batch size N; the estimate log N - L_N is measured on 40
    held-out batches. Two seeds."""
    threads()
    d = 20
    Ns = [2, 4, 8, 16, 32, 64, 128, 256, 512]
    mis = [2.0, 5.0, 10.0]
    steps = max(30, int(round(1500 * S.SCALE)))
    out = {"Ns": Ns, "mis": mis, "d": d, "steps": steps, "est": {}, "curve": {}}
    part = CACHE.partial("infonce", {"Ns": Ns, "mis": mis, "steps": steps})

    def critic():
        def net():
            return torch.nn.Sequential(torch.nn.Linear(d, 128), torch.nn.ReLU(), torch.nn.Linear(128, 128),
                                       torch.nn.ReLU(), torch.nn.Linear(128, 32))
        return net(), net()

    for I in mis:
        rho = math.sqrt(1 - math.exp(-2 * I / d))
        for N in Ns:
            for s in (0, 1):
                key = f"I{I:g}_N{N}_s{s}"
                if key not in part:
                    torch.manual_seed(100 + s)
                    gx, hy = critic()
                    opt = torch.optim.Adam(list(gx.parameters()) + list(hy.parameters()), 1e-3)
                    g = torch.Generator().manual_seed(1000 * s + N)
                    curve = []
                    for t in range(steps):
                        x, y = gaussian_pairs(N, d, rho, g)
                        sc = gx(x) @ hy(y).t()
                        L = F.cross_entropy(sc, torch.arange(N))
                        opt.zero_grad()
                        L.backward()
                        opt.step()
                        if t % max(1, steps // 30) == 0:
                            curve.append([t, math.log(N) - float(L)])
                    ge = torch.Generator().manual_seed(77)
                    with torch.no_grad():
                        Ls = []
                        for _ in range(40):
                            x, y = gaussian_pairs(N, d, rho, ge)
                            Ls.append(float(F.cross_entropy(gx(x) @ hy(y).t(), torch.arange(N))))
                    est = math.log(N) - float(np.mean(Ls))
                    assert est <= math.log(N) + 1e-9  # a cross-entropy is never negative
                    part[key] = {"est": est, "curve": curve}
                    log(f"infonce I={I} N={N} seed {s}: estimate {est:.3f} (log N = {math.log(N):.3f})")
                out["est"][key] = part[key]["est"]
                out["curve"][key] = part[key]["curve"]
    return out


# ---------------------------------------------------------------------------
# Pretext: rotation prediction
# ---------------------------------------------------------------------------
def compute_pretext():
    threads()
    D = S.data()
    ids = first_of_each(D["yte"])[:4]
    xs = S.fl(D["xte"][ids])
    rots = torch.cat([torch.rot90(xs, k, (2, 3)) for k in range(4)])  # 4 rotations x 4 digits

    def record(m, step):
        m.eval()
        with torch.no_grad():
            p = F.softmax(m.head(m.enc(rots)), 1)
        m.train()
        return {"p": p.numpy()}

    def extra(m):
        Xte, Yte = D["xte"], D["yte"]
        x = S.fl(Xte)
        m.eval()
        right = torch.zeros(10)
        with torch.no_grad():
            for k in range(4):
                for i in range(0, len(Xte), 1000):
                    pr = m.head(m.enc(torch.rot90(x[i:i + 1000], k, (2, 3)))).argmax(1)
                    right.index_add_(0, Yte[i:i + 1000], (pr == k).float())
        m.train()
        per = right / (4 * torch.bincount(Yte, minlength=10).float())
        return {"rot_acc_by_digit": per.tolist(), "rot_acc": float(right.sum() / (4 * len(Yte)))}, {}

    part = CACHE.partial("pretext", {"steps": S.STEPS})
    keys = []
    for s in SEEDS:
        k = f"rotation_s{s}"
        run(part, k, "rotation", s, extra=extra, record=record if s == 0 else None, keep_model=s == 0,
            record_at=replay_steps(S.STEPS) if s == 0 else None)
        keys.append(k)
    out = {"runs": {k: part[k] for k in keys}, "summary": finals(part.done, keys), "ids": ids,
           "rec_steps": part[keys[0]]["rec_steps"]}
    with np.load(RUNS / f"{keys[0]}.npz") as z:
        out["rec_p"] = z["rec_p"]
    out["digits"] = D["xte"][ids].numpy()
    return out


def compute_supervised():
    threads()
    part = CACHE.partial("supervised", {"steps": S.STEPS})
    keys = {"cnn": []}
    for s in SEEDS:
        k = f"supervised_s{s}"
        run(part, k, "supervised", s, extra=z_extras, keep_model=s == 0)
        keys["cnn"].append(k)
    return {"runs": dict(part.done), "summary": {a: finals(part.done, ks) for a, ks in keys.items()}, "keys": keys}


# ---------------------------------------------------------------------------
# SimCLR, MoCo
# ---------------------------------------------------------------------------
def hardness(m, tau):
    """How the softmax spreads its weight over the negatives: for 256 test digits in two views, each anchor's weights
    on its 510 negatives, sorted; the mean of those sorted weights, and the share taken by the top ten."""
    D = S.data()
    g = torch.Generator().manual_seed(5)
    x = S.fl(D["xte"][2000:2256])
    m.eval()
    with torch.no_grad():
        a, b = S.augment(x, g), S.augment(x, g)
        z = F.normalize(torch.cat([m.proj(m.enc(a)), m.proj(m.enc(b))]), dim=1)
    m.train()
    n = len(x)
    s = z @ z.t() / tau
    s.fill_diagonal_(float("-inf"))
    pos = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    s[torch.arange(2 * n), pos] = float("-inf")  # negatives only
    w = F.softmax(s, 1)
    ws = w.sort(1, descending=True).values
    return {"top10": float(ws[:, :10].sum(1).mean()), "top1": float(ws[:, 0].mean())}, {"wsorted": ws.mean(0)[:60].numpy()}


def neighbours(m, queries, pool_n=2000, k=8):
    """The k nearest test digits (by the encoder's representation, cosine) of each query, from the first pool_n."""
    D = S.data()
    f = S.features(m.enc, D["xte"][:pool_n])
    mu = f.mean(0, keepdim=True)
    q = F.normalize(S.features(m.enc, D["xte"][queries]) - mu, dim=1)
    f = F.normalize(f - mu, dim=1)
    s = q @ f.t()
    s[torch.arange(len(queries)), torch.as_tensor(queries)] = -2  # not the query itself
    return s.topk(k, dim=1).indices.numpy()


QUERIES = [3, 2, 1, 18, 4, 8]  # test digits 0..? whose neighbours are replayed (indices into the test set)


def compute_simclr():
    threads()
    part = CACHE.partial("simclr", {"steps": S.STEPS, "taus": TAUS})
    D = S.data()
    keys = {}

    def rec_nn(m, step):
        return {"nn": neighbours(m, QUERIES)}

    for tau in TAUS:
        keys[tau] = []
        for s in (SEEDS if tau == MAIN_TAU else SEEDS[:2]):
            k = f"simclr_t{tau:g}_s{s}"
            main0 = tau == MAIN_TAU and s == 0

            def extra(m, tau=tau):
                n1, a1 = z_extras(m, NESTED)
                n2, a2 = hardness(m, tau)
                if tau == MAIN_TAU:  # the probe after the projection head, against the one before it
                    ztr, zte = S.features(m.embed, D["xtr"], module=m), S.features(m.embed, D["xte"], module=m)
                    n2["zlinear"] = S.linear_probe(ztr, D["ytr"], zte, D["yte"])
                    n2["zknn"] = S.knn(ztr, D["ytr"], zte, D["yte"])
                return {**n1, **n2}, {**a1, **a2}

            run(part, k, "simclr", s, kw={"tau": tau}, extra=extra, record=rec_nn if main0 else None,
                record_at=replay_steps(S.STEPS) if main0 else None, keep_model=main0)
            keys[tau].append(k)
    keys["crop"] = []
    for s in SEEDS[:2]:
        k = f"simclr_crop_s{s}"
        run(part, k, "simclr", s, kw={"tau": MAIN_TAU, "light": True}, extra=z_extras)
        keys["crop"].append(k)
    main = keys[MAIN_TAU][0]
    out = {"runs": dict(part.done), "keys": {str(k): v for k, v in keys.items()},
           "summary": {str(k): finals(part.done, v) for k, v in keys.items()}, "queries": QUERIES,
           "rec_steps": part[main]["rec_steps"]}
    with np.load(RUNS / f"{main}.npz") as z:
        out["rec_nn"] = z["rec_nn"]
    out["pool_y"] = D["yte"][:2000].numpy()
    out["pool"] = D["xte"][:2000].numpy()  # the test digits the neighbours are drawn from, for the screen
    for tau in TAUS:  # how each temperature's softmax spreads its weight over the negatives (seed 0)
        with np.load(RUNS / f"simclr_t{tau:g}_s0.npz") as z:
            out[f"wsorted_{tau:g}"] = z["x_wsorted"]
    return out


def compute_moco():
    threads()
    part = CACHE.partial("moco", {"steps": S.STEPS})
    keys = []
    for s in SEEDS:
        k = f"moco_s{s}"
        run(part, k, "moco", s, kw={"tau": MAIN_TAU}, extra=z_extras, keep_model=s == 0)
        keys.append(k)
    return {"runs": dict(part.done), "keys": keys, "summary": finals(part.done, keys)}


# ---------------------------------------------------------------------------
# The sphere: three-number embeddings
# ---------------------------------------------------------------------------
SPHERE = {"simclr": ("simclr", {"tau": MAIN_TAU, "out": 3}), "naive": ("naive", {"out": 3}),
          "simsiam": ("simsiam", {"out": 3})}


def compute_sphere():
    threads()
    D = S.data()
    ids = torch.arange(2000, 2600)
    xs = S.fl(D["xte"][ids])
    g = torch.Generator().manual_seed(11)
    a, b = S.augment(xs, g), S.augment(xs, g)

    def record(m, step):
        m.eval()
        with torch.no_grad():
            z, za, zb = m.embed(xs), m.embed(a), m.embed(b)
        m.train()
        al, un = S.align_uniform(za, zb)
        return {"z": z.numpy().astype(np.float32), "align": al, "unif": un}

    def extra(m):  # how well the three numbers alone sort the digits: a k-NN vote on the sphere
        ztr, zte = S.features(m.embed, D["xtr"], module=m), S.features(m.embed, D["xte"], module=m)
        return {"zknn": S.knn(ztr, D["ytr"], zte, D["yte"])}, {}

    part = CACHE.partial("sphere", {"steps": S.STEPS})
    at = replay_steps(S.STEPS, 36)
    out = {"labels": D["yte"][ids].numpy(), "rec_steps": at}
    for name, (meth, kw) in SPHERE.items():
        k = f"sphere_{name}_s0"
        piece, arrs = run(part, k, meth, 0, kw=kw, record=record, record_at=at, few=False, extra=extra)
        out[f"{name}_zknn"] = piece["extra"]["zknn"]
        out[f"{name}_z"] = arrs["rec_z"]
        out[f"{name}_align"] = arrs["rec_align"]
        out[f"{name}_unif"] = arrs["rec_unif"]
        out[f"{name}_final"] = piece["final"]
    out["runs"] = dict(part.done)
    return out


# ---------------------------------------------------------------------------
# Collapse: the naive siamese net, SimSiam with and without the stop-gradient, BYOL
# ---------------------------------------------------------------------------
COLLAPSE = {"naive": ("naive", {}, SEEDS[:2]), "simsiam": ("simsiam", {}, SEEDS),
            "simsiam_nosg": ("simsiam", {"stopgrad": False}, SEEDS[:2]), "byol": ("byol", {}, SEEDS)}


def compute_collapse():
    threads()
    part = CACHE.partial("collapse", {"steps": S.STEPS})
    keys = {}
    for name, (meth, kw, seeds) in COLLAPSE.items():
        keys[name] = []
        for s in seeds:
            k = f"{name}_s{s}"
            run(part, k, meth, s, kw=kw, extra=z_extras, few=not name.endswith(("nosg",)) and name != "naive",
                keep_model=s == 0 and name in ("simsiam", "byol"))
            keys[name].append(k)
    out = {"runs": dict(part.done), "keys": keys, "summary": {n: finals(part.done, v) for n, v in keys.items()}}
    for n, ks in keys.items():
        with np.load(RUNS / f"{ks[0]}.npz") as z:
            out[f"{n}_spectrum"] = z["x_spectrum"]
    with _need("simclr", f"simclr_t{MAIN_TAU:g}_s0") as z:
        out["simclr_spectrum"] = z["x_spectrum"]
    return out


def _need(item: str, key: str):
    """The arrays of run ``key``, computing its item first if they are missing."""
    if not (RUNS / f"{key}.npz").exists():
        CACHE.save(item, ITEMS[item]())
    return np.load(RUNS / f"{key}.npz")


# ---------------------------------------------------------------------------
# Redundancy reduction: Barlow Twins, VICReg
# ---------------------------------------------------------------------------
def compute_redundancy():
    threads()
    D = S.data()
    g = torch.Generator().manual_seed(13)
    x = S.fl(D["xte"][2000:2512])
    va, vb = S.augment(x, g), S.augment(x, g)

    def rec_C(m, step):
        m.eval()
        with torch.no_grad():
            z1, z2 = S.standardize(m.proj(m.enc(va))), S.standardize(m.proj(m.enc(vb)))
        m.train()
        c = (z1.t() @ z2 / len(z1))
        return {"C": c[:24, :24].numpy().astype(np.float32), "diag": float(torch.diagonal(c).mean()),
                "off": float((c.pow(2).sum() - torch.diagonal(c).pow(2).sum()) / (c.shape[0] * (c.shape[0] - 1)))}

    part = CACHE.partial("redundancy", {"steps": S.STEPS})
    keys = {"barlow": [], "vicreg": [], "vicreg_novar": []}
    for s in SEEDS:
        k = f"barlow_s{s}"
        run(part, k, "barlow", s, extra=z_extras, record=rec_C if s == 0 else None, keep_model=s == 0,
            record_at=replay_steps(S.STEPS) if s == 0 else None)
        keys["barlow"].append(k)
    for s in SEEDS:
        k = f"vicreg_s{s}"
        run(part, k, "vicreg", s, extra=z_extras, keep_model=s == 0)
        keys["vicreg"].append(k)
    for s in SEEDS[:2]:
        k = f"vicreg_novar_s{s}"
        run(part, k, "vicreg", s, kw={"variance": False}, extra=z_extras, few=False)
        keys["vicreg_novar"].append(k)
    out = {"runs": dict(part.done), "keys": keys, "summary": {n: finals(part.done, v) for n, v in keys.items()},
           "rec_steps": part["barlow_s0"]["rec_steps"]}
    with np.load(RUNS / "barlow_s0.npz") as z:
        out["rec_C"], out["rec_diag"], out["rec_off"] = z["rec_C"], z["rec_diag"], z["rec_off"]
    return out


# ---------------------------------------------------------------------------
# DINO
# ---------------------------------------------------------------------------
DINOS = {"dino": ({}, SEEDS), "nocenter": ({"center": False}, SEEDS[:2]), "nosharpen": ({"tau_t": 0.1}, SEEDS[:2])}


def compute_dino():
    threads()
    D = S.data()
    x = S.fl(D["xte"][2000:2512])

    def rec_P(m, step):
        m.eval()
        with torch.no_grad():
            P = m.teacher_probs(m.thead(m.tenc(x)))
        m.train()
        Pm = P.mean(0)
        return {"Pmean": Pm.sort(descending=True).values.numpy(), "P0": P[0].sort(descending=True).values.numpy(),
                "used": float(torch.exp(-(Pm * Pm.clamp_min(1e-12).log()).sum())),
                "H": float(-(P * P.clamp_min(1e-12).log()).sum(1).mean())}

    part = CACHE.partial("dino", {"steps": S.STEPS})
    keys = {}
    for name, (kw, seeds) in DINOS.items():
        keys[name] = []
        for s in seeds:
            k = f"dino_{name}_s{s}"
            run(part, k, "dino", s, kw=kw, extra=z_extras, record=rec_P if s == 0 else None,
                keep_model=s == 0 and name == "dino",
                record_at=replay_steps(S.STEPS) if s == 0 else None, few=name == "dino")
            keys[name].append(k)
    out = {"runs": dict(part.done), "keys": keys, "summary": {n: finals(part.done, v) for n, v in keys.items()},
           "K": 256, "rec_steps": part["dino_dino_s0"]["rec_steps"]}
    for name in DINOS:
        with np.load(RUNS / f"dino_{name}_s0.npz") as z:
            for f in ("Pmean", "P0", "used", "H"):
                out[f"{name}_{f}"] = z[f"rec_{f}"]
    return out


# ---------------------------------------------------------------------------
# Masked modelling: MAE, BEiT
# ---------------------------------------------------------------------------
MAE_IDS = [3, 2, 1, 18, 4, 8]


def compute_mae():
    threads()
    D = S.data()
    x = S.fl(D["xte"][MAE_IDS])

    def record(m, step):
        g = torch.Generator().manual_seed(21)  # the same masks at every snapshot
        m.eval()
        with torch.no_grad():
            pred, masked = m.reconstruct(x, g)
        m.train()
        pm = S.pixel_mask(masked)
        shown = torch.where(pm, torch.zeros_like(x), x)
        filled = torch.where(pm, pred, x)
        return {"masked": u8(shown.squeeze(1).numpy()), "recon": u8(filled.squeeze(1).numpy()),
                "raw": u8(pred.squeeze(1).numpy()), "mask": masked.numpy()}

    part = CACHE.partial("mae", {"steps": S.STEPS})
    keys = {"0.75": []}
    for s in SEEDS:
        k = f"mae_r0.75_s{s}"
        run(part, k, "mae", s, kw={"ratio": 0.75}, record=record if s == 0 else None, keep_model=s == 0,
            record_at=replay_steps(S.STEPS) if s == 0 else None)
        keys["0.75"].append(k)
    for r in (0.5, 0.9):
        k = f"mae_r{r:g}_s0"
        run(part, k, "mae", 0, kw={"ratio": r}, few=False)
        keys[f"{r:g}"] = [k]
    out = {"runs": dict(part.done), "keys": keys, "summary": {n: finals(part.done, v) for n, v in keys.items()},
           "rec_steps": part["mae_r0.75_s0"]["rec_steps"], "ids": MAE_IDS, "orig": D["xte"][MAE_IDS].numpy()}
    with np.load(RUNS / "mae_r0.75_s0.npz") as z:
        for f in ("masked", "recon", "raw", "mask"):
            out[f"rec_{f}"] = z[f"rec_{f}"]
    return out


def compute_beit():
    threads()
    cb = S.kmeans_codebook(K=64, n=max(2000, int(20000 * min(1.0, S.SCALE * 10))), seed=0)
    part = CACHE.partial("beit", {"steps": S.STEPS})
    keys = []
    for s in SEEDS:
        k = f"beit_s{s}"
        run(part, k, "beit", s, kw={"codebook": cb}, keep_model=s == 0)
        keys.append(k)
    D = S.data()
    x = S.fl(D["xte"][MAE_IDS])
    codes = torch.cdist(S.patchify(x).reshape(-1, 16), cb).argmin(1).view(len(MAE_IDS), -1)
    quant = S.unpatchify(cb[codes]).squeeze(1)
    use = torch.bincount(torch.cdist(S.patchify(S.fl(D["xte"][:2000])).reshape(-1, 16), cb).argmin(1), minlength=64)
    return {"runs": dict(part.done), "keys": keys, "summary": finals(part.done, keys), "codebook": cb.numpy(),
            "codes": codes.numpy(), "quant": u8(quant.numpy()), "use": use.numpy(), "orig": D["xte"][MAE_IDS].numpy()}


def compute_jepa():
    threads()
    part = CACHE.partial("jepa", {"steps": S.STEPS})
    keys = {"ijepa": []}
    for s in SEEDS:
        k = f"ijepa_s{s}"
        run(part, k, "ijepa", s, keep_model=s == 0)
        keys["ijepa"].append(k)
    g = torch.Generator().manual_seed(4)  # three examples of I-JEPA's targets, for the screen
    ex = S.make("ijepa").masks(g, 3)
    return {"runs": dict(part.done), "keys": keys, "summary": {n: finals(part.done, v) for n, v in keys.items()},
            "ex_targets": ex.numpy(), "grid": S.GRID}


# ---------------------------------------------------------------------------
# Matryoshka embeddings
# ---------------------------------------------------------------------------
def compute_matryoshka():
    threads()
    part = CACHE.partial("matryoshka", {"steps": S.STEPS, "nested": NESTED})
    keys = []

    def extra(m):
        nums, arrs = z_extras(m, NESTED)
        D = S.data()
        z = F.normalize(S.features(m.embed, D["xte"][:2000], module=m), dim=1)
        for k in (4, 128):  # neighbours of the queries with the first k numbers (centred, as the k-NN vote)
            zk = F.normalize(z[:, :k] - z[:, :k].mean(0, keepdim=True), dim=1)
            s = zk[QUERIES] @ zk.t()
            s[torch.arange(len(QUERIES)), torch.as_tensor(QUERIES)] = -2
            arrs[f"nn{k}"] = s.topk(8, dim=1).indices.numpy()
        return nums, arrs

    for s in SEEDS:
        k = f"matryoshka_s{s}"
        run(part, k, "simclr", s, kw={"tau": MAIN_TAU, "nested": NESTED}, extra=extra, keep_model=s == 0)
        keys.append(k)
    out = {"runs": dict(part.done), "keys": keys, "summary": finals(part.done, keys), "nested": NESTED,
           "queries": QUERIES}
    with np.load(RUNS / "matryoshka_s0.npz") as z:
        out["nn4"], out["nn128"] = z["x_nn4"], z["x_nn128"]
    # the plain SimCLR embedding, truncated, for comparison: its neighbours with 4 and 128 numbers
    sc = load("simclr")
    out["plain_prefix"] = {k: sc["runs"][k]["extra"]["prefix_knn"] for k in sc["keys"][str(MAIN_TAU)]}
    m = trained_simclr()
    D = S.data()
    z = F.normalize(S.features(m.embed, D["xte"][:2000], module=m), dim=1)
    for k in (4, 128):
        zk = F.normalize(z[:, :k] - z[:, :k].mean(0, keepdim=True), dim=1)
        s_ = zk[QUERIES] @ zk.t()
        s_[torch.arange(len(QUERIES)), torch.as_tensor(QUERIES)] = -2
        out[f"plain_nn{k}"] = s_.topk(8, dim=1).indices.numpy()
    out["pool_y"] = D["yte"][:2000].numpy()
    return out


def trained_simclr():
    """The main SimCLR encoder (temperature 0.2, seed 0), from its saved weights (trained again if they are gone)."""
    key = f"simclr_t{MAIN_TAU:g}_s0"
    m = S.make("simclr", tau=MAIN_TAU)
    p = MODELS / f"{key}.pt"
    if not p.exists():
        part = CACHE.partial("simclr_again", {"steps": S.STEPS})
        torch.manual_seed(0)
        m = S.make("simclr", tau=MAIN_TAU)
        S.train(m, 0)
        save_model(m, key)
        part.finish()
    m.load_state_dict(torch.load(p))
    m.eval()
    return m


# ---------------------------------------------------------------------------
# Data curation: an unbalanced pool, curated by retrieval
# ---------------------------------------------------------------------------
SHARE = [0.36, 0.22, 0.14, 0.09, 0.06, 0.045, 0.035, 0.025, 0.015, 0.01]  # class shares of the raw pool, largest first


def compute_curation():
    """An unlabelled pool of 14,000 training digits whose classes are as unbalanced as web images (shares from 36% down
    to 1%, the order of the classes shuffled); DINOv2's recipe curates it: a small balanced set of 1,000 seed images,
    each retrieves its 4 nearest neighbours from the pool (by a self-supervised encoder trained elsewhere: our main
    SimCLR), duplicates removed. SimCLR is trained on each pool for the same number of steps, two seeds; the test is
    the usual balanced test set."""
    threads()
    D = S.data()
    g = np.random.default_rng(2024)
    order = g.permutation(10)
    share = np.zeros(10)
    share[order] = SHARE
    ytr_all = D["ytr"].numpy()
    smallest = int(np.bincount(ytr_all, minlength=10).min())  # every class must be able to take the largest share
    n_pool = 14000 if S.SCALE == 1.0 else int(0.9 * smallest / max(SHARE))
    counts = np.round(share * n_pool).astype(int)
    ytr = D["ytr"].numpy()
    used = np.zeros(len(ytr), bool)
    pool = []
    for c in range(10):
        idx = g.choice(np.flatnonzero(ytr == c), counts[c], replace=False)
        pool.append(idx)
        used[idx] = True
    pool = np.sort(np.concatenate(pool))
    seeds = np.concatenate([g.choice(np.flatnonzero((ytr == c) & ~used), 100, replace=False) for c in range(10)])
    enc = trained_simclr().enc
    fp = S.features(enc, D["xtr"][torch.as_tensor(pool)])
    mu = fp.mean(0, keepdim=True)
    fs = F.normalize(S.features(enc, D["xtr"][torch.as_tensor(seeds)]) - mu, dim=1)
    fp = F.normalize(fp - mu, dim=1)
    nn_ = (fs @ fp.t()).topk(4, dim=1).indices
    curated = np.unique(pool[nn_.numpy().ravel()])
    out = {"pool": pool, "curated": curated, "pool_counts": np.bincount(ytr[pool], minlength=10),
           "curated_counts": np.bincount(ytr[curated], minlength=10), "seed_counts": np.bincount(ytr[seeds], minlength=10),
           "share": share}
    part = CACHE.partial("curation", {"steps": S.STEPS, "pool": len(pool), "curated": len(curated)})
    keys = {"raw": [], "curated": []}
    yte = D["yte"]

    def extra(m):
        pred = S.knn_pred(S.features(m.enc, D["xtr"]), D["ytr"], S.features(m.enc, D["xte"]))
        per = [float((pred[yte == c] == c).float().mean()) for c in range(10)]
        return {"knn_by_digit": per}, {}

    for name, idx in (("raw", pool), ("curated", curated)):
        for s in SEEDS[:2]:
            k = f"curation_{name}_s{s}"
            run(part, k, "simclr", s, kw={"tau": MAIN_TAU}, pool=idx, extra=extra)
            keys[name].append(k)
    out.update({"runs": dict(part.done), "keys": keys, "summary": {n: finals(part.done, v) for n, v in keys.items()}})
    return out


# ---------------------------------------------------------------------------
# Two halves: do encoders that see different parts of the world converge?
# ---------------------------------------------------------------------------
def compute_halves():
    """Becker & Hinton's setting (1992), and a small test of the platonic representation hypothesis: one encoder sees
    only the top half of each digit, another only the bottom half; each is trained by itself with SimCLR. At each
    checkpoint, the mutual nearest neighbours (k = 10) of their representations of the same 1,000 test digits; and
    against untrained encoders and the raw half-images. Two seeds."""
    threads()
    D = S.data()
    ids = torch.arange(2000, 3000)
    top, bot = S.fl(D["xte"][ids][:, :14]), S.fl(D["xte"][ids][:, 14:])
    at = replay_steps(S.STEPS, 12)

    def recorder(x):
        def rec(m, step):
            m.eval()
            with torch.no_grad():
                f = m.enc(x)
            m.train()
            return {"f": f.numpy().astype(np.float16)}
        return rec

    part = CACHE.partial("halves", {"steps": S.STEPS})
    feats = {}
    for s in SEEDS[:2]:
        for half, x in (("top", top), ("bottom", bot)):
            k = f"halves_{half}_s{s}"
            _, arrs = run(part, k, "simclr", s, kw={"tau": MAIN_TAU}, half=half, record=recorder(x), record_at=at,
                          few=False)
            feats[(half, s)] = torch.from_numpy(arrs["rec_f"].astype(np.float32))
    out = {"rec_steps": at, "runs": dict(part.done), "labels": D["yte"][ids].numpy()}
    for s in SEEDS[:2]:
        T, Bt = feats[("top", s)], feats[("bottom", s)]
        out[f"align_s{s}"] = [S.mutual_knn(T[i], Bt[i]) for i in range(len(at))]
        out[f"cka_s{s}"] = [S.cka(T[i], Bt[i]) for i in range(len(at))]
    out["align_cross_seed_top"] = S.mutual_knn(feats[("top", 0)][-1], feats[("top", 1)][-1])
    out["align_pixels"] = S.mutual_knn(top.flatten(1), bot.flatten(1))
    # the same digits' labels as a "representation": the best two encoders could share (neighbours of the same class)
    out["same_class_top"] = float(np.mean([part[f"halves_top_s{s}"]["final"]["knn"] for s in SEEDS[:2]]))
    out["same_class_bottom"] = float(np.mean([part[f"halves_bottom_s{s}"]["final"]["knn"] for s in SEEDS[:2]]))
    return out


# ---------------------------------------------------------------------------
# Fine-tuning the whole network from 100 labels
# ---------------------------------------------------------------------------
FT_DRAWS, FT_PER, FT_STEPS = 3, 10, max(20, int(round(300 * S.SCALE)))


def finetune_from(enc, draws=FT_DRAWS, per=FT_PER, steps=FT_STEPS) -> list[float]:
    """Train the whole encoder and a linear head on 10 labelled digits per class (the same draws for every method),
    with crops, for ``steps`` full-batch updates; test accuracy for each draw."""
    import copy

    D = S.data()
    g = np.random.default_rng(0)
    yn = D["ytr"].numpy()
    accs = []
    for d in range(draws):
        idx = torch.from_numpy(np.concatenate([g.choice(np.flatnonzero(yn == c), per, replace=False)
                                               for c in range(10)]))
        e = copy.deepcopy(enc)
        torch.manual_seed(1000 + d)
        head = torch.nn.Linear(e.dim, 10)
        opt = torch.optim.Adam(list(e.parameters()) + list(head.parameters()), 1e-3)
        x, y = S.fl(D["xtr"][idx]), D["ytr"][idx]
        gg = torch.Generator().manual_seed(2000 + d)
        e.train()
        for _ in range(steps):
            L = F.cross_entropy(head(e(S.augment(x, gg, light=True))), y)
            opt.zero_grad()
            L.backward()
            opt.step()
        e.eval()
        with torch.no_grad():
            pred = torch.cat([head(e(S.fl(D["xte"][i:i + 1000]))).argmax(1) for i in range(0, len(D["xte"]), 1000)])
        accs.append(float((pred == D["yte"]).float().mean()))
    return accs


def trained(item: str, key: str):
    """Run ``key``'s trained method, from its saved weights (its item computed first, or the run repeated, if they
    are missing)."""
    p = MODELS / f"{key}.pt"
    if not p.exists():
        CACHE.load(item)
    if not p.exists():  # the item was cached but the weights deleted: compute the item again
        CACHE.save(item, ITEMS[item]())
    piece = load(item)["runs"][key]
    kw = dict(piece["kw"])
    if piece["name"] == "beit":
        kw["codebook"] = torch.zeros(64, 16)
    m = S.make(piece["name"], **kw)
    m.load_state_dict(torch.load(p))
    return m


def compute_finetune():
    """Every method's seed-0 network, fine-tuned whole from 100 labels (three draws), against the same network from
    scratch: the protocol under which masked models are said to shine."""
    threads()
    part = CACHE.partial("finetune", {"steps": FT_STEPS, "draws": FT_DRAWS})
    out = {}
    for name, item, pre, _ in TABLE:
        key = f"{pre}0"
        if name not in part:
            m = trained(item, key)
            if m.masked_input:
                S.recalibrate(m.enc)
            part[name] = finetune_from(m.enc)
            log(f"fine-tuned {name}: {np.mean(part[name]):.4f}")
        out[name] = part[name]
    if "scratch" not in part:
        torch.manual_seed(0)
        part["scratch"] = finetune_from(S.CNN())
    out["scratch"] = part["scratch"]
    return {"acc": out, "steps": FT_STEPS, "per": FT_PER, "draws": FT_DRAWS}


# ---------------------------------------------------------------------------
# Every method side by side
# ---------------------------------------------------------------------------
TABLE = [  # (label key, item, run keys prefix, architecture)
    ("supervised", "supervised", "supervised_s", "cnn"),
    ("rotation", "pretext", "rotation_s", "cnn"),
    ("simclr", "simclr", f"simclr_t{MAIN_TAU:g}_s", "cnn"),
    ("moco", "moco", "moco_s", "cnn"),
    ("byol", "collapse", "byol_s", "cnn"),
    ("simsiam", "collapse", "simsiam_s", "cnn"),
    ("barlow", "redundancy", "barlow_s", "cnn"),
    ("vicreg", "redundancy", "vicreg_s", "cnn"),
    ("dino", "dino", "dino_dino_s", "cnn"),
    ("matryoshka", "matryoshka", "matryoshka_s", "cnn"),
    ("mae", "mae", "mae_r0.75_s", "cnn"),
    ("beit", "beit", "beit_s", "cnn"),
    ("ijepa", "jepa", "ijepa_s", "cnn"),
]


def compute_compare():
    threads()
    base = load("baselines")
    rows = {}
    for name, item, pre, arch in TABLE:
        d = load(item)["runs"]
        ks = sorted(k for k in d if k.startswith(pre) and k[len(pre):].isdigit())
        rows[name] = {"arch": arch, "keys": ks, **finals(d, ks), "secs": float(np.mean([d[k]["secs"] for k in ks])),
                      "params": int(d[ks[0]]["params"]), "curves": {k: {"steps": d[k]["steps"], "knn": d[k]["knn"]}
                                                                     for k in ks}}
    r = base["random_cnn"]
    rows["random_cnn"] = {"arch": "cnn", "linear": _mmm([x["linear"] for x in r]), "knn": _mmm([x["knn"] for x in r]),
                          "few": _mmm([np.mean(x["few"]) for x in r]), "rank": _mmm([x["rank"] for x in r])}
    px = base["pixels"]
    rows["pixels"] = {"arch": "pixels", "linear": [px["linear"]] * 3, "knn": [px["knn"]] * 3,
                      "few": [float(np.mean(px["few"]))] * 3, "rank": [px["rank"]] * 3}
    # representations of the same 2,000 test digits, seed 0 of each method, compared two by two
    names = [n for n, *_ in TABLE] + ["random_cnn", "pixels"]
    feats = {}
    for n in names:
        key = rows[n]["keys"][0] if "keys" in rows[n] else ("random_cnn_s0" if n == "random_cnn" else "pixels")
        with np.load(RUNS / f"{key}.npz") as z:
            feats[n] = torch.from_numpy(z["feat"].astype(np.float32))
    nm = len(names)
    C, M = np.eye(nm), np.eye(nm)
    for i in range(nm):
        for j in range(i + 1, nm):
            C[i, j] = C[j, i] = S.cka(feats[names[i]], feats[names[j]])
            M[i, j] = M[j, i] = S.mutual_knn(feats[names[i]], feats[names[j]])
    # the same method from different seeds: how alike two runs of one recipe end up
    seeds_cka, seeds_mknn = {}, {}
    for n in ("supervised", "simclr", "byol", "dino", "mae"):
        ks = rows[n]["keys"]
        if len(ks) > 1:
            with np.load(RUNS / f"{ks[0]}.npz") as a, np.load(RUNS / f"{ks[1]}.npz") as b:
                fa, fb = torch.from_numpy(a["feat"].astype(np.float32)), torch.from_numpy(b["feat"].astype(np.float32))
            seeds_cka[n], seeds_mknn[n] = S.cka(fa, fb), S.mutual_knn(fa, fb)
    learned = [n for n, *_ in TABLE]
    idx = [names.index(n) for n in learned]
    mean_align = {n: float(np.mean([M[names.index(n), j] for j in idx if j != names.index(n)])) for n in learned}
    acc = {n: rows[n]["linear"][0] for n in learned}
    from scipy.stats import spearmanr

    rho = float(spearmanr([acc[n] for n in learned], [mean_align[n] for n in learned]).correlation)
    return {"rows": rows, "names": names, "cka": C, "mknn": M, "seeds_cka": seeds_cka, "seeds_mknn": seeds_mknn,
            "mean_align": mean_align, "spearman": rho, "steps": S.STEPS, "batch": S.B}


def _mmm(v):
    return [float(np.mean(v)), float(np.min(v)), float(np.max(v))]


ITEMS = {
    "views": compute_views,
    "baselines": compute_baselines,
    "infonce": compute_infonce,
    "pretext": compute_pretext,
    "supervised": compute_supervised,
    "simclr": compute_simclr,
    "moco": compute_moco,
    "sphere": compute_sphere,
    "collapse": compute_collapse,
    "redundancy": compute_redundancy,
    "dino": compute_dino,
    "mae": compute_mae,
    "beit": compute_beit,
    "jepa": compute_jepa,
    "matryoshka": compute_matryoshka,
    "curation": compute_curation,
    "halves": compute_halves,
    "finetune": compute_finetune,
    "compare": compute_compare,
}

if __name__ == "__main__":
    threads()
    CACHE.main(ITEMS, __doc__)
