"""Helpers shared by the open-models scenes: text, model tags, layer strips,
expert grids, heat maps, plots."""

from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm

from .toys import cfg, data, model  # noqa: F401

KEYS = ("mimo", "glm", "kimi")
NAMES = {"mimo": "MiMo-V2.6-Pro", "glm": "GLM-5.3", "kimi": "Kimi K3"}
MAKERS = {"mimo": "Xiaomi", "glm": "Z.ai", "kimi": "Moonshot AI"}
MCOLOR = {"mimo": C.MIMO, "glm": C.GLM, "kimi": C.KIMI}
MONO = "DejaVu Sans Mono"

# ---------------------------------------------------------------------------
# Text (labels never wrap on their own and are shrunk to fit the frame)
# ---------------------------------------------------------------------------
WIDE_TEX = TEX_TEMPLATE.copy()
WIDE_TEX.add_to_preamble(r"\setlength{\textwidth}{40cm}")
MAX_TEXT_WIDTH = 13.6


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    kw.setdefault("tex_template", WIDE_TEX)
    t = Tex(text, color=color, font_size=font_size, **kw)
    if t.width > MAX_TEXT_WIDTH:
        t.width = MAX_TEXT_WIDTH
    return t


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    return label(text, font_size=font_size, color=color)


def schematic_tag(corner=DR) -> Tex:
    return note(r"schematic").to_corner(corner, buff=0.25)


def toy_tag(text=r"toy computation on random vectors", corner=DR) -> Tex:
    return note(text).to_corner(corner, buff=0.25)


def source(text: str, font_size=20) -> Tex:
    return label(r"Source: " + text, font_size=font_size, color=GREY_B).to_corner(DR, buff=0.25)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def fmt_int(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")


def model_tag(key: str, font_size=28) -> VGroup:
    """Small colored name tag for the top-left corner of a model's chapter."""
    dot = Dot(radius=0.09, color=MCOLOR[key])
    t = label(NAMES[key], font_size=font_size, color=MCOLOR[key])
    g = VGroup(dot, t).arrange(RIGHT, buff=0.15)
    return g.to_corner(UL, buff=0.3)


def chapter_card(number: int, text: str, sub: str = "") -> VGroup:
    num = label(rf"Chapter {number}", font_size=32, color=C.DIM)
    title = label(text, font_size=58)
    g = VGroup(num, title)
    if sub:
        g.add(label(sub, font_size=32, color=GREY_A))
    return g.arrange(DOWN, buff=0.25)


def show_chapter_card(scene: Scene, number: int, text: str, sub: str = "", hold: float = 1.2):
    card = chapter_card(number, text, sub)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
    scene.wait(hold)
    scene.play(FadeOut(card, shift=UP * 0.2), run_time=0.6)


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------
def block(text: str, color, width=2.8, height=0.85, font_size=32, fill_opacity=0.18) -> VGroup:
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=fill_opacity)
    lab = label(text, color=WHITE, font_size=font_size).move_to(box)
    if lab.width > width - 0.2:
        lab.width = width - 0.2
    g = VGroup(box, lab)
    g.box, g.text = box, lab
    return g


def vector_strip(values, color=C.EMBED, cell=0.2, gap=0.035, vmax=None, outline=True, direction=DOWN) -> VGroup:
    """A column (or row) of cells whose brightness follows |value|."""
    values = np.asarray(values, dtype=float)
    vmax = vmax or (np.abs(values).max() + 1e-9)
    cells = VGroup()
    for v in values:
        a = min(1.0, abs(v) / vmax)
        col = color if v >= 0 else interpolate_color(ManimColor(color), ManimColor(BACKGROUND), 0.45)
        cells.add(Square(cell, stroke_width=0, fill_color=col, fill_opacity=0.12 + 0.88 * a))
    cells.arrange(direction, buff=gap)
    group = VGroup(cells)
    if outline:
        group.add(SurroundingRectangle(cells, buff=0.04, color=color, stroke_width=1.5, corner_radius=0.04))
    group.cells = cells
    return group


def random_values(n, seed=0, scale=1.0) -> np.ndarray:
    return np.random.default_rng(seed).normal(0, scale, n)


def cell_matrix(rows, cols, color, cell=0.16, gap=0.025, seed=0, label_tex=None, font_size=34) -> VGroup:
    """A weight matrix drawn as a grid of cells (values are illustrative)."""
    rng = np.random.default_rng(seed)
    grid = VGroup()
    for _ in range(rows * cols):
        a = abs(rng.normal(0, 0.45))
        grid.add(Square(cell, stroke_width=0, fill_color=color, fill_opacity=min(0.95, 0.1 + a)))
    grid.arrange_in_grid(rows, cols, buff=gap)
    frame = SurroundingRectangle(grid, buff=0.05, color=color, stroke_width=2, corner_radius=0.04)
    g = VGroup(grid, frame)
    if label_tex:
        g.label = MathTex(label_tex, font_size=font_size, color=color).next_to(frame, UP, buff=0.12)
        g.add(g.label)
    g.grid, g.frame = grid, frame
    return g


def layer_strip(types, colors: dict, cell=0.13, gap=0.03, height=None, outline_types=(), per_row=None) -> VGroup:
    """One cell per layer, colored by layer type (real layouts come from the configs)."""
    height = height or cell * 2.6
    cells = VGroup()
    for t in types:
        col = colors[t]
        r = Rectangle(width=cell, height=height, stroke_width=1.2 if t in outline_types else 0, stroke_color=col,
                      fill_color=col, fill_opacity=0.12 if t in outline_types else 0.9)
        r.layer_type = t
        cells.add(r)
    if per_row:
        cells.arrange_in_grid(cols=per_row, buff=gap)
    else:
        cells.arrange(RIGHT, buff=gap)
    cells.types = list(types)
    return cells


def expert_grid(rows, cols, active=(), shared=0, cell=0.16, gap=0.04, color=C.EXPERT, active_color=None) -> VGroup:
    """Routed experts as a grid of small squares; ``active`` indices light up."""
    active_color = active_color or color
    sq = VGroup()
    for i in range(rows * cols):
        on = i in active
        sq.add(Square(cell, stroke_width=1 if on else 0.6, stroke_color=active_color if on else color,
                      fill_color=active_color if on else color, fill_opacity=0.95 if on else 0.16))
    sq.arrange_in_grid(rows, cols, buff=gap)
    g = VGroup(sq)
    g.cells = sq
    g.shared = VGroup()
    if shared:
        sh = VGroup(*[RoundedRectangle(width=cell * 3.2, height=cell * 3.2, corner_radius=0.05, stroke_color=C.SHARED_EXPERT,
                                       stroke_width=2, fill_color=C.SHARED_EXPERT, fill_opacity=0.8) for _ in range(shared)])
        sh.arrange(DOWN, buff=0.12).next_to(sq, LEFT, buff=0.25)
        g.add(sh)
        g.shared = sh
    return g


PLANE_SCALE = 1.35


def vec_arrow(plane, v, color, width=5) -> Arrow:
    return Arrow(plane.c2p(0, 0), plane.c2p(*v), buff=0, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.15)


def pick_active(n, k, seed) -> list[int]:
    return sorted(np.random.default_rng(seed).choice(n, size=k, replace=False).tolist())


def heat_image(arr, height, width=None, colors=None, vmin=None, vmax=None, diverging=False, neg=None, pos=None,
               nearest=True) -> ImageMobject:
    """A 2-D array as a pixel image (rows top to bottom)."""
    arr = np.asarray(arr, dtype=float)
    if diverging:
        vmax = vmax or np.abs(arr).max()
        rgb = cm.diverging(arr, vmax, neg=neg or "#5B8CFF", pos=pos or "#FF9F5A", gamma=0.9)
    else:
        lo, hi = colors or (BACKGROUND, "#FFFFFF")
        rgb = cm.sequential(arr, arr.min() if vmin is None else vmin, arr.max() if vmax is None else vmax,
                            low=lo, high=hi)
    img = ImageMobject(cm.to_uint8(rgb))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest" if nearest else "bilinear"])
    img.stretch_to_fit_height(height)
    img.stretch_to_fit_width(width or height * arr.shape[1] / arr.shape[0])
    return img


def color_hex(c) -> str:
    return ManimColor(c).to_hex()


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
class Plot(VGroup):
    """Axes along the bottom and left edges of a box; optional log scales."""

    def __init__(self, x_range, y_range, width=9.0, height=4.6, x_ticks=(), y_ticks=(), x_fmt=str, y_fmt=None,
                 font_size=26, color=GREY_B, log_x=False, log_y=False):
        super().__init__()
        self.x_range, self.y_range, self.w, self.h = x_range, y_range, width, height
        self.log_x, self.log_y = log_x, log_y
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
            m.next_to(p, DOWN, buff=0.15)
            self.x_labels.add(m)
        for t in y_ticks:
            p = self.c2p(x_range[0], t)
            self.add(Line(p, p + LEFT * 0.08, color=color, stroke_width=2))
            lab = y_fmt(t)
            m = lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=GREY_A)
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

    def bars(self, xs, ys, width, color, opacity=0.85, y0=None) -> VGroup:
        y0 = self.y_range[0] if y0 is None else y0
        g = VGroup()
        for x, y in zip(xs, ys):
            top, bot = self.c2p(x, max(y, y0)), self.c2p(x, min(y, y0))
            h = max(1e-3, top[1] - bot[1])
            g.add(Rectangle(width=width, height=h, stroke_width=0, fill_color=color, fill_opacity=opacity)
                  .move_to((top + bot) / 2))
        return g


def bar_row(values, width_total, height, color, gap=0.0, opacity=0.85) -> VGroup:
    """Horizontal stacked bar: segment widths proportional to ``values``."""
    tot = float(sum(values))
    segs = VGroup(*[Rectangle(width=max(1e-3, width_total * v / tot), height=height, stroke_width=0,
                              fill_color=c, fill_opacity=opacity) for v, c in zip(values, color)])
    segs.arrange(RIGHT, buff=gap)
    return segs


def equal_sign_bars(values, plot: Plot, color, width=0.06) -> VGroup:
    return plot.bars(np.arange(len(values)) + 0.5, values, width, color)
