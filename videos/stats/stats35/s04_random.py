from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Randomization(VoiceoverScene):
    def construct(self):
        self.card()
        self.decompose()
        self.doctor()
        self.numbers()
        self.coin()
        self.why_()
        self.board()
        self.balance()

    def card(self):
        card = chapter_card(3, r"Why randomization works", r"Selection bias, measured", lit=(1935,), part=PART)
        with self.voiceover("Chapter three. Why randomization works."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def decompose(self):
        rows = [
            cmath(r"E[Y \mid Z = 1] - E[Y \mid Z = 0]", r"=", r"E[Y(1) \mid Z = 1] - E[Y(0) \mid Z = 0]", font_size=28),
            cmath(r"", r"=", r"\underbrace{E[Y(1) - Y(0) \mid Z = 1]}_{\text{ATT}} + \underbrace{E[Y(0) \mid Z = 1] - E[Y(0) \mid Z = 0]}_{\text{selection bias}}", font_size=26),
            cmath(r"Z \perp\!\!\!\perp (Y(0), Y(1))", r"\Rightarrow", r"\text{selection bias} = 0, \ \text{ATT} = \text{ATE}", font_size=28),
            cmath(r"\text{a coin}", r":", r"Z \text{ ignores everything about the patient}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"what we can compute"), why(r"add and subtract $E[Y(0) \mid Z = 1]$"),
                why(r"independence of assignment and science"), why(r"by construction")]
        with self.voiceover(
            "<bookmark mark='a'/> Here is the whole argument. The difference in average outcomes between treated and "
            "untreated is the average treated outcome among the treated minus the average untreated outcome among the "
            "untreated. <bookmark mark='b'/> Add and subtract what the treated would have had without treatment. The "
            "difference splits into the average effect on the treated, plus a selection bias: how the treated would have "
            "differed from the untreated even without treatment. <bookmark mark='c'/> If the assignment is independent of "
            "the potential outcomes, the selection bias is zero and the effect on the treated equals the average effect. "
            "<bookmark mark='d'/> A coin achieves that independence by construction, because it knows nothing about the "
            "patients. Nothing else is guaranteed to."
        ) as vo:
            intro=label('An observed comparison combines an effect and selection bias',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def doctor(self):
        t = World().trial
        base, doc = t["base"], t["doctor"]
        A = axes([138, 185], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"baseline pressure (mm Hg)",
                 ylabel=r"chance of prescription", xticks=[140, 160, 180], yticks=[0, 0.5, 1], center=[-2.0, 0.2, 0])
        ax = A.ax
        xs = np.linspace(138, 185, 100)
        c = curve(ax, xs, 1 / (1 + np.exp(-(xs - 152) / 6)), MISSC, 3.5)
        coin = DashedLine(ax.c2p(138, 0.5), ax.c2p(185, 0.5), color=BANDC, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"in practice: \ a doctor decides", font_size=22),
            label(r"the higher the pressure, \ the likelier the drug", font_size=22, color=MISSC),
            label(r"in a trial: \ a coin, \ one half for everyone", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Watch it happen on the World's patients. Suppose that instead of a trial, doctors "
            "prescribe the drug as they see fit. <bookmark mark='b'/> A sensible doctor prescribes it to the patients whose "
            "pressure is highest: the chance of a prescription rises steeply with the baseline reading. <bookmark mark='c'/> "
            "In the trial, a coin gives every patient the same one-half chance."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(coin), FadeIn(side[2]))
        self.clear_scene()

    def numbers(self):
        d = load("selection")
        rows = [[r"", r"doctor chooses", r"a coin"]]
        rows.append([r"treated, \ baseline", rf"{d['base_treated']:.1f}", r"$\approx$ the same"])
        rows.append([r"untreated, \ baseline", rf"{d['base_untreated']:.1f}", r"$\approx$ the same"])
        rows.append([r"difference in means", rf"{d['naive']['est']:.2f}", rf"{d['rand']['est']:.2f}"])
        rows.append([r"90\% interval", rf"[{d['naive']['lo']:.1f}, \ {d['naive']['hi']:.1f}]", rf"[{d['rand']['lo']:.1f}, \ {d['rand']['hi']:.1f}]"])
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.3, colors=[GREY_A, None, None, TAUC, TAUC]).move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(rf"truth: \ ATE $= {d['ate']:.2f}$; \ ATT under the doctor $= {d['att']:.2f}$", font_size=24, color=TRUEC),
            label(rf"the doctor's comparison: \ ATT {d['att']:.1f} \ $+$ \ selection bias $+{d['sel_bias']:.1f}$", font_size=24, color=MISSC),
        ), 12.4, 0.35, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The results. When the doctor chooses, the treated patients started at an average of "
            + say(d["base_treated"], 0) + " millimetres, the untreated at " + say(d["base_untreated"], 0) + ". <bookmark "
            "mark='b'/> Comparing their twelve-week pressures, the drug seems to lower pressure by only " + say(-d["naive"]["est"], 1)
            + " points. With the coin it lowers it by " + say(-d["rand"]["est"], 1) + ". <bookmark mark='c'/> The truth, known "
            "in the World, is an average effect of " + say(-d["ate"], 1) + " points, and among the patients the doctor "
            "treated, " + say(-d["att"], 1) + ". <bookmark mark='d'/> So the doctor's comparison is the effect on the treated, "
            "minus nine and a half, plus a selection bias of over seven points: the treated would have had higher pressures "
            "anyway. The bias swamps most of the effect, and its interval is narrow and wrong."
        ) as vo:
            self.add(trial_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def coin(self):
        rows = [
            cmath(r"P(Z_i = 1)", r"=", r"\tfrac12 \ \text{for every } i", font_size=32),
            cmath(r"E\big[\bar Y_1 - \bar Y_0\big]", r"=", r"\tfrac1n \textstyle\sum_i \big(Y_i(1) - Y_i(0)\big) = \text{SATE}", font_size=30),
            cmath(r"\text{over}", r":", r"\text{the } \binom{n}{n_1} \text{ possible assignments}", font_size=30),
            cmath(r"\text{assumes}", r":", r"\text{SUTVA; \ nothing about the science}", font_size=30),
        ]
        rows[1][-1].set_color(BANDC)
        whys = [why(r"complete randomization, $n_1 = n/2$"), why(r"Neyman (1923)"),
                why(r"the expectation is over the design"), why(r"no model for $Y$")]
        with self.voiceover(
            "<bookmark mark='a'/> In the design-based view the argument is even simpler. Under complete randomization, "
            "every patient has the same chance of treatment. <bookmark mark='b'/> Then the expected difference in means is "
            "exactly the sample average treatment effect: each unit's treated outcome appears in the treated mean with "
            "probability one half, and likewise its untreated outcome. <bookmark mark='c'/> The expectation is over the "
            "possible assignments, with the science held fixed. <bookmark mark='d'/> It assumes SUTVA, and nothing at all "
            "about how the outcomes are distributed: no normality, no linearity, no model."
        ) as vo:
            intro=label('Complete randomization is unbiased for the fixed sample average effect',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def why_(self):
        rows = fit_rows(VGroup(
            label(r"the doctor's rule used the baseline: \ we could adjust for it", font_size=26),
            label(r"but real doctors also use what the data do not record: \ how the patient looks, \ their history", font_size=26, color=MISSC),
            label(r"a coin balances the unrecorded too, \ on average", font_size=26, color=BANDC),
            label(r"Part 36: \ when we must rely on recording enough", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here the doctor's rule used only the baseline reading, which we recorded, so we could "
            "adjust for it. <bookmark mark='b'/> Real doctors also use what no data set records: how the patient looks, "
            "what they say, their history. <bookmark mark='c'/> A coin balances those unrecorded differences too, on "
            "average, which no adjustment can promise. <bookmark mark='d'/> Part 36 asks what can be done when there is no "
            "coin, and we must hope we have recorded enough."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("doctor chooses")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, over a thousand repetitions of the doctor's choices: the difference "
                   "in means, as a ninety percent interval for the average effect, never covers it. Broken, completely, by "
                   "selection bias.",
                   [("a", [0])])

    def balance(self):
        rows = fit_rows(VGroup(
            label(r"randomization does not make the groups identical, \ only exchangeable", font_size=26),
            label(r"a bad draw can still be unbalanced: \ chance, \ not bias", font_size=26, color=GREY_A),
            label(r"its size is what Neyman's variance measures, \ and blocking reduces", font_size=26, color=TAUC),
            label(r"and Fisher's test asks whether chance is enough to explain what we saw", font_size=26, color=Y0C),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One caution. Randomization does not make the two groups identical; it makes them "
            "exchangeable, alike in distribution. <bookmark mark='b'/> Any one draw can be unbalanced by chance, but that is "
            "chance, not bias, and it averages out. <bookmark mark='c'/> How large the chance imbalance is, is exactly what "
            "Neyman's variance measures, and what blocking reduces. <bookmark mark='d'/> And whether chance alone could "
            "explain what we saw is Fisher's question, next."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
