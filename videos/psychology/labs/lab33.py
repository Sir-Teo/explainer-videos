"""Lab 33: five factors in 2,800 people's answers, aggregation and the person-situation debate, what a median split
does to types, and sex differences in one dimension and in many."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import personality as P
from explainer.stats.kit import multi

TITLE = "Personality"
GOAL = ("Score the SAPA sample's 25 items, decide how many factors to keep by parallel analysis and fit them; build a "
        "world of people and situations and watch aggregation turn a .3 into a .9; see why types are unstable; and "
        "compare women and men one trait at a time and all at once.")
TASKS = [
    "Raise the signature's SD in the act world from 0.6 to 1.2. How do the single-act correlation, the same-situation "
    "retest and the aggregated curve change, and why does the retest move more?",
    "Drop the reverse-keyed items from each scale. How do alpha and the sex differences change?",
    "Add a sixth, random 'trait' to the five scales before computing Mahalanobis's D. Does D grow, and what does that "
    "say about choosing variables?",
]


def run(seed=0):
    out = labs.Lab()
    if opendata.available("bfi2010"):
        d = opendata.bfi()
        X, items = d["X"], d["items"]
        pa = P.parallel(X, n_iter=20, seed=seed)
        out.row("SAPA, 25 items: eigenvalues 1-6; factors kept by parallel analysis",
                ", ".join(f"{v:.2f}" for v in pa["eigen"][:6]) + f"; {pa['keep']}")
        assert pa["keep"] == 5
        ok = ~np.isnan(X).any(axis=1)
        f = multi.factor_ml(np.corrcoef(X[ok], rowvar=False), 5, n=int(ok.sum()))
        L = np.asarray(multi.varimax(f["loadings"])["loadings"])
        hits = sum(1 for i, nm in enumerate(items)
                   if len({items[j][0] for j in range(len(items)) if np.argmax(np.abs(L[j])) == np.argmax(np.abs(L[i]))}) == 1)
        out.row("items whose strongest factor holds only their own trait's items", f"{hits} of {len(items)}")
        sc = P.score(X, items)
        S5 = np.column_stack([sc[t] for t in P.TRAITS])
        g = d["gender"]
        m = P.mahalanobis(S5[g == 1], S5[g == 2])
        out.row("women minus men, d for A, C, E, N, O; D on five scales",
                ", ".join(f"{v:+.2f}" for v in m["d"]) + f"; {m['D']:.2f}")
    else:
        out.row("SAPA data", "not fetched (python -m videos.psychology.psych33.compute factors)")

    w = P.act_world(n=4000, situations=40, seed=seed + 33)
    a = P.aggregate_curve(w, ks=(1, 4, 16))
    out.row("one act vs another; 4 vs 4; 16 vs 16 situations", ", ".join(f"{v:.2f}" for v in a["observed"]))
    out.row("Spearman-Brown from the single act", ", ".join(f"{v:.2f}" for v in a["spearman_brown"]))
    t = P.type_agreement(0.8, dims=4)
    out.row("reliability 0.8: same type on one dimension; on four", f"{t['one']:.3f}; {t['all']:.3f}")

    out.note = ("Five factors are in the data, and every item finds its own; one act predicts another weakly and many "
                "acts predict many others well, exactly as Spearman-Brown says; types lose information and change on "
                "retest; and small differences in many traits add up to a larger multivariate distance.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ks = np.array([1, 2, 4, 8, 16])
    ag = P.aggregate_curve(w, ks=tuple(ks))
    ax[0].plot(ks, ag["observed"], "o", color=labs.GOLD, label="simulated")
    ax[0].plot(ks, ag["spearman_brown"], "-", color=labs.BLUE, label="Spearman-Brown")
    ax[0].set(title="Aggregation", xlabel="situations averaged", ylabel="consistency", xscale="log")
    ax[0].legend(fontsize=8)
    rs = np.linspace(0, 0.99, 50)
    ax[1].plot(rs, 0.5 + np.arcsin(rs) / np.pi, color=labs.GOLD, label="one dimension")
    ax[1].plot(rs, (0.5 + np.arcsin(rs) / np.pi) ** 4, color=labs.BLUE, label="four dimensions")
    ax[1].set(title="Same type on retest", xlabel="reliability", ylabel="share")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out
