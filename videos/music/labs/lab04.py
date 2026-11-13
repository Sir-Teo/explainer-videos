"""Lab 4: the ear's transformer, its filters, a pitch that is not in the sound, and a safe dose."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import ear

TITLE = "A listener in numbers: the middle ear, critical bands, the missing fundamental"
GOAL = ("Compute the middle ear's gain, find which partials of a note the ear resolves, give Monochord's pitch model "
        "a note with no fundamental and a note whose partials have been shifted, and work out a safe listening time.")
TASKS = [
    "Set F0 to 65 Hz, then to 520 Hz. How many partials are resolved? Why do close chords sound muddy in the bass?",
    "Set LOWEST to 8, then 12 (only high, unresolved partials). What happens to the model's salience?",
    "Set SHIFT to 100 Hz (half the spacing of a 200 Hz note). The model's answer jumps: why are there two candidates?",
]
F0 = 300.0        # the note
LOWEST = 3        # the lowest partial present
COUNT = 3         # how many partials
SHIFT = 50.0      # every partial moved up by this many hertz
LEVEL = 103.0     # a concert, in dBA
PLUG = 15.0       # what the earplugs take off, in dB
SR = 48_000


def complex_tone(freqs, seconds=0.4):
    t = np.arange(int(seconds * SR)) / SR
    return sum(np.sin(2 * np.pi * f * t) for f in freqs)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the middle ear
    m = ear.middle_ear()
    lab.row("middle ear: pressure gain", f"{m['pressure_gain']:.1f} times = {m['gain_db']:.1f} dB")
    lab.row("power reaching the fluid", f"{100 * m['without']:.1f}% without it, {100 * m['with']:.0f}% with it")
    lab.row("ear canal's resonance", f"{ear.canal_resonance():.0f} Hz")
    assert abs(m["gain_db"] - 20 * math.log10(m["area_ratio"] * m["lever"])) < 1e-9

    # 2. which partials are resolved
    k = 1
    while float(ear.erb(k * F0)) < F0 and k < 60:
        k += 1
    lab.row(f"band of the ear at {F0:.0f} Hz", f"{float(ear.erb(F0)):.0f} Hz wide")
    lab.row("partials resolved", f"the first {k - 1}")
    assert 4 <= k - 1 <= 9

    # 3. a pitch that is not there, and one that moves
    partials = [F0 * n for n in range(LOWEST, LOWEST + COUNT)]
    moved = [f + SHIFT for f in partials]
    p_plain, s_plain = ear.pitch(complex_tone(partials), SR, lo=F0 / 2.5, hi=F0 * 2.7)
    p_moved, _ = ear.pitch(complex_tone(moved), SR, lo=F0 / 2.5, hi=F0 * 2.7)
    spec = np.abs(np.fft.rfft(complex_tone(partials) * np.hanning(int(0.4 * SR))))
    fr = np.fft.rfftfreq(int(0.4 * SR), 1 / SR)
    at_f0 = 20 * math.log10(max(spec[np.abs(fr - F0) < 10].max(), 1e-12) / spec.max())
    lab.row("partials", ", ".join(f"{f:.0f}" for f in partials) + " Hz")
    lab.row("level at the fundamental", f"{at_f0:.0f} dB")
    lab.row("the model's pitch", f"{p_plain:.1f} Hz   (salience {s_plain:.2f})")
    lab.row(f"all partials moved up {SHIFT:.0f} Hz", f"{p_moved:.1f} Hz: " + ("up" if p_moved > p_plain else "down")
            + f" by {1200 * math.log2(p_moved / p_plain):.0f} cents")
    if LOWEST <= 6 and SHIFT < F0 / 3:
        assert abs(1200 * math.log2(p_plain / F0)) < 5, "the missing fundamental is found"
        centre = LOWEST + (COUNT - 1) / 2
        assert abs(p_moved - (F0 + SHIFT / centre)) < 0.02 * F0, "the shift is the centre partial's share"

    # 4. a safe dose
    bare, plugged = ear.safe_hours(LEVEL), ear.safe_hours(LEVEL - PLUG)
    lab.row(f"safe time at {LEVEL:.0f} dBA", f"{60 * bare:.1f} minutes")
    lab.row(f"with {PLUG:.0f} dB earplugs", f"{plugged:.1f} hours ({plugged / bare:.0f} times as long)")
    assert abs(plugged / bare - 2 ** (PLUG / 3)) < 1e-9

    # the ear problem (Problem 3): the complex, a pure tone at the fundamental, one an octave above, the moved complex
    def clip(y):
        return Clip(y).fade(0.02, 0.08).at_level(-19.0)

    order = rng.permutation(2)
    pures = [("a pure tone at the fundamental", [F0]), ("a pure tone an octave above it", [2 * F0])]
    seq = [clip(complex_tone(partials, 1.2))] + [clip(complex_tone(pures[j][1], 1.2)) for j in order] + [clip(complex_tone(partials, 1.0)), clip(complex_tone(moved, 1.0))]
    lab.audio = concat(seq, gap=0.4)
    lab.row("ear problem (listen first)", f"the complex; {pures[order[0]][0]}; {pures[order[1]][0]}; the complex; the complex moved")

    fig, (a, b) = labs.figure(2)
    f = np.geomspace(100, 12000, 300)
    a.semilogx(f, ear.threshold_db(f), color=labs.BLUE, lw=1.6, label="threshold in quiet")
    a.semilogx(f, ear.masked_threshold(1000.0, 70.0, f), color=labs.RED, lw=1.6, label="beside a 1 kHz tone at 70 dB")
    a.set_title("What a loud tone hides")
    a.set_xlabel("frequency (Hz)")
    a.set_ylabel("level needed to be heard (dB)")
    a.legend()
    for freqs, col, name in ((partials, labs.GOLD, "partials as given"), (moved, labs.RED, f"moved up {SHIFT:.0f} Hz")):
        lags, s = ear.summary_acf(complex_tone(freqs), SR, max_lag=2.5 / F0)
        b.plot(1000 * lags, s, color=col, lw=1.4, label=name)
    b.axvline(1000 / F0, color=labs.BLUE, ls="--", lw=1.0, label=f"1/{F0:.0f} s")
    b.set_title("The pitch model: where the nerve's pattern repeats")
    b.set_xlabel("delay (ms)")
    b.set_ylabel("summary autocorrelation")
    b.legend()
    lab.fig = fig
    lab.note = ("The pitch model finds the fundamental although the sound has no energy there, and when every partial "
                "is moved by the same number of hertz it follows the listeners, not the spacing of the partials.")
    return lab
