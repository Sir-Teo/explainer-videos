"""Lab 48: digital audio, computed: aliasing, quantization at any word length, dither, noise shaping and a one-bit
modulator."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import digital as D
from videos.music.music48 import compute as C

TITLE = "Digital audio, computed"
GOAL = ("Sample and fold a tone, quantize the Tune to any word length with and without dither, shape the noise, and "
        "build a one-bit converter.")
TASKS = [
    "Change TONE and RATE. Predict the frequency you will hear before you run it, then check against alias().",
    "Change BITS (2 to 16) and DITHER ('none', 'rpdf', 'tpdf'). When does dither stop being worth its extra noise?",
    "Change ORDER (1 or 2) and OSR. How many decibels does each doubling of OSR buy?",
]
TONE, RATE = 7000.0, 8000
BITS, DITHER = 6, "tpdf"
ORDER, OSR = 2, 32


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    lab.row(f"a {TONE:.0f} Hz tone sampled at {RATE} Hz is heard at", f"{D.alias(TONE, RATE):.0f} Hz")
    x = C.tune_signal((0,), peak=0.9)
    q = D.quantize(x, BITS, DITHER, rng)
    lab.row(f"the Tune at {BITS} bits, {DITHER} dither: signal to error", f"{D.snr_db(x, q):.1f} dB (rule for a full-scale sine: {D.theory_snr(BITS):.1f})")
    m = D.error_moments(BITS, DITHER, 11, 2000, seed)
    lab.row("error mean across one step: largest |mean|, spread of variance (steps)", f"{max(abs(v) for v in m['mean']):.2f}, {max(m['var']) - min(m['var']):.2f}")
    sh = D.shaped(x, BITS, 2, DITHER, rng)
    f, P0 = D.noise_spectrum(q - x, SR)
    _, P2 = D.noise_spectrum(sh - x, SR)
    lo = f < 4000
    lab.row("error below 4 kHz, flat / second-order shaped (mean dB per band)", f"{np.mean(P0[lo]):.1f} / {np.mean(P2[lo]):.1f}")
    fs = 48000 * OSR
    t = np.arange(int(0.1 * fs)) / fs
    snr = D.band_snr_db(D.delta_sigma(0.5 * np.sin(2 * np.pi * 1000 * t), ORDER), 1000, fs, 20000)
    lab.row(f"one bit, order {ORDER}, {OSR} times 48 kHz: SNR below 20 kHz", f"{snr:.1f} dB")
    assert snr > 0

    # sound: the Tune at BITS with and without dither; ear problem: three versions in random order
    plain = D.quantize(x, BITS, "none")
    clips, answers = [Clip(plain, SR), Clip(q, SR)], []
    for i in range(3):
        if rng.random() < 0.5:
            clips.append(Clip(D.quantize(x, 4, "none"), SR))
            answers.append("4 bits, no dither")
        else:
            clips.append(Clip(D.quantize(x, 4, "tpdf", rng), SR))
            answers.append("4 bits, dithered")
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: the last three are each 4 bits with or without dither (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    k = slice(20000, 20400)
    ax1.plot(x[k], color="C7", label="the Tune")
    ax1.plot(q[k], color=labs.GOLD, label=f"{BITS} bits, {DITHER}")
    ax1.set_xlabel("sample")
    ax1.legend(fontsize=7)
    ax2.plot(f, P0, color="C0", label="flat")
    ax2.plot(f, P2, color="C3", label="shaped")
    ax2.set_xlabel("Hz")
    ax2.set_ylabel("error, dB")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Each bit buys about 6 dB; triangular dither makes the error plain noise at the cost of 4.8 dB; shaping "
                "moves that noise up out of the ear's way; and one bit suffices if the rate is high enough.")
    return lab
