"""Lab 35: maqam, computed: ajnas and maqamat in cents, medieval ratios against 24 and 53 equal steps, Safi al-Din's
seventeen tones, Turkish Rast in commas, and phrases to name by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import maqam as Q

TITLE = "Maqam, computed"
GOAL = ("Build maqamat from ajnas in cents; measure how well equal divisions approximate neutral and just intervals; "
        "compare Arabic and Turkish Rast; and hear the difference a three-quarter tone makes.")
TASKS = [
    "Choose MAQAM. List its notes in cents, and the nearest steps of 24 and of 53 equal divisions for each.",
    "Change N, the number of equal steps. Which N under 80 fits both 27/22 and 5/4 within 5 cents?",
    "Define a new jins in AJNAS (four notes within a fourth) and build a maqam from it. Does it close at the octave?",
]
MAQAM = "Saba"
N = 24


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    sc = Q.maqam_scale(MAQAM)
    lab.row(f"{MAQAM}: notes in cents", ", ".join(f"{c:.0f}" for c in sc))
    lab.row(f"{MAQAM}: nearest steps of {N} and errors", ", ".join(f"{Q.edo_error(c, N)[0]} ({Q.edo_error(c, N)[1]:+.0f})" for c in sc))
    lab.row(f"{MAQAM}: nearest steps of 53 and errors", ", ".join(f"{Q.edo_error(c, 53)[0]} ({Q.edo_error(c, 53)[1]:+.1f})" for c in sc))
    good = [n for n in range(5, 80) if abs(Q.edo_error(1200 * np.log2(27 / 22), n)[1]) < 5 and abs(Q.edo_error(1200 * np.log2(5 / 4), n)[1]) < 5]
    lab.row("divisions under 80 fitting 27/22 and 5/4 within 5 cents", str(good))
    tr = Q.turkish_rast()
    lab.row("Turkish Rast in commas; segah in cents", f"{tr['commas']}; {tr['cents'][2]:.1f}")
    lab.row("Safi al-Din's 17 notes (cents)", ", ".join(f"{c:.0f}" for c in Q.safi_17()))
    assert len(Q.safi_17()) == 17

    # Problem 3: phrases in Rast, Bayati or Hijaz on D
    names, clips = [], []
    for i in range(6):
        name = ["Rast", "Bayati", "Hijaz"][int(rng.integers(3))]
        s_ = Q.maqam_scale(name)
        seq = [s_[k] for k in (0, 1, 2, 3, 4, 3, 2, 1, 0)]
        parts = [(Clip(Q.oud(293.66 * 2 ** (c / 1200), 0.7), SR), j * 0.3, 0.0) for j, c in enumerate(seq)]
        clips.append(Clip(mix(parts, duration=len(seq) * 0.3 + 0.8).y, SR).at_level(-20.0))
        names.append(name)
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem: the maqam of each phrase, in order (listen first)", ", ".join(names))

    fig, (a, b) = labs.figure(2)
    for i, k in enumerate(["Rast", "Bayati", "Hijaz", "Saba", "Nahawand", "Kurd", "Ajam"]):
        s_ = Q.maqam_scale(k)
        a.scatter(s_, [i] * len(s_), s=40)
    a.set_yticks(range(7))
    a.set_yticklabels(["Rast", "Bayati", "Hijaz", "Saba", "Nahawand", "Kurd", "Ajam"])
    a.set_xticks(range(0, 1300, 100))
    a.grid(axis="x", alpha=0.3)
    a.set_xlabel("cents above the tonic")
    a.set_title("seven maqamat; grid lines at the piano's keys")
    ns = list(range(5, 80))
    b.plot(ns, [abs(Q.edo_error(1200 * np.log2(27 / 22), n)[1]) for n in ns], label="27/22 (neutral third)")
    b.plot(ns, [abs(Q.edo_error(1200 * np.log2(5 / 4), n)[1]) for n in ns], label="5/4 (just third)")
    b.set_xlabel("equal divisions of the octave")
    b.set_ylabel("error, cents")
    b.legend(frameon=False)
    b.set_title("which grids fit which thirds")
    lab.fig = fig
    lab.note = ("Neutral steps sit between the piano's keys; 24 equal steps fits them, 53 fits the just intervals, and the "
                "smallest division fitting both the neutral third 27/22 and the just third 5/4 within five cents is 34.")
    return lab
