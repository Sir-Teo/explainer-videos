from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Gainers(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Who gains and who loses", r"Where does the money go, \ and who pays?",
             "Chapter ten. Who gains, and who loses.", lit={1971: r"Rawls", 2020: r"Hendren"},
             scale=("household", "nation"), horizon=("a year",))
        self.deciles()
        self.losers()
        self.is_ought()

    def deciles(self):
        D = load("deciles")
        g = D["mean_gain"]
        ax = plane([0, 10], [0, 6000], center=LEFT * 1.6 + DOWN * 0.35, x_length=8.6, y_length=4.6, xticks=[],
                   yticks=[0, 2000, 4000, 6000], ylabel=r"average gain a year, \ \$",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=14)
        bars = VGroup()
        for i, v in enumerate(g):
            p0, p1 = ax.ax.c2p(i + 0.15, 0), ax.ax.c2p(i + 0.85, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0,
                          fill_color=interpolate_color(ManimColor(CHILD), ManimColor(OLD), i / 9), fill_opacity=0.9)
            r.move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(f"{v:,.0f}".replace(",", "{,}"), font_size=13, color=WHITE).next_to(r, UP,
                                                                                                    buff=0.05),
                            label(str(i + 1), font_size=15, color=GREY_A).next_to(ax.ax.c2p(i + 0.5, 0), DOWN,
                                                                                buff=0.12)))
        xl = label(r"tenths of families, \ poorest to richest, \ under the old credit", font_size=15,
                   color=GREY_A).next_to(ax, DOWN, buff=0.5)
        side = VGroup(
            label(rf"poorest tenth: \\ +\${g[0]:,.0f}, \ more than \\ their whole income \\ before".replace(",", "{,}"),
                  font_size=17, color=CHILD),
            label(r"middle: \ about \\ \$1,400--1,800".replace(",", "{,}"), font_size=17, color=WHITE),
            label(rf"richest tenth: \\ +\${g[-1]:,.0f}, \ phased out".replace(",", "{,}"), font_size=17, color=OLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Who gains? Rank the Island's families by their income under the old credit, and cut them into ten "
            "equal groups. <bookmark mark='a'/> The poorest tenth gains most: "
            f"{g[0]:,.0f} dollars a year on average, more than the whole of their income before, because many of "
            "them had little or no earnings and so little or none of the old credit. <bookmark mark='b'/> The "
            "gain falls through the second and third tenths, as the old credit phases in, <bookmark mark='c'/> and "
            "in the middle it settles at fourteen to eighteen hundred dollars, the difference between the old and "
            "new amounts per child. <bookmark mark='d'/> The richest tenth gains only "
            f"{g[-1]:,.0f} dollars, because the extra is phased out above seventy-five thousand for a single "
            "parent and a hundred and fifty thousand for a couple."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars[1:3]], *[FadeIn(b[1:]) for b in bars[1:3]])
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars[3:9]], lag_ratio=0.2),
                      *[FadeIn(b[1:]) for b in bars[3:9]], FadeIn(side[1]), run_time=1.8)
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[9][0], DOWN), FadeIn(bars[9][1:]), FadeIn(side[2]))
        self.clear_scene()

    def losers(self):
        D = load("deciles")
        I = load("island")
        cards = point_cards([
            (r"families with less income", rf"{100 * D['losers']:.1f}\%: \ the parents who stop working; \ "
                                           r"by their own lights not worse off, \ since they chose it", WORK),
            (r"their children", r"did not choose: \ some fall below half the line \ (chapter eight)", POOR),
            (r"the taxpayers", r"whoever pays: \ top earners under a surtax, \ later taxpayers if it is "
                               r"borrowed", BUDGET),
            (r"families without children", r"nothing directly; \ they pay their share of the tax", GREY_A),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"and who loses", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "And who loses? <bookmark mark='a'/> On the Island, "
            f"{100 * D['losers']:.1f} percent of families end up with less income: the families of the "
            f"{I['exits']:.0f} parents who stop working. By their own lights they are not worse off, since they "
            "chose to stop, and nothing forced them. <bookmark mark='b'/> But their children did not choose, and "
            "some of them fall below half the line, as chapter eight showed. A memo that cares about children "
            "cannot simply defer to the parents' choice. <bookmark mark='c'/> The taxpayers lose whatever they "
            "pay: top earners under a surtax, or later taxpayers if the money is borrowed. <bookmark mark='d'/> "
            "And families without children gain nothing directly, and pay their share."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def is_ought(self):
        I = load("island")
        card_ = is_ought_card(
            rf"child poverty falls by about a fifth \ ({100 * I['fall']:.0f}\% on the Island); \ the poorest gain "
            r"most; \ a few parents stop working; \ deep poverty may rise if many do",
            r"pay the allowance, \ pay it with a work requirement, \ or spend the money another way",
            r"how much a dollar to a poor child should count against a dollar to a taxpayer, \ and whether support "
            r"for children should depend on what their parents do",
            width=12.0, font_size=23).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here the memo reaches the step from is to ought. <bookmark mark='a'/> What is: child poverty falls "
            "by about a fifth; the poorest families gain the most; a few parents stop working; and if many did, "
            "deep poverty could rise. <bookmark mark='b'/> What the step needs: a judgment about how much a "
            "dollar to a poor child should count against a dollar to the person who pays for it, and whether help "
            "for children should depend on what their parents do. People who agree on every number in this film "
            "can disagree here, and neither side is making an error of economics. <bookmark mark='c'/> And what "
            "follows: pay the allowance, pay it with a work requirement, or spend the money another way."
        ) as vo:
            self.play(FadeIn(card_.card), FadeIn(card_.is_row))
            vo.wait_until("b")
            self.play(FadeIn(card_.judgment), FadeIn(card_[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card_.ought), FadeIn(card_[1][3]))
        self.clear_scene()
