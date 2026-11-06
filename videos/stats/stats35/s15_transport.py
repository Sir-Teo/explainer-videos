from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Transport(VoiceoverScene):
    def construct(self):
        self.card()
        self.who()
        self.ages()
        self.ladder_()
        self.result()
        self.positivity()
        self.lesson()

    def card(self):
        card = chapter_card(14, r"External validity", r"Transporting a trial", lit=(2011, 2019), part=PART)
        with self.voiceover("Chapter fourteen. External validity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def who(self):
        rows = fit_rows(VGroup(
            label(r"randomization gives internal validity: \ the right answer for these patients", font_size=26, color=BANDC),
            label(r"trial patients are volunteers, \ younger, \ healthier, \ near big hospitals", font_size=26, color=MISSC),
            label(r"if the effect varies, \ the answer for them is not the answer for everyone", font_size=26, color=TAUC),
            label(r"external validity: \ carrying the result to a target population", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Randomization gives internal validity: the right answer for the patients in the trial. "
            "<bookmark mark='b'/> But trial patients are volunteers, usually younger and healthier than the patients who "
            "will eventually take the drug, and they live near hospitals that run trials. <bookmark mark='c'/> If the effect "
            "varies between kinds of patient, the answer for them is not the answer for everyone. <bookmark mark='d'/> "
            "External validity is the problem of carrying a trial's result to a target population."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ages(self):
        d = load("transport")
        ag = np.asarray(d["ages"], float)
        mids = (ag[:-1] + ag[1:]) / 2
        A = axes([40, 100], [0, 0.32], x_length=7.4, y_length=4.2, xlabel=r"age", ylabel=r"share", xticks=[40, 60, 80, 100],
                 yticks=[0, 0.1, 0.2, 0.3], center=[-2.0, 0.2, 0])
        ax = A.ax
        bt = bars_at(ax, mids - 1.2, d["h_trial"], 2.2, ESTC)
        bp = bars_at(ax, mids + 1.2, d["h_pool"], 2.2, Y1C)
        side = fit_rows(VGroup(
            label(r"blue: \ the trial's 2,000 patients", font_size=22, color=ESTC),
            label(r"red: \ the 87,406 eligible islanders", font_size=22, color=Y1C),
            label(rf"average effect: \ trial {d['ate_trial']:.2f}, \ island {d['ate_pool']:.2f}", font_size=22, color=TAUC),
            label(r"the drug works better in the old", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the World, younger patients were likelier to enrol. <bookmark mark='b'/> The eligible "
            "islanders are much older: most are over sixty-five. <bookmark mark='c'/> Since the drug works better in older and "
            "sicker patients, the average effect among the eligible islanders is minus " + say(-d["ate_pool"], 1) + ", against "
            "minus " + say(-d["ate_trial"], 1) + " in the trial. A perfectly run trial answers the wrong population's question."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bt), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def ladder_(self):
        rows = [
            cmath(r"S_i = 1", r":", r"\text{in the trial; \ } S_i = 0: \text{ in the target}", font_size=30),
            cmath(r"\text{assume}", r":", r"\tau \perp\!\!\!\perp S \mid X \ \text{and overlap}", font_size=32),
            cmath(r"w_i", r"=", r"\dfrac{P(S = 0 \mid x_i)}{P(S = 1 \mid x_i)}", font_size=32),
            cmath(r"\hat\tau_{\rm target}", r"=", r"\text{the } w\text{-weighted difference in means}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"stack trial and target"), why(r"effect modifiers all measured"),
                why(r"inverse odds of participation"), why(r"Stuart et al. (2011); \ Dahabreh et al. (2019)")]
        with self.voiceover(
            "<bookmark mark='a'/> The method stacks the trial patients and a sample of the target population, and models "
            "the probability of being in the trial given covariates. <bookmark mark='b'/> It assumes that, given those "
            "covariates, trial membership tells us nothing more about the effect: all the effect modifiers are measured. And "
            "it needs overlap: every kind of target patient must appear in the trial. <bookmark mark='c'/> Each trial patient "
            "is weighted by the inverse odds of participation, so that the weighted trial looks like the target. <bookmark "
            "mark='d'/> The weighted difference in means estimates the target's average effect. Elizabeth Stuart and "
            "colleagues proposed propensity scores for this in 2011, and Issa Dahabreh and colleagues worked out its theory "
            "in 2019."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def result(self):
        d = load("transport")
        rows = fit_rows(VGroup(
            label(rf"the trial, \ analysed as usual: \ ${d['trial']['est']:.2f}$ \ [{d['trial']['lo']:.1f}, \ {d['trial']['hi']:.1f}]", font_size=26, color=ESTC),
            label(r"weights from age, \ baseline pressure, \ sex and BMI, \ against 20,000 islanders", font_size=26),
            label(rf"transported: \ ${d['transported']:.2f}$ \ (truth for the island: \ ${d['ate_pool']:.2f}$)", font_size=26, color=BANDC),
            label(rf"the price: \ an effective sample of {d['ess']:,.0f} instead of 2,000", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The trial, analysed as usual, estimates minus " + say(-d["trial"]["est"], 1) + ", close to "
            "its own patients' average effect. <bookmark mark='b'/> Now weight it to twenty thousand of the eligible islanders, "
            "using age, baseline pressure, sex and body-mass index. <bookmark mark='c'/> The transported estimate is minus "
            + say(-d["transported"], 1) + ", most of the way to the island's true minus " + say(-d["ate_pool"], 1) + "; the gap "
            "is within its uncertainty. <bookmark mark='d'/> The price is precision: the weights are uneven, and the trial's "
            "two thousand patients count as about a thousand."
        ) as vo:
            self.add(trial_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def positivity(self):
        rows = fit_rows(VGroup(
            label(r"over-80s are a fifth of the island and almost absent from the trial", font_size=26),
            label(r"their weights are huge, \ and if there were none, \ nothing could be transported", font_size=26, color=MISSC),
            label(r"an unmeasured effect modifier breaks the method silently", font_size=26, color=MISSC),
            label(r"design answer: \ enrol the population you will treat \ (pragmatic trials)", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The weakness is overlap. Islanders over eighty are a large share of the target, and almost "
            "absent from the trial. <bookmark mark='b'/> The few who did enrol carry enormous weights, and if none had, no "
            "weighting could recover their effect. <bookmark mark='c'/> And if an effect modifier was not measured, the "
            "method fails without any warning. <bookmark mark='d'/> The design answer is a pragmatic trial, which enrols the "
            "kinds of patients who will actually be treated, in the places they will be treated."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"internal validity comes from the coin", font_size=28, color=BANDC),
            label(r"external validity needs assumptions, \ as observational studies always do", font_size=28, color=TAUC),
            label(r"which is where Part 36 begins", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So internal validity comes from the coin. <bookmark mark='b'/> External validity needs "
            "assumptions about what was measured, exactly as observational studies always do. <bookmark mark='c'/> Which is "
            "where Part 36 begins."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
