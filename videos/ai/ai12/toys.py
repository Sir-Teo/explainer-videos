"""The small, exactly controllable experiments of Part 12: wide two-layer networks (the Gaussian-process and
neural-tangent limits, lazy against rich training), the quanta model's multitask sparse parity, and regression on a
data manifold of dimension d. All seeded; each runs in a few minutes on one CPU thread."""

from __future__ import annotations

import math

import numpy as np


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
# 1. A one-hidden-layer ReLU network in the neural-tangent parametrization, in closed form (numpy)
#    f(x) = (1/sqrt n) sum_j a_j relu(u_j x + c_j),  x in [-1, 1],  u, c, a ~ N(0, 1)
# ---------------------------------------------------------------------------
def ntk_target(x):
    return np.sin(2.6 * x) + 0.4 * np.cos(5.0 * x)  # illustrative


NTK_X = np.array([-0.92, -0.71, -0.48, -0.30, -0.08, 0.13, 0.35, 0.52, 0.74, 0.93])


def _feats(x, u, c):
    z = np.outer(x, u) + c  # points x units
    return np.maximum(z, 0.0), (z > 0).astype(float)


def net(x, u, c, a):
    r, _ = _feats(x, u, c)
    return r @ a / math.sqrt(len(a))


def tangent(x, u, c, a):
    """The tangent features: the gradient of f at each x with respect to (a, u, c)."""
    r, s = _feats(x, u, c)
    n = len(a)
    return np.concatenate([r, s * a * x[:, None], s * a], 1) / math.sqrt(n)


def train_ntk(n: int, seed: int, steps: int = 4000, eta: float | None = None, grid=None, record=()):
    """Full-batch gradient descent on the 10 training points (mean squared error / 2). Returns how far the weights
    and the kernel moved, and the trained function against its own linearization (Lee et al. 2019)."""
    g = rng(seed)
    u, c, a = g.normal(size=n), g.normal(size=n), g.normal(size=n)
    X, y = NTK_X, ntk_target(NTK_X)
    m = len(X)
    grid = np.linspace(-1, 1, 81) if grid is None else grid
    J0, Jg0 = tangent(X, u, c, a), tangent(grid, u, c, a)
    K0, Kg0 = J0 @ J0.T, Jg0 @ J0.T
    if eta is None:
        eta = 1.0 / np.linalg.eigvalsh(K0 / m).max()
    f0, f0g = net(X, u, c, a), net(grid, u, c, a)
    u0, c0, a0 = u.copy(), c.copy(), a.copy()
    res_sum = np.zeros(m)  # the linearized model's residuals, summed over steps
    r_lin = f0 - y
    snaps = {}
    for t in range(steps):
        if t in record:
            snaps[t] = net(grid, u, c, a)
        res_sum += r_lin
        r_lin = r_lin - eta / m * K0 @ r_lin
        r = net(X, u, c, a) - y
        J = tangent(X, u, c, a)
        grad = J.T @ r / m
        a -= eta * grad[:n]
        u -= eta * grad[n:2 * n]
        c -= eta * grad[2 * n:]
    fT, fTg = net(X, u, c, a), net(grid, u, c, a)
    flin = f0g - eta / m * Kg0 @ res_sum
    JT, JgT = tangent(X, u, c, a), tangent(grid, u, c, a)
    KgT0 = JgT @ JgT.T
    Kgg0 = Jg0 @ Jg0.T
    return dict(n=n, eta=float(eta),
                moved_hidden=float(np.sqrt(((u - u0) ** 2).sum() + ((c - c0) ** 2).sum()) / np.sqrt((u0 ** 2).sum() + (c0 ** 2).sum())),
                moved_out=float(np.linalg.norm(a - a0) / np.linalg.norm(a0)),
                kernel_moved=float(np.linalg.norm(KgT0 - Kgg0) / np.linalg.norm(Kgg0)),
                train_mse=float(((fT - y) ** 2).mean()), lin_gap=float(np.abs(fTg - flin).max()),
                f0=f0g, fT=fTg, flin=flin, snaps=snaps, grid=grid)


def nngp(widths=(1, 2, 8, 64, 512), draws=6000, x=0.5, seed=1994):
    """The network's output at one input, across many random initializations: it tends to a Gaussian as the width
    grows (Neal 1994), with variance (x^2 + 1)/2."""
    out = {}
    for n in widths:
        g = rng(seed + n)
        u, c, a = g.normal(size=(draws, n)), g.normal(size=(draws, n)), g.normal(size=(draws, n))
        f = (np.maximum(u * x + c, 0) * a).sum(1) / math.sqrt(n)
        k = float(((f - f.mean()) ** 4).mean() / f.var() ** 2 - 3)
        out[n] = dict(f=f, var=float(f.var()), kurt=k)
    # sample functions of a wide network, and the arc-cosine kernel they are drawn from
    xs = np.linspace(-1, 1, 101)
    g = rng(seed)
    n = 2000
    samples = []
    for _ in range(5):
        u, c, a = g.normal(size=n), g.normal(size=n), g.normal(size=n)
        samples.append(net(xs, u, c, a))
    res = dict(widths=list(widths), x=x, var_theory=(x * x + 1) / 2, var={str(n): v["var"] for n, v in out.items()},
               kurt={str(n): v["kurt"] for n, v in out.items()}, xs=xs, samples=np.array(samples))
    for n, v in out.items():
        res[f"draws{n}"] = v["f"]
    return res


# ---------------------------------------------------------------------------
# 2. Lazy against rich: a two-layer network learning y = (w*.x)^2 - 1 in 32 dimensions from 256 examples
# ---------------------------------------------------------------------------
RICH_D, RICH_N, RICH_TEST = 32, 256, 4000


def rich_data(seed):
    import torch

    g = torch.Generator().manual_seed(500 + seed)
    w = torch.randn(RICH_D, generator=g)
    w /= w.norm()
    X = torch.randn(RICH_N, RICH_D, generator=g)
    Xt = torch.randn(RICH_TEST, RICH_D, generator=g)
    return w, X, (X @ w) ** 2 - 1, Xt, (Xt @ w) ** 2 - 1


def train_rich(mode: str, seed: int, width: int = 1024, steps: int = 6000, eta: float = 1.0, every: int = 100,
               keep_units: int = 160):
    """``mode`` 'ntk': f = (1/sqrt n) sum a_j relu(w_j.x / sqrt d), minus its value at initialization, learning rate
    eta (the lazy limit as n grows); 'mf': f = (1/n) sum a_j relu(w_j.x / sqrt d), learning rate eta n (mean field,
    which is muP for two layers: every unit moves by O(1)). Same data, same width, same steps."""
    import torch

    w, X, y, Xt, yt = rich_data(seed)
    torch.manual_seed(seed)
    W = torch.randn(width, RICH_D)
    a = torch.randn(width)
    W0, a0 = W.clone(), a.clone()
    W.requires_grad_()
    a.requires_grad_()
    s = 1 / math.sqrt(width) if mode == "ntk" else 1 / width
    lr = eta * (1.0 if mode == "ntk" else width)
    sq = math.sqrt(RICH_D)

    def f(Z, W_, a_):
        return s * torch.relu(Z @ W_.T / sq) @ a_

    with torch.no_grad():
        off, offt = (f(X, W0, a0), f(Xt, W0, a0)) if mode == "ntk" else (0.0, 0.0)
    curve, units = [], []
    pick = torch.arange(min(keep_units, width))
    for t in range(steps + 1):
        out = f(X, W, a) - off
        loss = 0.5 * ((out - y) ** 2).mean()
        if t % every == 0:
            with torch.no_grad():
                te = float(((f(Xt, W, a) - offt - yt) ** 2).mean())
                al = float((W @ w).abs().div(W.norm(dim=1)).mean())
            curve.append((t, float(loss) * 2, te, al))
            if t % (every * 5) == 0:
                with torch.no_grad():  # each kept unit's weight vector: along w*, and its length off w*
                    Wk = W[pick]
                    along = Wk @ w
                    off_ = (Wk - along[:, None] * w).norm(dim=1)
                    units.append(np.stack([along.numpy(), off_.numpy()], 1) / sq)
        if t == steps:
            break
        gW, ga = torch.autograd.grad(loss, (W, a))
        with torch.no_grad():
            W -= lr * gW
            a -= lr * ga
    return dict(curve=np.array(curve), units=np.array(units), moved=float((W - W0).norm() / W0.norm()),
                var=float(yt.var()))


def kernel_regression(seed: int, width: int = 4096, ridge: float = 1e-6):
    """The lazy limit exactly: regression with the network's tangent kernel at initialization (gradient descent on
    the linearized network, run to convergence)."""
    import torch

    w, X, y, Xt, yt = rich_data(seed)
    torch.manual_seed(seed + 77)
    W = torch.randn(width, RICH_D)
    a = torch.randn(width)
    sq = math.sqrt(RICH_D)

    def tf(Z):
        z = Z @ W.T / sq
        r, s_ = torch.relu(z), (z > 0).float()
        # gradient wrt a: r / sqrt n; wrt W_j: a_j s_j x / (sqrt d sqrt n): K = r r' + (a^2 s s') (x.x')/d
        return r, s_ * a

    r, sa = tf(X)
    rt, sat = tf(Xt)
    K = (r @ r.T + (sa @ sa.T) * (X @ X.T) / RICH_D) / width
    Kt = (rt @ r.T + (sat @ sa.T) * (Xt @ X.T) / RICH_D) / width
    alpha = torch.linalg.solve(K + ridge * torch.eye(len(X)), y)
    pred = Kt @ alpha
    return float(((pred - yt) ** 2).mean())


# ---------------------------------------------------------------------------
# 3. The quanta model: multitask sparse parity (Michaud et al. 2023), small
# ---------------------------------------------------------------------------
QT_TASKS, QT_BITS, QT_K, QT_ALPHA = 32, 12, 3, 0.4


def quanta_tasks():
    from itertools import combinations

    g = rng(31)
    combos = np.array(list(combinations(range(QT_BITS), QT_K)))
    S = combos[g.choice(len(combos), QT_TASKS, replace=False)]  # 32 different subsets of the 12 task bits
    p = np.arange(1, QT_TASKS + 1, dtype=float) ** -(QT_ALPHA + 1)
    return S, p / p.sum()


def quanta_batch(g, B, S, p, task=None):
    t = g.choice(QT_TASKS, B, p=p) if task is None else np.full(B, task)
    bits = g.integers(0, 2, (B, QT_BITS))
    y = bits[np.arange(B)[:, None], S[t]].sum(1) % 2
    x = np.zeros((B, QT_TASKS + QT_BITS), np.float32)
    x[np.arange(B), t] = 1
    x[:, QT_TASKS:] = bits
    return x, y, t


def train_quanta(width: int, seed: int, steps: int = 20000, batch: int = 1024, lr: float = 1e-3, every: int = 250):
    """A one-hidden-layer ReLU network on multitask sparse parity, fresh samples every step; the test loss on each
    subtask, recorded through training."""
    import torch

    S, p = quanta_tasks()
    torch.manual_seed(seed)
    net = torch.nn.Sequential(torch.nn.Linear(QT_TASKS + QT_BITS, width), torch.nn.ReLU(), torch.nn.Linear(width, 2))
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    g = rng(1000 + seed)
    gt = rng(77)  # the test set: the same 256 inputs per subtask for every run
    tests = [quanta_batch(gt, 256, S, p, task=k) for k in range(QT_TASKS)]
    Xt = torch.tensor(np.concatenate([x for x, _, _ in tests]))
    Yt = torch.tensor(np.concatenate([y for _, y, _ in tests]))
    curve = []
    for s in range(steps + 1):
        if s % every == 0 or s == steps:
            with torch.no_grad():
                lt = torch.nn.functional.cross_entropy(net(Xt), Yt, reduction="none").reshape(QT_TASKS, -1).mean(1)
            curve.append((s, lt.numpy() / math.log(2)))
        if s == steps:
            break
        x, y, _ = quanta_batch(g, batch, S, p)
        loss = torch.nn.functional.cross_entropy(net(torch.tensor(x)), torch.tensor(y))
        opt.zero_grad()
        loss.backward()
        opt.step()
    steps_ = np.array([c[0] for c in curve])
    per_task = np.stack([c[1] for c in curve])  # checkpoints x tasks, bits
    n_params = sum(q.numel() for q in net.parameters())
    return dict(steps=steps_, per_task=per_task, n_params=n_params)


# ---------------------------------------------------------------------------
# 4. Regression on a data manifold of dimension d (Sharma & Kaplan 2020): N linear pieces
# ---------------------------------------------------------------------------
def manifold_teacher(d, seed=3):
    """A smooth function on the d-dimensional torus: a few random waves (illustrative)."""
    g = rng(seed + d)
    K = g.integers(-2, 3, size=(24, d)).astype(float)
    ph = g.uniform(0, 2 * math.pi, 24)
    amp = g.normal(size=24) / np.maximum(1.0, np.linalg.norm(K, axis=1)) ** 1.5

    def f(X):
        return np.cos(2 * math.pi * X @ K.T + ph) @ amp

    def grad(X):
        return -(np.sin(2 * math.pi * X @ K.T + ph) * amp) @ K * 2 * math.pi

    return f, grad


def manifold_error(d: int, pieces: int, seed: int = 0, test: int = 40000):
    """A model made of ``pieces`` linear pieces tiling the d-dimensional manifold (each piece the teacher's
    linearization at a random centre, used on the points nearest to it): its mean squared error. The pieces have
    size ~ N^(-1/d), the error of a linear piece ~ size^2, so the loss ~ N^(-4/d)."""
    from scipy.spatial import cKDTree

    f, grad = manifold_teacher(d)
    g = rng(100 * d + seed)
    C = g.uniform(0, 1, (pieces, d))
    Xt = g.uniform(0, 1, (test, d))
    tree = cKDTree(C, boxsize=1.0)  # the torus: distances wrap around
    _, j = tree.query(Xt)
    delta = Xt - C[j]
    delta -= np.round(delta)  # shortest way round the torus
    pred = f(C)[j] + (grad(C)[j] * delta).sum(1)
    return float(((pred - f(Xt)) ** 2).mean())
