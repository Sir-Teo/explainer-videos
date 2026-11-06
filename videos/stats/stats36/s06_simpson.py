from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class Simpson(VoiceoverScene):
    def construct(self):
        self.card()
        self.recall()
        self.graph()
        self.adjust()
        self.other()
        self.lesson()

    def card(self):
        card = chapter_card(5, r"Simpson resolved", r"The paradox is in the causal story, \ not the numbers", lit=(1995,), part=PART)
        with self.voiceover("Chapter five. Simpson's paradox, resolved."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def recall(self):
        d = load("simpson")
        rows = [[r"", r"treated", r"untreated", r"difference"],
                [r"mild", rf"{100 * d['mild']['t']:.1f}\%", rf"{100 * d['mild']['c']:.1f}\%", rf"$+{100 * (d['mild']['t'] - d['mild']['c']):.1f}$"],
                [r"severe", rf"{100 * d['severe']['t']:.1f}\%", rf"{100 * d['severe']['c']:.1f}\%", rf"$+{100 * (d['severe']['t'] - d['severe']['c']):.1f}$"],
                [r"everyone", rf"{100 * d['overall']['t']:.1f}\%", rf"{100 * d['overall']['c']:.1f}\%", rf"${100 * d['naive']:.1f}$"]]
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.35, colors=[GREY_A, BANDC, BANDC, MISSC]).move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"Part 1's clinic: \ recovery rates, \ 20,000 patients", font_size=24, color=GREY_A),
            label(rf"severe patients are treated {100 * d['severe']['treated_share']:.0f}\% of the time, \ mild ones {100 * d['mild']['treated_share']:.0f}\%", font_size=24, color=TAUC),
        ), 12.4, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 1 ended with a puzzle from the World's clinic. <bookmark mark='b'/> Among patients "
            "with mild illness, the treated recover more often, by about eight points; among the severely ill, also by "
            "about eight points; <bookmark mark='c'/> but over everyone, the treated recover less often, by eleven points. "
            "<bookmark mark='d'/> The reason is that doctors treat the severely ill three times as often, and the severely ill "
            "recover less. Part 1 said that statistics alone cannot say which comparison is right. Now we can."
        ) as vo:
            self.add(clinic_tag())
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def graph(self):
        G = CausalGraph({"S": (0, 1.5), "T": (-2.4, -0.6), "R": (2.4, -0.6)}, [("S", "T"), ("S", "R"), ("T", "R")],
                        center=[-2.6, 0.2, 0], colors={"T": Y1C, "R": Y0C, "S": TAUC},
                        labels={"S": r"sev.", "T": r"$T$", "R": r"rec."})
        side = fit_rows(VGroup(
            label(r"severity is measured before treatment", font_size=22),
            label(r"it causes treatment \ (doctors' choices)", font_size=22, color=TAUC),
            label(r"and recovery \ (sicker patients recover less)", font_size=22, color=TAUC),
            label(r"a confounder: \ the back door must be closed", font_size=22, color=BANDC),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Draw the clinic. Severity is determined before treatment. <bookmark mark='b'/> It causes "
            "treatment, through the doctors' choices, <bookmark mark='c'/> and it causes recovery. <bookmark mark='d'/> So it "
            "is a confounder, and the back-door path from treatment through severity to recovery must be closed by "
            "adjusting for it."
        ) as vo:
            self.add(clinic_tag())
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
                if k == 3:
                    self.play(FadeIn(G.path(["T", "S", "R"], MISSC)), Create(G.condition(["S"])))
        self.clear_scene()

    def adjust(self):
        d = load("simpson")
        rows = [
            cmath(r"P(r \mid do(t))", r"=", r"\textstyle\sum_s P(r \mid t, s)\, P(s)", font_size=32),
            cmath(r"P(s)", r":", rf"\text{{mild }} {d['mild']['share']:.3f}, \ \text{{severe }} {d['severe']['share']:.3f}", font_size=30),
            cmath(r"\text{effect}", r"=", rf"+{100 * d['adjusted']:.1f} \text{{ points}}", font_size=34),
            cmath(r"\text{the World's truth}", r":", r"+7 \text{ to } +8 \text{ points in each group}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"the back-door formula"), why(r"the clinic's case mix"), why(r"the treatment helps"), why(r"Part 1's design")]
        with self.voiceover(
            "<bookmark mark='a'/> The back-door formula: average the within-severity recovery rates over the population's "
            "mix of severity. <bookmark mark='b'/> About sixty-five percent mild and thirty-five percent severe. <bookmark "
            "mark='c'/> The causal effect of treatment is a gain of " + say(100 * d["adjusted"], 1) + " points in recovery. "
            "<bookmark mark='d'/> That is what the World built in: the treatment raises everyone's chance of recovery by "
            "seven or eight points. The aggregate comparison mixed the effect of treatment with the effect of being sick."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def other(self):
        G = CausalGraph({"T": (-2.4, -0.6), "P": (0, 1.5), "R": (2.4, -0.6)}, [("T", "P"), ("P", "R"), ("T", "R")],
                        center=[-2.6, 0.2, 0], colors={"T": Y1C, "R": Y0C, "P": TAUC},
                        labels={"T": r"$T$", "P": r"BP", "R": r"rec."})
        side = fit_rows(VGroup(
            label(r"the same numbers, \ a different story:", font_size=22),
            label(r"the third variable is blood pressure \emph{after} treatment", font_size=22, color=TAUC),
            label(r"now it is a mediator", font_size=22, color=TAUC),
            label(r"the aggregate comparison is the right one", font_size=22, color=BANDC),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Pearl's point is that the same table can call for the opposite answer. Suppose the third "
            "variable were not severity at admission but blood pressure measured after treatment, <bookmark mark='b'/> "
            "which the treatment affects. <bookmark mark='c'/> Then it is a mediator, part of the path by which treatment "
            "acts. <bookmark mark='d'/> Adjusting for it would remove part of the effect, and the aggregate comparison is the "
            "right one. The numbers are identical; the causal story decides."
        ) as vo:
            self.add(clinic_tag())
            self.play(FadeIn(G))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"Simpson's paradox is not a paradox of probability", font_size=26),
            label(r"it is a reminder that causal questions need causal assumptions", font_size=26, color=TAUC),
            label(r"with the graph, \ the right comparison is a calculation", font_size=26, color=BANDC),
            label(r"next: \ computing the adjustment formula when $X$ is not one binary variable", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So Simpson's paradox is not a paradox of probability; the arithmetic is fine. <bookmark "
            "mark='b'/> It is a reminder that causal questions need causal assumptions. <bookmark mark='c'/> With the graph, "
            "choosing the right comparison is a calculation. <bookmark mark='d'/> Next, carrying out that calculation when the "
            "covariates are many and continuous."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
