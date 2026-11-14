"""Pictures of keys (Part 15, *Key*): the circle of fifths, Krumhansl's torus laid flat, and a meter of keys.

    clock = fifths_clock()            # twelve major keys round a circle, a fifth apart; .cell[pc], .at(pc)
    tmap = torus_map(angles)          # the 24 keys by their two angles; .cell[(tonic, mode)]
    m = key_meter(names)              # rows of bars, one per key; m.set(values) redraws them
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, GREY, LEFT, RIGHT, UP, WHITE, Circle, Line, Rectangle, VGroup

from . import label
from .chordviz import tex
from .scaleviz import BLUE, GOLD

DIM = "#3A4250"
FLAT_NAMES = ("C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B")


def fifths_clock(radius: float = 1.9, font_size: int = 28, color=WHITE, signatures: bool = True, minors: bool = False) -> VGroup:
    """The twelve major keys round a circle, each a fifth above the one before it clockwise, C at the top.
    ``.cell[pc]`` is a key's name; ``.at(pc, r)`` its place; ``.sig[pc]`` its number of sharps or flats."""
    g = VGroup()
    ring = Circle(radius=radius, color=DIM, stroke_width=2)
    g.add(ring)
    g.cell, g.sig, g.minor = {}, {}, {}

    def at(pc, r: float = 1.0):
        k = (7 * pc) % 12                                   # steps round the circle
        a = np.pi / 2 - 2 * np.pi * k / 12.0
        return ring.get_center() + radius * r * np.array([np.cos(a), np.sin(a), 0.0])

    g.at = at
    for pc in range(12):
        k = (7 * pc) % 12
        t = label(tex(FLAT_NAMES[pc]), font_size=font_size, color=color).move_to(at(pc, 1.0))
        back = Circle(radius=0.3 * font_size / 28, stroke_width=0, fill_color="#0B0E14", fill_opacity=1).move_to(t)
        g.add(back, t)
        g.cell[pc] = t
        if signatures:
            n = k if k <= 6 else k - 12
            s = label("0" if n == 0 else (rf"{n}$\sharp$" if n > 0 else rf"{-n}$\flat$"), font_size=font_size - 10, color=GREY).move_to(at(pc, 1.32))
            g.add(s)
            g.sig[pc] = s
        if minors:
            mn = label(tex(FLAT_NAMES[(pc + 9) % 12]).lower() if len(FLAT_NAMES[(pc + 9) % 12]) == 1 else tex(FLAT_NAMES[(pc + 9) % 12][0].lower() + FLAT_NAMES[(pc + 9) % 12][1:]),
                       font_size=font_size - 8, color=BLUE).move_to(at(pc, 0.68))
            g.add(mn)
            g.minor[pc] = mn
    g.ring, g.radius = ring, radius
    return g


def torus_map(angles, width: float = 9.0, height: float = 4.6, font_size: int = 24, major=GOLD, minor=BLUE) -> VGroup:
    """Krumhansl and Kessler's torus cut open and laid flat: each key at (theta, phi), both running from 0 to 1;
    the left edge joins the right, and the top joins the bottom.  ``angles`` is a list of dicts with ``tonic``,
    ``mode``, ``short``, ``theta``, ``phi``."""
    frame = Rectangle(width=width, height=height, stroke_color=DIM, stroke_width=1.5)
    g = VGroup(frame)
    g.cell = {}
    for a in angles:
        x = frame.get_left()[0] + width * (0.04 + 0.92 * a["theta"])
        y = frame.get_bottom()[1] + height * (0.06 + 0.88 * a["phi"])
        t = label(tex(a["short"]), font_size=font_size, color=major if a["mode"] == "major" else minor).move_to([x, y, 0])
        g.add(t)
        g.cell[(a["tonic"], a["mode"])] = t
    g.frame = frame
    return g


def key_meter(names, width: float = 5.0, row: float = 0.55, color=GOLD, font_size: int = 26, values=None) -> VGroup:
    """Rows of bars, one for each key named.  ``.set(values)`` gives each bar its length (values from 0 to 1) and
    its number; the bars are family members, so the meter can be driven while a sound plays."""
    g = VGroup()
    g.rows = []
    for k, nm in enumerate(names):
        y = -k * row
        name = label(tex(nm), font_size=font_size, color=WHITE).move_to([-width / 2 - 0.2, y, 0], aligned_edge=RIGHT)
        track = Line([-width / 2, y, 0], [width / 2, y, 0], color=DIM, stroke_width=10)
        bar = Line([-width / 2, y, 0], [-width / 2 + 0.01, y, 0], color=color, stroke_width=10)
        g.add(name, track, bar)
        g.rows.append((name, track, bar))

    def set_(values):
        for (name, track, bar), v in zip(g.rows, values):
            a = track.get_start()
            b = a + (track.get_end() - a) * float(np.clip(v, 0.004, 1.0))
            bar.put_start_and_end_on(a, b)
        return g

    g.set = set_
    if values is not None:
        set_(values)
    return g
