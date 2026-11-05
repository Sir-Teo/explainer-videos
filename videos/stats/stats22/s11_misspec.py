from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats22.common import *  # noqa: F403


class Misspecification(VoiceoverScene):
    def construct(self):
        self.card()
        self.target()
        self.incomes()
        self.sandwich()
        self.practice()
        self.counts()
        self.board()

    def card(self):
        card = chapter_card(10, r"Misspecification", r"What the MLE estimates when the model is wrong", lit=(1967,), part=PART)
        with self.voiceover("Chapter ten. Misspecification: what happens when the model is wrong, as every model is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def target(self):
        rows = [
            cmath(r"\tfrac1n \ell_n(\theta)", r"\to", r"E_g \log f(X;\theta)", font_size=30),
            cmath(r"", r"=", r"-\mathrm{KL}(g \,\|\, f_\theta) + E_g \log g(X)", font_size=30),
            cmath(r"\hat\theta", r"\to", r"\theta^* = \arg\min_\theta \mathrm{KL}(g \,\|\, f_\theta)", font_size=30),
            cmath(r"\text{if } g = f_{\theta_0}", r":", r"\theta^* = \theta_0, \ \ \text{chapter two again}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"$g$: \ the true distribution, \ not in the model"), why(r"the second term does not involve $\theta$"),
                why(r"the KL projection of the truth onto the model"), why(r"a true model is the special case")]
        with self.voiceover(
            "Suppose the data really come from some distribution g that isn't in our model at all. "
            "<bookmark mark='a'/> The average log likelihood still converges, by the law of large numbers, to the expected "
            "log density under the truth. <bookmark mark='b'/> That's minus the Kullback–Leibler divergence from the truth to "
            "the model, plus a term that doesn't depend on theta. <bookmark mark='c'/> So the maximum likelihood estimate "
            "converges to theta star, the member of the model closest to the truth in Kullback–Leibler divergence: the "
            "truth's projection onto the model. <bookmark mark='d'/> When the model is right, the projection is the truth "
            "itself, and chapter two's consistency is the special case."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def incomes(self):
        d = load("kl")
        e, h = np.asarray(d["edges"]), np.asarray(d["hist"])
        gr, dn = np.asarray(d["grid"]), np.asarray(d["dens"])
        ticks = [np.log(v) for v in (10_000, 30_000, 100_000, 300_000, 1_000_000)]
        A = axes([e[0], e[-1]], [0, 0.75], x_length=8.0, y_length=4.4, xlabel=r"income, \ log scale", ylabel=r"density of log income",
                 xticks=ticks, yticks=[0, 0.25, 0.5, 0.75], center=[-1.6, 0.3, 0],
                 xfmt=lambda v: {10: r"10\mathrm{k}", 30: r"30\mathrm{k}", 100: r"100\mathrm{k}", 300: r"300\mathrm{k}",
                                 1000: r"1\mathrm{M}"}[int(round(np.exp(v) / 1000))])
        ax = A.ax
        bars = hist_bars(ax, e, h, color=REAL, opacity=0.6)
        fit = curve(ax, gr, dn, PATH, 3.5)
        cut = DashedLine(ax.c2p(np.log(300_000), 0), ax.c2p(np.log(300_000), 0.6), color=RES, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"5,000 of the World's adult incomes", font_size=22, color=REAL),
            VGroup(label(r"gold: \ the best log-normal", font_size=22, color=PATH),
                   label(rf"$\mu = {d['mu']:.2f}$, \ $\sigma = {d['sd']:.2f}$", font_size=22, color=PATH)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            label(rf"median: \ fit {np.exp(d['mu']) / 1000:.1f}k, \ truth {d['true_median'] / 1000:.1f}k", font_size=22),
            label(rf"mean: \ fit {d['implied_mean'] / 1000:.1f}k, \ truth {d['true_mean'] / 1000:.1f}k", font_size=22),
            label(rf"over 300k: \ fit {100 * d['tail_model']:.2f}\%, \ truth {100 * d['tail_true']:.2f}\%", font_size=22, color=RES),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's a model that's wrong in an instructive way. Five thousand of the World's adult incomes, "
            "on a log scale. <bookmark mark='b'/> Fit a log-normal by maximum likelihood: a normal curve for log income. It "
            "looks reasonable. <bookmark mark='c'/> The median comes out right, within a hundred. <bookmark mark='d'/> The "
            "mean is a little low. <bookmark mark='e'/> But the World's incomes have a heavier upper tail than any log-normal: "
            "the fit says point oh seven percent of adults earn over three hundred thousand, and the truth is point three two "
            "percent, more than four times as many. The projection gets right what most of the data are about and wrong what "
            "few of them are about."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(cut), FadeIn(rows[4]))
        self.clear_scene()

    def sandwich(self):
        rows = [
            cmath(r"\sqrt n(\hat\theta - \theta^*)", r"\approx", r"A^{-1}\, U_n(\theta^*)/\sqrt n", font_size=30),
            cmath(r"A = -E_g \nabla^2 \log f, \ \ B", r"=", r"\mathrm{Var}_g\, \nabla \log f", font_size=30),
            cmath(r"\sqrt n(\hat\theta - \theta^*)", r"\to", r"N\big(0, \ A^{-1} B A^{-1}\big)", font_size=30),
            cmath(r"\text{model true}", r":", r"A = B, \ \ A^{-1}BA^{-1} = A^{-1} = I^{-1}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"chapter three's expansion, \ around $\theta^*$"), why(r"two different matrices now"),
                why(r"bread, \ meat, \ bread: \ the sandwich"), why(r"the information identity of chapter one")]
        with self.voiceover(
            "And the uncertainty? <bookmark mark='a'/> Chapter three's expansion still works, around theta star instead of "
            "the truth. <bookmark mark='b'/> But now two different matrices appear: A, the expected curvature, and B, the "
            "variance of the score, both computed under the true distribution. <bookmark mark='c'/> The estimate is "
            "approximately normal with covariance A inverse, B, A inverse: bread, meat, bread, the sandwich. Peter Huber "
            "derived it in 1967; Friedhelm Eicker had the regression case in 1963 and Halbert White brought it to economics "
            "in 1980. <bookmark mark='d'/> If the model is true, the information identity of chapter one says A equals B, the "
            "sandwich collapses to the inverse information, and we're back to the usual answer. Estimate A and B by their "
            "sample averages and you have standard errors that don't trust the model."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def practice(self):
        rows = [
            cmath(r"\hat A", r"=", r"-\tfrac1n \textstyle\sum_i \nabla^2 \log f(x_i;\hat\theta)", font_size=30),
            cmath(r"\hat B", r"=", r"\tfrac1n \textstyle\sum_i U_i U_i^{\top}, \ \ U_i = \nabla \log f(x_i;\hat\theta)", font_size=30),
            cmath(r"\widehat{\mathrm{Cov}}(\hat\theta)", r"=", r"\tfrac1n \hat A^{-1} \hat B \hat A^{-1}", font_size=30),
            cmath(r"\text{clusters}", r":", r"\hat B = \tfrac1n \textstyle\sum_g \big(\sum_{i \in g} U_i\big)\big(\sum_{i \in g} U_i\big)^{\top}", font_size=28),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"the observed information, \ per observation"), why(r"each observation's own score, \ squared"),
                why(r"least squares: \ HC0, \ Part 12's robust SEs"), why(r"sum scores within a cluster first: \ Part 23")]
        with self.voiceover(
            "<bookmark mark='a'/> In practice both matrices come from the fitted model. The bread is the observed information, "
            "averaged over observations. <bookmark mark='b'/> The meat is the average outer product of each observation's own "
            "score: it measures how much the scores actually vary, whatever the model claims. <bookmark mark='c'/> Combine "
            "them and divide by n. For least squares this is exactly the heteroskedasticity-robust covariance of Part 12, "
            "White's HC zero. <bookmark mark='d'/> If observations come in correlated clusters, add up the scores within each "
            "cluster before squaring: the cluster-robust sandwich, which Part 23 examines when there are few clusters."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def counts(self):
        d = load("sandwich")
        yh = np.asarray(d["y_hist"], float)
        n = 400
        A = axes([-0.5, 14.5], [0, 130], x_length=6.6, y_length=4.0, xlabel=r"count", ylabel=r"observations",
                 xticks=[0, 2, 4, 6, 8, 10, 12, 14], yticks=[0, 50, 100], center=[-2.6, 1.2, 0])
        ax = A.ax
        bars = bars_at(ax, np.arange(len(yh)), yh, 0.8, SERIES, 0.75)
        hdr = [r"\textbf{SE of the slope}", r"\textbf{value}", r"\textbf{ratio}"]
        body = [[r"Poisson model", f"{d['se_model'][1]:.4f}", "1.00"],
                [r"sandwich", f"{d['se_sandwich'][1]:.4f}", f"{d['se_sandwich'][1] / d['se_model'][1]:.2f}"],
                [r"quasi-Poisson, \ $\sqrt{\hat\phi}$", f"{d['se_quasi'][1]:.4f}", f"{d['se_quasi'][1] / d['se_model'][1]:.2f}"]]
        t = table_rows([hdr] + body, font_size=22, col_buff=0.45, row_buff=0.28, colors=[GREY_A, RES, HIT, TEAL])
        t.move_to([0, -2.35, 0])
        rows = fit_rows(VGroup(
            label(rf"{n} counts: \ log mean $0.5 + 0.4x$", font_size=22),
            label(r"but negative binomial, \ not Poisson", font_size=22, color=RES),
            label(rf"mean {d['mean']:.2f}, \ variance {d['var']:.2f}", font_size=22),
            label(rf"slope estimate {d['b'][1]:.3f} \ (truth 0.4): \ fine", font_size=22, color=HIT),
        ), 4.6, 0.38, [4.2, 1.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An everyday case. Four hundred counts whose log mean rises linearly with a covariate, with a "
            "slope of point four, <bookmark mark='b'/> but generated from a negative binomial, so they're more variable than a "
            "Poisson model allows. <bookmark mark='c'/> The mean is two point one, the variance six point six, three times as "
            "large. <bookmark mark='d'/> Fit a Poisson regression anyway. The slope estimate is fine, point four seven, "
            "because the Poisson score equations only need the mean to be right. <bookmark mark='e'/> But the model-based "
            "standard error is too small: the sandwich is sixty percent larger, and quasi-Poisson, which scales by the "
            "estimated dispersion, agrees with it."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in t], lag_ratio=0.3))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=22) if r.part == 22][3:5]
        b = coverage_board(rows, lit_part=22, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> To the Board: a thousand such data sets. Ninety-five percent intervals from the Poisson "
            "model's standard error cover the true slope seventy-seven percent of the time: broken. <bookmark mark='b'/> The "
            "same estimates with sandwich standard errors cover ninety-three percent: kept. The sandwich didn't fix the "
            "model; it stopped the model from lying about its precision."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()
