from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, CURV, GOOD, LEVEL, PART, SLOPE, ask, butterfly_example, illustration, load


class RV(VoiceoverScene):
    def construct(self):
        f = butterfly_example()
        self.card()
        self.salomon()
        self.build(f)
        self.rule(f)
        self.verdict(f)

    def card(self):
        c = chapter_card(16, r"Relative value: the butterfly", r"Can you trade the curve's shape and nothing else?",
                         part=PART)
        with self.voiceover("Chapter sixteen. Relative value: trading the curve's shape."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def salomon(self):
        fc = firm_card(r"Salomon Brothers",
                       r"its bond arbitrage group, led by John Meriwether, bought cheap Treasuries and sold rich ones of "
                       r"nearly the same maturity, hedged and leveraged, and became famous for it in the 1980s. "
                       r"In 1991 its government desk was found to have submitted false bids to get around the Treasury's "
                       r"limit of 35\% of any auction per bidder; in the May 1991 two-year note auction Salomon "
                       r"controlled more than 90\% of the issue",
                       numbers=[(r"35\%", r"limit per bidder"), (r">90\%", r"of the May 1991 two-year notes"),
                                (r"\$290\,\text{m}", r"sanctions, forfeitures and restitution, 1992")],
                       source=r"SEC and DOJ settlements (1992); Federal Reserve Bank of Cleveland (1992)", width=6.6,
                       font_size=21).to_edge(LEFT, buff=0.5)
        after = VGroup(
            wrapped_label(r"Meriwether left Salomon in 1991. In 1994 he founded Long-Term Capital Management with "
                          r"several of the arbitrage group, and Robert Merton and Myron Scholes as partners", 5.4, 20,
                          GREY_A),
            wrapped_label(r"related relative-value and financing risks recur in Part 41, which examines LTCM in 1998", 5.4, 20,
                          QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The firm file for this chapter is Salomon Brothers. In the 1980s its bond arbitrage group, led by John "
            "Meriwether, bought Treasuries that looked cheap against nearly identical ones, sold the rich ones, hedged "
            "the rest, and levered the difference; the group became famous for it. <bookmark mark='a'/> In 1991 the firm's government bond desk was "
            "caught submitting false bids to get around the Treasury's rule that no bidder may take more than "
            "thirty-five percent of an auction; in the May two-year auction, Salomon ended up controlling more than "
            "ninety percent. The settlements in 1992 came to two hundred and ninety million dollars. "
            "<bookmark mark='b'/> Meriwether resigned. In 1994 he founded Long-Term Capital Management, with much of "
            "the old group and two future Nobel laureates. Part forty-one tells how it ended."
        ) as vo:
            self.play(FadeIn(fc))
            vo.wait_until("a")
            self.play(Indicate(fc, color=QC.FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(after))
        self.wait(0.4)
        self.clear_scene()

    def build(self, f):
        w = np.asarray(f["weights"])
        rows = [cmath(r"F", r"=", rf"{w[0]:.3f}y^{{(2)}}+y^{{(5)}}{w[2]:+.3f}y^{{(10)}}", font_size=40, colors={r"F": CURV}),
                cmath(r"\ell^\top w", r"=", r"0,\qquad s^\top w=0", font_size=40),
                cmath(r"\Delta F", r"=", r"(c^\top w)\Delta s_3+\text{omitted components}", font_size=34),
                cmath(r"\Delta V", r"\simeq", r"-D_{5,\mathrm{bp}}\,\Delta F_{\mathrm{bp}}", font_size=40, colors={r"\Delta V": BAD})]
        whys = [why(r"a descriptive yield combination in the full-sample December 1985--2025 PCA basis; not a strategy backtest"),
                why(r"solve for two wings with belly weight one. This cancels two fitted linear loadings, not every form of curve risk"),
                why(r"the remaining factor and residual risks are not a guarantee of mean reversion or profitability"),
                why(r"if the belly DV01 is dollars per bp and bond DV01 weights are proportional to w, positive weighted yield change means negative first-order value change; carry and costs omitted")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.8, buff=0.62, edge=6.8)
        with self.voiceover(f"A butterfly combines a five-year belly with two- and ten-year wings. Here the weights come from the already-restored full-sample principal components of chapter ten, not the legacy strategy's training window. <bookmark mark='a'/> Fix the belly coefficient at one and solve two linear equations to cancel the fitted level and slope loadings. The wing coefficients are {w[0]:.3f} and {w[2]:.3f}. This neutrality is exact only for these linear yield loadings and this basis. <bookmark mark='b'/> Curvature and omitted components remain. Also distinguish a yield combination from bond profit: with signed bond DV01 weights proportional to these coefficients, a rise in the weighted yield causes a first-order loss. Coupon cash flows, financing, convexity and changing loadings add further differences.") as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def rule(self, f):
        title = label(r"Proposed validation protocol: not executed", font_size=30, color=QC.HOUSE).to_edge(UP, buff=0.4)
        rows = VGroup(*[wrapped_label(text, 12.0, 23, GREY_A) for text in [
            r"Freeze a decision-time fitting window, signal, holdings, exit rule and risk limits",
            r"Specify actual bond-price P\&L, carry, financing, turnover and executable bid/ask costs",
            r"Choose a genuinely untouched evaluation window before seeing results; record all configurations",
            r"Report uncertainty, stress losses and implementation differences, not only a Sharpe ratio",
            r"This pass: no legacy fly cache, sealed-return opening, new registration or strategy score",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(title, DOWN, buff=0.6)
        with self.voiceover("A factor hedge is not yet a tested relative-value strategy. Before any future return evaluation, specify the fitting window, signal timing, position convention, holding rule, financing, turnover and executable costs. Full-sample fitted curves are not decision-time executable quotes. <bookmark mark='a'/> Freeze the specification and select a genuinely untouched evaluation window before inspecting its outcomes. Report uncertainty and every configuration tried. This pass does not load the legacy fly cache, open its sealed return window, register another strategy or show historical Sharpe ratios. The validation protocol here is explicitly unfinished.") as vo:
            self.play(FadeIn(title), LaggedStart(*[FadeIn(x) for x in rows[:3]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(FadeIn(rows[3:]))
        self.wait(0.5)
        self.clear_scene()

    def verdict(self, f):
        title = label(r"Factor neutrality is an exposure condition", font_size=30).to_edge(UP, buff=0.5)
        rows = VGroup(*[wrapped_label(text, 11.8, 24, GREY_A) for text in [
            r"Two fitted linear loadings cancel in one full-sample basis",
            r"Higher factors, changing loadings, funding and execution risks remain",
            r"Bond portfolios require signed DV01 weights and consistent price/cash-flow units",
            r"No strategy return or historical profitability result is established here",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.6)
        with self.voiceover("What has actually been established? Two linear factor loadings were cancelled in a fixed descriptive basis. <bookmark mark='a'/> This does not cancel higher components, unstable loadings, funding or execution risk. A yield combination can drift for years without offering an admissible arbitrage. <bookmark mark='b'/> Turning it into a bond portfolio requires consistent signed DV01 units and cash flows. The House report next shows residual coupon-portfolio exposures rather than assuming point-maturity neutrality transfers exactly. <bookmark mark='c'/> No historical profitability conclusion follows from these exposure equations. A completed return evaluation would require the frozen protocol and new, appropriately untouched evidence.") as vo:
            self.play(FadeIn(title), FadeIn(rows[0]))
            for i, mark in enumerate(["a", "b", "c"], 1):
                vo.wait_until(mark)
                self.play(FadeIn(rows[i]))
        self.clear_scene()
        question = wrapped_label(r"Pause and predict: $D_{5,\mathrm{bp}}=\$1{,}000/\mathrm{bp}$ and $\Delta F=+1$ bp. What is the first-order bond-portfolio value change?", 11.8, 29, QC.IDEA).shift(UP * 1.0)
        result = MathTex(r"\Delta V\simeq-1{,}000\times1=-\$1{,}000", font_size=44, color=BAD).shift(DOWN * 0.7)
        with self.voiceover('Pause and predict: the belly DV01 is one thousand dollars per basis point, and the weighted yield rises one basis point. What is the first-order value change for the corresponding long-belly bond portfolio, before carry and costs?'):
            self.play(FadeIn(question))
        self.wait(2.5)
        with self.voiceover('The first-order value change is minus one thousand dollars. The sign comes from bond prices falling when their weighted yield rises. This is a sensitivity calculation, not an observed trading return.'):
            self.play(FadeIn(result))
        self.wait(0.5)
        self.clear_scene()
