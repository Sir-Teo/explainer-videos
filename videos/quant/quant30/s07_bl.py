from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, SHRINK_C, TRUE_C, fit_right, load


class BlackLitterman(VoiceoverScene):
    def construct(self):
        b = load("bl")
        self.card()
        self.reverse(b)
        self.formula()
        self.view(b)
        self.weights(b)
        self.question()

    def card(self):
        c = chapter_card(6, r"Black--Litterman", r"What if the optimizer started from the market, not from estimated "
                         r"means?", part=PART)
        with self.voiceover("Chapter six. In 1990, at Goldman Sachs, Fischer Black and Robert Litterman faced the "
                            "problem of the first chapter: optimizers fed with estimated means gave absurd portfolios. "
                            "Their answer was to start from the market itself."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def reverse(self, b):
        rows = [cmath(r"w_{\text{mkt}}", r"=", r"\tfrac1\delta\Sigma^{-1}\Pi", font_size=34, colors={r"w_{\text{mkt}}": TRUE_C}),
                cmath(r"\Pi", r"=", r"\delta\,\Sigma\,w_{\text{mkt}}", font_size=36, colors={r"\Pi": TRUE_C}),
                cmath(r"\delta", r"=", rf"\frac{{\mathbb E[r_m]}}{{\sigma_m^2}} \approx {b['delta']:.1f}", font_size=32)]
        whys = [why(r"if everyone held mean-variance portfolios with risk aversion $\delta$, the market would be the "
                    r"optimum (Part 23's CAPM)"),
                why(r"so run the optimizer backwards: the expected excess returns that make today's market weights "
                    r"optimal, the equilibrium returns"),
                why(r"the market's own excess return over its variance, here from 2011--2020 monthly data (high: a decade "
                    r"of strong returns and calm)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The first idea is to run the optimizer backwards. <bookmark mark='a'/> If every investor held a "
            "mean-variance portfolio, the market portfolio would be the optimum. <bookmark mark='b'/> So ask which "
            "expected returns would make today's market weights optimal: delta times the covariance times the market "
            "weights. These are the equilibrium returns, and they are as stable as the covariance is, because no mean "
            f"was estimated. <bookmark mark='c'/> Delta is the market's risk aversion; from the last decade of the "
            f"research data, about {b['delta']:.1f}."
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

    def formula(self):
        rows = [cmath(r"\mu", r"\sim", r"N(\Pi,\ \tau\Sigma)", font_size=34, colors={r"\mu": TRUE_C}),
                cmath(r"P\mu", r"=", r"Q + \varepsilon,\quad \varepsilon \sim N(0, \Omega)", font_size=34, colors={r"P\mu": EST_C}),
                cmath(r"\mu_{\text{BL}}", r"=", r"\big[(\tau\Sigma)^{-1} + P^\top\Omega^{-1}P\big]^{-1}\big[(\tau\Sigma)^{-1}\Pi + "
                      r"P^\top\Omega^{-1}Q\big]", font_size=28, colors={r"\mu_{\text{BL}}": SHRINK_C})]
        whys = [why(r"the prior: expected returns are near equilibrium, with an uncertainty proportional to the "
                    r"covariance ($\tau$ small)"),
                why(r"the views: linear statements about expected returns, each with its own confidence"),
                why(r"the posterior: a precision-weighted average of the two (Black and Litterman 1992; the form of He "
                    r"and Litterman 1999)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The second idea is Bayes. <bookmark mark='a'/> Treat the equilibrium returns as a prior: expected returns "
            "are near them, with an uncertainty proportional to the covariance. <bookmark mark='b'/> Express what you "
            "believe as views, linear statements such as one industry beating another, each with a confidence. "
            "<bookmark mark='c'/> The posterior mean is the precision-weighted average of the two. With no views it is "
            "the market; with confident views it moves toward them, and only in the directions the views speak about."
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

    def view(self, b):
        c = b["columns"]
        i, j = c.index("Softw"), c.index("Util")
        names = [r"software", r"utilities"]
        vals = [(b["pi"][i], b["pi"][j], TRUE_C, r"equilibrium $\Pi$"), (b["post"][i], b["post"][j], SHRINK_C,
                                                                          r"posterior"),
                (b["sample_mean"][i], b["sample_mean"][j], EST_C, r"sample mean, 2011--20")]
        top = 0.2
        g = axes([-0.5, 1.5], [0, top], x_length=6.0, y_length=4.2, xlabel=r"", ylabel=r"expected excess return, a year",
                 xticks=[], yticks=[0, 0.1, 0.2], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15).move_to(LEFT * 2.4 + DOWN * 0.1)
        ax = g.ax
        bars = VGroup()
        for k, (a_, b_, col, _) in enumerate(vals):
            for x, v in ((0, a_), (1, b_)):
                r = Rectangle(width=0.32, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                              fill_color=col, fill_opacity=0.85)
                r.move_to(ax.c2p(x - 0.36 + 0.36 * k, 0), aligned_edge=DOWN)
                bars.add(r)
        labs = VGroup(*[label(n, font_size=18, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.2) for x, n in
                        enumerate(names)])
        leg = legend([(col, t) for _, _, col, t in vals], font_size=15).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        spread_eq = b["pi"][i] - b["pi"][j]
        spread_post = b["post"][i] - b["post"][j]
        view_pct = 100 * b["view"][2]
        side = wrapped_label(rf"the view: software beats utilities by {view_pct:.0f}\% a year, held with the prior's own "
                             rf"confidence. Equilibrium already says {100 * spread_eq:.1f}\%; the posterior, "
                             rf"{100 * spread_post:.1f}\%", 3.6, 15, GREY_A).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "An example on the industries. <bookmark mark='a'/> The market's weights imply that software should earn "
            f"{100 * b['pi'][i]:.1f} percent a year over cash, and utilities {100 * b['pi'][j]:.1f}. <bookmark mark='b'/> "
            f"Now a view that sounds bullish on software: it will beat utilities by {view_pct:.0f} percent a year. But "
            f"equilibrium already says {100 * spread_eq:.1f} percent. Relative to the market, the view is bearish, and "
            f"the posterior spread falls to {100 * spread_post:.1f} percent. A view in Black-Litterman is a statement "
            "about what the market has not already priced."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(bars[k], DOWN) for k in (0, 1)])
            vo.wait_until("b")
            self.play(*[GrowFromEdge(bars[k], DOWN) for k in (2, 3)], FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def weights(self, b):
        c = b["columns"]
        wd = np.asarray(b["w_post"]) - np.asarray(b["w_mkt"])
        k_out, k_in = int(np.argmin(wd)), int(np.argmax(wd))
        cards = VGroup(
            desk_question(r"the posterior portfolio", rf"moves {100 * abs(wd[k_out]):.1f}\% of weight from "
                          rf"{c[k_out]} to {c[k_in]}, and leaves the other {len(c) - 2} industries at their market "
                          r"weights: the view touches only what it speaks about", width=12.4, font_size=19),
            desk_question(r"against the sample means", rf"plugging 2011--20's sample means into the same optimizer gives "
                          rf"weights whose absolute values sum to {b['gross_sample']:.0f}: Chapter 1's error maximiser",
                          width=12.4, font_size=19),
            desk_question(r"what BL is", r"shrinkage of the means toward equilibrium, with the views as the only "
                          r"departures: the same idea as Chapter 4, applied to the first moment", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the portfolio. <bookmark mark='a'/> The posterior portfolio moves "
            f"{100 * abs(wd[k_out]):.1f} percent of weight out of software and into utilities, and leaves every other "
            "industry at its market weight. <bookmark mark='b'/> Compare the naive alternative: plug the decade's sample "
            f"means into the same optimizer, and the weights' absolute values sum to {b['gross_sample']:.0f}. "
            "<bookmark mark='c'/> Black-Litterman is shrinkage of the means toward equilibrium, with the views as the "
            "only departures."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the view is held with zero confidence, $\Omega \to \infty$. What are the posterior returns, and "
                       r"the portfolio?")
        with self.voiceover(
            "Pause and predict. What happens to the posterior and the portfolio if the view is held with no confidence "
            "at all?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
