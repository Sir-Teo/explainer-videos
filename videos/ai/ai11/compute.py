"""Precompute everything numerical in Part 11 of the AI series ("Going Downhill").

    python -m videos.ai.ai11.compute              # everything missing (needs Part 1's books and Part 6's pages)
    python -m videos.ai.ai11.compute --force optim

Results are cached in ``.cache/ai11/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

The workhorse task: a small character model (8 characters of context, 16-number character vectors, 256 tanh units)
on Part 1's books, scored in bits per character on held-out text.

Items:
    noise     stochastic gradient descent on a real loss with two weights (logistic regression on Part 6's two word
              rates): paths for batch sizes 1, 16 and all, and the cloud each settles into
    valley    a narrow valley (curvatures 1 and 30): gradient descent, momentum and Adam, step by step
    eos       the edge of stability: full-batch gradient descent on the spirals (squared error) at two learning
              rates; the sharpness (the Hessian's largest eigenvalue, by power iteration on Hessian-vector products)
              climbs to 2/eta
    optim     the character model trained by SGD, SGD with momentum, Adam, AdamW and Muon: held-out bits per step
    muon      Newton-Schulz orthogonalization: the singular values of a real gradient matrix before and after
    schedule  AdamW with a constant, a cosine and a warmup-stable-decay learning rate: held-out bits per step
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai11")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_noise():
    from videos.ai.ai6 import compute as c5

    X, y, test, X2 = c5.split()
    Z, _, _, _ = c5.standardize(X2[~test], X2[test])
    t = 2.0 * y[~test] - 1
    n = len(t)

    def loss(w):
        return np.log1p(np.exp(-t * (Z @ w))).mean(axis=-1) if w.ndim == 1 else \
            np.log1p(np.exp(-t[None] * (w @ Z.T))).mean(1)

    def grad(w, idx):
        m = -t[idx] / (1 + np.exp(t[idx] * (Z[idx] @ w)))
        return (m[:, None] * Z[idx]).mean(0)

    # the loss on a grid, for contour lines
    w1, w2 = np.linspace(-1.4, 2.0, 137), np.linspace(-3.4, 0.6, 161)
    W = np.stack(np.meshgrid(w1, w2), -1).reshape(-1, 2)
    L = loss(W).reshape(len(w2), len(w1))
    w_star = W[np.argmin(L)]
    for _ in range(3000):  # polish the minimum by full-batch descent
        w_star = w_star - 0.5 * grad(w_star, np.arange(n))
    out = dict(w1=w1, w2=w2, L=L, w_star=w_star, n=n)
    lr, steps = 0.25, 300
    for B in (1, 16, n):
        g = rng(B)
        w, path = np.array([-1.0, 0.2]), []
        for _ in range(steps):
            path.append(w.copy())
            idx = g.choice(n, size=B, replace=False) if B < n else np.arange(n)
            w = w - lr * grad(w, idx)
        path.append(w.copy())
        # the stationary cloud: keep going from the minimum
        w, cloud = w_star.copy(), []
        for k in range(4000):
            idx = g.choice(n, size=B, replace=False) if B < n else np.arange(n)
            w = w - lr * grad(w, idx)
            if k % 10 == 0:
                cloud.append(w.copy())
        out[f"path{B}"] = np.array(path)
        out[f"cloud{B}"] = np.array(cloud)
        out[f"spread{B}"] = float(np.sqrt(((np.array(cloud) - w_star) ** 2).sum(1).mean()))
    assert out["spread1"] > 2.5 * out["spread16"] and out[f"spread{n}"] < 1e-3
    return out


# ---------------------------------------------------------------------------
VALLEY = np.array([1.0, 30.0])  # curvatures


def compute_valley():
    def g(p):
        return VALLEY * p

    start = np.array([-4.5, 0.9])
    out = {}
    lr = 0.06  # 2 / 30 = 0.067: just stable in the steep direction
    p, path = start.copy(), [start.copy()]
    for _ in range(80):
        p = p - lr * g(p)
        path.append(p.copy())
    out["gd"] = np.array(path)
    p, v, path = start.copy(), np.zeros(2), [start.copy()]
    for _ in range(80):
        v = 0.85 * v + g(p)
        p = p - 0.012 * v
        path.append(p.copy())
    out["momentum"] = np.array(path)
    p, m, s, path = start.copy(), np.zeros(2), np.zeros(2), [start.copy()]
    for k in range(1, 81):
        gr = g(p)
        m = 0.9 * m + 0.1 * gr
        s = 0.999 * s + 0.001 * gr * gr
        p = p - 0.25 * (m / (1 - 0.9 ** k)) / (np.sqrt(s / (1 - 0.999 ** k)) + 1e-8)
        path.append(p.copy())
    out["adam"] = np.array(path)
    dist = {k: np.linalg.norm(v, axis=1) for k, v in out.items()}
    out["steps_to_5pct"] = {k: int(np.argmax(d < 0.05 * np.linalg.norm(start))) for k, d in dist.items()}
    assert out["steps_to_5pct"]["momentum"] < out["steps_to_5pct"]["gd"]
    return out


# ---------------------------------------------------------------------------
def compute_eos():
    import torch

    from videos.ai.ai9.compute import spirals

    torch.set_num_threads(1)
    X, y = spirals(n=200, seed=1)
    Xt, yt = torch.tensor(X, dtype=torch.float64), torch.tensor(y)
    Yt = torch.nn.functional.one_hot(yt, 2).double()
    out = {}
    for eta in (0.05, 0.1):
        torch.manual_seed(0)
        net = torch.nn.Sequential(torch.nn.Linear(2, 64), torch.nn.Tanh(), torch.nn.Linear(64, 64), torch.nn.Tanh(),
                                  torch.nn.Linear(64, 2)).double()
        params = list(net.parameters())

        def loss_fn():  # squared error against one-hot targets, as in Cohen et al.'s cleanest examples
            return 0.5 * ((net(Xt) - Yt) ** 2).sum(1).mean()

        def sharpness(iters=20):
            v = [torch.randn_like(p) for p in params]
            nv = math.sqrt(sum(float((a * a).sum()) for a in v))
            v = [a / nv for a in v]
            lam = 0.0
            for _ in range(iters):
                g = torch.autograd.grad(loss_fn(), params, create_graph=True)
                hv = torch.autograd.grad(sum((a * b).sum() for a, b in zip(g, v)), params)
                lam = sum(float((a * b).sum()) for a, b in zip(hv, v))
                nh = math.sqrt(sum(float((a * a).sum()) for a in hv))
                v = [a / nh for a in hv]
            return lam

        curve = []
        for step in range(4001):
            if step % 40 == 0:
                curve.append((step, float(loss_fn()), sharpness()))
            net.zero_grad()
            loss_fn().backward()
            with torch.no_grad():
                for p in params:
                    p -= eta * p.grad
        out[f"curve{eta}"] = np.array(curve)
    for eta in (0.05, 0.1):
        c = out[f"curve{eta}"]
        late = c[len(c) // 2:, 2]
        assert late.max() > 0.8 * 2 / eta, (eta, late.max())  # the sharpness reaches the edge ...
        assert np.median(late) < 1.3 * 2 / eta  # ... and hovers there
    out["etas"] = [0.05, 0.1]
    return out


# ---------------------------------------------------------------------------
CTX, EMB, HID = 8, 16, 256


def char_data():
    from videos.ai.ai1 import compute as c1

    texts = {k: c1.text(k) for k in ("train", "valid")}
    chars = sorted(set("".join(texts.values())))
    cp = np.array([ord(c) for c in chars])
    order = np.argsort(cp)

    def enc(t):
        a = np.frombuffer(t.encode("utf-32-le"), dtype=np.uint32)
        return order[np.searchsorted(cp[order], a)]

    return enc(texts["train"]), enc(texts["valid"])[:100_000], len(chars)


def newton_schulz(G, steps=5):
    """Muon's orthogonalization: push every singular value of G towards 1 (Keller Jordan's quintic iteration)."""

    a, b, c = 3.4445, -4.7750, 2.0315
    X = G / (G.norm() + 1e-7)
    tall = X.shape[0] > X.shape[1]
    if tall:
        X = X.T
    for _ in range(steps):
        A = X @ X.T
        X = a * X + (b * A + c * A @ A) @ X
    return X.T if tall else X


def char_vocab():
    from videos.ai.ai1 import compute as c1

    return sorted(set("".join(c1.text(k) for k in ("train", "valid"))))


WRITE_PROMPT, WRITE_LEN, WRITE_AT = "It was a", 72, (0, 100, 300, 1000, 2500)


def train_char(opt_name, steps=2500, schedule="constant", lr=None, seed=0, log_every=100, grab=None, write_at=()):
    import torch

    torch.set_num_threads(1)
    torch.manual_seed(seed)
    tr, va, K = char_data()
    tr, va = torch.tensor(tr), torch.tensor(va)
    emb = torch.nn.Embedding(K, EMB)
    hid = torch.nn.Linear(CTX * EMB, HID)
    hid2 = torch.nn.Linear(HID, HID)
    out = torch.nn.Linear(HID, K)
    mats = [hid.weight, hid2.weight]  # the hidden matrices (Muon's domain)
    rest = [emb.weight, hid.bias, hid2.bias, out.weight, out.bias]

    def logits(ctx):
        h = torch.tanh(hid(emb(ctx).reshape(len(ctx), -1)))
        return out(torch.tanh(hid2(h)) + h)

    def windows(seq, pos):
        return torch.stack([seq[pos - CTX + j] for j in range(CTX)], 1)

    def bits():
        with torch.no_grad():
            pos = torch.arange(CTX, len(va))
            return float(torch.nn.functional.cross_entropy(logits(windows(va, pos)), va[pos])) / math.log(2)

    base = dict(sgd=0.5, momentum=0.05, adam=2e-3, adamw=2e-3, muon=2e-3)[opt_name] if lr is None else lr
    params = mats + rest
    if opt_name == "sgd":
        opts = [torch.optim.SGD(params, lr=base)]
    elif opt_name == "momentum":
        opts = [torch.optim.SGD(params, lr=base, momentum=0.9)]
    elif opt_name == "adam":
        opts = [torch.optim.Adam(params, lr=base)]
    elif opt_name == "adamw":
        opts = [torch.optim.AdamW(params, lr=base, weight_decay=0.1)]
    else:  # muon on the hidden matrices, AdamW on the rest
        opts = [torch.optim.AdamW(rest, lr=base, weight_decay=0.1)]
        mom = [torch.zeros_like(m) for m in mats]
    lrs = []

    def lr_at(k):
        if schedule == "constant":
            return 1.0
        if schedule == "cosine":
            w = min(1.0, k / (0.02 * steps))
            return w * 0.5 * (1 + math.cos(math.pi * k / steps))
        w = min(1.0, k / (0.02 * steps))  # warmup, stable, then a linear decay over the last 20%
        return w * min(1.0, (steps - k) / (0.2 * steps))

    def write():
        """Continue the same prompt with the same random draws (temperature 0.8), so checkpoints differ only by the model."""
        chars = char_vocab()
        seq = [chars.index(c) for c in WRITE_PROMPT]
        gen = torch.Generator().manual_seed(1234)
        with torch.no_grad():
            for _ in range(WRITE_LEN):
                p = torch.softmax(logits(torch.tensor([seq[-CTX:]])) / 0.8, -1)
                seq.append(int(torch.multinomial(p[0], 1, generator=gen)))
        return "".join(chars[i] for i in seq[CTX:])

    g = rng(seed + 1)
    curve, grabbed = [(0, bits())], None
    writes = {0: write()} if 0 in write_at else {}
    for k in range(1, steps + 1):
        f = lr_at(k)
        lrs.append(f)
        for o in opts:
            for pg in o.param_groups:
                pg["lr"] = base * f
        pos = torch.tensor(g.integers(CTX, len(tr), 256))
        loss = torch.nn.functional.cross_entropy(logits(windows(tr, pos)), tr[pos])
        for o in opts:
            o.zero_grad()
        for m in mats:
            m.grad = None
        loss.backward()
        if grab is not None and k == grab:
            grabbed = hid2.weight.grad.detach().clone()
        if opt_name == "muon":
            with torch.no_grad():
                for m, buf in zip(mats, mom):
                    buf.mul_(0.95).add_(m.grad)
                    upd = newton_schulz(m.grad + 0.95 * buf)  # Nesterov-style
                    scale = max(1.0, m.shape[0] / m.shape[1]) ** 0.5
                    m.mul_(1 - 0.02 * f * 0.01)  # decoupled weight decay, per step the same as AdamW's (2e-3 x 0.1)
                    m.add_(upd, alpha=-0.02 * f * scale)  # Muon's own learning rate, 0.02
        for o in opts:
            o.step()
        if k % log_every == 0:
            curve.append((k, bits()))
        if k in write_at:
            writes[k] = write()
    if write_at:
        return np.array(curve), writes
    return np.array(curve), np.array(lrs), grabbed


def compute_optim():
    out = {}
    for name in ("sgd", "momentum", "adam", "adamw", "muon"):
        curve, _, _ = train_char(name)
        out[name] = curve
        print(f"    {name}: {curve[-1, 1]:.3f}", flush=True)
    finals = {k: float(v[-1, 1]) for k, v in out.items()}
    assert finals["adam"] < finals["sgd"] and finals["muon"] < finals["sgd"]
    return dict(**out, finals=finals, names=list(out))


def compute_writing():
    """What the race's numbers read like: SGD and AdamW continuing the same prompt at checkpoints."""
    out = dict(steps=list(WRITE_AT), prompt=WRITE_PROMPT)
    for name in ("sgd", "adamw"):
        curve, writes = train_char(name, write_at=WRITE_AT)
        out[f"text_{name}"] = [writes[k] for k in WRITE_AT]
        out[f"bits_{name}"] = [float(np.interp(k, curve[:, 0], curve[:, 1])) for k in WRITE_AT]
        for k in WRITE_AT:
            print(f"    {name} {k}: {writes[k]!r}", flush=True)
    return out


def compute_muon():
    import torch

    _, _, G = train_char("adamw", steps=300, grab=300, log_every=300)
    s_before = torch.linalg.svdvals(G).numpy()
    s_after = torch.linalg.svdvals(newton_schulz(G)).numpy()
    assert s_before.max() / max(s_before.min(), 1e-12) > 20 and np.median(s_after) > 0.5
    return dict(before=s_before / s_before.max(), after=s_after, raw_max=float(s_before.max()))


def compute_schedule():
    out = {}
    for sched in ("constant", "cosine", "wsd"):
        curve, lrs, _ = train_char("adamw", steps=4000, schedule=sched, lr=3e-3)
        out[sched] = curve
        out[f"lr_{sched}"] = lrs[::20]
        print(f"    {sched}: {curve[-1, 1]:.3f}", flush=True)
    finals = {k: float(out[k][-1, 1]) for k in ("constant", "cosine", "wsd")}
    assert finals["wsd"] < finals["constant"] and finals["cosine"] < finals["constant"]
    return dict(**out, finals=finals)


ITEMS = {
    "noise": compute_noise,
    "valley": compute_valley,
    "eos": compute_eos,
    "optim": compute_optim,
    "muon": compute_muon,
    "writing": compute_writing,
    "schedule": compute_schedule,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
