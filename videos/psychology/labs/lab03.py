"""Lab 3: take a questionnaire apart on the Pool, where every person's true score is known."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import measure as M
from explainer.psychology import pool as pool_mod
from explainer.psychology.pool import Pool

TITLE = "A questionnaire taken apart: how much of a score is true, and what the estimates say"
GOAL = ("Give a ten-item questionnaire to the Pool and split the variance of its scores into true score and "
        "error; estimate the same reliability from a second form, from alpha and from the Spearman-Brown formula; "
        "correct a correlation for attenuation; watch alpha mislead; and see a robust effect fail as a test.")
TASKS = [
    "Change the number of items from 10 to 3 and to 30. Which of the four reliability figures move together, and "
    "what happens to the observed correlation between the two traits?",
    "Give the items unequal loadings (loading=np.linspace(0.2, 0.9, 10)). Which estimate of reliability is now "
    "too low, and why is that the safe direction for it to be wrong?",
    "Cut the conflict task to 20 trials a condition, then raise it to 480. What happens to the retest agreement "
    "of the cost, and what stays the same about how often a study of 20 people finds the effect?",
]


def run(seed=0):
    out = labs.Lab()
    pool = Pool()
    n, k = 20_000, 10
    ids = pool.sample(n, seed=seed + 31)
    truth = pool.conscientious[ids]

    # 1. the variance of the scores, split into true score and error
    occasions = np.array([pool.scale("conscientious", ids[:3000], k, seed=100 * (seed + 1) + j) for j in range(40)])
    var_x, var_e = occasions.var(axis=1).mean(), occasions.var(axis=0, ddof=1).mean()
    rel = (var_x - var_e) / var_x
    out.row("variance of the scores = true + error", f"{var_x:.1f} = {var_x - var_e:.1f} + {var_e:.1f}")
    out.row("reliability, from the hidden true scores", f"{rel:.3f}")

    # 2. the same number from things an investigator can see
    items = pool.items("conscientious", ids, k, seed=seed + 1)
    a, b = items.sum(axis=1), pool.scale("conscientious", ids, k, seed=seed + 2)
    parallel, alpha = np.corrcoef(a, b)[0, 1], M.cronbach_alpha(items)
    one = M.reliability(truth, pool.scale("conscientious", ids, 1, seed=seed + 3))
    sb = M.spearman_brown(one, k)
    out.row("... from a second form (parallel-forms correlation)", f"{parallel:.3f}")
    out.row("... from one sitting (Cronbach's alpha)", f"{alpha:.3f}")
    out.row(f"... from one item ({one:.3f}) by Spearman-Brown", f"{sb:.3f}")
    assert max(abs(parallel - rel), abs(alpha - rel), abs(sb - rel)) < 0.03, "four routes to one number"
    out.row("standard error of measurement (points)", f"{M.sem(a.std(), rel):.2f}")

    # 3. attenuation and its correction
    grit = pool.scale("grit", ids, k, seed=seed + 4)
    rel_g = np.corrcoef(grit, pool.scale("grit", ids, k, seed=seed + 5))[0, 1]
    r_obs = np.corrcoef(a, grit)[0, 1]
    r_fix = M.disattenuate(r_obs, parallel, rel_g)
    out.row("two traits that truly correlate", f"{pool_mod.GRIT_R:.2f}")
    out.row("... as observed through two 10-item scales", f"{r_obs:.3f}")
    out.row("... after Spearman's correction", f"{r_fix:.3f}")
    assert r_obs < pool_mod.GRIT_R - 0.08 and abs(r_fix - pool_mod.GRIT_R) < 0.03

    # 4. alpha is not evidence of one dimension
    two = np.hstack([items, pool.items("extravert", ids, k, seed=seed + 6)])
    halves = np.corrcoef(two[:, :k].sum(axis=1), two[:, k:].sum(axis=1))[0, 1]
    out.row("20 items from two unrelated traits: alpha", f"{M.cronbach_alpha(two):.3f}")
    out.row("... correlation of its two halves", f"{halves:.3f}")
    assert M.cronbach_alpha(two) > 0.7 and abs(halves) < 0.2

    # 5. a robust effect that is a poor test
    s1, s2 = pool.conflict_task(ids, 120, seed=seed + 7), pool.conflict_task(ids, 120, seed=seed + 8)
    rng = np.random.default_rng(seed)
    found = 0
    for s in range(300):
        cost = pool.conflict_task(rng.choice(ids, 20, replace=False), 120, seed=1000 + 300 * seed + s)["cost"]
        found += cost.mean() / (cost.std(ddof=1) / np.sqrt(20)) > 2.1
    icc_cost, icc_level = M.icc(s1["cost"], s2["cost"]), M.icc(s1["congruent"], s2["congruent"])
    out.row("conflict task, 300 studies of 20 people: effect found in", f"{100 * found / 300:.0f}%")
    out.row("... retest agreement of a person's cost", f"{icc_cost:.2f}")
    out.row("... retest agreement of a person's speed", f"{icc_level:.2f}")
    assert found == 300 and icc_cost < 0.75 < icc_level
    out.note = ("Reliability computed from hidden true scores is recovered by three methods that never see them. "
                "Error shrinks the correlation between two traits, and the correction restores it. Alpha is high "
                "for a test of two unrelated things. And an effect found by every small study agrees with itself "
                "only moderately as a score for a person.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    lengths = [1, 2, 4, 6, 10, 15, 20, 30, 40]
    measured = [M.reliability(truth, pool.scale("conscientious", ids, m, seed=seed + 40 + m)) for m in lengths]
    ks = np.arange(1, 41)
    ax[0].plot(ks, [M.spearman_brown(one, m) for m in ks], color=labs.PURPLE, lw=2, label="Spearman-Brown")
    ax[0].plot(lengths, measured, "o", color=labs.BLUE, label="measured on the Pool")
    ax[0].set(title="Reliability against the number of items", xlabel="items", ylabel="reliability", ylim=(0, 1))
    ax[0].legend()
    show = np.random.default_rng(seed + 9).choice(n, 600, replace=False)
    ax[1].plot(s1["cost"][show], s2["cost"][show], ".", color=labs.PINK, alpha=0.5)
    ax[1].set(title=f"A person's conflict cost on two days (agreement {icc_cost:.2f})", xlabel="first session (ms)",
              ylabel="second session (ms)")
    out.fig = fig
    return out
