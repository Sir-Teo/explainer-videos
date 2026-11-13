"""Lab 44: bet against a fair coin, stop when you like, and check Ville, optional stopping and the coupling bound."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import chains

TITLE = "Fair games in time: Ville's inequality, gambler's ruin and coupling"
GOAL = ("Watch 10,000 likelihood-ratio wealth paths under a fair coin for 1,000 tosses and count how many ever reach "
        "wealth 10, against a z test that peeks every tenth toss; then check gambler's ruin against optional stopping, "
        "and the lazy walk's distance from uniform against the tail of a coupling time.")
TASKS = [
    "Make the coin truly biased (p = 0.55) and plot the time at which wealth first reaches 10. How does it depend on the bet p1?",
    "Let the z test peek at every toss instead of every tenth. How large does its false alarm rate become by n = 1,000, and by 10,000?",
    "Change the cycle's length from 20 to 40. By what factor do the mixing time and the mean coupling time grow?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Ville: a nonnegative martingale started at 1 reaches 1 / alpha with probability at most alpha, at any time.
    reps, n, alpha = 10_000, 1000, 0.10
    x = rng.random((reps, n)) < 0.5
    wealth = chains.betting_paths(x, 0.5, 0.6)
    cross = float(np.mean(wealth.max(axis=1) >= 1 / alpha))
    looks = np.arange(10, n + 1, 10)
    heads = np.cumsum(x, axis=1)[:, looks - 1]
    z = (heads - looks / 2) / np.sqrt(looks / 4)
    peek = float(np.mean(np.any(np.abs(z) > 1.6449, axis=1)))
    fixed = float(np.mean(np.abs(z[:, -1]) > 1.6449))
    lab.row("wealth paths ever reaching 10 in 1,000 tosses", f"{cross:.1%}   (Ville: at most {alpha:.0%})")
    lab.row("z test at the last toss only, size 10%", f"{fixed:.1%}   (nominal 10%)")
    lab.row("z test at every 10th toss, size 10% each", f"{peek:.1%}   false alarms")
    lab.row("mean wealth at toss 20", f"{wealth[:, 19].mean():.3f}   (a martingale: 1)")
    assert cross <= alpha + 0.01, "Ville's inequality (0.01 is three Monte Carlo standard errors)"
    assert abs(wealth[:, 19].mean() - 1) < 0.05, "the wealth is a martingale with mean 1"
    assert abs(fixed - 0.10) < 0.02 and peek > 0.4, "peeking breaks the fixed-sample test"

    # 2. Optional stopping: P(reach b before 0) from a, for a fair coin and for red at American roulette.
    a, b, m = 10, 20, 20_000
    sims = {}
    for name, p in (("fair coin", 0.5), ("roulette, red (18/38)", 18 / 38)):
        pos, t, alive = np.full(m, a), np.zeros(m), np.ones(m, bool)
        while alive.any():
            pos[alive] += np.where(rng.random(alive.sum()) < p, 1, -1)
            t[alive] += 1
            alive = (pos > 0) & (pos < b)
        th = chains.ruin(p, a, b)
        sims[name] = (float(np.mean(pos == b)), float(t.mean()), th)
        lab.row(f"{name}: P(10 becomes 20)", f"{sims[name][0]:.3f}   (theory {th['win']:.3f})")
        lab.row(f"{name}: mean number of bets", f"{sims[name][1]:.1f}   (theory {th['duration']:.1f})")
        assert abs(sims[name][0] - th["win"]) < 0.015 and abs(sims[name][1] / th["duration"] - 1) < 0.04, "ruin"

    # 3. Coupling: max_x ||P^t(x, .) - pi||_TV <= P(coupling time > t) on the lazy cycle of 20.
    k = 20
    P = chains.lazy_cycle(k)
    pi = np.full(k, 1 / k)
    ts = np.arange(0, 301, 2)
    d = chains.distance_curve(P, pi, ts[1:], starts=[0])
    d = np.concatenate([[1 - 1 / k], d])
    tau = chains.coupling_time_cycle(k, 1500, rng)
    tail = np.array([np.mean(tau > t) for t in ts])
    tmix, relax = chains.mixing_time(P, pi, starts=[0]), 1 / chains.spectral_gap(P)
    lab.row("lazy cycle of 20: mixing time, relaxation time", f"{tmix}, {relax:.1f}")
    lab.row("mean coupling time", f"{tau.mean():.1f}   (theory (20/2)^2 = 100)")
    assert np.all(d <= tail + 0.04), "the coupling inequality"
    assert abs(tau.mean() - 100) < 8, "the gap is a fair walk from 10 to 0 or 20"
    lab.note = ("A fair bet stays fair under any stopping rule: the wealth test keeps its 10% under continuous "
                "monitoring while the peeking z test does not, and a coupling time bounds the distance to stationarity.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    hit = wealth.max(axis=1) >= 1 / alpha
    steps = np.arange(1, n + 1)
    for i in range(40):
        ax[0].semilogy(steps, wealth[i], lw=0.7, alpha=0.9 if hit[i] else 0.45, color=labs.GOLD if hit[i] else labs.BLUE)
    ax[0].axhline(1 / alpha, color=labs.RED, ls="--", label="wealth 10 = 1 / alpha")
    ax[0].plot([], [], color=labs.BLUE, label="wealth paths under a fair coin")
    ax[0].plot([], [], color=labs.GOLD, label=f"paths that reach 10 ({cross:.1%} of all)")
    ax[0].set(title="Betting on heads at a 60% coin's odds", xlabel="toss", ylabel="wealth (log scale)", ylim=(1e-12, 1e3))
    ax[0].legend(loc="lower left")
    ax[1].plot(ts, d, color=labs.BLUE, label="distance from uniform, exact")
    ax[1].plot(ts, tail, color=labs.GOLD, label="P(coupling time > t), simulated")
    ax[1].axhline(0.25, color=labs.MUTED, ls=":", lw=1)
    ax[1].axvline(tmix, color=labs.MUTED, ls=":", lw=1)
    ax[1].text(tmix + 4, 0.28, f"t_mix = {tmix}", color=labs.MUTED, fontsize=9)
    ax[1].set(title="Lazy walk on a cycle of 20: coupling bounds mixing", xlabel="steps t", ylabel="total variation")
    ax[1].legend()
    lab.fig = fig
    return lab
