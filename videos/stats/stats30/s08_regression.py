from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class Regression(VoiceoverScene):
    def construct(self):
        self.card()
        self.stars()
        self.leverage()
        self.gm()
        self.lms_lts()
        self.s_est()
        self.fits()
        self.mm()
        self.inference()
        self.residuals()
        self.advice()

    def card(self):
        card = chapter_card(7, r"Robust regression", r"LMS, \ LTS, \ S and MM", lit=(1984,), part=PART)
        with self.voiceover("Chapter seven. Robust regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def _axes(self):
        return axes([3.3, 4.8], [3.8, 6.4], x_length=7.4, y_length=4.4, xlabel=r"log surface temperature",
                    ylabel=r"log light intensity", xticks=[3.5, 4, 4.5], yticks=[4, 5, 6], center=[-2.0, 0.3, 0])

    def _line(self, ax, b, col, sw=3.5):
        # the part of the line inside the axes' box
        x0, x1, y_lo, y_hi = 3.35, 4.75, 3.85, 6.35
        xs = np.linspace(x0, x1, 400)
        ys = b[0] + b[1] * xs
        k = (ys >= y_lo) & (ys <= y_hi)
        xs, ys = xs[k], ys[k]
        return Line(ax.c2p(xs[0], ys[0]), ax.c2p(xs[-1], ys[-1]), color=col, stroke_width=sw)

    def stars(self):
        d = load("regression")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = self._axes()
        ax = A.ax
        giants = set(d["giants"])
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=RES if k in giants else WHITE) for k, (a, b) in enumerate(zip(x, y))])
        ols = self._line(ax, d["ols"], MEANC)
        rows = fit_rows(VGroup(
            label(r"47 stars of the cluster CYG OB1", font_size=22),
            label(r"most on the main sequence: \ hotter is brighter", font_size=22),
            label(r"red: \ four giants, \ cool and bright", font_size=22, color=RES),
            label(rf"least squares: \ slope {d['ols'][1]:.2f}: \ cooler is brighter?", font_size=22, color=MEANC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Hertzsprung–Russell diagram of the star cluster CYG OB1: forty-seven stars, log surface "
            "temperature against log brightness. <bookmark mark='b'/> Most lie on the main sequence, where hotter stars are "
            "brighter. <bookmark mark='c'/> Four are giants, cool and very bright, far to the left. <bookmark mark='d'/> Least "
            "squares, pulled by them, has a negative slope: it says cooler stars are brighter, true of neither group."
        ) as vo:
            self.add(stars_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[pts[k] for k in giants]), color=RES), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ols), FadeIn(rows[3]))
        self.clear_scene()

    def leverage(self):
        rows = [
            cmath(r"\text{M-regression}", r":", r"\textstyle\sum_i \psi(r_i/s)\, x_i = 0", font_size=30),
            cmath(r"\text{bounded in } r", r":", r"\text{yes; \ \ bounded in } x: \ \text{no}", font_size=30),
            cmath(r"\text{breakdown}", r":", r"1/n \ \text{to a bad leverage point}", font_size=30),
            cmath(r"\text{Huber M on the stars}", r":", r"\text{slope } {-0.43}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"psi of the residual, \ times the row"), why(r"an outlying $x$ multiplies the influence"),
                why(r"Maronna, \ Bustos \& Yohai (1979)"), why(r"no better than least squares")]
        with self.voiceover(
            "<bookmark mark='a'/> First try: Huber's M-estimator applied to regression, the estimating equation summing psi "
            "of each standardized residual times its row of the design. <bookmark mark='b'/> It bounds the influence of a large "
            "residual, but not of an outlying x: the row multiplies psi. <bookmark mark='c'/> A single bad leverage point can "
            "still break it. <bookmark mark='d'/> On the stars, Huber's regression gives slope minus point four three, no "
            "better than least squares, because the giants are leverage points that pull the line towards themselves and so "
            "don't even have large residuals."
        ) as vo:
            intro=label('Bounding the residual score alone does not bound design leverage',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lms_lts(self):
        rows = [
            cmath(r"\text{LMS}", r":", r"\min_\beta\ \mathrm{median}_i\, r_i^2", font_size=32),
            cmath(r"\text{LTS}", r":", r"\min_\beta \textstyle\sum_{i=1}^h r_{(i)}^2, \ \ h \approx n/2", font_size=32),
            cmath(r"\text{breakdown}", r":", r"\approx 50\%", font_size=32),
            cmath(r"\text{FAST-LTS}", r":", r"\text{C-steps: \ refit on the } h \text{ best, \ repeat}", font_size=30),
        ]
        rows[1][2].set_color(HLC)
        whys = [why(r"Rousseeuw (1984)"), why(r"least trimmed squares"), why(r"whatever the outliers' $x$ or $y$"),
                why(r"each step can only lower the criterion")]
        with self.voiceover(
            "<bookmark mark='a'/> Peter Rousseeuw's answer, 1984: minimize the median of the squared residuals "
            "instead of their sum. <bookmark mark='b'/> Or, better behaved, least trimmed squares: the sum of only "
            "the h smallest squared residuals, with h about half of n. <bookmark mark='c'/> Under general position "
            "and a fixed predictor dimension, exact high-breakdown regression estimators can approach one-half "
            "breakdown. Finite-sample bounds depend on n, p and h; a random-start approximation is not a certificate "
            "of the global optimum. <bookmark mark='d'/> Finding the best half is combinatorial; FAST-LTS starts from"
            " many random small subsets and improves each by concentration steps, refitting least squares on the h "
            "best points, which can only lower the criterion."
        ) as vo:
            intro=label('Trimming the residual objective changes its replacement sensitivity',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fits(self):
        d = load("regression")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = self._axes()
        ax = A.ax
        giants = set(d["giants"])
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=RES if k in giants else WHITE) for k, (a, b) in enumerate(zip(x, y))])
        ls = {k: self._line(ax, d[k], c) for k, c in (("ols", MEANC), ("lms", TRIMC), ("lts_rw", HLC), ("mm", BIWC))}
        rows = fit_rows(VGroup(
            label(rf"red: \ least squares, \ slope {d['ols'][1]:.2f}", font_size=22, color=MEANC),
            label(rf"teal: \ LMS, \ slope {d['lms'][1]:.2f}", font_size=22, color=TRIMC),
            label(rf"blue: \ reweighted LTS, \ slope {d['lts_rw'][1]:.2f}", font_size=22, color=HLC),
            label(rf"purple: \ MM, \ slope {d['mm'][1]:.2f}", font_size=22, color=BIWC),
            label(r"all the robust lines follow the main sequence", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The fits. Least squares, sloping down. <bookmark mark='b'/> Least median of "
            "squares: slope four, through the densest part of the main sequence. <bookmark mark='c'/> Least trimmed "
            "squares, after the customary reweighting step: intercept minus eight and a half, slope three point oh "
            "five, for this seeded teaching implementation; tuning, corrections and algorithms can change software "
            "results. <bookmark mark='d'/> The MM-estimator: slope two point two six. <bookmark mark='e'/> They "
            "differ, because the main sequence itself is curved and scattered, but all of them describe the main "
            "sequence, and none is captured by the giants."
        ) as vo:
            self.add(stars_tag())
            self.play(FadeIn(A), FadeIn(pts))
            for k, (key, m_) in enumerate((("ols", "a"), ("lms", "b"), ("lts_rw", "c"), ("mm", "d"))):
                vo.wait_until(m_)
                self.play(Create(ls[key]), FadeIn(rows[k]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def mm(self):
        rows = [
            cmath(r"\text{step 1}", r":", r"\text{a 50\% breakdown start (LTS, \ or an S-estimate)}", font_size=28),
            cmath(r"\text{step 2}", r":", r"\text{an M-scale } \hat s: \ \tfrac1n \textstyle\sum \rho(r_i/\hat s) = \tfrac12", font_size=28),
            cmath(r"\text{step 3}", r":", r"\text{biweight M-regression from the start, \ } \hat s \text{ fixed}, \ c = 4.685", font_size=28),
            cmath(r"\text{result}", r":", r"\text{theoretical MM: high breakdown, }95\%\text{ normal efficiency}", font_size=30),
        ]
        rows[3][2].set_color(BIWC)
        whys = [why(r"robust, \ but inefficient: \ LTS is 7\%"), why(r"the biweight $\rho$, \ $c = 1.547$"),
                why(r"a redescender, \ started in the right basin"), why(r"Yohai (1987)")]
        with self.voiceover(
            "<bookmark mark='a'/> High breakdown alone is not enough: least trimmed squares is only seven percent "
            "efficient when the errors really are normal. Victor Yohai's MM-estimator fixes that in three steps. "
            "Start from a high-breakdown fit. <bookmark mark='b'/> Estimate the residual scale by a robust M-scale. "
            "<bookmark mark='c'/> Then run a biweight M-regression from that start with the scale held fixed: a "
            "redescending estimator with a robust start. Multiple roots and convergence remain computational issues; "
            "theoretical MM guarantees require the appropriate initial fit and objective conditions. <bookmark "
            "mark='d'/> The theoretical construction can combine asymptotic high breakdown and about ninety-five "
            "percent Gaussian efficiency, under the theoretical conditions. Our LTS-initialized fixed-scale fit is an"
            " MM-style illustration, not a certified global S/MM solution."
        ) as vo:
            intro=label('High-breakdown initialization and fixed-scale refinement have distinct roles',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def residuals(self):
        d = load("regression")
        n = len(d["x"])
        so, sl = np.asarray(d["ols_std"]), np.asarray(d["lts_std"])
        A = axes([0, n + 1], [min(-4,float(sl.min())-1),max(14,float(sl.max())+1)], x_length=8.2, y_length=4.2, xlabel=r"star number", ylabel=r"standardized residual",
                 xticks=[1, 10, 20, 30, 40, 47], yticks=[-2.5, 0, 2.5, 10], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}",
                 center=[-2.2, 0.3, 0])
        ax = A.ax
        bands = VGroup(*[DashedLine(ax.c2p(0, v), ax.c2p(n + 1, v), color=GREY_B, stroke_width=1.5) for v in (-2.5, 2.5)])
        po = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.06, color=MEANC) for k, v in enumerate(so)])
        pl = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.06, color=HLC) for k, v in enumerate(sl)])
        out = [int(k) + 1 for k in d["lts_outliers"]]
        rows = fit_rows(VGroup(
            label(r"red: \ least squares: \ none beyond $\pm 2.5$", font_size=22, color=MEANC),
            label(rf"blue: \ LTS: \ stars {', '.join(map(str, out))}", font_size=22, color=HLC),
            label(r"the giants hide from least squares", font_size=22, color=RES),
        ), 3.6, 0.42, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Diagnostics tell the same story. Standardized by least squares, no residual exceeds two and "
            "a half: the giants have pulled the line so close that they look ordinary. <bookmark mark='b'/> Standardized by "
            "LTS, the four giants stand out far above the band, with stars seven and nine, two smaller anomalies. "
            "<bookmark mark='c'/> Least squares residuals mask exactly the points that matter; robust residuals reveal them."
        ) as vo:
            self.add(stars_tag())
            self.play(FadeIn(A), Create(bands))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in po], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(po), LaggedStart(*[FadeIn(p) for p in pl], lag_ratio=0.02), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"fit robustly and by least squares; \ if they differ, \ find out why", font_size=24),
            label(r"use robust residuals to find outliers, \ not least squares ones", font_size=24, color=HLC),
            label(r"MM for estimation and inference; \ LTS for diagnosis", font_size=24, color=BIWC),
            label(r"an outlier is a question, \ not a nuisance: \ here, \ a different kind of star", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Practical advice: fit both robustly and by least squares, and when they disagree, "
            "find out why. <bookmark mark='b'/> Compare robust and ordinary residual diagnostics; neither a large "
            "residual nor a robust weight proves a data error. <bookmark mark='c'/> Use MM for estimates and "
            "inference, LTS for diagnosis. <bookmark mark='d'/> And treat an outlier as a question: here the four "
            "points were not errors at all, but a different kind of star."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def s_est(self):
        rows = [
            cmath(r"\hat\beta_S", r"=", r"\arg\min_\beta\ s(r(\beta)), \ \ s \text{ an M-scale}", font_size=30),
            cmath(r"\text{LS}", r":", r"\arg\min \text{ residual mean square about zero}", font_size=30),
            cmath(r"\text{breakdown}", r":", r"\text{near }50\% \text{ for fixed }p\text{ and general position}", font_size=30),
            cmath(r"\text{efficiency}", r":", r"\le 33\% \text{ at 50\% breakdown}", font_size=30),
        ]
        rows[0][2].set_color(BIWC)
        whys = [why(r"Rousseeuw \& Yohai (1984)"), why(r"least squares minimizes a non-robust scale"),
                why(r"the scale's breakdown, \ inherited"), why(r"Hössjer (1992): \ the price of high breakdown")]
        with self.voiceover(
            "<bookmark mark='a'/> S-estimators, from Rousseeuw and Yohai, generalize the idea: choose the "
            "coefficients that minimize a robust M-scale of the residuals. <bookmark mark='b'/> Least squares "
            "minimizes the residual mean square about zero. Using a centered residual standard deviation alone would "
            "leave the intercept unidentified. <bookmark mark='c'/> With a fifty percent breakdown scale, the fit "
            "inherits fifty percent breakdown. <bookmark mark='d'/> But Ola Hössjer proved that at fifty percent "
            "breakdown an S-estimator can be at most thirty-three percent efficient. High breakdown and high "
            "efficiency need two steps."
        ) as vo:
            intro=label('Robust residual scale can define a regression objective',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gm(self):
        rows = [
            cmath(r"\text{GM-estimator}", r":", r"\textstyle\sum_i w(x_i)\, \psi(r_i/s)\, x_i = 0", font_size=30),
            cmath(r"w(x_i)", r":", r"\text{small for high-leverage rows}", font_size=30),
            cmath(r"\text{influence}", r":", r"\text{bounded in } x \text{ and in } r", font_size=30),
            cmath(r"\text{breakdown}", r":", r"\le 1/(p + 1): \ \text{falls with dimension}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"generalized M: \ Mallows (1975), \ Schweppe"), why(r"e.g.\ from robust distances of the $x_i$"),
                why(r"Hampel's bounded-influence regression"), why(r"Maronna, \ Bustos \& Yohai (1979)")]
        with self.voiceover(
            "<bookmark mark='a'/> One repair: generalized M-estimators, from Colin Mallows and Fred Schweppe, multiply each "
            "row's contribution by a weight depending on its x. <bookmark mark='b'/> Rows with high leverage get small "
            "weights. <bookmark mark='c'/> Now the influence is bounded in both x and the residual. <bookmark mark='d'/> But "
            "Ricardo Maronna, Oscar Bustos and Victor Yohai showed their breakdown point is at most one over p plus one, "
            "falling as predictors are added. High breakdown needs a different idea."
        ) as vo:
            intro=label('Design weights can limit local leverage influence',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def inference(self):
        rows = [
            cmath(r"\sqrt n(\hat\beta - \beta)", r"\Rightarrow", r"N\bigl(0, \ \sigma^2 \tfrac{E\psi^2}{(E\psi')^2} (X^\top X/n)^{-1}\bigr)", font_size=28),
            cmath(r"\text{SEs}", r":", r"\text{the M-estimator's sandwich, \ Part 22}", font_size=30),
            cmath(r"\text{tests}", r":", r"\text{robust Wald, \ and robust likelihood-ratio-type tests}", font_size=30),
            cmath(r"\text{caution}", r":", r"\text{valid near the model, \ not under arbitrary contamination}", font_size=28),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"fixed $p$, homoscedastic independent errors and regular design"), why(r"heteroscedasticity-robust versions too"),
                why(r"Ronchetti \& Hampel's tests"), why(r"robust inference is still local")]
        with self.voiceover(
            "<bookmark mark='a'/> MM estimates come with standard errors: at the model the estimator is asymptotically normal, "
            "with the familiar covariance inflated by E psi squared over E psi prime squared. <bookmark mark='b'/> In practice "
            "the M-estimator's sandwich of Part 22 is used, which also allows uneven noise. <bookmark mark='c'/> Robust Wald "
            "tests and robust analogues of likelihood-ratio tests follow. <bookmark mark='d'/> But these intervals are valid "
            "near the model, not under arbitrary contamination: robust inference, like robust estimation, buys protection "
            "within a neighbourhood, not everywhere."
        ) as vo:
            intro=label('Model-based robust asymptotics require design and error conditions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
