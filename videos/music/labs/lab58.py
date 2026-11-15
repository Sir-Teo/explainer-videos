"""Lab 58: compression for the ear, computed: a lossless round trip, the MDCT's alias cancellation, a masking
threshold, a perceptual coder at several bit rates, and the power of an ABX test."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import codec as K

TITLE = "Compression for the ear, computed"
GOAL = ("Compress a sound losslessly and get every bit back, check that the MDCT's aliases cancel, compute a masking "
        "threshold, code a sound at several bit rates with a perceptual coder, and work out how many ABX trials it takes "
        "to find a subtle difference.")
TASKS = [
    "Change RATES. Where does the margin to the mask go negative, and what do you hear when it does?",
    "Change N (the MDCT size). Do the aliases still cancel? What happens to the masking threshold's detail?",
    "Change P_TRUE and TRIALS. How many trials does a listener who is right 65% of the time need to be found 80% of the time?",
]
RATES = [96, 48, 24, 12]
N = 1024
P_TRUE, TRIALS = 0.7, 16


def tone_mix(seconds=2.5, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(int(seconds * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * t) / (i + 1) for i, f in enumerate((220, 330, 440, 660, 880))) * 0.12
    x += 0.02 * rng.standard_normal(len(t)) * (1 + np.sin(2 * np.pi * 2 * t))
    return x * np.clip(t / 0.02, 0, 1)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    x = tone_mix(seed=seed)
    s = np.round(x * 32767).astype(np.int64)
    e = K.lossless_encode(s)
    ok = np.array_equal(K.lossless_decode(e["data"]), s)
    lab.row("lossless: size against 16-bit PCM, exact?", f"{100 * e['bits'] / (16 * len(s)):.0f} %, {ok}")
    assert ok
    y = K.frames_imdct(K.frames_mdct(x, N), N, len(x))
    lab.row(f"MDCT, N = {N}: largest error after overlap-add", f"{np.max(np.abs(y - x)):.1e}")
    assert np.max(np.abs(y - x)) < 1e-9
    m = K.mask(K.frames_mdct(x, N)[10], N)
    lab.row("one frame: tonality (0 noise, 1 tone), bands", f"{m['alpha']:.2f}, {len(m['bands'])}")
    coded = {}
    for kb in RATES:
        r = K.encode(x, kb, N=N)
        coded[kb] = r["y"]
        snr = 10 * np.log10(np.sum(x ** 2) / np.sum((x - r["y"]) ** 2))
        lab.row(f"coded at {kb} kbit/s: rate reached, margin to the mask, SNR", f"{r['kbps']:.1f}, {r['margin_db']:+.1f} dB, {snr:.1f} dB")
    lab.row(f"ABX: right answers needed in {TRIALS}; power for a listener right {100 * P_TRUE:.0f} %",
            f"{K.abx_threshold(TRIALS)}, {100 * K.abx_power(TRIALS, P_TRUE):.0f} %")

    order = list(rng.permutation(len(RATES)))
    lab.audio = concat([Clip(x, SR)] + [Clip(coded[RATES[i]], SR) for i in order], gap=0.6)
    lab.row("ear problem: after the original, the four coded versions: their bit rates? (listen first)", ", ".join(f"{RATES[i]}" for i in order))

    fig, (ax1, ax2) = labs.figure(2)
    f = (np.arange(N) + 0.5) * SR / (2 * N)
    X = K.frames_mdct(x, N)[10]
    ax1.semilogx(f, 10 * np.log10(X ** 2 + 1e-12), color="0.6", lw=0.6, label="frame")
    allowed = np.zeros(N)
    for (a, b), nb in zip(m["bands"], m["allowed"]):
        allowed[a:b] = nb / (b - a)
    ax1.semilogx(f, 10 * np.log10(allowed + 1e-12), color=labs.GOLD, label="allowed noise")
    ax1.set_xlabel("Hz")
    ax1.set_ylabel("dB")
    ax1.legend(fontsize=7)
    ns = np.arange(8, 101)
    ax2.plot(ns, [K.abx_power(int(n), P_TRUE) for n in ns], color="C0")
    ax2.set_xlabel("ABX trials")
    ax2.set_ylabel("power")
    lab.fig = fig
    lab.note = ("Lossless coding removes what can be predicted; perceptual coding removes what cannot be heard, by "
                "putting its noise under a masking threshold computed band by band; the MDCT makes that possible without "
                "sending extra numbers; and a listening test needs enough trials to see a small difference.")
    return lab
