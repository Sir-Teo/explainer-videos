from __future__ import annotations


from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (HURDLE, PART, era_strip, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.question()
        self.claims(load("maker"), load("deep"), load("bcs"))
        self.stakes()
        self.not_mm()
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Market Making, ETFs and the Speed Race")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-eight. Market making, exchange-traded funds and the speed race: the business on the other side "
            "of every order in the last three parts, and why it has become a contest of microseconds."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def question(self):
        rows = VGroup(label(r"buy at the bid, sell at the offer, keep the spread", font_size=26),
                      label(r"Bitcoin's perpetual: a spread of one tick, about 0.04 bp", font_size=24, color=GREY_A),
                      label(r"so how does anyone make money doing this?", font_size=26, color=HURDLE))
        rows.arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        with self.voiceover(
            "A simple description of market making. <bookmark mark='a'/> Buy at the bid, sell at the offer, and keep "
            "the spread. <bookmark mark='b'/> On Bitcoin's perpetual future, the spread is one tick: about four "
            "hundredths of a basis point. <bookmark mark='c'/> So how does anyone make money doing it? This part "
            "measures the answer on the real tape."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, mk, dp, bcs):
        d = mk["days"]["2023-05-17"]
        rows = {r["delta"]: r for r in dp["rows"]}
        cards = VGroup(
            desk_question(r"quoting at the touch loses", rf"a maker replayed on the tape loses about "
                          rf"{abs(d['slow']['pnl_per_fill']):.0f} ticks a fill; one that cancels before every sweep still "
                          rf"loses {abs(d['fast']['pnl_per_fill']):.0f}", width=12.4, font_size=19),
            desk_question(r"the model says: quote wide", rf"fill rates fitted to the tape put Guéant, Lehalle and "
                          rf"Fernandez-Tapia's optimal quotes about 30 ticks out; quotes there earn "
                          rf"{rows[30]['pnl60']:+.0f} ticks a fill, and at 45, {rows[45]['pnl60']:+.0f}", width=12.4,
                          font_size=19),
            desk_question(r"the speed race is an equilibrium", r"Budish, Cramton and Shim's sniping spread, proved here, "
                          r"does not depend on how many firms race; batch auctions remove the prize", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this part finds. <bookmark mark='a'/> Quoting at the touch loses: a maker replayed on the tape loses "
            f"about {abs(d['slow']['pnl_per_fill']):.0f} ticks per fill, and even one that could cancel before every "
            f"sweep loses {abs(d['fast']['pnl_per_fill']):.0f}. <bookmark mark='b'/> The optimal-quote model, fitted "
            "to the same tape, says quote about thirty ticks away, and quotes that far out do earn money, before "
            "queues and fees. <bookmark mark='c'/> And the speed race is an equilibrium, proved in the research chapter: "
            "its spread does not depend on how many firms race, and batch auctions take the prize away."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"who they are", r"electronic market makers and high-frequency firms supply most displayed "
                          r"liquidity in stocks, futures, options, FX and crypto; banks once did this on their balance "
                          r"sheets", width=12.4, font_size=19),
            desk_question(r"what they sell", r"immediacy: the right to trade now, at a known price, against someone who "
                          r"will hold the risk until the other side arrives", width=12.4, font_size=19),
            desk_question(r"why the House cares", r"every order of Part 37 trades against them; and ETF arbitrage, the "
                          r"same business, keeps fund prices near their holdings", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> Electronic market makers now supply most displayed liquidity in stocks, "
            "futures, options, currencies and crypto, a job banks once did with their balance sheets. "
            "<bookmark mark='b'/> What they sell is immediacy: the right to trade now, at a known price, against someone "
            "who will carry the risk until the other side arrives. <bookmark mark='c'/> Every order of Part thirty-seven "
            "trades against them, and the same business, as ETF arbitrage, keeps fund prices near their holdings."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def not_mm(self):
        cards = VGroup(
            desk_question(r"not a bet on direction", r"a maker wants to end the day flat; its inventory is a by-product "
                          r"of serving takers, to be shed, not a view to be held", width=12.4, font_size=19),
            desk_question(r"not free money from the spread", r"the spread is the gross margin; adverse selection and "
                          r"inventory are the costs, and on the busiest markets they are larger than the margin", width=12.4,
                          font_size=19),
            desk_question(r"not one market", r"a maker's real book is a portfolio across thousands of instruments and "
                          r"venues, netted and hedged", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three things market making is not. <bookmark mark='a'/> It is not a bet on direction: a maker wants to end "
            "the day flat, and its inventory is a by-product of serving takers. <bookmark mark='b'/> It is not free money "
            "from the spread: the spread is a gross margin, and on the busiest markets its costs are larger. "
            "<bookmark mark='c'/> And it is not one market: a maker's real book is a portfolio across thousands of "
            "instruments and venues, netted and hedged."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Part thirty-five met the dealer in theory; Part thirty-six measured the queue, and Part "
            "thirty-seven the executor's cost. This part runs the dealer's business, closing Act six's look at "
            "microstructure before Part thirty-nine moves to crypto and decentralised finance."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1976, r"inventory models", I), (1981, r"Ho--Stoll", I), (1985, r"Glosten--Milgrom", I),
                   (1993, r"the first ETF", I), (2008, r"Avellaneda--Stoikov", I), (2010, r"the flash crash", I),
                   (2013, r"GLFT; Menkveld", I), (2015, r"batch auctions", I), (2016, r"IEX's speed bump", I),
                   (2019, r"HFT economics", I), (2020, r"bond ETFs in March", I), (2022, r"the race measured", I)]
        strip = era_strip(entries, y0=1970, y1=2027, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Fifty years of the dealer's problem", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 12)]
        with self.voiceover(
            "Fifty years of the dealer's problem. Inventory models from Mark Garman, then Thomas Ho and Hans Stoll; "
            "Glosten and Milgrom's adverse selection; and in 1993 the first American ETF. <bookmark mark='a'/> Then "
            "Avellaneda and Stoikov's optimal quotes, the flash crash, Guéant, Lehalle and Fernandez-Tapia's closed "
            "form, and Albert Menkveld's study of a high-frequency market maker. <bookmark mark='b'/> And the speed race: "
            "batch auctions proposed, a speed bump approved, the economics of high-frequency trading, bond ETFs in "
            "March twenty twenty, and the race measured on the London Stock Exchange."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk_ in zip(groups, [None, "a", "b"]):
                if mk_:
                    vo.wait_until(mk_)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The maker's P\&L: spread, rebates, adverse selection and inventory",
            r"A market maker replayed on Bitcoin's tape, slow and fast",
            r"Fill rates fitted to the tape, and the optimal quotes they imply",
            r"Tick size, queue position and the rent in a pinned spread",
            r"ETF market making: creation, redemption and March 2020",
            r"The speed race, and the economics of high-frequency trading",
            r"For the researcher: the sniping equilibrium and batch auctions, proved",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: the maker's profit and loss; a maker replayed on Bitcoin's tape; fill rates and the optimal quotes "
            "they imply; tick size and the rent in a pinned spread; ETF market making and March twenty twenty; the speed "
            "race and the economics of high-frequency trading; and the sniping equilibrium, proved."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("mm", "execution"))
        with self.voiceover(
            "In the House, the market-making desk opens beside the execution desk: one sells immediacy, the other buys "
            "it, and each must know what the other is paying."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
