from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import BAD, DEALER_C, FLOW_C, GOOD, HURDLE, INF_C, PART, PRICE_C


class HFT(VoiceoverScene):
    def construct(self):
        self.card()
        self.new_mm()
        self.evidence()
        self.sniping()
        self.backrun()
        self.race_tax()
        self.manipulation()
        self.question()

    def card(self):
        c = chapter_card(9, r"High-frequency traders as market makers", r"Are the fastest traders the dealers of today, "
                         r"or their predators?", part=PART)
        with self.voiceover("Chapter nine. The dealers of Chapter one are now algorithms, quoting thousands of instruments "
                            "and updating in microseconds. Are they the market makers of today, or something else? The "
                            "evidence says both, depending on the moment."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def new_mm(self):
        rows = [cmath(r"\text{passive}", r":", r"\text{quote both sides, earn spread and rebates}", font_size=32,
                      colors={r"\text{passive}": DEALER_C}),
                cmath(r"\text{inventory}", r"\approx", r"0\ \text{by the end of the day}", font_size=34),
                cmath(r"\text{edge}", r"=", r"\text{speed to update quotes when the value moves}", font_size=32,
                      colors={r"\text{edge}": HURDLE})]
        whys = [why(r"Menkveld (2013) studied one high-frequency market maker in European stocks: most of its trades were "
                    r"passive, at its own quotes"),
                why(r"its inventory mean-reverted fast and ended each day near zero: Ho and Stoll's dealer, automated"),
                why(r"its profit came from the spread, net of losses to better-informed traders; speed is what keeps those "
                    r"losses small")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The new market makers. <bookmark mark='a'/> Albert Menkveld studied one high-frequency market maker in "
            "European stocks: most of its trades were passive, at its own quotes. <bookmark mark='b'/> Its inventory "
            "reverted to zero fast, and ended each day near flat: Chapter one's shading, automated. "
            "<bookmark mark='c'/> It earned the spread, less what better-informed traders took, and its speed is what "
            "kept those losses small: a quote that updates before the news is a quote that is not picked off."
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

    def evidence(self):
        cards = VGroup(
            desk_question(r"Hendershott, Jones and Menkveld (2011)", r"when NYSE automated its quote dissemination in 2003, "
                          r"algorithmic trading rose and spreads in large stocks narrowed, because quotes carried less "
                          r"adverse selection", width=12.4, font_size=19),
            desk_question(r"Brogaard, Hendershott and Riordan (2014)", r"high-frequency traders' aggressive orders went in "
                          r"the direction of permanent price changes and against transitory errors: they speed up price "
                          r"discovery", width=12.4, font_size=19),
            desk_question(r"and the other side", r"the same traders take liquidity from slower quotes when news arrives; "
                          r"their profit is partly other market makers' adverse selection", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The evidence. <bookmark mark='a'/> Terrence Hendershott, Charles Jones and Albert Menkveld: when the New York "
            "Stock Exchange automated its quotes in 2003, algorithmic trading rose and spreads in large stocks narrowed. "
            "<bookmark mark='b'/> Jonathan Brogaard, Hendershott and Ryan Riordan: high-frequency traders' aggressive "
            "orders moved in the direction of permanent price changes, speeding up price discovery. "
            "<bookmark mark='c'/> And the same orders take liquidity from slower quotes when news arrives: part of their "
            "profit is other market makers' adverse selection."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def sniping(self):
        rows = [cmath(r"\text{public news}", r"\Rightarrow", r"\text{a race: cancel the stale quote, or hit it}", font_size=32),
                cmath(r"\text{the maker loses}", r"\text{if}", r"\text{one of } N \text{ snipers is faster}", font_size=32,
                      colors={r"\text{the maker loses}": BAD}),
                cmath(r"\text{spread}", r"\ge", r"\text{the expected sniping loss per trade}", font_size=34,
                      colors={r"\text{spread}": HURDLE})]
        whys = [why(r"Budish, Cramton and Shim (2015): when a public signal moves the value, everyone sees it at once"),
                why(r"the quote's owner is one trader trying to cancel; many others are trying to trade against it; in "
                    r"continuous time someone always arrives first"),
                why(r"a cost of symmetric information, not private: spreads must cover it, however fast everyone becomes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Eric Budish, Peter Cramton and John Shim found an adverse selection with no private information at all. "
            "<bookmark mark='a'/> When public news moves the value, a race begins: the quote's owner tries to cancel, "
            "everyone else tries to hit it. <bookmark mark='b'/> In continuous time someone always arrives first, and "
            "the owner is one against many. <bookmark mark='c'/> So spreads must cover a sniping loss that no amount of "
            "speed removes, because everyone gets faster together. Chapter ten gives their remedy."
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

    def backrun(self):
        rows = [cmath(r"\text{a large order}", r"\Rightarrow", r"\text{a pattern in the flow}", font_size=34,
                      colors={r"\text{a large order}": INF_C}),
                cmath(r"\text{back-runners}", r":", r"\text{detect it, trade the same way, ahead of it}", font_size=32,
                      colors={r"\text{back-runners}": BAD}),
                cmath(r"\text{the institution}", r":", r"\text{randomises, hides, uses dark pools}", font_size=32,
                      colors={r"\text{the institution}": GOOD})]
        whys = [why(r"a pension fund slicing a large order leaves a statistical signature in the order flow"),
                why(r"Yang and Zhu (2020): fast traders who learn from that signature trade in the same direction, which "
                    r"raises the institution's cost and speeds up price discovery"),
                why(r"so execution algorithms add randomness and route to venues that hide size: Part 37's game against an "
                    r"opponent who reads the flow")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And a subtler kind of speed. <bookmark mark='a'/> A pension fund slicing a large order leaves a pattern in "
            "the flow. <bookmark mark='b'/> Liyan Yang and Haoxiang Zhu modelled back-runners: fast traders who detect "
            "the pattern and trade the same way, raising the institution's cost while moving the price toward its "
            "information sooner. <bookmark mark='c'/> So execution algorithms add randomness and hide size in dark pools: "
            "Kyle's insider, playing against an opponent who reads the flow."
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

    def race_tax(self):
        cards = VGroup(
            desk_question(r"measuring the races", r"Aquilina, Budish and O'Neill (2022) used the London Stock Exchange's "
                          r"message data, failed cancellations included, to find races between fast traders to the same "
                          r"stale quote, lasting microseconds", width=12.4, font_size=19),
            desk_question(r"how much", r"they reported races in about a fifth of FTSE 100 trading volume, and a cost to "
                          r"liquidity providers, a latency-arbitrage tax, of about half a basis point on all trading", width=12.4,
                          font_size=19),
            desk_question(r"who pays", r"investors, through spreads that must cover the tax; the winners are a handful of "
                          r"the fastest firms", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Is the sniping cost large? <bookmark mark='a'/> Matteo Aquilina, Eric Budish and Peter O'Neill used the "
            "London Stock Exchange's message data, including the failed attempts to cancel, to find races between fast "
            "traders to the same stale quote, settled in microseconds. <bookmark mark='b'/> They reported races in about "
            "a fifth of FTSE one hundred trading volume, and a tax on liquidity of about half a basis point on all "
            "trading. <bookmark mark='c'/> Paid by investors through the spread, and won by a handful of the fastest firms."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def manipulation(self):
        cards = VGroup(
            desk_question(r"momentum ignition", r"aggressive orders meant to start a move that other algorithms follow, "
                          r"then trading against it: illegal when it is the intent", width=12.4, font_size=19),
            desk_question(r"spoofing and layering", r"Part 34's cases: orders placed to be cancelled, to move the queue "
                          r"others read", width=12.4, font_size=19),
            desk_question(r"quote stuffing", r"floods of orders and cancels that slow others' data feeds; the regulators' "
                          r"data now record every message (the CAT)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the abuses speed allows. <bookmark mark='a'/> Momentum ignition: aggressive orders meant to start a "
            "move that other algorithms follow, then trading against it. <bookmark mark='b'/> Spoofing and layering, "
            "Part thirty-four's cases. <bookmark mark='c'/> And floods of orders and cancels that slow others' data. "
            "Every one exploits other algorithms reading the order book, which is why surveillance reads it too."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a quote is hit by a sniper when public news arrives, which happens on 2\% of the quote's trades, "
                       r"each costing 3 ticks. What minimum spread covers it?")
        with self.voiceover(
            "Pause and predict. A quote is hit by a sniper when public news arrives, on two percent of its trades, each "
            "costing three ticks. What is the smallest spread that covers it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
