"""Lab 64: source separation, computed: a two-source mixture of tones and drum hits pulled apart by median filtering,
by supervised NMF and by the oracle masks that bound them; a dry two-channel mixture unmixed by FastICA; Griffin-Lim's
phase, consistent but not correct; and SDR's blind spots."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord.mir import separate as S
from explainer.music.monochord.partkit import organ_tone

TITLE = "Source separation, computed"
GOAL = ("Mix tones with drum hits, separate them three ways, score each against the truth and against the best any mask "
        "could do, unmix a stereo pair blindly, and see where the signal-to-distortion ratio disagrees with your ears.")
TASKS = [
    "Change KERNEL, the median filters' length. Which length separates these tones from these hits best, and why?",
    "Change RANK, the templates per source. When do more templates stop helping?",
    "Change ROOM to True. Why does ICA, perfect on the dry mix, fail when each microphone hears echoes?",
]
KERNEL = 17
RANK = 6
ROOM = False


def tones(midis, seed=0, seconds=4.0):
    rng = np.random.default_rng(seed)
    y = np.zeros(int(seconds * SR))
    for k, m in enumerate(midis):
        d = float(rng.choice([0.4, 0.5, 0.8]))
        z = organ_tone(440 * 2 ** ((m - 69) / 12), d, partials=6, rolloff=0.7)
        i = int(k * 0.5 * SR)
        if i < len(y):
            y[i:i + len(z)] += z[: len(y) - i]
    return y


def hits(seed=0, seconds=4.0, every=0.25):
    rng = np.random.default_rng(seed)
    y = np.zeros(int(seconds * SR))
    n = int(0.03 * SR)
    for t in np.arange(0.02, seconds - 0.05, every):
        i = int(t * SR)
        y[i:i + n] += rng.standard_normal(n) * np.exp(-np.arange(n) / (0.006 * SR))
    return y * 0.9 / np.std(y)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    melody = [60, 62, 64, 65, 67, 65, 64, 62]
    a, b = tones(melody, seed), hits(seed)
    x = a + b
    lab.row("the mixture: tones and hits, equally loud", f"{np.std(a):.2f}, {np.std(b):.2f}")

    r = S.hpss(x, harm=KERNEL, perc=KERNEL)
    lab.row(f"median filtering ({KERNEL} frames or bins): SDR tones, hits", f"{S.sdr(a, r['harmonic']):.1f} dB, {S.sdr(b, r['percussive']):.1f} dB")

    examples = {"tones": tones([59, 61, 63, 66, 68, 66, 63, 61], seed + 1), "hits": hits(seed + 1)}
    est = S.nmf_separate(x, examples, rank=RANK, iters=100)
    s_nmf = S.sdr(a, est["tones"])
    lab.row(f"supervised NMF ({RANK} templates each): SDR tones, hits", f"{s_nmf:.1f} dB, {S.sdr(b, est['hits']):.1f} dB")

    o = S.oracle_masks({"tones": a, "hits": b})
    s_ibm, s_irm, s_tp = (S.sdr(a, o[m]["tones"]) for m in ("ibm", "irm", "true_phase"))
    lab.row("the bounds for the tones: ideal binary, ideal ratio, ratio with true phase", f"{s_ibm:.1f}, {s_irm:.1f}, {s_tp:.1f} dB")
    assert s_irm > S.sdr(a, x) and s_tp >= s_irm - 0.5

    A = np.array([[0.9, 0.35], [0.4, 0.85]])
    X = A @ np.array([a, b])
    if ROOM:
        h = rng.standard_normal(int(0.3 * SR)) * np.exp(-np.arange(int(0.3 * SR)) / (0.08 * SR))
        h[0] = 8.0
        X = np.array([np.convolve(X[0], h)[: X.shape[1]], np.convolve(X[1], h[::-1].copy())[: X.shape[1]]])
    out = S.fastica(X)["S"]
    corr = max(abs(np.corrcoef(a, z)[0, 1]) for z in out)
    lab.row(f"FastICA on a {'room' if ROOM else 'dry'} two-channel mixture: best correlation with the tones", f"{corr:.4f}")
    if not ROOM:
        assert corr > 0.99

    mag = np.abs(S.stft(a))
    gl = S.griffin_lim(mag, len(a), iters=50)
    incons = 20 * np.log10(np.linalg.norm(np.abs(S.stft(gl)) - mag) / np.linalg.norm(mag))
    lab.row("Griffin-Lim on the tones' true magnitude: inconsistency, SDR", f"{incons:.1f} dB, {S.sdr(a, gl):.1f} dB")
    assert S.sdr(a, gl) < s_irm

    late = np.concatenate([np.zeros(48), a[:-48]])
    lab.row("SDR of a perfect estimate half as loud, upside down, 1 ms late",
            f"{S.sdr(a, 0.5 * a):.1f}, {S.sdr(a, -a):.1f}, {S.sdr(a, late):.1f} dB")

    n = lambda y: Clip(y / np.max(np.abs(y)) * 0.8, SR)
    lab.audio = concat([n(x), n(r["harmonic"]), n(est["tones"]), n(o["irm"]["tones"])], gap=0.6)
    order = sorted([("median filter", S.sdr(a, r["harmonic"])), ("NMF", s_nmf), ("ideal ratio mask", s_irm)], key=lambda t: t[1])
    lab.row("ear problem: the mixture, then the tones three ways; rank them by ear, then check", " < ".join(f"{k} ({v:.1f} dB)" for k, v in order))

    fig, (ax1, ax2) = labs.figure(2)
    X_ = np.abs(S.stft(x))[:300]
    ax1.imshow(np.log10(X_ + 1e-4), origin="lower", aspect="auto", cmap="magma")
    ax1.set_xlabel("frame")
    ax1.set_ylabel("bin")
    ax1.set_title("the mixture: lines and stripes", fontsize=8)
    ax2.imshow(r["mask"][:300], origin="lower", aspect="auto", cmap="gray", vmin=0, vmax=1)
    ax2.set_xlabel("frame")
    ax2.set_title("the harmonic mask", fontsize=8)
    lab.fig = fig
    lab.note = ("Every separator here is a mask on a spectrogram, bounded by the ideal masks, which need the answer; the "
                "mixture's phase is the error no mask removes; and SDR counts every difference, audible or not.")
    return lab
