"""Lab 29: a map of feelings by classical scaling of Abelson and Sermat's 1962 faces, a simulated observer's map
aligned by Procrustes, the facial-feedback meta-analysis recomputed from its open table, arousal attribution, an
appraisal model, and a plateau hidden in an average."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import drive as D
from explainer.psychology.psyche import emotion as E

TITLE = "Emotion"
GOAL = ("Recover a two-dimensional map of feelings from judged similarities of faces, and check it against rated "
        "scales; align a simulated observer's map to the truth; recompute the facial-feedback meta-analysis and "
        "its precision-effect test; read the two-factor theory as Bayesian attribution; label scenarios by "
        "appraisal; and see how a plateau for some people hides in the average.")
TASKS = [
    "Run classical scaling of the 1962 faces in three dimensions. Does the third dimension match the "
    "attention-rejection scale better than the first two do?",
    "Recompute the facial-feedback pool with each effect weighted separately rather than pooled within study "
    "first. How much do the estimate and its interval change, and why is the within-study pooling safer?",
    "Change the income world's unhappy share from 0.2 to 0.05. Which percentiles still flatten, and what does "
    "a measure of 'felt bad yesterday' show?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. the 1962 faces
    f = opendata.faces_1962()
    m = E.classical_mds(f["D"])
    fits = {k: E.fit_scale(m["X"], f[k])["R"] for k in ("PU", "TS", "AR")}
    out.row("1962 faces: share in two dimensions; R for pleasantness, tension, attention-rejection",
            f"{m['share']:.2f}; {fits['PU']:.2f}, {fits['TS']:.2f}, {fits['AR']:.2f}")
    assert m["share"] > 0.8 and fits["PU"] > 0.9 and fits["TS"] > 0.9

    # 2. a simulated observer's map
    rs = {k: E.pairs_map(n_reps=k, seed=29)["r"] for k in (1, 3, 10)}
    out.row("ten schematic faces, 45 pairs: map against the truth after 1, 3, 10 judgments per pair",
            ", ".join(f"{rs[k]:.2f}" for k in (1, 3, 10)))
    assert rs[10] > rs[1]

    # 3. facial feedback
    c = opendata.coles_2019()
    y, v, sid = c["yi"], c["vi"], c["study_id"]
    ys, vs = [], []
    for i in sorted(set(sid.tolist())):
        w = 1 / v[sid == i]
        ys.append(float((w * y[sid == i]).sum() / w.sum()))
        vs.append(float(1 / w.sum()))
    re = D.random_effects(ys, vs)
    pe = D.pet(ys, np.sqrt(vs))
    out.row("facial feedback: studies; pooled d [95% CI]; I^2; PET intercept",
            f"{re['k']}; {re['estimate']:.3f} [{re['lo']:.3f}, {re['hi']:.3f}]; {100 * re['I2']:.0f}%; "
            f"{pe['intercept']:.3f}")
    assert re["k"] == 138 and abs(re["estimate"] - 0.20) < 0.01

    # 4. attribution
    a = {k: E.attribution(*args)["mean"] for k, args in
         (("no explanation", (1.2, 0.0)), ("explained injection", (1.2, 1.0)), ("placebo", (0.3, 0.0)))}
    out.row("arousal attributed to the situation: unexplained, explained, placebo",
            ", ".join(f"{v_:.2f}" for v_ in a.values()))
    assert a["explained injection"] < a["no explanation"]

    # 5. appraisal
    for text, code in (("a colleague takes credit for your work", (-0.8, 0.7, -0.3, 0.9, 0.3, 0.4)),
                       ("a noise downstairs at three in the morning", (-0.7, -0.8, 0.0, 0.1, -0.7, 0.8))):
        r = E.appraise(code)
        out.row(f"appraisal of '{text}'", f"{r['labels'][0]} {r['p'][0]:.2f}, {r['labels'][1]} {r['p'][1]:.2f}")

    # 6. the hidden plateau
    w = E.income_world()
    x = np.log2(w["income"])
    hi = w["income"] > 120_000
    s_mean, s_p10 = np.polyfit(x[hi], w["mean"][hi], 1)[0], np.polyfit(x[hi], w["p10"][hi], 1)[0]
    out.row("above $120,000: slope per doubling of the mean, of the 10th percentile", f"{s_mean:.2f}, {s_p10:.2f}")
    assert s_mean > 0.2 and abs(s_p10) < 0.08

    out.note = ("Judged similarities of faces fall on two dimensions that match rated pleasantness and tension; a "
                "coarse yes-or-no per pair recovers the map; facial feedback pools to about d = 0.2 with large "
                "heterogeneity; an explanation takes arousal away from the situation; and a plateau for a fifth of "
                "people shows in the low percentiles, not in the mean.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    X = m["X"]
    ax[0].scatter(X[:, 0], X[:, 1], color=labs.BLUE)
    for (px, py), name in zip(X, f["labels"]):
        ax[0].annotate(name, (px, py), fontsize=7)
    ax[0].set(title="Abelson and Sermat's faces, by classical scaling", xlabel="dimension 1", ylabel="dimension 2")
    order = np.argsort(ys)
    ax[1].errorbar(np.array(ys)[order], np.arange(len(ys)), xerr=1.96 * np.sqrt(np.array(vs))[order], fmt=".",
                   color=labs.BLUE, alpha=0.6)
    ax[1].axvline(re["estimate"], color=labs.GOLD)
    ax[1].axvline(0, ls="--", color="#888888")
    ax[1].set(title="Facial feedback, by study", xlabel="d", ylabel="study")
    out.fig = fig
    return out
