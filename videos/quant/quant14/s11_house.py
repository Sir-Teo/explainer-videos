from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(10, r"The rough lab", r"What does the desk adopt, and on what evidence?", part=PART)
        with self.voiceover("Chapter ten. The rough lab."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("vol",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{rbergomi\_paths}", r"rough Bergomi by the hybrid scheme, any forward variance curve"),
            (r"\texttt{rough\_heston\_cf}", r"the fractional Riccati equation by Adams; COS prices"),
            (r"\texttt{lifted\_heston\_cf}", r"the Markovian lift, $N$ factors"),
            (r"\texttt{log\_rv\_scaling}", r"Gatheral--Jaisson--Rosenbaum's estimator, checked on fBm"),
            (r"\texttt{fit\_pdv}", r"Guyon--Lekeufack path-dependent volatility"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 4.6)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 14: a new model is adopted only if it beats the simpler one out of sample, on the "
                             r"quantity it is for (prices, hedges or forecasts), with its estimator checked on synthetic "
                             r"data whose answer is known.  "
                             rf"The trial counter still reads {env['trials']}.", 12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The volatility desk now has a rough lab. <bookmark mark='a'/> Rough Bergomi, simulated by the hybrid "
            "scheme. Rough Heston, priced through its fractional Riccati equation. The lift that makes it Markovian. "
            "The roughness estimator, tested on processes whose answer is known. And path-dependent volatility. "
            "<bookmark mark='b'/> The fourteenth rule comes out of the debate: a new model is adopted only if it "
            "beats the simpler one out of sample, on the quantity it is meant for, and its estimator has been "
            "checked on synthetic data whose answer is known. Elegance is not evidence. No strategy was tested, and "
            f"the counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
