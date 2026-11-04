from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, COST_C, GOOD, HURDLE, PART, RES_C, SPREAD_C, fit_right, load


class Crowding(VoiceoverScene):
    def construct(self):
        n = load("nagel")
        self.card()
        self.liquidity()
        self.test(n)
        self.scatter(n)
        self.quake()
        self.decay()
        self.question()

    def card(self):
        c = chapter_card(9, r"Liquidity, crowding and decay", r"Who pays the stat-arb trader, and when do they stop?",
                         part=PART)
        with self.voiceover("Chapter nine. A reversal strategy buys from people who are selling in a hurry. Its return is "
                            "the price of that hurry. That idea explains when it pays, when it crashes, and why it fades."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def liquidity(self):
        rows = [cmath(r"\text{reversal}", r"=", r"\text{the price of immediacy}", font_size=38, colors={r"\text{reversal}": RES_C}),
                cmath(r"\text{supply of liquidity}", r"\downarrow", r"\text{when market makers' capital is scarce}", font_size=30),
                cmath(r"\mathbb E[\text{reversal return}]", r"\uparrow", r"\text{with the VIX (Nagel 2012)}", font_size=32,
                      colors={r"\text{with the VIX (Nagel 2012)}": HURDLE})]
        whys = [why(r"Grossman and Miller (1988): an investor who must trade now accepts a worse price; whoever takes the "
                    r"other side is paid when the price recovers"),
                why(r"in a crisis, the market makers' own losses and margin calls cut how much risk they can absorb"),
                why(r"Stefan Nagel: short-term reversal returns in US stocks rise with lagged volatility, peaking in 2008: "
                    r"`evaporating liquidity'")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The theory. <bookmark mark='a'/> Sanford Grossman and Merton Miller: an investor who must trade now accepts a "
            "worse price, and whoever takes the other side is paid when the price recovers. Reversal is the price of "
            "immediacy. <bookmark mark='b'/> In a crisis, the liquidity providers' own capital is scarce. "
            "<bookmark mark='c'/> So the expected return of reversal should rise with market stress. Stefan Nagel found "
            "exactly that for American stocks: reversal returns rise with the VIX, and peaked in 2008."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def test(self, n):
        rows = [cmath(r"\pi_{m}", r"=", r"a + b\,\text{VIX}_{m-1} + e_m", font_size=38),
                cmath(r"\hat b", r"=", rf"{1e4 * n['slope']:+.2f}\ \text{{bp per VIX point}},\quad t = {n['t']:.2f}",
                      font_size=32, colors={r"\hat b": HURDLE}),
                cmath(r"\text{Sharpe}", r"=", rf"{n['sharpe']:.2f}\ \ \text{{(1990--2020, monthly)}}", font_size=32,
                      colors={r"\text{Sharpe}": BAD})]
        whys = [why(r"the contrarian's monthly return on the 49 industries against the VIX at the previous month's end"),
                why(r"no relation on industries"),
                why(r"and the industry contrarian lost money on average: industries trend at these horizons")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The House tests it on its own universe. <bookmark mark='a'/> Regress the industry contrarian's monthly "
            "return on the VIX a month earlier. <bookmark mark='b'/> The slope is indistinguishable from zero, a "
            f"t-statistic of {n['t']:.2f}. <bookmark mark='c'/> And the industry contrarian lost money on average, a "
            f"Sharpe ratio of {n['sharpe']:.2f}. Industries are not where immediacy is sold: they are portfolios of "
            "hundreds of stocks, and the price pressure of a hurried seller washes out inside them."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def scatter(self, n):
        v = np.asarray(n["vix"], float)
        r = 100 * np.asarray(n["ret"], float)
        lim = float(np.ceil(np.percentile(np.abs(r), 99)))
        g = axes([9, 60], [-lim, lim], x_length=7.0, y_length=4.2, xlabel=r"VIX at the previous month's end",
                 ylabel=r"industry contrarian, \% a month", xticks=[10, 30, 50], yticks=[-lim, 0, lim],
                 yfmt=lambda u: f"{u:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(min(a, 60), np.clip(b, -lim, lim)), radius=0.04, color=RES_C, fill_opacity=0.7)
                        for a, b in zip(v, r)])
        zero = DashedLine(ax.c2p(9, 0), ax.c2p(60, 0), color=GREY_C, stroke_width=1)
        st = VGroup(label(rf"calmest fifth of months: {100 * n['low']:+.2f}\%", font_size=16, color=GREY_A),
                    label(rf"most stressed fifth: {100 * n['high']:+.2f}\%", font_size=16, color=GREY_A))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            "Month by month. <bookmark mark='a'/> The calmest fifth of months and the most stressed fifth look the same "
            f"for the industry contrarian: {100 * n['low']:+.2f} and {100 * n['high']:+.2f} percent a month. "
            "<bookmark mark='b'/> The lesson is about the universe, not the theory: the liquidity premium lives where "
            "hurried selling moves prices, in single stocks, small caps, and the residuals of a factor model."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.005), FadeIn(st))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def quake(self):
        cards = VGroup(
            desk_question(r"August 2007, again", r"Part 31: the market-neutral stat-arb books lost heavily in three days "
                          r"as a crowd unwound the same positions; Khandani and Lo's contrarian lost and rebounded within "
                          r"the week", width=12.4, font_size=19),
            desk_question(r"why stat arb is crowd-prone", r"the same data, the same factor models, the same residuals and "
                          r"similar bands lead different firms to the same trades", width=12.4, font_size=19),
            desk_question(r"why it rebounds", r"forced selling is immediacy demanded at any price: those who could hold "
                          r"on were paid the largest reversal premium of the decade", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Crowding is the other face of liquidity. <bookmark mark='a'/> August 2007, from Part thirty-one: market-neutral "
            "stat-arb books lost heavily in three days as a crowd unwound the same positions, then rebounded. "
            "<bookmark mark='b'/> Stat arb is especially prone to crowds, because the same data and the same factor "
            "models lead different firms to the same residual trades. <bookmark mark='c'/> And the rebound is the theory "
            "again: forced selling is immediacy demanded at any price, and those who could hold on were paid the largest "
            "reversal premium of the decade."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def decay(self):
        cards = VGroup(
            desk_question(r"competition", r"Avellaneda and Lee found their residual strategy's returns on US stocks fell "
                          r"after the early 2000s; the distance rule decayed after the 1980s (Do and Faff)", width=12.4,
                          font_size=19),
            desk_question(r"speed", r"as more firms trade the same reversal, it is harvested faster: the edge moves to "
                          r"shorter horizons, intraday and then to market making (Part 38)", width=12.4, font_size=19),
            desk_question(r"costs decide", r"what remains is a few basis points a trade, and the firm with the cheapest "
                          r"execution keeps it: Chapter 10's book is judged net of costs", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And decay. <bookmark mark='a'/> Avellaneda and Lee found that their residual strategy's returns on American "
            "stocks fell after the early 2000s, as the distance rule had after the 1980s. <bookmark mark='b'/> As more "
            "firms trade a reversal, it is harvested faster, and the edge moves to shorter horizons, then into market "
            "making, Part thirty-eight's subject. <bookmark mark='c'/> What remains is a few basis points a trade, and the "
            "firm with the cheapest execution keeps it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a reversal strategy earns 2 bp a day before costs and trades 40\% of its book daily at 5 bp per "
                       r"side. What does it earn after costs?")
        with self.voiceover(
            "Pause and predict. A reversal strategy earns two basis points a day before costs, and trades forty percent "
            "of its book daily at five basis points a side. What does it earn after costs?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
