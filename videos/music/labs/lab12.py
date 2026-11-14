"""Lab 12: stack fifths and watch the steps, count scale shapes two ways, put the modes in order, find the most even seven notes among nineteen, and name modes by ear."""

import math
from fractions import Fraction

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat, mix
from explainer.music.monochord import scales as S
from explainer.music.monochord.partkit import organ_tone

TITLE = "Scales, derived and counted: fifths, evenness and necklaces"
GOAL = ("Stack a generator and see at which sizes the steps come in two kinds, count the shapes of scale on any number "
        "of notes by Burnside's lemma and by listing them, order the seven modes by brightness, test a scale for the "
        "three properties of the white keys, and tell modes apart by ear.")
TASKS = [
    "Set GENERATOR to 697 (a meantone fifth) and to 709 (a wide one). Which sizes of scale have two kinds of step now? What happened at 12, and why?",
    "Set EDO to 19 and K to 7, then to 12. Is the most even scale deep? Does it have an interval that occurs only once? What are its two step sizes?",
    "Set BEADS to 6, 7 and 8. Compare Burnside's count with the list. For which sizes does some shape map onto itself when turned, and why can it not happen for 7?",
]
GENERATOR = 701.955     # the interval that is stacked, in cents
LIMIT = 31              # stacks of up to this many notes
BEADS = 12              # notes to the octave for the count of shapes
EDO, K = 12, 7          # the most even K notes among EDO equal ones
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    g = GENERATOR / 1200.0

    # 1. Problem 1: five pure fifths from C
    five = S.stack(5, S.FIFTH)
    names = ["C", "G", "D", "A", "E"]
    order = np.argsort((np.arange(5) * S.FIFTH) % 1.0)
    lab.row("five pure fifths from C, folded", " ".join(names[i] for i in order) + ";  steps " + " ".join(f"{x:.0f}" for x in S.gaps(five)) + " cents")
    lab.row("intervals of a semitone or a tritone in that scale", f"{S.interval_vector((0, 2, 4, 7, 9))[0]} and {S.interval_vector((0, 2, 4, 7, 9))[5]}")

    # 2. where the steps come in two sizes (Problem 4)
    two = S.moments(LIMIT, g)
    lab.row(f"a generator of {GENERATOR:g} cents: two sizes of step at", " ".join(str(n) for n in two))
    for n in two[2:6]:
        lab.row(f"   {n} notes", " and ".join(f"{x:.1f}" for x in S.gap_sizes(S.stack(n, g))) + " cents")
    assert all(len(S.gap_sizes(S.stack(n, g))) <= 3 for n in range(2, LIMIT + 1))

    # 3. the modes, in order
    for name, steps in S.by_brightness():
        lab.row(f"{name:<11}", " ".join(str(x) for x in steps) + f"   brightness {S.brightness(steps)}")

    # 4. the white keys' three properties, for the most even K notes of EDO
    notes = S.maximally_even(K, EDO, offset=K - 2 if (EDO, K) == (12, 7) else 0)
    steps = S.steps_of(notes, EDO)
    vec = S.interval_vector(notes, EDO)
    lab.row(f"the most even {K} of {EDO}", " ".join(str(n) for n in notes) + ";  steps " + " ".join(str(s) for s in steps))
    lab.row("how often each interval occurs", " ".join(str(v) for v in vec) + ("   (deep: all different)" if S.is_deep(notes, EDO) else "   (not deep)"))
    lab.row("every kind of interval in exactly two sizes?", "yes" if S.has_myhill(steps) else "no")
    lab.row("its complement", " ".join(str(n) for n in range(EDO) if n not in notes))
    if (EDO, K) == (12, 7):
        assert vec == (2, 5, 4, 3, 6, 1) and notes == (0, 2, 4, 5, 7, 9, 11)

    # 5. every shape (Problem 2)
    divisors = [d for d in range(1, BEADS + 1) if BEADS % d == 0]
    lab.row(f"Burnside, {BEADS} beads", "(" + " + ".join(f"{S.euler_phi(d)}x2^{BEADS // d}" for d in divisors) + f")/{BEADS} = {S.burnside(BEADS)}")
    neck = S.necklaces(BEADS)
    counts = S.classify(BEADS)
    lab.row("listed", f"{len(neck)} shapes; by size " + " ".join(str(counts[k]) for k in range(BEADS + 1)))
    turn = [s for s in neck if s and len({S.rotate(s, k) for k in range(len(s))}) < len(s)]
    lab.row("shapes that map onto themselves when turned", str(len(turn)) + ("" if not turn else ":  " + ";  ".join(" ".join(str(x) for x in s) for s in turn[:8])))
    assert S.burnside(BEADS) == len(neck)

    # 6. the ear problem (Problem 3): eight modes on C
    order = S.by_brightness()
    picks = [int(x) for x in rng.integers(0, 7, 8)]
    c4 = 261.6255653005986
    tone = lambda semis, sec: Clip(organ_tone(c4 * 2 ** (semis / 12.0), sec, partials=5, decay=3.0), SR).fade(0.01, 0.08).at_level(-20.0)        # noqa: E731
    scales = []
    for p in picks:
        ns = list(S.pcs(order[p][1])) + [12]
        placed = [(tone(n, 0.4), 0.3 * k) for k, n in enumerate(ns)] + [(Clip(organ_tone(c4 / 2, 0.3 * len(ns) + 0.4, partials=3), SR).fade(0.2, 0.3).at_level(-30.0), 0.0)]
        scales.append(mix(placed))
    lab.audio = concat(scales, gap=0.8)
    lab.row("ear problem, the eight modes (listen first)", "; ".join(order[p][0] for p in picks))

    fig, (a, b) = labs.figure(2)
    ns = np.arange(2, LIMIT + 1)
    sizes = [len(S.gap_sizes(S.stack(int(n), g))) for n in ns]
    a.bar(ns, sizes, color=[labs.GOLD if s == 2 else "#888" for s in sizes])
    a.set_title(f"Sizes of step in a stack of {GENERATOR:g}-cent fifths")
    a.set_xlabel("notes in the stack")
    a.set_ylabel("different sizes of step")
    a.set_yticks([1, 2, 3])
    b.bar(range(BEADS + 1), [counts[k] for k in range(BEADS + 1)], color=labs.GOLD)
    b.set_title(f"Shapes of scale on {BEADS} notes: {len(neck)} in all")
    b.set_xlabel("notes in the scale")
    b.set_ylabel("shapes")
    lab.fig = fig
    lab.note = ("One interval, stacked, gives scales whose steps come in two sizes at 5, 7 and 12 notes; the seven-note one is "
                "also the most even choice of seven among twelve, and one of only two in which every interval occurs a different "
                "number of times (the other is seven neighbouring semitones). Counting every other possibility shows how unusual that is.")
    return lab
