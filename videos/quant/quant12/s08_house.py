from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(8, r"The surface builder", r"What surface does the desk quote from?", part=PART)
        with self.voiceover("Chapter eight. The surface builder."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{ssvi\_w}, \texttt{fit\_ssvi}", r"one arbitrage-free formula for the whole surface"),
            (r"\texttt{g\_function}", r"Gatheral's butterfly check, expiry by expiry"),
            (r"\texttt{dupire\_local\_var}", r"local volatility from the surface's slopes"),
            (r"\texttt{var\_swap\_strike}, \texttt{vix}", r"variance from a strip of options; the VIX recipe"),
            (r"\texttt{surface.build}", r"a day of Deribit trades into a surface of quotes (Part 1)"),
            (r"the surface VAE", r"two numbers that describe a day's surface"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 5.6)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 12: the desk quotes only from a fitted surface that passes the arbitrage checker, and "
                             r"every exotic price states which dynamics (local, stochastic, rough) it assumed.  "
                             rf"The trial counter still reads {env['trials']}.", 12.4, 23, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The volatility desk now has its surface builder. <bookmark mark='a'/> One arbitrage-free formula for the "
            "whole surface, and the butterfly check that guards it. Local volatility from its slopes. Variance from "
            "a strip of options, and the VIX recipe. The daily builder that turns a day of trades into quotes. And "
            "a learned summary of a day's surface in two numbers. <bookmark mark='b'/> The twelfth rule: the desk "
            "quotes only from a fitted surface that passes the checker, and every exotic price says which dynamics "
            "it assumed, because, as local volatility's forward smile showed, the same surface can come from very "
            f"different futures. This part tested no strategy, so the counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
