"""Helpers shared by the scenes of Part 35 ("Maqam")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 35
clip = clip_loader(CACHE, CLIPS)
WEAK = "#8A93A0"
DIM = "#3A4250"
VOICE_C = [TUNE, BLUE, EAR, "#A3E635", GREY_B]
NAMES = {0: "C", 1: "C♯", 2: "D", 3: "E♭", 4: "E", 5: "F", 6: "F♯", 7: "G", 8: "G♯", 9: "A", 10: "B♭", 11: "B"}
LETTER = {0: "C", 1: r"C$\sharp$", 2: "D", 3: r"E$\flat$", 4: "E", 5: "F", 6: r"F$\sharp$", 7: "G", 8: r"G$\sharp$", 9: "A", 10: r"B$\flat$", 11: "B"}


def chapter(scene, number, title, question, lit=(), extra=(), spoken=None):
    open_chapter(scene, number, title, question, lit=lit, part=PART, extra=extra, spoken=spoken)


def mroll(notes, width=10.0, height=1.8, lo=60, hi=86, color=TUNE, total=None, bar_h=0.13):
    """Notes [midi, onset, duration] as a roll on a time axis of ``total`` units (gaps kept)."""
    total = total or max(n[1] + n[2] for n in notes)
    frame = Rectangle(width=width, height=height, stroke_width=0, fill_opacity=0)
    g = VGroup(frame)
    g.frame, g.total, g.lo, g.hi = frame, total, lo, hi
    g.notes = []
    for p, a, d in notes:
        w = max(width * d / total - 0.04, 0.03)
        b = RoundedRectangle(width=w, height=bar_h, corner_radius=min(0.05, bar_h / 2.5), stroke_width=0, fill_color=color, fill_opacity=1.0)
        b.move_to([frame.get_left()[0] + width * a / total + w / 2 + 0.02, frame.get_bottom()[1] + height * (p - lo) / max(hi - lo, 1), 0])
        g.add(b)
        g.notes.append(b)
    return g


def voices_roll(voices, width=11.0, height=3.0, colors=None, total=None, lo=None, hi=None, bar_h=0.11):
    """Several voices in one frame, each its own colour; ``.parts[j].notes`` for flashing."""
    allp = [n[0] for v in voices for n in v]
    lo = lo if lo is not None else min(allp) - 1
    hi = hi if hi is not None else max(allp) + 1
    total = total or max(n[1] + n[2] for v in voices for n in v)
    colors = colors or VOICE_C
    g = VGroup()
    g.parts = []
    for j, v in enumerate(voices):
        r = mroll(v, width=width, height=height, lo=lo, hi=hi, color=colors[j % len(colors)], total=total, bar_h=bar_h)
        g.add(r)
        g.parts.append(r)
    g.frame = g.parts[0].frame
    g.total = total
    return g


def flash_voices(snd, g, voices, start, unit, hot=WHITE, colors=None):
    colors = colors or VOICE_C
    for j, v in enumerate(voices):
        if v and g.parts[j].notes:
            flash(snd, g.parts[j].notes, [start + n[1] * unit for n in v], hot=hot, base=colors[j % len(colors)])


def cursor(snd, g, start, unit, color=WHITE):
    """A vertical line sweeping the roll in time with the sound."""
    fr = g.frame
    ln = Line(fr.get_corner(DL) + DOWN * 0.1, fr.get_corner(UL) + UP * 0.1, color=color, stroke_width=2, stroke_opacity=0.7)

    def upd(m, t):
        x = (t - start) / unit / g.total
        x = min(max(x, 0.0), 1.0)
        m.move_to([fr.get_left()[0] + fr.width * x, fr.get_center()[1], 0])

    snd.show(ln)
    snd.drive(ln, upd)
    return ln


def text_rows(items, font_size=25, buff=0.38, width=12.6):
    rows_ = VGroup(*[label(t, font_size=font_size, color=c_) for t, c_ in items]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    rows_.scale_to_fit_width(min(rows_.width, width))
    return rows_.move_to(DOWN * 0.1)


def rows_scene(scene, head_text, items, script, font_size=25, buff=0.38, marks="bcdefg"):
    """A heading and rows revealed at bookmarks a, b, c ... (the first row with the heading)."""
    rows_ = text_rows(items, font_size=font_size, buff=buff)
    head = label(head_text, font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
    with scene.voiceover(script) as vo:
        scene.play(FadeIn(head), FadeIn(rows_[0]))
        for mark, r in zip(marks, rows_[1:]):
            vo.wait_until(mark)
            scene.play(FadeIn(r))
    scene.wait(0.4)
    scene.clear_scene()


TN = {"C": "C", "C#": r"C$\sharp$", "D": "D", "Eb": r"E$\flat$", "E": "E", "F": "F", "F#": r"F$\sharp$", "G": "G", "Ab": r"A$\flat$",
      "A": "A", "Bb": r"B$\flat$", "B": "B"}


def tex_triad(n: str) -> str:
    """A triad name like 'Abm' as LaTeX: A-flat minor written as a$\\flat$ (lower case for minor)."""
    minor = n.endswith("m")
    root = n[:-1] if minor else n
    t = TN[root]
    return t[0].lower() + t[1:] if minor else t


def tonnetz(radius=0.42, cols=9, rows_=5, origin=(-4.4, -1.6)):
    """A patch of the Tonnetz: pitch classes on a triangular lattice (fifths to the right, major thirds up-right),
    with ``.pos[(i, j)]`` and ``.pc[(i, j)]``."""
    g = VGroup()
    g.pos, g.pc = {}, {}
    dx = 2 * radius * 1.6
    for j in range(rows_):
        for i in range(cols):
            x = origin[0] + i * dx + j * dx / 2
            y = origin[1] + j * dx * 0.866
            pc = (7 * i + 4 * j) % 12
            g.pos[(i, j)] = np.array([x, y, 0])
            g.pc[(i, j)] = pc
    for (i, j), p in g.pos.items():
        for di, dj in ((1, 0), (0, 1), (-1, 1)):
            q = g.pos.get((i + di, j + dj))
            if q is not None:
                g.add(Line(p, q, color=GREY_B, stroke_width=1, stroke_opacity=0.5))
    for (i, j), p in g.pos.items():
        g.add(VGroup(Circle(radius=radius * 0.62, color=GREY_B, stroke_width=1.5, fill_color=BLACK, fill_opacity=1).move_to(p),
                     label(PCN[g.pc[(i, j)]], font_size=16, color=GREY_A).move_to(p)))
    return g


PCN = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


def triangle(g, cells, color=TUNE, opacity=0.35):
    return Polygon(*[g.pos[c] for c in cells], color=color, stroke_width=2, fill_color=color, fill_opacity=opacity)


def spoken(n: str) -> str:
    """'Bbm' -> 'B flat minor', 'F#' -> 'F sharp major'."""
    minor = n.endswith("m")
    root = n[:-1] if minor else n
    return root[0] + (" flat" if root.endswith("b") else " sharp" if root.endswith("#") else "") + (" minor" if minor else " major")


def necklace(pattern, radius=1.3, color=TUNE, label_steps=False, dot=0.11):
    """A rhythm (string of x and . or a list of 0/1) round a circle, onset 0 at the top, clockwise; ``.dots`` are the
    onsets in order, ``.ticks`` every pulse."""
    p = [1 if (c == "x" or c == 1) else 0 for c in pattern]
    n = len(p)
    g = VGroup(Circle(radius=radius, color=DIM, stroke_width=1.5))
    g.ticks, g.dots = [], []
    pts = []
    for i in range(n):
        ang = PI / 2 - i * TAU / n
        pos = radius * np.array([np.cos(ang), np.sin(ang), 0])
        t = Dot(pos, radius=0.035, color=GREY_B)
        g.add(t)
        g.ticks.append(t)
        if p[i]:
            d = Dot(pos, radius=dot, color=color)
            g.dots.append(d)
            pts.append(pos)
    if len(pts) >= 3:
        g.add(Polygon(*pts, color=color, stroke_width=2, fill_opacity=0.12, fill_color=color))
    elif len(pts) == 2:
        g.add(Line(pts[0], pts[1], color=color, stroke_width=2))
    for d in g.dots:
        g.add(d)
    return g


def pattern_text(pattern, size=24, color=WHITE):
    s = "".join("x" if (c == "x" or c == 1) else "." for c in pattern)
    return label(r"\texttt{" + s + "}", font_size=size, color=color)


SARG = {-1: r"\b{N}", -3: r"\b{D}", -5: r"\b{P}", 0: "S", 1: "r", 2: "R", 3: "g", 4: "G", 5: "m", 6: "M", 7: "P", 8: "d", 9: "D", 10: "n", 11: "N", 12: "S'"}
SARG_PLAIN = {-1: "N.", -3: "D.", -5: "P.", 0: "S", 1: "r", 2: "R", 3: "g", 4: "G", 5: "m", 6: "M'", 7: "P", 8: "d", 9: "D", 10: "n", 11: "N", 12: "S'"}


def sargam(sts, size=24, color=WHITE, buff=0.3):
    """Notes in sargam (S R G m P D N; komal lower case, tivra Ma as M'; a dot after a note for the lower octave)."""
    return VGroup(*[label(SARG_PLAIN.get(s, str(s)), font_size=size, color=color) for s in sts]).arrange(RIGHT, buff=buff)


def tala_grid(theka, vibhags, marks, cell=0.62, size=17):
    """A tala cycle as boxes grouped in vibhags, each with its bol, and the clap/wave mark over each vibhag's first beat."""
    g = VGroup()
    g.cells = []
    x = 0.0
    i = 0
    for vi, (n, mk) in enumerate(zip(vibhags, marks)):
        for k in range(n):
            box = Rectangle(width=cell, height=cell * 0.75, stroke_color=GREY_B, stroke_width=1.5).move_to([x + cell / 2, 0, 0])
            b = theka[i] if i < len(theka) else ""
            txt = label(b, font_size=size, color=WHITE).move_to(box)
            num = label(str(i + 1), font_size=12, color=GREY_A).next_to(box, DOWN, buff=0.08)
            cellg = VGroup(box, txt, num)
            if k == 0:
                cellg.add(label(mk, font_size=18, color=TUNE if mk in ("X", "laghu") else (BLUE if mk == "0" else EAR)).next_to(box, UP, buff=0.1))
            g.add(cellg)
            g.cells.append(cellg)
            x += cell
            i += 1
        x += cell * 0.3
    return g.move_to(ORIGIN)


def contour_plot(contour, rate, width=10.0, height=2.4, lo=-2, hi=11, color=TUNE):
    ax = Axes(x_range=[0, len(contour) / rate, 1], y_range=[lo, hi, 1], x_length=width, y_length=height, tips=False,
              axis_config={"color": GREY_B, "include_numbers": False, "stroke_width": 1})
    pts = [ax.c2p(i / rate, v) for i, v in enumerate(contour)]
    line = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
    ticks = VGroup(*[label(SARG_PLAIN[s], font_size=14, color=GREY_A).next_to(ax.c2p(0, s), LEFT, buff=0.15) for s in (0, 2, 4, 5, 7, 9) if lo <= s <= hi])
    lines = VGroup(*[DashedLine(ax.c2p(0, s), ax.c2p(len(contour) / rate, s), color=DIM, stroke_width=1) for s in (0, 2, 4, 5, 7, 9) if lo <= s <= hi])
    g = VGroup(lines, ax, line, ticks)
    g.ax, g.line = ax, line
    return g


def cents_ruler(scales, width=11.0, top=1200.0, labels=None, colors=None, row_gap=0.9, tick_h=0.36, show_et=True):
    """Scales (lists of cents) as rows of ticks on a common ruler, with the twelve piano keys faint underneath."""
    colors = colors or [TUNE, BLUE, EAR, "#A3E635", "#F59E0B", "#22D3EE", GREY_A, WHITE]
    g = VGroup()
    g.rows = []
    for i, sc in enumerate(scales):
        y = -i * row_gap
        base = Line([-width / 2, y, 0], [width / 2, y, 0], color=DIM, stroke_width=1)
        ticks = VGroup(*[Line([-width / 2 + width * c / top, y - tick_h / 2, 0], [-width / 2 + width * c / top, y + tick_h / 2, 0], color=colors[i % len(colors)], stroke_width=4) for c in sc if c <= top])
        row = VGroup(base, ticks)
        if show_et:
            row.add(VGroup(*[Line([-width / 2 + width * k * 100 / top, y - tick_h * 0.3, 0], [-width / 2 + width * k * 100 / top, y + tick_h * 0.3, 0], color=GREY_B, stroke_width=1, stroke_opacity=0.5) for k in range(int(top / 100) + 1)]))
        if labels:
            row.add(label(labels[i], font_size=18, color=colors[i % len(colors)]).next_to(base, LEFT, buff=0.25))
        g.add(row)
        g.rows.append(row)
    return g
