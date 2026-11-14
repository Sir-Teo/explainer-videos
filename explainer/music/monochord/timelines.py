"""Monochord's timelines (Part 37 of *Music, Built*).

    TIMELINES                  a table of well-known timelines as strings of x and . (as commonly transcribed)
    metrics(pattern)           evenness (Part 33), oddity, off-beatness, and how many onsets fall on a 4-beat and a
                               3-beat grid
    offbeat_positions(n)       the pulses that lie on no regular polygon inscribed in the cycle: gcd(k, n) = 1
    hocket(melody, voices)     split a melody so that each voice plays only its own pitches
    mbira(f)                   a plucked tine: a clamped-free bar's partials (1 : 6.27 : 17.55), modal synthesis
    streams(notes, split)      the simplest streaming model: a fast sequence heard as separate high and low streams
    inherent(parts, split)     the high stream of several interlocking parts combined: an 'inherent pattern'
    design_inherent(target)    two interlocking parts whose combined high stream is a target melody, though neither
                               part plays it
    interlock_melody(events)   the same for a melody with its own rhythm (high notes at given pulses)
    swap_distance, centrality  Toussaint's swap distance between rhythms with equal onsets, and each one's total
                               distance to the others (son clave is the most central of six claves)
    interval_content(p)        how often each distance between onsets occurs (the standard pattern's are all different)
    rotations(p)               the timeline started on each of its strokes: the seven diatonic modes, for the standard
                               pattern
"""

from __future__ import annotations

from itertools import combinations
from math import gcd

import numpy as np

from .audio import SR
from .instruments import percussion as PC
from . import mathmusic as MM

TIMELINES = {
    "standard pattern (12)": "x.x.xx.x.x.x",
    "son clave (16)": "x..x..x...x.x...",
    "rumba clave (16)": "x..x...x..x.x...",
    "bossa nova (16)": "x..x..x...x..x..",
    "gahu (16)": "x..x..x...x...x.",
    "soli (12)": "x.x.x..x.x..",
    "tresillo (8)": "x..x..x.",
    "cinquillo (8)": "x.xx.xx.",
    "soukous (16)": "x..x..x...xx....",
    "shiko (16)": "x...x.x...x.x...",
}
CLAVES = ["son clave (16)", "rumba clave (16)", "bossa nova (16)", "gahu (16)", "soukous (16)", "shiko (16)"]
MODES = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]


def onsets(p) -> list[int]:
    return [i for i, c in enumerate(p) if c == "x"]


def offbeat_positions(n: int) -> list[int]:
    """Toussaint's off-beat positions: the pulses that lie on no regular polygon through pulse 0 (gcd(k, n) = 1)."""
    return [k for k in range(n) if gcd(k, n) == 1]


def metrics(p: str) -> dict:
    n = len(p)
    on = onsets(p)
    pat = [1 if c == "x" else 0 for c in p]
    e = MM.euclid(len(on), n)
    from .geometry import evenness
    even = evenness([12.0 * o / n for o in on]) * n / 12.0
    four = [k for k in range(n) if (k * 4) % n == 0]
    three = [k for k in range(n) if (k * 3) % n == 0]
    return {"n": n, "k": len(on), "onsets": on, "evenness": even, "euclidean": MM.is_rotation(pat, e),
            "oddity": MM.oddity(on, n) if n % 2 == 0 else None, "offbeat": sum(1 for o in on if o in offbeat_positions(n)),
            "on4": sum(1 for o in on if o in four), "on3": sum(1 for o in on if o in three)}


def swap_distance(a: str, b: str) -> int:
    """Toussaint's swap distance: the fewest swaps of adjacent pulses that turn one rhythm into the other (same
    number of onsets): the sum of the distances between corresponding onsets."""
    A, B = onsets(a), onsets(b)
    if len(A) != len(B):
        raise ValueError("swap distance needs equal numbers of onsets")
    return sum(abs(x - y) for x, y in zip(A, B))


def centrality(names: list[str] | None = None) -> dict:
    """Each rhythm's total swap distance to the others in the set."""
    names = names or CLAVES
    return {k: sum(swap_distance(TIMELINES[k], TIMELINES[j]) for j in names) for k in names}


def interval_content(p: str) -> dict:
    """For each distance d from 1 to n/2, how many pairs of onsets lie d pulses apart (around the cycle)."""
    n = len(p)
    on = onsets(p)
    out = {d: 0 for d in range(1, n // 2 + 1)}
    for a, b in combinations(on, 2):
        out[min((b - a) % n, (a - b) % n)] += 1
    return out


def steps(p: str) -> list[int]:
    on = onsets(p)
    n = len(p)
    return [(on[(i + 1) % len(on)] - on[i]) % n for i in range(len(on))]


def rotations(p: str) -> list[dict]:
    """The timeline started on each of its strokes, as a pattern and as steps."""
    on = onsets(p)
    n = len(p)
    out = []
    for k, o in enumerate(on):
        q = "".join(p[(o + i) % n] for i in range(n))
        out.append({"k": k, "pattern": q, "steps": steps(q)})
    return out


# ------------------------------------------------------------------------------------------------- hocket
def hocket(melody: list, voices: list[set]) -> list[list]:
    """Each voice plays the melody's notes that belong to its own set of pitches, and rests otherwise."""
    return [[m if m in v else None for m in melody] for v in voices]


# ------------------------------------------------------------------------------------------------- the mbira
TINE = [1.0, 6.267, 17.55]                                         # clamped-free bar: (4.694/1.875)^2, (7.855/1.875)^2


def mbira(f: float, seconds: float = 1.6, buzz: float = 0.15, sr: int = SR) -> np.ndarray:
    """A plucked metal tine (a clamped-free bar, Part 9's beam with one end held), with a little bottle-cap buzz:
    short noise bursts that follow the tine's own decay."""
    y = PC.modal([f * r for r in TINE], [1.0, 0.25, 0.08], [2.0, 9.0, 20.0], seconds, sr)
    if buzz:
        rng = np.random.default_rng(int(f))
        t = np.arange(len(y)) / sr
        y = y + buzz * rng.standard_normal(len(y)) * np.abs(y) * np.exp(-3 * t)
    return y / np.abs(y).max()


# ------------------------------------------------------------------------------------------------- streaming
def streams(notes: list, split: float) -> tuple[list, list]:
    """notes: [(time, pitch), ...].  The simplest streaming model (van Noorden's 'fission' at fast tempi and wide
    pitch separation): notes above ``split`` form one stream, the rest another."""
    hi = [(t, p) for t, p in notes if p >= split]
    lo = [(t, p) for t, p in notes if p < split]
    return hi, lo


def inherent(parts: list[list], split: float) -> list:
    """Combine parts (each a list of (time, pitch)) and return the high stream: the pattern a listener hears."""
    allnotes = sorted(n for part in parts for n in part)
    return streams(allnotes, split)[0]


def interlock_melody(events: list, n: int, low: list[int]) -> tuple[list, list]:
    """events: [(pulse, pitch), ...], the melody's high notes.  Part A plays the even pulses and part B the odd ones;
    a pulse with no melody note is filled from the repeating low figure.  Returns (A, B) as lists of (pulse, pitch)."""
    at = dict(events)
    a, b = [], []
    for i in range(n):
        pitch = at.get(i, low[i % len(low)])
        (a if i % 2 == 0 else b).append((i, pitch))
    return a, b


def design_inherent(target: list[int], low: list[int], pulse_per_note: int = 3) -> tuple[list, list, list]:
    """Two interlocking parts, A on even pulses and B on odd pulses, whose high notes, taken together, spell
    ``target`` (one high note every ``pulse_per_note`` pulses), alternating between the two parts; the remaining
    pulses are filled from ``low`` (a repeating low figure).  Neither part alone contains the target melody."""
    n = len(target) * pulse_per_note
    a, b = [], []
    for i in range(n):
        if i % pulse_per_note == 0:
            k = i // pulse_per_note
            pitch = target[k]
        else:
            pitch = low[i % len(low)]
        (a if i % 2 == 0 else b).append((i, pitch))
    return a, b, [(i, target[i // pulse_per_note]) for i in range(0, n, pulse_per_note)]
