"""Helpers shared by the scenes of Part 18 ("Pretraining at Scale").

Instruments of this part, worth sharing:

* :class:`ShardGrid`, devices as rows and a tensor's shards as cells; collectives (reduce-scatter, all-gather,
  all-to-all) animate as blocks moving between rows;
* :func:`gantt`, a pipeline schedule as a Gantt chart that fills in as time runs (``fill_gantt``);
* :func:`log2_axis`, a number line in powers of two with the ranges of floating-point formats;
* :func:`stage_row`, a row of boxes joined by arrows (a pipeline of stages).
"""

from __future__ import annotations

import math
import re

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18 import facts as F  # noqa: F401

from .compute import load  # noqa: F401

PART = 18
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
PAGE, KEPT, REMOVED, DUP, EDU = C.PAGE, C.KEPT, C.REMOVED, C.DUP, C.EDU  # the data pipeline
GPU, COMM = C.GPU, C.COMM  # devices; communication between them
WEIGHTS, GRADS, OPT, ACTS = C.WEIGHTS, C.GRADS, C.OPT_STATE, C.ACTS  # what memory holds
FWD, BWD, WGT = C.EMBED, C.GRADS, C.OPT_STATE  # pipeline: forward, backward (input), backward (weights)
N_COL, D_COL, C_COL, LR_COL = C.PARAMS, C.DATA, C.COMPUTE, C.LR
BASE_C = "#8FA3BF"  # our 2020 recipe
FULL_C = "#FF9F45"  # our 2026 recipe
PREC = {"fp32": GREY_A, "bf16": "#5CD0B3", "fp16": "#FF6B8B", "fp16_scaled": "#FFB86B", "fp8_tensor": "#B39DDB",
        "fp8_tile": "#6EA8FE"}
PREC_NAME = {"fp32": r"FP32", "bf16": r"BF16", "fp16": r"FP16, \ no loss scaling", "fp16_scaled": r"FP16, \ loss scaling",
             "fp8_tensor": r"FP8, \ one scale per tensor", "fp8_tile": r"FP8, \ one scale per tile"}
PREC_SPOKEN = {"fp32": "FP32", "bf16": "bfloat16", "fp16": "FP16 without loss scaling",
               "fp16_scaled": "FP16 with loss scaling", "fp8_tensor": "FP8 with one scale per tensor",
               "fp8_tile": "FP8 with one scale per tile"}
STAB_C = {"plain": "#FF6B8B", "qk": "#5CD0B3", "qkz": "#6EA8FE"}
STAB_NAME = {"plain": r"plain", "qk": r"QK-norm", "qkz": r"QK-norm $+$ z-loss"}
MTP_C = "#D4A5FF"
GROUP_C = ["#6EA8FE", "#FFB86B", "#5CD0B3", "#D4A5FF"]


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------
def human(x: float, digits: int = 3) -> str:
    """175e9 -> '175B', 1.4e12 -> '1.4T', 65e6 -> '65M', 274080 -> '274k' (plain text)."""
    for unit, v in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(x) >= v:
            y = x / v
            nd = max(0, digits - len(str(int(abs(y)))))
            s = f"{y:.{nd}f}"
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            return s + unit
    return f"{x:g}"


def pct(x: float, d: int = 1) -> str:
    return f"{100 * x:.{d}f}"


def nbytes(x: float) -> str:
    """Bytes in TeX text: 6.48e12 -> '6.5 TB'."""
    for unit, v in (("TB", 1e12), ("GB", 1e9), ("MB", 1e6), ("kB", 1e3)):
        if x >= v:
            return f"{x / v:.{1 if x / v < 100 else 0}f}" + rf"\,\mathrm{{{unit}}}"
    return f"{x:.0f}" + r"\,\mathrm{B}"


def spoken_int(n: float) -> str:
    """12,288 -> '12,288' for narration (the Chinese table strips the commas)."""
    return f"{int(round(n)):,}"


# ---------------------------------------------------------------------------
# Small drawing helpers
# ---------------------------------------------------------------------------
def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, fill=0.1, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    w = max(width or 0, t.width + 2 * pad)
    box = RoundedRectangle(width=w, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=fill)
    return VGroup(box, t.move_to(box))


def chip(text: str, color=GREY_B, font_size=22, height=0.46, fill=0.12) -> VGroup:
    """A token in a rounded box (monospaced data text, never translated)."""
    t = data_text(text.replace(" ", "␣") if text.strip() == "" else text, font=MONO, font_size=font_size,
                  color=WHITE)
    box = RoundedRectangle(width=max(t.width + 0.2, height * 0.8), height=height, corner_radius=0.08,
                           stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=fill)
    return VGroup(box, t.move_to(box))


def said(text: str, chars: int = 46, font_size: int = 20, max_lines: int = 3, color=WHITE, box_color=GREY_B) -> VGroup:
    """Words a model (or a web page) wrote: monospaced, wrapped, boxed, never translated."""
    import textwrap

    # a crawled page can carry someone's contact details: e-mail addresses and phone numbers are blanked
    text = re.sub(r"\S+@\S+\.\S+", "[e-mail]", text)
    text = re.sub(r"\+?\d{7,}|\(?\d{3}\)?[-\s.]\d{3}[-\s.]\d{4}", "[phone]", text)
    lines = textwrap.wrap(" ".join(text.split()), chars) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: chars - 3] + "..."
    t = data_text("\n".join(lines), font=MONO, font_size=font_size, color=color, line_spacing=0.8)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.32, corner_radius=0.12, stroke_color=box_color,
                           stroke_width=2, fill_color=box_color, fill_opacity=0.07)
    return VGroup(box, t.move_to(box))


def stat(value: str, caption: str, color=WHITE, font_size=44, cap_size=20) -> VGroup:
    v = label(value, font_size=font_size, color=color)
    c = label(caption, font_size=cap_size, color=GREY_A)
    return VGroup(v, c).arrange(DOWN, buff=0.12)


def take_away(text: str, color=C.BITS, font_size=30) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    band_ = RoundedRectangle(width=min(t.width + 0.8, 13.6), height=t.height + 0.4, corner_radius=0.14,
                             stroke_width=0, fill_color=color, fill_opacity=0.10)
    return VGroup(band_, t.move_to(band_)).to_edge(DOWN, buff=0.6)


def stage_row(items, buff=0.45, font_size=22, height=0.62) -> VGroup:
    """(text, colour) boxes in a row joined by arrows; ``.boxes`` and ``.arrows``."""
    boxes = VGroup(*[node_box(t, c, font_size=font_size, height=height) for t, c in items]).arrange(RIGHT, buff=buff)
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.3) for a, b in zip(boxes, boxes[1:])])
    g = VGroup(boxes, arrows)
    g.boxes, g.arrows = boxes, arrows
    return g


def hbars(items, max_value, width=5.0, bar_h=0.34, gap=0.16, font_size=20, label_width=3.2, fmt=lambda v: f"{v:g}",
          log=False, lo=0.0):
    """Horizontal bars: rows of (name, value, colour) -> VGroup of (name, bar, value) rows, top to bottom."""
    rows = VGroup()
    for i, (name, v, col) in enumerate(items):
        frac = ((math.log10(v) - lo) / (math.log10(max_value) - lo)) if log else v / max_value
        w = max(width * frac, 0.02)
        nm = label(name, font_size=font_size, color=GREY_A)
        if nm.width > label_width:
            nm.width = label_width
        y = -i * (bar_h + gap)
        bar = Rectangle(width=w, height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([w / 2, y, 0])
        nm.move_to([-0.2 - nm.width / 2, y, 0])
        val = label(fmt(v), font_size=font_size, color=col).next_to(bar, RIGHT, buff=0.12)
        rows.add(VGroup(nm, bar, val))
    return rows


def run_curve(ax, evals, color, x_of=lambda e: e[1], stroke_width=3):
    """A held-out loss curve from a run's evals ([step, tokens, loss] rows)."""
    return curve(ax, [x_of(e) for e in evals], [e[2] for e in evals], color, stroke_width)


# ---------------------------------------------------------------------------
# ShardGrid: a tensor cut across devices
# ---------------------------------------------------------------------------
class ShardGrid(VGroup):
    """``p`` devices (rows, labelled) by ``k`` shards (columns).  ``cells[r][c]`` is a square; ``paint`` fills
    cells, ``fly`` sends copies of cells to other cells (a collective), and ``label_col`` names the columns."""

    def __init__(self, p, k, cell=0.48, gap=0.07, row_gap=0.32, color=GPU, font_size=20, name=r"GPU",
                 row_names=None):
        super().__init__()
        self.p, self.k, self.cs = p, k, cell
        self.cells = []
        self.rows = VGroup()
        for r in range(p):
            row = VGroup(*[Square(cell, stroke_width=1.4, stroke_color=GREY_C, fill_color=GREY_D, fill_opacity=0.15)
                           for _ in range(k)]).arrange(RIGHT, buff=gap)
            self.cells.append(list(row))
            self.rows.add(row)
        self.rows.arrange(DOWN, buff=row_gap)
        self.names = VGroup(*[label(row_names[r] if row_names else rf"{name} {r}", font_size=font_size, color=color)
                              .next_to(self.rows[r], LEFT, buff=0.25) for r in range(p)])
        self.frames = VGroup(*[SurroundingRectangle(self.rows[r], buff=0.08, corner_radius=0.08, stroke_color=color,
                                                    stroke_width=1.6) for r in range(p)])
        self.add(self.frames, self.rows, self.names)

    def paint(self, r, c, color, opacity=0.85):
        return self.cells[r][c].animate.set_fill(color, opacity=opacity)

    def set(self, r, c, color, opacity=0.85):
        self.cells[r][c].set_fill(color, opacity=opacity)
        return self

    def fly(self, moves, color_after=None, opacity_after=0.85):
        """Animations for ``moves``: (src_row, src_col, dst_row, dst_col); copies travel and land.  Returns
        (travel animations, landing animations, the copies to remove)."""
        travel, land, ghosts = [], [], []
        for (r0, c0, r1, c1) in moves:
            g = self.cells[r0][c0].copy().set_stroke(width=0)
            ghosts.append(g)
            travel.append(g.animate.move_to(self.cells[r1][c1]).scale(0.8))
            col = color_after if color_after is not None else self.cells[r0][c0].get_fill_color()
            land.append(self.cells[r1][c1].animate.set_fill(col, opacity=opacity_after))
        return travel, land, ghosts

    def label_cols(self, texts, font_size=18, color=GREY_B):
        g = VGroup(*[label(t, font_size=font_size, color=color).next_to(self.cells[0][c], UP, buff=0.15)
                     for c, t in enumerate(texts)])
        return g


def play_fly(scene, grid, moves, run_time=0.9, color_after=None, opacity_after=0.85):
    travel, land, ghosts = grid.fly(moves, color_after, opacity_after)
    for g in ghosts:
        scene.add(g)
    scene.play(*travel, run_time=run_time)
    scene.play(*land, *[FadeOut(g) for g in ghosts], run_time=0.35)


# ---------------------------------------------------------------------------
# Pipeline Gantt charts
# ---------------------------------------------------------------------------
KIND_C = {"F": FWD, "B": BWD, "W": WGT}


def gantt(ops, p, total, width=11.0, row_h=0.5, gap=0.12, font_size=14, unit=1.0, numbers=True, shade_chunks=True):
    """``ops``: (device, kind, chunk, micro-batch, start, end) rows from ``sched.ops_list``.  Returns a VGroup with
    ``.rects`` (one per op, in the order of ``ops``), ``.starts``, ``.rows`` (device labels) and ``.scale``."""
    sc = width / (total * unit)
    g = VGroup()
    lanes = VGroup()
    for s in range(p):
        y = -s * (row_h + gap)
        lanes.add(Rectangle(width=width, height=row_h, stroke_width=1, stroke_color=GREY_D, fill_color=GREY_E,
                            fill_opacity=0.25).move_to([width / 2, y, 0]))
    names = VGroup(*[label(rf"GPU {s}", font_size=18, color=GPU).next_to(lanes[s], LEFT, buff=0.15) for s in range(p)])
    rects = VGroup()
    starts = []
    for (dev, kind, chunk, mb, a, b) in ops:
        y = -dev * (row_h + gap)
        col = KIND_C[kind]
        r = Rectangle(width=max((b - a) * sc * unit - 0.02, 0.02), height=row_h * 0.86, stroke_width=0.8,
                      stroke_color=BLACK, fill_color=col, fill_opacity=0.95 if (chunk == 0 or not shade_chunks) else 0.55)
        r.move_to([(a + b) / 2 * sc * unit, y, 0])
        if numbers and r.width > 0.16:
            t = Text(str(mb + 1), font=MONO, font_size=font_size, color=BLACK if chunk == 0 else WHITE).move_to(r)
            r = VGroup(r, t)
        rects.add(r)
        starts.append(a)
    g.add(lanes, names, rects)
    g.rects, g.starts, g.lanes, g.names, g.scale_x = rects, starts, lanes, names, sc * unit
    return g


def fill_gantt(scene, g, run_time=4.0):
    """Reveal the operations in order of start time, as if time were running."""
    order = sorted(range(len(g.rects)), key=lambda i: g.starts[i])
    T = max(g.starts) + 1e-9
    cursor = Line(g.lanes.get_corner(UL) + UP * 0.1, g.lanes.get_corner(DL) + DOWN * 0.1, color=YELLOW,
                  stroke_width=2).set_x(g.lanes.get_left()[0])
    scene.add(cursor)
    anims = [cursor.animate(run_time=run_time, rate_func=linear).set_x(g.lanes.get_left()[0] + g.lanes.width)]
    for i in order:
        anims.append(Succession(Wait(run_time * g.starts[i] / T * 0.97), FadeIn(g.rects[i], run_time=0.25)))
    scene.play(*anims, run_time=run_time + 0.3)
    scene.remove(cursor)


# ---------------------------------------------------------------------------
# Number formats
# ---------------------------------------------------------------------------
def log2_axis(lo=-40, hi=18, width=12.0, ticks=(-40, -30, -24, -20, -14, -10, 0, 10, 16), font_size=18):
    """A horizontal number line in powers of two; ``.x(e)`` is the x of 2^e."""
    sc = width / (hi - lo)
    x0 = -width / 2
    line = Line([x0, 0, 0], [x0 + width, 0, 0], color=GREY_C, stroke_width=2)
    g = VGroup(line)
    for e in ticks:
        x = x0 + (e - lo) * sc
        g.add(Line([x, -0.07, 0], [x, 0.07, 0], color=GREY_C, stroke_width=1.5))
        g.add(MathTex(rf"2^{{{e}}}", font_size=font_size, color=GREY_B).move_to([x, -0.32, 0]))
    g.x = lambda e: x0 + (e - lo) * sc
    g.line = line
    return g


def format_band(axis, lo_e, hi_e, color, y, text, sub_e=None, h=0.26, font_size=18):
    """A format's range on a log2 axis: subnormals (faint) from ``sub_e`` to ``lo_e``, normals to ``hi_e``."""
    g = VGroup()
    if sub_e is not None:
        g.add(Rectangle(width=axis.x(lo_e) - axis.x(sub_e), height=h, stroke_width=0, fill_color=color,
                        fill_opacity=0.25).move_to([(axis.x(lo_e) + axis.x(sub_e)) / 2, y, 0]))
    g.add(Rectangle(width=axis.x(hi_e) - axis.x(lo_e), height=h, stroke_width=0, fill_color=color,
                    fill_opacity=0.75).move_to([(axis.x(hi_e) + axis.x(lo_e)) / 2, y, 0]))
    t = label(text, font_size=font_size, color=color).next_to(g, LEFT, buff=0.15)
    g.add(t)
    g.name = t
    return g
