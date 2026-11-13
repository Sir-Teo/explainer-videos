"""Lab 8: a pipe's resonances, the pressure at which a reed speaks, holes for a scale, and four vowels to name by ear."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord.instruments import winds as W

TITLE = "Winds, computed: a column of air and a valve"
GOAL = ("Find a pipe's resonances with and without its end correction, find the blowing pressure at which a reed begins "
        "to sound, place six holes for a major scale, and name four sung vowels from their formants.")
TASKS = [
    "Set RADIUS to 0.02. How much do the resonances fall, and why does a fat pipe need a bigger end correction?",
    "Set ZETA to 0.2 (a tighter embouchure). Does the reed speak at a higher or a lower pressure? Why does the lossless answer, 1/3, not change?",
    "Set HOLE to 0.002 and to 0.0075. Which holes move furthest from where a saw would cut, the small ones or the large?",
]
LENGTH = 0.40      # the pipe of Problem 1, metres
RADIUS = 0.01      # and its radius
ZETA = 0.35        # the reed's embouchure parameter
HOLE = 0.004       # radius of the finger holes, metres
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a pipe's resonances (Problem 1)
    pipe = W.cylinder(LENGTH, RADIUS)
    plain_open = [n * W.C / (2 * LENGTH) for n in (1, 2, 3)]
    corr_open = [n * W.C / (2 * (LENGTH + 2 * 0.6133 * RADIUS)) for n in (1, 2, 3)]
    plain_shut = [n * W.C / (4 * LENGTH) for n in (1, 3, 5)]
    corr_shut = [n * W.C / (4 * (LENGTH + 0.6133 * RADIUS)) for n in (1, 3, 5)]
    got_open = [p[0] for p in pipe.peaks(1500, admittance=True)][:3]
    got_shut = [p[0] for p in pipe.peaks(1500)][:3]
    fmt = lambda xs: ", ".join(f"{x:.0f}" for x in xs)     # noqa: E731
    lab.row("open at both ends: no correction; corrected; computed", f"{fmt(plain_open)}; {fmt(corr_open)}; {fmt(got_open)} Hz")
    lab.row("closed at one end: no correction; corrected; computed", f"{fmt(plain_shut)}; {fmt(corr_shut)}; {fmt(got_shut)} Hz")
    assert all(abs(1200 * math.log2(a / b)) < 25 for a, b in zip(got_open, corr_open))
    assert all(abs(1200 * math.log2(a / b)) < 25 for a, b in zip(got_shut, corr_shut))

    # 2. where the reed's flow is greatest (Problem 2), and where a reed on this pipe begins to speak
    dp = np.linspace(0.0, 1.0, 3001)
    top = float(dp[int(np.argmax(W.reed_flow(dp, ZETA)))])
    lab.row("the flow through a reed is greatest at", f"{top:.3f} of the pressure that shuts it")
    assert abs(top - 1 / 3) < 1e-3
    lo, hi = 0.30, 0.50
    for _ in range(4):
        mid = 0.5 * (lo + hi)
        if W.playing(W.reed_tone(pipe, mid, 1.2, zeta=ZETA)["p"])["amp"] > 0.02:
            hi = mid
        else:
            lo = mid
    lab.row("a reed on this pipe speaks at about", f"{0.5 * (lo + hi):.2f} of that pressure")
    assert lo >= 0.30 and hi <= 0.50

    # 3. six holes for a major scale (Problem 4)
    clar, a = 0.60, 0.0075
    f0 = W.cylinder(clar, a).peaks(400)[0][0]
    rows = []
    for name, ratio in (("re", 9 / 8), ("mi", 5 / 4), ("fa", 4 / 3), ("so", 3 / 2), ("la", 5 / 3), ("ti", 15 / 8)):
        target = f0 * ratio
        x_lo, x_hi = 0.15, clar - 0.01                       # a hole nearer the reed gives a higher note
        for _ in range(18):
            x = 0.5 * (x_lo + x_hi)
            f1 = W.Bore().tube(x, a).hole(HOLE, 0.003).tube(clar - x, a).peaks(1.5 * target, df=0.5)[0][0]
            if f1 > target:
                x_lo = x
            else:
                x_hi = x
        saw = (W.C / (4 * target)) - 0.6133 * a
        rows.append((name, x, saw))
    lab.row("holes for a major scale, cm from the reed", "; ".join(f"{n} {100 * x:.1f}" for n, x, _ in rows))
    lab.row("  each hole, cm above where a saw would cut", "; ".join(f"{n} {100 * (s - x):.1f}" for n, x, s in rows))
    assert all(x < s for _, x, s in rows)                    # a hole is never as good as a saw: it must sit higher up

    # 4. the ear problem (Problem 3): one note, four vowels
    vowels = list(W.VOWELS)
    pick = [vowels[j] for j in rng.permutation(len(vowels))[:4]]
    lab.audio = concat([Clip(W.voice(131.0, W.VOWELS[v], 1.2, seed=k), SR).fade(0.03, 0.08).at_level(-20.0) for k, v in enumerate(pick)], gap=0.4)
    lab.row("ear problem, the four words (listen first)", "; ".join(W.VOWEL_WORDS[v] for v in pick))
    lab.row("  their first two formants", "; ".join(f"{W.VOWEL_WORDS[v]} {W.VOWELS[v][0]}, {W.VOWELS[v][1]}" for v in pick))

    fig, (p, q) = labs.figure(2)
    f = np.arange(60.0, 1500.0, 1.0)
    p.plot(f, 20 * np.log10(np.abs(pipe.impedance(f))), color=labs.GOLD, lw=1.2)
    for x in got_shut:
        p.axvline(x, color=labs.RED, lw=0.6, ls=":")
    for x in got_open:
        p.axvline(x, color=labs.BLUE, lw=0.6, ls=":")
    p.set_title(f"A pipe {100 * LENGTH:.0f} cm long: peaks for a reed, valleys for a flute")
    p.set_xlabel("frequency (Hz)")
    p.set_ylabel("input impedance (dB)")
    for v, fm in W.VOWELS.items():
        q.plot(fm[0], fm[1], "o", color=labs.RED if v in pick else "#888", ms=5)
        q.annotate(W.VOWEL_WORDS[v], (fm[0], fm[1]), textcoords="offset points", xytext=(5, 3), fontsize=7)
    q.set_title("The vowels (Peterson and Barney, men); the lab's four in colour")
    q.set_xlabel("first formant (Hz)")
    q.set_ylabel("second formant (Hz)")
    lab.fig = fig
    lab.note = ("A wind instrument is a column of air and a valve. The column's resonances come from its shape, by arithmetic; "
                "the valve decides whether, and how brightly, they sound; and a voice is the one instrument in which the two "
                "are set independently, so that a vowel is a place on a map of two formants.")
    return lab
