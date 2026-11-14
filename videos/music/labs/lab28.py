"""Lab 28: new scales and new rhythms, computed: any pitch-class set's symmetry and Messiaen mode, the chance that a
passage of k pitch classes fits a scale, additive and palindromic rhythms counted, the golden section against its null
model, and eight ostinatos, regular or displaced, sorted by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import modern as MD
from explainer.music.monochord.partkit import organ_tone

TITLE = "New scales and new rhythms, computed"
GOAL = ("Find any scale's symmetries, measure how often a passage would fit a scale by chance, count additive and "
        "palindromic rhythms, test a golden-section claim against a null model, and hear accents displaced.")
TASKS = [
    "Choose a SET of pitch classes. How many transpositions does it have, is it one of Messiaen's modes, and which scales contain it?",
    "Change BARS, TOL and LANDMARKS. How many landmarks does an analyst need before a golden-section 'hit' is likely by chance?",
    "Change PULSES. How fast do the additive rhythms grow, and how fast the palindromes?",
]
SET = (0, 1, 4, 5, 8, 9)
BARS, TOL, LANDMARKS = 88, 1.0, 5
PULSES = 12


def hit(acc: bool, seconds: float = 0.16) -> np.ndarray:
    y = sum(organ_tone(440 * 2 ** ((m - 69) / 12), seconds, partials=5, rolloff=0.6, decay=12.0) for m in (52, 56, 59, 63))
    return y * (0.35 if acc else 0.08)


def ostinato(accents, pulses: int = 32, unit: float = 0.17) -> Clip:
    y = np.zeros(int((pulses * unit + 0.5) * SR))
    for i in range(pulses):
        s = hit(i in accents)
        j = int(i * unit * SR)
        y[j:j + len(s)] += s[: len(y) - j]
    return Clip(y, SR).fade(0.005, 0.1).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a set's symmetry
    lab.row(f"the set {SET}: transpositions, Messiaen mode", f"{MD.transpositions(SET)}, {MD.messiaen_mode(SET)}")
    lab.row("contained in some octatonic / diatonic / whole-tone / pentatonic scale",
            " / ".join(str(MD.fits(SET, s)) for s in (MD.OCTATONIC, MD.DIATONIC, MD.WHOLE_TONE, MD.PENTATONIC)))
    c = MD.census()
    lab.row("shapes up to transposition; symmetric ones", f"{c['classes']}; {c['n_symmetric']}")

    # 2. chance fits
    for name, sc in (("octatonic", MD.OCTATONIC), ("diatonic", MD.DIATONIC)):
        lab.row(f"chance a k-note set fits some {name} scale, k = 3..8",
                ", ".join(f"{MD.chance_fits(k, sc):.3f}" for k in range(3, 9)))

    # 3. rhythms
    lab.row(f"ways to group {PULSES} pulses in 2s and 3s", f"{len(MD.additive(PULSES))}: " + " ".join("+".join(map(str, r)) for r in MD.additive(PULSES)[:6]) + " ...")
    lab.row(f"rhythms of length {PULSES} from durations 1-4; palindromes among them",
            f"{len(MD.compositions(PULSES, (1, 2, 3, 4)))}; {MD.count_palindromes(PULSES)}")

    # 4. the golden section
    lab.row(f"{BARS} bars, within {TOL:g} bar(s), {LANDMARKS} landmarks: chance of a 'golden' hit",
            f"{MD.golden_chance(BARS, TOL, LANDMARKS):.3f} (one landmark: {MD.golden_chance(BARS, TOL, 1):.3f})")
    assert 0.0 <= MD.golden_chance(BARS, TOL, LANDMARKS) <= 1.0

    # 5. Problem 3: eight ostinatos, regular or displaced
    kinds = list(rng.permutation(["regular"] * 4 + ["displaced"] * 4))
    clips = []
    for k in kinds:
        acc = list(range(0, 32, 4)) if k == "regular" else MD.accents(32, 8, rng)
        clips.append(ostinato(set(acc)))
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: the eight ostinatos in the order played (listen first)", ", ".join(kinds))

    fig, (a, b) = labs.figure(2)
    ks = list(range(3, 9))
    for name, sc, col in (("octatonic", MD.OCTATONIC, labs.GOLD), ("diatonic", MD.DIATONIC, labs.BLUE), ("whole-tone", MD.WHOLE_TONE, labs.RED)):
        a.plot(ks, [MD.chance_fits(k, sc) for k in ks], "o-", color=col, label=name)
    a.set_xlabel("pitch classes in the passage")
    a.set_ylabel("share that fit by chance")
    a.legend(frameon=False)
    a.set_title("does a passage 'belong' to a scale?")
    ms = np.arange(1, 21)
    for tol, col in ((1.0, labs.GOLD), (2.0, labs.RED)):
        b.plot(ms, [MD.golden_chance(BARS, tol, int(m)) for m in ms], color=col, label=f"within {tol:g} bar(s)")
    b.set_xlabel("landmarks the analyst may choose")
    b.set_ylabel("chance of a golden hit")
    b.legend(frameon=False)
    b.set_title(f"{BARS} bars, events at random")
    lab.fig = fig
    lab.note = ("Symmetric scales are rare and are all built from a repeated pattern; short passages fit common scales by "
                "chance; and a golden-section claim is only as good as the landmarks fixed before looking.")
    return lab
