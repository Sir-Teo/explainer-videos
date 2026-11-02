from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.module(env)

    def card(self):
        c = chapter_card(8, r"The arbitrage checker", r"What must every surface pass before the House prices with it?",
                         part=PART)
        with self.voiceover("Chapter eight. The arbitrage checker."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def module(self, env):
        chart = house_chart(PART, lit=("data",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{parity\_gap}", r"put--call parity, with rates and borrow"),
            (r"\texttt{ftap}", r"state prices or an arbitrage portfolio, by linear programming"),
            (r"\texttt{superhedge}", r"the no-arbitrage interval in an incomplete market"),
            (r"\texttt{static\_checks}, \texttt{calendar\_check}", r"calls decreasing, convex and bounded; variance "
                                                                  r"rising with maturity"),
            (r"\texttt{mot\_bounds}", r"model-free bounds from two expiries"),
            (r"\texttt{ross\_recovery}", r"Perron--Frobenius on state prices, with its caveat"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 5.4)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 10: no model is fitted to a surface that fails the arbitrage checker; it is repaired "
                             r"or rejected first, and a model whose prices fail it is rejected too.  "
                             rf"The trial counter still reads {env['trials']}: this part tested no strategy.", 12.4, 23,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House's arbitrage checker collects this part's tools. <bookmark mark='a'/> Parity, with rates and "
            "borrowing. The fundamental theorem as a linear program, which returns state prices or an arbitrage. "
            "Super-replication for incomplete markets. The static checks: calls must fall and bend the right way "
            "across strikes, and variance must rise with maturity. Model-free bounds. And Ross recovery, with its "
            "warning label. <bookmark mark='b'/> The tenth rule: no model is fitted to a surface that fails these "
            "checks; the surface is repaired or rejected first, and a model whose own prices fail them is rejected "
            f"too. This part tested no strategy, so the trial counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
