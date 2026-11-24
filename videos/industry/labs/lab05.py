"""Lab 5: measure how long high returns last, how concentrated industries are, and what a moat looks like in a margin."""

import numpy as np

from videos.coursekit import labs
from videos.industry.industry5.compute import EARLY, LATE, results, spearman

TITLE = "The moat: persistent returns, concentration and steady margins"
GOAL = ("Rank 88 US industries by their return on capital in 2015-2019 and again in 2022-2025 and measure how much "
        "of the order survives; describe how concentrated 897 industries are; total the profit above the cost of "
        "capital; and compare the steadiness of three companies' margins.")
TASKS = [
    "Repeat the persistence test with single years instead of averages (2015 against 2025). Is the rank correlation "
    "higher or lower, and why would averaging change it?",
    "Using census_conc_2022.csv, find the five most concentrated industries with more than 1,000 firms. What lets "
    "four firms dominate an industry with so many small ones?",
    "Add Microsoft and NextEra Energy (in sec_annual.csv) to the margin comparison. Where do their standard deviations "
    "fall between Costco's and Delta's, and what does that suggest about their moats?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    # 1. Berkshire's three businesses: extra profit per extra dollar of capital
    s, f = R["three"]["sees"], R["three"]["fsi"]
    assert abs(s["incr"] - (s["pre1"] - s["pre0"]) / (s["cap1"] - s["cap0"])) < 1e-12 and s["incr"] > 2 > f["incr"]
    lab.row("See's / FlightSafety: extra pre-tax profit per extra $ of capital", f"${s['incr']:.2f} / ${f['incr']:.2f}")

    # 2. Persistence: rank correlation of early and late averages, recomputed here
    P = R["persist"]
    early = np.array([p[1] for p in P["pairs"]])
    late = np.array([p[2] for p in P["pairs"]])
    rho = spearman(early, late)
    assert abs(rho - P["rho"]) < 1e-12 and 0.3 < rho < 0.8
    lab.row(f"rank correlation of returns, {EARLY[0]}-{EARLY[-1]} against {LATE[0]}-{LATE[-1]} ({P['n']} industries)",
            f"{rho:.2f}; top quarter {100 * P['top_early']:.0f}% -> {100 * P['top_late']:.0f}%, bottom "
            f"{100 * P['bottom_early']:.0f}% -> {100 * P['bottom_late']:.0f}%")

    # 3. Concentration: the spread of four-firm ratios
    C = R["conc"]
    assert sum(C["hist"]) == C["n"]
    lab.row("four-firm concentration, 2022: industries / median / share above 50%",
            f"{C['n']} / {C['median']:.1f}% / {100 * C['above50']:.0f}%")

    # 4. Economic profit by industry
    E = R["eva"]
    lab.row("profit above the cost of capital, 2025: total / share of the top five industries",
            f"${E['positive']:.0f}bn / {100 * E['top5_share']:.0f}%")

    # 5. HHI: the squares of shares
    for shares in ([25] * 4, [55, 15, 15, 15], [5] * 20):
        hhi = sum(x * x for x in shares)
        assert 10_000 / len(shares) - 1e-9 <= hhi <= 10_000  # equal shares give the minimum, one firm the maximum
    lab.row("HHI: four equal / one at 55% and three at 15% / twenty equal", f"{4 * 625:,} / {55 ** 2 + 3 * 225:,} / "
            f"{20 * 25:,}")

    # 6. Margins: standard deviation of operating margins, fiscal 2009-2026
    M = R["margins"]
    assert M["COST"]["sd"] < M["V"]["sd"] < M["DAL"]["sd"]
    lab.row("sd of operating margin, points: Costco / Visa / Delta",
            f"{100 * M['COST']['sd']:.1f} / {100 * M['V']['sd']:.1f} / {100 * M['DAL']['sd']:.1f}")

    # 7. Called it?: how often a top ten stays in the top twenty three years later
    B = R["base_rate"]
    lab.row("top ten still in the top twenty three years later (>= 7)", f"{B['hits']} of {B['n']} windows")

    fig, (ax1, ax2) = labs.figure(2)
    ax1.scatter(early * 100, late * 100, s=18, color=labs.GOLD)
    lim = [min(early.min(), late.min()) * 100 - 2, min(max(early.max(), late.max()) * 100 + 2, 100)]
    ax1.plot(lim, lim, color=labs.GREY, lw=1, ls="--", label="no change")
    ax1.set_xlim(lim)
    ax1.set_ylim(lim)
    ax1.set_xlabel(f"return on capital, {EARLY[0]}-{EARLY[-1]} average (%)")
    ax1.set_ylabel(f"{LATE[0]}-{LATE[-1]} average (%)")
    ax1.set_title(f"Returns persist: rank correlation {rho:.2f}")
    ax1.legend(fontsize=8)
    for tic, name, col in (("V", "Visa", labs.GOLD), ("COST", "Costco", labs.BLUE), ("DAL", "Delta", labs.RED)):
        pts = M[tic]["points"]
        ax2.plot([y for y, _ in pts], [100 * v for _, v in pts], marker="o", ms=3, color=col, label=name)
    ax2.axhline(0, color=labs.GREY, lw=0.8)
    ax2.set_xlabel("fiscal year")
    ax2.set_ylabel("operating margin (%)")
    ax2.set_title("A moat is a steady margin, not a high one")
    ax2.legend(fontsize=8)
    lab.fig = fig
    lab.note = ("Returns on capital differ widely between industries and fade only slowly; concentration alone does "
                "not explain them; and a moat shows up as a margin rivals and recessions cannot move, whatever its "
                "height.")
    return lab
