"""Lab 46: check that a test with Neyman structure is similar, that the UMPU test is unbiased, and Fieller's coverage."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import testing

TITLE = "Similar tests, unbiased tests, and an interval that must sometimes be infinite"
GOAL = ("Compute the size of the conditional two-binomial test at every value of the nuisance parameter, with and "
        "without randomization; compare the UMPU and equal-tailed binomial tests near the null; then simulate a ratio "
        "of normal means and compare Fieller's set with the delta-method interval.")
TASKS = [
    "Change the group sizes from 8 and 10 to 30 and 40. How close to 5% does Fisher's exact test (no randomization) get?",
    "Move the binomial null from p0 = 0.3 to p0 = 0.5. Why do the UMPU and equal-tailed tests now coincide?",
    "Give the numerator and denominator estimates a correlation of 0.8 (use the cab argument of testing.fieller). Does Fieller still cover 95%?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    alpha = 0.05

    # 1. Neyman structure: X ~ Bin(8, p1), Y ~ Bin(10, p2), H0: p1 <= p2.  Each slice X + Y = t is tested at level alpha.
    m, n = 8, 10
    ps = np.linspace(0.02, 0.98, 97)
    size_r = testing.unconditional_size(testing.conditional_test(m, n, alpha)["phi"], m, n, ps)
    size_f = testing.unconditional_size(testing.conditional_test(m, n, alpha, randomized=False)["phi"], m, n, ps)
    lab.row("randomized conditional test: size over p", f"{size_r.min():.4f} to {size_r.max():.4f}   (similar: {alpha} at every p)")
    lab.row("Fisher's exact test: size over p", f"{size_f.min():.4f} to {size_f.max():.4f}   (at most {alpha})")
    assert np.allclose(size_r, alpha, atol=1e-10), "every slice spends exactly alpha, so the test is similar"
    assert size_f.max() < 0.03, "without randomization the test is conservative"

    # 2. UMPU against equal tails for Bin(20, p), H0: p = 0.3.
    N, p0 = 20, 0.3
    u = testing.umpu_binomial(N, p0, alpha)
    grid = np.linspace(0.2, 0.4, 2001)
    pow_u = testing.power(u["phi"], N, grid)
    pow_e = testing.power(testing.equal_tailed_binomial(N, p0, alpha), N, grid)
    lab.row("UMPU test of p = 0.3, n = 20", f"reject x < {u['c1']} or x > {u['c2']}, with probability {u['g1']:.3f} at {u['c1']} and {u['g2']:.3f} at {u['c2']}")
    lab.row("UMPU: lowest power near the null", f"{pow_u.min():.5f} at p = {grid[pow_u.argmin()]:.3f}   (unbiased: {alpha} at p0)")
    lab.row("equal tails: lowest power near the null", f"{pow_e.min():.5f} at p = {grid[pow_e.argmin()]:.3f}   (biased: below {alpha})")
    assert abs(pow_u.min() - alpha) < 1e-9 and abs(grid[pow_u.argmin()] - p0) < 1e-3, "the UMPU power is smallest at p0"
    assert pow_e.min() < alpha - 5e-5 and abs(grid[pow_e.argmin()] - p0) > 2e-3, "the equal-tailed test is biased"

    # 3. Fieller: a ~ N(1, 1), b ~ N(beta, 1), the ratio 1 / beta.  The set is bounded, two rays, or the whole line.
    reps, betas = 4000, (4.0, 2.0, 1.0, 0.5)
    z = stats.norm.ppf(0.975)
    cover_f, cover_d, bounded = [], [], []
    for beta in betas:
        rho = 1 / beta
        a, b = 1 + rng.standard_normal(reps), beta + rng.standard_normal(reps)
        hit, bd = 0, 0
        for ai, bi in zip(a, b):
            s = testing.fieller(ai, bi, 1.0, 1.0)
            inside = s["lo"] <= rho <= s["hi"] if s["kind"] != "all" else True
            hit += inside if s["kind"] != "exclusive" else not (s["lo"] < rho < s["hi"])
            bd += s["kind"] == "bounded"
        se = np.sqrt(1 / b ** 2 + a ** 2 / b ** 4)  # the delta method for a / b
        cover_f.append(hit / reps)
        bounded.append(bd / reps)
        cover_d.append(float(np.mean(np.abs(a / b - rho) <= z * se)))
        lab.row(f"denominator mean {beta:g}: coverage of the ratio", f"Fieller {cover_f[-1]:.1%} (bounded {bounded[-1]:.0%} of the time)   delta method {cover_d[-1]:.1%}")
    assert np.all(np.abs(np.array(cover_f) - 0.95) < 0.015), "Fieller's pivot is exact"
    assert cover_d[-1] < 0.85 and bounded[-1] < 0.2, "a bounded interval cannot cover when the denominator is near 0"
    lab.note = ("Conditioning on the total makes the test's size free of the nuisance parameter; the UMPU test's power "
                "bottoms out exactly at the null; and Fieller keeps 95% only by returning unbounded sets.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    ax[0].plot(ps, size_r, color=labs.GOLD, label="randomized conditional test")
    ax[0].plot(ps, size_f, color=labs.BLUE, label="Fisher's exact test")
    ax[0].axhline(alpha, color=labs.MUTED, ls=":", lw=1)
    ax[0].set(title="Size against the nuisance parameter (8 and 10 trials)", xlabel="common success probability p",
              ylabel="P(reject) when p1 = p2 = p", ylim=(0, 0.07))
    ax[0].legend(loc="lower center")
    xpos = np.arange(len(betas))
    ax[1].bar(xpos - 0.2, cover_f, 0.4, color=labs.GOLD, label="Fieller's set")
    ax[1].bar(xpos + 0.2, cover_d, 0.4, color=labs.RED, label="delta-method interval")
    ax[1].plot(xpos, bounded, "o--", color=labs.BLUE, label="share of Fieller sets that are bounded")
    ax[1].axhline(0.95, color=labs.MUTED, ls=":", lw=1)
    ax[1].set_xticks(xpos, [f"{b:g}" for b in betas])
    ax[1].set(title="A ratio of normal means: 95% sets", xlabel="denominator mean (its SE is 1)", ylabel="coverage", ylim=(0, 1.3))
    ax[1].legend(loc="upper left", ncols=1)
    lab.fig = fig
    return lab
