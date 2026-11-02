"""Decisions and control (Part 8, the sizing module): utility, dynamic programming, Merton, Kelly, stopping, BSDEs and a
policy-gradient check.  Every routine here is tested against a closed form in ``tests/test_quant_house.py``.

* utility: CRRA and CARA, certainty equivalents, the Arrow-Pratt risk premium;
* ``merton_fraction`` and ``bellman_merton``: Merton's problem by its closed form and by backward induction on a wealth
  grid (Gauss-Hermite expectations), with an optional floor (HARA utility, whose answer is portfolio insurance);
* Kelly: the binary and continuous fractions, growth rates, realized growth of fixed-fraction rebalancing;
* ``secretary``: the 1/e stopping rule; ``bsde_regression``: a backward SDE solved by least-squares Monte Carlo,
  including the nonlinear case of different borrowing and lending rates; ``hjb_two_rates``: the same price from the
  nonlinear PDE, as a check;
* ``ppo_merton``: proximal policy optimization on Merton's problem with log utility, to compare with the closed form.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------
def crra(w, gamma: float):
    """u(w) = w^(1-gamma)/(1-gamma), and log w at gamma = 1."""
    w = np.asarray(w, float)
    return np.log(w) if abs(gamma - 1) < 1e-12 else w ** (1 - gamma) / (1 - gamma)


def crra_inv(u, gamma: float):
    u = np.asarray(u, float)
    return np.exp(u) if abs(gamma - 1) < 1e-12 else (u * (1 - gamma)) ** (1 / (1 - gamma))


def cara(w, a: float):
    return -np.exp(-a * np.asarray(w, float)) / a


def certainty_equivalent(outcomes, probs, gamma: float) -> float:
    """The sure amount with the same expected CRRA utility as the gamble."""
    o, p = np.asarray(outcomes, float), np.asarray(probs, float)
    return float(crra_inv(np.sum(p * crra(o, gamma)), gamma))


def pratt_premium(w: float, sd: float, gamma: float) -> float:
    """Arrow-Pratt: the premium for a small fair gamble of standard deviation sd at wealth w, ~ (1/2) A(w) sd^2 with
    absolute risk aversion A(w) = gamma / w."""
    return 0.5 * gamma / w * sd ** 2


# ---------------------------------------------------------------------------
# Merton
# ---------------------------------------------------------------------------
def merton_fraction(mu: float, r: float, sigma: float, gamma: float) -> float:
    return (mu - r) / (gamma * sigma ** 2)


def hara_fraction(w, t, T, mu, r, sigma, gamma, floor):
    """u(W) = (W - F)^(1-gamma)/(1-gamma): invest the Merton fraction of the cushion above the floor's present value."""
    pv = floor * np.exp(-r * (T - t))
    return merton_fraction(mu, r, sigma, gamma) * (np.asarray(w, float) - pv) / np.asarray(w, float)


def bellman_merton(mu, r, sigma, gamma, T=10.0, steps=120, floor=0.0, w_max=4.0, n_w=240, pis=None, nodes=15):
    """Merton's problem by dynamic programming: V_n(w) = max_pi E[V_{n+1}(w (1 + r dt + pi (R - r dt)))] with log-normal
    stock returns R, the expectation by Gauss-Hermite quadrature, and V interpolated through its certainty equivalent
    on a grid of the cushion above the floor.  Returns the grid, the value surface V[n, i] and the optimal fraction pi[n, i]."""
    dt = T / steps
    if pis is None:
        pis = np.linspace(0.0, 3.0, 121)
    z, wq = np.polynomial.hermite_e.hermegauss(nodes)
    wq = wq / wq.sum()
    R = np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z) - 1  # stock's simple return per step
    times = np.linspace(0, T, steps + 1)
    out_V = np.zeros((steps + 1, n_w))
    out_pi = np.full((steps + 1, n_w), np.nan)
    pv = floor * np.exp(-r * (T - times))
    # grid in the cushion c = w - pv(t), log-spaced: the problem is scale-free in c
    cgrid = np.geomspace(1e-3, w_max, n_w)
    V_next = crra(cgrid, gamma)  # at T the cushion is w - F
    out_V[-1] = V_next
    for n in range(steps - 1, -1, -1):
        w = cgrid + pv[n]
        # next wealth for every (w, pi, node); cushion next = w' - pv[n+1]
        gross = 1 + r * dt + pis[None, :, None] * (R[None, None, :] - r * dt)
        c_next = w[:, None, None] * gross - pv[n + 1]
        c_next = np.maximum(c_next, 1e-9)
        lc = np.log(c_next)
        # interpolate the log certainty equivalent, which is linear in the log cushion for CRRA (and nearly so in
        # general): interpolating V itself, a concave function, biases the choice toward less risk
        lg = np.log(cgrid)
        lce = np.log(crra_inv(V_next, gamma))
        slope_lo = (lce[1] - lce[0]) / (lg[1] - lg[0])
        slope_hi = (lce[-1] - lce[-2]) / (lg[-1] - lg[-2])
        inside = np.interp(lc, lg, lce)
        lce_x = np.where(lc < lg[0], lce[0] + slope_lo * (lc - lg[0]),
                         np.where(lc > lg[-1], lce[-1] + slope_hi * (lc - lg[-1]), inside))
        val = crra(np.exp(lce_x), gamma)
        ev = val @ wq
        k = np.argmax(ev, axis=1)
        V_next = ev[np.arange(n_w), k]
        out_V[n] = V_next
        out_pi[n] = pis[k]
    return {"t": times, "cushion": cgrid, "pv_floor": pv, "V": out_V, "pi": out_pi}


# ---------------------------------------------------------------------------
# Kelly
# ---------------------------------------------------------------------------
def kelly_binary(p: float, b: float = 1.0) -> float:
    """Win b per unit staked with probability p, lose the stake otherwise: f* = p - (1 - p)/b."""
    return p - (1 - p) / b


def growth_binary(f, p: float, b: float = 1.0):
    f = np.asarray(f, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return p * np.log1p(b * f) + (1 - p) * np.log1p(-f)


def growth_continuous(f, excess: float, sigma: float, r: float = 0.0):
    """Log growth of a constant fraction f in a log-normal asset: r + f (mu - r) - f^2 sigma^2 / 2."""
    f = np.asarray(f, float)
    return r + f * excess - 0.5 * f ** 2 * sigma ** 2


def realized_growth(fractions, excess_returns, rf) -> np.ndarray:
    """Average log growth per period of rebalancing to fraction f in the risky asset each period (borrowing at rf)."""
    x, rf = np.asarray(excess_returns, float), np.asarray(rf, float)
    f = np.asarray(fractions, float)
    gross = 1 + rf[None, :] + f[:, None] * x[None, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        g = np.where(np.all(gross > 0, axis=1), np.mean(np.log(np.maximum(gross, 1e-300)), axis=1), -np.inf)
    return g


def kelly_simulation(p: float, fractions, n_bets: int, n_paths: int, seed: int = 0, w0: float = 1.0,
                     cap: float | None = None) -> dict:
    """Wealth after n_bets even-money bets at fixed fractions (optionally stopping at a cap); returns final wealth by
    fraction."""
    g = np.random.default_rng(seed)
    wins = g.random((n_paths, n_bets)) < p
    out = {}
    for f in fractions:
        w = np.full(n_paths, w0)
        done = np.zeros(n_paths, bool)
        for t in range(n_bets):
            stake = f * w
            w = np.where(done, w, w + np.where(wins[:, t], stake, -stake))
            if cap is not None:
                hit = w >= cap
                w = np.where(hit & ~done, cap, w)
                done |= hit
        out[float(f)] = w
    return out


# ---------------------------------------------------------------------------
# Optimal stopping
# ---------------------------------------------------------------------------
def secretary(n: int, cutoffs, trials: int = 20000, seed: int = 0) -> np.ndarray:
    """Probability of choosing the best of n candidates seen in random order, rejecting the first k and then taking the
    first one better than all before it."""
    g = np.random.default_rng(seed)
    ranks = np.argsort(g.random((trials, n)), axis=1)  # ranks[i, j]: quality of candidate j (higher is better)
    best = ranks.argmax(axis=1)
    out = []
    for k in cutoffs:
        if k == 0:
            out.append(float(np.mean(best == 0)))
            continue
        bar = ranks[:, :k].max(axis=1)
        better = ranks[:, k:] > bar[:, None]
        has = better.any(axis=1)
        pick = k + better.argmax(axis=1)
        out.append(float(np.mean(has & (pick == best))))
    return np.array(out)


def secretary_exact(n: int, k: int) -> float:
    if k == 0:
        return 1.0 / n
    return k / n * sum(1.0 / (j - 1) for j in range(k + 1, n + 1))


# ---------------------------------------------------------------------------
# BSDEs
# ---------------------------------------------------------------------------
def _basis(x, deg):
    return np.column_stack([x ** k for k in range(deg + 1)])


def bsde_regression(payoff, S0, T, sigma, mu, r, R=None, steps=50, paths=100_000, deg=6, seed=0) -> dict:
    """Solve -dY = f(Y, Z) dt - Z dW, Y_T = payoff(S_T), by least-squares Monte Carlo (Gobet, Lemor and Warin 2005).

    The driver is the hedger's: f = -r Y - theta Z with theta = (mu - r)/sigma (Black-Scholes), and with a borrowing
    rate R > r for negative cash, f = -r Y - theta Z - (R - r) min(Y - Z/sigma, 0) (Bergman 1995), which makes the
    price nonlinear.  Z/(sigma S) is the hedge ratio.  Returns Y0 and Z0."""
    g = np.random.default_rng(seed)
    dt = T / steps
    dW = g.standard_normal((paths, steps)) * np.sqrt(dt)
    logS = np.log(S0) + np.cumsum((mu - 0.5 * sigma ** 2) * dt + sigma * dW, axis=1)
    S = np.column_stack([np.full(paths, S0), np.exp(logS)])
    theta = (mu - r) / sigma
    Y = payoff(S[:, -1])
    scale = S0
    Z0 = 0.0
    for n in range(steps - 1, -1, -1):
        x = (S[:, n] - scale) / scale
        if n == 0:
            Zn = np.full(paths, np.mean(Y * dW[:, n]) / dt)
            EY = np.full(paths, Y.mean())
        else:
            B = _basis(x, deg)
            cz, *_ = np.linalg.lstsq(B, Y * dW[:, n] / dt, rcond=None)
            cy, *_ = np.linalg.lstsq(B, Y, rcond=None)
            Zn, EY = B @ cz, B @ cy
        # explicit in Y: Y_n = E[Y_{n+1}] + f(E[Y_{n+1}], Z_n) dt
        f = -r * EY - theta * Zn
        if R is not None:
            f = f - (R - r) * np.minimum(EY - Zn / sigma, 0.0)
        Y = EY + f * dt
        if n == 0:
            Z0 = float(Zn[0])
    return {"Y0": float(Y.mean()), "Z0": Z0, "delta0": Z0 / (sigma * S0)}


def hjb_two_rates(payoff, S0, T, sigma, r, R, n_s=400, steps=2000, s_max_mult=4.0) -> float:
    """The same nonlinear price from the PDE  V_t + (1/2) sigma^2 S^2 V_SS + rho (S V_S - V) = 0, where the rate
    rho is r when the hedge's cash V - S V_S is positive and R when it is negative.  Explicit finite differences."""
    s = np.linspace(0, s_max_mult * S0, n_s + 1)
    ds = s[1] - s[0]
    dt = T / steps
    lim = ds ** 2 / (sigma ** 2 * s[-1] ** 2 + 1e-12)
    if dt > 0.9 * lim:
        steps = int(np.ceil(T / (0.9 * lim)))
        dt = T / steps
    V = payoff(s)
    for _ in range(steps):
        Vs = np.gradient(V, ds)
        Vss = np.zeros_like(V)
        Vss[1:-1] = (V[2:] - 2 * V[1:-1] + V[:-2]) / ds ** 2
        cash = V - s * Vs
        rho = np.where(cash >= 0, r, R)
        Vn = V + dt * (0.5 * sigma ** 2 * s ** 2 * Vss + rho * (s * Vs - V))
        Vn[0] = V[0] * (1 - dt * r)
        Vn[-1] = 2 * Vn[-2] - Vn[-3]
        V = Vn
    return float(np.interp(S0, s, V))


# ---------------------------------------------------------------------------
# Reinforcement learning: PPO on Merton's problem with log utility
# ---------------------------------------------------------------------------
def merton_discrete_optimum(mu, r, sigma, dt, nodes=41) -> float:
    """The fraction that maximizes E log(1 + r dt + pi (R - r dt)) for one step of a log-normal stock."""
    from scipy.optimize import minimize_scalar
    z, wq = np.polynomial.hermite_e.hermegauss(nodes)
    wq = wq / wq.sum()
    R = np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z) - 1
    res = minimize_scalar(lambda p: -np.sum(wq * np.log(np.maximum(1 + r * dt + p * (R - r * dt), 1e-12))),
                          bounds=(0, 10), method="bounded")
    return float(res.x)


def ppo_merton(mu, r, sigma, T=10.0, steps=40, iters=150, batch=256, seed=0, lr=3e-3, clip=0.2, epochs=8,
               snapshots=(0, 5, 10, 20, 40, 80, 149)) -> dict:
    """Train a Gaussian policy pi(t/T, log w) by PPO, reward = each step's log growth (log utility), discount 1.
    Returns the mean fraction during training, and the policy's mean over a (t, w) grid at a few iterations."""
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    g = np.random.default_rng(seed)
    dt = T / steps

    class Net(torch.nn.Module):
        def __init__(self, out):
            super().__init__()
            self.f = torch.nn.Sequential(torch.nn.Linear(2, 32), torch.nn.Tanh(), torch.nn.Linear(32, 32), torch.nn.Tanh(),
                                         torch.nn.Linear(32, out))

        def forward(self, x):
            return self.f(x)

    pol, val = Net(1), Net(1)
    with torch.no_grad():
        pol.f[-1].bias.fill_(0.5)
    log_std = torch.nn.Parameter(torch.tensor(-0.5))
    opt = torch.optim.Adam(list(pol.parameters()) + list(val.parameters()) + [log_std], lr=lr)
    tt, ww = np.meshgrid(np.linspace(0, 1, 21), np.linspace(-1.0, 1.0, 21))
    grid = torch.tensor(np.column_stack([tt.ravel(), ww.ravel()]), dtype=torch.float32)
    mean_hist, snaps = [], {}
    for it in range(iters):
        # roll out a batch of episodes
        lw = np.zeros(batch)
        S, A, Rw, LP = [], [], [], []
        for n in range(steps):
            s = np.column_stack([np.full(batch, n / steps), lw])
            st = torch.tensor(s, dtype=torch.float32)
            with torch.no_grad():
                m = pol(st).squeeze(-1)
                d = torch.distributions.Normal(m, log_std.exp())
                a = d.sample()
                lp = d.log_prob(a)
            a_np = a.numpy().astype(float)
            R = np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * g.standard_normal(batch)) - 1
            gross = np.maximum(1 + r * dt + a_np * (R - r * dt), 1e-6)
            rew = np.log(gross)
            lw = lw + rew
            S.append(s), A.append(a_np), Rw.append(rew), LP.append(lp.numpy())
        S, A, Rw, LP = (np.array(x) for x in (S, A, Rw, LP))  # [steps, batch, ...]
        ret = np.cumsum(Rw[::-1], axis=0)[::-1]  # reward-to-go
        st = torch.tensor(S.reshape(-1, 2), dtype=torch.float32)
        at = torch.tensor(A.reshape(-1), dtype=torch.float32)
        rt = torch.tensor(ret.reshape(-1), dtype=torch.float32)
        lpt = torch.tensor(LP.reshape(-1), dtype=torch.float32)
        with torch.no_grad():
            adv = rt - val(st).squeeze(-1)
            adv = (adv - adv.mean()) / (adv.std() + 1e-8)
        for _ in range(epochs):
            d = torch.distributions.Normal(pol(st).squeeze(-1), log_std.exp())
            ratio = torch.exp(d.log_prob(at) - lpt)
            l_pol = -torch.mean(torch.minimum(ratio * adv, torch.clamp(ratio, 1 - clip, 1 + clip) * adv))
            l_val = torch.mean((val(st).squeeze(-1) - rt) ** 2) * 100.0
            opt.zero_grad()
            (l_pol + l_val).backward()
            opt.step()
        with torch.no_grad():
            gm = pol(grid).squeeze(-1).numpy()
        mean_hist.append(float(A.mean()))
        if it in snapshots:
            snaps[it] = gm.reshape(tt.shape)
    return {"mean_fraction": np.array(mean_hist), "snapshots": snaps, "grid_t": tt, "grid_logw": ww,
            "final_std": float(log_std.exp())}
