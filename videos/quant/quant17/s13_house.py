from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(12, r"The deep hedger in the House", r"Which networks may the desks use, and on what terms?",
                         part=PART)
        with self.voiceover("Chapter twelve. The deep hedger in the House."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("vol", "research")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{calib\_net}, \texttt{calibrate\_neural}", r"rough Bergomi through a network, with a Monte Carlo check"),
            (r"\texttt{train\_differential}", r"differential machine learning"),
            (r"\texttt{deep\_bsde}, \texttt{deep\_stopping}", r"high-dimensional pricing and exercise"),
            (r"\texttt{Hedger}, \texttt{train\_hedger}", r"the deep hedger: plain and band networks, entropic or CVaR"),
            (r"\texttt{NeuralSV}", r"neural SDEs and robust bounds"),
            (r"\texttt{train\_sig\_generator}, \texttt{train\_ddpm}", r"market generators, scored by \texttt{stylized\_facts}"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.4)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 17: no network is used without a slower, independent engine that can check it; inputs "
                             r"outside the region it was trained on go to that engine instead; and a hedger is tested on at "
                             r"least two market generators and on replayed history before it trades.  "
                             rf"No strategy was tested: the trial counter still reads {env['trials']}.", 12.4, 22,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House now has its deep-learning tools. <bookmark mark='a'/> The neural calibrator, with its Monte "
            "Carlo check. Differential machine learning. The deep BSDE solver and deep stopping. The deep hedger, in "
            "both forms. Neural SDEs for model risk. And the market generators, with the stylized facts as their "
            "scorecard. <bookmark mark='b'/> The seventeenth rule: no network is used without a slower, independent "
            "engine that can check it. Inputs outside its training region go to that engine instead. And a hedger is "
            "tested on at least two market generators and on replayed history before it trades. Nothing here tested a "
            f"trading strategy, so the counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
