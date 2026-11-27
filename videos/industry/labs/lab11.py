"""Lab 11: a kilogram's price, the glut game, steel's two routes and its spread, China's share, cement's market areas,
aluminium's power, the price of stone, and the chemistry of the carbon chapter."""

import numpy as np

from explainer.industry.works import mill  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry11.compute import results

TITLE = "Heavy materials: the glut, the spread, the circle on the map and the quarry"
GOAL = ("Price a kilogram of stone, cement, steel and aluminium; play a blast furnace through a glut and see what happens "
        "when every mill runs full; read a minimill's metal spread; follow China's share of world steel; draw two cement "
        "plants' market areas; size a smelter's electricity; see why the real price of stone rises; and do the "
        "chemistry of calcination and hydrogen reduction.")
TASKS = [
    "Play mill.glut with a longer glut: repeat the bottom quarter of mill.GLUT_PRICE (and of mill.GLUT_ORDERS) four more "
    "times. Which strategy loses least now, with and without rivals running full (mill.industry_glut)? At what restart "
    "cost (mill.Mill(..., restart=...)) does banking stop paying?",
    "With mill.market, put three cement plants at 0, 250 and 400 km with gate costs of $95, $90 and $100 and trucking at "
    "12 cents a tonne-km. Where are the borders, and where is each plant's margin largest? What happens to the middle "
    "plant's area if trucking falls to 6 cents?",
    "From R['tonne'], compute Nucor's metal spread as a share of its price for each year 2018-2025, and correlate the "
    "spread with Nucor's net income (R['mustrun']['nets']['NUE']). How much does a $100 change in the spread move "
    "profit, roughly, and why does that fit about 20-25 million tons shipped?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("a kilogram: stone / cement / steel sheet / bananas / aluminium",
            " / ".join(f"${h['per_kg'][k]:.3f}" for k in ("crushed stone", "cement", "steel", "bananas", "aluminium")))
    lab.row("world output, 2025: steel / cement / aluminium (Mt)", f"{h['steel']:,.0f} / {h['cement']:,.0f} / {h['aluminium']:.0f}")

    g = R["run"]
    lab.row("glut game, one mill (run full / cut output / bank), $m",
            " / ".join(f"{g['games'][k]['total']:+,.0f}" for k in ("price", "output", "bank")))
    lab.row("glut game if every mill runs full, $m; lowest price",
            " / ".join(f"{g['games_all'][k]['total']:+,.0f}" for k in ("price", "output", "bank")) +
            f"; ${min(g['all_prices']):.0f}")
    assert g["games"]["price"]["total"] > g["games"]["output"]["total"]
    assert g["games_all"]["bank"]["total"] > g["games_all"]["price"]["total"]

    q = R["routes"]
    lab.row("blast furnace route: pellets / coke / scrap per ton; CO2 per tonne",
            f"{q['pellets']:.1f} / {q['coke']:.2f} / {q['scrap_bof']:.1f}; {q['co2']['bfbof']:.2f} t")
    lab.row("electric furnace (scrap): scrap per ton; CO2 per tonne", f"{q['scrap_eaf']:.1f}; {q['co2']['scrapeaf']:.2f} t")
    lab.row("electric-furnace share, 2025: world / China / US", f"{q['eaf']['world']:.1f}% / {q['eaf']['china']:.1f}% / "
            f"{q['eaf']['us']:.1f}%")

    t = R["tonne"]
    for y in (2020, 2022, 2025):
        lab.row(f"Nucor {y}: price / scrap in a ton / spread ($)", f"{t['price'][y]:,.0f} / {t['metal'][y]:,.0f} / "
                f"{t['spread'][y]:,.0f}")
    lab.row("real price of steel mill products, 1960 and 2025 (2025 = 1)", f"{t['real_ppi'][1960]:.2f} / {t['real_ppi'][2025]:.2f}")

    m = R["mustrun"]
    lab.row("US iron and steel capacity utilization, 1982 / 2009 / 2025", f"{m['cap_util'][1982]:.0f}% / {m['cap_util'][2009]:.0f}% / "
            f"{m['cap_util'][2025]:.0f}%")
    mm = R["minimills"]
    lab.row("US electric-furnace share 1992 / 2025; Nucor vs US Steel profit 2010-2024 ($bn)",
            f"{mm['eaf_share'][1992]:.0f}% / {mm['eaf_share'][2025]:.0f}%; {mm['cum_net']['NUE']:.0f} vs {mm['cum_net']['X']:.0f}")

    gl = R["glut"]
    lab.row("China's share of world crude steel, 1995 / 2025", f"{100 * gl['share_1995']:.0f}% / {100 * gl['share_2025']:.0f}%")
    lab.row("China's steel use 2021 / 2025; exports 2021 / 2025 (Mt)", f"{gl['asu'][2021]:.0f} / {gl['asu'][2025]:.0f}; "
            f"{gl['exports21']:.0f} / {gl['exports25']:.0f}")

    c = R["cement"]
    mk = c["market"]
    k_mid = int(np.argmin([abs(x - 150) for x in mk["x"]]))
    lab.row("two kilns 300 km apart: price at A's gate / at the border; margin at A's gate",
            f"${mk['price'][int(np.argmin([abs(x) for x in mk['x']]))]:.0f} / ${mk['price'][k_mid]:.0f}; "
            f"${mk['price'][int(np.argmin([abs(x) for x in mk['x']]))] - mk['cost'][int(np.argmin([abs(x) for x in mk['x']]))]:.0f}")
    lab.row("US cement: plants / price / CR4 cement vs ready-mix", f"{c['plants']:.0f} / ${c['price']:.0f} / "
            f"{c['cr4_cement'][0]:.0f}% vs {c['cr4_readymix'][0]:.0f}%")

    a = R["aluminium"]
    lab.row("aluminium: kWh a tonne 1980 / 2025; a 500 kt smelter's load", f"{a['energy'][1980]:,} / {a['energy'][2025]:,}; "
            f"{a['smelter']['mw']:,.0f} MW")
    lab.row("China's share of aluminium 2000 / 2025; Gulf output Jan-Mar vs Apr 2026 (kt/month)",
            f"{100 * a['china_share'][2000]:.0f}% / {100 * a['china_share'][2025]:.0f}%; {a['gcc_base']:.0f} vs {a['gcc_low']:.0f}")

    ag = R["aggregates"]
    lab.row("real price of crushed stone (today's $): 2000 / 2025", f"${ag['stone_real'][2000]:.2f} / ${ag['stone_real'][2025]:.2f}")
    lab.row("Vulcan 2025: price / gross profit a ton; years of reserves", f"${ag['vmc']['price']:.2f} / ${ag['vmc']['gp']:.2f}; "
            f"{ag['vmc']['years']:.0f}")

    cb = R["carbon"]
    lab.row("CO2 from chemistry: per t clinker / per t iron; H2 per t iron", f"{cb['calcination']:.2f} t / {cb['co2_chem']:.2f} t; "
            f"{cb['h2_kg']:.1f} kg")
    lab.row("hydrogen for a tonne of iron at $2 / $5 a kg", f"${cb['h2'][2.0]['cost']:.0f} / ${cb['h2'][5.0]['cost']:.0f}")
    lab.row("cement's process CO2 and share of the world's", f"{cb['cement_co2']:.2f} Gt ({100 * cb['cement_share']:.1f}%)")

    cl = R["called"]
    lab.row("worldsteel's year-ahead China forecasts vs outcomes",
            "; ".join(f"{r_['year']}: {r_['forecast']:+.1f}% vs {r_['actual']:+.1f}%" for r_ in cl["rows"] if r_["actual"] is not None))
    lab.row("this series' call: China's 2026 fall greater than 2.0%", f"{100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    rates = np.array(m["rates"])
    ax1.plot(100 * rates, m["curves"]["integrated"], color=labs.RED, lw=1.8, label="integrated mill")
    ax1.plot(100 * rates, m["curves"]["minimill"], color=labs.BLUE, lw=1.8, label="minimill")
    ax1.set_xlabel("share of capacity in use, %")
    ax1.set_ylabel("$ a tonne")
    ax1.set_title("Cost of a tonne against output (the Works)")
    ax1.legend(fontsize=7)
    ys = sorted(ag["stone_real"])
    ax2.plot(ys, [ag["stone_real"][y] for y in ys], color=labs.GREY, lw=1.6, label="crushed stone")
    ax2.set_ylabel("$ a tonne, today's dollars")
    ax2.set_title("The real price of crushed stone (USGS)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Heavy plants must run, so gluts last and profits swing; scrap beats ore where there is scrap; cement and "
                "stone travel badly, so each plant owns a circle; and the money stays where something cannot be copied.")
    return lab
