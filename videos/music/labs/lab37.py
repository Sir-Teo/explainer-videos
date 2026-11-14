"""Lab 37: timelines, computed: evenness, oddity, off-beatness and centrality for any rhythm; an ensemble whose parts
can be muted and soloed; interlocking parts designed so that a melody of your own appears in their high notes."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import timelines as T
from videos.music.music37 import compute as C

TITLE = "Timelines, computed"
GOAL = ("Measure timelines four ways and by their distance to each other; listen to an ensemble part by part; and "
        "design interlocking parts whose combined high notes spell a melody that neither part plays.")
TASKS = [
    "Add a RHYTHM of your own (x for a stroke, . for a rest). Is it Euclidean? Odd? How off-beat?",
    "Change SOLO to any of bell, rattle, kagan, kidi, sogo, lead. How does each part sound alone against the bell?",
    "Write your own MELODY (key numbers above 66) and design its parts. At what speed does it appear?",
]
RHYTHM = "x..x.x..x.x..x.."
SOLO = ["bell", "kidi", "sogo"]
MELODY = [72, 76, 79, 81, 79, 76, 74, 72]
LOW = [55, 59, 62, 57]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    for name in ("standard pattern (12)", "son clave (16)", "bossa nova (16)"):
        m = T.metrics(T.TIMELINES[name])
        lab.row(f"{name}: from even, Euclidean, odd, off-beat", f"{m['evenness']:.2f}, {m['euclidean']}, {m['oddity']}, {m['offbeat']}")
    m = T.metrics(RHYTHM)
    lab.row(f"your rhythm {RHYTHM}: from even, Euclidean, odd, off-beat", f"{m['evenness']:.2f}, {m['euclidean']}, {m['oddity']}, {m['offbeat']}")
    cent = T.centrality()
    assert min(cent, key=cent.get) == "son clave (16)"
    lab.row("total swap distance to the other five claves", ", ".join(f"{k.split(' (')[0]}: {v}" for k, v in cent.items()))
    lab.row("the standard pattern's interval content (distances 1 to 6)", str(list(T.interval_content(T.TIMELINES["standard pattern (12)"]).values())))

    # the ensemble, with only the SOLO parts, four cycles
    parts = []
    for name in SOLO:
        if name == "lead":
            C.lead_layer(parts, 0.0, 4)
        else:
            C.ewe_layer(parts, name, 0.0, 4)
    ens = Clip(mix(parts, duration=4 * 12 * C.P12 + 1.0).y, SR).at_level(-20.0)

    # interlocking parts for MELODY, and the ear problem: the parts at several speeds, in a random order
    a, b, target = T.design_inherent(MELODY, LOW, 3)
    heard = [p for _, p in T.inherent([a, b], 66)]
    assert heard == MELODY or max(MELODY) <= 66 or min(LOW) > 66, "the high stream should spell the melody"
    lab.row("your melody, as heard in the high stream of the two parts", f"{heard} (matches: {heard == MELODY})")
    lab.row("high notes in part A / part B", f"{[p for _, p in a if p > 66]} / {[p for _, p in b if p > 66]}")
    rates = list(rng.permutation([3.0, 5.0, 8.0, 12.0]))
    clips = []
    for r in rates:
        pr = []
        for part in (a, b):
            for rep in range(2):
                for i, mm in part:
                    pr.append((Clip(C.tine(mm, 0.12, 0.8), SR), (rep * len(target) * 3 + i) / r, -1.5 if mm > 66 else 0.0))
        clips.append(Clip(mix(pr, duration=2 * len(target) * 3 / r + 0.8).y, SR).at_level(-20.0))
    lab.audio = concat([ens] + clips, gap=1.0)
    lab.row("ear problem: notes a second in each version, in order (listen first)", ", ".join(f"{r:g}" for r in rates))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.bar(range(1, 7), [T.interval_content(T.TIMELINES["standard pattern (12)"])[d] for d in range(1, 7)], color=labs.GOLD)
    ax1.set_xlabel("distance between two strokes (pulses)")
    ax1.set_ylabel("pairs")
    ax1.set_title("the standard pattern is deep")
    for part, col in ((a, "C0"), (b, "C1")):
        ax2.scatter([i for i, _ in part], [p for _, p in part], s=14, color=col)
    ax2.plot([i for i, _ in target], [p for _, p in target], color="k", lw=1)
    ax2.axhline(66, color="grey", ls="--", lw=0.8)
    ax2.set_xlabel("pulse")
    ax2.set_ylabel("key number")
    ax2.set_title("two parts and the melody between them")
    lab.fig = fig
    lab.note = ("Son clave is the most central of the six five-stroke claves; the standard pattern shares the major scale's "
                "steps and interval content; and an inherent melody separates from its low filler only at speed.")
    return lab
