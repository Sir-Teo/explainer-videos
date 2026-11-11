"""The House's factor library (Part 24): the classic factors as returns, tested, timed and kept honest.

* Summary statistics a factor is judged by: annualised mean, volatility, Sharpe ratio and its standard error, t, skew,
  worst month, maximum drawdown (:func:`stats`, :func:`drawdown`, :func:`cumulative`).
* Tests: time-series alphas against a model (:func:`alpha`), spanning (is a factor redundant given others?), and the
  joint tests of Part 6 (``econ.grs``, ``econ.two_pass``), wrapped as :func:`model_test`.
* Portfolio construction, as Fama and French do it: 2 x 3 sorts on size and a characteristic, NYSE breakpoints
  (:func:`two_by_three`), shown on toy cross-sections.
* Momentum's repairs: Barroso and Santa-Clara's volatility scaling (:func:`vol_scaled`) and Daniel and Moskowitz's
  bear-market beta (:func:`conditional_beta`).
* Timing: Ehsani and Linnainmaa's time-series factor momentum (:func:`factor_momentum`) and a value-spread forecast.
* Combinations: an equal-risk mix (:func:`equal_risk`) and the 50/50 value-momentum book (Asness, Moskowitz and Pedersen).

Returns are monthly decimals unless stated; annualisation multiplies means by 12 and volatilities by sqrt(12).
"""

from __future__ import annotations

import numpy as np

from explainer.quant.house import econ as E


def cumulative(r) -> np.ndarray:
    """Growth of $1 from monthly returns (simple, compounded; NaN months count as zero)."""
    return np.cumprod(1 + np.nan_to_num(np.asarray(r, float)))


def drawdown(r) -> dict:
    """The path's drawdown from its running peak: ``dd`` (series, <= 0), ``max`` (most negative), and the indices of
    the peak and trough of the worst one."""
    w = cumulative(r)
    peak = np.maximum.accumulate(w)
    dd = w / peak - 1
    j = int(np.argmin(dd))
    i = int(np.argmax(w[:j + 1])) if j > 0 else 0
    return {"dd": dd, "max": float(dd[j]), "peak": i, "trough": j}


def stats(r) -> dict:
    """What a factor is judged by, from monthly returns: annualised ``mean``, ``vol``, ``sharpe`` (with Lo's standard
    error), ``t`` (of the mean), ``skew``, ``worst`` month and ``maxdd``; ``n`` months."""
    x = np.asarray(r, float)
    x = x[np.isfinite(x)]
    n = len(x)
    m, s = x.mean(), x.std(ddof=1)
    sk = float(((x - m) ** 3).mean() / s ** 3)
    ku = float(((x - m) ** 4).mean() / s ** 4)
    sr = m / s * np.sqrt(12)
    se = E.sharpe_se(m / s, n, sk, ku) * np.sqrt(12)
    return {"mean": float(m * 12), "vol": float(s * np.sqrt(12)), "sharpe": float(sr), "sharpe_se": float(se),
            "t": float(m / s * np.sqrt(n)), "skew": sk, "worst": float(x.min()), "maxdd": drawdown(x)["max"], "n": n}


def alpha(y, F, lags: int = 6) -> dict:
    """Time-series regression of a factor (or portfolio) on others: annualised ``alpha`` with a Newey-West ``t``,
    the ``betas`` and ``r2``. If ``alpha`` is indistinguishable from zero, ``y`` is spanned by ``F``."""
    y = np.asarray(y, float)
    F = np.asarray(F, float)
    if F.ndim == 1:
        F = F[:, None]
    o = E.ols(y, F, se="nw", lags=lags)
    resid = y - (o["beta"][0] + F @ o["beta"][1:])
    r2 = 1 - resid.var() / y.var()
    return {"alpha": float(o["beta"][0] * 12), "t": float(o["beta"][0] / o["se"][0]), "betas": o["beta"][1:],
            "r2": float(r2), "resid_vol": float(resid.std() * np.sqrt(12))}


def model_test(R, F) -> dict:
    """A factor model on test portfolios ``R`` (T x N excess returns): GRS (are all alphas zero?), the average
    absolute alpha (annualised), and the two-pass premia with Shanken t-statistics."""
    g = E.grs(R, F)
    tp = E.two_pass(R, F)
    return {"grs": g["F"], "p": g["p"], "mean_abs_alpha": float(np.mean(np.abs(g["alpha"])) * 12),
            "alpha": np.asarray(g["alpha"]) * 12, "lambda": np.asarray(tp["lambda"]) * 12,
            "t_shanken": np.asarray(tp["t_shanken"]), "df": g["df"]}


def two_by_three(size, char, nyse, ret, weight) -> dict:
    """Fama and French's construction on one cross-section: split by the NYSE median of ``size`` and the NYSE 30th
    and 70th percentiles of ``char``; six value-weighted portfolios; SMB = mean(small) - mean(big) over the three
    characteristic groups, and HML-style = mean(high) - mean(low) over the two size groups."""
    size, char, ret, weight = (np.asarray(v, float) for v in (size, char, ret, weight))
    nyse = np.asarray(nyse, bool)
    med = np.median(size[nyse])
    lo, hi = np.percentile(char[nyse], [30, 70])
    s = np.where(size <= med, 0, 1)
    c = np.where(char <= lo, 0, np.where(char <= hi, 1, 2))
    P = np.full((2, 3), np.nan)
    for i in range(2):
        for j in range(3):
            m = (s == i) & (c == j)
            if m.any():
                P[i, j] = float(np.sum(weight[m] * ret[m]) / np.sum(weight[m]))
    return {"P": P, "smb": float(np.nanmean(P[0]) - np.nanmean(P[1])),
            "hml": float(np.nanmean(P[:, 2]) - np.nanmean(P[:, 0])), "breaks": (float(med), float(lo), float(hi))}


def vol_scaled(r, target: float = 0.12, window: int = 6) -> np.ndarray:
    """Barroso and Santa-Clara (2015): hold ``target`` / (forecast volatility) of the factor, the forecast being the
    realised volatility of the previous ``window`` months (annualised). The first ``window`` months are NaN. Uses only
    returns before each month: point in time."""
    r = np.asarray(r, float)
    out = np.full(len(r), np.nan)
    for t in range(window, len(r)):
        sig = r[t - window:t].std(ddof=1) * np.sqrt(12)
        out[t] = r[t] * min(target / sig, 3.0) if sig > 0 else np.nan
    return out


def conditional_beta(r, mkt, bear, rebound) -> dict:
    """Daniel and Moskowitz (2016): regress a factor on the market, separately in normal months, in bear markets
    (``bear``: the market fell over the prior 24 months), and in bear markets when the market rebounds (``rebound``:
    bear and the market's return this month is positive). After a crash the losers left in the short leg are
    high-beta, so momentum is short the rebound."""
    r, mkt = np.asarray(r, float), np.asarray(mkt, float)
    bear, rebound = np.asarray(bear, bool), np.asarray(rebound, bool)
    out = {}
    for nm, m in (("normal", ~bear), ("bear, market down", bear & ~rebound), ("bear, market up", rebound)):
        o = E.ols(r[m], mkt[m])
        out[nm] = {"alpha": float(o["beta"][0] * 12), "beta": float(o["beta"][1]), "n": int(m.sum()),
                   "mean": float(r[m].mean() * 12)}
    return out


def factor_momentum(F, lookback: int = 12) -> dict:
    """Ehsani and Linnainmaa (2022), time-series factor momentum: each month, long each factor whose return over the
    previous ``lookback`` months was positive and short each whose return was negative, equal weights. Returns the
    strategy (``r``), the equal-weighted buy-and-hold of the same factors (``ew``), and the share of months each factor
    is held long. Point in time: month t uses returns to t - 1."""
    F = np.asarray(F, float)
    T, K = F.shape
    r = np.full(T, np.nan)
    sgn = np.zeros((T, K))
    for t in range(lookback, T):
        past = np.prod(1 + F[t - lookback:t], axis=0) - 1
        s = np.sign(past)
        sgn[t] = s
        r[t] = float(np.mean(s * F[t]))
    return {"r": r, "ew": F.mean(axis=1), "long_share": (sgn[lookback:] > 0).mean(axis=0)}


def equal_risk(F, window: int = 36) -> np.ndarray:
    """Each factor scaled by its trailing ``window``-month volatility to equal risk, then averaged: the simplest
    'factor book'. Point in time; NaN for the first ``window`` months."""
    F = np.asarray(F, float)
    T, K = F.shape
    out = np.full(T, np.nan)
    for t in range(window, T):
        s = F[t - window:t].std(axis=0, ddof=1)
        w = (1 / s) / np.sum(1 / s)
        out[t] = float(w @ F[t])
    return out


def value_spread(bm_value, bm_growth) -> np.ndarray:
    """The value spread: the log book-to-market of value stocks less that of growth stocks. Wide spreads mean value
    stocks are unusually cheap relative to growth (Cohen, Polk and Vuolteenaho 2003)."""
    return np.log(np.asarray(bm_value, float)) - np.log(np.asarray(bm_growth, float))


def ddm_bm(roe, inv, r, horizon: int = 200) -> float:
    """Fama and French's (2006, 2015) motivation for profitability and investment, from the dividend discount model:
    with book equity B growing at ``inv`` a year and earnings ROE x B, of which ROE - inv is paid out, the market value
    over book is sum (ROE - inv)(1 + inv)^(t-1) / (1 + r)^t. Returns B/M: higher with lower profitability, higher
    investment, or a higher discount rate ``r``."""
    t = np.arange(1, horizon + 1)
    mb = float(np.sum((roe - inv) * (1 + inv) ** (t - 1) / (1 + r) ** t))
    return 1 / mb
