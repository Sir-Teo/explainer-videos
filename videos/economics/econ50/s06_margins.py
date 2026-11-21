from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Margins(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The margins the textbook misses", r"Who claims it, \ when it arrives, \ what it is called",
             "Chapter five. The margins the textbook misses.", lit={1997: r"Lundberg, Pollak and Wales",
                                                                   2021: r"the non-filer portal"},
             scale=("household",), horizon=("a month", "a year"))
        self.takeup()
        self.timing()
        self.labels()

    def takeup(self):
        T = load("tornado")
        tp = {r["dial"]: r for r in T["child_poverty"]}["take_up"]
        tc = {r["dial"]: r for r in T["per_child"]}["take_up"]
        ax = plane([0, 4], [0, 16], center=LEFT * 3.4 + DOWN * 0.4, x_length=4.6, y_length=4.2, xticks=[],
                   yticks=[0, 5, 10, 15], ylabel=r"children in poverty, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=13)
        bx = plane([0, 4], [0, 1600], center=RIGHT * 1.6 + DOWN * 0.4, x_length=4.6, y_length=4.2, xticks=[],
                   yticks=[0, 500, 1000, 1500], ylabel=r"cost per child, \ \$",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=13)

        def bar(axes, x, v, col, txt):
            p0, p1 = axes.ax.c2p(x - 0.55, 0), axes.ax.c2p(x + 0.55, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            return VGroup(r, label(txt, font_size=15, color=WHITE).next_to(r, UP, buff=0.06))

        old = DashedLine(ax.ax.c2p(0, 100 * T["old_poverty"]), ax.ax.c2p(4, 100 * T["old_poverty"]), color=OLD,
                         stroke_width=2)
        old_l = label(rf"old credit: \ {100 * T['old_poverty']:.1f}", font_size=14, color=OLD).next_to(
            old, UP, buff=0.06).align_to(old, RIGHT)
        pb = VGroup(bar(ax, 1.2, 100 * tp["at_high"], NEW, f"{100 * tp['at_high']:.1f}"),
                    bar(ax, 2.8, 100 * tp["at_low"], HOLD, f"{100 * tp['at_low']:.1f}"))
        cb = VGroup(bar(bx, 1.2, tc["at_high"], NEW, f"{tc['at_high']:,.0f}".replace(",", "{,}")),
                    bar(bx, 2.8, tc["at_low"], HOLD, f"{tc['at_low']:,.0f}".replace(",", "{,}")))
        names = VGroup(*[VGroup(label(r"all claim", font_size=15, color=NEW).next_to(a.ax.c2p(1.2, 0), DOWN,
                                                                                     buff=0.15),
                                label(r"85\% claim", font_size=15, color=HOLD).next_to(a.ax.c2p(2.8, 0), DOWN,
                                                                                       buff=0.15))
                         for a in (ax, bx)])
        side = VGroup(
            label(r"the poorest families \\ often file no tax \\ return at all", font_size=17, color=WHITE),
            label(r"on the Island \\ the missing are drawn \\ at random: \ the real \\ loss is likely larger",
                  font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Textbook pictures assume that everyone eligible for a payment receives it. They do not. <bookmark "
            "mark='a'/> A credit paid through the tax system reaches families that file a tax return, and the "
            "families with the lowest incomes are the most likely not to file at all, because they owe nothing. "
            "In 2021 the tax authority built a simplified portal for them. <bookmark mark='b'/> On the Island, "
            "if every family claims, child poverty under the allowance is "
            f"{100 * tp['at_high']:.1f} percent; <bookmark mark='c'/> if only eighty-five percent claim, it is "
            f"{100 * tp['at_low']:.1f}. <bookmark mark='d'/> The cost falls too, from {tc['at_high']:,.0f} dollars "
            f"a child to {tc['at_low']:,.0f}: incomplete take-up saves money exactly by failing the families the "
            "policy is for. <bookmark mark='e'/> And the Island is generous here: it lets the families who miss "
            "out be chosen at random. In fact they are poorer than average, so the real loss would be larger."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(bx), FadeIn(old), FadeIn(old_l), FadeIn(tag), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(pb[0][0], DOWN), FadeIn(pb[0][1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(pb[1][0], DOWN), FadeIn(pb[1][1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(cb[0][0], DOWN), FadeIn(cb[0][1]), GrowFromEdge(cb[1][0], DOWN), FadeIn(cb[1][1]),
                      run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[1], shift=UP * 0.1))
        self.clear_scene()

    def timing(self):
        months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        ax_old = plane([0, 12], [0, 4000], center=UP * 1.35 + LEFT * 1.6, x_length=8.2, y_length=2.0, xticks=[],
                       yticks=[0, 4000], yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=12)
        ax_new = plane([0, 12], [0, 4000], center=DOWN * 1.65 + LEFT * 1.6, x_length=8.2, y_length=2.0,
                       xticks=[], yticks=[0, 4000], yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=12)
        S = load("schedules")
        full = S["at0_new"]

        def bars(axes, vals, col):
            g = VGroup()
            for i, v in enumerate(vals):
                p0, p1 = axes.ax.c2p(i + 0.15, 0), axes.ax.c2p(i + 0.85, max(v, 1))
                g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                fill_opacity=0.85).move_to((p0 + p1) / 2))
            return g

        lump = [0.0] * 12
        lump[2] = 2745.0
        b_old = bars(ax_old, lump, OLD)
        b_new = bars(ax_new, [full / 12] * 12, NEW)
        ml = VGroup(*[label(m, font_size=13, color=GREY_B).next_to(ax_new.ax.c2p(i + 0.5, 0), DOWN, buff=0.1)
                      for i, m in enumerate(months)])
        l_old = label(r"the old credit, \ working at 20k: \\ one payment, \ at tax time", font_size=16,
                      color=OLD).next_to(ax_old, RIGHT, buff=0.3)
        l_new = label(rf"the allowance: \\ \${full / 12:,.0f} every month".replace(",", "{,}"), font_size=16,
                      color=NEW).next_to(ax_new, RIGHT, buff=0.3)
        sch = label(r"schematic: \ when the money arrives in one year", font_size=13, color=GREY_B).to_corner(
            DL, buff=0.3)
        risk = label(r"the catch: \ monthly payments rest on last year's income, \ and someone must bear the "
                     r"overpayments", font_size=18, color=HOLD).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Second, timing. <bookmark mark='a'/> The old credit arrived once a year, in a lump at tax time. For "
            "a family with savings that makes little difference. <bookmark mark='b'/> For a family living month "
            "to month, a monthly payment is a different thing: it arrives when the rent and the food bills do. "
            "The present bias of Part forty-five says the same from the other side: a large sum in March is "
            "easily spent by April. During the six months of 2021, the Census Bureau's surveys found families "
            "spending the payments most often on food, and then on school costs, clothing, rent and bills. "
            "<bookmark mark='c'/> The catch: monthly payments are based on last year's income and family, and "
            "when circumstances change, someone must bear the overpayments. If families repay them at tax time, "
            "the risk falls on those with the least slack; the 2021 law protected low-income families from most "
            "repayment, at a cost to the budget."
        ) as vo:
            self.play(FadeIn(ax_old), FadeIn(ax_new), FadeIn(ml), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowFromEdge(b_old[2], DOWN), FadeIn(l_old))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b_new], lag_ratio=0.15), FadeIn(l_new),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(risk, shift=UP * 0.1))
        self.clear_scene()

    def labels(self):
        cards = point_cards([
            (r"money is fungible", r"a dollar for children frees a dollar for anything else: \ in the textbook, \ "
                                   r"the label does nothing", GREY_A),
            (r"whose purse", r"paid to the mother, \ spending on children rose: \ Britain in the late 1970s "
                             r"(Part 49)", CHILD),
            (r"what it is called", r"a child benefit, \ a tax credit or welfare: \ the name changes who claims and "
                                   r"how it is spent", NEW),
            (r"what it is tied to", r"a work requirement keeps the reward for work, \ and misses the children of "
                                    r"parents who cannot work", WORK),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"labels, \ recipients, \ conditions", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Third, labels and conditions. <bookmark mark='a'/> In the textbook a dollar is a dollar: money given "
            "for children frees money for anything else, so the label does nothing. <bookmark mark='b'/> But Part "
            "forty-nine showed that whose purse the money reaches matters: when Britain moved its child allowance "
            "from fathers' pay packets to mothers, spending on children's clothing rose. <bookmark mark='c'/> The "
            "name matters too: a child benefit, a tax credit and welfare are claimed by different people and spent "
            "in different ways, which the behavioural economics of Part forty-five calls mental accounting. "
            "<bookmark mark='d'/> And the condition: a work requirement protects the reward for work, at the price "
            "of missing the children whose parents cannot work, because of illness, disability or caring. Each "
            "of these margins moves the answer, and none appears in the textbook picture."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
