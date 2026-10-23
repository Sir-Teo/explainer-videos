"""Helpers shared by the scenes of Part 24 ("Learning Without Labels")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 24

# one meaning per colour, for the whole part
SUP = "#C9D1D9"  # supervised: trained with the labels
PIX = GREY_B  # raw pixels
RAND = GREY_C  # an untrained encoder
ROT = "#F2A541"  # rotation prediction, pretext tasks
SIMCLR = "#58A6FF"  # SimCLR, the contrastive family
MOCO = "#7C9CF0"  # MoCo
NAIVE = "#FF5C5C"  # the naive siamese net, collapse
SIMSIAM = "#5CD0B3"  # SimSiam
BYOL_C = "#9BE37B"  # BYOL
BARLOW = "#E3A8F0"  # Barlow Twins
VICREG_C = "#C49BFF"  # VICReg
DINO_C = "#F7D154"  # DINO, the teacher
MAE_C = "#FF9F45"  # MAE, masked modelling
BEIT_C = "#FFC98A"  # BEiT
JEPA = "#FF7EB6"  # I-JEPA, JEPA
MATRY = "#7FD3FF"  # Matryoshka embeddings
POS = "#5BD17A"  # the positive pair: two views of one image
NEG = "#EF6A5B"  # negatives
TARGET = GREY_B  # a target branch: stop-gradient, a moving average
STUDENT = "#58A6FF"  # DINO's student
TEACHER = "#F7D154"  # DINO's teacher
MI = C.TRUE_P  # mutual information, the truth
EST = C.MODEL_Q  # an estimate of it
LOGN = GREY_B  # the log N ceiling
HIST = C.HUMAN  # history cards
PANEL = "#121722"
BG = "#0B0F17"

COLOR = {"supervised": SUP, "rotation": ROT, "simclr": SIMCLR, "moco": MOCO, "naive": NAIVE, "simsiam": SIMSIAM,
         "simsiam_nosg": NAIVE, "byol": BYOL_C, "barlow": BARLOW, "vicreg": VICREG_C, "vicreg_novar": NAIVE,
         "dino": DINO_C, "mae": MAE_C, "beit": BEIT_C, "ijepa": JEPA, "matryoshka": MATRY, "supervised_vit": SUP,
         "simclr_vit": SIMCLR, "random_cnn": RAND, "random_vit": RAND, "pixels": PIX}
NAME = {"supervised": r"supervised", "rotation": r"rotation", "simclr": r"SimCLR", "moco": r"MoCo",
        "naive": r"naive siamese", "simsiam": r"SimSiam", "simsiam_nosg": r"SimSiam, no stop-grad", "byol": r"BYOL",
        "barlow": r"Barlow Twins", "vicreg": r"VICReg", "vicreg_novar": r"VICReg, no variance", "dino": r"DINO",
        "mae": r"MAE", "beit": r"BEiT-style", "ijepa": r"I-JEPA", "matryoshka": r"Matryoshka", "supervised_vit":
        r"supervised", "simclr_vit": r"SimCLR", "random_cnn": r"untrained", "random_vit": r"untrained",
        "pixels": r"raw pixels"}
SPOKEN = {"supervised": "the supervised network", "rotation": "rotation prediction", "simclr": "SimCLR",
          "moco": "MoCo", "byol": "BYOL", "simsiam": "SimSiam", "barlow": "Barlow Twins", "vicreg": "VICReg",
          "dino": "DINO", "matryoshka": "the Matryoshka model", "mae": "MAE", "beit": "the BEiT-style model",
          "ijepa": "I-JEPA", "simclr_vit": "SimCLR on the transformer", "supervised_vit": "the supervised transformer",
          "pixels": "raw pixels", "random_cnn": "the untrained network"}
# ten digit classes, ten hues (only on the screens where the labels are shown, never used in training)
DIGIT = ["#FF6B6B", "#FFA94D", "#FFD43B", "#A9E34B", "#51CF66", "#3BC9DB", "#4DABF7", "#748FFC", "#B197FC",
         "#F783AC"]


def rgb_of(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


BG_RGB = rgb_of(BG)


# ---------------------------------------------------------------------------
# Pictures from arrays
# ---------------------------------------------------------------------------
def to_image(rgb: np.ndarray, width: float, height: float | None = None, smooth=False) -> ImageMobject:
    a = np.clip(rgb, 0, 1)
    img = ImageMobject((np.concatenate([a, np.ones(a.shape[:2] + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height if height is not None else width * a.shape[0] / a.shape[1])
    return img


def ink_rgb(q, color=None) -> np.ndarray:
    """A grey-level image (uint8 0..255 or floats in [0, 1]) as RGB: dark background, white (or ``color``) ink."""
    a = np.asarray(q, float)
    a = a / 255.0 if a.max() > 1.0 else a
    a = np.clip(a, 0, 1)
    ink = np.ones(3) if color is None else rgb_of(color)
    return BG_RGB[None, None] * (1 - a[..., None]) + ink[None, None] * a[..., None]


def digit(q, size=1.0, color=None, frame=False) -> Mobject:
    """An image ``size`` tall (its width in proportion)."""
    h, w = np.asarray(q).shape[:2]
    img = to_image(ink_rgb(q, color), size * w / h, size)
    if not frame:
        return img
    return Group(SurroundingRectangle(img, buff=0.03, color=GREY_D, stroke_width=1.2), img)


def digit_sheet(Q, rows, cols, size=0.6, gap=0.06, color=None, colors=None, frame=True) -> Group:
    """Many images as one picture: rows x cols cells; ``colors``: an ink colour per cell."""
    Q = np.asarray(Q)
    h, w = Q.shape[1], Q.shape[2]
    g = max(1, int(round(gap / size * h)))
    H, W = rows * h + (rows - 1) * g, cols * w + (cols - 1) * g
    sheet = np.ones((H, W, 3)) * rgb_of(PANEL)[None, None]
    for k in range(min(len(Q), rows * cols)):
        r, c = divmod(k, cols)
        col = colors[k] if colors is not None else color
        sheet[r * (h + g): r * (h + g) + h, c * (w + g): c * (w + g) + w] = ink_rgb(Q[k], col)
    img = to_image(sheet, cols * size * w / h + (cols - 1) * gap, rows * size + (rows - 1) * gap)
    if not frame:
        return Group(img)
    box = SurroundingRectangle(img, buff=0.06, color=GREY_D, stroke_width=1.2, corner_radius=0.05)
    return Group(box, img)


def heat_rgb(M, vmax=None, signed=True, pos=C.TRUE_P, neg=C.MODEL_Q, gamma=0.8) -> np.ndarray:
    M = np.asarray(M, float)
    v = vmax if vmax is not None else max(np.abs(M).max(), 1e-9)
    t = np.clip(np.abs(M) / v, 0, 1) ** gamma
    cp, cn = rgb_of(pos), rgb_of(neg)
    col = np.where((M >= 0)[..., None] if signed else np.ones(M.shape + (1,), bool), cp[None, None], cn[None, None])
    return BG_RGB[None, None] * (1 - t[..., None]) + col * t[..., None]


def heat(M, width, height=None, **kw) -> ImageMobject:
    M = np.asarray(M)
    return to_image(heat_rgb(M, **kw), width, height if height is not None else width * M.shape[0] / M.shape[1])


# ---------------------------------------------------------------------------
# The hypersphere: unit vectors in three numbers, turning
# ---------------------------------------------------------------------------
class Hypersphere(Group):
    """Points on the unit sphere S^2, drawn by projection after turning by ``self.angle`` (radians, about the vertical
    axis) and tilting by ``self.tilt``: a wire sphere (outline, equator and two meridians, their far halves dim) and
    one dot per point, nearer dots larger and brighter. ``self.t`` (a ValueTracker) scrubs through snapshots
    ``frames`` (n_snap, n, 3) of the points, renormalized in between; ``colors`` one per point."""

    def __init__(self, frames, colors, radius=2.4, center=ORIGIN, dot=0.045, tilt=0.35, wire=GREY_D):
        super().__init__()
        F_ = np.asarray(frames, float)
        if F_.ndim == 2:
            F_ = F_[None]
        self.frames = F_ / np.maximum(np.linalg.norm(F_, axis=-1, keepdims=True), 1e-9)
        self.R, self.c, self.dotr = radius, np.asarray(center, float), dot
        self.angle, self.tilt, self.t = ValueTracker(0.0), ValueTracker(tilt), ValueTracker(0.0)
        self.outline = Circle(radius=radius, stroke_color=wire, stroke_width=2).move_to(center)
        self.wire = always_redraw(self._wire)
        cols = [ManimColor(c) for c in colors]
        self.dots = VGroup(*[Dot(radius=dot, color=c) for c in cols])
        self._dl = list(self.dots.submobjects)
        self.dots.add_updater(self._place)
        self.add(self.outline, self.wire, self.dots)
        self._place(self.dots)

    def _rot(self, P):
        a, t = self.angle.get_value(), self.tilt.get_value()
        x, y, z = P[..., 0], P[..., 1], P[..., 2]
        x, z = x * np.cos(a) + z * np.sin(a), -x * np.sin(a) + z * np.cos(a)
        y, z = y * np.cos(t) - z * np.sin(t), y * np.sin(t) + z * np.cos(t)
        return np.stack([x, y, z], -1)

    def points_now(self) -> np.ndarray:
        t = self.t.get_value()
        k = int(np.clip(np.floor(t), 0, len(self.frames) - 1))
        f = t - k
        P = self.frames[k] if k + 1 >= len(self.frames) or f <= 0 else \
            (1 - f) * self.frames[k] + f * self.frames[k + 1]
        return P / np.maximum(np.linalg.norm(P, axis=-1, keepdims=True), 1e-9)

    def _place(self, dots):
        Q = self._rot(self.points_now())
        for d, q in zip(self._dl, Q):
            k = 0.7 + 0.45 * (q[2] + 1) / 2
            d.set(width=2 * self.dotr * k)
            d.move_to(self.c + self.R * np.array([q[0], q[1], 0.0]))
            d.set_opacity(0.25 + 0.75 * (q[2] + 1) / 2)
        dots.submobjects = [self._dl[i] for i in np.argsort(Q[:, 2])]  # nearer dots drawn last
        return dots

    def _circle_pts(self, kind, n=90):
        s = np.linspace(0, 2 * np.pi, n)
        if kind == "eq":
            P = np.stack([np.cos(s), np.zeros_like(s), np.sin(s)], 1)
        elif kind == "m1":
            P = np.stack([np.zeros_like(s), np.cos(s), np.sin(s)], 1)
        else:
            P = np.stack([np.cos(s), np.sin(s), np.zeros_like(s)], 1)
        return self._rot(P)

    def _wire(self):
        g = VGroup()
        for kind in ("eq", "m1", "m2"):
            Q = self._circle_pts(kind)
            for front in (True, False):
                seg = VMobject(stroke_color=GREY_C if front else GREY_D, stroke_width=1.4 if front else 0.8,
                               stroke_opacity=0.7 if front else 0.35)
                pts = [self.c + self.R * np.array([q[0], q[1], 0]) for q in Q]
                mask = (Q[:, 2] >= 0) == front
                # draw the runs of consecutive points on this side
                run = []
                for p, m_ in zip(pts, mask):
                    if m_:
                        run.append(p)
                    elif len(run) > 1:
                        seg.start_new_path(run[0])
                        seg.add_points_as_corners(run[1:])
                        run = []
                    else:
                        run = []
                if len(run) > 1:
                    seg.start_new_path(run[0])
                    seg.add_points_as_corners(run[1:])
                g.add(seg)
        return g

    def freeze(self):
        for m in self.get_family():
            m.clear_updaters()
        return self


# ---------------------------------------------------------------------------
# Cards, boxes and charts
# ---------------------------------------------------------------------------
def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=width or (t.width + 2 * pad), height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def arrow(a, b, color=GREY_B, buff=0.08, stroke_width=2.5, **kw) -> Arrow:
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke_width, max_tip_length_to_length_ratio=0.18, **kw)


def tag(text: str, corner=DR, font_size=20) -> Tex:
    return note(text, font_size=font_size).to_corner(corner, buff=0.25)


def take_away(text: str, color=C.BITS, font_size=28, width=12.0) -> VGroup:
    """The chapter's takeaway: a line in a soft box at the bottom of the frame."""
    t = wrapped_label(text, width, font_size, color)
    box = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.35, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.5, fill_color=BG, fill_opacity=0.92)
    return VGroup(box, t.move_to(box)).to_edge(DOWN, buff=0.35)


def bars_chart(values, colors, names, height=3.0, bar_w=0.6, gap=0.35, vmin=0.0, vmax=None, spread=None, digits=1,
               font_size=20, value_fmt=None, name_size=None) -> VGroup:
    """Bars with names under them and values over them; ``spread``: (lo, hi) per bar, a whisker; bars start at
    ``vmin`` (a zoomed axis)."""
    vals = np.asarray(values, float)
    top_v = vmax or float(np.nanmax(vals if spread is None else np.asarray(spread)[:, 1])) * 1.05
    H = lambda v: height * (v - vmin) / (top_v - vmin)  # noqa: E731
    g = VGroup()
    base = Line(LEFT * 0.1, RIGHT * (len(vals) * (bar_w + gap) - gap + 0.1), color=GREY_C, stroke_width=1.5)
    g.add(base)
    g.bars, g.vals, g.names, g.whiskers = VGroup(), VGroup(), VGroup(), VGroup()
    for i, (v, c, n) in enumerate(zip(vals, colors, names)):
        x = i * (bar_w + gap) + bar_w / 2
        h = max(H(v), 0.01)
        b = Rectangle(width=bar_w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x, h / 2, 0])
        g.bars.add(b)
        top = h
        if spread is not None:
            lo, hi = spread[i]
            w = VGroup(Line([x, H(lo), 0], [x, H(hi), 0], color=WHITE, stroke_width=1.6),
                       Line([x - 0.08, H(lo), 0], [x + 0.08, H(lo), 0], color=WHITE, stroke_width=1.6),
                       Line([x - 0.08, H(hi), 0], [x + 0.08, H(hi), 0], color=WHITE, stroke_width=1.6))
            g.whiskers.add(w)
            top = max(top, H(hi))
        s = value_fmt(v) if value_fmt else f"{v:.{digits}f}"
        g.vals.add(MathTex(s, font_size=font_size, color=c).move_to([x, top + 0.22, 0]))
        nm = label(n, font_size=name_size or font_size - 2, color=GREY_A)
        if nm.width > bar_w + gap - 0.05:
            nm.width = bar_w + gap - 0.05
        g.names.add(nm.next_to([x, 0, 0], DOWN, buff=0.15))
    g.add(g.bars, g.whiskers, g.vals, g.names)
    return g


def mmm(v) -> tuple[float, float, float]:
    v = np.asarray(v, float)
    return float(v.mean()), float(v.min()), float(v.max())


def pct(x: float, d: int = 1) -> str:
    return f"{100 * x:.{d}f}"


def words_num(n: int) -> str:
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen"]
    return w[n] if 0 <= n < len(w) else str(n)


def mini_axes(xmax, ymin, ymax, w=3.0, h=1.8) -> Axes:
    return Axes(x_range=[0, xmax, xmax], y_range=[ymin, ymax, ymax - ymin], x_length=w, y_length=h, tips=False,
                axis_config={"stroke_color": GREY_D, "include_ticks": False})


def seed_curves(ax, runs, keys, field, color, stroke_width=2.5, x="steps", fn=None) -> VGroup:
    """One thin line per seed of a run field (a band of curves)."""
    g = VGroup()
    for i, k in enumerate(keys):
        xs = np.asarray(runs[k][x], float)
        ys = np.asarray(runs[k][field], float)
        if fn is not None:
            ys = fn(ys)
        ok = np.isfinite(ys)
        g.add(curve(ax, xs[ok], ys[ok], color, stroke_width if i == 0 else stroke_width * 0.6).set_stroke(
            opacity=1.0 if i == 0 else 0.55))
    return g


def run_finals(runs: dict, keys, field="linear") -> np.ndarray:
    return np.array([runs[k]["final"][field] for k in keys], float)
