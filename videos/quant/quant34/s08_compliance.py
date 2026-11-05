from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, LAW_C, PART, fit_right, illustration


class Compliance(VoiceoverScene):
    def construct(self):
        self.card()
        self.abuses()
        self.spoof_book()
        self.sarao()
        self.jpm()
        self.cat()
        self.detect()
        self.india()
        self.desk()
        self.question()

    def card(self):
        c = chapter_card(7, r"Surveillance and the cases", r"Which trading is illegal, and how is it caught?", part=PART)
        with self.voiceover("Chapter seven. An algorithm can break the law as easily as a person, and faster. Every firm "
                            "runs a compliance function that watches its own orders, and every regulator now has the data "
                            "to watch everyone's."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def abuses(self):
        rows = [cmath(r"\text{spoofing}", r":", r"\text{orders placed with the intent to cancel them}", font_size=32,
                      colors={r"\text{spoofing}": LAW_C}),
                cmath(r"\text{layering}", r":", r"\text{many such orders at several price levels}", font_size=32,
                      colors={r"\text{layering}": LAW_C}),
                cmath(r"\text{marking the close}", r":", r"\text{trading to move a closing or settlement price}",
                      font_size=32, colors={r"\text{marking the close}": LAW_C}),
                cmath(r"\text{wash trades}", r":", r"\text{trading with oneself to fake volume}", font_size=32,
                      colors={r"\text{wash trades}": LAW_C})]
        whys = [why(r"made explicitly illegal in US futures markets by the Dodd--Frank Act of 2010: bidding or offering "
                    r"with the intent to cancel before execution"),
                why(r"the visible orders suggest pressure on one side, while the trader executes on the other"),
                why(r"many contracts, options and funds settle on a closing price; moving it moves their value"),
                why(r"volume attracts other traders and earns rebates; fake volume is fraud")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The abuses an algorithm can commit. <bookmark mark='a'/> Spoofing: placing orders you intend to cancel "
            "before they trade, made explicitly illegal in American futures markets by the Dodd-Frank Act. "
            "<bookmark mark='b'/> Layering: many such orders, stacked at several prices, to suggest pressure on one "
            "side while you trade on the other. <bookmark mark='c'/> Marking the close: trading to move a price that "
            "contracts settle on. <bookmark mark='d'/> And wash trades: trading with yourself to fake volume."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def spoof_book(self):
        prices = np.arange(99.95, 100.06, 0.01)
        bid_q = {99.95: 6, 99.96: 5, 99.97: 6, 99.98: 4, 99.99: 3}
        ask_q = {100.01: 3, 100.02: 4, 100.03: 5, 100.04: 6, 100.05: 5}
        spoof = {99.97: 18, 99.96: 20, 99.95: 22}
        g = VGroup()
        bars, sbars, labs = VGroup(), VGroup(), VGroup()
        for p in prices:
            p = round(float(p), 2)
            y = (p - 100.0) * 50
            if p in bid_q:
                bars.add(Rectangle(width=0.2 * bid_q[p], height=0.36, fill_color=GOOD, fill_opacity=0.6, stroke_width=0)
                         .move_to([-0.1 * bid_q[p] - 0.2, y, 0]))
            if p in ask_q:
                bars.add(Rectangle(width=0.2 * ask_q[p], height=0.36, fill_color=BAD, fill_opacity=0.6, stroke_width=0)
                         .move_to([0.1 * ask_q[p] + 0.2, y, 0]))
            if p in spoof:
                sbars.add(Rectangle(width=0.2 * spoof[p], height=0.36, fill_color=LAW_C, fill_opacity=0.7, stroke_width=0)
                          .move_to([-0.1 * spoof[p] - 0.2 - 0.2 * bid_q[p], y, 0]))
            if p in bid_q or p in ask_q:
                labs.add(MathTex(f"{p:.2f}", font_size=20).move_to([0, y, 0]))
        g.add(bars, labs)
        whole = VGroup(g, sbars)
        whole.shift(RIGHT * 1.0 - g.get_center())
        cap = VGroup(label(r"bids", font_size=18, color=GOOD), label(r"offers", font_size=18, color=BAD),
                     label(r"orders meant to be cancelled", font_size=18, color=LAW_C))
        cap.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.5)
        sell = label(r"meanwhile: the trader sells at the offer, to buyers drawn in by the apparent demand", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        ill = illustration(r"illustration: a stylised order book")
        with self.voiceover(
            "What it looks like in the order book. <bookmark mark='a'/> Bids on the left, offers on the right. "
            "<bookmark mark='b'/> A layering trader stacks large bids below the market, which look like demand. "
            "<bookmark mark='c'/> Buyers, reading the book, raise their prices, and the trader sells to them. Then the "
            "large bids are cancelled, never having been meant to trade. The pattern is the signature surveillance "
            "looks for: large orders, quickly cancelled, opposite to the trader's executions."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cap[:2]), FadeIn(ill))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, RIGHT) for b_ in sbars], lag_ratio=0.2), FadeIn(cap[2]))
            vo.wait_until("c")
            self.play(FadeIn(sell))
            self.play(FadeOut(sbars))
        self.wait(0.4)
        self.clear_scene()

    def sarao(self):
        card = crisis_card(r"2010--2020", r"Navinder Sarao", body=r"a trader working from his parents' home near London "
                           r"was charged in the US in 2015 with spoofing E-mini S\&P 500 futures, including on the day of "
                           r"the 6 May 2010 flash crash; he pleaded guilty in 2016 to spoofing and wire fraud and was "
                           r"sentenced in 2020 to a year of home confinement, credited with his cooperation",
                           width=10.6, font_size=22).move_to(UP * 0.3)
        with self.voiceover(
            "The cases, from court records. <bookmark mark='a'/> Navinder Sarao, a trader working from his parents' home "
            "near London, was charged in the United States in 2015 with spoofing the E-mini futures, including on the "
            "day of the 2010 flash crash. He pleaded guilty in 2016, cooperated, and in 2020 was sentenced to a year of "
            "home confinement. Regulators have not said his orders caused the crash; the charge was the spoofing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def jpm(self):
        card = crisis_card(r"September 2020", r"J.P. Morgan", body=r"the bank agreed to pay about \$920 million to the CFTC, "
                           r"the Justice Department and the SEC to resolve spoofing by traders on its precious-metals and "
                           r"Treasury desks over about eight years; several traders were later convicted at trial",
                           stats=((r"\$920\text{m}", r"the resolution, a record for spoofing"),), width=10.6,
                           font_size=22).move_to(UP * 0.3)
        with self.voiceover(
            "And at the largest scale. <bookmark mark='a'/> In September 2020, J.P. Morgan agreed to pay about nine "
            "hundred and twenty million dollars to three American agencies to resolve spoofing by traders on its "
            "precious-metals and Treasury desks over about eight years. Several of the traders were later convicted at "
            "trial. Spoofing is not a small-trader's crime."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def cat(self):
        rows = [cmath(r"\text{the CAT}", r":", r"\text{every order, quote, cancel and trade, by customer}", font_size=32,
                      colors={r"\text{the CAT}": LAW_C}),
                cmath(r"\text{exchanges}", r":", r"\text{their own surveillance of their own books}", font_size=32),
                cmath(r"\text{the firm}", r":", r"\text{its own surveillance of its own orders}", font_size=32,
                      colors={r"\text{the firm}": FIRM_C})]
        whys = [why(r"the SEC's Consolidated Audit Trail (Rule 613, adopted 2012; reporting from 2020): one record of the "
                    r"US equity and options markets' life cycle of orders"),
                why(r"each exchange and futures market watches for abuse on its own venue"),
                why(r"and the law expects a firm to catch its own traders and algorithms first")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Who watches. <bookmark mark='a'/> In American equities and options, the SEC's Consolidated Audit Trail "
            "records the whole life of every order, by customer, with reporting since 2020. "
            "<bookmark mark='b'/> Each exchange watches its own book. <bookmark mark='c'/> And the firm is expected to "
            "catch its own traders and algorithms first, which is the compliance desk this part adds to the House."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def detect(self):
        rows = [cmath(r"\text{cancel ratio}", r"=", r"\frac{\text{cancelled quantity}}{\text{executed quantity}}",
                      font_size=34),
                cmath(r"\text{opposite-side test}", r":", r"\text{large cancels on one side, fills on the other, within seconds}",
                      font_size=28),
                cmath(r"\text{an alert}", r"\neq", r"\text{a violation}", font_size=36, colors={r"\text{an alert}": HURDLE})]
        whys = [why(r"market makers cancel almost every quote, legitimately; the ratio alone flags everyone"),
                why(r"the pattern of intent: size and cancels that move with the trader's own executions"),
                why(r"surveillance produces alerts; people review them, with the order data and the trader's messages")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How surveillance looks for it. <bookmark mark='a'/> The cancel ratio alone flags everyone, because market "
            "makers legitimately cancel almost every quote. <bookmark mark='b'/> So the test is for intent: large orders "
            "cancelled on one side, moving in step with fills on the other, within seconds. <bookmark mark='c'/> And an "
            "alert is not a violation: people review it, with the order data and, often, the trader's own messages, "
            "which is how most of the cases were proved."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def india(self):
        card = firm_card(r"SEBI and Jane Street, 2025 (allegations, contested)", r"India's securities regulator issued an "
                         r"interim order in July 2025 alleging that Jane Street entities manipulated index levels on "
                         r"options-expiry days, barred them from its markets pending the case and impounded what it called "
                         r"unlawful gains of about Rs 4{,}840 crore; the firm disputed the findings, deposited the sum and "
                         r"was allowed to resume trading, as reported; the matter is not decided",
                         kind=r"The record", width=10.6, font_size=21).move_to(UP * 0.3)
        with self.voiceover(
            "And a case not yet decided. <bookmark mark='a'/> In July 2025, India's securities regulator issued an "
            "interim order alleging that Jane Street entities had manipulated index levels on options-expiry days, "
            "barred them from its markets pending the case, and impounded what it called unlawful gains. The firm "
            "disputed the findings, deposited the sum and, as reported, was allowed to resume trading. These are "
            "allegations, contested, and undecided; the question they raise for every firm is where hedging and "
            "liquidity provision end and influencing a settlement price begins."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        cards = VGroup(
            desk_question(r"pre-approval", r"new strategies and new markets are reviewed for how they could look to a "
                          r"regulator, before they trade", width=12.4, font_size=19),
            desk_question(r"recorded and retained", r"orders, messages and calls are kept for years; the compliance desk "
                          r"reads samples, and every alert", width=12.4, font_size=19),
            desk_question(r"independent", r"compliance reports to the firm's leadership, not to the desks it watches, and "
                          r"can stop a strategy", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The compliance desk the House adds. <bookmark mark='a'/> New strategies and markets are reviewed for how "
            "they could look to a regulator, before they trade. <bookmark mark='b'/> Orders and messages are recorded, "
            "kept, sampled, and every alert reviewed. <bookmark mark='c'/> And the desk is independent: it reports to the "
            "firm's leadership, not to the desks it watches, and it can stop a strategy."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a market maker cancels 98\% of its quotes. Is that evidence of spoofing? What additional pattern "
                       r"would be?")
        with self.voiceover(
            "Pause and predict. A market maker cancels ninety-eight percent of its quotes. Is that evidence of spoofing? "
            "What additional pattern would be?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
