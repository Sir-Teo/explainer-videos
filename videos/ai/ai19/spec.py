"""Speculative decoding on the series' novels model: two drafters trained here, the sampling rule run for real, and
checks that it is exact.

Drafters:
    ``draft``  a separate small language model (2 layers, width 128, the same tokenizer), trained on the same novels
    ``eagle``  an EAGLE-style head (Li et al. 2024): one transformer block that reads the big model's own last hidden
               state and the next token's embedding, predicts the next hidden state, and reuses the big model's output
               head; it drafts by feeding its predictions back in

Both train resumably (a checkpoint every 50 steps in ``.cache/ai19/``), and their acceptance is measured as they
train: for held-out positions, the chance sum_x min(p(x), q(x)) that a drafted token survives the check.
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np

DRAFT_CFG = dict(d=128, layers=2, heads=4, seq=256)
DRAFT_RUN = dict(steps=600, batch=32, lr=4e-3, warmup=50, seed=0)
EAGLE_RUN = dict(steps=500, batch=16, lr=2e-3, warmup=40, seed=0, heads=4)
EVAL_EVERY = 50


# ---------------------------------------------------------------------------
# Training helpers
# ---------------------------------------------------------------------------
def lr_at(step, total, warm, peak, final=0.1):
    if step < warm:
        return peak * (step + 1) / warm
    t = (step - warm) / max(1, total - warm)
    return peak * (final + (1 - final) * 0.5 * (1 + math.cos(math.pi * t)))


def target_probs(base, windows):
    """The big model's next-token distributions at every position of the windows (float32, kept in memory)."""
    import torch

    with torch.inference_mode():
        return torch.cat([base(windows[i:i + 4, :-1]).softmax(-1) for i in range(0, len(windows), 4)])


def overlap(p, q) -> tuple[float, float]:
    """Mean over positions of sum_x min(p, q) (the acceptance chance when sampling) and of [argmax p = argmax q]
    (the acceptance when both decode greedily)."""
    import torch

    a = torch.minimum(p, q).sum(-1).mean().item()
    g = (p.argmax(-1) == q.argmax(-1)).float().mean().item()
    return float(a), float(g)


def _save(path: Path, obj):
    import torch

    tmp = path.with_suffix(".tmp")
    torch.save(obj, tmp)
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Drafter 1: a small model of its own
# ---------------------------------------------------------------------------
def draft_model():
    from explainer.lm import pocket

    return pocket.PocketGPT(pocket.Config(vocab=4096, **DRAFT_CFG))


def train_draft(cache_dir: Path, base, ev_windows, verbose=True) -> dict:
    """Train the small drafter on the novels (AdamW, cosine schedule), resumably; every EVAL_EVERY steps measure its
    acceptance against the big model on held-out windows.  Returns the curves and saves ``draft.pt``."""
    import torch
    import torch.nn.functional as F

    from explainer.ai import novels as N
    from explainer.lm import pocket

    R = DRAFT_RUN
    torch.manual_seed(R["seed"])
    model = draft_model()
    opts = pocket.make_optimizers(model, "adamw", R["lr"])
    tr, _ = N.token_arrays()
    data = pocket.TokenStream(tr, tr[:1000], DRAFT_CFG["seq"], seed=R["seed"])
    ck = cache_dir / "draft.ckpt"
    curve, evals, start, secs = [], [], 0, 0.0
    if ck.exists():
        st = torch.load(ck, weights_only=False)
        model.load_state_dict(st["model"])
        for o, s in zip(opts, st["opts"]):
            o.load_state_dict(s)
        data.rng.bit_generator.state = st["data_rng"]
        torch.set_rng_state(st["torch_rng"])
        curve, evals, start, secs = st["curve"], st["evals"], st["step"], st["seconds"]
        if verbose:
            print(f"    draft: resuming at step {start}", flush=True)
    P = target_probs(base, ev_windows)
    t0 = time.time() - secs

    def evaluate(step):
        model.eval()
        with torch.inference_mode():
            Q = torch.cat([model(ev_windows[i:i + 4, :-1]).softmax(-1) for i in range(0, len(ev_windows), 4)])
            ce = float(F.cross_entropy(torch.log(Q.clamp_min(1e-12)).reshape(-1, Q.shape[-1]),
                                       ev_windows[:, 1:].reshape(-1)))
        model.train()
        a, g = overlap(P, Q)
        evals.append([step, ce, a, g])
        if verbose:
            print(f"    draft step {step}: loss {ce:.3f}, acceptance {a:.3f} (greedy {g:.3f}), "
                  f"{time.time() - t0:.0f}s", flush=True)

    if start == 0:
        evaluate(0)
    model.train()
    for step in range(start, R["steps"]):
        if step > start and step % 50 == 0:
            _save(ck, {"model": model.state_dict(), "opts": [o.state_dict() for o in opts],
                       "data_rng": data.rng.bit_generator.state, "torch_rng": torch.get_rng_state(), "step": step,
                       "curve": curve, "evals": evals, "seconds": time.time() - t0})
        for o in opts:
            for gr in o.param_groups:
                gr["lr"] = lr_at(step, R["steps"], R["warmup"], R["lr"])
        x, y = data.batch(R["batch"])
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        for o in opts:
            o.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        for o in opts:
            o.step()
        if step % 10 == 0:
            curve.append([step, float(loss)])
        if (step + 1) % EVAL_EVERY == 0:
            evaluate(step + 1)
    model.eval()
    _save(cache_dir / "draft.pt", model.state_dict())
    ck.unlink(missing_ok=True)
    return dict(curve=curve, evals=evals, seconds=time.time() - t0, params=int(sum(p.numel() for p in model.parameters())),
                tokens=R["steps"] * R["batch"] * DRAFT_CFG["seq"])


def load_draft(cache_dir: Path):
    import torch

    m = draft_model()
    m.load_state_dict(torch.load(cache_dir / "draft.pt"))
    return m.eval()


# ---------------------------------------------------------------------------
# Drafter 2: an EAGLE-style head on the big model's features
# ---------------------------------------------------------------------------
def eagle_head(base):
    import torch
    import torch.nn as nn

    from explainer.lm import pocket

    d = base.cfg.d

    class Head(nn.Module):
        """Input at position i: the big model's hidden state h_i and the embedding of token x_(i+1); output: a
        prediction of h_(i+1), whose logits (through the big model's own norm and head) give x_(i+2)."""

        def __init__(self):
            super().__init__()
            self.fc = nn.Linear(2 * d, d, bias=False)
            cfg = pocket.Config(vocab=base.cfg.vocab, d=d, layers=1, heads=EAGLE_RUN["heads"], seq=base.cfg.seq + 16)
            self.block = pocket.Block(cfg)
            with torch.no_grad():  # start as "the next hidden state is like this one"
                self.fc.weight.zero_()
                self.fc.weight[:, :d].copy_(torch.eye(d))
                self.fc.weight[:, d:].normal_(std=0.02)

        def forward(self, h, nxt_emb):
            return self.block(self.fc(torch.cat([h, nxt_emb], -1)))

    return Head()


def base_hidden(base, x):
    """The big model's last hidden states (before the final norm) and logits for token windows x (B, T)."""
    h = base.emb(x)
    for b in base.blocks:
        h = b(h)
    return h


def train_eagle(cache_dir: Path, base, ev_windows, verbose=True) -> dict:
    """Train the head with the big model frozen: loss = cross-entropy of its token prediction (through the frozen
    head) + a smooth L1 pull of its (normalized) predicted feature toward the true one, as EAGLE does."""
    import torch
    import torch.nn.functional as F

    from explainer.ai import novels as N
    from explainer.lm import pocket

    R = EAGLE_RUN
    torch.manual_seed(R["seed"])
    for p in base.parameters():
        p.requires_grad_(False)
    head = eagle_head(base)
    opt = torch.optim.AdamW(head.parameters(), lr=R["lr"], betas=(0.9, 0.95), weight_decay=0.0)
    tr, _ = N.token_arrays()
    data = pocket.TokenStream(tr, tr[:1000], base.cfg.seq, seed=R["seed"] + 1)  # windows the base model can read
    ck = cache_dir / "eagle.ckpt"
    curve, evals, start, secs = [], [], 0, 0.0
    if ck.exists():
        st = torch.load(ck, weights_only=False)
        head.load_state_dict(st["model"])
        opt.load_state_dict(st["opt"])
        data.rng.bit_generator.state = st["data_rng"]
        torch.set_rng_state(st["torch_rng"])
        curve, evals, start, secs = st["curve"], st["evals"], st["step"], st["seconds"]
        if verbose:
            print(f"    eagle: resuming at step {start}", flush=True)
    t0 = time.time() - secs
    with torch.inference_mode():
        Hs = [base_hidden(base, ev_windows[i:i + 4, :-1]) for i in range(0, len(ev_windows), 4)]
        Hev = torch.cat(Hs)
        P = torch.cat([base.head(base.norm(h)).softmax(-1) for h in Hs])

    def predict(h, x):
        """Teacher-forced: from (h_i, x_(i+1)) for i < T-1, the distribution of x_(i+2)."""
        z = head(h[:, :-1], base.emb(x[:, 1:]))
        return z, base.head(base.norm(z))

    def evaluate(step):
        head.eval()
        with torch.inference_mode():
            Q = torch.cat([predict(Hev[i:i + 4], ev_windows[i:i + 4, :-1])[1].softmax(-1)
                           for i in range(0, len(ev_windows), 4)])
        head.train()
        a, g = overlap(P[:, 1:], Q)
        ce = float(F.cross_entropy(torch.log(Q.clamp_min(1e-12)).reshape(-1, Q.shape[-1]),
                                   ev_windows[:, 2:].reshape(-1)))
        evals.append([step, ce, a, g])
        if verbose:
            print(f"    eagle step {step}: loss {ce:.3f}, acceptance {a:.3f} (greedy {g:.3f}), "
                  f"{time.time() - t0:.0f}s", flush=True)

    if start == 0:
        evaluate(0)
    head.train()
    for step in range(start, R["steps"]):
        if step > start and step % 50 == 0:
            _save(ck, {"model": head.state_dict(), "opt": opt.state_dict(), "data_rng": data.rng.bit_generator.state,
                       "torch_rng": torch.get_rng_state(), "step": step, "curve": curve, "evals": evals,
                       "seconds": time.time() - t0})
        for gr in opt.param_groups:
            gr["lr"] = lr_at(step, R["steps"], R["warmup"], R["lr"])
        x, _ = data.batch(R["batch"])  # windows of seq tokens
        with torch.no_grad():
            h = base_hidden(base, x)
        z, logits = predict(h, x)
        ce = F.cross_entropy(logits[:, :-1].flatten(0, 1), x[:, 2:].flatten())
        reg = F.smooth_l1_loss(base.norm(z[:, :-1]), base.norm(h[:, 1:-1]).detach())
        loss = ce + reg
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(head.parameters(), 1.0)
        opt.step()
        if step % 10 == 0:
            curve.append([step, float(ce), float(reg)])
        if (step + 1) % EVAL_EVERY == 0:
            evaluate(step + 1)
    head.eval()
    _save(cache_dir / "eagle.pt", head.state_dict())
    ck.unlink(missing_ok=True)
    return dict(curve=curve, evals=evals, seconds=time.time() - t0,
                params=int(sum(p.numel() for p in head.parameters())),
                tokens=R["steps"] * R["batch"] * base.cfg.seq)


def load_eagle(cache_dir: Path, base):
    import torch

    h = eagle_head(base)
    h.load_state_dict(torch.load(cache_dir / "eagle.pt"))
    return h.eval()


# ---------------------------------------------------------------------------
# One transformer block, one step at a time, with its own cache (for the EAGLE head)
# ---------------------------------------------------------------------------
class BlockRunner:
    def __init__(self, block, d, heads, max_len):
        import torch

        self.b, self.H, self.dh, self.d = block, heads, d // heads, d
        self.k = torch.zeros(1, heads, max_len, self.dh)
        self.v = torch.zeros(1, heads, max_len, self.dh)
        self.len = 0
        inv = 1.0 / 10_000.0 ** (torch.arange(0, self.dh, 2).float() / self.dh)
        ang = torch.outer(torch.arange(max_len).float(), inv)
        self.cos, self.sin = ang.cos(), ang.sin()

    def rope(self, x, p0):
        import torch

        T = x.shape[-2]
        c, s = self.cos[p0:p0 + T], self.sin[p0:p0 + T]
        x1, x2 = x[..., ::2], x[..., 1::2]
        return torch.stack([x1 * c - x2 * s, x1 * s + x2 * c], dim=-1).flatten(-2)

    def __call__(self, x):
        import torch
        import torch.nn.functional as F

        B, T, _ = x.shape
        p0 = self.len
        a = self.b.attn
        q, k, v = a.qkv(self.b.n1(x)).view(B, T, 3, self.H, self.dh).permute(2, 0, 3, 1, 4)
        q, k = self.rope(q, p0), self.rope(k, p0)
        self.k[:, :, p0:p0 + T], self.v[:, :, p0:p0 + T] = k, v
        mask = (torch.arange(T)[:, None] + p0) >= torch.arange(p0 + T)[None, :] if T > 1 else None
        y = F.scaled_dot_product_attention(q, self.k[:, :, :p0 + T], self.v[:, :, :p0 + T], attn_mask=mask)
        x = x + a.out(y.transpose(1, 2).reshape(B, T, self.d))
        self.len = p0 + T
        return x + self.b.mlp(self.b.n2(x))


# ---------------------------------------------------------------------------
# Decoding: plain, and speculative with either drafter
# ---------------------------------------------------------------------------
def _sample(p, u):
    """Inverse-CDF sampling from probabilities ``p`` (numpy) with a uniform ``u``."""
    c = np.cumsum(p)
    return int(min(np.searchsorted(c, u * c[-1], side="right"), len(p) - 1))


class Decoder:
    """Generates from the novels model on the engine, plainly or speculatively.  Every random choice comes from one
    numpy generator, so a run is reproducible; times exclude nothing (drafting, checking, sampling)."""

    def __init__(self, base, draft=None, eagle=None, max_len=640):
        from videos.ai.ai19.engine import Engine

        self.base, self.draft, self.eagle = base, draft, eagle
        self.E = Engine(base, max_len=max_len)
        self.D = Engine(draft, max_len=max_len) if draft is not None else None
        self.max_len = max_len

    def probs(self, logits, temp):
        import torch

        if temp == 0:
            return torch.nn.functional.one_hot(logits.argmax(-1), logits.shape[-1]).double().numpy()
        return torch.softmax(logits.double() / temp, -1).numpy()

    def plain(self, prompt, n, temp=1.0, seed=0):
        import torch

        g = np.random.default_rng(seed)
        with torch.inference_mode():
            c = self.E.new_cache(1, self.max_len)
            z = self.E.forward(torch.tensor([prompt]), c, logits="last")[0]
            out = []
            for _ in range(n):
                tok = _sample(self.probs(z, temp), g.random())
                out.append(tok)
                z = self.E.forward(torch.tensor([[tok]]), c, logits="last")[0]
        return out

    def speculative(self, prompt, n, k, temp=1.0, seed=0, mode="draft"):
        """Draft k tokens, check them in one pass of the big model, keep the accepted ones and one more.  Returns
        (tokens, per-round records (drafted, accepted), per drafted position the overlap sum_x min(p, q))."""
        import torch

        g = np.random.default_rng(seed)
        E, base = self.E, self.base
        rounds, betas = [], []
        with torch.inference_mode():
            tc = E.new_cache(1, self.max_len)
            ctx = list(prompt)
            # the big model has read everything but the last token; its hidden states feed the EAGLE head
            hid = E.forward(torch.tensor([ctx[:-1]]), tc, logits="none")[0]
            if mode == "draft":
                dc = self.D.new_cache(1, self.max_len)
                self.D.forward(torch.tensor([ctx[:-1]]), dc, logits="none")
                pending = [ctx[-1]]  # tokens the drafter has yet to read
            else:
                # head entry i = (h_i, x_(i+1)) for every position the big model has read; the last one's output
                # predicts the feature of the newest token's position, whose logits give the first draft
                hr = BlockRunner(self.eagle.block, base.cfg.d, EAGLE_RUN["heads"], self.max_len)
                zz = hr(self.eagle.fc(torch.cat([hid[None], base.emb(torch.tensor([ctx[1:]]))], -1)))
                last_pred = zz[:, -1:]
            out = []
            while len(out) < n:
                # --- draft k tokens, keeping each q
                drafts, qs = [], []
                if mode == "draft":
                    z = self.D.forward(torch.tensor([pending]), dc, logits="last")[0]
                    base_len = dc.len
                    for i in range(k):
                        q = self.probs(z, temp)
                        tok = _sample(q, g.random())
                        drafts.append(tok)
                        qs.append(q)
                        if i < k - 1:
                            z = self.D.forward(torch.tensor([[tok]]), dc, logits="last")[0]
                else:  # feed the head its own predicted features
                    base_len = hr.len
                    zf = last_pred
                    for i in range(k):
                        q = self.probs(base.head(base.norm(zf))[0, -1], temp)
                        tok = _sample(q, g.random())
                        drafts.append(tok)
                        qs.append(q)
                        if i < k - 1:
                            zf = hr(self.eagle.fc(torch.cat([zf[:, -1:], base.emb(torch.tensor([[tok]]))], -1)))
                # --- check: the big model reads the last token and the drafts in one pass
                L0 = tc.len
                h = E.forward(torch.tensor([[ctx[-1]] + drafts]), tc, logits="none")
                ps = self.probs(base.head(base.norm(h))[0], temp)  # (k+1, V)
                acc = 0
                new = None
                for i in range(k):
                    p, q, x = ps[i], qs[i], drafts[i]
                    betas.append(float(np.minimum(p, q).sum()))
                    if g.random() * q[x] < p[x]:  # accept with probability min(1, p/q)
                        acc += 1
                        continue
                    r = np.maximum(p - q, 0)
                    new = _sample(r / r.sum() if r.sum() > 0 else p, g.random())
                    break
                if new is None:
                    new = _sample(ps[k], g.random())  # all accepted: a free token from the last position
                rounds.append((k, acc))
                emitted = drafts[:acc] + [new]
                out += emitted
                tc.len = L0 + 1 + acc  # keep the big model's cache for the last token and the accepted drafts
                hid_new = h[0, :1 + acc]
                ctx += emitted
                if mode == "draft":
                    dc.len = base_len + min(acc, k - 1)
                    pending = ([drafts[k - 1]] if acc == k else []) + [new]
                else:
                    hr.len = base_len
                    # true entries: (h of each newly confirmed position, the token after it)
                    nxt = torch.tensor([emitted])
                    zz = hr(self.eagle.fc(torch.cat([hid_new[None], base.emb(nxt)], -1)))
                    last_pred = zz[:, -1:]
                if len(ctx) >= self.max_len - k - 2:
                    break
        return out[:n], rounds, betas


# ---------------------------------------------------------------------------
# Exactness: the distribution of what speculative sampling writes
# ---------------------------------------------------------------------------
def joint_test(base, draft, ctx, N=60_000, seed=0):
    """At one context, the first two tokens written by (a) speculative sampling with a two-token draft, (b) plain
    sampling from the big model, (c) the shortcut that keeps every draft unchecked; each N times.  The exact joint
    distribution p(y1) p(y2 | y1) is known (the big model, evaluated wherever a sample went), so each method's total
    variation distance from it can be computed: (a) and (b) differ from it only by sampling noise, (c) does not."""
    import torch
    from collections import Counter

    from videos.ai.ai19.engine import Engine

    E, D = Engine(base, max_len=len(ctx) + 4), Engine(draft, max_len=len(ctx) + 4)
    with torch.inference_mode():
        ce, cd = E.new_cache(1), D.new_cache(1)
        zp = E.forward(torch.tensor([ctx]), ce, logits="last")[0]
        zq = D.forward(torch.tensor([ctx]), cd, logits="last")[0]
    L = len(ctx)
    P = {(): torch.softmax(zp.double(), -1).numpy()}
    Q = {(): torch.softmax(zq.double(), -1).numpy()}

    def dist(table, eng, cache, a):
        if (a,) not in table:
            with torch.inference_mode():
                cache.len = L
                z = eng.forward(torch.tensor([[a]]), cache, logits="last")[0]
            table[(a,)] = torch.softmax(z.double(), -1).numpy()
        return table[(a,)]

    cdf = {}

    def draw(key, arr, u):
        if key not in cdf:
            c = np.cumsum(arr)
            cdf[key] = c / c[-1]
        return int(min(np.searchsorted(cdf[key], u, side="right"), len(arr) - 1))

    def resid(a):
        key = ("r", a)
        if key not in cdf:
            p = P[a] if a == () else P[a]
            q = Q[a]
            r = np.maximum(p - q, 0)
            c = np.cumsum(r)
            cdf[key] = c / c[-1]
        return cdf[key]

    g = np.random.default_rng(seed)
    spec, direct, naive = Counter(), Counter(), Counter()
    for _ in range(N):
        u = g.random(8)
        x1 = draw(("q", ()), Q[()], u[0])
        q2 = dist(Q, D, cd, x1)
        x2 = draw(("q", (x1,)), q2, u[1])
        p1 = P[()]
        if u[2] * Q[()][x1] < p1[x1]:
            p2 = dist(P, E, ce, x1)
            if u[3] * q2[x2] < p2[x2]:
                y = (x1, x2)
            else:
                y = (x1, int(min(np.searchsorted(resid((x1,)), u[4], side="right"), len(p1) - 1)))
        else:
            y1 = int(min(np.searchsorted(resid(()), u[4], side="right"), len(p1) - 1))
            qz, pz = dist(Q, D, cd, y1), dist(P, E, ce, y1)
            z = draw(("q", (y1,)), qz, u[5])
            y2 = z if u[6] * qz[z] < pz[z] else int(min(np.searchsorted(resid((y1,)), u[7], side="right"),
                                                          len(p1) - 1))
            y = (y1, y2)
        spec[y] += 1
        a = draw(("p", ()), P[()], u[5])
        b = draw(("p", (a,)), dist(P, E, ce, a), u[6])
        direct[(a, b)] += 1
        naive[(x1, x2)] += 1

    def exact(pair):
        a, b = pair
        return P[()][a] * dist(P, E, ce, a)[b]

    def tv(cnt):
        obs = sum(abs(n / N - exact(k)) for k, n in cnt.items())
        mass = sum(exact(k) for k in cnt)
        return 0.5 * (obs + (1 - mass))

    def tv1(cnt):
        m = np.zeros(len(P[()]))
        for (a, _), n in cnt.items():
            m[a] += n / N
        return 0.5 * float(np.abs(m - P[()]).sum())

    top = sorted(set(spec) | set(direct), key=lambda k: -exact(k))[:8]
    q_joint = lambda k: Q[()][k[0]] * dist(Q, D, cd, k[0])[k[1]]  # noqa: E731
    return dict(N=N, tv_spec=tv(spec), tv_direct=tv(direct), tv_naive=tv(naive), tv1_spec=tv1(spec),
                tv1_direct=tv1(direct), tv1_naive=tv1(naive), top=[list(k) for k in top],
                p_top=[exact(k) for k in top], q_top=[q_joint(k) for k in top],
                spec_top=[spec[k] / N for k in top], direct_top=[direct[k] / N for k in top],
                naive_top=[naive[k] / N for k in top], n_prefixes=len(P) - 1)
