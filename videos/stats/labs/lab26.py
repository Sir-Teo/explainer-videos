"""Lab 26: fit the eight schools' hierarchical model on a grid and check the grid against brute-force integration."""

import numpy as np
from scipy import integrate, stats

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import bayes

TITLE = "The eight schools: tau on a grid, then mu, then the effects"
GOAL = ("Compute the marginal posterior of tau for Rubin's eight schools with statkit's hier_normal, check it against "
        "direct numerical integration over mu, then draw from the joint posterior and read off the film's numbers.")
TASKS = [
    "Pass log_prior_tau=lambda t: -np.log1p((t / 25) ** 2) (a half-Cauchy with scale 25). How far does tau's median move?",
    "Keep only schools A, B and C. Where is tau's median now, and what does that say about a flat prior with three groups?",
    "Divide every standard error by 3. Watch the conditional means stop pooling and tau's posterior leave zero.",
]

TAU = np.r_[np.linspace(0, 0.1, 101), np.geomspace(0.101, 1e6, 10000)]  # the film's wide nonuniform grid


def quantile(h, q):
    cdf = integrate.cumulative_trapezoid(h.post_tau, h.tau, initial=0)
    return float(np.interp(q, cdf / cdf[-1], h.tau))


def run(seed=0):
    rng = np.random.default_rng(seed)
    names, y, s = museum.eight_schools()
    h = bayes.hier_normal(y, s, TAU)
    lab = labs.Lab()

    # Brute force: p(tau | y) is the integral over mu of prod_j N(y_j | mu, sigma_j^2 + tau^2), under flat priors.
    def brute(tau):
        f = lambda mu: np.exp(stats.norm.logpdf(y, mu, np.sqrt(s ** 2 + tau ** 2)).sum() + 30)
        return integrate.quad(f, -200, 200, points=[0, 8, 16], epsabs=0, epsrel=1e-10)[0]

    checks = np.array([0.0, 2.0, 5.0, 10.0, 20.0])
    kit = np.interp(checks, h.tau, h.post_tau)
    ref = np.array([brute(t) for t in checks])
    err = np.max(np.abs(kit / kit[0] - ref / ref[0]) / (ref / ref[0]))
    lab.row("grid density against integration over mu", f"largest relative error {err:.1e} at tau = 0, 2, 5, 10, 20")
    assert err < 1e-3, "the closed-form marginal agrees with brute-force integration"

    pooled, pooled_se = h.mu_hat[0], np.sqrt(h.v_mu[0])
    lab.row("complete pooling (tau = 0)", f"{pooled:.1f} +/- {pooled_se:.1f}   (film: 7.7 +/- 4.1)")
    assert abs(pooled - 7.7) < 0.05 and abs(pooled_se - 4.1) < 0.05

    med, lo, hi = (quantile(h, q) for q in (0.5, 0.025, 0.975))
    lab.row("tau: posterior median, 95% interval", f"{med:.1f}  [{lo:.1f}, {hi:.1f}]   (film: 5.2 [0.2, 20.8])")
    assert abs(med - 5.2) < 0.1 and abs(lo - 0.2) < 0.1 and abs(hi - 20.8) < 0.3
    assert h.post_tau.argmax() == 0, "the posterior mode of tau is on the boundary"

    d = bayes.hier_normal(y, s, TAU).draws(40000, rng)
    th = d["theta"]
    a_med, a_lo, a_hi = np.percentile(th[:, 0], [50, 2.5, 97.5])
    p_ac = np.mean(th[:, 0] > th[:, 2])
    p_best = np.mean(th.argmax(1) == 0)
    lab.row("school A (y = 28): posterior median, interval", f"{a_med:.1f}  [{a_lo:.1f}, {a_hi:.1f}]   (film: 10.2 [-2.2, 31.6])")
    lab.row("school C (y = -3): posterior median", f"{np.median(th[:, 2]):.1f}   (film: 6.7)")
    lab.row("P(theta_A > theta_C)", f"{p_ac:.3f}   (film: 0.68)")
    lab.row("P(A is the best school)", f"{p_best:.3f}   (film: 0.25; 1/8 a priori)")
    assert abs(a_med - 10.2) < 0.5 and abs(np.median(th[:, 2]) - 6.7) < 0.5
    assert abs(p_ac - 0.68) < 0.02 and abs(p_best - 0.25) < 0.02
    assert a_hi - a_lo < 2 * 1.96 * s[0], "partial pooling narrows A's interval"
    lab.note = ("The posterior for tau peaks at zero but its median is 5: averaging over it pulls school A from 28 "
                "to about 10 without forcing all eight schools to one number.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    keep = h.tau <= 30
    mean, _ = h.cond_theta()
    for j, name in enumerate(names):
        ax[0].plot(h.tau[keep], mean[keep, j], color=labs.CYCLE[j], label=f"{name} (y = {y[j]:.0f})")
    ax[0].plot(h.tau[keep], h.mu_hat[keep], color=labs.MUTED, ls="--", label="mu")
    ax[0].axvline(med, color=labs.GREY, lw=0.8, ls=":")
    ax[0].set(title="Each school's estimate given tau", xlabel="tau (between-school sd)", ylabel="E(theta_j | tau, y)")
    ax[0].legend(ncol=3, fontsize=8, loc="upper left")
    ax[1].hist(d["tau"], bins=np.linspace(0, 30, 61), density=True, color=labs.BLUE, alpha=0.45,
               label="40,000 draws of tau")
    ax[1].plot(h.tau[keep], h.post_tau[keep], color=labs.GOLD, label="p(tau | y) on the grid")
    ax[1].axvline(med, color=labs.GREY, lw=0.8, ls=":", label=f"median {med:.1f}")
    ax[1].set(title="The posterior of tau: mode at 0, long tail", xlabel="tau", ylabel="density")
    ax[1].legend()
    lab.fig = fig
    return lab
