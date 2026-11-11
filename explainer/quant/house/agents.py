"""Machines in the market (Part 42): artificial markets, herding, a dealer environment with a learning market maker,
algorithmic collusion by Q-learning, and crowds that share one model.

* :func:`fw_model` — a Franke-Westerhoff-type market of fundamentalists and chartists who switch by herding and by
  past performance ("structural stochastic volatility"); :func:`stylized` — the stylised facts of a return series.
* :func:`kirman` / :func:`kirman_stationary` — Kirman's ant model and its exact stationary law (a birth-death chain),
  against its Beta limit.
* :class:`DealerEnv`, :func:`q_maker`, :func:`run_maker` — a Glosten-Milgrom dealer market with inventory: noise
  traders, informed traders who know the next value, and a market maker choosing its half-spread and skew.
* :func:`logit_demand`, :func:`bertrand_points`, :func:`calvano` — the Calvano-Calzolari-Denicolo-Pastorello game:
  two Q-learners setting prices on a grid against logit demand, many sessions at once; :func:`greedy_cycle`,
  :func:`impulse` — the prices they settle on and their response to a forced deviation; :func:`grim_threshold` —
  the discount factor above which grim trigger sustains a price.
* :func:`crowd` — a crowd of traders mixing a shared model's signal with their own; the flow, the volatility and the
  crash frequency as the share rises.
"""

from __future__ import annotations

import math

import numpy as np
from numba import njit


# ----------------------------------------------------------------------------------------------- artificial markets
def fw_model(T: int = 20000, phi: float = 0.18, chi: float = 2.3, sig_f: float = 0.70, sig_c: float = 2.6,
             a0: float = -0.15, a_n: float = 1.25, a_p: float = 12.0, nu: float = 0.05, mu: float = 0.01,
             seed: int = 0) -> dict:
    """Fundamentalists (who expect reversion to the log fundamental 0) and chartists (who extrapolate the last
    change), shares n_f and n_c = 1 - n_f. The market maker moves the log price by mu times their net demand:

        p_{t+1} = p_t + mu [ n_f (phi (0 - p_t) + sig_f e_f) + n_c (chi (p_t - p_{t-1}) + sig_c e_c) ].

    Each period a fraction of agents switches: the attractiveness of fundamentalism is a = a0 + a_n (n_f - n_c) +
    a_p p^2 (herding, and the pull of a mispricing), and the switching probabilities are nu e^{-a} (to chartism) and
    nu e^{a} (to fundamentalism). Volatility rises with the chartists' share, which herding makes persistent."""
    rng = np.random.default_rng(seed)
    p = np.zeros(T + 2)
    nf = np.empty(T + 2)
    nf[:2] = 0.5
    for t in range(1, T + 1):
        f, c = nf[t], 1 - nf[t]
        dem = f * (phi * (0 - p[t]) + sig_f * rng.standard_normal()) + c * (chi * (p[t] - p[t - 1]) +
                                                                            sig_c * rng.standard_normal())
        p[t + 1] = p[t] + mu * dem
        a = a0 + a_n * (f - c) + a_p * p[t] ** 2
        to_c = min(1.0, nu * math.exp(-a))
        to_f = min(1.0, nu * math.exp(a))
        nf[t + 1] = min(1.0, max(0.0, f + c * to_f - f * to_c))
    r = np.diff(p[1:])
    return {"p": p[1:], "r": r, "nf": nf[1:-1]}


def stylized(r, lags=(1, 2, 5, 10, 20, 50, 100)) -> dict:
    """Excess kurtosis, the Hill tail exponent of |r| (top 2.5%), and the autocorrelations of r and |r|."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    x = (r - r.mean()) / r.std()
    a = np.abs(x)

    def acf(y, k):
        y = y - y.mean()
        return float(np.dot(y[:-k], y[k:]) / np.dot(y, y))
    s = np.sort(a)[::-1]
    m = max(10, int(0.025 * len(s)))
    hill = float(1 / np.mean(np.log(s[:m] / s[m])))
    return {"kurt": float(np.mean(x ** 4) - 3), "hill": hill, "acf_r": [acf(x, k) for k in lags],
            "acf_abs": [acf(a, k) for k in lags], "lags": list(lags)}


# ------------------------------------------------------------------------------------------------------- herding
def kirman(N: int, eps: float, delta: float, T: int, seed: int = 0) -> np.ndarray:
    """Kirman's ant model (1993): each step one agent, chosen at random, switches on its own with probability eps, or
    else meets another at random and is converted with probability 1 - delta if the other holds the other view.
    Returns the number holding view A after each step."""
    return _kirman(N, eps, delta, T, seed)


@njit(cache=True)
def _kirman(N, eps, delta, T, seed):
    np.random.seed(seed)
    k = N // 2
    out = np.empty(T, np.int64)
    for t in range(T):
        x = k / N
        up = (1 - x) * (eps + (1 - delta) * k / (N - 1))
        dn = x * (eps + (1 - delta) * (N - k) / (N - 1))
        u = np.random.random()
        if u < up:
            k += 1
        elif u < up + dn:
            k -= 1
        out[t] = k
    return out


def kirman_stationary(N: int, eps: float, delta: float) -> np.ndarray:
    """The exact stationary law of the share k of the ant chain, by detailed balance of a birth-death chain:
    pi(k + 1) / pi(k) = up(k) / down(k + 1)."""
    k = np.arange(N + 1)
    up = (1 - k / N) * (eps + (1 - delta) * k / (N - 1))
    dn = (k / N) * (eps + (1 - delta) * (N - k) / (N - 1))
    lp = np.zeros(N + 1)
    for j in range(N):
        lp[j + 1] = lp[j] + math.log(up[j]) - math.log(dn[j + 1])
    p = np.exp(lp - lp.max())
    return p / p.sum()


def kirman_alpha(N: int, eps: float, delta: float) -> float:
    """alpha = eps (N - 1) / (1 - delta). The stationary law of k is exactly beta-binomial(N, alpha, alpha): the
    detailed-balance ratio up(k) / down(k + 1) = (N - k)(alpha + k) / ((k + 1)(alpha + N - k - 1)) is the
    beta-binomial's. So the share k / N tends to Beta(alpha, alpha): bimodal (herding) iff alpha < 1."""
    return eps * (N - 1) / (1 - delta)


def kirman_passage(N: int, eps: float, delta: float, a: int, b: int) -> float:
    """The exact mean number of steps for the ant chain to fall from k = a to k = b < a. For a birth-death chain the
    mean time to step down from k satisfies m_k = (1 + up(k) m_{k+1}) / down(k), with m_N = 1 / down(N); the passage
    time is the sum of m_k for k = b + 1, ..., a."""
    k = np.arange(N + 1)
    up = (1 - k / N) * (eps + (1 - delta) * k / (N - 1))
    dn = (k / N) * (eps + (1 - delta) * (N - k) / (N - 1))
    m = np.zeros(N + 2)
    m[N] = 1 / dn[N]
    for j in range(N - 1, 0, -1):
        m[j] = (1 + up[j] * m[j + 1]) / dn[j]
    return float(m[b + 1:a + 1].sum())


def cascade_theory(p: float) -> dict:
    """Bikhchandani-Hirshleifer-Welch with binary signals of accuracy p > 1/2, an indifferent agent following its own
    signal. Agents act in pairs: a pair that agrees (probability p^2 + q^2) starts a cascade, since every later agent's
    posterior is then set by the actions whatever its signal; a pair that disagrees leaves the public belief where it
    was. So P(right cascade) = p^2 / (p^2 + q^2), P(wrong) = q^2 / (p^2 + q^2), and P(no cascade after 2n agents) =
    (2pq)^n."""
    q = 1 - p
    return {"right": p * p / (p * p + q * q), "wrong": q * q / (p * p + q * q), "none_per_pair": 2 * p * q}


def cascade_sim(p: float, n_agents: int = 40, trials: int = 200_000, seed: int = 0) -> dict:
    """Simulate the sequence: each agent sees the earlier actions and a private signal; once the actions so far lead by
    two, everyone copies (a cascade). The true state is 1; returns the share of trials ending in each cascade."""
    rng = np.random.default_rng(seed)
    sig = rng.random((trials, n_agents)) < p
    lead = np.zeros(trials, int)
    for t in range(n_agents):
        free = np.abs(lead) < 2
        lead = lead + np.where(free, np.where(sig[:, t], 1, -1), 0)
    return {"right": float(np.mean(lead >= 2)), "wrong": float(np.mean(lead <= -2)), "none": float(np.mean(np.abs(lead) < 2))}


def betabinom_pmf(N: int, a: float) -> np.ndarray:
    """The beta-binomial(N, a, a) law, by its pmf ratio."""
    k = np.arange(N)
    lr = np.log(N - k) + np.log(a + k) - np.log(k + 1) - np.log(a + N - k - 1)
    lp = np.r_[0.0, np.cumsum(lr)]
    p = np.exp(lp - lp.max())
    return p / p.sum()


# ------------------------------------------------------------------------------------------- the dealer market
class DealerEnv:
    """A dealer market in ticks. The value v follows a random walk (+-1 tick with probability ``vol`` each step).
    Each step one trader may arrive. Informed with probability ``pi_inf``: buys if v > ask, sells if v < bid. Otherwise
    noise: a buyer and a seller each come with probability ``lam``, and each trades with probability
    exp(-kf x distance from the mid), so wider quotes trade less (the Avellaneda-Stoikov fill law). The maker quotes
    mid - half - skew s and mid + half - skew s, where s is the sign of its inventory, and moves its mid one tick
    toward each trade (it learns from flow, as in Glosten-Milgrom). Reward: the spread earned against v, the inventory
    marked to v, less ``gamma`` x inventory^2."""

    def __init__(self, pi_inf: float = 0.15, lam: float = 0.45, kf: float = 0.5, vol: float = 0.15,
                 gamma: float = 0.02, max_inv: int = 6, steps: int = 400, seed: int = 0):
        self.pi_inf, self.lam, self.kf, self.vol, self.gamma = pi_inf, lam, kf, vol, gamma
        self.max_inv, self.steps = max_inv, steps
        self.rng = np.random.default_rng(seed)
        self.tape = None

    def reset(self, record: bool = False):
        self.v = 0
        self.mid = 0
        self.inv = 0
        self.t = 0
        self.last = 0
        self.tape = [] if record else None
        return self.state()

    def state(self) -> int:
        i = int(np.clip(self.inv, -self.max_inv, self.max_inv)) + self.max_inv
        return i * 3 + (self.last + 1)

    @property
    def n_states(self) -> int:
        return (2 * self.max_inv + 1) * 3

    def quotes(self, half: int, skew: int):
        s = int(np.sign(self.inv))
        return self.mid - half - skew * s, self.mid + half - skew * s

    def step(self, half: int, skew: int):
        rng = self.rng
        bid, ask = self.quotes(half, skew)
        side, kind = 0, 0
        if rng.random() < self.pi_inf:
            kind = 1
            side = 1 if self.v > ask else (-1 if self.v < bid else 0)
        else:
            u = rng.random()
            if u < self.lam:
                side = 1 if rng.random() < math.exp(-self.kf * (ask - self.mid)) else 0
            elif u < 2 * self.lam:
                side = -1 if rng.random() < math.exp(-self.kf * (self.mid - bid)) else 0
        r = 0.0
        if side == 1 and self.inv > -self.max_inv:      # a trader buys at the ask
            r += ask - self.v
            self.inv -= 1
            self.mid += 1
        elif side == -1 and self.inv < self.max_inv:   # a trader sells at the bid
            r += self.v - bid
            self.inv += 1
            self.mid -= 1
        else:
            side = 0
        if self.tape is not None and side:
            self.tape.append((self.t, side, kind, self.v))
        self.last = side
        dv = (1 if rng.random() < 0.5 else -1) if rng.random() < self.vol else 0
        self.v += dv
        r += self.inv * dv - self.gamma * self.inv ** 2
        self.t += 1
        return self.state(), r, self.t >= self.steps


MAKER_ACTIONS = [(h, k) for h in (1, 2, 3, 4) for k in (0, 1)]


def q_maker(env: DealerEnv, episodes: int = 3000, alpha: float = 0.05, eps0: float = 0.3, disc: float = 0.97,
            seed: int = 0, snapshots=()) -> np.ndarray:
    """Tabular Q-learning over (inventory, last trade) and (half-spread, skew). ``snapshots``: episode counts at which
    a copy of the table is kept, in ``q_maker.snaps``."""
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.n_states, len(MAKER_ACTIONS)))
    q_maker.snaps = {}
    for ep in range(episodes):
        if ep in snapshots:
            q_maker.snaps[ep] = Q.copy()
        eps = eps0 * (1 - ep / episodes) + 0.01
        s = env.reset()
        done = False
        while not done:
            a = int(rng.integers(len(MAKER_ACTIONS))) if rng.random() < eps else int(np.argmax(Q[s]))
            s2, r, done = env.step(*MAKER_ACTIONS[a])
            Q[s, a] += alpha * (r + (0 if done else disc * Q[s2].max()) - Q[s, a])
            s = s2
    return Q


def maker_path(env: DealerEnv, policy) -> dict:
    """One session under ``policy``: the value, the mid, the inventory and the trades, step by step."""
    s = env.reset()
    v, mid, inv, side, done = [], [], [], [], False
    while not done:
        a = policy(s)
        s, r, done = env.step(*MAKER_ACTIONS[a])
        v.append(env.v)
        mid.append(env.mid)
        inv.append(env.inv)
        side.append(env.last)
    return {"v": v, "mid": mid, "inv": inv, "side": side}


def run_maker(env: DealerEnv, policy, episodes: int = 500) -> dict:
    """Average reward per episode and per step, and the mean half-spread quoted, for ``policy(state) -> action``."""
    tot, halves, n = [], [], 0
    for _ in range(episodes):
        s = env.reset()
        done, R = False, 0.0
        while not done:
            a = policy(s)
            halves.append(MAKER_ACTIONS[a][0])
            s, r, done = env.step(*MAKER_ACTIONS[a])
            R += r
            n += 1
        tot.append(R)
    tot = np.array(tot)
    return {"mean": float(tot.mean()), "se": float(tot.std() / math.sqrt(len(tot))), "per_step": float(tot.sum() / n),
            "half": float(np.mean(halves))}


# ---------------------------------------------------------------------------------------------- collusion
def logit_demand(p, a: float = 2.0, a0: float = 0.0, mu: float = 0.25) -> np.ndarray:
    """Calvano et al.'s logit demand for n differentiated goods: q_i = e^{(a - p_i)/mu} / (sum_j e^{(a - p_j)/mu} +
    e^{a0/mu})."""
    p = np.asarray(p, float)
    e = np.exp((a - p) / mu)
    return e / (e.sum(-1, keepdims=True) + math.exp(a0 / mu))


def profits(p, c: float = 1.0, **kw) -> np.ndarray:
    return (np.asarray(p, float) - c) * logit_demand(p, **kw)


def bertrand_points(n: int = 2, c: float = 1.0, **kw) -> dict:
    """The symmetric one-shot Nash price and the joint-profit-maximising (monopoly) price, by fixed point and search."""
    from scipy.optimize import brentq, minimize_scalar

    def br(p_other):
        f = lambda x: -profits(np.r_[x, np.full(n - 1, p_other)], c, **kw)[0]
        return minimize_scalar(f, bounds=(c, c + 5), method="bounded").x
    pn = brentq(lambda x: br(x) - x, c + 1e-6, c + 5)
    pm = minimize_scalar(lambda x: -profits(np.full(n, x), c, **kw).sum(), bounds=(c, c + 5), method="bounded").x
    return {"p_nash": float(pn), "p_mon": float(pm), "pi_nash": float(profits(np.full(n, pn), c, **kw)[0]),
            "pi_mon": float(profits(np.full(n, pm), c, **kw)[0]), "br": br}


def price_grid(pn: float, pm: float, k: int = 15, xi: float = 0.1) -> np.ndarray:
    """k equally spaced prices from p_N - xi (p_M - p_N) to p_M + xi (p_M - p_N), as in Calvano et al."""
    d = pm - pn
    return np.linspace(pn - xi * d, pm + xi * d, k)


@njit(cache=True)
def _calvano(R, k, S, iters, alpha, delta, beta, seed, noise):
    # R[a1, a2, i]: agent i's profit; state = a1 * k + a2 (last prices); S sessions in parallel
    np.random.seed(seed)
    ns = k * k
    Q = np.empty((S, 2, ns, k))
    for s in range(S):
        for i in range(2):
            for st in range(ns):
                for a in range(k):
                    # Calvano's initialisation: the discounted payoff of a against a uniformly random rival
                    tot = 0.0
                    for b in range(k):
                        tot += R[a, b, 0] if i == 0 else R[b, a, 1]
                    Q[s, i, st, a] = tot / k / (1 - delta)
    state = np.random.randint(0, ns, S)
    for t in range(iters):
        eps = math.exp(-beta * t)
        for s in range(S):
            st = state[s]
            act = np.empty(2, np.int64)
            for i in range(2):
                if np.random.random() < eps:
                    act[i] = np.random.randint(0, k)
                else:
                    best, ba = -1e18, 0
                    for a in range(k):
                        if Q[s, i, st, a] > best:
                            best, ba = Q[s, i, st, a], a
                    act[i] = ba
            nst = act[0] * k + act[1]
            for i in range(2):
                r = R[act[0], act[1], i]
                if noise > 0:
                    r += noise * np.random.standard_normal()
                mx = -1e18
                for a in range(k):
                    if Q[s, i, nst, a] > mx:
                        mx = Q[s, i, nst, a]
                Q[s, i, st, act[i]] += alpha * (r + delta * mx - Q[s, i, st, act[i]])
            state[s] = nst
    return Q, state


def calvano(k: int = 15, sessions: int = 64, iters: int = 600_000, alpha: float = 0.15, delta: float = 0.95,
            beta: float = 1e-5, noise: float = 0.0, seed: int = 0, n: int = 2, c: float = 1.0, **kw) -> dict:
    """Two Q-learners with one-period memory set prices on Calvano et al.'s grid. ``noise`` adds a zero-mean shock to
    each realised profit (an uncertain cost, as adverse selection makes a market maker's). Returns the Q tables, the
    final states, the grid and the payoff table."""
    pts = bertrand_points(n, c, **kw)
    grid = price_grid(pts["p_nash"], pts["p_mon"], k)
    P1, P2 = np.meshgrid(grid, grid, indexing="ij")
    R = profits(np.stack([P1, P2], -1), c, **kw)
    Q, st = _calvano(R, k, sessions, iters, alpha, delta, beta, seed, noise)
    return {"Q": Q, "state": st, "grid": grid, "R": R, "pts": pts, "k": k, "delta": delta}


def greedy_cycle(Q, start: int, k: int, R, max_len: int = 200) -> dict:
    """Play the greedy strategies of one session from ``start`` until a state repeats; the cycle's mean profit."""
    seen, path = {}, []
    st = start
    while st not in seen and len(path) < max_len:
        seen[st] = len(path)
        path.append(st)
        a1 = int(np.argmax(Q[0, st]))
        a2 = int(np.argmax(Q[1, st]))
        st = a1 * k + a2
    cyc = path[seen.get(st, 0):]
    pr = np.array([[R[s // k, s % k, 0], R[s // k, s % k, 1]] for s in cyc])
    return {"cycle": cyc, "len": len(cyc), "profit": pr.mean(0), "prices": [(s // k, s % k) for s in cyc]}


def delta_index(profit: float, pi_n: float, pi_m: float) -> float:
    """Calvano et al.'s collusion index: (pi - pi_N) / (pi_M - pi_N); 0 is competition, 1 is monopoly."""
    return (profit - pi_n) / (pi_m - pi_n)


def impulse(Q, start: int, k: int, R, grid, deviate_to: int | None = None, periods: int = 15) -> dict:
    """From a session's cycle, force agent 1 to deviate for one period (to its static best response to agent 2's
    price, or to ``deviate_to``), then let both play greedily: the prices that follow."""
    cyc = greedy_cycle(Q, start, k, R)
    st = cyc["cycle"][0]
    a2 = int(np.argmax(Q[1, st]))
    if deviate_to is None:
        deviate_to = int(np.argmax(R[:, a2, 0]))
    p1, p2 = [st // k], [st % k]
    st = deviate_to * k + a2
    p1.append(deviate_to)
    p2.append(a2)
    for _ in range(periods):
        a1 = int(np.argmax(Q[0, st]))
        b2 = int(np.argmax(Q[1, st]))
        p1.append(a1)
        p2.append(b2)
        st = a1 * k + b2
    return {"p1": [float(grid[i]) for i in p1], "p2": [float(grid[i]) for i in p2]}


def grim_threshold(pi_c: float, pi_n: float, pi_d: float) -> float:
    """Grim trigger sustains the collusive payoff pi_c iff pi_c / (1 - d) >= pi_d + d pi_n / (1 - d), that is
    d >= (pi_d - pi_c) / (pi_d - pi_n)."""
    return (pi_d - pi_c) / (pi_d - pi_n)


def punish_threshold(pi_c: float, pi_n: float, pi_d: float, T: int) -> float:
    """The least discount factor at which a T-period reversion to Nash deters a one-shot deviation:
    pi_d - pi_c <= (pi_c - pi_n)(d + ... + d^T); solved by bisection (inf if no d < 1 works)."""
    lo, hi = 0.0, 1.0 - 1e-12
    f = lambda d: (pi_c - pi_n) * sum(d ** j for j in range(1, T + 1)) - (pi_d - pi_c)
    if f(hi) < 0:
        return float("inf")
    for _ in range(100):
        m = 0.5 * (lo + hi)
        lo, hi = (m, hi) if f(m) < 0 else (lo, m)
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------------------------- monoculture
def crowd(N: int = 100, share: float = 0.0, T: int = 5000, kappa: float = 0.02, model_err: float = 0.0,
          seed: int = 0) -> dict:
    """N traders each trade x_i = share s_t + (1 - share) e_{i,t}: s is a shared model's signal, e their own (all
    standard normal and independent). The price moves kappa per unit of net flow per sqrt(N) traders; on day T/2 the
    shared model makes an error of ``model_err`` standard deviations (a common mistake). Returns returns, the flow's
    variance against the formula N[share^2 N + (1 - share)^2], and the share of variance that is common."""
    rng = np.random.default_rng(seed)
    s = rng.standard_normal(T)
    if model_err:
        s[T // 2] += model_err
    own = rng.standard_normal((T, N))
    flow = (share * s[:, None] + (1 - share) * own).sum(1)
    r = kappa * flow / math.sqrt(N)
    var_th = N * (share ** 2 * N + (1 - share) ** 2)
    return {"r": r, "flow_var": float(flow.var()), "flow_var_th": var_th,
            "common_share": share ** 2 * N / (share ** 2 * N + (1 - share) ** 2),
            "shock_day": float(r[T // 2]), "vol": float(r.std())}
