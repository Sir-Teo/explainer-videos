"""Lab 19: run Hamilton's rule on four kinds of kin and check it against the Price covariance."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import evo as Ev

TITLE = "Hamilton's rule, simulated and derived from Price"
GOAL = ("Simulate altruism between relatives for sixty generations and compare which way it goes with the sign of "
        "rb - c; then compute Price's covariance exactly for the same model and check it equals p(1-p)(rb - c).")
TASKS = [
    "Set the cousins' benefit to exactly eight times the cost (b = 0.8). What does the trajectory do, and why?",
    "Replace the relatedness values by Ev.relatedness('daughter', 'son', True): can a worker bee afford to raise "
    "brothers at b = 3c?",
    "Call Ev.multilevel() with groups ((10, 1), (10, 9)) and find a cost c at which the between-group term no "
    "longer outweighs the within-group term.",
]

CASES = [("siblings, b = 3c", 0.5, 0.3), ("half-siblings, b = 3c", 0.25, 0.3),
         ("cousins, b = 10c", 0.125, 1.0), ("cousins, b = 6c", 0.125, 0.6)]
COST = 0.1


def run(seed=0):
    lab = labs.Lab()
    sims = []
    for name, r, b in CASES:
        sim = Ev.hamilton_sim(r, b, COST, seed=seed)
        sims.append(sim)
        rose = sim["traj"][-1] > sim["traj"][0]
        lab.row(name, f"rb - c = {sim['rb_minus_c']:+.4f}   altruists 0.20 -> {sim['traj'][-1]:.2f}")
        assert rose == (sim["rb_minus_c"] > 0), f"{name}: the sign of rb - c decides the direction"

    # Price's covariance for the pairing model, by enumeration, against p(1-p)(rb - c) on a grid of (r, b, p)
    rng = np.random.default_rng(seed)
    xs, ys = [], []
    for _ in range(200):
        r, b, c, p = rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 0.5), rng.uniform(0.05, 0.95)
        h = Ev.hamilton_from_price(r, b, c, p)
        xs.append(p * (1 - p) * (r * b - c))
        ys.append(h["cov"])
        assert abs(h["cov"] - h["formula"]) < 1e-12, "Cov(w, z) = p(1-p)(rb - c)"
        assert (h["cov"] > 0) == (r * b > c), "selection favours altruism iff rb > c"
    lab.row("Price covariance vs p(1-p)(rb - c)", f"max gap {max(abs(np.array(xs) - np.array(ys))):.1e} on 200 random models")

    birds = Ev.price_check(seed=seed)
    lab.row("Price identity on 500 birds", f"change {birds['delta']:+.3f} = selection {birds['selection']:+.3f} "
            f"+ transmission {birds['transmission']:+.3f}")
    assert birds["identity_error"] < 1e-12, "the Price equation is an identity"
    assert birds["selection"] > 0 > birds["transmission"]

    table = Ev.relatedness_table()["rows"]
    lab.row("haplodiploid sisters", f"r = {table['sister to sister (haplodiploid)']:.2f}   (theory 3/4)")
    assert abs(table["sister to sister (haplodiploid)"] - 0.75) < 1e-12
    lab.note = ("The direction of every run is the sign of rb - c, because Price's covariance between carrying the "
                "gene and fitness is p(1-p)(rb - c) exactly.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for (name, _, _), sim, color in zip(CASES, sims, labs.CYCLE):
        ax[0].plot(sim["traj"], color=color, label=f"{name}: rb - c = {sim['rb_minus_c']:+.3f}")
    ax[0].set(title="Altruism over sixty generations (4,000 pairs)", xlabel="generation",
              ylabel="share of altruists", ylim=(-0.02, 1.02))
    ax[0].legend(loc="upper left")
    xs, ys = np.array(xs), np.array(ys)
    ax[1].scatter(xs, ys, s=12, c=np.where(xs > 0, labs.GREEN, labs.RED))
    lim = [xs.min(), xs.max()]
    ax[1].plot(lim, lim, color=labs.MUTED, ls="--", lw=1, label="equal")
    ax[1].axvline(0, color=labs.GRID)
    ax[1].axhline(0, color=labs.GRID)
    ax[1].set(title="Price's covariance, enumerated, against the formula", xlabel="p(1-p)(rb - c)",
              ylabel="Cov(w, z) by enumeration")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
