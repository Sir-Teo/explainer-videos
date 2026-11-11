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
        debt_tags = ("LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations", "LongTermDebt")
        f = data.sec_facts(cik, ("LiabilitiesCurrent",) + debt_tags + ("dei:EntityCommonStockSharesOutstanding",))["facts"]
        fl, cl = _quarterly(f, "LiabilitiesCurrent")
        # the first tag the company used continuously from 2018 (filers differ in how they tag their debt)
        ltd_c = next(c for c in debt_tags if f[c] and min(x["end"] for x in f[c]) <= "2018-03-31")
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
        Vp = np.full(len(d), np.nan)
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
                Vp[j] = Vj
        w = int(np.nanargmin(dtd))
        okv = np.isfinite(Vp)
        spread = np.full(len(d), np.nan)  # what Merton would charge on one-year debt with this default point
        spread[okv] = CR.merton_spread(Vp[okv], sig[okv], DP[okv], r, 1.0) * 1e4
        out[tk] = {"name": name, "t": _fy(d), "date": d, "E": E, "DP": DP, "dtd": dtd, "sigma_V": sig, "V": Vp,
                   "spread_bp": spread,
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
    # partial dependence: leverage (TL/TA) against the market cushion (ME/TL), every other input at its fit median
    fitm = sets["fit"]
    qs = np.linspace(0.05, 0.95, 19)
    gz_l, gz_m = np.quantile(Z[fitm, 6], qs), np.quantile(Z[fitm, 3], qs)
    raw_l, raw_m = np.nanquantile(X[fitm, 6], qs), np.nanquantile(X[fitm, 3], qs)
    base = np.median(Z[fitm], axis=0)
    grid = np.tile(base, (len(qs) * len(qs), 1))
    grid[:, 6] = np.repeat(gz_l, len(qs))
    grid[:, 3] = np.tile(gz_m, len(qs))
    pdp = {"lev": raw_l, "cushion": raw_m, "q": qs, "gbm": g.predict_proba(grid).reshape(len(qs), len(qs)),
           "logit": CR.logit_predict(b, grid).reshape(len(qs), len(qs))}
    cik = np.asarray(d["cik"], int)
    firms = {tk: [{"fy": int(fy[i]), "logit": float(pl[i]), "gbm": float(pg[i]), "y": int(y[i])}
                  for i in np.where(cik == c_)[0]] for tk, (c_, _) in KMV_FIRMS.items()}
    return _json({"results": res, "roc": roc, "calib": calib, "top_decile_capture": float(y[h][top].sum() / y[h].sum()),
                  "firms": firms, "pdp": pdp,
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
    # a market that prices a calm state (correlation 5%, 85% of the time) and a systemic one (80%, 15%): price the
    # [0, d] tranches there, and read off the one flat Gaussian correlation that matches each: the base correlations
    dets = [0.03, 0.07, 0.10, 0.15, 0.30]
    mix = [(0.05, 0.85), (0.8, 0.15)]
    Lt = (1 - R) * kt / N
    base = [CR.base_correlation(sum(w * CR.lhp_tranche_el(pd_, r_, R, 0, d_) for r_, w in mix), pd_, R, d_)
            for d_ in dets]
    tail = {"gauss": float(np.mean((1 - R) * kg / N > 0.15)), "t": float(np.mean(Lt > 0.15))}
    return _json({"pts": pts, "rho2": rho, "nu": nu, "losses_g": (1 - R) * kg / N, "losses_t": Lt, "rhos": rhos,
                  "el": el, "dets": dets, "base": base, "mix": mix, "pd": pd_, "R": R, "N": N, "tail": tail})


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


def compute_leland() -> dict:
    """Leland (1994): debt, equity and firm value against the coupon; the chosen barrier and the optimal leverage."""
    V, r, s_, tax, alpha = 100.0, 0.06, 0.2, 0.35, 0.5
    X = 2 * r / s_ ** 2
    C = np.linspace(0.05, 12.0, 240)
    VB = (1 - tax) * C / (r + 0.5 * s_ ** 2)
    pB = np.where(VB < V, (V / VB) ** (-X), 1.0)
    debt = C / r + ((1 - alpha) * VB - C / r) * pB
    firm = V + tax * C / r * (1 - pB) - alpha * VB * pB
    eq = firm - debt
    k = int(np.argmax(firm))
    return _json({"C": C, "VB": VB, "debt": debt, "firm": firm, "equity": eq, "V": V, "r": r, "sigma": s_, "tax": tax,
                  "alpha": alpha, "opt": {"C": float(C[k]), "lev": float(debt[k] / firm[k]), "VB": float(VB[k]),
                                          "spread_bp": float((C[k] / debt[k] - r) * 1e4), "gain": float(firm[k] - V)}})


def compute_cox() -> dict:
    """A CIR default intensity (Lando's Cox process): survival curves and spreads in closed form, by starting level."""
    from explainer.quant.house import termstructure as TS
    k_, th, sg, R = 0.5, 0.02, 0.1, 0.4
    T = np.linspace(0.25, 10, 40)
    out = {}
    for name, l0 in (("calm", 0.005), ("long run", 0.02), ("stressed", 0.08)):
        Q = TS.cir_zcb(l0, k_, th, sg, T)
        out[name] = {"l0": l0, "Q": Q, "spread_bp": -np.log(Q) / T * (1 - R) * 1e4}
    return _json({"T": T, "curves": out, "kappa": k_, "theta": th, "sigma": sg, "R": R})


def compute_cdsrisk() -> dict:
    """A protection buyer's mark-to-market on 10 million of 5-year protection struck at 150 bp, as the par spread
    moves; and the jump to default."""
    def df(t):
        return np.exp(-0.04 * np.asarray(t, float))
    R, N, s0 = 0.4, 10e6, 0.015
    shifts = np.linspace(-0.01, 0.03, 41)
    mtm, rp = [], []
    for ds in shifts:
        k, h = CR.bootstrap_hazard([5.0], [s0 + ds], df, R)
        a, p = CR.cds_legs(5.0, k, h, df, R)
        mtm.append(N * (p - s0 * a))
        rp.append(a)
    k0, h0 = CR.bootstrap_hazard([5.0], [s0], df, R)
    a0, _ = CR.cds_legs(5.0, k0, h0, df, R)
    return _json({"shifts_bp": shifts * 1e4, "mtm": mtm, "rpv01": rp, "cs01": float(N * a0 * 1e-4), "jtd": N * (1 - R),
                  "N": N, "s0": s0})


def compute_sorts() -> dict:
    """Bankruptcy rates by decile of leverage, of operating profit and of Altman's Z, in the fit years only."""
    d = load("dataset")
    X, y, fy = np.asarray(d["X"], float), np.asarray(d["y"], int), np.asarray(d["fy"], int)
    fit = fy <= 2016
    out = {}
    for name, j in (("leverage", 6), ("profit", 2)):
        x = X[fit, j]
        ok = np.isfinite(x)
        q = np.nanquantile(x[ok], np.linspace(0, 1, 11))
        dec = np.clip(np.searchsorted(q, x[ok], side="right") - 1, 0, 9)
        out[name] = {"rate": [float(y[fit][ok][dec == i].mean()) for i in range(10)],
                     "mid": [float(np.median(x[ok][dec == i])) for i in range(10)]}
    z = CR.altman_z(np.nan_to_num(X[fit, :5], nan=0.0))
    q = np.quantile(z, np.linspace(0, 1, 11))
    dec = np.clip(np.searchsorted(q, z, side="right") - 1, 0, 9)
    out["altman"] = {"rate": [float(y[fit][dec == i].mean()) for i in range(10)],
                     "mid": [float(np.median(z[dec == i])) for i in range(10)]}
    out["base"] = float(y[fit].mean())
    return _json(out)


def compute_finite() -> dict:
    """The large pool against finite ones: the 99.9th percentile of the default fraction for 50, 200 and 1,000 loans."""
    pd_, rho = 0.02, 0.15
    out = {}
    for n in (50, 200, 1000):
        k, _ = CR.copula_defaults(n, pd_, rho, 100000, seed=n)
        out[str(n)] = float(np.quantile(k / n, 0.999))
    return _json({"pd": pd_, "rho": rho, "q999": out, "lhp": float(CR.vasicek_quantile(0.999, pd_, rho))})


def compute_joint() -> dict:
    """Two names with 2% default probabilities: the joint default probability and the default correlation implied by
    each asset correlation of the Gaussian copula."""
    from scipy.stats import multivariate_normal
    pd_ = 0.02
    k = norm.ppf(pd_)
    rhos = np.linspace(0.0, 0.9, 19)
    p12 = np.array([multivariate_normal(mean=[0, 0], cov=[[1, r_], [r_, 1]]).cdf([k, k]) for r_ in rhos])
    dc = (p12 - pd_ ** 2) / (pd_ * (1 - pd_))
    return _json({"rhos": rhos, "p12": p12, "default_corr": dc, "pd": pd_})


def compute_glm() -> dict:
    """Ares Capital, quarter by quarter: the change in reported NAV per share against the change in the share price
    (both before dividends, which they share); their volatilities and the NAV changes' autocorrelation."""
    b = load("bdc")
    nav_t, nav = np.asarray(b["nav_t"]), np.asarray(b["nav"])
    pt, px = np.asarray(b["t"]), np.asarray(b["price"])
    pq = np.array([px[np.searchsorted(pt, t, side="right") - 1] for t in nav_t])
    r_nav, r_px = nav[1:] / nav[:-1] - 1, pq[1:] / pq[:-1] - 1
    x = r_nav - r_nav.mean()
    return _json({"t": nav_t[1:], "r_nav": r_nav, "r_px": r_px, "rho1": float(np.sum(x[1:] * x[:-1]) / np.sum(x * x)),
                  "vol_nav": float(r_nav.std() * 2), "vol_px": float(r_px.std() * 2), "n": len(r_nav),
                  "corr": float(np.corrcoef(r_nav, r_px)[0, 1]), "worst_nav": float(r_nav.min()),
                  "worst_px": float(r_px.min())})


def compute_recovery() -> dict:
    """Recovery that falls when defaults rise (Altman, Brady, Resti and Sironi 2005; Andersen and Sidenius 2004):
    each tranche's expected loss with recovery fixed at 40%, against recovery that moves with the economy, the
    same 40% on average; and each tranche's sensitivity to the pool's default probability (its 'delta')."""
    pd_, rho = 0.02, 0.2
    z = np.linspace(-9, 9, 8001)
    w = norm.pdf(z) / norm.pdf(z).sum()
    p = norm.cdf((norm.ppf(pd_) - np.sqrt(rho) * z) / np.sqrt(1 - rho))
    Rz = np.clip(0.4 + 0.15 * z, 0.05, 0.75)
    Rz = Rz - (np.sum(w * p * Rz) / np.sum(w * p) - 0.4)  # the same 40% on average, weighted by defaults
    tr = {"equity 0-3%": (0.0, 0.03), "mezzanine 3-7%": (0.03, 0.07), "senior 15-30%": (0.15, 0.30)}
    fixed = {k: float(np.sum(w * CR.tranche_loss(0.6 * p, a, d))) for k, (a, d) in tr.items()}
    rand = {k: float(np.sum(w * CR.tranche_loss((1 - Rz) * p, a, d))) for k, (a, d) in tr.items()}
    el_pool = 0.6 * pd_
    delta = {}
    for k, (a, d) in tr.items():
        up = CR.lhp_tranche_el(pd_ * 1.01, rho, 0.4, a, d)
        dn = CR.lhp_tranche_el(pd_ * 0.99, rho, 0.4, a, d)
        delta[k] = float((up - dn) * (d - a) / (0.6 * pd_ * 0.02))  # tranche notional loss per unit of pool loss
    return _json({"fixed": fixed, "random": rand, "delta": delta, "pd": pd_, "rho": rho, "el_pool": el_pool,
                  "R_bad": float(np.interp(-2.33, z, Rz)), "R_good": float(np.interp(1.0, z, Rz))})


def compute_altfit() -> dict:
    """Altman's five ratios, re-weighted by a logit on the fit years and judged on the validation years only (the
    sealed years are not touched again): do fifty-seven-year-old weights still hold up?"""
    d = load("dataset")
    X, y, fy = np.asarray(d["X"], float)[:, :5], np.asarray(d["y"], int), np.asarray(d["fy"], int)
    fit, val = fy <= 2016, (fy >= 2017) & (fy <= 2020)
    lo, hi = np.nanpercentile(X[fit], 1, axis=0), np.nanpercentile(X[fit], 99, axis=0)
    Z = np.clip(X, lo, hi)
    med = np.nanmedian(Z[fit], axis=0)
    Z = np.where(np.isfinite(Z), Z, med)
    sd = Z[fit].std(0)
    b = CR.logit_fit(Z[fit] / sd, y[fit], l2=1e-3)
    alt = CR.altman_z(np.nan_to_num(X, nan=0.0))
    return _json({"beta_std": b[1:], "beta_raw": b[1:] / sd, "altman": CR.ALTMAN_1968,
                  "auc_val": {"altman_1968": CR.auc(y[val], -alt[val]),
                              "refit": CR.auc(y[val], CR.logit_predict(b, Z[val] / sd))},
                  "auc_fit": {"altman_1968": CR.auc(y[fit], -alt[fit]), "refit": CR.auc(y[fit], CR.logit_predict(b, Z[fit] / sd))}})


def compute_ftd() -> dict:
    """Li's recipe for default times: correlated normals mapped through each name's survival curve. A five-name
    first-to-default basket, 5 years, every name at 100 bp (flat hazard, R = 40%): its fair spread against the copula
    correlation, from the sum of the spreads (independent) to one name's spread (perfectly correlated)."""
    R, s, T, n, N = 0.4, 0.01, 5.0, 5, 200000
    lam = s / (1 - R)
    rng = np.random.default_rng(0)
    out = []
    rhos = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99]
    M = rng.standard_normal(N)
    Zs = rng.standard_normal((N, n))
    for rho in rhos:
        X = np.sqrt(rho) * M[:, None] + np.sqrt(1 - rho) * Zs
        tau = -np.log(norm.cdf(X)) / lam  # Q(tau) = U: survival exp(-lam t) inverted
        first = tau.min(1)
        # par spread of the basket: protection (1 - R) e^{-r tau1} 1{tau1 < T} against premium on the survival
        r = 0.04
        prot = np.mean((1 - R) * np.exp(-r * first) * (first < T))
        grid = np.arange(0.25, T + 1e-9, 0.25)
        prem = np.mean([np.sum(0.25 * np.exp(-r * grid) * (f > grid)) for f in first[:20000]])
        out.append(float(prot / prem))
    return _json({"rhos": rhos, "ftd_bp": np.array(out) * 1e4, "single_bp": s * 1e4, "n": n})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": load("models")["registered"]}


def compute_granularity_theory() -> dict:
    """The research chapter: the granularity adjustment.  Vasicek's large-pool quantile (Basel's ASRF) assumes
    infinitely many small loans.  For N equal loans the loss fraction given the factor y is Binomial(N, p(y))/N, so the
    exact loss distribution is P(L <= k/N) = int BinomCDF(k; N, p(y)) phi(y) dy, and Gordy's (2003) adjustment (from
    Gourieroux, Laurent and Scaillet 2000; Martin and Wilde 2002) adds
    GA = -(1/(2N)) (1/phi(y)) d/dy[ phi(y) p(y)(1 - p(y)) / p'(y) ] at y = Phi^-1(alpha) to the large-pool quantile.
    Checked against the exact quantile at Basel-like PD and correlation, and by Monte Carlo."""
    from scipy.stats import binom
    alpha = 0.999
    Ns = [25, 50, 100, 250, 500, 1000, 2500, 10000]
    y = np.linspace(-8, 8, 8001)
    phi = norm.pdf(y)
    out = {"alpha": alpha, "N": Ns, "cases": {}}
    rng = np.random.default_rng(2020)
    for pd_, rho in ((0.01, 0.12), (0.01, 0.24), (0.03, 0.12)):
        p = norm.cdf((norm.ppf(pd_) + np.sqrt(rho) * y) / np.sqrt(1 - rho))   # y large is the bad state
        ys = norm.ppf(alpha)
        q_asrf = float(norm.cdf((norm.ppf(pd_) + np.sqrt(rho) * ys) / np.sqrt(1 - rho)))
        dp = np.gradient(p, y)
        inner = phi * p * (1 - p) / dp
        dinner = np.gradient(inner, y)
        ga_unit = float(-0.5 * np.interp(ys, y, dinner) / norm.pdf(ys))      # times 1/N
        rows = []
        for N in Ns:
            ks = np.arange(N + 1)
            # P(L <= k/N) for each k, by quadrature over the factor
            F = np.array([np.trapezoid(binom.cdf(k, N, p) * phi, y) for k in ks]) if N <= 2500 else None
            if F is None:
                # large N: only the neighbourhood of the quantile matters
                k0 = int(q_asrf * N)
                kk = np.arange(max(0, k0 - 4 * int(np.sqrt(N) + 5)), min(N, k0 + 6 * int(np.sqrt(N) + 5)))
                Fk = np.array([np.trapezoid(binom.cdf(k, N, p) * phi, y) for k in kk])
                j = int(np.argmax(Fk >= alpha))
                q_exact = float(kk[j] / N)
                lo, hi = Fk[j - 1], Fk[j]
                q_smooth = float((kk[j - 1] + (alpha - lo) / (hi - lo)) / N)
            else:
                j = int(np.argmax(F >= alpha))
                q_exact = float(ks[j] / N)
                lo, hi = F[j - 1], F[j]
                q_smooth = float((ks[j - 1] + (alpha - lo) / (hi - lo)) / N)   # interpolated between the steps
            # an independent Monte Carlo check: 400,000 factor draws, binomial defaults
            if N in (50, 250, 1000):
                Y = rng.standard_normal(400000)
                P = norm.cdf((norm.ppf(pd_) + np.sqrt(rho) * Y) / np.sqrt(1 - rho))
                L = rng.binomial(N, P) / N
                q_mc = float(np.quantile(L, alpha))
            else:
                q_mc = None
            rows.append({"N": N, "exact": q_exact, "smooth": q_smooth, "mc": q_mc, "asrf": q_asrf,
                         "asrf_ga": q_asrf + ga_unit / N})
        out["cases"][f"{pd_:g}_{rho:g}"] = {"pd": pd_, "rho": rho, "asrf": q_asrf, "ga_unit": ga_unit, "rows": rows}
    # a lumpy book: 500 loans with Zipf exposures (the k-th largest proportional to 1/k), PD 1%, rho 0.12
    pd_, rho = 0.01, 0.12
    w = 1 / np.arange(1, 501)
    w = w / w.sum()
    n_eff = float(1 / np.sum(w ** 2))
    c = out["cases"]["0.01_0.12"]
    Ls = []
    for b_ in range(10):
        Y = rng.standard_normal(40000)
        P = norm.cdf((norm.ppf(pd_) + np.sqrt(rho) * Y) / np.sqrt(1 - rho))
        D = rng.random((40000, 500)) < P[:, None]
        Ls.append(D @ w)
    L = np.concatenate(Ls)
    out["lumpy"] = {"n": 500, "n_eff": n_eff, "largest": float(w[0]), "q_mc": float(np.quantile(L, alpha)),
                    "asrf": c["asrf"], "asrf_ga": c["asrf"] + c["ga_unit"] / n_eff,
                    "q_equal500": [r_["smooth"] for r_ in c["rows"] if r_["N"] == 500][0]}
    return _json(out)


ITEMS = {"granularity_theory": compute_granularity_theory, "spreads": compute_spreads, "merton": compute_merton, "kmv": compute_kmv, "blackcox": compute_blackcox,
         "hazard": compute_hazard, "cds": compute_cds, "defaults": compute_defaults, "dataset": compute_dataset,
         "models": compute_models, "vasicek": compute_vasicek, "copula": compute_copula, "cjs": compute_cjs,
         "march2020": compute_march2020, "bdc": compute_bdc, "leland": compute_leland, "cox": compute_cox,
         "cdsrisk": compute_cdsrisk, "sorts": compute_sorts, "finite": compute_finite, "joint": compute_joint,
         "glm": compute_glm, "recovery": compute_recovery,
         "altfit": compute_altfit, "ftd": compute_ftd, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
