"""Precompute everything numerical in Part 20 of the AI series ("Inside the Model").

    python -m videos.ai.ai20.compute              # everything missing (Part 11's transformer)
    python -m videos.ai.ai20.compute --force sae

Results are cached in ``.cache/ai20/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    superposition  Elhage et al.'s toy model: 5 features squeezed into 2 dimensions and back (x -> ReLU(W^T W x + b)),
                   trained at several sparsities: dense features get 2 dimensions and the rest are dropped; sparse ones
                   all fit, as a pentagon
    sae            a sparse autoencoder on Part 11's transformer: the vectors of its residual stream after block 2, for
                   200,000 characters of the novels, rewritten as sparse combinations of 512 learned features; how many
                   are active per character, how well they rebuild the vector, and the text where some features fire
    frontier       (frontier.py) the same vectors, taken apart by sparse autoencoders trained with an L1 penalty at four
                   strengths and with TopK at k = 4 to 32: features per vector, variance left, dead features, shrinkage
    steering       adding one feature's direction to the residual stream while the model writes: its text with and
                   without the push
    attribution    an attribution graph for one prediction: which features (and which input characters behind them)
                   raised the score of the character the model writes next
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai20")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_superposition():
    import torch

    torch.set_num_threads(2)
    n, m = 5, 2
    imp = 0.9 ** np.arange(n)  # feature importance, falling
    out = dict(n=n, m=m, importance=imp, sparsities=[0.0, 0.7, 0.9, 0.97])
    for S in out["sparsities"]:
        torch.manual_seed(2022)  # Elhage et al., Toy Models of Superposition
        W = torch.nn.Parameter(torch.randn(m, n) * 0.3)
        b = torch.nn.Parameter(torch.zeros(n))
        opt = torch.optim.Adam([W, b], lr=1e-2)
        I = torch.tensor(imp, dtype=torch.float32)
        g = torch.Generator().manual_seed(0)
        checks = [0, 30, 100, 250, 600, 1500, 3000, 6000]
        snaps, losses = [], []
        for step in range(6000):
            if step in checks:
                snaps.append(W.detach().numpy().copy())
            x = torch.rand(1024, n, generator=g) * (torch.rand(1024, n, generator=g) > S).float()
            xh = torch.relu(x @ W.T @ W + b)
            loss = (I * (xh - x) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            if step % 30 == 0:
                losses.append((step, float(loss)))
        snaps.append(W.detach().numpy().copy())
        out[f"Wtrain{S:g}"], out[f"losses{S:g}"], out["checks"] = np.array(snaps), np.array(losses), checks  # how it learns
        Wn = W.detach().numpy()
        out[f"W{S:g}"] = Wn  # each column: where a feature points in the 2D hidden space
        out[f"b{S:g}"] = b.detach().numpy()
        out[f"norms{S:g}"] = np.linalg.norm(Wn, axis=0)
    dense, sparse = out["norms0"], out["norms0.97"]
    assert (dense > 0.5).sum() <= 3 and (sparse > 0.5).sum() == n  # dense: only a few represented; sparse: all five
    # one feature on, in the sparse model: what reaches each output before and after the bias and the ReLU
    W, b = out["W0.97"], out["b0.97"]
    out["readout"] = W.T @ W[:, 0]
    out["after_relu"] = np.maximum(W.T @ W[:, 0] + b, 0)
    assert out["after_relu"][0] > 0.5 and np.all(out["after_relu"][1:] < 0.25 * out["after_relu"][0])
    # in many dimensions there is room: the cosine between random directions, for growing dimension
    g = rng(1984)  # Johnson & Lindenstrauss
    out["dims"] = [2, 16, 128, 1024]
    edges = np.linspace(-1, 1, 81)
    for d in out["dims"]:
        u, v = g.normal(size=(20000, d)), g.normal(size=(20000, d))
        c = (u * v).sum(1) / np.linalg.norm(u, axis=1) / np.linalg.norm(v, axis=1)
        out[f"cos_hist{d}"] = np.histogram(c, bins=edges)[0] / len(c)
        out[f"cos_std{d}"] = float(c.std())
    out["cos_edges"] = edges
    return out


# ---------------------------------------------------------------------------
def residuals(model, seq, layer, starts, c11):
    """The residual-stream vectors after block ``layer`` (0-based), for windows of the text."""
    import torch

    acts = []
    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)
    T = c11.CTX
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)
    with torch.no_grad():
        for i in range(0, len(starts), 16):
            x = torch.stack([seq[s:s + T] for s in starts[i:i + 16]])
            h = model.emb(x)
            for b in model.blocks[: layer + 1]:
                h, _, _ = b(h, cos, sin)
            acts.append(h[:, 64:].reshape(-1, h.shape[-1]))  # positions with enough context
    return torch.cat(acts)


def mlp_neurons(model, seq, starts, c11):
    """The 512 neurons of block 2's MLP (after the GELU), for windows of the text (positions 64 on)."""
    import torch
    import torch.nn.functional as F

    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)
    T = c11.CTX
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)
    acts = []
    with torch.no_grad():
        for i in range(0, len(starts), 16):
            h = model.emb(torch.stack([seq[s:s + T] for s in starts[i:i + 16]]))
            h, _, _ = model.blocks[0](h, cos, sin)
            b = model.blocks[1]
            a, _, _ = b.attend(h, cos, sin, 1.0, None)
            h = h + b.o(a.transpose(1, 2).reshape(h.shape))
            acts.append(F.gelu(b.f1(b.n2(h)))[:, 64:].reshape(-1, b.f1.out_features))
    return torch.cat(acts)


def compute_sae():
    import torch

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(3)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    va = data["valid"]
    g = rng(2023)  # Bricken et al., Towards Monosemanticity; Cunningham et al., sparse autoencoders
    starts = g.integers(0, len(va) - c11.CTX - 1, 1100)
    A = residuals(model, va, 1, starts, c11)  # (N, D)
    text_ids = torch.cat([torch.stack([va[s:s + c11.CTX] for s in starts[i:i + 16]])[:, 64:].reshape(-1)
                          for i in range(0, len(starts), 16)])
    mu = A.mean(0)
    scale = (A - mu).norm(dim=1).mean()
    X = (A - mu) / scale
    D, F_ = X.shape[1], 512
    torch.manual_seed(0)
    Wd = torch.nn.Parameter(torch.randn(F_, D) / math.sqrt(D))
    We = torch.nn.Parameter(Wd.detach().clone().T)
    be = torch.nn.Parameter(torch.zeros(F_))
    bd = torch.nn.Parameter(torch.zeros(D))
    opt = torch.optim.Adam([Wd, We, be, bd], lr=1e-3)
    lam = 3e-3
    for step in range(6000):
        i = torch.randint(0, len(X), (1024,))
        x = X[i]
        f = torch.relu(x @ We + be)
        dec = Wd / Wd.norm(dim=1, keepdim=True)
        xh = f @ dec + bd
        loss = ((xh - x) ** 2).sum(1).mean() + lam * f.sum(1).mean() * D
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        dec = Wd / Wd.norm(dim=1, keepdim=True)
        f = torch.relu(X @ We + be)
        xh = f @ dec + bd
        l0 = float((f > 0).float().sum(1).mean())
        fvu = float(((xh - X) ** 2).sum(1).mean() / ((X - X.mean(0)) ** 2).sum(1).mean())
        alive = (f > 0).float().mean(0)
        # describe features by the characters where they fire hardest: a window of text around each top activation
        tid = text_ids.numpy()
        T64 = c11.CTX - 64
        feats = []
        order = torch.argsort(alive, descending=True)
        for k in order[: int((alive > 0).sum())].tolist():  # every feature that ever fires, most frequent first
            top = torch.topk(f[:, k], 8).indices.numpy()
            nxt = []
            for p in top:
                w, off = p // T64, p % T64
                s = starts[w] + 64 + off
                ctx = "".join(chars[int(c)] for c in va[s - 24:s + 2])  # ...up to the character, then the next one
                nxt.append(ctx)
            last = [c_[-2] for c_ in nxt]
            purity = max(last.count(c_) for c_ in set(last)) / len(last)
            feats.append(dict(id=int(k), freq=float(alive[k]), contexts=nxt, purity=purity))
        # the same picture for the model's own neurons (block 2's MLP), on a subset of the windows
        N = mlp_neurons(model, va, starts[:300], c11)
        n_pur = []
        for k in range(N.shape[1]):
            top = torch.topk(N[:, k], 8).indices.numpy()
            last = [chars[int(va[starts[p // T64] + 64 + p % T64])] for p in top]
            n_pur.append(max(last.count(c_) for c_ in set(last)) / len(last))
        n_pur = np.array(n_pur)
        med = int(np.argsort(n_pur)[len(n_pur) // 2])  # a neuron of median purity
        top = torch.topk(N[:, med], 8).indices.numpy()
        neuron_ctx = ["".join(chars[int(c)] for c in va[starts[p // T64] + 64 + p % T64 - 24:starts[p // T64] + 64 + p % T64 + 2])
                      for p in top]
        # a stretch of the passage: its residual vectors, and the same as features
        ps = data["passage"]
        s0 = 400
        h = residuals(model, ps, 1, [s0 - 192], c11)[-64:]
        Xd = (h - mu) / scale
        Fd = torch.relu(Xd @ We + be)
        Rd = Fd @ dec + bd
    f_pur = np.array([f_["purity"] for f_ in feats])
    out = dict(D=int(D), F=F_, l0=l0, fvu=fvu, n_vectors=int(len(X)), lam=lam, features=feats,
               dead=int((alive == 0).sum()), mu=mu.numpy(), scale=float(scale), dirs=(dec * scale).numpy(),
               neuron_purity=n_pur, feature_purity=f_pur, neuron=med, neuron_contexts=neuron_ctx,
               demo_text="".join(chars[int(c)] for c in ps[s0:s0 + 64]), demo_resid=Xd.numpy(),
               demo_feats=Fd.numpy(), demo_rec=Rd.numpy())
    print(f"    {len(X)} vectors; {l0:.1f} features active per character; unexplained variance {fvu:.3f}; "
          f"{out['dead']} dead; purity: neurons {n_pur.mean():.2f}, features {f_pur.mean():.2f}", flush=True)
    assert l0 < 0.1 * F_ and fvu < 0.35
    torch.save(dict(We=We.detach(), be=be.detach(), dec=dec, bd=bd.detach(), mu=mu, scale=scale), CACHE.dir / "sae.pt")
    return out


# ---------------------------------------------------------------------------
def compute_steering():
    import torch

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(3)
    s = load("sae")
    model, chars, enc, data = c11.load_tf()
    sae = torch.load(CACHE.dir / "sae.pt")
    # the feature most tied to quotation marks: its top activations sit on a '"'
    best, best_k = -1.0, None
    for f in s["features"]:
        frac = np.mean([c_[-2] == '"' for c_ in f["contexts"]])
        if frac > best:
            best, best_k = frac, f["id"]
    direction = sae["dec"][best_k] * sae["scale"]
    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)

    def generate(prompt, alpha, seed, n=160):
        torch.manual_seed(seed)
        ctx = enc(prompt)
        out = []
        with torch.no_grad():
            for _ in range(n):
                x = ctx[None, -c11.CTX:]
                T = x.shape[1]
                ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
                cos, sin = torch.cos(ang), torch.sin(ang)
                h = model.emb(x)
                for li, b in enumerate(model.blocks):
                    h, _, _ = b(h, cos, sin)
                    if li == 1:
                        h = h + alpha * direction  # push every position along the feature
                z = model.out(model.nf(h))[0, -1]
                c = int(torch.multinomial(torch.softmax(z / 0.8, 0), 1))
                ctx = torch.cat([ctx, torch.tensor([c])])
                out.append(chars[c])
        return "".join(out)

    prompt = "Spade looked at the girl for a long moment. "
    # strengths in units of a typical residual vector's length: much more than half of one and the text falls apart
    alphas = [0.0, 0.25, 0.5]
    texts = {f"{a:g}": [generate(prompt, a, seed) for seed in (1, 2, 3)] for a in alphas}
    # the push reads as "we're inside someone's speech": count the marks of speech, quotes and apostrophes, ! and ?
    marks = "\"'!?"
    speech = {k: float(np.mean([sum(t.count(m) for m in marks) for t in v])) for k, v in texts.items()}
    quotes = {k: float(np.mean([t.count('"') for t in v])) for k, v in texts.items()}
    out = dict(feature=int(best_k), purity=float(best), prompt=prompt, alphas=alphas, texts=texts, quotes=quotes,
               speech=speech, marks=marks, contexts=next(f["contexts"] for f in s["features"] if f["id"] == best_k))
    print(f"    feature {best_k} (on a quote in {best:.0%} of its top contexts); speech marks per text: {speech}", flush=True)
    assert best >= 0.5 and speech[f"{alphas[-1]:g}"] > speech["0"] + 1
    return out


# ---------------------------------------------------------------------------
PROMPT = 'Spade looked at the girl. "I don\'t know," she sai'


def compute_attribution():
    """An attribution graph for one prediction: the residual stream after block 2 rewritten as SAE features (plus the
    part they miss), and each feature's effect on the predicted character's score, to first order (activation times
    gradient); then, for the strongest features, which input characters switched them on."""
    import torch

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(3)
    s = load("sae")
    model, chars, enc, data = c11.load_tf()
    for p_ in model.parameters():
        p_.requires_grad_(False)
    sae = torch.load(CACHE.dir / "sae.pt")
    We, be, dec, bd, mu, scale = (sae[k] for k in ("We", "be", "dec", "bd", "mu", "scale"))
    assert all(c_ in chars for c_ in PROMPT)
    ids = enc(PROMPT)[None]
    T = ids.shape[1]
    th = torch.tensor(c11.rope_freqs(), dtype=torch.float32)
    ang = torch.arange(T, dtype=torch.float32)[:, None] * th[None]
    cos, sin = torch.cos(ang), torch.sin(ang)

    def features(emb):
        h = emb
        for b in model.blocks[:2]:
            h, _, _ = b(h, cos, sin)
        f = torch.relu(((h - mu) / scale) @ We + be)
        return h, f

    emb = model.emb(ids).detach()
    h, f = features(emb)
    rec = (f @ dec + bd) * scale + mu
    f_leaf = f.detach().requires_grad_(True)
    err = (h - rec).detach().requires_grad_(True)
    h2 = (f_leaf @ dec + bd) * scale + mu + err
    for b in model.blocks[2:]:
        h2, _, _ = b(h2, cos, sin)
    z = model.out(model.nf(h2))[0, -1]
    prob = torch.softmax(z, -1)
    target = int(z.argmax())
    z[target].backward()
    attr = (f_leaf.grad * f_leaf).detach()[0]  # (T, features)
    err_attr = float((err.grad * err).sum())
    flat = attr.flatten()
    top = torch.topk(flat, 6).indices
    nodes = []
    by_id = {f_["id"]: f_ for f_ in s["features"]}
    for i in top.tolist():
        pos, k = divmod(i, attr.shape[1])
        e = model.emb(ids).detach().requires_grad_(True)  # which input characters switched this feature on
        _, fk = features(e)
        fk[0, pos, k].backward()
        src = (e.grad * e).sum(-1)[0].detach().numpy()
        nodes.append(dict(pos=int(pos), feature=int(k), attr=float(flat[i]), act=float(f[0, pos, k]), inputs=[float(v) for v in src],
                          contexts=by_id[k]["contexts"] if k in by_id else []))
    top_p = torch.topk(prob, 5)
    out = dict(prompt=PROMPT, target=chars[target], p_target=float(prob[target]), logit=float(z[target]),
               total_feature_attr=float(attr.sum()), err_attr=err_attr, nodes=nodes, n_active=int((f[0] > 0).sum()),
               top_chars=[chars[int(i)] for i in top_p.indices], top_probs=top_p.values.detach().numpy())
    print(f"    '{PROMPT[-12:]}' -> {chars[target]!r} ({float(prob[target]):.0%}); top features "
          f"{[(n['pos'], n['feature'], round(n['attr'], 2)) for n in nodes]}; error term {err_attr:.2f}", flush=True)
    return out


from videos.ai.ai20.frontier import compute_frontier  # noqa: E402

ITEMS = {
    "superposition": compute_superposition,
    "sae": compute_sae,
    "frontier": compute_frontier,
    "steering": compute_steering,
    "attribution": compute_attribution,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
