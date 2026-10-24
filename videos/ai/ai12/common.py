"""Helpers shared by the scenes of Part 12 ("The Mathematics of Scale")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 12

# one meaning per colour, for the whole part
SP = C.SURPRISE  # the standard parametrization; things that drift or fail
MUP = C.INTERVAL  # muP, and the depth scalings that transfer
LAZY = "#7FD3FF"  # the lazy / kernel regime, frozen features
RICH = C.MODEL_Q  # feature learning, the rich regime
NCOL = C.BITS  # model size N, parameters
DCOL = C.TRUE_P  # data D, training tokens / characters
CCOL = C.CONTEXT  # compute C
FIT = WHITE  # fitted laws
HIST = C.HUMAN  # history cards
TT = C.ADVANTAGE  # test-time compute, tries
QUANT = "#5CD0B3"  # quanta, skills
WIDTH_COLORS = ["#7FD3FF", C.BITS, C.MODEL_Q]  # three widths (small, medium, large)
BUDGET_COLORS = ["#FFE08A", C.BITS, C.MODEL_Q, C.SURPRISE, "#D4A5FF"]  # five compute budgets, small to large
DEPTH_COLORS = ["#4FA3D9", "#7FD3FF", C.BITS, C.MODEL_Q, C.SURPRISE]

PANEL_FILL = "#121722"


def ramp(i: int, n: int, a="#4FA3D9", b=C.SURPRISE) -> ManimColor:
    """The i-th of n colours from cool (small) to warm (large)."""
    return interpolate_color(ManimColor(a), ManimColor(b), i / max(1, n - 1))


def width_ramp(i: int, n: int) -> ManimColor:
    """Model sizes, small to large: blue through yellow to red."""
    stops = [ManimColor("#4FA3D9"), ManimColor(C.BITS), ManimColor(C.SURPRISE)]
    t = i / max(1, n - 1)
    if t <= 0.5:
        return interpolate_color(stops[0], stops[1], t * 2)
    return interpolate_color(stops[1], stops[2], (t - 0.5) * 2)


def log_axes(x_range, y_range, x_length=8.0, y_length=4.6, center=ORIGIN, x_ticks=(), y_ticks=(), y_fmt="{:.1f}",
             font_size=22):
    """Axes whose x coordinate is log10 of the quantity; tick labels written as given."""
    ax = CornerAxes(x_range=[*x_range, 1], y_range=[*y_range, (y_range[1] - y_range[0]) / 4], x_length=x_length,
                    y_length=y_length, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05})
    ax.move_to(center)
    labels = VGroup(*[MathTex(t, font_size=font_size, color=GREY_B).next_to(ax.c2p(v, y_range[0]), DOWN, buff=0.1)
                      for t, v in x_ticks],
                    *[MathTex(y_fmt.format(v) if not isinstance(v, tuple) else v[0], font_size=font_size, color=GREY_B)
                      .next_to(ax.c2p(x_range[0], v if not isinstance(v, tuple) else v[1]), LEFT, buff=0.1)
                      for v in y_ticks])
    return ax, labels


def pow10(k) -> str:
    return rf"10^{{{int(k)}}}"


def pow2(k) -> str:
    return rf"2^{{{int(k)}}}"


def big(x: float) -> str:
    """A count for narration: 2400000 -> '2.4 million', 31000 -> '31,000'."""
    if x >= 1e9:
        return f"{x / 1e9:.1f} billion"
    if x >= 1e6:
        return f"{x / 1e6:.1f} million"
    if x >= 1e4:
        return f"{round(x, -3):,.0f}"
    return f"{x:,.0f}"


def big_tex(x: float) -> str:
    """The same count for MathTex: 2.4 \\text{ million}."""
    if x >= 1e9:
        return rf"{x / 1e9:.1f}" + r"\text{ billion}"
    if x >= 1e6:
        return rf"{x / 1e6:.1f}" + r"\text{ million}"
    return f"{x:,.0f}".replace(",", "{,}")


def words(n: int) -> str:
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
    return w[n] if 0 <= n < len(w) else f"{n:,}"


def panel(width, height, center=ORIGIN, color=GREY_D) -> RoundedRectangle:
    return RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=color, stroke_width=1.5,
                            fill_color=PANEL_FILL, fill_opacity=1).move_to(center)


def dots(ax, xs, ys, color, radius=0.06) -> VGroup:
    return VGroup(*[Dot(ax.c2p(x, y), radius=radius, color=color) for x, y in zip(xs, ys) if np.isfinite(y)])


def era_strip(scene, events, head_text=r"How we got here", tag_text=r"milestones evenly spaced, \ not to scale",
              y0=-0.2, color=None, font_size=21):
    """Part 13's era timeline: events [(year, text)] evenly spaced, alternating above and below; returns the marks."""
    color = color or HIST
    n = len(events)
    xs = np.linspace(-5.9, 5.9, n)
    axis = Line([-6.6, y0, 0], [6.6, y0, 0], color=GREY_C, stroke_width=3)
    marks, skel = [], VGroup()
    for i, ((yr, txt), x) in enumerate(zip(events, xs)):
        up = i % 2 == 0
        stem = Line([x, y0, 0], [x, y0 + (0.9 if up else -0.9), 0], color=color, stroke_width=2.5)
        dot = Dot([x, y0, 0], radius=0.08, color=color)
        yl = label(rf"{yr}", font_size=30, color=color)
        t = label(txt, font_size=font_size, color=WHITE)
        w = VGroup(yl, t).arrange(DOWN, buff=0.06)
        w.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
        keep_in_frame(w, margin=0.12)
        marks.append(VGroup(stem, dot, w))
        skel.add(VGroup(stem.copy().set_stroke(GREY_D), Dot([x, y0, 0], radius=0.06, color=GREY_D),
                        yl.copy().set_color(GREY_D).move_to(yl)))
    head = label(head_text, font_size=42).to_edge(UP, buff=0.3)
    tag = note(tag_text).to_corner(DR, buff=0.2)
    return head, axis, tag, skel, marks


def table_card(rows, col_colors=None, font_size=24, head_color=GREY_A, buff_x=0.45, buff_y=0.22) -> VGroup:
    """A small table: rows of Tex cells (the first row is the header), columns aligned left."""
    grid = VGroup()
    for r, cells in enumerate(rows):
        row = VGroup()
        for c, txt in enumerate(cells):
            col = head_color if r == 0 else (col_colors[c] if col_colors else WHITE)
            row.add(label(txt, font_size=font_size, color=col))
        grid.add(row)
    ncol = len(rows[0])
    widths = [max(grid[r][c].width for r in range(len(rows))) for c in range(ncol)]
    y = 0.0
    for r, row in enumerate(grid):
        x = 0.0
        h = max(m.height for m in row)
        for c, m in enumerate(row):
            m.move_to([x + m.width / 2, y - h / 2, 0])
            x += widths[c] + buff_x
        y -= h + buff_y
    line = Line(grid[0].get_corner(DL) + DOWN * buff_y / 2 + LEFT * 0.1,
                [grid.get_right()[0] + 0.1, grid[0].get_bottom()[1] - buff_y / 2, 0], color=GREY_D, stroke_width=1.5)
    return VGroup(grid, line).move_to(ORIGIN)


def sweep_grid(s):
    """The sweep's arrays: (widths, N, D, bits) with bits[i, j] for width i and length 2^ks[j]."""
    return (list(s["widths"]), np.asarray(s["N"], float), np.asarray(s["D"], float), np.asarray(s["bits"], float))


def lag(anims, **kw) -> Animation:
    """LaggedStart that tolerates an empty list (a measurement with nothing to show)."""
    anims = list(anims)
    return LaggedStart(*anims, **kw) if anims else Wait(kw.get("run_time", 0.1))
