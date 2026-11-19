from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403

WHO = ("ana", "bo", "chidi", "dara")


class VCG(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Vickrey, \ Clarke and Groves: \ pay for the harm you do", r"Can a rule make everyone tell the "
             r"truth about what a shared project is worth to them?", "Chapter three. Vickrey, Clarke and Groves: pay "
             "for the harm you do.", lit={1961: r"Vickrey", 1971: r"Clarke", 1973: r"Groves"},
             scale=("person", "community"), horizon=("a year",))
        self.bridge()
        self.pivot()
        self.flaws()

    def bars(self, b, ax, values, color_fn):
        a = ax.ax
        g = VGroup()
        for i, v in enumerate(values):
            lo, hi = a.c2p(i - 0.3, min(0, v)), a.c2p(i + 0.3, max(0, v))
            r = Rectangle(width=hi[0] - lo[0], height=max(hi[1] - lo[1], 0.02), stroke_width=0,
                          fill_color=color_fn(i, v), fill_opacity=0.85).move_to((lo + hi) / 2)
            g.add(r)
        return g

    def bridge(self):
        b = load("bridge")
        ax = plane([-0.6, 3.6], [-25, 45], center=LEFT * 2.4 + DOWN * 0.4, x_length=6.6, y_length=5.0, xticks=[],
                   yticks=[-20, 0, 20, 40], ylabel=r"value of the bridge, \ less a quarter of its cost", font_size=16,
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        zero = Line(a.c2p(-0.6, 0), a.c2p(3.6, 0), color=GREY_B, stroke_width=2)
        net = b["net"]
        bars = self.bars(b, ax, net, lambda i, v: color_of(WHO[i]))
        who = VGroup(*[who_chip(k, 0.45, 16).move_to(a.c2p(i, -21)) for i, k in enumerate(WHO)])
        vals = VGroup(*[label(rf"{v:+.0f}", font_size=18, color=color_of(WHO[i])).next_to(
            bars[i], UP if v >= 0 else DOWN, buff=0.08) for i, v in enumerate(net)])
        side = VGroup(
            label(rf"a footbridge costs {b['share'] * 4:.0f} shells, \\ {b['share']:.0f} from each of four", font_size=21),
            label(r"worth to them: \ " + r", \ ".join(f"{v:.0f}" for v in b["values"]), font_size=21, color=GREY_A),
            label(rf"net values add up to {sum(net):+.0f}: \\ build it", font_size=22, color=STABLE),
            label(r"but ask them, \ and each has a reason to lie: \\ shout if you want it, \ hide if you don't",
                  font_size=20, color=REJECT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Back to the island. A footbridge across the creek would cost a hundred shells, twenty-five from each of "
            "four islanders. <bookmark mark='a'/> It is worth sixty to Ana, ten each to Bo and Chidi, and forty to "
            "Dara. Take away each one's share, and this is what the bridge is worth to them, net. "
            "<bookmark mark='b'/> The net values add up to plus twenty, so the bridge is worth building. "
            "<bookmark mark='c'/> But ask them, and each has a reason to lie. Ana, who wants it, should exaggerate; "
            "Bo and Chidi, who would rather keep their shells, should play their values down. Part fifteen's free "
            "riders are back."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(who), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), *[GrowFromEdge(r, DOWN if v >= 0 else UP) for r, v in zip(bars, net)],
                      FadeIn(vals), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def pivot(self):
        b = load("bridge")
        net = b["net"]
        rows = VGroup(
            label(r"Clarke's rule: \ build if the reported net values add up to zero or more", font_size=24,
                  color=MECH),
            label(r"and charge anyone whose report changes the decision \ the net loss it causes the others",
                  font_size=24, color=MONEY),
            label(rf"without Ana, \ the others add up to {sum(net) - net[0]:+.0f}: \ no bridge", font_size=24),
            label(rf"so Ana is pivotal, \ and pays {b['tax'][0]:.0f} shells on top of her share", font_size=25,
                  color=MONEY),
            label(r"nobody else changes the decision: \ they pay nothing extra", font_size=23, color=GREY_A),
            label(r"each person's payoff is now everyone's net value: \ the truth is the best report, \ whatever "
                  r"others say", font_size=23, color=STABLE),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Vickrey, J. Finance (1961); \ Clarke, Public Choice 11 (1971); \ Groves, Econometrica "
                            r"41(4) (1973)", corner=DR, font_size=12)
        with self.voiceover(
            "Edward Clarke in 1971 and Theodore Groves in 1973 found a way to make the truth pay, extending "
            "Vickrey's idea. <bookmark mark='a'/> Ask each person what the bridge is worth, and build it if the "
            "reported net values add up to zero or more. <bookmark mark='b'/> Then charge anyone whose report "
            "changes the decision the net loss that change causes everyone else. <bookmark mark='c'/> Without Ana, "
            "the others' net values add up to minus fifteen, and no bridge would be built. <bookmark mark='d'/> So "
            "Ana is pivotal, and pays fifteen shells on top of her share: the harm her wish does to the others. "
            "<bookmark mark='e'/> Nobody else changes the decision, so nobody else pays anything extra. "
            "<bookmark mark='f'/> With this charge, each person's payoff moves one for one with everyone's total net "
            "value, so the best report is the truth, whatever the others say. It is Vickrey's second-price auction "
            "again: pay for the harm you do."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def flaws(self):
        b = load("bridge")
        rows = point_cards([
            (r"the budget", rf"Ana's {b['tax'][0]:.0f} shells can't go back \\ to the islanders, \ or truth fails",
             MONEY),
            (r"collusion", r"two who lie together \\ can beat the rule", REJECT),
            (r"tiny revenue", r"in some auctions, \\ near nothing at all", HELD),
            (r"complexity", r"everyone must report \\ every value", GREY_A),
        ], width=12.0, cols=2, font_size=23).move_to(DOWN * 0.3)
        head = label(r"lovely, \ but rarely used", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Green and Laffont, Econometrica 45(2) (1977); \ Ausubel and Milgrom, in \emph{Combinatorial "
                            r"Auctions} (2006)", corner=DR, font_size=12)
        with self.voiceover(
            "The rule is beautiful, and rarely used. Lawrence Ausubel and Paul Milgrom called it lovely but lonely. "
            "<bookmark mark='a'/> The fifteen shells Ana pays cannot be handed back to the islanders, because if "
            "they expected a refund, their reports would change it, and the truth would no longer be best. The "
            "money must be thrown away, or given to someone outside. Jerry Green and Jean-Jacques Laffont proved in "
            "1977 that no rule of this kind can always balance its books. Two islanders who lie together can beat it, and in some "
            "auctions it raises next to nothing. <bookmark mark='b'/> And it asks everyone to report every value, "
            "which in a market with many goods is a great deal to ask."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows.cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[1:3]], lag_ratio=0.8), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[3], shift=UP * 0.1))
        self.clear_scene()
