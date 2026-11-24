"""Every number in Part 8 of *Industry, Built* ("Oil and Gas"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry8.compute        # prints the film's numbers; writes .cache/industry8/computed.json

Items:
    negative    20 April 2020: the futures settlement, the intraday low, Cushing's storage, monthly WTI around it
    shock       2026: Brent and WTI month by month, EIA's account of the Strait of Hormuz, the shut-ins, demand
    long        WTI since 1946 in dollars of the day and of today (CPI), Brent since 1987, the labelled episodes
    us          US crude production since 1859 (annual) and since 2000 (monthly, with Texas, North Dakota and the Gulf),
                oil rigs, net imports; Hubbert's two 1956 curves reconstructed as logistics, and cumulative output
    world       crude production by country and group, 1973-2025; OPEC's share; Saudi Arabia's swing, 1980-1986
    pump        what a gallon of regular gasoline paid for, 2000-2026
    crack       the 3-2-1 crack spread from New York Harbor gasoline and heating oil against Brent, monthly
    gas         Henry Hub, European gas and Asian LNG, monthly; US LNG exports and gas production, yearly
    companies   majors, shale producers, refiners, services and Cheniere: revenue, profit and spending
    cost        Aramco's lifting cost and the Dallas Fed's break-evens; the Works' three prospects
    run         the Run it game: three prospects across 400 price paths
    inelastic   the price multiple that clears a lost share of supply, for a few elasticities
    treadmill   the Works' shale basin: wells to stand still, and what stopping does
    call        this series' call on Brent in 2027
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import oil

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry8"


def _series(name, key="series", period="period", value="value") -> dict:
    S: dict = collections.defaultdict(dict)
    for r in read(name):
        k = r[period]
        S[r[key]][str(int(k)) if isinstance(k, float) else str(k)] = r[value]
    return S


def _months(y0, m0, y1, m1):
    out = []
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def _logistic_curve(U: float, peak: float, cum_at: float, at_year: float):
    """Hubbert's curve as a logistic: cumulative Q(t) = U / (1 + exp(-k (t - peak))), with k set so that Q(at_year)
    = cum_at.  Returns (k, production function in barrels a year)."""
    k = -np.log(U / cum_at - 1) / (at_year - peak)

    def prod(t):
        e = np.exp(-k * (np.asarray(t, float) - peak))
        return U * k * e / (1 + e) ** 2
    return float(k), prod


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    pet = _series("eia_petroleum")
    fe = _series("fred_energy", period="month")
    sec = read("sec_annual")

    # --- 20 April 2020 ----------------------------------------------------------------------------------------------
    wm = pet["RWTC"]
    R["negative"] = dict(settle=get("cftc.wti.settle.2020"), prior=get("cftc.wti.prior.2020"),
                         low=get("eia.wti.low.2020"), cushing=get("eia.cushing.2020"), runs=get("eia.runs.2020"),
                         since=get("eia.wti.since"),
                         months=_months(2019, 10, 2020, 12),
                         wti=[wm.get(k) for k in _months(2019, 10, 2020, 12)])

    # --- 2026 ------------------------------------------------------------------------------------------------------
    ks = _months(2025, 1, 2026, 10)
    R["shock"] = dict(months=ks, brent=[pet["RBRTE"].get(k) for k in ks], wti=[wm.get(k) for k in ks],
                      brent_start=get("eia.2026.brent.start"), brent_q1=get("eia.2026.brent.q1end"),
                      spread=get("eia.2026.spread"), brent_oct=get("eia.steo.brent.oct"),
                      shutin_peak=get("eia.steo.shutin.peak"), shutin_oct=get("eia.steo.shutin.oct"),
                      demand=get("eia.steo.demand.2026"), hormuz=get("eia.hormuz.2024"),
                      brent_2025=69.0, brent_2026=get("eia.steo.brent.2026"), brent_2027=get("eia.steo.brent.2027"),
                      supply_2025=get("eia.steo.supply.2025"), supply_2026=get("eia.steo.supply.2026"),
                      gasoline=pet["EMM_EPMR_PTE_NUS_DPG"].get("2026-10"))

    # --- the long view: WTI since 1946 in today's dollars -----------------------------------------------------------
    cpi = fe["CPIAUCSL"]
    last_cpi_month = max(cpi)
    lm = _months(1946, 1, 2026, 10)
    nom = [fe["WTISPLC"].get(k) for k in lm]
    real = [None if (n is None or cpi.get(k) is None) else n * cpi[last_cpi_month] / cpi[k] for k, n in zip(lm, nom)]
    yrs = sorted({int(k[:4]) for k in lm})
    yrs = [y for y in yrs if any(r is not None for k, r in zip(lm, real) if int(k[:4]) == y)]
    ann = {y: np.mean([r for k, r in zip(lm, real) if int(k[:4]) == y and r is not None]) for y in yrs}
    R["long"] = dict(months=lm, nominal=nom, real=real, cpi_month=last_cpi_month, years=yrs,
                     real_annual=[float(ann[y]) for y in yrs],
                     episodes=[(1973.8, "1973 embargo"), (1979.5, "1979 revolution in Iran"), (1986.3, "1986 Saudi flood"),
                               (2008.5, "2008 peak"), (2014.9, "2014 shale glut"), (2020.3, "2020 lockdowns"),
                               (2022.4, "2022 Ukraine"), (2026.3, "2026 Hormuz")])

    # --- the United States ----------------------------------------------------------------------------------------
    ua = {int(k): v for k, v in pet["MCRFPUS1"].items()}  # thousand barrels a year
    uy = sorted(ua)
    cum = np.cumsum([ua[y] for y in uy]) / 1e6  # billion barrels
    cum_at = dict(zip(uy, cum))
    hub = {}
    for U, peak in ((get("hubbert.us.150"), 1965), (get("hubbert.us.200"), 1970)):
        k, f = _logistic_curve(U, peak, cum_at[1955], 1955.5)
        hub[int(U)] = dict(k=k, peak=peak, years=list(range(1900, 2051)),
                           kbd=[float(f(y + 0.5) * 1e6 / 365) for y in range(1900, 2051)])  # thousand b/d
    us_kbd = {y: ua[y] / 365.0 for y in uy}
    mm = _months(2000, 1, 2026, 8)
    R["us"] = dict(years=uy, kbd=[us_kbd[y] for y in uy], cum=[float(c) for c in cum], cum_1955=float(cum_at[1955]),
                   cum_2025=float(cum_at[2025]), peak1970=us_kbd[1970], y2025=us_kbd[2025],
                   pass1970=min(y for y in uy if y > 1975 and us_kbd[y] > us_kbd[1970]),
                   hubbert=hub, months=mm,
                   monthly=[pet["MCRFPUS2"].get(k) for k in mm], texas=[pet["MCRFPTX2"].get(k) for k in mm],
                   dakota=[pet["MCRFPND2"].get(k) for k in mm], gulf=[pet["MCRFP3FM2"].get(k) for k in mm],
                   rigs=[pet["E_ERTRRO_XR0_NUS_C"].get(k) for k in mm],
                   net_imports={int(k): v for k, v in pet["MTTNTUS2"].items()},
                   exports={int(k): v for k, v in pet["MCREXUS2"].items()})
    rg = {k: v for k, v in zip(mm, R["us"]["rigs"]) if v is not None}
    pr = {k: v for k, v in zip(mm, R["us"]["monthly"]) if v is not None}
    rig_hi = max((k for k in rg if "2014-01" <= k <= "2015-06"), key=lambda k: rg[k])
    rig_lo = min((k for k in rg if "2015-06" <= k <= "2017-01"), key=lambda k: rg[k])
    p_hi = max((k for k in pr if "2015-01" <= k <= "2016-06"), key=lambda k: pr[k])
    p_lo = min((k for k in pr if "2015-06" <= k <= "2017-06"), key=lambda k: pr[k])
    R["us"]["bust"] = dict(rig_hi=(rig_hi, rg[rig_hi]), rig_lo=(rig_lo, rg[rig_lo]), prod_hi=(p_hi, pr[p_hi]),
                           prod_lo=(p_lo, pr[p_lo]), rig_fall=rg[rig_lo] / rg[rig_hi] - 1,
                           prod_fall=pr[p_lo] / pr[p_hi] - 1)
    R["us"]["per_rig"] = {y: pr[f"{y}-06"] / rg[f"{y}-06"] for y in (2008, 2012, 2016, 2020, 2024) if f"{y}-06" in rg}
    R["us"]["first_net_export"] = min(y for y, v in R["us"]["net_imports"].items() if v < 0)

    # --- the world ------------------------------------------------------------------------------------------------
    wi = collections.defaultdict(dict)
    for r in read("eia_intl"):
        wi[(r["area"], r["series"])][int(r["year"])] = r["kbd"]
    prod = {a: wi[(a, "crude_production")] for a, s in wi if s == "crude_production"}
    world = prod["WORL"]
    top = sorted((a for a in prod if a not in ("WORL", "OPEC", "OPNO")), key=lambda a: -prod[a].get(2025, 0))[:10]
    sau = prod["SAU"]
    R["world"] = dict(years=sorted(world), world=[world[y] for y in sorted(world)],
                      opec_share={y: prod["OPEC"][y] / world[y] for y in sorted(world) if y in prod["OPEC"]},
                      top=[(a, prod[a][2025]) for a in top], consumption=wi[("WORL", "consumption")],
                      saudi={y: sau[y] for y in range(1973, 2026) if y in sau},
                      swing=dict(hi=(1980, sau[1980]), lo=(1985, sau[1985]), y1986=sau[1986]))
    wti = fe["WTISPLC"]
    R["world"]["swing"].update(p1981=float(np.mean([wti[f"1981-{m:02d}"] for m in range(1, 13)])),
                               p1985=float(np.mean([wti[f"1985-{m:02d}"] for m in range(1, 13)])),
                               p1986=float(np.mean([wti[f"1986-{m:02d}"] for m in range(1, 13)])),
                               nov85=wti["1985-11"], jul86=wti["1986-07"])
    s = R["world"]["swing"]
    s["rev1981"] = sau[1981] * 365 * s["p1981"] / 1e6  # $bn, crude only, at WTI
    s["rev1985"] = sau[1985] * 365 * s["p1985"] / 1e6
    s["rev1986"] = sau[1986] * 365 * s["p1986"] / 1e6

    # --- the pump --------------------------------------------------------------------------------------------------
    pump = read("eia_pump")
    last = pump[-1]
    R["pump"] = dict(months=[p["month"] for p in pump], retail=[p["retail"] for p in pump],
                     shares={k: [p[k] for p in pump] for k in ("crude_pct", "refining_pct", "distribution_pct",
                                                               "taxes_pct")},
                     last=last, last_cents={k: last["retail"] * last[k] for k in ("crude_pct", "refining_pct",
                                                                                   "distribution_pct", "taxes_pct")},
                     taxes_cents=[p["retail"] * p["taxes_pct"] for p in pump])

    # --- refining: the 3-2-1 crack spread ---------------------------------------------------------------------------
    cm = _months(1987, 6, 2026, 10)
    crack = []
    for k in cm:
        b, g, h = pet["RBRTE"].get(k), pet["EER_EPMRU_PF4_Y35NY_DPG"].get(k), pet["EER_EPD2F_PF4_Y35NY_DPG"].get(k)
        crack.append(None if None in (b, g, h) else oil.crack_321(b, g, h))
    cy = sorted({int(k[:4]) for k in cm})
    R["crack"] = dict(months=cm, crack=crack, annual={y: float(np.mean([c for k, c in zip(cm, crack) if int(k[:4]) == y
                                                                        and c is not None])) for y in cy},
                      last=crack[-1])

    # --- gas and LNG -----------------------------------------------------------------------------------------------
    gm = _months(2010, 1, 2026, 9)
    gas = read("eia_gas")
    lng = {r["year"]: r["mmcf"] / 1e6 for r in gas if r["series"] == "N9133US2"}  # tcf
    dry = {r["year"]: r["mmcf"] / 1e6 for r in gas if r["series"] == "N9070US2"}
    eu = fe["PNGASEUUSDM"]
    R["gas"] = dict(months=gm, hh=[fe["MHHNGSP"].get(k) for k in gm], eu=[eu.get(k) for k in gm],
                    asia=[fe["PNGASJPUSDM"].get(k) for k in gm],
                    eu_peak=max((k for k in gm if eu.get(k)), key=lambda k: eu[k]),
                    lng={y: lng[y] for y in range(2014, 2026) if y in lng}, dry_2025=dry.get(2025),
                    lng_bcfd_2025=lng[2025] * 1000 / 365)
    R["gas"]["eu_peak_val"] = eu[R["gas"]["eu_peak"]]
    R["gas"]["hh_at_peak"] = fe["MHHNGSP"].get(R["gas"]["eu_peak"])

    # --- companies -------------------------------------------------------------------------------------------------
    def series(tic, key):
        return {int(r["year_end"][:4]): r[key] for r in sec if r["ticker"] == tic and r.get(key) is not None}
    R["companies"] = {t: dict(revenue=series(t, "revenue"), net=series(t, "net_income"), capex=series(t, "capex"),
                              dep=series(t, "depreciation"))
                      for t in ("XOM", "CVX", "COP", "EOG", "OXY", "DVN", "VLO", "MPC", "SLB", "HAL", "LNG")}
    hal = R["companies"]["HAL"]["revenue"]
    R["companies"]["hal_fall"] = hal[2016] / hal[2014] - 1
    slb = R["companies"]["SLB"]["revenue"]
    R["companies"]["slb_fall"] = slb[2016] / slb[2014] - 1

    # --- cost ------------------------------------------------------------------------------------------------------
    P = oil.prospects()
    R["cost"] = dict(lifting=get("aramco.lifting"), capex=get("aramco.capex"), dallas_new=get("dallas.new"),
                     dallas_permian=get("dallas.new.permian"), dallas_large=get("dallas.new.large"),
                     dallas_existing=get("dallas.existing"),
                     prospects=[dict(name=f.name, breakeven=f.breakeven(0.10), barrels=float(f.barrels().sum()),
                                     capex=f.capex, build=f.build, decline=oil.first_year_decline(f.di, f.b),
                                     note=f.note) for f in P])

    # --- Run it ----------------------------------------------------------------------------------------------------
    paths = oil.price_paths(400, 30, p0=90.0, vol=0.28, revert=0.25, mean=70.0, seed=8)
    run = []
    for f in P:
        npvs = np.array([f.npv(paths[i], 0.10) for i in range(len(paths))])
        payback = None
        cf = np.cumsum(f.cashflows(90.0))
        pos = np.where(cf > 0)[0]
        payback = int(pos[0]) if len(pos) else None
        run.append(dict(name=f.name, mean=float(npvs.mean()), loss_share=float((npvs < 0).mean()),
                        p10=float(np.percentile(npvs, 10)), p90=float(np.percentile(npvs, 90)), capex=f.capex,
                        payback_at_90=payback, npv_at_90=f.npv(90.0), per_dollar=float(npvs.mean() / f.capex)))
    R["run"] = dict(paths=paths[:40, :20].tolist(), results=run, p0=90.0)

    # --- inelastic -------------------------------------------------------------------------------------------------
    R["inelastic"] = dict(rows=[dict(loss=L, eps=e, mult=oil.clearing_multiple(L, -e, e)) for L in (0.02, 0.05, 0.10)
                                for e in (0.05, 0.1, 0.2)])

    # --- the treadmill ---------------------------------------------------------------------------------------------
    level = 1_000_000
    n = oil.wells_to_hold(level, qi=650, di=1.5, b=1.0)
    months = 72
    hold = oil.treadmill(np.full(480 + months, n), qi=650, di=1.5, b=1.0)[480:]
    stop = oil.treadmill(np.r_[np.full(480, n), np.zeros(months)], qi=650, di=1.5, b=1.0)[480:]
    R["treadmill"] = dict(level=level, wells=n, hold=hold.tolist(), stop=stop.tolist(),
                          stop_12=float(stop[12] / stop[0] - 1), well=oil.arps(np.arange(0, 61) / 12, 650, 1.5, 1.0).tolist(),
                          conv=oil.arps(np.arange(0, 61) / 12, 700, 0.10, 0.3).tolist())

    # --- the call --------------------------------------------------------------------------------------------------
    R["call"] = dict(threshold=90, prob=0.6, eia=get("eia.steo.brent.2027"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    n = R["negative"]
    print(f"20 April 2020: settle {n['settle']}, low {n['low']}, Cushing {n['cushing']}% full")
    s = R["shock"]
    print("2026 Brent by month:", ", ".join(f"{k[2:]} {v:.0f}" for k, v in zip(s["months"], s["brent"]) if v))
    u = R["us"]
    print(f"US: 1970 {u['peak1970']:.0f} kb/d; passed in {u['pass1970']}; 2025 {u['y2025']:.0f}; cumulative to 1955 "
          f"{u['cum_1955']:.1f}bn, to 2025 {u['cum_2025']:.1f}bn; first net exporter {u['first_net_export']}")
    for U, h in u["hubbert"].items():
        print(f"   Hubbert {U}bn: peak {h['peak']}, {max(h['kbd']):.0f} kb/d; 2025 {h['kbd'][125]:.0f} kb/d")
    b = u["bust"]
    print(f"   rigs {b['rig_hi']} -> {b['rig_lo']} ({100 * b['rig_fall']:.0f}%); production {b['prod_hi']} -> "
          f"{b['prod_lo']} ({100 * b['prod_fall']:.0f}%); per rig {u['per_rig']}")
    w = R["world"]
    print(f"world 2025 {w['world'][-1]:.0f} kb/d; top {w['top'][:5]}; OPEC share 1973 {w['opec_share'][1973]:.2f}, "
          f"1985 {w['opec_share'][1985]:.2f}, 2025 {w['opec_share'][2025]:.2f}")
    print(f"   swing {w['swing']}")
    p = R["pump"]
    print(f"pump {p['last']}")
    print(f"crack last {R['crack']['last']:.1f}; annual 2020 {R['crack']['annual'][2020]:.1f}, 2022 "
          f"{R['crack']['annual'][2022]:.1f}, 2025 {R['crack']['annual'][2025]:.1f}")
    g = R["gas"]
    print(f"gas: EU peak {g['eu_peak']} {g['eu_peak_val']:.1f} vs HH {g['hh_at_peak']:.1f}; LNG {g['lng']}; "
          f"{g['lng_bcfd_2025']:.1f} bcf/d")
    c = R["companies"]
    print(f"HAL 2014-16 {100 * c['hal_fall']:.0f}%, SLB {100 * c['slb_fall']:.0f}%; XOM net {c['XOM']['net']}")
    for x in R["cost"]["prospects"]:
        print(f"   {x['name']}: breakeven ${x['breakeven']:.0f}, {x['barrels']:.0f}m bbl, first-year decline "
              f"{100 * x['decline']:.0f}%")
    for x in R["run"]["results"]:
        print(f"   run {x['name']}: mean NPV {x['mean']:.0f}, loss share {x['loss_share']:.2f}, payback at $90 "
              f"{x['payback_at_90']}, per dollar {x['per_dollar']:.2f}")
    t = R["treadmill"]
    print(f"treadmill: {t['wells']:.1f} wells a month hold {t['level']:,}; stop and a year later {100 * t['stop_12']:.0f}%")
    print("inelastic:", [(r["loss"], r["eps"], round(r["mult"], 2)) for r in R["inelastic"]["rows"]])


if __name__ == "__main__":
    main()
