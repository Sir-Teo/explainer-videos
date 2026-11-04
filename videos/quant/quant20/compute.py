"""Every number in Part 20 (Credit), computed and cached in .cache/quant20/.

    python -m videos.quant.quant20.compute [items] [--force]

* ``spreads``   Moody's Baa and Aaa yields over the 10-year Treasury, monthly since 1953 (Baa since 1919 against the
                long Treasury proxy is not used), daily since 1986; peaks, and recessions;
* ``merton``    Merton's spreads over (leverage, asset volatility) and by maturity: the structural model's shapes;
* ``kmv``       distances to default every day, 2018-2025, for Boeing, American Airlines and Norwegian Cruise Line:
                equity from prices and shares outstanding, the default point from their 10-Q/10-K liabilities;
* ``blackcox``  terminal against first-passage default over horizons;
* ``hazard``    survival as discounting: simulated default times, and risky zeros under two recovery conventions;
* ``cds``       a hazard curve bootstrapped from (illustrative) par spreads, the legs, and the Big Bang's upfronts;
* ``defaults``  bankruptcy filings (8-K Item 1.03) by SEC registrants each year 2009-2025, against the Baa spread;
* ``dataset``   firm-years 2010-2023 from EDGAR's XBRL frames: Altman's ratios and more, labelled by a bankruptcy
                filing 3 to 15 months after the fiscal year;
* ``models``    Altman's Z, a logit and gradient-boosted trees, fitted to 2010-2016, chosen on 2017-2020, and
                registered before the sealed 2021-2023 firm-years are opened;
* ``vasicek``   the large pool's loss distribution and the Basel IRB capital curve;
* ``copula``    Gaussian and t copulas: two names' latent variables, a 125-name pool's losses, tranche expected
                losses against correlation, and the base-correlation skew a t-copula market produces;
* ``cjs``       Coval, Jurek and Stafford's point: a senior tranche's losses arrive only in the worst states;
* ``march2020`` corporate bond ETFs (LQD, HYG) and the Baa spread through March-April 2020;
* ``bdc``       a listed private-credit lender (Ares Capital): price against reported net asset value per share;
* ``envelope``  the trial counter after this part's registrations.
"""

from __future__ import annotations

import inspect
import json

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import credit as CR, pit
from scipy.stats import norm

CACHE = Cache("quant20")
load = pit.counted(CACHE.load, 20, items=("models",))


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _fy(d):
    d = np.asarray(d)
    return d // 10000 + (d // 100 % 100 - 1) / 12 + (d % 100 - 1) / 365


# ---------------------------------------------------------------------------
# Spreads
# ---------------------------------------------------------------------------
def compute_spreads() -> dict:
    baa, aaa, gs10 = (data.fred(s, "1953-04-01", "2025-12-31") for s in ("BAA", "AAA", "GS10"))
    d = np.intersect1d(np.intersect1d(baa["date"], aaa["date"]), gs10["date"])

    def at(f):
        return f["value"][np.searchsorted(f["date"], d)]
    sb, sa = at(baa) - at(gs10), at(aaa) - at(gs10)
    daily = data.fred("BAA10Y", "1986-01-01", "2025-12-31")
    rec = data.fred("USREC", "1953-01-01", "2025-12-31")
    k = int(np.argmax(daily["value"]))
    pk = {}
    for a, b in ((19800101, 19830101), (20080101, 20100101), (20200101, 20201231)):
        s_ = (daily["date"] >= a) & (daily["date"] < b) if a >= 19860101 else (d >= a) & (d < b)
        if a >= 19860101:
            j = int(np.argmax(np.where(s_, daily["value"], -9)))
            pk[str(a // 10000)] = {"date": int(daily["date"][j]), "v": float(daily["value"][j])}
        else:
            j = int(np.argmax(np.where(s_, sb, -9)))
            pk[str(a // 10000)] = {"date": int(d[j]), "v": float(sb[j])}
    return _json({"t": _fy(d), "baa": sb, "aaa": sa, "daily_t": _fy(daily["date"]), "daily": daily["value"],
                  "max": {"date": int(daily["date"][k]), "v": float(daily["value"][k])}, "peaks": pk,
                  "rec_t": _fy(rec["date"]), "rec": rec["value"], "mean_baa": float(sb.mean()),
                  "mean_aaa": float(sa.mean()), "end": float(daily["value"][-1])})


# ---------------------------------------------------------------------------
# Structural models
# ---------------------------------------------------------------------------
def compute_merton() -> dict:
    r, T = 0.04, 5.0
    lev = np.linspace(0.1, 0.9, 33)  # D e^{-rT} / V
    vol = np.linspace(0.1, 0.6, 26)
    Z = np.array([[CR.merton_spread(1.0, s, L * np.exp(r * T), r, T) for L in lev] for s in vol]) * 1e4
    Ts = np.linspace(0.05, 20, 120)
    term = {}
    for name, L, s in (("safe", 0.3, 0.2), ("middling", 0.6, 0.25), ("distressed", 1.05, 0.3)):
        term[name] = [float(CR.merton_spread(1.0, s, L, r, t) * 1e4) for t in Ts]
    return _json({"lev": lev, "vol": vol, "spread_bp": Z, "r": r, "T": T, "Ts": Ts, "term": term})


KMV_FIRMS = {"BA": (12927, "Boeing"), "AAL": (6201, "American Airlines"), "NCLH": (1513761, "Norwegian Cruise Line")}


def _quarterly(facts, concept):
    rows = facts.get(concept, [])
    best = {}
    for x in rows:  # keep, for each period end, the earliest filing (what was known first)
        e = int(x["end"].replace("-", ""))
        f = int(x["filed"].replace("-", ""))
        if e not in best or f < best[e][1]:
            best[e] = (float(x["val"]), f)
    ends = sorted(best)
    return np.array([best[e][1] for e in ends]), np.array([best[e][0] for e in ends])


def compute_kmv() -> dict:
    out = {}
    r = 0.03
    for tk, (cik, name) in KMV_FIRMS.items():
        px = data.yahoo_daily(tk, "2017-01-01", "2025-11-30")
        f = data.sec_facts(cik, ("LiabilitiesCurrent", "LongTermDebtNoncurrent", "LongTermDebt",
                                 "dei:EntityCommonStockSharesOutstanding"))["facts"]
        fl, cl = _quarterly(f, "LiabilitiesCurrent")
        ltd_c = "LongTermDebtNoncurrent" if len(f["LongTermDebtNoncurrent"]) else "LongTermDebt"
        fd, ld = _quarterly(f, ltd_c)
        fs, sh = _quarterly(f, "dei:EntityCommonStockSharesOutstanding")
        d = px["date"]
        sel = d >= 20180102
        d, p = d[sel], px["close"][sel]

        def asof(fd_, v_):  # the latest value filed by each day (no look-ahead)
            i = np.searchsorted(fd_, d, side="right") - 1
            return np.where(i >= 0, v_[np.maximum(i, 0)], np.nan)
        E = p * asof(fs, sh) / 1e9
        DP = (asof(fl, cl) + 0.5 * asof(fd, ld)) / 1e9  # KMV's default point: short-term plus half long-term debt
        ok = np.isfinite(E) & np.isfinite(DP)
        d, E, DP, p = d[ok], E[ok], DP[ok], p[ok]
        # one year of equity history at a time: re-estimate the asset volatility each month end, as a desk would
        dtd = np.full(len(d), np.nan)
        sig = np.full(len(d), np.nan)
        months = np.where(np.r_[d[1:] // 100 != d[:-1] // 100, True])[0]
        for m in months:
            lo = max(0, m - 251)
            if m - lo < 200:
                continue
            k = CR.kmv_iterate(E[lo:m + 1], DP[lo:m + 1], r, 1.0)
            mu = max(k["mu"], r)  # a negative trailing drift would double-count the fall
            j0 = 0 if m == months[0] else months[months < m][-1] + 1
            for j in range(j0, m + 1):
                Vj = float(k["V"][j - lo]) if j >= lo else np.nan
                dtd[j] = CR.distance_to_default(Vj, k["sigma_V"], DP[j], mu, 1.0)
                sig[j] = k["sigma_V"]
        w = int(np.nanargmin(dtd))
        out[tk] = {"name": name, "t": _fy(d), "date": d, "E": E, "DP": DP, "dtd": dtd, "sigma_V": sig,
                   "worst": {"date": int(d[w]), "dtd": float(dtd[w]), "pd": float(norm.cdf(-dtd[w])), "E": float(E[w]),
                             "DP": float(DP[w])},
                   "end": {"dtd": float(dtd[-1]), "E": float(E[-1]), "DP": float(DP[-1])}}
    return _json(out)


def compute_blackcox() -> dict:
    V, s, mu, K = 100.0, 0.3, 0.06, 60.0
    T = np.linspace(0.05, 10, 100)
    return _json({"T": T, "terminal": CR.merton_pd(V, s, K, mu, T), "first": CR.black_cox_pd(V, s, mu, K, T),
                  "V": V, "s": s, "mu": mu, "K": K})


# ---------------------------------------------------------------------------
# Reduced form and CDS
# ---------------------------------------------------------------------------
def compute_hazard() -> dict:
    lam, r, R = 0.03, 0.04, 0.4
    rng = np.random.default_rng(0)
    tau = rng.exponential(1 / lam, 200)
    T = np.linspace(0, 10, 101)
    Q = np.exp(-lam * T)
    emp = np.array([np.mean(tau > t) for t in T])
    df = np.exp(-r * T)
    return _json({"lam": lam, "r": r, "R": R, "tau": tau, "T": T, "Q": Q, "emp": emp,
                  "rmv": CR.risky_zero(T, df, Q, R, "RMV"), "rf": CR.risky_zero(T, df, Q, R, "RF"), "df": df})


CDS_QUOTES = {"tenors": [1, 2, 3, 5, 7, 10], "spreads_bp": [60, 85, 110, 150, 170, 185]}  # illustrative


def compute_cds() -> dict:
    def df(t):
        return np.exp(-0.04 * np.asarray(t, float))
    R = 0.4
    ten, sp = CDS_QUOTES["tenors"], np.array(CDS_QUOTES["spreads_bp"]) / 1e4
    k, h = CR.bootstrap_hazard(ten, sp, df, R)
    Tq = np.linspace(0, 10, 201)
    a5, p5 = CR.cds_legs(5.0, k, h, df, R)
    ups = {}
    for name, sp5 in (("investment grade", 0.006), ("crossover", 0.025), ("distressed", 0.12)):
        kk, hh = CR.bootstrap_hazard([5.0], [sp5], df, R)
        cpn = 0.01 if sp5 < 0.02 else 0.05
        ups[name] = {"par": sp5, "coupon": cpn, "upfront": CR.cds_upfront(cpn, 5.0, kk, hh, df, R)}
    return _json({"tenors": ten, "spreads": sp, "knots": k, "hazards": h, "Tq": Tq,
                  "Q": CR.survival(Tq, k, h), "rpv01_5": a5, "prot_5": p5, "triangle_5": CR.credit_triangle(sp[3], R),
                  "R": R, "upfronts": ups})


# ---------------------------------------------------------------------------
# Defaults, and the default-prediction dataset
# ---------------------------------------------------------------------------
def _first_filings():
    """Each company's bankruptcy episodes: the first Item 1.03 filing, and any later one more than two years on."""
    rows = sorted({(c, d) for y in range(2009, 2026) for c, d, *_ in data.sec_bankruptcy_8k(y)})
    eps = {}
    for c, d in rows:
        last = eps.get(c, [])
        if not last or d - last[-1] > 20000:
            eps.setdefault(c, []).append(d)
    return eps


def compute_defaults() -> dict:
    eps = _first_filings()
    years = np.arange(2009, 2026)
    counts = np.array([sum(1 for v in eps.values() for d in v if d // 10000 == y) for y in years])
    s = data.fred("BAA10Y", "2009-01-01", "2025-12-31")
    avg = np.array([s["value"][s["date"] // 10000 == y].mean() for y in years])
    names = {}
    for y in years:
        for c, d, form, name in data.sec_bankruptcy_8k(int(y)):
            names.setdefault(c, name)
    return _json({"years": years, "count": counts, "baa": avg, "corr": float(np.corrcoef(counts, avg)[0, 1]),
                  "total": int(counts.sum()), "firms": len(eps)})


INST = ["Assets", "AssetsCurrent", "LiabilitiesCurrent", "Liabilities", "StockholdersEquity",
        "RetainedEarningsAccumulatedDeficit", "CashAndCashEquivalentsAtCarryingValue"]
FLOW = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "OperatingIncomeLoss",
        "NetIncomeLoss", "NetCashProvidedByUsedInOperatingActivities", "InterestExpense"]
FEATURES = ["WC/TA", "RE/TA", "EBIT/TA", "ME/TL", "S/TA", "NI/TA", "TL/TA", "Cash/TA", "CFO/TA", "log TA", "log ME",
            "Int/TA"]


def _firm_years(y):
    f = {c: data.sec_frame(c, f"CY{y}Q4I") for c in INST}
    g = {c: data.sec_frame(c, f"CY{y}") for c in FLOW}
    fl = data.sec_frame("EntityPublicFloat", f"CY{y}Q2I", taxonomy="dei")
    rows = []
    for cik, (ta, end, *_r) in f["Assets"].items():
        if not isinstance(ta, (int, float)) or ta < 1e7:
            continue
        def v(dct, c=cik):
            x = dct.get(c)
            return float(x[0]) if x is not None else np.nan
        tl = v(f["Liabilities"])
        if not np.isfinite(tl):
            tl = ta - v(f["StockholdersEquity"])
        sales = next((v(g[c]) for c in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
                                         "SalesRevenueNet") if np.isfinite(v(g[c]))), np.nan)
        me = v(fl)
        if not np.isfinite(tl) or tl <= 0 or not np.isfinite(me) or me <= 0:
            continue
        x = [(v(f["AssetsCurrent"]) - v(f["LiabilitiesCurrent"])) / ta, v(f["RetainedEarningsAccumulatedDeficit"]) / ta,
             v(g["OperatingIncomeLoss"]) / ta, me / tl, sales / ta, v(g["NetIncomeLoss"]) / ta, tl / ta,
             v(f["CashAndCashEquivalentsAtCarryingValue"]) / ta, v(g["NetCashProvidedByUsedInOperatingActivities"]) / ta,
             np.log(ta), np.log(me), v(g["InterestExpense"]) / ta]
        rows.append((cik, int(end.replace("-", "")), x))
    return rows


def _label(eps, cik, end):
    """1 if the company's bankruptcy filing falls 3 to 15 months after the fiscal year's end; None (excluded) if it
    was already in bankruptcy in the year before."""
    e = end // 10000 * 12 + end // 100 % 100
    for d in eps.get(cik, []):
        m = d // 10000 * 12 + d // 100 % 100
        if e - 12 < m <= e + 3:
            return None
        if e + 3 < m <= e + 15:
            return 1
    return 0


def compute_dataset() -> dict:
    eps = _first_filings()
    X, y, cik, end, fy = [], [], [], [], []
    for yr in range(2010, 2024):
        for c, e, x in _firm_years(yr):
            lab = _label(eps, c, e)
            if lab is None:
                continue
            X.append(x)
            y.append(lab)
            cik.append(c)
            end.append(e)
            fy.append(yr)
    X = np.array(X, float)
    return _json({"X": X, "y": np.array(y), "cik": np.array(cik), "end": np.array(end), "fy": np.array(fy),
                  "features": FEATURES, "n": len(y), "defaults": int(np.sum(y))})


MODEL_RULE = {"target": "a bankruptcy filing (8-K Item 1.03) 3-15 months after the fiscal year end",
              "features": FEATURES, "fit": "fiscal years 2010-2016", "validation": "2017-2020",
              "holdout": "2021-2023 (sealed)", "prep": "winsorise 1/99% on the fit years, median-impute, standardise",
              "models": ["logit, ridge 1e-3", "boosted trees: depth 3, lr 0.05, min leaf 30, 0.8 rows, "
                         "early stopping on validation log loss, max 600 trees"]}


def _prep(X, fit):
    lo, hi = np.nanpercentile(X[fit], 1, axis=0), np.nanpercentile(X[fit], 99, axis=0)
    Z = np.clip(X, lo, hi)
    med = np.nanmedian(Z[fit], axis=0)
    miss = ~np.isfinite(Z)
    Z = np.where(miss, med, Z)
    mu, sd = Z[fit].mean(0), Z[fit].std(0) + 1e-12
    return (Z - mu) / sd, miss


def _models(X, y, fy):
    fit, val = (fy >= 2010) & (fy <= 2016), (fy >= 2017) & (fy <= 2020)
    Z, miss = _prep(X, fit)
    b = CR.logit_fit(Z[fit], y[fit], l2=1e-3)
    g = CR.GBM(n_trees=600, depth=3, lr=0.05, min_leaf=30, subsample=0.8, seed=0).fit(
        Z[fit], y[fit], X_val=Z[val], y_val=y[val], early_stop=60)
    return Z, b, g


def compute_models() -> dict:
    d = load("dataset")
    X, y, fy = np.asarray(d["X"], float), np.asarray(d["y"], int), np.asarray(d["fy"], int)
    code = inspect.getsource(_prep) + inspect.getsource(_models)
    reg = {"logit_default_holdout": pit.register("logit_default_holdout", code, MODEL_RULE, trials=1),
           "gbm_default_holdout": pit.register("gbm_default_holdout", code, MODEL_RULE, trials=1)}
    Z, b, g = _models(X, y, fy)
    key = fy * 10000 + 1231  # a firm-year dated by its fiscal year's end: 2021 onward is the sealed hold-out
    order = np.lexsort((np.asarray(d["cik"]), key))
    pit.open_envelope("logit_default_holdout", "edgar_default_firm_years", key[order], y[order])
    pit.open_envelope("gbm_default_holdout", "edgar_default_firm_years", key[order], y[order])
    sets = {"fit": (fy >= 2010) & (fy <= 2016), "validation": (fy >= 2017) & (fy <= 2020), "holdout": fy >= 2021}
    alt = CR.altman_z(np.nan_to_num(X[:, :5], nan=0.0))
    pl, pg = CR.logit_predict(b, Z), g.predict_proba(Z)
    res = {}
    for k, s in sets.items():
        res[k] = {"n": int(s.sum()), "defaults": int(y[s].sum()),
                  "auc": {"altman": CR.auc(y[s], -alt[s]), "logit": CR.auc(y[s], pl[s]), "gbm": CR.auc(y[s], pg[s])},
                  "brier": {"logit": CR.brier(y[s], pl[s]), "gbm": CR.brier(y[s], pg[s]),
                            "base": CR.brier(y[s], np.full(s.sum(), y[sets["fit"]].mean()))}}
    h = sets["holdout"]
    roc = {m: [x[::max(1, len(x) // 300)] for x in CR.roc_curve(y[h], sc[h])]
           for m, sc in (("altman", -alt), ("logit", pl), ("gbm", pg))}
    q = np.quantile(pg[h], np.linspace(0, 1, 11))
    dec = np.clip(np.searchsorted(q, pg[h], side="right") - 1, 0, 9)
    calib = {"pred": [float(pg[h][dec == i].mean()) for i in range(10)],
             "real": [float(y[h][dec == i].mean()) for i in range(10)]}
    top = pg[h] >= np.quantile(pg[h], 0.9)
    zones = {"distress": float(y[h][alt[h] < 1.81].mean()), "grey": float(y[h][(alt[h] >= 1.81) & (alt[h] < 2.99)].mean()),
             "safe": float(y[h][alt[h] >= 2.99].mean()),
             "share": [float(np.mean(alt[h] < 1.81)), float(np.mean((alt[h] >= 1.81) & (alt[h] < 2.99))),
                       float(np.mean(alt[h] >= 2.99))]}
    return _json({"results": res, "roc": roc, "calib": calib, "top_decile_capture": float(y[h][top].sum() / y[h].sum()),
                  "logit_beta": b, "gbm_importance": g.importance(len(FEATURES)), "gbm_trees": len(g.trees),
                  "features": FEATURES, "zones": zones, "registered": reg, "trials": pit.trials_so_far(),
                  "rule": MODEL_RULE, "val_loss": g.val_loss})


# ---------------------------------------------------------------------------
# Portfolios: the large pool, bank capital, copulas and tranches
# ---------------------------------------------------------------------------
def compute_vasicek() -> dict:
    x = np.linspace(0.0005, 0.2, 400)
    curves = {}
    for pd_, rho in ((0.02, 0.0001), (0.02, 0.05), (0.02, 0.15), (0.02, 0.3)):
        curves[f"{rho:g}"] = CR.vasicek_loss_pdf(x, pd_, rho)
    pds = np.geomspace(0.0003, 0.2, 60)
    K = CR.basel_irb_k(pds)
    return _json({"x": x, "pdf": curves, "pd": 0.02, "q999": {k: CR.vasicek_quantile(0.999, 0.02, float(k))
                                                             for k in curves},
                  "pds": pds, "K": K, "rho": CR.basel_corporate_rho(pds), "rw_1pct": 12.5 * CR.basel_irb_k(0.01)})


def compute_copula() -> dict:
    rng = np.random.default_rng(0)
    n = 1500
    rho, nu = 0.5, 3
    M = rng.standard_normal(n)
    Z = rng.standard_normal((n, 2))
    G = np.sqrt(rho) * M[:, None] + np.sqrt(1 - rho) * Z
    W = rng.chisquare(nu, n) / nu
    Tt = G / np.sqrt(W)[:, None]
    from scipy.stats import norm, t as st
    pts = {"gauss": norm.cdf(G), "t": st.cdf(Tt, nu)}
    pd_, R, N = 0.02, 0.4, 125
    kg, _ = CR.copula_defaults(N, pd_, 0.2, 40000, seed=1)
    kt, _ = CR.copula_defaults(N, pd_, 0.2, 40000, seed=1, nu=4)
    rhos = np.linspace(0.01, 0.9, 45)
    tr = {"equity 0-3%": (0.0, 0.03), "mezzanine 3-7%": (0.03, 0.07), "senior 15-30%": (0.15, 0.30)}
    el = {k: [CR.lhp_tranche_el(pd_, r_, R, a, d) for r_ in rhos] for k, (a, d) in tr.items()}
    # a 't-copula market': price [0, d] tranches by simulation under t, read off the Gaussian base correlations
    dets = [0.03, 0.07, 0.10, 0.15, 0.30]
    Lt = (1 - R) * kt / N
    base = []
    for d_ in dets:
        e = float(CR.tranche_loss(Lt, 0, d_).mean())
        try:
            base.append(CR.base_correlation(e, pd_, R, d_))
        except ValueError:
            base.append(float("nan"))
    tail = {"gauss": float(np.mean((1 - R) * kg / N > 0.15)), "t": float(np.mean(Lt > 0.15))}
    return _json({"pts": pts, "rho2": rho, "nu": nu, "losses_g": (1 - R) * kg / N, "losses_t": Lt, "rhos": rhos,
                  "el": el, "dets": dets, "base": base, "pd": pd_, "R": R, "N": N, "tail": tail})


def compute_cjs() -> dict:
    """The senior tranche's expected loss conditional on the market factor: an 'economic catastrophe bond'."""
    from scipy.stats import norm
    pd_, rho, R = 0.02, 0.25, 0.4
    m = np.linspace(-4, 2, 121)
    p = norm.cdf((norm.ppf(pd_) - np.sqrt(rho) * m) / np.sqrt(1 - rho))
    L = (1 - R) * p
    out = {"m": m, "pool": L, "senior": CR.tranche_loss(L, 0.15, 0.30), "mezz": CR.tranche_loss(L, 0.03, 0.07),
           "equity": CR.tranche_loss(L, 0.0, 0.03)}
    # the share of the senior tranche's expected loss that arrives in the worst 1% and 5% of states
    z = np.linspace(-9, 9, 20001)
    w = norm.pdf(z) / norm.pdf(z).sum()
    Ls = CR.tranche_loss((1 - R) * norm.cdf((norm.ppf(pd_) - np.sqrt(rho) * z) / np.sqrt(1 - rho)), 0.15, 0.30)
    tot = float(np.sum(w * Ls))
    out["share_worst"] = {q: float(np.sum((w * Ls)[z < norm.ppf(q)]) / tot) for q in (0.001, 0.002, 0.005, 0.01)}
    # the state of the economy below which the senior tranche starts to lose: pool loss (1 - R) p(M) = 15%
    m_star = (norm.ppf(pd_) - np.sqrt(1 - rho) * norm.ppf(0.15 / (1 - R))) / np.sqrt(rho)
    out["threshold_pct"] = float(norm.cdf(m_star))
    out["m_star"] = float(m_star)
    out["params"] = {"pd": pd_, "rho": rho, "R": R}
    out["el_senior"] = tot
    out["el_pool"] = (1 - R) * pd_
    return _json(out)


# ---------------------------------------------------------------------------
# March 2020, and private credit's marks
# ---------------------------------------------------------------------------
def compute_march2020() -> dict:
    out = {}
    for tk in ("LQD", "HYG"):
        p = data.yahoo_daily(tk, "2020-01-01", "2020-06-30")
        k0 = int(np.searchsorted(p["date"], 20200220))
        lo = int(np.argmin(p["close"]))
        out[tk] = {"date": p["date"], "close": p["close"], "peak": float(p["close"][:k0 + 1].max()),
                   "low": {"date": int(p["date"][lo]), "v": float(p["close"][lo])},
                   "drawdown": float(p["close"][lo] / p["close"][:k0 + 1].max() - 1)}
    s = data.fred("BAA10Y", "2020-01-01", "2020-06-30")
    out["baa"] = {"date": s["date"], "v": s["value"]}
    return _json(out)


def compute_bdc() -> dict:
    p = data.yahoo_daily("ARCC", "2018-01-01", "2025-11-30")
    f = data.sec_facts(1287750, ("NetAssetValuePerShare",))["facts"]["NetAssetValuePerShare"]
    best = {}
    for x in f:
        e = int(x["end"].replace("-", ""))
        if x["unit"] == "USD/shares" and 20171231 <= e <= 20251231 and (e not in best or x["filed"] < best[e][1]):
            best[e] = (float(x["val"]), x["filed"])
    ends = np.array(sorted(best))
    nav = np.array([best[e][0] for e in ends])
    i = np.clip(np.searchsorted(p["date"], ends, side="right") - 1, 0, None)
    disc = p["close"][i] / nav - 1
    k = int(np.argmin(p["close"]))
    return _json({"t": _fy(p["date"]), "price": p["close"], "nav_t": _fy(ends), "nav": nav, "disc": disc,
                  "low": {"date": int(p["date"][k]), "v": float(p["close"][k])},
                  "nav_mar2020": float(nav[np.searchsorted(ends, 20200331)]),
                  "nav_dec2019": float(nav[np.searchsorted(ends, 20191231)])})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": load("models")["registered"]}


ITEMS = {"spreads": compute_spreads, "merton": compute_merton, "kmv": compute_kmv, "blackcox": compute_blackcox,
         "hazard": compute_hazard, "cds": compute_cds, "defaults": compute_defaults, "dataset": compute_dataset,
         "models": compute_models, "vasicek": compute_vasicek, "copula": compute_copula, "cjs": compute_cjs,
         "march2020": compute_march2020, "bdc": compute_bdc, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
