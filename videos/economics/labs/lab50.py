"""Lab 50: the policy memo: the credits for one family and the reward for work, the Island's microsimulation at the
central dials and across the participation elasticity, the deep-poverty crossing, take-up, the value of public funds
by repayment and financing, and a second design that keeps the old credit's work requirement."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import memo
from explainer.economics.island import truths

TITLE = "The policy memo"
GOAL = ("Price a child allowance for one family, run it on the Island's 40,000 families across the range of the "
        "participation elasticity, value it per dollar under different assumptions about repayment and financing, "
        "and compare it with a design that keeps the reward for work.")
TASKS = [
    "Raise the Island's poverty line from 24,000 to 28,000. Does the allowance cut child poverty by more or less, in "
    "percent, and why?",
    "Set the income effect to 0.5 with the elasticity at 0. How many parents stop working, and what happens to deep "
    "poverty?",
    "Find the elasticity at which the second design and the full allowance leave the same share of children poor.",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(50)
    F = memo.families(**{**T["families"], "seed": T["families"]["seed"] + seed})

    e = np.array([0.0, 10000.0, 20000.0, 30000.0])
    one = np.ones_like(e)
    single = np.zeros_like(e, dtype=int)
    old = memo.ctc_2020(e, 2 * one, single)
    new = memo.allowance_2021(e, one, one, single)
    lab.row("one parent of two: old credit at 0, 10k, 20k, 30k", ", ".join(f"{x:,.0f}" for x in old))
    lab.row("one parent of two: the allowance at the same earnings", ", ".join(f"{x:,.0f}" for x in new))
    assert np.allclose(old, [0, 1125, 2745, 3920]) and np.allclose(new, 6600)
    net = e - memo.income_tax(e, single) + memo.eitc_2021(e, 2 * one, single)
    g_old, g_new = (net[2] + old[2]) - (net[0] + old[0]), (net[2] + new[2]) - (net[0] + new[0])
    lab.row("what working at 20k adds: old, new", f"{g_old:,.0f}, {g_new:,.0f} ({100 * (g_new / g_old - 1):+.1f}%)")
    assert g_new < g_old

    r = memo.compare(F, line_base=T["line_base"], **T["base"])
    o, n = r["old"]["child_poverty"], r["new"]["child_poverty"]
    lab.row("child poverty: old credit, no response, with responses",
            f"{100 * o:.1f}%, {100 * r['static_child_poverty']:.1f}%, {100 * n:.1f}%")
    lab.row("parents who stop working; cost per child", f"{r['exits']:.0f}; ${r['per_child']:,.0f}")
    assert r["static_child_poverty"] < n < o

    els = np.linspace(0, 0.5, 6)
    fan = [memo.compare(F, elasticity=float(x), line_base=T["line_base"]) for x in els]
    pov = np.array([f["new"]["child_poverty"] for f in fan])
    deep = np.array([f["new"]["deep"] for f in fan])
    lab.row("child poverty across the elasticity 0 to 0.5", ", ".join(f"{100 * x:.1f}%" for x in pov))
    lab.row("deep poverty across the elasticity (old credit " + f"{100 * fan[0]['old']['deep']:.1f}%)",
            ", ".join(f"{100 * x:.1f}%" for x in deep))
    assert np.all(np.diff(pov) > 0) and np.all(pov < o)

    tk = memo.compare(F, elasticity=T["base"]["elasticity"], take_up=0.85, line_base=T["line_base"])
    lab.row("take-up 85%: child poverty, cost per child",
            f"{100 * tk['new']['child_poverty']:.1f}%, ${tk['per_child']:,.0f}")

    st = T["surtax"]
    for cr in T["child_return"]:
        vals = [memo.mvpf(r["static_cost"], mc * (r["cost"] - cr * r["static_cost"]))
                for mc in [1.0] + [memo.top_mcpf(st["tau"], st["a"], x) for x in st["e"][1:]]]
        lab.row(f"value per dollar, {100 * cr:.0f}% repaid: no extra cost, surtax 0.25, surtax 0.4",
                ", ".join(f"{v:.2f}" for v in vals))

    h = memo.compare(F, line_base=T["line_base"], policy="hybrid", **T["base"])
    lab.row("second design: child poverty, deep poverty, exits, cost per child",
            f"{100 * h['new']['child_poverty']:.1f}%, {100 * h['new']['deep']:.1f}%, {h['exits']:.0f}, "
            f"${h['per_child']:,.0f}")
    assert h["per_child"] < r["per_child"] and h["exits"] < r["exits"]

    lab.note = ("The allowance adds most where the old credit gave least and removes the reward the old credit paid "
                "for starting work; on the Island it cuts child poverty by about a fifth at the central elasticity, "
                "less if parents respond more, and raises deep poverty if they respond strongly; its value per "
                "dollar is about one unless children repay part of the cost later, and below one if it is paid for "
                "by a distorting tax; keeping the work requirement for the old credit gives up a little of the "
                "poverty reduction for safety and a lower cost.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(els, 100 * pov, color=labs.ORANGE, marker="o", label="the allowance")
    ax[0].axhline(100 * o, color="grey", ls="--", label="the old credit")
    ax[0].set(title="children in poverty", xlabel="participation elasticity", ylabel="%")
    ax[0].legend()
    ax[1].plot(els, 100 * deep, color=labs.BLUE, marker="o", label="the allowance")
    ax[1].axhline(100 * fan[0]["old"]["deep"], color="grey", ls="--", label="the old credit")
    ax[1].set(title="children in deep poverty", xlabel="participation elasticity", ylabel="%")
    ax[1].legend()
    lab.fig = fig
    return lab
