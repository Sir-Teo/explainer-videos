from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class Intermediary(VoiceoverScene):
    def construct(self):
        im = load("intermediary")
        self.card()
        self.idea()
        self.spiral()
        self.ratio(im)
        self.tests(im)
        self.aem()

    def card(self):
        c = chapter_card(9, r"Intermediaries price assets", r"Whose marginal value of a dollar matters?", lit=(2008,),
                         part=PART)
        with self.voiceover("Chapter nine. Perhaps the investor whose discount factor matters is not a household at all, "
                            "but a dealer."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        rows = [cmath(r"m_{t+1}", r"\propto", r"\Big(\frac{\eta_{t+1}}{\eta_t}\Big)^{-\gamma},\quad \eta = \frac{\text{equity}}"
                      r"{\text{assets}}\ \text{of the primary dealers}", font_size=34, colors={r"m_{t+1}": SDF})]
        whys = [why("He and Krishnamurthy (2013): most trading in complex assets is done by intermediaries, so their marginal value of wealth prices those assets. When dealers' capital is low, a dollar to them is worth a lot, and the assets they must hold pay a premium. He, Kelly and Manela (2017) proxy $\\eta$ using the market equity of the New York Fed's primary dealers' parent companies")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Households own most stocks in the end, but they rarely trade bonds, options, swaps or currencies directly. Dealers do. Zhiguo He and Arvind Krishnamurthy argued that the marginal investor in those markets is the intermediary, so its value of a dollar is the discount factor. When dealers' capital is scarce, a dollar to them is worth a great deal, and the assets they must hold pay a premium for loading on that scarcity. Zhiguo He, Bryan Kelly and Asaf Manela constructed a proxy for that scarcity: the equity capital ratio of the New York Fed's primary dealers' parent companies. The link to marginal utility is a model, not a measurement identity or causal proof."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def spiral(self):
        hx = [-4.2, -1.3, 1.3, 4.2]
        heads = [r"", r"assets", r"equity", r"capital ratio"]
        data = [(r"before", 100, 10, BAD), (r"assets fall 5\%", 95, 5, BAD), (r"sell to restore 10\%", 50, 5, BAD)]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.2, 0]) for h_, x in zip(heads, hx)]))
        for k, (nm, a, e, col) in enumerate(data):
            y = 1.55 - 0.6 * k
            tab.add(VGroup(label(nm, font_size=19).move_to([hx[0], y, 0]),
                           MathTex(rf"\${a}", font_size=28).move_to([hx[1], y, 0]),
                           MathTex(rf"\${e}", font_size=28).move_to([hx[2], y, 0]),
                           MathTex(rf"{100 * e / a:.1f}\%", font_size=28, color=GOOD if k != 1 else col).move_to(
                               [hx[3], y, 0])))
        foot = VGroup(
            MathTex(r"\text{a 5\% fall halves equity; restoring the ratio means selling } \$45 \text{ of } \$95", font_size=28,
                    color=BAD),
            wrapped_label("selling repays debt: $90\\to45$, assets $95\\to50$, equity $5$ unchanged, assuming no extra price impact/costs. Raising equity is another option. If many dealers sell together, so prices fall further and the next round of losses begins: Brunnermeier and Pedersen's (2009) loss and margin spirals. That is why a dollar to a dealer with little capital is worth so much, and why the assets it must sell pay a premium for the risk", 12.0, 17, GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why should a dealer's capital matter so much? A worked balance sheet. A dealer holds a hundred dollars of assets with ten of equity: a capital ratio of ten percent. <bookmark mark='a'/> The assets fall five percent. Debt does not fall, so the whole loss comes out of equity, which halves to five, and the ratio drops to about five percent. <bookmark mark='b'/> To get back to ten percent with five dollars of equity the dealer can hold only fifty dollars of assets: with no new equity, it sells forty-five of its ninety-five and repays forty-five of debt, leaving assets fifty, debt forty-five and equity five. This arithmetic assumes no additional price impact or financing costs; raising equity is another option. <bookmark mark='c'/> If other constrained dealers do the same thing with the same assets, prices fall again, and the next round of losses begins. Markus Brunnermeier and Lasse Pedersen called these loss and margin spirals. So a dollar is worth most to a dealer exactly when capital is scarce, and assets that fall in those moments must pay a premium."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(FadeIn(tab[2], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(tab[3], shift=RIGHT * 0.2), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()

    def ratio(self, im):
        t, r = np.asarray(im["t"]), np.asarray(im["ratio"])
        g = axes([1970, 2019], [0, 0.16], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"capital ratio",
                 xticks=[1970, 1980, 1990, 2000, 2010], yticks=[0, 0.04, 0.08, 0.12, 0.16], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, r, SDF, stroke_width=2.6)
        k = int(np.argmin(np.where(t > 2007, r, 9)))
        side = VGroup(
            MathTex(rf"\text{{low}}:\ {r[k]:.3f}\ \ ({int(t[k])})", font_size=26, color=BAD),
            wrapped_label(r"the primary dealers' parents: market equity over market equity plus book debt, monthly "
                          r"1970--2018, as He, Kelly and Manela publish it. It falls in the crises: 1974, 1987, "
                          r"2001--03, and most of all in 2008--09", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is their measure: the dealers' parent companies' market equity as a share of their equity plus debt. "
            "<bookmark mark='a'/> It falls in the crises: 1974, 1987, the early 2000s, and above all in the "
            f"winter of 2008 and 2009, when it reached about {100 * r[k]:.0f} percent. An asset that does badly when "
            "this ratio falls is an asset that loses money exactly when the people who must hold it can least afford "
            "to."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2.5)
        self.add(illustration(r"He, Kelly and Manela (2017), factors as published by the authors"))
        self.wait(0.4)
        self.clear_scene()

    def tests(self, im):
        cl = im["classes"]
        hx = [-4.6, -1.9, 0.6, 3.0, 5.2]
        heads = [r"asset class", r"portfolios", r"price of capital risk", r"$R^2$, with it", r"$R^2$, CAPM"]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.55, 0]) for h_, x in zip(heads, hx)]))
        for i, (k, v) in enumerate(cl.items()):
            y = 1.95 - 0.5 * i
            lam, t = v["lam"][2], v["t"][2]
            tab.add(VGroup(label(k, font_size=18).move_to([hx[0], y, 0]),
                           MathTex(str(v["N"]), font_size=24).move_to([hx[1], y, 0]),
                           MathTex(rf"{100 * lam:.1f}\%\ \ ({t:.1f})", font_size=24,
                                   color=GOOD if t > 1.96 else (TAN if lam > 0 else BAD)).move_to([hx[2], y, 0]),
                           MathTex(f"{v['r2']:.2f}", font_size=24).move_to([hx[3], y, 0]),
                           MathTex(f"{v['r2_capm']:.2f}", font_size=24, color=GREY_B).move_to([hx[4], y, 0])))
        foot = wrapped_label("quarterly, 1970--2012 where each class's data exist; two-pass regressions on the market and the capital-risk factor, Shanken $t$ in brackets; prices of risk per quarter. The price is positive in all seven saved point estimates; four approximate Shanken $t$ values exceed 1.96. Different class windows, full-sample betas, no HAC/joint/causal certificate or exact paper replication", 12.4, 16, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Their test is ambitious: one factor, the shocks to that capital ratio, should price assets in every market dealers make. <bookmark mark='a'/> Take their portfolios of stocks, Treasuries, sovereign bonds, options, credit default swaps, commodities and currencies, and run the two-pass regressions of Part six on the market and the capital factor. <bookmark mark='b'/> All seven saved capital-risk point estimates are positive. Four approximate Shanken t-statistics exceed one point nine six; positivity is not the same as significance. In stocks it raises the explained share of average returns from {cl['stocks']['r2_capm']:.2f} with the CAPM to {cl['stocks']['r2']:.2f}. The commodity point estimate is also positive, with an approximate t-statistic of one point six. The classes use different available quarterly windows and full-sample first-stage betas. These approximate iid Shanken statistics are not HAC-robust, a joint seven-class test, causal evidence or an exact replication of the paper."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def aem(self):
        cards = VGroup(
            desk_question(r"Adrian, Etula and Muir (2014)", r"broker-dealers' leverage, from the Fed's flow of funds: when "
                          r"it rises, dealers are flush, and the assets that pay off then are worth less. A single "
                          r"leverage factor prices size, value and momentum portfolios", width=12.0, font_size=20),
            desk_question(r"the tension", 'leverage measured at book value rises in booms (Adrian et al.); capital at market value falls in busts (He et al.): different balance sheets and book/market measures: opposite signs cannot be read as contradictory estimates of the same variable', width=12.0, font_size=20),
            desk_question(r"why it matters", "Part 22's basis trades and Part 21's capital rules again: when intermediaries are constrained, required returns and intermediation costs can change; scarcity alone does not establish fundamental mispricing", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "There is a rival measure. <bookmark mark='a'/> Tobias Adrian, Erkko Etula and Tyler Muir used broker-dealer leverage from the Fed's flow of funds: when leverage rises, dealers are flush, and a dollar to them is worth less. <bookmark mark='b'/> These papers measure different objects: book leverage of broker-dealers and market equity capital of their parents. Opposite signs cannot be interpreted as contradictory estimates of the same variable. <bookmark mark='c'/> But both point to the same idea, the one behind the bases of Part twenty-two: when the people who make markets are constrained, required returns and intermediation costs can change. Capital scarcity alone does not prove fundamental mispricing."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"if dealers' capital prices assets, what should happen to the CIP basis of Part 22 when bank equity "
                r"falls, and why?")
        with self.voiceover("If dealers' capital prices assets, what should happen to the covered interest parity basis "
                            "of Part twenty-two when bank equity falls, and why?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
