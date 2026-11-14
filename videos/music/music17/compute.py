"""Precompute everything numerical, and every sound, in Part 17 of *Music, Built* ("Four Voices").

    python -m videos.music.music17.compute              # everything missing (a few minutes)
    python -m videos.music.music17.compute --force evaluation

Numbers are cached in ``.cache/music17/<name>.json``, sounds in ``.cache/music17/audio/``.  The chorales are
Monochord's table (``explainer/music/monochord/chorales.py``, derived from the music21 corpus encodings), the rules
and the harmonizer are ``explainer/music/monochord/fourpart.py``, the choir is
``explainer/music/monochord/instruments/choir.py``; published findings are cited in the README.

Items:
    hook        the Passion Chorale's first two phrases: the tune alone, Bach's setting, a chord-chooser's
    book        the chorales as a collection: keys, metres, phrases, tunes set more than once; one tune, two settings
    ranges      where each voice sings; spacing, crossing and doubling, counted
    motion      how each voice moves; the alto alone; how close Bach comes to the shortest way
    rules       the rules of four-part writing, each shown with a pair of chords, wrong and right
    census      how often Bach does what the rules forbid; two of his parallel fifths, heard
    vocab       the chords on the beats: how often each, what follows what, how often the chord changes
    cadences    the chords at the fermatas; the Picardy third; three cadences heard
    decoration  passing and neighbouring notes in the chorales; one phrase with and without them
    harmonizer  the lattice of chords and voicings under one melody; plain and full
    evaluation  ours against Bach on 84 chorales whose tunes the model never saw; an ear question
    improve     ours with passing notes added by rule
    tune        Variation 17: the Tune as a chorale, first by the chord-chooser, then corrected
    variation   the Variations ledger, row 17
    more        the hook's chorale complete; figured bass; the Phrygian half cadence
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import choir
from explainer.music.monochord.partkit import organ_tone, saver

CACHE = Cache("music17")
CLIPS = ClipStore("music17")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
BEAT = 0.72                                          # seconds to a quarter note
PAUSE = 0.8                                          # quarters added after a fermata
T = BC.TICKS
HOOK = "bwv244.62"                                   # the last setting of the Passion Chorale, in the St Matthew Passion
OFFSET = 2                                           # the split that holds out the Passion Chorale's tune
_BOOK: list = []


def book():
    if not _BOOK:
        _BOOK.extend(BC.load())
    return _BOOK


def chorale(name):
    return next(c for c in book() if c.name == name)


def models(train=None):
    train = book() if train is None else train
    return {"major": F.ChordModel(train, "major"), "minor": F.ChordModel(train, "minor")}


# ---------------------------------------------------------------------------
# Sound
# ---------------------------------------------------------------------------
def warp(voices, fermatas) -> callable:
    """Ticks to seconds, with a pause after each fermata."""
    ends = sorted(fermatas)

    def sec(t):
        return t / T * BEAT + PAUSE * BEAT * sum(1 for e in ends if e < t)
    return sec


def fermata_ends(voices) -> list[int]:
    return sorted({o + d for p, o, d, f in voices[0] if f})


def sing(voices, which=(0, 1, 2, 3), organ: bool = False) -> tuple[Clip, list]:
    """Some of four voices (lists of (key, onset tick, duration ticks, fermata)), sung by the choir (or on organ
    tones), with fermata pauses, starting at the first note.  Also the start time (s) of every note, voice by voice."""
    base = min(o for v in voices for _, o, _, _ in v)
    voices = [[(p, o - base, d, f) for p, o, d, f in v] for v in voices]
    ends = fermata_ends(voices)
    sec = warp(voices, ends)
    parts = ("soprano", "alto", "tenor", "bass")
    outs, times = [], []
    for j in which:
        notes = []
        for p, o, d, f in voices[j]:
            a, b = sec(o), sec(o + d)
            if f or (o + d) in ends:
                b += PAUSE * BEAT * 0.9
            notes.append((int(p), a, b - a))
        times.append([n[1] for n in notes])
        if organ:
            y = np.zeros(int((max(a + d for _, a, d in notes) + 0.6) * SR))
            for m, a, d in notes:
                tone = organ_tone(choir.hz(m), d + 0.05, partials=6, rolloff=0.7)
                i = int(a * SR)
                y[i:i + len(tone)] += tone[: len(y) - i] * 0.25
            outs.append(y)
        else:
            outs.append(choir.sing(notes, parts[j], seed=j) * 10 ** ((0.0, -2.0, -2.0, -1.0)[j] / 20))
    n = max(len(o) for o in outs)
    y = np.zeros(n)
    for o in outs:
        y[: len(o)] += o
    c = Clip(y / max(np.abs(y).max(), 1e-12), SR).fade(0.01, 0.3).at_level(LEVEL)
    return c, times


def cut(voices, t0: int, t1: int) -> list:
    """The notes sounding in [t0, t1), shifted to start at 0 and cut to the window."""
    out = []
    for v in voices:
        out.append([(p, max(o, t0) - t0, min(o + d, t1) - max(o, t0), f) for p, o, d, f in v if o < t1 and o + d > t0])
    return out


def rows(voices) -> list:
    return [[[int(p), int(o), int(d), int(f)] for p, o, d, f in v] for v in voices]


def from_chords(chords, soprano_voice=None, beat_ticks: int = T, ferm=(), lengths=None) -> list:
    """Four voices from one chord a beat (or ``lengths`` ticks each); repeated notes are held in the lower three
    voices (the soprano, which carries the words, sings each again).  With
    ``soprano_voice``, the soprano is that voice's notes as written instead."""
    out = [[], [], [], []]
    starts = np.concatenate([[0], np.cumsum(lengths)]).astype(int) if lengths is not None else [k * beat_ticks for k in range(len(chords) + 1)]
    for k, ch in enumerate(chords):
        at, ln = int(starts[k]), int(starts[k + 1] - starts[k])
        for j in range(4):
            if soprano_voice is not None and j == 0:
                continue
            p = int(ch[j])
            f = k in ferm
            if j > 0 and out[j] and out[j][-1][0] == p and out[j][-1][1] + out[j][-1][2] == at and not out[j][-1][3]:
                q, o, d, ff = out[j][-1]
                out[j][-1] = (q, o, d + ln, f)
            else:
                out[j].append((p, at, ln, f))
    if soprano_voice is not None:
        out[0] = list(soprano_voice)
    return out


def beat_soprano(c, t1=None):
    b = [x for x in c.beats() if t1 is None or x[0] < t1]
    sop = [ch[0] for _, ch, _ in b]
    ferm = [k for k, (_, _, f) in enumerate(b) if f]
    first = b[0][0]
    return sop, ferm, first


def phrase_end(c, n: int) -> int:
    """The tick just after the soprano's ``n``-th fermata note ends."""
    fs = [(o, d) for p, o, d, f in c.voices[0] if f]
    o, d = fs[n - 1]
    return o + d


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    c = chorale(HOOK)
    t1 = phrase_end(c, 2)
    bach = cut(c.voices, 0, t1)
    train, test = BC.split(book(), offset=OFFSET)
    mods = models(train)
    sop, ferm, first = beat_soprano(c, t1)
    m = mods[c.mode]
    plain = F.harmonize(sop, c.tonic, m, fermatas=ferm, plain=True)
    full = F.harmonize(sop, c.tonic, m, fermatas=ferm)
    shift = lambda vs: [[(p, o + first, d, f) for p, o, d, f in v] for v in vs]                 # noqa: E731
    ours_plain = shift(from_chords(plain["chords"], ferm=ferm))
    ours_plain[0] = bach[0]
    ours_full = shift(from_chords(full["chords"], ferm=ferm))
    ours_full[0] = bach[0]
    alone, ta = sing(bach, which=(0,))
    sb, tb = sing(bach)
    sp, tp = sing(ours_plain)
    seq = concat([alone, sb, sp], gap=1.2, names=["alone", "bach", "plain"])
    par_plain = [k + 1 for k, (a, b) in enumerate(zip(plain["chords"], plain["chords"][1:])) if F.parallels(a, b)]
    return {"name": HOOK, "tonic": c.tonic, "mode": c.mode, "fifths": c.fifths, "bach": rows(bach), "plain": rows(ours_plain), "full": rows(ours_full),
            "plain_chords": [list(x) for x in plain["chords"]], "full_chords": [list(x) for x in full["chords"]], "first": first,
            "plain_roman": [m.name(s) for s in plain["states"]], "full_roman": [m.name(s) for s in full["states"]],
            "parallels_plain": par_plain, "parallels_full": [k + 1 for k, (a, b) in enumerate(zip(full["chords"], full["chords"][1:])) if F.parallels(a, b)],
            "times": {"alone": ta, "bach": tb, "plain": tp}, "starts": {k: float(seq.events[k]) for k in ("alone", "bach", "plain")},
            "clips": {"three": save("hook.three", seq, level=None, detail="the Passion Chorale's first two phrases: the tune alone; Bach's setting (1727); a chord-chooser's: a model choir")}}


def compute_book() -> dict:
    b = book()
    groups = BC.tunes(b)
    sizes = Counter(len(g) for g in groups.values())
    passion = next(g for g in groups.values() if any(c.name == HOOK for c in g))
    lengths = [c.length / T for c in b]
    phrases = [len(c.phrases()) for c in b]
    # one tune, two settings: the Passion Chorale the first and the last time it is sung in the St Matthew Passion
    two = []
    for name in ("bwv244.15", "bwv244.62"):
        c = chorale(name)
        two.append(cut(c.voices, 0, phrase_end(c, 1)))
    ca, ta = sing(two[0])
    cb, tb = sing(two[1])
    seq = concat([ca, cb], gap=1.2, names=["a", "b"])
    return {"count": len(b), "modes": dict(Counter(c.mode for c in b)), "metres": {f"{k[0]}/{k[1]}": v for k, v in Counter(c.time for c in b).items()},
            "tunes": len(groups), "set_once": sizes[1], "set_more": len(groups) - sizes[1], "passion": sorted(c.name for c in passion),
            "beats_mean": float(np.mean(lengths)), "phrases_mean": float(np.mean(phrases)), "notes": int(sum(len(v) for c in b for v in c.voices)),
            "two": {"names": ["bwv244.15", "bwv244.62"], "voices": [rows(v) for v in two], "keys": [chorale(n).fifths for n in ("bwv244.15", "bwv244.62")]},
            "times": {"a": ta, "b": tb}, "starts": {k: float(seq.events[k]) for k in "ab"},
            "clips": {"two": save("book.two", seq, level=None, detail="the Passion Chorale's first phrase in two of Bach's settings (St Matthew Passion, 1727): a model choir")}}


def compute_ranges() -> dict:
    b = book()
    allp = [[p for c in b for p, _, _, _ in c.voices[j]] for j in range(4)]
    pct = [[int(np.percentile(x, 1)), int(np.percentile(x, 99)), int(min(x)), int(max(x)), float(np.median(x))] for x in allp]
    outside = [float(np.mean([(p < lo) or (p > hi) for p in x])) for x, (lo, hi) in zip(allp, F.RANGES)]
    hist = [np.bincount(np.array(x) - 30, minlength=60)[:60].tolist() for x in allp]
    gaps = {"S-A": [], "A-T": [], "T-B": []}
    dbl = Counter()
    for c in b:
        for _, ch, _ in F.verticals(c):
            if ch[0] >= ch[1] >= ch[2] >= ch[3]:
                gaps["S-A"].append(ch[0] - ch[1])
                gaps["A-T"].append(ch[1] - ch[2])
                gaps["T-B"].append(ch[2] - ch[3])
        for x in F.beat_labels(c):
            lab = x["label"]
            if lab and lab[1] in ("major", "minor"):
                d = F.doubled(x["chord"], ((lab[0] + c.tonic) % 12, lab[1], lab[2]))
                dbl[f"{lab[2]}:{d}"] += 1
    over = {k: float(np.mean(np.array(v) > 12)) for k, v in gaps.items()}
    return {"ranges": pct, "textbook": [list(r) for r in F.RANGES], "outside": outside, "hist": hist, "hist_lo": 30,
            "gap_mean": {k: float(np.mean(v)) for k, v in gaps.items()}, "gap_over_octave": over, "doubling": dict(dbl)}


def compute_motion() -> dict:
    b = book()
    mv = [[abs(v[k + 1][0] - v[k][0]) for c in b for v in [c.voices[j]] for k in range(len(v) - 1)] for j in range(4)]
    stats = [{"mean": float(np.mean(x)), "step": float(np.mean(np.array(x) <= 2)), "repeat": float(np.mean(np.array(x) == 0)), "leap": float(np.mean(np.array(x) > 7))} for x in mv]
    # the shortest way: Bach's alto and tenor motion against the least possible for the same next chord, soprano and bass
    actual, least = [], []
    for c in b[::3]:
        labs = F.beat_labels(c)
        for x, y in zip(labs, labs[1:]):
            if not x["label"] or not y["label"]:
                continue
            a, ch = x["chord"], y["chord"]
            pcs = {p % 12 for p in ch}
            best = None
            for al in range(F.RANGES[1][0], F.RANGES[1][1] + 1):
                if al % 12 not in pcs or al > ch[0]:
                    continue
                for te in range(F.RANGES[2][0], F.RANGES[2][1] + 1):
                    if te % 12 not in pcs or te > al or te < ch[3]:
                        continue
                    if {ch[0] % 12, al % 12, te % 12, ch[3] % 12} != pcs:
                        continue
                    m = abs(al - a[1]) + abs(te - a[2])
                    best = m if best is None else min(best, m)
            if best is not None:
                actual.append(abs(ch[1] - a[1]) + abs(ch[2] - a[2]))
                least.append(best)
    c = chorale(HOOK)
    alto = cut(c.voices, 0, phrase_end(c, 2))
    ca, ta = sing(alto, which=(1,))
    cs, ts = sing(alto, which=(0, 1))
    seq = concat([ca, cs], gap=1.2, names=["alto", "with"])
    return {"stats": stats, "shortest": {"actual": float(np.mean(actual)), "least": float(np.mean(least)), "same": float(np.mean(np.array(actual) == np.array(least))),
                                         "within2": float(np.mean(np.array(actual) - np.array(least) <= 2)), "n": len(actual)},
            "alto": rows(alto), "times": {"alto": ta, "with": ts}, "starts": {k: float(seq.events[k]) for k in ("alto", "with")},
            "clips": {"alto": save("motion.alto", seq, level=None, detail="the alto of the Passion Chorale's first two phrases alone; then with the soprano")}}


def compute_rules() -> dict:
    """Four rules, each as two chords done wrong and then right, in C major."""
    demos = {
        "parallel": {"wrong": [(67, 64, 60, 48), (69, 65, 62, 50)], "right": [(67, 64, 60, 48), (65, 62, 57, 50)],
                     "text": "parallel fifths and octaves"},
        "leading": {"wrong": [(71, 67, 62, 43), (67, 64, 60, 48)], "right": [(71, 67, 62, 43), (72, 64, 60, 48)],
                    "text": "the leading note rises to the tonic"},
        "seventh": {"wrong": [(71, 65, 62, 43), (72, 67, 64, 48)], "right": [(71, 65, 62, 43), (72, 64, 60, 48)],
                    "text": "a seventh falls by step"},
        "spacing": {"wrong": [(79, 64, 55, 48), (81, 65, 60, 41)], "right": [(67, 64, 60, 48), (69, 65, 60, 53)],
                    "text": "upper voices within an octave of each other"},
    }
    clips, out, starts = {}, {}, {}
    for name, d in demos.items():
        parts = []
        for which in ("wrong", "right"):
            chs = d[which]
            vs = [[(int(ch[j]), 2 * T * k, 2 * T, 0) for k, ch in enumerate(chs)] for j in range(4)]
            c, _ = sing(vs, organ=True)
            parts.append(c)
        seq = concat(parts, gap=0.7, names=["wrong", "right"])
        clips[name] = save(f"rules.{name}", seq, level=None, detail=f"{d['text']}: two chords done wrong, then right: organ tones")
        starts[name] = {k: float(seq.events[k]) for k in ("wrong", "right")}
        out[name] = {"wrong": [list(x) for x in d["wrong"]], "right": [list(x) for x in d["right"]], "text": d["text"],
                     "wrong_par": [[list(p_), k] for p_, k in F.parallels(*d["wrong"])], "right_par": [[list(p_), k] for p_, k in F.parallels(*d["right"])],
                     "spacing": {w: [F.spacing_ok(x) for x in d[w]] for w in ("wrong", "right")}}
    return {"demos": out, "starts": starts, "clips": clips}


def compute_census() -> dict:
    b = book()
    r = F.rule_census(b)
    # where Bach's parallels fall: on the beat or between beats
    on, off = 0, 0
    for e in r["examples"]:
        if e["tick"] % T == 0:
            on += 1
        else:
            off += 1
    allpar = []
    for c in b:
        vs = F.verticals(c)
        for (t0, a, _), (t1, bb, _) in zip(vs, vs[1:]):
            for pair, kind in F.parallels(a, bb):
                allpar.append({"chorale": c.name, "t0": int(t0), "t1": int(t1), "pair": F.PAIR_NAMES[pair], "kind": kind, "from": list(a), "to": list(bb),
                               "on_beat": bool(t0 % T == 0 and t1 % T == 0)})
    pairs = Counter(p["pair"] for p in allpar)
    # two to hear: on the beat, between the outer or a clear pair
    pick = ([p for p in allpar if p["on_beat"] and p["kind"] == "fifths"] + [p for p in allpar if not p["on_beat"]])[:2]
    clips, ctx = [], []
    for p in pick:
        c = chorale(p["chorale"])
        t0 = max(0, p["t0"] - 2 * T)
        t1 = p["t1"] + 2 * T
        vs = cut(c.voices, t0, t1)
        cl, tm = sing(vs)
        clips.append(cl)
        ctx.append({"name": p["chorale"], "voices": rows(vs), "times": tm, "at": [p["t0"] - t0, p["t1"] - t0], "pair": p["pair"]})
    seq = concat(clips, gap=1.2, names=["a", "b"])
    return {**{k: v for k, v in r.items() if k != "examples"}, "all": allpar, "pairs": dict(pairs), "on_beat": int(sum(p["on_beat"] for p in allpar)),
            "rate": r["moves"] / max(1, sum(r["parallel"].values())), "heard": ctx, "starts": {k: float(seq.events[k]) for k in "ab"},
            "clips": {"two": save("census.two", seq, level=None, detail="two of Bach's parallel fifths, each with a beat or two around it: a model choir")}}


def compute_vocab() -> dict:
    b = book()
    out = {}
    for mode in ("major", "minor"):
        uni, bi = Counter(), Counter()
        none = total = same = pairs = 0
        for c in b:
            if c.mode != mode:
                continue
            labs = F.beat_labels(c)
            prev = None
            for x in labs:
                total += 1
                if x["label"] is None:
                    none += 1
                    prev = None
                    continue
                s = F.roman((x["label"][0], x["label"][1], 0), mode)
                uni[s] += 1
                if prev is not None:
                    bi[(prev, s)] += 1
                    pairs += 1
                    same += prev == s
                prev = s
        top = [s for s, _ in uni.most_common(8)]
        mat = [[bi[(a, c_)] for c_ in top] for a in top]
        out[mode] = {"top": uni.most_common(16), "beats": total, "unlabelled": none, "same_next": same / max(pairs, 1), "matrix_names": top, "matrix": mat,
                     "after": {a: [[c_, n] for (x, c_), n in sorted(bi.items(), key=lambda kv: -kv[1]) if x == a][:4] for a in top[:6]}}
    return out


def compute_cadences() -> dict:
    b = book()
    out = {}
    for mode in ("major", "minor"):
        pairs, finals = Counter(), Counter()
        for c in b:
            if c.mode != mode:
                continue
            labs = F.beat_labels(c)
            fk = [k for k, x in enumerate(labs) if x["fermata"]]
            for k in fk:
                if k == 0:
                    continue
                a, z = labs[k - 1]["label"], labs[k]["label"]
                pairs[(F.roman((a[0], a[1], 0), mode) if a else "–", F.roman((z[0], z[1], 0), mode) if z else "–")] += 1
            last = labs[-1]["label"]
            if last:
                finals[F.roman((last[0], last[1], 0), mode)] += 1
        out[mode] = {"pairs": [[a, z, n] for (a, z), n in pairs.most_common(10)], "total": int(sum(pairs.values())), "finals": dict(finals)}
    # three cadences heard: an authentic, a half and a Picardy ending, from the chorales themselves
    picks = {}
    for c in b:
        labs = F.beat_labels(c)
        fk = [k for k, x in enumerate(labs) if x["fermata"]]
        for k in fk[:-1]:
            if k < 2:
                continue
            a, z = labs[k - 1]["label"], labs[k]["label"]
            if not a or not z:
                continue
            if c.mode == "major" and "authentic" not in picks and a[:2] == (7, "major") and z[:2] == (0, "major") and z[2] == 0:
                picks["authentic"] = (c, labs[k - 2]["tick"], labs[k]["tick"] + T)
            if c.mode == "major" and "half" not in picks and z[:2] == (7, "major") and a[:2] in ((2, "major"), (5, "major")):
                picks["half"] = (c, labs[k - 2]["tick"], labs[k]["tick"] + T)
        if c.mode == "minor" and "picardy" not in picks and labs[-1]["label"] and labs[-1]["label"][:2] == (0, "major"):
            picks["picardy"] = (c, labs[-3]["tick"], c.length)
    clips, heard = [], {}
    for name in ("authentic", "half", "picardy"):
        c, t0, t1 = picks[name]
        vs = cut(c.voices, t0, t1)
        cl, tm = sing(vs)
        clips.append(cl)
        heard[name] = {"chorale": c.name, "voices": rows(vs), "times": tm}
    seq = concat(clips, gap=1.0, names=list(heard))
    return {**out, "heard": heard, "starts": {k: float(seq.events[k]) for k in heard},
            "clips": {"three": save("cadences.three", seq, level=None, detail="three cadences from Bach's chorales: authentic, half, and a minor chorale's major last chord")}}


def classify_decorations(c) -> Counter:
    """Each note that begins off the beat, by how it moves: passing (step in, step on, same way), neighbour (step
    out and back), other (a leap, or a chord note)."""
    out = Counter()
    for j, v in enumerate(c.voices):
        for k in range(1, len(v) - 1):
            p, o, d, _ = v[k]
            if o % T == 0:
                continue
            a, z = v[k - 1][0], v[k + 1][0]
            i, e = p - a, z - p
            if 0 < abs(i) <= 2 and 0 < abs(e) <= 2:
                out[(j, "passing" if (i > 0) == (e > 0) else "neighbour")] += 1
            else:
                out[(j, "other")] += 1
    return out


def compute_decoration() -> dict:
    b = book()
    tot = Counter()
    beats = 0
    decorated = 0
    for c in b:
        tot.update(classify_decorations(c))
        bt = c.beats()
        beats += len(bt)
        onsets = {o for v in c.voices for _, o, _, _ in v}
        decorated += sum(1 for t, _, _ in bt if any(t < x < t + T for x in onsets))
    per = {j: {k: int(tot[(j, k)]) for k in ("passing", "neighbour", "other")} for j in range(4)}
    c = chorale(HOOK)
    t1 = phrase_end(c, 2)
    full = cut(c.voices, 0, t1)
    sop, ferm, first = beat_soprano(c, t1)
    chords = [ch for t, ch, f in c.beats() if t < t1]
    block = from_chords(chords, ferm=ferm)
    block = [[(p, o + first, d, f) for p, o, d, f in v] for v in block]
    cA, tA = sing(block)
    cB, tB = sing(full)
    seq = concat([cA, cB], gap=1.2, names=["A", "B"])
    return {"per_voice": per, "beats": beats, "decorated": decorated, "share": decorated / beats, "block": rows(block), "full": rows(full),
            "times": {"A": tA, "B": tB}, "starts": {k: float(seq.events[k]) for k in "AB"}, "answer": "B",
            "clips": {"quiz": save("decoration.quiz", seq, level=None, detail="the Passion Chorale's first two phrases: Bach's chords on the beats only; then as he wrote them")}}


def compute_harmonizer() -> dict:
    c = chorale(HOOK)
    t1 = phrase_end(c, 2)
    sop, ferm, first = beat_soprano(c, t1)
    train, _ = BC.split(book(), offset=OFFSET)
    m = models(train)[c.mode]
    lead = (c.tonic + 11) % 12
    sizes, chords_per = [], []
    for s in sop:
        deg = (s - c.tonic) % 12
        n_ch = n_v = 0
        for si in np.argsort(-m.E[:, deg])[:14]:
            mem = m.members(m.states[si])
            if deg in mem:
                v = len(F.voicings_under(s, mem, c.tonic, lead))
                if v:
                    n_ch += 1
                    n_v += v
        sizes.append(n_v)
        chords_per.append(n_ch)
    import time
    t = time.time()
    full = F.harmonize(sop, c.tonic, m, fermatas=ferm)
    secs = time.time() - t
    paths = float(np.sum(np.log10(sizes)))
    return {"beats": len(sop), "states": sizes, "chords": chords_per, "log10_paths": paths, "seconds": secs, "vocab": len(m.states),
            "vocab_names": [m.name(s) for s in m.states], "weights": F.DEFAULT_WEIGHTS, "full_roman": [m.name(s) for s in full["states"]],
            "bach_roman": [F.roman(x["label"], c.mode, figures=False) if x["label"] else "–" for x in F.beat_labels(c) if x["tick"] < t1]}


def compute_evaluation() -> dict:
    train, test = BC.split(book(), offset=OFFSET)
    mods = models(train)
    res = {"full": [], "plain": []}
    per = []
    for c in test:
        if c.mode not in mods:
            continue
        B = F.bach_on_beats(c)
        try:
            full = F.harmonize(B["soprano"], c.tonic, mods[c.mode], fermatas=B["fermatas"])
            plain = F.harmonize(B["soprano"], c.tonic, mods[c.mode], fermatas=B["fermatas"], plain=True)
        except ValueError:
            continue
        ef, ep = F.evaluate(full, B), F.evaluate(plain, B)
        res["full"].append(ef)
        res["plain"].append(ep)
        per.append({"name": c.name, "beats": len(B["soprano"]), "same_chord": ef["same_chord"], "same_bass": ef["same_bass"]})

    def agg(rs):
        moves = sum(1 for _ in rs)
        return {"same_chord": float(np.mean([r["same_chord"] for r in rs])), "same_bass": float(np.mean([r["same_bass"] for r in rs])),
                "parallels": int(sum(r["ours"]["parallels"] for r in rs)), "hidden": int(sum(r["ours"]["hidden"] for r in rs)),
                "inner_motion": float(np.mean([r["ours"]["inner_motion"] for r in rs])), "n": moves}
    bach = {"parallels": int(sum(r["bach"]["parallels"] for r in res["full"])), "hidden": int(sum(r["bach"]["hidden"] for r in res["full"])),
            "inner_motion": float(np.mean([r["bach"]["inner_motion"] for r in res["full"]]))}
    beats = int(sum(p["beats"] for p in per))
    # the ear question: Bach and ours on the hook chorale's third and fourth phrases, in an order the listener must decide
    c = chorale(HOOK)
    t0, t1 = phrase_end(c, 2), phrase_end(c, 4)
    sub = [x for x in c.beats() if t0 <= x[0] < t1]
    sop = [ch[0] for _, ch, _ in sub]
    ferm = [k for k, x in enumerate(sub) if x[2]]
    full = F.harmonize(sop, c.tonic, mods[c.mode], fermatas=ferm)
    bachv = cut(c.voices, t0, t1)
    first = sub[0][0] - t0
    ours = from_chords(full["chords"], ferm=ferm)
    ours = [[(p, o + first, d, f) for p, o, d, f in v] for v in ours]
    ours[0] = bachv[0]
    ca, ta = sing(ours)
    cb, tb = sing(bachv)
    seq = concat([ca, cb], gap=1.2, names=["A", "B"])
    return {"test": len(per), "train": len(train), "beats": beats, "full": agg(res["full"]), "plain": agg(res["plain"]), "bach": bach, "per": per,
            "quiz": {"A": rows(ours), "B": rows(bachv), "answer": "B", "times": {"A": ta, "B": tb}, "starts": {k: float(seq.events[k]) for k in "AB"},
                     "roman_ours": [mods[c.mode].name(s) for s in full["states"]]},
            "clips": {"quiz": save("evaluation.quiz", seq, level=None, detail="the Passion Chorale's third and fourth phrases, harmonized twice: ours, then Bach's")}}


def decorate(voices, tonic: int, mode: str) -> list:
    """Passing notes added by rule: where an alto, tenor or bass note moves a third to the next beat, split it into
    two eighths, the second a step between, if that makes no parallel fifths or octaves with any other voice."""
    scale = {(tonic + s) % 12 for s in (F.MAJOR if mode == "major" else (0, 2, 3, 5, 7, 8, 10, 11))}
    out = [list(v) for v in voices]
    for j in (1, 2, 3):
        new = []
        v = out[j]
        for k, (p, o, d, f) in enumerate(v):
            nxt = v[k + 1] if k + 1 < len(v) else None
            if nxt is None or d != T or f or abs(nxt[0] - p) not in (3, 4):
                new.append((p, o, d, f))
                continue
            step = 1 if nxt[0] > p else -1
            mid = next((q for q in range(p + step, nxt[0], step) if q % 12 in scale), None)
            if mid is None:
                new.append((p, o, d, f))
                continue
            ok = True
            t = o + T // 2
            for i in range(4):
                if i == j:
                    continue
                oi = next(((q, a, dd) for q, a, dd, _ in out[i] if a <= t < a + dd), None)
                oa = next(((q, a, dd) for q, a, dd, _ in out[i] if a <= o < a + dd), None)
                if oi is None or oa is None:
                    continue
                for (x0, x1, y0, y1) in ((p, mid, oa[0], oi[0]),):
                    if x0 != x1 and y0 != y1 and (x0 - y0) % 12 == (x1 - y1) % 12 and (x0 - y0) % 12 in (0, 7) and np.sign(x1 - x0) == np.sign(y1 - y0):
                        ok = False
                if (mid - oi[0]) % 12 in (1, 11) and abs(mid - oi[0]) < 3:
                    ok = False
            if ok:
                new += [(p, o, T // 2, False), (mid, o + T // 2, T // 2, False)]
            else:
                new.append((p, o, d, f))
        out[j] = new
    return out


def compute_improve() -> dict:
    ev = load("evaluation")
    ours = [[tuple(n) for n in v] for v in ev["quiz"]["A"]]
    c = chorale(HOOK)
    dec = decorate(ours, c.tonic, c.mode)
    added = sum(len(a) - len(b) for a, b in zip(dec, ours))
    cl, tm = sing(dec)
    seq = concat([cl], gap=0.0, names=["dec"])
    # over all held-out chorales: notes a beat in the lower three voices, before and after
    train, test = BC.split(book(), offset=OFFSET)
    mods = models(train)
    before, after, bach = [], [], []
    for c2 in test[::3]:
        B = F.bach_on_beats(c2)
        try:
            full = F.harmonize(B["soprano"], c2.tonic, mods[c2.mode], fermatas=B["fermatas"])
        except ValueError:
            continue
        vs = from_chords(full["chords"], ferm=B["fermatas"])
        d2 = decorate(vs, c2.tonic, c2.mode)
        n = len(full["chords"])
        before.append(sum(len(v) for v in vs[1:]) / (3 * n))
        after.append(sum(len(v) for v in d2[1:]) / (3 * n))
        bach.append(sum(len(v) for v in c2.voices[1:]) / (3 * max(1, len(B["soprano"]))))
    return {"voices": rows(dec), "added": int(added), "times": tm, "notes_per_beat": {"ours": float(np.mean(before)), "decorated": float(np.mean(after)), "bach": float(np.mean(bach))},
            "clips": {"decorated": save("improve.decorated", seq, level=None, detail="our harmonization of the third and fourth phrases, with passing notes added by rule")}}


def compute_tune() -> dict:
    """Variation 17: the Tune as a chorale melody, one chord to a note, a fermata at the end of each phrase; first
    by the chord-chooser alone, then by the full harmonizer, which corrects it."""
    tune = M.corpus()[0]
    sop = [72 + p for p in tune.pitches]
    ferm = [k for k, b in enumerate(tune.beats) if b >= 2]
    m = models()["major"]
    plain = F.harmonize(sop, 0, m, fermatas=ferm, plain=True)
    full = F.harmonize(sop, 0, m, fermatas=ferm)
    lengths = [int(b * T) for b in tune.beats]
    vp = from_chords(plain["chords"], ferm=ferm, lengths=lengths)
    vf = from_chords(full["chords"], ferm=ferm, lengths=lengths)
    cp, tp = sing(vp)
    cf, tf = sing(vf)
    seq = concat([cp, cf], gap=1.5, names=["plain", "full"])
    changed = [k for k, (a, b) in enumerate(zip(plain["chords"], full["chords"])) if tuple(a) != tuple(b)]
    pp = [k + 1 for k, (a, b) in enumerate(zip(plain["chords"], plain["chords"][1:])) if F.parallels(a, b)]
    pf = [k + 1 for k, (a, b) in enumerate(zip(full["chords"], full["chords"][1:])) if F.parallels(a, b)]
    return {"soprano": sop, "fermatas": ferm, "plain": [list(x) for x in plain["chords"]], "full": [list(x) for x in full["chords"]],
            "plain_roman": [m.name(s) for s in plain["states"]], "full_roman": [m.name(s) for s in full["states"]], "changed": changed,
            "parallels_plain": pp, "parallels_full": pf, "voices_plain": rows(vp), "voices_full": rows(vf), "times": {"plain": tp, "full": tf},
            "starts": {k: float(seq.events[k]) for k in ("plain", "full")}, "seconds": seq.duration,
            "clip": {"name": "tune.variation17", "seconds": seq.duration},
            "clips": {"variation": save("tune.variation17", seq, level=None, detail="the Tune as a chorale: the chord-chooser's setting, then the harmonizer's: a model choir")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 17, "title": r"as a chorale for four voices: chosen chord by chord, then corrected by the rules", "seconds": round(t["seconds"], 2),
            "measure": rf"parallel fifths and octaves: {len(t['parallels_plain'])} before the corrections, {len(t['parallels_full'])} after",
            "clip": "tune.variation17"}


def compute_more() -> dict:
    """The hook's chorale complete; figured bass on its beats and across the chorales; the Phrygian half cadence."""
    from explainer.music.monochord import chords as CH
    from explainer.music.monochord.score import Pitch
    c = chorale(HOOK)
    whole, tw = sing(c.voices)
    seq = concat([whole], gap=0.0, names=["whole"])
    beats = [x for x in c.beats() if x[0] < phrase_end(c, 2)]
    figs = [CH.figure_name([Pitch.from_midi(int(p)) for p in ch]) for _, ch, _ in beats]
    allfig = Counter()
    for x in book():
        for _, ch, _ in x.beats():
            allfig[CH.figure_name([Pitch.from_midi(int(p)) for p in ch])] += 1
    phry, examples = 0, []
    minor_fermatas = 0
    for x in book():
        if x.mode != "minor":
            continue
        labs = F.beat_labels(x)
        for k, y in enumerate(labs):
            if not y["fermata"] or k == 0:
                continue
            minor_fermatas += 1
            a, z = labs[k - 1]["label"], y["label"]
            if a and z and z[:2] == (7, "major") and a[:2] == (5, "minor") and a[2] == 1:
                phry += 1
                examples.append([x.name, int(labs[k - 1]["tick"]), list(labs[k - 1]["chord"]), list(y["chord"])])
    tot = sum(allfig.values())
    return {"voices": rows(c.voices), "times": tw, "seconds": whole.duration, "figures": figs, "bass": [int(ch[3]) for _, ch, _ in beats],
            "figure_shares": [[k, v / tot] for k, v in allfig.most_common(8)], "phrygian": phry, "phrygian_examples": examples[:5],
            "minor_fermatas": minor_fermatas,
            "clips": {"whole": save("more.whole", seq, level=None, detail="Bach's last setting of the Passion Chorale (St Matthew Passion, 1727), complete: a model choir")}}


ITEMS = {"hook": compute_hook, "book": compute_book, "ranges": compute_ranges, "motion": compute_motion, "rules": compute_rules, "census": compute_census,
         "vocab": compute_vocab, "cadences": compute_cadences, "decoration": compute_decoration, "harmonizer": compute_harmonizer,
         "evaluation": compute_evaluation, "improve": compute_improve, "tune": compute_tune, "variation": compute_variation, "more": compute_more}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
