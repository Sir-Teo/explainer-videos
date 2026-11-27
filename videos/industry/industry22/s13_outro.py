from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, D, Rt, Pr, T = R["hook"], R["dollar"], R["retailer"], R["pricing"], R["tobacco"]
        lines = [
            (f"the gap: P&G sells for {H['ratio']:.1f} times what its products cost to make and ship", BRAND),
            (f"it is paid for: {100 * D['ads']:.0f}c of each dollar on advertising, every year (the Works: stop, and share slides)", ADS),
            ("advertising is a fixed cost, so the biggest spender pays least per bottle", WHITE),
            (f"the buyer pushes back: Walmart takes {Rt['walmart']['Clorox']}% of Clorox, {Rt['walmart']['Procter & Gamble']}% of P&G, and sells its own label", PRICE),
            (f"the test: prices up {Pr[2023]['price']}% in a year, volume down {abs(Pr[2023]['vol'])}%; Marlboro the leader for 50 years", GOOD),
        ]
        g = VGroup(*[tx(t, 20, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        beat(self,
             "So why can a company charge double for soap? <bookmark mark='a'/> Because the product is cheap to make and the "
             "name is not: half the price is the brand. <bookmark mark='b'/> The brand is kept alive by spending, every "
             "year, on being remembered; stop, and shoppers drift to the cheaper bottle. <bookmark mark='c'/> That spending is "
             "a fixed cost, so the biggest brands pay least per bottle for it, and stay the biggest. <bookmark mark='d'/> The "
             "retailers push back with their size and their own labels, and take a share of the gap. <bookmark mark='e'/> "
             "And when prices rose for everyone, the brands raised theirs and most shoppers stayed. Double, for a hundred "
             "years, is a premium that is paid for every year.",
             base=[head("Double, for a hundred years")], steps=list(g))

    def close(self):
        items = VGroup(draw.soap(0.9), draw.detergent(1.1), draw.cereal_box(1.1), draw.can(0.9), draw.can(0.9, color="#7EC8F5")).arrange(RIGHT, buff=0.45).move_to([0, 0.6, 0])
        nxt = tx("Next: Part 23, Fashion and Luxury", 26, PRICE, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("Everyday things, sold at a premium that has to be earned again every year: consumer goods are a "
                            "business of memory, paid for in advertising, defended on the shelf, and tested every time "
                            "prices rise. Next time: fashion and luxury, two industries that sell clothes and run on "
                            "opposite rules.") as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in items], lag_ratio=0.2), run_time=2)
            self.play(items.animate.scale(1.1), run_time=1.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
