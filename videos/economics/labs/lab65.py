"""Lab 65: the economics of AI: Keynes's two forecasts on the Data Room, the task model's displacement, productivity and
new tasks, so-so automation, the J-curve, an experiment with an AI assistant, Hulten's arithmetic, growth with
automated research and its bottleneck, Baumol's two sectors, the race between automation and capital, and prices when
buyers have shopping agents."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import automation as A

TITLE = "The economics of AI"
GOAL = ("Work through what automation does to wages, labour's share and growth in the task model and its growth "
        "version, turn a task-level experiment into an aggregate number, and check Keynes's 1930 forecasts.")
TASKS = [
    "Make tasks substitutes rather than complements in the research model (A.ideas_growth(0.9, sigma=0.8)). Does "
    "growth still fall back?",
    "Let machines be barely cheaper than people (A.tasks(0.6, R=1.1) against A.tasks(0.5, R=1.1)). What happens to the "
    "wage and labour's share?",
    "Put Eloundou et al.'s exposure into Hulten's arithmetic with adoption of one half (A.hulten_ai(0.2, 0.5)). How "
    "far is it from Acemoglu's number?",
]


def run(seed=0):
    lab = labs.Lab()
    K = A.keynes()
    assert all(4.0 < v < 8.0 for v in K["ratio"].values())       # inside Keynes's four to eight
    lab.row("Keynes: GDP per head in 2022 against 1930 (six countries)",
            ", ".join(f"{c} {v:.1f}" for c, v in sorted(K["ratio"].items(), key=lambda kv: kv[1])))
    hrs = {c: h["hours"][-1] for c, h in K["hours"].items()}
    lab.row("hours worked a year per worker, latest (Keynes's week: 780)",
            ", ".join(f"{c} {v:,.0f}" for c, v in sorted(hrs.items(), key=lambda kv: kv[1])))
    T = A.task_paths()
    assert abs(T["displacement"] + T["productivity"] - T["dlnw"]) < 1e-9   # the wage decomposes exactly
    lab.row("the task model, capital fixed: displacement, productivity, net change in the log wage (x100)",
            f"{100 * T['displacement']:.0f}, +{100 * T['productivity']:.0f}, {100 * T['dlnw']:.0f}")
    lab.row("long run: labour's share as automation rises; then with new tasks",
            f"{T['long']['labour_share'][0]:.2f} to {T['long']['labour_share'][-1]:.2f}; back to "
            f"{T['new_tasks']['labour_share'][-1]:.2f}")
    S = A.so_so()["rows"]
    lab.row("so-so automation: the wage gain from automating 10% more tasks, cheap and dear machines",
            f"{100 * S[0]['wage_gain']:.0f}% and {100 * S[-1]['wage_gain']:.0f}%")
    J = A.j_curve()
    lab.row("the J-curve: measured productivity at its low and at the end; the truth at the end",
            f"{J['low']:.3f} (year {J['low_year']}), {J['end']:.3f}; {J['end_true']:.3f}")
    D = A.support_desk(seed=65 + seed)
    assert D["fifths"][0]["est"] > D["fifths"][-1]["est"]               # the least skilled gain most
    lab.row("the support desk: the assistant's average effect (95% interval); bottom and top fifths",
            f"{100 * D['est']:.0f}% ({100 * D['lo']:.0f} to {100 * D['hi']:.0f}); {100 * D['fifths'][0]['est']:.0f}% "
            f"and {100 * D['fifths'][-1]['est']:.0f}%")
    H = A.hulten_scenarios()["rows"]
    lab.row("Hulten's arithmetic: TFP after ten years under three readings",
            ", ".join(f"{r['name']} {100 * r['tfp']:.2f}%" for r in H))
    G = {b: A.ideas_growth(b) for b in (0.0, 0.5, 0.9, 1.0)}
    assert G[1.0]["exploded"] and not G[0.9]["exploded"]                 # only full automation explodes
    lab.row("growth with automated research: peak and year 100 (or the year it explodes)",
            "; ".join(f"{100 * b:.0f}%: {100 * max(g['growth']):.1f}% / "
                      + (f"explodes in year {g['year'][-1]}" if g["exploded"] else f"{100 * g['growth'][100]:.1f}%")
                      for b, g in G.items()))
    B = A.baumol()
    lab.row("Baumol: aggregate growth at the start and after a century", f"{100 * B['growth'][0]:.2f}% and "
            f"{100 * B['growth'][-1]:.2f}%")
    R = A.race_scenarios()
    lab.row("the race: the wage after sixty years, by scenario", ", ".join(f"{k} {v['w'][-1]:.2f}"
                                                                         for k, v in R.items()))
    V = A.shoppers()["rows"]
    assert all(abs(r["average_paid"] - (0.4 + 0.6 * (1 - r["mu"]))) < 2e-3 for r in V)   # c + (1 - mu)(v - c)
    lab.row("Varian's shoppers: the average price paid with 2%, 50% and 98% of buyers using agents",
            ", ".join(f"{r['average_paid']:.3f}" for r in (V[0], V[24], V[-1])))

    lab.note = ("Tasks are complements: what the machines cannot do sets the pace, and the wage. The aggregate number "
                "depends far more on adoption than on any experiment.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for b, g in G.items():
        ax[0].plot(g["year"], np.minimum(100 * np.array(g["growth"]), 30), label=f"{100 * b:.0f}% automated")
    ax[0].set(title="growth with automated research", xlabel="years", ylabel="% a year (capped at 30)")
    ax[0].legend(fontsize=8)
    for k, v in R.items():
        ax[1].plot(v["year"], v["w"], label=k)
    ax[1].set(title="the race: wages", xlabel="years", ylabel="the wage")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
