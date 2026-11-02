"""The options quoting engine (Part 11, the volatility desk's tools): positions as Greeks, strategy P&L surfaces, the
gamma-theta trade-off, implied correlation, quotes skewed by inventory, and hedging bands under costs.  Tested in
``tests/test_quant_house.py``.

* ``Leg``, ``book_value``, ``book_greeks``: a book of options as a sum of legs, valued and risk-measured at once;
* ``pnl_surface``: the book's P&L over a grid of spot moves and implied-volatility moves after a holding period;
* ``STRATEGIES``: the standard structures (straddle, strangle, risk reversal, butterfly, call spread, calendar);
* ``implied_correlation``: the average pairwise correlation that makes an index's implied variance consistent with
  its components' (the dispersion trade's quantity);
* ``quote``: a market maker's bid and ask in volatility, centred on a fair value and skewed against inventory in vega
  (an Avellaneda-Stoikov style rule);
* ``ww_band``: Whalley and Wilmott's (1997) no-trade band around the Black-Scholes delta under proportional costs.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from explainer.quant.house import bs


@dataclass
class Leg:
    cp: int        # +1 call, -1 put
    K: float
    T: float       # years to expiry at time 0
    qty: float     # + long, - short


def book_value(legs, S, sigma, t=0.0, r=0.0):
    """The book's value at spot ``S`` (array ok), implied volatility ``sigma`` (a number, or one per leg), elapsed
    time ``t``."""
    S = np.asarray(S, float)
    sig = np.broadcast_to(np.asarray(sigma, float), (len(legs),)) if np.ndim(sigma) else [sigma] * len(legs)
    v = np.zeros_like(S)
    for leg, s in zip(legs, sig):
        v = v + leg.qty * bs.price(S, leg.K, max(leg.T - t, 0.0), s, r, 0.0, leg.cp)
    return v


def book_greeks(legs, S, sigma, t=0.0, r=0.0) -> dict:
    out = {k: 0.0 for k in ("price", "delta", "gamma", "vega", "theta", "vanna", "volga")}
    for leg in legs:
        g = bs.greeks(S, leg.K, max(leg.T - t, 0.0), sigma, r, 0.0, leg.cp)
        for k in out:
            out[k] = out[k] + leg.qty * g[k]
    return out


def pnl_surface(legs, S0, sigma0, dS, dvol, dt, r=0.0) -> np.ndarray:
    """P&L of the book (not delta-hedged) over a grid of relative spot moves ``dS`` and implied-vol moves ``dvol``
    after ``dt`` years: rows are vol moves, columns spot moves."""
    v0 = book_value(legs, S0, sigma0, 0.0, r)
    out = np.empty((len(dvol), len(dS)))
    for i, dv in enumerate(dvol):
        out[i] = book_value(legs, S0 * (1 + np.asarray(dS)), max(sigma0 + dv, 1e-4), dt, r) - v0
    return out


def strategies(S0=100.0, T=0.25, width=0.1) -> dict:
    """The standard structures, long one unit each, at spot ``S0``."""
    lo, hi = S0 * (1 - width), S0 * (1 + width)
    return {
        "straddle": [Leg(1, S0, T, 1), Leg(-1, S0, T, 1)],
        "strangle": [Leg(1, hi, T, 1), Leg(-1, lo, T, 1)],
        "risk reversal": [Leg(1, hi, T, 1), Leg(-1, lo, T, -1)],
        "butterfly": [Leg(1, lo, T, 1), Leg(1, S0, T, -2), Leg(1, hi, T, 1)],
        "call spread": [Leg(1, S0, T, 1), Leg(1, hi, T, -1)],
        "calendar": [Leg(1, S0, 2 * T, 1), Leg(1, S0, T, -1)],
    }


# ---------------------------------------------------------------------------
def implied_correlation(index_vol, weights, vols) -> float:
    """rho such that sigma_I^2 = sum w_i^2 s_i^2 + rho sum_{i != j} w_i w_j s_i s_j."""
    w, s = np.asarray(weights, float), np.asarray(vols, float)
    own = np.sum(w ** 2 * s ** 2)
    cross = np.sum(w * s) ** 2 - own
    return float((index_vol ** 2 - own) / cross)


def quote(fair_vol, inventory_vega, half_spread=0.01, skew_per_vega=0.002, vega_limit=None) -> dict:
    """Bid and ask in implied volatility around ``fair_vol``, shifted against the book's vega inventory: long vega,
    quote lower (to sell, not buy); short vega, quote higher.  Outside a vega limit, quote one side only."""
    mid = fair_vol - skew_per_vega * inventory_vega
    bid, ask = mid - half_spread, mid + half_spread
    if vega_limit is not None and inventory_vega >= vega_limit:
        bid = np.nan
    if vega_limit is not None and inventory_vega <= -vega_limit:
        ask = np.nan
    return {"bid": bid, "ask": ask, "mid": mid}


def ww_band(S, K, T, sigma, cost, gamma_risk=1.0, r=0.0, cp=1) -> dict:
    """Whalley and Wilmott's asymptotic no-trade band for a short option hedged under proportional cost ``cost``:
    delta +/- (3 cost S Gamma^2 / (2 gamma_risk))^(1/3), with ``gamma_risk`` the hedger's risk aversion."""
    g = bs.greeks(S, K, T, sigma, r, 0.0, cp)
    h = (1.5 * cost * S * g["gamma"] ** 2 * np.exp(-r * T) / gamma_risk) ** (1 / 3)
    return {"delta": g["delta"], "lo": g["delta"] - h, "hi": g["delta"] + h, "half_width": h}


def hedge_with_band(t, S, K, T, sigma, cost, band_half=None, gamma_risk=1.0, position=-1, cp=1) -> dict:
    """Run a short (``position`` = -1) option hedged only when the delta leaves a band (Whalley-Wilmott if
    ``band_half`` is None, a fixed half-width otherwise; 0 means rehedge every step).  Returns the P&L per path,
    the trading cost, and the number of trades."""
    t = np.asarray(t, float)
    S = np.atleast_2d(np.asarray(S, float))
    n_paths, n1 = S.shape
    tau = np.maximum(T - t, 1e-12)
    prem = bs.price(S[:, 0], K, T, sigma, 0.0, 0.0, cp)
    g0 = bs.greeks(S[:, 0], K, tau[0], sigma, 0.0, 0.0, cp)
    shares = -position * g0["delta"]
    cash = -position * prem - shares * S[:, 0] - cost * np.abs(shares) * S[:, 0]
    costs = cost * np.abs(shares) * S[:, 0]
    trades = np.ones(n_paths)
    for i in range(1, n1 - 1):
        g = bs.greeks(S[:, i], K, tau[i], sigma, 0.0, 0.0, cp)
        target = -position * g["delta"]
        if band_half is None:
            hw = (1.5 * cost * S[:, i] * g["gamma"] ** 2 / gamma_risk) ** (1 / 3)
        else:
            hw = np.full(n_paths, band_half)
        out = np.abs(shares - target) > hw
        # move to the nearest edge of the band (Whalley-Wilmott), or to the target with no band
        new = np.where(out, np.where(shares < target, target - hw, target + hw), shares)
        d = new - shares
        cash = cash - d * S[:, i] - cost * np.abs(d) * S[:, i]
        costs = costs + cost * np.abs(d) * S[:, i]
        trades = trades + out
        shares = new
    payoff = np.maximum(cp * (S[:, -1] - K), 0.0)
    pnl = cash + shares * S[:, -1] - cost * np.abs(shares) * S[:, -1] + position * payoff
    costs = costs + cost * np.abs(shares) * S[:, -1]
    return {"pnl": pnl, "cost": costs, "trades": trades}


# ---------------------------------------------------------------------------
# Part 11's expansion: the P&L explain, smiles from three quotes, markouts, the inventory problem, Greek hedges
# ---------------------------------------------------------------------------
def pnl_explain(legs, S0, S1, sig0, sig1, dt) -> dict:
    """A day's P&L of a book split into its Taylor terms: delta, gamma, theta, vega, vanna, volga, and what they
    miss.  ``sig0``/``sig1`` are each leg's implied vol before and after (a number, or one per leg)."""
    s0 = np.broadcast_to(np.asarray(sig0, float), (len(legs),))
    s1 = np.broadcast_to(np.asarray(sig1, float), (len(legs),))
    out = {k: 0.0 for k in ("delta", "gamma", "theta", "vega", "vanna", "volga", "actual")}
    dS = S1 - S0
    for leg, a, b in zip(legs, s0, s1):
        g = bs.greeks(S0, leg.K, leg.T, a, 0.0, 0.0, leg.cp)
        ds = b - a
        terms = {"delta": g["delta"] * dS, "gamma": 0.5 * g["gamma"] * dS ** 2, "theta": g["theta"] * dt,
                 "vega": g["vega"] * ds, "vanna": g["vanna"] * dS * ds, "volga": 0.5 * g["volga"] * ds ** 2,
                 "actual": bs.price(S1, leg.K, leg.T - dt, b, 0.0, 0.0, leg.cp) - g["price"]}
        for k, v in terms.items():
            out[k] += leg.qty * float(v)
    out["explained"] = sum(out[k] for k in ("delta", "gamma", "theta", "vega", "vanna", "volga"))
    out["unexplained"] = out["actual"] - out["explained"]
    return out


def delta_strike(F, T, iv_fn, delta, cp=1, lo=None, hi=None, tol=1e-10) -> float:
    """The strike whose Black (forward) delta is ``delta`` on a smile ``iv_fn(k)`` (k = ln K/F): a 25-delta call is
    delta_strike(F, T, iv, 0.25), a 25-delta put delta_strike(F, T, iv, -0.25, cp=-1).  Bisection in k."""
    from scipy.special import ndtr

    def dlt(k):
        s = float(iv_fn(k))
        d1 = (-k + 0.5 * s * s * T) / (s * np.sqrt(T))
        return cp * ndtr(cp * d1)

    a, b = (-3.0, 3.0) if lo is None else (lo, hi)
    for _ in range(200):  # call delta falls in k; put delta (negative) falls in k too
        m = 0.5 * (a + b)
        if dlt(m) > delta:
            a = m
        else:
            b = m
        if b - a < tol:
            break
    return float(F * np.exp(0.5 * (a + b)))


def vanna_volga(K, F, T, strikes3, vols3, atm_vol) -> np.ndarray:
    """Castagna and Mercurio's (2007) vanna-volga smile: the Black price at the flat ``atm_vol`` plus the market's
    over-price of three pillar options, weighted to match the strike's vega, vanna and volga.  Returns the implied
    vol of that price at each strike in ``K`` (exactly the market vol at the pillars)."""
    K = np.atleast_1d(np.asarray(K, float))
    k3 = np.asarray(strikes3, float)
    g3 = bs.greeks(F, k3, T, atm_vol)
    A = np.vstack([g3["vega"], g3["vanna"], g3["volga"]])
    gap = bs.price(F, k3, T, np.asarray(vols3, float)) - bs.price(F, k3, T, atm_vol)
    out = np.empty(len(K))
    for j, k in enumerate(K):
        g = bs.greeks(F, k, T, atm_vol)
        x = np.linalg.solve(A, np.array([float(g["vega"]), float(g["vanna"]), float(g["volga"])]))
        c = float(bs.price(F, k, T, atm_vol)) + float(x @ gap)
        out[j] = bs.implied_vol(c, F, k, T, 0.0, 0.0, 1)
    return out


def markouts(ts, sign, price, mark, index, delta, vega, horizons=(300, 1800, 3600)) -> dict:
    """The maker's side of one instrument's trades (taker ``sign`` +1 buy, -1 sell; prices in units of the index):
    the edge against the exchange's mark at the trade, and the delta-hedged markout at the first later print past
    each horizon (NaN when there is none), all in vol points (dollars over vega per vol point)."""
    edge = sign * (price - mark) * index / vega        # takers buy above the mark: the maker sells there
    out = {"edge": edge}
    for h in horizons:
        k = np.searchsorted(ts, ts + h)
        kk = np.minimum(k, len(ts) - 1)
        dv = mark[kk] * index[kk] - price * index          # the option's move, marked later
        dh = delta * (index[kk] - index)                   # what the maker's delta hedge made meanwhile
        out[h] = np.where(k < len(ts), -sign * (dv - dh) / vega, np.nan)
    return out


def _mm_model(Q, A, k, offs, phi):
    qs = np.arange(-Q, Q + 1)
    offs = np.asarray(offs, float)
    p = np.minimum(A * np.exp(-k * offs), 1.0)
    acts = [(b, a) for b in range(len(offs)) for a in range(len(offs))]
    n = 2 * Q + 1
    # per state and action: fill probabilities (a client arrives on each side with probability 1/2), reward
    pb = np.array([[0.5 * p[b] if q < Q else 0.0 for b, a in acts] for q in qs])
    pa = np.array([[0.5 * p[a] if q > -Q else 0.0 for b, a in acts] for q in qs])
    r = pb * offs[[b for b, _ in acts]] + pa * offs[[a for _, a in acts]] - phi * (qs ** 2)[:, None]
    return qs, offs, acts, n, pb, pa, r


def mm_policy_value(policy, Q=10, A=0.45, k=1.5, offs=(0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0), phi=0.02,
                    disc=0.995) -> np.ndarray:
    """The discounted value of a quoting policy (one action index per inventory) in the inventory game: solve
    (I - disc P) V = r."""
    qs, offs, acts, n, pb, pa, r = _mm_model(Q, A, k, offs, phi)
    P = np.zeros((n, n))
    rr = np.zeros(n)
    for i, a in enumerate(policy):
        P[i, min(i + 1, n - 1)] += pb[i, a]
        P[i, max(i - 1, 0)] += pa[i, a]
        P[i, i] += 1 - pb[i, a] - pa[i, a]
        rr[i] = r[i, a]
    return np.linalg.solve(np.eye(n) - disc * P, rr)


def mm_value_iteration(Q=10, A=0.45, k=1.5, offs=(0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0), phi=0.02, disc=0.995,
                       tol=1e-10) -> dict:
    """The options market maker's inventory game, solved exactly: inventory q in [-Q, Q] (vega units); each step a
    client arrives at the bid or the ask (probability 1/2 each) and trades with probability A exp(-k offset); the
    reward is the offset earned minus phi q^2 (the running inventory penalty of Cartea and Jaimungal).  Returns the
    value function, the optimal policy (bid and ask offsets) and its skew (bid offset minus ask offset)."""
    qs, offs, acts, n, pb, pa, r = _mm_model(Q, A, k, offs, phi)
    V = np.zeros(n)
    up, dn = np.minimum(np.arange(n) + 1, n - 1), np.maximum(np.arange(n) - 1, 0)
    for _ in range(100000):
        Qv = r + disc * (pb * V[up][:, None] + pa * V[dn][:, None] + (1 - pb - pa) * V[:, None])
        Vn = Qv.max(1)
        if np.max(np.abs(Vn - V)) < tol:
            V = Vn
            break
        V = Vn
    pol = Qv.argmax(1)
    bid = offs[[acts[a][0] for a in pol]]
    ask = offs[[acts[a][1] for a in pol]]
    return {"q": qs, "V": V, "policy": pol, "bid": bid, "ask": ask, "skew": bid - ask, "acts": acts}


def mm_q_learning(steps=800_000, seed=0, checkpoints=(), Q=10, A=0.45, k=1.5,
                  offs=(0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0), phi=0.02, disc=0.995, restart=200, eps_end=0.1,
                  eps_steps=300_000) -> dict:
    """Tabular Q-learning on the same game, from simulated clients only (it never sees A, k or phi): epsilon-greedy,
    a step size 1/(1 + visits)^0.6, and a random restart of the inventory every ``restart`` steps (exploring starts,
    so rarely visited inventories are seen).  Returns the greedy policy at each checkpoint."""
    qs, offs, acts, n, pb, pa, r = _mm_model(Q, A, k, offs, phi)
    g = np.random.default_rng(seed)
    Qt = np.zeros((n, len(acts)))
    N = np.zeros_like(Qt)
    i, snaps = Q, {}
    ck = set(int(c) for c in checkpoints)
    for s in range(steps + 1):
        if s in ck:
            snaps[s] = Qt.argmax(1).copy()
        if s % restart == 0:
            i = int(g.integers(n))
        eps = max(eps_end, 1 - s / eps_steps)
        a = int(g.integers(len(acts))) if g.random() < eps else int(Qt[i].argmax())
        u, f = g.random(), g.random()
        j = i
        rew = -phi * qs[i] ** 2
        if u < 0.5:
            if f < 2 * pb[i, a]:
                rew += offs[acts[a][0]]
                j = i + 1
        elif f < 2 * pa[i, a]:
            rew += offs[acts[a][1]]
            j = i - 1
        N[i, a] += 1
        Qt[i, a] += (rew + disc * Qt[j].max() - Qt[i, a]) / (1 + N[i, a]) ** 0.6
        i = j
    return {"snapshots": snaps, "Q": Qt, "policy": Qt.argmax(1)}


def glft_quotes(q, A, k, phi):
    """Gueant, Lehalle and Fernandez-Tapia's (2013) closed-form approximation, in its risk-neutral limit with a running
    inventory penalty phi q^2 (Gueant 2017): bid and ask offsets 1/k +/- (2q +/- 1)/2 sqrt(phi e / (A k)).  Long
    inventory (q > 0) widens the bid and tightens the ask: both quotes move down."""
    q = np.asarray(q, float)
    c = np.sqrt(phi * np.e / (A * k))
    return {"bid": 1 / k + (q + 0.5) * c, "ask": 1 / k - (q - 0.5) * c, "skew": (2 * q) * c}


def greek_hedge(book: dict, instruments) -> dict:
    """Quantities of two hedge options that zero the book's gamma and vega (a 2x2 solve), then shares that zero the
    delta of the whole.  ``book`` and each instrument are dicts of greeks (``delta``, ``gamma``, ``vega``)."""
    i1, i2 = instruments
    M = np.array([[i1["gamma"], i2["gamma"]], [i1["vega"], i2["vega"]]], float)
    n1, n2 = np.linalg.solve(M, -np.array([book["gamma"], book["vega"]], float))
    n0 = -(book["delta"] + n1 * i1["delta"] + n2 * i2["delta"])
    return {"n1": float(n1), "n2": float(n2), "shares": float(n0)}
