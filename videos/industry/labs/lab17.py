"""Lab 17: the carmakers' year, Ford's moving line, the showroom duel, how a car is made and where its dollar goes, scale
and platforms, the plant's break-even and a century of capacity use, lean production and the chip shortage, suppliers,
dealers and lenders, where the profit is, the battery, China, labour, the landscape, and forecasts of the electric car."""

import numpy as np

from explainer.industry.works import auto  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry17.compute import results

TITLE = "Automobiles: volume, the duel and the money around the car"
GOAL = ("Measure what the carmakers kept in 2025; time Ford's moving line; play the showroom duel and find why both "
        "makers discount; follow a car's dollar to the suppliers; see how R&D per car falls with volume; find a plant's "
        "break-even and set it against a century of capacity use; see what lean production bet on; read a dealer's and a "
        "lender's accounts; find where the profit is; price a battery; follow China's exports and the tariffs against them; "
        "and score forecasts of the electric car, including this series' own.")
TASKS = [
    "With auto.Duel(discount=d) and auto.run_it(d), find the smallest discount at which discounting stops being the better "
    "reply to a rival who holds the price. Then make buyers less willing to switch (auto.Duel(own=5, cross=4)): is the "
    "duel still a prisoner's dilemma?",
    "With auto.Plant, find the break-even share of capacity on two shifts. How much lower would the price of a car have "
    "to be (the variable cost unchanged) to push the break-even above the 65% at which America's plants ran in 2025?",
    "With auto.battery and the chapter's DOE estimates, find the pack cost per kWh at which a 75 kWh battery costs the same "
    "as a $6,000 engine, gearbox and exhaust. At the 2008-2023 average rate of decline, in what year would the DOE's "
    "estimate reach it?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    m = R["hook"]["margins"]
    lab.row("net profit per dollar of revenue, 2024 -> 2025 (Toyota, Honda: years to March)",
            "; ".join(f"{k} {100 * a:.1f}% -> {100 * b:.1f}%" for k, (a, b) in m.items()))
    f = R["hook"]["ford"]
    lab.row("Ford, 1913-14: chassis hours standing / rope / moving line; magneto minutes",
            f"{f['chassis'][0]:.2f} / {f['chassis'][1]:.2f} / {f['chassis'][2]:.2f}; {f['magneto'][0]:.0f} -> {f['magneto'][1]:.0f}")

    u = R["run"]
    t = u["table"]
    lab.row("the showroom duel, $m each (you, rival): hold/hold; discount/hold; discount/discount",
            f"{t['hold|hold'][0]:.0f}, {t['hold|hold'][1]:.0f}; {t['discount|hold'][0]:.0f}, {t['discount|hold'][1]:.0f}; "
            f"{t['discount|discount'][0]:.0f}, {t['discount|discount'][1]:.0f}")
    lab.row("equilibrium; both cut a shift ($m each)", f"{u['equilibria']}; {u['both_cut']:.0f}")
    assert u["equilibria"] == [("discount", "discount")]

    mk = R["making"]
    lab.row("US car and light-truck assembly, 2022: companies / plants / people / shipments ($bn)",
            f"{mk['firms']:.0f} / {mk['plants']:.0f} / {mk['employees']:,.0f} / {mk['shipments']:.0f}")
    d = R["dollar"]
    lab.row("assembly plants: materials / payroll as a share of shipments", f"{100 * d['mat_share']:.1f}% / {100 * d['pay_share']:.1f}%")
    lab.row("dealer's gross margin on a new car (AutoNation); GM North America EBIT margin",
            f"{100 * d['split']['dealer']:.1f}%; {100 * d['gmna']:.1f}%")

    s = R["scale"]["points"]
    lab.row("R&D per vehicle ($): " + " / ".join(s), " / ".join(f"{v['rnd_per']:,.0f}" for v in s.values()))
    lab.row("net profit per vehicle ($): " + " / ".join(s), " / ".join(f"{v['profit_per']:,.0f}" for v in s.values()))

    p = R["plant"]
    lab.row("the Works' plant: break-even (cars; share of capacity)", f"{p['be']:,.0f}; {100 * p['be_share']:.1f}%")
    lab.row("US motor vehicle plants' capacity use: average 1948-2025; 2009; 2025; lowest month",
            f"{p['avg']:.0f}%; {p['util'][2009]:.0f}%; {p['util'][2025]:.0f}%; {p['low']:.0f}% ({p['low_month']})")
    lab.row("Rivian and Lucid: built / capacity, 2025",
            f"{p['rivian'][0]:,.0f} / {p['rivian'][1]:,.0f}; {p['lucid'][0]:,.0f} / {p['lucid'][1]:,.0f}")
    ln = R["lean"]
    lab.row("dealers' months of supply: 2019; lowest (month); 2025",
            f"{ln['s2019']:.2f}; {ln['low']:.2f} ({ln['low_month']}); {ln['s2025']:.2f}")
    lab.row("semiconductors in the assemblers' materials, 2022", f"${ln['chips']:.2f}bn ({100 * ln['chips_share']:.1f}%)")

    sp = R["suppliers"]["avg"]
    lab.row("average net margin 2015-2025: " + " / ".join(sp), " / ".join(f"{100 * v:.1f}%" for v in sp.values()))

    dl = R["dealers"]
    lab.row("AutoNation 2025, share of revenue / of gross profit: new, used, parts and service, finance",
            " ; ".join(f"{100 * dl['rev_share'][k]:.0f}% / {100 * dl['gp_share'][k]:.0f}%" for k in ("new", "used", "ps", "fi")))
    fi = R["finance"]
    lab.row("finance arms: GM Financial / Ford Credit ($m before tax); Toyota financial services (yen bn)",
            f"{fi['gmf']:,.0f} / {fi['credit']:,.0f}; {fi['tm'][0]:,.0f}")
    lab.row("a loan on the average new car, 10% down, 60 months; a 36-month lease (58% residual)",
            f"${fi['loan']:,.0f} / month; ${fi['lease']:,.0f} / month")

    pr = R["profit"]["ford"]
    lab.row("Ford 2025, EBIT per vehicle: Blue / Pro / Model e",
            " / ".join(("-" if pr[k][2] < 0 else "") + f"${abs(pr[k][2] * 1e3 / pr[k][0]):,.0f}" for k in ("blue", "pro", "e")))

    e = R["ev"]
    lab.row("DOE battery pack cost per kWh, 2008 -> 2023 (2023 $)", f"${e['pack'][2008]:,.0f} -> ${e['pack'][2023]:,.0f}")
    lab.row("electric share of new cars, 2025: world / China / Europe / US / Norway",
            " / ".join(f"{e['shares'][k][2025]:.0f}%" for k in ("World", "China", "Europe", "United States", "Norway")))
    lab.row("2025 charges for electric plans ($bn): " + " / ".join(e["writedowns"]),
            " / ".join(f"{v:.1f}" for v in e["writedowns"].values()))

    c = R["china"]
    lab.row("car exports, $bn, 2015 -> 2025: China / Japan / Germany",
            " / ".join(f"{c['exports'][k][2015]:.0f} -> {c['exports'][k][2025]:.0f}" for k in ("China", "Japan", "Germany")))
    lab.row("China 2025: vehicles sold; new energy share; BYD's net margin",
            f"{c['total']:.1f}m; {100 * c['share']:.1f}%; {100 * c['byd']['margin']:.1f}%")
    lb = R["labour"]
    lab.row("UAW 2023 contract: base wage rise to 2027, compounded; GM's strike cost (EBIT, $bn)",
            f"{100 * lb['wage']:.1f}%; {lb['strike'][0]:.1f}")

    cl = R["called"]
    lab.row("Tesla: planned 500,000 in 2018; built 2018 / 2020",
            f"{cl['tesla']['p2018']:,.0f} / {cl['tesla']['p2020']:,.0f}")
    lab.row("EIA 2017 outlook, US electric share: forecast / actual, 2020 and 2025",
            f"{cl['aeo'][2020]:.1f}% / {cl['us'][2020]:.1f}%; {cl['aeo'][2025]:.1f}% / {cl['us'][2025]:.1f}%")
    lab.row("this series' call: world share in 2026 below the fitted curve",
            f"below {cl['threshold']:.0f}% (fit {cl['proj'][2026]:.1f}%), probability {100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    cv = R["plant"]["curve"]
    us_ = sorted(cv)
    ax1.plot([100 * x for x in us_], [cv[x] for x in us_], color=labs.BLUE, lw=1.8)
    ax1.axhline(0, color="grey", lw=0.8)
    ax1.axvline(100 * R["plant"]["be_share"], color=labs.GOLD, lw=1, ls="--")
    ax1.set_xlabel("how full the plant is, %")
    ax1.set_ylabel("profit, $m a year")
    ax1.set_title("The plant's break-even (the Works)")
    for k, col in (("World", labs.GOLD), ("China", labs.RED), ("Europe", labs.PURPLE), ("United States", labs.BLUE)):
        ser = e["shares"][k]
        ys = sorted(y for y in ser if y >= 2012)
        ax2.plot(ys, [ser[y] for y in ys], color=col, lw=1.6, label=k)
    ys = sorted(cl["proj"])
    ax2.plot(ys, [cl["proj"][y] for y in ys], color=labs.GOLD, lw=1, ls="--", label="fitted curve")
    ax2.set_ylabel("electric share of new cars, %")
    ax2.set_title("The electric car's share (IEA)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A car plant costs nearly the same full or empty, so profit depends on volume and the upside is capped by "
                "the line; every maker is tempted to fill its own plant, so discounts spread; and much of the money is made "
                "around the car, in service, finance and a few exclusive brands.")
    _ = np  # the tasks use numpy for their searches
    return lab
