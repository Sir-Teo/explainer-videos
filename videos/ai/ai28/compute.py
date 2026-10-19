"""Precompute everything numerical in Part 28 of the AI series ("Reasoning").

    python -m videos.ai.ai28.compute              # everything missing
    python -m videos.ai.ai28.compute --force rl

Results are cached in ``.cache/ai28/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Every model here is a
tiny transformer trained on this machine.

Items:
    parity     the parity of n random bits (is the number of 1s odd?), for n = 4, 8 and 16: a two-layer transformer
               trained to answer at once, and the same trained to write the running parity first (a chain of thought);
               accuracy on new strings, and the training curves at n = 16
    rl         reinforcement learning with a verifiable reward: a model briefly trained on two-digit addition, then
               improved by GRPO (sample 8 answers per question, reward the right ones, compare within the group);
               accuracy along the way, and the model's samples before and after
    sampling   test-time compute from the same model before RL: pass@k (any of k samples right, with a checker) and
               majority voting over k samples, as k grows
    objectives (objectives.py) the same start trained by six RL objectives: plain group-relative policy gradient,
               GRPO with clipping and a KL penalty, Dr. GRPO, DAPO, GSPO and DPO; accuracy, entropy, KL from the start,
               groups with no signal, clipped tokens; pass@k before and after RL
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai28")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def tiny_gpt(vocab, T, D=64, L=2, H=4):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.n1, self.n2 = nn.LayerNorm(D), nn.LayerNorm(D)
            self.qkv = nn.Linear(D, 3 * D, bias=False)
            self.o = nn.Linear(D, D, bias=False)
            self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D))

        def forward(self, x):
            B, t, _ = x.shape
            q, k, v = self.qkv(self.n1(x)).view(B, t, 3, H, D // H).permute(2, 0, 3, 1, 4)
            a = F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, t, D)
            x = x + self.o(a)
            return x + self.mlp(self.n2(x))

    class GPT(nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = nn.Embedding(vocab, D)
            self.pos = nn.Parameter(torch.randn(T, D) * 0.02)
            self.blocks = nn.ModuleList([Block() for _ in range(L)])
            self.nf = nn.LayerNorm(D)
            self.out = nn.Linear(D, vocab)

        def forward(self, x):
            h = self.emb(x) + self.pos[: x.shape[1]]
            for b in self.blocks:
                h = b(h)
            return self.out(self.nf(h))

    return GPT()


# ---------------------------------------------------------------------------
def compute_parity():
    import torch
    import torch.nn.functional as F

    torch.set_num_threads(2)
    EQ = 2  # tokens: 0, 1, '='

    def batch(g, n, size, cot):
        bits = g.integers(0, 2, (size, n))
        run = np.cumsum(bits, 1) % 2
        if cot:  # the bits, '=', then the running parity, one bit at a time; the last one is the answer
            x = np.concatenate([bits, np.full((size, 1), EQ), run], 1)
            tgt_from = n  # predict every token after '='
        else:
            x = np.concatenate([bits, np.full((size, 1), EQ), run[:, -1:]], 1)
            tgt_from = n
        return torch.tensor(x), tgt_from, run[:, -1]

    def train(n, cot, steps=2500, log=False):
        torch.manual_seed(2022)  # Wei et al., chain-of-thought prompting
        m = tiny_gpt(3, 2 * n + 1)
        opt = torch.optim.AdamW(m.parameters(), lr=2e-3, weight_decay=0.01)
        g = rng(n * 10 + cot)
        curve = []
        test, tf, ans = batch(rng(999), n, 1000, cot)
        for step in range(1, steps + 1):
            x, tf_, _ = batch(g, n, 128, cot)
            z = m(x[:, :-1])
            loss = F.cross_entropy(z[:, tf_:].reshape(-1, 3), x[:, tf_ + 1:].reshape(-1))
            opt.zero_grad()
            loss.backward()
            opt.step()
            if log and (step % 100 == 0 or step == 1):
                curve.append((step, accuracy(m, test, n, cot, ans)))
        return accuracy(m, test, n, cot, ans), np.array(curve)

    def accuracy(m, test, n, cot, ans):
        with torch.no_grad():
            x = test[:, : n + 1]
            steps = n if cot else 1
            for _ in range(steps):  # greedy: write the chain (or just the answer)
                nxt = m(x)[:, -1, :2].argmax(-1, keepdim=True)
                x = torch.cat([x, nxt], 1)
            return float((x[:, -1].numpy() == ans).mean())

    out = dict(ns=[4, 8, 16])
    for n in out["ns"]:
        for cot in (0, 1):
            acc, curve = train(n, cot, log=(n == 16))
            out[f"acc_{'cot' if cot else 'direct'}{n}"] = acc
            if n == 16:
                out[f"curve_{'cot' if cot else 'direct'}"] = curve
            print(f"    n={n} {'chain' if cot else 'direct'}: {acc:.1%}", flush=True)
    assert out["acc_cot16"] > 0.95 and out["acc_direct16"] < 0.7
    return out


# ---------------------------------------------------------------------------
DIG = 10
PLUS, EQ, END = 10, 11, 12
VOC = 13


def add_problems(g, size):
    a, b = g.integers(10, 100, size), g.integers(10, 100, size)
    return a, b


def encode(a, b, ans=None):
    """'a+b=' then the answer's digits, least significant first, then END (a fixed 3-digit answer)."""
    rows = []
    for i in range(len(a)):
        r = [a[i] // 10, a[i] % 10, PLUS, b[i] // 10, b[i] % 10, EQ]
        if ans is not None:
            s = ans[i]
            r += [s % 10, (s // 10) % 10, s // 100, END]
        rows.append(r)
    return np.array(rows)


def compute_rl():
    import torch
    import torch.nn.functional as F

    torch.set_num_threads(2)
    torch.manual_seed(2025)  # DeepSeek-AI, DeepSeek-R1 (GRPO)
    m = tiny_gpt(VOC, 10, D=64, L=2, H=4)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3)
    g = rng(1)
    # a little supervised training: enough to be often right, not always
    for step in range(400):
        a, b = add_problems(g, 128)
        x = torch.tensor(encode(a, b, a + b))
        z = m(x[:, :-1])
        loss = F.cross_entropy(z[:, 5:].reshape(-1, VOC), x[:, 6:].reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
    ta, tb = add_problems(rng(77), 500)

    def sample(a, b, k=1, temp=1.0):
        x = torch.tensor(encode(a, b)).repeat_interleave(k, 0)
        logp = torch.zeros(len(x))
        for _ in range(3):
            z = m(x)[:, -1, :DIG] / temp
            p = torch.softmax(z, -1)
            c = torch.multinomial(p, 1)
            logp = logp + torch.log(p.gather(1, c))[:, 0]
            x = torch.cat([x, c], 1)
        d = x[:, 6:9]
        val = d[:, 0] + 10 * d[:, 1] + 100 * d[:, 2]
        return x, val, logp

    def acc():
        with torch.no_grad():
            _, val, _ = sample(ta, tb, temp=1.0)
            return float((val.numpy() == ta + tb).mean())

    before = acc()
    with torch.no_grad():
        _, vals_before, _ = sample(ta[:200], tb[:200], k=32)
    vals_before = vals_before.numpy().reshape(200, 32)
    # GRPO: for each question, 8 samples; advantage = (reward - group mean) / group std; push up the good ones
    curve = [(0, before)]
    opt = torch.optim.AdamW(m.parameters(), lr=5e-4)
    G = 8
    for step in range(1, 301):
        a, b = add_problems(g, 32)
        x, val, _ = sample(a, b, k=G)
        reward = (val.numpy() == np.repeat(a + b, G)).astype(float)
        r = reward.reshape(-1, G)
        adv = (r - r.mean(1, keepdims=True)) / (r.std(1, keepdims=True) + 1e-6)
        adv = torch.tensor(adv.reshape(-1), dtype=torch.float32)
        z = m(x[:, :-1])[:, 5:8, :DIG]
        lp = torch.log_softmax(z, -1).gather(2, x[:, 6:9, None])[..., 0].sum(1)
        loss = -(adv * lp).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 20 == 0:
            curve.append((step, acc()))
            print(f"    GRPO step {step}: {curve[-1][1]:.1%}", flush=True)
    after = acc()
    out = dict(before=before, after=after, curve=np.array(curve), G=G, sft_steps=400, rl_steps=300,
               vals_before=vals_before, truth=(ta[:200] + tb[:200]), ex_a=ta[:6], ex_b=tb[:6])
    with torch.no_grad():
        _, ex_vals, _ = sample(ta[:6], tb[:6], k=8)
    out["ex_after"] = ex_vals.numpy().reshape(6, 8)
    out["ex_before"] = vals_before[:6, :8]
    assert after > before + 0.15
    return out


def compute_sampling():
    r = load("rl")
    V, truth = np.asarray(r["vals_before"]), np.asarray(r["truth"])
    n = V.shape[1]
    right = (V == truth[:, None])
    c = right.sum(1)
    ks = [1, 2, 4, 8, 16, 32]

    def pass_at_k(c_, k):  # 1 - C(n - c, k) / C(n, k): the chance at least one of k samples is right
        if n - c_ < k:
            return 1.0
        return 1.0 - math.comb(n - c_, k) / math.comb(n, k)

    passk = [float(np.mean([pass_at_k(int(ci), k) for ci in c])) for k in ks]
    g = rng(5)
    maj = []
    for k in ks:
        hits = []
        for _ in range(20):
            idx = np.stack([g.choice(n, k, replace=False) for _ in range(len(V))])
            pick = np.take_along_axis(V, idx, 1)
            votes = [np.bincount(row, minlength=1000).argmax() for row in pick]
            hits.append(np.mean(np.array(votes) == truth))
        maj.append(float(np.mean(hits)))
    out = dict(ks=ks, passk=passk, majority=maj, n=n)
    assert passk[-1] > maj[-1] >= maj[0] - 0.02 and passk[0] == passk[0]
    return out


from videos.ai.ai28.objectives import compute_objectives  # noqa: E402

ITEMS = {
    "parity": compute_parity,
    "rl": compute_rl,
    "sampling": compute_sampling,
    "objectives": compute_objectives,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
