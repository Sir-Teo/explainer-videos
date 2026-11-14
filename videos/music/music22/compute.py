"""Precompute everything numerical, and every sound, in Part 22 of *Music, Built* ("Analysis").

    python -m videos.music.music22.compute              # everything missing (about ten minutes: the grammars train)
    python -m videos.music.music22.compute --force learned

Numbers are cached in ``.cache/music22/<name>.json``, sounds in ``.cache/music22/audio/``.  The reductions and grammars
are Monochord's (``explainer/music/monochord/grammar.py``); the chord sequences are Part 17's chorales, cut at their
fermatas; the tunes are Part 14's corpus; everything heard is played on Part 7's piano.  Published findings are cited
in the README.

Items:
    hook        the Tune and its time-span reduction, level by level, heard
    skeleton    the Tune's first strain and two candidate skeletons (an ear question)
    urlinie     how many of Part 14's tunes end with a stepwise descent to the tonic, against shuffled tunes
    grouping    grouping preference strengths on the Tune
    parses      parse trees and counts of parses for example progressions under the functional grammar
    learned     grammars trained on the chorales' phrases against chord n-grams, on held-out chorales
    growth      three melodies grown from the Tune's skeleton by the elaboration grammar (an ear question)
    tune        Variation 22: the skeleton, then the Tune regrown along a different derivation
    variation   the Variations ledger, row 22
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import grammar as G
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music22")
CLIPS = ClipStore("music22")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
C4 = 261.6255653005986
_NOTES: dict = {}
BEAT = 0.4

HARMONY = ["C", "C", "F", "G", "F", "C", "G", "C", "C", "F", "C", "G", "C", "F", "C", "G", "C", "C", "F", "G", "F", "C", "G", "C"]
PCS = {"C": (0, 4, 7), "F": (5, 9, 0), "G": (7, 11, 2)}
BASS = {"C": 48, "F": 53, "G": 43}


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def piano(m: float, seconds: float, velocity: float = 1.4) -> Clip:
    key = (round(m, 3), round(seconds, 3), velocity)
    if key not in _NOTES:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=velocity, seconds=seconds + 0.3))
        _NOTES[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _NOTES[key]


def chord_at(t: float):
    return set(PCS[HARMONY[min(int(t // 2), len(HARMONY) - 1)]])


def play(melody, beat: float = BEAT, harmony: bool = True, tail: float = 1.2) -> Clip:
    """A melody of (midi, onset, beats) over the Tune's harmony (a bass and a chord every two beats)."""
    placed, ev = [], {}
    T = max(a + d for _, a, d in melody)
    for k, (p, a, d) in enumerate(melody):
        placed.append((piano(p, d * beat * 1.05), a * beat, 0.0))
        ev[f"n{k}"] = a * beat
    if harmony:
        for k in range(int(round(T / 2))):
            c = HARMONY[k % len(HARMONY)]
            for m in [BASS[c]] + [60 + x if 60 + x < 67 else 48 + x for x in PCS[c][1:]]:
                placed.append((piano(m, 2 * beat * 1.05, velocity=1.0), 2 * k * beat, -8.0))
    ev["end"] = T * beat
    return Clip(mix(placed, duration=T * beat + tail).y, SR, ev, [])


def tune_notes(base: int = 72):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in zip(t.pitches, t.beats):
        out.append((base + p, a, float(d)))
        a += d
    return out


def rows(ln):
    return [[int(p), float(a), float(d)] for p, a, d in ln]


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    notes = tune_notes()
    levels = G.reduce_levels(notes, chord_at, span=1.0)
    shown = [0, 1, 2, 3, 4]
    clips = [play(levels[k]).at_level(LEVEL) for k in shown]
    s = concat(clips, gap=1.0, names=[f"L{k}" for k in shown])
    return {"levels": [rows(levels[k]) for k in range(len(levels))], "shown": shown, "starts": {f"L{k}": float(s.events[f"L{k}"]) for k in shown},
            "beat": BEAT, "clips": {"levels": save("hook.levels", s, level=None, detail="the Tune, then its time-span reduction at spans of 2, 4, 8 and 16 beats, over its harmony: Part 7's piano")}}


def compute_skeleton() -> dict:
    notes = [n for n in tune_notes() if n[1] < 16]
    levels = G.reduce_levels(notes, chord_at, span=1.0)
    right = levels[2]                                    # a note every four beats
    wrong = [(G.scale_step(p, 1) if k in (1, 2) else p, a, d) for k, (p, a, d) in enumerate(right)]
    c0, cA, cB = play(notes), play(wrong), play(right)
    s = concat([c0.at_level(LEVEL), cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.0, names=["surface", "A", "B"])
    return {"surface": rows(notes), "A": rows(wrong), "B": rows(right), "starts": {k: float(s.events[k]) for k in ("surface", "A", "B")}, "beat": BEAT,
            "clips": {"three": save("skeleton.three", s, level=None, detail="the Tune's first strain, then two candidate skeletons, each over the same harmony: Part 7's piano")}}


def descends(pitches, tonic_pc=0) -> str | None:
    """Does a tune end on a stepwise descent to the tonic in its last notes (repeats merged): 5-4-3-2-1, 3-2-1, or none?"""
    merged = []
    for p in pitches:
        if not merged or merged[-1] != p:
            merged.append(p)
    rel = [(p - tonic_pc) for p in merged]
    if len(rel) >= 5 and [r % 12 for r in rel[-5:]] == [7, 5, 4, 2, 0] and all(b < a for a, b in zip(rel[-5:], rel[-4:])):
        return "5-4-3-2-1"
    if len(rel) >= 3 and [r % 12 for r in rel[-3:]] == [4, 2, 0] and all(b < a for a, b in zip(rel[-3:], rel[-2:])):
        return "3-2-1"
    return None


def compute_urlinie() -> dict:
    ts = [m for m in M.corpus() if m.mode == "major"]
    real = Counter(descends(m.pitches) for m in ts)
    rng = np.random.default_rng(22)
    shuf = Counter()
    trials = 200
    for _ in range(trials):
        for m in ts:
            p = list(m.pitches[:-1])
            rng.shuffle(p)
            shuf[descends(p + [m.pitches[-1]])] += 1
    names = {m.name: descends(m.pitches) for m in ts}
    return {"n": len(ts), "real": {str(k): v for k, v in real.items()}, "shuffled": {str(k): v / trials for k, v in shuf.items()},
            "which": {k: v for k, v in names.items() if v}, "tune": names[M.THE_TUNE]}


def compute_cadence() -> dict:
    """The Tune's second phrase, F F E E D D C, over its own bass (IV I V I) and over a tonic pedal (I I I I)."""
    mel = [(77, 0.0, 1.0), (77, 1.0, 1.0), (76, 2.0, 1.0), (76, 3.0, 1.0), (74, 4.0, 1.0), (74, 5.0, 1.0), (72, 6.0, 2.0)]

    def render(chords):
        placed = []
        for p, a, d in mel:
            placed.append((piano(p, d * BEAT * 1.05), a * BEAT, 0.0))
        for k, c in enumerate(chords):
            for m in [BASS[c]] + [60 + x if 60 + x < 67 else 48 + x for x in PCS[c][1:]]:
                placed.append((piano(m, 2 * BEAT * 1.05, velocity=1.0), 2 * k * BEAT, -8.0))
        return Clip(mix(placed, duration=8 * BEAT + 1.2).y, SR, {"end": 8 * BEAT}, [])

    pedal = ["C", "C", "C", "C"]
    own = ["F", "C", "G", "C"]
    s = concat([render(pedal).at_level(LEVEL), render(own).at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"melody": rows(mel), "A": pedal, "B": own, "starts": {k: float(s.events[k]) for k in "AB"}, "beat": BEAT,
            "clips": {"two": save("cadence.two", s, level=None, detail="F F E E D D C, over a tonic pedal, then over IV I V I: Part 7's piano")}}


ROMAN = {"I": ((0, 4, 7), 48), "IV": ((5, 9, 0), 53), "V": ((7, 11, 2), 43), "vi": ((9, 0, 4), 45), "ii": ((2, 5, 9), 50),
         "V7": ((7, 11, 2, 5), 43), "V/V": ((2, 6, 9, 0), 50), "V/V/V": ((9, 1, 4, 7), 45), "V/V/V/V": ((4, 8, 11, 2), 52)}


def chords_clip(names, beat: float = 0.75):
    """Block chords, one a beat, the upper voices the shortest way."""
    placed, prev, ev = [], (67, 64, 60), {}
    for k, n in enumerate(names):
        pcs, bass = ROMAN[n]
        cands = []
        for s in range(60, 80):
            for a in range(55, s):
                for t in range(50, a):
                    if {s % 12, a % 12, t % 12} | {bass % 12} >= set(pcs[:3]) and all(x % 12 in pcs for x in (s, a, t)) and s - t <= 12:
                        cands.append((s, a, t))
        v = min(cands, key=lambda c: sum(abs(x - y) for x, y in zip(c, prev)))
        prev = v
        for m in (bass,) + v:
            placed.append((piano(m, beat * 1.1), k * beat, 0.0 if m == v[0] else -4.0))
        ev[f"c{k}"] = k * beat
    ev["end"] = len(names) * beat
    return Clip(mix(placed, duration=len(names) * beat + 1.2).y, SR, ev, [])


def compute_progressions() -> dict:
    seqs = {"cadence": ["I", "IV", "V", "I"], "longer": ["I", "vi", "ii", "V", "I"], "plagal": ["I", "IV", "I", "V", "I"],
            "nest1": ["I", "V/V", "V", "I"], "nest3": ["I", "V/V/V/V", "V/V/V", "V/V", "V", "I"]}
    cl = {k: chords_clip(v) for k, v in seqs.items()}
    two = concat([cl["cadence"].at_level(LEVEL), cl["longer"].at_level(LEVEL)], gap=1.0, names=["cadence", "longer"])
    nest = concat([cl["nest1"].at_level(LEVEL), cl["nest3"].at_level(LEVEL)], gap=1.0, names=["nest1", "nest3"])
    pl = concat([cl["plagal"].at_level(LEVEL)], gap=0.0, names=["plagal"])
    return {"seqs": seqs, "beat": 0.75, "two_starts": {k: float(two.events[k]) for k in ("cadence", "longer")},
            "nest_starts": {k: float(nest.events[k]) for k in ("nest1", "nest3")},
            "clips": {"two": save("grammar.two", two, level=None, detail="I IV V I, then I vi ii V I: Part 7's piano"),
                      "plagal": save("parsing.plagal", pl, level=None, detail="I IV I V I: Part 7's piano"),
                      "nest": save("recursion.nest", nest, level=None, detail="I, V of V, V, I; then four dominants nested: E7, A7, D7, G, C: Part 7's piano")}}


def compute_kinds() -> dict:
    demos = {"passing": [(72, 0, 1), (74, 1, 1), (76, 2, 2)], "neighbour": [(72, 0, 1), (74, 1, 1), (72, 2, 2)],
             "arpeggiation": [(72, 0, 1), (76, 1, 1), (79, 2, 2)], "repetition": [(72, 0, 1), (72, 1, 1), (72, 2, 2)]}
    cl = [play([(p, float(a), float(d)) for p, a, d in v], harmony=False).at_level(LEVEL) for v in demos.values()]
    s = concat(cl, gap=0.6, names=list(demos))
    return {"demos": {k: [[p, float(a), float(d)] for p, a, d in v] for k, v in demos.items()}, "starts": {k: float(s.events[k]) for k in demos},
            "beat": BEAT, "clips": {"four": save("reduction.kinds", s, level=None, detail="a passing note, a neighbour, an arpeggiation, a repetition: Part 7's piano")}}


def compute_grouping() -> dict:
    notes = tune_notes()
    s = G.grouping_strength(notes)
    ends = [8, 16, 24, 32, 40]
    gaps = [notes[i + 1][1] for i in range(len(notes) - 1)]
    top = sorted(range(len(s)), key=lambda i: -s[i])[:5]
    c = concat([play(notes, harmony=False).at_level(LEVEL)], gap=0.0, names=["tune"])
    return {"notes": rows(notes), "strength": [float(x) for x in s], "gaps": [float(g) for g in gaps], "top": sorted(gaps[i] for i in top), "ends": ends,
            "beat": BEAT, "clips": {"tune": save("grouping.tune", c, level=None, detail="the Tune's melody alone: Part 7's piano")}}


EXAMPLES = {"I IV V I": ["I", "IV", "V", "I"], "I vi ii V I": ["I", "vi", "ii", "V", "I"], "I IV I V I": ["I", "IV", "I", "V", "I"],
            "I ii V I IV V I": ["I", "ii", "V", "I", "IV", "V", "I"]}


def hand_grammar() -> G.PCFG:
    """The functional grammar with hand-set probabilities: no training."""
    g = G.PCFG(["I", "vi", "iii", "IV", "ii", "V", "V7", "vii°"], prior=50.0)
    g.p_split = np.array([0.5, 0.4, 0.2])
    return g


def tree_rows(t):
    if t is None:
        return None
    if len(t) == 2:
        return [t[0], t[1]]
    return [t[0], tree_rows(t[1]), tree_rows(t[2])]


def compute_parses() -> dict:
    g = hand_grammar()
    out = {}
    for name, seq in EXAMPLES.items():
        out[name] = {"tree": tree_rows(g.viterbi(seq)), "parses": g.count_parses(seq), "chords": seq}
    lengths = {n: g.count_parses(["I"] + ["IV", "V", "I"] * ((n - 1) // 3)) for n in (4, 7, 10, 13)}
    return {"examples": out, "growth": {str(k): v for k, v in lengths.items()}, "rules": [list(r) for r in G.RULES]}


def phrases(book, mode="major"):
    out = []
    for c in book:
        if c.mode != mode:
            continue
        cur, prev = [], None
        for x in F.beat_labels(c):
            s = x["label"][:2] if x["label"] else None
            if s is not None:
                r = F.roman((s[0], s[1], 0), mode)
                if r != prev:
                    cur.append(r)
                    prev = r
            if x["fermata"] and cur:
                out.append(cur)
                cur, prev = [], None
        if cur:
            out.append(cur)
    return out


def compute_learned() -> dict:
    book = BC.load()
    train, test = BC.split(book, offset=2)
    P, Q = phrases(train), phrases(test)
    cnt = Counter(x for p in P for x in p)
    vocab = [v for v, c in cnt.most_common() if c >= 5]
    fix = lambda S: [[x if x in vocab else "?" for x in p] for p in S if 2 <= len(p) <= 14]  # noqa: E731
    P2, Q2 = fix(P), fix(Q)
    vocab = vocab + ["?"]
    res = {"uniform": float(np.log2(len(vocab) + 1)), "unigram": G.ngram_bits(P2, Q2, vocab, 1), "bigram": G.ngram_bits(P2, Q2, vocab, 2),
           "trigram": G.ngram_bits(P2, Q2, vocab, 3)}
    g3 = G.PCFG(vocab, seed=0)
    g3.train(P2, iters=40)
    res["functional"] = G.pcfg_bits(g3, Q2)
    lat = {}
    for K in (4, 12):
        g = G.LatentPCFG(vocab, K=K, seed=2)
        hist = g.train(P2, iters=150 if K == 12 else 80)
        lat[str(K)] = {"test": g.bits(Q2), "train": g.bits(P2), "history": [float(x) for x in hist[::10]]}
    res["latent"] = lat
    emit = {g3.nt[k]: sorted([(float(g3.emit[k, i]), v) for i, v in enumerate(vocab)], reverse=True)[:6] for k in range(3)}
    # tree depth of every held-out phrase under the hand-set functional grammar (where it parses)
    hg = hand_grammar()
    depths = []
    for p in Q:
        if 2 <= len(p) <= 14 and all(x in hg.index for x in p):
            t = hg.viterbi(p)
            if t is not None:
                depths.append((len(p), G.tree_depth(t)))
    return {"bits": res, "emit": {k: [[round(a, 3), b] for a, b in v] for k, v in emit.items()}, "train_phrases": len(P2), "test_phrases": len(Q2),
            "vocab": len(vocab), "mean_length": float(np.mean([len(p) for p in P2])), "depths": depths,
            "parsed_share": len(depths) / max(1, sum(1 for p in Q if 2 <= len(p) <= 14))}


def skeleton_notes():
    """The Tune's skeleton: its reduction at a note every four beats."""
    lv = G.reduce_levels(tune_notes(), chord_at, span=1.0)
    return lv[2]


def compute_growth() -> dict:
    sk = skeleton_notes()
    outs = {}
    for seed in (3, 8, 13):
        rng = np.random.default_rng(seed)
        surf, used = G.elaborate(sk, chord_at, rng, depth=2, min_dur=1.0)
        outs[str(seed)] = {"notes": rows(surf), "rules": used}
    keys = list(outs)
    orig = [n for n in tune_notes() if n[1] < 16]
    first = [tuple(x) for x in outs[keys[0]]["notes"] if x[1] < 16]
    cA, cB = play(first), play(orig)
    s = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    three = concat([play([tuple(x) for x in outs[k]["notes"]]).at_level(LEVEL) for k in keys], gap=1.0, names=[f"g{k}" for k in keys])
    return {"skeleton": rows(sk), "grown": outs, "order": keys, "quiz": {"A": rows(first), "B": rows(orig)},
            "starts": {k: float(s.events[k]) for k in "AB"}, "beat": BEAT, "three_starts": {k: float(three.events[f"g{k}"]) for k in keys},
            "rule_counts": {k: dict(Counter(v["rules"])) for k, v in outs.items()},
            "clips": {"quiz": save("growth.quiz", s, level=None, detail="two melodies over the Tune's first-strain harmony: one grown by the grammar from the Tune's skeleton, one the Tune: Part 7's piano"),
                      "three": save("growth.three", three, level=None, detail="three melodies grown by the grammar from the Tune's skeleton, over its harmony: Part 7's piano")}}


def compute_tune() -> dict:
    sk = skeleton_notes()
    g = load("growth")
    surf = [tuple(x) for x in g["grown"][g["order"][1]]["notes"]]
    cs, cg = play(sk), play(surf)
    s = concat([cs.at_level(LEVEL), cg.at_level(LEVEL)], gap=1.2, names=["skeleton", "regrown"])
    ok = sum(1 for p, a, d in surf if abs(a % 1) < 1e-9 and p % 12 in chord_at(a) and abs(a % 2) < 1e-9)
    strong = sum(1 for p, a, d in surf if abs(a % 2) < 1e-9)
    return {"skeleton": rows(sk), "regrown": rows(surf), "starts": {k: float(s.events[k]) for k in ("skeleton", "regrown")}, "beat": BEAT,
            "chord_tones_on_strong_beats": ok, "strong_beats": strong, "seconds": s.duration,
            "same_as_tune": sum(1 for (p, a, d), (q, b, e) in zip(surf, tune_notes()) if p == q and abs(a - b) < 1e-9),
            "clips": {"variation": save("tune.variation22", s, level=None, detail="the Tune's skeleton, then the Tune regrown from it along a different derivation: Part 7's piano")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 22, "title": r"reduced to its skeleton, a note every four beats, and regrown along a different derivation", "seconds": round(t["seconds"], 2),
            "measure": rf"{len(t['skeleton'])} skeleton notes grown into {len(t['regrown'])}; on {t['chord_tones_on_strong_beats']} of {t['strong_beats']} strong beats a note of the chord",
            "clip": "tune.variation22"}


ITEMS = {"hook": compute_hook, "kinds": compute_kinds, "skeleton": compute_skeleton, "urlinie": compute_urlinie, "cadence": compute_cadence,
         "progressions": compute_progressions, "grouping": compute_grouping, "parses": compute_parses,
         "learned": compute_learned, "growth": compute_growth, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
