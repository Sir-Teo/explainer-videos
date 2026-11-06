from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Surrogates(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. Surrogates and long-term effects: answering a ten-year question in one year.", 9,
                            r"Surrogates", r"Short-term proxies for long-term effects", lit=(2019,))
        self.problem()
        self.paradox()
        self.principal()
        self.index()
        self.chart()
        self.uses()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The outcome that matters often takes years: survival, lifetime earnings, a child's "
            "eventual schooling. Decisions cannot wait. <bookmark mark='b'/> A surrogate is an early measurement standing "
            "in for the late one: tumour shrinkage for survival, blood pressure for strokes. <bookmark mark='c'/> Part "
            "thirty-five's Prentice criteria asked that the treatment's whole effect pass through the surrogate. <bookmark "
            "mark='d'/> That is a strong and untestable condition, and when it fails the result can be not just biased but "
            "reversed.",
            [(r"\text{goal}", r":", r"\text{the effect on a late outcome } Y", 40),
             (r"\text{surrogate}", r":", r"\text{an early } S \text{ standing in for } Y", 40),
             (r"\text{Prentice}", r":", r"Y \perp T \mid S", 40),
             (r"\text{if not}", r":", r"\text{bias, \ even reversal}", 40)],
            [r"the long wait", r"tumours, \ pressures", r"Part 35", r"the surrogate paradox"],
            colors=[(3, NAIVEC)])

    def paradox(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The Museum's most famous reversal is the CAST trial of 1989, from Part fifty-eight. "
            "<bookmark mark='b'/> Encainide and flecainide suppressed the irregular heartbeats that predicted death after a "
            "heart attack: the surrogate improved. <bookmark mark='c'/> But patients on the drugs died more often: 63 deaths "
            "against 26 on placebo, in Echt and co-authors' 1991 report, and the drug arms were stopped. <bookmark mark='d'/> Tyler VanderWeele named the general phenomenon the "
            "surrogate paradox in 2013: a treatment can help the surrogate, the surrogate can help the outcome, and the "
            "treatment can still harm the outcome, through another path or a different subgroup.",
            [(r"\text{CAST (1989)}", r":", r"\text{arrhythmias suppressed}", 40),
             (r"\text{but}", r":", r"63 \text{ deaths on the drugs vs } 26 \text{ on placebo}", 40),
             (r"\text{paradox}", r":", r"T \nearrow S, \ S \nearrow Y, \ \text{yet } T \searrow Y", 40),
             (r"\text{why}", r":", r"\text{another path, \ or another subgroup}", 40)],
            [r"Part 58: \ the surrogate improved", r"Echt et al. (1991)", r"VanderWeele (2013)", r"Prentice fails"],
            colors=[(1, NAIVEC)])

    def index(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Susan Athey, Raj Chetty, Guido Imbens and Hyunseung Kang's surrogate index, from 2019, "
            "uses many surrogates and two data sets. <bookmark mark='b'/> An observational sample where both the surrogates "
            "and the long-term outcome are seen: fit the outcome as a function of the surrogates. <bookmark mark='c'/> An "
            "experiment where only the surrogates are seen: predict the long-term outcome from them, and compare arms. "
            "<bookmark mark='d'/> Two assumptions: surrogacy, that the treatment works only through the surrogates "
            "together; and comparability, that the surrogate-to-outcome relation is the same in both samples.",
            [(r"\text{observational}", r":", r"\hat g(s) = \hat E[Y \mid S = s]", 40),
             (r"\text{experiment}", r":", r"\hat\tau = \overline{\hat g(S)}_{T = 1} - \overline{\hat g(S)}_{T = 0}", 40),
             (r"\text{surrogacy}", r":", r"Y \perp T \mid S \ \text{(jointly)}", 40),
             (r"\text{comparability}", r":", r"E[Y \mid S] \text{ the same in both samples}", 40)],
            [r"Athey et al. (2019)", r"the index", r"applied", r"two assumptions"],
            colors=[(1, IDC)])

    def chart(self):
        d = load("surrogate")
        cases = [("valid", r"surrogacy holds", IDC), ("bypass", r"the treatment also acts directly", NAIVEC)]
        A = axes([-0.6, 1.6], [0, 2.2], x_length=6.4, y_length=4.4, xlabel=r"", ylabel=r"long-term effect",
                 xticks=None, yticks=[0, 0.5, 1, 1.5, 2], center=[-2.6, 0.2, 0])
        ax = A.ax
        grp = VGroup()
        for i, (k, name, c) in enumerate(cases):
            e, se, tr = d[k]["est"], d[k]["se"], d[k]["truth"]
            ci = Line(ax.c2p(i, e - 1.96 * se), ax.c2p(i, e + 1.96 * se), color=c, stroke_width=5)
            dot = Dot(ax.c2p(i, e), radius=0.1, color=c)
            truth = Line(ax.c2p(i - 0.35, tr), ax.c2p(i + 0.35, tr), color=GOLDC, stroke_width=4)
            nm = label(name, font_size=20, color=c).next_to(ax.c2p(i, 0), DOWN, buff=0.3)
            grp.add(VGroup(ci, dot, truth, nm))
        side = side_groups([
            [(r"surrogates $S_1, S_2$ in both samples", WHITE), (r"$Y$ only in 5,000 observational units", GREY_A), (r"2,000 in the experiment", GREY_A)],
            [(r"gold: \ the true long-term effect", GOLDC)],
            [(rf"valid: \ {d['valid']['est']:.2f} vs {d['valid']['truth']:.2f}", IDC)],
            [(rf"bypass: \ {d['bypass']['est']:.2f} vs {d['bypass']['truth']:.2f}", NAIVEC), (r"confidently wrong", NAIVEC)],
        ], width=4.6, pos=(4.1, 0.2, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation with two surrogates, the long-term outcome seen only in an observational "
            f"sample of five thousand, and an experiment of two thousand. <bookmark mark='b'/> The gold bars are the true "
            f"long-term effects. <bookmark mark='c'/> When surrogacy holds, the index estimates {say(d['valid']['est'], 2)} "
            f"against a truth of {say(d['valid']['truth'], 2)}. <bookmark mark='d'/> When the treatment also lowers the outcome "
            f"directly, bypassing the surrogates, the index still says {say(d['bypass']['est'], 2)}, with the same confident "
            f"interval, while the truth is {say(d['bypass']['truth'], 2)}. Nothing in the data warns of it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(g[2]) for g in grp], *[FadeIn(g[3]) for g in grp], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(grp[0][0]), FadeIn(grp[0][1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(grp[1][0]), FadeIn(grp[1][1]), FadeIn(side[3]))
        self.clear_scene()

    def uses(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Where surrogate methods are used, and checked. <bookmark mark='b'/> Athey and co-authors "
            "estimated a job-training programme's long-run earnings effect from a few early quarters, and checked it "
            "against the realized long-run data. <bookmark mark='c'/> Technology companies estimate long-term engagement "
            "from short experiments. <bookmark mark='d'/> Drug regulators accept validated surrogates for accelerated "
            "approval, with confirmatory trials afterward. <bookmark mark='e'/> In each, the check against real long-term "
            "outcomes, where available, is what earns the assumption.",
            [(r"uses:", GREY_A),
             (r"job training: \ long-run earnings from early quarters", IDC),
             (r"online platforms: \ long-term engagement", TRTC),
             (r"accelerated approval: \ validated surrogates", HIDC),
             (r"always: \ validate against real long-term outcomes", GOLDC)])

    def principal(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Constantine Frangakis and Donald Rubin's principal surrogates, in 2002, reframe the "
            "question with potential outcomes. <bookmark mark='b'/> A surrogate is good if, among people whose surrogate "
            "would be the same under both treatments, the treatment has no effect on the outcome: dissociative effects are "
            "zero. <bookmark mark='c'/> And among people whose surrogate the treatment changes, the outcome changes too: "
            "associative effects. <bookmark mark='d'/> These depend on joint potential outcomes, never observed together, so "
            "principal surrogate evaluation needs extra structure, such as baseline predictors of the surrogate.",
            [(r"\text{principal strata}", r":", r"(S(0), S(1))", 40),
             (r"\text{dissociative}", r":", r"S(0) = S(1) \Rightarrow \text{no effect on } Y", 40),
             (r"\text{associative}", r":", r"S(0) \ne S(1) \Rightarrow \text{effect on } Y", 40),
             (r"\text{but}", r":", r"\text{joint potential outcomes: \ unobserved}", 40)],
            [r"Frangakis \& Rubin (2002)", r"Part 35's strata", r"the good case", r"vaccine correlates"],
            colors=[(1, IDC)])
