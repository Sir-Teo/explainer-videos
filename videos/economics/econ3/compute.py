"""Precompute every number in Part 3 of *Economics, Built* ("The Measure").

    python -m videos.economics.econ3.compute            # everything missing (a minute or two)
    python -m videos.economics.econ3.compute --force world

Results are cached in ``.cache/econ3/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data come from the Data
Room (``explainer.economics.data``: FRED's national accounts, labour-market and price series, the World Bank's WDI,
the UNDP's Human Development Report, the Philadelphia Fed's real-time GDP, all frozen on 19 November 2026, and the
transcribed tables in ``data.tables``); models from Agora (``agora.accounts``: the Island's input-output table and
Leontief's inverse; ``agora.indices``: price indexes); the Island's parameters from ``explainer.economics.island``
(Part 3's truths).  Every random draw is seeded.

Items:
    kuznets       the 1934 report's tables 1 and 2: income produced and paid out, 1929-32, by type of payment, and
                  income paid out deflated by the cost-of-living index
    accounts      the Island's year three ways (output, expenditure, income) with the flows of the Sankey diagram,
                  saving and investment; the United States in 2025 (GDP, its parts, GDI and the statistical
                  discrepancy), and the expenditure shares of GDP 1929-2025
    unpaid        the Island's unpaid work against its GDP; BEA's household-production estimates
    indices       Bo's two baskets (Laspeyres, Paasche, Fisher, the true cost of living), the budget lines and the
                  indifference curve, chain drift over twelve stormy and calm seasons; US nominal and real GDP and
                  the deflator, 1929-2025
    hedonic       the boatyard's boats in two years: the naive change in the average price, the hedonic regression's
                  pure price change, against the planted truth
    cpi           the CPI-U against the chained CPI-U (from December 1999) and the PCE price index: the average
                  yearly gaps; the bias audits by source
    world         GDP at market exchange rates and at purchasing power parity, 2024: a Dorling cartogram of each
                  (circles' areas proportional to GDP, the US the same size in both), the price level against income
                  per head (the Penn effect), China's and India's two sizes
    unemployment  Dara's survey of the Island's 100 adults and its six rates; the US rates of October 2026; U-3 and
                  U-6 since 1994; participation and the employment ratio; the missing month
    distribution  the Island's 40 households: the Lorenz curve, the Gini, the shares; the WDI Gini across countries;
                  the distributional national accounts
    leontief      the Island's technical coefficients and inverse; the rounds of extra output for $10 more fish
                  exports; value added in exports
    revisions     real GDP growth in 2008 as each vintage reported it; first estimates against the latest since 1965;
                  the size of revisions
    beyond        the HDI against income per head (2023); Jones and Klenow's welfare against income
    kaldor        Kaldor's facts on US data: GDP per head on a log scale (Maddison), the labour share (PWT)
    film          the intermission's data film: the US unemployment rate, January 1948 to October 2026, month by month,
                  with the missing month
    melody        the intermission's data melody: the unemployment rate as a tune, a year a note, then a month a note
                  from 2025, with a rest where October 2025 is missing (saved as a clip)
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import accounts as acc
from explainer.economics.agora import indices as ix
from explainer.economics.data import tables

CACHE = Cache("econ3")
load = CACHE.load
TRUTH = island.truths(3)


def _fred(series: str, start: str = "", end: str = "9999") -> tuple[list, np.ndarray]:
    s = data.fred(series)
    keep = [(d, v) for d, v in zip(s["date"], s["value"]) if start <= d <= end]
    return [d for d, _ in keep], np.array([v for _, v in keep], float)


def _annual(series: str) -> dict:
    d, v = _fred(series)
    return {int(x[:4]): float(y) for x, y in zip(d, v) if np.isfinite(y)}


# ---------------------------------------------------------------------------
def compute_kuznets() -> dict:
    k = tables.KUZNETS_1934.data
    rel = lambda key: [100.0 * x / k[key][0] for x in k[key]]  # noqa: E731
    types = ("salaries_selected", "wages_selected", "salaries_wages_other", "dividends", "interest",
             "rents_royalties", "withdrawals")
    real_paid = [p / (c / 100.0) for p, c in zip(k["paid_out"], k["cost_of_living"])]
    return {
        "years": list(k["years"]), "paid_out": list(k["paid_out"]), "produced": list(k["produced"]),
        "business_savings": list(k["business_savings"]), "cost_of_living": list(k["cost_of_living"]),
        "paid_rel": rel("paid_out"), "produced_rel": rel("produced"),
        "real_paid": real_paid, "real_paid_rel": [100.0 * x / real_paid[0] for x in real_paid],
        "types": list(types), "type_rel": {t: rel(t) for t in types},
        "groups": {g: rel(g) for g in ("labour", "property", "entrepreneurial")},
        "fall_paid": 1 - k["paid_out"][-1] / k["paid_out"][0],
        "fall_produced": 1 - k["produced"][-1] / k["produced"][0],
    }


# ---------------------------------------------------------------------------
def _island_table() -> acc.IOTable:
    t = acc.IOTable(**TRUTH["accounts"])
    t.check()
    return t


def compute_accounts() -> dict:
    t = _island_table()
    names = list(t.industries)
    e = t.expenditure()
    g = t.gdp()
    out = {
        "industries": names,
        "gross": t.gross_output().tolist(), "inputs": t.inputs_used().tolist(), "va": t.value_added().tolist(),
        "Z": t.Z.tolist(), "imports_used": t.imports_used.tolist(),
        "final": {k: v.tolist() for k, v in t.final.items()}, "imports_final": t.imports_final,
        "expenditure": e, "income": t.income(), "gdp": g,
        "wages": t.wages.tolist(), "profits": t.profits.tolist(), "taxes": t.taxes.tolist(),
        # national saving = Y - C - G; it equals I + (X - M)
        "saving": g["output"] - e["C"] - e["G"], "nx": e["X"] - e["M"],
    }
    # the Sankey: income parts -> industries (value added) -> final uses (net of imports), all summing to GDP.
    # Industry j's value added is attributed to final uses in proportion to the domestic value added each use embodies
    v = t.value_added() / t.gross_output()
    L = t.leontief()
    uses = {}
    for k in ("C", "I", "G", "X"):
        uses[k] = (v * (L @ t.final[k])).tolist()  # value added of each industry embodied in use k
    out["va_by_use"] = uses
    # imports: the expenditure side counts C, I, G, X gross of imports, then subtracts M
    out["by_use_total"] = {k: float(np.sum(u)) for k, u in uses.items()}
    # the United States, 2025 (billions of current dollars)
    yr = 2025
    us = {k: _annual(s)[yr] for k, s in (("GDP", "GDPA"), ("GDI", "GDIA"), ("C", "PCECA"), ("I", "GPDIA"),
                                         ("G", "GCEA"), ("X", "EXPGSA"), ("M", "IMPGSA"),
                                         ("wages", "A033RC1A027NBEA"))}
    us["NX"] = us["X"] - us["M"]
    us["sum"] = us["C"] + us["I"] + us["G"] + us["NX"]
    us["discrepancy"] = us["GDP"] - us["GDI"]
    us["year"] = yr
    out["us"] = us
    # expenditure shares of GDP, 1929-2025
    gdp, c, i, gg, x, m = (_annual(s) for s in ("GDPA", "PCECA", "GPDIA", "GCEA", "EXPGSA", "IMPGSA"))
    years = sorted(set(gdp) & set(c) & set(i) & set(gg) & set(x) & set(m))
    out["shares"] = {"years": years,
                     "C": [c[y] / gdp[y] for y in years], "I": [i[y] / gdp[y] for y in years],
                     "G": [gg[y] / gdp[y] for y in years], "NX": [(x[y] - m[y]) / gdp[y] for y in years]}
    out["peak_G"] = max(zip(out["shares"]["G"], years))
    return out


def compute_unpaid() -> dict:
    t = _island_table()
    u = TRUTH["unpaid"]
    total = float(sum(u.values()))
    gdp = t.gdp()["output"]
    return {"items": list(u.items()), "total": total, "gdp": gdp, "share": total / gdp,
            "bea": {"1965": 39.0, "2010": 25.7}}


# ---------------------------------------------------------------------------
def compute_indices() -> dict:
    b = TRUTH["basket"]
    s = np.array(b["shares"])
    I = b["income"]
    p0, p1 = np.array(b["calm"]), np.array(b["storm"])
    q0, q1 = ix.cobb_douglas_demand(p0, I, s), ix.cobb_douglas_demand(p1, I, s)
    L, P, F = ix.laspeyres(p0, p1, q0), ix.paasche(p0, p1, q1), ix.fisher(p0, p1, q0, q1)
    T = ix.tornqvist(p0, p1, q0, q1)
    true = ix.cost_of_living(p0, p1, s)
    u0 = float(np.prod(q0 ** s))
    comp = I * true
    qc = ix.cobb_douglas_demand(p1, comp, s)       # what Bo buys if compensated exactly
    ql = ix.cobb_douglas_demand(p1, I * L, s)      # ... if compensated by Laspeyres
    out = {"p0": p0.tolist(), "p1": p1.tolist(), "q0": q0.tolist(), "q1": q1.tolist(), "income": I,
           "laspeyres": L, "paasche": P, "fisher": F, "tornqvist": T, "true": true, "u0": u0,
           "q_true": qc.tolist(), "q_lasp": ql.tolist(), "u_lasp": float(np.prod(ql ** s)),
           "cost_old_new": float(p1 @ q0), "cost_new_old": float(p0 @ q1)}
    # chain drift: twelve seasons alternating calm and storm, ending calm (prices end where they began)
    n = b["seasons"]
    prices = np.array([p0 if k % 2 == 0 else p1 for k in range(n + 1)])
    qs = np.array([ix.cobb_douglas_demand(p, I, s) for p in prices])
    out["chain"] = {f: ix.chained(prices, qs, f).tolist() for f in ("laspeyres", "paasche", "fisher", "tornqvist")}
    out["seasons"] = n
    # US nominal and real GDP and the deflator
    nom, real, defl = _annual("GDPA"), _annual("GDPCA"), _annual("A191RD3A086NBEA")
    years = sorted(set(nom) & set(real) & set(defl))
    out["us"] = {"years": years, "nominal": [nom[y] for y in years], "real": [real[y] for y in years],
                 "deflator": [defl[y] for y in years],
                 "fall_29_33_nominal": 1 - nom[1933] / nom[1929], "fall_29_33_real": 1 - real[1933] / real[1929],
                 "growth_nominal": (nom[2025] / nom[1929]) ** (1 / 96) - 1,
                 "growth_real": (real[2025] / real[1929]) ** (1 / 96) - 1,
                 "ratio_nominal": nom[2025] / nom[1929], "ratio_real": real[2025] / real[1929]}
    return out


def compute_hedonic() -> dict:
    h = TRUTH["boats"]
    rng = np.random.default_rng(h["seed"])
    rows = []
    for year in (0, 1):
        mu, sd = h["length"][year]
        L = np.clip(rng.normal(mu, sd, h["n"]), 3.5, 8.0)
        price = h["A"] * L ** h["B"] * (1 + h["inflation"]) ** year * np.exp(rng.normal(0, h["noise"], h["n"]))
        rows += [(year, float(l), float(p)) for l, p in zip(L, price)]
    yr = np.array([r[0] for r in rows], float)
    Ls = np.array([r[1] for r in rows])
    Ps = np.array([r[2] for r in rows])
    # log price on log length and a year dummy
    X = np.column_stack([np.ones_like(Ls), np.log(Ls), yr])
    beta, *_ = np.linalg.lstsq(X, np.log(Ps), rcond=None)
    resid = np.log(Ps) - X @ beta
    s2 = resid @ resid / (len(Ps) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    naive = Ps[yr == 1].mean() / Ps[yr == 0].mean() - 1
    return {"year": yr.tolist(), "length": Ls.tolist(), "price": Ps.tolist(), "beta": beta.tolist(),
            "se": se.tolist(), "pure": float(np.exp(beta[2]) - 1),
            "pure_ci": [float(np.exp(beta[2] - 1.96 * se[2]) - 1), float(np.exp(beta[2] + 1.96 * se[2]) - 1)],
            "naive": float(naive), "truth": h["inflation"], "B": h["B"],
            "mean_length": [float(Ls[yr == 0].mean()), float(Ls[yr == 1].mean())],
            "mean_price": [float(Ps[yr == 0].mean()), float(Ps[yr == 1].mean())]}


def compute_cpi() -> dict:
    d1, cpi = _fred("CPIAUCSL")
    d2, ccpi = _fred("SUUR0000SA0")
    d3, pce = _fred("PCEPI")
    a = dict(zip(d1, cpi))
    c = dict(zip(d2, ccpi))
    p = dict(zip(d3, pce))
    start, end = "1999-12-01", "2026-10-01"
    years = (int(end[:4]) - int(start[:4])) + (int(end[5:7]) - int(start[5:7])) / 12
    g_cpi = (a[end] / a[start]) ** (1 / years) - 1
    g_c = (c[end] / c[start]) ** (1 / years) - 1
    # CPI against PCE: both seasonally adjusted, to the last month of the PCE series
    pend = d3[-1]
    pyears = (int(pend[:4]) - 1999) + (int(pend[5:7]) - 12) / 12
    g_cpi_p = (a[pend] / a[start]) ** (1 / pyears) - 1
    g_pce = (p[pend] / p[start]) ** (1 / pyears) - 1
    months = [m for m in d2 if m >= start]
    series = {"months": months, "cpi": [a[m] / a[start] * 100 for m in months],
              "chained": [c[m] / c[start] * 100 for m in months],
              "pce": [p[m] / p[start] * 100 if m in p else float("nan") for m in months]}
    t = tables.CPI_BIAS.data
    return {"start": start, "end": end, "pce_end": pend, "years": years, "g_cpi": g_cpi, "g_chained": g_c,
            "gap_chained": g_cpi - g_c, "g_cpi_pce_window": g_cpi_p, "g_pce": g_pce, "gap_pce": g_cpi_p - g_pce,
            "cum_cpi": a[end] / a[start], "cum_chained": c[end] / c[start],
            "series": series, "audit": {k: t[k] for k in ("components", "boskin_1996", "lebow_rudd_2003",
                                                          "moulton_2018", "boskin_range", "lebow_rudd_range",
                                                          "moulton_range")},
            "audit_totals": [t["boskin_total"], t["lebow_rudd_total"], t["moulton_total"]]}


# ---------------------------------------------------------------------------
def _xy(lon: float, lat: float) -> np.ndarray:
    """An equirectangular projection onto the frame: longitude -170..190 across 13 units, latitude -50..72 up."""
    return np.array([-6.5 + 13.0 * (lon + 170) / 360, -3.3 + 6.0 * (lat + 50) / 122])


def _dorling(anchors: np.ndarray, r: np.ndarray, iters: int = 900) -> np.ndarray:
    """Circles that keep near their anchors without overlapping (a Dorling cartogram), by relaxation."""
    x = anchors.copy()
    order = np.argsort(-r)
    for it in range(iters):
        pull = 0.04 if it < iters * 0.7 else 0.012
        x += pull * (anchors - x)
        for a in range(3):
            d = x[:, None, :] - x[None, :, :]
            dist = np.sqrt((d ** 2).sum(-1)) + 1e-9
            need = r[:, None] + r[None, :] + 0.025
            over = np.clip(need - dist, 0, None)
            np.fill_diagonal(over, 0)
            push = (d / dist[..., None]) * over[..., None]
            wgt = r[None, :] ** 2 / (r[:, None] ** 2 + r[None, :] ** 2)
            x += 0.5 * (push * wgt[..., None]).sum(1)
        x[:, 0] = np.clip(x[:, 0], -6.8 + r, 6.8 - r)
        x[:, 1] = np.clip(x[:, 1], -3.5 + r, 3.0 - r)
    del order
    return x


def compute_world() -> dict:
    rows = [r for r in data.wdi(2024) if np.isfinite(r["gdp_usd"]) and np.isfinite(r["gdp_ppp"])
            and np.isfinite(r["lon"]) and r["pop"] > 1e6]
    rows.sort(key=lambda r: -r["gdp_ppp"])
    keep = rows[:70]
    us = next(r for r in rows if r["code"] == "USA")
    k = 0.95 / np.sqrt(us["gdp_usd"])      # the US circle has radius 0.95 in both maps
    anchors = np.array([_xy(r["lon"], r["lat"]) for r in keep])
    r_mkt = np.array([k * np.sqrt(r["gdp_usd"]) for r in keep])
    r_ppp = np.array([k * np.sqrt(r["gdp_ppp"]) for r in keep])
    pos_mkt = _dorling(anchors, r_mkt)
    pos_ppp = _dorling(anchors, r_ppp)
    world_usd = sum(r["gdp_usd"] for r in data.wdi(2024) if np.isfinite(r["gdp_usd"]))
    world_ppp = sum(r["gdp_ppp"] for r in data.wdi(2024) if np.isfinite(r["gdp_ppp"]))
    out = {"codes": [r["code"] for r in keep], "names": [r["country"] for r in keep],
           "regions": [r["region"] for r in keep],
           "gdp_usd": [r["gdp_usd"] for r in keep], "gdp_ppp": [r["gdp_ppp"] for r in keep],
           "r_mkt": r_mkt.tolist(), "r_ppp": r_ppp.tolist(), "pos_mkt": pos_mkt.tolist(),
           "pos_ppp": pos_ppp.tolist(), "world_usd": world_usd, "world_ppp": world_ppp,
           "share_kept_usd": sum(r["gdp_usd"] for r in keep) / world_usd}
    # the Penn effect: price level (market GDP / PPP GDP, US = 1) against PPP income per head
    pts = [r for r in data.wdi(2024) if np.isfinite(r["gdppc_usd"]) and np.isfinite(r["gdppc_ppp"])
           and r["pop"] > 1e6]
    out["penn"] = {"codes": [r["code"] for r in pts], "names": [r["country"] for r in pts],
                   "income_ppp": [r["gdppc_ppp"] for r in pts],
                   "price_level": [r["gdppc_usd"] / r["gdppc_ppp"] for r in pts],
                   "pop": [r["pop"] for r in pts]}
    x = np.log(np.array(out["penn"]["income_ppp"]))
    y = np.log(np.array(out["penn"]["price_level"]))
    w = np.array(out["penn"]["pop"])
    out["penn"]["slope"] = float(np.polyfit(x, y, 1)[0])
    out["penn"]["corr"] = float(np.corrcoef(x, y)[0, 1])
    del w
    for code in ("CHN", "IND", "USA", "JPN", "DEU", "IDN", "NGA", "ETH", "CHE", "BRA", "RUS"):
        r = next((r for r in data.wdi(2024) if r["code"] == code), None)
        if r:
            out[code] = {k: r[k] for k in ("country", "gdp_usd", "gdp_ppp", "gdppc_usd", "gdppc_ppp", "pop")}
    dh = tables.DEATON_HESTON_2010.data
    out["icp2005"] = {"china": dh["china_smaller"], "india": dh["india_smaller"]}
    return out


# ---------------------------------------------------------------------------
def compute_unemployment() -> dict:
    s = TRUTH["survey"]
    emp_full = s["employed full time or by choice part time"]
    ptr = s["employed part time, wanting full time"]
    long_u = s["unemployed 15 weeks or more"]
    short_u = s["unemployed, lost a job in the last 15 weeks"]
    disc = s["discouraged"]
    marg = s["marginally attached, other reasons"]
    nilf = s["not in the labour force"]
    E_ = emp_full + ptr
    U = long_u + short_u
    LF = E_ + U
    pop = E_ + U + disc + marg + nilf
    island_rates = {"U-1": long_u / LF, "U-2": short_u / LF, "U-3": U / LF, "U-4": (U + disc) / (LF + disc),
                    "U-5": (U + disc + marg) / (LF + disc + marg),
                    "U-6": (U + disc + marg + ptr) / (LF + disc + marg)}
    out = {"survey": list(s.items()), "pop": pop, "employed": E_, "unemployed": U, "labour_force": LF,
           "participation": LF / pop, "employment_ratio": E_ / pop, "island": island_rates}
    us = {}
    for k, sid in (("U-1", "U1RATE"), ("U-2", "U2RATE"), ("U-3", "UNRATE"), ("U-4", "U4RATE"), ("U-5", "U5RATE"),
                   ("U-6", "U6RATE")):
        d, v = _fred(sid)
        ok = np.isfinite(v)
        us[k] = float(v[ok][-1])
        us[k + "_month"] = [x for x, o in zip(d, ok) if o][-1]
    out["us"] = us
    d, u3 = _fred("UNRATE", "1994-01-01")
    _, u6 = _fred("U6RATE", "1994-01-01")
    out["history"] = {"months": d, "u3": u3.tolist(), "u6": u6.tolist()}
    for sid in ("CIVPART", "EMRATIO"):
        dd, vv = _fred(sid)
        ok = np.isfinite(vv)
        out[sid] = {"last": float(vv[ok][-1]), "month": [x for x, o in zip(dd, ok) if o][-1],
                    "peak": float(np.nanmax(vv)),
                    "peak_month": dd[int(np.nanargmax(vv))]}
    # the missing month: every month since January 1948 has a rate except these
    dU, vU = _fred("UNRATE")
    out["missing"] = [x for x, v in zip(dU, vU) if not np.isfinite(v)]
    out["months_total"] = len(dU)
    return out


# ---------------------------------------------------------------------------
def _gini(x: np.ndarray) -> float:
    x = np.sort(np.asarray(x, float))
    n = len(x)
    return float((2 * np.arange(1, n + 1) - n - 1) @ x / (n * x.sum()))


def _lorenz(x: np.ndarray) -> tuple[list, list]:
    x = np.sort(np.asarray(x, float))
    c = np.concatenate([[0.0], np.cumsum(x)]) / x.sum()
    return np.linspace(0, 1, len(x) + 1).tolist(), c.tolist()


def compute_distribution() -> dict:
    h = TRUTH["households"]
    t = _island_table()
    rng = np.random.default_rng(h["seed"])
    n = h["n"]
    w = np.exp(rng.normal(0, h["wage_sigma"], n - 2))
    wages = np.concatenate([w / w.sum() * float(t.wages.sum()), [0.0, 0.0]])  # Friday and Crusoe draw no wage
    prof = np.zeros(n)
    prof[-2], prof[-1] = h["friday"], h["crusoe"]
    k, amount = h["small_owners"]
    small = rng.choice(n - 2, k, replace=False)
    prof[small] += amount / k
    inc = wages + prof
    assert abs(inc.sum() - (t.wages.sum() + t.profits.sum())) < 1e-6
    xs, ys = _lorenz(inc)
    srt = np.sort(inc)
    out = {"incomes": inc.tolist(), "names": [f"h{i}" for i in range(n - 2)] + ["Friday", "Crusoe"],
           "lorenz_x": xs, "lorenz_y": ys, "gini": _gini(inc), "gini_wages": _gini(wages[:-2]),
           "bottom50": float(srt[: n // 2].sum() / srt.sum()), "top10": float(srt[-n // 10:].sum() / srt.sum()),
           "top2_share": float(srt[-2:].sum() / srt.sum()), "total": float(inc.sum())}
    # the WDI Gini: each country's latest estimate, 2015-2024
    latest = {}
    for r in data.wdi():
        if np.isfinite(r["gini"]) and r["year"] <= 2024 and r["pop"] > 1e6:
            if r["code"] not in latest or r["year"] > latest[r["code"]]["year"]:
                latest[r["code"]] = r
    g = sorted(latest.values(), key=lambda r: r["gini"])
    out["wdi"] = {"codes": [r["code"] for r in g], "names": [r["country"] for r in g],
                  "gini": [r["gini"] for r in g], "year": [r["year"] for r in g]}
    out["wdi_n"] = len(g)
    p = tables.PSZ_2018.data
    out["psz"] = {k: p[k] for k in ("bottom50_share", "top1_share", "years", "bottom50_income", "average_growth",
                                    "ratio", "as_top1_pretax_rise", "as_top1_aftertax_rise", "as_years")}
    return out


# ---------------------------------------------------------------------------
def compute_leontief() -> dict:
    t = _island_table()
    A = t.coefficients()
    L = t.leontief()
    f = np.array([10.0, 0, 0, 0])      # ten dollars more of fish sold abroad
    rounds = [f]
    for _ in range(7):
        rounds.append(A @ rounds[-1])
    cum = np.cumsum(rounds, axis=0)
    va = t.value_added_in("X")
    v = t.value_added() / t.gross_output()
    return {"industries": list(t.industries), "A": A.tolist(), "L": L.tolist(),
            "multipliers": L.sum(axis=0).tolist(), "rounds": [r.tolist() for r in rounds],
            "cumulative": cum.tolist(), "total": (L @ f).tolist(), "f": f.tolist(),
            "va_share_exports": va["share"], "va_exports": va["domestic_value_added"], "exports": va["gross"],
            "va_ratio": v.tolist(),
            "import_ratio": (t.imports_used / t.gross_output()).tolist()}


# ---------------------------------------------------------------------------
def compute_revisions() -> dict:
    r = data.rtdsm()
    q = r["quarters"]
    show = ["2008:Q1", "2008:Q2", "2008:Q3", "2008:Q4", "2009:Q1", "2009:Q2"]
    growth = {}
    for v in r["vintages"]:
        lv = r["level"][v]
        g = {}
        for s in show:
            i = q.index(s)
            a, b = lv[i], lv[i - 1]
            if np.isfinite(a) and np.isfinite(b):
                g[s] = 100 * ((a / b) ** 4 - 1)
        if g:
            growth[v] = g
    fl = [x for x in r["first_latest"] if x["quarter"] <= "2023:Q4"]     # at least three years of revisions
    first = np.array([x["first"] for x in fl])
    latest = np.array([x["latest"] for x in fl])
    rev = latest - first
    sign_flip = int(np.sum(np.sign(first) != np.sign(latest)))
    return {"show": show, "vintages": list(growth), "growth": growth,
            "first_latest": {"quarters": [x["quarter"] for x in fl], "first": first.tolist(),
                             "latest": latest.tolist()},
            "mean_abs_rev": float(np.mean(np.abs(rev))), "mean_rev": float(np.mean(rev)),
            "sd_rev": float(np.std(rev)), "corr": float(np.corrcoef(first, latest)[0, 1]),
            "sign_flips": sign_flip, "n": len(fl),
            "biggest": sorted(zip(np.abs(rev).tolist(), [x["quarter"] for x in fl], first.tolist(),
                                  latest.tolist()))[-5:]}


def compute_beyond() -> dict:
    rows = [r for r in data.hdr() if 2023 in r["hdi"] and 2023 in r["gnipc"]]
    out = {"codes": [r["code"] for r in rows], "names": [r["country"] for r in rows],
           "hdi": [r["hdi"][2023] for r in rows], "gnipc": [r["gnipc"][2023] for r in rows],
           "le": [r["le"].get(2023, float("nan")) for r in rows]}
    x = np.log(np.array(out["gnipc"]))
    out["corr_log"] = float(np.corrcoef(x, np.array(out["hdi"]))[0, 1])
    jk = tables.JONES_KLENOW_2016.data
    out["jk"] = {"rows": [list(r) for r in jk["rows"]], "france": jk["france"], "corr": jk["correlation"]}
    nt = tables.NORDHAUS_TOBIN_1972.data
    out["nt"] = nt
    return out


def compute_kaldor() -> dict:
    us = data.maddison_country("USA")
    yrs = [y for y in us["year"] if 1870 <= y <= 2022]
    g = [us["gdppc"][us["year"].index(y)] for y in yrs]
    slope = np.polyfit(yrs, np.log(g), 1)[0]
    d, ls = _fred("LABSHPUSA156NRUG")
    years = [int(x[:4]) for x in d]
    return {"years": yrs, "gdppc": g, "trend_growth": float(np.exp(slope) - 1),
            "ls_years": years, "labour_share": ls.tolist(),
            "ls_1950_79": float(np.mean(ls[[i for i, y in enumerate(years) if 1950 <= y <= 1979]])),
            "ls_2010_23": float(np.mean(ls[[i for i, y in enumerate(years) if 2010 <= y <= 2023]])),
            "ls_last": float(ls[-1]), "ls_last_year": years[-1]}


# ---------------------------------------------------------------------------
FILM_SECONDS = 36.0
MELODY_SECONDS = 46.0
ANNUAL_END = 2024          # a note a year up to here, then a note a month


def film_time(month: str) -> float:
    """When the data film reaches ``month`` ("YYYY-MM"): 1948-2024 take the first 26 seconds, January 2025 to October
    2026 the last ten, so the months around the missing one can be heard one by one."""
    y, m = int(month[:4]), int(month[5:7])
    if y <= ANNUAL_END:
        return 1.5 + 26.0 * ((y - 1948) * 12 + (m - 1)) / ((ANNUAL_END - 1948 + 1) * 12)
    k = (y - 2025) * 12 + (m - 1)            # 0 .. 21
    return 1.5 + 26.0 + 10.0 * k / 21


def compute_film() -> dict:
    d, v = _fred("UNRATE", "1948-01-01")
    months = [x[:7] for x in d]
    return {"months": months, "u3": v.tolist(), "missing": [m for m, x in zip(months, v) if not np.isfinite(x)],
            "times": [film_time(m) for m in months], "peaks": {
                "1949": float(np.nanmax(v[[i for i, m in enumerate(months) if m.startswith("1949")]])),
                "1982": float(np.nanmax(v[[i for i, m in enumerate(months) if m.startswith("1982")]])),
                "2009": float(np.nanmax(v[[i for i, m in enumerate(months) if m.startswith("2009")]])),
                "2020": float(np.nanmax(v[[i for i, m in enumerate(months) if m.startswith("2020")]]))},
            "low": float(np.nanmin(v)), "low_month": months[int(np.nanargmin(v))]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    d, v = _fred("UNRATE", "1948-01-01")
    months = [x[:7] for x in d]
    vals, times, names = [], [], []
    for y in range(1948, ANNUAL_END + 1):
        xs = [x for m, x in zip(months, v) if m.startswith(str(y)) and np.isfinite(x)]
        vals.append(float(np.mean(xs)))
        times.append(film_time(f"{y}-07"))
        names.append(str(y))
    for m, x in zip(months, v):
        if int(m[:4]) > ANNUAL_END and np.isfinite(x):      # October 2025 has no value: a rest
            vals.append(float(x))
            times.append(film_time(m))
            names.append(m)
    mel = score.data_melody(np.array(vals), MELODY_SECONDS, times=times, act=1, log=False)
    events = {f"t{n}": float(t) for n, t in zip(names, times)}
    events["rest"] = film_time("2025-10")
    events["film_end"] = film_time("2026-10") + 1.5
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.5, "hz": score.hz(n), "name": nm}
                       for t, n, nm in zip(times, mel["notes"], names)],
                meta={"label": "the US unemployment rate, 1948-2026, as a tune, with a rest for October 2025 "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ3").save("intermission.melody", clip)
    return {"names": names, "values": vals, "times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS,
            "film_seconds": FILM_SECONDS, "rest": film_time("2025-10")}


ITEMS = {
    "kuznets": compute_kuznets,
    "accounts": compute_accounts,
    "unpaid": compute_unpaid,
    "indices": compute_indices,
    "hedonic": compute_hedonic,
    "cpi": compute_cpi,
    "world": compute_world,
    "unemployment": compute_unemployment,
    "distribution": compute_distribution,
    "leontief": compute_leontief,
    "revisions": compute_revisions,
    "beyond": compute_beyond,
    "kaldor": compute_kaldor,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
