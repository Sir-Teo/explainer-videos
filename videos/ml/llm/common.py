"""Helpers shared by the LLM scenes: tokens, vectors, bars, attention grids, blocks."""

from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403

from .analyze import PROMPT, TARGET, load, load_arrays  # noqa: F401

MONO = "DejaVu Sans Mono"
SPACE_MARK = "␣"  # ␣, shown where a token starts with a space
NEWLINE_MARK = "↵"  # ↵


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    return Tex(text, color=color, font_size=font_size, **kw)


def caption_box(mob: Mobject, color=WHITE, buff=0.18) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=2)


def data() -> dict:
    return load("gpt2_small")


# ---------------------------------------------------------------------------
# Text in a monospace font with a consistent baseline
# ---------------------------------------------------------------------------
def display_token(s: str, show_space: bool = False) -> str:
    s = s.replace("\n", NEWLINE_MARK)
    if s.startswith(" "):
        s = (SPACE_MARK if show_space else "") + s[1:]
    return s if s.strip() else SPACE_MARK


class Mono(VGroup):
    """Monospace text whose vertical extent always includes ascenders and
    descenders, so rows of words line up on one baseline.  ``self.glyphs`` are
    the visible characters; the bounding box is that of the full line."""

    def __init__(self, s: str, font_size=28, color=WHITE, space_color=GREY_D, **kw):
        strut = "Ég"  # tall + descending glyphs
        t = Text(strut + s, font=MONO, font_size=font_size, color=color, **kw)
        struts, glyphs = t[:2], t[2:]
        if len(glyphs):
            x0, x1 = glyphs.get_left()[0], glyphs.get_right()[0]
        else:
            x0 = struts.get_right()[0]
            x1 = x0 + 0.2
        # Invisible corners (unaffected by set_opacity) fix the line's bounding box.
        frame = VGroup(VectorizedPoint([x0, struts.get_top()[1], 0]), VectorizedPoint([x1, struts.get_bottom()[1], 0]))
        for i, ch in enumerate(c for c in s if not c.isspace()):
            if ch in (SPACE_MARK, NEWLINE_MARK) and i < len(glyphs):
                glyphs[i].set_color(space_color)
        super().__init__(frame, *glyphs)
        self.frame = frame
        self.glyphs = VGroup(*glyphs)


class TokenBox(VGroup):
    def __init__(self, s: str, color=C.TOKEN, font_size=28, show_space=False, fill_opacity=0.12, pad=0.1,
                 text_color=WHITE, min_width=0.0):
        txt = Mono(display_token(s, show_space), font_size=font_size, color=text_color)
        w = max(txt.width + 2 * pad, min_width, txt.frame.height * 0.9)
        box = RoundedRectangle(width=w, height=txt.frame.height + 1.2 * pad, corner_radius=0.07,
                               stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill_opacity)
        txt.move_to(box)
        super().__init__(box, txt)
        self.box, self.text, self.token = box, txt, s


def token_row(pieces, buff=0.08, **kw) -> VGroup:
    row = VGroup(*[TokenBox(p, **kw) for p in pieces])
    row.arrange(RIGHT, buff=buff)
    return row


def text_line(s: str, font_size=30, color=WHITE) -> Mono:
    return Mono(s, font_size=font_size, color=color)


def wrap_text(s: str, width=56, font_size=24, color=WHITE, max_lines=3, line_buff=0.14) -> VGroup:
    """Monospace paragraph, wrapped at ``width`` characters; newlines shown as ↵."""
    import textwrap

    s = " ".join(s.replace("\n", f" {NEWLINE_MARK} ").split())
    lines = textwrap.wrap(s, width)[:max_lines]
    return VGroup(*[Mono(ln, font_size=font_size, color=color) for ln in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=line_buff)


def piece_text(pieces, font_size=28, color=WHITE) -> Mono:
    """The concatenated text set as one line; ``.pieces[i]`` holds the glyphs of
    token i, so tokens can be revealed or highlighted one at a time in place."""
    line = Mono("".join(pieces).replace("\n", " "), font_size=font_size, color=color)
    groups, k = VGroup(), 0
    for p in pieces:
        n = sum(1 for ch in p if not ch.isspace())
        groups.add(VGroup(*line.glyphs[k:k + n]))
        k += n
    line.pieces = groups
    return line


# ---------------------------------------------------------------------------
# Vectors
# ---------------------------------------------------------------------------
def vector_strip(values, color=C.EMBED, cell=0.2, gap=0.035, vmax=None, outline=True) -> VGroup:
    """A column of cells whose brightness follows |value| (sign shown by tint)."""
    values = np.asarray(values, dtype=float)
    vmax = vmax or (np.abs(values).max() + 1e-9)
    cells = VGroup()
    for v in values:
        a = min(1.0, abs(v) / vmax)
        col = color if v >= 0 else interpolate_color(ManimColor(color), ManimColor(BACKGROUND), 0.45)
        sq = Square(cell, stroke_width=0, fill_color=col, fill_opacity=0.12 + 0.88 * a)
        cells.add(sq)
    cells.arrange(DOWN, buff=gap)
    group = VGroup(cells)
    if outline:
        group.add(SurroundingRectangle(cells, buff=0.04, color=color, stroke_width=1.5, corner_radius=0.04))
    group.cells = cells
    return group


def random_values(n, seed=0, scale=1.0) -> np.ndarray:
    return np.random.default_rng(seed).normal(0, scale, n)


def num_column(values, color=WHITE, font_size=28, decimals=2, dots=True, bracket_color=GREY_B) -> VGroup:
    """3b1b-style column vector of numbers in square brackets."""
    entries = VGroup(*[DecimalNumber(v, num_decimal_places=decimals, include_sign=True, font_size=font_size, color=color)
                       for v in values])
    if dots:
        entries.add(MathTex(r"\vdots", font_size=font_size, color=color))
    entries.arrange(DOWN, buff=0.16)
    for e in entries[:len(values)]:
        e.align_to(entries[0], RIGHT)
    h = entries.height + 0.25
    lb = MathTex(r"\left[\vphantom{\rule{1pt}{%.2fcm}}\right." % (h * 0.9), color=bracket_color)
    rb = MathTex(r"\left.\vphantom{\rule{1pt}{%.2fcm}}\right]" % (h * 0.9), color=bracket_color)
    lb.stretch_to_fit_height(h).next_to(entries, LEFT, buff=0.1)
    rb.stretch_to_fit_height(h).next_to(entries, RIGHT, buff=0.1)
    g = VGroup(lb, entries, rb)
    g.entries = entries
    return g


def cell_matrix(rows, cols, color, cell=0.16, gap=0.025, seed=0, label_tex=None, font_size=34) -> VGroup:
    """A weight matrix drawn as a grid of cells (values are illustrative)."""
    rng = np.random.default_rng(seed)
    grid = VGroup()
    for _ in range(rows):
        for _ in range(cols):
            a = abs(rng.normal(0, 0.45))
            grid.add(Square(cell, stroke_width=0, fill_color=color, fill_opacity=min(0.95, 0.1 + a)))
    grid.arrange_in_grid(rows, cols, buff=gap)
    frame = SurroundingRectangle(grid, buff=0.05, color=color, stroke_width=2, corner_radius=0.04)
    g = VGroup(grid, frame)
    if label_tex:
        lab = MathTex(label_tex, font_size=font_size, color=color).next_to(frame, UP, buff=0.12)
        g.add(lab)
        g.label = lab
    g.grid, g.frame = grid, frame
    return g


# ---------------------------------------------------------------------------
# Probability bars
# ---------------------------------------------------------------------------
class ProbBars(VGroup):
    """Horizontal bars: token label | bar | percentage.  ``set_probs`` updates
    bars and numbers in place (fast enough for updaters)."""

    def __init__(self, tokens, probs, max_width=4.0, scale_max=None, bar_height=0.32, gap=0.12, color=C.PROB,
                 font_size=26, show_pct=True, highlight=None, highlight_color=YELLOW, decimals=1, percent=True):
        super().__init__()
        self.max_width = max_width
        self.percent = percent
        self.scale_max = scale_max or max(max(probs), 1e-9)
        self.labels, self.bars, self.pcts = VGroup(), VGroup(), VGroup()
        rows = VGroup()
        for t in tokens:
            lab = Mono(display_token(t), font_size=font_size)
            rows.add(lab)
        rows.arrange(DOWN, buff=gap, aligned_edge=RIGHT)
        step = max(bar_height + gap, rows[0].height + gap) if len(rows) else 0
        for i, lab in enumerate(rows):
            lab.move_to([0, -i * step, 0], aligned_edge=RIGHT)
        self.x0 = rows.get_right()[0] + 0.2 if len(rows) else 0
        for i, (lab, p) in enumerate(zip(rows, probs)):
            y = lab.get_center()[1]
            col = highlight_color if highlight is not None and tokens[i] == highlight else color
            bar = Rectangle(width=1.0, height=bar_height, stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to([self.x0, y, 0], aligned_edge=LEFT)
            self.bars.add(bar)
            if percent:
                pct = DecimalNumber(100 * p, num_decimal_places=decimals, unit=r"\%", font_size=font_size * 0.9, color=GREY_A)
            else:
                pct = DecimalNumber(p, num_decimal_places=decimals, font_size=font_size * 0.9, color=GREY_A)
            self.pcts.add(pct)
            if col != color:
                lab.set_color(highlight_color)
        self.labels = rows
        self.add(self.labels, self.bars)
        if show_pct:
            self.add(self.pcts)
        self.show_pct = show_pct
        self.set_probs(probs)

    def set_probs(self, probs):
        for bar, pct, p in zip(self.bars, self.pcts, probs):
            w = max(1e-3, self.max_width * p / self.scale_max)
            y = bar.get_center()[1]
            bar.stretch_to_fit_width(w)
            bar.move_to([self.x0, y, 0], aligned_edge=LEFT)
            pct.set_value(100 * p if self.percent else p)
            pct.next_to(bar, RIGHT, buff=0.12)
        return self

    def row(self, i) -> VGroup:
        return VGroup(self.labels[i], self.bars[i], self.pcts[i])


def softmax(x, temperature=1.0) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64) / temperature
    e = np.exp(x - x.max())
    return e / e.sum()


# ---------------------------------------------------------------------------
# Attention patterns
# ---------------------------------------------------------------------------
def attention_grid(pattern, pieces, cell=0.42, color=C.ATTN, causal=True, font_size=22, gamma=0.7,
                   row_labels=True, col_labels=True) -> VGroup:
    """Rows = the token doing the looking (query), columns = tokens looked at (keys)."""
    W = np.asarray(pattern, dtype=float)
    n = len(pieces)
    cells = VGroup()
    for i in range(n):
        for j in range(n):
            if causal and j > i:
                sq = Square(cell * 0.92, stroke_width=0, fill_color=GREY_E, fill_opacity=0.35)
            else:
                a = float(np.clip(W[i, j], 0, 1)) ** gamma
                sq = Square(cell * 0.92, stroke_width=0, fill_color=color, fill_opacity=0.06 + 0.94 * a)
            sq.move_to([j * cell, -i * cell, 0])
            cells.add(sq)
    g = VGroup(cells)
    g.cells = cells
    g.n = n
    if row_labels:
        rl = VGroup(*[Mono(display_token(p), font_size=font_size) for p in pieces])
        for i, m in enumerate(rl):
            m.next_to(cells[i * n], LEFT, buff=0.15)
        g.add(rl)
        g.row_labels = rl
    if col_labels:
        cl = VGroup(*[Mono(display_token(p), font_size=font_size).rotate(PI / 2) for p in pieces])
        for j, m in enumerate(cl):
            m.next_to(cells[j], UP, buff=0.15)
        g.add(cl)
        g.col_labels = cl
    return g


def cell_at(grid: VGroup, i: int, j: int) -> Mobject:
    return grid.cells[i * grid.n + j]


def attention_arcs(row: VGroup, target: int, weights, color=C.ATTN, max_width=10, min_weight=0.02, above=True):
    """Arcs from every earlier token to ``target``, thickness and opacity ~ weight."""
    arcs = VGroup()
    direction = UP if above else DOWN
    for j, w in enumerate(weights):
        if j == target or w < min_weight:
            continue
        a = row[j].get_edge_center(direction) + 0.05 * direction
        b = row[target].get_edge_center(direction) + 0.05 * direction
        angle = -PI / 2.2 if above else PI / 2.2
        if j > target:
            angle = -angle
        arc = ArcBetweenPoints(a, b, angle=angle, color=color, stroke_width=1 + max_width * w)
        arc.set_stroke(opacity=0.25 + 0.75 * min(1, 2 * w))
        arcs.add(arc)
    return arcs


# ---------------------------------------------------------------------------
# Architecture diagrams
# ---------------------------------------------------------------------------
def block(text: str, color, width=2.8, height=0.85, font_size=32, fill_opacity=0.18) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=fill_opacity)
    lab = label(text, color=WHITE, font_size=font_size).move_to(box)
    g = VGroup(box, lab)
    g.box, g.text = box, lab
    return g


def chapter_card(number: int, text: str) -> VGroup:
    num = Tex(f"Chapter {number}", font_size=32, color=C.DIM)
    title = Tex(text, font_size=60)
    return VGroup(num, title).arrange(DOWN, buff=0.25)


def show_chapter_card(scene: Scene, number: int, text: str, hold: float = 1.2):
    card = chapter_card(number, text)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
    scene.wait(hold)
    scene.play(FadeOut(card, shift=UP * 0.2), run_time=0.6)


class Plot(VGroup):
    """Axes drawn along the bottom and left edges of a box (unlike ``Axes``, the
    x-axis stays at the bottom even when the data goes negative)."""

    def __init__(self, x_range, y_range, width=9.0, height=4.6, x_ticks=(), y_ticks=(), x_fmt=str, y_fmt=None,
                 font_size=26, color=GREY_B, log_x=False, log_y=False):
        super().__init__()
        self.x_range, self.y_range, self.w, self.h = x_range, y_range, width, height
        self.log_x, self.log_y = log_x, log_y
        y_fmt = y_fmt or (lambda v: f"{v:g}")
        x_axis = Line(ORIGIN, RIGHT * width, color=color, stroke_width=2)
        y_axis = Line(ORIGIN, UP * height, color=color, stroke_width=2)
        self.add(x_axis, y_axis)
        self.x_axis, self.y_axis = x_axis, y_axis
        self.x_labels, self.y_labels = VGroup(), VGroup()
        for t in x_ticks:
            p = self.c2p(t, y_range[0])
            self.add(Line(p, p + DOWN * 0.08, color=color, stroke_width=2))
            lab = x_fmt(t)
            m = (lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=GREY_A))
            m.next_to(p, DOWN, buff=0.15)
            self.x_labels.add(m)
        for t in y_ticks:
            p = self.c2p(x_range[0], t)
            self.add(Line(p, p + LEFT * 0.08, color=color, stroke_width=2))
            lab = y_fmt(t)
            m = (lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=GREY_A))
            m.next_to(p, LEFT, buff=0.15)
            self.y_labels.add(m)
        self.add(self.x_labels, self.y_labels)

    def _t(self, v, rng, log):
        lo, hi = rng
        if log:
            v, lo, hi = np.log10(v), np.log10(lo), np.log10(hi)
        return (v - lo) / (hi - lo)

    def c2p(self, x, y):
        o = self.x_axis.get_start()
        return o + RIGHT * self.w * self._t(x, self.x_range, self.log_x) + UP * self.h * self._t(y, self.y_range, self.log_y)

    def line(self, xs, ys, color, stroke_width=4) -> VMobject:
        return VMobject().set_points_as_corners([self.c2p(x, y) for x, y in zip(xs, ys)]).set_stroke(color, stroke_width)

    def dots(self, xs, ys, color, radius=0.06) -> VGroup:
        return VGroup(*[Dot(self.c2p(x, y), radius=radius, color=color) for x, y in zip(xs, ys)])


def fmt_int(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")
