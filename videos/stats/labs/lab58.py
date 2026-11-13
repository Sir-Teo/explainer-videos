"""Lab 58: look after every observation, with a z-test, a test martingale, the SPRT and a confidence sequence."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import sequential

TITLE = "Peeking, Ville's inequality and the SPRT"
GOAL = ("Check a 5% z-test after every observation of null data and count how often it ever rejects; do the same "
        "with a likelihood-ratio test martingale and Ville's threshold of 20, and with Robbins's mixture confidence "
        "sequence. Then compute Wald's SPRT for a defective rate of 10% against 20% exactly and compare its "
        "sample size with the fixed test's.")
TASKS = [
    "Change the martingale's bet mu1 from 0.2 to 0.05 and to 1. Ville's bound holds each time; which bet crosses 20 soonest when the true mean is 0.2?",
    "Replace the normal data by centred exponentials (rng.exponential(size) - 1). Does the mixture confidence sequence, built for sub-Gaussian data, still cover at every time?",
    "Evaluate sequential.sprt_bernoulli_exact at p = 0.15, between the hypotheses. How does the expected sample size compare with the fixed test's 109, and what does Wald's approximation say?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    alpha, T, reps = 0.05, 1000, 4000
    lab = labs.Lab()

    # 1. peeking against Ville, on N(0, 1) data
    looks = np.array([1, 10, 100, 1000])
    peek = sequential.peeking_curve(looks, alpha, reps, rng)
    v = sequential.ville_check(T, 0.2, alpha, reps, rng)
    for n, p in zip(looks, peek):
        lab.row(f"z-test rejects a true null within {n} look{'s' if n > 1 else ''}", f"{p:.1%}   nominal {alpha:.0%}")
    lab.row("test martingale ever reaches 20 in 1,000 looks", f"{v['ville']:.1%}   Ville's bound {alpha:.0%}")

    # 2. a confidence sequence against the fixed-n interval, at every time from 10 to 1,000
    z = stats.norm.isf(alpha / 2)
    t = np.arange(1, T + 1)

    def clt(x):
        m = np.cumsum(x) / t
        return m - z / np.sqrt(t), m + z / np.sqrt(t)

    def mixture(x):
        return sequential.normal_mixture_cs(np.cumsum(x) / t, t, alpha)

    def sampler(r, n):
        return r.standard_normal(n)

    c_clt = sequential.cs_coverage(clt, sampler, T, 1500, 0.0, rng, t_min=10)
    c_mix = sequential.cs_coverage(mixture, sampler, T, 1500, 0.0, rng, t_min=10)
    lab.row("fixed-n interval covers at every t in [10, 1000]", f"{c_clt['uniform']:.1%}   (at t = 1000 alone: {c_clt['final']:.1%})")
    lab.row("mixture confidence sequence covers at every t", f"{c_mix['uniform']:.1%}   guarantee at least {1 - alpha:.0%}")

    # 3. Wald's SPRT, exactly: defective rate 10% against 20%, alpha 5%, beta 10%
    p0, p1, beta = 0.1, 0.2, 0.1
    fixed = sequential.fixed_n_binomial(p0, p1, alpha, beta)
    e0 = sequential.sprt_bernoulli_exact(p0, p0, p1, alpha, beta)
    e1 = sequential.sprt_bernoulli_exact(p1, p0, p1, alpha, beta)
    w0 = sequential.sprt_wald_approx(p0, p0, p1, alpha, beta)
    lab.row("SPRT expected sample size at p = 0.1", f"{e0['asn']:.1f}   Wald's approximation {w0['asn']:.1f}   fixed test n = {fixed['n']}")
    lab.row("SPRT expected sample size at p = 0.2", f"{e1['asn']:.1f}")
    lab.row("SPRT error rates", f"{e0['accept_h1']:.1%} and {e1['accept_h0']:.1%}   targets {alpha:.0%} and {beta:.0%}")
    lab.note = ("A fixed-n test looked at every step rejects a true null about half the time within a thousand looks; "
                "a nonnegative martingale crosses 1/alpha with probability at most alpha however often you look, "
                "and the SPRT built on that idea needs about half the fixed test's sample.")
    assert peek[0] < 0.07 and peek[2] > 0.3 and peek[3] > 0.45 and np.all(np.diff(peek) > 0), "peeking inflates the error"
    assert 0.01 < v["ville"] <= alpha + 0.01, "Ville's inequality holds and is not vacuous"
    assert c_mix["uniform"] >= 0.95 and c_clt["uniform"] < 0.75 and abs(c_clt["final"] - 0.95) < 0.025, "only the confidence sequence is time-uniform"
    assert e0["accept_h1"] <= alpha and e1["accept_h0"] <= beta, "Wald's thresholds keep both error rates"
    assert max(e0["asn"], e1["asn"]) < 0.6 * fixed["n"] and abs(w0["asn"] / e0["asn"] - 1) < 0.15, "the SPRT's saving"

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.unique(np.round(np.logspace(0, 3, 40)).astype(int))
    curve = sequential.peeking_curve(grid, alpha, 2000, rng)
    ax[0].plot(grid, curve, color=labs.RED, label="z-test, checked after every observation")
    ax[0].axhline(v["ville"], color=labs.GREEN, label=f"martingale ever at 20 (1,000 looks): {v['ville']:.1%}")
    ax[0].axhline(alpha, color=labs.MUTED, ls="--", lw=1, label="nominal 5%")
    ax[0].set(title="Chance of ever rejecting a true null", xlabel="number of looks (log scale)", ylabel="probability",
              xscale="log", ylim=(0, 0.62))
    ax[0].legend(loc="upper left")
    x = rng.standard_normal(T)
    for _ in range(200):  # a stream whose fixed-n interval excludes the truth at some time after 10
        lo, hi = clt(x)
        if ((lo > 0) | (hi < 0))[9:].any():
            break
        x = rng.standard_normal(T)
    lo, hi = clt(x)
    mlo, mhi = mixture(x)
    out = np.flatnonzero((lo > 0) | (hi < 0))
    out = out[out >= 9]
    ax[1].fill_between(t, mlo, mhi, color=labs.GOLD, alpha=0.18, label="mixture confidence sequence")
    ax[1].fill_between(t, lo, hi, color=labs.BLUE, alpha=0.35, label="fixed-n 95% interval")
    ax[1].plot(t, np.cumsum(x) / t, color=labs.INK, lw=1.2, label="running mean")
    ax[1].plot(t[out], np.zeros(len(out)), ".", color=labs.RED, ms=4, label="fixed-n interval excludes the truth")
    ax[1].axhline(0, color=labs.MUTED, lw=1)
    ax[1].set(title="One null stream: two bands around the running mean", xlabel="observations (log scale)", ylabel="mean",
              xscale="log", xlim=(10, T), ylim=(-1.3, 1.8))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
