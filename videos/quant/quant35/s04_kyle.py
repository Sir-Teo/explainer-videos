from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import (BAD, DEALER_C, FLOW_C, GOOD, HURDLE, INF_C, NOISE_C, PART, PRICE_C, VALUE_C,
                                         fit_right, load)


class Kyle(VoiceoverScene):
    def construct(self):
        k = load("kyle")
        self.card()
        self.setup_()
        self.guess()
        self.best()
        self.solve()
        self.check(k)
        self.deviate(k)
        self.multi(k)
        self.dims()
        self.versus()
        self.who()
        self.meaning()
        self.question()

    def card(self):
        c = chapter_card(3, r"Kyle: how an insider trades, and what it costs", r"How fast should someone who knows the "
                         r"value trade, and how far does the price move?", part=PART)
        with self.voiceover("Chapter three. Glosten and Milgrom fixed the trade size at one. In 1985 Albert Kyle let the "
                            "informed trader choose how much to trade, knowing that a bigger order moves the price "
                            "further. The answer gives the field its most used number: lambda, the price impact of "
                            "order flow."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"v", r"\sim", r"N(p_0, \sigma_v^2)", font_size=38, colors={r"v": VALUE_C}),
                cmath(r"x", r"=", r"X(v)\ \ \text{(the insider)},\qquad u \sim N(0, \sigma_u^2)\ \ \text{(noise)}",
                      font_size=30, colors={r"x": INF_C}),
                cmath(r"y", r"=", r"x + u,\qquad p = P(y)\ \ \text{(the market maker)}", font_size=34,
                      colors={r"y": FLOW_C})]
        whys = [why(r"one asset, worth $v$, which only the insider knows"),
                why(r"the insider submits a market order $x$; noise traders submit $u$, independent of everything"),
                why(r"the market maker sees only the total flow $y$, not who sent it, and sets a price at which it "
                    r"breaks even: $p = \mathbb E[v \mid y]$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> An asset worth v, normally distributed; only the insider knows v. "
            "<bookmark mark='b'/> The insider submits an order x; noise traders submit u, independent of everything. "
            "<bookmark mark='c'/> A competitive market maker sees only the total, y, and sets the price at which it "
            "breaks even: the expected value given the flow. The insider hides inside the noise."
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

    def guess(self):
        rows = [cmath(r"x", r"=", r"\beta\,(v - p_0)", font_size=38, colors={r"\beta": INF_C}),
                cmath(r"p", r"=", r"p_0 + \lambda\, y", font_size=38, colors={r"\lambda": FLOW_C}),
                cmath(r"\lambda", r"=", r"\frac{\operatorname{Cov}(v, y)}{\operatorname{Var}(y)} = \frac{\beta\sigma_v^2}"
                      r"{\beta^2\sigma_v^2 + \sigma_u^2}", font_size=34)]
        whys = [why(r"guess a linear strategy: trade in proportion to the mispricing"),
                why(r"and a linear pricing rule"),
                why(r"the market maker's break-even price is the regression of $v$ on $y$, given $\beta$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Guess that both sides are linear. <bookmark mark='a'/> The insider trades in proportion to the mispricing, "
            "with intensity beta. <bookmark mark='b'/> The market maker moves the price in proportion to the flow, with "
            "impact lambda. <bookmark mark='c'/> Given beta, the break-even lambda is a regression coefficient: the "
            "covariance of value with flow over the flow's variance."
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

    def best(self):
        rows = [cmath(r"\mathbb E[\pi \mid v]", r"=", r"\mathbb E[(v - p_0 - \lambda(x + u))\,x] = (v - p_0)x - \lambda x^2",
                      font_size=32, colors={r"\mathbb E[\pi \mid v]": INF_C}),
                cmath(r"x^*", r"=", r"\frac{v - p_0}{2\lambda}\ \Rightarrow\ \beta = \frac{1}{2\lambda}", font_size=36),
                cmath(r"\text{the insider}", r":", r"\text{trades half as hard as the mispricing invites}", font_size=30)]
        whys = [why(r"given $\lambda$, the insider's expected profit is a downward parabola in its order"),
                why(r"its peak: the insider's best response"),
                why(r"a bigger order would move the price against itself; the profit-maximising order leaves half the "
                    r"mispricing unexploited")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The insider's side. <bookmark mark='a'/> Given lambda, its expected profit is the mispricing times its "
            "order, minus lambda times the order squared: a downward parabola. <bookmark mark='b'/> Its peak is the "
            "mispricing over two lambda. <bookmark mark='c'/> The insider trades only half as hard as it could, because "
            "every unit moves the price against itself."
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

    def solve(self):
        st = VGroup(MathTex(r"\beta = \frac{\sigma_u}{\sigma_v},\qquad \lambda = \frac{\sigma_v}{2\sigma_u}", font_size=40),
                    MathTex(r"\mathbb E[\pi] = \frac{\sigma_u\sigma_v}{2},\qquad \operatorname{Var}(v \mid p) = "
                            r"\frac{\sigma_v^2}{2}", font_size=36),
                    wrapped_label(r"put the two best responses together: the insider scales its trading to the noise, so "
                                  r"its order is always as large as the camouflage allows; the impact rises with "
                                  r"what there is to know and falls with how much noise hides it", 9.6, 20)).arrange(
            DOWN, buff=0.35)
        card = theorem_card(r"Kyle's equilibrium (1985)", st, r"one auction", width=11.8, font_size=22)
        with self.voiceover(
            "Put the two together. <bookmark mark='a'/> Beta is sigma u over sigma v, and lambda is sigma v over two "
            "sigma u. The insider scales its order to the noise: it always trades exactly as much as the camouflage "
            "allows. The price impact rises with what there is to know, and falls with how much noise hides it. "
            "<bookmark mark='b'/> The insider expects half of sigma u sigma v, and the price reveals half of the "
            "value's variance."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def check(self, k):
        mc, one = k["mc"], k["one"]
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(label(r"$\sigma_v = \sigma_u = 1$", font_size=18, color=GREY_B), label(r"theorem", font_size=18,
                                                                                          color=GOOD),
                      label(r"200{,}000 draws", font_size=18, color=HURDLE))
        tab = VGroup(head,
                     VGroup(label(r"insider's profit", font_size=20, color=INF_C), MathTex(f"{one['profit']:.3f}", font_size=26),
                            MathTex(f"{mc['profit']:.3f}", font_size=26)),
                     VGroup(label(r"noise traders' loss", font_size=20, color=NOISE_C), MathTex(f"{one['profit']:.3f}",
                                                                                              font_size=26),
                            MathTex(f"{mc['noise_loss']:.3f}", font_size=26)),
                     VGroup(label(r"$\operatorname{Var}(v \mid p)$", font_size=20), MathTex(f"{one['post_var']:.3f}",
                                                                                         font_size=26),
                            MathTex(f"{mc['post_var']:.3f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.8 * j, 0])
        with self.voiceover(
            "Checked by simulation. <bookmark mark='a'/> The insider's profit, the noise traders' loss and the remaining "
            "uncertainty all match the theorem. And the first two are the same number: the market maker breaks even, "
            "so whatever the insider makes, the noise traders lose. That is who pays for an insider."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def deviate(self, k):
        dev = k["dev"]
        xs = [d["scale"] for d in dev]
        ys = [d["profit"] for d in dev]
        g = axes([0.4, 1.6], [0.3, 0.55], x_length=7.0, y_length=4.2, xlabel=r"the insider's order, as a multiple of $x^*$",
                 ylabel=r"expected profit", xticks=[0.5, 1.0, 1.5], yticks=[0.3, 0.4, 0.5], font_size=15)
        g.move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=INF_C) for a, b in zip(xs, ys)])
        xx = np.linspace(0.45, 1.55, 60)
        par = curve(ax, xx, 0.5 * (2 * xx - xx ** 2), GREY_B, stroke_width=2)
        with self.voiceover(
            "And the insider cannot do better. <bookmark mark='a'/> Against the same price impact, trading half as much "
            "or one and a half times as much both earn less, on the same parabola the theorem predicts. Equilibrium "
            "means neither side wants to change, and here neither does."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(par), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def multi(self, k):
        m = k["multi"]
        g = axes([0, 1], [0, 1], x_length=7.0, y_length=4.4, xlabel=r"time", ylabel=r"$\Sigma_t / \sigma_v^2$, what is "
                 r"still unknown", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        cols = {"1": GREY_B, "4": QC.SPOT, "16": QC.DELTA, "256": QC.GAIN}
        lines = VGroup()
        for n, col in cols.items():
            S = np.asarray(m[n]["Sigma"], float)
            t = np.linspace(0, 1, len(S))
            if n == "1":
                lines.add(curve(ax, [0, 1], [1, S[-1]], col, stroke_width=2.5))
            else:
                lines.add(curve(ax, t, S, col, stroke_width=2.5))
        lim = DashedLine(ax.c2p(0, 1), ax.c2p(1, 0), color=WHITE, stroke_width=1.5)
        leg = legend([(c, rf"$N = {n}$") for n, c in cols.items()] + [(WHITE, r"$1 - t$")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        l1, l256 = m["1"]["lambda0"], m["256"]["lambda0"]
        with self.voiceover(
            "Kyle also let the insider trade over many auctions. <bookmark mark='a'/> The recursion, computed: with one "
            "auction, half the uncertainty remains at the end. With four, sixteen, two hundred and fifty-six, the "
            "insider spreads its trading out, and the remaining uncertainty falls along a straight line, to zero at the "
            f"end. <bookmark mark='b'/> The price impact rises from {l1:.2f} with one auction to {l256:.2f} with two "
            "hundred and fifty-six: toward sigma v over sigma u. The research chapter proves the limit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(Create(lim))
        self.wait(0.4)
        self.clear_scene()

    def dims(self):
        cards = VGroup(
            desk_question(r"tightness", r"the cost of turning a position round quickly: the spread", width=12.4,
                          font_size=19),
            desk_question(r"depth", r"the order flow needed to move the price by one unit: $1/\lambda$, Kyle's own "
                          r"definition", width=12.4, font_size=19),
            desk_question(r"resiliency", r"how fast prices recover from an uninformative shock; in Kyle's dynamic model the "
                          r"noise part of a move never reverses, because the market maker cannot tell it from information",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Kyle's three dimensions of liquidity", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Kyle also named the three dimensions of liquidity that the rest of this act measures. "
            "<bookmark mark='a'/> Tightness: the cost of turning a position round, the spread. <bookmark mark='b'/> Depth: "
            "the flow needed to move the price one unit, one over lambda. <bookmark mark='c'/> And resiliency: how fast "
            "the price recovers from a shock that carried no information. Real markets have all three; the order book of "
            "Part thirty-six measures them separately."
        ) as vo:
            self.play(FadeIn(head))
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def versus(self):
        hx = [-3.6, 0.2, 3.8]
        head = VGroup(label(r"", font_size=17), label(r"Glosten--Milgrom", font_size=19, color=GREY_B),
                      label(r"Kyle", font_size=19, color=GREY_B))
        data = [(r"trade size", r"one unit", r"chosen by the insider"),
                (r"market maker sees", r"each trade's side", r"only the net flow"),
                (r"cost of liquidity", r"a bid-ask spread", r"price impact $\lambda$"),
                (r"informed traders", r"many, non-strategic", r"one, strategic"),
                (r"the price", r"a martingale, learning", r"a martingale, learning")]
        tab = VGroup(head)
        for a, b, c in data:
            tab.add(VGroup(label(a, font_size=18, color=HURDLE), label(b, font_size=18), label(c, font_size=18)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.3 - 0.75 * j, 0])
        with self.voiceover(
            "The two models side by side. <bookmark mark='a'/> Glosten and Milgrom fix the trade size and let the market "
            "maker see each trade's side; liquidity costs a spread; the informed are many and mechanical. Kyle lets one "
            "strategic insider choose its size, shows the market maker only the net flow, and prices liquidity by impact. "
            "In both, the price is a martingale that learns the value from the trades. The research chapter shows they "
            "meet in the limit."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[1:]], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def who(self):
        cards = VGroup(
            desk_question(r"not only corporate insiders", r"trading on material non-public information is illegal; Kyle's "
                          r"insider is anyone with better information, legally obtained: a better model, faster analysis, a "
                          r"better forecast", width=12.4, font_size=19),
            desk_question(r"Collin-Dufresne and Fos (2015)", r"activist investors who must later disclose their stakes traded "
                          r"most when noise trading was high and, as Kyle predicts, standard liquidity measures barely showed "
                          r"their presence", width=12.4, font_size=19),
            desk_question(r"the lesson for a measure", r"a strategic insider hides by design, so a quiet market is not "
                          r"evidence of no information", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Who are Kyle's insiders? <bookmark mark='a'/> Trading on material non-public information is illegal; Kyle's "
            "insider is anyone with better information, legally: a better model or a faster analysis. "
            "<bookmark mark='b'/> Pierre Collin-Dufresne and Vyacheslav Fos studied activist investors, who must later "
            "disclose their stakes, and found them trading most when noise was high, while standard liquidity measures "
            "barely registered them. <bookmark mark='c'/> A strategic insider hides by design, so a quiet market is not "
            "evidence that nobody knows anything."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def meaning(self):
        cards = VGroup(
            desk_question(r"lambda is measurable", r"regress price changes on signed order flow: the slope is Kyle's "
                          r"lambda, the market's price for a unit of flow (Chapter 5)", width=12.4, font_size=19),
            desk_question(r"depth is noise", r"a market is deep when there is much uninformed flow to hide in; "
                          r"$1/\lambda$ rises with $\sigma_u$", width=12.4, font_size=19),
            desk_question(r"informed trading is gradual", r"an insider who can trade over time does so slowly and "
                          r"steadily, so that its flow looks like noise: the shape of an optimal execution (Part 37)",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What Kyle gives a practitioner. <bookmark mark='a'/> Lambda is measurable: regress price changes on signed "
            "flow, as Chapter five does on Bitcoin. <bookmark mark='b'/> Depth is noise: a market is deep when there is "
            "much uninformed flow to hide in. <bookmark mark='c'/> And informed trading is gradual: an insider who can "
            "trade over time does so slowly and steadily, which is also the shape of the optimal execution of Part "
            "thirty-seven."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"noise trading doubles. What happens to $\lambda$, to the insider's order and to its expected "
                       r"profit?")
        with self.voiceover(
            "Pause and predict. Noise trading doubles. What happens to lambda, to the insider's order, and to its "
            "expected profit?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
