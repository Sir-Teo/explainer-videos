from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


class Spirals(VoiceoverScene):
    def construct(self):
        s = load("spiral")
        self.card(s)
        self.model()
        self.two()
        self.paths(s)
        self.table(s)
        self.shocks(s)
        self.depth(s)
        self.evidence()
        self.policy()
        self.question()

    def card(self, s):
        r0 = [r for r in s["rows"] if r["kappa"] == 0.0][0]
        r2 = [r for r in s["rows"] if r["kappa"] == 2.0][0]
        c = chapter_card(2, r"Spirals", r"How do falling prices and rising margins feed each other?", part=PART)
        with self.voiceover(
            f"Chapter two, and the answer to the pause: in this model, about {100 * r2['fall']:.0f} percent, "
            f"{r2['amp']:.0f} times the shock. Forced sales alone take the price down {100 * r0['fall']:.0f} percent; "
            "margins that rise as the price falls take it further. Markus Brunnermeier and Lasse Pedersen called these the "
            "loss spiral and the margin spiral."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\text{holder}", r":", r"100 \text{ units, equity } 20,\ \text{margin } m_0 = 20\%", font_size=34,
                      colors={r"\text{holder}": LEV_C}),
                cmath(r"m", r"=", r"\min(0.9,\ m_0 + \kappa\,(1 - p))", font_size=40, colors={r"m": FUND_C}),
                cmath(r"q", r"\le", r"E / (m\,p)", font_size=42),
                cmath(r"\Delta p", r"=", r"-\,\text{dollars sold} / \text{depth}", font_size=40, colors={r"\Delta p": PRICE_C})]
        whys = [why(r"a leveraged holder at five times, at a price of 1"),
                why(r"its lender's margin rises with the fall in the price: $\kappa$ measures how nervous lenders get"),
                why(r"each round the holder cuts its position to what its equity can carry at today's margin"),
                why(r"and its sales move the price linearly against it, with a market depth of 400: the holder owns a "
                    r"large share of the market")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A minimal version, in the House's spiral function. <bookmark mark='a'/> A holder at five times. "
            "<bookmark mark='b'/> Its margin rises as the price falls, by an amount kappa that measures how nervous "
            "lenders become. <bookmark mark='c'/> Each round it cuts its position to what its equity can carry, "
            "<bookmark mark='d'/> and its sales push the price down, marking everything it still holds lower."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def two(self):
        rows = [cmath(r"\text{loss spiral}", r":", r"p\downarrow \Rightarrow E\downarrow \Rightarrow \text{sell} \Rightarrow p\downarrow",
                      font_size=36, colors={r"\text{loss spiral}": SPIRAL_C}),
                cmath(r"\text{margin spiral}", r":", r"p\downarrow \Rightarrow m\uparrow \Rightarrow \text{sell} \Rightarrow p\downarrow",
                      font_size=36, colors={r"\text{margin spiral}": FUND_C})]
        whys = [why(r"a loss shrinks equity, and at constant leverage the holder must sell in proportion; the sale lowers "
                    r"the price and makes the next loss"),
                why(r"Brunnermeier and Pedersen (2009): when lenders face more uncertainty they raise margins, so leverage "
                    r"itself must fall, and the sales are larger still")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Two spirals. <bookmark mark='a'/> The loss spiral: a price fall shrinks equity, the holder sells to keep its "
            "leverage, and the sale lowers the price again. <bookmark mark='b'/> The margin spiral: lenders facing more "
            "uncertainty raise margins, so leverage itself must fall, and the sales are larger still. Both run through "
            "the same market, at the same time."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def paths(self, s):
        p0 = np.asarray(s["path0"]["p"], float)
        p2 = np.asarray(s["path2"]["p"], float)
        top = max(len(p0), len(p2))
        fall0, fall2 = 100 * (1 - p0[-1]), 100 * (1 - p2[-1])
        g = axes([0, top], [0.75, 1.01], x_length=7.6, y_length=4.2, xlabel=r"round of forced selling",
                 ylabel=r"price", xticks=[0, 10, 20, 30, 40], yticks=[0.8, 0.9, 1.0], font_size=16).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        c0 = curve(ax, np.arange(len(p0)), p0, SPIRAL_C, stroke_width=3)
        c2 = curve(ax, np.arange(len(p2)), p2, FUND_C, stroke_width=3)
        leg = legend([(SPIRAL_C, r"loss spiral only ($\kappa = 0$)"), (FUND_C, r"with the margin spiral ($\kappa = 2$)")],
                     font_size=18).to_corner(UR, buff=0.5)
        with self.voiceover(
            "The price, round by round, after a three percent shock. <bookmark mark='a'/> With constant margins, each "
            f"round's sale is smaller than the last, and the price settles {fall0:.0f} percent down. "
            f"<bookmark mark='b'/> With margins that rise as it falls, the early rounds are larger, and it settles "
            f"{fall2:.0f} percent down, in fewer rounds."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(c0))
            vo.wait_until("a")
            self.play(Indicate(c0, color=HURDLE), run_time=2)
            vo.wait_until("b")
            self.play(Create(c2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def table(self, s):
        hx = [-3.6, -1.0, 1.6, 4.2]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"margin sensitivity $\kappa$", r"price fall",
                                                                         r"amplification", r"units sold")])
        tab = VGroup(head)
        for r in s["rows"]:
            tab.add(VGroup(MathTex(f"{r['kappa']:g}", font_size=28), MathTex(rf"{100 * r['fall']:.1f}\%", font_size=28, color=SPIRAL_C),
                           MathTex(rf"{r['amp']:.1f}\times", font_size=28, color=HURDLE), MathTex(f"{r['sold']:.0f}", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        r0, r3 = s["rows"][0], s["rows"][-1]
        with self.voiceover(
            "By how nervous the lenders are. <bookmark mark='a'/> With fixed margins, a three percent shock becomes "
            f"{100 * r0['fall']:.0f}, and the holder sells {r0['sold']:.0f} of its hundred units. <bookmark mark='b'/> As "
            f"margins become more sensitive, the fall reaches {100 * r3['fall']:.0f} percent, {r3['amp']:.1f} times the "
            f"news, and the holder sells {r3['sold']:.0f} units: nearly everything, into a market it is itself pushing down."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], color=HURDLE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def shocks(self, s):
        hx = [-3.0, 0.0, 3.0]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"initial shock", r"loss spiral only",
                                                                         r"with the margin spiral")])
        tab = VGroup(head)
        for r in s["shocks"]:
            tab.add(VGroup(MathTex(rf"{100 * r['shock']:.0f}\%", font_size=28),
                           MathTex(rf"{100 * r['loss_only']:.1f}\%", font_size=28, color=SPIRAL_C),
                           MathTex(rf"{100 * r['both']:.1f}\%", font_size=28, color=FUND_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.75 * j, 0])
        a, b = s["shocks"][0], s["shocks"][-1]
        with self.voiceover(
            "By the size of the news. <bookmark mark='a'/> A one percent shock: the loss spiral turns it into "
            f"{100 * a['loss_only']:.0f} percent, and with the margin spiral, {100 * a['both']:.0f}. <bookmark mark='b'/> "
            f"An eight percent shock ends at {100 * b['both']:.0f}. With nervous lenders, the outcome barely depends on "
            "the size of the news: once the spiral starts, it runs until the leverage is gone. That is a tipping point, "
            "not a proportional response."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], color=HURDLE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def depth(self, s):
        hx = [-2.4, 2.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"market depth", r"price fall, $\kappa = 2$")])
        tab = VGroup(head)
        for r in s["deep"]:
            tab.add(VGroup(MathTex(f"{r['depth']:,.0f}".replace(",", "{,}"), font_size=28),
                           MathTex(rf"{100 * r['fall']:.1f}\%", font_size=28, color=FUND_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.8 * j, 0])
        with self.voiceover(
            "And by the depth of the market. <bookmark mark='a'/> The deeper the market relative to the forced seller, the "
            f"smaller the spiral: from {100 * s['deep'][0]['fall']:.0f} percent when the holder is very large to "
            f"{100 * s['deep'][-1]['fall']:.0f} when the market is four times deeper. Crowded trades are dangerous because "
            "everyone in them is the large holder."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Indicate(tab[1], color=HURDLE), LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            desk_question(r"repo haircuts, 2007--08", r"Gorton and Metrick measured haircuts on bilateral repo against "
                          r"securitised bonds rising from near zero in early 2007 to around 45\% by late 2008: a run on "
                          r"repo, as a margin spiral", width=12.4, font_size=19),
            desk_question(r"exchange margins", r"futures exchanges raise margins after volatility jumps; in silver in "
                          r"2011 and across markets in March 2020 the increases came in the middle of the falls, as "
                          r"reported", width=12.4, font_size=19),
            desk_question(r"the illiquid asset suffers most", r"assets that are hard to sell and hard to finance fall "
                          r"together in a spiral: Brunnermeier and Pedersen's flight to quality", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The evidence. <bookmark mark='a'/> Gary Gorton and Andrew Metrick measured haircuts on repo against "
            "securitised bonds rising from near zero in early twenty oh seven to around forty-five percent by late twenty "
            "oh eight: a run on repo, as a margin spiral. <bookmark mark='b'/> Futures exchanges raise margins after "
            "volatility jumps, and in silver in twenty eleven and across markets in March twenty twenty the increases "
            "came during the falls, as reported. <bookmark mark='c'/> And the assets hardest to sell and to finance fall "
            "furthest: the flight to quality."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def policy(self):
        cards = VGroup(
            desk_question(r"the lender of last resort", r"Bagehot's rule: lend freely, against good collateral, at a "
                          r"penalty rate; a central bank that accepts the asset at a stable haircut breaks the margin "
                          r"spiral", width=12.4, font_size=19),
            desk_question(r"through-the-cycle margins", r"floors and buffers on haircuts, so they need not rise as much "
                          r"in the bust (Part 40's procyclicality)", width=12.4, font_size=19),
            desk_question(r"the buyer of last resort", r"in 2008 and 2020 central banks bought the assets themselves, "
                          r"replacing the market depth that forced sellers had exhausted", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What stops it. <bookmark mark='a'/> A lender of last resort, by Walter Bagehot's rule: lend freely, against "
            "good collateral, at a penalty rate. A central bank that accepts the asset at a stable haircut breaks the "
            "margin spiral. <bookmark mark='b'/> Margins set through the cycle, so they need not rise as much in the bust. "
            "<bookmark mark='c'/> And, in twenty oh eight and twenty twenty, central banks as buyers of last resort, "
            "replacing the depth that forced sellers had used up."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('five banks hold mortgage securities, loans and government bonds, at leverage from 15 to 30. Mortgage securities fall 5\\%. Use the unchanged leverage-times-loss approximation and chosen impact coefficients. How large are the second-round marks relative to the initial loss?')
        with self.voiceover(
            'Pause and predict. Five chosen banks hold mortgage securities, loans and government bonds at leverage fifteen to thirty. Mortgage values fall five percent. Use the unchanged high-leverage approximation, sales equal leverage times the first loss, and the chosen impact coefficients. How do the resulting second-round marks compare with the first losses? Distinguish this approximation from exact leverage restoration.'
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
