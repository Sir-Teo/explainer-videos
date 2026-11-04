from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class Shiller(VoiceoverScene):
    def construct(self):
        s = load("shiller")
        self.card()
        self.pstar()
        self.chart(s)
        self.identity()
        self.split(s)
        self.meaning()

    def card(self):
        c = chapter_card(8, r"Prices move too much", r"Can news about dividends explain the stock market's swings?",
                         lit=(1981,), part=PART)
        with self.voiceover("Chapter eight. Robert Shiller's question: do stock prices move too much to be explained by "
                            "news about dividends?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pstar(self):
        rows = [cmath(r"p_t", r"=", r"\mathbb{E}_t\big[p^*_t\big],\quad p^*_t = \textstyle\sum_{k\ge1}\frac{D_{t+k}}{(1+r)^k}",
                      font_size=38, colors={r"p_t": MKT}),
                cmath(r"\text{var}(p^*)", r"=", r"\text{var}(p) + \text{var}(p^* - p)\ \ \Rightarrow\ \ \sigma(p) \le \sigma(p^*)",
                      font_size=36, colors={r"\text{var}(p^*)": BAD})]
        whys = [why(r"if prices are expected discounted dividends at a constant rate, the price is the market's forecast of "
                    r"$p^*$, the 'ex post rational' price: what the dividends that actually came were worth"),
                why(r"a rational forecast's error is uncorrelated with the forecast, so the forecast must vary less than "
                    r"the thing forecast: prices should be smoother than $p^*$ (Shiller, 1981; LeRoy and Porter, 1981)")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Suppose a stock is worth its expected dividends, discounted at a constant rate. Then today's price is the "
            "market's forecast of something we can compute after the fact: the present value of the dividends that "
            "actually arrived, which Shiller called the ex post rational price, p star. <bookmark mark='a'/> A rational "
            "forecast's error is uncorrelated with the forecast itself, so the variance of p star is the variance of the "
            "price plus the variance of the error. Prices must therefore be smoother than p star. A forecast can never "
            "be more volatile than the thing it forecasts."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def chart(self, s):
        y, p, ps = np.asarray(s["years"]), np.asarray(s["p"]), np.asarray(s["pstar"])
        g = axes([1870, 2024], [0, 3.0], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"real price, detrended",
                 xticks=[1880, 1920, 1960, 2000], yticks=[0, 1, 2, 3], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lp = curve(ax, y, np.minimum(p, 3.0), MKT, stroke_width=2.6)
        lps = curve(ax, y, ps, TAN, stroke_width=3)
        side = VGroup(
            legend([(MKT, r"the S\&P composite, $p$"), (TAN, r"the ex post rational price, $p^*$")], font_size=17),
            MathTex(rf"\sigma(p) = {s['sd_p']:.2f},\ \ \sigma(p^*) = {s['sd_pstar']:.2f}", font_size=26, color=BAD),
            wrapped_label(rf"Shiller's data, January each year, 1871--2022, real; both divided by the price's exponential "
                          rf"trend ({100 * s['growth']:.1f}\% a year), $p^*$ discounted at the average real return, "
                          rf"{100 * s['rbar']:.1f}\%. The price swings far more than the dividends it forecasts", 3.6, 16,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is Shiller's picture, updated, on the data Shiller publishes, since 1871, adjusted for inflation and for the "
            "market's long-run growth. <bookmark mark='a'/> The present value of the dividends that were actually paid "
            "is a smooth, slow line: dividends simply did not vary much. <bookmark mark='b'/> The price swings around "
            "it, through the boom of the 1920s, the slump of the 1970s, the bubble of the late 1990s. Its standard "
            f"deviation is {s['sd_p']:.2f} against {s['sd_pstar']:.2f} for p star. If prices were rational forecasts of "
            "dividends at a constant discount rate, that could not happen."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lps), run_time=2)
            vo.wait_until("b")
            self.play(Create(lp), FadeIn(side[1]), FadeIn(side[2]), run_time=2.5)
        self.add(illustration(r"Robert Shiller's online data (ie\_data)"))
        self.wait(0.4)
        self.clear_scene()

    def identity(self):
        rows = [cmath(r"r_{t+1}", r"\approx", r"\kappa + \rho\,pd_{t+1} + \Delta d_{t+1} - pd_t", font_size=40),
                cmath(r"dp_t", r"\approx", r"\textstyle\sum_{j\ge0}\rho^j\,r_{t+1+j} - \sum_{j\ge0}\rho^j\,\Delta d_{t+1+j} + "
                      r"\text{const}", font_size=36, colors={r"dp_t": MKT}),
                cmath(r"\text{var}(dp)", r"\approx", r"\text{cov}\big(dp, \textstyle\sum\rho^j r\big) - "
                      r"\text{cov}\big(dp, \textstyle\sum\rho^j\Delta d\big)", font_size=34)]
        whys = [why(r"Campbell and Shiller (1988): log-linearise the return around the average price--dividend ratio, "
                    r"$\rho = 1/(1 + e^{\overline{dp}})$"),
                why(r"iterate forward: a high dividend yield must mean either high future returns or low future dividend "
                    r"growth. It is an identity, true of any price"),
                why(r"so the dividend yield's variance splits exactly into the two: how much of its movement is news "
                    r"about returns, how much about dividends")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "John Campbell and Shiller turned the observation into an identity. Write the log return in terms of the "
            "price-dividend ratio, and linearise around its average. <bookmark mark='a'/> Iterate forward, and the "
            "dividend yield today equals discounted future returns minus discounted future dividend growth. That is not "
            "a model; it is accounting, true of any asset. <bookmark mark='b'/> So the dividend yield's variance must "
            "split exactly into two parts: news about future returns, and news about future dividends."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def split(self, s):
        cs = s["cs"]
        tot = cs["b_r"] - cs["b_d"]
        share_r, share_d = cs["b_r"] / tot, -cs["b_d"] / tot
        g = axes([-0.6, 1.6], [-0.2, 1.1], x_length=6.0, y_length=4.2, xlabel=r"", ylabel=r"share of the dividend yield's "
                 r"variance", xticks=[], yticks=[0, 0.5, 1.0], font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (v, c_, nm) in enumerate(((share_r, MKT, r"future returns"), (share_d, CONS, r"future dividends"))):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.8, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=c_,
                                      fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]),
                            MathTex(f"{100 * v:.0f}\\%", font_size=26).next_to(ax.c2p(i, max(v, 0)), UP, buff=0.1),
                            label(nm, font_size=17).next_to(ax.c2p(i, -0.2), DOWN, buff=0.1)))
        side = VGroup(
            MathTex(rf"b_r = {cs['b_r']:.2f},\ \ b_d = {cs['b_d']:.2f},\ \ \rho = {cs['rho']:.3f}", font_size=24),
            wrapped_label(r"annual, 1871--2022: regressions of 15 years of discounted future returns and dividend growth on "
                          r"today's log dividend yield. The truncation leaves part in the yield 15 years ahead; of what is "
                          r"explained, almost all is returns. A high yield forecasts high returns, not falling dividends",
                          3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Measure the split on Shiller's century and a half of data. <bookmark mark='a'/> Of the part explained over "
            f"fifteen years, about {100 * share_r:.0f} percent of the dividend yield's movement is news about future "
            "returns. <bookmark mark='b'/> News about dividends explains almost none, and with the wrong sign. When "
            "stock prices are high relative to dividends, it is not because dividends are about to rise. It is because "
            "future returns are about to be low. John Cochrane put it simply in a presidential address to the American Finance Association: discount "
            "rates, not cash flows, drive prices."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def meaning(self):
        cards = VGroup(
            desk_question(r"two readings", r"either the discount rate varies a lot, rationally, as habit models predict "
                          r"(chapter 7), or investors' expectations swing too far, as Shiller argued: the evidence is the "
                          r"same, the interpretations opposite", width=12.0, font_size=21),
            desk_question(r"the Nobel of 2013", r"Fama, Hansen and Shiller shared it: one for efficiency, one for the "
                          r"tools, one for excess volatility. All three agree that long-horizon returns are predictable",
                          width=12.0, font_size=21),
            desk_question(r"for a forecaster", r"the predictability is real at horizons of years, weak at months, and "
                          r"fragile out of sample (Part 6's Welch and Goyal): enough to set expectations, rarely enough "
                          r"to time the market", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "What does it mean? <bookmark mark='a'/> Either discount rates really do vary a great deal, because "
            "investors' appetite for risk rises and falls, as the habit model of the last chapter predicts; or "
            "investors' expectations swing too far, as Shiller himself argued. The evidence is the same; the readings "
            "are opposite. <bookmark mark='b'/> In 2013 the Nobel committee gave the prize to Eugene Fama, Lars Hansen "
            "and Robert Shiller together. <bookmark mark='c'/> For a forecaster the practical point is narrower: "
            "returns are predictable over years, barely over months, and fragile out of sample, as Part six found."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"the market's dividend yield is at a record low. By Campbell--Shiller, what must happen next, and which "
                r"of the two would you bet on?")
        with self.voiceover("The market's dividend yield is at a record low. By the Campbell-Shiller identity, what must "
                            "happen next, and which of the two would you bet on?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
