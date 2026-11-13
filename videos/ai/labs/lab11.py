"""Lab 11: race gradient descent, the heavy ball and Nesterov down a quadratic valley, against their derived rates."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Three ways downhill, against their derived rates"
GOAL = ("Run gradient descent, the tuned heavy ball and Nesterov's method on a 50-dimensional quadratic with condition "
        "number 1,000, with gradients from the series' autodiff, and compare each one's measured contraction per step "
        "with the rate the part derives. Then count the steps to a millionth of the starting gap as the condition "
        "number grows.")
TASKS = [
    "Run gradient descent with step=1.9, 2.0 and 2.05 (in units of 1/L). Which direction grows, and by what factor a step?",
    "Give the heavy ball Nesterov's momentum (drop the square in `beta`) and compare its step count at kappa = 1,000.",
    "Replace the quadratic by sum(h * x**4): the loss is still convex. Do the three rates still hold?",
]


def make_loss(h):
    """f(x) = 1/2 sum_i h_i x_i^2 as an autodiff graph; returns a function x -> (f, gradient)."""
    def f_and_grad(x):
        t = Tensor(x, requires_grad=True)
        loss = ((t * t) * h).sum() * 0.5
        loss.backward()
        return float(loss.data), t.grad
    return f_and_grad


def run_method(name, h, x0, steps, step=1.0):
    """The objective gaps f(x_k) - f* (f* = 0) along a run of one method with its textbook tuning; ``step`` is
    gradient descent's step in units of 1/L."""
    L, mu = h.max(), h.min()
    kappa = L / mu
    f = make_loss(h)
    x, prev, gaps = x0.copy(), x0.copy(), []
    for _ in range(steps):
        if name == "gd":  # x - (1/L) grad
            val, g = f(x)
            new = x - step * g / L
        elif name == "heavy":  # Polyak (1964): tuned step and momentum
            beta = ((np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1)) ** 2
            eta = 4 / (np.sqrt(L) + np.sqrt(mu)) ** 2
            val, g = f(x)
            new = x - eta * g + beta * (x - prev)
        else:  # Nesterov (1983): the gradient is taken at the look-ahead point
            beta = (np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1)
            val = f(x)[0]
            y = x + beta * (x - prev)
            new = y - f(y)[1] / L
        gaps.append(val)
        x, prev = new, x
    return np.array(gaps)


def late_ratio(gaps):
    """The geometric-mean contraction of sqrt(gap) per step, over the stretch where the gap falls from 1e-6 to 1e-12
    of its start (late enough for the slowest direction to dominate, early enough to stay above rounding)."""
    rel = gaps / gaps[0]
    a = int(np.argmax(rel < 1e-6))
    b = int(np.argmax(rel < 1e-12)) or len(rel) - 1
    return (rel[b] / rel[a]) ** (0.5 / (b - a))


def steps_to(gaps, tol=1e-6):
    return int(np.argmax(gaps / gaps[0] < tol))


def run(seed=0):
    rng = np.random.default_rng(seed)
    d = 50
    x0 = rng.standard_normal(d)
    lab = labs.Lab()

    kappa = 1000.0
    h = np.geomspace(1.0, 1 / kappa, d)  # curvatures from L = 1 down to mu = 1/kappa
    budget = {"gd": 16000, "heavy": 700, "nesterov": 700}
    derived = {"gd": 1 - 1 / kappa, "heavy": (np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1), "nesterov": 1 - 1 / np.sqrt(kappa)}
    label = {"gd": "gradient descent", "heavy": "heavy ball", "nesterov": "Nesterov"}
    runs = {m: run_method(m, h, x0, budget[m]) for m in budget}
    measured = {m: late_ratio(runs[m]) for m in budget}
    count = {m: steps_to(runs[m]) for m in budget}
    for m in budget:
        lab.row(f"{label[m]}: contraction per step", f"{measured[m]:.4f}   (derived {derived[m]:.4f})")
    lab.row("steps to 1e-6 of the gap, kappa = 1,000",
            "   ".join(f"{label[m]} {count[m]:,}" for m in budget))

    kappas = np.array([10.0, 30.0, 100.0, 300.0, 1000.0])
    sweep = {m: [] for m in budget}
    for k in kappas:
        hk = np.geomspace(1.0, 1 / k, d)
        for m in budget:
            sweep[m].append(steps_to(run_method(m, hk, x0, int(16 * k) if m == "gd" else int(30 * np.sqrt(k)) + 60)))
    slope = {m: np.polyfit(np.log(kappas), np.log(sweep[m]), 1)[0] for m in budget}
    lab.row("slope of steps against kappa (log axes)",
            "   ".join(f"{label[m]} {slope[m]:.2f}" for m in budget) + "   (theory 1, 1/2, 1/2)")

    diverge = run_method("gd", h, x0, 400, step=2.05)  # eta * L = 2.05 > 2: the steepest direction flips and grows
    lab.row("gradient descent with step 2.05 / L", f"gap grows {diverge[-1] / diverge[0]:.1e} times in 400 steps")
    lab.note = ("Plain gradient descent pays for the condition number, momentum for its square root: each measured "
                "contraction sits on the root of its recurrence, and a step past 2 / L does not converge at all.")

    assert abs(measured["gd"] - derived["gd"]) < 5e-4, "gradient descent contracts by 1 - 1/kappa"
    assert abs(measured["heavy"] - derived["heavy"]) < 0.012, "the heavy ball's roots have modulus sqrt(beta)"
    assert abs(measured["nesterov"] - derived["nesterov"]) < 0.012, "Nesterov's double root is 1 - 1/sqrt(kappa)"
    assert count["heavy"] < count["gd"] / 8 and count["nesterov"] < count["gd"] / 8, "momentum is far faster"
    assert 0.8 < slope["gd"] < 1.1 and 0.4 < slope["heavy"] < 0.65 and 0.4 < slope["nesterov"] < 0.65, slope
    assert diverge[-1] > 1e6 * diverge[0], "a step over 2/L diverges"

    fig, ax = labs.figure(2, size=(11, 4.2))
    color = {"gd": labs.BLUE, "heavy": labs.GOLD, "nesterov": labs.GREEN}
    for m in budget:
        g = runs[m] / runs[m][0]
        keep = g > 1e-14
        ax[0].semilogy(np.arange(len(g))[keep], g[keep], color=color[m], label=f"{label[m]}: {measured[m]:.4f} a step")
    ax[0].axhline(1e-6, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="The gap at condition number 1,000", xlabel="step", ylabel="(f - f*) / starting gap", xscale="log")
    ax[0].legend(loc="lower left")
    for m in budget:
        ax[1].loglog(kappas, sweep[m], "o-", color=color[m], label=f"{label[m]}: slope {slope[m]:.2f}")
    ax[1].set(title="Steps to a millionth of the gap", xlabel="condition number kappa", ylabel="steps")
    ax[1].legend()
    lab.fig = fig
    return lab
