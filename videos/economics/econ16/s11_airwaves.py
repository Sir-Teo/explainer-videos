from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403

NAT = "#C9A0FF"


class Airwaves(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Selling the airwaves", r"How do you sell hundreds of licences at once, \ when each is worth "
             r"more alongside others?", "Chapter nine. Selling the airwaves.",
             lit={1959: r"Coase proposes it", 1994: r"the FCC's first auctions", 2000: r"Britain's 3G sale"},
             scale=("market", "nation"), horizon=("a decade",))
        self.history()
        self.saa()
        self.exposure()
        self.britain()

    def history(self):
        rows = VGroup(
            label(r"1927 to 1993: \ American licences given away by hearings, \ then by lottery", font_size=24),
            label(r"1959: \ Ronald Coase proposes selling them to the highest bidder; \ the FCC is not persuaded",
                  font_size=24, color=GREY_A),
            label(r"1993: \ Congress allows auctions; \ the FCC asks economists to design them", font_size=24,
                  color=SECOND),
            label(r"the problem: \ hundreds of licences, \ each worth more next to its neighbours", font_size=24,
                  color=HOLD),
            label(r"one at a time, \ a bidder can't know what to pay for the first \ without the price of the rest",
                  font_size=24, color=HOLD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Coase, JLE 2 (1959); \ McMillan, JEP 8(3) (1994); \ Milgrom, \emph{Putting Auction "
                            r"Theory to Work} (2004)", corner=DR, font_size=12)
        with self.voiceover(
            "For most of the twentieth century, American governments gave radio licences away. "
            "<bookmark mark='a'/> The Federal Communications Commission held hearings to decide who deserved them, "
            "and in the 1980s it held lotteries. <bookmark mark='b'/> In 1959 Ronald Coase had proposed selling them "
            "to the highest bidder, and one commissioner asked him whether he was joking. <bookmark mark='c'/> In 1993 "
            "Congress allowed auctions, and the Commission asked economists to design them. "
            "<bookmark mark='d'/> The problem was hard. There were hundreds of licences, one for each area and band, "
            "and a licence was worth more next to its neighbours: a phone network covering a whole region is worth "
            "more than the sum of its scraps. <bookmark mark='e'/> Sold one at a time, a bidder could not know what "
            "to pay for the first licence without knowing the price of the rest."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def saa(self):
        hc = history_card(1994, r"the simultaneous ascending auction", r"Paul Milgrom, \ Robert Wilson and Preston "
                          r"McAfee", color=SECOND, width=11.0, font_size=24).to_edge(UP, buff=0.45)
        rows = point_cards([
            (r"all at once", r"every licence open \\ at the same time", SECOND),
            (r"in rounds", r"bids rise round by round; \\ prices are posted", SECOND),
            (r"switching", r"move to the licences \\ that are cheap for you", PRICE),
            (r"an activity rule", r"bid now or lose the \\ right to bid later", FIRST),
            (r"one ending", r"nothing closes until \\ nothing gets a new bid", E.ACCENT),
            (r"a Nobel", r"Milgrom and Wilson, \\ 2020", GREY_A),
        ], width=12.6, cols=3, font_size=22).next_to(hc, DOWN, buff=0.45)
        with self.voiceover(
            "The design that won was the simultaneous ascending auction, worked out by Paul Milgrom, Robert Wilson "
            "and Preston McAfee. <bookmark mark='a'/> Every licence is open at once, and bids rise in rounds, with "
            "the standing high bids posted after each. Bidders can switch to whichever licences are cheap for them, "
            "and so build the network they want as prices form. <bookmark mark='b'/> An activity rule stops anyone "
            "waiting to see what others do: a bidder who doesn't bid now loses the right to bid later. "
            "<bookmark mark='c'/> And nothing closes until no licence gets a new bid. The first such auctions ran in "
            "1994. The format and its descendants have since sold spectrum around the world for many billions of "
            "dollars, and in 2020 Milgrom and Wilson shared the Nobel prize for their work on auctions."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[:3]], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[3], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows.cards[4], shift=UP * 0.1), FadeIn(rows.cards[5], shift=UP * 0.1))
        self.clear_scene()

    def exposure(self):
        x = load("exposure")
        c1, c2 = x["cases"]
        head = label(r"the exposure problem: \ two fishing rights, \ North and South", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        who = VGroup(
            VGroup(islander("bo", 0.7), label(rf"Bo: \ both together, \ {x['both']:.0f}; \ either alone, "
                                             rf"{x['alone']:.0f}", font_size=20, color=NAT)).arrange(RIGHT, buff=0.25),
            VGroup(islander("ana", 0.7), label(r"Ana: \ North only", font_size=20, color=RIVALS[0])).arrange(RIGHT,
                                                                                                    buff=0.25),
            VGroup(islander("dara", 0.7), label(r"Dara: \ South only", font_size=20, color=RIVALS[2])).arrange(
                RIGHT, buff=0.25),
        ).arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.35)

        def case_block(c, title, color):
            r_lo, r_hi = c["rivals"]
            lines = VGroup(
                label(title, font_size=22, color=color),
                label(rf"Bo cautious: \ bids each only to {x['alone']:.0f}; \ Ana and Dara win; \ surplus "
                      rf"{c['cautious']['welfare']:.0f}", font_size=19, color=GREY_A),
            )
            b = c["bold"]
            if b["national_wins"] == 2:
                lines.add(label(rf"Bo bold: \ wins both, \ paying {b['prices'][0]:.0f} + {b['prices'][1]:.0f}; \ "
                                rf"profit {b['national_profit']:.0f}; \ surplus {b['welfare']:.0f}", font_size=19,
                                color=NAT))
            else:
                lines.add(label(rf"Bo bold: \ wins one at {b['prices'][0]:.0f}, \ worth {x['alone']:.0f} alone; "
                                rf"\ profit {b['national_profit']:.0f}", font_size=19, color=HOLD))
            lines.add(label(rf"the best outcome: \ {'Bo' if c['efficient'] == 'national' else 'Ana and Dara'}; \ "
                            rf"surplus {c['efficient_welfare']:.0f}", font_size=19, color=E.ACCENT))
            return lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        b1 = case_block(c1, rf"if Ana and Dara value theirs at {c1['rivals'][0]:.0f} and {c1['rivals'][1]:.0f}",
                        PRICE)
        b2 = case_block(c2, rf"if they value theirs at {c2['rivals'][0]:.0f} and {c2['rivals'][1]:.0f}", HOLD)
        VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(who, DOWN, buff=0.45)
        foot = label(r"the cure: \ let Bo bid for the pair as a package \ (combinatorial auctions)", font_size=23,
                     color=SECOND).to_edge(DOWN, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Selling licences side by side has one trap, and the island shows it with two fishing rights, North and "
            "South. <bookmark mark='a'/> Bo wants both: together they are worth ten to him, but either alone only "
            "one. Ana wants only North, and Dara only South. <bookmark mark='b'/> Suppose Ana and Dara value theirs "
            "at four each. If Bo is cautious and bids each right only up to one, its value alone, Ana and Dara win, "
            "and the island's surplus is eight. If Bo is bold, and bids until the two prices together reach ten, he "
            "wins both for eight and makes two: the best outcome, worth ten. <bookmark mark='c'/> But suppose instead "
            "that Ana values North at two and Dara values South at nine. Bold Bo wins North at two, but South climbs "
            "past eight, and he must stop, holding one right worth one to him, which cost him two. He loses. "
            "<bookmark mark='d'/> Caution wastes the pair's value; boldness risks a loss. That is the exposure "
            "problem. <bookmark mark='e'/> The cure is to let Bo bid for the pair as a package. Combinatorial "
            "auctions do that, and Britain sold its 4G licences with one in 2013."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(who))
            vo.wait_until("b")
            self.play(FadeIn(b1))
            vo.wait_until("c")
            self.play(FadeIn(b2))
            vo.wait_until("d")
            self.play(Indicate(b2[2], color=WHITE, scale_factor=1.03))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def britain(self):
        uk = load("spectrum")["uk"]
        rows = VGroup(
            label(r"Britain, \ 2000: \ four incumbents, \ and the design's first question was entry", font_size=24),
            label(r"with four licences, \ four incumbents might scare everyone else away", font_size=23,
                  color=HOLD),
            label(r"so five licences, \ and the largest reserved for a newcomer", font_size=24, color=SECOND),
            label(rf"{uk['bidders']} bidders; \ {uk['rounds']} rounds; \ \pounds{uk['revenue_bn_gbp']} billion",
                  font_size=26, color=PRICE),
            label(rf"Vodafone paid about \pounds{uk['vodafone_bn_gbp']} billion for one licence; \ every licence "
                  rf"went for over \pounds{uk['cheapest_over_bn_gbp']} billion", font_size=22, color=GREY_A),
            label(r"the companies overpaid, \ said some, \ as the telecom bubble burst; \ the designers replied "
                  r"that a sunk price doesn't raise a phone bill", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Binmore and Klemperer, EJ 112(478) (2002)", corner=DR, font_size=13)
        with self.voiceover(
            "Britain's sale of 2000 faced a different problem first. <bookmark mark='a'/> There were four "
            "established mobile companies, and an auction is only as good as its bidders. <bookmark mark='b'/> With "
            "four licences, the four incumbents would each expect to win one, and nobody else would bother to "
            "come, knowing the incumbents valued a licence more. <bookmark mark='c'/> So the designers offered five "
            "licences, and kept the largest for a newcomer, which guaranteed that at least one would win. "
            "<bookmark mark='d'/> Thirteen companies bid, over a hundred and fifty rounds, for twenty-two and a half "
            "billion pounds. <bookmark mark='e'/> Vodafone paid about six billion for a single licence, and every "
            "licence went for more than four. <bookmark mark='f'/> Within a year the telecom bubble had burst, and "
            "some said the companies had been fleeced. The designers replied that the price of a licence, once paid, "
            "is sunk: it does not raise anyone's phone bill, which is set by competition, as part ten showed."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
