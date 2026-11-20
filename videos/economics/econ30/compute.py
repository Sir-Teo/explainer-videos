"""Precompute every number in Part 30 of *Economics, Built* ("Sticky Prices").

    python -m videos.economics.econ30.compute            # everything missing (half a minute)
    python -m videos.economics.econ30.compute --force zlb

Results are cached in ``.cache/econ30/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's federal funds rate, the GDP deflator, real GDP and the CBO's potential, core PCE
prices, and the Atlanta Fed's sticky-price and flexible-price CPIs).  Models: Agora's sticky prices
(``agora.nk``) with the Island's Part 30 truths.

Items:
    sticky       the Atlanta Fed's sticky- and flexible-price inflation, monthly, 1968-2026, and their volatility
    menu         Mankiw's arithmetic: profit lost against output lost, for price gaps of 1% to 10%
    calvo        Calvo's theta: durations, monthly frequencies and the slope kappa, for several thetas
    taylor       the Taylor rule against the federal funds rate, 1987-2005 and since; the fitted coefficients
    determinacy  the Taylor principle: unique equilibria on a grid of (phi_pi, phi_x)
    irfs         the three-equation model's responses to monetary, demand and cost-push shocks
    coincidence  a demand shock under strict inflation targeting, and a cost-push shock
    optimal      a cost-push shock under discretion and commitment
    setters      20,000 price setters: Calvo against menu costs after a 5% rise in money
    zlb          a six-quarter trap; forward guidance; the forward-guidance puzzle
    hybrid       habits, indexation and smoothing: the hump
    film         the intermission's data film: sticky- and flexible-price inflation, month by month
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import nk

CACHE = Cache("econ30")
load = CACHE.load
TRUTH = island.truths(30)
NK = {k: v for k, v in TRUTH["nk"].items() if k in ("beta", "sigma", "phi", "alpha", "eps", "theta", "phi_pi",
                                                     "phi_x")}


def _monthly(key: str) -> dict:
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12


def compute_sticky() -> dict:
    s, f = _monthly("CORESTICKM159SFRBATL"), _monthly("COREFLEXCPIM159SFRBATL")
    ds = sorted(d for d in s if d in f)
    sv, fv = np.array([s[d] for d in ds]), np.array([f[d] for d in ds])
    k = [i for i, d in enumerate(ds) if "1985-01-01" <= d <= "2019-12-01"]
    return {"t": [_t(d) for d in ds], "sticky": sv.tolist(), "flex": fv.tolist(), "sd_sticky": float(sv[k].std()),
            "sd_flex": float(fv[k].std()), "first": ds[0], "last": ds[-1],
            "max_flex": float(fv.max()), "min_flex": float(fv.min()),
            "peak_sticky_2022": float(max(s[d] for d in ds if d >= "2021-01-01")),
            "peak_flex_2022": float(max(f[d] for d in ds if d >= "2021-01-01"))}


def compute_menu() -> dict:
    m = TRUTH["menu"]
    return nk.menu_cost(m["eps"], m["gaps"])


def compute_calvo() -> dict:
    p = TRUTH["nk"]
    rows = []
    for th in p["thetas"]:
        d = nk.calvo_durations(th)
        rows.append({"theta": th, "kappa": nk.kappa(th, p["beta"], p["sigma"], p["phi"], p["alpha"], p["eps"]),
                     "kappa_no_alpha": nk.kappa(th, p["beta"], p["sigma"], p["phi"], 0.0, p["eps"]), **d})
    base = nk.calvo_durations(p["theta"])
    return {"rows": rows, "base": {**base, "kappa": nk.kappa(p["theta"], p["beta"], p["sigma"], p["phi"], p["alpha"],
                                                              p["eps"])},
            "theta_bk": nk.theta_from_monthly(1 - np.exp(-1 / 4.3)),
            "theta_ns": nk.theta_from_monthly(0.105)}


def _quarterly_ff() -> dict:
    d = data.fred("FEDFUNDS")
    out: dict = {}
    for x, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            q = f"{x[:4]}-{3 * ((int(x[5:7]) - 1) // 3) + 1:02d}-01"
            out.setdefault(q, []).append(v)
    return {k: float(np.mean(v)) for k, v in out.items() if len(v) == 3}


def compute_taylor() -> dict:
    D, Y, P = _monthly("GDPDEF"), _monthly("GDPC1"), _monthly("GDPPOT")
    ff = _quarterly_ff()
    rows = []
    for d in sorted(D):
        prev = f"{int(d[:4]) - 1}{d[4:]}"
        if prev in D and d in Y and d in P and d in ff:
            pi = 100 * (D[d] / D[prev] - 1)
            gap = 100 * (Y[d] / P[d] - 1)
            rows.append((d, pi, gap, ff[d]))
    t = np.array([_t(r[0]) for r in rows])
    pi = np.array([r[1] for r in rows])
    gap = np.array([r[2] for r in rows])
    i = np.array([r[3] for r in rows])
    rule = 2 + pi + 0.5 * (pi - 2) + 0.5 * gap
    g = (t >= 1987.5) & (t < 2006.0)
    X = np.column_stack([np.ones(g.sum()), pi[g], gap[g]])
    b, *_ = np.linalg.lstsq(X, i[g], rcond=None)
    rmse = float(np.sqrt(np.mean((rule[g] - i[g]) ** 2)))
    late = (t >= 2009) & (t < 2016)
    return {"t": t.tolist(), "ff": i.tolist(), "rule": rule.tolist(), "pi": pi.tolist(), "gap": gap.tolist(),
            "fit": {"const": float(b[0]), "pi": float(b[1]), "gap": float(b[2])}, "rmse": rmse,
            "corr": float(np.corrcoef(rule[g], i[g])[0, 1]), "rule_2009": float(rule[late].min()),
            "ff_2009": float(i[late].min()), "first": rows[0][0], "last": rows[-1][0]}


def compute_determinacy() -> dict:
    p = TRUTH["nk"]
    kap = nk.kappa(p["theta"], p["beta"], p["sigma"], p["phi"], p["alpha"], p["eps"])
    fps = np.round(np.arange(0.0, 3.01, 0.05), 3)
    fxs = np.round(np.arange(0.0, 1.01, 0.025), 3)
    grid = [[int(nk.determinacy(fp, fx, p["beta"], p["sigma"], kap)["unique"]) for fp in fps] for fx in fxs]
    # the boundary: phi_pi = 1 - (1 - beta) phi_x / kappa
    bound = [float(1 - (1 - p["beta"]) * fx / kap) for fx in fxs]
    return {"phi_pi": fps.tolist(), "phi_x": fxs.tolist(), "unique": grid, "boundary": bound, "kappa": kap,
            "examples": {k: nk.determinacy(a, b, p["beta"], p["sigma"], kap)["moduli"] for k, (a, b) in
                         {"taylor": (1.5, 0.125), "passive": (0.8, 0.125)}.items()}}


def compute_irfs() -> dict:
    p = TRUTH["nk"]
    out = {}
    for s in ("monetary", "demand", "cost"):
        out[s] = nk.irf_ar1(s, rho_s=p["rho_shock"], size=p["size"], periods=12, **NK)
    return out


def compute_coincidence() -> dict:
    """Strict inflation targeting (a very large phi_pi) after a demand shock and after a cost-push shock."""
    p = TRUTH["nk"]
    strict = {**NK, "phi_pi": 1000.0, "phi_x": 0.0}
    return {"demand": nk.irf_ar1("demand", rho_s=p["rho_shock"], size=p["size"], periods=12, **strict),
            "cost": nk.irf_ar1("cost", rho_s=p["rho_shock"], size=p["size"], periods=12, **strict),
            "demand_taylor": nk.irf_ar1("demand", rho_s=p["rho_shock"], size=p["size"], periods=12, **NK)}


def compute_optimal() -> dict:
    p = TRUTH["nk"]
    return nk.optimal_policy(rho_u=p["rho_shock"], size=p["size"], periods=12, **NK)


def compute_setters() -> dict:
    s = TRUTH["setters"]
    c = nk.price_setters("calvo", n=s["n"], months=s["months"], freq=s["freq"], shock=s["shock"],
                         sigma_a=s["sigma_a"], seed=s["seed"])
    m = nk.price_setters("menu", n=s["n"], months=s["months"], freq=s["freq"], shock=s["shock"],
                         sigma_a=s["sigma_a"], seed=s["seed"])
    # output (real money balances) lost: the shock not yet passed through, summed over months, in percent-months
    real_c = float(np.sum(1 - np.array(c["pass_through"])) * 100 * s["shock"])
    real_m = float(np.sum(1 - np.array(m["pass_through"])) * 100 * s["shock"])
    return {"calvo": c, "menu": m, "real_calvo": real_c, "real_menu": real_m, "band": m["band"],
            "half_calvo": int(np.argmax(np.array(c["pass_through"]) >= 0.5)) + 1,
            "half_menu": int(np.argmax(np.array(m["pass_through"]) >= 0.5)) + 1}


def compute_zlb() -> dict:
    z = TRUTH["zlb"]
    paths = {str(e): nk.zlb(T=z["T"], rn_low=z["rn_low"], extra=e, periods=12, **NK) for e in z["extras"]}
    fg = nk.forward_guidance_puzzle(horizons=z["fg_horizons"], cut=1.0, **NK)
    return {"paths": paths, "fg": fg, "T": z["T"], "rn_low": z["rn_low"]}


def compute_hybrid() -> dict:
    h = TRUTH["hybrid"]
    p = TRUTH["nk"]
    base = nk.hybrid_irf(rho_v=p["rho_shock"], size=p["size"], periods=16, **NK)
    rich = nk.hybrid_irf(habit=h["habit"], index=h["index"], smooth=h["smooth"], rho_v=p["rho_shock"],
                         size=p["size"], periods=16, **NK)
    only_h = nk.hybrid_irf(habit=h["habit"], rho_v=p["rho_shock"], size=p["size"], periods=16, **NK)
    only_s = nk.hybrid_irf(smooth=h["smooth"], rho_v=p["rho_shock"], size=p["size"], periods=16, **NK)
    return {"base": base, "rich": rich, "habit": only_h, "smooth": only_s}


FILM_SECONDS = 40.0
def compute_called() -> dict:
    """Bernanke's 2002 promise checked: consumer prices and core PCE prices, change over twelve months, 2006-2019."""
    out = {}
    for key, name in (("CPIAUCSL", "cpi"), ("PCEPILFE", "core")):
        m = _monthly(key)
        ds = [d for d in sorted(m) if "2006-01-01" <= d <= "2019-12-01" and f"{int(d[:4]) - 1}{d[4:]}" in m]
        out[name] = {"t": [_t(d) for d in ds],
                     "yoy": [100 * (m[d] / m[f"{int(d[:4]) - 1}{d[4:]}"] - 1) for d in ds]}
    neg = [t for t, v in zip(out["cpi"]["t"], out["cpi"]["yoy"]) if v < 0]
    return {**out, "cpi_min": float(min(out["cpi"]["yoy"])), "core_min": float(min(out["core"]["yoy"])),
            "cpi_negative_months": len(neg)}


MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1968.0, last: float = 2026.9) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    s = compute_sticky()
    return {"t": s["t"], "sticky": s["sticky"], "flex": s["flex"], "times": [film_time(x) for x in s["t"]]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    vals = np.array(f["flex"])
    times = [film_time(x) for x in t]
    mel = score.data_melody(vals - vals.min() + 1.0, MELODY_SECONDS, times=times, act=6, log=False, low=40,
                            high=86)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the Atlanta Fed's flexible-price CPI less food and energy, change over twelve "
                               "months, month by month, 1968-2026 (via FRED), as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ30").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "sticky": compute_sticky,
    "menu": compute_menu,
    "calvo": compute_calvo,
    "taylor": compute_taylor,
    "determinacy": compute_determinacy,
    "irfs": compute_irfs,
    "coincidence": compute_coincidence,
    "optimal": compute_optimal,
    "setters": compute_setters,
    "zlb": compute_zlb,
    "hybrid": compute_hybrid,
    "called": compute_called,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
