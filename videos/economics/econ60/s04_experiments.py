from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Experiments(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Price experiments", r"An A/B test says the discount works. \ Does it?",
             "Chapter three. Price experiments.", lit={2014: r"Blake and Coey"}, scale=("person", "market"),
             horizon=("a day", "a year"))
        self.design()
        self.interference()

    def design(self):
        rows = VGroup(
            label(r"split buyers at random: \ half see the old price, \ half a 10\% discount", font_size=23,
                  color=TEST),
            label(r"compare how often each half books: \ the difference is the effect", font_size=23, color=WHITE),
            label(r"randomization removes every other difference between the halves", font_size=21,
                  color=GREY_A),
            label(r"but it assumes one buyer's price does not change another's outcome", font_size=23,
                  color=COST),
            label(r"in a market with scarce rooms, \ seats or listings, \ it does", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"the A/B test", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Firms that sell online can do better than ask: they can experiment. <bookmark mark='a'/> Split buyers "
            "at random; show half the old price and half a ten percent discount. <bookmark mark='b'/> Compare how "
            "often each half buys: the difference is the effect of the discount. <bookmark mark='c'/> Because the "
            "split is random, the halves differ in nothing else, which is why the method is trusted. <bookmark "
            "mark='d'/> But it rests on an assumption economists call no interference: that one buyer's price does "
            "not change what happens to another buyer. <bookmark mark='e'/> In a market where something is scarce, "
            "rooms, seats, listings, drivers, that assumption fails."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()

    def interference(self):
        X = load("experiment")
        rooms = VGroup(*[Square(side_length=0.28, stroke_color=GREY_C, stroke_width=1.2, fill_color=GREY_E,
                                fill_opacity=0.6) for _ in range(27)]).arrange_in_grid(3, 9, buff=0.08)
        rooms.to_edge(LEFT, buff=0.7).shift(UP * 1.7)
        rl = label(r"a city's rooms \ (one square = 10)", font_size=16, color=GREY_B).next_to(rooms, UP, buff=0.12)
        fill = [TEST if k % 5 in (0, 2, 4) else AIR for k in range(27)]
        ax = plane([-0.6, 2.6], [0, 0.11], center=LEFT * 3.0 + DOWN * 1.6, x_length=5.6, y_length=3.0, xticks=[],
                   yticks=[0, 0.05, 0.10], ylabel=r"rise in the booking rate", yfmt=lambda v: f"{100 * v:.0f}pp",
                   font_size=13)
        vals = [X["naive"], X["global"], X["cluster"]]
        cols = [COST, OPT, LEIS]
        b = bars(ax, range(3), vals, cols, width=0.5)
        labs = VGroup(*[label(t, font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.1) for k, (t, c) in
                        enumerate(((r"the A/B test", COST), (r"the truth: \\ discount for all", OPT),
                                   (r"a test \\ by city", LEIS)))])
        vl = VGroup(*[label(f"{100 * v:.1f}", font_size=15, color=c).next_to(x, UP, buff=0.05)
                      for v, c, x in zip(vals, cols, b)])
        side = VGroup(
            label(rf"{X['markets']} cities, \ {X['rooms']} rooms and {X['buyers']} buyers each", font_size=19,
                  color=GREY_A),
            label(r"pink buyers have the discount; \ blue do not", font_size=19, color=TEST),
            label(r"when rooms run out, \ every room a pink buyer takes \\ is a room a blue buyer cannot", font_size=19,
                  color=WHITE),
            label(rf"the A/B test: \ +{100 * X['naive']:.1f} points; \ the truth: \ +{100 * X['global']:.1f}",
                  font_size=21, color=COST),
            label(r"randomize whole cities instead, \ and the comparison is clean", font_size=20, color=LEIS),
            label(r"eBay's email test: \ the naive estimate about twice the effect \ (Blake and Coey)", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ hotel rooms; \ agora.revenue.interference, \ 200 runs", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Here is the Island's hotel test. <bookmark mark='a'/> In each of forty cities there are "
            f"{X['rooms']} rooms and {X['buyers']} buyers. <bookmark mark='b'/> Half the buyers, in pink, are shown "
            "a ten percent discount. <bookmark mark='c'/> Demand is close to the number of rooms, so as they fill, "
            "every room a discounted buyer takes is a room an undiscounted buyer can no longer book. The control "
            "group is hurt by the treatment. <bookmark mark='d'/> The A/B test compares the two halves and finds "
            f"the discount raises the booking rate by {100 * X['naive']:.1f} points. Giving the discount to everyone "
            f"would raise it by only {100 * X['global']:.1f}: half the measured effect was buyers taking rooms from "
            "each other. <bookmark mark='e'/> The cure is to randomize whole markets, here cities, so treated and "
            f"control buyers never compete; that test finds {100 * X['cluster']:.1f}, at the cost of a noisier "
            "estimate from fewer units. <bookmark mark='f'/> Thomas Blake and Dominic Coey found the same pattern "
            "on eBay: a naive comparison exaggerated an email campaign's effect by about a factor of two. An "
            "elasticity from an A/B test answers the question of one buyer facing a different price, while "
            "everyone else's stays the same; a firm changing its price for everyone needs the other one."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rooms), FadeIn(rl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[r.animate.set_fill(c, opacity=0.9) for r, c in zip(rooms, fill)],
                                  lag_ratio=0.05), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(ax), FadeIn(labs), GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(vl[0]),
                      FadeIn(vl[1]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(vl[2]), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
