from __future__ import annotations

from videos.stats.stats49.common import *  # noqa: F403


class MissingData(VoiceoverScene):
    def construct(self):
        self.card()
        self.eif()
        self.survey()
        self.robust()
        self.imputation()
        self.general()

    def card(self):
        card = chapter_card(9, r"Missing data, \ semiparametrically", r"Robins, \ Rotnitzky \& Zhao's augmented weights", lit=(1994,), part=PART)
        with self.voiceover("Chapter nine. Missing data, semiparametrically: Robins, Rotnitzky and Zhao's augmented weights."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def eif(self):
        rows = [
            cmath(r"\psi = E\,Y", r",", r"R = \mathbf 1\{Y \text{ seen}\}, \ \ P(R = 1 \mid X, Y) = \pi(X): \ \text{MAR}", font_size=32),
            cmath(r"\phi^*", r"=", r"m(X) + \frac{R}{\pi(X)}(Y - m(X)) - \psi, \ \ m(x) = E[Y \mid X = x, R = 1]", font_size=30),
            cmath(r"E\,\phi^{*2}", r"=", r"\mathrm{Var}\, m(X) + E\Big[\frac{\sigma^2(X)}{\pi(X)}\Big]", font_size=34),
            cmath(r"\text{the same shape as the ATE}", r":", r"\text{one arm, \ with } \pi \text{ for } e", font_size=32),
        ]
        rows[1][-1].set_color(EFFC)
        rows[2][-1].set_color(TANC)
        whys = [why(r"Part 41's missing at random"), why(r"Robins, \ Rotnitzky \& Zhao (1994)"), why(r"the bound: \ what was lost"), why(r"Tsiatis (2006): \ one theory")]
        heading = label('Under MAR, augment weighted residuals with a regression prediction', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-one's problem: estimate the mean of Y when some values are missing at random given always-observed covariates X, so that the chance of seeing Y depends only on X, with positive response probabilities and finite influence-function variance. <bookmark mark='b'/> The efficient influence function, found by James Robins, Andrea Rotnitzky and Lue Ping Zhao in 1994, is the regression prediction plus the inverse-probability-weighted residual of the observed cases. <bookmark mark='c'/> Its variance is the bound: the variance of the regression function plus the residual variance inflated by one over the response probability. <bookmark mark='d'/> It is the average treatment effect's influence function with one arm, and Anastasios Tsiatis's 2006 book develops the whole theory of missing data and causal inference this way, as one theory."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def survey(self):
        d = load("mar")
        e = d["est"]
        t = d["truth"]
        rows = [[r"estimator of mean log income", r"estimate", r"error"],
                [r"complete cases", f"{e['cc']:.4f}", f"{e['cc'] - t:+.4f}"],
                [r"IPW, \ logistic $\hat\pi$", f"{e['ipw']:.4f}", f"{e['ipw'] - t:+.4f}"],
                [r"regression imputation", f"{e['reg']:.4f}", f"{e['reg'] - t:+.4f}"],
                [r"AIPW", f"{e['aipw']:.4f} $\\pm$ {1.645 * e['aipw_se']:.4f}", f"{e['aipw'] - t:+.4f}"],
                [r"the truth \ (all 2,000)", f"{t:.4f}", r""]]
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.34, colors=[GREY_B, NUIC, None, None, EFFC, TANC])
        tab.move_to([0, 0.7, 0])
        foot = label(rf"the World's survey: \ {d['n']:,} adults, \ {d['n_obs']:,} answer; \ the young and two regions answer less", font_size=24, color=GREY_A).move_to([0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The World's survey of Part forty-one: {d['n']:,} adults, of whom {d['n_obs']:,} report their income; the young, and the people of two regions, answer less often, and their incomes differ. Complete cases overstate mean log income by {say(e['cc'] - t, 3)}. Inverse probability weighting, regression imputation and the augmented estimator all reduce the realized error in this example, and the augmented estimator's ninety percent interval contains the complete survey-sample mean in this draw. Its influence-function SE is an iid superpopulation reference; it is not an exact interval for a fixed finite survey."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"the World: \ one draw, \ truth known")))
        self.wait(2.0)
        self.clear_scene()

    def robust(self):
        d = load("mar")
        t = d["truth"]
        rows = [
            cmath(r"\text{both models fitted}", r":", rf"\text{{AIPW error }} {d['est']['aipw'] - t:+.4f}", font_size=34),
            cmath(r"\text{outcome model wrong (sex only)}", r":", rf"\text{{regression }} {d['wrong_om']['reg'] - t:+.4f}, \ \text{{AIPW }} {d['wrong_om']['aipw'] - t:+.4f}", font_size=32),
            cmath(r"\text{response model wrong (a constant)}", r":", rf"\text{{IPW }} {d['wrong_ps']['ipw'] - t:+.4f}, \ \text{{AIPW }} {d['wrong_ps']['aipw'] - t:+.4f}", font_size=32),
            cmath(r"\text{true } \pi \text{ instead of } \hat\pi", r":", rf"\text{{SE }} {d['true_e']['aipw_se']:.4f} \ \text{{vs.\ }} {d['est']['aipw_se']:.4f}", font_size=32),
        ]
        rows[1][-1].set_color(TANC)
        rows[2][-1].set_color(TANC)
        whys = [why(r"the efficient one"), why(r"the propensity rescues it"), why(r"the regression rescues it"), why(r"with a good outcome model, \ it hardly matters")]
        heading = label('A single survey draw illustrates working-model sensitivity', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> Double robustness on the survey. With both working models fitted, the augmented estimator "
            f"is off by {say(d['est']['aipw'] - t, 4)}. <bookmark mark='b'/> Replace the outcome model with one that uses "
            f"only sex: regression imputation alone is now as biased as the complete cases, but the augmented estimator, "
            f"rescued by the response model, barely moves. <bookmark mark='c'/> Replace the response model by a constant: "
            f"weighting alone collapses to the complete cases, but the augmented estimator, rescued by the regression, is "
            f"fine. <bookmark mark='d'/> And with a good outcome model it hardly matters whether the response probabilities are "
            f"known or estimated: the standard errors are {say(d['true_e']['aipw_se'], 4)} and {say(d['est']['aipw_se'], 4)}. "
            f"The efficient influence function depends on the propensity only through a term that the regression has "
            f"already made small."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def imputation(self):
        rows = [
            cmath(r"\text{multiple imputation (Part 41)}", r":", r"\text{can be efficient with proper congenial imputation}", font_size=32),
            cmath(r"\text{AIPW}", r":", r"\text{efficient if both are right, \ consistent if either is}", font_size=32),
            cmath(r"\text{Hajek IPW}", r":", r"\text{normalized known-}\pi\text{: inefficient unless augmentation vanishes}", font_size=30),
            cmath(r"\mathrm{Var}\,\phi_{\text{HT}} - \mathrm{Var}\,\phi^*", r"=", r"E\Big[\frac{1 - \pi(X)}{\pi(X)}\, m(X)^2\Big]: \ \text{the price of ignoring } m", font_size=30),
        ]
        rows[1][-1].set_color(EFFC)
        rows[2][-1].set_color(NUIC)
        whys = [why(r"a parametric bet"), why(r"two bets, \ hedged"), why(r"one bet, \ wasteful"), why(r"by Pythagoras, \ chapter 3")]
        heading = label('Compare known-propensity influence functions and augmentation', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> How does this compare with Part forty-one's multiple imputation? Proper multiple imputation can be efficient under a correct, congenial model and suitable inference, but it is a single bet on that model. <bookmark mark='b'/> The augmented estimator hedges: efficient when both working models are right, and still consistent when either one is. <bookmark mark='c'/> Weighting alone is consistent when the response model is right, but it ignores what the covariates say about the outcome, and is the normalized known-propensity estimator is inefficient unless its augmentation term vanishes. Estimated propensity fitting can change this comparison. <bookmark mark='d'/> For the Horvitz–Thompson form the waste is exactly the expected value of one minus pi over pi times the squared regression: the squared distance from its influence function to the efficient one, chapter three's Pythagoras again."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def general(self):
        rows = fit_rows(VGroup(
            label(r"Robins--Rotnitzky--Zhao: \ every regular estimator under MAR is an IPW estimator plus an augmentation", font_size=26),
            label(r"the optimal augmentation is $-\big(\tfrac{R}{\pi} - 1\big) m(X)$: \ augmentation subspace $\{(R/\pi-1)a(X)\}$", font_size=26, color=EFFC),
            label(r"monotone dropout, \ longitudinal data, \ survival with censoring: \ the same recipe", font_size=26, color=TANC),
            label(r"MNAR without extra restrictions: \ generally not identified; \ sensitivity analysis \ (Part 41) \ is the honest answer", font_size=26, color=NUIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Robins, Rotnitzky and Zhao proved more: under missing at random, regular asymptotically linear observed-data influence functions have an inverse-probability-weighted plus augmentation representation under suitable MAR conditions. <bookmark mark='b'/> The best augmentation is a projection, onto the functions of the response indicator and the covariates, and it is the regression term of the efficient influence function. <bookmark mark='c'/> The same recipe handles monotone dropout, longitudinal studies and censored survival data. <bookmark mark='d'/> Without additional identifying restrictions, missing-not-at-random data generally do not identify the population mean, and no efficiency theory helps: Part forty-one's sensitivity analysis is the honest answer."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
