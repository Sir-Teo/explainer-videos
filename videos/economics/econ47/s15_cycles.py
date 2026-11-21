from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Cycles(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Political business cycles", r"Do governments time the economy to elections?",
             "Chapter thirteen. Political business cycles.", lit={1975: r"Nordhaus", 1985: r"Rogoff"},
             scale=("nation",), horizon=("a term",))
        self.cycle()
        self.delegation()

    def cycle(self):
        C = load("cycle")
        yrs = list(range(1, len(C["u"]) + 1))
        a1 = plane([0.5, 16.5], [3.9, 5.5], center=UP * 1.35 + LEFT * 1.6, x_length=8.4, y_length=2.4,
                   xticks=[4, 8, 12, 16], yticks=[4.0, 4.5, 5.0, 5.5], ylabel=r"unemployment, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        a2 = plane([0.5, 16.5], [-0.4, 1.0], center=DOWN * 1.9 + LEFT * 1.6, x_length=8.4, y_length=2.4,
                   xticks=[4, 8, 12, 16], yticks=[0, 0.5, 1.0], xlabel=r"year", ylabel=r"inflation, \ points",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        u = path(a1, yrs, C["u"], POL, 3.0, smooth=False)
        pi = path(a2, yrs, C["pi"], LOSS, 3.0, smooth=False)
        ud = DashedLine(a1.ax.c2p(0.5, 5.0), a1.ax.c2p(16.5, 5.0), color=AUDIT, stroke_width=2)
        pd = DashedLine(a2.ax.c2p(0.5, 0), a2.ax.c2p(16.5, 0), color=AUDIT, stroke_width=2)
        elect = VGroup(*[VGroup(vline(a1, e + 1, 3.9, 5.5, GREY_B), vline(a2, e + 1, -0.4, 1.0, GREY_B))
                         for e in C["elections"]])
        el = label(r"elections", font_size=14, color=GREY_B).next_to(a1.ax.c2p(4, 5.5), UP, buff=0.05)
        side = VGroup(
            label(r"voters remember \\ the last year best", font_size=18, color=VOTER),
            label(r"pink: \ unemployment \\ pushed down before \\ each election", font_size=18, color=POL),
            label(r"red: \ inflation that \\ follows, \ and ratchets up", font_size=18, color=LOSS),
            label(r"green, \ dashed: \\ delegated to a \\ central bank", font_size=18, color=AUDIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1975 William Nordhaus asked what a government facing short-sighted voters would do with Part "
            "twenty-eight's Phillips curve. <bookmark mark='a'/> Suppose voters judge a government mostly by the "
            "last year before an election. <bookmark mark='b'/> Then it pays to hold unemployment up early in the "
            "term, and push it down just before the vote: on the Island, the pink line dips before every "
            "election. <bookmark mark='c'/> The price comes after: pushing unemployment below its natural rate "
            "raises inflation, which expectations then carry forward, so it ratchets up term after term. "
            "<bookmark mark='d'/> A central bank that cannot be voted out, and that keeps unemployment at its "
            "natural rate, removes the cycle: the dashed lines. The evidence for crude Nordhaus cycles in rich "
            "democracies is mixed, partly because so many of them did exactly this, and handed monetary policy to "
            "independent central banks."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(tag), FadeIn(elect), FadeIn(el), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(u), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(pi), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(ud), Create(pd), FadeIn(side[3]))
        self.clear_scene()

    def delegation(self):
        cards = point_cards([
            (r"central banks", r"independent, \ with \\ a mandate: \ Rogoff's \\ conservative \\ banker, \ Part 28",
             AUDIT),
            (r"fiscal councils", r"independent forecasts \\ of the budget, \ such \\ as Britain's OBR \\ since 2010",
             VOTER),
            (r"rules", r"debt brakes, \\ deficit limits, \\ written into law", ELITE),
            (r"the cost", r"decisions taken \\ out of politics \\ answer less \\ to voters", HOLD),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"delegation as a remedy", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.CYCLES_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Delegation is political economy's most widely adopted remedy. <bookmark mark='a'/> Independent central "
            "banks, with a mandate and a governor who cares more about inflation than the government does: "
            "Kenneth Rogoff's conservative central banker, from Part twenty-eight. <bookmark mark='b'/> Fiscal "
            "councils, which publish independent forecasts of the budget, such as Britain's Office for Budget "
            "Responsibility, created in 2010. <bookmark mark='c'/> Fiscal rules, from deficit limits to debt "
            "brakes. <bookmark mark='d'/> The cost of delegation is accountability: decisions taken out of "
            "politics are also taken away from voters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
