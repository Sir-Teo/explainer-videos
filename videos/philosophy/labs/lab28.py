"""Lab 28: compute what 'some' conveys with the Rational Speech Acts model, and grow a convention from reward."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import pragmatics as pr

TITLE = "Some, not all; and a convention from nothing"
GOAL = ("Run the Rational Speech Acts model on the cookie game for random numbers of cookies and rationality "
        "parameters, check the pragmatic listener against a closed form, and let thirty pairs of Roth-Erev "
        "learners play Lewis's signalling game until their signals carry information.")
TASKS = [
    "Give the state 'all' a prior of 0.7 (prior=[0.1, 0.1, 0.1, 0.7] in pr.rsa). Does 'some' still convey 'not all'?",
    "Make 'all' costly (cost=[0, 0, 2] in pr.rsa). How does the implicature change, and why?",
    "Play the signalling game with three states (pr.signalling(n=3, rounds=1500, runs=30)). How many runs stop "
    "near 2/3, and how many bits do their signals carry?",
]


def _closed(n, alpha):
    """L1(all | some) with n cookies and a uniform prior: the speaker who saw all says 'some' with chance q."""
    q = 1 / (1 + n ** alpha)
    return q / (n - 1 + q)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the reference game and the cookie game
    ref = pr.reference_game()
    lab.row("hearing 'blue': blue square against blue circle", f"{ref['L1'][0][0]} to {ref['L1'][0][1]}   (by hand: 0.6 to 0.4)")
    assert abs(ref["L0"][0][0] - 0.5) < 1e-9 and abs(ref["L1"][0][0] - 0.6) < 1e-4
    film = pr.scalar()
    lab.row("3 cookies, alpha = 4: P(all | 'some')", f"{film['L1'][1][3]:.4f}   (closed form 1/165 = {1 / 165:.4f})")
    worst = 0.0
    for _ in range(60):
        n, alpha = int(rng.integers(2, 8)), float(rng.uniform(0.3, 6))
        r = pr.scalar(n=n, alpha=alpha)
        got = r["L1"][1][n]
        worst = max(worst, abs(got - _closed(n, alpha)))
        assert got < r["L0"][1][n], "the pragmatic listener always gives 'all' less than the literal one"
    lab.row("60 random games (n cookies, alpha)", f"largest gap from the closed form {worst:.1e}")
    assert worst < 1e-4, "the model matches q / (n - 1 + q)"
    rec = pr.recursion()
    lab.row("deeper listeners, alpha = 1", f"P(all | 'some') = {rec['some_all'][:5]}")
    assert all(a > b for a, b in zip(rec["some_all"], rec["some_all"][1:])), "each level strengthens the implicature"

    # 2. plus and quus
    pq = pr.plus_quus(seed=seed)
    lab.row("1000 past sums: plus and quus agree on", f"{pq['agree']}; rival rules below 200: {pq['rival_bounds_below_200']}")
    assert pq["agree"] == pq["history"] and pq["rival_bounds_below_200"] == 199 - pq["biggest"]
    assert pq["plus_68_57"] == 125 and pq["quus_68_57"] == 5

    # 3. the signalling game
    sig = pr.signalling(n=2, rounds=1500, runs=30, seed=seed, threshold=0.9)
    lab.row("signalling, 30 runs of 1500 rounds", f"{sig['perfect']} end above 90% success   (chance: 50%)")
    lab.row("bits carried by the learned signals", f"{sig['info_top']:.2f} of {sig['max_info']:.0f}")
    assert sig["perfect"] >= 18 and sig["mean_final"] > 0.85, "reinforcement alone finds a signalling system"
    assert 0.7 < sig["info_top"] <= 1.0 + 1e-9, "the signals carry most of one bit, and never more"
    lab.note = ("A listener who reasons about why the speaker did not say 'all' hears 'some' as 'not all', more "
                "strongly the more rational she takes the speaker to be; and two learners rewarded only for "
                "success end up with signals that carry nearly one bit.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    alphas = np.linspace(0.3, 8, 80)
    for n, color in ((2, labs.GOLD), (3, labs.BLUE), (6, labs.GREEN)):
        ax[0].plot(alphas, [_closed(n, a) for a in alphas], color=color, label=f"closed form, {n} cookies")
        pts = np.array([a for a in (0.5, 1, 2, 3, 4, 6, 8) if _closed(n, a) > 5e-3])  # the library rounds to 4 places
        ax[0].scatter(pts, [pr.scalar(n=n, alpha=float(a))["L1"][1][n] for a in pts], s=26, color=color, zorder=3)
        ax[0].axhline(1 / n, color=color, ls=":", lw=1)
    ax[0].plot([], [], color=labs.MUTED, ls=":", lw=1, label="literal listener, 1/n")
    ax[0].scatter([], [], s=26, color=labs.MUTED, label="the model")
    ax[0].set(title="How strongly 'some' conveys 'not all'",
              xlabel="speaker's rationality alpha", ylabel="pragmatic listener's P(all | 'some')", yscale="log")
    ax[0].legend(loc="lower left")
    t = 100 * np.arange(len(sig["curves"][0]))
    for i, c in enumerate(sig["curves"]):
        ax[1].plot(t, c, color=labs.CYCLE[i % len(labs.CYCLE)], lw=1.4)
    ax[1].axhline(0.5, color=labs.MUTED, ls="--", lw=1)
    ax[1].text(t[-1], 0.52, "chance", color=labs.MUTED, ha="right")
    ax[1].set(title="Six pairs of learners: success of the current strategies", xlabel="rounds played",
              ylabel="expected success", ylim=(0.4, 1.02))
    lab.fig = fig
    return lab
