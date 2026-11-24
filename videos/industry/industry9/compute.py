"""Every number in Part 9 of *Industry, Built* ("Mining and Metals"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry9.compute        # prints the film's numbers; writes .cache/industry9/computed.json

Items:
    esc         Escondida: found in 1981, opened in 1991, its 2025 results and the grade it expects
    grade       rock moved per tonne of copper at falling grades; Freeport's grades; the tonnage funnel
    curve       a copper cost curve of real operations (Freeport's three regions, Escondida) against the LME price
    where       copper mine and refinery output by country (USGS); China's share of refining
    prices      the IMF's monthly metal prices since 1992, nominal and in today's dollars
    iron        iron ore's annual benchmark steps and the market price after 2010
    boom        the supercycle: copper and iron ore, 2002-2011; the miners' profits and losses since 2015
    lithium     lithium carbonate's boom and bust (USGS) and Albemarle's accounts
    gold        gold's price (USGS) and Newmont's accounts
    bet         Simon and Ehrlich's wager, 1980-1990, recomputed from USGS's unit values, and every ten-year window
    run         the Run it game: the Works' mine across copper price paths; build now, wait, or sell
    wait        the option to wait at prices around the break-even
    spikes      what copper did in the 15 months after its previous real highs (for the call)
    call        this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import mine

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry9"
LB = mine.LB_PER_T


def _months(y0, m0, y1, m1):
    out, y, m = [], y0, m0
    while (y, m) <= (y1, m1):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    fm: dict = collections.defaultdict(dict)
    for r in read("fred_metals"):
        fm[r["series"]][r["month"]] = r["value"]
    cpi = {r["month"]: r["value"] for r in read("fred_energy") if r["series"] == "CPIAUCSL"}
    cpi_last = max(cpi)

    # --- Escondida ---------------------------------------------------------------------------------------------------
    R["esc"] = {k: get(f"esc.{k}") for k in ("holes", "found", "first_estimate", "cost", "opened")}
    R["esc"].update(output=get("esc.output.2025"), unit_cost=get("esc.cost.2025"), ebitda=get("esc.ebitda.2025"),
                    grade25=get("esc.grade.2025"), grade26=get("esc.grade.2026"), medium=get("esc.medium"),
                    first_capacity=320)

    # --- grade -------------------------------------------------------------------------------------------------------
    grades = [3.0, 1.5, 1.0, 0.5, 0.3, 0.21]
    R["grade"] = dict(grades=grades, rock=[mine.rock_per_tonne(g, 0.85, 0.0) for g in grades],
                      rock_strip=[mine.rock_per_tonne(g, 0.85, 2.0) for g in grades],
                      grasberg=get("fcx.grasberg.grade"), us_leach=get("fcx.us.leach"),
                      esc25=get("esc.grade.2025"), esc26=get("esc.grade.2026"),
                      esc_drop=1 - get("esc.grade.2026") / get("esc.grade.2025"))
    # one tonne of copper from 1% ore with two tonnes of waste a tonne of ore
    ore = 1 / (0.01 * 0.85)
    R["funnel"] = dict(moved=ore * 3, ore=ore, concentrate=1 / 0.28, cathode=1.0)

    # --- a cost curve of real operations ---------------------------------------------------------------------------------
    kt = lambda mlb: mlb * 1e6 / LB / 1e3  # noqa: E731
    pts = [("Grasberg (Freeport, Indonesia)", get("fcx.grasberg.cost"), kt(get("fcx.ptfi.prod"))),
           ("Escondida (BHP, Chile)", get("esc.cost.2025"), get("esc.output.2025")),
           ("Freeport, South America", get("fcx.sa.cost"), kt(get("fcx.sa.prod"))),
           ("Freeport, US mines", get("fcx.us.cost"), kt(get("fcx.us.prod")))]
    R["curve"] = dict(points=mine.cost_curve(pts), lme=get("lme.copper.2025"))

    # --- where it is mined and refined -----------------------------------------------------------------------------
    mine_c = {k: get(f"usgs.cu.mine.{k}") for k in ("chl", "cod", "per", "chn", "rus", "usa", "zmb", "aus", "idn", "kaz")}
    ref_c = {k: get(f"usgs.cu.ref.{k}") for k in ("chn", "cod", "chl", "jpn", "rus", "usa")}
    R["where"] = dict(mine=mine_c, refined=ref_c, world_mine=get("usgs.cu.mine"), world_refined=get("usgs.cu.refined"),
                      china_share=get("usgs.cu.china.refined") / get("usgs.cu.refined"),
                      china_mine_share=mine_c["chn"] / get("usgs.cu.mine"))

    # --- prices since 1992 ------------------------------------------------------------------------------------------------
    ms = _months(1992, 1, 2026, 9)
    real = {}
    for sid in fm:
        real[sid] = [None if fm[sid].get(m) is None or cpi.get(m) is None else fm[sid][m] * cpi[cpi_last] / cpi[m]
                     for m in ms]
    R["prices"] = dict(months=ms, nominal={k: [fm[k].get(m) for m in ms] for k in fm}, real=real, cpi_month=cpi_last,
                       copper_last=fm["PCOPPUSDM"][ms[-1]], copper_last_lb=fm["PCOPPUSDM"][ms[-1]] / LB)

    # --- iron ore: the benchmark's steps ----------------------------------------------------------------------------------
    fe = fm["PIORECRUSDM"]
    distinct = {y: len({round(fe[m], 2) for m in ms if m.startswith(str(y)) and m in fe}) for y in range(1992, 2026)}
    R["iron"] = dict(distinct=distinct, before=float(np.mean([distinct[y] for y in range(1992, 2009)])),
                     after=float(np.mean([distinct[y] for y in range(2011, 2026)])), vale_share=get("vale.2010"),
                     p2003=float(np.mean([fe[m] for m in ms if m.startswith("2003")])),
                     peak=max((m for m in ms if m in fe), key=lambda m: fe[m]))
    R["iron"]["peak_val"] = fe[R["iron"]["peak"]]
    R["iron"]["last"] = fe[ms[-1]]

    # --- the supercycle --------------------------------------------------------------------------------------------------
    cu = fm["PCOPPUSDM"]

    def yavg(series, y):
        v = [series[m] for m in ms if m.startswith(str(y)) and m in series]
        return float(np.mean(v)) if v else None
    ifrs: dict = collections.defaultdict(dict)
    for r in read("sec_ifrs"):
        y = int(r["year_end"][:4])
        ifrs[r["ticker"]][y] = dict(revenue=r["revenue"], profit=r["profit"])
    R["boom"] = dict(cu={y: yavg(cu, y) for y in range(1992, 2026)}, fe={y: yavg(fe, y) for y in range(1992, 2026)},
                     miners={t: dict(sorted(ifrs[t].items())) for t in ifrs})
    R["boom"]["cu_rise"] = R["boom"]["cu"][2011] / R["boom"]["cu"][2002]
    R["boom"]["fe_rise"] = R["boom"]["fe"][2011] / R["boom"]["fe"][2002]

    # --- lithium and gold ---------------------------------------------------------------------------------------------------
    sec = read("sec_annual")

    def acc(tic, key):
        return {int(r["year_end"][:4]): r[key] for r in sec if r["ticker"] == tic and r.get(key) is not None}
    R["lithium"] = dict(price={2021: 11700, 2022: get("usgs.li.price.2022"), 2023: 39000, 2024: 11800,
                               2025: get("usgs.li.price.2025")},
                        alb_revenue=acc("ALB", "revenue"), alb_net=acc("ALB", "net_income"),
                        batteries=get("usgs.li.batteries"))
    R["gold"] = dict(price={2021: get("usgs.au.price.2021"), 2022: get("usgs.au.price.2022"),
                            2023: get("usgs.au.price.2023"), 2024: get("usgs.au.price.2024"), 2025: get("usgs.au.price")},
                     nem_revenue=acc("NEM", "revenue"), nem_net=acc("NEM", "net_income"),
                     cb=get("usgs.au.cb"), mine=get("usgs.au.mine"))

    # --- the wager -----------------------------------------------------------------------------------------------------
    ds: dict = collections.defaultdict(dict)
    dsn: dict = collections.defaultdict(dict)
    for r in read("usgs_ds140"):
        if r["unit_value_98"] is not None:
            ds[r["metal"]][int(r["year"])] = r["unit_value_98"]
        if r["unit_value"] is not None:
            dsn[r["metal"]][int(r["year"])] = r["unit_value"]
    metals = ["chromium", "copper", "nickel", "tin", "tungsten"]
    start = {m: ds[m][1980] for m in metals}
    end = {m: ds[m][1990] for m in metals}
    win = mine.bet_windows({m: ds[m] for m in metals}, 10)
    R["bet"] = dict(metals=metals, change={m: end[m] / start[m] - 1 for m in metals},
                    nominal_change={m: dsn[m][1990] / dsn[m][1980] - 1 for m in metals},
                    basket_real=mine.basket(start, end), basket_nominal=mine.basket({m: dsn[m][1980] for m in metals},
                                                                                    {m: dsn[m][1990] for m in metals}),
                    cheque=get("bet.cheque"), windows=win, n=len(win), ehrlich=sum(1 for _, x in win if x > 1),
                    first=win[0][0], last=win[-1][0], series={m: dict(sorted(ds[m].items())) for m in metals})
    R["bet"]["ehrlich_share"] = R["bet"]["ehrlich"] / R["bet"]["n"]

    # --- Run it: the Works' mine ---------------------------------------------------------------------------------------------
    M = mine.Mine("Model deposit", ore_mt=600, grade=0.5, mill_mtpa=40, capex=3000)
    rng = np.random.default_rng(9)
    n, years = 400, 4 + M.life
    p0, mean, vol, rev = 4.5, 3.8, 0.25, 0.3
    lp = np.full(n, np.log(p0))
    paths = np.zeros((n, years))
    for y in range(years):
        paths[:, y] = np.exp(lp)
        lp = lp + rev * (np.log(mean) - lp) + vol * rng.standard_normal(n)
    now = np.array([M.npv(paths[i]) for i in range(n)])
    # wait a year: build only if next year's price makes the flat-price NPV positive
    later = np.array([(M.npv(paths[i, 1:]) if M.npv(float(paths[i, 1])) > 0 else 0.0) / 1.08 for i in range(n)])
    sell = 0.5 * M.npv(p0)  # an offer of half the value at today's price
    R["run"] = dict(name=M.name, ore=M.ore_mt, grade=M.grade, life=M.life, capex=M.capex, build=M.build,
                    copper=float(M.copper_kt()[0]), cost0=float(M.unit_cost()[0]), cost_end=float(M.unit_cost()[-1]),
                    breakeven=M.breakeven(), p0=p0, now_mean=float(now.mean()), now_loss=float((now < 0).mean()),
                    wait_mean=float(later.mean()), wait_loss=float((later < 0).mean()), sell=float(sell),
                    paths=paths[:40, :years].tolist(), years=years)

    # --- the option to wait -------------------------------------------------------------------------------------------------
    be = M.breakeven()
    R["wait"] = dict(breakeven=be, rows=[dict(price=p, **mine.wait_value(M, p, 0.25, n=800, seed=3))
                                         for p in (be * 0.8, be, be * 1.25, be * 1.6)])

    # --- copper after earlier real highs (for the call) ----------------------------------------------------------------------
    rc = real["PCOPPUSDM"]
    highs = []
    for k in range(120, len(ms) - 15):
        if rc[k] is not None and rc[k] >= max(v for v in rc[k - 120:k] if v is not None):
            if not highs or k - highs[-1] > 12:
                highs.append(k)
    after = [(ms[k], rc[k + 15] / rc[k] - 1) for k in highs]
    R["spikes"] = dict(events=after, lower=sum(1 for _, x in after if x < 0), n=len(after))

    R["call"] = dict(threshold=1100, prob=0.75, fy25=get("esc.output.2025"), fy26=(1150, 1250), medium=get("esc.medium"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    g = R["grade"]
    print("rock per tonne:", [(gr, round(x)) for gr, x in zip(g["grades"], g["rock"])], "with strip:",
          [round(x) for x in g["rock_strip"]])
    print("cost curve:", [(n, c, round(a), round(b)) for n, c, a, b in R["curve"]["points"]], "LME", R["curve"]["lme"])
    w = R["where"]
    print(f"China: {100 * w['china_share']:.0f}% of refined copper, {100 * w['china_mine_share']:.0f}% of mined")
    i = R["iron"]
    print(f"iron ore: distinct monthly prices a year {i['before']:.1f} (1992-2008) vs {i['after']:.1f} (2011-2025); "
          f"2003 ${i['p2003']:.0f}, peak {i['peak']} ${i['peak_val']:.0f}, last ${i['last']:.0f}")
    b = R["boom"]
    print(f"boom: copper x{b['cu_rise']:.1f}, iron ore x{b['fe_rise']:.1f} (2002-2011); miners {json.dumps({t: {y: round(v['profit'] or 0, 1) for y, v in d.items()} for t, d in b['miners'].items()})}")
    bt = R["bet"]
    print(f"bet: real changes {[(m, round(100 * v)) for m, v in bt['change'].items()]}; basket ${bt['basket_real']:.0f} "
          f"real, ${bt['basket_nominal']:.0f} nominal; windows {bt['first']}-{bt['last']}: Ehrlich wins {bt['ehrlich']} of "
          f"{bt['n']} ({100 * bt['ehrlich_share']:.0f}%)")
    r = R["run"]
    print(f"run: {r['copper']:.0f} kt/yr, cost ${r['cost0']:.2f}->{r['cost_end']:.2f}/lb, breakeven ${r['breakeven']:.2f}; "
          f"now mean {r['now_mean']:.0f} loss {r['now_loss']:.2f}; wait mean {r['wait_mean']:.0f}; sell {r['sell']:.0f}")
    print("wait:", [(round(x["price"], 2), round(x["now"]), round(x["wait"])) for x in R["wait"]["rows"]])
    s = R["spikes"]
    print(f"spikes: {s['events']}; lower 15 months later {s['lower']} of {s['n']}")
    print(f"copper last {R['prices']['copper_last']:.0f} $/t = {R['prices']['copper_last_lb']:.2f} $/lb")


if __name__ == "__main__":
    main()
