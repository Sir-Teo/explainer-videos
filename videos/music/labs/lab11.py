"""Lab 11: tempo in milliseconds, a metre's weights, syncopation by brute force, twos and threes, swing by subtraction, the telephone game, and bars to tell apart by ear."""

import math
from itertools import combinations

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat, mix
from explainer.music.monochord import rhythm as R
from explainer.music.monochord.instruments import drumkit as K

TITLE = "Rhythm, counted: metres, syncopation and the ratios a listener expects"
GOAL = ("Turn a tempo into milliseconds, weigh the pulses of a bar, find the most syncopated rhythm of five notes by trying "
        "them all, count the metres made of twos and threes, get the swing ratio from one short note, run the telephone "
        "game on random rhythms, and tell 3 + 3 from 2 + 2 + 2 by ear.")
TASKS = [
    "Set NOTES to 3, 4, 6 and 7. How does the largest possible index change? Is the winner always the rhythm with a note on every weakest pulse?",
    "Set SHORT to 0.08 and 0.12. At what tempo is the swing ratio exactly two? What does a drummer with a quicker hand do to the triplet feel?",
    "Set HEARING to 0.02 and 0.1 and run the telephone game. Does a listener who hears timing less exactly end up closer to the whole-number rhythms, or further?",
]
BPM, SIGNATURE = 132.0, (2, 3)     # Problem 1: a jig in six-eight, the beat a dotted quarter
NOTES = 5                          # Problem 4: how many notes in the bar of sixteen pulses
SHORT = 0.1                        # the short note of a swung pair, seconds
HEARING = 0.05                     # how blurred the listener's hearing of a rhythm is (fraction of the cycle)
SR = 48_000
FOUR = (2, 2, 2, 2)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. tempo on a clock (Problem 1)
    beat = 60.0 / BPM
    division = beat / SIGNATURE[1]
    lab.row(f"{BPM:g} beats to the minute, {SIGNATURE[0]} beats of {SIGNATURE[1]}", f"bar {1000 * beat * SIGNATURE[0]:.0f} ms, beat {1000 * beat:.0f} ms, division {1000 * division:.0f} ms")
    lab.row("the tempo at which the division reaches 100 ms", f"{60.0 / (0.1 * SIGNATURE[1]):.0f} beats to the minute")

    # 2. a metre's weights, and a rhythm's index
    lab.row("weights of four-four, in sixteenths", " ".join(str(w) for w in R.meter_weights(FOUR)))
    for name, p in (("every beat", "x...x...x...x..."), ("son clave", "x..x..x...x.x..."), ("bossa nova", "x..x..x...x..x.."), ("every off-beat", "..x...x...x...x.")):
        lab.row(f"syncopation of {name}", f"{p}   {R.syncopation(p, FOUR)}")

    # 3. the most syncopated rhythm of NOTES notes (Problem 4): try them all
    best, best_down = (-1, ""), (-1, "")
    hist = []
    for combo in combinations(range(16), NOTES):
        p = "".join("x" if i in combo else "." for i in range(16))
        s = R.syncopation(p, FOUR)
        hist.append(s)
        best = max(best, (s, p))
        if 0 in combo:
            best_down = max(best_down, (s, p))
    lab.row(f"rhythms of {NOTES} notes on 16 pulses", f"{len(hist)}; index from {min(hist)} to {max(hist)}, typically {np.median(hist):.0f}")
    lab.row("the most syncopated", f"{best[1]}   {best[0]}")
    lab.row("the most syncopated that sounds the downbeat", f"{best_down[1]}   {best_down[0]}")
    assert best[0] >= best_down[0] > R.syncopation("x..x..x...x.x...", FOUR) or NOTES != 5

    # 4. twos and threes (Problem 2)
    counts = [len(R.compositions(n)) for n in range(2, 13)]
    lab.row("ways to fill 2..12 pulses with twos and threes", " ".join(str(c) for c in counts))
    twelve = R.compositions(12)
    lab.row("of the twelve ways to fill 12, those with four beats", str(sum(len(c) == 4 for c in twelve)) + " (3+3+3+3); with five: " + str(sum(len(c) == 5 for c in twelve)) + "; with six: " + str(sum(len(c) == 6 for c in twelve)))
    assert all(counts[k] == counts[k - 2] + counts[k - 3] for k in range(3, len(counts))) and counts[-1] == 12

    # 5. three against two, and swing by subtraction
    p = R.polyrhythm(3, 2)
    lab.row("three against two, on six pulses: the gaps between strokes", " ".join(str(g) for g in p["gaps"]))
    for bpm in (120, 160, 200, 240, 300):
        b = 60.0 / bpm
        lab.row(f"swing ratio at {bpm} if the short note lasts {1000 * SHORT:.0f} ms", f"{max((b - SHORT) / SHORT, 1.0):.2f} to 1")

    # 6. the telephone game
    pk = np.array([R.simplex_point(r) for r in R.INTEGER_RHYTHMS])
    seeds = rng.dirichlet([1, 1, 1], 300)
    seeds = seeds[seeds.min(axis=1) > 0.12]
    weights = np.array([1.0 if set(r) <= {1, 2} else 0.02 for r in R.INTEGER_RHYTHMS])
    it = R.iterate(seeds, pk, weights, 5, seed=seed, hearing=HEARING)
    d = [float(R.nearest_ratio(it[k], pk)[:, 1].mean()) for k in range(6)]
    lab.row("mean distance to the nearest whole-number rhythm, rounds 0..5", " ".join(f"{x:.3f}" for x in d))
    assert d[5] < d[0]

    # 7. the ear problem (Problem 3): eight bars of six, grouped 3 + 3 or 2 + 2 + 2
    kinds = rng.integers(0, 2, 8)
    if kinds.min() == kinds.max():
        kinds[0] = 1 - kinds[0]
    pulse = 0.2
    bars = []
    for k in kinds:
        starts = (0, 2, 4) if k else (0, 3)
        rows = [(Clip(K.woodblock(), SR), i * pulse, -6.0) for i in range(6)] + [(Clip(K.kick(), SR), i * pulse, 0.0) for i in starts]
        bar = mix(rows, duration=6 * pulse)
        bars.append(concat([bar, bar]))
    lab.audio = concat(bars, gap=0.8).at_level(-20.0)
    lab.row("ear problem, the eight bars, each played twice (listen first)", "; ".join("2+2+2" if k else "3+3" for k in kinds))

    fig, (a, b) = labs.figure(2)
    a.hist(hist, bins=np.arange(-0.5, max(hist) + 1.5), color=labs.GOLD)
    a.axvline(R.syncopation("x..x..x...x.x...", FOUR), color=labs.RED, lw=1.2, label="son clave")
    a.set_title(f"Every rhythm of {NOTES} notes on sixteen pulses")
    a.set_xlabel("syncopation index")
    a.set_ylabel("how many rhythms")
    a.legend()
    bpm = np.linspace(100, 330, 100)
    b.plot(bpm, np.clip((60.0 / bpm - SHORT) / SHORT, 1.0, None), color=labs.GOLD, lw=1.6)
    for r in (1, 2, 3):
        b.axhline(r, color="#888", lw=0.5, ls=":")
    b.set_ylim(0.8, 4.2)
    b.set_title(f"Swing ratio, if the short note lasts {1000 * SHORT:.0f} ms")
    b.set_xlabel("tempo (beats to the minute)")
    b.set_ylabel("long : short")
    lab.fig = fig
    lab.note = ("A rhythm is a list of times; a metre is what a listener lays over them. Once the metre is a grid of weights, "
                "syncopation is a sum, the dances of the Balkans are compositions of twos and threes, and swing is one "
                "subtraction. What the grid cannot tell you is where the listener got it.")
    return lab
