"""Lab 43: measure the central limit theorem's rate exactly, and hold it against Berry-Esseen and Stein."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import limits

TITLE = "How fast is the central limit theorem?"
GOAL = ("Compute the exact Kolmogorov distance between a standardized sum and the normal law for four kinds of "
        "summand, n = 1 to 1,024, fit its slope on log-log axes, and compare it with the Berry-Esseen bound "
        "0.4748 rho / sqrt(n); then check Stein's identity on simulated sums.")
TASKS = [
    "Change the unfair coin's p from 0.1 to 0.01. How does the share of the Berry-Esseen bound it uses change, and why?",
    "Replace the Kolmogorov distance by limits.wasserstein1 for the fair coin and compare with Stein's bound rho / sqrt(n).",
    "In the Stein check use f(x) = x**3 (f' = 3x**2). Which moment of the sum does the residual measure now?",
]


def distance(kind, n, p=0.5):
    """The Kolmogorov distance of a standardized sum of n summands from N(0, 1): exact for the lattice laws."""
    if kind == "bernoulli":
        a = limits.bernoulli_sum_atoms(n, p)
        return limits.kolmogorov_lattice(a["atoms"], a["probs"], stats.norm.cdf)["d"]
    if kind == "poisson":
        a = limits.poisson_sum_atoms(n)
        return limits.kolmogorov_lattice(a["atoms"], a["probs"], stats.norm.cdf)["d"]
    z = np.linspace(-6, 6, 24001)  # a gamma law is continuous: a fine grid
    return limits.kolmogorov(limits.exponential_sum_cdf(n), stats.norm.cdf, z)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    ns = 2 ** np.arange(0, 11)
    kinds = [("fair coin", "bernoulli", 0.5, labs.BLUE), ("coin, p = 0.1", "bernoulli", 0.1, labs.GREEN),
             ("Poisson(1)", "poisson", 0.5, labs.PURPLE), ("exponential", "exponential", 0.5, labs.GOLD)]
    out = {}
    for name, kind, p, color in kinds:
        d = np.array([distance(kind, int(n), p) for n in ns])
        rho = limits.third_abs_moment(kind, p) if kind == "bernoulli" else limits.third_abs_moment(kind)
        bound = np.array([limits.berry_esseen(rho, int(n)) for n in ns])
        slope = np.polyfit(np.log(ns[4:]), np.log(d[4:]), 1)[0]
        out[name] = dict(d=d, bound=bound, slope=slope, ratio=d[-1] / bound[-1], color=color)
        lab.row(f"{name}: slope of log distance on log n", f"{slope:.3f}   (theory -0.5)")
        lab.row(f"{name}: distance / Berry-Esseen bound at n = 1024", f"{d[-1]:.5f} / {bound[-1]:.5f} = {d[-1] / bound[-1]:.0%}")
        assert np.all(d <= bound + 1e-12), "the Berry-Esseen bound holds at every n"
        assert abs(slope + 0.5) < 0.02, "the rate is 1 / sqrt(n)"
    fair = out["fair coin"]
    # a fair coin's largest gap is half the central atom, about 1 / sqrt(2 pi n): 0.399 / 0.4748 = 84% of the bound
    assert abs(fair["ratio"] - 1 / (np.sqrt(2 * np.pi) * limits.SHEVTSOVA)) < 0.01, "the constant is nearly sharp"
    assert out["exponential"]["ratio"] < 0.25, "a smooth summand is far inside the bound"

    # Stein's identity: E[f'(W) - W f(W)] = 0 exactly when W is N(0, 1).  With f(x) = x^2 the residual is -E W^3,
    # which for a standardized sum of n exponentials is -2 / sqrt(n).
    reps, n = 400_000, 16
    w = (rng.gamma(n, size=reps) - n) / np.sqrt(n)
    z = rng.standard_normal(reps)
    f, fp = (lambda x: x ** 2), (lambda x: 2 * x)
    r_sum, r_norm = limits.stein_residual(f, fp, w), limits.stein_residual(f, fp, z)
    lab.row("Stein residual, normal sample", f"{r_norm:+.3f}   (theory 0)")
    lab.row("Stein residual, 16 exponentials", f"{r_sum:+.3f}   (theory -2/sqrt(16) = -0.500)")
    assert abs(r_norm) < 0.03 and abs(r_sum + 0.5) < 0.06, "Stein's identity separates the two laws"
    lab.note = ("Every exact distance falls like 1 / sqrt(n) and stays under 0.4748 rho / sqrt(n); the fair coin uses "
                "84% of the bound, the exponential about an eighth of it.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    for name, r in out.items():
        ax[0].loglog(ns, r["d"], "o-", ms=3, color=r["color"], label=f"{name} (slope {r['slope']:.3f})")
        ax[0].loglog(ns, r["bound"], ls="--", lw=1, color=r["color"], alpha=0.7)
    ax[0].set(title="Exact Kolmogorov distance (dashed: Berry-Esseen bound)", xlabel="n", ylabel="sup |F_n - Phi|")
    ax[0].legend(loc="lower left")
    a = limits.bernoulli_sum_atoms(10)
    F = limits.lattice_cdf(a["atoms"], a["probs"])
    x = np.linspace(-3.5, 3.5, 2001)
    k = limits.kolmogorov_lattice(a["atoms"], a["probs"], stats.norm.cdf)
    ax[1].step(x, F(x), where="post", color=labs.BLUE, label="standardized Binomial(10, 1/2)")
    ax[1].plot(x, stats.norm.cdf(x), color=labs.GOLD, label="normal CDF")
    ax[1].plot([k["x"], k["x"]], [k["F"], k["G"]], color=labs.RED, lw=3, label=f"Kolmogorov gap {k['d']:.3f}")
    ax[1].set(title="Ten coin tosses against the normal law", xlabel="z", ylabel="CDF")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
