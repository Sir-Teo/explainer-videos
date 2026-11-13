"""Lab 62: hide a confounder, keep two noisy proxies of it, and compare adjustment with proximal two-stage least squares."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import frontier

TITLE = "Proximal inference: two proxies in place of a hidden confounder"
GOAL = ("Simulate a treatment and an outcome that share an unmeasured cause U, seen only through a treatment proxy Z "
        "and an outcome proxy W. Compare regression that adjusts for the proxies with proximal two-stage least "
        "squares, and then break the exclusion restriction the proximal estimator relies on.")
TASKS = [
    "Raise the proxies' noise sd from 0.7 to 2. What happens to the proximal estimate's spread, and to the bias of "
    "ordinary adjustment?",
    "Make W a proxy of something else (replace U by fresh noise in W). Which step of two-stage least squares fails, "
    "and how does the standard error show it?",
    "Replace the simulated truth 1 by 0 and count how often each 95% interval excludes zero.",
]

TRUTH, GAMMA, NOISE = 1.0, 1.5, 0.7


def draw(n, rng, direct=0.0):
    """One sample: U hidden; A and Y depend on it; Z and W are U plus noise; ``direct`` is Z's own effect on Y."""
    u = rng.standard_normal(n)
    a = (0.9 * u + rng.standard_normal(n) > 0).astype(float)
    z = u + NOISE * rng.standard_normal(n)
    w = u + NOISE * rng.standard_normal(n)
    y = 0.5 + TRUTH * a + GAMMA * u + direct * z + rng.standard_normal(n)
    return y, a, z, w


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, reps = 400, 200
    lab = labs.Lab()
    est = {"unadjusted": [], "adjusted for Z and W": [], "proximal": [], "proximal, Z affects Y": []}
    cover = 0
    for _ in range(reps):
        y, a, z, w = draw(n, rng)
        est["unadjusted"].append(frontier.ols_adjusted(y, a, np.empty((n, 0)))["effect"])
        est["adjusted for Z and W"].append(frontier.ols_adjusted(y, a, np.column_stack([z, w]))["effect"])
        p = frontier.proximal_2sls(y, a, z, w)
        est["proximal"].append(p["effect"])
        cover += abs(p["effect"] - TRUTH) <= 1.96 * p["se"]
        y, a, z, w = draw(n, rng, direct=0.4)
        est["proximal, Z affects Y"].append(frontier.proximal_2sls(y, a, z, w)["effect"])
    est = {k: np.array(v) for k, v in est.items()}
    for k, v in est.items():
        lab.row(f"{k}: mean estimate", f"{v.mean():.3f}   (sd {v.std(ddof=1):.3f}; truth {TRUTH})")
    cover /= reps
    lab.row("proximal 95% interval covers the truth", f"{cover:.1%}")
    lab.note = ("Adjusting for noisy proxies removes only part of the confounding; treating one proxy as an instrument "
                "for the other removes all of it, until the instrument has its own path to the outcome.")
    assert est["unadjusted"].mean() - TRUTH > 1.0, "the hidden cause biases the raw contrast"
    assert est["adjusted for Z and W"].mean() - TRUTH > 0.2, "noisy proxies leave residual confounding"
    assert abs(est["proximal"].mean() - TRUTH) < 0.06, "proximal 2SLS is centred on the truth"
    assert 0.89 <= cover <= 0.99, "its sandwich interval covers about 95%"
    assert est["proximal, Z affects Y"].mean() - TRUTH < -0.2, "an excluded path from Z to Y breaks it"

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(0.2, 3.2, 70)
    for (k, v), color in zip(list(est.items())[:3], (labs.RED, labs.ORANGE, labs.GREEN)):
        ax[0].hist(v, bins=bins, color=color, alpha=0.65, label=k)
    ax[0].axvline(TRUTH, color=labs.INK, ls="--", lw=1.2, label="truth")
    ax[0].set(title=f"{reps} samples of {n}: three estimates of the effect", xlabel="estimated effect of A on Y",
              ylabel="samples")
    ax[0].legend()
    bins = np.linspace(-0.4, 1.8, 60)
    ax[1].hist(est["proximal"], bins=bins, color=labs.GREEN, alpha=0.65, label="exclusion holds")
    ax[1].hist(est["proximal, Z affects Y"], bins=bins, color=labs.PURPLE, alpha=0.65, label="Z also affects Y directly")
    ax[1].axvline(TRUTH, color=labs.INK, ls="--", lw=1.2, label="truth")
    ax[1].set(title="Proximal estimates with and without the exclusion", xlabel="estimated effect of A on Y")
    ax[1].legend()
    lab.fig = fig
    return lab
