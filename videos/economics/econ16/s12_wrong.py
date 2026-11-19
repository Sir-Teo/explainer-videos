from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403

MANN = "#F2788F"
TMOB = "#C9A0FF"


class Wrong(VoiceoverScene):
    def construct(self):
        card(self, 10, r"What went wrong", r"Signals in the bids, \ deals without words, \ and auctions nobody came "
             r"to", "Chapter ten. What went wrong.",
             lit={1997: r"trailing digits", 1999: r"Germany's ten blocks", 2000: r"The Hague and Bern",
                  2002: r"Klemperer"}, scale=("firm", "nation"), horizon=("a year",))
        self.digits()
        self.germany()
        self.dutch()
        self.called()
        self.lesson()

    def digits(self):
        s = load("spectrum")["signals"]["trailing"]
        head = label(r"the FCC's PCS auction, \ 1996--97: \ US West and McLeod", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        bid = VGroup(label(r"\$313,", font_size=64, color=GREY_A), label(r"378", font_size=64, color=HOLD)).arrange(
            RIGHT, buff=0.05).next_to(head, DOWN, buff=0.5)
        rows = VGroup(
            label(rf"round {s['uswest_bid_round']}: \ US West outbids McLeod for Waterloo, \ Iowa, \ with this bid",
                  font_size=24),
            label(rf"378 was the number of another licence: \ Rochester, \ Minnesota, \ which both wanted",
                  font_size=24, color=HOLD),
            label(r"the message: \ leave Rochester to us, \ or we fight you here", font_size=25, color=E.ACCENT),
            label(rf"McLeod took Waterloo back; \ US West won Rochester in round {s['uswest_wins_rochester_round']}",
                  font_size=23, color=GREY_A),
            label(r"the FCC later stopped bidders typing their own amounts", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.36).next_to(bid, DOWN, buff=0.45)
        tag = published_tag(r"Cramton and Schwartz, JRE 17(3) (2000)", corner=DR, font_size=13)
        with self.voiceover(
            "An ascending auction lets bidders talk, through their bids. <bookmark mark='a'/> In an FCC auction in "
            "1996 and 1997, the companies US West and McLeod both wanted licences in the American Midwest. In round "
            "fifty-nine US West outbid McLeod for the licence in Waterloo, Iowa, with a bid of three hundred and "
            "thirteen thousand, three hundred and seventy-eight dollars. <bookmark mark='b'/> Three seven eight was "
            "the number of another licence: Rochester, Minnesota, which both companies wanted. "
            "<bookmark mark='c'/> Peter Cramton and Jesse Schwartz read it as a message: leave Rochester to us, or "
            "we'll fight you in Waterloo. <bookmark mark='d'/> McLeod took Waterloo back, and "
            "US West won Rochester a few rounds later. <bookmark mark='e'/> Signals like these were common "
            "enough that the FCC later stopped bidders from typing their own amounts: they choose from a short "
            "menu of increments."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bid[0]), FadeIn(bid[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(bid[1], color=HOLD), FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def germany(self):
        g = load("spectrum")["signals"]["germany_1999"]
        head = label(r"Germany, \ 1999: \ ten blocks of spectrum, \ each new bid at least 10\% higher", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        cells = VGroup()
        for i in range(10):
            box = Square(side_length=0.95, stroke_color=GREY_B, stroke_width=2)
            num = label(rf"{i + 1}", font_size=16, color=GREY_B).move_to(box.get_top() + DOWN * 0.15)
            cells.add(VGroup(box, num))
        cells.arrange(RIGHT, buff=0.12).next_to(head, DOWN, buff=0.6)

        def bid_text(v, color):
            return label(rf"{v:g}", font_size=20, color=color)

        r1 = VGroup(*[bid_text(g["mannesmann_1_5"] if i < 5 else g["mannesmann_6_10"], MANN).move_to(
            cells[i][0].get_center() + DOWN * 0.1) for i in range(10)])
        r2 = VGroup(*[bid_text(g["tmobil_round2_1_5"], TMOB).move_to(cells[i][0].get_center() + DOWN * 0.1)
                      for i in range(5)])
        k1 = label(r"round 1: \ Mannesmann bids 18.18 on blocks 1--5, \ 20 on blocks 6--10 \ (million DM per MHz)",
                   font_size=22, color=MANN).next_to(cells, DOWN, buff=0.45)
        math_ = MathTex(r"18.18 \times 1.1 = 19.998 \approx 20", font_size=40, color=E.ACCENT).next_to(k1, DOWN,
                                                                                                    buff=0.35)
        k2 = label(r"round 2: \ T-Mobil bids 20 on blocks 1--5; \ nobody bids again", font_size=22,
                   color=TMOB).next_to(math_, DOWN, buff=0.35)
        quote = quote_card(r"There were no agreements with Mannesmann. \ But Mannesmann's first bid was a clear offer.",
                           r"a T-Mobil manager, \ Frankfurter Allgemeine Zeitung, \ 29 October 1999", width=11.0,
                           font_size=22, color=TMOB).to_edge(DOWN, buff=0.3)
        tag = published_tag(r"Klemperer, JEP 16(1) (2002), from Jehiel and Moldovanu (2000)", corner=UR,
                            font_size=12)
        with self.voiceover(
            "Bids can carry whole proposals. <bookmark mark='a'/> In 1999 Germany auctioned ten blocks of spectrum, "
            "with the rule that every new bid on a block had to beat the last by at least ten percent. In the first "
            "round, Mannesmann bid eighteen point one eight million marks per megahertz for blocks one to five, and "
            "twenty for blocks six to ten. <bookmark mark='b'/> Eighteen point one eight plus ten percent is nineteen "
            "point nine nine eight: twenty. <bookmark mark='c'/> In the second round T-Mobil bid exactly twenty on "
            "blocks one to five, and nobody bid again. Two rounds, and each company had half the spectrum at the "
            "same low price. <bookmark mark='d'/> A T-Mobil manager told a newspaper: there were no agreements with "
            "Mannesmann, but Mannesmann's first bid was a clear offer. Nothing about it was illegal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(r1), FadeIn(k1))
            vo.wait_until("b")
            self.play(FadeIn(math_))
            vo.wait_until("c")
            self.play(*[FadeOut(r1[i]) for i in range(5)], FadeIn(r2), FadeIn(k2))
            vo.wait_until("d")
            self.play(FadeOut(k1), FadeOut(math_), FadeOut(k2), FadeIn(quote))
        self.clear_scene()

    def dutch(self):
        e = load("spectrum")["euro"]
        nl = e["netherlands"]
        hc = history_card(2000, r"The Hague, \ July", r"five licences, \ five incumbents, \ and the British design",
                          color=HOLD, width=10.8, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"an ascending auction lets the strong outbid any newcomer: \ why enter?", font_size=24),
            label(r"the strongest would-be entrants joined incumbents instead", font_size=24, color=HOLD),
            label(r"one weak entrant bid, \ and stopped after an incumbent's letter threatening legal action",
                  font_size=23, color=HOLD),
            label(r"Switzerland, \ November: \ last-minute partnerships left as many bidders as licences",
                  font_size=23, color=GREY_A),
            label(rf"revenue per person: \ the Netherlands {e['per_capita_eur']['Netherlands']} euros, \ "
                  rf"Switzerland {e['per_capita_eur']['Switzerland']}, \ Britain {e['per_capita_eur']['United Kingdom']}",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Klemperer, EER 46 (2002)", corner=DR, font_size=13)
        with self.voiceover(
            "The Dutch sale went wrong in a different way. <bookmark mark='a'/> The Netherlands copied the British "
            "design, but had five licences and five incumbents. In an ascending auction a strong bidder can always "
            "outbid a weak one, so why would a newcomer pay to enter? <bookmark mark='b'/> The strongest would-be "
            "entrants partnered with incumbents instead. <bookmark mark='c'/> One weak newcomer did bid, and "
            "stopped after an incumbent sent it a letter threatening legal action. <bookmark mark='d'/> In "
            "Switzerland that autumn, a round of last-minute partnerships left as many bidders as licences. "
            "<bookmark mark='e'/> The Dutch raised a hundred and seventy euros a person, the Swiss twenty, the "
            "British six hundred and fifty."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["dutch_3g"]
        nl = load("spectrum")["euro"]["netherlands"]
        cc = call_card(r"the Dutch government, \ before its 3G auction", c.when,
                       rf"five licences would raise almost {nl['forecast_bn_eur']} billion euros, \ judging by "
                       r"Britain's sale",
                       rf"less than {nl['revenue_bn_eur_below']} billion euros: \ five incumbents for five licences, \ "
                       r"entrants who stayed away; \ Paul Klemperer had warned of it in the Dutch press",
                       c.verdict, width=12.4, font_size=23).move_to(UP * 0.5)
        q = label(r"a design copied from a country with more licences than incumbents, \ into one with as many",
                  font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Klemperer, EER 46 (2002)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Before its auction, the Dutch government expected almost ten billion "
            "euros, scaling up from Britain's. <bookmark mark='b'/> It raised less than three. Paul Klemperer, one "
            "of the British designers, had warned in the Dutch press that this design, with as many licences as "
            "incumbents, would keep entrants away. <bookmark mark='c'/> Wrong, by more than two thirds. A design "
            "that worked where there were more licences than incumbents was copied to a country with exactly as "
            "many."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()

    def lesson(self):
        hc = history_card(2002, r"Paul Klemperer, \ ``What Really Matters in Auction Design''", r"entry and "
                          r"collusion, \ far more than the fine points of theory", color=E.ACCENT, width=11.4,
                          font_size=24).to_edge(UP, buff=0.45)
        stages = VGroup(
            VGroup(label(r"stage 1: \ English", font_size=24, color=SECOND),
                   label(r"prices rise until only one bidder \\ more than the licences remains", font_size=20,
                         color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"stage 2: \ Dutch, \ or sealed", font_size=24, color=FIRST),
                   label(r"the survivors make one sealed bid each, \\ no lower than the last price", font_size=20,
                         color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=1.2).next_to(hc, DOWN, buff=0.6)
        arrow = Arrow(stages[0].get_right(), stages[1].get_left(), buff=0.15, color=GREY_B)
        rows = VGroup(
            label(r"the open stage finds the price; \ the sealed stage gives a weaker bidder a chance", font_size=23,
                  color=E.ACCENT),
            label(r"so newcomers come, \ and there is no last round of signals to coordinate on", font_size=23),
            label(r"the Anglo-Dutch auction, \ first proposed for Britain's 3G sale", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(stages, DOWN, buff=0.6)
        tag = published_tag(r"Klemperer, JEP 16(1) (2002); \ Klemperer, EER 42 (1998)", corner=DR, font_size=13)
        with self.voiceover(
            "Klemperer drew the lesson in a paper called What Really Matters in Auction Design. "
            "<bookmark mark='a'/> What matters most is entry and collusion, far more than the fine points of theory "
            "that the early chapters of this part were about. His own remedy combines the two games. "
            "<bookmark mark='b'/> First an English stage, with prices rising until only one more bidder remains than "
            "there are licences. <bookmark mark='c'/> Then the survivors make one sealed bid each, no lower than "
            "the last price. <bookmark mark='d'/> The open stage finds the price; the sealed stage gives a weaker "
            "bidder a real chance, since the strong can't simply top its bid. <bookmark mark='e'/> So newcomers "
            "come, and there is no last round of bidding in which to send signals. <bookmark mark='f'/> He called "
            "it the Anglo-Dutch auction, and first proposed it for Britain's sale."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(stages[0]))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(stages[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
            vo.wait_until("f")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
