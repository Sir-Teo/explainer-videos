"""Helpers shared by the stochastic-calculus scenes: text, curves from arrays, histograms, glowing particle
clouds drawn as images, and the "tank" that collects area (squares, triangles) to show what a sum adds up to."""

from __future__ import annotations

import math

import numpy as np
from scipy.ndimage import gaussian_filter

from explainer import *  # noqa: F403
from explainer.fluids import colormaps as cm

from .compute import load  # noqa: F401

# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
WIDE_TEX = TEX_TEMPLATE.copy()
WIDE_TEX.add_to_preamble(r"\setlength{\textwidth}{40cm}")
MAX_TEXT_WIDTH = 13.6


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    """A Tex label that never wraps on its own (line breaks are explicit) and shrinks to fit the frame."""
    kw.setdefault("tex_template", WIDE_TEX)
    t = Tex(text, color=color, font_size=font_size, **kw)
    if t.width > MAX_TEXT_WIDTH:
        t.width = MAX_TEXT_WIDTH
    return t


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    """Small grey caption, e.g. a source line or 'simulated'."""
    return label(text, font_size=font_size, color=color)


def mtex(tex: str, color=WHITE, font_size=36, **kw) -> MathTex:
    return MathTex(tex, color=color, font_size=font_size, **kw)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def boxed(mob: Mobject, color=YELLOW, buff=0.25, fill=0.0) -> VGroup:
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12, stroke_width=2.5)
    if fill:
        box.set_fill(color, opacity=fill)
    return VGroup(box, mob)


def part_card(number: int, title: str, subtitle: str = "") -> VGroup:
    num = label(rf"Part {number}", font_size=34, color=C.DIM)
    t = label(title, font_size=60)
    g = VGroup(num, t)
    if subtitle:
        g.add(label(subtitle, font_size=32, color=GREY_A))
    return g.arrange(DOWN, buff=0.3)


def sim_tag(text=r"simulated", corner=UR) -> Tex:
    return note(text).to_corner(corner, buff=0.3)


def num(x: float, digits=3, sign=False) -> str:
    s = f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}"
    return s.replace("-", "{-}")


def fmt_int(n: int) -> str:
    """12345678 -> '12{,}345{,}678' for MathTex."""
    return f"{int(n):,}".replace(",", "{,}")


# The multiplication table, the one rule everything else rests on.
def mult_table(font_size=40) -> VGroup:
    cells = [
        [r"\times", r"dt", r"dW"],
        [r"dt", r"0", r"0"],
        [r"dW", r"0", r"dt"],
    ]
    grid = VGroup()
    for i, row in enumerate(cells):
        for j, c in enumerate(row):
            m = MathTex(c, font_size=font_size)
            if c == "dW":
                m.set_color(C.BROWNIAN)
            elif c == "dt":
                m.set_color(C.CLOCK)
            if (i, j) == (2, 2):
                m.set_color(C.QV)
            if c == "0":
                m.set_color(GREY_B)
            m.move_to([j * 1.25, -i * 0.85, 0])
            grid.add(m)
    h = Line([0.6, 0.42, 0], [0.6, -2.12, 0], color=GREY_C, stroke_width=2)
    v = Line([-0.55, -0.42, 0], [3.0, -0.42, 0], color=GREY_C, stroke_width=2)
    t = VGroup(grid, h, v).center()
    t.cells = grid
    return t


# ---------------------------------------------------------------------------
# Curves from arrays
# ---------------------------------------------------------------------------
def polyline(ax: Axes, xs, ys, color=WHITE, stroke_width=3, **kw) -> VMobject:
    pts = ax.c2p(np.asarray(xs, float), np.asarray(ys, float)).T
    m = VMobject(color=color, stroke_width=stroke_width, **kw)
    m.set_points_as_corners(pts)
    return m


def decimate(xs, ys, max_points=2400):
    """Keep at most ``max_points`` vertices, preserving each bucket's min and max (so the roughness
    survives on screen)."""
    xs, ys = np.asarray(xs), np.asarray(ys)
    n = len(xs)
    if n <= max_points:
        return xs, ys
    k = int(math.ceil(n / (max_points // 2)))
    m = (n // k) * k
    bx = xs[:m].reshape(-1, k)
    by = ys[:m].reshape(-1, k)
    lo, hi = by.argmin(axis=1), by.argmax(axis=1)
    first = np.minimum(lo, hi)
    second = np.maximum(lo, hi)
    r = np.arange(len(bx))
    ox = np.stack([bx[r, first], bx[r, second]], axis=1).ravel()
    oy = np.stack([by[r, first], by[r, second]], axis=1).ravel()
    return np.concatenate([ox, xs[m:]]), np.concatenate([oy, ys[m:]])


def path_curve(ax: Axes, W, t0=0.0, t1=1.0, color=C.BROWNIAN, stroke_width=2.5, max_points=2400, **kw):
    ts = np.linspace(t0, t1, len(W))
    xs, ys = decimate(ts, W, max_points)
    return polyline(ax, xs, ys, color=color, stroke_width=stroke_width, **kw)


def hero(n: int | None = None) -> np.ndarray:
    """The hero path W on [0, 1], sampled at n + 1 equally spaced times (n a power of 2)."""
    W = load("hero")["W"]
    if n is None:
        return W
    return W[:: (len(W) - 1) // n]


class TWAxes(Axes):
    """Axes whose end-of-axis numbers are built on first access of ``x_labels``, i.e. after the axes have been
    positioned (labels made at construction would be left behind by ``move_to`` / ``to_edge``)."""

    def __init__(self, *args, t_max=1.0, y_min=0.0, numbers=True, **kwargs):
        super().__init__(*args, **kwargs)
        self._t_max, self._y_min, self._numbers, self._x_labels = t_max, y_min, numbers, None

    @property
    def x_labels(self) -> VGroup:
        if self._x_labels is None:
            g = VGroup()
            if self._numbers:
                g.add(MathTex("0", font_size=24).next_to(self.c2p(0, self._y_min), DOWN, buff=0.12),
                      MathTex(f"{self._t_max:g}", font_size=24).next_to(self.c2p(self._t_max, self._y_min), DOWN, buff=0.12))
            self._x_labels = g
        return self._x_labels


def tw_axes(x_length=11.0, y_range=(-1.0, 1.6, 0.5), y_length=4.6, t_max=1.0, numbers=True, **kw) -> TWAxes:
    cfg = {"stroke_color": GREY_B, "stroke_width": 2, "include_ticks": False}
    return TWAxes(x_range=[0, t_max, t_max / 4], y_range=list(y_range), x_length=x_length, y_length=y_length,
                  tips=False, axis_config=cfg, t_max=t_max, y_min=y_range[0], numbers=numbers, **kw)


def axis_labels(ax: Axes, x="t", y="W_t", y_color=C.BROWNIAN, font_size=30) -> VGroup:
    xl = MathTex(x, font_size=font_size, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
    yl = MathTex(y, font_size=font_size, color=y_color).next_to(ax.y_axis.get_end(), UP, buff=0.12)
    return VGroup(xl, yl)


# ---------------------------------------------------------------------------
# Probability
# ---------------------------------------------------------------------------
def gauss_pdf(x, mean=0.0, var=1.0):
    x = np.asarray(x, float)
    return np.exp(-((x - mean) ** 2) / (2 * var)) / np.sqrt(2 * np.pi * var)


def density(samples, edges) -> np.ndarray:
    h, _ = np.histogram(samples, bins=edges)
    return h / (len(samples) * np.diff(edges))


def hist_shape(ax: Axes, edges, heights, color=C.PDF, fill_opacity=0.35, stroke_width=2, sideways=False,
               base=0.0) -> VMobject:
    """A histogram as one step-shaped polygon.  ``sideways``: the value axis is the y axis of ``ax``
    (bars grow in +x from x = ``base``), for a histogram standing next to a fan of paths."""
    xs, ys = [edges[0]], [0.0]
    for a, b, h in zip(edges[:-1], edges[1:], heights):
        xs += [a, b]
        ys += [h, h]
    xs.append(edges[-1])
    ys.append(0.0)
    xs, ys = np.array(xs, float), np.array(ys, float)
    pts = ax.c2p(base + ys, xs).T if sideways else ax.c2p(xs, base + ys).T
    m = VMobject(stroke_color=color, stroke_width=stroke_width, fill_color=color, fill_opacity=fill_opacity)
    m.set_points_as_corners(pts)
    return m


def pdf_curve(ax: Axes, xs, ps, color=C.PDF, stroke_width=3, sideways=False, base=0.0) -> VMobject:
    xs, ps = np.asarray(xs, float), np.asarray(ps, float)
    pts = ax.c2p(base + ps, xs).T if sideways else ax.c2p(xs, base + ps).T
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_smoothly(pts) if len(xs) < 80 else m.set_points_as_corners(pts)
    return m


# ---------------------------------------------------------------------------
# Glowing particle clouds, drawn into an image each frame (thousands of vector dots would crawl)
# ---------------------------------------------------------------------------
def splat(xs, ys, extent, shape, sigma=1.3, weights=None) -> np.ndarray:
    """Deposit particles bilinearly into a (H, W) grid, blur, and normalize so one isolated particle peaks
    at 1.  ``extent`` = (x0, x1, y0, y1) in the same units as xs, ys."""
    H, W = shape
    x0, x1, y0, y1 = extent
    px = (np.asarray(xs, float) - x0) / (x1 - x0) * (W - 1)
    py = (y1 - np.asarray(ys, float)) / (y1 - y0) * (H - 1)
    w = np.ones_like(px) if weights is None else np.asarray(weights, float)
    ok = (px >= 0) & (px < W - 1) & (py >= 0) & (py < H - 1) & np.isfinite(px) & np.isfinite(py)
    px, py, w = px[ok], py[ok], w[ok]
    ix, iy = px.astype(int), py.astype(int)
    fx, fy = px - ix, py - iy
    img = np.zeros((H, W), np.float64)
    np.add.at(img, (iy, ix), w * (1 - fx) * (1 - fy))
    np.add.at(img, (iy, ix + 1), w * fx * (1 - fy))
    np.add.at(img, (iy + 1, ix), w * (1 - fx) * fy)
    np.add.at(img, (iy + 1, ix + 1), w * fx * fy)
    return gaussian_filter(img, sigma) * (2 * np.pi * sigma * sigma)


def glow(intensity, color, gain=1.6, white=0.55, alpha=1.0) -> np.ndarray:
    """Intensity -> RGBA uint8: the color fades in with intensity and turns whiter where particles pile up."""
    a = 1 - np.exp(-gain * intensity)
    hot = np.clip((intensity - 1.0) / 6.0, 0, 1)[..., None] * white
    c = np.array(ManimColor(color).to_rgb(), dtype=np.float32)
    rgb = c + (1 - c) * hot
    out = np.concatenate([rgb, (a * alpha)[..., None]], axis=2)
    return cm.to_uint8(out)


def composite(*layers) -> np.ndarray:
    """'Over'-composite RGBA uint8 layers (first = bottom)."""
    out = layers[0].astype(np.float32) / 255
    for lay in layers[1:]:
        lay = lay.astype(np.float32) / 255
        a = lay[..., 3:]
        out_a = a + out[..., 3:] * (1 - a)
        out[..., :3] = (lay[..., :3] * a + out[..., :3] * out[..., 3:] * (1 - a)) / np.maximum(out_a, 1e-6)
        out[..., 3:] = out_a
    return cm.to_uint8(out)


class Raster(ImageMobject):
    """An image redrawn by ``draw(value) -> RGBA uint8`` whenever ``tracker`` changes value.

    Fades go through :meth:`fade` (the alpha is applied on top of whatever ``draw`` returns), so playback
    keeps running during them.  ``clear_scene`` removes the updater before fading it out.
    """

    def __init__(self, draw, tracker: ValueTracker, width: float, height: float, center=ORIGIN, alpha=1.0, **kw):
        self.draw = draw
        self.tracker = tracker
        self.alpha = alpha
        self._v = tracker.get_value()
        super().__init__(self._render(self._v), **kw)
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.stretch_to_fit_width(width).stretch_to_fit_height(height).move_to(center)
        self.add_updater(Raster._tick)

    def _render(self, v):
        img = self.draw(v)
        if self.alpha < 1:
            img = img.copy()
            img[..., 3] = (img[..., 3] * self.alpha).astype(np.uint8)
        return img

    def refresh(self):
        self._v = self.tracker.get_value()
        self.pixel_array = self._render(self._v)
        return self

    @staticmethod
    def _tick(m):
        if m.tracker.get_value() != m._v:
            m.refresh()

    def fade(self, to: float = 1.0, **kwargs) -> Animation:
        start = self.alpha

        def upd(m, a):
            m.alpha = start + (to - start) * a
            m.refresh()

        return UpdateFromAlphaFunc(self, upd, suspend_mobject_updating=False, **kwargs)


def raster_for(ax: Axes, x_range, y_range, px_per_unit=110):
    """Geometry for a Raster covering the data rectangle x_range x y_range of ``ax``:
    returns (extent, shape, width, height, center)."""
    (x0, x1), (y0, y1) = x_range, y_range
    p0, p1 = ax.c2p(x0, y0), ax.c2p(x1, y1)
    width, height = p1[0] - p0[0], p1[1] - p0[1]
    shape = (max(8, int(height * px_per_unit)), max(8, int(width * px_per_unit)))
    return (x0, x1, y0, y1), shape, width, height, (p0 + p1) / 2


# ---------------------------------------------------------------------------
# The area tank: a container whose capacity is a known area (T, or T/2); squares or triangles of area
# poured into it become strips of the tank's width stacked from the bottom, so the fill level *is* the sum.
# ---------------------------------------------------------------------------
class Tank(VGroup):
    def __init__(self, capacity: float, unit: float, width: float, color=C.QV, cap_label=None, overflow=0.45):
        """``unit``: screen length of one unit of the quantity whose square is being collected
        (one unit of area = unit**2 screen area).  The brim sits at ``capacity``.  Move the tank freely,
        but don't rescale it: strips are sized in screen units."""
        super().__init__()
        self.capacity, self.unit, self.w, self.color = capacity, unit, width, color
        self.h = capacity * unit * unit / width
        H = self.h * (1 + overflow)
        self.outline = VMobject(stroke_color=GREY_A, stroke_width=3)
        self.outline.set_points_as_corners([[-width / 2, H, 0], [-width / 2, 0, 0], [width / 2, 0, 0], [width / 2, H, 0]])
        self.brim = DashedLine([-width / 2 - 0.15, self.h, 0], [width / 2 + 0.15, self.h, 0], color=C.CLOCK,
                               stroke_width=2.5, dash_length=0.1)
        self.floor = Dot(ORIGIN, radius=0.001).set_opacity(0)  # moves with the group; strips stack from here
        self.add(self.outline, self.brim, self.floor)
        if cap_label is not None:
            self.cap = MathTex(cap_label, font_size=30, color=C.CLOCK).next_to(self.brim, RIGHT, buff=0.12)
            self.add(self.cap)
        self.level = 0.0

    def y_of(self, area: float) -> float:
        """Screen height above the floor of fill level ``area``."""
        return area * self.unit * self.unit / self.w

    def strip(self, area: float, at: float | None = None, color=None, opacity=0.75) -> Rectangle:
        """A strip holding ``area`` (in units of the quantity squared), placed on top of level ``at``."""
        at = self.level if at is None else at
        h = max(self.y_of(area), 1e-4)
        r = Rectangle(width=self.w - 0.04, height=h, stroke_width=0, fill_color=color or self.color, fill_opacity=opacity)
        r.move_to(self.floor.get_center() + UP * (self.y_of(at) + h / 2))
        return r

    def fill_rect(self, area: float, color=None, opacity=0.75) -> Rectangle:
        return self.strip(area, at=0.0, color=color, opacity=opacity)


def pour(scene: Scene, tank: Tank, pieces: list[VMobject], areas, run_time=2.0, lag=0.08, color=None):
    """Animate each piece morphing into its strip in the tank; returns the strips (left in the scene)."""
    strips = []
    for a in areas:
        s = tank.strip(abs(a), color=color)
        tank.level += abs(a)
        strips.append(s)
    anims = [ReplacementTransform(p, s) for p, s in zip(pieces, strips)]
    scene.play(LaggedStart(*anims, lag_ratio=lag), run_time=run_time)
    return VGroup(*strips)


def square_on(ax: Axes, t: float, w0: float, w1: float, unit: float, color=C.QV, opacity=0.45) -> Square:
    """The square whose left side is the increment from (t, w0) to (t, w1), drawn to the W scale ``unit``."""
    side = abs(w1 - w0) * unit
    sq = Square(side_length=max(side, 1e-3), stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=opacity)
    p = ax.c2p(t, min(w0, w1))
    sq.move_to(p + RIGHT * side / 2 + UP * side / 2)
    return sq


def traced_path(ax: Axes, W, tracker: ValueTracker, t0=0.0, t1=1.0, color=C.BROWNIAN, stroke_width=2.5,
                max_points=2400, dot=True) -> VGroup:
    """A path drawn up to time ``tracker`` (in time order, unlike Create, which follows arc length), with a dot
    at its tip."""
    ts = np.linspace(t0, t1, len(W))
    xs, ys = decimate(ts, W, max_points)
    pts = ax.c2p(xs, ys).T

    def make():
        t = tracker.get_value()
        k = int(np.searchsorted(xs, t, side="right"))
        m = VMobject(color=color, stroke_width=stroke_width)
        if k >= 2:
            m.set_points_as_corners(pts[:k])
        else:
            m.set_points_as_corners([pts[0], pts[0] + 1e-4 * RIGHT])
        return m

    curve = always_redraw(make)
    g = VGroup(curve)
    if dot:
        def tip():
            t = tracker.get_value()
            k = max(0, min(len(xs) - 1, int(np.searchsorted(xs, t, side="right")) - 1))
            return Dot(pts[k], radius=0.06, color=WHITE)
        g.add(always_redraw(tip))
    g.curve = curve
    return g


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
    rule = Line([-0.1, -(height + v_buff) / 2 - 0.05, 0], [xs[-1] + widths[-1] + 0.1, -(height + v_buff) / 2 - 0.05, 0],
                color=GREY_D, stroke_width=1.5)
    t = VGroup(grid, rule)
    t.header, t.rule, t.rows = grid[0], rule, list(grid[1:])
    t.cols = [VGroup(*[grid[i][j] for i in range(len(cells))]) for j in range(cols)]
    return t
