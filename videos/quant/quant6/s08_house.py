from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(7, r"The statistics module", r"What does the House report with every number?", part=PART)
        with self.voiceover("Chapter seven. The statistics module."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("data",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{ols}", r"naive, White, Newey--West, Hansen--Hodrick, one- and two-way clustered errors"),
            (r"\texttt{fama\_macbeth}", r"monthly cross-sections, with Newey--West on the slopes"),
            (r"\texttt{moving\_block\_bootstrap}, \texttt{stationary\_bootstrap}", r"resampling that keeps dependence"),
            (r"\texttt{sharpe\_se}, \texttt{years\_to\_significance}", r"Lo and Mertens errors; the signal-to-noise budget"),
            (r"\texttt{holm}, \texttt{benjamini\_hochberg}", r"family-wise and false-discovery control"),
            (r"\texttt{gmm}, \texttt{dml\_plr}, \texttt{shrink\_means}", r"two-step GMM with $J$; double ML; empirical Bayes"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.0)
        tab.next_to(chart, DOWN, buff=0.35)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 7: no number leaves the House without a standard error that respects how the data "
                             rf"were sampled, and the count of everything tried.  The trial counter reads {env['trials']}.",
                             12.4, 23, QC.HOUSE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The House's statistics module collects this part's tools, each tested against a simulated case with a "
            "known answer. <bookmark mark='a'/> Regression with every standard error we met. Fama-MacBeth. "
            "Bootstraps that keep the dependence in the data. The Sharpe ratio's standard error and the "
            "signal-to-noise budget. Corrections for multiple testing. GMM, double machine learning and shrinkage. "
            "<bookmark mark='b'/> And a seventh rule: no number leaves the House without a standard error that "
            "respects how the data were sampled, and without the count of everything that was tried. This part "
            f"tested forty-nine industries, so the trial counter now reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
