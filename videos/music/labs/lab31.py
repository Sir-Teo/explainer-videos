"""Lab 31: transformations, computed: P, L and R on any triad, the two groups of 24 built and checked, the shortest
walk between any two triads on the Tonnetz, the hexatonic and octatonic systems, the 62 tours, and eight pairs of
triads to name by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import neoriemann as N
from explainer.music.monochord.partkit import organ_tone

TITLE = "Transformations, computed"
GOAL = ("Apply P, L and R to any triad; build the PLR and T/I groups and check that they commute; find the shortest walk "
        "between two triads and its voice leading; and hear the three moves well enough to name them.")
TASKS = [
    "Choose START and END triads. What is the shortest P, L, R word between them, and how many semitones do the voices move?",
    "Change WORD (for example 'PL', 'PR', 'LR'). How long is the cycle it makes from C major, and which pitch classes does it use?",
    "Is the PLR distance from C major a good predictor of voice-leading distance? Plot one against the other for all 23 triads.",
]
START = (0, "M")
END = (6, "M")
WORD = "PL"


def chord(t, seconds=1.0, low=55):
    y = None
    for pc in sorted(N.pcs(t)):
        m = low + ((pc - low) % 12)
        s = organ_tone(440 * 2 ** ((m - 69) / 12), seconds, partials=6, rolloff=0.6, decay=2.0) * 0.25
        y = s if y is None else y + s
    b = organ_tone(440 * 2 ** ((t[0] + 36 - 69) / 12), seconds, partials=6, rolloff=0.6, decay=2.0) * 0.2
    return Clip(y + b, SR).fade(0.01, 0.1)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the moves on a triad
    lab.row(f"P, L, R of {N.name(START)}", ", ".join(N.name(N.OPS[k](START)) for k in "PLR"))

    # 2. the groups
    G, H = N.plr_group(), N.ti_group()
    lab.row("orders of the PLR and T/I groups; do they commute?", f"{len(G)}, {len(H)}; {N.commute(G, H)}")
    assert len(G) == len(H) == 24 and N.commute(G, H)

    # 3. the shortest walk
    w = N.shortest_paths(START)[END]
    lab.row(f"shortest word {N.name(START)} to {N.name(END)}; semitones moved directly",
            f"{w or '(none: the same triad)'}; {N.voice_leading(START, END)}")

    # 4. cycles and systems
    cyc = N.cycle(WORD)
    used = sorted(set().union(*[N.pcs(t) for t in cyc]))
    lab.row(f"the cycle of {WORD} from C: length, pitch classes", f"{len(cyc)}, {used}")
    lab.row("hexatonic and octatonic systems (orbits of PL and PR)", f"{len(N.systems('PL'))} of 6, {len(N.systems('PR'))} of 8")
    lab.row("tours of all 24 triads by P, L and R (Hamiltonian cycles)", str(N.hamiltonian_cycles()))
    lab.row("triads at each distance from C major", str(N.distance_histogram()))

    # 5. Problem 3: eight pairs, each P, L or R
    moves = [str(k) for k in rng.permutation(list("PPPLLLRR"))]
    clips = []
    for k in moves:
        t = N.TRIADS[int(rng.integers(24))]
        clips.append(concat([chord(t), chord(N.OPS[k](t))], gap=0.1))
    lab.audio = concat(clips, gap=1.0)
    lab.row("ear problem: the eight moves in the order played (listen first)", " ".join(moves))

    fig, (a, b) = labs.figure(2)
    d = N.shortest_paths()
    xs = [len(d[t]) for t in N.TRIADS if t != (0, "M")]
    ys = [N.voice_leading((0, "M"), t) for t in N.TRIADS if t != (0, "M")]
    jit = rng.uniform(-0.1, 0.1, len(xs))
    a.plot(np.array(xs) + jit, np.array(ys) + jit[::-1], "o", color=labs.GOLD)
    a.set_xlabel("P, L, R steps from C major")
    a.set_ylabel("semitones of voice leading")
    a.set_title(f"two distances (r = {np.corrcoef(xs, ys)[0, 1]:.2f})")
    h = N.distance_histogram()
    b.bar(list(h), list(h.values()), color=labs.BLUE)
    b.set_xlabel("steps from C major")
    b.set_title("triads at each distance on the Tonnetz")
    lab.fig = fig
    lab.note = ("Each move keeps two notes and is its own inverse; the moves commute with transposition and inversion; "
                "and on the torus no triad is more than five steps from any other.")
    return lab
