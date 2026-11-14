"""Lab 13: name intervals, prove that thirds are what is left, find roots, space a chord, and name triads by ear."""

from itertools import combinations

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chords as C
from explainer.music.monochord.partkit import organ_tone
from explainer.music.monochord.score import Pitch

TITLE = "Chords, named, rooted and spaced"
GOAL = ("Name written intervals and place them on the line of fifths, list every shape of three notes and see which "
        "have no two notes adjacent, run the root model on any chord with extra weight on the bass, find the smoothest "
        "spacing of a chord over a given bass note, and tell the four triads apart by ear, in any inversion.")
TASKS = [
    "Set BASS_WEIGHT to 1.5, 2 and 3. At what weight does the model call A C E G (with A lowest) an A chord? What does it then say about C E G with E lowest, and is that what a musician would say?",
    "Set LOW to 31 (the G an octave lower) and then to 55. How does the smoothest spacing of the seventh chord change? Which interval is at the bottom each time?",
    "Change CHORD to [0, 3, 6, 9] and then to [0, 4, 8]. How many notes tie for the root? Why do the ties come in fours for the first chord and in threes for the second?",
]
P = Pitch.parse
INTERVALS = [("D4", "F#4"), ("E4", "C5"), ("B3", "F4"), ("Ab3", "F#4")]      # Problem 1
CHORD = [9, 0, 4, 7]            # pitch classes, the lowest first: A, C, E, G
BASS_WEIGHT = 1.0               # how many times the lowest note's votes count
SEVENTH = [7, 11, 2, 5]         # G, B, D, F
LOW, VOICES = 43, 5             # the bass note (MIDI) and the number of voices
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Problem 1: intervals, their inversions, and the line of fifths
    for a, b in INTERVALS:
        iv = C.interval(P(a), P(b))
        lab.row(f"{a[:-1]} up to {b[:-1]}", f"{iv.name} ({iv.semitones} semitones);  inversion: {iv.invert().name};  {abs(iv.line)} step{'s' if abs(iv.line) != 1 else ''} "
                                          f"{'sharpward' if iv.line > 0 else 'flatward'} on the line of fifths")
        assert iv.number + iv.invert().number == 9 and iv.quality == C.quality_of(C.fifths(P(b)) - C.fifths(P(a)))

    # 2. Problem 2: every shape of three notes; those with no step smaller than a minor third
    shapes = set()
    for trio in combinations(range(12), 3):
        steps = (trio[1] - trio[0], trio[2] - trio[1], 12 - trio[2] + trio[0])
        shapes.add(min(steps[i:] + steps[:i] for i in range(3)))
    wide = sorted(s for s in shapes if min(s) >= 3)
    names = {(3, 3, 6): "diminished", (3, 4, 5): "minor", (3, 5, 4): "major", (4, 4, 4): "augmented"}
    lab.row("shapes of three notes on twelve", str(len(shapes)))
    lab.row("with every step at least a minor third", ";  ".join(f"{' '.join(map(str, s))} ({names[s]})" for s in wide))
    assert len(shapes) == 19 and set(wide) == set(names)
    # the proof in one line: three steps of at least 3 that add to 12 are 3+3+6, 3+4+5 (two orders) or 4+4+4

    # 3. the root model, with a heavier bass (the research problem)
    w = [BASS_WEIGHT] + [1.0] * (len(CHORD) - 1)
    r = C.root(CHORD, w)
    sal = np.array(r["saliences"])
    lab.row("chord (lowest note first)", " ".join(C.pitch_label(p) for p in CHORD) + f";  bass counted {BASS_WEIGHT:g} times")
    lab.row("votes", "  ".join(f"{C.pitch_label(k)} {sal[k]:g}" for k in np.argsort(-sal)[:4]))
    lab.row("root, and ambiguity", (" = ".join(C.pitch_label(t) for t in r["tied"]) if len(r["tied"]) > 1 else C.pitch_label(r["root"])) + f";  {r['ambiguity']:.2f}")
    named = C.identify([48 + CHORD[0] + (p - CHORD[0]) % 12 for p in CHORD])
    lab.row("names it can have", ";  ".join(C.symbol(C.pitch_label(x["root"]).replace("♭", "b").replace("♯", "#"), x["kind"]) + f" (inversion {x['inversion']})" for x in named) or "none in the vocabulary")
    for name, pcs in (("C E G", [0, 4, 7]), ("C E♭ G", [0, 3, 7]), ("B D F", [11, 2, 5]), ("C E G♯", [0, 4, 8])):
        q = C.root(pcs)
        lab.row(f"   {name}", f"root {' = '.join(C.pitch_label(t) for t in q['tied'])};  ambiguity {q['ambiguity']:.2f}")
    assert abs(C.root([0, 4, 7])["ambiguity"] - 1.8708) < 1e-3

    # 4. Problem 4: the smoothest spacing of a seventh chord over a bass note
    vs = [v for v in C.voicings(SEVENTH, LOW, LOW + 36, voices=VOICES, bass=SEVENTH[0], max_gap=16) if v[0] == LOW]
    ranked = sorted(vs, key=C.spacing_roughness)
    show = lambda v: " ".join(Pitch.from_midi(m).name for m in v)       # noqa: E731
    doubled = lambda v: [C.pitch_label(p) for p in set(m % 12 for m in v) if sum(1 for m in v if m % 12 == p) > 1]       # noqa: E731
    lab.row(f"{len(vs)} spacings in {VOICES} voices; the smoothest", f"{show(ranked[0])}   roughness {C.spacing_roughness(ranked[0]):.2f};  doubles {', '.join(doubled(ranked[0]))}")
    lab.row("the roughest", f"{show(ranked[-1])}   roughness {C.spacing_roughness(ranked[-1]):.2f}")
    no5 = [v for v in C.voicings([SEVENTH[0], SEVENTH[1], SEVENTH[3]], LOW, LOW + 36, voices=VOICES - 1, bass=SEVENTH[0], max_gap=16) if v[0] == LOW]
    best5 = min(no5, key=C.spacing_roughness)
    lab.row(f"without its fifth, in {VOICES - 1} voices", f"{show(best5)}   roughness {C.spacing_roughness(best5):.2f};  doubles {', '.join(doubled(best5)) or 'nothing'}")
    lab.row("low limits by the model (as smooth as a major third on C3)", ";  ".join(
        f"{nm} {Pitch.from_midi(C.low_limit(s, reference=C.spacing_roughness([48, 52]))).name}" for nm, s in (("minor third", 3), ("fifth", 7), ("octave", 12))))

    # 5. Problem 3, for the ear: ten triads, any kind, any inversion
    kinds = ["major", "minor", "diminished", "augmented"]
    answers, clips = [], []
    for _ in range(10):
        k, inv, root = kinds[int(rng.integers(0, 4))], int(rng.integers(0, 3)), int(rng.integers(55, 66))
        v = [p.midi for p in C.invert(C.spell(Pitch.from_midi(root), k), inv)]
        y = sum(organ_tone(C.hz(m), 1.6, partials=6, rolloff=0.7, decay=1.2) for m in v)
        clips.append(Clip(y, SR).fade(0.01, 0.2).at_level(-20.0))
        answers.append(f"{k}, {('root', 'third', 'fifth')[inv]} in the bass")
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem, the ten triads (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    keys = np.arange(24, 85)
    for s, nm in ((3, "minor third"), (4, "major third"), (7, "fifth"), (12, "octave")):
        a.plot(keys, C.dyad_by_register(s, keys), label=nm)
    a.axhline(C.spacing_roughness([48, 52]), color="#888", ls="--", lw=1)
    a.set_title("An interval's roughness, by where its lower note is")
    a.set_xlabel("the lower note (MIDI key; 60 is middle C)")
    a.set_ylabel("roughness (Part 5's model)")
    a.legend(frameon=False)
    b.bar(range(12), sal, color=[labs.GOLD if abs(x - sal.max()) < 1e-9 else "#888" for x in sal])
    b.set_xticks(range(12))
    b.set_xticklabels([C.pitch_label(k) for k in range(12)])
    b.set_title("Votes for each note as the root of " + " ".join(C.pitch_label(p) for p in CHORD))
    b.set_ylabel("votes")
    lab.fig = fig
    lab.note = ("Three notes with no two adjacent are a triad, and nothing else; a root is the note the others could be harmonics of; "
                "and the same chord is clear or muddy according to where its notes are put. The root model cannot choose between "
                "A minor seventh and C with a sixth until the bass is given more weight, which is what a musician does.")
    return lab
