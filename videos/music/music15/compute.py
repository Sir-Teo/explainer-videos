"""Precompute everything numerical, and every sound, in Part 15 of *Music, Built* ("Key").

    python -m videos.music.music15.compute              # everything missing (about a minute)
    python -m videos.music.music15.compute --force finder

Numbers are cached in ``.cache/music15/<name>.json`` (+ ``.npz``), sounds in ``.cache/music15/audio/``.  The key
module is Monochord's (``explainer/music/monochord/key.py``); published findings are cited in the README.

Items:
    hook        a cadence, and then a single tone: one that fits and one that does not
    profile     Krumhansl and Kessler's ratings; how often each note occurs in the 54 tunes; three probes
    functions   the chords of a key by what they hold: resting notes and leaning notes; three progressions
    cadences    four ways to end a phrase; one to name by ear
    meter       the key finder listening to the Tune, note by note
    finder      key finders scored on 54 tunes in twelve keys; how many notes they need; what they mistake
    rare        how many keys contain a set of notes; the Tune's blind spot
    keymap      how alike the 24 keys are; the torus; near and far keys, heard
    modulate    a phrase that visits a key and a phrase that moves to it; the key finder's reading of both
    minor       one phrase in a key, its parallel and its relative; tunes that are in no major or minor key
    more        a phrase harmonized; two authentic cadences; the finder's near misses; signatures; shared chords;
                the dominant in minor; one cadence in two keys and the thirds of an unequal temperament
    tune        Variation 15: the Tune through all twelve keys, down the circle of fifths, to a deceptive cadence
    variation   the Variations ledger, row 15
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import chords as CH
from explainer.music.monochord import ear as EAR
from explainer.music.monochord import key as K
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music15")
CLIPS = ClipStore("music15")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C4 = 261.6255653005986
BOARD = STR.soundboard()
_NOTES: dict = {}
CORPUS = M.corpus()
BY_NAME = {m.name: m for m in CORPUS}
TUNE = BY_NAME[M.THE_TUNE]
TEMP = (K.TEMPERLEY_MAJOR, K.TEMPERLEY_MINOR)
TRIAD = {"major": (0, 4, 7), "minor": (0, 3, 7), "diminished": (0, 3, 6), "7": (0, 4, 7, 10)}
# the chords of a major key: degree -> (semitones of the root above the tonic, kind)
DEGREE = {"I": (0, "major"), "ii": (2, "minor"), "iii": (4, "minor"), "IV": (5, "major"), "V": (7, "major"), "V7": (7, "7"), "vi": (9, "minor"), "vii°": (11, "diminished"),
          "i": (0, "minor"), "iv": (5, "minor"), "v": (7, "minor"), "V/V": (2, "major"), "V7/V": (2, "7"), "V7/IV": (0, "7")}


def clip(y, fade=(0.001, 0.05)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def piano(hz: float, seconds: float) -> Clip:
    key = (round(hz, 3), round(seconds, 3))
    if key not in _NOTES:
        y = BOARD.play(STR.struck(String.tuned(hz, L=0.62 * (C4 / hz) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=1.6, seconds=seconds + 0.25))
        _NOTES[key] = clip(y, (0.001, 0.18)).at_level(LEVEL)
    return _NOTES[key]


def note(m: float, seconds: float) -> Clip:
    return piano(CH.hz(m), seconds)


def chord(midis, seconds: float, roll: float = 0.012) -> Clip:
    return mix([(note(m, seconds), k * roll, 0.0) for k, m in enumerate(midis)], duration=seconds + 0.3 + roll * len(midis))


def voiced(names, tonic: int = 60, start=None) -> list[list[int]]:
    """A progression (Roman numerals in the key whose tonic is MIDI ``tonic``) as chords for the piano: a bass
    note and three or four upper voices that move as little as they can."""
    out, cur = [], start
    for nm in names:
        off, kind = DEGREE[nm]
        root = tonic + off
        pcs = [(root + h) % 12 for h in TRIAD[kind]]
        if cur is None:
            cur = tuple(sorted(60 + ((p - 60) % 12) for p in pcs[:3]))
        upper_pcs = pcs if len(pcs) == 3 else [pcs[1], pcs[2], pcs[3]]          # a seventh chord leaves its root to the bass
        cur = CH.nearest_voicing(cur, upper_pcs, low=55, high=74)
        bass = 36 + root % 12
        out.append([bass if bass >= 41 else bass + 12] + list(cur))
    return out


def progression(names, tonic: int = 60, dur: float = 0.9, last: float = 1.6, start=None) -> tuple[Clip, list]:
    chords_ = voiced(names, tonic, start)
    placed, ev, t = [], {}, 0.0
    for k, ch in enumerate(chords_):
        d = last if k == len(chords_) - 1 else dur
        placed.append((chord(ch, d), t, 0.0))
        ev[f"c{k}"] = t
        t += d
    ev["end"] = t
    return Clip(mix(placed, duration=t + 0.4).y, SR, ev, []), chords_


def probe(pc: int, seconds: float = 1.0) -> Clip:
    """A Shepard tone on a pitch class (C is 0): a note with no particular octave, as in the experiments."""
    return clip(EAR.shepard(pc + 3, seconds), (0.02, 0.1)).at_level(LEVEL - 2.0)


def play(pitches, beats=None, beat: float = 0.42, base: int = 60, last: float = 1.6) -> Clip:
    pitches = list(pitches)
    beats = [1.0] * len(pitches) if beats is None else list(beats)
    placed, ev, t = [], {}, 0.0
    for k, (p, b) in enumerate(zip(pitches, beats)):
        d = b * beat * (last if k == len(pitches) - 1 else 1.0)
        placed.append((note(base + p, max(d, 0.14)), t, 0.0))
        ev[f"n{k}"] = t
        t += d
    ev["end"] = t
    return Clip(mix(placed, duration=t + 0.5).y, SR, ev, [])


def times(c: Clip, n: int, prefix: str = "", stem: str = "c") -> list[float]:
    return [float(c.events[f"{prefix}{stem}{k}"]) for k in range(n)]


def names_of(key) -> str:
    return K.key_name(key)


# ---------------------------------------------------------------------------
def with_probe(pc: int) -> tuple[Clip, dict]:
    ctx, chords_ = progression(["I", "IV", "V", "I"], dur=0.75, last=1.1)
    t_probe = ctx.events["end"] + 0.55
    c = mix([(ctx.at_level(LEVEL), 0.0, 0.0), (probe(pc), t_probe, 0.0)], duration=t_probe + 1.4)
    return Clip(c.y, SR, {**{k: v for k, v in ctx.events.items()}, "probe": t_probe}, []), {"chords": chords_, "times": times(ctx, 4), "probe": t_probe}


def compute_hook() -> dict:
    a, da = with_probe(0)
    b, db = with_probe(6)
    seq = concat([a, b], gap=1.0, names=["fits", "not"])
    return {"chords": da["chords"], "times": {"fits": [float(seq.events["fits"]) + t for t in da["times"]], "not": [float(seq.events["not"]) + t for t in da["times"]]},
            "probe": {"fits": float(seq.events["fits"]) + da["probe"], "not": float(seq.events["not"]) + db["probe"]}, "starts": {"fits": float(seq.events["fits"]), "not": float(seq.events["not"])},
            "ratings": {"C": float(K.KK_MAJOR[0]), "F♯": float(K.KK_MAJOR[6])},
            "clips": {"probe": save("hook.probe", seq, level=None, detail="four chords on Part 7's piano, then one tone with no octave: twice")}}


def compute_profile() -> dict:
    maj, mi = K.learn_profiles(CORPUS, floor=0.0)
    r = float(np.corrcoef(maj, K.KK_MAJOR)[0, 1])
    order = [int(i) for i in np.argsort(-K.KK_MAJOR)]
    parts, info = [], []
    for pc in (7, 1, 4):                                      # G, C sharp, E after the same chords
        c, d = with_probe(pc)
        parts.append(c)
        info.append(d)
    quiz = concat(parts, gap=0.9, names=["A", "B", "C"])
    return {"kk_major": K.KK_MAJOR.tolist(), "kk_minor": K.KK_MINOR.tolist(), "corpus_major": maj.tolist(), "r": r, "r_temperley": float(np.corrcoef(maj, K.TEMPERLEY_MAJOR)[0, 1]),
            "order": order, "names": list(K.NAMES_FLAT), "groups": {"tonic": [0], "triad": [4, 7], "scale": [2, 5, 9, 11], "outside": [1, 3, 6, 8, 10]},
            "group_means": {"tonic": float(K.KK_MAJOR[0]), "triad": float(K.KK_MAJOR[[4, 7]].mean()), "scale": float(K.KK_MAJOR[[2, 5, 9, 11]].mean()), "outside": float(K.KK_MAJOR[[1, 3, 6, 8, 10]].mean())},
            "quiz": {"probes": ["G", "C♯", "E"], "ratings": [float(K.KK_MAJOR[p]) for p in (7, 1, 4)], "answer": "B",
                     "probe_times": {k: float(quiz.events[k]) + info[i]["probe"] for i, k in enumerate("ABC")}, "starts": {k: float(quiz.events[k]) for k in "ABC"}},
            "clips": {"quiz": save("profile.quiz", quiz, level=None, detail="the same four chords, and three different tones after them")}}


def compute_functions() -> dict:
    t = M.degree_transitions(CORPUS)
    rest = {1, 3, 5}
    rows = []
    for nm, degs in (("I", (1, 3, 5)), ("ii", (2, 4, 6)), ("iii", (3, 5, 7)), ("IV", (4, 6, 1)), ("V", (5, 7, 2)), ("vi", (6, 1, 3)), ("vii°", (7, 2, 4))):
        lean = [d for d in degs if d not in rest]
        rows.append({"roman": nm, "degrees": list(degs), "resting": len(degs) - len(lean), "leaning": lean,
                     "function": {"I": "tonic", "vi": "tonic", "iii": "tonic", "IV": "predominant", "ii": "predominant", "V": "dominant", "vii°": "dominant"}[nm]})
    goes = {str(d): {"to": int(np.argmax(t[d - 1])) + 1, "p": float(np.max(t[d - 1]))} for d in (2, 4, 6, 7)}
    parts, chords_ = [], {}
    for label, prog in (("a", ["I", "IV", "V", "I"]), ("b", ["I", "ii", "V7", "I"]), ("c", ["I", "V", "IV", "I"])):
        c, ch = progression(prog, dur=0.85, last=1.5)
        parts.append(c.at_level(LEVEL))
        chords_[label] = {"names": prog, "chords": ch}
    seq = concat(parts, gap=0.8, names=["a", "b", "c"])
    return {"rows": rows, "goes": goes, "progressions": chords_, "times": {k: times(seq, 4, f"{k}.") for k in "abc"}, "starts": {k: float(seq.events[k]) for k in "abc"},
            "clips": {"three": save("functions.three", seq, level=None, detail="home, away, tension, home; the same with another chord; and the middle two exchanged")}}


CADENCES = {"authentic": ["I", "IV", "V7", "I"], "half": ["I", "ii", "IV", "V"], "plagal": ["I", "V", "IV", "I"], "deceptive": ["I", "IV", "V7", "vi"]}


def compute_cadences() -> dict:
    parts, chords_ = [], {}
    for name, prog in CADENCES.items():
        c, ch = progression(prog, dur=0.85, last=1.7)
        parts.append(c.at_level(LEVEL))
        chords_[name] = {"names": prog, "chords": ch}
    four = concat(parts, gap=0.9, names=list(CADENCES))
    order = ["half", "deceptive", "authentic"]
    q = concat([progression(CADENCES[n], tonic=62, dur=0.85, last=1.7)[0].at_level(LEVEL) for n in order], gap=0.9, names=["A", "B", "C"])
    return {"cadences": chords_, "times": {k: times(four, 4, f"{k}.") for k in CADENCES}, "starts": {k: float(four.events[k]) for k in CADENCES},
            "quiz": {"order": order, "answer": "B", "starts": {k: float(q.events[k]) for k in "ABC"}},
            "clips": {"four": save("cadences.four", four, level=None, detail="four endings in C major: Part 7's piano"),
                      "quiz": save("cadences.quiz", q, level=None, detail="three endings in D major")}}


def compute_meter() -> dict:
    n = 14
    p, b = TUNE.pitches[:n], TUNE.beats[:n]
    c = play(p, b, beat=0.5)
    rows = []
    for k in range(1, n + 1):
        post = K.posterior(p[:k], b[:k])
        top = sorted(post.items(), key=lambda kv: -kv[1])[:4]
        rows.append({"notes": k, "top": [{"key": names_of(key), "p": float(v)} for key, v in top], "c_major": float(post[(0, "major")]), "f_major": float(post[(5, "major")]),
                     "g_major": float(post[(7, "major")]), "a_minor": float(post[(9, "minor")])})
    first_sure = next(r["notes"] for r in rows if r["top"][0]["key"] == "C major" and r["top"][0]["p"] > 0.5)
    return {"pitches": p, "beats": b, "times": times(c, n, stem="n"), "rows": rows, "first_sure": int(first_sure),
            "clips": {"tune": save("meter.tune", c, detail="two phrases of the Tune")}}


def accuracy(finder, n=None) -> tuple[float, dict]:
    right = total = 0
    wrong: dict = {}
    for m in CORPUS:
        p, b = (m.pitches, m.beats) if n is None else (m.pitches[:n], m.beats[:n])
        for tr in range(12):
            got = finder([x + tr for x in p], b)
            total += 1
            if got == (tr, m.mode):
                right += 1
            else:
                rel = f"{(got[0] - tr) % 12} {got[1]} for {m.mode}"
                wrong[rel] = wrong.get(rel, 0) + 1
    return right / total, wrong


def compute_finder() -> dict:
    ks = lambda p, b: K.find_key(K.distribution(p, b))                              # noqa: E731
    kt = lambda p, b: K.find_key(K.distribution(p, b), TEMP)                        # noqa: E731
    finders = {"ratings": ks, "counts": kt, "bayes": K.bayes_key, "last": lambda p, b: (p[-1] % 12, "major"), "first": lambda p, b: (p[0] % 12, "major")}
    full = {}
    for name, f in finders.items():
        a, w = accuracy(f)
        full[name] = {"accuracy": a, "wrong": dict(sorted(w.items(), key=lambda kv: -kv[1])[:3])}
    ns = [2, 3, 4, 5, 6, 8, 10, 12, 16, 20]
    curve = {name: [accuracy(finders[name], n)[0] for n in ns] for name in ("ratings", "counts", "bayes")}
    # leave-one-out: profiles counted from the other tunes
    right = total = 0
    for i, m in enumerate(CORPUS):
        prof = K.learn_profiles(CORPUS[:i] + CORPUS[i + 1:])
        for tr in range(12):
            right += K.bayes_key([x + tr for x in m.pitches], m.beats, prof) == (tr, m.mode)
            total += 1
    return {"full": full, "ns": ns, "curve": curve, "cases": len(CORPUS) * 12, "own": right / total,
            "dominant_errors": full["ratings"]["wrong"].get("7 major for major", 0), "five": curve["bayes"][ns.index(5)]}


def compute_rare() -> dict:
    sets = [("C, D, E", [0, 2, 4]), ("C, D, E, F", [0, 2, 4, 5]), ("B, F", [11, 5]), ("B, F, C", [11, 5, 0]), ("C, G", [0, 7]), ("F♯, C", [6, 0])]
    rows = [{"notes": nm, "keys": [names_of(k).replace(" major", "") for k in K.keys_containing(pcs)]} for nm, pcs in sets]
    # the Tune, note by note: the major keys that still contain everything heard
    seen, steps = [], []
    for p in TUNE.pitches:
        if p % 12 not in seen:
            seen.append(p % 12)
            steps.append({"note": K.NAMES_FLAT[p % 12], "keys": [names_of(k).replace(" major", "") for k in K.keys_containing(seen)]})
    # how often each interval class occurs in a major scale (Part 12): the rarest is the best clue
    from explainer.music.monochord import scales as S
    vec = list(S.interval_vector(K.MAJOR_SCALE))
    pairs = {"tritone": 2, "semitone": None}
    return {"rows": rows, "tune_steps": steps, "tune_keys_left": steps[-1]["keys"], "vector": vec, "tritone_keys": len(K.keys_containing([11, 5])), "fifth_keys": len(K.keys_containing([0, 7])),
            "semitone_keys": len(K.keys_containing([11, 0])), "pairs": pairs}


def compute_keymap() -> dict:
    C = K.key_correlations()
    t = K.torus()
    near = [{"key": names_of(k), "r": r} for k, r in K.nearest_keys((0, "major"), top=6)]
    far = min(((K.KEYS[j], float(C[0, j])) for j in range(24)), key=lambda kv: kv[1])
    angles = [{"key": names_of(k), "short": K.key_name(k, short=True), "mode": k[1], "tonic": k[0], "theta": a, "phi": b} for k, (a, b) in t["angles"].items()]
    # near and far: a cadence in C, then the same cadence in another key
    targets = [("G major", 67 - 12), ("A minor", 57), ("F♯ major", 54)]
    parts = []
    home, _ = progression(["I", "IV", "V7", "I"], tonic=60, dur=0.7, last=1.2)
    for nm, tonic in targets:
        prog = ["i", "iv", "V7", "i"] if "minor" in nm else ["I", "IV", "V7", "I"]
        there, _ = progression(prog, tonic=tonic + (12 if tonic < 55 else 0), dur=0.7, last=1.3)
        parts.append(concat([home.at_level(LEVEL), there.at_level(LEVEL)], gap=0.25, names=["home", "there"]))
    seq = concat(parts, gap=1.0, names=["G", "a", "Fs"])
    shared = {names_of((tt, "major")): K.shared_notes((0, "major"), (tt, "major")) for tt in range(12)}
    return {"near": near, "far": {"key": names_of(far[0]), "r": far[1]}, "angles": angles, "explained": t["explained"], "shared": shared,
            "pairs": {"G": {"r": float(C[0, 7]), "shared": 6}, "a": {"r": float(C[0, 12 + 9]), "shared": 7}, "Fs": {"r": float(C[0, 6]), "shared": 2}},
            "starts": {k: float(seq.events[k]) for k in ("G", "a", "Fs")}, "there": {k: float(seq.events[k]) + float(parts[i].events["there"]) for i, k in enumerate(("G", "a", "Fs"))},
            "clips": {"jumps": save("keymap.jumps", seq, level=None, detail="a cadence in C major, then the same cadence in another key: three times")}}


def chord_notes(chords_, dur_beats):
    """The notes of a progression as (pitch, beats) for the key finder."""
    p, b = [], []
    for ch in chords_:
        for m in ch:
            p.append(m)
            b.append(dur_beats)
    return p, b


def compute_modulate() -> dict:
    visit = ["I", "V7/V", "V", "V7", "I"]                       # a dominant of the dominant, in passing
    move = ["I", "vi", "V7/V", "V"]                             # ... and then a cadence in the new key
    a, ca = progression(visit, dur=0.9, last=1.6)
    b1, cb1 = progression(move, dur=0.9, last=0.9)
    b2, cb2 = progression(["I", "IV", "V7", "I"], tonic=67 - 12, dur=0.9, last=1.6, start=tuple(cb1[-1][1:]))
    b = concat([b1, b2], gap=0.0, names=["x", "y"])
    seq = concat([a.at_level(LEVEL), Clip(b.y, SR, b.events, []).at_level(LEVEL)], gap=1.0, names=["A", "B"])
    read = {}
    for label, chs in (("A", ca), ("B", cb1 + cb2)):
        path = []
        for k in range(1, len(chs) + 1):
            p, bb = chord_notes(chs[max(0, k - 3):k], 1.0)       # the last three chords
            path.append(names_of(K.bayes_key(p, bb)))
        p, bb = chord_notes(chs, 1.0)
        read[label] = {"path": path, "whole": names_of(K.bayes_key(p, bb)), "last": path[-1]}
    return {"visit": {"names": visit, "chords": ca}, "move": {"names": move + ["I", "IV", "V7", "I"], "chords": cb1 + cb2}, "reading": read,
            "times": {"A": times(seq, 5, "A."), "B": [float(seq.events["B"]) + float(b.events[f"x.c{k}"]) for k in range(4)] + [float(seq.events["B"]) + float(b.events[f"y.c{k}"]) for k in range(4)]},
            "starts": {"A": float(seq.events["A"]), "B": float(seq.events["B"])}, "pivot": "vi in C major is ii in G major",
            "clips": {"two": save("modulate.two", seq, level=None, detail="a phrase that leans on G and comes home; a phrase that moves to G and stays")}}


def compute_minor() -> dict:
    ph, b = TUNE.pitches[:7], TUNE.beats[:7]
    minor = [p - 1 if p % 12 in (4, 9) else p for p in ph]      # the third and sixth lowered: C minor
    rel = [p - 3 for p in minor]                               # the same shape on A: A minor
    seq = concat([play(ph, b, beat=0.45).at_level(LEVEL), play(minor, b, beat=0.45).at_level(LEVEL), play(rel, b, beat=0.45).at_level(LEVEL)], gap=0.8, names=["major", "parallel", "relative"])
    odd = []
    for name in ("Drunken Sailor", "Greensleeves", "Amazing Grace", "Auld Lang Syne", "Jasmine Flower (Mo Li Hua)"):
        m = BY_NAME[name]
        post = K.posterior(m.pitches, m.beats)
        top = sorted(post.items(), key=lambda kv: -kv[1])[:2]
        pcs = sorted({p % 12 for p in m.pitches})
        odd.append({"name": name, "notes": len(pcs), "pcs": pcs, "found": names_of(top[0][0]), "p": float(top[0][1]), "second": names_of(top[1][0]), "mode": m.mode,
                    "right": top[0][0] == (0, m.mode)})
    return {"major": ph, "parallel": minor, "relative": rel, "beats": b, "times": {k: times(seq, 7, f"{k}.", stem="n") for k in ("major", "parallel", "relative")},
            "starts": {k: float(seq.events[k]) for k in ("major", "parallel", "relative")},
            "shared": {"parallel": K.shared_notes((0, "major"), (0, "minor")), "relative": K.shared_notes((0, "major"), (9, "minor"))},
            "r": {"parallel": float(K.key_correlations()[0, 12]), "relative": float(K.key_correlations()[0, 21])}, "odd": odd,
            "clips": {"three": save("minor.three", seq, level=None, detail="one phrase of the Tune in C major, C minor and A minor")}}


def diatonic_triads(key) -> set:
    """The seven triads of a major key, as (root pitch class, kind)."""
    t = key[0]
    return {((t + off) % 12, kind) for off, kind in ((0, "major"), (2, "minor"), (4, "minor"), (5, "major"), (7, "major"), (9, "minor"), (11, "diminished"))}


def with_top(names, top, tonic: int = 60, dur: float = 0.95, last: float = 1.9) -> tuple[Clip, list]:
    """A progression with a melody note above each chord."""
    chs = voiced(names, tonic)
    placed, ev, t = [], {}, 0.0
    for k, (ch, m) in enumerate(zip(chs, top)):
        d = last if k == len(chs) - 1 else dur
        placed.append((chord(ch, d), t, -4.0))
        placed.append((note(m, d), t + 0.02, 0.0))
        ev[f"c{k}"] = t
        t += d
    ev["end"] = t
    return Clip(mix(placed, duration=t + 0.4).y, SR, ev, []), [ch + [m] for ch, m in zip(chs, top)]


def compute_more() -> dict:
    """Numbers and sounds for the passages added after the first cut."""
    from explainer.music.monochord import tuning as TU

    out = {}
    # 1. each degree of the scale belongs to three of the seven triads
    members = {d: [nm for nm, degs in (("I", (1, 3, 5)), ("ii", (2, 4, 6)), ("iii", (3, 5, 7)), ("IV", (4, 6, 1)), ("V", (5, 7, 2)), ("vi", (6, 1, 3)), ("vii°", (7, 2, 4))) if d in degs] for d in range(1, 8)}
    # the Tune's first two phrases: alone, then with a chord to every two beats
    beat = 0.5
    mel_p, mel_b = TUNE.pitches[:14], TUNE.beats[:14]
    alone = play(mel_p[:7], mel_b[:7], beat=beat, base=72, last=1.0)
    prog = ["I", "I", "IV", "I", "IV", "I", "V7", "I"]
    chs = voiced(prog, 60)
    placed, ev, t = [], {}, 0.0
    for k, (pp, bb) in enumerate(zip(mel_p, mel_b)):
        placed.append((note(72 + pp, bb * beat * (1.6 if k == 13 else 1.0)), t, 0.0))
        ev[f"n{k}"] = t
        t += bb * beat
    for j, ch in enumerate(chs):
        placed.append((chord(ch, 2 * beat * (1.6 if j == 7 else 1.0), roll=0.01), j * 2 * beat, -5.0))
        ev[f"c{j}"] = j * 2 * beat
    ev["end"] = t
    both = Clip(mix(placed, duration=t + 1.2).y, SR, ev, [])
    harm = concat([alone.at_level(LEVEL), both.at_level(LEVEL)], gap=0.8, names=["alone", "chords"])
    out["harmonize"] = {"members": {str(k): v for k, v in members.items()}, "prog": prog, "chords": chs, "melody": [72 + x for x in mel_p], "beats": mel_b,
                        "alone_times": times(harm, 7, "alone.", stem="n"), "melody_times": times(harm, 14, "chords.", stem="n"), "chord_times": times(harm, 8, "chords."),
                        "starts": {"alone": float(harm.events["alone"]), "chords": float(harm.events["chords"])}}
    # 2. the same cadence with the melody ending on the tonic, and on the third
    a, cha = with_top(["IV", "V7", "I"], [69, 71, 72])
    b, chb = with_top(["IV", "V7", "I"], [72, 74, 76])
    sop = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=0.9, names=["perfect", "imperfect"])
    out["soprano"] = {"chords": {"perfect": cha, "imperfect": chb}, "times": {k: times(sop, 3, f"{k}.") for k in ("perfect", "imperfect")}, "starts": {k: float(sop.events[k]) for k in ("perfect", "imperfect")}}
    # 3. the key finder's mistakes are near misses
    f = load("finder")["full"]["ratings"]["wrong"]
    C = K.key_correlations()
    out["mistakes"] = {"wrong": f, "total": int(sum(f.values())), "dominant": f.get("7 major for major", 0), "mediant": f.get("4 minor for major", 0),
                       "r_dominant": float(C[0, 7]), "r_mediant": float(C[0, 12 + 4]), "own": load("finder")["own"]}
    # 4. key signatures
    out["signatures"] = {"sharps": list("FCGDAEB"), "flats": list("BEADGCF"), "keys_sharp": ["G", "D", "A", "E", "B", "F♯"], "keys_flat": ["F", "B♭", "E♭", "A♭", "D♭", "G♭"]}
    # 5. chords two keys share, by how far apart the keys are
    home = diatonic_triads((0, "major"))
    out["pivots"] = [{"fifths": k, "key": names_of(((7 * k) % 12, "major")), "shared": len(home & diatonic_triads(((7 * k) % 12, "major"))),
                      "chords": sorted(CH.triad_name((r, kind)) if kind != "diminished" else K.NAMES_FLAT[r] + "°" for r, kind in home & diatonic_triads(((7 * k) % 12, "major")))} for k in range(0, 7)]
    # 6. the dominant in a minor key: as the scale gives it, and with the leading note raised
    nat, chn = progression(["i", "iv", "v", "i"], tonic=57, dur=0.9, last=1.6) if "v" in DEGREE else (None, None)
    har, chh = progression(["i", "iv", "V7", "i"], tonic=57, dur=0.9, last=1.6)
    dom = concat([nat.at_level(LEVEL), har.at_level(LEVEL)], gap=0.9, names=["natural", "raised"])
    out["minor_dominant"] = {"chords": {"natural": chn, "raised": chh}, "times": {k: times(dom, 4, f"{k}.") for k in ("natural", "raised")}, "starts": {k: float(dom.events[k]) for k in ("natural", "raised")}}
    # 7. does it matter which key?  The same cadence in C and in D flat; and the thirds of an unequal temperament
    c1, ch1 = progression(["I", "IV", "V7", "I"], tonic=60, dur=0.8, last=1.5)
    c2, ch2 = progression(["I", "IV", "V7", "I"], tonic=61, dur=0.8, last=1.5)
    col = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=1.0, names=["C", "Db"])
    w = TU.werckmeister3()
    thirds = {name: float(size) for name, size in w.thirds()}
    out["colour"] = {"chords": {"C": ch1, "Db": ch2}, "times": {k: times(col, 4, f"{k}.") for k in ("C", "Db")}, "starts": {k: float(col.events[k]) for k in ("C", "Db")},
                     "thirds": thirds, "best": min(thirds, key=thirds.get), "worst": max(thirds, key=thirds.get), "pure": 386.3, "equal": 400.0}
    out["clips"] = {"harmonize": save("functions.tune", harm, level=None, detail="a phrase of the Tune alone; then two phrases with a chord to every two beats"),
                    "soprano": save("cadences.soprano", sop, level=None, detail="one cadence, with the melody ending on the first degree and on the third"),
                    "dominant": save("minor.dominant", dom, level=None, detail="a cadence in A minor with the scale's own fifth chord, and with its third raised"),
                    "colour": save("colour.two", col, level=None, detail="one cadence in C major and in D flat major")}
    return out


CIRCLE = [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7, 0]              # down a fifth each time, and home


def compute_tune() -> dict:
    beat = 0.42
    A, A2 = TUNE.pitches[:7], TUNE.pitches[7:14]
    keys = [0] + CIRCLE                                         # two phrases in C, then one in each key round the circle
    placed, events, phrases, t0 = [], {}, [], 0.0
    cur = None
    for k, pc in enumerate(keys):
        tonic = 60 + pc if pc <= 6 else 48 + pc                 # the tonic nearest middle C
        mel = A if k % 2 == 0 else A2
        last = k == len(keys) - 1
        prog = (["I", "I", "IV", "V7/IV"] if k % 2 == 0 else ["IV", "I", "V7", "V7/IV"]) if not last else ["IV", "I", "V7", "vi"]
        if k == 0:
            prog = ["I", "I", "IV", "I"]                        # the first phrase stays at home
        chs = voiced(prog, tonic, cur)
        cur = tuple(chs[-1][1:4])
        times_ = []
        t = t0
        for p, b in zip(mel, TUNE.beats[:7]):
            d = b * beat * (1.8 if last and p == mel[-1] and b == 2 else 1.0)
            placed.append((note(tonic + 12 + p if tonic + 12 + p <= 84 else tonic + p, max(d, 0.14)), t, 0.0))
            times_.append(t)
            t += b * beat
        for j, ch in enumerate(chs):
            placed.append((chord(ch, 2 * beat * (1.8 if last and j == 3 else 1.0), roll=0.01), t0 + j * 2 * beat, -6.0))
        events[f"phrase{k}"] = t0
        notes_p = [tonic + p for p in mel] + [m for ch in chs[:3] for m in ch]
        notes_b = list(TUNE.beats[:7]) + [2.0] * sum(len(ch) for ch in chs[:3])
        found = K.bayes_key(notes_p, notes_b)
        phrases.append({"key": names_of((pc, "major")), "pc": pc, "roman": prog, "chords": chs, "melody": [tonic + 12 + p if tonic + 12 + p <= 84 else tonic + p for p in mel], "times": times_,
                        "chord_times": [t0 + j * 2 * beat for j in range(4)], "t0": t0, "seconds": 8 * beat, "found": names_of(found), "right": found == (pc, "major"),
                        "signature": K.signature((pc, "major"))})
        t0 += 8 * beat
    events["end"] = t0
    out = Clip(mix(placed, duration=t0 + 2.2).y, SR, events, []).at_level(LEVEL)
    return {"clip": save("tune.variation15", out, level=None, detail="the Tune through twelve keys, a fifth lower each phrase: Part 7's piano"), "seconds": out.duration, "phrases": phrases,
            "keys": [p["key"] for p in phrases], "found_right": int(sum(p["right"] for p in phrases)), "of": len(phrases), "beat": beat}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 15, "title": r"through all twelve keys, down the circle of fifths, to a deceptive cadence", "seconds": t["seconds"],
            "measure": rf"the key finder names the key of {t['found_right']} of its {t['of']} phrases", "clip": "tune.variation15"}


ITEMS = {"hook": compute_hook, "profile": compute_profile, "functions": compute_functions, "cadences": compute_cadences, "meter": compute_meter, "finder": compute_finder,
         "rare": compute_rare, "keymap": compute_keymap, "modulate": compute_modulate, "minor": compute_minor, "more": compute_more, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
