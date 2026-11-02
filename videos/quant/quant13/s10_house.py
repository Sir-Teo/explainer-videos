from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(9, r"The calibrator", r"How does the desk turn quotes into a model?", part=PART)
        with self.voiceover("Chapter nine. The calibrator."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{heston\_cf}, \texttt{bates\_cf}, \texttt{vg\_cf}, \texttt{nig\_cf}, \texttt{kou\_jump\_cf}",
             r"characteristic functions, martingale-checked"),
            (r"\texttt{cos\_price}", r"Fang--Oosterlee pricing; Heston benchmark to $10^{-8}$"),
            (r"\texttt{calibrate}", r"vega-weighted fits, multi-start, bounds"),
            (r"\texttt{sabr\_iv}, \texttt{sabr\_density}", r"Hagan's formula, and its arbitrage check"),
            (r"\texttt{heston\_qe}, \texttt{bates\_paths}, \texttt{vg\_paths}", r"simulators, checked against COS prices"),
            (r"\texttt{local\_vol\_paths}, the particle SLV", r"Dupire and its stochastic twin"),
            (r"\texttt{forward\_start}, \texttt{cliquet}", r"exotics that bet on the future smile"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.0)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 13: every model the desk uses is fitted by the calibrator, which logs its error and "
                             r"how far its parameters moved since last week; every exotic is priced under at least two "
                             r"models fitted to the same surface, and the spread is reported as model risk.  "
                             rf"The trial counter still reads {env['trials']}.", 12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The volatility desk now has its calibrator. <bookmark mark='a'/> Characteristic functions for Heston, "
            "Bates, Kou, variance gamma and NIG, each checked to keep the forward a martingale. The COS method, which "
            "reproduces the published Heston benchmark to eight decimals. A vega-weighted fitter. SABR, with a check "
            "on its density. Simulators that agree with the Fourier prices, local volatility and its stochastic twin, "
            "and the exotics that bet on the future smile. <bookmark mark='b'/> The thirteenth rule: every model is "
            "fitted by the calibrator, which logs how well it fits and how far its parameters moved since last week. "
            "And every exotic is priced under at least two models fitted to the same surface, with the spread "
            f"reported as model risk. No strategy was tested, and the counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
