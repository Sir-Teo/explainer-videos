from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class Inelastic(VoiceoverScene):
    def construct(self):
        lim = load("limits")
        self.card()
        self.demand()
        self.logit()
        self.picture()
        self.gk(lim)
        self.consequences()

    def card(self):
        c = chapter_card(10, r"Demand systems and inelastic markets", r"How much does a dollar of buying move a price?",
                         lit=(2019, 2021), part=PART)
        with self.voiceover("Chapter ten. Prices are set where demand meets supply; how steep is the demand curve for "
                            "stocks?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def demand(self):
        rows = [cmath(r"w_{ij}", r"=", r"\frac{\delta_{ij}}{1 + \sum_k \delta_{ik}},\quad \ln\delta_{ij} = \beta_{0i}\,"
                      r"\text{me}_j + \beta_i^\top x_j + \varepsilon_{ij}", font_size=32, colors={r"w_{ij}": MKT}),
                cmath(r"\zeta", r"=", r"-\frac{\partial \ln Q}{\partial \ln P}", font_size=42, colors={r"\zeta": BAD})]
        whys = [why(r"Koijen and Yogo (2019): estimate each institution's demand for every stock from its holdings (the "
                    r"SEC's 13F filings): portfolio weights as a logit in the stock's price and characteristics. Prices "
                    r"are whatever clears the market"),
                why(r"the elasticity of demand: by how much the quantity investors want falls when the price rises 1\%. "
                    r"In the textbook it is huge, because any mispricing is arbitraged; in the holdings data it is small")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The models so far say what investors should demand; Ralph Koijen and Motohiro Yogo asked what they do "
            "demand. They estimated every institution's demand for every stock from its quarterly holdings, filed with "
            "the SEC: portfolio weights as a function of the stock's price and characteristics, and prices as whatever "
            "makes all the demands add up to the shares outstanding. <bookmark mark='a'/> The key number is the "
            "elasticity of demand: how much less of a stock investors want when its price rises one percent. In "
            "textbook models it is enormous, because a mispriced stock is arbitraged away. In the holdings data it is "
            "small."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def logit(self):
        rows = [cmath(r"\ln q_{ij}", r"=", r"\ln w_{ij} + \ln A_i - \ln P_j", font_size=38, colors={r"\ln q_{ij}": MKT}),
                cmath(r"\frac{\partial \ln w_{ij}}{\partial \ln P_j}", r"=", r"\beta_{0i}\,(1 - w_{ij})", font_size=38),
                cmath(r"\zeta_{ij}", r"=", r"1 - \beta_{0i}\,(1 - w_{ij})", font_size=42, colors={r"\zeta_{ij}": BAD})]
        whys = [why(r"shares held: the investor's assets $A_i$ times the weight, divided by the price"),
                why(r"in the logit, the weight responds to the stock's own market value with slope $\beta_0$, damped by "
                    r"$1 - w$ because the other weights must make room"),
                why('partial derivative holding wealth $A_i$, shares outstanding, characteristics and other prices fixed; not aggregate equilibrium elasticity')]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        hx = [-3.6, 0.0, 3.4]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, -1.45, 0]) for h_, x in
                              zip((r"investor", r"$\beta_0$", r"elasticity, $w$ = 1\%"), hx)]))
        for k, (nm, b0) in enumerate((('fixed-$A$ logit, $\\beta_0=1$', 1.0), (r"fixed dollars", 0.0), (r"a value investor", -4.0))):
            y = -1.95 - 0.45 * k
            tab.add(VGroup(label(nm, font_size=18).move_to([hx[0], y, 0]), MathTex(f"{b0:+.0f}", font_size=24).move_to(
                [hx[1], y, 0]), MathTex(f"{1 - b0 * 0.99:.2f}", font_size=24, color=BAD).move_to([hx[2], y, 0])))
        with self.voiceover(
            "Shares held equal wealth times the portfolio weight divided by price. <bookmark mark='a'/> In this logit, the own-price derivative holds wealth, shares outstanding, characteristics and other prices fixed. <bookmark mark='b'/> Under those assumptions, elasticity is one minus beta-nought times one minus the weight. <bookmark mark='c'/> At a one-percent weight, beta-nought one gives point zero one; beta-nought zero gives one; beta-nought minus four gives four point nine six. These are fixed-wealth logit examples. The first is not a literal self-financing capitalisation-weighted index fund: its wealth and normalisation also change when prices change. Aggregating demand requires wealth, supply and cross-price feedback, so a weighted partial derivative is not by itself an aggregate equilibrium elasticity. Holdings estimates require an identification strategy, not simply reading a causal slope off a portfolio snapshot."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeOut(VGroup(*rows[:2], *whys[:2])),
                      rows[2].animate.set_y(2.5), whys[2].animate.set_y(1.55))
            tab.shift(UP * 0.9)
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def picture(self):
        g = axes([0, 2], [0, 2], x_length=6.4, y_length=4.4, xlabel=r"shares demanded", ylabel=r"price", xticks=[],
                 yticks=[], font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        supply = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 2), color=GREY_B, stroke_width=2)
        sl = label(r"fixed supply of shares", font_size=15, color=GREY_A).next_to(ax.c2p(1.0, 2), UP, buff=0.05)
        elastic = Line(ax.c2p(0.2, 1.08), ax.c2p(1.8, 0.92), color=GOOD, stroke_width=3)
        inel = Line(ax.c2p(0.7, 1.6), ax.c2p(1.3, 0.4), color=BAD, stroke_width=3)
        inel2 = Line(ax.c2p(0.9, 1.6), ax.c2p(1.5, 0.4), color=BAD, stroke_width=3, stroke_opacity=0.6)
        el2 = Line(ax.c2p(0.4, 1.08), ax.c2p(2.0, 0.92), color=GOOD, stroke_width=3, stroke_opacity=0.6)
        side = VGroup(
            legend([(GOOD, r"elastic demand: arbitrageurs everywhere"), (BAD, r"inelastic demand: mandates, indices")],
                   font_size=16),
            wrapped_label(r"the same new buyer shifts either demand curve right by the same number of shares; with "
                          r"elastic demand the price barely moves, with inelastic demand it moves a lot", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Why it matters, in a picture. The supply of shares is fixed. <bookmark mark='a'/> If demand is elastic, flat, a new buyer who shifts it to the right barely moves the price: someone else sells the moment the price drifts above value. <bookmark mark='b'/> If demand is steep, inelastic, the same buyer moves the price a long way, because the other holders are pension funds with fixed allocations and index mandates with limited active substitution. This is a fixed-supply partial-equilibrium sketch, not a literal claim that an index fund owns every share or buys without a budget."
        ) as vo:
            self.play(FadeIn(g), Create(supply), FadeIn(sl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(elastic))
            self.play(TransformFromCopy(elastic, el2))
            vo.wait_until("b")
            self.play(Create(inel))
            self.play(TransformFromCopy(inel, inel2), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def gk(self, lim):
        rows = [cmath(r"\Delta\ln P", r"\approx", r"\frac{1}{\zeta}\,\frac{\Delta F}{W},\quad \zeta \approx 0.2\ \Rightarrow\ "
                      rf"\frac{{1}}{{\zeta}} \approx {lim['gk']:.0f}", font_size=36, colors={r"\Delta\ln P": BAD})]
        whys = [why("Gabaix and Koijen (2021): estimated from flows into and out of the US stock market as a whole, the aggregate elasticity is about 0.2, so a flow of 1\\% of the market's value into equities raises prices by about 5\\%: local allocation-shock hypothesis, not every trade: all purchases have sellers; wealth/supply feedback and causal identification matter")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        ex = VGroup(
            label(r"an illustration", font_size=22, color=GREY_A),
            MathTex(f"\\$100\\ \\text{{billion allocation shock, on a \\$50 trillion market}}:\\ 0.2\\%\\ \\text{{of value}}\\ \\Rightarrow\\ \\approx {0.2 * lim['gk']:.0f}\\%\\ \\text{{on prices}}", font_size=26),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Xavier Gabaix and Ralph Koijen estimated the elasticity for the market as a whole, from flows between stocks and bonds. They found it is about one fifth. <bookmark mark='a'/> So the multiplier is about five: in their estimated local allocation-shock framework, a dollar shift toward equities corresponds to about five dollars of valuation change. Every stock purchase has a seller; this is not net buying of shares by all holders combined. A hypothetical hundred-billion allocation-demand shock, a fifth of a percent of the market, lifts prices about one percent. They call it the inelastic markets hypothesis, and if it is right, flows, not just news, move prices, and a great deal of the volatility Shiller found is the market absorbing them."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    def consequences(self):
        cards = VGroup(
            desk_question(r"passive investing", 'index mandates may reduce active substitution; aggregate elasticity also depends on wealth, other investors, financing and supply', width=12.0, font_size=21),
            desk_question(r"buybacks and issuance", 'buybacks change both share supply and corporate cash/financing; price effects cannot be inferred from gross purchases alone', width=12.0, font_size=21),
            desk_question(r"the debate", r"critics argue the estimates confound flows with news; the elasticity of a "
                          r"single stock, where arbitrage is easier, is larger than the market's. Settling it is ongoing "
                          r"work", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The consequences are large if it is right. <bookmark mark='a'/> Index mandates may reduce active substitution, but aggregate elasticity also depends on wealth, financing, supply and other investors. <bookmark mark='b'/> Buybacks change both share supply and corporate cash or financing, so gross purchases alone do not determine their price effect. <bookmark mark='c'/> It is also contested: separating flows from the news that causes them is hard, and a single stock, where arbitrage between close substitutes is easier, is more elastic than the market as a whole."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"if the market's demand elasticity is 0.2, what does a pension fund's shift of 1\% of the market from bonds "
                r"to stocks do to prices, and who sells to it?")
        with self.voiceover("If the market's elasticity is a fifth, what does a shift of one percent of the market from "
                            "bonds to stocks do to prices, and who sells?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
