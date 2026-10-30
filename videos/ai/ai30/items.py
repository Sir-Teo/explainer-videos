"""Part 30's compute items beyond the dictionaries (compute.py registers them): saliency, steering, the induction
circuit, probes, lenses, a contrast vector, model diffing, transcoders and an attribution graph, the disagreements, and
grokking.  See compute.py's docstring for what each item holds."""

from __future__ import annotations

import math

import numpy as np



class _Compute:
    """compute.py, imported on first use (it imports this module at its end)."""

    def __getattr__(self, name):
        import importlib

        return getattr(importlib.import_module("videos.ai.ai30.compute"), name)


C = _Compute()


def _spearman(a, b):
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


# ---------------------------------------------------------------------------
SAL_PROMPT = 'Spade looked at the girl. "I don\'t know," she sai'


def compute_saliency():
    """Gradient x input against occlusion for predictions of Part 13's transformer, and the map after the model's
    blocks are re-randomized from the top down (Adebayo et al. 2018's cascading randomization)."""
    import copy

    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    C.threads()
    model, chars, enc, data = C.tf_model()

    def forward(m, e):
        cos, sin = acts.tf_rope(c13, e.shape[1])
        h = e
        for b in m.blocks:
            h, _, _ = b(h, cos, sin)
        return m.out(m.nf(h))[0, -1]

    def saliency(m, ids, target=None):
        e = m.emb(ids[None]).detach().requires_grad_(True)
        z = forward(m, e)
        t = int(z.argmax()) if target is None else target
        z[t].backward()
        return (e.grad * e).sum(-1)[0].detach().numpy(), t, z.detach()

    def occlusion(m, ids, t):
        with torch.no_grad():
            base = float(forward(m, m.emb(ids[None]))[t])
            sp = chars.index(" ")
            out = []
            for i in range(len(ids) - 1):  # every character but the last, replaced by a space
                x = ids.clone()
                x[i] = sp if int(x[i]) != sp else chars.index("e")
                out.append(base - float(forward(m, m.emb(x[None]))[t]))
            out.append(np.nan)
        return np.array(out)

    def randomized(k, seed=0):
        """The model with its top k blocks (k = 5: also the embedding) re-initialized."""
        torch.manual_seed(seed)
        fresh = c13.build_tf(len(chars))
        m = copy.deepcopy(model)
        for i in range(min(k, 4)):
            m.blocks[3 - i].load_state_dict(fresh.blocks[3 - i].state_dict())
        if k >= 5:
            m.emb.load_state_dict(fresh.emb.state_dict())
        return m.eval()

    ids = enc(SAL_PROMPT)
    sal, t, z = saliency(model, ids)
    occ = occlusion(model, ids, t)
    p = torch.softmax(z, 0)
    casc = []
    for k in range(6):
        s_k, _, _ = saliency(randomized(k), ids, t)
        casc.append(s_k)
    rho_casc = [_spearman(np.abs(casc[0]), np.abs(s_)) for s_ in casc]
    # the same on 24 more predictions from the passage
    g = C.rng(1998)
    ps = data["passage"]
    rho_occ, rho_rand = [], []
    for s0 in g.integers(80, len(ps) - 1, 24):
        x = ps[s0 - 48:s0]
        s1, t1, _ = saliency(model, x)
        o1 = occlusion(model, x, t1)
        ok = ~np.isnan(o1)
        rho_occ.append(_spearman(s1[ok], o1[ok]))
        s2, _, _ = saliency(randomized(5, seed=int(s0)), x, t1)
        rho_rand.append(_spearman(np.abs(s1), np.abs(s2)))
    ok = ~np.isnan(occ)
    out = dict(prompt=SAL_PROMPT, target=chars[t], p_target=float(p[t]), saliency=sal, occlusion=occ,
               cascade=np.array(casc), rho_cascade=rho_casc, rho_occ_demo=_spearman(sal[ok], occ[ok]),
               rho_occ=rho_occ, rho_rand=rho_rand, cascade_names=["trained", "block 4", "blocks 3-4", "blocks 2-4",
                                                                  "all blocks", "and the embedding"])
    print(f"    saliency vs occlusion: rho {out['rho_occ_demo']:.2f} (demo), {np.mean(rho_occ):.2f} on 24; trained vs "
          f"fully random map: {np.mean(rho_rand):.2f}; cascade {np.round(rho_casc, 2)}", flush=True)
    return out


# ---------------------------------------------------------------------------
STEER_PROMPT = "Spade looked at the girl for a long moment. "


def compute_steering():
    """Adding the L1 autoencoder's quotation feature (its decoder direction, scaled by a typical residual vector's
    length) to Part 13's transformer after block 2 while it writes; five samples per strength; a random direction of
    the same length as the control."""
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    C.threads()
    s = C.load("sae")
    model, chars, enc, data = C.tf_model()
    d, st = C.load_dict(C.CACHE.dir / "sae.pt")
    best, best_k = -1.0, None
    for f in s["features"]:  # the feature most tied to quotation marks: its top activations sit on a '"'
        frac = np.mean([c_[-2] == '"' for c_ in f["contexts"]])
        if frac > best:
            best, best_k = frac, f["id"]
    scale = float(st["scale"])
    direction = d.Wd[best_k] * scale
    g = torch.Generator().manual_seed(7)
    rnd = torch.randn(direction.shape[0], generator=g)
    rnd = rnd / rnd.norm() * scale

    def generate(prompt, vec, alpha, seed, n=160):
        gen = torch.Generator().manual_seed(seed)
        ctx = enc(prompt)
        out = []
        with torch.no_grad():
            for _ in range(n):
                x = ctx[None, -c13.CTX:]
                cos, sin = acts.tf_rope(c13, x.shape[1])
                h = model.emb(x)
                for li, b in enumerate(model.blocks):
                    h, _, _ = b(h, cos, sin)
                    if li == C.LAYER:
                        h = h + alpha * vec  # push every position along the direction
                z = model.out(model.nf(h))[0, -1]
                c = int(torch.multinomial(torch.softmax(z / 0.8, 0), 1, generator=gen))
                ctx = torch.cat([ctx, torch.tensor([c])])
                out.append(chars[c])
        return "".join(out)

    alphas = [0.0, 0.25, 0.5]
    seeds = (1, 2, 3, 4, 5)
    marks = "\"'!?"

    def count(t):
        return sum(t.count(m) for m in marks)

    texts = {f"{a:g}": [generate(STEER_PROMPT, direction, a, sd) for sd in seeds] for a in alphas}
    rtexts = [generate(STEER_PROMPT, rnd, alphas[-1], sd) for sd in seeds]
    speech = {k: [count(t) for t in v] for k, v in texts.items()}
    out = dict(feature=int(best_k), purity=float(best), prompt=STEER_PROMPT, alphas=alphas, seeds=list(seeds),
               texts=texts, speech=speech, speech_mean={k: float(np.mean(v)) for k, v in speech.items()},
               random_texts=rtexts, random_speech=[count(t) for t in rtexts], marks=marks, scale=scale,
               contexts=next(f["contexts"] for f in s["features"] if f["id"] == best_k))
    print(f"    feature {best_k} (a quote in {best:.0%} of its top contexts); speech marks per text: "
          f"{out['speech_mean']}; random direction: {np.mean(out['random_speech']):.1f}", flush=True)
    return out


# ---------------------------------------------------------------------------
# Induction heads
# ---------------------------------------------------------------------------
IV, IT, ID, IH = 64, 96, 64, 4  # Part 13's two-layer attention-only model: vocabulary, length, width, heads
I_STEPS, I_SNAP = 5000, 250


def att2_build():
    import torch
    import torch.nn as nn

    class AttnOnly(nn.Module):
        """Part 13's attention-only transformer (videos/ai/ai13/compute.py, compute_induction), with hooks: each head's
        output can be replaced, and the residual stream patched at any layer and position."""

        def __init__(self, layers=2):
            super().__init__()
            self.emb = nn.Embedding(IV, ID)
            self.pos = nn.Parameter(torch.randn(IT, ID) * 0.1)
            self.qkv = nn.ModuleList([nn.Linear(ID, 3 * ID, bias=False) for _ in range(layers)])
            self.o = nn.ModuleList([nn.Linear(ID, ID, bias=False) for _ in range(layers)])
            self.out = nn.Linear(ID, IV, bias=False)

        def head_out(self, l_, h_q, h_k, h_v):
            """Every head of layer l_, its queries from h_q, keys from h_k, values from h_v: (B, H, T, D) outputs and
            the patterns."""
            B, T, _ = h_q.shape
            W = self.qkv[l_].weight
            dh = ID // IH
            q = (h_q @ W[:ID].T).view(B, T, IH, dh).transpose(1, 2)
            k = (h_k @ W[ID:2 * ID].T).view(B, T, IH, dh).transpose(1, 2)
            v = (h_v @ W[2 * ID:].T).view(B, T, IH, dh).transpose(1, 2)
            s = (q @ k.transpose(-1, -2)) / math.sqrt(dh)
            s = s.masked_fill(~torch.ones(T, T, dtype=torch.bool).tril(), float("-inf"))
            p = torch.softmax(s, -1)
            Wo = self.o[l_].weight.view(ID, IH, dh)
            return torch.einsum("bhtd,ehd->bhte", p @ v, Wo), p

        def forward(self, x, rec=False, patch=None):
            """``patch``: {("resid", l_): fn(h) -> h} (l_ = 0: the input, 1: between the layers, 2: the output),
            {("head", l_, h_): fn(out) -> out}, {("kqv", l_, h_): (hq, hk, hv) inputs for that head}."""
            patch = patch or {}
            h = self.emb(x) + self.pos[None, : x.shape[1]]
            r = {"resid0": h}
            if ("resid", 0) in patch:
                h = patch[("resid", 0)](h)
            for l_ in range(len(self.qkv)):
                outs, p = self.head_out(l_, h, h, h)
                for h_ in range(IH):
                    if ("kqv", l_, h_) in patch:
                        hq, hk, hv = patch[("kqv", l_, h_)](h)
                        o2, p2 = self.head_out(l_, hq, hk, hv)
                        outs = outs.clone()
                        outs[:, h_] = o2[:, h_]
                        p = p.clone()
                        p[:, h_] = p2[:, h_]
                    if ("head", l_, h_) in patch:
                        outs = outs.clone()
                        outs[:, h_] = patch[("head", l_, h_)](outs[:, h_])
                r[f"heads{l_}"], r[f"attn{l_}"] = outs, p
                h = h + outs.sum(1)
                r[f"resid{l_ + 1}"] = h
                if ("resid", l_ + 1) in patch:
                    h = patch[("resid", l_ + 1)](h)
            z = self.out(h)
            return (z, r) if rec else z

        def mats(self, layer, head):
            W = self.qkv[layer].weight.detach().double().numpy()
            sl = slice(head * (ID // IH), (head + 1) * (ID // IH))
            Wq, Wk, Wv = W[:ID][sl], W[ID:2 * ID][sl], W[2 * ID:][sl]
            Wo = self.o[layer].weight.detach().double().numpy()[:, sl]
            return Wq.T @ Wk, Wo @ Wv

    return AttnOnly()


def att2_batch(g, n):
    """Part 13's task: random tokens with one stretch (12-29 tokens) repeated later; the mask marks the positions
    whose next token is predictable from the repeat."""
    import torch

    x = g.integers(0, IV, (n, IT))
    mask = np.zeros((n, IT), bool)
    src_ = np.zeros(n, int)
    dst_ = np.zeros(n, int)
    ln_ = np.zeros(n, int)
    for b in range(n):
        ln = int(g.integers(12, 30))
        src = int(g.integers(0, IT // 2 - ln))
        dst = int(g.integers(src + ln + 1, IT - ln + 1))
        x[b, dst:dst + ln] = x[b, src:src + ln]
        mask[b, dst:dst + ln - 1] = True
        src_[b], dst_[b], ln_[b] = src, dst, ln
    return torch.tensor(x), torch.tensor(mask), src_, dst_, ln_


def att2_corrupt(x, src, ln, g):
    """The same sequences with the first copy replaced by fresh random tokens: nothing left to copy from."""
    xc = x.clone()
    for b in range(len(x)):
        xc[b, src[b]:src[b] + ln[b]] = torch_tensor(g.integers(0, IV, ln[b]))
    return xc


def torch_tensor(a):
    import torch

    return torch.tensor(a)


def att2_metric(z, x, mask):
    """Mean log-probability (nats) of the right next token at the repeat's positions."""
    import torch

    lp = torch.log_softmax(z[:, :-1], -1).gather(2, x[:, 1:, None])[..., 0]
    m = mask[:, :-1]
    return float(lp[m].mean())


def compute_induction():
    import copy

    import torch
    import torch.nn.functional as F

    from explainer.ai import novels as N
    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    C.threads()
    # 1. our two transformers, on text shown twice
    t13 = c13.load("tf")
    out = dict(tf_text1=float(np.mean(t13["text_bits1"][4:])), tf_text2=float(np.mean(t13["text_bits2"][4:])),
               tf_rand1=float(np.mean(t13["copy_bits1"][4:])), tf_rand2=float(np.mean(t13["copy_bits2"][4:])),
               tf_ind_max=float(np.max(t13["text_induction"])), tf_tokens=int(t13["tokens"]))
    nov = N.load_base()
    _, valid = N.token_arrays()
    _, W = acts.nov_windows(valid, 16, 60, 31)
    x2 = torch.cat([W, W], 1)
    with torch.no_grad():
        z = nov(x2)
    ce = F.cross_entropy(z[:, :-1].reshape(-1, z.shape[-1]), x2[:, 1:].reshape(-1), reduction="none").view(16, -1)
    ce = ce.numpy() / math.log(2)
    out["nov_text1"], out["nov_text2"] = float(ce[:, 4:59].mean()), float(ce[:, 64:].mean())
    out["nov_bits1"], out["nov_bits2"] = ce[:, :59].mean(0), ce[:, 60:].mean(0)
    import json

    nb = json.loads((N.OUT / "base.json").read_text())
    out["nov_tokens"] = int(nb["steps"] * nb["tokens_per_step"])
    # 2. Part 13's attention-only model on repeated random tokens, retrained here with its seed and recipe (the
    # weights and the training snapshots are kept, so the analysis can be redone without retraining)
    test_x, test_m, tsrc, tdst, tln = att2_batch(C.rng(99), 128)
    test_c = att2_corrupt(test_x, tsrc, tln, C.rng(98))
    S = C.steps(I_STEPS)
    wpath, spath = C.CACHE.dir / "att2.pt", C.CACHE.dir / "att2_train.pt"
    m = att2_build()
    if wpath.exists() and spath.exists() and torch.load(spath, weights_only=False).get("steps") == S:
        tr = torch.load(spath, weights_only=False)
        m.load_state_dict(torch.load(wpath))
        curve, snaps = tr["curve"], tr["snaps"]
    else:
        torch.manual_seed(2022)  # Olsson et al., In-context Learning and Induction Heads (2022)
        m = att2_build()
        opt = torch.optim.AdamW(m.parameters(), lr=3e-3, weight_decay=0.01)
        g = C.rng(2022)
        curve, snaps = [], []
        for step in range(S + 1):
            if step % 100 == 0:
                with torch.no_grad():
                    z = m(test_x)
                    ce = F.cross_entropy(z[:, :-1].reshape(-1, IV), test_x[:, 1:].reshape(-1), reduction="none")
                    ce = ce.view(len(test_x), IT - 1) / math.log(2)
                    mk = test_m[:, :-1]
                    curve.append((step, float(ce[mk].mean()), float(ce[~mk].mean())))
            if step % I_SNAP == 0:
                snaps.append((step, copy.deepcopy(m.state_dict())))
            if step == S:
                break
            x, _, _, _, _ = att2_batch(g, 64)
            loss = F.cross_entropy(m(x)[:, :-1].reshape(-1, IV), x[:, 1:].reshape(-1))
            opt.zero_grad()
            loss.backward()
            opt.step()
        torch.save(m.state_dict(), wpath)
        torch.save(dict(steps=S, curve=curve, snaps=snaps), spath)
    m.eval()
    out["curve"] = np.array(curve)
    out["steps"] = S

    def scores(mm):
        """Each layer-1 head's attention to the previous token and to itself; each layer-2 head's attention to the
        token after the earlier copy of the current one."""
        with torch.no_grad():
            _, r = mm(test_x, rec=True)
        P1, P2 = r["attn0"].numpy(), r["attn1"].numpy()
        prev = [float(np.mean([P1[:, h, i, i - 1] for i in range(1, IT)])) for h in range(IH)]
        self_ = [float(np.mean([P1[:, h, i, i] for i in range(IT)])) for h in range(IH)]
        ind = np.zeros(IH)
        cnt = 0
        for b in range(len(test_x)):
            for p_ in range(tdst[b], tdst[b] + tln[b] - 1):
                ind += P2[b, :, p_, tsrc[b] + (p_ - tdst[b]) + 1]
                cnt += 1
        return prev, self_, list(ind / cnt)

    prev, self_, ind = scores(m)
    prev_set = [h for h in range(IH) if prev[h] > 0.2] or [int(np.argmax(prev))]
    ind_set = [h for h in range(IH) if ind[h] > 0.3] or [int(np.argmax(ind))]
    self_head = int(np.argmax(self_))
    hp, hi = int(np.argmax(prev)), int(np.argmax(ind))
    out.update(prev_scores=prev, self_scores=self_, ind_scores=ind, prev_head=hp, ind_head=hi, prev_set=prev_set,
               ind_set=ind_set, self_head=self_head)

    def metric(z):
        return att2_metric(z, test_x, test_m)

    with torch.no_grad():
        zc, rc = m(test_x, rec=True)
        zx, rx = m(test_c, rec=True)
    m_clean, m_corr = metric(zc), metric(zx)
    out["m_clean"], out["m_corrupt"] = m_clean, m_corr
    out["chance"] = -math.log(IV)

    def frac_noise(z):  # damage: 0 = as clean, 1 = as corrupted
        return (m_clean - metric(z)) / (m_clean - m_corr)

    # head by head: each head's output from the corrupted run, into the clean one (noising)
    noise = np.zeros((2, IH))
    with torch.no_grad():
        for l_ in range(2):
            for h_ in range(IH):
                rep = rx[f"heads{l_}"][:, h_]
                noise[l_, h_] = frac_noise(m(test_x, patch={("head", l_, h_): (lambda o, rep=rep: rep)}))
    out["head_noise"] = noise
    # mean-ablation of each head (its output replaced by its average over the batch and positions)
    abl = np.zeros((2, IH))
    with torch.no_grad():
        for l_ in range(2):
            for h_ in range(IH):
                mu_ = rc[f"heads{l_}"][:, h_].mean((0, 1), keepdim=True)
                z = m(test_x, patch={("head", l_, h_): (lambda o, mu_=mu_: mu_.expand_as(o))})
                ce = F.cross_entropy(z[:, :-1].reshape(-1, IV), test_x[:, 1:].reshape(-1), reduction="none")
                abl[l_, h_] = float((ce.view(len(test_x), -1) / math.log(2))[test_m[:, :-1]].mean())
    out["ablate_bits"] = abl
    out["clean_bits"] = float(curve[-1][1])

    # path patching (noising): layer-1 heads' corrupted outputs sent only into the layer-2 heads' queries, keys or
    # values; from the previous-token heads together, from each alone, and from the current-token head
    def path(mm, rc_, rx_, heads, mc, mx):
        delta = sum(rx_["heads0"][:, h] - rc_["heads0"][:, h] for h in heads)
        res = {}
        for nm, sel in (("q", (1, 0, 0)), ("k", (0, 1, 0)), ("v", (0, 0, 1))):
            fn = (lambda h, sel=sel: tuple(h + delta if s_ else h for s_ in sel))
            with torch.no_grad():
                z = mm(test_x, patch={("kqv", 1, h2): fn for h2 in range(IH)})
            res[nm] = (mc - metric(z)) / (mc - mx)
        return res

    out["path_noise"] = path(m, rc, rx, prev_set, m_clean, m_corr)
    out["path_single"] = [path(m, rc, rx, [h], m_clean, m_corr)["k"] for h in prev_set]
    out["path_self"] = path(m, rc, rx, [self_head], m_clean, m_corr)
    # residual stream patching, noising: one target position of one example; the corrupted residual at one (layer,
    # position) put into the clean run; how much of the target's log-probability is lost
    ex = np.asarray(C.rng(7).integers(0, IV, IT))
    ex[60:80] = ex[10:30]
    exc = ex.copy()
    exc[10:30] = C.rng(8).integers(0, IV, 20)
    xe, xce = torch.tensor(ex)[None], torch.tensor(exc)[None]
    tgt = 70  # predicts token 71, a copy of token 21
    with torch.no_grad():
        ze, re_ = m(xe, rec=True)
        zce, rce = m(xce, rec=True)
    lp = lambda z: float(torch.log_softmax(z[0, tgt], -1)[ex[tgt + 1]])  # noqa: E731
    lc, lx = lp(ze), lp(zce)
    heat = np.zeros((3, IT))
    with torch.no_grad():
        for l_ in range(3):
            for j in range(tgt + 1):
                cr = rce[f"resid{l_}"]

                def fn(h, j=j, cr=cr):
                    h = h.clone()
                    h[:, j] = cr[:, j]
                    return h

                heat[l_, j] = (lc - lp(m(xe, patch={("resid", l_): fn}))) / (lc - lx)
    out.update(ex=ex, ex_corrupt=exc, target=tgt, heat=heat, lp_clean=lc, lp_corrupt=lx,
               ex_prev=re_["attn0"][0, hp].numpy(), ex_ind=re_["attn1"][0, hi].numpy(),
               ex_self=re_["attn0"][0, self_head].numpy())
    # composition scores against random heads
    mats = [m.mats(l_, h_) for l_ in range(2) for h_ in range(IH)]
    cs = c13.composition_scores(mats, 2, IH)
    out["comp_k"], out["comp_q"], out["comp_v"] = (cs[k][:IH, IH:] for k in ("k", "q", "v"))
    out["comp_base"], out["comp_base_sd"] = c13.composition_baseline(ID, ID // IH)
    # the induction heads' OV circuit, token to logit: does attending to token t raise the logit of t?
    E = m.emb.weight.detach().double().numpy()  # (V, D)
    U = m.out.weight.detach().double().numpy()  # (V, D)
    M = sum(U @ m.mats(1, h)[1] @ E.T for h in ind_set)  # (V out, V in), the induction heads together
    lam = np.linalg.eigvals(M)
    out["ov"] = M.astype(np.float32)
    out["ov_diag_top"] = float(np.mean(M.argmax(0) == np.arange(IV)))
    out["ov_copy_score"] = float(lam.real.sum() / np.abs(lam).sum())
    # the previous-token heads' QK circuit on positions: where does a query at position i look?
    Pz = m.pos.detach().double().numpy()
    offs = []
    for h in prev_set:
        qk0, _ = m.mats(0, h)
        S_ = Pz @ qk0 @ Pz.T
        offs.append([np.mean([S_[i, i - d] for i in range(d, IT)]) for d in range(0, 8)])
    out["qk_pos_offsets"] = np.mean(offs, 0)
    # through training: the K path's effect (previous-token heads into every layer-2 head's keys), and the scores
    kpath, sc_ind, sc_prev = [], [], []
    for st, sd in snaps:
        mm = att2_build()
        mm.load_state_dict(sd)
        mm.eval()
        with torch.no_grad():
            zc_, rc_ = mm(test_x, rec=True)
            zx_, rx_ = mm(test_c, rec=True)
        mc, mx = metric(zc_), metric(zx_)
        kp = path(mm, rc_, rx_, prev_set, mc, mx)["k"] * (mc - mx)  # in nats
        kpath.append((st, kp, mc - mx))
        p_, _, i_ = scores(mm)
        sc_prev.append(float(np.mean([p_[h] for h in prev_set])))
        sc_ind.append(float(np.mean([i_[h] for h in ind_set])))
    out["snap_steps"] = [s_ for s_, _ in snaps]
    out["snap_kpath"] = np.array(kpath)
    out["snap_ind"], out["snap_prev"] = sc_ind, sc_prev
    print(f"    our transformers: TF {out['tf_text1']:.2f} -> {out['tf_text2']:.2f} bits on repeated text, novels "
          f"{out['nov_text1']:.2f} -> {out['nov_text2']:.2f}; attention-only: repeat {curve[0][1]:.2f} -> "
          f"{curve[-1][1]:.2f} bits; previous-token heads {prev_set}, induction heads {ind_set}, current-token head "
          f"{self_head}; head noise {np.round(noise, 2).tolist()}; paths {out['path_noise']}; OV copy "
          f"{out['ov_copy_score']:.2f}", flush=True)
    return out


# ---------------------------------------------------------------------------
# The novels model: probes, lenses, a contrast vector, model diffing
# ---------------------------------------------------------------------------
def nov_quote_labels():
    """For every held-out token of the novels model: is the text inside a quotation once this token is read (an odd
    number of '"' since the paragraph began)?  And is the token itself a closing quotation mark?"""
    from explainer.ai import novels as N
    from videos.ai.ai30 import acts

    _, valid = N.token_arrays()
    strs = acts.token_strings(range(N.tokenizer().get_vocab_size()))
    lab = np.zeros(len(valid), bool)
    closing = np.zeros(len(valid), bool)
    inside = False
    for i, t in enumerate(valid):
        s = strs[int(t)]
        before = inside
        for ch in s:
            if ch == "\n":
                inside = False
            elif ch == '"':
                inside = not inside
        lab[i] = inside
        closing[i] = before and '"' in s and not inside
    return valid, lab, closing, strs


PROBE = dict(windows=160, T=128, skip=16, seeds=(0, 1, 2), steps=400, hidden=256)


def compute_probes():
    """Hewitt & Liang's question: does a probe find what the model knows, or learn the task itself?  For "inside a
    quotation", per layer of the novels model: a linear and an MLP probe, on the real labels and on a control task
    (each token type given a random label at the same rate), several seeds; then the linear probe's direction removed
    from the residual stream (amnesic probing, Elazar et al. 2021) against random directions."""
    import torch
    import torch.nn.functional as F

    from explainer.ai import novels as N
    from videos.ai.ai30 import acts

    C.threads()
    model = N.load_base()
    valid, lab, closing, strs = nov_quote_labels()
    nw = max(20, int(PROBE["windows"] * min(1.0, C.SCALE * 4)))
    starts, W = acts.nov_windows(valid, nw, PROBE["T"], 1919)
    hs, _ = acts.nov_resid(model, W)
    sk = PROBE["skip"]
    L = len(hs)
    H = torch.stack([h[:, sk:].reshape(-1, h.shape[-1]) for h in hs])  # (layers + 1, N, d)
    pos = (starts[:, None] + np.arange(sk, PROBE["T"])[None]).ravel()
    y = torch.tensor(lab[pos]).float()
    tok = W[:, sk:].reshape(-1)
    win = np.repeat(np.arange(nw), PROBE["T"] - sk)
    tr = torch.tensor(win < nw // 2)
    te = ~tr
    S = C.steps(PROBE["steps"])
    rate = float(y.mean())
    res = {k: np.zeros((len(PROBE["seeds"]), L)) for k in ("lin_task", "lin_ctrl", "mlp_task", "mlp_ctrl")}
    dirs = []
    for si, seed in enumerate(PROBE["seeds"]):
        g = np.random.Generator(np.random.PCG64(100 + seed))
        ctrl_of_type = g.random(N.tokenizer().get_vocab_size()) < rate  # the control task: a label per token type
        yc = torch.tensor(ctrl_of_type[tok.numpy()]).float()
        for l_ in range(L):
            Xl = H[l_]
            mu, sd = Xl[tr].mean(0), Xl[tr].std(0) + 1e-6
            Xn = (Xl - mu) / sd
            for kind in ("lin", "mlp"):
                for task, yy in (("task", y), ("ctrl", yc)):
                    torch.manual_seed(seed)
                    if kind == "lin":
                        net = torch.nn.Linear(Xn.shape[1], 1)
                    else:
                        net = torch.nn.Sequential(torch.nn.Linear(Xn.shape[1], PROBE["hidden"]), torch.nn.ReLU(),
                                                  torch.nn.Linear(PROBE["hidden"], 1))
                    opt = torch.optim.Adam(net.parameters(), lr=3e-3, weight_decay=1e-4)
                    Xt, yt = Xn[tr], yy[tr]
                    gg = torch.Generator().manual_seed(seed)
                    for _ in range(S):
                        i = torch.randint(0, len(Xt), (1024,), generator=gg)
                        loss = F.binary_cross_entropy_with_logits(net(Xt[i])[:, 0], yt[i])
                        opt.zero_grad()
                        loss.backward()
                        opt.step()
                    with torch.no_grad():
                        acc = float(((net(Xn[te])[:, 0] > 0).float() == yy[te]).float().mean())
                    res[f"{kind}_{task}"][si, l_] = acc
                    if kind == "lin" and task == "task" and si == 0:
                        dirs.append((net.weight[0] / sd).detach())  # the direction in the raw residual stream
    maj_task = float(max(y[te].mean(), 1 - y[te].mean()))
    best = int(np.argmax(res["lin_task"].mean(0)[1:-1]) + 1)  # the inner layer where the linear probe does best
    # amnesic probing at that layer: remove the probe's direction (and, as the control, random ones) from the
    # residual stream entering block best + 1, and measure the next-token loss on closing quotation marks
    yv = torch.tensor(valid[pos + 1].astype(np.int64))  # the next token of each probed position
    cl = torch.tensor(closing[pos + 1])
    hl = hs[best]

    def loss_with(u):
        with torch.no_grad():
            h = hl
            if u is not None:
                u_ = u / u.norm()
                h = h - (h @ u_)[..., None] * u_
            z = acts.nov_run_from(model, h, best)[:, sk:].reshape(-1, model.cfg.vocab)
            ce = F.cross_entropy(z, yv, reduction="none") / math.log(2)
        return float(ce[cl].mean()), float(ce.mean())

    base_cl, base_all = loss_with(None)
    probe_cl, probe_all = loss_with(dirs[best])
    gr = torch.Generator().manual_seed(77)
    rand = [loss_with(torch.randn(hl.shape[-1], generator=gr)) for _ in range(10)]
    out = dict(layers=L, n_train=int(tr.sum()), n_test=int(te.sum()), rate=rate, majority=maj_task, best=best,
               seeds=list(PROBE["seeds"]), steps=S, n_closing=int(cl.sum()),
               amnesic=dict(base_closing=base_cl, base_all=base_all, probe_closing=probe_cl, probe_all=probe_all,
                            rand_closing=[a for a, _ in rand], rand_all=[b for _, b in rand]))
    for k, v in res.items():
        out[k] = v
    out["sel_lin"] = res["lin_task"] - res["lin_ctrl"]
    out["sel_mlp"] = res["mlp_task"] - res["mlp_ctrl"]
    # an example: a paragraph with its labels and the best layer's probe output
    g0 = int(np.flatnonzero(np.array([strs[int(t)].count('"') for t in valid[pos[:2000]]]) > 0)[0])
    out["example_tokens"] = [strs[int(t)] for t in valid[pos[g0] - 6:pos[g0] + 30]]
    out["example_labels"] = lab[pos[g0] - 6:pos[g0] + 30].astype(int)
    print(f"    probes: linear task {np.round(res['lin_task'].mean(0), 3)}, control {np.round(res['lin_ctrl'].mean(0), 3)}; "
          f"MLP task {np.round(res['mlp_task'].mean(0), 3)}, control {np.round(res['mlp_ctrl'].mean(0), 3)}; best layer "
          f"{best}; amnesic: closing quotes {base_cl:.2f} -> {probe_cl:.2f} bits (random {np.mean([a for a, _ in rand]):.2f})",
          flush=True)
    return out


LENS = dict(train_windows=200, eval_windows=80, T=128, steps=300, batch=512, lr=1e-3)
LENS_PROMPT = "It was the best of times, it was the worst of times, it was the age of"


def compute_lens():
    """nostalgebraist's logit lens (2020) and Belrose et al.'s tuned lens (2023) on the novels model: each layer's
    residual stream read through the final norm and unembedding, as it is or after a learned affine translator."""
    import torch
    import torch.nn.functional as F

    from explainer.ai import novels as N
    from videos.ai.ai30 import acts

    C.threads()
    model = N.load_base()
    for p_ in model.parameters():
        p_.requires_grad_(False)
    train, valid = N.token_arrays()
    sc = min(1.0, C.SCALE * 4)
    _, Wtr = acts.nov_windows(train, max(16, int(LENS["train_windows"] * sc)), LENS["T"], 2020)
    _, Wev = acts.nov_windows(valid, max(8, int(LENS["eval_windows"] * sc)), LENS["T"], 2023)
    htr, _ = acts.nov_resid(model, Wtr)
    hev, zev = acts.nov_resid(model, Wev)
    L = len(htr) - 1
    flat = lambda h: h.reshape(-1, h.shape[-1])  # noqa: E731
    Htr = [flat(h) for h in htr]
    Hev = [flat(h) for h in hev]
    yev = Wev[:, 1:].reshape(-1)
    read = lambda h: model.head(model.norm(h))  # noqa: E731
    S = C.steps(LENS["steps"])

    def kl_bits(z_lens, z_final):
        lq = torch.log_softmax(z_lens, -1)
        lp = torch.log_softmax(z_final, -1)
        return (lp.exp() * (lp - lq)).sum(-1) / math.log(2)

    def stats(fn, l_):
        kls, ces, agree = [], [], []
        with torch.no_grad():
            for i in range(0, len(Hev[l_]), 4096):
                zl = read(fn(Hev[l_][i:i + 4096]))
                zf = read(Hev[L][i:i + 4096])
                kls.append(kl_bits(zl, zf))
                agree.append((zl.argmax(-1) == zf.argmax(-1)).float())
            zl = read(fn(hev[l_]))[:, :-1].reshape(-1, model.cfg.vocab)
            ce = float(F.cross_entropy(zl, yev)) / math.log(2)
        return float(torch.cat(kls).mean()), ce, float(torch.cat(agree).mean())

    out = dict(layers=L, steps=S, n_train=int(len(Htr[0])), n_eval=int(len(Hev[0])), prompt=LENS_PROMPT)
    logit, tuned, curves = [], [], []
    trans = []
    for l_ in range(L + 1):
        logit.append(stats(lambda h: h, l_))
        if l_ == L:
            tuned.append(logit[-1])
            trans.append(None)
            continue
        torch.manual_seed(l_)
        A = torch.nn.Linear(Htr[l_].shape[1], Htr[l_].shape[1])
        torch.nn.init.zeros_(A.weight)
        torch.nn.init.zeros_(A.bias)
        opt = torch.optim.Adam(A.parameters(), lr=LENS["lr"])
        g = torch.Generator().manual_seed(100 + l_)
        cur = []
        for s in range(S + 1):
            i = torch.randint(0, len(Htr[l_]), (LENS["batch"],), generator=g)
            h = Htr[l_][i]
            loss = kl_bits(read(h + A(h)), read(Htr[L][i])).mean()
            if s % 10 == 0:
                cur.append((s, float(loss)))
            if s == S:
                break
            opt.zero_grad()
            loss.backward()
            opt.step()
        A.requires_grad_(False)
        curves.append(cur)
        trans.append(A)
        tuned.append(stats(lambda h, A=A: h + A(h), l_))
        print(f"    layer {l_}: logit lens KL {logit[-1][0]:.2f} bits, tuned {tuned[-1][0]:.2f}; bits/token "
              f"{logit[-1][1]:.2f} vs {tuned[-1][1]:.2f}", flush=True)
    out["logit_kl"], out["logit_ce"], out["logit_agree"] = (np.array([r[i] for r in logit]) for i in range(3))
    out["tuned_kl"], out["tuned_ce"], out["tuned_agree"] = (np.array([r[i] for r in tuned]) for i in range(3))
    out["curves"] = np.array(curves)  # (layers, checkpoints, 2)
    # the prompt, read at every layer by both lenses: the top token at each position
    ids = torch.tensor([N.encode(LENS_PROMPT)])
    hp, _ = acts.nov_resid(model, ids)
    strs = acts.token_strings(ids[0])
    tl, tt, pl, pt = [], [], [], []
    with torch.no_grad():
        for l_ in range(L + 1):
            zl = torch.softmax(read(hp[l_])[0], -1)
            zt = torch.softmax(read(hp[l_] + trans[l_](hp[l_]))[0], -1) if trans[l_] is not None else zl
            tl.append(acts.token_strings(zl.argmax(-1)))
            tt.append(acts.token_strings(zt.argmax(-1)))
            pl.append(zl.max(-1).values.numpy())
            pt.append(zt.max(-1).values.numpy())
    out.update(prompt_tokens=strs, table_logit=tl, table_tuned=tt, p_logit=np.array(pl), p_tuned=np.array(pt))
    return out


# ---------------------------------------------------------------------------
MOOD = dict(layer=3, alphas=(-0.6, -0.3, 0.0, 0.3, 0.6), seeds=(1, 2, 3), n_new=40, topics=12)


def mood_words(text):
    from videos.ai.ai27 import compute as c27

    w = c27.WORD.findall(text.lower())
    pos = sum(x in c27.POSITIVE for x in w)
    neg = sum(x in c27.NEGATIVE for x in w)
    return pos, neg, len(w)


POS_ADJ = ("happy joyful glad cheerful bright beautiful lovely warm kind gentle sweet pleasant merry charming wonderful "
           "peaceful calm friendly sunny glorious splendid tender lively hopeful delighted").split()
NEG_ADJ = ("sad sorrowful dark dead afraid terrible horrible dreadful painful cruel miserable unhappy wretched angry "
           "gloomy lonely evil sick wicked ugly bitter ashamed guilty pale grim").split()
FRAMES = ("She felt {}.", "It was a {} day.", "He looked {}.", "The room was {}.", "Their faces were {}.",
          "The news was {}.", "I am so {}.", "What a {} evening it was.")


def compute_mood():
    """A contrast vector in the novels model, in the manner of contrastive activation addition (Rimsky et al. 2024)
    and persona vectors (Chen et al. 2025): the residual stream after block 3 at a cheerful word minus that at a
    gloomy one, in the same short frames (half the words to find it, half held out); tested as a monitor on held-out
    words and on real sentences of the novels; then added while the model writes, at five strengths, against a random
    direction of the same length: the mood of the text (cheerful minus gloomy words per hundred, by Part 27's lists)
    and its fluency (bits per token under the unsteered model)."""
    import torch
    import torch.nn.functional as F

    from explainer.ai import novels as N
    from videos.ai.ai27 import compute as c27
    from videos.ai.ai30 import acts

    C.threads()
    model = N.load_base()
    lay = MOOD["layer"]
    g = C.rng(2025)
    pos, neg = list(POS_ADJ), list(NEG_ADJ)
    g.shuffle(pos)
    g.shuffle(neg)
    h_ = len(pos) // 2

    def at_word(frame, w):
        """The residual stream at the word's last token."""
        pre = frame.split("{}")[0]
        ids = N.encode(pre + w)
        hs, _ = acts.nov_resid(model, torch.tensor([ids]))
        return hs[lay][0, -1]

    Ap = torch.stack([torch.stack([at_word(f, w) for f in FRAMES]).mean(0) for w in pos])
    An = torch.stack([torch.stack([at_word(f, w) for f in FRAMES]).mean(0) for w in neg])
    v = Ap[:h_].mean(0) - An[:h_].mean(0)
    u = v / v.norm()

    def auroc(a, b):
        a, b = np.asarray(a), np.asarray(b)
        return float(np.mean(a[:, None] > b[None, :]) + 0.5 * np.mean(a[:, None] == b[None, :]))

    au_words = auroc((Ap[h_:] @ u).numpy(), (An[h_:] @ u).numpy())
    # real sentences of the novels: cheerful (a word from the held-out half of the cheerful list, none gloomy) against
    # gloomy; the sentence's score is its largest projection over its tokens
    d = c27.load("data")
    sents = [s for s, _ in d["which_test"]] + [s for s, _ in d["which_train"]]
    hp, hn = set(pos[h_:]), set(neg[h_:])
    cs, gs = [], []
    for s in sents:
        w = set(c27.WORD.findall(s.lower()))
        if w & hp and not w & c27.NEGATIVE:
            cs.append(s)
        elif w & hn and not w & c27.POSITIVE:
            gs.append(s)
    n = min(len(cs), len(gs), max(40, int(300 * min(1.0, C.SCALE * 4))))
    g.shuffle(cs)
    g.shuffle(gs)
    cs, gs = cs[:n], gs[:n]

    def sent_score(s):
        hs, _ = acts.nov_resid(model, torch.tensor([N.encode(s)]))
        return float((hs[lay][0] @ u).max())

    pc, pg = np.array([sent_score(s) for s in cs]), np.array([sent_score(s) for s in gs])
    au_sent = auroc(pc, pg)
    _, valid = N.token_arrays()
    _, Wn = acts.nov_windows(valid, 16, 128, 5)
    hs, _ = acts.nov_resid(model, Wn)
    norm = float(hs[lay].norm(dim=-1).mean())
    gr = torch.Generator().manual_seed(11)
    rnd = torch.randn(u.shape[0], generator=gr)
    rnd = rnd / rnd.norm()

    def generate(prompt, vec, alpha, seed):
        gen = torch.Generator().manual_seed(seed)
        ids = N.encode(prompt)
        start = len(ids)
        with torch.no_grad():
            for _ in range(MOOD["n_new"]):
                x = torch.tensor([ids[-model.cfg.seq:]])
                h2 = model.emb(x)
                for li, b in enumerate(model.blocks):
                    h2 = b(h2)
                    if li == lay - 1:
                        h2 = h2 + alpha * norm * vec
                z = model.head(model.norm(h2))[0, -1] / 0.8
                ids.append(int(torch.multinomial(torch.softmax(z, -1), 1, generator=gen)))
        return ids[start:], N.decode(ids[start:])

    def fluency(prompt, new):
        p_ = N.encode(prompt)
        ids = p_ + list(new)
        with torch.no_grad():
            z = model(torch.tensor([ids[:-1]]))[0, len(p_) - 1:]
        return float(F.cross_entropy(z, torch.tensor(ids[len(p_):]))) / math.log(2)

    topics = c27.TOPICS[: MOOD["topics"]]
    prompts = [f"The {t}" for t in topics]
    out = dict(layer=lay, words_fit=pos[:h_] + neg[:h_], pos_test=pos[h_:], neg_test=neg[h_:], frames=list(FRAMES),
               auroc_words=au_words, auroc_sent=au_sent, proj_cheer=pc, proj_gloom=pg, n_sent=n,
               proj_pos=(Ap[h_:] @ u).numpy(), proj_neg=(An[h_:] @ u).numpy(), norm=norm, vnorm=float(v.norm()),
               alphas=list(MOOD["alphas"]), seeds=list(MOOD["seeds"]), topics=topics, n_new=MOOD["n_new"],
               cheer_example=cs[0], gloom_example=gs[0])
    for nm, vec in (("v", u), ("r", rnd)):
        for a in MOOD["alphas"]:
            if nm == "r" and a == 0.0:
                continue
            moods, flu, samples = [], [], []
            for pr in prompts:
                for sd in MOOD["seeds"]:
                    new, text = generate(pr, vec, a, sd)
                    p, ng, w = mood_words(text)
                    moods.append(100 * (p - ng) / max(w, 1))
                    flu.append(fluency(pr, new))
                    if sd == MOOD["seeds"][0] and len(samples) < 3:
                        samples.append(pr + text)
            out[f"{nm}_{a:g}_mood"] = moods
            out[f"{nm}_{a:g}_flu"] = flu
            out[f"{nm}_{a:g}_samples"] = samples
            print(f"    {nm} alpha {a:g}: mood {np.mean(moods):+.1f} per 100 words, fluency {np.mean(flu):.2f} bits/token",
                  flush=True)
    print(f"    mood vector: monitor AUROC {au_words:.3f} on held-out words, {au_sent:.3f} on {n} + {n} sentences",
          flush=True)
    return out


# ---------------------------------------------------------------------------
DIFF = dict(layers=(3, 5), F=1024, k=32, steps=2000, batch=1024, windows=150, T=128, chat=700, seed=0)


def compute_diffing():
    """Model diffing between the novels model and Part 27's fine-tune of it (SFT): a BatchTopK crosscoder reading
    both models' residual streams on the same tokens, novel text and chat transcripts, after block 3 and after block
    5; each latent's decoder norm in each model; and the activation-difference lens on novel text alone."""
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai27 import compute as c27
    from videos.ai.ai27 import post as P27
    from videos.ai.ai30 import acts, dicts

    C.threads()
    base = N.load_base()
    c27.load("sft")
    sft = c27._load_model("sft")
    _, valid = N.token_arrays()
    sc = min(1.0, C.SCALE * 4)
    _, Wn = acts.nov_windows(valid, max(16, int(DIFF["windows"] * sc)), DIFF["T"], 99)
    d = c27.load("data")
    g = C.rng(27)
    ex = [P27.chat(c27.which_q(s), t) for s, t in d["which_test"]]
    ex += [P27.chat(c27.line_q(t), s) for t, s in (d["line_train"][i] for i in g.choice(len(d["line_train"]), 300, False))]
    g.shuffle(ex)
    ex = ex[: max(40, int(DIFF["chat"] * sc))]
    strs = acts.token_strings(range(N.tokenizer().get_vocab_size()))
    tok_n = Wn[:, 4:].reshape(-1)
    tok_c = torch.tensor([t for ids in ex for t in ids])
    tokens = torch.cat([tok_n, tok_c]).numpy()
    tn = Wn.shape[1] - 4
    seg0 = np.concatenate([np.repeat(np.arange(len(Wn)) * tn, tn),
                           len(tok_n) + np.repeat(np.cumsum([0] + [len(e_) for e_ in ex[:-1]]), [len(e_) for e_ in ex])])

    def ctx(i, before=8):
        """The tokens up to position i of the combined stream, within its own window or transcript."""
        lo = max(i - before, int(seg0[i]))
        return "".join(strs[int(t)] for t in tokens[lo:i + 1])

    hb_all = acts.nov_resid(base, Wn)[0]
    hf_all = acts.nov_resid(sft, Wn)[0]
    hbc = [acts.nov_resid(base, torch.tensor([ids]))[0] for ids in ex]
    hfc = [acts.nov_resid(sft, torch.tensor([ids]))[0] for ids in ex]
    D_ = base.cfg.d
    out = dict(layers=list(DIFF["layers"]), F=DIFF["F"], k=DIFF["k"], n_chat=int(len(tok_c)), n_novel=int(len(tok_n)))
    for lay in DIFF["layers"]:
        hb_n, hf_n = (h[lay][:, 4:].reshape(-1, D_) for h in (hb_all, hf_all))
        hb_c = torch.cat([h[lay][0] for h in hbc])
        hf_c = torch.cat([h[lay][0] for h in hfc])
        src = torch.cat([torch.zeros(len(hb_n)), torch.ones(len(hb_c))]).bool()  # True: chat
        Hb, Hf = torch.cat([hb_n, hb_c]), torch.cat([hf_n, hf_c])
        sb = float(Hb.pow(2).sum(1).mean().sqrt()) / math.sqrt(D_)
        sf = float(Hf.pow(2).sum(1).mean().sqrt()) / math.sqrt(D_)
        X = torch.cat([Hb / sb, Hf / sf], 1)
        S = C.steps(DIFF["steps"])
        cc, rec = dicts.train(X, "batchtopk", DIFF["k"], F=DIFF["F"], steps=S, batch=DIFF["batch"], seed=DIFF["seed"])
        e = dicts.evaluate(cc, X)
        nb, nf = cc.Wd[:, :D_].norm(dim=1).numpy(), cc.Wd[:, D_:].norm(dim=1).numpy()
        rel = nf / (nb + nf)
        with torch.no_grad():
            f = dicts.encode(cc, X)
        alive = (f > 0).any(0).numpy()
        on_chat = (f[src] > 0).float().mean(0).numpy()
        on_novel = (f[~src] > 0).float().mean(0).numpy()

        def top_contexts(j, k=5):
            idx = torch.topk(f[:, j], k).indices.numpy()
            return [dict(text=ctx(int(i)), chat=bool(src[int(i)]), tok=strs[int(tokens[int(i)])]) for i in idx
                    if f[int(i), j] > 0]

        cos = (cc.Wd[:, :D_] * cc.Wd[:, D_:]).sum(1) / torch.tensor(nb * nf).clamp_min(1e-9)
        groups = dict(base_only=np.flatnonzero(alive & (rel < 0.1)), chat_only=np.flatnonzero(alive & (rel > 0.9)),
                      shared=np.flatnonzero(alive & (rel > 0.3) & (rel < 0.7)))
        # the latents that fire mostly on chat transcripts, whatever their decoders: the base model's or new?
        ratio = (on_chat + 1e-4) / (on_novel + 1e-4)
        chatty = [int(j) for j in np.argsort(-ratio) if alive[j] and on_chat[j] > 0.005][:6]
        show = {}
        for nm, idx in list(groups.items()) + [("chatty", np.array(chatty))]:
            order = idx if nm == "chatty" else idx[np.argsort(-(on_chat + on_novel)[idx])][:6]
            show[nm] = [dict(id=int(j), rel=float(rel[j]), on_chat=float(on_chat[j]), on_novel=float(on_novel[j]),
                             contexts=top_contexts(int(j))) for j in order]
        diff = (hf_n - hb_n).mean(0)
        with torch.no_grad():
            zl = base.head(base.norm(hb_n.mean(0) + diff)) - base.head(base.norm(hb_n.mean(0)))
        topd = torch.topk(zl, 12).indices.numpy()
        r_ = dict(fvu=e["fvu"], l0=e["l0"], dead=e["dead"], rel=rel, alive=alive.astype(int), on_chat=on_chat,
                  on_novel=on_novel, cos_dec=cos.numpy(), n_base_only=int(len(groups["base_only"])),
                  n_chat_only=int(len(groups["chat_only"])), n_shared=int(len(groups["shared"])), show=show,
                  diff_tokens=[strs[int(t)] for t in topd], diff_logits=zl[topd].numpy(), diff_norm=float(diff.norm()),
                  base_norm=float(hb_n.norm(dim=1).mean()), rel_lo=float(rel[alive > 0].min()),
                  rel_hi=float(rel[alive > 0].max()), curve=np.array(list(zip(rec["step"], rec["l0"], rec["fvu"]))),
                  steps=S)
        for k_, v_ in r_.items():
            out[f"{k_}_{lay}"] = v_
        print(f"    crosscoder after block {lay}: unexplained {e['fvu']:.3f}, L0 {e['l0']:.1f}, {e['dead']} dead; base-only "
              f"{r_['n_base_only']}, chat-only {r_['n_chat_only']}, shared {r_['n_shared']}; r from {r_['rel_lo']:.2f} to "
              f"{r_['rel_hi']:.2f}; diff lens {r_['diff_tokens'][:8]}", flush=True)
    # how far apart the two models' next-token predictions are, on novel text (bits per token)
    with torch.no_grad():
        zb, zf = base(Wn), sft(Wn)
        kl_n = float((torch.softmax(zf, -1) * (torch.log_softmax(zf, -1) - torch.log_softmax(zb, -1))).sum(-1).mean())
    out["kl_novel"] = kl_n / math.log(2)
    return out


# ---------------------------------------------------------------------------
# Transcoders and the attribution graph (Part 13's transformer)
# ---------------------------------------------------------------------------
CLT = dict(F=512, k=16, steps=2500, batch=1024, windows=600, seed=0)


def clt_data():
    """For every block of Part 13's transformer, its MLP's input (after the layer norm) and output, on held-out
    windows (positions 64 on), in float16; and each layer's scale (root mean square length)."""
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    model, chars, enc, data = C.tf_model()
    n = max(40, int(CLT["windows"] * min(1.0, C.SCALE * 4)))
    starts, W = acts.tf_windows(c13, data, n, 3030)
    R = acts.tf_collect(model, c13, W, keys=("mlp_in", "mlp_out"), layers=(0, 1, 2, 3), dtype=torch.float16)
    sc = {}
    for k_, v_ in R.items():
        sc[k_] = float(v_.float().pow(2).sum(1).mean().sqrt()) / math.sqrt(v_.shape[1])
    return R, sc, starts, W


class CLTModel:
    """A cross-layer transcoder: features at layer l read that layer's MLP input; each writes to the MLP outputs of
    layers l ... 3 through its own decoder for each (Ameisen et al. 2025).  TopK per layer.  Units: inputs and
    outputs divided by their layer's scale."""

    def __init__(self, enc, benc, dec, bdec, k):
        self.enc, self.benc, self.dec, self.bdec, self.k = enc, benc, dec, bdec, k

    def features(self, l_, u):
        import torch

        z = u @ self.enc[l_] + self.benc[l_]
        v, i = torch.topk(z, self.k, dim=-1)
        return torch.zeros_like(z).scatter(-1, i, torch.relu(v))

    def output(self, l_, feats):
        """The reconstruction of layer l_'s MLP output from the features of layers 0 ... l_."""
        y = self.bdec[l_]
        for s in range(l_ + 1):
            if (s, l_) in self.dec:
                y = y + feats[s] @ self.dec[(s, l_)]
        return y


def train_clt(R, sc, cross=True, log=print):
    import torch

    L = 4
    D = R[("mlp_in", 0)].shape[1]
    F_, k = CLT["F"], CLT["k"]
    g = torch.Generator().manual_seed(CLT["seed"])
    enc = [torch.nn.Parameter(torch.randn(D, F_, generator=g) / math.sqrt(D)) for _ in range(L)]
    benc = [torch.nn.Parameter(torch.zeros(F_)) for _ in range(L)]
    pairs = [(s, t) for t in range(L) for s in range(L) if s <= t and (cross or s == t)]
    dec = {p: torch.nn.Parameter(torch.randn(F_, D, generator=g) / math.sqrt(D) * (1.0 if p[0] == p[1] else 0.1))
           for p in pairs}
    bdec = [torch.nn.Parameter(R[("mlp_out", t)][:4096].float().mean(0) / sc[("mlp_out", t)]) for t in range(L)]
    params = enc + benc + list(dec.values()) + bdec
    opt = torch.optim.Adam(params, lr=1e-3)
    N_ = len(R[("mlp_in", 0)])
    var = [float(((R[("mlp_out", t)].float() / sc[("mlp_out", t)]) -
                  (R[("mlp_out", t)].float() / sc[("mlp_out", t)]).mean(0)).pow(2).sum(1).mean()) for t in range(L)]
    S = C.steps(CLT["steps"])
    cur = []
    model = CLTModel(enc, benc, dec, bdec, k)
    for s in range(S + 1):
        i = torch.randint(0, N_, (CLT["batch"],), generator=g)
        feats = [model.features(l_, R[("mlp_in", l_)][i].float() / sc[("mlp_in", l_)]) for l_ in range(L)]
        errs = []
        for t in range(L):
            y = R[("mlp_out", t)][i].float() / sc[("mlp_out", t)]
            errs.append(((model.output(t, feats) - y) ** 2).sum(1).mean())
        loss = sum(e / v for e, v in zip(errs, var))
        if s % 50 == 0:
            cur.append([s] + [float(e) / v for e, v in zip(errs, var)])
        if s == S:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        m = CLTModel([e.detach().clone() for e in enc], [b.detach().clone() for b in benc],
                     {p: d.detach().clone() for p, d in dec.items()}, [b.detach().clone() for b in bdec], k)
    if not cross:  # a per-layer transcoder: only its own layer's decoder is used
        m.dec = {p: d for p, d in m.dec.items() if p[0] == p[1]}
        for t in range(L):
            for s_ in range(t):
                m.dec[(s_, t)] = torch.zeros(F_, D)
    return m, np.array(cur)


def replacement_bits(model, clt, sc, X, c13):
    """Bits per character with every MLP replaced by the transcoder (features computed from the replacement run's
    own MLP inputs), and how often its top prediction agrees with the model's."""
    import torch
    import torch.nn.functional as F

    from videos.ai.ai30 import acts

    cos, sin = acts.tf_rope(c13, X.shape[1] - 1)
    tot = n = agree = 0.0
    with torch.no_grad():
        for i in range(0, len(X), 16):
            x, y = X[i:i + 16, :-1], X[i:i + 16, 1:]
            h = model.emb(x)
            feats = []
            for l_, b in enumerate(model.blocks):
                a, _, _ = b.attend(h, cos, sin, 1.0, None)
                h = h + b.o(a.transpose(1, 2).reshape(h.shape))
                feats.append(clt.features(l_, b.n2(h) / sc[("mlp_in", l_)]))
                h = h + clt.output(l_, feats) * sc[("mlp_out", l_)]
            z = model.out(model.nf(h))
            z0 = model(x)
            tot += float(F.cross_entropy(z[:, 64:].reshape(-1, z.shape[-1]), y[:, 64:].reshape(-1), reduction="sum"))
            agree += float((z[:, 64:].argmax(-1) == z0[:, 64:].argmax(-1)).float().sum())
            n += y[:, 64:].numel()
    return tot / n / math.log(2), agree / n


def compute_clt():
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    C.threads()
    model, chars, enc, data = C.tf_model()
    R, sc, starts, W = clt_data()
    part = C.CACHE.partial("clt", dict(CLT, steps=C.steps(CLT["steps"]), n=len(R[("mlp_in", 0)])))
    res = {}
    for nm, cross in (("plt", False), ("clt", True)):
        path = C.CACHE.dir / f"{nm}.pt"
        if nm in part and path.exists():
            st = torch.load(path, weights_only=False)
            m_ = CLTModel(st["enc"], st["benc"], st["dec"], st["bdec"], st["k"])
            res[nm] = (m_, np.array(part[nm]["curve"]))
            continue
        m_, cur = train_clt(R, sc, cross)
        torch.save(dict(enc=m_.enc, benc=m_.benc, dec=m_.dec, bdec=m_.bdec, k=m_.k, sc=sc), path)
        part[nm] = dict(curve=cur.tolist())
        res[nm] = (m_, cur)
    Xe = C.tf_eval_windows()
    clean = acts.tf_bits_with(model, c13, Xe, 0, None)
    out = dict(F=CLT["F"], k=CLT["k"], steps=C.steps(CLT["steps"]), n=int(len(R[("mlp_in", 0)])), bits_clean=clean,
               scales={f"{a}_{b}": v for (a, b), v in sc.items()})
    # bits with the MLPs mean-ablated (what a transcoder has to beat)
    mean_out = [R[("mlp_out", l_)].float().mean(0) for l_ in range(4)]
    cos_, sin_ = acts.tf_rope(c13, Xe.shape[1] - 1)
    tot = n = 0.0
    import torch.nn.functional as F

    with torch.no_grad():
        for i in range(0, len(Xe), 16):
            x, y = Xe[i:i + 16, :-1], Xe[i:i + 16, 1:]
            h = model.emb(x)
            for l_, b in enumerate(model.blocks):
                a, _, _ = b.attend(h, cos_, sin_, 1.0, None)
                h = h + b.o(a.transpose(1, 2).reshape(h.shape)) + mean_out[l_]
            z = model.out(model.nf(h))
            tot += float(F.cross_entropy(z[:, 64:].reshape(-1, z.shape[-1]), y[:, 64:].reshape(-1), reduction="sum"))
            n += y[:, 64:].numel()
    out["bits_mlp_mean"] = tot / n / math.log(2)
    for nm, (m_, cur) in res.items():
        out[f"{nm}_curve"] = cur
        bits, agree = replacement_bits(model, m_, sc, Xe, c13)
        out[f"{nm}_bits"], out[f"{nm}_agree"] = bits, agree
        fvu = []
        with torch.no_grad():
            idx = torch.arange(0, len(R[("mlp_in", 0)]), 7)
            feats = [m_.features(l_, R[("mlp_in", l_)][idx].float() / sc[("mlp_in", l_)]) for l_ in range(4)]
            for t in range(4):
                y = R[("mlp_out", t)][idx].float() / sc[("mlp_out", t)]
                fvu.append(float(((m_.output(t, feats) - y) ** 2).sum(1).mean() / ((y - y.mean(0)) ** 2).sum(1).mean()))
        out[f"{nm}_fvu"] = fvu
        print(f"    {nm}: unexplained per layer {np.round(fvu, 3)}, replacement bits {bits:.3f} (clean {clean:.3f}, MLPs "
              f"mean-ablated {out['bits_mlp_mean']:.3f}), top-1 agreement {agree:.2f}", flush=True)
    return out


GRAPH_PROMPT = 'Spade looked at the girl. "I don\'t know," she sai'


def compute_graph():
    """An attribution graph for one prediction of Part 13's transformer, from the cross-layer transcoder.  The local
    replacement model: the prompt's attention patterns and layer-norm scales frozen, every MLP replaced by the
    transcoder's features plus an error node per position and layer (so it reproduces the model exactly on this
    prompt); then everything from features to the logit is linear, and an edge is a source's activation times the
    gradient of the target's pre-activation with respect to it.  Pruned by influence; the strongest features then
    ablated in the real model, their measured effect against the graph's prediction."""
    import torch

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts

    C.threads()
    C.load("clt")
    model, chars, enc, data = C.tf_model()
    for p_ in model.parameters():
        p_.requires_grad_(False)
    st = torch.load(C.CACHE.dir / "clt.pt", weights_only=False)
    clt = CLTModel(st["enc"], st["benc"], st["dec"], st["bdec"], st["k"])
    sc = st["sc"]
    ids = enc(GRAPH_PROMPT)[None]
    T = ids.shape[1]
    cos, sin = acts.tf_rope(c13, T)
    # the clean run, recording what the local model freezes
    with torch.no_grad():
        recs, z0 = acts.tf_layers(model, ids, c13, keep_attn=True)
    tgt = int(z0[0, -1].argmax())
    prob = torch.softmax(z0[0, -1], -1)

    def ln_frozen(ln, x, ref):
        mu_ref = ref.mean(-1, keepdim=True)
        rstd = 1.0 / torch.sqrt(ref.var(-1, unbiased=False, keepdim=True) + ln.eps)
        return (x - x.mean(-1, keepdim=True)) * rstd * ln.weight + ln.bias, mu_ref

    with torch.no_grad():
        feats = [clt.features(l_, recs[l_]["mlp_in"] / sc[("mlp_in", l_)]) for l_ in range(4)]
        errs = [recs[l_]["mlp_out"] - clt.output(l_, feats) * sc[("mlp_out", l_)] for l_ in range(4)]

    def local(E, A, Er):
        """The local replacement model: embeddings E, feature activations A (one tensor per layer), errors Er."""
        h = E
        pre = []
        for l_, b in enumerate(model.blocks):
            x1, _ = ln_frozen(b.n1, h, recs[l_]["pre"])
            qkv = b.qkv(x1).view(1, T, 3, c13.HEADS, c13.DH).permute(2, 0, 3, 1, 4)
            v = qkv[2]
            a = recs[l_]["attn"] @ v
            h = h + b.o(a.transpose(1, 2).reshape(h.shape))
            u, _ = ln_frozen(b.n2, h, recs[l_]["mid"])
            pre.append((u / sc[("mlp_in", l_)]) @ clt.enc[l_] + clt.benc[l_])
            h = h + clt.output(l_, A) * sc[("mlp_out", l_)] + Er[l_]
        hf, _ = ln_frozen(model.nf, h, recs[-1]["post"])
        return model.out(hf)[0], pre

    E0 = model.emb(ids).detach()
    zl, _ = local(E0, feats, errs)
    exact = float((zl[-1] - z0[0, -1]).abs().max())
    # the nodes: every active feature (layer, position, id), every embedding (position), every error (layer, position)
    act = [(l_, p, int(j)) for l_ in range(4) for p in range(T) for j in torch.nonzero(feats[l_][0, p]).flatten()]
    nf_ = len(act)
    n_nodes = nf_ + T + 4 * T + 1  # features, embeddings, errors, the logit
    A_ = np.zeros((n_nodes, n_nodes))  # A_[target, source]: the edge

    def leaves():
        E = E0.clone().requires_grad_(True)
        A = [f.clone().requires_grad_(True) for f in feats]
        Er = [e.clone().requires_grad_(True) for e in errs]
        return E, A, Er

    def row(E, A, Er):
        r_ = np.zeros(n_nodes)
        for i, (l_, p, j) in enumerate(act):
            g_ = A[l_].grad
            r_[i] = float(g_[0, p, j] * feats[l_][0, p, j]) if g_ is not None else 0.0
        if E.grad is not None:
            r_[nf_:nf_ + T] = (E.grad * E0).sum(-1)[0].numpy()
        for l_ in range(4):
            if Er[l_].grad is not None:
                r_[nf_ + T + l_ * T: nf_ + T + (l_ + 1) * T] = (Er[l_].grad * errs[l_]).sum(-1)[0].numpy()
        return r_

    E, A, Er = leaves()
    zl, _ = local(E, A, Er)
    zl[-1, tgt].backward()
    A_[-1] = row(E, A, Er)
    for i, (l_, p, j) in enumerate(act):
        E, A, Er = leaves()
        _, pre = local(E, A, Er)
        pre[l_][0, p, j].backward()
        A_[i] = row(E, A, Er)
    # influence on the logit through every path (Ameisen et al.): normalize each target's incoming edges by their
    # absolute sum, then B = A + A^2 + ...
    An = np.abs(A_)
    An = An / np.maximum(An.sum(1, keepdims=True), 1e-12)
    B = np.linalg.inv(np.eye(n_nodes) - An) - np.eye(n_nodes)
    infl = B[-1]
    # the total (signed) effect of each feature on the logit, features linearized: G = d pre / d a
    Gm = np.zeros((nf_ + 1, nf_))
    for i, (l_, p, j) in enumerate(act):
        a_val = float(feats[l_][0, p, j])
        Gm[:, i] = A_[list(range(nf_)) + [n_nodes - 1], i] / max(a_val, 1e-12)
    Gff, Glf = Gm[:nf_], Gm[nf_]
    total = Glf @ np.linalg.inv(np.eye(nf_) - Gff)  # d logit / d a_s, through every feature path
    a_vals = np.array([float(feats[l_][0, p, j]) for l_, p, j in act])
    pred_ablate = -a_vals * total  # predicted change of the logit when the feature is switched off
    pred_direct = -A_[-1, :nf_]
    # the strongest features by influence, ablated in the real model (their decoders' contribution removed from the
    # MLP outputs at their position, everything else recomputed)
    order = np.argsort(-infl[:nf_])
    top = [int(i) for i in order[:16]]
    meas = []
    for i in top:
        l_, p, j = act[i]

        def run(i=i, l_=l_, p=p, j=j):
            h = model.emb(ids)
            for li, b in enumerate(model.blocks):
                a, _, _ = b.attend(h, cos, sin, 1.0, None)
                h = h + b.o(a.transpose(1, 2).reshape(h.shape))
                m_out = b.f2(torch.nn.functional.gelu(b.f1(b.n2(h))))
                if li >= l_:
                    m_out = m_out.clone()
                    m_out[0, p] -= feats[l_][0, p, j] * clt.dec[(l_, li)][j] * sc[("mlp_out", li)]
                h = h + m_out
            return model.out(model.nf(h))[0, -1]

        with torch.no_grad():
            meas.append(float(run()[tgt] - z0[0, -1, tgt]))
    meas = np.array(meas)
    corr = float(np.corrcoef(meas, pred_ablate[top])[0, 1]) if np.std(meas) > 0 else float("nan")
    # describe the graph's features: where each fires hardest on the transcoder's data
    R, sc2, starts, W = clt_data()
    va = data["valid"]
    labels = {}
    with torch.no_grad():
        for i in top[:12]:
            l_, p, j = act[i]
            u = R[("mlp_in", l_)].float() / sc[("mlp_in", l_)]
            fz = []
            for c0 in range(0, len(u), 16384):
                fz.append(clt.features(l_, u[c0:c0 + 16384])[:, j])
            fz = torch.cat(fz)
            tk = torch.topk(fz, 6).indices.numpy()
            T64 = W.shape[1] - 64
            ctx = []
            for q in tk:
                w_, off = divmod(int(q), T64)
                s_ = int(starts[w_]) + 64 + off
                ctx.append("".join(chars[int(c)] for c in va[s_ - 20:s_ + 2]))
            labels[i] = ctx
    nodes = [dict(layer=act[i][0], pos=act[i][1], id=act[i][2], act=float(a_vals[i]), infl=float(infl[i]),
                  direct=float(A_[-1, i]), pred=float(pred_ablate[i]), contexts=labels.get(i, [])) for i in top]
    # edges among the shown nodes and from the embeddings, for the picture
    show = top[:12]
    edges = [(int(a), int(b), float(A_[b, a])) for a in show for b in show + [n_nodes - 1] if a != b and
             abs(A_[b, a]) > 0]
    emb_edges = [(int(p), int(b), float(A_[b, nf_ + p])) for p in range(T) for b in show if abs(A_[b, nf_ + p]) > 0]
    err_logit = A_[-1, nf_ + T:nf_ + 5 * T].reshape(4, T)
    tot_in = A_[-1].sum()
    out = dict(prompt=GRAPH_PROMPT, target=chars[tgt], p_target=float(prob[tgt]), logit=float(z0[0, -1, tgt]),
               exact=exact, n_features=nf_, nodes=nodes, node_ids=top, logit_index=n_nodes - 1, n_pos=T, edges=edges, emb_edges=emb_edges, err_logit=err_logit,
               feat_logit=float(A_[-1, :nf_].sum()), emb_logit=float(A_[-1, nf_:nf_ + T].sum()),
               err_total=float(err_logit.sum()), sum_edges=float(tot_in), measured=meas, predicted=pred_ablate[top],
               predicted_direct=pred_direct[top], corr=corr, infl_share=float(infl[top[:12]].sum() / infl[:nf_].sum()),
               top_chars=[chars[int(i)] for i in torch.topk(prob, 5).indices], top_probs=torch.topk(prob, 5).values.numpy())
    print(f"    graph: '{GRAPH_PROMPT[-10:]}' -> {chars[tgt]!r} ({float(prob[tgt]):.0%}); {nf_} active features; exact "
          f"to {exact:.1e}; logit {out['logit']:.2f} = features {out['feat_logit']:.2f} + embeddings "
          f"{out['emb_logit']:.2f} + errors {out['err_total']:.2f} (+ biases); ablation vs prediction r = {corr:.2f}",
          flush=True)
    return out


# ---------------------------------------------------------------------------
DIS = dict(sizes=(16, 64, 256, 1024, 4096), draws=5, k_latents=(1, 8))


def tf_quote_labels(seq, chars):
    """Inside a quotation after each character (an odd number of '"' since the paragraph began)."""
    lab = np.zeros(len(seq), bool)
    inside = False
    q, nl = chars.index('"'), chars.index("\n")
    for i, c in enumerate(seq.tolist()):
        if c == nl:
            inside = False
        elif c == q:
            inside = not inside
        lab[i] = inside
    return lab


def compute_disagree():
    """Three disagreements, measured small: (1) do autoencoders trained from different seeds find the same latents?
    (2) sparse probing on autoencoder latents against a plain linear probe, from 16 to 4,096 examples, in and out of
    distribution; (3) an autoencoder on a randomly initialized copy of the transformer: do its latents look as clean?"""
    import torch
    import torch.nn.functional as F

    from videos.ai.ai13 import compute as c13
    from videos.ai.ai30 import acts, dicts

    C.threads()
    C.load("frontier")
    v = C.tf_vectors()
    X = v["X"]
    model, chars, enc, data = C.tf_model()
    out = {}
    # (1) seeds
    Ws = [C.load_dict(C.dict_dir() / f"topk_16_{s}.pt")[0].Wd.numpy() for s in (0, 1, 2)]
    best = [dicts.match(Ws[a], Ws[b]) for a, b in ((0, 1), (0, 2), (1, 2))]
    out["seed_best_cos"] = best[0]
    out["seed_share"] = [float(np.mean(b_ >= 0.7)) for b_ in best]
    Wl = [C.load_dict(C.dict_dir() / f"l1_2_{s}.pt")[0].Wd.numpy() for s in (0, 1)]
    out["seed_share_l1"] = float(np.mean(dicts.match(Wl[0], Wl[1]) >= 0.7))
    # (2) sparse probing on the novels model (where "inside a quotation" is decodable, chapter 2): a TopK
    # autoencoder on its residual stream after block 5, trained here; then a linear probe on all 256 numbers
    # against probes on the 1 or 8 latents that differ most between the classes, from 16 to 4,096 examples; tested
    # on held-out novel text and, out of distribution, inside Part 27's chat transcripts
    from explainer.ai import novels as N
    from videos.ai.ai27 import compute as c27
    from videos.ai.ai27 import post as P27

    nov = N.load_base()
    train_ids, valid_ids = N.token_arrays()
    lay = 5
    strs = acts.token_strings(range(N.tokenizer().get_vocab_size()))

    def quote_labels(ids):
        lab, inside = np.zeros(len(ids), bool), False
        for i, t in enumerate(ids):
            for ch in strs[int(t)]:
                if ch == "\n":
                    inside = False
                elif ch == '"':
                    inside = not inside
            if strs[int(t)].startswith("<|"):
                inside = False
            lab[i] = inside
        return lab

    def resid_of(Wt):
        hs, _ = acts.nov_resid(nov, Wt)
        return hs[lay][:, 8:].reshape(-1, nov.cfg.d)

    sc_ = min(1.0, C.SCALE * 4)
    st_tr, W_tr = acts.nov_windows(train_ids, max(30, int(400 * sc_)), 128, 4001)
    st_va, W_va = acts.nov_windows(valid_ids, max(20, int(160 * sc_)), 128, 4002)
    H_tr, H_va = resid_of(W_tr), resid_of(W_va)
    lab_tr = np.concatenate([quote_labels(train_ids[s:s + 128])[8:] for s in st_tr])
    lab_va = np.concatenate([quote_labels(valid_ids[s:s + 128])[8:] for s in st_va])
    dd = c27.load("data")
    chats = [P27.chat(c27.which_q(s_), t_) for s_, t_ in dd["which_test"] if '"' in s_][:300]
    H_ch = torch.cat([acts.nov_resid(nov, torch.tensor([ids]))[0][lay][0] for ids in chats])
    lab_ch = np.concatenate([quote_labels(ids) for ids in chats])
    mu_n = H_tr.mean(0)
    sg_n = float(((H_tr - mu_n) ** 2).sum(1).mean().sqrt()) / math.sqrt(H_tr.shape[1])
    Ztr, Zva, Zch = ((h - mu_n) / sg_n for h in (H_tr, H_va, H_ch))
    nsae, _ = dicts.train(Ztr, "topk", 32, F=1024, steps=C.steps(2000), batch=1024, seed=0)
    out["nov_sae_fvu"] = dicts.evaluate(nsae, Zva)["fvu"]
    y_tr, y_va, y_ch = (torch.tensor(l_).float() for l_ in (lab_tr, lab_va, lab_ch))
    with torch.no_grad():
        Fva, Fch = dicts.encode(nsae, Zva), dicts.encode(nsae, Zch)

    def fit(Z, yy, Zt_list, steps=300, l2=1e-3):
        mu, sd = Z.mean(0), Z.std(0) + 1e-6
        w = torch.zeros(Z.shape[1], requires_grad=True)
        b = torch.zeros(1, requires_grad=True)
        opt = torch.optim.LBFGS([w, b], lr=0.5, max_iter=steps)
        Zn = (Z - mu) / sd

        def closure():
            opt.zero_grad()
            loss = F.binary_cross_entropy_with_logits(Zn @ w + b, yy) + l2 * (w ** 2).sum()
            loss.backward()
            return loss

        opt.step(closure)
        with torch.no_grad():
            return [float((((((Zt - mu) / sd) @ w + b) > 0).float() == yt).float().mean()) for Zt, yt in Zt_list]

    res = {k: np.zeros((len(DIS["sizes"]), DIS["draws"], 2)) for k in ["raw"] + [f"sae{k}" for k in DIS["k_latents"]]}
    for si, n in enumerate(DIS["sizes"]):
        for dr in range(DIS["draws"]):
            gg = np.random.Generator(np.random.PCG64(1000 * si + dr))
            idx = torch.tensor(gg.choice(len(Ztr), min(n, len(Ztr)), replace=False))
            yy = y_tr[idx]
            if yy.min() == yy.max():
                yy = yy.clone()
                yy[0] = 1 - yy[0]
            res["raw"][si, dr] = fit(Ztr[idx], yy, [(Zva, y_va), (Zch, y_ch)])
            with torch.no_grad():
                Fi = dicts.encode(nsae, Ztr[idx])
            diff = (Fi[yy > 0.5].mean(0) - Fi[yy < 0.5].mean(0)).abs()
            for kk in DIS["k_latents"]:
                j = torch.topk(diff, kk).indices
                res[f"sae{kk}"][si, dr] = fit(Fi[:, j], yy, [(Fva[:, j], y_va), (Fch[:, j], y_ch)])
    for k_, val in res.items():
        out[f"probe_{k_}"] = val
    out["probe_sizes"] = list(DIS["sizes"])
    out["probe_layer"] = lay
    out["probe_majority"] = float(max(y_va.mean(), 1 - y_va.mean()))
    out["probe_majority_ood"] = float(max(y_ch.mean(), 1 - y_ch.mean()))
    out["n_probe_pool"], out["n_probe_test"], out["n_probe_ood"] = int(len(Ztr)), int(len(Zva)), int(len(Zch))
    sae, _ = C.load_dict(C.dict_dir() / "topk_16_0.pt")
    # (3) a random transformer
    torch.manual_seed(1)
    rnd = c13.build_tf(len(chars)).eval()
    W_ = v["windows"]
    Ar = acts.tf_collect(rnd, c13, W_, layers=(C.LAYER,))[("post", C.LAYER)]
    mur = Ar.mean(0)
    sr = float(((Ar - mur) ** 2).sum(1).mean().sqrt()) / math.sqrt(Ar.shape[1])
    Xr = (Ar - mur) / sr
    dr_, _ = dicts.train(Xr, "topk", 16, F=512, steps=C.steps(2000), batch=1024, seed=0)
    er = dicts.evaluate(dr_, Xr[:40000])
    vr = dict(v, X=Xr)
    fr = C.describe(dr_, vr)
    ft = C.describe(sae, v)
    out["random_fvu"] = er["fvu"]
    out["trained_fvu"] = dicts.evaluate(sae, X[:40000])["fvu"]
    out["random_purity"] = np.array([f["purity"] for f in fr])
    out["trained_purity"] = np.array([f["purity"] for f in ft])
    out["random_examples"] = [f for f in fr if f["purity"] >= 0.75][:2]
    print(f"    seeds: {np.round(out['seed_share'], 2)} of latents recur (cos >= 0.7); L1 {out['seed_share_l1']:.2f}; probes "
          f"raw {res['raw'][:, :, 0].mean(1).round(3)}, sae1 {res['sae1'][:, :, 0].mean(1).round(3)}; random model: "
          f"purity {out['random_purity'].mean():.2f} vs trained {out['trained_purity'].mean():.2f}", flush=True)
    return out


# ---------------------------------------------------------------------------
def compute_grok():
    import torch

    from videos.ai.ai30 import grok as G

    C.threads()
    S = C.steps(G.STEPS)
    model, hist, (x, y, tr, te) = G.train(C.CACHE.dir / "grok.ckpt", steps=S)
    an = G.analyse(model, x, y)
    keys = ["step", "train_loss", "test_loss", "train_acc", "test_acc", "restricted_loss", "excluded_loss",
            "weight_norm"]
    out = {k: np.array([h[k] for h in hist]) for k in keys}
    out["spectrum"] = np.array([h["spectrum"] for h in hist])
    out["key_final"] = hist[-1]["key"]
    B, _ = G.fourier_basis()
    # each number's position in the plane of the strongest frequency, at the stored moments
    k0 = hist[-1]["key"][0]
    snaps = [(h["step"], h["WE"].astype(np.float64)) for h in hist if "WE" in h]
    planes = []
    for st, WE in snaps:
        cvec = B[2 * k0 - 1] @ WE
        svec = B[2 * k0] @ WE
        Q, _ = np.linalg.qr(np.stack([cvec, svec], 1))
        planes.append(WE @ Q)
    out["plane_steps"] = [s for s, _ in snaps]
    out["planes"] = np.array(planes)  # (moments, p, 2)
    out["neuron_freq"], out["neuron_share"] = an["neuron_freq"], an["neuron_share"]
    # the logits explained by the key frequencies' waves, at the end
    L = an["L"]
    keep = G.restricted(L, hist[-1]["key"])
    out["fit_r2"] = float(1 - ((L - keep) ** 2).sum() / (L ** 2).sum())
    j = int(np.argmax(an["neuron_share"] * (an["neuron_freq"] == k0)))
    out["neuron"] = j
    out["neuron_act"] = an["act"][:, :, j].astype(np.float32)
    out.update(P=G.P, frac=G.FRAC, lr=G.LR, wd=G.WD, steps=S, n_train=int(len(tr)), n_test=int(len(te)))
    ta = out["train_acc"]
    va = out["test_acc"]
    out["t_memorized"] = int(out["step"][np.argmax(ta > 0.99)]) if (ta > 0.99).any() else -1
    out["t_grokked"] = int(out["step"][np.argmax(va > 0.99)]) if (va > 0.99).any() else -1
    print(f"    grok: memorized by {out['t_memorized']}, grokked by {out['t_grokked']}; key {out['key_final']}; "
          f"fit {out['fit_r2']:.3f}", flush=True)
    return out
