from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Question(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The question made answerable", r"What exactly is proposed, \ to whom, \ against what?",
             "Chapter one. The question made answerable.", lit={2017: r"TCJA", 2021: r"ARPA"},
             scale=("household", "nation"), horizon=("a year", "a decade"))
        self.proposal()
        self.families()
        self.channels()
        self.criteria()

    def proposal(self):
        rows = [
            (r"per child", r"2,000 \ (under 17)", r"3,600 under six, \\ 3,000 from six to seventeen"),
            (r"if the family \\ earns little", r"refundable only up to 1,400, \\ 15\% of earnings above 2,500",
             r"fully refundable: \\ no earnings needed"),
            (r"paid", r"once a year, \ at tax time", r"monthly"),
            (r"for the better off", r"phased out above \\ 200,000 \ (400,000 a couple)",
             r"the extra phased out above \\ 75,000 \ (150,000 a couple)"),
            (r"paid for by", r"---", r"to be decided: \\ borrowing, \ a top surtax, \ cuts"),
        ]
        head = VGroup(label(r"", font_size=20), label(r"the credit before 2021", font_size=22, color=OLD),
                      label(r"the proposal", font_size=22, color=NEW))
        grid = VGroup()
        for r in rows:
            grid.add(VGroup(label(r[0], font_size=19, color=GREY_A), label(r[1], font_size=19, color=OLD),
                            label(r[2], font_size=19, color=NEW)))
        xs = (-4.6, -0.9, 3.4)
        y = 2.3
        for m, x in zip(head, xs):
            m.move_to([x, y, 0])
        y -= 0.75
        for g in grid:
            h = max(m.height for m in g)
            for m, x in zip(g, xs):
                m.move_to([x, y - h / 2 + 0.2, 0])
            y -= h + 0.42
        lines = VGroup(*[Line([-6.2, g.get_top()[1] + 0.2, 0], [6.2, g.get_top()[1] + 0.2, 0], stroke_width=1,
                              color=GREY_D) for g in grid])
        tag = published_tag(tables.CREDITS_50.tag, corner=DR, font_size=12)
        with self.voiceover(
            "A memo begins by pinning the question down, because a vague question gets a vague answer. What "
            "exactly is proposed? <bookmark mark='a'/> The old credit, as it stood from 2018 to 2020, paid up to "
            "two thousand dollars a child. <bookmark mark='b'/> But a family that earned little got only part of "
            "it: at most fourteen hundred dollars a child, and only fifteen cents for every dollar earned above "
            "twenty-five hundred. A family with no earnings got nothing. <bookmark mark='c'/> It came once a year, "
            "at tax time. <bookmark mark='d'/> The proposal is the 2021 design made permanent: thirty-six hundred "
            "dollars for each child under six and three thousand for each older child, the whole of it paid "
            "whatever the family earns, every month, with the extra phased out for the better off. <bookmark "
            "mark='e'/> How to pay for it is a separate decision, and the memo must keep it separate, because the "
            "answer can depend on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid[0][0]), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(grid[0][1]), *[FadeIn(g[0]) for g in grid[1:]], *[FadeIn(ln) for ln in lines[1:]])
            vo.wait_until("b")
            self.play(FadeIn(grid[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(grid[2][1]), FadeIn(grid[3][1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(g[2], shift=LEFT * 0.15) for g in grid[:4]], lag_ratio=0.4),
                      run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(grid[4][1]), FadeIn(grid[4][2], shift=LEFT * 0.15))
            self.play(Indicate(grid[4][2], color=WHITE, scale_factor=1.04))
        self.clear_scene()

    def families(self):
        F = load("families")
        n_single = int(round(100 * F["single"]))
        dots = VGroup()
        for i in range(100):
            single = i < n_single
            dots.add(Circle(radius=0.13, stroke_width=0, fill_color=CHILD if single else WORK, fill_opacity=0.9))
        dots.arrange_in_grid(rows=10, cols=10, buff=0.12).move_to(LEFT * 3.6 + DOWN * 0.2)
        cap = label(r"100 families \ $\approx$ \ 400 on the Island", font_size=18, color=GREY_A).next_to(
            dots, UP, buff=0.25)
        ax = plane([0.4, 4.6], [0, 0.5], center=RIGHT * 2.9 + DOWN * 0.9, x_length=4.6, y_length=2.6, xticks=[],
                   yticks=[0, 0.25, 0.5], yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"families with ... children",
                   font_size=13)
        bars = VGroup()
        for k, s in zip((1, 2, 3, 4), F["kids_dist"]):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, s)
            b = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=CHILD,
                          fill_opacity=0.75).move_to((p0 + p1) / 2)
            bars.add(VGroup(b, label(str(k) if k < 4 else r"4", font_size=16).next_to(ax.ax.c2p(k, 0), DOWN,
                                                                                         buff=0.12),
                            label(rf"{100 * s:.0f}\%", font_size=14, color=GREY_A).next_to(b, UP, buff=0.05)))
        facts = VGroup(
            label(rf"{F['n']:,} families with children".replace(",", "{,}"), font_size=21, color=WHITE),
            label(rf"pink: \ a single parent \ ({100 * F['single']:.0f}\%); \ blue: \ a couple", font_size=19,
                  color=GREY_A),
            label(rf"{F['children']:,} children, \ {100 * F['young_share']:.0f}\% under six".replace(",", "{,}"),
                  font_size=19, color=CHILD),
            label(rf"what the main earner could earn, \ median: \ \${F['median_single']:,.0f} single, \ "
                  rf"\${F['median_couple']:,.0f} a couple".replace(",", "{,}"), font_size=17, color=WORK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 2.9 + UP * 2.0)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Who is touched? The memo is for the Island, so it is answered on the Island. <bookmark mark='a'/> The "
            f"Island has {F['n']:,} families with children. <bookmark mark='b'/> About a third are single parents, "
            f"{100 * F['single']:.0f} percent, the rest couples. <bookmark mark='c'/> They have "
            f"{F['children']:,} children between them, about a third of them under six. <bookmark mark='d'/> Most "
            "families have one or two children; a few have four. <bookmark mark='e'/> And what matters most for "
            "how they respond: what the main earner could earn in a year if they worked, about twenty-eight "
            "thousand dollars for the median single parent and fifty-two thousand for the median couple, with a "
            "long spread on both sides. These people are simulated, as always on the Island, built loosely to "
            "resemble American families."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(tag), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]), Indicate(VGroup(*dots[:n_single]), color=WHITE, scale_factor=1.05))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(ax), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.3),
                      run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(facts[3]))
        self.clear_scene()

    def channels(self):
        chain = flow_chain([(r"the allowance", NEW), (r"the family's \\ budget", CHILD), (r"work", WORK),
                            (r"earnings \\ and taxes", BUDGET), (r"poverty \\ and the budget", POOR),
                            (r"children's \\ later lives", EVIDENCE)],
                           box_w=1.85, box_h=1.0, buff=0.32, font_size=18,
                           notes=[r"the payment", r"now", r"months", r"a year", r"a year", r"decades"], note_size=15)
        chain.move_to(UP * 0.9)
        markets = label(r"markets: \ labour, \ what families buy, \ housing, \ the government's budget", font_size=21,
                        color=GREY_A).next_to(chain, DOWN, buff=0.8)
        horizon = label(r"the memo must say which horizon each number belongs to", font_size=22,
                        color=E.ACCENT).next_to(markets, DOWN, buff=0.4)
        with self.voiceover(
            "Through which channels does it work, and over what horizon? <bookmark mark='a'/> The money arrives in "
            "the family's budget at once. <bookmark mark='b'/> Over the following months parents decide whether "
            "and how much to work, <bookmark mark='c'/> which changes their earnings and the taxes and credits "
            "they pay and receive. <bookmark mark='d'/> Within the year those decide two of the memo's numbers: "
            "how many children are poor, and what the policy costs. <bookmark mark='e'/> And over decades, the "
            "children's own schooling, health and earnings, which may feed back into the budget. <bookmark "
            "mark='f'/> The markets touched are the labour market, the markets for what families buy, housing, and "
            "the government's own budget. <bookmark mark='g'/> Each number in the memo belongs to one horizon, and "
            "the memo should say which."
        ) as vo:
            self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[i]), FadeIn(chain.boxes[i + 1]), FadeIn(chain.notes[i + 1]),
                          run_time=0.9)
            vo.wait_until("f")
            self.play(FadeIn(markets, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(horizon, shift=UP * 0.1), Indicate(chain.notes, color=E.ACCENT, scale_factor=1.05))
        self.clear_scene()

    def criteria(self):
        cards = point_cards([
            (r"the comparison", r"the allowance against the old credit, \ not against nothing", GREY_A),
            (r"child poverty", r"children below the Island's line: \ 24,000 for two adults and two children, \ "
                               r"scaled by the square root of family size".replace("24,000", "24{,}000"), POOR),
            (r"work", r"how many parents stop or start working", WORK),
            (r"cost", r"the credits paid, \ net of changes in taxes", BUDGET),
            (r"value", r"what families gain per dollar the government spends", NEW),
            (r"who gains", r"the change in income by decile; \ who pays", CHILD),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.3)
        head = label(r"what counts as an answer", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        rule = label(r"answerable: \ the policy, \ the people, \ the outcomes, \ the comparison, \ the horizon",
                     font_size=22, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "And what counts as an answer? <bookmark mark='a'/> First, the comparison: the allowance against the "
            "credit it replaces, not against doing nothing. <bookmark mark='b'/> Then child poverty, measured "
            "against the Island's own line: twenty-four thousand dollars a year for two adults and two children, "
            "more for bigger families and less for smaller ones. <bookmark mark='c'/> Work: how many parents stop "
            "working, or start. <bookmark mark='d'/> The cost, counting the credits paid and the change in taxes "
            "collected. <bookmark mark='e'/> The value: what families gain per dollar the government spends, the "
            "yardstick of Part forty-two. <bookmark mark='f'/> And who gains and who pays. <bookmark mark='g'/> "
            "With the policy, the people, the outcomes, the comparison and the horizon named, the question can be "
            "answered."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcdef", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(rule, shift=UP * 0.1))
        self.clear_scene()
