from __future__ import annotations

from videos.stats.stats25.common import *  # noqa: F403

PROBLEMS = [
    r"Prove Stein's lemma $E(X - \theta)h(X) = E\,h'(X)$ for $X \sim N(\theta, 1)$, \ and use it to derive SURE for $X + g(X)$.",
    r"Show that $E\{(p - 2)/\|X\|^2\} = 1/(1 + \tau^2)$ when $X_i \sim N(0, 1 + \tau^2)$ independently, \ $p \ge 3$.",
    r"Random intercept: \ show that the BLUP is $\hat u_g = \lambda_g(\bar y_g - \bar x_g^\top\hat\beta)$, \ $\lambda_g = \tau^2/(\tau^2 + \sigma^2/n_g)$.",
    r"One sample: \ show that REML gives $\hat\sigma^2 = \sum(y_i - \bar y)^2/(n - 1)$.",
    r"Show that under $\tau^2 = 0$ the LR statistic is $\tfrac12\chi^2_0 + \tfrac12\chi^2_1$ in large samples; \ what is the 5\% cut-off?",
    r"Mundlak: \ show that adding $\bar x_g$ makes the coefficient of $x_{gi}$ equal the within estimator.",
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
            (r"18 hitters: \ shrinking wins 3.5 to 1", PATH), (r"James--Stein dominates; \ SURE", SHRUNK),
            (r"empirical Bayes; \ Tweedie, \ the winner's curse", PRIOR), (r"variance components; \ ICC 0.18", SHRUNK),
            (r"the LMM: \ GLS and Henderson's BLUPs", SHRUNK), (r"REML: \ unbiased with few groups", HIT),
            (r"Satterthwaite 94\%; \ boundary mixtures", HIT), (r"growth curves: \ random slopes", SHRUNK),
            (r"nested and crossed: \ raters corrected", PATH), (r"Mundlak and Hausman", RES),
            (r"GLMMs; \ league tables shrunk", POOLED), (r"Fay--Herriot: \ 383 to 21", SHRUNK),
            (r"meta-analysis: \ Hartung--Knapp 94\%", HIT), (r"Rasch: \ an exam is a GLMM", PATH),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 25, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-five in fourteen lines. <bookmark mark='a'/> Shrinking eighteen hitters' averages towards each "
            "other cut the error three and a half times. James–Stein dominates the obvious estimator whenever there are "
            "three or more means, and SURE estimates its risk. It is empirical Bayes, and Tweedie's formula corrects the "
            "winner's curse without assuming a normal prior. Variance components split the World's scores: eighteen percent "
            "between schools. The linear mixed model is GLS with an estimated covariance, and Henderson's equations give its "
            "BLUPs. REML removes maximum likelihood's bias when groups are few. Satterthwaite's t restored coverage to "
            "ninety-four percent, and tests of a zero variance need a fifty-fifty mixture. Random slopes model growth. "
            "Nested and crossed effects corrected the essays for their raters. Mundlak's model and Hausman's test handle "
            "school effects correlated with SES. Mixed logistic models give conditional effects, and shrunk league tables "
            "find the truly bad hospitals. Fay–Herriot cut small-area error from three hundred and eighty-three to twenty-one. "
            "Hartung–Knapp kept meta-analysis coverage at ninety-four percent. And an exam is a mixed model, Rasch's."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"hierarchical Bayes: \ the eight schools", [26]), (r"MCMC for mixed models; \ the funnel", [27]),
            (r"mixed models in model selection", [28]), (r"false discovery rates as empirical Bayes", [33]),
            (r"fixed effects for panels", [37]), (r"spatial random effects", [39]),
            (r"frailty: \ random effects in survival", [40]), (r"admissibility, \ proved", [45]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 26 makes the hierarchy fully Bayesian with the eight schools, and "
            "Part 27 computes it, meeting Neal's funnel, the shape of a variance near zero. Part 28 asks how to choose among "
            "mixed models. Part 33 reads false discovery rates as empirical Bayes. Part 37 uses fixed effects for panel "
            "data. Part 39's spatial models are random effects that vary smoothly over a map. Part 40's frailties are random "
            "effects in survival. And Part 45 proves the theory of admissibility that Stein's paradox began."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Stein's lemma and SURE; why James–Stein's "
            "shrinkage estimates the empirical Bayes factor; the BLUP of a random intercept; REML's n minus one; the boundary "
            "mixture and its cut-off; and Mundlak's equivalence with fixed effects. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. Efron, \emph{Large-Scale Inference} (2010)",
             r"A. Gelman \& J. Hill, \emph{Data Analysis Using Regression and Multilevel/Hierarchical Models} (2007)",
             r"J. Pinheiro \& D. Bates, \emph{Mixed-Effects Models in S and S-PLUS} (2000)",
             r"J. N. K. Rao \& I. Molina, \emph{Small Area Estimation} (2nd ed., 2015)"],
            [r"C. Stein (1956); \ W. James \& C. Stein (1961); \ H. Robbins (1956); \ B. Efron \& C. Morris (1973, 1975)",
             r"C. Henderson (1950); \ H. Patterson \& R. Thompson (1971); \ N. Laird \& J. Ware (1982); \ S. Self \& K.-Y. Liang (1987)",
             r"Y. Mundlak (1978); \ J. Hausman (1978); \ N. Breslow \& D. Clayton (1993); \ R. Fay \& R. Herriot (1979)",
             r"R. DerSimonian \& N. Laird (1986); \ J. Hartung \& G. Knapp (2001); \ G. Rasch (1960); \ B. Efron (2011)"])
        with self.voiceover(
            "The books this part follows: Efron's Large-Scale Inference, Gelman and Hill's multilevel models, Pinheiro and "
            "Bates on mixed-effects models, and Rao and Molina on small areas; with the papers from Stein to Efron's "
            "Tweedie's formula."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=25, current=None)
        nxt = VGroup(label(r"Part 26", font_size=30, color=GREY_B), label(r"Bayesian Data Analysis", font_size=48),
                     label(r"hierarchies, \ priors, \ Bayes factors and model checking", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-five parts of sixty-five. <bookmark mark='a'/> Many related estimates are now made together, each "
            "borrowing strength from the rest. <bookmark mark='b'/> But the shrinkage target and its variance were "
            "estimated, then treated as known. In 1981 Donald Rubin analysed coaching programmes in eight schools, and "
            "treated the variance itself as uncertain, with a prior. Part 26: Bayesian data analysis."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(25)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
