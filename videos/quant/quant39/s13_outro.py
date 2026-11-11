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

DESK = [('A fee-free constant-product pool; price doubles. Loss against holding?', '$2\\sqrt2/3-1=-5.72\\%$ relative to terminal hold value; LVR uses a different benchmark'), ('What does the continuous fee-free pool lose against rebalancing?', "$-\\tfrac12\\int V''(P_t)\\,d[P]_t$ with common initial wealth and local regularity; CPMM local rate $\\sigma^2V/8$"), ('Does a narrower range always improve LP performance?', 'no: local centre efficiency scales curvature; fees also depend on active volume, competition, exits and costs'), ('What keeps a perpetual near spot?', 'funding incentives, subject to constraints; the proportional continuous solution requires constant coefficients, $\\kappa>r-q$ and transversality'), ('Does a matched-unit carry hedge remove every risk?', 'basis, funding, margin liquidity, collateral currency, custody, execution and venue risks remain'), ('Does a stablecoin quote below a reserve stress prove illiquidity?', 'no: inspect reserve values, other claims, redemption rights, timing and quote currency; accounting alone does not identify the cause')]

PROBLEMS = ['Fee-free constant product: compute relative impermanent loss for price ratios $4$ and $1/4$.', 'A pool has 1,000 ETH and \\$2m. With no fee, find payment and average price for buying 50 ETH.', 'At current value \\$10m and annual sigma 80\\%, find the local LVR rate in dollars per year and per calendar day.', 'A single price ratio is $2$. Derive exact discrete LVR/$V_0$; explain why this endpoint does not determine quadratic variation.', 'For $[P/1.21,1.21P]$, compute centre efficiency and the local in-range LVR multiple per dollar.', 'Driftless log price, mean Poisson block 12 s, sigma 5\\%/sqrt(day), input fee 0.3\\%: use $\\gamma=-\\log(1-f)$ to find $\\eta$ and trade probability.', 'Chosen constant funding 0.01\\% per 8 h, fixed notional, one-third cash margin, zero basis/costs: find simple annual return on committed capital.', 'Continuous funding: $r-q=5\\%$/year, $\\kappa=3$/day. Under constant coefficients and transversality, find $F/S-1$.', 'A one-year chosen book returns $+10\\%$ if no venue failure and $-25\\%$ if failure. Find the failure probability giving zero expected simple return.', 'Chosen liquidation: 70\\% liquid at par, other assets haircut 30\\%. Find aggregate coverage; under upfront liquidation and sequential par payouts, who is unpaid? Does this prove a run equilibrium?', '(qual) Under explicit regularity and common initial wealth, prove the continuous LVR identity, concentrated boundary case, exact CPMM step gap and conditional lognormal expectation. Add the jump concavity gap.', '(qual) For driftless Brownian log mispricing and independent Poisson edge resets, derive the stationary density, flux balance, normalization and $P_{trade}$. Distinguish log-band/input fee and probability/profit limits.']


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("lvr"), load("fees"), load("v3"), load("funding"), load("stable"))
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
        rows=VGroup()
        for j,(text,col) in items:
            row=VGroup(MathTex(str(j),font_size=28,color=col),wrapped_label(text,11.5,26)).arrange(RIGHT,buff=0.28)
            rows.add(row)
        rows.arrange(DOWN,aligned_edge=LEFT,buff=0.22)
        if rows.height>6.0:rows.scale_to_fit_height(6.0)
        head=label(title,font_size=32).to_edge(UP,buff=0.35)
        rows.next_to(head,DOWN,buff=0.35)
        return head,rows

    def recap(self, lv, fe, v3, fu, st):
        items = [
            (r"custodial venues and contracts on chain have different risks", BAD),
            (r"a fee-adjusted swap invariant differs from a fee-retaining reserve product", POOL_C),
            (r"holding and rebalancing are distinct benchmarks", ARB_C),
            (rf"ETH local normalized loss sum {lv['lvr_pct']:.2f}\%; log-increment squares / 8: {lv['rv8_pct']:.2f}\%", ARB_C),
            (r"concentration scales local curvature; fee income is conditional", POOL_C),
            (r"the learner is a chosen contextual-bandit reward experiment", GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 39: definitions and measurements")
        with self.voiceover("Six definitions and measurements. Custodial venues and contracts on chain have different exposures. A fee-adjusted swap invariant differs from a reserve product that grows with retained fees. Holding and self-financing rebalancing answer different questions. The ether figures are changing-denominator normalized sums, compared with a small-step squared-log relation. Concentration scales local curvature, while realized fee income also depends on time in range and competition. The learned provider is a contextual-bandit experiment in an assumed world, without a claim of live investment performance."):
            self.play(FadeIn(head), FadeIn(rows))
        self.wait(0.5)
        self.clear_scene()
        items = [
            (r"ordering-attack outputs are bounded feasible candidates, not verified profit optima", BAD),
            (r"funding annualization is not a financed strategy return", PERP_C),
            (r"matched carry retains basis, collateral, venue and execution risks", PERP_C),
            (r"25\% venue loss is one chosen zero-recovery accounting stress", BAD),
            (rf"USDC sample low {st['usdc']['low']:.3f} is a venue quote in tether", STABLE_C),
            (r"fee-band probability and profit comparisons have different assumptions", GOOD),
            (r"Rule 39 is a proposed research and risk checklist", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 7)), r"Part 39: economic interpretation")
        with self.voiceover("Seven interpretation checks. A largest-feasible attack is not automatically profit-optimal. A simple funding annualization is not a strategy return on committed capital. Matched-unit carry still has basis, funding, collateral, venue and execution risks. The quarter-capital venue loss is a chosen zero-recovery stress. A USDC quote in tether is not a direct dollar redemption valuation. The stationary fee-band probability and the leading-order profit comparison have distinct assumptions. Finally, the proposed House rule organizes research and exposures; the lecture supplies no deployment or capital approval."):
            self.play(FadeIn(head), FadeIn(rows))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the old models, in new clothes", 'a pool follows a specified swap rule; a perpetual has a funding clock; a reserve-backed token has issuer and redemption risks', width=12.4,
                          font_size=19),
            desk_question(r"measure against the right benchmark", 'holding and rebalancing answer different questions; hedging, execution and capital costs require separate accounting', width=12.4, font_size=19),
            desk_question(r"the backtest shows the market, not the plumbing", r"venues, contracts, keys and pegs fail in "
                          r"ways no return series contains, and they are the largest risks here", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three connections. <bookmark mark='a'/> The familiar tools return in new mechanisms: a pool follows a swap rule, a perpetual has a funding clock and a reserve-backed token has issuer and redemption risks. <bookmark mark='b'/> Choose the benchmark for the question. Holding and self-financing rebalancing measure different gaps, and a real hedge adds costs. <bookmark mark='c'/> Market returns alone need not reveal custody, contracts, collateral transfers or redemption access. A research design needs those operational exposures alongside its price model, without assuming any one reported return series is complete."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
        rows.next_to(head, DOWN, buff=0.25)
        scope=wrapped_label(r"Exact accounting, continuous local rates and asymptotic models have distinct assumptions; see the derivations.",12.0,17,GREY_A).to_edge(DOWN,buff=0.25)
        self.add(scope)
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
        self.add(cards[0])
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
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a, width=12.4, font_size=21) for q,a in qs]).arrange(DOWN,buff=0.25)
            if cards.height>7.1:cards.scale_to_fit_height(7.1)
            return cards
        cards=page(DESK[:3])
        with self.voiceover("Three pool questions. Price doubles in a fee-free constant-product pool: relative to terminal holding value the gap is minus five point seven two percent. <bookmark mark='a'/> The continuous rebalancing gap is a curvature-weighted quadratic-variation integral with common initial wealth and regularity assumptions. <bookmark mark='b'/> Narrowing a range scales local curvature, but cannot guarantee better net performance when volume, competition, exits and costs also change.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()
        cards=page(DESK[3:])
        with self.voiceover("Three institutional questions. Funding incentives help link a perpetual to spot, subject to constraints and the contract's rules. <bookmark mark='a'/> Matched-unit carry retains basis, funding, margin, custody and venue risks. <bookmark mark='b'/> A stablecoin quote below a reserve stress does not identify its cause. Reserve valuation, other claims, redemption rights, timing and quote currency all matter. The notes give the assumptions behind each answer.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def answers(self):
        cards = VGroup(
            desk_question(r"Research: volatility doubles", 'at fixed price/pool state, the fee-free local rate quadruples; whole-path losses can differ', width=12.4,
                          font_size=20),
            desk_question(r"the arbitrageurs' share", 'stationary reset model: $\\eta:1\\to1/2$, $P_{trade}:1/2\\to2/3$; profit scaling needs the separate leading-order approximation', width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "The research pause is conditional on the model. <bookmark mark='a'/> At the same price and pool state, doubling instantaneous sigma quadruples the fee-free local LVR rate. A realized whole-path loss need not be exactly four times. <bookmark mark='b'/> In the stationary driftless-log Poisson model, eta halves from one to one half, so trade probability rises from one half to two thirds. The leading-order profit comparison would scale by sixteen thirds relative to the original arbitrage profit, if its additional regularity and asymptotic approximation apply. It is not an exact finite-fee statement about all LP losses or fees."
        ) as vo:
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        def page(lo,hi,title):
            head=label(title,font_size=32,color=QC.IDEA).to_edge(UP,buff=0.35)
            rows=VGroup(*[wrapped_label(str(i+1)+". "+PROBLEMS[i],12.0,27) for i in range(lo,hi)])
            rows.arrange(DOWN,aligned_edge=LEFT,buff=0.32)
            if rows.height>6.0:rows.scale_to_fit_height(6.0)
            rows.next_to(head,DOWN,buff=0.35)
            return head,rows
        with self.voiceover("Twelve problems with complete bilingual solutions. Six basic problems cover relative impermanent loss, an exact curve trade, local dollar loss rates, a discrete doubling, multiplicative range efficiency and the exact log fee band. <bookmark mark='a'/> Four advanced problems distinguish simple funding return on committed capital, the continuous perpetual model, a fully specified failure-payoff calculation and sequential liquidation accounting. <bookmark mark='b'/> Two qualifying problems prove the continuous and discrete LVR identities with regularity and a jump extension, then derive the stationary reset density with flux balance, its probability limits and the conditions needed for profit comparisons. Each answer states its units and assumptions.") as vo:
            head,rows=page(0,6,r"Basic problems 1--6")
            self.play(FadeIn(head),FadeIn(rows))
            self.wait(3)
            vo.wait_until("a")
            self.clear_scene()
            head,rows=page(6,10,r"Advanced problems 7--10")
            self.play(FadeIn(head),FadeIn(rows))
            self.wait(3)
            vo.wait_until("b")
            self.clear_scene()
            head,rows=page(10,12,r"Qualifying problems 11--12")
            self.play(FadeIn(head),FadeIn(rows))
            self.wait(6)
        self.wait(1)
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
            [r"Harvey, Ramachandran and Santoro, \textit{DeFi and the Future of Finance} (2021)",
             r"Narayanan et al., \textit{Bitcoin and Cryptocurrency Technologies} (2016)"],
            [r"Diamond and Dybvig (1983); Nakamoto (2008); Buterin (2014)",
             r"Angeris and Chitra (2020); Daian et al. (2020); Makarov and Schoar (2020)",
             r"Capponi and Jia (2021); Liu and Tsyvinski (2021); Liu, Tsyvinski and Wu (2022)",
             r"Milionis et al. (2022), LVR; Milionis, Moallemi and Roughgarden (2023), fees",
             r"He, Manela, Ross and von Wachter (2022); Lyons and Viswanath-Natraj (2023)",
             r"Liu, Makarov and Schoar (2023); Lehar and Parlour; full citations in notes",
             r"Data: Binance public archive; Yahoo Finance"], font_size=23)
        with self.voiceover(
            'The notes connect the textbook chapters with primary papers and their assumptions, including the loss-versus-rebalancing identity and fee-band model. Computed ordinary outputs, chosen accounting examples and cited historical facts have distinct labels. The market samples do not turn the idealized simulator into a verified executable strategy, and historical legal milestones do not certify current product terms.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("digital",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 40, Measuring Risk", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Act six has built the tools to study dealers, books, execution, market making and on-chain mechanisms. The digital-assets desk remains a proposed research design with unresolved operational and investment validation. <bookmark mark='a'/> Next, Act seven studies the system. Part forty measures risk with value at risk and expected shortfall, and asks how to tell whether a risk model works."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
