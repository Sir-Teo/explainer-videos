from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403



class Units(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Many units: \ bonds and electricity", r"When many identical units are sold at once, \ "
             r"should every winner pay the same price?", "Chapter twelve. Many units: bonds and electricity.",
             lit={1929: r"the first bill auction", 1960: r"Friedman", 1992: r"the Treasury's experiment",
                  2001: r"Britain's electricity"}, scale=("market", "nation"), horizon=("a week",))
        self.treasury()
        self.reduction()
        self.electricity()

    def treasury(self):
        t = load("spectrum")["treasury"]
        rows = VGroup(
            label(r"the Treasury sells billions of identical bills at once: \ each bidder says how many, \ at what "
                  r"yield", font_size=23),
            label(rf"from {t['bills_first']}: \ pay your own bid \ (``multiple-price'', \ or pay-as-bid)",
                  font_size=24, color=FIRST),
            label(r"Milton Friedman, \ 1960: \ charge every winner the same price, \ the lowest accepted",
                  font_size=24, color=SECOND),
            label(r"then bidders need not guess the market, \ and bid what the bills are worth to them",
                  font_size=23, color=SECOND),
            label(r"1991: \ broken auction rules; \ 1992: \ an experiment on two- and five-year notes",
                  font_size=23, color=GREY_A),
            label(rf"{t['all_single_price']}: \ one price for every auction, \ on evidence the Treasury called "
                  r"not unambiguous", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Garbade and Ingber, NY Fed Current Issues 11(2) (2005)", corner=DR, font_size=13)
        with self.voiceover(
            "Some auctions sell many identical units at once. <bookmark mark='a'/> The American Treasury sells "
            "billions of dollars of bills and notes at a time, and each bidder says how many it wants, at what "
            "yield. <bookmark mark='b'/> From its first bill auction in 1929, the Treasury charged each winner its "
            "own bid. <bookmark mark='c'/> In 1960 Milton Friedman argued for a single price instead: every winner "
            "pays the same, the price of the last bid accepted. <bookmark mark='d'/> Then, he said, nobody need "
            "guess where the market will clear, and bidders would simply bid what the bills were worth to them. "
            "<bookmark mark='e'/> Nothing changed until 1991, when a dealer was found breaking the auction's rules. "
            "In the overhaul that followed, the Treasury tried single prices on its two- and five-year notes. "
            "<bookmark mark='f'/> In 1998 it moved every auction to a single price, though its own studies of the "
            "experiment could not say for certain that it had saved money."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def reduction(self):
        b = load("bonds")
        tr, best, vk = b["truthful"], b["best"], b["vickrey"]
        head = label(r"two bonds; \ Bo wants both, \ worth 10 each; \ Dara wants one, \ worth 6", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        who = VGroup(VGroup(islander("bo", 0.7), label(r"10, \ 10", font_size=20, color=BO)).arrange(DOWN,
                                                                                                    buff=0.08),
                     VGroup(islander("dara", 0.7), label(r"6", font_size=20, color=DARA)).arrange(DOWN, buff=0.08)
                     ).arrange(RIGHT, buff=1.2).next_to(head, DOWN, buff=0.3)
        hdr = [r"rule", r"who wins", r"price", r"Bo's profit", r"seller gets", r"surplus"]
        xs = [-4.6, -1.5, 0.6, 2.3, 4.0, 5.6]
        top = 0.9
        header = VGroup(*[label(h, font_size=21, color=GREY_B).move_to([xs[j], top, 0]) for j, h in enumerate(hdr)])

        def row(i, cells, colors):
            return VGroup(*[label(c, font_size=25, color=col).move_to([xs[j], top - 0.7 * (i + 1), 0])
                            for j, (c, col) in enumerate(zip(cells, colors))])

        r1 = row(0, [r"one price; \ Bo bids for 2", r"Bo, \ Bo", rf"{tr['price']:.0f} each", rf"{tr['big_profit']:.0f}",
                     rf"{tr['revenue']:.0f}", rf"{tr['surplus']:.0f}"],
                 [SECOND, WHITE, WHITE, BO, PRICE, WHITE])
        r2 = row(1, [r"one price; \ Bo bids for 1", r"Bo, \ Dara", rf"{best['price']:.0f}",
                     rf"{best['big_profit']:.0f}", rf"{best['revenue']:.0f}", rf"{best['surplus']:.0f}"],
                 [HOLD, WHITE, WHITE, BO, HOLD, HOLD])
        r3 = row(2, [r"Vickrey's rule", r"Bo, \ Bo", rf"{vk['big_pays']:.0f} in all", rf"{vk['big_profit']:.0f}",
                     rf"{vk['revenue']:.0f}", rf"{vk['surplus']:.0f}"],
                 [PRICE, WHITE, WHITE, BO, PRICE, WHITE])
        foot = VGroup(
            label(r"with one price, \ a big buyer's own bid sets the price it pays: \ so it asks for less",
                  font_size=22, color=HOLD),
            label(r"demand reduction \ (Ausubel and Cramton): \ less revenue, \ and units in the wrong hands",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.15).move_to(DOWN * 2.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Friedman's single price has its own trap, and two bonds on the island show it. "
            "<bookmark mark='a'/> Bo wants both bonds, each worth ten to him. Dara wants one, worth six. The seller "
            "charges every winner one price: the highest bid that loses. <bookmark mark='b'/> If Bo bids for both "
            "bonds at their value, Dara's six is the losing bid, so Bo wins both and pays six each. His profit is "
            "eight. <bookmark mark='c'/> But if Bo bids for only one bond, nobody loses. Bo and Dara each get one, "
            "the price falls to nothing, and Bo's profit is ten. Asking for less pays him. The seller gets "
            "nothing, and one bond goes to Dara, who values it less. <bookmark mark='d'/> Vickrey's rule for many "
            "units charges each winner the bids it displaces. Bo wins both and pays six in all: his profit is "
            "fourteen, so he has no reason to ask for less, and the bonds go where they are worth most. "
            "<bookmark mark='e'/> With one price, a big buyer's own bid sets the price it pays on everything it buys, "
            "so it asks for less than it wants. Lawrence Ausubel and Peter Cramton called it demand reduction: less "
            "revenue, and units in the wrong hands."
        ) as vo:
            self.play(FadeIn(head), FadeIn(header), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(who))
            vo.wait_until("b")
            self.play(FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(r3))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def electricity(self):
        rows = VGroup(
            label(r"electricity markets: \ generators offer power at prices, \ cheapest first, \ until demand is met",
                  font_size=23),
            label(r"most pay every generator the same price: \ the offer of the last one needed", font_size=23,
                  color=SECOND),
            label(r"Britain, \ 2001: \ the Pool's single price gave way to trading \ with a market that pays each "
                  r"its own offer", font_size=22, color=FIRST),
            label(r"the hope: \ lower prices; \ the theory: \ generators would offer what they expect the price to be",
                  font_size=22, color=GREY_A),
            label(r"2022: \ when gas set the price paid to every generator, \ Europe asked again; \ its regulators "
                  r"kept the single price", font_size=22, color=GREY_A),
            label(r"pay-as-bid changes how bidders bid \ more than what they pay", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Krishna, \emph{Auction Theory}, chs.\ 12--13; \ Wolak, in \emph{Handbook of "
                            r"Industrial Organization} (2021)", corner=DR, font_size=12)
        with self.voiceover(
            "Electricity markets face the same choice every day. <bookmark mark='a'/> Generators offer power at "
            "prices, and the market takes the cheapest offers first until demand is met. "
            "<bookmark mark='b'/> Most markets pay every generator the same price: the offer of the last one needed. "
            "<bookmark mark='c'/> In 2001 Britain replaced its Pool, which did that, with arrangements in which "
            "generators trade with buyers directly, and a balancing market pays each its own offer. "
            "<bookmark mark='d'/> The hope was lower prices. The theory says generators who are paid their offers "
            "simply offer what they expect the market price to be. <bookmark mark='e'/> In 2022, when gas set the "
            "price paid to every generator in Europe, the question was asked again, and Europe's regulators, after a "
            "review, kept the single price. <bookmark mark='f'/> Paying the bids changes how people bid, more than "
            "what they end up paying."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
