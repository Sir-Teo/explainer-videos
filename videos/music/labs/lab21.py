"""Lab 21: form computed: self-similarity matrices and novelty curves for plans of your own, boundaries scored,
repetition in a tune against shuffled tunes, the golden section's base rate, and forms named by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chords as CH
from explainer.music.monochord import form as FM
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import organ_tone

TITLE = "Form, measured"
GOAL = ("Build pieces from a plan of sections, see their self-similarity matrices and novelty curves, score the "
        "boundaries a program finds, measure how much a tune repeats itself, test the golden section against chance, "
        "and name forms by ear.")
TASKS = [
    "Write a PLAN of your own from the letters A, B and C (for example A B A C A B A). Which boundaries does the novelty curve find, and which does it miss?",
    "Change WIDTH, the checkerboard's half-width in beats, from 2 to 16. At which width are the section boundaries found best, and why?",
    "Choose a TUNE from Part 14's corpus. How much of it repeats? Is it more or less repetitive than the average?",
]
PLAN = "A A B A C A"
WIDTH = 6
TUNE = "Frère Jacques"
SR = 48_000
CHORDS = {"A": [(60, 64, 67), (65, 69, 72), (67, 71, 74), (60, 64, 67)],      # C F G C
          "B": [(67, 71, 74), (62, 66, 69), (67, 71, 74), (62, 66, 69)],      # G D G D
          "C": [(57, 60, 64), (62, 65, 69), (64, 68, 71), (57, 60, 64)]}      # Am Dm E Am


def plan_notes(plan, beats_per_chord=2):
    ev, t, starts = [], 0.0, []
    for x in plan.split():
        starts.append(t)
        for ch in CHORDS[x]:
            for p in ch:
                ev.append((p, t, float(beats_per_chord)))
            t += beats_per_chord
    return ev, starts, t


def render(ev, beat=0.18):
    T = max(a + d for _, a, d in ev)
    y = np.zeros(int((T * beat + 0.6) * SR))
    for p, a, d in ev:
        tone = organ_tone(CH.hz(p), d * beat, partials=5, rolloff=0.7, decay=1.0)
        i = int(a * beat * SR)
        y[i:i + len(tone)] += tone[: len(y) - i] * 0.3
    return Clip(y, SR).fade(0.01, 0.2).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a plan: its picture, its novelty, its boundaries
    ev, starts, total = plan_notes(PLAN)
    S = FM.ssm(FM.chroma_notes(ev, step=1.0))
    assert np.allclose(S, S.T) and np.allclose(np.diag(S), 1.0)
    nov = FM.novelty(S, L=WIDTH)
    found = FM.peaks(nov, min_gap=max(2, WIDTH), threshold=0.2)
    names = PLAN.split()
    truth = [int(starts[i]) for i in range(1, len(names)) if names[i] != names[i - 1]]
    sc = FM.boundary_score(found, truth, tol=2)
    lab.row(f"plan {PLAN}: section starts (beats)", ", ".join(str(int(s)) for s in starts))
    lab.row("where the material changes / where novelty peaks", f"{truth} / {found}")
    lab.row("boundaries found: precision, recall, F", f"{sc['precision']:.2f}, {sc['recall']:.2f}, {sc['f']:.2f}")
    lab.row("the labels the picture gives the sections", " ".join(FM.label_sections(S, [int(s) for s in starts[1:]])))

    # 2. repetition in a tune, against shuffled versions of it
    m = [x for x in M.corpus() if x.name == TUNE][0]
    share = FM.repeated_share(m.pitches, m.beats)
    shuf = FM.shuffled_share(m.pitches, m.beats, trials=200)
    allshare = np.mean([FM.repeated_share(x.pitches, x.beats) for x in M.corpus()])
    lab.row(f"{TUNE}: notes in a repeated four-note figure", f"{share:.2f} (shuffled {shuf:.2f}; corpus average {allshare:.2f})")
    lab.row(f"{TUNE}: its phrases in letters", FM.form_letters(m))

    # 3. the golden section against chance
    sim = rng.uniform(0.5, 0.75, size=100_000)
    rate = float(np.mean(np.abs(sim - FM.PHI) <= 0.02))
    lab.row("chance of a 'golden' division (larger part uniform on 0.5 to 0.75, within 0.02)", f"{rate:.3f} (formula {FM.golden_base_rate():.3f})")
    assert abs(rate - FM.golden_base_rate()) < 0.01

    # 4. Problem 3, for the ear: six short forms
    plans = ["A A B B", "A B A", "A B A C A", "A A B A", "A A B B", "A B A C A"]
    order = rng.permutation(len(plans))
    clips, answers = [], []
    for k in order:
        e, _, _ = plan_notes(plans[k], beats_per_chord=1)
        clips.append(render(e))
        answers.append(plans[k])
    lab.audio = concat(clips, gap=1.2)
    lab.row("ear problem, the six plans in the order played (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    a.imshow(S, cmap="magma", origin="upper")
    for s in starts[1:]:
        a.axhline(s - 0.5, color="w", lw=0.5)
        a.axvline(s - 0.5, color="w", lw=0.5)
    a.set_title(f"Self-similarity of {PLAN}")
    a.set_xlabel("beat")
    a.set_ylabel("beat")
    b.plot(nov, color=labs.GOLD)
    for t in truth:
        b.axvline(t, color="#888", ls="--")
    b.plot(found, [nov[i] for i in found], "o", color="#d66")
    b.set_title(f"Novelty (checkerboard {WIDTH} beats on a side)")
    b.set_xlabel("beat")
    lab.fig = fig
    lab.note = ("A self-similarity matrix shows returns as stripes and sections as blocks; its novelty curve peaks where "
                "the material changes, at a scale set by the checkerboard's width, and cannot see a seam between a "
                "passage and its own repeat; tunes repeat themselves far beyond chance; and a golden division turns up "
                "about one time in six by accident.")
    return lab
