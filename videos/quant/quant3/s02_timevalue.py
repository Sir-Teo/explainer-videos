from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, PART, VALUE

C_ = {r"V": VALUE, r"D_1": CASH, r"r": QC.IMPLIED, r"g": CASH}


def row(*parts, fs=42):
    return cmath(*parts, colors=C_, font_size=fs)


class TimeValue(VoiceoverScene):
    def construct(self):
        self.card()
        self.pv()
        self.gordon()
        self.sensitivity()

    def card(self):
        c = chapter_card(1, r"Time value", r"What is a dollar next year worth today?", part=PART)
        with self.voiceover("Chapter one. Time value."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pv(self):
        d = definition_card(r"Present value", r"A payment $C$ in $t$ years is worth $C/(1 + r)^t$ today, where $r$ is "
                            r"the return available on investments of the same risk. The net present value (NPV) of a "
                            r"project is the sum over all its cash flows, costs negative.", width=9.6, color=VALUE,
                            font_size=24).to_edge(UP, buff=0.5)
        forms = VGroup(
            MathTex(r"\text{annuity:}\quad C\,\frac{1 - (1 + r)^{-n}}{r}", font_size=36),
            MathTex(r"\text{perpetuity:}\quad \frac{C}{r}", font_size=36),
            MathTex(r"\text{IRR: the } r \text{ at which NPV} = 0", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(d, DOWN, buff=0.6)
        ex = label(rf"a bond paying 5 a year for 10 years, then 100: at 4\%, "
                   rf"${valuation.npv(0.04, [0] + [5] * 9 + [105]):.2f}$; its IRR at a price of 100 is "
                   rf"${100 * valuation.irr([-100] + [5] * 9 + [105]):.2f}\%$", font_size=24, color=GREY_A)
        ex.next_to(forms, DOWN, buff=0.5)
        with self.voiceover(
            "A dollar next year is worth less than a dollar today, because today's dollar could be invested. At a "
            "rate r, a payment in t years is worth that payment divided by one plus r to the t: its present value. "
            "Add up a project's cash flows this way, costs counted as negative, and you have its net present value. "
            "<bookmark mark='a'/> Three closed forms do most of the work: an annuity, a fixed payment for n years; a "
            "perpetuity, a fixed payment forever, worth simply the payment over the rate; and the internal rate of "
            "return, the rate that makes a project's NPV zero. <bookmark mark='b'/> A bond paying five a year for ten "
            "years and then its hundred back is worth a little more than a hundred when rates are four percent, and "
            "its yield at a price of a hundred is exactly five."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in forms], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    def gordon(self):
        rows = [
            row(r"V", r"=", r"\frac{D_1}{1 + r} + \frac{D_1(1 + g)}{(1 + r)^2} + \frac{D_1(1 + g)^2}{(1 + r)^3} + \cdots"),
            row(r"V", r"=", r"\frac{D_1}{1 + r}\sum_{k \ge 0}\Big(\frac{1 + g}{1 + r}\Big)^k"),
            row(r"V", r"=", r"\frac{D_1}{1 + r}\cdot\frac{1 + r}{r - g}", r"=", r"\frac{D_1}{r - g}"),
        ]
        whys = [why(r"a dividend that grows at $g$ forever, discounted at $r$"),
                why(r"a geometric series with ratio $(1+g)/(1+r)$"),
                why(r"it converges when $g < r$: Gordon's growth model (1956)")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-2.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "The model of a share that every analyst knows. Suppose a company pays a dividend D one next year, and "
            "its dividend grows at g every year forever. Its value is the sum of each future dividend, discounted. "
            "<bookmark mark='a'/> Factor out the first term, and what's left is a geometric series, with ratio one "
            "plus g over one plus r. <bookmark mark='b'/> If growth is slower than the discount rate, the series "
            "converges, and the value is the next dividend over r minus g. Myron Gordon's formula, from 1956."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.6)
        self.clear_scene()

    def sensitivity(self):
        rs = np.linspace(0.04, 0.12, 161)
        V = 5 / (rs - 0.03)
        g = axes([0.04, 0.12], [0, 520], x_length=7.6, y_length=4.4, xlabel=r"discount rate $r$",
                 ylabel=r"value of a dividend of 5 growing at 3\%", xticks=[0.05, 0.08, 0.11],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yticks=[0, 100, 200, 300, 400, 500], font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, rs, np.clip(V, 0, 519), VALUE, stroke_width=3.5)
        dots = VGroup(*[Dot(ax.c2p(r, 5 / (r - 0.03)), radius=0.08, color=QC.IMPLIED) for r in (0.08, 0.07, 0.05)])
        labs = VGroup(*[MathTex(rf"r = {int(100 * r)}\%:\ {5 / (r - 0.03):.0f}", font_size=28, color=QC.IMPLIED)
                        for r in (0.08, 0.07, 0.05)]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lesson = wrapped_label(r"value is most sensitive to the discount rate when $r - g$ is small: long-lived, "
                               r"growing cash flows behave like long-dated bonds", 4.4, 23, GREY_A)
        side = VGroup(labs, lesson).arrange(DOWN, aligned_edge=LEFT, buff=0.6).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        with self.voiceover(
            "The formula carries a warning. A dividend of five growing at three percent, discounted at eight: worth "
            "a hundred. <bookmark mark='a'/> Lower the discount rate by one point, to seven, and it is worth a "
            "hundred and twenty-five. To five, and it is worth two hundred and fifty. <bookmark mark='b'/> When the "
            "gap between the discount rate and growth is small, a small change in either moves the value enormously. "
            "That is why long-lived growth companies swing so hard when interest rates change, and it is one answer to "
            "Shiller's puzzle: if the discount rate moves, prices must move a lot."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=2)
            self.play(FadeIn(dots[0]), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots[1]), FadeIn(labs[1]))
            self.play(FadeIn(dots[2]), FadeIn(labs[2]))
            vo.wait_until("b")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()
