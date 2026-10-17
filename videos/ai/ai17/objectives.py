"""The RL objectives of 2024-25, side by side on Part 17's two-digit addition (the ``objectives`` item).

Every run starts from the same briefly supervised model and sees the same stream of questions. Variants:

    pg      group-relative policy gradient, one step per batch (what the RL chapter trains): the ratio is always 1
    grpo    GRPO as published: 4 updates per batch of samples, the ratio clipped to [1 - 0.2, 1 + 0.2], and a KL
            penalty to the starting model (the k3 estimator, weight 0.04)
    dr      Dr. GRPO: the advantage without the division by the group's spread, no KL
    dapo    DAPO: clip-higher (0.2 below, 0.28 above), no KL, and dynamic sampling: groups whose answers are all right
            or all wrong carry no signal, so they are dropped and more questions drawn
    gspo    GSPO: one ratio per answer (the geometric mean of its tokens' ratios), clipped as a whole
    dpo     DPO: no sampling during training; pairs (a right answer, a wrong one) drawn once from the starting model,
            and the Bradley-Terry loss on the log-ratio margin

Recorded every 20 steps: accuracy on 500 new questions, the entropy of the model's digits, and its KL from the start;
every step: the share of groups with no signal and the share of tokens the clip holds back. At the end, pass@k of the
GRPO model against the starting model, on the RL chapter's 200 questions.
"""

from __future__ import annotations

import copy
import math

import numpy as np


STEPS, G, Q = 300, 8, 32  # RL steps, answers per question, questions per step
DPO_LR, DPO_BETA = 2e-5, 0.1  # Adam ignores the loss scale, so DPO needs a far smaller step than the RL runs
VARIANTS = ("pg", "grpo", "dr", "dapo", "gspo", "dpo")


def sft_model():
    """Part 17's starting point, exactly: 400 supervised steps on two-digit addition."""
    import torch

    from videos.ai.ai17.compute import VOC, add_problems, encode, rng, tiny_gpt
    import torch.nn.functional as F

    torch.manual_seed(2025)
    m = tiny_gpt(VOC, 10, D=64, L=2, H=4)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3)
    g = rng(1)
    for _ in range(400):
        a, b = add_problems(g, 128)
        x = torch.tensor(encode(a, b, a + b))
        z = m(x[:, :-1])
        loss = F.cross_entropy(z[:, 5:].reshape(-1, VOC), x[:, 6:].reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
    return m


def sample(m, a, b, k=1, gen=None):
    """k answers per question (3 digits, least significant first): tokens, value, per-digit log-probabilities."""
    import torch

    from videos.ai.ai17.compute import DIG, encode

    x = torch.tensor(encode(a, b)).repeat_interleave(k, 0)
    lps = []
    with torch.no_grad():
        for _ in range(3):
            p = torch.softmax(m(x)[:, -1, :DIG], -1)
            c = torch.multinomial(p, 1, generator=gen)
            lps.append(torch.log(p.gather(1, c))[:, 0])
            x = torch.cat([x, c], 1)
    d = x[:, 6:9]
    return x, (d[:, 0] + 10 * d[:, 1] + 100 * d[:, 2]).numpy(), torch.stack(lps, 1)


def digit_logp(m, x):
    """Log-probabilities of the 3 answer digits in x under m, and the full digit distributions."""
    import torch

    from videos.ai.ai17.compute import DIG

    z = m(x[:, :-1])[:, 5:8, :DIG]
    lp = torch.log_softmax(z, -1)
    return lp.gather(2, x[:, 6:9, None])[..., 0], lp


def answer_dist(m, a, b):
    """The model's probability for every 3-digit answer (0 to 999) to each question: (questions, 1000)."""
    import torch

    from videos.ai.ai17.compute import encode

    vals = np.arange(1000)
    digits = np.stack([vals % 10, (vals // 10) % 10, vals // 100], 1)
    out = []
    with torch.no_grad():
        for ai, bi in zip(a, b):
            pre = np.repeat(encode(np.array([ai]), np.array([bi])), 1000, 0)
            x = torch.tensor(np.concatenate([pre, digits], 1))
            lp, _ = digit_logp(m, x)
            out.append(lp.sum(1).exp().numpy())
    return np.array(out)


def evaluate(m, ref, ta, tb, gen):
    """Accuracy (one try each), mean entropy of a digit (bits), and KL(model || start) per answer (bits)."""
    import torch


    x, val, _ = sample(m, ta, tb, gen=gen)
    with torch.no_grad():
        _, lp = digit_logp(m, x)
        _, lr_ = digit_logp(ref, x)
        p = lp.exp()
        ent = float(-(p * lp).sum(-1).mean()) / math.log(2)
        kl = float((p * (lp - lr_)).sum(-1).sum(-1).mean()) / math.log(2)
    return float((val == ta + tb).mean()), ent, kl


def run(variant, base, ta, tb):
    import torch

    from videos.ai.ai17.compute import add_problems, rng
    import torch.nn.functional as F

    torch.manual_seed(7)
    m, ref = copy.deepcopy(base), copy.deepcopy(base)
    ref.eval()
    opt = torch.optim.AdamW(m.parameters(), lr=DPO_LR if variant == "dpo" else 5e-4)
    g, gen, egen = rng(11), torch.Generator().manual_seed(3), torch.Generator().manual_seed(4)
    eps_lo, eps_hi = 0.2, (0.28 if variant == "dapo" else 0.2)
    mu = 1 if variant == "pg" else 4  # updates per batch of samples
    beta_kl = 0.04 if variant == "grpo" else 0.0
    curve, zero, clipped, drawn = [(0, *evaluate(m, ref, ta, tb, egen))], [], [], []
    dists = [answer_dist(m, ta[:6], tb[:6])] if variant == "grpo" else []  # how it learns: probability over answers
    pairs = None
    if variant == "dpo":  # preference pairs, drawn once from the starting model
        pa, pb = add_problems(rng(12), STEPS * Q * 2)
        win, lose = [], []
        for c0 in range(0, len(pa), 2048):
            a, b = pa[c0:c0 + 2048], pb[c0:c0 + 2048]
            x, val, _ = sample(base, a, b, k=G, gen=gen)
            ok = (val == np.repeat(a + b, G)).reshape(-1, G)
            xs = x.view(-1, G, x.shape[1])
            for i in range(len(a)):
                if ok[i].any() and not ok[i].all():
                    win.append(xs[i, int(np.argmax(ok[i]))])
                    lose.append(xs[i, int(np.argmin(ok[i]))])
        pairs = torch.stack(win), torch.stack(lose)
        hold = (pairs[0][-512:], pairs[1][-512:])  # held out: how the winners' and losers' log-probabilities move
        pairs = (pairs[0][:-512], pairs[1][:-512])
        with torch.no_grad():
            ref_w, ref_l = digit_logp(ref, pairs[0])[0].sum(1), digit_logp(ref, pairs[1])[0].sum(1)
            hw0, hl0 = digit_logp(ref, hold[0])[0].sum(1), digit_logp(ref, hold[1])[0].sum(1)
        moves = [(0, 0.0, 0.0)]
    for step in range(1, STEPS + 1):
        if variant == "dpo":
            i = torch.arange((step - 1) * Q, step * Q) % len(pairs[0])
            lw, ll = digit_logp(m, pairs[0][i])[0].sum(1), digit_logp(m, pairs[1][i])[0].sum(1)
            margin = DPO_BETA * ((lw - ref_w[i]) - (ll - ref_l[i]))
            loss = -F.logsigmoid(margin).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            zero.append(float("nan"))
            clipped.append(float("nan"))
        else:
            # draw questions; DAPO keeps drawing until it has Q groups that carry a signal (at most 4 rounds)
            xs, rs, olds, n_drawn, n_zero = [], [], [], 0, 0
            for _ in range(4 if variant == "dapo" else 1):
                a, b = add_problems(g, Q)
                x, val, lp_old = sample(m, a, b, k=G, gen=gen)
                r = (val == np.repeat(a + b, G)).astype(float).reshape(Q, G)
                n_drawn += Q
                flat = r.std(1) == 0
                n_zero += int(flat.sum())
                keep = ~flat if variant == "dapo" else np.ones(Q, bool)
                xs.append(x.view(Q, G, -1)[keep])
                rs.append(r[keep])
                olds.append(lp_old.view(Q, G, 3)[keep])
                if variant != "dapo" or sum(len(r_) for r_ in rs) >= Q:
                    break
            x = torch.cat(xs)[:Q].reshape(-1, xs[0].shape[-1])
            r = np.concatenate(rs)[:Q]
            lp_old = torch.cat(olds)[:Q].reshape(-1, 3)
            zero.append(n_zero / n_drawn)
            drawn.append(n_drawn)
            adv = r - r.mean(1, keepdims=True)
            if variant not in ("dr",):
                adv = adv / (r.std(1, keepdims=True) + 1e-6)
            A = torch.tensor(adv.reshape(-1), dtype=torch.float32)
            cl = []
            for _ in range(mu if len(r) else 0):  # if every group was all right or all wrong, nothing to learn
                lp, _ = digit_logp(m, x)
                if variant == "pg":  # the RL chapter's loss: the advantage times the answer's log-probability
                    cl.append(0.0)
                    loss = -(A * lp.sum(1)).mean()
                elif variant == "gspo":  # one ratio per answer: the geometric mean of its digits' ratios
                    ratio = torch.exp((lp - lp_old).mean(1))
                    obj = torch.minimum(ratio * A, ratio.clamp(1 - eps_lo, 1 + eps_hi) * A)
                    cl.append(float(((ratio < 1 - eps_lo) | (ratio > 1 + eps_hi)).float().mean()))
                    loss = -obj.mean()
                else:
                    ratio = torch.exp(lp - lp_old)
                    obj = torch.minimum(ratio * A[:, None], ratio.clamp(1 - eps_lo, 1 + eps_hi) * A[:, None])
                    cl.append(float(((ratio < 1 - eps_lo) | (ratio > 1 + eps_hi)).float().mean()))
                    loss = -obj.mean()
                    if beta_kl:
                        lr_ = digit_logp(ref, x)[0].detach()
                        k3 = torch.exp(lr_ - lp) - (lr_ - lp) - 1  # an unbiased, never negative estimate of KL
                        loss = loss + beta_kl * k3.mean()
                opt.zero_grad()
                loss.backward()
                opt.step()
            clipped.append(float(np.mean(cl)) if cl else 0.0)
        if step % 20 == 0:
            curve.append((step, *evaluate(m, ref, ta, tb, egen)))
            if variant == "grpo":
                dists.append(answer_dist(m, ta[:6], tb[:6]))
            if variant == "dpo":
                with torch.no_grad():
                    dw = float((digit_logp(m, hold[0])[0].sum(1) - hw0).mean()) / math.log(2)
                    dl = float((digit_logp(m, hold[1])[0].sum(1) - hl0).mean()) / math.log(2)
                moves.append((step, dw, dl))
            print(f"    {variant} step {step}: acc {curve[-1][1]:.1%}, entropy {curve[-1][2]:.3f} bits, "
                  f"KL {curve[-1][3]:.3f}, no-signal groups {np.nanmean(zero[-20:]):.0%}", flush=True)
    out = dict(curve=np.array(curve), zero=np.array(zero), clipped=np.array(clipped))
    if dists:
        out["dists"] = np.array(dists, dtype=np.float32)  # (evaluations, 6 questions, 1000 answers)
        out["dist_a"], out["dist_b"] = ta[:6], tb[:6]
    if drawn:
        out["drawn"] = np.array(drawn)
    if pairs is not None:
        out["n_pairs"] = len(pairs[0])
        out["moves"] = np.array(moves)  # step, change in log2 p(winner), change in log2 p(loser), held-out pairs
    return out, m


def pass_at_k(V, truth, ks):
    n = V.shape[1]
    c = (V == truth[:, None]).sum(1)

    def one(c_, k):
        return 1.0 if n - c_ < k else 1.0 - math.comb(n - c_, k) / math.comb(n, k)

    return [float(np.mean([one(int(ci), k) for ci in c])) for k in ks]


def compute_objectives():
    import torch

    from videos.ai.ai17.compute import add_problems, rng

    torch.set_num_threads(2)
    base = sft_model()
    ta, tb = add_problems(rng(77), 500)
    out = dict(steps=STEPS, G=G, Q=Q, variants=list(VARIANTS))
    models = {}
    for v in VARIANTS:
        res, models[v] = run(v, base, ta, tb)
        for k, val in res.items():
            out[f"{v}_{k}"] = val
    # does RL find new answers, or sharpen the ones the model could already find? pass@k before and after
    ks = [1, 2, 4, 8, 16, 32, 64, 128]
    a, b = ta[:200], tb[:200]
    gen = torch.Generator().manual_seed(9)
    for name, mm in (("base", base), ("grpo", models["grpo"]), ("pg", models["pg"])):
        _, val, _ = sample(mm, a, b, k=max(ks), gen=gen)
        out[f"passk_{name}"] = pass_at_k(val.reshape(len(a), -1), a + b, ks)
        print(f"    pass@k {name}: " + " ".join(f"{p:.2f}" for p in out[f"passk_{name}"]), flush=True)
    out["ks"] = ks
    acc = {v: float(out[f"{v}_curve"][-1][1]) for v in VARIANTS}
    assert all(acc[v] > float(out[f"{v}_curve"][0][1]) for v in VARIANTS if v != "dpo")  # DPO may not improve: see moves
    return out
