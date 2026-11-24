from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Bottom(VoiceoverScene):
    def construct(self):
        card(self, 4, "Bottom-up: units times price", "Can you build a market from the gallons and the prices?",
             "Chapter four. Bottom-up: units times price.", lit=("unit", "dollar"))
        self.units()
        self.companies()

    def units(self):
        W = R["water"]
        tank = VGroup(*[draw.bottle(0.45, color=WATER) for _ in range(40)]).arrange_in_grid(rows=4, cols=10,
                                                                                         buff=(0.04, 0.06))
        tank.move_to([-4.2, 1.4, 0])
        tl = VGroup(tx(f"{W['gallons']:.1f} billion gallons", 24, WATER, bold=True),
                    tx(f"{W['pop']:.0f}m people × {W['percap']} gallons, 2023", 16, GREY_B)).arrange(
            DOWN, buff=0.05).next_to(tank, DOWN, buff=0.2)
        u = 1.6
        base = -2.7
        steps = [("leaving the factory", W["factory_per_gal"], FACTORY, "the Census's $7.2bn ÷ the gallons"),
                 ("at the till", W["retail_per_gal"], RETAIL, "Primo's $25bn ÷ the gallons")]
        bars = VGroup()
        for k, (name, v, col, how) in enumerate(steps):
            b = Rectangle(width=1.3, height=v * u, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                [1.2 + 2.6 * k, base, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"${v:.2f}", 28, col, bold=True).next_to(b, UP, buff=0.08),
                            tx(name, 17, GREY_A).next_to(b, DOWN, buff=0.12), tx(how, 13, GREY_C).next_to(b, DOWN, buff=0.45)))
        pt = tx("what a gallon is worth", 20, WHITE).move_to([2.5, 1.6, 0])
        chain = VGroup(draw.truck(0.9, color=GREY_B), draw.shop(0.7, color=RETAIL)).arrange(RIGHT, buff=0.15).move_to(
            [2.5, 0.6, 0])
        mult = tx(f"× {W['ratio']:.1f}", 34, GOLD, bold=True).move_to([5.9, -0.6, 0])
        tag = estimate_tag("prices per gallon implied by dividing each source's dollars by the tracker's gallons", corner=DR,
                           size=13)
        with self.voiceover(
            "The bottom-up way builds a market out of units and prices, as you did with the shelf. "
            "<bookmark mark='a'/> The units are the easier half. Three hundred and thirty-seven million people at "
            f"forty-six gallons each is about {W['gallons']:.1f} billion gallons a year. <bookmark mark='b'/> The "
            "price is the hard half, because a gallon has a different price at every step of the chain. Divide the "
            f"Census's dollars by those gallons and a gallon leaving the factory is worth about "
            f"{100 * W['factory_per_gal']:.0f} cents. <bookmark mark='c'/> Divide Primo's retail figure by the same "
            f"gallons and a gallon at the till is worth about {W['retail_per_gal']:.2f}. <bookmark mark='d'/> That "
            f"is the gap between the two published numbers: roughly {W['ratio']:.1f} times. Some of it is the truck "
            "and the shop. Some is water the Census files elsewhere, from soft-drink plants and from abroad. The "
            "bottom-up method makes you choose the price, and the price you choose decides which market you have "
            "measured."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(b_, shift=DOWN * 0.1) for b_ in tank], lag_ratio=0.02),
                      run_time=1.8)
            vo.wait_until("a")
            self.play(FadeIn(tl, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(pt), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("c")
            self.play(FadeIn(chain, shift=RIGHT * 0.3), GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]))
            vo.wait_until("d")
            self.play(FadeIn(mult, scale=1.3))
        self.clear_scene()

    def companies(self):
        W = R["water"]
        u = 0.16
        base = -2.5
        mk = Rectangle(width=2.0, height=W["primo"] * u, stroke_color=RETAIL, stroke_width=3, fill_opacity=0.08).move_to(
            [-2.8, base, 0], aligned_edge=DOWN)
        pr = Rectangle(width=2.0, height=W["primo_rev"] * u, stroke_width=0, fill_color=UNITS, fill_opacity=0.9).move_to(
            [-2.8, base, 0], aligned_edge=DOWN)
        mk_t = tx(f"the retail market, ${W['primo']:.0f}bn (2023)", 17, RETAIL).next_to(mk, UP, buff=0.1)
        pr_t = VGroup(tx("Primo Brands' own revenue", 17, UNITS, bold=True),
                      tx(f"${W['primo_rev']:.2f}bn (2024)", 17, UNITS)).arrange(DOWN, buff=0.04).next_to(pr, RIGHT, buff=0.3)
        giants = VGroup(*[VGroup(draw.factory(0.9, color=c), tx("water inside,", 14, GREY_B), tx("not broken out", 14, GREY_B)
                                 ).arrange(DOWN, buff=0.06) for c in ("#E8554E", "#3B7DD8", "#7BD88F")]).arrange(
            RIGHT, buff=0.5).move_to([3.4, 0.4, 0])
        gt = tx("the soft-drink giants' reports", 18, GREY_A).next_to(giants, UP, buff=0.25)
        src = source("Primo Brands, Forms 10-K (SEC company facts)", size=13)
        with self.voiceover(
            "The other bottom-up way is to add up the companies. <bookmark mark='a'/> The largest seller in American "
            f"shops, Primo Brands, reported revenue of {W['primo_rev']:.1f} billion dollars in 2024, at the prices it "
            "charges shops and offices, including home delivery, filters and coffee. <bookmark mark='b'/> But the "
            "other big sellers of bottled water are soft-drink companies, and their reports do not say how much of "
            "their revenue is water. Adding up companies works when they report the market you want, and that is "
            "rarer than it sounds. <bookmark mark='c'/> So the analyst ends up with a sum of the companies that do "
            "report, and a remainder that is a guess."
        ) as vo:
            self.play(FadeIn(src), Create(mk), FadeIn(mk_t))
            vo.wait_until("a")
            self.play(GrowFromEdge(pr, DOWN), FadeIn(pr_t))
            vo.wait_until("b")
            self.play(FadeIn(gt), LaggedStart(*[FadeIn(g_, shift=UP * 0.2) for g_ in giants], lag_ratio=0.25))
            vo.wait_until("c")
            q = tx("?", 60, GREY_B, bold=True).move_to(mk.get_center() + UP * 0.6)
            self.play(FadeIn(q, scale=1.4))
        self.clear_scene()
