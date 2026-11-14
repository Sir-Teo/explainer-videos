"""Tablature: where the fingers go (Part 10).

A staff says which note; a tablature says which string and which fret.  Most notes can be played in several places
on a fretted instrument, so a tablature records a decision that a staff leaves to the player.
"""

from __future__ import annotations

import numpy as np

GUITAR = (40, 45, 50, 55, 59, 64)            # E2 A2 D3 G3 B3 E4, lowest string first
LUTE = (43, 48, 53, 57, 62, 67)              # a six-course Renaissance lute in G: G2 C3 F3 A3 D4 G4
FRENCH = "abcdefghiklmn"                      # French lute tablature's letters: a is the open string, and there is no j


def positions(midi: int, tuning=GUITAR, frets: int = 12) -> list[tuple[int, int]]:
    """Every (string, fret) that sounds a note; strings are numbered from the lowest, 0."""
    return [(s, midi - open_) for s, open_ in enumerate(tuning) if 0 <= midi - open_ <= frets]


def count_fingerings(midis, tuning=GUITAR, frets: int = 12) -> int:
    """The number of different tablatures for one melody."""
    n = 1
    for m in midis:
        n *= len(positions(m, tuning, frets))
    return n


def _cost(a, b) -> float:
    """What it costs a hand to go from one position to the next: moving along the neck is dear, crossing strings is
    cheap, and an open string leaves the hand where it was."""
    (s1, f1), (s2, f2) = a, b
    move = 0.0 if f1 == 0 or f2 == 0 else abs(f2 - f1)
    return 1.0 * move + 0.3 * abs(s2 - s1) + 0.15 * f2


def fingering(midis, tuning=GUITAR, frets: int = 12) -> dict:
    """The tablature with the least movement (dynamic programming over every choice for every note)."""
    options = [positions(m, tuning, frets) for m in midis]
    if any(not o for o in options):
        raise ValueError("a note is off the instrument")
    best = [np.array([0.15 * f for _, f in options[0]])]
    back = []
    for k in range(1, len(options)):
        c = np.array([[best[-1][i] + _cost(a, b) for i, a in enumerate(options[k - 1])] for b in options[k]])
        back.append(c.argmin(axis=1))
        best.append(c.min(axis=1))
    j = int(best[-1].argmin())
    path = [j]
    for b in reversed(back):
        j = int(b[j])
        path.append(j)
    path.reverse()
    return {"positions": [options[k][j] for k, j in enumerate(path)], "cost": float(best[-1].min()), "choices": [len(o) for o in options]}


def sounded(positions_, tuning=GUITAR) -> list[int]:
    """What a tablature sounds like: back to keys of the piano."""
    return [tuning[s] + f for s, f in positions_]
