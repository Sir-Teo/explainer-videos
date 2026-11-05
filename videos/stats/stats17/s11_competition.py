from __future__ import annotations

import numpy as np

from videos.stats.stats17.common import *  # noqa: F403

NAMES = {"naive": r"naive: \ the last value", "drift": r"drift: \ the average step continued", "ses": r"simple smoothing",
         "ar": r"AR, \ order by AIC", "combo": r"the average of drift, \ smoothing and AR"}


class Competition(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.results()
        self.mini()
        self.ranks()
        self.why_combine()
        self.rolling()
        self.lessons()

    def card(self):
        card = chapter_card(10, r"The M-competitions", r"What actually forecasts well?", lit=(1982,), part=PART)
        with self.voiceover("Chapter ten. The M-competitions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        hc = history_card(1979, r"S. Makridakis \& M. Hibon, \ \emph{JRSS A}",
                          r"``Accuracy of forecasting: \ an empirical investigation'': \ 111 series, \ and the sophisticated "
                          r"methods were not more accurate than simple ones", color=OBS, width=10.4, font_size=24).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"the discussants objected: \ the methods must have been misapplied", font_size=22, color=GREY_A),
            label(r"so Makridakis invited the experts to run their own methods", font_size=22),
            label(r"M (1982): \ 1,001 series \quad M3 (2000): \ 3,003 \quad M4 (2018): \ 100,000", font_size=24, color=OBS),
        ), 12.4, 0.32, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1979 Spyros Makridakis and Michèle Hibon compared forecasting methods on a hundred and "
            "eleven real series, holding out the last observations of each. Their finding was awkward: the sophisticated "
            "methods, Box–Jenkins included, were not more accurate than simple ones. <bookmark mark='b'/> The discussants at "
            "the Royal Statistical Society objected that the methods must have been misapplied. <bookmark mark='c'/> So "
            "Makridakis invited the experts to forecast the series themselves. <bookmark mark='d'/> The M-competition of "
            "1982 used a thousand and one series; M3, in 2000, three thousand and three; M4, in 2018, a hundred thousand."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def results(self):
        rows = fit_rows(VGroup(
            label(r"what the competitions found, \ again and again:", font_size=26),
            label(r"1. \ \ sophisticated methods are not necessarily more accurate", font_size=24, color=SERIES),
            label(r"2. \ \ the ranking depends on the accuracy measure and the horizon", font_size=24, color=SERIES),
            label(r"3. \ \ combining forecasts beats most of the methods combined", font_size=24, color=HIT),
            label(r"4. \ \ simple benchmarks, \ such as damped trend smoothing, \ are hard to beat", font_size=24, color=OBS),
            label(r"M4 (2018): \ the winners combined statistics with machine learning", font_size=22, color=GREY_A),
        ), 12.4, 0.45, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The conclusions held up through every round. <bookmark mark='b'/> Sophisticated methods aren't "
            "necessarily more accurate than simple ones. <bookmark mark='c'/> Which method wins depends on how accuracy is "
            "measured and how far ahead. <bookmark mark='d'/> Averaging the forecasts of several methods beats most of the "
            "methods being averaged. <bookmark mark='e'/> And simple benchmarks, exponential smoothing with a damped trend "
            "especially, are very hard to beat. <bookmark mark='f'/> In M4, the top entries combined statistical models with "
            "machine learning, and pure machine-learning entries did poorly: a lesson Part 19 will return to."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mini(self):
        d = load("mcomp")
        meths = d["methods"]
        mm = d["mean_mase"]
        A = axes([1.6, 1.9], [0, 5], x_length=6.4, y_length=3.8, xlabel=r"mean MASE, \ 6 steps ahead \ (lower is better)",
                 xticks=[1.6, 1.7, 1.8, 1.9], center=[1.2, 0.0, 0], xfmt=lambda v: f"{v:.1f}")
        ax = A.ax
        order = sorted(meths, key=lambda m: -mm[m])
        bars = VGroup()
        labs = VGroup()
        for k, m in enumerate(order):
            y = 0.6 + k * 0.95
            col = HIT if m == "combo" else SERIES
            bars.add(Line(ax.c2p(1.6, y), ax.c2p(mm[m], y), color=col, stroke_width=16))
            labs.add(VGroup(label(NAMES[m], font_size=20, color=col).next_to(ax.c2p(1.6, y), LEFT, buff=0.2),
                            MathTex(f"{mm[m]:.3f}", font_size=22, color=col).next_to(ax.c2p(mm[m], y), RIGHT, buff=0.12)))
        head = fit_rows(VGroup(
            label(rf"our own competition: \ {d['n_series']} series, \ the last 6 values held out", font_size=24),
            label(r"60 simulated (stationary, \ random walks, \ trends) \ + \ Yule's two \ + \ the sunspots since 1900", font_size=20,
                  color=GREY_A),
        ), 12.4, 0.15, [0, 3.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> We can run a small competition of our own. Sixty-three series: sixty simulated, some "
            "stationary, some random walks, some with trends, plus Yule's two series and the sunspots since 1900. Hold out "
            "the last six values of each and forecast them five ways. <bookmark mark='b'/> The naive forecast, the last value "
            "carried forward. The drift method, which continues the average step. Simple exponential smoothing. An "
            "autoregression with its order chosen by AIC. And the plain average of the last three. "
            "<bookmark mark='c'/> On average scaled error, four of them are within two percent of each other. "
            "<bookmark mark='d'/> The combination comes first, about three percent better than its best component."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(A), LaggedStart(*[FadeIn(l_[0]) for l_ in labs], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(b_) for b_ in bars[:-1]], lag_ratio=0.2), *[FadeIn(l_[1]) for l_ in labs[:-1]])
            vo.wait_until("d")
            self.play(Create(bars[-1]), FadeIn(labs[-1][1]))
        self.clear_scene()

    def ranks(self):
        d = load("mcomp")
        mr, md = d["mean_rank"], d["median_mase"]
        tab = table_rows([
            [r"method", r"mean rank (1--5)", r"median MASE"],
            *[[NAMES[m], f"{mr[m]:.2f}", f"{md[m]:.2f}"] for m in d["methods"]],
        ], font_size=24, colors=[GREY_B, None, None, None, None, HIT]).move_to([0, 0.6, 0])
        foot = fit_rows(VGroup(
            label(r"the combination has the best average rank", font_size=22, color=HIT),
            label(r"by the median, \ drift wins: \ the ranking depends on the measure", font_size=22, color=OBS),
        ), 12.4, 0.2, [0, -2.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Rank the five methods on each series and average. The combination's mean rank is two point "
            "five nine; every single method is near three. It's rarely the best on any one series, but it's rarely bad. "
            "<bookmark mark='b'/> Judged by the median error instead, the drift method comes first. The competitions' second "
            "lesson, reproduced in miniature: the ranking depends on the measure."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def why_combine(self):
        rows = [
            cmath(r"\bar e", r"=", r"\tfrac12 (e_1 + e_2)", font_size=32),
            cmath(r"\mathrm{Var}(\bar e)", r"=", r"\tfrac14\big(\sigma_1^2 + \sigma_2^2 + 2\rho\,\sigma_1\sigma_2\big)", font_size=32),
            cmath(r"\sigma_1 = \sigma_2 = \sigma", r":", r"\sigma^2\,\frac{1 + \rho}{2} \le \sigma^2", font_size=32),
            cmath(r"\rho = 0.5", r":", r"\text{the combined error variance is } 0.75\,\sigma^2", font_size=30),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"average two forecasts' errors"), why(r"Part 5: \ the variance of a sum"),
                why(r"never worse, \ unless the errors are identical"), why(r"Bates \& Granger (1969): \ the combination of forecasts")]
        with self.voiceover(
            "Why does averaging work? <bookmark mark='a'/> Average two forecasts, and you average their errors. "
            "<bookmark mark='b'/> By Part 5, the variance of the average depends on how correlated the errors are. "
            "<bookmark mark='c'/> If the two methods are equally accurate, the combined variance is sigma squared times one "
            "plus rho over two, never more than either alone, and less whenever their errors aren't perfectly correlated. "
            "<bookmark mark='d'/> With a correlation of a half, a quarter of the error variance disappears. John Bates and Clive "
            "Granger made the case in 1969. Different methods make different mistakes, and averaging lets them cancel: the "
            "same principle as averaging observations, applied to opinions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rolling(self):
        n = 24
        cell = 0.4
        rows_ = VGroup()
        for k in range(5):
            row = VGroup()
            tr = 12 + 2 * k
            for i in range(n):
                col = SERIES if i < tr else (FC if i < tr + 2 else GREY_D)
                op = 0.85 if i < tr + 2 else 0.35
                row.add(Square(cell, stroke_width=1, stroke_color="#101418", fill_color=col, fill_opacity=op)
                        .move_to([(i - n / 2 + 0.5) * cell, 1.8 - 0.6 * k, 0]))
            rows_.add(row)
        key = VGroup(label(r"fit", font_size=22, color=SERIES), label(r"forecast and score", font_size=22, color=FC),
                     label(r"not yet seen", font_size=22, color=GREY_B)).arrange(RIGHT, buff=0.8).move_to([0, 2.8, 0])
        foot = fit_rows(VGroup(
            label(r"the origin rolls forward: \ every forecast uses only the past", font_size=24),
            label(r"Part 16's random folds would let the future leak into the fit", font_size=22, color=RES),
            label(r"the competitions' own method: \ hold out the end", font_size=22, color=OBS),
        ), 12.4, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "How should a method be chosen for a single series, without a competition? <bookmark mark='a'/> With "
            "cross-validation, adapted to time. Fit on the data up to some origin and score the forecasts of the next few "
            "values. <bookmark mark='b'/> Then roll the origin forward, refit, and score again, and average the scores. "
            "<bookmark mark='c'/> Every forecast uses only the past, as a real one would. Part 16's random folds would scatter "
            "future observations into the fitting set and flatter every method. <bookmark mark='d'/> Holding out the end of "
            "each series is exactly what the competitions did."
        ) as vo:
            self.play(FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows_[1:]], lag_ratio=0.4), run_time=2.5)
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k + (1 if k else 0)]) if k else AnimationGroup(FadeIn(foot[0]), FadeIn(foot[1])))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"judge forecasts on data held out, \ never on the fit", font_size=24),
            label(r"always compare with naive benchmarks: \ the last value, \ last year's value", font_size=24, color=OBS),
            label(r"models are tools: \ the best-fitting model is not always the best forecaster", font_size=24, color=SERIES),
            label(r"combine when unsure", font_size=24, color=HIT),
            label(r"intervals matter as much as point forecasts", font_size=24, color=FC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lessons for practice. Judge forecasts on data held out, never on the fit. "
            "<bookmark mark='b'/> Always compare with naive benchmarks: the last value, or last year's value. A method that "
            "can't beat them isn't worth its complexity. <bookmark mark='c'/> Models are tools, and the one that fits the past "
            "best isn't always the one that forecasts best. <bookmark mark='d'/> When unsure, combine. "
            "<bookmark mark='e'/> And report intervals, which the later competitions scored too: a forecast without its "
            "uncertainty invites false confidence."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
