"""Every number in Part 13 of *Industry, Built* ("Electricity"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry13.compute        # prints the film's numbers; writes .cache/industry13/computed.json

Items:
    hook        Insull's Chicago block of 1910: load factor alone and together
    run         the Run it game: a gas plant through a week with a cold snap, hedged or not, frozen or not (the Works);
                Vistra's 2021
    physics     ERCOT's hourly demand in 2025 (EIA-930): its peak and quietest days, the load duration curve, the load
                factor and the capacity needed for the last few hours
    plants      the screening curve from EIA's AEO2026 costs; capacity factors by technology in 2025 (EIA)
    dispatch    ERCOT's hour-by-hour generation on its peak day of 2025; ERCOT's average prices against gas (IMM)
    utility     the Works' revenue requirement; Duke Energy's rate cases; the price of a kWh in three pieces (AEO2021)
    texas       February 2021 in ERCOT, hour by hour (EIA-930): forecast, served load and generation by source; the FERC-NERC
                report; the market monitor; Vistra
    history     US electricity sales since 1949 (EIA, Monthly Energy Review) and growth by decade; the real price (BLS)
    sun         California's net load on April days in 2019 and 2026 (EIA-930); CAISO's capacity (EIA)
    storage     the storage signature in California's April 2026 data; the Works' battery
    retail      Britain's suppliers (NAO); the Works' retailer through 2021's gas prices
    world       electricity by country since 2000 (Ember via Our World in Data)
    demand      US sales growth year by year and 2026 to date; data centers (DOE/LBNL)
    landscape   the listed power companies by group
    called      AEO2005's 2025 against the Monthly Energy Review; this series' call on 2027
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import power

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry13"
FUELS = ("nuclear", "coal", "gas", "hydro", "wind", "solar", "oil", "other")


def _monthly(rows):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r["series"]][str(r["month"])] = r["value"]
    return d


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        if v is not None:
            by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    G = collections.defaultdict(list)
    for r in read("eia_930"):
        G[r["ba"]].append(r)
    for k in G:
        G[k].sort(key=lambda r: (r["date"], int(r["hour"])))

    # --- hook ---------------------------------------------------------------------------------------------------------
    kwh, peaks, peak = get("insull.kwh"), get("insull.peaks"), get("insull.peak")
    rng = np.random.default_rng(1910)
    hours = np.arange(24)
    homes = []
    for _ in range(12):           # an illustration of 12 of the block's households: each lights up at its own hour
        on = int(rng.integers(17, 23))
        h = np.where((hours >= on) & (hours < on + int(rng.integers(2, 4))), 1.0, 0.05)
        homes.append(h * float(rng.uniform(0.25, 0.45)))
    R["hook"] = dict(kwh=kwh, peaks=peaks, peak=peak, lf_alone=kwh / (peaks * 8760), lf_together=kwh / (peak * 8760),
                     apartments=get("insull.apartments"), customers=get("insull.customers"), turn=get("insull.turn"),
                     homes=[list(h) for h in homes], diversity=peaks / peak)

    # --- Run it ---------------------------------------------------------------------------------------------------------
    prices = power.week_prices()
    games = power.run_it(prices)
    R["run"] = dict(prices=list(prices), games={k: dict(total=v["total"], cum=list(v["cum"])) for k, v in games.items()},
                    vst=get("vst.uri"), mw=power.GasPlantWeek().mw, cost=power.GasPlantWeek().cost,
                    snap_cost=power.GasPlantWeek().snap_cost, forward=power.GasPlantWeek().forward)

    # --- physics: ERCOT 2025 ----------------------------------------------------------------------------------------------
    e25 = [r for r in G["ERCO"] if r["date"].startswith("2025") and r["demand"]]
    dem = np.array([r["demand"] for r in e25], dtype=float)
    by_day: dict = collections.defaultdict(list)
    for r in e25:
        by_day[r["date"]].append(r["demand"])
    full = {d: v for d, v in by_day.items() if len(v) >= 23}
    peak_day = max(full, key=lambda d: max(full[d]))
    low_day = min(full, key=lambda d: max(full[d]))
    srt = np.sort(dem)[::-1]
    pk = srt[0]
    top = {p: int((dem > (1 - p) * pk).sum()) for p in (0.05, 0.10, 0.20)}
    R["physics"] = dict(load_factor=power.load_factor(dem), peak=float(pk), mean=float(dem.mean()), low=float(srt[-1]),
                        peak_day=peak_day, low_day=low_day, peak_curve=full[peak_day], low_curve=full[low_day],
                        duration=[float(x) for x in srt[::8]], hours=len(dem), top=top,
                        peak_hour=int(np.argmax(full[peak_day])) + 1, nine=get("nerc.minutes"))

    # --- plants ----------------------------------------------------------------------------------------------------------
    rows = read("eia_power")

    def table(t, year=2025):
        return [r["value"] for r in rows if r["table"] == t and str(r["row"]).startswith(str(year))]
    a, b = table("epa_04_08_a"), table("epa_04_08_b")
    names_a = ["coal", "gas_cc", "gas_ct", "gas_steam", "gas_ic", "oil_steam", "oil_ct", "oil_ic"]
    names_b = ["geothermal", "hydro", "nuclear", "biomass", "other_gas", "solar", "solar_thermal", "wind", "wood"]
    cf = {}
    for names, vals in ((names_a, a), (names_b, b)):
        for k, nm in enumerate(names):
            cf[nm] = dict(gw=vals[2 * k] / 1e3, cf=vals[2 * k + 1])
    fuel = [r["value"] for r in rows if r["table"] == "epa_07_04" and str(r["row"]).startswith("2025")
            and "Average Cost" in r["column"]]
    gas_price = fuel[5]
    techs = {}
    for key, name in (("ct_frame", "gas peaker"), ("cc2", "combined-cycle gas"), ("nuclear", "nuclear"), ("solar", "solar"),
                      ("wind", "wind")):
        t = power.Tech(name, get(f"plant.{key}.overnight"), get(f"plant.{key}.fom"), get(f"plant.{key}.vom"),
                       get(f"plant.{key}.heat"), fuel=gas_price if key in ("ct_frame", "cc2") else (0.7 if key == "nuclear" else 0.0),
                       life=40 if key == "nuclear" else 30)
        techs[key] = dict(name=name, fixed=t.fixed(), running=t.running(), overnight=t.overnight,
                          curve=[t.per_kw_year(x / 100) for x in range(0, 101, 5)])
    R["plants"] = dict(cf=cf, gas_price=gas_price, techs=techs, rate=0.07,
                       cross_cc_nuke=power.crossover(power.Tech("cc", get("plant.cc2.overnight"), get("plant.cc2.fom"),
                                                                get("plant.cc2.vom"), get("plant.cc2.heat"), fuel=gas_price),
                                                     power.Tech("n", get("plant.nuclear.overnight"), get("plant.nuclear.fom"),
                                                                get("plant.nuclear.vom"), get("plant.nuclear.heat"), fuel=0.7,
                                                                life=40)))

    # --- dispatch ---------------------------------------------------------------------------------------------------------
    day = [r for r in G["ERCO"] if r["date"] == peak_day]
    mix = {f: [max(r[f] or 0.0, 0.0) for r in day] for f in FUELS}
    pr = {y: get(f"imm.price.{y}") for y in range(2014, 2025)}
    gp = {y: get(f"imm.gas.{y}") for y in range(2014, 2022)}
    R["dispatch"] = dict(day=peak_day, mix=mix, demand=[r["demand"] for r in day], prices=pr, gas=gp,
                         price21x=get("imm.price.2021x"), total=[sum(mix[f][h] for f in FUELS) for h in range(len(day))])

    # --- utility ---------------------------------------------------------------------------------------------------------
    u = power.Utility(rate_base=30000)
    cases = [(k, get(f"duke.{k}.rev"), get(f"duke.{k}.roe")) for k in ("dec_nc_2023", "dep_nc_2022", "dei_2024", "def_2024",
                                                                       "dec_sc_2024", "dek_2024", "dek_2022", "dep_sc_2025",
                                                                       "dep_sc_2022", "dec_sc_2025", "deo_2021")]
    pending = [(k, get(f"duke.{k}.rev"), get(f"duke.{k}.roe")) for k in ("dec_nc_2025", "dep_nc_2025")]
    split = {"generation": get("aeo21.gen"), "transmission": get("aeo21.trans"), "distribution": get("aeo21.dist")}
    R["utility"] = dict(req=u.requirement(), wacc=u.wacc(), roe=u.roe, equity=u.equity, rate_base=u.rate_base,
                        sales=u.sales, cases=cases, pending=pending, split=split, total_c=sum(split.values()),
                        roe_hi=power.Utility(rate_base=30000, roe=u.roe + 0.01).requirement())

    # --- Texas, February 2021 ---------------------------------------------------------------------------------------------
    feb = [r for r in G["ERCO"] if r["date"].startswith("2021-02")]
    t = [i / 24 + 1 for i in range(len(feb))]       # days since 1 Feb (hour ending)
    gap = [(r["forecast"] or 0) - (r["demand"] or 0) for r in feb]
    i_gap = int(np.argmax(gap))
    R["texas"] = dict(t=t, forecast=[r["forecast"] for r in feb], demand=[r["demand"] for r in feb],
                      mix={f: [max(r[f] or 0.0, 0.0) for r in feb] for f in FUELS},
                      gap_max=gap[i_gap], gap_when=(feb[i_gap]["date"], int(feb[i_gap]["hour"])),
                      people=get("nerc.people"), deaths=get("nerc.deaths"), shed=get("nerc.shed"),
                      unavail=get("nerc.ercot_unavail"), winter_peak=get("nerc.winter_peak"), units=get("nerc.units"),
                      freezing=get("nerc.freezing"), fuel=get("nerc.fuel"), voll=get("imm.voll"), value=get("imm.value"),
                      price21=get("imm.price.2021"), price20=get("imm.price.2020"), vst=get("vst.uri"),
                      gas_units=get("nerc.gas_share"))
    pre = [r for r in feb if "2021-02-08" <= r["date"] <= "2021-02-10"]
    low = [r for r in feb if "2021-02-15" <= r["date"] <= "2021-02-17"]
    R["texas"]["fall"] = {f: (float(np.mean([r[f] or 0 for r in pre])), float(np.mean([r[f] or 0 for r in low])))
                          for f in ("gas", "coal", "nuclear", "wind")}

    # --- history: US sales since 1949 --------------------------------------------------------------------------------------
    mer: dict = collections.defaultdict(dict)
    for r in read("eia_mer"):
        mer[r["msn"]][(int(r["year"]), int(r["month"]))] = r["value"]
    sales = {y: v / 1e3 for (y, m), v in mer["ESTCPUS"].items() if m == 13}      # billion kWh
    end_use = {y: v / 1e3 for (y, m), v in mer["ELTCPUS"].items() if m == 13}
    dec = {}
    for y0 in (1950, 1960, 1970, 1980, 1990, 2000, 2010):
        y1 = min(y0 + 10, max(sales))
        dec[y0] = 100 * ((sales[y1] / sales[y0]) ** (1 / (y1 - y0)) - 1)
    F = _monthly(read("fred_power"))
    kwh = _annual(F["APU000072610"])
    cpi = _annual(F["CPIAUCSL"])
    real = {y: kwh[y] * cpi[max(cpi)] / cpi[y] for y in kwh if y in cpi}
    R["history"] = dict(sales=sales, end_use=end_use, decades=dec, kwh=kwh, real=real, last=max(sales))

    # --- sun and storage: California ---------------------------------------------------------------------------------------
    def avg_day(rows_, key):
        by: dict = collections.defaultdict(list)
        for r in rows_:
            v = r[key]
            if v is not None:
                by[int(r["hour"])].append(v)
        return [float(np.mean(by[h])) for h in range(1, 25)]
    c19 = [r for r in G["CISO"] if r["date"].startswith("2019-04")]
    c26 = [r for r in G["CISO"] if r["date"].startswith("2026-04")]
    sun = {}
    for y, rows_ in ((2019, c19), (2026, c26)):
        d_, s_, w_ = avg_day(rows_, "demand"), avg_day(rows_, "solar"), avg_day(rows_, "wind")
        sun[y] = dict(demand=d_, solar=s_, wind=w_, net=[a_ - b_ - c_ for a_, b_, c_ in zip(d_, s_, w_)],
                      other=avg_day(rows_, "other"), gas=avg_day(rows_, "gas"))
    day15 = [r for r in c26 if r["date"] == "2026-04-15"]
    R["sun"] = dict(days=sun, solar_cap=get("caiso.solar.cap"), battery_cap=get("caiso.battery.cap"),
                    gas_cap=get("caiso.gas.cap"), solar_days=get("caiso.solar_days"), battery_x=get("caiso.battery_x"),
                    ercot_solar=get("imm.solar.2024"), ercot_storage=get("imm.storage.2024"))
    R["storage"] = dict(day=[dict(hour=int(r["hour"]), other=r["other"], solar=r["solar"], demand=r["demand"], gas=r["gas"])
                             for r in day15],
                        min_other=min(r["other"] for r in day15), max_other=max(r["other"] for r in day15))
    shape = [30, 28, 27, 27, 28, 32, 38, 35, 20, 8, 2, -3, -5, -4, 0, 10, 30, 70, 140, 120, 80, 55, 42, 35]
    bat = power.battery(shape, mw=100, hours=4, efficiency=0.85)
    R["storage"]["works"] = dict(prices=shape, profit=bat["profit"], charge=bat["charge"], discharge=bat["discharge"])

    # --- retail: Britain --------------------------------------------------------------------------------------------------
    eu_gas = {m: v for m, v in F["PNGASEUUSDM"].items() if "2020-07" <= m <= "2022-12"}
    ms = sorted(eu_gas)
    whole = [eu_gas[m] * 7.0 + 15 for m in ms]            # $/MWh: a gas plant's fuel at 7 MMBtu/MWh plus $15
    fixed = whole[0] * 1.15 + 20                           # the supplier's fixed price, set when gas was cheap
    unh = power.retailer(whole, fixed, hedge=0.0, hedge_price=whole[0])
    hed = power.retailer(whole, fixed, hedge=0.9, hedge_price=whole[0] * 1.05)
    R["retail"] = dict(months=ms, wholesale=whole, fixed=fixed, unhedged=unh["margin"], hedged=hed["margin"],
                       failed=get("nao.failed"), s2010=get("nao.suppliers.2010"), speak=get("nao.suppliers.peak"),
                       s2022=get("nao.suppliers.2022"), cap18=get("nao.cap.2018"), cap22=get("nao.cap.2022"),
                       gas_x=get("nao.gas_x"), cost=get("nao.cost"), per=get("nao.per_customer"), bulb=get("nao.bulb"),
                       new_share=get("nao.new_share"))

    # --- world ----------------------------------------------------------------------------------------------------------
    O: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("owid_elec"):
        O[r["series"]][r["entity"]][int(r["year"])] = r["value"]
    gen = O["electricity-generation"]
    R["world"] = dict(gen={k: dict(v) for k, v in gen.items()}, per={k: dict(v) for k, v in O["per-capita-electricity-generation"].items()},
                      solar={k: dict(v) for k, v in O["share-electricity-solar"].items()},
                      wind={k: dict(v) for k, v in O["share-electricity-wind"].items()},
                      coal={k: dict(v) for k, v in O["share-electricity-coal"].items()})

    # --- demand -----------------------------------------------------------------------------------------------------------
    monthly = {k: v for k, v in mer["ESTCPUS"].items() if k[1] != 13}
    last = max(monthly)
    n = last[1]
    ytd = sum(monthly[(last[0], m)] for m in range(1, n + 1)) / sum(monthly[(last[0] - 1, m)] for m in range(1, n + 1)) - 1
    growth = {y: 100 * (sales[y] / sales[y - 1] - 1) for y in sales if y - 1 in sales and y >= 2000}
    R["demand"] = dict(growth=growth, ytd=100 * ytd, ytd_months=n, ytd_year=last[0], dc14=get("dc.twh.2014"),
                       dc23=get("dc.twh.2023"), dc28=get("dc.twh.2028"), dc28_lo=325, dc28_hi=580, dc_share=get("dc.share.2023"),
                       ev=mer["ESVHPUS"].get((2025, 13), 0) / 1e3)

    # --- landscape ----------------------------------------------------------------------------------------------------------
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_annual"):
        sec[r["ticker"]][int(str(r["year_end"])[:4])] = r

    def comp(tk, upto=2025):
        d = sec.get(tk, {})
        ys = [y for y in d if y <= upto and d[y]["revenue"] and d[y]["net_income"] is not None]
        if not ys:
            return None
        y = max(ys)
        m5 = [d[k]["net_income"] / d[k]["revenue"] for k in range(y - 4, y + 1)
              if k in d and d[k]["revenue"] and d[k]["net_income"] is not None]
        return dict(ticker=tk, year=y, revenue=d[y]["revenue"], net=d[y]["net_income"], margin5=float(np.mean(m5)),
                    capex=d[y].get("capex"), assets=d[y].get("assets"))
    groups = {"regulated utilities": ("NEE", "DUK", "SO", "AEP", "D", "EXC", "XEL", "ED", "PCG", "SRE", "ETR"),
              "generators": ("VST", "CEG", "NRG", "AES"), "equipment": ("GEV",)}
    land = []
    for g, ts in groups.items():
        for tk in ts:
            c = comp(tk)
            if c:
                c["group"] = g
                land.append(c)
    R["landscape"] = dict(companies=land)

    # --- called it? ---------------------------------------------------------------------------------------------------------
    R["called"] = dict(proj=get("aeo05.elec.2025"), base=get("aeo05.elec.2003"), actual=end_use[2025], actual2003=end_use[2003],
                       growth_proj=100 * ((get("aeo05.elec.2025") / get("aeo05.elec.2003")) ** (1 / 22) - 1),
                       growth_actual=100 * ((end_use[2025] / end_use[2003]) ** (1 / 22) - 1),
                       ytd=100 * ytd, threshold=1.5, prob=0.65, g25=growth.get(2025), g24=growth.get(2024))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    h = R["hook"]
    print(f"Insull: LF alone {100 * h['lf_alone']:.1f}%, together {100 * h['lf_together']:.1f}%, diversity {h['diversity']:.2f}")
    print("run:", {k: round(v["total"], 1) for k, v in R["run"]["games"].items()})
    p = R["physics"]
    print(f"ERCOT 2025: LF {p['load_factor']:.3f}, peak {p['peak']:.0f} on {p['peak_day']} (hour {p['peak_hour']}), mean {p['mean']:.0f}, "
          f"low {p['low']:.0f}; quiet day {p['low_day']}; hours above 95/90/80% of peak {p['top']}")
    pl = R["plants"]
    print("plants:", {k: (round(v["fixed"]), round(v["running"], 1)) for k, v in pl["techs"].items()}, "gas", pl["gas_price"],
          "cf", {k: v["cf"] for k, v in pl["cf"].items() if k in ("nuclear", "coal", "gas_cc", "gas_ct", "wind", "solar", "hydro")})
    d = R["dispatch"]
    print("dispatch", d["day"], {f: round(max(v)) for f, v in d["mix"].items()})
    u = R["utility"]
    print("utility", {k: round(v, 1) for k, v in u["req"].items()}, "wacc", u["wacc"], "split", u["split"])
    t = R["texas"]
    print("texas gap", round(t["gap_max"]), t["gap_when"], {k: (round(a), round(b)) for k, (a, b) in t["fall"].items()})
    hi = R["history"]
    print("history", {y: round(v) for y, v in hi["sales"].items() if y % 10 == 0 or y >= 2023}, {k: round(v, 1) for k, v in hi["decades"].items()})
    print("real kWh", {y: round(v, 3) for y, v in hi["real"].items() if y % 5 == 0 or y >= 2024})
    s = R["sun"]["days"]
    print("CISO net load min 2019/2026", round(min(s[2019]["net"])), round(min(s[2026]["net"])), "max", round(max(s[2019]["net"])),
          round(max(s[2026]["net"])))
    st = R["storage"]
    print("storage other min/max", st["min_other"], st["max_other"], "works profit", round(st["works"]["profit"]))
    rt = R["retail"]
    print("retail fixed", round(rt["fixed"]), "wholesale max", round(max(rt["wholesale"])), "unhedged min", round(min(rt["unhedged"])))
    w = R["world"]["gen"]
    print("world gen", {k: (round(v.get(2000, 0)), round(v.get(2025, 0))) for k, v in w.items()})
    dm = R["demand"]
    print("demand growth", {y: round(v, 1) for y, v in dm["growth"].items() if y >= 2019}, "ytd", round(dm["ytd"], 2), dm["ytd_months"])
    print("landscape", [(c["ticker"], round(c["revenue"], 1), round(100 * c["margin5"], 1)) for c in R["landscape"]["companies"]])
    print("called", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in R["called"].items()})


if __name__ == "__main__":
    main()
