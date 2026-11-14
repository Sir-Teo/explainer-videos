"""Precompute everything numerical, and every sound, in Part 27 of *Music, Built* ("The Romantic Century").

    python -m videos.music.music27.compute              # everything missing (several minutes: the pianos and strings)
    python -m videos.music.music27.compute --force library

Numbers are cached in ``.cache/music27/<name>.json``, sounds in ``.cache/music27/audio/``.  The measures are Monochord's
(``explainer/music/monochord/romantic.py``, with Part 15's key profiles); the music is the Library: every dated piece in
the music21 corpus from C. P. E. Bach to Webern, read with all its notes, beside the collections Parts 17 and 23 to 26
read (the trecento, Palestrina, Monteverdi, Bach's chorales, Corelli, Handel, the Classical quartets).  Excerpts are
played by Part 7's piano and bowed string and sung by Part 17's synthetic voice.

Items:
    hook        Der Lindenbaum's piano prelude and first phrase, from the encoding
    keyboards   documented compasses; the register span of the Library's keyboard pieces; every C, then the new ones
    lied        Der Lindenbaum's keys, two bars at a time; the same phrase in E major and in E minor (an ear question)
    mazurka     Chopin's Op. 6 No. 2: the theme in strict time and with a mazurka's uneven beats
    rubato      the Tune's opening strict, under a phrase arch, and with the melody alone bending (Mozart's description)
    idee        the Tune's head as an idée fixe: plain, as a waltz, in minor, as a march, augmented
    tristan     a plain cadence, then the Tristan chord and its resolution; keys that contain each chord
    library     chromaticism and tonal clarity from 1370 to 1924; the trend from 1680 to 1900 with a bootstrap interval;
                songs against instrumental music; two quartet passages (an ear question: which is later?)
    nations     Lift Every Voice and Sing (1900), its first eight bars sung; the Maple Leaf Rag (1899), sixteen bars
    orchestra   the winds, brass and timpani that five symphonies call for
    tune        Variation 27: a nocturne, a Lied, a leitmotif transformed
    variation   the Variations ledger, row 27
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import baroque as B
from explainer.music.monochord import chorales as CHO
from explainer.music.monochord import key as K
from explainer.music.monochord import melody as M
from explainer.music.monochord import renaissance as RN
from explainer.music.monochord import romantic as R
from explainer.music.monochord import trecento as TR
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music27")
CLIPS = ClipStore("music27")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
VIOLIN = STR.violin_body()
C4 = 261.6255653005986
_V: dict = {}
_P: dict = {}
BAR = 72                                                   # ticks in a 3/4 bar


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def bowed(m: float, seconds: float) -> Clip:
    key = (round(m, 2), round(min(seconds, 2.6), 2))
    if key not in _V:
        y = VIOLIN.play(STR.bowed_note(hz(m), max(min(seconds, 2.6), 0.1)))
        _V[key] = Clip(np.asarray(y, dtype=float)).fade(0.008, 0.05).at_level(LEVEL)
    return _V[key]


def piano(m: float, seconds: float, velocity: float = 1.2) -> Clip:
    seconds = round(min(max(seconds, 0.12), 3.0), 2)
    key = (round(m, 2), seconds, round(velocity, 2))
    if key not in _P:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4),
                                  velocity=velocity, seconds=seconds + 0.3))
        _P[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _P[key]


def place(lines, inst, unit: float, gains=None, tail: float = 1.0, times=None) -> Clip:
    """Lines of (key number, beat, beats); ``times`` optionally maps a beat to seconds (rubato)."""
    gains = gains or [0.0] * len(lines)
    tm = times or (lambda b: b * unit)
    placed, end = [], 0.0
    for ln, g in zip(lines, gains):
        for p, a, d in ln:
            t0, t1 = tm(a), tm(a + d)
            placed.append((inst(p, (t1 - t0) * 1.02), t0, g))
            end = max(end, t1)
    return Clip(mix(placed, duration=end + tail).y, SR)


def voice(notes, unit: float, part: str = "tenor", vowel: str = "a", times=None) -> Clip:
    tm = times or (lambda b: b * unit)
    y = CH.sing([(m, tm(a), tm(a + d) - tm(a)) for m, a, d in notes], part, vowel)
    return Clip(y / max(np.abs(y).max(), 1e-9) * 0.5, SR).fade(0.02, 0.2)


def rows(v):
    return [[float(p), float(a), float(d)] for p, a, d in v]


def piece(word: str) -> dict:
    return next(r for r in R.load_library() if word in r["path"])


def cut(notes, lo: int, hi: int):
    """Notes with onsets in [lo, hi) ticks, as (key number, beat from lo, beats)."""
    return [(p, (o - lo) / 24.0, min(d, hi - o) / 24.0) for p, o, d in notes if lo <= o < hi]


def tune_line(base: int = 72, n: int = 14):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


def lindenbaum_clip(lo: int, hi: int, unit: float, voice_shift: int = -12):
    L = piece("Linden")
    v = cut(L["parts"]["Voice"], lo, hi)
    pno = cut(L["parts"]["Piano"], lo, hi)
    cp = place([pno], lambda m, s: piano(m, s, 0.9), unit, gains=[-4.0], tail=1.2)
    parts = [(cp, 0.0, 0.0)]
    if v:
        cv = voice([(p + voice_shift, a, d) for p, a, d in v], unit, "tenor", "a")
        parts.append((cv.at_level(LEVEL), 0.0, 0.0))
    c = Clip(mix(parts, duration=max(cp.duration, parts[-1][0].duration)).y, SR)
    return c, v, pno


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    unit = 0.48
    c, v, pno = lindenbaum_clip(0, 15 * BAR, unit)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["linden"])
    return {"voice": rows(v), "piano": rows(pno), "unit": unit, "voice_start": float(min(a for _, a, _ in v)),
            "clips": {"linden": save("hook.lindenbaum", s_, kind="synthesized", level=None,
                                     detail="Schubert, Der Lindenbaum (Winterreise, 1827), bars 1-15 from the encoding: Part 7's piano and a synthetic tenor")}}


def compute_keyboards() -> dict:
    lib = R.load_library()
    spans = [{"year": r["year"], "composer": r["composer"], "title": r["title"], "span": R.register_span(R.all_notes(r["parts"])),
              "low": min(p for p, _, _ in R.all_notes(r["parts"])), "high": max(p for p, _, _ in R.all_notes(r["parts"]))}
             for r in lib if r["kind"] == "keyboard"]
    cs_old = [36, 48, 60, 72, 84]
    cs_new = [24, 96, 108]
    a = Clip(mix([(piano(m, 1.8, 0.8), 1.25 * i, 0.0) for i, m in enumerate(cs_old)], duration=1.25 * len(cs_old) + 1.0).y, SR)
    b = Clip(mix([(piano(m, 2.0, 0.8), 1.75 * i, 0.0) for i, m in enumerate(cs_new)], duration=1.75 * len(cs_new) + 1.0).y, SR)
    s_ = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["old", "new"])
    return {"keyboards": [{"year": y, "name": n, "low": lo, "high": hi, "keys": hi - lo + 1} for y, n, lo, hi in R.KEYBOARDS],
            "spans": spans, "cs_old": cs_old, "cs_new": cs_new, "starts": {k: float(s_.events[k]) for k in ("old", "new")},
            "clips": {"cs": save("keyboards.cs", s_, detail="every C on a 1780s fortepiano's five octaves (C2 to C6), then the Cs added by 1880 (C1, C7, C8), Part 7's piano")}}


def compute_lied() -> dict:
    L = piece("Linden")
    notes = R.all_notes(L["parts"])
    m = R.measure(notes, window=6.0, hop=6.0)
    unit = 0.48
    starts = {}
    out = {}
    clips = []
    for k, (lo_bar, hi_bar) in {"A": (27, 31), "B": (7, 11)}.items():          # A: the minor stanza; B: the major
        lo = min(o for _, o, _ in L["parts"]["Voice"] if o >= lo_bar * BAR)
        c, v, pno = lindenbaum_clip(lo, hi_bar * BAR, unit)
        clips.append(c.at_level(LEVEL))
        out[k] = {"voice": rows(v), "piano": rows(pno), "bar": lo_bar}
    s_ = concat(clips, gap=1.4, names=["A", "B"])
    keys = [{"bar": k["start"] / 3.0, "key": k["key"]} for k in m["keys"]]
    nb = int(np.ceil(max(o + d for _, o, d in notes) / (2 * BAR)))
    share = {"voice": [0] * nb, "piano": [0] * nb}
    for part, key_ in (("Voice", "voice"), ("Piano", "piano")):
        for _, o, _ in L["parts"][part]:
            share[key_][min(o // (2 * BAR), nb - 1)] += 1
    share["n_voice"] = len(L["parts"]["Voice"])
    share["n_piano"] = len(L["parts"]["Piano"])
    return {"share": share, "keys": keys, "bars": max(o + d for _, o, d in notes) / BAR, "A": out["A"], "B": out["B"], "unit": unit, "answer": "A",
            "starts": {k: float(s_.events[k]) for k in "AB"},
            "minor_bars": [k["bar"] for k in keys if tuple(k["key"]) == (4, "minor")],
            "clips": {"quiz": save("lied.quiz", s_, kind="synthesized", level=None,
                                   detail="Der Lindenbaum: bars 27-30 (E minor), then bars 7-10 (E major), the same tune, from the encoding: piano and a synthetic tenor")}}


def compute_mazurka() -> dict:
    c = piece("chopin")
    lo, hi = 8 * BAR, 16 * BAR
    parts = [cut(v, lo, hi) for v in c["parts"].values()]
    unit = 0.36
    strict = place(parts, lambda m, s: piano(m, s, 1.0), unit, gains=[-3.0, 0.0])
    warp = lambda b: unit * float(R.mazurka_beats([b])[0])  # noqa: E731
    bent = place(parts, lambda m, s: piano(m, s, 1.0), unit, gains=[-3.0, 0.0], times=warp)
    s_ = concat([strict.at_level(LEVEL), bent.at_level(LEVEL)], gap=1.2, names=["strict", "mazurka"])
    beats = R.mazurka_beats(np.arange(0, 25)) - np.arange(0, 25)
    return {"parts": [rows(p) for p in parts], "unit": unit, "starts": {k: float(s_.events[k]) for k in ("strict", "mazurka")},
            "beat_lengths": [0.85, 1.2, 0.95], "shift": [float(x) for x in beats],
            "clips": {"two": save("mazurka.two", s_, level=None, detail="Chopin, Mazurka Op. 6 No. 2 (1830), bars 9-16 from the encoding: in strict time, then with a short first beat and a long second, Part 7's piano")}}


ACC = [(48, 0, 2), (55, 0, 2), (64, 0, 2), (48, 2, 2), (55, 2, 2), (64, 2, 2), (53, 4, 2), (57, 4, 2), (65, 4, 2), (48, 6, 2), (55, 6, 2), (64, 6, 2),
       (43, 8, 2), (53, 8, 2), (59, 8, 2), (48, 10, 2), (55, 10, 2), (64, 10, 2), (43, 12, 2), (53, 12, 2), (59, 12, 2), (48, 14, 2), (55, 14, 2), (64, 14, 2)]


def compute_rubato() -> dict:
    mel = tune_line()
    unit = 0.5
    arch = lambda b: unit * float(R.phrase_arch([b], 8.0, depth=0.3)[0])  # noqa: E731

    def melody_only(b):                                   # the melody bends within each bar of two beats; the bar lines do not
        bar = np.floor(b / 2.0) * 2.0
        u = (b - bar) / 2.0
        return unit * (bar + 2.0 * (u + 0.18 * np.sin(np.pi * u)))
    acc = [(p, a, d) for p, a, d in ACC]
    clips = []
    for name, tm_m, tm_a in (("strict", None, None), ("arch", arch, arch), ("melody", melody_only, None)):
        cm = place([mel], lambda m, s: piano(m, s, 1.25), unit, times=tm_m)
        ca = place([acc], lambda m, s: piano(m, s, 0.8), unit, gains=[-5.0], times=tm_a)
        clips.append(Clip(mix([(cm, 0.0, 0.0), (ca, 0.0, 0.0)], duration=max(cm.duration, ca.duration)).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.2, names=["strict", "arch", "melody"])
    grid = np.linspace(0, 16, 161)
    tempo_arch = np.gradient(grid) / np.gradient(R.phrase_arch(grid, 8.0, depth=0.3))
    return {"melody": rows(mel), "acc": rows(acc), "unit": unit, "starts": {k: float(s_.events[k]) for k in ("strict", "arch", "melody")},
            "grid": grid.tolist(), "tempo_arch": tempo_arch.tolist(),
            "onsets": {"strict": [a for _, a, _ in mel], "arch": [float(R.phrase_arch([a], 8.0, depth=0.3)[0]) for _, a, _ in mel],
                       "melody": [float(melody_only(a) / unit) for _, a, _ in mel]},
            "clips": {"three": save("rubato.three", s_, level=None, detail="the Tune's first two phrases on Part 7's piano: strict, under a phrase arch (both hands), and with only the melody bending inside each bar")}}


def compute_idee() -> dict:
    head = tune_line(n=7)
    kinds = ["original", "waltz", "minor", "march", "augmented"]
    acc = {"original": [(48, 0, 4), (55, 0, 4), (64, 0, 4), (53, 4, 2), (57, 4, 2), (48, 6, 2), (55, 6, 2)],
           "waltz": [(48, 0, 1), (55, 1, 1), (64, 1, 1), (55, 2, 1), (64, 2, 1), (48, 3, 1), (55, 4, 1), (64, 4, 1), (55, 5, 1), (64, 5, 1),
                     (53, 6, 1), (57, 7, 1), (65, 7, 1), (57, 8, 1), (65, 8, 1), (48, 9, 1), (55, 10, 1), (64, 10, 1)],
           "minor": [(48, 0, 4), (55, 0, 4), (63, 0, 4), (53, 4, 2), (56, 4, 2), (48, 6, 2), (55, 6, 2)],
           "march": [(36, 0, 1), (43, 1, 1), (36, 2, 1), (43, 3, 1), (41, 4, 1), (36, 5, 1), (43, 6, 1), (36, 7, 1)],
           "augmented": [(36, 0, 8), (43, 0, 8), (52, 0, 8), (41, 8, 4), (45, 8, 4), (36, 12, 4), (43, 12, 4)]}
    units = {"original": 0.42, "waltz": 0.26, "minor": 0.5, "march": 0.34, "augmented": 0.4}
    lines, clips = {}, []
    for k in kinds:
        ln = R.transform(head, "minor" if k == "minor" else k)
        if k == "minor":
            ln = [(p, a, d * 1.0) for p, a, d in ln]
        lines[k] = ln
        cm = place([ln], bowed, units[k])
        ca = place([acc[k]], lambda m, s: piano(m, s, 0.9), units[k], gains=[-5.0])
        clips.append(Clip(mix([(cm, 0.0, 0.0), (ca, 0.0, 0.0)], duration=max(cm.duration, ca.duration)).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=kinds)
    return {"kinds": kinds, "lines": {k: rows(v) for k, v in lines.items()}, "acc": {k: rows(v) for k, v in acc.items()}, "units": units,
            "starts": {k: float(s_.events[k]) for k in kinds},
            "clips": {"five": save("idee.five", s_, level=None, detail="the Tune's first phrase as an idée fixe: plain, as a waltz, in minor, as a march, augmented; Part 7's bowed string over its piano")}}


def compute_tristan() -> dict:
    plain = [[57, 60, 64, 69], [50, 57, 62, 65], [52, 56, 62, 71], [45, 57, 60, 64]]          # A minor: i, iv, V7, i
    tris = [[53, 59, 63, 68], [53, 59, 63, 69], [52, 56, 62, 70], [52, 56, 62, 71]]           # the chord, the line G#-A-A#-B, E7
    unit = 0.62
    lines_p = [[(ch[j], 2 * i, 2) for i, ch in enumerate(plain)] for j in range(4)]
    lines_t = []
    for j in range(4):
        ln = []
        for i, ch in enumerate(tris):
            if ln and ln[-1][0] == ch[j] and ln[-1][1] + ln[-1][2] == 2 * i:
                ln[-1] = (ch[j], ln[-1][1], ln[-1][2] + 2)
            else:
                ln.append((ch[j], 2 * i, 2))
        lines_t.append(ln)
    cp = place(lines_p, bowed, unit, gains=[0, -1, -2, -1])
    ct = place(lines_t, bowed, unit, gains=[0, -1, -2, 0])
    s_ = concat([cp.at_level(LEVEL), ct.at_level(LEVEL)], gap=1.4, names=["plain", "tristan"])

    def fits(ch):
        pcs = {p % 12 for p in ch}
        return [list(k) for k in K.KEYS if all(R.in_key(pc, k) for pc in pcs)]
    return {"plain": plain, "tristan": tris, "unit": unit, "starts": {k: float(s_.events[k]) for k in ("plain", "tristan")},
            "fits_plain": [len(fits(c)) for c in plain], "fits_tristan": [len(fits(c)) for c in tris],
            "tristan_keys": fits(tris[0]),
            "clips": {"two": save("tristan.two", s_, level=None, detail="A minor: i, iv, V7, i; then the Tristan chord (F, B, D sharp, G sharp) with the rising line G sharp, A, A sharp, B, resolving to E7, Part 7's bowed string")}}


QUARTET_YEARS = {"haydn/opus1no1": 1762, "mozart/k80": 1770, "mozart/k155": 1772, "mozart/k156": 1772, "mozart/k458": 1784, "haydn/opus74no1": 1793,
                 "beethoven/opus18": 1800, "beethoven/opus59": 1806, "beethoven/opus74": 1809, "beethoven/opus132": 1825, "beethoven/opus133": 1825}
MONTEVERDI_YEARS = {"3": 1592, "4": 1603, "5": 1605}


def _group(name, label_, year, measures, kind):
    c = [m["chromaticism"] for m in measures if m["windows"]]
    k = [m["clarity"] for m in measures if m["windows"]]
    return {"group": name, "label": label_, "year": year, "n": len(c), "kind": kind, "chromaticism": float(np.mean(c)), "clarity": float(np.mean(k)),
            "each": [[float(a), float(b)] for a, b in zip(c, k)]}


def compute_library() -> dict:
    pts = []
    tr = TR.load()
    pts.append(_group("trecento", r"the trecento", 1370, [R.measure(R.all_notes(p.voices)) for p in tr], "vocal"))
    rn = RN.load()
    pal = [p for p in rn if "alestrina" in p.composer]
    pal = pal[:: max(1, len(pal) // 240)]
    pts.append(_group("palestrina", r"Palestrina", 1580, [R.measure(R.all_notes(p.voices)) for p in pal], "vocal"))
    mon = defaultdict(list)
    for p in rn:
        if "onteverdi" in p.composer:
            book = p.name.split(".")[1] if "." in p.name else "4"
            mon[book].append(R.measure(R.all_notes(p.voices)))
    for book, ms in sorted(mon.items()):
        pts.append(_group(f"monteverdi{book}", rf"Monteverdi, Book {book}", MONTEVERDI_YEARS.get(book, 1600), ms, "vocal"))
    b = B.load()
    pts.append(_group("corelli", r"Corelli", 1689, [R.measure(R.all_notes(b["corelli"]))], "instrumental"))
    pts.append(_group("handel", r"Handel", 1711, [R.measure(R.all_notes(b["handel"]))], "song"))
    ch = CHO.load()
    pts.append(_group("bach", r"Bach's chorales", 1730, [R.measure(R.all_notes([[n[:3] for n in v] for v in c.voices])) for c in ch], "vocal"))
    qs = defaultdict(list)
    for q in B.load_quartets():
        key = next((k for k in QUARTET_YEARS if f"{q['composer']}/{q['name']}".startswith(k)), None)
        if key:
            qs[key].append(R.measure(R.all_notes(q["voices"])))
    for key, ms in qs.items():
        comp, op = key.split("/")
        pts.append(_group(key, rf"{comp.title()}, {op.replace('opus', 'Op. ').replace('no', ' No. ').replace('k', 'K. ')}", QUARTET_YEARS[key], ms, "quartet"))
    for r in R.load_library():
        pts.append(_group(r["path"], rf"{r['composer']}, {r['title']}", r["year"], [R.measure(R.all_notes(r["parts"]))], r["kind"]))
    pts.sort(key=lambda p: p["year"])

    # the trend, 1680-1900: ordinary least squares on the points, a bootstrap over points for the interval
    sel = [p for p in pts if 1680 <= p["year"] <= 1900]
    x = np.array([p["year"] for p in sel], float)
    y = np.array([p["chromaticism"] for p in sel])
    z = np.array([p["clarity"] for p in sel])

    def slope(xx, yy):
        return float(np.polyfit(xx, yy, 1)[0] * 100)
    rng = np.random.default_rng(27)
    boots_c, boots_k = [], []
    for _ in range(4000):
        i = rng.integers(0, len(x), len(x))
        if np.ptp(x[i]) > 0:
            boots_c.append(slope(x[i], y[i]))
            boots_k.append(slope(x[i], z[i]))
    ins = np.array([p["kind"] not in ("song", "vocal") for p in sel])
    boots_i = []
    for _ in range(4000):
        i = rng.choice(np.flatnonzero(ins), ins.sum())
        if np.ptp(x[i]) > 0:
            boots_i.append(slope(x[i], y[i]))
    after = [p for p in pts if p["year"] > 1900 and p["group"].split("/")[0] in ("schoenberg", "webern")]
    songs = [p["chromaticism"] for p in sel if p["year"] >= 1800 and p["kind"] == "song"]
    inst = [p["chromaticism"] for p in sel if p["year"] >= 1800 and p["kind"] != "song"]

    # an ear question: a Haydn passage and a Schumann passage, four bars each
    hq = next(q for q in B.load_quartets() if q["name"] == "opus74no1/movement1")
    sq = piece("opus41no1/movement1")
    unit = 0.3

    def best(voices, bar, sign):
        n = R.all_notes(voices)
        end = max(o + d for _, o, d in n)
        cands = []
        for s in range(8 * bar, end - 4 * bar, bar):
            w = [x_ for x_ in n if s <= x_[1] < s + 4 * bar]
            if len(w) >= 20:
                cands.append((sign * R.measure([(p, o - s, d) for p, o, d in w], window=4 * bar / 24, hop=4 * bar / 24)["chromaticism"], s))
        return sorted(cands)[len(cands) // 2 if sign > 0 else 0][1]
    hb = 96
    s_h = best(hq["voices"], hb, 1)
    sv = list(sq["parts"].values())
    sb = 48
    s_s = best({k: v for k, v in sq["parts"].items()}, sb, -1)
    exA = [cut(v, s_s, s_s + 8 * sb) for v in sv]
    exB = [cut(v, s_h, s_h + 4 * hb) for v in hq["voices"]]
    cA = place(exA, bowed, unit, gains=[0, -1, -2, -1])
    cB = place(exB, bowed, unit, gains=[0, -1, -2, -1])
    s_ = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.4, names=["A", "B"])
    mA = R.measure(R.all_notes([[(p, int(a * 24), int(d * 24)) for p, a, d in v] for v in exA]), window=16, hop=16)
    mB = R.measure(R.all_notes([[(p, int(a * 24), int(d * 24)) for p, a, d in v] for v in exB]), window=16, hop=16)
    return {"points": pts, "slope_c": slope(x, y), "slope_k": slope(x, z), "ci_c": [float(np.percentile(boots_c, 2.5)), float(np.percentile(boots_c, 97.5))],
            "ci_k": [float(np.percentile(boots_k, 2.5)), float(np.percentile(boots_k, 97.5))], "n_trend": len(sel),
            "slope_i": slope(x[ins], y[ins]), "ci_i": [float(np.percentile(boots_i, 2.5)), float(np.percentile(boots_i, 97.5))], "n_i": int(ins.sum()),
            "after": [{"label": p["label"], "chromaticism": p["chromaticism"], "clarity": p["clarity"]} for p in after],
            "songs": float(np.mean(songs)), "instrumental": float(np.mean(inst)), "n_songs": len(songs), "n_inst": len(inst),
            "quiz": {"A": [rows(v) for v in exA], "B": [rows(v) for v in exB], "unit": unit, "answer": "A",
                     "A_bar": s_s // sb + 1, "B_bar": s_h // hb + 1, "A_chrom": mA["chromaticism"], "B_chrom": mB["chromaticism"]},
            "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("library.quiz", s_, level=None, detail="two string-quartet passages from the encodings: Schumann, Op. 41 No. 1 (1842), and Haydn, Op. 74 No. 1 (1793), first movements, Part 7's bowed string")}}


def satb(voices, unit: float) -> Clip:
    outs = []
    for v, part, vowel in zip(voices, ("soprano", "alto", "tenor", "bass"), ("a", "O", "a", "O")):
        outs.append(CH.sing([(m, a * unit, d * unit) for m, a, d in v], part, vowel))
    n = max(len(y) for y in outs) + int(0.6 * SR)
    out = np.zeros(n)
    for y in outs:
        out[: len(y)] += y
    return Clip(out / max(np.abs(out).max(), 1e-9) * 0.5, SR).fade(0.02, 0.3)


def compute_nations() -> dict:
    lv = piece("lift_every")
    voices = [cut(lv["parts"][k], 0, 8 * BAR) for k in ("Soprano", "Alto", "Tenor", "Bass")]
    c1 = satb(voices, 0.5)
    rag = piece("joplin")
    rb = 48
    notes = cut(rag["parts"]["Piano"], 0, 16 * rb)
    split = 58
    rh = [n for n in notes if n[0] >= split]
    lh = [n for n in notes if n[0] < split]
    c2 = place([rh, lh], lambda m, s: piano(m, s, 1.1), 0.3, gains=[0.0, -3.0])
    s_ = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=1.4, names=["lift", "rag"])
    onbeat = sum(1 for p, a, d in rh if abs(a - round(a)) < 1e-6)
    return {"lift": [rows(v) for v in voices], "rag": [rows(rh), rows(lh)], "units": {"lift": 0.5, "rag": 0.3},
            "starts": {k: float(s_.events[k]) for k in ("lift", "rag")}, "rh_onbeat": onbeat, "rh_notes": len(rh),
            "lh_onbeat": sum(1 for p, a, d in lh if abs(a - round(a)) < 1e-6), "lh_notes": len(lh),
            "clips": {"two": save("nations.two", s_, kind="synthesized", level=None,
                                  detail="J. Rosamond Johnson, Lift Every Voice and Sing (1900), bars 1-8, Part 17's synthetic choir; Joplin, Maple Leaf Rag (1899), bars 1-16, Part 7's piano; from the encodings")}}


def compute_orchestra() -> dict:
    return {"rows": [{"year": y, "name": n, "parts": spec, "players": R.winds(spec)} for y, n, spec in R.ORCHESTRAS]}


def compute_tune() -> dict:
    mel = tune_line()
    unit = 0.5
    # the nocturne: the melody ornamented, a wide left hand in triplet eighths, a phrase arch
    noct = []
    for p, a, d in mel:
        if d >= 2:
            noct += [(p + 2, a, 0.25), (p, a + 0.25, 0.25), (p - 1, a + 0.5, 0.25), (p, a + 0.75, d - 0.75)]
        else:
            noct.append((p, a, d))
    bassline = {0: 36, 2: 36, 4: 41, 6: 36, 8: 31, 10: 36, 12: 31, 14: 36}
    lh = []
    for b0, root in bassline.items():
        third = 4 if root in (36, 41) else 4
        fig = [root, root + 7, root + 12 + third, root + 19, root + 12 + third, root + 7]
        if root == 31:
            fig = [31, 38, 47, 53, 47, 38]
        lh += [(m, b0 + k / 3.0, 1 / 3.0) for k, m in enumerate(fig)]
    arch = lambda b: unit * 1.15 * float(R.phrase_arch([b], 8.0, depth=0.22)[0])  # noqa: E731
    cn = Clip(mix([(place([noct], lambda m, s: piano(m, s, 1.15), unit, times=arch), 0.0, 0.0),
                   (place([lh], lambda m, s: piano(m, s, 0.75), unit, gains=[-6.0], times=arch), 0.0, 0.0)], duration=16 * unit * 1.2 + 1.5).y, SR)
    # the Lied: the voice sings the Tune; the piano's right hand murmurs triplets as in Der Lindenbaum
    lu = 0.55
    harm = ["I", "I", "IV", "I", "V", "I", "V", "I"]
    ch = {"I": (48, [60, 64, 67]), "IV": (53, [60, 65, 69]), "V": (43, [59, 62, 67])}
    rh, lb = [], []
    for k, hname in enumerate(harm):
        bass, tri = ch[hname]
        lb.append((bass, 2 * k, 2))
        for beat in range(2):
            for j, m in enumerate([tri[0], tri[1], tri[2]]):
                rh.append((m, 2 * k + beat + j / 3.0, 1 / 3.0))
    cv = voice([(p - 12, a, d) for p, a, d in mel], lu, "tenor", "a")
    cp = place([rh, lb], lambda m, s: piano(m, s, 0.8), lu, gains=[-8.0, -4.0])
    cl = Clip(mix([(cp, 0.0, 0.0), (cv.at_level(LEVEL), 0.0, 0.0)], duration=max(cp.duration, cv.duration)).y, SR)
    # the leitmotif transformed: the head in minor and augmented, low, over darkening chromatic chords, then home
    head = R.transform(R.transform(tune_line(base=60, n=7), "minor"), "augmented")
    chords = [(0, [48, 55, 63]), (4, [47, 53, 62]), (8, [44, 53, 60]), (12, [43, 50, 59, 65]), (16, [48, 52, 55, 64])]
    cl_lines = [[(m, t, 4) for t, c_ in chords for m in c_[i:i + 1]] for i in range(4)]
    head = head + [(60, 14, 4)]
    cm = place([head], bowed, 0.42)
    cc = place(cl_lines, lambda m, s: piano(m, s, 0.7), 0.42, gains=[-6.0] * 4)
    ct = Clip(mix([(cm, 0.0, 0.0), (cc, 0.0, 0.0)], duration=max(cm.duration, cc.duration)).y, SR)
    s_ = concat([cn.at_level(LEVEL), cl.at_level(LEVEL), ct.at_level(LEVEL)], gap=1.2, names=["nocturne", "lied", "motif"])
    return {"nocturne": rows(noct), "lh": rows(lh), "lied": rows(mel), "rh": rows(rh), "lb": rows(lb), "motif": rows(head),
            "chords": [[t, c_] for t, c_ in chords], "units": {"nocturne": unit * 1.15, "lied": lu, "motif": 0.42},
            "starts": {k: float(s_.events[k]) for k in ("nocturne", "lied", "motif")}, "seconds": s_.duration,
            "notes": {"nocturne": len(noct), "left_hand": len(lh), "lied_piano": len(rh) + len(lb), "motif": len(head)},
            "clips": {"variation": save("tune.variation27", s_, kind="synthesized", level=None,
                                        detail="the Tune as a nocturne (Part 7's piano, a phrase arch), as a Lied (a synthetic tenor over the piano), and as a leitmotif transformed (Part 7's bowed string and piano)")}}


def compute_variation() -> dict:
    t = load("tune")
    n = t["notes"]
    return {"part": 27, "title": r"as a nocturne, as a Lied, and as a leitmotif transformed", "seconds": round(t["seconds"], 2),
            "measure": rf"nocturne: {n['nocturne']} melody notes over {n['left_hand']} in the left hand; the motif augmented to {n['motif']} long notes",
            "clip": "tune.variation27"}


ITEMS = {"hook": compute_hook, "keyboards": compute_keyboards, "lied": compute_lied, "mazurka": compute_mazurka, "rubato": compute_rubato,
         "idee": compute_idee, "tristan": compute_tristan, "library": compute_library, "nations": compute_nations, "orchestra": compute_orchestra, "tune": compute_tune,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
