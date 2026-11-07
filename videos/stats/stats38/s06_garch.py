from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Volatility(VoiceoverScene):
    def construct(self):
        self.card()
        self.returns()
        self.facts()
        self.model()
        self.fit()
        self.forecast_vol()
        self.var_()
        self.lesson()

    def card(self):
        card = chapter_card(5, r"Volatility", r"When the variance has a memory", lit=(1963, 1982, 1986), part=PART)
        with self.voiceover("Chapter five. Volatility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def returns(self):
        d = load("garch")
        r = np.asarray(d["r"], float)
        p = np.asarray(d["price"], float)
        n = len(r)
        A = axes([0, n + 1], [1000, 6500], x_length=10.4, y_length=1.8, xlabel=r"", ylabel=r"DAX", xticks=[], yticks=[2000, 5000],
                 center=[0, 1.9, 0])
        B = axes([0, n], [-10, 8], x_length=10.4, y_length=2.6, xlabel=r"trading day, \ July 1991 -- August 1998",
                 ylabel=r"daily return (\%)", xticks=[], yticks=[-8, -4, 0, 4], center=[0, -1.0, 0])
        cp = series_line(A.ax, np.arange(n + 1), p, GREY_A, 1.8)
        cr = series_line(B.ax, np.arange(n), r, VOLC, 1.2)
        i = int(np.argmin(r))
        mark = VGroup(Dot(B.ax.c2p(i, r[i]), radius=0.08, color=TAUC),
                      label(rf"August 1991: \ {r[i]:.1f}\%", font_size=20, color=TAUC).next_to(B.ax.c2p(i, r[i]), RIGHT, buff=0.2))
        with self.voiceover(
            "<bookmark mark='a'/> The German stock index, the DAX, at every close from July 1991 to August 1998. <bookmark "
            "mark='b'/> Its daily returns, in percent. They hover around zero with no visible pattern in their signs. But "
            "the size of the moves comes in clusters: calm months, then turbulent ones, as in late 1997 and the summer of "
            "1998. <bookmark mark='c'/> The largest fall, almost ten percent in a day, came in August 1991, with the "
            "attempted coup in Moscow."
        ) as vo:
            self.add(dax_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cp), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(B), Create(cr), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(mark))
        self.clear_scene()

    def facts(self):
        d = load("garch")
        lags = np.arange(1, 31)
        A = axes([0, 31], [-0.1, 0.35], x_length=7.6, y_length=4.0, xlabel=r"lag (days)", ylabel=r"autocorrelation",
                 xticks=[1, 10, 20, 30], yticks=[0, 0.1, 0.2, 0.3], yfmt=lambda v: f"{v:g}", center=[-1.8, 0.2, 0])
        ax = A.ax
        r1 = np.asarray(d["acf_r"], float)[1:]
        r2 = np.asarray(d["acf_abs"], float)[1:]
        b1 = VGroup(*[Line(ax.c2p(k - 0.15, 0), ax.c2p(k - 0.15, v), color=GREY_A, stroke_width=4) for k, v in zip(lags, r1)])
        b2 = VGroup(*[Line(ax.c2p(k + 0.15, 0), ax.c2p(k + 0.15, v), color=VOLC, stroke_width=4) for k, v in zip(lags, r2)])
        ci = 1.96 / np.sqrt(d["n"])
        band = Rectangle(width=ax.c2p(31, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, ci)[1] - ax.c2p(0, -ci)[1], stroke_width=0,
                         fill_color=GREY_C, fill_opacity=0.25).move_to(ax.c2p(15.5, 0))
        side = fit_rows(VGroup(
            label(r"grey: \ ACF of returns: little linear dependence", font_size=22, color=GREY_A),
            label(r"red: \ ACF of $|r_t|$: \ positive for weeks", font_size=22, color=VOLC),
            label(rf"kurtosis {d['kurt']:.1f} \ (normal: 3): \ heavy tails", font_size=22, color=TAUC),
            label(rf"Engle's ARCH test: \ LM = {d['lm']['LM']:.0f}, \ $p \approx 10^{{-13}}$", font_size=22, color=MISSC),
            label(r"Mandelbrot (1963): \ cotton prices, \ the same facts", font_size=22, color=GREY_A),
        ), 3.8, 0.38, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The autocorrelations of the returns, in grey, are inside the band of noise: this "
            "plot shows little linear predictability in returns; it does not rule out every form of predictability. "
            "<bookmark mark='b'/> But the autocorrelations of their absolute sizes, in red, are positive for weeks: a"
            " big move, of either sign, predicts more big moves. <bookmark mark='c'/> The returns' kurtosis is " + say(d["kurt"], 1) + ", three times the normal's: extreme days are far more common than a "
            "normal distribution allows. <bookmark mark='d'/> Robert Engle's test for this clustering, regressing squared "
            "returns on their own lags, rejects decisively. <bookmark mark='e'/> Benoit Mandelbrot had described the same "
            "facts in cotton prices in 1963: these are the stylized facts of financial returns."
        ) as vo:
            self.add(dax_tag())
            self.play(FadeIn(A), FadeIn(band))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(side[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 2]))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"r_t", r"=", r"\mu + \sigma_t z_t, \quad z_t \sim \text{i.i.d.}(0, 1)", font_size=32),
            cmath(r"\text{ARCH}(q)", r":", r"\sigma_t^2 = \omega + \textstyle\sum_{j=1}^q \alpha_j \varepsilon_{t-j}^2", font_size=30),
            cmath(r"\text{GARCH}(1,1)", r":", r"\sigma_t^2 = \omega + \alpha\, \varepsilon_{t-1}^2 + \beta\, \sigma_{t-1}^2", font_size=30),
            cmath(r"\alpha + \beta < 1", r":", r"E\,\sigma_t^2 = \omega / (1 - \alpha - \beta); \ \text{shocks to variance decay at rate } \alpha + \beta", font_size=28),
        ]
        rows[2][-1].set_color(VOLC)
        whys = [why(r"signs unpredictable, \ sizes not"), why(r"Engle (1982): \ UK inflation"), why(r"Bollerslev (1986)"),
                why(r"persistence")]
        with self.voiceover(
            "<bookmark mark='a'/> The model writes each return as a mean plus a standard deviation that changes over "
            "time, times an independent shock. <bookmark mark='b'/> Engle's autoregressive conditional "
            "heteroskedasticity, ARCH, of 1982, made today's variance a weighted sum of recent squared shocks. He "
            "applied it to inflation in the United Kingdom. <bookmark mark='c'/> His student Tim Bollerslev's "
            "generalization of 1986, GARCH, adds yesterday's variance itself, so that one extra parameter gives a "
            "long, geometrically decaying memory. <bookmark mark='d'/> With positive omega, nonnegative coefficients "
            "and alpha plus beta below one, the stationary return process has a finite unconditional second moment. "
            "Its conditional variance forecasts revert at rate alpha plus beta per day; stationarity of the variance "
            "process in a stronger moment sense can require more."
        ) as vo:
            intro=label('GARCH predicts conditional scale with persistent variance dynamics',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fit(self):
        d = load("garch")
        r, s = np.asarray(d["r"], float), np.asarray(d["s"], float)
        n = len(r)
        A = axes([0, n], [-10, 8], x_length=10.4, y_length=3.6, xlabel=r"trading day", ylabel=r"return (\%)", xticks=[],
                 yticks=[-8, -4, 0, 4], center=[0, 0.6, 0])
        cr = series_line(A.ax, np.arange(n), r, GREY_C, 1.0)
        up = series_line(A.ax, np.arange(n), 2 * s, VOLC, 2.2)
        dn = series_line(A.ax, np.arange(n), -2 * s, VOLC, 2.2)
        foot = fit_rows(VGroup(
            label(rf"GARCH(1,1) by maximum likelihood: \ $\omega$ = {d['omega']:.3f}, \ $\alpha$ = {d['alpha']:.3f}, \ $\beta$ = {d['beta']:.3f}", font_size=24, color=VOLC),
            label(rf"persistence $\alpha + \beta$ = {d['persistence']:.3f}: \ a volatility shock halves in {d['half_life']:.0f} trading days", font_size=24, color=TAUC),
        ), 12.4, 0.3, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fitted to the DAX by maximum likelihood: alpha " + say(d["alpha"], 3) + ", beta "
            + say(d["beta"], 3) + ". <bookmark mark='b'/> The red band is plus and minus two conditional standard "
            "deviations. It widens in the storms and narrows in the calms, following the returns. <bookmark mark='c'/> "
            "Alpha plus beta is " + say(d["persistence"], 3) + ": a burst of volatility halves in about "
            + str(round(d["half_life"])) + " trading days, three weeks. Values this close to one are typical of daily "
            "financial data."
        ) as vo:
            self.add(dax_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cr), FadeIn(foot[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(up), Create(dn), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def var_(self):
        d = load("garch")
        rows = [[r"1\% value-at-risk rule", r"all days", r"calm half", r"turbulent half"],
                [r"constant variance, \ normal", f"{100 * d['exc_const']:.2f}\\%", f"{100 * d['exc_const_lo']:.2f}\\%", f"{100 * d['exc_const_hi']:.2f}\\%"],
                [r"GARCH variance, \ normal", f"{100 * d['exc_garch']:.2f}\\%", f"{100 * d['exc_garch_lo']:.2f}\\%", f"{100 * d['exc_garch_hi']:.2f}\\%"]]
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.36, colors=[GREY_A, MISSC, BANDC]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"in-sample fitted diagnostic; a valid conditional 1\% rule has 1\% conditional breach risk", font_size=24, color=GREY_A),
            label(r"closer group rates do not establish calibrated or independent violations", font_size=24, color=TAUC),
        ), 12.4, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a retrospective diagnostic using parameters fitted to the whole record, not"
            " an out-of-sample backtest. A bank's one-day value at risk at one percent is the loss it should exceed "
            "on one day in a hundred. <bookmark mark='b'/> With a constant variance and a normal distribution, the "
            "DAX breaches it on " + say(100 * d["exc_const"], 1) + " percent of days overall, but on fewer than one in a hundred calm days and about three in a hundred "
            "turbulent ones: the breaches cluster, exactly when they hurt. <bookmark mark='c'/> With the fitted GARCH"
            " variance, the breach rates in these two volatility groups are closer. Equal group rates alone do not "
            "establish independent violations. <bookmark mark='d'/> Both still exceed one percent overall, consistent"
            " with heavier standardized tails and possible model misspecification relative to the normal. Student t "
            "innovations or empirical residual quantiles may help, but need fresh validation; robust location methods"
            " alone do not guarantee accurate tail risk."
        ) as vo:
            self.add(dax_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"uncorrelated is not independent: \ the variance is forecastable", font_size=26, color=VOLC),
            label(r"descendants: \ EGARCH (leverage), \ stochastic volatility, \ realized volatility from intraday data", font_size=26),
            label(r"stochastic volatility: \ the variance as a hidden state \ (chapter 9's particle filters)", font_size=26, color=STATEC),
            label(r"Engle's Nobel, \ 2003: \ ``for methods of analyzing economic time series with time-varying volatility''", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson is that uncorrelated is not independent: the sign of tomorrow's return is "
            "unpredictable, but its size is not. <bookmark mark='b'/> The family has grown: exponential GARCH lets falls "
            "raise volatility more than rises; stochastic volatility models; and realized volatility, measured from "
            "intraday prices. <bookmark mark='c'/> Stochastic volatility treats the variance as a hidden state, the subject "
            "of the filters in chapters seven to nine. <bookmark mark='d'/> Engle received the 2003 Nobel prize for methods "
            "of analyzing economic time series with time-varying volatility."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def forecast_vol(self):
        d = load("garch")
        rows = [
            cmath(r"\bar\sigma^2", r"=", rf"\omega / (1 - \alpha - \beta) = {d['uncond_sd'] ** 2:.2f} \ \text{{(sd {d['uncond_sd']:.2f}\%)}}", font_size=30),
            cmath(r"E_t\, \sigma_{t+h}^2", r"=", r"\bar\sigma^2 + (\alpha + \beta)^{h-1} (\sigma_{t+1}^2 - \bar\sigma^2)", font_size=30),
            cmath(r"\text{a month ahead}", r":", rf"(\alpha + \beta)^{{20}} = {d['persistence'] ** 20:.2f} \ \text{{of the one-day forecast excess remains}}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{volatility forecasts revert to the long-run level, \ geometrically}", font_size=30),
        ]
        rows[1][-1].set_color(VOLC)
        whys = [why(r"the long-run variance"), why(r"the term structure of volatility"), why(r"21 trading days"),
                why(r"options and risk limits use this")]
        with self.voiceover(
            "<bookmark mark='a'/> GARCH also forecasts. The long-run variance is omega over one minus alpha minus beta: for "
            "the DAX, a daily standard deviation of about " + say(d["uncond_sd"], 2) + " percent. <bookmark mark='b'/> The "
            "forecast of the variance h days ahead is the long-run level plus the current excess, shrunk by alpha plus beta "
            "for every day. <bookmark mark='c'/> A month of trading days ahead, " + say(d["persistence"] ** 20, 2) + " of "
            "the one-day variance forecast's excess over the long-run level remains at horizon twenty-one. <bookmark mark='d'/> So volatility forecasts revert, geometrically, "
            "to the long-run level: the term structure of volatility that option prices and risk limits are built on."
        ) as vo:
            intro=label('Variance forecasts revert toward a model-based long-run level',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
