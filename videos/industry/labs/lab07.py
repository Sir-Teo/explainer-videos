"""Lab 7: size a market three ways, split its growth into price and quantity, and fit and stress S-curves."""

import numpy as np

from explainer.industry.works.diffusion import early_forecast, peak_year, predict
from videos.coursekit import labs
from videos.industry.industry7.compute import results

TITLE = "Sizing a market: top-down, bottom-up, addressable markets and S-curves"
GOAL = ("Rebuild American bottled water from the bottom up and set it against the Census Bureau's and Primo Brands' "
        "figures; add up two companies to size home centers; split a market's growth into price and quantity; read "
        "Uber's addressable market as a share; fit Bass curves, show that the early years cannot fix the ceiling, and "
        "size a full market by what wears out.")
TASKS = [
    "Refit colour television's curve on the years up to 50% of households instead of 25%. How close does the "
    "ceiling come to what happened, and how many years of data did that cost?",
    "Give the microwave a life of 7 and then 14 years in the replacement model. How many are sold in 2025 in each "
    "case, and in which year do replacements first outnumber first purchases?",
    "Split the growth of bottled-water shipments from 2012 to 2019, before the inflation of the 2020s, into price "
    "and quantity. How does the story differ from 2012-2024?",
]


def replacement(years, stock, life):
    first = [0.0] + [max(stock[k] - stock[k - 1], 0.0) for k in range(1, len(years))]
    repl = [0.0] + [stock[k - 1] / life for k in range(1, len(years))]
    return np.array(first), np.array(repl)


def run(seed=0):
    lab = labs.Lab()
    R = results()

    # 1. Uber's addressable market, read as a share
    U = R["uber"]
    lab.row("Uber's TAM in its 2019 prospectus: mobility + freight + meals",
            f"${U['mobility']:.1f}tn + ${U['freight']:.1f}tn + ${U['eats']:.1f}tn = ${U['tam']:.1f}tn")
    for y in (2018, 2025):
        lab.row(f"Uber's revenue {y} as a share of the TAM", f"{100 * U['revenue'][y] / 1000 / U['tam']:.2f}%")

    # 2. three answers for bottled water, on one definition at a time
    W = R["water"]
    assert abs(W["gallons"] - W["pop"] * W["percap"] / 1000) < 1e-9
    lab.row("gallons, 2023: people x gallons each", f"{W['pop']:.1f}m x {W['percap']} = {W['gallons']:.1f}bn")
    lab.row("a gallon at the plant door (Census) / at the till (Primo)",
            f"${W['factory_per_gal']:.2f} / ${W['retail_per_gal']:.2f} (x{W['ratio']:.1f})")

    # 3. adding up companies where a few hold the market
    H = R["homes"]
    assert abs(H["both"] - (H["hd"] + H["low"])) < 1e-9
    lab.row("home centers, 2022: Census / Home Depot + Lowe's",
            f"${H['census']:.0f}bn / ${H['both']:.0f}bn ({100 * H['gap']:+.1f}%)")

    # 4. dollars = units x price
    C = R["census"]
    dol = C["shipments"][-1] / C["shipments"][0] - 1
    qty = C["real"][-1] / C["real"][0] - 1
    pri = (1 + dol) / (1 + qty) - 1
    assert abs((1 + pri) * (1 + qty) - (1 + dol)) < 1e-12
    lab.row(f"bottled water shipments {C['years'][0]}-{C['years'][-1]}: dollars / price / quantity",
            f"{100 * dol:+.0f}% / {100 * pri:+.0f}% / {100 * qty:+.0f}%")
    P = R["prices"]
    lab.row("consumer prices 2000-2025, quality-adjusted: computers / new vehicles",
            f"{100 * P['comp_fall']:+.0f}% / {100 * P['car_rise']:+.0f}%")

    # 5. S-curves: fits, the peak, and the fan of ceilings through the early years
    for name, f in R["diffusion"].items():
        lab.row(f"Bass fit, {name}: p / q / ceiling / peak year",
                f"{f['p']:.3f} / {f['q']:.2f} / {f['m']:.0f}% / {f['t0'] + peak_year(f['p'], f['q']):.0f}")
    F = R["fan"]
    lab.row(f"colour TV to {F['cut']:.0f}: rmse of curves capped at 40 / 60 / 80 / 100%",
            " / ".join(f"{f['rmse']:.2f}" for f in F["fits"]))
    tv = next(d for d in R["early"]["rows"] if d["name"] == "Colour TV")
    e50 = early_forecast(np.array(tv["years"]), np.array(tv["shares"]), 50)
    lab.row("colour TV: ceiling fitted to the years up to 25% / up to 50% / what happened",
            f"{tv['ceiling']:.0f}% / {e50['early']['m']:.0f}% / {tv['last']:.0f}%")
    E = R["early"]
    lab.row(f"all {E['n']} technologies fitted on their first quarter: median miss", f"{E['median']:.0f} points")

    # 6. a full market: first purchases and replacements
    M = R["replace"]
    for life in (8, 10, 12):
        first, repl = replacement(M["years"], M["stock"], life)
        lab.row(f"microwaves sold in 2025 with a {life}-year life (model)", f"{first[-1] + repl[-1]:.1f}m")
    first, repl = replacement(M["years"], M["stock"], M["life"])
    assert abs(first[-1] + repl[-1] - M["sales"]) < 1e-9

    fig, (ax1, ax2) = labs.figure(2)
    ys, ss = np.array(tv["years"]), np.array(tv["shares"])
    xs = np.linspace(1964, 2006, 200)
    for f, col in zip(F["fits"], (labs.GOLD, labs.RED, labs.BLUE, labs.GREY)):
        ax1.plot(xs, predict(f, xs), color=col, lw=1.6, label=f"ceiling {f['m']:.0f}%")
    ax1.plot(ys, ss, "o", color="k", ms=3.5, label="households with colour TV")
    ax1.axvline(F["cut"], color=labs.GREY, ls="--", lw=0.8)
    ax1.set_ylabel("% of US households")
    ax1.set_title("Four ceilings fit the early years equally well")
    ax1.legend(fontsize=7)
    yy = np.array(M["years"])
    ax2.stackplot(yy, first, repl, colors=(labs.GOLD, labs.BLUE), labels=("first purchases", "replacements"))
    ax2.set_ylabel("microwaves sold a year, millions (model)")
    ax2.set_title(f"A full market is what wears out ({M['life']}-year life)")
    ax2.legend(fontsize=8, loc="upper left")
    lab.fig = fig
    lab.note = ("Every sizing is a definition plus two counts; the counts agree only on one definition, the growth "
                "splits into price and quantity, and the ceiling of an S-curve has to come from outside its early years.")
    return lab
