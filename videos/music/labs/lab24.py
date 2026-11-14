"""Lab 24: the Renaissance, computed: a Mass movement's dissonances classified, its opening imitation found, its
sonorities and lines measured, a stylometric test with leave-one-out on features you choose, a triad in any equal
tuning, and prepared and struck dissonances sorted by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import palestrina as PS
from explainer.music.monochord import renaissance as R
from explainer.music.monochord.instruments import choir as CH

TITLE = "The Renaissance, measured"
GOAL = ("Classify every dissonance in a piece by how it is treated, find its opening point of imitation, measure its "
        "thirds and its lines, test whether twelve style features can tell Monteverdi's early madrigals from his later "
        "ones, tune a triad in any equal division of the octave, and sort prepared from struck dissonances by ear.")
TASKS = [
    "Choose a PIECE (part of a Mass's name and a movement, or a madrigal like 'madrigal.5.1'). How many of its dissonances are free? Where are they?",
    "Choose which FEATURES the stylometric test uses. Which single feature separates Book 3 from Books 4-5 best? Does using all twelve help?",
    "Change N, the number of equal steps to the octave. Which N between 12 and 60 give a major third within 2 cents of 5:4 and a fifth within 3 cents of 3:2?",
]
PIECE = ("Papae Marcelli", "Kyrie")
FEATURES = ["free", "suspension", "note_len"]
N = 31


def sing(voices, unit=0.3):
    outs = []
    for j, v in enumerate(voices):
        y = CH.sing([(p, a * unit, d * unit) for p, a, d in v], ["alto", "bass"][j], "a", seed=j)
        outs.append(y)
    n = max(len(y) for y in outs) + SR // 2
    out = np.zeros(n)
    for y in outs:
        out[: len(y)] += y
    return Clip(out / max(np.abs(out).max(), 1e-9) * 0.4, SR).fade(0.02, 0.2).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    book = R.load()

    # 1. one piece: its dissonances, its imitation, its sonorities, its lines
    if isinstance(PIECE, tuple):
        pc = [p for p in book if PIECE[0].lower() in p.work.lower() and p.title.lower().startswith(PIECE[1].lower())][0]
    else:
        pc = [p for p in book if p.name == PIECE][0]
    c = PS.dissonances(pc)
    sh = PS.shares(c)
    lab.row(f"{pc.work} {pc.title}: dissonances against the bass", f"{sum(c.values())}: " + ", ".join(f"{k} {100 * sh[k]:.1f}%" for k in PS.KINDS))
    im = PS.imitation(pc)
    lab.row("opening imitation: entries, delays (quarters), intervals (semitones)",
            f"{im['entries']} of {im['voices']} voices; " + ", ".join(f"{f['delay'] / 24:g}/{f['interval']}" for f in im["followers"]))
    so = PS.sonorities(pc)
    me = PS.melodic(pc)
    lab.row("sonorities with a third, full triads; last chord with a third?", f"{so['third'] / so['n']:.2f}, {so['triad'] / so['n']:.2f}; {so['final_third']}")
    lab.row("leaps, turned back by step, forbidden intervals per 1000 moves",
            f"{me['leaps']}, {me['recovered']}, {1000 * me['forbidden'] / max(me['moves'], 1):.1f}")

    # 2. stylometry on Monteverdi's books, with the features you choose
    mon = [p for p in book if p.book]
    X = np.array([PS.features(p) for p in mon])
    y = ["Book 3" if p.book == 3 else "Books 4-5" for p in mon]
    cols = [PS.FEATURES.index(f) for f in FEATURES]
    res = PS.loo_centroid(X[:, cols], y)
    full = PS.loo_centroid(X, y)
    lab.row(f"Book 3 against Books 4-5, leave-one-out, features {FEATURES}", f"{res['accuracy']:.2f} (all twelve: {full['accuracy']:.2f})")
    singles = sorted(((PS.loo_centroid(X[:, [k]], y)["accuracy"], f) for k, f in enumerate(PS.FEATURES)), reverse=True)[:3]
    lab.row("the best single features", ", ".join(f"{f} {a:.2f}" for a, f in singles))
    assert 0.0 <= res["accuracy"] <= 1.0

    # 3. a triad in N equal steps
    third = round(N * np.log2(5 / 4))
    fifth = round(N * np.log2(3 / 2))
    lab.row(f"in {N} equal steps: the third and fifth (cents) and their errors",
            f"{1200 * third / N:.1f} ({1200 * third / N - 1200 * np.log2(5 / 4):+.1f}), {1200 * fifth / N:.1f} ({1200 * fifth / N - 1200 * np.log2(1.5):+.1f})")
    good = [n for n in range(12, 61) if abs(1200 * round(n * np.log2(1.25)) / n - 386.31) < 2 and abs(1200 * round(n * np.log2(1.5)) / n - 701.96) < 3]
    lab.row("N from 12 to 60 with a third within 2 cents and a fifth within 3", ", ".join(map(str, good)))
    assert 31 not in good or abs(1200 * 10 / 31 - 386.31) < 2

    # 4. Problem 3: ten cadences, prepared or struck
    clips, answers = [], []
    for k in range(10):
        prepared = bool(rng.random() < 0.5)
        tr = int(rng.integers(-3, 4))
        up = [(72 + tr, 0, 4), (72 + tr, 4, 2), (71 + tr, 6, 2), (72 + tr, 8, 4)] if prepared else [(69 + tr, 0, 4), (72 + tr, 4, 2), (71 + tr, 6, 2), (72 + tr, 8, 4)]
        lo = [(57 + tr, 0, 4), (62 + tr, 4, 4), (60 + tr, 8, 4)]
        clips.append(sing([up, lo], 0.28))
        answers.append("prepared" if prepared else "struck")
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem, the ten cadences in order (listen first)", ", ".join(answers))

    fig, (a, b) = labs.figure(2)
    ks = list(PS.KINDS)
    a.bar(range(len(ks)), [100 * sh[k] for k in ks], color=labs.GOLD)
    a.set_xticks(range(len(ks)))
    a.set_xticklabels(ks, fontsize=8)
    a.set_ylabel("in 100 dissonances")
    a.set_title(f"{pc.title}: how its dissonances are treated")
    fi, si = PS.FEATURES.index("free"), PS.FEATURES.index("suspension")
    for lab_, col in (("Book 3", labs.GOLD), ("Books 4-5", "#d66")):
        m = [i for i, v in enumerate(y) if v == lab_]
        b.scatter(X[m, fi], X[m, si], color=col, label=lab_, s=18)
    b.set_xlabel("share of free dissonance")
    b.set_ylabel("share of suspensions")
    b.legend()
    b.set_title("Monteverdi's madrigals, two of the twelve features")
    lab.fig = fig
    lab.note = ("Palestrina's dissonances are passing notes, suspensions and neighbours almost without exception; his "
                "movements open with imitation at the octave, fourth or fifth; Monteverdi's later madrigals leave "
                "dissonance free far more often, enough for a crude test to tell his books apart some of the time; and "
                "31 equal steps give an almost pure third.")
    return lab
