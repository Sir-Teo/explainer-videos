from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

MONEY = "#F2C14E"
NECTAR = "#7BD88F"


class Bees(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The fable of the bees, \ investigated", r"Did the market for pollination exist, \ and what "
             r"did it price?", "Chapter five. The fable of the bees, investigated.",
             lit={1952: r"Meade's fable", 1973: r"Cheung's investigation"}, scale=("firm", "market"),
             horizon=("a season",))
        self.rents()
        self.lesson()

    def rents(self):
        b = load("bees")
        po, ho = b["pollination"], b["honey"]
        ax = plane([0, 3], [0, 11], center=LEFT * 2.9 + DOWN * 0.4, x_length=5.6, y_length=4.6, xticks=[],
                   yticks=[0, 2, 4, 6, 8, 10], xlabel="", ylabel=r"rent per hive, \ dollars of 1971", font_size=16,
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        uy = a.y_axis.get_unit_size()
        w = 0.7 * a.x_axis.get_unit_size()
        bars = VGroup()
        for x0, d, name in ((0.9, po, r"spring: \\ fruit pollination"), (2.1, ho, r"summer: \\ honey crops")):
            m = Rectangle(width=w, height=d["money"] * uy, stroke_width=0, fill_color=MONEY, fill_opacity=0.85
                          ).move_to(a.c2p(x0, 0), aligned_edge=DOWN)
            n_ = Rectangle(width=w, height=d["nectar"] * uy, stroke_width=0, fill_color=NECTAR, fill_opacity=0.85
                           ).next_to(m, UP, buff=0)
            tot = label(rf"\${d['total']:.2f}", font_size=20, color=WHITE).next_to(n_, UP, buff=0.1)
            ml = label(rf"\${d['money']:.2f}", font_size=16, color=BACKGROUND).move_to(m) if d["money"] > 1.5 else \
                label(rf"\${d['money']:.2f}", font_size=16, color=MONEY).next_to(m, RIGHT, buff=0.1)
            nl = label(rf"\${d['nectar']:.2f}", font_size=16, color=BACKGROUND).move_to(n_) if d["nectar"] > 1.5 else \
                label(rf"\${d['nectar']:.2f}", font_size=16, color=NECTAR).next_to(n_, RIGHT, buff=0.1)
            nm = label(name, font_size=16, color=GREY_A).next_to(a.c2p(x0, 0), DOWN, buff=0.2)
            bars.add(VGroup(m, n_, tot, ml, nl, nm))
        key = VGroup(
            VGroup(Square(0.2, stroke_width=0, fill_color=MONEY, fill_opacity=0.85),
                   label(r"paid in money", font_size=15, color=MONEY)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.2, stroke_width=0, fill_color=NECTAR, fill_opacity=0.85),
                   label(r"paid in nectar: \ the honey the bees bring home", font_size=15, color=NECTAR)
                   ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        side = VGroup(
            label(r"a hive earns its keep two ways: \\ a fee in money, \ and the honey", font_size=21),
            label(r"in spring the orchards pay: \\ fruit blossom gives little honey", font_size=21, color=MONEY),
            label(r"in summer the honey pays, \\ and the money fee shrinks, \\ or turns into a rent the beekeeper pays",
                  font_size=21, color=NECTAR),
            label(rf"across the spring farms, \ money and nectar \\ move against each other: \ correlation {b['corr']:.2f}",
                  font_size=21, color=E.ACCENT),
            label(r"the total stays near \$8 to \$10: \\ a hive earns about the same wherever it goes",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Cheung, JLE 16(1) (1973), pp.\ 25--27", corner=DR, font_size=13)
        with self.voiceover(
            "Here is what Cheung found. <bookmark mark='a'/> A hive earns its keep in two ways: a fee paid in money, "
            "and the honey its bees bring home from the crop. <bookmark mark='b'/> In late spring, the orchards' "
            "blossom gives little honey, so the orchards pay: on average nine dollars and two cents a hive, with "
            "sixty-four cents' worth of nectar on top, nine sixty-five in all. <bookmark mark='c'/> In summer, on "
            "clover, alfalfa and mint, the honey pays: six seventy-seven in nectar, and only a dollar thirty in "
            "money. For some honey crops the fee turns negative, and the beekeeper pays the farmer a rent. "
            "<bookmark mark='d'/> Across the spring farms Cheung recorded, the money fee and the nectar moved "
            "against each other almost perfectly, with a correlation of minus nought point nine seven. "
            "<bookmark mark='e'/> The total stays at eight to ten dollars a hive, wherever the hive goes. That is "
            "exactly what a working market would do: the price of the bees' service adjusts for the value of what "
            "they take."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(key))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(bars[0][k], DOWN) for k in (0, 1)], FadeIn(bars[0][2:]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(bars[1][k], DOWN) for k in (0, 1)], FadeIn(bars[1][2:]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(bars[0][2]), Indicate(bars[1][2]))
        self.clear_scene()

    def lesson(self):
        rows = VGroup(
            label(r"Meade's example failed as an example: \ the spillover had a price", font_size=25, color=E.ACCENT),
            label(r"a few hundred farmers and beekeepers, \ crops that stay put, \ hives that can be counted",
                  font_size=23),
            label(r"when contracts are cheap, \ Coase is right: \ people bargain the spillover away", font_size=24,
                  color=GOOD),
            label(r"the same market still runs: \ its largest part now in California's almond groves", font_size=22,
                  color=GREY_A),
            label(r"but the lesson is about bargaining costs, \ not about bees: \ smoke over a city has no Cheung",
                  font_size=23, color=SMOKE),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Cheung, JLE 16(1) (1973)", corner=DR, font_size=13)
        with self.voiceover(
            "So Meade's example failed as an example. <bookmark mark='a'/> The spillover Meade chose had a price. "
            "<bookmark mark='b'/> It is not hard to see why: a few hundred farmers and beekeepers, crops that stay "
            "put, hives that can be counted and moved by truck. <bookmark mark='c'/> When contracts are cheap to "
            "write, Coase is right, and people bargain the spillover away. <bookmark mark='d'/> The market Cheung "
            "found is still running; the largest part of it now is in California's almond groves. "
            "<bookmark mark='e'/> But the lesson is about the cost of bargaining, not about bees. Smoke spread over "
            "a city, or sulphur over a continent, has no Cheung to find its contracts, because there are none."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
