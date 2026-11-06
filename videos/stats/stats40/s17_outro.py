from __future__ import annotations

from videos.stats.stats40.common import *  # noqa: F403

PROBLEMS = [
    r"With no censoring, \ show the Kaplan--Meier estimate is the empirical survival function $\#\{T_i > t\}/n$.",
    r"Exponential lifetimes, \ right censoring: \ show $\hat\lambda = d / \sum_i x_i$ and $\text{Var}(\hat\lambda) \approx \lambda^2 / d$.",
    r"Two groups, \ no ties: \ show Cox's score at $\beta = 0$ is $\sum_k (d_{1k} - n_{1k}/n_k)$, \ the log-rank O $-$ E.",
    r"Weibull: \ show $\log T = x^\top\gamma + \sigma W$ has proportional hazards with $\beta = -\gamma/\sigma$.",
    r"Gamma frailty: \ show the population hazard is $h_0(t)/(1 + \theta H_0(t))$.",
    r"Show $E \min(T, \tau) = \int_0^\tau S(t)\, dt$.",
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
            (r"6-MP: \ twelve open rings", MPC), (r"$S$, \ $h$, \ $H$; \ Graunt and Gompertz", HAZC),
            (r"censoring and truncation, \ handled", CENSC), (r"Kaplan--Meier: \ the risk set's product", SURVC),
            (r"Greenwood; \ use log-log", SURVC), (r"Nelson--Aalen: \ the hazard, \ summed", HAZC),
            (r"martingales: \ observed minus expected", TAUC), (r"log-rank: \ 16.8 on Gehan's data", TAUC),
            (r"Cox: \ $h_0$ cancels; \ the Mayo model", SURVC), (r"checking PH; \ Karnofsky fades", MISSC),
            (r"hazard ratios select; \ RMST; \ immortal time", MISSC), (r"AFT, \ competing risks, \ frailty, \ prediction", CIFC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 40, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part forty in twelve lines. <bookmark mark='a'/> Twelve children still in remission made the average "
            "remission impossible to compute naively. The survival function, the hazard and the cumulative hazard are "
            "three faces of one distribution, and Gompertz's law gives the shape of adult mortality. Censoring and "
            "truncation must be handled, never ignored. Kaplan and Meier multiply conditional survivals over the risk "
            "sets, and Greenwood's formula gives their variance; use the log-log interval when the risk set is small. "
            "Nelson and Aalen sum the hazard instead. Counting processes make every estimator observed minus expected, "
            "a martingale. The log-rank test sums observed minus expected over the event times. Cox's partial "
            "likelihood removes the baseline hazard, and gave medicine the Mayo model. Schoenfeld residuals check "
            "proportional hazards, and showed the Karnofsky effect fading. Hazard ratios select their survivors, so "
            "report restricted means, and never let future treatment classify the past. And accelerated failure time "
            "models, competing risks, frailty and honest prediction complete the toolkit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(40, r"lifetimes partly seen: \ censoring that says ``at least this long''",
                            r"censoring independent of the lifetime, \ given covariates",
                            r"Part 41: \ data missing for reasons that may matter: \ MAR, \ multiple imputation, \ measurement error")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part handled lifetimes we see only in part. <bookmark mark='b'/> "
            "Everything rested on one untestable assumption: that censoring is independent of the lifetime, given the "
            "covariates. <bookmark mark='c'/> Part forty-one takes up missing data in general, where that assumption has a "
            "name, missing at random, and the tools are weighting, imputation and sensitivity analysis."
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
            (r"censoring as missing data; \ IPCW", [41]), (r"martingales, \ counting processes, \ Rebolledo", [44]),
            (r"the Kaplan--Meier process", [48]), (r"Cox as a semiparametric model", [49]),
            (r"group-sequential survival trials", [58]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-one treats censoring as one kind of missing data, and "
            "its weights as inverse probability weights. Part forty-four proves the martingale theory behind every "
            "estimator here. Part forty-eight studies the Kaplan-Meier curve as a random function. Part forty-nine shows "
            "why Cox's estimator is efficient in a semiparametric model. And Part fifty-eight monitors survival trials as "
            "the data accumulate."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Kaplan-Meier without censoring; the "
            "exponential rate under censoring; Cox's score test as the log-rank test; the Weibull as both a proportional "
            "hazards and an accelerated failure time model; the gamma frailty's population hazard; and the restricted mean "
            "as an area. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Kalbfleisch \& R. Prentice, \emph{The Statistical Analysis of Failure Time Data} (2nd ed. 2002)",
             r"T. Fleming \& D. Harrington, \emph{Counting Processes and Survival Analysis} (1991)",
             r"T. Therneau \& P. Grambsch, \emph{Modeling Survival Data: Extending the Cox Model} (2000)",
             r"O. Aalen, \O. Borgan \& H. Gjessing, \emph{Survival and Event History Analysis} (2008)"],
            [r"M. Greenwood (1926); \ E. Kaplan \& P. Meier (1958); \ E. Freireich et al. (1963); \ E. Gehan (1965); \ N. Mantel (1966)",
             r"D. Cox (1972, 1975); \ B. Efron (1977); \ J. Crowley \& M. Hu (1977); \ O. Aalen (1978); \ J. Vaupel et al. (1979)",
             r"D. Schoenfeld (1982); \ P. Andersen \& R. Gill (1982); \ P. Grambsch \& T. Therneau (1994); \ J. Fine \& R. Gray (1999)",
             r"D. Redelmeier \& S. Singh (2001); \ S. Suissa (2008); \ M. Hern\'an (2010); \ E. Cand\`es, L. Lei \& Z. Ren (2023)"])
        with self.voiceover(
            "The books this part follows: Kalbfleisch and Prentice; Fleming and Harrington on counting processes; "
            "Therneau and Grambsch on extending Cox's model; and Aalen, Borgan and Gjessing on event history analysis; "
            "with the papers from Greenwood to conformal survival."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=40, current=None)
        nxt = VGroup(label(r"Part 41", font_size=30, color=GREY_B), label(r"What You Didn't See", font_size=48),
                     label(r"missing data, \ multiple imputation, \ and measurement error", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty parts of sixty-five. <bookmark mark='a'/> A censored time is not a missing value but a partial one, and "
            "the risk set is how to use it. <bookmark mark='b'/> Next, data that are missing for reasons that may matter: "
            "Part forty-one, what you didn't see."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(40)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
