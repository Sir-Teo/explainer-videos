"""The House's valuation tools (Part 3, *Value, Accounting and the Firm*): what a claim on future cash is worth.

* :func:`npv`, :func:`irr`: present value of dated cash flows, and the rate that makes it zero;
* :func:`annuity`, :func:`perpetuity`, :func:`gordon`: the closed forms;
* :func:`dcf`: a firm's value from explicit free cash flows plus a Gordon terminal value;
* :func:`wacc`, :func:`levered_beta`, :func:`mm_cost_of_equity`: the cost of capital and Modigliani-Miller;
* :func:`merton_equity`: equity as a call on the firm's assets (Merton 1974; Part 20).
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
