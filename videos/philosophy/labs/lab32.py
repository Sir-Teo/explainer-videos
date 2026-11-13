"""Lab 32: check the consequence argument's rules on models of options, replay one moment, and build a readiness potential from noise."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import freewill as fw

TITLE = "Rule beta on a coin, a rollback, and Libet's ramp from noise"
GOAL = ("Check rules alpha, beta and beta-box on McKay and Johnson's coin and on 300 random models of options, "
        "replay an undetermined moment a thousand times, and average a leaky noisy accumulator backward from the "
        "moments it crosses its threshold.")
TASKS = [
    "Give the coin a third action, 'toss a two-headed coin', leading only to heads. Which of N(no heads), "
    "N(no tails) survive, and does rule beta still fail?",
    "Set leak = 0 in fw.accumulator (a pure drift with noise). Is the backward average still a late curve, or "
    "a straight ramp?",
    "Run fw.rollback with p_truth = 0.5 and 100 replays, twenty times with different seeds. How far does the "
    "share of truths stray, and what does one replay tell you?",
]


def random_model(rng, chancy):
    """Four worlds and three actions; with chancy=False every action leads to exactly one world."""
    worlds = list(range(4))
    actions = {}
    for a in range(3):
        k = int(rng.integers(1, 4)) if chancy else 1
        actions[a] = [int(w) for w in rng.choice(4, size=k, replace=False)]
    actual = actions[0][0]
    return fw.Options(worlds, actual, actions)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    coin = fw.rule_check()
    lab.row("the coin: failures of alpha, beta, beta-box", f"{coin['alpha_fail']}, {coin['beta_fail']}, "
            f"{coin['beta_box_fail']} in {coin['pairs']} pairs   (film: 0, 2, 0 in 64)")
    lab.row("N(no heads), N(no tails), N(no heads and no tails)",
            f"{coin['N_no_heads']}, {coin['N_no_tails']}, {coin['N_both']}")
    assert (coin["alpha_fail"], coin["beta_fail"], coin["beta_box_fail"], coin["pairs"]) == (0, 2, 0, 64)
    assert coin["N_no_heads"] and coin["N_no_tails"] and not coin["N_both"], "agglomeration fails on the coin"

    tally = {}
    for chancy in (True, False):
        checks = [fw.rule_check(random_model(rng, chancy)) for _ in range(150)]
        tally[chancy] = (sum(c["alpha_fail"] for c in checks), sum(c["beta_fail"] > 0 for c in checks),
                         sum(c["beta_box_fail"] for c in checks), sum(c["agg_fail"] > 0 for c in checks))
    lab.row("150 random models with chancy actions", f"alpha fails in 0, beta-box in 0, beta in {tally[True][1]} "
            f"models, agglomeration in {tally[True][3]}")
    lab.row("150 random models, every action certain", f"beta fails in {tally[False][1]} models")
    assert tally[True][0] == tally[True][2] == tally[False][0] == tally[False][2] == 0, "alpha and beta-box are valid"
    assert tally[True][1] > 10 and tally[True][1] == tally[True][3], "beta fails exactly where agglomeration does"
    assert tally[False][1] == 0, "without chance in the outcomes, beta never fails"

    p = 0.7
    roll = fw.rollback(p_truth=p, replays=1000, seed=2000 + seed)
    share = roll["truths"] / 1000
    lab.row("rollback: truths in 1000 replays at chance 0.7", f"{roll['truths']}   (after 10 replays: "
            f"{roll['running'][3]:.2f}; three standard errors: 0.043)")
    assert abs(share - p) < 3 * np.sqrt(p * (1 - p) / 1000), "the replays settle at the chance"

    acc = fw.accumulator(trials=300, seed=2012 + seed)
    par = acc["params"]
    rest = par["drift"] / par["leak"]
    lab.row("accumulator: resting level I/k against the threshold", f"{rest:.3f} < {par['threshold']}")
    lab.row("runs that cross within 20 s, mean wait", f"{acc['crossed']} of {acc['trials']}, {acc['mean_wait']:.1f} s")
    lab.row("backward average: 2 s before, at the crossing", f"{acc['rp_start']:.3f} -> {acc['rp_end']:.3f}"
            f"   (half the rise in the last {-acc['half_rise']:.2f} s)")
    assert rest < par["threshold"] and acc["crossed"] > 0.9 * acc["trials"], "only noise carries it over, and it does"
    assert acc["rp_start"] < rest and acc["rp_end"] > 0.29, "the average climbs from below the resting level"
    assert -0.8 < acc["half_rise"] < -0.1, "and most of the climb is in the last second"
    lab.note = ("Rule beta fails only where an action's outcome is left to chance, which is where agglomeration "
                "fails; the repaired rule never fails. The ramp before each movement is what averaging noise "
                "backward from a threshold crossing looks like: nothing in the model decides.")

    fig, ax = labs.figure(3, size=(12.5, 4.2))
    ax[0].set_axisbelow(True)
    ax[0].bar(["alpha", "beta", "beta-box"], [tally[True][0], tally[True][1], tally[True][2]], width=0.55,
              color=labs.BLUE, label="outcomes left to chance")
    ax[0].bar(["alpha", "beta", "beta-box"], [tally[False][0], tally[False][1], tally[False][2]], width=0.3,
              color=labs.GOLD, label="every action certain")
    ax[0].set(title="Models where a rule fails, of 150", ylabel="models with a failing instance",
              ylim=(0, 1.4 * max(tally[True][1], 1)))
    ax[0].legend()
    ax[1].plot(np.arange(len(roll["curve"])) * 5 + 1, roll["curve"], color=labs.BLUE)
    ax[1].axhline(p, color=labs.GOLD, ls="--", label="the chance, 0.7")
    ax[1].set(title="Rollback: share of truths so far", xlabel="replays", xscale="log", ylim=(0, 1.05))
    ax[1].legend(loc="lower right")
    ax[2].plot(acc["rp_t"], acc["rp"], color=labs.GREEN, label=f"mean of {acc['averaged']} runs")
    ax[2].axhline(par["threshold"], color=labs.RED, ls=":", label="threshold")
    ax[2].axhline(rest, color=labs.MUTED, ls="--", label="resting level I/k")
    ax[2].set(title="Averaged backward from the crossing", xlabel="time before the movement (s)", ylabel="x")
    ax[2].legend(loc="lower right")
    lab.fig = fig
    return lab
