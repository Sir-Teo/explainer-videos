from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, PART, UMD, ask, fit_right, illustration, load


class Timing(VoiceoverScene):
    def construct(self):
        t = load("timing")
        self.card()
        self.siren()
        self.spread(t)
        self.hks()
        self.fm_rule()
        self.fm_result(t)
        self.explains(t)
        self.lesson()

    def card(self):
        c = chapter_card(10, r"Factor timing and factor momentum", r"Can you tell when a factor will pay?", lit=(2022,),
                         part=PART)
        with self.voiceover("Chapter ten. Holding a factor through a lost decade is hard. Can one time it instead?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def siren(self):
        cards = VGroup(
            desk_question(r"by valuation", r"hold more of a factor when its stocks are unusually cheap relative to the "
                          r"other side: the value spread of chapter 8", width=12.0, font_size=20),
            desk_question(r"by its own past", r"hold more of a factor that has done well recently: factor momentum",
                          width=12.0, font_size=20),
            desk_question(r"the warning", r"Asness (2016), 'The siren song of factor timing': timing signals are weak, "
                          r"and each one is correlated with the factors you already hold, so a timed book is less "
                          r"diversified than it looks", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "There are two natural ways to time a factor. <bookmark mark='a'/> By valuation: hold more of it when its "
            "long side is unusually cheap relative to its short side. <bookmark mark='b'/> Or by its own past: hold "
            "more of a factor that has done well lately. <bookmark mark='c'/> Cliff Asness called it the siren song. "
            "The signals are weak, and timing value by its spread is, in effect, a second dose of value. A timed book "
            "is less diversified than it looks."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def spread(self, t):
        x, y = np.asarray(t["spread_x"]), np.asarray(t["hml_y"])
        c = np.polyfit(x, y, 1)
        g = axes([0.9, 2.8], [-0.5, 0.9], x_length=7.0, y_length=4.4, xlabel=r"value spread at the end of the year",
                 ylabel=r"HML over the next year", xticks=[1.0, 1.5, 2.0, 2.5], yticks=[-0.4, 0, 0.4, 0.8],
                 font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, min(max(b, -0.5), 0.9)), radius=0.05, color=HML, fill_opacity=0.8)
                        for a, b in zip(x, y)])
        xs = np.linspace(1.0, 2.7, 20)
        fit = curve(ax, xs, np.polyval(c, xs), WHITE, stroke_width=3)
        side = VGroup(
            MathTex(rf"\text{{slope}} = {t['slope']:.3f},\ t = {t['slope_t']:.1f},\ R^2 = {t['r2']:.2f}", font_size=22),
            MathTex(rf"\text{{at 2020's spread}}\ (2.40):\ {100 * np.polyval(c, 2.40):.0f}\%\ \text{{vs mean}}\ "
                    rf"{100 * y.mean():.0f}\%", font_size=22, color=HML),
            wrapped_label(r"one dot per year, 1927--2020: the spread in December against value's return in the following "
                          r"calendar year, Newey--West $t$. The slope has the expected sign and is weak: a wide spread "
                          r"tilts the odds, it does not set the date", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Test the first idea on value itself. Each December, the value spread; the following year, value's "
            "return. Ninety-three years. <bookmark mark='a'/> The slope is positive, as Part twenty-three's identity "
            "says it should be: a wider spread has been followed by better years for value. But the t-statistic is "
            "about one point eight and the R squared five percent. At the end of 2020 the fitted line pointed to a "
            "value return of about twelve percent for the coming year, three times the average. With an R squared of "
            "five percent, that is a tilt of the odds, not a forecast anyone should bet the firm on."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def hks(self):
        rows = [cmath(r"\mathbb{E}_t[f_{t+1}]", r"\approx", r"a + b\,\text{bm}^f_t", font_size=42,
                      colors={r"\mathbb{E}_t[f_{t+1}]": GOOD}),
                cmath(r"w_t", r"\propto", r"\Sigma^{-1}\,\mathbb{E}_t[f_{t+1}]", font_size=42)]
        whys = [why(r"Haddad, Kozak and Santosh (2020): forecast each of the main principal components of fifty anomaly "
                    r"portfolios by its own book-to-market spread, a few regressions instead of fifty"),
                why(r"then combine them mean--variance style, as Part 23 did for assets. They find the timed portfolio's "
                    r"Sharpe ratio well above the static one: the stochastic discount factor's volatility moves a lot")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A more disciplined version comes from Valentin Haddad, Serhiy Kozak and Shrihari Santosh. Instead of "
            "timing fifty anomalies one at a time, they take the few dominant principal components of the anomaly "
            "portfolios, Part twenty-three's APT again, and forecast each by its own valuation spread. "
            "<bookmark mark='a'/> Then they combine the forecasts with the covariance matrix, Markowitz style. They "
            "report a timed portfolio far better than the static one, and conclude that the discount factor's "
            "volatility, the Hansen-Jagannathan quantity, moves a great deal over time. The method keeps the number "
            "of forecasts small, which is the only defence against overfitting a weak signal."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def fm_rule(self):
        rows = [cmath(r"r^{TSFM}_{t+1}", r"=", r"\frac{1}{K}\textstyle\sum_k \text{sign}\Big(\prod_{j=0}^{11}(1 + f_{k,t-j}) - "
                      r"1\Big)\, f_{k,t+1}", font_size=38, colors={r"r^{TSFM}_{t+1}": UMD})]
        whys = [why(r"Ehsani and Linnainmaa (2022): time-series momentum applied to factors. Long each factor whose past "
                    r"year was positive, short each whose past year was negative. Here: SMB, HML, RMW, CMA, UMD and the "
                    r"short-term reversal factor, 1964--2020")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "The second idea: factor momentum. Sina Ehsani and Juhani Linnainmaa applied chapter three's time-series "
            "momentum to the factors themselves. Each month, hold every factor whose past year was positive, and short "
            "every factor whose past year was negative. Do it with six American factors, size, value, profitability, "
            "investment, momentum and short-term reversal, from 1964."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def fm_result(self, t):
        d = np.asarray(t["date"])
        tt = d // 100 + (d % 100 - 0.5) / 12
        g = axes([1964, 2021], [-0.05, 1.1], x_length=7.8, y_length=4.4, xlabel=r"year", ylabel=r"\$1 in 1964, $\log_{10}$",
                 xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 0.5, 1.0], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        l1 = curve(ax, tt, np.log10(np.asarray(t["cum_tsfm"])), UMD, stroke_width=2.6)
        l2 = curve(ax, tt, np.log10(np.asarray(t["cum_ew"])), GOOD, stroke_width=2.6)
        a, b = t["tsfm"], t["ew"]
        side = VGroup(
            legend([(UMD, r"factor momentum"), (GOOD, r"all six, equally, always")], font_size=16),
            MathTex(rf"SR:\ {a['sharpe']:.2f}\ (t = {a['t']:.1f})\ \text{{vs}}\ {b['sharpe']:.2f}", font_size=24),
            label(r"share of months each factor is held long:", font_size=15, color=GREY_A),
            MathTex(r",\ ".join(rf"\text{{{n}}}\ {s:.2f}" for n, s in zip(t["names"], t["long_share"])), font_size=17),
            wrapped_label(r"factor momentum works, with a $t$ above four; it is beaten by simply holding all six, because "
                          r"shorting a factor that lost last year gives up its premium and its diversification", 3.6, 15,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The result. <bookmark mark='a'/> Factor momentum works: a Sharpe ratio of about six tenths, a "
            "t-statistic above four. Factors do trend. <bookmark mark='b'/> But simply holding all six factors, all "
            "the time, in equal amounts, did far better here: a Sharpe ratio above one. Each factor is held long most "
            "of the time anyway, and every month factor momentum shorts one of them it gives up that factor's premium "
            "and its diversification. Timing is not free."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(side[2:]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def explains(self, t):
        a = t["umd_on_tsfm"]
        rows = [cmath(r"UMD_t", r"=", rf"\alpha + b\,TSFM_t + e_t:\quad \alpha = {100 * a['alpha']:.1f}\%\ (t = {a['t']:.1f}),"
                      rf"\ R^2 = {a['r2']:.2f}", font_size=36, colors={r"UMD_t": UMD})]
        whys = [why(r"Ehsani and Linnainmaa's claim: stock momentum is largely factor momentum. Stocks that went up last "
                    r"year are, disproportionately, stocks exposed to the factors that went up; once factor momentum is "
                    r"held, momentum in individual stocks adds little. Here, its alpha falls to an insignificant 1.9\%")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "And a surprising link. Regress the stock momentum factor on factor momentum. <bookmark mark='a'/> The "
            "alpha of stock momentum falls to about two percent a year, with a t of one: statistically, nothing left. "
            "Ehsani and Linnainmaa's reading is that stocks that rose last year are mostly stocks exposed to factors "
            "that rose last year. Momentum in individual stocks may be momentum in factors, seen one stock at a time."
        ) as vo:
            vo.wait_until("a")
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"signals are weak", r"an $R^2$ of a few percent a year: timing helps only when applied across "
                          r"many factors over many years, and costs eat a good part of it", width=12.0, font_size=20),
            desk_question(r"few forecasts, not many", r"time a handful of principal components, not every anomaly: the "
                          r"number of choices is the overfitting risk (Part 25)", width=12.0, font_size=20),
            desk_question(r"the default", r"hold a diversified set of factors steadily, and lean on timing at the "
                          r"margin", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "So: <bookmark mark='a'/> timing signals explain a few percent of a year's factor returns; they help only "
            "across many factors and many years, and trading costs take a share. <bookmark mark='b'/> Forecast a few "
            "combinations, not every anomaly, because every forecast is another chance to overfit. "
            "<bookmark mark='c'/> And make the default a diversified set of factors held steadily, with timing at the "
            "margin."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a factor-momentum rule would have sold value in 2019 and 2020, after two bad years. Was that a good rule "
                r"or bad luck, and how many years would you need to tell?")
        with self.voiceover("A factor-momentum rule would have sold value in 2019 and 2020, after two bad years. Was that "
                            "a good rule or bad luck, and how many years would you need to tell?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
