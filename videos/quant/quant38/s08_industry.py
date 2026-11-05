from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, FAST_C, GOOD, PART, SPREAD_C)


class Industry(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.menkveld()
        self.styles()
        self.costs()
        self.stress()
        self.options()
        self.crypto()
        self.question()

    def answer(self):
        rows = [cmath(r"\text{sniping prize}", r"\to", r"0", font_size=40, colors={r"0": GOOD}),
                cmath(r"\text{spread}", r"\to", r"\text{inventory and adverse-selection costs only}", font_size=32),
                cmath(r"\text{a microsecond}", r"\to", r"\text{worth almost nothing}", font_size=36, colors={r"\text{a microsecond}": FAST_C})]
        whys = [why(r"public news arriving inside a batch reaches every bidder before the auction clears, so stale quotes "
                    r"can be updated in time"),
                why(r"makers no longer need to charge investors for being sniped"),
                why(r"speed matters only at the boundary of a batch, a tiny fraction of the time; the arms race loses its "
                    r"point")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> In a batch auction, public news that arrives within a batch "
            "reaches every bidder before the auction clears, so the sniping prize all but disappears. "
            "<bookmark mark='b'/> The spread falls to what inventory risk and genuine private information cost. "
            "<bookmark mark='c'/> And a microsecond is worth almost nothing, because it matters only at the edge of a "
            "batch."
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

    def card(self):
        c = chapter_card(7, r"The economics of fast market making", r"What do high-frequency market makers earn, and "
                         r"what does it cost them?", part=PART)
        with self.voiceover("Chapter seven. A handful of studies have seen inside high-frequency firms' trading through "
                            "regulators' data. They tell a consistent story about where the money comes from, and who "
                            "keeps it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def menkveld(self):
        rows = [cmath(r"\text{spread}", r"+", r"\text{rebates}", font_size=40, colors={r"\text{spread}": SPREAD_C}),
                cmath(r"-\ \text{positioning}", r"<", r"0", font_size=40, colors={r"-\ \text{positioning}": BAD}),
                cmath(r"\text{net}", r">", r"0,\ \text{small per trade}", font_size=38, colors={r"\text{net}": GOOD})]
        whys = [why(r"Menkveld (2013): one large high-frequency maker on Chi-X and Euronext earned the spread on its "
                    r"trades and the venue's rebates"),
                why(r"and lost money on its positions, the adverse selection and inventory of Chapter 1"),
                why(r"the net was positive but small per trade, made on enormous volume; its inventory mean-reverted "
                    r"within minutes and it hedged across venues")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Inside one maker. <bookmark mark='a'/> Albert Menkveld studied a single large high-frequency market maker "
            "on the Chi-X and Euronext venues. It earned the spread and the rebates. <bookmark mark='b'/> It lost money "
            "on its positions: Chapter one's adverse selection and inventory. <bookmark mark='c'/> The net was positive "
            "but small per trade, made on enormous volume, with inventory that mean-reverted within minutes and was "
            "hedged across venues. Our replay's arithmetic, done by someone faster."
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

    def styles(self):
        cards = VGroup(
            desk_question(r"passive and aggressive", r"high-frequency firms both make and take; Baron et al.\ (2019) found "
                          r"the aggressive, liquidity-taking ones among the most profitable", width=12.4, font_size=19),
            desk_question(r"concentration", r"profits concentrate in the fastest few; new entrants earn less and are more "
                          r"likely to exit, a winner-take-most market", width=12.4, font_size=19),
            desk_question(r"relative speed", r"what predicts profit is rank in speed, not speed itself: being faster than "
                          r"the others is the asset", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Across firms. <bookmark mark='a'/> High-frequency firms both make and take liquidity, and Baron and "
            "colleagues found the aggressive, liquidity-taking ones among the most profitable. <bookmark mark='b'/> "
            "Profits concentrate in the fastest few; new entrants earn less and exit more often. <bookmark mark='c'/> "
            "And what predicts profit is rank in speed, not speed itself: the asset is being faster than everyone else, "
            "the arms race of Chapter six."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def costs(self):
        cards = VGroup(
            desk_question(r"colocation and data", r"servers in the exchange's data centre, direct feeds of every message, "
                          r"and the exchange fees for both: a fixed cost that favours scale", width=12.4, font_size=19),
            desk_question(r"links between venues", r"microwave and laser networks between financial centres shave "
                          r"milliseconds off fibre, because light travels faster through air than glass", width=12.4,
                          font_size=19),
            desk_question(r"hardware and people", r"order logic in programmable chips, and engineers who measure "
                          r"themselves in nanoseconds; the spending is Chapter 6's social cost", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What speed costs. <bookmark mark='a'/> Servers inside the exchange's data centre, direct feeds of every "
            "message, and the fees for both: a fixed cost that favours scale. <bookmark mark='b'/> Microwave and laser "
            "links between financial centres, because light travels faster through air than through glass fibre. "
            "<bookmark mark='c'/> And order logic built into programmable chips. All of it is Chapter six's social "
            "cost, a race to split the same prize."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stress(self):
        rows = [cmath(r"\text{calm}", r":", r"\text{narrow spreads, deep books}", font_size=38, colors={r"\text{calm}": GOOD}),
                cmath(r"\text{stress}", r":", r"\text{quotes widen or vanish}", font_size=38, colors={r"\text{stress}": BAD}),
                cmath(r"\text{no obligation}", r"\Rightarrow", r"\text{liquidity is a choice}", font_size=36)]
        whys = [why(r"in normal times, competition among fast makers has narrowed spreads in most markets"),
                why(r"when volatility jumps, adverse selection and inventory risk jump, and makers widen or withdraw: 6 May "
                    r"2010, 15 October 2014 (Part 35)"),
                why(r"unlike the specialists of old, most electronic makers are not obliged to quote; liquidity supplied "
                    r"by choice can be withdrawn by choice")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "In stress. <bookmark mark='a'/> In normal times, competition among fast makers has narrowed spreads in most "
            "markets. <bookmark mark='b'/> When volatility jumps, so do adverse selection and inventory risk, and makers "
            "widen or withdraw, as on the sixth of May twenty ten and the fifteenth of October twenty fourteen. "
            "<bookmark mark='c'/> Most electronic makers are not obliged to quote. Liquidity supplied by choice can be "
            "withdrawn by choice."
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

    def options(self):
        cards = VGroup(
            desk_question(r"thousands of quotes, one surface", r"an options maker quotes every strike and expiry from one "
                          r"volatility surface; a move in the surface reprices them all at once (Part 12)", width=12.4,
                          font_size=19),
            desk_question(r"the inventory is the Greeks", r"delta hedged continuously in the underlying, vega and gamma "
                          r"managed by skewing quotes across the surface (Part 11)", width=12.4, font_size=19),
            desk_question(r"the same race", r"a stale surface is sniped like a stale quote; options makers race to "
                          r"update thousands of prices after every move in the underlying", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Options at scale. <bookmark mark='a'/> An options maker quotes every strike and expiry from one volatility "
            "surface, so a move in the surface reprices them all at once. <bookmark mark='b'/> Its inventory is its "
            "Greeks: delta hedged continuously, vega and gamma managed by skewing quotes. <bookmark mark='c'/> And it "
            "runs the same race: a stale surface is sniped like a stale quote, thousands of prices at a time."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def crypto(self):
        cards = VGroup(
            desk_question(r"fee tiers", r"exchanges charge by volume tier; the largest makers pay little or receive "
                          r"rebates, which Chapter 2 showed is the difference between a loss and a business", width=12.4,
                          font_size=19),
            desk_question(r"many venues, one asset", r"makers quote on several exchanges and hedge on the deepest; the "
                          r"perpetual's funding rate is part of the inventory cost (Part 39)", width=12.4, font_size=19),
            desk_question(r"contracts with issuers", r"new tokens often hire market makers by contract; the terms, as "
                          r"reported in some enforcement cases, can create conflicts the public never sees", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And in crypto. <bookmark mark='a'/> Exchanges charge by volume tier, and the largest makers pay little or "
            "receive rebates: as Chapter two showed, the difference between a loss and a business. "
            "<bookmark mark='b'/> Makers quote on many venues and hedge on the deepest, with the perpetual's funding rate "
            "part of the inventory cost. <bookmark mark='c'/> And new tokens often hire market makers by contract; some "
            "enforcement cases, as reported, have shown how such terms can create conflicts the public never sees."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the House wants to quote Bitcoin's perpetual. Given Chapters 2 to 6, what three things must its "
                       r"desk have before it posts a single order?")
        with self.voiceover(
            "Pause and predict. The House wants to make markets in Bitcoin's perpetual. Given Chapters two to six, what "
            "three things must its desk have before it posts a single order?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
