from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, IM_C, PART, ask, fit_right, illustration, load


class Nickel(VoiceoverScene):
    def construct(self):
        n = load("nickel")
        self.card()
        self.chart(n)
        self.case()

    def card(self):
        c = chapter_card(11, r"March 2022: the LME's nickel market", r"What does a clearing house do when prices run "
                         r"away?", lit=(2022,), part=PART)
        with self.voiceover("Chapter eleven. March 2022: the London Metal Exchange's nickel market."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def chart(self, n):
        t, v = np.asarray(n["t"]), np.asarray(n["v"]) / 1e3
        g = axes([2015, 2026], [0, 40], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"nickel, \$ thousand a tonne",
                 xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 10, 20, 30, 40], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, IM_C, stroke_width=3)
        mx = n["max"]
        side = VGroup(
            MathTex(rf"\text{{March 2022 average}}: \${mx['v'] / 1e3:.1f}\text{{k}}", font_size=26),
            wrapped_label(r"a monthly average hides the days: on 7--8 March the LME price more than tripled in under two "
                          r"days, passing \$100{,}000 a tonne early on 8 March", 3.6, 17, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Nickel, month by month, from the IMF's commodity prices. March 2022 looks like a spike. "
            "<bookmark mark='a'/> Inside that month were two days that a monthly average cannot show. After Russia "
            "invaded Ukraine, nickel rose on the seventh of March, and early on the eighth it passed one hundred "
            "thousand dollars a tonne, more than three times its level a week before."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.add(illustration(r"FRED: PNICKUSDM (IMF, monthly average)"))
        self.wait(0.4)
        self.clear_scene()

    def case(self):
        cc = crisis_card(r"8 March 2022", r"The LME suspends nickel and cancels the day's trades",
                         r"a large short position, held by a Chinese producer partly through banks' over-the-counter "
                         r"positions, faced margin calls running into billions; members could not pay their own calls. "
                         r"The exchange halted trading and cancelled all nickel trades done that day, worth several "
                         r"billion dollars, to avoid member defaults through its clearing house",
                         stats=[(r"> \$100{,}000", r"a tonne, intraday, 8 March"), (r"\text{cancelled}", r"8 March's trades")],
                         width=8.6, font_size=20).move_to(UP * 0.4)
        foot = wrapped_label(r"the cancellation was challenged in court by traders who had been on the right side; the "
                             r"High Court ruled in 2023 that the exchange had acted within its powers. The lesson for a "
                             r"clearing house: margin that cannot be paid in time is not a buffer", 11.5, 19,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A Chinese nickel producer held a very large short position, partly through banks' over-the-counter "
            "contracts that were themselves hedged on the exchange. As the price ran away, margin calls on the short "
            "side ran into billions, and some of the exchange's members could not meet their own. "
            "<bookmark mark='a'/> On the eighth of March the London Metal Exchange halted trading and cancelled every "
            "nickel trade done that day, to stop defaults cascading through its clearing house. Traders who had been "
            "on the right side sued; in 2023 the High Court found that the exchange had acted within its powers. "
            "Margin that cannot be paid in time is not a buffer; it is the beginning of a default."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        q = ask(r"why might a clearing house prefer to cancel trades rather than let its waterfall work?")
        with self.voiceover("Why might a clearing house prefer to cancel trades rather than let its waterfall work?"):
            self.play(FadeIn(q))
        self.add(illustration(r"LME notices (8 and 16 March 2022); High Court judgment (November 2023); press reports"))
        self.wait(0.5)
        self.clear_scene()
