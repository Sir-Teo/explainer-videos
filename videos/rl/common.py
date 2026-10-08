"""Helpers shared by the reinforcement-learning scenes: text, plots, token strips, the probability simplex,
and the answer tree (every answer the model might give, as a river of probability)."""

from __future__ import annotations

import math
import textwrap

import numpy as np

from explainer import *  # noqa: F403

from .compute import ANS_MAX, ND, load  # noqa: F401

# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
WIDE_TEX = TEX_TEMPLATE.copy()
WIDE_TEX.add_to_preamble(r"\setlength{\textwidth}{40cm}")
MAX_TEXT_WIDTH = 13.6
MONO = "DejaVu Sans Mono"


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    """A Tex label that never wraps on its own (line breaks are explicit) and shrinks to fit the frame."""
    kw.setdefault("tex_template", WIDE_TEX)
    t = Tex(text, color=color, font_size=font_size, **kw)
    if t.width > MAX_TEXT_WIDTH:
        t.width = MAX_TEXT_WIDTH
    return t


def mtex(*tex: str, color=WHITE, font_size=36, **kw) -> MathTex:
    return MathTex(*tex, color=color, font_size=font_size, **kw)


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    return label(text, font_size=font_size, color=color)


def schematic_tag(corner=DL) -> Tex:
    return note(r"schematic").to_corner(corner, buff=0.3)


def real_tag(text: str = r"real run, on this computer", corner=DL) -> Tex:
    return note(text, color=GREY_A).to_corner(corner, buff=0.25)


def exact_tag(text: str = r"exact computation", corner=DL) -> Tex:
    return note(text, color=GREY_A).to_corner(corner, buff=0.3)


def source(text: str, font_size=20) -> Tex:
    return label(r"Source: " + text, font_size=font_size, color=GREY_B).to_corner(DR, buff=0.25)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def boxed(mob: Mobject, color=YELLOW, buff=0.25, fill=0.0) -> VGroup:
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12, stroke_width=2.5)
    if fill:
        box.set_fill(color, opacity=fill)
    return VGroup(box, mob)


def chip(text: str, color=GREY_B, font_size=22, fill=0.18) -> VGroup:
    t = label(text, font_size=font_size)
    box = RoundedRectangle(width=t.width + 0.25, height=t.height + 0.16, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.5, fill_color=color, fill_opacity=fill)
    t.move_to(box)
    return VGroup(box, t)


def part_card(number: int, title: str, subtitle: str = "") -> VGroup:
    num = label(rf"Part {number}", font_size=34, color=C.DIM)
    t = label(title, font_size=60)
    g = VGroup(num, t)
    if subtitle:
        g.add(label(subtitle, font_size=32, color=GREY_A))
    return g.arrange(DOWN, buff=0.3)


def why(text: str, color=GREY_A, font_size=26) -> Tex:
    """The small grey justification that sits beside a derivation step."""
    return label(text, color=color, font_size=font_size)


def fmt_int(n) -> str:
    """12345678 -> '12{,}345{,}678' for TeX."""
    return f"{int(n):,}".replace(",", "{,}")


def sci(x: float, digits: int = 1) -> str:
    """3.8e25 -> '3.8\\times10^{25}' (TeX)."""
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10**e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    ms = f"{m:.{digits}f}".rstrip("0").rstrip(".")
    return rf"10^{{{e}}}" if ms == "1" else rf"{ms}\times10^{{{e}}}"


def pct(x: float, digits: int = 0) -> str:
    return f"{100 * x:.{digits}f}" + r"\%"


# ---------------------------------------------------------------------------
# Monospace text (baseline-consistent)
# ---------------------------------------------------------------------------
class Mono(VGroup):
    """Monospace text whose bounding box always includes ascenders and descenders, so rows line up.
    ``self.glyphs`` are the visible characters."""

    def __init__(self, s: str, font_size=24, color=WHITE, **kw):
        strut = "Ég"
        t = Text(strut + s, font=MONO, font_size=font_size, color=color, **kw)
        struts, glyphs = t[:2], t[2:]
        if len(glyphs):
            x0, x1 = glyphs.get_left()[0], glyphs.get_right()[0]
        else:
            x0 = struts.get_right()[0]
            x1 = x0 + 0.2
        frame = VGroup(VectorizedPoint([x0, struts.get_top()[1], 0]), VectorizedPoint([x1, struts.get_bottom()[1], 0]))
        super().__init__(frame, *glyphs)
        self.frame = frame
        self.glyphs = VGroup(*glyphs)


def mono_lines(text: str, width: int = 60, max_lines: int = 8, font_size=18, color=WHITE, line_buff=0.08) -> VGroup:
    lines: list[str] = []
    for para in text.split("\n"):
        para = " ".join(para.split())
        if not para:
            continue
        lines += textwrap.wrap(para, width) or [""]
    lines = lines[:max_lines]
    g = VGroup(*[Mono(ln, font_size=font_size, color=color) for ln in lines])
    return g.arrange(DOWN, aligned_edge=LEFT, buff=line_buff)


# ---------------------------------------------------------------------------
# Token strips for the addition task
# ---------------------------------------------------------------------------
def token_color(ch: str, pos_in_answer: int | None, think: bool) -> str:
    """Prompt tokens grey; work tokens (">", the reversed digits, "|") light blue; answer digits white."""
    if pos_in_answer is None:
        return C.PROMPT_TOK
    if think and pos_in_answer <= ND + 2:
        return C.WORK_TOK
    if ch == ".":
        return GREY_B
    return WHITE


def tokens(prompt: str, answer: str = "", font_size=30, cell=0.42, height=0.56, buff=0.04, frame=True,
           answer_color=None) -> VGroup:
    """A row of token cells.  ``.cells[i]`` = VGroup(box, glyph).  The answer's "think" part is colored."""
    think = answer.startswith(">")
    cells = VGroup()
    for i, ch in enumerate(prompt + answer):
        pa = None if i < len(prompt) else i - len(prompt)
        col = token_color(ch, pa, think)
        if answer_color is not None and pa is not None and not (think and pa <= ND + 2):
            col = answer_color
        g = Mono("→" if ch == ">" else ch, font_size=font_size, color=col)
        box = Rectangle(width=cell, height=height, stroke_width=1.2 if frame else 0, stroke_color=GREY_D,
                        fill_color=col, fill_opacity=0.08 if frame else 0)
        g.move_to(box)
        cells.add(VGroup(box, g))
    cells.arrange(RIGHT, buff=buff)
    cells.cells = cells
    return cells


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
class Plot(VGroup):
    """Axes along the bottom and left edges of a box, with optional log scales; ``c2p(x, y)``."""

    def __init__(self, x_range, y_range, width=9.0, height=4.6, x_ticks=(), y_ticks=(), x_fmt=None, y_fmt=None,
                 font_size=24, color=GREY_B, log_x=False, log_y=False, x_label=None, y_label=None,
                 label_color=GREY_A):
        super().__init__()
        self.x_range, self.y_range, self.w, self.h = x_range, y_range, width, height
        self.log_x, self.log_y = log_x, log_y
        x_fmt = x_fmt or (lambda v: f"{v:g}")
        y_fmt = y_fmt or (lambda v: f"{v:g}")
        self.x_axis = Line(ORIGIN, RIGHT * width, color=color, stroke_width=2)
        self.y_axis = Line(ORIGIN, UP * height, color=color, stroke_width=2)
        self.add(self.x_axis, self.y_axis)
        self.x_labels, self.y_labels = VGroup(), VGroup()
        for t in x_ticks:
            p = self.c2p(t, y_range[0])
            self.add(Line(p, p + DOWN * 0.08, color=color, stroke_width=2))
            lab = x_fmt(t)
            m = lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=GREY_A)
            self.x_labels.add(m.next_to(p, DOWN, buff=0.14))
        for t in y_ticks:
            p = self.c2p(x_range[0], t)
            self.add(Line(p, p + LEFT * 0.08, color=color, stroke_width=2))
            lab = y_fmt(t)
            m = lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=GREY_A)
            self.y_labels.add(m.next_to(p, LEFT, buff=0.14))
        self.add(self.x_labels, self.y_labels)
        if x_label is not None:
            xl = x_label if isinstance(x_label, Mobject) else label(x_label, font_size=font_size + 2, color=label_color)
            xl.next_to(self.x_labels if len(self.x_labels) else self.x_axis, DOWN, buff=0.18)
            xl.set_x(self.x_axis.get_center()[0])
            self.add(xl)
            self.x_title = xl
        if y_label is not None:
            yl = y_label if isinstance(y_label, Mobject) else label(y_label, font_size=font_size + 2, color=label_color)
            yl.next_to(self.y_axis, UP, buff=0.18).align_to(self.y_axis, LEFT).shift(LEFT * 0.3)
            self.add(yl)
            self.y_title = yl

    def _t(self, v, rng, log):
        lo, hi = rng
        if log:
            v, lo, hi = np.log10(v), np.log10(lo), np.log10(hi)
        return (v - lo) / (hi - lo)

    def c2p(self, x, y):
        o = self.x_axis.get_start()
        return o + RIGHT * self.w * self._t(x, self.x_range, self.log_x) + UP * self.h * self._t(y, self.y_range, self.log_y)

    def line(self, xs, ys, color, stroke_width=3.5, **kw) -> VMobject:
        pts = [self.c2p(x, y) for x, y in zip(xs, ys)]
        return VMobject(**kw).set_points_as_corners(pts).set_stroke(color, stroke_width)

    def smooth_line(self, xs, ys, color, stroke_width=3.5) -> VMobject:
        pts = [self.c2p(x, y) for x, y in zip(xs, ys)]
        return VMobject().set_points_smoothly(pts).set_stroke(color, stroke_width)

    def dots(self, xs, ys, color, radius=0.06) -> VGroup:
        return VGroup(*[Dot(self.c2p(x, y), radius=radius, color=color) for x, y in zip(xs, ys)])

    def area(self, xs, ys, color, opacity=0.35, y0=None) -> Polygon:
        y0 = self.y_range[0] if y0 is None else y0
        pts = [self.c2p(xs[0], y0)] + [self.c2p(x, y) for x, y in zip(xs, ys)] + [self.c2p(xs[-1], y0)]
        return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)

    def hline(self, y, color=GREY_C, **kw) -> DashedLine:
        return DashedLine(self.c2p(self.x_range[0], y), self.c2p(self.x_range[1], y), color=color, **kw)

    def vline(self, x, color=GREY_C, **kw) -> DashedLine:
        return DashedLine(self.c2p(x, self.y_range[0]), self.c2p(x, self.y_range[1]), color=color, **kw)


def pct_fmt(v) -> MathTex:
    return MathTex(rf"{int(round(100 * v))}\%", font_size=24, color=GREY_A)


def smooth(y, k: int = 5) -> np.ndarray:
    """Centered moving average (edges use the available window)."""
    y = np.asarray(y, float)
    if k <= 1:
        return y
    out = np.empty_like(y)
    h = k // 2
    for i in range(len(y)):
        out[i] = y[max(0, i - h):i + h + 1].mean()
    out[0], out[-1] = y[0], y[-1]  # keep the endpoints exact: a chart must start where the data starts
    return out


def histogram(plot: Plot, values, bins, color, opacity=0.75, density=True, scale=1.0) -> VGroup:
    """Bars of a histogram on ``plot`` (bins = edges)."""
    h, edges = np.histogram(values, bins=bins, density=density)
    g = VGroup()
    for lo, hi, v in zip(edges[:-1], edges[1:], h * scale):
        if v <= 0:
            continue
        v = min(v, plot.y_range[1])
        a, b = plot.c2p(lo, plot.y_range[0]), plot.c2p(hi, v)
        r = Rectangle(width=max(1e-3, b[0] - a[0]), height=max(1e-3, b[1] - a[1]), stroke_width=0, fill_color=color,
                      fill_opacity=opacity)
        r.move_to((a + b) / 2)
        g.add(r)
    return g


def bar_rows(items, scale: float, font_size=26, bar_h=0.36, buff=0.18, name_color=GREY_A, value_color=WHITE,
             opacity=0.85) -> VGroup:
    """Horizontal bar chart rows.  items = [(name TeX, value, color, value TeX)]; bar length = value * scale."""
    names = [label(n, font_size=font_size, color=name_color) for n, *_ in items]
    w = max(n.width for n in names)
    rows = VGroup()
    for i, ((_, v, col, vt), nm) in enumerate(zip(items, names)):
        y = -i * (bar_h + buff)
        nm.move_to([w, y, 0], aligned_edge=RIGHT)
        b = Rectangle(width=max(0.03, v * scale), height=bar_h, stroke_width=0, fill_color=col, fill_opacity=opacity)
        b.move_to([w + 0.25, y, 0], aligned_edge=LEFT)
        t = label(vt, font_size=font_size - 2, color=value_color).next_to(b, RIGHT, buff=0.12)
        rows.add(VGroup(nm, b, t))
    return rows


# ---------------------------------------------------------------------------
# The probability simplex of a 3-action softmax policy
# ---------------------------------------------------------------------------
ACTION_NAMES = ("A", "B", "C")


class Simplex(VGroup):
    """An equilateral triangle whose points are probability vectors (pi_A, pi_B, pi_C).
    Vertex A at the top, B bottom-left, C bottom-right.  ``p2s(pi)`` maps a distribution to a point."""

    def __init__(self, side=5.2, rewards=None, color=GREY_B, font_size=30, fill=True):
        super().__init__()
        h = side * math.sqrt(3) / 2
        self.V = np.array([[0, 2 * h / 3, 0], [-side / 2, -h / 3, 0], [side / 2, -h / 3, 0]])
        self.tri = Polygon(*self.V, stroke_color=color, stroke_width=2.5,
                           fill_color=GREY_E, fill_opacity=0.35 if fill else 0)
        self.add(self.tri)
        self.vlabels = VGroup()
        dirs = [UP, DL, DR]
        for i, (nm, d) in enumerate(zip(ACTION_NAMES, dirs)):
            t = label(rf"\textbf{{{nm}}}", font_size=font_size)
            if rewards is not None:
                r = rewards[i]
                t = VGroup(t, MathTex(rf"r={r:g}", font_size=font_size - 6,
                                      color=C.REWARD if r > 0.5 else (GREY_A if r > 0 else C.PENALTY)))
                t.arrange(DOWN if i == 0 else DOWN, buff=0.08)
                if i == 0:
                    t.arrange(RIGHT, buff=0.2)
            t.next_to(self.V[i], d, buff=0.15)
            self.vlabels.add(t)
        self.add(self.vlabels)

    def p2s(self, pi) -> np.ndarray:
        """Barycentric map, using the triangle's current corners (so it follows moves and scaling)."""
        pi = np.asarray(pi, float)
        v = self.tri.get_vertices()
        return pi[0] * v[0] + pi[1] * v[1] + pi[2] * v[2]

    def path(self, pis, color, stroke_width=3.5, smooth_=False) -> VMobject:
        pts = [self.p2s(p) for p in pis]
        m = VMobject()
        if smooth_:
            m.set_points_smoothly(pts)
        else:
            m.set_points_as_corners(pts)
        return m.set_stroke(color, stroke_width)

    def iso_lines(self, r, levels, color=C.REWARD, stroke_width=1.5, opacity=0.5) -> VGroup:
        """Lines of constant expected reward J = pi . r (straight lines across the triangle)."""
        g = VGroup()
        for J in levels:
            pts = []
            for i, j in ((0, 1), (1, 2), (0, 2)):
                # points on edge i-j: pi = t e_i + (1-t) e_j, J = t r_i + (1-t) r_j
                if abs(r[i] - r[j]) < 1e-12:
                    continue
                t = (J - r[j]) / (r[i] - r[j])
                if -1e-9 <= t <= 1 + 1e-9:
                    pi = np.zeros(3)
                    pi[i], pi[j] = t, 1 - t
                    pts.append(self.p2s(pi))
            if len(pts) >= 2:
                g.add(Line(pts[0], pts[1], stroke_width=stroke_width, color=color, stroke_opacity=opacity))
        return g


# ---------------------------------------------------------------------------
# The answer tree: every answer to one prompt, as a river of probability flowing left to right
# ---------------------------------------------------------------------------
class AnswerTree(VGroup):
    """Column t holds the t-th answer token; each prefix is a block whose height is its probability.
    Build once from the *union* of answers over several checkpoints (``all_texts``) so trees at different
    training steps have the same blocks and can be morphed into each other with ``Transform``.

    ``.blocks[prefix]`` = the block (rectangle) of that prefix; ``.leaf_bars`` = the reward column."""

    def __init__(self, leaves: list[dict], all_texts: list[str], height=5.6, col_w=0.62, gap=0.02,
                 font_size=20, min_label=0.10, show_labels=True, reward_col=True):
        super().__init__()
        p = {L["text"]: L["p"] for L in leaves}
        r = {L["text"]: L["r"] for L in leaves}
        texts = list(all_texts)
        total = sum(p.get(t, 0.0) for t in texts) or 1.0
        self.height, self.col_w = height, col_w
        self.blocks, self.glyphs = {}, {}
        rects, glyphs = VGroup(), VGroup()
        prefixes = []
        seen = set()
        for t in texts:
            for k in range(1, len(t) + 1):
                if t[:k] not in seen:
                    seen.add(t[:k])
                    prefixes.append(t[:k])
        # probability of each prefix, and its vertical interval (children stacked in the order of all_texts)
        mass = {q: 0.0 for q in prefixes}
        for t in texts:
            for k in range(1, len(t) + 1):
                mass[t[:k]] += p.get(t, 0.0) / total
        top = {}
        cursor = {}
        for q in prefixes:
            parent = q[:-1]
            start = cursor.get(parent, top.get(parent, 0.0)) if parent else cursor.get("", 0.0)
            top[q] = start
            if parent:
                cursor[parent] = start + mass[q]
            else:
                cursor[""] = start + mass[q]
        for q in prefixes:
            k = len(q) - 1
            y0 = height / 2 - top[q] * height
            h = mass[q] * height
            think = q.startswith(">")
            col = token_color(q[-1], k, think)
            rect = Rectangle(width=col_w - gap, height=max(h - gap, 1e-4), stroke_width=0, fill_color=col,
                             fill_opacity=0.32 if h > 1e-3 else 0.0)
            rect.move_to([k * col_w + col_w / 2, y0 - h / 2, 0])
            rects.add(rect)
            self.blocks[q] = rect
            ch = "→" if q[-1] == ">" else q[-1]
            g = Mono(ch, font_size=font_size, color=col).move_to(rect)
            if not show_labels or mass[q] < min_label:
                g.set_opacity(0)
            glyphs.add(g)
            self.glyphs[q] = g
        self.rects, self.glyph_group = rects, glyphs
        self.add(rects, glyphs)
        self.leaf_bars = VGroup()
        if reward_col:
            x = (ANS_MAX + 0.4) * col_w
            cum = 0.0
            for t in texts:
                m = p.get(t, 0.0) / total
                y0 = height / 2 - cum * height
                bar = Rectangle(width=0.32, height=max(m * height - gap, 1e-4), stroke_width=0,
                                fill_color=C.REWARD if r.get(t, 0) > 0 else C.PENALTY,
                                fill_opacity=0.9 if m > 1e-3 else 0.0)
                bar.move_to([x, y0 - m * height / 2, 0])
                self.leaf_bars.add(bar)
                cum += m
            self.add(self.leaf_bars)
        self.mass = mass
        self.p_correct = sum(p.get(t, 0.0) * r.get(t, 0.0) for t in texts) / total


def union_texts(trees: list[list[dict]], min_p: float = 2e-3) -> list[str]:
    """Answers that reach probability >= min_p in any tree, ordered think-first then by digits."""
    keep = set()
    for leaves in trees:
        for L in leaves:
            if L["p"] >= min_p:
                keep.add(L["text"])
    order = {c: (-1 if c == ">" else i) for i, c in enumerate("0123456789+=>|.")}
    return sorted(keep, key=lambda t: [order[c] for c in t])


# ---------------------------------------------------------------------------
# Loss anatomy: the full GRPO objective, built so every piece can be lit up separately
# ---------------------------------------------------------------------------
def grpo_objective(font_size=34) -> MathTex:
    """J_GRPO with the pieces as separate submobjects:
    0 J =, 1 E over q and the group, 2 1/G sum, 3 1/|o| sum, 4 min(, 5 ratio, 6 A, 7 , clip(ratio), 8 A, 9 ),
    10 - beta KL, 11 ]"""
    m = MathTex(
        r"\mathcal{J}(\theta) = ",
        r"\mathbb{E}_{q,\;\{o_i\}_{i=1}^{G} \sim \pi_{\theta_{\text{old}}}}\Big[",
        r"\frac{1}{G}\sum_{i=1}^{G}",
        r"\frac{1}{|o_i|}\sum_{t=1}^{|o_i|}",
        r"\min\!\Big(",
        r"\frac{\pi_\theta(o_{i,t}\mid q, o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t}\mid q, o_{i,<t})}",
        r"\hat A_{i,t}",
        r",\ \operatorname{clip}\!\big(\rho_{i,t},\,1-\varepsilon,\,1+\varepsilon\big)",
        r"\hat A_{i,t}",
        r"\Big)",
        r"- \beta\, \mathbb{D}_{\mathrm{KL}}\!\big[\pi_\theta \,\|\, \pi_{\text{ref}}\big]",
        r"\Big]",
        font_size=font_size,
    )
    return m


def color_grpo(m: MathTex) -> MathTex:
    m[5].set_color(C.RATIO)
    m[6].set_color(C.ADVANTAGE)
    m[7].set_color(C.RATIO)
    m[8].set_color(C.ADVANTAGE)
    m[10].set_color(C.KL)
    m[3].set_color(C.LENGTH)
    m[2].set_color(C.BASELINE)
    m[1].set_color(C.OLD_POLICY)
    return m
