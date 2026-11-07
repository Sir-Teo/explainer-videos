from __future__ import annotations

from videos.stats.stats35.common import *  # noqa: F403


class Estimands(VoiceoverScene):
    def construct(self):
        self.card()
        self.ladder_()
        self.numbers()
        self.sutva()
        self.versions()
        self.risk()

    def card(self):
        card = chapter_card(2, r"Estimands and SUTVA", r"What exactly are we estimating?", lit=(1974,), part=PART)
        with self.voiceover("Chapter two. Estimands, and the stable unit treatment value assumption."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ladder_(self):
        rows = [
            cmath(r"\text{SATE}", r"=", r"\tfrac1n \textstyle\sum_{i=1}^n \tau_i", font_size=32),
            cmath(r"\text{ATT}", r"=", r"\tfrac{1}{n_1} \textstyle\sum_{i: Z_i = 1} \tau_i", font_size=32),
            cmath(r"\text{CATE}(x)", r"=", r"E[\tau_i \mid X_i = x]", font_size=32),
            cmath(r"\text{PATE}", r"=", r"E[\tau] \ \text{over a specified target population}", font_size=30),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"the sample average effect"), why(r"the effect on the treated"),
                why(r"conditional on covariates"), why(r"direct generalization or justified transport")]
        with self.voiceover(
            "<bookmark mark='a'/> Because individual effects are out of reach, we choose an average to estimate: an "
            "estimand. The sample average treatment effect averages tau over the units in the study. <bookmark "
            "mark='b'/> The average effect on the treated averages it over those who actually received the treatment,"
            " which matters when the treated are chosen rather than random. <bookmark mark='c'/> The conditional "
            "average effect averages within a kind of unit, say patients of a given age: the basis of personalized "
            "medicine, and of Part 62. <bookmark mark='d'/> And the population average treatment effect refers to "
            "some larger population. Direct generalization needs representative effects; otherwise transport requires"
            " additional measured covariates and assumptions, as chapter fourteen explains."
        ) as vo:
            intro=label('An estimand names the units and averaging distribution',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def numbers(self):
        d = load("science")
        rows = fit_rows(VGroup(
            label(rf"the trial's 2,000 patients: \ SATE $= {d['ate']:.2f}$ mm Hg", font_size=26, color=TAUC),
            label(rf"all {d['n_pool']:,} eligible islanders: \ PATE $= {d['ate_pool']:.2f}$", font_size=26, color=Y1C),
            label(rf"why different? \ the trial's patients average {d['age_trial']:.0f} years, \ the island's {d['age_pool']:.0f}", font_size=26),
            label(r"the drug works better in the old: \ two honest estimands, \ two numbers", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the World these are just numbers. The sample average effect in the trial is minus "
            + say(-d["ate"], 2) + " millimetres. <bookmark mark='b'/> Among all " + f"{d['n_pool']:,}" + " islanders who "
            "would have been eligible, it is minus " + say(-d["ate_pool"], 2) + ". <bookmark mark='c'/> They differ because "
            "younger people were likelier to enrol: the trial's patients average " + f"{d['age_trial']:.0f}" + " years, the "
            "eligible islanders " + f"{d['age_pool']:.0f}" + ". <bookmark mark='d'/> Since the drug works better in older and "
            "sicker patients, these are two different, equally honest estimands, and a study should say which it is after."
        ) as vo:
            self.add(trial_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sutva(self):
        rows = [
            cmath(r"Y_i(z_1, \ldots, z_n)", r"=", r"Y_i(z_i)", font_size=34),
            cmath(r"\text{1. no interference}", r":", r"\text{my outcome ignores your treatment}", font_size=30),
            cmath(r"\text{2. no hidden versions}", r":", r"\text{one treatment, \ one } Y_i(1)", font_size=30),
            cmath(r"\text{without it}", r":", r"2^n \text{ potential outcomes per unit}", font_size=32),
        ]
        rows[0][-1].set_color(TAUC)
        whys = [why(r"Rubin (1980): \ SUTVA"), why(r"vaccines, \ classrooms, \ markets: \ chapter 10"),
                why(r"the dose, \ the surgeon, \ the brand"), why(r"requires a structured interference model")]
        with self.voiceover(
            "<bookmark mark='a'/> Writing Y i of one and Y i of zero hides an assumption. In general a unit's outcome"
            " could depend on everyone's treatment. Rubin's stable unit treatment value assumption, SUTVA, says it "
            "depends only on its own. <bookmark mark='b'/> That has two parts. No interference: my outcome does not "
            "depend on whether you were treated. Vaccines, which protect the neighbours of the vaccinated, break it, "
            "and chapter ten deals with them. <bookmark mark='c'/> And no hidden versions of the treatment: there is "
            "one Y i of one, not one for each dose, surgeon or brand. <bookmark mark='d'/> Without SUTVA, each unit "
            "has two to the n potential outcomes, one for every assignment of the whole study, so learning requires a"
            " design and restrictions on which assignments affect which outcomes. Chapter ten gives an example."
        ) as vo:
            intro=label('Interference and treatment versions determine the potential outcomes',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def versions(self):
        rows = fit_rows(VGroup(
            label(r"`the effect of obesity on mortality': \ by diet? \ by surgery? \ by exercise? \ by disease?", font_size=26),
            label(r"each intervention has its own potential outcomes, \ and its own effect", font_size=26, color=TAUC),
            label(r"Hern\'an \& Taubman (2008): \ ill-defined interventions give ill-defined effects", font_size=26, color=GREY_A),
            label(r"the remedy: \ name the trial you would run, \ even if you cannot", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hidden versions matter most when the treatment is not something we do. What is the "
            "effect of obesity on mortality? Losing weight by diet, by surgery, by exercise and by illness are different "
            "interventions, <bookmark mark='b'/> each with its own potential outcomes and its own effect. <bookmark "
            "mark='c'/> Miguel Hernán and Sarah Taubman argued in 2008 that such questions have no single answer until the "
            "intervention is specified. <bookmark mark='d'/> The remedy, which Part 36 will turn into a method, is to name "
            "the trial you would run if you could: the target trial."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def risk(self):
        rows = [
            cmath(r"\text{risk difference}", r":", r"P(Y(1) = 1) - P(Y(0) = 1)", font_size=30),
            cmath(r"\text{risk ratio}", r":", r"P(Y(1) = 1) / P(Y(0) = 1)", font_size=30),
            cmath(r"\text{odds ratio}", r":", r"\text{not collapsible: \ subgroup ORs need not average to it}", font_size=28),
            cmath(r"\text{Salk}", r":", r"28 - 71 = -43 \text{ per } 10^5; \ 28/71 = 0.39", font_size=30),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"negative when cases are prevented"), why(r"proportion remaining"), why(r"Greenland, \ Robins \& Pearl (1999)"),
                why(r"vaccine efficacy $1 - 0.39 = 61\%$")]
        with self.voiceover(
            "<bookmark mark='a'/> For a yes-or-no outcome there are several estimands. With our treated-minus-control"
            " convention, the risk difference is negative for cases prevented. <bookmark mark='b'/> The risk ratio is"
            " the proportion of risk that remains. <bookmark mark='c'/> The odds ratio, the natural parameter of "
            "logistic regression, has a strange property: it is not collapsible, so the odds ratio in a whole "
            "population need not be any average of the odds ratios in its subgroups, even without confounding. "
            "<bookmark mark='d'/> For the Salk trial, the treated-minus-control risk difference was minus forty-three"
            " per hundred thousand, and the risk ratio point three nine: the vaccine prevented about sixty percent of"
            " paralytic cases."
        ) as vo:
            intro=label('Risk differences and risk ratios use explicit sign conventions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
