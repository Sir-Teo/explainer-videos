"""Precompute everything numerical, and every sound, in Part 14 of *Music, Built* ("Melody").

    python -m videos.music.music14.compute              # everything missing (about a minute)
    python -m videos.music.music14.compute --force leaps

Numbers are cached in ``.cache/music14/<name>.json`` (+ ``.npz``), sounds in ``.cache/music14/audio/``.  The melody
module is Monochord's (``explainer/music/monochord/melody.py``), the corpus ``explainer/music/monochord/tunes.py``;
published findings are cited in the README.

Items:
    hook        the Tune's one leap; the Tune with its notes shuffled; how often a leap is followed by a turn back
    contour     one tune in two disguises (its octaves scrambled; its leaps stretched), and undisguised
    steps       every move in the corpus: repeats, steps and leaps; two made-up melodies; one stream or two
    range       how much room each tune uses; the widest and the narrowest
    arch        the shape of every phrase, and the average shape
    leaps       what follows a leap, by where it lands: real tunes, shuffled tunes, notes from an urn
    tendency    where each degree of the scale goes; gap-fill against two kinds of chance; three endings
    motive      repeats and sequences; a tune compared with itself
    phrase      phrase lengths, long last notes, and the notes phrases end on
    info        bits per note with no memory, and with one to five notes of memory; Zipf's law
    model       the Tune's surprise, note by note; what the model expects next; melodies it makes up
    tone        four tones of speech on Part 8's voice
    frontier    three predictors of the next note, scored on tunes they have not seen
    more        one tune in two keys; contour codes; three rolls of a die; where a tune peaks; step inertia; the
                plan of a tune in letters; the guessing game; the most and least predictable tunes
    tune        Variation 14: the Tune decorated, upside down, backwards, and continued as expected and not
    variation   the Variations ledger, row 14
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.instruments import winds as WINDS
from explainer.music.monochord.partkit import organ_tone, saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music14")
CLIPS = ClipStore("music14")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C4 = 261.6255653005986
BOARD = STR.soundboard()
_NOTES: dict = {}
CORPUS = M.corpus()
BY_NAME = {m.name: m for m in CORPUS}
TUNE = BY_NAME[M.THE_TUNE]
OTHERS = [m for m in CORPUS if m.name != M.THE_TUNE]
DEGREE_NAMES = ["1", "2", "3", "4", "5", "6", "7"]


def clip(y, fade=(0.001, 0.05)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def piano(hz: float, seconds: float) -> Clip:
    key = (round(hz, 3), round(seconds, 3))
    if key not in _NOTES:
        y = BOARD.play(STR.struck(String.tuned(hz, L=0.62 * (C4 / hz) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=1.6, seconds=seconds + 0.25))
        _NOTES[key] = clip(y, (0.001, 0.18)).at_level(LEVEL)
    return _NOTES[key]


def hz_of(semis: float, base: float = C4) -> float:
    return base * 2.0 ** (semis / 12.0)


def play(pitches, beats=None, beat: float = 0.42, base: float = C4, last: float = 1.6, phrase_ends=(), t0: float = 0.0) -> Clip:
    """A melody on the piano: semitones above ``base``, each for its number of beats.  Events ``n0, n1, ...``,
    ``p0, p1, ...`` at the start of each phrase, and ``end``."""
    pitches = list(pitches)
    beats = [1.0] * len(pitches) if beats is None else list(beats)
    placed, events, t = [], {}, t0
    starts = [0] + [e for e in phrase_ends if e < len(pitches)]
    for k, (p, b) in enumerate(zip(pitches, beats)):
        d = b * beat * (last if k == len(pitches) - 1 else 1.0)
        placed.append((piano(hz_of(p, base), max(d, 0.14)), t, 0.0))
        events[f"n{k}"] = t
        if k in starts:
            events[f"p{starts.index(k)}"] = t
        t += d
    events["end"] = t
    c = mix(placed, duration=t + 0.5)
    return Clip(c.y, SR, events, [])


def melody_clip(m: M.Melody, beat: float = 0.42, phrases=None, base: float = C4, **kw) -> Clip:
    if phrases is None:
        return play(m.pitches, m.beats, beat, base, phrase_ends=m.phrase_ends, **kw)
    ends = [0] + m.phrase_ends
    a, b = ends[phrases[0]], ends[phrases[1]]
    return play(m.pitches[a:b], m.beats[a:b], beat, base, phrase_ends=[e - a for e in m.phrase_ends if a < e < b], **kw)


def note_times(c: Clip, n: int, prefix: str = "") -> list[float]:
    return [float(c.events[f"{prefix}n{k}"]) for k in range(n)]


def rows(m: M.Melody, phrases=None) -> dict:
    """What a picture needs of a melody: its pitches, beats and phrase ends (for some of its phrases)."""
    ends = [0] + m.phrase_ends
    a, b = (0, len(m)) if phrases is None else (ends[phrases[0]], ends[phrases[1]])
    return {"name": m.name, "pitches": m.pitches[a:b], "beats": m.beats[a:b], "phrase_ends": [e - a for e in m.phrase_ends if a < e <= b], "mode": m.mode}


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    first = melody_clip(TUNE, phrases=(0, 2), beat=0.5)
    two = M.Melody("", TUNE.pitches[:14], TUNE.beats[:14], [7, 14])
    sh = M.shuffled([two], seed=3)[0]                         # the same fourteen notes, in a random order
    shuffled = play(sh.pitches, sh.beats, beat=0.5)
    real = M.post_skip(CORPUS)
    chance = [M.post_skip(M.shuffled(CORPUS, s))["all"]["share"] for s in range(200)]
    tune_ps = M.post_skip([TUNE])
    return {"tune": rows(TUNE, (0, 2)), "times": note_times(first, 14), "shuffled": {"pitches": sh.pitches[:14], "beats": sh.beats[:14]}, "shuffled_times": note_times(shuffled, 14),
            "tunes": len(CORPUS), "notes": int(sum(len(m) for m in CORPUS)), "leaps": real["all"]["n"], "real": real["all"]["share"], "turned": real["all"]["reversal"], "went_on": real["all"]["continuation"],
            "chance": float(np.mean(chance)), "chance_sd": float(np.std(chance)), "tune_leaps": tune_ps["all"]["n"], "tune_share": tune_ps["all"]["share"],
            "shuffled_tune_share": M.post_skip([sh])["all"]["share"],
            "clips": {"tune": save("hook.tune", first, detail="the Tune's first two phrases: Part 7's piano"),
                      "shuffled": save("hook.shuffled", shuffled, detail="the same notes in a random order")}}


def compute_contour() -> dict:
    fj = BY_NAME["Frère Jacques"]
    n = fj.phrase_ends[3]                                    # the first four phrases
    p, b = fj.pitches[:n], fj.beats[:n]
    rng = np.random.default_rng(5)
    octs = []
    for k in range(n):                                       # the same notes, each thrown into another octave
        choices = [-12, 0, 12] if not octs else [o for o in (-12, 0, 12) if o != octs[-1]]
        octs.append(int(rng.choice(choices)))
    scrambled = [x + o for x, o in zip(p, octs)]
    stretched = [p[0]]                                       # the same ups and downs, every move twice as large
    for i in M.intervals(p):
        stretched.append(stretched[-1] + 2 * i)
    A = play(scrambled, b, beat=0.42)
    B = play(stretched, b, beat=0.42, base=C4 * 2 ** (-5 / 12))
    seq = concat([A.at_level(LEVEL), B.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    real = play(p, b, beat=0.42)
    same_contour = [int(np.sign(x)) for x in M.intervals(stretched)] == [int(np.sign(x)) for x in M.intervals(p)]
    kept = sum(int(np.sign(x) == np.sign(y)) for x, y in zip(M.intervals(scrambled), M.intervals(p)))
    return {"original": {"pitches": p, "beats": b}, "scrambled": scrambled, "stretched": stretched, "same_contour": bool(same_contour),
            "scrambled_kept": int(kept), "moves": n - 1, "times": {"A": note_times(seq, n, "A."), "B": note_times(seq, n, "B."), "real": note_times(real, n)},
            "clips": {"disguises": save("contour.disguises", seq, level=None, detail="one well-known tune, disguised two ways"),
                      "real": save("contour.real", real, detail="the tune as it is sung")}}


def bounded_walk(n: int, hist: dict, low: int = 0, high: int = 12, start: int = 0, seed: int = 0) -> list[int]:
    """A melody made by drawing each move from the corpus's histogram of intervals, kept inside a range and on
    the notes of the major scale."""
    rng = np.random.default_rng(seed)
    ivs = np.array(list(hist))
    w = np.array([hist[i] for i in ivs], dtype=float)
    out = [start]
    while len(out) < n:
        ok = [(i, x) for i, x in zip(ivs, w) if low <= out[-1] + i <= high and (out[-1] + i) % 12 in M.MAJOR]
        probs = np.array([x for _, x in ok])
        out.append(out[-1] + int(rng.choice([i for i, _ in ok], p=probs / probs.sum())))
    return out


def compute_steps() -> dict:
    s = M.shares(CORPUS)
    hist = M.interval_histogram(CORPUS)
    rng = np.random.default_rng(11)
    scale = [0, 2, 4, 5, 7, 9, 11, 12]
    urn = [int(rng.choice(scale)) for _ in range(16)]         # any note of the octave, each as likely as another
    walk = bounded_walk(16, hist, seed=4)
    A, B = play(urn, beat=0.36), play(walk, beat=0.36)
    two = concat([A.at_level(LEVEL), B.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    # one stream or two: the same alternation, a tone apart and nine semitones apart
    def gallop(gap: int, rate: float = 0.11, cycles: int = 14) -> Clip:
        y = []
        for k in range(cycles):
            for semi in (0, gap, 0):
                y.append(clip(organ_tone(hz_of(semi + 9), rate * 0.9, partials=3, rolloff=0.5), (0.008, 0.02)).y)
                y.append(np.zeros(int(rate * 0.1 * SR)))
            y.append(np.zeros(int(rate * SR)))
        return clip(np.concatenate(y), (0.005, 0.05)).at_level(LEVEL)

    streams = concat([gallop(2), gallop(9)], gap=0.8, names=["near", "far"])
    return {"shares": s, "histogram": {str(k): v for k, v in hist.items()}, "most_common": int(max((k for k in hist if k), key=lambda k: hist[k])),
            "urn": urn, "walk": walk, "times": {"A": note_times(two, 16, "A."), "B": note_times(two, 16, "B.")},
            "urn_mean": float(np.mean(np.abs(M.intervals(urn)))), "walk_mean": float(np.mean(np.abs(M.intervals(walk)))),
            "up": {"whole_tone": hist[2], "fourth": hist[5]}, "down": {"whole_tone": hist[-2], "fourth": hist[-5]},
            "clips": {"two": save("steps.two", two, level=None, detail="two made-up melodies on the white keys"),
                      "streams": save("steps.streams", streams, level=None, kind="synthesized", detail="three-note gallops: the middle note a tone away, then nine semitones away")}}


def compute_range() -> dict:
    spans = sorted(((M.span(m), m.name) for m in CORPUS))
    counts = Counter(s for s, _ in spans)
    banner = BY_NAME["The Star-Spangled Banner"]
    hot = BY_NAME["Hot Cross Buns"]
    seq = concat([melody_clip(hot, beat=0.36, phrases=(0, 2)).at_level(LEVEL), melody_clip(banner, beat=0.4, phrases=(0, 2), base=C4 * 2 ** (-5 / 12)).at_level(LEVEL)], gap=0.9, names=["narrow", "wide"])
    lo, hi = zip(*[M.tessitura(m) for m in CORPUS])
    rel = np.concatenate([np.array(m.pitches) - np.median(m.pitches) for m in CORPUS])        # every note, measured from the middle note of its own tune
    around, _ = np.histogram(rel, bins=np.arange(-9.5, 10.5, 1.0))
    return {"spans": [s for s, _ in spans], "names": [n for _, n in spans], "counts": {str(k): v for k, v in sorted(counts.items())}, "median": float(np.median([s for s, _ in spans])),
            "within_octave": sum(s <= 12 for s, _ in spans), "of": len(spans), "narrowest": list(spans[0]), "widest": list(spans[-1]),
            "tessitura": float(np.mean(np.array(hi) - np.array(lo))), "around": around.tolist(), "near": float(np.mean(np.abs(rel) <= 2.5)),
            "top_share": float(np.mean([np.mean(np.array(m.pitches) == max(m.pitches)) for m in CORPUS])),
            "narrow": rows(hot, (0, 2)), "wide": rows(banner, (0, 2)),
            "times": {"narrow": note_times(seq, len(rows(hot, (0, 2))["pitches"]), "narrow."), "wide": note_times(seq, len(rows(banner, (0, 2))["pitches"]), "wide.")},
            "clips": {"two": save("range.two", seq, level=None, detail="a tune of three notes; a tune of a twelfth")}}


def compute_arch() -> dict:
    shapes = Counter(M.contour_shape(ph) for m in CORPUS for ph in m.phrases)
    phrases = sum(len(m.phrases) for m in CORPUS)
    a = M.arch(CORPUS, bins=9)
    ode = BY_NAME["Ode to Joy"]
    c = melody_clip(ode, beat=0.45, phrases=(0, 2))
    sample = []
    for m in CORPUS[:30]:
        for ph in m.phrases[:2]:
            if len(ph) >= 5:
                x = np.linspace(0, 1, len(ph))
                sample.append(np.interp(np.linspace(0, 1, 9), x, np.asarray(ph, dtype=float) - np.mean(ph)).tolist())
    return {"shapes": dict(shapes.most_common()), "phrases": int(phrases), "arch": a.tolist(), "sample": sample[:40], "peak_at": int(np.argmax(a)),
            "end_minus_start": float(a[-1] - a[0]), "ode": rows(ode, (0, 2)), "times": note_times(c, len(rows(ode, (0, 2))["pitches"])),
            "clips": {"ode": save("arch.ode", c, detail="two phrases of Beethoven's tune")}}


def interval_shuffled(tunes, seed: int = 0):
    """Each tune with its moves in a random order: as many steps and leaps as it had, in no particular order."""
    rng = np.random.default_rng(seed)
    out = []
    for m in tunes:
        iv = rng.permutation(M.intervals(m))
        p = [m.pitches[0]]
        for i in iv:
            p.append(p[-1] + int(i))
        out.append(M.Melody(m.name, p, list(m.beats), list(m.phrase_ends), m.mode, m.origin))
    return out


def compute_leaps() -> dict:
    real = M.post_skip(CORPUS)
    kinds = ("all", "departing", "approaching", "crossing")
    chance = [M.post_skip(M.shuffled(CORPUS, s)) for s in range(200)]
    urn = M.post_skip([M.urn_melody(400, seed=s) for s in range(40)])
    out = {k: {"real": real[k]["share"], "n": real[k]["n"], "shuffled": float(np.mean([c[k]["share"] for c in chance])),
               "shuffled_sd": float(np.std([c[k]["share"] for c in chance])), "urn": urn[k]["share"]} for k in kinds}
    u = M.urn_melody(24, seed=2)
    c = play(u, beat=0.34)
    return {"kinds": out, "urn_melody": u, "urn_times": note_times(c, 24), "median": float(np.median(u)),
            "clips": {"urn": save("leaps.urn", c, detail="twenty-four notes drawn from an urn")}}


def compute_tendency() -> dict:
    t = M.degree_transitions(CORPUS)
    share = M.degree_counts(CORPUS)
    gf = M.gap_fill(CORPUS)
    notes_sh = float(np.mean([M.gap_fill(M.shuffled(CORPUS, s))["share"] for s in range(60)]))
    moves_sh = float(np.mean([M.gap_fill(interval_shuffled(CORPUS, s))["share"] for s in range(60)]))
    # steps in a confined range: melodies made by chance from the corpus's moves, kept within an octave
    hist = M.interval_histogram(CORPUS)
    walks = [M.Melody("", bounded_walk(len(m), hist, low=0, high=12, start=int(np.clip(m.pitches[0], 0, 12)) if m.pitches[0] % 12 in M.MAJOR else 0, seed=k), [1.0] * len(m), [len(m)])
             for k, m in enumerate(CORPUS * 4)]
    walk_fill = M.gap_fill(walks)["share"]
    # the Tune's second phrase with three endings
    model = M.NGram(2).fit(OTHERS)
    stem = TUNE.pitches[7:13]                                # 4 4 3 3 2 2
    ends = {"2": 2, "7": -1, "1": 0}
    probs = {k: float(model.distribution(stem)[v]) for k, v in ends.items()}
    parts = [play(stem + [v], [1] * 6 + [2], beat=0.45).at_level(LEVEL) for v in ends.values()]
    c = concat(parts, gap=0.9, names=["A", "B", "C"])
    return {"transitions": t.tolist(), "share": share.tolist(), "triad": float(share[0] + share[2] + share[4]),
            "goes": {str(d + 1): {"to": int(np.argmax(t[d])) + 1, "p": float(np.max(t[d]))} for d in range(7)},
            "gap_fill": {"real": gf["share"], "leaps": gf["leaps"], "notes_shuffled": notes_sh, "moves_shuffled": moves_sh, "walks": walk_fill},
            "stem": stem, "endings": ends, "ending_probs": probs,
            "times": {k: note_times(c, 7, f"{k}.") for k in "ABC"},
            "clips": {"endings": save("tendency.endings", c, level=None, detail="one phrase of the Tune with three last notes")}}


def self_similarity(m: M.Melody) -> list[list[int]]:
    """Note against note: 1 where two notes are the same pitch and are followed by the same move."""
    iv = M.intervals(m) + [0]
    n = len(m)
    return [[int(m.pitches[i] == m.pitches[j] and iv[i] == iv[j]) for j in range(n)] for i in range(n)]


def compute_motive() -> dict:
    found = {m.name: [s for n in range(3, 9) for s in M.sequences(m, n)] for m in CORPUS}       # patterns of three to eight notes
    exact = [n for n, f in found.items() if any(s["shift"] == 0 for s in f)]
    moved = [n for n, f in found.items() if any(s["shift"] != 0 for s in f)]
    either = sorted(set(exact) | set(moved))
    # how much of a tune is a phrase heard before (the same pitches and rhythm as an earlier phrase)
    repeated = total = 0
    for m in CORPUS:
        ends = [0] + m.phrase_ends
        seen = []
        for a, b in zip(ends, ends[1:]):
            key = (tuple(m.pitches[a:b]), tuple(m.beats[a:b]))
            total += 1
            repeated += key in seen
            seen.append(key)
    kk = BY_NAME["Kuckuck, Kuckuck"]
    joy = BY_NAME["Joy to the World"]
    c1 = melody_clip(kk, beat=0.4, phrases=(2, 4))
    c2 = melody_clip(joy, beat=0.36, phrases=(4, 6))
    seq = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=0.9, names=["kuckuck", "joy"])
    fj = BY_NAME["Frère Jacques"]
    return {"exact": len(exact), "moved": len(moved), "either": len(either), "of": len(CORPUS), "moved_names": moved, "phrases_repeated": repeated, "phrases": total,
            "kuckuck": rows(kk, (2, 4)), "joy": rows(joy, (4, 6)), "kuckuck_seq": M.sequences(kk, 5)[0] if M.sequences(kk, 5) else None,
            "times": {"kuckuck": note_times(seq, len(rows(kk, (2, 4))["pitches"]), "kuckuck."), "joy": note_times(seq, len(rows(joy, (4, 6))["pitches"]), "joy.")},
            "matrix": self_similarity(fj), "matrix_name": fj.name, "matrix_ends": fj.phrase_ends,
            "clips": {"sequence": save("motive.sequence", seq, level=None, detail="a pattern, and the same pattern one step away: two tunes")}}


def compute_phrase() -> dict:
    lengths = Counter()
    last, other = [], []
    mid_end, final_end = Counter(), Counter()
    for m in CORPUS:
        ends = [0] + m.phrase_ends
        d = m.degrees()
        for k, (a, b) in enumerate(zip(ends, ends[1:])):
            lengths[int(round(sum(m.beats[a:b])))] += 1
            last.append(m.beats[b - 1])
            other += m.beats[a:b - 1]
            (final_end if k == len(ends) - 2 else mid_end)[d[b - 1]] += 1
    mid_total, fin_total = sum(mid_end.values()), sum(final_end.values())
    ode = BY_NAME["Ode to Joy"]
    c = melody_clip(ode, beat=0.42)
    return {"lengths": {str(k): v for k, v in sorted(lengths.items())}, "common": [int(k) for k, _ in lengths.most_common(3)],
            "last_mean": float(np.mean(last)), "other_mean": float(np.mean(other)), "lengthening": float(np.mean(last) / np.mean(other)),
            "mid_end": {str(k): mid_end.get(k, 0) / mid_total for k in range(1, 8)}, "final_end": {str(k): final_end.get(k, 0) / fin_total for k in range(1, 8)},
            "ode": rows(ode), "times": note_times(c, len(ode)), "phrase_times": [float(c.events[f"p{k}"]) for k in range(4)],
            "clips": {"ode": save("phrase.ode", c, detail="Beethoven's tune: four phrases")}}


def compute_info() -> dict:
    alphabet = sorted({p for m in CORPUS for p in m.pitches})
    ce = [M.cross_entropy(CORPUS, o) for o in range(6)]
    z = M.zipf(CORPUS, 2)
    return {"alphabet": len(alphabet), "uniform": float(np.log2(len(alphabet))), "unigram": M.entropy([p for m in CORPUS for p in m.pitches]),
            "by_order": ce, "best_order": int(np.argmin(ce)), "zipf": {"rank": z["rank"], "frequency": z["frequency"], "slope": z["slope"], "kinds": z["kinds"], "total": z["total"], "top": z["top"]},
            "intervals_entropy": M.entropy([i for m in CORPUS for i in M.intervals(m)])}


NOTE_NAMES = {-12: "C", -10: "D", -8: "E", -7: "F", -5: "G", -3: "A", -1: "B", 0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B", 12: "C", 14: "D", 16: "E", 17: "F", 19: "G"}


def compute_model() -> dict:
    model = M.NGram(2).fit(OTHERS)
    s = model.surprise(TUNE)
    c = melody_clip(TUNE, beat=0.48, phrases=(0, 4))
    n = TUNE.phrase_ends[3]
    after = {}
    for label, ctx in (("C, C", [0, 0]), ("C, C, G, G, A, A", [0, 0, 7, 7, 9, 9]), ("F, F, E, E, D, D", [5, 5, 4, 4, 2, 2])):
        after[label] = [{"note": NOTE_NAMES.get(p, str(p)), "pitch": int(p), "p": float(q)} for p, q in model.continuations(ctx, 4)]
    gens, parts = {}, []
    full = M.NGram(0).fit(CORPUS), M.NGram(1).fit(CORPUS), M.NGram(2).fit(CORPUS)
    for o, mdl in enumerate(full):
        seed = 7 + o
        g = mdl.generate(16, start=(0,), seed=seed)
        while max(len(list(grp)) for _, grp in __import__("itertools").groupby(g)) > 3:      # skip a draw that sits on one note
            seed += 10
            g = mdl.generate(16, start=(0,), seed=seed)
        gens[str(o)] = g
        parts.append(play(g, beat=0.36).at_level(LEVEL))
    seq = concat(parts, gap=0.9, names=["o0", "o1", "o2"])
    return {"surprise": s.tolist(), "mean": float(s.mean()), "peak": float(s.max()), "peak_at": int(np.argmax(s)), "tune": rows(TUNE, (0, 4)), "times": note_times(c, n),
            "after": after, "generated": gens, "gen_times": {k: note_times(seq, 16, f"o{k}.") for k in "012"},
            "gen_surprise": {k: float(full[2].surprise(v).mean()) for k, v in gens.items()},
            "clips": {"tune": save("model.tune", c, detail="four phrases of the Tune"),
                      "orders": save("model.orders", seq, level=None, detail="three melodies made by the model: with no memory, one note of memory, two")}}


def compute_tone() -> dict:
    # Mandarin's four tones as pitch contours on the five-level scale of Chao (1930): 55, 35, 214, 51
    levels = {"1": [5, 5, 5], "2": [3, 4, 5], "3": [2, 1, 4], "4": [5, 3, 1]}
    lo, hi = 110.0, 190.0
    f_of = lambda lv: lo * (hi / lo) ** ((lv - 1) / 4.0)                    # noqa: E731
    seconds = 0.5
    n = int(seconds * SR)
    formants = WINDS.VOWELS["a"] if "a" in WINDS.VOWELS else list(WINDS.VOWELS.values())[0]
    parts, curves = [], {}
    for name, lv in levels.items():
        f = np.interp(np.linspace(0, 1, n), [0, 0.5, 1], [f_of(x) for x in lv])
        y = WINDS.voice(f, formants, seconds, seed=3)
        parts.append(clip(y, (0.03, 0.08)).at_level(LEVEL))
        curves[name] = f[:: n // 40].tolist()
    c = concat(parts, gap=0.35, names=["t1", "t2", "t3", "t4"])
    return {"levels": levels, "curves": curves, "lo": lo, "hi": hi, "starts": [float(c.events[f"t{k}"]) for k in (1, 2, 3, 4)], "seconds": seconds,
            "cantonese_match": 0.918, "vowel": "a",
            "clips": {"four": save("tone.four", c, level=None, kind="physical model", detail="one vowel on Part 8's voice, with four pitch shapes")}}


def proximity_bits(tunes, tau: float) -> float:
    """Bits per note for a predictor that knows only that the next note is probably near the last."""
    alphabet = np.array(sorted({p for m in tunes for p in m.pitches}))
    bits = n = 0
    for m in tunes:
        for a, b in zip(m.pitches, m.pitches[1:]):
            w = np.exp(-np.abs(alphabet - a) / tau)
            bits += -np.log2(w[list(alphabet).index(b)] / w.sum())
            n += 1
    return float(bits / n)


def compute_frontier() -> dict:
    taus = np.linspace(0.8, 5.0, 22)
    prox = [proximity_bits(CORPUS, t) for t in taus]
    info = load("info")
    return {"uniform": info["uniform"], "unigram": info["by_order"][0], "proximity": float(min(prox)), "tau": float(taus[int(np.argmin(prox))]),
            "ngram": float(min(info["by_order"])), "ngram_order": info["best_order"]}


def contour_code(m, n: int) -> str:
    """Parsons's code: the first n moves of a tune as U (up), D (down) or R (repeat)."""
    return "".join("U" if i > 0 else "D" if i < 0 else "R" for i in M.intervals(m)[:n])


def compute_more() -> dict:
    """Numbers and sounds for the passages added after the first cut."""
    out = {}
    # 1. one tune in two keys
    ph = TUNE.pitches[:7]
    keys = concat([play(ph, TUNE.beats[:7], beat=0.45).at_level(LEVEL), play(ph, TUNE.beats[:7], beat=0.45, base=C4 * 2 ** (6 / 12)).at_level(LEVEL)], gap=0.8, names=["C", "Fs"])
    out["keys"] = {"times": {"C": note_times(keys, 7, "C."), "Fs": note_times(keys, 7, "Fs.")}, "pitches": ph, "beats": TUNE.beats[:7], "shared": 0}
    # 2. how many moves of contour (or of exact interval) it takes to tell the tunes apart
    def unique(code, n):
        seen = {}
        for m in CORPUS:
            seen.setdefault(code(m, n), []).append(m.name)
        return sum(1 for v in seen.values() if len(v) == 1)

    exact = lambda m, n: tuple(M.intervals(m)[:n])                              # noqa: E731
    out["parsons"] = {"n": list(range(2, 16)), "contour": [unique(contour_code, n) for n in range(2, 16)], "interval": [unique(exact, n) for n in range(2, 16)],
                      "tune_code": contour_code(TUNE, 13), "of": len(CORPUS)}
    # 3. three rolls of a die: after a rise of two or more, how often does the third roll fall?
    rise = [(a, b, c) for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) if b - a >= 2]
    fall = sum(c < b for _, b, c in rise)
    stay = sum(c == b for _, b, c in rise)
    out["dice"] = {"cases": len(rise), "fall": fall, "rise": len(rise) - fall - stay, "same": stay, "share": fall / (len(rise) - stay), "mean_landing": float(np.mean([b for _, b, _ in rise]))}
    # 4. where the highest note of a tune first comes, as a fraction of the tune's length
    where = []
    for m in CORPUS:
        on = np.concatenate([[0.0], np.cumsum(m.beats)])
        where.append(float(on[int(np.argmax(m.pitches))] / on[-1]))
    hist, _ = np.histogram(where, bins=5, range=(0, 1))
    out["peak"] = {"where": where, "fifths": hist.tolist(), "mean": float(np.mean(where)), "median": float(np.median(where)), "second_half": int(sum(w >= 0.5 for w in where)), "of": len(where)}
    # 5. after a step, does the next move keep going?  And where do leaps land?
    def inertia(tunes):
        keep = {1: [0, 0], -1: [0, 0]}
        for m in tunes:
            iv = M.intervals(m)
            for a, b in zip(iv, iv[1:]):
                if 1 <= abs(a) <= 2 and b != 0:
                    keep[int(np.sign(a))][0] += int(np.sign(b) == np.sign(a))
                    keep[int(np.sign(a))][1] += 1
        return {"up": keep[1][0] / keep[1][1], "down": keep[-1][0] / keep[-1][1]}

    real = inertia(CORPUS)
    sh = [inertia(interval_shuffled(CORPUS, k)) for k in range(60)]
    land_leap, land_step = [], []
    for m in CORPUS:
        if m.mode != "major":
            continue
        d = m.degrees()
        for k, i in enumerate(M.intervals(m)):
            (land_leap if abs(i) >= 3 else land_step if abs(i) >= 1 else []).append(d[k + 1] in (1, 3, 5))
    out["inertia"] = {"real": real, "chance": {"up": float(np.mean([x["up"] for x in sh])), "down": float(np.mean([x["down"] for x in sh]))},
                      "leaps_on_triad": float(np.mean(land_leap)), "steps_on_triad": float(np.mean(land_step))}
    # 6. the plan of a tune: its phrases as letters
    def letters(m):
        ends = [0] + m.phrase_ends
        seen, out_ = [], ""
        for a, b in zip(ends, ends[1:]):
            key = (tuple(m.pitches[a:b]), tuple(m.beats[a:b]))
            if key not in seen:
                seen.append(key)
            out_ += "ABCDEFGH"[seen.index(key)]
        return out_

    out["form"] = {name: letters(BY_NAME[name]) for name in (M.THE_TUNE, "Frère Jacques", "Mary Had a Little Lamb", "Au clair de la lune", "Lightly Row (Hänschen klein)", "Good King Wenceslas")}
    # 7. the guessing game: how often is the model's first guess right?  Its first three?
    alphabet = sorted({p for m in CORPUS for p in m.pitches})
    ranks, per_tune = [], {}
    for k, m in enumerate(CORPUS):
        mdl = M.NGram(1, alphabet).fit(CORPUS[:k] + CORPUS[k + 1:])
        per_tune[m.name] = float(mdl.surprise(m)[1:].mean())
        for j in range(1, len(m)):
            d = mdl.distribution(m.pitches[:j])
            order = sorted(d, key=lambda q: -d[q])
            ranks.append(order.index(m.pitches[j]) + 1)
    ranks = np.array(ranks)
    out["guess"] = {"first": float(np.mean(ranks == 1)), "three": float(np.mean(ranks <= 3)), "mean_rank": float(ranks.mean()), "notes": int(len(ranks)), "chance_first": 1.0 / len(alphabet)}
    # 8. the most and the least predictable tunes
    order = sorted(per_tune, key=per_tune.get)
    easy, hard = BY_NAME[order[0]], BY_NAME[order[-1]]
    ex = concat([melody_clip(easy, beat=0.4, phrases=(0, 2)).at_level(LEVEL), melody_clip(hard, beat=0.4, phrases=(0, 2)).at_level(LEVEL)], gap=0.9, names=["easy", "hard"])
    out["extremes"] = {"easy": {"name": order[0], "bits": per_tune[order[0]], **rows(easy, (0, 2))}, "hard": {"name": order[-1], "bits": per_tune[order[-1]], **rows(hard, (0, 2))},
                       "next_easy": [(n, per_tune[n]) for n in order[:4]], "next_hard": [(n, per_tune[n]) for n in order[-4:]], "tune_bits": per_tune[M.THE_TUNE],
                       "tune_rank": order.index(M.THE_TUNE) + 1,
                       "times": {"easy": note_times(ex, len(rows(easy, (0, 2))["pitches"]), "easy."), "hard": note_times(ex, len(rows(hard, (0, 2))["pitches"]), "hard.")}}
    out["clips"] = {"keys": save("contour.keys", keys, level=None, detail="one phrase of the Tune, on C and then on F sharp"),
                    "extremes": save("model.extremes", ex, level=None, detail="the tune the model finds easiest, and the one it finds hardest")}
    return out


def compute_tune() -> dict:
    model = M.NGram(2).fit(OTHERS)
    beat = 0.46
    ph = lambda k: M.Melody("", TUNE.pitches[7 * k: 7 * k + 7], TUNE.beats[7 * k: 7 * k + 7], [7], "major")       # noqa: E731
    first, second = ph(0), ph(1)
    versions = [("as it is", first), ("with neighbour notes", M.ornament(first, "neighbour")), ("with the leap filled in", M.ornament(first, "passing")),
                ("with turns", M.ornament(second, "turn")), ("upside down", M.invert(first)), ("backwards", M.retrograde(first))]
    # what the model expects after the first phrase, and what it expects least
    ctx = list(first.pitches)
    most, least = [], []
    for _ in range(7):
        d = model.distribution(ctx + most)
        most.append(int(max(d, key=d.get)))
    for _ in range(7):
        d = {k: v for k, v in model.distribution(ctx + least).items() if 0 <= k <= 12 and k % 12 in M.MAJOR}
        least.append(int(min(d, key=d.get)))
    b7 = [1, 1, 1, 1, 1, 1, 2]
    versions += [("continued as the model expects", M.Melody("", most, b7, [7], "major")), ("continued as it expects least", M.Melody("", least, b7, [7], "major"))]
    placed, events, phrases, t0 = [], {}, [], 0.0
    for k, (name, m) in enumerate(versions):
        base = 12 if name == "upside down" else 0
        c = play([p + base for p in m.pitches], m.beats, beat=beat, last=1.0)
        placed.append((c, t0, 0.0))
        events[f"phrase{k}"] = t0
        context = [] if k < 6 else ctx
        s = model.surprise(context + [p + base for p in m.pitches])[len(context):]
        phrases.append({"name": name, "pitches": [p + base for p in m.pitches], "beats": list(m.beats), "t0": t0, "seconds": float(sum(m.beats) * beat),
                        "times": [t0 + float(c.events[f"n{j}"]) for j in range(len(m))], "bits": float(s.mean())})
        t0 += sum(m.beats) * beat
    events["end"] = t0
    out = Clip(mix(placed, duration=t0 + 1.4).y, SR, events, []).at_level(LEVEL)
    return {"clip": save("tune.variation14", out, level=None, detail="the Tune's first phrase, eight ways: Part 7's piano"), "seconds": out.duration, "phrases": phrases,
            "names": [n for n, _ in versions], "most": most, "least": least, "bits_plain": phrases[0]["bits"], "bits_most": phrases[6]["bits"], "bits_least": phrases[7]["bits"]}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 14, "title": r"decorated, upside down, backwards, and continued as a model expects and as it expects least", "seconds": t["seconds"],
            "measure": rf"the expected continuation costs {t['bits_most']:.1f} bits a note; the least expected, {t['bits_least']:.1f}", "clip": "tune.variation14"}


ITEMS = {"hook": compute_hook, "contour": compute_contour, "steps": compute_steps, "range": compute_range, "arch": compute_arch, "leaps": compute_leaps,
         "tendency": compute_tendency, "motive": compute_motive, "phrase": compute_phrase, "info": compute_info, "model": compute_model, "tone": compute_tone,
         "frontier": compute_frontier, "more": compute_more, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
