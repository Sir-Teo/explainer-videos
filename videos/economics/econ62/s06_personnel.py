from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Personnel(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Personnel economics", r"How should a firm pay its workers, \ and whom should it promote?",
             "Chapter five. Personnel economics.", lit={1969: r"the Peter principle", 2000: r"Safelite",
                                                         2019: r"Benson, Li and Shue"},
             scale=("person", "firm"), horizon=("a year",))
        self.piece()
        self.peter()
        self.called()

    def piece(self):
        P = load("piece")
        y0 = P["output_wage"]
        vals = [100.0, 100 * P["output_same_workers"] / y0, 100 * P["output_after"] / y0]
        ax = plane([-0.6, 2.6], [0, 160], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.8, y_length=4.4, xticks=[],
                   yticks=[0, 50, 100, 150], ylabel=r"output per worker \ (hourly wage = 100)",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        cols = (GREY_B, WORK, PLANT)
        b = bars(ax, range(3), vals, cols, width=0.55)
        names = (r"hourly wage", r"piece rate, \\ the same workers", r"piece rate, \\ after turnover")
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.1)
                        for k, (n, c) in enumerate(zip(names, cols))])
        vl = VGroup(*[label(f"{v:.0f}", font_size=15, color=c).next_to(x, UP, buff=0.06)
                      for v, c, x in zip(vals, cols, b)])
        side = VGroup(
            label(r"an hourly wage pays for the standard, \ and no more", font_size=19, color=GREY_B),
            label(r"a piece rate, \ with the old wage guaranteed: \\ able workers now choose to do more",
                  font_size=19, color=WORK),
            label(rf"effort: \ +{100 * P['gain_effort']:.0f}\% from the same people", font_size=20, color=WORK),
            label(rf"sorting: \ new hires are abler; \ +{100 * P['gain_total']:.0f}\% in all, \ "
                  rf"{100 * P['share_sorting']:.0f}\% of it from who joins", font_size=20, color=PLANT),
            label(r"Safelite's windscreen installers, \ in the 1990s: \ output per worker +44\% \ (Lazear)",
                  font_size=19, color=E.ACCENT),
            label(r"the catch: \ output becomes more unequal, \ and quality needs watching", font_size=18,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Lazear, \ American Economic Review 90(5) (2000); \ the Island: \ agora.org.piece\_rates",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Part fourteen built incentive theory. Personnel economics takes it into the firm, and its most famous "
            "case is a windscreen company. <bookmark mark='a'/> On the Island, a plant pays its installers by the "
            "hour, and they install the standard number of windscreens and no more, since effort above it is not "
            "paid. <bookmark mark='b'/> Switch to a piece rate, with the old wage guaranteed so nobody loses. "
            f"<bookmark mark='c'/> The same people produce {100 * P['gain_effort']:.0f} percent more: the able ones "
            "now find extra effort worth it. <bookmark mark='d'/> And over time the workforce changes. The piece "
            "rate attracts people who are good at the job and keeps them, so output per worker rises "
            f"{100 * P['gain_total']:.0f} percent in all, about half of it from who joins rather than how hard "
            "anyone works. <bookmark mark='e'/> Edward Lazear found this at Safelite Glass when it switched its "
            "installers to piece rates in the 1990s: output per worker rose forty-four percent, with both "
            "effects at work, and about half of each worker's gain was passed on in higher pay. <bookmark "
            "mark='f'/> The catch is that piece rates pay for what is counted: output becomes more unequal, and "
            "quality, which is harder to count, needs watching."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vl[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(vl[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(vl[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def peter(self):
        P = load("peter")["rules"]
        rules = ("the best seller", "the best manager", "at random")
        cols = (WORK, MGR, GREY_B)
        ax = plane([-0.6, 2.6], [-0.2, 1.6], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.8, y_length=4.4, xticks=[],
                   yticks=[0, 0.5, 1.0, 1.5], ylabel=r"the promoted person's skill \ (standard deviations)",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        x0 = np.arange(3)
        bs = bars(ax, x0 - 0.16, [P[r]["sales_skill"] for r in rules], [GREY_C] * 3, width=0.3)
        bm = bars(ax, x0 + 0.16, [P[r]["manage_skill"] for r in rules], list(cols), width=0.3)
        labs = VGroup(*[label(rf"promote \\ {r}", font_size=14, color=c).next_to(ax.ax.c2p(k, -0.2), DOWN, buff=0.1)
                        for k, (r, c) in enumerate(zip(rules, cols))])
        team = {r: 100 * (P[r]["team_sales"] - P["at random"]["team_sales"]) for r in rules}
        side = VGroup(
            label(r"grey: \ selling skill; \ colour: \ managing skill", font_size=19, color=WHITE),
            label(r"the two skills are only weakly related \ (correlation 0.2)", font_size=19, color=GREY_A),
            label(rf"team sales after: \ best seller {team['the best seller']:+.1f}\%, \ best manager "
                  rf"{team['the best manager']:+.1f}\% \ (against at random)".replace("-", "{-}"), font_size=19,
                  color=MGR),
            label(r"but selling is what the firm can see: \\ promoting for it rewards the sales force, \ and costs "
                  r"the teams", font_size=19, color=WORK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 400 sales teams of 8; \ agora.org.peter", corner=DL, font_size=12)
        with self.voiceover(
            "Promotion is the second tool, and it has a famous flaw. <bookmark mark='a'/> Each of the Island's sales "
            "teams has eight people with two skills: selling, and managing other sellers. <bookmark mark='b'/> The "
            "two are only weakly related. Promote the best seller, and the new manager is a superb salesperson and "
            "an ordinary manager. Promote the best manager, if the firm could see who that is, and the team does "
            "far better: <bookmark mark='c'/> team sales rise about ten percent, against nothing for the best "
            "seller. <bookmark mark='d'/> Firms promote the best seller anyway, partly because selling is what they "
            "can see, and partly because the promotion is itself a prize that keeps the whole sales force "
            "working. The cost lands on the teams."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bs], lag_ratio=0.2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bm], lag_ratio=0.2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["peter_1969"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17)
        cc.move_to(UP * 0.6)
        lesson = label(r"the principle holds where firms let it: \ the cure is to promote on the next job's skills",
                       font_size=21, color=E.ACCENT).next_to(cc, DOWN, buff=0.55)
        tag = published_tag(r"Peter and Hull (1969); \ Benson, \ Li and Shue, \ QJE 134(4) (2019)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1969 Laurence Peter and Raymond Hull put it in a sentence: in a "
            "hierarchy every employee tends to rise to his level of incompetence. People are promoted for doing "
            "their present job well, until they reach one they do badly, and there they stay. <bookmark mark='b'/> "
            "Fifty years later Alan Benson, Danielle Li and Kelly Shue tested it with sales workers at a hundred "
            "and thirty-one firms. Firms do promote their best salespeople, and those salespeople make worse "
            "managers than colleagues who sold less. But firms limit the damage: where the manager's job carries "
            "more responsibility, they give sales less weight. <bookmark mark='c'/> The verdict: partly right. "
            "<bookmark mark='d'/> The principle holds where firms let it, and the cure is to promote on the "
            "skills of the next job, not the last."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()
