"""Lab 39: changes, computed: the bebop-scale claim for any chord, chord scales and avoid notes, Coltrane's third
cycle, reharmonisation, and an improviser judged against random lines."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import blues as BL
from explainer.music.monochord import changes as CH
from videos.music.music39 import compute as C

TITLE = "Changes, computed"
GOAL = ("Check the bebop-scale claim for any chord; list chord scales and avoid notes; build Coltrane's cycle in any key; "
        "reharmonise a melody; and judge the improviser against random lines, by ear and by number.")
TASKS = [
    "Change CHORD. Does the bebop scale still land chord tones on every beat? Try a minor seventh: what goes wrong?",
    "Change SEED and CHANGES. How do the improviser's measures move? Which figure would you add first?",
    "Write your own MELODY in C and reharmonise it three ways. Which chords did the program change?",
]
CHORD = "Bb7"
SEED = 0
CHANGES = BL.twelve_bar("F", "jazz")
MELODY = [76, 77, 79, 81, 79, 77, 76, 74, 72]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    claim = CH.bebop_claim(CHORD)
    lab.row(f"bebop scale on {CHORD}", str(claim["bebop_scale"]))
    lab.row("chord tones on every beat? (bebop / mean share for the plain scale)", f"{claim['bebop_all']} / {claim['plain_mean']:.2f}")
    for s in ("Cmaj7", "C7", "Cm7", "Cm7b5"):
        cs = CH.chord_scale(s)
        lab.row(f"{s}: scale, avoid notes", f"{cs['scale']}, {cs['avoid']}")
    lab.row("Coltrane's cycle in F", " ".join(CH.coltrane("F")))
    for scheme in ("diatonic", "secondary", "tritone"):
        lab.row(f"your melody, {scheme}", " ".join(CH.reharmonise(MELODY, scheme)))
    imp = [CH.judge(CH.improvise(CHANGES, seed=SEED + k), CHANGES) for k in range(20)]
    rnd = [CH.judge(CH.random_line(CHANGES, seed=SEED + k), CHANGES) for k in range(20)]
    m = lambda js, k: float(np.mean([j[k] for j in js]))
    assert m(imp, "on_beat_chord_tones") > m(rnd, "on_beat_chord_tones"), "the improviser should beat random lines"
    lab.row("improviser / random: beats on chord tones", f"{m(imp, 'on_beat_chord_tones'):.2f} / {m(rnd, 'on_beat_chord_tones'):.2f}")
    lab.row("improviser / random: guide tones at changes", f"{m(imp, 'guide_at_changes'):.2f} / {m(rnd, 'guide_at_changes'):.2f}")

    # ear problem: four lines over the first four bars, improviser or random, in random order
    bpm = 150
    four = CHANGES[:4]
    kinds, clips = [], []
    for k in range(4):
        who = "improviser" if rng.random() < 0.5 else "random"
        line = CH.improvise(four, seed=100 + k) if who == "improviser" else CH.random_line(four, seed=100 + k)
        parts = []
        C.comp(parts, four, bpm)
        C.line_parts(parts, line, bpm, 0.0, "piano", -1.0)
        clips.append(Clip(mix(parts, duration=4 * 4 * 60 / bpm + 1.0).y, SR).at_level(-20.0))
        kinds.append(who)
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem: improviser or random, in order (listen first)", ", ".join(kinds))

    fig, (ax1, ax2) = labs.figure(2)
    keys = ["on_beat_chord_tones", "guide_at_changes", "in_scale", "steps"]
    x = np.arange(len(keys))
    ax1.bar(x - 0.2, [m(imp, k) for k in keys], 0.4, color=labs.GOLD, label="improviser")
    ax1.bar(x + 0.2, [m(rnd, k) for k in keys], 0.4, color="C0", label="random in scale")
    ax1.set_xticks(x)
    ax1.set_xticklabels(["chord tones\non beats", "guide tones\nat changes", "in scale", "steps"])
    ax1.legend(frameon=False)
    ax1.set_title("the improviser, judged")
    line = CH.improvise(CHANGES, seed=SEED)
    ax2.plot([e for _, e in line], [p for p, _ in line], ".-", color=labs.GOLD, lw=0.8)
    ax2.set_xlabel("eighth note")
    ax2.set_ylabel("key number")
    ax2.set_title("one chorus over the jazz blues in F")
    lab.fig = fig
    lab.note = ("The bebop scale lands chord tones on every beat over any dominant or sixth chord; keys a major third apart "
                "share three notes; and a page of rules beats random scale notes because it aims at the next chord.")
    return lab
