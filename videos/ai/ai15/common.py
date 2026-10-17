"""Helpers shared by the scenes of Part 15 ("Images and Video")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

MONO = "DejaVu Sans Mono"
PATCH = C.BITS
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def gray_image(a, size) -> ImageMobject:
    a = np.clip(np.asarray(a, float), 0, 1)
    rgb = np.stack([a, a, a, np.ones_like(a)], -1)
    img = ImageMobject((rgb * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def heat_image(M, size, color=C.ATTN, gamma=0.7) -> ImageMobject:
    M = np.asarray(M, float)
    v = np.clip((M - M.min()) / max(M.max() - M.min(), 1e-12), 0, 1) ** gamma
    c = np.array(ManimColor(color).to_rgb())
    bg = np.array(ManimColor("#121722").to_rgb())
    rgb = bg[None, None] * (1 - v[..., None]) + c[None, None] * v[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(M.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


def patch_grid(img_mob, n, color=PATCH, stroke_width=1.5) -> VGroup:
    """Lines cutting a square picture into n x n patches."""
    w = img_mob.width
    ul = img_mob.get_corner(UL)
    g = VGroup()
    for k in range(1, n):
        g.add(Line(ul + RIGHT * w * k / n, ul + RIGHT * w * k / n + DOWN * w, color=color, stroke_width=stroke_width))
        g.add(Line(ul + DOWN * w * k / n, ul + DOWN * w * k / n + RIGHT * w, color=color, stroke_width=stroke_width))
    return g


# a 7 x 7 letter A, for the convolution pictures
A_PIXELS = np.array([[int(ch) for ch in row] for row in
                     ("0011100", "0110110", "1100011", "1100011", "1111111", "1100011", "1100011")], float)


def conv_picture(cell=0.26) -> VGroup:
    """A convolution: one 3 x 3 window slid over a letter's pixels, the same weighted sum (here an average) at every
    spot filling one cell of the output.  ``.inp``, ``.out``, ``.window`` and ``.vals`` (each output cell's
    brightness) let a scene slide the window and fill the output."""
    P = A_PIXELS
    inp = VGroup(*[Square(cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=WHITE, fill_opacity=0.05 + 0.8 * v)
                   for v in P.flatten()]).arrange_in_grid(7, 7, buff=0)
    vals = [float(P[i:i + 3, j:j + 3].mean()) for i in range(5) for j in range(5)]
    out = VGroup(*[Square(cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=PATCH, fill_opacity=0.0)
                   for _ in vals]).arrange_in_grid(5, 5, buff=0)
    arrow = Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.25)
    row = VGroup(inp, arrow, out).arrange(RIGHT, buff=0.3)
    window = Square(3 * cell, stroke_color=PATCH, stroke_width=3.5).move_to(inp[8])
    names = VGroup(label(r"the pixels", font_size=18, color=GREY_A).next_to(inp, DOWN, buff=0.1),
                   label(r"one learned $3 \times 3$ stencil, \ the same at every spot", font_size=18, color=PATCH)
                   .next_to(row, UP, buff=0.12),
                   label(r"the output", font_size=18, color=GREY_A).next_to(out, DOWN, buff=0.1))
    names[2].match_y(names[0])
    g = VGroup(row, window, names)
    g.inp, g.out, g.window, g.vals = inp, out, window, vals
    return g


def slide_window(scene, pic, run_time=0.11):
    """Slide a conv_picture's window over every spot, filling the output cell by cell."""
    for k, v in enumerate(pic.vals):
        i, j = divmod(k, 5)
        scene.play(pic.window.animate.move_to(pic.inp[(i + 1) * 7 + j + 1]),
                   pic.out[k].animate.set_fill(opacity=0.1 + 0.85 * v), run_time=run_time, rate_func=linear)


def causal_conv_picture(cell=0.22) -> VGroup:
    """A causal convolution in time: the 3 x 3 stencil becomes a 3 x 3 x 3 block, reaching over this frame and the two
    before it, never the next."""
    frames = VGroup()
    for f in range(4):
        sq = VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D, fill_color="#121722", fill_opacity=1)
                      for _ in range(25)]).arrange_in_grid(5, 5, buff=0)
        frames.add(sq)
    frames.arrange(RIGHT, buff=0.35)
    frames[3].set_opacity(0.3)
    wins = VGroup(*[Square(3 * cell, stroke_color=PATCH, stroke_width=3, fill_color=PATCH, fill_opacity=0.25)
                    .move_to(frames[f][12]) for f in range(3)])
    tie = VGroup(*[DashedLine(wins[f].get_right(), wins[f + 1].get_left(), color=PATCH, stroke_width=2, dash_length=0.05)
                   for f in range(2)])
    names = VGroup(*[MathTex(t, font_size=24, color=PATCH if f < 3 else GREY_C).next_to(frames[f], DOWN, buff=0.1)
                     for f, t in enumerate((r"t-2", r"t-1", r"t", r"t+1"))])
    br = Brace(VGroup(frames[0], frames[2]), UP, buff=0.08, color=PATCH)
    bl = label(r"one $3 \times 3 \times 3$ stencil: \ this frame and two before", font_size=18, color=PATCH).next_to(br, UP, buff=0.06)
    fl = label(r"the future: \\ never seen", font_size=18, color=GREY_C).next_to(frames[3], UP, buff=0.1)
    return VGroup(frames, wins, tie, names, br, bl, fl)


def codebook_picture() -> VGroup:
    """A 16-entry codebook on a number line: each number snaps to its nearest entry, whose index is the token."""
    w = 7.5
    xs = np.linspace(-w / 2, w / 2, 16)
    line = Line([-w / 2 - 0.2, 0, 0], [w / 2 + 0.2, 0, 0], color=GREY_B, stroke_width=2)
    ticks = VGroup(*[Line([x, -0.1, 0], [x, 0.1, 0], color=GREY_B, stroke_width=2) for x in xs])
    idx = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).move_to([x, -0.32, 0]) for k, x in enumerate(xs)])
    g = VGroup(line, ticks, idx)
    for v in (2.35, 7.7, 12.2):  # values, in units of the spacing
        k = int(round(v))
        x0 = -w / 2 + v * (w / 15)
        dot = Dot([x0, 0.75, 0], radius=0.08, color=WHITE)
        arr = Arrow([x0, 0.66, 0], [xs[k], 0.12, 0], buff=0, color=PATCH, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        box = SurroundingRectangle(idx[k], buff=0.05, color=PATCH, stroke_width=2)
        g.add(dot, arr, box)
    g.add(label(r"a number", font_size=20, color=WHITE).next_to(g[3], UP, buff=0.1))
    return g
