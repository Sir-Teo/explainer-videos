from __future__ import annotations

import numpy as np

from explainer.stats.kit import ts as T
from videos.stats.stats17.common import *  # noqa: F403

MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]


class Seasonal(VoiceoverScene):
    def construct(self):
        self.card()
        self.keeling()
        self.model()
        self.panels()
        self.figure()
        self.growth()
        self.leftover()
        self.variants()

    def card(self):
        card = chapter_card(7, r"Trend and seasonality", r"Taking a series apart", part=PART)
        with self.voiceover("Chapter seven. Trend and seasonality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def keeling(self):
        d = load("co2")
        t, y = np.asarray(d["t"]), np.asarray(d["y"])
        A = axes([1958, 2003], [310, 375], x_length=8.6, y_length=4.4, xlabel=r"year", ylabel=r"CO$_2$, \ parts per million",
                 xticks=[1960, 1970, 1980, 1990, 2000], yticks=[320, 340, 360], center=[-1.6, 0.2, 0])
        ln = series_line(A.ax, t, y, S.ALT, 1.8)
        hc = fit_rows(VGroup(
            label(r"Mauna Loa, \ Hawaii, \ 3,400 m", font_size=22),
            label(r"C. D. Keeling, \ from 1958", font_size=22, color=GREY_A),
            MathTex(rf"{d['first']:.0f} \to {d['last']:.0f}\ \text{{ppm}}", font_size=30, color=S.ALT),
            label(r"a rising trend, \ and a yearly wave", font_size=22, color=OBS),
        ), 4.0, 0.4, [4.9, 0.4, 0])
        tag = historical_tag(r"Keeling's record, \ as statsmodels ships it", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> In 1958 Charles David Keeling began measuring carbon dioxide in the air on Mauna Loa, a "
            "Hawaiian volcano three thousand four hundred metres up, far from local sources. Here are the monthly averages to "
            "the end of 2001. <bookmark mark='b'/> Two things are obvious at once. The level rises, from three hundred and "
            "sixteen parts per million in 1959 to three hundred and seventy-one in 2001. <bookmark mark='c'/> And it waves, up "
            "and down, every year. Neither a trend nor a season is stationary. To model the series, first take it apart."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), FadeIn(hc[0]), FadeIn(hc[1]))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(hc[2]))
            vo.wait_until("c")
            self.play(FadeIn(hc[3]))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"y_t", r"=", r"T_t + S_t + R_t", font_size=34),
            cmath(r"\hat T_t", r"=", r"\tfrac{1}{24}y_{t-6} + \tfrac1{12}(y_{t-5} + \cdots + y_{t+5}) + \tfrac{1}{24}y_{t+6}", font_size=28),
            cmath(r"\hat S_m", r"=", r"\text{average of } y_t - \hat T_t \text{ over all months } m,\ \textstyle\sum_m \hat S_m = 0", font_size=28),
            cmath(r"\hat R_t", r"=", r"y_t - \hat T_t - \hat S_t", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"trend, \ season, \ remainder"), why(r"a centred 2 $\times$ 12 moving average: \ one full year"),
                why(r"the seasonal figure: \ 12 numbers"), why(r"what's left, \ hopefully stationary")]
        with self.voiceover(
            "<bookmark mark='a'/> The classical decomposition writes the series as a trend, plus a seasonal pattern, plus a "
            "remainder. <bookmark mark='b'/> Estimate the trend with a moving average spanning exactly one year: thirteen "
            "months centred on each point, with half weight on the two ends, so every calendar month counts equally and the "
            "seasonal wave cancels. <bookmark mark='c'/> Subtract the trend, and average what's left for each calendar month: "
            "twelve numbers, adjusted to sum to zero, the seasonal figure. <bookmark mark='d'/> What remains is the remainder. "
            "If the decomposition has worked, it should look like a stationary series, ready for chapter two's models."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def panels(self):
        d = load("co2")
        t = np.asarray(d["t"])
        specs = [("y", r"data", S.ALT, (310, 375)), ("trend", r"trend", MODEL, (310, 375)),
                 ("seasonal", r"seasonal", OBS, (-4, 4)), ("remainder", r"remainder", RES, (-1.2, 1.2))]
        panels = VGroup()
        for k, (key, nm, col, (lo, hi)) in enumerate(specs):
            A = axes([1958, 2003], [lo, hi], x_length=10.6, y_length=1.25, center=[0.5, 2.55 - 1.65 * k, 0], font_size=14)
            ln = series_line(A.ax, t, d[key], col, 1.6)
            lab = label(nm, font_size=22, color=col).next_to(A, LEFT, buff=0.2)
            panels.add(VGroup(A, ln, lab))
        ticks = VGroup(*[MathTex(str(yr), font_size=18, color=GREY_B).next_to(panels[3][0].ax.c2p(yr, -1.2), DOWN, buff=0.1)
                         for yr in (1960, 1970, 1980, 1990, 2000)])
        sdev = MathTex(rf"\text{{SD}} = {d['rem_sd']:.2f}\ \text{{ppm}}", font_size=24, color=RES).next_to(panels[3][0], RIGHT, buff=0.1)
        sdev.shift(LEFT * 1.3 + UP * 0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the result, as four panels on a common time axis. The data. <bookmark mark='b'/> The "
            "trend: smooth, and steepening. <bookmark mark='c'/> The seasonal component: the same wave each year, about six "
            "parts per million from trough to peak. <bookmark mark='d'/> And the remainder: small wiggles with a standard "
            "deviation of a quarter of a part per million. It still has some memory, and an ARMA model could describe it, "
            "but the trend and the season carry nearly everything."
        ) as vo:
            self.add(ticks)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                p = panels[k]
                self.play(FadeIn(p[0]), FadeIn(p[2]), Create(p[1]), run_time=1.4)
            self.play(FadeIn(sdev))
        self.clear_scene()

    def figure(self):
        d = load("co2")
        f = np.asarray(d["figure"])
        A = axes([-0.6, 11.6], [-3.6, 3.6], x_length=8.6, y_length=4.2, xlabel=r"", ylabel=r"ppm above the trend",
                 yticks=[-3, 0, 3], center=[-1.6, 0.2, 0])
        ax = A.ax
        bars = VGroup()
        for m, v in enumerate(f):
            top, bot = ax.c2p(m, max(v, 0)), ax.c2p(m, min(v, 0))
            h = max(1e-3, top[1] - bot[1])
            bars.add(Rectangle(width=ax.c2p(0.7, 0)[0] - ax.c2p(0, 0)[0], height=h, stroke_width=0,
                               fill_color=HIT if v > 0 else RES, fill_opacity=0.85).move_to((top + bot) / 2))
        ml = VGroup(*[label(MONTHS[m], font_size=20, color=GREY_B).next_to(ax.c2p(m, -3.6), DOWN, buff=0.1) for m in range(12)])
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(11.6, 0), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{May}}: +{f[4]:.1f}", font_size=28, color=HIT),
            MathTex(rf"\text{{October}}: {f[9]:.1f}", font_size=28, color=RES),
            label(r"the northern forests breathe in each summer", font_size=22),
            label(r"and out each winter", font_size=22),
        ), 4.0, 0.4, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The seasonal figure, month by month. <bookmark mark='b'/> The air holds the most carbon dioxide "
            "in May, nearly three parts per million above the trend, <bookmark mark='c'/> and the least in September and "
            "October, about three below. <bookmark mark='d'/> It's the breathing of the northern hemisphere's vegetation, which "
            "has most of the planet's land: plants draw carbon dioxide in as they grow through the summer, and decay and "
            "respiration release it through the winter. A statistical decomposition, read the right way, shows a planet "
            "breathing."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(ml))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if v > 0 else UP) for b_, v in zip(bars, f)], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), Indicate(bars[4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), Indicate(bars[9]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def growth(self):
        d = load("co2")
        t, tr = np.asarray(d["t"]), np.asarray(d["trend"])
        A = axes([1958, 2003], [310, 375], x_length=8.6, y_length=4.2, xlabel=r"year", ylabel=r"the trend, \ ppm",
                 xticks=[1960, 1970, 1980, 1990, 2000], yticks=[320, 340, 360], center=[-1.6, 0.2, 0])
        ax = A.ax
        ln = series_line(ax, t, tr, MODEL, 3)
        k = np.isfinite(tr)
        e = (t < 1969) & k
        l_ = (t > 1991) & k
        ce = np.polyfit(t[e], tr[e], 1)
        cl = np.polyfit(t[l_], tr[l_], 1)
        s1 = Line(ax.c2p(1958.5, np.polyval(ce, 1958.5)), ax.c2p(1975, np.polyval(ce, 1975)), color=HIT, stroke_width=4)
        s2 = Line(ax.c2p(1985, np.polyval(cl, 1985)), ax.c2p(2002, np.polyval(cl, 2002)), color=RES, stroke_width=4)
        rows = fit_rows(VGroup(
            MathTex(rf"1959\text{{--}}68:\ {d['early']:.2f}\ \text{{ppm/year}}", font_size=28, color=HIT),
            MathTex(rf"1992\text{{--}}2001:\ {d['late']:.2f}\ \text{{ppm/year}}", font_size=28, color=RES),
            label(r"the rise is itself rising", font_size=22, color=OBS),
            label(r"a straight-line trend would forecast badly", font_size=22, color=GREY_A),
        ), 4.2, 0.4, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The trend deserves its own look. <bookmark mark='b'/> In the first decade it rose about three "
            "quarters of a part per million a year. <bookmark mark='c'/> In the last decade of the record, one point six four: "
            "more than twice as fast. <bookmark mark='d'/> The growth is accelerating, so a straight-line trend fitted to the "
            "whole record would forecast too low. Any trend we extrapolate is an assumption about the future, and the "
            "forecasting methods of the next chapter let the trend's slope adapt as the data arrive."
        ) as vo:
            self.play(FadeIn(A), Create(ln))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(s1), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(s2), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def leftover(self):
        d = load("co2")
        r = np.asarray(d["remainder"])
        r = r[np.isfinite(r)]
        a = T.acf(r, 24)
        A = axes([0, 25], [-0.5, 0.5], x_length=8.4, y_length=3.8, xlabel=r"lag, \ months", ylabel=r"ACF of the remainder",
                 xticks=[0, 6, 12, 18, 24], yticks=[-0.4, 0, 0.4], center=[-1.6, 0.3, 0])
        cg = Correlogram(A.ax, a, band=2 / np.sqrt(len(r)), color=RES, hot=RES)
        Q, pq = T.ljung_box(r, 24)
        rows = fit_rows(VGroup(
            MathTex(rf"\hat\rho(1) = {a[1]:.2f}", font_size=28, color=RES),
            label(r"a wave: \ negative at lags 4--7, \ positive at 11--12", font_size=22),
            MathTex(rf"\text{{Ljung--Box}}\ Q(24) = {Q:.0f}", font_size=26),
            label(r"the season itself changes over the years", font_size=22, color=OBS),
            label(r"a fixed seasonal figure can't follow it", font_size=22, color=GREY_A),
        ), 4.2, 0.38, [4.9, 0.3, 0])
        with self.voiceover(
            "Is the remainder really just noise? Chapter five's check says no. <bookmark mark='a'/> Its autocorrelation at lag "
            "one is point four: a wet month tends to follow a wet month, so to speak. <bookmark mark='b'/> And there's a wave in "
            "the correlogram, negative around lags four to seven and positive again at a year. <bookmark mark='c'/> The "
            "Ljung–Box statistic is enormous. <bookmark mark='d'/> The yearly wave left over in the remainder says the season "
            "isn't the same every year: its shape and size drift, partly with the growing level and partly with climate, and "
            "<bookmark mark='e'/> twelve fixed numbers can't follow that. Methods that let the season evolve, and an ARMA model "
            "for what's left, do better."
        ) as vo:
            self.play(FadeIn(A), FadeIn(cg.zero), FadeIn(cg.bands))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cg.bars], lag_ratio=0.04), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def variants(self):
        rows = fit_rows(VGroup(
            label(r"multiplicative seasons, \ $y = T \times S \times R$: \ take logs first", font_size=24),
            label(r"STL (Cleveland et al., \ 1990): \ local regression; \ the season may evolve", font_size=24, color=MODEL),
            label(r"X-11, \ X-13: \ the official seasonal adjustment of economic statistics", font_size=24, color=GREY_A),
            label(r"seasonally adjusted series: \ the data minus $\hat S$", font_size=24, color=OBS),
            label(r"decomposition describes; \ forecasting needs a model of how the parts move", font_size=24, color=RES),
        ), 12.4, 0.48, [0, 0, 0])
        with self.voiceover(
            "Some variations. <bookmark mark='a'/> When the seasonal swing grows with the level, as in retail sales, the parts "
            "multiply rather than add, and one takes logs first. <bookmark mark='b'/> STL, from Robert Cleveland and colleagues "
            "in 1990, replaces the moving averages with local regressions and lets the seasonal pattern change slowly over the "
            "years. <bookmark mark='c'/> Statistical agencies use the X-11 and X-13 programs to seasonally adjust "
            "unemployment and output figures, <bookmark mark='d'/> the series you read in the news, with the estimated "
            "season removed. <bookmark mark='e'/> But a decomposition describes the past. To forecast, we need a model of how "
            "the level, the slope and the season move."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
