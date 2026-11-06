from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class TimeVarying(VoiceoverScene):
    def construct(self):
        self.card()
        self.graph()
        self.dilemma()
        self.msm()
        self.numbers()
        self.target()

    def card(self):
        card = chapter_card(14, r"Time-varying treatments", r"When the confounder is also a result", lit=(1986, 2000, 2016), part=PART)
        with self.voiceover("Chapter fourteen. Treatments that vary over time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def graph(self):
        G = CausalGraph({"A0": (-3.0, 0), "L1": (-0.8, 0), "A1": (1.4, 0), "Y": (3.4, 0), "U": (0.3, -2.0)},
                        [("A0", "L1"), ("L1", "A1"), ("L1", "Y"), ("A0", "Y"), ("A1", "Y"), ("U", "L1"), ("U", "Y")],
                        center=[-1.6, 0.6, 0], scale=0.95, colors={"A0": Y1C, "A1": Y1C, "Y": Y0C, "L1": TAUC, "U": MISSC},
                        labels={"A0": r"$A_0$", "L1": r"$L_1$", "A1": r"$A_1$", "Y": r"$Y$", "U": r"$U$"})
        side = fit_rows(VGroup(
            label(r"$A_0$: \ treatment now", font_size=22, color=Y1C),
            label(r"$L_1$: \ a health measure later", font_size=22, color=TAUC),
            label(r"$A_1$: \ treatment decided from $L_1$", font_size=22, color=Y1C),
            label(r"$U$: \ unmeasured, \ affects $L_1$ and $Y$", font_size=22, color=MISSC),
        ), 3.8, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Many treatments are not one decision but a sequence: HIV drugs adjusted to the latest "
            "viral load, insulin to the latest blood sugar. Here is the smallest example. A treatment at time zero. "
            "<bookmark mark='b'/> A health measure at time one, which the first treatment improves. <bookmark mark='c'/> A "
            "second treatment, chosen by doctors according to that health measure. <bookmark mark='d'/> And an unmeasured "
            "patient characteristic that affects both the health measure and the final outcome. We want the effect of "
            "always treating against never treating."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def dilemma(self):
        rows = fit_rows(VGroup(
            label(r"$L_1$ confounds $A_1$: \ it causes $A_1$ and $Y$, \ so we must adjust for it", font_size=26, color=TAUC),
            label(r"$L_1$ mediates $A_0$: \ part of $A_0$'s effect flows through it, \ so we must not", font_size=26, color=MISSC),
            label(r"and $L_1$ is a collider on $A_0 \to L_1 \leftarrow U \to Y$: \ adjusting opens a bias path", font_size=26, color=MISSC),
            label(r"no regression of $Y$ on the treatments and $L_1$ can be right", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the dilemma that Robins identified in 1986. The health measure confounds the second "
            "treatment: it causes both the treatment and the outcome, so we must adjust for it. <bookmark mark='b'/> But it "
            "is also a mediator of the first treatment, part of the way the first dose works, so we must not. <bookmark "
            "mark='c'/> Worse, it is a collider on the path from the first treatment through the health measure, back "
            "through the unmeasured characteristic, to the outcome; adjusting opens that path. <bookmark mark='d'/> No "
            "regression of the outcome on the treatments, with or without the health measure, can give the right answer."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def msm(self):
        rows = [
            cmath(r"E[Y(a_0, a_1)]", r"=", r"\beta_0 + \beta_1 a_0 + \beta_2 a_1", font_size=32),
            cmath(r"sw_i", r"=", r"\dfrac{P(A_1 = a_{1i} \mid a_{0i})}{P(A_1 = a_{1i} \mid a_{0i}, L_{1i})}", font_size=30),
            cmath(r"\text{fit}", r":", r"\text{the weighted regression of } Y \text{ on } A_0, A_1 \text{ only}", font_size=30),
            cmath(r"\text{g-formula}", r":", r"\textstyle\sum_{l} E[Y \mid a_0, l, a_1]\, P(l \mid a_0)", font_size=30),
        ]
        rows[1][-1].set_color(PSC)
        whys = [why(r"a marginal structural model"), why(r"stabilized weights: \ break the $L_1 \to A_1$ arrow"),
                why(r"Robins, \ Hern\'an \& Brumback (2000)"), why(r"Robins (1986): \ the alternative")]
        with self.voiceover(
            "<bookmark mark='a'/> Robins's solutions model the potential outcomes directly. A marginal structural model says "
            "how the average outcome under each treatment sequence depends on the sequence. <bookmark mark='b'/> Weight each "
            "patient by the inverse probability of the second treatment they received, given their health measure, "
            "stabilized by its probability without that information. In the weighted population, the second treatment no "
            "longer depends on the health measure: the arrow is broken. <bookmark mark='c'/> Then regress the outcome on the "
            "two treatments alone, with those weights, without adjusting for the health measure. <bookmark mark='d'/> Or use "
            "the g-formula: model the outcome given the whole history, and average over how the health measure would evolve "
            "under each sequence."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def numbers(self):
        d = load("msm")
        rows = [[r"method", r"always vs never"],
                [r"regress $Y$ on $A_0, A_1$", rf"{d['naive']:.2f}"],
                [r"\ldots and $L_1$", rf"{d['adjusted']:.2f}"],
                [r"IPW, \ marginal structural model", rf"{d['msm']:.2f}"],
                [r"g-formula", rf"{d['gformula']:.2f}"],
                [r"truth", rf"{d['truth']:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.3, colors=[GREY_A, MISSC, MISSC, BANDC, BANDC, TRUEC]).move_to([0, 0.7, 0])
        foot = label(rf"200,000 simulated patients; \ stabilized weights average {d['sw_mean']:.3f}, \ largest {d['sw_max']:.0f}",
                     font_size=22, color=GREY_A).move_to([0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two hundred thousand simulated patients. The truth, always against never treating, is minus "
            "seven. <bookmark mark='b'/> Regressing the outcome on the two treatments gives minus " + say(-d["naive"], 1) + ", "
            "because the second treatment goes to the sicker patients. <bookmark mark='c'/> Adding the health measure makes it "
            "worse, minus " + say(-d["adjusted"], 1) + ", for the reasons just given. <bookmark mark='d'/> The weighted "
            "marginal structural model gives minus " + say(-d["msm"], 2) + ", and the g-formula minus " + say(-d["gformula"], 2)
            + ". The stabilized weights average one, as they should."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[5]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(foot))
        self.clear_scene()

    def target(self):
        rows = fit_rows(VGroup(
            label(r"target-trial emulation \ (Hern\'an \& Robins 2016):", font_size=26, color=TAUC),
            label(r"write the protocol of the trial you would run: \ eligibility, \ strategies, \ start, \ outcome", font_size=26),
            label(r"then emulate it in observational data, \ aligning eligibility and time zero", font_size=26),
            label(r"avoids immortal-time and prevalent-user biases: \ the WHI hormone-therapy reconciliation", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> These tools are now organized by a discipline Miguel Hernán and Robins called target-trial "
            "emulation, in 2016. <bookmark mark='b'/> First write the protocol of the randomized trial you would run if you "
            "could: who is eligible, which treatment strategies are compared, when follow-up starts, what outcome is "
            "counted. <bookmark mark='c'/> Then emulate that trial with observational data, making sure that eligibility, "
            "treatment assignment and the start of follow-up line up, as they would in a trial. <bookmark mark='d'/> Many "
            "famous failures of observational studies came from misaligning them, such as counting time before treatment "
            "started as treated time. Emulating a trial properly reconciled the observational and randomized evidence on "
            "hormone therapy in the Women's Health Initiative."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
