from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, IM_C, PART, ask, fit_right, illustration, load


class Nickel(VoiceoverScene):
    def construct(self):
        n = load("nickel")
        self.card()
        self.chart(n)
        self.calls()
        self.case()
        self.after()

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

    def calls(self):
        days = [(r"4 March", 28.9), (r"7 March", 48.1), (r"8 March, early", 101.4)]
        g = axes([-0.6, 2.6], [0, 110], x_length=5.6, y_length=4.2, xlabel=r"", ylabel=r"\$ thousand a tonne",
                 xticks=[], yticks=[0, 25, 50, 75, 100], font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (d_, v_) in enumerate(days):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v_)[1]
            b_ = Rectangle(width=0.8, height=y1 - y0, stroke_width=0, fill_color=BAD if i else IM_C,
                           fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0])
            bars.add(VGroup(b_, MathTex(rf"{v_:.1f}", font_size=24).next_to(b_, UP, buff=0.08),
                            label(d_, font_size=16).next_to(ax.c2p(i, 0), DOWN, buff=0.12)))
        q = 100.0  # thousand tonnes, hypothetical
        d1, d2 = q * (days[1][1] - days[0][1]) / 1e3, q * (days[2][1] - days[1][1]) / 1e3
        rows = VGroup(
            label(r"variation margin on a hypothetical short of 100,000 tonnes", font_size=19, color=GREY_A),
            MathTex(rf"\text{{called for 7 March}}: \${d1:.1f}\text{{ billion}}", font_size=28, color=BAD),
            MathTex(rf"\text{{and by the morning of 8 March}}: \${d2:.1f}\text{{ billion more}}", font_size=28, color=BAD),
            wrapped_label(r"payable in cash, the same day, by the members carrying the position: an initial margin set "
                          r"for ordinary moves is a small fraction of this. The approximate prices are the LME's "
                          r"three-month closes and the intraday high, from press reports", 5.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(rows, 6.85)
        with self.voiceover(
            "Put numbers on it. Nickel closed at about twenty-nine thousand dollars a tonne on Friday the fourth of "
            "March, <bookmark mark='a'/> about forty-eight thousand on Monday the seventh, and early on the eighth "
            "it traded above a hundred and one thousand. <bookmark mark='b'/> On a short of a hundred thousand tonnes, "
            f"a size chosen only for the arithmetic, the variation margin called for Monday is {d1:.1f} billion "
            f"dollars, and the next morning's move adds {d2:.1f} billion more. In cash, the same day. Initial margin, "
            "set for ordinary moves, covers a small fraction of that. The question was no longer whether the short "
            "side was solvent, but whether its brokers could find the cash before the clearing house had to declare "
            "them in default."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4))
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
        self.wait(0.4)
        self.clear_scene()

    def after(self):
        cards = VGroup(
            desk_question(r"16 March 2022", r"trading resumed with daily price limits, a new tool for the exchange; the "
                          r"first sessions were halted repeatedly as prices hit them", width=12.0, font_size=21),
            desk_question(r"November 2023", r"the High Court dismissed the judicial review brought by Elliott and Jane "
                          r"Street: the cancellation, of trades worth about \$3.9 billion, was within the exchange's powers",
                          width=12.0, font_size=21),
            desk_question(r"March 2025", r"the Financial Conduct Authority fined the LME \pounds 9.2 million, its first "
                          r"penalty on a recognised exchange, for systems and controls that failed to keep trading orderly "
                          r"from 4 to 8 March 2022", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "What followed. <bookmark mark='a'/> When trading resumed on the sixteenth of March, the exchange imposed "
            "daily price limits, and the market hit them again and again in its first sessions. "
            "<bookmark mark='b'/> In November 2023 the High Court dismissed the challenge brought by Elliott and Jane "
            "Street: cancelling about three point nine billion dollars of trades had been within the exchange's "
            "powers. <bookmark mark='c'/> And in March 2025 the Financial Conduct Authority fined the exchange nine "
            "point two million pounds, the first such penalty on a recognised exchange, for controls that had not kept "
            "the market orderly in those five days. Legal and wise are different questions."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"why might a clearing house prefer to cancel trades rather than let its waterfall work?")
        with self.voiceover("Why might a clearing house prefer to cancel trades rather than let its waterfall work?"):
            self.play(FadeIn(q))
        self.add(illustration(r"LME notices (8 and 16 March 2022); High Court judgment (November 2023); press reports"))
        self.wait(0.5)
        self.clear_scene()
