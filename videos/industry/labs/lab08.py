"""Lab 8: price a barrel's cost, fade a well, clear a shortage, and test Hubbert against 125 years of output."""

import numpy as np

from explainer.industry.register import get
from explainer.industry.works import oil
from videos.coursekit import labs
from videos.industry.industry8.compute import results

TITLE = "Oil and gas: decline, cost, ownership, inelastic prices and the cartel"
GOAL = ("Fit the Works' wells and fields: decline curves, break-even prices and the shale treadmill; set Aramco's lifting "
        "cost against the Dallas Fed's break-evens; follow a gallon's dollar; measure how far a small shortage moves "
        "the price; read OPEC's share and Saudi Arabia's swing; and score Hubbert's 1956 forecasts on EIA's data.")
TASKS = [
    "Give the Works' shale pad a first-year decline parameter (di) of 1.0 and then 2.0. How does its break-even price "
    "move, and how many new wells a month would hold a basin at a million barrels a day in each case?",
    "Recompute the price multiple for a 10% loss of supply with responses of 0.03 and 0.3 on both sides. Which is "
    "closer to what happened in 2026, and what does the difference say about the cushions the world found?",
    "Using EIA's monthly data, find how many months passed between the peak in oil rigs and the peak in US output in "
    "2014-2015 and again in 2019-2020. Why might the lag be shorter the second time?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    n = R["negative"]
    lab.row("WTI for May 2020: settlement on 20 April 2020 / the trading day before",
            f"-${abs(n['settle']):.2f} / ${n['prior']:.2f}")
    lab.row("Cushing's working storage in use, 17 April 2020", f"{n['cushing']:.0f}%")
    s = R["shock"]
    lab.row("Brent, monthly average: Feb / Apr / Oct 2026",
            " / ".join(f"${s['brent'][s['months'].index(m)]:.0f}" for m in ("2026-02", "2026-04", "2026-10")))

    c = R["cost"]
    lab.row("Aramco: lifting + upstream capital spending per barrel (2025)", f"${c['lifting']:.2f} + ${c['capex']:.1f}")
    lab.row("Dallas Fed, Q1 2026: existing wells / new well / Permian new well",
            f"${c['dallas_existing']:.0f} / ${c['dallas_new']:.0f} / ${c['dallas_permian']:.0f}")
    for p in c["prospects"]:
        lab.row(f"Works: {p['name']}: break-even at 10% / first-year decline", f"${p['breakeven']:.0f} / {100 * p['decline']:.0f}%")
    for r in R["run"]["results"]:
        lab.row(f"Run it: {r['name']}: share of 400 price paths that lose money", f"{100 * r['loss_share']:.0f}%")

    t = R["treadmill"]
    assert abs(oil.treadmill(np.full(600, t["wells"]), qi=650, di=1.5, b=1.0)[-1] - t["level"]) < 0.02 * t["level"]
    lab.row("Works: new shale wells a month to hold 1m b/d; output a year after drilling stops",
            f"{t['wells']:.0f}; {100 * t['stop_12']:+.0f}%")

    lab.row("ExxonMobil's proved reserves, end of 2019 / 2020 / 2021 (bn boe)",
            f"{get('xom.reserves.2019')} / {get('xom.reserves.2020')} / {get('xom.reserves.2021')}")
    pm = R["pump"]["last"]
    lab.row(f"a gallon of regular, {pm['month']}: ${pm['retail']:.2f} = crude / refining / distribution / taxes (cents)",
            " / ".join(f"{pm['retail'] * pm[k]:.0f}" for k in ("crude_pct", "refining_pct", "distribution_pct", "taxes_pct")))

    for r in R["inelastic"]["rows"]:
        if r["loss"] == 0.10:
            lab.row(f"price multiple to clear a 10% loss, responses of {r['eps']:.2f}", f"x{r['mult']:.2f}")
    imp = (s["demand"] / s["consumption_2025"]) / (s["brent_2026"] / s["brent_2025"] - 1)
    lab.row("2026: change in use / change in price (a rough elasticity)", f"{imp:.3f}")

    w = R["world"]
    lab.row("OPEC's share of world crude: 1973 / 1985 / 2025",
            " / ".join(f"{100 * w['opec_share'][y]:.0f}%" for y in (1973, 1985, 2025)))
    sw = w["swing"]
    lab.row("Saudi crude output 1980 -> 1985 -> 1986 (m b/d)", f"{sw['hi'][1] / 1000:.1f} -> {sw['lo'][1] / 1000:.1f} -> "
            f"{sw['y1986'] / 1000:.1f}")
    cr = R["crack"]["annual"]
    lab.row("3-2-1 crack spread, yearly average: 2020 / 2022 / 2026 so far", f"${cr[2020]:.0f} / ${cr[2022]:.0f} / ${cr[2026]:.0f}")
    g = R["gas"]
    lab.row(f"gas, {g['eu_peak']}: Europe / Henry Hub ($/MMBtu)", f"${g['eu_peak_val']:.0f} / ${g['hh_at_peak']:.1f}")
    lab.row("US LNG exports, 2025", f"{g['lng_bcfd_2025']:.1f} bcf a day")
    lab.row("Halliburton / SLB revenue, 2014 -> 2016", f"{100 * R['companies']['hal_fall']:.0f}% / {100 * R['companies']['slb_fall']:.0f}%")

    u = R["us"]
    for U_, h in u["hubbert"].items():
        lab.row(f"Hubbert's {U_}bn-barrel curve (logistic): peak / 2025", f"{max(h['kbd']) / 1000:.1f}m in {h['peak']} / "
                f"{h['kbd'][2025 - 1900] / 1000:.2f}m b/d")
    lab.row("actual US output: 1970 / 2008 / 2025; cumulative by 2025",
            f"{u['peak1970'] / 1000:.2f} / {dict(zip(u['years'], u['kbd']))[2008] / 1000:.2f} / {u['y2025'] / 1000:.2f}m b/d; "
            f"{u['cum_2025']:.0f}bn barrels")
    lab.row("this series' call: Brent's 2027 average below $90", f"{100 * R['call']['prob']:.0f}% (EIA forecast ${R['call']['eia']:.0f})")

    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(u["years"], np.array(u["kbd"]) / 1000, color="k", lw=1.6, label="EIA, actual")
    for (U_, h), col in zip(u["hubbert"].items(), (labs.GOLD, labs.RED)):
        ax1.plot(h["years"], np.array(h["kbd"]) / 1000, color=col, ls="--", lw=1.4, label=f"Hubbert {U_}bn (logistic)")
    ax1.axvline(1956, color=labs.GREY, lw=0.8)
    ax1.set_ylabel("US crude, million b/d")
    ax1.set_title("Hubbert (1956) against what happened")
    ax1.legend(fontsize=7)
    ms = u["months"]
    k0, k1 = ms.index("2013-01"), ms.index("2018-12")
    x = np.arange(k1 - k0 + 1)
    ax2.plot(x, np.array(u["rigs"][k0:k1 + 1]) / u["rigs"][k0], color=labs.RED, label="oil rigs")
    ax2.plot(x, np.array(u["monthly"][k0:k1 + 1]) / u["monthly"][k0], color=labs.BLUE, label="US crude output")
    ax2.set_xticks([0, 24, 48, 71])
    ax2.set_xticklabels(["2013", "2015", "2017", "2018-12"])
    ax2.set_ylabel("relative to January 2013")
    ax2.set_title("Rigs fell 80%; output 11%")
    ax2.legend(fontsize=8)
    lab.fig = fig
    lab.note = ("A barrel's cost runs from a few dollars to sixty-odd; the last barrel needed sets the price, the owner "
                "of the rock keeps the difference, and an inelastic market turns small shortages into large price moves.")
    return lab
