"""Other ways to write music down, drawn in manim (Part 10 and after): every one returns a group whose ``.notes``
are the marks for the notes, in order, so that a scene can light them as they sound.

    neumes(heights)                signs over the words: higher, lower, the same (after St Gall, simplified)
    square_staff(positions)        Guido's lines with a letter for a clef, and square notes
    mensural(symbols, positions)   longs, breves, semibreves and minims on a staff, with the sign of the time
    tablature(positions)           strings and frets
    jianpu(degrees, beats)         numbered notation
    gongche(chars)                 the characters of gongche, in a column
    qin_character()                one character of guqin tablature, assembled from its parts
    piano_roll(notes)              holes in paper: time against pitch
    byte_row(data, groups)         a file, byte by byte
    code_block(text)               a file, as text
    light(snd, marks, times)       lights each mark while its note sounds

Staff notation itself is ``explainer/music/staff.py``.
"""

from __future__ import annotations

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, WHITE, Arc, Circle, Dot, Line, Polygon, Rectangle, RoundedRectangle, Square, Text, VGroup,
                   interpolate_color)
from manim.utils.color import ManimColor

from explainer.music.staff import music_font

MONO = "DejaVu Sans Mono"
CJK = "AR PL UMing CN"
RED_LINE = "#D9534F"
PARCHMENT = "#E9D8B4"


def _lines(n: int, width: float, space: float, color, stroke_width: float = 1.6) -> VGroup:
    """``n`` staff lines, the bottom one at y = 0."""
    return VGroup(*[Line([-width / 2, k * space, 0], [width / 2, k * space, 0], color=color, stroke_width=stroke_width) for k in range(n)])


def _spread(count: int, width: float, pad: float = 0.5) -> np.ndarray:
    return np.linspace(-width / 2 + pad, width / 2 - pad, count) if count > 1 else np.array([0.0])


# ---------------------------------------------------------------------------
# Neumes
# ---------------------------------------------------------------------------
def neume_sign(kind: int, size: float = 0.34, color=PARCHMENT) -> VGroup:
    """One sign: a rising stroke for a higher note (virga), a dash for the same note, a dot for a lower one."""
    if kind > 0:
        return VGroup(Line([-0.12 * size, -0.5 * size, 0], [0.12 * size, 0.5 * size, 0], color=color, stroke_width=5))
    if kind == 0:
        return VGroup(Line([-0.3 * size, 0, 0], [0.3 * size, 0, 0], color=color, stroke_width=5))
    return VGroup(Dot(radius=0.14 * size, color=color))


def neumes(heights, words=None, width: float = 6.0, heighted: float = 0.0, size: float = 0.34, color=PARCHMENT, word_color=WHITE, word_size: int = 26,
           line: int | None = None, line_color=RED_LINE) -> VGroup:
    """Neumes for a melody (``heights`` in scale steps).  With ``heighted`` = 0 every sign sits at the same level
    over its syllable and only its kind says where the melody goes; with ``heighted`` > 0 each is also raised by
    that much for every step (diastematic neumes).  ``line`` draws one ruled line at that step, as scribes began to
    do around the year 1000."""
    h = list(heights)
    con = [0] + [(b > a) - (b < a) for a, b in zip(h, h[1:])]
    xs = _spread(len(h), width)
    g = VGroup()
    g.notes = []
    base = min(h)
    for k, (x, c) in enumerate(zip(xs, con)):
        s = neume_sign(1 if k == 0 else c, size, color)
        s.move_to([x, 0.75 + heighted * (h[k] - base), 0])
        g.add(s)
        g.notes.append(s)
    if line is not None:
        y = 0.75 + heighted * (line - base)
        g.line = Line([xs[0] - 0.45, y, 0], [xs[-1] + 0.45, y, 0], color=line_color, stroke_width=2)
        g.add(g.line)
    if words:
        g.words = VGroup(*[Text(w, font_size=word_size, color=word_color, slant="ITALIC").move_to([x, 0, 0]) for x, w in zip(xs, words)])
        g.add(g.words)
    return g


# ---------------------------------------------------------------------------
# Guido's staff and square notes
# ---------------------------------------------------------------------------
def square_staff(positions, width: float = 6.0, space: float = 0.3, clef: str = "C", clef_line: int = 0, color=WHITE, line_color=RED_LINE, words=None,
                 word_size: int = 24, lines: int = 4, pad: float = 1.0) -> VGroup:
    """Square notes on ``lines`` lines.  ``positions`` are half-spaces above the bottom line; the clef is a letter
    written on line ``clef_line`` (0 is the bottom), which says that line is C (or F)."""
    g = VGroup()
    g.lines = _lines(lines, width, space, line_color)
    g.add(g.lines)
    g.clef = Text(clef, font_size=30, color=color, weight="BOLD").scale(space / 0.3).move_to([-width / 2 + 0.3, clef_line * space, 0])
    g.add(g.clef)
    xs = _spread(len(positions), width - pad, 0.3) + pad / 2
    g.notes = []
    for x, p in zip(xs, positions):
        n = Square(side_length=0.62 * space, color=color, fill_color=color, fill_opacity=1.0, stroke_width=0).move_to([x, p * space / 2, 0])
        g.add(n)
        g.notes.append(n)
    if words:
        g.words = VGroup(*[Text(w, font_size=word_size, color=color, slant="ITALIC").move_to([x, -1.6 * space - 0.15, 0]) for x, w in zip(xs, words)])
        g.add(g.words)
    return g


# ---------------------------------------------------------------------------
# Mensural notation
# ---------------------------------------------------------------------------
def mensural_shape(symbol: str, space: float = 0.3, color=WHITE, void: bool = False) -> VGroup:
    """L a long (a square with a tail), B a breve (a square), S a semibreve (a lozenge), M a minim (a lozenge with a
    stem).  ``void`` leaves the shapes hollow, as scribes did once paper replaced parchment."""
    fill = 0.0 if void else 1.0
    w = 0.7 * space
    kw = dict(color=color, fill_color=color, fill_opacity=fill, stroke_width=2.5 if void else 0)
    if symbol in "LB":
        body = Rectangle(width=w, height=0.62 * space, **kw)
        g = VGroup(body)
        if symbol == "L":
            g.add(Line(body.get_corner(DOWN + RIGHT), body.get_corner(DOWN + RIGHT) + DOWN * 1.3 * space, color=color, stroke_width=2.5))
    else:
        r = 0.42 * space
        body = Polygon([0, r, 0], [0.8 * r, 0, 0], [0, -r, 0], [-0.8 * r, 0, 0], **kw)
        g = VGroup(body)
        if symbol == "M":
            g.add(Line([0, r, 0], [0, r + 1.5 * space, 0], color=color, stroke_width=2.5))
    g.body = body
    return g


def time_sign(perfect: bool, space: float = 0.3, color=WHITE) -> VGroup:
    """A whole circle for perfect time (threes), a broken one for imperfect time (twos): the C of common time."""
    r = 0.75 * space
    return VGroup(Circle(radius=r, color=color, stroke_width=3)) if perfect else VGroup(Arc(radius=r, start_angle=np.pi / 4, angle=1.5 * np.pi, color=color, stroke_width=3))


def mensural(symbols: str, positions, width: float = 6.0, space: float = 0.3, perfect: bool | None = None, color=WHITE, line_color=None, void: bool = False,
             lines: int = 5, pad: float = 1.4) -> VGroup:
    g = VGroup()
    g.lines = _lines(lines, width, space, line_color or color, 1.4)
    g.add(g.lines)
    if perfect is not None:
        g.sign = time_sign(perfect, space, color).move_to([-width / 2 + 0.5, (lines - 1) * space / 2, 0])
        g.add(g.sign)
    xs = _spread(len(symbols), width - pad, 0.3) + pad / 2
    g.notes = []
    for x, sym, p in zip(xs, symbols, positions):
        n = mensural_shape(sym, space, color, void)
        n.shift(np.array([x, p * space / 2, 0]) - n.body.get_center())
        g.add(n)
        g.notes.append(n)
    return g


# ---------------------------------------------------------------------------
# Tablature
# ---------------------------------------------------------------------------
def tablature(positions, strings: int = 6, width: float = 6.0, space: float = 0.26, color=WHITE, line_color=None, letters: str | None = None,
              names=None, font_size: int = 22, pad: float = 1.0) -> VGroup:
    """Lines for strings (the lowest at the bottom), a number on a line for a fret.  ``letters`` (for instance
    French lute tablature's ``"abcdefghik"``) writes letters instead.  ``names`` labels the strings at the left."""
    g = VGroup()
    g.lines = _lines(strings, width, space, line_color or "#8A93A0", 1.4)
    g.add(g.lines)
    if names:
        g.names = VGroup(*[Text(nm, font=MONO, font_size=font_size - 6, color="#8A93A0").move_to([-width / 2 - 0.22, k * space, 0]) for k, nm in enumerate(names)])
        g.add(g.names)
    xs = _spread(len(positions), width - pad, 0.3) + (pad / 2 if not names else 0.0)
    g.notes = []
    for x, (s, f) in zip(xs, positions):
        t = Text(letters[f] if letters else str(f), font=MONO, font_size=font_size, color=color, weight="BOLD")
        t.move_to([x, s * space, 0])
        back = Rectangle(width=t.width + 0.08, height=t.height + 0.06, stroke_width=0, fill_color="#0E1117", fill_opacity=1.0).move_to(t)
        n = VGroup(back, t)
        n.mark = t
        g.add(n)
        g.notes.append(n)
    return g


# ---------------------------------------------------------------------------
# Jianpu and gongche
# ---------------------------------------------------------------------------
def jianpu(degrees, beats, width: float = 6.0, color=WHITE, font_size: int = 34, per_bar: int = 4, key: str | None = "1 = C", octaves=None) -> VGroup:
    """Numbered notation: a digit for a degree of the scale, a dash for each further beat a note lasts, a line under
    a digit that lasts half a beat, a dot above or below for the octave, and barlines."""
    cells = []                                            # (text, note index or None, underline, octave)
    for k, (d, b) in enumerate(zip(degrees, beats)):
        o = 0 if octaves is None else octaves[k]
        if b >= 1:
            cells.append((str(d), k, False, o))
            cells.extend([("–", None, False, 0)] * (int(b) - 1))
        else:
            cells.append((str(d), k, True, o))
    g = VGroup()
    g.notes = [None] * len(degrees)
    n_bars = int(np.ceil(sum(max(b, 0.5) if b < 1 else b for b in beats) / per_bar))
    step = width / (len(cells) + n_bars * 0.6)
    x, beat = -width / 2 + step / 2, 0.0
    for text, idx, under, octave in cells:
        t = Text(text, font=MONO, font_size=font_size, color=color, weight="BOLD")
        t.move_to([x, 0, 0])
        cell = VGroup(t)
        if under:
            cell.add(Line([x - 0.14, -0.3, 0], [x + 0.14, -0.3, 0], color=color, stroke_width=2.5))
        if octave:
            cell.add(Dot([x, 0.34 * np.sign(octave) - (0.08 if octave < 0 else 0.0), 0], radius=0.045, color=color))
        g.add(cell)
        if idx is not None:
            g.notes[idx] = cell
        beat += 0.5 if under else 1.0
        x += step * (0.6 if under else 1.0)
        if abs(beat % per_bar) < 1e-9:
            g.add(Line([x - step * 0.2, -0.3, 0], [x - step * 0.2, 0.3, 0], color="#8A93A0", stroke_width=2))
            x += step * 0.6
    if key:
        g.key = Text(key, font=MONO, font_size=font_size - 12, color="#8A93A0").next_to(g, UP, buff=0.2).align_to(g, LEFT)
        g.add(g.key)
    return g


def gongche(chars, beats=None, height: float = 3.2, color=WHITE, font_size: int = 30, columns: int = 1) -> VGroup:
    """Gongche characters, read from the top down and from the right-hand column to the left; a small mark beside a
    character shows a beat that is held (``beats`` > 1)."""
    g = VGroup()
    g.notes = []
    per = int(np.ceil(len(chars) / columns))
    step = height / max(per - 1, 1)
    for k, ch in enumerate(chars):
        col, row = divmod(k, per)
        t = Text(ch, font=CJK, font_size=font_size, color=color)
        t.move_to([-(col) * 0.75, height / 2 - row * step, 0])
        cell = VGroup(t)
        if beats is not None and beats[k] > 1:
            cell.add(Text("、", font=CJK, font_size=font_size - 8, color="#8A93A0").move_to(t.get_center() + RIGHT * 0.36 + DOWN * 0.1))
        g.add(cell)
        g.notes.append(cell)
    return g


def qin_character(size: float = 1.6, color=WHITE) -> VGroup:
    """One character of guqin tablature, built from abbreviations: 艹 (from 散, an open string) over 勹 (from 勾, the
    middle finger pulling inward) around 三 (the third string).  It says what the hands do, and nothing about how
    long."""
    top = Text("艹", font=CJK, font_size=60, color=color)
    hook = Text("勹", font=CJK, font_size=96, color=color)
    num = Text("三", font=CJK, font_size=40, color=color)
    hook.next_to(top, DOWN, buff=-0.1)
    num.move_to(hook.get_center() + DOWN * 0.12 + LEFT * 0.08)
    g = VGroup(top, hook, num)
    g.scale(size / g.height)
    g.parts = (top, hook, num)
    return g


# ---------------------------------------------------------------------------
# Rolls and bytes
# ---------------------------------------------------------------------------
def piano_roll(notes, width: float = 6.0, height: float = 2.2, lo: int | None = None, hi: int | None = None, color="#F5C542", grid="#2A313C", total: float | None = None,
               gap: float = 0.04) -> VGroup:
    """Holes in a roll: ``notes`` are (start, length, key) with times in any unit; time runs to the right, keys up."""
    notes = list(notes)
    lo = min(k for _, _, k in notes) - 1 if lo is None else lo
    hi = max(k for _, _, k in notes) + 1 if hi is None else hi
    total = max(t + d for t, d, _ in notes) if total is None else total
    row = height / (hi - lo + 1)
    g = VGroup()
    g.frame = Rectangle(width=width, height=height, stroke_color="#8A93A0", stroke_width=1.5)
    g.grid = VGroup(*[Line([-width / 2, -height / 2 + k * row, 0], [width / 2, -height / 2 + k * row, 0], color=grid, stroke_width=1) for k in range(1, hi - lo + 1)])
    g.add(g.grid, g.frame)
    g.notes = []
    for t, d, key in notes:
        w = max(width * d / total - gap, 0.03)
        r = RoundedRectangle(width=w, height=row * 0.78, corner_radius=min(0.04, w / 3), stroke_width=0, fill_color=color, fill_opacity=1.0)
        r.move_to([-width / 2 + width * t / total + w / 2 + gap / 2, -height / 2 + (key - lo + 0.5) * row, 0])
        g.add(r)
        g.notes.append(r)
    g.x_of = lambda t: g.frame.get_left()[0] + g.frame.width * t / total          # noqa: E731
    g.y_of = lambda key: g.frame.get_bottom()[1] + (key - lo + 0.5) * row         # noqa: E731
    g.total = total
    return g


def byte_row(data: bytes, groups=None, per_row: int = 16, font_size: int = 22, color="#8A93A0", step: float = 0.46, row_step: float = 0.42) -> VGroup:
    """A file as hexadecimal bytes.  ``groups`` is a list of (first, last + 1) ranges; ``.groups[k]`` is then the
    bytes of the k-th range, to be lit together, and ``.bytes`` every byte."""
    g = VGroup()
    g.bytes = []
    ranges = list(groups or [])
    g.groups = [VGroup() for _ in ranges]              # each group is part of the row's family, so a scene can animate it in place
    for k, b in enumerate(data):
        r, c = divmod(k, per_row)
        t = Text(f"{b:02X}", font=MONO, font_size=font_size, color=color).move_to([c * step, -r * row_step, 0])
        g.bytes.append(t)
        owner = next((j for j, (a, z) in enumerate(ranges) if a <= k < z), None)
        if owner is None:
            g.add(t)
        else:
            g.groups[owner].add(t)
    g.add(*g.groups)
    g.notes = g.groups
    return g


def code_block(text: str, font_size: int = 18, color=WHITE, line_step: float = 0.3) -> VGroup:
    """Lines of a text file, left-aligned, in a fixed-width face; ``.rows`` are the lines."""
    g = VGroup()
    g.rows = []
    for k, line in enumerate(text.splitlines()):
        if not line.strip():
            g.rows.append(VGroup())
            continue
        indent = len(line) - len(line.lstrip(" "))
        t = Text(line.strip(), font=MONO, font_size=font_size, color=color)
        t.move_to([0, -k * line_step, 0], aligned_edge=LEFT)
        t.shift(RIGHT * indent * 0.105 * font_size / 18)
        g.add(t)
        g.rows.append(t)
    return g


# ---------------------------------------------------------------------------
# Lighting marks while their notes sound
# ---------------------------------------------------------------------------
def light(snd, marks, times, hot="#F5C542", base=WHITE, fade: float = 0.35, end: float | None = None, part=lambda m: m):
    """Light each of ``marks`` from its time in the clip (``times``, seconds) until the next: bright at its start,
    fading towards its ordinary colour, so that the picture is never still while the sound runs."""
    parts, times = [part(m) for m in marks], [float(t) for t in times]
    stops = times[1:] + [end if end is not None else times[-1] + 1.0]
    hot_c, base_c = ManimColor(hot), ManimColor(base)

    def fn(_, t):
        for m, t0, t1 in zip(parts, times, stops):
            if t0 <= t < t1:
                w = 0.35 + 0.65 * float(np.exp(-(t - t0) / fade))
                m.set_color(interpolate_color(base_c, hot_c, w))
            else:
                m.set_color(base_c)

    snd.drive(parts[0], fn)                       # the first mark carries the updater for them all
    return parts
