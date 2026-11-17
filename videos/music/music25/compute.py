"""Precompute everything numerical, and every sound, in Part 25 of *Music, Built* ("The Baroque").

    python -m videos.music.music25.compute              # everything missing (a few minutes: the bowed strings)
    python -m videos.music.music25.compute --force corelli

Numbers are cached in ``.cache/music25/<name>.json``, sounds in ``.cache/music25/audio/``.  The tools are Monochord's
(``explainer/music/monochord/baroque.py``, Part 10's figured-bass realizer, Part 6's temperaments); the pieces are
Corelli's Op. 3 No. 1 Grave and Handel's *Lascia ch'io pianga* from the music21 corpus's encodings, with Part 24's
Palestrina and Part 17's Bach for the census of modes and keys.  Harpsichord: Part 1's string plucked near its end on
Part 7's soundboard; violins: Part 7's bowed string on its violin body (both physical models); organ and continuo
chords: additive organ tones; voices: Part 17's choir (synthesized).  Published findings are cited in the README.

Items:
    hook        Galilei's strings: weights 2:1 and 4:1 (an ear question: which pair is an octave?)
    monody      a recitative over a held bass, then an aria over a moving one (ours)
    corelli     the Grave of Corelli's Op. 3 No. 1: as written; its bass figured from the violins and realized again
    modes       Palestrina's modes against Bach's keys
    ritornello  a concerto movement built from returns (ours), and the finder run on it
    ornaments   a plain line, then ornamented; straight eighths, then notes inégales
    dances      the Tune in four dance rhythms
    keys        major thirds of every key in meantone, Werckmeister III and equal temperament; a cadence heard in two keys
    handel      Lascia ch'io pianga, the opening
    tune        Variation 25: the Tune as a French overture and as a chaconne with an ornamented reprise
    variation   the Variations ledger, row 25
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import baroque as B
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import melody as M
from explainer.music.monochord import renaissance as R
from explainer.music.monochord import tuning as TU
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.instruments.plucked import plucked as pluck
from explainer.music.monochord.partkit import organ_tone, saver, signoff
from explainer.music.monochord.score import Pitch
from explainer.music.monochord.score import figured as FIG

CACHE = Cache("music25")
CLIPS = ClipStore("music25")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
VIOLIN = STR.violin_body()
_H: dict = {}
_V: dict = {}


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def harpsichord(m: float, seconds: float) -> Clip:
    key = (round(m, 3), round(seconds, 2))
    if key not in _H:
        y = BOARD.play(pluck(hz(m), seconds=seconds + 0.4, beta=0.11))
        _H[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.12).at_level(LEVEL)
    return _H[key]


def violin(m: float, seconds: float) -> Clip:
    key = (round(m, 3), round(seconds, 2))
    if key not in _V:
        y = VIOLIN.play(STR.bowed_note(hz(m), max(seconds, 0.12)))
        _V[key] = Clip(np.asarray(y, dtype=float)).fade(0.01, 0.06).at_level(LEVEL)
    return _V[key]


def organ(m: float, seconds: float) -> Clip:
    return Clip(organ_tone(hz(m), seconds, partials=6, rolloff=0.75)).fade(0.02, 0.08).at_level(LEVEL)


def place(lines, instruments, unit: float, gains=None, tail: float = 1.0) -> Clip:
    """Lines of (key number, onset, duration) in units of ``unit`` seconds, each on its instrument."""
    gains = gains or [0.0] * len(lines)
    placed = []
    end = 0.0
    for ln, inst, g in zip(lines, instruments, gains):
        for p, a, d in ln:
            placed.append((inst(p, d * unit * 1.02), a * unit, g))
            end = max(end, (a + d) * unit)
    return Clip(mix(placed, duration=end + tail).y, SR)


def sing(notes, unit: float, part: str = "tenor", vowel: str = "a") -> Clip:
    y = CH.sing([(m, a * unit, d * unit) for m, a, d in notes], part, vowel)
    return Clip(y / max(np.abs(y).max(), 1e-9) * 0.5, SR).fade(0.02, 0.2)


def rows(v):
    return [[float(p), float(a), float(d)] for p, a, d in v]


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    f1 = 196.0
    pairs = {"A": 2.0, "B": 4.0}                       # weight ratios: A is the legend's 2:1, B Galilei's 4:1
    clips = []
    out = {}
    for k, w in pairs.items():
        f2 = f1 * np.sqrt(w)
        a = Clip(BOARD.play(pluck(f1, seconds=2.2, beta=0.11))).fade(0.001, 0.2).at_level(LEVEL)
        b = Clip(BOARD.play(pluck(f2, seconds=2.2, beta=0.11))).fade(0.001, 0.2).at_level(LEVEL)
        both = mix([(a, 0.0, 0.0), (b, 1.3, 0.0), (a, 2.8, -2.0), (b, 2.8, -2.0)], duration=5.6)
        clips.append(Clip(both.y, SR).at_level(LEVEL))
        out[k] = {"weights": w, "ratio": float(np.sqrt(w)), "cents": float(1200 * np.log2(np.sqrt(w)))}
    s = concat(clips, gap=1.2, names=["A", "B"])
    tensions = [9.8 * kg for kg in (1, 2, 4)]
    return {"pairs": out, "starts": {k: float(s.events[k]) for k in "AB"}, "answer": "B",
            "mersenne": [{"kg": kg, "hz": B.string_hz(9.8 * kg)} for kg in (1, 2, 4, 9)],
            "clips": {"weights": save("hook.weights", s, level=None, detail="two equal strings under weights in the ratio 2:1, then 4:1, plucked one after the other and together")}}


def compute_monody() -> dict:
    # a recitative: speech-like repeated notes over a held chord, a cadence; then an aria: a shaped tune over a walking bass
    rec = [(67, 0, 0.5), (67, 0.5, 0.5), (67, 1, 0.5), (69, 1.5, 0.5), (67, 2, 1), (67, 3, 0.5), (65, 3.5, 0.5), (64, 4, 0.5), (64, 4.5, 0.5),
           (64, 5, 0.5), (62, 5.5, 0.5), (60, 6, 1.5), (67, 8, 0.5), (67, 8.5, 0.5), (70, 9, 1), (69, 10, 0.5), (67, 10.5, 0.5), (65, 11, 1), (64, 12, 2)]
    rec_bass = [(48, 0, 6), (43, 6, 2), (45, 8, 3), (43, 11, 1), (48, 12, 2)]
    aria = [(72, 0, 1), (71, 1, 0.5), (72, 1.5, 0.5), (74, 2, 1), (76, 3, 1), (77, 4, 1.5), (76, 5.5, 0.5), (74, 6, 1), (72, 7, 1),
            (71, 8, 1), (72, 9, 0.5), (74, 9.5, 0.5), (76, 10, 1), (74, 11, 1), (72, 12, 2)]
    aria_bass = [(48, 0, 1), (52, 1, 1), (55, 2, 1), (52, 3, 1), (53, 4, 1), (57, 5, 1), (55, 6, 1), (52, 7, 1), (50, 8, 1), (55, 9, 1), (48, 10, 1), (55, 11, 1), (48, 12, 2)]
    unit_r, unit_a = 0.42, 0.42
    c1 = mix([(sing(rec, unit_r, "tenor"), 0.0, 0.0), (place([rec_bass], [harpsichord], unit_r), 0.0, -4.0)], duration=14 * unit_r + 1.2)
    c2 = mix([(sing(aria, unit_a, "soprano"), 0.0, 0.0), (place([aria_bass], [harpsichord], unit_a), 0.0, -4.0)], duration=14 * unit_a + 1.2)
    s = concat([Clip(c1.y, SR).at_level(LEVEL), Clip(c2.y, SR).at_level(LEVEL)], gap=1.2, names=["recitative", "aria"])
    return {"recitative": rows(rec), "rec_bass": rows(rec_bass), "aria": rows(aria), "aria_bass": rows(aria_bass), "unit": unit_r,
            "starts": {k: float(s.events[k]) for k in ("recitative", "aria")},
            "clips": {"two": save("monody.two", s, kind="synthesized", level=None, detail="a recitative, then an aria, ours: one synthetic voice over a harpsichord bass")}}


def compute_corelli() -> dict:
    d = B.load()["corelli"]
    v1, v2, bass = d["Violino I."], d["Violino II."], d["Violone e Organo"]
    fl = B.figured_line(bass, [v1, v2])
    basses = [Pitch.from_midi(p, flats=True) for p, _, _, _ in fl]
    real = FIG.realize(basses, [f for *_, f in fl], key=-1, voices=3, low=55, high=81)
    agree = B.agreement(real["chords"], bass, [v1, v2])
    bars = 8
    T = bars * 96                                                  # bars of 4/4
    cut = lambda ln: [(p, o / 24.0, min(d, T - o) / 24.0) for p, o, d in ln if o < T]  # noqa: E731
    V1, V2, BS = cut(v1), cut(v2), cut(bass)
    chords = []
    for ch, (p, o, dd) in zip(real["chords"], bass):
        if o < T:
            for m in ch:
                chords.append((m, o / 24.0, min(dd, T - o) / 24.0))
    unit = 0.5                                                     # seconds a quarter note: a grave tempo
    c1 = place([V1, V2, BS, BS], [violin, violin, organ, harpsichord], unit, gains=[0.0, -1.0, -6.0, -3.0])
    c2 = place([chords, BS], [organ, harpsichord], unit, gains=[-6.0, -3.0])
    s = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=1.2, names=["corelli", "realized"])
    figs = Counter(f for *_, f in fl)
    return {"v1": rows(V1), "v2": rows(V2), "bass": rows(BS), "chords": rows(chords), "unit": unit, "bars": bars,
            "figures": [[float(o) / 24.0, f] for p, o, d, f in fl if o < T], "figure_counts": dict(figs), "notes": len(bass),
            "agreement": agree, "parallels": real["parallels"], "starts": {k: float(s.events[k]) for k in ("corelli", "realized")},
            "clips": {"two": save("corelli.grave", s, kind="synthesized", level=None,
                                  detail="Corelli, Op. 3 No. 1, Grave, bars 1-8, from the encoding: two violins and continuo; then the bass figured from the violins and realized by Part 10's realizer")}}


def compute_modes() -> dict:
    pal = [p for p in R.load() if p.book == 0]
    modes = Counter(p.mode.split(":")[1] if p.mode else "untagged" for p in pal)
    bach = Counter(c.mode or "untagged" for c in BC.load())
    return {"palestrina": dict(modes), "bach": dict(bach), "n_pal": len(pal), "n_bach": sum(bach.values())}


def compute_ritornello() -> dict:
    """A concerto movement in C (ours): the ritornello (R), a solo episode, R in G, an episode, R in A minor (its head
    only), an episode, R in C.  Then the finder looks for R's head anywhere."""
    R0 = [(72, 0, 0.5), (76, 0.5, 0.5), (79, 1, 0.5), (76, 1.5, 0.5), (84, 2, 1), (83, 3, 0.5), (81, 3.5, 0.5),
          (79, 4, 0.5), (77, 4.5, 0.5), (76, 5, 0.5), (74, 5.5, 0.5), (72, 6, 2)]
    def shift(line, k, t0, diatonic_minor=False):
        return [(p + k, o + t0, d) for p, o, d in line]
    def episode(t0, start, steps=12):
        out, p = [], start
        for i in range(steps):
            out.append((p, t0 + 0.5 * i, 0.5))
            p += [2, 1, -1, 2, -2, 1][i % 6]
        return out
    tl = 0.0
    melody, plan = [], []
    melody += shift(R0, 0, tl); plan.append(("R", "C", tl)); tl += 8
    melody += episode(tl, 74); plan.append(("solo", "to G", tl)); tl += 6
    melody += shift(R0, 7, tl); plan.append(("R", "G", tl)); tl += 8
    melody += episode(tl, 76); plan.append(("solo", "to A minor", tl)); tl += 6
    head = shift(R0[:7], 9, tl)
    head = [(p - (1 if (p - 9) % 12 in (4, 11) else 0), o, d) for p, o, d in head]   # into the minor: the third lowered
    melody += head; plan.append(("R", "A minor (head)", tl)); tl += 4
    melody += episode(tl, 72); plan.append(("solo", "back", tl)); tl += 6
    melody += shift(R0, 0, tl); plan.append(("R", "C", tl)); tl += 8
    found = B.ritornello_returns([(p, o, d) for p, o, d in melody], head=6, tolerance=1)
    bass = []
    for kind, key, t0 in plan:
        root = {"C": 48, "G": 43, "to G": 50, "to A minor": 52, "A minor (head)": 45, "back": 43}.get(key, 48)
        span = 8 if kind == "R" and "head" not in key else (4 if "head" in key else 6)
        for b in range(int(span)):
            bass.append((root + (0 if b % 2 == 0 else 7), t0 + b, 1))
    unit = 0.3
    c = place([melody, bass], [violin, harpsichord], unit, gains=[0.0, -4.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["concerto"])
    return {"melody": rows(melody), "bass": rows(bass), "plan": [[a, b, float(c_)] for a, b, c_ in plan], "unit": unit,
            "found": [{"onset": float(f["onset"]), "transpose": f["transpose"], "misses": f["misses"]} for f in found],
            "clips": {"concerto": save("ritornello.concerto", s, level=None, detail="a concerto movement in ritornello form, ours: the ritornello in C, G, A minor (its head) and C, with solo episodes, violin and harpsichord")}}


def compute_ornaments() -> dict:
    plain = [(76, 0, 1), (74, 1, 1), (72, 2, 1), (74, 3, 1), (76, 4, 1), (77, 5, 1), (76, 6, 2)]
    orn = []
    orn += B.appoggiatura(76, 0, 1, from_above=1)
    orn += [(74, 1, 1)]
    orn += B.mordent(72, 2, 1)
    orn += [(74, 3, 1)]
    orn += [(76, 4, 1)]
    orn += B.trill(77, 5, 1, upper=2, n=6, turn=False)
    orn += [(76, 6, 2)]
    straight = [(72 + p, 0.5 * i, 0.5) for i, p in enumerate([0, 2, 4, 5, 7, 5, 4, 2, 0, 2, 4, 2, 0, -1, 0, 0])]
    uneven = B.inegale(straight, ratio=2.0, unit=0.5)
    unit = 0.5
    c1 = place([plain], [harpsichord], unit)
    c2 = place([orn], [harpsichord], unit)
    c3 = place([straight], [harpsichord], 0.6)
    c4 = place([uneven], [harpsichord], 0.6)
    s = concat([c1.at_level(LEVEL), c2.at_level(LEVEL), c3.at_level(LEVEL), c4.at_level(LEVEL)], gap=0.9, names=["plain", "ornamented", "straight", "inegale"])
    return {"plain": rows(plain), "ornamented": rows(orn), "straight": rows(straight), "inegale": rows(uneven), "unit": unit, "unit2": 0.6,
            "starts": {k: float(s.events[k]) for k in ("plain", "ornamented", "straight", "inegale")},
            "clips": {"four": save("ornaments.four", s, level=None, detail="a plain line, then ornamented (appoggiatura, mordent, trill); straight eighths, then notes inégales at 2:1, harpsichord")}}


def tune_line():
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in zip(t.pitches, t.beats):
        out.append((72 + p, a, float(d)))
        a += d
    return out


def compute_dances() -> dict:
    tl = tune_line()[:7]
    pitches = [p for p, _, _ in tl] + [tl[-1][0]]
    clips, out = [], {}
    tempo = {"allemande": 0.42, "courante": 0.36, "sarabande": 0.55, "gigue": 0.3}
    for name, info in B.DANCES.items():
        pat = info["pattern"]
        notes, t = [], 0.0
        for k, p in enumerate(pitches):
            d = pat[k % len(pat)]
            notes.append((p, t, d))
            t += d
        clips.append(place([notes], [harpsichord], tempo[name]).at_level(LEVEL))
        out[name] = {"metre": info["metre"], "tempo": info["tempo"], "notes": rows(notes), "unit": tempo[name]}
    s = concat(clips, gap=0.9, names=list(B.DANCES))
    return {"dances": out, "starts": {k: float(s.events[k]) for k in B.DANCES},
            "clips": {"four": save("dances.four", s, level=None, detail="the Tune's first phrase as an allemande, a courante, a sarabande and a gigue, harpsichord")}}


def compute_keys() -> dict:
    temps = {"quarter-comma meantone": TU.meantone(), "Werckmeister III": TU.werckmeister3(), "equal": TU.equal(12)}
    table = {k: B.key_colours(t) for k, t in temps.items()}
    # a I-IV-V-I cadence in C and in F#, in Werckmeister III, organ tones at exact cents
    w = temps["Werckmeister III"]

    def note(name_index, octave):
        c = w.cents[name_index % 12] + 1200 * (octave - 4)
        return 60 + c / 100.0

    def cadence(tonic):
        chords = [(0, 4, 7), (5, 9, 0), (7, 11, 2), (0, 4, 7)]
        lines = [[], [], [], []]
        for k, ch in enumerate(chords):
            root = (tonic + ch[0]) % 12
            notes = [note(root, 3)] + [note((tonic + x) % 12, 4) for x in ch]
            for j, m in enumerate(notes):
                lines[j].append((m, 2 * k, 2))
        return lines
    cC = place(cadence(0), [organ] * 4, 0.55)
    cF = place(cadence(6), [organ] * 4, 0.55)
    s = concat([cC.at_level(LEVEL), cF.at_level(LEVEL)], gap=1.2, names=["C", "F#"])
    return {"table": {k: [{kk: (round(v, 2) if isinstance(v, float) else v) for kk, v in r.items()} for r in rows_] for k, rows_ in table.items()},
            "starts": {"C": float(s.events["C"]), "F#": float(s.events["F#"])},
            "werck_C": next(r for r in table["Werckmeister III"] if r["key"] == "C"), "werck_Fs": next(r for r in table["Werckmeister III"] if r["key"] == "F#"),
            "clips": {"two": save("keys.cadences", s, kind="synthesized", level=None, detail="I-IV-V-I in C, then in F sharp, in Werckmeister III, organ tones at the temperament's exact pitches")}}


def compute_handel() -> dict:
    d = B.load()["handel"]
    voice = d[""]
    rh, lh = d["Piano"], d["Piano (staff 2)"]
    T = 8 * 96
    cut = lambda ln: [(p, o / 24.0, min(dd, T - o) / 24.0) for p, o, dd in ln if o < T]  # noqa: E731
    V, RH, LH = cut(voice), cut(rh), cut(lh)
    unit = 0.62
    inst = mix([(place([RH, LH], [harpsichord, harpsichord], unit, gains=[-3.0, -2.0]), 0.0, -2.0)]
               + ([(sing(V, unit, "soprano", "a"), 0.0, 0.0)] if V else []), duration=8 * 4 * unit + 1.0)
    s = concat([Clip(inst.y, SR).at_level(LEVEL)], gap=0.0, names=["aria"])
    return {"voice": rows(V), "rh": rows(RH), "lh": rows(LH), "unit": unit,
            "clips": {"aria": save("handel.lascia", s, kind="synthesized", level=None, detail="Handel, Lascia ch'io pianga (Rinaldo, 1711), the opening bars from the encoding: a synthetic voice and harpsichord")}}


def compute_tune() -> dict:
    tl = tune_line()[:14]
    # French overture: dotted, double-dotted, with a rushing upbeat (tirade) before strong notes
    over = []
    t = 0.0
    for k, (p, o, d) in enumerate(tl):
        if d >= 1 and k % 2 == 0:
            over += [(p, t, 0.75), (p, t + 0.75, 0.25)]
        else:
            over.append((p, t, d))
        t += d
    over2 = []
    for p, o, d in over:
        if abs(d - 0.75) < 1e-9:
            over2.append((p, o, 0.875))
        elif abs(d - 0.25) < 1e-9:
            over2.append((p, o + 0.125, 0.125))
        else:
            over2.append((p, o, d))
    tirade = [(over2[6][0] - 5 + k, over2[6][1] - 0.4 + 0.1 * k, 0.1) for k in range(4)]
    over_bass = [(48, 0, 4), (53, 4, 2), (55, 6, 2), (48, 8, 4), (55, 12, 2), (48, 14, 2)]
    # chaconne: a four-bar ground (C G A E F C F G) under the Tune's phrases, the reprise ornamented
    ground = [(48, 0, 2), (43, 2, 2), (45, 4, 2), (40, 6, 2), (41, 8, 2), (36, 10, 2), (41, 12, 2), (43, 14, 2)]
    phrase = tune_line()[:14]
    reprise = []
    for p, o, d in phrase:
        if d >= 2:
            reprise += B.trill(p, o, d, upper=2, n=6, turn=True)
        elif o % 2 == 0:
            reprise += B.mordent(p, o, d)
        else:
            reprise.append((p, o, d))
    unit = 0.38
    c1 = place([over2 + tirade, over_bass], [harpsichord, harpsichord], unit, gains=[0.0, -2.0])
    ch_mel = phrase + [(p, o + 16, d) for p, o, d in reprise]
    ch_bass = ground + [(p, o + 16, d) for p, o, d in ground]
    c2 = place([ch_mel, ch_bass], [harpsichord, harpsichord], unit, gains=[0.0, -2.0])
    s = concat([c1.at_level(LEVEL), c2.at_level(LEVEL)], gap=1.2, names=["overture", "chaconne"])
    return {"overture": rows(over2 + tirade), "overture_bass": rows(over_bass), "chaconne": rows(ch_mel), "ground": rows(ch_bass), "unit": unit,
            "starts": {k: float(s.events[k]) for k in ("overture", "chaconne")}, "ornaments": len(reprise) - len(phrase), "seconds": s.duration,
            "clips": {"variation": save("tune.variation25", s, level=None, detail="the Tune as a French overture (dotted, with a rushing upbeat) and as a chaconne on a four-bar ground with an ornamented reprise, harpsichord")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 25, "title": r"as a French overture and as a chaconne with an ornamented reprise", "seconds": round(t["seconds"], 2),
            "measure": rf"a ground of 8 bass notes heard twice; the reprise adds {t['ornaments']} ornament notes to 14",
            "clip": "tune.variation25"}


def compute_realize3() -> dict:
    """Corelli's first two bars of bass with the figures the violins imply, realized three ways: the realizer's
    smoothest choice with the top voice near three different starting notes."""
    d = B.load()["corelli"]
    v1, v2, bass = d["Violino I."], d["Violino II."], d["Violone e Organo"]
    fl = [x for x in B.figured_line(bass, [v1, v2]) if x[1] < 2 * 96]
    basses = [Pitch.from_midi(p, flats=True) for p, _, _, _ in fl]
    figs = [f for *_, f in fl]
    outs, clips = [], []
    for top in (72, 77, 81):
        r = FIG.realize(basses, figs, key=-1, voices=3, low=55, high=84, top=top)
        chords = []
        for ch, (p, o, dd, f) in zip(r["chords"], fl):
            for m in ch:
                chords.append((m, o / 24.0, dd / 24.0))
        bl = [(p, o / 24.0, dd / 24.0) for p, o, dd, f in fl]
        clips.append(place([chords, bl], [harpsichord, harpsichord], 0.5, gains=[-2.0, 0.0]).at_level(LEVEL))
        outs.append({"top": top, "chords": rows(chords), "tops": [int(max(ch)) for ch in r["chords"]]})
    s_ = concat(clips, gap=0.9, names=["r1", "r2", "r3"])
    return {"figures": figs, "bass": rows([(p, o / 24.0, dd / 24.0) for p, o, dd, f in fl]), "realizations": outs, "unit": 0.5,
            "starts": {k: float(s_.events[k]) for k in ("r1", "r2", "r3")},
            "clips": {"three": save("continuo.three", s_, level=None, detail="Corelli's first two bars of bass with their figures, realized three ways on harpsichord")}}


def compute_wolf() -> dict:
    mt = TU.meantone()
    c_g = (mt.cents[7] - mt.cents[0]) % 1200
    gs_eb = (mt.cents[3] - mt.cents[8]) % 1200
    def fifth(lo_pc, cents):
        base = 48 + mt.cents[lo_pc] / 100.0
        return [[(base, 0, 3)], [(base + cents / 100.0, 0, 3)]]
    a = place(fifth(0, c_g), [organ, organ], 0.8)
    b = place(fifth(8, gs_eb), [organ, organ], 0.8)
    s_ = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["good", "wolf"])
    return {"good": c_g, "wolf": gs_eb, "starts": {"good": float(s_.events["good"]), "wolf": float(s_.events["wolf"])},
            "clips": {"two": save("temperament.wolf", s_, kind="synthesized", level=None, detail="quarter-comma meantone: the fifth C-G, then the wolf G sharp-E flat, organ tones")}}


def compute_fundamental() -> dict:
    """Rameau's fundamental bass under a Bach chorale phrase: the chord roots on the beats, and how they move."""
    from explainer.music.monochord import fourpart as FP
    book = [c for c in BC.load() if c.mode == "major"]
    c = book[0]
    labs = FP.beat_labels(c)
    first_end = next(i for i, x in enumerate(labs) if x["fermata"])
    phrase = labs[: first_end + 1]
    roots, motions = [], Counter()
    prev = None
    for x in phrase:
        if x["label"] is None:
            continue
        r = (x["label"][0] + c.tonic) % 12
        roots.append((r, x["tick"]))
        if prev is not None and r != prev:
            iv = (r - prev) % 12
            motions[{5: "up a fourth (down a fifth)", 7: "up a fifth", 2: "up a step", 10: "down a step", 3: "up a third", 9: "down a third", 4: "up a third", 8: "down a third"}.get(iv, "other")] += 1
        prev = r
    T = phrase[-1]["tick"] + 24
    sop = [(p, o / 24.0, min(d, T - o) / 24.0) for p, o, d, _ in c.voices[0] if o < T]
    bas = [(p, o / 24.0, min(d, T - o) / 24.0) for p, o, d, _ in c.voices[3] if o < T]
    fund = [(36 + r, t / 24.0, 1.0) for r, t in roots]
    unit = 0.55
    a = place([sop, bas], [harpsichord, harpsichord], unit, gains=[0.0, -1.0])
    b = place([sop, bas, fund], [harpsichord, harpsichord, organ], unit, gains=[0.0, -1.0, -3.0])
    s_ = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["real", "fundamental"])
    return {"name": c.name, "soprano": rows(sop), "bass": rows(bas), "fundamental": rows(fund), "motions": dict(motions), "unit": unit,
            "starts": {"real": float(s_.events["real"]), "fundamental": float(s_.events["fundamental"])},
            "clips": {"two": save("keys.fundamental", s_, kind="synthesized", level=None, detail=f"Bach, chorale {c.name}, its first phrase: soprano and bass, then with Rameau's fundamental bass added below (organ)")}}


def compute_lament() -> dict:
    ground = [(57, 0, 2), (55, 2, 2), (53, 4, 2), (52, 6, 2)]
    bass = [(p, o + 8 * k, d) for k in range(3) for p, o, d in ground]
    mel = [(72, 0, 1.5), (71, 1.5, 0.5), (69, 2, 2), (72, 4, 1), (71, 5, 1), (69, 6, 1), (68, 7, 1),
           (69, 8, 1), (72, 9, 1), (76, 10, 2), (74, 12, 1), (72, 13, 1), (71, 14, 2),
           (72, 16, 1), (71, 17, 1), (69, 18, 1), (67, 19, 1), (65, 20, 1), (64, 21, 1), (64, 22, 2)]
    unit = 0.5
    c = mix([(sing(mel, unit, "soprano", "a"), 0.0, 0.0), (place([bass], [harpsichord], unit), 0.0, -3.0)], duration=24 * unit + 1.2)
    s_ = concat([Clip(c.y, SR).at_level(LEVEL)], gap=0.0, names=["lament"])
    return {"melody": rows(mel), "bass": rows(bass), "unit": unit,
            "clips": {"lament": save("opera.lament", s_, kind="synthesized", level=None, detail="a lament over the descending tetrachord A G F E, three times, ours: a synthetic soprano and harpsichord")}}


def compute_pitch() -> dict:
    standards = [("French chamber pitch", 392.0), ("today's Baroque convention", 415.0), ("modern", 440.0), ("Venetian cornett pitch", 465.0)]
    clips = []
    for name, a4 in standards:
        m = 69 + 12 * np.log2(a4 / 440.0)
        lines = [[(m - 12, 0, 2.5)], [(m - 8, 0, 2.5)], [(m - 5, 0, 2.5)], [(m, 0, 2.5)]]
        clips.append(place(lines, [organ] * 4, 0.6).at_level(LEVEL))
    s_ = concat(clips, gap=0.8, names=[n for n, _ in standards])
    return {"standards": [[n, a] for n, a in standards], "starts": {n: float(s_.events[n]) for n, _ in standards},
            "clips": {"four": save("frontier.pitch", s_, kind="synthesized", level=None, detail="an A major chord with A at 392, 415, 440 and 465 Hz, organ tones")}}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation25", 25)


ITEMS = {"hook": compute_hook, "realize3": compute_realize3, "wolf": compute_wolf, "fundamental": compute_fundamental,
         "lament": compute_lament, "pitch": compute_pitch, "monody": compute_monody, "corelli": compute_corelli, "modes": compute_modes, "ritornello": compute_ritornello,
         "ornaments": compute_ornaments, "dances": compute_dances, "keys": compute_keys, "handel": compute_handel, "tune": compute_tune,
         "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
