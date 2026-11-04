from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAB, BAD, GOOD, MKT, PART, ask, fit_right, illustration, load


class LowRisk(VoiceoverScene):
    def construct(self):
        lr = load("lowrisk")
        self.card()
        self.recipe()
        self.results(lr)
        self.lowvol(lr)
        self.why()
        self.critique()

    def card(self):
        c = chapter_card(6, r"Low risk", r"Why do safe stocks earn as much as risky ones?", lit=(2014,), part=PART)
        with self.voiceover("Chapter six. The low-risk anomaly: Part twenty-three's flat line, turned into a factor."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def recipe(self):
        rows = [cmath(r"\tilde\beta_i", r"=", r"0.6\,\hat\rho_{im}\frac{\hat\sigma_i}{\hat\sigma_m} + 0.4 \cdot 1", font_size=40,
                      colors={r"\tilde\beta_i": BAB}),
                cmath(r"r^{BAB}_{t+1}", r"=", r"\frac{r^L_{t+1} - r^f}{\beta^L_t} - \frac{r^H_{t+1} - r^f}{\beta^H_t}",
                      font_size=42, colors={r"r^{BAB}_{t+1}": BAB})]
        whys = [why(r"Frazzini and Pedersen (2014): estimate betas with correlations from five years of data and "
                    r"volatilities from one, then shrink them toward one (Part 24's chapter 1 cousin of Vasicek)"),
                why(r"rank stocks by beta; a low-beta portfolio levered up to a beta of one, a high-beta one levered down "
                    r"to one; long the first, short the second. Market-neutral by construction, and long safe stocks")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Part twenty-three found the security market line too flat: low-beta stocks earn too much, high-beta ones "
            "too little. Andrea Frazzini and Lasse Pedersen made it a factor. Estimate each stock's beta, from "
            "correlations over five years and volatilities over one, and shrink it toward one. <bookmark mark='a'/> "
            "Then rank the stocks by beta, lever the low-beta half up to a beta of one and the high-beta half down to "
            "one, and go long the first and short the second. The result has no market exposure, and it holds safe "
            "stocks with leverage, which is exactly what constrained investors cannot do."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def results(self, lr):
        d = np.asarray(lr["bab_date"])
        t = d // 100 + (d % 100 - 0.5) / 12
        w = np.asarray(lr["bab_cum"], float)
        g = axes([1930, 2021], [-0.2, 4.0], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\$1 in 1930, $\log_{10}$",
                 xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, 1, 2, 3, 4], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, np.log10(w), BAB, stroke_width=2.6)
        us, gl = lr["bab_us"], lr["bab_global"]
        side = VGroup(
            MathTex(rf"\text{{US}},\ 1930\text{{--}}2020:\ {100 * us['mean']:.1f}\%,\ SR\ {us['sharpe']:.2f},\ t\ {us['t']:.1f}",
                    font_size=22, color=BAB),
            MathTex(rf"\text{{global}},\ {lr['bab_gl_start'] // 100}\text{{--}}2020:\ {100 * gl['mean']:.1f}\%,\ SR\ "
                    rf"{gl['sharpe']:.2f}", font_size=22, color=BAB),
            MathTex(rf"\text{{worst drawdown (US)}}:\ {100 * us['maxdd']:.0f}\%", font_size=22, color=BAD),
            wrapped_label(r"AQR's updated BAB factors, monthly, excess of cash. On these published versions, the strongest "
                          r"of the classic US stock factors in the research window", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "AQR publishes the factor for twenty-four countries. <bookmark mark='a'/> In the United States since 1930, "
            "betting against beta earned eight percent a year, with a Sharpe ratio of about seven tenths and a "
            "t-statistic near seven, the strongest of the classic American stock factors in this window. Globally since 1987, nine "
            "percent, with a Sharpe ratio of nine tenths. <bookmark mark='b'/> It is not riskless. The American "
            "version lost more than half its value at its worst."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.add(illustration(r"AQR data set: Betting Against Beta, Equity Factors, Monthly"))
        self.wait(0.4)
        self.clear_scene()

    def lowvol(self, lr):
        v = lr["var"]
        mean, vol, sr, be = (np.asarray(v[k]) for k in ("mean", "vol", "sharpe", "beta"))
        g = axes([0, 0.3], [0, 0.12], x_length=6.4, y_length=4.2, xlabel=r"volatility, a year",
                 ylabel=r"average excess return, a year", xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.04, 0.08, 0.12],
                 font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[VGroup(Dot(ax.c2p(a, b), radius=0.09, color=interpolate_color(ManimColor(GOOD), ManimColor(BAD),
                                                                                    i / 4)),
                               MathTex(rf"Q{i + 1}", font_size=18).next_to(ax.c2p(a, b), UR, buff=0.06))
                        for i, (a, b) in enumerate(zip(vol, mean))])
        cml = DashedLine(ax.c2p(0, 0), ax.c2p(0.3, 0.3 * sr[0]), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{Sharpe}}:\ {sr[0]:.2f}\ (\text{{lowest}})\ \to\ {sr[-1]:.2f}\ (\text{{highest}})", font_size=22),
            MathTex(rf"\beta:\ {be[0]:.2f}\ \to\ {be[-1]:.2f}", font_size=22),
            wrapped_label(r"five value-weighted portfolios sorted on each stock's past variance, 1963--2020. Average "
                          r"returns rise only slightly across the first four and collapse in the fifth, while volatility more "
                          r"than doubles. Ang, Hodrick, Xing and Zhang (2006) found the same for idiosyncratic volatility",
                          3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The same pattern appears with plain volatility. Sort stocks into five groups by how volatile they have "
            "been. <bookmark mark='a'/> Their average returns are about the same for the first four, seven to ten "
            "percent a year, and then drop to four for the most volatile fifth, while volatility rises from twelve "
            "percent to twenty-eight. The Sharpe ratio falls from almost six tenths to under two. Andrew Ang, Robert "
            "Hodrick, Yuhang Xing and Xiaoyan Zhang found the starkest version: stocks with high idiosyncratic "
            "volatility, risk that should not be priced at all, earn the least."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.3), Create(cml), FadeIn(side), run_time=2.5)
        self.add(illustration(r"Kenneth French's data library: portfolios formed on variance"))
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        cards = VGroup(
            desk_question(r"leverage constraints", r"Black (1972), Frazzini and Pedersen (2014): investors who cannot or "
                          r"will not borrow buy risky stocks for their return, bidding them up", width=12.0, font_size=20),
            desk_question(r"lottery preferences", r"Part 23's prospect theory: volatile, skewed stocks are overpriced "
                          r"lottery tickets (Bali, Cakici and Whitelaw, 2011: the 'MAX' effect)", width=12.0, font_size=20),
            desk_question(r"benchmarking", r"Baker, Bradley and Wurgler (2011): a manager judged against an index cannot "
                          r"lever safe stocks without tracking error, so high-beta stocks are the cheap way to beat it",
                          width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Three explanations, all about constraints or preferences, none about risk. <bookmark mark='a'/> Leverage: "
            "investors who cannot borrow buy risky stocks to reach for return, and bid them up. "
            "<bookmark mark='b'/> Lotteries: volatile stocks with a small chance of a huge gain are overpriced, the "
            "prospect theory of Part twenty-three. <bookmark mark='c'/> Benchmarks: a fund manager judged against an "
            "index cannot hold levered safe stocks without straying from it, so high-beta stocks become the easy way "
            "to try to beat it."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def critique(self):
        cards = VGroup(
            desk_question(r"how it is built matters", r"Novy-Marx and Velikov (2022): BAB's construction (rank weights, "
                          r"betas from different windows, leverage in the small and illiquid) drives much of its return; "
                          r"value-weighted, conventionally built versions earn much less", width=12.0, font_size=20),
            desk_question(r"costs and leverage", r"the strategy levers its long side about 1.5 times and holds many small "
                          r"stocks: its costs and funding are far from the factor's paper return (Part 26)", width=12.0,
                          font_size=20),
            desk_question(r"what the plain sort says", r"the variance-sorted portfolios above: low minus high earns only "
                          r"2.5\% a year raw ($t \approx 0.9$), but with half the beta; the anomaly is in risk-adjusted "
                          r"returns, so it needs leverage to harvest", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "And a critique worth taking seriously. <bookmark mark='a'/> Robert Novy-Marx and Mihail Velikov argued "
            "that betting against beta's published returns depend on details of its construction, rank weights, "
            "betas from mismatched windows, and leverage concentrated in small, illiquid stocks; built "
            "conventionally, it earns much less. <bookmark mark='b'/> Its costs and funding are far from the paper "
            "return. <bookmark mark='c'/> And the plain sort shows why: low-volatility stocks earn only a little more "
            "than high-volatility ones in raw terms; the anomaly is in risk-adjusted returns, and leverage is needed to "
            "collect it."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a pension fund that cannot borrow wants more return. Should it buy high-beta stocks, or low-beta stocks "
                r"and a little equity futures? What does the low-risk anomaly say about everyone else's choice?")
        with self.voiceover("A pension fund that cannot borrow wants more return. Should it buy high-beta stocks, or "
                            "low-beta stocks and some equity futures? And what does the low-risk anomaly say about "
                            "everyone else's choice?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
