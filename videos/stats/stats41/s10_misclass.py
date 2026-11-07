from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class Misclassification(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_study()
        self.matrix()
        self.curve()
        self.tables()
        self.differential()
        self.outcomes()
        self.validation()
        self.lessons()

    def card(self):
        card = chapter_card(9, r"Misclassification", r"When the category itself is wrong", lit=(1904,), part=PART)
        with self.voiceover("Chapter nine. Misclassification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_study(self):
        rows = fit_rows(VGroup(
            label(r"a case-control study: \ 1,000 cases, \ 1,000 controls; \ was each exposed?", font_size=26),
            label(r"exposure recalled from memory: \ sensitivity 0.8, \ specificity 0.9", font_size=26, color=MNC),
            label(r"the true odds ratio: \ 2.5 \ (in this sample, \ 2.29)", font_size=26, color=TRUEC),
            label(r"the same errors for cases and controls: \ nondifferential", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Misclassification is measurement error for categories. A seeded case-control study: a "
            "thousand cases and a thousand controls, each asked whether they were exposed. <bookmark mark='b'/> Memory is "
            "imperfect: eighty percent of the exposed say yes, and ninety percent of the unexposed say no. <bookmark "
            "mark='c'/> The true odds ratio is two point five, and two point two nine in this particular sample. <bookmark "
            "mark='d'/> At first, everyone misremembers in the same way: nondifferential misclassification."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def matrix(self):
        rows = [
            cmath(r"P(\text{say exposed})", r"=", r"\text{Se}\, p + (1 - \text{Sp})(1 - p)", font_size=30),
            cmath(r"\Rightarrow p", r"=", r"\dfrac{P(\text{say exposed}) - (1 - \text{Sp})}{\text{Se} + \text{Sp} - 1}", font_size=30),
            cmath(r"\text{apply}", r":", r"\text{to cases and controls separately, \ then form the odds ratio}", font_size=30),
            cmath(r"\text{needs}", r":", r"\text{Se and Sp, \ from a validation study}", font_size=30),
        ]
        rows[1][-1].set_color(MIC)
        whys = [why(r"what we see"), why(r"invert it"), why(r"the matrix method"), why(r"Barron (1977)")]
        with self.voiceover(
            "<bookmark mark='a'/> The share who say they were exposed mixes the truly exposed who remember with the "
            "unexposed who wrongly say yes. <bookmark mark='b'/> If sensitivity and specificity are known, this inverts: the "
            "true share is the reported share, minus the false positives, divided by the sum of sensitivity and "
            "specificity minus one. <bookmark mark='c'/> Correct cases and controls separately, then form the odds ratio. "
            "<bookmark mark='d'/> The catch is the same as before: the error rates must come from a validation study, here "
            "perhaps medical records for a subsample."
        ) as vo:
            heading = label('Misclassification correction requires informative error rates', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curve(self):
        d = load("misclass")
        ses = np.asarray(d["ses"], float)
        A = axes([0.5, 1.0], [1, 2.6], x_length=7.4, y_length=4.2, xlabel=r"sensitivity of recall", ylabel=r"OR of expected observed proportions",
                 xticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[1, 1.5, 2, 2.5], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = polyline(ax, ses, np.asarray(d["exp_or"], float), MNC, 3)
        c2 = polyline(ax, ses, np.asarray(d["exp_or_sp1"], float), IPWC, 3)
        truth = DashedLine(ax.c2p(0.5, 2.5), ax.c2p(1.0, 2.5), color=TRUEC, stroke_width=2.5)
        one = DashedLine(ax.c2p(0.5, 1), ax.c2p(1.0, 1), color=GREY_D, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"gold: \ the true OR, \ 2.5", font_size=22, color=TRUEC),
            label(r"orange: \ specificity 0.9", font_size=22, color=MNC),
            label(r"purple: \ perfect specificity", font_size=22, color=IPWC),
            label(r"nondifferential error pulls toward 1", font_size=22, color=GREY_A),
            label(r"false positives hurt more \ if exposure is rare", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How much is the odds ratio diluted? The truth is two point five. <bookmark "
            "mark='b'/> With specificity ninety percent, the odds ratio formed from expected observed cell "
            "proportions falls steadily as sensitivity drops, <bookmark mark='c'/> and with perfect specificity it "
            "falls much more slowly. <bookmark mark='d'/> Nondifferential misclassification of a binary exposure "
            "pulls the population odds ratio toward one in this simple unconfounded setting with common error rates "
            "and sensitivity plus specificity greater than one. It is not a statement about every finite-sample "
            "estimate, <bookmark mark='e'/> and when the exposure is uncommon, false positives among the many "
            "unexposed do more damage than missed exposures."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(truth), FadeIn(one), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def tables(self):
        d = load("misclass")
        t, nd = d["true"], d["nd"]
        rows = [[r"", r"cases exposed", r"controls exposed", r"odds ratio"],
                [r"truth \ (this sample)", f"{t[0]}", f"{t[2]}", f"{d['true_or']:.2f}"],
                [r"as recalled \ (Se 0.8, \ Sp 0.9)", f"{nd[0]}", f"{nd[2]}", f"{d['nd_or']:.2f}"],
                [r"corrected by the matrix method", r"", r"", f"{d['corr_or']:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.0, row_buff=0.36, colors=[GREY_A, TRUEC, MNC, MIC]).move_to([0, 0.8, 0])
        foot = label(r"point correction only; propagate sampling and error-rate uncertainty for intervals", font_size=24, color=GREY_A).move_to([0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The study's tables. <bookmark mark='b'/> In truth, " + str(t[0]) + " cases and " + str(t[2])
            + " controls were exposed. <bookmark mark='c'/> As recalled, the counts are blurred, and the odds ratio drops to "
            + say(d["nd_or"], 2) + ". <bookmark mark='d'/> Correcting with the known error rates gives " + say(d["corr_or"], 2)
            + ", back near the truth, as a point correction. We have not computed an interval here; uncertainty must "
            "propagate sampling variation and any estimated error rates. Incompatible error-rate assumptions can even"
            " imply corrected proportions outside zero and one, requiring a constrained model rather than blind "
            "clipping."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def differential(self):
        d = load("misclass")
        rows = fit_rows(VGroup(
            label(r"recall bias: \ cases search their memories harder than controls", font_size=26, color=MNC),
            label(r"sensitivity 0.9 for cases, \ 0.7 for controls; \ specificity 0.9 for both", font_size=26),
            label(rf"observed odds ratio: \ {d['dif_or']:.2f}, \ above the truth of {d['true_or']:.2f}", font_size=26, color=MNC),
            label(r"differential error can push either way, \ and the matrix method must use each group's rates", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real case-control studies have a worse problem, recall bias: people who have a disease "
            "search their memories harder for possible causes. <bookmark mark='b'/> Suppose cases recall an exposure ninety "
            "percent of the time and controls seventy. <bookmark mark='c'/> The observed odds ratio is now "
            + say(d["dif_or"], 2) + ", above the truth: differential error can exaggerate an effect, or invent one. "
            "<bookmark mark='d'/> Correction is still possible, but only with separate error rates for cases and controls."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"``nondifferential error only biases toward the null'': \ population-limit result under informative common binary error rates", font_size=26, color=GREY_A),
            label(r"but not for one study, \ not for three or more categories, \ not with confounders also mismeasured", font_size=26, color=MNC),
            label(r"and a small estimate is not evidence of a large truth", font_size=26, color=MNC),
            label(r"probabilistic bias analysis: \ put priors on Se and Sp, \ and simulate \ (Lash et al.\ 2009)", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A common reassurance says that nondifferential error only biases toward the null. "
            "For a binary exposure in the simple informative, nondifferential error model, it describes the "
            "population odds-ratio limit, rather than the exact expectation of a finite-sample ratio. <bookmark "
            "mark='b'/> But not necessarily in a single study, not for exposures with three or more categories, and "
            "not when confounders are mismeasured too, as Sander Greenland and others have stressed. <bookmark "
            "mark='c'/> And a small estimated effect, explained away as dilution, is not evidence that the true "
            "effect is large. <bookmark mark='d'/> The modern approach, probabilistic bias analysis, puts "
            "distributions on the error rates and simulates the range of corrected answers."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def outcomes(self):
        rows = fit_rows(VGroup(
            label(r"misclassified outcomes: \ a disease defined by billing codes, \ a death certificate's cause", font_size=26, color=TAUC),
            label(r"imperfect specificity biases risk ratios toward 1", font_size=26, color=MNC),
            label(r"perfect specificity and common positive sensitivity preserve population risk ratios", font_size=26, color=MIC),
            label(r"so prefer outcome definitions that are specific, \ even at the cost of missing cases", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Outcomes are misclassified too: a disease defined from billing codes, a cause of "
            "death from a certificate. <bookmark mark='b'/> If some non-cases are counted as cases, with common "
            "informative error rates in both groups, population risk ratios are pulled toward one. <bookmark "
            "mark='c'/> But if the definition is perfectly specific, missing some true cases equally in both groups "
            "preserves the population risk ratio, because the same fraction of cases is lost from each. <bookmark "
            "mark='d'/> So in studies of risk, specificity can be especially valuable for a risk-ratio estimand, "
            "while sensitivity, precision and the study’s purpose still matter."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()


    def validation(self):
        rows = fit_rows(VGroup(
            label(r"a validation substudy: \ the gold standard on a few hundred", font_size=26, color=TAUC),
            label(r"estimates Se and Sp, \ or the calibration of $W$ on $X$", font_size=26, color=None),
            label(r"choose the substudy at random within strata, \ and analyse it with the main study", font_size=26, color=MIC),
            label(r"the same logic as two-phase sampling \ (Part 18) \ and MI for the unvalidated", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> All these corrections rest on a validation substudy: the expensive gold-standard measurement "
            "on a few hundred people. <bookmark mark='b'/> It estimates the sensitivity and specificity, or the calibration "
            "of the error-prone measure on the true one. <bookmark mark='c'/> Choose it at random, perhaps within strata, "
            "and analyse it together with the main study. <bookmark mark='d'/> It is two-phase sampling, from Part "
            "eighteen, and the unvalidated majority can even be multiply imputed: missing data and measurement error are "
            "one subject."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

