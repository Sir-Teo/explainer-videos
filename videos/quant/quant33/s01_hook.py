from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, GOOD, HURDLE, OU_C, PART, RES_C, SPREAD_C, era_strip, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.band()
        self.claims(load("coint"), load("pairs"))
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Statistical Arbitrage")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-three. Statistical arbitrage: trading the gap between prices that ought to move together, on "
            "the bet that the gap will close."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def band(self):
        rng = np.random.default_rng(33)
        T = 250
        common = np.cumsum(0.012 * rng.standard_normal(T))
        s = np.zeros(T)
        for t in range(1, T):
            s[t] = 0.93 * s[t - 1] + 0.012 * rng.standard_normal()
        a, b = 100 * np.exp(common + s / 2), 100 * np.exp(common - s / 2)
        top = axes([0, T], [float(np.floor(min(a.min(), b.min()) / 5) * 5), float(np.ceil(max(a.max(), b.max()) / 5) * 5)],
                   x_length=8.4, y_length=2.4, xlabel="", ylabel=r"two prices", xticks=[], yticks=[], font_size=14)
        top.move_to(UP * 1.5)
        bot = axes([0, T], [-0.1, 0.1], x_length=8.4, y_length=2.0, xlabel=r"days", ylabel=r"the spread",
                   xticks=[0, 125, 250], yticks=[], font_size=14).move_to(DOWN * 1.7)
        ca = curve(top.ax, np.arange(T), a, QC.SPOT, stroke_width=2.5)
        cb = curve(top.ax, np.arange(T), b, QC.DELTA, stroke_width=2.5)
        cs = curve(bot.ax, np.arange(T), np.clip(s, -0.1, 0.1), SPREAD_C, stroke_width=2.5)
        sd = float(np.std(s))
        bands = VGroup(*[DashedLine(bot.ax.c2p(0, k * 2 * sd), bot.ax.c2p(T, k * 2 * sd), color=OU_C, stroke_width=1.5)
                         for k in (-1, 1)])
        zero = DashedLine(bot.ax.c2p(0, 0), bot.ax.c2p(T, 0), color=GREY_C, stroke_width=1)
        ill = illustration(r"illustration: a common trend and a mean-reverting gap")
        with self.voiceover(
            "Two prices that wander together. <bookmark mark='a'/> Each moves like a random walk, so neither can be "
            "predicted. <bookmark mark='b'/> But the gap between them is tied to an elastic band: it stretches and "
            "snaps back. <bookmark mark='c'/> Sell the one that has run ahead and buy the one that lagged, when the gap "
            "is wide; close when it is shut. The market's direction does not matter. Only the band does."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(ca), Create(cb), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(zero), Create(cs), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(bands))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, c, p):
        fr = float(np.mean(c["frac"]))
        cards = VGroup(
            desk_question(r"the textbook promise", r"find pairs whose spread mean-reverts, trade the band, collect a "
                          r"market-neutral return", width=12.4, font_size=20),
            desk_question(r"what this part finds", rf"on the 49 US industries, the distance method lost money over "
                          rf"1964--2020 (Sharpe {p['all']['sharpe']:.2f}); {100 * fr:.0f}\% of industry pairs pass a "
                          rf"cointegration test in a year, against {100 * c['false_positive']:.0f}\% for unrelated random "
                          rf"walks, and a pair that passes is barely more likely to pass the next year", width=12.4,
                          font_size=19),
            desk_question(r"what survives", r"residuals against a factor model, traded with a band chosen for the "
                          r"costs: and an exact theory of that band (the research chapter)", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "That is the textbook promise. <bookmark mark='a'/> This part tests it. <bookmark mark='b'/> On the "
            "forty-nine American industries, the classic pairs rule lost money over half a century. Pairs that pass a "
            f"cointegration test in one year are about {100 * fr:.0f} percent of them, barely twice the rate for random "
            "walks with no connection at all, and passing once says almost nothing about passing again. "
            "<bookmark mark='c'/> What survives is subtler: residuals against a factor model, traded with a band "
            "chosen for the costs, and an exact theory of where that band should be."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Part thirty-two followed trends; this part bets against them, at the scale of days and of "
            "single securities. It uses Part five's Ornstein-Uhlenbeck process, Part seven's cointegration and Kalman "
            "filter, Part thirty-one's factor model and costs, and the crowding of August 2007, which began in exactly "
            "this kind of book."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1969, r"Thorp: Princeton/Newport", I), (1985, r"pairs at Morgan Stanley", I),
                   (1988, r"D. E. Shaw; Medallion", I), (1990, r"Lo--MacKinlay; Lehmann", I),
                   (2006, r"pairs re-run (GGR)", I), (2007, r"the quant quake", I), (2010, r"Avellaneda--Lee; Bertram", I),
                   (2012, r"evaporating liquidity", I), (2015, r"optimal mean reversion", I), (2022, r"deep stat arb", I)]
        strip = era_strip(entries, y0=1965, y1=2026, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Half a century of betting on reversion", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 3), (3, 7), (7, 10)]
        with self.voiceover(
            "Edward Thorp's Princeton/Newport Partners traded hedged convertible arbitrage from 1969; a group at Morgan "
            "Stanley traded pairs of stocks in the mid-1980s; and in 1988 David Shaw founded his firm while Renaissance's "
            "Medallion fund began. <bookmark mark='a'/> Academics measured the reversal it harvested in 1990, re-ran the "
            "pairs rule in 2006, and watched it crowd and crash in 2007. <bookmark mark='b'/> The modern era: residuals "
            "of factor models, optimal trading bands derived for the Ornstein-Uhlenbeck process, liquidity as the "
            "source of the return, and neural networks trained on residual paths."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk in zip(groups, [None, "a", "b"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The history: Morgan Stanley's group, D. E. Shaw, Renaissance",
            r"Pairs by distance, re-run; cointegration and the screening problem",
            r"The Ornstein--Uhlenbeck spread: half-lives and s-scores",
            r"Eigenportfolios and residuals (Avellaneda and Lee); Kalman hedge ratios",
            r"Reversal and lead-lag (Lo and MacKinlay); a network on residual paths",
            r"Liquidity, crowding and decay; the residual book, registered and opened",
            r"For the researcher: the optimal band for a mean-reverting spread, exactly",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: the history; pairs by distance, re-run; cointegration, and why screening for it misleads; the "
            "Ornstein-Uhlenbeck spread and its half-life; residuals against eigenportfolios; hedge ratios that move; "
            "reversal and lead-lag; a network trained on residual paths; liquidity, crowding and decay; a residual book "
            "opened on sealed years; and an exact formula for the best band."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research", "portfolio"))
        with self.voiceover(
            "In the House, the research desk gets a new family of signals, and the portfolio desk a book whose risk is "
            "almost entirely specific: the residuals that Part thirty-one's risk model leaves behind."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
