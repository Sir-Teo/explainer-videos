from __future__ import annotations

import numpy as np

from explainer.stats.kit import ts as T
from videos.stats.stats17.common import *  # noqa: F403


class Smoothing(VoiceoverScene):
    def construct(self):
        self.card()
        self.ses_rule()
        self.ses_demo()
        self.holt_winters()
        self.co2_forecast()
        self.scores()
        self.damped()
        self.theory()

    def card(self):
        card = chapter_card(8, r"Exponential smoothing", r"Forecasting by forgetting gracefully", part=PART)
        with self.voiceover("Chapter eight. Exponential smoothing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ses_rule(self):
        a = 0.3
        A = axes([-0.6, 11.6], [0, 0.35], x_length=5.6, y_length=2.8, xlabel=r"how many periods ago", ylabel=r"weight",
                 xticks=[0, 5, 10], yticks=[0, 0.1, 0.2, 0.3], center=[3.4, -1.2, 0], font_size=18)
        ax = A.ax
        w = a * (1 - a) ** np.arange(12)
        bars = bars_at(ax, np.arange(12), w, 0.7, MODEL)
        rows = [
            cmath(r"\ell_t", r"=", r"\alpha y_t + (1 - \alpha)\,\ell_{t-1}", font_size=32),
            cmath(r"\hat y_{t+h}", r"=", r"\ell_t\ \ \text{for every } h", font_size=32),
            cmath(r"\ell_t", r"=", r"\alpha \textstyle\sum_{j=0}^{t-1}(1-\alpha)^j y_{t-j}+(1-\alpha)^t\ell_0", font_size=32),
        ]
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.4, 1.4, 0])
        rows[2][2].set_color(MODEL)
        lab = label(r"$\alpha = 0.3$: \ weights $0.3,\ 0.21,\ 0.147, \ldots$", font_size=20, color=GREY_A).next_to(A, UP, buff=0.15)
        hist = historical_tag(r"Brown (1956), \ Holt (1957), \ Winters (1960)", corner=DL)
        intro = label('Exponential smoothing gives recent observations more weight', font_size=36)
        with self.voiceover(
            "In the 1950s, operations researchers forecasting inventories for the US Navy and for factories needed something "
            "simpler than Box and Jenkins. <bookmark mark='a'/> Robert Brown and Charles Holt proposed simple exponential "
            "smoothing: keep a running level, and each period move it a fraction alpha of the way toward the new observation. "
            "<bookmark mark='b'/> The forecast for every future period is the current level. <bookmark mark='c'/> Unrolled, the "
            "level is a weighted average of the observed history plus a diminishing initialization term, with weights that fall off geometrically, by a factor one "
            "minus alpha per period: recent data count most, and the past is forgotten gracefully. Alpha near one tracks the "
            "latest value; alpha near zero averages over a long history."
        ) as vo:
            self.play(FadeIn(intro))
            self.add(hist)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
            vo.wait_until("c")
            self.play(FadeIn(g[2]), FadeIn(A), FadeIn(lab), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08))
        self.clear_scene()

    def ses_demo(self):
        m = np.asarray(museum.YULE_MORTALITY)
        yrs = np.arange(1866, 1912)
        A = axes([1864, 1913], [13.5, 22.5], x_length=9.0, y_length=4.2, xlabel=r"year", ylabel=r"mortality per 1,000",
                 xticks=[1870, 1880, 1890, 1900, 1910], yticks=[14, 18, 22], center=[-1.4, 0.3, 0])
        ax = A.ax
        dots = scatter(ax, yrs, m, color=GREY_A, radius=0.06)
        f3 = T.ses(m, 0.3)
        f8 = T.ses(m, 0.8)
        l3 = series_line(ax, yrs, f3[:-1], MODEL, 3)
        l8 = series_line(ax, yrs, f8[:-1], OBS, 3)
        rows = fit_rows(VGroup(
            label(r"Yule's mortality series, \ one-step forecasts", font_size=22),
            label(r"$\alpha = 0.3$: \ smooth, \ lags behind the fall", font_size=22, color=MODEL),
            label(r"$\alpha = 0.8$: \ follows each year closely", font_size=22, color=OBS),
            label(r"a steady trend defeats both: \ they always trail it", font_size=22, color=RES),
        ), 3.8, 0.4, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is Yule's mortality series again, with exponential smoothing's one-step-ahead forecasts. "
            "<bookmark mark='b'/> With alpha point three, the forecast is smooth, but it lags behind the steady fall in "
            "deaths. <bookmark mark='c'/> With alpha point eight it follows each year closely, noise and all. "
            "<bookmark mark='d'/> Either way the forecast trails a trend: simple smoothing assumes a level that wanders, not one "
            "that slopes. It needs a second component."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(l3), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(l8), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def holt_winters(self):
        rows = [
            cmath(r"\ell_t", r"=", r"\alpha (y_t - s_{t-m}) + (1 - \alpha)(\ell_{t-1} + b_{t-1})", font_size=28),
            cmath(r"b_t", r"=", r"\beta (\ell_t - \ell_{t-1}) + (1 - \beta)\, b_{t-1}", font_size=28),
            cmath(r"s_t", r"=", r"\gamma (y_t - \ell_t) + (1 - \gamma)\, s_{t-m}", font_size=28),
            cmath(r"\hat y_{t+h}", r"=", r"\ell_t + h\, b_t + s_{t-m+1+((h-1)\bmod m)}", font_size=30),
        ]
        rows[3][2].set_color(FC)
        whys = [why(r"the level, \ with last year's season removed"), why(r"the slope: \ Holt (1957)"),
                why(r"the season, \ $m = 12$: \ Winters (1960)"), why(r"level, \ plus slope times horizon, \ plus season")]
        with self.voiceover(
            "<bookmark mark='a'/> Holt added a slope, and his student Peter Winters a season, in 1960. The level is smoothed as "
            "before, after removing the seasonal effect for this month. <bookmark mark='b'/> The slope is smoothed too: a "
            "running average of how much the level changes each period, with its own smoothing constant beta. "
            "<bookmark mark='c'/> And each calendar month's seasonal effect is updated, with constant gamma, whenever that "
            "month comes round. <bookmark mark='d'/> The forecast h periods ahead is the level, plus h times the slope, plus "
            "the right month's seasonal effect. Three smoothing constants, chosen to minimize the one-step forecast errors on "
            "the past."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def co2_forecast(self):
        d = load("hw")
        t, y = np.asarray(d["t"]), np.asarray(d["y"])
        cut = d["cut"]
        A = axes([1993, 2002.2], [348, 376], x_length=10.2, y_length=3.9, xlabel=r"year", ylabel=r"CO$_2$, \ ppm",
                 xticks=[1994, 1996, 1998, 2000, 2002], yticks=[350, 360, 370], center=[-0.6, 0.95, 0])
        ax = A.ax
        k0 = np.searchsorted(t, 1993.0)
        past = series_line(ax, t[k0:cut], y[k0:cut], S.ALT, 2.2)
        tf = t[cut:]
        actual = series_line(ax, tf, y[cut:], GREY_A, 2.2, 0.9)
        hw = series_line(ax, tf, d["forecast"], FC, 3)
        sn = series_line(ax, tf, d["snaive"], RES, 2.2, 0.8)
        cutl = DashedLine(ax.c2p(1998.0, 348), ax.c2p(1998.0, 375), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"fit to 1959--1997; \ forecast 48 months", font_size=22),
            MathTex(rf"\hat\alpha = {d['alpha']:.2f},\ \ \hat\beta = {d['beta']:.2f},\ \ \hat\gamma = {d['gamma']:.2f}", font_size=26, color=FC),
            label(r"red: \ last year's values, \ repeated", font_size=22, color=RES),
            label(r"grey: \ what Mauna Loa recorded", font_size=22, color=GREY_A),
        ), 12.0, 0.2, [0, -2.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Let's forecast Keeling's curve. Fit Holt–Winters to the record up to the end of 1997, and "
            "forecast the next four years, month by month. <bookmark mark='b'/> The fitted constants: alpha about a half, beta "
            "point oh one, gamma about a half. The tiny beta means the slope is estimated from a long stretch of history, "
            "while level and season adapt quickly. <bookmark mark='c'/> For comparison, the seasonal naive forecast simply "
            "repeats the last year's values. <bookmark mark='d'/> And here's what was recorded. Holt–Winters tracks it closely "
            "for four years; the seasonal naive forecast, with no trend, falls steadily behind."
        ) as vo:
            self.play(FadeIn(A), Create(past), Create(cutl), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(hw), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(sn), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(actual), FadeIn(rows[3]), run_time=2.0)
        self.clear_scene()

    def scores(self):
        d = load("hw")
        tab = table_rows([
            [r"method, \ 48 months ahead", r"MASE"],
            [r"simple smoothing: \ a flat line", f"{d['mase_ses']:.2f}"],
            [r"seasonal naive: \ last year again", f"{d['mase_snaive']:.2f}"],
            [r"seasonal naive plus the average yearly rise", f"{d['mase_sdrift']:.2f}"],
            [r"Holt--Winters", f"{d['mase_hw']:.2f}"],
        ], font_size=28, colors=[GREY_B, GREY_A, RES, OBS, FC]).move_to([0, 0.7, 0])
        foot = label(r"MASE scaled by the in-sample error of the seasonal naive forecast", font_size=22, color=GREY_B
                     ).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The scores, as mean absolute scaled errors, scaled this time by the seasonal naive forecast's in-sample error. "
            "<bookmark mark='a'/> Simple smoothing, a flat line with no trend or season: four point five three. "
            "<bookmark mark='b'/> The seasonal naive forecast: four point oh two, because the series has climbed since last "
            "year. <bookmark mark='c'/> Adding the average yearly rise to it: one point five three. <bookmark mark='d'/> "
            "Holt–Winters: point seven eight. Each component the model represents, the season, then the trend, cuts the error "
            "substantially."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def damped(self):
        h = np.arange(0, 41)
        lvl, b = 10.0, 0.5
        A = axes([0, 40], [0, 32], x_length=8.4, y_length=4.2, xlabel=r"forecast horizon $h$", ylabel=r"forecast",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 10, 20, 30], center=[-1.6, 0.3, 0])
        ax = A.ax
        holt = series_line(ax, h, lvl + b * h, RES, 3)
        cols = {0.95: OBS, 0.85: HIT}
        damp = {ph: series_line(ax, h, lvl + b * np.r_[0, np.cumsum(ph ** np.arange(1, 41))], cols[ph], 3) for ph in (0.95, 0.85)}
        rows = fit_rows(VGroup(
            MathTex(r"\hat y_{t+h} = \ell_t + (\phi + \phi^2 + \cdots + \phi^h)\, b_t", font_size=28),
            label(r"Holt: \ $\phi = 1$, \ the slope forever", font_size=22, color=RES),
            label(r"$\phi = 0.95$, \ $0.85$: \ the slope fades, \ the forecast levels off", font_size=22, color=OBS),
            label(r"Gardner \& McKenzie (1985): \ a winner in M3", font_size=22, color=GREY_A),
        ), 4.2, 0.4, [4.8, 0.3, 0])
        tag = label(r"illustrative: \ level 10, \ slope 0.5", font_size=18, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "One small change to Holt's method has a remarkable record. <bookmark mark='a'/> Holt's forecast extends today's "
            "slope forever, in a straight line. Over long horizons that's usually too bold: growth rarely continues unchecked. "
            "<bookmark mark='b'/> Everette Gardner and Ed McKenzie, in 1985, multiplied the slope's contribution by a damping "
            "factor phi at each step ahead, so the forecast trend fades and the forecast levels off. <bookmark mark='c'/> With "
            "phi point nine five it bends gently; with point eight five, sooner. <bookmark mark='d'/> This damped trend was "
            "among the most accurate methods in the M3 competition, and it's now a standard benchmark."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(holt), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(damp[0.95]))
            vo.wait_until("c")
            self.play(Create(damp[0.85]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def theory(self):
        rows = [
            cmath(r"\text{SES}", r"\equiv", r"\text{the optimal forecast for ARIMA}(0, 1, 1)", font_size=30),
            cmath(r"\text{ARIMA}(0,1,1)", r":", r"y_t - y_{t-1} = e_t - (1 - \alpha)\, e_{t-1}", font_size=30),
            cmath(r"\text{ETS}", r":", r"\text{state-space models with these updates}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{likelihoods, \ intervals, \ AIC for smoothing}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"Muth (1960)"), why(r"a random walk plus noise"),
                why(r"Hyndman, \ Koehler, \ Snyder \& Grose (2002)"), why(r"ad hoc rules, \ given a statistical model")]
        intro = label('A statistical model gives smoothing an uncertainty calculation', font_size=36)
        with self.voiceover(
            "Is this ad hoc? Less than it looks. <bookmark mark='a'/> John Muth showed in 1960 that simple exponential "
            "smoothing gives the optimal forecast for a particular model, <bookmark mark='b'/> an ARIMA zero one one, which is "
            "a random walk observed with noise: the smoothing constant is set by the ratio of the two variances. "
            "<bookmark mark='c'/> In 2002 Rob Hyndman and colleagues showed that the standard exponential smoothing methods can be represented as "
            "forecasts of state-space models, the ETS family, for error, trend and season. <bookmark mark='d'/> So smoothing "
            "methods have likelihoods, prediction intervals and information criteria, like everything else in this part."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()
