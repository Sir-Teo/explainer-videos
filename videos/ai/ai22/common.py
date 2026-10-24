"""Helpers shared by the scenes of Part 22 ("Images, Video and 3D")."""

from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 22
MONO = "DejaVu Sans Mono"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PANEL = "#121722"

# one meaning per colour, for the whole part
PATCH = C.BITS  # patches, tokens of a picture
TXT = C.TRUE_P  # text tokens
HIST = C.HUMAN  # history cards
VIT_C, CNN_C = C.BITS, C.TRUE_P
CFG_C = {"zero": C.BITS, "ada": C.SURPRISE, "context": "#B39DDB", "unet": C.TRUE_P, "repa": C.INTERVAL}
CFG_NAME = {"zero": r"adaLN-Zero", "ada": r"adaLN", "context": r"in-context", "unet": r"U-Net", "repa": r"adaLN-Zero + REPA"}
GEN_C = {"raster": C.TRUE_P, "maskgit": "#B39DDB", "var": C.BITS}
GEN_NAME = {"raster": r"raster order", "maskgit": r"MaskGIT", "var": r"VAR"}
VID_C = {"clip": "#B39DDB", "teacher": C.SURPRISE, "forcing": C.INTERVAL, "forcing_noisy": C.BITS}
VID_NAME = {"clip": r"whole clip", "teacher": r"teacher forcing", "forcing": r"diffusion forcing",
            "forcing_noisy": r"diffusion forcing, noisy context"}
NERF_C, GS_C = "#7FD3FF", C.BITS
LAT_C = C.EMBED


def rgb_of(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


def gray_image(a, size, height=None) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    rgb = np.stack([a, a, a, np.ones_like(a)], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(height or size * a.shape[0] / a.shape[1])


def rgb_image(a, size, smooth=False) -> ImageMobject:
    """An (h, w, 3) picture in [0, 1]."""
    a = np.clip(np.asarray(a, float), 0, 1)
    img = ImageMobject((np.concatenate([a, np.ones(a.shape[:2] + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size * a.shape[0] / a.shape[1])


def heat_image(M, size, color=C.ATTN, gamma=0.7, vmax=None) -> ImageMobject:
    M = np.asarray(M, float)
    top = vmax if vmax is not None else M.max()
    v = np.clip((M - M.min()) / max(top - M.min(), 1e-12), 0, 1) ** gamma
    c = rgb_of(color)
    bg = rgb_of(PANEL)
    rgb = bg[None, None] * (1 - v[..., None]) + c[None, None] * v[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size * M.shape[0] / M.shape[1])


def signed_image(D, size, top=None, pos=C.BITS, neg=C.TRUE_P) -> ImageMobject:
    """A signed picture: dark where zero, gold where positive, blue where negative."""
    D = np.asarray(D, float)
    top = top or max(float(np.abs(D).max()), 1e-9)
    v = np.clip(D / top, -1, 1)
    bg = rgb_of(PANEL)
    a = np.abs(v)[..., None]
    rgb = bg * (1 - a) + np.where(v[..., None] > 0, rgb_of(pos), rgb_of(neg)) * a
    img = ImageMobject((np.concatenate([rgb, np.ones(D.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def glyph_sheet(Q, rows, cols, size=0.6, gap=0.06, frame=True) -> Group:
    """Many letter pictures as one image (cheaper to draw than many)."""
    Q = np.clip(np.asarray(Q, float), 0, 1)
    px = Q.shape[-1]
    g = max(1, int(round(gap / size * px)))
    H, W = rows * px + (rows - 1) * g, cols * px + (cols - 1) * g
    sheet = np.ones((H, W, 3)) * rgb_of(PANEL)[None, None]
    for k in range(min(len(Q), rows * cols)):
        r, c = divmod(k, cols)
        sheet[r * (px + g): r * (px + g) + px, c * (px + g): c * (px + g) + px] = Q[k][..., None]
    img = rgb_image(sheet, cols * size + (cols - 1) * gap)
    if not frame:
        return Group(img)
    box = SurroundingRectangle(img, buff=0.06, color=GREY_D, stroke_width=1.2, corner_radius=0.05)
    return Group(box, img)


def patch_grid(img_mob, n, color=PATCH, stroke_width=1.5) -> VGroup:
    """Lines cutting a square picture into n x n patches."""
    w = img_mob.width
    ul = img_mob.get_corner(UL)
    g = VGroup()
    for k in range(1, n):
        g.add(Line(ul + RIGHT * w * k / n, ul + RIGHT * w * k / n + DOWN * w, color=color, stroke_width=stroke_width))
        g.add(Line(ul + DOWN * w * k / n, ul + DOWN * w * k / n + RIGHT * w, color=color, stroke_width=stroke_width))
    return g


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def words(n: int) -> str:
    return WORDS[n] if 0 <= n < len(WORDS) else str(n)


def strip_tex(s: str) -> str:
    return s.replace(r"\ ", " ").replace("\\", "").replace("$", "").replace("{", "").replace("}", "")


def take_away(text: str, color=C.BITS, font_size=26, width=12.4) -> VGroup:
    """The chapter's takeaway: a line in a soft box at the bottom of the frame."""
    t = wrapped_label(text, width, font_size, color)
    box = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.35, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.94)
    return VGroup(box, t.move_to(box)).to_edge(DOWN, buff=0.3)


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=width or (t.width + 2 * pad), height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def spread_bars(groups, colors, names, height=2.8, bar_w=0.5, gap=0.18, group_gap=0.7, vmax=None, fmt=None,
                font_size=18, group_names=None) -> VGroup:
    """Bars of the mean over seeds with min-max whiskers and every seed as a dot. ``groups``: a list of groups, each a
    list of per-bar seed values. Returns a VGroup with ``.bars`` (per group), ``.base``, ``.names``, ``.vals``."""
    fmt = fmt or (lambda v: f"{v:.2f}")
    allv = [v for g in groups for b in g for v in b]
    vmax = vmax or max(allv) * 1.15
    g_all = VGroup()
    g_all.bars, g_all.vals, g_all.names, g_all.gnames = VGroup(), VGroup(), VGroup(), VGroup()
    x = 0.0
    for gi, grp in enumerate(groups):
        gb = VGroup()
        x0 = x
        for bi, vals in enumerate(grp):
            vals = np.asarray(vals, float)
            m = float(vals.mean())
            h = max(height * m / vmax, 0.01)
            c = colors[bi]
            b = Rectangle(width=bar_w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to([x + bar_w / 2, h / 2, 0])
            lo, hi = height * vals.min() / vmax, height * vals.max() / vmax
            wh = VGroup(Line([x + bar_w / 2, lo, 0], [x + bar_w / 2, hi, 0], color=WHITE, stroke_width=1.6),
                        Line([x + bar_w / 2 - 0.07, lo, 0], [x + bar_w / 2 + 0.07, lo, 0], color=WHITE, stroke_width=1.6),
                        Line([x + bar_w / 2 - 0.07, hi, 0], [x + bar_w / 2 + 0.07, hi, 0], color=WHITE, stroke_width=1.6))
            dots = VGroup(*[Dot([x + bar_w / 2, height * v / vmax, 0], radius=0.035, color=WHITE) for v in vals])
            val = MathTex(fmt(m), font_size=font_size, color=c).move_to([x + bar_w / 2, max(h, hi) + 0.2, 0])
            gb.add(VGroup(b, wh, dots, val))
            g_all.vals.add(val)
            x += bar_w + gap
        x -= gap
        if group_names is not None:
            g_all.gnames.add(label(group_names[gi], font_size=font_size, color=GREY_A).move_to([(x0 + x) / 2, -0.3, 0]))
        g_all.bars.add(gb)
        x += group_gap
    x -= group_gap
    base = Line([-0.15, 0, 0], [x + 0.15, 0, 0], color=GREY_C, stroke_width=1.5)
    g_all.base = base
    g_all.add(base, g_all.bars, g_all.gnames)
    if names is not None:
        leg = legend([(c, n) for c, n in zip(colors, names)], font_size=font_size)
        g_all.legend = leg
    return g_all


def plot_axes(x_range, y_range, x_length=5.0, y_length=3.0, xlabel="", ylabel="", xticks=None, yticks=None, xfmt=None,
              yfmt=None, center=ORIGIN, font_size=18):
    return axes(x_range, y_range, x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=ylabel, xticks=xticks,
                yticks=yticks, xfmt=xfmt, yfmt=yfmt, center=center, font_size=font_size)


def mean_band(ax, xs, Y, color, opacity=0.18, stroke_width=3):
    """The mean of several seeds as a line, and their min-max as a band."""
    Y = np.asarray(Y, float)
    return VGroup(band(ax, xs, Y.min(0), Y.max(0), color, opacity=opacity), curve(ax, xs, Y.mean(0), color, stroke_width))


def pct(x) -> str:
    return f"{100 * float(x):.0f}"


def fmt_int(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")
