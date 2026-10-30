from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, PART, VALUE, expo, load, log_axes, mant

C64, C32 = C.TRUE_P, GRAD


class GradCheck(VoiceoverScene):
    def construct(self):
        self.card()
        self.cancellation()
        self.derive()
        self.measured()

    def card(self):
        card = chapter_card(10, r"Cancellation, and the gradient check", r"How small should a nudge be?", part=PART)
        with self.voiceover("Chapter ten. Cancellation, and the gradient check."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cancellation(self):
        d = load("cancel")
        xs = np.asarray(d["xs"])
        g = log_axes((-6, 0), (-17, 1), x_length=6.8, y_length=4.6, xlabel=r"$x$",
                     ylabel=r"relative error of $(1 - \cos x)/x^2$", center=[-2.6, -0.5, 0], ystep=4)
        ax = g.ax

        def c(key, col, w=3):
            y = np.asarray(d[key])
            ok = y > 0
            return curve(ax, np.log10(xs[ok]), np.clip(np.log10(y[ok]), -17, 1), col, w)

        c32, c64 = c("naive_fp32", C32), c("naive_fp64", C64)
        ys32 = np.asarray(d["stable_fp32"])
        s32 = VGroup(*[Dot(ax.c2p(math.log10(x_), math.log10(y_)), radius=0.025, color=WHITE)
                       for x_, y_ in zip(xs[::2], ys32[::2]) if y_ > 0])  # dots: many values are exact (error 0)
        pred = np.asarray(d["pred_fp32"])
        okp = pred < 10
        pr32 = DashedVMobject(curve(ax, np.log10(xs[okp]), np.log10(pred[okp]), C32, 1.5), num_dashes=40)
        leg = VGroup(label(r"float32, \ as written", font_size=22, color=C32),
                     label(r"float64, \ as written", font_size=22, color=C64),
                     label(r"float32, \ rewritten as $2\sin^2(x/2)/x^2$", font_size=22, color=WHITE),
                     label(r"predicted: \ $u / (x^2/2)$", font_size=22, color=C32)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        leg.move_to([4.2, 1.3, 0])
        ex = VGroup(label(rf"float32, \ $x = 10^{{-4}}$:", font_size=22, color=GREY_A),
                    MathTex(rf"\cos x \to {d['cos32_x0']}", font_size=28, color=C32),
                    MathTex(rf"\frac{{1 - \cos x}}{{x^2}} \to {d['naive32_x0']:g} \quad (\text{{true: }} 0.5)", font_size=28,
                            color=C32)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, -1.6, 0])
        with self.voiceover(
            "One more way numbers go wrong, and it explains how to check a gradient. Take one minus cos x, over x "
            "squared: for small x it is very nearly one half. <bookmark mark='a'/> Computed as written, in float32, "
            "the error explodes as x shrinks, <bookmark mark='b'/> and at x of ten to the minus four, cos x rounds to "
            "exactly one, and the answer is zero. <bookmark mark='c'/> This is cancellation: subtracting two nearly "
            "equal numbers keeps their rounding errors but loses their size, so the relative error grows like one "
            "over x squared, just as predicted. Float64 only delays it. <bookmark mark='d'/> Rewritten without the "
            "subtraction, the same formula is accurate everywhere."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c32), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(Create(pr32), FadeIn(leg[3]), Create(c64), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(s32), FadeIn(leg[2]), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"f(x \pm h)", r"=", r"f \pm h f' + \tfrac{h^2}{2} f'' \pm \tfrac{h^3}{6} f''' + \dots", font_size=34),
            cmath(r"\frac{f(x+h) - f(x-h)}{2h}", r"=", r"f' + \tfrac{h^2}{6} f''' + \dots", font_size=34),
            cmath(r"\text{rounding: \ } \frac{u|f| + u|f|}{2h}", r"=", r"\frac{u|f|}{h}", font_size=34),
            cmath(r"E(h)", r"\approx", r"\tfrac{h^2}{6}|f'''| + \frac{u|f|}{h}", font_size=36),
            cmath(r"h^*", r"=", r"\Big(\frac{3u|f|}{|f'''|}\Big)^{1/3}", font_size=36, colors={r"h^*": GRAD}),
        ]
        whys = [why(r"Taylor, \ to third order", font_size=22), why(r"the even terms cancel: \ truncation error", font_size=22),
                why(r"each $f$ is off by about $u|f|$, \\ $u$ the unit roundoff: \ cancellation", font_size=22),
                why(r"both together", font_size=22), why(r"$E'(h) = 0$", font_size=22)]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-2.2, buff=0.38, edge=6.9)
        head = label(r"central differences: \ two errors", font_size=24, color=GREY_A).to_corner(UL, buff=0.3)
        with self.voiceover(
            "A gradient check is a cancellation on purpose. Expand f a step either side of x, by Taylor's theorem. "
            "<bookmark mark='a'/> Subtract and divide by two h: the even terms cancel, leaving the derivative plus a "
            "truncation error that shrinks like h squared. <bookmark mark='b'/> But each value of f was rounded, by "
            "about u times f, u the unit roundoff, and the subtraction keeps those errors while dividing by a tiny 2 "
            "h: a rounding error that grows like one over h. <bookmark mark='c'/> Add the two, <bookmark mark='d'/> "
            "and set the derivative to zero: the best step is the cube root of three u f over the third derivative. "
            "Too large a step and Taylor's error wins; too small and rounding does."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("vcurve")
        hs = np.asarray(d["hs"])
        pred, meas = d["pred"], d["meas"]
        g = log_axes((-13, 0), (-14, 0), x_length=7.4, y_length=5.0, xlabel=r"the step $h$",
                     ylabel=r"error of the central difference", center=[-2.4, -0.4, 0], xstep=2, ystep=2)
        ax = g.ax
        curves, marks = VGroup(), VGroup()
        for k, col in (("fp64", C64), ("fp32", C32)):
            y = np.asarray(d[f"central_{k}"])
            ok = y > 0
            band_lo = np.asarray(d[f"central_{k}_all"]).min(0)
            band_hi = np.asarray(d[f"central_{k}_all"]).max(0)
            okb = (band_lo > 0) & (band_hi > 0)
            curves.add(VGroup(band(ax, np.log10(hs[okb]), np.clip(np.log10(band_lo[okb]), -14, 0),
                                   np.clip(np.log10(band_hi[okb]), -14, 0), col, 0.15),
                              curve(ax, np.log10(hs[ok]), np.clip(np.log10(y[ok]), -14, 0), col, 3.5)))
            ph = math.log10(pred[k]["central"])
            marks.add(VGroup(DashedLine(ax.c2p(ph, -14), ax.c2p(ph, 0), color=col, stroke_width=1.8),
                             Dot(ax.c2p(math.log10(meas[k]["central"]), math.log10(meas[k]["central_err"])), radius=0.08,
                                 color=col)))
        r64 = meas["fp64"]["central"] / pred["fp64"]["central"]
        r32 = meas["fp32"]["central"] / pred["fp32"]["central"]
        table = VGroup(
            label(r"best step: \ measured \ (predicted)", font_size=22, color=GREY_A),
            label(rf"float64: \ ${sci(meas['fp64']['central'], 0)}$ \ (${sci(pred['fp64']['central'], 0)}$)", font_size=24, color=C64),
            label(rf"float32: \ ${sci(meas['fp32']['central'], 0)}$ \ (${sci(pred['fp32']['central'], 0)}$)", font_size=24, color=C32),
            label(rf"slopes: \ ${d['slope_right_fp64']:+.2f}$ on the right, \ ${d['slope_left_fp32']:+.2f}$ on the left",
                  font_size=22, color=GREY_A),
            label(rf"smallest error: \ ${sci(meas['fp64']['central_err'], 0)}$ \ and \ ${sci(meas['fp32']['central_err'], 0)}$",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.5, 0.6, 0])
        tag = note(r"computed: \ chapter 7's network, \ $8$ random directions \ (median and range)").to_corner(DR, buff=0.25)
        both_close = max(r64, 1 / r64, r32, 1 / r32) < 3
        verdict = ("both within a factor of three of the prediction" if both_close
                   else "the right order of magnitude, if not closer")
        e64, e32 = meas["fp64"]["central_err"], meas["fp32"]["central_err"]
        e6 = 10 ** float(d["at_1e-6_fp64"])
        with self.voiceover(
            "Here it is measured, on chapter seven's network, along eight random directions, in both precisions. "
            "<bookmark mark='a'/> In float64 the error falls like h squared from the right, with a slope of "
            f"{d['slope_right_fp64']:.2f}, until rounding takes over and it climbs again like one over h. A V. "
            f"<bookmark mark='b'/> In float32 the same V sits far higher and further right. <bookmark mark='c'/> The "
            f"bottoms are where the formula said: {verdict}. <bookmark mark='d'/> At its best, float64's check is good "
            f"to {mant(e64)} times ten to the minus {expo(e64)}; float32's only to {mant(e32)} times ten to the minus "
            f"{expo(e32)}. So check gradients in float64, with a step near the cube root of the unit roundoff. "
            f"Chapter seven's nudge of a millionth was close: its error there is about {mant(e6)} times ten to the "
            f"minus {expo(e6)}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(curves[0][0]), Create(curves[0][1]), FadeIn(table[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(curves[1][0]), Create(curves[1][1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(marks), FadeIn(table[1]), FadeIn(table[2]), FadeIn(table[3]))
            vo.wait_until("d")
            self.play(FadeIn(table[4]))
        self.wait(0.3)
        self.clear_scene()
