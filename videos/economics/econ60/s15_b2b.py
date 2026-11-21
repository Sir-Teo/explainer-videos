from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class B2B(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Business prices: \ negotiation, \ clauses, \ tenders", r"When every customer negotiates, \ "
             r"what is `the' price?", "Chapter thirteen. Business prices: negotiation, clauses, tenders.",
             lit={2013: r"Apple's e-books"}, scale=("firm",), horizon=("a year",))
        self.negotiated()
        self.mfn()

    def negotiated(self):
        cards = point_cards([
            (r"list price and discount", r"a list price that almost nobody pays, \ and a negotiated discount for "
             r"each customer", FIRM),
            (r"bargaining", r"Part 11's split: \ the price falls between each side's alternative, \ by bargaining "
             r"power", AIR),
            (r"price dispersion", r"buyers of the same product pay different prices, \ by size, \ skill and how "
             r"hard they push", COST),
            (r"tenders", r"for large orders, \ a sealed-bid auction among suppliers: \ Part 16's first-price rules, "
             r"\ and Part 59's bid-rigging screens", LEIS),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"how businesses price to businesses", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Much of the economy's trade is between firms, and there the posted price is the exception. <bookmark "
            "mark='a'/> A supplier publishes a list price that almost nobody pays, and negotiates a discount with "
            "each customer. <bookmark mark='b'/> The discount is a bargain: Part eleven's split, landing between "
            "each side's alternative according to their bargaining power. <bookmark mark='c'/> So buyers of the "
            "same product pay different prices, by their size, their skill and how hard they push, and much of a "
            "pricing team's work is managing that dispersion. <bookmark mark='d'/> For large orders, buyers run "
            "tenders: sealed-bid auctions among suppliers, with the first-price rules of Part sixteen, and the "
            "bid-rigging screens of Part fifty-nine watching them."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def mfn(self):
        M = load("menu")["mfn"]
        ax = plane([-0.6, 1.6], [0, 70], center=LEFT * 2.8 + DOWN * 0.4, x_length=5.6, y_length=4.4, xticks=[],
                   yticks=[0, 20, 40, 60], ylabel=r"price, \ \$", yfmt=lambda v: f"{v:.0f}", font_size=14)
        own = M["p_sep"]
        one = [M["p_one"], M["p_one"]]
        b1 = bars(ax, [-0.17, 0.83], own, [BUS, LEIS], width=0.3)
        b2 = bars(ax, [0.17, 1.17], one, [FIRM, FIRM], width=0.3)
        labs = VGroup(label(r"the customer \\ with the clause", font_size=14, color=BUS).next_to(ax.ax.c2p(0, 0), DOWN,
                                                                                                 buff=0.12),
                      label(r"a price-sensitive \\ customer", font_size=14, color=LEIS).next_to(ax.ax.c2p(1, 0), DOWN,
                                                                                               buff=0.12))
        vals = VGroup(*[label(f"{v:.0f}", font_size=15, color=c).next_to(x, UP, buff=0.05)
                        for v, c, x in zip(own + one, [BUS, LEIS, FIRM, FIRM], list(b1) + list(b2))])
        side = VGroup(
            label(r"a most-favoured-customer clause: \\ `you will get any lower price we give anyone'", font_size=19,
                  color=FIRM),
            label(rf"without it: \ {own[0]:.0f} and {own[1]:.0f}; \ with it, \ one price: \ {M['p_one']:.0f}",
                  font_size=20, color=WHITE),
            label(r"the clause protects one buyer \\ by raising the price to others", font_size=19, color=COST),
            label(r"across sellers it can soften competition: \\ a seller who cuts for one must cut for all",
                  font_size=19,
                  color=GREY_A),
            label(r"2013: \ Apple's e-book contracts with publishers carried such clauses; \\ a court found Apple had "
                  r"conspired with them to raise prices", font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"United States v. Apple, 952 F. Supp. 2d 638 (S.D.N.Y. 2013)", corner=DL, font_size=12)
        with self.voiceover(
            "One contract term deserves a closer look: the most-favoured-customer clause. <bookmark mark='a'/> A big "
            "customer insists that it will get any lower price the supplier gives anyone else. <bookmark mark='b'/> "
            f"Without the clause, the supplier charges it {own[0]:.0f} and a more price-sensitive customer "
            f"{own[1]:.0f}. With it, any discount to the second customer must go to the first too, so the supplier "
            f"charges both {M['p_one']:.0f}. <bookmark mark='c'/> The clause protects the buyer who has it by raising "
            "the price everyone else pays. <bookmark mark='d'/> Across sellers it can soften competition, since a "
            "seller who cuts its price for one customer must cut it for all. <bookmark mark='e'/> In 2013 a federal "
            "court found that Apple had conspired with publishers to raise the prices of e-books; clauses of this "
            "kind in their contracts were part of the story."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b1[0], DOWN), GrowFromEdge(b1[1], DOWN), FadeIn(vals[0]), FadeIn(vals[1]))
            self.play(GrowFromEdge(b2[0], DOWN), GrowFromEdge(b2[1], DOWN), FadeIn(vals[2]), FadeIn(vals[3]),
                      FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
