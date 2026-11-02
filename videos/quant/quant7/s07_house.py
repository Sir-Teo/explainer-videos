from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(6, r"The volatility forecaster", r"How does the House forecast risk, and keep itself honest?",
                         part=PART)
        with self.voiceover("Chapter six. The volatility forecaster."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("data",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{realized\_variance}, \texttt{bipower\_variation}", r"measures from intraday prices, with and without jumps"),
            (r"\texttt{two\_scale\_rv}, \texttt{realized\_kernel}", r"measures that correct for microstructure noise"),
            (r"\texttt{garch\_fit} (GARCH, GJR, EGARCH), \texttt{dcc\_fit}", r"maximum likelihood; dynamic correlation"),
            (r"\texttt{har\_fit}, \texttt{har\_predict}", r"HAR and HARQ by least squares"),
            (r"\texttt{markov\_switching}, \texttt{kalman\_local\_level}", r"hidden regimes and hidden levels"),
            (r"\texttt{adf}, \texttt{engle\_granger}", r"unit roots and cointegration"),
            (r"\texttt{qlike}, \texttt{diebold\_mariano}", r"robust losses and tests of forecast accuracy"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.4)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 8: every forecast is scored out of sample, against a simple benchmark, with a loss "
                             r"that is robust to noise in what it is judged against.  "
                             rf"Eight models raced, one added after a first look: the trial counter reads {env['trials']}.",
                             12.4, 23, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House's data desk now carries a volatility forecaster, the engine the volatility desk will run on "
            "when it opens in Part ten. "
            "<bookmark mark='a'/> Realized measures from intraday prices, with and without jumps, and corrected for "
            "noise. The GARCH family by maximum likelihood, and dynamic correlation. HAR and HARQ. Regimes and the "
            "Kalman filter. Tests for unit roots and cointegration. And the scoring: QLIKE and the Diebold-Mariano "
            "test, each checked against simulated data with a known answer. <bookmark mark='b'/> The eighth rule: "
            "every forecast is scored out of sample, against a simple benchmark, with a loss that stays honest when "
            "the target is measured with noise. The race was registered before it was run, and the model we added "
            f"after the first look was registered too: eight in all, so the trial counter now reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
