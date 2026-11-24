"""Every number in Part 7 of *Industry, Built* ("Sizing a Market"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry7.compute        # prints the film's numbers; writes .cache/industry7/computed.json

Items:
    uber        Uber's 2019 addressable market, the miles behind it, and its revenue since
    wework      WeWork's 2019 "total opportunity" and what followed
    water       three sizes of the US bottled water market, with the population and the volume they imply
    census      the Census Bureau's shipments of US bottled water makers, 2012-2024, and the producer price index
    diffusion   Bass fits to US adoption curves (Our World in Data)
    early       S-curves fitted on each technology's first quarter of adoption, against what happened
    call        this series' call on the Census's next figures
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works.diffusion import early_forecast, fit_bass, peak_year, predict

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry7"
SHOW = ["Radio", "Household refrigerator", "Colour TV", "Microwave", "Cellular phone", "Internet",
        "Smartphone usage", "Social media usage"]


def _fred() -> dict:
    S: dict = collections.defaultdict(dict)
    for r in read("fred_market"):
        S[r["series"]][int(r["year"])] = r["value"]
    return S


def _tech() -> dict:
    by: dict = {}
    for r in read("owid_tech"):
        by.setdefault(r["name"], []).append((int(r["year"]), r["share"]))
    return {k: sorted(v) for k, v in by.items()}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec = read("sec_annual")

    # --- Uber -----------------------------------------------------------------------------------------------------
    rev = {int(r["year_end"][:4]): r["revenue"] for r in sec if r["ticker"] == "UBER" and r["revenue"]}
    tam = get("uber.tam.mobility") + get("uber.tam.eats") + get("uber.tam.freight")
    R["uber"] = dict(mobility=get("uber.tam.mobility"), eats=get("uber.tam.eats"), freight=get("uber.tam.freight"),
                     tam=tam, sam=get("uber.sam.mobility"), miles=get("uber.tam.miles"),
                     platform_miles=get("uber.miles.2018"), per_mile=get("uber.tam.mobility") / get("uber.tam.miles"),
                     revenue=rev, share_2018=rev[2018] / (tam * 1000), share_2025=rev[2025] / (tam * 1000))

    # --- WeWork ----------------------------------------------------------------------------------------------------
    R["wework"] = dict(per_employee=get("wework.cost"), members=get("wework.members"), total=get("wework.total"),
                       check=get("wework.cost") * get("wework.members") * 1e6 / 1e12, addressable=get("wework.addressable"))

    # --- bottled water: three sizes --------------------------------------------------------------------------------
    S = _fred()
    pop23 = S["POPTHM"][2023] / 1000  # millions
    gallons = get("water.bmc.percap.2023") * pop23 / 1000  # billions of gallons
    census, primo = get("water.census.2023"), get("water.primo.2023")
    R["water"] = dict(pop=pop23, percap=get("water.bmc.percap.2023"), gallons=gallons, census=census, primo=primo,
                      factory_per_gal=census / gallons, retail_per_gal=primo / gallons, ratio=primo / census,
                      primo_rev=[r["revenue"] for r in sec if r["ticker"] == "PRMB" and r["year_end"][:4] == "2024"][0],
                      percap24=get("water.bmc.percap.2024"), single24=get("water.bmc.single.2024"))

    # --- the census, over time ---------------------------------------------------------------------------------------
    ship = {y: v / 1e6 for y, v in S["AIES312112RCTUS"].items()}  # $bn
    ppi = S["PCU312112312112"]
    yrs = sorted(ship)
    R["census"] = dict(years=yrs, shipments=[ship[y] for y in yrs], ppi={y: ppi[y] for y in yrs if y in ppi},
                       real=[ship[y] / (ppi[y] / ppi[yrs[0]]) for y in yrs if y in ppi],
                       employees=S["AIES312112EMPUS"].get(max(yrs)), last=max(yrs),
                       ppi_2026=ppi.get(2026))

    # --- diffusion ----------------------------------------------------------------------------------------------------
    T = _tech()
    fits = {}
    for name in SHOW:
        d = T[name]
        y = np.array([a for a, _ in d], float)
        s = np.array([b for _, b in d], float)
        f = fit_bass(y, s)
        f["peak"] = f["t0"] + peak_year(f["p"], f["q"])
        f["years"], f["shares"] = y.tolist(), s.tolist()
        fits[name] = f
    R["diffusion"] = fits

    # --- calling the curve early: fit on the first quarter, compare with the last observation -------------------------
    early = []
    for name, d in T.items():
        y = np.array([a for a, _ in d], float)
        s = np.array([b for _, b in d], float)
        if len(y) < 8 or s.max() < 40:
            continue
        e = early_forecast(y, s, 25)
        if e is None:
            continue
        final_pred = float(predict(e["early"], [y[-1]])[0])
        early.append(dict(name=name, cut=e["cut"], last_year=float(y[-1]), last=float(s[-1]), predicted=final_pred,
                          miss=final_pred - float(s[-1]), ceiling=e["early"]["m"], years=y.tolist(),
                          shares=s.tolist(), early=e["early"]))
    early.sort(key=lambda d: abs(d["miss"]))
    miss = np.array([abs(d["miss"]) for d in early])
    R["early"] = dict(rows=early, n=len(early), median=float(np.median(miss)), within10=int((miss <= 10).sum()),
                      over30=int((miss > 30).sum()))

    # --- adding up companies where a few hold nearly everything: home centers, 2022 ---------------------------------
    hc = next(r for r in read("census_conc_2022") if r["code"] == "444110")
    fy22 = {t: next(r["revenue"] for r in sec if r["ticker"] == t and r["year_end"][:4] == "2023") for t in ("HD", "LOW")}
    R["homes"] = dict(census=hc["sales_k"] / 1e6, firms=int(hc["firms"]), cr4=hc["cr4"], hd=fy22["HD"], low=fy22["LOW"],
                      both=fy22["HD"] + fy22["LOW"], gap=(fy22["HD"] + fy22["LOW"]) / (hc["sales_k"] / 1e6) - 1)

    # --- price and quantity: what a dollar of computers or cars buys over time ------------------------------------------
    pr = {int(r["year"]): r for r in read("fred_prices")}
    R["prices"] = dict(years=sorted(pr), computers=[pr[y]["CUUR0000SEEE01"] for y in sorted(pr)],
                       cars=[pr[y]["CUSR0000SETA01"] for y in sorted(pr)],
                       comp_fall=pr[2025]["CUUR0000SEEE01"] / pr[2000]["CUUR0000SEEE01"] - 1,
                       car_rise=pr[2025]["CUSR0000SETA01"] / pr[2000]["CUSR0000SETA01"] - 1)

    # --- this series' call -------------------------------------------------------------------------------------------
    R["call"] = dict(last=ship[max(yrs)], last_year=max(yrs), threshold=7.5)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    u = R["uber"]
    print(f"Uber TAM ${u['tam']:.1f}tn (mobility {u['mobility']}, eats {u['eats']}, freight {u['freight']}); "
          f"{u['miles']}tn miles at {100 * u['per_mile']:.0f} cents; revenue 2018 ${u['revenue'][2018]:.1f}bn "
          f"({100 * u['share_2018']:.2f}% of TAM), 2025 ${u['revenue'][2025]:.1f}bn ({100 * u['share_2025']:.2f}%)")
    w = R["wework"]
    print(f"WeWork: ${w['per_employee']:,.0f} x {w['members']:.0f}m = ${w['check']:.2f}tn (stated ${w['total']}tn)")
    b = R["water"]
    print(f"water 2023: pop {b['pop']:.1f}m x {b['percap']} gal = {b['gallons']:.1f}bn gal; Census ${b['census']}bn "
          f"(${b['factory_per_gal']:.2f}/gal), Primo ${b['primo']}bn (${b['retail_per_gal']:.2f}/gal), x{b['ratio']:.1f}; "
          f"Primo revenue 2024 ${b['primo_rev']:.2f}bn")
    c = R["census"]
    print("census shipments " + ", ".join(f"{y}: {v:.2f}" for y, v in zip(c["years"], c["shipments"])))
    for n, f in R["diffusion"].items():
        print(f"   {n:24s} p={f['p']:.3f} q={f['q']:.2f} m={f['m']:.0f} peak {f['peak']:.0f} rmse {f['rmse']:.1f}")
    e = R["early"]
    print(f"early fits: {e['n']} technologies; median miss {e['median']:.1f} points; {e['within10']} within 10; "
          f"{e['over30']} over 30")
    for d in e["rows"][-5:]:
        print(f"   {d['name']:30s} cut {d['cut']:.0f}: predicted {d['predicted']:.0f} for {d['last_year']:.0f}, "
              f"was {d['last']:.0f}")


if __name__ == "__main__":
    main()
