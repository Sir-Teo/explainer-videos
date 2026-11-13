"""Lab 51: the sphere's equator, the thin shell and the singular values of a Gaussian matrix, against exact laws."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import hdp

TITLE = "Concentration in high dimensions: the equator, the shell, and root n plus or minus root p"
GOAL = ("Sample points uniformly on spheres of growing dimension and check the mass of the exact 95% equatorial "
        "band; check that the norm of a Gaussian vector has standard deviation near 0.707 in every dimension; and "
        "compare the extreme singular values of n x p Gaussian matrices with Gordon's bounds.")
TASKS = [
    "Fix the band's half-width at 0.1 and print hdp.sphere_band_mass(0.1, n) for n = 3 to 10,000. At which n does "
    "it pass 99%?",
    "Replace the Gaussian matrix entries by Rademacher signs. Do the extreme singular values still sit near root n "
    "plus or minus root p?",
    "Draw two independent directions with hdp.sample_sphere and plot their angle's standard deviation against n; "
    "compare with 1/sqrt(n) radians.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    dims = [3, 10, 100, 1000]
    for n in dims:
        t = hdp.sphere_band_for(0.95, n)
        x1 = hdp.sample_sphere(n, 20000, rng)[:, 0]
        inside = float(np.mean(np.abs(x1) <= t))
        lab.row(f"n = {n}: 95% half-width of one coordinate", f"{t:.4f}   (1.96/sqrt(n) = {1.96 / np.sqrt(n):.4f})   "
                f"simulated mass {inside:.3f}")
        assert abs(inside - 0.95) < 0.01, "the exact band holds 95%"
        assert abs(hdp.sphere_band_mass(t, n) - 0.95) < 1e-9
    assert abs(hdp.sphere_band_for(0.95, 1000) - 0.062) < 5e-4, "the film's number"

    shell = {}
    for n in (2, 100, 10000):
        norms = np.sqrt(rng.chisquare(n, 200000))
        shell[n] = (float(norms.std()), hdp.norm_chi_moments(n)["sd"], float(norms.mean()))
        lab.row(f"n = {n}: sd of ||g||", f"{shell[n][0]:.4f}   exact {shell[n][1]:.4f}   (mean {shell[n][2]:.2f})")
        assert abs(shell[n][0] / shell[n][1] - 1) < 0.02, "the chi law's sd"
    assert abs(shell[10000][1] - np.sqrt(0.5)) < 1e-3, "the shell's thickness does not grow with n"

    n = 400
    ps = [25, 50, 100, 200]
    ext = []
    for p in ps:  # as hdp.singular_extremes, by the eigenvalues of X'X (quick on any BLAS)
        ev = np.array([np.linalg.eigvalsh((X := rng.standard_normal((n, p))).T @ X)[[0, -1]] for _ in range(12)])
        sv = np.sqrt(ev)
        ext.append({"max": sv[:, 1].mean(), "min": sv[:, 0].mean(), "max_sd": sv[:, 1].std(), "min_sd": sv[:, 0].std(),
                    "gordon_max": np.sqrt(n) + np.sqrt(p), "gordon_min": np.sqrt(n) - np.sqrt(p)})
    for p, e in zip(ps, ext):
        lab.row(f"400 x {p}: mean largest / smallest singular value",
                f"{e['max']:.2f} / {e['min']:.2f}   Gordon: at most {e['gordon_max']:.2f}, at least {e['gordon_min']:.2f}")
        assert e["gordon_min"] < e["min"] < e["max"] < e["gordon_max"], "Gordon's bounds on the expectations"
        assert e["gordon_max"] - e["max"] < 0.9 and e["min"] - e["gordon_min"] < 0.9, "and they are nearly attained"
    lab.note = ("One coordinate of a random point on the sphere is about N(0, 1/n); the norm of a Gaussian vector "
                "is sqrt(n) give or take 0.71 in any dimension; a tall Gaussian matrix stretches every direction by "
                "between sqrt(n) - sqrt(p) and sqrt(n) + sqrt(p).")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.linspace(-1, 1, 2001)
    for n, color in zip((3, 10, 100), (labs.BLUE, labs.GREEN, labs.GOLD)):
        ax[0].plot(x, hdp.sphere_coordinate_pdf(x, n), color=color, label=f"n = {n}")
        t = hdp.sphere_band_for(0.95, n)
        ax[0].plot([-t, t], [-0.12 * (1 + dims.index(n))] * 2, color=color, lw=4, solid_capstyle="butt")
    ax[0].text(-0.98, -0.52, "bars: the band holding 95%", color=labs.MUTED, fontsize=9, va="center")
    ax[0].set(title="Exact density of one coordinate on the sphere", xlabel="x1", ylabel="density", ylim=(-0.65, 4.3))
    ax[0].legend()
    ax[1].plot(ps, [e["gordon_max"] for e in ext], color=labs.MUTED, ls="--", label="sqrt(n) ± sqrt(p)")
    ax[1].plot(ps, [e["gordon_min"] for e in ext], color=labs.MUTED, ls="--")
    ax[1].errorbar(ps, [e["max"] for e in ext], yerr=[2 * e["max_sd"] for e in ext], fmt="o", color=labs.RED,
                   label="largest singular value (± 2 sd)")
    ax[1].errorbar(ps, [e["min"] for e in ext], yerr=[2 * e["min_sd"] for e in ext], fmt="o", color=labs.BLUE,
                   label="smallest singular value (± 2 sd)")
    ax[1].set(title="Gaussian matrices with n = 400 rows", xlabel="columns p", ylabel="singular value")
    ax[1].legend(loc="center left")
    lab.fig = fig
    return lab
