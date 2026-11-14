"""Precompute everything numerical, and every sound, in Part 40 of *Music, Built* ("The Song").

    python -m videos.music.music40.compute              # everything missing (under a minute)
    python -m videos.music.music40.compute --force drop

Numbers are cached in ``.cache/music40/<name>.json``, sounds in ``.cache/music40/audio/``.  The tools are Monochord's
(``explainer/music/monochord/song.py``); the instruments are Part 38's (piano, plucked bass and guitar, cymbals) with an
acoustic kit from Part 9's membrane and noise, drum-machine voices built from their circuits' principles, additive
pads and sub-bass, and Part 17's model voice, which sings vowels, not words (labelled synthesized).  Every song, riff,
beat and verse is ours; published chart statistics are quoted, not recomputed.

Items:
    hook        a song of ours with a twenty-second intro, then a five-second one (an ear question: when does the voice enter?)
    forms       a 32-bar AABA song of ours, shortened; a verse, pre-chorus and chorus
    loops       three rock loops: I-V-vi-IV, bVII-IV-I, i-bVI-bIII-bVII
    riffs       a rock riff and a funk riff of ours
    beats       rock, funk, disco, house and a half-time trap-style beat
    power       a triad and a power chord through the model amplifier
    tuned       the drum-machine kick tuned to a bass line
    swing16     a funk beat with straight, then swung, sixteenths
    eight       an 808-style kick at three decays; the kit in a pattern
    breaks      a drum break of ours, then chopped, re-sequenced and pitched up
    flow        a verse of ours rapped (on vowels) two ways: on the beat, and in threes against the beat
    drop        a build and a drop; a pad without and with sidechain (an ear question: which pumps?)
    tune        Variation 40: the Tune as a pop single, then a beat that samples Variation 7
    variation   the Variations ledger, row 40
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import blues as BL
from explainer.music.monochord import melody as M
from explainer.music.monochord import song as S
from explainer.music.monochord.audio import ClipStore as _CS
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import drumkit as DK
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38

CACHE = Cache("music40")
CLIPS = ClipStore("music40")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano, bass, guitar = P38.piano, P38.bass, P38.guitar
_C: dict = {}


def cached(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------------------------------------------- instruments
def drive(y, amount=6.0):
    """A guitar amplifier, schematically: soft clipping, then a speaker's band limit."""
    z = np.tanh(amount * y / np.abs(y).max())
    return sosfilt(butter(2, [90, 4500], btype="band", fs=SR, output="sos"), z)


def eguitar(m, seconds=0.4, dist=True):
    y = guitar(m, seconds)
    return cached(("eg", m, round(seconds, 2), dist), lambda: drive(y) if dist else y)


def pad(chord_pcs, seconds, base=60, bright=2500.0):
    """A pad: detuned sawtooth-like tones (additive) on the chord's notes, low-passed, slow attack."""
    def make():
        n = int(seconds * SR)
        t = np.arange(n) / SR
        y = np.zeros(n)
        for p in chord_pcs:
            m = base + (p - base) % 12
            for det in (-0.004, 0.0, 0.004):
                f = hz(m) * (1 + det)
                for k in range(1, 14):
                    if f * k > 6000:
                        break
                    y += np.sin(2 * np.pi * f * k * t + k * det * 50) / k
        y = sosfilt(butter(2, bright, btype="low", fs=SR, output="sos"), y)
        y *= np.clip(t / 0.15, 0, 1) * np.clip((seconds - t) / 0.2, 0, 1)
        return y / np.abs(y).max()
    return cached(("pad", tuple(chord_pcs), round(seconds, 2), base, bright), make)


def sub(m, seconds):
    def make():
        n = int(seconds * SR)
        t = np.arange(n) / SR
        y = np.sin(2 * np.pi * hz(m) * t) + 0.15 * np.sin(4 * np.pi * hz(m) * t)
        return y * np.clip(t / 0.005, 0, 1) * np.clip((seconds - t) / 0.03, 0, 1)
    return cached(("sub", m, round(seconds, 2)), make)


def kick():
    return cached(("kick",), lambda: DK.kick())


def snare(seed=0):
    return P38.snare(seed)


def hat(open_=False):
    return cached(("hat", open_), lambda: DK.hat(0.1, open_=open_, seed=2))


def k808(decay=0.45):
    return cached(("k808", decay), lambda: S.kick808(52.0, decay))


def drums(parts, style, bpm, bars, start=0.0, kit="acoustic", gain=0.0, swing=None):
    p = S.PATTERNS[style]
    step = 60.0 / bpm / 4
    for b in range(bars):
        t0 = start + b * 16 * step
        for s in p["kick"]:
            parts.append((arr(kick() if kit == "acoustic" else k808()), t0 + s * step, -2.0 + gain))
        for s in p["snare"]:
            ghost = s in p.get("ghost", [])
            if kit == "acoustic":
                parts.append((arr(snare(s)), t0 + s * step, (-14.0 if ghost else -5.0) + gain))
            else:
                parts.append((arr(cached(("clap", s % 2), lambda s=s: S.clap808(s % 2))), t0 + s * step, -6.0 + gain))
        for s in p["hat"]:
            h = hat() if kit == "acoustic" else cached(("h808",), lambda: S.hat808())
            parts.append((arr(h), t0 + s * step, (-13.0 if s % 4 else -10.0) + gain))
        for s in p["open"]:
            h = hat(True) if kit == "acoustic" else cached(("h808o",), lambda: S.hat808(True))
            parts.append((arr(h), t0 + s * step, -12.0 + gain))


def sing(notes, part="tenor", vowel="a", seed=0):
    y = CH.sing(notes, part, vowel, seed=seed)
    return y / max(np.abs(y).max(), 1e-9)


def bounce(parts, end):
    return Clip(mix(parts, duration=end).y, SR).at_level(LEVEL)


ROOTS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "Bb": 10, "Eb": 3, "Ab": 8}


def chord_of(sym):
    minor = sym.endswith("m")
    r = ROOTS[sym[:-1] if minor else sym]
    return r, [r, (r + (3 if minor else 4)) % 12, (r + 7) % 12]


def band(parts, chords, bpm, start=0.0, style="rock", strum=True, bass_on=True, drums_on=True, pad_on=False, gain=0.0, kit="acoustic"):
    """One chord a bar: bass on the beats, a strummed (clean) guitar in eighths, drums, optional pad."""
    beat = 60.0 / bpm
    for b, sym in enumerate(chords):
        r, pcs = chord_of(sym)
        t0 = start + b * 4 * beat
        if bass_on:
            for k in range(4):
                parts.append((arr(bass(36 + r if r < 5 else 24 + r, beat * 0.9)), t0 + k * beat, -3.0 + gain))
        if strum:
            notes = sorted(52 + (p - 52) % 12 for p in pcs) + [64 + (pcs[0] - 64) % 12]
            for k in range(8):
                if k in (0, 3, 4, 6):
                    for j, m in enumerate(notes):
                        parts.append((arr(guitar(m, beat * 0.45)), t0 + k * beat / 2 + 0.008 * j, -12.0 + gain))
        if pad_on:
            parts.append((arr(pad(pcs, 4 * beat)), t0, -14.0 + gain))
    if drums_on:
        drums(parts, style, bpm, len(chords), start, kit=kit, gain=gain)


# ---------------------------------------------------------------------------------------------------------- the song
VERSE = [(64, 0, 1), (64, 1, 1), (67, 2, 1), (69, 3, 1.5), (67, 4.5, 0.5), (64, 5, 1), (62, 6, 2),
         (64, 8, 1), (64, 9, 1), (67, 10, 1), (72, 11, 1.5), (71, 12.5, 0.5), (67, 13, 1), (69, 14, 2)]       # ours, in beats
CHORUS = [(72, 0, 1), (72, 1, 0.5), (71, 1.5, 0.5), (72, 2, 2), (74, 4, 1), (72, 5, 1), (69, 6, 2),
          (72, 8, 1), (72, 9, 0.5), (71, 9.5, 0.5), (72, 10, 2), (76, 12, 1), (74, 13, 1), (72, 14, 2)]      # the hook, ours


def voice_line(parts, notes, bpm, start, shift=-12, gain=0.0, part="tenor", vowel="a", seed=0):
    beat = 60.0 / bpm
    y = sing([(m + shift, start + a * beat, d * beat * 0.95) for m, a, d in notes], part, vowel, seed)
    parts.append((arr(y), 0.0, gain))


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    bpm = 96
    beat = 60.0 / bpm
    out, enters = {}, {}
    for name, intro_bars in (("long", 8), ("short", 2)):
        parts = []
        chords = ["C", "Am", "F", "G"] * ((intro_bars + 4) // 4 + 1)
        chords = chords[: intro_bars + 4]
        band(parts, chords, bpm, style="rock")
        t_voice = intro_bars * 4 * beat
        voice_line(parts, VERSE, bpm, t_voice, gain=-1.0)
        enters[name] = t_voice
        out[name] = save_synth(f"hook.{name}", bounce(parts, (intro_bars + 4) * 4 * beat + 1.0),
                               detail=f"a song of ours with a {intro_bars}-bar intro before the voice; guitar, bass, drums and a model voice")
    return {"bpm": bpm, "enters": enters, "answer": {"long": 20, "short": 5}, "clips": out}


def compute_forms() -> dict:
    bpm = 120
    beat = 60.0 / bpm
    # AABA, each section four bars (shortened from eight): A = VERSE's first half, B = a bridge of ours
    A = VERSE[:7]
    B = [(69, 0, 1), (71, 1, 1), (72, 2, 2), (74, 4, 1), (72, 5, 1), (71, 6, 2)]
    plan = [("A", A, ["C", "Am", "F", "G"]), ("A", A, ["C", "Am", "F", "C"]), ("B", B, ["F", "Em", "Dm", "G"]), ("A", A, ["C", "Am", "G", "C"])]
    parts, starts, t = [], [], 0.0
    for name, mel, chords in plan:
        starts.append((name, t))
        for b, sym in enumerate(chords):
            r, pcs = chord_of(sym)
            for m in sorted(55 + (p - 55) % 12 for p in pcs):
                parts.append((arr(piano(m, 3.6 * beat, 0.6)), t + b * 4 * beat, -9.0))
            parts.append((arr(bass(36 + r if r < 5 else 24 + r, 1.8 * beat)), t + b * 4 * beat, -3.0))
            parts.append((arr(bass(36 + r if r < 5 else 24 + r, 1.8 * beat)), t + (b * 4 + 2) * beat, -5.0))
        voice_line(parts, mel, bpm, t, gain=-1.0)
        t += 16 * beat
    c1 = bounce(parts, t + 1.0)
    # verse, pre-chorus, chorus (fuller)
    bpm2 = 100
    beat2 = 60.0 / bpm2
    parts, s2 = [], {}
    s2["verse"] = 0.0
    band(parts, ["Am", "F", "C", "G"], bpm2, 0.0, strum=False, gain=-3.0)
    voice_line(parts, VERSE[:7], bpm2, 0.0, gain=-1.0)
    s2["pre"] = 16 * beat2
    band(parts, ["F", "G"], bpm2, 16 * beat2, gain=-1.0)
    voice_line(parts, [(69, 0, 1), (71, 1, 1), (72, 2, 1), (74, 3, 1), (76, 4, 4)], bpm2, 16 * beat2, gain=-1.0)
    s2["chorus"] = 24 * beat2
    band(parts, ["C", "G", "Am", "F"], bpm2, 24 * beat2, pad_on=True, gain=0.0)
    voice_line(parts, CHORUS[:7], bpm2, 24 * beat2, gain=0.0)
    voice_line(parts, [(m - 5, a, d) for m, a, d in CHORUS[:7]], bpm2, 24 * beat2, part="alto", vowel="O", gain=-5.0, seed=3)
    c2 = bounce(parts, 40 * beat2 + 1.2)
    return {"bpm": bpm, "aaba": [(n, s) for n, s in starts], "bpm2": bpm2, "vc": s2,
            "clips": {"aaba": save_synth("forms.aaba", c1, detail="a 32-bar AABA song of ours, each section shortened to four bars: a model voice, Part 7's piano and bass"),
                      "vc": save_synth("forms.vc", c2, detail="a verse, a pre-chorus and a chorus of ours, the chorus fuller with a second voice and a pad")}}


LOOPS = {"I-V-vi-IV": ["C", "G", "Am", "F"], "bVII-IV-I": ["Bb", "F", "C", "C"], "i-bVI-bIII-bVII": ["Am", "F", "C", "G"]}


def compute_loops() -> dict:
    bpm = 120
    beat = 60.0 / bpm
    parts, starts, t = [], {}, 0.0
    for name, chords in LOOPS.items():
        starts[name] = t
        band(parts, chords * 2, bpm, t)
        t += 8 * 4 * beat + 0.6
    c = bounce(parts, t + 0.6)
    # the melodic-harmonic 'divorce': the chorus hook over I-V-vi-IV, notes on beats that are not in the chord
    loop = LOOPS["I-V-vi-IV"]
    on, out_ = 0, 0
    for m, a, d in CHORUS:
        if abs(a - round(a)) < 1e-9:
            on += 1
            _, pcs = chord_of(loop[int(a // 4) % 4])
            out_ += m % 12 not in pcs
    return {"bpm": bpm, "loops": LOOPS, "starts": starts, "divorce": {"on_beat": on, "outside": out_},
            "clips": {"three": save("loops.three", c, detail="three loops of ours, twice each: I-V-vi-IV in C, bVII-IV-I in C, i-bVI-bIII-bVII in A minor; guitar, bass and drums")}}


ROCK_RIFF = [(40, 0), (43, 2), (45, 3), (40, 4), (43, 6), (46, 7), (45, 8), (43, 10), (40, 12), (38, 14), (40, 15)]   # E minor pentatonic, 16ths
FUNK_RIFF = [(64, 0), (64, 2), (67, 3), (64, 5), (62, 6), (64, 8), (69, 10), (67, 11), (64, 13), (62, 14)]


def compute_riffs() -> dict:
    out = {}
    for name, riff, bpm, style, dist in (("rock", ROCK_RIFF, 110, "rock", True), ("funk", FUNK_RIFF, 100, "funk", False)):
        step = 60.0 / bpm / 4
        parts = []
        for bar in range(4):
            for m, s in riff:
                parts.append((arr(eguitar(m + (12 if name == "rock" else 0), step * (2.5 if name == "rock" else 1.2), dist)), (bar * 16 + s) * step, -4.0))
        drums(parts, style, bpm, 4)
        if name == "funk":
            for bar in range(4):
                for s in (0, 3, 10, 14):
                    parts.append((arr(bass(40 if s != 14 else 43, step * 1.5)), (bar * 16 + s) * step, -2.0))
        out[name] = save(f"riffs.{name}", bounce(parts, 64 * step + 1.0), detail=f"a {name} riff of ours over drums, four bars: plucked-string guitar{' through a model amplifier' if dist else ''}")
    return {"rock": ROCK_RIFF, "funk": FUNK_RIFF, "clips": out}


def compute_power() -> dict:
    """A C major triad and a C power chord (root, fifth, octave), each strummed through the model amplifier."""
    parts, t, starts = [], 0.0, {}
    for name, notes in (("triad", [48, 52, 55, 60, 64]), ("power", [48, 55, 60])):
        starts[name] = t
        for rep in range(2):
            for j, m in enumerate(notes):
                parts.append((arr(guitar(m, 1.4)), t + rep * 1.6 + 0.01 * j, -6.0))
        mixdown = Clip(mix(parts, duration=t + 3.6).y, SR).y
        t += 3.8
    dry = Clip(mix(parts, duration=t).y, SR).y
    wet = drive(dry, 8.0)
    c = Clip(wet / np.abs(wet).max(), SR).at_level(LEVEL)
    return {"starts": starts, "clips": {"two": save("power.two", c, detail="a C major triad, then a C power chord (root, fifth, octave), each strummed twice through the model amplifier")}}


def compute_tuned() -> dict:
    """A long-decay drum-machine kick tuned to each note of a bass line: the kick as the bass."""
    bpm = 90
    step = 60.0 / bpm / 4
    line = [(0, 36), (6, 36), (10, 43), (16, 32), (22, 32), (26, 34), (32, 29), (38, 29), (42, 31), (48, 31), (54, 34), (58, 36)]
    parts = []
    for s, m in line:
        f = hz(m + 12) / 2
        parts.append((arr(cached(("k808t", m), lambda f=f: S.kick808(f, 0.9, seconds=1.6, bend=0.5))), s * step, -1.0))
    drums_parts = []
    p = S.PATTERNS["trap"]
    for bar in range(4):
        for s in p["hat"]:
            parts.append((arr(cached(("h808",), lambda: S.hat808())), (bar * 16 + s) * step, -16.0))
        for s in p["snare"]:
            parts.append((arr(cached(("clap", 0), lambda: S.clap808(0))), (bar * 16 + s) * step, -8.0))
    c = bounce(parts, 64 * step + 1.5)
    return {"bpm": bpm, "line": line, "clips": {"bass": save_synth("tuned.bass", c, detail="a long-decay drum-machine kick tuned to each note of a bass line of ours, with clap and hats")}}


def compute_swing16() -> dict:
    """A funk beat with straight sixteenths, then with the second sixteenth of each pair delayed to 60% of the pair:
    a drum machine's swing setting."""
    bpm = 100
    out, starts, t = [], {}, 0.0
    for name, sw in (("straight", 0.5), ("swung", 0.6)):
        starts[name] = t
        step = 60.0 / bpm / 4
        p = S.PATTERNS["funk"]
        for bar in range(2):
            for kind, ons in (("kick", p["kick"]), ("snare", p["snare"]), ("hat", p["hat"])):
                for s in ons:
                    pair = s // 2
                    pos = (2 * pair + (0 if s % 2 == 0 else 2 * sw)) * step
                    snd = kick() if kind == "kick" else (snare(s) if kind == "snare" else hat())
                    g = {"kick": -2.0, "snare": -14.0 if s in p.get("ghost", []) else -5.0, "hat": -13.0 if s % 2 else -10.0}[kind]
                    out.append((arr(snd), t + bar * 16 * step + pos, g))
        t += 2 * 16 * step + 0.6
    c = bounce(out, t + 0.6)
    return {"bpm": bpm, "swing": 0.6, "starts": starts, "clips": {"two": save("swing16.two", c, detail="a funk beat of ours, two bars with straight sixteenths, two with each off sixteenth delayed to 60% of its pair; acoustic kit models")}}


def compute_beats() -> dict:
    parts, starts, t = [], {}, 0.0
    for style in ("rock", "funk", "disco", "house", "trap"):
        starts[style] = t
        bpm = S.TEMPO[style]
        drums(parts, style, bpm, 2, t, kit="808" if style in ("house", "trap") else "acoustic")
        t += 2 * 4 * 60.0 / bpm + 0.5
    c = bounce(parts, t + 0.6)
    return {"patterns": S.PATTERNS, "tempo": S.TEMPO, "starts": starts, "backbeat": {k: S.backbeat_share(p) for k, p in S.PATTERNS.items()},
            "clips": {"five": save("beats.five", c, detail="two bars each of rock, funk, disco (acoustic kit), house and a half-time trap-style beat (drum-machine voices)")}}


def compute_eight() -> dict:
    parts, t, starts = [], 0.0, []
    for dec in (0.15, 0.45, 1.2):
        starts.append(t)
        for k in range(2):
            parts.append((arr(k808(dec)), t + k * 0.8 * (1 + dec), 0.0))
        t += 1.6 * (1 + dec) + 0.6
    c1 = bounce(parts, t + 1.0)
    bpm = 90
    parts = []
    drums(parts, "trap", bpm, 4, kit="808")
    step = 60.0 / bpm / 4
    for bar in range(4):
        for s, m in ((0, 33), (7, 33), (10, 36)):
            parts.append((arr(sub(m, step * 5)), (bar * 16 + s) * step, -4.0))
    c2 = bounce(parts, 64 * step + 1.0)
    k = S.kick808(52.0, 0.45)
    f, spec = S.hat_spectrum()
    peaks = [float(f[i]) for i in np.argsort(spec)[-12:]]
    return {"decays": [0.15, 0.45, 1.2], "starts": starts, "pitch": S.measured_pitch(k), "pitch_attack": S.measured_pitch(k, 0.0, 0.01),
            "hat_hz": list(S.HAT_HZ), "hat_peaks": sorted(peaks),
            "clips": {"kick": save_synth("eight.kick", c1, detail="a drum-machine kick built as a struck resonator, at three decay settings"),
                      "kit": save_synth("eight.kit", c2, detail="the drum-machine voices in a half-time pattern with a sub-bass, four bars")}}


def compute_breaks() -> dict:
    bpm = 100
    step = 60.0 / bpm / 4
    parts = []
    drums(parts, "funk", bpm, 2)
    brk = Clip(mix(parts, duration=32 * step + 0.3).y, SR).y[: int(32 * step * SR)]
    order = [0, 1, 2, 3, 0, 1, 6, 7, 4, 5, 2, 3, 6, None, 6, 7]
    ch, _ = S.chop(brk, 16, order)
    # pitched up 'as a sampler did': played back 1.2 times faster, by resampling
    idx = np.arange(0, len(ch) - 1, 1.2)
    fast = np.interp(idx, np.arange(len(ch)), ch)
    out = concat([Clip(brk, SR).at_level(LEVEL), Clip(ch, SR).at_level(LEVEL), Clip(fast, SR).at_level(LEVEL)], gap=0.6,
                 names=["break", "chopped", "faster"])
    return {"bpm": bpm, "order": order, "slices": 16, "speed": 1.2, "starts": {k: float(out.events[k]) for k in ("break", "chopped", "faster")},
            "clips": {"three": save("breaks.three", out, detail="a two-bar drum break of ours on the acoustic kit; the same cut into sixteen slices and re-sequenced; then played 1.2 times faster, as a sampler did")}}


# a verse of ours: (syllable, accented, sixteenth from the first bar line, rhyme class)
VERSE_RAP_TEXT = [["I", "kept", "the", "time", "on", "a", "pa", "per", "line"],
                  ["count", "it", "in", "twos", "then", "I", "fold", "it", "in", "nine"],
                  ["the", "beat", "keeps", "walk", "ing", "I", "step", "out", "of", "line"],
                  ["ev", "ery", "bar", "is", "a", "door", "and", "the", "door", "is", "mine"]]


BEAT_STEPS = [[0, 2, 4, 6, 8, 10, 12, 13, 14], [0, 2, 4, 6, 8, 10, 11, 12, 13, 14], [0, 2, 4, 6, 7, 8, 10, 11, 12, 14],
              [0, 1, 2, 4, 6, 8, 10, 11, 12, 13, 14]]
THREE_SLOTS = [0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15]
RHYME = {"time": "A", "line": "A", "nine": "A", "mine": "A", "door": "B"}


def rap_layout(kind: str) -> list:
    """The verse placed two ways: ``beat`` (mostly eighth notes, accents on the beats, every line ending on the last
    eighth) and ``threes`` (sixteenths in a 3+3+3+3+3+1 grouping, accents every three sixteenths against the beat).
    Returns [(syllable, accented, sixteenth from the start, rhyme class)]."""
    out = []
    for bar, words in enumerate(VERSE_RAP_TEXT):
        n = len(words)
        steps = BEAT_STEPS[bar] if kind == "beat" else THREE_SLOTS[:n]
        for k, (w, st) in enumerate(zip(words, steps)):
            last = k == n - 1
            acc = (st % 4 == 0) if kind == "beat" else (st % 3 == 0)
            out.append((w, bool(acc or last), bar * 16 + st, RHYME.get(w)))
    return out


def rap_voice(syll, bpm, start):
    step = 60.0 / bpm / 4
    vowels = {"a": "a", "e": "E", "i": "I", "o": "O", "u": "U"}
    notes = []
    for k, (w, acc, s, r) in enumerate(syll):
        m = 50 + (3 if acc else 0) - (2 if r else 0)
        dur = step * (1.6 if acc else 1.1)
        notes.append((m, start + s * step, dur))
    y = CH.sing(notes, "tenor", "a", seed=4, glide=0.02, vibrato=0.0, depth=0.0)
    return y / max(np.abs(y).max(), 1e-9)


def compute_flow() -> dict:
    bpm = 90
    step = 60.0 / bpm / 4
    out, layouts, stats = {}, {}, {}
    for kind in ("beat", "threes"):
        syll = rap_layout(kind)
        layouts[kind] = [list(x) for x in syll]
        stats[kind] = S.flow(syll, 4)
        parts = [(arr(rap_voice(syll, bpm, 0.0)), 0.0, 0.0)]
        drums(parts, "trap", bpm, 4, kit="808", gain=-6.0)
        out[kind] = save_synth(f"flow.{kind}", bounce(parts, 64 * step + 1.0),
                               detail=("a verse of ours rapped on the eighth notes" if kind == "beat" else "the same verse placed in threes against the beat") + "; a model voice on vowels over drum-machine voices")
    pro_good = [("BEAU", True, 0), ("ti", False, 2), ("ful", False, 3), ("DAY", True, 4)]
    pro_bad = [("beau", False, 0), ("TI", True, 2), ("FUL", True, 3), ("day", False, 5)]
    return {"bpm": bpm, "layouts": layouts, "stats": stats, "prosody": {"good": S.prosody(pro_good), "bad": S.prosody(pro_bad)},
            "text": VERSE_RAP_TEXT, "clips": out}


def compute_drop() -> dict:
    bpm = 126
    beat = 60.0 / bpm
    step = beat / 4
    parts = []
    # build: four bars, snare in quarters, eighths, sixteenths, thirty-seconds; a noise riser; the pad's filter opening
    rng = np.random.default_rng(9)
    for bar, div in enumerate((4, 8, 16, 32)):
        for k in range(div):
            parts.append((arr(snare(k)), (bar * 4 + k * 4 / div) * beat, -9.0 + 2 * bar))
    n = int(16 * beat * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    riser = np.zeros(n)
    for k, (a, b) in enumerate(zip(np.linspace(400, 6000, 16), np.linspace(800, 9000, 16))):
        seg = slice(k * n // 16, (k + 1) * n // 16)
        riser[seg] = sosfilt(butter(2, [a, b], btype="band", fs=SR, output="sos"), noise[seg])
    riser *= np.linspace(0.1, 1.0, n)
    parts.append((arr(riser / np.abs(riser).max()), 0.0, -14.0))
    for bar, (sym, br) in enumerate(zip(["Am", "F", "C", "G"], (600, 1200, 2400, 4800))):
        parts.append((arr(pad(chord_of(sym)[1], 4 * beat, bright=br)), bar * 4 * beat, -12.0))
    t_drop = 16 * beat
    # drop: four bars, four-on-the-floor kick, sub bass, a sidechained pad
    hits = [t_drop + k * beat for k in range(16)]
    for h in hits:
        parts.append((arr(k808(0.3)), h, -1.0))
    drums(parts, "house", bpm, 4, t_drop, kit="808", gain=-4.0)
    padline = np.concatenate([pad(chord_of(s)[1], 4 * beat, bright=4000) for s in ["Am", "F", "C", "G"]])
    ducked, _ = S.sidechain(padline, [h - t_drop for h in hits], depth_db=14.0)
    parts.append((arr(ducked), t_drop, -8.0))
    for bar, sym in enumerate(["Am", "F", "C", "G"]):
        r = chord_of(sym)[0]
        for k in range(4):
            parts.append((arr(sub(33 + (r - 9) % 12, beat * 0.45)), t_drop + (bar * 4 + k + 0.5) * beat, -5.0))
    c = bounce(parts, t_drop + 16 * beat + 1.0)
    # the pad alone, without and then with the sidechain, under the kick
    two, st2 = [], {}
    for k, depth in enumerate((0.0, 14.0)):
        t0 = k * (8 * beat + 0.8)
        st2[("plain", "ducked")[k]] = t0
        line = np.concatenate([pad(chord_of(s)[1], 4 * beat, bright=4000) for s in ["Am", "F"]])
        hh = [j * beat for j in range(8)]
        y, g = S.sidechain(line, hh, depth_db=depth) if depth else (line, np.ones(len(line)))
        two.append((arr(y), t0, -6.0))
        for h in hh:
            two.append((arr(k808(0.3)), t0 + h, -4.0))
    c2 = bounce(two, 2 * (8 * beat + 0.8) + 0.6)
    _, gshape = S.sidechain(np.ones(int(2 * beat * SR)), [0.0, beat], depth_db=14.0)
    return {"bpm": bpm, "t_drop": t_drop, "starts2": st2, "answer": "second", "gain_shape": [float(x) for x in gshape[:: SR // 100]],
            "clips": {"drop": save_synth("drop.build", c, detail="a four-bar build of ours (snare doubling, a noise riser, a pad opening) and a four-bar drop: drum-machine kick, sub-bass, a sidechained pad"),
                      "two": save_synth("drop.two", c2, detail="a pad under a steady kick, first plain, then sidechained 14 dB: additive pad, drum-machine kick")}}


def tune_line(n=14, base=72):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


def compute_tune() -> dict:
    bpm = 104
    beat = 60.0 / bpm
    mel = tune_line(14, 72)
    p1 = [(m, a, d) for m, a, d in mel[:7]]
    p2 = [(m, a - 8, d) for m, a, d in mel[7:]]
    parts = []
    # intro (two bars), verse: the Tune's second phrase low over Am F C G, twice; chorus: its first phrase as the hook
    band(parts, ["Am", "F"], bpm, 0.0, strum=False, drums_on=False, pad_on=True, gain=-3.0)
    tv = 8 * beat
    band(parts, ["Am", "F", "C", "G"] * 2, bpm, tv, strum=False, gain=-3.0)
    voice_line(parts, [(m - 7, a * 2, d * 2) for m, a, d in p2], bpm, tv, gain=-1.0)
    voice_line(parts, [(m - 7, a * 2, d * 2) for m, a, d in p2], bpm, tv + 16 * beat, gain=-1.0)
    tc = tv + 32 * beat
    hits = [tc + k * beat for k in range(32)]
    band(parts, ["C", "G", "Am", "F"] * 2, bpm, tc, gain=0.0)
    padline = np.concatenate([pad(chord_of(s)[1], 4 * beat, bright=4000) for s in ["C", "G", "Am", "F"] * 2])
    ducked, _ = S.sidechain(padline, [h - tc for h in hits], depth_db=10.0)
    parts.append((arr(ducked), tc, -12.0))
    voice_line(parts, [(m, a * 2, d * 2) for m, a, d in p1], bpm, tc, gain=0.0)
    voice_line(parts, [(m, a * 2, d * 2) for m, a, d in p1], bpm, tc + 16 * beat, gain=0.0)
    voice_line(parts, [(m - 4 if m % 12 != 0 else m - 3, a * 2, d * 2) for m, a, d in p1], bpm, tc + 16 * beat, part="alto", vowel="O", gain=-5.0, seed=6)
    end1 = tc + 32 * beat + 1.0
    c1 = Clip(mix(parts, duration=end1).y, SR).at_level(LEVEL)
    # a beat that samples Variation 7: its recording cut into sixteen slices and re-sequenced over drum-machine voices
    v7 = _CS("music7").load("tune.variation7")
    src = v7.mono if not callable(getattr(v7, "mono", None)) else v7.mono()
    src = np.asarray(src, float)
    src = src[: int(12.0 * SR)]
    bpm2 = 90
    step = 60.0 / bpm2 / 4
    order = [0, None, 0, 1, 4, None, 5, 5, 0, None, 0, 1, 8, 9, None, 3]
    ch, slices = S.chop(src, 16, order, slice_len=4 * step)
    loop = np.concatenate([ch, ch])
    parts = [(arr(loop / np.abs(loop).max()), 0.0, -4.0)]
    drums(parts, "trap", bpm2, 8, kit="808", gain=-3.0)
    for bar in range(8):
        for s, m in ((0, 36), (10, 31)):
            parts.append((arr(sub(m, step * 5)), (bar * 16 + s) * step, -6.0))
    c2 = Clip(mix(parts, duration=128 * step + 1.0).y, SR).at_level(LEVEL)
    s_ = concat([c1, c2], gap=1.0, names=["single", "beat"])
    return {"bpm": bpm, "melody": [list(x) for x in mel], "verse_at": tv, "chorus_at": tc, "voice_enters": tv,
            "bpm2": bpm2, "order": order, "slice_starts": slices, "starts": {k: float(s_.events[k]) for k in ("single", "beat")},
            "seconds": s_.duration,
            "clips": {"variation": save_synth("tune.variation40", s_, detail="the Tune as a pop single of ours (its second phrase as the verse, its first as the chorus hook, a sidechained pad), then a beat built from sixteen slices of Variation 7's recording over drum-machine voices")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 40, "title": "as a pop single, then as a beat that samples Variation 7", "seconds": round(t["seconds"], 1),
            "measure": f"the voice enters after {t['voice_enters']:.1f} s; the beat: 16 slices of Variation 7, {sum(1 for x in t['order'] if x is None)} rests",
            "clip": "tune.variation40"}


ITEMS = {"hook": compute_hook, "forms": compute_forms, "loops": compute_loops, "riffs": compute_riffs, "beats": compute_beats,
         "eight": compute_eight, "power": compute_power, "tuned": compute_tuned, "swing16": compute_swing16, "breaks": compute_breaks, "flow": compute_flow, "drop": compute_drop, "tune": compute_tune,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
