from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class Multivariate(VoiceoverScene):
    def construct(self):
        self.card()
        self.masking()
        self.mcd_def()
        self.dd()
        self.ellipses()
        self.stahel()
        self.swamping()

    def card(self):
        card = chapter_card(8, r"Robust multivariate", r"Masking, \ swamping, \ and the MCD", lit=(1999,), part=PART)
        with self.voiceover("Chapter eight. Robust multivariate estimation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def masking(self):
        rows = [
            cmath(r"d_i^2", r"=", r"(x_i - \bar x)^\top S^{-1} (x_i - \bar x)", font_size=32),
            cmath(r"\text{flag}", r":", r"d_i > \sqrt{\chi^2_{p, 0.975}}", font_size=32),
            cmath(r"\text{masking}", r":", r"\text{a cluster of outliers inflates } S \text{ and shifts } \bar x", font_size=30),
            cmath(r"\text{swamping}", r":", r"\text{good points pushed out by the shifted centre}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Mahalanobis distance, \ Part 5"), why(r"the normal-theory cut-off"),
                why(r"the outliers hide themselves"), why(r"and accuse the innocent")]
        with self.voiceover(
            "<bookmark mark='a'/> In many dimensions, outliers are judged by Mahalanobis distance from the mean, in the "
            "metric of the covariance, Part 5's tool. <bookmark mark='b'/> Points beyond the chi-squared cut-off are "
            "flagged. <bookmark mark='c'/> But a cluster of outliers inflates the covariance and drags the mean towards "
            "itself, so its own distances shrink: masking. <bookmark mark='d'/> And the displaced centre can push genuine "
            "points beyond the cut-off: swamping."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mcd_def(self):
        rows = [
            cmath(r"\text{MCD}", r":", r"\text{the } h \text{ points whose covariance has the smallest determinant}", font_size=28),
            cmath(r"(\hat\mu, \hat\Sigma)", r"=", r"\text{their mean and (rescaled) covariance}", font_size=30),
            cmath(r"\text{C-step}", r":", r"\text{keep the } h \text{ closest in } (\hat\mu, \hat\Sigma), \ \text{repeat}", font_size=30),
            cmath(r"\text{breakdown}", r":", r"\approx (n - h)/n \to 50\%", font_size=32),
        ]
        rows[0][2].set_color(HLC)
        whys = [why(r"Rousseeuw (1984): \ the tightest ellipsoid"), why(r"consistency factor from $\chi^2_p$"),
                why(r"the determinant never increases: \ FAST-MCD (1999)"), why(r"affine equivariant")]
        with self.voiceover(
            "<bookmark mark='a'/> Rousseeuw's minimum covariance determinant estimator looks for the h points, about half, "
            "whose covariance matrix has the smallest determinant: the tightest ellipsoid holding half the data. "
            "<bookmark mark='b'/> Their mean and rescaled covariance estimate the centre and shape. <bookmark mark='c'/> "
            "FAST-MCD, Rousseeuw and Van Driessen's algorithm of 1999, improves random starts by concentration steps: keep the "
            "h points closest under the current estimate, and the determinant can only fall. <bookmark mark='d'/> The "
            "breakdown point approaches one half."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dd(self):
        d = load("mcd")
        c, r = np.asarray(d["classical"]), np.asarray(d["robust"])
        cut = d["cutoff"]
        A = axes([0, 7.5], [0, 42], x_length=7.4, y_length=4.4, xlabel=r"classical Mahalanobis distance",
                 ylabel=r"MCD robust distance", xticks=[0, 2, 4, 6], yticks=[0, 10, 20, 30, 40], center=[-2.0, 0.3, 0])
        ax = A.ax
        vline = DashedLine(ax.c2p(cut, 0), ax.c2p(cut, 42), color=GREY_B, stroke_width=1.5)
        hline = DashedLine(ax.c2p(0, cut), ax.c2p(7.5, cut), color=GREY_B, stroke_width=1.5)
        cols = [RES if k < 10 else (HUBC if k < 14 else WHITE) for k in range(len(c))]
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=col) for a, b, col in zip(c, r, cols)])
        rows = fit_rows(VGroup(
            label(r"Hawkins, \ Bradu \& Kass: \ 75 points in 3 dimensions", font_size=22),
            label(rf"classical distances: \ only {len(d['classical_flagged'])} beyond the cut-off", font_size=22, color=GREY_A),
            label(r"red: \ cases 1--10, \ all masked", font_size=22, color=RES),
            label(rf"MCD: \ all 14 planted points flagged, \ the rest kept", font_size=22, color=HLC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hawkins, Bradu and Kass built a data set to defeat classical diagnostics: seventy-five "
            "points in three dimensions, with fourteen planted outliers. The distance–distance plot puts each point's "
            "classical distance against its robust one. <bookmark mark='b'/> Classical distances flag just two points, and "
            "not the worst ones. <bookmark mark='c'/> The ten planted bad points, in red, have classical distances of about "
            "two: perfectly masked. <bookmark mark='d'/> Their robust distances are around thirty, far beyond the cut-off, and "
            "the MCD flags exactly the fourteen planted points and nothing else."
        ) as vo:
            self.add(hbk_tag())
            self.play(FadeIn(A), Create(vline), Create(hline))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*pts[:10]), color=RES), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def swamping(self):
        rows = fit_rows(VGroup(
            label(r"the MCD is the start for robust PCA, \ discriminant analysis, \ regression", font_size=24, color=HLC),
            label(r"its cost grows fast with dimension: \ subsets of $p + 1$ points", font_size=24, color=RES),
            label(r"in high dimensions: \ Tukey depth, \ spectral filtering \ (Part 60)", font_size=24, color=PATH),
            label(r"look at the data: \ the distance--distance plot is the diagnosis", font_size=24),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The MCD is the robust starting point for principal components, discriminant analysis and "
            "regression with many predictors, the next part's territory. <bookmark mark='b'/> But its cost grows quickly "
            "with dimension. <bookmark mark='c'/> High-dimensional robust estimation, through Tukey's depth and spectral "
            "filtering, returns in Part 60. <bookmark mark='d'/> And always look at the data: the distance–distance plot is "
            "itself the diagnosis."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ellipses(self):
        d = load("mcd")
        X = np.asarray(d["X"])
        A = axes([-2, 40], [-2, 40], x_length=5.6, y_length=5.0, xlabel=r"$X_1$", ylabel=r"$X_2$", xticks=[0, 10, 20, 30],
                 yticks=[0, 10, 20, 30], center=[-2.6, 0.2, 0])
        ax = A.ax
        cols = [RES if k < 10 else (HUBC if k < 14 else WHITE) for k in range(len(X))]
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=c) for (a, b), c in zip(X[:, :2], cols)])
        from scipy import stats as st
        r = np.sqrt(st.chi2.ppf(0.975, 2))

        def ell(mu, S, col):
            w, V = np.linalg.eigh(np.asarray(S)[:2, :2])
            t = np.linspace(0, 2 * np.pi, 120)
            E = (V @ np.diag(np.sqrt(np.maximum(w, 1e-12))) @ np.vstack([np.cos(t), np.sin(t)])).T * r + np.asarray(mu)[:2]
            E = np.clip(E, -2, 40)
            m = VMobject(stroke_color=col, stroke_width=3)
            m.set_points_as_corners([ax.c2p(a, b) for a, b in E] + [ax.c2p(*E[0])])
            return m

        ec = ell(d["loc_classical"], d["scatter_classical"], MEANC)
        er = ell(d["loc"], d["scatter"], HLC)
        rows = fit_rows(VGroup(
            label(r"two of the three coordinates", font_size=22),
            label(r"red: \ the classical 97.5\% ellipse: \ stretched to swallow the outliers", font_size=22, color=MEANC),
            label(r"blue: \ the MCD's: \ tight around the 61 good points", font_size=22, color=HLC),
            label(r"the bad ten sit far outside it", font_size=22, color=RES),
        ), 4.6, 0.42, [4.2, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two of the three coordinates show why. <bookmark mark='b'/> The classical ninety-seven and a "
            "half percent ellipse is stretched along the line towards the outliers, wide enough to swallow them. "
            "<bookmark mark='c'/> The MCD's ellipse is a small tight disc around the sixty-one good points, "
            "<bookmark mark='d'/> and the fourteen planted points lie far outside it. The outliers built the classical "
            "ellipse that then declared them normal."
        ) as vo:
            self.add(hbk_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ec), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(er), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(VGroup(*pts[:14]), color=RES), FadeIn(rows[3]))
        self.clear_scene()

    def stahel(self):
        rows = [
            cmath(r"\text{outlyingness}", r":", r"r_i = \sup_{\|a\| = 1} \dfrac{|a^\top x_i - \mathrm{med}_j\, a^\top x_j|}{\mathrm{MAD}_j(a^\top x_j)}", font_size=26),
            cmath(r"\text{weights}", r":", r"w_i = w(r_i), \ \text{small for outlying points}", font_size=30),
            cmath(r"\text{estimate}", r":", r"\text{the weighted mean and covariance}", font_size=30),
            cmath(r"\text{breakdown}", r":", r"\approx 50\% \text{ in any dimension}", font_size=30),
        ]
        rows[0][2].set_color(HLC)
        whys = [why(r"the worst one-dimensional projection"), why(r"Stahel (1981); \ Donoho (1982)"),
                why(r"affine equivariant"), why(r"but the supremum is costly: \ random directions")]
        with self.voiceover(
            "<bookmark mark='a'/> A second route, from Werner Stahel and David Donoho: measure how outlying each point is in "
            "its worst one-dimensional projection, standardized robustly by median and MAD. <bookmark mark='b'/> Down-weight "
            "points by that outlyingness, <bookmark mark='c'/> and take the weighted mean and covariance. "
            "<bookmark mark='d'/> The Stahel–Donoho estimator has breakdown near one half in any dimension, but the supremum "
            "over all directions must be approximated by random ones, and the cost grows with dimension."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
