"""Clips: the unit of sound in *Music, Built*.

A :class:`Clip` is an array of samples at 48 kHz (mono ``(n,)`` or stereo ``(n, 2)``, float, full scale 1.0) with

* ``events``: named moments in seconds (``{"note3": 1.25, "bar2": 2.0}``), so a scene can time a picture to the
  sound the way it times one to a narrated word;
* ``notes``: optional ``{"t", "dur", "hz", "name"}`` rows, for a staff, a piano roll or a moving finger;
* ``meta``: how it was made (what the on-screen label says: ``physical model``, ``synthesized``, ...).

Clips are produced by a part's ``compute.py`` and kept by a :class:`ClipStore` under ``.cache/<part>/audio/`` as a
float WAV and a JSON sidecar.  A clip is cached exactly when its ``.json`` exists (it is written last).
"""

from __future__ import annotations

import json
import wave
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SR = 48_000  # the series' sample rate
# Levels are set by the loudest 400 ms of a clip (Clip.at_level), in LUFS.  The narration is mastered to -16 LUFS
# integrated, whose loudest moments read about -12.
EXAMPLE_LEVEL = -15.0  # an example in a listening window
QUIET_LEVEL = -21.0    # an example meant to sit back, or to run under narration


@dataclass
class Clip:
    y: np.ndarray
    sr: int = SR
    events: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        self.y = np.asarray(self.y, dtype=np.float32)
        if self.y.ndim == 2 and self.y.shape[1] == 1:
            self.y = self.y[:, 0]
        if self.y.ndim not in (1, 2) or (self.y.ndim == 2 and self.y.shape[1] != 2):
            raise ValueError(f"a clip is (n,) or (n, 2), not {self.y.shape}")
        if not np.isfinite(self.y).all():
            raise ValueError("a clip must be finite")

    # -- shape ----------------------------------------------------------
    @property
    def n(self) -> int:
        return self.y.shape[0]

    @property
    def duration(self) -> float:
        return self.n / self.sr

    @property
    def channels(self) -> int:
        return 1 if self.y.ndim == 1 else 2

    @property
    def mono(self) -> np.ndarray:
        """The mid signal, ``(n,)``."""
        return self.y if self.y.ndim == 1 else self.y.mean(axis=1)

    @property
    def stereo(self) -> np.ndarray:
        """``(n, 2)``; a mono clip is placed in the centre at equal power (-3 dB in each channel)."""
        if self.y.ndim == 2:
            return self.y
        return np.repeat(self.y[:, None], 2, axis=1) * np.float32(np.sqrt(0.5))

    @property
    def peak(self) -> float:
        return float(np.abs(self.y).max()) if self.n else 0.0

    @property
    def peak_db(self) -> float:
        return 20 * np.log10(max(self.peak, 1e-12))

    @property
    def rms_db(self) -> float:
        return 10 * np.log10(max(float(np.mean(np.square(self.mono, dtype=np.float64))), 1e-24)) if self.n else -240.0

    # -- edits (each returns a new clip) --------------------------------
    def _with(self, y, events=None, notes=None, meta=None) -> "Clip":
        return Clip(y, self.sr, dict(self.events if events is None else events),
                    [dict(n) for n in (self.notes if notes is None else notes)],
                    dict(self.meta if meta is None else meta))

    def gain(self, db: float) -> "Clip":
        return self._with(self.y * np.float32(10 ** (db / 20)))

    def fade(self, fade_in: float = 0.005, fade_out: float = 0.02) -> "Clip":
        """Raised-cosine fades (seconds), so that no clip starts or ends on a step."""
        y = self.y.copy()
        for secs, sl, ramp in ((fade_in, slice(None), 1), (fade_out, slice(None), -1)):
            k = min(int(round(secs * self.sr)), self.n)
            if k <= 1:
                continue
            w = (0.5 - 0.5 * np.cos(np.pi * np.arange(k) / k)).astype(np.float32)
            if ramp < 0:
                w = w[::-1]
            idx = slice(0, k) if ramp > 0 else slice(self.n - k, self.n)
            y[idx] = y[idx] * (w if y.ndim == 1 else w[:, None])
        return self._with(y)

    def pad(self, before: float = 0.0, after: float = 0.0) -> "Clip":
        a, b = int(round(before * self.sr)), int(round(after * self.sr))
        shape = (a,) if self.y.ndim == 1 else (a, 2)
        shape_b = (b,) if self.y.ndim == 1 else (b, 2)
        y = np.concatenate([np.zeros(shape, np.float32), self.y, np.zeros(shape_b, np.float32)])
        shift = a / self.sr
        return self._with(y, {k: v + shift for k, v in self.events.items()},
                          [{**n, "t": n["t"] + shift} for n in self.notes])

    def trim(self, start: float = 0.0, end: float | None = None) -> "Clip":
        a = int(round(start * self.sr))
        b = self.n if end is None else int(round(end * self.sr))
        dur = (b - a) / self.sr
        ev = {k: v - start for k, v in self.events.items() if 0 <= v - start <= dur}
        notes = [{**n, "t": n["t"] - start} for n in self.notes if 0 <= n["t"] - start < dur]
        return self._with(self.y[a:b], ev, notes)

    def at_lufs(self, target: float) -> "Clip":
        """The clip scaled to an integrated loudness (ITU-R BS.1770)."""
        from .loudness import integrated

        now = integrated(self)
        if not np.isfinite(now):
            return self
        return self.gain(target - now)

    def at_level(self, target: float = EXAMPLE_LEVEL) -> "Clip":
        """The clip scaled so that its loudest 400 ms reads ``target`` LUFS (BS.1770 momentary loudness).  This is
        how the series sets the level of an example: a note that dies away and a sustained tone then sound about
        equally loud, which integrated loudness (an average over the whole clip) does not give."""
        from .loudness import momentary_max

        now = momentary_max(self)
        if not np.isfinite(now):
            return self
        return self.gain(target - now)

    def at_peak(self, db: float) -> "Clip":
        return self.gain(db - self.peak_db) if self.peak > 0 else self

    def label(self, kind: str, **more) -> "Clip":
        """Record what the on-screen label must say: ``physical model``, ``synthesized``, ``illustrative``."""
        return self._with(self.y, meta={**self.meta, "label": kind, **more})

    # -- files ----------------------------------------------------------
    def write(self, path: Path) -> None:
        """A 32-bit float WAV (format 3), written with the standard library so nothing else is needed."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = np.ascontiguousarray(self.y, dtype="<f4").tobytes()
        ch = self.channels
        import struct

        fmt = struct.pack("<HHIIHH", 3, ch, self.sr, self.sr * ch * 4, ch * 4, 32)
        fact = struct.pack("<I", self.n)
        body = (b"WAVE" + b"fmt " + struct.pack("<I", len(fmt)) + fmt + b"fact" + struct.pack("<I", 4) + fact
                + b"data" + struct.pack("<I", len(data)) + data)
        tmp = path.with_suffix(".tmp.wav")
        tmp.write_bytes(b"RIFF" + struct.pack("<I", len(body)) + body)
        tmp.replace(path)

    def write_pcm16(self, path: Path) -> None:
        """A 16-bit PCM WAV with triangular dither: for tools that read nothing else (previews)."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        rng = np.random.default_rng(0)
        y = self.y.astype(np.float64) * 32767.0
        y = y + rng.random(y.shape) - rng.random(y.shape)
        pcm = np.clip(np.round(y), -32768, 32767).astype("<i2")
        with wave.open(str(path), "wb") as f:
            f.setnchannels(self.channels)
            f.setsampwidth(2)
            f.setframerate(self.sr)
            f.writeframes(pcm.tobytes())

    @staticmethod
    def read(path: Path) -> "Clip":
        """Read a WAV written by :meth:`write` (float32) or a 16-bit PCM one."""
        import struct

        raw = Path(path).read_bytes()
        if raw[:4] != b"RIFF" or raw[8:12] != b"WAVE":
            raise ValueError(f"{path} is not a WAV file")
        pos, fmt, data = 12, None, None
        while pos + 8 <= len(raw):
            tag, size = raw[pos:pos + 4], struct.unpack("<I", raw[pos + 4:pos + 8])[0]
            chunk = raw[pos + 8:pos + 8 + size]
            if tag == b"fmt ":
                fmt = struct.unpack("<HHIIHH", chunk[:16])
            elif tag == b"data":
                data = chunk
            pos += 8 + size + (size & 1)
        if fmt is None or data is None:
            raise ValueError(f"{path}: no fmt or data chunk")
        code, ch, sr, _, _, bits = fmt
        if code == 3 and bits == 32:
            y = np.frombuffer(data, dtype="<f4").astype(np.float32)
        elif code == 1 and bits == 16:
            y = np.frombuffer(data, dtype="<i2").astype(np.float32) / 32768.0
        else:
            raise ValueError(f"{path}: unsupported WAV (format {code}, {bits} bits)")
        if ch == 2:
            y = y.reshape(-1, 2)
        elif ch != 1:
            raise ValueError(f"{path}: {ch} channels")
        return Clip(y, sr)


def silence(seconds: float, sr: int = SR) -> Clip:
    return Clip(np.zeros(int(round(seconds * sr)), np.float32), sr)


def concat(clips, gap: float = 0.0, names=None) -> Clip:
    """Clips end to end with ``gap`` seconds between them.  Each clip's events are kept under ``<name>.<event>`` and
    its start as ``<name>`` (``names`` defaults to ``c0``, ``c1``, ...)."""
    clips = list(clips)
    names = list(names) if names is not None else [f"c{i}" for i in range(len(clips))]
    sr = clips[0].sr
    stereo = any(c.channels == 2 for c in clips)
    parts, events, notes, t = [], {}, [], 0.0
    for i, (name, c) in enumerate(zip(names, clips)):
        if c.sr != sr:
            raise ValueError("clips of different sample rates")
        y = c.stereo if stereo else c.y
        parts.append(y)
        events[name] = t
        events.update({f"{name}.{k}": v + t for k, v in c.events.items()})
        notes += [{**n, "t": n["t"] + t} for n in c.notes]
        t += c.duration
        if gap and i < len(clips) - 1:
            g = int(round(gap * sr))
            parts.append(np.zeros((g, 2) if stereo else (g,), np.float32))
            t += g / sr
    events["end"] = t
    return Clip(np.concatenate(parts), sr, events, notes)


def mix(placed, sr: int = SR, duration: float | None = None) -> Clip:
    """``placed``: ``(clip, start seconds)`` or ``(clip, start, gain dB)`` or ``(clip, start, gain dB, pan)`` with
    pan from -1 (left) to +1 (right), constant power.  The sum, stereo if any clip is stereo or panned."""
    rows = []
    for item in placed:
        c, start, *rest = item
        g = rest[0] if rest else 0.0
        pan = rest[1] if len(rest) > 1 else None
        rows.append((c, float(start), float(g), pan))
    stereo = any(c.channels == 2 or pan is not None for c, _, _, pan in rows)
    end = max((s + c.duration for c, s, _, _ in rows), default=0.0)
    n = int(round((duration if duration is not None else end) * sr))
    out = np.zeros((n, 2) if stereo else (n,), np.float64)
    events, notes = {}, []
    for c, start, g, pan in rows:
        if c.sr != sr:
            raise ValueError("clips of different sample rates")
        a = int(round(start * sr))
        y = c.y.astype(np.float64) * 10 ** (g / 20)
        if stereo:
            if pan is not None:
                th = (pan + 1) * np.pi / 4
                y = np.stack([c.mono * 10 ** (g / 20) * np.cos(th), c.mono * 10 ** (g / 20) * np.sin(th)], axis=1)
            elif c.channels == 1:
                y = np.repeat(y[:, None], 2, axis=1) * np.sqrt(0.5)
        b = min(a + len(y), n)
        if b > a:
            out[a:b] += y[: b - a]
        events.update({k: v + start for k, v in c.events.items()})
        notes += [{**nn, "t": nn["t"] + start} for nn in c.notes]
    return Clip(out, sr, events, sorted(notes, key=lambda r: r["t"]))


class ClipStore:
    """The clips of one part: ``.cache/<part>/audio/<name>.wav`` and ``.json``."""

    def __init__(self, part: str, root: Path | None = None):
        self.part = part
        self.dir = (Path(root) if root else Path(__file__).resolve().parents[3] / ".cache" / part) / "audio"
        self._loaded: dict = {}

    def wav(self, name: str) -> Path:
        return self.dir / f"{name}.wav"

    def has(self, name: str) -> bool:
        return self.wav(name).with_suffix(".json").exists() and self.wav(name).exists()

    def save(self, name: str, clip: Clip) -> str:
        clip.write(self.wav(name))
        clip.write_pcm16(self.wav(name).with_suffix(".pcm.wav"))
        side = {"sr": clip.sr, "n": clip.n, "channels": clip.channels, "duration": clip.duration,
                "peak_db": round(clip.peak_db, 2), "events": clip.events, "notes": clip.notes, "meta": clip.meta}
        tmp = self.wav(name).with_suffix(".tmp.json")
        tmp.write_text(json.dumps(side, indent=1, default=float))
        tmp.replace(self.wav(name).with_suffix(".json"))
        self._loaded.pop(name, None)
        return name

    def load(self, name: str) -> Clip:
        if name not in self._loaded:
            if not self.has(name):
                raise FileNotFoundError(f"no clip {name!r} in {self.dir}")
            side = json.loads(self.wav(name).with_suffix(".json").read_text())
            c = Clip.read(self.wav(name))
            c.events, c.notes, c.meta = side["events"], side["notes"], side["meta"]
            c.meta["name"], c.meta["path"] = name, str(self.wav(name))
            self._loaded[name] = c
        return self._loaded[name]
