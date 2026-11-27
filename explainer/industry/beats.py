"""Beats and charts for *Industry, Built* scenes (manim).

A film is a run of beats: one narrated paragraph with bookmarks, a base picture put up as the paragraph starts, and one
step revealed at each bookmark.  :func:`beat` plays one, putting dim copies of every step on screen from the first
word so that no part of the narration runs over an empty frame (the series' dead-air rule).  The chart builders return
plain ``VGroup``s with their parts named, so a scene can pass them to :func:`beat` as steps or animate them itself.

    from explainer.industry.beats import beat, line_chart, hbars

    ch = line_chart({"China": (series, RED)}, x=(2015, 2025), y=(0, 120), yfmt=lambda v: f"${v:.0f}bn")
    beat(self, "Say this. <bookmark mark='a'/> Then this.", base=[ch.frame], steps=[ch.lines["China"]])
"""

from __future__ import annotations

import numpy as np
from manim import (DL, DOWN, LEFT, RIGHT, UP, UR, Animation, AnimationGroup, Create, DashedLine, Dot, FadeIn,
                   GrowFromCenter, GrowFromEdge, Line, Rectangle, RoundedRectangle, VGroup, VMobject, WHITE)

from explainer.industry import viz
from explainer.industry.draw import tx

GREY_A, GREY_B = "#C9D3E0", "#9AA3B2"
GOOD, BAD = "#7BD88F", "#E8554E"


# ------------------------------------------------------------------------------------------------------------ beats
def ghost(*mobs, opacity=0.3) -> VGroup:
    """Dim copies of what a beat will show, put up while its first sentence is spoken (fills stay unfilled for lines)."""
    g = VGroup(*[m.copy() for m in mobs])
    for sm in g.get_family():
        if isinstance(sm, VMobject):
            filled = sm.get_fill_opacity() > 0
            stroked = sm.get_stroke_width() > 0 and sm.get_stroke_opacity() > 0
            sm.set_fill(opacity=opacity if filled else 0)
            sm.set_stroke(opacity=opacity if stroked else 0)
        elif hasattr(sm, "set_opacity"):
            sm.set_opacity(opacity)
    return g


def _reveal(step) -> list:
    """Animations that reveal a step: mobjects fade in (lines are drawn, bars grow), animations play as given."""
    items = step if isinstance(step, (list, tuple)) else [step]
    out = []
    for it in items:
        if isinstance(it, Animation):
            out.append(it)
        elif getattr(it, "grow", None) is not None:
            out.append(GrowFromEdge(it, it.grow))
        elif isinstance(it, VMobject) and getattr(it, "is_line", False):
            out.append(Create(it))
        else:
            out.append(FadeIn(it))
    return out


def _mobs(step) -> list:
    items = step if isinstance(step, (list, tuple)) else [step]
    return [it for it in items if not isinstance(it, Animation)]


def beat(scene, say: str, base=(), steps=(), ghost_opacity: float = 0.3, run_time: float = 1.2, clear: bool = True,
         after=None):
    """Play one narrated beat: ``base`` appears at once, with dim copies of every step; step k is revealed at bookmark
    k ('a', 'b', ...) of ``say``.  ``after(vo)`` may play more inside the voiceover.  The screen is cleared at the end
    unless ``clear`` is False.  The dim copies are kept as ``scene.beat_ghost``, so an ``after`` that moves the steps
    can fade them out."""
    marks = "abcdefghijklmnop"
    base = [b for b in (base if isinstance(base, (list, tuple)) else [base]) if b is not None]
    pending = [m for s in steps for m in _mobs(s)]
    with scene.voiceover(say) as vo:
        first = [FadeIn(b) for b in base]
        scene.beat_ghost = None
        if pending:
            scene.beat_ghost = ghost(*pending, opacity=ghost_opacity)
            first.append(FadeIn(scene.beat_ghost))
        if first:
            scene.play(*first, run_time=1.0)
        for mk, step in zip(marks, steps):
            if f"mark='{mk}'" in say:
                vo.wait_until(mk)
            anims = _reveal(step)
            if anims:
                scene.play(*anims, run_time=run_time)
        if after is not None:
            after(vo)
    if clear:
        scene.clear_scene()


# ----------------------------------------------------------------------------------------------------------- charts
def poly(ax, pts, color, width: float = 3.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, y) for x, y in pts])
    m.is_line = True
    return m


def line_chart(series: dict, x, y, xticks=None, yticks=None, xfmt=None, yfmt=None, ylabel: str = "", xlabel: str = "",
               width: float = 9.6, height: float = 4.4, center=(-0.6, -0.5), label_end: bool = True, size: float = 13,
               nudge: dict | None = None, lw: float = 3.0, fmt_end=None) -> VGroup:
    """Lines over a shared x axis.  ``series``: {name: (dict x -> value, colour)}.  Returns VGroup with ``.frame`` (axes and
    labels), ``.ax``, ``.lines`` {name: line} and ``.labels`` {name: end label}."""
    xticks = xticks or [x[0], x[1]]
    yticks = yticks or [y[0], y[1]]
    pa = viz.plot_axes([x[0], x[1]], [y[0], y[1]], x_length=width, y_length=height, xticks=xticks, yticks=yticks,
                       xfmt=xfmt or (lambda v: f"{int(v)}"), yfmt=yfmt, ylabel=ylabel, size=size)
    if xlabel:
        pa[1].add(tx(xlabel, size, GREY_B).next_to(pa.ax.c2p((x[0] + x[1]) / 2, y[0]), DOWN, buff=0.55))
    pa.move_to([center[0], center[1], 0])
    g = VGroup(pa)
    g.frame, g.ax, g.lines, g.labels = pa, pa.ax, {}, {}
    nudge = nudge or {}
    for name, (data, col) in series.items():
        pts = sorted((k, v) for k, v in data.items() if v is not None and x[0] <= k <= x[1])
        if len(pts) < 2:
            continue
        ln = poly(pa.ax, pts, col, lw)
        g.lines[name] = ln
        g.add(ln)
        if label_end:
            xe, ye = pts[-1]
            txt = name if fmt_end is None else f"{name} {fmt_end(ye)}"
            lab = tx(txt, size + 1, col, bold=True).next_to(pa.ax.c2p(xe, ye), RIGHT, buff=0.12).shift(UP * nudge.get(name, 0.0))
            g.labels[name] = lab
            g.add(lab)
    return g


def hbars(items, max_value: float | None = None, x0: float = 0.0, top: float = 2.2, row: float = 0.52,
          length: float = 6.0, size: float = 16, bar_h: float = 0.34, name_gap: float = 0.15) -> VGroup:
    """Horizontal bars, one row per (name, value, colour, value_text).  Negative values grow left from ``x0``; the
    name sits left of the axis for positive values and right of it for negative ones.  Each row is VGroup(name, bar,
    value) and its bar carries ``.grow`` for :func:`beat`."""
    max_value = max_value or max(abs(v) for _, v, _, _ in items) or 1.0
    rows = VGroup()
    for i, (name, v, col, vt) in enumerate(items):
        yy = top - row * i
        L = np.sign(v) * max(abs(v) * length / max_value, 0.04)
        b = Rectangle(width=abs(L), height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([x0 + L / 2, yy, 0])
        b.grow = LEFT if v >= 0 else RIGHT
        nm = tx(name, size, WHITE)
        if v >= 0:
            nm.move_to([x0 - name_gap, yy, 0], aligned_edge=RIGHT)
        else:
            nm.move_to([x0 + name_gap, yy, 0], aligned_edge=LEFT)
        val = tx(vt, size - 1, col, bold=True).next_to(b, RIGHT if v >= 0 else LEFT, buff=0.1)
        rows.add(VGroup(nm, b, val))
    rows.axis = Line([x0, top + row * 0.6, 0], [x0, top - row * (len(items) - 0.4), 0], stroke_color=GREY_B, stroke_width=2)
    return rows


def vbars(items, base_y: float = -2.4, height: float = 4.2, width: float = 0.9, gap: float = 0.45, x0: float | None = None,
          max_value: float | None = None, size: float = 15) -> VGroup:
    """Vertical bars, one per (label, value, colour, value_text), left to right, growing up from ``base_y``."""
    max_value = max_value or max(v for _, v, _, _ in items) or 1.0
    n = len(items)
    x0 = -(n * width + (n - 1) * gap) / 2 + width / 2 if x0 is None else x0
    out = VGroup()
    for i, (lab, v, col, vt) in enumerate(items):
        h = max(height * v / max_value, 0.03)
        x = x0 + i * (width + gap)
        b = Rectangle(width=width, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([x, base_y + h / 2, 0])
        b.grow = DOWN
        out.add(VGroup(b, tx(vt, size, col, bold=True).next_to(b, UP, buff=0.08),
                       tx(lab, size - 1, GREY_A).next_to([x, base_y, 0], DOWN, buff=0.12)))
    return out


def dumbbell(items, x, center=(1.0, -0.4), width: float = 8.6, height: float = 5.0, xticks=None, xfmt=None,
             size: float = 15) -> VGroup:
    """Rows of (name, before, after): a grey dot for before, an arrow to a coloured dot for after."""
    from manim import Arrow
    n = len(items)
    pa = viz.plot_axes([x[0], x[1]], [0, n], x_length=width, y_length=height, xticks=xticks or [x[0], x[1]],
                       xfmt=xfmt, grid=False, size=13).move_to([center[0], center[1], 0])
    rows = VGroup()
    for i, (name, a, b) in enumerate(items):
        yy = n - 0.5 - i
        col = GOOD if b >= a else BAD
        d0 = Dot(pa.ax.c2p(a, yy), radius=0.07, color=GREY_B)
        d1 = Dot(pa.ax.c2p(b, yy), radius=0.09, color=col)
        arr = Arrow(pa.ax.c2p(a, yy), pa.ax.c2p(b, yy), buff=0.08, stroke_width=3, color=col,
                    max_tip_length_to_length_ratio=0.35, tip_length=0.13)
        nm = tx(name, size, WHITE, bold=True).next_to(pa.ax.c2p(x[0], yy), LEFT, buff=0.2)
        rows.add(VGroup(nm, d0, arr, d1))
    g = VGroup(pa, rows)
    g.frame, g.rows, g.ax = pa, rows, pa.ax
    return g


def stat_cards(items, y: float = 0.4, size: float = 40, span: float = 12.0) -> VGroup:
    """A row of big numbers with captions: (number_text, caption, colour)."""
    n = len(items)
    out = VGroup()
    for i, (num, cap, col) in enumerate(items):
        x = -span / 2 + span * (i + 0.5) / n
        card = VGroup(tx(num, size, col, bold=True), tx(cap, 15, GREY_A)).arrange(DOWN, buff=0.1).move_to([x, y, 0])
        if card.width > span / n - 0.2:
            card.scale_to_fit_width(span / n - 0.2)
        out.add(card)
    return out


def quote(lines, who: str, size: float = 16, width: float = 12.0) -> VGroup:
    """A quotation, its lines and its attribution, left-aligned."""
    g = VGroup(*[tx(l, size, WHITE) for l in lines], tx(who, size - 3, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    if g.width > width:
        g.scale_to_fit_width(width)
    return g


def bullets(lines, size: float = 17, color=WHITE, head: str = "", head_color: str = "#F6C453") -> VGroup:
    g = VGroup()
    if head:
        g.add(tx(head, size + 2, head_color, bold=True))
    for l in lines:
        g.add(tx(l, size, color))
    return g.arrange(DOWN, aligned_edge=LEFT, buff=0.1)


def table(rows, col_x, top: float = 2.0, row_h: float = 0.55, size: float = 16, colors=None, bold_first: bool = True) -> VGroup:
    """A table: ``rows`` is a list of lists of strings; ``col_x`` the x of each column's left edge.  Returns VGroup of
    row VGroups (the first is the header)."""
    out = VGroup()
    for i, r in enumerate(rows):
        g = VGroup()
        for j, (cell, x) in enumerate(zip(r, col_x)):
            col = (colors[i][j] if colors and colors[i] and colors[i][j] else (GREY_A if i == 0 else WHITE))
            t = tx(str(cell), size, col, bold=(i == 0 and bold_first))
            g.add(t.move_to([x, top - row_h * i, 0], aligned_edge=LEFT))
        out.add(g)
    return out


def head(text: str, size: float = 22):
    from manim import UP as _UP
    return tx(text, size, WHITE, bold=True).to_edge(_UP, buff=0.3)


def marker(ax, x, y, text: str, color, side=UP, size: float = 14, radius: float = 0.08) -> VGroup:
    """A dot on a chart with a label beside it."""
    d = Dot(ax.c2p(x, y), radius=radius, color=color)
    return VGroup(d, tx(text, size, color, bold=True).next_to(d, side, buff=0.1))


def hline(ax, y, x0, x1, color=GREY_B, text: str = "", size: float = 13) -> VGroup:
    ln = DashedLine(ax.c2p(x0, y), ax.c2p(x1, y), stroke_color=color, stroke_width=1.5, dash_length=0.08)
    g = VGroup(ln)
    if text:
        g.add(tx(text, size, color).next_to(ax.c2p(x0, y), UR, buff=0.06))
    return g


def callout(ax, x, y, text: str, color, at, size: float = 14, radius: float = 0.08) -> VGroup:
    """A dot on a chart with its label placed at ``at`` (data coordinates) and a thin leader line between them, for a
    point whose neighbourhood is too crowded for a label beside it."""
    d = Dot(ax.c2p(x, y), radius=radius, color=color)
    lab = tx(text, size, color, bold=True).move_to(ax.c2p(*at))
    end = lab.get_bottom() if at[1] > y else lab.get_top()
    ln = Line(end, d.get_center(), stroke_color=color, stroke_width=1.5, buff=0.08)
    return VGroup(d, ln, lab)
