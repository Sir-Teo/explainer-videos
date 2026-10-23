"""Sets and graphs (Part 25, chapters 3-6): Deep Sets against an MLP, Weisfeiler-Leman colour refinement, message
passing networks on synthetic graphs, over-smoothing and graph attention.  Small, dense, CPU-only; seeded.
"""

from __future__ import annotations

import math
import time
from collections import Counter

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def mlp(sizes, act=nn.ReLU, last_act=False) -> nn.Sequential:
    layers = []
    for i, (a, b) in enumerate(zip(sizes, sizes[1:])):
        layers.append(nn.Linear(a, b))
        if i < len(sizes) - 2 or last_act:
            layers.append(act())
    return nn.Sequential(*layers)


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters())


# ===========================================================================
# Sets: four shapes of sixteen points
# ===========================================================================
SET_N = 16
SHAPES = ("ring", "disc", "segment", "two blobs")


def point_sets(count: int, rng: np.random.Generator):
    """``count`` sets of 16 points in the plane, each drawn from one of four shapes and turned by a random angle; the
    points of a set come in random order (a set has no order).  Returns (X: count x 16 x 2, labels)."""
    y = rng.integers(0, 4, count)
    X = np.zeros((count, SET_N, 2))
    for k in range(count):
        c = y[k]
        if c == 0:  # ring
            a = rng.uniform(0, 2 * np.pi, SET_N)
            r = 1.0 + rng.normal(0, 0.05, SET_N)
            P = np.c_[r * np.cos(a), r * np.sin(a)]
        elif c == 1:  # filled disc
            a = rng.uniform(0, 2 * np.pi, SET_N)
            r = np.sqrt(rng.uniform(0, 1, SET_N))
            P = np.c_[r * np.cos(a), r * np.sin(a)]
        elif c == 2:  # a segment
            t = rng.uniform(-1, 1, SET_N)
            P = np.c_[t, rng.normal(0, 0.05, SET_N)]
        else:  # two blobs
            s = rng.choice([-0.7, 0.7], SET_N)
            P = np.c_[s + rng.normal(0, 0.2, SET_N), rng.normal(0, 0.2, SET_N)]
        th = rng.uniform(0, 2 * np.pi)
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        P = P @ R.T
        X[k] = P[rng.permutation(SET_N)]
    return X.astype(np.float32), y


class SetMLP(nn.Module):
    """The 32 coordinates in a fixed order: a plain network, which sees a reordered set as a new input."""

    def __init__(self, hidden=256):
        super().__init__()
        self.net = mlp([SET_N * 2, hidden, hidden, 4])

    def forward(self, X):
        return self.net(X.reshape(X.shape[0], -1))


class DeepSets(nn.Module):
    """rho(sum_i phi(x_i)) (Zaheer et al. 2017): the sum forgets the order, so reordering can't change the output.
    The pooled vector is layer-normalized before rho (still order-free); without it some seeds stall below 90%."""

    def __init__(self, hidden=128):
        super().__init__()
        self.phi = mlp([2, hidden, hidden], last_act=True)
        self.ln = nn.LayerNorm(hidden)
        self.rho = mlp([hidden, hidden, 4])

    def latent(self, X):
        return self.phi(X).sum(1) / X.shape[1]

    def forward(self, X):
        return self.rho(self.ln(self.latent(X)))


SET_MODELS = {"mlp": SetMLP, "mlp_aug": SetMLP, "deepsets": DeepSets}


SET_STEPS = 6000


def train_sets(kind: str, X, y, seed: int, steps=SET_STEPS, batch=64, lr=1e-3, val=None, every=100):
    """``val`` = (X, y) of held-out sets: record test accuracy every ``every`` steps (evaluation draws no random
    numbers, so the trained network is the same with or without it)."""
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(500 + seed)
    m = SET_MODELS[kind]()
    opt = torch.optim.Adam(m.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)  # so the last step is not a random moment
    Xt, yt = torch.from_numpy(X), torch.from_numpy(y).long()
    t0 = time.time()
    curve = []
    for s in range(steps + 1):
        if val is not None and s % every == 0:
            with torch.no_grad():
                curve.append((s, float((m(torch.from_numpy(val[0])).argmax(1).numpy() == val[1]).mean())))
        if s == steps:
            break
        j = torch.randint(0, len(Xt), (min(batch, len(Xt)),), generator=gen)
        xb = Xt[j]
        if kind == "mlp_aug":  # a fresh order for every set, every time it is seen
            perm = torch.argsort(torch.rand(xb.shape[0], SET_N, generator=gen), 1)
            xb = torch.gather(xb, 1, perm.unsqueeze(-1).expand(-1, -1, 2))
        loss = F.cross_entropy(m(xb), yt[j])
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    m.eval()
    return m, dict(secs=time.time() - t0, params=n_params(m), curve=curve)


def set_scores(m, Xte, yte, gen: torch.Generator, n_perm=20, n_sets=500):
    """Test accuracy, and how often the predicted class changes when the same sets are presented in other orders."""
    X = torch.from_numpy(Xte)
    with torch.no_grad():
        acc = float((m(X).argmax(1).numpy() == yte).mean())
        Xs = X[:n_sets]
        base = m(Xs).argmax(1)
        flipped = torch.zeros(n_sets, dtype=torch.bool)
        spread = []
        for _ in range(n_perm):
            perm = torch.argsort(torch.rand(n_sets, SET_N, generator=gen), 1)
            Xp = torch.gather(Xs, 1, perm.unsqueeze(-1).expand(-1, -1, 2))
            out = m(Xp)
            flipped |= out.argmax(1) != base
            spread.append(F.softmax(out, -1))
        prob_sd = float(torch.stack(spread).std(0).max(1).values.mean())
    return dict(acc=acc, flip=float(flipped.float().mean()), prob_sd=prob_sd)


# ===========================================================================
# Graphs: small helpers
# ===========================================================================
def edges_to_adj(n: int, edges) -> np.ndarray:
    A = np.zeros((n, n), np.float32)
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    return A


def cycle_edges(lengths, offset=0):
    out, k = [], offset
    for L in lengths:
        out += [(k + i, k + (i + 1) % L) for i in range(L)]
        k += L
    return out


def decalin():
    """Two fused six-rings (bicyclo[4.4.0]decane): ten carbons, eleven bonds."""
    e = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (4, 6), (6, 7), (7, 8), (8, 9), (9, 5)]
    return 10, e


def bicyclopentyl():
    """Two five-rings joined by one bond: ten carbons, eleven bonds, the same degrees as decalin."""
    e = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (5, 6), (6, 7), (7, 8), (8, 9), (9, 5), (0, 5)]
    return 10, e


def wl_refine(graphs, rounds=None, init=None):
    """1-dimensional Weisfeiler-Leman colour refinement run on several graphs at once, with one shared palette, so
    colours can be compared across graphs.  ``graphs``: list of (n, edges).  Returns per round, per graph, the colour
    of every node, and whether the colour histograms of the graphs differ."""
    adj = []
    for n, e in graphs:
        nb = [[] for _ in range(n)]
        for a, b in e:
            nb[a].append(b)
            nb[b].append(a)
        adj.append(nb)
    cols = [list(init[g]) if init is not None else [0] * n for g, (n, _) in enumerate(graphs)]
    history = [[list(c) for c in cols]]
    rounds = rounds or max(n for n, _ in graphs)
    for _ in range(rounds):
        sigs = [[(c[v], tuple(sorted(c[u] for u in adj[g][v]))) for v in range(len(c))] for g, c in enumerate(cols)]
        palette = {s: i for i, s in enumerate(sorted({s for sg in sigs for s in sg}))}
        new = [[palette[s] for s in sg] for sg in sigs]
        stable = all(len(set(nc)) == len(set(oc)) for nc, oc in zip(new, cols))
        cols = new
        history.append([list(c) for c in cols])
        if stable:
            break
    hists = [[sorted(Counter(c).items()) for c in h] for h in history]
    differ = [any(hh != hs[0] for hh in hs) for hs in hists]
    return dict(colors=history, differ=differ)


def wl_distinguishes(g1, g2) -> bool:
    return any(wl_refine([g1, g2])["differ"])


# ===========================================================================
# Message passing on one graph: a stochastic block model
# ===========================================================================
def sbm(rng, sizes=(100, 100, 100), p_in=0.06, p_out=0.004, feat_dim=8, signal=0.6, noise_edges=0):
    """A graph with communities (denser inside them), each node carrying a weak, noisy hint of its community.
    ``noise_edges`` extra edges are thrown in uniformly at random (most of them between communities)."""
    n = sum(sizes)
    y = np.concatenate([np.full(s, k) for k, s in enumerate(sizes)])
    P = np.where(y[:, None] == y[None, :], p_in, p_out)
    U = rng.uniform(size=(n, n))
    A = np.triu((U < P).astype(np.float32), 1)
    if noise_edges:
        iu = np.triu_indices(n, 1)
        pick = rng.choice(len(iu[0]), noise_edges, replace=False)
        A[iu[0][pick], iu[1][pick]] = 1
    A = A + A.T
    means = rng.normal(0, 1, (len(sizes), feat_dim))
    means /= np.linalg.norm(means, axis=1, keepdims=True)
    X = signal * means[y] + rng.normal(0, 1, (n, feat_dim))
    return A.astype(np.float32), X.astype(np.float32), y


def norm_adj(A: np.ndarray, self_loops=True) -> np.ndarray:
    """D^{-1/2} (A + I) D^{-1/2}, the GCN propagation matrix (Kipf & Welling 2017)."""
    M = A + np.eye(len(A), dtype=A.dtype) if self_loops else A
    d = M.sum(1)
    s = 1 / np.sqrt(np.maximum(d, 1e-12))
    return (s[:, None] * M * s[None, :]).astype(np.float32)


def split_masks(y, rng, per_class=20):
    tr = np.zeros(len(y), bool)
    for k in np.unique(y):
        idx = np.flatnonzero(y == k)
        tr[rng.choice(idx, per_class, replace=False)] = True
    return tr


class GCN(nn.Module):
    """h <- relu(A_hat h W), ``depth`` times; ``residual`` adds the input back at every layer."""

    def __init__(self, din, hidden, dout, depth=2, residual=False, dropout=0.5):
        super().__init__()
        self.inp = nn.Linear(din, hidden)
        self.layers = nn.ModuleList([nn.Linear(hidden, hidden) for _ in range(depth)])
        self.out = nn.Linear(hidden, dout)
        self.residual, self.dropout = residual, dropout

    def hidden(self, X, Ah):
        h = F.relu(self.inp(X))
        for L in self.layers:
            h = F.dropout(h, self.dropout, self.training)
            z = F.relu(Ah @ L(h))
            h = h + z if self.residual else z
        return h

    def forward(self, X, Ah):
        return self.out(F.dropout(self.hidden(X, Ah), self.dropout, self.training))


class NodeMLP(nn.Module):
    def __init__(self, din, hidden, dout, dropout=0.5):
        super().__init__()
        self.a, self.b, self.dropout = nn.Linear(din, hidden), nn.Linear(hidden, dout), dropout

    def forward(self, X, Ah=None):
        return self.b(F.dropout(F.relu(self.a(X)), self.dropout, self.training))


class GAT(nn.Module):
    """Graph attention (Velickovic et al. 2018), one head per layer, two layers: each node weighs its neighbours by
    softmax_j LeakyReLU(a^T [W h_i ; W h_j])."""

    def __init__(self, din, hidden, dout, dropout=0.5):
        super().__init__()
        self.W1, self.W2 = nn.Linear(din, hidden, bias=False), nn.Linear(hidden, dout, bias=False)
        self.a1 = nn.Parameter(torch.randn(2, hidden) * 0.1)
        self.a2 = nn.Parameter(torch.randn(2, dout) * 0.1)
        self.dropout = dropout

    @staticmethod
    def attend(h, a, mask):
        e = F.leaky_relu((h @ a[0])[:, None] + (h @ a[1])[None, :], 0.2)
        e = e.masked_fill(~mask, float("-inf"))
        return torch.softmax(e, 1)

    def forward(self, X, mask, return_att=False):
        h = self.W1(F.dropout(X, self.dropout, self.training))
        att1 = self.attend(h, self.a1, mask)
        h = F.elu(att1 @ h)
        h2 = self.W2(F.dropout(h, self.dropout, self.training))
        att2 = self.attend(h2, self.a2, mask)
        out = att2 @ h2
        return (out, att1) if return_att else out


def dirichlet(h: np.ndarray, A: np.ndarray) -> float:
    """Dirichlet energy of node features h: (1/2) sum_ij A_ij |h_i/sqrt(d_i) - h_j/sqrt(d_j)|^2 / n, with self-loops
    (zero exactly when every feature is proportional to sqrt(degree): the fixed point of repeated averaging)."""
    M = A + np.eye(len(A))
    d = M.sum(1)
    g = h / np.sqrt(d)[:, None]
    diff = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
    return float(0.5 * (M * diff).sum() / len(A))


# ===========================================================================
# Graph-level message passing: GIN, mean and max aggregation, and a pair network
# ===========================================================================
class GIN(nn.Module):
    """Graph isomorphism network (Xu et al. 2019): h_v <- MLP((1 + eps) h_v + sum_{u ~ v} h_u), a sum readout.  Its
    sum of an injective encoding makes it exactly as strong as 1-WL, and no stronger."""

    def __init__(self, din, hidden=64, layers=4, dout=2, agg="sum"):
        super().__init__()
        self.inp = nn.Linear(din, hidden)
        self.mlps = nn.ModuleList([mlp([hidden, hidden, hidden], last_act=True) for _ in range(layers)])
        self.eps = nn.Parameter(torch.zeros(layers))
        self.out = mlp([hidden, hidden, dout])
        self.agg = agg

    def aggregate(self, A, h):
        if self.agg == "sum":
            return A @ h
        if self.agg == "mean":
            return (A @ h) / A.sum(-1, keepdim=True).clamp(min=1)
        big = torch.where(A.unsqueeze(-1) > 0, h.unsqueeze(-3), torch.full_like(h.unsqueeze(-3), -1e9))
        return big.max(-2).values.clamp(min=-1e8) * (A.sum(-1, keepdim=True) > 0)

    def node_states(self, A, X):
        h = self.inp(X)
        for k, f in enumerate(self.mlps):
            h = f((1 + self.eps[k]) * h + self.aggregate(A, h))
        return h

    def forward(self, A, X):
        return self.out(self.node_states(A, X).sum(-2))


class PairNet(nn.Module):
    """A network over pairs of nodes (Maron et al. 2019's 'provably powerful' layer): pair features are updated by a
    matrix product over the third node, z_ij <- f(z_ij, sum_k g(z_ik) h(z_kj)), which sees triangles; a sum readout."""

    def __init__(self, hidden=32, layers=3, dout=2):
        super().__init__()
        # no biases before the product: a constant term would swamp the sum over the third node (with them, some
        # seeds never leave the base rate)
        self.inp = nn.Linear(2, hidden, bias=False)
        self.g = nn.ModuleList([nn.Linear(hidden, hidden, bias=False) for _ in range(layers)])
        self.h = nn.ModuleList([nn.Linear(hidden, hidden, bias=False) for _ in range(layers)])
        self.f = nn.ModuleList([mlp([2 * hidden, hidden, hidden], last_act=True) for _ in range(layers)])
        self.out = mlp([hidden, hidden, dout])

    def forward(self, A, X=None):
        n = A.shape[-1]
        eye = torch.eye(n).expand_as(A)
        z = self.inp(torch.stack([A, eye], -1))
        for g, h, f in zip(self.g, self.h, self.f):
            prod = torch.einsum("bikc,bkjc->bijc", g(z), h(z))
            z = f(torch.cat([z, prod], -1))
        return self.out(z.sum((1, 2)) / n)


def two_regular(rng, n=15, lo=3):
    """A random 2-regular graph on n nodes (a disjoint union of cycles, each at least ``lo`` long), nodes shuffled."""
    while True:
        parts, left = [], n
        while left:
            if left < 2 * lo and left >= lo:
                parts.append(left)
                break
            L = int(rng.integers(lo, left - lo + 1)) if left - lo >= lo else left
            parts.append(L)
            left -= L
        if all(p >= lo for p in parts):
            break
    perm = rng.permutation(n)
    e = [(perm[a], perm[b]) for a, b in cycle_edges(parts)]
    return sorted(parts), edges_to_adj(n, e)


def regular_dataset(count, rng, n=15):
    """Unions of cycles: label 1 if there is a triangle.  To 1-WL (and so to every message-passing network) all of
    them look the same: every node has two neighbours, all the way down."""
    As, ys, parts = [], [], []
    for _ in range(count):
        p, A = two_regular(rng, n)
        As.append(A)
        ys.append(int(3 in p))
        parts.append(p)
    return np.array(As), np.array(ys), parts


def train_graph_classifier(model, A, X, y, seed, steps=1500, batch=32, lr=1e-3, rni=False, val=None, every=100):
    """Train on graph classification; ``rni``: each node also gets fresh random numbers (random node initialization,
    Sato et al. 2021; Abboud et al. 2021), which breaks the symmetry 1-WL can't.  ``val`` = (A, X, y): record held-out
    accuracy every ``every`` steps in ``model.curve`` (its random numbers come from a separate generator)."""
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(700 + seed)
    opt = torch.optim.Adam(model.parameters(), lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    At, Xt, yt = torch.from_numpy(A), torch.from_numpy(X), torch.from_numpy(y).long()
    model.curve = []
    for s in range(steps + 1):
        if val is not None and s % every == 0:
            model.eval()
            g = torch.Generator().manual_seed(3)
            model.curve.append((s, graph_accuracy(model, *val, rni=rni, gen=g, reps=2)))
            model.train()
        if s == steps:
            break
        j = torch.randint(0, len(At), (batch,), generator=gen)
        xb = Xt[j]
        if rni:
            xb = torch.cat([xb, torch.rand(xb.shape[0], xb.shape[1], 4, generator=gen)], -1)
        loss = F.cross_entropy(model(At[j], xb), yt[j])
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    model.eval()
    return model


def graph_accuracy(model, A, X, y, rni=False, gen=None, reps=1):
    At, Xt = torch.from_numpy(A), torch.from_numpy(X)
    with torch.no_grad():
        probs = 0
        for _ in range(reps):
            xb = Xt
            if rni:
                xb = torch.cat([xb, torch.rand(xb.shape[0], xb.shape[1], 4, generator=gen)], -1)
            probs = probs + F.softmax(model(At, xb), -1)
    return float((probs.argmax(1).numpy() == y).mean())


# ===========================================================================
# How far can a message travel?  Distances to a marked node
# ===========================================================================
def geometric_graph(rng, n=60, radius=0.2):
    """Points in the unit square joined when closer than ``radius`` (kept connected by joining the components)."""
    P = rng.uniform(size=(n, 2))
    D = np.sqrt(((P[:, None] - P[None]) ** 2).sum(-1))
    A = ((D < radius) & (D > 0)).astype(np.float32)
    # join components through their closest pairs
    while True:
        comp = components(A)
        if comp.max() == 0:
            break
        a, b = np.flatnonzero(comp == 0), np.flatnonzero(comp != 0)
        sub = D[np.ix_(a, b)]
        i, j = np.unravel_index(sub.argmin(), sub.shape)
        A[a[i], b[j]] = A[b[j], a[i]] = 1
    return P, A


def components(A) -> np.ndarray:
    n = len(A)
    comp = -np.ones(n, int)
    c = 0
    for s in range(n):
        if comp[s] >= 0:
            continue
        stack = [s]
        comp[s] = c
        while stack:
            v = stack.pop()
            for u in np.flatnonzero(A[v]):
                if comp[u] < 0:
                    comp[u] = c
                    stack.append(u)
        c += 1
    return comp


def bfs_dist(A, s) -> np.ndarray:
    n = len(A)
    d = np.full(n, 10 ** 6)
    d[s] = 0
    frontier = [s]
    while frontier:
        nxt = []
        for v in frontier:
            for u in np.flatnonzero(A[v]):
                if d[u] > d[v] + 1:
                    d[u] = d[v] + 1
                    nxt.append(u)
        frontier = nxt
    return d
