"""The colours of *Music, Built*: one meaning per colour across all sixty-eight parts.

Plain hex strings and no manim, so the labs and the course site's interactives use the same table.
"""

from __future__ import annotations

import colorsys
from types import SimpleNamespace

MC = SimpleNamespace(
    TUNE="#F7D154",      # the Tune, wherever it appears: gold
    STRING="#E2C08D",    # the vibrating thing itself: a string, a membrane, a column of air
    RATIO="#FFB86B",     # ratios and lengths: the monochord's numbers
    FREQ="#58A6FF",      # frequency: hertz, partial numbers, the frequency axis
    TIME="#2EC4B6",      # time: the time axis, periods, the playhead
    LEVEL="#FF6B8B",     # amplitude, level, loudness, energy
    FORCE="#FF7EB6",     # forces: tension, the pull of a neighbour
    MASS="#94A3B8",      # mass, density, inertia
    RIGHT="#5BD17A",     # the wave travelling right
    LEFT="#D4A5FF",      # the wave travelling left
    NODE="#FF5C5C",      # nodes: points that do not move
    SMOOTH="#5BD17A",    # partials that coincide, consonance, "in tune"
    ROUGH="#FF5C5C",     # partials that clash, beats, "out of tune"
    EAR="#F472B6",       # the listener: what is heard, perception
    HUMAN="#FFB070",     # people and dates
    CODE="#9DD6F0",      # code from the repository
    LIMIT="#F472B6",     # the frontier: what the model leaves out, what is open
    PLAY="#FFFFFF",      # the playhead
)


def pc_color(pc: int, lightness: float = 0.66, saturation: float = 0.62) -> str:
    """The colour of a pitch class (0 = C, 1 = C sharp, ... 11 = B).  Hues run round the circle of fifths
    (C red, G orange, D yellow, A, E green, B, F sharp cyan, ... F rose), so that keys a fifth apart look alike and
    the two notes of a tritone are opposites."""
    k = (int(pc) * 7) % 12  # position on the circle of fifths
    r, g, b = colorsys.hls_to_rgb(k / 12.0, lightness, saturation)
    return "#{:02X}{:02X}{:02X}".format(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


# The pitch class nearest each harmonic of a fundamental (in semitones above it): 1 2 3 4 5 6 7 8 ...
_HARMONIC_PC = {n: int(round(12 * __import__("math").log2(n))) % 12 for n in range(1, 65)}


def harmonic_color(n: int, root_pc: int = 0) -> str:
    """The colour of the n-th harmonic of a note of pitch class ``root_pc``: the colour of the note it is nearest
    to.  Harmonics 1, 2, 4, 8 share the root's colour; 3, 6, 12 the fifth's; 5, 10 the third's."""
    return pc_color((root_pc + _HARMONIC_PC[min(int(n), 64)]) % 12)
