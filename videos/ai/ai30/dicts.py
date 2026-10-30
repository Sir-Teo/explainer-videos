"""Sparse dictionaries: sparse autoencoders of five kinds, transcoders and crosscoders, one trainer for all.

    f = encode(x)          the latent code (most entries zero)
    x_hat = f @ D + b_d    each latent adds its decoder row (unit length), scaled by how strongly it is on

Kinds of encoder:
    l1          f = ReLU(W_e (x - b_d) + b_e), loss + lam * sum f          (Bricken et al. 2023; Cunningham et al. 2023)
    topk        keep each vector's k largest pre-activations               (Makhzani & Frey 2013; Gao et al. 2024)
    batchtopk   keep the batch's k * B largest; a single threshold at use   (Bussmann, Leask & Nanda 2024)
    jumprelu    f = z * H(z - theta), a learned threshold per latent, loss + lam * #active, trained through
                straight-through estimators with a rectangle kernel of width eps (Rajamanoharan et al. 2024)
    matryoshka  topk, with the reconstruction asked of nested prefixes of the dictionary too (Bussmann et al. 2025)

``aux_k`` adds Gao et al.'s auxiliary loss: the latents dead for a while try to rebuild what the live ones miss.
Inputs are normalized so a vector's mean squared length is D (entries of order 1).  Everything is seeded.
"""

from __future__ import annotations

import math

import numpy as np


def _jump_fns():
    import torch

    class Jump(torch.autograd.Function):
        @staticmethod
        def forward(ctx, z, th, eps):
            ctx.save_for_backward(z, th)
            ctx.eps = eps
            return z * (z > th)

        @staticmethod
        def backward(ctx, g):
            z, th = ctx.saved_tensors
            k = (((z - th).abs() < ctx.eps / 2).float() / ctx.eps)
            return g * (z > th), (-th * k * g).sum(0), None

    class Step(torch.autograd.Function):
        @staticmethod
        def forward(ctx, z, th, eps):
            ctx.save_for_backward(z, th)
            ctx.eps = eps
            return (z > th).float()

        @staticmethod
        def backward(ctx, g):
            z, th = ctx.saved_tensors
            k = (((z - th).abs() < ctx.eps / 2).float() / ctx.eps)
            return torch.zeros_like(z), (-k * g).sum(0), None

    return Jump.apply, Step.apply


class Dict:
    """A trained dictionary: ``encode`` (x -> f), ``decode`` (f -> x_hat), parameters as tensors."""

    def __init__(self, kind, We, be, Wd, bd, param, theta=None, thresh=None, prefixes=None):
        self.kind, self.We, self.be, self.Wd, self.bd, self.param = kind, We, be, Wd, bd, param
        self.theta, self.thresh, self.prefixes = theta, thresh, prefixes

    def encode(self, x):
        return encode(self, x)

    def decode(self, f):
        return f @ self.Wd + self.bd

    def state(self):
        d = dict(kind=self.kind, We=self.We, be=self.be, Wd=self.Wd, bd=self.bd, param=self.param,
                 auto=getattr(self, "auto", True))
        if self.theta is not None:
            d["theta"] = self.theta
        if self.thresh is not None:
            d["thresh"] = self.thresh
        return d

    @staticmethod
    def from_state(d):
        out = Dict(d["kind"], d["We"], d["be"], d["Wd"], d["bd"], d["param"], d.get("theta"), d.get("thresh"))
        out.auto = d.get("auto", True)
        return out


def train(X, kind, param, F=512, steps=2000, batch=1024, lr=1e-3, seed=0, Y=None, aux_k=0, prefixes=None,
          eps=0.05, log_every=50, snap_every=0, dead_window=200):
    """Train one dictionary on rows of ``X`` (N, D) (float tensor); with ``Y`` (N, D'), a transcoder or a crosscoder
    that reads X and rebuilds Y (default: Y = X, an autoencoder).  ``param``: lam (l1, jumprelu) or k (topk,
    batchtopk, matryoshka).  Returns the Dict and a record of training (loss, L0 and unexplained variance every
    ``log_every`` steps; with ``snap_every``, copies of the decoder along the way)."""
    import torch

    Y = X if Y is None else Y
    D, Do = X.shape[1], Y.shape[1]
    g = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    Wd = torch.nn.Parameter(torch.randn(F, Do, generator=g) / math.sqrt(Do))
    with torch.no_grad():
        Wd /= Wd.norm(dim=1, keepdim=True)
    if Do == D:
        We = torch.nn.Parameter(Wd.detach().clone().T.contiguous())
    else:
        We = torch.nn.Parameter(torch.randn(D, F, generator=g) / math.sqrt(D))
    be = torch.nn.Parameter(torch.zeros(F))
    bd = torch.nn.Parameter(Y[torch.randperm(len(Y), generator=g)[:4096]].mean(0).clone())
    params = [We, be, Wd, bd]
    log_th = None
    if kind == "jumprelu":
        log_th = torch.nn.Parameter(torch.full((F,), math.log(0.5)))
        jump, step_fn = _jump_fns()
    groups = [dict(params=params)] + ([dict(params=[log_th], lr=10 * lr)] if log_th is not None else [])
    opt = torch.optim.Adam(groups, lr=lr)
    var = float(((Y - Y.mean(0)) ** 2).sum(1).mean())
    last_fire = torch.zeros(F)
    thresh_run = None
    rec = dict(step=[], loss=[], l0=[], fvu=[], snaps=[], snap_steps=[])
    auto = Do == D and Y is X

    for s in range(steps + 1):
        idx = torch.randint(0, len(X), (batch,), generator=g)
        x, y = X[idx], Y[idx]
        z = ((x - bd) if auto else x) @ We + be
        if kind == "l1":
            f = torch.relu(z)
        elif kind == "jumprelu":
            th = log_th.exp()
            f = jump(z, th, eps)
        elif kind == "batchtopk":
            zr = torch.relu(z)
            k_all = int(param) * batch
            v, i = torch.topk(zr.flatten(), k_all)
            f = torch.zeros_like(zr).flatten().scatter(0, i, v).view_as(zr)
            mn = float(v[-1])
            thresh_run = mn if thresh_run is None else 0.99 * thresh_run + 0.01 * mn
        else:  # topk, matryoshka
            v, i = torch.topk(z, int(param), dim=1)
            f = torch.zeros_like(z).scatter(1, i, torch.relu(v))
        dec = Wd / Wd.norm(dim=1, keepdim=True)
        yh = f @ dec + bd
        err = ((yh - y) ** 2).sum(1).mean()
        loss = err
        if kind == "matryoshka":
            for m in prefixes:
                loss = loss + ((f[:, :m] @ dec[:m] + bd - y) ** 2).sum(1).mean()
            loss = loss / (1 + len(prefixes))
        if kind == "l1":
            loss = loss + param * f.sum(1).mean()
        if kind == "jumprelu":
            loss = loss + param * step_fn(z, th, eps).sum(1).mean()
        fired = (f > 0).any(0)
        last_fire = torch.where(fired, torch.zeros_like(last_fire), last_fire + 1)
        if aux_k:
            dead = last_fire > dead_window
            if dead.any():
                e = (y - yh).detach()
                zd = z.masked_fill(~dead[None], -1e9)
                ka = min(aux_k, int(dead.sum()))
                v2, i2 = torch.topk(zd, ka, dim=1)
                fa = torch.zeros_like(z).scatter(1, i2, torch.relu(v2))
                ea = fa @ dec
                loss = loss + (1 / 32) * ((ea - e) ** 2).sum(1).mean() / (e ** 2).sum(1).mean().clamp_min(1e-9)
        if s % log_every == 0:
            rec["step"].append(s)
            rec["loss"].append(float(loss.detach()))
            rec["l0"].append(float((f > 0).float().sum(1).mean()))
            rec["fvu"].append(float(err) / var)
        if snap_every and s % snap_every == 0:
            rec["snaps"].append(dec.detach().numpy().astype(np.float16))
            rec["snap_steps"].append(s)
        if s == steps:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        dec = Wd / Wd.norm(dim=1, keepdim=True)
        out = Dict(kind, We.detach().clone(), be.detach().clone(), dec.detach().clone(), bd.detach().clone(), param,
                   theta=log_th.exp().detach().clone() if log_th is not None else None,
                   thresh=thresh_run)
    out.auto = auto
    return out, rec


def encode(d: Dict, x):
    """The code of rows ``x`` (an autoencoder subtracts b_d first; a transcoder or crosscoder reads x as it is)."""
    import torch

    z = ((x - d.bd) if getattr(d, "auto", True) and d.bd.shape[-1] == x.shape[-1] else x) @ d.We + d.be
    if d.kind == "l1":
        return torch.relu(z)
    if d.kind == "jumprelu":
        return z * (z > d.theta)
    if d.kind == "batchtopk":
        return torch.relu(z) * (z > d.thresh)
    v, i = torch.topk(z, int(d.param), dim=1)
    return torch.zeros_like(z).scatter(1, i, torch.relu(v))


def evaluate(d: Dict, X, Y=None, chunk=8192):
    """L0, unexplained variance, latents that never fire, and shrinkage (the factor that best rescales the
    reconstruction: 1 means none) on rows ``X``."""
    import torch

    Y = X if Y is None else Y
    n_on = torch.zeros(d.We.shape[1])
    l0 = err = var = num = den = 0.0
    mu = Y.mean(0)
    with torch.no_grad():
        for i in range(0, len(X), chunk):
            x, y = X[i:i + chunk], Y[i:i + chunk]
            f = encode(d, x)
            yh = f @ d.Wd + d.bd
            n_on += (f > 0).float().sum(0)
            l0 += float((f > 0).float().sum())
            err += float(((yh - y) ** 2).sum())
            var += float(((y - mu) ** 2).sum())
            hc, yc = yh - d.bd, y - d.bd
            num += float((hc * yc).sum())
            den += float((hc * hc).sum())
    return dict(l0=l0 / len(X), fvu=err / var, dead=int((n_on == 0).sum()), shrink=num / max(den, 1e-12),
                freq=(n_on / len(X)).numpy())


def match(Da, Db):
    """For each decoder row of Da, its best cosine with any row of Db."""
    A = Da / np.linalg.norm(Da, axis=1, keepdims=True)
    B = Db / np.linalg.norm(Db, axis=1, keepdims=True)
    return (A @ B.T).max(1)
