from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import KELLY, OVER, PART, UNDER, illustration, load, tbar


class Hook(VoiceoverScene):
    def construct(self):
        c = load("coin")
        self.title_card()
        self.game(c)
        self.answer(c)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"How much to bet")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part eight. Decisions and control. Part seven forecast how much the market will move. This part asks "
            "the question every trader faces next: given what you believe, how much should you bet?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def game(self, c):
        q = desk_question(r"You have \$25 and a coin that lands heads 60\% of the time. For 30 minutes you may bet any "
                          r"amount on either side, at even odds, as often as you like; winnings are capped at \$250. "
                          r"How much do you bet each time?", width=10.6, font_size=28).to_edge(UP, buff=0.5)
        facts = VGroup(
            label(r"Haghani and Dewey (2016) gave this game to 61 people trained in finance and economics.",
                  font_size=24, color=GREY_A),
            label(r"About 30\% of them went bust.", font_size=30, color=OVER),
            label(r"Many over-bet, some bet erratically, some even bet on tails.", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "Here is a game. You are given twenty-five dollars and a coin that lands heads sixty percent of the time. "
            "For half an hour you may bet as much as you like, on either side, at even odds, as often as you like. "
            "Your winnings are capped at two hundred and fifty dollars. How much do you bet? <bookmark mark='a'/> In "
            "2016 Victor Haghani and Richard Dewey gave this game to sixty-one young people trained in finance and "
            "economics. The edge is enormous, and still about thirty percent of them went bust. Many bet too much; "
            "some even bet on tails."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.6, run_time=4))
        self.wait(0.5)
        self.clear_scene()

    def answer(self, c):
        f, gr = np.asarray(c["f"]), np.asarray(c["growth"])
        ok = np.isfinite(gr) & (gr > -0.06)
        g = axes([0, 0.6], [-0.06, 0.03], x_length=5.6, y_length=3.6, xlabel=r"fraction of wealth bet each flip",
                 ylabel=r"growth per flip", xticks=[0, 0.2, 0.4, 0.6], xfmt=lambda u: f"{100 * u:.0f}\\%",
                 yticks=[-0.04, 0, 0.02], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_corner(UL, buff=0.6)
        ax = g.ax
        line = curve(ax, f[ok], gr[ok], KELLY, stroke_width=4)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.6, 0), color=GREY_C, stroke_width=1.5)
        top = Dot(ax.c2p(0.2, c["g_kelly"]), color=KELLY)
        tl = MathTex(r"f^* = p - q = 20\%", font_size=28, color=KELLY).next_to(top, UP, buff=0.12)
        eq = MathTex(r"g(f) = p\log(1 + f) + q\log(1 - f)", font_size=30).next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        # the outcome of 20,000 simulated players at each fraction
        fr = [k for k in c["by_fraction"]]
        g2 = axes([0, len(fr)], [0, 1], x_length=5.8, y_length=3.6, ylabel=r"share of 20{,}000 simulated players",
                  xticks=[], yticks=[0, 0.5, 1], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g2.to_corner(UR, buff=0.6)
        a2 = g2.ax
        cap = VGroup(*[tbar(a2, i + 0.3, c["by_fraction"][k]["p_cap"], KELLY if k == "0.20" else UNDER, width=0.36)
                       for i, k in enumerate(fr)])
        bust = VGroup(*[tbar(a2, i + 0.7, c["by_fraction"][k]["p_bust"], OVER, width=0.36) for i, k in enumerate(fr)])
        labs = VGroup(*[label(f"{100 * float(k):.0f}\\%", font_size=16, color=GREY_A).next_to(a2.c2p(i + 0.5, 0), DOWN,
                                                                                            buff=0.1)
                        for i, k in enumerate(fr)])
        leg = legend([(UNDER, r"reached \$250"), (OVER, r"went bust (under 1 cent)")], font_size=18)
        leg.next_to(g2, DOWN, buff=0.35).align_to(g2, LEFT)
        k20 = c["by_fraction"]["0.20"]
        k100 = c["by_fraction"]["1.00"]
        src = illustration(r"simulation: 300 flips, 20{,}000 players per fraction")
        with self.voiceover(
            "The answer is older than the game. If you bet a fraction f of your wealth each time, your wealth after "
            "many flips grows at the rate p log of one plus f, plus q log of one minus f, per flip. <bookmark mark='a'/> "
            "That curve peaks at f equals p minus q: twenty percent. It is the Kelly criterion, from 1956. Bet more and "
            "you grow more slowly; bet twice as much, forty percent, and you no longer grow at all; beyond that, a "
            "sure edge makes you poorer. <bookmark mark='b'/> Simulate twenty thousand players at each fraction for three "
            f"hundred flips. At twenty percent, {100 * k20['p_cap']:.0f} percent reach the cap and none go bust. Bet "
            f"everything each time, and {100 * k100['p_bust']:.0f} percent go bust. The coin is the same; only the "
            "size changed."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(line), FadeIn(eq), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(labs), FadeIn(leg), FadeIn(src),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cap], lag_ratio=0.1),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bust], lag_ratio=0.1), run_time=3)
        self.wait(0.5)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Expected utility, risk aversion and the certainty equivalent",
            r"Dynamic programming and the Hamilton--Jacobi--Bellman equation, solved on a grid",
            r"Merton's problem: how much of your wealth to hold in stocks, on 94 years of data",
            r"Kelly, fractional Kelly and Thorp; Samuelson's objection; ergodicity",
            r"Leverage beyond Kelly: LTCM, 1998",
            r"Optimal stopping, prospect theory and ambiguity",
            r"Frontiers: BSDEs, mean-field games, and a reinforcement learner checked against Merton",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Utility, and what risk aversion means in numbers. Dynamic programming, and the equation that "
            "solves every problem of this kind. Merton's answer for how much to hold in stocks, on ninety-four years "
            "of data. Kelly's answer, the controversy around it, and what happens when a fund levers far beyond it. "
            "When to stop. How real people decide. And three frontiers: backward stochastic equations, games with "
            "millions of players, and a reinforcement learner that has to rediscover Merton."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part builds the sizing module: utility, the Merton and Kelly fractions, and the "
            "solvers behind them. <bookmark mark='a'/> Every position the House takes, from Part ten's options to "
            "Part thirty's portfolios, will be sized by it."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["portfolio"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
