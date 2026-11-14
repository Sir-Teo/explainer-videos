"""Lab 36: bronze and silk, computed: the rule of three and the twelve lü, how close chains of fifths come to closing,
qin harmonics, dissonance curves for harmonic and bar spectra, paired tuning by beat rate, and interlocking parts."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import bronze as B

TITLE = "Bronze and silk, computed"
GOAL = ("Generate the lü by the rule of three; find the chains of fifths that nearly close; compute dissonance curves "
        "for different spectra; design a paired tuning by beat rate; and split a figure into interlocking parts.")
TASKS = [
    "Change PARTIALS (a list of ratios). Where do the dissonance curve's minima fall? Is there one at the octave?",
    "Change BEAT. How many cents apart must the pair be at 100 Hz, 400 Hz and 1600 Hz?",
    "Write your own FIGURE and split it with bronze.interlock. Does every pulse sound exactly once?",
]
PARTIALS = B.bar_partials(4)
BEAT = 6.0
FIGURE = [1, 2, 3, 5, 3, 2, 1, 2, 3, 5, 6, 5, 3, 2, 3, 1]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    lu = B.sanfen_lu(12)
    lab.row("the twelve lü (cents, in order generated)", ", ".join(f"{x['cents']:.0f}" for x in lu))
    best = sorted(B.fifths_closeness(60), key=lambda r: abs(r["gap"]))[:4]
    lab.row("chains of fifths that nearly close (n: cents off)", ", ".join(f"{b['n']}: {b['gap']:+.2f}" for b in best))
    cs, d = B.dissonance_curve(PARTIALS)
    lab.row(f"dissonance minima for partials {[round(p, 2) for p in PARTIALS]}", str(B.minima(cs, d)))
    lab.row(f"paired tuning at {BEAT:g} Hz: cents apart at 100, 400, 1600 Hz",
            ", ".join(f"{1200 * np.log2((f + BEAT) / f):.1f}" for f in (100, 400, 1600)))
    a, b = B.interlock(FIGURE)
    assert all((x is None) != (y is None) for x, y in zip(a, b))
    lab.row("interlocking: polos / sangsih", f"{a} / {b}")

    # Problem 3: pairs of metallophones, some tuned apart
    kinds, clips = [], []
    for i in range(6):
        beat = float(rng.choice([0.0, 0.0, 4.0, 7.0]))
        f = 300.0
        y = B.metallophone(f, 2.0) + B.metallophone(f + beat, 2.0)
        clips.append(Clip(y, SR).at_level(-20.0))
        kinds.append("together" if beat == 0 else f"{beat:g} Hz")
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: each pair's tuning, in order (listen first)", ", ".join(kinds))

    fig, (ax1, ax2) = labs.figure(2)
    cs2, dh = B.dissonance_curve([1, 2, 3, 4, 5, 6])
    ax1.plot(cs2, dh / dh.max(), label="harmonic spectrum")
    ax1.plot(cs, d / d.max(), label="given partials")
    ax1.set_xlabel("interval (cents)")
    ax1.set_ylabel("dissonance (scaled)")
    ax1.legend(frameon=False)
    ax1.set_title("spectrum and scale")
    gaps = [r["gap"] for r in B.fifths_closeness(60)]
    ax2.bar(range(1, 61), np.abs(gaps), color=labs.GOLD)
    ax2.set_xlabel("number of fifths")
    ax2.set_ylabel("cents from closing")
    ax2.set_title("Jing Fang's search")
    lab.fig = fig
    lab.note = ("Fifty-three fifths come within 3.6 cents of 31 octaves; a bar's inharmonic partials move the dissonance "
                "minima away from the just intervals and the octave; and a constant beat needs less detuning at higher pitch.")
    return lab
