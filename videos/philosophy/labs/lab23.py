"""Lab 23: check the modal ontological argument on every small frame, and Hume's maxim on simulated witnesses."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import theism

TITLE = "Proofs on frames, miracles by witnesses"
GOAL = ("Count the frames on which Plantinga's argument and its mirror image are valid, search the finite models of "
        "Gödel's and Scott's axioms, and simulate a rare event reported by one to five witnesses, independent or "
        "copying one another, against the Bayesian formula.")
TASKS = [
    "Make the witnesses less reliable (HIT = 0.8, FALSE = 0.2). How many independent witnesses does a "
    "one-in-a-thousand event now need to pass one half?",
    "Call theism.plantinga(max_worlds=4) and check whether the argument is still valid on exactly the S5 frames.",
    "Set COPY = 0.5, so that half of the later witnesses repeat the first. Derive the likelihood ratio of k reports "
    "and compare it with the simulation.",
]

PRIOR, HIT, FALSE, COPY = 1e-3, 0.9, 0.1, 1.0


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    frames = theism.plantinga()
    arg = {s: frames[s]["argument"] for s in frames}
    lab.row("argument valid on S5 / S4 / T frames", " / ".join(f"{arg[s]['valid_on']} of {arg[s]['frames']}"
                                                                for s in ("S5", "S4", "T")) + "   (film: 8 of 8, 8 of 34)")
    assert arg["S5"] == {"frames": 8, "valid_on": 8} and arg["S4"] == {"frames": 34, "valid_on": 8}
    assert frames["S5"]["mirror"]["valid_on"] == 8, "the mirror image is valid wherever the argument is"
    assert frames["B"]["conclusion"]["valid_on"] == frames["B"]["conclusion"]["frames"], "the conclusion needs only B"

    g = theism.godel()
    n_godel = sum(r["models"] for r in g["godel"])
    scott = [r for r in g["scott"] if r["models"]]
    lab.row("models of Gödel's own axioms", f"{n_godel} among {sum(r['candidates'] for r in g['godel'])} candidates")
    lab.row("models of Scott's axioms", f"{sum(r['models'] for r in scott)}, all with "
            f"{max(r['worlds'] for r in scott)} world and one God")
    assert n_godel == 0, "Gödel's axioms are inconsistent"
    assert scott and all(r["worlds"] == 1 and r["collapse"] == r["models"] == r["one_god"] for r in scott), "modal collapse"

    # Hume: a rare event, k witnesses; every world in which all k report, and the share of those where it happened
    n, ks = 3_000_000, np.arange(1, 6)
    happened = rng.random(n) < PRIOR
    rate = np.where(happened, HIT, FALSE)
    reports = rng.random((5, n)) < rate
    all_report = np.cumprod(reports, axis=0).astype(bool)
    sim = np.array([happened[all_report[k - 1]].mean() for k in ks])
    exact = np.array([r["posterior"] for r in theism.hume(PRIOR, HIT, FALSE, 5)["rows"]][1:])
    first = reports[0]
    copied = np.where(rng.random((4, n)) < COPY, first, reports[1:])
    all_copied = np.vstack([first, copied]).all(axis=0)
    sim_copy = happened[all_copied].mean()
    for k in (1, 3, 4):
        lab.row(f"{k} independent witness{'es' if k > 1 else ''}", f"{sim[k - 1]:.4f}   (formula {exact[k - 1]:.4f})")
    lab.row("5 witnesses copying the first", f"{sim_copy:.4f}   (one witness: {exact[0]:.4f})")
    assert np.all(np.abs(sim - exact) < 0.03), "the simulation matches Bayes's rule"
    assert abs(sim[0] - exact[0]) < 0.002 and abs(sim_copy - exact[0]) < 0.002, "copied testimony adds nothing"
    assert exact[2] < 0.5 < exact[3]
    film = theism.hume()
    assert film["first_over_half"] == 4 and abs(film["rows"][1]["posterior"] - 1e-4) < 2e-6
    lab.note = ("The modal argument is exactly as strong as S5 and proves its mirror image as well; and testimony "
                "overcomes a tiny prior only when the witnesses are independent, since copies multiply nothing.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    systems = ["S5", "B", "S4", "T"]
    x = np.arange(4)
    ax[0].bar(x - 0.2, [arg[s]["frames"] for s in systems], 0.4, color=labs.GREY, label="reflexive frames, up to 3 worlds")
    ax[0].bar(x + 0.2, [arg[s]["valid_on"] for s in systems], 0.4, color=labs.GOLD, label="argument valid")
    ax[0].set_xticks(x, systems)
    ax[0].set(title="Possibly necessarily g, so necessarily g: where it is valid", ylabel="frames")
    ax[0].legend()
    k6 = np.arange(0, 7)
    ax[1].plot(k6, [r["posterior"] for r in film["rows"]], "o-", color=labs.PURPLE,
               label="formula, prior one in a million, 99% reliable")
    ax[1].plot(np.r_[0, ks], np.r_[PRIOR, exact], "-", color=labs.BLUE, label="formula, prior one in a thousand, 90% reliable")
    ax[1].plot(ks, sim, "o", color=labs.BLUE, label="simulated, independent witnesses")
    ax[1].plot([5], [sim_copy], "s", color=labs.RED, label="simulated, five who copy the first")
    ax[1].axhline(0.5, color=labs.MUTED, ls=":", lw=0.9)
    ax[1].set(title="Probability the event happened, given k reports", xlabel="witnesses k", ylabel="posterior",
              ylim=(-0.04, 1.5), yticks=np.linspace(0, 1, 6))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
