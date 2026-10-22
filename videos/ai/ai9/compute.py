"""Precompute everything numerical in Part 9 of the AI series ("Networks").

    python -m videos.ai.ai9.compute              # everything missing (Part 1's books: .cache/ai1)
    python -m videos.ai.ai9.compute --force lm

Results are cached in ``.cache/ai9/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Every network here is
trained on this computer (PyTorch on the CPU, or the series' own autodiff from Part 4); the published numbers on
screen are cited there.

Items:
    hinges    universal approximation, one hidden layer of ReLUs: a target curve fitted by least squares on n hinges
              (n = 2 ... 256), each hinge's contribution, and the error against n
    sawtooth  depth: the tent map composed k times has 2^k pieces; a random ReLU net's linear regions in the plane,
              counted, for depth 1 ... 6 at a fixed number of neurons
    spiral    a 2 -> 32 -> 32 -> 32 -> 2 ReLU network trained on two interleaved spirals: decision regions and linear
              regions at checkpoints through training
    signal    signal propagation through 50 layers of width 256: the spread of activations (and of gradients) per
              layer for weights drawn with gain 0.7, 1 and 1.4 times He's sqrt(2 / n), ReLU; tanh at gain 1
    residual  a 40-layer plain network and the same with residual connections (and with LayerNorm), trained on the
              spirals: loss curves
    kn        Part 7's interpolated Kneser-Ney on Part 1's books, every order (computed with Part 7's code, so this
              part doesn't depend on Part 7's cache)
    lm        Bengio et al.'s neural language model, for characters: 24 characters of context, each a learned vector of
              32 numbers, one hidden layer of 1,024, trained on Part 1's books; bits per character on the passage, and
              mixed with Kneser-Ney (the scoreboard's new rows); the learned character vectors; what it writes at
              checkpoints through training
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai9")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def target(x):
    """The curve the hinges build (illustrative)."""
    return np.sin(3.0 * x) * np.exp(-0.25 * x * x) + 0.35 * x


# ---------------------------------------------------------------------------
HINGE_NS = [2, 4, 8, 16, 32, 64, 128, 256]


def compute_hinges():
    xs = np.linspace(-3, 3, 2001)
    y = target(xs)
    out = dict(xs=xs[::5], y=y[::5], ns=HINGE_NS)
    errs = []
    for n in HINGE_NS:
        knots = np.linspace(-3, 3, n + 2)[1:-1]
        H = np.maximum(xs[:, None] - knots[None], 0)  # one hinge per knot
        A = np.c_[np.ones_like(xs), xs, H]
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        fit = A @ coef
        out[f"knots{n}"] = knots
        out[f"fit{n}"] = fit[::5]
        if n <= 64:
            out[f"parts{n}"] = (H * coef[2:]).T[:, ::5]  # each hinge's contribution
        out[f"base{n}"] = (coef[0] + coef[1] * xs)[::5]
        out[f"err{n}"] = float(np.sqrt(((fit - y) ** 2).mean()))
        errs.append(out[f"err{n}"])
    # the rate: a straight line on log-log axes, fitted over the larger n
    ln, le = np.log(HINGE_NS[3:]), np.log(errs[3:])
    out["slope"] = float(np.polyfit(ln, le, 1)[0])
    out["errs"] = errs
    assert all(b < a for a, b in zip(errs, errs[1:]))  # more hinges never fit worse (nested least squares)
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


SPIRAL_KEEP = (0, 25, 50, 100, 200, 300, 450, 600, 1000, 1500, 2000, 3000)


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
    snaps, keep = {}, SPIRAL_KEEP
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
                snaps[f"prob{step}"] = prob.astype(np.float32)
                snaps[f"regions{step}"] = inv.reshape(len(xs), len(xs)).astype(np.int32)
                snaps[f"nreg{step}"] = int(inv.max() + 1)
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(net(Xt), yt)
        loss.backward()
        opt.step()
        if step % 25 == 0:
            with torch.no_grad():
                curve.append((step, float(loss), float((net(Xt).argmax(1) == yt).float().mean())))
    curve = np.array(curve)
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
    return out


# ---------------------------------------------------------------------------
SNAP_RES = (0, 50, 150, 400, 1500)


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

    out = dict(snap_steps=list(SNAP_RES))
    xs = np.linspace(-3.4, 3.4, 90)
    G = torch.tensor(np.stack(np.meshgrid(xs, xs), -1).reshape(-1, 2), dtype=torch.float32)
    out["xs"] = xs
    for name, kw in (("plain", {}), ("residual", dict(residual=True)), ("residual_norm", dict(residual=True, norm=True))):
        torch.manual_seed(1)
        net = Net(**kw)
        opt = torch.optim.Adam(net.parameters(), lr=1e-3)
        curve, probs, gnorms = [], [], []
        for step in range(1501):
            opt.zero_grad()
            loss = torch.nn.functional.cross_entropy(net(Xt), yt)
            loss.backward()
            if step in SNAP_RES:  # what the net says everywhere, and how much gradient reaches each layer
                with torch.no_grad():
                    probs.append(torch.softmax(net(G), 1)[:, 1].numpy().reshape(len(xs), len(xs)))
                gnorms.append([float(lay.weight.grad.norm()) for lay in net.layers])
            opt.step()
            if step % 20 == 0:
                with torch.no_grad():
                    curve.append((step, float(loss), float((net(Xt).argmax(1) == yt).float().mean())))
        out[name] = np.array(curve)
        out[f"probs_{name}"], out[f"gnorm_{name}"] = np.array(probs), np.array(gnorms)
    return out


# ---------------------------------------------------------------------------
def compute_kn():
    """Part 7's Kneser-Ney rows, computed here with Part 7's own functions (its cache isn't needed)."""
    from videos.ai.ai7 import compute as c7

    return c7.compute_kn()


N_CTX, EMB, HID = 24, 32, 1024
LM_STEPS, LM_BATCH = 24000, 512
LM_SNAPS = (100, 300, 1000, 2000, 4000, 8000, 16000, 24000)
LM_PROMPT = "Spade sat down in the armchair, and "


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

    def sample(prompt, seed, n=160):
        with torch.no_grad():
            gen = torch.Generator().manual_seed(seed)
            ctx = list(enc(" " * N_CTX + prompt).numpy())  # padded on the left, so a short prompt fills the window
            outc = []
            for _ in range(n):
                z = logits(torch.tensor([ctx[-N_CTX:]]))[0]
                c = int(torch.multinomial(torch.softmax(z, 0), 1, generator=gen))
                ctx.append(c)
                outc.append(chars[c])
            return "".join(outc)

    steps, batch = LM_STEPS, LM_BATCH
    saved = CACHE.dir / "lm.pt"  # the trained weights, kept so the analysis below can be rerun without retraining
    config = dict(n_ctx=N_CTX, emb=EMB, hid=HID, steps=steps, batch=batch, K=K, snaps=list(LM_SNAPS))
    state = torch.load(saved) if saved.exists() else None
    if state is not None and state["config"] == config:
        for p_, v_ in zip(params, state["params"]):
            p_.data.copy_(v_)
        curve, snaps = state["curve"], state["snaps"]
        print("    reusing the trained weights in", saved, flush=True)
    else:
        opt = torch.optim.Adam(params, lr=2e-3)
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-3, total_steps=steps, pct_start=0.05)
        g = rng(2003)
        curve, snaps = [(0, bits(va, 50_000), bits(ps))], [(0, bits(ps), sample(LM_PROMPT, 1, 120))]
        for step in range(1, steps + 1):
            pos = torch.tensor(g.integers(N_CTX, len(tr), batch))
            loss = torch.nn.functional.cross_entropy(logits(windows(tr, pos)), tr[pos])
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            if step % 1000 == 0 or step in (100, 300, 500):
                curve.append((step, bits(va, 50_000), bits(ps)))
                print(f"    step {step}: valid {curve[-1][1]:.3f}  passage {curve[-1][2]:.3f}", flush=True)
            if step in LM_SNAPS:  # what it writes at this moment of training: same prompt, same random draws
                snaps.append((step, bits(ps), sample(LM_PROMPT, 1, 120)))
        CACHE.dir.mkdir(parents=True, exist_ok=True)
        torch.save(dict(config=config, params=[p_.detach().clone() for p_ in params], curve=curve, snaps=snaps), saved)
    passage_bits = bits(ps)
    valid_bits = bits(va)
    # the vectors the output layer scores each character with (their directions), for the letters, digits and common
    # punctuation, in 2D (PCA); the output vectors group far more cleanly than the input table
    E = outl.weight.detach().numpy()
    E = E / np.linalg.norm(E, axis=1, keepdims=True)
    show = [i for i, c in enumerate(chars) if c.isascii() and (c.isalnum() or c in " .,;:!?'\"-")]  # rare symbols left out
    Es = E[show] - E[show].mean(0)
    u, s, vt = np.linalg.svd(Es, full_matrices=False)
    xy = Es @ vt[:2].T
    samples = [[p, sample(p, sd)] for sd, p in ((1, LM_PROMPT), (2, "It was the best of times, "),
                                                (3, "The telephone rang. "), (4, "\"I don't know,\" he said. "))]
    # Bengio et al.'s best results mixed the network with a smoothed n-gram model: here, Part 7's Kneser-Ney
    from videos.ai.ai7 import compute as c7

    kn = load("kn")
    M = int(kn["best"])
    assert kn["K"] == K
    model = c7.kn_model(c7.ngram_tables(tr.numpy(), K, M), K, M)

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
        return c7.kn_probs(model, a, K, M)[N_CTX - M:]  # aligned with the network's positions

    pv_nn, pv_kn = nn_probs(va, 200_000), kn_probs(va, 200_000)
    pp_nn, pp_kn = nn_probs(ps), kn_probs(ps)
    lams = np.linspace(0, 1, 101)
    vb = [float(-np.log2(l_ * pv_nn + (1 - l_) * pv_kn).mean()) for l_ in lams]
    lam = float(lams[int(np.argmin(vb))])  # the mixing weight, chosen on held-out text, never on the passage
    mix_bits = float(-np.log2(lam * pp_nn + (1 - lam) * pp_kn).mean())
    kn_alone = float(-np.log2(pp_kn).mean())
    assert abs(kn_alone - kn["best_bits"]) < 0.02, (kn_alone, kn["best_bits"])  # the same model as Part 7's
    # where on the passage the two models disagree most: the network's and KN's bits, character by character
    nn_b, kn_b = -np.log2(pp_nn), -np.log2(pp_kn)
    return dict(K=K, n_ctx=N_CTX, emb=EMB, hid=HID, n_params=int(n_params), steps=steps, batch=batch,
                curve=np.array(curve), passage_bits=passage_bits, valid_bits=valid_bits, chars=[chars[i] for i in show],
                xy=xy, xy_chars=[chars[i] for i in show], samples=samples, kn=kn["best_bits"], kn_order=M, lam=lam,
                mix_bits=mix_bits, lam_curve=np.array(vb), snaps=[[int(s), float(b), t] for s, b, t in snaps],
                prompt=LM_PROMPT, nn_wins=float((nn_b < kn_b).mean()), positions=int(steps * batch),
                train_chars=int(len(tr)))


# ---------------------------------------------------------------------------
# The perceptron (Rosenblatt 1958) and Novikoff's bound (1962)
# ---------------------------------------------------------------------------
def separable(n, margin, seed, angle=0.6, offset=0.25):
    """n points in [-2, 2]^2 labelled by a line, none closer to it than ``margin``."""
    g = rng(seed)
    u = np.array([math.cos(angle), math.sin(angle)])
    X = []
    while len(X) < n:
        p = g.uniform(-2, 2, 2)
        if abs(p @ u - offset) >= margin:
            X.append(p)
    X = np.array(X)
    return X, np.where(X @ u - offset > 0, 1, -1)


def aug(X):
    return np.c_[X, np.ones(len(X))]  # a constant input: the bias is one more weight


def perceptron(X, y, order_seed=0, max_epochs=1000):
    """Rosenblatt's rule on the augmented inputs: on a mistake, w <- w + y x. Returns the weights after every
    update, which point caused it, and the mistakes in each pass through the data."""
    Xa = aug(X)
    w = np.zeros(3)
    ws, who, per_epoch = [w.copy()], [], []
    g = rng(order_seed)
    for _ in range(max_epochs):
        m = 0
        for i in g.permutation(len(X)):
            if y[i] * (w @ Xa[i]) <= 0:
                w = w + y[i] * Xa[i]
                ws.append(w.copy())
                who.append(int(i))
                m += 1
        per_epoch.append(m)
        if m == 0:
            break
    return np.array(ws), who, per_epoch


def max_margin(X, y):
    """The best separator through the origin of the augmented space, w* with |w*| = 1, and its margin gamma."""
    from scipy.optimize import minimize

    Xa = aug(X) * y[:, None]
    w0 = perceptron(X, y)[0][-1]
    w0 = w0 / max((Xa @ w0).min(), 1e-9)
    res = minimize(lambda w: 0.5 * w @ w, w0, jac=lambda w: w, method="SLSQP",
                   constraints=[{"type": "ineq", "fun": lambda w: Xa @ w - 1, "jac": lambda w: Xa}],
                   options=dict(maxiter=500, ftol=1e-12))
    w = res.x
    gamma = 1 / np.linalg.norm(w)
    return w * gamma, float(gamma)


def compute_perceptron():
    X, y = separable(50, 0.1, seed=1958)
    ws, who, per_epoch = perceptron(X, y, order_seed=0)
    R = float(np.linalg.norm(aug(X), axis=1).max())
    wstar, gamma = max_margin(X, y)
    k = len(who)
    assert k <= (R / gamma) ** 2 + 1e-9  # Novikoff's theorem: an invariant, not a hope
    # the bound against reality as the margin shrinks: 20 orders of the data each
    sweep = []
    for j, m in enumerate((0.4, 0.2, 0.1, 0.05, 0.025, 0.0125)):
        Xm, ym = separable(200, m, seed=100 + j)
        _, gm = max_margin(Xm, ym)
        Rm = float(np.linalg.norm(aug(Xm), axis=1).max())
        ks = [len(perceptron(Xm, ym, order_seed=s)[1]) for s in range(20)]
        sweep.append((m, gm, Rm, float(np.mean(ks)), float(np.max(ks)), (Rm / gm) ** 2))
        assert max(ks) <= (Rm / gm) ** 2 + 1e-9
    # XOR: no line separates it, and the perceptron never settles
    Xx = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, 0.0]])
    yx = np.array([-1, -1, 1, 1])
    _, _, xor_epochs = perceptron(Xx, yx, max_epochs=40)
    return dict(X=X, y=y, ws=ws, who=who, per_epoch=per_epoch, R=R, gamma=gamma, wstar=wstar, mistakes=k,
                bound=(R / gamma) ** 2, epochs=len(per_epoch), sweep=np.array(sweep), xor_epochs=xor_epochs)


# ---------------------------------------------------------------------------
# XOR with a hidden layer, trained by the series' own autodiff (Part 4); backpropagation checked
# ---------------------------------------------------------------------------
XOR_X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
XOR_Y = np.array([0.0, 1.0, 1.0, 0.0])


def xor_init(seed):
    g = rng(seed)
    return dict(W1=g.normal(0, 1.0, (2, 2)), b1=g.normal(0, 0.5, 2), W2=g.normal(0, 1.0, (2, 1)), b2=np.zeros(1))


def xor_forward_np(p, X):
    z1 = X @ p["W1"] + p["b1"]
    h = np.tanh(z1)
    z2 = (h @ p["W2"])[:, 0] + p["b2"][0]
    return z1, h, z2, 1 / (1 + np.exp(-z2))


def xor_loss_np(p, X=XOR_X, y=XOR_Y):
    *_, q = xor_forward_np(p, X)
    q = np.clip(q, 1e-12, 1 - 1e-12)
    return float(-(y * np.log(q) + (1 - y) * np.log(1 - q)).mean())


def xor_backprop_np(p, X=XOR_X, y=XOR_Y):
    """Backpropagation by hand: the delta equations of the chapter, for tanh hidden units and a sigmoid output with
    cross-entropy (whose delta at the output is simply q - y)."""
    z1, h, z2, q = xor_forward_np(p, X)
    n = len(X)
    d2 = (q - y) / n                          # dL/dz2
    d1 = np.outer(d2, p["W2"][:, 0]) * (1 - h ** 2)  # dL/dz1 = W2^T d2 (.) tanh'(z1)
    return dict(W1=X.T @ d1, b1=d1.sum(0), W2=(h.T @ d2)[:, None], b2=np.array([d2.sum()]))


def xor_autodiff(p, X=XOR_X, y=XOR_Y):
    from explainer.ai.autodiff import Tensor

    T = {k: Tensor(v, requires_grad=True) for k, v in p.items()}
    h = (Tensor(X) @ T["W1"] + T["b1"]).tanh()
    z2 = h @ T["W2"] + T["b2"]  # (4, 1)
    q = (1 + (-z2).exp()) ** -1
    yy = Tensor(y[:, None])
    loss = -(yy * q.log() + (1 - yy) * (1 - q).log()).mean()
    loss.backward()
    return float(loss.data), {k: T[k].grad.copy() for k in p}


def compute_xor():
    # the gradient three ways, at a random point: our autodiff, the delta equations, finite differences
    p = xor_init(7)
    _, g_ad = xor_autodiff(p)
    g_bp = xor_backprop_np(p)
    g_fd = {}
    eps = 1e-6
    for k, v in p.items():
        g_fd[k] = np.zeros_like(v)
        for idx in np.ndindex(v.shape):
            a = {kk: vv.copy() for kk, vv in p.items()}
            b = {kk: vv.copy() for kk, vv in p.items()}
            a[k][idx] += eps
            b[k][idx] -= eps
            g_fd[k][idx] = (xor_loss_np(a) - xor_loss_np(b)) / (2 * eps)
    flat = lambda g: np.concatenate([g[k].ravel() for k in p])  # noqa: E731
    err_bp = float(np.abs(flat(g_ad) - flat(g_bp)).max())
    err_fd = float(np.abs(flat(g_ad) - flat(g_fd)).max() / np.abs(flat(g_fd)).max())
    assert err_bp < 1e-12 and err_fd < 1e-6
    # train from 20 random starts by gradient descent; how many solve it
    lr, steps = 1.0, 3000

    def train(seed, keep=()):
        p = xor_init(seed)
        losses, snaps = [], []
        for t in range(steps + 1):
            loss, g = xor_autodiff(p)
            losses.append(loss)
            if t in keep:
                snaps.append({k: v.copy() for k, v in p.items()})
            for k in p:
                p[k] = p[k] - lr * g[k]
        q = xor_forward_np(p, XOR_X)[3]
        return np.array(losses), snaps, bool(((q > 0.5) == (XOR_Y > 0.5)).all())

    results = [train(s) for s in range(20)]
    solved = [s for s, r in enumerate(results) if r[2]]
    keep = (0, 50, 100, 200, 300, 400, 600, 800, 1200, 2000, 3000)
    seed = solved[0]
    losses, snaps, _ = train(seed, keep)
    # each snapshot: the output over the input square, the hidden layer's image of a grid, and of the four points
    xs = np.linspace(-0.5, 1.5, 81)
    G = np.stack(np.meshgrid(xs, xs), -1).reshape(-1, 2)
    lines = np.linspace(-0.5, 1.5, 9)
    tt = np.linspace(-0.5, 1.5, 41)
    grid_lines = [np.c_[np.full_like(tt, c), tt] for c in lines] + [np.c_[tt, np.full_like(tt, c)] for c in lines]
    out = dict(keep=list(keep), losses=losses, seed=seed, solved=len(solved), starts=len(results), xs=xs,
               err_bp=err_bp, err_fd=err_fd, lr=lr, steps=steps, g_ad=flat(g_ad), g_bp=flat(g_bp), g_fd=flat(g_fd),
               stuck_losses=np.array([r[0][-1] for r in results]))
    for t, sp in zip(keep, snaps):
        out[f"q{t}"] = xor_forward_np(sp, G)[3].reshape(len(xs), len(xs))
        out[f"h{t}"] = np.tanh(XOR_X @ sp["W1"] + sp["b1"])
        out[f"grid{t}"] = np.array([np.tanh(L @ sp["W1"] + sp["b1"]) for L in grid_lines])
        out[f"w2_{t}"] = np.r_[sp["W2"][:, 0], sp["b2"]]
    return out


# ---------------------------------------------------------------------------
# Barron (1993): a dimension-free rate, against a grid's curse of dimensionality
# ---------------------------------------------------------------------------
def compute_barron():
    """f(x) = exp(-|x|^2 / (2 s^2)) on the cube [-1, 1]^d, with s^2 = d / 3 so that |x|/s is about 1 in every
    dimension. f is exactly an average of cosine units: f(x) = E[cos(w . x)], w ~ N(0, I / s^2) (the Gaussian's
    characteristic function). Draw n units at random and average them (Maurey's argument): the error, against n.
    And a table on a grid (multilinear interpolation, which in 1D is exactly a layer of ReLU hinges), against its
    number of points."""
    from scipy.interpolate import RegularGridInterpolator

    g = rng(1993)  # Barron, 1993
    out = {}
    ns = [4, 16, 64, 256, 1024, 4096, 16384]
    for d in (1, 4, 16, 64):
        s2 = d / 3
        Xt = g.uniform(-1, 1, (2000, d))
        f = np.exp(-(Xt ** 2).sum(1) / (2 * s2))
        errs = []
        for n in ns:
            e = []
            for _ in range(4):
                W = g.normal(0, 1 / math.sqrt(s2), (n, d))
                fn = np.cos(Xt @ W.T).mean(1)
                e.append(np.sqrt(((fn - f) ** 2).mean()))
            errs.append(float(np.mean(e)))
        out[f"mc{d}"] = errs
        out[f"fstd{d}"] = float(f.std())
    out["mc_n"] = ns
    grids = {1: [4, 16, 64, 256, 1024, 4096, 16384], 2: [2, 4, 8, 16, 32, 64, 128], 4: [2, 3, 4, 6, 8, 11],
             8: [2, 3, 4]}
    for d, ms in grids.items():
        s2 = d / 3
        Xt = g.uniform(-1, 1, (2000, d))
        f = np.exp(-(Xt ** 2).sum(1) / (2 * s2))
        errs, npts = [], []
        for m in ms:
            ax = np.linspace(-1, 1, m)
            mesh = np.meshgrid(*([ax] * d), indexing="ij")
            vals = np.exp(-sum(c ** 2 for c in mesh) / (2 * s2))
            fn = RegularGridInterpolator([ax] * d, vals)(Xt)
            errs.append(float(np.sqrt(((fn - f) ** 2).mean())))
            npts.append(m ** d)
        out[f"grid{d}"], out[f"grid_n{d}"] = errs, npts
    # the slopes on log-log axes: -1/2 for the random units in every d; about -2/d for the grid
    out["mc_slope"] = {d: float(np.polyfit(np.log(ns), np.log(out[f"mc{d}"]), 1)[0]) for d in (1, 4, 16, 64)}
    out["grid_slope"] = {d: float(np.polyfit(np.log(out[f"grid_n{d}"][-3:]), np.log(out[f"grid{d}"][-3:]), 1)[0])
                         for d in grids}
    return out


# ---------------------------------------------------------------------------
# Folding the plane, and counting pieces
# ---------------------------------------------------------------------------
N_FOLDS = 5


def fold_map(P, k):
    """k folds of the square [-1, 1]^2, alternately along x and y; each is one ReLU layer:
    t -> 2|t| - 1 = 2 relu(t) + 2 relu(-t) - 1, a fold followed by a stretch back to [-1, 1]."""
    P = P.copy()
    pats = []
    for i in range(k):
        j = i % 2
        pats.append(P[:, j] > 0)
        P[:, j] = 2 * np.abs(P[:, j]) - 1
    return P, pats


def compute_fold():
    xs = np.linspace(-1, 1, 512, endpoint=False) + 1 / 512
    P = np.stack(np.meshgrid(xs, xs), -1).reshape(-1, 2)
    out = dict(xs=xs, n_folds=N_FOLDS)
    cells = []
    for k in range(N_FOLDS + 1):
        Q, pats = fold_map(P, k)
        n = len(np.unique(np.stack(pats, 1), axis=0)) if pats else 1  # activation patterns = linear pieces
        cells.append(n)
        out[f"fold{k}"] = Q.reshape(len(xs), len(xs), 2).astype(np.float32)  # where each input point lands
    assert cells == [2 ** k for k in range(N_FOLDS + 1)]
    out["cells"] = cells
    # one hidden layer of n random ReLUs in the plane: n lines in general position cut the whole plane into
    # 1 + n + n(n-1)/2 pieces (Zaslavsky); counted directly, on a box that holds every crossing
    g = rng(1975)
    counts = []
    for n in (1, 2, 3, 4, 5, 6):
        W, b = g.normal(size=(n, 2)), g.normal(size=n) * 0.5
        pts = [np.linalg.solve(np.array([W[i], W[j]]), -np.array([b[i], b[j]])) for i in range(n)
               for j in range(i + 1, n)]
        r = 1.5 * max([np.abs(p_).max() for p_ in pts] + [1.0])
        zs = np.linspace(-r, r, 1501)
        Z = np.stack(np.meshgrid(zs, zs), -1).reshape(-1, 2)
        _, inv = np.unique(Z @ W.T + b > 0, axis=0, return_inverse=True)
        counts.append((n, int(inv.max() + 1), 1 + n + n * (n - 1) // 2))
    out["one_layer"] = np.array(counts)
    return out


# ---------------------------------------------------------------------------
# Histograms through depth (the ridge plot), and vanishing gradients in a 1990s network
# ---------------------------------------------------------------------------
def compute_ridge():
    g = rng(2010)  # Glorot & Bengio, 2010
    L, n, batch = 50, 256, 1024
    x0 = g.normal(size=(batch, n))
    out = dict(L=L, n=n)
    cases = {  # name: (activation, variance of each weight times n)
        "tanh_std": ("tanh", 1 / 3),     # the "standard" heuristic U[-1/sqrt(n), 1/sqrt(n)]: Var = 1/(3n)
        "tanh_xavier": ("tanh", 1.0),    # Glorot & Bengio with n_in = n_out: Var = 1/n
        "tanh_big": ("tanh", 4.0),
        "sigmoid_std": ("sigmoid", 1 / 3),
        "relu_he": ("relu", 2.0),
    }
    edges = np.linspace(-1, 1, 51)
    for name, (act, v) in cases.items():
        h, hists, sds = x0, [], []
        Ws, pre = [], []
        for _ in range(L):
            W = g.normal(size=(n, n)) * math.sqrt(v / n)
            Ws.append(W)
            z = h @ W
            pre.append(z)
            h = np.tanh(z) if act == "tanh" else (1 / (1 + np.exp(-z)) if act == "sigmoid" else np.maximum(z, 0))
            sds.append(float(h.std()))
            if act == "relu":
                hists.append(np.histogram(z.ravel() / z.std(), bins=50, range=(-4, 4))[0])
            else:
                hists.append(np.histogram(h.ravel() if act == "tanh" else 2 * h.ravel() - 1, bins=edges)[0])
        gr, gsd = g.normal(size=(batch, n)), []
        for W, z in zip(Ws[::-1], pre[::-1]):
            if act == "tanh":
                d = 1 - np.tanh(z) ** 2
            elif act == "sigmoid":
                s = 1 / (1 + np.exp(-z))
                d = s * (1 - s)
            else:
                d = (z > 0).astype(float)
            gr = (gr * d) @ W.T
            gsd.append(float(np.sqrt((gr ** 2).mean())))
        H = np.array(hists, float)
        out[f"hist_{name}"] = H / H.sum(1, keepdims=True)
        out[f"sd_{name}"] = np.array(sds)
        out[f"gsd_{name}"] = np.array(gsd[::-1])  # by layer, first to last
    return out


# ---------------------------------------------------------------------------
# Mean-field signal propagation (Poole et al. 2016; Schoenholz et al. 2017), for tanh
# ---------------------------------------------------------------------------
GH_Z, GH_W = np.polynomial.hermite_e.hermegauss(81)
GH_W = GH_W / GH_W.sum()  # expectations over z ~ N(0, 1)


def mf_qmap(q, sw2, sb2, phi=np.tanh):
    return sw2 * (GH_W * phi(np.sqrt(q) * GH_Z) ** 2).sum() + sb2


def mf_qstar(sw2, sb2):
    q = 1.0
    for _ in range(5000):
        q2 = mf_qmap(q, sw2, sb2)
        if abs(q2 - q) < 1e-13:
            return q2
        q = q2
    return q


def mf_chi1(sw2, sb2):
    q = mf_qstar(sw2, sb2)
    return sw2 * (GH_W * (1 - np.tanh(np.sqrt(q) * GH_Z) ** 2) ** 2).sum()


def mf_cmap(c, q, sw2, sb2):
    """The correlation of two inputs after one more layer, both of length q (at the fixed point)."""
    z1, z2 = np.meshgrid(GH_Z, GH_Z, indexing="ij")
    w = np.outer(GH_W, GH_W)
    u1 = np.sqrt(q) * z1
    u2 = np.sqrt(q) * (c * z1 + np.sqrt(max(1 - c * c, 0)) * z2)
    return (sw2 * (w * np.tanh(u1) * np.tanh(u2)).sum() + sb2) / q


def compute_meanfield():
    sb2 = 0.05
    out = dict(sb2=sb2)
    # the phase diagram: chi_1 over (sigma_w^2, sigma_b^2)
    sw = np.linspace(0.5, 4.0, 71)
    sb = np.linspace(0.0, 0.5, 51)
    chi = np.array([[mf_chi1(a, b) for a in sw] for b in sb])
    out.update(phase_sw=sw, phase_sb=sb, phase_chi=chi)
    crit = []
    for b in sb:  # where chi_1 crosses 1
        c = np.array([mf_chi1(a, b) for a in sw]) - 1
        k = int(np.argmax(c > 0))
        lo, hi = sw[k - 1], sw[k]
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if mf_chi1(mid, b) < 1 else (lo, mid)
        crit.append((lo + hi) / 2)
    out["crit_sw"] = np.array(crit)
    sw_c = float(np.interp(sb2, sb, crit))
    out["sw_crit"] = sw_c
    # three settings: ordered, critical, chaotic
    sets = {"ordered": 1.0, "critical": sw_c, "chaotic": 3.0}
    out["sets"] = sets
    qs = np.linspace(0, 3, 121)
    cs = np.linspace(0, 1, 101)
    for name, a in sets.items():
        qstar = mf_qstar(a, sb2)
        out[f"qmap_{name}"] = np.array([mf_qmap(q, a, sb2) for q in qs])
        out[f"qstar_{name}"] = qstar
        out[f"cmap_{name}"] = np.array([mf_cmap(c, qstar, a, sb2) for c in cs])
        out[f"chi_{name}"] = mf_chi1(a, sb2)
        c, traj = 0.6, [0.6]
        for _ in range(60):
            c = mf_cmap(c, qstar, a, sb2)
            traj.append(c)
        out[f"ctraj_{name}"] = np.array(traj)
    out.update(qs=qs, cs=cs)
    # a real network of width 1,000: two inputs, their correlation layer by layer
    g = rng(2016)
    n, L = 1000, 60
    for name, a in sets.items():
        qstar = out[f"qstar_{name}"]
        u = g.normal(size=n)
        v = g.normal(size=n)
        x1 = u / np.linalg.norm(u)
        v = v - (v @ x1) * x1
        x2 = 0.6 * x1 + 0.8 * v / np.linalg.norm(v)
        z = np.stack([x1, x2]) * math.sqrt(qstar * n)  # pre-activations of length q* each, correlation 0.6
        cor = [float(z[0] @ z[1] / np.linalg.norm(z[0]) / np.linalg.norm(z[1]))]
        for _ in range(L):
            W = g.normal(size=(n, n)) * math.sqrt(a / n)
            b = g.normal(size=n) * math.sqrt(sb2)
            z = np.tanh(z) @ W + b
            cor.append(float(z[0] @ z[1] / np.linalg.norm(z[0]) / np.linalg.norm(z[1])))
        out[f"csim_{name}"] = np.array(cor)
    # the depth scale xi_c = -1 / log chi_c over sigma_w^2 (chi_c: the c-map's slope at its fixed point)
    sws = np.linspace(0.6, 4.0, 69)
    xi = []
    for a in sws:
        qstar = mf_qstar(a, sb2)
        c = 0.5
        for _ in range(3000):
            c2 = mf_cmap(c, qstar, a, sb2)
            if abs(c2 - c) < 1e-12:
                c = c2
                break
            c = c2
        if c > 0.999:
            chi_c = mf_chi1(a, sb2)
        else:
            h = 1e-4
            chi_c = (mf_cmap(c + h, qstar, a, sb2) - mf_cmap(c - h, qstar, a, sb2)) / (2 * h)
        xi.append(-1 / math.log(min(chi_c, 1 - 1e-9)) if chi_c < 1 else float("inf"))
    out["xi_sw"], out["xi"] = sws, np.array(xi)
    return out


def compute_trainable():
    """Which (sigma_w^2, depth) can be trained: tanh networks of width 64 fitting a 10-class task (Gaussian clusters in
    32 dimensions), 300 steps of RMSProp each (as Schoenholz et al. trained theirs), training accuracy at the end."""
    import torch

    torch.set_num_threads(2)
    mf = load("meanfield")
    sb2 = float(mf["sb2"])
    g = rng(2017)
    K, D, N = 10, 32, 2048
    centres = g.normal(size=(K, D))
    lab = g.integers(0, K, N)
    X = centres[lab] + 1.2 * g.normal(size=(N, D))
    Xt = torch.tensor(X / X.std(), dtype=torch.float32)
    yt = torch.tensor(lab)
    sws = np.round(np.linspace(0.6, 4.0, 12), 3)
    depths = [5, 10, 20, 35, 50, 70, 100]
    acc = np.zeros((len(depths), len(sws)))
    width, steps = 64, 300
    for i, L in enumerate(depths):
        for j, a in enumerate(sws):
            torch.manual_seed(1000 * i + j)
            layers = [torch.nn.Linear(D, width)] + [torch.nn.Linear(width, width) for _ in range(L - 1)]
            for lay in layers:
                torch.nn.init.normal_(lay.weight, std=math.sqrt(a / lay.in_features))
                torch.nn.init.normal_(lay.bias, std=math.sqrt(sb2))
            head = torch.nn.Linear(width, K)
            params = [p for lay in layers for p in lay.parameters()] + list(head.parameters())
            opt = torch.optim.RMSprop(params, lr=1e-3)

            def fwd(x):
                for lay in layers:
                    x = torch.tanh(lay(x))
                return head(x)

            for _ in range(steps):
                idx = torch.randint(0, N, (128,))
                loss = torch.nn.functional.cross_entropy(fwd(Xt[idx]), yt[idx])
                opt.zero_grad()
                loss.backward()
                opt.step()
            with torch.no_grad():
                acc[i, j] = float((fwd(Xt).argmax(1) == yt).float().mean())
            print(f"    depth {L:3d}  sigma_w^2 {a:.2f}: {acc[i, j]:.2f}", flush=True)
    xi = np.interp(sws, mf["xi_sw"], np.minimum(mf["xi"], 1e6))
    return dict(sws=sws, depths=depths, acc=acc, xi=xi, width=width, steps=steps, classes=K, dim=D, n=N)


# ---------------------------------------------------------------------------
# Normalization: Jacobians, measured
# ---------------------------------------------------------------------------
def compute_norms():
    import torch

    torch.manual_seed(2016)
    d = 16
    h = torch.randn(d) * 2.0 + 0.7
    ln = lambda v: torch.nn.functional.layer_norm(v, (d,), eps=0.0)  # noqa: E731
    rms = lambda v: v / v.pow(2).mean().sqrt()  # noqa: E731
    J_ln = torch.autograd.functional.jacobian(ln, h).numpy()
    J_rms = torch.autograd.functional.jacobian(rms, h).numpy()
    hn = h.numpy().astype(float)
    sig = hn.std()
    c = hn - hn.mean()
    one = np.ones(d) / math.sqrt(d)
    u = c / np.linalg.norm(c)
    J_ln_formula = (np.eye(d) - np.outer(one, one) - np.outer(u, u)) / sig
    r = math.sqrt((hn ** 2).mean())
    v = hn / np.linalg.norm(hn)
    J_rms_formula = (np.eye(d) - np.outer(v, v)) / r
    err = max(np.abs(J_ln - J_ln_formula).max(), np.abs(J_rms - J_rms_formula).max())
    assert err < 1e-4, err
    sv_ln = np.sort(np.linalg.svd(J_ln, compute_uv=False))[::-1]
    sv_rms = np.sort(np.linalg.svd(J_rms, compute_uv=False))[::-1]
    # scale invariance: the same output for 2h, and half the Jacobian
    scale = [(float(a_), float(np.abs(ln(a_ * h) - ln(h)).max()),
              float(np.linalg.norm(torch.autograd.functional.jacobian(ln, a_ * h).numpy(), 2)))
             for a_ in (0.5, 1.0, 2.0, 4.0)]
    return dict(d=d, h=hn, sv_ln=sv_ln, sv_rms=sv_rms, sigma=float(sig), rms=r, err=float(err), scale=np.array(scale),
                radial=float(np.abs(J_rms_formula @ hn).max()))


# ---------------------------------------------------------------------------
# The modern block, assembled piece by piece: a deep MLP language model on the novels
# ---------------------------------------------------------------------------
BLK_CTX, BLK_EMB, BLK_D, BLK_DEPTH, BLK_STEPS, BLK_BATCH, BLK_LR = 16, 16, 64, 24, 1200, 128, 3e-3
BLOCK_VARIANTS = ("plain", "residual", "post_ln", "pre_ln", "pre_rms", "pre_rms_swiglu")


def compute_block():
    import torch

    from videos.ai.ai1 import compute as c1

    torch.set_num_threads(2)
    texts = {k: c1.text(k) for k in ("train", "valid")}
    chars = sorted(set(c1.text("train") + c1.text("valid") + c1.text("passage")))
    K = len(chars)
    cp = np.array([ord(c) for c in chars])
    order = np.argsort(cp)

    def enc(t):
        a = np.frombuffer(t.encode("utf-32-le"), dtype=np.uint32)
        return torch.tensor(order[np.searchsorted(cp[order], a)])

    tr, va = enc(texts["train"]), enc(texts["valid"])
    d, hid = BLK_D, 4 * BLK_D
    hid_glu = round(2 * hid / 3)  # three matrices instead of two: the same number of weights

    class RMSNorm(torch.nn.Module):
        def __init__(self, n):
            super().__init__()
            self.g = torch.nn.Parameter(torch.ones(n))

        def forward(self, x):
            return self.g * x / x.pow(2).mean(-1, keepdim=True).add(1e-6).sqrt()

    class Block(torch.nn.Module):
        def __init__(self, kind):
            super().__init__()
            self.kind = kind
            if kind.endswith("swiglu"):
                self.w1, self.w3 = torch.nn.Linear(d, hid_glu, bias=False), torch.nn.Linear(d, hid_glu, bias=False)
                self.w2 = torch.nn.Linear(hid_glu, d, bias=False)
            else:
                self.w1, self.w2 = torch.nn.Linear(d, hid), torch.nn.Linear(hid, d)
            self.norm = (RMSNorm(d) if "rms" in kind else torch.nn.LayerNorm(d) if "ln" in kind else torch.nn.Identity())

        def mlp(self, x):
            if self.kind.endswith("swiglu"):
                return self.w2(torch.nn.functional.silu(self.w1(x)) * self.w3(x))
            return self.w2(torch.relu(self.w1(x)))

        def forward(self, h):
            k = self.kind
            if k == "plain":
                return self.mlp(h)
            if k == "residual":
                return h + self.mlp(h)
            if k == "post_ln":
                return self.norm(h + self.mlp(h))
            return h + self.mlp(self.norm(h))  # pre-norm

    class Net(torch.nn.Module):
        def __init__(self, kind):
            super().__init__()
            self.emb = torch.nn.Embedding(K, BLK_EMB)
            self.inp = torch.nn.Linear(BLK_CTX * BLK_EMB, d)
            self.blocks = torch.nn.ModuleList([Block(kind) for _ in range(BLK_DEPTH)])
            self.final = (RMSNorm(d) if "rms" in kind else torch.nn.LayerNorm(d) if kind == "pre_ln" else
                          torch.nn.Identity())
            self.out = torch.nn.Linear(d, K)

        def forward(self, ctx):
            h = self.inp(self.emb(ctx).reshape(len(ctx), -1))
            for b in self.blocks:
                h = b(h)
            return self.out(self.final(h))

    def windows(seq, pos):
        return torch.stack([seq[pos - BLK_CTX + j] for j in range(BLK_CTX)], 1)

    g = rng(9)
    vpos = torch.tensor(g.integers(BLK_CTX, len(va), 20000))
    vctx, vy = windows(va, vpos), va[vpos]
    out = dict(variants=list(BLOCK_VARIANTS), depth=BLK_DEPTH, d=d, hid=hid, hid_glu=hid_glu, steps=BLK_STEPS,
               batch=BLK_BATCH, lr=BLK_LR, ctx=BLK_CTX)
    for kind in BLOCK_VARIANTS:
        torch.manual_seed(24)
        net = Net(kind)
        out[f"params_{kind}"] = int(sum(p.numel() for b in net.blocks for p in b.parameters() if p.dim() > 1))
        opt = torch.optim.Adam(net.parameters(), lr=BLK_LR)
        gr = rng(10)  # the same batches for every variant
        curve, gnorm0 = [], None
        for step in range(BLK_STEPS + 1):
            if step % 100 == 0:
                with torch.no_grad():
                    vb = float(torch.nn.functional.cross_entropy(net(vctx), vy)) / math.log(2)
                curve.append((step, vb if math.isfinite(vb) else float("nan")))
            if step == BLK_STEPS:
                break
            pos = torch.tensor(gr.integers(BLK_CTX, len(tr), BLK_BATCH))
            loss = torch.nn.functional.cross_entropy(net(windows(tr, pos)), tr[pos])
            opt.zero_grad()
            loss.backward()
            if step == 0:  # how much gradient reaches each block at the start
                gnorm0 = [float(torch.sqrt(sum(p.grad.pow(2).sum() for p in b.parameters() if p.dim() > 1)))
                          for b in net.blocks]
            opt.step()
        out[kind] = np.array(curve)
        out[f"gnorm0_{kind}"] = np.array(gnorm0)
        print(f"    {kind}: valid {curve[-1][1]:.3f} bits/char", flush=True)
    return out


# ---------------------------------------------------------------------------
# Published configurations (Hugging Face config.json of each model), and what they imply per block
# ---------------------------------------------------------------------------
CONFIGS = {  # d, MLP width, layers, attention heads, key-value heads, head size, vocabulary, gated MLP?
    "GPT-2 (2019)": dict(d=768, f=3072, layers=12, heads=12, kv=12, hd=64, vocab=50257, gated=False),
    "Llama 2 7B (2023)": dict(d=4096, f=11008, layers=32, heads=32, kv=32, hd=128, vocab=32000, gated=True),
    "Llama 3 8B (2024)": dict(d=4096, f=14336, layers=32, heads=32, kv=8, hd=128, vocab=128256, gated=True),
    "Qwen3-8B (2025)": dict(d=4096, f=12288, layers=36, heads=32, kv=8, hd=128, vocab=151936, gated=True),
}


def compute_configs():
    rows = []
    for name, c in CONFIGS.items():
        d = c["d"]
        attn = d * c["heads"] * c["hd"] + 2 * d * c["kv"] * c["hd"] + c["heads"] * c["hd"] * d
        mlp = (3 if c["gated"] else 2) * d * c["f"]
        rows.append(dict(name=name, **c, attn=attn, mlp=mlp, block=attn + mlp + 2 * d, ratio=c["f"] / d,
                         total=c["layers"] * (attn + mlp + 2 * d) + c["vocab"] * d * (1 if name.startswith("GPT")
                                                                                       else 2)))
    return dict(rows=rows)


# ---------------------------------------------------------------------------
# Kolmogorov-Arnold networks (Liu et al. 2024) against MLPs, on the KAN paper's own example
# ---------------------------------------------------------------------------
def kan_target(x):
    return np.exp(np.sin(np.pi * x[:, 0]) + x[:, 1] ** 2)


def compute_kan():
    import torch

    torch.set_num_threads(1)
    torch.set_default_dtype(torch.float64)
    g = rng(2024)
    Xtr, Xte = g.uniform(-1, 1, (1000, 2)), g.uniform(-1, 1, (1000, 2))
    ytr, yte = kan_target(Xtr), kan_target(Xte)
    Xtr_t, Xte_t = torch.tensor(Xtr), torch.tensor(Xte)
    ytr_t, yte_t = torch.tensor(ytr), torch.tensor(yte)

    class KANLayer(torch.nn.Module):
        """Each edge (i -> j) carries its own function of one variable: a cubic B-spline on G intervals of
        [-1, 1] plus a scaled SiLU, phi(x) = w_b silu(x) + sum_k c_k B_k(x). A node adds what arrives."""

        def __init__(self, n_in, n_out, G, k=3, lo=-1.0, hi=1.0):
            super().__init__()
            h = (hi - lo) / G
            self.grid = torch.arange(-k, G + k + 1) * h + lo  # knots, extended k beyond each end
            self.k = k
            self.coef = torch.nn.Parameter(torch.randn(n_out, n_in, G + k) * 0.1)
            self.wb = torch.nn.Parameter(torch.randn(n_out, n_in) / math.sqrt(n_in))

        def basis(self, x):  # x: (batch, n_in) -> (batch, n_in, G + k)
            t = self.grid
            x = x[..., None]
            B = ((x >= t[:-1]) & (x < t[1:])).to(x.dtype)
            for p in range(1, self.k + 1):
                B = ((x - t[:-(p + 1)]) / (t[p:-1] - t[:-(p + 1)]) * B[..., :-1]
                     + (t[p + 1:] - x) / (t[p + 1:] - t[1:-p]) * B[..., 1:])
            return B

        def edges(self, x):  # each edge's value: (batch, n_out, n_in)
            return (torch.einsum("bik,oik->boi", self.basis(x), self.coef)
                    + self.wb[None] * torch.nn.functional.silu(x)[:, None, :])

        def forward(self, x):
            return self.edges(x).sum(-1)

    class KAN(torch.nn.Module):
        def __init__(self, widths, G):
            super().__init__()
            self.layers = torch.nn.ModuleList([KANLayer(a, b, G) for a, b in zip(widths, widths[1:])])

        def forward(self, x):
            for i, lay in enumerate(self.layers):
                x = lay(x)
                if i < len(self.layers) - 1:
                    x = torch.tanh(x)  # keep the next layer's inputs on its grid, [-1, 1]
            return x[:, 0]

    def mlp(h):
        return torch.nn.Sequential(torch.nn.Linear(2, h), torch.nn.SiLU(), torch.nn.Linear(h, h), torch.nn.SiLU(),
                                   torch.nn.Linear(h, 1))

    def fit(model, steps=3000, snaps=()):
        torch.manual_seed(0)
        opt = torch.optim.Adam(model.parameters(), lr=1e-2)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
        curve, kept = [], []
        for s in range(steps + 1):
            pred = model(Xtr_t).reshape(-1)
            loss = ((pred - ytr_t) ** 2).mean()
            if s % 50 == 0:
                with torch.no_grad():
                    te = float(((model(Xte_t).reshape(-1) - yte_t) ** 2).mean().sqrt())
                curve.append((s, float(loss.sqrt()), te))
            if s in snaps:
                kept.append(edge_functions(model))
            if s == steps:
                break
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
        return np.array(curve), kept

    xs = torch.linspace(-1, 1, 101)

    def edge_functions(model):
        with torch.no_grad():
            first = model.layers[0].edges(torch.stack([xs, xs], 1))  # (101, out, 2)
            second = model.layers[1].edges(torch.stack([xs] * model.layers[1].wb.shape[1], 1))  # (101, 1, hidden)
        return np.concatenate([first.permute(1, 2, 0).reshape(-1, 101).numpy(),
                               second.permute(1, 2, 0).reshape(-1, 101).numpy()])

    n_params = lambda m: int(sum(p.numel() for p in m.parameters()))  # noqa: E731
    out = dict(xs=xs.numpy())
    snaps = (0, 100, 300, 1000, 3000)
    torch.manual_seed(1)
    kan = KAN([2, 5, 1], G=5)
    curve, kept = fit(kan, snaps=snaps)
    out.update(kan_curve=curve, kan_params=n_params(kan), kan_snaps=list(snaps),
               kan_edges=np.array(kept), kan_test=float(curve[-1, 2]))
    # how much the learned curves look like the formula's pieces: |correlation| of each hidden unit's curve of x with
    # sin(pi x), and of its curve of y with y^2
    E = np.array(kept[-1])
    xv = xs.numpy()
    cx = [abs(np.corrcoef(E[2 * j], np.sin(np.pi * xv))[0, 1]) for j in range(5)]
    cy = [abs(np.corrcoef(E[2 * j + 1], xv ** 2)[0, 1]) for j in range(5)]
    out.update(corr_sin=cx, corr_sq=cy)
    rows = []
    for G in (2, 3, 5, 10, 20):
        torch.manual_seed(1)
        m = KAN([2, 5, 1], G=G)
        c, _ = fit(m)
        rows.append(("kan", G, n_params(m), float(c[-1, 2])))
    for h in (4, 7, 10, 16, 28):
        torch.manual_seed(1)
        m = mlp(h)
        c, _ = fit(m)
        rows.append(("mlp", h, n_params(m), float(c[-1, 2])))
    out["table"] = rows
    m = mlp(10)
    torch.manual_seed(1)
    c, _ = fit(m)
    out.update(mlp_curve=c, mlp_params=n_params(m), mlp_test=float(c[-1, 2]), y_std=float(yte.std()))
    torch.set_default_dtype(torch.float32)
    return out


def compute_lm_words():
    """How much of what the language model writes at each checkpoint is made of real words: the share of the
    whitespace-separated words of each sample (punctuation stripped, lower-cased) that occur at least 3 times in the
    training text."""
    import collections
    import re

    from videos.ai.ai1 import compute as c1

    words = re.findall(r"[a-z']+", c1.text("train").lower())
    vocab = {w for w, n in collections.Counter(words).items() if n >= 3}
    lm = load("lm")
    rows = []
    for step, bits, txt in lm["snaps"]:
        toks = [re.sub(r"[^a-z']", "", t.lower()) for t in txt.split()]
        toks = [t for t in toks if t]
        real = sum(t in vocab for t in toks)
        rows.append((int(step), float(bits), len(toks), real, real / max(len(toks), 1)))
    return dict(rows=rows, vocab=len(vocab))


ITEMS = {
    "hinges": compute_hinges,
    "sawtooth": compute_sawtooth,
    "spiral": compute_spiral,
    "signal": compute_signal,
    "residual": compute_residual,
    "kn": compute_kn,
    "lm": compute_lm,
    "perceptron": compute_perceptron,
    "xor": compute_xor,
    "barron": compute_barron,
    "fold": compute_fold,
    "ridge": compute_ridge,
    "meanfield": compute_meanfield,
    "trainable": compute_trainable,
    "norms": compute_norms,
    "block": compute_block,
    "configs": compute_configs,
    "kan": compute_kan,
    "lm_words": compute_lm_words,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
