from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MKT, NET, PART, TREE, ask, fit_right, load


class DeepSDF(VoiceoverScene):
    def construct(self):
        s = load("sdf")
        self.card()
        self.moments()
        self.tangency()
        self.game()
        self.result(s)
        self.diagnosis(s)
        self.question()

    def card(self):
        c = chapter_card(8, r"Deep SDFs with adversarial moments", r"Can a network learn the discount factor that "
                         r"prices every coin?", part=PART)
        with self.voiceover("Chapter eight. Instead of forecasting returns, learn the one object that prices them all: "
                            "the stochastic discount factor of Part 4, with a network inside."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def moments(self):
        rows = [cmath(r"\mathbb E_t\big[M_{t+1} R^e_{i,t+1}\big]", r"=", r"0\quad \text{for every asset } i", font_size=32,
                      colors={r"\mathbb E_t\big[M_{t+1} R^e_{i,t+1}\big]": HURDLE}),
                cmath(r"M_{t+1}", r"=", r"1 - \textstyle\sum_i w(z_{i,t})\, R^e_{i,t+1}", font_size=32,
                      colors={r"M_{t+1}": NET}),
                cmath(r"\mathbb E\big[M_{t+1} R^e_{i,t+1}\, g(z_{i,t})\big]", r"=", r"0\quad \text{for every function } g",
                      font_size=32, colors={r"\mathbb E\big[M_{t+1} R^e_{i,t+1}\, g(z_{i,t})\big]": HURDLE})]
        whys = [why(r"no arbitrage (Part 4): a discount factor prices every excess return to zero, conditionally on "
                    r"what is known at $t$"),
                why(r"the SDF as a portfolio: its weights a network of each coin's characteristics (Chen, Pelger and Zhu "
                    r"2024)"),
                why(r"a conditional expectation is zero exactly when the unconditional one is zero against every function "
                    r"of the conditioning information: infinitely many moment conditions")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "Start from no arbitrage. <bookmark mark='a'/> A discount factor prices every excess return to zero, "
            "conditionally on what is known today. <bookmark mark='b'/> Write it as one minus a portfolio of the "
            "assets, with weights a network of each asset's characteristics. <bookmark mark='c'/> A conditional "
            "expectation is zero exactly when it is zero against every function of the conditioning information. So "
            "the condition is infinitely many moments, one for each function g. Luyang Chen, Markus Pelger and Jason "
            "Zhu turned that into a training rule in 2024."
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

    def tangency(self):
        rows = [cmath(r"\mathbb E[MR^e]", r"=", r"0\ \Rightarrow\ \mu = \mathbb E[R^e R^{e\top}]\,w", font_size=32,
                      colors={r"\mathbb E[MR^e]": HURDLE}),
                cmath(r"w", r"=", r"(\Sigma + \mu\mu^{\top})^{-1}\mu = \frac{\Sigma^{-1}\mu}{1 + \mu^{\top}\Sigma^{-1}\mu}",
                      font_size=32, colors={r"w": NET}),
                cmath(r"\frac{\sigma(M)}{\mathbb E[M]}", r"\ge", r"\max_p |SR_p| = \sqrt{\mu^{\top}\Sigma^{-1}\mu}",
                      font_size=32, colors={r"\frac{\sigma(M)}{\mathbb E[M]}": GOOD})]
        whys = [why(r"substitute $M = 1 - w^{\top}R^e$: the pricing conditions are linear in $w$"),
                why(r"Sherman--Morrison: the SDF's weights are proportional to $\Sigma^{-1}\mu$, the tangency portfolio "
                    r"of Part 23. Learning the SDF is learning the maximum-Sharpe portfolio"),
                why(r"Hansen and Jagannathan (1991): the SDF's volatility bounds every Sharpe ratio; so the SDF "
                    r"portfolio's Sharpe ratio is the natural yardstick of a learned SDF")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "For the researcher, one derivation shows what the SDF portfolio is. <bookmark mark='a'/> Substitute the "
            "portfolio form into the pricing condition: the condition is linear in the weights. <bookmark mark='b'/> "
            "Solve it, and by the Sherman-Morrison formula the weights are proportional to sigma inverse mu: the "
            "tangency portfolio of Part 23. Learning the discount factor and learning the maximum Sharpe ratio "
            "portfolio are the same problem. <bookmark mark='c'/> And by Hansen and Jagannathan, the discount factor's "
            "volatility bounds every Sharpe ratio, so the natural score of a learned SDF is the Sharpe ratio of its "
            "portfolio, out of sample."
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

    def game(self):
        eq = MathTex(r"\min_{w}\ \max_{g}\ \sum_{j}\Big(\tfrac1T\textstyle\sum_t \tfrac{1}{N_t}\sum_i M_{t+1}\, R^e_{i,t+1}\, "
                     r"g_j(z_{i,t})\Big)^2", font_size=34).to_edge(UP, buff=0.5)
        w_box = VGroup(RoundedRectangle(width=4.2, height=1.6, corner_radius=0.15, stroke_color=NET, fill_color=NET,
                                        fill_opacity=0.15),
                       Tex(r"SDF network $w(z)$\\prices the moments", font_size=24)).move_to(LEFT * 3.2 + DOWN * 0.3)
        w_box[1].move_to(w_box[0])
        g_box = VGroup(RoundedRectangle(width=4.2, height=1.6, corner_radius=0.15, stroke_color=BAD, fill_color=BAD,
                                        fill_opacity=0.15),
                       Tex(r"adversary $g(z)$\\finds the worst-priced\\test portfolios", font_size=24)).move_to(
            RIGHT * 3.2 + DOWN * 0.3)
        g_box[1].move_to(g_box[0])
        a1 = CurvedArrow(w_box.get_top() + RIGHT * 0.6, g_box.get_top() + LEFT * 0.6, angle=-TAU / 6, color=GREY_B)
        a2 = CurvedArrow(g_box.get_bottom() + LEFT * 0.6, w_box.get_bottom() + RIGHT * 0.6, angle=-TAU / 6, color=GREY_B)
        foot = wrapped_label(r"the House's version: $w$ a 32--16 network, $g$ four tanh outputs plus the constant (so the "
                             r"unconditional moments are always priced); alternating rounds of Adam, as in a GAN "
                             r"(AI, Built, Part 20); three seeds", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Infinitely many moments cannot all be checked, so Chen, Pelger and Zhu let a second network choose them. "
            "<bookmark mark='a'/> The SDF network tries to price the moments. <bookmark mark='b'/> An adversary, "
            "another network of the characteristics, searches for the test portfolios the SDF prices worst, and the "
            "two are trained against each other, as in a generative adversarial network. The House's adversary also "
            "always includes the constant, so the plain unconditional moments must be priced too."
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(w_box))
            vo.wait_until("b")
            self.play(FadeIn(g_box), Create(a1), Create(a2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def result(self, s):
        weeks = np.asarray(s["weeks"])
        n = len(weeks)
        ca, cl = np.asarray(s["cum_adv"]), np.asarray(s["cum_lin"])
        lo, hi = min(ca.min(), cl.min(), 0) - 0.1, max(ca.max(), cl.max(), 0.2) + 0.1
        g = axes([0, n - 1], [lo, hi], x_length=8.6, y_length=4.0, xlabel=r"week of 2020",
                 ylabel=r"cumulative return of the SDF portfolio (sum of weekly)", xticks=[], yticks=[], font_size=13).move_to(
            LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        la = curve(ax, np.arange(n), ca, NET, stroke_width=3)
        ll = curve(ax, np.arange(n), cl, LINEAR, stroke_width=3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(n - 1, 0), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{adversarial}}:\ SR = {s['sr_adv']:.2f}", font_size=24, color=NET),
            MathTex(rf"\text{{linear SDF}}:\ SR = {s['sr_lin']:.2f}", font_size=24, color=LINEAR),
            MathTex(rf"\text{{holding every coin}}:\ SR = {s['sr_ew']:.2f}", font_size=24, color=MKT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        fit_right(side)
        with self.voiceover(
            "Trained on 2018 and 2019 and run on 2020. <bookmark mark='a'/> The linear SDF, with weights linear in the "
            "characteristics, earns nothing: a Sharpe ratio of zero. <bookmark mark='b'/> The adversarial network "
            "loses steadily, a Sharpe ratio of minus one and a half, in a year when simply holding every coin earned "
            "plus one and a half."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(ll), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(la), FadeIn(side[0]), FadeIn(side[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def diagnosis(self, s):
        rows = VGroup(
            MathTex(rf"\text{{the coin market, 2018--19}}:\ {100 * s['train_mkt']:.0f}\%\ \text{{a year}}", font_size=30,
                    color=BAD),
            MathTex(rf"\text{{the coin market, 2020}}:\ +{100 * s['test_mkt']:.0f}\%\ \text{{a year}}", font_size=30,
                    color=GOOD),
            MathTex(rf"\operatorname{{corr}}(\text{{SDF portfolio}},\ \text{{market}})_{{2020}} = {s['corr_mkt_adv']:.3f}",
                    font_size=30, color=NET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.9)
        lesson = wrapped_label(r"the network did what it was asked: it priced the training years, in which the market's "
                               r"premium was negative, so the maximum-Sharpe portfolio was short the market. An SDF "
                               r"estimates premia, and premia are the least stable thing in finance; the cross-sectional "
                               r"structure the network found is buried under one wrong sign", 11.4, 19,
                               QC.HOUSE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Why? <bookmark mark='a'/> In the training years the average coin fell at about forty percent a year. In "
            "2020 it rose at about a hundred and twenty-five. <bookmark mark='b'/> And the adversarial SDF's portfolio "
            "has a correlation of minus point nine nine six with the market: it is, almost exactly, short crypto. "
            "<bookmark mark='c'/> The network did what it was asked. It priced the training years, in which the "
            "market's premium was negative, so the maximum Sharpe ratio portfolio was short the market. A discount "
            "factor is an estimate of premia, and premia are the least stable numbers in finance. Chen, Pelger and "
            "Zhu had fifty years of stocks, with a positive equity premium through most of them; on two years of "
            "coins, one sign decides everything."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"you must learn an SDF from two years in which the market fell. Propose a restriction on $w$ that "
                r"keeps the market's premium from deciding the answer, and say what it gives up.")
        with self.voiceover(
            "Pause and predict. You must learn a discount factor from two years in which the market fell. Propose a "
            "restriction on the weights that keeps the market's premium from deciding the answer, and say what it "
            "gives up."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
