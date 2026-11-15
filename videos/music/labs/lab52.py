"""Lab 52: FM, grains and physical models, computed: Bessel's sidebands, a granular stretch, a tuned string, and a clarinet's threshold."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import synth2 as F

TITLE = "FM, grains and physical models, computed"
GOAL = ("Check FM's lines against Bessel's functions, stretch a sound with grains, tune a Karplus-Strong string, and find "
        "the pressure at which a waveguide clarinet starts to sound.")
TASKS = [
    "Change RATIO and INDEX. Which ratios give a clear pitch, and at what index does the carrier's line vanish?",
    "Change GRAIN_MS and DENSITY in the stretch. When do you hear the grains themselves, and when a smooth stretch?",
    "Change BELL (the clarinet's bell filter) and find how the threshold pressure and the odd harmonics move.",
]
FC, RATIO, INDEX = 220.0, 1.4, 3.0
GRAIN_MS, DENSITY = 60.0, 50.0
BELL = 0.5


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    y = F.fm(FC, RATIO * FC, INDEX, SR)
    pred = [(f, a) for f, a in F.sidebands(FC, RATIO * FC, INDEX, 12) if 0 < f < 5000]
    meas = F.line_levels(y, [f for f, _ in pred])
    err = float(np.max(np.abs(meas - np.abs([a for _, a in pred]))))
    lab.row(f"FM {FC:g} Hz, ratio {RATIO:g}, index {INDEX:g}: lines below 5 kHz", f"{len(pred)}; largest |predicted - measured| {err:.2e}")
    t = np.arange(int(1.5 * SR)) / SR
    src = np.sin(2 * np.pi * 330 * t) * np.exp(-t / 0.8) + 0.3 * np.sin(2 * np.pi * 660 * t) * np.exp(-t / 0.4)
    st = F.grains(src, 4 * 1.2, lambda tt: tt / 4, density=DENSITY, grain_ms=GRAIN_MS, seed=seed)
    lab.row("granular stretch: grains used, length in and out (s)", f"{len(st['grains'])}; 1.2 -> 4.8")
    errs = []
    for m in (72, 84, 96):
        f = 440 * 2 ** ((m - 69) / 12)
        errs.append(1200 * np.log2(F.measured_pitch(F.ks_tuned(f, 0.6), guess=f) / f))
    lab.row("tuned Karplus-Strong at C5, C6, C7: error (cents)", ", ".join(f"{e:+.2f}" for e in errs))
    ps = np.round(np.arange(0.3, 1.31, 0.05), 2)
    rms = [float(np.sqrt(np.mean(F.clarinet(220.0, 0.4, pressure=float(p), breath=0.0, normalize=False, bell=BELL)[int(0.25 * SR):] ** 2))) for p in ps]
    on = ps[int(np.argmax(np.array(rms) > 0.1))]
    lab.row("clarinet: the tone starts at a mouth pressure of", f"{on:.2f} (1 closes the reed)")
    assert err < 1e-3 and max(abs(e) for e in errs) < 1.0

    # sound: the FM tone, the stretch, the clarinet; ear problem: FM at random ratios, harmonic or bell
    clips = [Clip(0.3 * y[: SR] * np.exp(-np.arange(SR) / SR / 0.6), SR), Clip(0.5 * st["y"] / np.max(np.abs(st["y"])), SR),
             Clip(0.4 * F.clarinet(220.0, 1.5, bell=BELL), SR)]
    answers = []
    for i in range(3):
        r = [1.0, 2.0, 1.4, 1.41421, 3.0, 2.76][int(rng.integers(0, 6))]
        n = int(1.2 * SR)
        e = np.exp(-np.arange(n) / SR / 0.6)
        clips.append(Clip(0.3 * e * F.fm(262.0, r * 262.0, 4.0 * e, n), SR))
        answers.append("harmonic" if r in (1.0, 2.0, 3.0) else "bell")
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem: the last three are harmonic or bells (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.stem([f for f, _ in pred], [abs(a) for _, a in pred], linefmt="C1-", markerfmt="C1o", basefmt=" ")
    ax1.plot([f for f, _ in pred], meas, "k.", label="measured")
    ax1.set_xlabel("Hz")
    ax1.set_ylabel("|J_k(I)|")
    ax1.legend(fontsize=7)
    ax2.plot(ps, rms, "o-", color=labs.GOLD)
    ax2.set_xlabel("mouth pressure")
    ax2.set_ylabel("RMS")
    lab.fig = fig
    lab.note = ("FM's lines are Bessel functions exactly; grains free time from pitch; an all-pass tunes a string to a "
                "fraction of a cent; a reed on a delay line has a threshold no one programmed.")
    return lab
