"""Every number in Part 3 (Value, Accounting and the Firm), computed and cached in .cache/quant3/.

    python -m videos.quant.quant3.compute [items] [--force]

Research window: to December 2020 (the sealed envelope).  Items (seconds):

* ``shiller``  Shiller (1981), "Do stock prices move too much?": the real S&P price since 1871 against the
               ex-post rational price p*, the present value of the dividends that were actually paid;
* ``cape``     the cyclically adjusted P/E against the next ten years' real total return, 1881-2010 starts;
* ``factors``  accounting signals as long-short portfolios on Ken French's decile sorts, 1963-2020: accruals,
               operating profitability, investment, book-to-market, earnings yield; before and after publication;
* ``dcf``      a firm's DCF value over discount rate and terminal growth (the value surface).
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import valuation

CACHE = Cache("quant3")
load = CACHE.load


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def _real(s):
    cpi = s["cpi"]
    base = cpi[-1]
    return s["price"] * base / cpi, s["div"] * base / cpi, s["earn"] * base / cpi


# ---------------------------------------------------------------------------
def compute_shiller() -> dict:
    s = data.shiller()
    t = s["t"]
    P, D, E = _real(s)
    ok = np.isfinite(P) & np.isfinite(D)
    t, P, D = t[ok], P[ok], D[ok]
    # annual series (January of each year): the real price and the real dividend paid over the following year
    jan = np.isclose(t % 1, 0)
    ty, Py = t[jan], P[jan]
    Dy = np.array([D[(t >= y + 11 / 12 - 1e-6) & (t < y + 1)][0] if np.any((t >= y + 11 / 12 - 1e-6) & (t < y + 1))
                   else np.nan for y in ty])
    m = np.isfinite(Dy)
    ty, Py, Dy = ty[m], Py[m], Dy[m]
    # the average real return (price growth plus dividend yield), used as the constant discount rate
    gross = (Py[1:] + Dy[:-1]) / Py[:-1]
    r = float(np.mean(gross) - 1)
    # p*: backward recursion from the last price: p*_t = (p*_{t+1} + D_t) / (1 + r)
    pstar = np.empty_like(Py)
    pstar[-1] = Py[-1]
    for i in range(len(Py) - 2, -1, -1):
        pstar[i] = (pstar[i + 1] + Dy[i]) / (1 + r)
    # detrend both by the same exponential trend of the price, to compare their volatility
    k = np.polyfit(ty, np.log(Py), 1)
    trend = np.exp(np.polyval(k, ty))
    sd_p = float(np.std(Py / trend))
    sd_ps = float(np.std(pstar / trend))
    # the sharper measure: how much each moves from one year to the next
    dP = np.diff(np.log(Py))
    dS = np.diff(np.log(pstar))
    return {"t": ty, "price": Py, "pstar": pstar, "div": Dy, "r": r, "sd_price": sd_p, "sd_pstar": sd_ps,
            "ratio": sd_p / sd_ps, "n_years": int(len(ty)), "sd_dprice": float(np.std(dP)), "sd_dpstar": float(np.std(dS)),
            "ratio_changes": float(np.std(dP) / np.std(dS)), "big_moves": int(np.sum(np.abs(dP) > 0.2)),
            "big_moves_pstar": int(np.sum(np.abs(dS) > 0.2)), "dy": Dy / Py, "earn_yield": None}


# ---------------------------------------------------------------------------
def compute_cape() -> dict:
    s = data.shiller()
    t = s["t"]
    P, D, _ = _real(s)
    cape = s["cape"]
    # real total return index: monthly price change plus a twelfth of the annual dividend
    tr = np.ones(len(t))
    for i in range(1, len(t)):
        tr[i] = tr[i - 1] * (P[i] + D[i - 1] / 12) / P[i - 1] if np.isfinite(P[i]) and np.isfinite(D[i - 1]) else tr[i - 1]
    h = 120
    starts = np.arange(len(t) - h)
    valid = np.isfinite(cape[starts]) & (cape[starts] > 0)
    st = starts[valid]
    fwd = (tr[st + h] / tr[st]) ** (1 / 10) - 1
    x = np.log(cape[st])
    b, a = np.polyfit(x, fwd, 1)
    r2 = float(np.corrcoef(x, fwd)[0, 1] ** 2)
    # non-overlapping (every 10th year, January) for an honest count
    jan10 = st[np.isclose(t[st] % 10, 1.0 % 10) | np.isclose(t[st] % 10, 1.0)]
    last = len(t) - 1
    now = float(cape[last])
    pred_now = float(a + b * np.log(now))
    return {"t": t[st], "cape": cape[st], "fwd": fwd, "slope": float(b), "intercept": float(a), "r2": r2,
            "n": int(len(st)), "n_indep": int(len(st) // h), "cape_now": now, "pred_now": pred_now,
            "cape_series_t": t[np.isfinite(cape) & (cape > 0)], "cape_series": cape[np.isfinite(cape) & (cape > 0)],
            "mean_cape": float(np.nanmean(cape[cape > 0]))}


# ---------------------------------------------------------------------------
# (file name, long leg column, short leg column, label, publication year)
SIGNALS = [("AC", "Lo 10", "Hi 10", "low minus high accruals", "Sloan (1996)", 1996),
           ("OP", "Hi 10", "Lo 10", "high minus low operating profitability", "Novy-Marx (2013); Fama--French (2015)", 2013),
           ("INV", "Lo 10", "Hi 10", "low minus high asset growth", "Titman, Wei and Xie (2004)", 2004),
           ("BE-ME", "Hi 10", "Lo 10", "high minus low book-to-market", "Fama and French (1992)", 1992),
           ("E-P", "Hi 10", "Lo 10", "high minus low earnings yield", "Basu (1977)", 1977)]


def _stats(r):
    r = np.asarray(r)
    r = r[np.isfinite(r)]
    m, s = r.mean() * 12, r.std(ddof=1) * np.sqrt(12)
    return {"mean": float(m), "vol": float(s), "sharpe": float(m / s), "t": float(r.mean() / r.std(ddof=1) * np.sqrt(len(r))),
            "n": int(len(r))}


def compute_factors() -> dict:
    out = {}
    for name, lo, hi, lab, who, year in SIGNALS:
        k = data.ken_french_sorts(name)
        cols = k["columns"]
        d = k["date"]
        m = d >= 196307
        ls = k["returns"][m, cols.index(lo)] - k["returns"][m, cols.index(hi)]
        dm = d[m]
        pre = ls[dm < (year + 1) * 100]
        post = ls[dm >= (year + 1) * 100]
        cum = np.cumprod(1 + np.nan_to_num(ls))
        out[name] = {"label": lab, "who": who, "year": year, "all": _stats(ls), "pre": _stats(pre) if len(pre) > 24 else None,
                     "post": _stats(post) if len(post) > 24 else None, "t": (dm // 100 + (dm % 100 - 0.5) / 12).tolist(),
                     "cum": cum.tolist()}
    return _json({"signals": out, "order": [s_[0] for s_ in SIGNALS]})


# ---------------------------------------------------------------------------
def compute_dcf() -> dict:
    rates = np.linspace(0.06, 0.12, 31)
    growths = np.linspace(0.0, 0.04, 21)
    fcf0 = 100.0
    V = np.zeros((len(growths), len(rates)))
    share_tv = np.zeros_like(V)
    for i, g in enumerate(growths):
        for j, r in enumerate(rates):
            fcf = fcf0 * (1.05) ** np.arange(1, 6)  # five years of 5% growth, then g forever
            d = valuation.dcf(fcf, r, g)
            V[i, j] = d["value"]
            share_tv[i, j] = d["terminal"] / d["value"]
    base = valuation.dcf(fcf0 * 1.05 ** np.arange(1, 6), 0.08, 0.02)
    alt = valuation.dcf(fcf0 * 1.05 ** np.arange(1, 6), 0.07, 0.03)
    return {"rates": rates, "growths": growths, "value": V, "share_tv": share_tv, "base": base["value"],
            "base_tv_share": base["terminal"] / base["value"], "alt": alt["value"]}


ITEMS = {"shiller": compute_shiller, "cape": compute_cape, "factors": compute_factors, "dcf": compute_dcf}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
