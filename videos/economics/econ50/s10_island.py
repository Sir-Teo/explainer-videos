from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Island(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The policy run on the Island", r"How far does child poverty fall, \ once families respond?",
             "Chapter eight. The policy run on the Island.", lit={1957: r"Orcutt", 2021: r"Corinth et al."},
             scale=("household", "nation"), horizon=("a year",))
        self.method()
        self.steps()
        self.who()
        self.fan()
        self.deep()

    def method(self):
        chain = flow_chain([(r"40,000 families".replace(",", "{,}"), CHILD), (r"who works, \\ old credit", OLD),
                            (r"each parent's \\ reward for work", NEW), (r"who works, \\ allowance", WORK),
                            (r"incomes, \\ poverty, \ cost", POOR)],
                           box_w=2.2, box_h=1.05, buff=0.42, font_size=19,
                           notes=[r"simulated", r"85\% of single parents, \\ 95\% of couples' \\ main earners",
                                  r"before and after", r"the elasticity", r"the same draws"], note_size=15)
        chain.move_to(UP * 1.2)
        f = MathTex(r"P(\text{work}) = \frac{1}{1 + e^{-(a_i + b \,\log g_i)}}", font_size=40,
                    color=THEORY).next_to(chain, DOWN, buff=0.85)
        fl = label(r"$g_i$: \ what working adds to the family's income, \ per dollar it could earn; \ $b$ set so "
                   r"the average participation elasticity is the dial's value", font_size=18,
                   color=GREY_A).next_to(f, DOWN, buff=0.3)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Now the analysis the memo rests on: a microsimulation, the method Guy Orcutt proposed in 1957, which "
            "applies the rules of a policy to each family one by one. <bookmark mark='a'/> The Island's forty "
            "thousand families start under the old credit, calibrated so that eighty-five percent of single "
            "parents work and ninety-five percent of couples' main earners. <bookmark mark='b'/> For each parent "
            "the simulation computes what working adds to the family's income, under each system. <bookmark "
            "mark='c'/> Whether they work depends on that reward through a logistic curve, whose slope is set so "
            "that the average participation elasticity is the dial's value, a quarter to begin with. <bookmark "
            "mark='d'/> Then incomes, poverty and the cost follow. Every family uses the same random draws under "
            "both systems, so the comparison is like for like: no difference is noise."
        ) as vo:
            self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), FadeIn(chain.notes[1]))
            vo.wait_until("b")
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(chain.notes[2]))
            vo.wait_until("c")
            self.play(GrowArrow(chain.arrows[2]), FadeIn(chain.boxes[3]), FadeIn(chain.notes[3]), Write(f),
                      FadeIn(fl), run_time=1.6)
            vo.wait_until("d")
            self.play(GrowArrow(chain.arrows[3]), FadeIn(chain.boxes[4]), FadeIn(chain.notes[4]))
        self.clear_scene()

    def steps(self):
        I = load("island")
        vals = [(r"the old credit", 100 * I["old"]["child_poverty"], OLD),
                (r"the allowance, \\ no one responds", 100 * I["static_child_poverty"], HOLD),
                (r"the allowance, \\ families respond", 100 * I["new"]["child_poverty"], NEW)]
        ax = plane([0, 3], [0, 16], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.2, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15], ylabel=r"children in poverty, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        bars = VGroup()
        for i, (n, v, c) in enumerate(vals):
            p0, p1 = ax.ax.c2p(i + 0.2, 0), ax.ax.c2p(i + 0.8, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=c,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(f"{v:.1f}", font_size=18, color=WHITE).next_to(r, UP, buff=0.06),
                            label(n, font_size=16, color=c).next_to(ax.ax.c2p(i + 0.5, 0), DOWN, buff=0.15)))
        side = VGroup(
            label(rf"no response: \ {100 * I['static_fall']:.0f}\% fewer poor children", font_size=19, color=HOLD),
            label(rf"{I['exits']:.0f} parents stop working: \\ {100 * I['exit_share']:.1f}\% of those who worked",
                  font_size=19, color=WORK),
            label(rf"with responses: \ {100 * I['fall']:.0f}\% fewer", font_size=21, color=NEW),
            label(r"your forecast: \ a tenth to a quarter \\ was right", font_size=21, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            f"The results. <bookmark mark='a'/> Under the old credit, {vals[0][1]:.1f} percent of the Island's "
            "children are poor. <bookmark mark='b'/> If no family changed what it did, the allowance would bring "
            f"that to {vals[1][1]:.1f} percent, {100 * I['static_fall']:.0f} percent fewer poor children. This is "
            "the static arithmetic, the kind of number a first headline uses. <bookmark mark='c'/> But at an "
            f"elasticity of a quarter, {I['exits']:.0f} parents stop working, {100 * I['exit_share']:.1f} percent "
            "of those who worked. Their families lose earnings and earned income credits, and some of them fall "
            f"below the line. <bookmark mark='d'/> With responses, child poverty is {vals[2][1]:.1f} percent: "
            f"{100 * I['fall']:.0f} percent fewer poor children, about two thirds of the static fall. <bookmark "
            "mark='e'/> Your forecast from chapter four: if you chose a tenth to a quarter, you were right; if you "
            "anchored on the 2021 headline of almost half, the difference is the measure, the year's other aid, "
            "and the responses a permanent policy would bring."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            for k, mk in enumerate("ab"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[k][0], DOWN), FadeIn(bars[k][1:]))
                if k == 1:
                    self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]), Indicate(bars[2], color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def who(self):
        I = load("island")
        q = I["quit_by_potential"]
        names = [r"under 10k", r"10--20k", r"20--30k", r"30--40k", r"40--60k", r"60k+"]
        ax = plane([0, 6], [0, 0.035], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.0, y_length=4.4, xticks=[],
                   yticks=[0, 0.01, 0.02, 0.03], ylabel=r"share of working parents who stop",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        bars = VGroup()
        for i, (n, v) in enumerate(zip(names, q["rate"])):
            p0, p1 = ax.ax.c2p(i + 0.18, 0), ax.ax.c2p(i + 0.82, v)
            r = Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=WORK,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(rf"{100 * v:.1f}", font_size=15, color=WHITE).next_to(r, UP, buff=0.05),
                            label(n, font_size=15, color=GREY_A).next_to(ax.ax.c2p(i + 0.5, 0), DOWN, buff=0.12)))
        xl = label(r"what the parent could earn in a year", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.55)
        side = VGroup(
            label(r"the whole old credit \\ needed earnings: \\ the reward falls by \\ about a tenth \\ up to 40k",
                  font_size=17, color=WHITE),
            label(rf"single parents: \\ {100 * I['quit_single_share']:.0f}\% of those \\ who stop", font_size=17,
                  color=CHILD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Who stops working? <bookmark mark='a'/> Not only the lowest earners. Under the old credit a family "
            "needed earnings to receive any of it, and enough earnings to receive all of it; so for parents who "
            "could earn anywhere up to about forty thousand dollars, the allowance cuts the reward for working by "
            f"roughly a tenth, and about two to three percent of them stop. <bookmark mark='b'/> Above that the "
            "cut is smaller, and fewer stop. <bookmark mark='c'/> And single parents, a third of families, are "
            f"{100 * I['quit_single_share']:.0f} percent of those who stop, because for them working is a closer "
            "call: they have no second earner, and more of them are near the margin."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars[:4]], lag_ratio=0.2),
                      *[FadeIn(b[1:]) for b in bars[:4]], FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars[4:]], *[FadeIn(b[1:]) for b in bars[4:]])
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def fan(self):
        Fn = load("fan")
        e = Fn["elasticity"]
        ax = plane([0, 0.5], [0, 16], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 5, 10, 15],
                   xlabel=r"participation elasticity \ (the dial)", ylabel=r"children in poverty, \ \%",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        old = DashedLine(ax.ax.c2p(0, 100 * Fn["old"]), ax.ax.c2p(0.5, 100 * Fn["old"]), color=OLD, stroke_width=2.4)
        new = path(ax, e, [100 * v for v in Fn["new"]], NEW, 3.4)
        gap = band(ax, e, [100 * v for v in Fn["new"]], [100 * Fn["old"]] * len(e), GAIN, 0.18)
        central = vline(ax, 0.25, 0, 16, GREY_B)
        side = VGroup(
            label(rf"grey: \ the old credit, \ {100 * Fn['old']:.1f}", font_size=18, color=OLD),
            label(rf"gold: \ the allowance, \\ {100 * Fn['new'][0]:.1f} at zero \\ to {100 * Fn['new'][-1]:.1f} "
                  r"at 0.5", font_size=18, color=NEW),
            label(rf"at 0.5: \ {Fn['exits'][-1]:,.0f} parents stop".replace(",", "{,}"), font_size=18, color=WORK),
            label(r"the fall in poverty \\ survives the whole \\ range of the dial", font_size=19, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "But the elasticity is uncertain, so the memo cannot rest on a quarter. Run it across the whole range "
            "of the dial. <bookmark mark='a'/> The old credit's poverty rate stays where it is. <bookmark "
            f"mark='b'/> The allowance's rises with the elasticity: {100 * Fn['new'][0]:.1f} percent if no one "
            f"responds, {100 * Fn['new'][-1]:.1f} percent at an elasticity of a half, <bookmark mark='c'/> where "
            f"{Fn['exits'][-1]:,.0f} parents stop working. <bookmark mark='d'/> Across the whole range the "
            "allowance leaves fewer children in poverty than the old credit. The size of the fall depends on the "
            "dial; its direction does not."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(central))
            vo.wait_until("a")
            self.play(Create(old), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(new), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(gap), FadeIn(side[3]))
        self.clear_scene()

    def deep(self):
        Fn = load("fan")
        e = Fn["elasticity"]
        ax = plane([0, 0.5], [0, 12], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 4, 8, 12],
                   xlabel=r"participation elasticity \ (the dial)", ylabel=r"children in deep poverty, \ \%",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        old = DashedLine(ax.ax.c2p(0, 100 * Fn["deep_old"]), ax.ax.c2p(0.5, 100 * Fn["deep_old"]), color=OLD,
                         stroke_width=2.4)
        new = path(ax, e, [100 * v for v in Fn["deep_new"]], POOR, 3.4)
        xc = Fn["deep_cross"]
        cross = dot(ax, xc, 100 * Fn["deep_old"], WHITE, 0.08)
        cl = label(rf"{xc:.2f}", font_size=16, color=WHITE).next_to(cross, UP, buff=0.15)
        side = VGroup(
            label(r"deep poverty: \\ below half the line", font_size=19, color=WHITE),
            label(rf"grey: \ the old credit, \ {100 * Fn['deep_old']:.1f}", font_size=18, color=OLD),
            label(rf"red: \ the allowance, \\ {100 * Fn['deep_new'][0]:.1f} to {100 * Fn['deep_new'][-1]:.1f}",
                  font_size=18, color=POOR),
            label(r"a parent who stops \\ loses earnings and \\ the EITC; \ the allowance \\ does not replace them",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "One number does change sign, and the memo must report it. <bookmark mark='a'/> Deep poverty: "
            "children whose families have less than half the poverty line. <bookmark mark='b'/> Under the old "
            f"credit, {100 * Fn['deep_old']:.1f} percent. <bookmark mark='c'/> Under the allowance, "
            f"{100 * Fn['deep_new'][0]:.1f} percent if no one responds, but rising faster with the elasticity, "
            f"<bookmark mark='d'/> and above an elasticity of about {xc:.2f}, higher than under the old credit. "
            "<bookmark mark='e'/> The reason is the parents who stop working: they give up their earnings and "
            "their earned income credit, and an allowance of a few thousand dollars does not replace them. A "
            "single parent of two who stops working lands below half the line. This is exactly the finding the "
            "simulation of chapter seven emphasized, and it is why the elasticity matters so much."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(old), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(new), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(cross), FadeIn(cl), Indicate(cross, color=WHITE, scale_factor=1.6))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
