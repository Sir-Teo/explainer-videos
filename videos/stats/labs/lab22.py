"""Lab 22: fit a Poisson regression to overdispersed counts, and see which standard error tells the truth."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import mle

TITLE = "The sandwich under a wrong variance, and Neyman-Scott"
GOAL = ("Fit a Poisson regression 600 times to Poisson counts and to negative-binomial counts with the same mean, and "
        "compare the slope's true spread with the model-based and the sandwich standard errors; then watch the MLE of "
        "a variance converge to half the truth when every pair has its own mean.")
TASKS = [
    "Raise the negative binomial's k from 1.5 to 50. At what k do the model-based intervals cover 95% again?",
    "Use the quasi-Poisson standard error (fit['se_quasi']). Why is it close here, and for which variance is it exact?",
    "Give each group m = 5 readings instead of 2 in the Neyman-Scott check. What does the MLE converge to now?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, reps, beta, k = 400, 600, (0.5, 0.4), 1.5
    lab = labs.Lab()
    out = {}
    for name in ("Poisson", "negative binomial"):
        slopes, se_m, se_s, cov_m, cov_s = [], [], [], 0, 0
        for _ in range(reps):
            x = rng.normal(size=n)
            mu = np.exp(beta[0] + beta[1] * x)
            y = rng.poisson(mu) if name == "Poisson" else rng.negative_binomial(k, k / (k + mu))
            f = mle.poisson_regression(np.column_stack([np.ones(n), x]), y)
            b, sm, ss = f["b"][1], f["se_model"][1], f["se_sandwich"][1]
            slopes.append(b)
            se_m.append(sm)
            se_s.append(ss)
            cov_m += abs(b - beta[1]) < 1.96 * sm
            cov_s += abs(b - beta[1]) < 1.96 * ss
        r = out[name] = dict(slopes=np.array(slopes), sd=np.std(slopes), se_m=np.mean(se_m), se_s=np.mean(se_s),
                             cov_m=cov_m / reps, cov_s=cov_s / reps)
        lab.row(f"{name} counts: mean slope", f"{r['slopes'].mean():.3f}   (truth {beta[1]})")
        lab.row(f"{name} counts: true sd of the slope", f"{r['sd']:.4f}   model SE {r['se_m']:.4f}   sandwich SE {r['se_s']:.4f}")
        lab.row(f"{name} counts: 95% interval covers", f"model {r['cov_m']:.1%}   sandwich {r['cov_s']:.1%}")
    ns = [mle.neyman_scott(n_pairs, 1.0, rng) for n_pairs in (10, 30, 100, 300, 1000, 3000, 10000)]
    lab.row("Neyman-Scott, 10,000 pairs: MLE of sigma^2", f"{ns[-1]['mle']:.3f}   (truth 1, limit 0.5)")
    lab.row("Neyman-Scott, 10,000 pairs: divide by 2n", f"{ns[-1]['fixed']:.3f}   (truth 1)")
    lab.note = ("A wrong variance leaves the slope consistent but makes the model's standard error too small, and the "
                "sandwich measures the spread the scores really have; with a new mean per pair, more data never "
                "repairs the MLE of the variance.")
    p, nb = out["Poisson"], out["negative binomial"]
    assert abs(p["slopes"].mean() - beta[1]) < 0.01 and abs(nb["slopes"].mean() - beta[1]) < 0.02, "the mean model is right"
    assert abs(p["se_m"] / p["sd"] - 1) < 0.1 and abs(p["se_s"] / p["sd"] - 1) < 0.1, "A = B when the model is true"
    assert abs(p["cov_m"] - 0.95) < 0.035, "model-based intervals work for Poisson counts"
    assert nb["se_m"] / nb["sd"] < 0.75 and nb["cov_m"] < 0.87, "the model SE understates under overdispersion"
    assert abs(nb["se_s"] / nb["sd"] - 1) < 0.15 and nb["cov_s"] > 0.90, "the sandwich tracks the true spread"
    assert abs(ns[-1]["mle"] - 0.5) < 0.03 and abs(ns[-1]["fixed"] - 1) < 0.06, "Neyman-Scott: sigma^2 / 2"

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(beta[1] - 4 * nb["sd"], beta[1] + 4 * nb["sd"], 50)
    ax[0].hist(nb["slopes"], bins=bins, density=True, color=labs.BLUE, alpha=0.6, label="600 fitted slopes")
    for se, color, name in ((nb["se_m"], labs.RED, "model SE"), (nb["se_s"], labs.GREEN, "sandwich SE")):
        ax[0].plot(bins, np.exp(-0.5 * ((bins - beta[1]) / se) ** 2) / (se * np.sqrt(2 * np.pi)), color=color,
                   label=f"normal with the {name}")
    ax[0].set(title="Overdispersed counts: which SE matches the spread?", xlabel="fitted Poisson slope",
              ylabel="density")
    ax[0].legend(loc="upper left", fontsize=8)
    sizes = [10, 30, 100, 300, 1000, 3000, 10000]
    ax[1].semilogx(sizes, [r["mle"] for r in ns], "o-", color=labs.RED, label="MLE: divide by 4n")
    ax[1].semilogx(sizes, [r["fixed"] for r in ns], "o-", color=labs.GREEN, label="contrasts: divide by 2n")
    ax[1].axhline(1.0, color=labs.MUTED, ls="--", lw=1)
    ax[1].axhline(0.5, color=labs.MUTED, ls=":", lw=1)
    ax[1].set(title="Neyman-Scott: more pairs do not help the MLE", xlabel="number of pairs",
              ylabel="estimate of σ² (truth 1)", ylim=(0, 1.8))
    ax[1].legend()
    lab.fig = fig
    return lab
