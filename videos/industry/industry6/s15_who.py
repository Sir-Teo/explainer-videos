from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403

# a supply stack of ten producers (illustrative): capacity and cost per unit
STACK = [(12, 30), (10, 34), (8, 38), (9, 41), (7, 45), (8, 49), (6, 54), (7, 60), (5, 68), (6, 77)]


class Who(VoiceoverScene):
    def construct(self):
        card(self, 13, "Who wins a cycle", "If the cycle cannot be stopped, who comes out ahead?",
             "Chapter thirteen. Who wins a cycle.", lit=("change", "moat"))
        self.stack()
        self.others()

    def stack(self):
        x0, base, u, v = -5.6, -2.4, 0.13, 0.055
        price = ValueTracker(82.0)
        blocks = VGroup()
        x = x0
        for cap, cost in STACK:
            w = cap * u
            blocks.add(Rectangle(width=w, height=cost * v, stroke_width=1, stroke_color="#0E1117", fill_color=CAP,
                                 fill_opacity=0.85).move_to([x + w / 2, base + cost * v / 2, 0]))
            x += w
        floor = Line([x0, base, 0], [x + 0.2, base, 0], stroke_color=GREY_B, stroke_width=1.5)

        def recolor(g):
            p = price.get_value()
            for b_, (_, cost) in zip(g, STACK):
                b_.set_fill(BOOM if cost < p - 3 else (ORDER if cost < p else BUST), opacity=0.85)
        blocks.add_updater(recolor)
        pline = always_redraw(lambda: DashedLine([x0, base + price.get_value() * v, 0],
                                                 [x + 0.2, base + price.get_value() * v, 0], stroke_color=WHITE,
                                                 stroke_width=2.5))
        pnum = draw.number(lambda: price.get_value(), 0, prefix="price $", size=24, color=WHITE)
        pnum.add_updater(lambda g: g.next_to([x + 0.25, base + price.get_value() * v, 0], RIGHT, buff=0.1))
        xl = tx("producers, from lowest cost to highest; width = capacity", 16, GREY_B).next_to(floor, DOWN, buff=0.15)
        yl = tx("cost of one more unit", 16, GREY_B).move_to([x0 + 1.4, base + 4.6, 0])
        key = VGroup(tx("profitable", 16, BOOM, bold=True), tx("barely covering costs", 16, ORDER, bold=True),
                     tx("losing money on every unit", 16, BUST, bold=True)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.1).move_to([4.8, 2.4, 0])
        tag = estimate_tag("an illustrative industry of ten producers (Part 4's supply curve)", corner=DR, size=13)
        with self.voiceover(
            "Who wins a cycle? Go back to Part 4's supply curve: every producer in an industry, lined up from the "
            "lowest cost to the highest. <bookmark mark='a'/> In a boom, demand is so high that even the costliest "
            "plant is needed, and the price sits above all of them. Everyone makes money. <bookmark mark='b'/> "
            "Then the new capacity arrives and the price falls, to the cost of whichever plant is the last one "
            "needed. The costliest producers now lose money on every unit they make. <bookmark mark='c'/> They "
            "close, or are bought, or go bankrupt. <bookmark mark='d'/> The lowest-cost producer is still making "
            "money at the bottom. That is the first way to win a cycle: be the plant that is still needed when "
            "nobody else is."
        ) as vo:
            self.play(FadeIn(tag), Create(floor), FadeIn(xl), FadeIn(yl),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in blocks], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("a")
            self.add(pline, pnum)
            self.play(FadeIn(key))
            vo.wait_until("b")
            self.play(price.animate.set_value(47.0), run_time=3.0)
            vo.wait_until("c")
            self.play(*[blocks[i].animate.set_opacity(0.15) for i in range(6, 10)], run_time=1.4)
            vo.wait_until("d")
            self.play(Indicate(blocks[0], color=WHITE, scale_factor=1.08))
        blocks.clear_updaters()
        pnum.clear_updaters()
        self.clear_scene()

    def others(self):
        from videos.industry.industry3.s03_ledger import _bank
        cards = VGroup()
        specs = [(draw.ship(1.2), "Buy at the bottom",
                  "ships, plants and whole companies are cheapest when nobody wants them"),
                 (VGroup(_bank().scale(2.0), Cross(stroke_color=BUST, stroke_width=4).scale(0.25)), "Owe little",
                  "a company without debt can wait out the trough, and buy its rivals' plants"),
                 (draw.crane(1.0), "Be paid in advance",
                  "shipyards and toolmakers take orders and deposits in the boom, years before delivery"),
                 (VGroup(*[draw.coin(0.12) for _ in range(5)]).arrange(RIGHT, buff=0.02), "Spend against the crowd",
                  "building in a trough can pay best: costs are low, and so is the competition for workers")]
        for g, head, sub in specs:
            g.scale_to_fit_height(min(g.height, 0.8))
            txt = VGroup(tx(head, 24, WHITE, bold=True), tx(sub, 17, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            cards.add(VGroup(g, txt).arrange(RIGHT, buff=0.4))
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        head = tx("Other ways to come out ahead", 26, GOLD, bold=True).to_edge(UP, buff=0.5)
        with self.voiceover(
            "There are other ways. <bookmark mark='a'/> Buy at the bottom. In a trough, ships, plants and whole "
            "companies sell for a fraction of what they cost to build, because the people who own them need cash. "
            "<bookmark mark='b'/> Owe little. A company without much debt can wait out a bad year, and pick up its "
            "rivals' plants when they cannot. <bookmark mark='c'/> Be paid in advance. Shipyards and the makers of "
            "chip-making machines take orders and deposits in the boom, and deliver years later. Their own cycle "
            "comes, but later, and with a cushion. <bookmark mark='d'/> And spend against the crowd. The plant "
            "ordered in a trough is built cheaply, by contractors hungry for work, and arrives when the next "
            "shortage begins. It is the hardest of all, because in a trough every number on the page argues "
            "against it."
        ) as vo:
            self.play(FadeIn(head))
            for c_, m in zip(cards, "abcd"):
                vo.wait_until(m)
                self.play(FadeIn(c_[0], scale=0.8), FadeIn(c_[1], shift=RIGHT * 0.15))
        self.clear_scene()
