from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ auction desks", r"Who designs auctions today, \ and what do they do all day?",
             "Chapter fourteen. In practice: auction desks.",
             lit={1993: r"Porter and Zona", 2000: r"Guerre, Perrigne and Vuong", 2015: r"Britain's first CfD round"},
             scale=("firm", "market", "nation"), horizon=("a year",))
        self.where()
        self.values()
        self.work()

    def where(self):
        rows = point_cards([
            (r"regulators", r"spectrum teams: \ lots, \ caps, \\ reserves, \ activity rules", SECOND),
            (r"bidders' advisers", r"game theorists hired \\ to plan the bidding", FIRST),
            (r"treasuries, \ central banks", r"bond sales; \ the Bank of \\ England's product-mix auction",
             PRICE),
            (r"the platforms", r"reserves, \ quality scores, \\ machines that bid", ALLPAY),
            (r"procurement", r"reverse auctions: \ roads, \\ wind and solar contracts", RESERVE),
            (r"marketplaces", r"auction houses, \ online \\ sales, \ the fish market", VALUE),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.2)
        head = label(r"where auction economists work", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Auction design is now a trade. <bookmark mark='a'/> Regulators have spectrum teams who choose the lots, "
            "the caps on how much one company may win, the reserves and the activity rules. The companies hire their "
            "own game theorists to plan the bidding. Treasuries and central banks run auctions for bonds and loans, "
            "and the Bank of England uses a design of Paul Klemperer's, the product-mix auction, worked out during "
            "the financial crisis. The platforms employ auction teams who set reserves, weight bids by quality, and "
            "build the machines that bid on advertisers' behalf. Governments buy by reverse auction, from roads to "
            "wind and solar power: Britain has bought renewable electricity by auction since 2015. "
            "<bookmark mark='b'/> And the oldest marketplaces, the auction houses and the fish markets, are still "
            "there."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[1:5]], lag_ratio=0.9), run_time=14)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[5], shift=UP * 0.1))
        self.clear_scene()

    def values(self):
        head = label(r"reading values from bids: \ the first-price auction, \ inverted", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        eqs = VGroup(
            MathTex(r"\max_b\;(v - b)\,G(b)^{\,n-1}", font_size=40),
            MathTex(r"\Rightarrow\quad v = b + \frac{G(b)}{(n-1)\,g(b)}", font_size=46, color=FIRST),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.5)
        rows = VGroup(
            label(r"$G$: \ the spread of rivals' bids, \ seen in the data; \ $g$: \ its density", font_size=23,
                  color=GREY_A),
            label(r"each bid, \ plus a markup read off the bids, \ is the value behind it", font_size=24,
                  color=FIRST),
            label(r"Guerre, \ Perrigne and Vuong (2000): \ values, \ and so reserves and designs, \ from bids alone",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(eqs, DOWN, buff=0.5)
        tag = published_tag(r"Guerre, Perrigne and Vuong, Econometrica 68(3) (2000)", corner=DR, font_size=13)
        with self.voiceover(
            "The first thing an auction economist needs is the bidders' values, which nobody reveals. "
            "<bookmark mark='a'/> In a first-price auction, each bidder chooses its bid to maximize its value less "
            "its bid, times the chance that all rivals bid less. <bookmark mark='b'/> Turn that condition around, "
            "and the value behind each bid is the bid plus a markup, <bookmark mark='c'/> where the markup depends "
            "only on how rivals' bids are spread, which the data show. <bookmark mark='d'/> So each bid can be "
            "inverted into a value. <bookmark mark='e'/> Emmanuel Guerre, Isabelle Perrigne and Quang Vuong turned "
            "this into an estimator in 2000. With the values in hand, a seller can compute the best reserve, or "
            "simulate a different format, from bids alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def work(self):
        rows = VGroup(
            label(r"simulate the design on many draws of values, \ as Agora did: \ revenue, \ efficiency, \ the "
                  r"risk of no sale", font_size=23),
            label(r"test it on people first: \ laboratory ``wind tunnels'' before a billion-dollar sale",
                  font_size=23, color=SECOND),
            label(r"write the rules that theory leaves out: \ ties, \ increments, \ withdrawals, \ deposits",
                  font_size=23, color=FIRST),
            label(r"watch for collusion: \ bids that rotate, \ or move together \ (Porter and Zona's road "
                  r"contracts, 1993)", font_size=23, color=HOLD),
            label(r"part seventeen designs markets without prices; \ part sixty-one goes inside the platforms",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Porter and Zona, JPE 101(3) (1993); \ Plott, J. Econ.\ Management Strategy 6(3) (1997)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The rest of the work is engineering. <bookmark mark='a'/> Simulate the design on many draws of values, "
            "as Agora did in this part, and measure revenue, efficiency and the risk of no sale. "
            "<bookmark mark='b'/> Test it on people first: Charles Plott and others ran laboratory wind tunnels for "
            "the spectrum auctions before billions of dollars were at stake. <bookmark mark='c'/> Write the rules "
            "that theory leaves out: what happens at a tie, how much each bid must rise, whether a bid can be "
            "withdrawn, how much deposit a bidder must put down. <bookmark mark='d'/> And watch for collusion. "
            "Robert Porter and Douglas Zona showed in 1993 how the bids of a ring rigging road contracts on Long "
            "Island differed from honest ones. <bookmark mark='e'/> Part seventeen designs markets where prices "
            "can't be used, and part sixty-one goes inside the platforms."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
