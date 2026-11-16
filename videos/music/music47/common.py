"""Helpers shared by the scenes of Part 47 ("Origins and Universals")."""

from __future__ import annotations

import numpy as np

from explainer.music.chordviz import tex  # noqa: F401
from explainer.music.kit import *  # noqa: F403
from explainer.music.melodyviz import columns, roll  # noqa: F401
from explainer.music.rhythmviz import flash  # noqa: F401
from explainer.music.scaleviz import BLUE, GOLD, RED  # noqa: F401

from .compute import CACHE, CLIPS, load  # noqa: F401

PART = 47
clip = clip_loader(CACHE, CLIPS, item_aliases={"tune": "tune47"})
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


def necklace(pattern, radius=1.3, color=TUNE, dot=0.11):
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
    for d in g.dots:
        g.add(d)
    return g


def grid_row(pattern, cell=0.42, color=TUNE, label_text=None, size=18):
    """A row of boxes, filled where the pattern strikes."""
    g = VGroup()
    g.cells = []
    for c in pattern:
        on = c == "x" or c == 1
        box = Square(cell, stroke_color=GREY_B, stroke_width=1, fill_color=color if on else BLACK, fill_opacity=0.85 if on else 0)
        g.add(box)
        g.cells.append(box)
    g.arrange(RIGHT, buff=0.03)
    if label_text:
        return VGroup(label(label_text, font_size=size, color=color), g).arrange(RIGHT, buff=0.35)
    return g


def flash_cells(snd, cells, onsets_, start, pulse_s, cycles, n, hold=0.85, color=None, fill=None):
    """Light the cells of a pattern row in time: cell ``o`` at each onset, cycle after cycle (one glow per cell)."""
    end = start + cycles * n * pulse_s
    for o in sorted(set(onsets_)):
        glow = SurroundingRectangle(cells[o], color=color or EAR, buff=0.02, stroke_width=4, corner_radius=0.06)
        if fill:
            glow.set_fill(fill, opacity=0.0)
        snd.show(glow)

        def upd(m, t, o=o):
            on = False
            if start <= t < end:
                ph = ((t - start) / pulse_s - o) % n
                on = ph < hold
            m.set_stroke(opacity=1.0 if on else 0.0)
            if fill:
                m.set_fill(opacity=0.45 if on else 0.0)
        snd.drive(glow, upd)


def hand(snd, neck, start, cycle_s, color=WHITE, radius=None):
    """A clock hand sweeping a necklace once a cycle, starting at the top when the sound reaches ``start``."""
    r = radius or (neck[0].width / 2)
    c = neck[0].get_center()
    ln = Line(c, c + UP * r, color=color, stroke_width=3, stroke_opacity=0.8)

    def upd(m, t):
        ang = PI / 2 - TAU * max(t - start, 0.0) / cycle_s
        m.put_start_and_end_on(c, c + r * np.array([np.cos(ang), np.sin(ang), 0]))

    snd.show(ln)
    snd.drive(ln, upd)
    return ln


def pat_row(pattern, cell=0.42, color=TUNE, name=None, size=18, name_w=None):
    """A labelled row of cells: ``.cells`` for flashing."""
    g = grid_row(pattern, cell=cell, color=color)
    if name is None:
        g.cells = list(g)
        return g
    lab = label(name, font_size=size, color=color)
    out = VGroup(lab, g).arrange(RIGHT, buff=0.35)
    out.cells = list(g)
    return out


def sym(s: str) -> str:
    """A chord symbol as LaTeX text: Db7 -> D$\\flat$7, F#dim7 -> F$\\sharp$dim7."""
    if len(s) > 1 and s[1] == "b":
        s = s[0] + r"$\flat$" + s[2:]
    elif len(s) > 1 and s[1] == "#":
        s = s[0] + r"$\sharp$" + s[2:]
    return s.replace("dim7", r"$^{\circ}$7").replace("m7b5", r"m7$\flat$5")


def chart(changes, cell_w=2.6, cell_h=0.9, size=24, color=WHITE, per_row=4):
    """A lead-sheet chart: bars as boxes, four to a row, chord symbols inside; ``.bars`` for flashing."""
    g = VGroup()
    g.bars = []
    for i, bar in enumerate(changes):
        box = Rectangle(width=cell_w, height=cell_h, stroke_color=GREY_B, stroke_width=1.5)
        txt = VGroup(*[label(sym(s), font_size=size, color=color) for s in bar]).arrange(RIGHT, buff=0.35)
        txt.move_to(box)
        cell = VGroup(box, txt)
        g.add(cell)
        g.bars.append(cell)
    rows_ = [VGroup(*g.bars[i:i + per_row]).arrange(RIGHT, buff=0.0) for i in range(0, len(g.bars), per_row)]
    VGroup(*rows_).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    return g


def line_over(notes, changes, width=11.6, height=2.4, color=TUNE, lo=None, hi=None, size=17):
    """An eighth-note line [(key, eighth)] as a roll over bars of chords, with the chord symbols above it."""
    total = 8 * len(changes)
    ms = [m for m, _ in notes] or [60]
    lo = lo if lo is not None else min(ms) - 2
    hi = hi if hi is not None else max(ms) + 2
    roll = mroll([[m, e, 1.0] for m, e in notes], width=width, height=height, lo=lo, hi=hi, color=color, total=total, bar_h=0.11)
    fr = roll.frame
    labs = VGroup()
    lines_ = VGroup()
    for b, bar in enumerate(changes):
        x = fr.get_left()[0] + width * b * 8 / total
        lines_.add(Line([x, fr.get_bottom()[1], 0], [x, fr.get_top()[1], 0], color=GREY_D, stroke_width=1))
        for k, s in enumerate(bar):
            xx = x + width * 8 * k / len(bar) / total
            labs.add(label(sym(s), font_size=size, color=WHITE).move_to([xx + 0.32, fr.get_top()[1] + 0.25, 0]))
    g = VGroup(lines_, roll, labs)
    g.roll, g.labels, g.total = roll, labs, total
    return g


def scored(mel, chords=None, beats=4.0, width=11.0, height=2.2, lo=None, hi=None, color=TUNE, size=17, bars=None):
    """A melody [(key, onset, length)] as a roll with bar lines and, above each bar, its chord(s) in roman numerals."""
    ms = [m for m, _, _ in mel]
    lo = lo if lo is not None else min(ms) - 2
    hi = hi if hi is not None else max(ms) + 2
    nb = bars or int(round(max(a + d for _, a, d in mel) / beats))
    total = nb * beats
    roll = mroll([list(n) for n in mel], width=width, height=height, lo=lo, hi=hi, color=color, total=total, bar_h=0.12)
    fr = roll.frame
    lines_ = VGroup(*[Line([fr.get_left()[0] + width * b / nb, fr.get_bottom()[1] - 0.05, 0], [fr.get_left()[0] + width * b / nb, fr.get_top()[1] + 0.05, 0],
                           color=GREY_D, stroke_width=1) for b in range(nb + 1)])
    labs = VGroup()
    if chords:
        per = len(chords) // nb if len(chords) >= nb else 1
        for i, c_ in enumerate(chords):
            x = fr.get_left()[0] + width * (i / per) / nb
            labs.add(label(roman_tex(c_), font_size=size, color=GREY_A).move_to([x + 0.08, fr.get_top()[1] + 0.3, 0], aligned_edge=LEFT))
    g = VGroup(lines_, roll, labs)
    g.roll, g.labels, g.total, g.frame, g.nb = roll, labs, total, fr, nb
    return g


def roman_tex(s: str) -> str:
    return s.replace("viio", r"vii$^{\circ}$").replace("V7", r"V$^7$")


def bar_box(g, b, color=EAR):
    """A rectangle around bar b of a ``scored`` roll."""
    fr = g.frame
    w = fr.width / g.nb
    return Rectangle(width=w, height=fr.height + 0.2, stroke_color=color, stroke_width=3).move_to([fr.get_left()[0] + w * (b + 0.5), fr.get_center()[1], 0])


WHY = {"leaps": r"a forbidden leap", "range": r"a range wider than a tenth", "parallels": r"parallel fifths or octaves with the bass",
       "harmony": r"too few chord tones on the beats", "cadence": r"no cadence"}
WHY_SAID = {"leaps": "a forbidden leap: a tritone, a seventh, or more than an octave", "range": "a range wider than a tenth",
            "parallels": "parallel fifths or octaves with the bass", "harmony": "too few chord tones on the strong beats",
            "cadence": "a missing cadence"}


def perf_roll(perf, width=11.0, height=1.6, lo=None, hi=None, color=TUNE, total=None, vel=False):
    """A performance [{key, t, dur, vel}] as a roll in seconds; with ``vel``, each bar's opacity follows its velocity."""
    notes = [[p["key"], p["t"], p["dur"]] for p in perf]
    ks = [p["key"] for p in perf]
    lo = lo if lo is not None else min(ks) - 2
    hi = hi if hi is not None else max(ks) + 2
    g = mroll(notes, width=width, height=height, lo=lo, hi=hi, color=color, total=total or max(p["t"] + p["dur"] for p in perf), bar_h=0.13)
    if vel:
        for b, p in zip(g.notes, perf):
            b.set_fill(opacity=0.25 + 0.75 * min(max((p["vel"] - 0.2) / 0.6, 0), 1))
    return g


def value_bars(vals, width=11.0, height=1.4, base=1.0, scale=1.0, color=TUNE, neg=BLUE):
    """One bar per note: its value minus ``base``, up (color) or down (neg)."""
    n = len(vals)
    g = VGroup(Line([0, 0, 0], [width, 0, 0], color=GREY_D))
    for i, v in enumerate(vals):
        h = (v - base) * scale * height
        if abs(h) < 0.01:
            h = 0.01 if h >= 0 else -0.01
        g.add(Rectangle(width=width / n * 0.7, height=abs(h), stroke_width=0, fill_color=color if h >= 0 else neg, fill_opacity=0.85)
              .move_to([width * (i + 0.5) / n, h / 2, 0]))
    return g


# ------------------------------------------------------------------ the animated scene
HITS_ = (3.20, 7.95, 11.40)
GROUND_Y, LOW_Y, EDGE_X, DOOR_X = -0.4, -2.9, 3.0, -0.6


def _fig_pos(t):
    """The figure's centre and tilt at scene time t."""
    r = 0.28
    if t < HITS_[0]:
        x = -5.6 + (-1.05 + 5.6) * t / HITS_[0]
        return x, GROUND_Y + r + 0.06 * abs(np.sin(np.pi * t / 0.34)), 0.0
    if t < 3.7:
        return -1.05, GROUND_Y + r, 0.0
    if t < HITS_[1]:
        u = (t - 3.7) / (HITS_[1] - 3.7)
        x = -1.05 + (2.7 + 1.05) * u
        return x, GROUND_Y + r + 0.06 * abs(np.sin(np.pi * (t - 3.7) / 0.34)), 0.0
    if t < 8.95:
        return 2.7, GROUND_Y + r, 0.35 * np.sin(2 * np.pi * (t - HITS_[1]) * 2.0)
    if t < HITS_[2]:
        u = (t - 8.95) / (HITS_[2] - 8.95)
        return 2.7 + 1.0 * u, GROUND_Y + r + (LOW_Y - GROUND_Y) * u * u, 4.0 * u
    return 3.7, LOW_Y + r * (0.8 if t < HITS_[2] + 0.25 else 1.0), 0.0


def stage():
    """The scene: ground, a door, a cliff, lower ground, and a round figure with eyes."""
    g = VGroup()
    ground = Line([-6.4, GROUND_Y, 0], [EDGE_X, GROUND_Y, 0], color=GREY_B, stroke_width=3)
    cliff = Line([EDGE_X, GROUND_Y, 0], [EDGE_X, LOW_Y, 0], color=GREY_B, stroke_width=3)
    low = Line([EDGE_X, LOW_Y, 0], [6.4, LOW_Y, 0], color=GREY_B, stroke_width=3)
    frame_ = Rectangle(width=0.7, height=1.5, stroke_color=GREY_A, stroke_width=2).move_to([DOOR_X + 0.35, GROUND_Y + 0.75, 0])
    door = Rectangle(width=0.62, height=1.42, stroke_width=0, fill_color="#7C5A3A", fill_opacity=1.0).move_to([DOOR_X + 0.35, GROUND_Y + 0.75, 0])
    body = Circle(radius=0.28, stroke_color=WHITE, stroke_width=2, fill_color=TUNE, fill_opacity=1.0)
    eyes = VGroup(Dot([-0.08, 0.06, 0], radius=0.045, color=BLACK), Dot([0.1, 0.06, 0], radius=0.045, color=BLACK))
    fig = VGroup(body, eyes)
    g.add(ground, cliff, low, frame_, door, fig)
    g.door, g.fig, g.door_frame = door, fig, frame_
    return g


def set_stage(st, t):
    x, y, tilt = _fig_pos(t)
    st.fig.move_to([x, y, 0])
    st.fig.rotate(tilt - getattr(st.fig, "_tilt", 0.0), about_point=st.fig.get_center())
    st.fig._tilt = tilt
    o = 0.0 if t < HITS_[0] else min((t - HITS_[0]) / 0.3, 1.0)
    w = 0.62 * (1 - 0.88 * o)
    st.door.stretch_to_fit_width(max(w, 0.05))
    st.door.move_to([DOOR_X + 0.04 + w / 2, GROUND_Y + 0.75, 0])
    return st


def drive_stage(snd, st, t0):
    snd.drive(st.fig, lambda m, now: set_stage(st, now - t0))


def strip(length=13.5, width=12.0, hits=HITS_, labels=("door", "edge", "landing")):
    """A timeline under the scene: seconds and 24 fps frames, the hit points, and a playhead."""
    x0 = -width / 2
    y = -3.55
    base = Line([x0, y, 0], [x0 + width, y, 0], color=GREY_D, stroke_width=2)
    ticks = VGroup(*[Line([x0 + width * s / length, y - 0.07, 0], [x0 + width * s / length, y + 0.07, 0], color=GREY_D, stroke_width=1) for s in range(int(length) + 1)])
    marks = VGroup()
    for h, lb in zip(hits, labels):
        x = x0 + width * h / length
        marks.add(VGroup(Line([x, y - 0.15, 0], [x, y + 0.15, 0], color=EAR, stroke_width=3),
                         label(rf"{lb}: \ {h:.2f} s, \ frame {h * 24:.0f}", font_size=12, color=EAR).move_to([x, y + 0.32, 0])))
    head = Line([x0, y - 0.18, 0], [x0, y + 0.18, 0], color=WHITE, stroke_width=3)
    g = VGroup(base, ticks, marks, head)
    g.head, g.x0, g.width, g.length, g.y = head, x0, width, length, y
    return g


def drive_strip(snd, sp, t0):
    def upd(m, now):
        t = min(max(now - t0, 0), sp.length)
        m.move_to([sp.x0 + sp.width * t / sp.length, sp.y, 0])
    snd.drive(sp.head, upd)


def keyroll(keys, ioi=1.0, width=11.0, height=2.0, lo=None, hi=None, colors=None, bar_h=0.14):
    """A sequence of key numbers, one per slot, as a roll; ``colors`` per note (default gold)."""
    notes = [[k, i * ioi, ioi * 0.9] for i, k in enumerate(keys)]
    g = mroll(notes, width=width, height=height, lo=lo if lo is not None else min(keys) - 2, hi=hi if hi is not None else max(keys) + 2,
              color=TUNE, total=len(keys) * ioi, bar_h=bar_h)
    if colors:
        for b, c_ in zip(g.notes, colors):
            b.set_fill(c_, 1.0)
    return g


def bits_plot(values, width=11.0, height=1.6, top=8.0, color=EAR, x0=None, y0=0.0):
    """One bar per note: its surprise (or uncertainty) in bits, on a fixed scale up to ``top``."""
    n = len(values)
    x0 = -width / 2 if x0 is None else x0
    g = VGroup(Line([x0, y0, 0], [x0 + width, y0, 0], color=GREY_D))
    for i, v in enumerate(values):
        h = height * min(v, top) / top
        g.add(Rectangle(width=width / n * 0.7, height=max(h, 0.01), stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x0 + width * (i + 0.5) / n, y0 + h / 2, 0]))
    return g


# ------------------------------------------------------------------------------------------------ Part 47's drawings
def mel_notes(mel, base=60.0, centre=None):
    """A melody of [pitch, beats] as roll notes [key, onset, beats] (``centre``: put the median pitch there)."""
    off = 0.0 if centre is None else centre - float(np.median([x[0] for x in mel])) - base
    out, t = [], 0.0
    for p, b in mel:
        out.append([base + p + off, t, b])
        t += b
    return out


def simplex(side=4.4, color=GREY_B):
    """The triangle of three-interval rhythms: a rhythm (a, b, c), proportions of the cycle, sits at a*A + b*B + c*C,
    so each corner is the rhythm whose whole cycle is one interval."""
    h = side * np.sqrt(3) / 2
    tri = Polygon([-side / 2, -h / 3, 0], [side / 2, -h / 3, 0], [0, 2 * h / 3, 0], stroke_color=color, stroke_width=2)
    g = VGroup(tri)
    g.tri = tri

    def at(x):
        A, B, C = tri.get_vertices()
        x = np.asarray(x, float)
        if len(x) == 2:
            x = np.array([x[0], x[1], 1 - x[0] - x[1]])
        return x[0] * A + x[1] * B + x[2] * C

    g.at = at
    return g


def ratio_tex(pat) -> str:
    return r"\,:\,".join(str(int(v)) for v in pat)


def line_plot(series, width=5.2, height=2.6, ylo=0.0, yhi=1.0, xmax=None, colors=None, bands=None, xlabel="", ylabel="",
              yticks=(), xticks=(), size=16, stroke=3):
    """Lines ``series[k] = ys`` against 0, 1, 2, ...; ``bands[k] = (lo, hi)`` shaded behind.  ``.to(x, y)`` maps data
    to the screen; ``.lines`` are the curves."""
    colors = colors or [TUNE, BLUE, EAR, GOLD]
    xmax = xmax or max(len(s) for s in series) - 1
    fr = VGroup(Line([0, 0, 0], [width, 0, 0], color=GREY_B, stroke_width=1.5), Line([0, 0, 0], [0, height, 0], color=GREY_B, stroke_width=1.5))
    g = VGroup(fr)

    def to(x, y):
        return fr[0].get_start() + RIGHT * width * x / xmax + UP * height * (y - ylo) / (yhi - ylo)

    g.to = to
    if bands:
        for k, (lo, hi) in enumerate(bands):
            pts = [to(i, v) for i, v in enumerate(hi)] + [to(i, v) for i, v in reversed(list(enumerate(lo)))]
            g.add(Polygon(*pts, stroke_width=0, fill_color=colors[k % len(colors)], fill_opacity=0.18))
    g.lines = VGroup()
    for k, ys in enumerate(series):
        ln = VMobject(stroke_color=colors[k % len(colors)], stroke_width=stroke).set_points_as_corners([to(i, v) for i, v in enumerate(ys)])
        g.lines.add(ln)
    g.add(g.lines)
    for v in yticks:
        g.add(label(f"{v:g}", font_size=size - 2, color=GREY_A).next_to(to(0, v), LEFT, buff=0.12))
    for v in xticks:
        g.add(label(f"{v:g}", font_size=size - 2, color=GREY_A).next_to(to(v, ylo), DOWN, buff=0.12))
    if xlabel:
        g.add(label(xlabel, font_size=size, color=GREY_A).next_to(fr[0], DOWN, buff=0.45))
    if ylabel:
        g.add(label(ylabel, font_size=size, color=WHITE).next_to(fr[1], UP, buff=0.15).align_to(fr[1], LEFT))
    return g


def phase_circle(phases, R, mean, radius=1.25, color=TUNE, dot=0.07):
    """Angles round a circle, 0 at the top (on the beat), clockwise; the mean resultant as an arrow of length R."""
    c = Circle(radius=radius, stroke_color=GREY_B, stroke_width=2)
    top = Dot(c.get_top(), radius=0.05, color=WHITE)
    dots = VGroup(*[Dot([radius * np.sin(t), radius * np.cos(t), 0], radius=dot, color=color, fill_opacity=0.85) for t in phases])
    end = np.array([R * radius * np.sin(mean), R * radius * np.cos(mean), 0])
    arr_ = Arrow(ORIGIN, end if R > 0.05 else end + 0.001, buff=0, color=WHITE, stroke_width=5, max_tip_length_to_length_ratio=0.25) if R > 0.08 else Dot(ORIGIN, radius=0.06, color=WHITE)
    g = VGroup(c, top, dots, arr_)
    g.dots, g.arrow = dots, arr_
    return g


def tree_depth(t):
    return 0 if not isinstance(t, (list, tuple)) else 1 + max(tree_depth(t[0]), tree_depth(t[1]))


def tree_leaves(t):
    return [t] if not isinstance(t, (list, tuple)) else tree_leaves(t[0]) + tree_leaves(t[1])


def dendro(tree, width=8.0, height=3.0, color=GREY_A, size=18, labels=None, leaf_colors=None, stroke=3):
    """A cladogram of nested pairs: leaves along the bottom in the tree's order, each join drawn at the height of its
    deepest branch.  ``.clades[frozenset(leaves)]`` is the join's drawing; ``.tags[leaf]`` its label."""
    lv = tree_leaves(tree)
    D = max(tree_depth(tree), 1)
    xs = {n: -width / 2 + width * i / max(len(lv) - 1, 1) for i, n in enumerate(lv)}
    g = VGroup()
    g.clades, g.tags = {}, {}

    def draw(t):
        if not isinstance(t, (list, tuple)):
            return np.array([xs[t], -height / 2, 0])
        a, b = draw(t[0]), draw(t[1])
        y = -height / 2 + height * tree_depth(t) / D
        j = VGroup(Line(a, [a[0], y, 0], color=color, stroke_width=stroke), Line(b, [b[0], y, 0], color=color, stroke_width=stroke),
                   Line([a[0], y, 0], [b[0], y, 0], color=color, stroke_width=stroke))
        g.add(j)
        g.clades[frozenset(tree_leaves(t))] = j
        return np.array([(a[0] + b[0]) / 2, y, 0])

    draw(tree)
    for n in lv:
        t = label((labels or {}).get(n, n), font_size=size, color=(leaf_colors or {}).get(n, WHITE))
        t.next_to([xs[n], -height / 2, 0], DOWN, buff=0.15)
        g.tags[n] = t
        g.add(t)
    return g


def log_timeline(events, width=11.5, lo=1000, hi=100000, y=0.0, size=17):
    """Events (years ago, text, colour) above or below a logarithmic axis of years ago (older to the left)."""
    def x(v):
        return width / 2 - width * (np.log10(v) - np.log10(lo)) / (np.log10(hi) - np.log10(lo))

    ax = Line([-width / 2, y, 0], [width / 2, y, 0], color=GREY_B, stroke_width=2)
    g = VGroup(ax)
    g.x = x
    for v in (1000, 3000, 10000, 30000, 100000):
        if lo <= v <= hi:
            g.add(Line([x(v), y - 0.08, 0], [x(v), y + 0.08, 0], color=GREY_B, stroke_width=2),
                  label(f"{v:,}", font_size=size - 3, color=GREY_A).move_to([x(v), y - 0.32, 0]))
    g.add(label(r"years ago", font_size=size - 2, color=GREY_A).next_to(ax, RIGHT, buff=0.15))
    g.marks = VGroup()
    for k, ev in enumerate(events):
        v, text, col = ev[:3]
        lev = ev[3] if len(ev) > 3 else (1 if k % 2 == 0 else -1)          # +1, +2 above the axis; -1, -2 below
        up = lev > 0
        tip = Dot([x(v), y, 0], radius=0.07, color=col)
        stem = Line([x(v), y, 0], [x(v), y + 0.75 * lev, 0], color=col, stroke_width=1.5)
        tag = label(text, font_size=size, color=col).next_to(stem, UP if up else DOWN, buff=0.08)
        side = ev[4] if len(ev) > 4 else None                  # 'left': the label ends at the stem; 'right': starts there
        if side == "left":
            tag.shift(RIGHT * (x(v) + 0.15 - tag.get_right()[0]))
        elif side == "right":
            tag.shift(RIGHT * (x(v) - 0.15 - tag.get_left()[0]))
        g.marks.add(VGroup(tip, stem, tag))
    g.add(g.marks)
    return g


def note_of(f: float) -> str:
    """The nearest note to a frequency, and how far off it is in cents (for Tex): ``G5 $-$40``."""
    m = 69 + 12 * np.log2(f / 440.0)
    k = int(round(m))
    c = int(round(100 * (m - k)))
    name = LETTER[k % 12] + str(k // 12 - 1)
    return name + (r" \ $+$" + str(c) if c > 0 else r" \ $-$" + str(-c) if c < 0 else "")


def ghost(m, k=0.15):
    """A faint copy of ``m`` to hold the screen before it is drawn: every stroke and fill scaled by ``k`` (so that open
    curves, which have no fill, do not grow one, as ``set_opacity`` would give them)."""
    c = m.copy()
    for s in c.family_members_with_points():
        s.set_stroke(opacity=s.get_stroke_opacity() * k)
        s.set_fill(opacity=s.get_fill_opacity() * k)
    return c
