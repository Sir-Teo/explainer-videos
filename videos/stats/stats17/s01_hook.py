from __future__ import annotations

import numpy as np

from explainer.stats.kit import ts as T
from videos.stats.stats17.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.yule()
        self.series()
        self.differences()
        self.random_walks()
        self.pendulum()
        self.objectives()

    def yule(self):
        tl = timeline(lit=(1926,)).to_edge(UP, buff=0.35)
        hc = history_card(1926, r"G. Udny Yule, \ presidential address, \ Royal Statistical Society",
                          r"``Why do we sometimes get nonsense-correlations between time-series?'': \ two series that "
                          r"merely drift with time can correlate almost perfectly", color=SERIES, width=10.4, font_size=24
                          ).move_to([0, 1.1, 0])
        rows = fit_rows(VGroup(
            label(r"every method so far assumed independent observations", font_size=24),
            label(r"a time series remembers: \ this year looks like last year", font_size=24, color=RES),
            label(r"what goes wrong, \ and what to do instead", font_size=26, color=OBS),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In January 1926 George Udny Yule gave his presidential address to the Royal Statistical "
            "Society. His title was a question: why do we sometimes get nonsense correlations between time series? "
            "<bookmark mark='b'/> Every method in this course so far has assumed that the observations are independent, or at "
            "least exchangeable. <bookmark mark='c'/> A time series isn't like that. This year looks like last year; each "
            "observation remembers the one before. <bookmark mark='d'/> This part is about what goes wrong when we forget "
            "that, and what to do instead."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def series(self):
        d = load("yule")
        yrs = np.asarray(d["years"])
        m, c = np.asarray(d["mortality"]), np.asarray(d["marriages"])
        A = axes([1864, 1913], [13, 23], x_length=8.6, y_length=4.2, xlabel=r"year", ylabel=r"deaths per 1,000",
                 xticks=[1870, 1880, 1890, 1900, 1910], yticks=[14, 18, 22], center=[-1.6, 0.4, 0])
        ax = A.ax
        lm = series_line(ax, yrs, m, RES, 3)
        # marriages on a second scale: 58 .. 80 per 1,000 marriages mapped onto 13 .. 23
        lc = series_line(ax, yrs, 13 + (c - 58) * 10 / 22, S.CTRL, 3)
        right = VGroup(*[MathTex(f"{v}", font_size=20, color=S.CTRL).next_to(ax.c2p(1913, 13 + (v - 58) * 10 / 22), RIGHT, buff=0.1)
                         for v in (60, 70, 80)])
        rows = fit_rows(VGroup(
            label(r"standardized mortality, \ England and Wales", font_size=22, color=RES),
            label(r"Church of England marriages per 1,000 marriages \ (right scale)", font_size=22, color=S.CTRL),
            MathTex(rf"r = {d['r']:.4f}", font_size=34, color=OBS),
            label(r"Yule: \ 0.9512, \ from the original figures", font_size=20, color=GREY_A),
            label(r"do church weddings kill?", font_size=24, color=RES),
        ), 3.8, 0.36, [5.0, 0.4, 0])
        tag = historical_tag(r"Yule (1926), \ p.~3; \ Hipel \& McLeod", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> His first example. In red, the standardized death rate in England and Wales, every year from "
            "1866 to 1911. <bookmark mark='b'/> In blue, the share of marriages performed in the Church of England, per "
            "thousand marriages. <bookmark mark='c'/> The correlation is point nine five. <bookmark mark='d'/> Yule computed "
            "point nine five one two from the original figures. <bookmark mark='e'/> Taken at face value, the fewer church "
            "weddings, the fewer deaths. Nobody believes that, and Yule didn't. But he wanted to know why the correlation "
            "is so high, and whether a significance test would have warned us."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lm), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lc), FadeIn(right), FadeIn(rows[1]), run_time=2.0)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def differences(self):
        d = load("yule")
        m, c = np.asarray(d["mortality"]), np.asarray(d["marriages"])
        A = axes([58, 80], [13.5, 22.5], x_length=5.0, y_length=3.8, xlabel=r"C of E marriages", ylabel=r"mortality",
                 xticks=[60, 70, 80], yticks=[14, 18, 22], center=[-3.6, 0.4, 0], font_size=18)
        B = axes([-5, 5], [-0.6, 0.6], x_length=5.0, y_length=3.8, xlabel=r"change in marriages", ylabel=r"change in mortality",
                 xticks=[-4, 0, 4], yticks=[-0.4, 0, 0.4], center=[3.2, 0.4, 0], font_size=18)
        d1 = scatter(A.ax, c, m, radius=0.07)
        d2 = scatter(B.ax, np.diff(c), np.clip(np.diff(m), -0.58, 0.58), color=S.ALT, radius=0.07)
        ta = MathTex(rf"\text{{levels}}:\ r = {d['r']:.2f}", font_size=28, color=OBS).next_to(A, UP, buff=0.15)
        tb = MathTex(rf"\text{{year-on-year changes}}:\ r = {d['r_diff']:.2f}", font_size=28, color=S.ALT).next_to(B, UP, buff=0.15)
        foot = fit_rows(VGroup(
            label(r"both series drift down with time: \ the correlation is between two trends", font_size=24),
            label(r"the 46 years are not 46 independent observations", font_size=24, color=RES),
        ), 12.4, 0.25, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Plotted against each other, the forty-six years lie almost on a line. <bookmark mark='b'/> "
            "But look at the changes from one year to the next. If marriages and deaths were linked, a year with an unusual "
            "drop in church weddings should bring an unusual drop in deaths. The correlation of the changes is point oh two: "
            "nothing. <bookmark mark='c'/> Both series simply drift downward over the half-century, for unrelated reasons, and "
            "any two drifting series will line up. <bookmark mark='d'/> The forty-six years aren't forty-six independent "
            "observations. They're closer to one observation each of two trends."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(d1), FadeIn(ta))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(d2), FadeIn(tb))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def random_walks(self):
        d = load("yule")
        rw, wn = np.asarray(d["rw_r"]), np.asarray(d["wn_r"])
        e = np.linspace(-1, 1, 41)
        A = axes([-1, 1], [0, 0.14], x_length=7.6, y_length=3.6, xlabel=r"correlation of two independent series of 46",
                 ylabel=r"share", xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 0.05, 0.1], center=[-2.0, 0.5, 0])
        ax = A.ax
        hw = hist_bars(ax, e, np.histogram(wn, e)[0] / len(wn), color=GREY_B, opacity=0.55)
        hr = hist_bars(ax, e, np.histogram(rw, e)[0] / len(rw), color=RES, opacity=0.75)
        pair = np.asarray(d["pair"])
        B = axes([0, 46], [-18, 2], x_length=3.4, y_length=2.0, xlabel=r"", ylabel=r"", center=[4.6, 2.0, 0])
        p1 = series_line(B.ax, np.arange(46), pair[0], S.CTRL, 2)
        p2 = series_line(B.ax, np.arange(46), pair[1], RES, 2)
        pl = MathTex(rf"r = {d['pair_r']:.2f}", font_size=24).next_to(B, DOWN, buff=0.1)
        rows = fit_rows(VGroup(
            label(r"independent noise: \ $|r| > 0.5$ in 0.04\%", font_size=22, color=GREY_A),
            label(rf"independent random walks: \ $|r| > 0.5$ in {100 * d['rw_big']:.0f}\%", font_size=22, color=RES),
            label(r"Yule did this with cards and dice", font_size=20, color=GREY_B),
        ), 4.2, 0.34, [4.6, -1.2, 0])
        tag = simulated_tag(r"20,000 pairs each", corner=DR)
        with self.voiceover(
            "Yule then did an experiment, by hand, with shuffled cards. <bookmark mark='a'/> Take two series of forty-six "
            "independent random numbers, unrelated to each other, and correlate them. Twenty thousand pairs: the correlations "
            "cluster near zero, and beyond plus or minus a half only four times in ten thousand. <bookmark mark='b'/> Now "
            "make each series a random walk, each step adding a fresh random number to the last value, like a drunkard's "
            "path. Here's one pair. <bookmark mark='c'/> The two walks are still completely independent, but their "
            "correlation can be almost anything: beyond plus or minus a half in thirty-nine percent of pairs. "
            "<bookmark mark='d'/> Series that wander produce large correlations by chance. The usual test, built for "
            "independent observations, would call most of them significant."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hw], lag_ratio=0.02), FadeIn(rows[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(B), Create(p1), Create(p2), FadeIn(pl), run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hr], lag_ratio=0.02), FadeIn(rows[1]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def pendulum(self):
        d = load("sunspot")
        phi = d["ols"]
        g = np.random.Generator(np.random.PCG64(1927))
        n = 80
        e = g.normal(size=n + 50)
        x = np.zeros(n + 50)
        for t in range(2, n + 50):
            x[t] = phi[0] * x[t - 1] + phi[1] * x[t - 2] + e[t]
        x, e = x[50:], e[50:]
        pend = YulePendulum(x, pivot=[-4.2, 2.6, 0], length=2.8, max_angle=0.55, color=SERIES)
        A = axes([0, n], [-1.1, 1.1], x_length=6.8, y_length=2.6, xlabel=r"time", ylabel=r"displacement", center=[2.8, 1.0, 0],
                 font_size=18)
        ax = A.ax
        xs = x / np.max(np.abs(x))
        tracker = ValueTracker(0)
        trace = always_redraw(lambda: series_line(ax, np.arange(int(tracker.get_value()) + 1), xs[: int(tracker.get_value()) + 1],
                                                  SERIES, 2.5))

        def upd(m):
            m.at(int(tracker.get_value()))

        pend.add_updater(upd)
        rows = fit_rows(VGroup(
            label(r"Yule (1927): \ a pendulum, \ pelted by boys with pea-shooters", font_size=22),
            MathTex(rf"x_t = {phi[0]:.2f}\,x_{{t-1}} {phi[1]:+.2f}\,x_{{t-2}} + e_t", font_size=30, color=MODEL),
            label(rf"the sunspots of 1749--1924: \ a period of {d['period']:.1f} years", font_size=22, color=OBS),
        ), 12.0, 0.3, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The next year Yule offered a model for series like these, with a famous image. A pendulum "
            "left to itself swings in a slowly damped rhythm. Now imagine boys with pea-shooters hitting it at random. "
            "Each pea knocks it a little, so the swing never dies away and never repeats exactly. <bookmark mark='b'/> In "
            "symbols, this year's position is a multiple of last year's, minus a multiple of the year before's, plus a fresh "
            "random shock: an autoregression. <bookmark mark='c'/> Yule fitted it to the yearly sunspot numbers from 1749 to "
            "1924, and found the pendulum's natural period: about ten and a half years, the sunspot cycle. Here it is "
            "swinging. That model, and its relatives, are what this part builds."
        ) as vo:
            self.add(pend)
            self.play(FadeIn(A))
            self.add(trace)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(tracker.animate.set_value(40), run_time=8.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), tracker.animate.set_value(n - 1), run_time=8.0, rate_func=linear)
        pend.clear_updaters()
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 17", font_size=34, color=GREY_B), label(r"Time Series", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"stationarity, \ the autocorrelation function, \ and the effective sample size",
            r"AR, \ MA and ARMA models; \ roots and the unit circle; \ pseudo-cycles",
            r"identification, \ estimation and checking: \ Box and Jenkins",
            r"forecasts with honest intervals; \ trend, \ seasonality and exponential smoothing",
            r"spurious regression, \ and what forecasting competitions teach",
        ], color=SERIES, font_size=26)
        prereq = note(r"prerequisites: \ Parts 7 and 12").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.ts}; \ the correlogram, \ the root plane, \ Yule's pendulum").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part seventeen: time series. <bookmark mark='b'/> We'll define stationarity and the "
            "autocorrelation function, and see how much information a dependent sample really holds; build autoregressive and "
            "moving-average models and read their behaviour from the roots of a polynomial; identify, fit and check them, "
            "the way George Box and Gwilym Jenkins taught; forecast with intervals that widen honestly; take apart trend and "
            "season; and end with spurious regression and the surprising lessons of forecasting competitions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
