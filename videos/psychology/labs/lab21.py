"""Lab 21: four forgetting laws fitted to Ebbinghaus and three replications, compared by AIC; the averaging artefact;
interference in a linear associator; a two-store model of consolidation and Ribot's gradient; Pavlik and Anderson's
spacing ridgeline; the bifurcation model fitted to the testing effect; the category adjustment model; the DRM
illusion by global matching; a line-up's confidence-accuracy characteristic; half-life regression; and the
verbal-overshadowing replication pooled from its open data."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import archive, opendata
from explainer.psychology.psyche import memory as M

TITLE = "Memory: forgetting and inventing"
GOAL = ("Fit and compare forgetting laws; see a power law appear from averaged exponentials; watch interference, "
        "consolidation and the spacing ridgeline come out of small models; fit the bifurcation model to the testing "
        "effect; make a memory lean toward its category; produce a false memory by summing similar traces; read a "
        "witness's confidence by signal detection; fit a scheduler's forgetting curve; and pool 22 labs' replication.")
TASKS = [
    "Fit `c`, `a`, `threshold` and `s` of `memory.spacing_ridge` to Cepeda's optimal gaps (3, 8, 12, 27 days) and "
    "gains (10 to 111%). Can one setting get both the timing and the size?",
    "In `memory.bifurcation`, give the failed items a gain too (feedback). How small a gain removes the crossover?",
    "Pool the first overshadowing replication (description straight after the video) with random effects. Is the "
    "between-lab spread larger or smaller than in the second?",
]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. four laws, four people
    s = archive.SAVINGS_REPLICATIONS.data
    t = np.array(s["minutes"], float)
    for who in ("ebbinghaus", "mack", "seitz", "dros"):
        a = {law: M.fit_law(law, t, s[who])["aic"] for law in M.LAWS}
        out.row(f"{who}: AIC power, exponential, log, Wickelgren",
                ", ".join(f"{a[k]:.1f}" for k in ("power", "exponential", "log", "wickelgren")))
        assert a["power"] < a["exponential"]  # fast, then slow

    # 2. averaged exponentials are a power function
    rates = rng.gamma(1.5, 0.4, 100_000)
    tt = np.array([1.0, 5.0, 20.0])
    mc = np.exp(-np.outer(rates, tt)).mean(0)
    out.row("mean of exponentials at t = 1, 5, 20; (1 + 0.4 t)^-1.5",
            ", ".join(f"{v:.3f}" for v in mc) + "; " + ", ".join(f"{v:.3f}" for v in M.gamma_mixture(tt, 1.5, 0.4)))
    assert np.allclose(mc, M.gamma_mixture(tt, 1.5, 0.4), rtol=0.02)

    # 3. interference
    lo = M.associator_interference(overlap=0.0, rng=rng)["both"]
    hi = M.associator_interference(overlap=1.0, rng=rng)["both"]
    out.row("recall of list 1 after list 2: cues unrelated, cues the same", f"{lo:.2f}, {hi:.2f}")
    assert lo > hi

    # 4. consolidation
    age = np.array([0.0, 5.0, 20.0, 100.0])
    spared = M.two_store(age, lesion=True) / M.two_store(age)
    out.row("share of retrieval strength left after a lesion, by age", ", ".join(f"{v:.2f}" for v in spared))
    assert np.all(np.diff(spared) > 0)  # Ribot: the older, the safer

    # 5. spacing
    gaps = np.unique(np.r_[np.linspace(0, 2, 9), np.geomspace(2, 120, 40)])
    ri = np.array([7.0, 35.0, 70.0, 350.0])
    R = M.spacing_ridge(gaps, ri, c=1.0, a=0.1)
    best = gaps[R.argmax(1)]
    out.row("best gap as a share of the retention interval (7, 35, 70, 350 days)",
            ", ".join(f"{v:.2f}" for v in best / ri))
    assert np.all(np.diff(best / ri) < 0)

    # 6. testing
    r = archive.ROEDIGER_KARPICKE_2006.data
    f = M.fit_bifurcation({"restudy": r["exp1_restudy"], "test": r["exp1_test"]})
    m = f["model"]
    out.row("bifurcation fit: re-read and tested at 5 min, 2 d, 1 wk",
            ", ".join(f"{a:.2f}/{b:.2f}" for a, b in zip(m["restudy"], m["test"])))
    out.row("predicted share recalled on the first test (observed: about 0.70)", f"{m['initial_test']:.2f}")
    assert m["restudy"][0] > m["test"][0] and m["test"][2] > m["restudy"][2]

    # 7. category adjustment
    ca = M.category_adjustment(np.linspace(5, 85, 9), 15.0, 22.0, rng=rng)
    out.row("bias at 5 and 85 degrees; error blended and raw",
            f"{ca['bias'][0]:+.1f}, {ca['bias'][-1]:+.1f}; {ca['rmse'].mean():.1f}, {ca['rmse_trace'].mean():.1f}")
    assert ca["rmse"].mean() < ca["rmse_trace"].mean()

    # 8. DRM
    d = M.drm_global_matching(lists=100, assoc=0.095, rng=rng)["familiarity"]
    crit = float(np.quantile(d["studied"], 0.14))
    yes = {k: float(np.mean(v > crit)) for k, v in d.items()}
    out.row("called old: studied, lure, unrelated", f"{yes['studied']:.2f}, {yes['lure']:.2f}, {yes['unrelated']:.2f}")
    assert yes["lure"] > 3 * yes["unrelated"]

    # 9. line-ups
    cac = M.lineup_cac(1.5, n=60_000, rng=rng)
    out.row("line-up accuracy by confidence, 1 to 5 (d' = 1.5)", ", ".join(f"{v:.2f}" for v in cac["cac"]))
    assert cac["cac"][-1] > cac["cac"][0]

    # 10. half-life regression
    sim = M.hlr_simulate(learners=200, rng=rng)
    h = M.fit_hlr(sim["x"], sim["gap"], sim["recalled"])
    out.row("half-life regression: theta fitted (true 0.9, -0.6, 2.2)", ", ".join(f"{v:.2f}" for v in h["theta"]))
    assert h["theta"][0] > 0 > h["theta"][1]

    # 11. the overshadowing replication, if the open data can be fetched
    if opendata.available("overshadowing_rrr2"):
        o = opendata.overshadowing_rrr(2)
        v, c = o["verbal"], o["control"]
        diff = v[:, 0] / v[:, 1] - c[:, 0] / c[:, 1]
        out.row("overshadowing (RRR 2): labs, mean difference, original",
                f"{len(diff)}, {diff.mean():+.3f}, {o['original'][0, 0] / o['original'][0, 1] - o['original'][1, 0] / o['original'][1, 1]:+.3f}")
        assert diff.mean() < 0
    else:
        out.row("overshadowing (RRR 2)", "the open data could not be fetched")

    out.note = ("Power-like forgetting in every replication, and a power law from averaged exponentials. Interference "
                "grows with shared cues; a lesion spares old memories; the best gap shrinks relative to the retention "
                "interval; testing loses at five minutes and wins at a week; a blended memory is biased and more "
                "accurate; the DRM lure is called old almost as often as a studied word; high-confidence line-up "
                "choices are mostly right; half-life regression recovers its parameters.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    tt = np.geomspace(15, 60000, 200)
    for who, col in (("ebbinghaus", labs.GOLD), ("dros", labs.BLUE)):
        p = M.fit_law("power", t, s[who])["params"]
        ax[0].scatter(t, s[who], color=col, s=14, label=who)
        ax[0].plot(tt, M.law_curve("power", p, tt), color=col, lw=1.4)
    ax[0].set_xscale("log")
    ax[0].set(title="Savings and the power law", xlabel="minutes since learning", ylabel="savings")
    ax[0].legend(fontsize=8)
    for i, col in enumerate((labs.GOLD, labs.BLUE, "#5bd18b", "#f28fb8")):
        ax[1].plot(gaps, R[i], color=col, lw=1.6, label=f"tested after {int(ri[i])} d")
    ax[1].set(title="The spacing ridgeline (Pavlik and Anderson)", xlabel="gap between sessions (days)",
              ylabel="recall at test")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out
