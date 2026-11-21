"""Precompute every number in Part 48 of *Economics, Built* ("Environment and Climate").

    python -m videos.economics.econ48.compute            # everything missing (about a minute)
    python -m videos.economics.econ48.compute --force dice

Results are cached in ``.cache/econ48/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Data: the Data Room
(``explainer.economics.data``: the World Bank's Pink Sheet metal and oil prices with the US CPI from FRED; NOAA's Mauna
Loa CO2; HadCRUT5; the Global Carbon Budget's emissions and CEDS sulphur dioxide via Our World in Data; ERA5 country
temperatures via Our World in Data with the World Bank's GDP per head; IRENA's solar prices and capacity and FAO's fish
stocks via Our World in Data; oil production via Our World in Data; the tables of Part 48). Models: Agora's climate
(``agora.climate``) with the Island's Part 48 truths.

Items:
    metals      real prices of copper, nickel and tin (and oil), 1960-2025, indexed; the 1980-1990 bundle
    bet         Simon and Ehrlich's bet rerun for every ten-year window from 1960
    hotelling   Hotelling's price path with a constant and with a falling extraction cost
    fishery     the sustainable-yield curve, open access against a quota, and the fleet's dynamics
    fao         the share of the world's assessed fish stocks overexploited, 1974-2021
    climate     the climate model fitted to Mauna Loa and HadCRUT5: parameters and fitted series
    dice        the DICE-style model: business as usual, the optimal path, a near-zero-discount path
    scc         the social cost of carbon by discount rate and by (rho, eta); the damage path for the widget
    tails       fat tails: certainty-equivalent losses as the warming is truncated higher
    club        the climate club: members and abatement against the penalty tariff
    solar       solar module prices and installed capacity; Wright's law
    dtc         directed technical change: four policies
    panel       temperature and growth across 181 countries, 1961-2023 (ERA5, World Bank)
    power       the Island's merit order, a day of prices, and withholding at the peak
    oil         US and world oil production, 1900-2025 (Hubbert's call)
    film        the intermission's data film: HadCRUT5's warming, 1850-2025, as stripes
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import climate as cl

CACHE = Cache("econ48")
load = CACHE.load
TRUTH = island.truths(48)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0
METALS = ("copper", "nickel", "tin")
RHO_N, ETA_N = 0.015, 1.45        # a modest pure rate of time preference and inequality aversion
RHO_S, ETA_S = 0.001, 1.0         # the Stern Review's 0.1% and logarithmic utility


def _annual(d: dict, key: str = "month") -> dict:
    out: dict = {}
    for m, v in zip(d[key], d["value"]):
        if np.isfinite(v):
            out.setdefault(int(m[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items() if len(v) == 12}


def _metals():
    cpi = _annual(data.fred("CPIAUCNS"), "date")
    series = {k: _annual(data.pinksheet(k)) for k in (*METALS, "oil")}
    years = sorted(set(cpi).intersection(*[set(v) for v in series.values()]))
    return years, cpi, series


def compute_metals() -> dict:
    years, cpi, s = _metals()
    real = {k: [s[k][y] / cpi[y] for y in years] for k in s}
    idx = {k: (100 * np.array(v) / v[0]).tolist() for k, v in real.items()}
    i80, i90 = years.index(1980), years.index(1990)
    change = {k: float(real[k][i90] / real[k][i80] - 1) for k in s}
    bundle = [float(np.mean([real[k][i] / real[k][i80] for k in METALS])) for i in range(len(years))]
    return {"year": years, "index": idx, "change_8090": change, "bundle": bundle,
            "bundle_8090": float(bundle[i90] - 1), "cpi_8090": float(cpi[1990] / cpi[1980] - 1),
            "real_2024_vs_1960": {k: float(real[k][-1] / real[k][0]) for k in s}}


def compute_bet() -> dict:
    years, cpi, s = _metals()
    b = cl.bet_windows(years, {k: [s[k][y] for y in years] for k in METALS}, [cpi[y] for y in years])
    i = b["start"].index(1980)
    return {**b, "bet_1980": b["change"][i], "first": b["start"][0], "last": b["start"][-1]}


def compute_hotelling() -> dict:
    a = cl.hotelling(**TRUTH["mine"])
    b = cl.hotelling(**TRUTH["mine_falling"])
    pb = np.array(b["price"][:b["exhausted"]])
    return {"constant": a, "falling": b, "falling_min_t": int(pb.argmin()), "falling_min": float(pb.min())}


def compute_fishery() -> dict:
    F = TRUTH["fishery"]
    curves = cl.fishery_curves(**F)
    fl = TRUTH["fleet"]
    kw = dict(F, entry=fl["entry"], stock0=fl["stock0"], effort0=fl["effort0"])
    open_ = cl.fishery_dynamics(**kw)
    quota = cl.fishery_dynamics(**kw, quota=fl["quota"])
    s = np.array(open_["stock"])
    return {"curves": curves, "open": open_, "quota": quota, "open_min": float(s.min()),
            "open_min_t": float(open_["t"][int(s.argmin())]), "open_end": float(s[-1]),
            "quota_end": float(quota["stock"][-1]), "quota_level": fl["quota"]}


def compute_fao() -> dict:
    f = data.fish_stocks()
    return {**f, "first": f["overexploited"][0], "last": f["overexploited"][-1], "first_year": f["year"][0],
            "last_year": f["year"][-1]}


def _so2(years):
    s = data.so2("World")
    sy, sv = np.array(s["year"]), np.array(s["value"]) / 1e6
    out = np.interp(years, sy, sv, left=0.0, right=sv[-1])
    early = years < sy[0]
    out[early] = sv[0] * np.clip((years[early] - 1850) / (sy[0] - 1850), 0, None)
    return out


def _fit():
    g = data.gcp_co2()
    years = np.array(g["year"])
    so2 = _so2(years)
    c, h = data.co2_mlo(), data.hadcrut5()
    fit = cl.fit_climate(years, g["fossil"], g["land"], so2, c["year"], c["ppm"], h["year"], h["anomaly"])
    E = np.array(g["fossil"]) + fit["land_weight"] * np.nan_to_num(np.array(g["land"]))
    cc = cl.carbon_cycle(E, fit["speed"])
    T, D = cl.ebm(cl.forcing(cc["ppm"], so2, fit["ghg_scale"], fit["aerosol"]), fit["ecs"])
    pre = (years >= 1850) & (years <= 1900)
    off = T[pre].mean()
    return fit, cc["boxes"], (float(T[-1] - off), float(D[-1] - off)), years, g, so2, c


def compute_climate() -> dict:
    fit, boxes, temps, years, g, so2, c = _fit()
    keep = years >= 1850
    obs_t = np.array(fit["obs_temp"])
    ty = np.array(fit["temp_year"])
    return {"speed": fit["speed"], "land_weight": fit["land_weight"], "ghg_scale": fit["ghg_scale"],
            "aerosol": fit["aerosol"], "ecs": fit["ecs"], "tcr": cl.tcr(fit["ecs"]), "ppm_rmse": fit["ppm_rmse"],
            "temp_rmse": fit["temp_rmse"], "year": years[keep].tolist(),
            "ppm": np.array(fit["ppm"])[keep].tolist(), "temp": np.array(fit["temp"])[keep].tolist(),
            "fossil": np.array(g["fossil"])[keep].tolist(), "land": np.nan_to_num(np.array(g["land"]))[keep].tolist(),
            "so2": so2[keep].tolist(), "obs_year": c["year"], "obs_ppm": c["ppm"], "obs_temp_year": ty.tolist(),
            "obs_temp": obs_t.tolist(), "decade_model": float(np.array(fit["temp"])[years >= 2016].mean()),
            "decade_obs": float(obs_t[ty >= 2016].mean()), "ppm_2025": float(c["ppm"][-1]),
            "fossil_2025": float(g["fossil"][-1]), "cum_fossil": float(np.nansum(g["fossil"])),
            "temps_2025": temps}


def _model():
    fit, boxes, temps, *_ = _fit()
    return cl.Dice(fit, boxes, temps)


def _summ(d, run, every=5):
    yr = np.array(run["year"])
    k = (yr - yr[0]) % every == 0
    price = d.backstop * np.array(run["mu"]) ** (d.p["theta2"] - 1)
    out = {x: np.array(run[x])[k].tolist() for x in ("year", "E", "T", "mu", "ppm", "damage", "abate", "c", "Y")}
    out["price"] = price[k].tolist()
    for y in (2030, 2050, 2100):
        i = int(y - yr[0])
        out[f"T{y}"], out[f"E{y}"] = float(run["T"][i]), float(run["E"][i])
        out[f"mu{y}"], out[f"price{y}"] = float(run["mu"][i]), float(price[i])
        out[f"damage{y}"] = float(run["damage"][i])
    out["peak_T"] = float(np.max(run["T"]))
    out["peak_year"] = int(yr[int(np.argmax(run["T"]))])
    out["zero_year"] = int(yr[int(np.argmax(np.array(run["E"]) < 0.5))]) if np.any(np.array(run["E"]) < 0.5) else None
    return out


def compute_dice() -> dict:
    d = _model()
    base_mu = np.interp(d.year, [2025, 2050, 2100, 2300], [0.05, 0.10, 0.22, 0.22])
    base = d.run(base_mu)
    opt = d.optimize(RHO_N, ETA_N)
    stern = d.optimize(RHO_S, ETA_S)
    w_base = d.welfare(base, RHO_N, ETA_N)
    gain = opt["welfare"] - w_base
    # the welfare gain in today's consumption: dW = u'(c0) dC in the first year, so dollars now = dW / u'(c0)
    c0 = base["c"][0]
    mu0 = c0 ** (-ETA_N)
    return {"base": _summ(d, base), "opt": _summ(d, opt["run"]), "stern": _summ(d, stern["run"]),
            "gain_trillions": float(gain / mu0), "output0": d.p["output0"], "emissions0": float(base["E"][0]),
            "damage_coef": d.p["damage"], "backstop2050": d.p["backstop2050"], "theta2": d.p["theta2"],
            "pop2100": float(d.L[75]), "c_growth": float(np.log(base["c"][75] / base["c"][0]) / 75)}


def compute_scc() -> dict:
    d = _model()
    base_mu = np.interp(d.year, [2025, 2050, 2100, 2300], [0.05, 0.10, 0.22, 0.22])
    rates = (0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06)
    s = d.scc(base_mu, RHO_N, ETA_N, rates=rates)
    stern = d.scc(base_mu, RHO_S, ETA_S)
    opt = d.optimize(RHO_N, ETA_N)
    s_opt = d.scc(opt["mu"], RHO_N, ETA_N)
    by_rate = [s[f"r{r:g}"] for r in rates]
    dC = np.array(s["dC_per_t"])
    c = np.array(s["c"])
    g = np.diff(np.log(c))
    share_after_2100 = float(np.sum(dC[76:] * 1.03 ** -np.arange(76, len(dC))) / s["r0.03"])
    return {"rates": list(rates), "by_rate": by_rate, "ramsey": s["ramsey"], "stern": stern["ramsey"],
            "optimal_path": s_opt["ramsey"], "dC_per_t": [round(x, 4) for x in dC.tolist()],
            "growth": [round(x, 5) for x in g.tolist()], "year": s["year"], "first_growth": float(g[:25].mean()),
            "share_after_2100_at3": share_after_2100, "r_ramsey_n": float(RHO_N + ETA_N * g[:25].mean()),
            "r_ramsey_s": float(RHO_S + ETA_S * g[:25].mean())}


def compute_tails() -> dict:
    t = TRUTH["tails"]
    return cl.tail_losses([5, 6, 7, 8, 10, 12, 15, 20], **t)


def compute_club() -> dict:
    tariffs = np.round(np.arange(0.0, 0.121, 0.005), 3)
    rows = [cl.club(tariff=float(x), **TRUTH["club"]) for x in tariffs]
    first = next((float(x) for x, r in zip(tariffs, rows) if r["members"] > 0), None)
    full = next((float(x) for x, r in zip(tariffs, rows) if r["members"] == TRUTH["club"]["n"]), None)
    return {"tariff": tariffs.tolist(), "members": [r["members"] for r in rows],
            "abatement": [r["abatement"] for r in rows], "first": first, "full": full, "n": TRUTH["club"]["n"]}


def compute_solar() -> dict:
    s = data.solar_pv()
    py, pr = np.array(s["price_year"]), np.array(s["price"])
    cy, cap = np.array(s["cap_year"]), np.array(s["capacity"])
    m, mc = np.isin(py, cy), np.isin(cy, py)
    lc = cl.learning_curve(cap[mc], pr[m])
    return {"price_year": py.tolist(), "price": pr.tolist(), "cap_year": cy.tolist(), "capacity": cap.tolist(),
            "fit_year": py[m].tolist(), "fit": lc["fit"], "b": lc["b"], "se": lc["se"],
            "learning_rate": lc["learning_rate"], "fall_total": float(1 - pr[-1] / pr[0]),
            "doublings": float(np.log2(cap[-1] / cap[0])), "first": float(pr[0]), "last": float(pr[-1]),
            "cap_first": float(cap[0]), "cap_last": float(cap[-1])}


def compute_dtc() -> dict:
    T = TRUTH["dtc"]
    cases = {"laissez-faire": dict(tax=0.0, subsidy=0.0, policy_years=150),
             "a tax alone": dict(tax=0.2, subsidy=0.0, policy_years=40),
             "a tax and a research subsidy": dict(tax=0.2, subsidy=0.5, policy_years=40),
             "a heavy tax alone": dict(tax=0.4, subsidy=0.0, policy_years=40)}
    out = {}
    for k, v in cases.items():
        r = cl.directed_change(**T, **v)
        out[k] = {"share": r["clean_share"], "research": r["research_clean"], **v}
    return {"cases": out, "t": list(range(150))}


def compute_panel() -> dict:
    temp = {(r["code"], r["year"]): r["temp"] for r in data.era5_temperature()}
    w = data.wdi_gdppc_kd()
    first: dict = {}
    for c, d in w.items():
        ys = [y for y in sorted(d["values"]) if y >= 1980]
        if ys:
            first[c] = d["values"][ys[0]]
    med = float(np.median(list(first.values())))
    codes, years, T, G, poor = [], [], [], [], []
    for c, d in w.items():
        v = d["values"]
        for y in sorted(v):
            if y - 1 in v and (c, y) in temp and 1961 <= y <= 2023:
                g = float(np.log(v[y]) - np.log(v[y - 1]))
                if abs(g) < 0.5:
                    codes.append(c)
                    years.append(y)
                    T.append(temp[(c, y)])
                    G.append(g)
                    poor.append(first.get(c, med) < med)
    r = cl.temperature_growth(codes, years, T, G, trends=2, poor=poor)
    mean_t = {}
    for c, t in zip(codes, T):
        mean_t.setdefault(c, []).append(t)
    mt = {c: float(np.mean(v)) for c, v in mean_t.items()}
    hot = float(r["b1"] + 2 * r["b2"] * 25.0)
    cool = float(r["b1"] + 2 * r["b2"] * 5.0)
    # the marginal effect's standard error at 25 C by the delta method is not computed; report the curve
    return {**r, "mean_temps": sorted(mt.values()), "marg25": hot, "marg5": cool,
            "named": {k: mt[k] for k in ("RUS", "CAN", "DEU", "USA", "CHN", "IND", "NGA", "BRA", "IDN", "QAT",
                                          "MLI") if k in mt}}


def compute_power() -> dict:
    P = TRUTH["power"]
    cap, cost, owner = P["capacity"], P["cost"], P["owner"]
    hours = np.arange(24)
    load_gw = 26 + 9 * np.exp(-((hours - 18) / 3.2) ** 2) + 4 * np.exp(-((hours - 9) / 2.5) ** 2) - 4 * np.exp(
        -((hours - 3) / 3.0) ** 2)
    mo = cl.merit_order(cap, cost, load_gw)
    peak = float(load_gw.max())
    wh = cl.withholding(cap, cost, owner, 1, peak, cap_price=P["cap_price"], steps=57)
    held = np.array(wh["held"])
    steps = []
    for p_ in sorted(set(wh["price"])):
        k = int(np.argmax(np.array(wh["price"]) == p_))
        steps.append({"price": p_, "held": float(held[k]), "profit": wh["profit"][k]})
    names = [P["name"][i] for i in mo["order"]]
    return {"name": names, "cum": mo["cum"], "cost": mo["cost"], "hours": hours.tolist(), "load": load_gw.tolist(),
            "price": mo["price"], "peak": peak, "withhold": wh, "steps": steps, "total": float(sum(cap)),
            "cap_price": P["cap_price"],
            "dynamo_cap": float(sum(c for c, o in zip(cap, owner) if o == 1))}


def compute_oil() -> dict:
    us, wd = data.oil_production("United States"), data.oil_production("World")
    y, v = np.array(us["year"]), np.array(us["twh"])
    pre = y < 2000
    peak_y = int(y[pre][np.argmax(v[pre])])
    peak_v = float(v[pre].max())
    low = (y > peak_y) & (y <= 2012)
    low_y = int(y[low][np.argmin(v[low])])
    passed = y[(y > low_y) & (v > peak_v)]
    return {"year": us["year"], "us": us["twh"], "world_year": wd["year"], "world": wd["twh"], "peak_year": peak_y,
            "peak": peak_v, "low_year": low_y, "low": float(v[y == low_y][0]),
            "passed": int(passed[0]) if len(passed) else None, "last": float(v[-1]), "last_year": int(y[-1])}


def film_time(t: float, first: float = 1850.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    h = data.hadcrut5()
    y, a = np.array(h["year"]), np.array(h["anomaly"])
    a = a - a[(y >= 1850) & (y <= 1900)].mean()
    k = int(np.argmax(a))
    return {"t": y.tolist(), "v": a.tolist(), "times": [film_time(t) for t in y], "first": float(a[0]),
            "last": float(a[-1]), "peak": float(a[k]), "peak_t": int(y[k]), "v1950": float(a[y == 1950][0]),
            "v2000": float(a[y == 2000][0]), "decade": float(a[y >= 2016].mean())}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "y1950": film_time(1950),
              "y2000": film_time(2000), "peak": film_time(f["peak_t"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:+.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the world's warming since 1850-1900, 1850-2025 (HadCRUT5), as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ48").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "metals": compute_metals,
    "bet": compute_bet,
    "hotelling": compute_hotelling,
    "fishery": compute_fishery,
    "fao": compute_fao,
    "climate": compute_climate,
    "dice": compute_dice,
    "scc": compute_scc,
    "tails": compute_tails,
    "club": compute_club,
    "solar": compute_solar,
    "dtc": compute_dtc,
    "panel": compute_panel,
    "power": compute_power,
    "oil": compute_oil,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
