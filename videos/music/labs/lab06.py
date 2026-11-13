"""Lab 6: the commas in exact fractions, a temperament of your own, the beats a tuner counts, and a chord to rank by ear."""

import math
from fractions import Fraction

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import tuning as T
from explainer.music.monochord.partkit import organ_chord

TITLE = "Tuning, computed: where each system hides the comma"
GOAL = ("Check the commas in exact arithmetic, temper a chain of fifths by any fraction of the comma and see what it does "
        "to the thirds and to the wolf, count the beats of an equal-tempered third, and pump a comma.")
TASKS = [
    "Set FRACTION to Fraction(0), Fraction(1, 6) and Fraction(1, 3). Which keeps the fifths best? Which makes the minor thirds pure?",
    "Set FRACTION to Fraction(1, 11). Compare the result with twelve equal steps. How wide is the 'wolf' now?",
    "Set ROUNDS to 5. How far has the tonic of the pump fallen, and what note is it nearest to?",
]
FRACTION = Fraction(1, 4)     # how much of the syntonic comma each fifth gives up
ROUNDS = 4                    # times round I-vi-ii-V-I in pure chords
C4 = 261.6255653005986


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the commas, exactly
    assert Fraction(3, 2) ** 12 / 2 ** 7 == T.PYTHAGOREAN_COMMA and Fraction(3, 2) ** 4 / 4 / Fraction(5, 4) == T.SYNTONIC_COMMA
    lab.row("Pythagorean comma", f"{T.PYTHAGOREAN_COMMA} = {T.cents(T.PYTHAGOREAN_COMMA):.2f} cents")
    lab.row("syntonic comma", f"{T.SYNTONIC_COMMA} = {T.cents(T.SYNTONIC_COMMA):.2f} cents")
    lab.row("diesis (octave less three pure thirds)", f"{T.DIESIS} = {T.cents(T.DIESIS):.2f} cents")

    # 2. a temperament of your own
    t = T.meantone(FRACTION)
    fifths, thirds = dict(t.fifths()), dict(t.thirds())
    wolf = fifths["G#"] - T.cents(T.PURE_FIFTH)
    lab.row(f"fifths narrowed by {FRACTION} comma", f"{fifths['C']:.1f} cents each; the twelfth is {wolf:+.1f} cents from pure")
    lab.row("major third on C", f"{thirds['C'] - T.cents(T.PURE_THIRD):+.1f} cents from pure")
    lab.row("worst major third", f"{max(thirds.values()) - T.cents(T.PURE_THIRD):+.1f} cents from pure")
    assert abs(math.fsum(fifths.values()) - 8400.0) < 1e-6          # the twelve fifths always add up to seven octaves
    if FRACTION == Fraction(1, 4):
        assert abs(thirds["C"] - T.cents(T.PURE_THIRD)) < 1e-9 and abs(wolf - 35.68) < 0.01

    # 3. the beats a tuner counts (Problem 1)
    e = T.equal(12)
    f3, a3 = e.hz("F", 3), e.hz("A", 3)
    beat = T.beat_rate(f3, a3, 5, 4)
    lab.row("equal temperament: F3 and A3", f"{f3:.2f} and {a3:.2f} Hz")
    lab.row("their major third beats", f"{beat:.2f} times a second; an octave higher, {2 * beat:.2f}")
    assert abs(beat - 6.93) < 0.01

    # 4. the pump
    drift = T.pump_drift(ROUNDS)
    lab.row(f"{ROUNDS} times round I-vi-ii-V-I in pure chords", f"the tonic is {drift:.1f} cents from where it began")
    assert abs(drift + ROUNDS * T.cents(T.SYNTONIC_COMMA)) < 1e-9

    # 5. the ear problem (Problem 3): the chord of C major in four tunings
    systems = [("pure (just intonation)", T.just()), ("quarter-comma meantone", T.meantone()), ("twelve equal steps", T.equal(12)), ("Pythagorean", T.pythagorean())]
    order = rng.permutation(4)

    def chord(tn):
        return organ_chord([C4 * 2 ** (tn.pc(n) / 1200.0) for n in ("C", "E", "G")], 2.0).at_level(-18.0)

    lab.audio = concat([chord(systems[j][1]) for j in order], gap=0.4)
    lab.row("ear problem, the order (listen first)", "; ".join(systems[j][0] for j in order))
    lab.row("  from stillest to busiest", "; ".join(f"{n} ({tn.triad_error('C'):.1f})" for n, tn in sorted(systems, key=lambda s: s[1].triad_error("C"))))

    fig, (a, b) = labs.figure(2)
    names = [n for n, _ in t.thirds()]
    a.bar(range(12), [thirds[n] - T.cents(T.PURE_THIRD) for n in names], color=labs.RED, label="major third")
    a.bar(range(12), [fifths[n] - T.cents(T.PURE_FIFTH) for n in names], color=labs.BLUE, width=0.4, label="fifth")
    a.set_xticks(range(12))
    a.set_xticklabels(names, fontsize=7)
    a.axhline(0, color="#888", lw=0.6)
    a.set_title(f"Fifths narrowed by {FRACTION} of a comma")
    a.set_ylabel("cents from pure")
    a.legend()
    ns = np.arange(5, 61)
    b.plot(ns, [abs(T.edo_errors(int(n))["fifth_error"]) for n in ns], color=labs.BLUE, lw=1.2, label="best fifth")
    b.plot(ns, [abs(T.edo_errors(int(n))["third_error"]) for n in ns], color=labs.GOLD, lw=1.2, label="best major third")
    for n in (12, 19, 31, 53):
        b.axvline(n, color="#888", lw=0.5, ls=":")
    b.set_title("Equal divisions of the octave")
    b.set_xlabel("steps to the octave")
    b.set_ylabel("cents from pure")
    b.set_ylim(0, 30)
    b.legend()
    lab.fig = fig
    lab.note = ("Temper the fifths and the comma does not go away: it moves. A quarter of a comma from each fifth makes eight thirds "
                "pure and leaves a wolf; an eleventh of a comma from each is, very nearly, twelve equal steps.")
    return lab
