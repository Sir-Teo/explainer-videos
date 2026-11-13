"""Lab 4: solve three equations by iterating a contraction: cos x = x, a differential equation, a system."""

from fractions import Fraction
from math import cos, factorial, sin

import numpy as np
from scipy.integrate import cumulative_simpson, solve_ivp

from videos.coursekit import labs

TITLE = "One contraction, three equations"
GOAL = ("Iterate cos from a random start and check the error bound the contraction principle gives in advance; run "
        "Picard's iteration for y' = t + sin y and check the h^k/k! estimate; watch Newton's residuals square.")
TASKS = [
    "Iterate x -> 2.5 cos x instead. The slope at the fixed point now exceeds 1: describe what the iteration does, and find the two points it settles on.",
    "Run Picard's iteration for y' = 2 sqrt(y), y(0) = 0, from the starts y = 0 and y = t. Which solution does each start find, and which hypothesis failed?",
    "Freeze the Jacobian at the starting point in Newton's method (the inverse function theorem's iteration) and compare the two convergence rates.",
]


def picard(y_start, t, steps, y0=0.5):
    """Picard iterates for y' = t + sin y, y(0) = y0: T(y)(t) = y0 + the integral from 0 to t of s + sin y(s)."""
    ys = [y_start]
    for _ in range(steps):
        ys.append(y0 + cumulative_simpson(t + np.sin(ys[-1]), x=t, initial=0))
    return np.array(ys)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. cos x = x on [0, 1]: cos maps [0, 1] into itself and |cos'| <= sin 1 = c there.
    c, x0 = sin(1.0), float(rng.uniform(0, 1))
    xs = [x0]
    for _ in range(60):
        xs.append(cos(xs[-1]))
    xs = np.array(xs)
    star = 0.7390851332151607
    err = np.abs(xs - star)
    bound = c ** np.arange(61) / (1 - c) * abs(xs[1] - xs[0])
    assert abs(xs[-1] - star) < 1e-9 and abs(cos(star) - star) < 1e-15
    assert np.all(err <= bound + 1e-15), "the a priori bound c^n/(1 - c) |x1 - x0| holds at every step"
    assert np.all(err[1:41] <= c * err[:40] + 1e-15), "each step shrinks the error by at least c"
    lab.row("cos x = x from x0 = %.3f" % x0, f"x_60 = {xs[-1]:.10f}   (0.7390851332)")
    lab.row("  error after 20 steps, and the bound", f"{err[20]:.2e}   <=   {bound[20]:.2e}   (c = sin 1 = {c:.4f})")

    # 2. Completeness cannot be dropped: x/2 + 1/x keeps the rationals in Q and closes in on the hole at sqrt 2.
    p, seq = Fraction(1), []
    for _ in range(5):
        p = p / 2 + 1 / p
        seq.append(p)
    assert seq[:3] == [Fraction(3, 2), Fraction(17, 12), Fraction(577, 408)] and all(q * q != 2 for q in seq)
    lab.row("x/2 + 1/x from 1, in Q", f"{seq[0]}, {seq[1]}, {seq[2]}, ...   (p² - 2 = {float(seq[4] ** 2 - 2):.1e}, never 0)")

    # 3. Picard for y' = t + sin y, y(0) = 0.5 on [0, 1] (L = 1, h = 1), from a random constant start.
    t = np.linspace(0, 1, 2001)
    ys = picard(np.full_like(t, rng.uniform(-1, 2)), t, 14)
    steps = np.abs(np.diff(ys, axis=0)).max(axis=1)
    fact = np.array([steps[0] / factorial(k) for k in range(len(steps))])
    ref = solve_ivp(lambda s, y: s + np.sin(y), (0, 1), [0.5], t_eval=t, rtol=1e-12, atol=1e-13).y[0]
    gap = np.abs(ys - ref).max(axis=1)
    assert np.all(steps <= fact * (1 + 1e-9) + 1e-13), "the k-th change is at most h^k / k! times the first"
    assert gap[12] < 1e-7 and np.all(np.diff(gap[:12]) < 0), "the iterates converge to the solution"
    lab.row("Picard, y' = t + sin y: change at step 8", f"{steps[8]:.2e}   <=   first/8! = {fact[8]:.2e}")
    lab.row("  sup distance to solve_ivp after 12 steps", f"{gap[12]:.1e}")

    # 4. Newton on the circle and the hyperbola: x² + y² = 4, xy = 1.
    f = lambda q: np.array([q[0] ** 2 + q[1] ** 2 - 4, q[0] * q[1] - 1])  # noqa: E731
    jac = lambda q: np.array([[2 * q[0], 2 * q[1]], [q[1], q[0]]])  # noqa: E731
    q = np.array([2.5, 1.0]) + rng.uniform(-0.2, 0.2, 2)
    res = [np.linalg.norm(f(q))]
    for _ in range(6):
        q = q - np.linalg.solve(jac(q), f(q))
        res.append(np.linalg.norm(f(q)))
    res = np.array(res)
    assert np.all(res[1:5] <= 0.5 * res[:4] ** 2 + 1e-14) and res[5] < 1e-12, "the residual squares at each step"
    lab.row("Newton's residuals |F|", "  ".join(f"{r:.1e}" for r in res[:6]))
    lab.note = ("A contraction's fixed point comes with an error bound known before iterating; in C[0, 1] the same "
                "iteration solves a differential equation, and Newton's method contracts harder at every step.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    n = np.arange(41)
    ax[0].semilogy(n, bound[:41], "--", color=labs.GOLD, label="bound: cⁿ/(1 - c) · |x₁ - x₀|")
    ax[0].semilogy(n, err[:41], "o-", ms=3, color=labs.BLUE, label="|xₙ - x*| for cos")
    ax[0].semilogy(np.arange(len(res))[res > 1e-16], res[res > 1e-16], "s-", ms=4, color=labs.GREEN, label="Newton's residual |F|")
    ax[0].set(title="Geometric for a contraction, squaring for Newton", xlabel="step n", ylim=(1e-16, 30))
    ax[0].legend(loc="upper right")
    k = np.arange(len(steps))
    ax[1].semilogy(k, fact, "--", color=labs.GOLD, label="first change / k!")
    ax[1].semilogy(k, steps, "o-", ms=3, color=labs.BLUE, label="sup |y_(k+1) - y_k|")
    ax[1].semilogy(np.arange(len(gap)), gap, "o-", ms=3, color=labs.PINK, label="sup |y_k - solution|")
    ax[1].set(title="Picard's iteration for y' = t + sin y in C[0, 1]", xlabel="iteration k")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
