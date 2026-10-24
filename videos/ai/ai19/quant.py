"""Quantization of the novels model, the methods of Part 19 written small: round to nearest at any granularity, GPTQ
(Optimal Brain Surgeon one column at a time), AWQ's activation-aware scales, SmoothQuant, LLM.int8()'s outlier
channels, rotations of the residual stream (QuaRot's Hadamard, random, learned as in SpinQuant), and the 4-bit float
formats (``formats.py``).

A quantized model is a copy of the novels model whose linear layers (the 36 matrices of its six blocks; the
embedding and the output head stay in 32 bits, as is usual) are replaced by :class:`QLinear`: the weight rounded
once, offline, and optionally the input rounded on every call (activation quantization), after an optional smoothing
scale or rotation.
"""

from __future__ import annotations

import copy
import math

import numpy as np


# ---------------------------------------------------------------------------
# Rounding
# ---------------------------------------------------------------------------
def qmax(bits: int) -> int:
    return 2 ** (bits - 1) - 1


def rtn(W, bits: int, group: int | str = "row"):
    """Symmetric round to nearest, absmax scale: one scale per tensor ("tensor"), per output row ("row"), or per
    ``group`` consecutive inputs of a row.  Works on numpy arrays; returns the dequantized weights."""
    W = np.asarray(W, np.float64)
    q = qmax(bits)
    if group == "tensor":
        s = np.abs(W).max() / q
        return np.clip(np.round(W / s), -q - 1, q) * s
    if group == "row":
        s = np.abs(W).max(1, keepdims=True) / q
        s = np.where(s > 0, s, 1.0)
        return np.clip(np.round(W / s), -q - 1, q) * s
    r, c = W.shape
    Wg = W.reshape(r, c // group, group)
    s = np.abs(Wg).max(2, keepdims=True) / q
    s = np.where(s > 0, s, 1.0)
    return (np.clip(np.round(Wg / s), -q - 1, q) * s).reshape(r, c)


def scales_of(W, bits, group="row"):
    """The step sizes Delta that ``rtn`` uses, one per weight (for the Delta^2/12 prediction)."""
    W = np.asarray(W, np.float64)
    q = qmax(bits)
    if group == "tensor":
        return np.full_like(W, np.abs(W).max() / q)
    if group == "row":
        return np.broadcast_to(np.abs(W).max(1, keepdims=True) / q, W.shape)
    r, c = W.shape
    s = np.abs(W.reshape(r, c // group, group)).max(2, keepdims=True) / q
    return np.broadcast_to(s, (r, c // group, group)).reshape(r, c)


def bits_per_weight(bits, group, cols, scale_bits=16):
    """Storage per weight, scales included."""
    if group == "tensor":
        return float(bits)
    if group == "row":
        return bits + scale_bits / cols
    return bits + scale_bits / group


def fake_act(x, bits: int, keep=None):
    """Activations rounded per token (one absmax scale per row of ``x``), in torch; ``keep``: channels left as they
    are (LLM.int8()'s outliers).  Straight-through: the gradient passes the rounding unchanged."""
    import torch

    q = qmax(bits)
    xq = x
    if keep is not None:
        mask = torch.ones(x.shape[-1], dtype=torch.bool)
        mask[keep] = False
        xr = x * mask
    else:
        xr = x
    s = xr.abs().amax(-1, keepdim=True).clamp_min(1e-8) / q
    y = torch.clamp(torch.round(xr / s), -q - 1, q) * s
    if keep is not None:
        y = torch.where(mask, y, x)
    return xq + (y - xq).detach()


def fake_w(W, bits: int):
    """Weights rounded per row in torch, straight-through (for learning a rotation)."""
    import torch

    q = qmax(bits)
    s = W.abs().amax(-1, keepdim=True).clamp_min(1e-8) / q
    return W + (torch.clamp(torch.round(W / s), -q - 1, q) * s - W).detach()


# ---------------------------------------------------------------------------
# The quantized linear layer, and model surgery
# ---------------------------------------------------------------------------
def linear_names(model) -> list[str]:
    return [n for n, mod in model.named_modules() if n.startswith("blocks") and type(mod).__name__ == "Linear"]


def make_qlinear():
    import torch
    import torch.nn as nn

    class QLinear(nn.Module):
        """y = Q_a(x R / s) W_q^T: an optional online rotation R, smoothing scale s, activation rounding to
        ``a_bits`` per token (``keep``: channels exempt), and a weight already rounded (dequantized) offline."""

        def __init__(self, Wq, R=None, s=None, a_bits=0, keep=None):
            super().__init__()
            self.register_buffer("W", torch.as_tensor(Wq, dtype=torch.float32))
            self.R = None if R is None else torch.as_tensor(R, dtype=torch.float32)
            self.s = None if s is None else torch.as_tensor(s, dtype=torch.float32)
            self.a_bits, self.keep = a_bits, keep

        def forward(self, x):
            if self.R is not None:
                x = x @ self.R
            if self.s is not None:
                x = x / self.s
            if self.a_bits:
                x = fake_act(x, self.a_bits, self.keep)
            return x @ self.W.T

    return QLinear


def set_module(model, name, new):
    parent, _, attr = name.rpartition(".")
    setattr(model.get_submodule(parent), attr, new)


def quantized(model, weights: dict, extra: dict | None = None):
    """A copy of ``model`` with each named linear replaced: ``weights[name]`` the rounded weight (numpy), ``extra[name]``
    keyword arguments for QLinear (R, s, a_bits, keep)."""
    QLinear = make_qlinear()
    m = copy.deepcopy(model)
    for name, Wq in weights.items():
        set_module(m, name, QLinear(Wq, **(extra or {}).get(name, {})))
    return m.eval()


# ---------------------------------------------------------------------------
# Calibration: what each linear layer sees
# ---------------------------------------------------------------------------
def collect(model, windows, batch=8):
    """For every block linear: H = E[x x^T] of its inputs, the channel-wise max |x| and mean |x|, over ``windows``."""
    import torch

    names = linear_names(model)
    acc = {n: dict(H=0.0, amax=0.0, amean=0.0, n=0) for n in names}

    def hook(name):
        def f(_m, inp, _o):
            x = inp[0].detach().reshape(-1, inp[0].shape[-1]).double()
            a = acc[name]
            a["H"] = a["H"] + x.T @ x
            a["amax"] = torch.maximum(torch.as_tensor(a["amax"], dtype=torch.float64), x.abs().amax(0))
            a["amean"] = a["amean"] + x.abs().sum(0)
            a["n"] += len(x)
        return f

    hs = [model.get_submodule(n).register_forward_hook(hook(n)) for n in names]
    with torch.inference_mode():
        for i in range(0, len(windows), batch):
            model(windows[i:i + batch, :-1])
    for h in hs:
        h.remove()
    out = {}
    for n, a in acc.items():
        out[n] = dict(H=(a["H"] / a["n"]).numpy(), amax=np.asarray(a["amax"]), amean=(a["amean"] / a["n"]).numpy())
    return out


def out_err(W, Q, H) -> float:
    """Relative output error of a rounded layer on the calibration inputs: ||(W - Q) X|| / ||W X||, via H."""
    E = W - Q
    return float(math.sqrt(np.trace(E @ H @ E.T) / np.trace(W @ H @ W.T)))


# ---------------------------------------------------------------------------
# GPTQ: Optimal Brain Surgeon, one input column at a time
# ---------------------------------------------------------------------------
def gptq(W, H, bits: int, group: int | str = "row", damp: float = 0.01, trace_row: int | None = None):
    """GPTQ (Frantar et al. 2022) for y = W x with input second moment H.  Columns are rounded left to right; after
    each, its rounding error is spread over the columns not yet rounded, along row j of the upper Cholesky factor U of
    H^-1 (H^-1 = U^T U): the Optimal Brain Surgeon update, which keeps the layer's output error, measured with H,
    as small as possible.  Scales: per row (from the original weights) or per group (from the updated weights at the
    group's start, as GPTQ does).  ``trace_row``: also return that row after each column, for the picture."""
    W = np.asarray(W, np.float64).copy()
    r, n = W.shape
    q = qmax(bits)
    H = H + damp * np.mean(np.diag(H)) * np.eye(n)
    U = np.linalg.cholesky(np.linalg.inv(H)).T
    Q = np.zeros_like(W)
    s = np.abs(W).max(1) / q if group == "row" else None
    trace = []
    for j in range(n):
        if group != "row" and j % group == 0:
            s = np.abs(W[:, j:j + group]).max(1) / q
        sj = np.where(s > 0, s, 1.0)
        w = W[:, j]
        qj = np.clip(np.round(w / sj), -q - 1, q) * sj
        Q[:, j] = qj
        err = (w - qj) / U[j, j]
        W[:, j + 1:] -= np.outer(err, U[j, j + 1:])
        if trace_row is not None:
            trace.append(np.concatenate([Q[trace_row, :j + 1], W[trace_row, j + 1:]]))
    return (Q, np.array(trace)) if trace_row is not None else Q


# ---------------------------------------------------------------------------
# AWQ: scale the input channels that matter before rounding
# ---------------------------------------------------------------------------
def awq(W, H, amean, bits: int, group: int | str = "row", grid: int = 20):
    """AWQ (Lin et al. 2023): multiply input channel j of W by s_j = mean|x_j|^alpha (dividing the input by s_j,
    which costs nothing: it folds into the layer before), round, and choose alpha in [0, 1] by the output error on
    the calibration inputs.  Returns (rounded weight in the original basis, alpha)."""
    best = None
    for a in np.linspace(0, 1, grid + 1):
        s = np.maximum(amean, 1e-8) ** a
        s = s / math.sqrt(s.max() * s.min())
        Q = rtn(W * s, bits, group) / s
        e = out_err(W, Q, H)
        if best is None or e < best[0]:
            best = (e, Q, float(a))
    return best[1], best[2]


def smooth_scales(amax, W, alpha=0.5):
    """SmoothQuant (Xiao et al. 2022): s_j = max|X_j|^alpha / max|W_:j|^(1 - alpha), so that X / s and W s share the
    range of channel j between them."""
    wmax = np.abs(W).max(0)
    s = np.maximum(amax, 1e-5) ** alpha / np.maximum(wmax, 1e-5) ** (1 - alpha)
    return np.maximum(s, 1e-5)


# ---------------------------------------------------------------------------
# Rotations of the residual stream (QuaRot, SpinQuant)
# ---------------------------------------------------------------------------
def hadamard(n: int):
    Hm = np.array([[1.0]])
    while Hm.shape[0] < n:
        Hm = np.block([[Hm, Hm], [Hm, -Hm]])
    assert Hm.shape[0] == n, "Sylvester's construction needs a power of two"
    return Hm / math.sqrt(n)


def random_orthogonal(n: int, seed: int):
    g = np.random.default_rng(seed)
    Qm, R = np.linalg.qr(g.standard_normal((n, n)))
    return Qm * np.sign(np.diag(R))


def fold_norms(model):
    """A copy of the model with every RMSNorm's gain folded into the linear layers it feeds (W <- W diag(gamma)), and
    the gains set to one: the same function, now invariant under rotating the residual stream."""
    import torch

    m = copy.deepcopy(model)
    with torch.no_grad():
        for b in m.blocks:
            g1, g2 = b.n1.weight.clone(), b.n2.weight.clone()
            b.attn.qkv.weight.mul_(g1)
            b.mlp.gate.weight.mul_(g2)
            b.mlp.up.weight.mul_(g2)
            b.n1.weight.fill_(1.0)
            b.n2.weight.fill_(1.0)
        m.head.weight.mul_(m.norm.weight)
        m.norm.weight.fill_(1.0)
    return m.eval()


def rotate(model, Rm):
    """QuaRot's computational invariance: with the norms folded, rotate the residual stream by the orthogonal ``Rm``
    (x -> x R).  Linears that read the stream become W R; those that write to it, R^T W; the embedding E R; the head
    W R.  RMSNorm commutes with R, so the output is unchanged (``check``)."""
    import torch

    m = fold_norms(model)
    R = torch.as_tensor(Rm, dtype=torch.float32)
    with torch.no_grad():
        m.emb.weight.copy_(m.emb.weight @ R)
        for b in m.blocks:
            for lin in (b.attn.qkv, b.mlp.gate, b.mlp.up):
                lin.weight.copy_(lin.weight @ R)
            for lin in (b.attn.out, b.mlp.down):
                lin.weight.copy_(R.T @ lin.weight)
        m.head.weight.copy_(m.head.weight @ R)
    return m.eval()


def crest(X) -> float:
    """How peaked a set of vectors is: the mean over rows of max |x| / rms(x) (1 for a flat vector, sqrt(n) for a
    single spike)."""
    X = np.asarray(X, np.float64)
    return float(np.mean(np.abs(X).max(1) / np.sqrt((X ** 2).mean(1) + 1e-30)))


# ---------------------------------------------------------------------------
# Whole-model recipes
# ---------------------------------------------------------------------------
def weight_only(model, fn):
    """Round every block linear with ``fn(name, W) -> Wq`` (numpy), activations untouched."""
    ws = {n: fn(n, model.get_submodule(n).weight.detach().numpy().astype(np.float64)) for n in linear_names(model)}
    return quantized(model, ws)


def w_a(model, w_bits, a_bits, stats=None, method="plain", alpha=0.5, keep_share=0.01, down_R=None, w_fn=None):
    """Weights rounded per row to ``w_bits``, every block linear's input rounded per token to ``a_bits``.
    ``method``: "plain"; "smooth" (SmoothQuant scales from ``stats``); "keep" (the largest ``keep_share`` of input
    channels by max |x| left unrounded, as LLM.int8() keeps its outliers in 16 bits).  ``down_R``: an online rotation
    of the down projection's input (QuaRot rotates it with a Hadamard transform at run time).  ``w_fn(name, W)``
    rounds the weights instead of plain rounding (e.g. GPTQ)."""
    ws, ex = {}, {}
    for n in linear_names(model):
        W = model.get_submodule(n).weight.detach().numpy().astype(np.float64)
        kw = dict(a_bits=a_bits)
        Wt = W
        if down_R is not None and n.endswith("mlp.down"):
            kw["R"] = down_R
            Wt = W @ down_R
        if method == "smooth":
            s = smooth_scales(stats[n]["amax"], Wt, alpha)
            kw["s"] = s
            Wt = Wt * s
        elif method == "keep":
            k = max(1, int(round(keep_share * W.shape[1])))
            kw["keep"] = np.argsort(-stats[n]["amax"])[:k].copy()
        ws[n] = w_fn(n, Wt) if w_fn else rtn(Wt, w_bits, "row")
        ex[n] = kw
    return quantized(model, ws, ex)
