"""Lab 2: three exact answers from the probability engine, each checked against a seeded simulation."""

from fractions import Fraction
from functools import lru_cache

import numpy as np

from videos.coursekit import labs
from explainer.stats.prob import Dist, coin

TITLE = "Exact answers, checked by simulation"
GOAL = ("Solve the problem of points by Fermat's enumeration and by Pascal's recursion, a screening test by Bayes' "
        "theorem, and Monty Hall under a host who prefers one door, exactly as fractions; then simulate each and "
        "see the frequencies settle on the fractions.")
TASKS = [
    "Change the interrupted score so that A needs 2 points and B needs 3. What is A's fair share of the 64 pistoles?",
    "Lower the test's specificity from 19/20 to 9/10. What happens to the chance of the condition given a positive?",
    "Make the host open a door at random, without knowing where the car is, and condition on his showing a goat. "
    "What does switching win now?",
]

SENS, SPEC = Fraction(9, 10), Fraction(19, 20)


def fermat(a: int, b: int) -> Fraction:
    """A needs a points, B needs b: play all a + b - 1 remaining fair rounds and count the futures A wins."""
    rounds = coin() ** (a + b - 1)
    return rounds.P(lambda r: r.count("H") >= a)


@lru_cache(maxsize=None)
def pascal(a: int, b: int) -> Fraction:
    """A's share by backward recursion: the average of the two scores one round ahead."""
    if a == 0:
        return Fraction(1)
    if b == 0:
        return Fraction(0)
    return (pascal(a - 1, b) + pascal(a, b - 1)) / 2


def screening(prev: Fraction) -> Dist:
    """The two-stage tree: the condition, then the test result given the condition."""
    return coin(prev, "sick", "well").then(lambda s: coin(SENS if s == "sick" else 1 - SPEC, "+", "-"))


def posterior(prev: Fraction) -> Fraction:
    return screening(prev).given(lambda o: o[1] == "+").P(lambda o: o[0] == "sick")


def monty(q: Fraction) -> Fraction:
    """You pick door 1; the host knows, never shows the car, and opens door 3 with probability q when he may open
    either.  The chance the car is behind door 2 given that he opened door 3."""
    def host(car):
        return {1: Dist({3: q, 2: 1 - q}), 2: Dist({3: 1}), 3: Dist({2: 1})}[car]
    game = Dist.uniform([1, 2, 3]).then(host)
    return game.given(lambda o: o[1] == 3).P(lambda o: o[0] == 2)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. The problem of points: two roads to one answer, for every score of a short game.
    share = fermat(1, 2)
    assert share == pascal(1, 2) == Fraction(3, 4)
    assert all(fermat(a, b) == pascal(a, b) for a in range(1, 6) for b in range(1, 6)), "Fermat and Pascal agree"
    n_games = 10_000
    tosses = rng.random((n_games, 2)) < 0.5  # True: A wins the round.  A needs one of the next two rounds.
    a_wins = tosses.any(1)
    freq = a_wins.mean()
    lab.row("problem of points at 2-1: A's share", f"{share} = {float(share):.4f}   simulated {freq:.4f} ({n_games:,} games)")
    lab.row("A's fair stake of 64 pistoles", f"{64 * share}")
    assert abs(freq - 0.75) < 4 * np.sqrt(0.75 * 0.25 / n_games)

    # 2. The screening test: one adult in a hundred has the condition.
    prev = Fraction(1, 100)
    post = posterior(prev)
    odds = prev / (1 - prev) * SENS / (1 - SPEC)  # prior odds times the likelihood ratio, 18
    assert post == odds / (1 + odds) == Fraction(2, 13), "the tree and the odds form give the same posterior"
    odds2 = odds * SENS / (1 - SPEC)
    post2 = odds2 / (1 + odds2)
    n_people = 400_000
    sick = rng.random(n_people) < float(prev)
    positive = np.where(sick, rng.random(n_people) < float(SENS), rng.random(n_people) < float(1 - SPEC))
    sim_post = sick[positive].mean()
    lab.row("P(condition | positive)", f"{post} = {float(post):.4f}   simulated {sim_post:.4f}   (P(positive | condition) = 0.9)")
    lab.row("after a second, independent positive", f"{post2} = {float(post2):.4f}")
    assert abs(sim_post - float(post)) < 4 * np.sqrt(float(post) * (1 - float(post)) / positive.sum())

    # 3. Monty Hall: the host's protocol is part of the data.
    for q in (Fraction(1, 2), Fraction(1), Fraction(0)):
        assert monty(q) == 1 / (1 + q)
    n_shows = 30_000
    car = rng.integers(1, 4, n_shows)
    q = 0.5
    opened = np.where(car == 1, np.where(rng.random(n_shows) < q, 3, 2), np.where(car == 2, 3, 2))
    saw3 = opened == 3
    sim_switch = (car[saw3] == 2).mean()
    lab.row("Monty Hall, fair host: switching wins", f"{monty(Fraction(1, 2))} = {float(monty(Fraction(1, 2))):.4f}   simulated {sim_switch:.4f}")
    lab.row("host always opens door 3 if he can", f"{monty(Fraction(1))}   (1 / (1 + q) with q = 1)")
    assert abs(sim_switch - 2 / 3) < 4 * np.sqrt(2 / 9 / saw3.sum())
    lab.note = ("Each fraction is the exact value of its model, and each simulated frequency lands within the noise "
                "of a finite experiment; 0.9 and 2/13 are different conditionals of the same test.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    k = np.arange(1, n_games + 1)
    ax[0].plot(k, np.cumsum(a_wins) / k, color=labs.BLUE, label="fraction of games A wins")
    ax[0].axhline(0.75, color=labs.GOLD, ls="--", label="Fermat and Pascal: 3/4")
    band = 2 * np.sqrt(0.75 * 0.25 / k)
    ax[0].fill_between(k, 0.75 - band, 0.75 + band, color=labs.GOLD, alpha=0.12, label="3/4 plus or minus 2 SE")
    ax[0].set(xscale="log", ylim=(0.5, 1.0), title="The problem of points, played out from 2-1",
              xlabel="simulated games", ylabel="running fraction")
    ax[0].legend(loc="upper right")
    prevs = np.logspace(-3, np.log10(0.5), 80)
    lr = float(SENS / (1 - SPEC))
    one = prevs * lr / (prevs * lr + 1 - prevs)
    two = prevs * lr ** 2 / (prevs * lr ** 2 + 1 - prevs)
    ax[1].plot(prevs, one, color=labs.GOLD, label="after one positive test")
    ax[1].plot(prevs, two, color=labs.PURPLE, label="after two independent positives")
    ax[1].axhline(float(SENS), color=labs.MUTED, ls=":", label="P(positive | condition) = 0.9")
    sim_prev = np.array([0.002, 0.01, 0.05, 0.2])
    sims = []
    for pv in sim_prev:
        s = rng.random(100_000) < pv
        pos = np.where(s, rng.random(100_000) < float(SENS), rng.random(100_000) < float(1 - SPEC))
        sims.append(s[pos].mean())
    ax[1].plot(sim_prev, sims, "o", color=labs.BLUE, ms=5, label="simulated, 100,000 people each")
    ax[1].set(xscale="log", title="What a positive test means depends on the prior", xlabel="prevalence of the condition",
              ylabel="P(condition | positive)")
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
