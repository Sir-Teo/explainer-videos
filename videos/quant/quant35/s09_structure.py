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
        with self.voiceover("Chapter eight. The models so far had one dealer and one market. An American stock trades on "
                            "more than a dozen exchanges and dozens of off-exchange venues, linked by rules. The rules "
                            "decide who meets whom, and at what price."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def nms(self):
        rows = [cmath(r"\text{order protection}", r":", r"\text{no trade through a better displayed quote elsewhere}",
                      font_size=30, colors={r"\text{order protection}": PRICE_C}),
                cmath(r"\text{access}", r":", r"\text{fair access to quotes; fees capped}", font_size=30,
                      colors={r"\text{access}": PRICE_C}),
                cmath(r"\text{sub-penny}", r":", r"\text{no quotes finer than a cent above \$1}", font_size=30,
                      colors={r"\text{sub-penny}": PRICE_C}),
                cmath(r"\text{NBBO}", r"=", r"\text{the best bid and offer across all exchanges}", font_size=30,
                      colors={r"\text{NBBO}": GOOD})]
        whys = [why(r"Regulation NMS, adopted by the SEC in 2005: an order must be routed to the venue showing the best "
                    r"price"),
                why(r"and every venue must let others reach its quotes, at a capped fee"),
                why(r"the tick: a minimum price increment that, for a cheap stock, can be wider than its natural spread"),
                why(r"the national best bid and offer, the reference every broker's execution is judged against")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The rules, in the United States. <bookmark mark='a'/> Regulation NMS, adopted in 2005: no venue may trade "
            "through a better price displayed on another. <bookmark mark='b'/> Every venue must let others reach its "
            "quotes, at a capped fee. <bookmark mark='c'/> No quotes finer than a cent, for stocks above a dollar. "
            "<bookmark mark='d'/> Together they define the national best bid and offer, the reference against which "
            "every broker's execution is judged. One market, assembled from many."
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
                cmath(r"\text{net spread}", r"=", r"\text{quoted spread} - 2\,\text{rebate}", font_size=32)]
        whys = [why(r"maker-taker pricing pays liquidity providers a fraction of a cent per share"),
                why(r"and charges those who remove liquidity, up to the cap"),
                why(r"so the true cost of trading is the quoted spread net of fees and rebates; inverted venues reverse the "
                    r"signs, paying takers, and attract different orders")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How venues compete. <bookmark mark='a'/> Most exchanges pay a rebate, a fraction of a cent per share, to the "
            "trader who posts a limit order: the maker. <bookmark mark='b'/> And charge a fee to the trader who crosses "
            "the spread: the taker. <bookmark mark='c'/> So the real cost of a trade is the spread net of fees and "
            "rebates. Some venues invert the scheme and pay takers instead, and attract different orders: the venue's "
            "price list decides who trades there."
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
                          r"and closing prices", width=12.4, font_size=19),
            desk_question(r"dark pools", r"alternative trading systems with no displayed quotes, usually matching at the "
                          r"midpoint; they let large orders hide, Kyle's insider's wish", width=12.4, font_size=19),
            desk_question(r"wholesalers", r"retail orders bought from brokers (Part 34) and filled internally, often "
                          r"slightly better than the NBBO; with dark pools, off-exchange trading has been around half of "
                          r"US equity volume, as reported", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
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
                          font_size=19),
            desk_question(r"why the tick matters", r"a spread pinned at one cent is wider than the natural spread; the "
                          r"excess is paid by takers and competed for by queue position, not by price (Part 36)",
                          width=12.4, font_size=19),
            desk_question(r"speed bumps", r"IEX, an exchange since 2016, delays incoming orders by 350 microseconds, so "
                          r"its own pegged orders update before stale quotes can be picked off", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rules keep changing. <bookmark mark='a'/> In September 2024 the SEC adopted half-cent ticks for stocks "
            "whose spreads are usually pinned at one tick, and lowered the cap on access fees. <bookmark mark='b'/> A "
            "spread pinned at a cent is wider than its natural level; the excess is paid by takers, and makers compete "
            "for it by queue position rather than by price, Part thirty-six's subject. <bookmark mark='c'/> And IEX, an "
            "exchange since 2016, delays every incoming order by three hundred and fifty microseconds, so that stale "
            "quotes cannot be picked off."
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
                          font_size=19),
            desk_question(r"why an auction", r"a single price at which all orders cross: a batch auction once a day, the "
                          r"design of Chapter 10, already used where it matters most", width=12.4, font_size=19),
            desk_question(r"order types", r"limit, market, pegged to the midpoint, hidden, post-only, immediate-or-cancel: "
                          r"each tells the venue how much immediacy the trader wants to buy or sell", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
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
        rows = [cmath(r"\text{T+1}", r":", r"\text{US equities settle one business day after the trade, from May 2024}",
                      font_size=28, colors={r"\text{T+1}": GOOD}),
                cmath(r"\text{shorter settlement}", r"\Rightarrow", r"\text{less margin at the clearing house}", font_size=30),
                cmath(r"\text{crypto}", r":", r"\text{settlement inside the exchange, instantly, with its own risks}",
                      font_size=28)]
        whys = [why(r"the time between agreeing a trade and exchanging cash for shares, cut from two days to one"),
                why(r"the clearing house's exposure to a member's default is shorter, so it asks for less collateral; "
                    r"the January 2021 meme-stock squeeze was the argument (Part 21)"),
                why(r"Binance's spot and perpetual markets settle on its own books: no clearing house, and the exchange "
                    r"itself as the counterparty risk, as FTX showed in 2022")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And after the trade. <bookmark mark='a'/> Since May 2024 American equities settle one business day after "
            "the trade, not two. <bookmark mark='b'/> A shorter wait means less exposure to a member's default, so the "
            "clearing house asks for less collateral; the meme-stock squeeze of January 2021, from Part twenty-one, was "
            "the argument. <bookmark mark='c'/> On a crypto exchange, trades settle instantly on the exchange's own "
            "books, with no clearing house at all, and the exchange itself as the counterparty, as FTX showed."
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
        q = pause_card(r"a stock trades at \$20 with a one-cent spread and a natural spread of a third of a cent. A rebate "
                       r"of 0.2 cents is paid to makers. What does a taker really pay, and who gains from a half-cent tick?")
        with self.voiceover(
            "Pause and predict. A twenty-dollar stock is quoted a cent wide, though its natural spread is a third of a "
            "cent, and makers earn a rebate of a fifth of a cent. What does a taker really pay, and who gains from a "
            "half-cent tick?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
