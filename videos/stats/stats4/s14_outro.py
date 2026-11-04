from __future__ import annotations

from videos.stats.stats4.common import *  # noqa: F403

PROBLEMS = [
    r"Show that if $P$ is a projection, so is $I - P$, \ and that $P(I - P) = 0$. \ What are the eigenvalues of $I - P$?",
    r"Show that $\operatorname{tr}(H) = p$ for $H = X(X^\top X)^{-1}X^\top$ \ by cycling the trace.",
    r"Let $\mathbf x$ have mean $\boldsymbol\mu$ and covariance $\sigma^2 I_n$. \ Use $E[\mathbf x^\top A\mathbf x] = "
    r"\operatorname{tr}(A\Sigma) + \boldsymbol\mu^\top A\boldsymbol\mu$ \ to show $E\, s^2 = \sigma^2$.",
    r"Find the eigenvalues and eigenvectors of $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, \ and sketch the ellipse "
    r"$\mathbf x^\top A^{-1}\mathbf x = 1$.",
    r"Verify the Sherman--Morrison formula by multiplying it out.",
    r"For $\mathbf z \sim N(\mathbf 0, I_n)$, \ show that $\sum_i (z_i - \bar z)^2 \sim \chi^2_{n-1}$ \ using the projection "
    r"$I - \tfrac1n J$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"the hat matrix: \ eigenvalues $0$ and $1$; \ $n - p$", S.ACCENT),
            (r"data are vectors; \ centring is a projection", DATA),
            (r"$P = A(A^\top A)^{-1}A^\top$; \ Gram--Schmidt, \ QR", FIT),
            (r"$\operatorname{tr}(AB) = \operatorname{tr}(BA)$; \ $E\,\mathbf x^\top A\mathbf x$", EIG),
            (r"spectral theorem: \ ellipses and the Rayleigh quotient", EIG),
            (r"PSD $=$ possible covariance; \ Cholesky; \ Loewner", SPACE),
            (r"SVD: \ rotate, stretch, rotate; \ Eckart--Young", S.WORLD),
            (r"the pseudoinverse: \ minimum-norm solutions", FIT),
            (r"Schur complements; \ Woodbury updates", RES),
            (r"Kronecker products and $\operatorname{vec}$", SPACE),
            (r"$\partial \log\det\Sigma = \Sigma^{-1}$; \ the Gaussian MLE", EIG),
            (r"$\mathbf z^\top P\mathbf z \sim \chi^2_{\operatorname{rank} P}$; \ Cochran", EXACT),
            (r"never invert $X^\top X$: \ $\kappa(X^\top X) = \kappa(X)^2$", RES),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=30, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.44),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.44)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 4, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part four in thirteen lines. <bookmark mark='a'/> The hat matrix's eigenvalues are zero and one, and "
            "degrees of freedom count the ones. Data are vectors, and centring is a projection. Projections are A, A "
            "transpose A inverse, A transpose, or Q Q transpose after Gram–Schmidt. The trace cycles, and gives the "
            "expectation of any quadratic form. The spectral theorem draws ellipses, and the Rayleigh quotient "
            "finds their axes. Covariance matrices are exactly the positive semidefinite ones, and Cholesky makes "
            "correlated normals. Every matrix rotates, stretches and rotates, and the truncated SVD is the best "
            "low-rank approximation. The pseudoinverse picks the minimum-norm solution. Schur complements and "
            "Woodbury invert in blocks; Kronecker products build structured covariances. The derivative of log det "
            "is the inverse. Quadratic forms in projections are chi-squared. And you should never invert X "
            "transpose X."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=26.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"projections, \ $n - p$", [8, 12, 13]),
            (r"Schur complements", [5, 25]),
            (r"the spectral theorem, \ PCA", [5, 31]),
            (r"the SVD, \ low rank", [31, 32, 52]),
            (r"Cochran's theorem", [8, 12, 13]),
            (r"matrix calculus", [22, 23]),
            (r"Woodbury", [25, 38, 39]),
            (r"conditioning", [21, 23]),
        ], font_size=22)
        with self.voiceover(
            "This part is a toolkit, so it comes back everywhere. <bookmark mark='a'/> Projections and n minus p in "
            "sampling theory, regression and the analysis of variance. Schur complements in Part 5's conditional "
            "distributions and Part 25's mixed models. The spectral theorem and the SVD in principal components, "
            "sparsity and random matrices. Cochran's theorem in every chi-squared, t and F test. Matrix calculus in "
            "likelihood and the linear model in depth. Woodbury in mixed models, the Kalman filter and kriging. And "
            "conditioning in optimization."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3),
                      run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The complement of a projection; "
            "the trace of the hat matrix; why the sample variance is unbiased, by the trace trick; an ellipse from "
            "an eigen-decomposition; checking Sherman–Morrison; and the chi-squared law of the centred sum of "
            "squares. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. Harville, \emph{Matrix Algebra From a Statistician's Perspective} (1997)",
             r"S. Searle \& A. Khuri, \emph{Matrix Algebra Useful for Statistics} (2nd ed., 2017)",
             r"J. Magnus \& H. Neudecker, \emph{Matrix Differential Calculus} (3rd ed., 2019); \ G. Seber, \emph{A Matrix "
             r"Handbook for Statisticians} (2008)",
             r"G. Strang, \emph{Introduction to Linear Algebra}; \ L. Trefethen \& D. Bau, \emph{Numerical Linear Algebra} (1997)"],
            [r"C. Eckart \& G. Young (1936); \ R. Penrose (1955); \ M. Woodbury (1950)",
             r"W. Cochran (1934); \ A.-L. Cholesky (1924, posthumous)",
             r"D. Hoaglin \& R. Welsch, ``The hat matrix in regression and ANOVA'' (1978)",
             r"J. von Neumann \& H. Goldstine (1947); \ J. H. Wilkinson, \emph{Rounding Errors} (1963); \ G. Golub (1965)"])
        with self.voiceover(
            "The books and papers this part follows: Harville, Searle and Khuri, Magnus and Neudecker, Seber, "
            "Strang, and Trefethen and Bau for numerical linear algebra, along with the original papers from "
            "Cochran to Golub."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=4, current=None)
        nxt = VGroup(label(r"Part 5", font_size=30, color=GREY_B), label(r"Many Variables at Once", font_size=48),
                     label(r"Galton's ellipses: \ how do heights travel through families?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Four parts of sixty-five. <bookmark mark='a'/> We have the tools; now we use them. In 1886 Francis "
            "Galton plotted parents' heights against their children's and saw ellipses, the same ellipses as our "
            "spectral theorem. <bookmark mark='b'/> Joint distributions of many variables, their covariances, "
            "conditioning on some of them, and the multivariate normal: that's Part 5. Galton's question was about "
            "inheritance, but his answer, regression toward the mean, turned out to be a fact about ellipses, and "
            "Part 5 will prove it with the Schur complement from chapter eight."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(4)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
