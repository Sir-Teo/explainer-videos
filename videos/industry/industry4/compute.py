"""Every number in Part 4 of *Industry, Built* ("The Cost Curve"), from the Register and the Filing Room.

    python -m videos.industry.industry4.compute        # prints the film's numbers; writes .cache/industry4/computed.json

Items:
    wright      an 80% learning curve (Wright, 1936), unit by unit
    plant       the model plant of the opening game: fixed and variable costs, the order below average cost
    delta       Delta's 2025 costs split by how soon they can be avoided (its 10-K's expense lines)
    lcoe        cost per megawatt-hour of new plants against how much of the time they run (EIA's AEO2026 costs)
    scale       cost per kilowatt of small and large versions of the same machine; the six-tenths rule
    solar       solar module prices since 1975 and installed capacity since 2000; Wright's law fitted
    seats       Delta per seat mile: the break-even load factor and operating leverage
    fleet       the US power fleet in 2025: capacity, how often each kind runs, fuel cost per megawatt-hour
    day         an illustrative hot summer day on that fleet: demand, the sun, the marginal plant and the price
    memory      Micron's gross margin by fiscal year (Part 1's rows): a price war in a high-fixed-cost industry
    software    Microsoft's Productivity and Business Processes margin (Part 3's rows): near-zero marginal cost
    called      the IEA's 2010 solar roadmap against what was built; EIA's outlook for 2027
"""

from __future__ import annotations

import functools
import json
import math
from pathlib import Path

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import stack as st

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry4"
CRF_RATE, LIFE = 0.07, 30   # an assumed 7% cost of capital over 30 years, to turn a plant's price into a yearly charge
HOURS = 8760


def crf(rate: float = CRF_RATE, years: int = LIFE) -> float:
    """Capital recovery factor: the yearly payment that repays $1 over ``years`` at ``rate``."""
    return rate / (1 - (1 + rate) ** -years)


def _eia():
    rows = read("eia_power")

    def table(t, year=2025):
        return [r for r in rows if r["table"] == t and str(r["row"]).startswith(str(year))]
    cap = {r["row"]: r["value"] for r in rows if r["table"] == "epa_04_03" and r["column"] == "Net Summer Capacity"}
    a = [r["value"] for r in table("epa_04_08_a")]
    b = [r["value"] for r in table("epa_04_08_b")]
    names_a = ["coal", "gas_cc", "gas_ct", "gas_steam", "gas_ic", "oil_steam", "oil_ct", "oil_ic"]
    names_b = ["geothermal", "hydro", "nuclear", "biomass", "other_gas", "solar", "solar_thermal", "wind", "wood"]
    cf = {}
    for names, vals in ((names_a, a), (names_b, b)):
        for k, nm in enumerate(names):
            cf[nm] = dict(gw=vals[2 * k] / 1e3, cf=vals[2 * k + 1])
    assert abs(cf["coal"]["gw"] - 169.85) < 0.1 and abs(cf["nuclear"]["cf"] - 0.911) < 1e-6
    fuel = [r["value"] for r in table("epa_07_04") if "Average Cost" in r["column"]]
    fuel = dict(coal=fuel[3], oil=fuel[4], gas=fuel[5])  # all coal ranks, petroleum, natural gas ($/MMBtu)
    assert abs(fuel["gas"] - 3.85) < 1e-9 and abs(fuel["coal"] - 2.42) < 1e-9
    heat = {(r["block"], r["column"]): r["value"] for r in rows if r["table"] == "epa_08_02" and str(r["row"]) == "2025"}
    heat = {(r["row"], r["column"]): r["value"] for r in rows if r["table"] == "epa_08_02" and
            str(r["block"]).startswith("2025")} or heat
    om = [r["value"] for r in table("epa_08_04")]  # operation (4), maintenance (4), fuel (3), total (4)
    gen = {r["column"]: r["value"] for r in rows if r["table"] == "epa_03_01_a" and str(r["row"]).startswith("2025")}
    price = {r["column"]: r["value"] for r in rows if r["table"] == "epa_02_04" and str(r["row"]).startswith("2025")}
    return dict(cap=cap, cf=cf, fuel=fuel, heat=heat, om=om, gen=gen, price=price)


# --- the illustrative day: shared with the scenes ----------------------------------------------------------------------
AVAIL = dict(wind=0.22, hydro=0.45, nuclear=0.93, coal=0.85, gas_cc=0.92, gas_steam=0.9, gas_ct=0.95, oil=0.9)


def demand(h: float) -> float:
    """Illustrative: a low of about 470 GW before dawn and a peak of about 745 GW in the early evening."""
    x = (h - 4.5) / 24 * 2 * math.pi
    return 607 - 137 * math.cos(x) - 10 * math.sin(2 * x)


def sun(h: float) -> float:
    """The sun's height, 0 at night to 1 at 1 pm (sunrise 6 am, sunset 8 pm)."""
    return max(0.0, math.sin(math.pi * (h - 6) / 14)) if 6 <= h <= 20 else 0.0


def avail(key: str, gw: float, h: float) -> float:
    """Capacity available at hour ``h``: solar follows the sun, the rest a fixed share (illustrative)."""
    if key == "solar":
        return gw * 0.85 * sun(h)
    return gw * AVAIL[key]


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R = {}

    # --- Wright's 80% curve ------------------------------------------------------------------------------------
    b80 = -math.log2(1 - get("wright.rate"))
    R["wright"] = dict(rate=get("wright.rate"), b=b80,
                       units=[2 ** k for k in range(8)], hours=[100_000 * (2 ** k) ** -b80 for k in range(8)])

    # --- the opening game: a plant with a big fixed cost and an empty order book (illustrative) ---------------------
    P = dict(fixed=10_000_000, variable=40.0, capacity=400_000, sold=200_000, price=80.0, offer_units=100_000,
             offer_price=60.0)
    base = P["sold"] * (P["price"] - P["variable"]) - P["fixed"]
    with_offer = base + P["offer_units"] * (P["offer_price"] - P["variable"])
    P.update(avg_cost=st.unit_costs(P["fixed"], P["variable"], P["sold"])["total"],
             avg_cost_after=st.unit_costs(P["fixed"], P["variable"], P["sold"] + P["offer_units"])["total"],
             profit=base, profit_after=with_offer)
    R["plant"] = P

    # --- Delta's costs by how soon they can be avoided ------------------------------------------------------------
    D = {"Salaries and benefits": 17.520, "Fuel": 9.819, "Refinery and other businesses": 5.987,
         "Contracted services": 4.617, "Landing fees and rents": 3.564, "Regional partners": 2.553,
         "Commissions and selling": 2.485, "Depreciation": 2.443, "Maintenance": 2.432, "Passenger service": 1.855,
         "Profit sharing": 1.337, "Aircraft rent": 0.542, "Other": 2.388}
    assert abs(sum(D.values()) - 57.542) < 0.01
    HORIZON = {"Fuel": 0, "Landing fees and rents": 0, "Passenger service": 0, "Commissions and selling": 0,
               "Regional partners": 1, "Contracted services": 1, "Maintenance": 1, "Refinery and other businesses": 1,
               "Salaries and benefits": 1, "Profit sharing": 1, "Other": 1, "Aircraft rent": 2, "Depreciation": 2}
    R["delta"] = dict(lines=D, horizon=HORIZON, total=sum(D.values()), revenue=get("dal.rev"), oi=get("dal.oi"))

    # --- cost per MWh of new plants against utilization (EIA's AEO2026 costs) ------------------------------------
    gas = 3.85  # $/MMBtu, 2025 electric power sector (EIA)
    techs = {}
    for key, nm in (("nuclear", "Nuclear"), ("cc2", "Combined-cycle gas"), ("ct_frame", "Gas turbine (peaker)"),
                    ("solar", "Solar"), ("wind", "Onshore wind")):
        cap = get(f"plant.{key}.overnight") * crf() + get(f"plant.{key}.fom")  # $/kW-yr
        var = get(f"plant.{key}.vom") + (gas * get(f"plant.{key}.heat") / 1000 if key in ("cc2", "ct_frame") else 0)
        if key == "nuclear":
            var += 6.64  # nuclear fuel, mills/kWh = $/MWh (EIA Table 8.4, 2025)
        techs[key] = dict(name=nm, fixed_kw_yr=cap, variable=var,
                          per_mwh={u: cap * 1000 / (HOURS * u) + var for u in (0.1, 0.25, 0.6, 0.95)})
    R["lcoe"] = dict(techs=techs, crf=crf(), rate=CRF_RATE, life=LIFE)

    # --- scale ----------------------------------------------------------------------------------------------------
    R["scale"] = dict(
        pairs=[("Gas turbine", get("plant.ct_aero.size"), get("plant.ct_aero.overnight"), get("plant.ct_frame.size"),
                get("plant.ct_frame.overnight")),
               ("Combined-cycle gas", get("plant.cc1.size"), get("plant.cc1.overnight"), get("plant.cc2.size"),
                get("plant.cc2.overnight")),
               ("Nuclear", get("plant.smr.size"), get("plant.smr.overnight"), get("plant.nuclear.size"),
                get("plant.nuclear.overnight"))],
        six_tenths=[(c, st.scale_cost(100, 1, c)) for c in (0.5, 1, 2, 4, 8)])

    # --- solar: prices since 1975, capacity since 2000, Wright's law ---------------------------------------------------
    from explainer.economics import data as econ
    s = econ.solar_pv()
    price = dict(zip(s["price_year"], s["price"]))
    capacity = dict(zip(s["cap_year"], s["capacity"]))
    yrs = [y for y in range(2000, 2026) if y in price and y in capacity]
    fit = st.wright([capacity[y] for y in yrs], [price[y] for y in yrs])
    doublings = math.log2(capacity[2025] / capacity[2000])
    R["solar"] = dict(price=price, capacity=capacity, fit=fit, years=yrs, doublings=doublings,
                      fall=price[1975] / price[2025], fall_2000=price[2000] / price[2025])

    # --- Delta's seat mile: break-even and operating leverage ------------------------------------------------------
    trasm, casm, lf = get("dal.trasm"), get("dal.casm"), get("dal.load")
    per_rpm = trasm / lf  # revenue per occupied seat mile, cents
    asm = get("dal.asm") * 1e6
    R["seats"] = dict(trasm=trasm, casm=casm, load=lf, per_rpm=per_rpm, break_even=casm / per_rpm,
                      per_point=asm * 0.01 * per_rpm / 100 / 1e9,  # $bn of revenue per point of load factor
                      oi=get("dal.oi"), leverage=(trasm * asm / 100 / 1e9) / get("dal.oi"))

    # --- the US fleet in 2025 and its merit order --------------------------------------------------------------------
    E = _eia()
    cf = E["cf"]
    fuel = E["fuel"]
    nuclear_mc = 6.64 + get("plant.nuclear.vom")
    blocks = [
        ("wind", "Wind", cf["wind"]["gw"], 0.0, cf["wind"]["cf"]),
        ("solar", "Solar", cf["solar"]["gw"], 0.0, cf["solar"]["cf"]),
        ("hydro", "Hydro", cf["hydro"]["gw"], 1.0, cf["hydro"]["cf"]),
        ("nuclear", "Nuclear", cf["nuclear"]["gw"], nuclear_mc, cf["nuclear"]["cf"]),
        ("coal", "Coal", cf["coal"]["gw"], fuel["coal"] * 10.647, cf["coal"]["cf"]),
        ("gas_cc", "Gas, combined cycle", cf["gas_cc"]["gw"], fuel["gas"] * 7.535 + get("plant.cc2.vom"),
         cf["gas_cc"]["cf"]),
        ("gas_steam", "Gas, steam", cf["gas_steam"]["gw"], fuel["gas"] * 10.293, cf["gas_steam"]["cf"]),
        ("gas_ct", "Gas turbines (peakers)", cf["gas_ct"]["gw"] + cf["gas_ic"]["gw"],
         fuel["gas"] * 10.975 + get("plant.ct_frame.vom"), cf["gas_ct"]["cf"]),
        ("oil", "Oil", cf["oil_steam"]["gw"] + cf["oil_ct"]["gw"] + cf["oil_ic"]["gw"], fuel["oil"] * 10.969,
         0.05),
    ]
    R["fleet"] = dict(blocks=[dict(key=k, name=n, gw=g, mc=m, cf=c) for k, n, g, m, c in blocks], fuel=fuel,
                      price=E["price"], nuclear_mc=nuclear_mc)

    # --- an illustrative hot summer day on that fleet ---------------------------------------------------------------
    def dispatch(h: float) -> dict:
        bl = [st.Block(b["key"], avail(b["key"], b["gw"], h), b["mc"]) for b in R["fleet"]["blocks"]]
        c = st.clear(bl, demand(h))
        marginal = max(c["running"], key=lambda k: next(b.marginal for b in bl if b.name == k))
        return dict(hour=h, demand=demand(h), price=c["price"], marginal=marginal,
                    avail={b.name: b.capacity for b in bl})
    hours = [h / 2 for h in range(49)]
    R["day"] = dict(avail=AVAIL, path=[dispatch(h) for h in hours])
    prices = [p["price"] for p in R["day"]["path"]]
    R["day"].update(low=min(prices), high=max(prices), peak_hour=max(R["day"]["path"], key=lambda p: p["price"])["hour"])

    # --- memory's price war and software's zero marginal cost ----------------------------------------------------
    R["memory"] = dict(gm={2023: get("micron.gm.fy2023"), 2025: get("micron.gm.fy2025"), 2026: get("micron.gm.fy2026")},
                       rev={2023: get("micron.revenue.fy2023"), 2025: get("micron.revenue.fy2025"),
                            2026: get("micron.revenue.fy2026")})
    R["software"] = dict(margin=get("msft.pbp_oi") / get("msft.pbp_rev"), rev=get("msft.pbp_rev"))

    # --- Called it? ---------------------------------------------------------------------------------------------
    R["called"] = dict(iea_2020=get("iea.pv2010.2020"), iea_2040=get("iea.pv2010.2040"),
                       actual_2020=capacity[2020], actual_2025=capacity[2025],
                       solar_2025=get("steo.solar.2025"), solar_2027=get("steo.solar.2027"),
                       coal_2025=get("steo.coal.2025"), coal_2027=get("steo.coal.2027"), q2_2027=get("steo.q2_2027"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    P = R["plant"]
    print(f"plant: average cost ${P['avg_cost']:.0f}; profit ${P['profit'] / 1e6:.1f}m -> ${P['profit_after'] / 1e6:.1f}m "
          f"with the order")
    for k, t in R["lcoe"]["techs"].items():
        print(f"  {t['name']:<24} fixed ${t['fixed_kw_yr']:6.0f}/kW-yr  variable ${t['variable']:5.1f}/MWh  "
              + "  ".join(f"{int(100 * u)}%: ${v:5.0f}" for u, v in t["per_mwh"].items()))
    s = R["solar"]
    print(f"solar: learning rate {100 * s['fit']['learning_rate']:.0f}% (R2 {s['fit']['r2']:.2f}), {s['doublings']:.1f} "
          f"doublings 2000-2025, price fell {s['fall']:.0f}x since 1975")
    q = R["seats"]
    print(f"Delta: break-even load factor {100 * q['break_even']:.0f}% (actual {100 * q['load']:.0f}%); a point of load "
          f"factor ${q['per_point']:.2f}bn; revenue / operating income {q['leverage']:.1f}")
    for b in R["fleet"]["blocks"]:
        print(f"  {b['name']:<24} {b['gw']:6.1f} GW  ${b['mc']:6.1f}/MWh  capacity factor {b['cf']:.2f}")
    d = R["day"]
    print(f"day: price ${d['low']:.1f} to ${d['high']:.1f}; peak at {d['peak_hour']:.1f}h; "
          + ", ".join(f"{p['hour']:.0f}h {p['marginal']}" for p in d["path"][::6]))


if __name__ == "__main__":
    main()
