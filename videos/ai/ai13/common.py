"""Helpers shared by the scenes of Part 13 ("Attention as Geometry").  Parts 15 and 30 import ``heat_image`` and
``signed_image`` from here."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 13
MONO = "DejaVu Sans Mono"
Q, K, V, A = C.QUERY, C.KEY, C.VALUE, C.ATTN
POS = C.POSITION
OURS = C.NEURAL  # our transformer on the scoreboard
HIST = C.HUMAN  # history cards
MLPC = C.MLP
SINKC = C.SINK
GATEC = C.BITS
DIFFC = "#7FD3FF"
NORMC = C.INTERVAL
CAPC = C.TRUE_P
PANEL = "#121722"

# one colour per position scheme, for the whole part
POS_COLORS = {"sin": "#9BE37B", "rope": POS, "alibi": "#58A6FF", "nope": GREY_B}
POS_NAMES = {"sin": r"sinusoidal", "rope": r"RoPE", "alibi": r"ALiBi", "nope": r"no positions"}
# and one per way of getting past the training length
EXT_COLORS = {"plain": C.SURPRISE, "pi": C.TRUE_P, "ntk": C.INTERVAL, "yarn": C.BITS, "logn": "#B48EF0",
              "ntk_logn": "#7FD3FF", "window": GREY_B}
EXT_NAMES = {"plain": r"rotations as trained", "pi": r"position interpolation", "ntk": r"NTK-aware",
             "yarn": r"YaRN", "logn": r"$\log n$ scaling", "ntk_logn": r"NTK-aware $+ \log n$",
             "window": r"just the last $256$"}
SINK_COLORS = {"softmax": A, "sink": SINKC, "gate": GATEC, "diff": DIFFC}
SINK_NAMES = {"softmax": r"plain softmax", "sink": r"a sink logit", "gate": r"an output gate",
              "diff": r"differential"}


def heat_image(M, width, height, color=A, gamma=0.5, mask_upper=False) -> ImageMobject:
    """A matrix as a picture: dark for 0, ``color`` for the largest entry; ``gamma`` < 1 lifts the small ones.
    With ``mask_upper``, entries above the diagonal (the future, for causal attention) are drawn darker still."""
    M = np.asarray(M, float)
    v = np.clip(M / max(M.max(), 1e-12), 0, 1) ** gamma
    c = np.array(ManimColor(color).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + c[None, None] * v[..., None]
    if mask_upper:
        up = np.triu(np.ones(M.shape, bool), 1)
        rgb[up] = np.array(ManimColor("#080B11").to_rgb())
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def signed_image(M, width, height, pos=C.TRUE_P, neg=C.SURPRISE) -> ImageMobject:
    """A signed matrix as a picture: blue for positive, red for negative, dark for zero."""
    M = np.asarray(M, float)
    s = np.clip(M / max(np.abs(M).max(), 1e-12), -1, 1)
    bg = np.array(ManimColor("#121722").to_rgb())
    cp, cn = np.array(ManimColor(pos).to_rgb()), np.array(ManimColor(neg).to_rgb())
    a = np.abs(s)[..., None]
    rgb = bg * (1 - a) + np.where(s[..., None] > 0, cp, cn) * a
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def pattern_image(x, side, width, ink=WHITE, paper="#1B2230") -> ImageMobject:
    """A +1/-1 pattern (a stored letter) as a side x side picture."""
    a = (np.asarray(x, float).reshape(side, side) > 0)[..., None]
    rgb = np.where(a, np.array(ManimColor(ink).to_rgb()), np.array(ManimColor(paper).to_rgb()))
    img = ImageMobject((np.concatenate([rgb, np.ones((side, side, 1))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(width)


def framed(img, color=GREY_D, sw=1.2) -> Group:
    return Group(img, SurroundingRectangle(img, buff=0, color=color, stroke_width=sw))


def char_row(text: str, width: float, font_size=26, color=GREY_A) -> VGroup:
    """One glyph per character, evenly spaced across ``width`` (spaces shown as a dim dot)."""
    step = width / len(text)
    g = VGroup()
    for i, ch in enumerate(text):
        if ch == " ":
            m = Dot(radius=0.025, color=GREY_D)
        elif ch == "\n":
            m = Text("/", font=MONO, font_size=font_size, color=GREY_D)
        else:
            m = data_text(ch, font=MONO, font_size=font_size, color=color)
        g.add(m.move_to([-width / 2 + step * (i + 0.5), 0, 0]))
    return g


def attention_arcs(row: VGroup, i: int, weights, color=A, max_width=12, floor=0.02, up=True) -> VGroup:
    """Arcs from character ``i`` back to each earlier character, as thick as the attention weight."""
    w = np.asarray(weights, float)
    arcs = VGroup()
    top = max(w[: i + 1].max(), 1e-9)
    for j in range(i):
        if w[j] < floor * top:
            continue
        a, b = row[i].get_top() if up else row[i].get_bottom(), row[j].get_top() if up else row[j].get_bottom()
        a, b = a + (UP if up else DOWN) * 0.08, b + (UP if up else DOWN) * 0.08
        ang = -PI / 2.2 if up else PI / 2.2
        arcs.add(ArcBetweenPoints(a, b, angle=ang, stroke_width=1 + max_width * w[j] / top, color=color)
                 .set_stroke(opacity=float(0.25 + 0.75 * w[j] / top)))
    return arcs


LN_VEC = np.array([4.2, 1.0, 5.0, 0.6, 3.4, 1.8])  # one illustrative vector


def layernorm_picture(unit=0.3) -> VGroup:
    """A jargon-card picture of layer normalization: VGroup(the zero line, the band of spread one, a vector's numbers
    as bars).  ``layernorm_stage(pic, 1)`` is the same vector shifted to average zero, ``layernorm_stage(pic, 2)``
    also squashed to spread one, both rebuilt on the picture wherever it now is."""
    w = 0.5 * len(LN_VEC)
    zl = DashedLine([-0.35, 0, 0], [w - 0.15, 0, 0], color=GREY_B, stroke_width=1.5)
    band_ = VGroup(*[DashedLine([-0.35, s * unit, 0], [w - 0.15, s * unit, 0], color=C.TRUE_P, stroke_width=1.2,
                                dash_length=0.06) for s in (1, -1)])
    bars = VGroup(*[Rectangle(width=0.32, height=max(abs(u) * unit, 0.01), stroke_width=0, fill_color=C.EMBED,
                              fill_opacity=0.85).move_to([0.5 * i, u * unit / 2, 0]) for i, u in enumerate(LN_VEC)])
    return VGroup(zl, band_, bars)


def layernorm_stage(pic: VGroup, stage: int) -> VGroup:
    zl, band_, bars = pic
    y0 = zl.get_y()
    unit = band_[0].get_y() - y0
    v = LN_VEC - LN_VEC.mean()
    if stage >= 2:
        v = v / LN_VEC.std()
    return VGroup(*[Rectangle(width=b.width, height=max(abs(u) * unit, 0.01), stroke_width=0, fill_color=C.TRUE_P,
                              fill_opacity=0.85).move_to([b.get_x(), y0 + u * unit / 2, 0]) for b, u in zip(bars, v)])


SM_SCORES = np.array([1.2, -0.5, 0.4, -1.0, 0.8])  # illustrative scores
SM_STAGES = (r"scores", r"$e^{\,\mathrm{score}}$: \ all positive", r"divided by the total: \\ they add up to $1$")


def softmax_picture(unit=0.5) -> VGroup:
    """A jargon-card picture of the softmax: VGroup(zero line, bars, caption).  ``softmax_stage(pic, k)`` gives
    (bars, caption) for stage k: 0 the raw scores, 1 their exponentials, 2 those divided by their total."""
    zl = Line([-0.3, 0, 0], [0.45 * len(SM_SCORES) - 0.15, 0, 0], color=GREY_C, stroke_width=1.5)
    bars = _sm_bars(SM_SCORES, [0.45 * i for i in range(len(SM_SCORES))], 0.0, unit, 0.3, A)
    cap = label(SM_STAGES[0], font_size=18, color=GREY_A).next_to(zl, DOWN, buff=0.6)
    box = Rectangle(width=zl.get_length(), height=1.75 * unit, stroke_width=0, fill_opacity=0).next_to(zl, UP, buff=0)
    return VGroup(zl, bars, cap, box)  # (an invisible box keeps room for the tallest bars)


def _sm_bars(vals, xs, y0, unit, w, color):
    return VGroup(*[Rectangle(width=w, height=max(abs(float(v)) * unit, 0.01), stroke_width=0, fill_color=color,
                              fill_opacity=0.9 if v >= 0 else 0.45).move_to([x, y0 + float(v) * unit / 2, 0])
                    for x, v in zip(xs, vals)])


def softmax_stage(pic: VGroup, k: int) -> tuple[VGroup, Mobject]:
    zl, bars, cap, box = pic
    unit = box.height / 1.75
    e = np.exp(SM_SCORES)
    vals = SM_SCORES if k == 0 else 0.5 * e if k == 1 else 3.0 * e / e.sum()
    nb = _sm_bars(vals, [b.get_x() for b in bars], zl.get_y(), unit, bars[0].width, A)
    nc = label(SM_STAGES[k], font_size=18, color=GREY_A).scale(zl.get_length() / 2.4)  # as the picture was scaled
    if nc.width > zl.get_length() + 0.4:  # never wider than the picture it captions
        nc.scale_to_fit_width(zl.get_length() + 0.4)
    return nb, nc.move_to(cap)


def bars_chart(values, colors, width=4.0, height=2.0, base_y=0.0, x0=0.0, gap=0.25, vmax=None, labels=None,
               font_size=18, fmt="{:.2f}", spread=None) -> VGroup:
    """Vertical bars (one per value) on a baseline, with value labels on top and names below.  ``spread``: (lo, hi)
    per bar, drawn as a thin whisker (the range across seeds)."""
    n = len(values)
    vmax = vmax or max(max(values), 1e-9)
    bw = (width - gap * (n - 1)) / n
    g = VGroup()
    base = Line([x0 - 0.1, base_y, 0], [x0 + width + 0.1, base_y, 0], color=GREY_C, stroke_width=1.5)
    g.add(base)
    bars, vals, names, whisk = VGroup(), VGroup(), VGroup(), VGroup()
    for i, (v, c) in enumerate(zip(values, colors)):
        x = x0 + i * (bw + gap) + bw / 2
        h = max(height * float(v) / vmax, 0.01)
        r = Rectangle(width=bw, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x, base_y + h / 2, 0])
        bars.add(r)
        top = r.get_top()[1]
        if spread is not None:
            lo, hi = spread[i]
            y1, y2 = base_y + height * lo / vmax, base_y + height * hi / vmax
            whisk.add(VGroup(Line([x, y1, 0], [x, y2, 0], color=WHITE, stroke_width=2),
                             Line([x - 0.08, y1, 0], [x + 0.08, y1, 0], color=WHITE, stroke_width=2),
                             Line([x - 0.08, y2, 0], [x + 0.08, y2, 0], color=WHITE, stroke_width=2)))
            top = max(top, y2)
        vals.add(MathTex(fmt.format(v), font_size=font_size, color=c).move_to([x, top + 0.2, 0]))
        if labels is not None:
            names.add(label(labels[i], font_size=font_size, color=c).next_to([x, base_y, 0], DOWN, buff=0.12))
    g.add(bars, whisk, vals, names)
    g.bars, g.vals, g.names, g.whisk, g.base = bars, vals, names, whisk, base
    return g


def seed_lines(ax, xs, Y, color, sw=2.5, band_opacity=0.18) -> VGroup:
    """Several seeds' curves: the mean as a line, the min-max range as a band."""
    Y = np.asarray(Y, float)
    lo, hi, mu = Y.min(0), Y.max(0), Y.mean(0)
    return VGroup(band(ax, xs, lo, hi, color, band_opacity), curve(ax, xs, mu, color, sw))


def matrix_box(rows, cols, unit=0.18, color=GREY_B, fill=None, label_tex=None, font_size=26) -> VGroup:
    """A matrix drawn as a rectangle of its shape (rows x cols cells of ``unit``), optionally filled and labelled."""
    r = Rectangle(width=cols * unit, height=rows * unit, stroke_color=color, stroke_width=2,
                  fill_color=fill or color, fill_opacity=0.18 if fill else 0.0)
    g = VGroup(r)
    if label_tex:
        g.add(MathTex(label_tex, font_size=font_size, color=color).move_to(r))
    return g
