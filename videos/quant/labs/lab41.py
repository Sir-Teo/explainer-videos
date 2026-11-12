"""Lab 41: a levered fund that must sell, and a network of banks that must pay each other."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import crisis

TITLE = "Spirals and contagion"
GOAL = ("Shock a levered investor's asset and iterate the forced sales: first with a fixed margin (the loss "
        "spiral), then with a margin that rises as prices fall (the margin spiral). Then shock one bank in a ring "
        "and in a complete network of interbank debts, and solve for who can pay whom.")
TASKS = [
    "Halve the market's depth. At what shock does the spiral run away?",
    "Solve the same networks with crisis.eisenberg_noe and default costs (alpha = beta = 0.7). What changes?",
    "Split the banks into two clusters (crisis.clusters_pi). Does a firebreak help against the large shock?",
]


def run(seed=0):
    shocks = np.linspace(0.005, 0.08, 16)
    loss = [crisis.spiral(s, kappa=0.0) for s in shocks]
    both = [crisis.spiral(s, kappa=2.0) for s in shocks]
    lab = labs.Lab()
    for s in (0.02, 0.05):
        i = int(np.argmin(np.abs(shocks - s)))
        lab.row(f"A {s:.0%} shock, leverage 5", f"loss spiral: price falls {100 * loss[i]['fall']:.1f}% (x{loss[i]['amplification']:.1f})   "
                                               f"with rising margins: {100 * both[i]['fall']:.1f}% (x{both[i]['amplification']:.1f})")
    # eight banks, each with a project worth a, senior outside debt v, and interbank debt y (Acemoglu et al.)
    n, a, v, y = 8, 1.0, 0.9, 2.0
    hits = np.linspace(0.05, 1.0, 20)

    def defaults(Pi):
        return [int(crisis.senior_clearing(Pi, np.full(n, y), np.full(n, a), v, np.r_[h, np.zeros(n - 1)])["default"].sum())
                for h in hits]

    ring, comp = defaults(crisis.ring_pi(n)), defaults(crisis.complete_pi(n))
    small, big = int(np.argmin(np.abs(hits - 0.5))), len(hits) - 1
    lab.row("Bank 1's project loses 0.5", f"defaults: ring {ring[small]}, complete network {comp[small]}")
    lab.row("Bank 1's project loses 1.0", f"defaults: ring {ring[big]}, complete network {comp[big]}")
    lab.row("Threshold n(a - v)", f"{n * (a - v):.1f}: below it the complete network shares the loss; above it "
                                  f"everyone fails together")
    lab.note = ("Robust yet fragile: spreading claims evenly absorbs small shocks and transmits large ones to "
                "everyone at once (Acemoglu, Ozdaglar and Tahbaz-Salehi).")
    assert all(b["fall"] >= a_["fall"] - 1e-12 for a_, b in zip(loss, both)) and both[-1]["amplification"] > 2
    assert ring[small] > comp[small] == 1 and comp[big] == ring[big] == n
    first_all = hits[int(np.argmax(np.array(comp) == n))]
    assert abs(first_all - n * (a - v)) < 0.06, "the complete network fails all at once at n(a - v)"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(100 * shocks, 100 * shocks, color=labs.MUTED, ls=":", label="the shock itself")
    ax[0].plot(100 * shocks, [100 * o["fall"] for o in loss], "o-", color=labs.P, ms=3, label="loss spiral (fixed margin)")
    ax[0].plot(100 * shocks, [100 * o["fall"] for o in both], "o-", color=labs.LOSS, ms=3, label="loss + margin spiral")
    ax[0].set(title="Total price fall after forced selling", xlabel="initial shock, %", ylabel="total fall, %")
    ax[0].legend(fontsize=8)
    ax[1].step(hits, ring, where="mid", color=labs.SPOT, label="ring: each owes the next")
    ax[1].step(hits, comp, where="mid", color=labs.OPTION, label="complete: each owes all")
    ax[1].set(title="Banks in default after one bank is hit", xlabel="loss on the first bank's project", ylabel="defaults (of 8)")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
