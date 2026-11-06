from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, COST_C, GOOD, HURDLE, NET_C, PART, RES_C, comma, fit_right, load


class Deep(VoiceoverScene):
    def construct(self):
        d = load("deep")
        self.card()
        self.claim()
        self.literature()
        self.setup_(d)
        self.network()
        self.ic(d)
        self.bars(d)
        self.why_fail(d)
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(8, r"Learning the residual", r"Can a network read a residual's path better than an s-score?",
                         part=PART)
        with self.voiceover("Chapter eight. The s-score reads one number from a residual's path: how far it is from its "
                            "mean. A network could read the whole shape. Does it find more?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def claim(self):
        rows = [cmath(r"\text{residuals}", r"\to", r"\text{signal extractor}\to\text{allocation}", font_size=34,
                      colors={r"\text{residuals}": RES_C}),
                cmath(r"\text{signal}", r":", r"\text{a convolutional transformer on the last 30 days}", font_size=32,
                      colors={r"\text{signal}": NET_C}),
                cmath(r"\text{objective}", r":", r"\text{the portfolio's Sharpe ratio, trained end to end}", font_size=32)]
        whys = [why(r"Guijarro-Ordonez, Pelger and Zanotti, `Deep Learning Statistical Arbitrage' (2021): the Avellaneda--"
                    r"Lee pipeline, with every hand-made step learned"),
                why(r"the network sees the cumulative residual's whole recent path, not just its distance from the mean"),
                why(r"they report a high out-of-sample Sharpe ratio on large US stocks, still profitable after costs, from "
                    r"asymmetric trend and reversion patterns that an OU model cannot express")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The claim. <bookmark mark='a'/> In 2021 Jorge Guijarro-Ordonez, Markus Pelger and Greg Zanotti took the "
            "Avellaneda-Lee pipeline and learned every step. <bookmark mark='b'/> A convolutional transformer reads each "
            "residual's last thirty days. <bookmark mark='c'/> And the allocation is trained to maximise the portfolio's "
            "Sharpe ratio directly. They report a high out-of-sample Sharpe ratio on large American stocks, still "
            "profitable after trading costs, from patterns of trend and reversion that an Ornstein-Uhlenbeck model "
            "cannot express."
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

    def literature(self):
        cards = VGroup(
            desk_question(r"Krauss, Do and Huck (2017)", r"deep nets, boosted trees and random forests on the lagged "
                          r"returns of S\&P 500 stocks, 1992--2015: an ensemble earning over 0.45\% a day before costs, as "
                          r"reported, much less after them, and declining in the later years", width=12.4, font_size=19),
            desk_question(r"Guijarro-Ordonez, Pelger and Zanotti (2021)", r"residuals of conditional factors, a "
                          r"convolutional transformer, and an allocation trained on the Sharpe ratio; reported robust to "
                          r"costs", width=12.4, font_size=19),
            desk_question(r"the common thread", r"thousands of single stocks, signals from many days at once, and the "
                          r"decay over time that every reversal strategy shows", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The machine-learning literature on stat arb, briefly. <bookmark mark='a'/> Christopher Krauss, Xuan Anh Do "
            "and Nicolas Huck trained deep networks, boosted trees and random forests on the lagged returns of S and P "
            "five hundred stocks; their ensemble earned, as reported, over forty-five basis points a day before costs, "
            "much less after them, and less in the later years. <bookmark mark='b'/> The deep stat-arb paper learned the "
            "whole pipeline and reported robustness to costs. <bookmark mark='c'/> The common thread: thousands of single "
            "stocks, signals read from many days at once, and decay over time."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def setup_(self, d):
        ntr = comma(d["n_train"])
        rows = [cmath(r"x_{i,t}", r"=", r"\Big(\tfrac{X_{i,t-29}-X_{i,t}}{\hat\sigma_i}, \dots, \tfrac{X_{i,t-1}-X_{i,t}}"
                      r"{\hat\sigma_i}, 0\Big)", font_size=32, colors={r"x_{i,t}": RES_C}),
                cmath(r"y_{i,t}", r"=", r"u_{i,t+1}/\hat\sigma_i", font_size=36),
                cmath(r"\text{train}", r"\le", r"2012\ \ <\ \ \text{validate}\ \le 2016\ \ <\ \ \text{test}", font_size=32,
                      colors={r"\text{train}": NET_C})]
        whys = [why(r"each industry's cumulative residual over the last 30 days, relative to today, in units of its "
                    r"own volatility: a path, not a number"),
                why(r"the target: tomorrow's residual return, in the same units"),
                why(rf"${ntr}$ training examples from 1991 to 2012; early stopping on 2013--16; tested on 2017--20, "
                    r"which no choice has seen")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The House's version, smaller and honest. <bookmark mark='a'/> The input is each industry's cumulative "
            "residual over the last thirty days, measured from today, in units of its own volatility. "
            "<bookmark mark='b'/> The target is tomorrow's residual return. <bookmark mark='c'/> Train up to 2012, stop "
            "early on 2013 to 2016, and test on 2017 to 2020, which no choice has touched."
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

    def network(self):
        sizes = [30, 32, 16, 1]
        cols = [RES_C, NET_C, NET_C, HURDLE]
        layers = VGroup()
        for k, (n, c) in enumerate(zip(sizes, cols)):
            m = min(n, 10)
            lay = VGroup(*[Circle(radius=0.11, color=c, fill_opacity=0.5, stroke_width=1.5) for _ in range(m)])
            lay.arrange(DOWN, buff=0.14).move_to([-4.2 + 2.8 * k, 0, 0])
            layers.add(lay)
        edges = VGroup()
        for a, b in zip(layers[:-1], layers[1:]):
            for u in a:
                for v in b:
                    edges.add(Line(u.get_right(), v.get_left(), stroke_width=0.4, color=GREY_D, stroke_opacity=0.5))
        names = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(layers[k], DOWN, buff=0.3)
                         for k, t in enumerate([r"30-day path", r"32 units", r"16 units", r"tomorrow"])])
        foot = wrapped_label(r"three seeds averaged, an L1 penalty, early stopping: the ensemble of Part 27, "
                             r"\texttt{ml.MLPEnsemble}", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The network is Part twenty-seven's small ensemble: thirty inputs, two hidden layers of thirty-two and "
            "sixteen units, three random seeds averaged, a light penalty, and early stopping. "
            "<bookmark mark='a'/> It is much smaller than a transformer, but it can learn any shape of path the s-score "
            "ignores: a residual that has just turned, one that is still falling, one that overshot."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(l_) for l_ in layers], lag_ratio=0.2), FadeIn(names))
            self.play(Create(edges), FadeIn(foot), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(layers[0], color=RES_C))
        self.wait(0.4)
        self.clear_scene()

    def ic(self, d):
        rows = [cmath(r"\text{IC}", r"=", rf"\operatorname{{corr}}(\hat y, y) = {d['ic']:.4f}", font_size=36,
                      colors={r"\text{IC}": NET_C}),
                cmath(r"\operatorname{corr}(\hat y, -x_{\text{oldest}})", r"=", rf"{d['corr_with_reversal']:.2f}",
                      font_size=34),
                cmath(r"\operatorname{corr}(x_{t-1}, y)", r"=", rf"{d['lag1_corr']:.4f}", font_size=34)]
        whys = [why(r"the network's forecasts against tomorrow's residuals, 2017--20: almost no information"),
                why(r"its forecast is barely related to how far the residual has moved over the month, the s-score's raw material"),
                why(r"and yesterday's residual move alone says nothing about tomorrow's: the residuals of a five-factor "
                    r"model on industries are close to unpredictable from one day to the next")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        ic, cr = d["ic"], d["corr_with_reversal"]
        with self.voiceover(
            "On the test years. <bookmark mark='a'/> The correlation between the network's forecast and tomorrow's "
            f"residual is {ic:.4f}: almost nothing. <bookmark mark='b'/> Its forecast is nearly unrelated to the "
            f"s-score's raw material, how far the residual has moved over the month: a correlation of {cr:.2f}. <bookmark mark='c'/> And yesterday's residual move "
            "alone predicts nothing. With so little to learn from day to day, a flexible model mostly learns noise."
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

    def bars(self, d):
        items = [(r"the s-score rule, gross", d["sscore"]["sharpe"], RES_C),
                 (r"the network, gross", d["net"]["sharpe"], NET_C),
                 (r"the network, after costs", d["net_after_costs"]["sharpe"], COST_C)]
        lo = float(np.floor(min(v for _, v, _ in items)))
        hi = float(np.ceil(max(v for _, v, _ in items)))
        g = axes([0, 3.6], [lo, hi], x_length=7.6, y_length=4.6, xlabel=r"2017--2020, the test years",
                 ylabel=r"Sharpe ratio", xticks=[], yticks=[lo, 0, hi], yfmt=lambda v: f"{v:.0f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for k, (t, v, c) in enumerate(items):
            x0 = 0.4 + 1.1 * k
            r = Polygon(ax.c2p(x0, 0), ax.c2p(x0 + 0.8, 0), ax.c2p(x0 + 0.8, v), ax.c2p(x0, v), color=c, fill_opacity=0.7,
                        stroke_width=1)
            bars.add(r)
            lab = MathTex(f"{v:.2f}", font_size=24, color=c)
            lab.next_to(r, UP if v >= 0 else DOWN, buff=0.1)
            labs.add(lab)
        leg = legend([(c, t) for t, _, c in items], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        tv = 100 * d["turnover"]
        st = wrapped_label(rf"the network trades {tv:.0f}\% of its book a day", 4.0, 16, GREY_A)
        st.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        fit_right(st)
        s0, s1, s2 = (v for _, v, _ in items)
        with self.voiceover(
            "The test. <bookmark mark='a'/> On the same days, the plain s-score rule earns a gross Sharpe ratio of "
            f"{s0:.2f}. <bookmark mark='b'/> The network earns {s1:.2f} before costs. <bookmark mark='c'/> And after "
            f"costs, {s2:.1f}: because it rebalances to its forecast every day, it trades {tv:.0f} percent of its book "
            "daily, and pays for it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[k], DOWN if items[k][1] >= 0 else UP), FadeIn(labs[k]))
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def why_fail(self, d):
        cards = VGroup(
            desk_question(r"the wrong universe", r"49 industry portfolios have little residual predictability to learn; "
                          r"the paper used hundreds of single stocks, where the patterns live", width=12.4, font_size=19),
            desk_question(r"the wrong objective", r"a forecast of tomorrow's return, rebalanced daily, ignores costs; the "
                          r"paper trains the allocation on the net Sharpe ratio, so the network learns to trade less",
                          width=12.4, font_size=19),
            desk_question(r"too few examples, too much noise", r"a daily IC near zero needs years of data to separate from "
                          r"noise, and every architecture and seed tried is another trial", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Why it fails here, and why that is no verdict on the paper", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Why it fails here, and why that is not a verdict on the paper. <bookmark mark='a'/> The universe is wrong: "
            "forty-nine industries have little residual predictability; the paper used hundreds of single stocks. "
            "<bookmark mark='b'/> The objective is wrong: a forecast rebalanced daily ignores costs, while the paper "
            "trains the allocation on the Sharpe ratio after costs, so its network learns to trade less. "
            "<bookmark mark='c'/> And a near-zero daily signal needs years of data to tell from noise, and every "
            "architecture tried is another trial."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        rows = [cmath(r"\text{flexibility}", r"\Rightarrow", r"\text{needs signal, data and a cost-aware loss}",
                      font_size=32, colors={r"\text{flexibility}": NET_C}),
                cmath(r"\text{the s-score}", r"=", r"\text{a strong prior: revert to the mean}", font_size=32,
                      colors={r"\text{the s-score}": RES_C}),
                cmath(r"\text{a fair contest}", r":", r"\text{same residuals, same days, same costs}", font_size=32)]
        whys = [why(r"a network can only beat a simple rule when there is structure to find and enough data to find it"),
                why(r"on a weak signal, a model with a strong prior wastes less of the data"),
                why(r"the network is one more trial, and it lost: it is not registered")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The lessons. <bookmark mark='a'/> Flexibility pays only when there is structure to find, enough data, and a "
            "loss that knows about costs. <bookmark mark='b'/> On a weak signal, the s-score's strong prior, that "
            "residuals revert, wastes less of the data. <bookmark mark='c'/> The contest was fair: the same residuals, "
            "the same days, the same costs. The network is not registered."
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

    def question(self):
        q = pause_card(r"a forecast has a daily IC of 0.01 across 49 assets. Roughly how many years of daily data are "
                       r"needed for its IC to be two standard errors from zero?")
        with self.voiceover(
            "Pause and predict. A forecast has a daily information coefficient of point zero one across forty-nine "
            "assets. Roughly how many years of daily data are needed before its IC is two standard errors from zero?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
