from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import MART, P_C, PART, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        e = load("eprocess")
        self.title_card()
        self.betting(e)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Can you beat a fair game?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part four. Martingales and measure. The first act asked whether prices are a fair game. This act builds "
            "the mathematics that makes the question precise, and its first tool is the oldest idea in gambling: a "
            "fair bet."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def betting(self, e):
        old, new = e["19260701"], e["20000101"]
        g = axes([1926, 2021], [-2, 105], x_length=6.4, y_length=4.4, ylabel=r"wealth from \$1, betting since 1926",
                 xticks=[1930, 1960, 1990, 2020], xfmt=lambda x: f"{int(x)}", yticks=[0, 25, 50, 75, 100],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        t0, l0 = np.asarray(old["t"]), np.asarray(old["loge"])
        line0 = curve(ax, t0, l0, P_C, stroke_width=2.5)
        g2 = axes([2000, 2021], [-1, 2], x_length=4.6, y_length=2.4, ylabel=r"betting since 2000",
                  xticks=[2000, 2010, 2020], xfmt=lambda x: f"{int(x)}", yticks=[-1, 0, 1, 2],
                  yfmt=lambda u: {-1: "0.1", 0: "1", 1: "10", 2: "100"}[int(u)], font_size=16)
        g2.to_corner(DR, buff=0.6).shift(UP * 0.2)
        ax2 = g2.ax
        t1, l1 = np.asarray(new["t"]), np.asarray(new["loge"])
        line1 = curve(ax2, t1, l1, MART, stroke_width=2.5)
        bar = DashedLine(ax2.c2p(2000, np.log10(20)), ax2.c2p(2021, np.log10(20)), color=QC.LOSS, stroke_width=2)
        barl = label(r"20", font_size=18, color=QC.LOSS).next_to(ax2.c2p(2021, np.log10(20)), RIGHT, buff=0.08)
        bar0 = DashedLine(ax.c2p(1926, np.log10(20)), ax.c2p(2021, np.log10(20)), color=QC.LOSS, stroke_width=2)
        i29 = int(np.argmax(l0 >= np.log10(20)))
        dot29 = Dot(ax.c2p(t0[i29], l0[i29]), radius=0.07, color=YELLOW)
        side = VGroup(
            label(r"each day, bet that today's return keeps yesterday's sign", font_size=21, color=GREY_A),
            MathTex(rf"\text{{from 1926: }} 10^{{{int(np.log10(old['max']))}}}\text{{; past 20 in Feb.\ 1929}}",
                    font_size=28, color=P_C),
            MathTex(rf"\text{{from 2000: at most }} {new['max']:.1f}", font_size=28, color=MART),
            wrapped_label(r"20 is the line: a fair game reaches it with probability at most 5\%, however often you "
                          r"look", 5.2, 20, QC.LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for m_ in side:
            if m_.width > 5.4:
                m_.scale_to_fit_width(5.4)
        side.to_corner(UR, buff=0.4)
        src = real_data(r"Kenneth French's daily US market, 1926--2020; bets sized by the House's e-process (chapter 9)",
                        corner=DL)
        with self.voiceover(
            "Here is a gambler who bets against the American stock market, every day since 1926, on one thing: that "
            "today's return will have the same sign as yesterday's. The bets are sized with care and never risk "
            "everything. <bookmark mark='a'/> If the market were a fair game for this bet, the gambler's wealth "
            "would be a martingale, and a theorem from 1939 says it would almost never reach twenty times its "
            "start, however long we watched. It reached twenty in February 1929, and went on to ten to the "
            "hundredth. In the old market, yesterday's sign really did predict today's. "
            "<bookmark mark='b'/> Start the same gambler in 2000, and the wealth wanders and never reaches twenty. "
            "<bookmark mark='c'/> This is testing by betting: a way to ask whether a market is fair that stays "
            "honest no matter how often you look. By the end of this part you will know why it works."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            self.play(Create(line0), run_time=3)
            vo.wait_until("a")
            self.play(Create(bar0), FadeIn(side[3]), FadeIn(dot29))
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(bar), FadeIn(barl))
            self.play(Create(line1), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Information as a filtration; conditional expectation as a projection",
            r"Martingales: Ville's fair games, Doob's theory, and the optional stopping theorem",
            r"Why doubling escapes the theorem, gambler's ruin, bold play, and Barings (1995)",
            r"Doob's decomposition: drift plus martingale, on 94 years of the market",
            r"Change of measure on a coin: Radon--Nikodym, and what equivalent measures agree on",
            r"Heavy tails as stable laws (L\'evy, Mandelbrot, Fama, Mantegna--Stanley)",
            r"Testing by betting: e-values, Ville's inequality, anytime-valid inference",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Information, as a growing family of questions you can answer, and conditional expectation as "
            "a projection. Martingales, and the optional stopping theorem. Why the doubling system escapes it, the "
            "gambler's ruin, the best way to bet in a game you will lose, and the doubling trader who broke Barings. "
            "Doob's decomposition of the market into drift and martingale. A change of measure on a coin, the seed "
            "of risk-neutral pricing. Heavy tails as stable laws. And testing by betting."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part adds a monitor to the data desk: an e-process that can watch any strategy or "
            "any market every day, and raise its hand only when the evidence is real. <bookmark mark='a'/> The "
            "research desk will inherit it, when it starts testing hundreds of ideas at once."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
