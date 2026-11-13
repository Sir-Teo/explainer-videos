"""Lab 4: build a literature of small studies, filter it as journals did, and replicate what was printed."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import evidence as E

TITLE = "A literature of small studies: what gets printed, and what a replication finds"
GOAL = ("Run 4,000 laboratories on one small true effect, print only the significant results, and compare what is "
        "printed with the truth; read the literature's p-curve; replicate every printed finding; then make a study "
        "of nothing significant by flexible analysis and by looking early, and count how often it works.")
TASKS = [
    "Set the true effect to 0 and to 0.5. What happens to the mean printed effect, to the replication rate, and to "
    "the shape of the p-curve? Which of the three would let a reader tell the literatures apart?",
    "Raise the sample from 30 to 200 people a group. How much of the exaggeration is left, and what share of the "
    "laboratories now publish?",
    "In the optional-stopping block, allow 2 looks and then 20. At what number of looks does a study of nothing "
    "become more likely than not to succeed, and why does the curve flatten?",
]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed + 4)
    d, n, k = 0.2, 30, 4000

    # 1. what a study of this size can do
    out.row(f"power for d = {d} with {n} a group", f"{E.power(d, n):.2f}")
    out.row("people per group for 80% power", f"{E.n_for(d)}")
    out.row("smallest effect such a study can print (p < .05)", f"{1.96 * np.sqrt(2 / n):.2f}")

    # 2. the literature, and what the journals keep
    lit = E.literature(k, d, n, rng)
    pub = lit["published"]
    printed = float(lit["est"][pub].mean())
    out.row(f"laboratories that publish, of {k:,}", f"{int(pub.sum())} ({100 * pub.mean():.0f}%)")
    out.row("mean effect in all the laboratories", f"{lit['est'].mean():.2f}")
    out.row("mean effect in print", f"{printed:.2f} ({printed / d:.1f} times the truth)")
    assert abs(lit["est"].mean() - d) < 0.02 and printed > 2.5 * d, "the filter, not the laboratories, inflates"

    # 3. the p-curve of the printed studies
    curve = E.pcurve(lit["p"][pub])
    null = E.literature(40_000, 0.0, n, rng)
    flat = E.pcurve(null["p"][null["published"]])
    out.row("p-curve in print (five bins from 0 to .05)", " ".join(f"{c:.2f}" for c in curve))
    out.row("... of a literature about nothing", " ".join(f"{c:.2f}" for c in flat))
    assert curve[0] > 1.3 * curve[-1] and abs(flat[0] - flat[-1]) < 0.05

    # 4. replicate everything that was printed
    rep = E.replicate(lit, rng)
    out.row("replications that are significant", f"{100 * rep['rate']:.0f}%")
    out.row("replication effect as a share of the printed one", f"{rep['ratio']:.2f}")
    out.row("printed findings that are true", "100%")
    assert rep["rate"] < 0.45 and rep["ratio"] < 0.5

    # 5. two ways to make nothing significant
    forks = E.any_significant(range(1000 * seed, 1000 * seed + 1500))
    looks = [1, 2, 3, 5, 10, 20]
    peek = [E.peeking(m, 10, 3000, np.random.default_rng(seed + 50 + m))["rate"] for m in looks]
    out.row("a study of nothing: the planned analysis succeeds", f"{100 * forks['planned']:.1f}%")
    out.row("... at least one of sixteen defensible analyses does", f"{100 * forks['any']:.1f}%")
    out.row("... looking after every 10 people, up to 10 looks", f"{100 * peek[4]:.1f}%")
    assert 0.03 < forks["planned"] < 0.07 and forks["any"] > 2.5 * forks["planned"] and peek[4] > 0.15
    out.note = ("Every laboratory was honest and the effect was real, yet print reports about three times the truth "
                "and most replications fail: a low replication rate measures power and the filter, not only truth. "
                "The p-curve still shows that something is there. And a study of nothing succeeds about one time "
                "in five if the analysis, or the moment of stopping, is chosen after looking.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    se = lit["se"]
    ax[0].plot(lit["est"][~pub][:1500], 1 / se[~pub][:1500] + rng.normal(0, 0.03, min(1500, int((~pub).sum()))), ".",
               color=labs.BLUE, alpha=0.25, label="in the file drawer")
    ax[0].plot(lit["est"][pub], 1 / se[pub] + rng.normal(0, 0.03, int(pub.sum())), ".", color=labs.PINK, alpha=0.6,
               label="printed")
    ax[0].axvline(d, color=labs.GREEN, lw=2)
    ax[0].axvline(printed, color=labs.PINK, lw=1.5, ls="--")
    ax[0].set(title=f"{k:,} laboratories: truth {d}, print {printed:.2f}", xlabel="effect a laboratory found (d)",
              ylabel="precision (jittered)")
    ax[0].legend()
    ax[1].plot(looks, peek, "o-", color=labs.PURPLE, label="looking early and stopping")
    ax[1].axhline(forks["any"], color=labs.PINK, ls="--", label="any of sixteen analyses")
    ax[1].axhline(0.05, color=labs.GREEN, label="the 5% that was promised")
    ax[1].set(title="How often a study of nothing succeeds", xlabel="number of looks at the data",
              ylabel="share with p < .05", ylim=(0, 0.3))
    ax[1].legend()
    out.fig = fig
    return out
