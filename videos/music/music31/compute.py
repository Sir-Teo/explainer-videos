"""Precompute everything numerical, and every sound, in Part 31 of *Music, Built* ("Transformations").

    python -m videos.music.music31.compute              # everything missing (a minute)
    python -m videos.music.music31.compute --force groups

Numbers are cached in ``.cache/music31/<name>.json``, sounds in ``.cache/music31/audio/``.  The measures are Monochord's
(``explainer/music/monochord/neoriemann.py``).  Every progression is ours, played on Part 7's piano and bowed string.

Items:
    hook        a progression of our own in film style: C, E, C, A flat, and home
    plr         P, L and R from C major (an ear question: which is P?); voice-leading in semitones
    groups      the PLR group and the T/I group built by brute force: orders, commutation, simple transitivity; distances
    cycles      the hexatonic cycle (P, L, P, L ...) and the octatonic cycle (P, R ...), heard
    chain       the chain R, L, R, L ... through all 24 triads; the first nineteen, heard (the chain Cohn finds in Beethoven's Ninth)
    keys        a diatonic chain and an R-L chain of six chords (an ear question: which stays in one key?)
    poles       C to E minor (two common tones) and C to A flat minor (none) (an ear question)
    compound    two-step moves from C: LP (to E), PL (to A flat), RP (to A)
    commute     T3 then P, and P then T3, from C: the same chord either way
    walk        a random walk of eight PLR steps on the Tonnetz, heard
    film3       three moves from C in film style: to E major, to A flat major, to F sharp major
    thirds      three keys a major third apart, each reached through its dominant: B, D7, G, B flat 7, E flat, F sharp 7, B
    vl          voice-leading distance from C major to every triad, against PLR distance
    spheres     how many triads lie at each PLR distance from C major (1, 3, 6, 8, 5, 1)
    systems     Cohn's four hexatonic systems and the three octatonic systems, as orbits of PL and PR
    relations   the orders of the moves and their products; P = R(LR)^3, so L and R alone generate the group
    hamilton    every Hamiltonian cycle of the PLR graph, counted by search; one that is not the R-L chain, heard
    minor       P, L and R from A minor: to A major, F major and C major, heard
    sevenths    the dominant and half-diminished sevenths two semitones from C7 (Childs); C7 to F sharp 7, A7, E flat 7, and F half-diminished to E7, heard
    comma       Euler's lattice does not close in just intonation: E as a pure third above C, and E by four pure fifths, heard
    weitzmann   Weitzmann's region: the augmented triad C, E, G sharp resolving to its six neighbours, heard
    tune        Variation 31: the Tune harmonized by a walk on the Tonnetz
    variation   the Variations ledger, row 31
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord import neoriemann as N
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver, signoff
from explainer.music.monochord.physics.string import String

CACHE = Cache("music31")
CLIPS = ClipStore("music31")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
VIOLIN = STR.violin_body()
C4 = 261.6255653005986
_P: dict = {}
_V: dict = {}


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


def bowed(m: float, seconds: float) -> Clip:
    key = (round(m, 3), round(min(seconds, 3.5), 2))
    if key not in _V:
        y = VIOLIN.play(STR.bowed_note(hz(m), max(min(seconds, 3.5), 0.1)))
        _V[key] = Clip(np.asarray(y, dtype=float)).fade(0.02, 0.1).at_level(LEVEL)
    return _V[key]


def voicing(chain, low: int = 55) -> list[list[int]]:
    """Voice a chain of triads smoothly: the first in close position from ``low``, each next note the nearest member."""
    out = []
    prev = None
    for t in chain:
        s = sorted(N.pcs(t))
        if prev is None:
            notes = []
            for pc in s:
                m = low + ((pc - low) % 12)
                notes.append(m)
            notes = sorted(notes)
        else:
            notes, used = [], set()
            for m in prev:
                best = None
                for pc in s:
                    if pc in used:
                        continue
                    cand = m + ((pc - m + 6) % 12) - 6
                    if best is None or abs(cand - m) < abs(best[0] - m):
                        best = (cand, pc)
                notes.append(best[0])
                used.add(best[1])
        out.append(notes)
        prev = notes
    return out


def chord_clip(chain, unit: float = 1.0, bass: bool = True, inst=None, gap: float = 0.0) -> tuple[Clip, list]:
    inst = inst or (lambda m, s: piano(m, s, 0.9))
    vs = voicing(chain)
    parts, notes = [], []
    for i, ch in enumerate(vs):
        t0 = i * (unit + gap)
        for m in ch:
            parts.append((inst(m, unit * 1.05), t0, -2.0))
            notes.append([float(m), i * 1.0, 1.0])
        if bass:
            b = chain[i][0] + 36
            parts.append((inst(b, unit * 1.05), t0, -4.0))
            notes.append([float(b), i * 1.0, 1.0])
    c = Clip(mix(parts, duration=len(chain) * (unit + gap) + 1.2).y, SR)
    return c, notes


def rows(v):
    return [[float(p), float(a), float(d)] for p, a, d in v]


def tune_line(base: int = 72, n: int = 14):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


C = (0, "M")


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    chain = [C, (4, "M"), C, (8, "M"), (5, "M"), C]
    c, notes = chord_clip(chain, unit=1.5, inst=bowed)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["film"])
    return {"chain": [N.name(t) for t in chain], "notes": notes, "unit": 1.5,
            "moves": [N.name_move(a, b) for a, b in zip(chain, chain[1:])],
            "common": [N.common_tones(a, b) for a, b in zip(chain, chain[1:])],
            "clips": {"film": save("hook.film", s_, detail="a progression of our own in the manner of a film score: C major, E major, C, A flat major, F, C; Part 7's bowed string")}}


def compute_plr() -> dict:
    order = ["L", "R", "P"]                                        # A, B, C: P is C
    clips = []
    pairs = {}
    for k in order:
        chain = [C, N.OPS[k](C)]
        c, notes = chord_clip(chain, unit=1.2)
        clips.append(c.at_level(LEVEL))
        pairs[k] = {"to": N.name(chain[1]), "notes": notes, "voicing": voicing(chain), "semitones": N.voice_leading(*chain)}
    s_ = concat(clips, gap=1.0, names=order)
    return {"order": order, "pairs": pairs, "answer": "C", "starts": {k: float(s_.events[k]) for k in order},
            "clips": {"quiz": save("plr.quiz", s_, detail="C major to E minor, to A minor and to C minor, in some order: L, R and P; Part 7's piano")}}


def compute_groups() -> dict:
    G, H = N.plr_group(), N.ti_group()
    d = N.shortest_paths(C)
    hist = Counter(len(w) for w in d.values())
    far = [N.name(t) for t, w in d.items() if len(w) == max(hist)]
    return {"plr": len(G), "ti": len(H), "commute": N.commute(G, H), "simple_plr": N.is_simply_transitive(G), "simple_ti": N.is_simply_transitive(H),
            "dist": {str(k): v for k, v in sorted(hist.items())}, "words": {N.name(t): w for t, w in d.items()}, "farthest": far,
            "examples": {"E": d[(4, "M")], "Abm": d[(8, "m")], "Ab": d[(8, "M")], "A": d[(9, "M")], "F#": d[(6, "M")]}}


def compute_cycles() -> dict:
    hexa = N.cycle("PL") + [C]
    octa = N.cycle("PR") + [C]
    c1, n1 = chord_clip(hexa, unit=0.9)
    c2, n2 = chord_clip(octa, unit=0.9)
    s_ = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=1.2, names=["hexatonic", "octatonic"])
    return {"hexatonic": [N.name(t) for t in hexa], "octatonic": [N.name(t) for t in octa], "n1": n1, "n2": n2,
            "hexa_set": sorted(set().union(*[N.pcs(t) for t in hexa])), "octa_set": sorted(set().union(*[N.pcs(t) for t in octa])),
            "starts": {k: float(s_.events[k]) for k in ("hexatonic", "octatonic")}, "unit": 0.9,
            "clips": {"two": save("cycles.two", s_, detail="the hexatonic cycle from C (P, L, P, L, P, L) and the octatonic cycle (P, R, P, R ...), each back to C; Part 7's piano")}}


def compute_chain() -> dict:
    full = N.cycle("RL")
    first = full[:19]
    c, notes = chord_clip(first, unit=0.55, bass=True)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["chain"])
    return {"full": [N.name(t) for t in full], "first": [N.name(t) for t in first], "notes": notes, "unit": 0.55,
            "clips": {"chain": save("chain.nineteen", s_, detail="the chain R, L, R, L ... from C major through nineteen triads to A major, the chain Cohn finds in Beethoven's Ninth (our voicing); Part 7's piano")}}


def compute_keys() -> dict:
    dia = [C, (9, "m"), (5, "M"), (2, "m"), (7, "M"), C]
    lr = N.cycle("RL")[:6]
    ca, na = chord_clip(dia, unit=0.9)
    cb, nb = chord_clip(lr, unit=0.9)
    s_ = concat([ca.at_level(LEVEL), cb.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    def in_c(t):
        return N.pcs(t) <= {0, 2, 4, 5, 7, 9, 11}
    return {"A": [N.name(t) for t in dia], "B": [N.name(t) for t in lr], "na": na, "nb": nb, "answer": "A",
            "A_in_C": all(in_c(t) for t in dia), "B_in_C": [in_c(t) for t in lr], "starts": {k: float(s_.events[k]) for k in "AB"}, "unit": 0.9,
            "clips": {"quiz": save("keys.quiz", s_, detail="two six-chord chains from C: C, A minor, F, D minor, G, C (all in C major), and C, A minor, F, D minor, B flat, G minor (R, L, R, L, R); Part 7's piano")}}


def compute_poles() -> dict:
    a = [C, (4, "m")]
    b = [C, (8, "m")]
    ca, na = chord_clip(a, unit=1.4, inst=bowed)
    cb, nb = chord_clip(b, unit=1.4, inst=bowed)
    s_ = concat([ca.at_level(LEVEL), cb.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"A": [N.name(t) for t in a], "B": [N.name(t) for t in b], "common": [N.common_tones(*a), N.common_tones(*b)],
            "vl": [N.voice_leading(*a), N.voice_leading(*b)], "words": [N.name_move(*a), N.name_move(*b)], "answer": "B",
            "starts": {k: float(s_.events[k]) for k in "AB"}, "na": na, "nb": nb,
            "clips": {"quiz": save("poles.quiz", s_, detail="C major to E minor, then C major to A flat minor; Part 7's bowed string")}}


def compute_tune() -> dict:
    mel = tune_line(n=14)
    beats = []
    for p, a, d in mel:
        for k in range(int(d)):
            beats.append(p % 12)
    # one chord every two beats, chosen to contain the melody note on its first beat
    heads = [beats[i] for i in range(0, len(beats), 2)]
    walk = N.harmonize(heads, C, end=C)
    unit = 0.45
    vs = voicing(walk, low=48)
    parts = []
    for p, a, d in mel:
        parts.append((piano(p, d * unit, 1.15), a * unit, 0.0))
    for i, ch in enumerate(vs):
        for m in ch:
            parts.append((piano(m, 2 * unit, 0.8), 2 * i * unit, -6.0))
        parts.append((piano(walk[i][0] + 36, 2 * unit, 0.8), 2 * i * unit, -6.0))
    c = Clip(mix(parts, duration=16 * unit + 1.5).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["walk"])
    moves = [("=" if a == b else N.name_move(a, b)) for a, b in zip(walk, walk[1:])]
    return {"melody": rows(mel), "walk": [N.name(t) for t in walk], "walk_t": [list(t) for t in walk], "moves": moves, "unit": unit, "heads": heads,
            "voicing": vs, "seconds": s_.duration, "notes": {"chords": len(walk), "moves": sum(1 for m in moves if m != "="), "single": sum(1 for m in moves if len(m) == 1 and m != "=")},
            "clips": {"variation": save("tune.variation31", s_, detail="the Tune's first two phrases harmonized by a walk on the Tonnetz: each chord the same as the last or one or two P, L, R steps away; Part 7's piano")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 31, "title": r"harmonized by a walk on the Tonnetz", "seconds": round(t["seconds"], 2),
            "measure": rf"{t['notes']['chords']} chords: {' '.join(t['walk'])}; moves {' '.join(t['moves'])}",
            "clip": "tune.variation31"}


def compute_compound() -> dict:
    words = ["LP", "PL", "RP"]
    clips, out = [], {}
    for w in words:
        chain = [C, N.apply(w, C)]
        c, notes = chord_clip(chain, unit=1.2)
        clips.append(c.at_level(LEVEL))
        out[w] = {"to": N.name(chain[1]), "common": N.common_tones(*chain), "vl": N.voice_leading(*chain), "notes": notes}
    s_ = concat(clips, gap=0.9, names=words)
    return {"words": words, "pairs": out, "starts": {k: float(s_.events[k]) for k in words},
            "clips": {"three": save("compound.three", s_, detail="C major to E major (L then P), to A flat major (P then L), to A major (R then P); Part 7's piano")}}


def compute_commute() -> dict:
    a = [C, N.T(3)(C), N.P(N.T(3)(C))]
    b = [C, N.P(C), N.T(3)(N.P(C))]
    ca, na = chord_clip(a, unit=1.0)
    cb, nb = chord_clip(b, unit=1.0)
    s_ = concat([ca.at_level(LEVEL), cb.at_level(LEVEL)], gap=1.0, names=["TP", "PT"])
    return {"TP": [N.name(t) for t in a], "PT": [N.name(t) for t in b], "same": a[-1] == b[-1], "na": na, "nb": nb,
            "starts": {k: float(s_.events[k]) for k in ("TP", "PT")}, "unit": 1.0,
            "clips": {"two": save("commute.two", s_, detail="C major, transposed up three semitones, then P; then C major, P, then transposed: both end on E flat minor; Part 7's piano")}}


def compute_walk() -> dict:
    rng = np.random.default_rng(31)
    t = C
    chain, word = [C], ""
    for _ in range(8):
        k = str(rng.choice(["P", "L", "R"]))
        if word and k == word[-1]:
            k = {"P": "L", "L": "R", "R": "P"}[k]
        t = N.OPS[k](t)
        chain.append(t)
        word += k
    c, notes = chord_clip(chain, unit=0.8)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["walk"])
    return {"chain": [N.name(x) for x in chain], "word": word, "notes": notes, "unit": 0.8, "end_dist": len(N.shortest_paths(C)[t]),
            "clips": {"walk": save("walk.random", s_, detail="a random walk of eight P, L and R steps from C major, never the same move twice running; Part 7's piano")}}


def compute_film3() -> dict:
    targets = [(4, "M"), (8, "M"), (6, "M")]
    clips, out = [], []
    for t in targets:
        chain = [C, t, C]
        c, _ = chord_clip(chain, unit=1.3, inst=bowed)
        clips.append(c.at_level(LEVEL))
        out.append({"to": N.name(t), "word": N.name_move(C, t), "common": N.common_tones(C, t), "vl": N.voice_leading(C, t)})
    s_ = concat(clips, gap=1.0, names=["E", "Ab", "F#"])
    return {"moves": out, "starts": {k: float(s_.events[k]) for k in ("E", "Ab", "F#")}, "unit": 1.3,
            "clips": {"three": save("film3.three", s_, detail="C major to E major and back, to A flat major and back, to F sharp major and back; Part 7's bowed string")}}


def dom7(root: int) -> list:
    return [root % 12, (root + 4) % 12, (root + 7) % 12, (root + 10) % 12]


def compute_thirds() -> dict:
    seq = [("B", [11, 3, 6]), ("D7", dom7(2)), ("G", [7, 11, 2]), ("Bb7", dom7(10)), ("Eb", [3, 7, 10]), ("F#7", dom7(6)), ("B", [11, 3, 6])]
    unit = 0.9
    parts, notes = [], []
    prev = None
    for i, (nm, pcs_) in enumerate(seq):
        chord = []
        for j, pc in enumerate(pcs_):
            m = 55 + ((pc - 55) % 12)
            chord.append(m)
        chord = sorted(chord)
        for m in chord:
            parts.append((piano(m, unit * 1.05, 0.9), i * unit, -2.0))
            notes.append([float(m), float(i), 1.0])
        bass = 36 + ({"B": 11, "D7": 2, "G": 7, "Bb7": 10, "Eb": 3, "F#7": 6}[nm])
        parts.append((piano(bass, unit * 1.05, 0.9), i * unit, -4.0))
        notes.append([float(bass), float(i), 1.0])
    c = Clip(mix(parts, duration=len(seq) * unit + 1.2).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["thirds"])
    return {"seq": [nm for nm, _ in seq], "notes": notes, "unit": unit, "keys_apart": [(7 - 11) % 12, (3 - 7) % 12, (11 - 3) % 12],
            "clips": {"thirds": save("thirds.cycle", s_, detail="three major keys a major third apart, each reached through its own dominant seventh: B, D7, G, B flat 7, E flat, F sharp 7, B (our voicing); Part 7's piano")}}


def compute_vl() -> dict:
    d = N.shortest_paths(C)
    rows_ = [{"triad": N.name(t), "plr": len(d[t]), "vl": N.voice_leading(C, t), "common": N.common_tones(C, t)} for t in N.TRIADS if t != C]
    x = np.array([r["plr"] for r in rows_])
    y = np.array([r["vl"] for r in rows_])
    r = float(np.corrcoef(x, y)[0, 1])
    return {"rows": rows_, "r": r, "max_vl": int(y.max()), "far_vl": [r_["triad"] for r_ in rows_ if r_["vl"] == y.max()]}


def compute_minor() -> dict:
    A = (9, "m")
    out, clips = [], []
    for k in "PLR":
        t = N.OPS[k](A)
        c, _ = chord_clip([A, t], unit=1.0)
        clips.append(c.at_level(LEVEL))
        out.append({"move": k, "to": N.name(t), "vl": N.voice_leading(A, t), "common": N.common_tones(A, t)})
    s_ = concat(clips, gap=0.9, names=list("PLR"))
    return {"moves": out, "starts": {k: float(s_.events[k]) for k in "PLR"}, "unit": 1.0,
            "clips": {"three": save("minor.three", s_, detail="A minor followed by P (A major), L (F major) and R (C major); Part 7's piano")}}


SEVNAME = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def compute_sevenths() -> dict:
    nb = N.seventh_neighbours(("7", 0))
    rows_ = [{"chord": SEVNAME[r] + ("7" if k == "7" else "o7"), "vl": d, "common": c} for (k, r), d, c in nb]
    pairs = [(("7", 0), ("7", 6)), (("7", 0), ("7", 9)), (("7", 0), ("7", 3)), (("o", 5), ("7", 4))]
    clips, out = [], []
    for a, b in pairs:
        A = sorted(N.seventh(*a))
        va = sorted(55 + ((pc - 55) % 12) for pc in A)
        vb, used = [], set()
        B = N.seventh(*b)
        for m in va:
            best = None
            for pc in B:
                if pc in used:
                    continue
                cand = m + ((pc - m + 6) % 12) - 6
                if best is None or abs(cand - m) < abs(best[0] - m):
                    best = (cand, pc)
            vb.append(best[0])
            used.add(best[1])
        parts = []
        for i, (ch, root) in enumerate(((va, a[1]), (vb, b[1]), (va, a[1]))):
            for m in ch:
                parts.append((piano(m, 1.15, 0.85), i * 1.1, -2.0))
            parts.append((piano(36 + root, 1.15, 0.85), i * 1.1, -4.0))
        clips.append(Clip(mix(parts, duration=3 * 1.1 + 1.0).y, SR).at_level(LEVEL))
        out.append({"a": SEVNAME[a[1]] + ("7" if a[0] == "7" else "o7"), "b": SEVNAME[b[1]] + ("7" if b[0] == "7" else "o7"),
                    "vl": N.voice_leading4(N.seventh(*a), B), "common": len(N.seventh(*a) & B)})
    names = ["F#7", "A7", "Eb7", "tristan"]
    s_ = concat(clips, gap=0.8, names=names)
    two_semis = sum(1 for r in rows_ if r["common"] == 2)
    return {"rows": rows_, "pairs": out, "starts": {k: float(s_.events[k]) for k in names}, "n": len(rows_), "two_semitone": two_semis,
            "clips": {"four": save("sevenths.four", s_, detail="C7 to F sharp 7, to A7 and to E flat 7, each and back, then F half-diminished seventh to E7 and back (our voicing); Part 7's piano")}}


def compute_comma() -> dict:
    just_third = 12 * np.log2(5 / 4)
    fifths = 4 * 12 * np.log2(3 / 2) - 24
    comma = 100 * (fifths - just_third)
    parts = []
    # C with the just E; C with the Pythagorean E; then the two Es alone, one after the other
    for i, e in enumerate((just_third, fifths)):
        parts.append((piano(60, 2.2, 0.85), i * 2.6, -3.0))
        parts.append((piano(60 + e, 2.2, 0.85), i * 2.6, -3.0))
    parts.append((piano(64 + just_third - 4, 1.2, 0.9), 5.6, -2.0))
    parts.append((piano(64 + fifths - 4, 1.2, 0.9), 7.0, -2.0))
    parts.append((piano(64 + just_third - 4, 1.2, 0.9), 8.4, -2.0))
    parts.append((piano(64 + fifths - 4, 1.2, 0.9), 9.8, -2.0))
    c = Clip(mix(parts, duration=11.6).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["comma"])
    return {"just_cents": float(100 * just_third), "fifths_cents": float(100 * fifths), "comma_cents": float(comma),
            "starts": [0.0, 2.6, 5.6], "beats_just": 0.0,
            "clips": {"comma": save("comma.two", s_, detail="C with a pure major third (5:4), then C with the E reached by four pure fifths, then the two Es alone, alternating; Part 7's piano")}}


def compute_spheres() -> dict:
    h = N.distance_histogram(C)
    d = N.shortest_paths(C)
    by = {str(k): [N.name(t) for t, w in d.items() if len(w) == k] for k in h}
    return {"hist": {str(k): v for k, v in h.items()}, "by": by, "mean": float(sum(k * v for k, v in h.items()) / 24.0)}


def compute_systems() -> dict:
    return {"hexatonic": [[N.name(t) for t in s] for s in N.systems("PL")],
            "octatonic": [[N.name(t) for t in s] for s in N.systems("PR")],
            "names": ["Northern", "Eastern", "Southern", "Western"]}


def compute_relations() -> dict:
    words = ["P", "L", "R", "PL", "PR", "LR"]
    orders = {w: N.order(w) for w in words}
    p_redundant = all(N.apply("R" + "LR" * 3, t) == N.P(t) for t in N.TRIADS)
    sub = N.closure([N.as_perm(N.L), N.as_perm(N.R)])
    return {"orders": orders, "p_is_rlrlrlr": bool(p_redundant), "lr_group": len(sub)}


def hamilton_list(limit: int = 200) -> list:
    start, n = C, 24
    found, path, seen = [], [C], {C}

    def go(t):
        if len(found) >= limit:
            return
        if len(path) == n:
            for k in "PLR":
                if N.OPS[k](t) == start:
                    found.append(list(path))
            return
        for k in "PLR":
            u = N.OPS[k](t)
            if u not in seen:
                seen.add(u)
                path.append(u)
                go(u)
                path.pop()
                seen.discard(u)

    go(C)
    return found


def compute_hamilton() -> dict:
    count = N.hamiltonian_cycles()
    cycles = hamilton_list()
    words = []
    for cyc in cycles:
        w = "".join(next(k for k in "PLR" if N.OPS[k](cyc[i]) == cyc[(i + 1) % 24]) for i in range(24))
        words.append(w)
    # one with all three moves, and as many P moves as possible
    pick = max(range(len(words)), key=lambda i: (len(set(words[i])) == 3, words[i].count("P"), words[i]))
    chain = cycles[pick] + [C]
    c, notes = chord_clip(chain, unit=0.5)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["tour"])
    return {"count": count, "word": words[pick], "chain": [N.name(t) for t in chain], "notes": notes, "unit": 0.5,
            "moves": {k: words[pick].count(k) for k in "PLR"},
            "clips": {"tour": save("hamilton.tour", s_, detail="a tour of all 24 major and minor triads by P, L and R moves, each triad once, back to C major; Part 7's piano")}}


def compute_weitzmann() -> dict:
    region = N.weitzmann(0)
    aug = [60, 64, 68]
    unit = 0.9
    parts, notes, starts = [], [], []
    for i, t in enumerate(region):
        s = N.pcs(t)
        target = []
        for m in aug:
            if m % 12 in s:
                target.append(m)
            else:
                for dm in (-1, 1):
                    if (m + dm) % 12 in s and (m + dm) % 12 not in {x % 12 for x in target}:
                        target.append(m + dm)
                        break
        t0 = i * 2 * unit + i * 0.5
        starts.append(t0)
        for m in aug:
            parts.append((piano(m, unit * 1.05, 0.85), t0, -2.0))
            notes.append([float(m), 2.0 * i + 0.25 * i, 1.0])
        for m in sorted(target):
            parts.append((piano(m, unit * 1.1, 0.9), t0 + unit, -2.0))
            notes.append([float(m), 2.0 * i + 0.25 * i + 1.0, 1.0])
        parts.append((piano(t[0] + 36, unit * 1.1, 0.9), t0 + unit, -4.0))
    c = Clip(mix(parts, duration=starts[-1] + 2 * unit + 1.2).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["region"])
    return {"region": [N.name(t) for t in region], "starts": starts, "unit": unit, "notes": notes,
            "clips": {"region": save("weitzmann.region", s_, detail="the augmented triad C, E, G sharp, each time resolving by one semitone in one voice to one of its six neighbouring triads; Part 7's piano")}}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation31", 31)


ITEMS = {"hook": compute_hook, "plr": compute_plr, "groups": compute_groups, "cycles": compute_cycles, "chain": compute_chain,
         "keys": compute_keys, "poles": compute_poles, "compound": compute_compound, "commute": compute_commute,
         "walk": compute_walk, "film3": compute_film3, "thirds": compute_thirds, "vl": compute_vl, "minor": compute_minor, "sevenths": compute_sevenths, "comma": compute_comma, "spheres": compute_spheres, "systems": compute_systems,
         "relations": compute_relations, "hamilton": compute_hamilton, "weitzmann": compute_weitzmann, "tune": compute_tune, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
