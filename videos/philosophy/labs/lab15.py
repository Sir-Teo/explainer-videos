"""Lab 15: average every learner over all 256 worlds on three bits (no free lunch), then over smooth worlds only."""

import itertools

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import induction as Ind

TITLE = "No free lunch, by brute force, and Laplace's rule by simulation"
GOAL = ("Score the Reasoner's four learners, and twenty learners drawn at random, on the unseen inputs of every "
        "one of the 256 labellings of three bits: each must average exactly one half. Then restrict the worlds to "
        "smooth ones, where the learners separate. Finally check Laplace's (s + 1)/(n + 2) against simulated coins "
        "whose chance is drawn uniformly.")
TASKS = [
    "Weight the 256 worlds unevenly, for example in proportion to 2 to the minus (number of label changes along "
    "the inputs in order), and find which learner now wins.",
    "Draw the coins' chances from Beta(5, 5) instead of the uniform prior. Which member of Carnap's continuum, "
    "(s + lambda/2)/(n + lambda), now matches the simulated frequencies?",
    "Add a fifth method to Ind.meta_induction's world in a copy of the function and check that the regret stays "
    "below sqrt(T ln N / 2).",
]


def random_learner_accuracy(rng, n_bits=3):
    """A learner is any map from the four training labels to four test predictions: draw one at random and average
    its off-training-set accuracy over all 2^8 worlds."""
    table = {tr: rng.integers(0, 2, 4) for tr in itertools.product([0, 1], repeat=4)}
    total = 0.0
    for f in itertools.product([0, 1], repeat=2 ** n_bits):
        train, test = f[::2], np.array(f[1::2])
        total += np.mean(table[train] == test)
    return total / 2 ** (2 ** n_bits)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    nfl = Ind.no_free_lunch()
    smooth = Ind.smooth_world_lunch()
    assert nfl["targets"] == 256
    for name, acc in nfl["accuracy"].items():
        assert abs(acc - 0.5) < 1e-12, f"{name}: exactly one half over all worlds"
        lab.row(f"{name}: all 256 worlds, smooth worlds", f"{acc:.3f}   {smooth['accuracy'][name]:.3f}")
    assert smooth["accuracy"]["nearest neighbour"] == 1.0 and smooth["accuracy"]["anti-majority"] < 0.5
    rand = [random_learner_accuracy(rng) for _ in range(20)]
    assert max(abs(a - 0.5) for a in rand) < 1e-12, "any learner at all averages one half"
    lab.row("20 random learners: all 256 worlds", f"min {min(rand):.3f}   max {max(rand):.3f}   (theory 0.500)")
    sl = Ind.nfl_slice()
    assert all(c == len(sl["completions"]) // 2 for c in sl["correct"]), "half the consistent worlds agree"
    lab.row("worlds consistent with 4 labels; right per unseen input", f"{len(sl['completions'])}; {sl['correct']}")

    # Laplace: chance uniform on [0, 1], n tosses with s heads; how often is toss n + 1 a head?
    n, reps = 10, 400_000
    theta = rng.uniform(0, 1, reps)
    s = rng.binomial(n, theta)
    nxt = rng.uniform(0, 1, reps) < theta
    freq = np.array([nxt[s == k].mean() for k in range(n + 1)])
    rule = np.array([float(Ind.succession(k, n)) for k in range(n + 1)])
    straight = np.arange(n + 1) / n
    assert np.max(np.abs(freq - rule)) < 0.015, "Laplace's rule matches a uniform prior"
    assert np.max(np.abs(freq - straight)) > 0.05, "and the straight rule does not"
    lab.row("after 9 heads in 10: simulated, Laplace, straight rule", f"{freq[9]:.3f}   {rule[9]:.3f}   {straight[9]:.3f}")
    lab.row("largest gap, simulated vs (s+1)/(n+2), s = 0..10", f"{np.max(np.abs(freq - rule)):.4f}   (theory 0)")
    lab.note = ("Averaged over every possible world no learner beats any other on unseen inputs, so success "
                "belongs to the match between a learner's bias and the world; Laplace's rule is exactly right in "
                "the one world its uniform prior describes.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = list(nfl["accuracy"])
    x = np.arange(len(names))
    ax[0].bar(x - 0.2, [nfl["accuracy"][k] for k in names], 0.4, color=labs.BLUE, label="all 256 worlds")
    ax[0].bar(x + 0.2, [smooth["accuracy"][k] for k in names], 0.4, color=labs.GOLD,
              label="smooth worlds (label depends on bit 1 at most)")
    ax[0].axhline(0.5, color=labs.MUTED, ls="--", lw=1)
    ax[0].set_axisbelow(True)
    ax[0].set_xticks(x, [k.replace(" ", "\n") for k in names])
    ax[0].set(title="Accuracy on unseen inputs", ylabel="average accuracy off the training set", ylim=(0, 1.25))
    ax[0].legend(loc="upper left")
    k = np.arange(n + 1)
    ax[1].plot(k, rule, color=labs.GOLD, label="Laplace: (s + 1)/(n + 2)")
    ax[1].plot(k, straight, color=labs.MUTED, ls="--", label="straight rule: s/n")
    ax[1].scatter(k, freq, s=28, color=labs.BLUE, zorder=3, label="simulated, chance uniform on [0, 1]")
    ax[1].set(title="Is toss 11 a head, after s heads in 10?", xlabel="heads s in the first 10 tosses",
              ylabel="frequency of a head on toss 11")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
