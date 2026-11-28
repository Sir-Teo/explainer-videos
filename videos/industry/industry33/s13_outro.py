from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.close()

    def recap(self):
        U = R["run"]
        lines = [
            ("connecting many to many: one wholesaler turns millions of links into thousands", GOODS),
            (f"a few cents of each dollar, on almost no money of its own: the Works' distributor needs {m(U['base']['capital'])}", GOOD),
            ("density: the biggest local player delivers for less, so a few firms hold each market", DRUG),
            ("the service: holding stock and delivering tomorrow, which no website does by itself", IND),
            ("and where margins are too thin, the middleman becomes an owner, as the trading houses did", TRADE),
        ]
        g = VGroup(*[tx(t, 19, c, bold=True) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        for r_ in g:
            if r_.width > 12.8:
                r_.scale_to_fit_width(12.8)
        beat(self,
             "So if the internet removes the middleman, why are the middlemen among the largest companies in every "
             "country? <bookmark mark='a'/> Because connecting many makers to many buyers is cheaper through one middle "
             "than through millions of direct links. <bookmark mark='b'/> Because a penny on a dollar is a good business "
             "when other people's money pays for the stock. <bookmark mark='c'/> Because density lets the biggest local "
             "player deliver for less, so a few firms win each market. <bookmark mark='d'/> Because the service is the stock "
             "and the truck, not the order form. <bookmark mark='e'/> And because, where the margin is too thin, the "
             "middleman can become an owner. The internet changed how orders arrive; it did not change who brings them.",
             base=[head("Still in the middle")], steps=list(g))

    def close(self):
        f = draw.factory(1.4).move_to([-4.2, 0.3, 0])
        wh = draw.warehouse(2.6, docks=4, trucks=1).move_to([0, 0.4, 0])
        sh = draw.shop(1.4, color=FOOD).move_to([4.2, 0.3, 0])
        nxt = tx("Next: Part 34, Restaurants and Franchising", 26, TRADE, bold=True).move_to([0, -2.4, 0])
        with self.voiceover("A maker, a warehouse and a shop. Next time: restaurants and franchising, where the brand "
                            "owner rarely owns the restaurant."):
            self.play(LaggedStart(FadeIn(f), FadeIn(wh), FadeIn(sh), lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(nxt))
        self.clear_scene()
