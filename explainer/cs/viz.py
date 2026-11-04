"""The visual instruments of *Computer Science, Built* (videos/cs/SYLLABUS.md, section 3), in the manner of
3Blue1Brown.  Each part adds the instruments it first needs; the series reuses them unchanged.

* :class:`TapeView`: a Turing machine's tape, its head and its state, stepping through a run;
* :class:`RuleTable`: a machine's transition table with the rule being applied lit;
* :func:`bitmap`: an array of colour indices or RGB values as a crisp image (space-time diagrams of tapes and
  cellular automata, tables too large to draw cell by cell);
* :func:`chip` and :func:`node_box`: small labelled boxes for states, symbols, registers and modules.
"""

from __future__ import annotations

import numpy as np
from manim import *  # noqa: F403

from explainer.style import BACKGROUND, C  # noqa: F401

MONO = "DejaVu Sans Mono"
BLANK = "\u25a1"  # the blank symbol, as the textbooks draw it


def _verbatim_text(s: str, **kw) -> Text:
    """Text that is data (symbols on a tape, rule entries): never translated."""
    from explainer.zh_text import verbatim

    with verbatim():
        return Text(s, **kw)


def chip(text: str, color=GREY_B, font_size=26, height=0.5, width=None, fill=0.14, mono=True) -> VGroup:
    """A rounded box with a short monospace label: a state, a symbol, a register."""
    t = _verbatim_text(text, font=MONO if mono else "DejaVu Sans", font_size=font_size, color=WHITE)
    w = width or max(height, t.width + 0.3)
    box = RoundedRectangle(width=w, height=height, corner_radius=0.08, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=fill)
    g = VGroup(box, t.move_to(box))
    g.box, g.text = box, t
    return g


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62) -> VGroup:
    """A rounded box around a Tex label (translated in the Chinese build)."""
    from explainer.analysis import label

    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    g = VGroup(box, t.move_to(box))
    g.box, g.text = box, t
    return g


# ---------------------------------------------------------------------------
# Turing machines
# ---------------------------------------------------------------------------
SYMBOL_COLOR = {"0": C.BIT0, "1": C.BIT1, "_": GREY_D, "x": C.CS_FALSE, "#": GREY_A, "a": C.CS_DATA,
                "b": C.CS_FUNC, "X": C.CS_FALSE, "Y": C.CS_TRUE}


class TapeView(VGroup):
    """A finite window onto an infinite tape: ``symbols[i]`` is cell i (``"_"`` is blank, drawn empty), the head is a
    pointer above cell ``head`` with the machine's ``state`` in a chip.  Dots at both ends say the tape goes on.

    Animations: :meth:`write` (a cell's symbol changes, with a flash), :meth:`move_to_cell` (the head slides),
    :meth:`set_state` (the chip's label changes), and :meth:`step` (all three, as one step of the machine).
    ``.cells`` are the squares, ``.syms`` the symbols (one mobject per cell), ``.head`` the pointer and chip."""

    def __init__(self, symbols, head: int | None = 0, state: str | None = "A", cell=0.62, font_size=30,
                 colors: dict | None = None, ellipsis=True, state_color=None, show_index=False):
        super().__init__()
        self.cell = cell
        self.font_size = font_size
        self.colors = {**SYMBOL_COLOR, **(colors or {})}
        self.state_color = state_color or C.CS_CONTROL
        n = len(symbols)
        self.cells = VGroup(*[Square(cell, stroke_color=GREY_B, stroke_width=2, fill_color="#151B26",
                                     fill_opacity=1) for _ in range(n)]).arrange(RIGHT, buff=0)
        self.add(self.cells)
        self.symbols = list(symbols)
        self.syms = VGroup(*[self._sym(s, i) for i, s in enumerate(symbols)])
        self.add(self.syms)
        if ellipsis:
            dots_l = VGroup(*[Dot(radius=0.035, color=GREY_C) for _ in range(3)]).arrange(RIGHT, buff=0.1)
            dots_r = dots_l.copy()
            dots_l.next_to(self.cells, LEFT, buff=0.18)
            dots_r.next_to(self.cells, RIGHT, buff=0.18)
            self.dots = VGroup(dots_l, dots_r)
            self.add(self.dots)
        if show_index:
            self.index = VGroup(*[Text(str(i), font_size=14, color=GREY_C).next_to(c, DOWN, buff=0.08)
                                  for i, c in enumerate(self.cells)])
            self.add(self.index)
        self.pos = head
        self.state = state
        self.head = VGroup()
        if head is not None:
            self.head = self._head(head, state)
            self.add(self.head)

    # -- pieces ---------------------------------------------------------------
    def _sym(self, s: str, i: int) -> Mobject:
        if s in ("_", " ", ""):
            return VectorizedPoint(self.cells[i].get_center())
        t = _verbatim_text(s, font=MONO, font_size=self.font_size, color=self.colors.get(s, WHITE))
        return t.move_to(self.cells[i].get_center())

    def _head(self, i: int, state) -> VGroup:
        tri = Triangle(color=C.CS_HEAD, fill_color=C.CS_HEAD, fill_opacity=1, stroke_width=0)
        tri.rotate(PI).scale_to_fit_width(self.cell * 0.42)
        tri.next_to(self.cells[i], UP, buff=0.08)
        g = VGroup(tri)
        if state is not None:
            st = chip(str(state), color=self.state_color, font_size=int(self.font_size * 0.8),
                      height=self.cell * 0.72).next_to(tri, UP, buff=0.06)
            g.add(st)
        g.tri = tri
        return g

    def cell_center(self, i: int):
        return self.cells[i].get_center()

    # -- animations -------------------------------------------------------------
    def write(self, i: int, s: str, run_time=0.4) -> Animation:
        new = self._sym(s, i)
        old = self.syms[i]
        self.syms.submobjects[i] = new
        self.symbols[i] = s
        flash = self.cells[i].copy().set_fill(C.CS_HEAD, opacity=0.35).set_stroke(width=0)
        return AnimationGroup(FadeTransform(old, new), ShowPassingFlash(flash.copy(), time_width=1.0),
                              run_time=run_time)

    def move_to_cell(self, i: int, run_time=0.4) -> Animation:
        dx = self.cells[i].get_center()[0] - self.cells[self.pos].get_center()[0]
        self.pos = i
        return self.head.animate(run_time=run_time).shift(RIGHT * dx)

    def set_state(self, state, run_time=0.3) -> Animation:
        self.state = state
        if len(self.head) < 2:
            return Wait(0.01)
        old = self.head[1]
        new = chip(str(state), color=C.CS_TRUE if str(state) in ("H", "halt", "accept") else self.state_color,
                   font_size=int(self.font_size * 0.8), height=self.cell * 0.72).move_to(old)
        self.head.submobjects[1] = new
        return FadeTransform(old, new, run_time=run_time)

    def step(self, write: str, move: int, state, run_time=0.9) -> Succession:
        """One step: write ``write`` under the head, change state, move ``move`` (-1, 0, +1) cells."""
        anims = []
        if write != self.symbols[self.pos]:
            anims.append(self.write(self.pos, write, run_time=run_time * 0.45))
        if state != self.state:
            anims.append(self.set_state(state, run_time=run_time * 0.3))
        first = AnimationGroup(*anims) if anims else Wait(run_time * 0.3)
        target = min(max(self.pos + move, 0), len(self.cells) - 1)
        return Succession(first, self.move_to_cell(target, run_time=run_time * 0.55))


class RuleTable(VGroup):
    """A transition table: one row per rule (state, read) -> (write, move, next).  ``rules`` is a list of 5-tuples of
    strings.  :meth:`light` moves a highlight onto a row (the rule being applied)."""

    def __init__(self, rules, font_size=24, header=True, col_gap=0.42, row_gap=0.13, arrow=True):
        super().__init__()
        from explainer.analysis import label

        rows = VGroup()
        if header:
            names = [r"state", r"read", "", r"write", r"move", r"next"]
            hdr = VGroup(*[label(n, font_size=font_size - 6, color=GREY_B) if n else VectorizedPoint()
                           for n in names])
            rows.add(hdr)
        self.rule_rows = VGroup()
        def sym(s):  # the blank shows as a box, the way the textbooks write it
            return chip(BLANK if s in ("_", " ") else s, SYMBOL_COLOR.get(s, C.CS_DATA), font_size)

        for st, rd, wr, mv, nx in rules:
            cols = [chip(st, C.CS_CONTROL, font_size), sym(rd),
                    MathTex(r"\to", font_size=font_size + 6, color=GREY_B),
                    sym(wr),
                    chip(mv, GREY_B, font_size),
                    chip(nx, C.CS_TRUE if nx in ("H", "halt") else C.CS_CONTROL, font_size)]
            r = VGroup(*cols)
            rows.add(r)
            self.rule_rows.add(r)
        ncol = 6
        widths = [max(r[j].width for r in rows) for j in range(ncol)]
        for k, r in enumerate(rows):
            x = 0.0
            for j in range(ncol):
                r[j].move_to([x + widths[j] / 2, -k * (0.5 + row_gap), 0])
                x += widths[j] + (col_gap if j != 1 and j != 2 else col_gap * 0.6)
        self.add(rows)
        self.rows = rows
        self.hl = SurroundingRectangle(self.rule_rows[0], color=C.CS_HEAD, buff=0.08, corner_radius=0.08,
                                       stroke_width=2.5).set_fill(C.CS_HEAD, opacity=0.08)
        self.hl.set_opacity(0)
        self.add(self.hl)
        self.lit = None

    def light(self, i: int | None, run_time=0.3) -> Animation:
        if i is None:
            self.lit = None
            return self.hl.animate(run_time=run_time).set_stroke(opacity=0).set_fill(opacity=0)
        target = SurroundingRectangle(self.rule_rows[i], color=C.CS_HEAD, buff=0.08, corner_radius=0.08,
                                      stroke_width=2.5).set_fill(C.CS_HEAD, opacity=0.08)
        first = self.lit is None
        self.lit = i
        if first:
            self.hl.become(target).set_stroke(opacity=0).set_fill(opacity=0)
            return self.hl.animate(run_time=run_time).set_stroke(opacity=1).set_fill(opacity=0.08)
        return Transform(self.hl, target, run_time=run_time)


# ---------------------------------------------------------------------------
# Images of arrays
# ---------------------------------------------------------------------------
def hex_rgb(c) -> np.ndarray:
    return (np.array(ManimColor(c).to_rgb()) * 255).astype(np.uint8)


def bitmap(arr, palette=None, width=None, height=None, smooth=False) -> ImageMobject:
    """An array as a crisp image.  ``arr`` is either (h, w) of small integers, mapped through ``palette`` (a list of
    colours, index = value), or (h, w, 3) RGB in 0-255 or 0-1.  Nearest-neighbour scaling unless ``smooth``."""
    a = np.asarray(arr)
    if a.ndim == 2:
        pal = np.array([hex_rgb(c) for c in (palette or [BACKGROUND, WHITE])], np.uint8)
        rgb = pal[np.clip(a.astype(int), 0, len(pal) - 1)]
    else:
        rgb = a.astype(float)
        if rgb.max() <= 1.0:
            rgb = rgb * 255
        rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    if width is not None and height is not None:
        img.stretch_to_fit_width(width)
        img.stretch_to_fit_height(height)
    elif width is not None:
        img.scale_to_fit_width(width)
    elif height is not None:
        img.scale_to_fit_height(height)
    return img
