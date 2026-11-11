from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, GOOD, OIL, PART, USD, ask, fit_right, illustration, load


class Roll(VoiceoverScene):
    def construct(self):
        o = load("oil_public_example")
        self.card()
        self.decompose()
        self.mechanics()
        self.index(o)
        self.years(o)
        self.premium()
        self.optiver()

    def card(self):
        c = chapter_card(8, r"The roll and the commodity premium", r"What does holding futures pay?", lit=(2006,),
                         part=PART)
        with self.voiceover("Chapter eight. Rolling futures: what an investor in commodities actually earns."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def decompose(self):
        rows = [cmath(r"\frac{F_{t+1,T} - F_{t,T}}{F_{t,T}}", r"\approx", r"\underbrace{\frac{S_{t+1} - S_t}{S_t}}_{"
                      r"\text{spot}} + \underbrace{\frac{F_{t+1,T} - S_{t+1}}{S_{t+1}} - \frac{F_{t,T} - S_t}{S_t}}_{"
                      r"\text{the curve rolls toward spot}}", font_size=30),
                cmath(r"\text{roll yield}", r"\approx", r"-\frac{1}{T_2 - T_1}\ln\frac{F_{T_2}}{F_{T_1}}", font_size=38,
                      colors={r"\text{roll yield}": BASIS})]
        whys = [why(r"a future converges to the spot price as it expires: a holder earns the spot's move plus the "
                    r"convergence, which is positive when the future started below spot"),
                why(r"so an investor who keeps buying the next contract and selling the expiring one earns the curve's "
                    r"slope: positive in backwardation, negative in contango, every month")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "A futures contract has zero initial value when entered at its market delivery price. The difference between two contract prices is not an immediate cash payment to buy the next one. A held contract's subsequent price changes determine its marked profit. The first equation is a small-basis first-order decomposition around spot. <bookmark mark='a'/> The negative curve slope is a useful convergence or roll-yield approximation if the curve evolves in a specified stable way. Contango alone does not determine the realized return: spot and the whole curve can move. The next screens use an explicitly fixed convergence example, with the funding, collateral and monthly reset assumptions stated."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def mechanics(self):
        rows = [cmath(r"T_{\text{last}}", r"=", r"\text{the 25th of the month before delivery} - 3\ \text{business days}",
                      font_size=34, colors={r"T_{\text{last}}": BAD})]
        whys = [why(r"NYMEX's rule for WTI: the May 2020 contract stopped trading on 21 April 2020. An index holds "
                    r"the next contract, rolling early in each month (here on the fifth trading day), as the large "
                    r"commodity indices do, so it never holds a contract into its last days")]
        step = ladder(self, rows, whys, keep=1, top=2.2, x=-0.4, buff=0.8, edge=6.9)
        box = VGroup(
            label('An account needs an explicit collateral and sizing convention', font_size=24, color=OIL),
            wrapped_label('A fraction of futures price is not automatically a return on capital. Declare backing cash, contracts held, variation margin, collateral yield, funding and roll costs. No legacy performance is certified here.', 11.0, 19, GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "A rolling rule must identify delivery months and the exchange trading calendar. WTI normally stops trading three business days before the twenty-fifth of the month preceding delivery; if that date is not a business day, the rule refers to the preceding business day. <bookmark mark='a'/> Holding contract two until it is renumbered as contract one is different from jumping mechanically between continuous-series identifiers. The original fixed fifth-trading-day rule is left unchanged, but its historical performance cannot be restored under the recorded EIA hashes in this pass. We therefore do not substitute a new historical return series. Cash collateral, variation margin, transaction costs and funding belong in any implementable account."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(box))
        self.wait(0.4)
        self.clear_scene()

    def index(self, o):
        monthly = 100.0 / 105.0 - 1.0
        annual = (1.0 + monthly) ** 12 - 1.0
        rows = VGroup(
            label(r"Fixed convergence example: no historical performance", font_size=28, color=BASIS),
            MathTex(r"S=100,\quad F_0=105,\quad F_T=100", font_size=36),
            MathTex(r"r_1=\frac{100-105}{105}=-4.76\%", font_size=36, color=BAD),
            MathTex(r"(1+r_1)^{12}-1=" + f"{100 * annual:.1f}" + r"\%", font_size=36, color=BASIS),
            wrapped_label(r"One-times entry notional, reset monthly; fixed spot and curve; zero cash yield; no costs. Futures enter at zero value; convergence produces the P\&L.", 11.8, 20, GREY_A),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover("Here is a fixed arithmetic illustration, not a historical return series. Suppose spot stays at one hundred, each new one-month future is one hundred and five, and it converges to one hundred at settlement. Back each position by cash equal to its entry notional, reset that one-times exposure each month, and assume zero collateral yield and no trading or funding costs. <bookmark mark='a'/> One month's loss is five divided by one hundred and five, about four point eight percent. The five-dollar difference is earned or lost through subsequent convergence, not an upfront fee for replacing a zero-value future. <bookmark mark='b'/> Repeating exactly these assumptions for twelve months gives about forty-four percent loss. It is not sixty percent, and it is not the return of a real oil fund. A changing term structure, different leverage or cash interest would change the account.") as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[4]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    def years(self, o):
        outcomes = [80.0, 100.0, 125.0]
        title = label(r"One initial curve, three hypothetical settlements", font_size=30).to_edge(UP, buff=0.4)
        cards = VGroup(*[desk_question(rf"Settlement {value:.0f}", rf"$(F_T-105)/105 = {100*(value/105-1):+.1f}\%$; cash backing 105", width=12.0, font_size=24) for value in outcomes]).arrange(DOWN, buff=0.3)
        foot = wrapped_label(r"Initial spot 100, future 105 in every case. Initial contango alone does not fix the future price path, account P\&L or margin calls.", 12.0, 21, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover("The same initial contango permits different realized outcomes. Keep entry spot at one hundred and the one-month future at one hundred and five. Now consider three explicitly hypothetical settlement prices: eighty, one hundred, and one hundred and twenty-five. <bookmark mark='a'/> On cash backing equal to the entry futures notional, their returns are about minus twenty-four, minus five, and plus nineteen percent. All three began with the identical upward curve. <bookmark mark='b'/> This separates an initial slope from a realized return. Even a profitable final settlement can require large interim variation margin, and a trader unable to meet it may exit early. Historical continuous prices need contract mapping and an account convention before they can support a performance claim.") as vo:
            self.play(FadeIn(title), FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]), FadeIn(cards[2]))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def premium(self):
        rows = [cmath(r"\mathbb{E}[F_{T,T}] - F_{t,T}", r"=", r"\mathbb{E}[S_T] - F_{t,T}\ \ (\text{the risk premium})",
                      font_size=36, colors={r"\mathbb{E}[F_{T,T}] - F_{t,T}": GOOD})]
        whys = [why(r"Keynes's normal backwardation (1930): producers hedge by selling futures, so speculators who buy "
                    r"them are paid to bear the risk; the future sits below the expected spot")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        cards = VGroup(
            desk_question(r"Gorton and Rouwenhorst (2006)", r"an equal-weighted index of commodity futures, 1959--2004: "
                          r"about the same excess return and Sharpe ratio as US stocks, with negative correlation to "
                          r"stocks and bonds, and positive to inflation", width=12.0, font_size=20),
            desk_question(r"and since", 'after 2004 index money poured in and many curves sat in contango; broad commodity indices returned far less. The original WTI strategy cache is blocked by changed EIA raw hashes; fixed arithmetic above is not a replacement performance estimate', width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A long futures position's expected delivery profit is expected future spot minus today's delivery price, under the physical expectation. Keynes's normal-backwardation argument offers one reason that premium might be positive: producers may pay others to bear price risk. It is a hypothesis, not a theorem that all futures pay a positive premium. <bookmark mark='a'/> Gorton and Rouwenhorst reported favorable historical results for a diversified commodity-futures sample through 2004; that finding depends on dates, portfolio construction and collateral treatment. <bookmark mark='b'/> Later results differ across windows and contracts. A published premium, investment flows and subsequent returns do not by themselves identify a causal crowding effect. This pass leaves the original WTI strategy cache unavailable, rather than reporting a newly reconstructed historical performance."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def optiver(self):
        cc = crisis_card(r"March 2007", r"Optiver and the close",
                         r"the CFTC alleged that the trading firm made 19 attempts over 11 days to move NYMEX crude oil, "
                         r"heating oil and gasoline futures settlement prices by trading heavily into the close, "
                         r"'banging the close', to profit on positions priced at the settlement; settled in 2012 without "
                         r"admitting or denying the allegations",
                         stats=[(r"\$13\text{m} + \$1\text{m}", r"civil penalty and disgorgement (2012)"),
                                (r"19", r"alleged attempts in 11 days")], width=8.8, font_size=19).move_to(UP * 0.3)
        foot = wrapped_label(r"the roll and the settlement are where index money is most predictable; Part 34 returns to "
                             r"manipulation and surveillance", 11.0, 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Settlement prices matter: index rolls, and many contracts, are priced at them. In 2008 the Commodity "
            "Futures Trading Commission charged the trading firm Optiver with trying, nineteen times over eleven days "
            "in March 2007, to push crude, heating oil and gasoline settlement prices by trading heavily into the "
            "close. <bookmark mark='a'/> It settled in 2012 for a thirteen million dollar penalty and a million in "
            "disgorgement, without admitting or denying the charges. Where flows are predictable, someone will try "
            "to trade against them."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.add(illustration(r"CFTC press releases 5521-08 (July 2008) and 6239-12 (April 2012)"))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"an oil fund holds the front-month future and the curve is in 5\% a month contango. If the spot price "
                r"stays flat for a year, roughly what does the fund lose?")
        with self.voiceover("An oil fund holds the front-month future, and the curve is in five percent a month "
                            "contango. If the spot price stays flat for a year, roughly what does the fund lose?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
