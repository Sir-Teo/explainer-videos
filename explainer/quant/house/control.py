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
def _basis(x, deg, knots=None):
    """Polynomials of degree ``deg``, or, with ``knots``, piecewise-linear hat functions (local, so they follow a
    payoff's kinks; Gobet, Lemor and Warin use local bases for the same reason)."""
    if knots is None:
        return np.column_stack([x ** k for k in range(deg + 1)])
    h = np.diff(knots)
    cols = []
    for j, kj in enumerate(knots):
        left = (x - knots[j - 1]) / h[j - 1] if j > 0 else np.ones_like(x)
        right = (knots[j + 1] - x) / h[j] if j < len(knots) - 1 else np.ones_like(x)
        cols.append(np.clip(np.minimum(left, right), 0, 1))
    return np.column_stack(cols)


def bsde_regression(payoff, S0, T, sigma, mu, r, R=None, steps=50, paths=100_000, deg=6, seed=0, hats=0) -> dict:
    """Solve -dY = f(Y, Z) dt - Z dW, Y_T = payoff(S_T), by least-squares Monte Carlo (Gobet, Lemor and Warin 2005).

    The driver is the hedger's: f = -r Y - theta Z with theta = (mu - r)/sigma (Black-Scholes), and with a borrowing
    rate R > r for negative cash, f = -r Y - theta Z - (R - r) min(Y - Z/sigma, 0) (Bergman 1995), which makes the
    price nonlinear.  Z/(sigma S) is the hedge ratio.  ``hats`` > 0 regresses on that many piecewise-linear hat
    functions (knots at quantiles of the simulated spot) instead of polynomials.  Returns Y0 and Z0."""
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
            knots = np.quantile(x, np.linspace(0.001, 0.999, hats)) if hats else None
            B = _basis(x, deg, knots)
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


def ppo_merton(mu, r, sigma, T=10.0, steps=40, iters=150, batch=256, seed=0, lr=3e-3, clip=0.2, epochs=8, lam=0.0,
               explore=None, snapshots=(0, 5, 10, 20, 40, 80, 149)) -> dict:
    """Train a Gaussian policy pi(t/T, log w) by PPO, reward = each step's log growth (log utility), discount 1,
    advantages by GAE(lam) on a learned critic (lam = 0: one-step TD errors, which keep only this step's noise; the
    reward-to-go carries all the future noise, and near the optimum the signal is a fraction of a percent a year).
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
    # ``explore``: a fixed exploration noise instead of a learned one; near the optimum the objective is so flat that
    # a learned noise collapses before the mean arrives, and the gradient's signal shrinks with the noise
    log_std = torch.nn.Parameter(torch.tensor(float(np.log(explore)) if explore else -0.5),
                                 requires_grad=explore is None)
    opt = torch.optim.Adam(list(pol.parameters()) + list(val.parameters()) + ([log_std] if explore is None else []),
                           lr=lr)
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
        st = torch.tensor(S.reshape(-1, 2), dtype=torch.float32)
        with torch.no_grad():
            v = val(st).squeeze(-1).numpy().reshape(steps, batch)
        v_next = np.vstack([v[1:], np.zeros((1, batch))])
        delta = Rw + v_next - v
        adv = np.zeros_like(delta)
        run = np.zeros(batch)
        for n in range(steps - 1, -1, -1):
            run = delta[n] + lam * run
            adv[n] = run
        ret = adv + v
        at = torch.tensor(A.reshape(-1), dtype=torch.float32)
        rt = torch.tensor(ret.reshape(-1), dtype=torch.float32)
        lpt = torch.tensor(LP.reshape(-1), dtype=torch.float32)
        adv = torch.tensor(adv.reshape(-1), dtype=torch.float32)
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
            "final_std": float(log_std.detach().exp())}


# ---------------------------------------------------------------------------
# Part 8 expansion: the HJB by finite differences, viscosity, consumption, transaction costs, stopping, mean-field
# liquidation, prospect theory, robust control, drawdown floors, and PPO with trading costs
# ---------------------------------------------------------------------------
def merton_value_factor(mu, r, sigma, gamma, tau):
    """f(t) in V(t, x) = f(t) x^(1-gamma)/(1-gamma) for Merton's problem, tau = T - t time to go."""
    theta = (mu - r) / sigma
    return np.exp((1 - gamma) * (r + theta ** 2 / (2 * gamma)) * np.asarray(tau, float))


def hjb_fd_merton(mu, r, sigma, gamma, T=10.0, n_t=400, n_y=401, y_lim=2.0, tol=1e-10, max_pass=20):
    """Merton's HJB  V_t + sup_pi {(r + pi(mu - r) - pi^2 sigma^2/2) V_y + pi^2 sigma^2/2 V_yy} = 0  in y = log wealth,
    V(T) = u, by implicit finite differences with policy iteration at each time step (Howard): given pi, solve the
    linear system for V; given V, pi = -(mu - r) V_y / (sigma^2 (V_yy - V_y)); repeat until pi stops moving.  Central
    differences where they are monotone, upwind otherwise.  At the two ends of the grid the value scales with wealth
    (V_y = (1 - gamma) V), the homogeneity of CRRA.  Returns the grid, V and pi at t = 0, the passes per step, and a
    few time slices."""
    from scipy.linalg import solve_banded
    y = np.linspace(-y_lim, y_lim, n_y)
    h = y[1] - y[0]
    dt = T / n_t
    V = crra(np.exp(y), gamma)
    pi = np.full(n_y, 0.5)
    passes, slices = [], {}
    k = 1 - gamma
    for n in range(n_t - 1, -1, -1):
        Vn1 = V.copy()
        for p_ in range(max_pass):
            a = 0.5 * pi ** 2 * sigma ** 2
            b = r + pi * (mu - r) - a
            central = a >= np.abs(b) * h / 2
            lo = np.where(central, a / h ** 2 - b / (2 * h), a / h ** 2 + np.maximum(-b, 0) / h)
            up = np.where(central, a / h ** 2 + b / (2 * h), a / h ** 2 + np.maximum(b, 0) / h)
            di = -(lo + up)
            # (I - dt L) V = Vn1; ghost nodes from V_y = k V:  V_{-1} = V_1 - 2 h k V_0,  V_{N} = V_{N-2} + 2 h k V_{N-1}
            A = np.zeros((3, n_y))
            A[1] = 1 - dt * di
            A[0, 1:] = -dt * up[:-1]
            A[2, :-1] = -dt * lo[1:]
            A[1, 0] += dt * lo[0] * 2 * h * k
            A[0, 1] += -dt * lo[0]
            A[1, -1] += -dt * up[-1] * 2 * h * k
            A[2, -2] += -dt * up[-1]
            V = solve_banded((1, 1), A, Vn1)
            Vy = np.gradient(V, h)
            Vyy = np.empty_like(V)
            Vyy[1:-1] = (V[2:] - 2 * V[1:-1] + V[:-2]) / h ** 2
            Vyy[0], Vyy[-1] = Vyy[1], Vyy[-2]
            new = np.clip(-(mu - r) * Vy / (sigma ** 2 * (Vyy - Vy)), -5, 5)
            moved = float(np.max(np.abs(new - pi)))
            pi = new
            if moved < tol:
                break
        passes.append(p_ + 1)
        if n % max(n_t // 10, 1) == 0:
            slices[round(n * dt, 6)] = V.copy()
    exact = merton_value_factor(mu, r, sigma, gamma, T) * crra(np.exp(y), gamma)
    return {"y": y, "V": V, "pi": pi, "exact": exact, "passes": np.array(passes[::-1]), "slices": slices}


def eikonal_march(n, scheme="upwind", t_end=6.0, cfl=0.4, snapshots=()):
    """u_t + |u_x| = 1 on (-1, 1), u = 0 at both ends, from u = 0: its steady state solves |u'| = 1, whose viscosity
    solution is the distance to the boundary, 1 - |x|.  ``upwind``: the monotone Godunov (Rouy-Tourin) Hamiltonian
    max(D^- u, -D^+ u, 0); ``central``: |central difference|, consistent but not monotone.  Returns x, the final u and
    the profiles at the requested times."""
    x = np.linspace(-1, 1, n)
    h = x[1] - x[0]
    dt = cfl * h
    u = np.zeros(n)
    steps = int(round(t_end / dt))
    snaps = {}
    want = {int(round(s / dt)): s for s in snapshots}
    with np.errstate(over="ignore", invalid="ignore"):
        for it in range(1, steps + 1):
            if scheme == "upwind":
                dm = (u[1:-1] - u[:-2]) / h
                dp = (u[2:] - u[1:-1]) / h
                H = np.maximum(np.maximum(dm, 0), np.maximum(-dp, 0))
            else:
                H = np.abs((u[2:] - u[:-2]) / (2 * h))
            u[1:-1] = u[1:-1] + dt * (1 - H)
            if it in want:
                snaps[want[it]] = u.copy()
    return {"x": x, "u": u, "snaps": snaps}


def merton_consumption_rate(rho, mu, r, sigma, gamma, tau=None):
    """Merton (1971): the optimal consumption-to-wealth ratio with CRRA utility of consumption and time preference
    rho.  Infinite horizon: nu = (rho - (1 - gamma)(r + theta^2/(2 gamma)))/gamma; with tau years left (and no
    bequest), nu / (1 - exp(-nu tau))."""
    theta = (mu - r) / sigma
    nu = (rho - (1 - gamma) * (r + theta ** 2 / (2 * gamma))) / gamma
    if tau is None:
        return float(nu)
    tau = np.asarray(tau, float)
    return np.where(np.abs(nu) < 1e-12, 1 / np.maximum(tau, 1e-12), nu / (1 - np.exp(-nu * np.maximum(tau, 1e-12))))


def no_trade_band(mu, r, sigma, gamma, eps, dt, steps, grid=None, nodes=15):
    """The Davis-Norman no-trade band by dynamic programming in the risky fraction p (wealth factors out, CRRA).
    Each period: trade from p to p' paying eps |p' - p| of wealth, then the market moves.  h(p) is the expected
    utility of the growth factor to the horizon (gamma != 1: E[G^(1-gamma)], minimized for gamma > 1), or its expected
    log (gamma = 1, maximized).  Returns the band [lo, hi] (the fractions where not trading is optimal, far from the
    horizon) and the target for every starting fraction."""
    if grid is None:
        grid = np.linspace(0, 1.2, 601)
    z, wq = np.polynomial.hermite_e.hermegauss(nodes)
    wq = wq / wq.sum()
    R = np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)
    Rf = np.exp(r * dt)
    log_u = abs(gamma - 1) < 1e-12
    h = np.zeros_like(grid) if log_u else np.ones_like(grid)
    cost = np.maximum(1 - eps * np.abs(grid[None, :] - grid[:, None]), 1e-12)  # [from, to]
    for _ in range(steps):
        G = np.maximum(grid[:, None] * R[None, :] + (1 - grid[:, None]) * Rf, 1e-12)
        p_next = grid[:, None] * R[None, :] / G
        if log_u:
            C = ((np.log(G) + np.interp(p_next, grid, h)) * wq).sum(1)
            J = np.log(cost) + C[None, :]
            k = J.argmax(1)
        else:
            C = (G ** (1 - gamma) * np.interp(p_next, grid, h) * wq).sum(1)
            J = cost ** (1 - gamma) * C[None, :]
            k = J.argmax(1) if gamma < 1 else J.argmin(1)
        h = J[np.arange(len(grid)), k]
    target = grid[k]
    stay = np.isclose(target, grid, atol=1e-12)
    return {"lo": float(grid[stay].min()), "hi": float(grid[stay].max()), "grid": grid, "target": target}


def band_halfwidth_asymptotic(mu, r, sigma, gamma, eps):
    """Small-cost asymptotics of the no-trade band's half-width (Janecek and Shreve 2004; Rogers 2004):
    (3/(2 gamma) pi*^2 (1 - pi*)^2 eps)^(1/3)."""
    p = merton_fraction(mu, r, sigma, gamma)
    return float((3 / (2 * gamma) * p ** 2 * (1 - p) ** 2 * eps) ** (1 / 3))


def snell_envelope(g, max_sweeps=200000, tol=1e-12, every=0):
    """The Snell envelope of a payoff g on {0, ..., N} for a symmetric random walk absorbed at the ends, by value
    iteration: U <- max(g, (U(x-1) + U(x+1))/2) inside, U = g at the ends.  Returns U, the sweeps used, and (with
    ``every``) the iterates every so many sweeps."""
    g = np.asarray(g, float)
    U = g.copy()
    hist = [U.copy()] if every else []
    for s in range(1, max_sweeps + 1):
        new = U.copy()
        new[1:-1] = np.maximum(g[1:-1], 0.5 * (U[:-2] + U[2:]))
        moved = float(np.max(np.abs(new - U)))
        U = new
        if every and s % every == 0:
            hist.append(U.copy())
        if moved < tol:
            break
    return {"U": U, "sweeps": s, "history": hist}


def concave_majorant(g):
    """The least concave majorant of g on {0, ..., N}: the upper convex hull of the points (x, g(x)), interpolated."""
    g = np.asarray(g, float)
    x = np.arange(len(g))
    hull = []
    for i in range(len(g)):  # Andrew's monotone chain, upper hull
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            if (b - a) * (g[i] - g[a]) - (g[b] - g[a]) * (i - a) >= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    return np.interp(x, hull, g[hull])


def perpetual_put(K, r, sigma):
    """McKean (1965): the perpetual American put.  V(S) = (K - b)(S/b)^(-beta) above the exercise level b,
    beta = 2r/sigma^2, and smooth fit gives b* = beta K/(1 + beta)."""
    beta = 2 * r / sigma ** 2
    return {"beta": float(beta), "b": float(beta * K / (1 + beta))}


def perpetual_put_value(S, K, r, sigma, b):
    """The value of exercising the perpetual put the first time the stock falls to the level b."""
    beta = 2 * r / sigma ** 2
    S = np.asarray(S, float)
    return np.where(S <= b, np.maximum(K - S, 0), (K - b) * (S / b) ** (-beta))


def liquidation_closed(N, kappa, eta, T, t):
    """Inventory (from 1) of each of N symmetric traders liquidating over [0, T] with temporary cost eta v^2 and
    permanent impact kappa times the others' average selling rate (no risk aversion): Q'' + c Q' = 0 with
    c = kappa (N - 1)/(2 N eta).  N = 1 is TWAP; N -> infinity the mean-field game."""
    t = np.asarray(t, float)
    c = kappa * (1 - 1 / N) / (2 * eta) if np.isfinite(N) else kappa / (2 * eta)
    if c < 1e-12:
        return 1 - t / T
    return (np.exp(-c * t) - np.exp(-c * T)) / (1 - np.exp(-c * T))


def mfg_liquidation(N, kappa, eta, phi=0.0, T=1.0, n=400, iters=200, damping=0.5, tol=1e-12, q0=None):
    """The liquidation game by fictitious play.  Given the crowd's selling rate m(t), each trader's best response
    solves the Euler-Lagrange equation 2 eta Q'' = kappa m + 2 phi Q, Q(0) = q0, Q(T) = 0 (a tridiagonal system);
    the crowd's rate is then (N - 1)/N of the average best response's selling rate, mixed with the old m by
    ``damping``.  ``q0``: the traders' starting inventories (default one trader with 1).  Returns t, the inventories,
    the crowd's rate and the residual per iteration."""
    from scipy.linalg import solve_banded
    t = np.linspace(0, T, n + 1)
    h = T / n
    q0 = np.atleast_1d(np.asarray([1.0] if q0 is None else q0, float))
    share = (1 - 1 / N) if np.isfinite(N) else 1.0
    m = np.zeros(n + 1)
    A = np.zeros((3, n - 1))
    A[0, 1:] = 2 * eta / h ** 2
    A[1] = -4 * eta / h ** 2 - 2 * phi
    A[2, :-1] = 2 * eta / h ** 2
    res = []

    def best(m):
        rhs = np.repeat((kappa * m[1:-1])[:, None], len(q0), 1)
        rhs[0] -= 2 * eta / h ** 2 * q0
        Q = np.zeros((n + 1, len(q0)))
        Q[0] = q0
        Q[1:-1] = solve_banded((1, 1), A, rhs)
        return Q

    for _ in range(iters):
        Q = best(m)
        v = -np.gradient(Q.mean(1), h)
        new = share * v
        r_ = float(np.max(np.abs(new - m)))
        res.append(r_)
        m = (1 - damping) * m + damping * new
        if r_ < tol:
            break
    Q = best(m)
    return {"t": t, "Q": Q, "m": m, "residual": np.array(res)}


def cpt_value(z, alpha=0.88, lam=2.25, g_gain=0.61, g_loss=0.69):
    """Cumulative prospect theory (Tversky and Kahneman 1992) of equally likely outcomes z: value x^alpha for gains,
    -lam (-x)^alpha for losses, and rank-dependent decision weights from w(p) = p^g/(p^g + (1-p)^g)^(1/g), cumulated
    from the extremes inward."""
    z = np.sort(np.asarray(z, float))
    n = len(z)

    def w(p, g):
        return p ** g / (p ** g + (1 - p) ** g) ** (1 / g)

    v = np.where(z >= 0, np.abs(z) ** alpha, -lam * np.abs(z) ** alpha)
    i = np.arange(n)
    loss = z < 0
    wl = w((i + 1) / n, g_loss) - w(i / n, g_loss)          # losses: cumulative from the worst
    wg = w((n - i) / n, g_gain) - w((n - i - 1) / n, g_gain)  # gains: cumulative from the best
    return float(np.sum(np.where(loss, wl, wg) * v))


def robust_fraction(mu, r, sigma, gamma, theta):
    """Maenhout (2004): with an entropy penalty scaled by theta, the robust Merton fraction (mu - r)/((gamma + theta)
    sigma^2); nature's worst-case drift is lowered by theta pi sigma^2."""
    return (mu - r) / ((gamma + theta) * sigma ** 2)


def detection_error(delta_mu, sigma, years):
    """The chance of picking the wrong model when telling apart two drifts delta_mu apart, with volatility sigma, from
    ``years`` of data (a likelihood-ratio test with equal priors): Phi(-delta_mu sqrt(years)/(2 sigma))."""
    return float(stats.norm.cdf(-abs(delta_mu) * np.sqrt(years) / (2 * sigma)))


def theta_for_detection(p, mu, r, sigma, gamma, years):
    """The robustness theta whose worst-case model is detected with error probability p: the distortion
    theta pi sigma^2 at the robust pi is theta (mu - r)/(gamma + theta) = 2 sigma Phi^{-1}(1 - p)/sqrt(years)."""
    d = 2 * sigma * stats.norm.ppf(1 - p) / np.sqrt(years)
    x = d / (mu - r)
    return float(np.inf if x >= 1 else gamma * x / (1 - x))


def grossman_zhou_fraction(w, peak, alpha, pi_m):
    """Grossman and Zhou (1993): never fall below alpha times the running maximum; hold the Merton fraction of the
    cushion above that floor, pi_m (W - alpha M)/W."""
    w, peak = np.asarray(w, float), np.asarray(peak, float)
    return pi_m * np.maximum(w - alpha * peak, 0) / w


def ppo_rebalance(mu, r, sigma, eps, T=10.0, steps=40, iters=300, batch=1024, seed=0, lr=3e-3, clip=0.2, epochs=8,
                  explore=0.3, snapshots=(0, 10, 25, 50, 100, 200, 299), grid_p=None) -> dict:
    """PPO on Merton's problem with log utility and a proportional cost eps: the state is (t/T, the fraction p held
    before trading), the action a trade (the new fraction is p + a), and the reward log(1 - eps |a|) plus the
    period's log growth.  The policy network starts at 'do nothing'.  Returns the mean target fraction during
    training and the policy's target over a grid of p at mid-horizon at a few iterations."""
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    g = np.random.default_rng(seed)
    dt = T / steps
    if grid_p is None:
        grid_p = np.linspace(0.5, 3.0, 51)

    def net():
        return torch.nn.Sequential(torch.nn.Linear(2, 32), torch.nn.Tanh(), torch.nn.Linear(32, 32), torch.nn.Tanh(),
                                   torch.nn.Linear(32, 1))

    pol, val = net(), net()
    with torch.no_grad():
        pol[-1].weight.mul_(0.01)
        pol[-1].bias.fill_(0.0)
    std = float(explore)
    opt = torch.optim.Adam(list(pol.parameters()) + list(val.parameters()), lr=lr)
    gq = torch.tensor(np.column_stack([np.full(len(grid_p), 0.5), grid_p]), dtype=torch.float32)
    mean_hist, snaps = [], {}
    p0 = merton_fraction(mu, r, sigma, 1.0)
    for it in range(iters):
        p = np.full(batch, p0) * np.exp(0.3 * g.standard_normal(batch))  # start near Merton, spread out
        S, A, Rw, LP, TG = [], [], [], [], []
        for n in range(steps):
            s = np.column_stack([np.full(batch, n / steps), p])
            st = torch.tensor(s, dtype=torch.float32)
            with torch.no_grad():
                m = pol(st).squeeze(-1)
                d = torch.distributions.Normal(m, std)
                a = d.sample()
                lp = d.log_prob(a)
            a_np = a.numpy().astype(float)
            tgt = np.clip(p + a_np, 0.0, 4.0)
            R = np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * g.standard_normal(batch))
            G = np.maximum(tgt * R + (1 - tgt) * np.exp(r * dt), 1e-6)
            rew = np.log(np.maximum(1 - eps * np.abs(tgt - p), 1e-6)) + np.log(G)
            S.append(s), A.append(a_np), Rw.append(rew), LP.append(lp.numpy()), TG.append(tgt)
            p = tgt * R / G
        S, A, Rw, LP = (np.array(x) for x in (S, A, Rw, LP))
        st = torch.tensor(S.reshape(-1, 2), dtype=torch.float32)
        with torch.no_grad():
            v = val(st).squeeze(-1).numpy().reshape(steps, batch)
        v_next = np.vstack([v[1:], np.zeros((1, batch))])
        adv = Rw + v_next - v
        ret = adv + v
        at = torch.tensor(A.reshape(-1), dtype=torch.float32)
        rt = torch.tensor(ret.reshape(-1), dtype=torch.float32)
        lpt = torch.tensor(LP.reshape(-1), dtype=torch.float32)
        adv = torch.tensor(adv.reshape(-1), dtype=torch.float32)
        adv = (adv - adv.mean()) / (adv.std() + 1e-8)
        for _ in range(epochs):
            d = torch.distributions.Normal(pol(st).squeeze(-1), std)
            ratio = torch.exp(d.log_prob(at) - lpt)
            l_pol = -torch.mean(torch.minimum(ratio * adv, torch.clamp(ratio, 1 - clip, 1 + clip) * adv))
            l_val = torch.mean((val(st).squeeze(-1) - rt) ** 2) * 100.0
            opt.zero_grad()
            (l_pol + l_val).backward()
            opt.step()
        mean_hist.append(float(np.mean(TG)))
        if it in snapshots:
            with torch.no_grad():
                snaps[it] = grid_p + pol(gq).squeeze(-1).numpy()
    with torch.no_grad():
        final = grid_p + pol(gq).squeeze(-1).numpy()

    def policy(t_frac, p_now):
        with torch.no_grad():
            x = torch.tensor(np.column_stack([np.full(len(p_now), t_frac), p_now]), dtype=torch.float32)
            return np.clip(p_now + pol(x).squeeze(-1).numpy(), 0.0, 4.0)

    return {"mean_target": np.array(mean_hist), "snapshots": snaps, "grid_p": grid_p, "final": final,
            "policy": policy}


def simulate_rebalance(rule, mu, r, sigma, eps, T, steps, paths=200000, seed=0, p0=None):
    """Net log growth a year (mean, standard error) and turnover a year of a rebalancing rule rule(n, p) -> target
    fraction, with proportional cost eps, log-normal stock, ``steps`` periods over T years."""
    g = np.random.default_rng(seed)
    dt = T / steps
    p = np.full(paths, merton_fraction(mu, r, sigma, 1.0) if p0 is None else p0)
    lw = np.zeros(paths)
    turn = np.zeros(paths)
    for n in range(steps):
        tgt = rule(n, p)
        lw += np.log(np.maximum(1 - eps * np.abs(tgt - p), 1e-12))
        turn += np.abs(tgt - p)
        R = np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * g.standard_normal(paths))
        G = np.maximum(tgt * R + (1 - tgt) * np.exp(r * dt), 1e-12)
        lw += np.log(G)
        p = tgt * R / G
    return {"growth": float(lw.mean() / T), "se": float(lw.std() / np.sqrt(paths) / T), "turnover": float(turn.mean() / T)}
