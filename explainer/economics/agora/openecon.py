"""Agora's open economy (Part 34): what sets the price of one money in terms of another.  Purchasing power parity
and its half-life; the Balassa-Samuelson slope; uncovered interest parity and Fama's regression; the carry trade;
Meese and Rogoff's horse race; exchange-rate pass-through by distributed lags; the Mundell-Fleming small open
economy under fixed and floating rates; Dornbusch's overshooting; first-generation (Krugman, Flood and Garber) and
second-generation (Obstfeld) currency crises.  numpy only."""

from __future__ import annotations

import numpy as np


# --- purchasing power parity ---------------------------------------------------------------------------------------
def real_rates(D: dict, base: str = "USA") -> dict:
    """Log real exchange rates against ``base`` from the JST database: q = log(local per dollar) + log(P_us) -
    log(P_local); higher q means the local currency is cheaper in real terms.  ``{iso: (years, q)}``."""
    iso = np.array(D["iso"])
    yr = np.array(D["year"], int)
    cpi = np.array(D["cpi"], float)
    xr = np.array(D["xrusd"], float)
    us = {int(y): c for y, c, i in zip(yr, cpi, iso) if i == base}
    out = {}
    for c in sorted(set(iso) - {base}):
        m = iso == c
        y = yr[m]
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.log(xr[m]) + np.log([us.get(int(t), np.nan) for t in y]) - np.log(cpi[m])
        out[c] = (y, q)
    return out


def ppp_halflife(R: dict, first: int, last: int) -> dict:
    """The pooled AR(1) coefficient of real exchange rates, each demeaned over ``first``-``last`` (country effects),
    and the half-life ln(1/2)/ln(rho) in years; by country too."""
    X, Y, by = [], [], {}
    for c, (y, q) in R.items():
        k = (y >= first) & (y <= last)
        qq = q[k] - np.nanmean(q[k])
        a, b = qq[:-1], qq[1:]
        ok = np.isfinite(a) & np.isfinite(b)
        X += list(a[ok])
        Y += list(b[ok])
        if ok.sum() > 10:
            rho_c = float(a[ok] @ b[ok] / (a[ok] @ a[ok]))
            by[c] = float(np.log(0.5) / np.log(rho_c)) if 0 < rho_c < 1 else float("inf")
    X, Y = np.array(X), np.array(Y)
    rho = float(X @ Y / (X @ X))
    return {"rho": rho, "halflife": float(np.log(0.5) / np.log(rho)), "n": len(X), "by_country": by}


def balassa_samuelson(log_gdp, valuation) -> dict:
    """The slope of currencies' over- or undervaluation against the dollar on log GDP per head."""
    x, y = np.asarray(log_gdp, float), np.asarray(valuation, float)
    b = np.polyfit(x, y, 1)
    return {"slope": float(b[0]), "intercept": float(b[1]), "corr": float(np.corrcoef(x, y)[0, 1]), "n": len(x)}


# --- interest parity -------------------------------------------------------------------------------------------------
def fama(ls: dict, i_home: dict, i_for: dict, h: int = 3, first: str = "1979-01") -> dict:
    """Fama's regression: the change in the log price of the foreign currency (in dollars) over the next ``h`` months
    on the interest differential (home minus foreign, at the horizon's rate).  Uncovered interest parity says the
    slope is one: high-rate currencies should be expected to fall by the rate gap.  Inputs keyed "YYYY-MM"."""
    ks = sorted(k for k in ls if k >= first)
    X, Y = [], []
    for j, k in enumerate(ks[:-h]):
        k2 = ks[j + h]
        if k in i_home and k in i_for:
            X.append((i_home[k] - i_for[k]) / 100 * h / 12)
            Y.append(ls[k2] - ls[k])
    X, Y = np.array(X), np.array(Y)
    Z = np.column_stack([np.ones(len(X)), X])
    b, *_ = np.linalg.lstsq(Z, Y, rcond=None)
    e = Y - Z @ b
    # Newey-West standard error with h-1 lags (overlapping horizons)
    S = (Z * e[:, None]).T @ (Z * e[:, None])
    for L in range(1, h):
        w = 1 - L / h
        G = (Z[L:] * e[L:, None]).T @ (Z[:-L] * e[:-L, None])
        S += w * (G + G.T)
    Q = np.linalg.inv(Z.T @ Z)
    V = Q @ S @ Q
    return {"beta": float(b[1]), "se": float(np.sqrt(V[1, 1])), "n": len(X)}


def carry(ls: dict, rates: dict, i_us: dict, first: str = "1985-01", k: int = 2) -> dict:
    """The carry trade, monthly: hold the ``k`` highest-yielding currencies (the dollar included), funded by the ``k``
    lowest; the excess return is the interest differential plus the change in the currencies' values."""
    months = sorted(i_us)
    out = []
    for j, m in enumerate(months[:-1]):
        m2 = months[j + 1]
        if m < first:
            continue
        r, ret = {"US": i_us[m]}, {"US": i_us[m] / 1200}
        for c in ls:
            if m in rates[c] and m in ls[c] and m2 in ls[c]:
                r[c] = rates[c][m]
                ret[c] = rates[c][m] / 1200 + ls[c][m2] - ls[c][m]
        if len(r) < 2 * k + 2:
            continue
        o = sorted(r, key=r.get)
        out.append((m2, float(np.mean([ret[c] for c in o[-k:]]) - np.mean([ret[c] for c in o[:k]]))))
    x = np.array([v for _, v in out])
    return {"months": [m for m, _ in out], "returns": x.tolist(), "mean": float(12 * x.mean()),
            "sd": float(np.sqrt(12) * x.std()), "sharpe": float(np.sqrt(12) * x.mean() / x.std()),
            "skew": float(((x - x.mean()) ** 3).mean() / x.std() ** 3),
            "worst": min(out, key=lambda t: t[1]), "cumulative": np.cumsum(x).tolist()}


def horse_race(series: dict, rates: dict, i_us: dict, h: int, window: int = 120) -> dict:
    """Meese and Rogoff's test, out of sample: for each currency and month after the first ``window``, forecast the
    log rate ``h`` months ahead by (i) no change, (ii) uncovered interest parity (the rate gap), and (iii) an AR(1) in
    monthly changes fitted on the past ``window`` months; root mean squared errors, in percent."""
    err = {"random walk": [], "interest parity": [], "AR(1)": []}
    for c, s in series.items():
        ks = sorted(s)
        x = np.array([s[k] for k in ks])
        for t in range(window, len(ks) - h):
            if not (ks[t] in rates[c] and ks[t] in i_us):
                continue
            actual = x[t + h] - x[t]
            d = np.diff(x[t - window:t + 1])
            rho = float(d[:-1] @ d[1:] / (d[:-1] @ d[:-1]))
            err["random walk"].append(actual ** 2)
            err["interest parity"].append((actual - (i_us[ks[t]] - rates[c][ks[t]]) / 100 * h / 12) ** 2)
            err["AR(1)"].append((actual - sum(rho ** j for j in range(1, h + 1)) * d[-1]) ** 2)
    rm = {k: float(100 * np.sqrt(np.mean(v))) for k, v in err.items()}
    return {"rmse": rm, "ratio": {k: v / rm["random walk"] for k, v in rm.items()}, "n": len(err["random walk"])}


# --- pass-through ----------------------------------------------------------------------------------------------------
def passthrough(dlog_p, dlog_e, lags: int = 12) -> dict:
    """Distributed-lag pass-through: regress the monthly change in log import prices on the current and ``lags``
    lagged changes in the log exchange rate; the cumulative sums of the coefficients by horizon."""
    p, e = np.asarray(dlog_p, float), np.asarray(dlog_e, float)
    n = len(p)
    X = np.column_stack([np.ones(n - lags)] + [e[lags - j:n - j] for j in range(lags + 1)])
    y = p[lags:]
    ok = np.all(np.isfinite(X), axis=1) & np.isfinite(y)
    b, *_ = np.linalg.lstsq(X[ok], y[ok], rcond=None)
    cum = np.cumsum(b[1:])
    return {"cumulative": cum.tolist(), "long_run": float(cum[-1]), "impact": float(cum[0]), "n": int(ok.sum())}


# --- Mundell-Fleming -------------------------------------------------------------------------------------------------
MF = {"a": 0.5, "b": 0.6, "c": 0.4, "k": 0.5, "h": 0.8}


def mundell_fleming(regime: str, dg: float = 0.0, dm: float = 0.0, **kw) -> dict:
    """A small open economy with perfect capital mobility (r = r*), in deviations: IS  y = a y + g - b r + c e (e the
    price of foreign currency, up = cheaper home goods), LM  m = k y - h r.  Floating: m is set, e adjusts. Fixed: e
    is set, m adjusts (the central bank buys or sells reserves).  Returns the changes in output, the exchange rate and
    the money stock."""
    p = {**MF, **kw}
    a, c, k = p["a"], p["c"], p["k"]
    if regime == "floating":
        y = dm / k                                  # LM alone pins output when r = r*
        e = ((1 - a) * y - dg) / c
        return {"y": y, "e": e, "m": dm}
    y = dg / (1 - a)                                # e fixed: the IS curve alone; money follows
    return {"y": y, "e": 0.0, "m": k * y}


# --- overshooting ----------------------------------------------------------------------------------------------------
def dornbusch(dm: float = 0.10, lam: float = 4.0, theta: float = 0.5, T: float = 8.0, n: int = 161) -> dict:
    """Dornbusch (1976): prices are sticky, asset markets fast.  After a permanent rise ``dm`` in money, the long-run
    exchange rate and price level rise by dm.  Money-market equilibrium with p fixed at impact needs the interest rate
    to fall by dm/lam; interest parity then needs the currency expected to appreciate at that rate, so it must first
    depreciate beyond its long-run level: s(0) - s_bar = dm/(lam*theta), converging at rate theta.  Paths of s, p and
    i (deviations from the old steady state)."""
    t = np.linspace(0, T, n)
    gap0 = dm / (lam * theta)
    s = dm + gap0 * np.exp(-theta * t)
    pgap = -dm * np.exp(-theta * t)                 # p - p_bar: starts dm below its new level
    p = dm + pgap
    i = -(dm - p) / lam
    return {"t": t.tolist(), "s": s.tolist(), "p": p.tolist(), "i": i.tolist(), "jump": float(dm + gap0),
            "overshoot": float(gap0), "factor": float(1 + 1 / (lam * theta)), "lam": lam, "theta": theta}


# --- currency crises -------------------------------------------------------------------------------------------------
def krugman_attack(peg: float = 100.0, d0: float = 60.0, mu: float = 2.0, alpha: float = 5.0, T: float = 25.0,
                   n: int = 501) -> dict:
    """The first-generation crisis (Krugman 1979; Flood and Garber 1984), in levels: money = domestic credit d +
    reserves r; with purchasing power parity the price level is the exchange rate s, and money demand is m = s -
    alpha * E[ds/dt].  Credit grows at mu to pay a deficit.  Under the peg reserves fall steadily; once floating, s =
    d + alpha mu, the shadow rate.  Speculators attack when the shadow rate reaches the peg, T = (peg - alpha mu -
    d0)/mu, before reserves would have run out unaided at (peg - d0)/mu; reserves fall by alpha mu at once."""
    t = np.linspace(0, T, n)
    d = d0 + mu * t
    shadow = d + alpha * mu
    T_attack = (peg - alpha * mu - d0) / mu
    T_exhaust = (peg - d0) / mu
    reserves = np.where(t < T_attack, peg - d, 0.0)
    s = np.where(t < T_attack, peg, shadow)
    return {"t": t.tolist(), "reserves": reserves.tolist(), "shadow": shadow.tolist(), "s": s.tolist(),
            "T_attack": float(T_attack), "T_exhaust": float(T_exhaust), "jump_reserves": float(alpha * mu),
            "peg": peg}


def obstfeld_regions(cost: float = 1.0, gamma: float = 1.0, delta: float = 0.5) -> dict:
    """Second-generation crises (Obstfeld 1996), in a simple form: a government abandons the peg when the loss of
    defending it, (u + gamma * x)^2, exceeds a fixed cost of abandoning, ``cost``; u is the slack in the economy and x
    the devaluation markets expect, which raises the interest rate a defence needs.  If markets expect no devaluation
    (x = 0) the government defends while u < sqrt(cost); if they expect one of ``delta`` it gives up once u > sqrt(cost)
    - gamma delta.  Between the two thresholds both outcomes are equilibria: the attack succeeds because it is
    expected."""
    hi = float(np.sqrt(cost))
    lo = float(hi - gamma * delta)
    return {"safe_below": lo, "doomed_above": hi, "cost": cost, "gamma": gamma, "delta": delta}


def obstfeld_outcome(u: float, expect: bool, cost: float = 1.0, gamma: float = 1.0, delta: float = 0.5) -> str:
    """"defend" or "abandon" for slack ``u`` and the market's expectation."""
    x = delta if expect else 0.0
    return "abandon" if (u + gamma * x) ** 2 > cost else "defend"
