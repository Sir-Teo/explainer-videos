"""The score of *Economics, Built*: a little computed music under the films (videos/economics/SYLLABUS.md, 1.3).

Nothing is recorded and nothing is third-party: every note is synthesized here, deterministically, from sines (modal
synthesis, as *Music, Built* computes its instruments), placed in a computed stereo hall, and mixed into the master
by ``tools/build.py`` through the music-stem path (the narration is mastered to -16 LUFS; these clips sit 8 to 18 LU
below it).

The theme is **the scissors**.  Marshall (1890) said that asking whether value is set by demand or by supply is like
asking which blade of a pair of scissors cuts the paper.  Two voices: a falling one, struck like a soft bell (the
demand blade, blue on screen), and a rising one, plucked (supply, amber).  They start an octave apart and close on
one note, the price.

Cues, placed from the film's own timeline (each scene's start, length, chapter title and narration lines):

* **the theme** under the cold open: the two voices from an octave apart to the unison, about eight seconds;
* **a sting** at each chapter card: the two voices at the point of their paths that the chapter has reached, so the
  ear hears the part close in, chapter by chapter, and meet in the outro;
* **the bed** in dead air (a Play-it pause, a long animation): a quiet open chord that breathes, with a slow
  arpeggio, faded in after the voice stops and out before it returns;
* **the close** under the end of the outro: the voices meet once more, this time on the keynote, under a major chord.

The **data melody** of each part's intermission is made by :func:`data_melody` in the part's ``compute.py`` (it is
the part's own data, mapped to the scale) and played by the intermission scene itself, so the picture moves on the
melody's clock; :func:`cues` leaves that scene alone.

Each act has its own key and colour (:data:`ACT_KEYS`): the same theme, a step elsewhere, so a viewer feels the
course move on.  ``cues(timeline, cache)`` returns cue dicts (``path``, ``start``, ``gain_db``, ``duration``,
``underscore``) for ``tools/build.py``; ``python tools/build.py econN --no-score`` leaves the score out.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np

SR = 48_000
GAP_MIN = 2.8  # seconds of silence before the bed comes in
BED_EDGE = 0.4  # the bed starts this long after the voice stops, and ends this long before it returns
THEME_LUFS = -26.0  # the theme and the close, under the cold open's and the outro's narration
STING_LUFS = -28.0  # the chapter stings, under "Chapter six. Incentives."
# (both were 2 LU louder until Part 2: a sting or the close landing in phase with a narration peak took the mix
# over the -1 dBTP ceiling; under speech, 10 to 12 LU below the voice is room enough)
BED_LUFS = -34.0  # the bed, alone in the room
MELODY_LUFS = -20.0  # a data melody, which plays with no narration over it
PEAK_DB = -3.0  # no clip peaks above this (the master's ceiling is -1.5 dBTP)
VERSION = "economics_score_v2"

# D dorian, the series' home: the scale degrees as semitones above D
DORIAN = (0, 2, 3, 5, 7, 9, 10)
D4 = 62  # MIDI
# The two blades, as MIDI notes from D4 = 62: demand falls from D5, supply rises from D4; they meet on A4
DEMAND_PATH = (74, 72, 70, 69)
SUPPLY_PATH = (62, 64, 65, 67, 69)
# One key per act (semitones above D) and a brightness for the struck voice, so each act has its own colour
ACT_KEYS = {1: (0, 1.0), 2: (5, 0.9), 3: (-2, 1.1), 4: (3, 1.0), 5: (-5, 0.85), 6: (2, 1.15), 7: (-3, 0.95),
            8: (4, 1.0), 9: (-4, 0.9), 10: (1, 1.2), 11: (-1, 1.05), 12: (0, 1.25)}
ACTS = ((1, 4), (5, 8), (9, 12), (13, 18), (19, 24), (25, 33), (34, 37), (38, 42), (43, 50), (51, 56), (57, 62),
        (63, 68))


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def act_of(part: int) -> int:
    return next(i + 1 for i, (a, b) in enumerate(ACTS) if a <= part <= b)


# ---------------------------------------------------------------------------
# Instruments (modal synthesis: each is a sum of decaying sines, exactly in tune)
# ---------------------------------------------------------------------------
def _t(seconds: float) -> np.ndarray:
    return np.arange(int(seconds * SR)) / SR


def _fade(y: np.ndarray, attack: float, release: float) -> np.ndarray:
    n = len(y)
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    r = np.clip((n / SR - t) / max(release, 1e-4), 0, 1)
    return y * np.sin(a * np.pi / 2) ** 2 * np.sin(r * np.pi / 2) ** 2


def pluck(f: float, seconds: float = 2.6, position: float = 0.18, decay: float = 1.4, inharm: float = 1.2e-4,
          bright: float = 1.0) -> np.ndarray:
    """A plucked string: the modes of a slightly stiff string, weighted by where it was plucked, each dying faster
    than the one below (the supply blade)."""
    t = _t(seconds)
    y = np.zeros_like(t)
    for k in range(1, 14):
        fk = k * f * np.sqrt(1 + inharm * k * k)
        if fk > 12_000:
            break
        amp = abs(np.sin(np.pi * k * position)) / k ** (1.15 / bright)
        y += amp * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1 + 0.55 * (k - 1)) / decay)
    return _fade(y, 0.003, 0.08)


def bell(f: float, seconds: float = 3.0, bright: float = 1.0) -> np.ndarray:
    """A soft struck tone, like a felt mallet on a tuned bar or an electric piano's tine (the demand blade)."""
    t = _t(seconds)
    y = (np.sin(2 * np.pi * f * t) * np.exp(-t / 2.2)
         + 0.32 * bright * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 1.1)
         + 0.10 * bright * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.6)
         + 0.05 * bright * np.sin(2 * np.pi * 7.03 * f * t) * np.exp(-t / 0.12))
    return _fade(y, 0.006, 0.25)


def pad(fs, seconds: float, attack: float = 1.2, release: float = 1.8, breathe: float = 0.0) -> np.ndarray:
    """A sustained chord: each note two slightly detuned sines with a soft octave above, swelling ``breathe`` times
    a second if asked."""
    t = _t(seconds)
    y = np.zeros_like(t)
    for i, f in enumerate(fs):
        for cents in (-5.0, 5.0):
            g = f * 2 ** (cents / 1200)
            y += (np.sin(2 * np.pi * g * t + 1.1 * i) + 0.18 * np.sin(4 * np.pi * g * t + 0.4 * i)) / (1 + 0.5 * i)
    if breathe:
        y *= 0.7 + 0.3 * np.sin(2 * np.pi * breathe * t - np.pi / 2)
    return _fade(y, attack, release)


# ---------------------------------------------------------------------------
# The room
# ---------------------------------------------------------------------------
_IR = None


def hall(t60_low: float = 2.4, t60_mid: float = 1.9, t60_high: float = 0.9, seconds: float = 2.6,
         seed: int = 1758) -> np.ndarray:
    """A stereo impulse response: decorrelated noise decaying at a different rate in three bands (low frequencies
    ring longest, as in a hall), after a 14 ms pre-delay.  Computed once."""
    global _IR
    if _IR is not None:
        return _IR
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    f = np.fft.rfftfreq(n, 1 / SR)
    for ch in range(2):
        acc = np.zeros(n)
        for lo, hi, t60 in ((0, 400, t60_low), (400, 3000, t60_mid), (3000, SR / 2, t60_high)):
            spec = np.fft.rfft(rng.standard_normal(n))
            spec[(f < lo) | (f >= hi)] = 0
            band = np.fft.irfft(spec, n)
            acc += band * np.exp(-6.91 * t / t60)
        pre = int(0.014 * SR)
        acc = np.concatenate([np.zeros(pre), acc[:-pre]])
        out[:, ch] = acc
    out /= np.sqrt((out ** 2).sum(axis=0, keepdims=True))
    _IR = out
    return out


def _stereo(y: np.ndarray, pan: float = 0.0) -> np.ndarray:
    th = (pan + 1) * np.pi / 4
    return np.stack([y * np.cos(th), y * np.sin(th)], axis=1)


def _place(out: np.ndarray, y: np.ndarray, at: float, pan: float = 0.0, gain: float = 1.0) -> None:
    a = int(at * SR)
    b = min(a + len(y), len(out))
    if b > a:
        out[a:b] += gain * _stereo(y[: b - a], pan)


def _wet(dry: np.ndarray, mix: float = 0.24) -> np.ndarray:
    """Dry plus the hall's reverberation, the tail kept."""
    from scipy.signal import fftconvolve

    ir = hall()
    tail = len(ir)
    padded = np.concatenate([dry, np.zeros((tail, 2))])
    wet = np.stack([fftconvolve(padded[:, c], ir[:, c])[: len(padded)] for c in range(2)], axis=1)
    rms_d = np.sqrt(np.mean(padded ** 2)) + 1e-12
    rms_w = np.sqrt(np.mean(wet ** 2)) + 1e-12
    y = padded + mix * wet * (rms_d / rms_w)
    # trim the silent end of the tail
    env = np.abs(y).max(axis=1)
    last = np.nonzero(env > 1e-4 * env.max())[0]
    return y[: (last[-1] + 1 if len(last) else len(y))]


def _lufs(y: np.ndarray) -> float:
    """Loudness of a stereo clip by BS.1770's K-weighting, ungated (the clips are short and dense)."""
    from scipy.signal import lfilter

    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    z = lfilter(b2, a2, lfilter(b1, a1, y, axis=0), axis=0)
    ms = float(np.mean(z ** 2, axis=0).sum())
    return -0.691 + 10 * np.log10(max(ms, 1e-12))


def _at(y: np.ndarray, lufs: float) -> np.ndarray:
    y = y * 10 ** ((lufs - _lufs(y)) / 20)
    peak = np.abs(y).max()
    ceiling = 10 ** (PEAK_DB / 20)
    if peak > ceiling:  # never louder at the peak than the ceiling: quieter instead
        y = y * ceiling / peak
    return y.astype(np.float32)


# ---------------------------------------------------------------------------
# The cues
# ---------------------------------------------------------------------------
def _key(act: int) -> tuple:
    return ACT_KEYS.get(act, (0, 1.0))


def theme(act: int = 1) -> np.ndarray:
    """The scissors: demand falls from D5, supply rises from D4, and they strike the same A together."""
    shift, bright = _key(act)
    out = np.zeros((int(8.5 * SR), 2))
    _place(out, pad([hz(50 + shift), hz(57 + shift), hz(65 + shift)], 4.4, attack=1.0, release=1.6), 0.0, gain=0.42)
    _place(out, pad([hz(50 + shift), hz(57 + shift), hz(64 + shift), hz(69 + shift)], 4.6, attack=0.8,
                    release=2.4), 3.6, gain=0.40)
    times_d = (0.45, 1.25, 2.05, 3.25)
    times_s = (0.85, 1.65, 2.45, 2.85, 3.25)
    for k, (m, at) in enumerate(zip(DEMAND_PATH, times_d)):
        _place(out, bell(hz(m + shift), 3.4 if k < 3 else 4.6, bright), at, pan=0.32, gain=0.55)
    for k, (m, at) in enumerate(zip(SUPPLY_PATH, times_s)):
        _place(out, pluck(hz(m + shift), 2.6 if k < 4 else 4.0, bright=bright), at, pan=-0.32, gain=0.6)
    return _at(_wet(out), THEME_LUFS)


def blades(progress: float) -> tuple:
    """Where the two voices are when the part has gone ``progress`` (0 to 1) of the way: MIDI notes (demand,
    supply).  At 0 they are an octave apart; at 1 they meet."""
    progress = min(max(progress, 0.0), 1.0)
    d = DEMAND_PATH[int(round(progress * (len(DEMAND_PATH) - 1)))]
    s = SUPPLY_PATH[int(round(progress * (len(SUPPLY_PATH) - 1)))]
    return d, s


def sting(progress: float, act: int = 1) -> np.ndarray:
    """A chapter card: the supply voice, then the demand voice, at the point of their paths the part has reached,
    over a soft fifth."""
    shift, bright = _key(act)
    d, s = blades(progress)
    out = np.zeros((int(3.4 * SR), 2))
    _place(out, pad([hz(50 + shift), hz(57 + shift)], 3.2, attack=0.5, release=1.6), 0.0, gain=0.38)
    _place(out, pluck(hz(s + shift), 2.8, bright=bright), 0.10, pan=-0.3, gain=0.62)
    _place(out, bell(hz(d + shift), 3.0, bright), 0.36, pan=0.3, gain=0.55)
    if d == s:  # the last chapter: they meet, and the fifth below joins them
        _place(out, pluck(hz(s - 12 + shift), 2.8, bright=bright), 0.36, pan=-0.1, gain=0.35)
    return _at(_wet(out), STING_LUFS)


def bed(seconds: float, act: int = 1) -> np.ndarray:
    """Dead air: the open fifth with a ninth, breathing every five seconds, and a slow arpeggio under it, faded in
    and out within ``seconds``."""
    shift, bright = _key(act)
    fade = min(1.2, seconds / 3)
    n = int(seconds * SR)
    out = np.zeros((n, 2))
    _place(out, pad([hz(50 + shift), hz(57 + shift), hz(64 + shift)], seconds, attack=fade, release=fade,
                    breathe=0.2), 0.0)
    arp = (57, 62, 64, 62)
    k, at = 0, 0.9
    while at < seconds - 1.6:
        _place(out, pluck(hz(arp[k % 4] + shift), 1.8, decay=0.9, bright=0.7 * bright), at,
               pan=-0.25 + 0.17 * (k % 4), gain=0.16)
        k += 1
        at += 1.25
    y = _wet(out, mix=0.3)[:n]
    y = y * _fade(np.ones(len(y)), fade, fade)[:, None]
    return _at(y, BED_LUFS)


def close(act: int = 1) -> np.ndarray:
    """The ending: the blades meet on the keynote, under a major chord, about ten seconds."""
    shift, bright = _key(act)
    out = np.zeros((int(10.0 * SR), 2))
    _place(out, pad([hz(50 + shift), hz(57 + shift), hz(66 + shift)], 9.5, attack=1.4, release=4.0), 0.0, gain=0.42)
    for k, m in enumerate((69, 67, 66, 64, 62)):
        _place(out, bell(hz(m + shift), 3.2 if k < 4 else 5.5, bright), 0.4 + 0.6 * k, pan=0.3, gain=0.5)
    for k, m in enumerate((50, 54, 57, 62)):
        _place(out, pluck(hz(m + shift), 2.6 if k < 3 else 5.0, bright=bright), 0.7 + 0.6 * k + (0.6 if k == 3 else 0),
               pan=-0.3, gain=0.6)
    return _at(_wet(out), THEME_LUFS)


def data_melody(values, seconds: float, low: int = 50, high: int = 81, log: bool = True, act: int = 1,
                times=None) -> dict:
    """The part's data as a tune: one plucked note per value, its pitch the value's place between the series' least
    and greatest (on a log scale if ``log``), rounded to D dorian between MIDI ``low`` and ``high``; a bell doubles
    each note an octave up, softly, and a pad holds the keynote.  ``times``: when each value sounds (default: evenly
    spaced).  Returns ``{"y": stereo array, "times": [...], "notes": [...]}``."""
    shift, bright = _key(act)
    v = np.asarray(values, float)
    x = np.log(v) if log else v
    frac = (x - x.min()) / max(x.max() - x.min(), 1e-12)
    scale = [m for m in range(low, high + 1) if (m - D4) % 12 in DORIAN]
    notes = [scale[int(round(f * (len(scale) - 1)))] for f in frac]
    n = len(v)
    step = (seconds - 3.0) / max(n - 1, 1)
    if times is None:
        times_in = [0.8 + i * step for i in range(n)]
    else:
        times_in = [float(x) for x in times]
        assert len(times_in) == n
    out = np.zeros((int((seconds + 1.0) * SR), 2))
    _place(out, pad([hz(38 + shift), hz(50 + shift), hz(57 + shift)], seconds + 0.6, attack=1.5, release=2.5,
                    breathe=0.1), 0.0, gain=0.32)
    times = []
    for i, m in enumerate(notes):
        at = times_in[i]
        times.append(at)
        _place(out, pluck(hz(m + shift), 2.4, bright=bright), at, pan=-0.6 + 1.2 * i / max(n - 1, 1), gain=0.6)
        _place(out, bell(hz(m + 12 + shift), 1.8, 0.6 * bright), at + 0.02, pan=0.6 - 1.2 * i / max(n - 1, 1),
               gain=0.14)
    y = _wet(out, mix=0.28)[: int(seconds * SR)]
    y = y * _fade(np.ones(len(y)), 0.05, 1.2)[:, None]
    return {"y": _at(y, MELODY_LUFS), "times": times, "notes": notes}


# ---------------------------------------------------------------------------
# Placing the cues
# ---------------------------------------------------------------------------
def gaps(lines, duration: float, skip_head: float = 0.0, skip_tail: float = 0.0, minimum: float = GAP_MIN):
    """The silences inside a scene of ``duration`` seconds whose narration ``lines`` are ``{"start", "duration"}``
    (scene time): ``(start, end)`` pairs at least ``minimum`` long, outside the first ``skip_head`` and the last
    ``skip_tail`` seconds."""
    spans = sorted((float(x["start"]), float(x["start"]) + float(x["duration"])) for x in lines)
    out, t = [], skip_head
    for a, b in spans + [(duration - skip_tail, duration)]:
        a = min(a, duration - skip_tail)
        if a - t >= minimum:
            out.append((t, a))
        t = max(t, b)
    return out


def _write(y: np.ndarray, path: Path) -> Path:
    """Write once (the clips are deterministic): a float WAV the music stem reads."""
    from explainer.music.monochord.audio import Clip

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        Clip(np.asarray(y, np.float32), SR).write(path)
    return path


def _part() -> int:
    m = re.match(r"econ(\d+)", os.environ.get("EXPLAINER_VIDEO", "econ1"))
    return int(m.group(1)) if m else 1


def is_intermission(scene: dict) -> bool:
    return (scene.get("cls") == "Intermission") or (scene.get("chapter") or "").lower().startswith("intermission")


UNDER_VOICE = -1.5   # dB, for the cues that sound under narration


def cues(timeline, cache: Path, part: int | None = None) -> list[dict]:
    """The score for one film.  ``timeline``: the scenes in order, each ``{"cls", "chapter", "start", "duration",
    "lines"}`` (``start`` in film time; the lines' times within the scene).  Returns the music-stem cues."""
    part = part or _part()
    act = act_of(part)
    root = Path(cache) / VERSION / f"act{act}"
    out = []

    def cue(name, make, start, gain_db=0.0):
        p = root / f"{name}.wav"
        y = make() if not p.exists() else None
        _write(y, p) if y is not None else None
        from explainer.music.monochord.audio import Clip

        dur = Clip.read(p).duration
        out.append({"path": str(p), "start": float(start), "gain_db": gain_db, "duration": dur, "underscore": True,
                    "label": f"score: {name}"})

    if not timeline:
        return out
    numbered = [k for k, s in enumerate(timeline) if re.match(r"\s*\d+\.", s.get("chapter") or "")]
    # the theme and the chapter stings sound under narration (the cold open's first line, each chapter card's), so
    # they sit UNDER_VOICE dB lower than the beds, which play only in pauses: the mix then stays under the build's
    # true-peak ceiling whatever syllable they meet
    cue("theme", lambda: theme(act), timeline[0]["start"], UNDER_VOICE)
    for k, s in enumerate(timeline):
        head = 8.5 if k == 0 else 0.0
        if k in numbered:
            j = numbered.index(k) + 1
            prog = j / (len(numbered) + 1)
            d, sp = blades(prog)
            cue(f"sting_{d}_{sp}", lambda prog=prog: sting(prog, act), s["start"] + 0.05, UNDER_VOICE)
            head = 3.4
        if is_intermission(s):
            continue  # the intermission plays its own data melody, from its cue sheet
        tail = 10.0 if k == len(timeline) - 1 else 0.0
        for a, b in gaps(s.get("lines", []), s["duration"], skip_head=head, skip_tail=tail):
            secs = round(b - a - 2 * BED_EDGE, 1)
            if secs < 1.5:
                continue
            cue(f"bed{secs:.1f}", lambda secs=secs: bed(secs, act), s["start"] + a + BED_EDGE)
    # the close is the film's last ten seconds, at full level: an outro holds its end card that long after its last
    # line, so the close sounds in a pause (under a line it can meet a syllable and push the mix over the ceiling)
    last = timeline[-1]
    cue("close", lambda: close(act), max(last["start"], last["start"] + last["duration"] - 10.0))
    return out
