from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, FRONT, GOOD, MKT, PART, TAN, ask, fit_right, illustration, load


class CAPM(VoiceoverScene):
    def construct(self):
        c = load("capm")
        self.card()
        self.derive()
        self.sml_idea()
        self.noisy()
        self.flat(c)
        self.bab(c)
        self.roll()

    def card(self):
        c = chapter_card(3, r"The CAPM and the flat line", r"What return should a stock earn?", lit=(1964, 1977), part=PART)
        with self.voiceover("Chapter three. The capital asset pricing model: what follows if everyone holds the tangency, "
                            "and what the data say instead."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"w_T", r"=", r"w_{\text{mkt}}", font_size=42, colors={r"w_T": TAN}),
                cmath(r"\Sigma w_{\text{mkt}}", r"\propto", r"\mu - R^f\mathbf{1}", font_size=42),
                cmath(r"\mathbb{E}[R^i] - R^f", r"=", r"\beta_i\big(\mathbb{E}[R^m] - R^f\big),\quad \beta_i = "
                      r"\frac{\text{cov}(R^i, R^m)}{\text{var}(R^m)}", font_size=34, colors={r"\mathbb{E}[R^i] - R^f": MKT})]
        whys = [why(r"if everyone holds the same risky portfolio (Tobin) and markets clear, that portfolio must be the "
                    r"market itself: every share is held by someone"),
                why(r"the tangency condition says each asset's expected excess return is proportional to its covariance "
                    r"with the tangency portfolio, now the market"),
                why(r"Sharpe (1964), Lintner (1965), Mossin (1966): only market risk is paid. Risk that can be diversified "
                    r"away earns nothing, however large")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Suppose everyone uses the same estimates. Then everyone holds the same risky portfolio, and since every "
            "share must be held by someone, that portfolio is the market itself. <bookmark mark='a'/> The tangency "
            "condition then says something about every asset: its expected excess return is proportional to its "
            "covariance with the market. <bookmark mark='b'/> Divide by the market's variance and you have the capital "
            "asset pricing model of William Sharpe, John Lintner and Jan Mossin: an asset earns its beta times the "
            "market's premium. Only market risk is paid. Risk that can be diversified away earns nothing, however large "
            "it is."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def sml_idea(self):
        cards = VGroup(
            desk_question(r"the prediction", r"plot average excess returns against beta: the points should lie on a line "
                          r"through zero, with slope equal to the market's premium. That is the security market line",
                          width=12.0, font_size=21),
            desk_question(r"the test", r"Black, Jensen and Scholes (1972) sorted stocks into portfolios by beta and "
                          r"found the line too flat; Fama and French (1992) found it almost flat after controlling for "
                          r"size", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The model makes one sharp prediction. Plot each portfolio's average excess return against its beta, and "
            "the points should fall on a line through the origin, with a slope equal to the market's premium: the "
            "security market line. <bookmark mark='a'/> Fischer Black, Michael Jensen and Myron Scholes tested it in "
            "1972, sorting stocks by beta. The line came out too flat. Eugene Fama and Kenneth French, twenty years "
            "later, found it almost flat."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def noisy(self):
        rows = [cmath(r"\text{se}(\hat\beta)", r"\approx", r"\frac{\sigma_\varepsilon}{\sigma_m\sqrt{T}} = "
                      r"\frac{0.30/\sqrt{12}}{(0.15/\sqrt{12})\sqrt{60}} \approx 0.26", font_size=36,
                      colors={r"\text{se}(\hat\beta)": BAD}),
                cmath(r"\hat\lambda", r"\to", r"\lambda\cdot\frac{\text{var}(\beta)}{\text{var}(\beta) + \text{se}^2}",
                      font_size=40, colors={r"\hat\lambda": BAD}),
                cmath(r"\beta^{\text{adj}}", r"=", r"0.67\,\hat\beta + 0.33", font_size=40, colors={r"\beta^{\text{adj}}": MKT})]
        whys = [why(r"one stock, five years of monthly returns, idiosyncratic volatility 30\% and the market's 15\%: "
                    r"its estimated beta is uncertain by about a quarter either way"),
                why('regress average returns on noisy betas and the slope is biased toward zero: errors in variables. Black, Jensen and Scholes (1972) and Fama and MacBeth (1973) therefore sort stocks into portfolios, reducing idiosyncratic estimation noise; common errors and changing betas remain'),
                why(r"Blume (1971, 1975): betas also drift toward one over time, so the industry's 'adjusted beta' shrinks "
                    r"the estimate toward one; Vasicek's (1973) Bayesian version weights by the standard error")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Before testing the line, a word on how betas are measured, because a single stock's beta is very noisy. A stock with thirty percent idiosyncratic volatility, estimated on five years of monthly returns against a market of fifteen percent, has a beta uncertain by about a quarter either way. <bookmark mark='a'/> Regress average returns on such noisy betas and the slope is biased toward zero, the classic errors-in-variables problem. That is why Fischer Black, Michael Jensen and Myron Scholes, and then Fama and MacBeth, sorted stocks into portfolios by beta: diversification reduces idiosyncratic estimation error, but common residuals, changing betas and generated-regressor errors remain. A flat portfolio line is not automatically immune to noise. <bookmark mark='b'/> And practitioners shrink. Marshall Blume found that betas drift toward one, so the adjusted beta on a terminal screen is two thirds of the estimate plus one third. Oldrich Vasicek's Bayesian version shrinks each stock in proportion to how uncertain its own estimate is."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def flat(self, c):
        b, m = np.asarray(c["beta"]), np.asarray(c["means"])
        g = axes([0, 1.8], [0, 0.14], x_length=7.4, y_length=4.4, xlabel=r"beta", ylabel=r"average excess return, a year",
                 xticks=[0, 0.5, 1.0, 1.5], yticks=[0, 0.04, 0.08, 0.12], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), color=MKT, radius=0.08) for x, y in zip(b, m)])
        pred = Line(ax.c2p(0, 0), ax.c2p(1.8, 1.8 * c["mkt_prem"]), color=TAN, stroke_width=3)
        s = c["sml"]
        fit = Line(ax.c2p(0, s["intercept"]), ax.c2p(1.8, s["intercept"] + 1.8 * s["slope"]), color=BAD, stroke_width=3)
        side = VGroup(
            legend([(TAN, rf"CAPM: slope {100 * c['mkt_prem']:.1f}\%, through zero"),
                    (BAD, rf"fitted: slope {100 * s['slope']:.1f}\%, intercept {100 * s['intercept']:.1f}\%")], font_size=16),
            wrapped_label(rf"Kenneth French's beta-sorted deciles, value-weighted, {c['start'] // 100}--{c['end'] // 100}; "
                          r"betas estimated over the whole sample. Low-beta stocks earned too much, high-beta too little",
                          3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Here it is on fifty-seven years of data: ten portfolios sorted by beta, from {b[0]:.1f} to {b[-1]:.1f}. <bookmark mark='a'/> The model's line: through zero, rising at the market's premium of {100 * c['mkt_prem']:.0f} percent a year per unit of beta. <bookmark mark='b'/> The data's line: an intercept of {100 * s['intercept']:.1f} percent and a slope of {100 * s['slope']:.1f}, less than half the prediction. The low-beta portfolios earned more than this stock-index CAPM predicts; high beta is market exposure, not a ranking of total safety. This is a joint test of the model and the chosen market proxy."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Create(pred), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def bab(self, c):
        rows = [cmath(r"r^{BAB}", r"=", r"\frac{r^{\text{low}\,\beta}}{\beta_{\text{low}}} - \frac{r^{\text{high}\,\beta}}"
                      r"{\beta_{\text{high}}}", font_size=40, colors={r"r^{BAB}": GOOD})]
        whys = [why(f"lever the low-beta portfolio up to a beta of one and the high-beta one down: retrospective illustration using whole-sample betas, not implementable or published BAB performance; naive $t$. Here: {100 * c['bab_mean']:.1f}\\% a year, Sharpe {c['bab_sharpe']:.2f}, $t$ = {c['bab_t']:.1f}")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        cards = desk_question(r"why the line is flat", r"many investors cannot or will not borrow; to get more return they "
                              r"buy high-beta stocks instead of levering the market, bidding them up. Black (1972) saw "
                              r"it; Frazzini and Pedersen made it a trade", width=12.0, font_size=21).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"A flat fitted line motivates a mechanical long-short illustration, not a certified trade. Lever the lowest-beta portfolio up to a beta of one, lever the highest down to one, and go long the first and short the second. <bookmark mark='a'/> Using betas estimated over the same whole sample, the retrospective zero-cost illustration averaged {100 * c['bab_mean']:.1f} percent a year. This uses future beta information and ignores financing, costs and borrow constraints, so it is not a replication of published BAB performance. Andrea Frazzini and Lasse Pedersen studied betting against beta, and offered a reason: many investors cannot borrow, so to get more return they buy riskier stocks instead of levering safe ones, and bid them up. Fischer Black had suggested the same in 1972."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(cards, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def roll(self):
        rows = [cmath(r"\text{CAPM holds}", r"\iff", r"\text{the market portfolio is mean-variance efficient}",
                      font_size=36, colors={r"\text{CAPM holds}": MKT})]
        whys = [why(r"Roll (1977): the model is a statement about the true market portfolio of all wealth, including "
                    r"bonds, houses and human capital, which no one observes. A test with a stock index tests whether "
                    r"that index is efficient, nothing more")]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Richard Roll pointed out in 1977 that the CAPM is equivalent to a single statement: the market portfolio "
            "is efficient. And the market in the model is all wealth: stocks, bonds, houses, and the value of people's "
            "future earnings, which nobody observes. Every test with a stock index is a test of whether that index is "
            "efficient, nothing more. The model may be untestable; its failure with stock indices is not."
        ) as vo:
            step(0)
        q = ask(r"a stock has a beta of 1.5 and an idiosyncratic volatility of 60\%. The market premium is 6\%. What does "
                r"the CAPM say it should earn above cash, and why doesn't the 60\% matter?")
        with self.voiceover("A stock has a beta of one point five and sixty percent idiosyncratic volatility; the market "
                            "premium is six percent. What should it earn above cash, and why doesn't the sixty percent "
                            "matter?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
