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
        self.add(rows[0])
        with self.voiceover(
            "A simple gross-spread story. <bookmark mark='a'/> Buy at the bid and sell at the offer, if both trades occur before value changes and other costs. <bookmark mark='b'/> In the selected Bitcoin perpetual snapshots a one-tick spread is common, about four hundredths of a basis point. <bookmark mark='c'/> What remains after marking the selected fills and inventory? This part compares model-based answers with a particular public-tape reconstruction."
        ) as vo:
            vo.wait_until("a")
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
            desk_question(r"this touch replay loses", rf"final-mid marking in the chosen replay loses about "
                          rf"{abs(d['slow']['pnl_per_fill']):.0f} ticks per selected fill; the within-step hindsight variant still "
                          rf"loses {abs(d['fast']['pnl_per_fill']):.0f}", width=12.4, font_size=19),
            desk_question(r"a model suggests wide quotes", rf"reach proxies fed into Guéant, Lehalle and "
                          rf"Fernandez-Tapia's approximation put quotes about 30 ticks out; gross reach marks there are "
                          rf"{rows[30]['pnl60']:+.0f} ticks a fill, and at 45, {rows[45]['pnl60']:+.0f}", width=12.4,
                          font_size=19),
            desk_question(r"a conditional sniping equilibrium", r"the simplified role-indifference spread, under stated assumptions, "
                          r"does not depend on the number of equally fast firms; ideal batch repricing removes stale executions by assumption", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            f"Three results with different scopes. <bookmark mark='a'/> In our coarse-grid replay, the slow rule loses about {abs(d['slow']['pnl_per_fill']):.0f} ticks per fill marked to the final mid, and the rule that knows which trades will pass through it still loses {abs(d['fast']['pnl_per_fill']):.0f}. <bookmark mark='b'/> Feeding reach proxies into a quoting model suggests roughly thirty ticks. A separate optimistic reach test has positive gross marks there, without queues, fees or an inventory strategy. <bookmark mark='c'/> A simplified sniping model has a spread independent of the number of equally fast firms. That is a conditional model result; ideal repricing in a batch removes its stale-quote prize."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"who they are", r"electronic firms and banks supply displayed "
                          r"liquidity across products; their shares vary by market and banks still use their balance "
                          r"sheets", width=12.4, font_size=19),
            desk_question(r"what they sell", r"immediacy: the right to trade now, at a known price, against someone who "
                          r"will hold the risk until the other side arrives", width=12.4, font_size=19),
            desk_question(r"why the House cares", r"every order of Part 37 trades against them; and ETF arbitrage, the "
                          r"same business, keeps fund prices near their holdings", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Why this matters. <bookmark mark='a'/> Electronic market makers are important liquidity suppliers across stocks, futures, currencies and crypto, alongside banks and other dealers. Shares vary by venue and product. <bookmark mark='b'/> They sell immediacy: an executable price now while they manage the position that results. <bookmark mark='c'/> Part thirty-seven's executor trades against them. ETF creation and redemption add a second route between share liquidity and the underlying basket."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def not_mm(self):
        cards = VGroup(
            desk_question(r"not a bet on direction", r"inventory can arise as a by-product "
                          r"of serving takers; forecasts and overnight positions depend on the strategy", width=12.4, font_size=19),
            desk_question(r"not free money from the spread", r"the spread is the gross margin; adverse selection and "
                          r"inventory risk are costs; their size depends on the strategy and market", width=12.4,
                          font_size=19),
            desk_question(r"not one market", r"a maker's real book is a portfolio across thousands of instruments and "
                          r"venues, netted and hedged", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three distinctions. <bookmark mark='a'/> Inventory need not express a directional investment thesis, although makers can use forecasts and may carry positions overnight. <bookmark mark='b'/> The spread is gross revenue. Our simple replay loses after marking its fills; this does not establish that professional makers have costs above revenue. <bookmark mark='c'/> Many firms manage portfolios of instruments and venues with hedges and capital constraints."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
            r"The maker's ledger: execution edge, rebates and inventory gains",
            r"A market maker replayed on Bitcoin's tape, slow and fast",
            r"Reach probabilities, model quotes and gross markout proxies",
            r"Tick size, queue position and the rent in a pinned spread",
            r"ETF market making: creation, redemption and March 2020",
            r"The speed race, and the economics of high-frequency trading",
            r"For the researcher: conditional role roots, transfers and separate batch assumptions",
        ], color=QC.IDEA)
        with self.voiceover(
            'The plan: a consistent profit ledger; a coarse-grid maker replay; reach probabilities, model quotes and markout proxies; tick size and queues; ETF arbitrage and the historical policy chronology; the speed race and its economics; and a conditional sniping equilibrium, with a separate speed-investment game.'
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
