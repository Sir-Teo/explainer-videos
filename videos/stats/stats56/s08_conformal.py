from __future__ import annotations

from videos.stats.stats56.common import *  # noqa: F403


class ConformalSelection(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.pvalues()
        self.proof()
        self.example()
        self.shift()
        self.lesson()

    def card(self):
        card = chapter_card(7, r"Conformal selection", r"Choosing units, \ not variables, \ with FDR control", lit=(2023,), part=PART)
        with self.voiceover("Chapter seven. Conformal selection: choosing units, not variables, with false discovery rate control."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\text{test units } j = 1, \dots, m", r":", r"X_j \text{ observed, \ } Y_j \text{ not yet}", font_size=34),
            cmath(r"\text{goal}", r":", r"\text{select those with } Y_j > c, \ \ E\Big[\frac{\#\{j \in \hat S: Y_j \le c\}}{|\hat S| \vee 1}\Big] \le q", font_size=32),
            cmath(r"\text{tools}", r":", r"\text{any predictor } \hat\mu, \ \text{a labelled calibration set, \ exchangeable}", font_size=32),
            cmath(r"\text{examples}", r":", r"\text{hiring, \ drug screening, \ biopsies}", font_size=30),
        ]
        rows[1][-1].set_color(HYBC)
        whys = [why(r"Jin \& Cand\`es (2023)"), why(r"an FDR over units"), why(r"Part 34's conformal assumptions"), why(r"a screening decision")]
        with self.voiceover(
            "<bookmark mark='a'/> A different kind of selection. Ying Jin and Emmanuel Candès considered test units whose "
            "features are seen but whose outcomes are not yet known. <bookmark mark='b'/> The goal is to select the units "
            "whose outcome exceeds a threshold c, while controlling the false discovery rate: the expected fraction of "
            "selected units that do not. <bookmark mark='c'/> The tools are any prediction model and a labelled calibration "
            "set, exchangeable with the test units, as in Part thirty-four. <bookmark mark='d'/> Which candidates to "
            "interview, which compounds to send to the laboratory, which tumours to biopsy."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pvalues(self):
        rows = [
            cmath(r"V_j = \hat\mu(X_j)", r":", r"\text{a score: \ larger means more promising}", font_size=34),
            cmath(r"p_j", r"=", r"\frac{1 + \#\{i \text{ in calibration}: Y_i \le c, \ V_i \ge V_j\}}{n + 1}", font_size=34),
            cmath(r"\text{if } Y_j \le c", r":", r"P(p_j \le t) \le t: \ \text{a valid conformal } p\text{-value}", font_size=34),
            cmath(r"\hat S", r"=", r"\text{Benjamini--Hochberg at level } q \text{ on } p_1, \dots, p_m", font_size=34),
        ]
        rows[1][-1].set_color(CONDC)
        rows[3][-1].set_color(HYBC)
        whys = [why(r"any model, \ trained elsewhere"), why(r"rank among the calibration nulls"), why(r"exchangeability"), why(r"Part 33's procedure")]
        with self.voiceover(
            "<bookmark mark='a'/> Score each unit with the predictor: a larger score means more promising. <bookmark "
            "mark='b'/> For each test unit, the conformal p-value is one plus the number of calibration units that are below "
            "the threshold yet scored at least as high, over n plus one. <bookmark mark='c'/> For a test unit that is truly "
            "below the threshold, this p-value is valid by exchangeability, whatever the predictor. <bookmark mark='d'/> Then "
            "run Benjamini–Hochberg on the test p-values."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\text{the catch}", r":", r"\text{the } p_j \text{ share one calibration set: \ dependent}", font_size=34),
            cmath(r"\text{but}", r":", r"\text{they are PRDS \ (positively dependent) \ in the nulls}", font_size=34),
            cmath(r"\text{BH under PRDS}", r":", r"\text{FDR} \le q \ \ (\text{Benjamini \& Yekutieli 2001})", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{finite-sample FDR control, \ any model, \ any } m", font_size=34),
        ]
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"a common reference"), why(r"Bates et al. (2023); \ Jin \& Cand\`es"), why(r"Part 33"), why(r"distribution-free")]
        with self.voiceover(
            "<bookmark mark='a'/> The catch is that all the p-values are computed against the same calibration set, so they "
            "are dependent. <bookmark mark='b'/> Stephen Bates and colleagues, and Jin and Candès, showed the dependence is of the benign kind, positive "
            "regression dependence on a subset, for the null p-values. <bookmark mark='c'/> And under that condition, "
            "Benjamini and Yekutieli proved in 2001 that Benjamini–Hochberg still controls the false discovery rate. "
            "<bookmark mark='d'/> So conformal selection controls it in finite samples, with any prediction model and any "
            "number of test units."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def example(self):
        d = load("conformal")
        rows = fit_rows(VGroup(
            label(rf"the Wisconsin breast cancer data: \ {d['n']} biopsies, \ {100 * d['malignant_share']:.0f}\% malignant", font_size=28, color=GREY_A),
            label(r"50 random splits: \ 250 to train a ridge-logistic score, \ 150 to calibrate, \ the rest to test", font_size=26, color=GREY_A),
            label(rf"select the test tumours to call malignant, \ $q = 0.1$: \ on average {d['nsel']:.0f} of {d['n_test']}", font_size=26, color=SELC),
            label(rf"false discovery rate {100 * d['fdr']:.1f}\%: \ at most 10\%, \ as promised", font_size=28, color=HYBC),
            label(rf"power: \ {100 * d['power']:.1f}\% of the malignant tumours selected", font_size=28, color=CONDC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> On real data: the Wisconsin breast cancer biopsies, {100 * d['malignant_share']:.0f} "
            f"percent of them malignant. <bookmark mark='b'/> Over fifty random splits, two hundred and fifty biopsies train a "
            f"ridge-penalized logistic score, a hundred and fifty calibrate it, and the rest are the test units. <bookmark "
            f"mark='c'/> Conformal selection at q equal to a tenth calls on average {say(d['nsel'], 0)} of the "
            f"{d['n_test']} test tumours malignant. <bookmark mark='d'/> The false discovery rate is "
            f"{100 * d['fdr']:.1f} percent, within the promise. <bookmark mark='e'/> And {100 * d['power']:.1f} percent of "
            f"the malignant tumours are selected."
        ) as vo:
            self.play(FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995)")))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def shift(self):
        rows = [
            cmath(r"\text{prediction}", r":", r"\text{an interval for one } Y_{n+1}: \ \text{marginal coverage}", font_size=34),
            cmath(r"\text{selection}", r":", r"\text{a set of units: \ an error rate over the set}", font_size=34),
            cmath(r"\text{covariate shift}", r":", r"\text{weight by } w(x) = dP_{\text{test}}/dP_{\text{cal}}", font_size=32),
            cmath(r"\text{and}", r":", r"\text{FDR control survives, \ with the weights estimated well}", font_size=34),
        ]
        rows[2][-1].set_color(SPLITC)
        whys = [why(r"Part 34"), why(r"many decisions at once"), why(r"Jin \& Cand\`es (2023b)"), why(r"Part 57's subject")]
        with self.voiceover(
            "<bookmark mark='a'/> How does this differ from Part thirty-four's conformal prediction? Prediction gives "
            "an interval for one new outcome, with marginal coverage. <bookmark mark='b'/> Selection makes many "
            "decisions at once and controls an error rate over the selected set. <bookmark mark='c'/> When the test "
            "units differ from the calibration units in their features, a covariate shift, Jin and Candès weight the "
            "conformal p-values by the likelihood ratio of the two feature distributions. <bookmark mark='d'/> False "
            "discovery control survives, provided the weights are estimated well; how well is part of Part "
            "fifty-seven's subject."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"what it shows:", font_size=28, color=GREY_A),
            label(r"selection with a guarantee needs no model of $Y$ given $X$, \ only exchangeability", font_size=26, color=HYBC),
            label(r"the predictor's quality decides the power, \ never the validity", font_size=26, color=CONDC),
            label(r"the same pattern as knockoffs: \ a reference set that mimics the nulls", font_size=26, color=SPLITC),
            label(r"next: \ the oldest selection of all, \ picking the winner", font_size=26, color=SELC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What it shows. <bookmark mark='b'/> Selection with a guarantee needs no model of the outcome "
            "given the features, only exchangeability. <bookmark mark='c'/> The predictor's quality decides the power, "
            "never the validity. <bookmark mark='d'/> And the pattern is the same as for knockoffs: a reference set that "
            "behaves like the nulls, against which the candidates are ranked. <bookmark mark='e'/> Next, the oldest "
            "selection of all: picking the winner."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
