from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403

NAMES = ("ana", "bo", "dara", "friday")


class Ads(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The auction behind every search", r"Three slots beside a search, \ many advertisers: \ who "
             r"gets which, \ and what do they pay?", "Chapter eleven. The auction behind every search.",
             lit={1998: r"GoTo.com", 2002: r"Google's AdWords", 2007: r"Edelman, Ostrovsky and Schwarz; \ Varian"},
             scale=("firm", "market"), horizon=("a day",))
        self.history()
        self.board()
        self.vcg()
        self.practice()

    def history(self):
        rows = VGroup(
            label(r"1998: \ GoTo.com sells the places beside its search results, \ by auction, \ per click",
                  font_size=24),
            label(r"pay your own bid: \ advertisers outbid each other by a cent, \ then drop back, \ over and over",
                  font_size=23, color=FIRST),
            label(r"bids cycled in a sawtooth, \ changed by software many times an hour", font_size=23,
                  color=HOLD),
            label(r"2002: \ Google charges each advertiser the bid of the one below it, \ per click", font_size=24,
                  color=SECOND),
            label(r"the generalized second-price auction: \ soon the industry's standard", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Edelman, Ostrovsky and Schwarz, AER 97(1) (2007)", corner=DR, font_size=13)
        with self.voiceover(
            "Every advertisement beside a search result is placed by an auction, run while the page loads. "
            "<bookmark mark='a'/> The idea began in 1998 with a company called GoTo.com, which sold the places "
            "beside its results to the highest bidders, who paid per click. <bookmark mark='b'/> Each paid its own "
            "bid, and that made the bidding unstable. An advertiser would top a rival by a cent, then drop back to "
            "just above the one below, and the rival would do the same. <bookmark mark='c'/> With software doing the "
            "bidding, prices cycled in a sawtooth, many times an hour. <bookmark mark='d'/> In 2002 Google changed "
            "the rule: each advertiser pays, per click, the bid of the advertiser one place below. "
            "<bookmark mark='e'/> It is called the generalized second-price auction, and it became the industry's "
            "standard. It sounds like Vickrey's auction. It isn't."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def slots(self, g, center):
        ctrs = g["ctrs"]
        boxes = VGroup()
        for k, c in enumerate(ctrs):
            h = 0.55 + 0.6 * c / ctrs[0]
            r = RoundedRectangle(width=3.6, height=h + 0.15, corner_radius=0.08, stroke_color=GREY_B, stroke_width=2)
            t = label(rf"slot {k + 1}: \ {c:.0f} clicks", font_size=23, color=GREY_A).move_to(r)
            boxes.add(VGroup(r, t))
        boxes.arrange(DOWN, buff=0.18).move_to(center)
        return boxes

    def board(self):
        g = load("gsp")
        head = label(r"the island's notice board: \ three slots, \ four advertisers", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        boxes = self.slots(g, LEFT * 3.6 + DOWN * 0.2)
        who = VGroup(*[VGroup(islander(k, 0.6), label(rf"{v:.0f} a click", font_size=20,
                                                      color=island.CAST[k].color)).arrange(DOWN, buff=0.06)
                       for k, v in zip(NAMES, g["values"])]).arrange(RIGHT, buff=0.5)
        who.next_to(head, DOWN, buff=0.35).shift(RIGHT * 2.6)
        v = g["values"]
        c = g["ctrs"]
        side = VGroup(
            label(r"if all bid their values: \ Ana gets slot 1, \ and pays Bo's bid, \ 8 a click", font_size=21),
            label(rf"Ana's profit: \ {c[0]:.0f} $\times$ ({v[0]:.0f} $-$ {v[1]:.0f}) $=$ "
                  rf"{g['deviation_profits_top'][0]:.0f}", font_size=22, color=ANA),
            label(r"if Ana bids under 8 instead, \ she drops to slot 2, \ and pays Dara's 6", font_size=21),
            label(rf"profit: \ {c[1]:.0f} $\times$ ({v[0]:.0f} $-$ {v[2]:.0f}) $=$ "
                  rf"{g['deviation_profits_top'][1]:.0f}", font_size=22, color=HOLD),
            label(r"bidding your value is not best here: \ this is not Vickrey's auction", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(who, DOWN, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The island's notice board has three slots. The top one is seen most: it gets two hundred clicks a day, "
            "the second a hundred and twenty, the third sixty. <bookmark mark='a'/> Four advertisers want them. A "
            "click is worth ten shells to Ana, eight to Bo, six to Dara and four to Friday. "
            "<bookmark mark='b'/> Suppose everyone bids their value. Ana gets the top slot and pays Bo's bid, eight a "
            "click. <bookmark mark='c'/> Her profit is two hundred clicks times two: four hundred. "
            "<bookmark mark='d'/> But if Ana bids a little under eight, she falls to the second slot, and pays "
            "Dara's six. <bookmark mark='e'/> A hundred and twenty clicks times four is four hundred and eighty: "
            "more. <bookmark mark='f'/> So bidding your value is not the best thing to do. In Vickrey's auction it "
            "always is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(who))
            for mk, r in zip("bcdef", side):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def vcg(self):
        g = load("gsp")
        head = label(r"Vickrey's rule for slots: \ pay the harm you do to those below", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        hdr = [r"slot", r"clicks", r"all bid values: \ pay per click", r"Vickrey: \ pay per click",
               r"Vickrey: \ total"]
        rows_data = []
        for k in range(3):
            rows_data.append([rf"{k + 1}", rf"{g['ctrs'][k]:.0f}", rf"{g['truthful_pay'][k] / g['ctrs'][k]:.0f}",
                              rf"{g['gsp_price_per_click'][k]:.1f}", rf"{g['vcg_total'][k]:,.0f}"])
        xs = [-5.4, -3.6, -0.9, 2.4, 5.0]
        table = VGroup()
        for j, h in enumerate(hdr):
            table.add(label(h, font_size=20, color=GREY_B).move_to([xs[j], 2.0, 0]))
        cells = VGroup()
        for i, r in enumerate(rows_data):
            row = VGroup(*[label(t, font_size=28, color=[WHITE, GREY_A, FIRST, SECOND, SECOND][j]).move_to(
                [xs[j], 1.25 - 0.7 * i, 0]) for j, t in enumerate(r)])
            cells.add(row)
        expl = VGroup(
            label(r"slot 1's Vickrey price: \ Bo loses 80 clicks at 8, \ Dara 60 at 6, \ Friday 60 at 4: \ 1,240",
                  font_size=21, color=SECOND),
            label(r"Edelman, Ostrovsky and Schwarz; \ Varian (2007): \ the second-price auction for slots has an "
                  r"equilibrium", font_size=21),
            label(r"in which bidders shade, \ and each pays exactly Vickrey's price", font_size=21, color=E.ACCENT),
            label(r"the same revenue, \ by a different road: \ chapter five, \ again", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 1.75)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "What would Vickrey's rule be here? Each advertiser should pay the harm its presence does to the others. "
            "<bookmark mark='a'/> Ana, in the top slot, pushes Bo down from two hundred clicks to a hundred and "
            "twenty, Dara from a hundred and twenty to sixty, and Friday off the board. At their values, that costs "
            "them twelve hundred and forty shells: six point two a click. <bookmark mark='b'/> Here are Vickrey's "
            "prices for all three slots, beside what everyone would pay if all bid their values in the "
            "second-price auction for slots. <bookmark mark='c'/> In 2007 Benjamin Edelman, Michael Ostrovsky and "
            "Michael Schwarz, and separately Hal Varian, showed that the second-price auction for slots has an "
            "equilibrium in which bidders shade, <bookmark mark='d'/> and each ends up paying exactly Vickrey's "
            "price. <bookmark mark='e'/> The same revenue as Vickrey's auction, by a different road: chapter five's "
            "theorem, at work in the largest auction market in the world."
        ) as vo:
            self.play(FadeIn(head), FadeIn(table), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cells[0]), FadeIn(expl[0]))
            vo.wait_until("b")
            self.play(FadeIn(cells[1]), FadeIn(cells[2]))
            vo.wait_until("c")
            self.play(FadeIn(expl[1]))
            vo.wait_until("d")
            self.play(FadeIn(expl[2]), *[Indicate(cells[i][3], color=WHITE) for i in range(3)])
            vo.wait_until("e")
            self.play(FadeIn(expl[3]))
        self.clear_scene()

    def practice(self):
        rows = point_cards([
            (r"quality", r"bids weighted by \\ the chance of a click", SECOND),
            (r"reserves", r"a floor on every \\ keyword: \ chapter thirteen", RESERVE),
            (r"billions a day", r"each search \\ its own auction", PRICE),
            (r"display ads", r"moved to pay-your-bid \\ in 2019: \ chapter fifteen", FIRST),
        ], width=12.0, cols=2, font_size=23).move_to(DOWN * 0.2)
        head = label(r"the real thing", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The real auctions add more. <bookmark mark='a'/> Bids are weighted by the predicted chance that the "
            "advertisement is clicked, so that a slot goes to whoever is expected to pay the most for it, not just "
            "whoever bids the most per click. Every keyword has a reserve price, which chapter thirteen measures. "
            "There are billions of these auctions a day, one for each search. <bookmark mark='b'/> And the "
            "auctions for display advertisements on other websites moved from second price to pay-your-bid in 2019, "
            "for reasons chapter fifteen explains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[1:3]], lag_ratio=0.8), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[3], shift=UP * 0.1))
        self.clear_scene()
