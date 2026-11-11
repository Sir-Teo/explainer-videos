"""Helpers shared by the scenes of Part 37 ("Networks II: Reliable Conversation")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code  # noqa: F401
from videos.cs.cs30.common import curve, fit_right, flow_box, log_axes  # noqa: F401
from videos.cs.cs31.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, KERN, LAM, NO, YES, edge_arrow,  # noqa: F401
                                   kv_rows)
from videos.cs.cs34.common import ms, num  # noqa: F401

from .compute import load  # noqa: F401

PART = 37
SEG, ACKC, LOSS, WIN = DATA, YES, NO, HEAD            # data segments, acknowledgements, losses, windows
CCC = {"reno": DATA, "cubic": LAM, "bbr": YES, "vegas": KERN, "fixed": NO}
CCN = {"reno": "Reno", "cubic": "CUBIC", "bbr": "BBR", "vegas": "Vegas", "fixed": "1986 TCP"}


def box(w, h, text, color=DATA, font_size=22, fill=None):
    """A rounded box with a text-mode label (Part 6's ``box`` sets its text as mathematics)."""
    b = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2.2,
                         fill_color=fill or BG, fill_opacity=1)
    t = label(text, font_size=font_size, color=color).move_to(b)
    if t.width > w - 0.14:
        t.width = w - 0.14
    if t.height > h - 0.08:
        t.height = h - 0.08
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def axes(x_range, y_range, x_length=7.0, y_length=3.8, x_label=None, y_label=None, xticks=None, yticks=None,
         fx=lambda v: f"{v:g}", fy=lambda v: f"{v:g}", font=16):
    """Linear axes with tick labels; returns a VGroup with .ax."""
    ax = Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
              axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True})
    g = VGroup(ax)
    if xticks is not None:
        g.add(VGroup(*[label(fx(x), font_size=font, color=GREY_B).next_to(ax.c2p(x, y_range[0]), DOWN, buff=0.1)
                       for x in xticks]))
    if yticks is not None:
        g.add(VGroup(*[label(fy(y), font_size=font, color=GREY_B).next_to(ax.c2p(x_range[0], y), LEFT, buff=0.1)
                       for y in yticks]))
    if x_label:
        g.add(label(x_label, font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.45))
    if y_label:
        g.add(label(y_label, font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
    g.ax = ax
    return g


def trace(ax, pts, color, width=2.5, x_max=None, y_max=None):
    """A polyline through (x, y) points, clipped to the axes' ranges."""
    xr, yr = ax.x_range, ax.y_range
    xm = x_max if x_max is not None else xr[1]
    ym = y_max if y_max is not None else yr[1]
    P = [ax.c2p(min(max(x, xr[0]), xm), min(max(y, yr[0]), ym)) for x, y in pts if x <= xm]
    return VMobject(color=color, stroke_width=width).set_points_as_corners(P)


def seq_diagram(events, t_max, height=5.0, gap=5.0, names=(r"sender", r"receiver"), font=17, center=ORIGIN):
    """A sequence diagram: time runs down two vertical lines.  events: (t_from, t_to or None, text, from_left,
    color); ``None`` draws a packet lost half way, with a cross.  Returns a VGroup with .arrows (in order)."""
    top = height / 2
    xl, xr = -gap / 2, gap / 2

    def y(t):
        return top - t / t_max * height

    g = VGroup()
    ll = Line([xl, top + 0.1, 0], [xl, -top - 0.1, 0], color=GREY_C, stroke_width=2)
    lr = Line([xr, top + 0.1, 0], [xr, -top - 0.1, 0], color=GREY_C, stroke_width=2)
    nl = label(names[0], font_size=font + 2, color=GREY_A).next_to(ll, UP, buff=0.1)
    nr = label(names[1], font_size=font + 2, color=GREY_A).next_to(lr, UP, buff=0.1)
    g.add(ll, lr, nl, nr)
    arrows = VGroup()
    for t0, t1, text, from_left, color in events:
        x0, x1 = (xl, xr) if from_left else (xr, xl)
        if t1 is None:
            mid = np.array([(x0 + x1) / 2, y(t0) - (gap / 2) / gap * 0.25 * height / 2, 0])
            ln = Line([x0, y(t0), 0], mid, color=color, stroke_width=2.2)
            cross = VGroup(Line(mid + [-0.12, -0.12, 0], mid + [0.12, 0.12, 0], color=NO, stroke_width=4),
                           Line(mid + [-0.12, 0.12, 0], mid + [0.12, -0.12, 0], color=NO, stroke_width=4))
            a = VGroup(ln, cross)
            lab_pos = ln.get_center()
        else:
            a = VGroup(Arrow([x0, y(t0), 0], [x1, y(t1), 0], buff=0.02, color=color, stroke_width=2.4,
                             max_tip_length_to_length_ratio=0.06, tip_length=0.16))
            lab_pos = a.get_center()
        if text:
            t = label(text, font_size=font, color=color)
            t.move_to(lab_pos + UP * 0.17)
            bg = BackgroundRectangle(t, color=BG, fill_opacity=0.85, buff=0.03)
            a.add(bg, t)
        arrows.add(a)
    g.add(arrows)
    g.arrows = arrows
    g.y = y
    g.xl, g.xr = xl, xr
    g.shift(center)
    return g


def window_axes(t_max, x_length=10.5, y_length=4.4, step=5):
    """Window (packets, log scale 1 to 10,000) against seconds; .pt(t, w) maps a point, .line(points, colour)."""
    import math as _m
    g = axes([0, t_max, step], [0, 4, 1], x_length=x_length, y_length=y_length, x_label=r"seconds",
             y_label=r"window, \ packets \ (log scale)", xticks=range(0, int(t_max) + 1, step), yticks=(0, 1, 2, 3, 4),
             fy=lambda v: f"{10 ** v:,.0f}")
    ax = g.ax

    def line(pts, color, width=2.6, x_max=None):
        return trace(ax, [(t, _m.log10(max(1.0, w))) for t, w in pts], color, width=width, x_max=x_max)

    def hline(w, color, text=None, font=17, side=UP):
        y = _m.log10(w)
        ln = DashedLine(ax.c2p(0, y), ax.c2p(t_max, y), color=color, dash_length=0.1)
        out = VGroup(ln)
        if text:
            out.add(label(text, font_size=font, color=color).next_to(ax.c2p(t_max, y), side, buff=0.05).shift(
                LEFT * 1.2))
        return out

    g.line, g.hline = line, hline
    return g
