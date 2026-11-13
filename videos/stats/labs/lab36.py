"""Lab 36: give the doubly robust estimator one wrong model, then two, and watch where its two chances run out."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import causal

TITLE = "Double robustness: two chances to be right"
GOAL = ("Simulate an observational study in which treatment and outcome both depend on x squared, and estimate the "
        "average effect (truth 2) by outcome regression, by weighting and by AIPW, with each nuisance model either "
        "right (it uses x squared) or wrong (linear in x), three hundred times each.")
TASKS = [
    "Raise the confounding from 0.8 to 2 so some propensities approach 1. What happens to IPW's largest weight and RMSE, and to AIPW's?",
    "Use causal.dml_ate with a flexible learner of your own (for example a k-nearest-neighbour mean) for both nuisances, cross-fitted.",
    "Add an unmeasured confounder u to both the treatment and the outcome models. Which of the twelve cells stays unbiased?",
]

TAU, N, CONF = 2.0, 1000, 0.8


def study(rng):
    x = rng.uniform(-2, 2, N)
    e = 1 / (1 + np.exp(-CONF * (x ** 2 - 1.3)))  # doctors treat the extremes more often
    t = rng.random(N) < e
    y = TAU * t + 3 * x ** 2 + rng.standard_normal(N)
    return x, t, y


def estimates(x, t, y, out_right, ps_right):
    feats = lambda ok: np.column_stack([x, x ** 2]) if ok else x[:, None]  # noqa: E731
    D = np.column_stack([np.ones(N), feats(out_right)])
    mu1 = D @ np.linalg.lstsq(D[t], y[t], rcond=None)[0]
    mu0 = D @ np.linalg.lstsq(D[~t], y[~t], rcond=None)[0]
    ps = causal.propensity(feats(ps_right), t.astype(float))
    a = causal.aipw(y, t, mu0, mu1, ps)
    return float(np.mean(mu1 - mu0)), causal.ipw(y, t, ps)["est"], a["est"], a["lo"] <= TAU <= a["hi"]


def run(seed=0):
    rng = np.random.default_rng(seed)
    reps = 300
    lab = labs.Lab()
    cases = [(True, True), (True, False), (False, True), (False, False)]
    names = {(True, True): "both right", (True, False): "outcome right, propensity wrong",
             (False, True): "outcome wrong, propensity right", (False, False): "both wrong"}
    res = {c: [] for c in cases}
    naive = []
    for _ in range(reps):
        x, t, y = study(rng)
        naive.append(y[t].mean() - y[~t].mean())
        for c in cases:
            res[c].append(estimates(x, t, y, *c))
    res = {c: np.array(v) for c, v in res.items()}
    bias = {c: res[c][:, :3].mean(0) - TAU for c in cases}
    lab.row("difference in means, no adjustment: bias", f"{np.mean(naive) - TAU:+.2f}   (truth {TAU})")
    for c in cases:
        b = bias[c]
        lab.row(f"{names[c]}: bias", f"outcome model {b[0]:+.2f}   IPW {b[1]:+.2f}   AIPW {b[2]:+.2f}   "
                                     f"(AIPW 90% interval covers {res[c][:, 3].mean():.0%})")
    se = {c: res[c][:, 2].std(ddof=1) / np.sqrt(reps) for c in cases}
    for c in cases[:3]:
        assert abs(bias[c][2]) < max(0.03, 4 * se[c]), f"AIPW is consistent with {names[c]}"
    assert abs(bias[(True, False)][1]) > 0.5 and abs(bias[(False, True)][0]) > 0.5, "each single method fails with its model wrong"
    assert abs(bias[(False, False)][2]) > 0.5, "with both models wrong nothing is left"
    assert 0.84 < res[(True, True)][:, 3].mean() < 0.96, "influence-function interval with both models right"
    assert abs(np.mean(naive) - TAU) > 0.5
    lab.note = ("AIPW's error is a product of the two models' errors: it vanishes if either the outcome model or the "
                "propensity model is right, and with both wrong it is as biased as the comparison nobody adjusted.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x, t, y = study(np.random.default_rng(seed + 1))
    ax[0].scatter(x[~t], y[~t], s=6, color=labs.BLUE, alpha=0.5, label="untreated")
    ax[0].scatter(x[t], y[t], s=6, color=labs.GOLD, alpha=0.5, label="treated")
    g = np.linspace(-2, 2, 100)
    ax[0].plot(g, 3 * g ** 2, color=labs.BLUE)
    ax[0].plot(g, 3 * g ** 2 + TAU, color=labs.GOLD)
    ax[0].set(title="One study: the treated sit at the extremes of x", xlabel="x", ylabel="outcome y")
    ax[0].legend(loc="upper center")
    w = 0.25
    pos = np.arange(4)
    for j, (lbl, col) in enumerate((("outcome model", labs.BLUE), ("IPW", labs.ORANGE), ("AIPW", labs.GREEN))):
        ax[1].bar(pos + (j - 1) * w, [bias[c][j] for c in cases], w, color=col, label=lbl)
    ax[1].axhline(np.mean(naive) - TAU, color=labs.RED, ls="--", label="no adjustment")
    ax[1].axhline(0, color=labs.MUTED, lw=1)
    ax[1].set_xticks(pos)
    ax[1].set_xticklabels(["both right", "outcome right,\npropensity\nwrong", "outcome wrong,\npropensity\nright", "both wrong"])
    ax[1].set(title="Bias of each estimator over 300 studies (truth 2)", ylabel="mean estimate minus truth", ylim=(-0.3, 4.4))
    ax[1].legend(loc="upper left", ncol=2)
    lab.fig = fig
    return lab
