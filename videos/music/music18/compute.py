"""Precompute everything numerical, and every sound, in Part 18 of *Music, Built* ("Progressions").

    python -m videos.music.music18.compute              # everything missing (a minute or two)
    python -m videos.music.music18.compute --force schemata

Numbers are cached in ``.cache/music18/<name>.json``, sounds in ``.cache/music18/audio/``.  The syntax of harmony is
Monochord's (``explainer/music/monochord/progression.py``), measured on Part 17's chorales
(``explainer/music/monochord/chorales.py``); the galant examples are realized here and played on a plucked string over
Part 7's soundboard; published findings are cited in the README.

Items:
    hook        a partimento bass, alone and realized by the rule of the octave
    functions   tonic, subdominant and dominant: how often each follows each
    motion      how roots move: falling fifths and the rest
    predict     how predictable the next chord is: bits per chord on chorales held out by tune; the guessing game
    sequence    the descending-fifths sequence, heard; runs of falling fifths in the chorales
    rhythm      where in the bar the chord changes
    octave      the rule of the octave up and down, heard; how often Bach's harmony agrees with it
    schemata    eight galant schemata, realized and heard; a phrase built of them
    census      the schemata in the chorales and in the series' tunes, against shuffled controls
    grounds     the lament, the Folia, the Romanesca and the passamezzo, heard
    tune        Variation 18: the Tune over the Romanesca, a lament bass, and two pedals
    variation   the Variations ledger, row 18
    more        an unfigured bass realized by rule; the rising 5-6 sequence; a schema plain and decorated
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import chords as CH
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import melody as M
from explainer.music.monochord import progression as P
from explainer.music.monochord.instruments.plucked import plucked as pluck
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver

CACHE = Cache("music18")
CLIPS = ClipStore("music18")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
_NOTES: dict = {}
HALF = 0.62                                            # seconds to a chord (a half bar)
_BOOK: list = []


def book():
    if not _BOOK:
        _BOOK.extend(BC.load())
    return _BOOK


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def harpsichord(m: float, seconds: float) -> Clip:
    """A string plucked near its end, as a quill plucks it (Part 1's monochord, retuned), on Part 7's soundboard."""
    key = (round(m, 3), round(seconds, 3))
    if key not in _NOTES:
        y = BOARD.play(pluck(hz(m), seconds=seconds + 0.4, beta=0.11))
        _NOTES[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.12).at_level(LEVEL)
    return _NOTES[key]


def play_chords(chords, seconds=HALF, arpeggio: float = 0.0, tail: float = 1.0) -> Clip:
    """Chords (top voice first) one after another; ``arpeggio`` spreads each from the bass up (seconds)."""
    placed, ev = [], {}
    for k, ch in enumerate(chords):
        t = k * seconds
        for j, m in enumerate(sorted(ch)):
            placed.append((harpsichord(m, seconds * 1.4), t + arpeggio * j, -2.0 if j else 0.0))
        ev[f"c{k}"] = t
    end = len(chords) * seconds
    ev["end"] = end
    return Clip(mix(placed, duration=end + tail).y, SR, ev, [])


def play_line(notes, seconds=HALF / 2, tail: float = 0.8) -> Clip:
    placed, ev = [], {}
    for k, m in enumerate(notes):
        placed.append((harpsichord(m, seconds * 1.6), k * seconds, 0.0))
        ev[f"n{k}"] = k * seconds
    return Clip(mix(placed, duration=len(notes) * seconds + tail).y, SR, ev, [])


def starts(c: Clip, prefix: str, n: int, key: str = "c") -> list[float]:
    return [float(c.events[f"{prefix}{key}{k}"]) for k in range(n)]


def voicing_rows(chords) -> list:
    return [[int(x) for x in ch] for ch in chords]


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    up, down = P.realize_rule("up"), P.realize_rule("down")
    bass = [ch[3] for ch in up + down[1:]]
    chords = up + down[1:]
    alone = play_line(bass, seconds=HALF * 0.75)
    full = play_chords(chords, seconds=HALF * 0.75)
    seq = concat([alone.at_level(LEVEL), full.at_level(LEVEL)], gap=1.0, names=["bass", "full"])
    return {"bass": bass, "chords": voicing_rows(chords), "figures": [P.RULE_OF_OCTAVE["up"][d] for d in range(1, 9)] + [P.RULE_OF_OCTAVE["down"][d] for d in range(7, 0, -1)],
            "times": {"bass": starts(seq, "bass.", len(bass), "n"), "full": starts(seq, "full.", len(chords))},
            "starts": {k: float(seq.events[k]) for k in ("bass", "full")},
            "clips": {"partimento": save("hook.partimento", seq, level=None, detail="a bass up and down a scale, alone; then with the rule of the octave above it: a plucked string")}}


def compute_functions() -> dict:
    b = book()
    out = {m: P.function_transitions(b, m) for m in ("major", "minor")}
    # two orders of the same three chords
    I, IV, V = (72, 67, 64, 48), (72, 69, 65, 53), (71, 67, 62, 43)
    fwd = play_chords([I, IV, V, I])
    back = play_chords([I, V, IV, I])
    seq = concat([fwd.at_level(LEVEL), back.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    return {**out, "A": voicing_rows([I, IV, V, I]), "B": voicing_rows([I, V, IV, I]), "starts": {k: float(seq.events[k]) for k in "AB"},
            "clips": {"orders": save("functions.orders", seq, level=None, detail="I-IV-V-I, then I-V-IV-I: a plucked string")}}


def chain(roots, bass0: int, top=(72, 67, 64)) -> list[tuple]:
    """Chords on the given roots, the bass taking the nearest octave, the upper voices the shortest way."""
    out, prev, bass = [], tuple(top), bass0
    for k, (r, kind) in enumerate(roots):
        pcs = [(r + o) % 12 for o in CH.offsets(kind)]
        if k:
            opts = [m for m in range(38, 53) if m % 12 == r]
            bass = min(opts, key=lambda m: abs(m - bass))
        cands = P.upper_voices(pcs, bass, 58, 79)
        last = out[-1] if out else None
        best = min(cands, key=lambda v: (len(F.parallels(last, v + (bass,))) if last else 0, sum(abs(x - y) for x, y in zip(v, prev))))
        out.append(best + (bass,))
        prev = best
    return out


def compute_motion() -> dict:
    b = book()
    falling = chain([(9, "minor"), (2, "minor"), (7, "major"), (0, "major")], 45)
    rising = chain([(0, "major"), (7, "major"), (2, "minor"), (9, "minor")], 48)
    seq = concat([play_chords(falling).at_level(LEVEL), play_chords(rising).at_level(LEVEL)], gap=1.0, names=["A", "B"])
    return {**{m: dict(P.root_motions(b, m)) for m in ("major", "minor")}, "A": voicing_rows(falling), "B": voicing_rows(rising),
            "starts": {k: float(seq.events[k]) for k in "AB"},
            "clips": {"quiz": save("motion.quiz", seq, level=None, detail="vi-ii-V-I (roots falling by fifths), then I-V-ii-vi (rising): a plucked string")}}


def compute_predict() -> dict:
    b = book()
    train, test = BC.split(b, offset=2)
    out = {m: P.predictability(train, test, m) for m in ("major", "minor")}
    # the guessing game: after I and IV, what comes next?
    seqs = P.symbols(train, "major")
    vocab = sorted({x for s in seqs for x in s})
    bi = P.NGram(seqs, 2, vocab, 0.1)
    ctxs = [["I", "IV"], ["ii"], ["V"], ["vi"]]
    guesses = {}
    for ctx in ctxs:
        probs = sorted(((bi.prob(ctx, x), x) for x in vocab), reverse=True)[:5]
        guesses[" ".join(ctx)] = [[x, float(p)] for p, x in probs]
    return {**out, "guesses": guesses, "train": len(train), "test": len(test)}


def compute_sequence() -> dict:
    b = book()
    # the circle of fifths in C: I IV vii iii vi ii V I, the upper voices by the shortest way
    roots = [(0, "major"), (5, "major"), (11, "diminished"), (4, "minor"), (9, "minor"), (2, "minor"), (7, "major"), (0, "major")]
    chords, prev = [], (72, 67, 64)
    bass = 48
    for k, (r, kind) in enumerate(roots):
        pcs = [(r + o) % 12 for o in CH.offsets(kind)]
        if k:                                                     # down a fifth, then up a fourth (diatonically), and so on
            opts = [m for m in range(38, 53) if m % 12 == r]
            bass = min(opts, key=lambda m: (m >= bass) if k % 2 == 1 else (m <= bass)) if len(opts) > 1 else opts[0]
            bass = min([m for m in opts if (m < chords[-1][3]) == (k % 2 == 1)] or opts, key=lambda m: abs(m - chords[-1][3]))
        cands = P.upper_voices(pcs, bass, 58, 79)
        last = chords[-1] if chords else None
        best = min(cands, key=lambda v: (len(F.parallels(last, v + (bass,))) if last else 0, sum(abs(x - y) for x, y in zip(v, prev))))
        chords.append(best + (bass,))
        prev = best
    c = play_chords(chords)
    seq = concat([c.at_level(LEVEL)], gap=0.0, names=["circle"])
    chains = {m: dict(P.fifth_chains(b, m)) for m in ("major", "minor")}
    return {"chords": voicing_rows(chords), "names": ["I", "IV", "vii°", "iii", "vi", "ii", "V", "I"], "chains": chains,
            "times": starts(seq, "circle.", len(chords)),
            "clips": {"circle": save("sequence.circle", seq, level=None, detail="the descending-fifths sequence in C major: a plucked string")}}


def compute_rhythm() -> dict:
    b = book()
    pos, tot = Counter(), Counter()
    for c in b:
        if c.time != (4, 4):
            continue
        prev = None
        for x in F.beat_labels(c):
            p = (x["tick"] % (4 * BC.TICKS)) // BC.TICKS
            s = x["label"][:2] if x["label"] else None
            tot[p] += 1
            if prev is not None and s is not None and s != prev:
                pos[p] += 1
            prev = s if s is not None else prev
    near, far = [0, 0], [0, 0]                         # chord changes within two beats before a fermata, and elsewhere
    for c in b:
        labs = F.beat_labels(c)
        fk = [k for k, x in enumerate(labs) if x["fermata"]]
        for k in range(1, len(labs)):
            a, z = labs[k - 1]["label"], labs[k]["label"]
            if not a or not z:
                continue
            d = min([f - k for f in fk if f >= k] or [99])
            box = near if d <= 2 else far
            box[0] += a[:2] != z[:2]
            box[1] += 1
    return {"change": [pos[k] / tot[k] for k in range(4)], "beats": [tot[k] for k in range(4)], "near_cadence": near[0] / near[1], "elsewhere": far[0] / far[1]}


def compute_octave() -> dict:
    b = book()
    up, down = P.realize_rule("up"), P.realize_rule("down")
    cu, cd = play_chords(up), play_chords(down)
    seq = concat([cu.at_level(LEVEL), cd.at_level(LEVEL)], gap=1.0, names=["up", "down"])
    r = P.bach_vs_rule(b)
    a = sum(v["agree"] for v in r.values())
    w = sum(v["within"] for v in r.values())
    n = sum(v["n"] for v in r.values())
    names = Counter()                                   # what Bach puts over the rising second degree
    for c in b:
        if c.mode != "major":
            continue
        bt = [ch for _, ch, _ in c.beats()]
        for x0, x1, x2 in zip(bt, bt[1:], bt[2:]):
            if 1 <= x1[3] - x0[3] <= 2 and 1 <= x2[3] - x1[3] <= 2 and (x1[3] - c.tonic) % 12 == 2:
                lab = F.label(x1, c.tonic)
                names[F.roman(lab, "major") if lab else "-"] += 1
    return {"up": voicing_rows(up), "down": voicing_rows(down), "rule": P.RULE_OF_OCTAVE, "bach": r, "agree": a / n, "within": w / n, "n": n,
            "up2": names.most_common(5),
            "times": {"up": starts(seq, "up.", 8), "down": starts(seq, "down.", 8)}, "starts": {k: float(seq.events[k]) for k in ("up", "down")},
            "clips": {"updown": save("octave.updown", seq, level=None, detail="the rule of the octave, rising and falling, in C major: a plucked string")}}


# the eight schemata realized in C major: (chord pitch classes, bass key number, melody key number) per event
REAL = {
    "Do-Re-Mi": [((0, 4, 7), 48, 72), ((7, 11, 2), 47, 74), ((0, 4, 7), 48, 76)],
    "Romanesca": [((0, 4, 7), 48, 72), ((7, 11, 2), 47, 67), ((9, 0, 4), 45, 72), ((0, 4, 7), 40, 72)],
    "Prinner": [((5, 9, 0), 53, 69), ((0, 4, 7), 52, 67), ((7, 11, 2, 5), 50, 65), ((0, 4, 7), 48, 64)],
    "Meyer": [((0, 4, 7), 48, 72), ((7, 11, 2, 5), 50, 71), ((7, 11, 2, 5), 47, 77), ((0, 4, 7), 48, 76)],
    "Fonte": [((9, 1, 4, 7), 49, 79), ((2, 5, 9), 50, 77), ((7, 11, 2, 5), 47, 77), ((0, 4, 7), 48, 76)],
    "Monte": [((0, 4, 7, 10), 52, 70), ((5, 9, 0), 53, 69), ((2, 6, 9, 0), 54, 72), ((7, 11, 2), 55, 71)],
    "Ponte": [((7, 11, 2), 43, 67), ((7, 11, 2), 43, 71), ((7, 11, 2), 43, 74), ((7, 11, 2, 5), 43, 77)],
    "Quiescenza": [((0, 4, 7, 10), 48, 70), ((5, 9, 0), 48, 69), ((7, 11, 2), 48, 71), ((0, 4, 7), 48, 72)],
}
SCHEMA_TEXT = {
    "Do-Re-Mi": "an opening: the melody climbs 1-2-3 over 1-7-1",
    "Romanesca": "an opening: a bass falling by step or leap under a steady melody",
    "Prinner": "a reply: the melody falls 6-5-4-3 over a bass 4-3-2-1",
    "Meyer": "an opening: 1-7 answered by 4-3",
    "Fonte": "after the double bar: the same step twice, a tone lower, minor then major",
    "Monte": "after the double bar: the same step twice, a tone higher",
    "Ponte": "a bridge: the dominant held while the melody climbs",
    "Quiescenza": "after a cadence: a tonic pedal, 7-6 in the melody, flat then sharp",
}


def realize(events, prev=(72, 67, 64)) -> list[tuple]:
    out = []
    for pcs, bass, mel in events:
        cands = [v for v in P.upper_voices(pcs, bass, 55, 84) if v[0] == mel]
        last = out[-1] if out else None
        best = min(cands, key=lambda v: (len(F.parallels(last, v + (bass,))) if last else 0, sum(abs(x - y) for x, y in zip(v, prev))))
        out.append(best + (bass,))
        prev = best
    return out


def compute_schemata() -> dict:
    out, clips, names = {}, [], []
    for name, ev in REAL.items():
        ch = realize(ev)
        out[name] = {"chords": voicing_rows(ch), "text": SCHEMA_TEXT[name], "bass": [e[1] for e in ev], "melody": [e[2] for e in ev]}
        clips.append(play_chords(ch).at_level(LEVEL))
        names.append(name)
    seq = concat(clips, gap=0.8, names=names)
    for name in names:
        out[name]["times"] = starts(seq, f"{name}.", len(REAL[name]))
    # a little galant phrase: Do-Re-Mi, Prinner; after the double bar Fonte, Monte, Ponte; a cadence
    plan = ["Do-Re-Mi", "Prinner", "Fonte", "Monte", "Ponte"]
    cadence = [((2, 5, 9), 53, 74), ((0, 4, 7), 55, 72), ((7, 11, 2, 5), 43, 71), ((0, 4, 7), 48, 72)]
    events = [e for p in plan for e in REAL[p]] + cadence
    ch = realize(events)
    phrase = play_chords(ch, seconds=HALF * 0.85)
    ps = concat([phrase.at_level(LEVEL)], gap=0.0, names=["phrase"])
    bounds, k = [], 0
    for p in plan + ["cadence"]:
        n = len(REAL[p]) if p != "cadence" else len(cadence)
        bounds.append([p, k, k + n])
        k += n
    return {"schemata": out, "order": names, "starts": {n: float(seq.events[n]) for n in names}, "phrase": voicing_rows(ch), "plan": bounds,
            "phrase_times": starts(ps, "phrase.", len(ch)),
            "clips": {"eight": save("schemata.eight", seq, level=None, detail="eight galant schemata in C major: a plucked string"),
                      "phrase": save("schemata.phrase", ps, level=None, detail="a phrase assembled from schemata: Do-Re-Mi, Prinner, Fonte, Monte, Ponte, cadence")}}


def compute_census() -> dict:
    b = book()
    ch = P.schema_census(b)
    # melodies: the Prinner's 6-5-4-3 and the Do-Re-Mi's 1-2-3 in the series' fifty-four tunes, against shuffled tunes
    tunes = M.corpus()
    pats = {"6-5-4-3": [9, 7, 5, 4], "1-2-3": [0, 2, 4], "4-3-2-1": [5, 4, 2, 0], "5-4-3-2-1": [7, 5, 4, 2, 0]}
    rng = np.random.default_rng(0)

    def has(seq, pat):
        s = [x % 12 for k, x in enumerate(seq) if k == 0 or x != seq[k - 1]]
        return any(s[k:k + len(pat)] == pat for k in range(len(s) - len(pat) + 1))
    mel_stats = {}
    for name, pat in pats.items():
        real = sum(has(t.pitches, pat) for t in tunes if t.mode == "major")
        shuf = np.mean([sum(has(list(rng.permutation(t.pitches)), pat) for t in tunes if t.mode == "major") for _ in range(50)])
        mel_stats[name] = {"real": int(real), "shuffled": float(shuf)}
    n_major = sum(t.mode == "major" for t in tunes)
    # the Tune from its sixth note: A A G | F F E E | D D C, the Prinner's melody 6-5-4-3 over its bass 4-3-2-1, then a cadence
    tune = tunes[0]
    mel = [(72 + p, a, d) for p, a, d in zip(tune.pitches[4:14], np.cumsum([0] + list(tune.beats[4:13])), tune.beats[4:14])]
    plan = [((5, 9, 0), 53), ((0, 4, 7), 52), ((7, 11, 2, 5), 50), ((0, 4, 7), 48), ((7, 11, 2), 43), ((0, 4, 7), 48)]
    chords, prev = [], (69, 65)
    for k, (pcs, bass) in enumerate(plan):
        top = next(p for p, a, d in mel if 2 * k <= a < 2 * k + 2)
        cands = [x for x in P.upper_voices(pcs, bass, 50, 84) if x[0] == top]
        last = chords[-1] if chords else None
        best = min(cands, key=lambda x: (len(F.parallels(last, x + (bass,))) if last else 0, abs(x[1] - prev[0]) + abs(x[2] - prev[1])))
        chords.append(best + (bass,))
        prev = best[1:]
    beat = HALF * 0.9
    placed, ev = [], {}
    for k, (p, a, d) in enumerate(mel):
        placed.append((harpsichord(p, d * beat * 1.3), a * beat, 0.0))
        ev[f"m{k}"] = a * beat
    for k, chd in enumerate(chords):
        for j, m in enumerate(chd[1:]):
            placed.append((harpsichord(m, 2 * beat * 1.3), 2 * k * beat + 0.012 * (3 - j), -3.0))
        ev[f"c{k}"] = 2 * k * beat
    clp = Clip(mix(placed, duration=12 * beat + 1.2).y, SR, ev, []).at_level(LEVEL)
    seq = concat([clp], gap=0.0, names=["prinner"])
    return {"chorales": ch, "melodies": mel_stats, "tunes_major": n_major, "chorales_major": sum(c.mode == "major" for c in b),
            "prinner": {"chords": voicing_rows(chords), "names": ["IV", "I6", "V4/3", "I", "V", "I"], "times": [float(seq.events[f"prinner.c{k}"]) for k in range(len(chords))],
                        "melody": [[int(p), float(a), float(d)] for p, a, d in mel]},
            "clips": {"prinner": save("census.prinner", seq, level=None, detail="the Tune from its fifth note, A A G F F E E D D C, over a Prinner's bass and a cadence")}}


def compute_grounds() -> dict:
    out, clips, names = {}, [], []
    for name in ("lament", "folia", "romanesca", "passamezzo"):
        ch = P.ground_voicings(name)
        out[name] = {"chords": voicing_rows(ch), "text": P.GROUNDS[name]["text"], "mode": P.GROUNDS[name]["mode"]}
        clips.append(play_chords(ch + ch, seconds=HALF * 0.9).at_level(LEVEL))
        names.append(name)
    seq = concat(clips, gap=0.9, names=names)
    for name in names:
        out[name]["times"] = starts(seq, f"{name}.", 2 * len(out[name]["chords"]))
    return {"grounds": out, "order": names, "starts": {n: float(seq.events[n]) for n in names},
            "clips": {"four": save("grounds.four", seq, level=None, detail="four ground basses, each twice: lament, Folia, Romanesca, passamezzo antico")}}


# Variation 18: the Tune (two phrases, 16 beats, a chord a half bar) over three basses
VAR = {
    "Romanesca": {"mode": "major", "chords": [(0, 4, 7), (7, 11, 2), (9, 0, 4), (4, 7, 11), (5, 9, 0), (0, 4, 7), (7, 11, 2), (0, 4, 7)],
                  "bass": [48, 47, 45, 40, 41, 43, 43, 36], "names": ["I", "V6", "vi", "iii", "IV", "I6/4", "V", "I"]},
    "lament": {"mode": "minor", "chords": [(0, 3, 7), (7, 11, 2), (10, 2, 5, 8), (9, 0, 3, 7), (5, 8, 0), (0, 3, 7), (7, 11, 2), (0, 3, 7)],
               "bass": [48, 47, 46, 45, 44, 43, 43, 36], "names": ["i", "V6", "V4/2 of III", "vi\u00f87", "iv6", "i6/4", "V", "i"]},
    "pedals": {"mode": "major", "chords": [(0, 4, 7), (0, 4, 7), (5, 9, 0), (0, 4, 7), (7, 11, 2, 5), (0, 4, 7), (7, 11, 2), (0, 4, 7)],
               "bass": [36, 36, 36, 36, 43, 43, 43, 36], "names": ["I", "I", "IV/C", "I", "V7", "I6/4", "V", "I"]},
}


def compute_tune() -> dict:
    tune = M.corpus()[0]
    pitches = tune.pitches[:14]
    beats = tune.beats[:14]
    out, clips, names = {}, [], []
    for name, v in VAR.items():
        mel = [72 + p - (1 if v["mode"] == "minor" and p % 12 in (4, 9, 11) else 0) for p in pitches]
        # a chord every two beats; the melody as written above it
        events, t = [], 0.0
        for p, bt in zip(mel, beats):
            events.append((p, t, bt))
            t += bt
        chords = []
        prev = (67, 64)
        for k, (pcs, bass) in enumerate(zip(v["chords"], v["bass"])):
            notes_here = [p for p, a, d in events if 2 * k <= a < 2 * k + 2]
            top = notes_here[0]
            cands = [x for x in P.upper_voices(pcs, bass, 50, 84) if x[0] == top]
            if not cands:
                cands = [(top,) + x[1:] for x in P.upper_voices(pcs, bass, 50, 84) if x[1] < top]
            last = chords[-1] if chords else None
            best = min(cands, key=lambda x: (len(F.parallels(last, x + (bass,))) if last else 0, abs(x[1] - prev[0]) + abs(x[2] - prev[1])))
            chords.append(best + (bass,))
            prev = best[1:]
        beat = HALF * 0.9
        placed, ev = [], {}
        for k, (p, a, d) in enumerate(events):
            placed.append((harpsichord(p, d * beat * 1.3), a * beat, 0.0))
            ev[f"m{k}"] = a * beat
        for k, ch in enumerate(chords):
            for j, m in enumerate(ch[1:]):
                placed.append((harpsichord(m, 2 * beat * 1.3), 2 * k * beat + 0.012 * (3 - j), -3.0))
            ev[f"c{k}"] = 2 * k * beat
        c = Clip(mix(placed, duration=16 * beat + 1.2).y, SR, ev, []).at_level(LEVEL)
        out[name] = {"melody": [[int(p), float(a), float(d)] for p, a, d in events], "chords": voicing_rows(chords), "names": v["names"], "mode": v["mode"],
                     "parallels": [k for k, (a, b) in enumerate(zip(chords, chords[1:])) if F.parallels(a, b)]}
        clips.append(c)
        names.append(name)
    seq = concat(clips, gap=1.2, names=names)
    for name in names:
        out[name]["times_m"] = [float(seq.events[f"{name}.m{k}"]) for k in range(len(pitches))]
        out[name]["times_c"] = [float(seq.events[f"{name}.c{k}"]) for k in range(8)]
    return {"versions": out, "order": names, "starts": {n: float(seq.events[n]) for n in names}, "seconds": seq.duration,
            "clip": {"name": "tune.variation18", "seconds": seq.duration},
            "clips": {"variation": save("tune.variation18", seq, level=None, detail="the Tune over the Romanesca, a lament bass, and two pedals: a plucked string")}}


def compute_variation() -> dict:
    t = load("tune")
    n_par = sum(len(v["parallels"]) for v in t["versions"].values())
    return {"part": 18, "title": r"over the Romanesca, a lament bass, and two pedals: three basses, one tune", "seconds": round(t["seconds"], 2),
            "measure": rf"24 chords, every one holding the Tune's note; {n_par} parallel fifths or octaves", "clip": "tune.variation18"}


def compute_more() -> dict:
    """An unfigured bass realized by rule; the rising 5-6 sequence; a schema plain and decorated."""
    out, clips = {}, {}
    # 1. a partimento: C E F G A G F D G C, unfigured, realized by the rule of the octave
    bass = [48, 52, 53, 55, 57, 55, 53, 50, 55, 48]
    real = P.realize_bass(bass)
    chords = [x["chord"] for x in real]
    a, b = play_line(bass, seconds=HALF), play_chords(chords)
    seq = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["bass", "full"])
    out["partimento"] = {"bass": bass, "chords": voicing_rows(chords), "how": [x["how"] for x in real], "figures": [x["figure"] for x in real],
                         "times": {"bass": starts(seq, "bass.", len(bass), "n"), "full": starts(seq, "full.", len(chords))},
                         "starts": {k: float(seq.events[k]) for k in ("bass", "full")}}
    clips["partimento"] = save("more.partimento", seq, level=None, detail="an unfigured bass, alone; then realized by the rule of the octave")
    # 2. the rising 5-6 sequence: over a bass climbing by step, each note first a fifth, then a sixth
    plan = [((0, 4, 7), 48), ((9, 0, 4), 48), ((2, 5, 9), 50), ((11, 2, 5), 50), ((4, 7, 11), 52), ((0, 4, 7), 52), ((5, 9, 0), 53), ((7, 11, 2), 55), ((0, 4, 7), 48)]
    seq56, prev = [], (67, 64, 60)
    for pcs, bs in plan:
        cands = P.upper_voices(pcs, bs, 55, 79)
        last = seq56[-1] if seq56 else None
        best = min(cands, key=lambda v: (len(F.parallels(last, v + (bs,))) if last else 0, sum(abs(x - y) for x, y in zip(v, prev))))
        seq56.append(best + (bs,))
        prev = best
    c56 = concat([play_chords(seq56, seconds=HALF * 0.8).at_level(LEVEL)], gap=0.0, names=["s"])
    out["fivesix"] = {"chords": voicing_rows(seq56), "names": ["I", "vi6", "ii", "vii\u00b06", "iii", "I6", "IV", "V", "I"], "times": starts(c56, "s.", len(seq56))}
    clips["fivesix"] = save("more.fivesix", c56, level=None, detail="the rising 5-6 sequence in C major: a plucked string")
    # 3. diminution: the Prinner plain, then with its melody decorated in quick notes
    plain = realize(REAL["Prinner"])
    deco = [[69, 71, 72, 69], [67, 65, 64, 67], [65, 64, 62, 65], [64, 62, 60, 64]]     # passing notes between chord notes
    beat = HALF
    placed, ev = [], {}
    for k, ch in enumerate(plain):
        for j, m in enumerate(ch[1:]):
            placed.append((harpsichord(m, 2 * beat * 1.3), 2 * k * beat + 0.012 * (3 - j), -3.0))
        for i, m in enumerate(deco[k]):
            placed.append((harpsichord(m, beat * 0.7), 2 * k * beat + i * beat / 2, 0.0))
        ev[f"c{k}"] = 2 * k * beat
    dec = Clip(mix(placed, duration=8 * beat + 1.0).y, SR, ev, [])
    pl = play_chords(plain, seconds=2 * beat)
    seqd = concat([pl.at_level(LEVEL), dec.at_level(LEVEL)], gap=1.0, names=["plain", "decorated"])
    out["diminution"] = {"plain": voicing_rows(plain), "decorated": deco, "times": {"plain": starts(seqd, "plain.", 4), "decorated": starts(seqd, "decorated.", 4)},
                         "starts": {k: float(seqd.events[k]) for k in ("plain", "decorated")}}
    clips["diminution"] = save("more.diminution", seqd, level=None, detail="a Prinner plain, then with its melody decorated: a plucked string")
    # 4. a variation over the Folia: the ground twice, plain, then with a running melody above it
    fol = P.ground_voicings("folia")
    beat = HALF * 0.9
    placed, ev = [], {}
    run = []
    for k, ch in enumerate(fol + fol):
        t0 = 2 * k * beat
        for j, m in enumerate(ch[1:] if k >= len(fol) else ch):
            placed.append((harpsichord(m, 2 * beat * 1.3), t0 + 0.012 * j, -3.0 if k >= len(fol) else -1.0))
        ev[f"c{k}"] = t0
        if k >= len(fol):                                         # the chord broken into running notes: tenor, soprano, alto, soprano
            t_ = ch[2] if ch[2] >= 57 else ch[2] + 12
            figure = [t_, ch[0], ch[1], ch[0]]
            for i, m in enumerate(figure):
                placed.append((harpsichord(m, beat * 0.6), t0 + i * beat / 2, 0.0))
            run.append(figure)
    clip_f = Clip(mix(placed, duration=4 * len(fol) * beat + 1.2).y, SR, ev, [])
    seqf = concat([clip_f.at_level(LEVEL)], gap=0.0, names=["f"])
    out["folia"] = {"chords": voicing_rows(fol + fol), "run": run, "times": starts(seqf, "f.", 2 * len(fol)), "rounds": len(fol)}
    clips["folia"] = save("more.folia", seqf, level=None, detail="la Folia twice: the chords, then a running melody over them: a plucked string")
    out["clips"] = clips
    return out


ITEMS = {"hook": compute_hook, "functions": compute_functions, "motion": compute_motion, "predict": compute_predict, "sequence": compute_sequence,
         "rhythm": compute_rhythm, "octave": compute_octave, "schemata": compute_schemata, "census": compute_census, "grounds": compute_grounds,
         "tune": compute_tune, "variation": compute_variation, "more": compute_more}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
