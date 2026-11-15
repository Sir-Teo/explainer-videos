"""Lab 62: beat, chords and structure, computed: tempo with a prior, Ellis's beat tracker, chords by templates and by
an HMM, time warping between two timings, and form from repetition, all on sounds whose answers are known."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord.mir import rhythm as RH
from explainer.music.monochord.partkit import organ_tone

TITLE = "Beat, chords and structure, computed"
GOAL = ("Find the tempo of a drum pattern and track its beats, recognize a chord progression frame by frame and with an "
        "HMM, align a strict and a stretched performance by time warping, and find a piece's form from its repetitions.")
TASKS = [
    "Change BPM and PRIOR. When does the tracker report double or half the tempo?",
    "Change SELF (the HMM's chance of staying on a chord). What happens to the chord flicker, and to fast changes?",
    "Change STRETCH (how unevenly the second performance is timed). How large can it get before the alignment fails?",
]
BPM, PRIOR = 96.0, 120.0
SELF = 0.9
STRETCH = 0.25


def drums(seconds, bpm, seed=0):
    rng = np.random.default_rng(seed)
    x = np.zeros(int(seconds * SR))
    beat = 60.0 / bpm
    n = int(0.06 * SR)
    for k in range(int(seconds / beat)):
        g = 1.0 if k % 2 == 0 else 0.7
        burst = rng.standard_normal(n) * np.exp(-np.arange(n) / ((0.03 if k % 2 == 0 else 0.012) * SR)) * g
        i = int(k * beat * SR)
        x[i:i + n] += burst[: len(x) - i]
        j = int((k + 0.5) * beat * SR)
        if j + n // 3 < len(x):
            x[j:j + n // 3] += 0.25 * rng.standard_normal(n // 3) * np.exp(-np.arange(n // 3) / (0.004 * SR))
    return x / np.max(np.abs(x)) * 0.8, np.arange(int(seconds / beat)) * beat


def chords(prog, beat=0.5, times=None):
    out = []
    for k, (r, minor) in enumerate(prog):
        d = beat * 2 if times is None else times[k + 1] - times[k]
        out.append(sum(organ_tone(261.63 * 2 ** (t / 12), d, partials=5) for t in (r, r + (3 if minor else 4), r + 7)))
    y = np.concatenate(out)
    return y / np.max(np.abs(y)) * 0.8


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    x, beats = drums(12.0, BPM, seed)
    nv = RH.novelty(x)
    tp = RH.tempo(nv["nov"], nv["hop_s"], prior_bpm=PRIOR)
    est = RH.track_beats(nv["nov"], nv["hop_s"], tp["bpm"])
    sc = RH.beat_scores(beats, est)
    lab.row(f"drums at {BPM:g}: tempo found (prior {PRIOR:g})", f"{tp['bpm']:.1f}")
    lab.row("beats: F within 70 ms, at any level", f"{sc['f']:.2f}, {sc['any_level']:.2f}")
    assert sc["any_level"] > 0.8
    prog = [(0, False), (9, True), (5, False), (7, False)] * 2
    y = chords(prog)
    C = RH.chroma(y)
    A = np.full((25, 25), (1 - SELF) / 24)
    np.fill_diagonal(A, SELF)
    res = RH.recognize(C["C"], A=A)
    labels = RH.chord_labels()
    n = C["C"].shape[1]
    truth = np.array([(r + (12 if m else 0)) for r, m in prog])[np.minimum((np.arange(n) * C["hop_s"] / 1.0).astype(int), len(prog) - 1)]
    lab.row("chords right, frame by frame and with the HMM", f"{np.mean(res['frame'] == truth):.2f}, {np.mean(res['hmm'] == truth):.2f}")
    assert np.mean(res["hmm"] == truth) >= np.mean(res["frame"] == truth) - 0.05
    times = np.r_[0, np.cumsum(1.0 * (1 + STRETCH * np.sin(np.arange(len(prog)) * 1.3)))]
    y2 = chords(prog, times=times)
    d = RH.dtw(RH.chroma(y, hop=2400)["C"], RH.chroma(y2, hop=2400)["C"])
    hop = 2400 / SR
    pt = d["path"] * hop
    found = [pt[np.abs(pt[:, 0] - k * 1.0) <= hop, 1].mean() for k in range(len(prog))]
    err = np.abs(np.array(found) - times[: len(prog)])
    lab.row("alignment: chord starts placed within (median, worst)", f"{1000 * np.median(err):.0f} ms, {1000 * np.max(err):.0f} ms")
    form = [(0, False), (5, False), (7, False), (0, False)]
    piece = chords(form + [(9, True), (2, True), (7, False), (7, False)] + form)
    S = RH.ssm(RH.chroma(piece, hop=2400)["C"])
    L = int(round(4.0 / hop))
    M = RH.segment_similarity(S, L, 3)
    form_found = RH.labels_from_similarity(M, 0.95)
    lab.row("form from repetition (three four-chord phrases)", " ".join(form_found))
    assert form_found == ["a", "b", "a"]
    # the ear problem: the drums with a click track early, on time or late
    shifts = list(rng.permutation([0, 20, 40, 80]))
    clips = []
    for sft in shifts:
        y3 = x[: int(6 * SR)].copy()
        nclick = int(0.015 * SR)
        burst = np.sin(2 * np.pi * 2500 * np.arange(nclick) / SR) * np.exp(-np.arange(nclick) / (0.003 * SR)) * 0.4
        for b in beats[beats < 5.8]:
            i = int((b + sft / 1000) * SR)
            y3[i:i + nclick] += burst[: len(y3) - i]
        clips.append(Clip(y3, SR))
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: four click tracks; how late is each? (listen first)", ", ".join(f"{s} ms" for s in shifts))
    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(nv["t"], nv["nov"], color=labs.GOLD, lw=0.8)
    for b in est:
        ax1.axvline(b, color="0.5", lw=0.5)
    ax1.set_xlabel("s")
    ax1.set_ylabel("novelty and beats")
    ax2.imshow(S, origin="lower", cmap="magma", aspect="auto")
    ax2.set_xlabel("frame")
    ax2.set_ylabel("frame")
    lab.fig = fig
    lab.note = ("Novelty shows where things begin and autocorrelation how often; a prior picks the tempo's level; dynamic "
                "programming places the beats; chroma and an HMM hear chords in context; time warping aligns timings; "
                "repetition reveals form.")
    return lab
