"""The character model of Part 11 ("Going Downhill") and the optimizers that train it.

The workhorse: 8 characters of context, each a 16-number vector, a hidden layer of 256 tanh units, a second 256 x 256
hidden layer (tanh) added back onto the first, and a softmax over the 167 characters of Part 1's books; scored in bits
per character on held-out text (``compute.char_data``, which Parts 12 and 16 also use).

The optimizers, written out so each line of an update rule is visible:

* ``sgdm``     SGD with Nesterov momentum 0.9, every parameter;
* ``adamw``    AdamW (decoupled weight decay 0.1), every parameter; ``adam_l2`` is Adam with an L2 penalty instead;
* ``lion``     Lion (Chen et al. 2023): the sign of a blend of momentum and gradient, every parameter;
* ``shampoo``  Shampoo (Gupta, Koren & Singer 2018) on the two hidden matrices: momentum preconditioned on both sides
               by L^-1/4 and R^-1/4 (exponential averages of G G^T and G^T G, roots refreshed every 10 steps), its
               size grafted from Adam's (the practice of Distributed Shampoo); AdamW on everything else;
* ``soap``     SOAP (Vyas et al. 2024): Adam run in the eigenbasis of Shampoo's two factors (refreshed every 10
               steps), on the hidden matrices; AdamW on everything else;
* ``muon``     Muon (Jordan et al. 2024) as scaled by Moonlight (Liu et al. 2025): Nesterov momentum 0.95,
               orthogonalized by five Newton-Schulz rounds, times 0.2 sqrt(max(m, n)) so its size matches AdamW's and
               one learning rate serves both; decoupled weight decay 0.1; AdamW on everything else;
* ``sfadamw``  schedule-free AdamW (Defazio et al. 2024): no schedule after warmup; gradients taken at an
               interpolation y of the fast iterate z and its running average x, which is the model that is scored.

Every run is seeded (initial weights and the batches); nothing here sets torch's thread count at import time
(``threads()`` is called by each job).
"""

from __future__ import annotations

import copy
import math
import os
import time

import numpy as np

CTX, EMB, HID = 8, 16, 256
BATCH = 256
WARMUP = 60
EVAL_N = 20_000  # held-out characters scored during training (all 100,000 at the end)


def threads(n: int | None = None) -> None:
    import torch

    torch.set_num_threads(int(n or os.environ.get("AI11_THREADS", 1)))


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


_data: dict = {}


def tensors():
    """(train, held-out, vocabulary size) as torch tensors: Part 11's split of Part 1's books."""
    import torch

    from .compute import char_data

    if "t" not in _data:
        tr, va, K = char_data()
        _data["t"] = (torch.from_numpy(np.asarray(tr, np.int64)), torch.from_numpy(np.asarray(va, np.int64)), K)
    return _data["t"]


def vocab() -> list[str]:
    from videos.ai.ai1 import compute as c1

    if "v" not in _data:
        _data["v"] = sorted(set("".join(c1.text(k) for k in ("train", "valid"))))
    return _data["v"]


_OFF: dict = {}


def windows(seq, pos):
    """The 8 characters before each position."""
    import torch

    if "o" not in _OFF:
        _OFF["o"] = torch.arange(-CTX, 0)
    return seq[pos[:, None] + _OFF["o"]]


# ---------------------------------------------------------------------------
# The model
# ---------------------------------------------------------------------------
def make_model(seed: int = 0, hid: int = HID, norm: bool = False):
    """The character model. ``norm``: a LayerNorm (no gain) between the second hidden matrix and its tanh, which
    makes that matrix scale-invariant (the weight-decay equilibrium experiment)."""
    import torch

    _, _, K = tensors()
    torch.manual_seed(seed)

    class CharMLP(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = torch.nn.Embedding(K, EMB)
            self.h1 = torch.nn.Linear(CTX * EMB, hid)
            self.h2 = torch.nn.Linear(hid, hid, bias=not norm)
            self.ln = torch.nn.LayerNorm(hid, elementwise_affine=False) if norm else None
            self.out = torch.nn.Linear(hid, K)

        def forward(self, ctx):
            h = torch.tanh(self.h1(self.emb(ctx).reshape(len(ctx), -1)))
            z = self.h2(h)
            if self.ln is not None:
                z = self.ln(z)
            return self.out(torch.tanh(z) + h)

        def mats(self):
            return [self.h1.weight, self.h2.weight]

    return CharMLP()


def bits(model, n: int = EVAL_N) -> float:
    """Held-out bits per character on the first ``n`` predictions of the held-out text."""
    import torch

    _, va, _ = tensors()
    end = min(len(va), CTX + n)
    tot = 0.0
    with torch.no_grad():
        for a in range(CTX, end, 25_000):
            pos = torch.arange(a, min(end, a + 25_000))
            tot += float(torch.nn.functional.cross_entropy(model(windows(va, pos)), va[pos], reduction="sum"))
    return tot / (end - CTX) / math.log(2)


WRITE_PROMPT, WRITE_LEN = "It was a", 72


def write(model) -> str:
    """Continue the same prompt with the same random draws (temperature 0.8), so checkpoints differ only by the
    model."""
    import torch

    chars = vocab()
    seq = [chars.index(c) for c in WRITE_PROMPT]
    gen = torch.Generator().manual_seed(1234)
    with torch.no_grad():
        for _ in range(WRITE_LEN):
            p = torch.softmax(model(torch.tensor([seq[-CTX:]])) / 0.8, -1)
            seq.append(int(torch.multinomial(p[0], 1, generator=gen)))
    return "".join(chars[i] for i in seq[CTX:])


# ---------------------------------------------------------------------------
# Newton-Schulz
# ---------------------------------------------------------------------------
NS_JORDAN = (3.4445, -4.7750, 2.0315)  # Keller Jordan's quintic (2024)
NS_EXACT = (2.0, -1.5, 0.5)  # fixes 1 with zero slope: DeepSeek-V4's last two rounds (2026)
NS_CUBIC = (1.5, -0.5, 0.0)  # the classical Newton-Schulz iteration


def newton_schulz(G, steps=5, coeffs=NS_JORDAN):
    """Push every singular value of G towards 1 with rounds of X <- aX + b(XX^T)X + c(XX^T)^2 X."""
    a, b, c = coeffs
    X = G / (G.norm() + 1e-7)
    tall = X.shape[0] > X.shape[1]
    if tall:
        X = X.T
    for _ in range(steps):
        A = X @ X.T
        X = a * X + (b * A + c * A @ A) @ X
    return X.T if tall else X


def inv_root(M, p: int, eps: float = 1e-6):
    """M^(-1/p) for a symmetric positive semi-definite M, damped by eps times its largest eigenvalue."""
    import torch

    w, Q = torch.linalg.eigh(M.double())
    w = w.clamp_min(0) + eps * float(w.max().clamp_min(1e-30))
    return ((Q * w ** (-1.0 / p)) @ Q.T).to(M.dtype)


# ---------------------------------------------------------------------------
# The optimizers
# ---------------------------------------------------------------------------
class Opt:
    """``step(f)``: one update at learning rate ``lr * f`` (the schedule's factor), after ``loss.backward()``."""

    def __init__(self, name, model, lr, wd=None, betas=None):
        import torch

        self.name, self.lr, self.t = name, lr, 0
        self.model = model
        params = list(model.parameters())
        mats = model.mats()
        rest = [p for p in params if all(p is not q for q in mats)]
        self.mats, self.rest, self.params = mats, rest, params
        self.torch_opts = []
        self.state: dict = {}
        if name == "sgdm":
            self.torch_opts = [torch.optim.SGD(params, lr=lr, momentum=0.9, nesterov=True)]
        elif name == "adamw":
            self.torch_opts = [torch.optim.AdamW(params, lr=lr, betas=betas or (0.9, 0.95),
                                                 weight_decay=0.1 if wd is None else wd)]
        elif name == "adam_l2":  # torch's Adam adds weight_decay * theta to the gradient: an L2 penalty
            self.torch_opts = [torch.optim.Adam(params, lr=lr, betas=betas or (0.9, 0.95), weight_decay=wd or 0.0)]
        elif name in ("muon", "shampoo", "soap"):
            self.wd = 0.1 if wd is None else wd
            self.torch_opts = [torch.optim.AdamW(rest, lr=lr, betas=(0.9, 0.95), weight_decay=self.wd)]
        elif name == "lion":
            self.wd = 1.0 if wd is None else wd  # Lion's learning rate is smaller; its decay larger (Chen et al.)
            self.state = {("p", i): torch.zeros_like(p) for i, p in enumerate(params)}
        elif name == "sfadamw":
            self.wd = 0.1 if wd is None else wd
            self.b1, self.b2 = 0.9, 0.999
            self.state = {("p", i): dict(z=p.detach().clone(), x=p.detach().clone(), v=torch.zeros_like(p))
                          for i, p in enumerate(params)}
            self.wsum = 0.0
        else:
            raise ValueError(name)

    def zero_grad(self):
        for p in self.params:
            p.grad = None

    def step(self, f: float = 1.0):
        import torch

        self.t += 1
        lr = self.lr * f
        for o in self.torch_opts:
            for g in o.param_groups:
                g["lr"] = lr
            o.step()
        with torch.no_grad():
            if self.name == "muon":
                for i, p in enumerate(self.mats):
                    st = self.state.setdefault(("m", i), torch.zeros_like(p))
                    st.mul_(0.95).add_(p.grad)
                    u = newton_schulz(p.grad + 0.95 * st)  # Nesterov-style
                    p.mul_(1 - lr * self.wd)
                    p.add_(u, alpha=-lr * 0.2 * math.sqrt(max(p.shape)))
            elif self.name == "shampoo":
                b1, b2 = 0.9, 0.95
                for i, p in enumerate(self.mats):
                    g = p.grad
                    st = self.state.get(("m", i))
                    if st is None:
                        st = self.state[("m", i)] = dict(m=torch.zeros_like(p), v=torch.zeros_like(p),
                                                      L=torch.zeros(p.shape[0], p.shape[0]),
                                                      R=torch.zeros(p.shape[1], p.shape[1]), Li=None, Ri=None)
                    st["m"].mul_(b1).add_(g, alpha=1 - b1)
                    st["v"].mul_(b2).addcmul_(g, g, value=1 - b2)
                    st["L"].mul_(b2).add_(g @ g.T, alpha=1 - b2)
                    st["R"].mul_(b2).add_(g.T @ g, alpha=1 - b2)
                    if st["Li"] is None or self.t % 10 == 1:
                        st["Li"], st["Ri"] = inv_root(st["L"], 4), inv_root(st["R"], 4)
                    mh = st["m"] / (1 - b1 ** self.t)
                    adam = mh / ((st["v"] / (1 - b2 ** self.t)).sqrt() + 1e-8)
                    P = st["Li"] @ mh @ st["Ri"]
                    P = P * (adam.norm() / (P.norm() + 1e-30))  # grafting: Shampoo's direction, Adam's size
                    p.mul_(1 - lr * self.wd)
                    p.add_(P, alpha=-lr)
            elif self.name == "soap":
                b1, b2 = 0.9, 0.95
                for i, p in enumerate(self.mats):
                    g = p.grad
                    st = self.state.get(("m", i))
                    if st is None:
                        st = self.state[("m", i)] = dict(m=torch.zeros_like(p), v=torch.zeros_like(p),
                                                      L=g @ g.T, R=g.T @ g, QL=None, QR=None)
                    else:
                        st["L"].mul_(b2).add_(g @ g.T, alpha=1 - b2)
                        st["R"].mul_(b2).add_(g.T @ g, alpha=1 - b2)
                    if st["QL"] is None or self.t % 10 == 1:
                        st["QL"] = torch.linalg.eigh(st["L"].double())[1].float()
                        st["QR"] = torch.linalg.eigh(st["R"].double())[1].float()
                    QL, QR = st["QL"], st["QR"]
                    st["m"].mul_(b1).add_(g, alpha=1 - b1)
                    gr = QL.T @ g @ QR  # the gradient in Shampoo's eigenbasis
                    st["v"].mul_(b2).addcmul_(gr, gr, value=1 - b2)
                    mr = (QL.T @ st["m"] @ QR) / (1 - b1 ** self.t)
                    n_ = mr / ((st["v"] / (1 - b2 ** self.t)).sqrt() + 1e-8)  # Adam, there
                    p.mul_(1 - lr * self.wd)
                    p.add_(QL @ n_ @ QR.T, alpha=-lr)  # and back
            elif self.name == "lion":
                for i, p in enumerate(self.params):
                    m = self.state[("p", i)]
                    c = 0.9 * m + 0.1 * p.grad
                    p.mul_(1 - lr * self.wd)
                    p.add_(torch.sign(c), alpha=-lr)
                    m.mul_(0.99).add_(p.grad, alpha=0.01)
            elif self.name == "sfadamw":
                self.wsum += lr * lr
                c = lr * lr / self.wsum
                bc2 = 1 - self.b2 ** self.t
                for i, p in enumerate(self.params):
                    st = self.state[("p", i)]
                    st["v"].mul_(self.b2).addcmul_(p.grad, p.grad, value=1 - self.b2)
                    u = p.grad / ((st["v"] / bc2).sqrt() + 1e-8) + self.wd * p  # p holds y
                    st["z"].add_(u, alpha=-lr)
                    st["x"].mul_(1 - c).add_(st["z"], alpha=c)
                    p.copy_((1 - self.b1) * st["z"] + self.b1 * st["x"])

    def scored(self):
        """A context in which the model holds the weights that are scored (schedule-free: the average x)."""
        opt = self

        class _Swap:
            def __enter__(self):
                if opt.name == "sfadamw":
                    self.saved = [p.detach().clone() for p in opt.params]
                    with __import__("torch").no_grad():
                        for i, p in enumerate(opt.params):
                            p.copy_(opt.state[("p", i)]["x"])

            def __exit__(self, *a):
                if opt.name == "sfadamw":
                    with __import__("torch").no_grad():
                        for p, s in zip(opt.params, self.saved):
                            p.copy_(s)

        return _Swap()


# ---------------------------------------------------------------------------
# Schedules
# ---------------------------------------------------------------------------
def lr_factor(k: int, steps: int, sched: str, decay_from: int | None = None) -> float:
    """Step k (1-based) of ``steps``: linear warmup over WARMUP steps, then
    ``cosine`` down to 0; ``constant``; ``wsd`` (constant, then linear to 0 from ``decay_from``, default the last
    fifth)."""
    w = min(1.0, k / WARMUP)
    if sched == "cosine":
        t = min(1.0, max(0.0, (k - WARMUP) / max(1, steps - WARMUP)))
        return w * 0.5 * (1 + math.cos(math.pi * t))
    if sched == "constant":
        return w
    if sched == "wsd":
        d0 = int(round(0.8 * steps)) if decay_from is None else decay_from
        return w * (1.0 if k <= d0 else max(0.0, (steps - k) / max(1, steps - d0)))
    raise ValueError(sched)


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------
def train(opt="adamw", lr=2e-3, steps=3000, seed=0, sched="cosine", wd=None, hid=HID, subset=None, eval_every=150,
          eval_n=EVAL_N, write_at=(), grab=None, betas=None, norm=False, track=None, ema=None, branches=(),
          final_n=100_000, clip=None):
    """One seeded training run of the character model. Returns a dict: ``curve`` [(step, held-out bits)], ``final``
    (on all 100,000 held-out characters), ``ms`` per step, ``writes`` {step: text} at ``write_at``; ``grab``: the
    second hidden matrix's gradient at that step and the trained matrix; ``track``: per-``eval_every`` measurements
    of the second hidden matrix (its norm, its update's norm and alignment); ``ema``: an exponential average of the
    weights with that decay, scored with the run; ``branches``: for a constant run, (from, to) cool-downs, each a
    copy of the run at step ``from`` decayed linearly to zero at ``to`` and scored there; ``clip``: clip the
    gradient's norm."""
    import torch

    threads()
    tr, va, _ = tensors()
    model = make_model(seed, hid=hid, norm=norm)
    o = Opt(opt, model, lr, wd=wd, betas=betas)
    g = rng(seed + 1)
    sub = None if subset is None else np.arange(CTX, CTX + int(subset))
    out = dict(curve=[(0, bits(model, eval_n))], writes={}, track=[], ema_curve=[], branches={})
    if 0 in write_at:
        out["writes"]["0"] = write(model)
    ema_w = [p.detach().clone() for p in model.parameters()] if ema else None
    t0 = time.time()

    def run_steps(model, o, k0, k1, factor, rng_, curve_=None):
        for k in range(k0, k1 + 1):
            pos = rng_.integers(CTX, len(tr), BATCH) if sub is None else sub[rng_.integers(0, len(sub), BATCH)]
            pos = torch.from_numpy(pos)
            loss = torch.nn.functional.cross_entropy(model(windows(tr, pos)), tr[pos])
            if not torch.isfinite(loss):
                return False
            o.zero_grad()
            loss.backward()
            if clip:
                torch.nn.utils.clip_grad_norm_(o.params, clip)
            o.step(factor(k))
            if curve_ is not None and (k % eval_every == 0 or k == k1):
                curve_.append((k, bits(model, eval_n)))
        return True

    def factor(k):
        return lr_factor(k, steps, sched)

    for k in range(1, steps + 1):
        for b0, b1 in branches:  # cool-down branches leave from here
            if k == b0 + 1:
                m2, o2, r2 = copy.deepcopy((model, o, g))  # one copy: the optimizer keeps pointing at its model
                bc = []
                ok = run_steps(m2, o2, b0 + 1, b1, lambda kk, b0=b0, b1=b1: lr_factor(kk, b1, "wsd", decay_from=b0), r2,
                               bc)
                out["branches"][f"{b0}_{b1}"] = dict(final=bits(m2, final_n) if ok else float("nan"), curve=bc,
                                                       quick=bits(m2, eval_n) if ok else float("nan"))
        pos = g.integers(CTX, len(tr), BATCH) if sub is None else sub[g.integers(0, len(sub), BATCH)]
        pos = torch.from_numpy(pos)
        loss = torch.nn.functional.cross_entropy(model(windows(tr, pos)), tr[pos])
        if not torch.isfinite(loss):
            out["diverged"] = k
            break
        o.zero_grad()
        loss.backward()
        if clip:
            torch.nn.utils.clip_grad_norm_(o.params, clip)
        if grab is not None and k == grab:
            out["grad"] = model.h2.weight.grad.detach().clone().numpy()
        if track is not None:
            W0 = model.h2.weight.detach().clone()
        o.step(factor(k))
        if ema_w is not None:
            with torch.no_grad():
                for e, p in zip(ema_w, model.parameters()):
                    e.mul_(ema).add_(p.detach(), alpha=1 - ema)
        if track is not None and k % track == 0:
            with torch.no_grad():
                W = model.h2.weight.detach()
                f = lr * factor(k)
                wd_ = o.torch_opts[0].param_groups[0]["weight_decay"] if o.torch_opts else 0.0
                u = -(W - W0 * (1 - f * wd_)) / f  # the update, without the decay
                out["track"].append((k, float(W.norm()), float(u.norm()),
                                     float((u * W0).sum() / (u.norm() * W0.norm() + 1e-30))))
        if k % eval_every == 0 or k == steps:
            with o.scored():
                out["curve"].append((k, bits(model, eval_n)))
            if ema_w is not None:
                saved = [p.detach().clone() for p in model.parameters()]
                with torch.no_grad():
                    for p, e in zip(model.parameters(), ema_w):
                        p.copy_(e)
                out["ema_curve"].append((k, bits(model, eval_n)))
                with torch.no_grad():
                    for p, s_ in zip(model.parameters(), saved):
                        p.copy_(s_)
        if k in write_at:
            with o.scored():
                out["writes"][str(k)] = write(model)
    out["ms"] = 1000 * (time.time() - t0) / max(1, steps)
    if "diverged" not in out:
        with o.scored():
            out["final"] = bits(model, final_n)
        if grab is not None:
            out["weight"] = model.h2.weight.detach().clone().numpy()
    else:
        out["final"] = float("nan")
    return out
