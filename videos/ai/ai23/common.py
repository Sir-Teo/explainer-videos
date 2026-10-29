"""Helpers shared by the scenes of Part 23 ("Every Sense Is a Token")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 23
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
TEXT_C, IMG_C, SND_C = C.TRUE_P, C.BITS, C.INTERVAL  # the three senses
SEM_C, ACOU_C = C.CONTEXT, C.INTERVAL  # semantic and acoustic tokens
BLANK_C = GREY_C  # CTC's blank
CLIP_C, SIGLIP_C = C.SURPRISE, C.CONTEXT  # the two contrastive losses
SURP_C = C.SURPRISE  # surprise, entropy of the next byte
TOKEN_COLORS = ["#58A6FF", "#F7D154", "#FF6B8B", "#5BD17A", "#D4A5FF", "#FF9F45", "#7FD3FF", "#E86F8A"]
LM_COLORS = {"bytes256": GREY_B, "bpe1024": "#9CC8FF", "bpe4096": "#2F7FE0", "unigram1024": "#FFC98A",
             "unigram4096": "#FF8A2A"}
LM_NAMES = {"bytes256": r"bytes ($256$)", "bpe1024": r"BPE, $1{,}024$", "bpe4096": r"BPE, $4{,}096$",
            "unigram1024": r"unigram, $1{,}024$", "unigram4096": r"unigram, $4{,}096$"}
VQ_COLORS = {"vq": C.SURPRISE, "ema": C.MODEL_Q, "restart": C.INTERVAL, "fsq": C.TRUE_P, "lfq": C.CONTEXT}
VQ_NAMES = {"vq": r"VQ", "ema": r"VQ + EMA", "restart": r"EMA + restarts", "fsq": r"FSQ", "lfq": r"LFQ"}
CARD_BG = "#121722"


def gray_image(a, size) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    rgb = np.stack([a, a, a, np.ones_like(a)], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def heat(M, width, height, color=SND_C, signed=False, lo=None, hi=None, smooth=False) -> ImageMobject:
    """A matrix as a picture (row 0 at the top); ``lo``/``hi`` fix the brightness scale (default: its own range)."""
    M = np.asarray(M, float)
    bg = np.array(ManimColor("#121722").to_rgb())
    if signed:
        s = np.clip(M / max(np.abs(M).max(), 1e-9), -1, 1)
        a = np.abs(s)[..., None]
        rgb = bg * (1 - a) + np.where(s[..., None] > 0, np.array(ManimColor(C.TRUE_P).to_rgb()),
                                      np.array(ManimColor(C.SURPRISE).to_rgb())) * a
    else:
        lo_, hi_ = (np.nanmin(M) if lo is None else lo), (np.nanmax(M) if hi is None else hi)
        v = np.clip((np.nan_to_num(M, nan=lo_) - lo_) / max(hi_ - lo_, 1e-9), 0, 1)[..., None]
        rgb = bg * (1 - v) + np.array(ManimColor(color).to_rgb()) * v
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    return img.stretch_to_fit_width(width).stretch_to_fit_height(height)


def spectro(M, width, height, color=SND_C, lo=None, hi=None) -> ImageMobject:
    """A spectrogram (frequency x time, low frequencies in row 0) drawn with low frequencies at the bottom."""
    return heat(np.asarray(M)[::-1], width, height, color=color, lo=lo, hi=hi, smooth=True)


def token_chips(pieces, font_size=26, height=0.5, buff=0.06, colors=None) -> VGroup:
    """Text pieces as coloured chips, side by side (a leading space shown as a dim dot)."""
    g = VGroup()
    for i, p in enumerate(pieces):
        t = data_text(p.replace(" ", "·"), font=MONO, font_size=font_size, color=WHITE)
        col = (colors or TOKEN_COLORS)[i % len(colors or TOKEN_COLORS)]
        box = RoundedRectangle(width=t.width + 0.16, height=height, corner_radius=0.08, stroke_width=0,
                               fill_color=col, fill_opacity=0.35)
        g.add(VGroup(box, t.move_to(box)))
    return g.arrange(RIGHT, buff=buff)


def wrap_chips(chips: VGroup, width: float, buff=0.08, row_buff=0.14) -> VGroup:
    """Lay chips out in rows no wider than ``width`` (keeps the chips themselves; returns the rows)."""
    rows, cur, w = VGroup(), VGroup(), 0.0
    for c in chips:
        if len(cur) and w + c.width > width:
            rows.add(cur.arrange(RIGHT, buff=buff))
            cur, w = VGroup(), 0.0
        cur.add(c)
        w += c.width + buff
    if len(cur):
        rows.add(cur.arrange(RIGHT, buff=buff))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=row_buff)


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=max(width or 0, t.width + 2 * pad), height=max(height, t.height + 0.25),
                           corner_radius=0.12, stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def code_grid(codes, cell=0.18, K=None, colors=None, buff=0.0) -> VGroup:
    """A grid of integer codes (rows x columns) as coloured cells: the hue cycles with the code's value."""
    codes = np.asarray(codes)
    K = K or int(codes.max()) + 1
    cols = colors or TOKEN_COLORS
    g = VGroup()
    for r in range(codes.shape[0]):
        for c in range(codes.shape[1]):
            v = int(codes[r, c])
            g.add(Square(cell, stroke_width=0, fill_color=cols[v % len(cols)],
                         fill_opacity=0.25 + 0.7 * ((v * 2654435761) % 997) / 997).move_to(
                [c * (cell + buff), -r * (cell + buff), 0]))
    return g.move_to(ORIGIN)


def spread_rows(rows, x_max, width=6.0, row_h=0.62, font_size=22, fmt="{:.2f}", label_w=3.2, bar_h=0.32):
    """Comparison rows: (name, colour, values over seeds).  Each row: the name, a bar to the mean, a dot per seed, and
    the mean with the range.  Returns a VGroup with ``.rows`` (each with ``.bar``, ``.dots``, ``.value``)."""
    g, out = VGroup(), VGroup()
    x0 = 0.0
    scale = width / x_max
    for i, (name, col, vals) in enumerate(rows):
        y = -i * row_h
        vals = np.asarray(vals, float)
        m = float(vals.mean())
        nm = label(name, font_size=font_size, color=col)
        if nm.width > label_w:
            nm.width = label_w
        nm.move_to([x0 - 0.25 - nm.width / 2, y, 0])
        bar = Rectangle(width=max(m * scale, 0.02), height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.55)
        bar.move_to([x0 + max(m * scale, 0.02) / 2, y, 0])
        dots = VGroup(*[Dot([x0 + v * scale, y, 0], radius=0.055, color=WHITE) for v in vals])
        rng_ = Line([x0 + vals.min() * scale, y, 0], [x0 + vals.max() * scale, y, 0], color=WHITE, stroke_width=2)
        txt = fmt.format(m)
        if len(vals) > 1:
            txt = txt + r"\ \ (" + fmt.format(vals.min()) + r"\text{--}" + fmt.format(vals.max()) + ")"
        val = MathTex(txt, font_size=font_size, color=col).next_to([x0 + max(vals.max(), m) * scale, y, 0], RIGHT, buff=0.15)
        row = VGroup(nm, bar, rng_, dots, val)
        row.bar, row.dots, row.value, row.name = bar, VGroup(rng_, dots), val, nm
        out.add(row)
    g.add(out)
    g.rows = out
    g.x0, g.unit = x0, scale
    return g


def tag_schematic(corner=DL):
    return note(r"schematic").to_corner(corner, buff=0.3)
