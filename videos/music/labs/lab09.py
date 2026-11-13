"""Lab 9: a skin's overtones, a patch that tunes them, a bar carved to 1 : 4 : 10, two drums with one spectrum, and bells to tell apart by ear."""

import math

import numpy as np
from scipy.special import jn_zeros

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord.instruments import percussion as P

TITLE = "Percussion, computed: tuning things that nature tunes badly"
GOAL = ("Work out a drum's overtones from Bessel's zeros, load the skin at its centre and watch the overtones line up, "
        "carve a bar until its overtones are at 4 and 10 times its note, compare two drums that cannot be told apart, "
        "and name the third inside a bell by ear.")
TASKS = [
    "Set DENSITY to 1, 4 and 16. How does the worst miss change? Set PATCH to 0.2 and 0.6: does a small heavy patch or a large one do better?",
    "Set TARGET to 3.0. How deep is the cut for a xylophone, and where does its second overtone land?",
    "Set GRID to 8 and to 20. Do the two drums' spectra still agree with each other? Do they still agree with the published values?",
]
DIAMETER = 0.60     # the drum of Problem 1, metres
LOWEST = 80.0       # its lowest mode, Hz
PATCH = 0.4         # radius of the loaded patch, as a fraction of the skin's
DENSITY = 9.76      # how many times heavier the patch is
TARGET = 4.0        # where the bar's first overtone should be, in units of its note
GRID = 12           # mesh cells per unit length for the two drums
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a drumhead from Bessel's zeros (Problem 1)
    z = [float(jn_zeros(m, 1)[0]) for m in (0, 1, 2)]
    f = [LOWEST * v / z[0] for v in z]
    speed = 2 * math.pi * (DIAMETER / 2) * LOWEST / z[0]
    lab.row("zeros of J0, J1, J2", ", ".join(f"{v:.3f}" for v in z))
    lab.row("the drum's three lowest modes", ", ".join(f"{v:.1f} Hz" for v in f) + f"; {1200 * math.log2(f[1] / f[0]):.0f} and {1200 * math.log2(f[2] / f[0]):.0f} cents up")
    lab.row("speed of waves on the skin", f"{speed:.1f} m/s")
    assert abs(f[1] - 127.5) < 0.1 or LOWEST != 80.0

    # 2. a loaded skin
    bare = [r["ratio"] for r in P.drum_modes(9)]
    loaded = [r["ratio"] for r in P.tabla_modes(PATCH, DENSITY, 9)]
    lab.row("a bare skin's overtones", ", ".join(f"{r:.2f}" for r in bare))
    lab.row(f"with a patch {DENSITY:g} times as heavy out to {PATCH:g}", ", ".join(f"{r:.2f}" for r in loaded))
    lab.row("worst miss from 1, 2, 3, 4, 5", f"{P.harmonic_misfit(bare):.0f} cents bare; {P.harmonic_misfit(loaded):.0f} cents loaded")
    if (PATCH, DENSITY) == (0.4, 9.76):
        assert P.harmonic_misfit(loaded) < 70 < 500 < P.harmonic_misfit(bare)

    # 3. a bar and a knife (Problem 4): first an arch, then the shape of the arch as well
    plain = P.bar_modes(np.ones(240), count=3)
    lab.row("a plain bar's modes", " : ".join(f"{r:.2f}" for r in plain))
    cut = P.tune_bar(TARGET, power=2.0)
    lab.row(f"a round arch with the first overtone at {TARGET:g}", f"{100 * cut['depth']:.0f}% deep; modes " + " : ".join(f"{r:.2f}" for r in cut["ratios"][:3]))
    best = min((abs(P.tune_bar(TARGET, power=p)["ratios"][2] - (10.0 if TARGET == 4.0 else 6.0)), p) for p in np.arange(1.5, 4.51, 0.25))
    flat = P.tune_bar(TARGET, power=float(best[1]))
    lab.row("a flatter-bottomed arch (the cut's shape is a second handle)", f"power {best[1]:g}, {100 * flat['depth']:.0f}% deep; modes " + " : ".join(f"{r:.2f}" for r in flat["ratios"][:3]))
    lab.row("how far the cut lowers the bar's own note", f"{-math.log2(flat['lowered']):.2f} octaves")
    assert abs(flat["ratios"][1] - TARGET) < 1e-3 and (TARGET != 4.0 or abs(flat["ratios"][2] - 10.0) < 0.2)

    # 4. two drums, one spectrum
    a, b = P.membrane_eigs(P.GWW_1, 6, GRID), P.membrane_eigs(P.GWW_2, 6, GRID)
    lab.row("the two drums of 1992: their six lowest eigenvalues", ", ".join(f"{v:.3f}" for v in a))
    lab.row("largest difference between the two drums", f"{np.abs(a - b).max():.1e}")
    lab.row("the lowest, rescaled; published (Driscoll)", f"{a[0] / 4:.4f}; 2.5379")
    assert np.allclose(a, b, rtol=1e-8) and abs(a[0] / 4 - 2.5379) < 0.03

    # 5. the ear problem (Problem 3): five bells, minor or major third
    kinds = rng.integers(0, 2, 5)
    if kinds.min() == kinds.max():
        kinds[0] = 1 - kinds[0]
    notes = [Clip(P.bell(262.0, 2.4, tierce=1.25 if k else 1.2), SR).fade(0.001, 0.4).at_level(-20.0) for k in kinds]
    lab.audio = concat(notes, gap=0.35)
    lab.row("ear problem, the five bells (listen first)", "; ".join("major third" if k else "minor third" for k in kinds))

    fig, (p, q) = labs.figure(2)
    depths = np.linspace(0.0, 0.8, 33)
    r1 = [P.bar_modes(P.arch(float(d), 0.6, power=float(best[1])), count=3) for d in depths]
    p.plot(100 * depths, [r[1] / r[0] for r in r1], color=labs.GOLD, lw=1.4, label="first overtone / note")
    p.plot(100 * depths, [r[2] / r[0] for r in r1], color=labs.RED, lw=1.4, label="second overtone / note")
    for v in (3, 4, 6, 10):
        p.axhline(v, color="#888", lw=0.5, ls=":")
    p.set_title("Carving an arch under a bar")
    p.set_xlabel("depth of the cut (% of the thickness)")
    p.set_ylabel("ratio to the bar's note")
    p.legend()
    for k, (rs, col, name) in enumerate(((bare, "#888", "bare skin"), (loaded, labs.GOLD, "loaded skin"))):
        q.vlines(rs, k + 0.1, k + 0.9, color=col, lw=2, label=name)
    for v in range(1, 6):
        q.axvline(v, color="#888", lw=0.5, ls=":")
    q.set_yticks([])
    q.set_title("A skin's overtones, bare and loaded")
    q.set_xlabel("frequency, in units of the lowest mode")
    q.legend()
    lab.fig = fig
    lab.note = ("Strings and pipes are in tune by nature; skins, bars and bells are not. A weight at the centre of a skin, an arch "
                "under a bar, metal turned out of a bell: each moves some modes more than others, and the maker's art is knowing "
                "which. Going the other way, from the sound to the shape, has no unique answer: two drums can sound alike.")
    return lab
