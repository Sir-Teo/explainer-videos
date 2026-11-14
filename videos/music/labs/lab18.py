"""Lab 18: the syntax of harmony measured on Bach's chorales, a partimento bass realized by the rule of the octave,
galant schemata found (or not) by a detector, and root motion by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import chords as CH
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import progression as P
from explainer.music.monochord.partkit import organ_tone

TITLE = "Progressions, counted"
GOAL = ("Measure the order of harmonic functions and the motion of roots in Bach's chorales, see how predictable the "
        "next chord is, realize an unfigured bass by the rule of the octave, search for galant schemata, and hear root "
        "motion.")
TASKS = [
    "Set BASS to a bass of your own in C major (key numbers from 40 to 60). Where does the realizer use the rule, and where a plain triad? Does it make parallels?",
    "Set ALPHA to 0.01 and to 1.0. How does the smoothing change the bits per chord of the models of pairs and triples, and why does the triple model suffer most?",
    "Add a schema of your own to SCHEMATA (bass and melody degrees in semitones) and count it in the chorales and in shuffled ones.",
]
BASS = [48, 52, 53, 55, 57, 55, 53, 50, 55, 48]     # C E F G A G F D G C, unfigured
ALPHA = 0.1                                          # add-alpha smoothing of the chord models
SCHEMATA = dict(P.SCHEMATA)
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    book = BC.load()

    # 1. functions and root motion
    f = P.function_transitions(book, "major")
    lab.row("major chorales: T>S, S>D, D>T  /  S>T, D>S, T>D", f"{f['TS']}, {f['SD']}, {f['DT']}  /  {f['ST']}, {f['DS']}, {f['TD']}")
    m = P.root_motions(book, "major")
    tot = sum(m.values())
    lab.row("root motion (in a hundred)", ",  ".join(f"{k} {100 * v / tot:.0f}" for k, v in m.most_common()))
    assert m.most_common(1)[0][0] == "fifth down"

    # 2. how predictable
    train, test = BC.split(book, offset=2)
    p = P.predictability(train, test, "major", alpha=ALPHA)
    lab.row("bits per chord: uniform, frequencies, pairs, triples", f"{p['uniform']:.2f}, {p['n1']:.2f}, {p['n2']:.2f}, {p['n3']:.2f}")
    lab.row("the same chords shuffled: pairs, triples", f"{p['n2_shuffled']:.2f}, {p['n3_shuffled']:.2f}")

    # 3. a partimento: the bass realized by the rule of the octave
    real = P.realize_bass(BASS)
    lab.row("the bass, realized", "  ".join("-".join(str(x) for x in r["chord"]) for r in real))
    lab.row("how each chord was chosen", ";  ".join(f"{r['how']} ({r['figure']})" for r in real))
    par = [k for k, (a, b) in enumerate(zip(real, real[1:])) if F.parallels(a["chord"], b["chord"])]
    lab.row("parallel fifths or octaves", str(par or "none"))

    # 4. schemata in the chorales, real and shuffled
    real_c, shuf_c = {}, {}
    for c in book:
        if c.mode != "major":
            continue
        ev = P.degree_events(c)
        for name, _ in P.find_schemata(ev, SCHEMATA):
            real_c[name] = real_c.get(name, 0) + 1
        for name, _ in P.find_schemata([ev[i] for i in rng.permutation(len(ev))], SCHEMATA):
            shuf_c[name] = shuf_c.get(name, 0) + 1
    lab.row("schemata in 185 major chorales (shuffled)", ",  ".join(f"{n} {real_c.get(n, 0)} ({shuf_c.get(n, 0)})" for n in SCHEMATA))

    # 5. Problem 3, for the ear: eight two-chord progressions
    kinds = {"fifth down": 5, "fifth up": 7, "step": 2}
    answers, clips = [], []
    for _ in range(8):
        kind = list(kinds)[int(rng.integers(0, 3))]
        r0 = int(rng.integers(0, 12))
        r1 = (r0 + kinds[kind]) % 12
        y = np.zeros(int(2.6 * SR))
        for t, r in enumerate((r0, r1)):
            notes = [36 + r, 48 + r, 52 + r if t == 0 else 52 + r, 55 + r]
            notes = [n if n < 72 else n - 12 for n in notes]
            tone = sum(organ_tone(CH.hz(n), 1.1, partials=6, rolloff=0.7, decay=1.2) for n in notes)
            i = int(t * 1.0 * SR)
            y[i:i + len(tone)] += tone[: len(y) - i]
        clips.append(Clip(y, SR).fade(0.01, 0.2).at_level(-20.0))
        answers.append(kind)
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem, the eight progressions (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    keys = [k for k, _ in m.most_common()]
    a.bar(range(len(keys)), [100 * m[k] / tot for k in keys], color=[labs.GOLD if P.MOTION_KIND[k] == "forward" else "#888" for k in keys])
    a.set_xticks(range(len(keys)))
    a.set_xticklabels(keys, rotation=30)
    a.set_ylabel("in a hundred")
    a.set_title("How roots move in Bach's major chorales")
    names = ["uniform", "frequencies", "pairs", "triples"]
    b.bar(np.arange(4) - 0.2, [p["uniform"], p["n1"], p["n2"], p["n3"]], width=0.4, color=labs.GOLD, label="held-out chorales")
    b.bar(np.arange(4)[2:] + 0.2, [p["n2_shuffled"], p["n3_shuffled"]], width=0.4, color="#888", label="the same, shuffled")
    b.set_xticks(range(4))
    b.set_xticklabels(names)
    b.set_ylabel("bits per chord")
    b.set_title("How predictable the next chord is")
    b.legend(frameon=False)
    lab.fig = fig
    lab.note = ("Harmony has an order: away, tension, home; roots fall by fifths more than anything else; the chord "
                "before saves more than a bit per chord; a scale's worth of rules realizes a bass; and the galant "
                "schemata are hardly in the chorales, which belong to an older practice.")
    return lab
