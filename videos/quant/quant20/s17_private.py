from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, DEBT, EQUITY, PART, RISKY, ask, fit_right, illustration, load


class Private(VoiceoverScene):
    def construct(self):
        b = load("bdc")
        self.card()
        self.growth()
        self.marks(b)
        self.smoothing(load("glm"))
        self.feedback()

    def card(self):
        c = chapter_card(16, r"Private credit and its marks", r"What is a loan worth that never trades?", part=PART)
        with self.voiceover("Chapter sixteen. Private credit: loans that never trade, and how they are valued."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def growth(self):
        rows = [cmath(r"\text{lender}", r"=", r"\text{a fund or BDC, not a bank}", font_size=38, colors={r"\text{lender}": DEBT}),
                cmath(r"\text{loan}", r"=", r"\text{often floating rate and senior secured; illiquid, with model-based valuation}",
                      font_size=32, colors={r"\text{loan}": RISKY})]
        whys = [why(r"multiple drivers include investor demand and bank constraints; direct lenders, "
                    r"funds and listed business development companies (BDCs), took the mid-sized borrowers. The IMF "
                    r"put assets plus undeployed committed capital at about \$2.1 trillion in 2023"),
                why(r"limited trading: many loans are valued periodically by a model or an appraiser, as a Level 3 fair "
                    r"value, and the marks move slowly")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Private credit grew through several forces, including investor demand, bank constraints and changes in lending. It is not explained by one capital formula alone. The IMF's April twenty twenty-four report puts global private-credit assets plus undeployed committed capital at about two point one trillion dollars in twenty twenty-three. That is not simply outstanding loans. <bookmark mark='a'/> Many loans are illiquid and valued using models, appraisals or limited observable transactions. Floating-rate and senior-secured structures are common, but not universal. Reported marks can move less often than traded prices, and valuation frequency must not be confused with economic safety. The following listed BDC comparison is a window into reported values, with important balance-sheet differences."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.add(illustration(r"IMF, \textit{Global Financial Stability Report}, April 2024, chapter 2"))
        self.wait(0.4)
        self.clear_scene()

    def marks(self, b):
        t, p = np.asarray(b["t"]), np.asarray(b["price"])
        nt, nav = np.asarray(b["nav_t"]), np.asarray(b["nav"])
        g = axes([2018, 2026], [6, 24], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"\$ per share",
                 xticks=[2018, 2020, 2022, 2024, 2026], yticks=[8, 12, 16, 20, 24], font_size=14).to_edge(LEFT, buff=0.5
                                                                                                      ).shift(DOWN * 0.3)
        ax = g.ax
        lp = curve(ax, t, p, EQUITY, stroke_width=2)
        stairs = VMobject().set_points_as_corners([ax.c2p(a, c_) for a, c_ in zip(np.repeat(nt, 2)[1:],
                                                                                  np.repeat(nav, 2)[:-1])])
        stairs.set_stroke(DEBT, 3.5)
        lo = b["low"]
        dot = Dot(ax.c2p(2020 + 2.7 / 12, lo["v"]), color=BAD)
        drop_nav = b["nav_mar2020"] / b["nav_dec2019"] - 1
        drop_px = lo["v"] / b["nav_dec2019"] - 1
        side = VGroup(
            legend([(EQUITY, r"share price (daily)"), (DEBT, r"reported net asset value per share")], font_size=17),
            MathTex(rf"\text{{23 March 2020: price }} \${lo['v']:.2f}", font_size=24, color=BAD),
            MathTex(rf"\text{{NAV: }} \${b['nav_dec2019']:.2f} \to \${b['nav_mar2020']:.2f}\ ({100 * drop_nav:+.0f}\%)",
                    font_size=24, color=DEBT),
            wrapped_label(r"Share price and reported net assets are different claims and observation clocks. "
                          r"Quarter-end NAV is published later. Neither series identifies executable loan value.",3.6,19,GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Ares Capital is a listed business development company. Its reported NAV per share is net assets attributable to equity, including liabilities and other balance-sheet items; it is not simply loan value per share. The quarterly values are plotted at period ends, even though publication follows later. <bookmark mark='a'/> The saved low share price is {lo['v']:.2f} dollars, {abs(100 * drop_px):.0f} percent below the December twenty nineteen NAV used here as a comparison. That is not a contemporaneous executable loan discount. <bookmark mark='b'/> The March reported NAV changed by {100 * drop_nav:+.0f} percent from December. Share prices reflect leverage, future income, fees, liquidity and discount rates as well as underlying assets. Neither series alone establishes the true liquidation value of the loans or proves that one price was wrong."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), Create(lp), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(dot, scale=1.5), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(stairs), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
        self.add(illustration(r"Yahoo Finance closes (ARCC); NetAssetValuePerShare from Ares Capital's XBRL filings on "
                              r"EDGAR"))
        self.wait(0.4)
        self.clear_scene()

    def smoothing(self, gl):
        rows = [cmath(r"r^{\text{reported}}_t", r"=", r"\theta_0 r_t + \theta_1 r_{t-1} + \theta_2 r_{t-2},\ \ \sum\theta = 1",
                      font_size=36, colors={r"r^{\text{reported}}_t": DEBT}),
                cmath(r"\sigma^{\text{reported}}", r"=", r"\sigma\sqrt{\theta_0^2 + \theta_1^2 + \theta_2^2} < \sigma",
                      font_size=36, colors={r"\sigma^{\text{reported}}": BAD})]
        whys = [why(r"Getmansky, Lo and Makarov (2004), for hedge funds: marks that spread each true return over "
                    r"several quarters"),
                why(r"iid latent returns: volatility is reduced; naive Sharpe can rise; with "
                    r"$\theta = (0.5, 0.3, 0.2)$ volatility appears 38\% lower than it is. Under the stated iid latent-return assumptions, smoothing is a "
                    r"reporting mechanism, not proof of lower economic risk")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        foot = wrapped_label(rf"Ares Capital, {gl['n']} quarters: reported NAV per share moved with a volatility of "
                             rf"{100 * gl['vol_nav']:.1f}\% a year, its shares {100 * gl['vol_px']:.1f}\%; the worst "
                             rf"quarter was {100 * gl['worst_nav']:.1f}\% for the NAV and {100 * gl['worst_px']:.1f}\% "
                             r"for the shares. NAV and price changes exclude distributions; different claims and timing", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Getmansky, Lo and Makarov study a model in which reported returns average current and lagged latent returns. <bookmark mark='a'/> With independent identically distributed latent innovations and weights one half, point three and point two, reported volatility is the square root of point three eight times latent volatility, about thirty-eight percent lower. Autocorrelated latent returns add covariance terms, so that reduction is conditional. Mean-preserving smoothing can inflate a naive Sharpe ratio when it reduces the measured volatility. <bookmark mark='b'/> For this saved BDC sample, quarterly percentage changes in NAV and unadjusted share price have annualized standard deviations {100 * gl['vol_nav']:.1f} and {100 * gl['vol_px']:.1f} percent. These exclude distributions and are not total-return estimates. Leverage, fees, discount-rate changes, valuation timing and sampling also differ. Their volatility gap cannot identify the latent volatility of the same underlying loans or uniquely estimate appraisal smoothing."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        q = ask(r"a private credit fund reports volatility of 3\% a year and a Sharpe ratio of 2. What would you ask "
                r"for before believing either?")
        with self.voiceover("A private credit fund reports three percent volatility and a Sharpe ratio of two. What "
                            "would you ask for before believing either?"):
            self.play(FadeOut(foot), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: audit the return and valuation process', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('Ask for cash flows, distributions, fees, leverage, valuation timing, serial dependence, missing defaults and executable exits before interpreting volatility or Sharpe.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('Ask how returns include cash flows, distributions, fees and leverage. Inspect valuation methods, update dates, serial correlation, default handling and independent marks. Examine stressed exits and comparable executable prices. A small reported standard deviation and a high naive Sharpe ratio do not establish economic safety or identify how much smoothing occurred.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
