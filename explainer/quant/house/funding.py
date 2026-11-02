"""The House's treasury and funding desk (Part 2, *The Machinery of Markets*): what it costs, in cash and collateral,
to hold a position, and what the market's plumbing does with an order.  Every later backtest charges these.

* :func:`margin_account`: a leveraged futures or perpetual position marked to market bar by bar, with variation
  margin, funding payments and the exchange's liquidation rule;
* :func:`netting`: what a central counterparty saves: gross, bilateral-net and multilateral-net obligations of a
  set of trades;
* :func:`call_auction`: the single clearing price of an opening or closing auction (the price that executes the most);
* :func:`fund_fees`: management and performance fees with a high-water mark, period by period;
* :func:`max_leverage`: the leverage a repo or margin haircut allows.
"""

from __future__ import annotations

import numpy as np


def margin_account(prices, qty: float, leverage: float, maintenance: float, funding=None, fee: float = 0.0) -> dict:
    """A position of ``qty`` units (negative: short) opened at ``prices[0]`` with initial margin notional / leverage.
    Each bar the account gains qty * dP (variation margin) and pays ``funding[i]`` * notional (positive funding:
    longs pay shorts).  Liquidated at the first bar where equity < ``maintenance`` * notional: the account is closed
    at that bar's price, and whatever equity is left (possibly negative, absorbed by the exchange's insurance fund) is
    reported.  ``fee``: a trading fee per unit of notional, paid on opening."""
    p = np.asarray(prices, float)
    n = len(p)
    f = np.zeros(n) if funding is None else np.asarray(funding, float)
    notional0 = abs(qty) * p[0]
    margin0 = notional0 / leverage
    equity = np.empty(n)
    equity[0] = margin0 - fee * notional0
    paid_funding = 0.0
    liq = None
    for i in range(1, n):
        pay = f[i] * qty * p[i - 1]
        paid_funding += pay
        equity[i] = equity[i - 1] + qty * (p[i] - p[i - 1]) - pay
        if equity[i] < maintenance * abs(qty) * p[i]:
            liq = i
            equity[i + 1:] = np.nan
            break
    req = maintenance * abs(qty) * p
    return {"equity": equity, "maintenance_req": req, "initial_margin": margin0, "liquidated_at": liq,
            "funding_paid": paid_funding, "left": float(equity[liq]) if liq is not None else float(equity[-1])}


def liquidation_price(entry: float, leverage: float, maintenance: float, side: int = 1) -> float:
    """The price at which a fresh position opened at ``entry`` with margin entry/leverage hits the maintenance level
    (no funding, no fees): for a long, P (1 - m) = entry (1 - 1/L); for a short, P (1 + m) = entry (1 + 1/L)."""
    if side > 0:
        return entry * (1 - 1 / leverage) / (1 - maintenance)
    return entry * (1 + 1 / leverage) / (1 + maintenance)


def netting(payer, receiver, amount, n: int) -> dict:
    """Obligations among ``n`` members from trades (payer i owes receiver j ``amount``): the gross total, the total
    after each pair nets its trades (bilateral), and after a central counterparty nets everything (each member owes or
    is owed only its net position)."""
    payer, receiver, amount = map(np.asarray, (payer, receiver, amount))
    gross = float(amount.sum())
    M = np.zeros((n, n))
    np.add.at(M, (payer, receiver), amount)
    bilateral = float(np.abs(np.triu(M - M.T, 1)).sum())
    net = M.sum(axis=1) - M.sum(axis=0)
    multilateral = float(net[net > 0].sum())
    return {"gross": gross, "bilateral": bilateral, "multilateral": multilateral, "net_position": net}


def call_auction(bid_px, bid_qty, ask_px, ask_qty) -> dict:
    """The clearing price of a call auction: at each candidate price, demand = bids at or above it, supply = asks at
    or below it; the price that maximizes the executed volume min(demand, supply), ties broken by the smallest
    imbalance and then the midpoint of the tied prices."""
    bp, bq, ap, aq = map(lambda x: np.asarray(x, float), (bid_px, bid_qty, ask_px, ask_qty))
    cands = np.unique(np.concatenate([bp, ap]))
    demand = np.array([bq[bp >= c].sum() for c in cands])
    supply = np.array([aq[ap <= c].sum() for c in cands])
    vol = np.minimum(demand, supply)
    best = vol.max()
    m = vol == best
    imb = np.abs(demand - supply)
    m &= imb == imb[m].min()
    price = float(np.mean(cands[m]))
    return {"price": price, "volume": float(best), "candidates": cands, "demand": demand, "supply": supply}


def fund_fees(gross_returns, mgmt: float = 0.02, perf: float = 0.20, periods_per_year: int = 1) -> dict:
    """Net returns of a fund charging ``mgmt`` a year on assets and ``perf`` of gains above its high-water mark,
    period by period (fees crystallized each period).  Returns net returns, fees per period, and the high-water mark."""
    g = np.asarray(gross_returns, float)
    nav, hwm = 1.0, 1.0
    net, fees, marks = [], [], []
    for r in g:
        before = nav * (1 + r) - nav * mgmt / periods_per_year
        pf = perf * max(before - hwm, 0.0)
        after = before - pf
        fees.append((nav * (1 + r) - after) / nav)
        net.append(after / nav - 1)
        nav = after
        hwm = max(hwm, nav)
        marks.append(hwm)
    return {"net": np.array(net), "fees": np.array(fees), "hwm": np.array(marks), "nav": nav}


def max_leverage(haircut: float) -> float:
    """With a haircut h, every dollar of collateral funds 1 - h dollars of borrowing: repeated, a dollar of equity
    supports at most 1/h dollars of assets."""
    return 1.0 / haircut


# ---------------------------------------------------------------------------
# Part 2, expanded: hedging with futures, margin models, the waterfall, shorts, deleveraging, smoothing
# ---------------------------------------------------------------------------
def min_var_hedge(dS, dF) -> tuple[float, float]:
    """The minimum-variance hedge ratio h* = Cov(dS, dF) / Var(dF) of a position whose changes are ``dS`` hedged with
    a future whose changes are ``dF``, and its effectiveness: the share of the variance the hedge removes (rho^2
    in sample)."""
    dS, dF = np.asarray(dS, float), np.asarray(dF, float)
    c = np.cov(dS, dF)
    h = c[0, 1] / c[1, 1]
    resid = dS - h * dF
    return float(h), float(1 - resid.var() / dS.var())


def hedge_effectiveness(dS, dF, h: float) -> float:
    """The share of the variance of ``dS`` that a hedge of ``h`` futures per unit removes (out of sample: may be
    negative)."""
    dS, dF = np.asarray(dS, float), np.asarray(dF, float)
    return float(1 - (dS - h * dF).var() / dS.var())


def implied_carry(F, S, tau) -> np.ndarray:
    """The annualized carry a future implies: r - q = ln(F / S) / tau, ``tau`` in years to expiry (F = S e^{(r-q)tau})."""
    return np.log(np.asarray(F, float) / np.asarray(S, float)) / np.asarray(tau, float)


def ewma_var(r, lam: float = 0.97, v0: float | None = None) -> np.ndarray:
    """The EWMA variance known before day t: v_t = lam v_{t-1} + (1 - lam) r_{t-1}^2 (RiskMetrics), started at
    ``v0`` (default: the variance of the first 20 returns)."""
    r = np.asarray(r, float)
    v = np.empty(len(r))
    v[0] = r[:20].var() if v0 is None else v0
    for t in range(1, len(r)):
        v[t] = lam * v[t - 1] + (1 - lam) * r[t - 1] ** 2
    return v


def ewma_margin(r, lam: float = 0.97, z: float = 2.326, h: float = 2.0, v0: float | None = None) -> np.ndarray:
    """Initial margin per unit of notional for day t, from returns up to t - 1: z sigma_t sqrt(h), a Gaussian VaR at
    the confidence z (2.326: 99%) over a close-out of ``h`` days, with sigma_t from :func:`ewma_var`."""
    return z * np.sqrt(h * ewma_var(r, lam, v0))


def ewma_loglik(r, lam: float) -> float:
    """The Gaussian log-likelihood of returns ``r`` under EWMA variances: -1/2 sum(ln v_t + r_t^2 / v_t)."""
    r = np.asarray(r, float)
    v = ewma_var(r, lam)
    return float(-0.5 * np.sum(np.log(v[20:]) + r[20:] ** 2 / v[20:]))


def fit_ewma_lambda(r, lo: float = 0.80, hi: float = 0.999, iters: int = 30) -> dict:
    """Maximum-likelihood lambda by golden-section search on [lo, hi]; ``path`` is the sequence of midpoints the
    search visited (for replaying the fit), ``loglik`` their log-likelihoods."""
    g = (np.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = ewma_loglik(r, c), ewma_loglik(r, d)
    path, ll = [], []
    for _ in range(iters):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = ewma_loglik(r, c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = ewma_loglik(r, d)
        m = (a + b) / 2
        path.append(m)
        ll.append(ewma_loglik(r, m))
    return {"lam": float((a + b) / 2), "path": np.array(path), "loglik": np.array(ll)}


def kupiec(breaches: int, T: int, p: float = 0.01) -> dict:
    """Kupiec's unconditional coverage test: x breaches in T days against a nominal rate p.
    LR = -2 ln[(1-p)^(T-x) p^x / ((1-ph)^(T-x) ph^x)], chi-squared with one degree of freedom under the null."""
    from scipy.stats import chi2
    x, T = int(breaches), int(T)
    ph = x / T
    ll0 = (T - x) * np.log(1 - p) + x * np.log(p)
    ll1 = (T - x) * np.log(1 - ph) + (x * np.log(ph) if x > 0 else 0.0)
    lr = float(-2 * (ll0 - ll1))
    return {"rate": ph, "LR": lr, "p_value": float(chi2.sf(lr, 1))}


def liquidation_probability(leverage, horizon_days, sigma_daily: float, maintenance: float = 0.005) -> np.ndarray:
    """The chance a long opened with ``leverage`` is liquidated within ``horizon_days``, if the log price is a
    driftless Brownian motion with daily volatility ``sigma_daily``: by the reflection principle,
    P(min X <= -d) = 2 Phi(-d / (sigma sqrt(H))), with d = -ln(P_liq / P_0)."""
    from scipy.stats import norm
    L = np.asarray(leverage, float)
    H = np.asarray(horizon_days, float)
    d = -np.log((1 - 1 / L) / (1 - maintenance))
    return 2 * norm.cdf(-d / (sigma_daily * np.sqrt(H)))


def ccp_waterfall(loss, layers) -> np.ndarray:
    """A defaulter's uncovered losses run down a clearing house's default waterfall: ``layers`` are the sizes of the
    layers in order (the defaulter's margin, its default-fund contribution, the CCP's own capital, the survivors'
    default fund, assessments).  Returns, for each loss (rows), what each layer absorbs (columns) and, in the last
    column, what is left over (which the CCP would allocate by variation-margin haircuts)."""
    loss = np.atleast_1d(np.asarray(loss, float))
    caps = np.cumsum(np.concatenate([[0.0], np.asarray(layers, float)]))
    taken = np.clip(loss[:, None] - caps[None, :-1], 0, np.diff(caps)[None, :])
    left = np.maximum(loss - caps[-1], 0)
    return np.column_stack([taken, left])


def short_pnl(S0: float, ST: float, r: float, fee: float, T: float, dividends: float = 0.0,
              collateral: float = 1.02) -> float:
    """A short sale's profit per share: the price fall, plus the rebate the lender pays on the cash collateral
    (``collateral`` x S0 earning r - fee for T years: negative when the fee exceeds the rate, as for specials), less
    the dividends the short seller must pay the lender."""
    return float((S0 - ST) + collateral * S0 * (r - fee) * T - dividends)


def deleverage(E: float, A: float, h_new: float, impact: float, rounds: int = 60) -> dict:
    """A fund with equity ``E`` and assets ``A`` (units at price 1, debt A - E) whose haircut rises to ``h_new`` must
    cut its assets to E / h_new; each unit sold lowers the price by ``impact`` (a fraction per unit), which cuts E and
    forces more sales.  Returns the rounds of selling: ``sold`` per round, ``price``, ``equity``; ``amplification`` is
    the total sold over the first round's sale (1 / (1 - loop gain) for small impact)."""
    q, p, D = A, 1.0, A - E
    sold, price, equity = [], [p], [E]
    for _ in range(rounds):
        e = q * p - D
        if e <= 0:
            break
        s = max(q - e / (h_new * p), 0.0)
        if s < 1e-9 * A:
            break
        p_new = p * (1 - impact * s)
        D -= s * p_new          # the sale repays debt at the price it moved to
        q -= s
        p = p_new
        sold.append(s)
        price.append(p)
        equity.append(q * p - D)
    sold = np.array(sold)
    return {"sold": sold, "price": np.array(price), "equity": np.array(equity),
            "amplification": float(sold.sum() / sold[0]) if len(sold) else 0.0}


def fire_sale(K: int, q: float, lam: float, kind: str = "linear") -> np.ndarray:
    """K banks each sell ``q`` shares, one after another, into a market whose price falls by lam X (``linear``) or
    lam sqrt(X) (``sqrt``) after X shares sold in all. Returns each bank's loss against the starting price, in the
    order they sell: linear gives lam q^2 (j - 1/2) for the j-th."""
    out = []
    for j in range(1, K + 1):
        a, b = (j - 1) * q, j * q
        if kind == "linear":
            out.append(lam * (b * b - a * a) / 2)
        else:
            out.append(lam * (b ** 1.5 - a ** 1.5) * 2 / 3)
    return np.array(out)


def glm_smooth(R, theta) -> np.ndarray:
    """Getmansky-Lo-Makarov smoothing: reported R^o_t = sum_k theta_k R_{t-k} (theta sums to one); the first
    len(theta) - 1 values are dropped."""
    th = np.asarray(theta, float)
    return np.convolve(np.asarray(R, float), th, mode="valid")


def glm_fit(Ro, q: int = 2, record: bool = False) -> dict:
    """Fit the smoothing profile theta (length q + 1, summing to one) of reported returns ``Ro`` by Gaussian
    conditional maximum likelihood of the MA(q) process R^o_t = mu + theta_0 eta_t + ... + theta_q eta_{t-q}.
    ``path`` (with ``record``) holds theta after each optimizer iteration; ``theta_moment`` is the moment estimator
    from the first q autocorrelations, the baseline."""
    from scipy.optimize import minimize
    x = np.asarray(Ro, float)
    x = x - x.mean()

    def nll(b):
        from scipy.signal import lfilter
        if len(b) and np.any(np.abs(np.roots(np.r_[1.0, b])) >= 0.999):
            return 1e6  # non-invertible: outside the model
        e = lfilter([1.0], np.r_[1.0, b], x)  # innovations e_t = x_t - sum_k b_k e_{t-1-k}
        return 0.5 * len(e) * np.log(np.mean(e ** 2))

    path = []

    def to_theta(b):
        b = np.r_[1.0, b]
        return b / b.sum()

    cb = (lambda b: path.append(to_theta(b))) if record else None
    res = minimize(nll, np.zeros(q), method="BFGS", callback=cb)
    theta = to_theta(res.x)
    # the moment estimator: match the first q autocorrelations of an MA(q) with coefficients 1, b
    ac = np.array([np.corrcoef(x[:-k], x[k:])[0, 1] for k in range(1, q + 1)])

    def gap(b):
        c = np.r_[1.0, b]
        g0 = c @ c
        return sum((sum(c[i] * c[i + k] for i in range(q + 1 - k)) / g0 - ac[k - 1]) ** 2 for k in range(1, q + 1))
    mom = to_theta(minimize(gap, np.zeros(q), method="Nelder-Mead").x)
    return {"theta": theta, "theta_moment": mom, "path": np.array(path) if record else None,
            "smoothing_index": float(np.sum(theta ** 2))}
