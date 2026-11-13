"""Lab 38: choose a society behind the veil at every risk attitude, and divide a cake three ways without envy."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import justice

TITLE = "Behind the veil, and a cake for three"
GOAL = ("Draw two hundred societies and let a chooser who could be anyone pick one by the average, by maximin and by "
        "expected CRRA utility as the risk aversion eta grows. Then run Selfridge-Conway on forty random triples of "
        "valuations and check that nobody ever envies anybody, and recheck Sen's paradox and the rent division.")
TASKS = [
    "Call justice.veil with classes=2 and then classes=20. Does the eta at which the chooser reaches the maximin "
    "society go up or down, and why?",
    "Give two of the three cake eaters the same valuation in justice.selfridge_conway. Is the division still "
    "envy-free, and who now values their own bundle at exactly one third?",
    "Check that rents (1400, 900, 700) are also envy-free for the film's housemates, then find by hand a price "
    "vector that sums to 3000 and is not.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    etas = [0, 0.5, 1, 2, 3, 5, 8, 12, 20, 80]
    v = justice.veil(seed=1971 + seed, etas=etas)
    path = v["by_eta"]
    lab.row("average chooser: (average, least income)", f"({v['avg']['average']:.1f}, {v['avg']['minimum']:.1f})")
    lab.row("maximin chooser: (average, least income)", f"({v['maximin']['average']:.1f}, {v['maximin']['minimum']:.1f})")
    mid = next(p for p in path if p["eta"] == 2)
    lab.row("CRRA chooser at eta = 2", f"({mid['average']:.1f}, {mid['minimum']:.1f})")
    first_max = next((p["eta"] for p in path if p["choice"] == v["maximin_choice"]), None)
    lab.row("least eta tried that picks the maximin society", f"{first_max}   (film, seed 0: 8)")
    assert path[0]["choice"] == v["avg_choice"], "eta = 0 is risk neutrality: Harsanyi's average"
    assert path[-1]["minimum"] >= 0.95 * v["maximin"]["minimum"], "large eta approaches maximin"
    assert path[-1]["minimum"] > path[0]["minimum"] and path[-1]["average"] <= path[0]["average"]
    assert v["maximin"]["minimum"] > v["avg"]["minimum"] and v["maximin"]["average"] < v["avg"]["average"]
    if seed == 0:
        assert first_max == 8 and len({p["choice"] for p in path if 0.5 <= p["eta"] <= 5}) == 1

    dp = justice.difference_principle()["points"]
    assert (dp["difference"]["uA"], dp["difference"]["uL"]) == (8.0, 6.0)
    assert (dp["utilitarian"]["uA"], dp["utilitarian"]["uL"]) == (12.5, 3.75)

    worst, n_cakes = np.inf, 40
    for _ in range(n_cakes):
        r = justice.selfridge_conway(rng.uniform(0.2, 3.0, (3, 10)).tolist())
        w = np.array(r["worth"])
        assert r["envy_free"], f"envy with valuations {r['densities']}"
        assert abs(w.sum(axis=1) - 1).max() < 1e-3, "the bundles are the whole cake"
        worst = min(worst, float((np.diag(w)[:, None] - w).min()))
        assert np.diag(w).min() > 1 / 3 - 1e-3, "envy-freeness implies a proportional share"
    lab.row(f"Selfridge-Conway on {n_cakes} random cakes", f"envy in 0 of {n_cakes}   (theory: never)")
    lab.row("smallest margin, own bundle minus another's", f"{worst:+.4f}   (theory: at least 0)")

    sen = justice.liberal_paradox()
    lab.row("assignments of two rights forced into a cycle", f"{sum(bool(r['profile']) for r in sen['results'])} of "
            f"{sen['pairs_checked']}   (Sen: all)")
    assert sen["pairs_checked"] == 6 and sen["all_cycle"]

    rent = justice.rent_division()
    V, p = np.array(rent["values"]), np.array(rent["prices"])
    surplus = V - p
    lab.row("envy-free rents", f"{', '.join(f'{x:.0f}' for x in p)}   least surplus {rent['min_utility']:.0f}   (film: 1330, 935, 735)")
    assert list(p) == [1330.0, 935.0, 735.0] and abs(p.sum() - 3000) < 1e-9
    assert all(surplus[i, rent["assign"][i]] >= surplus[i].max() - 1e-9 for i in range(3)), "no envy at these rents"
    alt = V - np.array([1400.0, 900.0, 700.0])  # problem 5: also envy-free, but a smaller least surplus
    assert all(alt[i, i] >= alt[i].max() for i in range(3)) and np.diag(alt).min() == 100 < rent["min_utility"]
    lab.note = ("Rawls's and Harsanyi's choosers are the two ends of one dial, the risk aversion: the disagreement "
                "is about eta, not about the veil. And envy-freeness for three is a procedure, not a hope: it "
                "holds for every valuation tried.")

    fig, ax = labs.figure(2, size=(11.5, 4.3))
    pts = np.array(v["points"])
    ax[0].scatter(pts[:, 0], pts[:, 1], s=9, color=labs.MUTED, alpha=0.6, label="200 societies")
    ax[0].plot([q["average"] for q in path], [q["minimum"] for q in path], "-o", color=labs.GOLD, ms=4,
               label="CRRA choice as eta goes 0 to 80")
    ax[0].scatter(*[v["avg"][k] for k in ("average", "minimum")], s=90, color=labs.RED, zorder=3, label="average (Harsanyi)")
    ax[0].scatter(*[v["maximin"][k] for k in ("average", "minimum")], s=90, color=labs.GREEN, zorder=3, label="maximin (Rawls)")
    ax[0].set(title="Behind the veil: which society?", xlabel="average income", ylabel="least income")
    ax[0].legend(loc="upper left")
    film = np.array(justice.selfridge_conway()["worth"], float)
    x = np.arange(3)
    for j, color in enumerate((labs.BLUE, labs.PURPLE, labs.TEAL)):
        ax[1].bar(x + (j - 1) * 0.26, film[:, j], 0.24, color=color, label=f"bundle of person {j + 1}")
    for i in range(3):
        ax[1].plot(i + (i - 1) * 0.26, film[i, i] + 0.02, "v", color=labs.GOLD, ms=7)
    ax[1].set_axisbelow(True)
    ax[1].axhline(1 / 3, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="Selfridge-Conway: each values their own bundle most", xticks=x,
              xticklabels=["person 1 judges", "person 2 judges", "person 3 judges"], ylabel="value of the bundle",
              ylim=(0, 0.62))
    ax[1].legend(ncol=3, loc="upper center")
    lab.fig = fig
    return lab
