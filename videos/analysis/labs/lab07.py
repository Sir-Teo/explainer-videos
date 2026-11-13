"""Lab 7: read Fibonacci numbers, root counts and a real integral off contour integrals."""

import numpy as np
from scipy.integrate import quad

from videos.coursekit import labs

TITLE = "What a contour integral knows about the inside"
GOAL = ("Integrate around circles with the trapezoid rule: Cauchy's formula for the coefficients of 1/(1 - z - z^2) "
        "returns the Fibonacci numbers, the integral of p'/p counts the roots of a random polynomial inside each "
        "circle, and two residues give the integral of 1/(1 + x^4) over the real line.")
TASKS = [
    "Move the Fibonacci circle from radius 0.5 to 0.7, past the pole at 0.618. What do the integrals return now, and why?",
    "Count the roots of z^5 + 3z + 1 in |z| < 1 with root_count, then explain the answer by Rouche's theorem with 3z.",
    "Put a circle through a root of p (radius abs(roots[0])) and watch the count stop being an integer as m grows.",
]


def circle(radius, m):
    """m equally spaced points of |z| = radius and the factor dz / (2 pi i) for the trapezoid rule."""
    z = radius * np.exp(2j * np.pi * np.arange(m) / m)
    return z, z / m  # dz = i z dtheta, dtheta = 2 pi / m


def taylor_coefficient(f, n, radius=0.5, m=256):
    """a_n = (1 / 2 pi i) * the integral of f(z) / z^(n+1) over |z| = radius."""
    z, w = circle(radius, m)
    return np.sum(f(z) / z ** (n + 1) * w)


def root_count(coef, radius, m=4096):
    """(1 / 2 pi i) * the integral of p'/p over |z| = radius: the number of roots of p inside (argument principle)."""
    z, w = circle(radius, m)
    return np.sum(np.polyval(np.polyder(coef), z) / np.polyval(coef, z) * w)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Cauchy's formula as a coefficient extractor: the Fibonacci numbers.
    fib = np.array([taylor_coefficient(lambda z: 1 / (1 - z - z * z), n) for n in range(12)])
    exact = [1, 1]
    while len(exact) < 12:
        exact.append(exact[-1] + exact[-2])
    assert np.allclose(fib, exact, atol=1e-8), "the coefficients of 1/(1 - z - z^2) are the Fibonacci numbers"
    lab.row("coefficients of 1/(1 - z - z^2) by Cauchy", " ".join(f"{v.real:.0f}" for v in fib) + "   (Fibonacci)")
    lab.row("largest imaginary part / error", f"{np.abs(fib.imag).max():.1e} / {np.abs(fib - exact).max():.1e}")

    # 2. The argument principle on a random polynomial of degree 7: circles between consecutive root moduli.
    while True:
        coef = rng.normal(size=8) + 1j * rng.normal(size=8)
        roots = np.roots(coef)
        mod = np.sort(np.abs(roots))
        if np.diff(mod).min() > 0.03:  # keep the circles a clear distance from every root
            break
    radii = np.concatenate([[mod[0] / 2], (mod[:-1] + mod[1:]) / 2, [mod[-1] * 1.3]])
    counts = np.array([root_count(coef, r) for r in radii])
    truth = np.array([(np.abs(roots) < r).sum() for r in radii])
    assert np.abs(counts - truth).max() < 1e-6, "the integral of p'/p counts the roots inside"
    lab.row("roots of a random degree-7 p inside 8 circles", " ".join(f"{round(c.real, 3) + 0.0:.3f}" for c in counts))
    lab.row("the same counts from numpy.roots", " ".join(str(t) for t in truth))

    # 3. Residues: the integral of 1/(1 + x^4) over the line is 2 pi i times two residues 1/(4 z^3).
    poles = np.exp(1j * np.pi * np.array([1, 3]) / 4)
    by_residues = 2j * np.pi * np.sum(1 / (4 * poles**3))
    by_quad = 2 * quad(lambda x: 1 / (1 + x**4), 0, np.inf)[0]
    assert abs(by_residues - np.pi / np.sqrt(2)) < 1e-12 and abs(by_quad - by_residues.real) < 1e-8
    lab.row("integral of 1/(1 + x^4): residues", f"{by_residues.real:.10f}   (pi / sqrt 2 = {np.pi / np.sqrt(2):.10f})")
    lab.row("integral of 1/(1 + x^4): quadrature", f"{by_quad:.10f}")
    # the semicircle of radius R encloses the same two poles for every R > 1: the closed integral does not move
    closed = []
    for R in (2.0, 5.0, 20.0):
        t = np.linspace(0, np.pi, 20001)
        arc = R * np.exp(1j * t)
        f_arc = 1 / (1 + arc**4) * 1j * arc
        arc_part = np.sum((f_arc[1:] + f_arc[:-1]) / 2) * (t[1] - t[0])
        closed.append((R, quad(lambda x: 1 / (1 + x**4), -R, R)[0] + arc_part, abs(arc_part)))
    assert all(abs(c - by_residues) < 1e-6 for _, c, _ in closed) and closed[-1][2] < closed[0][2] / 100
    lab.row("size of the arc's share at R = 2, 5, 20", "  ".join(f"{a:.5f}" for _, _, a in closed) + "   (closed total fixed)")
    lab.note = ("A contour integral sees only what the contour winds around: Taylor coefficients, the number of "
                "zeros, the sum of residues. The trapezoid rule on a circle is exact to rounding here because the "
                "integrands are holomorphic in an annulus around the circle.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    t = np.linspace(0, 2 * np.pi, 400)
    for k, (r, c) in enumerate(zip(radii, counts)):
        ax[0].plot(r * np.cos(t), r * np.sin(t), color=labs.BLUE, lw=0.9, alpha=0.8)
        ax[0].text(r * np.cos(0.4 + 0.8 * k), r * np.sin(0.4 + 0.8 * k), f"{abs(round(c.real))}", color=labs.GOLD, fontsize=9,
                   ha="center", va="center", bbox=dict(facecolor=labs.BG, edgecolor="none", pad=1))
    ax[0].plot(roots.real, roots.imag, "o", color=labs.RED, ms=5, label="roots of p (numpy.roots)")
    ax[0].plot([], [], color=labs.BLUE, label="contours, labelled by the integral of p'/p")
    lim = radii[-1] * 1.08
    ax[0].set(title="The argument principle counts roots", xlabel="Re z", ylabel="Im z", xlim=(-lim, lim), ylim=(-lim, lim))
    ax[0].set_aspect("equal")
    ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=1)
    ms = np.array([8, 12, 16, 24, 32, 48, 64, 96, 128])
    for n, color in ((5, labs.GOLD), (11, labs.GREEN)):
        errs = [abs(taylor_coefficient(lambda z: 1 / (1 - z - z * z), n, m=int(m)) - exact[n]) + 1e-17 for m in ms]
        ax[1].semilogy(ms, errs, "o-", color=color, label=f"error of coefficient {n} (Fibonacci {exact[n]})")
    ax[1].set(title="Trapezoid rule on |z| = 1/2: geometric convergence", xlabel="points on the circle", ylabel="absolute error")
    ax[1].legend()
    lab.fig = fig
    return lab
