from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import (
    ARB_C,
    BAD,
    FEE_C,
    GOOD,
    PART,
    PERP_C,
    POOL_C,
    STABLE_C,
    load,
)

DESK = [
    (r"An LP in an $x \cdot y = k$ pool; the price doubles. Loss against holding?",
     r"$2\sqrt2/3 - 1 = -5.7\%$; but the right measure is the loss against rebalancing, $\sigma^2/8$ of value per unit "
     r"of time, which accrues whatever the end price"),
    (r"What does a pool lose to arbitrage?",
     r"$\ell = \tfrac12\sigma^2P^2|x^{*\prime}(P)|$; for constant product $\sigma^2 V/8$: 2.66\% on ether's 2023"),
    (r"Why concentrate liquidity, and when not to?",
     r"it multiplies fees and LVR by the range's efficiency ($41\times$ at $\pm5\%$): a bet that fees beat variance; "
     r"withdraw when volatility is high"),
    (r"What keeps a perpetual near spot?",
     r"funding, paid by longs when it trades above; $F = \kappa S/(\kappa - (r - q))$; on Binance, 0.01\% per 8 hours "
     r"when the premium is small"),
    (r"Is the cash-and-carry trade free money?",
     r"a premium for supplying leverage, with a hold-out Sharpe ratio of 2.2; its tail is the venue and the stablecoin, "
     r"which no backtest contains"),
    (r"When does a stablecoin break?",
     r"when its reserves are illiquid at the moment of redemption (USDC at 88 cents on a weekend) or are its own "
     r"token (UST and LUNA)"),
]

PROBLEMS = [
    r"Impermanent loss at a price ratio of 4, and of $\tfrac14$.",
    r"A pool holds 1,000 ETH and \$2m. The cost of buying 50 ETH with no fee, and the average price.",
    r"LVR of a \$10m constant-product pool at 80\% volatility, per year and per day.",
    r"The exact one-block loss if the price doubles within one block, against the continuous rate's estimate.",
    r"Capital efficiency of the range $[P/1.21,\ 1.21P]$, and its LVR per dollar against full range.",
    r"Fee 0.3\%, volatility 5\% a day, 12-second blocks: $\eta$ and the probability that a block holds an arbitrage.",
    r"Funding of 0.01\% every 8 hours on a cash-and-carry book with a third margin: the return on capital.",
    r"$r - q = 5\%$ a year and funding intensity of three a day: the perpetual's premium over spot.",
    r"A 10\% carry with 25\% of capital at the venue: the annual failure probability that cancels it.",
    r"Reserves 70\% liquid, the rest sold at a 30\% discount: what the last redeemers receive in a full run.",
    r"(qual) Prove the LVR theorem for a general constant-function market maker; derive the constant-product and "
    r"concentrated rates, the exact one-step loss and its expectation $V_0(1 - e^{-\sigma^2\Delta t/8})$.",
    r"(qual) With Poisson blocks of rate $\lambda$ and fee $\gamma$, derive the mispricing's stationary density and "
    r"$P_{\text{trade}} = 1/(1 + \gamma\sqrt{2\lambda}/\sigma)$; give the limits as $\gamma \to 0$ and $\lambda \to \infty$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("lvr"), load("fees"), load("v3"), load("funding"), load("carry"), load("stable"))
        self.lessons()
        self.formulas()
        self.connections()
        self.desk()
        self.answers()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, lv, fe, v3, fu, ca, st):
        f3 = [x for x in fe["eth"] if abs(x["fee"] - 0.003) < 1e-9][0]
        e5 = [r for r in v3["rows"] if abs(r["w"] - 1.05) < 1e-9][0]
        items = [
            (r"two venues: custodial exchanges and contracts on chain; FTX showed what custody means", BAD),
            (r"a constant-product pool's price is its reserves' ratio; arbitrageurs keep it honest", POOL_C),
            (r"impermanent loss depends only on the end price; LVR on the path", ARB_C),
            (rf"LVR = $\sigma^2/8$ of value: ether's 2023, {lv['lvr_pct']:.2f}\% measured, {lv['rv8_pct']:.2f}\% predicted",
             ARB_C),
            (rf"concentration multiplies fees and LVR: ${e5['eff']:.0f}\times$ at $\pm5\%$", POOL_C),
            (r"a learned LP's skill: stop selling volatility when it is high", GOOD),
        ]
        items2 = [
            (r"the order of transactions is worth money: sandwiches, liquidations, arbitrage", BAD),
            (rf"funding holds the perpetual to spot; on Bitcoin {100 * fu['BTCUSDT']['at_base']:.0f}\% of settlements at "
             r"0.01\%", PERP_C),
            (rf"the carry book, registered: Sharpe {ca['res']['sharpe']:.1f} promised, {ca['hold']['sharpe']:.1f} delivered",
             PERP_C),
            (r"its real tail is the venue: a quarter of capital sits at the exchange", BAD),
            (rf"stablecoins are uninsured banks: USDC at {st['usdc']['low']:.2f}, UST and LUNA to nothing", STABLE_C),
            (rf"research: LVR proved; fees and blocks; real prices give arbitrageurs {f3['arb_lvr']:.2f} at 0.3\%", GOOD),
            (r"Rule 39: count the risks the returns do not show", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 39 in thirteen lines")
        with self.voiceover(
            "Part thirty-nine in thirteen lines. Crypto trades on custodial exchanges and on contracts on chain, and FTX "
            "showed what custody means. A pool's price is the ratio of its reserves, kept honest by arbitrageurs. "
            "Impermanent loss depends only on where the price ends; the loss to arbitrage depends on the path, and is "
            "variance over eight of the pool's value, which ether's twenty twenty-three confirmed to the second decimal. "
            "Concentration multiplies both fees and loss, and a learned provider's only skill was to stop selling "
            "volatility when it was high."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 39 in thirteen lines")
        with self.voiceover(
            "The order of transactions is worth money. Funding holds the perpetual to spot, and on Bitcoin it sat at "
            "exactly the interest term at over a third of settlements. The registered carry book delivered about half "
            "its promise, still with a high Sharpe ratio, and its real tail is the venue. Stablecoins are uninsured "
            "banks. The research chapter proved the loss to arbitrage, and how fees and blocks split it. And the House's "
            "rule: count the risks the returns do not show."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the old models, in new clothes", r"a pool is a market maker that is always sniped, a "
                          r"perpetual is a future with a funding clock, a stablecoin is a narrow bank", width=12.4,
                          font_size=19),
            desk_question(r"measure against the right benchmark", r"LVR, not impermanent loss; the rebalancing portfolio "
                          r"removes the market exposure and leaves the cost", width=12.4, font_size=19),
            desk_question(r"the backtest shows the market, not the plumbing", r"venues, contracts, keys and pegs fail in "
                          r"ways no return series contains, and they are the largest risks here", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> The old models, in new clothes: a pool is a market maker that is always "
            "sniped, a perpetual is a future with a funding clock, and a stablecoin is a narrow bank. "
            "<bookmark mark='b'/> Measure against the right benchmark: the rebalancing portfolio removes the market "
            "exposure and leaves the cost. <bookmark mark='c'/> And the backtest shows the market, not the plumbing: "
            "venues, contracts, keys and pegs fail in ways no return series contains."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = VGroup(
            MathTex(r"\frac{V_{\text{pool}}}{V_{\text{hold}}} - 1 = \frac{2\sqrt r}{1 + r} - 1", font_size=32, color=POOL_C),
            MathTex(r"\ell = \tfrac12\sigma^2P^2|x^{*\prime}(P)|,\qquad \ell_{\text{CPMM}} = \tfrac{\sigma^2}{8}V", font_size=32,
                    color=ARB_C),
            MathTex(r"\Delta\text{LVR} = \tfrac{V_0}{2}\bigl(\sqrt{P_1/P_0} - 1\bigr)^2", font_size=32),
            MathTex(r"\text{efficiency} = \frac{1}{1 - w^{-1/2}}", font_size=32, color=POOL_C),
            MathTex(r"P_{\text{trade}} = \frac{1}{1 + \gamma\sqrt{2\lambda}/\sigma},\quad \text{ARB} \approx P_{\text{trade}}\,"
                    r"\text{LVR}", font_size=32, color=FEE_C),
            MathTex(r"F = \frac{\kappa}{\kappa - (r - q)}\,S", font_size=32, color=PERP_C),
        ).arrange(DOWN, buff=0.3)
        head = label(r"The part on one card", font_size=34).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "The part on one card. Impermanent loss. The LVR rate and its constant-product form. The exact one-step loss. "
            "The capital efficiency of a range. The trade probability with fees and blocks, and arbitrage profit. And "
            "the perpetual's no-arbitrage price."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4, run_time=6))
            self.wait(2)
        self.clear_scene()

    def connections(self):
        cards = VGroup(
            desk_question(r"backwards", r"Part 38's stale quote is a pool's stale price; Part 11's short gamma is an "
                          r"LP's; Part 22's carry is funding; Part 2's margin account is the perpetual's", width=12.4,
                          font_size=19),
            desk_question(r"sideways", r"Part 21's counterparty risk is venue risk; Part 9's futures are the perpetual's "
                          r"dated cousins; Part 27's coins are this market's cross-section", width=12.4, font_size=19),
            desk_question(r"forwards", r"Part 40 measures risk in a market with fat tails and no close; Part 41's "
                          r"spirals ran through crypto in 2022; Part 42's machines include its bots", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How this part connects. <bookmark mark='a'/> Backwards: Part thirty-eight's stale quote is a pool's stale "
            "price, Part eleven's short gamma is a provider's, Part twenty-two's carry is funding, and Part two's margin "
            "account is the perpetual's. <bookmark mark='b'/> Sideways: Part twenty-one's counterparty risk is venue "
            "risk, and Part nine's futures are the perpetual's dated cousins. <bookmark mark='c'/> Forwards: Part forty "
            "measures risk in a market with fat tails and no close, Part forty-one's spirals ran through crypto in twenty "
            "twenty-two, and Part forty-two's machines include its bots."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. A provider's loss against holding when the price doubles? Five point seven percent, but "
            "the right measure is the loss against rebalancing. <bookmark mark='a'/> What does a pool lose to arbitrage? "
            "Variance over eight of its value. <bookmark mark='b'/> Why concentrate liquidity? To multiply a bet that "
            "fees beat variance, and so not when volatility is high."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "What keeps a perpetual near spot? Funding. <bookmark mark='a'/> Is the carry trade free money? No: a premium "
            "with a tail no backtest holds. <bookmark mark='b'/> And when does a stablecoin break? When its reserves are "
            "illiquid at the moment of redemption, or are its own token. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        cards = VGroup(
            desk_question(r"Research: volatility doubles", r"LVR $\propto \sigma^2$, so it quadruples", width=12.4,
                          font_size=20),
            desk_question(r"the arbitrageurs' share", r"$\eta \propto 1/\sigma$ halves from 1 to $\tfrac12$: $P_{\text{trade}}$ "
                          r"rises from $\tfrac12$ to $\tfrac23$, so arbitrageurs keep two-thirds of a loss four times as "
                          r"large, and fees recover a smaller share", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The research chapter's pause, answered. <bookmark mark='a'/> Loss-versus-rebalancing is proportional to the "
            "variance, so it quadruples. <bookmark mark='b'/> And eta, inversely proportional to volatility, halves from "
            "one to a half, so the trade probability rises from a half to two thirds: arbitrageurs keep two thirds of a "
            "loss four times as large, and fees recover a smaller share of it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: impermanent loss; a trade's cost on the curve; LVR in dollars; the exact one-block "
            "loss; a range's efficiency; the trade probability; the carry book's return; the perpetual's premium; the "
            "venue risk that cancels the carry; and a run. Then two qualifying-exam problems: the LVR theorem in full, "
            "and arbitrage with fees and Poisson blocks. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"risk in a market with fat tails, no close and many venues", [40]),
            (r"leverage and liquidity spirals: 2022's crypto chain of failures", [41]),
            (r"bots and learning agents that trade, quote and order blocks", [42]),
            (r"whether anyone can beat the market, and what they pay to try", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part forty measures risk in markets with fat tails and no close. Part forty-one "
            "follows leverage and liquidity spirals, of which crypto's twenty twenty-two was a chain. Part forty-two "
            "builds the machines that trade, quote and order blocks. And Part forty-three asks whether anyone can beat "
            "the market."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Harvey, Ramachandran and Santoro, \textit{DeFi and the Future of Finance} (2021); Narayanan, Bonneau, "
             r"Felten, Miller and Goldfeder, \textit{Bitcoin and Cryptocurrency Technologies} (2016)"],
            [r"Diamond and Dybvig (1983); Nakamoto (2008); Buterin (2014); Angeris and Chitra (2020); Daian et al. "
             r"(2020); Makarov and Schoar (2020); Capponi and Jia (2021); Liu and Tsyvinski (2021); Liu, Tsyvinski and Wu "
             r"(2022)",
             r"Milionis, Moallemi, Roughgarden and Zhang (2022); He, Manela, Ross and von Wachter (2022); Milionis, "
             r"Moallemi and Roughgarden (2023); Lyons and Viswanath-Natraj (2023); Liu, Makarov and Schoar (2023); Lehar "
             r"and Parlour. Data: Binance's public archive; Yahoo Finance"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Diamond and Dybvig's bank run to the "
            "theory of loss-versus-rebalancing. Every number on screen was computed by the House's code from Binance's "
            "public archive, Yahoo Finance's bars, or simulation."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("digital",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 40, Measuring Risk", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Act six is complete: the House can now see who trades with whom, read the book, execute, make markets, and "
            "trade on chain, and its trading desks are all open. <bookmark mark='a'/> Next, Act seven, the system. Part "
            "forty: measuring risk. Value at risk, expected shortfall, and how to tell whether a risk model works."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
