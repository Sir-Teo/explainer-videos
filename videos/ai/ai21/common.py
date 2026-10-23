"""Helpers shared by the scenes of Part 21 ("Diffusion and Flow")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 21
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
NOISE, DATA = C.TRUE_P, C.BITS  # noise points, data points
SCORE = C.MODEL_Q  # the score / velocity arrows
DDPM_C, DDIM_C, FM_C, RF_C = C.SURPRISE, C.TRUE_P, C.INTERVAL, C.BITS
EULER_C, HEUN_C, DPM2_C, DPMPP_C = GREY_B, "#B39DDB", "#5CD0B3", C.MODEL_Q  # the samplers
OT_C, RF2_C = "#7FD3FF", "#FFB070"
PROG_C, CD_C, DMD_C, MF_C, SC_C = "#B39DDB", "#7FD3FF", "#FF6B8B", "#FFB070", C.TRUE_P  # the one-step students
CFG_C, CLS_C, AUTO_C = C.BITS, C.SURPRISE, C.INTERVAL  # the guidance methods
MDM_C, AR_C = "#7FD3FF", C.MODEL_Q  # the text models: masked diffusion, autoregressive
EPS_C, X0_C, F_C = C.SURPRISE, C.TRUE_P, "#B39DDB"  # what a denoiser predicts
SCHED = {"cos": C.BITS, "linb": C.SURPRISE, "fm": C.INTERVAL, "logn": "#B39DDB", "ddpm": C.SURPRISE,
         "trig": C.BITS, "cosine": "#7FD3FF", "vpsde": C.SURPRISE, "edm": "#B39DDB"}
HIST = C.HUMAN
PANEL = "#121722"
SOLVER_C = {"euler_vp": EULER_C, "ddim": DDIM_C, "heun": HEUN_C, "dpm2": DPM2_C, "dpmpp2m": DPMPP_C, "ddpm": DDPM_C}
SOLVER_NAME = {"euler_vp": r"Euler (VP time)", "ddim": r"DDIM", "heun": r"Heun (EDM)", "dpm2": r"DPM-Solver-2",
               "dpmpp2m": r"DPM-Solver++(2M)", "ddpm": r"DDPM"}


def rgb_of(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


BG_RGB = rgb_of("#0B0F17")


# ---------------------------------------------------------------------------
# The data plane
# ---------------------------------------------------------------------------
class Panel(VGroup):
    """A framed patch of the plane: data coordinates (xlim x ylim) to the scene. ``p``, ``pts``, ``dots``,
    ``image`` (a density on a grid), ``scatter`` (thousands of points as one picture), ``paths``."""

    def __init__(self, width=5.0, center=ORIGIN, xlim=(-2.7, 2.9), ylim=(-1.8, 1.6), frame=True, color=GREY_D):
        super().__init__()
        self.xlim, self.ylim = xlim, ylim
        self.w = width
        self.h = width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
        self.frame = RoundedRectangle(width=self.w, height=self.h, corner_radius=0.08, stroke_color=color,
                                      stroke_width=1.2).move_to(center)
        if not frame:
            self.frame.set_stroke(opacity=0)
        self.add(self.frame)

    @property
    def s(self):
        return self.w / (self.xlim[1] - self.xlim[0])

    def p(self, x, y=None):
        if y is None:
            x, y = x
        c = self.frame.get_center()
        cx, cy = (self.xlim[0] + self.xlim[1]) / 2, (self.ylim[0] + self.ylim[1]) / 2
        return np.array([c[0] + (x - cx) * self.s, c[1] + (y - cy) * self.s, 0.0])

    def clip(self, P, margin=0.02):
        P = np.asarray(P, float)
        mx = margin * (self.xlim[1] - self.xlim[0])
        return np.c_[np.clip(P[:, 0], self.xlim[0] + mx, self.xlim[1] - mx), np.clip(P[:, 1], self.ylim[0] + mx,
                                                                                       self.ylim[1] - mx)]

    def pts(self, P, clip=True) -> np.ndarray:
        P = self.clip(P) if clip else np.asarray(P, float)
        c = self.frame.get_center()
        cx, cy = (self.xlim[0] + self.xlim[1]) / 2, (self.ylim[0] + self.ylim[1]) / 2
        return np.c_[c[0] + (P[:, 0] - cx) * self.s, c[1] + (P[:, 1] - cy) * self.s, np.zeros(len(P))]

    def dots(self, P, color, radius=0.022, opacity=0.9) -> VGroup:
        return VGroup(*[Dot(q, radius=radius, color=color, fill_opacity=opacity) for q in self.pts(P)])

    def move(self, dots, P) -> list:
        return [d.animate.move_to(q) for d, q in zip(dots, self.pts(P))]

    def place(self, dots, P) -> None:
        for d, q in zip(dots, self.pts(P)):
            d.move_to(q)

    def paths(self, P, color, stroke_width=1.4, opacity=0.65, every=1, smooth=False) -> VGroup:
        """P: (frames, points, 2) -> one line per point."""
        P = np.asarray(P, float)
        g = VGroup()
        for i in range(0, P.shape[1], every):
            m = VMobject(stroke_color=color, stroke_width=stroke_width, stroke_opacity=opacity)
            q = self.pts(P[:, i])
            m.set_points_smoothly(q) if smooth else m.set_points_as_corners(q)
            g.add(m)
        return g

    def image(self, Dn, color, gamma=0.55, vmax=None, extent=None) -> ImageMobject:
        """A density on a grid whose rows run in y from ylim[0] up (extent: (x0, x1, y0, y1) of the grid)."""
        img = to_image(density_rgb(Dn, color, gamma, vmax), 1, 1, smooth=True)
        x0, x1, y0, y1 = extent or (*self.xlim, *self.ylim)
        img.stretch_to_fit_width((x1 - x0) * self.s).stretch_to_fit_height((y1 - y0) * self.s)
        return img.move_to(self.p((x0 + x1) / 2, (y0 + y1) / 2))

    def scatter(self, P, color, radius_px=1.6, res=420, alpha=0.85, base=None) -> ImageMobject:
        """Points drawn into a picture: thousands of points at the cost of one image."""
        P = np.asarray(P, float)
        H = int(round(res * self.h / self.w))
        img = np.zeros((H, res, 3)) + BG_RGB if base is None else base.copy()
        col = rgb_of(color)
        u = (P[:, 0] - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * (res - 1)
        v = (self.ylim[1] - P[:, 1]) / (self.ylim[1] - self.ylim[0]) * (H - 1)
        rr = int(np.ceil(radius_px))
        yy, xx = np.mgrid[-rr:rr + 1, -rr:rr + 1]
        disk = (xx ** 2 + yy ** 2) <= radius_px ** 2
        for a, b in zip(np.round(u).astype(int), np.round(v).astype(int)):
            x0, x1, y0, y1 = a - rr, a + rr + 1, b - rr, b + rr + 1
            if x0 < 0 or y0 < 0 or x1 > res or y1 > H:
                continue
            sub = img[y0:y1, x0:x1]
            sub[disk] = (1 - alpha) * sub[disk] + alpha * col
        return to_image(img, self.w, self.h, smooth=True).move_to(self.frame.get_center())


def to_image(rgb: np.ndarray, width: float, height: float | None = None, smooth=False) -> ImageMobject:
    """An (h, w, 3) array in [0, 1] as an ImageMobject, rows top to bottom."""
    a = np.clip(rgb, 0, 1)
    img = ImageMobject((np.concatenate([a, np.ones(a.shape[:2] + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height if height is not None else width * a.shape[0] / a.shape[1])
    return img


def density_rgb(Dn, color, gamma=0.55, vmax=None) -> np.ndarray:
    """A density on a grid (rows = y upwards) as a glow of ``color`` on the dark background."""
    Dn = np.asarray(Dn, float)
    v = vmax if vmax is not None else max(np.percentile(Dn, 99.7), 1e-12)
    t = np.clip(Dn / v, 0, 1) ** gamma
    col = rgb_of(color)
    return (BG_RGB[None, None] * (1 - t[..., None]) + col[None, None] * t[..., None])[::-1]


def cloud(P, color, radius=0.03, scale=1.0, shift=ORIGIN, opacity=0.9) -> VGroup:
    return VGroup(*[Dot([p[0] * scale + shift[0], p[1] * scale + shift[1], 0], radius=radius, color=color,
                        fill_opacity=opacity) for p in np.asarray(P)])


def move_cloud(dots: VGroup, P, scale=1.0, shift=ORIGIN) -> list:
    return [d.animate.move_to([p[0] * scale + shift[0], p[1] * scale + shift[1], 0]) for d, p in zip(dots, np.asarray(P))]


def gray_image(a, size) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    rgb = np.stack([a, a, a, np.ones_like(a)], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def glyph_sheet(Q, rows, cols, size=0.6, gap=0.05, frame=True) -> Group:
    """Many 20 x 20 letter pictures as one image (cheaper to draw than many)."""
    Q = np.clip(np.asarray(Q, float), 0, 1)
    px = Q.shape[-1]
    g = max(1, int(round(gap / size * px)))
    H, W = rows * px + (rows - 1) * g, cols * px + (cols - 1) * g
    sheet = np.ones((H, W, 3)) * rgb_of(PANEL)[None, None]
    for k in range(min(len(Q), rows * cols)):
        r, c = divmod(k, cols)
        sheet[r * (px + g): r * (px + g) + px, c * (px + g): c * (px + g) + px] = Q[k][..., None]
    img = to_image(sheet, cols * size + (cols - 1) * gap, rows * size + (rows - 1) * gap)
    if not frame:
        return Group(img)
    box = SurroundingRectangle(img, buff=0.06, color=GREY_D, stroke_width=1.2, corner_radius=0.05)
    return Group(box, img)


def arrows_field(grid, field, scale=0.12, max_len=0.45, color=SCORE, stroke_width=2.2, shift=ORIGIN, unit=1.0) -> VGroup:
    """Little arrows showing a 2D vector field (lengths compressed so that the strongest ones don't swamp the rest)."""
    g = VGroup()
    F = np.asarray(field)
    mag = np.linalg.norm(F, axis=1)
    top = max(np.percentile(mag, 95), 1e-9)
    for p, v, m in zip(np.asarray(grid), F, mag):
        L = max_len * min(m / top, 1.0) ** 0.6
        if L < 0.04:
            continue
        d = v / max(m, 1e-9)
        s = np.array([p[0] * unit + shift[0], p[1] * unit + shift[1], 0])
        g.add(Arrow(s, s + L * np.array([d[0], d[1], 0]), buff=0, color=color, stroke_width=stroke_width,
                    max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
    return g


def panel_arrows(panel: Panel, grid, field, color=SCORE, max_len=0.32, stroke_width=2.0) -> VGroup:
    """A vector field drawn in a Panel."""
    g = VGroup()
    F = np.asarray(field, float)
    mag = np.linalg.norm(F, axis=1)
    top = max(np.percentile(mag, 95), 1e-9)
    for q, v, m in zip(panel.pts(grid, clip=False), F, mag):
        L = max_len * min(m / top, 1.0) ** 0.6
        if L < 0.035:
            continue
        d = v / max(m, 1e-9)
        g.add(Arrow(q, q + L * np.array([d[0], d[1], 0]), buff=0, color=color, stroke_width=stroke_width,
                    max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
    return g


def distill_picture() -> VGroup:
    """A jargon-card picture of distillation: VGroup(teacher's curved path, its many small steps, the student's one
    jump, the two names, the start and the end).  Show the path and ends first, then the steps, then the jump."""
    a, b = np.array([-1.6, -0.45, 0]), np.array([1.6, 0.25, 0])
    path = ArcBetweenPoints(a, b, angle=-1.1, color=FM_C, stroke_width=2.5)
    steps = VGroup(*[Dot(path.point_from_proportion(u), radius=0.045, color=FM_C) for u in np.linspace(0.08, 0.92, 11)])
    jump = Arrow(a, b, buff=0.08, color=RF_C, stroke_width=4, max_tip_length_to_length_ratio=0.12)
    ends = VGroup(Dot(a, radius=0.08, color=NOISE), Dot(b, radius=0.08, color=DATA))
    names = VGroup(label(r"teacher: \ many small steps", font_size=18, color=FM_C).next_to(path, UP, buff=0.08),
                   label(r"student: \ one jump, \ the same place", font_size=18, color=RF_C).next_to(jump, DOWN, buff=0.12))
    return VGroup(path, steps, jump, names, ends)


# ---------------------------------------------------------------------------
# Cards, plots and small diagrams
# ---------------------------------------------------------------------------
def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=width or (t.width + 2 * pad), height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def take_away(text: str, color=C.BITS, font_size=28, width=12.0) -> VGroup:
    """The chapter's takeaway: a line in a soft box at the bottom of the frame."""
    t = wrapped_label(text, width, font_size, color)
    box = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.35, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.94)
    return VGroup(box, t.move_to(box)).to_edge(DOWN, buff=0.35)


def chapter(scene, k, title, question, lit=()):
    """The chapter card, read out ("Chapter k. Title."), then cleared."""
    card = chapter_card(k, title, question, part=PART, lit=lit)
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
             "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen"]
    return card, words[k]


def log_axes(x_range, y_range, x_length=6.0, y_length=3.6, xlabel="", ylabel="", xticks=(), yticks=(), center=ORIGIN,
             font_size=20, xfmt=None, yfmt=None):
    """Axes in log10 coordinates on both sides (x_range, y_range in log10); ticks given as plain values."""
    from explainer.analysis import label as _label

    ax = CornerAxes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
    g = VGroup(ax)
    for v in xticks:
        g.add(MathTex(xfmt(v) if xfmt else f"{v:g}", font_size=font_size, color=GREY_B)
              .next_to(ax.c2p(math.log10(v), y_range[0]), DOWN, buff=0.12))
    for v in yticks:
        g.add(MathTex(yfmt(v) if yfmt else f"{v:g}", font_size=font_size, color=GREY_B)
              .next_to(ax.c2p(x_range[0], math.log10(v)), LEFT, buff=0.12))
    if xlabel:
        xl = _label(xlabel, font_size=font_size + 2, color=GREY_A)
        xl.next_to(ax, DOWN, buff=0.5 if xticks else 0.2)
        g.add(xl)
        g.xlabel = xl
    if ylabel:
        yl = _label(ylabel, font_size=font_size + 2, color=GREY_A).next_to(ax, UP, buff=0.18).align_to(ax, LEFT)
        g.add(yl)
        g.ylabel = yl
    g.ax = ax
    g.move_to(center)
    return g


def logcurve(ax, xs, ys, color, stroke_width=3, dots=True, radius=0.05) -> VGroup:
    """A line through (log10 x, log10 y), with dots at the measured points."""
    pts = [ax.c2p(math.log10(x), math.log10(max(y, 1e-12))) for x, y in zip(xs, ys) if np.isfinite(y) and y > 0]
    g = VGroup(VMobject(color=color, stroke_width=stroke_width).set_points_as_corners(pts))
    if dots:
        g.add(*[Dot(p, radius=radius, color=color) for p in pts])
    return g


def bars_chart(values, colors, names, height=3.0, bar_w=0.6, gap=0.35, vmax=None, spread=None, digits=2,
               font_size=20, value_fmt=None) -> VGroup:
    """Static bars with names under them and values over them; ``spread``: (lo, hi) per bar, drawn as a whisker."""
    vals = np.asarray(values, float)
    vmax = vmax or float(np.nanmax(vals if spread is None else np.asarray(spread)[:, 1])) * 1.1
    g = VGroup()
    base = Line(LEFT * 0.1, RIGHT * (len(vals) * (bar_w + gap) - gap + 0.1), color=GREY_C, stroke_width=1.5)
    g.add(base)
    g.bars, g.vals, g.names = VGroup(), VGroup(), VGroup()
    for i, (v, c, n) in enumerate(zip(vals, colors, names)):
        x = i * (bar_w + gap) + bar_w / 2
        h = max(height * v / vmax, 0.01)
        b = Rectangle(width=bar_w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
        b.move_to([x, h / 2, 0])
        g.bars.add(b)
        top = h
        if spread is not None:
            lo, hi = spread[i]
            w = VGroup(Line([x, height * lo / vmax, 0], [x, height * hi / vmax, 0], color=WHITE, stroke_width=1.6),
                       Line([x - 0.08, height * lo / vmax, 0], [x + 0.08, height * lo / vmax, 0], color=WHITE,
                            stroke_width=1.6),
                       Line([x - 0.08, height * hi / vmax, 0], [x + 0.08, height * hi / vmax, 0], color=WHITE,
                            stroke_width=1.6))
            g.add(w)
            top = max(top, height * hi / vmax)
        s = value_fmt(v) if value_fmt else f"{v:.{digits}f}"
        g.vals.add(MathTex(s, font_size=font_size, color=c).move_to([x, top + 0.22, 0]))
        nm = label(n, font_size=font_size - 2, color=GREY_A)
        if nm.width > bar_w + gap - 0.05:
            nm.width = bar_w + gap - 0.05
        g.names.add(nm.next_to([x, 0, 0], DOWN, buff=0.15))
    g.add(g.bars, g.vals, g.names)
    return g


def mean_spread(vals):
    v = np.asarray(vals, float)
    return float(v.mean()), float(v.min()), float(v.max())


def words_num(n: int) -> str:
    """Small counts spoken as words."""
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen"]
    return w[n] if 0 <= n < len(w) else str(n)


def table(rows, col_x, y0, dy=0.5, font_size=24, colors=None) -> VGroup:
    """Rows of Tex cells placed at the x positions col_x (cells centred), from y0 down."""
    g = VGroup()
    for i, r in enumerate(rows):
        row = VGroup()
        for j, cell in enumerate(r):
            m = cell if isinstance(cell, Mobject) else label(cell, font_size=font_size,
                                                             color=(colors[i][j] if colors else WHITE))
            row.add(m.move_to([col_x[j], y0 - i * dy, 0]))
        g.add(row)
    return g


def fmt(x, d=3):
    return f"{x:.{d}f}"


def pct(x):
    return f"{100 * x:.0f}"
