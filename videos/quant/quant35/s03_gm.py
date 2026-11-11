from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import micro as M
from videos.quant.quant35.common import (ASK_C, BAD, BID_C, DEALER_C, GOOD, HURDLE, INF_C, NOISE_C, PART, PRICE_C,
                                         VALUE_C, fit_right, load)

MUC = {"0.1": QC.SPOT, "0.3": QC.DELTA, "0.5": QC.LOSS}


class GM(VoiceoverScene):
    def construct(self):
        g = load("gm")
        self.card()
        self.setup_()
        self.quotes()
        self.number()
        self.spread(g)
        self.belief(g)
        self.learning(g)
        self.events()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(2, r"Glosten and Milgrom: the spread as insurance", r"Why is there a spread when dealers are "
                         r"competitive and do not mind risk?", part=PART)
        self.add(c)
        with self.voiceover("Chapter two. Suppose dealers are competitive, so they earn nothing on average, and do not "
                            "mind risk, so inventory costs nothing. Is there still a spread? In 1985 Lawrence Glosten "
                            "and Paul Milgrom showed there must be, and Part eleven ran their market. Here it is derived."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"V", r"\in", r"\{0, 1\},\quad \Pr(V = 1) = p", font_size=38, colors={r"V": VALUE_C}),
                cmath(r"\text{informed}", r":", r"\text{probability } \mu;\ \text{buy if } V = 1,\ \text{sell if } V = 0",
                      font_size=30, colors={r"\text{informed}": INF_C}),
                cmath(r"\text{uninformed}", r":", r"\text{probability } 1 - \mu;\ \text{buy or sell, one half each}",
                      font_size=30, colors={r"\text{uninformed}": NOISE_C}),
                cmath(r"\text{dealer}", r":", r"\text{competitive, risk-neutral: zero expected profit per trade}",
                      font_size=30, colors={r"\text{dealer}": DEALER_C})]
        whys = [why(r"an asset worth one or nothing; the market's belief is $p$"),
                why(r"some traders know the value and trade on it"),
                why(r"the rest trade for their own reasons: liquidity, rebalancing, hedging"),
                why(r"one trader arrives at a time, and trades one unit at the dealer's quote")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The model. <bookmark mark='a'/> An asset is worth one or nothing; the market believes one with probability "
            "p. <bookmark mark='b'/> A fraction mu of traders know the value and trade on it. <bookmark mark='c'/> The "
            "rest buy or sell at random, for their own reasons. <bookmark mark='d'/> And the dealer is competitive and "
            "risk-neutral: it expects to make nothing on each trade."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def quotes(self):
        rows = [cmath(r"\text{ask}", r"=", r"\mathbb E[V \mid \text{buy}]", font_size=38, colors={r"\text{ask}": ASK_C}),
                cmath(r"\Pr(V = 1 \mid \text{buy})", r"=", r"\frac{p\,(\mu + \frac{1-\mu}{2})}{p\,(\mu + \frac{1-\mu}{2}) + "
                      r"(1-p)\frac{1-\mu}{2}}", font_size=32),
                cmath(r"p = \tfrac12", r":", r"\text{ask} = \tfrac{1 + \mu}{2},\quad \text{bid} = \tfrac{1 - \mu}{2},\quad "
                      r"\text{spread} = \mu", font_size=32, colors={r"\text{spread} = \mu": HURDLE})]
        whys = [why(r"zero profit on a buy means the ask equals the value expected, given that someone chose to buy: "
                    r"the trade itself is information"),
                why(r"Bayes' rule: buys are more likely when the value is high, because the informed buy then"),
                why(r"from an even prior, the spread equals the share of informed traders")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The quotes. <bookmark mark='a'/> To make nothing on a buy, the ask must equal the value expected given that "
            "someone chose to buy. The trade itself is information. <bookmark mark='b'/> By Bayes' rule a buy is more "
            "likely when the value is high, because the informed buy then. <bookmark mark='c'/> From an even prior, the "
            "ask is one plus mu over two, the bid one minus mu over two, and the spread is exactly mu: the share of "
            "informed traders. The uninformed pay the spread; the dealer passes it to the informed."
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

    def number(self):
        a, b = M.gm_quotes(0.5, 0.3)
        a2, b2 = M.gm_quotes(0.8, 0.3)
        rows = [cmath(r"\mu = 0.3,\ p = 0.5", r":", rf"\text{{bid}} = {b:.3f},\ \text{{ask}} = {a:.3f}", font_size=34),
                cmath(r"\mu = 0.3,\ p = 0.8", r":", rf"\text{{bid}} = {b2:.3f},\ \text{{ask}} = {a2:.3f}", font_size=34),
                cmath(r"\text{spread}", r"\to", r"0\ \text{as}\ p \to 0\ \text{or}\ 1", font_size=34, colors={r"\text{spread}": GOOD})]
        whys = [why(r"three in ten traders informed: the spread is 0.3 at an even prior"),
                why(r"after the belief has moved toward one, the quotes rise and the spread narrows, to "
                    rf"{a2 - b2:.3f}"),
                why(r"when the market is nearly sure, there is little left for the informed to know")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "With numbers. <bookmark mark='a'/> Three in ten traders informed, and an even prior: a bid of point three "
            "five and an ask of point six five. <bookmark mark='b'/> Once the belief has moved to point eight, the "
            f"quotes rise and the spread narrows, to {a2 - b2:.2f}. <bookmark mark='c'/> And as the market becomes sure, "
            "the spread vanishes: there is nothing left for the informed to know."
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

    def spread(self, g):
        g_ = axes([0, 80], [0, 0.5], x_length=7.4, y_length=4.4, xlabel=r"trades", ylabel=r"average spread",
                  xticks=[0, 20, 40, 60, 80], yticks=[0, 0.25, 0.5], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g_.ax
        lines = VGroup(*[curve(ax, np.arange(80), np.asarray(g[k]["spread"], float), MUC[k], stroke_width=3) for k in MUC])
        leg = legend([(MUC[k], rf"$\mu = {k}$") for k in MUC], font_size=16).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        t3 = g["0.3"]["to99"]
        self.add(g_, lines[0], leg)
        with self.voiceover(
            f"""Four hundred paths, each conditioned on true value one. <bookmark mark='a'/> The initial spread equals mu and typically narrows as beliefs learn. With more informed arrivals it starts wider. For mu point three the saved median crossing index is {t3:.0f}. The arrays record beliefs before each trade, through seventy-nine updates; a non-crossing path receives the sentinel eighty. This is a capped, conditional summary, not an uncensored population learning time."""
        ) as vo:
            self.play(FadeIn(g_), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def belief(self, g):
        g_ = axes([0, 80], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"trades", ylabel=r"the price, $\mathbb E[V]$",
                  xticks=[0, 20, 40, 60, 80], yticks=[0, 0.5, 1], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g_.ax
        ex = np.asarray(g["0.3"]["example"], float)
        c1 = curve(ax, np.arange(len(ex)), ex, PRICE_C, stroke_width=2.5)
        c2 = curve(ax, np.arange(80), np.asarray(g["0.3"]["belief"], float), HURDLE, stroke_width=3)
        val = DashedLine(ax.c2p(0, 1), ax.c2p(80, 1), color=VALUE_C, stroke_width=2)
        leg = legend([(PRICE_C, r"one run"), (HURDLE, r"the average of 400"), (VALUE_C, r"the value")],
                     font_size=16).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        self.add(g_, c1, val, leg)
        with self.voiceover(
            "The price path. <bookmark mark='a'/> Buys and sells update the dealer's belief by Bayes' rule. <bookmark mark='b'/> The average shown rises because every simulation here conditions on the high true value. Under the full prior mixture and the dealer's own information, the correctly specified conditional expectation is a martingale. Conditional drift when the value is fixed high does not contradict that statement. Finite eighty-trade paths need not learn the value exactly."
        ) as vo:
            self.play(FadeIn(g_), Create(val), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2)
            vo.wait_until("b")
            self.play(Create(c2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def learning(self, g):
        import math
        mu = 0.3
        r = (1 + mu) / (1 - mu)
        n_net = math.log(99) / math.log(r)
        rows = [cmath(r"\frac{p}{1-p}", r"\times", r"\frac{1+\mu}{1-\mu}\ \text{after a buy},\ \ \div\ \text{after a sell}",
                      font_size=32),
                cmath(r"\text{net buys to reach } 99\%", r"=", r"\frac{\ln 99}{\ln\frac{1+\mu}{1-\mu}}", font_size=34),
                cmath(r"\mu = 0.3", r":", rf"{n_net:.1f}\ \text{{net buys}} \approx {n_net / mu:.0f}\ \text{{trades}}",
                      font_size=34, colors={r"\mu = 0.3": HURDLE})]
        whys = [why(r"Bayes' rule in odds: each buy multiplies the odds of a high value by the same factor, each sell divides "
                    r"by it"),
                why(r"so the belief depends only on buys minus sells, and reaching 99\% needs a fixed number of net buys"),
                why('conditional on the high value, expected net buys grow at rate $\\mu$; dividing the log-odds threshold by this drift is a heuristic, not a median or exact first-passage mean')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        t3 = g["0.3"]["to99"]
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Odds make the update simple. <bookmark mark='a'/> A buy multiplies the odds by one plus mu over one minus mu; a sell divides by the same factor. <bookmark mark='b'/> Starting from equal odds, strictly crossing ninety-nine percent requires an integer net-buy count above the displayed logarithmic threshold. <bookmark mark='c'/> At mu point three that real-valued threshold is {n_net:.1f}. Dividing by drift mu gives roughly {n_net / mu:.0f} trades, only a heuristic. The saved capped median index is {t3:.0f}; these are different statistics, and non-hits are censored at eighty."""
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

    def events(self):
        cards = VGroup(
            desk_question(r"before announcements", r"spreads widen and depth thins ahead of scheduled news such as earnings, "
                          r"when the share of traders who may know more is highest", width=12.4, font_size=25),
            desk_question(r"after announcements", r"once the news is public, the informed share collapses and spreads "
                          r"narrow, even though volatility is high: a test that separates information from inventory",
                          width=12.4, font_size=25),
            desk_question(r"small, obscure stocks", r"fewer analysts, more scope for private information: wider spreads "
                          r"for the same volatility and volume", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "The model's predictions, as studies have found them. <bookmark mark='a'/> Spreads widen and depth thins "
            "before scheduled news, when the share of traders who may know more is highest. <bookmark mark='b'/> Once the "
            "news is public, spreads narrow even though volatility is high, a test that separates information from "
            "inventory. <bookmark mark='c'/> And small, obscure stocks, with fewer analysts and more room for private "
            "information, carry wider spreads for the same volume."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the spread is not a profit", r"competitive dealers earn nothing: they collect the spread from "
                          r"the uninformed and lose it to the informed", width=12.4, font_size=25),
            desk_question(r"the uninformed pay for price discovery", r"every liquidity trader pays half the spread so that "
                          r"the price learns the value", width=12.4, font_size=25),
            desk_question(r"too much information closes the market", r"if the informed are numerous enough, the spread "
                          r"exceeds what liquidity traders will pay, and trade stops: Akerlof's lemons", width=12.4,
                          font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "The lessons. <bookmark mark='a'/> The spread is not the dealer's profit: competitive dealers collect it from "
            "the uninformed and lose it to the informed. <bookmark mark='b'/> The uninformed pay for price discovery. "
            "<bookmark mark='c'/> And if the informed are numerous enough, the spread exceeds what anyone else will pay, "
            "and trade stops: George Akerlof's market for lemons, in a quote."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        eq = MathTex('p_0=0.5,\\quad\\mu=0.4,\\quad a(p)=\\frac{p(1+\\mu)}{p(1+\\mu)+(1-p)(1-\\mu)}', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('Binary values 0 and 1; independent noise buys/sells equally. Observe one buy, update the belief, then quote for the next trader.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover('Pause and predict. Start from an even prior with forty percent informed in the binary-value model. Observe one buy. Derive the new belief and then the next ask and bid; distinguish the executed ask from the next quotes.'):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()
