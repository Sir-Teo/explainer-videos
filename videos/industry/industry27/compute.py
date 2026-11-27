"""Every number in Part 27 of *Industry, Built* ("Shipping and Ports"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry27.compute        # prints the film's numbers; writes .cache/industry27/computed.json

Items:
    hook        the ocean freight on a pair of trainers; the Suez Canal's week in March 2021
    run         the Run it market: thirty years of a freight cycle and the owner's two rules (the Works)
    day         a ship's voyage at different speeds and fuel prices; ZIM's fuel share
    box         container port traffic since 2010; the fleet and the orderbook
    cycle       ZIM's freight rate since 2016 and by quarter; ZIM's and Maersk's profits; the deep-sea freight index
    liner       concentration; ZIM's chartered fleet; the lines against the ship lessors; Hapag-Lloyd and ZIM
    choke       daily transits through Suez, Bab el-Mandeb, the Cape, Panama, Hormuz and Malacca since 2019
    tanker      Frontline's earnings a day, its breakeven and the tanker orderbook; tanker and bulk owners' profits
    ports       the largest container countries; the forwarders; the Jones Act
    extra       the intermission's series: deep-sea freight prices, Brent, American imports
    landscape   the companies by revenue and margin
    called      ZIM's 2026 guidance, three times; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get, span
from explainer.industry.works import ship

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry27"

NAMES = {"ZIM": ("ZIM", "liner"), "MATX": ("Matson", "liner"), "KEX": ("Kirby", "barge"), "FRO": ("Frontline", "tanker"),
         "SBLK": ("Star Bulk", "bulk"), "DAC": ("Danaos", "lessor"), "GSL": ("Global Ship Lease", "lessor"),
         "CMRE": ("Costamare", "lessor"), "STNG": ("Scorpio Tankers", "tanker"), "INSW": ("International Seaways", "tanker"),
         "GNK": ("Genco", "bulk"), "TNK": ("Teekay Tankers", "tanker"), "DHT": ("DHT", "tanker"), "FLNG": ("Flex LNG", "gas"),
         "EXPD": ("Expeditors", "forwarder"), "CHRW": ("C.H. Robinson", "forwarder"), "NAT": ("Nordic American", "tanker"),
         "TRMD": ("TORM", "tanker"), "SFL": ("SFL", "lessor"), "DSX": ("Diana", "bulk"), "NMM": ("Navios Partners", "lessor")}
QUARTERS = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]


def _monthly(rows: list) -> dict:
    by: dict = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        by[r["series"]][str(r["month"])].append(r["value"])
    return {s: {m: float(np.mean(v)) for m, v in d.items()} for s, d in by.items()}


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


def _ym(p: str) -> float:
    return int(p[:4]) + (int(p[5:7]) - 0.5) / 12


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_ship"):
        if r.get("revenue"):
            sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    f = _monthly(read("fred_ship"))
    pw: dict = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in read("imf_portwatch"):
        pw[r["chokepoint"]][r["measure"]][str(r["period"])] = r["value"]

    # the hook
    rate = {y: get(f"zim.rate.{y}") for y in range(2016, 2026)}
    pairs = get("hook.pairs")
    per_pair = {y: 2 * v / pairs for y, v in rate.items()}
    suez = {p: v for p, v in pw["Suez Canal"]["n_total"].items() if len(p) == 10}
    R["hook"] = dict(rate=rate, pairs=pairs, pairs_span=span("hook.pairs"), per_pair=per_pair, suez=suez,
                     days=get("e2.evergiven"), before=float(np.mean([v for p, v in suez.items() if "2021-03-10" <= p <= "2021-03-22"])),
                     low=min(suez.values()), low_day=min(suez, key=suez.get))

    # Run it
    m = ship.Market()
    P = m.path()
    R["run"] = dict(path={k: [float(x) for x in v] for k, v in P.items()}, follow=m.owner("follow"), against=m.owner("against"),
                    lag=m.lag, breakeven=m.breakeven, opex=m.opex, floor=m.floor, top=m.top, knee=m.knee,
                    curve={round(u, 3): m.earnings(u) for u in np.arange(0.7, 1.001, 0.01)})

    # a ship's day
    R["day"] = dict(v20=ship.voyage(speed=20), v16=ship.voyage(speed=16), v14=ship.voyage(speed=14),
                    best={p: ship.best_speed(p) for p in (300, 450, 600, 750, 900)},
                    sweep={round(v, 1): ship.voyage(speed=v)["total"] / 1e6 for v in np.arange(12, 24.01, 0.5)},
                    fuel_sweep={round(v, 1): ship.voyage(speed=v)["fuel_cost"] / 1e6 for v in np.arange(12, 24.01, 0.5)},
                    ship_sweep={round(v, 1): ship.voyage(speed=v)["ship_cost"] / 1e6 for v in np.arange(12, 24.01, 0.5)},
                    bunker=get("zim.bunker"))

    # the box
    ports: dict = collections.defaultdict(dict)
    for r in read("wb_ports"):
        ports[r["country"]][int(r["year"])] = r["teu"] / 1e6
    R["box"] = dict(world={y: v for y, v in ports["World"].items()}, ports={c: v for c, v in ports.items() if c != "World"},
                    fleet=get("alpha.fleet"), ships=get("alpha.ships"), fleet21=get("alpha.fleet.2021"), order=get("alpha.order"),
                    g=dict(g21=get("alpha.g21"), g24=get("alpha.g24"), g25=get("alpha.g25"), g26=get("alpha.g26"),
                           d21=get("alpha.d21"), d25=get("alpha.d25"), d26=get("alpha.d26")),
                    deliv26=get("alpha.deliv26"), zim_teu=(get("zim.teu.2019"), get("zim.teu.2025")))

    # the cycle
    mae = {int(r["year"]): (r["revenue"], r["ebit"]) for r in read("esef_maersk")}
    zim = {y: (sec["ZIM"][y]["revenue"], sec["ZIM"][y]["profit"]) for y in sorted(sec["ZIM"])}
    ppi = _annual(f["PCU483111483111"], need=11)
    R["cycle"] = dict(rate=rate, q={q: get(f"zim.rate.{q}") for q in QUARTERS}, zim=zim, maersk=mae,
                      ppi={y: ppi[y] / ppi[2019] for y in ppi if 2005 <= y <= 2025},
                      ppi_m={_ym(k): v / ppi[2019] for k, v in f["PCU483111483111"].items() if k >= "2015-01"})

    # the liner business
    lessors = {NAMES[tk][0]: {y: sec[tk][y]["profit"] / sec[tk][y]["revenue"] for y in range(2019, 2026) if y in sec[tk]}
               for tk in ("DAC", "GSL", "CMRE")}
    zm = {y: zim[y][1] / zim[y][0] for y in zim if y >= 2019}
    R["liner"] = dict(top3=get("alpha.top3"), top3_23=get("alpha.top3.2023"), ships=get("zim.ships"), owned=get("zim.owned"),
                      zim_margin=zm, lessors=lessors, hapag=get("zim.hapag"),
                      zones={"Cross-Suez": get("zim.zone.suez"), "Pacific": get("zim.zone.pacific"),
                             "Latin America": get("zim.zone.latam"), "Atlantic-Europe": get("zim.zone.atl"),
                             "Intra-Asia": get("zim.zone.asia")}, pacific_teu=get("zim.zone.pacific.teu"))

    # chokepoints
    ch = {}
    for name in ("Suez Canal", "Bab el-Mandeb Strait", "Cape of Good Hope", "Panama Canal", "Strait of Hormuz", "Malacca Strait"):
        mm = pw[name]["n_total_mean"]
        ch[name] = {_ym(p): v for p, v in mm.items() if len(p) == 7}
    ann = {name: {y: float(np.mean([v for p, v in pw[name]["n_total_mean"].items() if p.startswith(str(y))])) for y in range(2019, 2027)}
           for name in ch}
    hz = pw["Strait of Hormuz"]["n_total_mean"]
    R["choke"] = dict(monthly=ch, annual=ann, hormuz_feb=hz["2026-02"], hormuz_mar=hz["2026-03"], hormuz_last=hz[max(hz)],
                      hormuz_last_m=max(hz), hormuz_2025=ann["Strait of Hormuz"][2025],
                      hormuz_tank25=float(np.mean([v for p, v in pw["Strait of Hormuz"]["n_tanker_mean"].items() if p.startswith("2025")])),
                      hormuz_tank_last=pw["Strait of Hormuz"]["n_tanker_mean"][max(hz)])

    # tankers and bulk
    tank = {NAMES[tk][0]: {y: (sec[tk][y]["revenue"], sec[tk][y]["profit"]) for y in range(2016, 2026) if y in sec[tk]}
            for tk in ("FRO", "SBLK")}
    R["tanker"] = dict(q3=get("fro.vlcc.q3"), q2=get("fro.vlcc.q2"), q4=get("fro.vlcc.q4"), be=get("fro.vlcc.be"),
                       suez=get("fro.suez.q3"), tc=get("fro.tc"), order=get("fro.order"), sale=get("fro.sale"), firms=tank)

    # ports and forwarders
    last = max(max(v) for v in ports.values())
    top = sorted(((c, v[max(v)]) for c, v in ports.items() if c != "World"), key=lambda t: -t[1])
    fw = {NAMES[tk][0]: {y: (sec[tk][y]["revenue"], sec[tk][y]["profit"] / sec[tk][y]["revenue"]) for y in range(2019, 2026)}
          for tk in ("EXPD", "CHRW")}
    R["ports"] = dict(top=top, year=last, fw=fw, jones=get("matx.jones"),
                      matx={y: (sec["MATX"][y]["revenue"], sec["MATX"][y]["profit"] / sec["MATX"][y]["revenue"]) for y in range(2019, 2026)})

    # the intermission
    brent = _annual(f["MCOILBRENTEU"], need=10)
    imp = _annual(f["BOPTIMP"], need=9)
    R["extra"] = dict(ppi_long={y: ppi[y] / ppi[1989] for y in ppi if y >= 1989}, brent={y: brent[y] for y in brent if y >= 2005},
                      brent_now=f["MCOILBRENTEU"][max(f["MCOILBRENTEU"])], brent_m=max(f["MCOILBRENTEU"]),
                      imports={y: 12 * imp[y] / 1e6 for y in imp if 2005 <= y})

    # the landscape
    comp = []
    for tk, (nm, grp) in NAMES.items():
        if not sec[tk]:
            continue
        y = max(sec[tk])
        rr = sec[tk][y]
        mm = [sec[tk][k]["profit"] / sec[tk][k]["revenue"] for k in sec[tk] if y - 4 <= k <= y and sec[tk][k].get("profit") is not None]
        comp.append(dict(name=nm, group=grp, rev=rr["revenue"], margin=float(np.median(mm)), fy=y, tk=tk))
    mm = [mae[y][1] / mae[y][0] for y in range(2021, 2026)]
    comp.append(dict(name="Maersk", group="liner", rev=mae[2025][0], margin=float(np.median(mm)), fy=2025, tk="MAERSK", ebit=True))
    R["landscape"] = dict(companies=comp)

    R["called"] = dict(g=[("19 August", get("zim.g.aug.lo"), get("zim.g.aug.hi")), ("6 October", get("zim.g.oct.lo"), get("zim.g.oct.hi")),
                          ("18 November", get("zim.g.nov.lo"), get("zim.g.nov.hi"))],
                       hapag=get("zim.hapag"), call="2027-06-30", prob=0.6, d21=get("alpha.d21"), g21=get("alpha.g21"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    H = R["hook"]
    print("hook", {y: round(v, 2) for y, v in H["per_pair"].items()}, "suez before", round(H["before"], 1), "low", H["low"], H["low_day"])
    U = R["run"]
    for k in ("follow", "against"):
        o = U[k]
        print(k, len(o["ships"]), round(o["avg_price"], 1), round(o["ret"], 2), round(o["profit"]), round(o["avg_earn_at_delivery"], 1))
    D = R["day"]
    print("day", {k: round(v, 2) for k, v in D["v20"].items()}, {k: round(v, 2) for k, v in D["v16"].items()}, D["best"])
    B = R["box"]
    print("box", {y: round(v) for y, v in B["world"].items()}, B["fleet"], B["order"])
    C = R["cycle"]
    print("zim", {y: (round(a, 2), round(b, 2)) for y, (a, b) in C["zim"].items()}, "maersk", C["maersk"])
    print("ppi", {y: round(v, 2) for y, v in C["ppi"].items() if y >= 2018})
    L = R["liner"]
    print("liner", {y: round(v, 3) for y, v in L["zim_margin"].items()}, {k: {y: round(x, 2) for y, x in v.items()} for k, v in L["lessors"].items()})
    K = R["choke"]
    print("choke", {k: {y: round(x, 1) for y, x in v.items()} for k, v in K["annual"].items()}, K["hormuz_feb"], K["hormuz_mar"], K["hormuz_last"],
          round(K["hormuz_tank25"], 1), K["hormuz_tank_last"])
    T = R["tanker"]
    print("tank", {k: {y: (round(a, 2), round(b, 2)) for y, (a, b) in v.items()} for k, v in T["firms"].items()})
    Po = R["ports"]
    print("ports", Po["year"], [(c, round(v, 1)) for c, v in Po["top"][:10]], {k: {y: (round(a, 1), round(100 * b, 1)) for y, (a, b) in v.items()} for k, v in Po["fw"].items()})
    E = R["extra"]
    print("extra", round(E["ppi_long"][2025], 2), {y: round(v) for y, v in E["brent"].items() if y >= 2019}, round(E["brent_now"], 1), E["brent_m"],
          {y: round(v, 2) for y, v in E["imports"].items() if y >= 2019})
    print("landscape", sorted([(c["name"], round(c["rev"], 2), round(100 * c["margin"], 1)) for c in R["landscape"]["companies"]], key=lambda t: -t[1]))


if __name__ == "__main__":
    main()
