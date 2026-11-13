"""Lab 50: Pinsker's taper against the best cut-off, its least favourable prior, and its exact constant."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import gsm

TITLE = "Pinsker's theorem in the Gaussian sequence model"
GOAL = ("Over a Sobolev ellipsoid (a_k = k, C = 1) compute Pinsker's linear minimax rule and risk, check by "
        "simulation that the rule's risk at a hard truth is that risk, that the least favourable Gaussian prior's "
        "Bayes risk equals it, and that the best projection estimator is worse by a factor tending to 3^(2/3).")
TASKS = [
    "Change the smoothness alpha from 1 to 2. Derive the limit of the projection ratio and check it against the table.",
    "Put all of C^2 on the first coordinate (theta_1 = C/a_1). Is the simulated risk of Pinsker's rule still the "
    "minimax risk? Then put it on a coordinate beyond the taper's support.",
    "Replace gsm.est_block_js by gsm.est_soft with the universal threshold eps*sqrt(2 log K) and compare its risk "
    "at the hard truth.",
]


def projection_worst(eps, a, C):
    """The smallest worst-case risk of a projection estimator: min over N of C^2 / a_{N+1}^2 + eps^2 N."""
    N = np.arange(1, len(a))
    r = C ** 2 / a[N] ** 2 + eps ** 2 * N
    return float(r.min()), int(N[r.argmin()])


def run(seed=0):
    rng = np.random.default_rng(seed)
    alpha, C, K = 1.0, 1.0, 4000
    a = gsm.sobolev_weights(K, alpha)
    lab = labs.Lab()
    grid = [0.1, 0.03, 0.01, 0.003, 0.001]
    ratio_asym, ratio_proj = [], []
    for eps in grid:
        p = gsm.pinsker(eps, a, C)
        ratio_asym.append(p["risk"] / gsm.pinsker_asymptotic(eps, alpha, C))
        ratio_proj.append(projection_worst(eps, a, C)[0] / p["risk"])
        assert abs(p["bayes"] / p["risk"] - 1) < 1e-9, "the Gaussian prior's Bayes risk is the linear minimax risk"
    for eps, ra, rp in zip(grid, ratio_asym, ratio_proj):
        lab.row(f"eps = {eps}: linear minimax / asymptotic formula", f"{ra:.4f}   best projection / Pinsker {rp:.4f}")
    limit = 3 ** (2 / 3)
    assert all(x < y for x, y in zip(ratio_asym, ratio_asym[1:])) and 0.99 < ratio_asym[-1] < 1.0, "Pinsker's constant"
    assert abs(ratio_proj[-1] / limit - 1) < 0.02, "a cut-off loses the factor 3^(2/3) when alpha = 1"

    # simulate at a truth on the ellipsoid's boundary, where the taper's risk is the minimax risk
    eps = 0.01
    p = gsm.pinsker(eps, a, C)
    theta = gsm.hardest_theta(eps, a, C)
    y = theta + eps * rng.standard_normal((2000, K))
    risk = lambda est: float(np.mean(np.sum((est - theta) ** 2, axis=1)))  # noqa: E731
    r_pin = risk(gsm.est_linear(y, p["shrink"]))
    r_proj = risk(gsm.est_truncation(y, projection_worst(eps, a, C)[1]))
    r_bjs = risk(gsm.est_block_js(y, eps))
    lab.row("eps = 0.01: Pinsker's rule at the hard truth, simulated", f"{r_pin:.6f}   minimax linear risk {p['risk']:.6f}")
    lab.row("the best cut-off at the same truth", f"{r_proj:.6f}   ({r_proj / p['risk']:.2f} x)")
    lab.row("blockwise James-Stein, told neither alpha nor C", f"{r_bjs:.6f}   ({r_bjs / p['risk']:.2f} x)")
    assert abs(np.sum(a ** 2 * theta ** 2) - C ** 2) < 1e-9, "the truth is on the boundary"
    assert abs(r_pin / p["risk"] - 1) < 0.02, "the taper's risk on the boundary is the minimax risk"
    assert r_pin < r_proj and r_pin < r_bjs < 2.5 * p["risk"], "the adaptive rule pays a bounded factor here"
    lab.note = ("The taper (1 - a_k/mu)+ is minimax among linear rules, a Gaussian prior makes it Bayes, and its "
                "risk approaches P(alpha) C^(2/(2 alpha+1)) eps^(4 alpha/(2 alpha+1)); a hard cut-off is rate "
                "optimal but loses a constant.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    k = np.arange(1, 121)
    N = projection_worst(eps, a, C)[1]
    ax[0].plot(k, p["shrink"][:120], color=labs.GOLD, label=f"Pinsker's taper (1 - k/mu)+, mu = {p['mu']:.1f}")
    ax[0].step(k, (k <= N).astype(float), where="mid", color=labs.BLUE, label=f"the best cut-off, N = {N}")
    ax[0].plot(k, p["prior_var"][:120] / p["prior_var"][0], color=labs.GREEN, ls="--",
               label="least favourable prior variance (scaled)")
    ax[0].set(title="Weights on coordinate k at eps = 0.01", xlabel="k", ylabel="weight")
    ax[0].legend(loc="upper right")
    ax[1].semilogx(grid, ratio_asym, "o-", color=labs.GOLD, label="linear minimax risk / Pinsker's asymptotic formula")
    ax[1].semilogx(grid, ratio_proj, "o-", color=labs.BLUE, label="best projection / Pinsker")
    ax[1].axhline(limit, color=labs.BLUE, ls=":", lw=1)
    ax[1].axhline(1, color=labs.GOLD, ls=":", lw=1)
    ax[1].text(grid[-1], limit + 0.05, "3^(2/3) = 2.08", color=labs.MUTED, ha="right")
    ax[1].invert_xaxis()
    ax[1].set(title="As the noise falls", xlabel="noise level eps (decreasing)", ylabel="ratio of risks", ylim=(0.7, 2.6))
    ax[1].legend(loc="center right")
    lab.fig = fig
    return lab
