"""The House's macro desk (Part 22): currencies, commodities, the Treasury basis and inflation.

Conventions: rates are decimals a year; a currency pair quoted as Q = units of USD per one unit of foreign currency
(GBP/USD = 1.27) unless said otherwise; ``tau`` in years.

* Covered interest parity and its basis (Du, Tepper and Verdelhan 2018), the Fama (1984) regression, carry sorts
  (Lustig, Roussanov and Verdelhan 2011) and their crash statistics (Brunnermeier, Nagel and Pedersen 2008).
* FX options: Garman–Kohlhagen, the four delta conventions, strikes from deltas, the at-the-money delta-neutral
  straddle, and a smile from the market's ATM / risk-reversal / butterfly quotes (the vanna–volga interpolation is
  ``quoting.vanna_volga``).
* Commodities: the cost of carry, the implied convenience yield, a rolled front-month futures index from contracts
  1 and 2 (WTI's expiry rule), and the spread between two futures.
* The Treasury basis: the futures invoice price, the implied repo rate, gross and net basis.
* Inflation: breakevens, and the realised inflation they are compared with.
* A first-generation speculative attack (Krugman 1979; Flood and Garber 1984): the shadow exchange rate and the date
  the peg falls.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr

from . import bs

# ---------------------------------------------------------------------------
# Covered and uncovered interest parity
# ---------------------------------------------------------------------------


def cc(r, tau):
    """A simple (money-market) rate over ``tau`` as a continuously compounded one."""
    return np.log1p(np.asarray(r, float) * tau) / tau


def cip_forward(Q, r_usd, r_for, tau):
    """The forward that covered interest parity requires: Q_F = Q (1 + r_usd tau) / (1 + r_for tau)."""
    return np.asarray(Q, float) * (1 + np.asarray(r_usd, float) * tau) / (1 + np.asarray(r_for, float) * tau)


def cip_basis(Q, F, r_usd, r_for, tau):
    """Du, Tepper and Verdelhan's basis x = y_USD - (y_for - rho), with rho the forward premium in their quote
    (foreign currency per dollar): here, with Q in USD per foreign unit, rho = -ln(F/Q)/tau, so
    x = y_USD - y_for - ln(F/Q)/tau.  Continuously compounded; zero when parity holds; negative when dollars obtained
    by swapping foreign currency cost more than dollars borrowed directly."""
    return cc(r_usd, tau) - cc(r_for, tau) - np.log(np.asarray(F, float) / np.asarray(Q, float)) / tau


def fama_regression(Q, r_usd, r_for, h=1 / 12, lags=0):
    """Fama (1984): regress the change in s = ln(foreign per dollar) over the next period on the forward premium
    f - s = (r_for - r_usd) h (by covered parity).  Uncovered parity predicts slope 1; the puzzle is that it is
    below 1, often negative.  ``Q`` USD per foreign unit, aligned with the rates at the start of each period."""
    from .econ import ols

    s = -np.log(np.asarray(Q, float))
    ds = s[1:] - s[:-1]
    fp = (np.asarray(r_for, float)[:-1] - np.asarray(r_usd, float)[:-1]) * h
    o = ols(ds, fp, se="nw" if lags else "white", lags=lags)
    return {"alpha": float(o["beta"][0]), "beta": float(o["beta"][1]), "se": float(o["se"][1]),
            "t_vs_1": float((o["beta"][1] - 1) / o["se"][1]), "r2": float(o["r2"]), "n": int(o["n"])}


def currency_excess_returns(Q, r_usd, r_for, h=1 / 12):
    """The log excess return of a US investor who holds the foreign currency for one period, earning its interest:
    ln(Q_{t+1}/Q_t) + (r_for - r_usd) h.  Uncovered parity says its mean is zero."""
    Q = np.asarray(Q, float)
    return np.log(Q[1:] / Q[:-1]) + (np.asarray(r_for, float)[:-1] - np.asarray(r_usd, float)[:-1]) * h


def carry_sort(excess, diff, k=3):
    """Carry portfolios: each period, rank the currencies by the interest differential known at its start
    (``diff`` [T, n], NaN for missing) and go long the ``k`` highest, short the ``k`` lowest, equal weights.
    ``excess`` [T, n] holds each currency's next-period excess return (aligned with ``diff``). Returns the
    long-short return series and the long and short legs."""
    excess, diff = np.asarray(excess, float), np.asarray(diff, float)
    ls, lo, sh = [], [], []
    for t in range(excess.shape[0]):
        ok = np.isfinite(diff[t]) & np.isfinite(excess[t])
        if ok.sum() < 2 * k:
            ls.append(np.nan), lo.append(np.nan), sh.append(np.nan)
            continue
        idx = np.where(ok)[0]
        order = idx[np.argsort(diff[t, idx])]
        lo_r, sh_r = excess[t, order[-k:]].mean(), excess[t, order[:k]].mean()
        ls.append(lo_r - sh_r), lo.append(lo_r), sh.append(sh_r)
    return {"ls": np.array(ls), "long": np.array(lo), "short": np.array(sh)}


def crash_stats(r, per_year=12):
    """Mean, volatility, Sharpe ratio (annualised), skewness and the worst period of a return series."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    m, s = r.mean(), r.std(ddof=1)
    z = (r - m) / s
    return {"mean": float(m * per_year), "vol": float(s * np.sqrt(per_year)), "sharpe": float(m / s * np.sqrt(per_year)),
            "skew": float(np.mean(z ** 3)), "worst": float(r.min()), "n": int(len(r))}


# ---------------------------------------------------------------------------
# FX options
# ---------------------------------------------------------------------------


def garman_kohlhagen(S, K, T, sigma, rd, rf, cp=1):
    """Garman and Kohlhagen (1983): Black–Scholes with the foreign rate as the carry yield. S and K in domestic per
    foreign; the price is in domestic currency per unit of foreign notional."""
    return bs.price(S, K, T, sigma, r=rd, q=rf, cp=cp)


def fx_delta(S, K, T, sigma, rd, rf, cp=1, kind="spot"):
    """The four delta conventions of the FX market: 'spot' (dV/dS, e^{-rf T} N(cp d1) cp), 'forward' (N(cp d1) cp),
    and their premium-adjusted versions 'spot_pa' and 'forward_pa' (the delta less the premium in foreign currency,
    for pairs whose premium is paid in the foreign unit: K/F N(cp d2) cp, times e^{-rf T} for spot)."""
    d1, d2 = bs.d1_d2(S, K, T, sigma, rd, rf)
    F = S * np.exp((rd - rf) * T)
    if kind == "spot":
        return cp * np.exp(-rf * T) * ndtr(cp * d1)
    if kind == "forward":
        return cp * ndtr(cp * d1)
    if kind == "spot_pa":
        return cp * np.exp(-rf * T) * K / F * ndtr(cp * d2)
    if kind == "forward_pa":
        return cp * K / F * ndtr(cp * d2)
    raise ValueError(kind)


def strike_from_delta(S, T, sigma, rd, rf, delta, cp=1, kind="forward"):
    """The strike with the given delta under a convention. Closed form for 'spot' and 'forward'; for the
    premium-adjusted conventions (not monotone far out) the root on the side of the forward the delta implies."""
    F = S * np.exp((rd - rf) * T)
    sT = sigma * np.sqrt(T)
    if kind in ("spot", "forward"):
        d = delta * (np.exp(rf * T) if kind == "spot" else 1.0)
        from scipy.special import ndtri
        return float(F * np.exp(-cp * ndtri(cp * d) * sT + 0.5 * sT ** 2))
    f = lambda K: float(fx_delta(S, K, T, sigma, rd, rf, cp, kind)) - delta  # noqa: E731
    if cp == 1:  # the premium-adjusted call delta peaks below F: search above the peak
        lo = F * np.exp(-0.5 * sT ** 2 - 1e-9)
        return float(brentq(f, lo, F * np.exp(8 * sT)))
    return float(brentq(f, F * np.exp(-8 * sT), F * np.exp(2 * sT)))


def atm_dns_strike(F, T, sigma, premium_adjusted=False):
    """The at-the-money delta-neutral straddle strike: call and put deltas cancel. K = F e^{sigma^2 T / 2}, or
    F e^{-sigma^2 T / 2} with premium-adjusted deltas."""
    return float(F * np.exp((-0.5 if premium_adjusted else 0.5) * sigma ** 2 * T))


def smile_quotes(atm, rr25, bf25):
    """The broker's three numbers to the 25-delta pillar vols (the 'smile strangle' convention):
    sigma_25c = ATM + BF + RR/2, sigma_25p = ATM + BF - RR/2."""
    return {"25p": atm + bf25 - 0.5 * rr25, "atm": atm, "25c": atm + bf25 + 0.5 * rr25}


# ---------------------------------------------------------------------------
# Commodities
# ---------------------------------------------------------------------------


def carry_forward(S, T, r, storage=0.0, convenience=0.0):
    """The cost-of-carry forward F = S e^{(r + u - y) T}: financing plus storage, less the convenience yield."""
    return np.asarray(S, float) * np.exp((r + storage - convenience) * T)


def implied_convenience(F1, F2, dT, r, storage=0.0):
    """The convenience yield net of storage that two futures dT apart imply: y - u = r - ln(F2/F1)/dT. Positive in
    backwardation; negative (paid to store) in steep contango."""
    return r - np.log(np.asarray(F2, float) / np.asarray(F1, float)) / dT + storage


def wti_last_trade(year, month, trading_days):
    """WTI's last trading day for the contract delivered in (year, month): three business days before the 25th of
    the month before delivery, or before the last business day before the 25th if that is not one. ``trading_days``
    is the sorted array of YYYYMMDD dates present in the data (business days)."""
    py, pm = (year, month - 1) if month > 1 else (year - 1, 12)
    d25 = py * 10000 + pm * 100 + 25
    td = np.asarray(trading_days)
    i = np.searchsorted(td, d25, side="right") - 1  # the 25th if it traded, else the last business day before
    return int(td[i - 3])  # three business days before either


def rolled_front(dates, c1, c2, roll_offset=5):
    """A rolled front-month futures index from the continuous contract-1 and contract-2 series (WTI): hold the
    second contract from the ``roll_offset``-th trading day of each month until the next month's roll (it becomes
    contract 1 after the front's last trading day), as index providers roll early in the month. Returns the daily
    excess return of the held contract (fully collateralised: the price change over the price) and the held index
    (1 or 2) on each day."""
    dates, c1, c2 = np.asarray(dates), np.asarray(c1, float), np.asarray(c2, float)
    ym = dates // 100
    ltd = set()
    for y_m in np.unique(ym):
        y, m = divmod(int(y_m), 100)
        ny, nm = (y, m + 1) if m < 12 else (y + 1, 1)  # the contract expiring in month m delivers in m + 1
        try:
            ltd.add(wti_last_trade(ny, nm, dates))
        except IndexError:
            pass
    first_of_month = np.r_[True, ym[1:] != ym[:-1]]
    k_in_month = np.zeros(len(dates), int)
    k = 0
    for i in range(len(dates)):
        k = 1 if first_of_month[i] else k + 1
        k_in_month[i] = k
    held = np.zeros(len(dates), int)
    h = 2
    for i in range(len(dates)):
        held[i] = h
        if dates[i] in ltd and h == 2:  # the front expires today: tomorrow our contract is contract 1
            h = 1
        if k_in_month[i] == roll_offset and h == 1:  # roll at today's close into the next contract (now 2)
            h = 2
    r = np.full(len(dates), np.nan)
    for i in range(1, len(dates)):
        p_prev = c1[i - 1] if held[i - 1] == 1 else c2[i - 1]
        if held[i - 1] == 2 and held[i] == 1:  # same contract, renumbered after the front's expiry
            p_now = c1[i]
        elif held[i - 1] == 1 and held[i] == 2:  # rolled at yesterday's close: yesterday's return was on the old one
            p_prev, p_now = c2[i - 1], c2[i]
        else:
            p_now = c1[i] if held[i] == 1 else c2[i]
        r[i] = (p_now - p_prev) / p_prev
    return {"r": r, "held": held, "ltd": np.array(sorted(ltd))}


def spark_spread(power, gas, heat_rate=7.0):
    """A gas plant's gross margin: power price ($/MWh) less heat rate (MMBtu per MWh) times gas ($/MMBtu)."""
    return np.asarray(power, float) - heat_rate * np.asarray(gas, float)


# ---------------------------------------------------------------------------
# The Treasury basis
# ---------------------------------------------------------------------------


def invoice_price(futures, conversion_factor, accrued):
    """What the long pays for a delivered bond: futures price times its conversion factor, plus accrued interest."""
    return futures * conversion_factor + accrued


def implied_repo(cash_dirty, futures, cf, accrued_delivery, days, coupons=0.0):
    """The financing rate that makes buying the bond and delivering it into the futures break even (actual/360):
    ((invoice + coupons received) / dirty price - 1) * 360 / days."""
    inv = invoice_price(futures, cf, accrued_delivery)
    return ((inv + coupons) / cash_dirty - 1) * 360 / days


def gross_basis(cash_clean, futures, cf):
    """Clean price less futures times conversion factor, per 100 (in 32nds on a desk)."""
    return cash_clean - futures * cf


def net_basis(cash_clean, futures, cf, coupon_rate, repo, days, cash_dirty):
    """Gross basis less carry: carry = coupon income (actual/365 here) minus financing at repo on the dirty price."""
    carry = coupon_rate * 100 * days / 365 - cash_dirty * repo * days / 360
    return gross_basis(cash_clean, futures, cf) - carry


# ---------------------------------------------------------------------------
# Inflation
# ---------------------------------------------------------------------------


def breakeven(nominal, real):
    """The breakeven inflation rate: nominal less real (TIPS) yield, the inflation at which the two bonds tie
    (it also carries an inflation risk premium and TIPS' liquidity discount)."""
    return np.asarray(nominal, float) - np.asarray(real, float)


def realised_inflation(cpi_dates, cpi, start, years):
    """Annualised CPI inflation from the month of ``start`` (YYYYMMDD) over ``years``; NaN if not yet known."""
    ym = np.asarray(cpi_dates) // 100
    s = start // 100
    y, m = divmod(s, 100)
    e = (y + years) * 100 + m
    i, j = np.searchsorted(ym, s), np.searchsorted(ym, e)
    if j >= len(ym) or ym[j] != e or ym[i] != s:
        return np.nan
    return float((cpi[j] / cpi[i]) ** (1 / years) - 1)


# ---------------------------------------------------------------------------
# A speculative attack (first generation)
# ---------------------------------------------------------------------------


def attack_model(peg=1.0, d0=0.5, mu=0.05, alpha=2.0, R0=None, T=20.0, n=2001):
    """Krugman (1979) and Flood and Garber (1984), in logs: money m = log(d + R) is approximated as m = d + R for
    small reserves, domestic credit d grows at mu, the price level is the exchange rate, and money demand is
    m - s = -alpha ds/dt. Under the peg s = peg, reserves R = peg - d fall as credit grows. The 'shadow' floating rate
    without reserves is s~ = d + alpha mu; speculators attack the moment s~ reaches the peg, at
    T* = (peg - alpha mu - d0)/mu, and buy the remaining reserves, alpha mu, in one day."""
    t = np.linspace(0, T, n)
    d = d0 + mu * t
    shadow = d + alpha * mu
    t_star = (peg - alpha * mu - d0) / mu
    R = np.where(t < t_star, peg - d, 0.0)
    s = np.where(t < t_star, peg, shadow)
    return {"t": t, "d": d, "shadow": shadow, "R": R, "s": s, "t_star": float(t_star),
            "reserves_at_attack": float(alpha * mu), "reserves_if_no_attack_run_out": float((peg - d0) / mu)}
