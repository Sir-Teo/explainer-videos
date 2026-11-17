"""Lab 50: the weight of evidence: a filtered literature, pooling, funnel asymmetry, corrections, GRIM and
statcheck, a specification curve and Meehl's crud."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import meta as M

TITLE = "The Weight of Evidence"
GOAL = ("Build a filtered literature with a known truth, pool it, see the filter in the funnel, try the corrections, "
        "and check reported numbers by arithmetic.")
TASKS = [
    "Publish every study (publish_null = 1). What happens to the naive estimate and to Egger's test?",
    "Add heterogeneity (tau = 0.3). Which correction suffers most?",
    "Find three means between 3.00 and 4.00 that GRIM rejects for n = 13.",
]


def run(seed=0):
    out = labs.Lab()
    lit = M.literature(k=300, true_d=0.2, tau=0.1, publish_null=0.15, seed=seed + 1)
    pub = lit["published"]
    y, v, se = lit["d"][pub], lit["v"][pub], lit["se"][pub]
    naive = M.random_effects(y, v)
    allre = M.random_effects(lit["d"], lit["v"])
    assert naive["mu"] > allre["mu"]
    out.row("pooled: every study; the published", f"{allre['mu']:.2f}; {naive['mu']:.2f} ({int(pub.sum())} studies)")
    e = M.estimate_all(lit)
    out.row("trim-and-fill; PET-PEESE; selection model; p-curve",
            f"{e['trim-and-fill']:.2f}; {e['PET-PEESE']:.2f}; {e['selection model']:.2f}; {e['p-curve']:.2f}")
    out.row("Egger's test p", f"{M.egger(y, se)['p']:.4f}")
    out.row("GRIM: 5.19 from 28 answers possible?", str(M.grim(5.19, 28)))
    sc = M.statcheck([(1.80, 30, 0.04, "=")])[0]
    out.row("t(30) = 1.80, reported p = .04: recomputed", f"{sc['recomputed']:.3f} (gross: {sc['gross']})")
    s = M.spec_curve(seed=seed + 2)
    out.row("specification curve: share significant of 96", f"{s['share_sig']:.2f}")

    out.note = ("Pooling a filtered literature gives a precise estimate of the wrong number; the corrections "
                "disagree because they assume different filters; arithmetic alone can catch some impossible results.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].scatter(lit["d"], lit["se"], s=6, color="grey", label="every study")
    ax[0].scatter(y, se, s=10, color=labs.BLUE, label="published")
    ax[0].invert_yaxis()
    ax[0].axvline(0.2, color="green", ls=":")
    ax[0].set(title="a funnel with a bite", xlabel="effect d", ylabel="standard error")
    ax[0].legend()
    ax[1].plot(np.arange(1, 97), s["est"], "o", ms=3, color=labs.RED)
    ax[1].set(title="a specification curve", xlabel="specification (sorted)", ylabel="estimate")
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())
