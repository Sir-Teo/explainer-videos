from __future__ import annotations

from videos.stats.stats5.common import *  # noqa: F403

PROBLEMS = [
    r"Let $X \sim N(0, 1)$ and $Y = X^2$. \ Show $\mathrm{Cov}(X, Y) = 0$, \ and find $E[Y \mid X]$ and $E[X \mid Y]$.",
    r"Prove Eve's law, $\mathrm{Var}\, Y = E\,\mathrm{Var}(Y \mid X) + \mathrm{Var}\, E[Y \mid X]$, \ from the tower property.",
    r"$(X, Y)$ is bivariate normal with $\sigma_X = 2$, $\sigma_Y = 3$, $\rho = 0.6$. \ Find $E[Y \mid X = x]$, \ "
    r"$\mathrm{Var}(Y \mid X = x)$, \ and the slope of $X$ on $Y$.",
    r"A student scores 2 SD above the mean on a test with test--retest correlation $0.7$. \ Predict the retest score, \ "
    r"assuming a bivariate normal.",
    r"Show that P\'olya's urn (one red, one blue) gives $P(\text{the first } n \text{ draws are all red}) = 1/(n+1)$, \ and "
    r"deduce the limiting share is uniform.",
    r"Find the density of $U_1 + U_2 + U_3$ for independent uniforms on $(0, 1)$, \ by convolving the triangle with a uniform.",
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
            (r"Galton's ellipses; \ regression towards mediocrity", DATA),
            (r"joint, marginal, conditional: \ slice and renormalize", COND),
            (r"uncorrelated $\ne$ independent", S.RESID),
            (r"$E[Y \mid X]$: \ the best predictor, \ a projection", COND),
            (r"Eve: \ $\mathrm{Var} = E\,\mathrm{Var} + \mathrm{Var}\,E$", S.ACCENT),
            (r"the multivariate normal: \ $A\mathbf Z + \boldsymbol\mu$", S.EST),
            (r"Gaussian conditionals: \ linear mean, \ Schur variance", COND),
            (r"regression to the mean is not a force", S.RESID),
            (r"three lines through one ellipse", LINE_MAJ),
            (r"Jacobians, \ convolutions, \ ratios", EXACT),
            (r"latent classes and mixtures", S.PRIOR),
            (r"copulas: \ margins apart from dependence; \ tails", S.POST),
            (r"P\'olya, \ exchangeability, \ de Finetti", S.PRIOR),
            (r"rank, distance and information measures; \ Dirichlet", S.LIK),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=30, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.44),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.44)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 5, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part five in fourteen lines. <bookmark mark='a'/> Galton's table held ellipses, and children regressed "
            "toward the mean. A joint distribution is read three ways, and conditioning slices and renormalizes. "
            "Uncorrelated is not independent. The conditional mean is the best predictor, a projection; and the law "
            "of total variance splits variance into within and between. The multivariate normal is an affine image "
            "of independent normals, and its conditionals have linear means and Schur-complement variances: "
            "regression is born. Regression to the mean is not a force but a property of imperfect correlation, and "
            "three different lines pass through every ellipse. Densities change with Jacobians; sums convolve; ratios "
            "can be Cauchy. Latent classes make mixtures. Copulas separate margins from dependence, and their tails "
            "matter. Pólya's urn is exchangeable, and de Finetti's theorem turns exchangeability into Bayes. Rank, "
            "distance and information measures see what correlation misses; and the Dirichlet lives on the simplex."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=28.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"conditional expectation", [12, 35, 44]),
            (r"Eve's law, within and between", [13, 25]),
            (r"Gaussian conditioning", [12, 25, 38, 39]),
            (r"regression to the mean", [12, 35]),
            (r"mixtures and latent variables", [22, 31]),
            (r"copulas and tails", [30, 60]),
            (r"exchangeability, de Finetti", [15, 34, 44]),
            (r"Dirichlet--multinomial", [14, 15, 26]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Conditional expectation is the backbone of regression, causal "
            "inference and martingales. Within and between returns in the analysis of variance and random effects. "
            "Gaussian conditioning is regression, mixed models, the Kalman filter and kriging. Regression to the mean "
            "haunts every before-and-after comparison. Mixtures return with the EM algorithm and factor analysis; "
            "copulas in robust statistics; exchangeability in Bayesian statistics and in the conformal prediction of "
            "Part 34; and the Dirichlet with counts and categories."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3),
                      run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Uncorrelated but dependent; a "
            "proof of Eve's law; a bivariate normal's conditional; predicting a retest; Pólya's urn's first n draws; "
            "and the sum of three uniforms. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Blitzstein \& J. Hwang, \emph{Introduction to Probability} (2nd ed., 2019), chs.~7, 9, 10",
             r"T. W. Anderson, \emph{An Introduction to Multivariate Statistical Analysis} (3rd ed., 2003)",
             r"R. Nelsen, \emph{An Introduction to Copulas} (2nd ed., 2006); \ H. Joe, \emph{Dependence Modeling with Copulas} (2014)",
             r"S. Stigler, \emph{Statistics on the Table} (1999) and \emph{The Seven Pillars} (2016)"],
            [r"F. Galton (1886, 1889); \ J. Hanley, ``Transmuting women into men'' (2004)",
             r"K. Pearson (1894, 1896); \ F. Eggenberger \& G. P\'olya (1923); \ B. de Finetti (1931)",
             r"A. Sklar (1959); \ D. X. Li (2000); \ D. MacKenzie \& T. Spears (2014)",
             r"C. Spearman (1904); \ M. Kendall (1938); \ G. Sz\'ekely, M. Rizzo \& N. Bakirov (2007)",
             r"A. Tversky \& D. Kahneman (1974); \ D. Kahneman, \emph{Thinking, Fast and Slow} (2011)",
             r"E. Lukacs (1955); \ A. Dempster (1972); \ P. Diaconis \& D. Freedman (1980); \ J. Aitchison (1982)"])
        with self.voiceover(
            "The books and papers this part follows: Blitzstein and Hwang, Anderson's classic on multivariate "
            "analysis, Nelsen and Joe on copulas, and Stigler's histories, along with the original papers from "
            "Galton to Székely, Rizzo and Bakirov."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=5, current=None)
        nxt = VGroup(label(r"Part 6", font_size=30, color=GREY_B), label(r"The Laws of Averages", font_size=48),
                     label(r"why does the average of many random things become predictable?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Five parts of sixty-five, halfway through the first stage. <bookmark mark='a'/> We can now describe many "
            "variables at once. Part 1 found that every summary jiggles from sample to sample; Galton's mid-parents "
            "varied less than individuals because they're averages. <bookmark mark='b'/> Why does the average of many "
            "random things become predictable, and why does its distribution so often take the shape of a bell? "
            "Those are the laws of averages, and they're Part 6."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(5)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
