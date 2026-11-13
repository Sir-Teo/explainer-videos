"""Lab 55: three exam answers checked by computation: optional stopping, a UMVUE, and the median's influence function."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import qual

TITLE = "Checking three qualifying-exam proofs with numbers"
GOAL = ("Problem 2: the walk stopped when it first reaches +1 has E S_T = 1 although E S at every bounded time is 0. "
        "Problem 3: (1 - 1/n)^T is unbiased for exp(-lambda) with the exact variance the proof gives, above the "
        "Cramer-Rao bound. Problem 8: the median's variance is 1/(4 n f(m)^2), and the Wald interval built on it "
        "covers.")
TASKS = [
    "Stop the walk at -a or +1 instead (qual.ruin(a, 1)). What are E S_T and E T now, and what happens to both as a "
    "grows?",
    "Print qual.poisson_umvue(n, 2) for n = 5, 10, 100. Does the UMVUE's variance approach the Cramer-Rao bound, and "
    "does it ever attain it?",
    "Draw the data for Problem 8 from a Cauchy law. The mean has no influence function with finite variance; does the "
    "median's interval still cover?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # ---- Problem 2: T = first time the simple random walk is at +1
    N = 4001
    fp = qual.first_passage(N)
    walks = np.cumsum(rng.choice(np.array([-1, 1], dtype=np.int16), size=(4000, 1001)), axis=1, dtype=np.int16)
    hit_sim = float(np.mean(walks.max(axis=1) >= 1))
    catalan = sum(qual.first_passage_pmf(k) for k in range(1, 502))  # P(T <= 1001) from the first-passage law
    lab.row("P(T <= 1,001): simulated, by dynamic programming, by Catalan numbers",
            f"{hit_sim:.3f}, {fp['hit'][1001]:.4f}, {catalan:.4f}")
    lab.row("P(T <= 4,001) and E[T ^ 4,001]", f"{fp['hit'][N]:.3f}, {fp['e_min'][N]:.1f}   (E T is infinite)")
    lab.row("E[S at T ^ m] = P(T <= m) + E[S_m; T > m] at m = 4,001",
            f"{fp['hit'][N]:.3f} + ({fp['tail_mean'][N]:.3f}) = {fp['hit'][N] + fp['tail_mean'][N]:.1e}   (and E S_T = 1)")
    assert abs(fp["hit"][1001] - catalan) < 1e-9 and abs(hit_sim - catalan) < 0.01, "the first-passage law"
    assert np.max(np.abs(fp["hit"] + fp["tail_mean"])) < 1e-9, "E S at T ^ m is 0 for every m: optional stopping, bounded"
    assert abs(fp["hit"][N] - 0.987) < 1e-3 and fp["e_min"][N] > 99, "T is finite a.s. but not integrable"

    # ---- Problem 3: the UMVUE of exp(-lambda) from n Poisson counts
    n, lam, reps = 10, 2.0, 400000
    T = rng.poisson(n * lam, reps)
    umvue, mle = (1 - 1 / n) ** T, np.exp(-T / n)
    th = qual.poisson_umvue(n, lam)
    lab.row("UMVUE of exp(-2), n = 10: simulated mean, variance", f"{umvue.mean():.5f}, {umvue.var():.5f}   "
            f"exact {th['target']:.5f}, {th['var_umvue']:.5f}   Cramer-Rao bound {th['crlb']:.5f}")
    lab.row("MLE exp(-mean): simulated bias, MSE", f"{mle.mean() - th['target']:+.5f}, "
            f"{np.mean((mle - th['target']) ** 2):.5f}   exact {th['mle_bias']:+.5f}, {th['mle_mse']:.5f}")
    assert abs(umvue.mean() - th["target"]) < 5e-4 and abs(umvue.var() / th["var_umvue"] - 1) < 0.02, "unbiased, exact variance"
    assert th["crlb"] < th["var_umvue"] < th["mle_mse"], "the bound is not attained, and the UMVUE beats the MLE here"
    assert abs(np.mean((mle - th["target"]) ** 2) / th["mle_mse"] - 1) < 0.02 and th["mle_bias"] > 0.005

    # ---- Problem 8: the median of 66 draws from t with 3 degrees of freedom
    m_n, sims = 66, 4000
    x = rng.standard_t(3, size=(sims, m_n))
    med = np.median(x, axis=1)
    f0 = stats.t.pdf(0, 3)
    covered = np.mean([(w := qual.median_wald(row))["lo"] <= 0 <= w["hi"] for row in x[:1500]])
    lab.row("median of 66 t3 draws: n Var simulated", f"{m_n * med.var():.3f}   1/(4 f(0)^2) = {1 / (4 * f0 ** 2):.3f}")
    lab.row("95% Wald interval from the influence function (KDE plug-in)", f"covers {covered:.1%}")
    assert abs(np.var(qual.median_if(x[0], 0.0, f0)) * 4 * f0 ** 2 - 1) < 0.05, "the influence function's variance"
    assert abs(m_n * med.var() * 4 * f0 ** 2 - 1) < 0.12 and 0.93 < covered < 0.995
    lab.note = ("Each proof leaves a number that can be checked: a stopped mean that is 0 at every bounded time and 1 "
                "in the limit, a variance strictly between the Cramer-Rao bound and the MLE's error, and a sampling "
                "variance equal to the influence function's.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    m = np.arange(1, N + 1)
    ax[0].semilogx(m, fp["hit"][1:], color=labs.GOLD, label="P(T <= m): mass stopped at +1")
    ax[0].semilogx(m, fp["tail_mean"][1:], color=labs.RED, label="E[S_m; T > m]: the walks still out")
    ax[0].semilogx(m, fp["hit"][1:] + fp["tail_mean"][1:], color=labs.INK, ls="--", label="their sum, E[S at T ^ m] = 0")
    ax[0].set(title="Problem 2: the walk stopped at +1", xlabel="time m", ylabel="contribution to the mean", ylim=(-1.1, 1.45))
    ax[0].legend(loc="upper left", ncols=1)
    tt = np.arange(4, 41)
    pmf = stats.poisson.pmf(tt, n * lam)
    ax[1].bar(tt, 0.3 * pmf / pmf.max(), color=labs.GREY, alpha=0.35, width=0.9, label="law of T, Poisson(20) (scaled)")
    ax[1].plot(tt, (1 - 1 / n) ** tt, "o-", ms=3, color=labs.BLUE, label="UMVUE (1 - 1/n)^T: unbiased")
    ax[1].plot(tt, np.exp(-tt / n), "o-", ms=3, color=labs.GOLD, label=f"MLE exp(-T/n): bias {th['mle_bias']:+.4f}")
    ax[1].axhline(th["target"], color=labs.INK, ls="--", label="the target exp(-2)")
    ax[1].set(title="Problem 3: two estimators of exp(-lambda), n = 10", xlabel="T, the total count", ylabel="estimate")
    ax[1].legend()
    lab.fig = fig
    return lab
