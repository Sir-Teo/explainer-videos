from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class Honest(VoiceoverScene):
    def construct(self):
        self.card()
        self.plugin()
        self.cv()
        self.meuse_check()
        self.board()
        self.checklist()

    def card(self):
        card = chapter_card(14, r"Honest prediction", r"Do the intervals cover?", lit=(2023,), part=PART)
        with self.voiceover("Chapter fourteen. Honest prediction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def plugin(self):
        rows = [
            cmath(r"\text{kriging variance}", r":", r"\text{exact if the covariance is known}", font_size=30),
            cmath(r"\text{plug-in}", r":", r"\text{insert } \hat\theta, \ \text{ignore its uncertainty}", font_size=30),
            cmath(r"\text{fixes}", r":", r"\text{Bayesian (integrate over } \theta), \ \text{the parametric bootstrap}", font_size=30),
            cmath(r"\text{wrong family}", r":", r"\text{Stein: \ the predictions survive, \ the variances may not}", font_size=30),
        ]
        rows[1][-1].set_color(MISSC)
        whys = [why(r"Part 5's conditional variance"), why(r"Zimmerman \& Cressie (1992)"), why(r"Parts 16, \ 26"),
                why(r"misspecified smoothness")]
        with self.voiceover(
            "<bookmark mark='a'/> The kriging variance is exact when the covariance is known. <bookmark mark='b'/> In "
            "practice we plug in estimated parameters and ignore their uncertainty, which tends to make intervals too "
            "short, as Dale Zimmerman and Noel Cressie showed. <bookmark mark='c'/> A Bayesian analysis integrates over the "
            "parameters; a parametric bootstrap can correct the variance. <bookmark mark='d'/> And if the covariance family "
            "is wrong, Stein's theory says the predictions can survive, but the variances need not. Only coverage, measured, "
            "can tell."
        ) as vo:
            intro=label('Estimated covariance uncertainty is absent from plug-in kriging variance',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cv(self):
        d = load("blockcv")
        r, b = d["random"], d["block"]
        rows = [[r"kriging the World's 300 stations", r"RMSE", r"90\% PI coverage", r"median distance to training data"],
                [r"random 10-fold CV", f"{r['rmse']:.2f}", f"{100 * r['cover']:.0f}\\%", f"{r['nn']:.2f}"],
                [r"spatial blocks \ (a 3 $\times$ 3 grid)", f"{b['rmse']:.2f}", f"{100 * b['cover']:.0f}\\%", f"{b['nn']:.2f}"]]
        tab = table_rows(rows, font_size=24, col_buff=0.6, row_buff=0.34, colors=[GREY_A, FIELDC, TAUC]).move_to([0, 1.2, 0])
        if tab.width > 12.6:
            tab.width = 12.6
        foot = fit_rows(VGroup(
            label(r"random folds test interpolation; \ blocks test extrapolation into empty regions", font_size=24, color=GREY_A),
            label(r"variances reflect the fitted model; empirical coverage still requires checking", font_size=24, color=BANDC),
            label(r"choose the CV that matches where you will predict \ (Roberts et al.\ 2017)", font_size=24, color=TAUC),
        ), 12.4, 0.3, [0, -1.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> First, cross-validation. Fit the covariance and trend within each training fold, "
            "then predict held-out stations. With random ten-fold validation, kriging misses by "
            + say(r["rmse"], 2) + ". <bookmark mark='b'/> Hold out whole blocks of the island instead, and it misses by "
            + say(b["rmse"], 2) + ", because the held-out stations are farther from the training data, as the distance column shows. "
            "<bookmark mark='c'/> Random folds measure interpolation, blocks measure extrapolation. <bookmark "
            "mark='d'/> Kriging variance reflects distance under its fitted model, but this does not guarantee "
            "coverage. Read the empirical coverage separately for each design, allowing for dependent errors and "
            "estimated parameters. <bookmark mark='e'/> The lesson, from David Roberts and colleagues in ecology: "
            "choose the cross-validation that matches the distances at which you will actually predict."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k]))
        self.clear_scene()

    def board(self):
        rows = board_rows("kriging", "OLS CI", "GLS")
        text = (
            "<bookmark mark='a'/> The Coverage Board averages over two hundred and fifty independent seeded fields, "
            "each with two hundred observations and fifty prediction sites. The true-covariance intervals cover "
            + say(100 * rows[0].achieved, 1) + " percent. <bookmark mark='b'/> The REML plug-in covers "
            + say(100 * rows[1].achieved, 1) + " percent, with a Monte Carlo standard error of "
            + say(100 * rows[1].se, 2) + " percentage points across fields. Its Board classification is "
            + rows[1].verdict + ". The fifty predictions within a field are correlated, so twelve thousand five "
            "hundred predictions are not that many independent studies. <bookmark mark='c'/> The fitted exponential "
            "model covers " + say(100 * rows[2].achieved, 1) + " percent in these smooth fields. Wrong covariance "
            "need not always make intervals conservative. <bookmark mark='d'/> For the regression slope, ordinary "
            "least squares covers " + say(100 * rows[3].achieved, 1) + " percent when it ignores spatial errors. "
            "<bookmark mark='e'/> Generalized least squares with REML covers " + say(100 * rows[4].achieved, 1) +
            " percent, classified " + rows[4].verdict + ". These simulation labels do not establish exact coverage "
            "or isolate covariance-estimation error from every finite-sample effect."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1]), ("c", [2]), ("d", [3]), ("e", [4])])

    def checklist(self):
        rows = fit_rows(VGroup(
            label(r"plot the data on a map, \ and the residuals' variogram", font_size=26, color=VARC),
            label(r"model the trend first; \ then the dependence", font_size=26, color=TAUC),
            label(r"Mat\'ern, \ with the smoothness checked; \ REML; \ do not trust $\hat\rho$ alone", font_size=26, color=FIELDC),
            label(r"report kriging standard errors, \ and check coverage by CV that matches the task", font_size=26, color=BANDC),
            label(r"a spatial random effect is not an adjustment for confounding", font_size=26, color=MISSC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A checklist for spatial data. Map the data, and look at the variogram of the residuals. "
            "<bookmark mark='b'/> Model the trend first, then the dependence. <bookmark mark='c'/> Use the Matérn family, "
            "check the smoothness, fit by REML, and do not read much into the range alone. <bookmark mark='d'/> Report "
            "prediction standard errors, and check their coverage with a cross-validation that matches the task. "
            "<bookmark mark='e'/> And remember that a spatial random effect is not an adjustment for confounding."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def meuse_check(self):
        d = load("extra")
        z = np.asarray(d["z"], float)
        lower = min(-3., float(np.floor(z.min()*2)/2))
        upper = max(4.5, float(np.ceil(z.max()*2)/2))
        edges = np.arange(lower, upper + .25, .5)
        h, _ = np.histogram(z, edges)
        dens = h / (len(z) * (edges[1] - edges[0]))
        A = axes([lower, upper], [0, max(.6, float(np.ceil(dens.max()*5)/5))], x_length=7.4, y_length=4.0, xlabel=r"leave-one-out $z$-score", ylabel=r"density",
                 xticks=[-3, -1.5, 0, 1.5, 3, 4.5], yticks=[0, 0.2, 0.4, 0.6], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, dens, FIELDC)
        xs = np.linspace(lower, upper, 200)
        nc = polyline(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), TRUEC, 3)
        side = fit_rows(VGroup(
            label(r"Meuse: trend and covariance refitted using only the other 154 samples", font_size=22),
            label(r"$z = (Z_i - \hat Z_{-i}) / \text{SE}$", font_size=22, color=FIELDC),
            label(rf"mean $z^2$: \ {d['mean_z2']:.2f} \ (ideal 1)", font_size=22, color=BANDC),
            label(rf"90\% intervals cover {100 * d['cover90']:.0f}\%: \ a little short", font_size=22, color=TAUC),
            label(r"the right tail: \ a few samples far richer than their neighbours", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real data allow the same check. Predict each Meuse sample from the other hundred "
            "and fifty-four, by universal kriging, <bookmark mark='b'/> and divide the error by the kriging standard "
            "error. With known Gaussian covariance the standardized prediction errors are marginally normal. Here "
            "covariance is estimated, so a normal histogram is a diagnostic, not an exact conditional guarantee. "
            "<bookmark mark='c'/> Their mean square is "
            + say(d["mean_z2"], 2) + ", close to one, <bookmark mark='d'/> but the ninety percent intervals cover "
            + str(round(100 * d["cover90"])) + " percent, a little short, <bookmark mark='e'/> because of a long right tail: a few samples much richer "
            "in zinc than anything near them, which a Gaussian field finds surprising. A heavier-tailed model or a "
            "new transformation might improve this, but must be fitted inside training folds and checked on fresh "
            "validation data."
        ) as vo:
            self.add(meuse_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars), Create(nc), FadeIn(side[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 2]))
        self.clear_scene()
