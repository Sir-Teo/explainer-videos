from __future__ import annotations

import numpy as np

from videos.stats.stats17.common import *  # noqa: F403


class Forecast(VoiceoverScene):
    def construct(self):
        self.card()
        self.best_linear()
        self.widening()
        self.random_walk()
        self.sunspot_ar2()
        self.sunspot_ar8()
        self.scoring()
        self.cautions()

    def card(self):
        card = chapter_card(6, r"Forecasting", r"How far ahead can memory see?", part=PART)
        with self.voiceover("Chapter six. Forecasting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def best_linear(self):
        rows = [
            cmath(r"\hat X_{n+h}", r"=", r"E[X_{n+h} \mid X_n, X_{n-1}, \ldots]", font_size=32),
            cmath(r"\text{AR}(p)", r":", r"\text{run the recursion, \ with future shocks set to } 0", font_size=30),
            cmath(r"\text{AR(1)}", r":", r"\hat X_{n+h} - \mu = \phi^h (X_n - \mu)", font_size=32),
            cmath(r"\text{error variance}", r":", r"\sigma^2 \textstyle\sum_{j=0}^{h-1} \psi_j^2", font_size=32),
        ]
        rows[3][2].set_color(FC)
        whys = [why(r"the minimum mean squared error forecast"), why(r"the shocks we can't yet see average zero"),
                why(r"memory fades: \ forecasts return to the mean"), why(r"the shocks between now and then, \ weighted")]
        with self.voiceover(
            "<bookmark mark='a'/> The best forecast, in mean squared error, is the conditional mean of the future given the "
            "past. <bookmark mark='b'/> For the Gaussian innovation models used here, future shocks have conditional mean zero, so it is easy to compute: run the model's recursion forward, setting "
            "every future shock to its mean, zero. <bookmark mark='c'/> For an AR one, the forecast h steps ahead is the "
            "current deviation from the mean, shrunk by phi to the h. As h grows, the forecast returns to the mean: memory "
            "fades. <bookmark mark='d'/> Its error is made of the shocks that will arrive between now and then, weighted by "
            "the psi weights of chapter two, so its variance is sigma squared times the sum of the first h squared weights."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def widening(self):
        phi = 0.8
        h = np.arange(1, 21)
        se = np.sqrt(np.cumsum(phi ** (2 * np.arange(20))))
        marg = 1 / np.sqrt(1 - phi ** 2)
        A = axes([0, 20], [0, 1.9], x_length=8.0, y_length=4.0, xlabel=r"forecast horizon $h$", ylabel=r"forecast SE / $\sigma$",
                 xticks=[1, 5, 10, 15, 20], yticks=[0, 0.5, 1, 1.5], center=[-1.6, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=FC) for a, b in zip(h, se)])
        lim = DashedLine(ax.c2p(0, marg), ax.c2p(20, marg), color=GREY_B, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"AR(1), \ $\phi = 0.8$", font_size=24),
            MathTex(r"h = 1:\ \ \sigma", font_size=28, color=FC),
            MathTex(rf"h \to \infty:\ \ \sigma/\sqrt{{1 - \phi^2}} = {marg:.2f}\,\sigma", font_size=28, color=GREY_B),
            label(r"far ahead, \ the forecast is the mean, \ its error the series' own spread", font_size=22, color=GREY_A),
        ), 4.2, 0.4, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For an AR one with phi point eight, here's the forecast's standard error against the horizon. "
            "<bookmark mark='b'/> One step ahead it's just sigma, the size of a single shock. <bookmark mark='c'/> It grows "
            "with the horizon, and levels off at the standard deviation of the series itself, one point six seven sigma. "
            "<bookmark mark='d'/> Far enough ahead, the past tells us nothing: the forecast is the mean, and its interval is "
            "the series' ordinary range. Stable causal ARMA models with decaying impulse weights behave this way; a stationary deterministic component can remain predictable. A random walk, whose variance has no "
            "limit, has intervals that widen forever."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[0], scale=1.5), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots[1:]], lag_ratio=0.1), Create(lim), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def random_walk(self):
        g = np.random.Generator(np.random.PCG64(1704))
        x = np.cumsum(g.normal(size=60))
        h = np.arange(0, 31)
        tf = 59 + h
        lo, hi = x[-1] - 1.96 * np.sqrt(h), x[-1] + 1.96 * np.sqrt(h)
        A = axes([0, 90], [x.min() - 12, x.max() + 12], x_length=9.4, y_length=4.2, xlabel=r"time", center=[-1.0, 0.4, 0])
        ax = A.ax
        ln = series_line(ax, np.arange(60), x, RES, 2.4)
        bd = band(ax, tf, lo, hi, FC, 0.25)
        fl = series_line(ax, tf, np.full(31, x[-1]), FC, 3)
        rows = fit_rows(VGroup(
            MathTex(r"\hat X_{n+h} = X_n", font_size=30, color=FC),
            MathTex(r"\text{SE} = \sigma\sqrt h", font_size=30, color=FC),
            label(r"the best forecast is ``no change''", font_size=22),
            label(r"and the interval never stops widening", font_size=22, color=RES),
        ), 3.2, 0.4, [5.4, 0.4, 0])
        tag = simulated_tag(r"a random walk", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> For a random walk the story is different. The next step is equally likely to go up or down, "
            "so the best forecast for every horizon is simply the last value: no change. <bookmark mark='b'/> But the errors "
            "accumulate, one shock per step, so the forecast's standard error is sigma times the square root of h, "
            "<bookmark mark='c'/> and the interval keeps widening without limit. <bookmark mark='d'/> This is the naive forecast "
            "that every method must beat. For stock prices and exchange rates, which behave much like random walks, it is "
            "notoriously hard to beat."
        ) as vo:
            self.play(FadeIn(A), Create(ln), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(fl), FadeIn(rows[0]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(bd), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Indicate(fl, color=FC))
        self.clear_scene()

    def fc_axes(self):
        A = axes([1865, 1956], [-40, 170], x_length=11.6, y_length=3.9, xlabel=r"year", ylabel=r"sunspots",
                 xticks=[1870, 1890, 1910, 1930, 1950], yticks=[0, 50, 100, 150], center=[0, 0.95, 0])
        return A, A.ax

    def sunspot_ar2(self):
        d = load("forecast")
        A, ax = self.fc_axes()
        tr = series_line(ax, d["train_years"], d["train"], OBS, 2.2)
        yrs = np.asarray(d["years"])
        cut = DashedLine(ax.c2p(1924.5, -40), ax.c2p(1924.5, 165), color=GREY_C, stroke_width=1.5)
        f = d["p2"]
        bd = band(ax, yrs, np.asarray(f["lo"]), np.asarray(f["hi"]), FC, 0.22)
        mn = series_line(ax, yrs, f["mean"], FC, 3)
        act = series_line(ax, yrs, d["actual"], GREY_A, 2, 0.9)
        rows = fit_rows(VGroup(
            label(r"fit to 1749--1924; \ forecast 1925--1955", font_size=22),
            label(r"AR(2): \ one damped swing, \ then the mean", font_size=22, color=FC),
            label(r"grey: \ what happened", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -2.75, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now the sunspots. Stand in 1924, at the end of Yule's data, with everything before it to "
            "fit. <bookmark mark='b'/> The AR two forecasts one damped swing up from the low of 1924, peaking a little above "
            "fifty, and then settles to the mean of forty-four. The band is the ninety-five percent forecast interval, "
            "widening quickly to the full range of the series, and below zero, which a sunspot count cannot be: the normal "
            "shocks are only an approximation. <bookmark mark='c'/> In grey, what actually happened: three full cycles, with a "
            "peak of a hundred and fifty-two in 1947. The AR two caught the first rise, and after that it only knew the mean."
        ) as vo:
            self.play(FadeIn(A), Create(tr), Create(cut))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bd), Create(mn), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(act), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()

    def sunspot_ar8(self):
        d = load("forecast")
        best = d["best"]
        A, ax = self.fc_axes()
        tr = series_line(ax, d["train_years"], d["train"], OBS, 2.2)
        yrs = np.asarray(d["years"])
        f = d[f"p{best}"]
        bd = band(ax, yrs, np.asarray(f["lo"]), np.asarray(f["hi"]), HIT, 0.22)
        mn = series_line(ax, yrs, f["mean"], HIT, 3)
        mn2 = series_line(ax, yrs, d["p2"]["mean"], FC, 2, 0.6)
        act = series_line(ax, yrs, d["actual"], GREY_A, 2, 0.9)
        rows = fit_rows(VGroup(
            label(rf"AR({best}): \ the longer memory forecasts more of the cycle", font_size=22, color=HIT),
            label(r"its swings shrink too, \ but more slowly", font_size=22),
            label(r"the 1947 peak was beyond both", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -2.75, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The AR eight, chosen by AIC, forecasts more. From the same 1924 low, it predicts a rise to "
            "about seventy by 1927, close to the real seventy-eight of 1928, then a fall, and then a second, smaller cycle. "
            "<bookmark mark='b'/> Its swings also fade toward the mean, but more slowly: it remembers the eleven-year rhythm. "
            "<bookmark mark='c'/> Neither model saw the great peak of 1947 coming. No linear model can predict the height of "
            "a cycle that far ahead: the shocks that will build it haven't happened yet."
        ) as vo:
            self.play(FadeIn(A), Create(tr), Create(act), Create(mn2))
            vo.wait_until("a")
            self.play(FadeIn(bd), Create(mn), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def scoring(self):
        d = load("forecast")
        best = d["best"]
        rows = [
            cmath(r"\text{MASE}", r"=", r"\frac{\text{mean } |y_{n+h} - \hat y_{n+h}|}{\text{in-sample mean } |y_t - y_{t-1}|}", font_size=30),
            cmath(r"\text{naive (last value)}", r":", rf"{d['naive_mase']:.2f}", font_size=30),
            cmath(r"\text{the mean}", r":", rf"{d['mean_mase']:.2f}", font_size=30),
            cmath(r"\text{AR(2)};\ \ \text{AR}" + rf"({best})", r":", rf"{d['p2']['mase']:.2f};\ \ {d[f'p{best}']['mase']:.2f}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"Hyndman \& Koehler (2006): \ below 1 beats the naive forecast's usual error"),
                why(r"the first 11 years, \ 1925--1935"), why(r"knows only the level"), why(r"memory pays")]
        intro = label('Scale forecast errors using the training data', font_size=36)
        with self.voiceover(
            "How to score forecasts fairly across series of different scales? <bookmark mark='a'/> Rob Hyndman and Anne "
            "Koehler's mean absolute scaled error divides the forecast's average absolute error by the average one-step change "
            "within the training data, so below one beats the naive forecast's typical in-sample error. "
            "<bookmark mark='b'/> Over the first eleven years, one full cycle, the naive forecast, the 1924 value carried "
            "forward, scores one point six nine. <bookmark mark='c'/> The long-run mean, one point three eight. "
            "<bookmark mark='d'/> Yule's AR two, one point two oh. And the AR eight, point five eight: half the AR two's error. "
            "Here the extra memory that AIC chose was worth having."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def cautions(self):
        d = load("forecast")
        rows = fit_rows(VGroup(
            label(r"intervals assume the model is right, \ and its parameters known", font_size=24),
            label(r"estimated parameters add error; \ the bootstrap can include it (Part 16)", font_size=24, color=BOOT),
            label(r"normal shocks gave intervals below zero: \ check the error distribution", font_size=24, color=RES),
            label(r"of the 31 years, \ 87\% (AR(2)) and 90\% (AR(8)) fell inside the 95\% bands", font_size=24, color=OBS),
            label(r"score forecasts on data the model never saw", font_size=26, color=HIT),
        ), 12.4, 0.48, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Some cautions. Forecast intervals assume the model is right and its parameters known. "
            "<bookmark mark='b'/> Estimated parameters add error, which refitting simulated training histories and adding new future shocks in Part 16's "
            "parametric bootstrap, can include. <bookmark mark='c'/> Normal shocks gave intervals that went below zero; "
            "sunspot numbers are skewed, and a square-root transformation is often used. <bookmark mark='d'/> Of the thirty-one "
            "years forecast, eighty-seven percent of the outcomes fell inside the AR two's ninety-five percent bands, and ninety "
            "percent inside the AR eight's: short of the promise, though thirty-one correlated years are a small test. "
            "<bookmark mark='e'/> Above all, score forecasts on data the model never saw."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
