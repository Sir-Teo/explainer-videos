"""Lab 50: dynamics, distortion and pitch, computed: shapers and their harmonics, a compressor, and a pitch corrector."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import dynamics as D
from videos.music.music50 import compute as C

TITLE = "Dynamics, distortion and pitch, computed"
GOAL = ("Design a shaper by its harmonics, compress a groove and measure what changed, and correct an out-of-tune voice.")
TASKS = [
    "Edit AMPS (harmonic amplitudes). Check the measured harmonics, then halve the input level and explain what moved.",
    "Change THRESHOLD, RATIO, ATTACK and RELEASE. Which setting most reduces the loudness spread? Which keeps the punch?",
    "Change DETUNE and SPEED_MS. At what speed does the corrected voice stop sounding like a singer?",
]
AMPS = [1.0, 0.0, 0.5, 0.0, 0.25]
THRESHOLD, RATIO, ATTACK, RELEASE = -24.0, 6.0, 3.0, 80.0
DETUNE, SPEED_MS = 0.45, 0.0


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    t = np.arange(SR) / SR
    x = np.cos(2 * np.pi * 220 * t)
    h = D.harmonics(D.cheb_shaper(AMPS, x), 220, SR, len(AMPS))
    lab.row("Chebyshev shaper, full input: harmonics (dB re the fundamental)", ", ".join(f"{v:.1f}" for v in h))
    h2 = D.harmonics(D.cheb_shaper(AMPS, 0.5 * x), 220, SR, len(AMPS))
    lab.row("the same shaper at half input", ", ".join(f"{v:.1f}" for v in h2))
    g = C.groove()
    r = D.compressor(g, SR, THRESHOLD, RATIO, 6, ATTACK, RELEASE)
    y = C.norm_rms(r["y"])
    lab.row("groove: loudness spread plain / compressed (dB, 20 ms windows)", f"{C.spread(C.norm_rms(g)):.1f} / {C.spread(y):.1f}")
    lab.row("crest factor plain / compressed (dB)", f"{D.crest_db(C.norm_rms(g)):.1f} / {D.crest_db(y):.1f}")
    v = C.sung(C.tune_notes(detune=DETUNE, seed=int(rng.integers(1000))))
    z, tt, f0, tg = C.correct_voice(v, SPEED_MS)
    ok = (f0 > 0) & (tg > 0)
    lab.row("voice: median pitch error before correction (cents)", f"{np.median(np.abs(1200 * np.log2(f0[ok] / tg[ok]))):.1f}")
    assert len(z) == len(v)

    # sound: compressed groove and corrected voice; ear problem: hard-tuned or natural, at random
    clips = [Clip(0.9 * y / np.max(np.abs(y)), SR), Clip(z, SR)]
    answers = []
    for i in range(3):
        vv = C.sung(C.tune_notes(detune=DETUNE, seed=int(rng.integers(1000))))
        if rng.random() < 0.5:
            clips.append(Clip(vv, SR))
            answers.append("natural")
        else:
            clips.append(Clip(C.correct_voice(vv, 0.0)[0], SR))
            answers.append("hard-tuned")
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: the last three are natural or hard-tuned (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.bar(range(1, len(h) + 1), np.maximum(h, -80), color=labs.GOLD, label="full")
    ax1.bar(np.arange(1, len(h2) + 1) + 0.3, np.maximum(h2, -80), width=0.3, color="C0", label="half")
    ax1.set_xlabel("harmonic")
    ax1.set_ylabel("dB")
    ax1.legend(fontsize=7)
    ax2.plot(tt, np.where(f0 > 0, f0, np.nan), color="C7", label="sung")
    ax2.plot(tt, np.where(tg > 0, tg, np.nan), color="C3", label="target")
    ax2.set_xlabel("s")
    ax2.set_ylabel("Hz")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A shaper's harmonics depend on the input level; a compressor narrows the loudness spread while its attack "
                "can keep the transients; pitch correction is detection, a target, and a shift that keeps the formants.")
    return lab
