"""Lab 34: raga and tala, computed: the tanpura's curved bridge, thaats and melakartas, a tihai solver for any tala,
gamaka contours and their pitch histogram, and phrases to name by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import raga as R

TITLE = "Raga and tala, computed"
GOAL = ("Model a tanpura string with and without its curved bridge; place any scale among the thaats and melakartas; "
        "solve tihais for any tala; and draw the pitch histogram of an ornamented phrase.")
TASKS = [
    "Change CYCLE and START. Which tihais (phrase, gap) land on sam? Which are bedam (no gap)?",
    "Choose a SCALE (seven pitch classes with Sa and Pa). Is it a thaat? Which melakarta is it?",
    "Change the bridge DEPTH. How does the string's brightness in the first half-second change?",
]
CYCLE, START = 10, 6
SCALE = (0, 2, 4, 6, 7, 9, 11)
DEPTH = 0.008


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    sols = R.tihai(CYCLE, START, phrase_lengths=range(1, 7), gaps=range(0, 4))
    lab.row(f"tihais in a {CYCLE}-beat tala from beat {START} (p, g, cycles)", ", ".join(f"({s['p']},{s['g']},{s['cycles']})" for s in sols) or "none")
    for s in sols:
        pos, strokes = START - 1, []
        for _ in range(3):
            strokes += list(range(pos, pos + s["p"]))
            pos += s["p"] + s["g"]
        assert strokes[-1] % CYCLE == 0
    thaat = [k for k, v in R.THAATS.items() if tuple(v) == tuple(SCALE)]
    mela = R.melakarta_number(SCALE) if tuple(SCALE) in R.melakartas() else None
    lab.row(f"scale {SCALE}: thaat; melakarta number", f"{thaat[0] if thaat else '(none)'}; {mela}")
    plain = R.jawari_string(130.0, 1.0, bridge=False)
    jaw = R.jawari_string(130.0, 1.0, bridge=True, depth=DEPTH)
    tp, cp = R.centroid_track(plain)
    tj, cj = R.centroid_track(jaw)
    lab.row("brightness at 0.1 s and 0.3 s: sharp bridge / curved bridge (Hz)",
            f"{np.interp(0.1, tp, cp):.0f}, {np.interp(0.3, tp, cp):.0f} / {np.interp(0.1, tj, cj):.0f}, {np.interp(0.3, tj, cj):.0f}")

    # Problem 3: phrases in Bilawal or Yaman
    kinds, clips = [], []
    for i in range(6):
        name = ["Bilawal", "Yaman"][int(rng.integers(2))]
        r = R.RAGAS[name]
        notes = [(s, 0.32) for s in r["pakad"]]
        c = R.gamaka_contour(notes, glide=0.06)
        clips.append(Clip(R.voice_from_contour(c, 261.6), SR).at_level(-20.0))
        kinds.append(name)
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem: the raga of each phrase, in order (listen first)", ", ".join(kinds))

    fig, (a, b) = labs.figure(2)
    a.plot(tp, cp, label="sharp bridge")
    a.plot(tj, cj, label="curved bridge")
    a.set_xlabel("seconds")
    a.set_ylabel("spectral centroid (Hz)")
    a.legend(frameon=False)
    a.set_title("the jawari's brightness")
    alap = [(0, 1.2), (2, 0.8), (4, 1.2), (5, 0.8), (4, 1.0), (2, 0.8), (0, 1.6)]
    con = R.gamaka_contour(alap, glide=0.3, shake={2: (0.5, 3.0)})
    cents, h = R.pitch_histogram(con)
    b.bar(cents, h, width=10, color=labs.GOLD)
    b.set_xlabel("cents above Sa")
    b.set_title("pitch histogram of an ornamented phrase")
    lab.fig = fig
    lab.note = ("A curved bridge pushes energy into high partials; a tihai is one modular equation; and an ornamented "
                "phrase spends much of its time between the named notes.")
    return lab
