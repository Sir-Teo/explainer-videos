"""Precompute everything numerical in Part 8 of the AI series ("Networks").

    python -m videos.ai.ai8.compute              # everything missing (Part 1's books: .cache/ai1)
    python -m videos.ai.ai8.compute --force lm

Results are cached in ``.cache/ai8/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    hinges    universal approximation, one hidden layer of ReLUs: a target curve fitted by least squares on n hinges
              (n = 2, 4, 8, 16, 64), each hinge's contribution, and the error
    sawtooth  depth: the tent map composed k times has 2^k pieces; a random ReLU net's linear regions in the plane,
              counted, for depth 1 ... 6 at a fixed number of neurons
    spiral    a 2 -> 32 -> 32 -> 32 -> 2 ReLU network trained on two interleaved spirals: decision regions and linear
              regions at several moments of training
    signal    signal propagation through 50 layers of width 256: the spread of activations (and of gradients) per
              layer for weights drawn with gain 0.7, 1 and 1.4 times He's sqrt(2 / n), ReLU; tanh at gain 1
    residual  a 40-layer plain network and the same with residual connections (and with LayerNorm), trained on the
              spirals: loss curves
    lm        Bengio et al.'s neural language model, for characters: 24 characters of context, each a learned vector of
              32 numbers, one hidden layer of 1,024, trained on Part 1's books; bits per character on the passage, and
              mixed with Part 6's Kneser-Ney (the scoreboard's new rows); the learned character vectors, and samples
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai8")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def target(x):
    """The curve the hinges build (illustrative)."""
    return np.sin(3.0 * x) * np.exp(-0.25 * x * x) + 0.35 * x


# ---------------------------------------------------------------------------
def compute_hinges():
    xs = np.linspace(-3, 3, 400)
    y = target(xs)
    out = dict(xs=xs, y=y, ns=[2, 4, 8, 16, 64])
    for n in out["ns"]:
        knots = np.linspace(-3, 3, n + 2)[1:-1]
        H = np.maximum(xs[:, None] - knots[None], 0)  # one hinge per knot
        A = np.c_[np.ones_like(xs), xs, H]
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        fit = A @ coef
        out[f"knots{n}"] = knots
        out[f"fit{n}"] = fit
        out[f"parts{n}"] = (H * coef[2:]).T  # each hinge's contribution
        out[f"base{n}"] = coef[0] + coef[1] * xs
        out[f"err{n}"] = float(np.sqrt(((fit - y) ** 2).mean()))
    errs = [out[f"err{n}"] for n in out["ns"]]
    assert all(b < a for a, b in zip(errs, errs[1:])) and errs[-1] < 0.01
    return out


# ---------------------------------------------------------------------------
def tent(x):
    return 1 - np.abs(2 * x - 1)


def regions(depth, width, seed, n=320):
    """Number of linear regions of a random ReLU net 2 -> width^depth on [-2, 2]^2 (counted on a grid), and the
    activation-pattern ids of the grid."""
    g = rng(seed)
    xs = np.linspace(-2, 2, n)
    P = np.stack(np.meshgrid(xs, xs), -1).reshape(-1, 2)
    h = P
    pats = []
    d_in = 2
    for _ in range(depth):
        W = g.normal(size=(d_in, width)) * math.sqrt(2 / d_in)
        b = g.normal(size=width) * 0.3
        z = h @ W + b
        pats.append(z > 0)
        h = np.maximum(z, 0)
        d_in = width
    pat = np.concatenate(pats, 1)
    _, inv = np.unique(pat, axis=0, return_inverse=True)
    return int(inv.max() + 1), inv.reshape(n, n)


def compute_sawtooth():
    xs = np.linspace(0, 1, 2049)
    teeth = {}
    y = xs.copy()
    for k in range(1, 6):
        y = tent(y)
        teeth[f"tent{k}"] = y.copy()
    # linear regions at a fixed budget of 48 neurons, spread over 1, 2, 3, 4, 6 layers
    counts, maps = [], {}
    for depth in (1, 2, 3, 4, 6):
        width = 48 // depth
        c = [regions(depth, width, s)[0] for s in range(3)]
        counts.append(float(np.mean(c)))
        maps[f"map{depth}"] = regions(depth, width, 0, n=200)[1]
    return dict(xs=xs, depths=[1, 2, 3, 4, 6], counts=counts, **teeth, **maps)


# ---------------------------------------------------------------------------
def spirals(n=300, seed=0, noise=0.18):
    g = rng(seed)
    t = np.sqrt(g.uniform(0, 1, n)) * 3 * math.pi
    a = np.stack([t * np.cos(t), t * np.sin(t)], 1) / 3 + g.normal(scale=noise, size=(n, 2))
    b = -a + g.normal(scale=noise / 2, size=(n, 2))
    return np.vstack([a, b]).astype(np.float32), np.r_[np.zeros(n), np.ones(n)].astype(np.int64)


def compute_spiral():
    import torch

    torch.set_num_threads(1)
    torch.manual_seed(0)
    X, y = spirals()
    net = torch.nn.Sequential(torch.nn.Linear(2, 32), torch.nn.ReLU(), torch.nn.Linear(32, 32), torch.nn.ReLU(),
                              torch.nn.Linear(32, 32), torch.nn.ReLU(), torch.nn.Linear(32, 2))
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    Xt, yt = torch.tensor(X), torch.tensor(y)
    xs = np.linspace(-3.4, 3.4, 170)
    G = torch.tensor(np.stack(np.meshgrid(xs, xs), -1).reshape(-1, 2), dtype=torch.float32)
    snaps, keep = {}, (0, 50, 200, 600, 3000)
    curve = []
    for step in range(3001):
        if step in keep:
            with torch.no_grad():
                h, pats = G, []
                for layer in net:
                    h = layer(h)
                    if isinstance(layer, torch.nn.Linear) and layer.out_features == 32:
                        pats.append((h > 0).numpy())
                prob = torch.softmax(h, 1)[:, 1].numpy().reshape(len(xs), len(xs))
                _, inv = np.unique(np.concatenate(pats, 1), axis=0, return_inverse=True)
                snaps[f"prob{step}"] = prob
                snaps[f"regions{step}"] = inv.reshape(len(xs), len(xs))
                snaps[f"nreg{step}"] = int(inv.max() + 1)
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(net(Xt), yt)
        loss.backward()
        opt.step()
        if step % 25 == 0:
            with torch.no_grad():
                curve.append((step, float(loss), float((net(Xt).argmax(1) == yt).float().mean())))
    curve = np.array(curve)
    assert curve[-1, 2] > 0.97
    return dict(X=X, y=y, xs=xs, keep=list(keep), curve=curve, **snaps)


# ---------------------------------------------------------------------------
def compute_signal():
    g = rng(2015)  # He, Zhang, Ren & Sun, 2015
    L, n, batch = 50, 256, 512
    out = dict(L=L, n=n)
    x0 = g.normal(size=(batch, n))
    for name, gain, act in (("small", 0.7, "relu"), ("he", 1.0, "relu"), ("big", 1.4, "relu"), ("tanh", 1.0, "tanh")):
        Ws = [g.normal(size=(n, n)) * gain * math.sqrt((2.0 if act == "relu" else 1.0) / n) for _ in range(L)]
        h, sds, hists, pre = x0, [], [], []
        for W in Ws:
            z = h @ W
            pre.append(z)
            h = np.maximum(z, 0) if act == "relu" else np.tanh(z)
            sds.append(float(np.sqrt((h ** 2).mean())))
            hists.append(np.histogram(z.ravel() / max(z.std(), 1e-300), bins=40, range=(-4, 4))[0])
        # gradients flowing back from a random signal at the top
        gr, gsds = g.normal(size=(batch, n)), []
        for W, z in zip(Ws[::-1], pre[::-1]):
            d = (z > 0).astype(float) if act == "relu" else 1 - np.tanh(z) ** 2
            gr = (gr * d) @ W.T
            gsds.append(float(np.sqrt((gr ** 2).mean())))
        out[f"sd_{name}"] = np.array(sds)
        out[f"gsd_{name}"] = np.array(gsds[::-1])
        out[f"hist_{name}"] = np.array(hists)
    assert out["sd_small"][-1] < 1e-3 * out["sd_he"][-1] and out["sd_big"][-1] > 1e3 * out["sd_he"][-1]
    assert 0.1 < out["sd_he"][-1] / out["sd_he"][0] < 10
    return out


# ---------------------------------------------------------------------------
def compute_residual():
    import torch

    torch.set_num_threads(1)  # small matrices: one thread is fastest, and leaves the other cores free
    X, y = spirals()
    Xt, yt = torch.tensor(X), torch.tensor(y)

    class Net(torch.nn.Module):
        def __init__(self, depth=40, width=32, residual=False, norm=False):
            super().__init__()
            self.inp = torch.nn.Linear(2, width)
            self.layers = torch.nn.ModuleList([torch.nn.Linear(width, width) for _ in range(depth)])
            self.norms = torch.nn.ModuleList([torch.nn.LayerNorm(width) if norm else torch.nn.Identity()
                                              for _ in range(depth)])
            self.out = torch.nn.Linear(width, 2)
            self.residual = residual
            if residual:  # each block starts small, so the whole stack starts near the identity
                for lay in self.layers:
                    torch.nn.init.normal_(lay.weight, std=0.3 / math.sqrt(width))

        def forward(self, x):
            h = self.inp(x)
            for lay, nm in zip(self.layers, self.norms):
                f = lay(torch.relu(nm(h)))
                h = h + f if self.residual else f
            return self.out(torch.relu(h))

    out = {}
    for name, kw in (("plain", {}), ("residual", dict(residual=True)), ("residual_norm", dict(residual=True, norm=True))):
        torch.manual_seed(1)
        net = Net(**kw)
        opt = torch.optim.Adam(net.parameters(), lr=1e-3)
        curve = []
        for step in range(1501):
            opt.zero_grad()
            loss = torch.nn.functional.cross_entropy(net(Xt), yt)
            loss.backward()
            opt.step()
            if step % 20 == 0:
                with torch.no_grad():
                    curve.append((step, float(loss), float((net(Xt).argmax(1) == yt).float().mean())))
        out[name] = np.array(curve)
    assert out["residual"][-1, 2] > 0.95 and out["plain"][-1, 2] < out["residual"][-1, 2] - 0.1
    return out


# ---------------------------------------------------------------------------
N_CTX, EMB, HID = 24, 32, 1024


def compute_lm():
    import torch

    from videos.ai.ai1 import compute as c1

    torch.manual_seed(2003)  # Bengio, Ducharme, Vincent & Jauvin, 2003
    torch.set_num_threads(2)
    texts = {k: c1.text(k) for k in ("train", "valid", "passage")}
    chars = sorted(set("".join(texts.values())))
    K = len(chars)
    cp = np.array([ord(c) for c in chars])
    order = np.argsort(cp)

    def enc(t):
        a = np.frombuffer(t.encode("utf-32-le"), dtype=np.uint32)
        return torch.tensor(order[np.searchsorted(cp[order], a)])

    tr, va, ps = (enc(texts[k]) for k in ("train", "valid", "passage"))
    emb = torch.nn.Embedding(K, EMB)
    hid = torch.nn.Linear(N_CTX * EMB, HID)
    outl = torch.nn.Linear(HID, K)
    direct = torch.nn.Linear(N_CTX * EMB, K, bias=False)  # Bengio et al.'s direct connections
    params = [*emb.parameters(), *hid.parameters(), *outl.parameters(), *direct.parameters()]
    n_params = sum(p.numel() for p in params)

    def logits(ctx):
        e = emb(ctx).reshape(len(ctx), -1)
        return outl(torch.tanh(hid(e))) + direct(e)

    def windows(seq, pos):
        return torch.stack([seq[pos - N_CTX + j] for j in range(N_CTX)], 1)

    def bits(seq, limit=None):
        with torch.no_grad():
            pos = torch.arange(N_CTX, len(seq) if limit is None else min(len(seq), limit))
            tot = 0.0
            for i in range(0, len(pos), 4096):
                p = pos[i:i + 4096]
                tot += float(torch.nn.functional.cross_entropy(logits(windows(seq, p)), seq[p], reduction="sum"))
            return tot / len(pos) / math.log(2)

    steps, batch = 50000, 1024
    saved = CACHE.dir / "lm.pt"  # the trained weights, kept so the analysis below can be rerun without retraining
    config = dict(n_ctx=N_CTX, emb=EMB, hid=HID, steps=steps, batch=batch, K=K)
    state = torch.load(saved) if saved.exists() else None
    if state is not None and state["config"] == config:
        for p_, v_ in zip(params, state["params"]):
            p_.data.copy_(v_)
        curve = state["curve"]
        print("    reusing the trained weights in", saved, flush=True)
    else:
        opt = torch.optim.Adam(params, lr=2e-3)
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-3, total_steps=steps, pct_start=0.05)
        g = rng(2003)
        curve = []
        for step in range(1, steps + 1):
            pos = torch.tensor(g.integers(N_CTX, len(tr), batch))
            loss = torch.nn.functional.cross_entropy(logits(windows(tr, pos)), tr[pos])
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            if step % 2000 == 0 or step in (100, 300, 1000):
                curve.append((step, bits(va, 200_000), bits(ps)))
                print(f"    step {step}: valid {curve[-1][1]:.3f}  passage {curve[-1][2]:.3f}", flush=True)
        CACHE.dir.mkdir(parents=True, exist_ok=True)
        torch.save(dict(config=config, params=[p_.detach().clone() for p_ in params], curve=curve), saved)
    passage_bits = bits(ps)
    valid_bits = bits(va)
    # the learned vectors of the letters, digits and common punctuation, in 2D (PCA)
    E = emb.weight.detach().numpy()
    show = [i for i, c in enumerate(chars) if c.isalnum() or c in " .,;:!?'\"-"]
    Es = E[show] - E[show].mean(0)
    u, s, vt = np.linalg.svd(Es, full_matrices=False)
    xy = Es @ vt[:2].T
    # samples
    samples = []
    with torch.no_grad():
        for seed, prompt in ((1, "Spade sat down in the armchair, and "), (2, "It was the best of times, "),
                             (3, "The telephone rang. "), (4, "\"I don't know,\" he said. ")):
            torch.manual_seed(seed)
            ctx = list(enc(" " * N_CTX + prompt).numpy())  # padded on the left, so even a short prompt fills the window
            outc = []
            for _ in range(160):
                z = logits(torch.tensor([ctx[-N_CTX:]]))[0]
                c = int(torch.multinomial(torch.softmax(z, 0), 1))
                ctx.append(c)
                outc.append(chars[c])
            samples.append([prompt, "".join(outc)])
    # Bengio et al.'s best results mixed the network with a smoothed n-gram model: here, Part 6's Kneser-Ney
    from videos.ai.ai6 import compute as c6

    kn = c6.load("kn")
    M = int(kn["best"])
    assert kn["K"] == K
    a_tr = tr.numpy()
    model = c6.kn_model(c6.ngram_tables(a_tr, K, M), K, M)

    def nn_probs(seq, limit=None):
        with torch.no_grad():
            pos = torch.arange(N_CTX, len(seq) if limit is None else min(len(seq), limit))
            out = []
            for i in range(0, len(pos), 4096):
                p = pos[i:i + 4096]
                out.append(torch.softmax(logits(windows(seq, p)), 1).gather(1, seq[p][:, None])[:, 0].numpy())
            return np.concatenate(out).astype(float)

    def kn_probs(seq, limit=None):
        a = seq.numpy()[: (len(seq) if limit is None else limit)]
        return c6.kn_probs(model, a, K, M)[N_CTX - M:]  # aligned with the network's positions

    pv_nn, pv_kn = nn_probs(va, 200_000), kn_probs(va, 200_000)
    pp_nn, pp_kn = nn_probs(ps), kn_probs(ps)
    lams = np.linspace(0, 1, 101)
    vb = [float(-np.log2(l_ * pv_nn + (1 - l_) * pv_kn).mean()) for l_ in lams]
    lam = float(lams[int(np.argmin(vb))])  # the mixing weight, chosen on held-out text, never on the passage
    mix_bits = float(-np.log2(lam * pp_nn + (1 - lam) * pp_kn).mean())
    kn_alone = float(-np.log2(pp_kn).mean())
    assert abs(kn_alone - kn["best_bits"]) < 0.02, (kn_alone, kn["best_bits"])
    assert mix_bits < min(kn_alone, passage_bits)
    return dict(K=K, n_ctx=N_CTX, emb=EMB, hid=HID, n_params=int(n_params), steps=steps, batch=batch,
                curve=np.array(curve), passage_bits=passage_bits, valid_bits=valid_bits, chars=[chars[i] for i in show],
                xy=xy, samples=samples, kn=kn["best_bits"], kn_order=M, lam=lam, mix_bits=mix_bits, lam_curve=np.array(vb))


ITEMS = {
    "hinges": compute_hinges,
    "sawtooth": compute_sawtooth,
    "spiral": compute_spiral,
    "signal": compute_signal,
    "residual": compute_residual,
    "lm": compute_lm,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
