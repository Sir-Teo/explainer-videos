"""Lab 39: count one election five ways, measure how often a majority cycles, and rerun Arrow's theorem by SAT."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import vote

TITLE = "Five winners, a cycle's probability, and Arrow by machine"
GOAL = ("Count the film's 55 ballots by five rules, check on random electorates that three rules always elect a "
        "Condorcet winner while plurality and Borda do not, compare the chance of no Condorcet winner with 1/18 and "
        "Guilbaud's limit, and compare simulated juries with the binomial formula, with and without an opinion leader.")
TASKS = [
    "In the random electorates use 3 candidates instead of 5. How often do plurality and Borda now miss the "
    "Condorcet winner, and how often is there none?",
    "Call vote.arrow_models with axioms ('ORDER', 'PARETO'). How many social welfare functions are there once "
    "independence is dropped, and why does the count stop at the limit?",
    "Set follow=0.6 in the jury simulation. Where does the majority's accuracy now peak, and what does it tend to?",
]


def _random_profile(rng, voters, alts="ABCDE"):
    orders = [tuple(alts[i] for i in rng.permutation(len(alts))) for _ in range(voters)]
    return [(orders.count(o), o) for o in sorted(set(orders))]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    z = vote.zoo()
    winners = [z["plurality"]["winner"], z["runoff"]["winner"], z["irv"]["winner"], z["borda"]["winner"], z["condorcet"]]
    lab.row("55 voters: plurality, runoff, IRV, Borda, Condorcet", f"{', '.join(winners)}   (film: A, B, C, D, E)")
    assert winners == list("ABCDE") and z["voters"] == 55

    n_elections, with_cw, miss = 250, 0, {"plurality": 0, "borda": 0, "irv": 0}
    for _ in range(n_elections):
        p = _random_profile(rng, 25)
        cw = vote.condorcet_winner(p)
        if cw is None:
            assert vote.majority_cycle(p) is not None, "25 voters cannot tie, so no winner means a top cycle"
            continue
        with_cw += 1
        for rule in (vote.copeland, vote.kemeny, vote.schulze):
            assert rule(p)["winner"] == cw, f"{rule.__name__} missed the Condorcet winner"
        for name in miss:
            miss[name] += getattr(vote, name)(p)["winner"] != cw
    lab.row("random electorates with a Condorcet winner", f"{with_cw} of {n_elections}")
    lab.row("... Copeland, Kemeny, Schulze elect it", f"{with_cw} of {with_cw}   (theory: always)")
    lab.row("... plurality, Borda, IRV miss it", f"{miss['plurality']}, {miss['borda']}, {miss['irv']} times")
    assert miss["plurality"] > 0 and miss["borda"] > 0, "neither is Condorcet-consistent"

    ns = [3, 5, 7, 9, 11, 13, 15]
    exact = [vote.paradox_exact(n) for n in ns]
    sim = vote.paradox_simulated(3, n=101, trials=20000, seed=1785 + seed)
    by_m = [vote.paradox_simulated(m, n=101, trials=3000, seed=1785 + seed) for m in (3, 4, 5, 6)]
    lab.row("P(no Condorcet winner), 3 voters, 3 candidates", f"{exact[0]:.5f}   (theory: 1/18 = {1 / 18:.5f})")
    lab.row("... 101 voters, simulated", f"{sim:.4f}   (Guilbaud's limit {vote.GUILBAUD:.4f})")
    lab.row("... 3, 4, 5, 6 candidates, simulated", ", ".join(f"{x:.3f}" for x in by_m))
    assert abs(exact[0] - 1 / 18) < 1e-12 and all(a < b < vote.GUILBAUD for a, b in zip(exact, exact[1:]))
    assert abs(sim - vote.GUILBAUD) < 0.012, "101 voters are close to the limit"
    assert by_m[0] < by_m[1] < by_m[2] < by_m[3], "more candidates, more cycles"

    arrow, models = vote.arrow_sat(), vote.arrow_models()
    lab.row("Arrow, 2 voters and 3 alternatives, as SAT", f"{arrow['n_vars']} variables, {arrow['total_clauses']} clauses, "
            f"satisfiable: {arrow['satisfiable']}   (film: 108, 992, no)")
    lab.row("rules with ORDER, PARETO and IIA", f"{models['models']}, dictators {models['dictator_of_each']}")
    assert (arrow["n_vars"], arrow["total_clauses"], arrow["satisfiable"]) == (108, 992, False)
    assert len(arrow["mus"]) == 1 and len(arrow["mus"][0]) == 5 and len(arrow["mcs"]) == 5, "every axiom is needed"
    assert models["models"] == 2 and sorted(models["dictator_of_each"]) == [[1], [2]]

    p, lead, follow, juries = 0.6, 0.6, 0.3, 20000
    sizes = np.array([1, 5, 11, 21, 51, 101, 201])
    sim_ind, sim_led = [], []
    for n in sizes:
        sim_ind.append(float((rng.binomial(n, p, juries) > n / 2).mean()))
        right = rng.random(juries) < lead
        q = np.where(right, follow + (1 - follow) * p, (1 - follow) * p)
        sim_led.append(float((rng.binomial(n, q) > n / 2).mean()))
    theory = vote.jury(ps=(p,), ns=tuple(int(n) for n in sizes), leader_p=lead, follow=follow)
    th_ind, th_led = np.array(theory["independent"][str(p)]), np.array(theory["correlated"])
    lab.row("majority of 201 independent voters right", f"{sim_ind[-1]:.3f}   (theory {th_ind[-1]:.3f}; film 0.998)")
    lab.row("... when 30% follow a leader", f"{sim_led[-1]:.3f}   (theory {th_led[-1]:.3f}, stuck near the leader's 0.60)")
    assert abs(th_ind[-1] - 0.998) < 5e-4 and np.abs(np.array(sim_ind) - th_ind).max() < 0.015
    assert np.abs(np.array(sim_led) - th_led).max() < 0.015 and abs(th_led[-1] - lead) < 0.03
    lab.note = ("The rules disagree because there is often no fact for them to agree on: a majority can cycle, and "
                "Arrow's axioms leave only dictators. A crowd is wise only when its errors are independent.")

    fig, ax = labs.figure(2, size=(11.5, 4.3))
    ax[0].plot(ns, exact, "o-", color=labs.BLUE, label="exact, 3 candidates")
    ax[0].axhline(vote.GUILBAUD, color=labs.GOLD, ls="--", label="Guilbaud's limit, 8.77%")
    ax[0].axhline(1 / 18, color=labs.MUTED, ls=":", label="1/18")
    ax[0].set(title="Chance of no Condorcet winner (impartial culture)", xlabel="voters", ylabel="probability",
              ylim=(0.05, 0.092))
    ax[0].legend(loc="lower right")
    curve = vote.jury(ps=(p,), leader_p=lead, follow=follow)
    ax[1].plot(curve["ns"], curve["independent"][str(p)], color=labs.GREEN, label="independent voters, each right 60%")
    ax[1].plot(curve["ns"], curve["correlated"], color=labs.RED, label="30% follow a leader who is right 60%")
    ax[1].plot(sizes, sim_ind, "o", color=labs.GREEN, ms=5)
    ax[1].plot(sizes, sim_led, "o", color=labs.RED, ms=5, label="dots: 20,000 simulated juries")
    ax[1].set(title="Condorcet's jury theorem, and its failure", xlabel="jury size", ylabel="P(the majority is right)",
              ylim=(0.55, 1.01))
    ax[1].legend(loc="center right")
    lab.fig = fig
    return lab
