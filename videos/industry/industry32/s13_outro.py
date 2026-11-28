from __future__ import annotations

from videos.industry.industry32.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        H, M, U = R["hook"], R["models"], R["run"]
        lines = [
            (f"a shop: Amazon's own stores sold ${H['mix']['online'][2025]:.0f}bn of goods on thin margins", SHOP),
            (f"a marketplace: take rates from {M['take']['eBay']:.0f}% at eBay to {M['take']['Etsy']:.0f}% at Etsy, bounded by what both sides can do instead", MARKET),
            (f"a toll road: Shopify takes about {M['take']['Shopify']:.0f} cents of every dollar its merchants sell", TOOLS),
            (f"an ad business: Amazon's ${H['ads']:.0f}bn of ads, more than its shops' whole operating income", ADS),
            ("and a network: fast delivery is a fixed cost that only the biggest can spread", DELIV),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So is selling online a shop, a toll road or an advertising business? <bookmark mark='a'/> It is a shop, "
             "with a shop's thin margin, when the platform owns the stock. <bookmark mark='b'/> It is a marketplace when "
             "it does not, and its fee is bounded by what both sides can do instead. <bookmark mark='c'/> It is a toll "
             "road for the firms that sell the tools. <bookmark mark='d'/> And for the biggest, it is above all an "
             "advertising business, selling the top of the page to the sellers who need it. <bookmark mark='e'/> Holding "
             "it all together is a network of sheds and vans that only scale can pay for. The website was never the hard "
             "part.",
             base=[head("A shop, a toll road and an ad business")], steps=list(g))

    def close(self):
        lap = draw.laptop(2.0).move_to([-3.6, 0.4, 0])
        wh = draw.warehouse(2.6, docks=4, trucks=1).move_to([0.4, 0.4, 0])
        vn = draw.van(1.4, color=SHOP).move_to([3.8, 0.1, 0])
        nxt = tx("Next: Part 33, The Middlemen", 26, MARKET, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A screen, a shed and a van. Next time: the middlemen, the wholesalers and distributors who "
                            "sit between the makers and the shops, and why they are still there."):
            self.play(LaggedStart(FadeIn(lap), FadeIn(wh), FadeIn(vn), lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
