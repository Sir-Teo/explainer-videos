"""Monochord's music for picture and play (Part 44 of *Music, Built*): hitting a cut on the beat, a score that
rearranges itself for a game, and a sound chip.

    FPS, frames(s), click(bpm)         film time: 24 frames a second; a click track's frames per beat, written as
                                       whole frames and eighths ("12-0" is 12 frames a beat, 120 beats a minute)
    find_tempo(hits, ...)              every tempo (and its click) that puts each hit point within a tolerance of a beat
                                       counted from the cue's start; the error curve over all tempos
    variable_click(hits, beats)        the tempos that land each hit exactly, one tempo per segment
    pulse_harmonics(duty, n)           a pulse wave's harmonic amplitudes: |sin(pi k d)| / k, every 1/d-th harmonic gone
    Chip                               a sound chip of ours: two pulse channels with duty cycles, a 4-bit triangle, an
                                       LFSR noise channel, volumes in 16 steps, updated 60 times a second
    arpeggio(chord, ...)               a chord as one channel cycling its notes every frame (the chiptune chord)
    Game, simulate(seed)               a game's state over time (explore, danger, combat, victory)
    Score, adapt(game, ...)            an adaptive score: two-bar segments per state, layers by intensity, transitions
                                       quantised to the next beat, bar or phrase, stingers; the delay of every transition
    duck(music, dialogue, depth)       music lowered under dialogue, and the dialogue-to-music ratio in the speech band

No manim here.  Checked in ``tests/music/test_screen.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .audio import SR

FPS = 24.0


# --------------------------------------------------------------------------------------------- film time
def frames(seconds: float, fps: float = FPS) -> float:
    return seconds * fps


def click(bpm: float, fps: float = FPS) -> tuple[int, int, float]:
    """Frames per beat as (whole frames, eighths, exact): the way click tracks are written ('12-3' is 12 3/8)."""
    f = fps * 60.0 / bpm
    whole = int(f)
    eighths = int(round((f - whole) * 8))
    if eighths == 8:
        whole, eighths = whole + 1, 0
    return whole, eighths, f


def click_bpm(whole: int, eighths: int = 0, fps: float = FPS) -> float:
    return fps * 60.0 / (whole + eighths / 8.0)


def find_tempo(hits, start: float = 0.0, lo: float = 60.0, hi: float = 180.0, step: float = 0.01, tol_frames: float = 1.0,
               subdivision: int = 1, fps: float = FPS) -> dict:
    """For every tempo from ``lo`` to ``hi``: the worst distance, in frames, from a hit point to the nearest beat (or
    ``subdivision`` of a beat) counted from the cue's start.  Solutions are tempos whose worst error is within
    ``tol_frames``; for each run of solutions the best tempo is kept, with its click and the beat each hit falls on."""
    hits = np.asarray(hits, float) - start
    bpms = np.arange(lo, hi + step / 2, step)
    worst = np.empty(len(bpms))
    for i, b in enumerate(bpms):
        per = 60.0 / b / subdivision
        n = hits / per
        worst[i] = np.max(np.abs(n - np.round(n)) * per * fps)
    ok = worst <= tol_frames
    sols = []
    i = 0
    while i < len(bpms):
        if ok[i]:
            j = i
            while j + 1 < len(bpms) and ok[j + 1]:
                j += 1
            k = i + int(np.argmin(worst[i:j + 1]))
            b = float(bpms[k])
            per = 60.0 / b / subdivision
            sols.append({"bpm": b, "worst_frames": float(worst[k]), "click": click(b, fps)[:2],
                         "beats": [float(np.round(h / per) / subdivision) for h in hits]})
            i = j + 1
        else:
            i += 1
    return {"bpm": bpms.tolist(), "worst": worst.tolist(), "solutions": sols}


def variable_click(hits, beats, start: float = 0.0) -> list[float]:
    """Tempos (bpm), one per segment between hits, that put hit i exactly on beat ``beats[i]``."""
    t = np.concatenate([[start], np.asarray(hits, float)])
    b = np.concatenate([[0.0], np.asarray(beats, float)])
    return [float(60.0 * (b[i + 1] - b[i]) / (t[i + 1] - t[i])) for i in range(len(hits))]


# --------------------------------------------------------------------------------------------- the chip
def pulse_harmonics(duty: float, n: int = 16) -> np.ndarray:
    """Amplitudes of harmonics 1..n of a pulse wave with the given duty cycle, relative to the strongest."""
    k = np.arange(1, n + 1)
    a = np.abs(np.sin(np.pi * k * duty)) / k
    return a / a.max()


class Chip:
    """Two pulse channels (duty 12.5, 25, 50 or 75 per cent), a triangle channel with 32 steps of 4 bits, and a noise
    channel driven by a 15-bit linear-feedback shift register; every channel's volume in 16 steps; registers updated
    60 times a second, as many 1980s sound chips were.  Original design, in their manner."""

    FRAME = 1.0 / 60.0

    def __init__(self, sr: int = SR):
        self.sr = sr

    def pulse(self, f, seconds, duty=0.5, vol=12, env=None):
        n = int(seconds * self.sr)
        t = np.arange(n) / self.sr
        ph = (np.cumsum(np.full(n, f) if np.isscalar(f) else f) / self.sr) % 1.0
        y = np.where(ph < duty, 1.0, -1.0)
        v = np.full(n, vol / 15.0) if env is None else np.repeat(np.asarray(env, float) / 15.0, int(np.ceil(n / len(env))))[:n]
        return y * v * 0.5 + 0 * t

    def triangle(self, f, seconds, vol=15):
        n = int(seconds * self.sr)
        ph = (np.cumsum(np.full(n, f)) / self.sr) % 1.0
        step = np.floor(ph * 32).astype(int)
        tri = np.where(step < 16, 15 - step, step - 16)          # 15 .. 0 .. 15 in 32 steps: 4 bits
        return (tri / 7.5 - 1.0) * 0.5 * vol / 15.0

    def noise(self, seconds, period=8, vol=10, short=False, decay=None):
        n = int(seconds * self.sr)
        reg = 1
        out = np.empty(n)
        bit = 1.0
        hold = max(1, int(self.sr / (1789773 / 16 / period))) if period else 1
        for i in range(n):
            if i % hold == 0:
                tap = 6 if short else 1
                fb = (reg ^ (reg >> tap)) & 1
                reg = (reg >> 1) | (fb << 14)
                bit = 1.0 if reg & 1 else -1.0
            out[i] = bit
        v = vol / 15.0
        if decay:
            v = v * np.exp(-np.arange(n) / self.sr / decay)
        return out * v * 0.4

    def arpeggio(self, freqs, seconds, duty=0.25, vol=10, rate: float = 60.0):
        """One pulse channel cycling through the chord's notes ``rate`` times a second: heard as a buzzing chord."""
        n = int(seconds * self.sr)
        idx = (np.arange(n) / self.sr * rate).astype(int) % len(freqs)
        f = np.asarray(freqs, float)[idx]
        return self.pulse(f, seconds, duty, vol)


# --------------------------------------------------------------------------------------------- the game
STATES = ("explore", "danger", "combat", "victory")


@dataclass
class Game:
    times: list = field(default_factory=list)          # seconds at which the state changes
    states: list = field(default_factory=list)         # the state from each time on
    intensity: np.ndarray = None                       # 0..1, sampled every 0.1 s
    length: float = 0.0


def simulate(seed: int = 3, length: float = 48.0) -> Game:
    """A small game: the player explores, an enemy is sometimes seen (danger), sometimes a fight starts (combat), and a
    fight ends in victory, then exploring again.  State changes happen at random moments, as a player's do."""
    rng = np.random.default_rng(seed)
    t, s = 0.0, "explore"
    times, states = [0.0], ["explore"]
    while t < length:
        stay = {"explore": rng.uniform(5, 11), "danger": rng.uniform(3, 6), "combat": rng.uniform(6, 12), "victory": 3.0}[s]
        t += stay
        if t >= length:
            break
        nxt = {"explore": "danger", "danger": "combat" if rng.random() < 0.7 else "explore", "combat": "victory",
               "victory": "explore"}[s]
        times.append(round(float(t), 2))
        states.append(nxt)
        s = nxt
    grid = np.arange(0, length, 0.1)
    level = {"explore": 0.2, "danger": 0.55, "combat": 1.0, "victory": 0.4}
    target = np.array([level[states[np.searchsorted(times, x, side="right") - 1]] for x in grid])
    inten = np.zeros_like(target)
    for i in range(1, len(grid)):
        inten[i] = inten[i - 1] + (target[i] - inten[i - 1]) * 0.15
    return Game(times, states, inten, length)


@dataclass
class Score:
    bpm: float = 120.0
    beats_per_bar: int = 4
    segment_bars: int = 2

    @property
    def beat(self) -> float:
        return 60.0 / self.bpm

    @property
    def bar(self) -> float:
        return self.beat * self.beats_per_bar


def next_boundary(t: float, unit: float) -> float:
    return float(np.ceil(t / unit - 1e-9) * unit)


def adapt(game: Game, score: Score = Score(), quantise: str = "bar", stingers: bool = True) -> dict:
    """The music's plan for a game: for each state change, when the music switches (the next beat, bar or phrase
    boundary, or at once), with a stinger at the moment of the change if asked; and how many layers sound at each
    moment (1 to 4, by intensity).  Returns the switches, their delays and the layer counts."""
    unit = {"now": 0.0, "beat": score.beat, "bar": score.bar, "phrase": score.bar * score.segment_bars}[quantise]
    switches = []
    for t, s in zip(game.times, game.states):
        at = t if unit == 0 else next_boundary(t, unit)
        switches.append({"event": float(t), "state": s, "switch": float(at), "delay": float(at - t), "stinger": bool(stingers and t > 0)})
    grid = np.arange(0, game.length, 0.1)
    layers = np.clip(1 + np.floor(game.intensity * 3.999), 1, 4).astype(int)
    # layers too change only on beat boundaries
    beat_idx = (grid / score.beat).astype(int)
    held = layers.copy()
    for i in range(1, len(grid)):
        held[i] = layers[i] if beat_idx[i] != beat_idx[i - 1] else held[i - 1]
    delays = [sw["delay"] for sw in switches[1:]]
    return {"switches": switches, "layers": held.tolist(), "grid_step": 0.1, "mean_delay": float(np.mean(delays)) if delays else 0.0,
            "max_delay": float(np.max(delays)) if delays else 0.0, "unit": unit, "quantise": quantise}


def expected_delay(unit: float) -> float:
    """If events arrive at uniformly random moments, waiting for the next boundary of length ``unit`` takes unit / 2
    on average."""
    return unit / 2.0


# --------------------------------------------------------------------------------------------- mixing
def band_energy(y, lo=1000.0, hi=4000.0, sr: int = SR) -> float:
    S = np.abs(np.fft.rfft(y)) ** 2
    f = np.fft.rfftfreq(len(y), 1 / sr)
    return float(S[(f >= lo) & (f < hi)].sum())


def envelope(y, sr: int = SR, attack: float = 0.01, release: float = 0.25) -> np.ndarray:
    a, r = np.exp(-1 / (attack * sr)), np.exp(-1 / (release * sr))
    env = np.zeros(len(y))
    e = 0.0
    for i, x in enumerate(np.abs(y)):
        c = a if x > e else r
        e = c * e + (1 - c) * x
        env[i] = e
    return env


def duck(music, dialogue, depth_db: float = 10.0, threshold: float = 0.05, sr: int = SR) -> dict:
    """Lower the music by up to ``depth_db`` while the dialogue's envelope is above ``threshold`` of its peak (a
    sidechain, as in Part 40), and report the dialogue-to-music energy ratio in the speech band (1 to 4 kHz) before
    and after."""
    n = min(len(music), len(dialogue))
    m, d = np.asarray(music[:n], float), np.asarray(dialogue[:n], float)
    env = envelope(d, sr)
    on = np.clip(env / (threshold * env.max() + 1e-12) - 1.0, 0, 1)
    g = 10 ** (-depth_db * on / 20)
    out = m * g
    before = 10 * np.log10(band_energy(d, sr=sr) / band_energy(m, sr=sr))
    after = 10 * np.log10(band_energy(d, sr=sr) / band_energy(out, sr=sr))
    return {"music": out, "gain": g, "ratio_before_db": float(before), "ratio_after_db": float(after)}
