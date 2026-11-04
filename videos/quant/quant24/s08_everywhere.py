from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, MKT, PART, QMJ, UMD, ask, fit_right, illustration, load


class Everywhere(VoiceoverScene):
    def construct(self):
        e = load("everywhere")
        self.card()
        self.define()
        self.table(e)
        self.combine(e)
        self.paths(e)
        self.carry_idea()
        self.carry(e)
        self.quality(e)
        self.wrap()

    def card(self):
        c = chapter_card(7, r"Value and momentum everywhere; carry; quality", r"Are the factors a feature of stocks, or of "
                         r"markets?", lit=(2013,), part=PART)
        with self.voiceover("Chapter seven. If value and momentum are real, they should appear in every market. Do "
                            "they?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def define(self):
        cards = VGroup(
            desk_question(r"stocks (US, UK, Europe, Japan)", r"value: book to market; momentum: the past year's return, "
                          r"skipping a month", width=12.0, font_size=20),
            desk_question(r"country equity indices", r"value: the index's book to market; momentum: its past year",
                          width=12.0, font_size=20),
            desk_question(r"currencies, commodities, bonds", r"value: the five-year change in the real exchange rate, "
                          r"the negative five-year return, the real bond yield; momentum: the past year, in each",
                          width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Cliff Asness, Tobias Moskowitz and Lasse Pedersen defined value and momentum the same way in eight "
            "markets. <bookmark mark='a'/> In four stock markets, value is book to market and momentum the past year's "
            "return. <bookmark mark='b'/> In country stock indices, the same, at the level of whole countries. "
            "<bookmark mark='c'/> In currencies, commodities and government bonds, value is a measure of long-run "
            "cheapness, such as a currency that has become cheap in real terms over five years, or a commodity that "
            "has fallen for five years; and momentum, again, the past year. No market-specific tuning."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def table(self, e):
        hx = [-4.6, -1.8, 0.2, 2.2, 4.6]
        heads = [r"market", r"value, Sharpe", r"momentum, Sharpe", r"correlation", r"50/50, Sharpe"]
        tab = VGroup(VGroup(*[label(h_, font_size=16, color=GREY_A).move_to([x, 2.65, 0]) for h_, x in zip(heads, hx)]))
        for i, (k, v) in enumerate(e["markets"].items()):
            y = 2.1 - 0.5 * i
            tab.add(VGroup(label(rf"{k} ({v['start'] // 100})", font_size=16).move_to([hx[0], y, 0]),
                           MathTex(f"{v['val']['sharpe']:.2f}", font_size=22, color=HML).move_to([hx[1], y, 0]),
                           MathTex(f"{v['mom']['sharpe']:.2f}", font_size=22, color=UMD).move_to([hx[2], y, 0]),
                           MathTex(f"{v['corr']:.2f}", font_size=22, color=BAD).move_to([hx[3], y, 0]),
                           MathTex(f"{v['combo']['sharpe']:.2f}", font_size=22, color=GOOD).move_to([hx[4], y, 0])))
        foot = wrapped_label(r"AQR's updated Value and Momentum Everywhere factors, from each market's start to 2020. Value "
                             r"and momentum are positive almost everywhere, negatively correlated everywhere, and their "
                             r"50/50 mix beats either alone in every market", 12.4, 16, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The results, updated to 2020. <bookmark mark='a'/> Value has a positive Sharpe ratio in all eight "
            "markets, momentum in all eight, though each is weak somewhere: momentum in Japan, both in bonds. "
            "<bookmark mark='b'/> In every single market their correlation is negative, between about minus a quarter "
            "and minus two thirds. <bookmark mark='c'/> So a fifty-fifty mix beats either one alone, in every market."
        ) as vo:
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_[0]) for r_ in tab[1:]], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(*[FadeIn(r_[1]) for r_ in tab[1:]], *[FadeIn(r_[2]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_[3]) for r_ in tab[1:]])
            vo.wait_until("c")
            self.play(*[FadeIn(r_[4]) for r_ in tab[1:]], FadeIn(foot))
        self.add(illustration(r"AQR data set: Value and Momentum Everywhere, Factors, Monthly"))
        self.wait(0.4)
        self.clear_scene()

    def combine(self, e):
        g = e["global"]
        rows = [cmath(r"SR_{50/50}", r"=", r"\frac{\tfrac12(\mu_V + \mu_M)}{\tfrac12\sqrt{\sigma_V^2 + \sigma_M^2 + 2\rho\,\sigma_V"
                      r"\sigma_M}}", font_size=40, colors={r"SR_{50/50}": GOOD}),
                cmath(r"\rho = -0.59", r"\Rightarrow", r"SR_{50/50} = "
                      rf"{g['combo']['sharpe']:.2f}\ \ (SR_V = {g['val']['sharpe']:.2f},\ SR_M = {g['mom']['sharpe']:.2f})",
                      font_size=38, colors={r"\rho = -0.59": BAD})]
        whys = [why(r"two strategies with similar volatility: the mix keeps the average return and, with negative "
                    r"correlation, loses most of the risk"),
                why(r"all markets together, 1972--2020: global value and momentum each modest, their mix a Sharpe ratio "
                    r"above one. A cheap asset is usually cheap because it has fallen, so it is a momentum loser: the two "
                    r"bets lean against each other")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The arithmetic is chapter one of Part twenty-three. Mix two strategies of similar volatility: the "
            "average return is kept, and with a negative correlation most of the risk cancels. <bookmark mark='a'/> "
            "Across all markets together, value alone has a Sharpe ratio of four tenths and momentum six tenths. "
            "Their correlation is minus six tenths, and the fifty-fifty mix has a Sharpe ratio above one. The reason "
            "is mechanical: an asset is usually cheap because it has fallen, which makes it a momentum loser. Value "
            "and momentum lean against each other, and each covers the other's worst years."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def paths(self, e):
        g = e["global"]
        d = np.asarray(g["date"])
        t = d // 100 + (d % 100 - 0.5) / 12
        ax_ = axes([1972, 2021], [-0.1, 1.1], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"\$1 in 1972, $\log_{10}$",
                   xticks=[1975, 1985, 1995, 2005, 2015], yticks=[0, 0.5, 1.0], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = ax_.ax
        lv = curve(ax, t, np.log10(np.asarray(g["cum_val"])), HML, stroke_width=2.2)
        lm = curve(ax, t, np.log10(np.asarray(g["cum_mom"])), UMD, stroke_width=2.2)
        lc = curve(ax, t, np.log10(np.asarray(g["cum_combo"])), GOOD, stroke_width=3)
        side = VGroup(legend([(HML, r"value, all markets"), (UMD, r"momentum, all markets"), (GOOD, r"the 50/50 mix")],
                             font_size=16),
                      MathTex(rf"\text{{worst drawdown}}:\ {100 * g['val']['maxdd']:.0f}\%,\ {100 * g['mom']['maxdd']:.0f}\%,\ "
                              rf"{100 * g['combo']['maxdd']:.0f}\%", font_size=20),
                      wrapped_label(r"the mix has half the volatility of either, so its dollar grows more slowly on this "
                                    r"scale; levered to the same volatility it would grow far faster. Its worst loss is a "
                                    r"third of either's", 3.6, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here are the paths. <bookmark mark='a'/> Value and momentum, each across all markets, climb in turn: "
            "momentum in the late 1990s while value sank, value in the early 2000s, momentum's crash in 2009. "
            "<bookmark mark='b'/> The mix is a steadier line. Its worst drawdown was ten percent, against about a "
            "third for either alone. It grows more slowly here only because it is half as volatile; levered to the "
            "same risk, it would leave both behind."
        ) as vo:
            self.play(FadeIn(ax_), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lv), Create(lm), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lc), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def carry_idea(self):
        rows = [cmath(r"C_t", r"=", r"\frac{S_t - F_t}{F_t}", font_size=46, colors={r"C_t": GOOD}),
                cmath(r"\mathbb{E}_t[r_{t+1}]", r"=", r"C_t + \mathbb{E}_t\Big[\frac{S_{t+1} - S_t}{F_t}\Big]", font_size=40)]
        whys = [why(r"Koijen, Moskowitz, Pedersen and Vrugt (2018): an asset's carry is the return it earns if its price "
                    r"does not change; with a futures contract, the gap between spot and futures (Part 22's roll and "
                    r"interest differential, in one number)"),
                why(r"so every expected return is carry plus expected price change: a carry strategy, long high carry and "
                    r"short low, bets that prices change less than carry promises. Part 22's currency carry trade is one "
                    r"instance")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A third style travels too: carry. Ralph Koijen, Moskowitz, Pedersen and Evert Vrugt defined an asset's "
            "carry as the return it would earn if its price did not move: for a futures contract, the gap between the "
            "spot price and the futures price. <bookmark mark='a'/> Every expected return is carry plus the expected "
            "price change. A carry strategy, long high carry and short low, bets that prices change less than the "
            "carry promises. Part twenty-two's currency carry trade is one case of it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def carry(self, e):
        c = e["carry"]
        names = list(c)
        g = axes([-0.6, len(names) - 0.4], [0, 0.8], x_length=7.0, y_length=4.2, xlabel=r"", ylabel=r"Sharpe ratio",
                 xticks=[], yticks=[0, 0.2, 0.4, 0.6, 0.8], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, k in enumerate(names):
            v = c[k]["sharpe"]
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.8, height=y1 - y0, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), MathTex(f"{v:.2f}", font_size=22).next_to(ax.c2p(i, v), UP, buff=0.08)))
            labs.add(label(rf"{k} ({c[k]['start'] // 100})", font_size=14, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.15))
        side = VGroup(
            MathTex(r"\text{skewness}:\ " + r",\ ".join(f"{c[k]['skew']:.1f}" for k in names), font_size=22, color=BAD),
            wrapped_label(r"AQR's Century of Factor Premia, carry in four asset classes, from each series' start to 2020. "
                          r"Positive everywhere, strongest in bonds, and negatively skewed in three of four: carry "
                          r"crashes, as Part 22 found in currencies", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "AQR's century of factor premia includes carry in four asset classes. <bookmark mark='a'/> It is positive "
            "in all four, strongest in government bonds, where buying the high-yielding, steep part of the curve has "
            "paid, and weakest in country stock indices. <bookmark mark='b'/> And in three of the four it is "
            "negatively skewed: like currency carry in Part twenty-two, carry pays steadily and loses suddenly."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.add(illustration(r"AQR data set: Century of Factor Premia, Monthly"))
        self.wait(0.4)
        self.clear_scene()

    def quality(self, e):
        q = e["qmj"]
        rows = [cmath(r"\text{quality}", r"=", r"z(\text{profitability}) + z(\text{growth}) + z(\text{safety}) + "
                      r"z(\text{payout})", font_size=36, colors={r"\text{quality}": QMJ})]
        whys = [why(r"Asness, Frazzini and Pedersen (2019): a stock is high quality if investors should pay more for it: "
                    r"profitable, growing, safe (low beta, low leverage, stable earnings) and paying out. Quality minus "
                    r"junk buys the best and sells the worst, within size groups")]
        step = ladder(self, rows, whys, keep=1, top=2.5, x=-0.4, buff=0.8, edge=6.9)
        res = VGroup(
            MathTex(rf"QMJ,\ \text{{US}},\ {q['start'] // 100}\text{{--}}2020:\ {100 * q['mean']:.1f}\%\ \text{{a year}},\ "
                    rf"SR\ {q['sharpe']:.2f},\ t\ {q['t']:.1f}", font_size=28, color=QMJ),
            MathTex(rf"\beta_{{\text{{market}}}} = {q['beta']:.2f}", font_size=28),
            wrapped_label(r"quality pays, and has a negative market beta: it does best in crashes, as investors fly to "
                          r"quality. High-quality stocks are only modestly more expensive than junk, which is the puzzle",
                          11.0, 17, GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "And quality. Cliff Asness, Andrea Frazzini and Lasse Pedersen asked what an investor should pay more for: "
            "a company that is profitable, growing, safe, and paying out its earnings. Score every stock on all four, "
            "buy the best and sell the worst. <bookmark mark='a'/> Since 1957, quality minus junk earned four percent "
            "a year with a Sharpe ratio above a half, and a negative market beta: it does best in crashes, when "
            "investors fly to quality. The puzzle is the price. Quality stocks are only a little more expensive than "
            "junk, too little for what they deliver."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4))
        self.add(illustration(r"AQR data set: Quality Minus Junk, Factors, Monthly"))
        self.wait(0.4)
        self.clear_scene()

    def wrap(self):
        cards = VGroup(
            desk_question(r"a common risk?", r"Asness, Moskowitz and Pedersen: value everywhere loads positively, and "
                          r"momentum negatively, on funding liquidity; the same styles crash together across markets",
                          width=12.0, font_size=20),
            desk_question(r"or common behaviour?", r"extrapolation and slow reaction are not specific to stocks; neither "
                          r"is the arbitrageur's limited capital (Part 23)", width=12.0, font_size=20),
            desk_question(r"for a book", r"diversify across styles and markets first: the cheapest risk reduction there "
                          r"is, and the reason multi-style funds exist", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "What does it mean that the same styles work in such different markets? <bookmark mark='a'/> Perhaps a "
            "common risk: Asness, Moskowitz and Pedersen found value and momentum everywhere loading, in opposite "
            "directions, on funding liquidity. <bookmark mark='b'/> Perhaps common behaviour: extrapolation, slow "
            "reaction and limited arbitrage capital are not specific to stocks. <bookmark mark='c'/> Either way the "
            "lesson for a portfolio is the same: diversify across styles and markets first. It is the cheapest risk "
            "reduction there is."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"momentum and value are negatively correlated. Why hold both, if each has a positive premium? And when "
                r"would holding both disappoint?")
        with self.voiceover("Momentum and value are negatively correlated. Why hold both, if each has a positive premium? "
                            "And when would holding both disappoint?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
