"""Every number in Part 3 (Value, Accounting and the Firm), computed and cached in .cache/quant3/.

    python -m videos.quant.quant3.compute [items] [--force]

Research window: to December 2020 (the sealed envelope).  Items (seconds):

* ``shiller``  Shiller (1981), "Do stock prices move too much?": the real S&P price since 1871 against the
               ex-post rational price p*, the present value of the dividends that were actually paid;
* ``cape``     the cyclically adjusted P/E against the next ten years' real total return, 1881-2010 starts;
* ``factors``  accounting signals as long-short portfolios on Ken French's decile sorts, 1963-2020: accruals,
               operating profitability, investment, book-to-market, earnings yield; before and after publication;
* ``dcf``      a firm's DCF value over discount rate and terminal growth (the value surface);
* ``envelope`` seals the hold-outs this part reads (Shiller's monthly price and dividend from 2021, French's five
               accounting sorts from 2021) and registers the CAPE forecast for 2021-30 and the five signals tested.
"""

from __future__ import annotations

import inspect

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, valuation

CACHE = Cache("quant3")
from explainer.quant.house import pit as _pit  # noqa: E402
load = _pit.counted(CACHE.load, 3)  # the series' trial counter as of this part


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


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    """Seal the hold-out of every dataset this part reads, and register what this part tested."""
    s = data.shiller(through="2030-12")
    t = s["t"]
    ym = np.round(t * 12).astype(int)
    dates = (ym // 12) * 10000 + (ym % 12 + 1) * 100 + 1
    ok = np.isfinite(s["price"])
    recs = {"Shiller monthly real price": pit.seal("shiller/price_monthly", dates[ok], s["price"][ok])}
    okd = np.isfinite(s["div"])
    recs["Shiller monthly dividend"] = pit.seal("shiller/div_monthly", dates[okd], s["div"][okd])
    for name, *_ in SIGNALS:
        k = data.ken_french_sorts(name, through="2025-12")
        recs[f"French sorts: {name}"] = pit.seal(f"kenfrench/sorts_{name}", k["date"] * 100 + 1, k["returns"])
    c = load("cape")
    reg = {"cape_forecast_2021_2030": pit.register(
        "cape_forecast_2021_2030", inspect.getsource(compute_cape),
        {"model": "10y real total return on log CAPE, OLS on 1881-2010 monthly starts", "cape_dec_2020": c["cape_now"],
         "forecast_real_annual": c["pred_now"]}, trials=1),
        "accounting_signals_part3": pit.register(
        "accounting_signals_part3", inspect.getsource(compute_factors),
        {"signals": [s_[0] for s_ in SIGNALS], "legs": "decile 10 minus decile 1, value-weighted"}, trials=len(SIGNALS))}
    # the expansion's data: Chen-Zimmermann's long-shorts and French's net-issuance sorts from 2021 are sealed too
    ym, names, R = _osap_matrix()
    recs["OSAP 2024.10 long-shorts"] = pit.seal("osap/2024.10/PredictorLSretWide", ym * 100 + 1, np.nan_to_num(R, nan=-999))
    k = data.ken_french_sorts("NI", through="2023-12")
    recs["French sorts: NI"] = pit.seal("kenfrench/sorts_NI", k["date"] * 100 + 1, np.nan_to_num(k["returns"], nan=-999))
    o = load("osap")
    reg["osap_predictors_part3"] = pit.register(
        "osap_predictors_part3", inspect.getsource(compute_osap),
        {"release": OSAP_RELEASE, "window": "to 2020-12", "predictors": o["n_all"]}, trials=o["n_all"])
    f = load("forecaster")
    reg["earnings_forecaster_part3"] = pit.register(
        "earnings_forecaster_part3", inspect.getsource(compute_forecaster),
        {"data": "simulated panel", "models": ["random walk", "OLS", "ridge on splines", "MLP"]},
        trials=f["n_trials"])
    return _json({"sealed": recs, "registered": reg, "trials": pit.trials_so_far()})




# ===========================================================================
# The expansion (November 2026): raw sources, then one item per chapter
# ===========================================================================
import csv  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import urllib.request  # noqa: E402
from datetime import date, datetime, timezone  # noqa: E402

from explainer.quant.house import econ, fundamentals  # noqa: E402

RAW = data.DATA
EDGAR_FROZEN = 20261031           # facts filed after this day are ignored, so the extract is frozen and checksummed
OSAP_RELEASE = "2024.10"
OSAP_URL = "https://huggingface.co/datasets/OpenSourceAP/CrossSection/resolve/{rel}/{path}"
DAMODARAN = "https://pages.stern.nyu.edu/~adamodar/pc/datasets/histimpl.xls"
FIRMS = {12927: "Boeing", 34088: "Exxon Mobil", 40545: "General Electric", 72971: "Wells Fargo", 320193: "Apple",
         789019: "Microsoft", 1530721: "Capri", 1637459: "Kraft Heinz"}
NONBANK = [12927, 34088, 40545, 320193, 789019, 1530721, 1637459]
ALIASES = {
    "sales": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
              "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet"],
    "cogs": ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"],
    "receivables": ["AccountsReceivableNetCurrent"], "current_assets": ["AssetsCurrent"],
    "ppe": ["PropertyPlantAndEquipmentNet"], "assets": ["Assets"],
    "depreciation": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "Depreciation"],
    "sga": ["SellingGeneralAndAdministrativeExpense", "GeneralAndAdministrativeExpense"], "current_liabilities": ["LiabilitiesCurrent"],
    "long_term_debt": ["LongTermDebtNoncurrent", "LongTermDebt", "LongTermDebtAndCapitalLeaseObligations"], "net_income": ["NetIncomeLoss"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities"], "equity": ["StockholdersEquity"],
}
EDGAR_CONCEPTS = sorted({c for cs in ALIASES.values() for c in cs})  # the frozen extract keeps these
STOCKS = {"receivables", "current_assets", "ppe", "assets", "current_liabilities", "long_term_debt", "equity"}


def _ymd(s: str) -> int:
    return int(s.replace("-", ""))


def _days(a: int, b: int) -> int:
    return (date(b // 10000, b // 100 % 100, b % 100) - date(a // 10000, a // 100 % 100, a % 100)).days


def _sec_get(url: str) -> bytes:
    ua = os.environ.get("SEC_USER_AGENT")
    if not ua:
        raise RuntimeError("EDGAR asks every client to identify itself with a contact: set SEC_USER_AGENT, e.g. "
                           "'Your Name your.address@example.org', to download company facts from data.sec.gov")
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=120) as r:
        return r.read()


def companyfacts(cik: int) -> dict:
    """EDGAR's XBRL company facts for ``cik`` (data.sec.gov), cached raw; returns the us-gaap concepts this part
    uses, facts filed through EDGAR_FROZEN only, and checks that extract against the manifest."""
    path = RAW / "edgar" / f"CIK{cik:010d}.json"
    if not path.exists():
        data._atomic_write(path, _sec_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))
    raw = json.loads(path.read_text())
    keep = EDGAR_CONCEPTS
    out = {}
    for c, body in raw["facts"].get("us-gaap", {}).items():
        if c not in keep:
            continue
        rows = []
        for unit, lst in body.get("units", {}).items():
            for r_ in lst:
                if _ymd(r_["filed"]) <= EDGAR_FROZEN:
                    rows.append({"unit": unit, "start": r_.get("start", ""), "end": r_["end"], "val": r_["val"],
                                 "filed": r_["filed"], "form": r_.get("form", ""), "fp": r_.get("fp", ""),
                                 "fy": r_.get("fy"), "accn": r_.get("accn", "")})
        rows.sort(key=lambda q: (q["end"], q["filed"], q["accn"], q["start"], q["unit"]))
        out[c] = rows
    frozen = json.dumps(out, sort_keys=True, separators=(",", ":")).encode()
    data._check(f"edgar/companyfacts/CIK{cik:010d}/v1_through_{EDGAR_FROZEN}", frozen,
                f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    return {"name": raw.get("entityName", FIRMS.get(cik, str(cik))), "facts": out}


def submissions(cik: int) -> dict:
    path = RAW / "edgar" / f"CIK{cik:010d}_submissions.json"
    if not path.exists():
        data._atomic_write(path, _sec_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))
    r = json.loads(path.read_text())["filings"]["recent"]
    rows = [(f, _ymd(d), a, i) for f, d, a, i in zip(r["form"], r["filingDate"], r["acceptanceDateTime"], r["items"])
            if _ymd(d) <= EDGAR_FROZEN]
    data._check(f"edgar/submissions/CIK{cik:010d}/through_{EDGAR_FROZEN}",
                json.dumps(rows, separators=(",", ":")).encode(), f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    return {"form": [x[0] for x in rows], "filed": [x[1] for x in rows], "accepted": [x[2] for x in rows],
            "items": [x[3] for x in rows]}


def _annual(facts: dict, item: str) -> dict:
    """Annual (10-K) facts for an item: {period end: [(filed, value), ...] sorted by filing}, flows over a year only,
    the first alias that reports the period."""
    out = {}
    for c in ALIASES[item]:
        for r_ in facts.get(c, []):
            if r_["unit"] != "USD" or r_["form"] not in ("10-K", "10-K/A", "10-KT"):
                continue
            if item not in STOCKS:
                if not r_["start"] or not 330 < _days(_ymd(r_["start"]), _ymd(r_["end"])) < 400:
                    continue
            e = _ymd(r_["end"])
            if e in out and c != out[e][0]:
                continue
            out.setdefault(e, [c, []])[1].append((_ymd(r_["filed"]), float(r_["val"])))
    return {e: sorted(set(v)) for e, (_, v) in out.items()}


def _asof(series: dict, end: int, t: int):
    v = [x for f, x in series.get(end, []) if f <= t]
    return v[-1] if v else None


def _osap():
    """Chen and Zimmermann's open-source long-short returns (release 2024.10, original-paper portfolios) and the
    signal documentation, cached and checked."""
    import pyarrow.parquet as pq

    base = RAW / "osap" / OSAP_RELEASE
    files = {"PredictorLSretWide.parquet": "Portfolios/Full%20Sets%20OP/PredictorLSretWide.parquet",
             "SignalDoc.csv": "SignalDoc.csv"}
    for fn, rel in files.items():
        url = OSAP_URL.format(rel=OSAP_RELEASE, path=rel)
        data._cached(f"osap/{OSAP_RELEASE}/{fn}", base / fn, lambda u=url: data._get(u), url)
    t = pq.read_table(base / "PredictorLSretWide.parquet")
    doc = {r_["Acronym"]: r_ for r_ in csv.DictReader(open(base / "SignalDoc.csv", encoding="latin-1"))}
    return t, doc


def _osap_matrix():
    t, _ = _osap()
    ym = np.array([d.year * 100 + d.month for d in t.column("date").to_pylist()])
    names = [c for c in t.column_names if c != "date"]
    R = np.column_stack([np.array(t.column(c).to_pylist(), dtype=float) for c in names])
    return ym, names, R


def _yahoo(symbol: str, interval: str, start: str, end: str) -> dict:
    """Yahoo Finance chart API at ``interval`` (1d, 1wk, 1mo), with adjusted closes (dividends reinvested) where Yahoo
    gives them; frozen window, checksummed."""
    p0 = int(datetime.fromisoformat(start).replace(tzinfo=timezone.utc).timestamp())
    p1 = int(datetime.fromisoformat(end).replace(tzinfo=timezone.utc).timestamp())
    safe = symbol.replace("^", "_")
    path = RAW / "yahoo" / f"{safe}_{interval}_{start}_{end}.json"
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={p0}&period2={p1}"
           f"&interval={interval}&events=div%2Csplit")
    if not path.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (education)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data._atomic_write(path, r.read())
    d = json.loads(path.read_text())["chart"]["result"][0]
    ts = np.asarray(d["timestamp"], float) + d["meta"].get("gmtoffset", 0)
    q = d["indicators"]
    close = np.array([np.nan if c is None else c for c in q["quote"][0]["close"]], float)
    adj = q.get("adjclose", [{}])[0].get("adjclose")
    adj = close if adj is None else np.array([np.nan if c is None else c for c in adj], float)
    ymd = np.array([int(datetime.fromtimestamp(x, timezone.utc).strftime("%Y%m%d")) for x in ts])
    ok = np.isfinite(close) & np.isfinite(adj)
    ymd, close, adj = ymd[ok], close[ok], adj[ok]
    frozen = json.dumps(np.column_stack([ymd, close.round(4), adj.round(4)]).tolist(), separators=(",", ":")).encode()
    data._check(f"yahoo/{symbol}/{interval}/{start}_{end}", frozen, url)
    return {"date": ymd, "close": close, "adj": adj}


# ---------------------------------------------------------------------------
def compute_timevalue() -> dict:
    """Ch. 1: the bond's IRR found by bisection, step by step, and a project with two IRRs."""
    bond = [-100] + [5] * 9 + [105]
    b = valuation.irr_bisect(bond, 0.0, 0.2, steps=30)
    proj = [-100, 230, -132]
    rs = np.linspace(0.0, 0.32, 161)
    npv = np.array([valuation.npv(r, proj) for r in rs])
    r1 = valuation.irr_bisect(proj, 0.0, 0.15, steps=40)
    r2 = valuation.irr_bisect(proj, 0.15, 0.5, steps=40)
    try:
        wide = valuation.irr_bisect(proj, 0.0, 0.5, steps=40)["root"]
    except ValueError:
        wide = None
    return _json({"bond_brackets": b["brackets"], "bond_irr": b["root"], "bond_pv4": valuation.npv(0.04, bond[1:] and
                  [0] + bond[1:]), "proj": proj, "rs": rs, "npv": npv, "root1": r1["root"], "root2": r2["root"],
                  "brackets1": r1["brackets"][:12], "npv15": valuation.npv(0.15, proj), "wide_bracket_root": wide,
                  "annuity": valuation.annuity(5, 0.04, 10)})


# ---------------------------------------------------------------------------
def compute_duration() -> dict:
    """Ch. 2: Gordon's duration, and the measured rate sensitivity of French's book-to-market deciles: monthly
    returns regressed on the monthly change in the 10-year yield (Shiller's GS10), July 1963 - December 2020."""
    k = data.ken_french_sorts("BE-ME")
    cols = k["columns"]
    s = data.shiller()
    ym = np.round(s["t"] * 12).astype(int)
    yyyymm = (ym // 12) * 100 + ym % 12 + 1
    dy = dict(zip(yyyymm[1:], np.diff(s["gs10"])))  # percentage points
    m = k["date"] >= 196307
    X = np.array([dy.get(x, np.nan) for x in k["date"][m]])
    dec = [c for c in cols if c.startswith(("Lo 10", "Dec", "Hi 10"))]
    betas, ses = [], []
    for c in dec:
        o = econ.ols(k["returns"][m, cols.index(c)], X, se="nw", lags=3)
        betas.append(float(o["beta"][1]))
        ses.append(float(o["se"][1]))
    gd = valuation.gordon_duration(0.08, 0.05)
    return _json({"deciles": dec, "beta": np.array(betas), "se": np.array(ses), "n": int(np.isfinite(X).sum()),
                  "gordon_mod": gd["modified"], "gordon_mac": gd["macaulay"],
                  "w_stock": valuation.pv_weights(0.08, 0.05, 120), "bond30": _bond_weights(0.08, 30)})


def _bond_weights(y, n, c=0.05):
    cf = np.full(n, c * 100.0)
    cf[-1] += 100
    pv = cf / (1 + y) ** np.arange(1, n + 1)
    return pv / pv.sum()


# ---------------------------------------------------------------------------
def compute_statements() -> dict:
    """Ch. 3: the toy firm run for twenty quarters through the House's double-entry machine."""
    firm = fundamentals.Firm()
    start = {"cash": firm.cash, "receivables": firm.receivables, "plant": firm.plant, "debt": firm.debt,
             "equity": firm.equity}
    rows = fundamentals.simulate(firm, 20, sales0=250, growth=0.02, vol=0.08, seed=4, write_off=0.03, payout=0.25,
                                 tax=0.21, rate_debt=0.01)
    keys = list(rows[0])
    gap = max(abs(r_["assets"] - r_["debt"] - r_["equity"]) for r_ in rows)
    # one quarter of the lab, from the start: sales double on credit
    f2 = fundamentals.Firm()
    q1 = fundamentals.step(f2, 250.0, credit=0.2)
    f3 = fundamentals.Firm()
    q2 = fundamentals.step(f3, 500.0, credit=0.9)
    return _json({"start": start, "rows": {k_: [r_[k_] for r_ in rows] for k_ in keys}, "max_gap": gap,
                  "lab": q1, "credit_heavy": q2})


# ---------------------------------------------------------------------------
def _edgar_annual_panel():
    """Annual items of the seven non-bank firms, as last reported by EDGAR_FROZEN and as first reported."""
    out = {}
    for cik in NONBANK:
        cf = companyfacts(cik)
        out[cik] = {"name": FIRMS[cik], "items": {it: _annual(cf["facts"], it) for it in ALIASES}}
    return out


def compute_accruals() -> dict:
    """Ch. 4: Sloan's persistence regression, E_{t+1} on CFO_t and ACC_t (all over assets).  (a) a simulated panel
    whose truth is known (the House's earnings_panel: accruals carry an estimation error that reverses); (b) the
    seven non-bank firms in the EDGAR cache, FY2009-2020, as last reported; (c) the accrual long-short."""
    p = fundamentals.earnings_panel(2000, 10, seed=7)
    n, T = p["E"].shape
    y = p["E"][:, 1:].ravel()
    X = np.column_stack([p["CFO"][:, :-1].ravel(), p["ACC"][:, :-1].ravel()])
    firm = np.repeat(np.arange(n), T - 1)
    sim = econ.ols(y, X, se="cluster", groups=firm)
    rng = np.random.default_rng(0)
    pick = rng.choice(len(y), 600, replace=False)
    # real firms
    panel = _edgar_annual_panel()
    rows = []
    for cik, d in panel.items():
        it = d["items"]
        ends = sorted(e for e in it["net_income"] if 20090101 <= e <= 20201231)
        for e in ends:
            nxt = [x for x in it["net_income"] if 330 < _days(e, x) < 400]
            prev_a = [x for x in it["assets"] if 330 < _days(x, e) < 400]
            if not nxt or not prev_a or e not in it["cfo"] or nxt[0] > 20201231:
                continue
            A = (it["assets"][prev_a[0]][-1][1] + it["assets"].get(e, it["assets"][prev_a[0]])[-1][1]) / 2
            ni, cfo = it["net_income"][e][-1][1], it["cfo"][e][-1][1]
            rows.append((cik, e, it["net_income"][nxt[0]][-1][1] / A, cfo / A, (ni - cfo) / A))
    R = np.array([r_[2:] for r_ in rows])
    real = econ.ols(R[:, 0], R[:, 1:], se="cluster", groups=np.array([r_[0] for r_ in rows]))
    ym, names, M = _osap_matrix()
    a = M[:, names.index("Accruals")]
    w = (ym >= 196307) & (ym <= 202012) & np.isfinite(a)
    return _json({"sim_beta": sim["beta"], "sim_se": sim["se"], "sim_n": sim["n"], "sim_firms": n,
                  "sim_points": np.column_stack([X[pick], y[pick]]), "sim_params": p["params"],
                  "real_beta": real["beta"], "real_se": real["se"], "real_n": real["n"],
                  "real_firms": len({r_[0] for r_ in rows}), "real_points": R,
                  "real_names": [FIRMS[r_[0]] for r_ in rows], "real_years": [r_[1] // 10000 for r_ in rows],
                  "osap_mean": float(a[w].mean()), "osap_t": float(a[w].mean() / a[w].std(ddof=1) * np.sqrt(w.sum())),
                  "sloan": {"acc": 0.765, "cfo": 0.855, "all": 0.841}})


# ---------------------------------------------------------------------------
def compute_pit() -> dict:
    """Ch. 5: the eight cached firms' 10-K facts: how many annual values a later 10-K showed differently (restated or
    recast), the days from year end to the first 10-K, and Kraft Heinz's net income asked as of two dates."""
    firms, lags_all = [], []
    for cik, name in FIRMS.items():
        cf = companyfacts(cik)
        rec = {"name": name}
        for it in ("net_income", "sales", "assets"):
            s_ = _annual(cf["facts"], it)
            s_ = {e: v for e, v in s_.items() if e <= 20201231}
            changed = sum(1 for v in s_.values() if any(abs(x - v[0][1]) > 1e-6 * max(1, abs(v[0][1])) for _, x in v[1:]))
            rec[it] = [len(s_), changed]
        ni = _annual(cf["facts"], "net_income")
        lags = [_days(e, v[0][0]) for e, v in ni.items() if 20090101 <= e <= 20201231]
        rec["median_lag"] = float(np.median(lags)) if lags else None
        lags_all += lags
        firms.append(rec)
    kh = _annual(companyfacts(1637459)["facts"], "net_income")
    store = fundamentals.Store()
    for e, v in kh.items():
        for f_, x in v:
            store.add("KHC", "NetIncomeLoss", e, f_, x, "10-K")
    ask = [20180630, 20200630]
    views = {str(t): [(f.period_end, f.value, f.filed) for f in store.history("KHC", "NetIncomeLoss", t)
                      if 20151231 <= f.period_end <= 20181231] for t in ask}
    ge = _annual(companyfacts(40545)["facts"], "sales")
    planes = {"Kraft Heinz net income": [(e, f_, x) for e, v in kh.items() for f_, x in v if 20141231 <= e <= 20201231],
              "General Electric revenue": [(e, f_, x) for e, v in ge.items() for f_, x in v if 20081231 <= e <= 20201231]}
    return _json({"firms": firms, "lags": np.array(lags_all), "khc_views": views, "planes": planes,
                  "khc_restatements": store.restatements("KHC", "NetIncomeLoss"),
                  "rules": {"large accelerated": 60, "accelerated": 75, "other": 90}})


# ---------------------------------------------------------------------------
def compute_dcf_mc() -> dict:
    """Ch. 6: a Monte Carlo DCF (the base firm of chapter 6 with r ~ U[6%, 10%], g ~ U[0, 3%] and free cash flow
    scaled by U[0.8, 1.2]) and the value-driver surface over growth and RONIC at a WACC of 8%."""
    rng = np.random.default_rng(3)
    N = 20000
    r = rng.uniform(0.06, 0.10, N)
    g = rng.uniform(0.0, 0.03, N)
    m = rng.uniform(0.8, 1.2, N)
    fcf = 100 * 1.05 ** np.arange(1, 6)
    V = np.array([valuation.dcf(fcf * mm, rr, gg)["value"] for rr, gg, mm in zip(r, g, m)])
    base = valuation.dcf(fcf, 0.08, 0.02)["value"]
    gs = np.linspace(0.0, 0.05, 26)
    ron = np.linspace(0.04, 0.20, 33)
    S = np.array([[valuation.value_driver_tv(100, gg, rr, 0.08) for gg in gs] for rr in ron])
    return {"r": r[:3000], "g": g[:3000], "m": m[:3000], "V": V, "base": base,
            "q05": float(np.percentile(V, 5)), "q50": float(np.percentile(V, 50)), "q95": float(np.percentile(V, 95)),
            "gs": gs, "ronic": ron, "vd": S, "vd_flat": valuation.value_driver_tv(100, 0.0, 0.08, 0.08)}


# ---------------------------------------------------------------------------
def compute_erp() -> dict:
    """Ch. 7: Damodaran's implied equity risk premium rebuilt: solve the two-stage model for the S&P 500 at each
    year end (cash yield = dividends, plus buybacks from 2001; five years at the analysts' or smoothed growth, then
    growth at the T-bond rate), and compare with his published FCFE column (histimpl.xls)."""
    import xlrd

    path = RAW / "damodaran" / "histimpl.xls"
    raw = data._cached("damodaran/histimpl.xls", path, lambda: data._get(DAMODARAN), DAMODARAN)
    sh = xlrd.open_workbook(file_contents=raw).sheet_by_index(0)
    rows = []
    for i in range(sh.nrows):
        v = sh.row_values(i)
        if isinstance(v[0], float) and 1960 <= v[0] <= 2030:
            rows.append(v)
    yr, ours, his, bond, inputs = [], [], [], [], []
    for v in rows:
        y = int(v[0])
        P, div, buy, tb = v[3], v[5], v[6], v[10]
        g = v[14] if isinstance(v[14], float) else v[12]
        pub = v[15] if isinstance(v[15], float) else None
        if pub is None or not isinstance(g, float):
            continue
        cf0 = buy if isinstance(buy, float) and buy != "" else div
        r = valuation.implied_rate(P, cf0, g, tb)
        yr.append(y)
        ours.append(r - tb)
        his.append(pub)
        bond.append(tb)
        inputs.append([P, cf0, g, tb])
    yr, ours, his = np.array(yr), np.array(ours), np.array(his)
    w = yr <= 2020
    gap = np.abs(ours - his)[w]
    lab = {str(y): dict(zip(["price", "cash", "growth", "bond", "implied", "erp", "published"],
                            inputs[list(yr).index(y)] + [ours[list(yr).index(y)] + bond[list(yr).index(y)],
                                                          ours[list(yr).index(y)], his[list(yr).index(y)]]))
           for y in (1999, 2008, 2020)}
    return {"year": yr, "ours": ours, "published": his, "bond": np.array(bond), "median_gap": float(np.median(gap)),
            "max_gap": float(gap.max()), "within20": int(np.sum(gap <= 0.002)), "n_window": int(w.sum()), "lab": lab}


# ---------------------------------------------------------------------------
def compute_ri() -> dict:
    """Ch. 8: residual income.  The P/B surface over (ROE, g) at r = 8%; the identity RI = DDM checked on the toy
    firm's statements; a firm whose ROE fades from 15% to the cost of equity."""
    roe = np.linspace(0.0, 0.24, 25)
    gs = np.linspace(0.0, 0.06, 13)
    PB = np.array([[valuation.pb_steady(a, 0.08, g) for a in roe] for g in gs])
    firm = fundamentals.Firm()
    b0 = firm.equity
    rows = fundamentals.simulate(firm, 40, seed=11, write_off=0.04, tax=0.21, rate_debt=0.01, payout=0.4)
    E = [r_["net_income"] for r_ in rows]
    D = [r_["dividends"] for r_ in rows]
    chk = valuation.residual_income(b0, E, D, 0.02)
    path = 0.08 + 0.07 * 0.7 ** np.arange(10)
    B, Es = [100.0], []
    for k in range(10):
        Es.append(path[k] * B[-1])
        B.append(B[-1] + Es[-1] * 0.6)
    fade = valuation.residual_income(100.0, Es, [e * 0.4 for e in Es], 0.08)
    return {"roe": roe, "gs": gs, "pb": PB, "check_ri": chk["value"], "check_ddm": chk["ddm"],
            "check_gap": abs(chk["value"] - chk["ddm"]), "fade_roe": path, "fade_ri": np.asarray(fade["ri"]),
            "fade_value": fade["value"], "fade_pv_ri": fade["value"] - 100.0}


# ---------------------------------------------------------------------------
def _cs_annual():
    s = data.shiller()
    t, P, D, cpi = s["t"], s["price"], s["div"], s["cpi"]
    jan = np.isclose(t % 1, 0)
    ty, Py, cy = t[jan], P[jan], cpi[jan]
    Dy = np.array([D[np.isclose(t, y + 11 / 12)][0] if np.any(np.isclose(t, y + 11 / 12)) else np.nan for y in ty])
    ok = np.isfinite(Dy) & np.isfinite(Py)
    ty, Py, Dy, cy = ty[ok], Py[ok], Dy[ok], cy[ok]
    infl = cy[1:] / cy[:-1]
    r = np.log((Py[1:] + Dy[:-1]) / Py[:-1] / infl)
    dg = np.log(Dy[1:] / Dy[:-1] / infl)
    dp = np.log(Dy / Py)
    return ty, r, dg, dp


def compute_campbell_shiller() -> dict:
    """Ch. 9: Cochrane's decomposition on Shiller's annual real data (January to January): returns, dividend growth
    and next year's dividend yield regressed on this year's; long-run coefficients; subsamples; and the Stambaugh
    bootstrap of the return slope's t under the null of no predictability."""
    ty, r, dg, dp = _cs_annual()
    full = valuation.campbell_shiller(r, dg, dp)
    o = econ.ols(r, dp[:-1], se="nw", lags=2)
    out = {"full": full, "t_r": float(o["t"][1]), "years": [int(ty[0]), int(ty[-1])], "n": int(len(r))}
    subs = {}
    for lo, hi in [(1871, 1945), (1946, 2020)]:
        m = (ty[:-1] >= lo) & (ty[:-1] <= hi)
        idx = np.flatnonzero(m)
        subs[f"{lo}-{hi}"] = valuation.campbell_shiller(r[idx], dg[idx], dp[np.r_[idx, idx[-1] + 1]])
    out["subs"] = subs
    v = econ.ols(dp[1:], dp[:-1])["resid"]
    u = o["resid"]
    corr = float(np.corrcoef(u, v)[0, 1])
    sims = econ.simulate_predictive(len(r), full["phi"], corr, n=5000, seed=1)
    se_r = float(o["se"][1])
    out["boot_slopes"] = sims
    out["boot_p"] = float(np.mean(sims >= full["b_r"]))
    out["boot_mean"] = float(sims.mean())
    out["corr_uv"] = corr
    out["dp"] = dp
    out["ty"] = ty
    out["se_r"] = se_r
    return _json(out) | {"boot_slopes": sims, "dp": dp, "ty": ty}


# ---------------------------------------------------------------------------
def compute_payout() -> dict:
    """Ch. 11: issuers against repurchasers (French's net-issuance sorts, value-weighted, July 1963 - 2020), the
    OSAP net payout yield and share issuance long-shorts, and two simulated firms, one paying dividends and one
    buying back, whose owners end up equally rich."""
    k = data.ken_french_sorts("NI")
    cols, d = k["columns"], k["date"]
    m = d >= 196307
    ann = {c: float(np.nanmean(k["returns"][m, cols.index(c)]) * 12) for c in cols}
    ym, names, M = _osap_matrix()
    _, doc = _osap()
    osap = {}
    for c in ("NetPayoutYield", "ShareIss1Y"):
        x = M[:, names.index(c)]
        s0, s1, py = int(doc[c]["SampleStartYear"]), int(doc[c]["SampleEndYear"]), int(doc[c]["Year"])
        y = ym // 100
        ins = x[(y >= s0) & (y <= s1) & np.isfinite(x)]
        post = x[(y > py) & (y <= 2020) & np.isfinite(x)]
        osap[c] = {"in": float(ins.mean()), "post": float(post.mean()), "year": py, "authors": doc[c]["Authors"]}
    # two firms with the same operations: earnings 100 a year on operations worth 1000, all paid out; the owner of
    # the dividend payer reinvests at the same 10%, so the comparison is like for like
    years = 10
    out = {"div": {}, "buy": {}}
    for mode in ("div", "buy"):
        shares, price, wealth, eps, cash_in = 100.0, 10.0, [], [], 0.0
        own = 1.0  # one share held throughout, cash kept
        held = own
        for t in range(years):
            V = 1000.0 + 100.0  # operations plus the year's cash, just before payout
            if mode == "div":
                dps = 100.0 / shares
                price = (V - 100.0) / shares
                cash_in = cash_in * 1.1 + held * dps  # dividends reinvested at the firm's 10% return
            else:
                price = V / shares
                bought = 100.0 / price
                shares -= bought
                price = (V - 100.0) / shares
            eps.append(100.0 / shares)
            wealth.append(held * price + cash_in)
        out[mode] = {"wealth": wealth, "eps": eps, "price": price, "shares": shares}
    return _json({"ni_columns": cols, "ni_annual": ann, "osap": osap, "two_firms": out})


# ---------------------------------------------------------------------------
def compute_merton() -> dict:
    """Ch. 12: equity and debt values over (assets, asset volatility), debt of face 80 due in a year; Myers's
    overhang: a project costing 10, paid by the owners, that adds 15 to the assets of a firm near default."""
    A = np.linspace(20, 200, 37)
    sig = np.linspace(0.1, 0.6, 26)
    F, T, r = 80.0, 1.0, 0.02
    E = np.array([valuation.merton_equity(A, F, T, s_, r)["equity"] for s_ in sig])
    D = np.array([valuation.merton_equity(A, F, T, s_, r)["debt"] for s_ in sig])
    a0, s0, cost, gain = 60.0, 0.3, 10.0, 15.0
    e0 = float(valuation.merton_equity(a0, F, T, s0, r)["equity"])
    e1 = float(valuation.merton_equity(a0 + gain, F, T, s0, r)["equity"])
    d0 = float(valuation.merton_equity(a0, F, T, s0, r)["debt"])
    d1 = float(valuation.merton_equity(a0 + gain, F, T, s0, r)["debt"])
    hi = float(valuation.merton_equity(a0, F, T, 2 * s0, r)["equity"])
    dhi = float(valuation.merton_equity(a0, F, T, 2 * s0, r)["debt"])
    return {"A": A, "sig": sig, "E": E, "D": D, "F": F, "T": T, "r": r, "a0": a0, "s0": s0, "cost": cost, "gain": gain,
            "e0": e0, "e1": e1, "d0": d0, "d1": d1, "e_risky": hi, "d_risky": dhi}


# ---------------------------------------------------------------------------
def compute_pead() -> dict:
    """Ch. 13: an event study on Apple's earnings announcements (8-K item 2.02 acceptances, October 2015 - December
    2020): SUE of quarterly net income as first reported, market-adjusted CARs against SPY from day -5 to +60;
    then the drift at scale from Chen-Zimmermann's EarningsSurprise long-short (Foster, Olsen and Shevlin 1984)."""
    cf = companyfacts(320193)["facts"]
    first = {}
    for r_ in cf["NetIncomeLoss"]:  # rows are sorted by filing date within a period: the first is first-reported
        if r_["unit"] == "USD" and r_["start"]:
            first.setdefault((_ymd(r_["start"]), _ymd(r_["end"])), float(r_["val"]))
    quarters = {e: v for (s_, e), v in first.items() if 80 < _days(s_, e) < 100}
    for (s_, e), v in first.items():  # the fourth quarter: the year less its first nine months
        if 350 < _days(s_, e) < 380 and e not in quarters:
            nine = [v9 for (s9, e9), v9 in first.items() if s9 == s_ and 260 < _days(s9, e9) < 290]
            if nine:
                quarters[e] = v - nine[0]
    ends = sorted(quarters)
    ni = np.array([quarters[e] for e in ends])
    su = fundamentals.sue(ni)
    sub = submissions(320193)
    ann = sorted((f_, a) for fm, f_, a, it in zip(sub["form"], sub["filed"], sub["accepted"], sub["items"])
                 if fm == "8-K" and "2.02" in it and f_ <= 20201231)
    px = data.yahoo_daily("AAPL", start="2013-01-01", through="2021-06-30")
    mk = data.yahoo_daily("SPY", start="2013-01-01", through="2021-06-30")
    common = np.intersect1d(px["date"], mk["date"])
    pa = px["close"][np.searchsorted(px["date"], common)]
    pm = mk["close"][np.searchsorted(mk["date"], common)]
    ra, rm = np.r_[np.nan, pa[1:] / pa[:-1] - 1], np.r_[np.nan, pm[1:] / pm[:-1] - 1]
    events = []
    for f_, acc in ann:
        qe = [e for e in ends if 10 < _days(e, f_) < 60]
        if not qe:
            continue
        i = ends.index(qe[-1])
        if not np.isfinite(su[i]):
            continue
        hour = int(acc[11:13]) if len(acc) > 12 else 12
        d0 = int(np.searchsorted(common, f_))
        if hour >= 16 and d0 < len(common) and common[d0] == f_:
            d0 += 1
        c = fundamentals.car(ra, rm, d0, (-5, 60))
        if np.all(np.isfinite(c)):
            events.append({"filed": f_, "quarter": ends[i], "sue": float(su[i]), "car": c, "day0": int(common[d0])})
    S = np.array([e_["sue"] for e_ in events])
    C = np.array([e_["car"] for e_ in events])
    pos, neg = S > 0, S <= 0
    jump = C[:, 6] - C[:, 4]          # days 0 and +1 against day -1
    drift = C[:, -1] - C[:, 6]        # from day +1 to day +60
    ym, names, M = _osap_matrix()
    _, doc = _osap()
    x = M[:, names.index("EarningsSurprise")]
    y = ym // 100
    s0, s1, py = (int(doc["EarningsSurprise"][k_]) for k_ in ("SampleStartYear", "SampleEndYear", "Year"))
    seg = {"in": x[(y >= s0) & (y <= s1) & np.isfinite(x)], "pre": x[(y > s1) & (y <= py) & np.isfinite(x)],
           "post": x[(y > py) & (y <= 2020) & np.isfinite(x)], "after2006": x[(y >= 2006) & (y <= 2020) & np.isfinite(x)]}
    w = (ym >= 197401) & (ym <= 202012)
    cum = np.cumprod(1 + np.nan_to_num(x[w]) / 100)
    lab_e = events[-1]
    return _json({"n_events": len(events), "sue": S, "car": C, "days": np.arange(-5, 61),
                  "mean_pos": C[pos].mean(0) if pos.any() else None, "mean_neg": C[neg].mean(0) if neg.any() else None,
                  "n_pos": int(pos.sum()), "n_neg": int(neg.sum()), "jump_corr": float(np.corrcoef(S, jump)[0, 1]),
                  "drift_pos": float(drift[pos].mean()), "drift_neg": float(drift[neg].mean()),
                  "lab": {"filed": lab_e["filed"], "day0": lab_e["day0"], "sue": lab_e["sue"],
                          "car0": float(lab_e["car"][6] - lab_e["car"][4]), "car60": float(lab_e["car"][-1])},
                  "osap": {k_: float(v.mean()) for k_, v in seg.items()} | {"year": py, "start": s0, "end": s1},
                  "osap_t": {k_: float(v.mean() / v.std(ddof=1) * np.sqrt(len(v))) for k_, v in seg.items()},
                  "osap_cum": cum, "osap_cum_t": (ym[w] // 100 + (ym[w] % 100 - 0.5) / 12)})


# ---------------------------------------------------------------------------
def compute_osap() -> dict:
    """Ch. 14: every predictor in Chen and Zimmermann's release 2024.10 (original papers' portfolios) with at least
    two years in sample and after publication, to December 2020: mean monthly long-short return in the original
    sample, out of sample before publication, and after publication; accounting predictors apart; a bootstrap over
    predictors of the decay ratio."""
    ym, names, M = _osap_matrix()
    _, doc = _osap()
    y = ym // 100
    recs = []
    for j, c in enumerate(names):
        r_ = doc.get(c)
        if not r_ or r_["Cat.Signal"] != "Predictor":
            continue
        try:
            s0, s1, py = int(r_["SampleStartYear"]), int(r_["SampleEndYear"]), int(r_["Year"])
        except ValueError:
            continue
        x = M[:, j]
        ins = x[(y >= s0) & (y <= s1) & np.isfinite(x)]
        oos = x[(y > s1) & (y <= py) & np.isfinite(x)]
        post = x[(y > py) & (y <= 2020) & np.isfinite(x)]
        if len(ins) < 24 or len(post) < 24:
            continue
        recs.append({"name": c, "cat": r_["Cat.Data"], "year": py, "in": float(ins.mean()),
                     "oos": float(oos.mean()) if len(oos) >= 12 else None, "post": float(post.mean()),
                     "authors": r_["Authors"]})

    def summary(rs):
        i_ = np.array([q["in"] for q in rs])
        o_ = np.array([q["oos"] for q in rs if q["oos"] is not None])
        p_ = np.array([q["post"] for q in rs])
        return {"n": len(rs), "in": float(i_.mean()), "oos": float(o_.mean()), "post": float(p_.mean()),
                "oos_ratio": float(o_.mean() / i_.mean()), "post_ratio": float(p_.mean() / i_.mean())}

    acc = [q for q in recs if q["cat"] == "Accounting"]
    rng = np.random.default_rng(0)
    boot = []
    for _ in range(2000):
        idx = rng.integers(0, len(recs), len(recs))
        boot.append(np.mean([recs[i]["post"] for i in idx]) / np.mean([recs[i]["in"] for i in idx]))
    ex = {q["name"]: q for q in recs if q["name"] in ("Accruals", "PS", "GP", "EarningsSurprise", "BM", "AssetGrowth")}
    return _json({"recs": recs, "all": summary(recs), "acc": summary(acc), "n_all": len(recs), "n_acc": len(acc),
                  "boot_lo": float(np.percentile(boot, 2.5)), "boot_hi": float(np.percentile(boot, 97.5)),
                  "examples": ex, "release": OSAP_RELEASE})


# ---------------------------------------------------------------------------
def compute_merger() -> dict:
    """Ch. 15: (a) The Merger Fund (MERFX), monthly total return, against the S&P 500 price index, January 1989 -
    December 2020: a piecewise-linear fit with a kink at a -4% market month, and a bootstrap of the extra slope below
    it; (b) Capri Holdings under Tapestry's $57 cash offer, weekly, 2023-24 (a case file, not a backtest)."""
    f = _yahoo("MERFX", "1mo", "1988-12-01", "2021-01-02")
    s = _yahoo("^GSPC", "1mo", "1988-12-01", "2021-01-02")
    km = {d // 100: v for d, v in zip(f["date"], f["adj"])}
    ks = {d // 100: v for d, v in zip(s["date"], s["adj"])}
    common = sorted(set(km) & set(ks))
    common = [c for c in common if c <= 202012]
    Mv, Sv = np.array([km[c] for c in common]), np.array([ks[c] for c in common])
    rm, rs = Mv[1:] / Mv[:-1] - 1, Sv[1:] / Sv[:-1] - 1
    kink = -0.04
    X = np.column_stack([np.ones_like(rs), rs, np.minimum(rs - kink, 0)])
    b = np.linalg.lstsq(X, rm, rcond=None)[0]
    rng = np.random.default_rng(5)
    boot = np.empty(5000)
    for i in range(5000):
        idx = rng.integers(0, len(rm), len(rm))
        boot[i] = np.linalg.lstsq(X[idx], rm[idx], rcond=None)[0][2]
    worst = int(np.argmin(rm))
    c = _yahoo("CPRI", "1wk", "2023-01-01", "2024-12-31")
    pre = c["date"] < 20230801  # bars are dated by their week's start: the last one to close before 10 Aug 2023
    B = float(c["close"][pre][-1])
    O = 57.0
    p = np.clip((c["close"] - B) / (O - B), -1, 1.2)
    return {"months": np.array(common[1:]), "rm": rm, "rs": rs, "alpha": float(b[0]), "beta_up": float(b[1]),
            "beta_extra": float(b[2]), "beta_down": float(b[1] + b[2]), "boot_lo": float(np.percentile(boot, 2.5)),
            "boot_hi": float(np.percentile(boot, 97.5)), "boot_p": float(np.mean(boot <= 0)),
            "mean": float(rm.mean() * 12), "vol": float(rm.std(ddof=1) * np.sqrt(12)), "worst": float(rm[worst]),
            "worst_mkt": float(rs[worst]), "worst_month": int(common[1:][worst]), "n": int(len(rm)),
            "cpri_date": c["date"], "cpri": c["close"], "cpri_B": B, "cpri_O": O, "cpri_p": p}


# ---------------------------------------------------------------------------
def compute_mscore() -> dict:
    """Ch. 16: Beneish's M-score for the seven non-bank firms, FY2010-2020, each year from the numbers in that year's
    10-K (the year and its comparative), and Kraft Heinz FY2016-17 as first reported and as restated."""
    panel = _edgar_annual_panel()
    out = []
    for cik, d in panel.items():
        it = d["items"]
        ends = sorted(e for e in it["sales"] if 20100101 <= e <= 20201231)
        for e in ends:
            prev = [x for x in it["sales"] if 330 < _days(x, e) < 400]
            if not prev:
                continue
            f0 = it["sales"][e][0][0]  # the filing that first reported the year

            def snap(end, t):
                return {k_: _asof(it[k_], end, t) for k_ in ALIASES}

            cur, prv = snap(e, f0), snap(prev[0], f0)
            if cur["assets"] is None or prv["assets"] is None:
                continue
            rt = valuation.beneish_ratios(cur, prv)
            mm = valuation.beneish_m(rt)
            later = snap(e, EDGAR_FROZEN), snap(prev[0], EDGAR_FROZEN)
            m_late = valuation.beneish_m(valuation.beneish_ratios(*later))
            out.append({"firm": FIRMS[cik], "year": e // 10000, "m": mm, "m_latest": m_late, "missing": rt["missing"],
                        "ratios": {k_: v for k_, v in rt.items() if k_ != "missing"}})
    M = np.array([o["m"] for o in out])
    kh = [o for o in out if o["firm"] == "Kraft Heinz" and o["year"] in (2016, 2017)]
    return _json({"rows": out, "m": M, "share_flagged": float(np.mean(M > -1.78)), "n": len(out), "khc": kh,
                  "base_rate": {"flag": 0.15, "fraud": 0.01, "catch": 0.5,
                                "ppv": 0.01 * 0.5 / 0.15}})


# ---------------------------------------------------------------------------
FEATURES = ["E_t", "E_{t-1}", "E_{t-2}", "CFO_t", "ACC_t", "CFO_{t-1}", "ACC_{t-1}", "growth_t", "growth_{t-1}",
            "loss", "dE", "noise_1", "noise_2", "noise_3"]


def _forecast_data(seed=21):
    p = fundamentals.earnings_panel(4000, 14, seed=seed, phi=0.8, phi_loss=0.4, mu=0.05, sd_roa=0.035)
    rng = np.random.default_rng(seed + 1)
    E, C, A, G = p["E"], p["CFO"], p["ACC"], p["growth"]
    rows = []
    for t in range(2, E.shape[1] - 1):
        f = np.column_stack([E[:, t], E[:, t - 1], E[:, t - 2], C[:, t], A[:, t], C[:, t - 1], A[:, t - 1], G[:, t],
                             G[:, t - 1], (E[:, t] < 0).astype(float), E[:, t] - E[:, t - 1],
                             rng.standard_normal((E.shape[0], 3)) * 0.03])
        rows.append((t, f, E[:, t + 1]))
    split = {"train": range(2, 9), "val": range(9, 11), "test": range(11, 13)}
    out = {}
    for k_, ts in split.items():
        out[k_] = (np.vstack([f for t, f, y in rows if t in ts]), np.concatenate([y for t, f, y in rows if t in ts]))
    floor = p["params"]["sd_roa"] ** 2 + p["params"]["sd_err"] ** 2
    return out, floor


def compute_forecaster() -> dict:
    """Ch. 18: next year's earnings (over assets) from 14 items on a simulated panel with known truth (profits
    persist with 0.8, losses with 0.4; accruals carry a reversing error; three items are pure noise).  Train on years
    2-8, choose on 9-10, test on 11-12.  A random walk, OLS, ridge on splines and a two-layer MLP (5 seeds, 30
    checkpoints); the MLP's width and weight decay chosen on validation from 4 configurations (logged trials)."""
    import torch

    torch.set_num_threads(1)
    d, floor = _forecast_data()
    (Xtr, ytr), (Xva, yva), (Xte, yte) = d["train"], d["val"], d["test"]
    mse = lambda a, b: float(np.mean((a - b) ** 2))  # noqa: E731
    res = {"rw": mse(Xte[:, 0], yte)}
    # least squares by lstsq: the items are collinear (earnings = cash flow + accruals), as real statements are
    beta = np.linalg.lstsq(np.column_stack([np.ones(len(ytr)), Xtr]), ytr, rcond=None)[0]
    pred_ols = beta[0] + Xte @ beta[1:]
    res["ols"] = mse(pred_ols, yte)
    best_lam, best = None, np.inf
    for lam in (0.01, 0.1, 1.0, 10.0):
        v = mse(econ.ridge_fit_predict(Xtr, ytr, Xva, lam=lam, knots=8), yva)
        if v < best:
            best_lam, best = lam, v
    pred_ridge = econ.ridge_fit_predict(np.vstack([Xtr]), ytr, Xte, lam=best_lam, knots=8)
    res["ridge"] = mse(pred_ridge, yte)
    mu, sd = Xtr.mean(0), Xtr.std(0)
    ysd = ytr.std()

    def tensor(a):
        return torch.tensor((a - mu) / sd, dtype=torch.float32)

    Ttr, Tva, Tte = tensor(Xtr), tensor(Xva), tensor(Xte)
    Ytr = torch.tensor(ytr / ysd, dtype=torch.float32)[:, None]
    epochs, ck = 60, 30

    def train(width, wd, seed):
        torch.manual_seed(seed)
        net = torch.nn.Sequential(torch.nn.Linear(Xtr.shape[1], width), torch.nn.ReLU(), torch.nn.Linear(width, width),
                                  torch.nn.ReLU(), torch.nn.Linear(width, 1))
        opt = torch.optim.Adam(net.parameters(), lr=1e-3, weight_decay=wd)
        g = torch.Generator().manual_seed(seed)
        val, test, snaps = [], [], []
        marks = set(np.unique(np.round(np.geomspace(1, epochs, ck)).astype(int)))
        for ep in range(1, epochs + 1):
            perm = torch.randperm(len(Ttr), generator=g)
            for i in range(0, len(Ttr), 512):
                b = perm[i:i + 512]
                opt.zero_grad()
                loss = torch.mean((net(Ttr[b]) - Ytr[b]) ** 2)
                loss.backward()
                opt.step()
            if ep in marks:
                with torch.no_grad():
                    pv = net(Tva).numpy().ravel() * ysd
                    pt = net(Tte).numpy().ravel() * ysd
                val.append(mse(pv, yva))
                test.append(mse(pt, yte))
                snaps.append((ep, pt[:400]))
        return {"val": val, "test": test, "epochs": [e for e, _ in snaps], "snaps": [s_ for _, s_ in snaps]}

    configs = [(16, 0.0), (16, 1e-4), (64, 0.0), (64, 1e-4)]
    sweep = {f"{w}x{wd}": train(w, wd, 0)["val"][-1] for w, wd in configs}
    bw, bwd = configs[int(np.argmin(list(sweep.values())))]
    runs = [train(bw, bwd, s_) for s_ in range(5)]
    mlp_test = np.array([r_["test"][-1] for r_ in runs])
    res["mlp"] = float(mlp_test.mean())
    best_seed = int(np.argmin([r_["val"][-1] for r_ in runs]))
    return {"res": _json(res), "floor": floor, "mlp_test": mlp_test, "val_curves": np.array([r_["val"] for r_ in runs]),
            "test_curves": np.array([r_["test"] for r_ in runs]), "epochs": np.array(runs[0]["epochs"]),
            "snaps": np.array(runs[best_seed]["snaps"]), "best_seed": best_seed, "y_test": yte[:400],
            "ols_test": pred_ols[:400], "ridge_lam": best_lam, "config": f"{bw} units, weight decay {bwd:g}",
            "sweep": sweep, "n_trials": 4 + len(configs), "features": FEATURES, "n_train": len(ytr),
            "n_test": len(yte), "var_y": float(yte.var())}


def compute_ohlson_theory() -> dict:
    """The research chapter: Ohlson's (1995) linear information dynamics.  The closed-form value against a Monte
    Carlo of discounted abnormal earnings; the persistence omega of abnormal earnings estimated on every EDGAR filer
    with positive book equity, fiscal 2010-2020 (net income and stockholders' equity from the XBRL frames), pooled
    and split by sign; and what each omega implies for price-to-book."""
    from explainer.quant.house import valuation as val
    checks = []
    for om, ga in ((0.0, 0.0), (0.6, 0.3), (0.9, 0.6), (0.62, 0.0)):
        f = val.ohlson_value(100.0, 5.0, 2.0, om, ga, 0.08)
        mc = val.ohlson_monte_carlo(100.0, 5.0, 2.0, om, ga, 0.08, n=20000, seed=int(om * 100 + ga * 10))
        checks.append({"omega": om, "gamma": ga, "formula": f["value"], "mc": mc, "a1": f["a1"], "a2": f["a2"]})
    r = 0.08
    NI = {y: data.sec_frame("NetIncomeLoss", f"CY{y}") for y in range(2010, 2021)}
    BE = {y: data.sec_frame("StockholdersEquity", f"CY{y}Q4I") for y in range(2009, 2021)}
    rows = []
    for y in range(2010, 2020):
        for cik, (b0, *_rest) in BE[y - 1].items():
            if cik not in NI[y] or cik not in NI[y + 1] or cik not in BE[y]:
                continue
            b1 = BE[y][cik][0]
            if not (b0 > 1e7 and b1 > 0):
                continue
            xa0 = NI[y][cik][0] - r * b0
            xa1 = NI[y + 1][cik][0] - r * b1
            rows.append((cik, y, xa0 / b0, xa1 / b0))
    R_ = np.array([r_[2:] for r_ in rows])
    lo, hi = np.quantile(R_, [0.01, 0.99], axis=0)
    R_ = np.clip(R_, lo, hi)
    groups = np.array([r_[0] for r_ in rows])
    pooled = econ.ols(R_[:, 1], R_[:, 0], se="cluster", groups=groups)
    neg = R_[:, 0] < 0
    by_sign = {}
    for k, m in (("loss", neg), ("profit", ~neg)):
        o = econ.ols(R_[m, 1], R_[m, 0], se="cluster", groups=groups[m])
        by_sign[k] = {"omega": float(o["beta"][1]), "se": float(o["se"][1]), "n": int(m.sum())}
    om = float(pooled["beta"][1])
    pick = np.random.default_rng(3).choice(len(R_), min(2500, len(R_)), replace=False)
    out = {"checks": checks, "r": r, "n_obs": int(len(R_)), "n_firms": int(len(set(groups))), "omega": om,
           "omega_se": float(pooled["se"][1]), "intercept": float(pooled["beta"][0]), "by_sign": by_sign,
           "scatter": R_[pick], "a1": om / (1 + r - om), "dhs_omega": 0.62}
    out["pb_at_5pct"] = {str(w): 1 + w / (1 + r - w) * 0.05 for w in (0.0, 0.62, om, 0.9, 1.0)}
    return _json(out)


ITEMS = {"shiller": compute_shiller, "cape": compute_cape, "factors": compute_factors, "dcf": compute_dcf,
         "timevalue": compute_timevalue, "duration": compute_duration, "statements": compute_statements,
         "accruals": compute_accruals, "pit": compute_pit, "dcf_mc": compute_dcf_mc, "erp": compute_erp,
         "ri": compute_ri, "campbell_shiller": compute_campbell_shiller, "payout": compute_payout,
         "merton": compute_merton, "pead": compute_pead, "osap": compute_osap, "merger": compute_merger,
         "mscore": compute_mscore, "forecaster": compute_forecaster, "envelope": compute_envelope, "ohlson_theory": compute_ohlson_theory}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
