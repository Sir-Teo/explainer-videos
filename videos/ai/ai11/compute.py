"""Precompute everything numerical in Part 11 of the AI series ("Going Downhill").

    python -m videos.ai.ai11.compute              # everything missing (Part 1's books, Part 6's pages); ~2.5 CPU-hours
    python -m videos.ai.ai11.compute race         # one item;  --force to recompute

Results are cached in ``.cache/ai11/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Every run is seeded and
single-threaded (``AI11_THREADS``, default 1). The long items (``race``, ``decay``, ``schedule``, ``natgrad``,
``spikes``) save each finished run as they go (``CACHE.partial``) and resume where they stopped; ``AI11_WORKERS``
(default 1) runs their runs in that many processes (``spawn``); the results do not depend on it.

The workhorse is a small character model (``charopt.py``: 8 characters of context, 16-number character vectors, 256
tanh units and a residual 256 x 256 hidden layer) on Part 1's thirty novels, scored in bits per character on
held-out text. ``char_data`` (below) is its data, and Parts 12 and 16 use it too: keep its name and output.

Items:
    quad        gradient descent, heavy ball and Nesterov on quadratics of condition number 1 ... 1,000: iterations to
                a millionth of the starting error, measured against the rates derived; f - f* against the O(1/k) and
                O(1/k^2) bounds on an ill-conditioned convex quadratic; paths on a 1:30 valley
    race3d      gradient descent, heavy ball, Adam and Lion on one curved valley (Rosenbrock's), each at its best
                learning rate on a grid, at equal steps
    noise       SGD on a real two-weight loss (logistic regression on Part 6's two word rates): paths for batch sizes
                1, 16 and all, and the cloud each settles into
    temperature the cloud's size against eta / B on a grid of learning rates and batch sizes (3 seeds), against the
                stationary covariance predicted from the loss's Hessian and gradient covariance
    eos         the edge of stability: full-batch gradient descent on Part 9's spirals at two learning rates, the
                sharpness (power iteration on Hessian-vector products) climbing to 2/eta
    adamview    Adam on the character model: m, v and the bias corrections on real gradients; every weight's step
                divided by the learning rate at steps 1, 100 and 1,000 (Adam as nearly sign descent)
    decay       AdamW against Adam + L2 on a model that overfits (50,000 characters, 128 units): held-out bits over a
                grid of learning rates and decay strengths, then 3 seeds at each one's best
    natgrad     the natural gradient: gradient descent and the natural gradient in two parametrizations of the same
                two-weight loss; on the spirals, gradient descent, Adam, K-FAC and the exact natural gradient, each
                at its best learning rate (5 values) over 3 seeds, with snapshots of the decision map
    race        the character model trained by SGD with momentum, AdamW, Lion, Shampoo, SOAP and Muon: 6 learning
                rates each at seed 0, then 3 seeds at the best (3,000 steps, warmup and cosine); samples of writing
    ns          Newton-Schulz on the trained model's 256 x 256 matrix and on its gradient: Jordan's 5 quintic rounds,
                the classical cubic, and DeepSeek-V4's hybrid (8 + 2 rounds)
    schedule    AdamW with cosine schedules of 1,000, 2,000 and 4,000 steps against one constant run with
                warmup-stable-decay cool-down branches at each length, an EMA of its weights, and schedule-free
                AdamW (2 seeds)
    river       a river valley (a slow river along x, steep hills across it) under noisy gradient steps with
                constant, cosine, WSD and small-constant schedules (20 seeds): loss split into river and hill
    equilibrium weight decay's equilibrium: a scale-invariant matrix (LayerNorm after it) under AdamW with three
                decay strengths: its norm against the predicted sqrt(eta (1 + b1) |u|^2 / (2 lambda (1 - b1)))
    spikes      a one-layer attention model trained too fast: the largest attention score and the loss, with and
                without QK-clip (Muon) and gradient clipping (Adam), 2 seeds
"""

from __future__ import annotations

import math
import os

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai11")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _workers() -> int:
    return max(1, int(os.environ.get("AI11_WORKERS", 1)))


def _pmap(fn, jobs: list) -> list:
    """``fn(*job)`` for every job, in AI11_WORKERS processes (spawn: fork and torch don't mix on macOS)."""
    if _workers() == 1 or len(jobs) < 2:
        return [fn(*j) for j in jobs]
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(_workers(), mp_context=mp.get_context("spawn")) as ex:
        return list(ex.map(fn, *zip(*jobs)))


def _run_pieces(part, jobs: dict, fn) -> None:
    """Run every job not yet in ``part`` (key -> args), saving each as it finishes; in batches of AI11_WORKERS."""
    todo = [k for k in jobs if k not in part]
    w = _workers()
    for i in range(0, len(todo), w):
        keys = todo[i:i + w]
        for k, r in zip(keys, _pmap(fn, [jobs[k] for k in keys])):
            part[k] = r
            print(f"    {k}: {r.get('final', r.get('held', ''))}", flush=True)


# ---------------------------------------------------------------------------
# The character data (Parts 12 and 16 import this: keep its name, signature and output)
# ---------------------------------------------------------------------------
CTX, EMB, HID = 8, 16, 256


def char_data():
    from videos.ai.ai1 import compute as c1

    texts = {k: c1.text(k) for k in ("train", "valid")}
    chars = sorted(set("".join(texts.values())))
    cp = np.array([ord(c) for c in chars])
    order = np.argsort(cp)

    def enc(t):
        a = np.frombuffer(t.encode("utf-32-le"), dtype=np.uint32)
        return order[np.searchsorted(cp[order], a)]

    return enc(texts["train"]), enc(texts["valid"])[:100_000], len(chars)


# ---------------------------------------------------------------------------
# 1-2. Gradient descent and momentum on quadratics
# ---------------------------------------------------------------------------
KAPPAS = [1, 3, 10, 30, 100, 300, 1000]
TOL = 1e-6  # stop at a millionth of the starting error f - f*


def _quad_iters(lam, x0, method, kmax=200_000, tol=TOL, rate=False):
    """Iterations of ``method`` on f(x) = 1/2 sum lam_i x_i^2 until f <= tol f(x0); ``rate``: also the measured
    contraction of the error per step over the last fifth of the run (sqrt of f's)."""
    L, mu = float(lam.max()), float(lam.min())
    k_ = L / mu
    f0 = 0.5 * float((lam * x0 * x0).sum())
    x, xp = x0.copy(), x0.copy()
    fs = []
    if method == "gd":
        eta, beta = 1 / L, 0.0
    elif method == "gd_opt":
        eta, beta = 2 / (L + mu), 0.0
    elif method == "hb":
        eta, beta = 4 / (math.sqrt(L) + math.sqrt(mu)) ** 2, ((math.sqrt(k_) - 1) / (math.sqrt(k_) + 1)) ** 2
    else:  # nesterov
        eta, beta = 1 / L, (math.sqrt(k_) - 1) / (math.sqrt(k_) + 1)
    for k in range(1, kmax + 1):
        if method == "nesterov":
            yv = x + beta * (x - xp)
            xn = yv - eta * lam * yv
        else:
            xn = x - eta * lam * x + beta * (x - xp)
        xp, x = x, xn
        fk = 0.5 * float((lam * x * x).sum())
        if rate:
            fs.append(fk)
        if fk <= tol * f0:
            break
    if not rate:
        return k
    j = int(0.8 * len(fs))
    return k, (fs[-1] / fs[j - 1]) ** (1 / (2 * (len(fs) - j)))


def _rho(kappa, method):
    """The derived contraction of the error per step (Nesterov's: sqrt(beta (1 - eta mu)), about 1 - 1/sqrt(kappa))."""
    if method == "nesterov":
        return _nest_rho(kappa)
    return {"gd": 1 - 1 / kappa, "gd_opt": (kappa - 1) / (kappa + 1),
            "hb": (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)}[method]


def _nest_rho(kappa):
    """Nesterov's slowest mode (eigenvalue mu = 1/kappa, eta = 1): x_{k+1} = (1 + b)(1 - mu) x_k - b (1 - mu) x_{k-1};
    the larger root's modulus of z^2 - (1 + b)(1 - mu) z + b (1 - mu)."""
    b = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
    mu = 1 / kappa
    r = np.roots([1, -(1 + b) * (1 - mu), b * (1 - mu)])
    return float(np.abs(r).max())


def _predicted(kappa, method):
    """Iterations the derived rate predicts: the error shrinks by rho per step, so f by rho^2."""
    r = _rho(kappa, method) if kappa > 1 else 0.0
    if r <= 0:
        return 1.0
    return math.log(1 / TOL) / (-2 * math.log(r))


def compute_quad():
    out = dict(kappas=KAPPAS, methods=["gd", "gd_opt", "hb", "nesterov"])
    g = rng(5)
    d = 50
    x0 = g.choice([-1.0, 1.0], d) / math.sqrt(d)
    for m in out["methods"]:
        out[f"iters_{m}"] = [_quad_iters(np.geomspace(1 / k, 1, d), x0, m) for k in KAPPAS]
        out[f"pred_{m}"] = [_predicted(k, m) for k in KAPPAS]
        rates = [_quad_iters(np.geomspace(1 / k, 1, d), x0, m, tol=1e-14, rate=True)[1] for k in KAPPAS[1:]]
        out[f"rate_{m}"] = [0.0] + rates  # kappa = 1: one step
        out[f"rate_pred_{m}"] = [0.0] + [_rho(k, m) for k in KAPPAS[1:]]
        big = np.array(KAPPAS) >= 10
        out[f"slope_{m}"] = float(np.polyfit(np.log(np.array(KAPPAS)[big]), np.log(np.array(out[f"iters_{m}"])[big]), 1)[0])
        print(f"    {m}: {out[f'iters_{m}']}", flush=True)
    # convex but not strongly: f - f* against the bounds L|x0-x*|^2/(2k) (GD) and 2L|x0-x*|^2/(k+1)^2 (Nesterov)
    lam = 1.0 / np.arange(1, 1001) ** 2
    x0c = np.ones(1000)
    K = 2000
    gd, ne = np.empty(K), np.empty(K)
    x = x0c.copy()
    for k in range(K):
        x = x - lam * x
        gd[k] = 0.5 * float((lam * x * x).sum())
    x, xp = x0c.copy(), x0c.copy()
    for k in range(K):
        yv = x + (k / (k + 3)) * (x - xp)
        xp, x = x, yv - lam * yv
        ne[k] = 0.5 * float((lam * x * x).sum())
    R2 = float((x0c * x0c).sum())
    ks = np.arange(1, K + 1)
    out.update(conv_k=ks, conv_gd=gd, conv_nesterov=ne, bound_gd=R2 / (2 * ks), bound_nesterov=2 * R2 / (ks + 1) ** 2,
               conv_R2=R2)
    # paths on the 1:30 valley, from the same start
    lam2 = np.array([1.0, 30.0])
    start = np.array([-4.5, 0.9])
    paths = {}
    for key, eta, beta, nest in (("gd", 1 / 30, 0.0, False), ("gd_big", 2.06 / 30, 0.0, False),
                                 ("hb", 4 / (1 + math.sqrt(30)) ** 2, ((math.sqrt(30) - 1) / (math.sqrt(30) + 1)) ** 2, False),
                                 ("nesterov", 1 / 30, (math.sqrt(30) - 1) / (math.sqrt(30) + 1), True),
                                 ("hb_mild", 1 / 30, 0.8, False)):
        x, xp, P = start.copy(), start.copy(), [start.copy()]
        for _ in range(60):
            if nest:
                yv = x + beta * (x - xp)
                xn = yv - eta * lam2 * yv
            else:
                xn = x - eta * lam2 * x + beta * (x - xp)
            xp, x = x, xn
            P.append(x.copy())
        paths[key] = np.array(P)
    for k, v in paths.items():
        out[f"path_{k}"] = v
    return out


# ---------------------------------------------------------------------------
# The hook: four optimizers on one landscape
# ---------------------------------------------------------------------------
ROSEN_B = 5.0
RACE_START = (-1.5, 2.2)
RACE_STEPS = 150


def rosen(x, y):
    return (1 - x) ** 2 + ROSEN_B * (y - x * x) ** 2


def _rosen_grad(p):
    x, y = p
    return np.array([-2 * (1 - x) - 4 * ROSEN_B * x * (y - x * x), 2 * ROSEN_B * (y - x * x)])


def _walk(name, lr, steps=RACE_STEPS):
    p = np.array(RACE_START, float)
    m, v, P = np.zeros(2), np.zeros(2), [p.copy()]
    for t in range(1, steps + 1):
        g = _rosen_grad(p)
        if name == "gd":
            p = p - lr * g
        elif name == "hb":
            m = 0.9 * m + g
            p = p - lr * m
        elif name == "adam":
            m = 0.9 * m + 0.1 * g
            v = 0.999 * v + 0.001 * g * g
            p = p - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
        else:  # lion
            c = 0.9 * m + 0.1 * g
            p = p - lr * np.sign(c)
            m = 0.99 * m + 0.01 * g
        if not np.all(np.isfinite(p)) or np.abs(p).max() > 1e3:
            return None
        P.append(p.copy())
    return np.array(P)


def compute_race3d():
    lrs = np.geomspace(1e-4, 1.0, 25)
    out = dict(lrs=lrs, names=["gd", "hb", "adam", "lion"], start=list(RACE_START), steps=RACE_STEPS)
    for name in out["names"]:
        finals = []
        for lr in lrs:
            P = _walk(name, lr)
            finals.append(float(rosen(*P[-1])) if P is not None else float("nan"))
        finals = np.array(finals)
        i = int(np.nanargmin(finals))
        P = _walk(name, lrs[i])
        f = rosen(P[:, 0], P[:, 1])
        out[f"path_{name}"] = P
        out[f"lr_{name}"] = float(lrs[i])
        out[f"final_{name}"] = float(finals[i])
        out[f"finals_{name}"] = finals
        out[f"edge_{name}"] = bool(i in (0, len(lrs) - 1))
        out[f"reach_{name}"] = int(np.argmax(f < 0.01)) if (f < 0.01).any() else -1
        print(f"    {name}: lr {lrs[i]:.3g}, final {finals[i]:.2e}, reach {out[f'reach_{name}']}", flush=True)
    return out


# ---------------------------------------------------------------------------
# 3-4. Stochastic gradients, and their temperature
# ---------------------------------------------------------------------------
def _logreg():
    from videos.ai.ai6 import compute as c5

    X, y, test, X2 = c5.split()
    Z, _, _, _ = c5.standardize(X2[~test], X2[test])
    t = 2.0 * y[~test] - 1
    return Z, t


def _logreg_fns(Z, t):
    def loss(w):
        return np.log1p(np.exp(-t * (Z @ w))).mean(axis=-1) if w.ndim == 1 else \
            np.log1p(np.exp(-t[None] * (w @ Z.T))).mean(1)

    def grad(w, idx):
        m = -t[idx] / (1 + np.exp(t[idx] * (Z[idx] @ w)))
        return (m[:, None] * Z[idx]).mean(0)

    return loss, grad


def _w_star(Z, t):
    loss, grad = _logreg_fns(Z, t)
    w = np.zeros(2)
    for _ in range(20_000):
        w = w - 0.5 * grad(w, np.arange(len(t)))
    return w


def compute_noise():
    Z, t = _logreg()
    n = len(t)
    loss, grad = _logreg_fns(Z, t)
    w1, w2 = np.linspace(-1.4, 2.0, 137), np.linspace(-3.4, 0.6, 161)
    W = np.stack(np.meshgrid(w1, w2), -1).reshape(-1, 2)
    L = loss(W).reshape(len(w2), len(w1))
    w_star = _w_star(Z, t)
    out = dict(w1=w1, w2=w2, L=L, w_star=w_star, n=n)
    lr, steps = 0.25, 300
    for B in (1, 16, n):
        g = rng(B)
        w, path = np.array([-1.0, 0.2]), []
        for _ in range(steps):
            path.append(w.copy())
            idx = g.choice(n, size=B, replace=False) if B < n else np.arange(n)
            w = w - lr * grad(w, idx)
        path.append(w.copy())
        w, cloud = w_star.copy(), []
        for k in range(4000):
            idx = g.choice(n, size=B, replace=False) if B < n else np.arange(n)
            w = w - lr * grad(w, idx)
            if k % 10 == 0:
                cloud.append(w.copy())
        out[f"path{B}"] = np.array(path)
        out[f"cloud{B}"] = np.array(cloud)
        out[f"spread{B}"] = float(np.sqrt(((np.array(cloud) - w_star) ** 2).sum(1).mean()))
    # Robbins and Monro: one page per step, a constant step against steps that shrink like 1/k
    K = 20_000
    for kind in ("constant", "decay"):
        dist = np.zeros(K)
        for sd in range(5):
            g = rng(77 + sd)
            w = np.array([-1.0, 0.2])
            for k in range(K):
                eta = lr if kind == "constant" else lr / (1 + k / 100)
                w = w - eta * grad(w, g.integers(0, n, 1))
                dist[k] += float(((w - w_star) ** 2).sum()) / 5
        out[f"rm_{kind}"] = dist
    return out


T_ETAS = [0.05, 0.1, 0.2, 0.4]
T_BATCHES = [1, 2, 4, 8, 16, 32]


def compute_temperature():
    """E|w - w*|^2 of SGD's stationary cloud (batches drawn with replacement), against the linearized prediction:
    the stationary covariance S of w <- w - eta (H (w - w*) + noise / sqrt B) solves S = (I - eta H) S (I - eta H)
    + (eta^2 / B) C, C the per-example gradient covariance at w*; for small eta, tr S ~ (eta / 2B) tr(H^-1 C)."""
    Z, t = _logreg()
    n = len(t)
    _, grad = _logreg_fns(Z, t)
    ws = _w_star(Z, t)
    s = 1 / (1 + np.exp(-(Z @ ws)))
    H = (Z * (s * (1 - s))[:, None]).T @ Z / n
    G = (-t / (1 + np.exp(t * (Z @ ws))))[:, None] * Z  # per-example gradients at w*
    C = np.cov(G.T, bias=True)
    out = dict(etas=T_ETAS, batches=T_BATCHES, H=H, C=C, w_star=ws,
               trHinvC=float(np.trace(np.linalg.solve(H, C))))
    meas = np.zeros((len(T_ETAS), len(T_BATCHES), 3))
    pred = np.zeros((len(T_ETAS), len(T_BATCHES)))
    I2 = np.eye(2)
    for i, eta in enumerate(T_ETAS):
        A = I2 - eta * H
        for j, B in enumerate(T_BATCHES):
            M = np.eye(4) - np.kron(A, A)
            S = np.linalg.solve(M, (eta * eta / B * C).reshape(-1)).reshape(2, 2)
            pred[i, j] = float(np.trace(S))
            for sd in range(3):
                g = rng(1000 * i + 10 * j + sd)
                w = ws.copy()
                acc, cnt = 0.0, 0
                for k in range(33_000):
                    w = w - eta * grad(w, g.integers(0, n, B))
                    if k >= 3000 and k % 3 == 0:
                        acc += float(((w - ws) ** 2).sum())
                        cnt += 1
                meas[i, j, sd] = acc / cnt
        print(f"    eta {eta}: {meas[i].mean(1)}", flush=True)
    out.update(measured=meas, predicted=pred)
    T = np.array([[eta / B for B in T_BATCHES] for eta in T_ETAS])
    m = meas.mean(2)
    out["slope"] = float(np.polyfit(np.log(T.ravel()), np.log(m.ravel()), 1)[0])
    out["ratio"] = m / pred  # measured over predicted
    return out


# ---------------------------------------------------------------------------
# 5. The edge of stability
# ---------------------------------------------------------------------------
EOS_ETAS = [0.05, 0.1]


def compute_eos():
    from . import nets
    from .charopt import threads

    threads(1)
    out = {"etas": EOS_ETAS}
    for eta in EOS_ETAS:
        out[f"curve{eta}"] = nets.eos_run(eta)
        c = out[f"curve{eta}"]
        late = c[len(c) // 2:, 2]
        out[f"late_max{eta}"] = float(late.max())
        out[f"late_median{eta}"] = float(np.median(late))
        out[f"first_edge{eta}"] = int(c[np.argmax(c[:, 2] > 0.9 * 2 / eta), 0]) if (c[:, 2] > 0.9 * 2 / eta).any() else -1
        print(f"    eta {eta}: late median sharpness {np.median(late):.1f} (2/eta = {2 / eta:.0f})", flush=True)
    return out


# ---------------------------------------------------------------------------
# 6. Adam, up close
# ---------------------------------------------------------------------------
def compute_adamview():
    import torch

    from . import charopt as co

    co.threads(1)
    tr, _, _ = co.tensors()
    model = co.make_model(0)
    lr = 2e-3
    b1, b2 = 0.9, 0.999
    opt = torch.optim.Adam(model.parameters(), lr=lr, betas=(b1, b2))
    g = rng(1)
    coords = [(3, 7), (40, 100), (200, 31)]
    grads, ratios = [], {}
    for k in range(1, 1001):
        pos = torch.from_numpy(g.integers(co.CTX, len(tr), co.BATCH))
        loss = torch.nn.functional.cross_entropy(model(co.windows(tr, pos)), tr[pos])
        opt.zero_grad()
        loss.backward()
        G = model.h2.weight.grad
        if k <= 60:
            grads.append([float(G[i, j]) for i, j in coords])
        W0 = model.h2.weight.detach().clone()
        opt.step()
        if k in (1, 100, 1000):
            r = ((model.h2.weight.detach() - W0) / lr).abs().numpy().ravel()
            ratios[str(k)] = np.histogram(r, bins=40, range=(0, 2))[0]
            ratios[f"frac{k}"] = float((r > 0.9).mean())
            ratios[f"max{k}"] = float(r.max())
            ratios[f"median{k}"] = float(np.median(r))
    grads = np.array(grads)
    m = np.zeros(3)
    v = np.zeros(3)
    M, V, MH, VH = [], [], [], []
    for k, gk in enumerate(grads, 1):
        m = b1 * m + (1 - b1) * gk
        v = b2 * v + (1 - b2) * gk * gk
        M.append(m.copy())
        V.append(v.copy())
        MH.append(m / (1 - b1 ** k))
        VH.append(v / (1 - b2 ** k))
    out = dict(grads=grads, m=np.array(M), v=np.array(V), mhat=np.array(MH), vhat=np.array(VH), coords=coords,
               lr=lr, b1=b1, b2=b2, raw_first=float((1 - b1) / math.sqrt(1 - b2)))
    for k_ in ("1", "100", "1000"):
        out[f"hist{k_}"] = np.asarray(ratios[k_])
        out[f"frac{k_}"] = ratios[f"frac{k_}"]
        out[f"max{k_}"] = ratios[f"max{k_}"]
        out[f"median{k_}"] = ratios[f"median{k_}"]
    return out


# ---------------------------------------------------------------------------
# 7. Weight decay is not L2
# ---------------------------------------------------------------------------
DEC_LRS = [1e-3, 2e-3, 4e-3, 8e-3, 1.6e-2]
DEC_WD = [0.0, 0.03, 0.1, 0.3, 1.0, 3.0]
DEC_L2 = [0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
DEC_KW = dict(hid=128, subset=50_000, steps=2000, eval_every=200, sched="cosine")


def _dec_job(opt, lr, wd, seed):
    from . import charopt as co

    r = co.train(opt=opt, lr=lr, wd=wd, seed=seed, **DEC_KW)
    return dict(final=r["final"], curve=r["curve"])


def compute_decay():
    part = CACHE.partial("decay", dict(lrs=DEC_LRS, wd=DEC_WD, l2=DEC_L2, kw=DEC_KW))
    jobs = {}
    for lr in DEC_LRS:
        for wd in DEC_WD:
            jobs[f"adamw_{lr}_{wd}_0"] = ("adamw", lr, wd, 0)
        for l2 in DEC_L2:
            jobs[f"adam_l2_{lr}_{l2}_0"] = ("adam_l2", lr, l2, 0)
    _run_pieces(part, jobs, _dec_job)
    out = dict(lrs=DEC_LRS, wd=DEC_WD, l2=DEC_L2, **{k: v for k, v in DEC_KW.items()})
    for name, grid in (("adamw", DEC_WD), ("adam_l2", DEC_L2)):
        A = np.array([[part[f"{name}_{lr}_{w}_0"]["final"] for w in grid] for lr in DEC_LRS])
        out[f"grid_{name}"] = A
        i, j = np.unravel_index(np.nanargmin(A), A.shape)
        out[f"best_{name}"] = [DEC_LRS[i], grid[j]]
        more = {f"{name}_{DEC_LRS[i]}_{grid[j]}_{s}": (name, DEC_LRS[i], grid[j], s) for s in (1, 2)}
        _run_pieces(part, more, _dec_job)
        finals = [A[i, j]] + [part[k]["final"] for k in more]
        out[f"seeds_{name}"] = finals
        out[f"curve_{name}"] = np.array(part[f"{name}_{DEC_LRS[i]}_{grid[j]}_0"]["curve"])
        out[f"curve0_{name}"] = np.array(part[f"{name}_{DEC_LRS[i]}_0.0_0"]["curve"])  # the same rate, no decay
        # how much the best decay strength moves with the learning rate: the best column in each row
        out[f"bestcol_{name}"] = [int(np.nanargmin(row)) for row in A]
    out["none"] = float(np.nanmin(np.array([part[f"adamw_{lr}_0.0_0"]["final"] for lr in DEC_LRS])))
    return out


# ---------------------------------------------------------------------------
# 8. The natural gradient
# ---------------------------------------------------------------------------
NG_LRS = {"gd": [0.3, 1.0, 3.0, 10.0, 30.0], "adam": [3e-3, 1e-2, 3e-2, 1e-1, 3e-1],
          "kfac": [0.03, 0.1, 0.3, 1.0, 3.0], "ng": [0.03, 0.1, 0.3, 1.0, 3.0]}
NG_SEEDS = (0, 1, 2)


def _ng_job(opt, lr, seed, snaps):
    from . import nets
    from .charopt import threads

    threads(1)
    r = nets.ng_run(opt, lr, seed=seed, snaps=tuple(snaps))
    c = np.asarray(r["curve"])
    return dict(final=float(c[-1, 1]) if len(c) == 301 else float("nan"), curve=r["curve"], snaps=r["snaps"], P=r["P"])


def compute_natgrad():
    out = {}
    # (a) one loss, two parametrizations: w = (a, s b)
    Z, t = _logreg()
    n = len(t)
    loss, grad = _logreg_fns(Z, t)
    ws = _w_star(Z, t)
    start = np.array([-1.0, 0.2])

    def fisher(w):
        s = 1 / (1 + np.exp(-(Z @ w)))
        return (Z * (s * (1 - s))[:, None]).T @ Z / n

    for scale in (1.0, 0.25):  # w = (a, s b): s = 1/4 writes the second weight four times as large
        J = np.diag([1.0, scale])  # dw/dtheta
        for kind in ("gd", "ng"):
            th = np.linalg.solve(J, start)
            P = [J @ th]
            for _ in range(40):
                w = J @ th
                gt = J.T @ grad(w, np.arange(n))
                if kind == "ng":
                    gt = np.linalg.solve(J.T @ fisher(w) @ J, gt)
                th = th - (0.6 if kind == "gd" else 0.15) * gt
                P.append(J @ th)
            out[f"path_{kind}_{scale:g}"] = np.array(P)
    out["w_star"] = ws
    # (b) the spirals: four optimizers, each at its best rate
    part = CACHE.partial("natgrad", dict(lrs=NG_LRS, seeds=NG_SEEDS, v=2))
    from .nets import NG_SNAP

    jobs = {f"{o}_{lr}_{s}": (o, lr, s, NG_SNAP if s == 0 else ()) for o, lrs in NG_LRS.items() for lr in lrs
            for s in NG_SEEDS}
    _run_pieces(part, jobs, _ng_job)
    out["opts"] = list(NG_LRS)
    for o, lrs in NG_LRS.items():
        F = np.array([[part[f"{o}_{lr}_{s}"]["final"] for s in NG_SEEDS] for lr in lrs])
        mean = np.where(np.isfinite(F).all(1), F.mean(1), np.nan)
        i = int(np.nanargmin(mean))
        out[f"lrs_{o}"] = lrs
        out[f"finals_{o}"] = F
        out[f"best_{o}"] = lrs[i]
        out[f"edge_{o}"] = bool(i in (0, len(lrs) - 1))
        out[f"curves_{o}"] = np.array([np.asarray(part[f"{o}_{lrs[i]}_{s}"]["curve"]) for s in NG_SEEDS])
        sn = part[f"{o}_{lrs[i]}_0"]["snaps"]
        out[f"snaps_{o}"] = np.array([sn[str(k)] for k in NG_SNAP if str(k) in sn])
        out["P"] = part[f"{o}_{lrs[i]}_0"]["P"]
    out["snap_steps"] = list(NG_SNAP)
    from .nets import ng_data

    X, y = ng_data()
    out["X"], out["y"] = X, y
    return out


# ---------------------------------------------------------------------------
# 12. The race, run fairly
# ---------------------------------------------------------------------------
RACE_OPTS = ["sgdm", "adamw", "lion", "shampoo", "soap", "muon"]
_A = [5e-4, 1e-3, 2e-3, 4e-3, 8e-3, 1.6e-2]
RACE_LRS = {"sgdm": [0.0125, 0.025, 0.05, 0.1, 0.2, 0.4], "adamw": _A, "lion": [x / 5 for x in _A], "shampoo": _A,
            "soap": _A, "muon": _A}
RACE_STEPS_N = 3000
RACE_WRITE = (0, 100, 300, 1000, 3000)
RACE_SEEDS = (0, 1, 2)


def _race_job(opt, lr, seed):
    from . import charopt as co

    r = co.train(opt=opt, lr=lr, seed=seed, steps=RACE_STEPS_N, sched="cosine", eval_every=150, write_at=RACE_WRITE)
    return dict(final=r["final"], curve=r["curve"], ms=r["ms"], writes=r["writes"], diverged=r.get("diverged", 0))


def compute_race():
    part = CACHE.partial("race", dict(steps=RACE_STEPS_N, write=RACE_WRITE, v=1))  # each piece is keyed by its rate
    jobs = {f"{o}_{lr}_0": (o, lr, 0) for o in RACE_OPTS for lr in RACE_LRS[o]}
    _run_pieces(part, jobs, _race_job)
    out = dict(opts=RACE_OPTS, steps=RACE_STEPS_N, write_at=list(RACE_WRITE), seeds=list(RACE_SEEDS))
    for o in RACE_OPTS:
        lrs = list(RACE_LRS[o])
        # a best rate at the end of the grid is not a tuned rate: extend the grid by factors of 2 (up to 3 more)
        for _ in range(3):
            F = np.array([part[f"{o}_{lr}_0"]["final"] for lr in lrs], float)
            i = int(np.nanargmin(F))
            if 0 < i < len(lrs) - 1:
                break
            new = lrs[-1] * 2 if i == len(lrs) - 1 else lrs[0] / 2
            _run_pieces(part, {f"{o}_{new}_0": (o, new, 0)}, _race_job)
            lrs = sorted(lrs + [new])
        F = np.array([part[f"{o}_{lr}_0"]["final"] for lr in lrs], float)
        i = int(np.nanargmin(F))
        more = {f"{o}_{lrs[i]}_{s}": (o, lrs[i], s) for s in RACE_SEEDS[1:]}
        _run_pieces(part, more, _race_job)
        runs = [part[f"{o}_{lrs[i]}_{s}"] for s in RACE_SEEDS]
        out[f"lrs_{o}"] = lrs
        out[f"sweep_{o}"] = F
        out[f"best_{o}"] = lrs[i]
        out[f"edge_{o}"] = bool(i in (0, len(lrs) - 1))
        out[f"curves_{o}"] = np.array([np.asarray(r["curve"]) for r in runs])
        out[f"finals_{o}"] = [float(r["final"]) for r in runs]
        out[f"ms_{o}"] = float(np.mean([r["ms"] for r in runs]))
        out[f"writes_{o}"] = [runs[0]["writes"][str(k)] for k in RACE_WRITE]
        print(f"    {o}: best lr {lrs[i]}, finals {out[f'finals_{o}']}", flush=True)
    return out


# ---------------------------------------------------------------------------
# 11. Newton-Schulz on real matrices
# ---------------------------------------------------------------------------
def _ns_history(M, coeffs_list):
    """The singular values of M / |M|_F and after each round X <- aX + b(XX^T)X + c(XX^T)^2 X (float32, as in
    practice; one normalization at the start, as in Muon)."""
    import torch

    X = torch.tensor(M, dtype=torch.float32)
    X = X / (X.norm() + 1e-7)
    hist = [torch.linalg.svdvals(X).numpy()]
    for a, b, c in coeffs_list:
        A = X @ X.T
        X = a * X + (b * A + c * A @ A) @ X
        hist.append(torch.linalg.svdvals(X).numpy())
    return np.array(hist)


def compute_ns():
    from . import charopt as co

    best = float(load("race")["best_adamw"])
    r = co.train(opt="adamw", lr=best, seed=0, steps=RACE_STEPS_N, sched="cosine", eval_every=RACE_STEPS_N, grab=300)
    out = dict(lr=best)
    for key, M in (("grad", r["grad"]), ("weight", r["weight"])):
        s0 = np.linalg.svd(M, compute_uv=False)
        out[f"sv_{key}"] = s0
        big = s0 > 0.01 * s0.max()
        for scheme, cl in (("jordan", [co.NS_JORDAN] * 5), ("cubic", [co.NS_CUBIC] * 12),
                           ("hybrid", [co.NS_JORDAN] * 8 + [co.NS_EXACT] * 2)):
            h = _ns_history(M, cl)
            out[f"hist_{key}_{scheme}"] = h
            srt = np.sort(h, 1)[:, ::-1]
            out[f"dev_{key}_{scheme}"] = [float(np.abs(row[big] - 1).max()) for row in srt]  # the big ones' worst gap
            out[f"band_{key}_{scheme}"] = [float(srt[-1][big].min()), float(srt[-1][big].max())]
        out[f"nbig_{key}"] = int(big.sum())
        # the scalar polynomial on the singular values agrees with the matrix iteration
        a, b, c = co.NS_JORDAN
        x = s0 / np.sqrt((s0 ** 2).sum())
        for _ in range(5):
            x = a * x + b * x ** 3 + c * x ** 5
        out[f"match_{key}"] = float(np.abs(np.sort(x)[::-1] - np.sort(out[f"hist_{key}_jordan"][-1])[::-1]).max())
    return out


# ---------------------------------------------------------------------------
# 13-14. Schedules: cosine, WSD, EMA, schedule-free
# ---------------------------------------------------------------------------
SCH_LENGTHS = (1000, 2000, 4000)
SCH_SEEDS = (0, 1)
SF_MULTS = (0.5, 1.0, 2.0, 4.0)


def _sch_job(kind, lr, steps, seed):
    from . import charopt as co

    if kind == "cosine":
        r = co.train(opt="adamw", lr=lr, steps=steps, seed=seed, sched="cosine", eval_every=100)
    elif kind == "constant":
        br = tuple((int(0.8 * S), S) for S in SCH_LENGTHS)
        r = co.train(opt="adamw", lr=lr, steps=steps, seed=seed, sched="constant", eval_every=100, ema=0.998,
                     branches=br)
    else:  # schedule-free
        r = co.train(opt="sfadamw", lr=lr, steps=steps, seed=seed, sched="constant", eval_every=100)
    return dict(final=r["final"], curve=r["curve"], ema_curve=r["ema_curve"], branches=r["branches"])


def compute_schedule():
    lr = float(load("race")["best_adamw"])
    part = CACHE.partial("schedule", dict(lr=lr, lengths=SCH_LENGTHS, seeds=SCH_SEEDS, sf=SF_MULTS, v=1))
    jobs = {}
    for s in SCH_SEEDS:
        for S in SCH_LENGTHS:
            jobs[f"cosine_{S}_{s}"] = ("cosine", lr, S, s)
        jobs[f"constant_{s}"] = ("constant", lr, max(SCH_LENGTHS), s)
    for mlt in SF_MULTS:
        jobs[f"sfgrid_{mlt}"] = ("sf", lr * mlt, 2000, 0)
    _run_pieces(part, jobs, _sch_job)
    sf = [part[f"sfgrid_{m}"]["final"] for m in SF_MULTS]
    mbest = SF_MULTS[int(np.nanargmin(sf))]
    _run_pieces(part, {f"sf_{s}": ("sf", lr * mbest, max(SCH_LENGTHS), s) for s in SCH_SEEDS}, _sch_job)
    out = dict(lr=lr, lengths=list(SCH_LENGTHS), seeds=list(SCH_SEEDS), sf_mults=list(SF_MULTS), sf_grid=sf,
               sf_best=mbest, sf_edge=bool(mbest in (SF_MULTS[0], SF_MULTS[-1])))
    for s in SCH_SEEDS:
        for S in SCH_LENGTHS:
            out[f"cos_{S}_{s}"] = np.array(part[f"cosine_{S}_{s}"]["curve"])
            out[f"cosfinal_{S}_{s}"] = part[f"cosine_{S}_{s}"]["final"]
        c = part[f"constant_{s}"]
        out[f"const_{s}"] = np.array(c["curve"])
        out[f"ema_{s}"] = np.array(c["ema_curve"])
        for S in SCH_LENGTHS:
            out[f"wsdfinal_{S}_{s}"] = c["branches"][f"{int(0.8 * S)}_{S}"]["final"]
            out[f"wsdquick_{S}_{s}"] = c["branches"][f"{int(0.8 * S)}_{S}"]["quick"]  # on the curves' 20,000
            out[f"wsdcurve_{S}_{s}"] = np.array(c["branches"][f"{int(0.8 * S)}_{S}"]["curve"])
        out[f"constfinal_{s}"] = c["final"]
        out[f"sf_{s}"] = np.array(part[f"sf_{s}"]["curve"])
        out[f"sffinal_{s}"] = part[f"sf_{s}"]["final"]
    return out


def compute_river():
    """The river valley (Wen et al. 2024), as a toy: L = R(x) + (A/2)(y - c(x))^2, a slow river R along the valley
    floor y = c(x) and steep hills across it; every gradient carries noise. A step's size sets how far up the hills
    the noise throws it (a 'hill' loss about eta sigma^2 / 4) and how fast it travels along the river."""
    A, sig, T = 4.0, 1.0, 400
    eta0 = 0.25

    def R(x):
        return 0.5 * np.log1p(np.exp(-(x - 6.0)))  # the river: falls gently towards large x

    def dR(x):
        return -0.5 / (1 + np.exp(x - 6.0))

    def c(x):
        return 0.8 * np.sin(0.5 * x)

    def dc(x):
        return 0.4 * np.cos(0.5 * x)

    def sched(k, kind):
        if kind == "constant":
            return eta0
        if kind == "small":
            return eta0 / 5
        if kind == "cosine":
            return eta0 * 0.5 * (1 + math.cos(math.pi * k / T))
        return eta0 if k < 0.8 * T else eta0 * (T - k) / (0.2 * T)  # wsd

    kinds = ["constant", "cosine", "wsd", "small"]
    out = dict(A=A, sigma=sig, T=T, eta0=eta0, kinds=kinds)
    for kind in kinds:
        riv, hill, paths = [], [], []
        for sd in range(20):
            g = rng(500 + sd)
            x, y = 0.0, c(0.0)
            rr, hh, P = [], [], [(x, y)]
            for k in range(T):
                e = y - c(x)
                gx = dR(x) - A * e * dc(x) + 0.3 * sig * g.normal()
                gy = A * e + sig * g.normal()
                lr = sched(k, kind)
                x, y = x - lr * gx, y - lr * gy
                rr.append(R(x))
                hh.append(0.5 * A * (y - c(x)) ** 2)
                P.append((x, y))
            riv.append(rr)
            hill.append(hh)
            paths.append(P)
        out[f"river_{kind}"] = np.array(riv).mean(0)
        out[f"hill_{kind}"] = np.array(hill).mean(0)
        out[f"path_{kind}"] = np.array(paths[0])
        out[f"final_{kind}"] = float(np.array(riv)[:, -1].mean() + np.array(hill)[:, -1].mean())
    out["hill_pred"] = eta0 * sig ** 2 / 4 / (1 - eta0 * A / 2)  # exact for the linear hill: (A/2) Var, Var = eta s^2/(A(2 - eta A))
    xs = np.linspace(-1, 13, 141)
    out["grid_x"] = xs
    out["river_x"] = R(xs)
    out["floor_y"] = c(xs)
    return out


# ---------------------------------------------------------------------------
# 15. Keeping training stable
# ---------------------------------------------------------------------------
EQ_WD = (0.1, 0.4, 1.6)
EQ_LR = 3e-3
EQ_STEPS = 4000


def _eq_job(wd):
    from . import charopt as co

    r = co.train(opt="adamw", lr=EQ_LR, wd=wd, steps=EQ_STEPS, sched="constant", norm=True, track=50,
                 eval_every=500)
    return dict(final=r["final"], track=r["track"], curve=r["curve"])


def compute_equilibrium():
    """A matrix followed by a normalization is scale-invariant: its gradient is orthogonal to it, so the update
    u pushes the norm up (a random walk, |W|^2 grows by about eta^2 |u|^2 per step, more when successive updates are
    correlated: momentum b1 makes the sum of correlations (1 + b1)/(1 - b1)), while decoupled decay shrinks it by
    2 eta lambda |W|^2 a step. Equilibrium: |W|^2 = eta |u|^2 (1 + b1) / (2 lambda (1 - b1))."""
    part = CACHE.partial("equilibrium", dict(wd=EQ_WD, lr=EQ_LR, steps=EQ_STEPS))
    _run_pieces(part, {f"wd_{w}": (w,) for w in EQ_WD}, _eq_job)
    b1 = 0.9
    out = dict(wd=list(EQ_WD), lr=EQ_LR, steps=EQ_STEPS, b1=b1)
    for w in EQ_WD:
        T = np.array(part[f"wd_{w}"]["track"])
        late = T[T[:, 0] >= 0.75 * EQ_STEPS]
        u2 = float((late[:, 2] ** 2).mean())
        pred = math.sqrt(EQ_LR * u2 * (1 + b1) / (2 * w * (1 - b1)))
        out[f"track_{w}"] = T
        out[f"norm_{w}"] = float(late[:, 1].mean())
        out[f"pred_{w}"] = pred
        out[f"pred_nomom_{w}"] = math.sqrt(EQ_LR * u2 / (2 * w))
        out[f"cos_{w}"] = float(late[:, 3].mean())
        out[f"tau_{w}"] = 1 / (2 * EQ_LR * w)
        out[f"final_{w}"] = part[f"wd_{w}"]["final"]
    ns = [out[f"norm_{w}"] for w in EQ_WD]
    out["slope"] = float(np.polyfit(np.log(EQ_WD), np.log(ns), 1)[0])
    return out


SPIKE_CFGS = {
    "muon_slow": dict(opt_name="muon", lr=0.03, clip_tau=None),
    "muon_fast": dict(opt_name="muon", lr=0.12, clip_tau=None),
    "muon_fast_qkclip": dict(opt_name="muon", lr=0.12, clip_tau=100.0),
    "adam_fast": dict(opt_name="adam", lr=0.05, clip_tau=None),
    "adam_fast_gclip": dict(opt_name="adam", lr=0.05, clip_tau=None, gclip=1.0),
    "adam_fast_qkclip": dict(opt_name="adam", lr=0.05, clip_tau=100.0),
}
SPIKE_SEEDS = (0, 1)


def _spike_job(name, seed):
    from . import nets
    from .charopt import threads

    threads(1)
    r = nets.qk_run(seed=seed, **SPIKE_CFGS[name])
    return dict(r, final=r["held"])


def compute_spikes():
    part = CACHE.partial("spikes", dict(cfgs=SPIKE_CFGS, seeds=SPIKE_SEEDS, v=1))
    _run_pieces(part, {f"{k}_{s}": (k, s) for k in SPIKE_CFGS for s in SPIKE_SEEDS}, _spike_job)
    out = dict(names=list(SPIKE_CFGS), seeds=list(SPIKE_SEEDS), cfgs=SPIKE_CFGS)
    for k in SPIKE_CFGS:
        logs = [np.array(part[f"{k}_{s}"]["log"]) for s in SPIKE_SEEDS]
        n = min(len(L) for L in logs)
        out[f"log_{k}"] = np.array([L[:n] for L in logs])
        out[f"held_{k}"] = [part[f"{k}_{s}"]["held"] for s in SPIKE_SEEDS]
        out[f"maxlogit_{k}"] = [float(np.nanmax(L[:, 2])) for L in logs]
        out[f"clipped_{k}"] = [part[f"{k}_{s}"]["clipped"] for s in SPIKE_SEEDS]
        jumps = []
        for L in logs:
            l_ = L[:, 1]
            sm = np.convolve(l_, np.ones(5) / 5, mode="valid")
            jumps.append(float(np.max(sm[10:] - np.minimum.accumulate(sm)[10:])))  # the biggest rise above the best so far
        out[f"jump_{k}"] = jumps
    return out


ITEMS = {
    "quad": compute_quad,
    "race3d": compute_race3d,
    "noise": compute_noise,
    "temperature": compute_temperature,
    "eos": compute_eos,
    "adamview": compute_adamview,
    "decay": compute_decay,
    "natgrad": compute_natgrad,
    "race": compute_race,
    "ns": compute_ns,
    "schedule": compute_schedule,
    "river": compute_river,
    "equilibrium": compute_equilibrium,
    "spikes": compute_spikes,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
