from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        U, F, C = R["run"], R["turns"], R["club"]
        lines = [
            (f"thin margins: about three cents per dollar at Walmart and Costco; a 1% price cut needs {100 * U['cut1_need']:.0f}% more sales", BAD),
            (f"fast turns: goods sell before they are paid for; Walmart's suppliers fund about ${F['float']['Walmart']['funded']:.0f}bn", GOOD),
            ("scale: the same lorries, warehouses and buyers behind thousands of stores", MASS),
            (f"the fee: Costco's ${C['fees']:.1f}bn of membership fees, half its operating income", CLUB),
            ("and local markets: the court that stopped Kroger and Albertsons looked at towns, not the nation", GROCER),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So how does a business that keeps two or three cents of every dollar become one of the largest on earth? "
             "<bookmark mark='a'/> By accepting the thin margin that competition sets, and never starting the price war "
             "that would wipe it out. <bookmark mark='b'/> By selling goods so fast that the suppliers pay for the stock. "
             "<bookmark mark='c'/> By spreading the same lorries, warehouses and buyers over thousands of stores. "
             "<bookmark mark='d'/> Sometimes, by charging at the door. <bookmark mark='e'/> And by winning town by town, "
             "because that is where shoppers, and courts, look. None of it is glamorous, and all of it is hard to copy: "
             "the giants of grocery are giants of logistics that happen to have tills.",
             base=[head("Pennies, turned fast")], steps=list(g))

    def close(self):
        shop = draw.shop(3.0, color=GROCER).move_to([-3.0, 0.4, 0])
        cart = draw.cart(1.6).move_to([0.6, 0.0, 0])
        pk = draw.parcel(0.9).move_to([3.4, 0.0, 0])
        nxt = tx("Next: Part 32, E-commerce", 26, CLUB, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A shop, a trolley, and a parcel. Next time: e-commerce, and whether selling online is a shop, a "
                            "toll road or an advertising business."):
            self.play(LaggedStart(FadeIn(shop), FadeIn(cart), FadeIn(pk), lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
