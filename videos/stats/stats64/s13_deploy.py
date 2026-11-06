from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Deployment(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter twelve. Causal questions about deployed AI systems.", 12,
                            r"Causal questions about deployments", r"When users share a world")
        self.questions()
        self.market()
        self.chart()
        self.designs()
        self.longterm()
        self.observational()

    def questions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Benchmarks measure a model in isolation. The questions people care about are causal. "
            "<bookmark mark='b'/> Does deploying the assistant make programmers more productive? Do students who use it "
            "learn more, or less? Does a new recommender increase sales, or move them from one seller to another? <bookmark "
            "mark='c'/> These are Part thirty-five's potential outcomes, and randomized experiments answer them, when they "
            "are run. <bookmark mark='d'/> Two complications from Part sixty-two come with them: users interact, and the "
            "outcomes that matter take a long time to observe.",
            [(r"\text{benchmarks}", r":", r"\text{the model alone}", 40),
             (r"\text{the questions}", r":", r"\text{effects on people}", 40),
             (r"\text{the tool}", r":", r"\text{randomized experiments}", 40),
             (r"\text{complications}", r":", r"\text{interference, \ long horizons}", 40)],
            [r"capability", r"impact", r"Part 35", r"Part 62"],
            colors=[(2, HONC)])

    def market(self):
        d = load("market")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Interference in a marketplace, simulated. <bookmark mark='b'/> {d['n']:,} buyers and "
            f"{d['supply']:,} items. Each buyer wants an item with probability {d['base']}; a new recommender raises that by "
            f"half. <bookmark mark='c'/> When more buyers want items than there are items, the items go to wanting buyers "
            f"at random. Supply binds: the recommender cannot create items, only decide who gets them. <bookmark mark='d'/> "
            f"Run an ordinary A/B test, half the buyers treated, and compare purchase rates.",
            [(r"\text{buyers}", r":", rf"{d['n']:,}, \ \text{{want w.p. }} {d['base']}".replace(",", "{,}", 1), 40),
             (r"\text{treatment}", r":", rf"\times (1 + {d['lift']}) \ \text{{demand}}", 40),
             (r"\text{supply}", r":", rf"{d['supply']:,} \ \text{{items, \ shared}}".replace(",", "{,}"), 40),
             (r"\text{A/B test}", r":", r"\text{half the buyers treated}", 40)],
            [r"a two-sided market", r"a stronger nudge", r"a binding constraint", r"the usual design"],
            colors=[(2, NAIVEC)])

    def chart(self):
        d = load("market")
        vals = [(d["naive"], d["naive_sd"], NAIVEC, r"A/B test,", r"buyers randomized"),
                (d["global"], d["global_sd"], WHITE, r"the global effect:", r"everyone vs no one"),
                (d["markets"], d["markets_sd"], HONC, rf"{d['n_markets']} markets", r"randomized whole")]
        A = axes([-0.6, 2.6], [0, 0.26], x_length=6.4, y_length=4.2, xlabel=r"", ylabel=r"estimated effect on purchase rate",
                 xticks=None, yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25], center=[-2.8, 0.3, 0])
        ax = A.ax
        bars = VGroup()
        for k, (v, s, c, n1, n2) in enumerate(vals):
            b = Rectangle(width=0.8, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            err = Line(ax.c2p(k, v - 1.96 * s), ax.c2p(k, v + 1.96 * s), color=GREY_A, stroke_width=3)
            nm = VGroup(label(n1, font_size=20, color=c), label(n2, font_size=20, color=c)).arrange(DOWN, buff=0.06)
            bars.add(VGroup(b, err, label(rf"{v:.3f}", font_size=22, color=c).next_to(ax.c2p(k, v + 1.96 * s), UP, buff=0.08), nm.next_to(ax.c2p(k, 0), DOWN, buff=0.15)))
        side = side_groups([
            [(rf"red: \ the A/B test says {d['naive']:.3f}", NAIVEC), (r"treated buyers take control buyers' items", NAIVEC)],
            [(rf"white: \ the real effect, \ {d['global']:.3f}", WHITE), (r"supply caps it", WHITE)],
            [(rf"green: \ market-level randomization", HONC), (rf"{d['markets']:.3f}, \ unbiased", HONC)],
        ], pos=(3.5, 0.3, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> Over three hundred simulated tests, the A/B comparison says the recommender raises "
            f"purchases by {100 * d['naive']:.1f} points. But treated buyers win items that control buyers would otherwise "
            f"have bought: the control group is harmed by the treatment group, a spillover. <bookmark mark='b'/> The effect "
            f"of switching everyone on, against everyone off, is {100 * d['global']:.1f} points: supply caps it. The A/B "
            f"test overstated it more than fourfold. <bookmark mark='c'/> Randomize whole markets instead, {d['n_markets']} "
            f"separate ones, half fully treated, and the estimate is {100 * d['markets']:.1f} points, unbiased, with a wider "
            f"interval because there are only twenty units. Part sixty-two's cluster design, and its price."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2]), FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def designs(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The designs that handle it. <bookmark mark='b'/> Cluster randomization by market, city or "
            "school, Part thirteen. <bookmark mark='c'/> Switchback experiments, which alternate a whole market between "
            "treatment and control over time, a crossover design, used by ride-hailing and delivery platforms. <bookmark "
            "mark='d'/> And two-sided randomization, of both buyers and sellers, whose combinations let the spillover "
            "itself be estimated, as Ramesh Johari and colleagues analysed in 2022.",
            [(r"\text{clusters}", r":", r"\text{markets, \ cities, \ schools}", 40),
             (r"\text{switchbacks}", r":", r"\text{alternate a market over time}", 40),
             (r"\text{two-sided}", r":", r"\text{randomize buyers and sellers}", 40),
             (r"\text{price}", r":", r"\text{fewer, \ larger units}", 40)],
            [r"Part 13", r"a crossover", r"Johari et al. (2022)", r"precision for validity"],
            colors=[(0, HONC)])

    def longterm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Long horizons. <bookmark mark='b'/> Whether students who use an assistant learn more is "
            "visible only at the end of a course, or later. <bookmark mark='c'/> Part sixty-two's surrogate index predicts "
            "the long-term outcome from short-term ones, such as homework scores and engagement, using an older dataset "
            "where both were observed. <bookmark mark='d'/> Its condition, that the treatment affects the long-term "
            "outcome only through the surrogates, is exactly what an assistant that writes the homework would violate: "
            "homework scores rise, and learning may not. The surrogate paradox, in a classroom.",
            [(r"\text{long-term}", r":", r"\text{learning, \ careers, \ health}", 40),
             (r"\text{surrogate index}", r":", r"\text{predict it from short-term outcomes}", 40),
             (r"\text{condition}", r":", r"\text{no path that bypasses the surrogates}", 40),
             (r"\text{the risk}", r":", r"\text{homework rises, \ learning does not}", 40)],
            [r"slow outcomes", r"Athey et al. (2019)", r"surrogacy", r"Part 62's paradox"],
            colors=[(3, NAIVEC)])

    def observational(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> And when no experiment was run. <bookmark mark='b'/> People who choose to use an assistant "
            "differ from those who do not, so comparing them is Part thirty-six's confounded comparison. <bookmark "
            "mark='c'/> The staggered rollout of a tool across teams or countries is Part thirty-seven's difference in "
            "differences, with its modern estimators for staggered adoption. <bookmark mark='d'/> The statistics of AI "
            "deployment is the statistics of policy evaluation: the same designs, the same assumptions, stated as clearly.",
            [(r"\text{self-selected users}", r":", r"\text{confounded}", 40),
             (r"\text{staggered rollouts}", r":", r"\text{difference in differences}", 40),
             (r"\text{estimators}", r":", r"\text{Callaway--Sant'Anna and kin}", 40),
             (r"\text{in short}", r":", r"\text{policy evaluation}", 40)],
            [r"Part 36", r"Part 37", r"Part 37", r"the same discipline"],
            colors=[(0, NAIVEC), (3, HONC)])
