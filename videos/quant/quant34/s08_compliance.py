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
        self.add(c)
        with self.voiceover('Chapter seven. Automated orders can create legal and operational problems. We review dated public cases and a proposed surveillance function. Order records and alerts support investigation; a diagram does not establish universal regulatory visibility or a deployed compliance system.'):
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
        self.add(rows[0], whys[0])
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
        self.add(g, cap[:2], ill)
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
        self.add(card)
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
        self.add(card)
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
        self.add(rows[0], whys[0])
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
        whys = [why('legitimate cancellations can be frequent; a high ratio alone does not establish abusive intent'),
                why('a possible investigation pattern; placement, executions, context and communications still need review'),
                why(r"surveillance produces alerts; people review them, with the order data and the trader's messages")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "A cancellation ratio alone cannot establish spoofing. <bookmark mark='a'/> Legitimate market making often cancels many quotes as conditions change. <bookmark mark='b'/> Repeated large orders, their placement and cancellation, executions on the other side, market context and communications can motivate investigation of intent. The pattern is neither a legal finding nor a calibrated probability of guilt. <bookmark mark='c'/> Review the complete record, alternative explanations and applicable rules. An alert requires assessment, and enforcement conclusions belong to the competent authorities."
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
        card = firm_card(r"SEBI and Jane Street, 2025 (allegations, contested)", "India's securities regulator issued an interim order in July 2025 alleging that Jane Street entities manipulated index levels on options-expiry days, barred them from its markets pending the case and impounded what it called unlawful gains of about Rs 4{,}840 crore; the firm disputed the findings, deposited the sum and was allowed to resume trading, as reported; this is a dated interim record; subsequent proceedings and current outcome are not verified here",
                         kind=r"The record", width=10.6, font_size=21).move_to(UP * 0.3)
        self.add(card)
        with self.voiceover(
            "A dated and contested example. <bookmark mark='a'/> SEBI's July 2025 interim order alleged index manipulation by Jane Street entities on options-expiry days and imposed restrictions and an impounding direction. The firm disputed the allegations; contemporary reports described a deposit and permission to resume trading. This panel recounts that historical interim record. It does not verify subsequent proceedings or assert the current legal outcome. The general question is how settlement-sensitive trading should be documented, reviewed and assessed under the relevant rules."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        cards = VGroup(
            desk_question(r"pre-approval", r"new strategies and new markets are reviewed for how they could look to a "
                          r"regulator, before they trade", width=12.4, font_size=26),
            desk_question(r"recorded and retained", r"orders, messages and calls are kept for years; the compliance desk "
                          r"reads samples, and every alert", width=12.4, font_size=26),
            desk_question(r"independent", r"compliance reports to the firm's leadership, not to the desks it watches, and "
                          r"can stop a strategy", width=12.4, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "A proposed compliance responsibility for the educational House. <bookmark mark='a'/> Review strategies, markets and controls before any authorized trading. <bookmark mark='b'/> Define order retention, alert handling, escalation and investigation records. <bookmark mark='c'/> Give the function independence, access and authority appropriate to the firm. These are design criteria. The lesson does not implement surveillance, certify legal compliance or authorize deployment."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('\\text{cancelled quotes}/\\text{submitted quotes}=0.98\\quad\\not\\Rightarrow\\quad\\text{spoofing finding}', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Investigate order size, placement and duration, opposite-side fills, market conditions and communications. A pattern or alert does not by itself establish intent or a violation.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. A market maker cancels ninety-eight percent of submitted quotes. Why is that alone insufficient to establish spoofing? What order patterns and contextual evidence would warrant investigation, and what remains to be shown?'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
