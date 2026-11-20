"""Lab 42: social insurance: pooling with independent and common risks, Baily and Chetty's formula checked at the
optimum of a static search model, Chetty's split into liquidity and moral hazard, a weekly search model with benefits
that run out, the coinsurance trade-off in health insurance, an Oregon-style lottery with its power, the examiner
instrument, defaults, the EITC's schedule, pay-as-you-go arithmetic and the MVPF."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import insurance as I
from explainer.economics.island import truths

TITLE = "Social insurance"
GOAL = ("Show why a pool cannot remove recession risk; derive and check the Baily-Chetty formula; split benefits' "
        "effect on search into liquidity and moral hazard; find the best coinsurance rate; estimate the effect of "
        "coverage from a lottery and judge its power; and compute pay-as-you-go benefits and the MVPF.")
TASKS = [
    "Baily: raise risk aversion from 2 to 4. How does the best benefit move, and does the formula still hold "
    "exactly at the new optimum?",
    "Health: make illnesses more dispersed (sigma from 1.3 to 1.8). What happens to the best coinsurance "
    "rate, and why?",
    "Oregon: how many people would the lottery need for the planted one-point effect on blood pressure to be "
    "detected four times in five?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(42)

    P = I.pooling([100, 10000, 1000000], **T["pooling"])
    lab.row("relative spread of claims per member, n = 100, 10,000, 1,000,000: independent; with recessions",
            ", ".join(f"{100 * x:.1f}%" for x in P["independent"]) + "; "
            + ", ".join(f"{100 * x:.1f}%" for x in P["correlated"]))
    assert P["correlated"][-1] > P["floor"] * 0.999

    m = I.Baily(**T["baily"])
    b = m.optimum()
    s = m.sides(b)
    lab.row("the static model: best benefit; gain and cost of the formula there", f"{100 * b:.1f}% of the wage; "
            f"{s['gain']:.4f} and {s['cost']:.4f}")
    assert abs(s["gain"] - s["cost"]) < 1e-3
    sp = m.split(b)
    lab.row("Chetty's split at the optimum: fall in de/db from liquidity, from moral hazard; liquidity's share "
            "(and its formula)", f"{abs(sp['liquidity']):.4f}, {abs(sp['moral_hazard']):.4f}, {100 * sp['share']:.1f}% "
            f"({100 * sp['share_formula']:.1f}%)")
    lab.row("MVPF of a little more UI at 20%, the optimum, 50%",
            ", ".join(f"{I.ui_mvpf(m, x):.2f}" for x in (0.2, b, 0.5)))

    W = dict(T["weekly"])
    bw, K = W.pop("b"), W.pop("K")
    wk = I.weekly(bw, K, **W)
    el = I.weekly_elasticities(bw, K, **W)
    lab.row("weekly model: hazard in week 1 and after exhaustion; mean duration; elasticities (level, length)",
            f"{100 * wk['hazard'][0]:.1f}%, {100 * wk['hazard'][K]:.1f}%; {wk['duration']:.1f} weeks; "
            f"{el['level']:.2f}, {el['length']:.2f}")

    h = I.Health(**T["health"])
    c = h.optimum()
    pl = {x: h.plan(x) for x in (0.0, 0.25, 0.95, 1.0)}
    lab.row("health: best coinsurance; risk premium with none, overuse with free care (% of income)",
            f"{100 * c:.0f}%; {100 * pl[1.0]['risk_premium']:.2f}%, {100 * pl[0.0]['overuse']:.2f}%")
    lab.row("RAND-style: the 95% plan against free care; arc elasticity between 25% and 95%",
            f"{100 * (1 - pl[0.95]['spending'] / pl[0.0]['spending']):.0f}% less; "
            f"{I.arc_elasticity(pl[0.25]['spending'], pl[0.95]['spending'], 0.25, 0.95):.2f}")

    L = dict(T["lottery"])
    runs = L.pop("runs")
    base = L.pop("seed")
    res = [I.lottery(seed=base + seed * 1000 + k, **L) for k in range(min(runs, 60))]
    fs = np.median([r["first_stage"] for r in res])
    sy = np.array([r["outcomes"]["systolic"]["wald"] for r in res])
    se = np.median([r["outcomes"]["systolic"]["se"] for r in res])
    lab.row("lottery: first stage; blood pressure estimates (mean, sd); power to find the planted -1",
            f"{100 * fs:.1f} points; {sy.mean():.2f}, {sy.std():.2f}; {100 * np.mean(np.abs(sy) > 1.96 * se):.0f}%")

    X = I.examiners(**T["examiners"])
    lab.row("examiners: naive gap, IV, truth for the marginal applicant (points of work)",
            f"{100 * X['naive']:.0f}, {100 * X['iv']:.0f}, {100 * X['true_marginal']:.0f}")
    assert abs(X["iv"] - X["true_marginal"]) < abs(X["naive"] - X["true_marginal"])

    D = I.defaults(**T["defaults"])
    lab.row("defaults at 15 months: opt in, automatic, still at the default",
            f"{100 * D['opt_in'][15]:.0f}%, {100 * D['auto'][15]:.0f}%, {100 * D['at_default'][15]:.0f}%")

    z = np.array([10000.0, 17880.0, 23350.0, 40000.0, 61555.0])
    cr = I.eitc(z, 0.45, 17880.0, 23350.0, 0.2106)
    lab.row("2025 EITC (three children) at $10,000, $17,880, $23,350, $40,000, $61,555",
            ", ".join(f"${x:,.0f}" for x in cr))
    for r in (5.1, 2.7, 2.3):
        lab.row(f"pay-as-you-go with 12.4% and {r} workers per beneficiary: benefit, share of the wage",
                f"{100 * I.payg(workers_per_retiree=r)['replacement']:.1f}%")
    E = I.eitc_mvpf()
    lab.row("the Island's EITC: participation before and after a 10% larger credit; MVPF",
            f"{100 * E['work0']:.1f}% -> {100 * E['work1']:.1f}%; {E['mvpf']:.2f}")

    lab.note = ("A pool removes independent risks but not recessions, which the state can carry by borrowing. The "
                "best benefit balances the value of a dollar to the unemployed against the cost of longer spells, "
                "and the formula holds exactly there; if much of the response is liquidity, the gain side is "
                "larger. Insurance raises medical spending, so the best plan keeps a price on care. A lottery with a "
                "first stage of a quarter needs large samples to see small effects.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    bs = np.linspace(0.05, 0.58, 40)
    sd = [m.sides(float(x)) for x in bs]
    ax[0].plot(bs, [r["gain"] for r in sd], color=labs.BLUE, label="gain: (u'(cu) - u'(ce))/u'(ce)")
    ax[0].plot(bs, [r["cost"] for r in sd], color=labs.ORANGE, label="cost: eps / e")
    ax[0].axvline(b, color="grey", ls="--")
    ax[0].set(title="Baily-Chetty on the Island", xlabel="benefit, share of the wage", ylim=(0, 1.5))
    ax[0].legend()
    ax[1].plot(np.arange(60), 100 * np.array(wk["hazard"][:60]), color=labs.ORANGE)
    ax[1].axvline(K, color="grey", ls="--")
    ax[1].set(title="weekly hazard of finding a job", xlabel="weeks unemployed", ylabel="%")
    lab.fig = fig
    return lab
