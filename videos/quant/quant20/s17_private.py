from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, DEBT, EQUITY, PART, RISKY, ask, fit_right, illustration, load


class Private(VoiceoverScene):
    def construct(self):
        b = load("bdc")
        self.card()
        self.growth()
        self.marks(b)
        self.smoothing()

    def card(self):
        c = chapter_card(16, r"Private credit and its marks", r"What is a loan worth that never trades?", part=PART)
        with self.voiceover("Chapter sixteen. Private credit: loans that never trade, and how they are valued."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def growth(self):
        rows = [cmath(r"\text{lender}", r"=", r"\text{a fund or BDC, not a bank}", font_size=38, colors={r"\text{lender}": DEBT}),
                cmath(r"\text{loan}", r"=", r"\text{floating rate, senior secured, held to maturity, marked by model}",
                      font_size=32, colors={r"\text{loan}": RISKY})]
        whys = [why(r"after 2008, capital rules (chapter 10) made banks' leveraged loans expensive; direct lenders, "
                    r"funds and listed business development companies (BDCs), took the mid-sized borrowers. The IMF "
                    r"put the asset class at about \$2.1 trillion in 2023"),
                why(r"no market price: each loan is valued quarterly by a model or an appraiser, as a Level 3 fair "
                    r"value, and the marks move slowly")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "After 2008, the capital rules of chapter ten made it expensive for banks to hold loans to mid-sized, "
            "indebted companies. Funds stepped in, lending directly, floating rate and senior secured, and holding "
            "the loans to maturity. The International Monetary Fund estimated the market at about two point one "
            "trillion dollars in 2023. <bookmark mark='a'/> These loans have no market price. Each quarter they are "
            "valued by a model or an appraiser, and the values move slowly. What does that hide?"
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
            wrapped_label(rf"the market priced the same loans {abs(100 * drop_px):.0f}\% below the last reported value "
                          r"on its worst day; the quarter's marks moved by a few percent. Both recovered", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Some private lenders are listed, which gives one rare window. Ares Capital, the largest business "
            "development company, reports the value of its loans per share every quarter, and its shares trade every "
            "day. <bookmark mark='a'/> In March 2020 the shares fell to "
            f"{lo['v']:.2f} dollars, {abs(100 * drop_px):.0f} percent below the last reported value of the loans. "
            f"<bookmark mark='b'/> The quarter's reported value fell by {abs(100 * drop_nav):.0f} percent. Both "
            "recovered. Which was the better estimate of what the loans were worth that week? The market's included a "
            "panic; the marks included almost no information at all."
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

    def smoothing(self):
        rows = [cmath(r"r^{\text{reported}}_t", r"=", r"\theta_0 r_t + \theta_1 r_{t-1} + \theta_2 r_{t-2},\ \ \sum\theta = 1",
                      font_size=36, colors={r"r^{\text{reported}}_t": DEBT}),
                cmath(r"\sigma^{\text{reported}}", r"=", r"\sigma\sqrt{\theta_0^2 + \theta_1^2 + \theta_2^2} < \sigma",
                      font_size=36, colors={r"\sigma^{\text{reported}}": BAD})]
        whys = [why(r"Getmansky, Lo and Makarov (2004), for hedge funds: marks that spread each true return over "
                    r"several quarters"),
                why(r"the reported volatility and correlation are too low, and the Sharpe ratio too high; with "
                    r"$\theta = (0.5, 0.3, 0.2)$ volatility appears 38\% lower than it is. Smooth marks are a "
                    r"risk-reporting choice, not a property of the loans")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "There is a formal way to say what smooth marks do. Mila Getmansky, Andrew Lo and Igor Makarov modelled "
            "reported returns as a weighted average of the true returns of the last few quarters. "
            "<bookmark mark='a'/> Averaging lowers the volatility you see, and the correlation with markets, and "
            "raises the Sharpe ratio. With half the move reported now, three tenths next quarter and the rest after, "
            "the volatility appears thirty-eight percent lower than it is. The loans are no safer; their risk is "
            "reported later."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"a private credit fund reports volatility of 3\% a year and a Sharpe ratio of 2. What would you ask "
                r"for before believing either?")
        with self.voiceover("A private credit fund reports three percent volatility and a Sharpe ratio of two. What "
                            "would you ask for before believing either?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
