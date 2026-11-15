"""Precompute everything numerical, and every sound, in Part 47 of *Music, Built* ("Origins and Universals").

    python -m videos.music.music47.compute              # everything missing (about three minutes)
    python -m videos.music.music47.compute --force chains

Numbers are cached in ``.cache/music47/<name>.json``, sounds in ``.cache/music47/audio/``.  The tools are Monochord's
(``explainer/music/monochord/origins.py``).  Every transmission, listener and dancer here is simulated, and says so;
published findings (Conard, Mehr, Savage, Jacoby and McDermott, Patel, Pietschnig, Sala and Gobet) are quoted, not
reproduced.  Sounds: Part 9's flute (a jet against an edge), Part 16's singing voice, Part 7's piano, Part 40's drums,
a struck-wood tap (a sum of decaying partials).

Items:
    hook        a pipe the size of the Hohle Fels flute, with five holes, by Part 9's flute model
    lullaby     an ear question: one melody as a dance song and as a lullaby
    universals  six of Savage's statistical universals, checked on the series' corpus of tunes
    rhythm      iterated reproduction of three-interval rhythms by two simulated listeners with different priors
    chains      twenty random melodies, each passed through forty simulated singers
    sampling    a learner that samples its posterior forgets a melody; one that takes the most probable value keeps it
    tune47      Variation 47: the Tune through thirty singers
    family      the Tune passed down a branching family of singers, and the tree rebuilt from alignment distances
    relatives   the Tune's real relatives and some unrelated tunes, aligned and clustered
    npvi        rhythmic contrast (nPVI) by language: the corpus's folk tunes and the Library's composers
    beat        an ear question: two simulated dancers; which is on the beat? and Rayleigh's test
    amusia      an ear question in the style of the Montreal battery: which pair of melodies differed?
    mozart      many small studies of a small effect, and what the published ones say
    variation   the Variations ledger, row 47
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord import origins as O
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments.percussion import modal
from explainer.music.monochord.instruments.winds import jet_tone
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.romantic import load_library
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40

CACHE = Cache("music47")
CLIPS = ClipStore("music47")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano = P38.piano
TUNES = M.corpus()
THE = [t for t in TUNES if t.name == M.THE_TUNE][0]
TUNE_MEL = [[float(p), float(b)] for p, b in zip(THE.pitches, THE.beats)]


def as_mel(m) -> list:
    return [[float(p), float(b)] for p, b in zip(m.pitches, m.beats)]


def voice_clip(mel, beat=0.42, base=64, part="soprano", vowel="u", tail=0.8, legato=0.96, seed=0, centre=True):
    """A melody ([pitch, beats]) sung by Part 16's voice, its median pitch placed on key ``base``."""
    mid = float(np.median([x[0] for x in mel])) if centre else 0.0
    notes, t = [], 0.0
    for p, b in mel:
        notes.append((base + p - mid, t, b * beat * legato))
        t += b * beat
    y = CH.sing(notes, part, vowel, tail=tail, seed=seed)
    return Clip(y / max(np.abs(y).max(), 1e-9), SR)


def piano_line(mel, beat=0.4, base=60, vel=0.7, tail=1.0):
    p, t = [], 0.0
    for m, b in mel:
        p.append((arr(piano(base + m, b * beat * 0.97, vel)), t, 0.0))
        t += b * beat
    return Clip(mix(p, duration=t + tail).y, SR)


def tap(seconds=0.25, f=1150.0):
    return Clip(modal([f, 2.71 * f, 4.9 * f], [1.0, 0.45, 0.2], [38.0, 70.0, 120.0], seconds), SR)


def names(mel, ref_median=None):
    """Note names of a melody whose pitches are semitones above C (moved so that its median matches ``ref_median``)."""
    letters = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    off = 0.0 if ref_median is None else float(np.median([x[0] for x in mel])) - ref_median
    return [letters[int(round(x[0] - off)) % 12] for x in mel]


# ---------------------------------------------------------------------------------------------------------- items
HOLES = [0.090, 0.110, 0.130, 0.150, 0.170]               # metres from the blown end: evenly spaced, 2 cm apart


def compute_hook() -> dict:
    L, bore = 0.218, 0.008
    hz = O.holes_scale(L, bore, HOLES)
    seq = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]
    tune = [(0, 1), (2, 1), (3, 1), (2, 1), (1, 2), (0, 1), (1, 1), (2, 2), (0, 3)]
    beat = 0.36
    p, t = [], 0.0
    for k in seq:
        p.append((Clip(jet_tone(hz[k], beat * 0.95, noise=0.04, seed=k), SR).fade(0.01, 0.03), t, 0.0))
        t += beat
    t += 0.7
    for k, b in tune:
        p.append((Clip(jet_tone(hz[k], b * beat * 1.4 * 0.95, noise=0.04, seed=10 + k), SR).fade(0.01, 0.05), t, 0.0))
        t += b * beat * 1.4
    c = Clip(mix(p, duration=t + 0.6).y, SR)
    cents = [1200 * math.log2(f / hz[0]) for f in hz]
    return {"length": L, "bore": bore, "holes": HOLES, "hz": hz, "cents": cents,
            "fundamental": {"0.218": O.pipe_hz(0.218, bore), "0.34": O.pipe_hz(0.34, bore)},
            "steps": [cents[i + 1] - cents[i] for i in range(len(cents) - 1)], "seq": seq, "tune": [list(x) for x in tune],
            "clips": {"flute": save("hook.flute", c, detail="a pipe 21.8 cm long and 8 mm across with five evenly spaced holes, opened one by one and then played as a little tune; Part 9's flute model, not a reconstruction of any real flute's tuning")}}


AU_CLAIR = [(0, 1), (0, 1), (0, 1), (2, 1), (4, 2), (2, 2), (0, 1), (4, 1), (2, 1), (2, 1), (0, 4)]


def compute_lullaby() -> dict:
    mel = [[float(p), float(b)] for p, b in AU_CLAIR]
    # the lullaby: slow, soft, smooth, in a low comfortable range, a falling tail, one voice
    lul_bpm = 66
    lul = voice_clip(mel, beat=60 / lul_bpm, base=60, part="soprano", vowel="u", legato=1.0, tail=1.2, seed=1)
    # the dance song: fast, loud, short notes, a higher range, accents and a drum kit
    dan_bpm = 132
    db = 60 / dan_bpm
    v = voice_clip(mel, beat=db, base=67, part="tenor", vowel="a", legato=0.55, tail=0.3, seed=2)
    parts = [(v, 0.0, 0.0)]
    bars = int(math.ceil(sum(b for _, b in mel) / 4))
    P40.drums(parts, "rock", dan_bpm, bars, gain=-1.0)
    dance = Clip(mix(parts, duration=bars * 4 * db + 0.6).y, SR)
    c = concat([dance.at_level(LEVEL), lul.at_level(LEVEL + 2.0)], gap=1.2, names=["first", "second"])
    feats = {"tempo (beats a minute)": [dan_bpm, lul_bpm], "note held for (share of its beat)": [0.55, 1.0],
             "range (keys above the lowest note)": [4, 4], "voices and instruments": [2, 1]}
    return {"order": ["dance", "lullaby"], "answer": "second", "features": feats, "bpm": {"dance": dan_bpm, "lullaby": lul_bpm},
            "notes": [list(x) for x in AU_CLAIR],
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("lullaby.two", c, detail="the opening of Au clair de la lune sung fast and short over drums, then slow, smooth and soft; Part 16's voice and Part 40's drums")}}


def compute_universals() -> dict:
    rows = {t.name: O.universals(t) for t in TUNES}
    feats = list(next(iter(rows.values())))
    share = {f: float(np.mean([r[f] for r in rows.values()])) for f in feats}
    fails = {f: [n for n, r in rows.items() if not r[f]] for f in feats}
    origins = sorted({t.origin for t in TUNES})
    return {"features": feats, "share": share, "fails": fails, "tunes": len(rows), "rows": {n: [bool(r[f]) for f in feats] for n, r in rows.items()},
            "origins": len(origins)}


PRIOR_A = {(1, 1, 2): 2.0, (1, 1, 1): 1.0, (1, 2, 2): 0.6, (1, 2, 3): 0.3}
PRIOR_B = {(2, 2, 3): 2.0, (1, 1, 1): 0.6, (1, 1, 2): 0.5, (1, 2, 2): 0.4}


def rhythm_clip(x, cycle=2.0, loops=4):
    on = [0.0, x[0], x[0] + x[1]]
    parts = [(tap(), (k + o) * cycle, 0.0 if i == 0 else -3.0) for k in range(loops) for i, o in enumerate(on)]
    return Clip(mix(parts, duration=loops * cycle + 0.4).y, SR)


def compute_rhythm() -> dict:
    out = {}
    for name, w in (("A", PRIOR_A), ("B", PRIOR_B)):
        pr = O.RhythmPrior(w)
        ch = O.rhythm_chains(pr, 400, 5, seed=47)
        ends = Counter_patterns(pr, ch[:, -1])
        starts = Counter_patterns(pr, ch[:, 0])
        prior_share = {"-".join(map(str, k)): float(v / sum(w.values()) * (1 - pr.floor)) for k, v in w.items()}
        out[name] = {"weights": {"-".join(map(str, k)): v for k, v in w.items()}, "mass": [pr.mass_near(ch[:, i]) for i in range(6)],
                     "end_share": ends, "start_share": starts, "prior_share": prior_share,
                     "paths": ch[:160].round(4).tolist(), "points": pr.points.tolist()}
    ch = np.array(out["A"]["paths"])
    first = ch[0, 0]
    last = ch[0, -1]
    c = concat([rhythm_clip(first), rhythm_clip(last)], gap=1.2, names=["start", "end"])
    out["example"] = {"start": first.tolist(), "end": last.tolist()}
    out["starts"] = {"start": float(c.events["start"]), "end": float(c.events["end"])}
    out["clips"] = {"two": save_synth("rhythm.two", c, detail="a random three-interval rhythm looped four times, then what one simulated listener tapped after five rounds of hearing its own tapping; struck-wood taps")}
    return out


def Counter_patterns(pr, ys) -> dict:
    counts = {}
    for y in ys:
        k = O.nearest_pattern(pr, y)
        key = "-".join(map(str, k)) if k else "none"
        counts[key] = counts.get(key, 0) + 1
    n = len(ys)
    return {k: v / n for k, v in counts.items()}


GENS = 40
KEYS = ["levels", "reused", "step", "simple", "durations", "repeats", "echo"]


def compute_chains() -> dict:
    rng = np.random.default_rng(47)
    chains = [O.transmission_chain(O.random_melody(rng), GENS, rng) for _ in range(20)]
    stats = {k: [] for k in KEYS}
    for g in range(GENS + 1):
        ss = [O.structure(ch[g]) for ch in chains]
        for k in KEYS:
            v = np.array([s[k] for s in ss], float)
            stats[k].append([float(np.percentile(v, 25)), float(np.mean(v)), float(np.percentile(v, 75))])
    err = np.array([[O.align(ch[g], ch[g + 1])["per_note"] for g in range(GENS)] for ch in chains])
    ex = chains[0]
    show = [0, 1, 5, 10, 20, 40]
    c = concat([voice_clip(ex[0], beat=0.42, base=64, seed=3), voice_clip(ex[GENS], beat=0.42, base=64, seed=4)], gap=1.2, names=["first", "last"])
    return {"stats": stats, "error": err.mean(0).tolist(), "error_q": [np.percentile(err, 25, axis=0).tolist(), np.percentile(err, 75, axis=0).tolist()],
            "example": {str(g): ex[g] for g in show}, "show": show, "generations": GENS, "chains": len(chains),
            "lengths": [len(ch[-1]) for ch in chains],
            "starts": {"first": float(c.events["first"]), "last": float(c.events["last"])},
            "clips": {"two": save_synth("chains.two", c, detail="a random melody, then what it became after forty simulated singers; Part 16's voice")}}


def compute_sampling() -> dict:
    out = {}
    for mode in ("best", "sample"):
        d = []
        for seed in range(12):
            ch = O.transmission_chain(TUNE_MEL, 30, np.random.default_rng(seed), {"choose": mode})
            d.append([O.align(TUNE_MEL, ch[g])["per_note"] for g in range(31)])
        d = np.array(d)
        out[mode] = {"mean": d.mean(0).tolist(), "lo": np.percentile(d, 25, axis=0).tolist(), "hi": np.percentile(d, 75, axis=0).tolist()}
    return out


def kept_notes(a, b) -> int:
    """Notes of ``a`` aligned to a note of ``b`` with the same pitch (within half a semitone, once ``b`` is moved by the
    median difference over the aligned notes, so that a tune sung a little higher still counts) and the same duration
    (within 10 per cent)."""
    r = O.align(a, b)
    both = [(i, j) for i, j in r["pairs"] if i is not None and j is not None]
    shift = float(np.median([a[i][0] - b[j][0] for i, j in both]))
    return sum(1 for i, j in both if abs(a[i][0] - b[j][0] - shift) < 0.5 and abs(math.log(a[i][1] / b[j][1])) < 0.1)


def compute_tune47() -> dict:
    rng = np.random.default_rng(47)
    ch = O.transmission_chain(TUNE_MEL, 30, rng)
    dist = [O.align(TUNE_MEL, m)["per_note"] for m in ch]
    show = [0, 10, 20, 30]
    ref = float(np.median(THE.pitches))
    c = concat([voice_clip(ch[g], beat=0.36, base=64 + 0, seed=g, tail=0.6) for g in (0, 15, 30)], gap=1.0, names=["g0", "g15", "g30"])
    last = ch[30]
    return {"melodies": {str(g): ch[g] for g in show}, "show": show, "distance": dist, "notes_in": len(TUNE_MEL), "notes_out": len(last),
            "kept": kept_notes(TUNE_MEL, last), "names": {str(g): names(ch[g], ref) for g in show},
            "steps": {str(g): O.structure(ch[g])["step"] for g in show}, "seconds": c.duration,
            "starts": {"g0": float(c.events["g0"]), "g15": float(c.events["g15"]), "g30": float(c.events["g30"])},
            "clips": {"variation47": save_synth("tune.variation47", c, detail="the Tune sung by Part 16's voice, then as the fifteenth and the thirtieth simulated singer sang it")}}


def compute_family() -> dict:
    rng = np.random.default_rng(1950)
    tt = O.tree_transmission(TUNE_MEL, 3, 12, rng)
    nm = sorted(tt["leaves"])
    D = O.distances([tt["leaves"][n] for n in nm])
    u = O.upgma(D, nm)
    rf = O.robinson_foulds(tt["tree"], u["tree"])
    trials, rand = [], []
    r2 = np.random.default_rng(7)
    for _ in range(20):
        t2 = O.tree_transmission(TUNE_MEL, 3, 12, r2)
        n2 = sorted(t2["leaves"])
        u2 = O.upgma(O.distances([t2["leaves"][n] for n in n2]), n2)
        trials.append(6 - O.robinson_foulds(t2["tree"], u2["tree"]) // 2)
        perm = list(r2.permutation(n2))
        fake = (((perm[0], perm[1]), (perm[2], perm[3])), ((perm[4], perm[5]), (perm[6], perm[7])))
        rand.append(6 - O.robinson_foulds(t2["tree"], fake) // 2)
    return {"names": nm, "D": D.round(4).tolist(), "true": tt["tree"], "built": u["tree"], "merges": u["merges"], "rf": rf,
            "correct": 6 - rf // 2, "trials": trials, "random": rand, "generations": 12, "leaves": {n: tt["leaves"][n] for n in nm}}


ALPHABET = ("1 1 5 5 6 6 5*2 / 4 4 3 3 2*.5 2*.5 2*.5 2*.5 1*2 / 5 5 4*2 3 3 2*2 / 5*.5 5*.5 5 4*2 3 3 2*2 / "
            "1 1 5 5 6 6 5*2 / 4 4 3 3 2 2 1*2 /")
BAA_BAA = ("1 1 5 5 6*.5 6*.5 6*.5 6*.5 5*2 / 4 4 3 3 2 2 1*2 / 5 5*.5 5*.5 4 4 3 3*.5 3*.5 2*2 / "
           "5*.5 5*.5 5*.5 5*.5 4*.5 4*.5 4*.5 4*.5 3 3 2*2 / 1 1 5 5 6*.5 6*.5 6*.5 6*.5 5*2 / 4 4 3 3 2 2 1*2 /")
OTHERS = ["Mary Had a Little Lamb", "Hot Cross Buns", "London Bridge", "Frère Jacques", "Au clair de la lune",
          "Lightly Row (Hänschen klein)", "Alle meine Entchen", "Yankee Doodle"]


def compute_relatives() -> dict:
    mels = {"the Tune": TUNE_MEL, "Alphabet Song": as_mel(M.parse(ALPHABET)), "Baa, Baa, Black Sheep": as_mel(M.parse(BAA_BAA))}
    for t in TUNES:
        if t.name in OTHERS:
            mels[t.name] = as_mel(t)
    nm = list(mels)
    D = O.distances([mels[n] for n in nm])
    u = O.upgma(D, nm)
    first = [mels[n][:7] if n != "Baa, Baa, Black Sheep" else mels[n][:9] for n in nm[:3]]
    c = concat([piano_line(m, beat=0.38) for m in first], gap=0.8, names=["tune", "alphabet", "baa"])
    return {"names": nm, "D": D.round(4).tolist(), "tree": u["tree"], "merges": u["merges"],
            "nearest": {n: nm[int(np.argsort(D[i])[1])] for i, n in enumerate(nm)},
            "starts": {k: float(c.events[k]) for k in ("tune", "alphabet", "baa")},
            "clips": {"three": save("relatives.three", c, detail="the first phrase of the Tune, of the Alphabet Song and of Baa, Baa, Black Sheep; Part 7's piano")}}


FRENCH = {"France", "Canada"}
ENGLISH = {"England", "United States", "Scotland", "Wales", "Britain", "sea shanty", "Stephen Foster, 1848", "Stephen Foster, 1850",
           "James Pierpont, 1857", "Lowell Mason, 1839", "Joseph Brackett, 1848", "George Poulton, 1861",
           "John Stafford Smith, about 1775", "James Murray, 1887"}
GERMAN = {"Germany", "Austria", "Brahms, 1868", "Franz Gruber, 1818", "Beethoven, 1824"}
LIB_LANG = {"C. P. E. Bach": "German", "Weber": "German", "Schubert": "German", "Robert Schumann": "German",
            "Clara Schumann": "German", "Schoenberg": "German", "Webern": "German", "Foster": "English", "Joplin": "English",
            "J. R. Johnson": "English", "Berlin": "English", "Chopin": "Polish", "Verdi": "Italian", "Liliʻuokalani": "Hawaiian"}
MELODY_PART = ("Voice", "Soprano", "Gesang", "1st Violin", "Clarinet", "Violin")


def compute_npvi() -> dict:
    folk = {"French": [], "English": [], "German": []}
    per = []
    for t in TUNES:
        lang = "French" if t.origin in FRENCH else "English" if t.origin in ENGLISH else "German" if t.origin in GERMAN else None
        v = O.npvi(t.beats[:-1])                                   # the last note is held as long as the singer likes
        per.append({"name": t.name, "origin": t.origin, "language": lang, "npvi": v})
        if lang:
            folk[lang].append(v)
    test = O.bootstrap_diff(folk["French"], folk["English"], seed=2003)
    lib = []
    for x in load_library():
        parts = list(x["parts"])
        pick = next((k for k in parts if any(s in k for s in MELODY_PART)), parts[0])
        line = O.melody_line(x["parts"][pick], longest=96)
        lib.append({"composer": x["composer"], "title": x["title"], "kind": x["kind"], "year": x["year"], "part": pick,
                    "language": LIB_LANG[x["composer"]], "npvi": O.npvi(line["ioi"]), "notes": len(line["ioi"]) + 1})
    by_kind = {}
    for r in lib:
        by_kind.setdefault(r["kind"], []).append(r["npvi"])
    by_lang = {}
    for r in lib:
        by_lang.setdefault(r["language"], []).append(r["npvi"])
    return {"folk": {k: {"values": v, "mean": float(np.mean(v)), "n": len(v)} for k, v in folk.items()}, "test": test, "per": per,
            "library": lib, "by_kind": {k: float(np.mean(v)) for k, v in by_kind.items()},
            "by_language": {k: float(np.mean(v)) for k, v in by_lang.items()},
            "examples": {"even": O.npvi([1, 1, 1, 1, 1, 1]), "dotted": O.npvi([1.5, 0.5, 1.5, 0.5, 1.5, 0.5]), "mixed": O.npvi([1, 1, 2, 1, 1, 2])}}


def compute_beat() -> dict:
    period, n = 0.5, 24
    rng = np.random.default_rng(2009)
    off = O.bobbing(n, period, 0.481, locked=False, rng=rng)
    on = O.bobbing(n, period, 0.515, locked=True, rng=rng)
    stats = {"off": O.rayleigh(off["phases"]), "on": O.rayleigh(on["phases"])}
    def take(d):
        parts = []
        P40.drums(parts, "rock", 120, n // 4, gain=-3.0)
        for t in d["times"]:
            if t >= 0:
                parts.append((tap(0.2, 1500.0), t, 1.0))
        return Clip(mix(parts, duration=n * period + 0.8).y, SR)
    c = concat([take(off), take(on)], gap=1.4, names=["first", "second"])
    return {"period": period, "beats": n, "off": off, "on": on, "stats": stats, "answer": "second",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("beat.two", c, detail="a rock beat at 120 a minute with a high wood tap for each simulated head-bob: a dancer keeping its own tempo, then a dancer correcting toward the beat; Part 40's drums")}}


AMUSIA_MEL = [(0, 1), (4, 1), (7, 1), (5, 1), (4, 1), (2, 1), (4, 1), (0, 2)]


def compute_amusia() -> dict:
    a = [[float(p), float(b)] for p, b in AMUSIA_MEL]
    b = [list(x) for x in a]
    b[3][0] = 6.0                                                      # F becomes F sharp: out of the key
    pair1 = concat([piano_line(a, beat=0.42), piano_line(b, beat=0.42)], gap=0.6, names=["a", "b"])
    pair2 = concat([piano_line(a, beat=0.42), piano_line(a, beat=0.42)], gap=0.6, names=["a", "b"])
    c = concat([pair1, pair2], gap=1.6, names=["first", "second"])
    return {"melody": [list(x) for x in AMUSIA_MEL], "changed": 3, "to": 6, "answer": "first",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"]),
                       "first_b": float(c.events["first"] + pair1.events["b"]), "second_b": float(c.events["second"] + pair2.events["b"])},
            "clips": {"pairs": save("amusia.pairs", c, detail="two pairs of eight-note melodies; in one pair the fourth note of the second melody is moved a semitone out of the key; Part 7's piano")}}


def compute_mozart() -> dict:
    out = {}
    for true in (0.0, 0.1):
        r = O.publication_bias(300, true, seed=1993)
        out[f"{true:.1f}"] = {k: v for k, v in r.items() if k != "rows"}
        out[f"{true:.1f}"]["rows"] = [[round(x["d"], 4), round(x["se"], 4), x["published"], x["sig"]] for x in r["rows"]]
    return out


def compute_variation() -> dict:
    t = load("tune47")
    return {"part": 47, "title": "through thirty simulated singers", "seconds": round(t["seconds"], 1),
            "measure": f"{t['notes_in']} notes in, {t['notes_out']} out; {t['kept']} kept exactly; alignment cost {t['distance'][-1]:.2f} a note",
            "clip": "tune.variation47"}


ITEMS = {"hook": compute_hook, "lullaby": compute_lullaby, "universals": compute_universals, "rhythm": compute_rhythm,
         "chains": compute_chains, "sampling": compute_sampling, "tune47": compute_tune47, "family": compute_family,
         "relatives": compute_relatives, "npvi": compute_npvi, "beat": compute_beat, "amusia": compute_amusia,
         "mozart": compute_mozart, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
