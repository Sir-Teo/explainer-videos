from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, GOOD, PART, ZERO, ask, fit_right, house_lab, illustration, load

EXP = QC.SPOT
TP = QC.OPTION


class Term(VoiceoverScene):
    def construct(self):
        t = load("term_example")
        self.card()
        self.hypothesis()
        self.regressions(t)
        self.acm_method()
        self.decompose(t)

    def card(self):
        c = chapter_card(14, r"Expectations and the term premium", r"Is a long yield a forecast, or a price for risk?",
                         part=PART)
        with self.voiceover("Chapter fourteen. Expectations, and the term premium."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def hypothesis(self):
        rows = [cmath(r"y_t^{(n)}", r"\simeq", r"\frac1n\sum_{k=0}^{n-1}\mathbb{E}_t\big[r_{t+k}\big] + \text{TP}_t^{(n)}",
                      font_size=42, colors={r"y_t^{(n)}": ZERO, r"\text{TP}_t^{(n)}": TP}),
                cmath(r"\text{TP} = \text{const}", r"\Rightarrow",
                      r"y_{t+1}^{(n-1)} - y_t^{(n)} = a + b\,\frac{y_t^{(n)} - y_t^{(1)}}{n - 1},\ \ b = 1",
                      font_size=36, colors={r"\Rightarrow": WHITE}),
                cmath(r"rx_{t+1}^{(n)}", r"=", r"a + b\,\big(f_t^{(n-1,n)} - y_t^{(1)}\big) + \varepsilon,\ \ b = 0",
                      font_size=38, colors={r"rx_{t+1}^{(n)}": GOOD})]
        whys = [why(r"a log-linear expectations decomposition; the exact affine counterfactual also contains a convexity adjustment. A term premium is a model-dependent residual, not a directly observed fee"),
                why(r"the expectations hypothesis (premium constant): a steep curve means short rates will rise, so long "
                    r"yields rise too, one for one. Campbell and Shiller (1991)"),
                why(r"under this null the forward-spread predictor has slope zero; the expected excess return need not itself be zero. Fama and Bliss (1987)")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "A long zero yield can be described approximately as an expected average short rate plus a term premium. Log yields and stochastic discounting add convexity terms, so the precise definition depends on the model. <bookmark mark='a'/> Under a specified log-linear expectations hypothesis with constant maturity-specific premia, the Campbell-Shiller regression has slope one. Its left side follows a bond as its remaining maturity rolls down; it is not simply tomorrow's constant-maturity ten-year yield. <bookmark mark='b'/> In the Fama-Bliss regression the forward-spread predictor has slope zero under the corresponding null. That does not mean the expected excess return or intercept is zero. These are joint hypotheses about expectations, premia, specification and measurement."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def regressions(self, t):
        cs, fb = t["cs"], t["fb"]
        ks = ["12", "24", "36", "60", "120"]
        g1 = axes([-0.5, 4.5], [-3, 1.5], x_length=5.4, y_length=3.8, ylabel=r"Campbell--Shiller slope",
                  xticks=list(range(5)), xfmt=lambda v: f"{int(ks[int(v)]) // 12}" + r"\,\text{y}", yticks=[-3, -2, -1, 0, 1],
                  font_size=13)
        g2 = axes([-0.5, 3.5], [-0.5, 2], x_length=4.4, y_length=3.8, ylabel=r"Fama--Bliss slope",
                  xticks=list(range(4)), xfmt=lambda v: f"{int(v) + 2}" + r"\,\text{y}", yticks=[0, 1, 2], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).shift(DOWN * 0.4)

        def bars(ax, vals, ses, col, ref):
            out = VGroup()
            for i, (v, se) in enumerate(zip(vals, ses)):
                p0, p1 = ax.c2p(i - 0.25, 0), ax.c2p(i + 0.25, v)
                out.add(VGroup(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                                         fill_color=col, fill_opacity=0.8).move_to((p0 + p1) / 2),
                               Line(ax.c2p(i, v - 2 * se), ax.c2p(i, v + 2 * se), color=WHITE, stroke_width=2)))
            line = DashedLine(ax.c2p(-0.5, ref), ax.c2p(len(vals) - 0.5, ref), color=WHITE, stroke_width=2)
            return out, line
        b1, r1 = bars(g1.ax, [cs[k]["b"] for k in ks], [cs[k]["se"] for k in ks], BAD, 1.0)
        b2, r2 = bars(g2.ax, [fb[k]["b"] for k in ("2", "3", "4", "5")], [fb[k]["se"] for k in ("2", "3", "4", "5")],
                      GOOD, 0.0)
        l1 = label(r"dashed: the hypothesis says 1", font_size=16, color=GREY_B).next_to(g1, UP, buff=0.05)
        l2 = label(r"dashed: the hypothesis says 0", font_size=16, color=GREY_B).next_to(g2, UP, buff=0.05)
        foot = wrapped_label(rf"monthly, 1961--2025, fitted GSW curve; whiskers $\pm 2$ SE: conventional homoskedastic OLS on left, "
                             rf"Newey--West 12 lags on right; not calibrated confidence intervals. At 10 years $b = {cs['120']['b']:.2f}$; Fama--Bliss $R^2$ "
                             rf"{100 * fb['2']['r2']:.0f}--{100 * fb['5']['r2']:.0f}\%", 12.0, 18, GREY_A).to_edge(DOWN,
                                                                                                         buff=0.35)
        with self.voiceover(
            f"These are full-sample descriptive regressions on monthly yields derived from the pinned GSW fit, including a model-extrapolated short maturity. <bookmark mark='a'/> The Campbell-Shiller coefficients differ markedly from the slope-one benchmark; at ten years the saved estimate is {cs['120']['b']:.2f}. The left whiskers use conventional homoskedastic OLS standard errors, which do not correct serial dependence. <bookmark mark='b'/> The Fama-Bliss slopes are positive. Its annual returns overlap, and the displayed errors use twelve-lag Newey-West estimates. Twice a standard error is not a certified confidence interval here. These patterns challenge the joint null; time-varying premia are one interpretation, alongside expectation errors, specification and measurement issues. No out-of-sample trading performance is established."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2), Create(r1), Create(r2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP) for b_ in b1], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def acm_method(self):
        from explainer.quant.house import rates as R
        rows = [cmath(r"X_{t+1}", r"=", r"\mu + \Phi X_t + v_{t+1}", font_size=40, colors={r"X_{t+1}": ZERO}),
                cmath(r"rx_{t+1}^{(n)}", r"=", r"a_n + \beta_n^\top v_{t+1} + c_n^\top X_t + e_{t+1}^{(n)}", font_size=40,
                      colors={r"rx_{t+1}^{(n)}": GOOD}),
                cmath(r"(\lambda_0, \lambda_1)", r"=", r"(\beta\beta^\top)^{-1}\beta\,\big(a + \tfrac12(\cdots),\ c\big)",
                      font_size=40, colors={r"(\lambda_0, \lambda_1)": TP}),
                cmath(r"\text{TP}_t^{(n)}", r"=", r"y_t^{(n)}(\lambda) - y_t^{(n)}(\lambda = 0)", font_size=40,
                      colors={r"\text{TP}_t^{(n)}": TP})]
        whys = [why(r"the curve's state: its first five principal components, a vector autoregression"),
                why(r"one regression per maturity: what part of a bond's excess return is exposure to news, and what part "
                    r"was predictable"),
                why(r"the predictable part must be a price of risk times the exposure: one cross-sectional regression "
                    r"gives the prices of risk"),
                why(r"price every bond with them, and again with them set to zero: the difference is the premium")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.2, buff=0.55, edge=6.9)
        with self.voiceover(
            "Adrian, Crump and Moench's 2013 framework estimates an affine term-structure model through regressions. Here five principal components follow a vector autoregression. <bookmark mark='a'/> Bond excess returns are regressed on innovations and lagged state factors to estimate news exposure and predictability. <bookmark mark='b'/> A cross-sectional step estimates affine risk prices, with Gaussian and residual-variance corrections and rank assumptions. An estimated implementation need not enforce every no-arbitrage or specification restriction exactly. <bookmark mark='c'/> Price bonds using the fitted risk prices, then set those prices to zero in the same recursion. Their yield difference defines this example's term premium. The counterfactual yield contains a convexity adjustment; it is not simply an observed expectation. The NY Fed publishes a related model series, but its revised file no longer matches this repository's pinned vintage, so that numerical comparison is omitted."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()
        card = house_lab(r"the term premium in three regressions", R.acm_decompose, "# 2. excess returns", 14, width=12.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "In the House it is forty lines, and the heart of it is here: the excess returns, the regression on news "
            "and state, and the prices of risk."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def decompose(self, t):
        T, y, rn, tp = (np.asarray(t[k]) for k in ("t", "y10", "rn10", "tp10"))
        g = axes([1961, 2026], [-3, 16], x_length=8.2, y_length=4.6, xlabel=r"year", ylabel=r"10-year, percent",
                 xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(1961, 0), ax.c2p(2026, 0), color=GREY_D, stroke_width=1.5)
        ly = curve(ax, T, y, ZERO, stroke_width=2.5)
        lr = curve(ax, T, rn, EXP, stroke_width=2.5)
        lt = curve(ax, T, tp, TP, stroke_width=3)
        leg = legend([(ZERO, r"10-year yield (model fit)"), (EXP, r"zero-risk-price counterfactual yield"),
                      (TP, r"term premium (House example)")], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.8)
        sc = t["since_cut"]
        a, b = sc["2024-08"], sc["2025-12"]
        side = VGroup(
            wrapped_label(rf"in-sample fitted-yield RMSE: {t['fit_rmse_bp']:.1f} bp; NY Fed vintage comparison unavailable", 3.6, 18, GREY_A),
            wrapped_label(rf"1981: premium {t['tp_1981']:.1f}\%; {int(t['tp_min']['t'])}: {t['tp_min']['v']:.1f}\%", 3.6,
                          17, TP),
            wrapped_label(rf"Aug 2024 to Dec 2025, while the Fed cut: yield {b['y'] - a['y']:+.2f}, counterfactual "
                          rf"{b['rn'] - a['rn']:+.2f}, premium {b['tp'] - a['tp']:+.2f}", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.35, aligned_edge=LEFT)
        fit_right(side)
        with self.voiceover(
            f"This separately named example uses the original full-sample regression settings and unchanged House routines on the pinned Treasury curve. Blue is the zero-risk-price counterfactual yield; pink is the model's residual term premium. <bookmark mark='a'/> Its in-sample fitted-yield RMSE is {t['fit_rmse_bp']:.1f} basis points. That is a yield-fit statistic, not a measure of latent-premium accuracy, and the unavailable NY Fed comparison is not shown. <bookmark mark='b'/> This model estimates a premium of {t['tp_1981']:.1f} percentage points in September 1981 and a minimum of {t['tp_min']['v']:.1f} in {int(t['tp_min']['t'])}. These are retrospective model estimates, not direct observations of investor beliefs or identified effects of asset purchases. <bookmark mark='c'/> From August 2024 to December 2025 the counterfactual component falls {abs(b['rn'] - a['rn']):.2f} points while the estimated premium rises {b['tp'] - a['tp']:.2f}. Their sum rises. This accounting split explains how a fitted long yield can rise during policy easing without identifying the causes of each component."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(ly), Create(lr), FadeIn(leg[0]), FadeIn(leg[1]), run_time=2.5)
            self.play(Create(lt), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), run_time=1)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        q = ask(r"Which overnight policy instrument is set directly, and why can both fitted long-yield components change?")
        with self.voiceover('Pause and predict: which overnight policy instrument is set directly, and through what channels could both fitted long-yield components respond? Neither ten-year component is mechanically fixed by the committee.'):
            self.play(FadeIn(q))
        self.add(wrapped_label(r"Full-sample GSW model illustration; five PCs from 3-month and longer yields; short rate model-derived; NY Fed comparison omitted", 12.4, 16, GREY_B).to_edge(DOWN, buff=0.25))
        self.wait(0.5)
        self.clear_scene()
