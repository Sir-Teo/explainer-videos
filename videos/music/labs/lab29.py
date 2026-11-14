"""Lab 29: twelve tones, computed: any chord's prime form and interval vector, every set class counted two ways, the
hexachord theorem checked, a row's forty-eight forms and matrix, the all-interval rows found by search, combinatorial
partners, and eight lines, some forms of a row and some not, sorted by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import atonal as A
from explainer.music.monochord.partkit import organ_tone

TITLE = "Twelve tones, computed"
GOAL = ("Name any chord by its set class and interval vector, count all the set classes two ways, check the hexachord "
        "theorem, lay out a row's forty-eight forms, find every all-interval row, and hear which lines are forms of a row.")
TASKS = [
    "Choose a CHORD (pitch classes). What is its prime form and interval vector, and does it have a Z-related twin?",
    "Choose a ROW. Are all its 48 forms different? Is it all-interval? Which hexachord does it start with, and is that combinatorial?",
    "Change the lab's ear problem SEED and try again: which cues let you hear a form of the row, and which mislead you?",
]
CHORD = (0, 1, 4, 6)
ROW = (0, 11, 7, 8, 3, 1, 2, 10, 6, 5, 4, 9)
SEED = 0


def tone_line(row, unit: float = 0.28) -> Clip:
    y = np.zeros(int((len(row) * unit + 0.6) * SR))
    for i, pc in enumerate(row):
        seg = organ_tone(440 * 2 ** ((60 + pc - 69) / 12), unit * 1.1, partials=6, rolloff=0.7, decay=3.0) * 0.3
        j = int(i * unit * SR)
        y[j:j + len(seg)] += seg[: len(y) - j]
    return Clip(y, SR).fade(0.01, 0.2).at_level(-20.0)


def run(seed=SEED):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the chord
    pf, iv = A.prime_form(CHORD), A.interval_vector(CHORD)
    twins = [p for pair in A.z_pairs() for p in pair if pf in pair and p != pf]
    lab.row(f"chord {CHORD}: normal order, prime form, interval vector", f"{A.normal_order(CHORD)}, {pf}, {iv}")
    lab.row("its Z-related twin (same interval vector, different class)", str(twins[0]) if twins else "none")

    # 2. counting
    sc = A.set_classes()
    lab.row("set classes by brute force / by Burnside's lemma", f"{len(sc)} / {A.burnside_ti()}")
    h = A.hexachord_theorem()
    lab.row("hexachord theorem: checked, holds, complement in the same class", f"{h['checked']}, {h['holds']}, {h['complement_same_class']}")
    assert h["holds"]

    # 3. the row
    f = A.forms(ROW)
    lab.row(f"row {ROW}: distinct forms, all-interval?", f"{A.distinct_forms(ROW)}, {A.is_all_interval(ROW)}")
    lab.row("first hexachord: prime form, combinatorial under T / I", f"{A.prime_form(ROW[:6])}, {A.combinatorial(ROW[:6])['T']} / {A.combinatorial(ROW[:6])['I']}")
    ai = A.all_interval_rows()
    lab.row("all-interval rows starting on 0; first and last a tritone apart", f"{len(ai)}; {sum((r[-1] - r[0]) % 12 == 6 for r in ai)}")

    # 4. Problem 3: eight lines, four of them forms
    names = list(f)
    lines, truth = [], []
    for k in range(8):
        if k % 2 == 0:
            name = names[int(rng.integers(len(names)))]
            lines.append(f[name])
            truth.append(name)
        else:
            r = list(ROW)
            i, j = sorted(rng.choice(12, 2, replace=False))
            r[i], r[j] = r[j], r[i]
            lines.append(r)
            truth.append("not a form")
    order = rng.permutation(8)
    lab.audio = concat([tone_line(ROW)] + [tone_line(lines[k]) for k in order], gap=0.8)
    lab.row("ear problem: the row, then eight lines (listen first)", ", ".join(truth[k] for k in order))

    fig, (a, b) = labs.figure(2)
    m = np.array(A.matrix(ROW))
    a.imshow(m, cmap="twilight")
    for r in range(12):
        for c in range(12):
            a.text(c, r, str(m[r, c]), ha="center", va="center", fontsize=6, color="white")
    a.set_title("the row's matrix: P across, I down")
    a.set_xticks([])
    a.set_yticks([])
    sizes = [sum(1 for p in sc if len(p) == k) for k in range(13)]
    b.bar(range(13), sizes, color=labs.GOLD)
    b.set_xlabel("notes in the set")
    b.set_ylabel("set classes")
    b.set_title("224 set classes")
    lab.fig = fig
    lab.note = ("Set classes, interval vectors and rows are exact objects that a program can enumerate and check; whether a "
                "listener follows them is a separate, empirical question.")
    return lab
