"""Lab 35: Kelley's cube as an analysis of variance, a rational observer of forced essays, the Dunning-Kruger plot
from regression to the mean, inverse planning in a gridworld, and the winner's curse."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import social as S

TITLE = "Social Cognition"
GOAL = ("Decompose Kelley's cube into main effects and read consensus, distinctiveness and consistency from it; infer "
        "a writer's attitude from an essay by Bayes' rule; rebuild the Dunning-Kruger graph from a modest correlation "
        "and a flattering shift; infer an agent's goal from its path with an inverse planner; and watch small "
        "significant studies overestimate a true effect.")
TASKS = [
    "Set the Dunning-Kruger correlation to 0.6 and the shift to 0. Which quarter now overestimates, which "
    "underestimates, and by how much? What does this say about reading the famous graph as a lack of insight?",
    "Give the inverse planner a prior of 0.8 on goal B and rerun the 'up' walk. How many steps does it take for A "
    "to pass 0.9? Then lower beta to 0.2: what does a noisier agent do to the observer's certainty?",
    "Rerun the winner's curse with 50 people per group. What share reaches significance, and how large do they look?",
]

SHAPE = (7, 9)
WALLS = [(r, 4) for r in range(1, 6)]
GOALS = [(0, 8), (6, 8), (3, 0)]
UP = [(3, 3), (2, 3), (1, 3), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
TURN = [(3, 6), (2, 6), (1, 6), (0, 6), (0, 5), (0, 4), (0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0)]


def curse(n, d=0.2, reps=20000, seed=0, full=False):
    """Two-group studies of a true effect d with n per group: the share significant at 5% (two-sided t, positive
    direction), and their mean estimated d."""
    from scipy import stats
    rng = np.random.default_rng(seed)
    x = rng.normal(d, 1, (reps, n))
    y = rng.normal(0, 1, (reps, n))
    sp = np.sqrt((x.var(axis=1, ddof=1) + y.var(axis=1, ddof=1)) / 2)
    dh = (x.mean(axis=1) - y.mean(axis=1)) / sp
    t = dh * np.sqrt(n / 2)
    sig = t > stats.t.ppf(0.975, 2 * n - 2)
    if full:
        return dh, sig
    return float(sig.mean()), float(dh[sig].mean())


def run(seed=0):
    out = labs.Lab()

    person = np.zeros((2, 2, 2))
    person[0] = 1
    k = S.kelley(person)
    out.row("Kelley, only person 1 reacts: person share; consensus, distinctiveness, consistency",
            f"{k['shares']['person']:.2f}; {k['consensus']:.0f}, {k['distinctiveness']:.0f}, {k['consistency']:.0f}")
    assert np.isclose(k["shares"]["person"], 1.0)
    entity = np.zeros((2, 2, 2))
    entity[:, 0, :] = 1
    k = S.kelley(entity)
    out.row("Kelley, everyone reacts to entity 1: entity share; consensus, distinctiveness, consistency",
            f"{k['shares']['entity']:.2f}; {k['consensus']:.0f}, {k['distinctiveness']:.0f}, {k['consistency']:.0f}")

    for pi in (1.0, 0.7, 0.3, 0.0):
        out.row(f"P(pro | pro essay) when the assignment held with probability {pi:.1f}", f"{1 / (1 + pi):.3f}")

    for rho, shift in ((0.3, 15), (1.0, 0), (0.0, 0)):
        dk = S.dunning_kruger(n=4000, rho=rho, shift=shift, seed=seed + 35)
        out.row(f"Dunning-Kruger, rho {rho}, shift {shift}: perceived by quarter",
                ", ".join(f"{v:.0f}" for v in dk["perceived"]))

    post = S.goal_posterior(UP, SHAPE, WALLS, GOALS, beta=0.7)
    out.row("inverse planning, the 'up' walk: P(A) after 0, 1, 2 and 3 steps",
            ", ".join(f"{p:.2f}" for p in post[:4, 0]))
    assert post[3, 0] > 0.9

    for n in (21, 100):
        power, dsig = curse(n, seed=seed)
        out.row(f"winner's curse, d = 0.2, {n} per group: share significant; their mean d", f"{power:.3f}; {dsig:.2f}")

    out.note = ("Attribution is an analysis of variance over people, things and occasions; an essay is evidence about "
                "its writer unless the observer is sure it was forced; regression to the mean and a flattering shift "
                "draw the Dunning-Kruger graph with no insight in it; a goal is read from a path by Bayes' rule with a "
                "planner as the likelihood; and studies too small for their effect overestimate it whenever they "
                "succeed.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    q = np.array([12.5, 37.5, 62.5, 87.5])
    ax[0].plot(q, q, color="0.6", ls="--", label="actual")
    for rho, shift, col in ((0.3, 15, labs.GOLD), (0.0, 0, labs.BLUE)):
        dk = S.dunning_kruger(n=4000, rho=rho, shift=shift, seed=seed + 35)
        ax[0].plot(q, dk["perceived"], "o-", color=col, label=f"rho {rho}, shift {shift}")
    ax[0].set(title="Dunning-Kruger from noise", xlabel="actual percentile (quarter)", ylabel="perceived percentile")
    ax[0].legend(fontsize=8)
    post = S.goal_posterior(TURN, SHAPE, WALLS, GOALS, beta=0.7)
    for j, (name, col) in enumerate(zip("ABC", (labs.GOLD, labs.GREEN, labs.BLUE))):
        ax[1].plot(post[:, j], "o-", color=col, label=name)
    ax[1].set(title="Inverse planning, the 'turn' walk", xlabel="step", ylabel="posterior")
    ax[1].legend(fontsize=8)
    dh, sig = curse(21, seed=seed, full=True)
    bins = np.linspace(-1.2, 1.6, 57)
    ax[2].hist(dh, bins=bins, color="0.6", alpha=0.6, label="all studies")
    ax[2].hist(dh[sig], bins=bins, color=labs.GOLD, label="significant")
    ax[2].axvline(0.2, color="k", lw=1)
    ax[2].set(title="Winner's curse, 21 per group, d = 0.2", xlabel="estimated d", ylabel="studies")
    ax[2].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
