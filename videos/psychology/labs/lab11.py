"""Lab 11: Weber's fraction built from noise, the three classical methods, a fitted psychometric function with a
bootstrap interval and a goodness-of-fit check, staircases and QUEST, Stevens's power law with its range effect, the
square-root regime of photon noise, and the triangle test's power."""

import math

import numpy as np
from scipy import optimize

from videos.coursekit import labs
from explainer.psychology import battery
from explainer.psychology.psyche import psychophysics as P

TITLE = "Thresholds and scales: Weber, Fechner, the psychometric function and Stevens"
GOAL = ("Build an observer whose noise has a floor and a part that grows with the stimulus, and find Weber's law in "
        "its thresholds and its failure near the floor; count Fechner's steps; run the method of limits with three "
        "response criteria, the method of adjustment and the method of constant stimuli; fit the psychometric "
        "function by maximum likelihood with a parametric bootstrap, with and without a lapse rate; check where "
        "two-down and three-down staircases settle and how step size biases them; run QUEST; and recover Stevens's "
        "exponents from simulated magnitude estimates, then watch the stimulus range move them.")
TASKS = [
    "Fit the Battery's threshold task for 40, 80, 160 and 320 trials with a fitted and a fixed lapse rate, 200 times "
    "each. Plot the bias and spread of the 75% threshold against trials. When does fitting the lapse rate help?",
    "Give the Observer poisson=1 and k=0.02, and plot the JND from 1e-4 to 1e7 on log-log axes. Where do the slopes "
    "change from 0 to 1/2 and from 1/2 to 1? Derive both crossing points from sigma0, poisson and k.",
    "How many tasters does a triangle test need to find, 80% of the time, a difference that 20% of people can taste? "
    "And a duo-trio test, where the guess rate is 1/2? Which test is more efficient, and why?",
]


def run(seed=0):
    out = labs.Lab()
    rng = lambda k: np.random.default_rng(seed + k)  # noqa: E731
    clean = P.Observer(k=0.08, sigma0=0.5, lapse=0.0)
    obs = P.Observer(k=0.08, sigma0=0.5, lapse=0.02)

    # 1. Weber's law, and where it fails
    w = P.weber_fractions(clean, [1.0, 10.0, 100.0, 1000.0, 10000.0])
    out.row("Weber's fraction at intensities 1, 10, 100, 1,000, 10,000", ", ".join(f"{v:.3f}" for v in w))
    out.row("Fechner: JND steps from 1 to 1,000 at a fraction of 0.08; and from 1 to 10", f"{P.fechner(1000.0, 1.0, 0.08):.1f}; "
            f"{P.fechner(10.0, 1.0, 0.08):.1f}")
    assert abs(w[-1] - w[-2]) < 1e-3 and w[0] > 4 * w[-1]

    # 2. the classical methods
    for c in (0.5, 1.0, 1.5):
        t = np.median([P.method_of_limits(clean, 100.0, 40.0, 2.5, 10, rng(10 + j), criterion=c)["threshold"] for j in range(100)])
        out.row(f"method of limits, criterion {c}: median threshold over 100 runs", f"{t:.1f}")
    adj = P.method_of_adjustment(clean, 100.0, 200, rng(20))
    out.row("method of adjustment, 200 settings: point of subjective equality; JND from the spread; true JND",
            f"{adj['pse']:.1f}; {adj['jnd_from_sd']:.2f}; {float(P.jnd(clean, 100.0)):.2f}")

    # 3. constant stimuli and the fit
    t = battery.run("threshold", obs, 320, seed=seed + 30)
    deltas = np.array(battery.THRESHOLD_DELTAS)
    k = np.array([int(t.correct[t.extra["delta"] == d].sum()) for d in deltas])
    n = np.array([int((t.extra["delta"] == d).sum()) for d in deltas])
    f = P.fit(deltas, k, n, form="gauss")
    b = P.bootstrap(deltas, k, n, f, n_boot=300, rng=rng(31))
    true75 = optimize.brentq(lambda d: float(obs.p_correct(100.0, d)) - 0.75, 0.01, 60)
    th = P.threshold_at(f, 0.75)
    out.row("Battery task 2, 320 trials: right answers at each increment", " ".join(str(v) for v in k))
    out.row("fitted 75% threshold [bootstrap 95%]; the truth", f"{th:.1f} [{b['threshold_ci'][0]:.1f}, {b['threshold_ci'][1]:.1f}]; {true75:.1f}")
    k2 = k.copy()
    k2[-1] = n[-1] - 3
    fixed = P.fit(deltas, k2, n, form="gauss", lam=0.0)
    free = P.fit(deltas, k2, n, form="gauss")
    out.row("one more error at the easiest level: threshold with lapse fixed at 0; with lapse fitted",
            f"{P.threshold_at(fixed, 0.75):.1f}; {P.threshold_at(free, 0.75):.1f}")

    # 4. adaptive methods
    for kd in (2, 3):
        est = [P.staircase(obs, 100.0, 30.0, factor=1.12, k_down=kd, n_trials=200, rng=rng(100 * kd + j),
                           n_reversals_used=12)["estimate"] for j in range(150)]
        aim = optimize.brentq(lambda d: float(obs.p_correct(100.0, d)) - P.updown_target(kd), 0.01, 60)
        out.row(f"{kd}-down 1-up staircase: median estimate; the {100 * P.updown_target(kd):.1f}% level", f"{np.median(est):.1f}; {aim:.1f}")
    coarse = np.median([P.staircase(obs, 100.0, 30.0, factor=1.5, rng=rng(500 + j))["estimate"] for j in range(150)])
    out.row("2-down staircase with steps of 1.5 instead of 1.12: median estimate", f"{coarse:.1f}")
    q = [P.quest(obs, 100.0, 40, rng=rng(600 + j))["estimate"] for j in range(60)]
    aim82 = optimize.brentq(lambda d: float(obs.p_correct(100.0, d)) - 0.82, 0.01, 60)
    out.row("QUEST, 40 trials: median estimate; the 82% level", f"{np.median(q):.1f}; {aim82:.1f}")
    assert abs(np.median(q) / aim82 - 1) < 0.15

    # 5. Stevens
    for a in (0.33, 1.45, 3.5):
        me = P.magnitude_estimation(np.logspace(0, 1, 7), a, 20, rng(int(700 + 10 * a)))
        out.row(f"magnitude estimation with exponent {a}: fitted exponent", f"{P.fit_power(me['intensity'], me['geometric_mean'])['exponent']:.2f}")
    out.row("cross-modality match of loudness (0.67) to brightness (0.33): predicted exponent", f"{P.cross_modality(0.33, 0.67):.2f}")
    out.row("light needed to double brightness at exponent 0.33", f"{2 ** (1 / 0.33):.1f} times")
    out.note = ("Noise with a floor and a proportional part gives a constant Weber fraction over the middle of the "
                "range and a rising one near the floor. A yes-no method's threshold moves with the observer's "
                "criterion, the forced choice's does not. Three hundred and twenty trials pin a threshold to about "
                "thirty percent either way, and a fit without a lapse rate lets one slip move it by a fifth or more. A "
                "k-down staircase settles where p^k = 1/2 if its steps are small, and below that if they are large. "
                "QUEST reaches its target in tens of trials. Simulated magnitude estimates give back their exponents. "
                "The slope of a threshold against its background says which noise is in charge, and a fit that "
                "passes its goodness-of-fit test can still hide drift. A triangle test of 30 tasters finds a "
                "difference that a tenth of people can taste less than one time in five.")

    # 6. The slope tells you the noise: a floor, photon noise and Weber noise
    eye = P.Observer(k=0.02, sigma0=0.05, lapse=0.0, poisson=1.0)
    lv = np.array([1e-4, 1e-3, 1.0, 10.0, 1e5, 1e6])
    jj = P.jnd(eye, lv)
    sl = [math.log10(jj[i + 1] / jj[i]) / math.log10(lv[i + 1] / lv[i]) for i in (0, 2, 4)]
    out.row("Threshold-against-background slopes: dark light, photon noise, Weber", ", ".join(f"{v:.2f}" for v in sl))

    # 7. Does the curve fit? The bootstrap's deviance
    bt = P.bootstrap(deltas, k, n, f, n_boot=200, rng=rng(80))
    out.row("Goodness of fit: deviance of the data; share of 200 repeats that fit worse", f"{f['deviance']:.2f}; "
            f"{bt['p_fit']:.2f}")

    # 8. The triangle test: guess rate 1/3
    out.row("Triangle test with 30 tasters: right answers needed at 5%; power if 30% (10%) can tell",
            f"{P.triangle_critical(30)}; {P.triangle_power(30, 0.3):.2f} ({P.triangle_power(30, 0.1):.2f})")

    fig, ax = labs.figure(2, size=(11, 4.2))
    s = np.logspace(-1, 4, 60)
    ax[0].loglog(s, P.weber_fractions(clean, s), color=labs.BLUE, lw=1.8, label="near_miss 0")
    ax[0].loglog(s, P.weber_fractions(P.Observer(k=0.08, sigma0=0.5, lapse=0.0, near_miss=0.05), s), color=labs.PINK, lw=1.4,
                 label="near_miss 0.05")
    ax[0].set(title="Weber's fraction against intensity", xlabel="standard", ylabel="JND / standard")
    ax[0].legend(fontsize=8)
    x = np.linspace(0.5, 25, 200)
    ax[1].plot(deltas, k / n, "o", color=labs.ORANGE if hasattr(labs, "ORANGE") else labs.PINK, label="data")
    ax[1].plot(x, P.psychometric(x, f["alpha"], f["beta"], 0.5, f["lam"], "gauss"), color=labs.GREEN, lw=1.8, label="ML fit")
    ax[1].axvline(th, color=labs.GREY, ls="--", lw=1)
    ax[1].set(title="Battery task 2: 320 trials, fitted", xlabel="increment over 100", ylabel="share right")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out
