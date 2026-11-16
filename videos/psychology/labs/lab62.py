"""Lab 62: the dissertation: the registered report rerun, its design check, and the Ledger by act."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import ledger, opendata
from explainer.psychology.psyche import thesis as Th

TITLE = "The Dissertation"
GOAL = ("Rerun the registered report on Ganis and Kievit's open data, check what the design could decide, and read "
        "the complete Ledger by act.")
TASKS = [
    "Apply the registered minimum (4 trials per cell) and confirm that it excludes everyone. What rule would you "
    "have registered instead?",
    "Split the trials into first and second halves instead of odd and even. Does the reliability change? Why might it?",
    "Run the design check with 160 people. How often is a true reliability of 0.6 now decided?",
]


def run(seed=0):
    out = labs.Lab()
    assert Th.plan_hash().startswith("1ee2fa7b")
    out.row("the registered plan's SHA-256", Th.plan_hash()[:16] + "...")
    if opendata.available("ganis_kievit_2015"):
        d = opendata.mental_rotation()
        h = Th.person_halves(d, min_per_cell=Th.DEVIATION["used_min_per_cell"])
        r = Th.analyse(h, boots=2000, seed=62)
        out.row("people kept; slope reliability (95% interval)",
                f"{r['n']}; {r['slope_rel']:.2f} ({r['slope_ci'][0]:.2f} to {r['slope_ci'][1]:.2f})")
        out.row("mean-time reliability", f"{r['mean_rel']:.2f}")
        out.row("verdict", ", ".join(f"{k} {v}" for k, v in Th.verdict(r).items()))
        so, se = h["slope_odd"], h["slope_even"]
    else:
        out.row("open data", "not cached here; the design check runs on simulated people")
        hh = Th.simulate_halves(true_rel=0.74, seed=seed)
        so, se = hh["slope_odd"], hh["slope_even"]
    p = Th.power(true_rels=(0.4, 0.7, 0.85), reps=60, seed=seed)
    out.row("design check: supported / inconclusive / refuted at 0.4, 0.7, 0.85",
            "; ".join("/".join(f"{x:.2f}" for x in row) for row in p["table"]))
    b = Th.ledger_by_act(ledger.rows())
    held = b["table"][:, 0].sum()
    out.row("Ledger rows held / total", f"{held} / {b['table'].sum()}")

    out.note = ("A registered report decides what the data can decide, reports what changed, and ends with a row "
                "that the next study will settle.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].scatter(so, se, s=14)
    lim = [min(so.min(), se.min()), max(so.max(), se.max())]
    ax[0].plot(lim, lim, color="grey", lw=0.8)
    ax[0].set(title="slopes: odd against even trials", xlabel="odd (ms/deg)", ylabel="even (ms/deg)")
    frac = b["table"] / b["table"].sum(1, keepdims=True)
    bottom = np.zeros(len(b["acts"]))
    for j, g in enumerate(b["groups"]):
        ax[1].bar(b["acts"], frac[:, j], bottom=bottom, label=g)
        bottom += frac[:, j]
    ax[1].set(title="the Ledger by act", ylabel="share of rows")
    ax[1].legend(fontsize=7)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
