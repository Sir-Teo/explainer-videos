from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, PLAT_C, PM_C, fit_right


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.money()
        self.prop()
        self.makers()
        self.pfof()
        self.platforms()
        self.systematic()
        self.banks()
        self.china()
        self.compare()
        self.question()

    def card(self):
        c = chapter_card(1, r"Six ways to be a quant firm", r"Whose money, which edge, and who gets paid?", part=PART)
        self.add(c)
        with self.voiceover("Chapter one. Every quant firm answers three questions: whose money it trades, what edge it "
                            "sells, and who is paid when it works. Six answers cover most of the industry."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def money(self):
        rows = [cmath(r"\text{P\&L}", r"=", r"\text{edge} \times \text{capacity} - \text{costs}", font_size=36,
                      colors={r"\text{edge}": GOOD}),
                cmath(r"\text{own capital}", r":", r"\text{keep all of it, bear all of the risk}", font_size=32,
                      colors={r"\text{own capital}": FIRM_C}),
                cmath(r"\text{outside capital}", r":", r"\text{fees: a share of assets and of profits}", font_size=32,
                      colors={r"\text{outside capital}": PLAT_C})]
        whys = [why(r"Part 31: an edge has a capacity, and costs grow with size; the firm's size is chosen where the "
                    r"marginal dollar stops paying"),
                why(r"proprietary traders and market makers trade the partners' own money"),
                why(r"funds and platforms trade investors' money and are paid fees; their size is set by fees as well as "
                    r"by edge")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The economics in one line. <bookmark mark='a'/> Profit is edge times capacity, less costs, and Part "
            "thirty-one showed that capacity is finite. <bookmark mark='b'/> A firm that trades its own capital keeps "
            "all the profit and bears all the risk. <bookmark mark='c'/> A firm that trades investors' capital is paid "
            "fees, a share of assets and of profits, and that changes how large it wants to be."
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

    def prop(self):
        a = firm_card(r"Proprietary trading", r"Jane Street (founded 2000), Hudson River Trading (2002), Jump Trading "
                      r"(1999), XTX Markets (2015): the partners' own capital, traded across thousands of instruments, "
                      r"mostly by quoting and by very short-horizon prediction", width=6.2, font_size=20)
        b = firm_card(r"What they sell", r"immediacy: a price to anyone who wants to trade now, in ETFs, options, bonds, "
                      r"currencies and futures; the profit is the spread earned, less what informed traders take and "
                      r"what the exchange charges", kind=r"The edge", width=6.2, font_size=20)
        cards = VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "First, proprietary trading firms. <bookmark mark='a'/> Jane Street, Hudson River Trading, Jump Trading and "
            "XTX Markets trade their partners' own capital across thousands of instruments, mostly by quoting prices "
            "and by predicting the next few seconds or minutes. <bookmark mark='b'/> What they sell is immediacy, Part "
            "thirty-three's word: a price for anyone who wants to trade now. They keep the spread, less what better-"
            "informed traders take from them, less the exchange's fees. Part thirty-eight builds the model."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def makers(self):
        a = firm_card(r"Market makers", r"Citadel Securities (2002), Virtu Financial (2008; listed 2015), Optiver (1986): "
                      r"designated or electronic market making on exchanges, and wholesale execution of retail orders "
                      r"bought from brokers", width=6.2, font_size=20)
        b = firm_card(r"What is public", r"Virtu is a listed company, so its revenue, its trading days and its costs "
                      r"are in its filings; most of the others disclose only through bond offerings, court cases and "
                      r"regulators' orders", kind=r"The record", width=6.2, font_size=20)
        cards = VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Second, the market makers, overlapping with the first. <bookmark mark='a'/> Citadel Securities, Virtu and "
            "Optiver make markets on exchanges, and some execute retail orders that brokers route to them. "
            "<bookmark mark='b'/> Virtu is listed, so its revenue and its trading days are in public filings; Chapter "
            "two reads one of them. Most of the rest disclose only through bond offerings, court cases and regulators' "
            "orders."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pfof(self):
        cards = VGroup(
            desk_question(r"payment for order flow", r"in the US, wholesale market makers pay retail brokers for their "
                          r"customers' orders, which are less likely to be informed and so cheaper to trade against; the "
                          r"broker can then offer commission-free trading", width=12.4, font_size=26),
            desk_question(r"the conflict", r"the broker must still seek best execution for its customer, while being paid "
                          r"by the firm that fills the order; the SEC requires the payments to be disclosed", width=12.4,
                          font_size=26),
            desk_question(r"elsewhere", r"the UK's regulator treated the practice as incompatible with its rules from "
                          r"2012, and the EU agreed in its 2024 market reforms to phase it out by mid-2026", width=12.4,
                          font_size=26),
        ).arrange(DOWN, buff=0.25)
        head = label(r"One part of market making deserves its own card", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(head, cards[0])
        with self.voiceover(
            "One part of the market-making business deserves its own card. <bookmark mark='a'/> In the United States, "
            "wholesale market makers pay retail brokers for their customers' orders. Retail orders are less likely to "
            "be informed, so they are cheaper to trade against, and the payment lets brokers offer trading without "
            "commission. <bookmark mark='b'/> The conflict: the broker owes its customer the best execution, while being "
            "paid by the firm that fills the order, and the payments must be disclosed. <bookmark mark='c'/> Elsewhere "
            "the answer differs: Britain's regulator treated the practice as incompatible with its rules from 2012, and "
            "the European Union agreed to phase it out by mid-2026."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def platforms(self):
        a = firm_card(r"Multi-manager platforms", r"Millennium (1989), Citadel (1990), Balyasny (2001), Point72 (2014): "
                      r"hundreds of independent teams, each with its own capital, risk limits and drawdown stops, under "
                      r"one central risk desk", width=6.2, font_size=20)
        b = firm_card(r"How they are paid", r"as reported, many charge investors pass-through fees: the platform's costs, "
                      r"including the teams' pay, are passed to the fund, with a performance fee on top; Chapter 3 "
                      r"simulates what that leaves", kind=r"The fees", width=6.2, font_size=20)
        cards = VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Third, the multi-manager platforms. <bookmark mark='a'/> Millennium, Citadel, Balyasny and Point72 run "
            "hundreds of independent teams, called pods, each with its own capital, its own risk limits and its own "
            "drawdown stops, under one central risk desk. <bookmark mark='b'/> As reported, many charge investors "
            "pass-through fees: the platform's costs, including what it pays its teams, are charged to the fund, with a "
            "performance fee on top. Chapter three simulates what that leaves for the investors."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def systematic(self):
        a = firm_card(r"Systematic funds", r"Renaissance (1982), D. E. Shaw (1988), AQR (1998), Two Sigma (2001), Man "
                      r"Group's AHL (1987): one research process and one book, or a few, run by models across asset "
                      r"classes", width=6.2, font_size=20)
        b = firm_card(r"The spectrum", r"from fast statistical arbitrage to slow factor and trend books (Parts 24, 32, 33); "
                      r"fees range from a few tenths of a percent for factor funds to the 5\% and 44\% reported for "
                      r"Medallion", kind=r"The range", width=6.2, font_size=20)
        cards = VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Fourth, the systematic funds. <bookmark mark='a'/> Renaissance, D. E. Shaw, AQR, Two Sigma and Man Group's "
            "AHL run one research process across many models and asset classes. <bookmark mark='b'/> They span the "
            "range of this series: fast statistical arbitrage, slower factor and trend books. Their fees span it too, "
            "from a few tenths of a percent for a factor fund to the five percent of assets and forty-four percent of "
            "profits reported for Renaissance's Medallion."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def banks(self):
        a = firm_card(r"Bank desks", r"banks still make electronic markets and sell quantitative index strategies to "
                      r"clients; their proprietary trading was restricted by the Volcker rule of the Dodd--Frank Act, and "
                      r"several prop groups left, Morgan Stanley's PDT in 2012", width=6.2, font_size=20)
        b = firm_card(r"What changed", r"a bank's balance sheet is funded cheaply and regulated heavily: capital rules "
                      r"(Part 21) price every position, so banks keep the client flow and the independent firms took "
                      r"the risk-taking", kind=r"The shift", width=6.2, font_size=20)
        cards = VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Fifth, the banks. <bookmark mark='a'/> Banks still make electronic markets and sell quantitative index "
            "strategies to clients, but the Volcker rule restricted their proprietary trading, and several prop groups "
            "left, Morgan Stanley's PDT in 2012 among them. <bookmark mark='b'/> A bank's balance sheet is cheap to fund "
            "but heavily regulated, and Part twenty-one's capital rules put a price on every position, so the banks kept "
            "the client business and the independent firms took the risk."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def china(self):
        a = firm_card(r"China's quant private funds", r"privately offered funds trading A-shares, index futures "
                      r"and commodities, many founded in the 2010s; the largest manage tens of billions of yuan, as "
                      r"reported, with products sold as index enhancement against the CSI 500 and 1000", width=6.2,
                      font_size=20)
        b = firm_card(r"The rules there", r"T+1 settlement, limited shorting, price limits; February 2024's small-cap "
                      r"drawdown (Part 29) and the regulators' new limits on high-frequency and DMA trading that "
                      r"followed, as reported", kind=r"The constraints", width=6.2, font_size=20)
        cards = VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Sixth, China's quant private funds. <bookmark mark='a'/> Privately offered funds trading A-shares, index "
            "futures and commodities, many founded in the 2010s, the largest managing tens of billions of yuan, as "
            "reported, and selling index enhancement: beating the CSI 500 or 1000 index. <bookmark mark='b'/> They work "
            "under different constraints: next-day settlement, limited shorting, daily price limits, and, after the "
            "small-cap drawdown of February 2024 from Part twenty-nine, new limits on high-frequency and direct market "
            "access trading, as reported."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def compare(self):
        hx = [-4.6, -1.6, 1.4, 4.4]
        head = VGroup(label(r"model", font_size=17, color=GREY_B), label(r"whose capital", font_size=17, color=GREY_B),
                      label(r"the edge sold", font_size=17, color=GREY_B), label(r"horizon", font_size=17, color=GREY_B))
        data = [(r"proprietary trading", r"partners'", r"immediacy, prediction", r"seconds to days"),
                (r"market making", r"own", r"immediacy", r"seconds"),
                (r"multi-manager", r"investors'", r"many small edges", r"days to months"),
                (r"systematic fund", r"investors' (or own)", r"premia, signals", r"days to years"),
                (r"bank desk", r"bank's, regulated", r"client flow", r"minutes to days"),
                (r"China quant fund", r"investors'", r"index enhancement", r"days")]
        tab = VGroup(head)
        for row in data:
            tab.add(VGroup(*[label(c, font_size=18, color=WHITE if i else FIRM_C) for i, c in enumerate(row)]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.7 * j, 0])
        self.add(tab[0], tab[1])
        with self.voiceover(
            "Side by side. <bookmark mark='a'/> Whose capital, what edge, and how long a position lasts. The rest of the "
            "part is about the machinery common to all six: how capital is given to traders and taken away, how ideas "
            "become capital, and how the firm keeps its traders inside the rules."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('R_{\\rm classic}=(0.10-0.02)(1-0.20),\\quad R_{\\rm platform}=(0.10-0.06)(1-0.20)', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('One period; fees on initial capital, then 20\\% of remaining positive profit. No timing or high-water-mark effects. Which leaves more at equal gross return?', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. At ten percent gross, compare a two-percent capital fee then twenty percent of remaining profit with six-percent costs then the same profit share. Assume positive eligible profit and one period. Which investor return is higher?'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
