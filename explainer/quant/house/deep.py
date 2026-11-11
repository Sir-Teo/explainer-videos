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

    def __init__(self, kind="mlp", width=32, depth=3, seed=0, sigma=0.2, T=30 / 365):
        import torch

        torch.manual_seed(seed)
        self.kind = kind
        self.sigma, self.T = sigma, T
        self.net = _mlp(3 if kind == "mlp" else 2, width, depth, 1 if kind == "mlp" else 2)
        if kind == "band":  # start from a narrow band around delta
            with torch.no_grad():
                self.net[-1].bias.fill_(-3.0)

    def parameters(self):
        return self.net.parameters()

    def __call__(self, x, tau, prev):
        import torch

        if self.kind == "mlp":
            # log-moneyness in units of the option's total volatility, so its inputs are all of order one
            z = x / (self.sigma * math.sqrt(self.T))
            return self.net(torch.stack([z, tau, prev], -1)).squeeze(-1)
        lo, hi = self.band(x, tau)
        return torch.minimum(torch.maximum(prev, lo), hi)

    def band(self, x, tau):
        """Imaki et al.'s no-transaction band: [delta - softplus(a), delta + softplus(b)], with delta the
        Black-Scholes hedge ratio and (a, b) the network's outputs; the hedge only moves to the nearest edge."""
        import torch
        import torch.nn.functional as F

        t = torch.clamp(tau * self.T, min=1e-6)
        d1 = (x + 0.5 * self.sigma ** 2 * t) / (self.sigma * torch.sqrt(t))
        delta = 0.5 * (1 + torch.erf(d1 / math.sqrt(2)))
        o = self.net(torch.stack([x, tau], -1))
        return delta - F.softplus(o[..., 0]), delta + F.softplus(o[..., 1])


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
    pol = Hedger(kind, seed=seed, sigma=sigma, T=T)
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
        rho = 0.95 * torch.tanh(self.rho)  # kept off +-1, where sqrt(1 - rho^2) has an infinite slope
        X = torch.zeros(n)
        V = torch.zeros(n)
        out = [X]
        for k in range(steps):
            t = torch.full((n,), k * dt)
            s = torch.clamp(F.softplus(self.sig(torch.stack([t, X, V], 1))[:, 0]) + 0.02, max=3.0)
            b = self.drift(torch.stack([t, V], 1))[:, 0]
            e = F.softplus(self.vol(torch.stack([t, V], 1))[:, 0])
            w1 = Z[:, k, 0]
            w2 = rho * w1 + torch.sqrt(1 - rho ** 2) * Z[:, k, 1]
            X = X - 0.5 * s ** 2 * dt + s * math.sqrt(dt) * w1
            V = torch.clamp(V + b * dt + e * math.sqrt(dt) * w2, -6.0, 6.0)
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
    """Distance between two sets of return windows: the norm of the difference of their expected signatures, all
    levels 1..depth concatenated unscaled (level k already carries the tensor exponential's 1/k!): a linear-kernel
    MMD between the two laws."""
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


# ---------------------------------------------------------------------------
# A neural SDE market generator (Part 5's frontier chapter)
# ---------------------------------------------------------------------------
class NeuralSDE:
    """A two-dimensional latent SDE dY = mu(t, Y) dt + sigma(t, Y) dW (drift and diagonal diffusion small MLPs of width
    ``width``, a random starting state), solved by Euler on ``L`` steps; the window's returns are the increments of
    Y's first coordinate.  Trained, like :func:`train_sig_generator`, by matching expected signatures: the linear-kernel
    cousin of the signature-kernel scores of Issa, Horvath, Lemercier and Salvi (2023)."""

    def __init__(self, L=32, width=32, dim=2, seed=0):
        import torch

        torch.manual_seed(seed)
        self.L, self.dim = L, dim
        self.drift = _mlp(dim + 1, width, 2, dim, act=torch.nn.Tanh)
        self.diff = _mlp(dim + 1, width, 2, dim, act=torch.nn.Tanh)
        self.y0 = torch.nn.Linear(dim, dim)

    def parameters(self):
        return [*self.drift.parameters(), *self.diff.parameters(), *self.y0.parameters()]

    def sample(self, n, gen=None):
        import torch
        import torch.nn.functional as F

        dt = 1.0 / self.L
        y = self.y0(torch.randn(n, self.dim, generator=gen))
        out = []
        for k in range(self.L):
            ty = torch.cat([torch.full((n, 1), k * dt), y], 1)
            dw = torch.randn(n, self.dim, generator=gen) * math.sqrt(dt)
            y_new = y + self.drift(ty) * dt + F.softplus(self.diff(ty)) * dw
            out.append((y_new[:, 0] - y[:, 0]) * math.sqrt(self.L))  # standardized returns
            y = y_new
        return torch.stack(out, 1)


def train_nsde(real, L=32, iters=1200, batch=256, lr=3e-3, depth=4, seed=0, every=100, n_show=24, log=None):
    """Train :class:`NeuralSDE` on standardized return windows ``real`` (n, L).  Returns the model, the loss curve and
    a fan of generated windows (cumulated) every ``every`` steps, from a fixed noise seed, for the replay."""
    import torch

    torch.manual_seed(seed)
    m = NeuralSDE(L, seed=seed)
    target = signature(window_path(torch.tensor(real, dtype=torch.float32)), depth).mean(0)
    opt = torch.optim.Adam(m.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, iters)
    gen = torch.Generator().manual_seed(seed + 1)
    curve, fans = [], {}
    for it in range(iters + 1):
        if it % every == 0:
            with torch.no_grad():
                fans[it] = m.sample(n_show, torch.Generator().manual_seed(123)).cumsum(1).numpy()
        if it == iters:
            break
        s = signature(window_path(m.sample(batch, gen)), depth).mean(0)
        loss = (s - target).pow(2).sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        curve.append(float(loss.detach()))
        if log and it % every == 0:
            log(it, curve[-1])
    return m, curve, fans


# ---------------------------------------------------------------------------
# Part 9: a neural dual for martingale optimal transport (Eckstein and Kupper's penalty; Neufeld and Sester 2023)
# ---------------------------------------------------------------------------
def mot_neural(x, mu, y, nu, cost, steps=3000, gamma=2000.0, width=32, lr=3e-3, seed=0, log_every=25,
               snapshots=(), grid=None):
    """A neural penalty approximation to the upper MOT dual: u, v and h are small networks, and the constraint
    u(x) + v(y) + h(x)(y - x) >= c(x, y) is enforced by a penalty (gamma / 2) E_{mu x nu}[(c - u - v - h (y - x))_+^2].
    Full batch over the grid (x_i, y_j) with weights mu_i nu_j. Returns the trace of the raw dual cost
    E_mu[u] + E_nu[v], the penalized loss and the weighted mean positive shortfall (not the largest violation).
    The legacy ``bound`` field stores raw cost, which is not a certified upper bound unless hedge dominance is
    established. The ``violation`` field is the final weighted mean shortfall. At ``snapshots`` it returns the hedge on
    ``grid`` (u(x) + v(y) + h(x)(y - x) on a (len(grid[0]), len(grid[1])) mesh)."""
    import torch

    torch.manual_seed(seed)
    f = lambda a: torch.tensor(np.asarray(a, float), dtype=torch.float64)  # noqa: E731
    X, MU, Y, NU = f(x), f(mu), f(y), f(nu)
    C = f([[cost(a, b) for b in y] for a in x])
    W = MU[:, None] * NU[None, :]
    nets = [_mlp(1, width, 2).double() for _ in range(3)]
    opt = torch.optim.Adam([p for n in nets for p in n.parameters()], lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)

    def hedge(xs, ys):
        u = nets[0](xs[:, None] - 1).squeeze(-1)
        v = nets[1](ys[:, None] - 1).squeeze(-1)
        h = nets[2](xs[:, None] - 1).squeeze(-1)
        return u, v, h, u[:, None] + v[None, :] + h[:, None] * (ys[None, :] - xs[:, None])

    trace, snaps = [], {}
    for it in range(steps + 1):
        u, v, h, H = hedge(X, Y)
        dual = (u * MU).sum() + (v * NU).sum()
        gap = torch.relu(C - H)
        loss = dual + 0.5 * gamma * (W * gap ** 2).sum()
        if it % log_every == 0 or it == steps:
            trace.append((it, float(dual.detach()), float(loss.detach()), float((W * gap).sum().detach())))
        if it in snapshots and grid is not None:
            with torch.no_grad():
                snaps[it] = hedge(f(grid[0]), f(grid[1]))[3].numpy()
        if it == steps:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    return {"trace": np.array(trace), "snapshots": snaps, "bound": trace[-1][1], "violation": trace[-1][3]}


# ---------------------------------------------------------------------------
# Part 12: an implied-volatility surface learned without arbitrage (Ackerer, Tagasovska and Vatter 2020)
# ---------------------------------------------------------------------------
def surface_net_g(net, kk, TT):
    """Total variance w(k, T) of a surface network and its no-arbitrage quantities by autodiff: Gatheral's g(k) and
    dw/dT (both must be >= 0)."""
    import torch

    kk = kk.clone().requires_grad_(True)
    TT = TT.clone().requires_grad_(True)
    w = net(kk, TT)
    dk, dT = torch.autograd.grad(w.sum(), [kk, TT], create_graph=True)
    d2k = torch.autograd.grad(dk.sum(), kk, create_graph=True)[0]
    g = (1 - kk * dk / (2 * w)) ** 2 - dk ** 2 / 4 * (1 / w + 0.25) + d2k / 2
    return w, g, dT


def train_surface_net(k, T, iv, penalty=1.0, seed=0, steps=3000, every=100, train=None, width=40, lr=3e-3,
                      grid=None, colloc=(41, 30), k_range=(-1.0, 1.0), T_range=(3 / 365, 0.8), log=None) -> dict:
    """Fit implied volatilities (k, T, iv) with a small network for total variance, w(k, T) = T softplus(net(k,
    sqrt T) + c) (c puts the start near 50% vol), by Adam on the squared vol error of the ``train`` quotes plus
    ``penalty`` times the mean violations relu(-g) + relu(-dw/dT) on a collocation grid (``colloc`` = (n_k, n_T)).
    Every ``every`` steps it records the train and held-out vol RMSE (vol points), the penalty, the share of
    collocation points with g < 0, and the vol surface on ``grid`` = (k values, T values). Returns those histories, the
    final RMSEs, and the violation shares on a fine 201 x 60 grid."""
    import torch

    torch.manual_seed(seed)
    k, T, iv = (np.asarray(a, float) for a in (k, T, iv))
    tr = np.ones(len(k), bool) if train is None else np.asarray(train, bool)
    te = ~tr
    f32 = lambda a: torch.tensor(np.asarray(a, float), dtype=torch.float32)  # noqa: E731
    mlp = _mlp(2, width, 2, act=torch.nn.Tanh)
    c0 = float(np.log(np.exp(0.25) - 1))

    def net(kk, TT):
        return TT * torch.nn.functional.softplus(mlp(torch.stack([kk, torch.sqrt(TT)], 1))[:, 0] + c0)

    kt, Tt, ivt = f32(k), f32(T), f32(iv)
    kc = torch.linspace(*k_range, colloc[0]).repeat(colloc[1])
    Tc = torch.linspace(*T_range, colloc[1]).repeat_interleave(colloc[0])
    if grid is not None:
        gk, gT = (np.asarray(a, float) for a in grid)
        GK, GT = f32(np.tile(gk, len(gT))), f32(np.repeat(gT, len(gk)))
    opt = torch.optim.Adam(mlp.parameters(), lr=lr)
    hist = {"step": [], "train": [], "test": [], "pen": [], "g_neg": [], "surf": [], "g_flags": []}
    t0 = time.time()
    for it in range(steps + 1):
        w, g, dT = surface_net_g(net, kc, Tc)
        pen = torch.relu(-g).mean() + torch.relu(-dT).mean()
        pred = torch.sqrt(net(kt, Tt) / Tt)
        err = (pred - ivt) ** 2
        fit = err[torch.tensor(tr)].mean()
        loss = fit + penalty * pen
        if it % every == 0 or it == steps:
            with torch.no_grad():
                hist["step"].append(it)
                hist["train"].append(float(fit.sqrt()) * 100)
                hist["test"].append(float(err[torch.tensor(te)].mean().sqrt()) * 100 if te.any() else float("nan"))
                hist["pen"].append(float(pen))
                hist["g_neg"].append(float((g < 0).float().mean()))
                hist["g_flags"].append((g < 0).numpy().astype(int))
                if grid is not None:
                    hist["surf"].append(torch.sqrt(net(GK, GT) / GT).numpy().reshape(len(gT), len(gk)))
            if log:
                log(f"  surface net seed {seed} step {it}: train {hist['train'][-1]:.2f} test {hist['test'][-1]:.2f} "
                    f"pen {hist['pen'][-1]:.2e} ({time.time() - t0:.0f}s)")
        if it == steps:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
    kf = torch.linspace(*k_range, 201).repeat(60)
    Tf = torch.linspace(*T_range, 60).repeat_interleave(201)
    _, g, dT = surface_net_g(net, kf, Tf)
    with torch.no_grad():
        pred = torch.sqrt(net(kt, Tt) / Tt).numpy()
    return {**{k_: np.array(v) for k_, v in hist.items()}, "pred": pred,
            "train_rmse": float(np.sqrt(np.mean((pred[tr] - iv[tr]) ** 2)) * 100),
            "test_rmse": float(np.sqrt(np.mean((pred[te] - iv[te]) ** 2)) * 100) if te.any() else float("nan"),
            "g_viol": float((g < 0).float().mean()), "cal_viol": float((dT < 0).float().mean()),
            "net": net, "secs": time.time() - t0}


# ---------------------------------------------------------------------------
# Part 17's hands-on layer: the same trainings with their curves and checkpoints, new objectives (CVaR in
# Rockafellar-Uryasev form, a drifted simulator), and the classical twins (Leland, a Gaussian process with gradients)
# ---------------------------------------------------------------------------
def train_mlp_trace(X, y, width=32, depth=2, epochs=200, lr=3e-3, batch=1024, seed=0, act=None, every=5,
                    snap_every=0, snap_fn=None, ckpt=None, ckpt_every=10):
    """:func:`train_mlp_regressor` with its training curve (the epoch's mean squared error, every ``every`` epochs)
    and snapshots ``snap_fn(net)`` at epoch 0 and every ``snap_every`` epochs; ``act`` picks the activation (a
    torch.nn class; SiLU by default, which reproduces train_mlp_regressor draw for draw). With ``ckpt`` (a path) the
    whole state is saved every ``ckpt_every`` epochs and a stopped run resumes from it. Returns (net, curve, snaps)
    with curve a list of (epoch, mse)."""
    import os

    import torch

    torch.manual_seed(seed)
    net = _mlp(X.shape[1], width, depth, y.shape[1] if y.ndim > 1 else 1, act=act)
    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.float32).reshape(len(X), -1)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
    g = torch.Generator().manual_seed(seed)
    curve, snaps, ep0 = [], {}, 0
    if ckpt is not None and os.path.exists(ckpt):
        st = torch.load(ckpt, weights_only=False)
        net.load_state_dict(st["net"])
        opt.load_state_dict(st["opt"])
        sched.load_state_dict(st["sched"])
        g.set_state(st["gen"])
        curve, snaps, ep0 = st["curve"], st["snaps"], st["epoch"]
    if snap_fn is not None and snap_every and 0 not in snaps:
        snaps[0] = snap_fn(net)
    for ep in range(ep0, epochs):
        perm = torch.randperm(len(X), generator=g)
        tot = 0.0
        for i in range(0, len(X), batch):
            j = perm[i:i + batch]
            loss = (net(Xt[j]) - yt[j]).pow(2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            tot += float(loss.detach()) * len(j)
        sched.step()
        if ep == 0 or (ep + 1) % every == 0:
            curve.append((ep + 1, tot / len(X)))
        if snap_fn is not None and snap_every and (ep + 1) % snap_every == 0:
            snaps[ep + 1] = snap_fn(net)
        if ckpt is not None and ((ep + 1) % ckpt_every == 0 or ep + 1 == epochs):
            torch.save({"net": net.state_dict(), "opt": opt.state_dict(), "sched": sched.state_dict(),
                        "gen": g.get_state(), "curve": curve, "snaps": snaps, "epoch": ep + 1}, str(ckpt) + ".tmp")
            os.replace(str(ckpt) + ".tmp", ckpt)
    return net, curve, snaps


def train_differential_trace(X, Y, dY=None, lam=1.0, width=20, depth=4, epochs=None, lr=3e-3, seed=0, snap_at=(),
                             snap_fn=None, every=None):
    """:func:`train_differential` (the same draws, the same network) with its curve and checkpoints: the value
    term of the loss (normalized squared error, comparable with and without derivatives) every ``every`` epochs, and
    ``snap_fn(predict)`` at the epochs in ``snap_at``. Returns (predict, curve, snaps)."""
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
    every = every or max(1, epochs // 100)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
    batch = min(256, len(X))
    g = torch.Generator().manual_seed(seed)

    def predict(Xq):
        xq = torch.tensor((Xq - mx) / sx, dtype=torch.float32, requires_grad=True)
        out = net(xq)
        gr, = torch.autograd.grad(out.sum(), xq)
        return (out.detach().numpy()[:, 0] * sy + my, gr.numpy() * sy / sx)
    curve, snaps = [], {}
    if 0 in snap_at and snap_fn is not None:
        snaps[0] = snap_fn(predict)
    for ep in range(epochs):
        perm = torch.randperm(len(X), generator=g)
        tot = 0.0
        for i in range(0, len(X), batch):
            j = perm[i:i + batch]
            xb = Xn[j].requires_grad_(use_d)
            out = net(xb)
            loss = (out - Yn[j]).pow(2).mean()
            tot += float(loss.detach()) * len(j)
            if use_d:
                gr, = torch.autograd.grad(out.sum(), xb, create_graph=True)
                loss = (loss + lam * ((gr - Dn[j]).pow(2) * wd).mean()) / (1 + lam)
            opt.zero_grad()
            loss.backward()
            opt.step()
        sched.step()
        if ep == 0 or (ep + 1) % every == 0:
            curve.append((ep + 1, tot / len(X)))
        if (ep + 1) in snap_at and snap_fn is not None:
            snaps[ep + 1] = snap_fn(predict)
    return predict, curve, snaps


def gp_with_gradients(X, y, dY, Xq, ls=1.0, sf=1.0, noise_y=1e-6, noise_d=1e-6, grad=False):
    """A Gaussian process (squared-exponential kernel, length ``ls``, scale ``sf``, constant mean = mean(y)) observed
    at X (n, d) through values y *and* gradients dY (n, d): the classical twin of differential machine learning
    (Dixon, Halperin and Bilokon ch. 3). Covariances of derivatives are derivatives of the kernel, so all n (1 + d)
    observations enter one linear solve, O((n (1 + d))^3). Returns the posterior mean and sd of f at Xq (and the
    mean gradient if ``grad``)."""
    X, Xq = np.atleast_2d(np.asarray(X, float)), np.atleast_2d(np.asarray(Xq, float))
    n, d = X.shape
    m = float(np.mean(y))

    def blocks(A, B):
        D = A[:, None, :] - B[None, :, :]                       # a - b
        k = sf ** 2 * np.exp(-(D ** 2).sum(-1) / (2 * ls ** 2))
        top = [k] + [k * D[..., j] / ls ** 2 for j in range(d)]  # cov(f(a), d_j f(b))
        rows = [np.hstack(top)]
        for i in range(d):
            r = [-k * D[..., i] / ls ** 2]                       # cov(d_i f(a), f(b))
            for j in range(d):
                r.append(k * ((i == j) / ls ** 2 - D[..., i] * D[..., j] / ls ** 4))
            rows.append(np.hstack(r))
        return np.vstack(rows)
    K = blocks(X, X)
    K[np.diag_indices(n)] += noise_y
    idx = np.arange(n, n * (1 + d))
    K[idx, idx] += noise_d
    obs = np.concatenate([np.asarray(y, float) - m] + [np.asarray(dY, float)[:, j] for j in range(d)])
    L = np.linalg.cholesky(K)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, obs))
    Kq = blocks(Xq, X)
    nq = len(Xq)
    mean = m + Kq[:nq] @ alpha
    v = np.linalg.solve(L, Kq[:nq].T)
    sd = np.sqrt(np.maximum(sf ** 2 - (v ** 2).sum(0), 0.0))
    if grad:
        return mean, sd, (Kq[nq:] @ alpha).reshape(d, nq).T
    return mean, sd


def gbm_torch_mu(n, steps, T, sigma, mu=0.0, S0=100.0, gen=None):
    """:func:`gbm_torch` under a real-world drift ``mu`` a year: the same normal draws, so mu = 0 gives its paths."""
    import torch

    dt = T / steps
    z = torch.randn(n, steps, generator=gen)
    inc = (mu - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * z
    return S0 * torch.exp(torch.cat([torch.zeros(n, 1), torch.cumsum(inc, 1)], 1))


def cvar_ru(X, w, alpha=0.5):
    """Rockafellar and Uryasev's CVaR of the loss -X: w + E[(-X - w)^+] / alpha. Its minimum over the threshold w is
    CVaR_alpha, attained at w = VaR_alpha, so w can be trained alongside the hedge."""
    import torch

    return w + torch.clamp(-X - w, min=0.0).mean() / alpha


class WWBandHedger(Hedger):
    """Imaki et al.'s band network started at Whalley and Wilmott's band (the prior of Arzel and Lehdili 2026): the
    two outputs are added to softplus^-1 of WW's half-width and the last layer starts at zero, so at initialization
    the band *is* WW's, and training corrects it."""

    def __init__(self, cost, gamma=1.0, width=32, depth=3, seed=0, sigma=0.2, T=30 / 365, K=100.0):
        import torch

        super().__init__("band", width, depth, seed, sigma, T)
        self.cost, self.gamma, self.K = cost, gamma, K
        with torch.no_grad():
            self.net[-1].weight.zero_()
            self.net[-1].bias.zero_()

    def ww_half(self, x, tau):
        import torch

        t = torch.clamp(tau * self.T, min=1e-6)
        sq = self.sigma * torch.sqrt(t)
        d1 = (x + 0.5 * self.sigma ** 2 * t) / sq
        S = self.K * torch.exp(x)
        gam = torch.exp(-0.5 * d1 ** 2) / math.sqrt(2 * math.pi) / (S * sq)
        return torch.clamp((1.5 * self.cost * S * gam ** 2 / self.gamma) ** (1 / 3), 1e-3, 1.0)

    def band(self, x, tau):
        import torch
        import torch.nn.functional as F

        t = torch.clamp(tau * self.T, min=1e-6)
        d1 = (x + 0.5 * self.sigma ** 2 * t) / (self.sigma * torch.sqrt(t))
        delta = 0.5 * (1 + torch.erf(d1 / math.sqrt(2)))
        base = torch.log(torch.expm1(self.ww_half(x, tau)))
        o = self.net(torch.stack([x, tau], -1))
        return delta - F.softplus(o[..., 0] + base), delta + F.softplus(o[..., 1] + base)


def train_hedger_on(paths, pol, cost=0.0, T=30 / 365, K=100.0, gamma=1.0, risk="entropic", alpha=0.5, iters=1500,
                    lr=3e-3, seed=0, batch=8192, snap_at=(), snap_fn=None, log=None, ckpt=None, ckpt_every=100):
    """Train any policy ``pol`` on fresh paths ``paths(batch, gen)`` (n, steps + 1) each iteration: the deep hedger
    with its simulator made explicit (a drifted GBM, a GARCH fitted to history). ``risk``: 'entropic', 'cvar' (the
    mean of the worst alpha) or 'cvar_ru' (Rockafellar-Uryasev, the threshold w trained alongside, started at the
    first batch's VaR). With ``ckpt`` the state is saved every ``ckpt_every`` steps and a stopped run resumes.
    Returns (curve, snaps, w)."""
    import os

    import torch

    gen = torch.Generator().manual_seed(seed + 1)
    w = torch.zeros((), requires_grad=True) if risk == "cvar_ru" else None
    params = list(pol.parameters()) + ([w] if w is not None else [])
    opt = torch.optim.Adam(params, lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, iters)
    curve, snaps, it0 = [], {}, 0
    if ckpt is not None and os.path.exists(ckpt):
        st = torch.load(ckpt, weights_only=False)
        pol.net.load_state_dict(st["net"])
        opt.load_state_dict(st["opt"])
        sched.load_state_dict(st["sched"])
        gen.set_state(st["gen"])
        curve, snaps, it0 = st["curve"], st["snaps"], st["it"]
        if w is not None:
            with torch.no_grad():
                w.fill_(st["w"])
    for it in range(it0, iters + 1):
        if ckpt is not None and it > it0 and it % ckpt_every == 0:
            torch.save({"net": pol.net.state_dict(), "opt": opt.state_dict(), "sched": sched.state_dict(),
                        "gen": gen.get_state(), "curve": curve, "snaps": snaps, "it": it,
                        "w": float(w.detach()) if w is not None else None}, str(ckpt) + ".tmp")
            os.replace(str(ckpt) + ".tmp", ckpt)
        if it in snap_at and snap_fn is not None:
            with torch.no_grad():
                snaps[it] = snap_fn(pol)
        if it == iters:
            break
        S = paths(batch, gen)
        X, _, _ = hedge_pnl(pol, S, K, T, cost)
        if risk == "entropic":
            loss = entropic(X, gamma)
        elif risk == "cvar":
            loss = cvar(X, alpha)
        else:
            if it == 0:
                with torch.no_grad():
                    w.fill_(float(torch.quantile(-X, 1 - alpha)))
            loss = cvar_ru(X, w, alpha)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        curve.append(float(loss.detach()))
        if log and it % 100 == 0:
            log(it, curve[-1])
    return curve, snaps, (float(w.detach()) if w is not None else None)


def train_hedger_p(kind="mlp", mu=0.0, cost=0.0, sigma=0.2, T=30 / 365, steps=30, K=100.0, gamma=1.0,
                   risk="entropic", iters=1500, batch=8192, lr=3e-3, seed=0, snap_at=(), snap_fn=None, log=None,
                   ckpt=None):
    """:func:`train_hedger` on paths with a real-world drift ``mu`` (mu = 0 reproduces it): the drift trap. Returns
    (policy, curve, snaps)."""
    pol = Hedger(kind, seed=seed, sigma=sigma, T=T)
    curve, snaps, _ = train_hedger_on(lambda b, g: gbm_torch_mu(b, steps, T, sigma, mu, K, g), pol, cost, T, K, gamma,
                                      risk, 0.5, iters, lr, seed, batch, snap_at, snap_fn, log, ckpt)
    return pol, curve, snaps


def merton_hedge(S, sigma, mu, gamma=1.0):
    """The extra shares an exponential-utility hedger holds when the stock drifts: mu / (gamma sigma^2 S), Merton's
    fixed dollar amount mu / (gamma sigma^2) in shares (complete market, zero rates)."""
    return mu / (gamma * sigma ** 2 * np.asarray(S, float))


def leland_sigma(sigma, cost, dt):
    """Leland (1985): hedge a short option with Black-Scholes at the inflated volatility sigma sqrt(1 + Le),
    Le = sqrt(2/pi) k / (sigma sqrt(dt)), k = 2 cost the round-trip cost, rebalancing every dt."""
    return sigma * math.sqrt(1 + math.sqrt(2 / math.pi) * 2 * cost / (sigma * math.sqrt(dt)))


def garch_paths_torch(params, residuals, n, steps, scale=1.0, S0=100.0, h0=None, gen=None):
    """GJR-GARCH(1,1) paths (params = omega, alpha, gamma, beta, for standardized returns) with shocks bootstrapped
    from ``residuals``: e_t = sqrt(h_t) eps_t, h_{t+1} = omega + (alpha + gamma 1{e_t < 0}) e_t^2 + beta h_t. Prices
    S_{t+1} = S_t exp(scale e_t - scale^2 h_t / 2) (about a martingale); h0 defaults to the unconditional variance.
    Returns (S (n, steps + 1), e (n, steps)) as float32 tensors."""
    import torch

    w_, a_, g_, b_ = (float(v) for v in params)
    res = torch.as_tensor(np.asarray(residuals, float), dtype=torch.float32)
    hbar = w_ / max(1 - a_ - g_ / 2 - b_, 1e-6)
    h = torch.full((n,), hbar) if h0 is None else torch.as_tensor(h0, dtype=torch.float32).reshape(n)
    eps = res[torch.randint(len(res), (n, steps), generator=gen)]
    logS = torch.full((n,), math.log(S0))
    out, es = [torch.exp(logS)], []
    for t in range(steps):
        e = torch.sqrt(h) * eps[:, t]
        logS = logS + scale * e - 0.5 * scale ** 2 * h
        out.append(torch.exp(logS))
        es.append(e)
        h = w_ + (a_ + g_ * (e < 0).float()) * e ** 2 + b_ * h
    return torch.stack(out, 1), torch.stack(es, 1)


def calibrate_neural_trace(net, T, k, iv, w=None, starts=8, seed=0, iters=200, every=5):
    """:func:`calibrate_neural` (the same starts, the same steps) recording every start's iterates: the parameters
    and the weighted RMSE every ``every`` Adam steps, then after L-BFGS. Returns calibrate_neural's dict plus
    'traces' (one per start: steps, params, rmse) and 'best' (the winning start's index)."""
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
    best, traces = None, []
    for s in range(starts):
        u = torch.tensor(rng.uniform(-1.2, 1.2, 5), dtype=torch.float32, requires_grad=True)
        opt = torch.optim.Adam([u], lr=0.05)
        tr = {"step": [], "params": [], "rmse": []}
        for it in range(iters):
            f, th = model(u)
            loss = (w * (f - tgt).pow(2)).mean() * 1e4
            if it % every == 0:
                tr["step"].append(it)
                tr["params"].append(th.detach().numpy().astype(float).tolist())
                tr["rmse"].append(float(loss.detach().sqrt()))
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
        tr["step"].append(iters + 100)
        tr["params"].append(th.numpy().astype(float).tolist())
        tr["rmse"].append(r)
        traces.append(tr)
        if best is None or r < best[1]:
            best = (th.numpy().astype(float), r, f.numpy().astype(float), s)
    for p_ in net.parameters():
        p_.requires_grad_(True)
    return {"params": dict(zip(CALIB_NAMES, map(float, best[0]))), "x": best[0].tolist(), "rmse": best[1],
            "fit": best[2], "seconds": time.perf_counter() - t0, "traces": traces, "best": best[3]}


def train_calib_net_ckpt(X, y, epochs=40, batch=2048, lr=2e-3, seed=0, val=None, ckpt=None, snap_at=(), snap_fn=None,
                         log=None):
    """:func:`train_calib_net` that saves its state (network, optimizer, schedule, sampler, history, snapshots) to
    ``ckpt`` after every epoch and resumes from it, with snapshots ``snap_fn(net)`` after the epochs in
    ``snap_at``: a long training on a shared machine that survives being stopped."""
    import os

    import torch

    torch.manual_seed(seed)
    net = calib_net()
    Xt, yt = torch.from_numpy(X), torch.from_numpy(y.astype(np.float32)).reshape(-1, 1)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    steps = epochs * int(np.ceil(len(X) / batch))
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps)
    g = torch.Generator().manual_seed(seed)
    hist, snaps, ep0 = [], {}, 0
    if ckpt is not None and os.path.exists(ckpt):
        st = torch.load(ckpt, weights_only=False)
        net.load_state_dict(st["net"])
        opt.load_state_dict(st["opt"])
        sched.load_state_dict(st["sched"])
        g.set_state(st["gen"])
        hist, snaps, ep0 = st["hist"], st["snaps"], st["epoch"]
    if 0 in snap_at and 0 not in snaps and snap_fn is not None:
        snaps[0] = snap_fn(net)
    for ep in range(ep0, epochs):
        perm = torch.randperm(len(X), generator=g)
        tot = 0.0
        net.train()
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
        if (ep + 1) in snap_at and snap_fn is not None:
            snaps[ep + 1] = snap_fn(net)
        if log:
            log(row)
        if ckpt is not None:
            tmp = str(ckpt) + ".tmp"
            torch.save({"net": net.state_dict(), "opt": opt.state_dict(), "sched": sched.state_dict(),
                        "gen": g.get_state(), "hist": hist, "snaps": snaps, "epoch": ep + 1}, tmp)
            os.replace(tmp, ckpt)
    return net, hist, snaps


def deep_bsde_snap(p=DEFAULT_RISK, iters=4000, batch=64, lr=0.008, seed=0, log_every=50, snap_at=(), n_snap=256,
                   log=None, ckpt=None, ckpt_every=100):
    """:func:`deep_bsde` (the same network and draws) with the shooting picture: at the iterations in ``snap_at``,
    the terminal values Y_N against their targets g(X_N) on ``n_snap`` fresh paths. Pass p with delta = 1 for the
    linear check (no default: plain discounted expectation)."""
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

    def run(n, gen=None, keep=False):
        dW = math.sqrt(dt) * torch.randn(n, N, d, generator=gen)
        logx = math.log(p["x0"]) + torch.cumsum((p["mu"] - 0.5 * p["sigma"] ** 2) * dt + p["sigma"] * dW, 1)
        X = torch.cat([torch.full((n, 1, d), p["x0"]), torch.exp(logx)], 1)
        Y = y0.expand(n)
        Z = z0.expand(n, d)
        path = [Y]
        for k in range(N):
            if k > 0:
                Z = nets[k - 1](X[:, k] / p["x0"] - 1) * p["x0"] * p["sigma"] / 10
            Y = Y + ((1 - p["delta"]) * Q(Y) * Y + p["R"] * Y) * dt + (Z * dW[:, k]).sum(1)
            path.append(Y)
        if keep:
            return Y, X[:, -1].min(1).values, torch.stack(path, 1)
        return Y, X[:, -1].min(1).values

    curve, snaps, it0 = [], {}, 0
    import os
    if ckpt is not None and os.path.exists(ckpt):  # resume: weights, optimizer, random state, history
        st = torch.load(ckpt, weights_only=False)
        with torch.no_grad():
            y0.copy_(st["y0"])
            z0.copy_(st["z0"])
        nets.load_state_dict(st["nets"])
        opt.load_state_dict(st["opt"])
        torch.set_rng_state(st["rng"])
        curve, snaps, it0 = st["curve"], st["snaps"], st["it"]
    for it in range(it0, iters + 1):
        if ckpt is not None and it > it0 and it % ckpt_every == 0:
            torch.save({"y0": y0.detach(), "z0": z0.detach(), "nets": nets.state_dict(), "opt": opt.state_dict(),
                        "rng": torch.get_rng_state(), "curve": curve, "snaps": snaps, "it": it}, str(ckpt) + ".tmp")
            os.replace(str(ckpt) + ".tmp", ckpt)
        nets.train()
        if it in snap_at:
            with torch.no_grad():
                Ys, gs, Yp = run(n_snap, torch.Generator().manual_seed(4242), keep=True)
            snaps[it] = {"Y": Ys.numpy(), "g": gs.numpy(), "u0": float(y0.detach()), "Ypath": Yp[:32].numpy()}
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
    return {"u0": float(y0.detach()), "curve": curve, "snaps": snaps}


def stopping_regions(nets, p=MAX_CALL, grid=None, dates=None):
    """The exercise regions of trained deep-stopping networks (:func:`deep_stopping`'s 'nets') for two assets: at
    each date n, 'stop' on a grid of (S1, S2). Returns (grid, {n: 0/1 array (len(grid), len(grid)), rows S2})."""
    import torch

    grid = np.linspace(60, 180, 61) if grid is None else np.asarray(grid, float)
    G1, G2 = np.meshgrid(grid, grid)
    S = torch.tensor(np.c_[G1.ravel(), G2.ravel()] / p["s0"], dtype=torch.float32)
    out = {}
    for n in (dates or sorted(nets)):
        net = nets[n]
        net.eval()
        disc = math.exp(-p["r"] * n * p["T"] / p["N"])
        pay = torch.clamp(S.max(1).values * p["s0"] - p["K"], min=0) * disc
        with torch.no_grad():
            out[n] = (net(torch.cat([S, pay[:, None] / p["s0"]], 1))[:, 0] > 0).numpy().reshape(len(grid), -1).astype(int)
    return grid, out


def train_ddpm_snap(real, steps=200, iters=4000, batch=256, lr=1e-3, width=256, seed=0, log=None):
    """:func:`train_ddpm` (the same network and draws) whose sampler can also return the reverse process:
    ``sample(n, seed, snap_at=(...))`` -> (x_0, {t: x_t}). Returns (sample, curve, abar) with abar the forward
    process's cumulative products (x_t = sqrt(abar_t) x_0 + sqrt(1 - abar_t) eps)."""
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
    def sample(n, seed=0, snap_at=()):
        gg = torch.Generator().manual_seed(seed)
        x = torch.randn(n, L, generator=gg)
        snaps = {steps: x.numpy().copy()} if steps in snap_at else {}
        for t in range(steps - 1, -1, -1):
            tt = torch.full((n,), t)
            e = net(torch.cat([x, temb(tt)], 1))
            x = (x - betas[t] / (1 - abar[t]).sqrt() * e) / alpha[t].sqrt()
            if t > 0:
                x = x + betas[t].sqrt() * torch.randn(x.shape, generator=gg)
            if t in snap_at:
                snaps[t] = x.numpy().copy()
        return (x.numpy(), snaps) if snap_at else x.numpy()
    return sample, curve, abar.numpy()


def deep_stopping_ckpt(p=MAX_CALL, steps=600, batch=8192, lr=1e-3, n_eval=1_000_000, seed=0, ckpt=None, log=None):
    """:func:`deep_stopping` (the same networks, draws and objective) saving the trained networks after every exercise
    date to ``ckpt`` and resuming from there: on a shared machine a run that is stopped loses one date, not all."""
    import os

    import torch
    import torch.nn as nn

    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed + 1)
    d, N = p["d"], p["N"]

    def net():
        return nn.Sequential(nn.BatchNorm1d(d + 1), nn.Linear(d + 1, d + 40), nn.BatchNorm1d(d + 40), nn.ReLU(),
                             nn.Linear(d + 40, d + 40), nn.BatchNorm1d(d + 40), nn.ReLU(), nn.Linear(d + 40, 1))
    nets, curves = {}, {}

    def feats(S, g, n):
        return torch.cat([S[:, n] / p["s0"], g[:, n:n + 1] / p["s0"]], 1)

    def future_value(S, g, n_from):
        G = g[:, N].clone()
        for m in range(N - 1, n_from - 1, -1):
            nets[m].eval()
            with torch.no_grad():
                stop = nets[m](feats(S, g, m))[:, 0] > 0
            G = torch.where(stop, g[:, m], G)
        return G

    start = N - 1
    if ckpt is not None and os.path.exists(ckpt):
        st = torch.load(ckpt, weights_only=False)
        for m, sd in st["nets"].items():
            nets[m] = net()
            nets[m].load_state_dict(sd)
        curves = st["curves"]
        gen.set_state(st["gen"])
        torch.set_rng_state(st["rng"])
        start = min(nets) - 1
    for n in range(start, 0, -1):
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
        if ckpt is not None:
            torch.save({"nets": {m: v.state_dict() for m, v in nets.items()}, "curves": curves, "gen": gen.get_state(),
                        "rng": torch.get_rng_state()}, str(ckpt) + ".tmp")
            os.replace(str(ckpt) + ".tmp", ckpt)
    vals = []
    for _ in range(n_eval // 100000):
        S, g = max_call_paths(p, 100000, gen)
        vals.append(future_value(S, g, 1))
    v = torch.cat(vals)
    return {"lower": float(v.mean()), "se": float(v.std() / math.sqrt(len(v))), "curves": curves, "nets": nets}
