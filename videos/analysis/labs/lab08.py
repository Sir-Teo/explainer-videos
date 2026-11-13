"""Lab 8: compute the norms of the partial-sum functionals on C(T) and watch uniform boundedness fail."""

import numpy as np

from videos.coursekit import labs

TITLE = "Lebesgue constants: the norms that Banach and Steinhaus need"
GOAL = ("Compute the norm of f -> s_n(f)(0) on the continuous functions, the integral of |D_n|, three ways (quadrature, "
        "Fejer's sum, the asymptote (4/pi^2) log n + 1.27), build a continuous function that nearly attains it, and "
        "check that no function bounded by 1 beats it.")
TASKS = [
    "Replace Dirichlet's kernel by Fejer's (the average of D_0 ... D_n). Its norm is 1 for every n: what does that say about Fejer means?",
    "Widen the ramps of the near-extremal function (width = 0.8) and see how much of the norm it still reaches.",
    "Sum f = sum_k 2^-k f_{n_k} with n_k = 2^(k^3), truncated at k = 3, and print s_n(f)(0) at n = n_k: this is the classical explicit construction.",
]

GX, GW = np.polynomial.legendre.leggauss(12)


def dirichlet(t, n):
    """D_n(t) = sin((n + 1/2) t) / sin(t / 2) = the sum of e^(ikt) for |k| <= n."""
    s = np.sin(t / 2)
    safe = np.where(np.abs(s) < 1e-12, 1.0, s)
    return np.where(np.abs(s) < 1e-12, 2 * n + 1.0, np.sin((n + 0.5) * t) / safe)


def integrate_lobes(g, n):
    """(1 / 2 pi) * the integral of g over [-pi, pi] for even g, by Gauss-Legendre on each lobe of D_n in [0, pi]."""
    edges = np.minimum(np.arange(n + 2) * 2 * np.pi / (2 * n + 1), np.pi)  # the zeros of D_n, then pi
    a, b = edges[:-1, None], edges[1:, None]
    t = (a + b) / 2 + (b - a) / 2 * GX
    return float(np.sum((b - a) / 2 * GW * g(t)) / np.pi)


def lebesgue_quadrature(n):
    return integrate_lobes(lambda t: np.abs(dirichlet(t, n)), n)


def lebesgue_fejer(n):
    """Fejer's closed sum for the Lebesgue constant."""
    k = np.arange(1, n + 1)
    return 1 / (2 * n + 1) + 2 / np.pi * np.sum(np.tan(np.pi * k / (2 * n + 1)) / k)


def near_extremal(t, n, width=0.2):
    """A continuous function bounded by 1 that follows the sign of D_n, with linear ramps across its zeros."""
    f = np.clip(np.sin((n + 0.5) * np.abs(t)) / width, -1, 1)
    return np.where(np.abs(t) < np.pi / (2 * n + 1), 1.0, f)  # 1 across the central peak, where D_n does not change sign


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    ns = 2 ** np.arange(1, 13)
    quad = np.array([lebesgue_quadrature(n) for n in ns])
    fejer = np.array([lebesgue_fejer(n) for n in ns])
    asym = 4 / np.pi**2 * np.log(ns) + 1.27
    assert np.abs(quad - fejer).max() < 1e-8, "quadrature agrees with Fejer's sum"
    assert np.all(np.diff(fejer) > 0.2), "the norms grow with every doubling, toward (4/pi^2) log 2 = 0.281 each: unbounded"
    assert np.abs(fejer - asym)[ns >= 64].max() < 0.01, "the norms follow (4/pi^2) log n + 1.27"

    # the continuous near-extremal function: s_n(f_n)(0) = (1/2pi) int f_n D_n, just below the norm
    reach = np.array([integrate_lobes(lambda t, n=n: near_extremal(t, n) * dirichlet(t, n), n) for n in ns])
    assert np.all(reach < fejer) and np.all(reach > 0.97 * fejer), "a continuous function comes within 3% of the norm"

    # no function bounded by 1 beats the norm: 300 random continuous (piecewise linear) functions at n = 64
    n0 = 64
    best = 0.0
    knots = np.linspace(0, np.pi, 400)
    for _ in range(300):
        vals = rng.uniform(-1, 1, knots.size)
        best = max(best, abs(integrate_lobes(lambda t: np.interp(t, knots, vals) * dirichlet(t, n0), n0)))
    L0 = lebesgue_fejer(n0)
    assert best < L0, "|s_n(f)(0)| <= ||D_n||_1 sup|f|"

    for n, q, f, a, r in zip(ns[[2, 5, 8, 11]], quad[[2, 5, 8, 11]], fejer[[2, 5, 8, 11]], asym[[2, 5, 8, 11]], reach[[2, 5, 8, 11]]):
        lab.row(f"n = {n}: norm of f -> s_n(f)(0)", f"{q:.5f} (quadrature)  {f:.5f} (Fejer)  {a:.3f} (asymptote)")
        lab.row(f"n = {n}: reached by the continuous f_n", f"{r:.5f}   ({r / f:.1%} of the norm)")
    lab.row(f"n = {n0}: best of 300 random f with |f| <= 1", f"{best:.4f}   (norm {L0:.4f})")
    lab.note = ("The functionals f -> s_n(f)(0) are each bounded, but their norms grow like (4/pi^2) log n, so by "
                "Banach-Steinhaus they cannot be bounded at every continuous f: some f (a dense G-delta of them) has "
                "partial sums at 0 that are unbounded. Random functions come nowhere near the norm; the extremal "
                "ones are special, which is why the theorem is needed to find them.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    n = 8
    t = np.linspace(-np.pi, np.pi, 2001)
    ax[0].plot(t, dirichlet(t, n) / (2 * n + 1), color=labs.BLUE, label="Dirichlet kernel D_8 / 17")
    ax[0].plot(t, near_extremal(t, n), color=labs.GOLD, lw=1.2, label="continuous f_8 following its sign")
    ax[0].fill_between(t, 0, np.minimum(dirichlet(t, n), 0) / (2 * n + 1), color=labs.RED, alpha=0.5, label="negative lobes")
    ax[0].set(title="A function bounded by 1 lines up with the kernel", xlabel="t", ylim=(-1.15, 2.2))
    ax[0].legend(loc="upper right", ncol=1)
    ax[1].semilogx(ns, fejer, "o", color=labs.BLUE, label="norm = (1/2pi) int |D_n|")
    ax[1].semilogx(ns, asym, color=labs.MUTED, ls="--", label="(4/pi^2) log n + 1.27")
    ax[1].semilogx(ns, reach, "x", color=labs.GOLD, label="s_n(f_n)(0) for the continuous f_n")
    ax[1].axhline(1, color=labs.GREEN, lw=1.2, label="Fejer kernel's norm: 1 for every n")
    ax[1].set(title="The norms are unbounded", xlabel="n", ylabel="norm of the functional", ylim=(0, 5))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
