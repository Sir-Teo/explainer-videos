from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class Weighting(VoiceoverScene):
    def construct(self):
        self.card()
        self.ipw()
        self.dictionary()
        self.aipw()
        self.results()
        self.dr_table()
        self.calibration()
        self.weights()
        self.balance()
        self.board()

    def card(self):
        card = chapter_card(5, r"Weighting is causal inference", r"Respondents stand in for the missing", lit=(1994,), part=PART)
        with self.voiceover("Chapter five. Weighting is causal inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ipw(self):
        rows = [
            cmath(r"\pi(x)", r"=", r"P(R = 1 \mid X = x)", font_size=32),
            cmath(r"E\Big[\dfrac{R\, Y}{\pi(X)}\Big]", r"=", r"E\Big[\dfrac{E(R \mid X, Y)}{\pi(X)}\, Y\Big] = E[Y] \ \text{under MAR}", font_size=30),
            cmath(r"\hat\mu_{\text{IPW}}", r"=", r"\textstyle\sum_i \dfrac{R_i Y_i}{\hat\pi_i} \Big/ \textstyle\sum_i \dfrac{R_i}{\hat\pi_i}", font_size=30),
            cmath(r"\text{each respondent}", r":", r"\text{counts for } 1/\hat\pi \text{ people like them}", font_size=30),
        ]
        rows[2][-1].set_color(IPWC)
        whys = [why(r"the response propensity"), why(r"MAR: $E(R \mid X, Y) = \pi(X)$"), why(r"Hajek's weighted mean"), why(r"Part 18's Horvitz--Thompson")]
        with self.voiceover(
            "<bookmark mark='a'/> Weighting attacks the problem from the other side. Model the chance of responding "
            "given the always-observed variables. <bookmark mark='b'/> Under missing at random, weighting each "
            "respondent's value by one over that chance with the known true response probability gives an unbiased "
            "Horvitz-Thompson mean, under positivity and suitable moments. <bookmark mark='c'/> The normalized Hájek "
            "version divides by the sum of the weights; it and estimators using fitted probabilities generally have "
            "finite-sample bias but can be consistent. <bookmark mark='d'/> Each respondent stands in for one over pi"
            " people like them: Part eighteen's Horvitz-Thompson estimator, with the response propensity in place of "
            "a designed inclusion probability."
        ) as vo:
            heading = label('Response weighting needs MAR and positive response probabilities', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dictionary(self):
        rows = [[r"missing data", r"causal inference \ (Parts 35--36)"],
                [r"responding, \ $R = 1$", r"being treated, \ $A = 1$"],
                [r"$Y$ for non-respondents", r"the unobserved potential outcome"],
                [r"MAR", r"no unmeasured confounding"],
                [r"response propensity", r"propensity score"],
                [r"IPW, \ AIPW", r"IPW, \ AIPW"]]
        tab = table_rows(rows, font_size=26, col_buff=1.4, row_buff=0.32, colors=[GREY_A, None, None, MIC, IPWC, TAUC]).move_to([0, 0.6, 0])
        foot = label(r"a potential outcome is a missing value: \ causal inference is a missing-data problem", font_size=24, color=TAUC).move_to([0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This is causal inference in disguise, or the other way round. <bookmark mark='b'/> "
            "Responding plays the role of being treated; the outcome of a non-respondent is an unseen potential outcome; "
            "missing at random is no unmeasured confounding; the response propensity is the propensity score; and the "
            "estimators are the same. <bookmark mark='c'/> Rubin built the potential-outcome framework and the theory of "
            "missing data at the same time, because a potential outcome you did not observe is a missing value."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.4), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def aipw(self):
        rows = [
            cmath(r"\hat\mu_{\text{AIPW}}", r"=", r"\tfrac1n \textstyle\sum_i \Big[\hat m(X_i) + \dfrac{R_i (Y_i - \hat m(X_i))}{\hat\pi(X_i)}\Big]", font_size=30),
            cmath(r"\hat m \text{ right}", r":", r"\text{the correction averages to } 0", font_size=30),
            cmath(r"\hat\pi \text{ right}", r":", r"\text{the correction removes } \hat m\text{'s bias}", font_size=30),
            cmath(r"\text{both right}", r":", r"\text{the smallest variance among such estimators}", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"Robins, \ Rotnitzky \& Zhao (1994)"), why(r"outcome model"), why(r"response model"), why(r"Part 49's efficiency")]
        with self.voiceover(
            "<bookmark mark='a'/> The augmented estimator of James Robins, Andrea Rotnitzky and Lue Ping Zhao "
            "combines both approaches: predict everyone's outcome from a regression, then correct the predictions by "
            "the weighted residuals of the respondents. <bookmark mark='b'/> If the outcome model is right, the "
            "correction averages to zero. <bookmark mark='c'/> If the response model is right, the correction removes"
            " the outcome model's bias. <bookmark mark='d'/> Consistent if either is right, double robustness, under "
            "regularity and suitable nuisance-estimation rates, when both are right it attains the semiparametric "
            "efficiency bound, a fact Part forty-nine explains."
        ) as vo:
            heading = label('Double robustness concerns consistency under nuisance conditions', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def results(self):
        d = load("mech")
        t = d["truth"]
        A = axes([10.3, 10.7], [0, 4], x_length=8.0, y_length=3.8, xlabel=r"mean log income", ylabel=r"",
                 xticks=[10.3, 10.4, 10.5, 10.6, 10.7], yticks=[], xfmt=lambda v: f"{v:.1f}", center=[0.8, 0.2, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(t, 0), ax.c2p(t, 4), color=TRUEC, stroke_width=2.5)
        g = VGroup()
        for k, (key, name) in enumerate((("mcar", r"MCAR"), ("mar", r"MAR"), ("mnar", r"MNAR"))):
            yv = 3.3 - k * 1.15
            row = VGroup(label(name, font_size=24, color=GREY_A).next_to(ax.c2p(10.3, yv), LEFT, buff=0.3))
            for off, (val, col) in zip((0.22, 0.0, -0.22), ((d[key]["cc"], CCC), (d[key]["mi"], MIC), (d[key]["ipw"], IPWC))):
                row.add(Dot(ax.c2p(val, yv + off), radius=0.09, color=col))
            g.add(row)
        key = label(r"red: \ complete cases; \ green: \ MI; \ purple: \ IPW", font_size=22, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> All three methods on the World's three masks. <bookmark mark='b'/> Under the coin, "
            "all agree with the truth. <bookmark mark='c'/> Under missing at random, multiple imputation and "
            "weighting both remove the complete cases' bias. <bookmark mark='d'/> Under missing not at random, all "
            "three are equally wrong. These implementations do not correct this MNAR mechanism; other identifying "
            "restrictions or validation information could change what is recoverable."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(truth), FadeIn(key))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(g[k]))
        self.clear_scene()

    def dr_table(self):
        d = load("weight")
        rows = [[r"MAR mask: \ mean log income", r"estimate", r"error"],
                [r"complete cases", f"{d['cc']:.4f}", f"{d['cc'] - d['truth']:+.4f}"],
                [r"IPW, \ right response model", f"{d['ipw_right']['est']:.4f}", f"{d['ipw_right']['est'] - d['truth']:+.4f}"],
                [r"IPW, \ wrong response model", f"{d['ipw_wrong']['est']:.4f}", f"{d['ipw_wrong']['est'] - d['truth']:+.4f}"],
                [r"AIPW, \ right response, \ wrong outcome", f"{d['aipw_rw']['est']:.4f}", f"{d['aipw_rw']['est'] - d['truth']:+.4f}"],
                [r"AIPW, wrong response, rich working outcome", f"{d['aipw_wr']['est']:.4f}", f"{d['aipw_wr']['est'] - d['truth']:+.4f}"],
                [r"AIPW, \ both wrong", f"{d['aipw_ww']['est']:.4f}", f"{d['aipw_ww']['est'] - d['truth']:+.4f}"]]
        tab = table_rows(rows, font_size=26, col_buff=1.0, row_buff=0.28, colors=[GREY_A, CCC, IPWC, MNC, MIC, MIC, MNC]).move_to([0, 0.6, 0])
        foot = label(rf"the truth: {d['truth']:.4f}; finite-sample agreement is not proof of nuisance correctness", font_size=24, color=TRUEC).move_to([0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Double robustness in numbers, on the missing-at-random mask. <bookmark mark='b'/> "
            "Weighting with the right response model, which uses age and region, removes the bias; with a wrong one, "
            "built on BMI, it does not. <bookmark mark='c'/> In this finite example, the rich outcome regression is a"
            " working approximation, not the simulator’s known exact conditional mean. The double-robustness theorem "
            "concerns consistency if either nuisance model is correct: wrong outcome with right weights, or right "
            "outcome with wrong weights. <bookmark mark='d'/> With both wrong, it fails like the rest."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]))
            vo.wait_until("d")
            self.play(FadeIn(tab[6]))
        self.clear_scene()

    def weights(self):
        d = load("weight")
        rows = fit_rows(VGroup(
            label(rf"here: \ the largest weight is {d['max_w']:.1f}; \ {d['n_obs']:,} respondents count as {d['ess']:,.0f} by Kish's formula", font_size=26, color=IPWC),
            label(r"with stronger selection, \ a few respondents carry huge weights: \ the variance explodes", font_size=26, color=MNC),
            label(r"remedies: \ trim or stabilize weights; \ prefer AIPW; \ check overlap \ (Part 36)", font_size=26, color=TAUC),
            label(r"MI and weighting assume the same thing \ (MAR); \ they model different parts", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Weights cost precision. Here the largest is " + say(d["max_w"], 1) + ", and the "
            + f"{d['n_obs']:,}" + " respondents have a weight-only Kish effective sample size of about " + f"{d['ess']:,.0f}" + " units. This is a diagnostic, not a universal equivalence in outcome precision. <bookmark mark='b'/> "
            "With stronger selection, a few respondents can carry enormous weights, and the variance explodes. "
            "<bookmark mark='c'/> The remedies are those of Part thirty-six: check overlap and consider augmentation "
            "or carefully justified weight modification. Trimming can introduce bias or change the target; "
            "multiplying all normalized weights by one constant does not fix extreme relative weights. <bookmark "
            "mark='d'/> Imputation and weighting assume the same thing, missing at random; they differ in which part "
            "of the problem they model."
        ) as vo:
            self.add(missing_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("AIPW")
        text = (
            "<bookmark mark='a'/> On the Board, in chapter two's design with three hundred units and strong "
            "selection, the augmented estimator's interval, from its influence function, covers a little less than "
            "promised: the large weights make the normal approximation optimistic at this sample size. Double-robust "
            "consistency is not a finite-sample unbiasedness or coverage guarantee, and this study does not isolate "
            "every source of undercoverage."
        )
        show_board(self, rows, text, [("a", [0])])

    def calibration(self):
        rows = fit_rows(VGroup(
            label(r"calibration weighting: \ adjust weights so the sample matches known totals", font_size=26, color=IPWC),
            label(r"raking \ (Part 18) \ is one; \ GREG is another", font_size=26, color=None),
            label(r"suitable calibration equations can imply a response model under stated conditions", font_size=26, color=TAUC),
            label(r"model-assisted robustness depends on the calibration and response assumptions \ (Deville \& S\"arndal 1992)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Survey statisticians usually weight differently: they adjust the weights so that "
            "the sample reproduces known population totals, by age, sex or region. <bookmark mark='b'/> Raking, from "
            "Part eighteen, is one such calibration, and the generalized regression estimator is another. <bookmark "
            "mark='c'/> For suitable calibration distances and model classes, calibration equations can be related to"
            " an implied response model; <bookmark mark='d'/> and Jean-Claude Deville and Carl-Erik Särndal developed"
            " the calibration framework. Consistency under either an implied response model or a suitable linear "
            "outcome model needs the relevant design, support and calibration assumptions; arbitrary calibration "
            "weights are not automatically doubly robust."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def balance(self):
        rows = fit_rows(VGroup(
            label(r"check the weights as Part 36 checked propensity scores: \ balance", font_size=26, color=TAUC),
            label(r"after weighting, \ respondents should look like everyone on the observed variables", font_size=26, color=None),
            label(r"here: \ the weighted respondents' mean age matches the full sample's", font_size=26, color=MIC),
            label(r"balance on what we see is necessary, \ never sufficient", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Weights should be checked the way Part thirty-six checked propensity scores, by "
            "balance. <bookmark mark='b'/> After weighting, the respondents should resemble the whole sample on every"
            " observed variable: age, sex, region. <bookmark mark='c'/> On the World's survey, the weighted "
            "respondents' age distribution matches the full sample's, while the unweighted one is several years too "
            "old. <bookmark mark='d'/> Balance is a useful diagnostic; exact finite-sample balance is not necessary "
            "for every valid estimated-propensity procedure. It is never sufficient, because the assumption that "
            "matters is about what we do not see."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

