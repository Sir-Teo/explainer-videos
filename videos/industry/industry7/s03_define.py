from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Define(VoiceoverScene):
    def construct(self):
        card(self, 2, "Definition is most of it", "Why do two honest sources give the same market different sizes?",
             "Chapter two. Definition is most of it.", lit=("unit", "dollar"))
        self.two()
        self.levers()

    def two(self):
        W = R["water"]
        u = 0.15
        base = -2.6
        b1 = Rectangle(width=1.6, height=W["census"] * u, stroke_width=0, fill_color=FACTORY, fill_opacity=0.9).move_to(
            [-3.2, base, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.6, height=W["primo"] * u, stroke_width=0, fill_color=RETAIL, fill_opacity=0.9).move_to(
            [0.0, base, 0], aligned_edge=DOWN)
        g = Rectangle(width=1.6, height=28 * u, stroke_color=GUESS, stroke_width=3, fill_opacity=0).move_to(
            [3.2, base, 0], aligned_edge=DOWN)
        labs = VGroup(
            VGroup(tx(f"${W['census']:.1f}bn", 30, FACTORY, bold=True), tx("Census Bureau, 2023", 16, GREY_B),
                   tx("what US bottled-water plants shipped", 15, GREY_B)).arrange(DOWN, buff=0.05).next_to(b1, UP, buff=0.12),
            VGroup(tx(f"${W['primo']:.0f}bn", 30, RETAIL, bold=True), tx("Primo Brands' 10-K, 2023", 16, GREY_B),
                   tx("'retail sales'", 15, GREY_B)).arrange(DOWN, buff=0.05).next_to(b2, UP, buff=0.12),
            VGroup(tx("about $28bn", 30, GUESS, bold=True), tx("the game's sum", 16, GREY_B),
                   tx("units × illustrative prices", 15, GREY_B)).arrange(DOWN, buff=0.05).next_to(g, UP, buff=0.12))
        plant = draw.factory(1.0, color=FACTORY).next_to(b1, DOWN, buff=0.15)
        shop = draw.shop(0.9, color=RETAIL).next_to(b2, DOWN, buff=0.15)
        src = source("US Census Bureau, Annual Integrated Economic Survey (via FRED); Primo Brands, Form 10-K for 2024",
                     size=13)
        with self.voiceover(
            "Two published numbers for the same market, the same year. <bookmark mark='a'/> The Census Bureau, "
            f"which surveys American businesses every year, says American bottled-water plants shipped {W['census']:.1f} "
            f"billion dollars of water in 2023. <bookmark mark='b'/> Primo Brands, which says it has the largest "
            f"share of bottled water sold in American shops, told its shareholders the market was {W['primo']:.0f} billion "
            "dollars of retail sales. <bookmark mark='c'/> And your sum from the shelf was about twenty-eight. "
            f"The second number is {W['ratio']:.1f} times the first. Nobody made a mistake. They measured different "
            "things."
        ) as vo:
            self.play(FadeIn(src), FadeIn(plant, shift=UP * 0.2), FadeIn(shop, shift=UP * 0.2), Create(g))
            vo.wait_until("a")
            self.play(GrowFromEdge(b1, DOWN), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b2, DOWN), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(g.animate.set_stroke(width=5), FadeIn(labs[2]))
        self.clear_scene()

    def levers(self):
        rows = [("Which level of the chain?", "the price at the factory gate, or the price at the till: the "
                 "wholesaler, the truck and the shop all add their share", VGroup(draw.factory(0.6, color=FACTORY),
                                                                                 Text("→", font_size=28, color=GREY_A),
                                                                                 draw.truck(0.7, color=GREY_B),
                                                                                 Text("→", font_size=28, color=GREY_A),
                                                                                 draw.shop(0.6, color=RETAIL)).arrange(
                     RIGHT, buff=0.1)),
                ("Which plants?", "the Census files a plant by what it mainly makes: water bottled in a plant "
                 "that mainly makes soft drinks is counted as soft drinks", VGroup(draw.factory(0.6, color="#E8554E"),
                                                                                   draw.bottle(0.6, color=WATER)).arrange(
                     RIGHT, buff=0.1)),
                ("Which products?", "still, sparkling, flavoured, delivered jugs, imported Fiji and Evian", VGroup(
                    *[draw.bottle(0.6, color=c) for c in (WATER, "#9AD0F5", "#B58CFF", "#7BD88F")]).arrange(RIGHT, buff=0.05)),
                ("Which buyers, which year, which money?", "homes or offices; 2023 or 2024; dollars of the day or "
                 "after inflation", VGroup(draw.house(0.6, color=STONE), draw.coin(0.2)).arrange(RIGHT, buff=0.15))]
        cards = VGroup()
        for head, sub, pic in rows:
            pic.scale_to_fit_height(min(pic.height, 0.7))
            if pic.width > 2.6:
                pic.scale_to_fit_width(2.6)
            t_ = VGroup(tx(head, 24, WHITE, bold=True), tx(sub, 17, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            cards.add(VGroup(pic, t_).arrange(RIGHT, buff=0.4))
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.3, 0])
        for c_ in cards:
            c_[0].move_to([cards.get_left()[0] + 1.3, c_.get_y(), 0])
            c_[1].next_to(c_[0], RIGHT, buff=0.4).align_to(cards[0][1], LEFT)
        if cards.width > 13.4:
            cards.scale_to_fit_width(13.4)
        head = tx("Four questions every market size answers, whether it says so or not", 24, GOLD, bold=True).to_edge(
            UP, buff=0.45)
        with self.voiceover(
            "Every market size answers four questions, whether it says so or not. <bookmark mark='a'/> First, at which "
            "level of the chain? The Census counts what water is worth leaving the factory. By the time it reaches a "
            "shop till, a wholesaler, a truck and the shop itself have each added their share. <bookmark mark='b'/> "
            "Second, which plants? The Census files each plant under what it mainly makes. Water bottled in a plant "
            "that mostly makes soft drinks is counted with the soft drinks, not with the water. "
            "<bookmark mark='c'/> Third, which products? Still or sparkling, plain or flavoured, delivered in "
            "five-gallon jugs to offices, or imported from Fiji and France. <bookmark mark='d'/> And fourth, which "
            "buyers, which year, which money: homes or businesses, last year or this, dollars of the day or after "
            "inflation. Change any answer and the number moves, sometimes by billions. A market size without its "
            "definition is not a fact. It is half of one."
        ) as vo:
            self.play(FadeIn(head))
            for c_, m in zip(cards, "abcd"):
                vo.wait_until(m)
                self.play(FadeIn(c_[0], scale=0.8), FadeIn(c_[1], shift=RIGHT * 0.15))
        self.clear_scene()
