"""Precompute every number in Part 23 of *Economics, Built* ("Capital and Asset Prices").

    python -m videos.economics.econ23.compute            # everything missing (seconds)
    python -m videos.economics.econ23.compute --force mp

Results are cached in ``.cache/econ23/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Shiller's annual stock, interest-rate and consumption series with his ex post rational
prices; the national home price index and the CPI's rent; Mehra and Prescott's and others' published numbers,
transcribed).  Models: Agora's asset prices and investment (``agora.assets``), with the Island's Part 23 truths.

Items:
    moments      Mehra and Prescott's published moments and the same computed from Shiller's data
    playit       the coconut tree's price
    gordon       the Gordon formula and a one-point rise in the discount rate; Shiller's price-dividend ratio
    firm         Hayashi's firm after a rise in productivity: capital, q and investment
    option       the option to wait: the investment threshold against volatility
    region       Mehra and Prescott's economy: the (risk-free rate, premium) pairs it can produce
    hj           the Hansen-Jagannathan bound, the risk aversion it needs, and the risk-free rate puzzle
    ccapm        the consumption CAPM: the premium over its covariance with consumption growth
    disasters    rare disasters: the premium and the risk-free rate against risk aversion
    habit        Campbell and Cochrane's surplus ratio and the price of risk
    volatility   Shiller's excess volatility: the real price against its ex post rational value
    predict      the dividend-price ratio and returns over 1, 5 and 10 years
    ssw          a stylized laboratory market
    housing      US home prices against rents, 1987-2026
    film         the intermission's data film: a real dollar in stocks and in bills, 1871-2013
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import assets as ast
from explainer.economics.data import tables

CACHE = Cache("econ23")
load = CACHE.load
TRUTH = island.truths(23)


def _shiller():
    d = data.shiller()
    return {k: np.array(v, float) for k, v in d.items()}


def _moments(first: int, last: int) -> dict:
    """Annual real returns (January to January) on the S&P composite and on one-year bonds, and the growth of real
    consumption per head over the same year (from year t to t + 1)."""
    s = _shiller()
    y, R, rf, C = s["year"], s["Return"], s["RealR"] - 1, s["C"]
    g = np.r_[C[1:] / C[:-1] - 1, np.nan]
    m = (y >= first) & (y <= last) & np.isfinite(R) & np.isfinite(rf) & np.isfinite(g)
    ex = R[m] - rf[m]
    return {"first": first, "last": last, "n": int(m.sum()), "stock": float(R[m].mean()), "sd_stock": float(R[m].std()),
            "bill": float(rf[m].mean()), "sd_bill": float(rf[m].std()), "premium": float(ex.mean()),
            "sd_premium": float(ex.std()), "sharpe": float(ex.mean() / ex.std()), "growth": float(g[m].mean()),
            "sd_growth": float(g[m].std()), "corr": float(np.corrcoef(R[m], g[m])[0, 1]),
            "cov": float(np.cov(ex, g[m])[0, 1])}


def compute_moments() -> dict:
    mp = tables.MEHRA_PRESCOTT_1985.data
    return {"published": mp, "mp_window": _moments(1889, 1978), "long": _moments(1889, 2009)}


def compute_playit() -> dict:
    p = TRUTH["playit"]
    price = 0.5 * p["m_good"] * p["pay_good"] + 0.5 * p["m_bad"] * p["pay_bad"]
    safe = 0.5 * (p["m_good"] + p["m_bad"]) * 0.5 * (p["pay_good"] + p["pay_bad"])
    insurance = 0.5 * p["m_good"] * p["pay_bad"] + 0.5 * p["m_bad"] * p["pay_good"]
    answer = int(np.argmin([abs(o - price) for o in p["options"]]))
    rf = 1 / (0.5 * (p["m_good"] + p["m_bad"])) - 1
    return {**p, "price": price, "safe": safe, "insurance": insurance, "answer": answer, "expected": 0.5 * (
        p["pay_good"] + p["pay_bad"]), "rf": rf, "return": 0.5 * p["pay_good"] / price - 1}


def compute_gordon() -> dict:
    g = TRUTH["gordon"]
    out = ast.gordon(g["D1"], g["r"], g["g"])
    s = _shiller()
    m = np.isfinite(s["RealP"]) & np.isfinite(s["RealD"])
    years = s["year"][m]
    pd = s["RealP"][m] / s["RealD"][m]
    D = s["RealD"][m]
    growth = float((D[-1] / D[0]) ** (1 / (years[-1] - years[0])) - 1)
    return {**g, **out, "pd_years": years.tolist(), "pd": pd.tolist(), "div_growth": growth,
            "pd_first": float(pd[0]), "pd_last": float(pd[-1]), "pd_mean": float(pd.mean()),
            "pd_max": float(pd.max()), "pd_max_year": int(years[int(np.argmax(pd))])}


def compute_firm() -> dict:
    f = TRUTH["firm"]
    out = ast.q_investment(**f)
    out["user_cost"] = ast.user_cost(f["r"], f["delta"])
    out.update(f)
    return out


def compute_option() -> dict:
    o = TRUTH["option"]
    rows = [{"sigma": s, **ast.option_to_wait(r=o["r"], mu=o["mu"], sigma=s)} for s in o["sigmas"]]
    sig = np.linspace(0.02, 0.5, 60)
    curve = [ast.option_to_wait(r=o["r"], mu=o["mu"], sigma=float(s))["multiple"] for s in sig]
    return {"rows": rows, "sigma": sig.tolist(), "multiple": curve, "r": o["r"], "mu": o["mu"]}


def compute_region() -> dict:
    p = TRUTH["mp"]
    gammas = np.linspace(0.05, p["gamma_max"], 60)
    betas = np.linspace(p["beta_min"], 0.999, 60)
    reg = ast.mp_region(gammas, betas, mu=p["mu"], delta=p["delta"], phi=p["phi"])
    pts = np.array(reg["points"])
    ok = pts[:, 2] <= p["rf_max"]
    best = pts[ok][np.argmax(pts[ok][:, 3])]
    edge = {}
    for g in (1, 2, 5, 10):
        m = ast.mehra_prescott(0.99, g, mu=p["mu"], delta=p["delta"], phi=p["phi"])
        edge[str(g)] = m
    return {"rf": pts[:, 2].tolist(), "premium": pts[:, 3].tolist(), "gamma": pts[:, 0].tolist(),
            "beta": pts[:, 1].tolist(), "max_premium_rf4": float(best[3]), "at_gamma": float(best[0]),
            "at_beta": float(best[1]), "at_rf": float(best[2]), "beta99": edge, **p}


def compute_hj() -> dict:
    mo = _moments(1889, 2009)
    gam = np.linspace(0, 30, 121)
    hj = ast.hj_bound(mo["sharpe"], mo["sd_growth"], gam)
    need = hj["needed_gamma"]
    beta = 0.99
    rf_need = float(np.exp(-np.log(beta) + need * mo["growth"] - need ** 2 * mo["sd_growth"] ** 2 / 2) - 1)
    return {**hj, "moments": mo, "rf_at_need": rf_need, "beta": beta}


def compute_ccapm() -> dict:
    out = {}
    for k, (a, b) in {"mp_window": (1889, 1978), "long": (1889, 2009)}.items():
        mo = _moments(a, b)
        out[k] = {**mo, "implied_gamma": mo["premium"] / mo["cov"]}
    return out


def compute_disasters() -> dict:
    d = TRUTH["disasters"]
    beta = float(np.exp(-d["rho"]))
    kw = {"g": d["g"], "sd": d["sd"], "sizes": d["sizes"], "weights": d["weights"]}
    rows = []
    for g in d["gammas"]:
        w = ast.disasters(beta, g, p=d["p"], **kw)
        wo = ast.disasters(beta, g, p=0.0, **kw)
        rows.append({"gamma": g, "with": w, "without": wo})
    gam = np.linspace(0.5, 4.2, 60)
    curve_w = [ast.disasters(beta, float(g), p=d["p"], **kw) for g in gam]
    curve_o = [ast.disasters(beta, float(g), p=0.0, **kw) for g in gam]
    return {"rows": rows, "gamma": gam.tolist(), "premium_with": [c["premium"] if c else None for c in curve_w],
            "rf_with": [c["rf"] if c else None for c in curve_w], "premium_without": [c["premium"] for c in curve_o],
            "rf_without": [c["rf"] for c in curve_o], "mean_size": float(np.dot(d["sizes"], d["weights"]) /
                                                                         np.sum(d["weights"])), **d}


def compute_habit() -> dict:
    h = TRUTH["habit"]
    return {**ast.habit(**h), **h}


def compute_volatility() -> dict:
    s = _shiller()
    m = np.isfinite(s["RealP"]) & np.isfinite(s["Pstar"])
    y = s["year"][m]
    return {"years": y.tolist(), "P": s["RealP"][m].tolist(), "Pstar": s["Pstar"][m].tolist(),
            "PstarC": [float(x) if np.isfinite(x) else None for x in s["PstarC"][m]],
            "sd_P": float(s["RealP"][m].std()), "sd_Pstar": float(s["Pstar"][m].std()), "first": int(y[0]),
            "last": int(y[-1])}


def compute_predict() -> dict:
    s = _shiller()
    y, R, P, D = s["year"], s["Return"], s["RealP"], s["RealD"]
    r = np.log1p(R)
    dp = np.log(D / P)
    rows = []
    for k in (1, 5, 10):
        xs, ys = [], []
        for i in range(len(y)):
            if i + k <= len(y) and np.all(np.isfinite(r[i:i + k])) and np.isfinite(dp[i]):
                xs.append(dp[i])
                ys.append(r[i:i + k].sum())
        xs, ys = np.array(xs), np.array(ys)
        b = np.polyfit(xs, ys, 1)
        res = ys - np.polyval(b, xs)
        rows.append({"k": k, "n": int(len(xs)), "slope": float(b[0]), "r2": float(1 - res.var() / ys.var()),
                     "x": xs.tolist(), "y": ys.tolist()})
    return {"rows": rows}


def compute_ssw() -> dict:
    p = TRUTH["ssw"]
    return {**ast.ssw_market(**p), **p}


def compute_housing() -> dict:
    hp, rent = data.fred("CSUSHPINSA"), data.fred("CUSR0000SEHA")
    rmap = dict(zip(rent["date"], rent["value"]))
    dates = [d for d in hp["date"] if d in rmap]
    ratio = np.array([hp["value"][hp["date"].index(d)] / rmap[d] for d in dates])
    base = ratio[dates.index("2000-01-01")]
    ratio = ratio / base
    t = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in dates]
    k = int(np.argmax(ratio[: dates.index("2012-01-01")]))
    k2 = dates.index("2012-01-01") + int(np.argmin(ratio[dates.index("2012-01-01"): dates.index("2013-12-01")]))
    return {"t": t, "ratio": ratio.tolist(), "peak": float(ratio[k]), "peak_when": dates[k], "trough": float(ratio[k2]),
            "trough_when": dates[k2], "last": float(ratio[-1]), "last_when": dates[-1],
            "retrieved": hp["retrieved"]}


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0
FILM_FIRST, FILM_LAST = 1871, 2013


def film_time(year: float) -> float:
    return 1.5 + FILM_SECONDS * (year - FILM_FIRST) / (FILM_LAST - FILM_FIRST)


def compute_film() -> dict:
    s = _shiller()
    m = np.isfinite(s["Return"]) & np.isfinite(s["RealR"])
    y = s["year"][m]
    stock = np.r_[1.0, np.cumprod(1 + s["Return"][m])]
    bill = np.r_[1.0, np.cumprod(s["RealR"][m])]
    years = np.r_[y[0], y + 1]
    events = [(1929, r"1929"), (1973, r"1973--74"), (2000, r"2000"), (2008, r"2008")]
    return {"years": years.tolist(), "stock": stock.tolist(), "bill": bill.tolist(),
            "times": [film_time(x) for x in years], "events": [{"year": a, "say": b, "time": film_time(a)}
                                                              for a, b in events],
            "stock_end": float(stock[-1]), "bill_end": float(bill[-1]), "last": int(years[-1])}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = np.array(f["years"], float)
    vals = np.array(f["stock"])
    times = [film_time(x) for x in years]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=5, log=True, low=40, high=86)
    events = {"film_end": film_time(FILM_LAST) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.2, "hz": score.hz(nn), "name": str(int(x))}
                       for t, nn, x in zip(times, mel["notes"], years)],
                meta={"label": "a real dollar invested in the S&P composite in 1871, year by year to 2013 (Shiller), as "
                               "a rising tune on a log scale (computed)", "kind": "synthesized"})
    ClipStore("econ23").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": years.tolist(), "seconds": MELODY_SECONDS}


ITEMS = {
    "moments": compute_moments,
    "playit": compute_playit,
    "gordon": compute_gordon,
    "firm": compute_firm,
    "option": compute_option,
    "region": compute_region,
    "hj": compute_hj,
    "ccapm": compute_ccapm,
    "disasters": compute_disasters,
    "habit": compute_habit,
    "volatility": compute_volatility,
    "predict": compute_predict,
    "ssw": compute_ssw,
    "housing": compute_housing,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
