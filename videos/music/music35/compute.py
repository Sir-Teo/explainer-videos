"""Precompute everything numerical, and every sound, in Part 35 of *Music, Built* ("Maqam").

    python -m videos.music.music35.compute              # everything missing (under a minute)
    python -m videos.music.music35.compute --force ajnas

Numbers are cached in ``.cache/music35/<name>.json``, sounds in ``.cache/music35/audio/``.  The maqam engine is
Monochord's (``explainer/music/monochord/maqam.py``).  The oud is a plucked string retuned to exact pitches through
Part 7's guitar body; the darbuka is Part 9's membrane.  Every phrase is ours.

Items:
    hook        C with three thirds: 300, 400 and 350 cents (an ear question: which is Rast's?)
    ajnas       the eight common ajnas, each up and down on the oud
    maqamat     Rast, Bayati, Hijaz and Saba, each up and down on the oud
    neutral     medieval ratios for the neutral intervals; their errors in 24 and 53 equal steps
    safi        Safi al-Din's seventeen-tone gamut by a chain of fourths
    turkish     Rast in Arel-Ezgi-Uzdilek commas against the Arabic 24-step Rast (an ear question: which third is higher?)
    iqa         maqsum, baladi, samai thaqil and aksak on the darbuka (an ear question: which cycle has ten beats?)
    taqsim      a short taqsim of ours in Bayati, touching Saba and returning
    tonics      jins Bayati on D, G and A, heard
    descent     Rast up with B half-flat and down with B flat, heard
    thirds3     three neutral thirds over C: 350 (24 steps), 355 (Zalzal), 362 (16 of 53), heard
    ehalf       an illustration (values ours) of E half-flat placed higher in a Rast phrase than in a Bayati phrase, heard
    baladi      maqsum and baladi, which differ in one stroke, heard
    mandal      one qanun-style course lowered by lever steps: E, -25, -50, -75, -100 cents, heard
    hijaz       a second short taqsim of ours, in Hijaz on D
    koron       a phrase of ours in the Persian manner with one koron note (E lowered about a quarter tone)
    saba        Saba climbing: where the octave would be, D flat, heard
    ney         jins Bayati on a ney-like breathy tone
    tune        Variation 35: a taqsim opening, then the Tune in Rast, Bayati and Hijaz over maqsum
    variation   the Variations ledger, row 35
"""

from __future__ import annotations

from math import log2

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import maqam as Q
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import saver

CACHE = Cache("music35")
CLIPS = ClipStore("music35")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C3 = 130.8127826502993
_O: dict = {}
_D: dict = {}


def arr(y):
    return Clip(np.asarray(y, float), SR)


def oudc(c: float, seconds: float = 1.0, base: float = C3 * 2):
    """The oud at ``c`` cents above ``base``."""
    key = (round(c, 2), round(seconds, 2), base)
    if key not in _O:
        _O[key] = Q.oud(base * 2 ** (c / 1200), seconds)
    return _O[key]


def drum(s):
    if s not in _D:
        _D[s] = Q.darbuka(s)
    return _D[s]


def line(cents_seq, unit=0.38, last=1.2, base=C3 * 2, start=0.0, level=0.0):
    parts, t = [], start
    for i, c in enumerate(cents_seq):
        d = unit if i < len(cents_seq) - 1 else last
        parts.append((arr(oudc(c, max(d, 0.6) + 0.4, base)), t, level))
        t += d
    return parts, t


def updown(sc):
    return list(sc) + list(reversed(sc[:-1]))


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    order = [300.0, 400.0, 350.0]
    clips = []
    for c in order:
        parts = [(arr(oudc(0, 1.4)), 0.0, 0.0), (arr(oudc(c, 1.4)), 0.7, 0.0), (arr(oudc(0, 1.8)), 1.6, -2.0), (arr(oudc(c, 1.8)), 1.6, -2.0)]
        p2, t = line([0, 200, c, 500, c, 200, 0], unit=0.32, last=1.0, start=3.6)
        clips.append(Clip(mix(parts + p2, duration=t + 1.2).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=list("ABC"))
    return {"order": order, "answer": "C", "starts": {k: float(s_.events[k]) for k in "ABC"},
            "clips": {"quiz": save("hook.quiz", s_, detail="C on the oud with three different thirds, 300, 400 and 350 cents, each alone, together, and in the phrase C D third F third D C; a plucked string through Part 7's guitar body")}}


def compute_ajnas() -> dict:
    names = ["Rast", "Bayati", "Sikah", "Hijaz", "Saba", "Nahawand", "Kurd", "Ajam"]
    clips, times = [], {}
    for n in names:
        p, t = line(updown(Q.AJNAS[n]), unit=0.3, last=0.9)
        clips.append(Clip(mix(p, duration=t + 0.9).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.6, names=names)
    return {"names": names, "ajnas": {n: Q.AJNAS[n] for n in names}, "starts": {n: float(s_.events[n]) for n in names}, "unit": 0.3,
            "clips": {"eight": save("ajnas.eight", s_, detail="eight ajnas from C, each up and down: Rast, Bayati, Sikah, Hijaz, Saba, Nahawand, Kurd, Ajam; the oud model")}}


def compute_maqamat() -> dict:
    names = ["Rast", "Bayati", "Hijaz", "Saba"]
    bases = {"Rast": C3 * 2, "Bayati": C3 * 2 * 2 ** (2 / 12), "Hijaz": C3 * 2 * 2 ** (2 / 12), "Saba": C3 * 2 * 2 ** (2 / 12)}
    clips, scales = [], {}
    for n in names:
        sc = Q.maqam_scale(n)
        p, t = line(updown(sc), unit=0.3, last=1.0, base=bases[n])
        clips.append(Clip(mix(p, duration=t + 0.9).y, SR).at_level(LEVEL))
        scales[n] = sc
    s_ = concat(clips, gap=0.8, names=names)
    return {"names": names, "scales": scales, "tonics": {"Rast": "C", "Bayati": "D", "Hijaz": "D", "Saba": "D"},
            "starts": {n: float(s_.events[n]) for n in names}, "unit": 0.3, "def": {k: list(v) for k, v in Q.MAQAMAT.items()},
            "clips": {"four": save("maqamat.four", s_, detail="maqam Rast on C, and Bayati, Hijaz and Saba on D, each up and down; the oud model")}}


def compute_neutral() -> dict:
    fr = Q.farabi_ratios()
    rows_ = []
    for k, c in fr.items():
        k24, e24 = Q.edo_error(c, 24)
        k53, e53 = Q.edo_error(c, 53)
        rows_.append({"name": k, "cents": c, "e24": e24, "e53": e53, "k24": k24, "k53": k53})
    return {"rows": rows_}


def compute_safi() -> dict:
    s17 = Q.safi_17()
    steps = [round(b - a, 1) for a, b in zip(s17, s17[1:] + [1200.0])]
    return {"notes": s17, "steps": steps, "kinds": sorted(set(steps))}


def compute_turkish() -> dict:
    tr = Q.turkish_rast()
    ar = Q.maqam_scale("Rast")
    clips = []
    for sc in (ar, tr["cents"]):
        p, t = line(updown(sc[:5]), unit=0.34, last=0.6)
        p2 = [(arr(oudc(0, 2.0)), t + 0.2, -2.0), (arr(oudc(sc[2], 2.0)), t + 0.2, -2.0), (arr(oudc(sc[4], 2.0)), t + 0.2, -2.0)]
        clips.append(Clip(mix(p + p2, duration=t + 2.4).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=["A", "B"])
    return {"arabic": ar, "turkish": tr, "answer": "B", "starts": {k: float(s_.events[k]) for k in "AB"},
            "third": {"arabic": ar[2], "turkish": tr["cents"][2]},
            "clips": {"quiz": save("turkish.quiz", s_, detail="the lower half of Rast up and down, then C, its third and G together: A with the Arabic 24-step third (350 cents), B with the Turkish 17-comma third (385 cents); the oud model")}}


def compute_iqa() -> dict:
    order = ["maqsum", "samai thaqil", "aksak"]
    beat = 0.24
    clips = []
    for name in order:
        st = Q.IQAAT[name]["strokes"]
        parts = []
        for cyc in range(3):
            for i, s in enumerate(st):
                if s:
                    parts.append((arr(drum(s)), (cyc * len(st) + i) * beat, 0.0 if s == "dum" else -3.0))
        parts.append((arr(drum("dum")), 3 * len(st) * beat, 0.0))
        clips.append(Clip(mix(parts, duration=(3 * len(st) + 1) * beat + 0.8).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=list("ABC"))
    return {"order": order, "iqaat": {k: v for k, v in Q.IQAAT.items()}, "beat": beat, "answer": "B",
            "starts": {k: float(s_.events[k]) for k in "ABC"},
            "clips": {"quiz": save("iqa.quiz", s_, detail="three rhythmic cycles on the darbuka, three times round each: maqsum (8), samai thaqil (10), aksak (9); dum at the centre, tek at the rim; Part 9's membrane")}}


def compute_taqsim() -> dict:
    base = C3 * 2 * 2 ** (2 / 12)                                     # D
    bay = Q.maqam_scale("Bayati")
    saba = Q.maqam_scale("Saba")
    # (cents, seconds): free rhythm; dwell on the tonic and the fourth, touch Saba's lowered fourth, return
    phrase = [(0, 0.9), (150, 0.3), (300, 0.3), (500, 1.1), (300, 0.25), (150, 0.25), (300, 0.6), (150, 0.3), (0, 1.3),
              (300, 0.3), (400, 0.9), (300, 0.25), (150, 0.25), (300, 0.3), (400, 0.3), (700, 1.0), (400, 0.35), (300, 0.3), (150, 0.3), (0, 0.6),
              (150, 0.3), (300, 0.3), (500, 0.7), (300, 0.3), (150, 0.4), (0, 1.8)]
    parts, t, times = [], 0.0, []
    for c, d in phrase:
        parts.append((arr(oudc(c, max(d, 0.6) + 0.4, base)), t, 0.0))
        times.append(t)
        t += d
    s_ = concat([Clip(mix(parts, duration=t + 1.0).y, SR).at_level(LEVEL)], gap=0.0, names=["taqsim"])
    return {"phrase": phrase, "times": times, "bayati": bay, "saba": saba, "saba_from": 9, "saba_to": 19,
            "clips": {"taqsim": save("taqsim.bayati", s_, detail="a short taqsim of ours on the oud in Bayati on D, moving into Saba's lowered fourth (G flat) and back; free rhythm")}}


def compute_tonics() -> dict:
    tonics = {"D": 2, "G": 7, "A": 9}
    clips = []
    for k, st in tonics.items():
        p, t = line(updown(Q.AJNAS["Bayati"]), unit=0.3, last=0.9, base=C3 * 2 * 2 ** (st / 12))
        clips.append(Clip(mix(p, duration=t + 0.9).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.6, names=list(tonics))
    return {"tonics": tonics, "starts": {k: float(s_.events[k]) for k in tonics}, "jins": Q.AJNAS["Bayati"],
            "clips": {"three": save("tonics.three", s_, detail="jins Bayati up and down on D, on G and on A; the oud model")}}


def compute_descent() -> dict:
    up = Q.maqam_scale("Rast")
    down = [1200, 1000, 900, 700, 500, 350, 200, 0]
    p, t = line(up + down[1:], unit=0.3, last=1.2)
    s_ = concat([Clip(mix(p, duration=t + 1.0).y, SR).at_level(LEVEL)], gap=0.0, names=["rast"])
    return {"up": up, "down": down, "unit": 0.3,
            "clips": {"updown": save("descent.updown", s_, detail="maqam Rast on C up with B half-flat (1050 cents) and down with B flat (1000), as often played; the oud model")}}


def compute_thirds3() -> dict:
    cs = [350.0, 1200 * log2(27 / 22), 16 * 1200 / 53]
    clips = []
    for c in cs:
        parts = [(arr(oudc(0, 1.6)), 0.0, 0.0), (arr(oudc(c, 1.6)), 0.6, 0.0), (arr(oudc(0, 2.0)), 1.5, -2.0), (arr(oudc(c, 2.0)), 1.5, -2.0)]
        clips.append(Clip(mix(parts, duration=3.8).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=0.6, names=["24", "zalzal", "53"])
    return {"cents": cs, "starts": {k: float(s_.events[k]) for k in ("24", "zalzal", "53")},
            "clips": {"three": save("thirds3.three", s_, detail="C with three neutral thirds: 350 cents (24 equal steps), 355 (Zalzal's 27/22), 362 (16 of 53 equal steps); the oud model")}}


def compute_ehalf() -> dict:
    # values chosen for illustration of a reported tendency, not measurements
    rast = [0, 200, 360, 500, 360, 200, 0]
    bay = [200, 340, 500, 340, 200]                                    # Bayati on D, written above C
    p1, t1 = line(rast, unit=0.4, last=1.0)
    p2, t2 = line(bay, unit=0.4, last=1.0)
    s_ = concat([Clip(mix(p1, duration=t1 + 0.9).y, SR).at_level(LEVEL), Clip(mix(p2, duration=t2 + 0.9).y, SR).at_level(LEVEL)], gap=0.8, names=["rast", "bayati"])
    return {"rast": rast, "bayati": bay, "starts": {k: float(s_.events[k]) for k in ("rast", "bayati")}, "unit": 0.4,
            "clips": {"two": save("ehalf.two", s_, detail="an illustration with values of ours: a Rast phrase on C with E half-flat at 360 cents, then a Bayati phrase on D with the same note at 340; the oud model")}}


def compute_baladi() -> dict:
    beat = 0.24
    clips = []
    for name in ("maqsum", "baladi"):
        st = Q.IQAAT[name]["strokes"]
        parts = []
        for cyc in range(3):
            for i, s_ in enumerate(st):
                if s_:
                    parts.append((arr(drum(s_)), (cyc * 8 + i) * beat, 0.0 if s_ == "dum" else -3.0))
        clips.append(Clip(mix(parts, duration=24 * beat + 0.8).y, SR).at_level(LEVEL))
    s2 = concat(clips, gap=1.0, names=["maqsum", "baladi"])
    return {"beat": beat, "starts": {k: float(s2.events[k]) for k in ("maqsum", "baladi")},
            "strokes": {k: Q.IQAAT[k]["strokes"] for k in ("maqsum", "baladi")},
            "clips": {"two": save("baladi.two", s2, detail="maqsum, then baladi, three cycles each, differing in the second stroke (tek or dum); Part 9's membrane")}}


def compute_mandal() -> dict:
    steps = [400, 375, 350, 325, 300]
    parts, t = [], 0.0
    for c in steps:
        parts.append((arr(oudc(0, 1.0)), t, -2.0))
        parts.append((arr(oudc(c, 1.0)), t + 0.45, 0.0))
        t += 1.2
    s_ = concat([Clip(mix(parts, duration=t + 0.8).y, SR).at_level(LEVEL)], gap=0.0, names=["mandal"])
    return {"steps": steps, "step_time": 1.2,
            "clips": {"levers": save("mandal.levers", s_, detail="C, then the third above it lowered a lever at a time: 400, 375, 350, 325 and 300 cents; the oud model standing in for a qanun course")}}


def free_line(phrase, base):
    parts, t, times = [], 0.0, []
    for c, d in phrase:
        parts.append((arr(oudc(c, max(d, 0.6) + 0.4, base)), t, 0.0))
        times.append(t)
        t += d
    return Clip(mix(parts, duration=t + 1.0).y, SR), times


def compute_hijaz() -> dict:
    base = C3 * 2 * 2 ** (2 / 12)
    phrase = [(0, 0.9), (100, 0.3), (400, 0.9), (500, 0.4), (400, 0.3), (100, 0.3), (0, 1.1), (400, 0.3), (500, 0.3), (700, 1.0),
              (800, 0.3), (700, 0.3), (500, 0.3), (400, 0.6), (100, 0.4), (0, 1.8)]
    c, times = free_line(phrase, base)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["hijaz"])
    return {"phrase": phrase, "times": times,
            "clips": {"taqsim": save("hijaz.taqsim", s_, detail="a short taqsim of ours on the oud in Hijaz on D, free rhythm; the oud model")}}


def compute_koron() -> dict:
    base = C3 * 2 * 2 ** (2 / 12)                                     # on D
    phrase = [(0, 0.6), (150, 0.5), (300, 0.5), (500, 0.9), (300, 0.4), (150, 0.4), (0, 0.5), (-200, 0.5), (0, 1.6)]
    c, times = free_line(phrase, base)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["koron"])
    return {"phrase": phrase, "times": times,
            "clips": {"phrase": save("koron.phrase", s_, detail="a phrase of ours on D in the Persian manner, with one koron note (E lowered about a quarter tone, written 150 cents above D); the oud model")}}


def compute_saba() -> dict:
    base = C3 * 2 * 2 ** (2 / 12)
    sc = [0, 150, 300, 400, 700, 800, 1000, 1100]                     # one common form: where the octave D would be, D flat
    p, t = line(sc, unit=0.36, last=1.4, base=base)
    s_ = concat([Clip(mix(p, duration=t + 1.0).y, SR).at_level(LEVEL)], gap=0.0, names=["saba"])
    return {"scale": sc, "unit": 0.36,
            "clips": {"up": save("saba.up", s_, detail="maqam Saba on D climbing in one common form, reaching D flat (1100 cents) where the octave D would be; the oud model")}}


def compute_ney() -> dict:
    rng = np.random.default_rng(35)
    base = C3 * 2 * 2 ** (2 / 12)
    seq = updown(Q.AJNAS["Bayati"])
    parts, t = [], 0.0
    from scipy.signal import butter, sosfilt
    for c in seq:
        f = base * 2 ** (c / 1200)
        n = int(0.55 * SR)
        tt = np.arange(n) / SR
        tone = sum((0.5 ** k) * np.sin(2 * np.pi * f * (k + 1) * tt) for k in range(4))
        noise = sosfilt(butter(2, [f * 0.8, f * 4], btype="band", fs=SR, output="sos"), rng.standard_normal(n)) * 0.6
        env = np.minimum(1, tt / 0.08) * np.minimum(1, (0.55 - tt) / 0.1)
        parts.append((Clip((tone + noise) * env, SR), t, 0.0))
        t += 0.5
    from explainer.music.monochord import EXAMPLE_LEVEL as _E
    s_ = concat([Clip(mix(parts, duration=t + 0.6).y, SR).at_level(LEVEL)], gap=0.0, names=["ney"])
    return {"seq": seq,
            "clips": {"bayati": save("ney.bayati", s_, kind="synthesized", detail="jins Bayati up and down on D on a breathy, ney-like tone: four harmonics and band-limited noise")}}


DEG = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}


def compute_tune() -> dict:
    t = M.corpus([M.THE_TUNE])[0]
    mel = list(zip(t.pitches, t.beats))[:14]
    beat = 0.3
    out, clips = {}, []
    # a short taqsim opening in Rast
    rast = Q.maqam_scale("Rast")
    op = [(0, 0.8), (200, 0.3), (350, 0.9), (500, 0.3), (700, 1.0), (500, 0.3), (350, 0.3), (200, 0.3), (0, 1.4)]
    parts, tt = [], 0.0
    for c, d in op:
        parts.append((arr(oudc(c, max(d, 0.6) + 0.4)), tt, 0.0))
        tt += d
    clips.append(Clip(mix(parts, duration=tt + 0.8).y, SR).at_level(LEVEL))
    for name, base in (("Rast", C3 * 2), ("Bayati", C3 * 2 * 2 ** (2 / 12)), ("Hijaz", C3 * 2 * 2 ** (2 / 12))):
        sc = Q.maqam_scale(name)
        parts, a = [], 0.0
        cs = []
        for p, d in mel:
            c = sc[DEG[p % 12]] + 1200 * (p // 12)
            parts.append((arr(oudc(c, d * beat + 0.4, base)), a * beat, 0.0))
            cs.append(c)
            a += d
        st = Q.IQAAT["maqsum"]["strokes"]
        n_beats = int(a)
        for i in range(n_beats * 2):                                  # maqsum at two strokes per beat
            s = st[i % 8]
            if s:
                parts.append((arr(drum(s)), i * beat / 2, -8.0 if s == "dum" else -11.0))
        clips.append(Clip(mix(parts, duration=a * beat + 1.0).y, SR).at_level(LEVEL))
        out[name] = cs
    s_ = concat(clips, gap=0.8, names=["taqsim", "Rast", "Bayati", "Hijaz"])
    changed = {k: sum(1 for p, _ in mel if abs(Q.maqam_scale(k)[DEG[p % 12]] - [0, 200, 400, 500, 700, 900, 1100][DEG[p % 12]]) > 1) for k in out}
    return {"opening": op, "melodies": out, "beat": beat, "starts": {k: float(s_.events[k]) for k in ("taqsim", "Rast", "Bayati", "Hijaz")},
            "changed": changed, "seconds": s_.duration, "notes": [[p, float(d)] for p, d in mel],
            "clips": {"variation": save("tune.variation35", s_, detail="a short taqsim of ours in Rast, then the Tune's first two phrases in Rast on C, Bayati on D and Hijaz on D, over maqsum on the darbuka; the oud model and Part 9's membrane")}}


def compute_variation() -> dict:
    t = load("tune")
    ch = t["changed"]
    return {"part": 35, "title": "in Rast, Bayati and Hijaz, after a taqsim", "seconds": round(t["seconds"], 1),
            "measure": f"of 14 notes, {ch['Rast']} move off the piano's keys in Rast, {ch['Bayati']} change in Bayati, {ch['Hijaz']} in Hijaz",
            "clip": "tune.variation35"}


ITEMS = {"hook": compute_hook, "ajnas": compute_ajnas, "maqamat": compute_maqamat, "neutral": compute_neutral, "safi": compute_safi,
         "turkish": compute_turkish, "iqa": compute_iqa, "taqsim": compute_taqsim, "tonics": compute_tonics, "descent": compute_descent,
         "thirds3": compute_thirds3, "ehalf": compute_ehalf, "baladi": compute_baladi, "mandal": compute_mandal, "hijaz": compute_hijaz, "koron": compute_koron,
         "saba": compute_saba, "ney": compute_ney, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
