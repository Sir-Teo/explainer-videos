"""The score of *Statistics, Built*: computed music that gives an hour-long lecture a shape you can hear, and never
plays under an explanation (videos/stats/SYLLABUS.md, section 1.2; Moreno & Mayer 2000).

Nothing is recorded and nothing is third-party. Every note is synthesized here, deterministically, from sines, and
mixed into the master by ``tools/build.py`` through the music-stem path that *Music, Built*, *Psychology, Built* and
*Computer Science, Built* use. The narration is mastered to -16 LUFS; these clips sit 8 to 20 LU below it.

The series' motif is **a Galton board you can hear**. A ball falls through the rows of pegs and every peg it strikes
sounds a note: a bounce to the right is one step up the C major pentatonic scale, a bounce to the left one step down.
The ball falls under gravity, so it passes row r at a time proportional to the square root of r and the notes come
faster as it drops. It lands in a bin, and the bins struck by many balls ring together as **the bell**: the chord whose
notes sound as loud as the binomial probabilities of their bins, the normal curve heard as a chord.

The degree's five stages each have their own instrument, so the ear hears the course grow up: a marimba for the
first-year foundations, a vibraphone for the methods, an electric piano for the master's, a celesta's glassy bars for
the PhD core, and a warm bell over a pad for the research stage. The four milestones (Parts 20, 42, 55 and 65) end on
a fuller close.

Seven cues, placed from the film's timeline (each scene's start, length, chapter title, narration lines, and the
marks its scene recorded, ``explainer.voiceover.VoiceoverScene.mark``):

* **the theme** at the ``title`` mark (after the cold open), or at the film's start if no scene recorded one: one
  ball falls along the part number's binary path, a flurry of balls fills the bins, and the bell rings, about 7.5 s;
* **a sting** at each chapter card: the chapter number's four binary digits as one ball's four bounces, then its bin;
* **a pulse** under every countdown (a prediction's, a checkpoint's): one soft peg click a second, the last one a note;
* **a chime** at every ``reveal`` (the right answer lit): the ball dropping into its bin;
* **a thud** at every ``strike`` (a wrong idea struck through): two low muted notes, falling;
* **the bed** in dead air: wherever the narration stops for more than :data:`GAP_MIN` seconds inside a scene (a run
  playing out, a pause for the problems), the bell's open chord, breathing, fading in and out before the voice returns;
* **the close** under the end of the outro: one ball rising back up the board, slowing, to rest on the tonic.

``cues(timeline, cache)`` returns cue dicts (``path``, ``start``, ``gain_db``, ``duration``, ``underscore``) for
``tools/build.py``; ``python tools/build.py statsN --no-score`` leaves the score out.
"""

from __future__ import annotations

import re
from math import comb
from pathlib import Path

import numpy as np

SR = 48_000
GAP_MIN = 2.6          # seconds of silence before the bed comes in
BED_EDGE = 0.35        # the bed starts this long after the voice stops, and ends this long before it returns
THEME_LUFS = -24.0     # the theme and the close: under the silent title card and the last words
STING_LUFS = -27.0     # the chapter stings, under "Chapter seven. The bootstrap."
PULSE_LUFS = -32.0     # a countdown's clicks
CHIME_LUFS = -30.0     # the answer's chime, the wrong idea's thud
BED_LUFS = -36.0       # the bed, alone in the room: present, never in the way
VERSION = "stats_score_v1"

# The five stages of the degree (explainer.stats.STAGES; tests/test_stats_score.py keeps the two in step)
STAGE_PARTS = [(1, 10), (11, 20), (21, 42), (43, 55), (56, 65)]
STAGE_VOICES = ["marimba", "vibraphone", "electric piano", "celesta", "bell and pad"]
MILESTONES = (20, 42, 55, 65)

# C major pentatonic, indexed by steps from C4 (step 0); the board's centre bin is the tonic
_PENT = [0, 2, 4, 7, 9]   # semitones of C D E G A
C4 = 261.6256


def pitch(step: int) -> float:
    """The frequency ``step`` pentatonic steps above (or below) C4."""
    octave, degree = divmod(step, 5)
    return C4 * 2 ** (octave + _PENT[degree] / 12)


def stage(part: int | None) -> int:
    """The stage (0-4) a part belongs to; the first stage when the part is unknown."""
    for i, (a, b) in enumerate(STAGE_PARTS):
        if part is not None and a <= part <= b:
            return i
    return 0


# ---------------------------------------------------------------------------- sound
def _env(n: int, attack: float, release: float) -> np.ndarray:
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-3), 0, 1)
    r = np.clip((n / SR - t) / max(release, 1e-3), 0, 1)
    return (np.sin(a * np.pi / 2) ** 2) * (np.sin(r * np.pi / 2) ** 2)


def note(hz: float, dur: float, voice: int = 0) -> np.ndarray:
    """One struck note in the stage's instrument (mono)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    if voice == 0:      # marimba: the fundamental, a quiet fourth harmonic that dies at once
        y = np.sin(2 * np.pi * hz * t) * np.exp(-t / 0.55)
        y += 0.25 * np.sin(2 * np.pi * hz * 4 * t) * np.exp(-t / 0.06)
        y += 0.06 * np.sin(2 * np.pi * hz * 10 * t) * np.exp(-t / 0.015)
    elif voice == 1:    # vibraphone: pure, long, with the motor's slow tremolo
        y = np.sin(2 * np.pi * hz * t) * np.exp(-t / 1.4)
        y += 0.18 * np.sin(2 * np.pi * hz * 4 * t) * np.exp(-t / 0.25)
        y *= 1.0 - 0.28 * (0.5 - 0.5 * np.cos(2 * np.pi * 5.2 * t))
    elif voice == 2:    # electric piano: a few harmonics, each decaying faster than the last
        y = np.zeros(n)
        for k, amp in ((1, 1.0), (2, 0.32), (3, 0.10), (4, 0.04)):
            y += amp * np.sin(2 * np.pi * hz * k * t) * np.exp(-t * k / 1.5)
    elif voice == 3:    # celesta: the inharmonic partials of a struck bar, bright and short
        y = np.zeros(n)
        for ratio, amp, dec in ((1.0, 1.0, 0.9), (2.756, 0.30, 0.25), (5.404, 0.12, 0.08), (2.0, 0.15, 0.5)):
            y += amp * np.sin(2 * np.pi * hz * ratio * t) * np.exp(-t / dec)
    else:               # bell and pad: a soft bell whose two detuned sines beat slowly
        y = np.zeros(n)
        for cents, amp in ((-4.0, 0.6), (4.0, 0.6)):
            f = hz * 2 ** (cents / 1200)
            y += amp * np.sin(2 * np.pi * f * t) * np.exp(-t / 2.2)
        y += 0.2 * np.sin(2 * np.pi * hz * 3 * t) * np.exp(-t / 0.6)
    return y * _env(n, 0.004, min(0.25, dur / 3))


def click(dur: float = 0.09, hz: float = 1800.0) -> np.ndarray:
    """A peg: a short wooden click (a tuned knock and a puff of noise)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(1876)  # Galton's quincunx, shown to the Royal Institution in 1874-77
    noise = rng.standard_normal(n) * np.exp(-t / 0.004)
    tone = np.sin(2 * np.pi * hz * t) * np.exp(-t / 0.012)
    return (0.3 * noise + tone) * _env(n, 0.001, 0.02)


def pad(hzs, dur: float, attack: float = 0.9, release: float = 1.2, breathe: float = 0.0, weights=None) -> np.ndarray:
    """A sustained chord: each note two slightly detuned sines, with a slow swell (``breathe`` Hz) if asked."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    weights = weights if weights is not None else [1.0 / (1 + 0.5 * i) for i in range(len(hzs))]
    for i, (hz, w) in enumerate(zip(hzs, weights)):
        for cents in (-5.0, 5.0):
            f = hz * 2 ** (cents / 1200)
            y += w * np.sin(2 * np.pi * f * t + 1.1 * i)
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


def lufs(y: np.ndarray) -> float:
    """Loudness of a stereo clip by BS.1770's K-weighting, ungated (the clips are short and dense)."""
    from scipy.signal import lfilter

    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    z = lfilter(b2, a2, lfilter(b1, a1, y, axis=0), axis=0)
    ms = float(np.mean(z ** 2, axis=0).sum())
    return -0.691 + 10 * np.log10(max(ms, 1e-12))


def _at(y: np.ndarray, target: float) -> np.ndarray:
    return (y * 10 ** ((target - lufs(y)) / 20)).astype(np.float32)


# ---------------------------------------------------------------------------- the board
def path(n: int, rows: int) -> list[int]:
    """The ball's bounces for the number ``n``: row r goes right (+1) when bit r of n is set, left (-1) otherwise."""
    return [1 if (n >> r) & 1 else -1 for r in range(rows)]


def fall_times(rows: int, seconds: float) -> list[float]:
    """When a ball dropped at time 0 strikes each row: a body falling from rest passes row r at sqrt(r / rows)."""
    return [seconds * np.sqrt((r + 1) / rows) for r in range(rows)]


def bell(rows: int) -> list[tuple[int, float]]:
    """The bell: each bin's step (centre bin the tonic) and its binomial probability."""
    return [(2 * k - rows, comb(rows, k) / 2 ** rows) for k in range(rows + 1)]


def _drop(out, bounces, at: float, seconds: float, voice: int, gain: float = 1.0) -> float:
    """One ball through the board from ``at``: a click and a note at every peg; returns its landing time and bin."""
    step = 0
    for t, b in zip(fall_times(len(bounces), seconds), bounces):
        step += b
        pan = float(np.clip(step / (len(bounces) + 1), -0.7, 0.7))
        _place(out, click(), at + t, pan=pan, gain=0.18 * gain)
        _place(out, note(pitch(step), 1.2, voice), at + t, pan=pan, gain=0.55 * gain)
    return step


def _land(out, step: int, at: float, voice: int, gain: float = 1.0, ring: float = 2.4) -> None:
    """The ball in its bin: its note again, louder, with the fifth below it."""
    pan = float(np.clip(step / 8, -0.6, 0.6))
    _place(out, note(pitch(step), ring, voice), at, pan=pan, gain=0.9 * gain)
    _place(out, note(pitch(step - 3), ring, voice), at + 0.02, pan=pan, gain=0.45 * gain)


def _bell_chord(out, at: float, dur: float, rows: int = 6, gain: float = 1.0, voice: int = 0) -> None:
    """The bell struck: every bin's note at the loudness of its probability, over a pad of the same shape."""
    weights = bell(rows)
    peak = max(w for _, w in weights)
    _place(out, pad([pitch(s) for s, _ in weights], dur, attack=0.7, release=min(2.5, dur / 2),
                     weights=[0.5 * w / peak for _, w in weights]), at, gain=gain)
    for j, (s, w) in enumerate(weights):
        _place(out, note(pitch(s), min(dur, 3.0), voice), at + 0.03 * j, pan=float(np.clip(s / 8, -0.6, 0.6)),
               gain=0.7 * gain * w / peak)


def theme(part: int | None = None) -> np.ndarray:
    """The opening, about 7.5 s: the part's own ball, a flurry filling the bins, and the bell."""
    v = stage(part)
    dur = 7.5
    out = np.zeros((int(dur * SR), 2))
    _place(out, pad([pitch(-5), pitch(-2), pitch(0)], dur, attack=1.2, release=2.2), 0.0, gain=0.35)
    land = _drop(out, path(part or 1, 6), 0.35, 1.7, v)
    _land(out, land, 0.35 + 1.75, v)
    rng = np.random.default_rng(1874 + (part or 0))
    for j in range(18):  # the flurry: only each ball's bin is heard, so the bins fill like a histogram
        bins = int(rng.binomial(6, 0.5))
        _place(out, note(pitch(2 * bins - 6), 0.9, v), 2.55 + 0.11 * j + 0.03 * rng.random(),
               pan=float(np.clip((2 * bins - 6) / 8, -0.6, 0.6)), gain=0.22)
    _bell_chord(out, 4.75, dur - 4.75, gain=1.0, voice=v)
    return _at(out, THEME_LUFS)


def close(part: int | None = None) -> np.ndarray:
    """The ending, about 8 s: the bell, then one ball rising back up the board, slowing, to rest on the tonic.
    A milestone part (BSc, MSc, candidacy, PhD) adds the octave above to its last chord."""
    v = stage(part)
    dur = 8.0
    out = np.zeros((int(dur * SR), 2))
    _bell_chord(out, 0.0, 3.2, gain=0.7, voice=v)
    bounces = path(part or 1, 6)
    steps = list(np.cumsum(bounces))[::-1]   # the landing bin first, back up to the top
    times = [1.4 + 2.4 * (1 - np.sqrt(1 - (k + 1) / (len(steps) + 1))) for k in range(len(steps))]
    for t, s in zip(times, steps):
        _place(out, note(pitch(int(s)), 1.6, v), t, pan=float(np.clip(s / 8, -0.6, 0.6)), gain=0.5)
    end = 1.4 + 2.4 + 0.45
    _place(out, pad([pitch(-10), pitch(-5), pitch(0), pitch(2)], dur - end + 0.4, attack=0.6, release=2.5),
           end - 0.4, gain=0.4)
    _land(out, 0, end, v, ring=3.5)
    if part in MILESTONES:
        _place(out, note(pitch(5), 3.5, v), end + 0.12, gain=0.55)
        _place(out, note(pitch(8), 3.5, v), end + 0.24, gain=0.4)
    return _at(out, THEME_LUFS)


def sting(chapter: int, part: int | None = None) -> np.ndarray:
    """A chapter card, about 3 s: chapter n's four binary digits as one ball's four bounces, then its bin."""
    v = stage(part)
    n = chapter % 16
    out = np.zeros((int(3.0 * SR), 2))
    _place(out, pad([pitch(-5), pitch(-2), pitch(0)], 3.0, attack=0.4, release=1.4), 0.0, gain=0.3)
    land = _drop(out, path(n, 4), 0.06, 0.9, v)
    _land(out, land, 1.0, v, ring=2.0)
    return _at(out, STING_LUFS)


def pulse(seconds: float, part: int | None = None) -> np.ndarray:
    """Under a countdown: one soft peg click a second, then the tonic on the last beat."""
    k = max(1, int(round(seconds)))
    out = np.zeros((int((k + 0.9) * SR), 2))
    for j in range(k):
        _place(out, click(dur=0.08, hz=1500.0 + 150 * j), j * 1.0, gain=0.8)
    _place(out, note(pitch(5), 0.9, stage(part)), k * 1.0 - 0.04, gain=0.6)
    return _at(out, PULSE_LUFS)


def chime(part: int | None = None) -> np.ndarray:
    """The answer lit: a ball's last two bounces and its bin, rising to the tonic, about 1.6 s."""
    v = stage(part)
    out = np.zeros((int(1.6 * SR), 2))
    _place(out, note(pitch(3), 1.2, v), 0.0, pan=0.2, gain=0.6)
    _place(out, note(pitch(4), 1.2, v), 0.09, pan=0.25, gain=0.6)
    _place(out, note(pitch(5), 1.4, v), 0.18, pan=0.1, gain=0.9)
    return _at(out, CHIME_LUFS)


def thud(part: int | None = None) -> np.ndarray:
    """A wrong idea struck through: two low muted notes, falling a step, about 1.2 s."""
    v = stage(part)
    out = np.zeros((int(1.2 * SR), 2))
    for j, s in enumerate((-6, -7)):
        y = note(pitch(s), 0.6, v) * np.exp(-np.arange(int(0.6 * SR)) / SR / 0.12)
        _place(out, y, 0.13 * j, gain=1.0)
    return _at(out, CHIME_LUFS)


def bed(seconds: float) -> np.ndarray:
    """Dead air: the bell's open chord (C, G, E), breathing once every five seconds, fading in and out."""
    fade = min(1.0, seconds / 3)
    y = pad([pitch(-5), pitch(-2), pitch(2)], seconds, attack=fade, release=fade, breathe=0.2)
    return _at(_stereo(y), BED_LUFS)


# ---------------------------------------------------------------------------- placing the cues
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
        m = re.fullmatch(r"stats(\d+)", s.get("video", "") or "")
        if m:
            return int(m.group(1))
    return None


ROMAN = {"I": 1, "V": 5, "X": 10}


def chapter_number(title: str) -> int | None:
    """A numbered chapter's number ("7. The bootstrap" -> 7; an exam section, "III. Testing" -> 3), else None."""
    m = re.match(r"\s*(\d+)\.\s", title)
    if m:
        return int(m.group(1))
    m = re.match(r"\s*([IVX]+)\.\s", title)
    if not m:
        return None
    vals = [ROMAN[c] for c in m.group(1)]
    return sum(-v if i + 1 < len(vals) and v < vals[i + 1] else v for i, v in enumerate(vals))


COUNTDOWN = re.compile(r"countdown(?::(\d+(?:\.\d+)?))?$")


def cues(timeline, cache: Path, part: int | None = None) -> list[dict]:
    """The score for one film.  ``timeline``: the scenes in order, each ``{"video", "cls", "chapter", "start",
    "duration", "lines", "marks"}`` (``start`` in film time; lines and marks in scene time).  Returns the
    music-stem cues, in film order."""
    cache = Path(cache) / VERSION
    part = part if part is not None else _part(timeline)
    v = stage(part)
    out = []

    def cue(name, y, start):
        p = _write(y, cache / f"{name}.wav")
        out.append({"path": str(p), "start": float(start), "gain_db": 0.0, "duration": len(y) / SR,
                    "underscore": True, "label": f"score: {name}"})
        return len(y) / SR

    if not timeline:
        return out
    titled = False
    tag = f"p{part or 0}"
    for k, s in enumerate(timeline):
        busy = []
        n = chapter_number(s.get("chapter") or "")
        head = 0.0
        if n is not None:
            d = cue(f"sting{n % 16}_s{v}", sting(n, part), s["start"] + 0.05)
            head = d + 0.05
        for mk in s.get("marks", []):
            t, name = float(mk["time"]), str(mk["name"])
            cd = COUNTDOWN.match(name)
            if name == "title" and not titled:
                d = cue(f"theme_{tag}", theme(part), s["start"] + t)
                busy.append((t, t + d))
                titled = True
            elif cd:
                secs = int(round(float(cd.group(1) or 3)))
                d = cue(f"pulse{secs}_s{v}", pulse(secs, part), s["start"] + t)
                busy.append((t, t + d))
            elif name == "reveal":
                d = cue(f"chime_s{v}", chime(part), s["start"] + t)
                busy.append((t, t + d))
            elif name == "strike":
                d = cue(f"thud_s{v}", thud(part), s["start"] + t)
                busy.append((t, t + d))
        tail = 8.0 if k == len(timeline) - 1 else 0.0
        for a, b in gaps(s.get("lines", []), s["duration"], skip_head=head, skip_tail=tail, busy=busy):
            secs = round(b - a - 2 * BED_EDGE, 1)
            if secs >= 1.5:
                cue(f"bed{secs:.1f}", bed(secs), s["start"] + a + BED_EDGE)
    if not titled:
        cue(f"theme_{tag}", theme(part), timeline[0]["start"])
    last = timeline[-1]
    cl = close(part)
    cue(f"close_{tag}", cl, max(last["start"], last["start"] + last["duration"] - len(cl) / SR))
    return sorted(out, key=lambda c: c["start"])
