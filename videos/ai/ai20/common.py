"""Helpers shared by the scenes of Part 20 ("Four Ways to Generate")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 20
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
DATA = C.TRUE_P  # the data, p, real digits
AR = "#5CD0B3"  # autoregressive models (PixelCNN)
VAE_C = "#B39DDB"  # VAEs
GAN_C = "#FF6B8B"  # GANs, the generator
DISC = "#7C9CF0"  # the discriminator / critic
WGAN_C = "#FFB070"  # WGAN-GP
FLOW = "#9BE37B"  # normalizing flows
CNF_C = "#D9F27B"  # continuous flows, neural ODEs
EBM = "#F2A541"  # energy-based models, energies E
VQ_C = "#D4A5FF"  # VQ-VAE, codes and tokens
LATENT = "#E3A8F0"  # the latent code z
RECON = C.INTERVAL  # reconstruction terms
KLC = C.KL  # KL terms, the rate
SCORE_C = C.SCORE  # the score, gradients of log p
NOISE = GREY_B  # noise, the base distribution
HIST = C.HUMAN  # history cards
PANEL = "#121722"

FAM = {"pixelcnn": AR, "ar": AR, "vae": VAE_C, "gan": GAN_C, "wgan": WGAN_C, "flow": FLOW, "cnf": CNF_C, "ebm": EBM,
       "vq": VQ_C, "real": DATA}
FAM_NAME = {"pixelcnn": r"PixelCNN", "ar": r"autoregressive", "vae": r"VAE", "gan": r"GAN", "wgan": r"WGAN-GP",
            "flow": r"RealNVP", "cnf": r"neural ODE", "ebm": r"energy model", "vq": r"VQ-VAE + prior",
            "real": r"real digits"}

COLORS = {r"x": DATA, r"z": LATENT, r"p": DATA, r"q": C.MODEL_Q, r"D": DISC, r"G": GAN_C, r"E": EBM}

BOX = 3.0  # the 2D plane: [-BOX, BOX]^2


def rgb_of(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


BG_RGB = rgb_of("#0B0F17")


# ---------------------------------------------------------------------------
# Pictures from arrays
# ---------------------------------------------------------------------------
def to_image(rgb: np.ndarray, width: float, height: float | None = None, smooth=False) -> ImageMobject:
    """An (h, w, 3) array in [0, 1] as an ImageMobject, rows top to bottom."""
    a = np.clip(rgb, 0, 1)
    img = ImageMobject((np.concatenate([a, np.ones(a.shape[:2] + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height if height is not None else width * a.shape[0] / a.shape[1])
    return img


def digit_rgb(q, color=None) -> np.ndarray:
    """A 14 x 14 digit (levels 0..15, or values in [0, 1]) as RGB: dark background, white (or ``color``) ink."""
    a = np.asarray(q, float)
    a = a / 15.0 if a.max() > 1.0 else a
    ink = np.ones(3) if color is None else rgb_of(color)
    return BG_RGB[None, None] * (1 - a[..., None]) + ink[None, None] * a[..., None]


def digit(q, size=1.0, color=None) -> ImageMobject:
    return to_image(digit_rgb(q, color), size, size)


def digit_sheet(Q, rows, cols, size=0.6, gap=0.06, color=None, frame=True) -> Group:
    """Many digits as one picture (one image is much cheaper to draw than many): rows x cols cells."""
    Q = np.asarray(Q)
    px = 14
    g = max(1, int(round(gap / size * px)))
    H, W = rows * px + (rows - 1) * g, cols * px + (cols - 1) * g
    sheet = np.ones((H, W, 3)) * rgb_of(PANEL)[None, None]
    for k in range(min(len(Q), rows * cols)):
        r, c = divmod(k, cols)
        sheet[r * (px + g): r * (px + g) + px, c * (px + g): c * (px + g) + px] = digit_rgb(Q[k], color)
    img = to_image(sheet, cols * size + (cols - 1) * gap, rows * size + (rows - 1) * gap)
    if not frame:
        return Group(img)
    box = SurroundingRectangle(img, buff=0.06, color=GREY_D, stroke_width=1.2, corner_radius=0.05)
    return Group(box, img)


def density_rgb(Dn, color, gamma=0.55, vmax=None) -> np.ndarray:
    """A density on the grid (rows = y from -BOX up) as a glow of ``color`` on the dark background."""
    Dn = np.asarray(Dn, float)
    v = vmax if vmax is not None else max(np.percentile(Dn, 99.7), 1e-12)
    t = np.clip(Dn / v, 0, 1) ** gamma
    col = rgb_of(color)
    return (BG_RGB[None, None] * (1 - t[..., None]) + col[None, None] * t[..., None])[::-1]


class Plane(VGroup):
    """A square panel showing [-BOX, BOX]^2: ``p(x, y)`` maps data coordinates to the scene."""

    def __init__(self, side=3.6, center=ORIGIN, box=BOX, color=GREY_D, axes_lines=False):
        super().__init__()
        self.side, self.box = side, box
        self.frame = Square(side, color=color, stroke_width=1.2).move_to(center)
        self.add(self.frame)
        if axes_lines:
            c = self.frame.get_center()
            self.add(Line(c + LEFT * side / 2, c + RIGHT * side / 2, color=GREY_D, stroke_width=0.8).set_opacity(0.5),
                     Line(c + DOWN * side / 2, c + UP * side / 2, color=GREY_D, stroke_width=0.8).set_opacity(0.5))

    def p(self, x, y=None):
        if y is None:
            x, y = x
        c = self.frame.get_center()
        s = self.side / (2 * self.box)
        return np.array([c[0] + x * s, c[1] + y * s, 0.0])

    def pts(self, P) -> np.ndarray:
        P = np.asarray(P, float)
        c = self.frame.get_center()
        s = self.side / (2 * self.box)
        return np.c_[c[0] + P[:, 0] * s, c[1] + P[:, 1] * s, np.zeros(len(P))]

    def image(self, Dn, color, gamma=0.55, vmax=None) -> ImageMobject:
        img = to_image(density_rgb(Dn, color, gamma, vmax), self.side, self.side, smooth=True)
        return img.move_to(self.frame.get_center())

    def scatter_image(self, P, color, radius_px=1.6, res=360, alpha=0.85, base=None) -> ImageMobject:
        """Points drawn into a picture (thousands of points at the cost of one image)."""
        P = np.asarray(P, float)
        img = np.zeros((res, res, 3)) + (BG_RGB if base is None else 0)
        if base is not None:
            img = base.copy()
        col = rgb_of(color)
        u = ((P[:, 0] + self.box) / (2 * self.box) * (res - 1))
        v = ((self.box - P[:, 1]) / (2 * self.box) * (res - 1))
        rr = int(np.ceil(radius_px))
        yy, xx = np.mgrid[-rr:rr + 1, -rr:rr + 1]
        disk = (xx ** 2 + yy ** 2) <= radius_px ** 2
        for a, b in zip(np.round(u).astype(int), np.round(v).astype(int)):
            x0, x1, y0, y1 = a - rr, a + rr + 1, b - rr, b + rr + 1
            if x0 < 0 or y0 < 0 or x1 > res or y1 > res:
                continue
            sub = img[y0:y1, x0:x1]
            sub[disk] = (1 - alpha) * sub[disk] + alpha * col
        return to_image(img, self.side, self.side, smooth=True).move_to(self.frame.get_center())

    def dots(self, P, color, radius=0.025, opacity=0.9) -> VGroup:
        return VGroup(*[Dot(q, radius=radius, color=color, fill_opacity=opacity) for q in self.pts(P)])


def move_dots(dots: VGroup, plane: Plane, P) -> list:
    return [d.animate.move_to(q) for d, q in zip(dots, plane.pts(P))]


def place_dots(dots: VGroup, plane: Plane, P) -> None:
    for d, q in zip(dots, plane.pts(P)):
        d.move_to(q)


def polyline(plane: Plane, P, color, stroke_width=2.0) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=stroke_width).set_points_as_corners(plane.pts(P))


def arrows(plane: Plane, pts, vecs, color=SCORE_C, max_len=0.38, stroke_width=2.2, floor=0.04) -> VGroup:
    """Little arrows of a 2D vector field (lengths compressed, so strong ones don't swamp the rest)."""
    g = VGroup()
    V = np.asarray(vecs, float)
    mag = np.linalg.norm(V, axis=1)
    top = max(np.percentile(mag, 95), 1e-9)
    for p, v, m in zip(plane.pts(pts), V, mag):
        L = max_len * min(m / top, 1.0) ** 0.6
        if L < floor:
            continue
        d = v / max(m, 1e-9)
        g.add(Arrow(p, p + L * np.array([d[0], d[1], 0]), buff=0, color=color, stroke_width=stroke_width,
                    max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
    return g


# ---------------------------------------------------------------------------
# Cards and small diagrams
# ---------------------------------------------------------------------------
def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=width or (t.width + 2 * pad), height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def tag(text: str, corner=DR, font_size=20) -> Tex:
    return note(text, font_size=font_size).to_corner(corner, buff=0.25)


def caption(mob: Mobject, text: str, color=GREY_A, font_size=22, direction=UP, buff=0.15) -> Tex:
    return label(text, font_size=font_size, color=color).next_to(mob, direction, buff=buff)


def take_away(text: str, color=C.BITS, font_size=28, width=12.0) -> VGroup:
    """The chapter's takeaway: a line in a soft box at the bottom of the frame."""
    t = wrapped_label(text, width, font_size, color)
    box = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.35, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.92)
    return VGroup(box, t.move_to(box)).to_edge(DOWN, buff=0.35)


def bars_chart(values, colors, names, height=3.0, bar_w=0.6, gap=0.35, vmax=None, spread=None, digits=1,
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
        g.names.add(nm.move_to([x, -0.25, 0]))
    g.add(g.bars, g.vals, g.names)
    return g


def stack_label(lines, font_size=24, color=WHITE, buff=0.18) -> VGroup:
    return VGroup(*[label(t, font_size=font_size, color=color) for t in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=buff)


def check_mark(ok: bool, size=0.3) -> Mobject:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=36 if ok else 40,
                   color=C.INTERVAL if ok else GREY_C)


def mean_spread(vals):
    v = np.asarray(vals, float)
    return float(v.mean()), float(v.min()), float(v.max())


def words_num(n: int) -> str:
    """Small counts spoken as words (the narrator reads 'three seeds' better than '3 seeds')."""
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen"]
    return w[n] if 0 <= n < len(w) else str(n)
