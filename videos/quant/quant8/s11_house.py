from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(10, r"The sizing module", r"How big is every position the House takes?", part=PART)
        with self.voiceover("Chapter ten. The sizing module."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("data",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{crra}, \texttt{certainty\_equivalent}, \texttt{pratt\_premium}", r"utility and the price of risk"),
            (r"\texttt{merton\_fraction}, \texttt{bellman\_merton}", r"Merton by formula and by dynamic programming"),
            (r"\texttt{kelly\_binary}, \texttt{realized\_growth}", r"Kelly, and growth measured on history"),
            (r"\texttt{secretary}, \texttt{trees.crr}", r"optimal stopping"),
            (r"\texttt{bsde\_regression}, \texttt{hjb\_two\_rates}", r"nonlinear pricing, two ways"),
            (r"\texttt{ppo\_merton}", r"a reinforcement learner, checked against the closed form"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.6)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 9: no position is sized above the Kelly fraction of its estimated edge; the default "
                             r"is half of that; and sizes are recomputed whenever the volatility forecast changes.  "
                             rf"The trial counter reads {env['trials']}.", 12.4, 23, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House's sizing module collects this part's tools, each checked against a closed form. "
            "<bookmark mark='a'/> Utility and certainty equivalents. Merton's fraction, by formula and by a grid "
            "solver. Kelly, and growth measured directly on history. Optimal stopping. Nonlinear pricing by a BSDE and "
            "by a PDE. And a reinforcement learner that must agree with Merton before it is trusted with anything "
            "harder. <bookmark mark='b'/> And a ninth rule: no position is sized above the Kelly fraction of its "
            "estimated edge; the default is half of that, for the doubt in the estimate; and every size is "
            "recomputed whenever the volatility forecast changes, so that a calm-market size never meets a storm. "
            f"This part registered one test, so the trial counter reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
