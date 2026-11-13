"""Lab 24: fit Bliss's beetles by IRLS under three links, and test the deviance's chi-squared approximation."""

import numpy as np
from scipy import special, stats

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import glm

TITLE = "Bliss's beetles, and when the deviance is chi-squared"
GOAL = ("Fit the logit, probit and complementary log-log to Bliss's eight doses with the series' IRLS, then simulate "
        "from a true logistic model to see the deviance come close to chi-squared for grouped data and fail for binary data.")
TASKS = [
    "Start IRLS for the cloglog link from zeros (start=np.zeros(2)). How many steps does it take, and does it halve?",
    "Halve every group size in the grouped simulation. At what size does the 5% test stop rejecting about 5%?",
    "For the binary data, compare the deviance drop between two nested models with chi-squared(1). Does Wilks hold?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    x, n, k = museum.bliss()
    X = np.column_stack([np.ones(len(x)), x])
    fits = {link: glm.glm_fit(X, k / n, glm.family("binomial", link), n=n) for link in ("logit", "probit", "cloglog")}
    cold = glm.glm_fit(X, k / n, glm.family("binomial"), n=n, start=np.zeros(2))
    ld = glm.ld50(fits["cloglog"])
    lab = labs.Lab()
    for link, film in (("logit", 11.23), ("probit", 10.12), ("cloglog", 3.45)):
        f = fits[link]
        lab.row(f"{link}: deviance on {f.df_resid} df", f"{f.deviance:.2f}   (the film: {film})")
    lab.row("IRLS from beta = 0: deviance path", " -> ".join(f"{d:.4g}" for d in cold.deviance_path[:5]))
    lab.row("cloglog LD50 (log dose), Fieller 95%", f"{ld['x']:.4f}   [{ld['fieller'][0]:.4f}, {ld['fieller'][1]:.4f}]")

    reps = 800
    p_true = special.expit(X @ fits["logit"].coef)  # a true logistic model at Bliss's doses and group sizes
    grouped = np.array([glm.glm_fit(X, rng.binomial(n.astype(int), p_true) / n, glm.family("binomial"), n=n).deviance
                        for _ in range(reps)])
    nb, binary = 200, []
    for _ in range(reps):
        xb = rng.normal(size=nb)
        yb = (rng.random(nb) < special.expit(0.3 + xb)).astype(float)
        binary.append(glm.glm_fit(np.column_stack([np.ones(nb), xb]), yb, glm.family("binomial")).deviance)
    binary = np.array(binary)
    rej_g = np.mean(grouped > stats.chi2.ppf(0.95, 6))
    rej_b = np.mean(binary > stats.chi2.ppf(0.95, nb - 2))
    lab.row("grouped data: deviance mean, sd", f"{grouped.mean():.2f}, {grouped.std():.2f}   (chi-squared(6): 6, 3.46)")
    lab.row("grouped data: a correct model rejected at 5%", f"{rej_g:.1%}")
    lab.row("binary data: deviance mean, sd", f"{binary.mean():.1f}, {binary.std():.1f}   (chi-squared(198): 198, 19.9)")
    lab.row("binary data: a correct model 'rejected' at 5%", f"{rej_b:.1%}")
    lab.note = ("With many beetles per dose the deviance is a rough goodness-of-fit test; with one trial per row it depends on "
                "the fitted probabilities alone and says nothing about fit.")
    for link, film in (("logit", 11.23), ("probit", 10.12), ("cloglog", 3.45)):
        assert abs(fits[link].deviance - film) < 0.01, f"{link} deviance"
    assert np.all(np.diff(cold.deviance_path) <= 1e-8) and np.allclose(cold.coef, fits["logit"].coef, atol=1e-6), "IRLS"
    assert abs(ld["x"] - 1.7788) < 2e-4 and ld["fieller"][0] < fits["logit"].coef[0] / -fits["logit"].coef[1] < ld["x"]
    assert abs(grouped.mean() - 6) < 1.0 and 0.03 < rej_g < 0.12, "grouped deviance is close to chi-squared(6)"
    assert binary.std() < 16 and abs(rej_b - 0.05) > 0.2, "binary deviance is not chi-squared(198)"

    fig, ax = labs.figure(3, size=(13.5, 4.2))
    grid = np.linspace(1.66, 1.91, 200)
    Xg = np.column_stack([np.ones(200), grid])
    ax[0].scatter(x, k / n, s=28, color=labs.INK, zorder=3, label="Bliss's eight doses")
    for link, color in (("logit", labs.BLUE), ("probit", labs.GREEN), ("cloglog", labs.GOLD)):
        ax[0].plot(grid, fits[link].fam.ginv(Xg @ fits[link].coef), color=color,
                   label=f"{link}: deviance {fits[link].deviance:.2f}")
    ax[0].set(title="Three links through the beetles", xlabel="log10 dose", ylabel="proportion killed")
    ax[0].legend(fontsize=8)
    for a, dev, df, name in ((ax[1], grouped, 6, "Grouped: 8 doses of about 60"), (ax[2], binary, nb - 2, "Binary: 200 single trials")):
        lo, hi = min(dev.min(), stats.chi2.ppf(0.001, df)), max(dev.max(), stats.chi2.ppf(0.999, df))
        g = np.linspace(lo, hi, 200)
        a.hist(dev, bins=30, density=True, color=labs.BLUE, alpha=0.6, label=f"{reps} deviances, model true")
        a.plot(g, stats.chi2.pdf(g, df), color=labs.RED, label=f"chi-squared({df})")
        a.axvline(stats.chi2.ppf(0.95, df), color=labs.MUTED, ls="--", lw=1)
        a.set(title=name, xlabel="residual deviance", ylabel="density")
        a.legend(fontsize=8)
    lab.fig = fig
    return lab
