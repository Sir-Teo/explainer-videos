"""Precompute every piece of real footage in the reinforcement-learning video.

    python -m videos.rl.compute                    # everything missing (about two CPU-hours on 4 cores)
    python -m videos.rl.compute simplex gauss      # specific items
    python -m videos.rl.compute --force runs       # recompute

Results are cached in ``.cache/rl/<name>.json`` (+ ``.npz`` for arrays); scenes call
``load(name)`` and never sample or train anything themselves.

Exact toys (NumPy, seconds)
    gauss       a 1-D Gaussian policy on a bumpy reward: samples, score-function arrows, REINFORCE paths
    cloud       a 2-D Gaussian policy: single-sample gradient estimates with and without a baseline
    simplex     a softmax policy over 3 actions: vanilla vs natural gradient flow, REINFORCE paths,
                variance as a function of the baseline, iso-KL contours, the tilted family
    kl_est      Schulman's three Monte-Carlo estimators of KL(q||p): bias and spread

A real miniature of RL post-training (PocketGPT, explainer/lm/pocket.py)
    base        pretrain a pocket transformer on 4-digit addition, where a quarter of the examples
                "show their work" (the sum written right-to-left first, then the answer)
    runs        RL from that model with a 0/1 reward: GRPO (the hero run), REINFORCE, RLOO,
                Dr. GRPO, DAPO-style clip-higher, PPO with a learned critic and GAE
    tree        the model's probability tree over whole answers to one prompt, before and during RL
    tilt        the KL-regularized optimum pi_ref * exp(r / beta) / Z of the base model, for every beta
    passk       pass@k (unbiased estimator, n = 128 samples) for the base model and the RL'd model
    critic      the learned value V(s_t) along real answers, TD errors, GAE for several lambda
    scaling     ScaleRL's sigmoid fitted to the RL runs' reward-vs-compute curves
A real reasoning model
    mismatch    Qwen3-0.6B: sample in bfloat16 (an "inference engine") and re-score the same tokens in
                float32 (a "trainer"): per-token and per-sequence importance ratios
"""

from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "rl"
RUN_DIR = DATA_DIR / "runs"


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"


_loaded: dict = {}


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"{p} missing: run `python -m videos.rl.compute {name}`")
        _loaded[name] = json.loads(p.read_text())
        npz = p.with_suffix(".npz")
        if npz.exists():
            with np.load(npz) as z:
                _loaded[name].update({k: z[k] for k in z.files})
    return _loaded[name]


def _save(name: str, out: dict) -> None:
    arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
    rest = {k: v for k, v in out.items() if k not in arrays}
    tmp = path(name).with_suffix(".tmp.json")
    tmp.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
    tmp.replace(path(name))
    if arrays:
        np.savez_compressed(path(name).with_suffix(".tmp.npz"), **arrays)
        path(name).with_suffix(".tmp.npz").replace(path(name).with_suffix(".npz"))


# ---------------------------------------------------------------------------
# Exact toys
# ---------------------------------------------------------------------------
def gauss_reward(a):
    """A bumpy 1-D reward landscape: a tall peak at a = 2, a smaller one at a = -2.2."""
    a = np.asarray(a, float)
    return 1.0 * np.exp(-((a - 2.0) ** 2) / 0.9) + 0.45 * np.exp(-((a + 2.2) ** 2) / 0.5)


def compute_gauss():
    """Policy a ~ N(mu, 1).  Score: d/dmu log p(a) = (a - mu).  Exact gradient by quadrature;
    a fixed batch of 10 samples for the arrows; REINFORCE paths of mu with and without a baseline."""
    rng = np.random.default_rng(3)
    mu0, sigma = -0.3, 1.0
    xs = np.linspace(-5, 5, 2001)
    dens = np.exp(-((xs - mu0) ** 2) / (2 * sigma**2)) / np.sqrt(2 * np.pi * sigma**2)
    r = gauss_reward(xs)
    J = float(np.trapezoid(dens * r, xs))
    grad = float(np.trapezoid(dens * r * (xs - mu0) / sigma**2, xs))
    samples = np.sort(rng.normal(mu0, sigma, 10))
    # exact J(mu) and dJ/dmu over a range of mu (the landscape the policy climbs)
    mus = np.linspace(-4, 4, 401)
    Jmu = np.array([np.trapezoid(np.exp(-((xs - m) ** 2) / 2) / np.sqrt(2 * np.pi) * r, xs) for m in mus])

    def path_(baseline: bool, seed: int, steps=60, lr=0.6, n=8, offset=0.0):
        g = np.random.default_rng(seed)
        mu, out = mu0, [mu0]
        for _ in range(steps):
            a = g.normal(mu, sigma, n)
            R = gauss_reward(a) + offset
            b = R.mean() if baseline else 0.0
            mu += lr * float(np.mean((R - b) * (a - mu) / sigma**2))
            out.append(mu)
        return out

    paths_nb = [path_(False, s, offset=2.0) for s in range(6)]
    paths_b = [path_(True, s, offset=2.0) for s in range(6)]
    return dict(mu0=mu0, sigma=sigma, J=J, grad=grad, samples=samples, sample_r=gauss_reward(samples),
                mus=mus, Jmu=Jmu, paths_nb=np.array(paths_nb), paths_b=np.array(paths_b), offset=2.0)


def cloud_reward(p):
    p = np.atleast_2d(p)
    return 2.0 * (np.exp(-np.sum((p - [1.6, 0.9]) ** 2, -1) / 1.2)
                  + 0.6 * np.exp(-np.sum((p - [-1.8, -1.2]) ** 2, -1) / 0.8))


CLOUD_MU = np.array([0.2, 0.0])
CLOUD_OFFSET = 2.0
CLOUD_BATCH = 16


def compute_cloud():
    """2-D Gaussian policy a ~ N(mu, I) on a reward surface plus a constant offset.  One sample gives the
    gradient estimate (R(a) - b)(a - mu).  We keep 12 single samples (for arrows) and 300 estimates that each
    average a batch of 16 samples, with b = 0 and with b = E[R]; plus the variance as a function of b."""
    rng = np.random.default_rng(7)
    mu, offset, n = CLOUD_MU, CLOUD_OFFSET, CLOUD_BATCH
    big = rng.normal(size=(400_000, 2)) + mu
    Rbig = cloud_reward(big) + offset
    true = (Rbig[:, None] * (big - mu)).mean(0)
    Rmean = float(Rbig.mean())
    a = rng.normal(size=(300, n, 2)) + mu
    R = cloud_reward(a.reshape(-1, 2)).reshape(300, n) + offset
    est_nb = (R[..., None] * (a - mu)).mean(1)
    est_b = ((R - Rmean)[..., None] * (a - mu)).mean(1)
    singles = rng.normal(size=(12, 2)) + mu
    g2 = np.sum((big - mu) ** 2, -1)
    bstar = float(np.mean(Rbig * g2) / np.mean(g2))
    bs = np.linspace(0, 4.5, 181)
    var = np.array([np.mean(np.sum(((Rbig - b)[:, None] * (big - mu)) ** 2, -1)) - np.sum(true**2) for b in bs])
    gx = np.linspace(-4, 4, 161)
    G = np.stack(np.meshgrid(gx, gx), -1).reshape(-1, 2)
    surf = cloud_reward(G).reshape(len(gx), len(gx))
    return dict(mu=mu, offset=offset, batch=n, true=true, Rmean=Rmean, est_nb=est_nb, est_b=est_b,
                singles=singles, singles_R=cloud_reward(singles) + offset, bstar=bstar, bs=bs, var=var, grid=gx,
                surf=surf, var_nb=float(np.interp(0.0, bs, var)), var_mean=float(np.interp(Rmean, bs, var)),
                var_star=float(var.min()))


SIMPLEX_R = np.array([1.0, 0.35, 0.0])  # rewards of actions A, B, C
SIMPLEX_PI0 = np.array([0.12, 0.28, 0.60])


def _softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def _kl(p, q):
    return float(np.sum(p * (np.log(p) - np.log(q))))


def compute_simplex():
    """Softmax policy pi = softmax(z) over 3 actions with rewards r.  J = pi . r.
    vanilla gradient on logits:  dz = pi * (r - J)        (the exact policy gradient)
    natural gradient:           dz = r - J               (Fisher-preconditioned; pi_t = pi0 * exp(t r) / Z)
    REINFORCE:                  dz = mean_i (R_i - b)(e_{a_i} - pi), n samples per step."""
    r, pi0 = SIMPLEX_R, SIMPLEX_PI0
    z0 = np.log(pi0)

    def flow(kind, steps=4000, dt=0.01):
        z, out = z0.copy(), []
        for k in range(steps):
            pi = _softmax(z)
            if k % 10 == 0:
                out.append(pi)
            J = pi @ r
            z = z + dt * (pi * (r - J) if kind == "vanilla" else (r - J))
        return np.array(out)

    def reinforce(baseline: str, seed: int, steps=300, lr=0.5, n=4, shift=0.0):
        g = np.random.default_rng(seed)
        z, out = z0.copy(), [pi0]
        for _ in range(steps):
            pi = _softmax(z)
            a = g.choice(3, size=n, p=pi)
            R = r[a] + shift
            if baseline == "none":
                b = np.zeros(n)
            elif baseline == "loo":
                b = (R.sum() - R) / (n - 1)
            else:
                b = np.full(n, R.mean())
            E = np.eye(3)[a]
            z = z + lr * np.mean((R - b)[:, None] * (E - pi), 0)
            out.append(_softmax(z))
        return np.array(out)

    # iso-KL contours KL(center || pi) = c around a few centers (polar search in the simplex plane)
    def contour(center, c=0.06, m=120):
        pts = []
        u = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)
        v = np.array([1.0, 1.0, -2.0]) / np.sqrt(6)
        for th in np.linspace(0, 2 * np.pi, m, endpoint=False):
            d = np.cos(th) * u + np.sin(th) * v
            lo, hi = 0.0, 1.0
            # largest step that stays inside the simplex
            neg = d < 0
            if neg.any():
                hi = min(hi, float(np.min(center[neg] / -d[neg])) * 0.999)
            for _ in range(60):
                mid = (lo + hi) / 2
                if _kl(center, center + mid * d) < c:
                    lo = mid
                else:
                    hi = mid
            pts.append(center + lo * d)
        return np.array(pts)

    centers = [np.array([1 / 3, 1 / 3, 1 / 3]), np.array([0.7, 0.15, 0.15]), np.array([0.12, 0.28, 0.60]),
               np.array([0.08, 0.84, 0.08])]
    contours = np.array([contour(c) for c in centers])
    betas = np.logspace(1.5, -2, 200)
    tilt = np.array([pi0 * np.exp(r / b) / np.sum(pi0 * np.exp(r / b)) for b in betas])

    # variance of the single-sample estimator (R - b)(e_a - pi) at pi0, with rewards shifted by +2
    shift = 2.0
    R = r + shift
    G = np.eye(3) - pi0  # rows: grad log pi(a) for each action
    true = np.sum(pi0[:, None] * R[:, None] * G, 0)
    bs = np.linspace(0, 4, 161)
    var = np.array([np.sum(pi0 * np.sum(((R - b)[:, None] * G) ** 2, 1)) - true @ true for b in bs])
    g2 = np.sum(G**2, 1)
    bstar = float(np.sum(pi0 * R * g2) / np.sum(pi0 * g2))
    return dict(r=r, pi0=pi0, vanilla=flow("vanilla"), natural=flow("natural"),
                rf_none=np.array([reinforce("none", s, shift=shift) for s in range(5)]),
                rf_loo=np.array([reinforce("loo", s, shift=shift) for s in range(5)]),
                shift=shift, centers=np.array(centers), contours=contours, betas=betas, tilt=tilt,
                var_bs=bs, var=var, bstar=bstar, mean_R=float(pi0 @ R))


def compute_kl_est():
    """John Schulman, 'Approximating KL Divergence' (2020): x ~ q, r = p(x)/q(x);
    k1 = -log r,  k2 = (log r)^2 / 2,  k3 = (r - 1) - log r.  Estimates KL(q || p)."""
    rng = np.random.default_rng(0)
    out = {}
    for mu in (0.1, 1.0):
        x = rng.normal(size=2_000_000)
        logr = -((x - mu) ** 2) / 2 + x**2 / 2
        true = mu**2 / 2
        ks = dict(k1=-logr, k2=0.5 * logr**2, k3=np.expm1(logr) - logr)
        out[f"mu{mu}"] = dict(true=true, **{k: dict(bias=float(v.mean() / true - 1), std=float(v.std() / true))
                                            for k, v in ks.items()})
        if mu == 1.0:
            sub = x[:4000]
            lr = -((sub - mu) ** 2) / 2 + sub**2 / 2
            out["hist_logr"] = lr.tolist()
    return out


# ---------------------------------------------------------------------------
# The miniature: addition, with or without showing your work
# ---------------------------------------------------------------------------
VOCAB = "0123456789+=>|."
TOK = {c: i for i, c in enumerate(VOCAB)}
THINK, SEP, EOS = TOK[">"], TOK["|"], TOK["."]
ND = 4  # digits per operand
PL = 2 * ND + 2  # prompt length: "AAAA+BBBB="
ANS_MAX = 2 * (ND + 1) + 3  # ">" + reversed sum + "|" + sum + "."
SEQ = PL + ANS_MAX
P_THINK = 0.25  # share of pretraining answers that show their work
P_SLIP = 0.25  # in quick (direct) answers, each carry is forgotten with this probability
BASE_CFG = dict(vocab=len(VOCAB), d=96, layers=3, heads=3, seq=SEQ)
BASE_STEPS = 4000


def answer_text(a: int, b: int, think: bool) -> str:
    s = f"{a + b:0{ND + 1}d}"
    return (">" + s[::-1] + "|" + s + ".") if think else (s + ".")


def sloppy_sum(a: int, b: int, rng) -> int:
    """The sum as a hurried writer computes it: each carry is forgotten with probability P_SLIP."""
    da, db = f"{a:0{ND}d}"[::-1], f"{b:0{ND}d}"[::-1]
    out, c = [], 0
    for x, y in zip(da, db):
        t = int(x) + int(y) + c
        out.append(t % 10)
        c = int(t >= 10)
        if c and rng.random() < P_SLIP:
            c = 0
    out.append(c)
    return int("".join(str(d) for d in reversed(out)))


def prompt_text(a: int, b: int) -> str:
    return f"{a:0{ND}d}+{b:0{ND}d}="


def enc(s: str) -> list[int]:
    return [TOK[c] for c in s]


def dec(ids) -> str:
    return "".join(VOCAB[i] for i in ids)


def grade(a: int, b: int, ans: str) -> tuple[float, str]:
    """Outcome reward: 1 if the final answer is right (and well formed), else 0.  Also the answer's mode."""
    s = f"{a + b:0{ND + 1}d}"
    if ans.startswith(">"):
        body = ans[1:]
        ok = len(body) >= 2 * ND + 4 and body[ND + 1] == "|" and body[ND + 2:2 * ND + 3] == s \
            and body[2 * ND + 3] == "."
        return float(ok), "think"
    return float(ans[:ND + 2] == s + "."), "direct"


def answer_len(ids) -> int:
    """Tokens up to and including the first end-of-answer '.'."""
    for i, t in enumerate(ids):
        if t == EOS:
            return i + 1
    return len(ids)


def _model(cfg=None):
    from explainer.lm.pocket import Config, PocketGPT

    return PocketGPT(Config(**(cfg or BASE_CFG)))


def base_path() -> Path:
    return DATA_DIR / "base.pt"


def compute_base():
    """Pretrain on addition text where 25% of answers show their work (the sum written right-to-left, then the
    sum: always right) and the rest answer at once, forgetting each carry with probability P_SLIP.
    Loss on answer tokens only.  Saves the weights and the per-mode accuracy."""
    import torch
    import torch.nn.functional as F

    torch.set_num_threads(int(os.environ.get("RL_THREADS", 4)))
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    model = _model()

    def batch(n):
        a, b = rng.integers(0, 10**ND, n), rng.integers(0, 10**ND, n)
        th = rng.random(n) < P_THINK
        rows, masks = [], []
        for x, y, t in zip(a, b, th):
            ans = answer_text(x, y, True) if t else f"{sloppy_sum(x, y, rng):0{ND + 1}d}."
            ids = enc(prompt_text(x, y) + ans)
            m = [0] * (PL - 1) + [1] * (len(ids) - PL)
            ids += [EOS] * (SEQ - len(ids))
            m += [0] * (SEQ - 1 - len(m))
            rows.append(ids)
            masks.append(m)
        return torch.tensor(rows), torch.tensor(masks, dtype=torch.float32)

    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=0.0, betas=(0.9, 0.98))
    curve = []
    for step in range(BASE_STEPS):
        lr = 2e-3 * min(1, step / 200) * (0.1 + 0.9 * 0.5 * (1 + np.cos(np.pi * step / BASE_STEPS)))
        for g in opt.param_groups:
            g["lr"] = lr
        x, m = batch(128)
        logits = model(x[:, :-1])
        loss = (F.cross_entropy(logits.flatten(0, 1), x[:, 1:].flatten(), reduction="none") * m.flatten()).sum() / m.sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 100 == 0:
            curve.append([step, loss.item()])
    torch.save(model.state_dict(), base_path())
    ev = evaluate(model, n=2000, seed=123)
    return dict(curve=curve, cfg=BASE_CFG, steps=BASE_STEPS, p_think=P_THINK, eval=ev,
                params=sum(p.numel() for p in model.parameters()))


def load_model(state_path: Path):
    import torch

    m = _model()
    m.load_state_dict(torch.load(state_path, weights_only=True))
    m.eval()
    return m


def sample(model, prompts, temperature=1.0, greedy=False, force=None, eos=None, ans_max=None):
    """Autoregressive sampling of whole answers.  prompts: LongTensor (B, prompt length).  Returns (B, ans_max) answer
    ids; everything after the first end token is end-token padding.  ``force``: first answer token to force."""
    import torch

    eos = EOS if eos is None else eos
    ans_max = ANS_MAX if ans_max is None else ans_max
    pl = prompts.shape[1]
    with torch.no_grad():
        x = prompts
        done = torch.zeros(len(x), dtype=torch.bool)
        for t in range(ans_max):
            if t == 0 and force is not None:
                nxt = torch.full((len(x),), force, dtype=torch.long)
            else:
                logits = model(x)[:, -1].float()
                if greedy:
                    nxt = logits.argmax(-1)
                else:
                    nxt = torch.multinomial((logits / temperature).softmax(-1), 1)[:, 0]
            nxt = torch.where(done, torch.full_like(nxt, eos), nxt)
            done |= nxt == eos
            x = torch.cat([x, nxt[:, None]], 1)
            if done.all():
                pad = torch.full((len(x), ans_max - t - 1), eos, dtype=torch.long)
                x = torch.cat([x, pad], 1)
                break
        return x[:, pl:]


def prompts_tensor(a, b):
    import torch

    return torch.tensor([enc(prompt_text(x, y)) for x, y in zip(a, b)])


def evaluate(model, n=1000, seed=123, k=4):
    """Accuracy at temperature 1 on held-out problems: overall, per mode, and the probability of thinking."""
    import torch

    rng = np.random.default_rng(seed)
    a, b = rng.integers(0, 10**ND, n), rng.integers(0, 10**ND, n)
    P = prompts_tensor(a, b)
    with torch.no_grad():
        p_think = float(model(P)[:, -1].softmax(-1)[:, THINK].mean())
    out = dict(p_think=p_think)
    ans = sample(model, P.repeat_interleave(k, 0))
    rs, modes, lens = [], [], []
    for i, row in enumerate(ans.tolist()):
        r, mode = grade(int(a[i // k]), int(b[i // k]), dec(row))
        rs.append(r)
        modes.append(mode)
        lens.append(answer_len(row))
    rs, modes = np.array(rs), np.array(modes)
    out.update(pass1=float(rs.mean()), length=float(np.mean(lens)), think_frac=float((modes == "think").mean()))
    for mode, f in (("think", THINK), ("direct", None)):
        if mode == "direct":
            # force a direct answer: sample the first token among digits only
            with torch.no_grad():
                logits = model(P)[:, -1].clone()
                logits[:, THINK] = -1e9
                first = torch.multinomial(logits.softmax(-1), 1)[:, 0]
            Pf = torch.cat([P, first[:, None]], 1)
            rest = sample_from(model, Pf, ANS_MAX - 1)
            full = torch.cat([first[:, None], rest], 1)
        else:
            full = sample(model, P, force=THINK)
        acc = np.mean([grade(int(x), int(y), dec(row))[0] for x, y, row in zip(a, b, full.tolist())])
        out[f"acc_{mode}"] = float(acc)
    return out


def sample_from(model, x, n_tokens):
    """Continue sequences x for n_tokens (temperature 1), padding after '.'."""
    import torch

    with torch.no_grad():
        start = x.shape[1]
        done = x[:, -1] == EOS
        for _ in range(n_tokens):
            nxt = torch.multinomial(model(x)[:, -1].float().softmax(-1), 1)[:, 0]
            nxt = torch.where(done, torch.full_like(nxt, EOS), nxt)
            done |= nxt == EOS
            x = torch.cat([x, nxt[:, None]], 1)
        return x[:, start:]


# ---------------------------------------------------------------------------
# RL from the pretrained pocket model
# ---------------------------------------------------------------------------
RL_DEFAULTS = dict(
    adv="grpo",  # raw | rloo | grpo (mean/std) | drgrpo (mean only) | gae (learned critic)
    agg="seq_token_mean",  # seq_token_mean (GRPO: 1/|o_i|) | token_mean (DAPO) | token_sum_const (Dr. GRPO)
    eps_low=0.2, eps_high=0.2, beta=0.0, lr=1e-4, steps=120, P=32, G=8, minibatches=4, epochs=1,
    dynamic=False,  # DAPO dynamic sampling: drop groups whose rewards are all equal
    lam=0.95, lr_v=1e-3, critic_warmup=20, seed=0, eval_every=5, checkpoints=(), temperature=1.0,
)


def token_logprobs(model, prompts, ans, with_entropy=False):
    """log pi(y_t | x, y_<t) of every answer token, (B, ANS_MAX); optionally the full-distribution entropy."""
    import torch.nn.functional as F

    import torch

    x = torch.cat([prompts, ans], 1)
    logits = model(x[:, :-1])[:, prompts.shape[1] - 1:].float()
    logp_all = F.log_softmax(logits, -1)
    lp = logp_all.gather(2, ans[..., None])[..., 0]
    if with_entropy:
        ent = -(logp_all.exp() * logp_all).sum(-1)
        return lp, ent
    return lp


def answer_mask(ans, eos=None):
    """1 for answer tokens up to and including the first end token, else 0."""
    import torch

    is_eos = (ans == (EOS if eos is None else eos)).long()
    first = torch.cumsum(is_eos, 1) - is_eos  # number of '.' strictly before t
    return (first == 0).float()


class Critic:
    """A value model: the pocket transformer's trunk with a scalar head, initialized from the base model."""

    def __init__(self, base_state, cfg=None):
        import torch

        cfg = cfg or BASE_CFG
        self.model = _model(cfg)
        self.model.load_state_dict(base_state)
        self.model.head = torch.nn.Linear(cfg["d"], 1, bias=True)
        torch.nn.init.zeros_(self.model.head.weight)
        torch.nn.init.constant_(self.model.head.bias, 0.5)

    def values(self, prompts, ans):
        """V(s_t) for t = 0..ANS_MAX-1, where s_t = prompt + the first t answer tokens."""
        import torch

        x = torch.cat([prompts, ans], 1)
        return self.model(x[:, :-1])[:, prompts.shape[1] - 1:, 0]


def gae(rewards, values, mask, lam, gamma=1.0):
    """Generalized advantage estimation on padded token sequences.  rewards, values, mask: (B, T)."""
    import torch

    B, T = rewards.shape
    adv = torch.zeros_like(rewards)
    last = torch.zeros(B)
    for t in reversed(range(T)):
        nxt_v = values[:, t + 1] * mask[:, t + 1] if t + 1 < T else torch.zeros(B)
        delta = rewards[:, t] + gamma * nxt_v - values[:, t]
        last = delta + gamma * lam * last * (mask[:, t + 1] if t + 1 < T else 0.0)
        adv[:, t] = last * mask[:, t]
    return adv


def adder_task() -> dict:
    """Everything the RL loop needs to know about the adder."""

    def draw(rng, n):
        a, b = rng.integers(0, 10**ND, n), rng.integers(0, 10**ND, n)
        return [(int(x), int(y)) for x, y in zip(a, b)]

    return dict(cfg=BASE_CFG, base=base_path(), eos=EOS, ans_max=ANS_MAX, dec=dec, draw=draw,
                prompts=lambda probs: prompts_tensor([p[0] for p in probs], [p[1] for p in probs]),
                grade=lambda prob, text: grade(prob[0], prob[1], text),
                evaluate=lambda m: evaluate(m, n=500, seed=123, k=2))


TASKS = {"adder": adder_task}


def rl_run(spec: dict) -> dict:
    """One RL run from the base model with a verifiable 0/1 reward.  Returns curves (and saves checkpoints)."""
    import torch

    cfg = {**RL_DEFAULTS, **spec}
    task = TASKS[cfg.get("task", "adder")]()
    torch.set_num_threads(1)
    torch.manual_seed(cfg["seed"])
    rng = np.random.default_rng(1000 + cfg["seed"])
    base_state = torch.load(task["base"], weights_only=True)
    policy, ref = _model(task["cfg"]), _model(task["cfg"])
    policy.load_state_dict(base_state)
    ref.load_state_dict(base_state)
    ref.eval()
    for p_ in ref.parameters():
        p_.requires_grad_(False)
    opt = torch.optim.AdamW(policy.parameters(), lr=cfg["lr"], weight_decay=0.0, betas=(0.9, 0.99))
    critic = None
    if cfg["adv"] == "gae":
        critic = Critic(base_state, task["cfg"])
        opt_v = torch.optim.AdamW(critic.model.parameters(), lr=cfg["lr_v"], weight_decay=0.0)
    n_params = sum(p_.numel() for p_ in policy.parameters())
    P, G = cfg["P"], cfg["G"]
    log = []
    evals = []
    gen_tokens = train_tokens = 0
    ckpts = {}
    for step in range(cfg["steps"] + 1):
        if step % cfg["eval_every"] == 0 or step == cfg["steps"]:
            policy.eval()
            ev = task["evaluate"](policy)
            policy.train()
            evals.append(dict(step=step, gen_tokens=gen_tokens, train_tokens=train_tokens, **ev))
        if step in cfg["checkpoints"]:
            ck = RUN_DIR / f"{cfg['name']}_step{step}.pt"
            torch.save(policy.state_dict(), ck)
            ckpts[step] = str(ck.relative_to(DATA_DIR))
        if step == cfg["steps"]:
            break
        # ---- rollouts
        probs = task["draw"](rng, P)
        prompts = task["prompts"](probs).repeat_interleave(G, 0)
        policy.eval()
        ans = sample(policy, prompts, temperature=cfg["temperature"], eos=task["eos"], ans_max=task["ans_max"])
        policy.train()
        texts = [task["dec"](r) for r in ans.tolist()]
        R = torch.tensor([task["grade"](probs[i // G], t)[0] for i, t in enumerate(texts)])
        mask = answer_mask(ans, task["eos"])
        lens = mask.sum(1)
        gen_tokens += int(lens.sum())
        Rg = R.view(P, G)
        zero_var = (Rg.std(1) == 0).float()
        # ---- advantages (one number per answer, broadcast to its tokens; per token for GAE)
        if cfg["adv"] == "raw":
            A = R.clone()
        elif cfg["adv"] == "rloo":
            A = (Rg - (Rg.sum(1, keepdim=True) - Rg) / (G - 1)).flatten()
        elif cfg["adv"] == "grpo":
            A = ((Rg - Rg.mean(1, keepdim=True)) / (Rg.std(1, keepdim=True) + 1e-4)).flatten()
        elif cfg["adv"] == "drgrpo":
            A = (Rg - Rg.mean(1, keepdim=True)).flatten()
        if cfg["adv"] == "gae":
            with torch.no_grad():
                V = critic.values(prompts, ans)
            rew = torch.zeros_like(V)
            last_idx = (lens - 1).long()
            rew[torch.arange(len(R)), last_idx] = R
            A_tok = gae(rew, V * mask, mask, cfg["lam"])
            returns = A_tok + V * mask
        else:
            A_tok = A[:, None] * mask
        keep = torch.ones(len(R), dtype=torch.bool)
        if cfg["dynamic"]:
            keep = (~zero_var.bool()).repeat_interleave(G)
        with torch.no_grad():
            old_lp = token_logprobs(policy, prompts, ans)
            ref_lp = token_logprobs(ref, prompts, ans)
        # ---- critic update (and warmup: critic only)
        if critic is not None:
            for _ in range(2):
                perm = torch.randperm(len(R))
                for mb in perm.chunk(cfg["minibatches"]):
                    v = critic.values(prompts[mb], ans[mb])
                    vl = (((v - returns[mb]) ** 2) * mask[mb]).sum() / mask[mb].sum()
                    opt_v.zero_grad()
                    vl.backward()
                    opt_v.step()
            if step < cfg["critic_warmup"]:
                log.append(dict(step=step, reward=float(R.mean()), value_loss=float(vl), warmup=True,
                                length=float(lens.mean()), think=float(np.mean([t.startswith(">") for t in texts]))))
                continue
        # ---- policy update: PPO-clip surrogate over minibatches
        idx = torch.nonzero(keep)[:, 0]
        stats = dict(clip=[], ent=[], cov=[], kl=[])
        for _ in range(cfg["epochs"]):
            perm = idx[torch.randperm(len(idx))]
            for mb in perm.chunk(cfg["minibatches"]):
                if len(mb) == 0:
                    continue
                lp, ent = token_logprobs(policy, prompts[mb], ans[mb], with_entropy=True)
                m, adv = mask[mb], A_tok[mb]
                ratio = torch.exp(lp - old_lp[mb])
                surr = torch.minimum(ratio * adv, torch.clamp(ratio, 1 - cfg["eps_low"], 1 + cfg["eps_high"]) * adv)
                per_tok = -surr
                if cfg["beta"] > 0:  # k3 estimator of KL(pi || ref), in the loss (as in GRPO)
                    d = ref_lp[mb] - lp
                    per_tok = per_tok + cfg["beta"] * (torch.exp(d) - d - 1)
                if cfg["agg"] == "seq_token_mean":
                    loss = ((per_tok * m).sum(1) / m.sum(1)).mean()
                elif cfg["agg"] == "token_mean":
                    loss = (per_tok * m).sum() / m.sum()
                else:  # token_sum_const: sum over tokens, divided by a constant (Dr. GRPO)
                    loss = (per_tok * m).sum() / (len(mb) * task["ans_max"])
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
                opt.step()
                train_tokens += int(m.sum())
                with torch.no_grad():
                    mm = m.bool()
                    stats["clip"].append(float(((ratio[mm] - 1).abs() > cfg["eps_low"]).float().mean()))
                    stats["ent"].append(float(ent[mm].mean()))
                    l, av = lp[mm], adv[mm]
                    stats["cov"].append(float(((l - l.mean()) * (av - av.mean())).mean()))
                    stats["kl"].append(float((old_lp[mb][mm] - ref_lp[mb][mm]).sum() / len(mb)))
        log.append(dict(step=step, reward=float(R.mean()), length=float(lens.mean()),
                        think=float(np.mean([t.startswith(">") for t in texts])), zero_var=float(zero_var.mean()),
                        clip=float(np.mean(stats["clip"])), entropy=float(np.mean(stats["ent"])),
                        cov=float(np.mean(stats["cov"])), kl=float(np.mean(stats["kl"])),
                        len_right=float(lens[R > 0].mean()) if (R > 0).any() else None,
                        len_wrong=float(lens[R == 0].mean()) if (R == 0).any() else None))
    return dict(spec={k: (list(v) if isinstance(v, tuple) else v) for k, v in cfg.items()}, log=log, evals=evals,
                checkpoints=ckpts, params=n_params)


# ---------------------------------------------------------------------------
# Runs, and what we measure on them
# ---------------------------------------------------------------------------
HERO = "grpo_s0"
HERO_CKPTS = (0, 5, 10, 15, 20, 30, 40, 60, 80, 120)


def run_specs() -> dict:
    """Every RL run in the video.  Three seeds per algorithm; the hero run keeps checkpoints."""
    algos = {
        "grpo": dict(adv="grpo", agg="seq_token_mean"),
        "reinforce": dict(adv="raw", agg="seq_token_mean"),
        # the same REINFORCE with a constant normalizer instead of 1/|o_i|: isolates the length bias
        "reinforce_tok": dict(adv="raw", agg="token_sum_const"),
        "rloo": dict(adv="rloo", agg="seq_token_mean"),
        "drgrpo": dict(adv="drgrpo", agg="token_sum_const"),
        "dapo": dict(adv="grpo", agg="token_mean", eps_high=0.28, dynamic=True),
        "ppo": dict(adv="gae", agg="token_mean"),
        # reusing each batch: 1 update vs 16 updates (4 minibatches x 4 epochs), clipped or not
        "onpolicy": dict(adv="grpo", agg="seq_token_mean", minibatches=1, epochs=1),
        "reuse_clip": dict(adv="grpo", agg="seq_token_mean", minibatches=4, epochs=4),
        "reuse_noclip": dict(adv="grpo", agg="seq_token_mean", minibatches=4, epochs=4, eps_low=1e9, eps_high=1e9),
    }
    specs = {}
    for algo, kw in algos.items():
        for seed in range(3):
            name = f"{algo}_s{seed}"
            specs[name] = dict(name=name, seed=seed, **kw)
    specs[HERO]["checkpoints"] = HERO_CKPTS
    return specs


def _run_one(spec):
    out_path = RUN_DIR / f"{spec['name']}.json"
    if out_path.exists():
        return spec["name"], 0.0
    t = time.time()
    res = rl_run(spec)
    res["seconds"] = time.time() - t
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, default=float))
    tmp.replace(out_path)
    return spec["name"], time.time() - t


def compute_runs(workers: int = int(os.environ.get("RL_WORKERS", 4))):
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    specs = list(run_specs().values())
    specs.sort(key=lambda s: (s["adv"] != "gae", s["name"] != HERO))  # slowest first
    with ProcessPoolExecutor(workers) as pool:
        for name, dt in pool.map(_run_one, specs):
            print(f"    run {name:<14} {dt:6.0f}s", flush=True)
    return {s["name"]: json.loads((RUN_DIR / f"{s['name']}.json").read_text()) for s in specs}


def load_run(name: str) -> dict:
    return json.loads((RUN_DIR / f"{name}.json").read_text())


def hero_model(step: int):
    return load_model(DATA_DIR / load_run(HERO)["checkpoints"][str(step)])


def answer_tree(model, a: int, b: int, min_p: float = 2e-4) -> list[dict]:
    """Every whole answer with probability >= min_p (exact, by expanding the token tree breadth-first).
    Returns [{text, p, r, mode}], sorted by the tree order (think branch first, then digits)."""
    import torch

    prompt = enc(prompt_text(a, b))
    frontier = [([], 1.0)]
    leaves = []
    with torch.no_grad():
        for depth in range(ANS_MAX):
            if not frontier:
                break
            x = torch.tensor([prompt + pre for pre, _ in frontier])
            probs = model(x)[:, -1].float().softmax(-1).numpy()
            nxt = []
            for (pre, pp), pr in zip(frontier, probs):
                for tok in np.argsort(-pr):
                    q = pp * float(pr[tok])
                    if q < min_p:
                        break
                    seq = pre + [int(tok)]
                    if tok == EOS or depth == ANS_MAX - 1:
                        text = dec(seq)
                        r, mode = grade(a, b, text)
                        leaves.append(dict(text=text, p=q, r=r, mode=mode))
                    else:
                        nxt.append((seq, q))
            frontier = nxt
    order = {c: (-1 if c == ">" else i) for i, c in enumerate(VOCAB)}
    leaves.sort(key=lambda L: [order[c] for c in L["text"]])
    return leaves


def pick_example(model, rng, n_cand=60, n=64):
    """A running example: a problem with a carry in nearly every column, whose direct answers are often wrong
    (about 40% right) but whose worked answers are reliable.  All candidates are sampled in two batched calls."""
    import torch

    cands = []
    while len(cands) < n_cand:
        a, b = int(rng.integers(1000, 10**ND)), int(rng.integers(1000, 10**ND))
        c, carries = 0, 0
        for da, db in zip(reversed(f"{a:0{ND}d}"), reversed(f"{b:0{ND}d}")):
            c = int(int(da) + int(db) + c >= 10)
            carries += c
        if carries >= ND - 1:
            cands.append((a, b))
    P = prompts_tensor([x for x, _ in cands], [y for _, y in cands]).repeat_interleave(n, 0)
    with torch.no_grad():
        logits = model(P)[:, -1].clone()
    logits[:, THINK] = -1e9
    first = torch.multinomial(logits.softmax(-1), 1)[:, 0]
    rest = sample_from(model, torch.cat([P, first[:, None]], 1), ANS_MAX - 1)
    direct = [grade(*cands[i // n], dec([f] + r))[0] for i, (f, r) in enumerate(zip(first.tolist(), rest.tolist()))]
    think = [grade(*cands[i // n], dec(r))[0] for i, r in enumerate(sample(model, P, force=THINK).tolist())]
    best = None
    for j, (a, b) in enumerate(cands):
        acc_d = float(np.mean(direct[j * n:(j + 1) * n]))
        acc_t = float(np.mean(think[j * n:(j + 1) * n]))
        score = abs(acc_d - 0.4) + max(0.0, 0.95 - acc_t)
        if best is None or score < best[0]:
            best = (score, a, b, acc_d, acc_t)
    return best[1:]


def compute_tree():
    """The answer tree for the running example, at every hero checkpoint; and one GRPO group from the base."""
    import torch

    torch.set_num_threads(int(os.environ.get("RL_THREADS", 4)))
    rng = np.random.default_rng(5)
    base = load_model(base_path())
    a, b, acc_d, acc_t = pick_example(base, rng)
    trees = {}
    for step in HERO_CKPTS:
        m = base if step == 0 else hero_model(step)
        trees[str(step)] = answer_tree(m, a, b)
    # one group of 8 answers from the base model, with every advantage estimator
    torch.manual_seed(11)
    G = 8
    groups = []
    for seed in range(40):
        torch.manual_seed(seed)
        ans = sample(base, prompts_tensor([a] * G, [b] * G))
        texts = [dec(r) for r in ans.tolist()]
        R = np.array([grade(a, b, t)[0] for t in texts])
        groups.append(dict(texts=[t[:answer_len(enc(t))] for t in texts], r=R.tolist()))
    return dict(a=a, b=b, acc_direct=acc_d, acc_think=acc_t, trees=trees, groups=groups, steps=list(HERO_CKPTS))


def compute_tilt(n_problems: int = 48, n_samples: int = 64):
    """pi_beta = pi_ref exp(r / beta) / Z on whole answers (exact, by enumerating the base model's answer trees), for
    48 problems; and, for each checkpoint of the hero run, its reward and KL from the base model, estimated from 64
    samples per problem with exact sequence log-probabilities (KL = E_pi[log pi - log pi_ref])."""
    import torch

    torch.set_num_threads(int(os.environ.get("RL_THREADS", 4)))
    rng = np.random.default_rng(77)
    base = load_model(base_path())
    probs = [(int(rng.integers(0, 10**ND)), int(rng.integers(0, 10**ND))) for _ in range(n_problems)]
    betas = np.logspace(1, -2.5, 120)
    ref_trees = [answer_tree(base, a, b, min_p=2e-4) for a, b in probs]
    R_beta, KL_beta = np.zeros(len(betas)), np.zeros(len(betas))
    for leaves in ref_trees:
        p = np.array([L["p"] for L in leaves])
        p = p / p.sum()
        r = np.array([L["r"] for L in leaves])
        for i, be in enumerate(betas):
            w = p * np.exp((r - r.max()) / be)
            q = w / w.sum()
            R_beta[i] += q @ r / len(probs)
            KL_beta[i] += np.sum(q * (np.log(q + 1e-300) - np.log(p))) / len(probs)
    P = prompts_tensor([a for a, _ in probs], [b for _, b in probs]).repeat_interleave(n_samples, 0)
    points = []
    torch.manual_seed(0)
    for step in HERO_CKPTS:
        m = hero_model(step) if step else base
        ans = sample(m, P)
        mask = answer_mask(ans)
        with torch.no_grad():
            lp = (token_logprobs(m, P, ans) * mask).sum(1)
            lr = (token_logprobs(base, P, ans) * mask).sum(1)
        R = np.array([grade(probs[i // n_samples][0], probs[i // n_samples][1], dec(x))[0] for i, x in enumerate(ans.tolist())])
        points.append(dict(step=step, R=float(R.mean()), KL=float((lp - lr).mean())))
    ex = load("tree")
    return dict(betas=betas, R_beta=R_beta, KL_beta=KL_beta, points=points, n_problems=len(probs), n_samples=n_samples,
                example=dict(a=ex["a"], b=ex["b"], leaves=ex["trees"]["0"]))


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased pass@k from n samples with c correct (Chen et al. 2021): 1 - C(n-c, k) / C(n, k)."""
    if n - c < k:
        return 1.0
    return float(1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))


def compute_passk():
    import torch

    torch.set_num_threads(int(os.environ.get("RL_THREADS", 4)))
    rng = np.random.default_rng(99)
    n, N = 128, 300
    probs = [(int(rng.integers(0, 10**ND)), int(rng.integers(0, 10**ND))) for _ in range(N)]
    ks = [1, 2, 4, 8, 16, 32, 64, 128]
    out = dict(ks=ks, n=n, problems=N)
    for name, step in (("base", 0), ("mid", 40), ("final", HERO_CKPTS[-1])):
        m = base_model = load_model(base_path()) if step == 0 else hero_model(step)
        cs = []
        for a, b in probs:
            ans = sample(m, prompts_tensor([a] * n, [b] * n))
            cs.append(int(sum(grade(a, b, dec(r))[0] for r in ans.tolist())))
        out[name] = dict(step=step, correct=cs, curve=[float(np.mean([pass_at_k(n, c, k) for c in cs])) for k in ks])
        del base_model
    return out


def compute_critic():
    """A value model learns V(s_t) for the *base* policy from Monte-Carlo returns (lambda = 1 targets), then
    we read it along real answers to the running example: values, TD errors, and GAE for several lambda."""
    import torch

    torch.set_num_threads(int(os.environ.get("RL_THREADS", 4)))
    torch.manual_seed(0)
    rng = np.random.default_rng(3)
    base_state = torch.load(base_path(), weights_only=True)
    policy = load_model(base_path())
    critic = Critic(base_state)
    opt = torch.optim.AdamW(critic.model.parameters(), lr=1e-3, weight_decay=0.0)
    curve = []
    for step in range(400):
        a, b = rng.integers(0, 10**ND, 64), rng.integers(0, 10**ND, 64)
        P = prompts_tensor(a, b).repeat_interleave(4, 0)
        ans = sample(policy, P)
        R = torch.tensor([grade(int(a[i // 4]), int(b[i // 4]), dec(r))[0] for i, r in enumerate(ans.tolist())])
        mask = answer_mask(ans)
        v = critic.values(P, ans)
        loss = (((v - R[:, None]) ** 2) * mask).sum() / mask.sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
        curve.append(float(loss))
    ex = load("tree")
    a, b = ex["a"], ex["b"]
    # pick real answers from the base tree: the likeliest right "think" answer, the likeliest right direct one,
    # and the likeliest wrong direct one
    leaves = ex["trees"]["0"]
    picks = {}
    for L in sorted(leaves, key=lambda L: -L["p"]):
        key = (L["mode"], L["r"])
        if key not in picks:
            picks[key] = L["text"]
    shows = []
    for key in [("think", 1.0), ("direct", 1.0), ("direct", 0.0)]:
        if key not in picks:
            continue
        t = picks[key]
        ids = torch.tensor([enc(t) + [EOS] * (ANS_MAX - len(t))])
        P = prompts_tensor([a], [b])
        with torch.no_grad():
            V = critic.values(P, ids)[0, :len(t)].numpy()
            lp = token_logprobs(policy, P, ids)[0, :len(t)].numpy()
        r = np.zeros(len(t))
        r[-1] = key[1]
        Vn = np.append(V[1:], 0.0)
        delta = r + Vn - V
        lams = [0.0, 0.5, 0.9, 1.0]
        gaes = {str(l): [float(sum((l ** j) * delta[t0 + j] for j in range(len(t) - t0))) for t0 in range(len(t))]
                for l in lams}
        shows.append(dict(text=t, mode=key[0], r=key[1], V=V.tolist(), delta=delta.tolist(), gae=gaes,
                          p_tok=np.exp(lp).tolist()))
    with torch.no_grad():
        P = prompts_tensor([a], [b])
        v0 = float(critic.values(P, torch.tensor([[EOS] * ANS_MAX]))[0, 0])
    return dict(curve=curve, shows=shows, V_prompt=v0, a=a, b=b)


def compute_dpo(beta: float = 0.1, lr: float = 1e-5, steps: int = 300, n_pairs: int = 4096):
    """Offline DPO from the base model: pairs (right answer, wrong answer) to the same prompt, sampled once from
    the base model; then the DPO loss with the base model as the frozen reference.  Also tracks how the log
    probabilities of the preferred and rejected answers move (likelihood displacement)."""
    import torch
    import torch.nn.functional as F

    torch.set_num_threads(int(os.environ.get("RL_THREADS", 4)))
    torch.manual_seed(0)
    rng = np.random.default_rng(42)
    ref = load_model(base_path())
    pairs_w, pairs_l, prompts = [], [], []
    while len(prompts) < n_pairs:
        a, b = rng.integers(0, 10**ND, 128), rng.integers(0, 10**ND, 128)
        P = prompts_tensor(a, b).repeat_interleave(8, 0)
        ans = sample(ref, P)
        for i in range(128):
            grp = ans[8 * i:8 * i + 8]
            r = [grade(int(a[i]), int(b[i]), dec(x))[0] for x in grp.tolist()]
            w = [j for j in range(8) if r[j] > 0]
            l_ = [j for j in range(8) if r[j] == 0]
            if w and l_:
                pairs_w.append(grp[rng.choice(w)])
                pairs_l.append(grp[rng.choice(l_)])
                prompts.append(P[8 * i])
    W, L, X = torch.stack(pairs_w[:n_pairs]), torch.stack(pairs_l[:n_pairs]), torch.stack(prompts[:n_pairs])
    with torch.no_grad():
        ref_w = (token_logprobs(ref, X, W) * answer_mask(W)).sum(1)
        ref_l = (token_logprobs(ref, X, L) * answer_mask(L)).sum(1)
    policy = load_model(base_path())
    policy.train()
    opt = torch.optim.AdamW(policy.parameters(), lr=lr, weight_decay=0.0, betas=(0.9, 0.99))
    evals, losses = [], []
    probe = torch.arange(512)
    for step in range(steps + 1):
        if step % 20 == 0:
            policy.eval()
            with torch.no_grad():
                lw = (token_logprobs(policy, X[probe], W[probe]) * answer_mask(W[probe])).sum(1)
                ll = (token_logprobs(policy, X[probe], L[probe]) * answer_mask(L[probe])).sum(1)
            evals.append(dict(step=step, dlogp_w=float((lw - ref_w[probe]).mean()), dlogp_l=float((ll - ref_l[probe]).mean()),
                              **evaluate(policy, n=500, seed=123, k=2)))
            policy.train()
        if step == steps:
            break
        idx = torch.randint(0, n_pairs, (64,))
        lw = (token_logprobs(policy, X[idx], W[idx]) * answer_mask(W[idx])).sum(1)
        ll = (token_logprobs(policy, X[idx], L[idx]) * answer_mask(L[idx])).sum(1)
        margin = beta * ((lw - ref_w[idx]) - (ll - ref_l[idx]))
        loss = -F.logsigmoid(margin).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        losses.append(float(loss))
    return dict(beta=beta, lr=lr, n_pairs=n_pairs, evals=evals, losses=losses,
                think_frac_winners=float(np.mean([dec(x.tolist()).startswith(">") for x in W])))


def run_compute(ev: dict, n_params: int) -> float:
    """Training arithmetic so far: 2N per generated token, 6N per trained token (forward + backward)."""
    return 2.0 * n_params * ev["gen_tokens"] + 6.0 * n_params * ev["train_tokens"]


def scalerl_curve(C, R0, A, C_mid, B):
    """ScaleRL (Khatri et al. 2025): R_C = R_0 + (A - R_0) / (1 + (C_mid / C)^B)."""
    C = np.asarray(C, float)
    return R0 + (A - R0) / (1.0 + (C_mid / np.maximum(C, 1e-30)) ** B)


def compute_scaling():
    """Fit ScaleRL's sigmoid to each algorithm's held-out pass@1 vs compute (three seeds pooled)."""
    from scipy.optimize import curve_fit

    specs = run_specs()
    algos = sorted({n.rsplit("_s", 1)[0] for n in specs})
    out = {}
    for algo in algos:
        Cs, Rs = [], []
        R0s = []
        for seed in range(3):
            r = load_run(f"{algo}_s{seed}")
            for ev in r["evals"]:
                C = run_compute(ev, r["params"])
                if ev["step"] == 0:
                    R0s.append(ev["pass1"])
                    continue
                Cs.append(C)
                Rs.append(ev["pass1"])
        Cs, Rs = np.array(Cs), np.array(Rs)
        R0 = float(np.mean(R0s))

        def f(C, A, logCmid, B):
            return scalerl_curve(C, R0, A, 10.0**logCmid, B)

        try:
            (A, logCmid, B), _ = curve_fit(f, Cs, Rs, p0=[0.97, np.log10(np.median(Cs)), 1.5],
                                           bounds=([R0, np.log10(Cs.min()) - 3, 0.1], [1.0, np.log10(Cs.max()) + 3, 10]))
            fit = dict(A=float(A), C_mid=float(10**logCmid), B=float(B))
        except Exception as e:  # noqa: BLE001
            fit = dict(error=str(e))
        out[algo] = dict(R0=R0, C=Cs.tolist(), R=Rs.tolist(), **fit)
    return out


# ---------------------------------------------------------------------------
# Training-inference mismatch, on a real reasoning model
# ---------------------------------------------------------------------------
QWEN = "Qwen/Qwen3-0.6B"
MISMATCH_PROMPTS = [
    "A train leaves at 2:15 pm and travels 210 km at 84 km/h. At what time does it arrive?",
    "What is the remainder when 7^100 is divided by 13?",
    "How many positive divisors does 360 have?",
    "Solve for x: 3(x - 4) + 2 = 5x - 18.",
    "The sum of three consecutive odd integers is 141. What is the largest?",
    "A rectangle has perimeter 46 and area 120. What are its side lengths?",
    "How many ways can 5 people sit in a row if two of them refuse to sit next to each other?",
    "What is the sum of the first 50 positive even numbers?",
]


def compute_mismatch(max_new: int = 768):
    """Sample eight thinking traces at once in bfloat16 with a KV cache (as an inference engine does), at
    temperature 1, recording log pi_sampler(y_t) from the raw logits.  Then score each trace's tokens again in one
    full forward pass, alone and unpadded, in bfloat16 and in float32 (as a trainer does).  Same weights, same
    tokens: only the arithmetic differs."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(int(os.environ.get("RL_THREADS", 4)))
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(QWEN, padding_side="left")
    m16 = AutoModelForCausalLM.from_pretrained(QWEN, torch_dtype=torch.bfloat16).eval()
    texts = [tok.apply_chat_template([{"role": "user", "content": q}], tokenize=False, add_generation_prompt=True,
                                     enable_thinking=True) for q in MISMATCH_PROMPTS]
    batch = tok(texts, return_tensors="pt", padding=True)
    t0 = time.time()
    with torch.no_grad():
        out = m16.generate(**batch, do_sample=True, temperature=1.0, top_k=0, top_p=1.0, max_new_tokens=max_new,
                           output_logits=True, return_dict_in_generate=True)
    print(f"    mismatch: sampled {len(texts)} x {max_new} tokens in {time.time() - t0:.0f}s", flush=True)
    gen = out.sequences[:, batch.input_ids.shape[1]:]
    # Keep only the sampled token's log probability. Stacking all vocabulary
    # logits and normalizing them together creates several multi-GB copies.
    lp_all = torch.stack([
        torch.log_softmax(step_logits.float(), -1)
        .gather(1, gen[:, t:t + 1])[:, 0]
        for t, step_logits in enumerate(out.logits)
    ], 1)
    del out
    m32 = AutoModelForCausalLM.from_pretrained(QWEN, torch_dtype=torch.float32).eval()
    seqs = []
    for i, q in enumerate(MISMATCH_PROMPTS):
        g = gen[i].tolist()
        n = g.index(tok.eos_token_id) + 1 if tok.eos_token_id in g else len(g)
        if tok.pad_token_id is not None and tok.pad_token_id != tok.eos_token_id and tok.pad_token_id in g[:n]:
            n = g.index(tok.pad_token_id)
        g = g[:n]
        prompt_ids = tok(texts[i], return_tensors="pt").input_ids
        full = torch.cat([prompt_ids, torch.tensor([g])], 1)
        n0 = prompt_ids.shape[1]
        scores = {}
        with torch.no_grad():
            for name, m in (("bf16", m16), ("fp32", m32)):
                lg = m(full).logits[0, n0 - 1:-1].float()
                scores[name] = torch.log_softmax(lg, -1).gather(1, torch.tensor(g)[:, None])[:, 0].tolist()
        seqs.append(dict(question=q, n_prompt=n0, tokens=g, text=tok.decode(g), lp_sampler=lp_all[i, :n].tolist(),
                         lp_bf16=scores["bf16"], lp_fp32=scores["fp32"]))
        print(f"    mismatch {i}: {len(g)} tokens scored", flush=True)
    return dict(model=QWEN, temperature=1.0, max_new=max_new, seqs=seqs)


# ---------------------------------------------------------------------------
# Item registry
# ---------------------------------------------------------------------------
ITEMS = {
    "gauss": compute_gauss,
    "cloud": compute_cloud,
    "simplex": compute_simplex,
    "kl_est": compute_kl_est,
    "base": compute_base,
    "runs": compute_runs,
    "tree": compute_tree,
    "tilt": compute_tilt,
    "passk": compute_passk,
    "critic": compute_critic,
    "scaling": compute_scaling,
    "dpo": compute_dpo,
    "mismatch": compute_mismatch,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(ITEMS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"  cached  {name}")
            continue
        t = time.time()
        print(f"  ...     {name}", flush=True)
        out = ITEMS[name]()
        _save(name, out)
        print(f"  done    {name}  ({time.time() - t:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
