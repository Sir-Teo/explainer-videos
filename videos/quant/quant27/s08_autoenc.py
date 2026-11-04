from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MKT, NET, PART, TREE, ask, fit_right, load

COLS = {"linear betas": LINEAR, "CA1": TREE, "CA2": NET}


class Autoencoder(VoiceoverScene):
    def construct(self):
        a = load("autoenc")
        self.card()
        self.model()
        self.ipca()
        self.picture()
        self.fit(a["rows"])
        self.predict(a["rows"])
        self.question()

    def card(self):
        c = chapter_card(7, r"Autoencoder asset pricing", r"Which few factors move all coins, and do their betas say "
                         r"which will earn more?", part=PART)
        with self.voiceover("Chapter seven. From forecasting returns one asset at a time to explaining them all at "
                            "once: factor models, learned."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"r_{i,t+1}", r"=", r"\beta(z_{i,t})^{\top} f_{t+1} + \varepsilon_{i,t+1}", font_size=34,
                      colors={r"r_{i,t+1}": COIN}),
                cmath(r"x_{t+1}", r"=", r"\tfrac{1}{N_t}\,[\mathbf 1, Z_t]^{\top} r_{t+1}", font_size=34,
                      colors={r"x_{t+1}": HURDLE}),
                cmath(r"f_{t+1}", r"=", r"W\, x_{t+1}", font_size=34, colors={r"f_{t+1}": HURDLE}),
                cmath(r"\min_{\beta(\cdot),\,W}", r"\ ", r"\textstyle\sum_{t, i}\big(r_{i,t+1} - \beta(z_{i,t})^{\top} W x_{t+1}"
                      r"\big)^2", font_size=34, colors={r"\min_{\beta(\cdot),\,W}": NET})]
        whys = [why(r"a conditional factor model: $K$ common factors, and each coin's exposures are a function of its "
                    r"characteristics last week (Part 24's betas, now changing with the coin)"),
                why(r"characteristic-managed portfolios: the market, and for each characteristic a portfolio long the "
                    r"coins that rank high on it; 16 returns a week"),
                why(r"the factors are combinations of those portfolios, so they are tradable"),
                why(r"Gu, Kelly and Xiu (2021): fit both arms together. The beta arm is a network of $z$; the factor arm "
                    r"is linear. An autoencoder: returns in, a $K$-dimensional bottleneck, returns out")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Part 24 explained returns with factors and fixed betas. <bookmark mark='a'/> A conditional model lets the "
            "betas move: each coin's exposure to each of K common factors is a function of its characteristics last "
            "week. <bookmark mark='b'/> To make the factors tradable, build sixteen portfolios each week: the market, "
            "and for each characteristic a portfolio weighted by the coins' ranks on it. <bookmark mark='c'/> The "
            "factors are combinations of those. <bookmark mark='d'/> And fit both together, betas and factor weights, "
            "to make the model's returns as close as possible to the real ones. Returns go in, are squeezed through K "
            "factors, and come out again: an autoencoder, conditioned on characteristics. Gu, Kelly and Xiu built it "
            "in 2021."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def ipca(self):
        rows = [cmath(r"\beta(z)", r"=", r"\Gamma^{\top} z", font_size=34, colors={r"\beta(z)": LINEAR}),
                cmath(r"\hat f_{t+1}", r"=", r"\big(\Gamma^{\top} Z_t^{\top} Z_t \Gamma\big)^{-1} \Gamma^{\top} Z_t^{\top} r_{t+1}",
                      font_size=34, colors={r"\hat f_{t+1}": HURDLE}),
                cmath(r"\operatorname{vec}(\hat\Gamma)", r"=", r"\Big(\textstyle\sum_t Z_t^{\top}Z_t \otimes \hat f_{t+1}"
                      r"\hat f_{t+1}^{\top}\Big)^{-1} \textstyle\sum_t \big(Z_t \otimes \hat f_{t+1}^{\top}\big)^{\top} r_{t+1}",
                      font_size=30, colors={r"\operatorname{vec}(\hat\Gamma)": LINEAR}),
                cmath(r"Z_t^{\top}Z_t \propto I", r"\Rightarrow", r"\hat\Gamma = \text{top } K \text{ eigenvectors of } "
                      r"\textstyle\sum_t x_{t+1}x_{t+1}^{\top}", font_size=30, colors={r"Z_t^{\top}Z_t \propto I": GOOD})]
        whys = [why(r"the linear special case: betas linear in characteristics, $\Gamma$ a $d \times K$ matrix"),
                why(r"first-order condition in $f$, $\Gamma$ fixed: each week's factors are a cross-sectional regression "
                    r"of returns on the betas (Fama--MacBeth, Part 24)"),
                why(r"first-order condition in $\Gamma$, factors fixed: a pooled regression; alternate the two until they "
                    r"agree. Instrumented PCA, Kelly, Pruitt and Su (2019)"),
                why(r"if the characteristics are orthonormal each week, the alternation is solved in one step: principal "
                    r"components of the managed portfolios. The autoencoder is the nonlinear extension of this PCA")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "For the researcher, the linear case has a closed structure. <bookmark mark='a'/> Make the betas linear in "
            "the characteristics, through a matrix gamma. <bookmark mark='b'/> With gamma fixed, minimising the error "
            "over each week's factors is a cross-sectional regression of returns on the betas: Fama and MacBeth's "
            "step. <bookmark mark='c'/> With the factors fixed, the condition for gamma is a single pooled regression. "
            "Alternate the two to a fixed point and you have Kelly, Pruitt and Su's instrumented principal components. "
            "<bookmark mark='d'/> And if the characteristics are orthonormal each week, the fixed point is reached in "
            "one step: gamma is the top eigenvectors of the managed portfolios' second-moment matrix. The autoencoder "
            "replaces the linear map by a network; everything else is this."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def picture(self):
        def stack(n, col, h=0.22):
            return VGroup(*[Circle(radius=h / 2, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3)
                            for _ in range(n)]).arrange(DOWN, buff=0.08)
        z_in = stack(8, COIN)
        hid = stack(6, NET)
        beta = stack(3, LINEAR)
        x_in = stack(8, HURDLE)
        fac = stack(3, HURDLE)
        out = stack(1, GOOD, h=0.4)
        left = VGroup(z_in, hid, beta).arrange(RIGHT, buff=1.0)
        right = VGroup(x_in, fac).arrange(RIGHT, buff=1.0)
        arms = VGroup(left, right).arrange(DOWN, buff=0.9).move_to(LEFT * 1.6)
        out.next_to(arms, RIGHT, buff=1.5)

        def connect(a, b, col):
            return VGroup(*[Line(p.get_center(), q.get_center(), stroke_width=0.6, color=col, stroke_opacity=0.4)
                            for p in a for q in b])
        lines = VGroup(connect(z_in, hid, NET), connect(hid, beta, NET), connect(x_in, fac, HURDLE),
                       *[Line(b_.get_center(), out.get_center(), stroke_width=1.2, color=GREY_B) for b_ in beta],
                       *[Line(f_.get_center(), out.get_center(), stroke_width=1.2, color=GREY_B) for f_ in fac])
        labs = VGroup(label(r"characteristics $z_{i,t}$", font_size=17, color=COIN).next_to(z_in, LEFT, buff=0.2),
                      label(r"betas $\beta(z_{i,t})$", font_size=17, color=LINEAR).next_to(beta, UP, buff=0.15),
                      label(r"managed portfolios $x_{t+1}$", font_size=17, color=HURDLE).next_to(x_in, LEFT, buff=0.2),
                      label(r"factors $f_{t+1}$", font_size=17, color=HURDLE).next_to(fac, DOWN, buff=0.15),
                      label(r"$\hat r_{i,t+1} = \beta^{\top} f$", font_size=20, color=GOOD).next_to(out, RIGHT, buff=0.2))
        for l_ in labs:
            fit_right(l_)
        with self.voiceover(
            "As a picture. <bookmark mark='a'/> On top, the beta arm: a coin's characteristics go through a small "
            "network to K exposures. <bookmark mark='b'/> Below, the factor arm: this week's sixteen managed portfolios "
            "go through a linear map to K factor returns. <bookmark mark='c'/> Their inner product is the model's "
            "return for that coin. With one hidden layer of thirty-two units the House calls it CA1, with two, CA2, and "
            "with none, linear betas: instrumented PCA."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left), Create(lines[0]), Create(lines[1]), FadeIn(labs[0]), FadeIn(labs[1]))
            vo.wait_until("b")
            self.play(FadeIn(right), Create(lines[2]), FadeIn(labs[2]), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(FadeIn(out), Create(VGroup(*lines[3:])), FadeIn(labs[4]))
        self.wait(0.4)
        self.clear_scene()

    def _plot(self, rows, key, lo, hi, ylabel, yticks):
        g = axes([0.6, 5.4], [lo, hi], x_length=7.0, y_length=4.0, xlabel=r"factors $K$", ylabel=ylabel,
                 xticks=[1, 2, 3, 4, 5], yticks=yticks, yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=14).move_to(
            LEFT * 1.8 + DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        for nm, col in COLS.items():
            ks = [r["K"] for r in rows if r["model"] == nm]
            vs = [r[key] for r in rows if r["model"] == nm]
            lines.add(VGroup(curve(ax, ks, np.clip(vs, lo, hi), col, stroke_width=3),
                             *[Dot(ax.c2p(k, min(max(v, lo), hi)), radius=0.06, color=col) for k, v in zip(ks, vs)]))
        leg = legend([(c, n) for n, c in COLS.items()], font_size=18).to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
        fit_right(leg)
        return g, lines, leg

    def fit(self, rows):
        g, lines, leg = self._plot(rows, "total", 0.3, 0.6, r"total $R^2$ on 2020, weekly", [0.3, 0.4, 0.5, 0.6])
        best = max(rows, key=lambda r: r["total"])
        one = [r["total"] for r in rows if r["K"] == 1]
        side = VGroup(
            MathTex(rf"K = 1:\ {100 * min(one):.0f}\text{{--}}{100 * max(one):.0f}\%", font_size=24, color=MKT),
            MathTex(rf"\text{{best}}:\ {100 * best['total']:.1f}\%\ ({best['model']}, K = {best['K']})".replace(
                "linear betas", r"\text{linear}"), font_size=24),
            wrapped_label(r"total $R^2 = 1 - \sum (r - \hat\beta^{\top}\hat f_t)^2 / \sum r^2$: how much of each week's "
                          r"returns the factors of that same week explain. Fitted on mid-2018 to mid-2019, tuned on the "
                          r"second half of 2019", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "How well does it explain? <bookmark mark='a'/> The total R squared, on 2020, which the models never saw: "
            "the share of each week's coin returns explained by the factors of the same week. One factor already "
            "explains about forty-five percent. That factor is the crypto market: when Bitcoin moves, everything "
            "moves. <bookmark mark='b'/> More factors add a few points; five linear ones reach about fifty-one and a "
            "half. The networks do not beat the linear betas here; the two-layer one is the worst. On a few thousand "
            "coin-weeks, the nonlinearity that helped Gu, Kelly and Xiu on sixty years of stocks has nothing to work "
            "with."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=2))
            self.play(FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def predict(self, rows):
        g, lines, leg = self._plot(rows, "pred", -0.03, 0.01, r"predictive $R^2$ on 2020", [-0.03, -0.02, -0.01, 0, 0.01])
        ax = g[0]
        zero = DashedLine(ax.c2p(0.6, 0), ax.c2p(5.4, 0), color=GREY_B, stroke_width=1.5)
        eq = MathTex(r"R^2_{\text{pred}} = 1 - \frac{\sum (r_{i,t+1} - \hat\beta(z_{i,t})^{\top}\hat\lambda)^2}{\sum r_{i,t+1}^2},"
                     r"\quad \hat\lambda = \overline{\hat f}", font_size=26).to_edge(UP, buff=0.3)
        side = wrapped_label(r"the factor means $\hat\lambda$ are estimated from mid-2018 to 2019 (the average coin: "
                             r"$-26\%$, then $-57\%$) and used in 2020 ($+143\%$): a model can know the betas exactly and still forecast with the wrong "
                             r"sign. The pricing errors are small; the premia are not stable", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Does it forecast? <bookmark mark='a'/> The predictive version replaces this week's factors by their "
            "average in the training years: a coin's expected return is its betas times the factor premia. "
            "<bookmark mark='b'/> Every model, every K, is below zero, about minus two percent. <bookmark mark='c'/> "
            "The reason is the premia, not the betas. They were estimated from mid-2018 to the end of 2019, when the "
            "average coin lost about two thirds of its value, and applied to 2020, when it more than doubled. A factor model can describe the "
            "co-movement almost perfectly and still forecast the level with the wrong sign. Explaining returns and "
            "predicting them are different problems, and only the second pays."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=2))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a factor model's total $R^2$ is 50\% but its predictive $R^2$ is negative. Name two ways to estimate "
                r"the premia $\lambda$ better, and what each assumes.")
        with self.voiceover(
            "Pause and predict. A factor model explains half the variance of returns but forecasts worse than zero. "
            "Name two ways to estimate the factor premia better, and say what each one assumes."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
