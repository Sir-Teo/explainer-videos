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
            cmath(r"\text{tools}", r":", r"\text{any predictor } \hat\mu, \ \text{a labelled calibration set, \ independent IID pairs}", font_size=32),
            cmath(r"\text{examples}", r":", r"\text{hiring, \ drug screening, \ biopsies}", font_size=30),
        ]
        rows[1][-1].set_color(HYBC)
        whys = [why(r"Jin \& Cand\`es (2023)"), why(r"an FDR over units"), why(r"Part 34's conformal assumptions"), why(r"a screening decision")]
        head = label('Problem', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> A different kind of selection. Ying Jin and Emmanuel Candès considered test units whose features are seen but whose outcomes are not yet known. <bookmark mark='b'/> The goal is to select the units whose outcome exceeds a threshold c, while controlling the false discovery rate: the expected fraction of selected units that do not. <bookmark mark='c'/> The tools are any prediction model and a labelled calibration set, with independent, identically distributed calibration and test pairs, and a predictor trained separately. More general conditional exchangeability conditions are possible, but bare exchangeability is not our theorem here. <bookmark mark='d'/> Which candidates to interview, which compounds to send to the laboratory, which tumours to biopsy."
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
            cmath(r"\text{joint guarantee}", r":", r"P(p_j \le t,\ Y_j \le c) \le t \quad \text{(not conditional on the null)}", font_size=34),
            cmath(r"\hat S", r"=", r"\text{Benjamini--Hochberg at level } q \text{ on } p_1, \dots, p_m", font_size=34),
        ]
        rows[1][-1].set_color(CONDC)
        rows[3][-1].set_color(HYBC)
        whys = [why(r"any model, \ trained elsewhere"), why(r"rank among the calibration nulls"), why(r"exchangeability"), why(r"Part 33's procedure")]
        head = label('Pvalues', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Score each unit with the predictor: a larger score means more promising. <bookmark mark='b'/> For each test unit, the conformal p-value is one plus the number of calibration units that are below the threshold yet scored at least as high, over n plus one. <bookmark mark='c'/> The guarantee is joint: the probability that the p-value is at most t and the test outcome is below the threshold is at most t. It is not a guarantee conditional on the outcome being below the threshold. <bookmark mark='d'/> Then run Benjamini–Hochberg on the test p-values."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\text{the catch}", r":", r"\text{the } p_j \text{ share one calibration set: \ dependent}", font_size=34),
            cmath(r"\text{but}", r":", r"\text{oracle ranks + a modified-vector PRDS lemma}", font_size=34),
            cmath(r"\text{Jin--Cand\`es, \ Theorem 3}", r":", r"\text{leave-one-out argument for a random null set}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{FDR} \le q: \ \text{IID pairs, \ separately trained score}", font_size=34),
        ]
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"a common reference"), why(r"Bates et al. (2023); \ Jin \& Cand\`es"), why(r"Part 33"), why(r"distribution-free")]
        head = label('Why the selection law is tractable', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The catch is that all the p-values are computed against the same calibration set, so they are dependent. <bookmark mark='b'/> Jin and Candès introduce oracle rank p-values, uniform under the independent sampling assumptions. On a null outcome, the reported p-value is at least its oracle value. A modified vector has the positive dependence property needed for a leave-one-out argument. <bookmark mark='c'/> Their leave-one-out proof handles the random null set and the shared calibration sample. Marginal joint validity alone would not justify ordinary Benjamini–Hochberg. <bookmark mark='d'/> Under these sampling and monotone-score conditions, their theorem gives finite-sample false discovery rate control, with any separately trained predictor."
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
            label(rf"mean split FDP {100 * d['fdr']:.1f}\% \ (MCSE {100 * d['fdp_mcse']:.1f} points)", font_size=28, color=HYBC),
            label(rf"power: \ {100 * d['power']:.1f}\% of the malignant tumours selected", font_size=28, color=CONDC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> On real data: the Wisconsin breast cancer biopsies, {100 * d['malignant_share']:.0f} percent of them malignant. <bookmark mark='b'/> Over fifty random splits, two hundred and fifty biopsies train a ridge-penalized logistic score, a hundred and fifty calibrate it, and the rest are the test units. <bookmark mark='c'/> Conformal selection at q equal to a tenth calls on average {say(d['nsel'], 0)} of the {d['n_test']} test tumours malignant. <bookmark mark='d'/> The average false discovery proportion over these splits is {100 * d['fdr']:.1f} percent. These are repeated random splits of one fixed dataset, not independent replications of a population experiment. <bookmark mark='e'/> And {100 * d['power']:.1f} percent of the malignant tumours are selected."
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
            cmath(r"\text{and}", r":", r"\text{use the weighted selection theorem; \ ordinary weighted BH can fail}", font_size=34),
        ]
        rows[2][-1].set_color(SPLITC)
        whys = [why(r"Part 34"), why(r"many decisions at once"), why(r"Jin \& Cand\`es (2023b)"), why(r"Part 57's subject")]
        head = label('Shift', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> How does this differ from Part thirty-four's conformal prediction? Prediction gives an interval for one new outcome, with marginal coverage. <bookmark mark='b'/> Selection makes many decisions at once and controls an error rate over the selected set. <bookmark mark='c'/> When the test units differ from the calibration units in their features, a covariate shift, weighted conformal selection uses the feature density ratio together with a selection and pruning procedure. <bookmark mark='d'/> Ordinary weighted p-values followed by Benjamini–Hochberg can fail even with known weights. The weighted selection theorem needs its specified procedure and assumptions; estimating the weights requires additional error control."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"Selection guarantees require the stated sampling assumptions", font_size=36, color=WHITE),
            label(r"selection can avoid a model of $Y$ given $X$; \ sampling conditions still matter", font_size=26, color=HYBC),
            label(r"power depends on the score; \ validity needs the sampling assumptions", font_size=26, color=CONDC),
            label(r"the same pattern as knockoffs: \ a reference set that mimics the nulls", font_size=26, color=SPLITC),
            label(r"next: \ the oldest selection of all, \ picking the winner", font_size=26, color=SELC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What it shows. <bookmark mark='b'/> Selection with a guarantee needs no model of the outcome given the features, but it does need the independent sampling assumptions used here, or the paper's stronger conditional exchangeability conditions. <bookmark mark='c'/> The predictor's quality decides the power, while validity also requires those sampling conditions and separate training. <bookmark mark='d'/> And the pattern is the same as for knockoffs: a reference set that behaves like the nulls, against which the candidates are ranked. <bookmark mark='e'/> Next, the oldest selection of all: picking the winner."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
