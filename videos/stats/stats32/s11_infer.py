from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats32.common import *  # noqa: F403

DEB = S.KEPT  # debiased: green
NAIVE = S.RESID  # naive: red


class Inference(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_fails()
        self.one_data()
        self.winners()
        self.debias()
        self.nodewise()
        self.histos()
        self.double_def()
        self.double_num()
        self.board()
        self.posi()

    def card(self):
        card = chapter_card(10, r"Inference after the lasso", r"Confidence intervals for selected coefficients", lit=(2014,), part=PART)
        with self.voiceover("Chapter ten. Inference after the lasso."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def why_fails(self):
        rows = [
            cmath(r"\text{naive}", r":", r"\text{select with the lasso, \ refit by OLS, \ report } t\text{-intervals}", font_size=28),
            cmath(r"\text{selected}", r"\Leftarrow", r"|\hat\beta_j| \text{ happened to be large}", font_size=30),
            cmath(r"E(\hat\beta_j \mid \text{selected})", r">", r"\beta_j: \ \text{the winner's curse}", font_size=30),
            cmath(r"\text{noise variables}", r":", r"\text{selected for looking real, \ so their intervals exclude } 0", font_size=28),
        ]
        rows[2][-1].set_color(RES)
        whys = [why(r"what most analyses do"), why(r"the data chose the model"), why(r"selection bias"),
                why(r"false positives with false confidence")]
        with self.voiceover(
            "<bookmark mark='a'/> The most common practice after a lasso is to take the selected variables, refit them by "
            "least squares, and report the usual t-intervals, as if the model had been chosen in advance. "
            "<bookmark mark='b'/> But a variable is selected precisely when its estimate happened to look large. "
            "<bookmark mark='c'/> So, given that it was selected, its estimate is biased away from zero: the winner's curse "
            "of Part 33. <bookmark mark='d'/> Worst of all, noise variables are selected exactly when they look real, so their "
            "intervals usually exclude zero, the true value."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def one_data(self):
        d = load("infer")
        beta, deb = np.asarray(d["beta"]), d["deb"]
        sel = list(d["selected"])
        nv = d["naive"]
        A = axes([0.3, 8.7], [-0.5, 1.5], x_length=8.0, y_length=4.4, xlabel=r"coefficient $j$", ylabel=r"estimate and 95\% interval",
                 xticks=list(range(1, 9)), yticks=[0, 0.5, 1], center=[-1.8, 0.2, 0])
        ax = A.ax
        tr = VGroup(*[Line(ax.c2p(j + 0.7, beta[j]), ax.c2p(j + 1.3, beta[j]), color=SPIKE, stroke_width=4) for j in range(8)])
        zero = DashedLine(ax.c2p(0.3, 0), ax.c2p(8.7, 0), color=GREY_D, stroke_width=1.5)
        nvb = VGroup()
        for k, j in enumerate(sel):
            if j < 8:
                nvb.add(VGroup(Line(ax.c2p(j + 0.85, nv["lo"][k]), ax.c2p(j + 0.85, nv["hi"][k]), color=NAIVE, stroke_width=3),
                               Dot(ax.c2p(j + 0.85, nv["b"][k]), radius=0.06, color=NAIVE)))
        dbb = VGroup(*[VGroup(Line(ax.c2p(j + 1.15, deb[j]["lo"]), ax.c2p(j + 1.15, deb[j]["hi"]), color=DEB, stroke_width=3),
                              Dot(ax.c2p(j + 1.15, deb[j]["b"]), radius=0.06, color=DEB)) for j in range(8)])
        rows = fit_rows(VGroup(
            label(r"$n = 100$, \ $p = 200$", font_size=22),
            label(r"gold: \ the truth", font_size=22, color=SPIKE),
            label(rf"red: \ lasso keeps {len(sel)}, \ then OLS on those", font_size=22, color=NAIVE),
            label(r"green: \ the debiased lasso, \ for every coefficient", font_size=22, color=DEB),
        ), 3.6, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One data set: a hundred observations, two hundred predictors, true effects of one, one, a "
            "half, a half, a quarter and a quarter, and zeros elsewhere. The first eight coefficients are shown. "
            "<bookmark mark='b'/> The truth in gold. <bookmark mark='c'/> The lasso, at the standard theoretical lambda, "
            "keeps only the four strongest; least squares on those gives the red intervals, and says nothing about the "
            "rest. <bookmark mark='d'/> The debiased lasso, next, gives an estimate and interval for every coefficient, in "
            "green, selected or not."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(nvb), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(dbb), FadeIn(rows[3]))
        self.clear_scene()

    def winners(self):
        b = load("board")
        hdr = [r"\textbf{1,000 data sets}", r"\textbf{value}"]
        body = [[r"variables selected per data set", f"{b['per_rep_selected']:.1f}"],
                [r"naive intervals covering the truth, \ all selected", f"{100 * b['pooled']:.0f}\\%"],
                [r"\quad of which false positives", f"{100 * b['fp_cov']:.0f}\\%"],
                [r"the 0.25 effect: \ selected", f"{b['naive_sel'] / b['reps'] * 100:.0f}\\% of the time"],
                [r"\quad its mean estimate when selected", f"{b['naive_mean']:.2f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.2, row_buff=0.3, colors=[GREY_A, None, NAIVE, NAIVE, None, SPIKE])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"a false positive's naive interval covers 0 only a quarter of the time", font_size=22, color=NAIVE),
            label(r"a weak effect is reported only when it looks a third larger than it is", font_size=22, color=SPIKE),
        ), 12.0, 0.22, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over a thousand data sets, the lasso selects about five and a half variables. Of all the "
            "naive intervals reported, only seventy-five percent cover the truth, against a promised ninety-five. "
            "<bookmark mark='b'/> For the false positives, a quarter. <bookmark mark='c'/> The weak effect of a quarter is "
            "selected only twenty-three percent of the time, and when it is, its estimate averages point three four: the "
            "winner's curse in action."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1:3]))
            vo.wait_until("b")
            self.play(FadeIn(tb[3]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(tb[4:]), FadeIn(foot[1]))
        self.clear_scene()

    def debias(self):
        rows = [
            cmath(r"\hat b_j", r"=", r"\hat\beta_j + \hat\theta_j^\top \tfrac1n X^\top (y - X\hat\beta)", font_size=32),
            cmath(r"\hat\theta_j", r"\approx", r"\text{row } j \text{ of } \Sigma^{-1}", font_size=32),
            cmath(r"\sqrt n(\hat b_j - \beta_j)", r"=", r"\underbrace{\hat\theta_j^\top X^\top \varepsilon/\sqrt n}_{\text{normal}} + \underbrace{\Delta_j}_{\to\, 0}", font_size=28),
            cmath(r"\text{needs}", r":", r"s \log p / \sqrt n \to 0", font_size=30),
        ]
        rows[0][-1].set_color(DEB)
        whys = [why(r"one Newton-like step from the lasso"), why(r"an approximate inverse"),
                why(r"van de Geer et al.; \ Zhang \& Zhang (2014)"), why(r"sparser than estimation needs")]
        with self.voiceover(
            "<bookmark mark='a'/> The debiased lasso adds back what the penalty took away. Take the lasso estimate and add a "
            "correction: an approximate inverse of the covariance applied to the correlation of X with the lasso residuals. "
            "<bookmark mark='b'/> If theta were the exact inverse, this would be one Newton step from the lasso to least "
            "squares. <bookmark mark='c'/> The result, scaled by root n, is a normal term plus a remainder that vanishes, as "
            "shown independently by Sara van de Geer, Peter Bühlmann, Ya'acov Ritov and Ruben Dezeure, and by Cun-Hui and "
            "Stephanie Zhang, and by Adel Javanmard and Andrea Montanari. <bookmark mark='d'/> The price: the true model must "
            "be sparser than for estimation alone, s log p over root n going to zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nodewise(self):
        rows = [
            cmath(r"\hat\gamma_j", r"=", r"\text{lasso of } x_j \text{ on } X_{-j}", font_size=32),
            cmath(r"\hat\tau_j^2", r"=", r"\tfrac1n\|x_j - X_{-j}\hat\gamma_j\|^2 + \lambda_j\|\hat\gamma_j\|_1", font_size=30),
            cmath(r"\hat\theta_j", r"=", r"(\ldots, -\hat\gamma_j, 1, \ldots)/\hat\tau_j^2", font_size=32),
            cmath(r"\widehat{\mathrm{se}}(\hat b_j)", r"=", r"\hat\sigma\sqrt{\hat\theta_j^\top \hat\Sigma \hat\theta_j / n}", font_size=30),
        ]
        rows[3][-1].set_color(DEB)
        whys = [why(r"nodewise regression: \ chapter nine of Part 31"), why(r"the residual variance"),
                why(r"$\theta_{jj} = 1/\tau_j^2$, \ off-diagonals $-\gamma_j/\tau_j^2$"), why(r"a standard error")]
        with self.voiceover(
            "<bookmark mark='a'/> Where does the approximate inverse come from? From Part 31's neighbourhood regression: a "
            "lasso of x j on all the other columns. <bookmark mark='b'/> Its residual variance, plus a penalty term, is tau j "
            "squared. <bookmark mark='c'/> Then row j of the inverse covariance is one over tau squared on the diagonal and "
            "minus the coefficients over tau squared elsewhere, the formula Part 31 used for graphs. "
            "<bookmark mark='d'/> The standard error follows from the variance of the normal term."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def histos(self):
        b = load("board")
        db, nv = np.asarray(b["deb_draws"]), np.asarray(b["naive_draws"])
        A = axes([-0.3, 0.9], [0, 7.0], x_length=8.0, y_length=4.4, xlabel=r"estimate of $\beta_j = 0.25$", ylabel=r"density",
                 xticks=[-0.25, 0, 0.25, 0.5, 0.75], yticks=[0, 2, 4, 6], center=[-1.6, 0.3, 0])
        ax = A.ax
        edges = np.linspace(-0.3, 0.9, 41)
        w = edges[1] - edges[0]
        hd = hist_bars(ax, edges, np.histogram(db, edges)[0] / (len(db) * w), color=DEB, opacity=0.6)
        hn = hist_bars(ax, edges, np.histogram(nv, edges)[0] / (len(db) * w), color=NAIVE, opacity=0.75)
        tline = DashedLine(ax.c2p(0.25, 0), ax.c2p(0.25, 6.8), color=SPIKE, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"green: \ debiased estimates, \ all 1,000", font_size=22, color=DEB),
            label(rf"centred at {b['deb_mean']:.2f}; \ intervals cover {100 * b['deb_cov']:.1f}\%", font_size=22, color=DEB),
            label(rf"red: \ naive estimates, \ only the {b['naive_sel']} selected", font_size=22, color=NAIVE),
            label(rf"centred at {b['naive_mean']:.2f}: \ cut off below", font_size=22, color=NAIVE),
        ), 3.6, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For the weak effect of a quarter, the debiased estimates from all thousand data sets form "
            "a normal histogram, <bookmark mark='b'/> centred at point two four, and their intervals cover ninety-five and a "
            "half percent of the time. <bookmark mark='c'/> The naive estimates exist only for the two hundred and thirty-one "
            "data sets where the lasso selected the variable, <bookmark mark='d'/> and their histogram is chopped off below: "
            "selection keeps only the lucky draws."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(tline))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in hd], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in hn], lag_ratio=0.02), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def double_def(self):
        rows = [
            cmath(r"y", r"=", r"\alpha d + X\beta + \varepsilon, \ \ d = X\gamma + v", font_size=32),
            cmath(r"\text{single selection}", r":", r"\text{lasso } y \text{ on } (d, X): \ \text{drops controls with small } \beta_j", font_size=28),
            cmath(r"\text{bias}", r"\approx", r"\text{omitted } \beta_j \times \text{their } \gamma_j\text{-driven correlation with } d", font_size=28),
            cmath(r"\text{double selection}", r":", r"\text{lasso } y \text{ on } X, \ \text{lasso } d \text{ on } X, \ \text{OLS on the union}", font_size=28),
        ]
        rows[3][-1].set_color(DEB)
        whys = [why(r"a treatment effect with many possible confounders"), why(r"$d$ absorbs their effect"),
                why(r"omitted-variable bias, \ Part 23"), why(r"Belloni, \ Chernozhukov \& Hansen (2014)")]
        with self.voiceover(
            "<bookmark mark='a'/> A related problem in causal work. We want the effect alpha of a treatment d, with many "
            "possible confounders X that affect both the treatment and the outcome. <bookmark mark='b'/> A lasso of the "
            "outcome on the treatment and the controls tends to drop confounders whose direct effect on the outcome is "
            "small, because the treatment, correlated with them, absorbs their effect. <bookmark mark='c'/> The result is "
            "Part 23's omitted-variable bias. <bookmark mark='d'/> Alexandre Belloni, Victor Chernozhukov and Christian "
            "Hansen's double selection runs two lassos, the outcome on the controls and the treatment on the controls, and "
            "keeps the union: any variable that predicts either one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def double_num(self):
        b = load("board")
        hdr = [r"\textbf{$\alpha = 0.5$, \ 1,000 data sets}", r"\textbf{mean estimate}", r"\textbf{controls kept}", r"\textbf{95\% CI covers}"]
        body = [[r"single selection", f"{b['ss_mean']:.2f}", f"{b['ss_k']:.2f}", f"{100 * b['ss_cov']:.1f}\\%"],
                [r"double selection", f"{b['ds_mean']:.2f}", f"{b['ds_k']:.1f}", f"{100 * b['ds_cov']:.1f}\\%"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.35, colors=[GREY_A, NAIVE, DEB])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"$n = 100$, \ $p = 100$; \ five confounders with $\gamma_j = 0.6$ on $d$ and $\beta_j = 0.2$ on $y$", font_size=22),
            label(r"single selection keeps almost no controls: \ the treatment soaks up their effect", font_size=22, color=NAIVE),
            label(r"double selection finds them through the treatment equation", font_size=22, color=DEB),
        ), 12.0, 0.22, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulation with five confounders, each moving the treatment by point six and the "
            "outcome directly by point two, among a hundred candidate controls. <bookmark mark='b'/> Single selection keeps "
            "almost no controls, point one five on average. Its estimate averages point seven one instead of point "
            "five, and its intervals cover nine percent of the time. <bookmark mark='c'/> Double selection finds the "
            "confounders through the treatment equation, estimates point four nine, and covers ninety-four percent. Part 36's "
            "double machine learning generalizes the idea."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(tb[2]), FadeIn(foot[2]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=32) if r.part == 32]
        b = coverage_board(rows, lit_part=32, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> On the Board. Naive post-lasso intervals: broken, seventy-five percent. "
            "<bookmark mark='b'/> The debiased lasso: kept, for the weak effect and for a null coefficient alike. "
            "<bookmark mark='c'/> Single selection: broken, nine percent. Double selection: kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]), FadeIn(b.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[3]), FadeIn(b.body[4]))
        self.wait(1.0)
        self.clear_scene()

    def posi(self):
        rows = fit_rows(VGroup(
            label(r"two targets: \ the true $\beta_j$, \ or the coefficient in the selected model", font_size=24),
            label(r"debiasing aims at the true $\beta_j$, \ assuming sparsity", font_size=24, color=DEB),
            label(r"PoSI (Berk et al. 2013) and selective inference (Lee et al. 2016) aim at the selected model, \ with no sparsity", font_size=24, color=SPIKE),
            label(r"both, \ and their costs: \ Part 56", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One subtlety remains: which target? The true coefficient in the full model, or the "
            "coefficient of a variable in whatever model was selected? <bookmark mark='b'/> Debiasing aims at the true "
            "coefficient and relies on sparsity. <bookmark mark='c'/> Richard Berk and colleagues' post-selection inference, "
            "and Jason Lee and colleagues' exact selective inference, aim at the selected model's coefficients and need no "
            "sparsity, at the price of wider intervals. <bookmark mark='d'/> Part 56 develops both."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
