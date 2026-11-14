"""Lab 14: count what tunes do, shuffle them and count again, prove the leap rule for a die, and train a model that is surprised."""

from fractions import Fraction

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import organ_tone

TITLE = "Melody, counted: steps, leaps, chance and surprise"
GOAL = ("Describe a tune by its moves, range and phrase shapes; test the rule that leaps turn back against shuffled notes "
        "and against a die; train a model of the next note on every tune but one and read that tune's surprise; and tell "
        "real, shuffled and made-up melodies apart by ear.")
TASKS = [
    "Set SKIP to 5 (a fourth or more) and to 7. Does the gap between real and shuffled tunes grow or shrink? Why would larger leaps land further from the middle?",
    "Set LEFT_OUT to 'Frère Jacques', then to 'Greensleeves'. Which note surprises the model most in each, and why is the second tune so much harder for it?",
    "Set ORDER to 0, 1, 2 and 3. Where is the cross-entropy lowest? Remove half of the corpus (CORPUS = CORPUS[::2] in run) and look again.",
]
TUNE = "Happy Birthday to You"      # Problem 1
SKIP = 3                            # a leap is this many semitones or more
SIDES = 6                           # Problem 2: a die of this many sides
LEFT_OUT = "Frère Jacques"          # Problem 4
ORDER = 2
SR = 48_000
NAMES = {-12: "C,", -10: "D,", -8: "E,", -7: "F,", -5: "G,", -3: "A,", -1: "B,", 0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B", 12: "C'", 14: "D'", 16: "E'", 17: "F'"}


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    corpus = M.corpus()
    by = {m.name: m for m in corpus}

    # 1. Problem 1: one tune, described
    m = by[TUNE]
    two = M.Melody(m.name, m.pitches[:m.phrase_ends[1]], m.beats[:m.phrase_ends[1]], m.phrase_ends[:2])
    iv = M.intervals(two)
    lab.row(f"{TUNE}, two phrases, in degrees", " ".join(str(d) for d in two.degrees()))
    lab.row("its moves, in semitones", " ".join(f"{i:+d}" for i in iv))
    lab.row("steps, repeats, leaps", f"{sum(1 <= abs(i) <= 2 for i in iv)}, {sum(i == 0 for i in iv)}, {sum(abs(i) >= 3 for i in iv)} of {len(iv)};  range {M.span(two)} semitones")
    lab.row("the shape of each phrase", "; ".join(M.contour_shape(p) for p in two.phrases))

    # 2. the whole corpus
    s = M.shares(corpus)
    lab.row(f"{len(corpus)} tunes, {sum(len(t) for t in corpus)} notes", f"steps {100 * s['step']:.0f}%, repeats {100 * s['repeat']:.0f}%, leaps {100 * s['leap']:.0f}%;  mean move {s['mean_size']:.2f} semitones")
    lab.row("median range; phrases that are arches", f"{np.median([M.span(t) for t in corpus]):.0f} semitones;  "
            f"{sum(M.contour_shape(p) == 'arch' for t in corpus for p in t.phrases)} of {sum(len(t.phrases) for t in corpus)}")

    # 3. the leap rule against chance
    real = M.post_skip(corpus, SKIP)
    chance = [M.post_skip(M.shuffled(corpus, k), SKIP) for k in range(100)]
    for kind in ("all", "departing", "approaching", "crossing"):
        lab.row(f"leaps of {SKIP}+ semitones that turn back: {kind}", f"tunes {100 * real[kind]['share']:.0f}%  ({real[kind]['n']} leaps);  shuffled {100 * np.mean([c[kind]['share'] for c in chance]):.0f}%")
    assert real["all"]["share"] < np.mean([c["all"]["share"] for c in chance])

    # 4. Problem 2: a die, exactly
    up = [(a, b, c) for a in range(1, SIDES + 1) for b in range(1, SIDES + 1) for c in range(1, SIDES + 1) if b - a >= 2]
    fall, rise = sum(c < b for _, b, c in up), sum(c > b for _, b, c in up)
    lab.row(f"a die of {SIDES} sides: after a rise of 2 or more", f"{len(up)} cases; the next roll is lower in {fall}, higher in {rise}:  {Fraction(fall, fall + rise)} = {100 * fall / (fall + rise):.0f}% turn back")
    by_landing = {k: Fraction(k - 1, SIDES - 1) for k in range(3, SIDES + 1)}
    lab.row("   by where the leap lands (k): (k-1)/(n-1) of moves go down", ",  ".join(f"{k}: {v}" for k, v in by_landing.items()))

    # 5. Problem 4: a model trained on every tune but one
    others = [t for t in corpus if t.name != LEFT_OUT]
    model = M.NGram(ORDER).fit(others)
    target = by[LEFT_OUT]
    bits = model.surprise(target)
    k = int(np.argmax(bits[1:])) + 1
    lab.row(f"{LEFT_OUT}: bits a note (order {ORDER})", f"{bits.mean():.2f};  most surprising: note {k + 1}, {NAMES.get(target.pitches[k], target.pitches[k])} after "
            f"{' '.join(NAMES.get(p, str(p)) for p in target.pitches[max(k - 2, 0):k])}  ({bits[k]:.1f} bits)")
    lab.row("cross-entropy, each tune predicted from the rest", ";  ".join(f"order {o}: {M.cross_entropy(corpus, o):.2f}" for o in range(4)) + " bits a note")

    # 6. Problem 3, for the ear: real, shuffled and made-up melodies
    full = M.NGram(2).fit(corpus)
    kinds, clips = [], []
    c4 = 261.6255653005986
    for _ in range(8):
        kind = ("real", "shuffled", "model")[int(rng.integers(0, 3))]
        src = corpus[int(rng.integers(0, len(corpus)))]
        n = min(src.phrase_ends[1], 16)
        if kind == "real":
            p, b = src.pitches[:n], src.beats[:n]
        elif kind == "shuffled":
            idx = rng.permutation(n)
            p, b = [src.pitches[i] for i in idx], [src.beats[i] for i in idx]
        else:
            p, b = full.generate(n, start=(0,), seed=int(rng.integers(0, 10_000))), src.beats[:n]
        y, t = np.zeros(int((sum(b) * 0.36 + 1.0) * SR)), 0.0
        for pitch, beats in zip(p, b):
            tone = organ_tone(c4 * 2 ** (pitch / 12), beats * 0.36 + 0.25, partials=5, decay=4.0)
            i = int(t * SR)
            y[i:i + len(tone)] += tone[: len(y) - i]
            t += beats * 0.36
        clips.append(Clip(y, SR).fade(0.01, 0.1).at_level(-20.0))
        kinds.append(f"{kind} ({src.name})" if kind != "model" else "made up by the model")
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem, the eight melodies (listen first)", ";  ".join(kinds))

    fig, (a, b) = labs.figure(2)
    hist = M.interval_histogram(corpus)
    a.bar(list(hist), list(hist.values()), color=[labs.GOLD if 1 <= abs(i) <= 2 else "#888" for i in hist])
    a.set_title("Every move in the corpus")
    a.set_xlabel("semitones from one note to the next")
    a.set_ylabel("how often")
    b.bar(range(len(bits)), bits, color=[labs.GOLD if i == k else "#888" for i in range(len(bits))])
    b.set_title(f"Surprise, note by note: {LEFT_OUT}")
    b.set_xlabel("note")
    b.set_ylabel("bits")
    lab.fig = fig
    lab.note = ("Leaps turn back more often in shuffled tunes than in real ones: the rule is regression to the mean, which a die "
                "shows exactly. What chance does not produce is repetition, tendency tones and phrase endings; and a model that only "
                "counts what follows what is already surprised where a listener is.")
    return lab
