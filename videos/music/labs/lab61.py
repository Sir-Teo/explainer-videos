"""Lab 61: pitch, onsets and transcription, computed: YIN against noise, spectral-flux onsets, and NMF with note
templates, scored against exact answer keys on a timbre it learnt and one it never heard."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord.instruments.strings import karplus_strong
from explainer.music.monochord.mir import transcribe as TR
from explainer.music.monochord.partkit import organ_tone

TITLE = "Pitch, onsets and transcription, computed"
GOAL = ("Track one voice's pitch with YIN as noise rises, find where notes begin, and transcribe polyphony by factorizing "
        "a spectrogram with note templates learnt from one instrument, then score it, note by note, on that instrument "
        "and on one it never heard.")
TASKS = [
    "Change SNRS. At what noise level does YIN start making octave errors on the test tone?",
    "Change DELTA, the onset threshold. Plot precision against recall on the harp.",
    "Learn the templates from the harp instead of the organ (TRAIN). Which instrument is now hard?",
]
SNRS = [20, 10, 0, -5]
DELTA = 0.07
TRAIN = "organ"
LO, HI = 55, 79


def note(inst, m, dur):
    hz = float(TR.midi_hz(m))
    if inst == "organ":
        y = organ_tone(hz, dur, partials=6, rolloff=0.7)
        k = int(0.02 * SR)
        y[:k] *= np.linspace(0, 1, k)
        y[-k:] *= np.linspace(1, 0, k)
    else:
        y = karplus_strong(hz, dur + 0.2, seed=m)
    return y / (np.sqrt(np.mean(y[: int(0.2 * SR)] ** 2)) + 1e-12) * 0.1


def render(notes, inst, seconds):
    y = np.zeros(int(seconds * SR) + SR)
    for m, a, b in notes:
        z = note(inst, m, b - a)
        k = int(a * SR)
        y[k:k + len(z)] += z
    return y[: int(seconds * SR)] / (np.max(np.abs(y)) + 1e-12) * 0.9


def piece(seed, seconds=5.0):
    rng = np.random.default_rng(seed)
    out, t = [], 0.0
    while t < seconds - 1.0:
        for _ in range(rng.poisson(0.4)):
            m = int(rng.integers(LO, HI + 1))
            if all(not (n[0] == m and n[1] <= t < n[2]) for n in out):
                out.append((m, round(t, 3), round(t + float(rng.choice([0.25, 0.5])), 3)))
        t += 0.125
    return out


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    t = np.arange(SR) / SR
    x = sum(a * np.sin(2 * np.pi * 196.0 * (k + 1) * t) for k, a in enumerate((0.3, 1.0, 0.7, 0.5)))
    for snr in SNRS:
        y = x + rng.standard_normal(len(x)) * np.std(x) * 10 ** (-snr / 20)
        a, b = TR.yin(y, SR), TR.acf_f0(y, SR)
        truth = np.full(len(a["f0"]), 196.0)
        ga = TR.gross_error(a["f0"], truth)
        lab.row(f"G3 tone at {snr:+d} dB: YIN and autocorrelation gross errors", f"{100 * ga:.0f}%, {100 * TR.gross_error(b['f0'], truth[:len(b['f0'])]):.0f}%")
        if snr == max(SNRS):
            assert ga < 0.05                                       # clean enough, YIN finds the period
    mel = [(60 + p, 0.4 * i, 0.4 * i + 0.35) for i, p in enumerate([0, 0, 7, 7, 9, 9, 7])]
    yh = render(mel, "harp", 3.4)
    o = TR.onset_strength(yh, SR)
    est = TR.pick_onsets(o["odf"], o["hop_s"], delta=DELTA)
    s = TR.onset_scores([n[1] for n in mel], est.tolist())
    lab.row(f"harp onsets (threshold {DELTA}): precision, recall", f"{s['precision']:.2f}, {s['recall']:.2f}")
    assert s["recall"] > 0.5                                       # a plucked string's attacks are easy to find
    spectra = {}
    for m in range(LO, HI + 1):
        S = TR.logfreq(note(TRAIN, m, 0.8), SR)["S"]
        spectra[m] = S[:, 1:30]
    W, keys = TR.note_templates(spectra)
    fs = {}
    for inst in ("organ", "harp"):
        f = []
        for k in range(4):
            nt = piece(100 + k)
            S = TR.logfreq(render(nt, inst, 5.0), SR)
            H = TR.nmf(S["S"], W=W, fix_W=True, iters=100)["H"]
            est = TR.activations_to_notes(H, keys, S["hop_s"], on=0.12, rel=True)
            f.append(TR.note_scores(nt, est)["f"])
        lab.row(f"NMF with {TRAIN} templates on the {inst}: note F", f"{np.mean(f):.2f}")
        fs[inst] = float(np.mean(f))
    if TRAIN == "organ":
        assert fs["organ"] > fs["harp"]                             # templates fit the instrument they came from
    # the ear problem: chords with and without an added octave
    chords = []
    order = list(rng.permutation(4))
    for i in order:
        base = [(60, 0, 1.2), (64, 0, 1.2), (67, 0, 1.2)] + ([(72, 0, 1.2)] if i % 2 else [])
        chords.append((Clip(render(base, "organ", 1.4), SR), bool(i % 2)))
    lab.audio = concat([c for c, _ in chords], gap=0.5)
    lab.row("ear problem: four organ chords; which have the C an octave up? (listen first)", ", ".join("yes" if h else "no" for _, h in chords))
    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(o["t"], o["odf"], color=labs.GOLD, lw=1)
    for n in mel:
        ax1.axvline(n[1], color="0.6", lw=0.6)
    ax1.set_xlabel("s")
    ax1.set_ylabel("flux")
    ax2.imshow(np.log10(W + 1e-4), aspect="auto", origin="lower", cmap="magma")
    ax2.set_xlabel("template (pitch)")
    ax2.set_ylabel("log-frequency bin")
    lab.fig = fig
    lab.note = ("YIN finds one voice's period by a normalized difference function; spectral flux finds where notes begin; "
                "NMF explains a spectrogram with one template per note; and every one of them is only as good as the sound "
                "it was built for.")
    return lab
