"""Lab 44: run A/A tests that are checked every morning, repair them with a sequential test, and cut their noise with CUPED."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.people import experiments as ex
from explainer.cs.people import hci

TITLE = "Peeking, a sequential test, and CUPED"
GOAL = ("Simulate A/A tests with the series' experiment tools: z-test them every day and stop at the first p < 0.05, "
        "look only once on day 30, or use the mixture sequential test; then check CUPED's variance against 1 - rho^2, "
        "the sample-size formula against simulated power, and Fitts's law on a simulated hand.")
TASKS = [
    "Run ex.peeking with days=90. Does the false-positive rate level off? Compare its growth with the law of the iterated logarithm's sqrt(2 log log n).",
    "Call ex.msprt with lift=0.10 and tau2=(0.05 * 0.10) ** 2, then with the default tau2. Which mixture stops earlier on a real 10% lift, and what does each do to an A/A test?",
    "In ex.cuped, use theta = 1 instead of the regression slope (edit a copy). At which correlations does the adjusted estimator become noisier than the plain one?",
]


def run(seed=0):
    lab = labs.Lab()

    # 1. an A/A test, 1,000 users a day per arm, 5% converting: a look every morning against one look
    peek = ex.peeking(days=30, per_day=1000, p=0.05, trials=3000, seed=seed)
    by_day = np.array(peek["fpr_peeking"])
    assert abs(by_day[0] - 0.05) < 0.02 and abs(peek["fpr_final_only"] - 0.05) < 0.02, "one look keeps its 5%"
    assert by_day[-1] > 0.20 and np.all(np.diff(by_day) >= 0), "thirty looks do not"
    lab.row("A/A test, one look on day 30", f"{peek['fpr_final_only']:.1%} declare a winner   (promised 5%)")
    lab.row("A/A test, stopped at the first p < 0.05", f"{by_day[0]:.1%} on day 1, {by_day[6]:.1%} by day 7, "
                                                         f"{by_day[-1]:.1%} by day 30")

    # 2. the mixture sequential test: valid at every look (Ville's inequality), and it still finds a real lift
    null, real = ex.msprt(lift=0.0, trials=3000, seed=seed), ex.msprt(lift=0.10, trials=3000, seed=seed)
    assert null["rejected"] <= 0.05, "always valid: at most alpha, however often one looks"
    assert real["rejected"] > 0.25, "and it has power against a real 10% lift"
    lab.row("mixture sequential test, looked at daily", f"{null['rejected']:.1%} false positives; "
                                                        f"finds a real 10% lift {real['rejected']:.0%} of the time")

    # 3. CUPED: the variance falls by the factor 1 - rho^2
    rhos = [0.0, 0.3, 0.5, 0.7, 0.9]
    ratios = [ex.cuped(n=1000, rho=r, trials=800, seed=seed + k)["ratio"] for k, r in enumerate(rhos)]
    for r, got in zip(rhos, ratios):
        assert abs(got - (1 - r * r)) < 0.25 * (1 - r * r) + 0.02, "Var(Y - theta X) = Var(Y)(1 - rho^2)"
    lab.row("CUPED variance ratio at rho = 0.5, 0.7, 0.9", "  ".join(f"{g:.2f}" for g in ratios[2:])
            + "   (1 - rho^2: 0.75  0.51  0.19)")

    # 4. the sample size that buys 80% power, and the rule of 16
    size = ex.sample_size(0.05, 0.10)
    power = ex.power_sim(p=0.05, lift=0.10, trials=3000, seed=seed)["power"]
    assert abs(power - 0.80) < 0.05 and abs(size["rule_16"] / size["n_per_arm"] - 16 / 15.7) < 0.01
    lab.row("10% lift on a 5% rate", f"{size['n_per_arm']:,.0f} users per arm (rule of 16: {size['rule_16']:,.0f}); "
                                     f"simulated power {power:.1%}")

    # 5. Fitts's law on the simulated hand
    fitts = hci.fitts_experiment(seed=seed, trials=200)
    assert fitts["r2"] > 0.97 and fitts["b"] > 0
    lab.row("Fitts's law, 20 simulated targets", f"MT = {fitts['a']:.2f} + {fitts['b']:.3f} log2(D/W + 1) s, R^2 = {fitts['r2']:.3f}")
    lab.note = ("A z-test promises 5% false positives for one look; stopping at the first significant morning turns "
                "that into more than 20% in a month. A test built as a martingale keeps its promise at every look, "
                "and a pre-period covariate buys precision without more users.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    days = np.arange(1, 31)
    ax[0].plot(days, 100 * by_day, "o-", ms=4, color=labs.RED, label="z-test every morning, stop at p < 0.05")
    ax[0].axhline(100 * peek["fpr_final_only"], color=labs.BLUE, label="z-test once, on day 30")
    ax[0].axhline(100 * null["rejected"], color=labs.GREEN, label="mixture sequential test, every morning")
    ax[0].axhline(5, color=labs.MUTED, ls="--", label="promised: 5%")
    ax[0].set(title="A/A tests that declare a winner", xlabel="day", ylabel="false positives so far (%)")
    ax[0].legend(loc="center right")
    grid = np.linspace(0, 0.95, 50)
    ax[1].plot(grid, 1 - grid ** 2, color=labs.GOLD, label="theory: 1 - rho²")
    ax[1].plot(rhos, ratios, "o", color=labs.BLUE, label="800 simulated experiments each")
    ax[1].set(title="CUPED: variance left after adjusting", xlabel="correlation rho with the pre-period metric",
              ylabel="Var(adjusted) / Var(plain)", ylim=(0, 1.15))
    ax[1].legend()
    lab.fig = fig
    return lab
