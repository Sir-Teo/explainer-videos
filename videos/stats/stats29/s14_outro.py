from __future__ import annotations

from videos.stats.stats29.common import *  # noqa: F403

PROBLEMS = [
    r"Show that the histogram's integrated squared bias is $\tfrac{h^2}{12} R(f') + o(h^2)$ and find $h^*$; \ evaluate it for $N(0, \sigma^2)$.",
    r"Derive the KDE's bias $\tfrac12 h^2 \mu_2 f''(x)$ and variance $f(x) R(K)/(nh)$; \ minimize the AMISE.",
    r"Show that the Epanechnikov kernel minimizes $\mu_2^{1/2} R(K)$ among non-negative symmetric kernels.",
    r"Prove the Reinsch--Schoenberg theorem: \ $\int s''(g'' - s'') = 0$ for the natural spline $s$ interpolating $g$.",
    r"Prove the representer theorem for $\sum (y_i - f(x_i))^2 + \lambda \|f\|^2_{\mathcal H}$ and solve for $\alpha$.",
    r"Show that $E \max_{i \le n} |Z_i| \le \sqrt{2 \log(2n)}$ for $Z_i \sim N(0, 1)$, \ by Jensen on $e^{t \max |Z_i|}$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Old Faithful: \ two broad humps; no compelling third", PATH), (r"histograms: \ $h \propto n^{-1/3}$, \ $n^{-2/3}$", HISTC),
            (r"kernels: \ $h \propto n^{-1/5}$, \ $n^{-4/5}$; \ Epanechnikov", KDEC), (r"bandwidths: \ Sheather--Jones, \ LSCV", KDEC),
            (r"the curse: \ 842,000 points in 10-D", RES), (r"local linear: \ boundary bias $O(h^2)$", KDEC),
            (r"splines: \ Reinsch--Schoenberg; \ the spectrum", SPLC), (r"$\lambda$: \ GCV, \ REML (steadier)", SPLC),
            (r"RKHS: \ the representer theorem; \ GPs", KDEC), (r"wavelets: \ sparse, \ SureShrink", WAVC),
            (r"additive models for ozone", SPLC), (r"honest intervals: \ RBC 95\%, \ naive 91\%", HIT),
            (r"shape: \ PAVA, \ Grenander, \ $n^{-1/3}$", SPLC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 29, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-nine in thirteen lines. <bookmark mark='a'/> Old Faithful has two broad modes, without "
            "compelling evidence of a third in our approximate bootstrap calculation. The histogram's best bin "
            "shrinks like n to the minus a third, and its error like n to the minus two thirds. Kernel estimates do "
            "better, n to the minus four fifths, and the kernel's shape hardly matters. Plug-in bandwidths outperform"
            " the normal-reference rules in our bimodal example and are less variable than LSCV there. In ten "
            "dimensions the same accuracy needs eight hundred and forty-two thousand points. Local linear fitting "
            "removes the leading slope and design-density bias, retaining curvature bias at the boundary. Smoothing "
            "splines are natural cubic splines, low-pass filters in the Demmler–Reinsch basis, and REML chooses their"
            " smoothness more steadily than GCV in our experiment. The representer theorem makes infinite-dimensional"
            " problems finite, and the same fits are Gaussian-process posterior means. Wavelets exploit sparsity and "
            "adapt to jumps. Fixed-dimensional additive structure can recover one-dimensional component rates under "
            "design conditions. Intervals at the optimal bandwidth undercover, and robust bias correction improves "
            "coverage under its regularity and bandwidth conditions. And shape constraints smooth without any tuning "
            "at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=42.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(29, r"smoothing has rates: \ $n^{-4/5}$ for twice-differentiable densities, \ $n^{-1/3}$ pointwise error for strictly decreasing interior densities",
                            r"that no other method could do better",
                            r"Part 50 proves the rates minimax: \ Le Cam, \ Assouad and Fano lower bounds match them")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part derived rates: n to the minus four fifths for "
            "densities with two derivatives, a cube-root pointwise estimation-error scale at a strictly decreasing "
            "interior density; this differs from a squared-error risk rate. <bookmark mark='b'/> It did not show that"
            " nothing can do better. <bookmark mark='c'/> Part 50 proves it, with the lower-bound methods of Lucien "
            "Le Cam, Patrice Assouad and Robert Fano: the rates are minimax."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"robust smoothing; \ influence", [30]), (r"sparse additive models; \ the lasso's rates", [32]),
            (r"conformal bands for any smoother", [34]), (r"local linear at a cutoff: \ regression discontinuity", [37]),
            (r"Gaussian processes, \ kriging", [39]), (r"hazard smoothing", [40]),
            (r"minimax rates", [50]), (r"posterior contraction for curves", [53]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 30 makes smoothers robust. Part 32 fits sparse additive models in "
            "high dimensions. Part 34 wraps any smoother in conformal prediction bands. Part 37 uses local linear regression "
            "at a cutoff, the regression discontinuity design, with exactly this chapter's robust bias correction. Part 39 "
            "builds Gaussian processes and kriging. Part 40 smooths hazards. Part 50 proves the rates minimax. And Part 53 "
            "studies how fast posteriors for curves contract."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The histogram's bias and best bin; the "
            "kernel estimate's bias and variance; Epanechnikov's optimality; the Reinsch–Schoenberg theorem; the representer "
            "theorem; and the bound on the maximum of n normals behind the universal threshold. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. Silverman, \emph{Density Estimation for Statistics and Data Analysis} (1986)",
             r"M. Wand \& M. C. Jones, \emph{Kernel Smoothing} (1995); \ J. Fan \& I. Gijbels, \emph{Local Polynomial Modelling} (1996)",
             r"P. Green \& B. Silverman, \emph{Nonparametric Regression and Generalized Linear Models} (1994); \ G. Wahba, \emph{Spline Models} (1990)",
             r"L. Wasserman, \emph{All of Nonparametric Statistics} (2006); \ S. Wood, \emph{Generalized Additive Models} (2nd ed., 2017)"],
            [r"M. Rosenblatt (1956); \ E. Parzen (1962); \ E. Nadaraya \& G. Watson (1964); \ C. Reinsch (1967); \ G. Kimeldorf \& G. Wahba (1970)",
             r"D. Scott (1979); \ B. Silverman (1981); \ S. Sheather \& M. C. Jones (1991); \ J. S. Marron \& M. Wand (1992)",
             r"D. Donoho \& I. Johnstone (1994, 1995); \ T. Hastie \& R. Tibshirani (1990); \ C. Stone (1980, 1985)",
             r"U. Grenander (1956); \ P. Hall (1992); \ S. Calonico, M. Cattaneo \& M. Farrell (2018)"])
        with self.voiceover(
            "The books this part follows: Silverman on density estimation, Wand and Jones on kernel smoothing, Fan and "
            "Gijbels on local polynomials, Green and Silverman and Wahba on splines, Wasserman's All of Nonparametric "
            "Statistics and Wood on additive models; with the papers from Rosenblatt to Calonico, Cattaneo and Farrell."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=29, current=None)
        nxt = VGroup(label(r"Part 30", font_size=30, color=GREY_B), label(r"Robust Statistics", font_size=48),
                     label(r"breakdown, \ influence, \ Huber's minimax, \ and estimators that refuse to be dragged", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-nine parts of sixty-five. <bookmark mark='a'/> We can estimate whole curves, and say how fast and"
            " how honestly. <bookmark mark='b'/> Robust LOESS already downweighted large residuals, but most examples"
            " still trusted every observation. In 1960 John Tukey showed that a few percent of contamination is "
            "enough to make the sample standard deviation worse than a crude alternative. When a few points are "
            "wrong, everything can be wrong. Part 30: robust statistics."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(29)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
