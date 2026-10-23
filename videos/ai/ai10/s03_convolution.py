from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (FMAP, KERNEL, MLPC, PART, NEG, POS, _image, img_gray, img_heat, load, rgb)

SHIFTC = C.INTERVAL
COLORS = {r"w": KERNEL, r"T_s": SHIFTC}


def heat_rgb(a, vmax, upto=None):
    """The feature map as colours (blue negative, gold positive), only the first ``upto`` positions filled."""
    t = np.clip(np.asarray(a, float) / vmax, -1, 1)[..., None]
    mid = rgb("#0B0F17")
    out = np.where(t >= 0, mid * (1 - t) + rgb(POS) * t, mid * (1 + t) + rgb(NEG) * (-t))
    if upto is not None:
        flat = out.reshape(-1, 3)
        flat[int(upto):] = rgb("#141A24")
        out = flat.reshape(out.shape)
    return out


def _oriented_fit(Kc, deg):
    """Best correlation of a centred 5x5 kernel with a bar or an edge through its centre at this angle."""
    yy, xx = np.mgrid[0:5, 0:5] - 2.0
    t = np.deg2rad(deg)
    d = xx * np.sin(t) + yy * np.cos(t)
    best = 0.0
    for T in (np.exp(-d ** 2 / 1.28), np.tanh(d / 0.8)):
        T = T - T.mean()
        best = max(best, abs(float((T * Kc).sum() / np.sqrt((T ** 2).sum() * (Kc ** 2).sum() + 1e-12))))
    return best


class Convolution(VoiceoverScene):
    def construct(self):
        self.card()
        self.sharing()
        self.sweep()
        self.theorem()
        self.check()

    def card(self):
        card = chapter_card(2, r"Convolution", r"What does it mean to look for the same thing everywhere?",
                            lit=(1998,), part=PART)
        with self.voiceover("Chapter two. Convolution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sharing(self):
        e = load("equivariance")
        digit = img_gray(np.asarray(e["digit"]), 2.8).move_to([-4.6, 0.6, 0])
        cell = digit.width / 28
        pix = lambda i, j: digit.get_corner(UL) + np.array([(j + 0.5) * cell, -(i + 0.5) * cell, 0])  # noqa: E731
        unit_d = Dot([-1.5, 1.9, 0], radius=0.09, color=MLPC)
        dense = VGroup(*[Line(pix(i, j), unit_d.get_center(), stroke_width=0.4, color=MLPC, stroke_opacity=0.35)
                         for i in range(0, 28, 3) for j in range(0, 28, 3)])
        unit_c = Dot([-1.5, -0.6, 0], radius=0.09, color=KERNEL)
        patch = Square(5 * cell, stroke_color=KERNEL, stroke_width=2).move_to(pix(14, 14))
        def local_lines():
            c0 = patch.get_center()
            return VGroup(*[Line(c0 + np.array([(b - 2) * cell, -(a - 2) * cell, 0]), unit_c.get_center(),
                                 stroke_width=0.8, color=KERNEL, stroke_opacity=0.7) for a in range(5) for b in range(5)])

        local = local_lines()
        ld = label(r"fully connected: \ every pixel", font_size=20, color=MLPC).next_to(unit_d, UP, buff=0.15)
        lc = label(r"convolutional: \ a $5 \times 5$ patch", font_size=20, color=KERNEL).next_to(unit_c, DOWN,
                                                                                                    buff=0.15)
        vals = [e["params_dense"], e["params_local"], e["params_conv"]]
        names = [r"fully connected", r"local, \ not shared", r"convolution: \ shared"]
        cols = [MLPC, GREY_B, KERNEL]
        bars = VGroup()
        top = math.log10(max(vals))
        for k, (v, nm, c) in enumerate(zip(vals, names, cols)):
            w = 3.8 * math.log10(v) / top
            b = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([0.7 + w / 2, 1.2 - 0.95 * k, 0])
            t = label(nm, font_size=22, color=c).next_to(b, UP, buff=0.08).align_to(b, LEFT)
            n = MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=28, color=c).next_to(b, RIGHT, buff=0.15)
            bars.add(VGroup(b, t, n))
        bl = label(r"weights for six $28 \times 28$ maps \ (log scale)", font_size=22, color=GREY_B)
        bl.next_to(bars, DOWN, buff=0.35).align_to(bars, LEFT)
        dl = label(r"a $28 \times 28$ digit", font_size=20, color=GREY_B).next_to(digit, DOWN, buff=0.15)
        with self.voiceover(
            "Suppose a network should find a short stroke in a digit. A fully connected unit weighs every pixel, "
            "<bookmark mark='a'/> so to find the stroke anywhere, the network must learn a detector for every "
            "place it might be. <bookmark mark='b'/> A convolutional unit looks at a small patch, five pixels by "
            "five, <bookmark mark='c'/> and every unit of a map uses the same twenty-five weights, slid across the "
            "image. <bookmark mark='d'/> For six maps the size of the digit, fully connected units need "
            f"{e['params_dense'] / 1e6:.1f} million weights; local patches without sharing, "
            f"{e['params_local']:,}; shared, just {e['params_conv']}. Sharing is the whole idea: the same pattern "
            "can appear anywhere, so look for it the same way everywhere."
        ) as vo:
            self.play(FadeIn(digit), FadeIn(dl))
            self.play(FadeIn(unit_d), Create(dense, lag_ratio=0.002), FadeIn(ld), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(patch), FadeIn(unit_c), Create(local), FadeIn(lc))
            self.remove(local)
            local = always_redraw(local_lines)
            self.add(local)
            vo.wait_until("c")
            self.play(patch.animate.move_to(pix(6, 9)), run_time=1.0)
            self.play(patch.animate.move_to(pix(20, 18)), run_time=1.0)
            local.clear_updaters()
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.4), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        e = load("equivariance")
        d, K, fmap = np.asarray(e["digit"]), np.asarray(e["kernel"]), np.asarray(e["fmap"])
        card = definition_card(
            r"Convolution (as deep learning uses the word)",
            cmath(r"(w \star x)[i, j] = \sum_{u, v} {{w}}[u, v]\; x[i + u,\, j + v] \; + \; b", colors=COLORS,
                  font_size=32), width=7.6, color=KERNEL).to_edge(UP, buff=0.3)
        digit = img_gray(d, 3.6).move_to([-4.2, -1.2, 0])
        cell = digit.width / 28
        kern = img_heat(K, 1.6).move_to([-0.6, -0.4, 0])
        kl = label(r"a learned $5 \times 5$ kernel", font_size=20, color=KERNEL).next_to(kern, DOWN, buff=0.15)
        vmax = float(np.abs(fmap).max())
        pos = ValueTracker(0.0)
        out = _image(heat_rgb(fmap, vmax, 0), 3.6, None, False).move_to([3.8, -1.2, 0])
        out.add_updater(lambda m: setattr(m, "pixel_array", (np.concatenate(
            [heat_rgb(fmap, vmax, pos.get_value()), np.ones((28, 28, 1))], -1) * 255).astype(np.uint8)))
        frame_o = SurroundingRectangle(out, buff=0, color=GREY_D, stroke_width=1.2)

        def window():
            p = int(min(pos.get_value(), 783))
            i, j = divmod(p, 28)
            c = digit.get_corner(UL) + np.array([(j + 0.5) * cell, -(i + 0.5) * cell, 0])
            return Square(5 * cell, stroke_color=KERNEL, stroke_width=2.5).move_to(c)

        def dot_out():
            p = int(min(pos.get_value(), 783))
            i, j = divmod(p, 28)
            return Square(cell, stroke_color=WHITE, stroke_width=2).move_to(
                out.get_corner(UL) + np.array([(j + 0.5) * cell, -(i + 0.5) * cell, 0]))

        win = always_redraw(window)
        dot = always_redraw(dot_out)
        ol = label(r"the feature map: \ one number per position", font_size=20, color=FMAP).next_to(out, DOWN,
                                                                                                     buff=0.15)
        dl = label(r"the input", font_size=20, color=GREY_B).next_to(digit, DOWN, buff=0.15)
        note_ = note(r"kernel: \ LeNet's first layer, \ trained here (Chapter 4); \ padded by $2$ at the border")
        note_.to_corner(DR, buff=0.2)
        # what the learned kernel likes: fit it with a linear ramp (an edge detector is close to one)
        yy, xx = np.mgrid[0:5, 0:5] - 2.0
        Kc = K - K.mean()
        cy, cx = float((Kc * yy).sum()), float((Kc * xx).sum())
        ramp = (cy ** 2 / 50 + cx ** 2 / 50) / max(float((Kc ** 2).sum()), 1e-12)
        if ramp > 0.4 and abs(cy) > 2 * abs(cx):
            if cy < 0:
                likes = "This kernel was learned, and it likes the bottom edges of strokes."
            else:
                likes = "This kernel was learned, and it likes the top edges of strokes."
        elif ramp > 0.4 and abs(cx) > 2 * abs(cy):
            if cx < 0:
                likes = "This kernel was learned, and it likes the right-hand edges of strokes."
            else:
                likes = "This kernel was learned, and it likes the left-hand edges of strokes."
        elif ramp > 0.4:
            likes = "This kernel was learned, and it likes the edges of strokes at a slant."
        elif max(_oriented_fit(Kc, th) for th in range(0, 180, 5)) > 0.45:
            likes = "This kernel was learned, and it likes strokes and their edges at one particular angle."
        else:
            likes = "This kernel was learned, and what it likes is not as simple as one edge."
        with self.voiceover(
            "Here is the operation. <bookmark mark='a'/> Lay a small grid of weights, the kernel, over a patch of "
            "the image; multiply each weight by the pixel under it and add them up. That is one number of the "
            "output. <bookmark mark='b'/> Slide the kernel one pixel along and do it again, row by row, until it "
            "has visited every position. <bookmark mark='c'/> The output is a feature map: bright wherever the "
            f"patch looks like the kernel. {likes} "
            "<bookmark mark='d'/> Strictly, this is a cross-correlation; a mathematician's convolution flips the "
            "kernel first. Since the kernel is learned, nobody minds, and deep learning calls both convolution."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(digit), FadeIn(dl), FadeIn(kern), FadeIn(kl), FadeIn(out), Create(frame_o), FadeIn(ol),
                      FadeIn(note_))
            self.add(win, dot)
            vo.wait_until("b")
            self.play(pos.animate.set_value(784), run_time=7.0, rate_func=linear)
        for m in (win, dot, out):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = theorem_card(r"Convolution commutes with shifts",
                           cmath(r"w \star (T_s x) \;=\; T_s (w \star x), \qquad (T_s x)[i] = x[i - s]",
                                 colors=COLORS, font_size=32),
                           who=r"translation equivariance", width=8.0, color=KERNEL).to_edge(UP, buff=0.3)
        ph = r"\phantom{(w \star T_s x)[i]}"
        COL = {r"w": KERNEL, r"T_s": SHIFTC, r"(T_s x)": SHIFTC}
        rows = [
            cmath(r"(w \star T_s x)[i]", r"=", r"\sum_u", r"w", r"[u]\,", r"(T_s x)", r"[i+u]", colors=COL,
                  font_size=38),
            cmath(ph, r"=", r"\sum_u", r"w", r"[u]\,", r"x", r"[i+u-s]", colors=COL, font_size=38),
            cmath(ph, r"=", r"(w \star x)", r"[i-s]", colors=COL, font_size=38),
            cmath(ph, r"=", r"\big(", r"T_s", r"(w \star x)", r"\big)", r"[i]", colors=COL, font_size=38),
        ]
        whys = [why(r"definition of $\star$"), why(r"definition of the shift $T_s$"),
                why(r"$\star$ evaluated at $i - s$"), why(r"definition of $T_s$ again")]
        step = ladder(self, rows, whys, keep=4, top=1.1, x=-2.0, align_index=1, edge=6.8)
        foot = label(r"in two dimensions the same, with $i$, $u$, $s$ pairs; \ exact if the image wraps around",
                     font_size=22, color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Sharing the weights buys a precise property: shift the image, and the feature map shifts with it. "
            "<bookmark mark='a'/> Write T s for the shift by s. The convolution of the shifted image at i is a sum "
            "of weights times the shifted image. <bookmark mark='b'/> The shifted image at i plus u is the original "
            "at i plus u minus s. <bookmark mark='c'/> That sum is the convolution of the original at i minus s. "
            "<bookmark mark='d'/> Which is the shifted feature map, for any kernel, learned or not. "
            "<bookmark mark='e'/> In two dimensions the argument is the same; it holds exactly when the image wraps "
            "around, and away from the border with zero padding."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        e = load("equivariance")
        S = 2.4
        x = img_gray(np.asarray(e["digit"]), S).move_to([-3.6, 1.5, 0])
        fx = img_heat(np.asarray(e["fmap"]), S).move_to([0.6, 1.5, 0])
        xs = img_gray(np.asarray(e["digit_shift"]), S).move_to([-3.6, -1.6, 0])
        fxs = img_heat(np.asarray(e["fmap_shift"]), S).move_to([0.6, -1.6, 0])
        a1 = Arrow(x.get_right(), fx.get_left(), buff=0.15, color=KERNEL, stroke_width=3)
        a2 = Arrow(xs.get_right(), fxs.get_left(), buff=0.15, color=KERNEL, stroke_width=3)
        a3 = Arrow(x.get_bottom(), xs.get_top(), buff=0.12, color=SHIFTC, stroke_width=3)
        a4 = Arrow(fx.get_bottom(), fxs.get_top(), buff=0.12, color=SHIFTC, stroke_width=3)
        l1 = label(r"$w \star$", font_size=26, color=KERNEL).next_to(a1, UP, buff=0.05)
        l2 = label(r"$w \star$", font_size=26, color=KERNEL).next_to(a2, UP, buff=0.05)
        sy, sx = e["shift"]
        l3 = label(rf"$T_s$, \ $s = ({sy}, {sx})$", font_size=22, color=SHIFTC).next_to(a3, LEFT, buff=0.1)
        l4 = label(r"$T_s$", font_size=24, color=SHIFTC).next_to(a4, RIGHT, buff=0.1)
        frames = VGroup(*[SurroundingRectangle(m, buff=0, color=GREY_D, stroke_width=1) for m in (x, fx, xs, fxs)])

        def sci(v):
            if v == 0:
                return "0"
            ex = int(math.floor(math.log10(v)))
            return rf"{v / 10 ** ex:.1f} \times 10^{{{ex}}}"

        rows = VGroup(
            label(r"largest difference, \ relative to the map's largest value:", font_size=22, color=GREY_A),
            VGroup(label(r"wrapping at the edges", font_size=22, color=KERNEL),
                   MathTex(sci(e["err_circular"]), font_size=30, color=KERNEL)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"zero padding, \ away from the border", font_size=22, color=KERNEL),
                   MathTex(sci(e["err_zero_inside"]), font_size=30, color=KERNEL)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"zero padding, \ at the border", font_size=22, color=GREY_B),
                   MathTex(f"{e['err_zero_all']:.2f}", font_size=30, color=GREY_B)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"a fully connected layer", font_size=22, color=MLPC),
                   MathTex(f"{e['err_dense']:.2f}", font_size=30, color=MLPC)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.9, 0.0, 0])
        if rows.width > 4.6:
            rows.width = 4.6
        keep_in_frame(rows)
        tag = note(r"computed").to_corner(DR, buff=0.25)
        err = float(e["err_circular"])
        ex = int(math.floor(math.log10(err))) if err > 0 else 0
        mant = round(err / 10 ** ex) if err > 0 else 0
        if 0 < err < 1e-5:
            v1 = (f"With the image wrapping around, the two routes differ by about {mant} times ten to the minus "
                  f"{-ex} of the map's largest value: rounding error in the last digits of the arithmetic.")
        elif err == 0:
            v1 = "With the image wrapping around, the two routes agree exactly, to the last bit."
        else:
            v1 = f"With the image wrapping around, the two routes differ by {err:.2g} of the map's largest value."
        with self.voiceover(
            "Let's check it on our digit. <bookmark mark='a'/> Convolve, then shift; <bookmark mark='b'/> or shift "
            f"the digit by {abs(sy)} pixels down and {abs(sx)} to the left, then convolve. <bookmark mark='c'/> "
            + v1 + " <bookmark mark='d'/> With zero padding the maps agree everywhere except a thin band at the "
            "border, where the shifted image has lost pixels. <bookmark mark='e'/> A fully connected layer of the "
            f"same shape has no such identity: its two routes differ by {e['err_dense']:.1f} times the size of its "
            "output. Equivariance is what weight sharing buys."
        ) as vo:
            self.play(FadeIn(x), FadeIn(frames[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(fx), FadeIn(frames[1]))
            self.play(GrowArrow(a4), FadeIn(l4))
            vo.wait_until("b")
            self.play(GrowArrow(a3), FadeIn(l3), FadeIn(xs), FadeIn(frames[2]))
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(fxs), FadeIn(frames[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()
