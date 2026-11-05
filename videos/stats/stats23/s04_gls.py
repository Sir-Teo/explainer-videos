from __future__ import annotations

import numpy as np

from videos.stats.stats23.common import *  # noqa: F403


class GLS(VoiceoverScene):
    def construct(self):
        self.card()
        self.aitken()
        self.wls()
        self.series()
        self.spreads()
        self.coverage()
        self.durbin()
        self.feasible()

    def card(self):
        card = chapter_card(3, r"GLS and Aitken", r"When the errors have a shape", lit=(1935,), part=PART)
        with self.voiceover("Chapter three. Generalized least squares."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def aitken(self):
        rows = [
            cmath(r"\mathrm{Var}(\varepsilon)", r"=", r"\sigma^2 \Omega, \ \ \Omega = LL^\top \ \text{known}", font_size=30),
            cmath(r"L^{-1} y", r"=", r"L^{-1} X \beta + L^{-1}\varepsilon, \ \ \mathrm{Var}(L^{-1}\varepsilon) = \sigma^2 I", font_size=28),
            cmath(r"\hat\beta_{\mathrm{GLS}}", r"=", r"(X^\top \Omega^{-1} X)^{-1} X^\top \Omega^{-1} y", font_size=30),
            cmath(r"\text{Aitken (1935)}", r":", r"\hat\beta_{\mathrm{GLS}} \ \text{is BLUE}", font_size=30),
        ]
        rows[2][2].set_color(GLS_C)
        whys = [why(r"correlated or unequal errors, \ of known shape"), why(r"whiten: \ Cholesky (Part 4)"),
                why(r"OLS on the whitened data"), why(r"Gauss--Markov, \ in the whitened world")]
        with self.voiceover(
            "<bookmark mark='a'/> Suppose the errors' covariance is sigma squared times a known matrix omega, with Cholesky "
            "factor L. <bookmark mark='b'/> Multiply the whole model by L inverse: the new errors have covariance sigma "
            "squared times the identity, so they satisfy Part 12's assumptions. <bookmark mark='c'/> Least squares on the "
            "whitened data is generalized least squares, which weights the data by omega inverse. <bookmark mark='d'/> "
            "Alexander Aitken proved in 1935 that it is the best linear unbiased estimator: Gauss–Markov, applied after "
            "whitening. Weighted least squares, from Part 12, is the special case of a diagonal omega."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def wls(self):
        rows = [
            cmath(r"\Omega", r"=", r"\mathrm{diag}(1/m_1, \dots, 1/m_G)", font_size=30),
            cmath(r"\hat\beta_{\mathrm{WLS}}", r"=", r"\arg\min \textstyle\sum_g m_g (\bar y_g - x_g^\top b)^2", font_size=30),
            cmath(r"\text{equal to}", r":", r"\text{OLS on the individual data, \ if } x \text{ is constant within groups}", font_size=28),
            cmath(r"\text{wrong weights}", r":", r"\text{still unbiased; \ less efficient; \ SE wrong}", font_size=30),
        ]
        rows[1][2].set_color(GLS_C)
        whys = [why(r"group means of $m_g$ observations"), why(r"weighted least squares: \ Part 12"),
                why(r"averaging first loses nothing"), why(r"the theme of the next two chapters")]
        with self.voiceover(
            "<bookmark mark='a'/> The simplest case is a diagonal omega. Suppose the data are group averages, the g-th of m "
            "g observations, so its variance is sigma squared over m g. <bookmark mark='b'/> GLS then weights each average "
            "by its group size: weighted least squares. <bookmark mark='c'/> If the predictors are the same within each "
            "group, this gives exactly the least squares fit to the individual data: averaging first loses nothing. "
            "<bookmark mark='d'/> With the wrong weights the estimate stays unbiased, merely less efficient, but the standard "
            "error printed from the wrong weights is wrong. Remember that pattern."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def series(self):
        d = load("gls")
        t, y = np.asarray(d["t"]), np.asarray(d["y"])
        A = axes([0, 1], [float(np.floor(y.min() - 1)), float(np.ceil(y.max() + 1))], x_length=8.0, y_length=4.2,
                 xlabel=r"time", ylabel=r"$y$", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[], center=[-1.6, 0.3, 0])
        ax = A.ax
        pts = polyline(ax, t, y, GREY_B, 2)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=GREY_A) for a, b in zip(t, y)])
        truth = Line(ax.c2p(0, 10), ax.c2p(1, 12), color=TRUE, stroke_width=3)
        a, b = d["ols_line"]
        fit = Line(ax.c2p(0, a), ax.c2p(1, a + b), color=OLS_C, stroke_width=3)
        rows = fit_rows(VGroup(
            label(rf"$n = {d['n']}$; \ errors AR(1), \ $\rho = {d['rho']}$", font_size=22),
            label(r"gold: \ the true trend, \ slope 2", font_size=22, color=TRUE),
            label(rf"blue: \ this series' OLS line, \ slope {b:.2f}", font_size=22, color=OLS_C),
            label(r"long runs above, \ then below: \ correlated errors", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A common case: a trend measured over time, sixty points, with errors that follow an "
            "autoregression, each one point eight times the previous plus fresh noise. <bookmark mark='b'/> The true trend "
            "has slope two. <bookmark mark='c'/> This particular series' least squares line has slope one point four "
            "eight. <bookmark mark='d'/> The errors wander in long runs above and below the trend, so sixty points carry much "
            "less information than sixty independent ones."
        ) as vo:
            self.play(FadeIn(A), Create(pts), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def spreads(self):
        d = load("gls")
        hdr = [r"\textbf{estimator}", r"\textbf{SD of the slope}", r"\textbf{relative}"]
        body = [[r"OLS", f"{d['sd_ols']:.2f}", "1.00"],
                [r"GLS, \ $\rho$ known", f"{d['sd_gls']:.2f}", f"{d['sd_gls'] / d['sd_ols']:.2f}"],
                [r"Prais--Winsten, \ $\rho$ estimated", f"{d['sd_pw']:.2f}", f"{d['sd_pw'] / d['sd_ols']:.2f}"],
                [r"OLS's own (naive) SE, \ on average", f"{d['mean_naive_se']:.2f}", f"{d['mean_naive_se'] / d['sd_ols']:.2f}"]]
        t = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, OLS_C, GLS_C, GLS_C, RES])
        t.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"{d['R']:,} series", font_size=22, color=GREY_B),
            label(r"for a trend, \ OLS is nearly as good as GLS: \ Grenander \& Rosenblatt (1957)", font_size=24, color=HIT),
            label(r"but OLS's formula SE is three times too small", font_size=24, color=RES),
        ), 12.0, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two thousand such series. The least squares slope varies with a standard deviation of about "
            "two. <bookmark mark='b'/> Generalized least squares, using the true correlation, does a little better, one "
            "point eight seven. <bookmark mark='c'/> Prais and Winsten's feasible version, which estimates the correlation "
            "first, is almost as good. <bookmark mark='d'/> For estimating a trend, least squares is nearly efficient, as "
            "Ulf Grenander and Murray Rosenblatt showed in 1957. <bookmark mark='e'/> The real damage is elsewhere: the "
            "standard error least squares reports, which assumes independent errors, averages point six five, a third of the "
            "truth."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(t[0]), FadeIn(t[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(t[2]))
            vo.wait_until("c")
            self.play(FadeIn(t[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
            vo.wait_until("e")
            self.play(FadeIn(t[4]), FadeIn(foot[2]))
        self.clear_scene()

    def coverage(self):
        d = load("gls")
        c = d["coverage"]
        items = [(r"OLS, \ naive SE", c["ols"], RES), (r"OLS, \ Newey--West SE", c["nw"], OLS_C),
                 (r"Prais--Winsten FGLS", c["pw"], GLS_C), (r"GLS, \ $\rho$ known", c["gls"], HIT)]
        A = axes([0.4, 1.0], [0, 4.6], x_length=8.0, y_length=3.8, xlabel=r"coverage of the 95\% interval for the slope",
                 xticks=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[], center=[0.6, 0.2, 0], xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        nom = DashedLine(ax.c2p(0.95, 0), ax.c2p(0.95, 4.6), color=TRUE, stroke_width=2.5)
        bars, labs = VGroup(), VGroup()
        for k, (name, v, col) in enumerate(items):
            y = 4 - k
            bars.add(Line(ax.c2p(0.4, y), ax.c2p(v, y), color=col, stroke_width=14))
            labs.add(VGroup(label(name, font_size=22, color=col).next_to(ax.c2p(0.4, y), LEFT, buff=0.25),
                            label(rf"{100 * v:.1f}\%", font_size=22, color=col).next_to(ax.c2p(v, y), RIGHT, buff=0.15)))
        with self.voiceover(
            "<bookmark mark='a'/> Coverage of nominal ninety-five percent intervals for the slope. <bookmark mark='b'/> With "
            "the naive standard error: forty-eight percent. <bookmark mark='c'/> Newey and West's autocorrelation-consistent "
            "standard error, from Part 17, helps but reaches only sixty-eight with sixty strongly correlated points. "
            "<bookmark mark='d'/> Feasible GLS reaches eighty-four. <bookmark mark='e'/> Only GLS with the true correlation "
            "is honest. Strong dependence and short series are a hard combination; there's no free lunch in estimating the "
            "error structure."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]))
        self.clear_scene()

    def durbin(self):
        d = load("gls")
        rows = [
            cmath(r"DW", r"=", r"\dfrac{\sum_t (e_t - e_{t-1})^2}{\sum_t e_t^2} \approx 2(1 - \hat\rho)", font_size=30),
            cmath(r"\hat\rho", r"=", r"\textstyle\sum e_t e_{t-1} / \sum e_{t-1}^2", font_size=30),
            cmath(r"\text{our series}", r":", rf"\hat\rho = {d['rho_hat_example']:.2f}, \ DW \approx {2 * (1 - d['rho_hat_example']):.2f}", font_size=30),
            cmath(r"\text{Cochrane--Orcutt}", r":", r"\text{difference out } \hat\rho, \ \text{refit, \ repeat}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Durbin \& Watson (1950)"), why(r"the residuals' lag-one correlation"),
                why(r"2 means no correlation; \ near 0, \ strong"), why(r"1949; \ Prais--Winsten keeps the first point")]
        with self.voiceover(
            "<bookmark mark='a'/> How would we have known? James Durbin and Geoffrey Watson's 1950 statistic compares "
            "successive residuals; it is about two times one minus the residuals' lag-one correlation. "
            "<bookmark mark='b'/> That correlation is estimated directly from the residuals. <bookmark mark='c'/> For our "
            "example series it is point eight two, so the Durbin–Watson statistic is about point three six, far below the "
            "value of two that independent errors would give. <bookmark mark='d'/> Donald Cochrane and Guy Orcutt's 1949 "
            "recipe then differences out the estimated correlation and refits, repeating until it settles; Prais and "
            "Winsten's version keeps the first observation instead of dropping it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def feasible(self):
        rows = [
            cmath(r"\text{FGLS}", r":", r"\text{estimate } \Omega(\hat\theta), \ \text{then GLS}", font_size=30),
            cmath(r"\text{asymptotically}", r":", r"\text{as good as GLS with the true } \Omega", font_size=30),
            cmath(r"\text{in practice}", r":", r"\text{OLS with a robust SE, \ or GLS with a robust SE}", font_size=28),
            cmath(r"\text{the lesson}", r":", r"\text{efficiency is cheap; \ honest SEs are not}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"e.g. Cochrane--Orcutt, \ Prais--Winsten (1954)"), why(r"if $\hat\theta$ is consistent"),
                why(r"in case $\Omega$'s shape is wrong"), why(r"the rest of this part")]
        with self.voiceover(
            "<bookmark mark='a'/> In practice omega is unknown, so feasible GLS estimates its parameters first, here the "
            "autocorrelation, and then whitens with the estimate. <bookmark mark='b'/> In large samples that's as good as "
            "knowing omega. <bookmark mark='c'/> Since the assumed shape may itself be wrong, the modern habit is to pair "
            "either estimator with a standard error that doesn't trust the shape. <bookmark mark='d'/> The lesson carries "
            "through the whole part: getting a nearly efficient estimate is easy; getting an honest standard error is the "
            "hard part."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
