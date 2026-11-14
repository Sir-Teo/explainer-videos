"""Lab 19: chromatic harmony computed: the three diminished sevenths and the keys they open, augmented sixths and
their enharmonic twins, the comma behind the trapdoors, a pathfinder between keys, Lerdahl's tension, the
voice-leading map of the triads, and predominants by ear."""

from fractions import Fraction

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chords as CH
from explainer.music.monochord import chromatic as X
from explainer.music.monochord.partkit import organ_tone

TITLE = "Chromatic harmony, computed"
GOAL = ("Find the keys a diminished seventh can open, check that the German sixth is a dominant seventh in disguise, "
        "measure the comma the trapdoors hide, search for the shortest modulation between keys, score a progression's "
        "tension, map the voice leading between all triads, and name predominants by ear.")
TASKS = [
    "Set START and TARGET to two keys of your own. How many steps with pivot chords only, and with the doors? Which door does the route use?",
    "Write a PROGRESSION of your own as (root, kind, key) triples and read its tension curve. Where does it peak, and why?",
    "Change TONIC. Is the German sixth always the dominant seventh of the key a semitone above the tonic?",
]
TONIC = 0                                            # the key for the augmented sixths (C)
START, TARGET = (0, "major"), (6, "major")           # C major to F sharp major
PROGRESSION = [(0, "major", (0, "major")), (8, "major", (0, "major")), (1, "major", (5, "minor")),
               (7, "7", (0, "major")), (0, "major", (0, "major"))]
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the three diminished sevenths divide the 24 keys among them
    seen = {}
    for root in (11, 0, 1):                                      # B, C, C♯: the three different chords
        d = X.dim7(root)
        keys = [r["key"] for r in X.dim7_resolutions(d)]
        lab.row(f"diminished seventh {'-'.join(X.NAMES[p] for p in d)}", ",  ".join(X.key_name(k) for k in keys))
        for k in keys:
            seen[k] = seen.get(k, 0) + 1
    lab.row("keys reached, and how many times each", f"{len(seen)} keys, each {set(seen.values())} time(s)")
    assert len(seen) == 24 and set(seen.values()) == {1}

    # 2. augmented sixths, and the German sixth as a dominant seventh
    six = X.augmented_sixths(TONIC)
    lab.row(f"augmented sixths in {X.key_name((TONIC, 'minor'))}", ";  ".join(f"{n}: {' '.join(X.NAMES[p] for p in pcs)}" for n, pcs in six.items()))
    ger = set(six["German"])
    dom = set(X.triad((TONIC + 8) % 12, "7"))
    lab.row("German sixth = dominant seventh on the flat sixth degree?", f"{ger == dom}  (resolves to {X.NAMES[(TONIC + 1) % 12]} as a dominant)")

    # 3. the comma behind the doors
    lab.row("four pure minor thirds against the octave (cents)", f"{X.pure_cycle(Fraction(6, 5), 4):+.1f}")
    lab.row("three pure major thirds against the octave (cents)", f"{X.pure_cycle(Fraction(5, 4), 3):+.1f}")
    lab.row("twelve pure fifths against seven octaves (cents)", f"{X.pure_cycle(Fraction(3, 2), 12):+.1f}")

    # 4. the pathfinder
    for chrom in (False, True):
        d = X.distances(START, chrom)
        route = d["routes"][TARGET]
        lab.row(f"{X.key_name(START)} to {X.key_name(TARGET)}, {'with the doors' if chrom else 'pivot chords only'}",
                f"{d['dist'][TARGET]} step(s): " + ";  ".join(f"{X.key_name(a)} > {X.key_name(b)} ({how})" for a, b, how in route))
    cnt = {c: np.bincount(list(X.distances(START, c)["dist"].values()), minlength=3)[1:].tolist() for c in (False, True)}
    lab.row("keys 1 and 2 steps away: pivots / with doors", f"{cnt[False]} / {cnt[True]}")

    # 5. tension
    t = X.tension_curve(PROGRESSION)
    lab.row("tension curve (distance from the chord before)", ",  ".join(str(x) for x in t))
    lab.row("Lerdahl's distances: I-V, I-vi, I-ii", ",  ".join(str(X.chord_distance((0, "major", (0, "major")), (r, k, (0, "major")))) for r, k in ((7, "major"), (9, "minor"), (2, "minor"))))

    # 6. the voice-leading map of the 24 triads, in circle-of-fifths order
    order = []
    for k in range(12):
        r = (7 * k) % 12
        order += [(r, "major"), ((r + 9) % 12, "minor")]
    m = np.array([[X.voice_leading(X.triad(*a), X.triad(*b))["cost"] for b in order] for a in order])
    lab.row("pairs of triads 1, 2, 3 semitones of motion apart", ",  ".join(str(int((m == v).sum() // 2)) for v in (1, 2, 3)))
    hexa = X.hexatonic((0, "major"))
    lab.row("the hexatonic cycle from C", " > ".join(CH.triad_name(x) for x in hexa))

    # 7. Problem 3, for the ear: ten cadences in C minor, the chord before V to be named
    kinds = {"iv6": [(56, 60, 65, 72)], "N6": [(53, 61, 65, 68)], "Italian": [(56, 60, 66, 72)],
             "French": [(56, 62, 66, 72)], "German": [(56, 60, 63, 66)]}
    tonic, dom7 = (48, 55, 63, 72), (43, 59, 65, 74)
    answers, clips = [], []
    for _ in range(10):
        kind = list(kinds)[int(rng.integers(0, len(kinds)))]
        y = np.zeros(int(4.6 * SR))
        for j, ch in enumerate([tonic, kinds[kind][0], dom7, tonic]):
            tone = sum(organ_tone(CH.hz(n), 1.05, partials=6, rolloff=0.7, decay=1.2) for n in ch)
            i = int(j * 1.0 * SR)
            y[i:i + len(tone)] += tone[: len(y) - i]
        clips.append(Clip(y, SR).fade(0.01, 0.2).at_level(-20.0))
        answers.append(kind)
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem, the chord before V in each cadence (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    a.imshow(m, cmap="magma_r")
    a.set_xticks(range(0, 24, 2))
    a.set_xticklabels([CH.triad_name(order[k]) for k in range(0, 24, 2)], rotation=60)
    a.set_yticks(range(0, 24, 2))
    a.set_yticklabels([CH.triad_name(order[k]) for k in range(0, 24, 2)])
    a.set_title("Least voice-leading motion between triads (semitones)")
    b.plot(range(len(t)), t, "o-", color=labs.GOLD)
    b.set_xticks(range(len(t)))
    b.set_xticklabels([f"{X.NAMES[r]}{'m' if k == 'minor' else ('7' if k == '7' else '')}" for r, k, _ in PROGRESSION])
    b.set_ylabel("distance from the chord before")
    b.set_title("Tension curve (Lerdahl's chord distance)")
    lab.fig = fig
    lab.note = ("The three diminished sevenths share out all 24 keys; the German sixth is a dominant seventh spelled "
                "another way; the doors put almost every key one chord from home, but only in equal temperament, "
                "where four minor thirds make an octave; and the triads nearest in motion are often far apart in key.")
    return lab
