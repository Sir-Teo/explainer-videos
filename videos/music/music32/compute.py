"""Precompute everything numerical, and every sound, in Part 32 of *Music, Built* ("The Geometry of Chords").

    python -m videos.music.music32.compute              # everything missing (about a minute)
    python -m videos.music.music32.compute --force bach

Numbers are cached in ``.cache/music32/<name>.json``, sounds in ``.cache/music32/audio/``.  The geometry is Monochord's
(``explainer/music/monochord/geometry.py``); Bach's chorales are Part 17's.  The gliding voices are synthesized; every
chord is played on Part 7's piano.

Items:
    hook        two voices that cross, and two that meet and turn back (an ear question: which crosses?)
    strip       the 78 two-note chords on the Möbius strip; parallel, contrary and oblique motion, heard
    duet        Fux's cantus with a first-species line (Part 16's best), drawn as a path on the Möbius strip, heard
    neutral     C major gliding to C minor through the neutral triad (E a quarter tone flat): a continuous path, heard
    triangle    every three-note chord type as a point of the triangle of shapes; from a cluster to the augmented triad, heard
    vlsize      C major to F major three ways, and the sizes under three norms (an ear question: which is smoother?)
    even        evenness against the smallest voice leading to a transposition, for every 3- and 4-note set class;
                three nearly even chords moving to transpositions, heard
    scales      the seven-note scales ranked by evenness; C major to G major to D major, one semitone each, heard
    mirror      C major and its mirror image about C (F minor), heard: the I of OPTIC
    optic       chord types of three and four notes under each combination of O, P, T, I and C
    fourier     the largest Fourier magnitude for each coefficient and size; three champions, heard (an ear question)
    bach        Bach's voice leadings against the minimal ones in 364 chorales, with a shuffled control; one phrase of
                *Wachet auf* (BWV 140.7), and the same chords with their voices reassigned (an ear question)
    tune        Variation 32: the Tune's harmony as a path of smallest voice leadings, then rerouted through chromatic chords
    variation   the Variations ledger, row 32
"""

from __future__ import annotations

from itertools import combinations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import atonal as A
from explainer.music.monochord import chorales as CH
from explainer.music.monochord import geometry as G
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music32")
CLIPS = ClipStore("music32")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
BOARD = STR.soundboard()
C4 = 261.6255653005986
_P: dict = {}
PCN = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def piano(m: float, seconds: float, velocity: float = 1.0) -> Clip:
    seconds = round(min(max(seconds, 0.12), 3.5), 2)
    key = (round(m, 3), seconds, round(velocity, 2))
    if key not in _P:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4),
                                  velocity=velocity, seconds=seconds + 0.3))
        _P[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _P[key]


def chords_clip(chords, unit=1.0, gap=0.0, bass=False, vel=0.9):
    """Chords given as lists of key numbers, one after another; notes [key, onset (units), duration]."""
    parts, notes = [], []
    for i, ch in enumerate(chords):
        for m in ch:
            parts.append((piano(m, unit * 1.05, vel), i * (unit + gap), -2.0))
            notes.append([float(m), float(i), 1.0])
    return Clip(mix(parts, duration=len(chords) * (unit + gap) + 1.2).y, SR), notes


def glide_voice(path, seconds, phase=0.0, partials=6, rolloff=0.55):
    """A synthesized voice whose pitch follows ``path`` (key numbers, piecewise linear over ``seconds``)."""
    n = int(seconds * SR)
    t = np.linspace(0, 1, n)
    xs = np.linspace(0, 1, len(path))
    m = np.interp(t, xs, path)
    f = hz(m)
    ph = phase + 2 * np.pi * np.cumsum(f) / SR
    y = sum(rolloff ** k * np.sin((k + 1) * ph) for k in range(partials))
    env = np.minimum(1, np.minimum(t * seconds / 0.08, (1 - t) * seconds / 0.15))
    return y * env


def rows(v):
    return [[float(p), float(a), float(d)] for p, a, d in v]


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    sec = 4.0
    # A: the voices cross; B: they meet in the middle and turn back.  At every moment the two pitches are the same.
    a = glide_voice([60, 64], sec) + glide_voice([64, 60], sec, phase=1.0)
    b = glide_voice([60, 62, 60], sec) + glide_voice([64, 62, 64], sec, phase=1.0)
    ca, cb = Clip(a, SR).fade(0.02, 0.1), Clip(b, SR).fade(0.02, 0.1)
    s_ = concat([ca.at_level(LEVEL), cb.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    t = np.linspace(0, 1, 50)
    same = bool(np.allclose(np.sort(np.c_[60 + 4 * t, 64 - 4 * t], axis=1),
                            np.sort(np.c_[np.interp(t, [0, .5, 1], [60, 62, 60]), np.interp(t, [0, .5, 1], [64, 62, 64])], axis=1)))
    return {"answer": "neither", "same_pitches": same, "seconds": sec, "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save_synth("hook.quiz", s_, detail="two synthesized voices, C4 and E4, gliding: in A they cross; in B they meet on D4 and turn back")}}


def compute_strip() -> dict:
    pts = []
    for a, b in G.dyads():
        c, d = G.dyad_strip(a, b)
        pts.append({"a": a, "b": b, "c": c, "d": d, "ic": min((b - a) % 12, (a - b) % 12)})
    # parallel minor thirds rising by semitones, contrary motion from a unison outwards, oblique motion against a held C
    par = [[60, 63], [61, 64], [62, 65], [63, 66], [64, 67]]
    con = [[62, 62], [61, 63], [60, 64], [59, 65], [58, 66]]
    obl = [[60, 62], [60, 64], [60, 66], [60, 67], [60, 69]]
    clips, out = [], {}
    for name, seq in (("parallel", par), ("contrary", con), ("oblique", obl)):
        c, notes = chords_clip(seq, unit=0.8)
        clips.append(c.at_level(LEVEL))
        out[name] = {"chords": seq, "points": [list(G.dyad_strip(*ch)) for ch in seq], "notes": notes}
    s_ = concat(clips, gap=0.9, names=["parallel", "contrary", "oblique"])
    return {"points": pts, "motions": out, "unit": 0.8, "starts": {k: float(s_.events[k]) for k in out},
            "clips": {"three": save("strip.three", s_, detail="parallel minor thirds rising by semitones, contrary motion from a unison out to a tritone, and oblique motion against a held C; Part 7's piano")}}


def compute_duet() -> dict:
    from explainer.music.monochord import counterpoint as CP
    cf = CP.FUX_DORIAN
    cp = CP.best(cf)
    pts = [list(G.dyad_strip(a, b)) for a, b in zip(cf, cp)]
    seq = [[a, b] for a, b in zip(cf, cp)]
    c, notes = chords_clip(seq, unit=0.8)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["duet"])
    ivs = [b - a for a, b in zip(cf, cp)]
    sizes = [G.vl([a0 % 12, b0 % 12], [a1 % 12, b1 % 12])[0] for (a0, b0), (a1, b1) in zip(seq, seq[1:])]
    actual = [abs(a1 - a0) + abs(b1 - b0) for (a0, b0), (a1, b1) in zip(seq, seq[1:])]
    return {"cf": cf, "cp": cp, "points": pts, "intervals": ivs, "unit": 0.8, "notes": notes, "sizes": sizes, "actual": actual,
            "clips": {"duet": save("duet.first", s_, detail="Fux's Dorian cantus firmus with a first-species counterpoint above it (Part 16's best line); Part 7's piano")}}


def compute_neutral() -> dict:
    steps = [64.0, 63.75, 63.5, 63.25, 63.0]
    seq = [[60, e, 67] for e in steps]
    c, notes = chords_clip(seq, unit=1.3, gap=0.2)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["glide"])
    return {"thirds": steps, "even": [G.evenness([0, e - 60, 7]) for e in steps],
            "xy": [list(G.triangle_xy((e - 60, 67 - e, 5))) for e in steps], "unit": 1.5,
            "clips": {"glide": save("neutral.glide", s_, detail="C major to C minor in five chords, the third lowered a quarter of a semitone at a time, through the neutral triad; Part 7's piano")}}


def compute_triangle() -> dict:
    pts = []
    for a in range(13):
        for b in range(13 - a):
            c = 12 - a - b
            x, y = G.triangle_xy((a, b, c))
            ch = [0, a % 12, (a + b) % 12]
            pf = A.prime_form(sorted(set(ch))) if len(set(ch)) == 3 else None
            pts.append({"steps": [a, b, c], "x": x, "y": y, "prime": list(pf) if pf else None,
                        "even": G.evenness(ch)})
    walk = [[60, 61, 62], [60, 62, 64], [60, 63, 66], [60, 64, 67], [60, 64, 68]]
    names = ["cluster", "whole tones", "diminished", "major", "augmented"]
    c, notes = chords_clip(walk, unit=1.3, gap=0.25)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["walk"])
    return {"points": pts, "walk": walk, "names": names, "walk_even": [G.evenness(w) for w in walk],
            "walk_xy": [list(G.triangle_xy(G.shape(w))) for w in walk], "unit": 1.55, "notes": notes,
            "clips": {"walk": save("triangle.walk", s_, detail="from a cluster to the augmented triad, each chord more evenly spread: C C♯ D, C D E, C E♭ G♭, C E G, C E G♯; Part 7's piano")}}


def compute_vlsize() -> dict:
    a = [60, 64, 67]
    ways = {"A": [60, 65, 69], "B": [65, 69, 72]}                  # the smallest; everything up a fourth
    out = {}
    for k, b in ways.items():
        mv = [q - p for p, q in zip(a, b)]
        out[k] = {"to": b, "moves": mv, "taxicab": float(sum(abs(x) for x in mv)),
                  "euclid": float(np.sqrt(sum(x * x for x in mv))), "max": float(max(abs(x) for x in mv))}
    third = [57, 65, 72]                                           # C E G -> A F C: C down to A, E up to F, G up to C
    mv3 = [q - p for p, q in zip(a, third)]
    out["C"] = {"to": third, "moves": mv3, "taxicab": float(sum(abs(x) for x in mv3)), "euclid": float(np.sqrt(sum(x * x for x in mv3))),
                "max": float(max(abs(x) for x in mv3))}
    best = G.vl([0, 4, 7], [5, 9, 0])
    clips = []
    for k in "AB":
        c, _ = chords_clip([a, ways[k], a, ways[k]], unit=0.9)
        clips.append(c.at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=["A", "B"])
    # C major to every major and minor triad: the smallest sizes
    tri = {}
    for r in range(12):
        for q, iv in (("M", (0, 4, 7)), ("m", (0, 3, 7))):
            tri[PCN[r] + ("" if q == "M" else "m")] = G.vl([0, 4, 7], [(r + i) % 12 for i in iv])[0]
    return {"ways": out, "best": best[0], "best_moves": best[1], "answer": "A", "starts": {k: float(s_.events[k]) for k in "AB"},
            "unit": 0.9, "triads": tri,
            "clips": {"quiz": save("vlsize.quiz", s_, detail="C major to F major twice in two voice leadings: A the smallest (G to A, E to F, C held), B every voice up a fourth; Part 7's piano")}}


def compute_even() -> dict:
    rows_ = []
    for size in (3, 4):
        for c in sorted({A.prime_form(x) for x in combinations(range(12), size)}):
            v, k = G.nearest_transposition(c)
            rows_.append({"size": size, "prime": list(c), "even": G.evenness(c), "vl": v, "k": k})
    demo = [("major", [60, 64, 67], 4), ("dominant seventh", [60, 64, 67, 70], 3), ("diatonic scale", [60, 62, 64, 65, 67, 69, 71], 7)]
    clips, out = [], []
    for name, ch, k in demo:
        pcs = [m % 12 for m in ch]
        size, mv = G.vl(pcs, [(p + k) % 12 for p in pcs])
        tgt = [m + d for m, d in zip(ch, mv)]
        if name == "diatonic scale":
            seq = [[m] for m in ch] + [[m] for m in sorted(tgt)]
            c, _ = chords_clip(seq, unit=0.32)
        else:
            c, _ = chords_clip([ch, tgt, ch, tgt], unit=0.95)
        clips.append(c.at_level(LEVEL))
        out.append({"name": name, "from": ch, "to": tgt, "k": k, "size": size, "moves": mv})
    s_ = concat(clips, gap=1.0, names=[d["name"] for d in out])
    for size in (3, 4):
        r = [x for x in rows_ if x["size"] == size]
        e = np.array([x["even"] for x in r])
        v = np.array([x["vl"] for x in r])
    best = {s: sorted([x for x in rows_ if x["size"] == s], key=lambda x: (x["vl"], x["even"]))[:3] for s in (3, 4)}
    return {"rows": rows_, "demos": out, "starts": {d["name"]: float(s_.events[d["name"]]) for d in out}, "best": {str(k): v for k, v in best.items()},
            "clips": {"three": save("even.three", s_, detail="C major to E major and back; C7 to E flat 7 and back; the C major scale, then the G major scale; Part 7's piano")}}


def compute_scales() -> dict:
    seven = sorted({A.prime_form(c) for c in combinations(range(12), 7)})
    ranked = sorted(seven, key=lambda c: G.evenness(c))
    named = {A.prime_form([0, 2, 4, 5, 7, 9, 11]): "diatonic", A.prime_form([0, 2, 3, 5, 7, 9, 11]): "melodic minor / acoustic set class",
             A.prime_form([0, 2, 3, 5, 7, 8, 11]): "harmonic minor (and harmonic major)", A.prime_form([0, 2, 4, 6, 8, 10, 11]): "whole-tone plus one"}
    top = [{"prime": list(c), "even": G.evenness(c), "name": named.get(tuple(c), "")} for c in ranked[:6]]
    keys = [[60, 62, 64, 65, 67, 69, 71], [60, 62, 64, 66, 67, 69, 71], [61, 62, 64, 66, 67, 69, 71]]
    seq = []
    for k in keys:
        seq += [[m] for m in k] + [[72 if k[0] == 60 else 73]]
    c, notes = chords_clip(seq, unit=0.3)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["keys"])
    hm = A.prime_form([0, 2, 3, 5, 7, 8, 11])
    mm = A.prime_form([0, 2, 3, 5, 7, 9, 11])
    return {"count": len(seven), "top": top, "harmonic_minor": {"prime": list(hm), "rank": ranked.index(hm) + 1, "even": G.evenness(hm)},
            "melodic_minor": {"prime": list(mm), "rank": ranked.index(mm) + 1, "even": G.evenness(mm)},
            "diatonic_even": G.evenness([0, 2, 4, 5, 7, 9, 11]),
            "circle": {str(k): G.vl([0, 2, 4, 5, 7, 9, 11], [(x + k) % 12 for x in [0, 2, 4, 5, 7, 9, 11]])[0] for k in range(12)}, "notes": notes, "unit": 0.3,
            "steps": [G.vl([m % 12 for m in a], [m % 12 for m in b])[0] for a, b in zip(keys, keys[1:])],
            "clips": {"keys": save("scales.keys", s_, detail="the C major scale, then G major (F becomes F sharp), then D major (C becomes C sharp); Part 7's piano")}}


def compute_mirror() -> dict:
    up = [60, 64, 67]
    down = [60, 56, 53]
    seq = [[m] for m in up] + [up] + [[m] for m in down] + [sorted(down)]
    c, notes = chords_clip(seq, unit=0.6, gap=0.05)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["mirror"])
    return {"up": up, "down": down, "steps_up": [4, 3], "steps_down": [-4, -3], "unit": 0.65, "notes": notes,
            "clips": {"mirror": save("mirror.two", s_, detail="C, E, G up from C, then its mirror image down from C: C, A flat, F; each as a chord; Part 7's piano")}}


def compute_optic() -> dict:
    return {"3": G.optic_counts(3), "4": G.optic_counts(4), "2": G.optic_counts(2)}


def compute_fourier() -> dict:
    champs = {str(s): {str(k): {"value": v["value"], "sets": [list(x) for x in v["sets"]]} for k, v in G.dft_champions(s).items()}
              for s in (3, 4, 5, 6, 7)}
    examples = {"major": [0, 4, 7], "minor": [0, 3, 7], "augmented": [0, 4, 8], "diminished seventh": [0, 3, 6, 9],
                "pentatonic": [0, 2, 4, 7, 9], "diatonic": [0, 2, 4, 5, 7, 9, 11], "whole tone": [0, 2, 4, 6, 8, 10],
                "hexatonic": [0, 1, 4, 5, 8, 9], "cluster": [0, 1, 2, 3]}
    mags = {k: [float(x) for x in G.dft(v)] for k, v in examples.items()}
    # the ear question: which of three chords is richest in fifths (largest |F5|)?  A pentatonic, a hexatonic, a whole-tone chord
    order = ["hexatonic", "pentatonic", "whole tone"]
    voiced = {"pentatonic": [55, 60, 62, 64, 67, 69], "hexatonic": [55, 56, 59, 60, 63, 64], "whole tone": [54, 56, 58, 60, 62, 64]}
    clips = []
    for k in order:
        c, _ = chords_clip([voiced[k], voiced[k]], unit=1.4, gap=0.1)
        clips.append(c.at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=list("ABC"))
    f5 = [mags[k][5] for k in order]
    return {"champions": champs, "mags": mags, "order": order, "answer": "ABC"[int(np.argmax(f5))], "f5": f5,
            "f3": [mags[k][3] for k in order], "f6": [mags[k][6] for k in order], "starts": {k: float(s_.events[k]) for k in "ABC"},
            "clips": {"quiz": save("fourier.quiz", s_, detail="three six-note chords: A on the hexatonic scale, B on the pentatonic scale with G below, C on the whole-tone scale; Part 7's piano")}}


def _phrase(c, end_tick):
    notes = []
    for v in c.voices:
        for p, o, d, _ in v:
            if o <= end_tick:
                notes.append((p, o / CH.TICKS, d / CH.TICKS))
    return notes


def compute_bach() -> dict:
    book = CH.load()
    allv = G.bach_voice_leading(book)
    upper = G.bach_voice_leading(book, upper_only=True)
    c = [x for x in book if x.name == "bwv140.7"][0]
    end = c.phrases()[0]
    beats = [b for b in c.beats() if b[0] <= end]
    t0 = beats[0][0]
    changes = []
    for (ta, a, _), (tb, b, _) in zip(beats, beats[1:]):
        if a == b:
            continue
        act = sum(abs(q - p) for p, q in zip(a, b))
        mn = G.vl([p % 12 for p in a], [q % 12 for q in b])[0]
        act3 = sum(abs(q - p) for p, q in zip(a[:3], b[:3]))
        mn3 = G.vl([p % 12 for p in a[:3]], [q % 12 for q in b[:3]])[0]
        changes.append({"t": (tb - t0) / CH.TICKS, "actual": act, "minimal": mn, "actual3": act3, "minimal3": mn3})
    # the quiz: A, Bach's beat chords as he voices them; B, the same chords with the upper voices' notes reassigned at random
    rng = np.random.default_rng(32)
    chords_a = [list(b[1]) for b in beats]
    chords_b = []
    for ch in chords_a:
        up = list(ch[:3])
        perm = rng.permutation(3)
        new = [up[i] for i in perm]
        # keep each voice in its own register: move each note by octaves towards that voice's original note
        fixed = []
        for j, m in enumerate(new):
            while m - ch[j] > 6:
                m -= 12
            while ch[j] - m > 6:
                m += 12
            fixed.append(m)
        chords_b.append(fixed + [ch[3]])
    unit = 0.75
    ca, na = chords_clip(chords_a, unit=unit)
    cb, nb = chords_clip(chords_b, unit=unit)
    tot_a = sum(sum(abs(q - p) for p, q in zip(x[:3], y[:3])) for x, y in zip(chords_a, chords_a[1:]))
    tot_b = sum(sum(abs(q - p) for p, q in zip(x[:3], y[:3])) for x, y in zip(chords_b, chords_b[1:]))
    s_ = concat([ca.at_level(LEVEL), cb.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    # the phrase itself, every note, heard
    ph = _phrase(c, end)
    pt0 = min(o for _, o, _ in ph)
    parts = [(piano(p, min(d * 0.6, 3.0), 0.9), (o - pt0) * 0.6, -2.0) for p, o, d in ph]
    cp = Clip(mix(parts, duration=max(o - pt0 + d for _, o, d in ph) * 0.6 + 1.2).y, SR)
    s2 = concat([cp.at_level(LEVEL)], gap=0.0, names=["phrase"])
    voices = [[[float(p), float(o - pt0), float(d)] for p, o, d in [(p, o / CH.TICKS, d / CH.TICKS) for p, o, d, _ in v if o <= end]] for v in c.voices]
    return {"all": allv, "upper": upper, "name": c.name, "changes": changes, "answer": "A", "tot_a": tot_a, "tot_b": tot_b,
            "chords_a": chords_a, "chords_b": chords_b, "na": na, "nb": nb, "unit": unit, "voices": voices, "phrase_unit": 0.6,
            "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("bach.quiz", s_, detail="the beat chords of the first phrase of Bach's chorale BWV 140.7 as he voices them, then with the upper three voices' notes reassigned at random within their registers; Part 7's piano"),
                      "phrase": save("bach.phrase", s2, detail="the first phrase of Bach's four-part chorale Wachet auf (BWV 140.7), every note, from the music21 corpus encoding; Part 7's piano")}}


TRIADS = [(r, q) for r in range(12) for q in ("M", "m")]


def _pcs(t):
    r, q = t
    return [r, (r + (4 if q == "M" else 3)) % 12, (r + 7) % 12]


def _harmonize(heads, allowed, start=None, end=None):
    """Viterbi: one triad per melody note, containing it, from ``allowed``; cost = smallest voice leading."""
    INF = 1e9
    cost = {t: (0.0 if (start is None or t == start) else INF) if heads[0] in _pcs(t) else INF for t in allowed}
    back = []
    for m in heads[1:]:
        new, ptr = {}, {}
        for t in allowed:
            if m not in _pcs(t):
                new[t] = INF
                continue
            best = min(((cost[s] + G.vl(_pcs(s), _pcs(t))[0] + (0.5 if s == t else 0.0), s) for s in allowed if cost[s] < INF), default=(INF, None))
            new[t], ptr[t] = best
        back.append(ptr)
        cost = new
    t = end if (end is not None and cost.get(end, INF) < INF) else min(cost, key=cost.get)
    total = cost[t]
    path = [t]
    for ptr in reversed(back):
        t = ptr[t]
        path.append(t)
    return path[::-1], total


def tune_line(base: int = 72, n: int = 14):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


def _name(t):
    return PCN[t[0]] + ("" if t[1] == "M" else "m")


def _voice(chain, low=52):
    out, prev = [], None
    for t in chain:
        s = _pcs(t)
        if prev is None:
            notes = sorted(low + ((pc - low) % 12) for pc in s)
        else:
            size, mv = G.vl([m % 12 for m in prev], s)
            notes = [m + d for m, d in zip(prev, mv)]
        out.append([int(round(x)) for x in notes])
        prev = out[-1]
    return out


def compute_tune() -> dict:
    mel = tune_line(n=14)
    beats = []
    for p, a, d in mel:
        for _ in range(int(d)):
            beats.append(p % 12)
    heads = [beats[i] for i in range(0, len(beats), 2)]
    diatonic = [t for t in TRIADS if set(_pcs(t)) <= {0, 2, 4, 5, 7, 9, 11}]
    chromatic = [t for t in TRIADS if not set(_pcs(t)) <= {0, 2, 4, 5, 7, 9, 11}]
    plain, cost1 = _harmonize(heads, diatonic, start=(0, "M"), end=(0, "M"))
    far, cost2 = _harmonize(heads, chromatic + [(0, "M")], start=(0, "M"), end=(0, "M"))
    unit = 0.45
    pieces = []
    out = {}
    for key, chain in (("plain", plain), ("far", far)):
        vs = _voice(chain)
        parts = [(piano(p, d * unit, 1.15), a * unit, 0.0) for p, a, d in mel]
        for i, ch in enumerate(vs):
            for m in ch:
                parts.append((piano(m, 2 * unit, 0.8), 2 * i * unit, -6.0))
            parts.append((piano(chain[i][0] + 36, 2 * unit, 0.8), 2 * i * unit, -6.0))
        pieces.append(Clip(mix(parts, duration=16 * unit + 1.2).y, SR).at_level(LEVEL))
        sizes = [G.vl(_pcs(a), _pcs(b))[0] for a, b in zip(chain, chain[1:])]
        out[key] = {"chain": [_name(t) for t in chain], "voicing": vs, "sizes": sizes, "total": float(sum(sizes)),
                    "xy": [list(G.triangle_xy(G.shape(_pcs(t)))) for t in chain]}
    s_ = concat(pieces, gap=1.0, names=["plain", "far"])
    return {"melody": rows(mel), "heads": heads, "unit": unit, "starts": {k: float(s_.events[k]) for k in ("plain", "far")}, **out,
            "seconds": s_.duration,
            "clips": {"variation": save("tune.variation32", s_, detail="the Tune's first two phrases harmonized twice by the smallest voice leadings: first with the chords of C major, then with chords outside it; Part 7's piano")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 32, "title": "harmonized by the shortest paths, then rerouted through chromatic chords", "seconds": round(t["seconds"], 1),
            "measure": f"{' '.join(t['far']['chain'])}; {t['plain']['total']:.0f} then {t['far']['total']:.0f} semitones of voice leading",
            "clip": "tune.variation32"}


ITEMS = {"hook": compute_hook, "strip": compute_strip, "duet": compute_duet, "neutral": compute_neutral, "triangle": compute_triangle, "vlsize": compute_vlsize, "even": compute_even,
         "scales": compute_scales, "mirror": compute_mirror, "optic": compute_optic, "fourier": compute_fourier, "bach": compute_bach, "tune": compute_tune,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
