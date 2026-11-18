"""The score of *Computer Science, Built*: computed music that gives a fifty-minute lecture a shape you can hear,
and never plays under an explanation (videos/cs/SYLLABUS.md, section 1.2; Moreno & Mayer 2000).

Nothing is recorded and nothing is third-party. Every note is synthesized here, deterministically, from sines,
and mixed into the master by ``tools/build.py`` through the music-stem path *Music, Built* and *Psychology,
Built* use. The narration is mastered to -16 LUFS; these clips sit 8 to 20 LU below it.

The series' motif is **a binary counter you can hear**. A pulse ticks like a clock. On beat k the instrument
sounds the set bits of k: bit 0 the root, bit 1 the fifth, bit 2 the octave, bit 3 the tenth above it. Counting
up from 1 to 7 climbs; counting down comes back to rest. It is Part 5's counter and Pebble's clock, and in the act
*Making It Fast* (Parts 7–10) the clock gets faster.

Five cues, placed from the film's timeline (each scene's start, length, chapter title, narration lines, and the
marks its scene recorded):

* **the theme** at the ``title`` mark (after the cold open), or at the film's start if no scene recorded one:
  the counter from 1 to 7 over an open chord, about six seconds;
* **a sting** at each chapter card: the chapter's own number in binary, its set bits rising, then struck
  together;
* **a pulse** under every prediction's countdown (the ``countdown`` marks): soft ticks, one a second;
* **the bed** in dead air: wherever the narration stops for more than :data:`GAP_MIN` seconds inside a scene
  (a run playing out, a countdown), a quiet chord that fades in and out again before the voice returns;
* **the close** under the end of the outro: the counter from 7 back down to 0.

``cues(timeline, cache)`` returns cue dicts (``path``, ``start``, ``gain_db``, ``duration``, ``underscore``) for
``tools/build.py``; ``python tools/build.py csN --no-score`` leaves the score out.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

SR = 48_000
GAP_MIN = 2.6          # seconds of silence before the bed comes in
BED_EDGE = 0.35        # the bed starts this long after the voice stops, and ends this long before it returns
THEME_LUFS = -24.0     # the theme and the close, under the title and the last words
STING_LUFS = -27.0     # the chapter stings, under "Chapter seven. Predicting branches."
PULSE_LUFS = -32.0     # the countdown's ticks
BED_LUFS = -36.0       # the bed, alone in the room: present, never in the way
VERSION = "cs_score_v1"

# A minor pentatonic around A3; the counter's four bits sound A3, E4, A4, C#5 (an open A major colour on top)
ROOT = 220.0
BIT_HZ = [220.00, 329.63, 440.00, 554.37]
CHORD = [110.00, 164.81, 220.00]       # A2 E3 A3: the open chord under the theme
BED_CHORD = [110.00, 164.81, 246.94]   # A2 E3 B3: open, unresolved, for waiting


def tempo(part: int | None) -> float:
    """Beats per minute: 112, and faster through *Making It Fast* (Parts 7-10), the act where clocks race."""
    if part is not None and 7 <= part <= 10:
        return 112.0 + 8.0 * (part - 6)
    return 112.0


def _env(n: int, attack: float, release: float) -> np.ndarray:
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-3), 0, 1)
    r = np.clip((n / SR - t) / max(release, 1e-3), 0, 1)
    return (np.sin(a * np.pi / 2) ** 2) * (np.sin(r * np.pi / 2) ** 2)


def _pluck(hz: float, dur: float, decay: float = 0.9) -> np.ndarray:
    """A soft mallet tone (a marimba-like pluck): the fundamental, a quiet fourth harmonic, a fast decay."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * hz * t) * np.exp(-t / decay)
    y += 0.22 * np.sin(2 * np.pi * hz * 4 * t) * np.exp(-t / (decay / 5))
    y += 0.08 * np.sin(2 * np.pi * hz * 2 * t) * np.exp(-t / (decay / 2))
    return y * _env(n, 0.004, 0.2)


def _tick(dur: float = 0.12, hz: float = 2400.0) -> np.ndarray:
    """A clock tick: a short, filtered click."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(7)
    noise = rng.standard_normal(n) * np.exp(-t / 0.006)
    tone = np.sin(2 * np.pi * hz * t) * np.exp(-t / 0.015)
    return (0.35 * noise + tone) * _env(n, 0.001, 0.03)


def _pad(hzs, dur: float, attack: float = 0.9, release: float = 1.2, breathe: float = 0.0) -> np.ndarray:
    """A sustained chord: each note two slightly detuned sines, with a slow swell (``breathe`` Hz) if asked."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for i, hz in enumerate(hzs):
        for cents in (-5.0, 5.0):
            f = hz * 2 ** (cents / 1200)
            y += np.sin(2 * np.pi * f * t + 1.1 * i) / (1 + 0.5 * i)
    if breathe:
        y *= 0.72 + 0.28 * np.sin(2 * np.pi * breathe * t - np.pi / 2)
    return y * _env(n, attack, release)


def _stereo(y: np.ndarray, pan: float = 0.0) -> np.ndarray:
    th = (pan + 1) * np.pi / 4
    return np.stack([y * np.cos(th), y * np.sin(th)], axis=1)


def _place(out: np.ndarray, y: np.ndarray, at: float, pan: float = 0.0, gain: float = 1.0) -> None:
    a = int(at * SR)
    if a >= len(out):
        return
    b = min(a + len(y), len(out))
    seg = y[: b - a]
    out[a:b] += gain * (seg if seg.ndim == 2 else _stereo(seg, pan))


def _lufs(y: np.ndarray) -> float:
    """Loudness of a stereo clip by BS.1770's K-weighting, ungated (the clips are short and dense)."""
    from scipy.signal import lfilter

    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    z = lfilter(b2, a2, lfilter(b1, a1, y, axis=0), axis=0)
    ms = float(np.mean(z ** 2, axis=0).sum())
    return -0.691 + 10 * np.log10(max(ms, 1e-12))


def _at(y: np.ndarray, lufs: float) -> np.ndarray:
    return (y * 10 ** ((lufs - _lufs(y)) / 20)).astype(np.float32)


def bits(k: int) -> list[int]:
    """The set bits of k, lowest first (k's binary digits, as the counter sounds them)."""
    return [b for b in range(4) if (k >> b) & 1]


def _beat(out, k: int, at: float, strum: float = 0.035, gain: float = 1.0) -> None:
    """Beat k of the counter: its set bits, struck nearly together, low to high, panned left to right."""
    for j, b in enumerate(bits(k)):
        _place(out, _pluck(BIT_HZ[b], 1.6), at + j * strum, pan=-0.45 + 0.3 * b, gain=gain * (1.0 - 0.12 * b))


def theme(part: int | None = None) -> np.ndarray:
    """The opening: ticks, then the counter from 1 to 7 over the open chord, then the chord left to ring."""
    beat = 60.0 / tempo(part)
    dur = 2.0 + 8 * beat + 2.5
    out = np.zeros((int(dur * SR), 2))
    _place(out, 0.5 * _pad(CHORD, dur, attack=1.0, release=2.2), 0.0)
    for k in range(8):
        _place(out, _tick(), 0.4 + k * beat, pan=0.0, gain=0.5)
    for k in range(1, 8):
        _beat(out, k, 0.4 + k * beat)
    _beat(out, 7, 0.4 + 8 * beat, strum=0.0, gain=1.1)
    return _at(out, THEME_LUFS)


def close(part: int | None = None) -> np.ndarray:
    """The ending: the counter from 7 back down to 0, slowing, and the chord left to ring."""
    beat = 60.0 / tempo(part) * 1.25
    dur = 1.0 + 8 * beat + 3.0
    out = np.zeros((int(dur * SR), 2))
    _place(out, 0.5 * _pad(CHORD, dur, attack=0.8, release=3.0), 0.0)
    for j, k in enumerate(range(7, 0, -1)):
        _beat(out, k, 0.3 + j * beat * (1 + 0.04 * j))
    _place(out, _pluck(ROOT / 2, 3.0, decay=1.8), 0.3 + 7.6 * beat)
    return _at(out, THEME_LUFS)


def sting(chapter: int) -> np.ndarray:
    """A chapter card: chapter n's binary digits rising one at a time, then struck together over the chord."""
    n = max(1, chapter % 16)
    out = np.zeros((int(3.2 * SR), 2))
    _place(out, 0.4 * _pad(CHORD, 3.2, attack=0.4, release=1.6), 0.0)
    bs = bits(n)
    for j, b in enumerate(bs):
        _place(out, _pluck(BIT_HZ[b], 1.8), 0.1 + 0.16 * j, pan=-0.45 + 0.3 * b)
    _beat(out, n, 0.18 + 0.16 * len(bs), strum=0.0, gain=0.8)
    return _at(out, STING_LUFS)


def pulse(seconds: float) -> np.ndarray:
    """Under a countdown: one soft tick a second, the last one an octave of the root."""
    k = max(1, int(round(seconds)))
    out = np.zeros((int((k + 0.8) * SR), 2))
    for j in range(k):
        _place(out, _tick(hz=2000.0), j * 1.0, gain=0.7)
    _place(out, _pluck(ROOT * 2, 0.8, decay=0.4), k * 1.0 - 0.05, gain=0.6)
    return _at(out, PULSE_LUFS)


def bed(seconds: float) -> np.ndarray:
    """Dead air: the open chord, breathing once every five seconds, fading in and out within ``seconds``."""
    fade = min(1.0, seconds / 3)
    y = _pad(BED_CHORD, seconds, attack=fade, release=fade, breathe=0.2)
    return _at(_stereo(y), BED_LUFS)


def gaps(lines, duration: float, skip_head: float = 0.0, skip_tail: float = 0.0, minimum: float = GAP_MIN,
         busy=()):
    """The silences inside a scene of ``duration`` seconds whose narration ``lines`` are ``{"start", "duration"}``
    (scene time): ``(start, end)`` pairs at least ``minimum`` long, outside the first ``skip_head`` and the last
    ``skip_tail`` seconds and outside the ``busy`` spans (where another cue already plays)."""
    spans = sorted([(float(x["start"]), float(x["start"]) + float(x["duration"])) for x in lines] + list(busy))
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


def _part(timeline) -> int | None:
    for s in timeline:
        m = re.search(r"cs(\d+)", s.get("video", "") or "")
        if m:
            return int(m.group(1))
    return None


def cues(timeline, cache: Path, part: int | None = None) -> list[dict]:
    """The score for one film.  ``timeline``: the scenes in order, each ``{"cls", "chapter", "start", "duration",
    "lines", "marks"}`` (``start`` in film time; lines and marks in scene time).  Returns the music-stem cues."""
    cache = Path(cache) / VERSION
    part = part if part is not None else _part(timeline)
    out = []

    def cue(name, y, start):
        p = _write(y, cache / f"{name}.wav")
        out.append({"path": str(p), "start": float(start), "gain_db": 0.0, "duration": len(y) / SR,
                    "underscore": True, "label": f"score: {name}"})
        return len(y) / SR

    if not timeline:
        return out
    th = theme(part)
    titled = False
    for k, s in enumerate(timeline):
        busy = []
        m = re.match(r"\s*(\d+)\.", s.get("chapter") or "")
        head = 0.0
        if m:
            cue(f"sting{int(m.group(1)) % 16}", sting(int(m.group(1))), s["start"] + 0.05)
            head = 3.2
        for mk in s.get("marks", []):
            t = float(mk["time"])
            if mk["name"] == "title" and not titled:
                d = cue(f"theme_{int(tempo(part))}", th, s["start"] + t)
                busy.append((t, t + d))
                titled = True
            elif mk["name"] == "countdown":
                p = pulse(3.0)
                d = cue("pulse3", p, s["start"] + t)
                busy.append((t, t + d))
        tail = 8.0 if k == len(timeline) - 1 else 0.0
        for a, b in gaps(s.get("lines", []), s["duration"], skip_head=head, skip_tail=tail, busy=busy):
            secs = round(b - a - 2 * BED_EDGE, 1)
            if secs >= 1.5:
                cue(f"bed{secs:.1f}", bed(secs), s["start"] + a + BED_EDGE)
    if not titled:
        cue(f"theme_{int(tempo(part))}", th, timeline[0]["start"])
    last = timeline[-1]
    cl = close(part)
    cue(f"close_{int(tempo(part))}", cl, max(last["start"], last["start"] + last["duration"] - len(cl) / SR))
    return out
