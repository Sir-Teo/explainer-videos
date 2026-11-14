"""Lab 17: Bach's chorales as data, the rules of four-part writing counted, a harmonizer judged against Bach, and
cadences by ear."""

from itertools import product

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import fourpart as F
from explainer.music.monochord.partkit import organ_tone

TITLE = "Four voices, counted and harmonized"
GOAL = ("Count where Bach's four voices sing and how often he breaks the rules, harmonize a chorale tune the "
        "harmonizer has never seen, compare it with Bach beat by beat, and name cadences by ear.")
TASKS = [
    "Set CHORALE to another name from the test set (the lab prints some). How often does the search agree with Bach, and where do they part?",
    "Set WEIGHTS to {'parallel': 0} and then {'motion': 0.5}. What happens to the parallels, and to the inner voices?",
    "Set PHRASE to the Tune's second phrase, [65, 65, 64, 64, 62, 62, 60]. How many choices of I, IV and V are there, and which does the search pick?",
]
CHORALE = "bwv244.62"           # a chorale whose tune is in the test set (the Passion Chorale's last setting)
WEIGHTS = {}                    # changes to fourpart.DEFAULT_WEIGHTS
PHRASE = [72, 72, 79, 79, 81, 81, 79]   # the Tune's first phrase, an octave up, as a soprano
SR = 48_000
CADENCE_KINDS = ("authentic", "half", "picardy")


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    book = BC.load()
    train, test = BC.split(book, offset=2)
    lab.row("chorales, tunes", f"{len(book)} chorales; {len(BC.tunes(book))} tunes; train {len(train)}, test {len(test)} (split by tune)")
    lab.row("some test chorales", ", ".join(c.name for c in test[:8]))

    # 1. the rules, counted in Bach
    r = F.rule_census(book)
    par = sum(r["parallel"].values())
    lab.row("changes of chord; parallel fifths and octaves", f"{r['moves']:,}; {r['parallel']['fifths']} and {r['parallel']['octaves']} (one in {r['moves'] / par:.0f})")
    lab.row("hidden fifths and octaves; overlaps; crossed chords", f"{r['hidden']}; {r['overlap']}; {r['crossing']} of {r['chords']:,}")

    # 2. Problem 1: chords of I, IV and V under a phrase
    tonic = 0                                                     # the phrase is in C major
    triads = {"I": (0, 4, 7), "IV": (5, 9, 0), "V": (7, 11, 2)}
    fits = [[n for n, pcs in triads.items() if (p - tonic) % 12 in pcs] for p in PHRASE]
    lab.row("chords of I, IV, V under each note", "  ".join("/".join(f) for f in fits))
    lab.row("choices of chords, before voicing", f"{int(np.prod([len(f) for f in fits]))}")
    assert all(fits)

    # 3. the harmonizer on a chorale it has never seen
    models = {m: F.ChordModel(train, m) for m in ("major", "minor")}
    c = next(x for x in book if x.name == CHORALE)
    B = F.bach_on_beats(c)
    full = F.harmonize(B["soprano"], c.tonic, models[c.mode], fermatas=B["fermatas"], weights=WEIGHTS)
    plain = F.harmonize(B["soprano"], c.tonic, models[c.mode], fermatas=B["fermatas"], plain=True)
    ef, ep = F.evaluate(full, B), F.evaluate(plain, B)
    m = models[c.mode]
    lab.row(f"{CHORALE}: Bach's chords (first 12 beats)", " ".join(F.roman(s + (0,), c.mode) if s else "–" for s in B["states"][:12]))
    lab.row(f"{CHORALE}: the search's", " ".join(m.name(s) for s in full["states"][:12]))
    lab.row("same chord / same bass as Bach: search, chord-chooser", f"{100 * ef['same_chord']:.0f}% / {100 * ef['same_bass']:.0f}%;  {100 * ep['same_chord']:.0f}% / {100 * ep['same_bass']:.0f}%")
    lab.row("parallels: search, chord-chooser, Bach", f"{ef['ours']['parallels']}, {ep['ours']['parallels']}, {ef['bach']['parallels']}")
    lab.row("alto and tenor motion (semitones a beat): search, Bach", f"{ef['ours']['inner_motion']:.1f}, {ef['bach']['inner_motion']:.1f}")
    if not WEIGHTS:
        assert ef["ours"]["parallels"] == 0

    # 4. Problem 1 by machine: the phrase harmonized
    ph = F.harmonize(PHRASE, 0, F.ChordModel(book, "major"), fermatas=[len(PHRASE) - 1], weights=WEIGHTS)
    lab.row("the phrase, harmonized", " ".join(F.roman(s + (0,), "major") for s in ph["states"]) + "   " + "  ".join("-".join(str(x) for x in ch) for ch in ph["chords"][:3]) + " ...")

    # 5. Problem 3, for the ear: eight cadences from the chorales, on organ tones
    picks = []
    for x in book:
        labs_ = F.beat_labels(x)
        fk = [k for k, y in enumerate(labs_) if y["fermata"]]
        for k in fk[:-1]:
            if k < 2 or not labs_[k - 1]["label"] or not labs_[k]["label"]:
                continue
            a, z = labs_[k - 1]["label"][:2], labs_[k]["label"][:2]
            if x.mode == "major" and a == (7, "major") and z == (0, "major"):
                picks.append(("authentic", [labs_[k - 1]["chord"], labs_[k]["chord"]]))
            if x.mode == "major" and z == (7, "major") and a in ((2, "major"), (0, "major")):
                picks.append(("half", [labs_[k - 1]["chord"], labs_[k]["chord"]]))
        if x.mode == "minor" and labs_[-1]["label"] and labs_[-1]["label"][:2] == (0, "major") and labs_[-2]["label"]:
            picks.append(("picardy", [labs_[-2]["chord"], labs_[-1]["chord"]]))
    by = {k: [p for p in picks if p[0] == k] for k in CADENCE_KINDS}
    answers, clips = [], []
    for _ in range(8):
        kind = CADENCE_KINDS[int(rng.integers(0, 3))]
        _, chs = by[kind][int(rng.integers(0, len(by[kind])))]
        y = np.zeros(int(3.0 * SR))
        for t, ch in enumerate(chs):
            tone = sum(organ_tone(440 * 2 ** ((p - 69) / 12), 1.3 if t else 0.95, partials=6, rolloff=0.7, decay=1.2) for p in ch)
            i = int(t * 0.95 * SR)
            y[i:i + len(tone)] += tone[: len(y) - i]
        clips.append(Clip(y, SR).fade(0.01, 0.2).at_level(-20.0))
        answers.append(kind)
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem, the eight cadences (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    st = [[abs(v[k + 1][0] - v[k][0]) for x in book for v in [x.voices[j]] for k in range(len(v) - 1)] for j in range(4)]
    names = ["soprano", "alto", "tenor", "bass"]
    a.bar(range(4), [np.mean(s) for s in st], color=[labs.GOLD, "#F472B6", "#A3E635", "#7DD3FC"])
    a.set_xticks(range(4))
    a.set_xticklabels(names)
    a.set_ylabel("semitones")
    a.set_title("Bach's voices: the average move to the next note")
    keys = ["same chord", "same bass"]
    x = np.arange(2)
    b.bar(x - 0.2, [ep["same_chord"], ep["same_bass"]], width=0.4, color="#888", label="chord-chooser")
    b.bar(x + 0.2, [ef["same_chord"], ef["same_bass"]], width=0.4, color=labs.GOLD, label="search")
    b.set_xticks(x)
    b.set_xticklabels(keys)
    b.set_ylim(0, 1)
    b.set_title(f"Agreement with Bach on {CHORALE}")
    b.legend(frameon=False)
    lab.fig = fig
    lab.note = ("Bach's four voices move by small steps, the bass the most freely; he obeys the rules almost always "
                "and breaks them now and then; a search over chords and voicings learned from his chorales breaks "
                "none, agrees with his chords about four times in ten, and moves its inner voices too little.")
    return lab
