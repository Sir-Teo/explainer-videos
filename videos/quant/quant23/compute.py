"""Every number in Part 23 (Risk and Return), computed and cached in .cache/quant23/.

    python -m videos.quant.quant23.compute [items] [--force]

* ``frontier``  the mean-variance frontier of ten US industries, 1990-2020: the bullet, GMV, tangency, the CML; the
                in-sample tangency against its out-of-sample record and against 1/N;
* ``twoasset``  two assets with 20% volatility each: the frontier as the correlation changes;
* ``capm``      the security market line on beta-sorted deciles, 1963-2020: predicted against realised;
* ``hj``        Hansen-Jagannathan: the largest Sharpe ratios of the market, ten industries and 25 size and value
                portfolios, the gross-return bound, and the CRRA consumption SDF's sigma(m)/E(m) as risk aversion rises;
* ``puzzle``    the equity premium puzzle on annual US data, 1948-2025: consumption growth, the premium, the implied risk
                aversion, and a GMM fit of the Euler equations (Hansen and Singleton);
* ``shiller``   Shiller's excess volatility on Shiller's own data, 1871-2022: the price against the ex post rational price;
                the Campbell-Shiller decomposition of the dividend yield;
* ``intermediary`` He, Kelly and Manela's capital ratio and factor; two-pass tests on their seven asset classes;
* ``apt``       principal components of 49 industries: how many factors, and how well they price the cross-section;
* ``limits``    Shleifer and Vishny's performance-based arbitrage; the Gabaix-Koijen multiplier;
* ``bubbles``   Greenwood, Shleifer and You's run-ups on 49 industries, 1926-2025; the Nasdaq, 1995-2003.
"""

from __future__ import annotations

import json

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import econ as E, premia as P

CACHE = Cache("quant23")
load = CACHE.load
THROUGH = "2025-12"
RESEARCH = "2020-12"  # strategy-like tests (fit, then hold) stay inside the research window; 2021- is sealed


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _ff():
    f = data.ken_french_factors_monthly(THROUGH)
    return f["date"], f["mkt_rf"], f["rf"]


def _align(dates_a, A, dates_b):
    idx = np.searchsorted(dates_a, dates_b)
    return A[idx]


def compute_frontier() -> dict:
    ind = data.ken_french_industries(10, RESEARCH)
    fd, mkt, rf = _ff()
    sel = (ind["date"] >= 199001) & (ind["date"] <= 202012)
    d = ind["date"][sel]
    R = ind["returns"][sel]
    r_f = _align(fd, rf, d)
    m_ex = _align(fd, mkt, d)
    ex = R - r_f[:, None]
    mu, S = R.mean(0) * 12, np.cov(R.T) * 12
    rfa = r_f.mean() * 12
    k = P.frontier_constants(mu, S)
    g = P.gmv(S)
    t = P.tangency(mu, S, rfa)
    ms = np.linspace(k["A"] / k["C"] - 0.06, 0.26, 120)
    sig = P.frontier_sigma(ms, mu, S)
    assets = [{"name": c, "mu": float(mu[j]), "sd": float(np.sqrt(S[j, j]))} for j, c in enumerate(ind["columns"])]
    mkt_pt = {"mu": float((m_ex + r_f).mean() * 12), "sd": float((m_ex + r_f).std() * np.sqrt(12))}
    # in-sample 1990-2007 against out-of-sample 2008-2020 (the research window's end)
    a = d <= 200712
    b = ~a
    mu_a, S_a = R[a].mean(0) * 12, np.cov(R[a].T) * 12
    ta = P.tangency(mu_a, S_a, r_f[a].mean() * 12)
    w = ta["w"]
    oos = ex[b] @ w
    eq = ex[b].mean(1)
    gmv_a = P.gmv(S_a)["w"]
    oos_g = ex[b] @ gmv_a

    def sr(x):
        return float(x.mean() / x.std() * np.sqrt(12))
    return _json({"columns": ind["columns"], "mu": mu, "sd": np.sqrt(np.diag(S)), "ms": ms, "sig": sig,
                  "gmv": {"w": g["w"], "mu": float(g["w"] @ mu), "sd": float(np.sqrt(g["var"]))},
                  "tan": {"w": t["w"], "mu": t["mean"], "sd": t["sd"], "sharpe": t["sharpe"]}, "rf": rfa,
                  "assets": assets, "mkt": mkt_pt, "mkt_sharpe": float(m_ex.mean() / m_ex.std() * np.sqrt(12)),
                  "oos": {"w": w, "in_sharpe": ta["sharpe"], "oos_sharpe": sr(oos), "eq_sharpe": sr(eq),
                          "gmv_sharpe": sr(oos_g), "mkt_sharpe": sr(m_ex[b]), "max_w": float(np.max(np.abs(w))),
                          "short": float(w[w < 0].sum())},
                  "start": int(d[0]), "end": int(d[-1])})


def compute_twoasset() -> dict:
    out = []
    ws = np.linspace(-0.5, 1.5, 81)
    for rho in (-1.0, -0.5, 0.0, 0.5, 1.0):
        mu1, mu2, s = 0.06, 0.10, 0.20
        sd = np.sqrt(ws ** 2 * s * s + (1 - ws) ** 2 * s * s + 2 * ws * (1 - ws) * rho * s * s)
        out.append({"rho": rho, "w": ws, "mu": ws * mu1 + (1 - ws) * mu2, "sd": sd,
                    "gmv": P.two_asset_gmv(s, s, rho)})
    return _json({"curves": out})


def compute_capm() -> dict:
    b = data.ken_french_sorts("BETA", RESEARCH)
    cols = b["columns"]
    dec = [i for i, c in enumerate(cols) if c in ("Lo 10", "Dec 2", "Dec 3", "Dec 4", "Dec 5", "Dec 6", "Dec 7", "Dec 8",
                                                  "Dec 9", "Hi 10")]
    fd, mkt, rf = _ff()
    d = b["date"]
    R = b["returns"][:, dec]
    r_f, m = _align(fd, rf, d), _align(fd, mkt, d)
    ex = R - r_f[:, None]
    c = P.capm_betas(ex, m)
    means = ex.mean(0) * 12
    s = P.sml(c["beta"], means)
    # the long-short: low beta minus high beta, levered to beta-neutral (Frazzini-Pedersen's idea, crude)
    lo, hi = ex[:, 0], ex[:, -1]
    bab = lo / c["beta"][0] - hi / c["beta"][-1]
    return _json({"beta": c["beta"], "alpha": c["alpha"] * 12, "means": means, "mkt_prem": float(m.mean() * 12),
                  "sml": s, "start": int(d[0]), "end": int(d[-1]), "bab_mean": float(bab.mean() * 12),
                  "bab_sharpe": float(bab.mean() / bab.std() * np.sqrt(12)),
                  "bab_t": float(bab.mean() / bab.std() * np.sqrt(len(bab)))})


def _annual_consumption():
    """Real per-capita consumption (PCE) in each year's fourth quarter: Q4-to-Q4 growth lines up with the
    December-to-December returns (an annual average would blur the timing and hide the covariance)."""
    c = data.fred("A794RX0Q048SBEA", "1947-01-01", "2025-12-31")
    d = np.asarray(c["date"])
    y, mth = d // 10000, d // 100 % 100
    v = np.asarray(c["value"])
    q4 = mth == 10
    return y[q4], v[q4]


def _annual_returns():
    fd, mkt, rf = _ff()
    y = fd // 100
    ys = np.unique(y)
    rm = np.array([np.prod(1 + (mkt + rf)[y == k]) - 1 for k in ys if (y == k).sum() == 12])
    r0 = np.array([np.prod(1 + rf[y == k]) - 1 for k in ys if (y == k).sum() == 12])
    ys = np.array([k for k in ys if (y == k).sum() == 12])
    cpi = data.fred("CPIAUCSL", "1947-01-01", "2025-12-31")
    cy = np.asarray(cpi["date"]) // 10000
    cv = np.asarray(cpi["value"])
    dec = {k: cv[(cy == k)][-1] for k in np.unique(cy) if (cy == k).sum() == 12}
    infl = np.array([dec[k] / dec[k - 1] - 1 if (k in dec and k - 1 in dec) else np.nan for k in ys])
    return ys, rm, r0, infl


def compute_puzzle() -> dict:
    yc, cons = _annual_consumption()
    gc = cons[1:] / cons[:-1]
    yg = yc[1:]
    yr, rm, r0, infl = _annual_returns()
    common = np.intersect1d(yg, yr)
    common = common[np.isfinite(infl[np.searchsorted(yr, common)])]
    g = gc[np.searchsorted(yg, common)]
    i = np.searchsorted(yr, common)
    Rm = (1 + rm[i]) / (1 + infl[i])
    Rf = (1 + r0[i]) / (1 + infl[i])
    dc = np.log(g)
    rmx = np.log(Rm)
    prem = float(np.mean(Rm - Rf))
    cov = float(np.cov(dc, rmx)[0, 1])
    corr = float(np.corrcoef(dc, rmx)[0, 1])
    gam = P.implied_gamma(prem, cov)
    # GMM with the market and the bill, instruments: a constant and last year's growth and market return
    Z = np.c_[np.ones(len(g) - 1), g[:-1], Rm[:-1]]
    f = P.euler_moments(g[1:], np.c_[Rm[1:], Rf[1:]], Z)
    est = E.gmm(f, np.array([0.98, 5.0]), lags=0)
    # the HJ comparison: sigma(m)/E(m) of the CRRA SDF for a range of gamma
    gams = np.array([1, 2, 5, 10, 20, 30, 50, 75, 100], float)
    ratios = np.array([P.sdf_ratio(g, gm) for gm in gams])
    return _json({"years": common, "dc": dc, "rm": rmx, "Rf": Rf, "prem": prem, "sd_dc": float(dc.std()),
                  "sd_rm": float(rmx.std()), "cov": cov, "corr": corr, "gamma_implied": gam,
                  "rf_mean": float(np.mean(Rf - 1)), "gmm": {k: (v.tolist() if hasattr(v, "tolist") else v)
                                                             for k, v in est.items() if k in ("theta", "se", "J",
                                                                                              "df", "p_J", "n")},
                  "gams": gams, "ratios": ratios, "sharpe": float((Rm - Rf).mean() / (Rm - Rf).std())})


def compute_hj() -> dict:
    fd, mkt, rf = _ff()
    sel = (fd >= 196307) & (fd <= 202012)
    m = mkt[sel]
    ind = data.ken_french_industries(10, RESEARCH)
    si = (ind["date"] >= 196307) & (ind["date"] <= 202012)
    rfi = _align(fd, rf, ind["date"][si])
    exi = ind["returns"][si] - rfi[:, None]
    ff25 = data._kf_monthly("25_Portfolios_5x5_CSV.zip", "ff25", RESEARCH, "value")
    s5 = (ff25["date"] >= 196307) & (ff25["date"] <= 202012)
    rf5 = _align(fd, rf, ff25["date"][s5])
    ex5 = ff25["returns"][s5] - rf5[:, None]
    sr_m = float(m.mean() / m.std() * np.sqrt(12))
    sr_i = P.hj_excess(exi.mean(0), np.cov(exi.T)) * np.sqrt(12)
    sr_5 = P.hj_excess(ex5.mean(0), np.cov(ex5.T)) * np.sqrt(12)
    # out of sample: the 25 portfolios' tangency fitted on 1963-1993, applied to 1994-2020
    h = ff25["date"][s5] <= 199312
    w = np.linalg.solve(np.cov(ex5[h].T), ex5[h].mean(0))
    o = ex5[~h] @ w
    sr_5_oos = float(o.mean() / o.std() * np.sqrt(12))
    # the gross-return bound with the market and the bill, annual
    yr, rm, r0, infl = _annual_returns()
    ok = np.isfinite(infl)
    R = np.c_[(1 + rm[ok]) / (1 + infl[ok]), (1 + r0[ok]) / (1 + infl[ok])]
    Em = np.linspace(0.95, 1.01, 61)
    bound = P.hj_gross(R.mean(0), np.cov(R.T), Em)
    yc, cons = _annual_consumption()
    g = cons[1:] / cons[:-1]
    pts = []
    for gm in (1, 2, 5, 10, 20, 30, 50):
        mm = P.crra_sdf(g, gm, 0.98)
        pts.append({"gamma": gm, "Em": float(mm.mean()), "sd": float(mm.std())})
    return _json({"sr_mkt": sr_m, "sr_ind": float(sr_i), "sr_ff25": float(sr_5), "sr_ff25_oos": sr_5_oos,
                  "Em": Em, "bound": bound, "pts": pts})


def compute_shiller() -> dict:
    s = data.shiller("2025-06")
    t, p, dv, cpi = (np.asarray(s[k], float) for k in ("t", "price", "div", "cpi"))
    jan = np.isclose(t % 1, 0, atol=1e-6) & np.isfinite(dv)
    yrs = t[jan].astype(int)
    keep = yrs <= 2022
    yrs = yrs[keep]
    P_ = (p[jan] / cpi[jan] * cpi[jan][keep][-1])[keep]
    D_ = (dv[jan] / cpi[jan] * cpi[jan][keep][-1])[keep]
    # annual real returns and dividend growth (January to January)
    r = np.log((P_[1:] + D_[1:]) / P_[:-1])
    dg = np.log(D_[1:] / D_[:-1])
    dp = np.log(D_ / P_)
    rbar = float(np.mean((P_[1:] + D_[1:]) / P_[:-1] - 1))
    # the detrended series, as Shiller plotted them: divide by the exponential trend of the price
    tt = yrs - yrs[0]
    b = np.polyfit(tt, np.log(P_), 1)
    trend = np.exp(np.polyval(b, tt))
    growth = np.exp(b[0]) - 1
    disc = (1 + rbar) / (1 + growth) - 1  # the discount rate on detrended dividends
    pstar = P.ex_post_rational(D_ / trend, disc, terminal=float(np.mean((P_ / trend)[-10:])))
    cs = P.cs_decomposition(dp[:-1], r, dg, horizon=15)
    return _json({"years": yrs, "p": P_ / trend, "pstar": pstar, "sd_p": float(np.std(P_ / trend)),
                  "sd_pstar": float(np.std(pstar)), "rbar": rbar, "growth": float(growth), "cs": cs,
                  "dp": dp, "dp_mean": float(dp.mean())})


def compute_intermediary() -> dict:
    q = data.hkm("quarterly_assets")
    m = data.hkm("monthly")
    cols = q["columns"]
    classes = {"FF25": "stocks", "US_bonds": "US bonds", "Sov_bonds": "sovereign bonds", "Options": "options",
               "CDS": "CDS", "Commod": "commodities", "FX": "currencies"}
    out = {}
    for pre, name in classes.items():
        names = [c for c in cols if c.startswith(pre + "_")]
        A = np.stack([q[c] for c in names], 1)
        ok = np.all(np.isfinite(A), 1) & np.isfinite(q["intermediary_capital_risk_factor"])
        A = A[ok]
        rf = q["rf"][ok]
        ex = A - rf[:, None]
        F = np.c_[q["mkt_rf"][ok], q["intermediary_capital_risk_factor"][ok]]
        tp = E.two_pass(ex, F, shanken=True)
        tp1 = E.two_pass(ex, F[:, [0]], shanken=True)

        def r2(t_):
            mu = t_["mean_returns"]
            fit = np.c_[np.ones(len(mu)), t_["betas"]] @ t_["lambda"]
            return float(1 - np.sum((mu - fit) ** 2) / np.sum((mu - mu.mean()) ** 2))
        out[name] = {"n": int(ok.sum()), "N": len(names), "lam": tp["lambda"], "t": tp["t_shanken"], "r2": r2(tp),
                     "r2_capm": r2(tp1), "lam_capm": tp1["lambda"], "t_capm": tp1["t_shanken"]}
    t = m["date"] // 100 + (m["date"] % 100 - 0.5) / 12
    return _json({"classes": out, "t": t, "ratio": m["intermediary_capital_ratio"],
                  "factor": m["intermediary_capital_risk_factor"]})


def compute_apt() -> dict:
    ind = data.ken_french_industries(49, THROUGH)
    fd, mkt, rf = _ff()
    sel = (ind["date"] >= 197001) & (ind["date"] <= 202512)
    R = ind["returns"][sel]
    ok = np.all(np.isfinite(R), 0)
    R = R[:, ok]
    r_f = _align(fd, rf, ind["date"][sel])
    m = _align(fd, mkt, ind["date"][sel])
    ex = R - r_f[:, None]
    C = np.cov(ex.T)
    w, V = np.linalg.eigh(C)
    w, V = w[::-1], V[:, ::-1]
    share = w / w.sum()
    pcs = ex @ V[:, :10]
    corr1 = float(abs(np.corrcoef(pcs[:, 0], m)[0, 1]))
    r2 = []
    for k in (1, 3, 5, 10):
        X = np.c_[np.ones(len(m)), pcs[:, :k]]
        B, *_ = np.linalg.lstsq(X, ex, rcond=None)
        betas = B[1:].T
        mu = ex.mean(0)
        Xc = np.c_[np.ones(len(mu)), betas]
        lam, *_ = np.linalg.lstsq(Xc, mu, rcond=None)
        fit = Xc @ lam
        r2.append({"k": k, "r2": float(1 - np.sum((mu - fit) ** 2) / np.sum((mu - mu.mean()) ** 2))})
    return _json({"share": share[:15], "cum": np.cumsum(share)[:15], "corr_pc1_mkt": corr1, "r2": r2,
                  "N": int(ok.sum())})


def compute_limits() -> dict:
    a_s = np.linspace(0, 3.0, 61)
    rows = [P.shleifer_vishny(V=1.0, S1=0.3, S2=0.4, F1=0.2, a=a) for a in a_s]
    return _json({"a": a_s, "p2": [r_["p2"] for r_ in rows], "F2": [r_["F2"] for r_ in rows],
                  "p1": rows[0]["p1"], "nw": rows[0]["no_withdrawal_p2"], "gk": P.gk_multiplier(0.2)})


def compute_bubbles() -> dict:
    ind = data.ken_french_industries(49, THROUGH)
    fd, mkt, rf = _ff()
    R = ind["returns"]
    Rm = _align(fd, mkt + rf, ind["date"])
    out = P.run_ups(np.nan_to_num(R, nan=0.0), Rm, months=24, threshold=1.0, crash=0.4, horizon=24)
    ev = out["events"]
    cols = ind["columns"]
    ex = [{"ind": cols[e["j"]], "ym": int(ind["date"][e["t"]]), "raw": e["raw"], "crash": e["crash"],
           "next": e["next"]} for e in ev]
    n = data.fred("NASDAQCOM", "1971-02-05", "2025-12-31")
    nd, nv = np.asarray(n["date"]), np.asarray(n["value"])
    s = (nd >= 19950101) & (nd <= 20031231)
    k = int(np.argmax(nv * s))
    after = s & (nd > nd[k])
    j = int(np.where(after)[0][np.argmin(nv[after])])
    t = nd // 10000 + (nd // 100 % 100 - 1) / 12 + (nd % 100 - 1) / 365
    return _json({"events": ex, "n": out["n"], "p_crash": out["p_crash"], "mean_next": out["mean_next"],
                  "nasdaq": {"t": t[s][::3], "v": nv[s][::3], "peak": {"date": int(nd[k]), "v": float(nv[k])},
                             "trough": {"date": int(nd[j]), "v": float(nv[j])}}})


def compute_hook() -> dict:
    fd, mkt, rf = _ff()
    t = fd // 100 + (fd % 100 - 0.5) / 12
    st = np.cumprod(1 + mkt + rf)
    bi = np.cumprod(1 + rf)
    yrs = (len(fd)) / 12
    return _json({"t": t[::3], "stocks": st[::3], "bills": bi[::3], "end_stocks": float(st[-1]),
                  "end_bills": float(bi[-1]), "years": yrs, "cagr_s": float(st[-1] ** (1 / yrs) - 1),
                  "cagr_b": float(bi[-1] ** (1 / yrs) - 1), "start": int(fd[0]), "end": int(fd[-1])})


def compute_disaster() -> dict:
    """Barro's (2006) rare disasters, simplified: lognormal consumption growth (sigma 2%) plus, with probability p a
    year, a contraction by b; for a claim on consumption the premium is about gamma sigma^2 + p E[b (1 - b)^-gamma].
    p = 1.7% and mean b = 0.29 are Barro's calibration; a fixed b is used here, so the numbers are a lower bound."""
    gams = np.linspace(1, 10, 37)
    sig, p = 0.02, 0.017
    out = {}
    for b in (0.29, 0.40):
        out[str(b)] = gams * sig ** 2 + p * b * (1 - b) ** (-gams)
    base = gams * sig ** 2
    return _json({"gams": gams, "prem": out, "base": base, "p": p, "sig": sig})


def compute_speculation_theory() -> dict:
    """The research chapter: speculative bubbles from disagreement (Harrison and Kreps 1978).  Two types of risk-neutral
    investors disagree about a two-state Markov dividend; short sales are impossible; the asset is held by whoever
    values it most, including the option to resell.  The price solves P = beta max_i Q_i (d + P) and exceeds every
    type's own buy-and-hold valuation V_i = sum beta^t Q_i^t d: the difference is the value of the resale option.
    Harrison and Kreps's own example, then a sweep of disagreement with the turnover it implies."""
    beta = 0.75
    d = np.array([0.0, 1.0])
    Q1 = np.array([[1 / 2, 1 / 2], [2 / 3, 1 / 3]])
    Q2 = np.array([[2 / 3, 1 / 3], [1 / 4, 3 / 4]])

    def bh(Q):
        return np.linalg.solve(np.eye(2) - beta * Q, beta * Q @ d)

    def spec(Qs):
        P = np.zeros(2)
        for _ in range(5000):
            P = beta * np.max(np.stack([Q @ (d + P) for Q in Qs]), axis=0)
        holder = np.argmax(np.stack([Q @ (d + P) for Q in Qs]), axis=0)
        return P, holder
    P, holder = spec([Q1, Q2])
    V1, V2 = bh(Q1), bh(Q2)
    hk = {"beta": beta, "Q1": Q1, "Q2": Q2, "V1": V1, "V2": V2, "P": P, "holder": holder,
          "premium": P - np.maximum(V1, V2), "iterations_check": float(np.max(np.abs(P - beta * np.maximum(Q1 @ (d + P),
                                                                                                    Q2 @ (d + P)))))}
    # disagreement sweep: beliefs symmetric around a common (true) chain
    Qbar = 0.5 * (Q1 + Q2)
    D = 0.5 * (Q1 - Q2)
    pi = np.linalg.eig(Qbar.T)[1][:, 0].real
    pi = pi / pi.sum()
    rows = []
    for lam in np.linspace(0, 1.0, 21):
        A, B = Qbar + lam * D, Qbar - lam * D
        Pl, hl = spec([A, B])
        Vmax = np.maximum(bh(A), bh(B))
        Vtrue = bh(Qbar)
        # turnover under the true chain: the chance the holder type changes from one state to the next
        switch = sum(pi[s_] * Qbar[s_, t_] * (hl[s_] != hl[t_]) for s_ in range(2) for t_ in range(2))
        rows.append({"lam": float(lam), "P": Pl, "Vmax": Vmax, "Vtrue": Vtrue,
                     "bubble_vs_true": float(np.dot(pi, Pl - Vtrue)), "premium": float(np.dot(pi, Pl - Vmax)),
                     "turnover": float(switch)})
    return _json({"hk": hk, "sweep": rows, "pi": pi})


ITEMS = {"speculation_theory": compute_speculation_theory, "frontier": compute_frontier, "twoasset": compute_twoasset, "capm": compute_capm, "hj": compute_hj,
         "puzzle": compute_puzzle, "shiller": compute_shiller, "intermediary": compute_intermediary,
         "apt": compute_apt, "limits": compute_limits, "bubbles": compute_bubbles, "hook": compute_hook,
         "disaster": compute_disaster}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
