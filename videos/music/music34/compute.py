"""Precompute everything numerical, and every sound, in Part 34 of *Music, Built* ("Raga and Tala").

    python -m videos.music.music34.compute              # everything missing (a minute)
    python -m videos.music.music34.compute --force tanpura

Numbers are cached in ``.cache/music34/<name>.json``, sounds in ``.cache/music34/audio/``.  The models are Monochord's
(``explainer/music/monochord/raga.py``): a tanpura string over a curved bridge by finite differences, tabla strokes by
modal synthesis from Part 9's loaded membrane, and melodic lines as synthesized bowed-string tones following pitch
contours.  Every phrase is ours, written in the manner of the ragas named; no recording is played.

Items:
    hook        a cycle of Teentaal on the tabla, then a tihai whose last stroke falls on sam, over the drone
    tanpura     the four tanpura strings with and without the curved bridge; brightness over time
    shruti      the twenty-two shrutis as just ratios against twelve equal steps
    ga          Ga against the drone, tempered and just (an ear question: which beats?)
    raga        Bilawal and Yaman: ascent, descent and a characteristic phrase each, over the drone (an ear question)
    gamaka      a phrase plain and with meend and andolan; the pitch contour and its histogram
    thaat       the 32 scales of Bhatkhande's scheme and his ten thaats; the 72 melakartas
    tala        Teentaal, Jhaptaal and Rupak, one cycle each on the tabla
    tihai       every tihai in Teentaal from a given beat; a bedam and a dumdar tihai, heard (an ear question)
    dronema     the drone tuned Ma, Sa, Sa, low Sa (for ragas without Pa), against the usual Pa tuning, heard
    comma       two Res over the drone, 9/8 and 10/9, a syntonic comma apart, heard
    bhupali     raga Bhupali (pentatonic) over the drone, heard
    kampita     a phrase in the Carnatic manner, its notes oscillating (kampita), heard
    thaats3     one phrase in three thaats: Bilawal, Kalyan, Bhairav, heard
    adi         Adi tala counted by hand: clap, three finger counts, clap-wave, clap-wave, heard
    chakkardar  tihais of tihais in Teentaal that land on sam, solved
    jhala       a jhala: melody notes alternating with the drone strings, accelerating, heard
    tune        Variation 34: the Tune's scale as Bilawal: an alap over the drone, then a gat in Teentaal ending in a tihai
    variation   the Variations ledger, row 34
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord import raga as R
from explainer.music.monochord.partkit import saver, signoff

CACHE = Cache("music34")
CLIPS = ClipStore("music34")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
SA = 130.8127826502993                                              # C3 as Sa
_J: dict = {}
_S: dict = {}


def arr(y):
    return Clip(np.asarray(y, float), SR)


def hz(st: float) -> float:
    return SA * 2 ** (st / 12)


def jaw(f, bridge=True, seconds=3.0):
    key = (round(f, 3), bridge, seconds)
    if key not in _J:
        _J[key] = R.jawari_string(f, seconds, bridge=bridge)
    return _J[key]


def bol(b, seconds=0.6):
    key = (b, seconds)
    if key not in _S:
        _S[key] = R.stroke(b, seconds=seconds)
    return _S[key]


def drone(seconds: float, bridge=True, gap=0.85, level=-8.0):
    """The tanpura's cycle Pa, Sa, Sa, low Sa, repeated for ``seconds``."""
    strings = [hz(-5), hz(0), hz(0), hz(-12)]
    parts, t, i = [], 0.0, 0
    while t < seconds:
        f = strings[i % 4]
        parts.append((arr(jaw(f, bridge)), t, level))
        t += gap if i % 4 != 3 else gap * 1.6
        i += 1
    return mix(parts, duration=seconds + 0.2).y


def tabla_line(bols, beat, start=0.0, level=0.0):
    parts = []
    for i, b in enumerate(bols):
        if b:
            parts.append((arr(bol(b, min(0.6, beat * 1.8))), start + i * beat, level))
    return parts


def melody_voice(notes, glide=0.1, shake=None, rate=200):
    """notes: [(semitones above Sa, seconds), ...]; a synthesized bowed-string-like line."""
    c = R.gamaka_contour(notes, rate=rate, glide=glide, shake=shake)
    return R.voice_from_contour(c, SA * 2, rate=rate), c


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    beat = 0.32
    theka = R.TALAS["Teentaal"]["theka"]
    p, g, start = 3, 2, 5                                            # dha-ti-dha, gaps of two beats, from beat 5
    sol = R.tihai(16, start, phrase_lengths=[p], gaps=[g])[0]
    parts = tabla_line(theka, beat)
    t2 = 16 * beat
    parts += tabla_line(theka[:start - 1], beat, start=t2)
    phrase = ["dha", "ti", "dha"]
    starts, pos = [], start - 1
    for k in range(3):
        starts.append(pos)
        lv = [1.5, 1.5, 4.0] if k == 2 else [1.5, 1.5, 1.5]
        for i, bb in enumerate(phrase):
            parts.append((arr(bol(bb, 0.6 if not (k == 2 and i == 2) else 0.9)), t2 + (pos + i) * beat, lv[i]))
        pos += p + g
    sam = t2 + 16 * beat
    total = sam + 1.6
    d = drone(total)
    y = mix(parts + [(Clip(d, SR), 0.0, -6.0)], duration=total).y
    s_ = concat([Clip(y, SR).at_level(LEVEL)], gap=0.0, names=["hook"])
    return {"beat": beat, "theka": theka, "tihai": sol, "start": start, "phrase": phrase, "starts": starts, "sam": sam,
            "clips": {"tihai": save("hook.tihai", s_, detail="a cycle of Teentaal's theka, then four beats and a tihai of dha-ti-dha three times with gaps of two beats, its last stroke on sam, over the tanpura drone; tabla by modal synthesis, tanpura by a string over a curved bridge")}}


def compute_tanpura() -> dict:
    out = {}
    clips = []
    for key, b in (("plain", False), ("jawari", True)):
        y = jaw(SA, b)
        ts, cs = R.centroid_track(y)
        out[key] = {"t": ts[::2].tolist(), "centroid": cs[::2].tolist()}
        clips.append(arr(y).at_level(LEVEL))
    cyc = arr(drone(8.0)).at_level(LEVEL)
    s_ = concat(clips + [cyc], gap=0.6, names=["plain", "jawari", "cycle"])
    at = {k: {str(q): float(np.interp(q, out[k]["t"], out[k]["centroid"])) for q in (0.1, 0.3, 1.0, 2.0)} for k in out}
    return {**out, "at": at, "starts": {k: float(s_.events[k]) for k in ("plain", "jawari", "cycle")}, "strings": ["Pa (low)", "Sa", "Sa", "Sa (lower octave)"],
            "clips": {"three": save("tanpura.three", s_, detail="one string at C3 on a sharp bridge, then on a curved bridge (the jawari), then the four-string cycle Pa, Sa, Sa, low Sa; a string by finite differences with a one-sided contact")}}


def compute_shruti() -> dict:
    rows_ = []
    for r in R.SHRUTIS:
        c = R.cents(r)
        rows_.append({"ratio": f"{r.numerator}/{r.denominator}", "cents": c, "nearest_et": round(c / 100) * 100, "diff": c - round(c / 100) * 100})
    return {"rows": rows_, "n": len(rows_)}


def compute_ga() -> dict:
    seconds = 4.0
    clips = []
    for c in (400.0, 386.3137):
        d = drone(seconds, level=-10.0)
        v, _ = melody_voice([(c / 100, seconds - 0.4)], glide=0.0)
        y = mix([(Clip(d, SR), 0.0, -4.0), (Clip(v, SR), 0.2, 0.0)], duration=seconds).y
        clips.append(Clip(y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=["A", "B"])
    return {"cents": [400.0, 386.3137], "answer": "A", "beat_hz": float(abs(hz(4.0) * 2 - hz(3.863137) * 2) * 0 + abs(5 * hz(0) * 2 - 4 * hz(4) * 2)),
            "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save_synth("ga.quiz", s_, detail="Ga held over the tanpura drone: A at 400 cents (equal temperament), B at 386 cents (5:4); a synthesized bowed tone over the modelled tanpura")}}


def phrase_notes(sts, unit=0.45, last=1.2):
    return [(s, unit if i < len(sts) - 1 else last) for i, s in enumerate(sts)]


def compute_raga() -> dict:
    out = {}
    clips = []
    order = ["Bilawal", "Yaman"]
    for name in order:
        r = R.RAGAS[name]
        notes = phrase_notes(r["aroha"]) + phrase_notes(r["avaroha"]) + phrase_notes(r["pakad"], unit=0.5, last=1.6)
        v, cont = melody_voice(notes, glide=0.08)
        dur = len(v) / SR
        d = drone(dur + 0.5, level=-12.0)
        y = mix([(Clip(d, SR), 0.0, -6.0), (Clip(v, SR), 0.3, 0.0)], duration=dur + 0.6).y
        clips.append(Clip(y, SR).at_level(LEVEL))
        out[name] = {"aroha": r["aroha"], "avaroha": r["avaroha"], "pakad": r["pakad"], "thaat": r["thaat"], "time": r["time"],
                     "lengths": [len(r["aroha"]), len(r["avaroha"]), len(r["pakad"])]}
    s_ = concat(clips, gap=1.2, names=["A", "B"])
    return {"ragas": out, "order": order, "answer": "B", "starts": {k: float(s_.events[k]) for k in "AB"}, "unit": 0.45,
            "clips": {"quiz": save_synth("raga.quiz", s_, detail="our phrases in the manner of two ragas over the drone: A in Bilawal (ascent, descent, a characteristic phrase), B in Yaman with its raised Ma; a synthesized bowed tone over the modelled tanpura")}}


def compute_gamaka() -> dict:
    sts = [0, 2, 4, 5, 4, 2, 4, 2, 0]
    notes = [(s, 0.7) for s in sts]
    plain, c1 = melody_voice(notes, glide=0.0)
    orn, c2 = melody_voice(notes, glide=0.28, shake={2: (0.6, 4.5), 5: (0.8, 3.5), 6: (0.5, 5.0)})
    clips = []
    for v in (plain, orn):
        dur = len(v) / SR
        d = drone(dur + 0.5, level=-12.0)
        clips.append(Clip(mix([(Clip(d, SR), 0.0, -6.0), (Clip(v, SR), 0.3, 0.0)], duration=dur + 0.6).y, SR).at_level(LEVEL))
    s_ = concat(clips, gap=1.0, names=["plain", "gamaka"])
    # an alap of our own, with gamakas, for the histogram
    alap = [(0, 1.6), (-1, 0.8), (2, 1.2), (4, 1.8), (2, 0.8), (4, 1.0), (5, 1.4), (4, 1.2), (2, 0.8), (0, 2.0), (7, 1.6), (9, 1.0), (7, 1.4),
            (5, 0.8), (4, 1.6), (2, 0.8), (0, 2.4)]
    ca = R.gamaka_contour(alap, glide=0.3, shake={3: (0.5, 3.0), 6: (0.7, 3.5), 11: (0.6, 4.0), 14: (0.5, 3.0)})
    cents, hist = R.pitch_histogram(ca)
    return {"plain": c1[::4].tolist(), "gamaka": c2[::4].tolist(), "rate": 50, "starts": {k: float(s_.events[k]) for k in ("plain", "gamaka")},
            "hist_cents": cents.tolist(), "hist": hist.tolist(), "peaks": sorted({int(round(c / 100.0)) % 12 for c, h in zip(cents, hist) if h > hist.max() * 0.3}),
            "clips": {"two": save_synth("gamaka.two", s_, detail="one phrase of ours twice over the drone: as plain notes, then with meend (glides) and andolan (slow oscillation); a synthesized bowed tone over the modelled tanpura")}}


def compute_thaat() -> dict:
    space = R.thaat_space()
    th = {k: list(v) for k, v in R.THAATS.items()}
    melas = R.melakartas()
    nums = {k: R.melakarta_number(v) for k, v in R.THAATS.items()}
    return {"space": [list(s) for s in space], "thaats": th, "in_space": all(tuple(v) in space for v in th.values()),
            "n_space": len(space), "n_mela": len(melas), "thaat_melas": nums, "names": {str(k): v for k, v in R.MELA_NAMES.items()}}


def compute_tala() -> dict:
    clips = []
    out = {}
    beat = 0.36
    for name in ("Teentaal", "Jhaptaal", "Rupak"):
        t = R.TALAS[name]
        parts = tabla_line(t["theka"], beat) + tabla_line(t["theka"][:1], beat, start=len(t["theka"]) * beat)
        clips.append(Clip(mix(parts, duration=(len(t["theka"]) + 1) * beat + 0.8).y, SR).at_level(LEVEL))
        out[name] = {"beats": t["beats"], "vibhags": t["vibhags"], "marks": t["marks"], "theka": t["theka"]}
    s_ = concat(clips, gap=0.9, names=["Teentaal", "Jhaptaal", "Rupak"])
    return {"talas": out, "beat": beat, "starts": {k: float(s_.events[k]) for k in ("Teentaal", "Jhaptaal", "Rupak")},
            "adi": R.TALAS["Adi"],
            "clips": {"three": save("tala.three", s_, detail="the thekas of Teentaal (16 beats), Jhaptaal (10) and Rupak (7), one cycle each and the next sam; tabla strokes by modal synthesis from Part 9's loaded membrane")}}


def compute_tihai() -> dict:
    sols = {str(st): R.tihai(16, st, phrase_lengths=range(1, 9), gaps=range(0, 5)) for st in (1, 3, 5, 9)}
    beat = 0.3
    theka = R.TALAS["Teentaal"]["theka"]
    clips, plans = [], {}
    for key, (p, g, start) in (("A", (5, 0, 3)), ("B", (3, 2, 5))):
        ok = R.tihai(16, start, phrase_lengths=[p], gaps=[g])
        phrase = ["dha", "ti", "ta", "ti", "dha"] if p == 5 else ["dha", "ti", "dha"]
        parts = tabla_line(theka, beat) + tabla_line(theka[:start - 1], beat, start=16 * beat)
        pos = start - 1
        for k in range(3):
            parts += tabla_line(phrase, beat, start=(16 + pos) * beat, level=1.5)
            pos += p + g
        clips.append(Clip(mix(parts, duration=32 * beat + 1.4).y, SR).at_level(LEVEL))
        plans[key] = {"p": p, "g": g, "start": start, "valid": bool(ok), "phrase": phrase}
    s_ = concat(clips, gap=1.0, names=["A", "B"])
    return {"solutions": sols, "plans": plans, "beat": beat, "answer": "B", "starts": {k: float(s_.events[k]) for k in "AB"},
            "clips": {"quiz": save("tihai.quiz", s_, detail="two tihais in Teentaal, each after a cycle of theka, each ending on sam: A a five-stroke phrase three times without gaps from beat 3 (bedam), B a three-stroke phrase with gaps of two beats from beat 5 (dumdar); tabla by modal synthesis")}}


def drone_with(first: float, seconds: float, gap=0.85, level=-8.0):
    strings = [hz(first), hz(0), hz(0), hz(-12)]
    parts, t, i = [], 0.0, 0
    while t < seconds:
        parts.append((arr(jaw(strings[i % 4])), t, level))
        t += gap if i % 4 != 3 else gap * 1.6
        i += 1
    return mix(parts, duration=seconds + 0.2).y


def compute_dronema() -> dict:
    a = arr(drone_with(-5, 7.0)).at_level(LEVEL)
    b = arr(drone_with(-7, 7.0)).at_level(LEVEL)
    s_ = concat([a, b], gap=1.0, names=["pa", "ma"])
    return {"starts": {k: float(s_.events[k]) for k in ("pa", "ma")}, "tunings": {"pa": "Pa, Sa, Sa, low Sa", "ma": "Ma, Sa, Sa, low Sa"},
            "clips": {"two": save("dronema.two", s_, detail="the tanpura cycle tuned Pa, Sa, Sa, low Sa, then Ma, Sa, Sa, low Sa; a string over a curved bridge")}}


def compute_comma() -> dict:
    seconds = 3.6
    clips = []
    for c in (203.91, 182.40):
        d = drone(seconds, level=-10.0)
        v, _ = melody_voice([(c / 100, seconds - 0.4)], glide=0.0)
        clips.append(Clip(mix([(Clip(d, SR), 0.0, -4.0), (Clip(v, SR), 0.2, 0.0)], duration=seconds).y, SR).at_level(LEVEL))
    alt = []
    for k in range(4):
        v, _ = melody_voice([((203.91 if k % 2 == 0 else 182.40) / 100, 0.9)], glide=0.0)
        alt.append(Clip(v, SR).at_level(LEVEL))
    s_ = concat(clips + [concat(alt, gap=0.15)], gap=0.8, names=["9/8", "10/9", "both"])
    return {"cents": [203.91, 182.40], "diff": 21.51, "starts": {k: float(s_.events[k]) for k in ("9/8", "10/9", "both")},
            "clips": {"three": save_synth("comma.three", s_, detail="Re at 9/8 (204 cents) over the drone, then at 10/9 (182 cents), then the two alternating alone; a synthesized bowed tone over the modelled tanpura")}}


def compute_bhupali() -> dict:
    r = R.RAGAS["Bhupali"]
    notes = phrase_notes(r["aroha"]) + phrase_notes(r["avaroha"]) + phrase_notes(r["pakad"], unit=0.5, last=1.6)
    v, _ = melody_voice(notes, glide=0.1, shake={len(r["aroha"]) + len(r["avaroha"]) + 0: (0.3, 3.0)})
    dur = len(v) / SR
    d = drone(dur + 0.5, level=-12.0)
    y = mix([(Clip(d, SR), 0.0, -6.0), (Clip(v, SR), 0.3, 0.0)], duration=dur + 0.6).y
    s_ = concat([Clip(y, SR).at_level(LEVEL)], gap=0.0, names=["bhupali"])
    return {"aroha": r["aroha"], "avaroha": r["avaroha"], "pakad": r["pakad"], "unit": 0.45,
            "clips": {"phrase": save_synth("bhupali.phrase", s_, detail="our ascent, descent and phrase in the manner of raga Bhupali (S R G P D) over the drone; a synthesized bowed tone over the modelled tanpura")}}


def compute_kampita() -> dict:
    sts = [0, 2, 3, 5, 7, 5, 3, 2, 0]
    notes = [(s, 0.75) for s in sts]
    shake = {i: (1.0 if s in (3, 5) else 0.6, 5.5) for i, s in enumerate(sts) if s not in (0, 7)}
    v, c = melody_voice(notes, glide=0.18, shake=shake)
    dur = len(v) / SR
    d = drone(dur + 0.5, level=-12.0)
    y = mix([(Clip(d, SR), 0.0, -6.0), (Clip(v, SR), 0.3, 0.0)], duration=dur + 0.6).y
    s_ = concat([Clip(y, SR).at_level(LEVEL)], gap=0.0, names=["kampita"])
    return {"notes": sts, "contour": c[::4].tolist(), "rate": 50,
            "clips": {"phrase": save_synth("kampita.phrase", s_, detail="a phrase of ours in the manner of Carnatic singing (S R g m P m g R S), with oscillation (kampita) on most notes, over the drone; a synthesized bowed tone over the modelled tanpura")}}


def compute_thaats3() -> dict:
    phrase = [0, 1, 2, 3, 4, 3, 2, 1, 0]                               # scale degrees 1..5 and back, then up to 8
    out, clips = {}, []
    for name in ("Bilawal", "Kalyan", "Bhairav"):
        sc = R.THAATS[name]
        sts = [sc[k] for k in phrase] + [sc[4], sc[5], sc[6], 12]
        notes = phrase_notes(sts, unit=0.36, last=1.2)
        v, _ = melody_voice(notes, glide=0.05)
        dur = len(v) / SR
        d = drone(dur + 0.4, level=-12.0)
        clips.append(Clip(mix([(Clip(d, SR), 0.0, -6.0), (Clip(v, SR), 0.2, 0.0)], duration=dur + 0.5).y, SR).at_level(LEVEL))
        out[name] = sts
    s_ = concat(clips, gap=0.9, names=["Bilawal", "Kalyan", "Bhairav"])
    return {"phrases": out, "starts": {k: float(s_.events[k]) for k in out}, "unit": 0.36,
            "clips": {"three": save_synth("thaats3.three", s_, detail="one phrase of ours in the scales of three thaats: Bilawal, Kalyan, Bhairav; a synthesized bowed tone over the modelled tanpura")}}


def clap(seconds=0.12, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(int(seconds * SR)) / SR
    y = rng.standard_normal(len(t)) * np.exp(-t * 60)
    from scipy.signal import butter, sosfilt
    y = sosfilt(butter(2, [800, 3500], btype="band", fs=SR, output="sos"), y)
    return y / np.abs(y).max()


def compute_adi() -> dict:
    beat = 0.5
    acts = ["clap", "finger", "finger", "finger", "clap", "wave", "clap", "wave"]
    parts = []
    for cyc in range(2):
        for i, a in enumerate(acts):
            t = (cyc * 8 + i) * beat
            if a == "clap":
                parts.append((Clip(clap(seed=i), SR), t, 0.0))
            elif a == "finger":
                parts.append((Clip(clap(0.05, seed=10 + i) * 0.25, SR), t, -10.0))
            else:
                parts.append((Clip(clap(0.08, seed=20 + i) * 0.12, SR), t, -14.0))
    parts.append((Clip(clap(seed=99), SR), 16 * beat, 0.0))
    c = Clip(mix(parts, duration=16 * beat + 0.8).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["adi"])
    return {"acts": acts, "beat": beat,
            "clips": {"adi": save_synth("adi.hands", s_, detail="Adi tala kept by hand, twice round: a clap and three finger counts, then clap and wave, clap and wave; filtered noise bursts")}}


def compute_chakkardar() -> dict:
    sols = []
    for start in (1, 3, 5, 9):
        s0 = start - 1
        for p in range(1, 7):
            for g1 in range(0, 3):
                for g2 in range(0, 4):
                    span = 3 * (3 * p + 2 * g1) + 2 * g2
                    end = s0 + span - 1
                    if end > s0 and end % 16 == 0 and end // 16 <= 3:
                        sols.append({"start": start, "p": p, "g1": g1, "g2": g2, "span": span, "cycles": end // 16})
    return {"solutions": sols, "count": len(sols)}


def compute_jhala() -> dict:
    sts = [0, 2, 4, 7, 9, 7, 4, 2, 0, 4, 7, 12, 9, 7, 4, 0]
    unit0, unit1 = 0.36, 0.17
    parts, t = [], 0.0
    n = len(sts)
    for i, s in enumerate(sts):
        u = unit0 + (unit1 - unit0) * i / (n - 1)
        v, _ = melody_voice([(s, u * 0.9)], glide=0.0)
        parts.append((Clip(v, SR), t, 0.0))
        for k in range(3):
            parts.append((arr(jaw(hz(12), seconds=0.6)), t + u * (k + 1) / 4, -8.0))
        t += u
    total = t + 1.0
    d = drone(total, level=-14.0)
    parts.append((Clip(d, SR), 0.0, -8.0))
    c = Clip(mix(parts, duration=total).y, SR)
    s_ = concat([c.at_level(LEVEL)], gap=0.0, names=["jhala"])
    return {"notes": sts, "unit0": unit0, "unit1": unit1,
            "clips": {"jhala": save_synth("jhala.fast", s_, detail="a jhala of ours: each melody note followed by three strokes on a high drone string, accelerating; a synthesized bowed tone and the modelled string over the tanpura")}}


def tune_notes(n=14):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((p, a, float(d)))
        a += d
    return out


def compute_tune() -> dict:
    mel = tune_notes(14)
    # 1. an alap: the Tune's first phrase, slow and free, with glides, over the drone
    alap_notes = [(0, 1.8), (0, 0.6), (7, 2.0), (9, 1.2), (7, 1.6), (5, 0.9), (4, 1.4), (2, 0.9), (0, 2.6)]
    va, ca = melody_voice(alap_notes, glide=0.3, shake={2: (0.5, 3.0), 6: (0.5, 3.5)})
    alap_dur = len(va) / SR
    # 2. a gat in Teentaal: the Tune's first two phrases, a beat a quarter note, with the theka, then a tihai
    beat = 0.36
    theka = R.TALAS["Teentaal"]["theka"]
    gat_start = alap_dur + 0.8
    notes = [(p, d * beat * 0.95) for p, a, d in mel]
    vg, cg = melody_voice(notes, glide=0.05)
    n_beats = int(sum(d for _, _, d in mel))                       # 16 beats: one cycle
    parts = [(Clip(va, SR), 0.4, 0.0), (Clip(vg, SR), gat_start, 0.0)]
    parts += tabla_line(theka, beat, start=gat_start, level=-3.0)
    # second cycle: theka to beat 4, then the tihai dha-ti-dha with gaps of 2 from beat 5, its last stroke on sam
    t2 = gat_start + 16 * beat
    parts += tabla_line(theka[:4], beat, start=t2, level=-3.0)
    pos = 4
    tihai_notes = []
    for k in range(3):
        parts += tabla_line(["dha", "ti", "dha"], beat, start=t2 + pos * beat, level=-1.0)
        tihai_notes += [(4, beat), (2, beat), (0, beat), (None, 2 * beat)] if k < 2 else [(4, beat), (2, beat), (0, 1.6)]
        pos += 5
    seq = [(p if p is not None else 0, d) for p, d in tihai_notes]
    vt, _ = melody_voice([(p, d * 0.95) for p, d in seq], glide=0.04)
    # silence the rests
    k = 0
    tt = 0.0
    for p, d in tihai_notes:
        if p is None:
            vt[int(tt * SR):int((tt + d) * SR)] = 0.0
        tt += d
    parts.append((Clip(vt, SR), t2 + 4 * beat, 0.0))
    sam = t2 + 16 * beat
    total = sam + 2.0
    d = drone(total, level=-12.0)
    parts.append((Clip(d, SR), 0.0, -6.0))
    y = mix(parts, duration=total).y
    s_ = concat([Clip(y, SR).at_level(LEVEL)], gap=0.0, names=["tune"])
    return {"alap": alap_notes, "alap_dur": alap_dur, "gat_start": gat_start, "beat": beat, "melody": [[p, a, d] for p, a, d in mel],
            "sam": sam, "tihai_start": t2 + 4 * beat, "n_beats": n_beats, "seconds": s_.duration,
            "clips": {"variation": save_synth("tune.variation34", s_, detail="the Tune's scale as Bilawal: an alap on its first phrase over the drone, then its first two phrases as a gat in Teentaal with the tabla, a tihai, and Sa on sam; synthesized bowed tone, modelled tanpura and tabla")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 34, "title": "as Bilawal: an alap over the drone, then a gat in Teentaal with a tihai", "seconds": round(t["seconds"], 1),
            "measure": "alap of 9 notes; a gat of 16 beats; tihai 3 + 2 + 3 + 2 + 3 beats from beat 5, its last stroke on sam",
            "clip": "tune.variation34"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation34", 34)


ITEMS = {"hook": compute_hook, "tanpura": compute_tanpura, "shruti": compute_shruti, "ga": compute_ga, "raga": compute_raga,
         "gamaka": compute_gamaka, "thaat": compute_thaat, "tala": compute_tala, "tihai": compute_tihai, "dronema": compute_dronema, "comma": compute_comma, "bhupali": compute_bhupali,
         "kampita": compute_kampita, "thaats3": compute_thaats3, "adi": compute_adi, "chakkardar": compute_chakkardar, "jhala": compute_jhala,
         "tune": compute_tune,
         "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
