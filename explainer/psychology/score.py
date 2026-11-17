"""The score of *Psychology, Built*: a little computed music under the films, so a fifty-minute lecture has a
shape you can hear.

Nothing is recorded and nothing is third-party: every note is synthesized here, deterministically, from sines (the
way *Music, Built* computes its sounds), and mixed into the master by ``tools/build.py`` through the same music-stem
path that series uses (the narration is mastered to -16 LUFS; these clips sit 8 to 18 LU below it).

Four cues, placed from the film's own timeline (each scene's start, length, chapter title and narration lines):

* **the theme** under the opening of Part N's hook: a motif that climbs the major pentatonic scale in six steps.
  It is the series' signature, and a small joke about Fechner, who counted sensation in equal steps;
* **a sting** at each chapter card: three notes of the motif over a soft chord, a different three for each
  chapter, so the ear hears the lecture turn a page;
* **the bed** in dead air: wherever the narration stops for longer than :data:`GAP_MIN` seconds inside a scene (an
  On-you pause, a long animation), a quiet sustained chord that breathes in and out (*psyche* is breath) fades in
  and out again before the voice returns;
* **the close** under the end of the outro: the motif coming back down to rest.

``cues(timeline, cache)`` returns cue dicts (``path``, ``start``, ``gain_db``, ``duration``, ``underscore``) that
``tools/build.py`` mixes into the music stem; ``python tools/build.py psychN --no-score`` leaves the score out.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

SR = 48_000
GAP_MIN = 2.6          # seconds of silence before the bed comes in
BED_EDGE = 0.35        # the bed starts this long after the voice stops, and ends this long before it returns
THEME_LUFS = -24.0     # the theme and the close, under the hook's and the outro's narration
STING_LUFS = -26.0     # the chapter stings, under "Chapter six. Goals."
BED_LUFS = -34.0       # the bed, alone in the room: present, never in the way

# D major pentatonic, from D3: the series' key
_SCALE = [146.83, 164.81, 185.00, 220.00, 246.94, 293.66, 329.63, 369.99, 440.00, 493.88, 587.33]
MOTIF = [5, 6, 7, 8, 9, 10]          # D4 E4 F#4 A4 B4 D5: up the scale in equal steps
CHORD = [0, 3, 7]                    # D3 A3 F#4: an open chord under everything
BED_CHORD = [0, 3, 6]                # D3 A3 E4: open, unresolved, for waiting


def _env(n: int, attack: float, release: float) -> np.ndarray:
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-3), 0, 1)
    r = np.clip((n / SR - t) / max(release, 1e-3), 0, 1)
    return (np.sin(a * np.pi / 2) ** 2) * (np.sin(r * np.pi / 2) ** 2)


def _note(hz: float, dur: float, decay: float = 1.6) -> np.ndarray:
    """A soft struck tone (an electric-piano-like bell): a few harmonics, each decaying faster than the last."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k, amp in ((1, 1.0), (2, 0.32), (3, 0.10), (4, 0.04)):
        y += amp * np.sin(2 * np.pi * hz * k * t) * np.exp(-t * k / decay)
    return y * _env(n, 0.006, 0.25)


def _pad(hzs, dur: float, attack: float = 0.9, release: float = 1.2, breathe: float = 0.0) -> np.ndarray:
    """A sustained chord: each note two slightly detuned sines, with a slow swell (``breathe`` Hz) if asked."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for i, hz in enumerate(hzs):
        for cents in (-4.0, 4.0):
            f = hz * 2 ** (cents / 1200)
            y += np.sin(2 * np.pi * f * t + 1.3 * i) / (1 + 0.6 * i)
    if breathe:
        y *= 0.72 + 0.28 * np.sin(2 * np.pi * breathe * t - np.pi / 2)
    return y * _env(n, attack, release)


def _stereo(y: np.ndarray, pan: float = 0.0) -> np.ndarray:
    th = (pan + 1) * np.pi / 4
    return np.stack([y * np.cos(th), y * np.sin(th)], axis=1)


def _place(out: np.ndarray, y: np.ndarray, at: float, pan: float = 0.0) -> None:
    a = int(at * SR)
    b = min(a + len(y), len(out))
    out[a:b] += _stereo(y[: b - a], pan)


def _lufs(y: np.ndarray) -> float:
    """Loudness of a stereo clip by BS.1770's K-weighting, ungated (the clips are short and dense)."""
    from scipy.signal import lfilter

    # the two K-weighting stages at 48 kHz (ITU-R BS.1770-4)
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    z = lfilter(b2, a2, lfilter(b1, a1, y, axis=0), axis=0)
    ms = float(np.mean(z ** 2, axis=0).sum())
    return -0.691 + 10 * np.log10(max(ms, 1e-12))


def _at(y: np.ndarray, lufs: float) -> np.ndarray:
    return (y * 10 ** ((lufs - _lufs(y)) / 20)).astype(np.float32)


def theme() -> np.ndarray:
    """The opening: the motif climbing over the open chord, about seven seconds."""
    out = np.zeros((int(7.5 * SR), 2))
    _place(out, 0.55 * _pad([_SCALE[i] for i in CHORD], 7.5, attack=1.2, release=2.0), 0.0)
    for k, i in enumerate(MOTIF):
        _place(out, _note(_SCALE[i], 2.6 if k < len(MOTIF) - 1 else 3.6), 0.6 + 0.42 * k, pan=-0.35 + 0.14 * k)
    return _at(out, THEME_LUFS)


def close() -> np.ndarray:
    """The ending: the motif coming back down, and the chord left to ring, about eight seconds."""
    out = np.zeros((int(8.0 * SR), 2))
    _place(out, 0.55 * _pad([_SCALE[i] for i in CHORD], 8.0, attack=1.0, release=3.0), 0.0)
    for k, i in enumerate(reversed(MOTIF)):
        _place(out, _note(_SCALE[i], 3.0 if k < len(MOTIF) - 1 else 4.5, decay=2.0), 0.4 + 0.5 * k,
               pan=0.35 - 0.14 * k)
    return _at(out, THEME_LUFS)


def sting(chapter: int) -> np.ndarray:
    """A chapter card: three rising notes of the motif, a different three for each chapter, over the chord."""
    start = [0, 2, 1, 3][chapter % 4]
    notes = MOTIF[start:start + 3]
    out = np.zeros((int(3.4 * SR), 2))
    _place(out, 0.45 * _pad([_SCALE[i] for i in CHORD], 3.4, attack=0.5, release=1.6), 0.0)
    for k, i in enumerate(notes):
        _place(out, _note(_SCALE[i], 2.4), 0.12 + 0.24 * k, pan=-0.2 + 0.2 * k)
    return _at(out, STING_LUFS)


def bed(seconds: float) -> np.ndarray:
    """Dead air: the open chord, breathing once every five seconds, fading in and out within ``seconds``."""
    fade = min(1.0, seconds / 3)
    y = _pad([_SCALE[i] for i in BED_CHORD], seconds, attack=fade, release=fade, breathe=0.2)
    return _at(_stereo(y), BED_LUFS)


def gaps(lines, duration: float, skip_head: float = 0.0, skip_tail: float = 0.0, minimum: float = GAP_MIN):
    """The silences inside a scene of ``duration`` seconds whose narration ``lines`` are ``{"start", "duration"}``
    (scene time): ``(start, end)`` pairs at least ``minimum`` long, outside the first ``skip_head`` and the last
    ``skip_tail`` seconds."""
    spans = sorted((float(l["start"]), float(l["start"]) + float(l["duration"])) for l in lines)
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
        Clip(np.asarray(y, np.float32), SR).write(path)
    return path


def cues(timeline, cache: Path) -> list[dict]:
    """The score for one film.  ``timeline``: the scenes in order, each ``{"cls", "chapter", "start", "duration",
    "lines"}`` (``start`` in film time; the lines' times within the scene).  Returns the music-stem cues."""
    cache = Path(cache) / "psychology_score_v1"
    out = []

    def cue(name, y, start):
        p = _write(y, cache / f"{name}.wav")
        out.append({"path": str(p), "start": float(start), "gain_db": 0.0, "duration": len(y) / SR,
                    "underscore": True, "label": f"score: {name}"})

    if not timeline:
        return out
    cue("theme", theme(), timeline[0]["start"])
    for k, s in enumerate(timeline):
        m = re.match(r"\s*(\d+)\.", s.get("chapter") or "")
        head = 0.0
        if k == 0:
            head = 7.5
        elif m:
            cue(f"sting{int(m.group(1)) % 4}", sting(int(m.group(1))), s["start"] + 0.05)
            head = 3.4
        tail = 8.0 if k == len(timeline) - 1 else 0.0
        for a, b in gaps(s.get("lines", []), s["duration"], skip_head=head, skip_tail=tail):
            secs = round(b - a - 2 * BED_EDGE, 1)
            cue(f"bed{secs:.1f}", bed(secs), s["start"] + a + BED_EDGE)
    last = timeline[-1]
    cue("close", close(), max(last["start"], last["start"] + last["duration"] - 8.0))
    return out
