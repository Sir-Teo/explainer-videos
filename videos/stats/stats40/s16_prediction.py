from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Prediction(VoiceoverScene):
    def construct(self):
        self.card()
        self.concordance()
        self.brier()
        self.compare()
        self.brier_plot()
        self.forest()
        self.conformal()
        self.board()

    def card(self):
        card = chapter_card(15, r"Prediction", r"Who will have the event, \ and when?", lit=(1999, 2008, 2023), part=PART)
        with self.voiceover("Chapter fifteen. Prediction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def concordance(self):
        rows = [
            cmath(r"\text{usable pair}", r":", r"X_i < X_j \text{ and } i \text{ had the event}", font_size=30),
            cmath(r"C", r"=", r"P(\text{risk}_i > \text{risk}_j \mid \text{usable pair})", font_size=32),
            cmath(r"C = 0.5", r":", r"\text{a coin}; \ \ C = 1: \ \text{a perfect ranking}", font_size=30),
            cmath(r"\text{limits}", r":", r"\text{ranks only; \ depends on censoring; \ blind to calibration}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"the shorter time is seen"), why(r"Harrell et al.\ (1982)"), why(r"Part 19's AUC, \ for lifetimes"),
                why(r"Uno et al.\ (2011) fix the second")]
        with self.voiceover(
            "<bookmark mark='a'/> To judge a prognostic model, compare pairs of patients where we know who failed first: "
            "the shorter time must be an event. <bookmark mark='b'/> Frank Harrell's concordance is the share of such pairs "
            "in which the model gave the earlier failure the higher risk. <bookmark mark='c'/> One half is a coin, one is a "
            "perfect ranking: Part nineteen's area under the ROC curve, for lifetimes. <bookmark mark='d'/> But it only "
            "judges the ranking, it depends on the censoring pattern, and it cannot see whether the predicted "
            "probabilities are right."
        ) as vo:
            heading = label('Concordance measures ranking among comparable observed pairs', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def brier(self):
        rows = [
            cmath(r"\text{BS}(t)", r"=", r"\tfrac1n \textstyle\sum_i w_i(t) \big(1\{T_i > t\} - \hat S(t \mid x_i)\big)^2", font_size=30),
            cmath(r"w_i(t)", r"=", r"\dfrac{1\{T_i \le t, \delta_i = 1\}}{\hat G(T_i-)} + \dfrac{1\{T_i > t\}}{\hat G(t)}", font_size=30),
            cmath(r"\hat G", r":", r"\text{the Kaplan--Meier curve of the censoring times}", font_size=30),
            cmath(r"\text{why}", r":", r"\text{the uncensored stand in for the censored}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"Graf et al.\ (1999)"), why(r"inverse probability of censoring"), why(r"censoring as a lifetime"),
                why(r"Part 18's Horvitz--Thompson")]
        with self.voiceover(
            "<bookmark mark='a'/> The Brier score measures calibration and discrimination together: the mean squared "
            "error of the predicted probability of surviving past t. <bookmark mark='b'/> Patients censored before t "
            "have no outcome, so the others are weighted up by the inverse probability of remaining uncensored, "
            "<bookmark mark='c'/> estimated by Kaplan-Meier applied to the censoring times. <bookmark mark='d'/> It "
            "is Part eighteen's Horvitz-Thompson weighting: the weights require adequate censoring support. A pooled "
            "censoring KM assumes the relevant unconditional independence; censoring that depends on predictors needs"
            " suitable conditional weights."
        ) as vo:
            heading = label('Censoring weights require independence and follow-up support', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("predict")
        b = d["brier5"]
        rows = [[rf"PBC, \ {d['n']} patients: \ trained on two thirds, \ tested on {d['n_test']}", r"concordance", r"Brier at 5 years"],
                [r"no model \ (Kaplan--Meier)", r"0.500", f"{b['km']:.3f}"],
                [r"bilirubin alone", f"{d['c_bili']:.3f}", r"---"],
                [r"Cox, \ the five Mayo variables", f"{d['c_cox']:.3f}", f"{b['cox']:.3f}"],
                [r"random survival forest", f"{d['c_rsf']:.3f}", f"{b['rsf']:.3f}"]]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.34, colors=[GREY_A, GREY_B, MISSC, SURVC, AREAC]).move_to([0, 0.7, 0])
        if tab.width > 12.6:
            tab.width = 12.6
        foot = label(rf"the Cox model's concordance on its own training data: \ {d['c_cox_train']:.3f}", font_size=24, color=GREY_A).move_to([0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> All four hundred and sixteen PBC patients with complete data, split into a training "
            "two thirds and a test third. <bookmark mark='b'/> With no model, the concordance is one half by definition, "
            "and the five-year Brier score is " + say(b["km"], 2) + ". <bookmark mark='c'/> Bilirubin alone ranks patients "
            "with a concordance of " + say(d["c_bili"], 2) + ". <bookmark mark='d'/> The Mayo Cox model reaches "
            + say(d["c_cox"], 2) + " on new patients, and cuts the Brier score to " + say(b["cox"], 2) + ". <bookmark mark='e'/> A random survival forest, a hundred and fifty trees split by log-rank statistics,"
            " does a little worse on this one seeded split: with five well-chosen variables and a few hundred "
            "patients, the old model is hard to beat."
        ) as vo:
            self.add(pbc_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def brier_plot(self):
        d = load("predict")
        ts = np.asarray(d["times"], float)
        A = axes([0, 10], [0, 0.3], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"IPCW Brier score \ (lower is better)",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.1, 0.2, 0.3], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        cs = {k: polyline(ax, ts, np.asarray(d["brier_t"][k], float), c, 3) for k, c in (("km", GREY_B), ("cox", SURVC), ("rsf", AREAC))}
        dots = {k: VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=c) for a, b in zip(ts, d["brier_t"][k])]) for k, c in (("km", GREY_B), ("cox", SURVC), ("rsf", AREAC))}
        side = fit_rows(VGroup(
            label(r"grey: \ no covariates", font_size=22, color=GREY_B),
            label(r"blue: \ Cox", font_size=22, color=SURVC),
            label(r"purple: \ the forest", font_size=22, color=AREAC),
            label(r"0.25 is a coin at $S = 1/2$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Brier score over time, on the test patients. Without covariates it climbs toward "
            "one quarter, the score of a coin, as survival approaches one half. <bookmark mark='b'/> The Cox model stays "
            "well below it at every horizon, <bookmark mark='c'/> and the forest stays a little above Cox."
        ) as vo:
            self.add(pbc_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cs["km"]), FadeIn(dots["km"]), FadeIn(side[0]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(Create(cs["cox"]), FadeIn(dots["cox"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["rsf"]), FadeIn(dots["rsf"]), FadeIn(side[2]))
        self.clear_scene()

    def forest(self):
        rows = fit_rows(VGroup(
            label(r"random survival forests \ (Ishwaran et al.\ 2008): \ trees split by the log-rank statistic", font_size=26, color=AREAC),
            label(r"each leaf: \ a Nelson--Aalen curve; \ the forest: \ their average", font_size=26),
            label(r"also: \ boosting Cox's partial likelihood; \ neural nets for hazards \ (DeepSurv)", font_size=26, color=GREY_A),
            label(r"potential gains with interactions and enough events; validate out of sample", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hemant Ishwaran's random survival forests grow trees whose splits maximize a "
            "log-rank statistic. <bookmark mark='b'/> Each leaf holds a Nelson-Aalen curve, and the forest averages "
            "them. <bookmark mark='c'/> Others boost Cox's partial likelihood, or fit hazards with neural networks. "
            "<bookmark mark='d'/> They can help when there are many variables, real interactions, and enough events "
            "to learn them; with a few strong predictors, as in PBC, a well-specified Cox model is hard to improve "
            "on."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def conformal(self):
        rows = [
            cmath(r"\text{goal}", r":", r"L(x) \text{ with } P(T \ge L(X)) \ge 1 - \alpha, \ \text{under exchangeability and censoring conditions}", font_size=30),
            cmath(r"\text{problem}", r":", r"\text{censored calibration times hide } T", font_size=30),
            cmath(r"\text{fix}", r":", r"\text{use } T \wedge c_0 \text{ for units with } C \ge c_0, \ \text{weighted by } 1/P(C \ge c_0 \mid x)", font_size=28),
            cmath(r"L(x)", r"=", r"\min\big(q(x) - \hat\eta, \ c_0\big): \ \text{Part 34's split conformal}", font_size=30),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"a lower prediction bound"), why(r"the score needs $T$"), why(r"Cand\`es, \ Lei \& Ren (2023)"),
                why(r"a model's $q$, \ corrected")]
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-four's conformal prediction can be carried over. The goal is a lower "
            "bound on a new patient's lifetime with ninety percent marginal coverage under exchangeability, a "
            "predictor trained separately, and the required censoring assumptions; it is not a conditional guarantee "
            "for every patient. <bookmark mark='b'/> The difficulty is that censoring hides the calibration patients'"
            " lifetimes. <bookmark mark='c'/> Emmanuel Candès, Lihua Lei and Zhimei Ren's answer: pick a threshold c "
            "nought, use only calibration patients whose censoring time exceeds it, for whom the lifetime capped at c"
            " nought is seen, and weight them by the inverse chance of being so lucky. <bookmark mark='d'/> The "
            "demonstration has known censoring times, even for early failures, and censoring independent of "
            "covariates and lifetimes, so weights are constant. With known correct censoring weights the model can be"
            " arbitrary; estimated weights do not generally give exact finite-sample coverage. Then calibrate its "
            "quantile as in split conformal."
        ) as vo:
            heading = label('Censored conformal bounds need known censoring information', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("conformal", "Cox Wald")
        text = (
            "<bookmark mark='a'/> The Coverage Board. Cox's Wald interval for a log hazard ratio, with sixty patients and "
            "a third censored, keeps its promise. <bookmark mark='b'/> And the conformal lower bound, built on a "
            "deliberately wrong quantile model and calibrated under censoring, covers ninety percent, as promised."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1])])
