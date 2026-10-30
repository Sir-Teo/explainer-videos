"""Precompute everything numerical in Part 30 of the AI series ("Inside the Model").

    python -m videos.ai.ai30.compute              # everything missing (about 2-3 CPU-hours on one or two threads)
    python -m videos.ai.ai30.compute --force sae
    AI30_SCALE=0.05 python -m videos.ai.ai30.compute   # a smoke test of every code path (into .cache/ai30_quick/)

Results are cached in ``.cache/ai30/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The subjects are the
series' own models, read through their owners' loaders: Part 13's character transformer (``videos.ai.ai13.compute``,
``load_tf``), the novels model (``explainer.ai.novels``) and Part 27's fine-tune of it (``videos.ai.ai27.compute``).
Every random choice is seeded.  The long items resume: the sweeps keep each finished run (``CACHE.partial``), the
grokking run checkpoints every 1,000 steps with its random state.  Torch threads: ``AI30_THREADS`` (default 1).

Items:
    superposition  Elhage et al.'s toy model: 5 features squeezed into 2 dimensions and back (x -> ReLU(W^T W x + b)),
                   trained at several sparsities; the interference of one feature on the rest; random directions'
                   cosines in 2 to 1,024 dimensions.  (Part 19 reads this item.)
    phase          Toy Models' phase diagram, computed: 2 features, 1 hidden dimension, a grid of feature densities and
                   relative importances, four seeds per cell; what the trained model does with the second feature (drops
                   it, gives it the dimension, or shares it in superposition) against the three candidate solutions'
                   expected losses
    saliency       a saliency map (gradient x input) for one prediction of Part 13's transformer against occlusion, and
                   Adebayo et al.'s sanity check: the map as the model's blocks are re-randomized from the top down
    probes         linear and MLP probes on every layer of the novels model for "inside a quotation", against Hewitt &
                   Liang's control task (the same labels shuffled across token types): selectivity; then the probe's
                   direction removed from the residual stream (amnesic probing) against random directions
    lens           the logit lens and a tuned lens (one affine translator per layer, trained here) on the novels model:
                   KL to the final prediction and bits per token, layer by layer; a prompt read at every layer
    induction      do our two transformers have induction heads? (copying repeated text); then Part 13's two-layer
                   attention-only model on repeated random tokens, retrained here, taken apart: previous-token and
                   induction heads, activation patching (residual stream by position, each head), path patching from
                   the previous-token head into the induction head's queries, keys and values, ablations, composition
                   scores, the induction head's OV circuit (copying), and the K path's effect through training
    sae            a sparse autoencoder (L1) with 512 features on the residual stream of Part 13's transformer after
                   block 2: 211,200 vectors from the novels; its training replayed; features per character, variance
                   explained, bits per character with the rebuild spliced in; where features fire; neurons against
                   features
    frontier       L1, JumpReLU and TopK autoencoders on the same vectors, at four or five sparsities each, three seeds each,
                   equal dictionaries, steps and batches: sparsity against variance explained and against bits per
                   character spliced in, dead latents, shrinkage; TopK with and without AuxK
    splitting      TopK dictionaries of 128, 512 and 2,048 latents: one latent's descendants as the dictionary grows
    absorption     feature absorption: a probe for "an upper-case letter", the dictionary's best latent for it, how often
                   it stays silent while a more specific latent takes over; TopK against Matryoshka, three seeds
    clt            per-layer transcoders and a cross-layer transcoder for all four MLPs of Part 13's transformer: their
                   training, reconstruction, the replacement model's bits per character
    graph          an attribution graph for one prediction, from the cross-layer transcoder (local replacement model:
                   attention patterns and layer-norm scales frozen, error nodes); its nodes' effects checked by
                   ablating them in the real model
    diffing        model diffing on the novels model and Part 27's chat fine-tune: a BatchTopK crosscoder on both
                   models' residual streams (shared, base-only and chat-only latents by relative decoder norm), and the
                   activation-difference lens (the mean difference read through the unembedding)
    steering       adding the autoencoder's quotation feature to Part 13's transformer while it writes, at three
                   strengths, five samples each, against a random direction of the same length
    mood           a contrast vector ("persona vector") in the novels model: cheerful minus gloomy sentences; its
                   projection as a monitor (AUROC on held-out sentences); steering with it at several strengths, mood and
                   fluency of the text, against a random direction
    grok           Nanda et al.'s grokking run, smaller: (a + b) mod 59, with their progress measures (grok.py)
    disagree       where the field argues, measured small: TopK dictionaries from three seeds (how many latents
                   recur), sparse probing on autoencoder latents against a linear probe on the raw vectors (few
                   examples, many), and an autoencoder trained on a randomly initialized copy of the transformer
"""

from __future__ import annotations

import math
import os
from functools import lru_cache

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai30")
load = CACHE.load
SCALE = float(os.environ.get("AI30_SCALE", "1"))
if SCALE != 1.0:  # a quick smoke test of every code path: its own cache, never the real one
    CACHE.dir = CACHE.dir.parent / "ai30_quick"


def steps(n: int) -> int:
    return max(20, int(round(n * SCALE)))


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def threads() -> None:
    from videos.ai.ai30.acts import threads as t

    t(int(os.environ.get("AI30_THREADS", "1")))


# ---------------------------------------------------------------------------
# Superposition (Part 19 reads this item: keep its keys)
# ---------------------------------------------------------------------------
def compute_superposition():
    import torch

    threads()
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
        out[f"Wtrain{S:g}"], out[f"losses{S:g}"], out["checks"] = np.array(snaps), np.array(losses), checks
        Wn = W.detach().numpy()
        out[f"W{S:g}"] = Wn  # each column: where a feature points in the 2D hidden space
        out[f"b{S:g}"] = b.detach().numpy()
        out[f"norms{S:g}"] = np.linalg.norm(Wn, axis=0)
    dense, sparse = out["norms0"], out["norms0.97"]
    assert (dense > 0.5).sum() <= 3 and (sparse > 0.5).sum() == n  # dense: only a few represented; sparse: all five
    W, b = out["W0.97"], out["b0.97"]
    out["readout"] = W.T @ W[:, 0]
    out["after_relu"] = np.maximum(W.T @ W[:, 0] + b, 0)
    assert out["after_relu"][0] > 0.5 and np.all(out["after_relu"][1:] < 0.25 * out["after_relu"][0])
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
PHASE_D = np.logspace(-2, 0, 17)  # feature density 1 - S
PHASE_R = np.logspace(-1, 1, 17)  # importance of feature 2 relative to feature 1
PHASE_SEEDS = 4


def phase_losses(W, b, dens, r, g, n=200_000):
    """Expected loss of x -> ReLU(W^T W x + b) for 2 features, density ``dens``, importances (1, r), by Monte Carlo."""
    x = g.random((n, 2)) * (g.random((n, 2)) < dens)
    xh = np.maximum(x @ np.outer(W, W) + b, 0)
    return float(((xh - x) ** 2 * np.array([1.0, r])).sum(1).mean())


def compute_phase():
    """Toy Models of Superposition, the 2-feature, 1-dimension phase diagram: trained models on a grid, and the best of
    the three candidate solutions (feature 1 alone, feature 2 alone, both antipodal with a shared bias)."""
    import torch

    threads()
    Dg, Rg = np.meshgrid(PHASE_D, PHASE_R, indexing="ij")
    cells = len(PHASE_D) * len(PHASE_R)
    G = cells * PHASE_SEEDS
    dens = torch.tensor(np.repeat(Dg.ravel(), PHASE_SEEDS), dtype=torch.float32)
    imp = torch.stack([torch.ones(G), torch.tensor(np.repeat(Rg.ravel(), PHASE_SEEDS), dtype=torch.float32)], 1)
    torch.manual_seed(2022)
    W = torch.nn.Parameter(torch.randn(G, 2) * 0.3)
    b = torch.nn.Parameter(torch.zeros(G, 2))
    opt = torch.optim.Adam([W, b], lr=3e-3)
    g = torch.Generator().manual_seed(1)
    S = steps(6000)
    mid = (len(PHASE_D) // 2) * len(PHASE_R) + len(PHASE_R) // 2  # one cell's training, replayed
    traj = []
    for s in range(S + 1):
        x = torch.rand(G, 256, 2, generator=g) * (torch.rand(G, 256, 2, generator=g) < dens[:, None, None]).float()
        h = (x * W[:, None]).sum(-1, keepdim=True)  # the one hidden number
        xh = torch.relu(h * W[:, None] + b[:, None])
        loss = ((xh - x) ** 2 * imp[:, None]).sum(-1).mean(1)
        if s % max(1, S // 60) == 0:
            traj.append([s] + W[mid * PHASE_SEEDS].tolist())
        if s == S:
            break
        opt.zero_grad()
        loss.sum().backward()
        opt.step()
    # the final loss of each run on a fixed evaluation batch (a larger one), the best seed per cell
    ge = torch.Generator().manual_seed(2)
    with torch.no_grad():
        tot = torch.zeros(G)
        for _ in range(8):
            x = torch.rand(G, 2048, 2, generator=ge) * (torch.rand(G, 2048, 2, generator=ge) < dens[:, None, None]).float()
            h = (x * W[:, None]).sum(-1, keepdim=True)
            tot += ((torch.relu(h * W[:, None] + b[:, None]) - x) ** 2 * imp[:, None]).sum(-1).mean(1)
    Wn = W.detach().numpy().reshape(cells, PHASE_SEEDS, 2)
    bn = b.detach().numpy().reshape(cells, PHASE_SEEDS, 2)
    L = (tot / 8).numpy().reshape(cells, PHASE_SEEDS)
    best = L.argmin(1)
    Wb = Wn[np.arange(cells), best]
    bb = bn[np.arange(cells), best]
    n1, n2 = np.abs(Wb[:, 0]), np.abs(Wb[:, 1])
    # 0: feature 2 not represented; 1: feature 2 gets the dimension (feature 1 dropped); 2: both, in superposition
    emp = np.where(n2 < 0.5, 0, np.where(n1 < 0.5, 1, 2))
    agree_seeds = np.mean([np.mean(np.where(np.abs(Wn[:, k, 1]) < 0.5, 0, np.where(np.abs(Wn[:, k, 0]) < 0.5, 1, 2)) == emp)
                           for k in range(PHASE_SEEDS)])
    # the candidates' expected losses (Monte Carlo, the bias of the shared solution searched on a grid)
    gm = rng(3)
    theory = np.zeros(cells, int)
    cand = np.zeros((cells, 3))
    bgrid = np.linspace(-1.0, 0.0, 21)
    for i, (dd, rr) in enumerate(zip(Dg.ravel(), Rg.ravel())):
        c1 = phase_losses(np.array([1.0, 0.0]), np.zeros(2), dd, rr, gm, 40_000)
        c2 = phase_losses(np.array([0.0, 1.0]), np.zeros(2), dd, rr, gm, 40_000)
        c3 = min(phase_losses(np.array([1.0, -1.0]), np.array([bv, bv]), dd, rr, gm, 40_000) for bv in bgrid)
        cand[i] = (c1, c2, c3)
        theory[i] = int(np.argmin([c1, c2, c3]))
    agree = float(np.mean(emp == theory))
    print(f"    phase diagram: trained and theory agree on {agree:.0%} of cells; seeds agree with the best on "
          f"{agree_seeds:.0%}; counts {np.bincount(emp, minlength=3)}", flush=True)
    return dict(dens=PHASE_D, rel=PHASE_R, emp=emp.reshape(Dg.shape), theory=theory.reshape(Dg.shape),
                W=Wb.reshape(*Dg.shape, 2), b=bb.reshape(*Dg.shape, 2), cand=cand.reshape(*Dg.shape, 3),
                agree=agree, agree_seeds=float(agree_seeds), seeds=PHASE_SEEDS, steps=S, traj=np.array(traj),
                mid=[int(len(PHASE_D) // 2), int(len(PHASE_R) // 2)])


# ---------------------------------------------------------------------------
# Part 13's transformer: the residual stream after block 2
# ---------------------------------------------------------------------------
LAYER = 1  # 0-based: the output of the second block
N_WIN = 1100
SAE_PROMPT = 'Spade looked at the girl. "I don\'t know," she sai'


@lru_cache(maxsize=None)
def tf_model():
    from videos.ai.ai13 import compute as c13

    c13.load("tf")
    return c13.load_tf()


@lru_cache(maxsize=None)
def tf_vectors(n_win=N_WIN):
    """The residual stream after block 2 on ``n_win`` windows of held-out text (positions 64 on): raw (A), centred and
    scaled so a vector's mean squared length is D (X), the character ids of every position, the window starts."""
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    model, chars, enc, data = tf_model()
    n_win = max(40, int(n_win * min(1.0, SCALE * 4)))
    starts, W = acts.tf_windows(c13, data, n_win, 2023)  # Bricken et al., Towards Monosemanticity
    A = acts.tf_collect(model, c13, W, keys=("post",), layers=(LAYER,))[("post", LAYER)]
    mu = A.mean(0)
    sig = float(((A - mu) ** 2).sum(1).mean().sqrt()) / math.sqrt(A.shape[1])
    X = (A - mu) / sig
    ids = W[:, 64:].reshape(-1)
    return dict(A=A, X=X, mu=mu, sig=sig, ids=ids, starts=starts, windows=W, T64=W.shape[1] - 64,
                mean_norm=float((A - mu).norm(dim=1).mean()))


def tf_splice(d, v):
    """A function for acts.tf_bits_with: the residual stream replaced by dictionary ``d``'s rebuild."""
    from videos.ai.ai30 import dicts

    def fn(h):
        x = (h - v["mu"]) / v["sig"]
        return dicts.encode(d, x) @ d.Wd * v["sig"] + d.bd * v["sig"] + v["mu"]

    return fn


@lru_cache(maxsize=None)
def tf_eval_windows(n=48):
    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    _, _, _, data = tf_model()
    _, W = acts.tf_windows(c13, data, max(8, int(n * min(1.0, SCALE * 4))), 4242, ctx=c13.CTX + 1)
    return W


def spliced_bits(d, v):
    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    model = tf_model()[0]
    return acts.tf_bits_with(model, c13, tf_eval_windows(), LAYER, tf_splice(d, v))


@lru_cache(maxsize=None)
def tf_reference_bits():
    """Bits per character as the model is, and with the residual stream after block 2 replaced by its mean (what a
    rebuild has to beat)."""
    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    model = tf_model()[0]
    v = tf_vectors()
    clean = acts.tf_bits_with(model, c13, tf_eval_windows(), LAYER, None)
    mean = acts.tf_bits_with(model, c13, tf_eval_windows(), LAYER, lambda h: v["mu"].expand_as(h))
    return clean, mean


def contexts_of(v, positions, before=24, after=2):
    """The text around each of ``positions`` (indices into the vectors), up to the character and one past it."""
    chars = tf_model()[1]
    va = tf_model()[3]["valid"]
    out = []
    for p in positions:
        w, off = divmod(int(p), v["T64"])
        s = int(v["starts"][w]) + 64 + off
        out.append("".join(chars[int(c)] for c in va[s - before:s + after]))
    return out


def top_positions(d, X, k=8, chunk=16384, latents=None):
    """For every latent (or those listed), the ``k`` positions where it is most strongly on, and its frequency."""
    import torch

    from videos.ai.ai30 import dicts

    F = d.We.shape[1]
    best_v = torch.full((F, k), -1.0)
    best_i = torch.zeros((F, k), dtype=torch.long)
    on = torch.zeros(F)
    with torch.no_grad():
        for i in range(0, len(X), chunk):
            f = dicts.encode(d, X[i:i + chunk])
            on += (f > 0).float().sum(0)
            v_, i_ = torch.topk(f.T, min(k, f.shape[0]), dim=1)
            allv = torch.cat([best_v, v_], 1)
            alli = torch.cat([best_i, i_ + i], 1)
            o = torch.topk(allv, k, dim=1).indices
            best_v, best_i = allv.gather(1, o), alli.gather(1, o)
    return best_v.numpy(), best_i.numpy(), (on / len(X)).numpy()


def describe(d, v, k=8, min_freq=0.0, latents=None):
    """Each live latent: its frequency, the contexts of its top activations, and their purity (the share of them on
    the most common character)."""
    bv, bi, freq = top_positions(d, v["X"], k)
    feats = []
    order = np.argsort(-freq)
    for j in order:
        if freq[j] <= min_freq or (latents is not None and j not in latents):
            continue
        ctx = contexts_of(v, [p for p, val in zip(bi[j], bv[j]) if val > 0])
        last = [c[-2] for c in ctx]
        pur = max(last.count(c) for c in set(last)) / len(last) if last else 0.0
        feats.append(dict(id=int(j), freq=float(freq[j]), contexts=ctx, purity=float(pur)))
    return feats


def mlp_neurons(model, seq, starts, c13):
    """The 512 neurons of block 2's MLP (after the GELU), for windows of the text (positions 64 on)."""
    import torch

    from videos.ai.ai30 import acts

    out = []
    with torch.no_grad():
        for i in range(0, len(starts), 16):
            x = torch.stack([seq[s:s + c13.CTX] for s in starts[i:i + 16]])
            recs, _ = acts.tf_layers(model, x, c13)
            b = model.blocks[LAYER]
            out.append(torch.nn.functional.gelu(b.f1(recs[LAYER]["mlp_in"]))[:, 64:].reshape(-1, b.f1.out_features))
    return torch.cat(out)


def compute_sae():
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts, dicts

    threads()
    model, chars, enc, data = tf_model()
    v = tf_vectors()
    X = v["X"]
    ps = data["passage"]
    s0 = 400
    h = acts.tf_collect(model, c13, torch.stack([ps[s0 - 192:s0 + 64]]), layers=(LAYER,))[("post", LAYER)][-64:]
    Xd = (h - v["mu"]) / v["sig"]
    lam = 2.0
    S = steps(4000)
    d, rec = dicts.train(X, "l1", lam, F=512, steps=S, batch=1024, seed=0, snap_every=max(1, S // 20), probe=Xd)
    e = dicts.evaluate(d, X)
    feats = describe(d, v)
    clean, mean_bits = tf_reference_bits()
    bits = spliced_bits(d, v)
    with torch.no_grad():
        Fd = dicts.encode(d, Xd)
        Rd = Fd @ d.Wd + d.bd
    # the model's own neurons (block 2's MLP), described the same way, on a subset of the windows
    N = mlp_neurons(model, data["valid"], v["starts"][:300], c13)
    n_pur = []
    for k in range(N.shape[1]):
        top = torch.topk(N[:, k], 8).indices.numpy()
        last = [c[-2] for c in contexts_of(v, top, 1, 2)]
        n_pur.append(max(last.count(c_) for c_ in set(last)) / len(last))
    n_pur = np.array(n_pur)
    med = int(np.argsort(n_pur)[len(n_pur) // 2])  # a neuron of median purity
    neuron_ctx = contexts_of(v, torch.topk(N[:, med], 8).indices.numpy())
    f_pur = np.array([f_["purity"] for f_ in feats])
    out = dict(D=int(X.shape[1]), F=512, l0=e["l0"], fvu=e["fvu"], dead=e["dead"], shrink=e["shrink"],
               n_vectors=int(len(X)), lam=lam, steps=S, features=feats, mu=v["mu"].numpy(), scale=v["mean_norm"],
               sig=v["sig"], dirs=(d.Wd * v["mean_norm"]).numpy(), neuron_purity=n_pur, feature_purity=f_pur,
               neuron=med, neuron_contexts=neuron_ctx, demo_text="".join(chars[int(c)] for c in ps[s0:s0 + 64]),
               demo_resid=Xd.numpy(), demo_feats=Fd.numpy(), demo_rec=Rd.numpy(), bits_clean=clean,
               bits_mean=mean_bits, bits_spliced=bits, rec_step=rec["step"], rec_l0=rec["l0"], rec_fvu=rec["fvu"],
               snap_steps=rec["snap_steps"], snap_codes=np.array(rec["snaps"]).astype(np.float32))
    print(f"    {len(X)} vectors; {e['l0']:.1f} features per character; unexplained {e['fvu']:.3f}; {e['dead']} dead; "
          f"bits {clean:.3f} clean, {bits:.3f} spliced, {mean_bits:.3f} mean; purity neurons {n_pur.mean():.2f}, "
          f"features {f_pur.mean():.2f}", flush=True)
    torch.save(dict(d.state(), mu=v["mu"], sig=v["sig"], scale=v["mean_norm"]), CACHE.dir / "sae.pt")
    return out


def load_dict(path):
    import torch

    from videos.ai.ai30 import dicts

    st = torch.load(path, weights_only=False)
    return dicts.Dict.from_state(st), st


# ---------------------------------------------------------------------------
FRONT = dict(F=512, steps=2000, batch=1024, seeds=(0, 1, 2), l1=(0.25, 0.5, 1.0, 2.0, 4.0),
             jumprelu=(0.1, 0.3, 1.0, 3.0, 8.0), topk=(4, 8, 16, 32))


def dict_dir():
    p = CACHE.dir / "dicts"
    p.mkdir(parents=True, exist_ok=True)
    return p


def compute_frontier():
    """Three kinds of sparse autoencoder at equal budgets: the same 512 latents, steps, batches and data; four
    sparsities each, three seeds each."""
    import torch

    from videos.ai.ai30 import dicts

    threads()
    v = tf_vectors()
    X = v["X"]
    n_eval = min(len(X), 40000)
    Xe = X[torch.randperm(len(X), generator=torch.Generator().manual_seed(9))[:n_eval]]
    S = steps(FRONT["steps"])
    # the pieces are keyed by kind, parameter and seed, so adding a sparsity to a sweep keeps the runs already done
    part = CACHE.partial("frontier", dict(F=FRONT["F"], steps=S, batch=FRONT["batch"], n=len(X)))
    runs = [(k, p, s) for k in ("l1", "jumprelu", "topk") for p in FRONT[k] for s in FRONT["seeds"]]
    runs += [("topk_aux", 16, s) for s in FRONT["seeds"]]
    for kind, p, seed in runs:
        key = f"{kind}_{p:g}_{seed}"
        if key in part:
            continue
        d, rec = dicts.train(X, "topk" if kind == "topk_aux" else kind, p, F=FRONT["F"], steps=S,
                             batch=FRONT["batch"], seed=seed, aux_k=64 if kind == "topk_aux" else 0)
        e = dicts.evaluate(d, Xe)
        r = dict(l0=e["l0"], fvu=e["fvu"], dead=e["dead"], shrink=e["shrink"], bits=spliced_bits(d, v),
                 curve=list(zip(rec["step"], rec["l0"], rec["fvu"])))
        if kind in ("topk", "l1", "jumprelu") and seed in (0, 1, 2):
            torch.save(d.state(), dict_dir() / f"{key}.pt")
        print(f"    {key}: L0 {r['l0']:.1f}, unexplained {r['fvu']:.3f}, {r['dead']} dead, rescale {r['shrink']:.2f}, "
              f"bits {r['bits']:.3f}", flush=True)
        part[key] = r
    clean, mean_bits = tf_reference_bits()
    out = dict(F=FRONT["F"], steps=S, batch=FRONT["batch"], seeds=list(FRONT["seeds"]), l1s=list(FRONT["l1"]),
               jumps=list(FRONT["jumprelu"]), ks=list(FRONT["topk"]), bits_clean=clean, bits_mean=mean_bits,
               n_vectors=int(len(X)))
    for kind, p, seed in runs:
        r = part[f"{kind}_{p:g}_{seed}"]
        for k_, val in r.items():
            out[f"{kind}_{p:g}_{seed}_{k_}"] = np.array(val) if k_ == "curve" else val
    # equal-sparsity comparison: each kind's unexplained variance, interpolated in log L0, at L0 = 8, 16, 32
    for kind, ps_ in (("l1", FRONT["l1"]), ("jumprelu", FRONT["jumprelu"]), ("topk", FRONT["topk"])):
        for target in (8, 16, 32):
            vals = []
            for seed in FRONT["seeds"]:
                pts = sorted((out[f"{kind}_{p:g}_{seed}_l0"], out[f"{kind}_{p:g}_{seed}_fvu"],
                              out[f"{kind}_{p:g}_{seed}_bits"]) for p in ps_)
                l0s = np.log([max(a, 1e-3) for a, _, _ in pts])
                if not (l0s[0] <= math.log(target) <= l0s[-1]):
                    vals.append((np.nan, np.nan))
                    continue
                vals.append((float(np.interp(math.log(target), l0s, [b for _, b, _ in pts])),
                             float(np.interp(math.log(target), l0s, [c for _, _, c in pts]))))
            out[f"at{target}_{kind}_fvu"] = [a for a, _ in vals]
            out[f"at{target}_{kind}_bits"] = [b for _, b in vals]
    return out


# ---------------------------------------------------------------------------
SPLIT = dict(sizes=(128, 512, 2048), k=16, steps=2000, batch=1024, seed=0)


def compute_splitting():
    """Feature splitting: TopK dictionaries of growing size on the same vectors; for latents of the smallest, their
    closest latents (by decoder direction) in the larger ones, and where each fires."""
    import torch

    from videos.ai.ai30 import dicts

    threads()
    v = tf_vectors()
    X = v["X"]
    S = steps(SPLIT["steps"])
    part = CACHE.partial("splitting", dict(SPLIT, steps=S, n=len(X)))
    ds = {}
    for F in SPLIT["sizes"]:
        path = dict_dir() / f"split_{F}.pt"
        if str(F) in part and path.exists():
            ds[F], _ = load_dict(path)
            continue
        d, _ = dicts.train(X, "topk", SPLIT["k"], F=F, steps=S, batch=SPLIT["batch"], seed=SPLIT["seed"])
        torch.save(d.state(), path)
        e = dicts.evaluate(d, X[:40000])
        part[str(F)] = dict(l0=e["l0"], fvu=e["fvu"], dead=e["dead"])
        ds[F] = d
        print(f"    split {F}: unexplained {e['fvu']:.3f}, {e['dead']} dead", flush=True)
    small, mid, big = (ds[F] for F in SPLIT["sizes"])
    dsm = describe(small, v)
    dmid = {f["id"]: f for f in describe(mid, v)}
    dbig = {f["id"]: f for f in describe(big, v)}

    def char_of(f):
        last = [c[-2] for c in f["contexts"]]
        return max(set(last), key=last.count) if last else ""

    Ws, Wm, Wb = (d.Wd.numpy() for d in (small, mid, big))
    # a clean family: a parent that fires on one character, and children (decoders pointing nearly the same way)
    # that fire on the same character in narrower contexts
    fam = []
    for f in dsm:
        j, ch = f["id"], char_of(f)
        if f["purity"] < 0.75 or ch in " \n":
            continue
        cm, cb = Wm @ Ws[j], Wb @ Ws[j]
        kids_m = [int(i) for i in np.argsort(-cm)[:8] if cm[i] > 0.4 and i in dmid and char_of(dmid[i]) == ch]
        kids_b = [int(i) for i in np.argsort(-cb)[:12] if cb[i] > 0.4 and i in dbig and char_of(dbig[i]) == ch]
        fam.append((j, kids_m, kids_b, f["freq"]))
    pick = max(fam, key=lambda t: (min(len(t[2]), 6), len(t[1]) > 0, t[3])) if fam else (dsm[0]["id"], [], [], 0)
    j, km, kb = pick[0], pick[1], pick[2]
    by_id = {f["id"]: f for f in dsm}
    best_m = np.array([float((Wm @ Ws[i]).max()) for i in range(len(Ws))])
    best_b = np.array([float((Wb @ Ws[i]).max()) for i in range(len(Ws))])
    n_kids = []
    for i in range(len(Ws)):
        cb = Wb @ Ws[i]
        n_kids.append(int((cb > 0.4).sum()))
    out = dict(sizes=list(SPLIT["sizes"]), k=SPLIT["k"], steps=S, parent=by_id[j], char=char_of(by_id[j]),
               mid=[dict(dmid[i], cos=float(Wm[i] @ Ws[j])) for i in km],
               big=[dict(dbig[i], cos=float(Wb[i] @ Ws[j])) for i in kb],
               best_mid=best_m, best_big=best_b, n_kids_big=np.array(n_kids),
               n_same_char_families=int(sum(len(t[2]) >= 2 for t in fam)), n_candidates=len(fam))
    for F in SPLIT["sizes"]:
        for k_, val in part[str(F)].items():
            out[f"{F}_{k_}"] = val
    print(f"    splitting: latent {j} ({by_id[j]['contexts'][0][-14:]!r}) -> {len(km)} in 512, {len(kb)} in 2048 on the same "
          f"character; {out['n_same_char_families']} of {len(fam)} clean latents have two or more such children", flush=True)
    return out


# ---------------------------------------------------------------------------
ABSORB = dict(F=512, k=16, steps=2000, batch=1024, seeds=(0, 1, 2), prefixes=(32, 128))


def compute_absorption():
    """Feature absorption (Chanin et al. 2024), measured for "the character is an upper-case letter": a logistic
    probe on the vectors gives the direction; the dictionary's main latent for it is the one that best separates
    upper case from the rest (F1); where upper case is true and the main latent is silent, does another active latent
    carry most of the probe direction instead?  TopK against Matryoshka (Bussmann et al. 2025), equal size and k."""
    import torch

    from videos.ai.ai30 import dicts

    threads()
    v = tf_vectors()
    X = v["X"]
    chars = tf_model()[1]
    upper = torch.tensor([chars[int(c)].isupper() for c in v["ids"]])
    g = torch.Generator().manual_seed(5)
    perm = torch.randperm(len(X), generator=g)
    tr, te = perm[: len(X) // 2], perm[len(X) // 2:]
    # the probe: logistic regression, balanced
    w = torch.zeros(X.shape[1], requires_grad=True)
    b0 = torch.zeros(1, requires_grad=True)
    opt = torch.optim.Adam([w, b0], lr=1e-2)
    pw = (~upper[tr]).float().sum() / upper[tr].float().sum()
    for _ in range(steps(600)):
        i = tr[torch.randint(0, len(tr), (4096,), generator=g)]
        loss = torch.nn.functional.binary_cross_entropy_with_logits(X[i] @ w + b0, upper[i].float(), pos_weight=pw)
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        acc = float((((X[te] @ w + b0) > 0) == upper[te]).float().mean())
        pdir = (w / w.norm()).detach()
    S = steps(ABSORB["steps"])
    part = CACHE.partial("absorption", dict(ABSORB, steps=S, n=len(X)))
    Xt, ut = X[te], upper[te]
    for kind in ("topk", "matryoshka"):
        for seed in ABSORB["seeds"]:
            key = f"{kind}_{seed}"
            if key in part:
                continue
            d, _ = dicts.train(X[tr], kind, ABSORB["k"], F=ABSORB["F"], steps=S, batch=ABSORB["batch"], seed=seed,
                               prefixes=list(ABSORB["prefixes"]) if kind == "matryoshka" else None)
            e = dicts.evaluate(d, Xt[:40000])
            with torch.no_grad():
                f = dicts.encode(d, Xt)
                on = f > 0
                tp = (on & ut[:, None]).float().sum(0)
                fp = (on & ~ut[:, None]).float().sum(0)
                fn = (~on & ut[:, None]).float().sum(0)
                f1 = 2 * tp / (2 * tp + fp + fn).clamp_min(1)
                main = int(f1.argmax())
                cos = d.Wd @ pdir
                # among upper-case positions where the main latent is silent: does one other active latent carry most
                # of the rebuild's projection on the probe direction (and point along it)?
                miss = ut & ~on[:, main]
                fm = f[miss]
                contrib = fm * cos[None]  # each active latent's share of the projection
                tot = contrib.clamp_min(0).sum(1).clamp_min(1e-9)
                topc, topj = contrib.max(1)
                absorbed = (topc / tot >= 0.4) & (cos[topj] >= 0.1)
                n_up = int(ut.sum())
                r = dict(fvu=e["fvu"], main=main, main_f1=float(f1[main]), main_cos=float(cos[main]),
                         recall=float(on[ut, main].float().mean()), precision=float(tp[main] / (tp[main] + fp[main])),
                         absorption=float(absorbed.sum()) / n_up, miss=float(miss.sum()) / n_up,
                         absorbers=[int(x_) for x_ in torch.bincount(topj[absorbed], minlength=d.Wd.shape[0])
                                    .argsort(descending=True)[:4]],
                         prefix_rank=main)
                # which characters the main latent misses most
                ch_miss = {}
                for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    sel = torch.tensor([chars[int(i_)] == c for i_ in v["ids"][te]])
                    if int(sel.sum()) >= 20:
                        ch_miss[c] = float((~on[sel, main]).float().mean())
                r["miss_by_char"] = ch_miss
                r["absorber_contexts"] = []
            if seed == ABSORB["seeds"][0]:
                torch.save(d.state(), dict_dir() / f"absorb_{key}.pt")
            print(f"    {key}: main latent {main} (F1 {r['main_f1']:.2f}, recall {r['recall']:.2f}); absorbed "
                  f"{r['absorption']:.1%} of upper-case positions; unexplained {r['fvu']:.3f}", flush=True)
            part[key] = r
    out = dict(F=ABSORB["F"], k=ABSORB["k"], steps=S, seeds=list(ABSORB["seeds"]), prefixes=list(ABSORB["prefixes"]),
               probe_acc=acc, upper_share=float(upper.float().mean()))
    for key, r in part.done.items():
        for k_, val in r.items():
            out[f"{key}_{k_}"] = val
    # the contexts of the first seed's main latent and its absorbers, for the picture
    for kind in ("topk", "matryoshka"):
        d, _ = load_dict(dict_dir() / f"absorb_{kind}_0.pt")
        r = part[f"{kind}_0"]
        lat = [r["main"]] + r["absorbers"][:3]
        desc = {f["id"]: f for f in describe(d, v, latents=set(lat))}
        out[f"{kind}_contexts"] = [desc[j] for j in lat if j in desc]
    return out


from videos.ai.ai30.items import (  # noqa: E402
    compute_clt, compute_diffing, compute_disagree, compute_graph, compute_grok, compute_induction, compute_lens,
    compute_mood, compute_probes, compute_saliency, compute_steering)

ITEMS = {
    "superposition": compute_superposition,
    "phase": compute_phase,
    "saliency": compute_saliency,
    "sae": compute_sae,
    "steering": compute_steering,
    "induction": compute_induction,
    "probes": compute_probes,
    "lens": compute_lens,
    "mood": compute_mood,
    "diffing": compute_diffing,
    "frontier": compute_frontier,
    "splitting": compute_splitting,
    "absorption": compute_absorption,
    "clt": compute_clt,
    "graph": compute_graph,
    "disagree": compute_disagree,
    "grok": compute_grok,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    from videos.ai.ai30 import compute as _module  # one instance of this module (items.py imports it by name)

    _module.CACHE.main(_module.ITEMS, __doc__)
