"""Deep pricing and hedging (Part 17, the volatility desk and research): networks that price, calibrate, hedge and
simulate, trained on the House's own engines.

* the neural calibrator (Horvath, Muguruza and Tomas 2021, pointwise form): a network learns rough Bergomi's implied
  volatility as a function of (H, eta, rho, xi0, xi1, T, k) from Monte Carlo, and then calibrates a whole surface in
  milliseconds by gradient descent through itself;
* differential machine learning (Huge and Savine 2020): train on payoffs *and* their pathwise derivatives;
* the deep BSDE solver (Han, Jentzen and E 2018) for a 100-dimensional nonlinear pricing equation;
* deep optimal stopping (Becker, Cheridito and Jentzen 2019) for a Bermudan max-call;
* the deep hedger (Buehler, Gonon, Teichmann and Wood 2019) with proportional costs, under an entropic or CVaR risk
  measure, and its indifference price;
* robust bounds from a neural SDE (Gierjatowicz et al. 2022);
* market generators scored on the stylized facts (signatures, a small diffusion model).

Everything runs on a CPU in minutes (torch, float32 unless noted); the production version retrains at full size.
"""

from __future__ import annotations

import math
import time

import numpy as np

from explainer.quant.house import bs

# ---------------------------------------------------------------------------
# The neural calibrator: rough Bergomi, pointwise
# ---------------------------------------------------------------------------
# the forward variance is a ramp from xi0 (today) to xi1 at T_RAMP and flat after it: two numbers for the term structure
CALIB_BOUNDS = {"H": (0.02, 0.5), "eta": (0.3, 4.0), "rho": (-0.9, 0.6), "vol0": (0.25, 1.2), "vol1": (0.25, 1.2)}
CALIB_NAMES = tuple(CALIB_BOUNDS)
T_RAMP = 0.5
T_MIN, T_MAX = 6 / 365, 200 / 365
K_ABS = 0.6


def xi_ramp(vol0: float, vol1: float, t_ramp: float = T_RAMP):
    """xi(t) = vol0^2 + (vol1^2 - vol0^2) min(t / t_ramp, 1)."""
    a, b = vol0 ** 2, vol1 ** 2
    return lambda t: a + (b - a) * np.minimum(np.asarray(t, float) / t_ramp, 1.0)


def _sample_params(rng, n):
    lo = np.array([v[0] for v in CALIB_BOUNDS.values()])
    hi = np.array([v[1] for v in CALIB_BOUNDS.values()])
    return lo + (hi - lo) * rng.random((n, len(lo)))


def rbergomi_iv_samples(theta, n_points=48, n_paths=10000, seed=0, days=200):
    """Implied volatilities of out-of-the-money options under rough Bergomi with parameters ``theta`` = (H, eta, rho,
    vol0, vol1), at ``n_points`` random (T, k): T log-uniform in [6, 200] days, k = z sd(T) with z uniform in
    [-2.5, 1.5] (BTC's quotes reach further on the put side), |k| <= 0.6. Monte Carlo with ``n_paths`` paths, one
    step a day. Returns rows (T, k, iv); points whose price is too small to invert reliably are dropped."""
    from explainer.quant.house import rough as R

    H, eta, rho, v0, v1 = theta
    rng = np.random.default_rng(seed)
    xi = xi_ramp(v0, v1)
    S = R.rbergomi_paths(H, eta, rho, xi, days / 365, days, n_paths, seed=seed + 1)
    d = np.unique(np.round(np.exp(rng.uniform(np.log(T_MIN * 365), np.log(T_MAX * 365), n_points))).astype(int))
    out = []
    per = int(np.ceil(n_points / len(d)))
    for dd in d:
        T = dd / 365
        tt = np.linspace(0, T, 9)
        sd = math.sqrt(float(np.mean(xi(tt))) * T)
        x = S[dd]
        for z in rng.uniform(-2.5, 1.5, per):
            k = float(np.clip(z * sd, -K_ABS, K_ABS))
            cp = 1 if k >= 0 else -1
            p = float(np.mean(np.maximum(cp * (x - math.exp(k)), 0.0)))
            if p < 2e-4:
                continue
            iv = bs.implied_vol(p, 1.0, math.exp(k), T, 0.0, 0.0, cp)
            if np.isfinite(iv) and 0.05 < iv < 4.0:
                out.append((T, k, iv))
    return np.array(out, float).reshape(-1, 3)


def calib_features(theta, T, k):
    """The network's inputs, scaled to about [-1, 1]: the five parameters, log T, and k / sqrt(T)."""
    theta = np.atleast_2d(np.asarray(theta, float))
    lo = np.array([v[0] for v in CALIB_BOUNDS.values()])
    hi = np.array([v[1] for v in CALIB_BOUNDS.values()])
    p = 2 * (theta - lo) / (hi - lo) - 1
    T = np.asarray(T, float).reshape(-1, 1)
    k = np.asarray(k, float).reshape(-1, 1)
    lt = 2 * (np.log(T) - math.log(T_MIN)) / (math.log(T_MAX) - math.log(T_MIN)) - 1
    m = k / np.sqrt(T) / 2.0
    return np.hstack([np.broadcast_to(p, (len(T), p.shape[1])), lt, m]).astype(np.float32)


def _mlp(d_in, width, depth, d_out=1, act=None):
    import torch.nn as nn

    act = act or nn.SiLU
    layers, d = [], d_in
    for _ in range(depth):
        layers += [nn.Linear(d, width), act()]
        d = width
    layers.append(nn.Linear(d, d_out))
    return nn.Sequential(*layers)


def calib_net(width=96, depth=4):
    """The pointwise network: 7 inputs (calib_features) -> implied volatility (via softplus, so it stays positive)."""
    import torch.nn as nn

    return nn.Sequential(_mlp(7, width, depth), nn.Softplus())


def train_calib_net(X, y, epochs=60, batch=2048, lr=2e-3, seed=0, val=None, log=None):
    """Adam with a cosine schedule on mean squared error in vol points. ``val`` = (X, y) for a held-out curve."""
    import torch

    torch.manual_seed(seed)
    net = calib_net()
    Xt, yt = torch.from_numpy(X), torch.from_numpy(y.astype(np.float32)).reshape(-1, 1)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    steps = epochs * int(np.ceil(len(X) / batch))
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps)
    hist = []
    g = torch.Generator().manual_seed(seed)
    for ep in range(epochs):
        perm = torch.randperm(len(X), generator=g)
        tot = 0.0
        for i in range(0, len(X), batch):
            j = perm[i:i + batch]
            loss = ((net(Xt[j]) - yt[j]) * 100).pow(2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            tot += float(loss) * len(j)
        row = {"epoch": ep + 1, "train_rmse": math.sqrt(tot / len(X))}
        if val is not None:
            with torch.no_grad():
                row["val_rmse"] = float(((net(torch.from_numpy(val[0])) - torch.from_numpy(
                    val[1].astype(np.float32)).reshape(-1, 1)) * 100).pow(2).mean().sqrt())
        hist.append(row)
        if log:
            log(row)
    return net, hist


def calibrate_neural(net, T, k, iv, w=None, starts=8, seed=0, iters=200):
    """Rough Bergomi calibrated to quotes (T, k, iv) through the network: Adam then L-BFGS on the five parameters
    (kept inside their box by a tanh map), from several starts; the best fit wins. Returns params, the weighted RMSE in
    vol points, and the time taken."""
    import torch

    t0 = time.perf_counter()
    lo = torch.tensor([v[0] for v in CALIB_BOUNDS.values()])
    hi = torch.tensor([v[1] for v in CALIB_BOUNDS.values()])
    T = np.asarray(T, float)
    k = np.asarray(k, float)
    w = np.ones_like(T) if w is None else np.asarray(w, float)
    w = torch.tensor(w / w.mean(), dtype=torch.float32)
    tgt = torch.tensor(np.asarray(iv, float), dtype=torch.float32)
    base = torch.from_numpy(calib_features(np.zeros(5) + lo.numpy(), T, k))
    lt_m = base[:, 5:]
    for p_ in net.parameters():
        p_.requires_grad_(False)

    def model(u):
        theta = lo + (hi - lo) * (torch.tanh(u) + 1) / 2
        p = 2 * (theta - lo) / (hi - lo) - 1
        x = torch.cat([p.expand(len(T), 5), lt_m], dim=1)
        return net(x).squeeze(1), theta

    rng = np.random.default_rng(seed)
    best = None
    for s in range(starts):
        u = torch.tensor(rng.uniform(-1.2, 1.2, 5), dtype=torch.float32, requires_grad=True)
        opt = torch.optim.Adam([u], lr=0.05)
        for _ in range(iters):
            f, _ = model(u)
            loss = (w * (f - tgt).pow(2)).mean() * 1e4
            opt.zero_grad()
            loss.backward()
            opt.step()
        lb = torch.optim.LBFGS([u], max_iter=100, line_search_fn="strong_wolfe")

        def closure():
            lb.zero_grad()
            f, _ = model(u)
            ls = (w * (f - tgt).pow(2)).mean() * 1e4
            ls.backward()
            return ls
        lb.step(closure)
        with torch.no_grad():
            f, th = model(u)
            r = float((w * (f - tgt).pow(2)).mean().sqrt() * 100)
        if best is None or r < best[1]:
            best = (th.numpy().astype(float), r, f.numpy().astype(float))
    for p_ in net.parameters():
        p_.requires_grad_(True)
    return {"params": dict(zip(CALIB_NAMES, map(float, best[0]))), "x": best[0].tolist(), "rmse": best[1],
            "fit": best[2], "seconds": time.perf_counter() - t0}


# ---------------------------------------------------------------------------
# The deep hedger (Buehler, Gonon, Teichmann and Wood 2019)
# ---------------------------------------------------------------------------
def gbm_torch(n, steps, T, sigma, S0=100.0, gen=None):
    """Black-Scholes paths with zero rates, as a (n, steps + 1) float32 tensor."""
    import torch

    dt = T / steps
    z = torch.randn(n, steps, generator=gen)
    inc = -0.5 * sigma ** 2 * dt + sigma * math.sqrt(dt) * z
    return S0 * torch.exp(torch.cat([torch.zeros(n, 1), torch.cumsum(inc, 1)], 1))


class Hedger:
    """A policy for the hedge ratio at each rebalancing date.

    ``kind='mlp'``: Buehler et al.'s semi-recurrent network, delta_k = f(log(S_k/K), tau_k, delta_{k-1}); it is told
    nothing about bands.  ``kind='band'``: the no-transaction band network of Imaki et al. (2021): the network
    outputs a band [lo, hi] from (log(S_k/K), tau_k) and the hedge only moves to its nearest edge."""

    def __init__(self, kind="mlp", width=32, depth=3, seed=0):
        import torch

        torch.manual_seed(seed)
        self.kind = kind
        self.net = _mlp(3 if kind == "mlp" else 2, width, depth, 1 if kind == "mlp" else 2)

    def parameters(self):
        return self.net.parameters()

    def __call__(self, x, tau, prev):
        import torch

        if self.kind == "mlp":
            return self.net(torch.stack([x, tau, prev], -1)).squeeze(-1)
        o = self.net(torch.stack([x, tau], -1))
        lo = o[..., 0]
        hi = lo + torch.nn.functional.softplus(o[..., 1])
        return torch.minimum(torch.maximum(prev, lo), hi)


def hedge_pnl(policy, S, K, T, cost=0.0, cp=1):
    """The P&L of a short option hedged by ``policy`` along paths ``S`` (n, steps + 1), proportional ``cost`` on
    every trade (including the first; the hedge is not unwound at expiry). Returns (pnl, costs, holdings)."""
    import torch

    n, m = S.shape
    steps = m - 1
    dt = T / steps
    prev = torch.zeros(n)
    pnl = torch.zeros(n)
    costs = torch.zeros(n)
    held = []
    for k in range(steps):
        tau = torch.full((n,), (T - k * dt) / T)
        d = policy(torch.log(S[:, k] / K), tau, prev)
        costs = costs + cost * torch.abs(d - prev) * S[:, k]
        pnl = pnl + d * (S[:, k + 1] - S[:, k])
        prev = d
        held.append(d)
    Z = torch.clamp(cp * (S[:, -1] - K), min=0.0)
    return pnl - costs - Z, costs, torch.stack(held, 1)


def entropic(X, gamma=1.0):
    """The entropic risk measure (1/gamma) log E[exp(-gamma X)]: exponential utility's certainty-equivalent loss."""
    import torch

    return (torch.logsumexp(-gamma * X, 0) - math.log(len(X))) / gamma


def cvar(X, alpha=0.5):
    """Expected shortfall of the loss -X at level alpha (the mean of the worst alpha fraction)."""
    import torch

    k = max(1, int(round(alpha * len(X))))
    return torch.topk(-X, k).values.mean()


def train_hedger(kind="mlp", cost=0.0, sigma=0.2, T=30 / 365, steps=30, K=100.0, gamma=1.0, risk="entropic",
                 iters=1500, batch=8192, lr=3e-3, seed=0, snap_at=(), snap_fn=None, log=None):
    """Train a hedger on fresh Black-Scholes paths each iteration. The objective (entropic or CVaR risk of the hedged
    short call) is also the indifference price: what the seller must charge to be no worse off than not selling
    (with costs and no option, not trading at all is optimal, and risk 0). Returns the policy, the loss curve and
    any snapshots ``snap_fn(policy)`` taken at the iterations in ``snap_at``."""
    import torch

    gen = torch.Generator().manual_seed(seed + 1)
    pol = Hedger(kind, seed=seed)
    opt = torch.optim.Adam(pol.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, iters)
    rho = (lambda X: entropic(X, gamma)) if risk == "entropic" else cvar
    curve, snaps = [], {}
    for it in range(iters + 1):
        if it in snap_at and snap_fn is not None:
            with torch.no_grad():
                snaps[it] = snap_fn(pol)
        if it == iters:
            break
        S = gbm_torch(batch, steps, T, sigma, K, gen)
        X, _, _ = hedge_pnl(pol, S, K, T, cost)
        loss = rho(X)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        curve.append(float(loss.detach()))
        if log and it % 100 == 0:
            log(it, curve[-1])
    return pol, curve, snaps


def evaluate_hedger(pol, cost=0.0, sigma=0.2, T=30 / 365, steps=30, K=100.0, gamma=1.0, n=200000, seed=99):
    """Out-of-sample: the indifference price (entropic risk), CVaR 50%, mean cost and turnover on fresh paths."""
    import torch

    gen = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        S = gbm_torch(n, steps, T, sigma, K, gen)
        X, c, h = hedge_pnl(pol, S, K, T, cost)
        turn = torch.abs(torch.diff(torch.cat([torch.zeros(n, 1), h], 1), dim=1)).sum(1)
        return {"price": float(entropic(X, gamma)), "cvar50": float(cvar(X, 0.5)), "mean_pnl": float(X.mean()),
                "sd_pnl": float(X.std()), "mean_cost": float(c.mean()), "turnover": float(turn.mean())}


def delta_hedger(sigma, T, K=100.0, band=None):
    """Black-Scholes delta as a policy (optionally with Whalley-Wilmott's band, cost and risk aversion given as
    band=(cost, gamma)), for comparison on the same paths."""
    import torch

    from explainer.quant.house import quoting

    class P:
        def __call__(self, x, tau, prev):
            S = (K * torch.exp(x)).numpy()
            t = np.maximum(tau.numpy() * T, 1e-9)
            if band is None:
                d = bs.greeks(S, K, t, sigma, 0.0, 0.0, 1)["delta"]
                return torch.as_tensor(d, dtype=torch.float32)
            b = quoting.ww_band(S, K, t, sigma, band[0], gamma_risk=band[1])
            return torch.minimum(torch.maximum(prev, torch.as_tensor(b["lo"], dtype=torch.float32)),
                                 torch.as_tensor(b["hi"], dtype=torch.float32))
    return P()


# ---------------------------------------------------------------------------
# Hutchinson, Lo and Poggio (1994), redone with a small MLP
# ---------------------------------------------------------------------------
def hlp_dataset(n_paths=10, days=504, sigma=0.2, r=0.0, seed=0):
    """Simulated 'market data' in the spirit of HLP: two years of daily prices; each day, calls struck on a grid
    around the price at listing, expiring at quarterly dates, priced by Black-Scholes. Rows (S/K, T, C/K)."""
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n_paths):
        S = 50 * np.exp(np.cumsum(np.r_[0, sigma * math.sqrt(1 / 252) * rng.standard_normal(days - 1)
                                       - 0.5 * sigma ** 2 / 252]))
        for start in range(0, days - 63, 21):
            K0 = np.round(S[start] / 5) * 5
            for K in K0 + 5 * np.arange(-2, 3):
                for d in range(start, start + 63):
                    T = (start + 63 - d) / 252
                    c = bs.price(S[d], K, T, sigma, r, 0.0, 1)
                    rows.append((S[d] / K, T, c / K))
    return np.array(rows, float)


def train_mlp_regressor(X, y, width=32, depth=2, epochs=200, lr=3e-3, batch=1024, seed=0):
    import torch

    torch.manual_seed(seed)
    net = _mlp(X.shape[1], width, depth, y.shape[1] if y.ndim > 1 else 1)
    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.float32).reshape(len(X), -1)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
    g = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        perm = torch.randperm(len(X), generator=g)
        for i in range(0, len(X), batch):
            j = perm[i:i + batch]
            loss = (net(Xt[j]) - yt[j]).pow(2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
        sched.step()
    return net


# ---------------------------------------------------------------------------
# Differential machine learning (Huge and Savine 2020): a Bachelier basket
# ---------------------------------------------------------------------------
def bachelier_basket(d=7, seed=0):
    """A random d-asset Bachelier market (normal dynamics, correlated) and a basket call: volatilities 10-30, a random
    correlation matrix, equal weights, strike 100, one year from the training date to expiry."""
    rng = np.random.default_rng(seed)
    vol = rng.uniform(10, 30, d)
    A = rng.standard_normal((d, d))
    C = A @ A.T
    C = C / np.sqrt(np.outer(np.diag(C), np.diag(C)))
    cov = np.outer(vol, vol) * C
    w = np.full(d, 1 / d)
    return {"d": d, "cov": cov, "chol": np.linalg.cholesky(cov), "w": w, "K": 100.0, "T": 1.0,
            "bvol": float(np.sqrt(w @ cov @ w))}


def bachelier_price(mkt, X):
    """Exact basket call price and its gradient at states X (n, d)."""
    from scipy.stats import norm

    B = X @ mkt["w"]
    s = mkt["bvol"] * math.sqrt(mkt["T"])
    m = (B - mkt["K"]) / s
    price = (B - mkt["K"]) * norm.cdf(m) + s * norm.pdf(m)
    return price, norm.cdf(m)[:, None] * mkt["w"][None, :]


def bachelier_samples(mkt, n, seed=0):
    """Training data as a desk would make it: states X spread around the money, one simulated payoff each, and its
    pathwise derivative dY/dX (here 1{basket > K} w). Labels are noisy; their expectations are the price and delta."""
    rng = np.random.default_rng(seed)
    d = mkt["d"]
    X = 100 + 1.5 * rng.standard_normal((n, d)) @ mkt["chol"].T  # spread like 1.5 years of moves
    XT = X + math.sqrt(mkt["T"]) * rng.standard_normal((n, d)) @ mkt["chol"].T
    BT = XT @ mkt["w"]
    Y = np.maximum(BT - mkt["K"], 0.0)
    dY = (BT > mkt["K"]).astype(float)[:, None] * mkt["w"][None, :]
    return X, Y, dY


def train_differential(X, Y, dY=None, lam=1.0, width=20, depth=4, epochs=None, lr=3e-3, seed=0):
    """An MLP fitted to (X, Y), and if ``dY`` is given also to the pathwise derivatives, by backpropagating through
    the network's own input gradient (Huge and Savine's 'twin network'). Inputs and outputs are normalized; the
    derivative loss is weighted so both terms count about equally, times ``lam``."""
    import torch

    torch.manual_seed(seed)
    mx, sx = X.mean(0), X.std(0)
    my, sy = Y.mean(), Y.std()
    Xn = torch.tensor((X - mx) / sx, dtype=torch.float32)
    Yn = torch.tensor((Y - my) / sy, dtype=torch.float32).reshape(-1, 1)
    net = _mlp(X.shape[1], width, depth, act=torch.nn.Softplus)
    use_d = dY is not None
    if use_d:
        Dn = torch.tensor(dY * sx / sy, dtype=torch.float32)
        wd = 1.0 / (Dn.pow(2).mean(0) + 1e-8)
    epochs = epochs or max(100, int(400000 / len(X)))
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
    batch = min(256, len(X))
    g = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        perm = torch.randperm(len(X), generator=g)
        for i in range(0, len(X), batch):
            j = perm[i:i + batch]
            xb = Xn[j].requires_grad_(use_d)
            out = net(xb)
            loss = (out - Yn[j]).pow(2).mean()
            if use_d:
                gr, = torch.autograd.grad(out.sum(), xb, create_graph=True)
                loss = (loss + lam * ((gr - Dn[j]).pow(2) * wd).mean()) / (1 + lam)
            opt.zero_grad()
            loss.backward()
            opt.step()
        sched.step()

    def predict(Xq):
        xq = torch.tensor((Xq - mx) / sx, dtype=torch.float32, requires_grad=True)
        out = net(xq)
        gr, = torch.autograd.grad(out.sum(), xq)
        return (out.detach().numpy()[:, 0] * sy + my, gr.numpy() * sy / sx)
    return predict


# ---------------------------------------------------------------------------
# The deep BSDE method (Han, Jentzen and E 2018): pricing with default risk in 100 dimensions
# ---------------------------------------------------------------------------
DEFAULT_RISK = {"d": 100, "T": 1.0, "N": 40, "delta": 2 / 3, "R": 0.02, "mu": 0.02, "sigma": 0.2, "vh": 50.0,
                "vl": 70.0, "gh": 0.2, "gl": 0.02, "x0": 100.0, "reference": 57.300, "no_default": 60.781}


def deep_bsde(p=DEFAULT_RISK, iters=4000, batch=64, lr=0.008, seed=0, log_every=50, log=None):
    """Han-Jentzen-E's solver for u_t + mu x.grad u + sigma^2/2 sum x_i^2 u_ii - (1 - delta) Q(u) u - R u = 0,
    u(T, x) = min_i x_i: u(0, x0) and its gradient are trainable numbers, each later Z_n = sigma^T grad u(t_n, X_n) is
    a small network (d -> d+10 -> d+10 -> d, batch-normalized), and the loss is the terminal mismatch
    E|Y_N - g(X_N)|^2 along the BSDE's Euler scheme. Returns the curve of u(0, x0) by iteration."""
    import torch
    import torch.nn as nn

    torch.manual_seed(seed)
    d, T, N = p["d"], p["T"], p["N"]
    dt = T / N
    y0 = nn.Parameter(torch.tensor(float(np.random.default_rng(seed).uniform(40, 70))))
    z0 = nn.Parameter(torch.zeros(d).uniform_(-0.1, 0.1))

    def sub():
        return nn.Sequential(nn.BatchNorm1d(d), nn.Linear(d, d + 10, bias=False), nn.BatchNorm1d(d + 10), nn.ReLU(),
                             nn.Linear(d + 10, d + 10, bias=False), nn.BatchNorm1d(d + 10), nn.ReLU(),
                             nn.Linear(d + 10, d), nn.BatchNorm1d(d))
    nets = nn.ModuleList([sub() for _ in range(N - 1)])
    opt = torch.optim.Adam([y0, z0, *nets.parameters()], lr=lr)

    def Q(y):
        slope = (p["gh"] - p["gl"]) / (p["vh"] - p["vl"])
        return torch.clamp(slope * (y - p["vh"]) + p["gh"], min=p["gl"], max=p["gh"])

    def run(n):
        dW = math.sqrt(dt) * torch.randn(n, N, d)
        logx = math.log(p["x0"]) + torch.cumsum((p["mu"] - 0.5 * p["sigma"] ** 2) * dt + p["sigma"] * dW, 1)
        X = torch.cat([torch.full((n, 1, d), p["x0"]), torch.exp(logx)], 1)
        Y = y0.expand(n)
        Z = z0.expand(n, d)
        for k in range(N):
            if k > 0:
                Z = nets[k - 1](X[:, k] / p["x0"] - 1) * p["x0"] * p["sigma"] / 10
            Y = Y + ((1 - p["delta"]) * Q(Y) * Y + p["R"] * Y) * dt + (Z * dW[:, k]).sum(1)
        return Y, X[:, -1].min(1).values

    curve = []
    for it in range(iters + 1):
        nets.train()
        Y, g = run(batch)
        loss = (Y - g).pow(2).mean()
        if it % log_every == 0:
            curve.append({"iter": it, "u0": float(y0.detach()), "loss": float(loss.detach())})
            if log:
                log(curve[-1])
        if it == iters:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
    return {"u0": float(y0.detach()), "curve": curve}


def no_default_price(p=DEFAULT_RISK, n=400000, seed=0):
    """The linear case (no default): e^{-RT} E[min_i X_T^i] by Monte Carlo (mu = R, so this is the risk-neutral
    price), with its standard error."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n // 20000):
        z = rng.standard_normal((20000, p["d"]))
        XT = p["x0"] * np.exp((p["mu"] - 0.5 * p["sigma"] ** 2) * p["T"] + p["sigma"] * math.sqrt(p["T"]) * z)
        out.append(XT.min(1))
    v = np.exp(-p["R"] * p["T"]) * np.concatenate(out)
    return float(v.mean()), float(v.std() / math.sqrt(len(v)))


# ---------------------------------------------------------------------------
# Deep optimal stopping (Becker, Cheridito and Jentzen 2019): a Bermudan max-call
# ---------------------------------------------------------------------------
MAX_CALL = {"d": 5, "s0": 100.0, "K": 100.0, "r": 0.05, "div": 0.10, "sigma": 0.2, "T": 3.0, "N": 9,
            "paper": {"lower": 26.156, "upper": 26.162, "ci": [26.138, 26.174]}}


def max_call_paths(p, n, gen):
    import torch

    dt = p["T"] / p["N"]
    z = torch.randn(n, p["N"], p["d"], generator=gen)
    inc = (p["r"] - p["div"] - 0.5 * p["sigma"] ** 2) * dt + p["sigma"] * math.sqrt(dt) * z
    logS = math.log(p["s0"]) + torch.cat([torch.zeros(n, 1, p["d"]), torch.cumsum(inc, 1)], 1)
    S = torch.exp(logS)
    t = torch.arange(p["N"] + 1) * dt
    g = torch.exp(-p["r"] * t)[None] * torch.clamp(S.max(2).values - p["K"], min=0.0)
    return S, g


def deep_stopping(p=MAX_CALL, steps=600, batch=8192, lr=1e-3, n_eval=1_000_000, seed=0, log=None):
    """One network per exercise date n = N-1..1 decides 'stop' from (S_n, g_n) (Becker et al.: two hidden layers of
    d + 40, batch norm), trained backwards: date n's network maximizes E[g_n F + G_{n+1} (1 - F)], with G_{n+1}
    the payoff of the already-trained later rule. The hard rule's average payoff on fresh paths is a lower bound."""
    import torch
    import torch.nn as nn

    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed + 1)
    d, N = p["d"], p["N"]

    def net():
        return nn.Sequential(nn.BatchNorm1d(d + 1), nn.Linear(d + 1, d + 40), nn.BatchNorm1d(d + 40), nn.ReLU(),
                             nn.Linear(d + 40, d + 40), nn.BatchNorm1d(d + 40), nn.ReLU(), nn.Linear(d + 40, 1))
    nets = {}

    def feats(S, g, n):
        return torch.cat([S[:, n] / p["s0"], g[:, n:n + 1] / p["s0"]], 1)

    def future_value(S, g, n_from):
        """Payoff of the trained rule from date n_from on (stopping at N if never before)."""
        G = g[:, N].clone()
        for m in range(N - 1, n_from - 1, -1):
            nets[m].eval()
            with torch.no_grad():
                stop = nets[m](feats(S, g, m))[:, 0] > 0
            G = torch.where(stop, g[:, m], G)
        return G

    curves = {}
    for n in range(N - 1, 0, -1):
        nets[n] = net()
        opt = torch.optim.Adam(nets[n].parameters(), lr=lr)
        curves[n] = []
        for it in range(steps):
            S, g = max_call_paths(p, batch, gen)
            G = future_value(S, g, n + 1) if n < N - 1 else g[:, N]
            nets[n].train()
            F = torch.sigmoid(nets[n](feats(S, g, n))[:, 0])
            loss = -(g[:, n] * F + G * (1 - F)).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            if it % 50 == 0:
                curves[n].append(-float(loss.detach()))
        if log:
            log(n, curves[n][-1])
    vals = []
    for _ in range(n_eval // 100000):
        S, g = max_call_paths(p, 100000, gen)
        vals.append(future_value(S, g, 1))
    v = torch.cat(vals)
    # the exercise boundary in two dimensions of a 2-asset slice, for the picture
    return {"lower": float(v.mean()), "se": float(v.std() / math.sqrt(len(v))), "curves": curves, "nets": nets}


# ---------------------------------------------------------------------------
# Robust bounds from a neural SDE (Gierjatowicz, Sabate-Vidales, Siska, Szpruch and Zuric 2022)
# ---------------------------------------------------------------------------
class NeuralSV:
    """dX = -sigma^2/2 dt + sigma dW1 (X = log S), dV = b dt + eta dW2, corr(W1, W2) = rho, V_0 = 0; sigma(t, X, V),
    b(t, V), eta(t, V) small networks and rho a number. Euler steps; differentiable end to end."""

    def __init__(self, seed=0, width=32):
        import torch
        import torch.nn as nn

        torch.manual_seed(seed)
        self.sig = _mlp(3, width, 2)
        self.drift = _mlp(2, width, 2)
        self.vol = _mlp(2, width, 2)
        self.rho = nn.Parameter(torch.tensor(-0.5))
        with torch.no_grad():
            self.sig[-1].bias.fill_(-1.5)

    def parameters(self):
        return [*self.sig.parameters(), *self.drift.parameters(), *self.vol.parameters(), self.rho]

    def state_dict(self):
        return {k: [p.detach().clone() for p in v] for k, v in
                (("sig", self.sig.parameters()), ("drift", self.drift.parameters()), ("vol", self.vol.parameters()),
                 ("rho", [self.rho]))}

    def load(self, sd):
        import torch

        with torch.no_grad():
            for name, mods in (("sig", self.sig.parameters()), ("drift", self.drift.parameters()),
                               ("vol", self.vol.parameters()), ("rho", [self.rho])):
                for p_, q in zip(mods, sd[name]):
                    p_.copy_(q)

    def paths(self, n, T=1.0, steps=50, gen=None, antithetic=True):
        import torch
        import torch.nn.functional as F

        dt = T / steps
        m = n // 2 if antithetic else n
        Z = torch.randn(m, steps, 2, generator=gen)
        if antithetic:
            Z = torch.cat([Z, -Z], 0)
        rho = torch.tanh(self.rho)
        X = torch.zeros(n)
        V = torch.zeros(n)
        out = [X]
        for k in range(steps):
            t = torch.full((n,), k * dt)
            s = F.softplus(self.sig(torch.stack([t, X, V], 1))[:, 0]) + 0.02
            b = self.drift(torch.stack([t, V], 1))[:, 0]
            e = F.softplus(self.vol(torch.stack([t, V], 1))[:, 0])
            w1 = Z[:, k, 0]
            w2 = rho * w1 + torch.sqrt(1 - rho ** 2) * Z[:, k, 1]
            X = X - 0.5 * s ** 2 * dt + s * math.sqrt(dt) * w1
            V = V + b * dt + e * math.sqrt(dt) * w2
            out.append(X)
        return torch.stack(out, 1)


def nsde_prices(S, mats, strikes, steps, T):
    """Call prices from log-paths S = log(S_t/S_0) (n, steps+1) at maturities and strikes (S_0 = 1, zero rates), with
    the martingale correction E[S_T] = 1 imposed (a control variate)."""
    import torch

    out = []
    for Tm in mats:
        i = int(round(Tm / T * steps))
        x = torch.exp(S[:, i])
        x = x / x.mean()
        out.append(torch.stack([torch.clamp(x - k, min=0).mean() for k in strikes]))
    return torch.stack(out)


def down_out_call(S, K=1.0, H=0.8):
    import torch

    x = torch.exp(S)
    alive = (x.min(1).values > H).float()
    return (alive * torch.clamp(x[:, -1] - K, min=0)).mean()


# ---------------------------------------------------------------------------
# Path signatures and market generators
# ---------------------------------------------------------------------------
def signature(path, depth=4):
    """Truncated signature of piecewise-linear paths (batch, length, channels), by Chen's identity: the signature of
    a straight segment with increment D is the tensor exponential (1, D, D^2/2, ...), and segments multiply.
    Returns the levels 1..depth flattened and concatenated (batch, sum c^k)."""
    import torch

    B, L, c = path.shape
    inc = path[:, 1:] - path[:, :-1]
    levels = [torch.zeros(B, *(c,) * k) for k in range(1, depth + 1)]
    for j in range(L - 1):
        D = inc[:, j]
        seg = [D]
        for k in range(2, depth + 1):
            seg.append(torch.einsum("b...,bi->b...i", seg[-1], D) / k)
        new = []
        for k in range(1, depth + 1):
            acc = levels[k - 1] + seg[k - 1]
            for i in range(1, k):
                a, b_ = levels[i - 1], seg[k - i - 1]
                acc = acc + (a.reshape(B, -1, 1) * b_.reshape(B, 1, -1)).reshape(acc.shape)
            new.append(acc)
        levels = new
    return torch.cat([lv.reshape(B, -1) for lv in levels], 1)


def window_path(r, lead_lag=True):
    """The path a signature reads from a window of returns (batch, L): time, cumulative return and the running sum of
    squared returns, scaled so each ends near 1 for standardized returns. With ``lead_lag`` the cumulative return also
    appears with a one-step lag (the lead-lag transform: its level-2 terms are the quadratic variation and the lag
    structure, which the expected signature otherwise barely sees)."""
    import torch

    B, L = r.shape
    t = torch.linspace(0, 1, L + 1).expand(B, L + 1)
    x = torch.cat([torch.zeros(B, 1), torch.cumsum(r, 1)], 1) / math.sqrt(L)
    q = torch.cat([torch.zeros(B, 1), torch.cumsum(r ** 2, 1)], 1) / L
    if not lead_lag:
        return torch.stack([t, x, q], 2)
    # lead-lag: 2L + 1 points; the lead moves first, then the lag catches up
    lead = torch.repeat_interleave(x, 2, 1)[:, 1:]
    lag = torch.repeat_interleave(x, 2, 1)[:, :-1]
    tt = torch.repeat_interleave(t, 2, 1)[:, 1:]
    qq = torch.repeat_interleave(q, 2, 1)[:, 1:]
    return torch.stack([tt, lead, lag, qq], 2)


def sig_mmd(a, b, depth=4):
    """Distance between two sets of return windows: the norm of the difference of their expected signatures (each
    level scaled by k!, so the levels weigh alike)."""
    import torch

    sa, sb = signature(window_path(a), depth), signature(window_path(b), depth)
    return float(torch.linalg.norm(sa.mean(0) - sb.mean(0)))


class LSTMGenerator:
    """Noise -> a window of returns, built like Quant GANs' (Wiese et al. 2020) volatility-times-noise output: an LSTM
    cell reads the previous return and shock (plus fresh latent noise) and outputs a volatility sigma_t and a small
    drift mu_t; the return is r_t = mu_t + sigma_t z_t with z_t a fresh normal. Volatility clustering, leverage and
    fat tails must be learned; spurious autocorrelation cannot arise. Trained by matching expected signatures (Ni et
    al. 2021's Sig-Wasserstein idea with a linear signature kernel)."""

    def __init__(self, L=32, hidden=48, noise=3, seed=0):
        import torch
        import torch.nn as nn

        torch.manual_seed(seed)
        self.L, self.noise, self.hidden = L, noise, hidden
        self.cell = nn.LSTMCell(noise + 2, hidden)
        self.head = nn.Linear(hidden, 2)
        self.h0 = nn.Linear(noise, 2 * hidden)  # a random starting state: windows begin in calm or stormy regimes

    def parameters(self):
        return [*self.cell.parameters(), *self.head.parameters(), *self.h0.parameters()]

    def sample(self, n, gen=None):
        import torch
        import torch.nn.functional as F

        u = torch.randn(n, self.L + 1, self.noise, generator=gen)
        z = torch.randn(n, self.L, generator=gen)
        hc = torch.tanh(self.h0(u[:, 0]))
        h, c = hc[:, :self.hidden], hc[:, self.hidden:]
        r_prev = torch.zeros(n)
        z_prev = torch.zeros(n)
        out = []
        for t in range(self.L):
            h, c = self.cell(torch.cat([u[:, t + 1], r_prev[:, None], z_prev[:, None]], 1), (h, c))
            o = self.head(h)
            sig = F.softplus(o[:, 0]) + 1e-3
            r = 0.1 * o[:, 1] + sig * z[:, t]
            out.append(r)
            r_prev, z_prev = r, z[:, t]
        return torch.stack(out, 1)


def train_sig_generator(real, L=32, iters=1500, batch=512, lr=2e-3, depth=4, seed=0, log=None):
    """``real``: (n, L) standardized return windows."""
    import torch

    g = LSTMGenerator(L, seed=seed)
    target = signature(window_path(torch.tensor(real, dtype=torch.float32)), depth).mean(0)
    opt = torch.optim.Adam(g.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, iters)
    gen = torch.Generator().manual_seed(seed + 1)
    curve = []
    for it in range(iters):
        s = signature(window_path(g.sample(batch, gen)), depth).mean(0)
        loss = (s - target).pow(2).sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        curve.append(float(loss.detach()))
        if log and it % 100 == 0:
            log(it, curve[-1])
    return g, curve


def train_ddpm(real, steps=200, iters=4000, batch=256, lr=1e-3, width=256, seed=0, log=None):
    """A small denoising diffusion model (Ho, Jain and Abbeel 2020) on return windows: an MLP predicts the noise added
    at step t of a linear-beta forward process. Returns a sampler."""
    import torch

    torch.manual_seed(seed)
    X = torch.tensor(real, dtype=torch.float32)
    L = X.shape[1]
    betas = torch.linspace(1e-4, 0.02, steps)
    alpha = 1 - betas
    abar = torch.cumprod(alpha, 0)
    net = _mlp(L + 16, width, 3, L)

    def temb(t):
        f = torch.exp(-math.log(1000) * torch.arange(8) / 8)
        a = t[:, None].float() * f[None]
        return torch.cat([torch.sin(a), torch.cos(a)], 1)

    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, iters)
    g = torch.Generator().manual_seed(seed + 1)
    curve = []
    for it in range(iters):
        x0 = X[torch.randint(len(X), (batch,), generator=g)]
        t = torch.randint(steps, (batch,), generator=g)
        eps = torch.randn(x0.shape, generator=g)
        xt = abar[t].sqrt()[:, None] * x0 + (1 - abar[t]).sqrt()[:, None] * eps
        loss = (net(torch.cat([xt, temb(t)], 1)) - eps).pow(2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        curve.append(float(loss.detach()))
        if log and it % 500 == 0:
            log(it, curve[-1])

    @torch.no_grad()
    def sample(n, seed=0):
        gg = torch.Generator().manual_seed(seed)
        x = torch.randn(n, L, generator=gg)
        for t in range(steps - 1, -1, -1):
            tt = torch.full((n,), t)
            e = net(torch.cat([x, temb(tt)], 1))
            x = (x - betas[t] / (1 - abar[t]).sqrt() * e) / alpha[t].sqrt()
            if t > 0:
                x = x + betas[t].sqrt() * torch.randn(x.shape, generator=gg)
        return x.numpy()
    return sample, curve


def stylized_facts(W):
    """Facts of Part 1 measured inside return windows W (n, L), pooled: excess kurtosis; the autocorrelation of |r|
    at lags 1-5 (volatility clustering); the leverage correlation corr(r_t, r_{t+1..5}^2); the autocorrelation of r
    at lag 1."""
    W = np.asarray(W, float)
    r = W.ravel()
    z = (r - r.mean()) / r.std()
    kurt = float(np.mean(z ** 4) - 3)

    def pooled_corr(a, b):
        a = a - a.mean()
        b = b - b.mean()
        return float((a * b).sum() / np.sqrt((a ** 2).sum() * (b ** 2).sum()))
    A = np.abs(W)
    acf_abs = [pooled_corr(A[:, :-k].ravel(), A[:, k:].ravel()) for k in range(1, 6)]
    lev = float(np.mean([pooled_corr(W[:, :-k].ravel(), (W[:, k:] ** 2).ravel()) for k in range(1, 6)]))
    ac1 = pooled_corr(W[:, :-1].ravel(), W[:, 1:].ravel())
    return {"kurtosis": kurt, "acf_abs": acf_abs, "acf_abs_mean": float(np.mean(acf_abs)), "leverage": lev, "acf1": ac1}
