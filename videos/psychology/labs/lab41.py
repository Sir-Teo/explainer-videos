"""Lab 41: the hollow mask on a Gaussian observer and the best strength of a prior, conditioned hallucinations,
aberrant salience, Redish's model of addiction, and hyperbolic discounting."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import clinic as K

TITLE = "Psychosis, Addiction and Development"
GOAL = ("Compute when a prior makes a hollow mask look like a face and how strong a prior should be; condition "
        "hallucinations in learners whose priors weigh more or less; let random dopamine bursts give irrelevant cues "
        "value; run Redish's drug signal against a natural reward; and find where hyperbolic preferences reverse.")
TASKS = [
    "Lower the eyes' precision from 4 to 1 (a dim room, or one eye shut). How weak a prior now produces the face?",
    "In the conditioned-hallucination design, keep the tone at 75% in every block. Does the difference between "
    "prior weights grow or shrink, and why?",
    "Give Redish's drug a surge D that falls with each use (tolerance). Does the drug's value still grow without "
    "bound?",
]


def run(seed=0):
    out = labs.Lab()

    for pp in (2.0, 4.0, 8.0):
        h = K.hollow_mask(pp)
        out.row(f"hollow mask, prior precision {pp:g}: posterior mean; chance of seeing a face",
                f"{h['mean']:+.2f}; {h['p_convex']:.2f}")
    assert abs(K.hollow_mask(4.0)["p_convex"] - 0.5) < 1e-9
    grid = np.linspace(0, 20, 2001)
    for p in (0.95, 0.6):
        best = grid[int(np.argmin(K.prior_tradeoff(grid, p_typical=p)))]
        w = 0.25 / (0.25 + 4 * (1 - p))
        out.row(f"best prior precision when the world is typical {100 * p:.0f}% of the time: grid; formula",
                f"{best:.2f}; {w * 4 / (1 - w):.2f}")
        assert abs(best - w * 4 / (1 - w)) < 0.02

    lo = K.conditioned_hallucinations(0.3, seed=seed)
    hi = K.conditioned_hallucinations(1.5, seed=seed)
    out.row("tone heard on silent trials: prior weight 0.3; 1.5",
            f"{100 * lo['overall']:.0f}%; {100 * hi['overall']:.0f}%")
    assert hi["overall"] > lo["overall"]

    for q in (0.0, 0.2, 0.3):
        a = K.aberrant_salience(q, seed=seed)
        out.row(f"aberrant salience, bursts on {100 * q:.0f}% of trials: irrelevant cues above 0.25; their mean value",
                f"{a['salient']}; {a['V'][1:].mean():.2f}")

    nat, drug, cost = K.redish(0.0), K.redish(0.2, reward=0.5), K.redish(0.2, reward=0.5, cost=1.0)
    out.row("Redish: value after 300 uses: natural reward; drug; drug with a cost of 1",
            f"{nat[-1]:.2f}; {drug[-1]:.2f}; {cost[-1]:.2f}")
    assert cost[-1] >= 300 * 0.1 * 0.2 - 1e-9

    for k in (0.01, 0.05):
        out.row(f"discounting k = {k}: 50 now against 100 in 30 days; 50 in 60 days against 100 in 90",
                f"{float(K.discount(50, 0, k)):.1f} vs {float(K.discount(100, 30, k)):.1f}; "
                f"{float(K.discount(50, 60, k)):.1f} vs {float(K.discount(100, 90, k)):.1f}")

    out.note = ("A prior more precise than the eyes makes the hollow mask a face; how strong a prior should be "
                "depends on how often the world matches it; heavier priors condition more hallucinations; random "
                "dopamine bursts give every cue a little value; a drug's surge that cannot be predicted away makes its "
                "value grow whatever it costs; and hyperbolic discounting reverses preferences as rewards come near.")

    fig, ax = labs.figure(3, size=(13, 4.0))
    pp = np.linspace(0, 14, 141)
    ax[0].plot(pp, [K.hollow_mask(float(x))["p_convex"] for x in pp], color=labs.BLUE)
    ax[0].axvline(4, color="grey", ls=":")
    ax[0].set(title="The hollow mask", xlabel="prior precision", ylabel="P(sees a face)")
    ax[1].plot(nat, color=labs.GREEN, label="natural")
    ax[1].plot(drug, color=labs.RED, label="drug")
    ax[1].plot(cost, color=labs.GOLD, ls="--", label="drug with a cost")
    ax[1].set(title="Redish's model", xlabel="uses", ylabel="value")
    ax[1].legend(fontsize=8)
    d = np.linspace(0, 365, 366)
    for k, c in ((0.01, labs.GREEN), (0.05, labs.RED)):
        ax[2].plot(d, K.discount(100, d, k), color=c, label=f"k = {k}")
    ax[2].axhline(50, color="grey", ls=":")
    ax[2].set(title="Hyperbolic discounting", xlabel="delay (days)", ylabel="value of 100 now")
    ax[2].legend(fontsize=8)
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
