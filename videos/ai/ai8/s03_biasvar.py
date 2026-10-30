from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BIAS, HIST, TEST, VAR, chapter, curve, load


class BiasVariance(VoiceoverScene):
    def construct(self):
        chapter(self, 2, r"Bias and variance, derived", r"Too simple, or too nervous?",
                "Chapter two. Bias and variance.")
        self.fits()
        self.derive()
        self.decomposition()

    # ------------------------------------------------------------------
    def fits(self):
        b = load("biasvar")
        xg, tr = np.asarray(b["xg"]), np.asarray(b["truth"])
        sx, sy = np.asarray(b["sample_x"]), np.asarray(b["sample_y"])
        best = int(b["best"])
        panels = VGroup()
        for k, (key, deg, col) in enumerate((("fits_1", 1, BIAS), ("fits_best", best, TEST), ("fits_top", int(b["top"]), VAR))):
            ax = Axes(x_range=[-1.6, 1.6, 1], y_range=[-2.2, 2.2, 1], x_length=3.9, y_length=3.4, tips=False,
                      axis_config={"stroke_color": GREY_D, "include_ticks": False})
            ax.move_to([-4.4 + 4.4 * k, -0.2, 0])
            truth = DashedVMobject(curve(ax, xg, tr, WHITE, 2.5, smooth=True), num_dashes=40)
            F = np.asarray(b[key])
            fits = VGroup(*[curve(ax, xg, np.clip(f, -2.2, 2.2), col, 1.6).set_stroke(opacity=0.55) for f in F])
            one = curve(ax, xg, np.clip(F[0], -2.2, 2.2), col, 3.5)
            pts = VGroup(*[Dot(ax.c2p(a, c), radius=0.055, color=WHITE) for a, c in zip(sx, sy)])
            t = label(rf"degree ${deg}$", font_size=30, color=col).next_to(ax, UP, buff=0.2)
            panels.add(VGroup(ax, truth, pts, one, fits, t))
        caps = VGroup(label(r"misses the same way \\ every time: \ bias", font_size=24, color=BIAS),
                      label(r"about right", font_size=24, color=TEST),
                      label(r"different every time: \\ variance", font_size=24, color=VAR))
        for c_, p_ in zip(caps, panels):
            c_.next_to(p_[0], DOWN, buff=0.25)
        head = label(r"Sixteen noisy points from one curve, \ drawn again and again \ (illustrative)", font_size=28)
        head.to_edge(UP, buff=0.3)
        poly = gloss(r"polynomial of degree $12$", r"adds up powers of $x$: \ $a_0 + a_1 x + a_2 x^2 + \dots + a_{12} "
                     r"x^{12}$. \\ The degree is the highest power, \ roughly how many bends it can make.",
                     corner=DOWN, width=11.0, color=VAR)
        with self.voiceover(
            "The classical answer starts with a setting small enough to see everything: a smooth curve, and sixteen "
            "noisy points drawn from it. <bookmark mark='a'/> Fit a straight line. Draw sixteen new points and fit "
            "again, and again: it misses the curve's shape in the same way every time. That systematic miss is "
            "bias. <bookmark mark='b'/> Fit a polynomial of degree twelve: a sum of powers of x, up to x to the "
            "twelfth. The degree, the highest power, is roughly how many bends the curve can make. It threads the "
            "points, but each new draw gives a wildly different curve. That's variance. <bookmark mark='c'/> In "
            f"between, at degree {best}, the fits hug the truth."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(VGroup(p[0], p[1], p[2])) for p in panels])
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                i = (0, 2, 1)[k]
                if m == "b":
                    self.play(FadeIn(poly, shift=UP * 0.2))
                elif m == "c":
                    self.play(FadeOut(poly))
                self.play(FadeIn(panels[i][5]), Create(panels[i][3]))
                self.play(LaggedStart(*[Create(f) for f in panels[i][4]], lag_ratio=0.06), FadeIn(caps[i]), run_time=1.6)
        self.wait(2.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        col = {r"\sigma^2": GREY_B, r"\big(f - \bar f\big)^2": BIAS, r"\mathbb{E}\big(\bar f - \hat f\big)^2": VAR}
        rows = [
            cmath(r"\mathbb{E}\big(y - \hat f\big)^2", r"=", r"\mathbb{E}\big(f + \varepsilon - \hat f\big)^2",
                  font_size=36),
            cmath(r"\mathbb{E}\big(y - \hat f\big)^2", r"=", r"\sigma^2", "+", r"\mathbb{E}\big(f - \hat f\big)^2",
                  colors=col, font_size=36),
            cmath(r"\mathbb{E}\big(f - \hat f\big)^2", r"=", r"\mathbb{E}\big(f - \bar f + \bar f - \hat f\big)^2",
                  font_size=36),
            cmath(r"\mathbb{E}\big(f - \hat f\big)^2", r"=", r"\big(f - \bar f\big)^2", "+",
                  r"\mathbb{E}\big(\bar f - \hat f\big)^2", colors=col, font_size=36),
            cmath(r"\mathbb{E}\big(y - \hat f\big)^2", r"=", r"\big(f - \bar f\big)^2", "+",
                  r"\mathbb{E}\big(\bar f - \hat f\big)^2", "+", r"\sigma^2", colors=col, font_size=38),
        ]
        whys = [why(r"$y = f(x) + \varepsilon$, \ noise of mean $0$, variance $\sigma^2$"),
                why(r"$\varepsilon$ is independent of the fit: \ the cross term is $0$"),
                why(r"add and subtract $\bar f = \mathbb{E}\hat f$, \ the average fit"),
                why(r"$\mathbb{E}(\bar f - \hat f) = 0$: \ again no cross term"),
                why(r"bias$^2$ \ + \ variance \ + \ noise")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.6, buff=0.5, edge=6.9)
        head = label(r"at one point $x$, \ averaged over the training sets $S$ \ and the noise", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.3)
        hist = history_card(1992, r"S.~Geman, E.~Bienenstock \& R.~Doursat", r"\textit{Neural Networks and the "
                            r"Bias/Variance Dilemma}: \ the trade-off, named for neural networks", width=6.0,
                            font_size=19, color=HIST).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Why does the error split that way? Fix a point x. The answer y is the true curve f plus noise of "
            "variance sigma squared, and the fit f hat depends on the random training set. <bookmark mark='a'/> The "
            "noise is independent of the fit and averages to zero, so the cross term vanishes: the noise variance "
            "comes off on its own. <bookmark mark='b'/> In what's left, add and subtract the average fit, f bar. "
            "<bookmark mark='c'/> The fit's deviation from its own average also averages to zero, so again no cross "
            "term. <bookmark mark='d'/> Three pieces remain: the average fit's distance from the truth, squared, the "
            "bias; how much the fit varies from sample to sample, the variance; and the noise. Geman, Bienenstock "
            "and Doursat named the dilemma in 1992, for neural networks."
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
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decomposition(self):
        b = load("biasvar")
        degs = np.asarray(b["degs"])
        bias2, var, total = np.asarray(b["bias2"]), np.asarray(b["var"]), np.asarray(b["total"])
        meas = np.asarray(b["measured"])
        noise = float(b["noise"])
        lo, hi = -3, 1.5
        ax = Axes(x_range=[0, 15, 3], y_range=[0, hi - lo, 1], x_length=8.2, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, -0.5, 0])
        xl = label(r"degree of the polynomial: \ flexibility $\longrightarrow$", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v - lo), LEFT, buff=0.1)
                      for v in range(lo, 2)])

        def ly(v):
            return float(np.clip(math.log10(max(v, 10.0 ** lo)), lo, hi) - lo)

        def lc(v, col, sw=4):
            return curve(ax, degs, [ly(x) for x in v], col, sw)

        cb, cv, ct = lc(bias2, BIAS), lc(var, VAR), lc(total, TEST, 5)
        cn = DashedLine(ax.c2p(0, math.log10(noise) - lo), ax.c2p(15, math.log10(noise) - lo), color=GREY_B, stroke_width=2)
        md = VGroup(*[Circle(radius=0.09, color=WHITE, stroke_width=2).move_to(ax.c2p(d_, ly(m_)))
                      for d_, m_ in zip(degs, meas) if ly(m_) < hi - lo])
        colors = {r"\text{bias}^2": BIAS, r"\text{variance}": VAR, r"\text{noise}": GREY_B}
        f = cmath(r"\text{error on new data}", "=", r"\text{bias}^2", "+", r"\text{variance}", "+", r"\text{noise}",
                  colors=colors, font_size=34).to_edge(UP, buff=0.4)
        best = int(b["best"])
        dot = Dot(ax.c2p(best, ly(total[best])), radius=0.09, color=TEST)
        bl = label(rf"best: \ degree ${best}$", font_size=26, color=TEST).next_to(dot, DOWN, buff=0.25)
        names = VGroup(label(r"bias$^2$", font_size=26, color=BIAS).next_to(ax.c2p(2, ly(bias2[2])), RIGHT, buff=0.2),
                       label(r"variance", font_size=26, color=VAR).next_to(cv.get_end(), LEFT, buff=0.15),
                       label(r"noise", font_size=24, color=GREY_B).next_to(cn.get_end(), UP, buff=0.08).shift(LEFT * 0.4))
        mkey = VGroup(Circle(radius=0.09, color=WHITE, stroke_width=2),
                      label(r"measured on fresh noisy points", font_size=22, color=WHITE)).arrange(RIGHT, buff=0.15)
        mkey.to_corner(DR, buff=0.4).shift(UP * 0.8)
        dev = float(np.max(np.abs(meas - total) / total))
        with self.voiceover(
            f"Now measure all three, over {b['runs']} training sets at every degree. <bookmark mark='a'/> Bias "
            "squared falls as the model gets more flexible. <bookmark mark='b'/> Variance rises. "
            "<bookmark mark='c'/> The noise is a floor no model can go below. Their sum is a U, with the best model "
            "at its bottom: flexible enough, and no more. <bookmark mark='d'/> And the circles are the error "
            "measured directly, on fresh noisy points: they sit on the sum, within "
            f"{100 * dev:.0f} percent at every degree. For thirty years this U was the textbook picture: control "
            "the flexibility, and you control the error. Keep it in mind; chapter twelve finds a second descent "
            "beyond its right edge."
        ) as vo:
            self.play(Write(f), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cb), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(names[1]))
            vo.wait_until("c")
            self.play(Create(cn), FadeIn(names[2]))
            self.play(Create(ct), FadeIn(dot), FadeIn(bl))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in md], lag_ratio=0.08), FadeIn(mkey), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()
