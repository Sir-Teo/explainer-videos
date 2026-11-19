from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.london()
        self.hague()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def london(self):
        uk = load("spectrum")["uk"]
        hc = history_card(2000, r"London, \ 6 March to 27 April", r"five licences for the airwaves of the third "
                          r"generation of mobile phones, \ sold by auction", color=E.ACCENT, width=11.6,
                          font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(rf"{uk['bidders']} bidders, \ {uk['licences']} licences, \ one of them kept for a newcomer",
                  font_size=25),
            label(rf"{uk['rounds']} rounds over seven weeks, \ every licence open until nobody bid again",
                  font_size=25, color=SECOND),
            label(rf"\pounds{uk['revenue_bn_gbp']} billion: \ about {uk['share_of_gnp'] * 100:.1f}\% of the "
                  r"nation's income", font_size=27, color=PRICE),
            label(r"five to ten times what the newspapers had predicted", font_size=25, color=GREY_A),
            label(r"the design: \ game theorists, \ led by Ken Binmore and Paul Klemperer", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.34).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Binmore and Klemperer, EJ 112(478) (2002)", corner=DR, font_size=13)
        with self.voiceover(
            "On the sixth of March 2000 the British government began to sell five licences to use the airwaves for "
            "the third generation of mobile phones, the ones that would carry the internet. It sold them by auction. "
            "<bookmark mark='a'/> Thirteen companies bid for five licences, one of which was kept for a company that "
            "did not already run a network. <bookmark mark='b'/> The bidding went on for seven weeks and a hundred "
            "and fifty rounds, with every licence open until nobody wanted to bid again. "
            "<bookmark mark='c'/> It raised twenty-two and a half billion pounds, about two and a half percent of "
            "the nation's income. <bookmark mark='d'/> That was five to ten times what the newspapers had predicted. "
            "<bookmark mark='e'/> The sale had been designed by economists, led by Ken Binmore and Paul Klemperer, "
            "using the theory of games."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def hague(self):
        eu = load("spectrum")["euro"]
        pc = eu["per_capita_eur"]
        order = ["United Kingdom", "Germany", "Italy", "Netherlands", "Austria", "Switzerland"]
        cols = {"United Kingdom": PRICE, "Germany": PRICE, "Italy": FIRST, "Netherlands": HOLD, "Austria": FIRST,
                "Switzerland": HOLD}
        base_y, scale_y, x0, dx = -2.4, 4.2 / 700, -4.6, 1.85
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for i, c in enumerate(order):
            h = pc[c] * scale_y
            r = Rectangle(width=1.1, height=max(h, 0.03), stroke_width=0, fill_color=cols[c], fill_opacity=0.85)
            r.move_to([x0 + i * dx, base_y + h / 2, 0])
            bars.add(r)
            names.add(label(c.replace("United Kingdom", "Britain"), font_size=19, color=GREY_A).next_to(
                [x0 + i * dx, base_y, 0], DOWN, buff=0.15))
            vals.add(label(rf"{pc[c]}", font_size=22, color=cols[c]).next_to(r, UP, buff=0.1))
        base = Line([x0 - 0.9, base_y, 0], [x0 + 5 * dx + 0.9, base_y, 0], color=GREY_B, stroke_width=2)
        head = label(r"the 3G auctions of 2000: \ euros raised per person", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.4)
        side = VGroup(
            label(r"the Netherlands, \ July: \ forecast almost 10 billion euros; \ raised less than 3", font_size=21,
                  color=HOLD),
            label(r"the same airwaves, \ the same phones: \ a different design, \ and different bidders",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.12).next_to(head, DOWN, buff=0.25)
        tag = published_tag(r"Klemperer, EER 46 (2002), Table 1", corner=DR, font_size=13)
        with self.voiceover(
            "That summer the rest of Europe sold the same kind of licences. Here is what each country raised, in euros "
            "per person. <bookmark mark='a'/> Britain, six hundred and fifty. Germany, six hundred and fifteen. Italy, "
            "two hundred and forty. <bookmark mark='b'/> The Netherlands, a hundred and seventy: its government had "
            "forecast almost ten billion euros, and raised less than three. Austria, a hundred. And Switzerland, in "
            "the autumn, twenty. <bookmark mark='c'/> The airwaves were much the same, and so were the phones and the "
            "companies. What differed was the design of the sale, and who turned up to bid."
        ) as vo:
            self.play(FadeIn(head), FadeIn(base), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(bars[i], DOWN) for i in range(3)], *[FadeIn(vals[i]) for i in range(3)])
            vo.wait_until("b")
            self.play(*[GrowFromEdge(bars[i], DOWN) for i in range(3, 6)], *[FadeIn(vals[i]) for i in range(3, 6)],
                      FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"the airwaves", r"licences for phones, \\ sold by governments", SECOND),
            (r"Treasury bills", r"sold by auction \\ since 1929", PRICE),
            (r"every search ad", r"an auction run in a \\ fraction of a second", FIRST),
            (r"electricity", r"generators' offers, \\ cleared through the day", VALUE),
            (r"art, \ houses, \ fish", r"the oldest auctions \\ of all", ALLPAY),
            (r"government contracts", r"auctions in reverse: \\ the lowest bid wins", RESERVE),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"whenever nobody knows what a thing is worth, \ it is auctioned", font_size=30,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Auctions are everywhere that a seller does not know what something is worth to its buyers. "
            "<bookmark mark='a'/> Governments sell the airwaves this way. The American Treasury has sold its bills "
            "by auction since 1929. Every advertisement beside a search result is placed by an auction, "
            "run in a fraction of a second while the page loads. Electricity markets clear generators' offers "
            "through the day. Art, houses and the morning's catch are auctioned, as they have been for centuries. "
            "<bookmark mark='b'/> And governments buy by auction in reverse, where the lowest offer wins."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[:5]], lag_ratio=0.6), run_time=9)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[5], shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"which format should the seller choose: \ open or sealed, \ rising or falling?", font_size=28,
                  color=SECOND),
            label(r"how much should a bidder bid, \ when bidding more wins more often \ but earns less?",
                  font_size=28, color=FIRST),
            label(r"and what goes wrong: \ too few bidders, \ collusion, \ the winner's curse?", font_size=28,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part fifteen was about the spillovers no market prices. This part is about markets built on purpose. "
            "How should something be sold, when nobody knows what it is worth to the buyers? "
            "<bookmark mark='a'/> Which format should the seller choose: open or sealed, with a price that rises or "
            "one that falls? <bookmark mark='b'/> How much should a bidder bid, when a higher bid wins more often but "
            "earns less when it wins? <bookmark mark='c'/> And what goes wrong: too few bidders, bidders who "
            "collude, and winners who pay too much?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = gavel(height=1.0)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 16 \ $\cdot$ \ Auctions", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixteen: auctions."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IV \ $\cdot$ \ Failure and Design", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"bid twice for a canoe; \ the four formats, \ and why they are two games",
            r"Vickrey's proof; \ shading, \ derived; \ revenue equivalence, \ and when it fails",
            r"Myerson's reserve price; \ the winner's curse, \ in oil and in a jar of coins",
            r"selling the airwaves, \ and what went wrong; \ the auction behind every search",
            r"bonds and electricity; \ a dial for reserves; \ credible auctions and auto-bidders",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Four. <bookmark mark='a'/> You'll bid twice for Crusoe's old canoe, then meet "
            "the four standard formats, and find that they are really two games. <bookmark mark='b'/> Vickrey's proof "
            "that you should bid your value; how much to shade a bid, derived; and the theorem that the formats raise "
            "the same money, with the ways it fails. <bookmark mark='c'/> Myerson's reserve price; and the winner's "
            "curse, in oil fields and in a jar of coins. <bookmark mark='d'/> Selling the airwaves, and what went "
            "wrong; and the auction behind every search. <bookmark mark='e'/> Then bonds and electricity, a dial for "
            "reserve prices, and a frontier of credible auctions and machines that bid."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
