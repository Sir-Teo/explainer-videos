from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, FORMULA, GOOD, HURDLE, PART


class China(VoiceoverScene):
    def construct(self):
        self.card()
        self.enhancement()
        self.february()
        self.lingjun()
        self.hedge()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(10, r"China's quant industry", r"What happens when many miners crowd into the same trade?",
                         part=PART)
        with self.voiceover("Chapter ten. China's quantitative-investment industry offers a useful setting for discussing common exposures, index hedges and execution constraints. What can happen when similar research pipelines produce crowded books?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def enhancement(self):
        rows = [cmath(r"r_{\text{fund}}", r"=", r"r_{\text{CSI 500 or 1000}} + \alpha", font_size=34,
                      colors={r"r_{\text{fund}}": FORMULA}),
                cmath(r"\text{market neutral}", r":", r"\text{long stocks, short futures; residual risks and costs remain}", font_size=30),
                cmath(r"\alpha", r"\leftarrow", r"\text{thousands of mined factors, combined daily}", font_size=30,
                      colors={r"\alpha": HURDLE})]
        whys = [why(r"index enhancement: a fund benchmarked to an index of mid- or small-cap stocks, which aims "
                    r"to beat it by stock selection"),
                why(r"index futures hedge an estimated beta; size, basis, financing and execution risks remain"),
                why(r"the excess return comes from factor libraries of the kind this part mines, rebalanced often; and "
                    r"much of it, in practice, from a tilt toward the smallest stocks")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Index enhancement aims to outperform a specified equity benchmark. <bookmark mark='a'/> A stock-selection portfolio benchmarked to the CSI500 or CSI1000 can carry factor exposures as well as security-specific bets. <bookmark mark='b'/> Shorting index futures offsets an estimated component of market exposure. It does not leave pure alpha: beta mismatch, size and sector tilts, basis moves, financing, margin and execution remain. <bookmark mark='c'/> Large factor libraries can share these risks even when their formula strings differ. Neither mined-factor counts nor a market-neutral label identifies a causal source of excess return."
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

    def february(self):
        card = crisis_card(r"Early 2024", r"A reported crowding episode",
                           body=r"AlphaAgent's version-1 introduction cites small-cap factor underperformance in China's A-share market as motivation for researching alpha decay",
                           stats=((r"\text{size}", r"stock-size exposure can survive an index hedge"),
                                  (r"\text{basis}", r"the futures hedge can move differently from the cash basket"),
                                  (r"\text{margin}", r"leveraged positions can face forced deleveraging"),
                                  (r"\text{scope}", r"a reported motivation, not a causal decomposition of all funds' losses")),
                           width=10.6, font_size=21).move_to(ORIGIN)
        with self.voiceover("An example in the literature. <bookmark mark='a'/> AlphaAgent's February2025 introduction cites small-cap factor underperformance in early2024 as a motivation for studying decay and reversals. That establishes what the paper reports, not a causal explanation for every fund. <bookmark mark='b'/> Common size exposure, basis risk, financing and margin mechanisms can amplify a loss. Their relative contribution needs actual positions, prices, timing and financing data. Unspecified index declines and aggregate fund-return percentages cannot be combined into one reliable account.") as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(card, color=QC.CRISIS, scale_factor=1.01))
        self.wait(0.4)
        self.clear_scene()

    def lingjun(self):
        cards = VGroup(
            desk_question(r"execution capacity is venue-specific", r"a fast sell instruction faces depth, participation limits, market impact and exchange rules", width=12.4, font_size=19),
            desk_question(r"read a trading restriction precisely", r"a restriction for specified accounts, instruments and dates is not a freeze of the firm's financial assets", width=12.4, font_size=19),
            desk_question(r"a loss attribution needs a common denominator", r"identify index membership, dates, fund sample, leverage, costs and source before comparing percentages", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("Execution and public records need separate interpretation. <bookmark mark='a'/> Machine speed does not supply market depth, unlimited participation or exemption from exchange rules. A position can be hard to exit precisely when many firms want the same trade. <bookmark mark='b'/> A temporary trading restriction concerns a stated scope and date range; it must not be described as frozen financial assets. To compare reported sales, index losses and fund returns, first align their dates, venue coverage, leverage and denominators. These distinctions matter even when no named firm's return or order-size figure is used.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.4)
        self.clear_scene()

    def hedge(self):
        rows = [cmath(r"r_{\text{book}}", r"=", r"r_{\text{long}} - \beta\, r_{\text{future}}", font_size=34,
                      colors={r"r_{\text{book}}": FORMULA}),
                cmath(r"r_{\text{long}}", r"=", r"\beta\,r_{\text{index}} + \underbrace{(r_{\text{small}} - r_{\text{index}})}"
                      r"_{\text{the size spread}} + \alpha", font_size=30),
                cmath(r"r_{\text{book}}", r"\approx", r"\alpha + (r_{\text{small}} - r_{\text{index}}) - \beta\,\Delta b",
                      font_size=30, colors={r"r_{\text{book}}": BAD}),
                cmath(r"\text{spread P\&L}", r"\approx", r"L\,(r_{\text{small}}-r_{\text{index}})\quad\text{(fixed toy)}", font_size=32,
                      colors={r"\text{loss}": BAD})]
        whys = [why(r"a long book of stocks, short index futures in proportion to its beta"),
                why(r"a book tilted toward smaller stocks than the index carries the size spread on top of its stock picks"),
                why(r"fixed linear toy: $\Delta b=r_{\text{future}}-r_{\text{index}}$ is the futures/index return gap"),
                why(r"leverage scales this spread component; margin constraints can trigger forced selling")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Use a deliberately simplified hedge decomposition. <bookmark mark='a'/> The long book is offset with index futures using an estimated beta. <bookmark mark='b'/> A small-cap tilt can add a size-spread exposure; the displayed coefficient of one is an illustrative choice, not an estimated industry exposure. <bookmark mark='c'/> The hedge can leave basis changes, beta error, sector and security risks, funding and transaction costs. The spread formula is not a complete portfolio accounting identity. <bookmark mark='d'/> In a fixed equal-notional toy, multiplying the spread by leverage scales that one component. Margin constraints can trigger further selling, but that feedback is a possible mechanism, not a measured causal conclusion about a named firm."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the factors were not independent", r"mined libraries at different firms share data, operators "
                          r"and size exposure: assess their common downside risks", width=12.4, font_size=19),
            desk_question(r"the hedge had a basis", 'small caps against index futures is a bet on the spread between them; the basis and liquidity can move adversely during deleveraging', width=12.4, font_size=19),
            desk_question(r"leverage turns a drawdown into forced selling", r"Part 21's margin spiral, in equities", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Similar data and operators can produce common exposures across firms; different strings do not establish independent risks. <bookmark mark='b'/> Cash baskets and futures can diverge, and their liquidity can deteriorate together. The basis need not always widen or move in the same direction in every episode. <bookmark mark='c'/> Leverage and margin can transmit drawdowns into forced selling. Evaluate those channels with positions and funding data before assigning a cause to an observed loss."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a fund is long small caps and short CSI 300 futures. Small caps fall 20\%, the CSI 300 falls 5\%. "
                       r"What did the `market-neutral' fund lose, per unit of gross long?")
        with self.voiceover(
            "Pause and predict. A fund is long small caps and short futures on the large-cap index. Small caps fall twenty "
            "percent and the large-cap index five. What did the market-neutral fund lose?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
