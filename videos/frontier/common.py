"""Helpers shared by the frontier-training scenes: text, plots, web-page cards, GPUs, the pipeline map."""

from __future__ import annotations

import math
import textwrap

import numpy as np

from explainer import *  # noqa: F403

from .compute import load  # noqa: F401

# ---------------------------------------------------------------------------
# Facts quoted on screen (sources: videos/frontier/README.md).  Numbers that can be recomputed from
# cached data are asserted against it where they are used.
# ---------------------------------------------------------------------------
CRAWL = dict(id="CC-MAIN-2026-39", name="September 2026", pages_b=2.17, tib=105.92, files=100_000)
LLAMA3 = dict(params=405e9, tokens=15.6e12, flops=3.8e25, gpus=16_384, gpu_hours=30.84e6, mfu=(38, 43),
              interruptions=466, unexpected=419, days=54)
DSV3 = dict(total=671e9, active=37e9, tokens=14.8e12, gpu_hours=2.788e6, gpus=2048, experts=256, top_k=8)
KIMI_K2 = dict(total=1.04e12, active=32.6e9, tokens=15.5e12, experts=384, top_k=8)


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


def mtex(tex: str, color=WHITE, font_size=36, **kw) -> MathTex:
    return MathTex(tex, color=color, font_size=font_size, **kw)


def calc(*lines: str, font_size=36, color=WHITE) -> MathTex:
    """A worked calculation: one MathTex in an align* environment, one submobject per line, aligned at '&'.
    Lines after the first should start with r"\\" (a line break), e.g. calc(r"C &= 6ND", r"\\ &= 2.4\times10^{12}")."""
    return MathTex(*lines, font_size=font_size, color=color)


def num_table(header: list[str], rows: list[list[str]], font_size=30, col_colors=None, h_buff=0.55, v_buff=0.22):
    """A small table of MathTex cells: header row, a rule, then rows.  Returns a VGroup with .header, .rule,
    .rows (list of VGroups of cells) and .cols (list of VGroups, header included) for staged reveals."""
    cols = len(header)
    cells = [[MathTex(h, font_size=font_size, color=GREY_A) for h in header]]
    for r in rows:
        cells.append([MathTex(c, font_size=font_size, color=(col_colors[j] if col_colors else WHITE))
                      for j, c in enumerate(r)])
    widths = [max(cells[i][j].width for i in range(len(cells))) for j in range(cols)]
    xs = np.cumsum([0] + [w + h_buff for w in widths[:-1]])
    height = max(c.height for row in cells for c in row)
    grid = VGroup()
    for i, row in enumerate(cells):
        y = -i * (height + v_buff) - (0.15 if i else 0)
        for j, c in enumerate(row):
            c.move_to([xs[j] + widths[j] / 2, y, 0])
        grid.add(VGroup(*row))
    rule = Line([0, -(height + v_buff) / 2 - 0.05, 0], [xs[-1] + widths[-1], -(height + v_buff) / 2 - 0.05, 0],
                color=GREY_D, stroke_width=1.5)
    t = VGroup(grid, rule)
    t.header, t.rule, t.rows = grid[0], rule, list(grid[1:])
    t.cols = [VGroup(*[grid[i][j] for i in range(len(cells))]) for j in range(cols)]
    return t


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    return label(text, font_size=font_size, color=color)


def schematic_tag(corner=UR) -> Tex:
    return note(r"schematic").to_corner(corner, buff=0.3)


def real_tag(text: str = r"real run, on this computer", corner=UR) -> Tex:
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


def chip(text: str, color=GREY_B, font_size=22, fill=0.18, mono=False) -> VGroup:
    t = Mono(text, font_size=font_size, color=WHITE) if mono else label(text, font_size=font_size)
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


def human(x: float, unit: str = "") -> str:
    """1.5e12 -> '1.5T', 37e9 -> '37B' (plain text)."""
    for v, s in [(1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")]:
        if abs(x) >= v:
            q = x / v
            txt = f"{q:.1f}".rstrip("0").rstrip(".") if q < 100 else f"{q:.0f}"
            return txt + s + unit
    return f"{x:g}{unit}"


# ---------------------------------------------------------------------------
# Monospace text (baseline-consistent), web-page cards
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


def clean_line(s: str) -> str:
    """Printable single line for Text(): no control characters, tabs or exotic whitespace."""
    s = "".join(ch if ch.isprintable() else " " for ch in s.replace("\t", " "))
    return " ".join(s.split()) if s.strip() else ""


def mono_lines(text: str, width: int = 60, max_lines: int = 8, font_size=18, color=WHITE, line_buff=0.08,
               keep_newlines=True) -> VGroup:
    """A paragraph wrapped to ``width`` characters, as Mono lines."""
    lines: list[str] = []
    paras = text.split("\n") if keep_newlines else [text]
    for para in paras:
        para = clean_line(para)
        if not para:
            continue
        lines += textwrap.wrap(para, width) or [""]
        if len(lines) >= max_lines:
            break
    lines = lines[:max_lines]
    g = VGroup(*[Mono(ln, font_size=font_size, color=color) for ln in lines])
    return g.arrange(DOWN, aligned_edge=LEFT, buff=line_buff)


def page_card(text: str, url: str = "", width: float = 5.2, lines: int = 6, chars: int = 46, color=C.PAGE,
              font_size=16, url_chars: int = 44) -> VGroup:
    """A small browser-window card showing a page's URL and the first lines of its text."""
    body = mono_lines(text, width=chars, max_lines=lines, font_size=font_size, color=GREY_A)
    width = max(width, body.width + 0.4)
    h = body.height + 0.75
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2,
                             fill_color=BACKGROUND, fill_opacity=0.92)
    bar = Rectangle(width=width, height=0.32, stroke_width=0, fill_color=color, fill_opacity=0.25)
    bar.move_to(frame.get_top() + DOWN * 0.16)
    dots = VGroup(*[Dot(radius=0.04, color=c) for c in (RED_C, YELLOW_C, GREEN_C)]).arrange(RIGHT, buff=0.07)
    dots.move_to(bar.get_left() + RIGHT * 0.25)
    u = url.split("://")[-1]
    u = u if len(u) <= url_chars else u[:url_chars - 1] + "…"
    ut = Mono(u, font_size=13, color=GREY_B).next_to(dots, RIGHT, buff=0.15)
    body.next_to(bar, DOWN, buff=0.15).align_to(frame.get_left() + RIGHT * 0.18, LEFT)
    g = VGroup(frame, bar, dots, ut, body)
    g.frame, g.body, g.url = frame, body, ut
    return g


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

    def dots(self, xs, ys, color, radius=0.06) -> VGroup:
        return VGroup(*[Dot(self.c2p(x, y), radius=radius, color=color) for x, y in zip(xs, ys)])

    def hline(self, y, color=GREY_C, **kw) -> DashedLine:
        return DashedLine(self.c2p(self.x_range[0], y), self.c2p(self.x_range[1], y), color=color, **kw)

    def vline(self, x, color=GREY_C, **kw) -> DashedLine:
        return DashedLine(self.c2p(x, self.y_range[0]), self.c2p(x, self.y_range[1]), color=color, **kw)


def pow10_label(e: int, font_size=24) -> MathTex:
    return MathTex(rf"10^{{{e}}}", font_size=font_size, color=GREY_A)


def smooth(y, k: int = 5) -> np.ndarray:
    """Centered moving average (edges use the available window)."""
    y = np.asarray(y, float)
    if k <= 1:
        return y
    out = np.empty_like(y)
    h = k // 2
    for i in range(len(y)):
        out[i] = y[max(0, i - h):i + h + 1].mean()
    return out


# ---------------------------------------------------------------------------
# Hardware
# ---------------------------------------------------------------------------
def gpu(label_text: str = "GPU", width=1.3, height=0.9, color=C.GPU, font_size=22, fill=0.15) -> VGroup:
    body = RoundedRectangle(width=width, height=height, corner_radius=0.1, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=fill)
    pins = VGroup()
    for k in range(5):
        x = body.get_left()[0] + width * (k + 1) / 6
        pins.add(Line([x, body.get_top()[1], 0], [x, body.get_top()[1] + 0.08, 0], color=color, stroke_width=2))
        pins.add(Line([x, body.get_bottom()[1], 0], [x, body.get_bottom()[1] - 0.08, 0], color=color, stroke_width=2))
    t = label(label_text, font_size=font_size).move_to(body)
    g = VGroup(body, pins, t)
    g.body, g.text = body, t
    return g


def memory_bar(parts: list[tuple[float, str]], scale: float, width=0.6, outline=None, capacity=None) -> VGroup:
    """Vertical stacked bar: parts = [(GB, color), ...], ``scale`` = scene units per GB."""
    g = VGroup()
    y = 0.0
    for gb, col in parts:
        h = max(gb * scale, 1e-3)
        r = Rectangle(width=width, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
        r.move_to([0, y + h / 2, 0])
        g.add(r)
        y += h
    if capacity is not None:
        cap = DashedLine([-width * 0.8, capacity * scale, 0], [width * 0.8, capacity * scale, 0], color=WHITE,
                         stroke_width=2)
        g.add(cap)
        g.cap = cap
    return g


# ---------------------------------------------------------------------------
# The pipeline map (recurring roadmap)
# ---------------------------------------------------------------------------
STAGES = [
    ("web", r"The web", C.PAGE),
    ("data", r"Clean data", C.KEPT),
    ("pretrain", r"Pretraining", C.PARAMS),
    ("cluster", r"GPU cluster", C.GPU),
    ("post", r"Post-training", C.REWARD),
    ("assistant", r"Assistant", WHITE),
]


def stage_icon(key: str, color) -> VGroup:
    if key == "web":
        g = VGroup(Circle(0.32, color=color, stroke_width=2.5),
                   Ellipse(0.32, 0.64, color=color, stroke_width=2),
                   Line(LEFT * 0.32, RIGHT * 0.32, color=color, stroke_width=2),
                   Arc(0.5, PI / 2 - 0.9, 1.8, color=color, stroke_width=2).shift(DOWN * 0.3).scale(0.62),
                   Arc(0.5, -PI / 2 - 0.9, 1.8, color=color, stroke_width=2).shift(UP * 0.3).scale(0.62))
    elif key == "data":
        g = VGroup(*[RoundedRectangle(width=0.5, height=0.62, corner_radius=0.05, stroke_color=color, stroke_width=2,
                                      fill_color=BACKGROUND, fill_opacity=1).shift((RIGHT + UP) * 0.06 * k)
                     for k in range(3)])
        for k in range(3):
            g.add(Line(LEFT * 0.16, RIGHT * 0.16, color=color, stroke_width=1.5).shift(UP * (0.15 - 0.12 * k) + (RIGHT + UP) * 0.12))
    elif key == "pretrain":
        nodes = [[Dot([x, y, 0], radius=0.045, color=color) for y in ys] for x, ys in
                 [(-0.3, [-0.2, 0.0, 0.2]), (0.0, [-0.27, -0.09, 0.09, 0.27]), (0.3, [-0.1, 0.1])]]
        lines = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=1, color=color, stroke_opacity=0.6)
                         for la, lb in zip(nodes, nodes[1:]) for a in la for b in lb])
        g = VGroup(lines, *[d for col in nodes for d in col])
    elif key == "cluster":
        g = VGroup(*[RoundedRectangle(width=0.24, height=0.24, corner_radius=0.03, stroke_color=color, stroke_width=1.8,
                                      fill_color=color, fill_opacity=0.25) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.06)
    elif key == "post":
        g = VGroup(Circle(0.3, color=color, stroke_width=2.5),
                   VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
                       [[-0.14, 0.0, 0], [-0.03, -0.12, 0], [0.16, 0.12, 0]]))
    else:  # assistant: a speech bubble
        bub = RoundedRectangle(width=0.66, height=0.46, corner_radius=0.12, stroke_color=color, stroke_width=2.5)
        tail = Polygon([-0.12, -0.23, 0], [0.02, -0.23, 0], [-0.16, -0.38, 0], stroke_color=color, stroke_width=2.5)
        dots = VGroup(*[Dot(radius=0.035, color=color) for _ in range(3)]).arrange(RIGHT, buff=0.08)
        g = VGroup(bub, tail, dots)
    return g


def pipeline_map(width=13.0, highlight: str | None = None, dim=0.3, font_size=24) -> VGroup:
    """The recurring roadmap: six stages joined by arrows.  ``.stages[key]`` is (box, icon, label)."""
    n = len(STAGES)
    cell = width / n
    stages, arrows = VGroup(), VGroup()
    by_key = {}
    for i, (key, name, col) in enumerate(STAGES):
        box = RoundedRectangle(width=cell * 0.78, height=1.25, corner_radius=0.14, stroke_color=col, stroke_width=2.5,
                               fill_color=col, fill_opacity=0.08)
        icon = stage_icon(key, col).move_to(box).shift(UP * 0.12)
        txt = label(name, font_size=font_size).next_to(box, DOWN, buff=0.15)
        g = VGroup(box, icon, txt)
        g.move_to(RIGHT * (i - (n - 1) / 2) * cell)
        g.box, g.icon, g.text = box, icon, txt
        stages.add(g)
        by_key[key] = g
    for a, b in zip(stages, stages[1:]):
        arrows.add(Arrow(a.box.get_right(), b.box.get_left(), buff=0.06, stroke_width=3, color=GREY_B,
                         max_tip_length_to_length_ratio=0.35))
    m = VGroup(stages, arrows)
    m.stages, m.arrows, m.by_key = stages, arrows, by_key
    if highlight is not None:
        for key, g in by_key.items():
            if key != highlight:
                g.set_opacity(dim)
        arrows.set_opacity(dim)
    return m


# ---------------------------------------------------------------------------
# Small numeric helpers for the training runs
# ---------------------------------------------------------------------------
def run(results: dict, name: str) -> dict:
    return results[name]


def eval_curve(r: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(steps, tokens, val loss) arrays of a cached run."""
    e = np.array(r["evals"], float)
    return e[:, 0], e[:, 1], e[:, 2]


def train_curve(r: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(steps, train loss, lr factor)."""
    c = np.array(r["curve"], float)
    return c[:, 0], c[:, 1], c[:, 3]


def pocket_total_flops() -> float:
    """Total training arithmetic of every miniature pretraining run made for this video, tuning runs
    included (6N + attention FLOPs per token)."""
    import json

    from explainer.lm.pocket import Config, PocketGPT, flops_per_token

    from .compute import RUN_DIR

    total = 0.0
    for f in RUN_DIR.glob("*.json"):
        r = json.loads(f.read_text())
        cfg = Config(**r["run"]["model"])
        steps_done = r["curve"][-1][0] + 1
        total += flops_per_token(PocketGPT(cfg).count(), cfg) * r["tokens_per_step"] * steps_done
    return total


def bar_rows(items, scale: float, font_size=26, bar_h=0.36, buff=0.18, name_color=GREY_A, value_color=WHITE,
             opacity=0.85) -> VGroup:
    """Horizontal bar chart rows.  items = [(name TeX, value, color, value TeX)]; bar length = value * scale.
    Names are right-aligned against a common left edge for the bars.  Row i is (name, bar, value label)."""
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
