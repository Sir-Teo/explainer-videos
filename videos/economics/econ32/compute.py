"""Precompute every number in Part 32 of *Economics, Built* ("The Treasury").

    python -m videos.economics.econ32.compute            # everything missing (about a minute)
    python -m videos.economics.econ32.compute --force rz

Results are cached in ``.cache/econ32/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Reinhart and Rogoff's spreadsheet as processed by Herndon, Ash and Pollin; Ramey and
Zubairy's quarterly data since 1889; Ramey's tax data with Romer and Romer's narrative tax changes; Blanchard and
Leigh's forecast errors; FRED's deficit, debt, interest, unemployment, yield and GDP series).  Models: Agora's treasury
(``agora.fiscal``) with the Island's Part 32 truths.

Items:
    hap          growth by public-debt band: Reinhart and Rogoff's published figures, and each correction in turn
    debt         US federal debt held by the public as a share of GDP, 1889-2026
    budget       the Island's debt dynamics for r - g of +2, 0 and -2 points, and the stabilizing surplus
    playit       the minister's budget: the surplus that holds the Island's debt steady
    nk           the spending multiplier over persistence, in normal times and at the zero bound
    rz           cumulative spending multipliers by local projections, military news and Blanchard-Perotti timing
    regions      the Island's currency union: the local multiplier and the missing intercept
    bl           Blanchard and Leigh's forecast errors against planned consolidation
    taxes        output after Romer and Romer's exogenous tax changes, by local projections
    stabilizers  the federal deficit and unemployment, 1948-2025
    rg           r - g in the United States, 1954-2025
    war          tax smoothing through a war; US debt through 1917-19 and 1941-46
    unpleasant   Sargent and Wallace's arithmetic
    default      Arellano's model solved and simulated; Greece's yield
    interest     federal interest payments as a share of GDP
    film         the intermission's data film: federal debt to GDP, quarter by quarter, since 1889
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import fiscal

CACHE = Cache("econ32")
load = CACHE.load
TRUTH = island.truths(32)
FILM_SECONDS = 50.0
BINS = ((0, 30), (30, 60), (60, 90), (90, 1e9))


def _series(key: str, first: str = "0000", last: str = "9999") -> dict:
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v) and first <= x <= last}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12


def _annual(key: str, first: str = "0000", last: str = "9999") -> dict:
    out: dict = {}
    for x, v in _series(key, first, last).items():
        out.setdefault(int(x[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items()}


def compute_hap() -> dict:
    R = data.rr_hap()
    c, y = np.array(R["country"]), np.array(R["year"], int)
    d, g = np.array(R["debtgdp"], float), np.array(R["growth"], float)
    ok = np.isfinite(d) & np.isfinite(g) & ~((c == "Italy") & (y < 1951))
    cat = np.full(len(d), -1)
    for k, (a, b) in enumerate(BINS):
        cat[ok & (d > a) & (d <= b)] = k
    five = np.isin(c, ["Australia", "Austria", "Belgium", "Canada", "Denmark"])
    early = ((c == "New Zealand") & (y < 1950)) | ((c == "Australia") & (y < 1951)) | ((c == "Canada") & (y < 1951))

    def pooled(mask):
        return [float(g[mask & (cat == k)].mean()) for k in range(4)]

    def country_means(mask, nz=False):
        out = []
        for k in range(4):
            vals = []
            for cc in np.unique(c[mask & (cat == k)]):
                m = float(g[mask & (cat == k) & (c == cc)].mean())
                if nz and k == 3 and cc == "New Zealand":
                    m = -7.9
                vals.append(m)
            out.append(float(np.mean(vals)))
        return out

    base = ok & (cat >= 0)
    steps = [
        ("published", country_means(base & ~five & ~early, nz=True)),
        ("New Zealand's figure as in the data", country_means(base & ~five & ~early)),
        ("the five countries back", country_means(base & ~early)),
        ("the excluded years back", country_means(base)),
        ("every country-year counted once", pooled(base)),
    ]
    nz_hi = base & (c == "New Zealand") & (cat == 3)
    years_hi = {str(cc): int((base & (cat == 3) & (c == cc)).sum()) for cc in np.unique(c[base & (cat == 3)])}
    scatter = [(float(a), float(b)) for a, b in zip(d[base], g[base]) if a <= 250]
    return {"bins": ["0-30%", "30-60%", "60-90%", "above 90%"], "steps": [{"name": n, "means": m} for n, m in steps],
            "n_high": int((base & (cat == 3)).sum()), "countries_high": years_hi,
            "nz_high_years": [int(v) for v in y[nz_hi]], "nz_high_growth": [float(v) for v in g[nz_hi]],
            "scatter": scatter, "medians": [float(np.median(g[base & (cat == k)])) for k in range(4)],
            "n_countries": int(len(np.unique(c[base])))}


def compute_debt() -> dict:
    R = data.ramey_zubairy()
    q = np.array(R["quarter"], float)
    debt, ng = np.array(R["pubfeddebt_treas"], float), np.array(R["ngdp"], float)
    t, v = [], []
    for qq, a, b in zip(q, debt, ng):
        if 1889 <= qq < 1970 and np.isfinite(a) and np.isfinite(b) and b > 0:
            t.append(float(qq))
            v.append(float(100 * a / b))
    f = _series("FYGFGDQ188S")
    for d_ in sorted(f):
        t.append(_t(d_))
        v.append(f[d_])
    t, v = np.array(t), np.array(v)

    def at(x):
        return float(v[np.argmin(np.abs(t - x))])

    k = int(np.argmax(v))
    return {"t": t.tolist(), "debt": v.tolist(), "peak": float(v[k]), "peak_t": float(t[k]), "d1916": at(1916.0),
            "d1919": at(1919.5), "d1940": at(1940.0), "d1974": at(1974.0), "d2007": at(2007.0),
            "d2020": at(2020.75), "last": float(v[-1]), "last_t": float(t[-1])}


def compute_budget() -> dict:
    B = TRUTH["budget"]
    out = {}
    for name, rg in (("plus", 0.02), ("zero", 0.0), ("minus", -0.02)):
        r = B["g"] + rg
        out[name] = {"r": r, "debt": fiscal.debt_path(B["debt"], r, B["g"], -B["deficit"], B["years"]),
                     "balanced": fiscal.debt_path(B["debt"], r, B["g"], 0.0, B["years"]),
                     "stabilizing": fiscal.stabilizing_surplus(B["debt"], r, B["g"])}
    return {"years": list(range(B["years"] + 1)), **out, "g": B["g"], "b0": B["debt"], "deficit": B["deficit"]}


def compute_playit() -> dict:
    B = TRUTH["budget"]
    s = fiscal.stabilizing_surplus(B["debt"], B["r"], B["g"])
    swing = s + B["deficit"]
    return {**B, "stabilizing": s, "swing": swing, "loss_m05": 0.5 * swing, "loss_m15": 1.5 * swing,
            "options": ["a surplus of about 1%", "a balanced primary budget", "a deficit of 1% is enough"],
            "answer": 0}


def compute_nk() -> dict:
    N = TRUTH["nk"]
    C = fiscal.nk_multiplier_curve(np.linspace(0.0, 0.72, 73), gamma=N["gamma"], gy=N["gy"])
    pts = {f"{r:.1f}": {"normal": fiscal.nk_multiplier(r, gamma=N["gamma"], gy=N["gy"])["multiplier"],
                        "zlb": fiscal.nk_multiplier(r, zlb=True, gamma=N["gamma"], gy=N["gy"])["multiplier"]}
           for r in N["rhos"]}
    edge = max(r for r, z in zip(C["rho"], C["zlb"]) if np.isfinite(z))
    return {**C, "points": pts, "edge": float(edge), "gamma": N["gamma"]}


def compute_rz() -> dict:
    S = fiscal.rz_series(data.ramey_zubairy())
    news = fiscal.lp_multiplier(S, "news")
    bp = fiscal.lp_multiplier(S, "bp")
    slack = fiscal.lp_multiplier(S, "news", state="slack")
    zlb = fiscal.lp_multiplier(S, "news", state="zlb")
    q = S["quarter"]
    nz = np.array(S["news"])
    big = sorted([(float(abs(v)), float(qq)) for v, qq in zip(nz, q) if np.isfinite(v)], reverse=True)[:6]
    return {"h": news["h"], "news": news["multiplier"], "bp": bp["multiplier"], "slack_high": slack["high"],
            "slack_low": slack["low"], "zlb_high": zlb["high"], "zlb_low": zlb["low"],
            "news8": news["multiplier"][8], "bp8": bp["multiplier"][8], "news16": news["multiplier"][16],
            "slack8": slack["high"][8], "normal8": slack["low"][8], "zlb8": zlb["high"][8],
            "share_slack": slack["share_high"], "share_zlb": zlb["share_high"],
            "q": q.tolist(), "news_series": [float(v) if np.isfinite(v) else None for v in nz],
            "biggest": [b[1] for b in big]}


def compute_regions() -> dict:
    return fiscal.regions(**TRUTH["regions"])


def compute_bl() -> dict:
    B = data.blanchard_leigh()
    cc, yy = np.array(B["wdicode"]), np.array(B["year"], float)
    names = np.array(B["country"])
    eu = np.array(B["eu"], float)
    gf, gs, sb = (np.array(B[k], float) for k in ("growth_fall2012", "growth_spring2010", "sb_spring2010"))
    rows = []
    for code in np.unique(cc):
        m = {int(a): (b, e, f, h) for a, b, e, f, h in zip(yy[cc == code], gf[cc == code], gs[cc == code],
                                                          sb[cc == code], eu[cc == code])}
        if not all(t in m for t in (2009, 2010, 2011)):
            continue
        if not (m[2011][3] == 1 or code in ("CHE", "ISL", "NOR")):
            continue
        err = 100 * ((1 + m[2011][0] / 100) * (1 + m[2010][0] / 100) - 1) - 100 * (
            (1 + m[2011][1] / 100) * (1 + m[2010][1] / 100) - 1)
        x = m[2011][2] - m[2009][2]
        if np.isfinite(err) and np.isfinite(x):
            rows.append({"code": str(code), "name": str(names[cc == code][0]), "x": float(x), "err": float(err)})
    X = np.column_stack([np.ones(len(rows)), [r["x"] for r in rows]])
    Y = np.array([r["err"] for r in rows])
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    e = Y - X @ b
    V = np.linalg.inv(X.T @ X) * (e @ e) / (len(Y) - 2)
    return {"rows": rows, "a": float(b[0]), "b": float(b[1]), "se": float(np.sqrt(V[1, 1])), "n": len(rows),
            "r2": float(1 - (e @ e) / ((Y - Y.mean()) @ (Y - Y.mean())))}


def compute_taxes() -> dict:
    T = data.ramey_tax()
    q = np.array(T["quarter"], float)
    ly = np.log(np.array(T["rgdp"], float))
    x = np.array(T["exog_rr"], float)
    en = np.array(T["endog_rr"], float)
    ok = np.isfinite(ly) & np.isfinite(x)
    q, ly, x, en = q[ok], ly[ok], x[ok], en[ok]
    dy = np.concatenate([[np.nan], np.diff(ly)])
    H, p = 16, 4
    out = []
    for h in range(H + 1):
        Y = np.concatenate([ly[h:], np.full(h, np.nan)]) - np.concatenate([[np.nan], ly[:-1]])
        cols = [np.ones(len(x)), x] + [np.concatenate([np.full(j, np.nan), x[:-j]]) for j in range(1, p + 1)] + \
               [np.concatenate([np.full(j, np.nan), dy[:-j]]) for j in range(1, p + 1)]
        Xm = np.column_stack(cols)
        okr = np.isfinite(Y) & np.all(np.isfinite(Xm), axis=1)
        b, *_ = np.linalg.lstsq(Xm[okr], Y[okr], rcond=None)
        out.append(float(100 * b[1]))       # percent of GDP per percentage point of GDP of tax change
    lo = int(np.argmin(out))
    events = [(float(a), float(b)) for a, b in zip(q, x) if abs(b) > 0]
    endog = [(float(a), float(b)) for a, b in zip(q, en) if np.isfinite(b) and abs(b) > 0]
    return {"h": list(range(H + 1)), "resp": out, "trough": out[lo], "trough_h": lo, "at12": out[12],
            "events": events, "endog": endog, "n_endog": len(endog), "n_changes": int((np.abs(x) > 0).sum()),
            "first": float(q[0]), "last": float(q[-1])}


def compute_stabilizers() -> dict:
    d = {int(k[:4]): v for k, v in _series("FYFSGDA188S").items()}
    u = _annual("UNRATE")
    yrs = sorted(y for y in d if y in u and y >= 1948)
    dd = np.diff([d[y] for y in yrs])
    du = np.diff([u[y] for y in yrs])
    b = float(np.polyfit(du, dd, 1)[0])
    return {"years": yrs, "deficit": [d[y] for y in yrs], "unemp": [u[y] for y in yrs], "slope": b,
            "corr": float(np.corrcoef(du, dd)[0, 1]), "d2009": d[2009], "d2020": d[2020], "d2007": d[2007],
            "d2019": d[2019], "u2009": u[2009], "u2020": u[2020]}


def compute_rg() -> dict:
    r1 = _annual("GS1")
    r10 = _annual("GS10")
    gdp = _annual("GDP")
    yrs = sorted(y for y in r1 if y in gdp and y - 1 in gdp and y in r10 and 1954 <= y <= 2025)
    g = {y: 100 * (gdp[y] / gdp[y - 1] - 1) for y in yrs}
    rg1 = [r1[y] - g[y] for y in yrs]
    rg10 = [r10[y] - g[y] for y in yrs]
    return {"years": yrs, "rg1": rg1, "rg10": rg10, "share1": float(np.mean(np.array(rg1) < 0)),
            "share10": float(np.mean(np.array(rg10) < 0)), "mean1": float(np.mean(rg1)),
            "mean10": float(np.mean(rg10)), "last1": rg1[-1], "last10": rg10[-1], "last_year": yrs[-1]}


def compute_war() -> dict:
    W = TRUTH["war"]
    path = [W["normal"]] * W["before"] + [W["war"]] * W["length"] + [W["normal"]] * W["after"]
    T = fiscal.tax_smoothing(path, r=W["r"])
    D = compute_debt()
    t, v = np.array(D["t"]), np.array(D["debt"])
    sl = (t >= 1910) & (t <= 1960)
    return {**T, "us_t": t[sl].tolist(), "us_debt": v[sl].tolist(), "d1941": float(v[np.argmin(np.abs(t - 1941))]),
            "d1946": float(v[np.argmin(np.abs(t - 1946.25))]), "d1960": float(v[np.argmin(np.abs(t - 1960))])}


def compute_unpleasant() -> dict:
    U = TRUTH["unpleasant"]
    out = fiscal.unpleasant(T_tight=U["T_tight"], years=U["years"], deficit=U["deficit"], b0=U["b0"], r=U["r"],
                            g=U["g"], base=U["base"], mu_tight=U["mu_tight"])
    F = TRUTH["ftpl"]
    out["ftpl"] = {"P": fiscal.ftpl_price_level(F["B"], F["surplus"], F["r"]),
                   "P_low": fiscal.ftpl_price_level(F["B"], F["surplus_low"], F["r"]), **F}
    return out


def compute_default() -> dict:
    M = fiscal.arellano()
    S = fiscal.arellano_simulate(M, seed=7)
    y, B, q = np.array(M["y"]), np.array(M["B"]), np.array(M["q"])
    D = np.array(M["default"], bool)
    iy = {"low": 3, "mid": len(y) // 2, "high": len(y) - 4}
    sched = {k: q[i].tolist() for k, i in iy.items()}
    thr = []                                   # for each income, the largest debt that is repaid
    for i in range(len(y)):
        rep = [-b for b, d_ in zip(B, D[i]) if not d_]
        thr.append(max(rep) if rep else 0.0)
    gr = _series("IRLTLT01GRM156N", "2007-01-01", "2016-12-01")
    de = _series("IRLTLT01DEM156N", "2007-01-01", "2016-12-01")
    ds = sorted(set(gr) & set(de))
    return {"B": B.tolist(), "y": y.tolist(), "sched": sched, "y_levels": {k: float(y[i]) for k, i in iy.items()},
            "threshold": thr, "iterations": M["iterations"], "sim": S, "params": M["params"],
            "gr_t": [_t(d_) for d_ in ds], "gr": [gr[d_] for d_ in ds], "de": [de[d_] for d_ in ds],
            "gr_peak": float(max(gr.values())), "gr_peak_date": max(gr, key=gr.get)}


def compute_interest() -> dict:
    i = _series("A091RC1Q027SBEA")
    g = _series("GDP")
    ds = sorted(d for d in i if d in g)
    v = [100 * i[d] / g[d] for d in ds]
    return {"t": [_t(d) for d in ds], "share": v, "last": v[-1], "last_date": ds[-1], "peak_80s": float(max(
        v[k] for k, d in enumerate(ds) if "1980" <= d < "2000")), "min": float(min(v)), "level_last": i[ds[-1]]}


MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1889.0, last: float = 2026.6) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    D = compute_debt()
    t = np.array(D["t"])
    return {"t": D["t"], "debt": D["debt"], "times": [film_time(x) for x in t]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    vals = np.array(f["debt"])
    times = [film_time(x) for x in t]
    mel = score.data_melody(vals - vals.min() + 1.0, MELODY_SECONDS, times=times, act=6, log=False, low=40,
                            high=86)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "US federal debt held by the public as a share of GDP, quarter by quarter, 1889-2026 "
                               "(Ramey and Zubairy; OMB via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ32").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "hap": compute_hap,
    "debt": compute_debt,
    "budget": compute_budget,
    "playit": compute_playit,
    "nk": compute_nk,
    "rz": compute_rz,
    "regions": compute_regions,
    "bl": compute_bl,
    "taxes": compute_taxes,
    "stabilizers": compute_stabilizers,
    "rg": compute_rg,
    "war": compute_war,
    "unpleasant": compute_unpleasant,
    "default": compute_default,
    "interest": compute_interest,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
