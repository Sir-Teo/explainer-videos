from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class Kriging(VoiceoverScene):
    def construct(self):
        self.card()
        self.blup()
        self.kinds()
        self.meuse_map()
        self.cv()
        self.world()
        self.gp()

    def card(self):
        card = chapter_card(4, r"Kriging", r"The best linear unbiased predictor", lit=(1963,), part=PART)
        with self.voiceover("Chapter four. Kriging."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def blup(self):
        rows = [
            cmath(r"\hat Z(s_0)", r"=", r"\textstyle\sum_i \lambda_i Z(s_i) = \lambda^\top Z", font_size=32),
            cmath(r"\text{unbiased}", r":", r"\textstyle\sum_i \lambda_i = 1 \quad \text{(for an unknown constant mean)}", font_size=30),
            cmath(r"\min_\lambda", r":", r"\text{Var}(\hat Z(s_0) - Z(s_0)) = \lambda^\top K \lambda - 2\lambda^\top k_0 + C(0)", font_size=28),
            cmath(r"\begin{pmatrix} K & \mathbf 1 \\ \mathbf 1^\top & 0 \end{pmatrix}\binom{\lambda}{m}", r"=", r"\binom{k_0}{1}", font_size=30),
        ]
        rows[3][-1].set_color(FIELDC)
        whys = [why(r"a weighted average"), why(r"ordinary kriging"), why(r"the prediction error variance"),
                why(r"a Lagrange multiplier $m$")]
        with self.voiceover(
            "<bookmark mark='a'/> Kriging predicts the value at a new site as a weighted average of the observations. "
            "<bookmark mark='b'/> For the prediction to be unbiased whatever the unknown constant mean, the weights must "
            "add to one. <bookmark mark='c'/> Among such weights, choose the ones that minimize the variance of the "
            "prediction error. That variance involves K, the covariances among the observations, and k nought, their "
            "covariances with the new site. <bookmark mark='d'/> A Lagrange multiplier turns the problem into one linear "
            "system. Its solution gives samples near the new site large weights, but discounts samples that cluster "
            "together, since they tell the same story: Krige's insight."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kinds(self):
        rows = fit_rows(VGroup(
            label(r"simple kriging: \ the mean is known", font_size=26, color=GREY_A),
            label(r"ordinary kriging: \ an unknown constant mean \ (weights sum to one)", font_size=26, color=FIELDC),
            label(r"universal kriging: \ an unknown trend $x(s)^\top\beta$, \ estimated by GLS \ (Part 23)", font_size=26, color=TAUC),
            label(r"the variance: \ zero at a sample \ (without a nugget), \ the sill far away, \ plus $\hat\beta$'s uncertainty", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three versions. Simple kriging assumes the mean is known. <bookmark mark='b'/> Ordinary "
            "kriging, the one just derived, assumes only that it is constant. <bookmark mark='c'/> Universal kriging allows "
            "a trend in covariates, estimated by the generalized least squares of Part twenty-three, and then kriges the "
            "residuals. <bookmark mark='d'/> Each comes with a prediction variance: zero at an observed site when there is no "
            "nugget, rising to the sill far from all data, plus the uncertainty of the estimated trend."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def meuse_map(self):
        d = load("meuse")
        gx, gy = np.asarray(d["gx"], float), np.asarray(d["gy"], float)
        uk, sd = np.asarray(d["uk"], float), np.asarray(d["uk_sd"], float)
        F = FieldSurface(gx, gy, uk, 0.04, width=3.6, center=[-4.6, -0.2, 0], lo=4.4, hi=7.5)
        G = FieldSurface(gx, gy, sd, 0.04, width=3.6, center=[-0.6, -0.2, 0], lo=float(sd.min()), hi=float(sd.max()))
        pts = G.dots(np.asarray(d["x"], float), np.asarray(d["y"], float), WHITE, 0.025)
        t1 = label(r"universal kriging of log zinc", font_size=22, color=FIELDC).next_to(F, UP, buff=0.12)
        t2 = label(r"its SE \ (white: \ samples)", font_size=22, color=TAUC).next_to(G, UP, buff=0.12)
        side = fit_rows(VGroup(
            label(r"trend: \ $\sqrt{d}$, \ $d$ = distance", font_size=24),
            label(r"\ \ to the river \ (scaled 0--1)", font_size=24),
            label(rf"$\hat\beta$: \ {d['uk_beta'][0]:.2f} $-$ {abs(d['uk_beta'][1]):.2f} $\sqrt{{d}}$", font_size=24, color=TAUC),
            label(r"error: \ smallest by samples,", font_size=24, color=BANDC),
            label(r"\ \ largest in gaps", font_size=24, color=BANDC),
        ), 4.0, 0.4, [4.6, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Universal kriging of log zinc over Meuse's prediction grid, with the square root of the "
            "distance to the river as the trend. <bookmark mark='b'/> Zinc falls with distance from the river, as the "
            "trend coefficient says, and the kriged residuals add the local detail the trend misses. <bookmark mark='c'/> "
            "On the right, the kriging standard error: smallest right beside the samples, in white, largest in the gaps "
            "between them and at the edges."
        ) as vo:
            self.add(meuse_tag())
            vo.wait_until("a")
            self.play(FadeIn(F), FadeIn(t1), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(G), FadeIn(t2), FadeIn(pts), FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def cv(self):
        d = load("meuse")
        r = d["rmse"]
        rows = [[r"leave-one-out prediction of log zinc", r"RMSE"],
                [r"the overall mean", f"{r['mean']:.3f}"],
                [r"inverse-distance weighting", f"{r['idw']:.3f}"],
                [r"ordinary kriging", f"{r['ok']:.3f}"],
                [r"universal kriging \ (river distance)", f"{r['uk']:.3f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.32, colors=[GREY_A, MISSC, TAUC, FIELDC, BANDC]).move_to([0, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How much does it help? Leave out each sample in turn and predict it from the others. "
            "<bookmark mark='b'/> The overall mean misses by " + say(r["mean"], 2) + " on the log scale. <bookmark "
            "mark='c'/> Inverse-distance weighting, the usual ad hoc interpolator, by " + say(r["idw"], 2) + ". <bookmark "
            "mark='d'/> Ordinary kriging by " + say(r["ok"], 2) + ", <bookmark mark='e'/> and universal kriging with the "
            "river's distance by " + say(r["uk"], 2) + ": almost half the error of the mean."
        ) as vo:
            self.add(meuse_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def world(self):
        d = load("world")
        px, py = np.asarray(d["px"], float), np.asarray(d["py"], float)
        tr, pr, sd = (np.asarray(d[k], float) for k in ("truth", "pred", "sd"))
        lo, hi = float(tr.min()), float(tr.max())
        F1 = FieldSurface(px, py, tr, 0.2, width=5.6, center=[-3.3, 0.4, 0], lo=lo, hi=hi)
        F2 = FieldSurface(px, py, pr, 0.2, width=5.6, center=[3.3, 0.4, 0], lo=lo, hi=hi)
        unc = F2.uncertainty(sd)
        st = F2.dots(np.asarray(d["sx"], float), np.asarray(d["sy"], float), WHITE, 0.025)
        t1 = label(r"the truth", font_size=22, color=TRUEC).next_to(F1, UP, buff=0.1)
        t2 = label(r"universal kriging from 300 stations", font_size=22, color=FIELDC).next_to(F2, UP, buff=0.1)
        foot = fit_rows(VGroup(
            label(rf"RMSE over the island: \ {d['rmse_krige']:.2f}, \ against {d['rmse_lm']:.2f} for the traffic trend alone", font_size=22, color=BANDC),
            label(rf"90\% intervals cover {100 * d['cover']:.0f}\% of the island's grid in this one field \ (the Board averages over many)", font_size=22, color=GREY_A),
        ), 12.4, 0.25, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World lets us check against the truth. On the left, the true field; on the right, "
            "universal kriging with the traffic index, from the three hundred stations. <bookmark mark='b'/> The darkening "
            "marks the kriging standard error: largest in the empty interior and at the coasts. <bookmark mark='c'/> Over "
            "the whole island, kriging misses by " + say(d["rmse_krige"], 2) + ", against " + say(d["rmse_lm"], 2) + " for "
            "the traffic trend alone. <bookmark mark='d'/> Its ninety percent intervals cover " + str(round(100 * d["cover"]))
            + " percent of the island in this one field. With one realization, coverage over space is itself noisy; "
            "chapter fourteen averages over many fields."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(F1), FadeIn(t1), FadeIn(F2), FadeIn(t2), FadeIn(st))
            vo.wait_until("b")
            self.play(FadeIn(unc))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def gp(self):
        rows = [
            cmath(r"W \sim \text{GP}(0, C)", r":", r"\text{a prior over functions}", font_size=30),
            cmath(r"E[W(s_0) \mid Z]", r"=", r"k_0^\top (K + \tau^2 I)^{-1} (Z - \mu)", font_size=30),
            cmath(r"\text{Var}[W(s_0) \mid Z]", r"=", r"C(0) - k_0^\top (K + \tau^2 I)^{-1} k_0", font_size=30),
            cmath(r"\text{so}", r":", r"\text{simple kriging = the GP posterior; \ universal = a flat prior on } \beta", font_size=28),
        ]
        rows[3][-1].set_color(FIELDC)
        whys = [why(r"Part 26's Bayes, \ infinite-dimensional"), why(r"Part 5's conditional normal"), why(r"the kriging variance"),
                why(r"Kimeldorf \& Wahba; \ O'Hagan (1978)")]
        with self.voiceover(
            "<bookmark mark='a'/> Kriging has a Bayesian reading. Treat the field as a Gaussian process: a prior over "
            "functions. <bookmark mark='b'/> Conditioning on the observations, by Part five's conditional normal, gives a "
            "posterior mean <bookmark mark='c'/> and variance <bookmark mark='d'/> that are exactly simple kriging's, and "
            "universal kriging is what a flat prior on the trend coefficients gives. Statisticians, geologists and "
            "machine-learning researchers found the same object three times."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
