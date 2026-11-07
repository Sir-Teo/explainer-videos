from __future__ import annotations

from videos.stats.stats34.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $B$ identically distributed predictions with pairwise correlation $\rho$ average to variance $\rho\sigma^2 + (1-\rho)\sigma^2/B$.",
    r"Show that $\arg\min_F E[e^{-YF} \mid x] = \frac12 \log\{P(Y = 1 \mid x)/P(Y = -1 \mid x)\}$.",
    r"For continuous scores, \ prove $1 - \alpha \le P(S_{n+1} \le \hat q) \le 1 - \alpha + 1/(n+1)$.",
    r"Show that, \ given the calibration set, \ for i.i.d. continuous scores, the coverage $F(\hat q)$ is $\mathrm{Beta}(k, n + 1 - k)$.",
    r"Show $\hat\theta^{PP}_\lambda$ is unbiased for every fixed $\lambda$; \ find the $\lambda$ minimizing its variance.",
    r"Prove the ACI bound $|\frac1T\sum_t \mathrm{err}_t - \alpha| \le (\max(\alpha_1, 1 - \alpha_1) + \gamma)/(\gamma T)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.asthma()
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def asthma(self):
        tl = timeline(lit=(2015,)).to_edge(UP, buff=0.35)
        hc = history_card(2015, r"Rich Caruana, \ Yin Lou, \ Johannes Gehrke, \ Paul Koch, \ Marc Sturm \& No\'emie Elhadad",
                          r"An intelligible model of the risk of death from pneumonia, \ built on 14,199 patients, \ learns "
                          r"that asthma \emph{lowers} the risk. \ It is right about the data: \ asthmatics with pneumonia went "
                          r"straight to intensive care, \ and their aggressive treatment saved them", color=MISSC, width=11.4,
                          font_size=22).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(r"used to decide who can go home, \ it would have sent the asthmatics home", font_size=24, color=MISSC),
            label(r"a perfect predictor of what happened \ $\neq$ \ a guide to what to do", font_size=24, color=CALC),
        ), 12.0, 0.35, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> We end with a warning that Rich Caruana and his colleagues published in 2015. In the "
            "1990s, a large study had built models to predict which pneumonia patients were likely to die, so that the "
            "low-risk ones could be treated at home. One rule-based model learned that patients with asthma were at "
            "lower risk. Caruana's team rebuilt the analysis on over fourteen thousand patients with an intelligible "
            "model, and found the same pattern, and others like it. <bookmark mark='b'/> The model was right about the "
            "data. Asthmatics who came in with pneumonia were sent straight to intensive care and treated aggressively, "
            "and the authors proposed treatment intensity as an explanation for the association; predictive accuracy alone does not establish that causal effect. <bookmark mark='c'/> Used to decide who can go home, the "
            "model could incorrectly classify asthmatics as suitable for less intensive care. That counterfactual risk is not measured by predictive accuracy. <bookmark mark='d'/> A perfect "
            "predictor of what happened is not a guide to what to do. Prediction answers what will happen if we carry on "
            "as before. Decisions need the answer to a different question: what would happen if we acted differently."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def recap(self):
        items = [
            (r"Breiman's two cultures, \ and the replies", PREDC), (r"Rashomon: \ equal accuracy, \ different stories", TREEC),
            (r"forests: \ $\rho\sigma^2 + (1 - \rho)\sigma^2/B$", TREEC), (r"IJ intervals: \ variance, \ not bias", MISSC),
            (r"boosting: \ stagewise additive modelling", BOOSTC), (r"CV estimates Err, \ not $\mathrm{Err}_{XY}$", CALC),
            (r"calibration: \ Platt, \ isotonic, \ temperature", CALC), (r"the quantile lemma: \ split conformal", BANDC),
            (r"jackknife+ and CV+; \ CQR's adaptive bands", BANDC), (r"weighted conformal; \ adaptive conformal online", BANDC),
            (r"prediction sets; \ Mondrian; \ conformal $p$-values", BANDC), (r"PPI: \ guesses plus a rectifier; \ PPI++", GUESSC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 34, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-four in twelve lines. <bookmark mark='a'/> Breiman told statisticians that algorithms had won "
            "prediction, and Cox and Efron replied that prediction is not all of science. Many models predict equally well "
            "and tell different stories. A forest's variance is rho sigma squared plus a term that vanishes with more "
            "trees, so decorrelating the trees is what helps. The infinitesimal jackknife measures a forest's variance but "
            "not its bias. Boosting is forward stagewise additive modelling. Cross-validation estimates the error of the "
            "procedure, not of the model in hand. Probabilities can be recalibrated. The quantile lemma makes split "
            "conformal intervals valid for any model. The jackknife plus uses all the data, and conformalized quantile "
            "regression gives bands that adapt. Weighting repairs a known covariate shift, and adaptive conformal tracks a "
            "drifting stream. Prediction sets admit doubt, class by class if we ask. And prediction-powered inference "
            "turns biased guesses into valid estimates with a rectifier."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(34, r"conformal prediction: \ coverage $\ge 1 - \alpha$ for any model, \ finite $n$",
                            r"exchangeability (or a known shift); \ marginal, \ not conditional, \ coverage",
                            r"Part 57: \ what can be guaranteed with no assumptions at all, \ what cannot (Bahadur--Savage), \ and conditional guarantees over function classes")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part gave every model a finite-sample coverage guarantee."
            " <bookmark mark='b'/> It assumed exchangeability, or a shift we know, and it delivered marginal "
            "coverage, an average over the population. <bookmark mark='c'/> Part 57 asks what can be guaranteed with "
            "no assumptions at all, proves that some things cannot, starting with Bahadur and Savage's obstruction to"
            " nontrivial honest mean intervals over an unrestricted finite-mean distribution class, and finds the "
            "conditional guarantees that are possible."
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
            (r"prediction is not intervention", [35]), (r"forests and boosting as nuisance fits: \ double ML", [36]),
            (r"survival forests; \ censored conformal", [40]), (r"generalization bounds for learners", [54]),
            (r"distribution-free inference, \ proved", [57]), (r"anytime-valid inference", [58]),
            (r"distribution shift", [60]), (r"causal forests and heterogeneous effects", [62]),
            (r"LLM labels, \ PPI and its successors", [64]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 35 begins with the difference between predicting and "
            "intervening. Part 36's double machine learning uses forests and boosting to fit nuisance functions. Part 40 "
            "grows survival forests and conformal bands for censored times. Part 54 proves generalization bounds for "
            "learners. Part 57 proves the distribution-free results of this part, and their limits. Part 58's anytime-valid "
            "inference uses probability guarantees that differ from adaptive conformal’s long-run miss-frequency control. Part 60 studies distribution shift in depth. "
            "Part 62 grows causal forests for treatment effects that vary from person to person. And Part 64 returns to "
            "machine-learning labels, with language models as the labellers."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The forest's variance formula; what "
            "AdaBoost estimates; both sides of the quantile lemma; the beta distribution of conditional coverage; the "
            "prediction-powered estimator's bias and its best lambda; and the adaptive conformal bound. Pause here if you "
            "want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"V. Vovk, A. Gammerman \& G. Shafer, \emph{Algorithmic Learning in a Random World} (2005; 2nd ed. 2022)",
             r"A. Angelopoulos \& S. Bates, \emph{A Gentle Introduction to Conformal Prediction} (2023)",
             r"T. Hastie, R. Tibshirani \& J. Friedman, \emph{The Elements of Statistical Learning} (2009)",
             r"B. Efron \& T. Hastie, \emph{Computer Age Statistical Inference} (2016)"],
            [r"L. Breiman (1996, 2001, 2001b); \ G. Shmueli (2010); \ J. Friedman, T. Hastie \& R. Tibshirani (2000); \ J. Friedman (2001)",
             r"S. Wager, T. Hastie \& B. Efron (2014); \ S. Wager \& S. Athey (2018); \ E. Scornet, G. Biau \& J.-P. Vert (2015)",
             r"J. Lei et al. (2018); \ R. Barber et al. (2021); \ Y. Romano et al. (2019, 2020); \ R. Tibshirani et al. (2019); \ I. Gibbs \& E. Cand\`es (2021)",
             r"A. Angelopoulos et al. (2023); \ S. Bates, T. Hastie \& R. Tibshirani (2024); \ R. Caruana et al. (2015)"])
        with self.voiceover(
            "The books this part follows: Vovk, Gammerman and Shafer's Algorithmic Learning in a Random World; Angelopoulos "
            "and Bates's gentle introduction to conformal prediction; The Elements of Statistical Learning; and Efron and "
            "Hastie's Computer Age Statistical Inference; with the papers from Breiman to Caruana."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=34, current=None)
        nxt = VGroup(label(r"Part 35", font_size=30, color=GREY_B), label(r"What If? \ Experiments and Potential Outcomes", font_size=44),
                     label(r"what does it mean for one thing to cause another?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-four parts of sixty-five. <bookmark mark='a'/> Any black box can now come with an honest interval, and "
            "its guesses can sharpen an honest estimate. <bookmark mark='b'/> But the asthma model shows the limit of "
            "prediction: it says what happens if nothing changes. Part 35 asks what it means for one thing to cause "
            "another, and why a coin flip lets us find out. What if?"
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(34)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
