from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

NEWTON = "#7BD88F"
AUCT = "#F2A65A"


class Compute(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Computing an equilibrium: \ the Island cleared at once", r"How do economists actually find "
             r"the prices of a whole economy?", "Chapter nine. Computing an equilibrium: the Island cleared at once.",
             scale=("market", "nation"))
        self.island()
        self.race()

    def island(self):
        i = load("island")
        goods = i["goods"]
        cols = (FISH, COCO, TIMBER, "#C9A0FF", "#E8E8E8")
        bars = VGroup()
        for k, (g, c, q) in enumerate(zip(goods, cols, i["total"])):
            name = label(g, font_size=22, color=c)
            bar = Rectangle(width=0.3 * q, height=0.32, stroke_width=0, fill_color=c, fill_opacity=0.8)
            num = label(f"{q:.1f}", font_size=19, color=GREY_A)
            bars.add(VGroup(name, bar, num))
        for k, row in enumerate(bars):
            y = -0.45 * k
            row[0].move_to([0, y, 0], aligned_edge=RIGHT)
            row[1].move_to([0.25, y, 0], aligned_edge=LEFT)
            row[2].next_to(row[1], RIGHT, buff=0.15)
        people = VGroup(*[islander(k, 0.55) for k in ("crusoe", "friday", "ana", "bo", "chidi", "dara") * 2]
                        ).arrange_in_grid(2, 6, buff=0.25)
        left = VGroup(people, label(r"12 islanders, \ each owning two goods", font_size=21, color=GREY_A),
                      label(r"what the island has", font_size=21, color=GREY_A), bars).arrange(DOWN, buff=0.3)
        left.to_edge(LEFT, buff=0.7)
        side = VGroup(
            label(r"five goods, \ twelve islanders", font_size=24),
            label(rf"CES tastes, \ elasticities {min(i['sigmas']):.1f} to {max(i['sigmas']):.1f}", font_size=22),
            label(r"four relative prices to find, \\ four markets to clear \ (Walras clears the fifth)", font_size=22,
                  color=E.ACCENT),
            label(r"prices, \ fish = 1:", font_size=22, color=CC),
            label(r" \quad ".join(rf"{g} {p:.2f}" for g, p in zip(goods[1:], i["p"][1:])), font_size=21, color=CC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now the whole island. <bookmark mark='a'/> Twelve islanders and five goods: fish, coconuts, timber, "
            "cloth and salt. Each islander owns two of them and has tastes of the CES kind from Part six, some "
            "finding goods easy to substitute, some hard. <bookmark mark='b'/> With fish as the unit of account "
            "there are four relative prices to find and four markets to clear; Walras's law clears the fifth. "
            "<bookmark mark='c'/> Here is the answer: a coconut costs nought point four eight fish, timber "
            "nought point seven one, cloth nought point four three, and salt nought point eight five. How do we "
            "get it?"
        ) as vo:
            self.play(FadeIn(people), FadeIn(left[1]), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(left[2]), FadeIn(bars), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def race(self):
        i = load("island")
        nw = np.log10(np.maximum(np.array(i["newton"]), 1e-16))
        au = np.log10(np.maximum(np.array(i["auctioneer_errs"]), 1e-16))
        step = max(1, (i["auctioneer_steps"] + 1) // len(au))
        ax = plane([0, 250], [-14, 1], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.0, y_length=5.0,
                   xticks=[0, 50, 100, 150, 200, 250], yticks=[-12, -8, -4, 0], xlabel=r"steps",
                   ylabel=r"largest excess demand", font_size=17, yfmt=lambda v: rf"10^{{{v:.0f}}}")
        a = ax.ax
        np_ = VMobject(stroke_color=NEWTON, stroke_width=4).set_points_as_corners(
            [a.c2p(k, v) for k, v in enumerate(nw)])
        nd = VGroup(*[Dot(a.c2p(k, v), radius=0.06, color=NEWTON) for k, v in enumerate(nw)])
        ap = VMobject(stroke_color=AUCT, stroke_width=3).set_points_as_corners(
            [a.c2p(k * step, v) for k, v in enumerate(au)])
        side = VGroup(
            label(r"the auctioneer: \ small steps toward excess demand", font_size=22, color=AUCT),
            label(rf"{i['auctioneer_steps']} steps to within a millionth", font_size=22, color=AUCT),
            label(r"Newton's method: \ use how excess demand \\ changes with every price, \ and jump", font_size=22,
                  color=NEWTON),
            label(rf"{i['newton_iterations']} steps to within $10^{{-13}}$: \\ near the answer the error squares "
                  r"each step",
                  font_size=22, color=NEWTON),
            label(r"fast, \ but it can fail from a bad start; \\ Scarf's walk always arrives", font_size=21,
                  color=GREY_A),
            label(r"models with thousands of markets \\ are solved by refined Newton methods", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Two ways, raced. <bookmark mark='a'/> The auctioneer takes small steps, each price moved a little "
            "toward its excess demand. On the island it overshoots at first, then settles: <bookmark mark='b'/> "
            "two hundred and thirty-eight steps before every market is within a millionth of clearing. "
            "<bookmark mark='c'/> Newton's method uses more information. At each step it measures how every "
            "excess demand responds to every price, and jumps to where the straight-line approximation says they "
            "all vanish. <bookmark mark='d'/> Six steps, and the error goes from about six to ten to the minus "
            "thirteen, roughly squaring at the end. <bookmark mark='e'/> Newton's method can fail if it starts "
            "badly; Scarf's walk always arrives, but slowly. <bookmark mark='f'/> The models economists use to "
            "study trade agreements and taxes have thousands of markets, and they are solved by refinements of "
            "Newton's method, with Scarf's guarantee in the background."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ap), FadeIn(side[0]), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(np_), LaggedStart(*[FadeIn(d_) for d_ in nd], lag_ratio=0.3), FadeIn(side[3]),
                      run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
