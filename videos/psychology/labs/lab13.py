"""Lab 13: counting quanta from a frequency-of-seeing curve, the eye's optics and the mosaic's limit, gain control
and Weber's law, the difference of Gaussians and Mach bands, Gabor cells, the CSF, and colour matching as linear
algebra checked against Stiles and Burch's 1955 data, with metamers built from the null space."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import vision as V

TITLE = "The eye and the code: quanta, filters and colour"
GOAL = ("Simulate Hecht, Shlaer and Pirenne's experiment and recover the number of quanta from the curve's shape; "
        "find the diffraction and mosaic limits; turn a saturating receptor into Weber's law with gain control; build "
        "the retina's difference of Gaussians and see Mach bands appear; tune a Gabor cell; fit a contrast "
        "sensitivity function; and derive colour-matching functions from the cone curves, check them against real "
        "1955 matches, and build a metamer.")
TASKS = [
    "Repeat the frequency-of-seeing experiment with 20, 50 and 200 flashes per intensity, 200 times each. How often "
    "is the fitted k within one of the truth? How many flashes did Hecht's argument need?",
    "Compute colour-matching functions for a display with primaries at 630, 532 and 467 nm. Where is each negative, "
    "and what does that say about the colours the display cannot show?",
    "Build a metamer of a daylight-lit leaf, then light both with a 2856 K lamp. Which cone class differs most, and "
    "by how much? Find the null-space direction that makes the difference largest.",
]


def run(seed=0):
    out = labs.Lab()
    rng = lambda k: np.random.default_rng(seed + k)  # noqa: E731

    # 1. counting quanta
    q = np.geomspace(25, 250, 7)
    y = V.simulate_fos(6, 0.09, q, 50, rng=rng(1))
    f = V.fit_fos(q, y, 50)
    out.row("Psyche (k = 6, 9% absorbed), 7 intensities x 50 flashes: fitted k and absorption", f"{f['k']}, {100 * f['efficiency']:.1f}%")
    out.row("steepness per tenfold step at the midpoint for k = 1, 6, 9", ", ".join(f"{V.fos_slope(k):.2f}" for k in (1, 6, 9)))
    lam = np.geomspace(0.1, 100, 2001)
    p1, p2 = V.frequency_of_seeing(lam, 6, 1.0), V.frequency_of_seeing(lam, 6, 0.1)
    i1, i2 = np.argmin(np.abs(p1 - 0.5)), np.argmin(np.abs(p2 - 0.5))
    assert abs(np.log10(lam[i2] / lam[i1]) - 1.0) < 0.01, "a tenfold loss slides the curve exactly one decade"

    # 2. optics and the mosaic
    out.row("diffraction cutoff for 2, 3 and 6 mm pupils (c/deg)", ", ".join(f"{V.cutoff_cpd(p):.0f}" for p in (2, 3, 6)))
    out.row("Nyquist limit of cones 0.5 arcmin apart; 80 c/deg sampled at 120/deg appears at",
            f"{V.nyquist_cpd(0.5):.0f}; {V.alias_cpd(80, 120):.0f} c/deg")

    # 3. gain control
    b = np.logspace(0, 8, 9)
    ratio = V.increment_threshold(b) / b
    out.row("increment threshold over background with gain control, 10^0 to 10^8", ", ".join(f"{r:.3f}" for r in ratio[::2]))
    assert np.allclose(ratio[2:], ratio[-1], rtol=0.05), "gain control gives a constant Weber fraction"

    # 4. the retina and the cortex
    m = V.mach_response(V.mach_profile())
    out.row("Mach bands: the filter's output at the dark corner and on the dark plateau", f"{m[148]:.3f} < {m[100]:.3f}")
    th = np.deg2rad(np.arange(-90, 91, 3))
    out.row("a Gabor complex cell's half-width at half height", f"{np.rad2deg(V.half_width(th, V.orientation_tuning(th))):.0f} deg")

    # 5. the CSF
    fq = np.array([0.5, 1, 2, 4, 8, 16, 24, 32])
    s = V.csf(fq) * 10 ** rng(5).normal(0, 0.08, len(fq))
    fit = V.fit_csf(fq, s)
    out.row("a CSF fitted to 8 noisy thresholds: peak, width (octaves); the acuity of the true curve",
            f"{fit['peak']:.1f} c/deg, {fit['bandwidth']:.1f}; {V.acuity_cpd():.0f} c/deg")

    # 6. colour matching against 1955
    cm = V.matching_functions(V.SB_PRIMARIES)
    idx = [int(np.where(V.WAVELENGTHS == w)[0][0]) for w in V.SB_WAVELENGTHS]
    r = [np.corrcoef(cm[idx, j], V.SB_RGB[:, j])[0, 1] for j in range(3)]
    out.row("derived colour-matching functions against Stiles and Burch (1955): r", ", ".join(f"{v:.4f}" for v in r))
    assert min(r) > 0.998, "three cone curves and one inverse reproduce the 1955 matches"
    base = V.surface(560, 70, 0.25, 0.55)
    twin = V.null_space_metamer(base, 0.9, seed=7)
    out.row("a metamer: cone excitations of A and B", f"{np.round(V.cone_excitations(base), 3)} = {np.round(V.cone_excitations(twin), 3)}")

    out.note = ("The curve's shape counts quanta without knowing the losses, because a loss only slides it along "
                "a log axis. Diffraction and the mosaic both stop near 60 to 90 cycles per degree. Gain control "
                "keeps the Weber fraction fixed over eight log units. Three cone curves and one 3-by-3 inverse "
                "reproduce ten observers' 1955 colour matches, and any spectrum plus a null-space wiggle is a metamer.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    lam = np.geomspace(0.3, 40, 300)
    for k, col in ((1, labs.GREY), (3, labs.BLUE), (6, labs.GREEN), (9, labs.PINK)):
        ax[0].plot(lam, V.frequency_of_seeing(lam, k), color=col, lw=1.6, label=f"k = {k}")
    ax[0].set_xscale("log")
    ax[0].set(title="Frequency of seeing", xlabel="mean quanta absorbed", ylabel="P(seen)")
    ax[0].legend(fontsize=8)
    for j, col in enumerate((labs.PINK, labs.GREEN, labs.BLUE)):
        ax[1].plot(V.SB_WAVELENGTHS, cm[idx, j] * np.dot(cm[idx, j], V.SB_RGB[:, j]) / np.dot(cm[idx, j], cm[idx, j]),
                   color=col, lw=1.6)
        ax[1].plot(V.SB_WAVELENGTHS[::2], V.SB_RGB[::2, j], "o", color=col, ms=3)
    ax[1].axhline(0, color=labs.GREY, lw=0.8)
    ax[1].set(title="Colour matching: derived (lines), 1955 (dots)", xlabel="wavelength (nm)", ylabel="amount")
    out.fig = fig
    return out
