from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403

# the game's shelf prices: illustrative, as a shopper might see them (not a statistic)
PACK_PRICE, PACK_BOTTLES, BOTTLE_L = 6.00, 24, 0.5
JUG_PRICE = 1.50
L_PER_GAL = 3.785


class Guess(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: size a market", "How much do Americans spend on bottled water in a year?",
             "Chapter one. Run it: size a market.", lit=("unit", "dollar"))
        W = R["water"]
        facts = [
            (draw.crowd(6, 0.38, color=STONE, cols=6), f"{W['pop']:.0f} million Americans (2023)", "Census Bureau"),
            (draw.bottle(0.8, color=WATER), f"{W['percap']:.0f} gallons of bottled water each, a year", "Beverage Marketing"),
            (VGroup(*[draw.bottle(0.4, color=WATER) for _ in range(6)]).arrange(RIGHT, buff=0.03),
             f"about {100 * 0.71:.0f}% of it in single-serve bottles", "Beverage Marketing, 2024"),
            (VGroup(*[draw.bottle(0.35, color=WATER) for _ in range(8)]).arrange_in_grid(rows=2, cols=4, buff=0.02),
             f"a 24-pack of half-litre bottles: ${PACK_PRICE:.2f}", "a shelf price, illustrative"),
            (draw.bottle(0.9, color="#9AD0F5", water=0.9), f"a gallon jug: ${JUG_PRICE:.2f}", "a shelf price, illustrative"),
            (tx("1 gallon = 3.785 litres", 18, GREY_A), "and the rest: jugs, delivery, sparkling, imports", ""),
        ]
        cards = VGroup()
        for pic, line, src_ in facts:
            pic.scale_to_fit_height(min(pic.height, 0.6))
            t_ = VGroup(tx(line, 20, WHITE), tx(src_, 14, GREY_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            cards.add(VGroup(pic, t_).arrange(RIGHT, buff=0.3))
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.8, 0.5), cell_alignment=LEFT).move_to([0, 0.6, 0])
        q = tx("Your estimate: Americans' spending on bottled water, a year?", 24, GUESS, bold=True).to_edge(DOWN, buff=0.9)
        tag = estimate_tag("the two shelf prices are illustrative", corner=DR, size=14)
        with self.voiceover(
            "Play it yourself. How much do Americans spend on bottled water in a year? You have six facts. "
            f"<bookmark mark='a'/> There are about {W['pop']:.0f} million Americans. <bookmark mark='b'/> According to "
            f"the Beverage Marketing Corporation, which tracks the industry, each drank about {W['percap']:.0f} gallons "
            "of bottled water in 2023. <bookmark mark='c'/> About seven tenths of it comes in single-serve bottles. "
            f"<bookmark mark='d'/> A supermarket sells a pack of twenty-four half-litre bottles for, say, six dollars. "
            f"<bookmark mark='e'/> A gallon jug costs, say, a dollar fifty. <bookmark mark='f'/> And the rest is jugs, "
            "home delivery, sparkling water and imports. <bookmark mark='g'/> Pause, and make your estimate. Write it "
            "down. Then we will see what three published sources say, and why they disagree with each other."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(q, shift=UP * 0.1))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k][0], scale=0.8), FadeIn(cards[k][1], shift=RIGHT * 0.1), run_time=0.8)
            vo.wait_until("g")
            self.play(FadeIn(q, shift=UP * 0.1))
            self.play(Indicate(q, color=WHITE))
        self.clear_scene()
        self.work()

    def work(self):
        W = R["water"]
        gal = W["gallons"]
        single = 0.71 * gal
        rest = gal - single
        per_gal_pack = PACK_PRICE / (PACK_BOTTLES * BOTTLE_L / L_PER_GAL)
        a, b = single * per_gal_pack, rest * JUG_PRICE
        lines = VGroup(
            MathTex(rf"{W['pop']:.0f}\text{{m people}} \times {W['percap']:.1f}\text{{ gal}} = "
                    rf"{gal:.1f}\text{{bn gallons}}", font_size=34),
            MathTex(rf"\text{{a pack: }} \frac{{\${PACK_PRICE:.2f}}}{{24 \times 0.5\,\text{{L}}}} = "
                    rf"\${per_gal_pack:.2f}\text{{ a gallon}}", font_size=34),
            MathTex(rf"{single:.1f}\text{{bn gal}} \times \${per_gal_pack:.2f} = \${a:.1f}\text{{bn}}", font_size=34,
                    color=RETAIL),
            MathTex(rf"{rest:.1f}\text{{bn gal}} \times \${JUG_PRICE:.2f} = \${b:.1f}\text{{bn}}", font_size=34,
                    color=RETAIL),
            MathTex(rf"\approx \${a + b:.0f}\text{{ billion a year}}", font_size=46, color=GUESS)).arrange(
            DOWN, buff=0.35).move_to([0.6, 0.0, 0])
        jug = VGroup(*[draw.bottle(0.55, color=WATER) for _ in range(10)]).arrange(DOWN, buff=-0.25).move_to([-5.6, 0, 0])
        tag = estimate_tag("one way to work it, with the illustrative shelf prices", corner=DR, size=14)
        with self.voiceover(
            "Here is one way to work it. <bookmark mark='a'/> Three hundred and thirty-seven million people times "
            f"forty-six gallons is about {gal:.1f} billion gallons a year. <bookmark mark='b'/> A pack of "
            "twenty-four half-litre bottles holds twelve litres, a little over three gallons, so at six dollars a "
            f"pack that water costs about {per_gal_pack:.2f} a gallon. <bookmark mark='c'/> Seven tenths of the "
            f"gallons at that price is about {a:.0f} billion dollars. <bookmark mark='d'/> The rest at a dollar fifty "
            f"is about {b:.0f} billion more. <bookmark mark='e'/> Call it {a + b:.0f} billion dollars a year. If your "
            "number was anywhere near that, you did what a market analyst does: units times price. Now meet the "
            "published numbers."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(j_, shift=DOWN * 0.2) for j_ in jug], lag_ratio=0.1))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(Write(lines[k]), run_time=1.2)
            self.play(Indicate(lines[4], color=WHITE))
        self.clear_scene()
