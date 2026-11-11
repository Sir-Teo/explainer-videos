from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, FRONT, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class APT(VoiceoverScene):
    def construct(self):
        a = load("apt")
        self.card()
        self.ross()
        self.worked()
        self.pca(a)
        self.pricing(a)
        self.merton()

    def card(self):
        c = chapter_card(5, r"Many factors: APT and ICAPM", r"What if more than one risk is paid?", part=PART)
        with self.voiceover("Chapter five. Two ways to more than one risk factor: arbitrage, and hedging."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ross(self):
        rows = [cmath(r"R^i_t", r"=", r"a_i + \textstyle\sum_k \beta_{ik} f_{kt} + \varepsilon^i_t,\quad "
                      r"\varepsilon^i\ \text{nearly independent}", font_size=34, colors={r"R^i_t": MKT}),
                cmath(r"\mathbb{E}[R^i] - R^f", r"\approx", r"\textstyle\sum_k \beta_{ik}\,\lambda_k", font_size=42,
                      colors={r"\mathbb{E}[R^i] - R^f": SDF})]
        whys = [why(r"Ross (1976): suppose returns have a few common factors and otherwise diversifiable noise"),
                why(r"then a portfolio of many assets with zero exposure to every factor is nearly riskless, so it must "
                    r"earn nearly the riskless rate: no arbitrage forces expected returns to be linear in the betas. The "
                    r"theory does not say which factors, or their prices")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Stephen Ross took a different route in 1976. Suppose returns are driven by a few common factors, plus noise "
            "that is nearly independent across assets. <bookmark mark='a'/> Then with many assets you can build a "
            "portfolio with no exposure to any factor, whose noise diversifies away: nearly riskless. If it earned more "
            "than cash there would be an arbitrage. So expected returns must be, approximately, linear in the factor "
            "betas. The arbitrage pricing theory needs no assumption about investors at all; but it does not tell you "
            "which factors, or what they pay."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def worked(self):
        g = axes([0, 2.4], [0, 0.16], x_length=6.0, y_length=4.2, xlabel=r"factor beta, $\beta$",
                 ylabel=r"expected return", xticks=[0, 1, 2], yticks=[0, 0.04, 0.08, 0.12, 0.16], font_size=14
                 ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        rf = Dot(ax.c2p(0, 0.03), color=GREY_A, radius=0.08)
        A = Dot(ax.c2p(1, 0.08), color=GOOD, radius=0.09)
        B = Dot(ax.c2p(2, 0.12), color=BAD, radius=0.09)
        la = label(r"A: $\beta$ = 1, 8\%", font_size=16, color=GOOD).next_to(A, UL, buff=0.08)
        lb = label(r"B: $\beta$ = 2, 12\%", font_size=16, color=BAD).next_to(B, DOWN, buff=0.12)
        lr = label(r"cash, 3\%", font_size=16, color=GREY_A).next_to(rf, RIGHT, buff=0.1)
        line = DashedLine(ax.c2p(0, 0.03), ax.c2p(2.4, 0.15), color=GOOD, stroke_width=2)
        Z = Dot(ax.c2p(0, 0.04), color=SDF, radius=0.09)
        lz = label(r"2A $-$ B: $\beta$ = 0, 4\%", font_size=16, color=SDF).next_to(Z, RIGHT, buff=0.12).shift(UP * 0.15)
        side = VGroup(
            MathTex(r"2A - B:\ \ \beta = 2(1) - 2 = 0", font_size=26),
            MathTex(r"\mathbb{E} = 2(8\%) - 12\% = 4\% > 3\%", font_size=26, color=SDF),
            wrapped_label('weights 2 and $-1$ sum to one, so 2A $-$ B is a fully invested portfolio with no factor risk that beats cash by a point: exact arbitrage only with zero residual risk, unrestricted shorts and identical cash financing. With residual risk this is an approximate APT illustration. The trade stops only when $(\\mathbb{E} - r_f)/\\beta$ is the same for A and B', 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is the arbitrage in numbers, with one factor. Two well-diversified portfolios: A has a beta of one and expects eight percent; B has a beta of two and expects twelve. Cash pays three. <bookmark mark='a'/> Hold two units of A and short one of B. The weights add up to one, and the beta is two minus two: zero. The expected return is sixteen minus twelve, four percent. <bookmark mark='b'/> Only if residual risks cancel completely, with unrestricted shorts and identical cash financing, is this a riskless portfolio paying four when cash pays three: borrow at three, buy it, and pocket a point with no risk and no money of your own. Traders do that until the reward per unit of beta is the same for A and for B, five percent: If A and cash are held fixed in this illustration, B adjusts until it expects thirteen; other equilibrium adjustments are also possible. That is the whole of the APT: every well-diversified portfolio must sit on one straight line in beta."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rf), FadeIn(lr), FadeIn(A), FadeIn(la), FadeIn(B), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), TransformFromCopy(VGroup(A, B), Z), FadeIn(lz))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[2]))
            self.play(B.animate.move_to(ax.c2p(2, 0.13)), lb.animate.shift(UP * (ax.c2p(0, 0.13)[1] - ax.c2p(0, 0.12)[1])))
        self.wait(0.4)
        self.clear_scene()

    def pca(self, a):
        sh, cum = np.asarray(a["share"])[:10], np.asarray(a["cum"])[:10]
        g = axes([0.4, 10.6], [0, 1.0], x_length=7.4, y_length=4.2, xlabel=r"principal component",
                 ylabel=r"share of variance", xticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.55, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=FRONT, fill_opacity=0.85).move_to(
            [ax.c2p(i + 1, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for i, v in enumerate(sh)])
        line = curve(ax, np.arange(1, 11), cum, TAN, stroke_width=3)
        side = VGroup(
            legend([(FRONT, r"each component"), (TAN, r"cumulative")], font_size=17),
            MathTex(rf"\text{{first}}:\ {100 * sh[0]:.0f}\%;\ \text{{first five}}:\ {100 * cum[4]:.0f}\%", font_size=24),
            MathTex(f"|\\text{{corr(first, market)}}| = {a['corr_pc1_mkt']:.2f}", font_size=24, color=MKT),
            wrapped_label(f"monthly excess returns of {a['N']} industries, 1970--2025: the eigenvectors of their whole-sample covariance; PC signs are arbitrary. Descriptive in-sample fit, not structural-risk identification", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Which factors? One answer is to let the data choose. Take forty-nine industries and find the principal components of their returns, as Part eighteen did for the yield curve. <bookmark mark='a'/> The first explains {100 * sh[0]:.0f} percent of all the variance, and its absolute correlation with the market is {a['corr_pc1_mkt']:.2f}. <bookmark mark='b'/> The next few add a few percent each. This is a full-sample 1970 to 2025 descriptive variance decomposition. Principal-component signs are arbitrary; variance explained does not establish priced structural risk."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[1:]], lag_ratio=0.1), Create(line), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def pricing(self, a):
        r2 = a["r2"]
        hx = [-2.5, 2.5]
        tab = VGroup(VGroup(label(r"components used", font_size=19, color=GREY_A).move_to([hx[0], 1.6, 0]),
                            label(r"cross-sectional $R^2$ of mean returns", font_size=19, color=GREY_A).move_to(
                                [hx[1], 1.6, 0])))
        for i, r_ in enumerate(r2):
            y = 0.95 - 0.6 * i
            tab.add(VGroup(MathTex(str(r_["k"]), font_size=30).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['r2']:.2f}", font_size=30, color=BAD if r_["r2"] < 0.1 else TAN).move_to(
                               [hx[1], y, 0])))
        foot = wrapped_label('same assets and full sample estimate components, betas and means: descriptive in-sample pricing fit; large variance components explain little mean-return dispersion: what moves returns together is not necessarily what is paid. Kozak, Nagel and Santosh (2018) find that priced factors hide among the smaller components',
                             12.0, 17, GREY_A).to_edge(DOWN, buff=0.45)
        title = label(r"Do the big components price the industries?", font_size=26).to_edge(UP, buff=0.5)
        with self.voiceover(
            f"But do these components explain why some industries earn more than others? <bookmark mark='a'/> Use the same full sample and same industries to estimate components, betas and average returns, then regress those means on their exposures to the first component: an R squared of almost zero. Three components, still almost nothing; ten, {r2[-1]['r2']:.2f}. <bookmark mark='b'/> These are in-sample descriptive fits, not an out-of-sample pricing test or causal identification. What makes returns move together is not necessarily what investors are paid for. Serhiy Kozak, Stefan Nagel and Shrihari Santosh argue that the priced factors hide among the small components, which is why finding them is the hard problem of Parts twenty-four and twenty-five."
        ) as vo:
            self.play(FadeIn(title), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def merton(self):
        rows = [cmath(r"\mathbb{E}[R^i] - R^f", r"=", r"\gamma\,\text{cov}(R^i, R^W) + \lambda_z\,\text{cov}(R^i, \Delta z)",
                      font_size=36, colors={r"\mathbb{E}[R^i] - R^f": MKT})]
        whys = [why(r"Merton's intertemporal CAPM (1973): long-lived investors also hedge changes in their investment "
                    r"opportunities $z$ (interest rates, expected returns, volatility). An asset that pays when "
                    r"opportunities worsen is a hedge and earns less; the theory says which factors: the state variables "
                    r"that forecast returns")]
        step = ladder(self, rows, whys, keep=1, top=2.3, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Robert Merton's intertemporal model gives the other route. An investor who lives for many periods cares "
            "not only about their wealth but about the opportunities it will meet: future interest rates, future expected "
            "returns, future volatility. An asset that pays off when those opportunities worsen is a hedge, and earns "
            "less, just as insurance does. So the priced factors are the market plus whatever forecasts the future, a "
            "rule that disciplines the search, if it is taken seriously."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a factor explains 40\% of the variance of stock returns but none of their average returns. Is it a risk "
                r"factor? What would make it one?")
        with self.voiceover("A factor explains forty percent of the variance of stock returns, but none of their average "
                            "returns. Is it a risk factor? What would make it one?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
