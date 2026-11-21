"""Lab 58: scoring the bill: a bridge appraised from surplus to sensitivity, values without prices, a statistical life,
a tax change scored with behaviour, discounting, microsimulation, general equilibrium, optimism bias and CBO's
record."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import appraisal as A

TITLE = "Scoring the bill"
GOAL = ("Appraise the Island's bridge, price what has no market, score a tax change with and without behaviour, and "
        "check the forecasts behind it all against a record.")
TASKS = [
    "Make the bridge charge a toll of 2 (A.appraise({'toll': 2.0})). Who gains, who loses, and does the NPV rise?",
    "Score the top rate with the survey's weights ignored (every weight 1, totals scaled by 400,000 / records). "
    "How far off is the static score, and why?",
    "Raise the reference class's traffic shortfall to 30% (A.REFERENCE['traffic'] = (0.7, 0.25)). What is the chance "
    "the bridge loses money now?",
]


def run(seed=0):
    lab = labs.Lab()
    y = A.bridge_year()
    lab.row("a year of the bridge: time, fares, new trips, Bo's profit, lives (millions)",
            f"{y['time']:.2f}, {y['fares']:.2f}, {y['new trips']:.2f}, {y["Bo's profit"]:.2f}, {y['safety']:.2f}")
    for r in (0.03, 0.035, 0.07):
        a = A.appraise(rate=r)
        lab.row(f"NPV and benefit-cost ratio at {100 * r:g}%", f"{a['npv']:+.1f}, {a['bcr']:.2f}")
    lab.row("internal rate of return; NPV on the Green Book's 2003 schedule",
            f"{100 * A.irr():.2f}%; {A.appraise(schedule=A.GREEN_BOOK_2003)['npv']:+.1f}")
    for name, lo, hi in A.tornado()[:3]:
        lab.row(f"tornado: {name}", f"{lo:+.0f} to {hi:+.0f}")
    H = A.hedonic_houses(seed=58 + seed)
    lab.row("road noise, % of price a decibel: alone; with the harbour and rooms; planted",
            f"{H['naive']:+.2f}; {H['full']:+.2f}; {H['truth']:+.2f}")
    T = A.travel_cost(seed=58 + seed)
    lab.row("the beach: demand a - b x cost; its yearly value beyond the cost of getting there",
            f"{T['a']:.2f} - {T['b']:.3f} c; {T['value'] / 1e3:.0f} thousand")
    V = A.wage_risk(seed=58 + seed)
    lab.row("VSL from wages (millions): risk alone; ability held fixed; risk mismeasured",
            f"{V['naive']:.1f}; {V['controls']:.1f}; {V['noisy']:.1f}")
    S = A.score_top_rate(A.taxpayers(seed=58 + seed))
    lab.row("top rate 40% to 45%: static, with behaviour (millions); ratio; Saez's formula",
            f"{S['static']:.0f}, {S['behavioural']:.0f}; {S['ratio']:.2f}; {S['formula']:.2f}")
    W = A.weitzman([0.01, 0.07], [0.5, 0.5], [0, 50, 100, 200])
    lab.row("Weitzman's certainty-equivalent rate at 0, 50, 100, 200 years",
            ", ".join(f"{100 * x:.2f}%" for x in W["rate"]))
    D = A.dynamic_score()
    lab.row("dynamic toy (% of GDP over ten years): conventional, growth, interest rates, dynamic",
            f"{D['sum_conventional']:.2f}, {D['sum_growth']:+.2f}, {D['sum_rates']:+.2f}, {D['sum_dynamic']:.2f}")
    Hh = A.households(seed=58 + seed)
    base = A.net_income(Hh)
    t = A.distribution_table(Hh, base, A.net_income(Hh, A.reform_schedule()))
    lab.row("allowance to 18,000 and 45% above 80,000: net cost; % change, poorest and richest tenths",
            f"{t['cost']:.1f} million; {t['rows'][0]['pct']:+.2f}%, {t['rows'][-1]['pct']:+.2f}%")
    G = A.harberger_check(0.10)
    lab.row("a 10% tax on manufactures: deadweight loss in general equilibrium, Harberger's triangle",
            f"{G['dwl']:.3f}, {G['triangle']:.3f}")
    M = A.monte_carlo(seed=58 + seed)
    assert M["mean"] < M["forecast"]           # the record pulls the bridge's value below its own forecast
    lab.row("the bridge with the reference class: forecast NPV, mean, chance of a loss",
            f"{M['forecast']:+.0f}, {M['mean']:+.0f}, {100 * M['p_negative']:.0f}%")
    R = A.cbo_record()
    lab.row("CBO's deficit errors, % of GDP, years 1, 6, 11 of the projection",
            ", ".join(f"{h['mae']:.2f}" for h in R["horizon"] if h["year"] in (1, 6, 11)))

    lab.note = ("A bridge that passes on its own forecasts can fail on the record of forecasts like them; the discount "
                "rate and behaviour can each change the answer; and every score should be checked afterwards.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    rates = np.linspace(0.0, 0.1, 41)
    ax[0].plot(100 * rates, A.npv_curve(None, rates), color=labs.ORANGE)
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set(title="the bridge's NPV by discount rate", xlabel="discount rate, %", ylabel="millions")
    ax[1].hist(M["npv"], bins=40, color=labs.PURPLE)
    ax[1].axvline(M["forecast"], color="k", lw=1)
    ax[1].set(title="NPV with costs and traffic from the record", xlabel="millions", ylabel="draws")
    lab.fig = fig
    return lab
