"""Every number in Part 35 of *Industry, Built* ("Travel and Hotels"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry35.compute        # prints the film's numbers; writes .cache/industry35/computed.json

Items:
    hook        Marriott: rooms by contract, revenue by kind, the 1993 split, the owner it left behind
    run         the Run it hotel: one rate or a rate a month, channels, the brand, the owner's return (the Works)
    night       occupancy times rate; RevPAR at Marriott, Hilton and Host; a hotel's costs; flow-through
    contract    owner, brand, operator: rooms by contract type, the fee lines, who keeps what
    light       why brands own nothing: returns on assets, the spin-offs, the pipelines
    loyalty     loyalty programmes and direct booking against the agents' commission
    traffic     the intermission's series: room prices, airfares, jobs, passengers, Booking's room nights
    agents      Booking, Expedia and Airbnb: bookings, take rates, marketing, rules
    cruise      Carnival's dollar, occupancy, deposits, the pandemic year; capacity shares
    casino      the Strip's hold, Macao, Sands in Singapore, a night at roulette; Disney's parks
    landscape   the companies by revenue and margin
    called      Booking's 2020 warning against its room nights; this series' call on 2027
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import hotel as hw

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry35"

NAMES = {"MAR": ("Marriott", "brand"), "HLT": ("Hilton", "brand"), "H": ("Hyatt", "brand"), "IHG": ("IHG", "brand"),
         "WH": ("Wyndham", "brand"), "CHH": ("Choice", "brand"), "HTHT": ("H World", "brand"), "ATAT": ("Atour", "brand"),
         "HST": ("Host Hotels", "owner"), "PK": ("Park Hotels", "owner"), "APLE": ("Apple Hospitality", "owner"),
         "RHP": ("Ryman", "owner"), "BKNG": ("Booking", "agent"), "EXPE": ("Expedia", "agent"), "ABNB": ("Airbnb", "agent"),
         "TRIP": ("Tripadvisor", "agent"), "TCOM": ("Trip.com", "agent"), "MMYT": ("MakeMyTrip", "agent"),
         "SABR": ("Sabre", "agent"), "CCL": ("Carnival", "cruise"), "RCL": ("Royal Caribbean", "cruise"),
         "NCLH": ("Norwegian", "cruise"), "LVS": ("Las Vegas Sands", "casino"), "WYNN": ("Wynn", "casino"),
         "MGM": ("MGM Resorts", "casino"), "CZR": ("Caesars", "casino"), "DKNG": ("DraftKings", "casino"),
         "FLUT": ("Flutter", "casino"), "PRKS": ("United Parks", "park"), "FUN": ("Six Flags", "park"),
         "VAC": ("Marriott Vacations", "park"), "HGV": ("Hilton Grand Vacations", "park")}


def _monthly(rows: list) -> dict:
    by: dict = collections.defaultdict(dict)
    for r in rows:
        by[r["series"]][str(r["month"])] = r["value"]
    return by


def _ym(p: str) -> float:
    return int(p[:4]) + (int(p[5:7]) - 0.5) / 12


def _fy(end: str) -> int:
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 3 else y


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    f = _monthly(read("fred_travel"))
    cny = collections.defaultdict(list)
    for m_, v in f["EXCHUS"].items():
        cny[int(m_[:4])].append(v)
    cny = {y: float(np.mean(v)) for y, v in cny.items() if len(v) == 12}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_travel"):
        if not r.get("revenue"):
            continue
        y = _fy(str(r["year_end"]))
        if r["currency"] == "CNY":
            if y not in cny:
                continue
            r = {k: (v / cny[y] if isinstance(v, float) and k not in ("year_end",) else v) for k, v in r.items()}
        sec[r["ticker"]][y] = r
    last = {t: max(d) for t, d in sec.items()}

    def g(t, item, y=None):
        y = last[t] if y is None else y
        return sec[t][y].get(item) if y in sec[t] else None

    # the hook
    rooms = {"franchised": get("ma35.fr.rooms"), "managed": get("ma35.mg.rooms"), "owned or leased": get("ma35.own.rooms"),
             "residences": get("ma35.res.rooms")}
    R["hook"] = dict(rooms=get("ma35.rooms"), props=get("ma35.props"), by=rooms, own_props=get("ma35.own.props"),
                     own_share=get("ma35.own.rooms") / get("ma35.rooms"),
                     fees=get("ma35.fees"), owned=get("ma35.owned"), reimb=get("ma35.reimb"), rev=get("ma35.rev"),
                     op=g("MAR", "operating_income"), mar_assets=g("MAR", "assets"),
                     hst_rev=g("HST", "revenue"), hst_op=g("HST", "operating_income"), hst_assets=g("HST", "assets"),
                     hst_hotels=get("hs35.hotels"), hst_marriott=get("hs35.marriott"))

    # Run it
    h = hw.Hotel(base=get("wk35.base"), elasticity=get("wk35.elast"), spread=get("wk35.spread"), lift=get("wk35.lift"),
                 ota=get("wk35.ota"), ota_indep=get("wk35.ota.ind"), commission=get("wk35.comm"), direct=get("wk35.direct"),
                 royalty=get("wk35.royalty"), programme=get("wk35.prog"), var_cost=get("wk35.var"), fixed_cost=get("wk35.fixed"),
                 invest=get("wk35.invest") * 1e3, debt=get("wk35.debt"), interest=get("wk35.rate"), shift=get("wk35.shift"))
    flat = h.best_flat()
    monthly = h.best_monthly()
    by_rate = {float(r): h.year(float(r)) for r in np.arange(120, 262, 10)}
    indep = h.with_(branded=False).best_monthly()
    disc = {float(round(d, 2)): h.with_(discount=d).best_monthly() for d in np.arange(0.0, 0.151, 0.025)}
    ft = hw.flow_through(h, 180.0)
    R["run"] = dict(hotel=dict(rooms=h.rooms, ref=h.ref_rate, ota=h.ota, ota_indep=h.ota_indep, commission=h.commission,
                               direct=h.direct, royalty=h.royalty, programme=h.programme, var=h.var_cost, fixed=h.fixed_cost,
                               invest=h.invest, debt=h.debt, interest=h.interest, lift=h.lift, season=h.season),
                    at180=h.year(180.0), flat=flat, monthly=monthly, by_rate=by_rate, indep=indep, discount=disc, flow=ft,
                    low=h.year(150.0), high=h.year(220.0))

    # the night that perishes
    R["night"] = dict(mar=(get("ma35.occ"), get("ma35.adr"), get("ma35.revpar")),
                      hlt=(get("hl35.occ"), get("hl35.adr"), get("hl35.revpar")),
                      hst_revpar=get("hs35.revpar"), hst_trevpar=get("hs35.trevpar"),
                      mix={"rooms": get("hs35.rev.rooms"), "food and drink": get("hs35.rev.fb"), "other": get("hs35.rev.other")},
                      costs={"rooms": get("hs35.c.rooms"), "food and drink": get("hs35.c.fb"), "other departments, support": get("hs35.c.dept"),
                             "management fees": get("hs35.c.mgmt"), "property tax, rent, insurance": get("hs35.c.prop"),
                             "depreciation": get("hs35.c.da")},
                      wages=get("hs35.wages"), margin=get("hs35.margin"), opm=get("hs35.opm"))

    # owner, brand, operator
    y = monthly
    roomrev = y["room_rev"]
    base_fee = get("hs35.fee.base") / 100 * y["revenue"]
    prior = 0.10 * y["cost"]
    pre = y["ebitda"] + y["fees"]   # before the brand's fees, as a managed hotel would be
    inc = max(0.0, get("hs35.fee.inc") / 100 * (pre - base_fee - y["fees"] - prior))
    R["contract"] = dict(mar=rooms, hlt={"franchised": get("hl35.fr.rooms"), "managed": get("hl35.mg.rooms"),
                                         "owned or leased": get("hl35.own.rooms")},
                         mar_fees={"franchise fees": get("ma35.franchise"), "base management": get("ma35.base"),
                                   "incentive management": get("ma35.incentive")},
                         hlt_fees={"franchise and licensing": get("hl35.franchise"), "management": get("hl35.mgmt")},
                         roy=(get("ma35.roy.lo"), get("ma35.roy.hi")), fee_base=get("hs35.fee.base"), fee_inc=get("hs35.fee.inc"),
                         imf=get("ma35.imf"), imf_us=get("ma35.imf.us"), imf_intl=get("ma35.imf.intl"),
                         split=dict(room_rev=roomrev, revenue=y["revenue"], brand=y["fees"], agents=y["dist"],
                                    costs=y["var"] + y["fixed"], ebitda=y["ebitda"], reserve=y["reserve"], interest=y["interest"],
                                    cash=y["cash"], base_fee=base_fee, inc_fee=inc, prior=prior),
                         reimb=get("ma35.reimb"), hl_reimb=get("hl35.reimb"))

    # why brands own nothing
    light = {}
    for t in ("MAR", "HLT", "H", "IHG", "WH", "CHH", "HST", "PK", "APLE", "RHP"):
        ys = sorted(sec[t])
        yy = ys[-1]
        oi = [sec[t][k]["operating_income"] / sec[t][k]["assets"] for k in ys if yy - 4 <= k <= yy and sec[t][k].get("operating_income")
              and sec[t][k].get("assets")]
        light[NAMES[t][0]] = dict(roa=100 * float(np.median(oi)) if oi else None, group=NAMES[t][1], assets=g(t, "assets"),
                                  rev=g(t, "revenue"))
    R["light"] = dict(roa=light, pipe=get("ma35.pipe"), hl_pipe=get("hl35.pipe"), nug=get("hl35.nug"), q3=get("ma35.q3"),
                      pk=dict(rev=g("PK", "revenue"), ni=g("PK", "profit")), hlt_hist={k: (sec["HLT"][k]["revenue"],
                      sec["HLT"][k].get("operating_income")) for k in sorted(sec["HLT"]) if k >= 2014})

    # loyalty
    R["loyalty"] = dict(us=get("ma35.loyal.us"), world=get("ma35.loyal"), honors=get("hl35.honors"), card=get("ma35.card"),
                        branded=monthly, indep=indep, disc={d: v["ebitda"] for d, v in disc.items()},
                        ota_disc={d: h.with_(discount=d).ota_share() for d in disc})

    # the intermission
    lod, air, cpi = f["CUUR0000SEHB"], f["CUUR0000SETG01"], f["CPIAUCNS"]
    b0 = "2019-12"
    enp = collections.defaultdict(list)
    for m_, v in f["ENPLANE"].items():
        enp[int(m_[:4])].append(v)
    R["traffic"] = dict(lodging={_ym(m_): 100 * v / lod[b0] for m_, v in lod.items() if m_ >= "2015-01"},
                        air={_ym(m_): 100 * v / air[b0] for m_, v in air.items() if m_ >= "2015-01" and v},
                        cpi={_ym(m_): 100 * v / cpi[b0] for m_, v in cpi.items() if m_ >= "2015-01"},
                        jobs={_ym(m_): v for m_, v in f["CES7072100001"].items() if m_ >= "2000-01"},
                        enplane={y: sum(v) / 1e3 for y, v in enp.items() if len(v) == 12},
                        nights={2019: get("bk35.n19"), 2020: get("bk35.n20"), 2021: get("bk35.n21"), 2022: get("bk35.n22"),
                                2023: get("bk35.n23"), 2024: get("bk35.n24"), 2025: get("bk35.nights")})

    # the online agents
    R["agents"] = dict(bk=dict(rev=get("bk35.rev"), merchant=get("bk35.merchant"), agency=get("bk35.agency"), ads=get("bk35.ads"),
                               gb=get("bk35.gb"), gbm=get("bk35.gb.merchant"), gba=get("bk35.gb.agency"), nights=get("bk35.nights"),
                               mkt=get("bk35.mkt"), op=get("bk35.op"), ni=get("bk35.ni"), props=get("bk35.props"),
                               hotels=get("bk35.hotels")),
                       ex=dict(gb=get("ex35.gb"), rev=get("ex35.rev"), mkt=g("EXPE", "marketing"), op=g("EXPE", "operating_income")),
                       ab=dict(gbv=get("ab35.gbv"), nights=get("ab35.nights"), rev=get("ab35.rev"), ni=get("ab35.ni"),
                               hosts=get("ab35.hosts"), mkt=g("ABNB", "marketing")),
                       tcom=dict(rev=g("TCOM", "revenue"), op=g("TCOM", "operating_income")))

    # cruise
    R["cruise"] = dict(ticket=get("cc35.ticket"), onboard=get("cc35.onboard"), rev=get("cc35.rev"),
                       costs={"commissions, air and port": get("cc35.c.comm"), "onboard costs": get("cc35.c.onboard"),
                              "crew pay": get("cc35.c.pay"), "fuel": get("cc35.c.fuel"), "food": get("cc35.c.food"),
                              "other ship costs": get("cc35.c.other"), "selling and admin": get("cc35.c.sga"),
                              "depreciation": get("cc35.c.da")},
                       op=get("cc35.op"), interest=get("cc35.int"), ni=get("cc35.ni"), occ=get("cc35.occ"), pax=get("cc35.pax"),
                       albd=get("cc35.albd"), deposits=get("cc35.deposits"), debt=get("cc35.debt"), berths=get("cc35.berths"),
                       industry=get("cc35.industry"), crew=get("cc35.crew"),
                       hist={2019: (get("cc35.r19"), get("cc35.ni19")), 2020: (get("cc35.r20"), get("cc35.ni20")),
                             2025: (get("cc35.rev"), get("cc35.ni"))},
                       rcl=dict(ticket=get("rc35.ticket"), onboard=get("rc35.onboard")),
                       ccl_hist={k: (sec["CCL"][k]["revenue"], sec["CCL"][k]["profit"]) for k in sorted(sec["CCL"]) if k >= 2015})

    # casinos and parks
    rl = hw.roulette(players=2000, buy_in=500.0, bet=25.0, spins=100, seed=3)
    hist, edges = np.histogram(rl["result"], bins=np.arange(-525, 526, 50))
    R["casino"] = dict(strip=get("nv35.strip"), tables=get("nv35.tables"), tablepct=get("nv35.tablepct"), bacc=get("nv35.bacc"),
                       slots=get("nv35.slots"), slotpct=get("nv35.slotpct"), state=get("nv35.state"),
                       macau={2019: get("lv35.ggr19"), 2020: get("lv35.ggr20"), 2025: get("lv35.ggr25")},
                       tax=get("lv35.tax"), contrib=get("lv35.contrib"), lvs=dict(casino=get("lv35.casino"), rooms=get("lv35.rooms"),
                       fb=get("lv35.fb"), mall=get("lv35.mall"), other=get("lv35.other"), rev=get("lv35.rev")),
                       mbs=get("lv35.mbs"), macau_ebitda=get("lv35.macau"), lvsale=get("lv35.lvsale"),
                       roulette=dict(hold=rl["hold"], house=rl["house"], drop=rl["drop"], wagered=rl["wagered"], edge=rl["edge"],
                                     win_share=rl["win_share"], expected=rl["expected"], hist=hist.tolist(),
                                     edges=edges.tolist(), players=2000, buy_in=500.0, bet=25.0, spins=100),
                       online={"DraftKings": (g("DKNG", "revenue"), g("DKNG", "operating_income")),
                               "Flutter": (g("FLUT", "revenue"), g("FLUT", "operating_income"))},
                       disney=dict(rev=get("ds35.rev"), adm=get("ds35.adm"), resorts=get("ds35.resorts"), merch=get("ds35.merch"),
                                   lic=get("ds35.lic"), plic=get("ds35.plic"), op=get("ds35.op"), ent=get("ds35.ent"),
                                   sports=get("ds35.sports"), capex=get("ds35.capex")))

    # landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if tk not in sec:
            continue
        ys = sorted(sec[tk])
        yy = ys[-1]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in ys if yy - 4 <= k <= yy and sec[tk][k].get("profit") is not None]
        if not mm:
            continue
        comp.append(dict(name=nm, group=grp, rev=sec[tk][yy]["revenue"], margin=float(np.median(mm)), fy=yy, tk=tk,
                         ni=sec[tk][yy].get("profit")))
    R["landscape"] = dict(companies=comp, cny=cny.get(2025))

    # Called it?
    N = R["traffic"]["nights"]
    q9, q9prev = get("bk35.q9"), 951.0
    est26 = N[2025] * q9 / q9prev
    target = 1400.0
    R["called"] = dict(nights=N, revs={2019: get("bk35.r19"), 2020: get("bk35.r20"), 2022: get("bk35.r22"), 2023: get("bk35.r23"),
                                       2024: get("bk35.r24"), 2025: get("bk35.rev")},
                       q9=q9, q9prev=q9prev, est26=est26, target=target, need=target / est26 - 1, prob=0.35)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", R["hook"])
    U = R["run"]
    for k in ("at180", "flat", "monthly", "indep", "low", "high"):
        y = U[k]
        print(k, "occ", round(y["occupancy"], 3), "adr", round(y["adr"], 1), "revpar", round(y["revpar"], 1), "rev", round(y["revenue"] / 1e6, 2),
              "ebitda", round(y["ebitda"] / 1e6, 3), "fees", round(y["fees"] / 1e6, 2), "dist", round(y["dist"] / 1e6, 2),
              "cash", round(y["cash"] / 1e6, 2), "yield", round(y["yield_"], 3), "turned", round(y["turned"]))
    print("monthly rates", [round(r) for r in U["monthly"]["rates"]], [round(m["occupancy"], 2) for m in U["monthly"]["months"]])
    print("by rate", {r: (round(y["occupancy"], 2), round(y["ebitda"] / 1e6, 2)) for r, y in U["by_rate"].items()})
    print("discount", {d: round(v["ebitda"] / 1e6, 3) for d, v in U["discount"].items()})
    print("flow", U["flow"])
    print("night", R["night"])
    print("contract", {k: v for k, v in R["contract"].items() if k != "split"}, {k: round(v / 1e6, 2) for k, v in R["contract"]["split"].items()})
    print("light", {k: (round(v["roa"], 1) if v["roa"] else None, v["group"]) for k, v in R["light"]["roa"].items()}, R["light"]["pk"])
    print("loyalty", {k: v for k, v in R["loyalty"].items() if k not in ("branded", "indep")})
    T = R["traffic"]
    print("traffic", round(T["lodging"][max(T["lodging"])], 1), round(T["air"][max(T["air"])], 1), round(T["cpi"][max(T["cpi"])], 1),
          {y: round(v) for y, v in T["enplane"].items() if y >= 2018}, T["jobs"][max(T["jobs"])], min(v for k, v in T["jobs"].items() if 2020 < k < 2021))
    print("agents", R["agents"])
    print("cruise", {k: v for k, v in R["cruise"].items() if k != "ccl_hist"})
    print("casino", {k: v for k, v in R["casino"].items() if k != "roulette"}, {k: v for k, v in R["casino"]["roulette"].items() if k not in ("hist", "edges")})
    print("called", R["called"])
    print("landscape", sorted([(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
