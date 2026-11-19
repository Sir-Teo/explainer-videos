from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ insurance, \ underwriting \ and trust", r"How do insurers, \ lenders and "
             r"platforms live with what they can't see?", "Chapter fourteen. In practice: insurance, underwriting and "
             "trust.", lit={2011: r"Test-Achats"}, scale=("person", "firm", "nation"), horizon=("a year",))
        self.underwriting()
        self.limits()
        self.kit()

    def underwriting(self):
        rows = VGroup(
            label(r"underwriting: \ price on everything you can observe, \ so that less is left hidden", font_size=24),
            label(r"car insurance: \ age, \ address, \ the car, \ the driving record, \ and in many places a credit "
                  r"score", font_size=23, color=SIGNAL),
            label(r"telematics: \ a box or an app that records how you drive, \ chosen mostly by careful drivers",
                  font_size=23, color=GOOD),
            label(r"which is itself a signal: \ agreeing to be watched tells the insurer something", font_size=23,
                  color=GREY_A),
            label(r"annuities: \ the people who buy a pension for life \ tend to live longer than those who don't",
                  font_size=23, color=LEMON),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Finkelstein and Poterba, JPE 112(1) (2004)", corner=DR, font_size=13)
        with self.voiceover(
            "In practice, insurers' first response to hidden information is to observe more. "
            "<bookmark mark='a'/> Underwriting prices on everything that can be seen, so that less is left hidden. "
            "<bookmark mark='b'/> A car insurer prices on age, address, the car and the driving record, and in many "
            "places on a credit score, which turns out to predict claims. <bookmark mark='c'/> Telematics goes further: "
            "a box or an app records how you drive, and it is chosen mostly by careful drivers. "
            "<bookmark mark='d'/> Which is itself a signal: agreeing to be watched tells the insurer something. "
            "<bookmark mark='e'/> Selection shows up wherever people know their own risk. Amy Finkelstein and James "
            "Poterba found that in Britain, people who buy annuities, pensions paid for life, tend to live longer than "
            "those who don't."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def limits(self):
        hc = history_card(2011, r"Test-Achats, \ the European Court of Justice", r"insurers in the European Union may "
                          r"not charge men and women different premiums: \\ from 21 December 2012, \ one price for "
                          r"both", color=POOL, width=11.4, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"society sometimes forbids what is observable: \ sex, \ genes, \ in some places credit scores",
                  font_size=23),
            label(r"each ban turns an observable difference into a hidden one: \ pooling by law", font_size=23,
                  color=POOL),
            label(r"young men's car insurance got cheaper, \ young women's dearer", font_size=23, color=GREY_A),
            label(r"the trade-off of Part 18: \ what is fair to price on, \ against what selection costs", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.34).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"Association Belge des Consommateurs Test-Achats, C-236/09 (1 March 2011)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Sometimes society forbids insurers to use what they can see. <bookmark mark='a'/> In the Test-Achats case "
            "of 2011, the European Court of Justice ruled that from December 2012 insurers in the European Union could "
            "no longer charge men and women different premiums. <bookmark mark='b'/> Bans like this, on sex, on genes, "
            "in some places on credit scores, turn an observable difference into a hidden one: pooling by law. "
            "<bookmark mark='c'/> Prices converged, so that insurance for young male drivers became cheaper relative "
            "to young women's. <bookmark mark='d'/> Whether that is fair, and what the selection it invites costs, is "
            "the kind of trade-off Part eighteen, on social choice, makes explicit."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def kit(self):
        rows = point_cards([
            (r"the diagram", r"estimate demand and \\ cost from price variation", LOSS),
            (r"the test", r"cover against claims, \\ given the price", SIGNAL),
            (r"menus", r"deductibles that sort \\ the careful from the rest", GOOD),
            (r"risk adjustment", r"formulas that pay \\ for sicker members", USED),
            (r"credit scoring", r"screening without \\ raising the rate", POOL),
            (r"platform trust", r"reviews, \ escrow, \\ guarantees", LEMON),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.1)
        head = label(r"the information economist's kit", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"social insurance: \ Part 42; \ platforms: \ Part 61; \ incentives inside the contract: \ Part 14",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the kit an economist brings to these markets. <bookmark mark='a'/> The Einav-Finkelstein diagram, "
            "estimated from variation in prices. The positive-correlation test, given what the insurer prices on. "
            "Menus of deductibles that sort the careful from the rest, as Rothschild and Stiglitz predicted. "
            "Risk-adjustment formulas that pay insurers more for sicker members. Credit scores, which let lenders "
            "screen without raising the rate. And the machinery of platform trust: reviews, escrow and guarantees. "
            "<bookmark mark='b'/> Part forty-two takes up social insurance, Part sixty-one platforms, and the next "
            "part the incentives written into contracts."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in rows.cards], lag_ratio=0.6), run_time=14)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
