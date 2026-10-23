"""Helpers shared by the scenes of Part 10 ("Seeing and Remembering").

Pictures of arrays (digits, photographs, filters, feature maps, alignments) are drawn as ``ImageMobject``s from the
cached numbers; ``img_gray``, ``img_rgb``, ``img_filter`` and ``img_heat`` are written to stand alone, so they could
move to ``explainer/ai/viz.py`` unchanged.
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 10
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
KERNEL = C.BITS  # a kernel / filter and what it touches
FMAP = C.TRUE_P  # feature maps, activations
CNN = C.NEURAL  # our convolutional networks and their results
MLPC = C.MODEL_Q  # the fully connected network (MLP) it is compared with
HAND = C.COUNTING  # hand-made features: edges, SIFT, HOG
GRADC = C.SURPRISE  # gradients flowing back
ADV = C.PENALTY  # adversarial perturbations, attacks
OK = C.REWARD  # right answers
HIST = C.HUMAN  # people and history
RNNC, LSTMC, GRUC, MINC = "#F2A541", C.NEURAL, C.TRUE_P, C.INTERVAL  # the four recurrent cells
CELLC = C.BITS  # the LSTM's cell state: the memory line
GATEC = C.CONTEXT  # gates
ATT = C.ATTN  # attention weights
ACTC = {"relu": C.NEURAL, "tanh": C.TRUE_P, "sigmoid": C.MODEL_Q}
CELLS = {"rnn": RNNC, "lstm": LSTMC, "gru": GRUC, "mingru": MINC}
CELL_NAME = {"rnn": r"RNN", "lstm": r"LSTM", "gru": r"GRU", "mingru": r"minGRU"}
DARK = "#141A24"


def rgb(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


def _image(a: np.ndarray, width: float, height: float | None, smooth: bool) -> ImageMobject:
    a = np.clip(a, 0, 1)
    img = ImageMobject((np.concatenate([a, np.ones(a.shape[:2] + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height if height is not None else width * a.shape[0] / a.shape[1])
    return img


def img_rgb(arr, width: float, height: float | None = None, smooth=False) -> ImageMobject:
    """An (H, W, 3) array (floats in [0, 1], or uint8) as a picture of the given width."""
    a = np.asarray(arr)
    a = a / 255.0 if a.dtype == np.uint8 else a.astype(float)
    return _image(a, width, height, smooth)


def img_gray(arr, width: float, lo=None, hi=None, color=WHITE, bg=DARK, smooth=False) -> ImageMobject:
    """A greyscale array drawn from ``bg`` (low) to ``color`` (high)."""
    a = np.asarray(arr, float)
    if a.max() > 1.5 and lo is None:
        a = a / 255.0
    lo = a.min() if lo is None else lo
    hi = a.max() if hi is None else hi
    t = np.clip((a - lo) / max(hi - lo, 1e-9), 0, 1)[..., None]
    return _image(rgb(bg) * (1 - t) + rgb(color) * t, width, None, smooth)


NEG, POS = "#3D7FE0", "#F2C14E"


def img_heat(arr, width: float, sym=True, neg=NEG, pos=POS, mid="#0B0F17", height=None, smooth=False,
             vmax=None) -> ImageMobject:
    """A signed array: blue for negative, dark at zero, gold for positive (or dark to gold if ``sym`` is False)."""
    a = np.asarray(arr, float)
    m = vmax or (np.abs(a).max() if sym else a.max()) or 1.0
    if sym:
        t = np.clip(a / m, -1, 1)[..., None]
        out = np.where(t >= 0, rgb(mid) * (1 - t) + rgb(pos) * t, rgb(mid) * (1 + t) + rgb(neg) * (-t))
    else:
        t = np.clip((a - min(a.min(), 0)) / max(m - min(a.min(), 0), 1e-9), 0, 1)[..., None]
        out = rgb(mid) * (1 - t) + rgb(pos) * t
    return _image(out, width, height, smooth)


def img_filter(w, width: float) -> ImageMobject:
    """A first-layer filter as a picture: a colour filter (3, k, k) scaled about mid-grey, as in Krizhevsky et al.'s
    figure; a grey filter (k, k) as a signed heat map."""
    w = np.asarray(w, float)
    if w.ndim == 3:
        a = w.transpose(1, 2, 0)
        a = 0.5 + 0.5 * a / (np.abs(a).max() + 1e-9)
        return _image(a, width, None, False)
    return img_heat(w, width)


def framed(m: Mobject, color=GREY_D, buff=0.0, width=1.2) -> Group:
    return Group(m, SurroundingRectangle(m, buff=buff, color=color, stroke_width=width))


def grid_of(mobs, cols: int, buff=0.08) -> Group:
    g = Group(*mobs)
    g.arrange_in_grid(cols=cols, buff=buff)
    return g


def pct(x: float, digits: int = 1) -> str:
    return f"{100 * x:.{digits}f}"


def box_label(text: str, color, width=None, height=0.62, font_size=24, fill=0.12) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    w = width or (t.width + 0.44)
    box = RoundedRectangle(width=w, height=max(height, t.height + 0.25), corner_radius=0.12, stroke_color=color,
                           stroke_width=2.2, fill_color=color, fill_opacity=fill)
    g = VGroup(box, t.move_to(box))
    g.box, g.text = box, t
    return g


def hbars(values, labels, colors, width=6.0, height=0.38, font_size=22, vmax=None, fmt=None, gap=0.22,
          label_width=None) -> VGroup:
    """Horizontal bars: a label on the left, a bar, the value on the right (``fmt`` gives its TeX)."""
    fmt = fmt or (lambda v: f"{v:.1f}")
    vals = np.asarray(values, float)
    vmax = vmax or float(vals.max())
    names = [label(t, font_size=font_size, color=c) for t, c in zip(labels, colors)]
    lw = label_width or max(n.width for n in names)
    rows = VGroup()
    for i, (v, nm, col) in enumerate(zip(vals, names, colors)):
        y = -i * (height + gap)
        nm.move_to([-lw - 0.2 + (lw - nm.width) + nm.width / 2, y, 0])
        w = max(width * v / vmax, 0.02)
        bar = Rectangle(width=w, height=height, stroke_width=0, fill_color=col, fill_opacity=0.85)
        bar.move_to([w / 2, y, 0])
        val = MathTex(fmt(v), font_size=font_size + 2, color=col).next_to(bar, RIGHT, buff=0.15)
        r = VGroup(nm, bar, val)
        r.name, r.bar, r.value = nm, bar, val
        rows.add(r)
    return rows


def seed_band(ax, xs, runs, color, opacity=0.18, stroke_width=3.5):
    """Mean curve over seeds with the min-max band around it."""
    R = np.asarray(runs, float)
    return VGroup(band(ax, xs, R.min(0), R.max(0), color, opacity), curve(ax, xs, R.mean(0), color, stroke_width))


def tile(m: Mobject, caption: str, color, TW=3.0, TH=2.0) -> Group:
    box, cap = tile_frame(caption, color, TW, TH)
    m.move_to(box.get_center() + UP * 0.22)
    if m.width > TW:
        m.width = TW
    if m.height > TH:
        m.height = TH
    return Group(box, m, cap)


def spoken_pct(x: float, digits: int = 1) -> str:
    """0.0123 -> '1.2 percent' for the narration."""
    return f"{100 * x:.{digits}f} percent"


def nn_layer_boxes(widths, heights, colors, buff=0.35, depth=0.25) -> VGroup:
    """A schematic stack of feature-map volumes (a box per layer, front face and a little depth)."""
    g = VGroup()
    for w, h, c in zip(widths, heights, colors):
        front = Rectangle(width=w, height=h, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.18)
        top = Polygon(front.get_corner(UL), front.get_corner(UL) + np.array([depth, depth, 0]),
                      front.get_corner(UR) + np.array([depth, depth, 0]), front.get_corner(UR), stroke_color=c,
                      stroke_width=1.2, fill_color=c, fill_opacity=0.1)
        side = Polygon(front.get_corner(UR), front.get_corner(UR) + np.array([depth, depth, 0]),
                       front.get_corner(DR) + np.array([depth, depth, 0]), front.get_corner(DR), stroke_color=c,
                       stroke_width=1.2, fill_color=c, fill_opacity=0.06)
        g.add(VGroup(front, top, side))
    g.arrange(RIGHT, buff=buff)
    return g


def sci_tex(v: float, digits: int = 0) -> str:
    """3.2e-8 -> '3 \\times 10^{-8}' for MathTex; 0 -> '0'."""
    if v == 0:
        return "0"
    import math as _m

    e = int(_m.floor(_m.log10(abs(v))))
    m = v / 10 ** e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f} \times 10^{{{e}}}"


def oriented_fit(K) -> tuple[float, int]:
    """How much a 5x5 kernel looks like a bar or an edge through its centre: the best correlation with either
    template over angles 0, 5, ..., 175 degrees, and that angle."""
    Kc = np.asarray(K, float) - np.mean(K)
    yy, xx = np.mgrid[0:5, 0:5] - 2.0
    best, at = 0.0, 0
    for deg in range(0, 180, 5):
        t = np.deg2rad(deg)
        d = xx * np.sin(t) + yy * np.cos(t)
        for T in (np.exp(-d ** 2 / 1.28), np.tanh(d / 0.8)):
            T = T - T.mean()
            c = abs(float((T * Kc).sum() / np.sqrt((T ** 2).sum() * (Kc ** 2).sum() + 1e-12)))
            if c > best:
                best, at = c, deg
    return best, at
