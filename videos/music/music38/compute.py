"""Precompute everything numerical, and every sound, in Part 38 of *Music, Built* ("Blues and Swing").

    python -m videos.music.music38.compute              # everything missing (several minutes: the pianos)
    python -m videos.music.music38.compute --force swing

Numbers are cached in ``.cache/music38/<name>.json``, sounds in ``.cache/music38/audio/``.  The tools are Monochord's
(``explainer/music/monochord/blues.py``).  Sounds: Part 7's piano (a struck string on a soundboard), Part 35's retuned
plucked string for bass and guitar, Part 17's model voice, modal models for the ride cymbal, and additive horns
(labelled synthesized).  *Maple Leaf Rag* (Joplin, 1899) is played from its encoding in the music21 corpus; every
other line, riff and lyric is ours.

Items:
    hook        a line of ours swung at 120 beats a minute (an ear question: how long is the long note against the short?)
    form        a twelve-bar blues of ours in C: piano, walking bass, ride and hi-hat
    blue        one phrase three ways: a minor third, a major third, and a third bent between them
    callresp    an AAB blues of ours: a model voice answered by a guitar
    rag         Maple Leaf Rag, bars 1-16 from the encoding; then bars 1-4 right hand, left hand, both
    swing       the ride pattern at 100, 180 and 260 beats a minute, swung by the model
    delay       a line over the rhythm section with its downbeats on time, then 30 ms late (illustrative)
    jitter      the same line exactly on the model's grid, then with random timing deviations (sd 15 ms)
    band        a riff chart of ours: saxophones' riff answered by brass over the rhythm section
    walking     the walking-bass generator over a jazz blues: bass and ride, then with piano
    guide       guide tones through ii-V-I and the jazz blues
    subs        ii-V-I and ii-bII7-I (an ear question: which bass moves by semitones?); a turnaround
    tune        Variation 38: the Tune as a twelve-bar blues, as a rag, and as a riff chart
    variation   the Variations ledger, row 38
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import blues as BL
from explainer.music.monochord import maqam as Q
from explainer.music.monochord import melody as M
from explainer.music.monochord import romantic as R
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import drumkit as DK
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music38")
CLIPS = ClipStore("music38")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
BOARD = STR.soundboard()
C4 = 261.6255653005986
_C: dict = {}


def hz(m):
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def arr(y):
    return Clip(np.asarray(y, float), SR)


def cached(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


# ---------------------------------------------------------------------------------------------------- instruments
def piano(m, seconds, velocity=1.0):
    seconds = round(min(max(seconds, 0.15), 2.5) * 4) / 4
    vel = round(velocity, 1)

    def make():
        f = hz(m)
        force = np.asarray(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4),
                                      velocity=vel, seconds=seconds + 0.3), float)
        r = int(0.08 * SR)                               # the damper: the string's force dies away over 80 ms, not in a click
        force[-r:] *= np.linspace(1.0, 0.0, r) ** 2
        y = BOARD.play(force)
        return Clip(np.asarray(y, float)).fade(0.001, 0.15).y
    return cached(("piano", m, seconds, vel), make)


def _cut(y, seconds, release=0.06):
    n = min(len(y), int((seconds + release) * SR))
    out = np.array(y[:n], float)
    r = int(release * SR)
    out[-r:] *= np.linspace(1.0, 0.0, r)
    return out


def bass(m, seconds=0.6):
    """A plucked string (Part 35's retuned Karplus-Strong through Part 7's body), rendered once per pitch and damped
    after ``seconds``, as a bassist's hand stops the string."""
    y = cached(("bass", m), lambda: Q.oud(hz(m), 1.8))
    return _cut(y, min(max(seconds, 0.15), 1.7))


def guitar(m, seconds=0.5):
    y = cached(("guitar", m), lambda: Q.oud(hz(m), 1.8))
    return _cut(y, min(max(seconds, 0.15), 1.7), 0.1)


RIDE_MODES = [(420, 1.0, 1.2), (1130, 0.7, 1.5), (2210, 0.55, 1.9), (3390, 0.5, 2.3), (4620, 0.45, 2.8), (5870, 0.4, 3.2),
              (7160, 0.35, 3.8), (8400, 0.3, 4.4), (9730, 0.25, 5.0), (11050, 0.2, 5.8)]


def ride(accent=False):
    """A ride cymbal: a plate's inharmonic modes by modal synthesis (designed, dense in the treble), with a stick's
    click."""
    def make():
        rng = np.random.default_rng(3)
        fs, amps, decs = [], [], []
        for f, a, d in RIDE_MODES:
            for k in range(4):
                fs.append(f * (1 + 0.03 * rng.standard_normal()))
                amps.append(a * (0.6 + 0.4 * rng.random()))
                decs.append(d * (0.8 + 0.4 * rng.random()))
        y = PC.modal(fs, amps, decs, 1.4, SR)
        n = len(y)
        t = np.arange(n) / SR
        click = sosfilt(butter(2, 5000, btype="high", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t * 90)
        y = y / np.abs(y).max() + 0.4 * click / np.abs(click).max()
        return y / np.abs(y).max()
    y = cached(("ride",), make)
    return y if accent else y * 0.75


def hat():
    return cached(("hat",), lambda: DK.hat(0.08, seed=4))


def snare(seed=0):
    def make():
        rng = np.random.default_rng(60 + seed)
        n = int(0.25 * SR)
        t = np.arange(n) / SR
        nz = sosfilt(butter(2, [1500, 8000], btype="band", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t * 22)
        y = 0.6 * nz / np.abs(nz).max() + 0.5 * PC.drum(190.0, 0.25, at=0.6, damping=20.0)[:n]
        return y / np.abs(y).max()
    return cached(("snare", seed % 2), make)


def horn(m, seconds, kind="sax"):
    """Additive horns (synthesized): a brass tone whose upper harmonics enter after the attack, or a reedy tone with
    breath."""
    seconds = round(min(max(seconds, 0.1), 2.0) * 8) / 8

    def make():
        f = hz(m)
        n = int((seconds + 0.12) * SR)
        t = np.arange(n) / SR
        y = np.zeros(n)
        for k in range(1, 16):
            if f * k > 9000:
                break
            if kind == "brass":
                a = k ** -1.1 * (1 - np.exp(-t / (0.012 + 0.004 * k)))
            else:
                a = k ** -1.3 * (1.0 if k % 2 else 0.6) * (1 - np.exp(-t / 0.02))
            y += a * np.sin(2 * np.pi * f * k * t + 0.3 * k)
        vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - 0.25) / 0.3, 0, 1)
        y = y * vib
        env = np.clip(t / 0.02, 0, 1) * np.clip((seconds + 0.12 - t) / 0.08, 0, 1)
        if kind == "sax":
            rng = np.random.default_rng(int(m))
            br = sosfilt(butter(2, [2000, 6000], btype="band", fs=SR, output="sos"), rng.standard_normal(n))
            y = y + 0.04 * br / np.abs(br).max() * np.abs(y).max()
        y = y * env
        return y / np.abs(y).max()
    return cached(("horn", kind, m, seconds), make)


def sing(notes, part="tenor", vowel="a", seed=0):
    y = CH.sing(notes, part, vowel, seed=seed, glide=0.06)
    return y / max(np.abs(y).max(), 1e-9)


# ---------------------------------------------------------------------------------------------------- the rhythm section
RIDE_PATTERN = [0, 2, 3, 4, 6, 7]                 # eighths in a bar: ding, ding-a ding, ding-a


def rhythm_section(parts, changes, bpm, start=0.0, ride_on=True, hat_on=True, bass_on=True, comp=True, ratio=None,
                   bass_line=None, gain=0.0, bars=None):
    """Walking bass, ride and hi-hat, and piano comping (shell voicings on beats 2 and 4, or Charleston), from a list
    of bars of chord symbols."""
    beat = 60.0 / bpm
    nb = len(changes) if bars is None else bars
    seq = BL.beats_of(changes)
    wb = bass_line or BL.walking_bass(changes)
    if bass_on:
        for i in range(nb * 4):
            parts.append((arr(bass(wb[i % len(wb)], beat * 0.95)), start + i * beat, -2.0 + gain))
    if ride_on:
        for b in range(nb):
            ts = BL.swing_times(RIDE_PATTERN, bpm, ratio) + start + b * 4 * beat
            for j, t in enumerate(ts):
                parts.append((arr(ride(RIDE_PATTERN[j] % 4 == 2)), t, -16.0 + gain))
    if hat_on:
        for b in range(nb):
            for k in (1, 3):
                parts.append((arr(hat()), start + (b * 4 + k) * beat, -18.0 + gain))
    if comp:
        gt = BL.guide_tones(seq[: nb * 4], lo=55, hi=70)
        for i in range(nb * 4):
            if i % 4 in (1, 3):
                vel = 0.7 if i % 4 == 1 else 0.6
                t = start + i * beat
                for m in (gt["upper"][i], gt["lower"][i]):
                    parts.append((arr(piano(m, beat * 0.6, vel)), t, -9.0 + gain))
    return wb


def bounce(parts, end):
    return Clip(mix(parts, duration=end).y, SR).at_level(LEVEL)


def tune_line(n=14, base=72):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


# ---------------------------------------------------------------------------------------------------------- items
HOOK_LINE = [(72, 0), (74, 1), (75, 2), (76, 3), (79, 4), (76, 5), (74, 6), (72, 7),
             (70, 8), (72, 9), (67, 10), (69, 11), (70, 12), (72, 14)]          # (key, eighth) over two bars: ours


def line_parts(parts, line, bpm, start, ratio=None, delay_ms=0.0, gain=0.0, inst="piano"):
    ts = BL.swing_times([e for _, e in line], bpm, ratio, delay_ms) + start
    beat = 60.0 / bpm
    for k, ((m, e), t) in enumerate(zip(line, ts)):
        nxt = ts[k + 1] if k + 1 < len(ts) else t + beat
        dur = max(nxt - t, 0.12)
        if inst == "piano":
            parts.append((arr(piano(m, dur * 0.9, 1.1)), t, gain))
        else:
            parts.append((arr(horn(m, dur * 0.9, inst)), t, gain))
    return ts


def compute_hook() -> dict:
    bpm = 120
    changes = [["C7"], ["F7"], ["C7"], ["G7"]]
    out, times = {}, {}
    for name, ratio in (("swung", None), ("straight", 1.0)):
        parts = []
        rhythm_section(parts, changes, bpm, ratio=ratio, comp=False)
        ts = []
        for rep in range(2):
            ts += list(line_parts(parts, HOOK_LINE, bpm, rep * 2 * 4 * 60 / bpm, ratio=ratio))
        c = bounce(parts, 4 * 4 * 60 / bpm + 1.2)
        times[name] = [float(x) for x in ts]
        out[name] = save(f"hook.{name}", c, detail=("a line of ours swung by the model at 120 beats a minute" if name == "swung" else "the same line played straight") + ", over bass, ride and hi-hat: piano, string, cymbal models")
    r = BL.swing_ratio(bpm)
    return {"bpm": bpm, "ratio": r, "line": HOOK_LINE, "times": times, "answer": "three times", "short_ms": BL.short_note_ms(bpm),
            "clips": out}


def compute_form() -> dict:
    bpm = 100
    changes = BL.twelve_bar("C", "basic")
    parts = []
    wb = rhythm_section(parts, changes, bpm)
    c = bounce(parts, 12 * 4 * 60 / bpm + 1.5)
    return {"bpm": bpm, "changes": changes, "bass": wb, "roman": ["I7", "I7", "I7", "I7", "IV7", "IV7", "I7", "I7", "V7", "IV7", "I7", "V7"],
            "quick": BL.twelve_bar("C", "quick"), "jazz": BL.twelve_bar("C", "jazz"),
            "clips": {"twelve": save("form.twelve", c, detail="a twelve-bar blues of ours in C: piano comping, walking bass, ride and hi-hat; piano, string and cymbal models")}}


BLUE_PHRASE = [(67, 0.0, 0.5), (69, 0.5, 0.5), (72, 1.0, 1.0), (75, 2.0, 1.5), (72, 3.5, 1.0), (67, 4.5, 1.5)]   # beats


def compute_blue() -> dict:
    bpm = 80
    beat = 60.0 / bpm
    versions = [("minor", 75.0, None), ("major", 76.0, None), ("bent", 75.0, 75.85)]
    parts, starts, t0 = [], {}, 0.0
    for name, third, bend in versions:
        starts[name] = t0
        notes = []
        for m, a, d in BLUE_PHRASE:
            if m == 75:
                if bend is None:
                    notes.append((third, t0 + a * beat, d * beat))
                else:
                    k = 6
                    for j in range(k):
                        notes.append((third + (bend - third) * min(1.0, (j + 1) / (k - 2)), t0 + (a + d * j / k) * beat, d * beat / k))
            else:
                notes.append((m - 0.0, t0 + a * beat, d * beat))
        parts.append((arr(sing([(m - 12, a, d) for m, a, d in notes], "tenor", "a", seed=1)), 0.0, 0.0))
        for m in (48, 52, 58, 64):
            parts.append((arr(piano(m, 2.5, 0.6)), t0, -10.0))
        t0 += 6.5 * beat + 1.2
    c = bounce(parts, t0 + 0.5)
    return {"bpm": bpm, "phrase": [list(x) for x in BLUE_PHRASE], "starts": starts, "cents": {"minor": 300, "major": 400, "bent": [300, 385]},
            "clips": {"three": save_synth("blue.three", c, detail="one phrase of ours sung three times over a C7 chord: with a minor third, a major third, and a third bent upwards between them; a model voice and Part 7's piano")}}


def compute_callresp() -> dict:
    bpm = 84
    beat = 60.0 / bpm
    changes = BL.twelve_bar("C", "basic")
    # three vocal lines (A, A over IV, B), each two bars, answered by two bars of guitar: ours
    vA = [(67, 0.5, 0.5), (70, 1.0, 1.0), (67, 2.0, 0.5), (64.6, 2.5, 1.0), (60, 3.5, 2.0)]
    vA2 = [(m + (0 if m != 64.6 else 0), a, d) for m, a, d in vA]
    vB = [(72, 0.5, 0.5), (70, 1.0, 0.5), (67, 1.5, 1.0), (64.6, 2.5, 0.5), (62, 3.0, 1.0), (60, 4.0, 2.0)]
    gfill = [(75, 0.0), (76, 0.5), (79, 1.0), (82, 1.5), (79, 2.0), (76, 2.5), (72, 3.0)]
    notes = []
    for k, (line, bar0) in enumerate(((vA, 0), (vA2, 4), (vB, 8))):
        for m, a, d in line:
            notes.append((m - 12, (bar0 * 4 + a) * beat, d * beat))
    parts = [(arr(sing(notes, "tenor", "a", seed=2)), 0.0, 0.0)]
    for bar0 in (2, 6, 10):
        for m, a in gfill:
            parts.append((arr(guitar(m - 12, 0.5)), (bar0 * 4 + a) * beat, -3.0))
    rhythm_section(parts, changes, bpm, gain=-3.0)
    c = bounce(parts, 12 * 4 * beat + 1.5)
    return {"bpm": bpm, "changes": changes, "voice": [[m - 12, a, d] for m, a, d in notes], "beat": beat,
            "lines": {"A": 0, "A2": 4, "B": 8}, "fills": [2, 6, 10],
            "clips": {"aab": save_synth("callresp.aab", c, detail="a twelve-bar blues of ours in AAB form: a model voice sings each line, a guitar answers; piano, bass and cymbal underneath")}}


def maple():
    L = next(r for r in R.load_library() if "joplin" in r["path"])
    return L["parts"]["Piano"]


def compute_rag() -> dict:
    notes = maple()
    bar = 48
    A = [n for n in notes if n[1] < 16 * bar]
    unit = 0.62 / 24.0                                     # seconds a tick: a quarter note is 0.62 s
    parts = []
    for p, o, d in A:
        parts.append((arr(piano(p, d * unit * 1.05, 0.9 if p > 61 else 0.8)), o * unit, -2.0 if p > 61 else -4.0))
    c = bounce(parts, 16 * bar * unit + 1.5)
    rh, lh = BL.rag_hands(A)
    s_r, s_l = BL.syncopation(rh), BL.syncopation(lh)
    # bars 1-4: right hand, left hand, both
    A4 = [n for n in notes if n[1] < 4 * bar]
    r4, l4 = BL.rag_hands(A4)
    out, starts, t = [], {}, 0.0
    for name, which in (("right", r4), ("left", l4), ("both", A4)):
        starts[name] = t
        for p, o, d in which:
            out.append((arr(piano(p, d * unit * 1.05, 0.9 if p > 61 else 0.8)), t + o * unit, -2.0 if p > 61 else -4.0))
        t += 4 * bar * unit + 0.9
    c2 = bounce(out, t + 0.6)
    rows = lambda v: [[int(p), int(o), int(d)] for p, o, d in v]
    return {"unit": unit, "bar": bar, "right": rows(rh), "left": rows(lh), "sync_right": s_r, "sync_left": s_l, "starts": starts,
            "clips": {"strain": save("rag.strain", c, detail="Scott Joplin, Maple Leaf Rag (1899), bars 1-16 from the music21 corpus encoding: Part 7's piano"),
                      "hands": save("rag.hands", c2, detail="Maple Leaf Rag, bars 1-4: right hand, left hand, both: Part 7's piano")}}


def compute_swing() -> dict:
    out, starts, t = [], {}, 0.0
    changes = [["C7"], ["F7"], ["C7"], ["G7"]]
    for bpm in (100, 180, 260):
        starts[str(bpm)] = t
        rhythm_section(out, changes, bpm, start=t, comp=False, hat_on=True)
        t += 4 * 4 * 60.0 / bpm + 0.9
    c = bounce(out, t + 0.6)
    table = [{"bpm": b, "ratio": BL.swing_ratio(b), "short_ms": BL.short_note_ms(b)} for b in range(100, 321, 20)]
    return {"tempos": [100, 180, 260], "ratios": {str(b): BL.swing_ratio(b) for b in (100, 180, 260)}, "starts": starts,
            "table": table, "pattern": RIDE_PATTERN,
            "clips": {"tempos": save("swing.tempos", c, detail="the ride pattern with walking bass and hi-hat at 100, 180 and 260 beats a minute, each swung by the model's ratio; string and cymbal models")}}


DELAY_LINE = [(76, 0), (79, 1), (81, 2), (79, 3), (76, 4), (74, 5), (72, 6), (74, 7),
              (76, 8), (72, 9), (69, 10), (72, 11), (74, 12), (76, 13), (72, 14)]


def compute_delay() -> dict:
    bpm = 160
    changes = [["C7"], ["F7"], ["C7"], ["G7"]]
    out = {}
    for name, dl in (("ontime", 0.0), ("late", 30.0)):
        parts = []
        rhythm_section(parts, changes + changes, bpm, comp=False)
        for rep in range(4):
            line_parts(parts, DELAY_LINE, bpm, rep * 2 * 4 * 60 / bpm, delay_ms=dl, inst="sax", gain=-1.0)
        out[name] = save_synth(f"delay.{name}", bounce(parts, 8 * 4 * 60 / bpm + 1.2),
                               detail=("a line of ours with every note placed by the swing model" if dl == 0 else "the same line with its on-beat notes 30 ms late (illustrative)") + "; an additive saxophone over string and cymbal models")
    return {"bpm": bpm, "delay_ms": 30.0, "ratio": BL.swing_ratio(bpm), "clips": out}


def compute_jitter() -> dict:
    """The same line placed exactly by the swing model, then with random timing deviations (sd 15 ms, seeded): the
    kind of manipulation Datseris and colleagues (2019) used, with values of ours."""
    bpm = 160
    changes = [["C7"], ["F7"], ["C7"], ["G7"]]
    rng = np.random.default_rng(11)
    out, devs = {}, []
    for name, sd in (("grid", 0.0), ("random", 15.0)):
        parts = []
        rhythm_section(parts, changes + changes, bpm, comp=False)
        beat = 60.0 / bpm
        for rep in range(4):
            ts = BL.swing_times([e for _, e in DELAY_LINE], bpm) + rep * 2 * 4 * beat
            dv = rng.normal(0.0, sd / 1000.0, len(ts)) if sd else np.zeros(len(ts))
            if sd:
                devs += list(dv * 1000)
            for k, ((m, e), t) in enumerate(zip(DELAY_LINE, ts + dv)):
                nxt = ts[k + 1] if k + 1 < len(ts) else ts[k] + beat
                parts.append((arr(horn(m, max(nxt - ts[k], 0.12) * 0.9, "sax")), max(t, 0.0), -1.0))
        out[name] = save_synth(f"jitter.{name}", bounce(parts, 8 * 4 * beat + 1.2),
                               detail=("a line of ours placed exactly by the swing model" if not sd else "the same line with random timing deviations, standard deviation 15 ms (ours)") + "; an additive saxophone over string and cymbal models")
    return {"bpm": bpm, "sd_ms": 15.0, "devs": [float(x) for x in devs], "max_ms": float(np.max(np.abs(devs))), "clips": out}


RIFF = [(67, 1), (70, 2), (72, 3), (70, 5), (67, 6)]                 # saxes: a two-bar riff, in eighths (ours)
ANSWER = [(79, 9), (79, 11), (76, 12)]                               # brass: the answer in the second bar


def compute_band() -> dict:
    bpm = 150
    beat = 60.0 / bpm
    changes = BL.twelve_bar("C", "basic")
    parts = []
    rhythm_section(parts, changes, bpm, gain=-2.0)
    sax_v = [0, -3, -7, -12]
    brass_v = [0, -4, -9]
    for b2 in range(6):
        t0 = b2 * 8 * beat
        root = BL.chord(changes[2 * b2][0])["root"]
        shift = {0: 0, 5: 5, 7: 7}.get(root, 0)
        shift = shift if shift <= 5 else shift - 12
        for m, e in RIFF:
            ts = BL.swing_times([e], bpm)[0] + t0
            for k, v in enumerate(sax_v):
                parts.append((arr(horn(m + shift + v - 12 * (k == 3), beat * 0.9, "sax")), ts, -9.0))
        for m, e in ANSWER:
            ts = BL.swing_times([e], bpm)[0] + t0
            for v in brass_v:
                parts.append((arr(horn(m + shift + v, beat * 0.8, "brass")), ts, -11.0))
    c = bounce(parts, 12 * 4 * beat + 1.5)
    return {"bpm": bpm, "riff": RIFF, "answer": ANSWER, "changes": changes,
            "clips": {"riff": save_synth("band.riff", c, detail="a riff chart of ours on a twelve-bar blues: saxophones' riff answered by brass, over the rhythm section; additive horns, string, cymbal and piano models")}}


def compute_walking() -> dict:
    bpm = 140
    changes = BL.twelve_bar("C", "jazz")
    wb = BL.walking_bass(changes)
    seq = BL.beats_of(changes)
    firsts = [i for i in range(len(seq)) if i == 0 or seq[i] != seq[i - 1]]
    roots_ok = all(wb[i] % 12 == BL.chord(seq[i])["root"] for i in firsts)
    approaches = [abs(wb[(i - 1) % len(wb)] - wb[i]) for i in firsts]
    parts = []
    rhythm_section(parts, changes, bpm, comp=False, bass_line=wb)
    rhythm_section(parts, changes, bpm, start=12 * 4 * 60 / bpm, bass_line=wb)
    c = bounce(parts, 24 * 4 * 60 / bpm + 1.5)
    return {"bpm": bpm, "changes": changes, "bass": wb, "beats": seq, "roots_ok": roots_ok, "approaches": approaches,
            "moves": [abs(wb[i + 1] - wb[i]) for i in range(len(wb) - 1)],
            "clips": {"trio": save("walking.trio", c, detail="the walking-bass generator's line over a jazz blues in C: bass, ride and hi-hat; then again with piano; string, cymbal and piano models")}}


def compute_guide() -> dict:
    two = BL.guide_tones(["Dm7", "G7", "Cmaj7"])
    jazz = [s for b in BL.twelve_bar("C", "jazz") for s in b]
    gj = BL.guide_tones(jazz)
    bpm = 90
    beat = 60.0 / bpm
    parts, starts, t = [], {}, 0.0
    starts["iiVI"] = t
    for rep in range(2):
        for k, s in enumerate(["Dm7", "G7", "Cmaj7", "Cmaj7"]):
            i = min(k, 2)
            tt = t + (rep * 4 + k) * 4 * beat
            for m in (two["upper"][i], two["lower"][i]):
                parts.append((arr(piano(m, 4 * beat * 0.95, 0.7)), tt, -3.0))
            parts.append((arr(bass(BL.chord(s)["root"] + 36, 4 * beat * 0.9)), tt, -2.0))
    t += 8 * 4 * beat + 1.0
    starts["jazz"] = t
    bpm2 = 120
    beat2 = 60.0 / bpm2
    bars = BL.twelve_bar("C", "jazz")
    idx = 0
    for b, bar in enumerate(bars):
        for j, s in enumerate(bar):
            tt = t + (b * 4 + j * 4 // len(bar)) * beat2
            dur = 4 * beat2 / len(bar)
            for m in (gj["upper"][idx], gj["lower"][idx]):
                parts.append((arr(piano(m, dur * 0.95, 0.7)), tt, -3.0))
            parts.append((arr(bass(BL.chord(s)["root"] + 36, dur * 0.9)), tt, -2.0))
            idx += 1
    t += 12 * 4 * beat2 + 1.0
    c = bounce(parts, t + 0.5)
    return {"iiVI": two, "jazz": gj, "jazz_symbols": jazz, "bpm": bpm, "bpm2": bpm2, "starts": starts,
            "clips": {"lines": save("guide.lines", c, detail="guide tones (thirds and sevenths) as two lines through ii-V-I twice, then through a jazz blues, over bass roots; piano and string models")}}


def shell(symbol):
    c = BL.chord(symbol)
    root = c["root"] + 36
    third = 52 + (c["third"] - 52) % 12
    seventh = 52 + (c["seventh"] - 52) % 12 if c["seventh"] is not None else 52 + (c["root"] - 52) % 12
    return root, sorted([third, seventh])


def compute_subs() -> dict:
    bpm = 90
    beat = 60.0 / bpm
    out, starts, t = [], {}, 0.0
    progs = {"plain": ["Dm7", "G7", "Cmaj7"], "sub": ["Dm7", "Db7", "Cmaj7"]}
    for name, prog in progs.items():
        starts[name] = t
        g = BL.guide_tones(prog)
        for rep in range(2):
            for k, s in enumerate(prog + [prog[-1]]):
                tt = t + (rep * 4 + k) * 4 * beat * 0.5
                i = min(k, 2)
                for m in (g["upper"][i], g["lower"][i]):
                    out.append((arr(piano(m, 2 * beat * 0.95, 0.7)), tt, -3.0))
                out.append((arr(bass(BL.chord(s)["root"] + (36 if BL.chord(s)["root"] < 6 else 24), 2 * beat * 0.9)), tt, 0.0))
        t += 8 * 2 * beat + 1.2
    c = bounce(out, t + 0.4)
    bass_plain = [BL.chord(s)["root"] + (36 if BL.chord(s)["root"] < 6 else 24) for s in progs["plain"]]
    bass_sub = [BL.chord(s)["root"] + (36 if BL.chord(s)["root"] < 6 else 24) for s in progs["sub"]]
    # a turnaround: I vi ii V, then I VI7 ii V, then with tritone subs: I bIII7 ii bII7
    turn = {"diatonic": ["Cmaj7", "Am7", "Dm7", "G7"], "secondary": ["Cmaj7", "A7", "Dm7", "G7"], "subs": ["Cmaj7", "Eb7", "Dm7", "Db7"]}
    parts, ts, t = [], {}, 0.0
    for name, prog in turn.items():
        ts[name] = t
        g = BL.guide_tones(prog * 2)
        for k, s in enumerate(prog * 2):
            tt = t + k * 2 * beat
            for m in (g["upper"][k], g["lower"][k]):
                parts.append((arr(piano(m, 2 * beat * 0.95, 0.7)), tt, -3.0))
            r = BL.chord(s)["root"]
            parts.append((arr(bass(r + (36 if r < 6 else 24), 2 * beat * 0.9)), tt, 0.0))
        t += 8 * 2 * beat + 1.0
    parts.append((arr(piano(48, 2.0, 0.7)), t - 1.0, -3.0))
    c2 = bounce(parts, t + 1.5)
    return {"bpm": bpm, "starts": starts, "progs": progs, "bass_plain": bass_plain, "bass_sub": bass_sub, "answer": "second",
            "shared": sorted(BL.tritone("G7")), "turn": turn, "turn_starts": ts,
            "clips": {"quiz": save("subs.quiz", c, detail="ii-V-I in C, then ii-bII7-I, each twice: guide tones on piano over bass roots; piano and string models"),
                      "turnaround": save("subs.turnaround", c2, detail="a turnaround three ways: I-vi-ii-V, I-VI7-ii-V, I-bIII7-ii-bII7; piano and string models")}}


def compute_tune() -> dict:
    mel = tune_line(14, 72)
    # 1. a twelve-bar blues: phrase 1 (bars 1-4) over I, again over IV (bars 5-8), phrase 2 over V-IV-I (bars 9-12)
    bpm = 96
    beat = 60.0 / bpm
    p1 = [(m, a, d) for m, a, d in mel[:7]]
    p2 = [(m, a - 8, d) for m, a, d in mel[7:]]
    blues_notes = []
    for bar0, ph, shift in ((0, p1, 0), (4, p1, 5), (8, p2, 0)):
        for m, a, d in ph:
            mm = m + shift
            if mm % 12 == 4:
                mm -= 0.35                                         # a blue third: between E flat and E
            blues_notes.append((mm - 12, (bar0 * 4 + a) * beat, d * beat * 0.95))
    parts = [(arr(sing(blues_notes, "tenor", "a", seed=5)), 0.0, 0.0)]
    rhythm_section(parts, BL.twelve_bar("C", "basic"), bpm, gain=-3.0)
    t1 = 12 * 4 * beat + 1.2
    c1 = Clip(mix(parts, duration=t1).y, SR).at_level(LEVEL)
    # 2. a rag: the Tune in the right hand as sixteenth-eighth-sixteenth figures, oom-pah left hand, 2/4, 8 bars
    q = 0.3                                                         # seconds a eighth
    parts = []
    rag_rh = []
    for k, (m, a, d) in enumerate(mel):
        t0 = a * 2 * q                                              # a Tune beat = a quarter = two eighths
        if d == 1:
            figs = [(m, 0.0, 0.5), (m + 12, 0.5, 1.0), (m, 1.5, 0.5)]
        else:
            figs = [(m, 0.0, 0.5), (m + 12, 0.5, 1.0), (m, 1.5, 1.0), (m + 7 if m + 7 <= 91 else m, 2.5, 1.5)]
        for mm, aa, dd in figs:
            rag_rh.append((mm, t0 + aa * q, dd * q))
    for mm, a, d in rag_rh:
        parts.append((arr(piano(mm, d * 1.05, 1.0)), a, -2.0))
    chords_rag = ["C", "C", "F", "C", "F", "C", "G", "C"]
    rag_lh = []
    for b, ch in enumerate(chords_rag):
        r = BL.chord(ch)["root"]
        bass_n = 36 + r if r < 8 else 24 + r
        tri = sorted(52 + (p - 52) % 12 for p in BL.chord(ch)["pcs"])
        t0 = b * 4 * q
        rag_lh += [(bass_n, t0, q), (tri, t0 + q, q), (bass_n + 7, t0 + 2 * q, q), (tri, t0 + 3 * q, q)]
    for item, a, d in rag_lh:
        for m in (item if isinstance(item, list) else [item]):
            parts.append((arr(piano(m, d, 0.8)), a, -6.0))
    t2 = 8 * 4 * q + 1.2
    c2 = Clip(mix(parts, duration=t2).y, SR).at_level(LEVEL)
    # 3. a riff chart: the Tune's first four notes as the saxes' riff, brass answering with its cadence
    bpm3 = 150
    beat3 = 60.0 / bpm3
    parts = []
    changes = BL.twelve_bar("C", "basic")
    rhythm_section(parts, changes, bpm3, gain=-2.0)
    riff = [(72, 0), (72, 1), (79, 2), (79, 3), (81, 4), (79, 6)]
    ans = [(77, 9), (76, 10), (74, 11), (72, 12)]
    for b2 in range(6):
        t0 = b2 * 8 * beat3
        root = BL.chord(changes[2 * b2][0])["root"]
        shift = root if root <= 5 else root - 12
        for m, e in riff:
            ts = BL.swing_times([e], bpm3)[0] + t0
            for v in (0, -3, -7):
                parts.append((arr(horn(m + shift + v - 12, beat3 * 0.9, "sax")), ts, -9.0))
        for m, e in ans:
            ts = BL.swing_times([e], bpm3)[0] + t0
            for v in (0, -4):
                parts.append((arr(horn(m + shift + v, beat3 * 0.8, "brass")), ts, -11.0))
    t3 = 12 * 4 * beat3 + 1.2
    c3 = Clip(mix(parts, duration=t3).y, SR).at_level(LEVEL)
    s_ = concat([c1, c2, c3], gap=1.0, names=["blues", "rag", "riff"])
    rag_s = BL.syncopation([(m, int(round(a / q * 12)), int(round(d / q * 12))) for m, a, d in rag_rh])
    return {"melody": [list(x) for x in mel], "blues_bpm": bpm, "blues": [list(x) for x in blues_notes], "rag_q": q,
            "rag_rh": [list(x) for x in rag_rh], "rag_sync": rag_s, "riff_bpm": bpm3, "riff": riff, "answer": ans,
            "starts": {k: float(s_.events[k]) for k in ("blues", "rag", "riff")}, "seconds": s_.duration,
            "clips": {"variation": save_synth("tune.variation38", s_, detail="the Tune as a twelve-bar blues sung with blue thirds, as a rag on Part 7's piano, and as a riff chart for additive horns over the rhythm section")}}


def compute_variation() -> dict:
    t = load("tune")
    rs = t["rag_sync"]
    return {"part": 38, "title": "as a twelve-bar blues, a rag and a riff chart", "seconds": round(t["seconds"], 1),
            "measure": f"blues thirds 35 cents below E; in the rag {rs['syncopated']} of {rs['onsets']} right-hand onsets syncopated; the riff swung {BL.swing_ratio(t['riff_bpm']):.1f} to 1",
            "clip": "tune.variation38"}


ITEMS = {"hook": compute_hook, "form": compute_form, "blue": compute_blue, "callresp": compute_callresp, "rag": compute_rag,
         "swing": compute_swing, "delay": compute_delay, "jitter": compute_jitter, "band": compute_band, "walking": compute_walking, "guide": compute_guide,
         "subs": compute_subs, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
