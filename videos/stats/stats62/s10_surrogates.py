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
            "<bookmark mark='a'/> Some important outcomes take years to observe. <bookmark mark='b'/> Early measurements may act as surrogate outcomes, but their predictive association alone does not validate a treatment-effect substitution. <bookmark mark='c'/> Prentice's conditional-independence criterion is a statistical statement about treatment and outcome given the surrogate in a specified setting. It is not simply equivalent to a graph saying all directed causal paths pass through the surrogate; conditioning on a post-treatment variable can change associations. <bookmark mark='d'/> Surrogate validity needs assumptions appropriate to the target treatment, outcome and population, and its failure can cause substantial bias or sign reversal.",
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
            "<bookmark mark='a'/> Susan Athey, Raj Chetty, Guido Imbens and Hyunseung Kang's surrogate index, from 2019, uses many surrogates and two data sets. <bookmark mark='b'/> An observational sample where both the surrogates and the long-term outcome are seen: fit the outcome as a function of the surrogates. <bookmark mark='c'/> An experiment where only the surrogates are seen: predict the long-term outcome from them, and compare arms. <bookmark mark='d'/> Two assumptions: surrogacy, a suitable conditional independence of the long-term outcome and randomized treatment given the surrogates; and comparability, that the surrogate-to-outcome relation is the same in both samples.",
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
            "<bookmark mark='a'/> The two-sample simulation observes outcomes and surrogates in five thousand untreated training units and only surrogates in a two-thousand-unit randomized experiment. <bookmark mark='b'/> The gold bars mark the known long-term effects. Standard errors now include both trial variation and fitting the index in the independent training sample, using a linear-model delta approximation. <bookmark mark='c'/> In the valid case the simulated outcome regression is shared across samples and the index estimates the effect reasonably. <bookmark mark='d'/> The bypass case adds a direct treatment effect absent from the untreated training sample. Here both experimental surrogacy and cross-sample conditional-mean comparability fail. The narrow index interval misses the true effect; these observed datasets alone cannot validate the missing long-term response."
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
            "<bookmark mark='a'/> Principal-surrogate approaches define strata by the pair of potential surrogate outcomes. <bookmark mark='b'/> Causal necessity asks about a zero treatment effect, typically a stratum-average effect, among units whose surrogate would not change. <bookmark mark='c'/> Causal sufficiency or associative-effect criteria concern how outcome effects vary with changes in the surrogate; they are not an automatic individual-level implication that every changed surrogate forces a changed outcome. <bookmark mark='d'/> Joint surrogate potential outcomes are not jointly observed, so evaluation needs additional assumptions or information.",
            [(r"\text{principal strata}", r":", r"(S(0), S(1))", 40),
             (r"\text{dissociative}", r":", r"E[Y(1)-Y(0)\mid S(0)=S(1)]=0\ \text{(a necessity criterion)}", 40),
             (r"\text{associative}", r":", r"\text{associative strata: \ relate average }Y\text{ effects to }S\text{ changes}", 40),
             (r"\text{but}", r":", r"\text{joint potential outcomes: \ unobserved}", 40)],
            [r"Frangakis \& Rubin (2002)", r"Part 35's strata", r"the good case", r"vaccine correlates"],
            colors=[(1, IDC)])
