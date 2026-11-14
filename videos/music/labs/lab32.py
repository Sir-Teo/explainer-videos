"""Lab 32: the geometry of chords, computed: the smallest voice leading between any two chords, evenness and the
nearest transposition, the Möbius strip of two-note chords, Fourier magnitudes, Bach's chorales against the shortest
paths, and pairs of progressions to judge by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import chorales as CH
from explainer.music.monochord import geometry as G
from explainer.music.monochord.partkit import organ_tone

TITLE = "The geometry of chords, computed"
GOAL = ("Find the smallest voice leading between two chords, measure how even a chord is and how cheaply it reaches its "
        "transpositions, read a set's Fourier magnitudes, and test Bach's voice leading against the shortest paths.")
TASKS = [
    "Choose CHORD_A and CHORD_B (pitch classes, same size; fractions allowed). What is the smallest voice leading, and which voice moves where?",
    "Choose CHORD. How far is it from even, and what is its cheapest move to a different transposition of itself?",
    "Change UPPER_ONLY. How much closer to the minimum are Bach's upper three voices than all four?",
]
CHORD_A = (0, 4, 7)
CHORD_B = (5, 9, 0)
CHORD = (0, 4, 7, 10)
UPPER_ONLY = True


def chord_sound(keys, seconds=0.9):
    y = sum(organ_tone(440 * 2 ** ((m - 69) / 12), seconds, partials=6, rolloff=0.6, decay=2.5) * 0.22 for m in keys)
    return Clip(y, SR).fade(0.01, 0.1)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    size, moves = G.vl(CHORD_A, CHORD_B)
    lab.row(f"smallest voice leading {CHORD_A} -> {CHORD_B}", f"{size:g} semitones; moves {[round(m, 2) for m in moves]}")
    lab.row("the same, Euclidean and largest leap", f"{G.vl(CHORD_A, CHORD_B, 'euclid')[0]:.2f}, {G.vl(CHORD_A, CHORD_B, 'max')[0]:g}")

    v, k = G.nearest_transposition(CHORD)
    lab.row(f"{CHORD}: distance from even; cheapest move to a transposition", f"{G.evenness(CHORD):.2f}; {v:g} semitones, to T{k}")
    lab.row(f"{CHORD}: Fourier magnitudes |F1| ... |F6|", " ".join(f"{x:.2f}" for x in G.dft(CHORD)[1:]))
    lab.row("chord types of 3 notes under OP, OPT, OPTI, OPTIC", str({k: v for k, v in G.optic_counts(3).items()}))

    book = CH.load()[:120]
    r = G.bach_voice_leading(book, upper_only=UPPER_ONLY)
    lab.row(f"Bach, 120 chorales ({'upper three voices' if UPPER_ONLY else 'all four'}): minimal share; means actual/min/shuffled",
            f"{r['minimal_share']:.2f}; {r['mean_actual']:.2f} / {r['mean_minimal']:.2f} / {r['mean_shuffled']:.2f}")
    assert all(x == 0 for x in r["excess_hist"][1::2])

    # Problem 3: four pairs of progressions; in each pair one is the minimal voice leading
    pairs = [((60, 64, 67), (60, 65, 69), (65, 69, 72)), ((60, 64, 67), (59, 62, 67), (55, 59, 62)),
             ((60, 63, 67), (60, 65, 68), (65, 68, 72)), ((60, 64, 67), (59, 64, 68), (64, 68, 71))]
    order, clips = [], []
    for a, small, big in pairs:
        first = bool(rng.integers(2))
        order.append("first" if first else "second")
        x, y = (small, big) if first else (big, small)
        clips.append(concat([chord_sound(a), chord_sound(x), chord_sound(a), chord_sound(y)], gap=0.15))
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem: where the minimal voice leading comes in each pair (listen first)", ", ".join(order))

    fig, (a, b) = labs.figure(2)
    pts = [G.dyad_strip(i, j) for i, j in G.dyads()]
    ics = [min((j - i) % 12, (i - j) % 12) for i, j in G.dyads()]
    a.scatter([p[0] for p in pts], [p[1] for p in pts], c=ics, cmap="viridis", s=30)
    a.set_xlabel("centre (glued with a twist at 0 and 6)")
    a.set_ylabel("interval")
    a.set_title("the Möbius strip of two-note chords")
    b.bar(range(0, 8, 2), [r["excess_hist"][k] for k in range(0, 8, 2)], color=labs.GOLD)
    b.set_xlabel("semitones more than the minimum")
    b.set_title("Bach's voice leading against the shortest path")
    lab.fig = fig
    lab.note = ("The smallest voice leading tries every assignment of notes to voices; nearly even chords reach their "
                "transpositions cheaply; and Bach's excess over the minimum is always even.")
    return lab
