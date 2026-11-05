from __future__ import annotations

from videos.stats.stats24.common import *  # noqa: F403

PROBLEMS = [
    r"Write the gamma density in exponential-dispersion form: \ find $\theta$, \ $b(\theta)$, \ $\phi$ and $V(\mu)$.",
    r"Show that one Fisher-scoring step for a GLM is the weighted regression of $z = \eta + (y - \mu)\,d\eta/d\mu$.",
    r"Poisson deviance: \ show $D = 2\sum y_i \log(y_i/\hat\mu_i)$ when the model has an intercept and the log link.",
    r"Show that complete separation makes $\ell(c\,b)$ increase to 0 as $c \to \infty$.",
    r"NB as a mixture: \ $y \mid \lambda \sim$ Poisson$(\lambda)$, \ $\lambda \sim$ Gamma$(k, k/\mu)$: \ derive $E\,y$ and Var $y$.",
    r"Show that the Brier score is proper: \ $E_p (q - y)^2$ is minimized at $q = p$. \ Is $|q - y|$?",
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
            (r"Bliss's probits; \ cloglog 3.45", PATH), (r"three parts: \ family, \ predictor, \ link", MODEL),
            (r"$\theta$, \ $b(\theta)$, \ $V(\mu)$", MODEL), (r"IRLS: \ scoring as WLS, \ 7 steps", MODEL),
            (r"deviance, \ quantile residuals", PATH), (r"binary deviance: \ 63\% false alarms", RES),
            (r"separation; \ Firth 2.55", RES), (r"quasi-Poisson 90\%, \ sandwich 94\%", HIT),
            (r"NB beats ZIP and hurdle", NBC), (r"log-linear: \ independence as zeros", TEAL),
            (r"proportional odds, \ checked", PATH), (r"GEE: \ 55\% vs 95\%", HIT),
            (r"marginal vs conditional", TEAL), (r"proper scores; \ accuracy is not", MODEL),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 24, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-four in fourteen lines. <bookmark mark='a'/> Bliss's probits fitted the beetles; the asymmetric "
            "complementary log-log fitted them best. A generalized linear model has a family, a linear predictor and a link. "
            "The exponential dispersion family is defined by its canonical parameter, its cumulant function and its variance "
            "function. IRLS is Fisher scoring written as weighted least squares, seven steps for the beetles. The deviance "
            "and quantile residuals judge fit; for binary data the deviance alone raised false alarms sixty-three percent of "
            "the time. Separation sends coefficients to infinity, and Firth brings them back. Quasi-Poisson rescues some "
            "coverage, the sandwich all of it. The negative binomial beat zero inflation and hurdles for the doctor visits. "
            "Log-linear models turn independence into missing terms. Proportional odds share one slope across cut-points, "
            "which must be checked. GEE turned fifty-five percent coverage into ninety-five; it estimates marginal effects, "
            "not conditional ones. And probability forecasts are graded by proper scores, which accuracy is not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=38.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GLMMs: \ the conditional effects", [25]), (r"Bayesian GLMs; \ priors for separation", [26]),
            (r"AIC, \ cross-validation: \ which link?", [28]), (r"robust GLMs", [30]),
            (r"penalized GLMs: \ the lasso for logistic", [32]), (r"propensity scores are GLMs", [36]),
            (r"Cox regression as a Poisson GLM", [40]), (r"scoring rules for conformal and calibration", [34]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 25 fits generalized linear mixed models, the conditional effects "
            "of chapter eleven. Part 26 puts priors on GLM coefficients, which also cures separation. Part 28 chooses links and "
            "terms by AIC and cross-validation. Part 30 makes GLMs robust. Part 32 penalizes them, the lasso for logistic "
            "regression. Part 34 uses proper scores to grade calibrated predictions. Part 36's propensity scores are fitted "
            "GLMs. And Part 40 fits Cox's survival model as a Poisson GLM."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The gamma as an exponential dispersion "
            "family; Fisher scoring as weighted least squares; the Poisson deviance with an intercept; why separation sends "
            "the likelihood to zero; the negative binomial as a gamma mixture; and whether the Brier and absolute scores are "
            "proper. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"P. McCullagh \& J. Nelder, \emph{Generalized Linear Models} (2nd ed., 1989)",
             r"A. Agresti, \emph{Categorical Data Analysis} (3rd ed., 2013)",
             r"P. Dunn \& G. Smyth, \emph{Generalized Linear Models with Examples in R} (2018)",
             r"A. Dobson \& A. Barnett, \emph{An Introduction to Generalized Linear Models} (4th ed., 2018)"],
            [r"C. Bliss (1935); \ J. Nelder \& R. Wedderburn (1972); \ R. Wedderburn (1974); \ P. McCullagh (1980)",
             r"A. Albert \& J. Anderson (1984); \ D. Firth (1993); \ P. Dunn \& G. Smyth (1996)",
             r"M. Greenwood \& G. U. Yule (1920); \ J. Mullahy (1986); \ D. Lambert (1992)",
             r"K.-Y. Liang \& S. Zeger (1986); \ S. Zeger, K.-Y. Liang \& P. Albert (1988); \ T. Gneiting \& A. Raftery (2007)"])
        with self.voiceover(
            "The books this part follows: McCullagh and Nelder's Generalized Linear Models, Agresti's Categorical Data "
            "Analysis, Dunn and Smyth's GLMs with examples in R, and Dobson and Barnett's introduction; with the papers from "
            "Bliss to Gneiting and Raftery."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=24, current=None)
        nxt = VGroup(label(r"Part 25", font_size=30, color=GREY_B), label(r"Borrowing Strength", font_size=48),
                     label(r"shrinkage, \ empirical Bayes and mixed models", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-four parts of sixty-five. <bookmark mark='a'/> One family of models now covers proportions, counts, "
            "categories and clusters. <bookmark mark='b'/> Next, estimating many related things at once. In 1975 Bradley "
            "Efron and Carl Morris predicted eighteen baseball players' batting averages, and shrinking each towards the "
            "others beat using each player's own record. Part 25: borrowing strength."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(24)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
