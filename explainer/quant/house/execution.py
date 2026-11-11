"""Market impact and execution (Part 37): what a large order costs, and how to schedule it.

Measurement on a trade tape: the response function and the propagator of trade signs (Bouchaud, Gefen, Potters and
Wyart 2004), aggregate impact of signed volume over windows. Models: the latent order book of Donier, Bonart,
Mastromatteo and Bouchaud (2015), whose impact is a square root; Almgren and Chriss's (2000) mean-variance schedule;
transient impact with a decay kernel (Obizhaeva and Wang 2013; Gatheral 2010; Alfonsi, Schied and Slynko 2012), its
optimal schedules and the closed form for exponential resilience. An execution environment built on the House's
queue-reactive simulator (Part 36) and a tabular Q-learning executor trained in it."""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# Measurement on a trade tape
# ---------------------------------------------------------------------------
def response_function(price, sign, lags) -> np.ndarray:
    """R(l) = E[eps_n (p_{n+l} - p_n)] in event time: the mean price move l trades after a trade, signed by it."""
    p = np.asarray(price, float)
    s = np.asarray(sign, float)
    return np.array([float(np.mean(s[:-L] * (p[L:] - p[:-L]))) for L in lags])


def propagator_fit(price, sign, n_lag: int = 200):
    """Fit the transient impact model p_{n+1} - p_n = sum_k g(k) eps_{n-k} + noise by least squares in Toeplitz form:
    g solves C g = r, with C the sign autocorrelation matrix and r(k) = E[(p_{n+1} - p_n) eps_{n-k}]. The propagator is
    G(l) = sum_{k<l} g(k), the price response l trades after a single trade. Returns (g, G)."""
    from scipy.linalg import solve_toeplitz

    p = np.asarray(price, float)
    s = np.asarray(sign, float)
    s = s - s.mean()
    r = np.diff(p)
    s0 = s[:-1]
    n = len(r)
    v = float(np.dot(s0, s0) / n)
    c = np.array([1.0] + [float(np.dot(s0[k:], s0[:-k]) / n / v) for k in range(1, n_lag)])
    rr = np.array([float(np.dot(r[k:], s0[:n - k]) / n / v) for k in range(n_lag)])
    g = solve_toeplitz(c, rr)
    G = np.r_[0.0, np.cumsum(g)]
    return g, G


def aggregate_impact(time, price, qty, sign, window_ms: float, bins: int = 12):
    """Aggregate impact: in consecutive windows, the price change against the signed volume imbalance
    phi = (buy - sell)/(buy + sell). Returns bin centres of phi, the mean price change in each bin, its standard error,
    and the counts."""
    t = np.asarray(time, float)
    k = ((t - t[0]) // window_ms).astype(np.int64)
    nw = int(k[-1]) + 1
    qs = np.asarray(qty, float) * np.asarray(sign, float)
    buy = np.bincount(k, weights=np.where(qs > 0, qs, 0.0), minlength=nw)
    sell = np.bincount(k, weights=np.where(qs < 0, -qs, 0.0), minlength=nw)
    tot = buy + sell
    first = np.full(nw, -1, np.int64)
    last = np.full(nw, -1, np.int64)
    idx = np.arange(len(k))
    first[k[::-1]] = idx[::-1]
    last[k] = idx
    ok = (tot > 0) & (first >= 0)
    p = np.asarray(price, float)
    # the change from the last trade of the previous window to the last of this one
    prev_last = np.r_[-1, last[:-1]]
    ok &= prev_last >= 0
    dp = np.where(ok, p[np.maximum(last, 0)] - p[np.maximum(prev_last, 0)], np.nan)
    phi = np.where(ok, (buy - sell) / np.maximum(tot, 1e-12), np.nan)
    edges = np.linspace(-1, 1, bins + 1)
    cen, mean, se, cnt = [], [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = ok & (phi >= a) & (phi < b if b < 1 else phi <= b)
        if m.sum() > 5:
            cen.append(float(np.mean(phi[m])))
            mean.append(float(np.mean(dp[m])))
            se.append(float(np.std(dp[m]) / math.sqrt(m.sum())))
            cnt.append(int(m.sum()))
    return np.array(cen), np.array(mean), np.array(se), np.array(cnt)


# ---------------------------------------------------------------------------
# The latent order book (Donier, Bonart, Mastromatteo and Bouchaud 2015)
# ---------------------------------------------------------------------------
def latent_book(rate: float, t_exec: float, t_after: float = 0.0, L: float = 1.0, D: float = 1.0,
                half_width: float = 30.0, nx: int = 1201, record: int = 200) -> dict:
    """A metaorder in the latent order book. The signed latent density phi(x, t) (bids positive, asks negative) diffuses,
    dphi/dt = D phi'' + m(t) delta(x - p_t), from the linear profile phi = -L x, with phi fixed at the far ends. The price
    p_t is the zero of phi. A buyer at rate m = ``rate`` for ``t_exec`` removes asks at the price (a positive source);
    then the order stops and the profile relaxes. Explicit finite differences. Returns times, prices and the volume
    executed."""
    x = np.linspace(-half_width, half_width, nx)
    dx = x[1] - x[0]
    dt = 0.4 * dx * dx / D
    phi = -L * x
    n_exec = int(round(t_exec / dt))
    n_tot = n_exec + int(round(t_after / dt))
    every = max(1, n_tot // record)
    ts, ps = [], []

    def price():
        j = int(np.argmax(phi < 0))
        if j == 0:
            return float(x[0])
        a, b = phi[j - 1], phi[j]
        return float(x[j - 1] + dx * a / (a - b))

    for n in range(n_tot):
        lap = np.zeros_like(phi)
        lap[1:-1] = (phi[2:] - 2 * phi[1:-1] + phi[:-2]) / (dx * dx)
        phi = phi + dt * D * lap
        if n < n_exec:
            p = price()
            j = int(np.clip(np.searchsorted(x, p), 1, nx - 2))
            phi[j] += rate * dt / dx
        if n % every == 0:
            ts.append(n * dt)
            ps.append(price())
    return {"t": np.array(ts), "p": np.array(ps), "Q": rate * n_exec * dt, "dt": dt}


# ---------------------------------------------------------------------------
# Almgren and Chriss (2000)
# ---------------------------------------------------------------------------
def almgren_chriss(X: float, T: float, n: int, sigma: float, eta: float, lam: float, gamma: float = 0.0) -> dict:
    """The mean-variance optimal liquidation of X over [0, T] in n steps: temporary impact eta v (cost eta n_k^2 / tau),
    permanent impact gamma, price volatility sigma per unit time, risk aversion lam. Holdings follow
    x_k = X sinh(kappa (T - t_k)) / sinh(kappa T) with cosh(kappa tau) = 1 + lam sigma^2 tau^2 / (2 eta~),
    eta~ = eta - gamma tau / 2. Returns holdings, trades, expected cost and variance."""
    tau = T / n
    eta_t = eta - gamma * tau / 2
    t = np.arange(n + 1) * tau
    if lam <= 0:
        x = X * (1 - t / T)
    else:
        kappa = math.acosh(1 + lam * sigma ** 2 * tau ** 2 / (2 * eta_t)) / tau
        x = X * np.sinh(kappa * (T - t)) / math.sinh(kappa * T)
    trades = -np.diff(x)
    cost = 0.5 * gamma * X ** 2 + eta_t / tau * float(np.sum(trades ** 2))
    var = sigma ** 2 * tau * float(np.sum(x[1:] ** 2))
    return {"t": t, "x": x, "trades": trades, "cost": cost, "var": var}


# ---------------------------------------------------------------------------
# Transient impact: decay kernels (Obizhaeva and Wang; Gatheral; Alfonsi, Schied and Slynko)
# ---------------------------------------------------------------------------
def kernel_cost(v, G) -> float:
    """The expected cost of trades v_0..v_{n-1} on a regular grid under linear transient impact with decay kernel
    values G[0..n-1] (G[0] the instantaneous impact): (1/2) v' Gamma v with Gamma_ij = G(|i - j|)."""
    v = np.asarray(v, float)
    n = len(v)
    Gm = np.asarray(G, float)[np.abs(np.subtract.outer(np.arange(n), np.arange(n)))]
    return 0.5 * float(v @ Gm @ v)


def kernel_optimal(G, X: float) -> np.ndarray:
    """The cost-minimising trades of total X under the kernel G (no sign constraint): v = X Gamma^{-1} 1 / 1' Gamma^{-1} 1,
    the discrete form of the Fredholm condition int G(|t - s|) dX_s = const."""
    n = len(G)
    Gm = np.asarray(G, float)[np.abs(np.subtract.outer(np.arange(n), np.arange(n)))]
    w = np.linalg.solve(Gm, np.ones(n))
    return X * w / w.sum()


def ow_closed_form(X: float, T: float, rho: float) -> dict:
    """Obizhaeva and Wang with exponential resilience G(t) = exp(-rho t) (unit depth): the optimal strategy is a block
    a = X/(2 + rho T) at the start, trading at the constant rate rho a in between, and a block a at the end; its cost is
    X^2/(2 + rho T)."""
    a = X / (2 + rho * T)
    return {"block": a, "rate": rho * a, "cost": X * X / (2 + rho * T)}


# ---------------------------------------------------------------------------
# An execution environment on the queue-reactive simulator (Part 36)
# ---------------------------------------------------------------------------
class QueueExec:
    """Sell ``inventory`` units of the queue-reactive book within ``steps`` decisions, each followed by ``sub`` steps of
    the simulator. A market sell of k units eats the best bid queue; each time a queue is emptied the mid falls half a
    tick and the queues are redrawn, and any remainder walks on. Prices are in half-ticks; the cost of a sale is
    (arrival mid - execution price). Unsold inventory at the end is dumped. ``fit`` is ``lob.qr_fit``'s output."""

    def __init__(self, fit, inventory: int = 20, steps: int = 20, sub: int = 10, seed: int = 0):
        self.pu, self.pd, self.rf = (np.asarray(fit[k], float) for k in ("p_up", "p_dn", "refill"))
        self.nq = int(fit["n_q"])
        self.inv0, self.steps, self.sub = inventory, steps, sub
        self.rng = np.random.default_rng(seed)
        self.cum_rf = np.cumsum(self.rf)

    def _draw(self) -> int:
        return int(np.searchsorted(self.cum_rf, self.rng.random() * self.cum_rf[-1])) + 1

    def reset(self):
        self.qb, self.qa, self.mid = self._draw(), self._draw(), 0.0
        for _ in range(self.rng.integers(0, 50)):              # a random start
            self._tick()
        self.mid0 = self.mid
        self.inv, self.k, self.cost = self.inv0, 0, 0.0
        return self.state()

    def _tick(self):
        for side in (0, 1):
            q = self.qb if side == 0 else self.qa
            r = self.rng.random()
            qi = min(q, self.nq)
            if r < self.pu[qi]:
                q += 1
            elif r < self.pu[qi] + self.pd[qi]:
                q -= 1
            if q <= 0:
                self.mid += -1.0 if side == 0 else 1.0
                self.qb, self.qa = self._draw(), self._draw()
                return
            if side == 0:
                self.qb = q
            else:
                self.qa = q

    def _sell(self, k: int) -> float:
        cost = 0.0
        while k > 0:
            take = min(k, self.qb)
            cost += take * (self.mid0 - (self.mid - 1.0))      # sold at the bid, half a tick below the mid
            self.qb -= take
            k -= take
            if self.qb <= 0:
                self.mid -= 1.0
                self.qb, self.qa = self._draw(), self._draw()
        return cost

    def imbalance_bucket(self, n: int = 3) -> int:
        i = self.qb / max(self.qb + self.qa, 1)
        return min(int(i * n), n - 1)

    def state(self):
        return (self.k, self.inv, self.imbalance_bucket())

    def step(self, k: int):
        k = int(min(k, self.inv))
        c = self._sell(k)
        self.inv -= k
        for _ in range(self.sub):
            self._tick()
        self.k += 1
        done = self.k >= self.steps or self.inv == 0
        if self.k >= self.steps and self.inv > 0:
            c += self._sell(self.inv)
            self.inv = 0
        self.cost += c
        return self.state(), -c, done


def q_learn(env: QueueExec, actions=(0, 1, 2, 4), episodes: int = 20000, alpha: float = 0.1, eps0: float = 0.3,
            seed: int = 0, risk: float = 0.0):
    """Tabular Q-learning of a selling schedule in ``env``: state (step, inventory, imbalance bucket), actions the units
    to sell now, reward minus the cost (less ``risk`` times the squared inventory held per step, a variance proxy).
    Epsilon-greedy, decaying. Returns the Q table and the learning curve (mean cost per 500 episodes)."""
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.steps + 1, env.inv0 + 1, 3, len(actions)))
    curve, run = [], []
    for ep in range(episodes):
        s = env.reset()
        eps = eps0 * max(0.02, 1 - ep / (0.8 * episodes))
        done = False
        while not done:
            if rng.random() < eps:
                a = int(rng.integers(len(actions)))
            else:
                a = int(np.argmax(Q[s]))
            s2, r, done = env.step(actions[a])
            r -= risk * s2[1] ** 2
            target = r if done else r + float(np.max(Q[s2]))
            Q[s][a] += alpha * (target - Q[s][a])
            s = s2
        run.append(env.cost)
        if len(run) == 500:
            curve.append(float(np.mean(run)))
            run = []
    return Q, np.array(curve)


def run_policy(env: QueueExec, policy, episodes: int = 5000) -> np.ndarray:
    """The implementation shortfall (in half-ticks, total over the parent order) of ``policy(state) -> units`` over
    ``episodes`` fresh episodes."""
    out = np.empty(episodes)
    for e in range(episodes):
        s = env.reset()
        done = False
        while not done:
            s, _, done = env.step(policy(s))
        out[e] = env.cost
    return out
