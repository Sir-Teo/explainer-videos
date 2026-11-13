"""Lab 5: Euler's numbers, a dissonance curve and its valleys, a timbre of your own, and an interval to judge by ear."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import consonance as K

TITLE = "Consonance, computed: where the valleys are, and how to move them"
GOAL = ("Rank the intervals by Euler's formula, draw the roughness of two tones against their interval, find its "
        "valleys, and do the same for a timbre whose partials are not whole multiples.")
TASKS = [
    "Set PARTIALS to [1, 2, 3] and then to [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]. Which valleys appear as partials are added?",
    "Set STRETCH to 1.9 (compressed octaves). Where is the deepest valley now? Check it against 2 ** log2(1.9) = 1.9.",
    "Set F0 to 65 Hz (two octaves down). Which valleys survive? Why do thirds sound muddy in the bass?",
]
F0 = 261.63                      # the lower note
STRETCH = 2.0                    # 2.0: partials at whole multiples; 2.1: every octave of the series stretched
PARTIALS = [1, 2.76, 5.40, 8.93]  # your own timbre: a uniform bar struck at its middle (Problem 4)
SR = 48_000


def tone(freqs, amps, seconds=1.6):
    t = np.arange(int(seconds * SR)) / SR
    return sum(a * np.sin(2 * np.pi * f * t) for f, a in zip(freqs, amps) if f < 0.45 * SR)


def curve_for(freqs, amps, ratios):
    return np.array([K.roughness(np.concatenate([freqs, r * freqs]), np.concatenate([amps, amps])) for r in ratios])


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Euler's numbers
    order = sorted(K.JUST, key=lambda n: (K.euler_gradus(*K.JUST[n]), K.tenney(*K.JUST[n])))
    lab.row("Euler, sweetest first", ", ".join(f"{n} {K.euler_gradus(*K.JUST[n])}" for n in order[:6]))
    lab.row("Euler, problem 1", f"16:9 scores {K.euler_gradus(16, 9)}, 7:4 scores {K.euler_gradus(7, 4)}")
    assert K.euler_gradus(3, 2) == 4 and K.euler_gradus(5, 4) == 7

    # 2. the curve for a tone with partials at f0 * k^(log2 STRETCH)
    r = np.linspace(1.0, 2.3, 2601)
    f, a = K.harmonic_partials(F0, 7, 0.88, STRETCH)
    c = curve_for(f, a, r)
    valleys = K.minima(r, c, depth=0.01)
    lab.row("seven partials, stretch", f"{STRETCH:g}")
    lab.row("valleys of the curve", ", ".join(f"{v:.3f}" for v in valleys))
    if STRETCH == 2.0 and F0 > 200:
        want = [7 / 6, 6 / 5, 5 / 4, 4 / 3, 7 / 5, 3 / 2, 5 / 3, 7 / 4, 2.0]
        assert len(valleys) == len(want) and all(abs(x - y) < 0.004 for x, y in zip(valleys, want)), "the just ratios"
        lab.row("as ratios", ", ".join("%d:%d" % K.nearest_ratio(v, 9) for v in valleys))
    else:
        assert abs(valleys[-1] - STRETCH) < 0.01 or F0 < 200, "the deepest valley is the stretched octave"

    # 3. your own timbre
    pf = F0 * np.asarray(PARTIALS, dtype=float)
    pa = 0.8 ** np.arange(len(pf))
    r2 = np.linspace(1.0, max(PARTIALS[1] * 1.1, 2.3), 3001)
    c2 = curve_for(pf, pa, r2)
    v2 = K.minima(r2, c2, depth=0.005)
    lab.row("your partials", ", ".join(f"{p:g}" for p in PARTIALS))
    ratios_of_partials = sorted({round(x / y, 3) for x in PARTIALS for y in PARTIALS if 1 < x / y <= r2[-1]})
    sharp = [v for v in v2 if min(abs(v - q) for q in ratios_of_partials) < 0.01]
    broad = [v for v in v2 if v not in sharp]
    lab.row("ratios between its partials", ", ".join(f"{x:.3f}" for x in ratios_of_partials))
    lab.row("valleys where two partials meet", ", ".join(f"{v:.3f}" for v in sharp))
    lab.row("valleys where nothing is close", ", ".join(f"{v:.3f}" for v in broad) or "none")
    assert len(sharp) == len(ratios_of_partials), "every ratio between two partials is a valley"

    # 4. the ear problem (Problem 3): one interval, in an ordinary tone and in a stretched one
    interval = float(rng.choice([2.0, 2.1]))
    plain, bent = K.harmonic_partials(F0, 7, 0.88, 2.0), K.harmonic_partials(F0, 7, 0.88, 2.1)

    def dyad(parts):
        fr, am = parts
        return Clip(tone(fr, am) + tone(interval * fr, am)).fade(0.03, 0.1).at_level(-18.0)

    lab.audio = concat([dyad(plain), dyad(bent)], gap=0.5)
    rough = [K.dyad_roughness(interval, F0, 7, 0.88, s) for s in (2.0, 2.1)]
    lab.row("ear problem (listen first)", f"the interval is {interval:g} : 1; roughness {rough[0]:.2f} in the ordinary tone, {rough[1]:.2f} in the stretched one")
    assert (rough[0] < rough[1]) == (interval == 2.0)

    fig, (ax, bx) = labs.figure(2)
    ax.plot(r, c, color=labs.RED, lw=1.6)
    for v in valleys:
        ax.axvline(v, color=labs.BLUE, lw=0.6, ls=":")
    ax.set_title(f"Two tones of seven partials (stretch {STRETCH:g})")
    ax.set_xlabel("interval (ratio)")
    ax.set_ylabel("roughness")
    bx.plot(r2, c2, color=labs.GOLD, lw=1.6)
    for v in v2:
        bx.axvline(v, color=labs.BLUE, lw=0.6, ls=":")
    bx.set_title("Two tones with your partials")
    bx.set_xlabel("interval (ratio)")
    bx.set_ylabel("roughness")
    lab.fig = fig
    lab.note = ("Wherever a partial of one tone lands on a partial of the other, the curve has a sharp valley: at the just ratios "
                "for a harmonic tone, at other intervals for any other timbre. Broad valleys also lie where no two partials are close.")
    return lab
