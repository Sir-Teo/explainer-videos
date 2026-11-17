"""Precompute everything numerical, and every sound, in Part 26 of *Music, Built* ("The Classical Style").

    python -m videos.music.music26.compute              # everything missing (several minutes: the bowed strings)
    python -m videos.music.music26.compute --force style

Numbers are cached in ``.cache/music26/<name>.json``, sounds in ``.cache/music26/audio/``.  The measures are Monochord's
(``explainer/music/monochord/classical.py``, with Part 24's stylometric test and Part 15's key tracker); the music is the
string quartet movements of Haydn, Mozart and Beethoven in the music21 corpus (``baroque.load_quartets``), excerpts played
by Part 7's bowed string on its violin body; the Tune's variations are played on Part 7's piano.  Mozart's K. 265 is not
in the corpus, so the film does not measure it; it measures the quartets instead and says so.

Items:
    hook        the Tune with a plain Classical accompaniment, on the piano
    phrases     an antecedent and two consequents (an ear question: which phrase is complete?); cadence gaps in the corpus
    plan        Haydn's Op. 74 No. 1, first movement: its tonal plan; the second theme in the exposition and the
                recapitulation (an ear question)
    texture     who leads in each bar; Mozart's 'Hunt' quartet opening, heard
    figures     the Tune over three accompaniments: block chords, an Alberti bass, repeated notes
    three       Haydn, Mozart and Beethoven: lengths, ranges, an excerpt of each (an ear question: which is Beethoven?)
    style       the fair attribution test: Part 24's features against the Classical ones
    keys        the second key of every movement (a census); Beethoven's Op. 59 No. 2 finale, which opens in the wrong key
    minuet      Haydn's Op. 74 No. 1, the minuet's first strain, heard
    tune        Variation 26: theme, minore, adagio, finale
    variation   the Variations ledger, row 26
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import baroque as B
from explainer.music.monochord import classical as CL
from explainer.music.monochord import melody as M
from explainer.music.monochord import palestrina as PS
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.physics.string import String
from explainer.music.monochord.partkit import saver, signoff
from explainer.music.monochord.trecento import Piece

CACHE = Cache("music26")
CLIPS = ClipStore("music26")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
VIOLIN = STR.violin_body()
C4 = 261.6255653005986
_V: dict = {}
_P: dict = {}


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def bowed(m: float, seconds: float) -> Clip:
    key = (round(m, 2), round(min(seconds, 2.4), 2))
    if key not in _V:
        y = VIOLIN.play(STR.bowed_note(hz(m), max(min(seconds, 2.4), 0.1)))
        _V[key] = Clip(np.asarray(y, dtype=float)).fade(0.008, 0.05).at_level(LEVEL)
    return _V[key]


def piano(m: float, seconds: float, velocity: float = 1.3) -> Clip:
    key = (round(m, 2), round(seconds, 2), velocity)
    if key not in _P:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=velocity, seconds=seconds + 0.3))
        _P[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _P[key]


def place(lines, inst, unit: float, gains=None, tail: float = 1.0) -> Clip:
    gains = gains or [0.0] * len(lines)
    placed, end = [], 0.0
    for ln, g in zip(lines, gains):
        for p, a, d in ln:
            placed.append((inst(p, d * unit * 1.02), a * unit, g))
            end = max(end, (a + d) * unit)
    return Clip(mix(placed, duration=end + tail).y, SR)


def rows(v):
    return [[float(p), float(a), float(d)] for p, a, d in v]


def movements():
    """Single movements only: four Beethoven files in the corpus hold whole quartets and are left out."""
    return [CL.Movement(r) for r in B.load_quartets() if "movement" in r["name"]]


def excerpt(m, start_bar: int, bars: int):
    lo, hi = start_bar * m.bar, (start_bar + bars) * m.bar
    return [[(p, (o - lo) / 24.0, min(d, hi - o) / 24.0) for p, o, d in v if lo <= o < hi] for v in m.voices]


def tune_line(base: int = 72):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in zip(t.pitches, t.beats):
        out.append((base + p, a, float(d)))
        a += d
    return out


CHORDS = {"I": (48, (60, 64, 67)), "IV": (53, (60, 65, 69)), "V": (43, (59, 62, 67)), "V7": (43, (59, 65, 67)), "vi": (45, (60, 64, 69)),
          "ii": (50, (62, 65, 69)), "i": (48, (60, 63, 67)), "iv": (53, (60, 65, 68)), "VI": (44, (60, 63, 68))}
HARM = ["I", "I", "IV", "I", "V7", "I", "V7", "I", "I", "V7", "I", "V7", "I", "V7", "I", "V7", "I", "I", "IV", "I", "V7", "I", "V7", "I"]


def accompany(kind: str, harmony=HARM, beats: int = 2):
    """Chords two beats each: 'block' chords, 'alberti' (low, high, middle, high in eighths), 'repeated' eighths."""
    out = []
    for k, name in enumerate(harmony):
        bass, (a, b_, c) = CHORDS[name]
        t0 = beats * k
        if kind == "block":
            out += [(bass, t0, beats), (a, t0, beats), (b_, t0, beats), (c, t0, beats)]
        elif kind == "alberti":
            pat = [a, c, b_, c]
            out += [(pat[i % 4] - 12, t0 + 0.5 * i, 0.5) for i in range(int(beats / 0.5))]
        elif kind == "repeated":
            out += [(bass, t0, beats)] + [(x, t0 + 0.5 * i, 0.5) for i in range(int(beats / 0.5)) for x in (b_ - 12, c - 12)]
    return out


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    tl = tune_line()[:14]
    acc = accompany("block", HARM[:8])
    unit = 0.38
    c = place([tl, acc], piano, unit, gains=[0.0, -6.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["theme"])
    return {"melody": rows(tl), "acc": rows(acc), "unit": unit,
            "clips": {"theme": save("hook.theme", s, level=None, detail="the Tune's first strain over plain chords, Part 7's piano")}}


def compute_phrases() -> dict:
    """An antecedent (ends on V, a half cadence) and a consequent (ends on I); the quiz plays two four-bar phrases and
    asks which is complete.  Then the gaps between cadences in the corpus."""
    mel = [(72, 0, 1), (72, 1, 1), (79, 2, 1), (79, 3, 1), (81, 4, 1), (81, 5, 1), (79, 6, 2)]
    ant = mel
    cons = [(72, 0, 1), (72, 1, 1), (79, 2, 1), (79, 3, 1), (77, 4, 1), (76, 5, 1), (74, 6, 1), (72, 7, 1)]
    h_ant = ["I", "I", "IV", "V"]
    h_con = ["I", "I", "V7", "I"]
    unit = 0.42
    cA = place([ant, accompany("block", h_ant)], piano, unit, gains=[0.0, -6.0])
    cB = place([cons, accompany("block", h_con)], piano, unit, gains=[0.0, -6.0])
    s = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    ms = movements()
    gaps = Counter(g for m in ms for g in CL.phrase_gaps(m))
    by = {c: Counter(g for m in ms if m.composer == c for g in CL.phrase_gaps(m)) for c in ("haydn", "mozart", "beethoven")}
    return {"A": rows(ant), "B": rows(cons), "A_acc": rows(accompany("block", h_ant)), "B_acc": rows(accompany("block", h_con)), "unit": unit,
            "starts": {k: float(s.events[k]) for k in "AB"}, "answer": "B",
            "gaps": {str(k): v for k, v in gaps.items()}, "cadences": sum(len(CL.cadences(m)) for m in ms),
            "periodic": {c: sum(v[k] for k in (4, 8)) / max(sum(v.values()), 1) for c, v in by.items()},
            "clips": {"quiz": save("phrases.quiz", s, level=None, detail="two four-bar phrases on the Tune: one ending on the dominant (a half cadence), one on the tonic, Part 7's piano")}}


def compute_plan() -> dict:
    ms = movements()
    m = [x for x in ms if x.name == "opus74no1/movement1"][0]
    tp = CL.tonal_plan(m, window_bars=8, hop_bars=2)
    # the second theme: where the plan first settles in G, and again (in C) after bar 100
    exp = next(t["bar"] for t in tp if t["key"] == [7, "major"] or t["key"] == (7, "major"))
    rec_cands = [t["bar"] for t in tp if t["bar"] > 100 and (t["key"] == (0, "major") or t["key"] == [0, "major"])]
    rec = rec_cands[0] if rec_cands else 110.0
    unit = 0.24
    exA = excerpt(m, int(exp), 6)
    exB = excerpt(m, int(rec), 6)
    cA = place(exA, bowed, unit, gains=[0, -1, -2, -1])
    cB = place(exB, bowed, unit, gains=[0, -1, -2, -1])
    s = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"name": m.name, "bars": m.bars, "plan": [{"bar": t["bar"], "key": list(t["key"])} for t in tp], "exp_bar": exp, "rec_bar": rec,
            "A": [rows(v) for v in exA], "B": [rows(v) for v in exB], "unit": unit, "starts": {k: float(s.events[k]) for k in "AB"}, "answer": "B",
            "clips": {"quiz": save("plan.quiz", s, level=None, detail="Haydn, String Quartet Op. 74 No. 1, first movement, from the encoding: six bars from the exposition, then six from the recapitulation, Part 7's bowed string")}}


def compute_texture() -> dict:
    ms = movements()
    out = {}
    for c in ("haydn", "mozart", "beethoven"):
        sel = [m for m in ms if m.composer == c]
        leads = Counter(j for m in sel for j in CL.lead_voices(m))
        tot = sum(leads.values())
        out[c] = {"shares": [leads[j] / tot for j in range(4)], "changes": float(np.mean([np.mean([a != b for a, b in zip(L, L[1:])]) for L in (CL.lead_voices(m) for m in sel)])),
                  "accompaniment": float(np.mean([CL.accompaniment_bars(m) for m in sel]))}
    m = [x for x in ms if x.name == "k458/movement1"][0]
    ex = excerpt(m, 0, 8)
    unit = 0.2
    c = place(ex, bowed, unit, gains=[0, -1, -2, -1])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["hunt"])
    return {"by": out, "hunt": [rows(v) for v in ex], "unit": unit, "hunt_leads": CL.lead_voices(m)[:8],
            "clips": {"hunt": save("texture.hunt", s, level=None, detail="Mozart, String Quartet K. 458 ('Hunt'), first movement, bars 1-8 from the encoding, Part 7's bowed string")}}


def compute_figures() -> dict:
    tl = tune_line()[:14]
    unit = 0.36
    clips = []
    out = {}
    for kind in ("block", "alberti", "repeated"):
        acc = accompany(kind, HARM[:8])
        clips.append(place([tl, acc], piano, unit, gains=[0.0, -7.0]).at_level(LEVEL))
        out[kind] = rows(acc)
    s = concat(clips, gap=0.9, names=["block", "alberti", "repeated"])
    return {"melody": rows(tl), "acc": out, "unit": unit, "starts": {k: float(s.events[k]) for k in out},
            "clips": {"three": save("figures.three", s, level=None, detail="the Tune's first strain over block chords, an Alberti bass and repeated chords, Part 7's piano")}}


def compute_three() -> dict:
    ms = movements()
    stats = {}
    for c in ("haydn", "mozart", "beethoven"):
        sel = [m for m in ms if m.composer == c]
        stats[c] = {"movements": len(sel), "bars": float(np.mean([m.bars for m in sel])), "span": float(np.mean([CL.features(m)[6] for m in sel])),
                    "longest": max(sel, key=lambda m: m.bars).name, "longest_bars": max(m.bars for m in sel)}
    hay = [x for x in ms if x.name == "opus1no1/movement1"][0]
    bee = [x for x in ms if x.name == "opus59no1/movement1"][0]
    exA = excerpt(hay, 0, 6)
    exB = excerpt(bee, 0, 6)
    cA = place(exA, bowed, 0.22, gains=[0, -1, -2, -1])
    cB = place(exB, bowed, 0.24, gains=[0, -1, -2, -1])
    s = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"stats": stats, "A": [rows(v) for v in exA], "B": [rows(v) for v in exB], "unitA": 0.22, "unitB": 0.24,
            "starts": {k: float(s.events[k]) for k in "AB"}, "answer": "B", "names": {"A": hay.name, "B": bee.name},
            "clips": {"quiz": save("three.quiz", s, level=None, detail="Haydn, Op. 1 No. 1, first movement, bars 1-6; Beethoven, Op. 59 No. 1, first movement, bars 1-6; from the encodings, Part 7's bowed string")}}


def compute_style() -> dict:
    ms = movements()
    y = [m.composer for m in ms]
    pieces = [Piece(m.name, m.name, m.composer, m.time, m.bar, m.voices) for m in ms]
    X24 = np.array([PS.features(p) for p in pieces])
    X26 = np.array([CL.features(m) for m in ms])
    a24 = PS.loo_centroid(X24, y)
    a26 = PS.loo_centroid(X26, y)
    singles = sorted(((PS.loo_centroid(X26[:, [k]], y)["accuracy"], f) for k, f in enumerate(CL.FEATURES)), reverse=True)
    means = {c: [float(x) for x in X26[np.array(y) == c].mean(0)] for c in ("haydn", "mozart", "beethoven")}
    rng = np.random.default_rng(26)
    null = np.array([PS.loo_centroid(X26, list(rng.permutation(y)))["accuracy"] for _ in range(2000)])
    return {"n": len(ms), "counts": dict(Counter(y)), "acc24": a24["accuracy"], "acc26": a26["accuracy"], "conf26": a26["confusion"], "conf24": a24["confusion"],
            "singles": [[f, a] for a, f in singles], "means": means, "features": list(CL.FEATURES),
            "chance": max(Counter(y).values()) / len(y), "X": X26.tolist(), "y": y, "names": [m.name for m in ms],
            "null": null.tolist(), "p_perm": float((1 + np.sum(null >= a26["accuracy"] - 1e-12)) / (1 + len(null)))}


def compute_tune() -> dict:
    tl = tune_line()[:14]
    unit = 0.34
    # theme with an Alberti bass
    theme = [tl, accompany("alberti", HARM[:8])]
    # minore: the melody in C minor (E and A flattened), repeated-chord accompaniment
    minor_h = ["i", "i", "iv", "i", "V7", "i", "V7", "i"]
    mn = [(p - 1 if p % 12 in (4, 9) else p, o, d) for p, o, d in tl]
    minore = [mn, accompany("repeated", minor_h)]
    # adagio: twice as slow, the melody ornamented with turns and passing notes
    ad = []
    for k, (p, o, d) in enumerate(tl):
        if d >= 2:
            ad += [(p, 2 * o, 2), (p + 2, 2 * o + 2, 0.5), (p, 2 * o + 2.5, 0.5), (p - 1, 2 * o + 3, 0.5), (p, 2 * o + 3.5, 0.5)]
        elif k % 2 == 1:
            ad += [(p, 2 * o, 1.5), (p + 1 if p % 12 in (4, 11) else p + 2, 2 * o + 1.5, 0.5)]
        else:
            ad.append((p, 2 * o, 2))
    adagio = [ad, accompany("block", [h for h in HARM[:8]], beats=4)]
    # finale: in 6/8, the melody's notes in long-short pairs, fast
    fin = []
    t = 0.0
    for p, o, d in tl:
        fin += [(p, t, 0.75 * d), (p + (2 if p % 12 != 11 else 1), t + 0.75 * d, 0.25 * d)] if d == 1 else [(p, t, d)]
        t += d
    finale = [fin, accompany("repeated", HARM[:8])]
    secs = []
    clips = []
    for name, (lines, u) in {"theme": (theme, unit), "minore": (minore, unit * 1.1), "adagio": (adagio, unit * 0.9), "finale": (finale, unit * 0.62)}.items():
        c = place(lines, piano, u, gains=[0.0, -7.0]).at_level(LEVEL)
        clips.append(c)
        secs.append(name)
    s = concat(clips, gap=1.0, names=secs)
    return {"theme": [rows(x) for x in theme], "minore": [rows(x) for x in minore], "adagio": [rows(x) for x in adagio], "finale": [rows(x) for x in finale],
            "units": {"theme": unit, "minore": unit * 1.1, "adagio": unit * 0.9, "finale": unit * 0.62},
            "starts": {k: float(s.events[k]) for k in secs}, "seconds": s.duration, "notes": {k: len(v[0]) for k, v in (("theme", theme), ("minore", minore), ("adagio", adagio), ("finale", finale))},
            "clips": {"variation": save("tune.variation26", s, level=None, detail="the Tune as a Classical variation set: theme with Alberti bass, minore, adagio, finale, Part 7's piano")}}


def compute_variation() -> dict:
    t = load("tune")
    n = t["notes"]
    return {"part": 26, "title": r"as a Classical set: theme with Alberti bass, minore, adagio, finale", "seconds": round(t["seconds"], 2),
            "measure": rf"melody notes: theme {n['theme']}, minore {n['minore']}, adagio {n['adagio']}, finale {n['finale']}",
            "clip": "tune.variation26"}


def compute_forms() -> dict:
    """A period (antecedent to a half cadence, consequent to a full one) and a sentence (an idea, its repetition a step
    higher, a quicker continuation to the cadence), on the Tune's material."""
    ant = [(72, 0, 1), (72, 1, 1), (79, 2, 1), (79, 3, 1), (81, 4, 1), (81, 5, 1), (79, 6, 2)]
    con = [(72, 8, 1), (72, 9, 1), (79, 10, 1), (79, 11, 1), (77, 12, 1), (76, 13, 1), (74, 14, 1), (72, 15, 1)]
    per_h = ["I", "I", "IV", "V", "I", "I", "V7", "I"]
    idea = [(72, 0, 1), (72, 1, 1), (79, 2, 1), (79, 3, 1)]
    rep = [(74, 4, 1), (74, 5, 1), (81, 6, 1), (81, 7, 1)]
    cont = [(81, 8, 0.5), (79, 8.5, 0.5), (77, 9, 0.5), (76, 9.5, 0.5), (77, 10, 0.5), (76, 10.5, 0.5), (74, 11, 0.5), (72, 11.5, 0.5), (74, 12, 1), (71, 13, 1), (72, 14, 2)]
    sen_h = ["I", "I", "V7", "V7", "I", "IV", "V7", "I"]
    unit = 0.4
    cP = place([ant + con, accompany("block", per_h)], piano, unit, gains=[0.0, -6.0])
    cS = place([idea + rep + cont, accompany("block", sen_h)], piano, unit, gains=[0.0, -6.0])
    s_ = concat([cP.at_level(LEVEL), cS.at_level(LEVEL)], gap=1.2, names=["period", "sentence"])
    return {"period": rows(ant + con), "period_acc": rows(accompany("block", per_h)), "sentence": rows(idea + rep + cont), "sentence_acc": rows(accompany("block", sen_h)),
            "unit": unit, "starts": {k: float(s_.events[k]) for k in ("period", "sentence")},
            "clips": {"two": save("forms.two", s_, level=None, detail="an eight-bar period and an eight-bar sentence on the Tune's material, Part 7's piano")}}


def compute_develop() -> dict:
    ms = movements()
    m = [x for x in ms if x.name == "opus74no1/movement1"][0]
    ex = excerpt(m, 60, 8)
    c = place(ex, bowed, 0.24, gains=[0, -1, -2, -1])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["dev"])
    return {"voices": [rows(v) for v in ex], "unit": 0.24, "start_bar": 60,
            "clips": {"dev": save("plan.development", s_, level=None, detail="Haydn, Op. 74 No. 1, first movement, bars 61-68 (the development), from the encoding, Part 7's bowed string")}}


def compute_dynamics() -> dict:
    tl = tune_line()[:7]
    out, t = [], 0.0
    for rep in range(3):
        for p, o, d in tl:
            out.append((p, t + o, d))
        t += 8
    vel = [0.5 + 1.4 * k / (len(out) - 1) for k in range(len(out))]
    placed = []
    for (p, o, d), v in zip(out, vel):
        placed.append((piano(p, d * 0.4 * 1.02, velocity=round(v, 2)), o * 0.4, 0.0))
    c = Clip(mix(placed, duration=24 * 0.4 + 1.2).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["cresc"])
    return {"notes": rows(out), "velocity": vel, "unit": 0.4,
            "clips": {"cresc": save("piano.crescendo", s_, level=None, detail="the Tune's first phrase three times in a long crescendo, hammer velocity rising, Part 7's piano")}}


def compute_keys() -> dict:
    """Where does each movement go first?  Part 15's tracker, eight-bar windows, the first new key that holds; counted
    only where the tracker reads the same key in the first and the last window, so that the home key is trustworthy."""
    ms = movements()
    rows_, tally = [], Counter()
    for m in ms:
        pl = CL.tonal_plan(m)
        home = tuple(pl[0]["key"])
        if tuple(pl[-1]["key"]) != home:
            rows_.append({"name": m.name, "composer": m.composer, "home": list(home), "second": None, "rel": None, "agree": False})
            continue
        sk = CL.second_key(pl)
        rel = None if sk is None else ("V" if sk[:2] == (7, "major") else "III" if sk[:2] == (3, "major") and home[1] == "minor"
                                       else "v" if sk[:2] == (7, "minor") else "other")
        tally[(home[1], rel)] += 1
        rows_.append({"name": m.name, "composer": m.composer, "home": list(home), "second": None if sk is None else list(sk), "rel": rel, "agree": True})
    m = [x for x in ms if x.name == "opus59no2/movement4"][0]
    plan4 = CL.tonal_plan(m, window_bars=4, hop_bars=2)
    ex = excerpt(m, 0, 16)
    unit = 0.22
    c = place(ex, bowed, unit, gains=[0, -1, -2, -1])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["wrong"])
    settle = next(t["bar"] for i, t in enumerate(plan4) if all(tuple(u["key"]) == (4, "minor") for u in plan4[i:i + 5]))
    return {"rows": rows_, "tally": {f"{a}|{b}": n for (a, b), n in tally.items()},
            "agree": sum(r["agree"] for r in rows_), "major": sum(1 for r in rows_ if r["agree"] and r["home"][1] == "major"),
            "minor": sum(1 for r in rows_ if r["agree"] and r["home"][1] == "minor"),
            "plan4": [{"bar": t["bar"], "key": list(t["key"])} for t in plan4[:30]], "settle": float(settle),
            "voices": [rows(v) for v in ex], "unit": unit, "bar_beats": m.bar / 24.0,
            "clips": {"wrong": save("keys.wrong", s_, level=None, detail="Beethoven, String Quartet Op. 59 No. 2, finale, bars 1-16 from the encoding: an E minor movement that begins in C major, Part 7's bowed string")}}


def compute_minuet() -> dict:
    ms = movements()
    m = [x for x in ms if x.name == "opus74no1/movement3"][0]
    ex = excerpt(m, 0, 8)
    unit = 0.3
    c = place(ex, bowed, unit, gains=[0, -1, -2, -1])
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["minuet"])
    threes = [r for r in ms if r.time[0] == 3 and r.time[1] == 4]
    return {"voices": [rows(v) for v in ex], "unit": unit, "bar_beats": m.bar / 24.0, "in34": len(threes), "n": len(ms),
            "clips": {"minuet": save("minuet.haydn", s_, level=None, detail="Haydn, String Quartet Op. 74 No. 1, third movement (Menuetto), bars 1-8 from the encoding, Part 7's bowed string")}}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation26", 26)


ITEMS = {"hook": compute_hook, "forms": compute_forms, "develop": compute_develop, "dynamics": compute_dynamics, "keys": compute_keys, "minuet": compute_minuet, "phrases": compute_phrases, "plan": compute_plan, "texture": compute_texture, "figures": compute_figures,
         "three": compute_three, "style": compute_style, "tune": compute_tune, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
