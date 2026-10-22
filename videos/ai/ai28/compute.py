"""Precompute everything numerical in Part 28 of the AI series ("Reasoning").

    python -m videos.ai.ai28.compute              # everything missing (about 1.5 hours of CPU, resumable)
    python -m videos.ai.ai28.compute --force rl

Results are cached in ``.cache/ai28/<name>.json`` (+ ``.npz``); trained weights and the finished sub-runs of the
long items in ``.cache/ai28/`` too, so an interrupted run resumes.  Every model here is a tiny transformer trained on
this machine, one or two CPU threads each; every run is seeded.

Three toy problems carry the part:

* **parity**: is the number of 1s among n bits odd?  (chapter 1)
* **two-digit addition**, answer only (``37+45=`` -> 82): reinforcement learning from a checker and its objectives,
  pass@k, the KL estimators, best-of-N.  The answers are three digits, so the model's probability of *every*
  answer can be computed exactly, and with it pass@k, KL divergences and best-of-N without sampling noise.
* **think or answer** (``think.py``): the sum of 2 to 10 digits; the model may answer at once or first write the
  running total, and may stop thinking at any point.  Length, overthinking, verifiers, search, budgets.

Items:
    parity     n = 4, 8, 16 bits: a two-layer transformer trained to answer at once, to answer after n filler
               tokens, and to write the running parity first (a chain of thought); three seeds at 16 bits; the
               training replayed (the chain it writes for three strings at each checkpoint)
    add_base   the addition model: 400 supervised steps (weights cached); its probability of every answer to the
               200 test questions
    rl         group-relative policy gradient on addition from that model, 3 seeds: accuracy as it trains, and its
               answers to six questions at every checkpoint (the replay)
    objectives (objectives.py) the same start trained by seven objectives, 3 seeds each: the plain group-relative
               gradient, GRPO, Dr. GRPO, DAPO, GSPO, CISPO and DPO; pass@k before and after, exactly, up to k = 1024
    sampling   pass@k from samples: the unbiased estimator against the naive one, and against the exact value
    kl_est     the k1, k2 and k3 estimators of KL(policy || start), against the exact KL, on a GRPO-trained model
    bon        best-of-N with a checker: accuracy, and its KL from the model against log N - (N - 1)/N
    think_*    (think.py) the think-or-answer model: see that module
"""

from __future__ import annotations

import json
import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai28")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def threads(n: int = 1):
    import torch

    torch.set_num_threads(n)


def memo(name: str, fn):
    """A finished sub-run of a long item, cached as JSON (+ npz) under .cache/ai28/runs/, so a restart resumes."""
    d = CACHE.dir / "runs"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{name}.json"
    if p.exists():
        out = json.loads(p.read_text())
        z = p.with_suffix(".npz")
        if z.exists():
            with np.load(z) as f:
                out.update({k: f[k] for k in f.files})
        return out
    out = fn()
    arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
    rest = {k: v for k, v in out.items() if k not in arrays}
    if arrays:
        np.savez_compressed(p.with_suffix(".tmp.npz"), **arrays)
        p.with_suffix(".tmp.npz").replace(p.with_suffix(".npz"))
    p.with_suffix(".tmp").write_text(json.dumps(rest, default=float))
    p.with_suffix(".tmp").replace(p)
    return out


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

        def hidden(self, x):
            h = self.emb(x) + self.pos[: x.shape[1]]
            for b in self.blocks:
                h = b(h)
            return self.nf(h)

        def forward(self, x):
            return self.out(self.hidden(x))

    return GPT()


# ---------------------------------------------------------------------------
# Parity
# ---------------------------------------------------------------------------
P_EQ, P_FILL = 2, 3  # tokens: 0, 1, '=', '.' (a filler)
PARITY_MODES = ("direct", "filler", "chain")
REPLAY_STRINGS = 3


def parity_batch(g, n, size, mode):
    """Rows of tokens and the positions whose next token is trained (or, at test time, generated)."""
    bits = g.integers(0, 2, (size, n))
    run = np.cumsum(bits, 1) % 2
    eq = np.full((size, 1), P_EQ)
    if mode == "chain":  # the bits, '=', then the running parity bit by bit: the last bit is the answer
        x = np.concatenate([bits, eq, run], 1)
    elif mode == "filler":  # the bits, '=', n dots (more positions to compute in, no more steps in a row), answer
        x = np.concatenate([bits, eq, np.full((size, n), P_FILL), run[:, -1:]], 1)
    else:
        x = np.concatenate([bits, eq, run[:, -1:]], 1)
    return x, run[:, -1]


def parity_train(n, mode, seed=0, steps=2500, log_every=100, replay=False):
    import torch
    import torch.nn.functional as F

    threads(1)
    torch.manual_seed(2022 + 7 * seed)  # 2022: Wei et al., chain-of-thought prompting
    T = 2 * n + 2
    m = tiny_gpt(4, T)
    opt = torch.optim.AdamW(m.parameters(), lr=2e-3, weight_decay=0.01)
    g = rng(1000 * seed + 10 * n + PARITY_MODES.index(mode))
    test, ans = parity_batch(rng(999), n, 1000, mode)
    test = torch.tensor(test)
    # which next tokens are trained: the chain (every position after '='), or only the final answer
    first = n if mode == "chain" else (T - 2 if mode == "filler" else n)

    @torch.no_grad()
    def generate(x0):
        x = x0[:, : n + 1]
        if mode == "filler":
            x = torch.cat([x, torch.full((len(x), n), P_FILL)], 1)
        for _ in range(n if mode == "chain" else 1):
            nxt = m(x)[:, -1, :2].argmax(-1, keepdim=True)
            x = torch.cat([x, nxt], 1)
        return x

    def accuracy():
        return float((generate(test)[:, -1].numpy() == ans).mean())

    curve, outs = [], []
    probe = test[:REPLAY_STRINGS]
    for step in range(0, steps + 1):
        if step % log_every == 0:
            curve.append((step, accuracy()))
            if replay:
                outs.append(generate(probe)[:, n + 1:].numpy() if mode == "chain" else generate(probe)[:, -1:].numpy())
        if step == steps:
            break
        x, _ = parity_batch(g, n, 128, mode)
        x = torch.tensor(x)
        z = m(x[:, :-1])
        loss = F.cross_entropy(z[:, first:].reshape(-1, 4), x[:, first + 1:].reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
    out = {"acc": curve[-1][1], "curve": np.array(curve)}
    if replay:
        out["replay"] = np.array(outs)
        out["probe"] = probe[:, :n].numpy()
    return out


def compute_parity(seeds16=3):
    out = dict(ns=[4, 8, 16], modes=list(PARITY_MODES), seeds=seeds16)
    for n in out["ns"]:
        for mode in PARITY_MODES:
            accs = []
            for s in range(seeds16 if n == 16 else 1):
                r = memo(f"parity_{n}_{mode}_{s}",
                         lambda: parity_train(n, mode, s, replay=(n == 16 and s == 0 and mode != "filler")))
                accs.append(float(r["acc"]))
                if n == 16:
                    out[f"curve_{mode}_{s}"] = np.asarray(r["curve"])
                    if "replay" in r:
                        out[f"replay_{mode}"] = np.asarray(r["replay"])
                        out["probe"] = np.asarray(r["probe"])
                print(f"    parity n={n} {mode} seed {s}: {accs[-1]:.1%}", flush=True)
            out[f"acc_{mode}{n}"] = float(np.mean(accs))
            out[f"accs_{mode}{n}"] = accs
    # the names the first chapter's scenes have always used
    for n in out["ns"]:
        out[f"acc_cot{n}"] = out[f"acc_chain{n}"]
    out["curve_cot"], out["curve_direct"] = out["curve_chain_0"], out["curve_direct_0"]
    return out


# ---------------------------------------------------------------------------
# Two-digit addition, answer only
# ---------------------------------------------------------------------------
DIG = 10
PLUS, EQ, END = 10, 11, 12
VOC = 13
N_TEST = 500  # accuracy is measured on 500 new questions; pass@k and the rest on the first 200


def add_problems(g, size):
    a, b = g.integers(10, 100, size), g.integers(10, 100, size)
    return a, b


def test_questions():
    return add_problems(rng(77), N_TEST)


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


def add_model():
    return tiny_gpt(VOC, 10, D=64, L=2, H=4)


def train_add_base():
    """The starting point of every addition experiment: 400 supervised steps, enough to be often right, not always."""
    import torch
    import torch.nn.functional as F

    torch.manual_seed(2025)  # DeepSeek-AI, DeepSeek-R1 (GRPO)
    m = add_model()
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


def base_model():
    """The cached starting model (trained once, then loaded)."""
    import torch

    p = CACHE.dir / "add_base.pt"
    if not p.exists():
        CACHE.dir.mkdir(parents=True, exist_ok=True)
        torch.save(train_add_base().state_dict(), p)
    m = add_model()
    m.load_state_dict(torch.load(p))
    return m.eval()


def answer_dist(m, a, b):
    """The model's probability for every 3-digit answer (0 to 999) to each question: (questions, 1000)."""
    import torch

    vals = np.arange(1000)
    digits = np.stack([vals % 10, (vals // 10) % 10, vals // 100], 1)
    out = []
    with torch.no_grad():
        for ai, bi in zip(a, b):
            pre = np.repeat(encode(np.array([ai]), np.array([bi])), 1000, 0)
            x = torch.tensor(np.concatenate([pre, digits], 1))
            lp = torch.log_softmax(m(x[:, :-1])[:, 5:8, :DIG], -1).gather(2, x[:, 6:9, None])[..., 0]
            out.append(lp.sum(1).exp().numpy())
    return np.array(out)


def sample_answers(m, a, b, k, gen=None, chunk=16384):
    """k sampled answers (values 0..999) per question: (questions, k)."""
    import torch

    q = np.repeat(np.arange(len(a)), k)
    out = np.zeros(len(q), int)
    with torch.no_grad():
        for c0 in range(0, len(q), chunk):
            idx = q[c0:c0 + chunk]
            x = torch.tensor(encode(a[idx], b[idx]))
            for _ in range(3):
                p = torch.softmax(m(x)[:, -1, :DIG], -1)
                x = torch.cat([x, torch.multinomial(p, 1, generator=gen)], 1)
            d = x[:, 6:9].numpy()
            out[c0:c0 + chunk] = d[:, 0] + 10 * d[:, 1] + 100 * d[:, 2]
    return out.reshape(len(a), k)


def exact_passk(p_right, ks):
    """pass@k exactly: 1 - (1 - p)^k per question, averaged."""
    p = np.asarray(p_right, float)
    return [float(np.mean(1 - (1 - p) ** k)) for k in ks]


def compute_add_base():
    threads(1)
    m = base_model()
    ta, tb = test_questions()
    a, b = ta[:200], tb[:200]
    D = answer_dist(m, a, b)
    return {"dist": D.astype(np.float32), "a": a, "b": b, "p_right": D[np.arange(200), a + b]}


def grpo_pg_run(seed, steps=300, G=8, Q=32, lr=5e-4, snap_every=20):
    """Chapter two's recipe: G answers per question, advantage (r - mean) / std within the group, one step on
    advantage x log-probability.  Accuracy every 20 steps; seed 0 also keeps its answers to six questions."""
    import torch

    threads(1)
    m = base_model()
    m.train()
    torch.manual_seed(100 + seed)
    gen = torch.Generator().manual_seed(200 + seed)
    egen = torch.Generator().manual_seed(4)
    opt = torch.optim.AdamW(m.parameters(), lr=lr)
    g = rng(300 + seed)
    ta, tb = test_questions()

    def acc():
        v = sample_answers(m, ta, tb, 1, gen=egen)[:, 0]
        return float((v == ta + tb).mean())

    curve, snaps = [(0, acc())], [sample_answers(m, ta[:6], tb[:6], 8, gen=egen)]
    for step in range(1, steps + 1):
        a, b = add_problems(g, Q)
        x = torch.tensor(encode(a, b)).repeat_interleave(G, 0)
        with torch.no_grad():
            for _ in range(3):
                p = torch.softmax(m(x)[:, -1, :DIG], -1)
                x = torch.cat([x, torch.multinomial(p, 1, generator=gen)], 1)
        d = x[:, 6:9].numpy()
        val = d[:, 0] + 10 * d[:, 1] + 100 * d[:, 2]
        r = (val == np.repeat(a + b, G)).astype(float).reshape(Q, G)
        adv = (r - r.mean(1, keepdims=True)) / (r.std(1, keepdims=True) + 1e-6)
        A = torch.tensor(adv.reshape(-1), dtype=torch.float32)
        lp = torch.log_softmax(m(x[:, :-1])[:, 5:8, :DIG], -1).gather(2, x[:, 6:9, None])[..., 0].sum(1)
        loss = -(A * lp).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % snap_every == 0:
            curve.append((step, acc()))
            if seed == 0:
                snaps.append(sample_answers(m, ta[:6], tb[:6], 8, gen=egen))
            print(f"    rl seed {seed} step {step}: {curve[-1][1]:.1%}", flush=True)
    out = {"curve": np.array(curve)}
    if seed == 0:
        out["snaps"] = np.array(snaps)
        import torch as _t

        _t.save(m.state_dict(), CACHE.dir / "add_rl.pt")
    return out


def compute_rl(seeds=3):
    threads(1)
    ta, tb = test_questions()
    runs = [memo(f"rl_seed{s}", lambda: grpo_pg_run(s)) for s in range(seeds)]
    C = np.stack([np.asarray(r["curve"]) for r in runs])  # (seeds, checkpoints, 2)
    snaps = np.asarray(runs[0]["snaps"])  # (checkpoints, 6, 8)
    m = base_model()
    import torch

    vals_before = sample_answers(m, ta[:200], tb[:200], 32, gen=torch.Generator().manual_seed(5))
    out = dict(G=8, Q=32, sft_steps=400, rl_steps=int(C[0, -1, 0]), seeds=seeds, curves=C, curve=C.mean(0),
               before=float(C[0, 0, 1]), after=float(C[:, -1, 1].mean()), after_seeds=C[:, -1, 1],
               snaps=snaps, snap_steps=C[0, :, 0], ex_a=ta[:6], ex_b=tb[:6], ex_before=snaps[0], ex_after=snaps[-1],
               vals_before=vals_before, truth=ta[:200] + tb[:200])
    return out


# ---------------------------------------------------------------------------
# pass@k from samples, the KL estimators, best-of-N
# ---------------------------------------------------------------------------
def compute_sampling(n=32, trials=400):
    """The unbiased pass@k estimator against the naive plug-in one, each from n samples per question, against the
    exact pass@k of the starting model (computed from its probability of the right answer)."""
    d = load("add_base")
    p = np.asarray(d["p_right"], float)
    ks = [1, 2, 4, 8, 16, 32]
    exact = exact_passk(p, ks)
    g = rng(31)
    unb, naive = np.zeros((trials, len(ks))), np.zeros((trials, len(ks)))
    for t in range(trials):
        c = g.binomial(n, p)  # right answers among n samples, per question
        for j, k in enumerate(ks):
            u = np.array([1.0 if n - ci < k else 1 - math.comb(n - ci, k) / math.comb(n, k) for ci in c])
            unb[t, j] = u.mean()
            naive[t, j] = np.mean(1 - (1 - c / n) ** k)
    # one question, many draws: the estimators' spread at k = 8
    qi = int(np.argsort(np.abs(p - 0.2))[0])
    c1 = g.binomial(n, p[qi], 4000)
    k = 8
    u1 = np.array([1.0 if n - ci < k else 1 - math.comb(n - ci, k) / math.comb(n, k) for ci in c1])
    n1 = 1 - (1 - c1 / n) ** k
    return dict(n=n, ks=ks, exact=exact, unbiased=unb.mean(0), unbiased_sd=unb.std(0), naive=naive.mean(0),
                naive_sd=naive.std(0), q=qi, q_p=float(p[qi]), q_exact=float(1 - (1 - p[qi]) ** k), q_k=k,
                q_unbiased=u1, q_naive=n1, trials=trials)


def compute_kl_est(n_samples=64):
    """KL(pi || start) estimated from samples y ~ pi with r = pi_start(y) / pi(y):
    k1 = -log r,  k2 = (log r)^2 / 2,  k3 = (r - 1) - log r  (Schulman 2020), against the exact KL per question."""
    import torch

    threads(1)
    d = load("add_base")
    a, b = np.asarray(d["a"]), np.asarray(d["b"])
    P0 = np.asarray(d["dist"], float)
    m = add_model()
    m.load_state_dict(torch.load(CACHE.dir / "add_rl.pt"))
    m.eval()
    P = answer_dist(m, a, b)
    eps = 1e-30
    exact = (P * (np.log(P + eps) - np.log(P0 + eps))).sum(1)  # nats, per question
    g = rng(41)
    est = {k: np.zeros((len(a), n_samples)) for k in ("k1", "k2", "k3")}
    for i in range(len(a)):
        p = P[i] / P[i].sum()
        y = g.choice(1000, n_samples, p=p)
        lr = np.log(P0[i, y] + eps) - np.log(P[i, y] + eps)
        est["k1"][i], est["k2"][i], est["k3"][i] = -lr, lr ** 2 / 2, np.expm1(lr) - lr
    out = dict(exact=exact, n=n_samples, mean_exact=float(exact.mean()))
    for k, v in est.items():
        out[f"{k}_mean"] = float(v.mean())  # over questions and samples: compare with the exact mean KL
        out[f"{k}_sd"] = float(v.std())  # the spread of a single sample's estimate
        out[f"{k}_neg"] = float((v < 0).mean())
        out[f"{k}_q"] = v.mean(1)  # per-question averages of 64 samples
        out[f"{k}_hist"] = v[:, :16].reshape(-1)  # some single-sample estimates, for the histogram
    return out


def compute_bon(Ns=(1, 2, 4, 8, 16, 32, 64, 128, 256)):
    """Best-of-N with the checker on the starting model: draw N answers, keep a right one if there is one (else a
    random wrong one).  With a 0/1 reward the best-of-N policy is pi_N(y) = pi(y) (1 - (1-p)^N) / p for a right
    answer, pi(y) (1-p)^(N-1) for a wrong one, so its KL from pi has a closed form, below log N - (N-1)/N."""
    d = load("add_base")
    P = np.asarray(d["dist"], float)
    P = P / P.sum(1, keepdims=True)
    p = np.asarray(d["p_right"], float) / np.asarray(d["dist"], float).sum(1)
    acc, kl, bound = [], [], []
    for N in Ns:
        w_right = (1 - (1 - p) ** N) / np.maximum(p, 1e-300)
        w_wrong = (1 - p) ** (N - 1)
        # KL = p * w_right * log w_right + (1 - p) * w_wrong * log w_wrong
        k = p * w_right * np.log(np.maximum(w_right, 1e-300)) + (1 - p) * w_wrong * np.log(np.maximum(w_wrong, 1e-300))
        acc.append(float(np.mean(1 - (1 - p) ** N)))
        kl.append(float(np.mean(k)))
        bound.append(math.log(N) - (N - 1) / N)
    return dict(Ns=list(Ns), acc=acc, kl=kl, bound=bound)


def compute_entropy_fit():
    """Cui et al. (2025) found accuracy R and policy entropy H related by R = -a exp(H) + b during RL.  Fit it to every
    checkpoint of every RL run in ``objectives`` (H in nats per digit; least squares, linear in a and b)."""
    o = load("objectives")
    H, R, V = [], [], []
    for v in o["variants"]:
        if v == "dpo":
            continue
        C_ = np.asarray(o[f"{v}_curves"])  # (seeds, checkpoints, 4): step, accuracy, entropy (bits), KL
        H.append(C_[:, :, 2].ravel() * math.log(2))  # nats: the law is written with e^H
        R.append(C_[:, :, 1].ravel())
        V += [v] * C_[:, :, 2].size
    H, R = np.concatenate(H), np.concatenate(R)
    X = np.stack([-np.exp(H), np.ones_like(H)], 1)
    (a, b), *_ = np.linalg.lstsq(X, R, rcond=None)
    pred = X @ np.array([a, b])
    r2 = 1 - float(((R - pred) ** 2).sum() / ((R - R.mean()) ** 2).sum())
    return dict(H=H, R=R, a=float(a), b=float(b), r2=r2, ceiling=float(b - a), variant=V)


def compute_passk_guess():
    """A checker-backed guesser: pass@k of guessing uniformly among the 199 possible sums of two two-digit numbers
    (20 to 198), 1 - (198/199)^k, at the k of the objectives item."""
    from videos.ai.ai28.objectives import KS

    m = 198 - 20 + 1
    return dict(ks=KS, m=m, passk=[1 - (1 - 1 / m) ** k for k in KS])


from videos.ai.ai28.objectives import compute_objectives  # noqa: E402
from videos.ai.ai28 import think  # noqa: E402

ITEMS = {
    "parity": compute_parity,
    "add_base": compute_add_base,
    "rl": compute_rl,
    "objectives": compute_objectives,
    "entropy_fit": compute_entropy_fit,
    "passk_guess": compute_passk_guess,
    "sampling": compute_sampling,
    "kl_est": compute_kl_est,
    "bon": compute_bon,
    **think.ITEMS,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
