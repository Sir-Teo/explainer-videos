"""The House's valuation tools (Part 3, *Value, Accounting and the Firm*): what a claim on future cash is worth.

* :func:`npv`, :func:`irr`: present value of dated cash flows, and the rate that makes it zero;
* :func:`annuity`, :func:`perpetuity`, :func:`gordon`: the closed forms;
* :func:`dcf`: a firm's value from explicit free cash flows plus a Gordon terminal value;
* :func:`wacc`, :func:`levered_beta`, :func:`mm_cost_of_equity`: the cost of capital and Modigliani-Miller;
* :func:`merton_equity`: equity as a call on the firm's assets (Merton 1974; Part 20);
* :func:`irr_bisect`, :func:`gordon_duration`, :func:`pv_weights`: the rate by bisection; the duration of equity;
* :func:`value_driver_tv`, :func:`residual_income`, :func:`pb_steady`, :func:`implied_rate`: the value driver,
  Ohlson's residual income, P/B, and the market's implied return;
* :func:`tax_shield`, :func:`apv`, :func:`miller_gain`: debt and taxes; :func:`campbell_shiller`: the dividend-yield
  decomposition; :func:`beneish_ratios`, :func:`beneish_m`: the forensic score.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize

from explainer.quant.house import bs


def npv(rate: float, cash_flows, times=None) -> float:
    """Present value at ``rate`` (annual, compounded yearly) of ``cash_flows`` paid at ``times`` (years; default 0,
    1, 2, ...)."""
    cf = np.asarray(cash_flows, float)
    t = np.arange(len(cf)) if times is None else np.asarray(times, float)
    return float(np.sum(cf / (1 + rate) ** t))


def irr(cash_flows, times=None, lo: float = -0.99, hi: float = 10.0) -> float:
    """The internal rate of return: the rate at which the NPV is zero (bracketed root; one sign change assumed)."""
    return float(optimize.brentq(lambda r: npv(r, cash_flows, times), lo, hi, xtol=1e-12))


def annuity(payment: float, rate: float, n: int) -> float:
    """Value today of ``payment`` at the end of each of ``n`` years: payment (1 - (1 + r)^-n) / r."""
    return payment * (1 - (1 + rate) ** -n) / rate


def perpetuity(payment: float, rate: float) -> float:
    return payment / rate


def gordon(next_payment: float, rate: float, growth: float) -> float:
    """A payment growing at ``growth`` forever, the first one a year from now: D1 / (r - g), for r > g."""
    if rate <= growth:
        return float("inf")
    return next_payment / (rate - growth)


def dcf(fcf, rate: float, terminal_growth: float) -> dict:
    """Value of explicit free cash flows (years 1..n) plus a Gordon terminal value at year n, all discounted at
    ``rate``.  Returns the total and its two parts (the terminal value usually dominates)."""
    f = np.asarray(fcf, float)
    n = len(f)
    pv_explicit = float(np.sum(f / (1 + rate) ** np.arange(1, n + 1)))
    tv = gordon(f[-1] * (1 + terminal_growth), rate, terminal_growth)
    pv_tv = tv / (1 + rate) ** n
    return {"value": pv_explicit + pv_tv, "explicit": pv_explicit, "terminal": pv_tv}


def wacc(equity: float, debt: float, cost_equity: float, cost_debt: float, tax: float = 0.0) -> float:
    v = equity + debt
    return equity / v * cost_equity + debt / v * cost_debt * (1 - tax)


def mm_cost_of_equity(r_assets: float, r_debt: float, debt_to_equity: float, tax: float = 0.0) -> float:
    """Modigliani-Miller's proposition II: r_E = r_A + (r_A - r_D)(1 - t) D/E."""
    return r_assets + (r_assets - r_debt) * (1 - tax) * debt_to_equity


def levered_beta(beta_assets: float, debt_to_equity: float, tax: float = 0.0, beta_debt: float = 0.0) -> float:
    return beta_assets + (beta_assets - beta_debt) * (1 - tax) * debt_to_equity


def merton_equity(assets, debt_face: float, T: float, sigma_assets: float, r: float = 0.0) -> dict:
    """Merton (1974): equity is a call on the firm's assets struck at the face value of its debt; debt is riskless
    debt minus a put.  Returns equity, debt, the credit spread on the debt, and the risk-neutral default probability."""
    A = np.asarray(assets, float)
    E = bs.price(A, debt_face, T, sigma_assets, r, 0.0, 1)
    D = A - E
    y = -np.log(D / debt_face) / T
    _, d2 = bs.d1_d2(A, debt_face, T, sigma_assets, r)
    from scipy.stats import norm

    return {"equity": E, "debt": D, "spread": y - r, "pd": norm.cdf(-d2)}


# ---------------------------------------------------------------------------
# Part 3, expanded: rates by bisection, duration, the value driver, residual income, the implied cost of capital,
# taxes and payout, Campbell-Shiller, and the forensic score
# ---------------------------------------------------------------------------
def irr_bisect(cash_flows, lo: float = 0.0, hi: float = 1.0, steps: int = 40) -> dict:
    """The IRR by bisection, keeping every bracket: halve [lo, hi], keep the half where NPV changes sign.  Returns
    the root and the list of (lo, hi) brackets (for a lab: the bracket shrinking step by step).  It finds one root
    of NPV(r) in the bracket; a project whose cash flows change sign more than once can have several."""
    f = lambda r: npv(r, cash_flows)  # noqa: E731
    flo = f(lo)
    if flo * f(hi) > 0:
        raise ValueError("NPV has the same sign at both ends of the bracket")
    brackets = [(lo, hi)]
    for _ in range(steps):
        mid = (lo + hi) / 2
        fm = f(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
        brackets.append((lo, hi))
    return {"root": (lo + hi) / 2, "brackets": brackets}


def gordon_duration(rate: float, growth: float) -> dict:
    """The duration of a Gordon stock, P = D1 / (r - g): modified duration -dlnP/dr = 1/(r - g), and Macaulay
    duration, the PV-weighted mean payment date, (1 + r)/(r - g)."""
    return {"modified": 1 / (rate - growth), "macaulay": (1 + rate) / (rate - growth)}


def pv_weights(rate: float, growth: float, horizon: int) -> np.ndarray:
    """The share of a Gordon stock's value paid in each year 1..horizon: (1 - q) q^(t-1), q = (1 + g)/(1 + r)."""
    q = (1 + growth) / (1 + rate)
    t = np.arange(1, horizon + 1)
    return (1 - q) * q ** (t - 1)


def value_driver_tv(nopat_next: float, growth: float, ronic: float, wacc_: float) -> float:
    """The value-driver (McKinsey) continuing value: NOPAT_{T+1} (1 - g/RONIC) / (WACC - g).  Growth needs
    reinvestment g/RONIC of NOPAT; it adds value only when RONIC > WACC."""
    return nopat_next * (1 - growth / ronic) / (wacc_ - growth)


def residual_income(book0: float, earnings, dividends, rate: float, terminal_growth: float | None = None) -> dict:
    """Ohlson (1995): value = book + PV of residual income E_t - r B_{t-1}, with book rolled forward by clean surplus
    B_t = B_{t-1} + E_t - D_t.  Optional Gordon terminal value on the last residual income.  Also returns the DDM
    value of the same dividends with the final book as a liquidating payment, which must agree (the identity)."""
    E = np.asarray(earnings, float)
    D = np.asarray(dividends, float)
    n = len(E)
    B = np.empty(n + 1)
    B[0] = book0
    for t in range(n):
        B[t + 1] = B[t] + E[t] - D[t]
    disc = (1 + rate) ** -np.arange(1, n + 1)
    ri = E - rate * B[:-1]
    v_ri = book0 + float(ri @ disc)
    v_ddm = float(D @ disc) + B[-1] * disc[-1]
    if terminal_growth is not None:  # an infinite horizon: the liquidating-book DDM check no longer applies
        v_ri += ri[-1] * (1 + terminal_growth) / (rate - terminal_growth) * disc[-1]
        v_ddm = None
    return {"value": v_ri, "ddm": v_ddm, "book": B, "ri": ri}


def pb_steady(roe: float, rate: float, growth: float) -> float:
    """Price-to-book of a firm with constant ROE whose book grows at g: 1 + (ROE - r)/(r - g)."""
    return 1 + (roe - rate) / (rate - growth)


def implied_rate(price: float, cf0: float, growth: float, growth_long: float, years: int = 5,
                 lo: float = None, hi: float = 0.5) -> float:
    """The discount rate that equates ``price`` with cash flows cf0 (1 + g)^t for t = 1..years, then growing at
    ``growth_long`` forever (Damodaran's two-stage implied return).  The right side falls in r, so the root is unique."""
    t = np.arange(1, years + 1)
    cf = cf0 * (1 + growth) ** t

    def value(r):
        return float(np.sum(cf / (1 + r) ** t) + cf[-1] * (1 + growth_long) / (r - growth_long) / (1 + r) ** years)

    lo = growth_long + 1e-6 if lo is None else lo
    return float(optimize.brentq(lambda r: value(r) - price, lo, hi, xtol=1e-12))


def tax_shield(tax: float, debt: float, rate_debt: float, years: int | None = None) -> float:
    """Present value of the interest tax shield T r_D D a year, discounted at r_D: T D for permanent debt."""
    if years is None:
        return tax * debt
    return annuity(tax * rate_debt * debt, rate_debt, years)


def apv(unlevered: float, tax: float, debt: float, rate_debt: float, distress: float = 0.0) -> float:
    """Adjusted present value: the unlevered firm, plus the tax shield of permanent debt, less expected distress costs."""
    return unlevered + tax_shield(tax, debt, rate_debt) - distress


def miller_gain(tax_corp: float, tax_equity: float, tax_debt: float) -> float:
    """Miller (1977): each dollar of permanent debt adds T* = 1 - (1 - Tc)(1 - TE)/(1 - TD) to the firm's value."""
    return 1 - (1 - tax_corp) * (1 - tax_equity) / (1 - tax_debt)


def campbell_shiller(r, dg, dp) -> dict:
    """Cochrane's (2008) decomposition from the Campbell-Shiller identity r_{t+1} ~ k - rho dp_{t+1} + dg_{t+1} + dp_t,
    with dp the log dividend yield.  Regress r_{t+1}, dg_{t+1} and dp_{t+1} on dp_t; rho = 1/(1 + exp(mean dp)).
    The identity says b_r - b_d + rho phi = 1 (approximately), and the long-run coefficients b/(1 - rho phi) of
    returns and dividend growth differ by one: a high yield must be paid for by returns or by low growth."""
    r, dg, dp = (np.asarray(a, float) for a in (r, dg, dp))
    x = dp[:-1]
    X = np.column_stack([np.ones_like(x), x])
    b = lambda y: float(np.linalg.lstsq(X, y, rcond=None)[0][1])  # noqa: E731
    br, bd, phi = b(r), b(dg), b(dp[1:])
    rho = 1 / (1 + np.exp(np.mean(dp)))
    return {"b_r": br, "b_d": bd, "phi": phi, "rho": float(rho), "lr_r": br / (1 - rho * phi),
            "lr_d": bd / (1 - rho * phi), "identity_gap": br - bd + rho * phi - 1}


BENEISH = {"const": -4.84, "DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892, "DEPI": 0.115, "SGAI": -0.172,
           "TATA": 4.679, "LVGI": -0.327}


def beneish_ratios(cur: dict, prev: dict) -> dict:
    """Beneish's eight indices from two years of statement items: sales, cogs, receivables, current_assets, ppe,
    securities, assets, depreciation, sga, current_liabilities, long_term_debt, net_income, cfo.  A missing input
    makes its index 1 (neutral) and TATA 0; ``missing`` lists them."""
    miss = []

    def g(d, k):
        v = d.get(k)
        return None if v is None or not np.isfinite(v) else float(v)

    def ratio(fn, keys, neutral=1.0, name=""):
        vals = [g(d, k) for d in (cur, prev) for k in keys]
        if any(v is None for v in vals):
            miss.append(name)
            return neutral
        try:
            out = fn()
        except ZeroDivisionError:
            miss.append(name)
            return neutral
        return out if np.isfinite(out) else neutral

    c, p = cur, prev
    out = {
        "DSRI": ratio(lambda: (c["receivables"] / c["sales"]) / (p["receivables"] / p["sales"]),
                      ["receivables", "sales"], name="DSRI"),
        "GMI": ratio(lambda: ((p["sales"] - p["cogs"]) / p["sales"]) / ((c["sales"] - c["cogs"]) / c["sales"]),
                     ["sales", "cogs"], name="GMI"),
        "AQI": ratio(lambda: (1 - (c["current_assets"] + c["ppe"]) / c["assets"])
                     / (1 - (p["current_assets"] + p["ppe"]) / p["assets"]),
                     ["current_assets", "ppe", "assets"], name="AQI"),
        "SGI": ratio(lambda: c["sales"] / p["sales"], ["sales"], name="SGI"),
        "DEPI": ratio(lambda: (p["depreciation"] / (p["depreciation"] + p["ppe"]))
                      / (c["depreciation"] / (c["depreciation"] + c["ppe"])), ["depreciation", "ppe"], name="DEPI"),
        "SGAI": ratio(lambda: (c["sga"] / c["sales"]) / (p["sga"] / p["sales"]), ["sga", "sales"], name="SGAI"),
        "LVGI": ratio(lambda: ((c["current_liabilities"] + c["long_term_debt"]) / c["assets"])
                      / ((p["current_liabilities"] + p["long_term_debt"]) / p["assets"]),
                      ["current_liabilities", "long_term_debt", "assets"], name="LVGI"),
    }
    if g(c, "net_income") is None or g(c, "cfo") is None or g(c, "assets") is None:
        miss.append("TATA")
        out["TATA"] = 0.0
    else:
        out["TATA"] = (c["net_income"] - c["cfo"]) / c["assets"]
    out["missing"] = miss
    return out


def beneish_m(ratios: dict) -> float:
    """Beneish (1999): M = -4.84 + 0.920 DSRI + 0.528 GMI + 0.404 AQI + 0.892 SGI + 0.115 DEPI - 0.172 SGAI
    + 4.679 TATA - 0.327 LVGI; above -1.78 the firm is flagged."""
    return float(BENEISH["const"] + sum(BENEISH[k] * ratios[k] for k in BENEISH if k != "const"))


def ohlson_value(book: float, xa: float, nu: float, omega: float, gamma: float, rate: float) -> dict:
    """Ohlson's (1995) linear information dynamics: abnormal earnings x^a_{t+1} = omega x^a_t + nu_t + e1 and other
    information nu_{t+1} = gamma nu_t + e2, with clean surplus.  Then the residual-income value is linear in the
    state: P = b + a1 x^a + a2 nu, a1 = omega/(R - omega), a2 = R/((R - omega)(R - gamma)), R = 1 + r."""
    R = 1 + rate
    a1 = omega / (R - omega)
    a2 = R / ((R - omega) * (R - gamma))
    return {"value": float(book + a1 * xa + a2 * nu), "a1": float(a1), "a2": float(a2)}


def ohlson_monte_carlo(book: float, xa: float, nu: float, omega: float, gamma: float, rate: float, n: int = 20000,
                       horizon: int = 400, sd1: float = 1.0, sd2: float = 0.5, seed: int = 0) -> float:
    """The same value by brute force: simulate the dynamics and average b + sum_t R^-t x^a_t (residual income)."""
    rng = np.random.default_rng(seed)
    R = 1 + rate
    x = np.full(n, float(xa))
    v = np.full(n, float(nu))
    total = np.zeros(n)
    disc = 1.0
    for _ in range(horizon):
        x, v = omega * x + v + sd1 * rng.standard_normal(n), gamma * v + sd2 * rng.standard_normal(n)
        disc /= R
        total += disc * x
    return float(book + total.mean())
