from __future__ import annotations

from videos.stats.stats42.common import *  # noqa: F403

PROBLEMS = [
    r"A cluster trial has $k$ towns per arm of $m$ adults, \ ICC $\rho$: \ show $\text{Var}(\hat\tau) = 2\sigma^2[1 + (m - 1)\rho]/(km)$, \ and find the fewest towns as $m \to \infty$.",
    r"Show that conditioning on a collider $V$ ($T \to V \leftarrow Y$) makes $T$ and $Y$ dependent \ even when $T$ has no effect on $Y$.",
    r"Show that the sandwich $A^{-1} B A^{-1}$ reduces to $I^{-1}$ when the model is correct \ (the information identity).",
    r"Show that IRLS is Newton's method for a GLM with its canonical link, \ and Fisher scoring otherwise.",
    r"With orthonormal columns, \ show that the lasso solution is the soft-thresholded least squares fit.",
    r"For independent p-values, \ show that BH controls the FDR at $q\, m_0 / m$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.degree()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"randomize what is delivered: \ towns", CASE1), (r"the ICC from a one-way ANOVA", CASE1),
            (r"design effect $1 + (m - 1)\rho$: \ towns are the $n$", CASE1), (r"a pre-registered cluster ANCOVA", CASE1),
            (r"confounding by indication: \ the sign flips", CASE2), (r"no mediators, \ no colliders", CASE2),
            (r"MI with the outcome, \ then AIPW", CASE2), (r"robustness values and benchmarks; \ one page", CASE2),
            (r"sandwich, \ IRLS, \ REML, \ partial pooling", S.ACCENT), (r"$\hat R$ and ESS; \ AIC vs BIC", S.ACCENT),
            (r"bandwidths, \ influence, \ KKT", S.ACCENT), (r"BH, \ conformal, \ Kaplan--Meier", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 42, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part forty-two in twelve lines. <bookmark mark='a'/> Randomize the unit that receives the intervention, here "
            "towns. Estimate the intraclass correlation from a pilot by one-way analysis of variance, and plan with the "
            "cautious end of its interval. The design effect, one plus m minus one rho, makes towns the real sample size. "
            "Write the analysis down before randomizing, at the level of the cluster, adjusted for baseline. In "
            "observational data, confounding by indication can flip the sign of an effect. Draw the graph, and adjust for "
            "neither mediators nor colliders. Impute with the outcome in the model, then use a doubly robust estimator. "
            "Measure how strong a hidden confounder would have to be, compare it with the measured ones, and write one "
            "page. And the exam: the sandwich, IRLS, REML and partial pooling; R hat, effective sample sizes, AIC and BIC; "
            "bandwidths, influence functions and KKT checks; Benjamini–Hochberg, conformal intervals and Kaplan–Meier."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=36.0)
        self.clear_scene()

    def degree(self):
        rows = fit_rows(VGroup(
            label(r"Stage III: \ the master's, \ Parts 21--42", font_size=28, color=GREY_A),
            label(r"optimization, \ likelihood, \ linear and generalized linear models, \ hierarchical and Bayesian models", font_size=22),
            label(r"model choice, \ smoothing, \ robustness, \ multivariate analysis, \ sparsity, \ multiplicity, \ conformal prediction", font_size=22),
            label(r"experiments, \ causal inference, \ natural experiments, \ time series, \ space, \ survival, \ missing data", font_size=22),
            label(r"and an exam: \ two clients, \ twelve problems", font_size=26, color=S.ACCENT),
            label(r"the Master's", font_size=48, color=S.ACCENT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> That completes the third stage, the master's. <bookmark mark='b'/> Optimization and"
            " likelihood, linear and generalized linear models, hierarchical and Bayesian models and their "
            "computation; <bookmark mark='c'/> choosing models, smoothing, robustness, many variables, sparsity, many"
            " tests and prediction with guarantees; <bookmark mark='d'/> experiments and causes, natural experiments,"
            " time series, space, survival, and the data we did not see. <bookmark mark='e'/> And an exam: two "
            "clients and twelve problems, every one solved. <bookmark mark='f'/> That completes this course's "
            "master's-level stage; it is not an accredited degree."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=UP * 0.15))
        self.wait(1.5)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(42, r"the sandwich, \ AIPW's standard error, \ asymptotic normality: \ used everywhere",
                            r"that the limits exist and the approximations hold, \ taken on trust",
                            r"Parts 43--47: \ measure, \ martingales, \ estimation, \ testing, \ asymptotics")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next stage. Many standard errors in this exam leaned on "
            "asymptotics: the sandwich, the influence-function standard error of AIPW, and normal approximations "
            "behind several intervals. The Gaussian regression t intervals and split-conformal rank bound have "
            "different, explicit finite-sample justifications. <bookmark mark='b'/> We took on trust that the limits "
            "exist and that the approximations hold. <bookmark mark='c'/> The PhD core proves it, starting from the "
            "foundations: measure-theoretic probability, martingales, the theory of estimation and of testing, and "
            "asymptotic statistics."
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
            (r"what a random variable is; \ why the limits hold", [43]), (r"the sandwich's asymptotics, \ proved", [47]),
            (r"AIPW's efficiency bound", [49]), (r"the qualifying exam", [55]), (r"anytime-valid trials and adaptive designs", [58]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-three asks what a random variable really is and why"
            " the laws of large numbers hold. Part forty-seven proves the sandwich's asymptotics. Part forty-nine "
            "shows when the augmented estimator attains the efficiency bound, including correct nuisance limits and "
            "regularity conditions. Part fifty-five is the next exam, the qualifying exam of the PhD. And Part "
            "fifty-eight revisits trial design, with experiments that can be watched and stopped at any time."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six more problems for the problem bank, with full solutions in the README alongside the twelve from the "
            "exam. <bookmark mark='a'/> The variance of a cluster trial; a collider's bias; the sandwich under a correct "
            "model; IRLS as Newton's method; the lasso with orthonormal columns; and the proof that Benjamini–Hochberg "
            "controls the false discovery rate. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. Hayes \& L. Moulton, \emph{Cluster Randomised Trials} (2nd ed. 2017); \ A. Donner \& N. Klar (2000)",
             r"D. Cox \& C. Donnelly, \emph{Principles of Applied Statistics} (2011); \ M. Hernán \& J. Robins, \emph{Causal Inference: What If} (2020)",
             r"A. Gelman et al., \emph{Bayesian Data Analysis} (3rd ed. 2013); \ L. Wasserman, \emph{All of Statistics} (2004)",
             r"D. Cox \& D. Hinkley, \emph{Problems and Solutions in Theoretical Statistics} (1978); \ the CONSORT statement (2010, 2012)"],
            [r"R. A. Fisher (1938); \ J. Cornfield (1978); \ D. Rubin (1981); \ H. Akaike (1974); \ G. Schwarz (1978); \ C. Bliss (1935); \ J. Longley (1967)",
             r"E. Freireich et al. (1963); \ M. Greenwood (1926); \ B. Silverman (1986); \ F. Hampel (1974); \ S. Stigler (1977)",
             r"R. Tibshirani (1996); \ Y. Benjamini \& Y. Hochberg (1995); \ J. Lei et al. (2018); \ A. Vehtari et al. (2021)",
             r"C. Cinelli \& C. Hazlett (2020); \ B. Neal et al. (2021), \ the Salt Substitute and Stroke Study"])
        with self.voiceover(
            "The books behind this part: Hayes and Moulton, and Donner and Klar, on cluster trials; Cox and Donnelly's "
            "principles of applied statistics, and Hernán and Robins on causal inference; Gelman and colleagues, and "
            "Wasserman, and Cox and Hinkley's book of problems, for the exam; and the CONSORT statement; with the papers from Bliss and Fisher to the salt "
            "substitute trial."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=42, current=None)
        nxt = VGroup(label(r"Part 43", font_size=30, color=GREY_B), label(r"Measure-Theoretic Probability", font_size=48),
                     label(r"what exactly is a random variable, \ and why do the limit theorems hold?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-two parts of sixty-five, and the second milestone. <bookmark mark='a'/> The master's is complete. "
            "<bookmark mark='b'/> The PhD core begins with the oldest question we have postponed: what exactly is a random "
            "variable, and why do the limit theorems we have leaned on since Part six actually hold? Part forty-three: "
            "measure-theoretic probability."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(42)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
