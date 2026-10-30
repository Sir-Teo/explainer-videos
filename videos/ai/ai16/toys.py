"""The small, exact experiments of Part 16: the 1991 mixture of experts on a curve, and the router's gradient checked."""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------------------
# 1991: competing local experts on a curve
# ---------------------------------------------------------------------------
N_EXP_91 = 4
SNAPS_91 = (0, 25, 50, 100, 200, 400, 800, 1600, 3000)


def target_91(x):
    """Three regimes a single straight line can't fit: a rise, a plateau, a fall (and a little noise)."""
    return np.where(x < -0.35, 1.6 * (x + 0.35) + 0.5, np.where(x < 0.3, 0.5 - 0.6 * x ** 2, -1.4 * (x - 0.3) + 0.446))


def mix1991(loss: str, seed: int, steps=3000, n=256, sigma=0.15):
    """A softmax gate over x and four linear experts, trained by Adam with either the 1991 competitive loss,
    -log sum_i g_i exp(-(y - o_i)^2 / 2 sigma^2), or the cooperative one, (y - sum_i g_i o_i)^2 / 2."""
    import torch

    torch.manual_seed(seed)
    g = np.random.default_rng(seed)
    x = np.sort(g.uniform(-1, 1, n))
    y = target_91(x) + g.normal(0, 0.03, n)
    X, Y = torch.tensor(x, dtype=torch.float64), torch.tensor(y, dtype=torch.float64)
    a = torch.nn.Parameter(torch.randn(N_EXP_91, dtype=torch.float64) * 0.3)
    b = torch.nn.Parameter(torch.randn(N_EXP_91, dtype=torch.float64) * 0.3)
    u = torch.nn.Parameter(torch.randn(N_EXP_91, dtype=torch.float64) * 0.5)  # gate logits: u_i x + v_i
    v = torch.nn.Parameter(torch.randn(N_EXP_91, dtype=torch.float64) * 0.5)
    opt = torch.optim.Adam([a, b, u, v], lr=0.02)
    grid = np.linspace(-1, 1, 201)
    G = torch.tensor(grid, dtype=torch.float64)
    snaps = []
    for step in range(steps + 1):
        o = a[None] * X[:, None] + b[None]
        gt = torch.softmax(u[None] * X[:, None] + v[None], -1)
        if loss == "compete":
            L = -torch.logsumexp(torch.log(gt) - (Y[:, None] - o) ** 2 / (2 * sigma ** 2), -1).mean()
        else:
            L = 0.5 * ((Y - (gt * o).sum(-1)) ** 2).mean()
        if step in SNAPS_91:
            with torch.no_grad():
                gg = torch.softmax(u[None] * G[:, None] + v[None], -1).numpy()
                oo = (a[None] * G[:, None] + b[None]).numpy()
                mix = (gg * oo).sum(-1)
                mse = float(((Y - (gt * o).sum(-1)) ** 2).mean())
            snaps.append(dict(step=step, gate=gg, experts=oo, mix=mix, mse=mse, sharp=float(gg.max(1).mean())))
        opt.zero_grad()
        L.backward()
        opt.step()
    return dict(x=x, y=y, grid=grid, snaps=snaps)


def compute_mix1991():
    out = dict(snaps=list(SNAPS_91), seeds=[0, 1, 2], n_experts=N_EXP_91)
    for loss in ("compete", "cooperate"):
        for s in (0, 1, 2):
            r = mix1991(loss, s)
            out[f"{loss}_s{s}_sharp"] = [sn["sharp"] for sn in r["snaps"]]
            out[f"{loss}_s{s}_mse"] = [sn["mse"] for sn in r["snaps"]]
            # how many experts own some stretch of the line at the end (are the most trusted somewhere)
            last = r["snaps"][-1]
            out[f"{loss}_s{s}_owners"] = int(len(np.unique(last["gate"].argmax(1))))
            if s == 0:
                out["x"], out["y"], out["grid"] = r["x"], r["y"], r["grid"]
                out[f"{loss}_gate"] = np.array([sn["gate"] for sn in r["snaps"]])
                out[f"{loss}_experts"] = np.array([sn["experts"] for sn in r["snaps"]])
                out[f"{loss}_mix"] = np.array([sn["mix"] for sn in r["snaps"]])
    for loss in ("compete", "cooperate"):
        out[f"{loss}_sharp_final"] = [out[f"{loss}_s{s}_sharp"][-1] for s in (0, 1, 2)]
        out[f"{loss}_mse_final"] = [out[f"{loss}_s{s}_mse"][-1] for s in (0, 1, 2)]
    return out


# ---------------------------------------------------------------------------
# The router's gradient through a top-k gate
# ---------------------------------------------------------------------------
def gate_fn(kind: str, k: int):
    """Gates from router logits s for the chosen set K (top-k of s): 'softmax-k' (softmax over the chosen, Mixtral),
    'sigmoid-k' (sigmoids renormalized over the chosen, DeepSeek-V3), 'switch' (top-1, the full softmax's p_i),
    'top1-renorm' (top-1, renormalized: always exactly 1)."""
    import torch

    def f(s, K):
        if kind == "softmax-k":
            return torch.softmax(s[K], -1)
        if kind == "sigmoid-k":
            g = torch.sigmoid(s[K])
            return g / g.sum()
        if kind == "switch":
            return torch.softmax(s, -1)[K]
        if kind == "top1-renorm":
            return torch.softmax(s[K], -1)
        raise ValueError(kind)
    return f


def analytic(kind, s, K, u):
    """dL/ds from the formulas on screen, with u_i = (dL/dy) . E_i(x) for the chosen experts (in K's order)."""
    s = np.asarray(s, float)
    out = np.zeros_like(s)
    if kind in ("softmax-k", "top1-renorm"):
        e = np.exp(s[K] - s[K].max())
        g = e / e.sum()
        out[K] = g * (u - (g * u).sum())
    elif kind == "sigmoid-k":
        sg = 1 / (1 + np.exp(-s[K]))
        g = sg / sg.sum()
        out[K] = (1 - sg) * g * (u - (g * u).sum())
    elif kind == "switch":
        e = np.exp(s - s.max())
        p = e / e.sum()
        i = K[0]
        out = u[0] * p[i] * ((np.arange(len(s)) == i) - p)
    return out


def compute_gradcheck():
    """For one token, E = 8 experts (random linear maps), a squared-error loss: the router's gradient by autograd,
    by the formulas, and by central finite differences (float64); and how many of the router's logits get any
    gradient at all, over a batch."""
    import torch

    torch.manual_seed(16)
    E, d = 8, 6
    g = torch.Generator().manual_seed(16)
    A = torch.randn(E, d, d, generator=g, dtype=torch.float64)
    x = torch.randn(d, generator=g, dtype=torch.float64)
    t = torch.randn(d, generator=g, dtype=torch.float64)
    W = torch.randn(E, d, generator=g, dtype=torch.float64)
    s0 = (W @ x).detach()
    out = dict(E=E, logits=s0.numpy(), kinds=[])
    for kind, k in (("softmax-k", 2), ("sigmoid-k", 2), ("switch", 1), ("top1-renorm", 1)):
        f = gate_fn(kind, k)
        K = torch.topk(s0, k).indices

        def loss(s):
            gt = f(s, K)
            y = sum(gt[j] * (A[K[j]] @ x) for j in range(k))
            return 0.5 * ((y - t) ** 2).sum(), y

        s = s0.clone().requires_grad_(True)
        L, y = loss(s)
        L.backward()
        auto = s.grad.numpy().copy()
        dy = (y - t).detach()
        u = np.array([float(dy @ (A[K[j]] @ x)) for j in range(k)])
        ana = analytic(kind, s0.numpy(), K.numpy(), u)
        fd = np.zeros(E)
        h = 1e-6
        for i in range(E):
            sp, sm = s0.clone(), s0.clone()
            sp[i] += h
            sm[i] -= h
            fd[i] = (float(loss(sp)[0]) - float(loss(sm)[0])) / (2 * h)
        scale = max(np.abs(fd).max(), 1e-12)
        out["kinds"].append(kind)
        out[kind] = dict(k=k, chosen=K.numpy().tolist(), auto=auto.tolist(), analytic=ana.tolist(), fd=fd.tolist(),
                         err_auto=float(np.abs(auto - fd).max() / scale), err_analytic=float(np.abs(ana - fd).max() / scale),
                         nonzero=int((np.abs(fd) > 1e-9).sum()), norm=float(np.abs(fd).sum()))
        assert out[kind]["err_auto"] < 1e-6 and out[kind]["err_analytic"] < 1e-6, (kind, out[kind])
    # our MoE layer (nets.MoE), in float64: autograd against finite differences on its router's weights
    from videos.ai.ai16.nets import Cfg, MoE

    torch.manual_seed(0)
    m = MoE(Cfg(d=8, E=8, k=2, he=16, gate="sigmoid", balance="bias")).double()
    xx = torch.randn(1, 12, 8, dtype=torch.float64)
    tgt = torch.randn(1, 12, 8, dtype=torch.float64)
    L = 0.5 * ((m(xx) - tgt) ** 2).sum()
    L.backward()
    Wr = m.router.weight
    auto = Wr.grad.detach().clone()
    fd = torch.zeros_like(auto)
    h = 1e-6
    with torch.no_grad():
        for i in range(Wr.shape[0]):
            for j in range(Wr.shape[1]):
                Wr[i, j] += h
                lp = float(0.5 * ((m(xx) - tgt) ** 2).sum())
                Wr[i, j] -= 2 * h
                lm = float(0.5 * ((m(xx) - tgt) ** 2).sum())
                Wr[i, j] += h
                fd[i, j] = (lp - lm) / (2 * h)
    out["layer_err"] = float((auto - fd).abs().max() / fd.abs().max())
    assert out["layer_err"] < 1e-5, out["layer_err"]
    # over a batch of 4,096 tokens: the share of (token, expert) logits that get a gradient
    tok = torch.randn(4096, d, generator=g, dtype=torch.float64)
    S = tok @ W.T
    out["batch_share"] = {f"k{k}": k / E for k in (1, 2)}
    out["batch_counts"] = np.bincount(torch.topk(S, 2, -1).indices.reshape(-1).numpy(), minlength=E)
    return out
