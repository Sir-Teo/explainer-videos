from __future__ import annotations

from videos.stats.stats12.common import *  # noqa: F403

PROBLEMS = [
    r"Derive $\hat a, \hat b$ for simple regression from the normal equations, \ and show $\hat b = r\,s_y/s_x$.",
    r"Show that $H = X(X^\top X)^{-1}X^\top$ is symmetric and idempotent, \ and that $\mathrm{tr}\,H = p$.",
    r"Prove the Frisch--Waugh--Lovell theorem for two predictors.",
    r"True model $y = \beta_1 x_1 + \beta_2 x_2 + \varepsilon$; \ $x_2 = 0.5 x_1 + u$. \ What does the regression of $y$ on $x_1$ alone estimate?",
    r"With $n = 25$, \ $\bar x = 10$, \ $\sum (x_i - \bar x)^2 = 100$, \ $s = 2$: \ the SE of the fitted mean at $x_0 = 10$ and at $x_0 = 20$, \ "
    r"and the prediction SE at $x_0 = 20$.",
    r"Two predictors with correlation $\rho$: \ show $\mathrm{VIF} = 1/(1 - \rho^2)$.",
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
            (r"Ceres; \ Legendre vs Gauss", DATA), (r"minimize the squared misses", FIT), (r"normal equations; \ $r\,s_y/s_x$", FIT),
            (r"why squares; \ Boscovich's absolute errors", S.POST), (r"a projection; \ $H$; \ Pythagoras, \ $R^2$", OBS),
            (r"Gauss--Markov: \ BLUE", FIT), (r"$t$ and $F$ under normality", S.LIK), (r"FWL: \ what ``controlling'' means", OBS),
            (r"omitted-variable bias $= \gamma\delta$", RES), (r"dummies, \ interactions, \ logs, \ splines", S.CTRL),
            (r"confidence vs prediction bands", S.PRIOR), (r"collinearity, \ leverage, \ Cook's $D$", S.ACCENT),
            (r"HC3; \ the regression fallacy", MISS),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=27, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 12, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twelve in thirteen lines. <bookmark mark='a'/> Gauss found Ceres with least squares, and Legendre published it "
            "first. The method minimizes the squared misses; the normal equations solve it, and for one predictor the slope is "
            "the correlation rescaled. Squares are convenient, are maximum likelihood for normal errors, and are optimal among "
            "linear unbiased estimators, though Boscovich's absolute errors resist outliers. Geometrically the fit is a "
            "projection, with Pythagoras giving R squared and the F-test. Gauss–Markov makes it best linear unbiased, and "
            "normal errors give exact t and F. Frisch–Waugh–Lovell says what controlling for a variable means, and leaving one "
            "out biases the rest by gamma times delta. Dummies, interactions, logs and splines change what coefficients mean. "
            "Confidence bands are for the line, prediction bands for the next point. Collinearity inflates variances; leverage "
            "and Cook's distance find influential points; uneven noise needs HC3. And regression to the mean is not a cause."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=28.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"ANOVA, designed experiments", [13]), (r"logistic, Poisson regression", [14, 24]), (r"the linear model in depth", [23]),
            (r"mixed models, shrinkage", [25]), (r"smoothing, splines", [29]), (r"robust regression", [30]),
            (r"ridge, lasso", [32]), (r"causal regression, IV, DiD", [35, 36, 37]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Least squares is the trunk from which much of statistics branches: the "
            "analysis of variance in the next part; generalized linear models in Parts 14 and 24; the linear model in full "
            "depth in Part 23; mixed models, smoothing, robust regression, ridge and the lasso; and, in Parts 35 to 37, the "
            "regressions that try to identify causes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The simple-regression formulas; the hat "
            "matrix; Frisch–Waugh–Lovell, proved; an omitted variable; standard errors for a fitted mean and a prediction; and "
            "the variance inflation factor. Each one takes a page or less, and each uses an idea from this part that later parts "
            "take for granted. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Weisberg, \emph{Applied Linear Regression} (4th ed., 2014)",
             r"A. Gelman, J. Hill \& A. Vehtari, \emph{Regression and Other Stories} (2020)",
             r"G. Seber \& A. Lee, \emph{Linear Regression Analysis} (2nd ed., 2003); \ J. Fox, \emph{Applied Regression Analysis} (3rd ed., 2016)",
             r"S. Stigler, \emph{The History of Statistics} (1986), chs.~1, 4, 8"],
            [r"A.-M. Legendre (1805); \ C. F. Gauss (1809, 1821); \ R. Boscovich (1757)",
             r"R. Frisch \& F. Waugh (1933); \ M. Lovell (1963); \ A. Aitken (1935); \ H. Working \& H. Hotelling (1929)",
             r"F. Anscombe (1973); \ D. Cook (1977); \ H. White (1980); \ J. MacKinnon \& H. White (1985)",
             r"H. Secrist (1933) and H. Hotelling's review; \ S. Stigler, ``Gauss and the invention of least squares'' (1981)"])
        with self.voiceover(
            "The books and papers this part follows: Weisberg's Applied Linear Regression, Gelman, Hill and Vehtari's "
            "Regression and Other Stories, Seber and Lee, Fox, and Stigler's history, with the papers from Boscovich to White."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=12, current=None)
        nxt = VGroup(label(r"Part 13", font_size=30, color=GREY_B), label(r"Experiments by Design", font_size=48),
                     label(r"Fisher at Rothamsted: \ seventy years of wheat records that cannot answer anything", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twelve parts of sixty-five, the second of Stage II. <bookmark mark='a'/> We can fit a relationship, measure our uncertainty about it, and "
            "check whether it's being fooled. <bookmark mark='b'/> But a regression on observed data can't tell a cause from a "
            "coincidence. In 1919 the young Fisher arrived at the Rothamsted experimental station and found seventy years of "
            "carefully kept wheat records that could answer almost nothing. His solution was to design the data. Part 13: "
            "experiments by design."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(12)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
