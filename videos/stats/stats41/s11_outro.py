from __future__ import annotations

from videos.stats.stats41.common import *  # noqa: F403

PROBLEMS = [
    r"Show that under MAR with distinct parameters, \ the likelihood factors as $P(R \mid Y_{\text{obs}}, \phi) f(Y_{\text{obs}} \mid \theta)$.",
    r"Bivariate normal, \ $y$ missing when $x > c$: \ show the complete-case slope of $y$ on $x$ is unbiased, \ but the mean of $y$ is not.",
    r"Derive $T = W + (1 + 1/m)B$ from the law of total variance, \ including the $B/m$ term.",
    r"Show $E[R Y / \pi(X)] = E[Y]$ under MAR, \ and that AIPW is unbiased if either model is right.",
    r"Show the OLS slope on $W = X + U$ tends to $\lambda\beta$, \ $\lambda = \sigma_X^2 / (\sigma_X^2 + \sigma_U^2)$.",
    r"With Se + Sp $> 1$, \ show the matrix method recovers the true exposure share exactly in expectation.",
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
            (r"Wald: \ armour where the survivors were not hit", MNC), (r"MCAR, \ MAR, \ MNAR; \ ignorability", TAUC),
            (r"complete cases: \ fine for some questions", CCC), (r"mean imputation and LOCF: \ don't", CCC),
            (r"EM and FIML: \ use everything seen", OBSV), (r"MI: \ draw, \ analyse, \ combine", MIC),
            (r"congeniality: \ impute with the outcome", MIC), (r"weighting = causal inference; \ AIPW", IPWC),
            (r"Heckman; \ pattern mixtures; \ tipping points", MNC), (r"MRP: \ the Xbox poll; \ small areas", MIC),
            (r"attenuation; \ regression calibration; \ SIMEX", MNC), (r"misclassification; \ recall bias", MNC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 41, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part forty-one in twelve lines. <bookmark mark='a'/> Wald armoured the bombers where the survivors had not been "
            "hit. Rubin's mechanisms decide what can be learned: completely at random, at random, or not at random, and "
            "under the first two the mechanism can be ignored by likelihood. Complete cases are fine for some questions and "
            "badly wrong for others. Mean imputation and carrying values forward distort and mislead. EM and full "
            "information likelihood use everything observed. Multiple imputation draws plausible values, analyses each "
            "copy, and combines by Rubin's rules, and the imputation model must include the outcome. Weighting by response "
            "propensities is causal inference, and the augmented estimator is doubly robust. When data are not missing at "
            "random, model the selection, as Heckman did, or vary the departure and find the tipping point. MRP repairs a "
            "self-selected poll, given the right cells. Measurement error dilutes slopes, and replicates let us correct "
            "them. And misclassification, especially when it differs by outcome, can push in either direction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(41, r"IPW and AIPW: \ unbiased under MAR, \ doubly robust",
                            r"that AIPW is the best one can do, \ taken on trust",
                            r"Part 49: \ influence functions and the semiparametric efficiency bound")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part used weighting and its augmented version. <bookmark "
            "mark='b'/> We took on trust that the augmented estimator is the most efficient of its kind. <bookmark mark='c'/> "
            "Part forty-nine proves it, with influence functions and the semiparametric efficiency bound. But first, Part "
            "forty-two: the comprehensive exam that closes the master's."
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
            (r"the comprehensive exam: \ messy data, \ a deadline", [42]), (r"EM's convergence; \ missing information", [45]),
            (r"AIPW's efficiency", [49]), (r"proximal inference: \ unmeasured confounding", [62]),
            (r"privacy noise as measurement error", [63]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-two's consulting case begins with missing values. Part "
            "forty-five studies EM's convergence and the information lost to missingness. Part forty-nine proves the "
            "augmented estimator's efficiency. Part sixty-two handles unmeasured confounding with proxies. And Part "
            "sixty-three treats the noise added for privacy as deliberate measurement error."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Rubin's factorization; complete cases "
            "selected on x; Rubin's total variance; the unbiasedness of weighting and its double robustness; regression "
            "dilution; and the matrix method. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. Little \& D. Rubin, \emph{Statistical Analysis with Missing Data} (3rd ed. 2019)",
             r"S. van Buuren, \emph{Flexible Imputation of Missing Data} (2nd ed. 2018); \ D. Rubin, \emph{Multiple Imputation for Nonresponse in Surveys} (1987)",
             r"R. Carroll, D. Ruppert, L. Stefanski \& C. Crainiceanu, \emph{Measurement Error in Nonlinear Models} (2nd ed. 2006)",
             r"National Research Council, \emph{The Prevention and Treatment of Missing Data in Clinical Trials} (2010)"],
            [r"C. Spearman (1904); \ A. Wald (1943); \ D. Rubin (1976); \ A. Dempster, N. Laird \& D. Rubin (1977); \ J. Heckman (1979)",
             r"T. Louis (1982); \ M. Mangel \& F. Samaniego (1984); \ T. Mroz (1987); \ R. Little (1988, 1993); \ X.-L. Meng (1994)",
             r"J. Robins, A. Rotnitzky \& L. P. Zhao (1994); \ J. Cook \& L. Stefanski (1994); \ A. Gelman \& T. Little (1997)",
             r"J. Barnard \& D. Rubin (1999); \ G. Molenberghs et al. (2008); \ W. Wang et al. (2015); \ K. Mohan \& J. Pearl (2021)"])
        with self.voiceover(
            "The books this part follows: Little and Rubin; van Buuren on flexible imputation, and Rubin's own book; Carroll, "
            "Ruppert, Stefanski and Crainiceanu on measurement error; and the National Research Council's report on missing "
            "data in trials; with the papers from Spearman to Mohan and Pearl."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=41, current=None)
        nxt = VGroup(label(r"Part 42", font_size=30, color=GREY_B), label(r"The Comprehensive Exam", font_size=48),
                     label(r"a client, \ messy data, \ a deadline: \ the master's milestone", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-one parts of sixty-five. <bookmark mark='a'/> What we did not see shapes what we can conclude; ask why it "
            "is missing before asking what it was. <bookmark mark='b'/> Next, the master's ends with an exam: Part "
            "forty-two, a client, messy data, and a deadline."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(41)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
