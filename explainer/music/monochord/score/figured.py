"""Figured bass: a bass line and a few numbers, to be filled in by the player (Part 10).

A figure names intervals above the bass, counted in steps of the key.  No figure means a third and a fifth; ``6``
means a third and a sixth.  Which octave each note goes in, and which is doubled, is left to the player.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np

from . import SEMITONES, STEPS, Pitch

FIGURES = {"": (3, 5), "5": (3, 5), "5/3": (3, 5), "6": (3, 6), "6/3": (3, 6), "6/4": (4, 6), "7": (3, 5, 7), "6/5": (3, 5, 6),
           "4/3": (3, 4, 6), "4/2": (2, 4, 6), "2": (2, 4, 6)}
_SHARPS, _FLATS = "FCGDAEB", "BEADGCF"


def in_key(step: str, key: int) -> int:
    """The alteration a letter has under a key signature."""
    if key > 0 and step in _SHARPS[:key]:
        return 1
    if key < 0 and step in _FLATS[:-key]:
        return -1
    return 0


def above(bass: Pitch, interval: int, key: int = 0) -> Pitch:
    """The note of the key a second, third, ... above a bass note."""
    d = bass.diatonic + interval - 1
    octave, idx = divmod(d, 7)
    return Pitch(STEPS[idx], in_key(STEPS[idx], key), octave)


def chord(bass: Pitch, figure: str = "", key: int = 0) -> list[Pitch]:
    """The notes a figure asks for, in the octave above the bass."""
    return [above(bass, i, key) for i in FIGURES[figure]]


def realizations(bass: Pitch, figure: str = "", key: int = 0, voices: int = 3, low: int = 55, high: int = 81, span: int = 12) -> list[tuple[int, ...]]:
    """Every way to set ``voices`` notes above the bass: all between the keys ``low`` and ``high``, above the bass,
    no two the same, the upper voices within ``span`` semitones of each other, and every note the figure asks for
    present at least once (the bass counts as itself)."""
    need = {(SEMITONES[p.step] + p.alter) % 12 for p in chord(bass, figure, key)}
    allowed = need | {bass.midi % 12}
    keys = [m for m in range(max(low, bass.midi + 1), high + 1) if m % 12 in allowed]
    out = []
    for combo in combinations(keys, voices):
        if combo[-1] - combo[0] <= span and need <= {m % 12 for m in combo}:
            out.append(combo)
    return out


def _motion(a, b, bass_a: int, bass_b: int) -> float:
    """The cost of going from one chord to the next: the upper voices should move little, and no two voices may
    move in parallel fifths or octaves."""
    cost = float(sum(abs(y - x) for x, y in zip(a, b)))
    va, vb = (bass_a, *a), (bass_b, *b)
    for i in range(len(va)):
        for j in range(i + 1, len(va)):
            ia, ib = (va[j] - va[i]) % 12, (vb[j] - vb[i]) % 12
            if ia == ib and ia in (0, 7) and va[i] != vb[i]:
                cost += 50.0
    return cost


def realize(basses, figures, key: int = 0, top: int | None = None, **kw) -> dict:
    """A whole bass line realized with the smoothest voice leading; ``top`` asks for a first chord whose highest
    note is as near that key as possible, which gives a different, equally correct, answer."""
    options = [realizations(b, f, key, **kw) for b, f in zip(basses, figures)]
    start = np.array([0.0 if top is None else 4.0 * abs(o[-1] - top) for o in options[0]])
    best, back = [start], []
    for k in range(1, len(options)):
        c = np.array([[best[-1][i] + _motion(a, b, basses[k - 1].midi, basses[k].midi) for i, a in enumerate(options[k - 1])] for b in options[k]])
        back.append(c.argmin(axis=1))
        best.append(c.min(axis=1))
    j = int(best[-1].argmin())
    path = [j]
    for b in reversed(back):
        j = int(b[j])
        path.append(j)
    path.reverse()
    chords = [options[k][j] for k, j in enumerate(path)]
    parallels = sum(_motion(a, b, basses[k].midi, basses[k + 1].midi) >= 50.0 for k, (a, b) in enumerate(zip(chords, chords[1:])))
    count = 1
    for o in options:
        count *= len(o)
    return {"chords": chords, "cost": float(best[-1].min()), "choices": [len(o) for o in options], "count": count, "parallels": int(parallels)}
