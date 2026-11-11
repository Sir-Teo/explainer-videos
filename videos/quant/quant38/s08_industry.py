from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (INV_C, BAD, FAST_C, GOOD, PART, SPREAD_C)


class Industry(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.menkveld()
        self.styles()
        self.costs()
        self.hedging()
        self.stress()
        self.obligations()
        self.rents()
        self.options()
        self.crypto()
        self.question()

    def answer(self):
        rows = [cmath(r"\text{sniping prize}", r"\to", r"0", font_size=40, colors={r"0": GOOD}),
                cmath(r"\text{spread}", r"\to", r"\text{inventory and adverse-selection costs only}", font_size=32),
                cmath(r"\text{a microsecond}", r"\to", r"\text{boundary-dependent value}", font_size=36, colors={r"\text{a microsecond}": FAST_C})]
        whys = [why(r"public news arriving inside a batch reaches every bidder before the auction clears, so stale quotes "
                    r"can be updated in time"),
                why(r"makers no longer need to charge investors for being sniped"),
                why(r"with uniform news phase and deterministic latency, a boundary exposure fraction is small; this is a separate model, not a general elimination of the "
                    r"race incentive")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The batch question, conditionally. <bookmark mark='a'/> Ideal common-information repricing before clearing removes the stale-quote prize by assumption. <bookmark mark='b'/> Inventory, private information, fees and participation can still support a positive spread. <bookmark mark='c'/> With finite latency, a small speed difference can matter near the boundary. How much it matters requires an explicit information and update model, which the binary batch flag does not supply."
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
            "An attributed case study. <bookmark mark='a'/> Menkveld examined one large high-frequency market maker trading on Chi-X and Euronext and documented spread and rebate revenues. <bookmark mark='b'/> Its positioning component was negative in the study's decomposition. <bookmark mark='c'/> Net profit was positive with high turnover and actively managed inventory. This is one firm's observed business, not our coarse-grid replay made profitable merely by substituting a faster label."
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
        self.add(cards[0])
        with self.voiceover(
            "Across firms. <bookmark mark='a'/> High-frequency firms both make and take liquidity, and Baron and "
            "colleagues found the aggressive, liquidity-taking ones among the most profitable. <bookmark mark='b'/> "
            "Profits concentrate in the fastest few; new entrants earn less and exit more often. <bookmark mark='c'/> "
            "And what predicts profit is rank in speed, not speed itself: the asset is being faster than everyone else, "
            "the arms race of Chapter six."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
                          r"processing latency; real resources are used, but their welfare value depends on the model", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "What speed uses. <bookmark mark='a'/> Colocation, feeds and technical staff have fixed and variable costs. <bookmark mark='b'/> Faster intercity links use real resources. <bookmark mark='c'/> Hardware logic can reduce processing latency. The fixed-prize toy game treats this spending as redundant. In a broader market, technology may also improve reliability, hedging or price discovery, so its entire cost is not automatically social waste."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def hedging(self):
        rows = [cmath(r"\text{inventory}", r":", r"q_1, \dots, q_n\ \text{across instruments}", font_size=36,
                      colors={r"\text{inventory}": INV_C}),
                cmath(r"\text{hedge}", r":", r"-\beta^\top q\ \text{in an index future}", font_size=38),
                cmath(r"\text{residual}", r":", r"\text{idiosyncratic, mean-reverting}", font_size=36,
                      colors={r"\text{residual}": GOOD})]
        whys = [why(r"a maker in many names accumulates small positions everywhere"),
                why(r"the common factor is hedged at once in the most liquid instrument, Part 31's risk model in real time"),
                why(r"what remains is small, specific to each name, and shed by skewing quotes; Menkveld's maker unwound "
                    r"within minutes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How inventory is really managed. <bookmark mark='a'/> A maker in many names accumulates small positions "
            "everywhere. <bookmark mark='b'/> The common factor is hedged at once in the most liquid instrument, an index "
            "future: Part thirty-one's risk model in real time. <bookmark mark='c'/> What remains is small and specific "
            "to each name, and is shed by skewing quotes, the way Menkveld's maker unwound within minutes."
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

    def obligations(self):
        cards = VGroup(
            desk_question(r"MiFID II in Europe", r"firms running algorithmic market-making strategies must sign "
                          r"market-making agreements and quote continuously for a specified share of trading hours",
                          width=12.4, font_size=19),
            desk_question(r"US designated makers", r"designated market makers on some exchanges must maintain quotes "
                          r"within set spreads; most electronic makers have only light quoting obligations", width=12.4,
                          font_size=19),
            desk_question(r"the trade-off", r"obligations keep liquidity in stress, but make the role costlier, so fewer "
                          r"firms take it on; rebates and priority are the payment for the burden", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Quoting obligations depend on jurisdiction and role. <bookmark mark='a'/> MiFID two established agreement and quoting requirements for covered algorithmic market-making strategies, subject to its definitions and exceptions. <bookmark mark='b'/> American designated-maker and exchange programs have venue-specific requirements and incentives. <bookmark mark='c'/> Such rules can support continuity but do not guarantee unlimited liquidity in stress. This is an institutional overview, not a current legal compliance test or a claim that every electronic firm has the same obligations."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def rents(self):
        cards = VGroup(
            desk_question(r"how large is the prize?", r"Aquilina, Budish and O'Neill scaled their London estimate to about "
                          r"\$5 billion a year across global equity markets, as reported in their paper", width=12.4,
                          font_size=19),
            desk_question(r"who earns it", r"a few of the fastest firms win most races; the losers include slower makers, "
                          r"and in the end investors, through the spread", width=12.4, font_size=19),
            desk_question(r"transfers versus resource costs", r"investor payments transfer surplus; resource costs and information effects need separate analysis, beyond the money a design may "
                          r"leave with them (Chapter 6)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Interpreting the measured race prize. <bookmark mark='a'/> Aquilina, Budish and O'Neill extrapolated their London estimate to a multi-billion-dollar global equity figure, with the study's sampling and scaling assumptions. <bookmark mark='b'/> Race winners receive transfers that can affect investor costs and firms' incentives. <bookmark mark='c'/> The transfer itself is not automatically a deadweight social loss. Resource spending, liquidity and information effects require a separate welfare analysis."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
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
        self.add(cards[0])
        with self.voiceover(
            "Options at scale. <bookmark mark='a'/> An options maker quotes every strike and expiry from one volatility "
            "surface, so a move in the surface reprices them all at once. <bookmark mark='b'/> Its inventory is its "
            "Greeks: delta hedged continuously, vega and gamma managed by skewing quotes. <bookmark mark='c'/> And it "
            "runs the same race: a stale surface is sniped like a stale quote, thousands of prices at a time."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def crypto(self):
        cards = VGroup(
            desk_question(r"fee tiers", r"exchanges charge by volume tier; the largest makers pay little or receive "
                          r"rebates, which changes accounting but does not establish a viable professional business from this replay", width=12.4,
                          font_size=19),
            desk_question(r"many venues, one asset", r"makers quote on several exchanges and hedge on the deepest; the "
                          r"perpetual's funding rate is part of the inventory cost (Part 39)", width=12.4, font_size=19),
            desk_question(r"contracts with issuers", r"new tokens often hire market makers by contract; the terms, as "
                          r"reported in some enforcement cases, can create conflicts the public never sees", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Crypto market-making costs. <bookmark mark='a'/> Volume tiers and contractual rebates change fees, but our chosen replay rebate arithmetic does not show a viable professional business. <bookmark mark='b'/> Cross-venue hedging adds basis, funding, collateral and counterparty risks absent from the single-book reconstruction. <bookmark mark='c'/> Token-issuer contracts can also create conflicts. Specific enforcement findings must be attributed to their cases rather than generalized to every maker."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label("the House wants to quote Bitcoin's perpetual. Given Chapters 2 to 6, what three things must its desk have before it posts a single order?", 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. The House wants to make markets in Bitcoin's perpetual. Given Chapters two to six, what "
            "three things must its desk have before it posts a single order?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
