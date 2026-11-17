"""Precompute everything numerical, and every sound, in Part 23 of *Music, Built* ("Chant to Polyphony").

    python -m videos.music.music23.compute              # everything missing (a few minutes)
    python -m videos.music.music23.compute --force isorhythm

Numbers are cached in ``.cache/music23/<name>.json``, sounds in ``.cache/music23/audio/``.  The theory is Monochord's
(``explainer/music/monochord/medieval.py``); the fourteenth-century pieces are ``monochord/trecento.py``'s table (the
editions' pitches and times, editorial accidentals included); everything heard is sung by Part 17's choir (Part 8's
source-filter voice), so every clip is labelled synthesized.  Published findings are cited in the README.

Items:
    hook        an organum on one held note in the manner of the Notre Dame quadrupla (ours), heard
    chant       Ut queant laxis sung; the eight modes; two psalm verses on D (an ear question)
    guido       the gamut and the hexachords; Ut queant laxis solmized; a line that must mutate, heard
    organum     parallel organum at the fifth with its tritones, and the Enchiriadis rule (an ear question); florid
    rhythm      the six rhythmic modes on one line, heard; ligature patterns
    notre       a clausula: the chant in long notes, a voice in the first mode above it
    motet       a three-voice motet: tenor ordo, motetus and triplum with their own rhythms
    mensuration the same note shapes read in the four mensurations, heard; Franco's rules
    isorhythm   the engine (color against talea), heard; talea scans of every motet in the corpus
    vitry       an excerpt of de Vitry's Vos qui admiramini, sung from the edition
    census      intervals on and off the beat, parallels against Bach, cadences, finals, ficta
    landini     Landini cadences counted by composer; one heard
    cadence     the double leading-tone cadence against a plain one (an ear question)
    subtilior   rhythmic proportions against one another, heard; the corpus's rhythmic variety
    tune        Variation 23: the Tune as chant, as organum and as an isorhythmic motet
    variation   the Variations ledger, row 23
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import medieval as MD
from explainer.music.monochord import melody as M
from explainer.music.monochord import trecento as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver, signoff

CACHE = Cache("music23")
CLIPS = ClipStore("music23")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")


def sing(voices, unit: float, parts=None, vowels=None, gains=None, tail: float = 0.6, seed: int = 0) -> Clip:
    """Voices of (key number, onset, duration) in units of ``unit`` seconds, each sung by one of the choir's parts."""
    parts = parts or ["tenor"] * len(voices)
    vowels = vowels or ["a"] * len(voices)
    gains = gains or [0.0] * len(voices)
    outs = []
    for j, v in enumerate(voices):
        if not v:
            continue
        y = CH.sing([(m, a * unit, d * unit) for m, a, d in v], parts[j], vowels[j], seed=seed + j)
        outs.append(y * 10 ** (gains[j] / 20))
    n = max(len(y) for y in outs) + int(tail * SR)
    out = np.zeros(n)
    for y in outs:
        out[: len(y)] += y
    return Clip(out / max(np.abs(out).max(), 1e-9) * 0.5, SR).fade(0.02, 0.3)


def rows(v):
    return [[int(p), float(a), float(d)] for p, a, d in v]


def chant_notes(pitches, ends=(), unit=1.0):
    """Chant in free rhythm: equal notes, the last of each phrase held."""
    out, t = [], 0.0
    for k, p in enumerate(pitches):
        d = 2.0 * unit if (k in ends or k == len(pitches) - 1) else unit
        out.append((p, t, d))
        t += d
    return out


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    rng = np.random.default_rng(23)
    lines = MD.notre_dame(53, 18, rng, voices=3, exchange=3)
    unit = 0.24
    c = sing(lines, unit, parts=["alto", "tenor", "tenor", "bass"], vowels=["a", "a", "O", "a"], gains=[-1.0, -2.0, -2.0, 0.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["organum"])
    return {"lines": [rows(v) for v in lines], "unit": unit, "perfections": 18,
            "clips": {"organum": save("hook.organum", s, level=None, detail="an organum on one held F in the manner of the Notre Dame quadrupla, ours: four of Part 17's voices")}}


def compute_chant() -> dict:
    ut = [p for p, _ in MD.UT_QUEANT]
    ends = [i - 1 for i in MD.UT_LINES[1:]]
    notes = chant_notes(ut, ends)
    unit = 0.42
    c = sing([notes], unit, parts=["tenor"], vowels=["a"])
    s1 = concat([c.at_level(LEVEL)], gap=0.0, names=["ut"])
    # two verses ending on D: an authentic one (mode 1) and a plagal one (mode 2); B first
    pA, pB = MD.psalm_tone(2, 16), MD.psalm_tone(1, 16)
    cA = sing([chant_notes(pA)], 0.36)
    cB = sing([chant_notes(pB)], 0.36)
    q = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    modes = {m: {"name": MD.MODES[m][0], "final": MD.MODES[m][1], "tenor": MD.MODES[m][2], "range": MD.mode_range(m),
                 "tone": MD.psalm_tone(m)} for m in range(1, 9)}
    return {"ut": rows(notes), "ut_syllables": [s for _, s in MD.UT_QUEANT], "ut_lines": MD.UT_LINES, "ut_mode": MD.classify(ut),
            "unit": unit, "modes": modes, "quiz": {"A": pA, "B": pB, "modes": [MD.classify(pA), MD.classify(pB)]},
            "quiz_starts": {k: float(q.events[k]) for k in "AB"}, "quiz_unit": 0.36,
            "clips": {"ut": save("chant.ut", s1, level=None, detail="Ut queant laxis, after the Liber Usualis, pitches only, one voice"),
                      "quiz": save("chant.modes", q, level=None, detail="two psalm verses ending on D: modes 2 and 1, simplified tones")}}


def compute_guido() -> dict:
    ut = [p for p, _ in MD.UT_QUEANT]
    syl, mut = MD.solmize(ut)
    line = [65, 67, 69, 70, 69, 67, 65, 67, 69, 71, 72, 71, 69, 67]      # F G A B-flat ... then up through B-natural to C
    syl2, mut2 = MD.solmize(line)
    c = sing([chant_notes(line)], 0.4)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["line"])
    hexa = [{"kind": k, "start": st, "notes": [st + d for d in MD.STEPS6]} for k, st in MD.hexachords()]
    return {"ut_syllables": syl, "ut_mutations": mut, "line": line, "line_syllables": syl2, "line_mutations": mut2,
            "gamut": MD.gamut(), "hexachords": hexa, "unit": 0.4,
            "clips": {"mutation": save("guido.mutation", s, level=None, detail="a line through B-flat and then B-natural, one voice")}}


def compute_organum() -> dict:
    pt = MD.psalm_tone(2, 14)                            # recites on F
    fifths = MD.parallel(pt, -4)                         # a diatonic fifth below: B under F, a tritone
    flat = [q - 1 if q % 12 == 11 else q for q in fifths]    # with B-flat: true fifths
    ench = MD.enchiriadis(pt, floor=60, steps=-3)        # at the fourth, never below C, meeting at the end
    unit = 0.42
    cA = sing([chant_notes(pt), chant_notes(flat)], unit, parts=["tenor", "bass"])
    cB = sing([chant_notes(pt), chant_notes(fifths)], unit, parts=["tenor", "bass"])
    q = concat([cA.at_level(LEVEL), cB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    ce = sing([chant_notes(pt), chant_notes(ench)], unit, parts=["tenor", "bass"])
    e = concat([ce.at_level(LEVEL)], gap=0.0, names=["ench"])
    rng = np.random.default_rng(5)
    tenor = [62, 65, 64, 62, 60, 62]
    fl = MD.florid(tenor, rng)
    upper, ten, t = [], [], 0.0
    for p, line in zip(tenor, fl):
        for k, x in enumerate(line):
            upper.append((x, t + k, 1.0))
        ten.append((p - 12, t, float(len(line))))
        t += len(line)
    cf = sing([upper, ten], 0.26, parts=["tenor", "bass"], gains=[0.0, -1.0])
    f = concat([cf.at_level(LEVEL)], gap=0.0, names=["florid"])
    return {"chant": pt, "fifths": fifths, "flat": flat, "enchiriadis": ench,
            "tritones": {"parallel": MD.tritones(pt, fifths), "flat": MD.tritones(pt, flat), "enchiriadis": MD.tritones(pt, ench)},
            "starts": {k: float(q.events[k]) for k in "AB"}, "unit": unit, "answer": "B",
            "florid": {"upper": rows(upper), "tenor": rows(ten), "unit": 0.26, "per_note": [len(x) for x in fl]},
            "clips": {"quiz": save("organum.quiz", q, level=None, detail="two organa at the fifth below a psalm verse: with B-flat under F, then with B-natural (a tritone)"),
                      "enchiriadis": save("organum.enchiriadis", e, level=None, detail="organum at the fourth by the Enchiriadis rule: the lower voice never below C, meeting the chant at the end"),
                      "florid": save("organum.florid", f, level=None, detail="florid organum over six chant notes, ours")}}


def compute_rhythm() -> dict:
    line = [65, 67, 69, 67, 65, 64, 62, 64, 65, 67, 65, 64]
    unit = 0.2
    parts, starts, t = [], {}, 0.0
    clips = []
    for m in range(1, 7):
        n = MD.realize(m, line[: (9 if m in (1, 2, 5) else 12) if m != 3 else 10])
        clips.append(sing([n], unit).at_level(LEVEL))
        parts.append(rows(n))
    s = concat(clips, gap=0.8, names=[f"m{m}" for m in range(1, 7)])
    return {"modes": {m: {"pattern": MD.RHYTHMIC_MODES[m], "name": MD.MODE_NAMES[m], "ligatures": MD.LIGATURES[m],
                          "notes": parts[m - 1]} for m in range(1, 7)},
            "starts": {m: float(s.events[f"m{m}"]) for m in range(1, 7)}, "unit": unit,
            "clips": {"six": save("rhythm.modes", s, level=None, detail="one line in each of the six rhythmic modes, one voice")}}


def compute_notre() -> dict:
    tenor = [65, 67, 65, 64, 62, 64, 65, 67]               # a chant fragment in long notes (mode 5)
    rng = np.random.default_rng(3)
    dup, ten = [], []
    t = 0.0
    prev = 72
    for k, p in enumerate(tenor):
        ten.append((p - 12, t, 3.0))
        cons = [p + c for c in (7, 12) if p + c <= 79]
        a = min(cons, key=lambda x: abs(x - prev))
        nb = MD.diatonic_shift(a, int(rng.choice([-1, 1])))
        dup.append((a, t, 2.0))
        dup.append((nb, t + 2.0, 1.0))
        prev = nb
        t += 3.0
    c = sing([dup, ten], 0.3, parts=["tenor", "bass"], gains=[0.0, -1.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["clausula"])
    return {"duplum": rows(dup), "tenor": rows(ten), "unit": 0.3,
            "clips": {"clausula": save("notre.clausula", s, level=None, detail="a discant clausula, ours: the chant in long notes, a voice in the first mode")}}


def compute_motet() -> dict:
    color = [53, 55, 57, 55, 53, 52, 50, 52, 53]
    ordo = [3, 3, 3, -3]                                   # mode 5 ordo: three longs and a rest
    ten = MD.isorhythm(color, ordo, repeats=1)
    T_end = max(a + d for _, a, d in ten)
    rng = np.random.default_rng(9)
    mot, tri = [], []
    t, p = 0.0, 65
    while t < T_end:
        for d in (2.0, 1.0):
            mot.append((p, t, d))
            t += d
            p = MD.diatonic_shift(p, int(rng.choice([-1, 1, 1, -2, 2]))) if 60 <= p <= 74 else 67
    t, q = 0.0, 72
    while t < T_end:
        for d in (1.0, 1.0, 1.0):
            tri.append((q, t, d))
            t += d
            q = MD.diatonic_shift(q, int(rng.choice([-1, 1, -1, 2, -2]))) if 67 <= q <= 79 else 74
    # perfect consonances on each perfection with the tenor where it sounds
    def snap(v):
        out = []
        for p, a, d in v:
            if a % 3 == 0:
                under = [x for x, o, dd in ten if o <= a < o + dd]
                if under:
                    p = min((y for y in range(p - 4, p + 5) if (y - under[0]) % 12 in (0, 7)), key=lambda y: abs(y - p))
            out.append((p, a, d))
        return out
    mot, tri = snap(mot), snap(tri)
    c = sing([tri, mot, ten], 0.26, parts=["alto", "tenor", "bass"], vowels=["i", "a", "O"], gains=[-1.0, -1.0, 0.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["motet"])
    return {"triplum": rows(tri), "motetus": rows(mot), "tenor": rows(ten), "unit": 0.26, "total": T_end,
            "clips": {"three": save("motet.three", s, level=None, detail="a three-voice motet, ours: tenor in the fifth mode, motetus in the first, triplum in the sixth")}}


def compute_mensuration() -> dict:
    # one string of shapes: B S S B S M M S B (breve, semibreve, minim), read in the four mensurations
    shapes = ["B", "S", "S", "B", "S", "M", "M", "S", "B"]
    pitches = [62, 64, 65, 67, 65, 64, 62, 64, 62]
    out, clips = {}, []
    for (tp, pm), (sign, minims, modern) in MD.MENSURATIONS.items():
        s_in_b, m_in_s = MD.breve(tp, pm)
        val = {"B": s_in_b * m_in_s, "S": m_in_s, "M": 1}
        notes, t = [], 0.0
        for p, sh in zip(pitches, shapes):
            notes.append((p, t, float(val[sh])))
            t += val[sh]
        clips.append(sing([notes], 0.17).at_level(LEVEL))
        out[sign] = {"modern": modern, "minims_per_breve": minims, "notes": rows(notes)}
    s = concat(clips, gap=0.9, names=list(out))
    rules = {"BSB": MD.read_perfect("BSB"), "BSSB": MD.read_perfect("BSSB"), "BSSSB": MD.read_perfect("BSSSB"), "BSSSSB": MD.read_perfect("BSSSSB")}
    return {"shapes": shapes, "pitches": pitches, "readings": out, "starts": {k: float(s.events[k]) for k in out}, "unit": 0.17, "franco": rules,
            "clips": {"four": save("mensuration.four", s, level=None, detail="one row of note shapes read in the four mensurations, one voice")}}


def compute_isorhythm() -> dict:
    color = [53, 55, 57, 58, 57, 55, 53]                 # seven pitches
    talea = [3, 3, 2, 1, -3, 3, -3]                      # five notes and two rests
    n_tal = sum(1 for d in talea if d > 0)
    notes = MD.isorhythm(color, talea)
    per = MD.periods(len(color), n_tal)
    rng = np.random.default_rng(23)
    upper, t = [], 0.0
    T_end = max(a + d for _, a, d in notes)
    p = 65
    while t < T_end:
        under = [x for x, o, d in notes if o <= t < o + d]
        if under and t % 3 == 0:
            p = min((y for y in range(p - 4, p + 5) if (y - under[0]) % 12 in (0, 7)), key=lambda y: abs(y - p))
        upper.append((p, t, 1.0 if rng.random() < 0.6 else 2.0))
        t += upper[-1][2]
        p = MD.diatonic_shift(p, int(rng.choice([-1, 1, 2, -2])))
        p = min(max(p, 62), 76)
    c = sing([upper, notes], 0.2, parts=["tenor", "bass"], gains=[-2.0, 0.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["engine"])
    # the corpus: every piece's lowest voices scanned for a talea
    book = T.load()
    scans = []
    for pc in book:
        best = None
        for j, v in enumerate(pc.voices):
            sc = MD.talea_scan(v, pc.bar)
            if best is None or sc["share"] > best["share"]:
                best = {"voice": j, "lag": sc["lag"], "share": sc["share"]}
        ch = MD.shuffled_share(pc.voices[best["voice"]], pc.bar, rng, trials=6)
        scans.append({"name": pc.name, "title": pc.title, "composer": pc.composer, "genre": pc.genre, "bars": pc.length // pc.bar,
                      "lag": best["lag"], "share": best["share"], "chance": ch, "voice": best["voice"], "voices": len(pc.voices)})
    iso = [s_ for s_ in scans if s_["share"] - s_["chance"] >= 0.25 and s_["share"] >= 0.6]
    vos = [pc for pc in book if pc.name.startswith("PMFC_01-Vos")][0]
    tenor_scan = MD.talea_scan(vos.voices[2], vos.bar)
    vitry = []
    for pc in book:
        if pc.composer != "Philippe de Vitry":
            continue
        sc = MD.talea_scan(pc.voices[2], pc.bar)
        P = sc["lag"]
        per_voice = []
        for v in pc.voices:
            f = MD.bar_prints(v, pc.bar)
            per_voice.append(float(np.mean([f[i] == f[i + P] for i in range(len(f) - P)])))
        vitry.append({"title": pc.title, "lag": P, "bars": pc.length // pc.bar, "shares": per_voice, "scan": {str(k): v for k, v in sc["scan"].items()},
                      "chance": MD.shuffled_share(pc.voices[2], pc.bar, rng, trials=10)})
    return {"color": color, "talea": talea, "notes": rows(notes), "upper": rows(upper), "periods": per, "unit": 0.2,
            "vitry": vitry, "scans": scans, "isorhythmic": [x["title"] for x in iso], "n_iso": len(iso),
            "vos_scan": {str(k): v for k, v in tenor_scan["scan"].items()}, "vos_lag": tenor_scan["lag"],
            "clips": {"engine": save("isorhythm.engine", s, level=None, detail="an isorhythmic tenor, ours: a color of 7 pitches through a talea of 5 notes, with a free voice above")}}


def excerpt(piece, bars: int, start_bar: int = 0):
    lo, hi = start_bar * piece.bar, (start_bar + bars) * piece.bar
    out = []
    for v in piece.voices:
        out.append([(p, (o - lo) / 24.0, d / 24.0) for p, o, d in v if lo <= o < hi])
    return out


def compute_vitry() -> dict:
    book = T.load()
    vos = [pc for pc in book if pc.name.startswith("PMFC_01-Vos")][0]
    ex = excerpt(vos, 14)
    q = 0.36                                             # seconds a quarter note of the edition
    c = sing(ex, q, parts=["alto", "tenor", "bass", "bass"], vowels=["i", "a", "O", "u"], gains=[-1.0, -1.0, 0.0, -1.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["vos"])
    return {"title": vos.title, "composer": vos.composer, "voices": [rows(v) for v in ex], "quarter": q, "bar": vos.bar / 24.0,
            "clips": {"vos": save("vitry.excerpt", s, level=None, detail="Philippe de Vitry, Vos qui admiramini (PMFC 1), bars 1-14 sung from the edition's pitches by four synthetic voices")}}


def compute_census() -> dict:
    book = T.load()
    oo = [MD.on_off_beat(p) for p in book]
    on = {k: float(np.mean([o["on"][k] for o in oo])) for k in ("perfect", "imperfect", "dissonant")}
    off = {k: float(np.mean([o["off"][k] for o in oo])) for k in ("perfect", "imperfect", "dissonant")}
    par = [MD.parallels(p.grid(4)) for p in book]
    par_t = {"parallels": sum(x["parallels"] for x in par), "moves": sum(x["moves"] for x in par)}
    bach = [MD.parallels(c.grid(4)) for c in BC.load()]
    par_b = {"parallels": sum(x["parallels"] for x in bach), "moves": sum(x["moves"] for x in bach)}
    cad = Counter()
    for p in book:
        cad.update(MD.cadences(p))
    fin = Counter(MD.final_sonority(p) for p in book)
    bach_fin = Counter("third" if any((x - min(ch)) % 12 in (3, 4, 8, 9) for x in ch) else "open"
                       for c in BC.load() for ch in [tuple(v[-1][0] for v in c.voices)])
    G = {0, 2, 4, 5, 7, 9, 10, 11}
    n = ch = up = 0
    kinds = Counter()
    for p in book:
        for v in p.voices:
            for i, (q, o, d) in enumerate(v):
                n += 1
                if q % 12 not in G:
                    ch += 1
                    kinds[q % 12] += 1
                    if i + 1 < len(v) and v[i + 1][0] - q == 1:
                        up += 1
    names = {1: "C♯", 3: "E♭", 6: "F♯", 8: "G♯"}
    return {"pieces": len(book), "voices": dict(Counter(len(p.voices) for p in book)), "genres": dict(Counter(p.genre for p in book)),
            "composers": dict(Counter(p.composer for p in book)), "on": on, "off": off,
            "parallels": {"trecento": par_t, "bach": par_b}, "cadences": dict(cad), "finals": dict(fin), "bach_finals": dict(bach_fin),
            "ficta": {"notes": n, "outside": ch, "rising": up, "kinds": {names.get(k, str(k)): v for k, v in kinds.items()}}}


def landini_count(p) -> list:
    top, low = p.voices[0], p.voices[-1]
    hits = []
    for i in range(len(top) - 2):
        a, b, c = top[i][0], top[i + 1][0], top[i + 2][0]
        if c - a == 1 and a - b in (1, 2):
            t = top[i + 2][1]
            lows = [q for q, o, d in low if o <= t < o + d]
            if lows and (c - lows[0]) % 12 == 0:
                hits.append(i)
    return hits


def compute_landini() -> dict:
    book = T.load()
    by, pieces = Counter(), Counter()
    for p in book:
        by[p.composer] += len(landini_count(p))
        pieces[p.composer] += 1
    lan = [p for p in book if p.composer == "Francesco Landini"]
    p = max(lan, key=lambda x: len(landini_count(x)))
    i = landini_count(p)[-1]
    t_end = p.voices[0][i + 2][1] + p.voices[0][i + 2][2]
    start = max(0, (t_end // p.bar) - 4)
    ex = excerpt(p, int(t_end // p.bar - start + 1), start_bar=int(start))
    q = 0.34
    c = sing(ex, q, parts=["alto", "tenor", "bass"][: len(ex)] if len(ex) <= 3 else ["alto", "tenor", "tenor", "bass"],
             gains=[0.0, -1.0, -1.0, 0.0][: len(ex)])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["cadence"])
    top_last = [x for x in ex[0]]
    return {"by_composer": {k: [by[k], pieces[k]] for k in by}, "total": sum(by.values()), "title": p.title, "voices": [rows(v) for v in ex], "quarter": q,
            "top": rows(top_last), "clips": {"landini": save("landini.cadence", s, level=None, detail=f"Francesco Landini, {p.title}: a cadence, sung from the edition's pitches")}}


def compute_cadence() -> dict:
    # E G# C# -> D A D (double leading tone) against E G C -> D A D (plain), over D
    plain = [[(73 - 1, 0, 2), (74, 2, 3)], [(67, 0, 2), (69, 2, 3)], [(64, 0, 2), (62, 2, 3)]]
    double = [[(73, 0, 2), (74, 2, 3)], [(68, 0, 2), (69, 2, 3)], [(64, 0, 2), (62, 2, 3)]]
    unit = 0.55
    cA = sing(double, unit, parts=["alto", "tenor", "bass"])
    cB = sing(plain, unit, parts=["alto", "tenor", "bass"])
    s = concat([cB.at_level(LEVEL), cA.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"A": [rows(v) for v in plain], "B": [rows(v) for v in double], "unit": unit, "starts": {k: float(s.events[k]) for k in "AB"}, "answer": "B",
            "clips": {"quiz": save("cadence.double", s, level=None, detail="a cadence to D: with the upper voices unaltered (C and G) and with both raised a semitone (C-sharp and G-sharp)")}}


def compute_subtilior() -> dict:
    # three voices dividing the same span in 2, 3 and 4 (with a 4:3 against 3:2 in the middle)
    span = 12.0
    voices = []
    for k, (n, base) in enumerate(((3, 74), (4, 69), (2, 62))):
        v, t = [], 0.0
        steps = [0, 2, -1, 1, 0, -2, 1, 0]
        p = base
        for r in range(4):
            for i in range(n):
                d = 3.0 / n
                v.append((p, t, d))
                t += d
                p = MD.diatonic_shift(p, steps[(i + r) % len(steps)]) if p % 12 in MD.WHITE else p + 1
        voices.append(v)
    c = sing(voices, 0.6, parts=["alto", "tenor", "bass"], vowels=["i", "a", "O"])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["proportions"])
    book = T.load()
    var = []
    for p in book:
        durs = Counter(d for v in p.voices for _, _, d in v)
        odd = sum(c for d, c in durs.items() if 24 % d and d % 24 and (d * 2) % 24 and (d * 3) % 24) / sum(durs.values())
        var.append({"title": p.title, "composer": p.composer, "positions": len(durs), "irregular": odd})
    var.sort(key=lambda x: -x["positions"])
    return {"voices": [rows(v) for v in voices], "unit": 0.6, "span": span, "variety": var[:8],
            "median_positions": float(np.median([x["positions"] for x in var])),
            "clips": {"proportions": save("subtilior.proportions", s, level=None, detail="three voices in proportion: three, four and two notes to the same span, ours")}}


def tune_pitches(base: int = 65):
    t = M.corpus([M.THE_TUNE])[0]
    return [base + p for p in t.pitches], list(t.beats)


def compute_tune() -> dict:
    pit, beats = tune_pitches(65)                         # in F, with B-flat: the tritus modes as singers sang them
    first = pit[:14]
    chant = chant_notes(first, ends=(6, 13))
    organ = MD.enchiriadis(first, floor=60, steps=-4)
    org = chant_notes(organ, ends=(6, 13))
    # an isorhythmic motet: the phrase as color in the tenor, a talea of 5, a free voice in the first mode above
    color = [p - 12 for p in first[:7]]
    talea = [3, 2, 1, 3, -3]
    ten = MD.isorhythm(color, talea, repeats=2)
    T_end = max(a + d for _, a, d in ten)
    up, t = [], 0.0
    i = 0
    while t < T_end:
        p = first[i % len(first)]
        under = [x for x, o, d in ten if o <= t < o + d]
        if under and t % 3 == 0:
            p = min((y for y in range(p - 4, p + 5) if (y - under[0]) % 12 in (0, 7)), key=lambda y: abs(y - p))
        d = 2.0 if i % 2 == 0 else 1.0
        up.append((p, t, d))
        t += d
        i += 1
    c1 = sing([chant], 0.4)
    c2 = sing([chant, org], 0.4, parts=["tenor", "bass"])
    c3 = sing([up, ten], 0.24, parts=["tenor", "bass"], gains=[-1.0, 0.0])
    s = concat([c1.at_level(LEVEL), c2.at_level(LEVEL), c3.at_level(LEVEL)], gap=1.2, names=["chant", "organum", "motet"])
    return {"chant": rows(chant), "organum": rows(org), "motet": {"upper": rows(up), "tenor": rows(ten), "unit": 0.24}, "unit": 0.4,
            "color": color, "talea": talea, "meet": MD.periods(len(color), sum(1 for d in talea if d > 0))["lcm"], "seconds": s.duration, "starts": {k: float(s.events[k]) for k in ("chant", "organum", "motet")},
            "clips": {"variation": save("tune.variation23", s, level=None, detail="the Tune's first phrase as chant, as organum at the fifth by the Enchiriadis rule, and as the color of an isorhythmic tenor")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 23, "title": r"as chant, as organum at the fifth below, and as the color of an isorhythmic motet", "seconds": round(t["seconds"], 2),
            "measure": rf"a color of {len(t['color'])} pitches through a talea of {sum(1 for d in t['talea'] if d > 0)} notes: they meet again after {t['meet']} notes",
            "clip": "tune.variation23"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation23", 23)


ITEMS = {"hook": compute_hook, "chant": compute_chant, "guido": compute_guido, "organum": compute_organum, "rhythm": compute_rhythm,
         "notre": compute_notre, "motet": compute_motet, "mensuration": compute_mensuration, "isorhythm": compute_isorhythm,
         "vitry": compute_vitry, "census": compute_census, "landini": compute_landini, "cadence": compute_cadence,
         "subtilior": compute_subtilior, "tune": compute_tune, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
