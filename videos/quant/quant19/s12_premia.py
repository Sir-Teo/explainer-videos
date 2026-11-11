from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, FWD, GOOD, PART, VAS, ZERO, ask, fit_right, illustration, load

CP_C, NN_C = QC.SPOT, QC.OPTION


class Premia(VoiceoverScene):
    def construct(self):
        self.card()
        self.theory()
        self.famabliss(load("famabliss"))
        self.validation()
        self.macro()

    def card(self):
        c = chapter_card(11, r"Bond risk premia", r"Can the curve forecast its own returns?", part=PART)
        with self.voiceover("Chapter eleven. Bond risk premia: does the curve forecast what bonds will earn?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theory(self):
        rows = [cmath(r"rx^{(n)}_{t+1}", r"=", r"p^{(n-1)}_{t+1} - p^{(n)}_t - y^{(1)}_t", font_size=42,
                      colors={r"rx^{(n)}_{t+1}": ZERO}),
                cmath(r"\mathbb{E}_t\big[rx^{(n)}_{t+1}\big]", r"=", r"\text{const}\quad\text{(expectations hypothesis)}",
                      font_size=38, colors={r"\mathbb{E}_t\big[rx^{(n)}_{t+1}\big]": ZERO}),
                cmath(r"\overline{rx}_{t+1}", r"=", r"\gamma_0 + \gamma_1 y^{(1)}_t + \gamma_2 f^{(2)}_t + \dots + "
                      r"\gamma_5 f^{(5)}_t + \varepsilon_{t+1}", font_size=38, colors={r"\overline{rx}_{t+1}": ZERO})]
        whys = [why(r"the excess return: buy an $n$-year zero, sell it a year later as an $(n{-}1)$-year zero, minus "
                    r"the one-year rate ($p$ are log prices)"),
                why(r"if long bonds paid the same premium at all times, the curve would only forecast rates; Fama and "
                    r"Bliss (1987) and Campbell and Shiller (1991) found that a steep curve forecasts high returns instead"),
                why(r"Cochrane and Piazzesi (2005): one combination of the five forward rates forecasts every maturity's "
                    r"excess return, with $R^2$ of about 35\% in their data")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.4, buff=0.7, edge=6.9)
        with self.voiceover(
            "Part eighteen split a long yield into the expected path of short rates and a term premium. Is the premium "
            "constant? Define the excess return: buy a bond, sell it a year later, and subtract what a one-year bill "
            "earned. <bookmark mark='a'/> If the premium were constant, the slope of the curve would forecast only "
            "future rates. Eugene Fama and Robert Bliss in 1987, and John Campbell and Robert Shiller in 1991, found "
            "the opposite: a steep curve forecasts high bond returns. <bookmark mark='b'/> In 2005 John Cochrane and "
            "Monika Piazzesi went further: a single combination of five forward rates forecast the excess returns of "
            "every maturity, explaining a third or more of their variation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def famabliss(self, fb):
        rows = fb["rows"]
        g = axes([1.4, 5.6], [-0.2, 2.0], x_length=6.6, y_length=4.2, xlabel=r"bond maturity $n$, years",
                 ylabel=r"slope on the forward spread", xticks=[2, 3, 4, 5], yticks=[0, 0.5, 1.0, 1.5, 2.0], font_size=14
                 ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        eh = Line(ax.c2p(1.4, 0), ax.c2p(5.6, 0), color=BAD, stroke_width=3)
        pts = VGroup()
        for r_ in rows:
            n_, b_, se = r_["n"], r_["slope"], r_["se"]
            pts.add(VGroup(Line(ax.c2p(n_, b_ - 2 * se), ax.c2p(n_, b_ + 2 * se), color=CP_C, stroke_width=4),
                           Dot(ax.c2p(n_, b_), color=CP_C, radius=0.09)))
        side = VGroup(
            MathTex(r"rx^{(n)}_{t+1} = \alpha + \beta_n\big(f^{(n)}_t - y^{(1)}_t\big) + \varepsilon", font_size=28),
            legend([(BAD, r"expectations hypothesis: $\beta_n = 0$"), (CP_C, r"estimate, $\pm$ 2 Newey--West s.e.")],
                   font_size=16),
            MathTex(rf"R^2:\ {100 * rows[0]['r2']:.0f}\text{{--}}{100 * rows[-1]['r2']:.0f}\%", font_size=26),
            wrapped_label(rf"monthly, {fb['start']}--{fb['end']}, overlapping one-year returns on the Fed's zero curve. "
                          r"a slope near one associates the spread with expected excess returns in this regression; not a universal decomposition",
                          3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Regress a zero's one-year excess log return on its own forward spread, the last annual forward minus the one-year yield. <bookmark mark='a'/> A constant conditional expected excess return implies zero slope here. This is a test of that return restriction, which is not identical to every version of an expectations hypothesis stated in yield levels. <bookmark mark='b'/> On this full sample of public fitted curves, slopes run from {rows[0]['slope']:.1f} to {rows[-1]['slope']:.1f}. The bars show plus or minus two Newey-West standard errors with twelve lags for overlapping annual outcomes. They summarize association, not causality or a live forecast. A slope near one links the forward spread to expected excess returns within this regression; it does not establish that all yield spreads are risk premia. The curves use a current data vintage and are smoothed estimates rather than directly investable bond prices."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(eh), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.25), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()





    def macro(self):
        rows = [cmath(r"X_t", r"=", r"\big(\text{inflation},\ \text{real activity},\ \text{latent}_1, \dots\big)",
                      font_size=40, colors={r"X_t": FWD}),
                cmath(r"r_t", r"=", r"\delta_0 + \delta_1^\top X_t,\quad \lambda_t = \lambda_0 + \lambda_1 X_t", font_size=40,
                      colors={r"r_t": ZERO}),
                cmath(r"y^{(n)}_t", r"=", r"A_n + B_n^\top X_t", font_size=42, colors={r"y^{(n)}_t": ZERO})]
        whys = [why(r"Ang and Piazzesi (2003): put macroeconomic variables into the state of an affine model, beside the "
                    r"curve's own factors"),
                why(r"a Taylor-like rule for the short rate (Part 18), and prices of risk that move with the state: a "
                    r"time-varying premium, which the expectations hypothesis forbids"),
                why(r"still affine (chapter 2), so every yield is in closed form, and every yield splits into expected "
                    r"rates and a premium, as the ACM model of Part 18 does")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "The models that connect these premia to the economy are the macro-finance term-structure models. In 2003 "
            "Andrew Ang and Monika Piazzesi put inflation and real activity into the state of an affine model. "
            "<bookmark mark='a'/> The short rate follows something like a Taylor rule, and the price of risk moves "
            "with the state, so the premium varies through time. <bookmark mark='b'/> And it stays affine: every yield "
            "is in closed form, and every yield splits into expected rates and a premium, the decomposition the "
            "central banks publish."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        q = ask(r"a model forecasts bond excess returns with an out-of-sample $R^2$ of 0.3, but only by getting the "
                r"average right. Could you trade it, and what would you be betting on?")
        with self.voiceover("A model forecasts bond returns out of sample, but only by getting their average right. "
                            "Could you trade it, and what would you really be betting on?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def validation(self):
        title = label(r"A forecast needs a test of its own", font_size=34).to_edge(UP, buff=0.4)
        entries = [
            (r"1. Fix the target and information set", r"one-year excess log returns; dated curve inputs; publication lags"),
            (r"2. Fit and select before the test", r"fit coefficients and scalers on training data; tune only on validation"),
            (r"3. Respect overlapping outcomes", r"a twelve-month target crosses split dates; purge or embargo the boundary"),
            (r"4. Declare the benchmark and every trial", r"compare with a feasible expanding mean; count architectures, seeds and variants"),
            (r"5. Open a sealed test only once", r"report errors, uncertainty, turnover and costs; no sealed scores in this review"),
        ]
        cards = VGroup(*[VGroup(label(a, font_size=25, color=FWD),
                    wrapped_label(b, 11.5, 21, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
                    for a,b in entries]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(title, DOWN, buff=0.4)
        with self.voiceover("A descriptive regression and a tradable forecast answer different questions. A regression fitted through the final date can summarize a historical relation, but it cannot certify performance on unseen returns. <bookmark mark='a'/> First define a one-year excess log return and the information available at each forecast date. Current-vintage fitted Treasury curves are useful for replication, but a live claim also needs a vintage and publication-lag audit. <bookmark mark='b'/> Fit coefficients, normalization and any neural network on training data. Select the model on validation data. Because the outcomes span twelve months, simply splitting on the forecast date leaves returns crossing the boundary; purge those observations or impose an embargo. <bookmark mark='c'/> Compare the forecast with an expanding historical mean that could actually have been known, rather than a test-period average. Record every specification tried, including seeds and tuning choices. <bookmark mark='d'/> Only then can an authorized, once-only sealed test be informative. This review does not open that test or report its scores. Even a positive out-of-sample R squared would not by itself establish market timing: a shifted forecast mean can beat the benchmark without useful month-to-month covariance. A trading claim also needs position rules, financing, turnover, costs and uncertainty from dependent observations.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until("a"); self.play(FadeIn(cards[1]))
            vo.wait_until("b"); self.play(FadeIn(cards[2]))
            vo.wait_until("c"); self.play(FadeIn(cards[3]))
            vo.wait_until("d"); self.play(FadeIn(cards[4]))
        self.wait(0.4)
        self.clear_scene()
