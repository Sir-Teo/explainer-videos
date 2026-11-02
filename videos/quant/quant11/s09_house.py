from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(8, r"The options quoting engine", r"How does the volatility desk make a market?", part=PART)
        with self.voiceover("Chapter eight. The options quoting engine."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{Leg}, \texttt{book\_value}, \texttt{book\_greeks}", r"a book as one Taylor series"),
            (r"\texttt{pnl\_surface}, \texttt{strategies}", r"what each structure is a bet on"),
            (r"\texttt{hedge.delta\_hedge}", r"gamma and theta, accounted hour by hour (Part 10)"),
            (r"\texttt{quote}", r"bids and offers in volatility, leaning against vega inventory"),
            (r"\texttt{implied\_correlation}", r"index against components"),
            (r"\texttt{ww\_band}, \texttt{hedge\_with\_band}", r"hedging that knows what trading costs"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.4)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 11: every quote leans against inventory and has a limit in each Greek; every hedge "
                             r"is net of costs; and no position is held into expiry near its strike without a plan for "
                             rf"the pin.  The trial counter reads {env['trials']}.", 12.4, 23, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The volatility desk now has its quoting engine. <bookmark mark='a'/> A book of options as one Taylor "
            "series. The P&L map of every structure. Part ten's hedging ledger. Quotes in volatility that lean "
            "against inventory. Implied correlation for index against members. And hedging bands that know what "
            "trading costs. <bookmark mark='b'/> The eleventh rule: every quote leans against inventory and stays "
            "within a limit in each Greek; every hedge is judged net of costs; and nothing is held into expiry near "
            "its strike without a plan for the pin. This part registered one test, the forecaster's edge, so the "
            f"trial counter reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
