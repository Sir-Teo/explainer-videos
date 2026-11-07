from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403


class CaseControl(VoiceoverScene):
    def construct(self):
        self.card()
        self.doll_hill()
        self.symmetry()
        self.sampling()
        self.world()
        self.ages()
        self.rare()

    def card(self):
        card = chapter_card(10, r"Case--control studies", r"Sampling on the outcome, \ and what survives it", lit=(1950,), part=PART)
        with self.voiceover("Chapter ten. Case–control studies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def doll_hill(self):
        dh = museum.DOLL_HILL
        t = load("tables")["doll_hill"]
        hc = history_card(1950, r"Richard Doll \ and \ Austin Bradford Hill, \ \emph{British Medical Journal}",
                          r"``Smoking and carcinoma of the lung'': \ patients with lung cancer in twenty London hospitals, \ each "
                          r"matched to a patient of the same sex and age group without it, \ all asked about their smoking",
                          color=S.MUSEUM, width=10.6, font_size=22).move_to([0, 2.0, 0])
        tab = table_rows([[r"men", r"smokers", r"non-smokers", r"total"],
                          [r"lung cancer (cases)", rf"{dh['cases_smokers']}", rf"{dh['cases'] - dh['cases_smokers']}", rf"{dh['cases']}"],
                          [r"other patients (controls)", rf"{dh['controls_smokers']}", rf"{dh['controls'] - dh['controls_smokers']}", rf"{dh['controls']}"]],
                         font_size=26, col_buff=0.8, row_buff=0.3, colors=[GREY_B, EVENT, NOEVENT]).move_to([0, -0.4, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"\widehat{{\text{{OR}}}} = \frac{{647 \times 27}}{{2 \times 622}} = {t['or']:.1f}\quad\text{{(crude aggregate OR; matching ignored)}}", font_size=28, color=OBS),
        ), 12.4, 0.2, [0, -2.4, 0])
        tag = historical_tag(r"Doll \& Hill (1950)", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> In 1950 Richard Doll and Austin Bradford Hill published a study of patients with lung cancer "
            "in twenty London hospitals. Each patient was matched with another patient, of the same sex and age group, who did "
            "not have lung cancer, and everyone was asked about their smoking. <bookmark mark='b'/> Among six hundred and "
            "forty-nine men with lung cancer, only two had never smoked. Among the six hundred and forty-nine controls, "
            "twenty-seven had never smoked. <bookmark mark='c'/> The crude aggregated odds ratio is fourteen. Inference for the matched design requires the paired or matched-stratum data, so this marginal table alone does not justify an unmatched confidence interval or Fisher test. "
            "But notice what the design fixed: the number of people with cancer. So what can such a study estimate?"
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(tab, lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows))
        self.clear_scene()

    def symmetry(self):
        rows = [
            cmath(r"P(\text{cancer} \mid \text{smoker})", r"\ ", r"\text{not estimable: \ the study chose how many had cancer}", font_size=28),
            cmath(r"\frac{\text{odds(smoke} \mid \text{case)}}{\text{odds(smoke} \mid \text{control)}}", r"=", r"\frac{a/b}{c/d} = \frac{ad}{bc}", font_size=30),
            cmath(r"\frac{\text{odds(case} \mid \text{smoker)}}{\text{odds(case} \mid \text{non-smoker)}}", r"=", r"\frac{a/c}{b/d} = \frac{ad}{bc}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the OR is the same either way round}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"risk needs sampling fractions or external prevalence"), why(r"what the study measures directly"),
                why(r"what we want to know"), why(r"Cornfield (1951)")]
        with self.voiceover(
            "<bookmark mark='a'/> The study can't estimate the risk of lung cancer for a smoker: it decided for itself that half "
            "its subjects would have cancer. <bookmark mark='b'/> What it measures directly is the odds of having smoked, among "
            "cases and among controls, and their ratio, a d over b c. <bookmark mark='c'/> The ratio we actually want compares "
            "the odds of being a case among smokers and among non-smokers. Write it out in the table's letters, and it's the "
            "same a d over b c. <bookmark mark='d'/> The odds ratio is symmetric: it doesn't care which margin was fixed by the "
            "design. Jerome Cornfield pointed this out in 1951, and it's why case–control studies report odds ratios."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.7, x=-0.6, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sampling(self):
        rows = [
            cmath(r"\text{population}", r":", r"\text{logit}\,P(y = 1 \mid x) = \beta_0 + \beta_1 x", font_size=30),
            cmath(r"\text{sample cases at rate } \pi_1", r",", r"\text{ controls at rate } \pi_0", font_size=30),
            cmath(r"\text{logit}\,P(y = 1 \mid x, \text{sampled})", r"=", r"\beta_0 + \log\frac{\pi_1}{\pi_0} + \beta_1 x", font_size=30),
            cmath(r"\text{so}", r":", r"\text{outcome-only sampling: logistic slopes survive asymptotically}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the truth, \ which a cohort would see"), why(r"sampling that depends only on the outcome"),
                why(r"Bayes's rule: \ the slope is untouched"), why(r"Prentice \& Pyke (1979)")]
        intro = label('Outcome-based sampling shifts the logistic intercept', font_size=36)
        with self.voiceover(
            "The same is true with regression. <bookmark mark='a'/> Suppose that in the population, the log-odds of disease are "
            "linear in a risk factor x. <bookmark mark='b'/> Sample the cases at one rate and the controls at another, the rates "
            "depending only on the outcome. <bookmark mark='c'/> By Bayes's rule, among the sampled people the log-odds are "
            "still linear in x, with the same slope; only the intercept shifts, by the log of the ratio of sampling rates. "
            "<bookmark mark='d'/> So an ordinary logistic regression on case–control data consistently estimates the population logistic slopes with asymptotically valid model-based standard errors under the stated regularity and sampling assumptions, as Ross Prentice and Ronald Pyke proved in 1979. Without sampling fractions or external prevalence, the baseline risk is not identifiable; matched or exposure-dependent sampling needs a design-appropriate analysis."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def world(self):
        d = load("casecontrol")
        tab = table_rows([
            [r"", r"people", r"cases", r"slope per decade", r"intercept"],
            [r"the whole World", rf"{741311:,}", rf"{d['n_cases']:,}", rf"{d['pop_coef'][1]:.3f}", rf"{d['pop_coef'][0]:.2f}"],
            [r"a cohort", r"40,000", rf"{d['cohort_cases']}", rf"{d['cohort_coef'][1]:.3f} \ ({d['cohort_se'][1]:.3f})", rf"{d['cohort_coef'][0]:.2f}"],
            [r"case--control", r"800", r"400", rf"{d['cc_coef'][1]:.3f} \ ({d['cc_se'][1]:.3f})", rf"{d['cc_coef'][0]:.2f}"],
        ], font_size=26, col_buff=0.7, row_buff=0.32, colors=[GREY_B, EXACT, S.ALT, OBS]).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"the slopes agree, \ within their standard errors", font_size=24, color=OBS),
            MathTex(rf"\text{{intercept shift: \ predicted}}\ \log\frac{{\pi_1}}{{\pi_0}} = {d['shift']:.2f},\quad"
                    rf"\text{{observed}}\ {d['cc_coef'][0] - d['pop_coef'][0]:.2f}", font_size=28),
            label(r"800 people, \ half of them cases, \ nearly match 40,000 people with 373 cases", font_size=24, color=S.ALT),
        ), 12.4, 0.3, [0, -1.9, 0])
        tag = simulated_tag(r"the World's screening condition", corner=DR)
        intro = label('Compare cohort and case-control sampling in the World', font_size=36)
        with self.voiceover(
            "Check it on the World, where we know the truth. <bookmark mark='a'/> Among all seven hundred and forty thousand "
            "adults, the log-odds of the silent condition rise by point four five per decade of age. A cohort of forty "
            "thousand random adults contains three hundred and seventy-three cases, and estimates point four nine. A "
            "case–control study takes four hundred cases and four hundred controls, and estimates point four one. "
            "<bookmark mark='b'/> Both slopes are within about one and a half standard errors of the truth. <bookmark mark='c'/> "
            "The case–control intercept is off by four point six eight, and the theory predicted four point six three: the "
            "log of the sampling-rate ratio. <bookmark mark='d'/> And look at the precision: eight hundred people, chosen on "
            "the outcome, give a standard error only forty percent larger than forty thousand people chosen at random. For a "
            "rare disease, that's why case–control studies exist."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tab, lag_ratio=0.08))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def ages(self):
        d = load("casecontrol")
        ac, at = np.asarray(d["cc_age_cases"]), np.asarray(d["cc_age_ctrl"])
        A = axes([18, 100], [0, 70], x_length=8.4, y_length=4.0, xlabel=r"age", ylabel=r"people", xticks=[20, 40, 60, 80, 100],
                 yticks=[0, 30, 60], center=[-1.4, 0.4, 0])
        ax = A.ax
        e = np.arange(18, 101, 4)
        b1 = hist_bars(ax, e, np.histogram(at, e)[0], color=NOEVENT, opacity=0.45)
        b2 = hist_bars(ax, e, np.histogram(ac, e)[0], color=EVENT, opacity=0.65)
        key = VGroup(label(r"400 controls", font_size=22, color=NOEVENT), label(r"400 cases", font_size=22, color=EVENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key.move_to([5.2, 1.4, 0])
        rows = fit_rows(VGroup(
            label(r"the cases are older: \ that difference is the slope", font_size=24, color=EVENT),
            label(r"the 50:50 split is the design's: \ it says nothing about prevalence (1\%)", font_size=24, color=GREY_A),
        ), 12.4, 0.26, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's what the case–control sample looks like: the ages of the four hundred controls and the "
            "four hundred cases. The cases are older, and that shift is what the slope measures. <bookmark mark='b'/> The "
            "fifty-fifty split between cases and controls is the design's choice, and says nothing about how common the "
            "condition is. In the World, it affects about one adult in a hundred."
        ) as vo:
            self.play(FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.03),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.03), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def rare(self):
        rows = fit_rows(VGroup(
            label(r"for a rare disease, \ the odds ratio is close to the relative risk \ (chapter seven)", font_size=26),
            label(r"case--control ORs can approximate risk ratios when risks are small", font_size=26, color=OBS),
            label(r"their weak point is not the arithmetic but the controls: \ do they represent exposure in the source population?", font_size=24, color=RES),
            label(r"and recall: \ cases may remember their past differently", font_size=24, color=RES),
            label(r"Doll \& Hill then followed 40,000 British doctors from 1951: \ the cohort confirmed it", font_size=24, color=GREY_A),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For a rare disease, chapter seven showed that the odds ratio is close to the relative risk. "
            "<bookmark mark='b'/> So a case–control study can estimate how much a factor multiplies the risk of a rare "
            "disease, with a few hundred subjects instead of a cohort of hundreds of thousands followed for decades. "
            "<bookmark mark='c'/> Its weak point isn't the arithmetic. It's the controls: do they represent the exposure distribution in the source population that generated the cases, within the chosen strata? <bookmark mark='d'/> And people with a disease may remember their past differently. "
            "<bookmark mark='e'/> Doll and Hill knew this, and in 1951 began following forty thousand British doctors forward "
            "in time. The cohort confirmed the case–control result, and then some."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
