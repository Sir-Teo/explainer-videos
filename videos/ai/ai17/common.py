"""Helpers shared by the scenes of Part 17 ("Silicon").

Instruments that deserve sharing with Parts 18 and 19 (``roofline_axes``, ``ring_devices``, ``bit_strip``,
``matrix_grid``) are written to stand alone, so they could move to ``explainer/ai/viz.py`` unchanged.
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401
from .specs import GPUS  # noqa: F401

PART = 17
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
FLOPC = C.COMPUTE  # arithmetic: FLOPs, FLOP/s, the flat roof
BYTEC = C.DRAM  # main memory (DRAM, HBM), bytes moved, the bandwidth slope
REGC = "#9BE37B"  # registers
L1C, L2C, L3C = C.CACHE_L1, C.CACHE_L2, C.CACHE_L3  # caches, SRAM, shared memory (L1C)
CPUC = C.MSG  # the CPU, this machine
GPUC = C.GPU  # GPUs and accelerators
COMMC = "#FF7EB6"  # communication between chips: links, messages, collectives
POWERC = C.HOT  # power, watts, heat
A_C, B_C, C_C = C.EMBED, C.MOMENTUM, C.PROB  # the matrices A, B and C = AB
SIGNC, EXPC, MANC = C.SIGN_BIT, C.EXP_BIT, C.MAN_BIT  # floating-point fields
WARPC = C.KEY  # threads and warps
IDLEC = GREY_D  # idle lanes, wasted slots

COLORS = {r"A": A_C, r"B": B_C, r"C": C_C, r"P": FLOPC, r"\beta": BYTEC, r"I": FLOPC}


def machine_name() -> str:
    m = load("machine")
    return m.get("model_short") or m.get("model", "this computer")


def gflops(x: float) -> str:
    """A rate in FLOP/s as GFLOP/s text with sensible digits."""
    g = x / 1e9
    return f"{g:.0f}" if g >= 10 else (f"{g:.1f}" if g >= 1 else f"{g:.2f}")


def gbs(x: float) -> str:
    g = x / 1e9
    return f"{g:.0f}" if g >= 10 else f"{g:.1f}"


def spoken_big(x: float) -> str:
    """1.5e18 -> 'one point five times ten to the eighteen'-style digits the narrator reads: '1.5 times 10 to the 18'."""
    e = int(math.floor(math.log10(x)))
    m = x / 10 ** e
    return f"{m:.1f} times 10 to the {e}"


# ---------------------------------------------------------------------------
# Boxes, chips and grids
# ---------------------------------------------------------------------------
def box_label(text: str, color, width=None, height=0.62, font_size=24, fill=0.12, stroke_width=2.2) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    w = width or (t.width + 0.44)
    box = RoundedRectangle(width=w, height=max(height, t.height + 0.25), corner_radius=0.12, stroke_color=color,
                           stroke_width=stroke_width, fill_color=color, fill_opacity=fill)
    g = VGroup(box, t.move_to(box))
    g.box, g.text = box, t
    return g


def matrix_grid(rows: int, cols: int, cell=0.32, color=WHITE, fill=0.12, stroke=1.2, buff=0.0) -> VGroup:
    """A matrix as a grid of square cells; ``g.cell(i, j)``."""
    cells = VGroup(*[Square(cell, stroke_color=color, stroke_width=stroke, fill_color=color, fill_opacity=fill)
                     for _ in range(rows * cols)])
    cells.arrange_in_grid(rows=rows, cols=cols, buff=buff)
    g = VGroup(cells)
    g.cells, g.rows, g.cols = cells, rows, cols
    g.cell = lambda i, j: cells[i * cols + j]
    return g


def bit_strip(fields, cell=0.3, font_size=20, show_bits=True) -> VGroup:
    """A floating-point layout: ``fields`` is [(bits as a string, colour), ...], left to right (sign, exponent,
    mantissa). Each bit is a box; ``g.parts[k]`` is the k-th field."""
    parts = VGroup()
    for bits, col in fields:
        boxes = VGroup()
        for b in bits:
            sq = Rectangle(width=cell, height=cell * 1.25, stroke_color=col, stroke_width=1.6, fill_color=col,
                           fill_opacity=0.28)
            if show_bits:
                d = Text(b, font=MONO, font_size=font_size, color=WHITE).move_to(sq)
                boxes.add(VGroup(sq, d))
            else:
                boxes.add(VGroup(sq))
        boxes.arrange(RIGHT, buff=0.0)
        parts.add(boxes)
    parts.arrange(RIGHT, buff=0.06)
    g = VGroup(parts)
    g.parts = parts
    return g


def cpu_die(width=4.6, height=3.6, cores=4) -> VGroup:
    """Schematic CPU: a few big cores with control and cache, a large shared cache."""
    die = RoundedRectangle(width=width, height=height, corner_radius=0.1, stroke_color=CPUC, stroke_width=2,
                           fill_color="#141A24", fill_opacity=1)
    g = VGroup(die)
    cw, ch = (width - 0.5) / 2, (height - 0.5) * 0.62 / 2
    cores_g = VGroup()
    for k in range(cores):
        core = VGroup(
            Rectangle(width=cw, height=ch, stroke_color=CPUC, stroke_width=1.5, fill_color=CPUC, fill_opacity=0.12),
        )
        ctrl = Rectangle(width=cw * 0.55, height=ch * 0.45, stroke_width=0, fill_color=GREY_C, fill_opacity=0.5)
        alu = Rectangle(width=cw * 0.3, height=ch * 0.45, stroke_width=0, fill_color=FLOPC, fill_opacity=0.7)
        l1 = Rectangle(width=cw * 0.9, height=ch * 0.28, stroke_width=0, fill_color=L1C, fill_opacity=0.5)
        VGroup(ctrl, alu).arrange(RIGHT, buff=0.08).move_to(core[0]).shift(UP * ch * 0.18)
        l1.move_to(core[0]).shift(DOWN * ch * 0.28)
        core.add(ctrl, alu, l1)
        cores_g.add(core)
    cores_g.arrange_in_grid(rows=2, cols=2, buff=0.15)
    cache = Rectangle(width=width - 0.5, height=(height - 0.5) * 0.3, stroke_width=0, fill_color=L3C, fill_opacity=0.45)
    body = VGroup(cores_g, cache).arrange(DOWN, buff=0.15).move_to(die)
    g.add(body)
    g.die, g.cores, g.cache = die, cores_g, cache
    return g


def gpu_die(width=4.6, height=3.6, sms=(6, 8), lanes=(4, 4)) -> VGroup:
    """Schematic GPU: a grid of streaming multiprocessors, each a block of many small arithmetic lanes; L2 across."""
    die = RoundedRectangle(width=width, height=height, corner_radius=0.1, stroke_color=GPUC, stroke_width=2,
                           fill_color="#141A24", fill_opacity=1)
    rows, cols = sms
    sw = (width - 0.4) / cols - 0.06
    sh = (height - 0.4) * 0.8 / rows - 0.06
    grid = VGroup()
    for _ in range(rows * cols):
        sm = VGroup(Rectangle(width=sw, height=sh, stroke_color=GPUC, stroke_width=0.8, fill_color=GPUC,
                              fill_opacity=0.08))
        lr, lc = lanes
        dots = VGroup(*[Square(min(sw / (lc + 1), sh / (lr + 1)) * 0.6, stroke_width=0, fill_color=FLOPC,
                               fill_opacity=0.75) for _ in range(lr * lc)])
        dots.arrange_in_grid(rows=lr, cols=lc, buff=min(sw / (lc + 1), sh / (lr + 1)) * 0.3).move_to(sm[0])
        sm.add(dots)
        grid.add(sm)
    grid.arrange_in_grid(rows=rows, cols=cols, buff=0.06)
    l2 = Rectangle(width=width - 0.4, height=(height - 0.4) * 0.12, stroke_width=0, fill_color=L2C, fill_opacity=0.45)
    body = VGroup(grid, l2).arrange(DOWN, buff=0.1).move_to(die)
    g = VGroup(die, body)
    g.die, g.sms, g.l2 = die, grid, l2
    return g


# ---------------------------------------------------------------------------
# Log-log plots: the roofline
# ---------------------------------------------------------------------------
def pow10(v) -> str:
    v = int(round(v))
    if v == 0:
        return "1"
    if v == 1:
        return "10"
    if v == 2:
        return "100"
    if v == 3:
        return r"1{,}000"
    if v == -1:
        return "0.1"
    if v == -2:
        return "0.01"
    return rf"10^{{{v}}}"


def loglog(x_range, y_range, x_length=7.0, y_length=4.4, xlabel="", ylabel="", center=ORIGIN, font_size=20,
           xstep=1, ystep=1) -> VGroup:
    """Axes for log10 x and log10 y (ranges given as exponents), ticks at powers of ten."""
    xt = list(range(int(math.ceil(x_range[0])), int(math.floor(x_range[1])) + 1, xstep))
    yt = list(range(int(math.ceil(y_range[0])), int(math.floor(y_range[1])) + 1, ystep))
    g = axes(x_range, y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel, xticks=xt,
             yticks=yt, xfmt=pow10, yfmt=pow10, font_size=font_size, center=center)
    return g


def roof_points(ax, peak, bw, x_range):
    """The roofline min(peak, bw * I) on log axes (log10 of FLOP/byte against log10 of FLOP/s)."""
    xs = np.linspace(x_range[0], x_range[1], 300)
    ys = np.minimum(math.log10(peak), math.log10(bw) + xs)
    return [ax.c2p(x, y) for x, y in zip(xs, ys)]


def roof_line(ax, peak, bw, x_range, color=WHITE, stroke_width=4, y_min=None) -> VMobject:
    pts = roof_points(ax, peak, bw, x_range)
    if y_min is not None:
        y0 = ax.c2p(0, y_min)[1]
        pts = [p for p in pts if p[1] >= y0 - 1e-6]
    return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners(pts)


# ---------------------------------------------------------------------------
# Devices on a ring, for collectives
# ---------------------------------------------------------------------------
def ring_devices(p: int, radius=2.2, center=ORIGIN, size=0.9, color=GPUC, names=None) -> VGroup:
    devs = VGroup()
    for r in range(p):
        ang = PI / 2 - 2 * PI * r / p
        pos = np.asarray(center) + radius * np.array([math.cos(ang), math.sin(ang), 0])
        box = RoundedRectangle(width=size * 1.35, height=size, corner_radius=0.1, stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=0.1).move_to(pos)
        nm = label(names[r] if names else rf"GPU {r}", font_size=18, color=color).next_to(box, UP, buff=0.06)
        devs.add(VGroup(box, nm))
    return devs


def arrow_between(a: Mobject, b: Mobject, color=COMMC, buff=0.12, stroke_width=3, angle=0.0) -> Mobject:
    if angle:
        return CurvedArrow(a.get_center(), b.get_center(), angle=angle, color=color, stroke_width=stroke_width,
                           tip_length=0.15)
    return Arrow(a.get_center(), b.get_center(), buff=buff + max(a.width, a.height) / 2, color=color,
                 stroke_width=stroke_width, max_tip_length_to_length_ratio=0.15, tip_length=0.18)


def spec_table(rows, col_colors=None, font_size=22, h_buff=0.45, v_buff=0.2) -> VGroup:
    """A small table of Tex cells: rows of strings, the first row the header (grey)."""
    tab = VGroup()
    for i, r in enumerate(rows):
        cells = VGroup()
        for j, c in enumerate(r):
            col = GREY_B if i == 0 else (col_colors[j] if col_colors else WHITE)
            cells.add(label(c, font_size=font_size, color=col))
        tab.add(cells)
    ncol = max(len(r) for r in rows)
    widths = [max(tab[i][j].width for i in range(len(rows)) if j < len(tab[i])) for j in range(ncol)]
    y = 0.0
    for i, cells in enumerate(tab):
        x = 0.0
        hmax = max(c.height for c in cells)
        for j, c in enumerate(cells):
            c.move_to([x + widths[j] / 2 if j else x + c.width / 2, y - hmax / 2, 0])
            if j:
                c.set_x(x + widths[j] - c.width / 2)  # numbers right-aligned
            x += widths[j] + h_buff
        y -= hmax + v_buff
    line = Line(LEFT, RIGHT, color=GREY_D, stroke_width=1.2)
    line.set_width(sum(widths) + h_buff * (ncol - 1))
    line.move_to([line.width / 2, (tab[0].get_bottom()[1] + tab[1].get_top()[1]) / 2 if len(tab) > 1 else 0, 0])
    g = VGroup(tab, line)
    g.tab = tab
    return g.move_to(ORIGIN)


def code_lines(lines, font_size=20, color=GREY_A, buff=0.12) -> VGroup:
    """Source code as monospaced lines, keeping indentation; drawn with ``data_text`` so it is never translated."""
    em = Text("M" * 20, font=MONO, font_size=font_size).width / 20
    rows = VGroup(*[data_text(s.strip() or ".", font=MONO, font_size=font_size, color=color) for s in lines])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    for r, s in zip(rows, lines):
        if not s.strip():
            r.set_opacity(0)
        r.shift(RIGHT * em * (len(s) - len(s.lstrip(" "))))
    return rows
