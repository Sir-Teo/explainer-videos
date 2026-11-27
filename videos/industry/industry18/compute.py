"""Every number in Part 18 of *Industry, Built* ("Aerospace and Defence"), from the Register, the Filing Room and the
Works.

    python -m videos.industry.industry18.compute        # prints the film's numbers; writes .cache/industry18/computed.json

Items:
    hook        2025's deliveries, backlogs and losses (Boeing, Airbus); GE's service share; Lockheed's one customer
    run         the Run it game: a new airliner or a re-engine, against a rival (the Works)
    making      deliveries by model; production rates
    programme   the Works' programme: the valley of cash, the learning curve; Boeing's accounting quantities
    accounting  Boeing's Commercial Airplanes losses and net income since 2015; reach-forward losses; the 777X
    two         the duopoly: deliveries, backlogs, the years of work in them
    aid         the WTO disputes
    engines     GE's equipment against services; the Works' engine; the GTF charge
    history     US orders and shipments of civil and defence aircraft since 1992 (FRED)
    suppliers   the suppliers' margins against the airframers' (SEC); TransDigm's proprietary parts
    lessors     AerCap's fleet and margins
    defence     the primes' margins; Lockheed's customer and contracts; America's defence spending (FRED)
    budgets     military spending by country and the world, 1988-2025 (SIPRI)
    landscape   the companies by revenue and margin
    called      Boeing's first-delivery targets against the outcomes; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import aircraft

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry18"
PRIMES = ("LMT", "RTX", "NOC", "GD", "LHX", "HII")
SUPPLIERS = ("TDG", "HEI", "HWM", "SPR", "TXT")
SIPRI_SHOW = ["United States of America", "China", "Russia", "Germany", "India", "United Kingdom", "Saudi Arabia",
              "Ukraine", "France", "Japan"]


def _series(rows):
    d: dict = collections.defaultdict(dict)
    for r in rows:
        d[r["series"]][str(r["month"])] = r["value"]
    return d


def _annual(monthly: dict, need: int = 12, how=np.mean) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(how(v)) for y, v in by.items() if len(v) >= need}


def _fy(end: str) -> int:
    y, m = int(end[:4]), int(end[5:7])
    return y - 1 if m <= 3 else y


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_aero"):
        if r.get("revenue") and r["revenue"] > 0:
            sec[r["ticker"]][str(r["year_end"])] = r
    fred = _series(read("fred_aero"))
    eur = {int(m[:4]): v for m, v in _series(read("fred_auto"))["AEXUSEU"].items()}[2025]

    def margins(tk, start=2010):
        return {_fy(e): r["profit"] / r["revenue"] for e, r in sec[tk].items() if r.get("profit") is not None and _fy(e) >= start}

    # --- hook -------------------------------------------------------------------------------------------------------------
    R["hook"] = dict(ab=get("ab.deliv"), ba=get("ba.deliv"), ab_backlog=get("ab.backlog"), bca_op=get("ba.bca.op"),
                     ge_services=get("ge.services.share"), lmt_usg=get("lmt.usg"), cum747=get("ba.cum.747"),
                     ba_ni=margins("BA"), ba_rev=sec["BA"]["2025-12-31"]["revenue"])

    # --- run it -----------------------------------------------------------------------------------------------------------
    d = aircraft.Duel()
    g = aircraft.run_it(d)
    R["run"] = dict(table={f"{a}|{b}": [v / 1e9 for v in vals] for (a, b), vals in g["table"].items()},
                    alt={f"{a}|{b}": [v / 1e9 for v in vals] for (a, b), vals in g["alt_table"].items()},
                    eq=g["equilibria"], alt_eq=g["alt_equilibria"], options=aircraft.OPTIONS,
                    alt_options=aircraft.variant(), market=d.market, margin=d.margin / 1e6, horizon=d.horizon, k=d.k)

    # --- making -----------------------------------------------------------------------------------------------------------
    R["making"] = dict(ba={m: get(f"ba.deliv.{m}") for m in ("737", "787", "777", "767")},
                       ab={m: get(f"ab.deliv.{m}") for m in ("a320", "a220", "a350", "a330")},
                       rate737=get("ba.rate.737"), rate320=get("ab.rate.a320"), rate220=get("ab.rate.a220"),
                       rate47=get("bq.rate.737"), spirit=get("ba.spirit"), ab_spirit=get("ab.spirit.charge"),
                       fal=get("ab.fal"), q9=get("bq.deliv.9m"), q9_prev=get("bq.deliv.9m.2025"))

    # --- the programme --------------------------------------------------------------------------------------------------------
    p = aircraft.Programme()
    fl = p.flows()
    R["programme"] = dict(dev=p.dev / 1e9, dev_years=p.dev_years, price=p.price / 1e6, first=p.first_cost / 1e6,
                          learning=p.learning, rate=p.rate, cum={f["year"]: f["cum"] / 1e9 for f in fl},
                          built={f["year"]: f["built"] for f in fl}, trough=p.trough() / 1e9, be=p.break_even(),
                          npv=p.npv() / 1e9, cross=p.unit_crosses_price(),
                          unit={n: p.unit_cost(n) / 1e6 for n in (1, 2, 4, 10, 50, 100, 200, 500, 1000, 2000)},
                          slow=aircraft.Programme(learning=0.9).npv() / 1e9,
                          cum_slow={f["year"]: f["cum"] / 1e9 for f in aircraft.Programme(learning=0.9).flows()},
                          be_slow=aircraft.Programme(learning=0.9).break_even(), rnd=get("ba.bca.rnd"),
                          units={f["year"]: f["units"] for f in fl},
                          aq={k: get(f"ba.aq.{k}") for k in ("737", "787", "777", "777x")})

    # --- programme accounting ------------------------------------------------------------------------------------------------
    ba = sec["BA"]
    R["accounting"] = dict(bca={2023: get("ba.bca.op.2023"), 2024: get("ba.bca.op.2024"), 2025: get("ba.bca.op")},
                           ni={_fy(e): r["profit"] for e, r in ba.items() if _fy(e) >= 2014},
                           rev={_fy(e): r["revenue"] for e, r in ba.items() if _fy(e) >= 2014},
                           rf=get("ba.rf.777x767.2024"), x_target=get("ba.777x.target"), x_first=get("ba.777x.first"),
                           rf777x={2024: get("ba.rf.777x.2024"), 2025: get("ba.rf.777x.2025")}, q9=get("bq.bca.op.9m"),
                           aq={k: get(f"ba.aq.{k}") for k in ("737", "787", "777", "777x")}, aq737_now=get("bq.aq.737"),
                           cum737=get("ba.cum.737"), cum737_now=get("bq.cum.737"),
                           undel={k: get(f"ba.undel.{k}") for k in ("737", "787", "777", "777x")},
                           cum={"737": get("ba.cum.737"), "787": get("bq.cum.787.2025"), "777": get("bq.cum.777.2025"), "777x": 0},
                           dpc=get("bq.777x.dpc"), avg=float(np.mean([p.unit_cost(n) for n in range(1, 1501)])) / 1e6,
                           unit_lin={n: p.unit_cost(n) / 1e6 for n in range(1, 1501, 10)})

    # --- why two ------------------------------------------------------------------------------------------------------------
    ba_undel = sum(get(f"ba.undel.{m}") for m in ("737", "767", "777", "777x", "787"))
    R["two"] = dict(ab=get("ab.deliv"), ba=get("ba.deliv"), share_ab=get("ab.deliv") / (get("ab.deliv") + get("ba.deliv")),
                    ab_backlog=get("ab.backlog"), ba_backlog=ba_undel, ab_years=get("ab.backlog") / get("ab.deliv"),
                    ba_years=ba_undel / get("ba.deliv"), y737=get("ba.undel.737") / get("ba.deliv.737"),
                    y787=get("ba.undel.787") / get("ba.deliv.787"), ab_cum=(get("ab.orders.cum"), get("ab.deliv.cum")),
                    ba_hist={2023: get("ba.deliv.2023"), 2024: get("ba.deliv.2024"), 2025: get("ba.deliv")},
                    ab_hist={2024: get("ab.deliv.2024"), 2025: get("ab.deliv")}, erj=margins("ERJ"),
                    a220=get("ab.a220"), single=get("ba.deliv.737") + get("ab.deliv.a320") + get("ab.deliv.a220"),
                    inc_n=get("ba.cum.737"), inc_cost=p.unit_cost(get("ba.cum.737")) / 1e6,
                    entrant={pr: aircraft.Programme(price=pr * 1e6).npv() / 1e9 for pr in range(60, 121, 5)},
                    entrant_be={pr: aircraft.Programme(price=pr * 1e6).break_even() for pr in (110, 100, 90, 80, 70)})

    # --- launch aid ---------------------------------------------------------------------------------------------------------
    hit, flop_p = aircraft.Programme(), aircraft.Programme(rate=30, years=12)
    a_hit, a_flop = aircraft.launch_aid(hit), aircraft.launch_aid(flop_p)
    R["aid"] = dict(ds316=get("wto.ds316"), ds353=get("wto.ds353"), claim=get("wto.ds353.claim"),
                    nasa=get("wto.ds353.nasa"), instances=get("wto.ds316.instances"), panel=get("wto.ds353.panel"),
                    tariff=get("ab.tariff"), tariff_charge=get("ab.tariff.charge"),
                    loan=a_hit["loan"] / 1e9, hit=dict(trough=hit.trough() / 1e9, trough_aid=a_hit["trough"] / 1e9,
                                                       repaid=a_hit["repaid"] / 1e9),
                    flop=dict(units=sum(flop_p.deliveries()), end=flop_p.flows()[-1]["cum"] / 1e9,
                              end_aid=a_flop["cum"][max(a_flop["cum"])] / 1e9, repaid=a_flop["repaid"] / 1e9,
                              rate=flop_p.rate, years=flop_p.years))

    # --- engines ------------------------------------------------------------------------------------------------------------
    e = aircraft.Engine()
    life = e.lifetime()
    yrs = list(range(0, e.life + 1))
    cum = []
    run = life["sale"]
    for t in yrs:
        if t > 0:
            run += life["service_yearly"] / (1 + e.discount) ** t
        cum.append(run / 1e6)
    R["engines"] = dict(equipment=get("ge.ces.equipment"), services=get("ge.ces.services"), profit=get("ge.ces.profit"),
                        base=get("ge.base.commercial"), share=get("ge.services.share"), engines=get("ge.engines"),
                        leap=get("ge.leap"), life={k: (v / 1e6 if isinstance(v, float) and abs(v) > 1000 else v)
                                                     for k, v in life.items()},
                        cum=dict(zip(yrs, cum)), price=e.price / 1e6, cost=e.cost / 1e6, hours=e.hours,
                        per_hour=e.per_hour, years=e.life, gtf=get("rtx.pw.charge"), install=get("ge.install"),
                        gtf_fleet=get("rtx.gtf.fleet"), cfm=get("ge.cfm"))

    # --- history: orders and shipments ---------------------------------------------------------------------------------------
    R["history"] = dict(orders=_annual(fred["ANAPNO"], how=np.sum), ships=_annual(fred["ANAPVS"], how=np.sum),
                        def_orders=_annual(fred["ADAPNO"], how=np.sum), monthly=fred["ANAPNO"],
                        ip=_annual(fred["IPG3364S"]))

    # --- suppliers ------------------------------------------------------------------------------------------------------------
    R["suppliers"] = dict(margins={tk: margins(tk, 2015) for tk in SUPPLIERS + ("BA", "GE")},
                          avg={tk: float(np.mean([v for y, v in margins(tk, 2015).items() if 2015 <= y <= 2025]))
                               for tk in SUPPLIERS + ("BA", "GE", "AER", "ERJ") + PRIMES},
                          tdg=(get("tdg.proprietary"), get("tdg.aftermarket")))

    # --- lessors -------------------------------------------------------------------------------------------------------------
    aer = sec["AER"]["2025-12-31"]
    R["lessors"] = dict(owned=get("aer.owned"), rev=aer["revenue"], margin=aer["profit"] / aer["revenue"],
                        assets=aer["assets"], order=get("aer.order"), em=get("aer.em"), bought=get("aer.bought"),
                        sold=get("aer.sold"), proceeds=get("aer.proceeds"), gain=get("aer.gain"), russia=get("aer.russia"),
                        avg=float(np.mean([v for y, v in margins("AER", 2021).items() if 2021 <= y <= 2025])),
                        margins=margins("AER", 2015), ab_orders=get("ab.orders.cum"), ab_deliv=get("ab.deliv.cum"),
                        ab_backlog=get("ab.backlog"), ab_net=get("ab.orders.net"))

    # --- defence --------------------------------------------------------------------------------------------------------------
    latest = {tk: sec[tk][max(sec[tk])] for tk in PRIMES}
    R["defence"] = dict(margins={tk: r["profit"] / r["revenue"] for tk, r in latest.items()},
                        rev={tk: r["revenue"] for tk, r in latest.items()}, usg=get("lmt.usg"), costplus=get("lmt.costplus"),
                        f35=get("lmt.f35"), fdefx=_annual(fred["FDEFX"], need=4), bds=get("ba.bds.fpd"),
                        cpi=_annual(fred["CPIAUCNS"], need=11))  # the BLS published no October 2025 CPI
    f, c = R["defence"]["fdefx"], R["defence"]["cpi"]
    R["defence"]["real"] = {y: f[y] * c[2025] / c[y] for y in f if y in c and y <= 2025}

    # --- budgets ------------------------------------------------------------------------------------------------------------
    sip: dict = collections.defaultdict(dict)
    gdp: dict = collections.defaultdict(dict)
    for r in read("sipri_milex"):
        (sip if r["measure"] == "usd2024_m" else gdp)[r["country"]][int(r["year"])] = r["value"]
    R["budgets"] = dict(top={c: sip[c].get(2025, 0) / 1e3 for c in SIPRI_SHOW}, world=dict(sip["World"]),
                        gdp={c: gdp[c].get(2025) for c in SIPRI_SHOW},
                        growth={c: sip[c][2025] / sip[c][2021] - 1 for c in ("Russia", "Ukraine", "Germany", "China",
                                                                             "United States of America") if 2021 in sip[c]},
                        us=dict(sip["United States of America"]), china=dict(sip["China"]))

    # --- landscape --------------------------------------------------------------------------------------------------------------
    comp = [dict(name="Airbus", group="airframer", rev=get("ab.rev") * eur / 1e3, margin=get("ab.ni") / get("ab.rev"), year="2025")]
    groups = {"BA": ("Boeing", "airframer"), "ERJ": ("Embraer", "airframer"), "GE": ("GE Aerospace", "engines"),
              "RTX": ("RTX", "engines"), "LMT": ("Lockheed Martin", "defence"), "NOC": ("Northrop Grumman", "defence"),
              "GD": ("General Dynamics", "defence"), "LHX": ("L3Harris", "defence"), "HII": ("Huntington Ingalls", "defence"),
              "TDG": ("TransDigm", "supplier"), "HEI": ("HEICO", "supplier"), "HWM": ("Howmet", "supplier"),
              "TXT": ("Textron", "supplier"), "AER": ("AerCap", "lessor")}
    for tk, (name, grp) in groups.items():
        r = sec[tk][max(sec[tk])]
        m5 = [v for y, v in margins(tk, 2021).items() if (2025 if tk == "GE" else 2021) <= y <= 2025]  # GE alone from 2024
        comp.append(dict(name=name, group=grp, rev=r["revenue"], margin=float(np.mean(m5)), year=str(_fy(max(sec[tk])))))
    R["landscape"] = dict(companies=comp, eur=eur, q9=get("bq.deliv.9m"), q9_prev=get("bq.deliv.9m.2025"),
                          rate47=get("bq.rate.737"), cert10=get("bq.737.10"), x_first=get("bq.777x.first"),
                          backlog=get("bq.backlog"), bca9=get("bq.bca.op.9m"))

    # --- called -------------------------------------------------------------------------------------------------------------------
    t787, t777x = (get("ba.787.target"), get("ba.787.first")), (get("ba.777x.target"), get("bq.777x.first"))
    R["called"] = dict(t787=t787, t777x=t777x, slips=[t787[1] - t787[0], t777x[1] - t777x[0]], now=get("bq.777x.first"),
                       prob=0.55, deliv9m=get("bq.deliv.9m"), rate47=get("bq.rate.737"), cert10=get("bq.737.10"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    h = R["hook"]
    print("hook", h["ab"], h["ba"], h["ab_backlog"], h["bca_op"], {y: round(v, 3) for y, v in h["ba_ni"].items() if y >= 2018})
    print("run", R["run"]["table"], R["run"]["eq"], R["run"]["alt_eq"])
    p = R["programme"]
    print("programme", round(p["trough"], 1), p["be"], round(p["npv"], 1), round(p["cross"]), round(p["slow"], 1), p["unit"])
    a = R["accounting"]
    print("accounting", a["bca"], {y: round(v, 2) for y, v in a["ni"].items()})
    t = R["two"]
    print("two", round(t["share_ab"], 3), t["ba_backlog"], round(t["ab_years"], 1), round(t["ba_years"], 1), round(t["y737"], 1), round(t["y787"], 1))
    e = R["engines"]
    print("engines", e["life"], round(e["equipment"] / (e["equipment"] + e["services"]), 3))
    hs = R["history"]
    print("orders $bn", {y: round(v / 1e3) for y, v in hs["orders"].items() if y in (1995, 2000, 2001, 2003, 2007, 2009, 2014, 2019, 2020, 2023, 2024, 2025)})
    print("suppliers avg", {k: round(100 * v, 1) for k, v in R["suppliers"]["avg"].items()})
    print("lessors", R["lessors"])
    dfc = R["defence"]
    print("defence", {k: round(100 * v, 1) for k, v in dfc["margins"].items()}, {y: round(v) for y, v in dfc["real"].items() if y in (1953, 1968, 1987, 2000, 2010, 2025)})
    b = R["budgets"]
    print("budgets", {k: round(v) for k, v in b["top"].items()}, round(b["world"][2025] / 1e3), {k: round(v, 2) for k, v in b["growth"].items()})
    print("landscape", [(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1)) for c in R["landscape"]["companies"]])
    print("called", R["called"])


if __name__ == "__main__":
    main()
