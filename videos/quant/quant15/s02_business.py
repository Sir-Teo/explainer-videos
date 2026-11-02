from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, CASH, GOOD, IV, OPT, PART, SPOT


class Business(VoiceoverScene):
    def construct(self):
        self.card()
        self.anatomy()
        self.players()

    def card(self):
        c = chapter_card(1, r"The structuring business", r"Who sells a structured note, and who buys it?", part=PART)
        with self.voiceover("Chapter one. The structuring business."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def anatomy(self):
        rows = [cmath(r"\text{note}", r"=", r"\text{zero-coupon bond} + \text{options}", font_size=40,
                      colors={r"\text{note}": OPT}),
                cmath(r"\text{price}", r"=", r"\text{fair value} + \text{issuer's margin}", font_size=40,
                      colors={r"\text{price}": IV}),
                cmath(r"\text{issuer}", r"\Rightarrow", r"\text{hedges the options it is short, or long, every day}",
                      font_size=36, colors={r"\text{issuer}": BAD})]
        whys = [why(r"every structured note is a bond plus a package of options, sold as one security; the options are "
                    r"what make the coupon high or the downside protected"),
                why(r"the buyer cannot see the parts or their prices; the issuer can, and keeps the difference: about 8\% "
                    r"on Morgan Stanley's US notes, 2001--2005 (Henderson and Pearson 2011)"),
                why(r"the bank issuing the note takes the other side of the options and runs the hedge: Parts 10 to 14, for "
                    r"products nobody can trade back")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-1.2, buff=0.9, edge=6.9)
        with self.voiceover(
            "A structured note is a bond and a package of options, sold as a single security. The options are what "
            "make it attractive: a high coupon, or protection on the downside, or a payoff that tracks an index the "
            "buyer cannot otherwise reach. <bookmark mark='a'/> The buyer sees one price. The issuer sees the parts, "
            "and keeps the difference between the price and their fair value. Brian Henderson and Neil Pearson priced a "
            "family of Morgan Stanley's retail notes, sold from 2001 to 2005, and found them priced about eight percent "
            "above fair value. "
            "<bookmark mark='b'/> And the bank that issues the note takes the other side of every option in it, and "
            "hedges it every day, for a product that nobody can trade back. Everything in Parts ten to fourteen, "
            "applied to payoffs with memory."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def players(self):
        cards = VGroup(
            firm_card(r"Buyers", r"Savers and wealthy individuals looking for yield above deposits, usually through a bank, "
                      r"a broker or a private fund. In low-rate years, European banks raised the headline rates of their "
                      r"retail products by making them more complex (C\'el\'erier and Vall\'ee 2017).",
                      source=r"Q.J.E. 2017", width=6.0, font_size=21),
            firm_card(r"Issuers", r"Investment banks in Europe and the US; securities firms and banks in Korea; in China, "
                      r"the OTC derivatives desks of brokers, which sold snowballs through private funds to qualified "
                      r"investors. Each issuer is short the exotic it sold, and hedges it in the futures and options "
                      r"markets.", source=r"public record", width=6.0, font_size=21),
        ).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(UP * 0.2)
        foot = wrapped_label(r"the risk that stays with the issuer is crowded: thousands of notes with the same index, the same "
                             r"barriers and similar dates, hedged by a handful of desks that must trade in the same direction "
                             r"at the same moment (chapters 5 and 6)", 11.8, 20, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Who are the players? On one side, savers and wealthy individuals looking for more than a deposit pays, "
            "buying through their bank, a broker or a private fund. Claire Célérier and Boris Vallée found European "
            "banks raising the headline rates of retail products, when rates were low, by making them more complex. "
            "<bookmark mark='a'/> On the other side, the issuers: investment banks in Europe and the US, securities "
            "firms and banks in Korea, and in China the over-the-counter desks of brokers. Each is short the exotic it "
            "sold. <bookmark mark='b'/> And the risk that stays with them is crowded: thousands of notes on the same "
            "index, with the same barriers, hedged by a handful of desks that must trade in the same direction at the "
            "same moment."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
