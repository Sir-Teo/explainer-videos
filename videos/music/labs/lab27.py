"""Lab 27: the Romantic century, computed: chromaticism and tonal clarity window by window in any piece of the Library,
the trend from 1680 to 1900 with a bootstrap interval, a theme transformed as Berlioz and Liszt transformed theirs, and
eight performances of a phrase, strict, arched or stolen, sorted by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import romantic as R
from explainer.music.monochord.partkit import organ_tone

TITLE = "The Romantic century, computed"
GOAL = ("Measure how far a piece strays from its key, window by window; fit the Library's trend with an honest interval; "
        "transform a theme; and hear the difference between strict time, a phrase arch and stolen time.")
TASKS = [
    "Choose a PIECE by a word of its corpus path ('Linden', 'opus19', 'maple', 'polonaise_op1n4'). Where are its most chromatic windows?",
    "Change WINDOW (in beats). How do chromaticism and clarity depend on it, and why does a short window find more 'keys'?",
    "Change DEPTH, the phrase arch's depth. At what depth does the rubato start to sound like a mistake?",
]
PIECE = "Linden"
WINDOW = 16.0
DEPTH = 0.3
TUNE = [(72, 0, 1), (72, 1, 1), (79, 2, 1), (79, 3, 1), (81, 4, 1), (81, 5, 1), (79, 6, 2),
        (77, 8, 1), (77, 9, 1), (76, 10, 1), (76, 11, 1), (74, 12, 1), (74, 13, 1), (72, 14, 2)]


def tone(m, seconds, gain=0.25):
    return organ_tone(440 * 2 ** ((m - 69) / 12), seconds, partials=6, rolloff=0.7, decay=2.0) * gain


def perform(kind: str, unit: float = 0.42) -> Clip:
    """The Tune's first two phrases over a bass, strict, under a phrase arch, or with the melody alone bending."""
    bass = [(48, 2 * k, 2) for k in range(8)]
    if kind == "strict":
        tm, tb = (lambda b: b), (lambda b: b)
    elif kind == "arch":
        tm = tb = lambda b: float(R.phrase_arch([b], 8.0, depth=DEPTH)[0])
    else:
        tm = lambda b: np.floor(b / 2) * 2 + 2 * ((b % 2) / 2 + 0.18 * np.sin(np.pi * (b % 2) / 2))
        tb = lambda b: b
    y = np.zeros(int(20 * unit * SR))
    for line, t_, g in ((TUNE, tm, 0.3), (bass, tb, 0.18)):
        for p, a, d in line:
            t0, t1 = t_(a) * unit, t_(a + d) * unit
            seg = tone(p, max(t1 - t0, 0.1), g)
            i = int(t0 * SR)
            y[i:i + len(seg)] += seg[: len(y) - i]
    return Clip(y, SR).fade(0.01, 0.2).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    lib = R.load_library()

    # 1. one piece, window by window
    r = next(x for x in lib if PIECE.lower() in x["path"].lower())
    notes = R.all_notes(r["parts"])
    m = R.measure(notes, window=WINDOW, hop=WINDOW / 2)
    lab.row(f"{r['composer']}, {r['title']} ({r['year']}): windows of {WINDOW:g} beats", f"{m['windows']}")
    lab.row("chromaticism, tonal clarity (time-weighted means)", f"{m['chromaticism']:.3f}, {m['clarity']:.3f}")
    worst = sorted(zip(m["per_window"], m["keys"]), key=lambda z: -z[0][0])[:3]
    lab.row("the three most chromatic windows (beat, key, share outside)",
            "; ".join(f"{k['start']:.0f} {k['key'][0]} {k['key'][1]} {c:.2f}" for (c, _), k in worst))
    assert 0.0 <= m["chromaticism"] <= 1.0

    # 2. the Library's trend, pieces of 1680-1900 only (the lab's Library: the music21 pieces)
    x = np.array([p["year"] for p in lib if p["year"] <= 1900], float)
    y = np.array([R.measure(R.all_notes(p["parts"]), window=WINDOW, hop=WINDOW / 2)["chromaticism"] for p in lib if p["year"] <= 1900])
    slope = np.polyfit(x, y, 1)[0] * 100
    boots = []
    for _ in range(1000):
        i = rng.integers(0, len(x), len(x))
        if np.ptp(x[i]) > 0:
            boots.append(np.polyfit(x[i], y[i], 1)[0] * 100)
    lab.row(f"the corpus pieces, {len(x)} of them to 1900: chromaticism per century, 95% interval",
            f"{100 * slope:+.1f} points ({100 * np.percentile(boots, 2.5):+.1f} to {100 * np.percentile(boots, 97.5):+.1f})")

    # 3. a theme transformed
    for kind in ("minor", "waltz", "march", "inverted"):
        lab.row(f"the Tune's head, {kind}", " ".join(f"{p}@{a:g}" for p, a, _ in R.transform(TUNE[:7], kind)))

    # 4. Problem 3: eight performances, shuffled
    kinds = list(rng.permutation(["strict", "strict", "arch", "arch", "arch", "stolen", "stolen", "stolen"]))
    lab.audio = concat([perform(k) for k in kinds], gap=0.9)
    lab.row("ear problem: the eight performances in the order played (listen first)", ", ".join(kinds))

    fig, (a, b) = labs.figure(2)
    st = [k["start"] for k in m["keys"]]
    a.plot(st, [c for c, _ in m["per_window"]], color=labs.RED, label="chromaticism")
    a.plot(st, [k for _, k in m["per_window"]], color=labs.BLUE, label="clarity")
    a.set_xlabel("beat")
    a.set_title(f"{r['composer']}: window by window")
    a.legend(frameon=False)
    b.scatter(x, 100 * y, color=labs.GOLD)
    xx = np.array([x.min(), x.max()])
    b.plot(xx, 100 * np.polyval(np.polyfit(x, y, 1), xx), color="#ddd")
    b.set_xlabel("year")
    b.set_ylabel("chromaticism, in 100")
    b.set_title("the corpus pieces to 1900, with a line")
    lab.fig = fig
    lab.note = ("Chromaticism and clarity depend on the window as much as on the music; the corpus pieces alone are too few "
                "for a sure trend, which is why the film adds the earlier collections and splits songs from instruments; "
                "and a transformed theme is the same notes with a new character.")
    return lab
