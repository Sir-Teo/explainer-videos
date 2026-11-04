from __future__ import annotations

from videos.stats.stats14.common import *  # noqa: F403

PROBLEMS = [
    r"With $\text{logit}\,p = 15.04 - 0.232\,T$: \ find $p$ at $60^\circ$F, \ and the odds ratio for $10^\circ$F colder.",
    r"For logistic regression, \ derive the score $X^\top(y - p)$ and the Hessian $-X^\top W X$, \ $W = \mathrm{diag}(p_i(1 - p_i))$.",
    r"30 events in 10,000 person-years exposed, \ 20 in 20,000 unexposed: \ the rate ratio and a 95\% Wald interval.",
    r"Kidney stones: \ A cures 81/87 small and 192/263 large; \ B cures 234/270 and 55/80. \ Which is better, \ and why do the totals disagree?",
    r"Show that the odds ratio of a $2\times2$ table is the same \ whether you compare rows or columns.",
    r"A constant forecast $q$ for a condition of prevalence $\pi$: \ show the expected Brier score is $(q - \pi)^2 + \pi(1 - \pi)$.",
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
            (r"Challenger: \ the chart without the zeros", EVENT), (r"least squares on 0/1 fails", RES),
            (r"logistic regression: \ linear log-odds", OBS), (r"odds ratios; \ logit vs probit", S.ALT),
            (r"maximum likelihood by IRLS", FIT), (r"deviance; \ LR vs Wald", S.LIK), (r"$\hat p(31) = 0.9996$, \ profile [0.80, 1]", EVENT),
            (r"extrapolation lives in the tails", RES), (r"Poisson regression with offsets", S.WORLD),
            (r"overdispersion: \ quasi, \ sandwich", RES), (r"tables: \ $\chi^2$, \ OR, \ RR; \ Simpson at Berkeley", WOMEN),
            (r"Mantel--Haenszel; \ case--control", S.ALT), (r"ROC, \ calibration, \ Brier", OBS),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=27, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 14, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part fourteen in thirteen lines. <bookmark mark='a'/> On the eve of the Challenger launch, a chart without the "
            "flights that had no damage hid the effect of cold. Least squares on zeros and ones gives impossible probabilities. "
            "Logistic regression makes the log-odds linear, so its coefficients are log odds ratios, and the logit and probit "
            "agree where the data are. Maximum likelihood is fitted by iteratively reweighted least squares, and deviances "
            "compare models, with likelihood ratios more trustworthy than Wald tests. At thirty-one degrees the fit gives "
            "point nine nine nine six, with a profile interval from point eight to one, but that number lives in the model's "
            "tail. Poisson regression models rates through an offset, and overdispersion makes its standard errors far too "
            "small. Tables have chi-squared tests, odds ratios and relative risks, and Berkeley's admissions reverse when "
            "departments are separated. Mantel and Haenszel pool strata, and case–control studies estimate odds ratios by "
            "sampling on the outcome. Finally, a forecast is judged by its ranking, its calibration and its Brier score."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=30.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"probabilities as beliefs: \ Bayes", [15]), (r"exact and rank tests, \ the bootstrap", [16]),
            (r"generalized linear models in full", [24]), (r"mixed models for clustered counts", [25]),
            (r"model choice, \ cross-validation", [28]), (r"classification and prediction", [19, 34]),
            (r"causal questions in tables", [35, 36]), (r"missing data and measurement error", [41]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> The next part reads probabilities as degrees of belief. Exact and rank "
            "tests and the bootstrap arrive in Part 16. Generalized linear models get their full theory in Part 24, and mixed "
            "models for clustered counts in Part 25. Choosing models, classification and prediction with guarantees come in "
            "Parts 19, 28 and 34; the causal reading of tables in Parts 35 and 36; and missing data and measurement error, "
            "which haunt every case–control study, in Part 41."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Reading the Challenger coefficients; the "
            "logistic score and Hessian; a rate ratio with its interval; the kidney-stone version of Simpson's paradox; the "
            "symmetry of the odds ratio; and the Brier score of a constant forecast. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Agresti, \emph{Categorical Data Analysis} (3rd ed., 2013)",
             r"P. McCullagh \& J. Nelder, \emph{Generalized Linear Models} (2nd ed., 1989)",
             r"D. Hosmer, S. Lemeshow \& R. Sturdivant, \emph{Applied Logistic Regression} (3rd ed., 2013)",
             r"E. Tufte, \emph{Visual Explanations} (1997), ch.~2; \ N. Breslow \& N. Day, \emph{Statistical Methods in Cancer Research} I (1980)"],
            [r"S. Dalal, E. Fowlkes \& B. Hoadley (1989); \ M. Lavine (1991)",
             r"J. Berkson (1944); \ D. Cox (1958); \ J. Nelder \& R. Wedderburn (1972); \ R. Wedderburn (1974)",
             r"P. Bickel, E. Hammel \& J. O'Connell (1975); \ N. Mantel \& W. Haenszel (1959)",
             r"R. Doll \& A. B. Hill (1950); \ J. Cornfield (1951); \ R. Prentice \& R. Pyke (1979); \ G. Brier (1950)"])
        with self.voiceover(
            "The books and papers this part follows: Agresti's Categorical Data Analysis, McCullagh and Nelder, Hosmer and "
            "Lemeshow, Tufte, and Breslow and Day, with the papers from Berkson to Prentice and Pyke."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=14, current=None)
        nxt = VGroup(label(r"Part 15", font_size=30, color=GREY_B), label(r"First Bayes", font_size=48),
                     label(r"a ball rolled on a billiard table, \ and a probability for what you cannot see", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fourteen parts of sixty-five, the fourth of Stage II. <bookmark mark='a'/> We can regress yes-or-no outcomes and "
            "counts, read tables without being fooled, and judge a forecast. <bookmark mark='b'/> All along, probability has "
            "described data: how often things happen. But the engineers at that teleconference were really arguing about a "
            "degree of belief in a single launch. Around the middle of the eighteenth century a Presbyterian minister, Thomas Bayes, imagined a ball rolled "
            "on a table, and showed how to put a probability on something you cannot see. Part 15: first Bayes."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(14)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
