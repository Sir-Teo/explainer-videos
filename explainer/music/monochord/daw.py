"""Monochord's studio (Part 53 of *Music, Built*): MIDI byte by byte, MIDI files, a sequencer and an audio graph that
run identically offline and in blocks, a small pattern language, a tracker, and tempo canons.

    note_on, note_off, control, bend         MIDI 1.0 channel messages as bytes
    encode(events, running=True)             a timed message list as a byte stream, with or without running status
    decode(stream)                           the stream back into messages (running status understood)
    wire_times(stream, t0)                   when each byte arrives down a 31,250-baud cable (ten bits a byte)
    vlq / unvlq                              variable-length quantities, as in MIDI files
    write_smf / read_smf                     a Standard MIDI File (format 1) with a tempo map, and back
    Engine                                   voices (oscillator, envelope, filter), a mixer and effects, run in blocks
                                             of any size; events placed to the sample, or snapped to block starts
    parse_pattern(text)                      a small mini-notation: spaces split a cycle, [ ] subdivide, ~ rests,
                                             x*n repeats, <a b> alternates from cycle to cycle
    tracker_events(rows, ...)                a tracker's rows (note, instrument, effect) as events
    tempo_canon(notes, ratios, converge)     voices at different tempos, started so they meet on one note

No manim here.  Checked in ``tests/music/test_daw.py``.
"""

from __future__ import annotations

import math
import re
import struct
from dataclasses import dataclass, field

import numpy as np

try:  # the loops below are compiled when numba is there; they are the same loops without it
    from numba import njit
except Exception:  # pragma: no cover
    def njit(*a, **k):
        def wrap(f):
            return f
        return wrap(a[0]) if a and callable(a[0]) else wrap

SR = 48000
BAUD = 31250
BYTE_S = 10 / BAUD             # a start bit, eight data bits, a stop bit: 320 microseconds

# --------------------------------------------------------------------------------------------- MIDI messages


def note_on(ch: int, key: int, vel: int) -> bytes:
    return bytes([0x90 | (ch & 15), key & 127, vel & 127])


def note_off(ch: int, key: int, vel: int = 0) -> bytes:
    return bytes([0x80 | (ch & 15), key & 127, vel & 127])


def control(ch: int, cc: int, value: int) -> bytes:
    return bytes([0xB0 | (ch & 15), cc & 127, value & 127])


def bend(ch: int, value: int) -> bytes:
    """Pitch bend: a 14-bit value, 8192 at rest, sent least significant seven bits first."""
    v = max(0, min(16383, int(value)))
    return bytes([0xE0 | (ch & 15), v & 127, v >> 7])


def encode(messages, running: bool = True) -> bytes:
    """Concatenate messages; with running status a status byte equal to the last one is left out (and a note-off may
    be sent as a note-on with velocity 0 to keep the status the same)."""
    out = bytearray()
    last = None
    for m in messages:
        m = bytes(m)
        st = m[0]
        if running and st & 0xF0 == 0x80:                     # a note-off as a note-on with velocity 0
            st = 0x90 | (st & 15)
            m = bytes([st, m[1], 0])
        if running and st == last:
            out += m[1:]
        else:
            out += m
        last = st
    return bytes(out)


DATA_LEN = {0x80: 2, 0x90: 2, 0xA0: 2, 0xB0: 2, 0xC0: 1, 0xD0: 1, 0xE0: 2}


def decode(stream: bytes) -> list[tuple]:
    """(kind, channel, a, b) for each message; a data byte where a status byte is expected reuses the last status."""
    out = []
    i = 0
    status = None
    while i < len(stream):
        b = stream[i]
        if b & 0x80:
            status = b
            i += 1
        if status is None:
            raise ValueError("data byte with no status")
        n = DATA_LEN[status & 0xF0]
        d = stream[i:i + n]
        i += n
        kind = {0x80: "off", 0x90: "on", 0xA0: "aftertouch", 0xB0: "cc", 0xC0: "program", 0xD0: "pressure", 0xE0: "bend"}[status & 0xF0]
        if kind == "on" and d[1] == 0:
            kind = "off"
        out.append((kind, status & 15, d[0], d[1] if n > 1 else None))
    return out


def wire_times(stream: bytes, t0: float = 0.0) -> np.ndarray:
    """The moment each byte has fully arrived, sent back to back at 31,250 bits a second."""
    return t0 + BYTE_S * np.arange(1, len(stream) + 1)


# --------------------------------------------------------------------------------------------- MIDI files


def vlq(n: int) -> bytes:
    """A variable-length quantity: seven bits a byte, the top bit set on every byte but the last."""
    if n < 0:
        raise ValueError(n)
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append(0x80 | (n & 0x7F))
        n >>= 7
    return bytes(reversed(out))


def unvlq(data: bytes, i: int) -> tuple[int, int]:
    n = 0
    while True:
        b = data[i]
        i += 1
        n = (n << 7) | (b & 0x7F)
        if not b & 0x80:
            return n, i


def write_smf(tracks, division: int = 480, tempo_us: int = 500000) -> bytes:
    """``tracks``: lists of (tick, message bytes).  Format 1: a first track with the tempo, then one per list; each
    event preceded by its delta time as a variable-length quantity; running status inside each track."""
    def chunk(tag, body):
        return tag + struct.pack(">I", len(body)) + body
    t0 = vlq(0) + bytes([0xFF, 0x51, 0x03]) + tempo_us.to_bytes(3, "big") + vlq(0) + bytes([0xFF, 0x2F, 0x00])
    out = chunk(b"MThd", struct.pack(">HHH", 1, len(tracks) + 1, division)) + chunk(b"MTrk", t0)
    for tr in tracks:
        body = bytearray()
        last_tick = 0
        last_status = None
        for tick, msg in sorted(tr, key=lambda e: (e[0], e[1][0] & 0xF0 != 0x80)):
            body += vlq(tick - last_tick)
            last_tick = tick
            msg = bytes(msg)
            if msg[0] == last_status:
                body += msg[1:]
            else:
                body += msg
                last_status = msg[0]
        body += vlq(0) + bytes([0xFF, 0x2F, 0x00])
        out += chunk(b"MTrk", bytes(body))
    return out


def read_smf(data: bytes) -> dict:
    """Header, tempo and every channel message with its tick and its time in seconds (one tempo)."""
    if data[:4] != b"MThd":
        raise ValueError("not a MIDI file")
    fmt, ntr, division = struct.unpack(">HHH", data[8:14])
    i = 14
    tempo = 500000
    events = []
    for _ in range(ntr):
        assert data[i:i + 4] == b"MTrk"
        L = struct.unpack(">I", data[i + 4:i + 8])[0]
        j, end = i + 8, i + 8 + L
        tick = 0
        status = None
        while j < end:
            dt, j = unvlq(data, j)
            tick += dt
            b = data[j]
            if b == 0xFF:
                typ = data[j + 1]
                ln, k = unvlq(data, j + 2)
                if typ == 0x51:
                    tempo = int.from_bytes(data[k:k + ln], "big")
                j = k + ln
                continue
            if b & 0x80:
                status = b
                j += 1
            n = DATA_LEN[status & 0xF0]
            msg = bytes([status]) + data[j:j + n]
            j += n
            events.append((tick, msg))
        i = end
    sec = tempo / 1e6 / division
    return {"format": fmt, "tracks": ntr, "division": division, "tempo_us": tempo,
            "events": [(t, m, t * sec) for t, m in sorted(events, key=lambda e: e[0])]}


# --------------------------------------------------------------------------------------------- the engine


@njit(cache=True)
def _voice_block(n, sr, f, ph, env, stage, rel_at, a, d, s, r, z, g, cut, vel, out, start):
    """One voice for ``n`` samples from ``start`` in the output: a PolyBLEP sawtooth, a linear-attack and exponential
    decay/release envelope, a one-pole low-pass.  Returns the state."""
    dt = f / sr
    ca = 1.0 / max(a * sr, 1.0)
    cd = math.exp(-1.0 / max(d * sr, 1.0))
    cr = math.exp(-1.0 / max(r * sr, 1.0))
    gk = 1.0 - math.exp(-2.0 * math.pi * cut / sr)
    for i in range(n):
        if stage == 3:
            break
        if stage == 0:
            env += ca
            if env >= 1.0:
                env = 1.0
                stage = 1
        elif stage == 1:
            env = s + (env - s) * cd
        else:
            env *= cr
            if env < 1e-5:                # silent: the voice ends here, at this sample, whatever the block size
                stage = 3
                env = 0.0
        if rel_at == 0 and stage < 2:
            stage = 2
        if rel_at > 0:
            rel_at -= 1
        ph += dt
        if ph >= 1.0:
            ph -= 1.0
        x = 2.0 * ph - 1.0
        if ph < dt:
            u = ph / dt
            x -= u + u - u * u - 1.0
        elif ph > 1.0 - dt:
            u = (ph - 1.0) / dt
            x -= u * u + u + u + 1.0
        z += gk * (x - z)
        out[start + i] += g * vel * env * z
    return ph, env, stage, rel_at, z


@dataclass
class Voice:
    f: float
    vel: float
    length: int                    # samples until the key is released
    a: float = 0.005
    d: float = 0.25
    s: float = 0.5
    r: float = 0.12
    cut: float = 3000.0
    gain: float = 0.25
    ph: float = 0.0
    env: float = 0.0
    stage: int = 0
    z: float = 0.0
    done: bool = False

    def run(self, out, start, n, sr):
        self.ph, self.env, self.stage, self.length, self.z = _voice_block(n, float(sr), self.f, self.ph, self.env, self.stage, self.length,
                                                                          self.a, self.d, self.s, self.r, self.z, self.gain, self.cut, self.vel, out, start)
        if self.stage == 3:
            self.done = True


@njit(cache=True)
def _delay_block(x, buf, w, D):
    """A delay of D samples through a circular buffer; returns the write position."""
    n = len(buf)
    for i in range(len(x)):
        buf[w] = x[i]
        x[i] = buf[(w - D) % n]
        w = (w + 1) % n
    return w


class Delay:
    """A plain delay: the processing graph's latency, or delay compensation for a parallel path."""

    def __init__(self, samples: int):
        self.D = int(samples)
        self.buf = np.zeros(max(self.D + 1, 2))
        self.w = 0

    def process(self, x):
        if self.D == 0:
            return x
        self.w = _delay_block(x, self.buf, self.w, self.D)
        return x


@njit(cache=True)
def _lookahead_block(x, buf, w, D, env, rel, ceil, out):
    """A look-ahead limiter: the gain follows the loudest sample of the next D, so no peak passes the ceiling; the
    signal itself is delayed by D samples (the plug-in's latency)."""
    n = len(buf)
    for i in range(len(x)):
        buf[w] = x[i]
        peak = 0.0
        for k in range(D + 1):
            v = abs(buf[(w - k) % n])
            if v > peak:
                peak = v
        target = 1.0 if peak <= ceil else ceil / peak
        if target < env:
            env = target
        else:
            env = target + (env - target) * rel
        out[i] = buf[(w - D) % n] * env
        w = (w + 1) % n
    return w, env


class Limiter:
    def __init__(self, lookahead: int, ceiling: float = 0.25, release_s: float = 0.08, sr: float = SR):
        self.D = int(lookahead)
        self.buf = np.zeros(self.D + 2)
        self.w = 0
        self.env = 1.0
        self.rel = math.exp(-1.0 / (release_s * sr))
        self.ceil = ceiling

    @property
    def latency(self) -> int:
        return self.D

    def process(self, x):
        out = np.empty_like(x)
        self.w, self.env = _lookahead_block(x, self.buf, self.w, self.D, self.env, self.rel, self.ceil, out)
        return out


@dataclass
class Engine:
    """Events (sample time, key, velocity, length in samples, track) drive voices; each track is a bus that may pass
    through a chain of processors; the buses are summed.  ``quantize=True`` starts each event at the start of the
    block it falls in, as a sequencer that only looks at the clock once a block would."""

    events: list
    sr: float = SR
    tracks: dict = field(default_factory=dict)          # track name -> dict(voice kwargs) and "chain": [processors]
    quantize: bool = False

    def render(self, n_total: int, block: int | None = None, timings: list | None = None) -> np.ndarray:
        import time as _t
        block = block or n_total
        ev = sorted(self.events, key=lambda e: e[0])
        k = 0
        active: list[tuple[str, Voice]] = []
        out = np.zeros(n_total)
        names = list(self.tracks) or ["main"]
        for b0 in range(0, n_total, block):
            t_start = _t.perf_counter()
            n = min(block, n_total - b0)
            while k < len(ev) and ev[k][0] < b0 + n:
                t, key, vel, length, tr = ev[k]
                start = b0 if self.quantize else t
                kw = {kk: vv for kk, vv in self.tracks.get(tr, {}).items() if kk != "chain"}
                v = Voice(f=440.0 * 2 ** ((key - 69) / 12), vel=vel, length=int(length), **kw)
                active.append((tr, v, start))
                k += 1
            buses = {nm: np.zeros(n) for nm in names}
            keep = []
            for tr, v, start in active:
                off = max(start - b0, 0)
                v.run(buses[tr], off, n - off, self.sr)
                if not v.done:
                    keep.append((tr, v, b0 + n))
            active = keep
            mix = np.zeros(n)
            for nm in names:
                y = buses[nm]
                for proc in self.tracks.get(nm, {}).get("chain", []):
                    y = proc.process(y)
                mix += y
            out[b0:b0 + n] = mix
            if timings is not None:
                timings.append(_t.perf_counter() - t_start)
        return out


# --------------------------------------------------------------------------------------------- a pattern language


def _tokens(text: str):
    return re.findall(r"\[|\]|<|>|[^\s\[\]<>]+", text)


def _parse(tokens, i, close):
    items = []
    while i < len(tokens) and tokens[i] != close:
        t = tokens[i]
        if t == "[":
            sub, i = _parse(tokens, i + 1, "]")
            items.append(("seq", sub))
        elif t == "<":
            sub, i = _parse(tokens, i + 1, ">")
            items.append(("alt", sub))
        else:
            m = re.fullmatch(r"([^*]+)\*(\d+)", t)
            if m:
                items.append(("seq", [("atom", m.group(1))] * int(m.group(2))))
            else:
                items.append(("atom", t))
        i += 1
    return items, i


def parse_pattern(text: str):
    items, _ = _parse(_tokens(text), 0, None)
    return items


def _expand(items, t0, dur, cycle, out):
    if not items:
        return
    step = dur / len(items)
    for j, it in enumerate(items):
        a = t0 + j * step
        if it[0] == "atom":
            if it[1] != "~":
                out.append((a, step, it[1]))
        elif it[0] == "seq":
            _expand(it[1], a, step, cycle, out)
        else:                                           # alternation: one item per cycle, in turn
            alt = it[1][cycle % len(it[1])]
            _expand([alt], a, step, cycle, out)


def pattern_events(text: str, cycles: int = 1, cycle_s: float = 2.0) -> list[tuple[float, float, str]]:
    """(start s, length s, symbol) for every sounding step over ``cycles`` cycles."""
    items = parse_pattern(text)
    out = []
    for c in range(cycles):
        _expand(items, c * cycle_s, cycle_s, c, out)
    return out


NOTE_RE = re.compile(r"([a-g])(#|b)?(-?\d)")


def note_number(sym: str) -> int:
    m = NOTE_RE.fullmatch(sym)
    if not m:
        raise ValueError(sym)
    base = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}[m.group(1)]
    acc = {"#": 1, "b": -1, None: 0}[m.group(2)]
    return 12 * (int(m.group(3)) + 1) + base + acc


# --------------------------------------------------------------------------------------------- trackers and canons


def tracker_events(rows, row_s: float, channels: int = 4):
    """Rows of a tracker pattern, each a list of ``channels`` cells (None, or (key, instrument)), one row every
    ``row_s`` seconds; a note sounds until the next note in its channel."""
    out = []
    for ch in range(channels):
        starts = [(r, cell) for r, row in enumerate(rows) if (cell := row[ch]) is not None]
        for j, (r, (key, ins)) in enumerate(starts):
            nxt = starts[j + 1][0] if j + 1 < len(starts) else len(rows)
            out.append((r * row_s, (nxt - r) * row_s, key, ins, ch))
    return sorted(out, key=lambda e: (e[0], e[4]))


def tempo_canon(notes, ratios, converge: int):
    """Nancarrow's tempo canon: voice v plays the same notes (key, onset, length in beats) at tempo ratio r_v (beats a
    second), started so that note ``converge`` sounds at the same moment in every voice.  Returns (voice, key,
    start s, length s) and the convergence time."""
    onset = notes[converge][1]
    t_conv = max(onset / r for r in ratios)
    out = []
    for v, r in enumerate(ratios):
        start = t_conv - onset / r
        for key, on, ln in notes:
            out.append((v, key, start + on / r, ln / r))
    return out, t_conv
