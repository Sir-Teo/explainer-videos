"""Precompute everything numerical, and every sound, in Part 24 of *Music, Built* ("The Renaissance").

    python -m videos.music.music24.compute              # everything missing (a few minutes)
    python -m videos.music.music24.compute --force style

Numbers are cached in ``.cache/music24/<name>.json``, sounds in ``.cache/music24/audio/``.  The style measures are
Monochord's (``explainer/music/monochord/palestrina.py``); the pieces are ``monochord/renaissance.py``'s table
(Palestrina's Masses from Humdrum encodings, Monteverdi's madrigals from Books 3 to 5) and Part 23's
fourteenth-century corpus; everything heard is sung by Part 17's choir, so every clip is labelled synthesized.
Published findings are cited in the README.

Items:
    hook        the opening of the Kyrie of the Missa Papae Marcelli, sung from the encoding
    thirds      sonorities with a third, full triads and final chords: the fourteenth century against Palestrina
    imitation   points of imitation in Palestrina's movements: how many, at what interval; one heard
    masses      the Masses in the corpus by title and kind
    dissonance  every dissonance in the corpus classified: passing, neighbour, suspension, cambiata, free
    kinds       the treatments, heard on two voices; prepared against unprepared (an ear question)
    melody      leaps and their recovery; forbidden intervals per thousand moves
    style       stylometric features, nearest-centroid attribution with leave-one-out, the features that decide
    quiz        an ear question: Palestrina or Monteverdi?
    cruda       Monteverdi's Cruda Amarilli, the opening, with its free dissonances marked
    tuning      the triad in Pythagorean, just (Zarlino) and 31-tone (Vicentino) tuning, heard
    chromatic   a chromatic progression in the manner of Gesualdo (ours), heard
    tune        Variation 24: the Tune as a four-voice point of imitation
    variation   the Variations ledger, row 24
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import canon as K
from explainer.music.monochord import melody as M
from explainer.music.monochord import palestrina as PS
from explainer.music.monochord import renaissance as R
from explainer.music.monochord import trecento as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver, signoff

CACHE = Cache("music24")
CLIPS = ClipStore("music24")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
PARTS6 = ["soprano", "alto", "alto", "tenor", "tenor", "bass", "bass", "bass"]


def sing(voices, unit: float, parts=None, vowels=None, gains=None, tail: float = 0.6, seed: int = 0, tuning=None) -> Clip:
    """Voices of (key number, onset, duration) in units of ``unit`` seconds, each sung by one of the choir's parts.
    ``tuning``: a function from key number to a (possibly fractional) key number."""
    parts = parts or PARTS6[: len(voices)]
    vowels = vowels or ["a", "O", "a", "O", "a", "O", "a", "O"][: len(voices)]
    gains = gains or [0.0] * len(voices)
    outs = []
    for j, v in enumerate(voices):
        if not v:
            continue
        notes = [((tuning(m) if tuning else m), a * unit, d * unit) for m, a, d in v]
        y = CH.sing(notes, parts[j], vowels[j], seed=seed + j)
        outs.append(y * 10 ** (gains[j] / 20))
    n = max(len(y) for y in outs) + int(tail * SR)
    out = np.zeros(n)
    for y in outs:
        out[: len(y)] += y
    return Clip(out / max(np.abs(out).max(), 1e-9) * 0.5, SR).fade(0.02, 0.3)


def rows(v):
    return [[int(round(p)), float(a), float(d)] for p, a, d in v]


def excerpt(piece, bars: int, start_bar: int = 0):
    lo, hi = start_bar * piece.bar, (start_bar + bars) * piece.bar
    return [[(p, (o - lo) / 24.0, min(d, hi - o) / 24.0) for p, o, d in v if lo <= o < hi] for v in piece.voices]


def corpus():
    book = R.load()
    pal = [p for p in book if p.book == 0]
    mon = [p for p in book if p.book]
    return book, pal, mon


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    _, pal, _ = corpus()
    ky = [p for p in pal if "Marcelli" in p.work and p.title.lower().startswith("kyrie")]
    p = ky[0] if ky else [p for p in pal if "Marcelli" in p.work][0]
    ex = excerpt(p, 8)
    q = 0.3                                                   # seconds a quarter note of the encoding (a half is the beat)
    c = sing(ex, q)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["kyrie"])
    return {"work": p.work, "title": p.title, "voices": [rows(v) for v in ex], "quarter": q, "n_voices": len(p.voices),
            "clips": {"kyrie": save("hook.kyrie", s, level=None, detail=f"Palestrina, {p.work}, {p.title}: the opening, sung from the Humdrum encoding by synthetic voices")}}


def compute_thirds() -> dict:
    _, pal, mon = corpus()
    tre = T.load()
    out = {}
    for name, ps in (("fourteenth century", tre), ("Palestrina", pal), ("Monteverdi", mon)):
        s = [PS.sonorities(p) for p in ps]
        n = sum(x["n"] for x in s)
        out[name] = {"pieces": len(ps), "third": sum(x["third"] for x in s) / n, "triad": sum(x["triad"] for x in s) / n,
                     "final_third": float(np.mean([x["final_third"] for x in s]))}
    # heard: a fourteenth-century final cadence and a Palestrina one
    t = max(tre, key=lambda p: len(p.voices) == 3 and p.length // p.bar > 30)
    tb = t.length // t.bar
    exA = excerpt(t, 3, tb - 3)
    p = [x for x in pal if len(x.voices) == 4 and PS.sonorities(x)["final_third"]][3]
    pb = p.length // p.bar
    exB = excerpt(p, 3, pb - 3)
    cA = sing(exA, 0.34, parts=["alto", "tenor", "bass"][: len(exA)])
    cB = sing(exB, 0.24)
    q = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"census": out, "A": {"title": t.title, "composer": t.composer, "voices": [rows(v) for v in exA], "quarter": 0.34},
            "B": {"title": f"{p.work}, {p.title}", "voices": [rows(v) for v in exB], "quarter": 0.24},
            "starts": {k: float(q.events[k]) for k in "AB"},
            "clips": {"two": save("thirds.endings", q, level=None, detail=f"two endings: {t.composer}, {t.title}; then Palestrina, {p.work}, {p.title}")}}


def compute_imitation() -> dict:
    _, pal, mon = corpus()
    im = [PS.imitation(p) for p in pal]
    share = float(np.mean([x["imitative"] for x in im]))
    entries = Counter(x["entries"] for x in im)
    iv = Counter(f["interval"] % 12 for x in im for f in x["followers"])
    exact = sum(f["exact"] for x in im for f in x["followers"])
    nf = sum(len(x["followers"]) for x in im)
    share_m = float(np.mean([PS.imitation(p)["imitative"] for p in mon]))
    # a clear point: four or more entries, all exact, in a four-voice movement
    cand = [(p, x) for p, x in zip(pal, im) if len(p.voices) == 4 and x["entries"] == 4 and all(f["exact"] for f in x["followers"])]
    p, x = cand[len(cand) // 2]
    last = max(f["delay"] for f in x["followers"])
    bars = int(last // p.bar) + 3
    ex = excerpt(p, bars)
    c = sing(ex, 0.26)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["point"])
    starts = sorted((v[0][1], j) for j, v in enumerate(ex) if v)
    return {"share": share, "share_monteverdi": share_m, "entries": {str(k): v for k, v in entries.items()}, "intervals": {str(k): v for k, v in iv.items()},
            "exact": exact, "followers": nf, "piece": {"work": p.work, "title": p.title, "voices": [rows(v) for v in ex], "quarter": 0.26,
                                                         "entry_order": [j for _, j in starts], "entry_times": [t for t, _ in starts]},
            "clips": {"point": save("imitation.point", s, level=None, detail=f"Palestrina, {p.work}, {p.title}: a point of imitation, sung from the encoding")}}


def compute_masses() -> dict:
    _, pal, _ = corpus()
    works = Counter(p.work for p in pal)
    voices = Counter(len(p.voices) for p in pal)
    titled = sorted({w for w in works if w})
    return {"works": len(titled), "movements": len(pal), "voices": {str(k): v for k, v in voices.items()}, "titles": titled[:200],
            "marcelli": [p.title for p in pal if "Marcelli" in p.work]}


def compute_dissonance() -> dict:
    _, pal, mon = corpus()
    out = {}
    for name, ps in (("Palestrina", pal), ("Monteverdi, Book 3 (1592)", [p for p in mon if p.book == 3]),
                     ("Monteverdi, Book 4 (1603)", [p for p in mon if p.book == 4]), ("Monteverdi, Book 5 (1605)", [p for p in mon if p.book == 5])):
        c = Counter()
        for p in ps:
            c.update(PS.dissonances(p))
        out[name] = {"pieces": len(ps), "total": sum(c.values()), "shares": PS.shares(c), "counts": dict(c)}
    per = sorted(PS.shares(PS.dissonances(p))["free"] for p in pal)
    return {"groups": out, "palestrina_free_quantiles": [per[int(q * (len(per) - 1))] for q in (0.1, 0.5, 0.9, 1.0)]}


def compute_kinds() -> dict:
    # two voices over a held or moving lower voice: passing, neighbour, suspension (7-6), cambiata
    demos = {
        "passing": ([(72, 0, 2), (71, 2, 2), (69, 4, 4)], [(57, 0, 8)]),
        "neighbour": ([(72, 0, 2), (74, 2, 2), (72, 4, 4)], [(57, 0, 8)]),
        "suspension": ([(72, 0, 6), (71, 6, 2), (72, 8, 4)], [(57, 0, 4), (62, 4, 4), (60, 8, 4)]),
        "cambiata": ([(72, 0, 2), (71, 2, 2), (67, 4, 2), (69, 6, 2), (71, 8, 4)], [(57, 0, 4), (55, 4, 4), (56, 8, 4)]),
    }
    clips, starts = [], {}
    for k, (u, l) in demos.items():
        clips.append(sing([u, l], 0.3, parts=["alto", "bass"]).at_level(LEVEL))
    s = concat(clips, gap=0.8, names=list(demos))
    # the ear question: the same cadence with the dissonance prepared (a suspension) and struck freely
    prep = [[(72, 0, 6), (71, 6, 2), (72, 8, 4)], [(57, 0, 4), (62, 4, 4), (60, 8, 4)]]
    free = [[(69, 0, 4), (72, 4, 2), (71, 6, 2), (72, 8, 4)], [(57, 0, 4), (62, 4, 4), (60, 8, 4)]]
    cA = sing(free, 0.32, parts=["alto", "bass"])
    cB = sing(prep, 0.32, parts=["alto", "bass"])
    q = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"demos": {k: [rows(u), rows(l)] for k, (u, l) in demos.items()}, "starts": {k: float(s.events[k]) for k in demos}, "unit": 0.3,
            "quiz": {"A": [rows(v) for v in free], "B": [rows(v) for v in prep], "unit": 0.32, "answer": "B"},
            "quiz_starts": {k: float(q.events[k]) for k in "AB"},
            "clips": {"four": save("kinds.four", s, level=None, detail="passing, neighbour, suspension and cambiata, two synthetic voices"),
                      "quiz": save("kinds.prepared", q, level=None, detail="a seventh over the bass: struck freely, then prepared as a suspension")}}


def compute_melody() -> dict:
    _, pal, mon = corpus()
    out = {}
    for name, ps in (("fourteenth century", T.load()), ("Palestrina", pal), ("Monteverdi", mon)):
        m = [PS.melodic(p) for p in ps]
        mv = sum(x["moves"] for x in m)
        lp = sum(x["leaps"] for x in m)
        out[name] = {"moves": mv, "leap_share": lp / mv, "recovered": sum(x["recovered"] for x in m) / max(lp, 1),
                     "forbidden_per_1000": 1000 * sum(x["forbidden"] for x in m) / mv}
    return {"groups": out}


def compute_style() -> dict:
    _, pal, mon = corpus()
    rng = np.random.default_rng(24)
    sample = [pal[i] for i in sorted(rng.choice(len(pal), size=len(mon), replace=False))]
    X1 = np.array([PS.features(p) for p in sample + mon])
    y1 = ["Palestrina"] * len(sample) + ["Monteverdi"] * len(mon)
    a1 = PS.loo_centroid(X1, y1)
    w1 = PS.centroid_weights(X1, y1, "Monteverdi", "Palestrina")
    X2 = np.array([PS.features(p) for p in mon])
    y2 = ["Book 3" if p.book == 3 else "Books 4-5" for p in mon]
    a2 = PS.loo_centroid(X2, y2)
    w2 = PS.centroid_weights(X2, y2, "Books 4-5", "Book 3")
    # one feature alone: the share of free dissonance, with a threshold chosen on the others (leave-one-out)
    f = X2[:, 0]
    yy = np.array([0 if v == "Book 3" else 1 for v in y2])
    hits = 0
    for i in range(len(f)):
        m = np.arange(len(f)) != i
        thr = (f[m][yy[m] == 0].mean() + f[m][yy[m] == 1].mean()) / 2
        hits += int((f[i] > thr) == bool(yy[i]))
    cruda = [i for i, p in enumerate(mon) if p.name == "madrigal.5.1"][0]
    fi, si = PS.FEATURES.index("free"), PS.FEATURES.index("suspension")
    scatter = [[float(x[fi]), float(x[si]), lab] for x, lab in zip(X1, y1)]
    return {"scatter": scatter, "composer": {"n": len(y1), "accuracy": a1["accuracy"], "confusion": a1["confusion"], "weights": w1},
            "books": {"n": len(y2), "accuracy": a2["accuracy"], "confusion": a2["confusion"], "weights": w2, "one_feature": hits / len(f),
                      "cruda_pred": a2["pred"][cruda]},
            "features": list(PS.FEATURES)}


def compute_quiz() -> dict:
    _, pal, mon = corpus()
    # the Monteverdi excerpt: the four bars of Books 4-5 densest in free dissonance; the Palestrina: a five-voice
    # movement's four bars with none
    best = None
    for m in [x for x in mon if x.book in (4, 5) and len(x.voices) == 5]:
        marks = free_marks(m, 0, m.length)
        nb = m.length // m.bar
        for b0 in range(1, max(nb - 4, 1)):
            n = sum(1 for _, t in marks if b0 * m.bar <= t * 24 < (b0 + 4) * m.bar)
            if best is None or n > best[0]:
                best = (n, m, b0)
    nA, m, b0 = best
    p = [x for x in pal if len(x.voices) == 5][40]
    exA = excerpt(m, 4, b0)
    exB = excerpt(p, 4, 4)
    cA = sing(exA, 0.3)
    cB = sing(exB, 0.24)
    q = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    marksA = free_marks(m, b0 * m.bar, (b0 + 4) * m.bar)
    marksB = free_marks(p, 4 * p.bar, 8 * p.bar)
    return {"A": {"title": m.title, "composer": m.composer, "work": m.work, "name": m.name, "voices": [rows(v) for v in exA], "quarter": 0.3, "free": len(marksA), "marks": marksA, "bar": b0},
            "B": {"title": p.title, "composer": p.composer, "work": p.work, "voices": [rows(v) for v in exB], "quarter": 0.24, "free": len(marksB), "marks": marksB},
            "starts": {k: float(q.events[k]) for k in "AB"}, "answer": {"A": "Monteverdi", "B": "Palestrina"},
            "clips": {"quiz": save("style.quiz", q, level=None, detail=f"two excerpts: Monteverdi, {m.work}, {m.name}; Palestrina, {p.work}, {p.title}")}}


def free_marks(piece, lo: int, hi: int) -> list[list]:
    """Where the free dissonances fall in a stretch of a piece: (voice, onset in quarters)."""
    V = PS.Voices(piece)
    marks = []
    ons = sorted({o for v in piece.voices for _, o, _ in v if lo <= o < hi})
    for t in ons:
        live = [(j, s[0], s[1][0]) for j in range(len(V.v)) for s in [V.at(j, t)] if s is not None]
        if len(live) < 2:
            continue
        low = min(live, key=lambda x: x[2])
        for j, i, p in live:
            if j == low[0] or (p - low[2]) % 12 in PS.CONSONANT:
                continue
            if PS.classify(V, j, i, low[0], low[1], t) == "free":
                marks.append([j, (t - lo) / 24.0])
    return marks


def compute_cruda() -> dict:
    _, _, mon = corpus()
    p = [x for x in mon if x.name == "madrigal.5.1"][0]
    bars = 16
    ex = excerpt(p, bars)
    c = sing(ex, 0.3)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["cruda"])
    marks = free_marks(p, 0, bars * p.bar)
    return {"voices": [rows(v) for v in ex], "quarter": 0.3, "marks": marks, "bars": bars, "n_voices": len(p.voices),
            "free_share": PS.shares(PS.dissonances(p))["free"],
            "clips": {"cruda": save("cruda.amarilli", s, level=None, detail="Monteverdi, Cruda Amarilli (Book 5, 1605): the opening, sung from the encoding by synthetic voices")}}


def compute_tuning() -> dict:
    tri = PS.triad_cents()
    # C E G sustained in each tuning: the third and fifth set by their cents above C
    clips = []
    for k in ("pythagorean", "just", "31-tone"):
        th, fi = tri[k]
        v = [[(60 + fi / 100, 0, 6)], [(60 + th / 100, 0, 6)], [(60, 0, 6)], [(48, 0, 6)]]
        clips.append(sing(v, 0.5, parts=["alto", "tenor", "tenor", "bass"], vowels=["a"] * 4).at_level(LEVEL))
    s = concat(clips, gap=0.9, names=["pythagorean", "just", "31-tone"])
    return {"cents": {k: list(v) for k, v in tri.items()}, "starts": {k: float(s.events[k]) for k in ("pythagorean", "just", "31-tone")},
            "clips": {"triads": save("tuning.triads", s, level=None, detail="C major triads with the third and fifth tuned Pythagorean, just (Zarlino) and in 31 equal steps (Vicentino)")}}


def compute_chromatic() -> dict:
    # chords whose roots move by thirds and semitones, voice-led by the smallest steps (ours)
    roots = [("A", 57, "minor"), ("F", 53, "major"), ("D♭", 49, "major"), ("B♭", 46, "minor"), ("G♭", 54, "major"), ("E", 52, "major"), ("A", 57, "major")]
    triads = []
    for name, b, q in roots:
        r = b % 12
        pcs = (r, (r + (3 if q == "minor" else 4)) % 12, (r + 7) % 12)
        triads.append((name, b, q, pcs))
    prev = (69, 64, 60)
    voices = [[], [], [], []]
    for k, (name, b, q, pcs) in enumerate(triads):
        cands = [(s, a, t) for s in range(62, 78) for a in range(57, s) for t in range(50, a)
                 if {s % 12, a % 12, t % 12} == set(pcs)]
        v = min(cands, key=lambda c: sum(abs(x - y) for x, y in zip(c, prev)))
        prev = v
        for j, p in enumerate(v + (b if b >= 40 else b + 12,)):
            voices[j].append((p, 4 * k, 4))
    c = sing(voices, 0.32)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["chromatic"])
    return {"chords": [f"{n} {q}" for n, _, q, _ in triads], "voices": [rows(v) for v in voices], "unit": 0.32,
            "clips": {"chromatic": save("chromatic.gesualdo", s, level=None, detail="seven triads joined by third and semitone relations, in the manner of Gesualdo, ours")}}


def tune_point():
    """The Tune's first two phrases as a point of imitation: soprano, then tenor an octave below, then alto at the fifth
    (a real answer), then bass, each entering four beats after the last; the voices then continue in free counterpoint
    on a beat grid to a final C."""
    t = M.corpus([M.THE_TUNE])[0]
    head = []
    a = 0.0
    for p, d in zip(t.pitches[:7], t.beats[:7]):
        head.append((p, a, float(d)))
        a += d
    entries = [("soprano", 72, 0.0), ("tenor", 60, 4.0), ("alto", 67, 8.0), ("bass", 48, 12.0)]
    total = 24.0
    grid = [float(k) for k in range(int(total))]
    lines = {}
    order = []
    for name, base, t0 in entries:
        lines[name] = [(base + p, t0 + o, d) for p, o, d in head]
        order.append(name)
    ranges = {"soprano": (64, 79), "alto": (57, 72), "tenor": (52, 67), "bass": (40, 57)}
    for name, base, t0 in entries:
        end = t0 + 8.0
        others = [lines[n] for n in lines if n != name]
        g = [x for x in grid if x >= end]
        if not g:
            continue
        lo, hi = ranges[name]
        notes = [p for p in range(lo, hi + 1) if p % 12 in (0, 2, 4, 5, 7, 9, 11)]
        free = K.free_voice(others, g, notes, below=(name == "bass"), ends=(None if name != "bass" else None))
        if free is None:
            continue
        lines[name] = lines[name] + [(p, x, 1.0) for p, x in zip(free, g)]
    return [lines[n] for n in ("soprano", "alto", "tenor", "bass")], entries


def compute_tune() -> dict:
    voices, entries = tune_point()
    c = sing(voices, 0.36, parts=["soprano", "alto", "tenor", "bass"])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["point"])
    # count consonance on the beats after all voices have entered
    bad = 0
    beats = 0
    for t in range(12, 24):
        live = [next((p for p, o, d in v if o <= t < o + d), None) for v in voices]
        live = [p for p in live if p is not None]
        if len(live) < 2:
            continue
        beats += 1
        b = min(live)
        if any((p - b) % 12 not in (0, 3, 4, 7, 8, 9) for p in live if p != b):
            bad += 1
    return {"voices": [rows(v) for v in voices], "entries": [[n, b, t] for n, b, t in entries], "unit": 0.36, "seconds": s.duration,
            "dissonant_beats": bad, "beats": beats,
            "clips": {"variation": save("tune.variation24", s, level=None, detail="the Tune's first phrase as a four-voice point of imitation, entries four beats apart, free counterpoint after")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 24, "title": r"as a four-voice point of imitation", "seconds": round(t["seconds"], 2),
            "measure": rf"four entries four beats apart; after the last entry {t['beats'] - t['dissonant_beats']} of {t['beats']} beats consonant above the bass",
            "clip": "tune.variation24"}


def compute_fauxbourdon() -> dict:
    """Fauxbourdon on the Tune's first phrase as a chant: the melody on top, a voice a sixth below, a middle voice a
    fourth below the top, opening and closing on an octave and fifth."""
    t = M.corpus([M.THE_TUNE])[0]
    mel, a = [], 0.0
    for p, d in zip(t.pitches[:14], t.beats[:14]):
        mel.append((72 + p, a, float(d)))
        a += d
    white = (0, 2, 4, 5, 7, 9, 11)

    def down(p, steps):
        q, k = p, 0
        while k < steps:
            q -= 1
            if q % 12 in white:
                k += 1
        return q
    low = [(down(p, 5), o, d) for p, o, d in mel]             # a sixth below
    mid = [(down(p, 3), o, d) for p, o, d in mel]             # a fourth below
    low[0] = (mel[0][0] - 12, low[0][1], low[0][2])
    low[-1] = (mel[-1][0] - 12, low[-1][1], low[-1][2])
    mid[0] = (mel[0][0] - 5, mid[0][1], mid[0][2])
    mid[-1] = (mel[-1][0] - 5, mid[-1][1], mid[-1][2])
    c = sing([mel, mid, low], 0.36, parts=["alto", "tenor", "bass"])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["fb"])
    return {"voices": [rows(v) for v in (mel, mid, low)], "unit": 0.36,
            "clips": {"fb": save("thirds.fauxbourdon", s_, level=None, detail="the Tune's first two phrases in fauxbourdon: the melody, a fourth below it, a sixth below it")}}


def compute_line() -> dict:
    """One voice of Palestrina alone: a long line, with its leaps and how it recovers."""
    _, pal, _ = corpus()
    p = [x for x in pal if "Marcelli" in x.work and x.title.lower().startswith("agnus")][0] if any("Marcelli" in x.work and x.title.lower().startswith("agnus") for x in pal) else pal[100]
    v = p.voices[0]
    seg = [n for n in v if n[1] < 12 * p.bar]
    t0 = seg[0][1]
    notes = [(q, (o - t0) / 24.0, d / 24.0) for q, o, d in seg]
    leaps = []
    for k in range(len(notes) - 1):
        iv = notes[k + 1][0] - notes[k][0]
        if abs(iv) >= 5:
            nx = notes[k + 2][0] - notes[k + 1][0] if k + 2 < len(notes) else 0
            leaps.append({"at": k + 1, "size": iv, "recovered": bool(nx and 1 <= abs(nx) <= 2 and np.sign(nx) == -np.sign(iv))})
    c = sing([notes], 0.3, parts=["alto"])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["line"])
    return {"work": p.work, "title": p.title, "notes": rows(notes), "quarter": 0.3, "leaps": leaps,
            "high": int(max(q for q, _, _ in notes)), "low": int(min(q for q, _, _ in notes)),
            "clips": {"line": save("melody.line", s_, level=None, detail=f"Palestrina, {p.work}, {p.title}: the top voice alone, sung from the encoding")}}


def compute_madrigal() -> dict:
    _, _, mon = corpus()
    p = [x for x in mon if x.book == 3][0]
    ex = excerpt(p, 8)
    c = sing(ex, 0.3)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["m"])
    return {"name": p.name, "title": p.title, "voices": [rows(v) for v in ex], "quarter": 0.3,
            "clips": {"opening": save("madrigal.opening", s_, level=None, detail=f"Monteverdi, Book 3 (1592), {p.name}: the opening, sung from the encoding")}}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation24", 24)


ITEMS = {"hook": compute_hook, "thirds": compute_thirds, "imitation": compute_imitation, "masses": compute_masses, "fauxbourdon": compute_fauxbourdon, "line": compute_line, "madrigal": compute_madrigal,
         "dissonance": compute_dissonance, "kinds": compute_kinds, "melody": compute_melody, "style": compute_style, "quiz": compute_quiz,
         "cruda": compute_cruda, "tuning": compute_tuning, "chromatic": compute_chromatic, "tune": compute_tune, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
