from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import ASK_C, BAD, BID_C, DEALER_C, FLOW_C, GOOD, HURDLE, PART, PRICE_C


class Structure(VoiceoverScene):
    def construct(self):
        self.card()
        self.nms()
        self.fees()
        self.venues()
        self.dark()
        self.routing()
        self.rules2024()
        self.auctions()
        self.settle()
        self.journey()
        self.question()

    def card(self):
        c = chapter_card(8, r"Market structure: the plumbing", r"Where does an order to buy a US stock actually go?",
                         part=PART)
        self.add(c)
        with self.voiceover("Chapter eight. The models so far had one dealer and one market. An American stock trades on "
                            "more than a dozen exchanges and dozens of off-exchange venues, linked by rules. The rules "
                            "decide who meets whom, and at what price."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def nms(self):
        rows = [cmath(r"\text{historical protection}", r":", r"\text{qualifying quotes; exceptions apply}", font_size=32, colors={r"\text{historical protection}": PRICE_C}),
                cmath(r"\text{access}", r":", r"\text{fair access to quotes; fees capped}", font_size=30,
                      colors={r"\text{access}": PRICE_C}),
                cmath(r"\text{historical tick}", r":", r"\text{usually 1 cent for }p\ge\$1", font_size=32, colors={r"\text{historical tick}": PRICE_C}),
                cmath(r"\text{NBBO}", r"=", r"\text{the best bid and offer across all exchanges}", font_size=30,
                      colors={r"\text{NBBO}": GOOD})]
        whys = [why('historical 2005 framework: Rule 611 protects qualifying automated displayed quotations, with specified exceptions; this is not a universal routing mandate'),
                why(r"and every venue must let others reach its quotes, at a capped fee"),
                why(r"the tick: a minimum price increment that, for a cheap stock, can be wider than its natural spread"),
                why(r"the national best bid and offer, the reference every broker's execution is judged against")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "A historical outline of the 2005 US framework. <bookmark mark='a'/> The order-protection rule restricts trade-throughs of qualifying protected quotations, with exceptions; it does not protect every displayed order or dictate every routing decision. <bookmark mark='b'/> Access rules and fee caps apply within their defined scope. <bookmark mark='c'/> The original sub-penny framework generally used a cent at prices of at least a dollar, subject to exceptions and later amendments. <bookmark mark='d'/> The national best bid and offer is a reference, not a complete measure of execution quality. This lesson does not verify the current legal regime or compliance dates."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def fees(self):
        rows = [cmath(r"\text{maker}", r":", r"\text{posts a limit order: earns a rebate}", font_size=32,
                      colors={r"\text{maker}": BID_C}),
                cmath(r"\text{taker}", r":", r"\text{crosses the spread: pays a fee}", font_size=32,
                      colors={r"\text{taker}": ASK_C}),
                cmath('\\text{taker round trip}', r"=", '\\text{quoted spread} + f_{\\rm buy}+f_{\\rm sell}', font_size=32)]
        whys = [why(r"maker-taker pricing pays liquidity providers a fraction of a cent per share"),
                why(r"and charges those who remove liquidity, up to the cap"),
                why('for a taker round trip add both access fees to the quoted spread; maker rebates are a separate schedule, and inverted venues can reverse signs')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Specify the participant. <bookmark mark='a'/> In a conventional maker-taker schedule, a passive fill may receive a rebate. <bookmark mark='b'/> An aggressive fill may pay a separately specified access fee. A maker rebate does not determine that taker fee. <bookmark mark='c'/> A taker round trip crosses the quoted spread and pays both taker fees, as displayed. A maker's bid-to-ask gross revenue instead adds any rebates before adverse selection and inventory costs. Inverted schedules change the fee signs. There is no participant-independent spread-minus-rebate cost formula, and fill probability and queueing remain important."
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

    def venues(self):
        cards = VGroup(
            desk_question(r"exchanges", r"lit order books, displayed quotes, the NBBO; their auctions set the opening "
                          r"and closing prices", width=12.4, font_size=25),
            desk_question(r"dark pools", r"alternative trading systems with no displayed quotes, usually matching at the "
                          r"midpoint; they let large orders hide, Kyle's insider's wish", width=12.4, font_size=25),
            desk_question(r"wholesalers", r"retail orders bought from brokers (Part 34) and filled internally, often "
                          r"slightly better than the NBBO; with dark pools, off-exchange trading has been around half of "
                          r"US equity volume, as reported", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Where orders go. <bookmark mark='a'/> Exchanges: displayed order books, which set the national best quotes "
            "and run the opening and closing auctions. <bookmark mark='b'/> Dark pools: venues with no displayed quotes, "
            "usually matching at the midpoint, where a large order can hide, which is Kyle's insider's wish. "
            "<bookmark mark='c'/> And wholesalers, who buy retail orders from brokers and fill them themselves, often "
            "slightly better than the best quote. Together, off-exchange trading has been around half of American "
            "equity volume, as reported."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def dark(self):
        rows = [cmath(r"\text{dark pool}", r":", r"\text{midpoint price, but no guarantee of a fill}", font_size=32,
                      colors={r"\text{dark pool}": DEALER_C}),
                cmath(r"\text{informed orders}", r":", r"\text{cluster on one side} \Rightarrow \text{rarely filled in the dark}",
                      font_size=30, colors={r"\text{informed orders}": BAD}),
                cmath(r"\text{result}", r":", r"\text{the dark attracts the uninformed}", font_size=32, colors={r"\text{result}": GOOD})]
        whys = [why(r"a dark pool matches buyers with sellers at the midpoint, saving the spread, if the other side shows up"),
                why(r"Zhu (2014): informed traders all want the same side, so their dark orders often go unmatched; they "
                    r"prefer the lit market's certain fill"),
                why(r"so dark pools skim off uninformed flow, which can concentrate information on the exchanges and even "
                    r"improve price discovery, at the cost of wider lit spreads (the routing argument above)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Who chooses the dark? <bookmark mark='a'/> A dark pool matches buyers and sellers at the midpoint, saving "
            "the spread, but only if the other side shows up. <bookmark mark='b'/> Haoxiang Zhu showed that informed "
            "traders all want the same side, so their dark orders often go unmatched, and they prefer the lit market's "
            "certain fill. <bookmark mark='c'/> So the dark attracts the uninformed, which concentrates information on "
            "the exchanges: discovery can improve even as the public spread widens."
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

    def routing(self):
        rows = [cmath(r"\text{uninformed flow}", r"\to", r"\text{wholesalers, dark pools}", font_size=32,
                      colors={r"\text{uninformed flow}": GOOD}),
                cmath(r"\text{informed flow}", r"\to", r"\text{lit exchanges}", font_size=32,
                      colors={r"\text{informed flow}": BAD}),
                cmath(r"\text{lit spreads}", r"\uparrow", r"\text{as the noise leaves}", font_size=32)]
        whys = [why(r"retail orders are less likely to be informed, so a wholesaler can fill them inside the spread and "
                    r"still profit"),
                why(r"what remains on the exchanges is richer in information"),
                why(r"Glosten and Milgrom's spread, with a larger share of informed traders: segmentation widens the public "
                    r"quote for everyone left")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Chapter two explains the consequences. <bookmark mark='a'/> Retail orders are less likely to be informed, "
            "so a wholesaler can fill them inside the spread and still profit. <bookmark mark='b'/> What remains on the "
            "exchanges is richer in information. <bookmark mark='c'/> And by Glosten and Milgrom, a larger share of "
            "informed traders means a wider public spread for everyone left. Segmentation helps the segment that leaves "
            "and can hurt the price everyone sees: the heart of the debate about payment for order flow."
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

    def rules2024(self):
        cards = VGroup(
            desk_question(r"the 2024 amendments", r"in September 2024 the SEC adopted half-cent ticks for stocks whose "
                          r"spreads are usually a tick wide, and lowered the cap on access fees, as published", width=12.4,
                          font_size=25),
            desk_question(r"why the tick matters", r"a spread pinned at one cent is wider than the natural spread; the "
                          r"excess is paid by takers and competed for by queue position, not by price (Part 36)",
                          width=12.4, font_size=25),
            desk_question(r"speed bumps", r"IEX, an exchange since 2016, delays incoming orders by 350 microseconds, so "
                          r"its own pegged orders update before stale quotes can be picked off", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Two dated design examples. <bookmark mark='a'/> In September 2024 the SEC adopted tick-size and access-fee amendments. Adoption is a historical event; this presentation does not verify subsequent litigation, amendments or current compliance dates. <bookmark mark='b'/> A binding minimum tick can prevent a spread narrowing to its hypothetical competitive level and shift competition toward queue position. That is conditional on the tick binding. <bookmark mark='c'/> IEX introduced a three-hundred-fifty-microsecond speed bump and particular order protections. A delay can reduce some stale-quote exposure; it does not guarantee that every quote is protected or that all latency arbitrage disappears."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def auctions(self):
        cards = VGroup(
            desk_question(r"the closing auction", r"index funds and benchmarked managers want the official closing price, "
                          r"so a large and growing share of each day's volume trades in the final auction", width=12.4,
                          font_size=25),
            desk_question(r"why an auction", r"a single price at which all orders cross: a batch auction once a day, the "
                          r"design of Chapter 10, already used where it matters most", width=12.4, font_size=25),
            desk_question(r"order types", r"limit, market, pegged to the midpoint, hidden, post-only, immediate-or-cancel: "
                          r"each tells the venue how much immediacy the trader wants to buy or sell", width=12.4,
                          font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Two more pieces of the plumbing. <bookmark mark='a'/> The closing auction: index funds and benchmarked "
            "managers want the official closing price, so a large and growing share of each day's volume trades in the "
            "final auction. <bookmark mark='b'/> An auction crosses all orders at a single price, a batch auction once a "
            "day, the design Chapter ten proposes for every moment. <bookmark mark='c'/> And order types, from market to "
            "pegged to hidden, each a statement of how much immediacy the trader wants to buy or to sell."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def settle(self):
        rows = [cmath(r"\text{US standard equities}", r":", r"\text{T+1 from May 2024}", font_size=32),
                cmath(r"\text{shorter exposure}", r"\Rightarrow", r"\text{potentially lower collateral}", font_size=32),
                cmath(r"\text{centralized venue}", r":", r"\text{internal credit}\ne\text{external finality}", font_size=32)]
        whys = [why(r"the time between agreeing a trade and exchanging cash for shares, cut from two days to one"),
                why('collateral also depends on volatility, netting, positions and clearing rules; a shorter exposure window does not guarantee a reduction in every case'),
                why('internal balance updates are not final on-chain settlement or a withdrawal guarantee; custody and counterparty exposure depend on the venue')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "After execution comes settlement. <bookmark mark='a'/> US equities moved to standard next-business-day settlement in May 2024, with exceptions for particular instruments and transactions. <bookmark mark='b'/> A shorter exposure window can reduce settlement risk and collateral needs, conditional on netting, volatility and clearing rules; it does not guarantee lower collateral in every case. <bookmark mark='c'/> A centralized crypto venue can credit internal balances immediately, but that is not final on-chain settlement or a withdrawal guarantee. Custody and counterparty risks depend on the venue's legal and operational arrangement."
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

    def journey(self):
        steps = [r"the investor's broker", r"smart order router", r"wholesaler or dark pool", r"lit exchanges",
                 r"clearing and settlement"]
        boxes = VGroup()
        for k, t in enumerate(steps):
            b = RoundedRectangle(width=3.6, height=0.75, corner_radius=0.12, color=PRICE_C if k < 4 else GOOD,
                                 fill_opacity=0.15)
            boxes.add(VGroup(b, label(t, font_size=19).move_to(b)))
        boxes.arrange(DOWN, buff=0.45).move_to(LEFT * 2.6)
        arrows = VGroup(*[Arrow(boxes[k].get_bottom(), boxes[k + 1].get_top(), buff=0.05, stroke_width=2, color=GREY_B,
                                max_tip_length_to_length_ratio=0.3) for k in range(4)])
        notes = VGroup(label(r"best execution duty; payment for order flow", font_size=16, color=GREY_A),
                       label(r"splits the order across venues by price, fees and fill odds", font_size=16, color=GREY_A),
                       label(r"fills inside the NBBO when it can", font_size=16, color=GREY_A),
                       label(r"the rest, at the protected best quotes", font_size=16, color=GREY_A),
                       label(r"one business day later, through the clearing house", font_size=16, color=GREY_A))
        for n_, b_ in zip(notes, boxes):
            n_.next_to(b_, RIGHT, buff=0.4)
        self.add(boxes[0], notes[0])
        with self.voiceover(
            "One retail order's journey. <bookmark mark='a'/> The broker, who owes the customer best execution and may be "
            "paid for the order. <bookmark mark='b'/> A router, which splits it across venues by price, fees and the odds "
            "of a fill. <bookmark mark='c'/> A wholesaler or dark pool, which fills it inside the best quotes if it can. "
            "<bookmark mark='d'/> The lit exchanges, for whatever is left, at the protected quotes. "
            "<bookmark mark='e'/> And a day later, settlement through the clearing house. Every arrow is a choice about "
            "who the counterparty will be."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(mk)
                anims = [FadeIn(boxes[k]), FadeIn(notes[k])]
                if k:
                    anims.append(Create(arrows[k - 1]))
                self.play(*anims)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        eq = MathTex('P=\\$20,\\quad s=1\\ \\mathrm{cent},\\quad s_*=\\tfrac13\\ \\mathrm{cent},\\quad r_m=0.2\\ \\mathrm{cent}', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('A maker rebate does not determine the taker fee. Compute half-spread in bp; then separately stipulate taker fee 0.2 cent and compare one-way cost with the natural half-spread.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover('Pause and predict. At twenty dollars, quoted full spread is one cent and a hypothetical natural full spread is one third cent. A maker earns point two cent rebate. What can be said about taker cost without its fee? Then stipulate a separate point two cent taker fee and compute one-way cost in basis points.'):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()
