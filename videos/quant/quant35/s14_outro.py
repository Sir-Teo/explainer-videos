from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from explainer.quant.house import micro as M
from videos.quant.quant35.common import (BAD, DEALER_C, FLOW_C, GOOD, INF_C, PART, PRICE_C, comma, load)

DESK = [
    (r"Why is there a spread when dealers are competitive and risk-neutral?",
     r"adverse selection: the ask is $\mathbb E[V \mid \text{buy}]$; from an even prior the spread equals the share of "
     r"informed traders (Glosten and Milgrom)"),
    (r"What is Kyle's lambda, and what sets it?",
     r"the price impact of a unit of net order flow: $\sigma_v/(2\sigma_u)$ in one auction, rising with what is unknown "
     r"and falling with noise"),
    (r"Why does a dealer shade its quotes when it holds inventory?",
     'to encourage inventory reduction; diffusing inventory exits fixed bounds, but financial ruin requires a separate wealth and capital model'),
    (r"When does Roll's spread estimator fail?",
     r"when the true bounce is tiny next to volatility and any reversal: daily data on liquid funds"),
    (r"What does VPIN measure?",
     'mean absolute bucket imbalance under bulk classification; the saved aggregate taker-window comparator is a different statistic, not true VPIN or informed probability'),
    (r"What made the flash crash possible?",
     r"a volume-targeted sell program, intermediaries passing inventory among themselves, and liquidity that withdrew "
     r"when inventory risk spiked"),
]

PROBLEMS = ['(basic 1) Quote heuristic: q=40, gamma=0.05, full spread 1. Derive bid and ask relative to fair value.', '(basic 2) Binary GM model: prior 0.5 and informed share 0.4. After a buy, derive the posterior and next bid/ask.', '(basic 3) One-auction Gaussian Kyle: double noise variance at fixed value variance. Compare lambda, order and expected profit.', '(basic 4) Roll covariance -0.0004 dollars squared: compute the full spread and state the identification assumptions.', '(basic 5) Descriptive flow slope 4.6 bp per million, flow 10 million. Compute fitted change; separately derive average cost on a permanent-linear execution path.', '(basic 6) Bulk classification: +2 standardized-return units, volume 1000 BTC. Compute assigned buys/sells and compare with possible balanced takers.', '(advanced 7) VECM alpha=(-0.9,0.1): derive common-trend weights. With equal independent innovation variances derive B information share.', '(advanced 8) Price 20 dollars, full spread 1 cent, natural full spread one third cent. Maker rebate 0.2 cent; then separately assume taker fee 0.2 cent. Derive one-way costs in bp.', '(advanced 9) Competitive per-fill model: adverse probability 0.02 and conditional loss 3 ticks; other costs zero. Derive the break-even full spread.', '(advanced 10) Sell 5 percent ADV at 9 percent of exogenous ADV/day. Compare independent volume doubling with own-generated turnover and state the clock.', '(qual 11) For fixed positive constant Kyle slope, derive the Ito verification identity and expected-profit bound. Specify admissibility, martingale integrability and terminal limits; verify the Gaussian bridge attains it.', '(qual 12) Derive one-auction Gaussian equilibrium and expected noise loss. Verify filtering in the continuous equilibrium and horizon T scaling at fixed noise variance rate; compare equal total noise variance.']


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("dealer"), load("gm"), load("kyle"), load("flow"), None, load("vpin"),
                   load("discovery"))
        self.desk()
        self.answers()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=25, color=col), wrapped_label(t, 11.6, 25)).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, dl, g, k, f, m, v, d):
        items = [
            ('a chosen linear quote heuristic controls inventory in the stipulated simulation; no universal ruin or optimality claim', DEALER_C),
            (r"the spread is insurance against the informed: ask $= \mathbb E[V \mid$ buy$]$", PRICE_C),
            (r"Kyle: $\lambda = \sigma_v/(2\sigma_u)$; half the information revealed in one auction", INF_C),
            ('daily liquidity proxies need assumptions; the planned ETF comparison is unavailable after frozen SPY rejection', BAD),
            (rf"Bitcoin: $\lambda$ = {f['full']['lambda']:.1f} bp per \$1m, concave; $R^2$ {f['agg']['1']['r2']:.2f} to "
             rf"{f['agg']['60']['r2']:.2f}", FLOW_C),
            (rf"VPIN: correlations {v['corr_rv']:.2f} with volatility; {v['corr_true']:.2f} with aggregate taker-window imbalance", INF_C),
            (rf"price discovery: one-minute bars cannot separate spot and perpetual (correlation {d['corr0']:.3f})", GOOD),
        ]
        items2 = [
            (r"Reg NMS, the NBBO, maker--taker, dark pools, wholesalers", PRICE_C),
            (r"the 2024 tick and fee amendments; T+1 from May 2024", PRICE_C),
            (r"high-frequency market makers: narrower spreads, faster discovery, sniping", DEALER_C),
            (r"6 May 2010 and 15 October 2014: liquidity withdrawn", BAD),
            (r"frequent batch auctions: compete on price, not speed", GOOD),
            (r"Rule 35: know who is on the other side", QC.HOUSE),
            (r"research: continuous Kyle, $\lambda = \sigma_v/\sigma_u$, profit $\sigma_v\sigma_u$, a Brownian bridge",
             INF_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 35 in fourteen lines")
        self.add(head, rows[0])
        with self.voiceover(
            "Part thirty-five's distinctions. Inventory control is illustrated by a specified heuristic, not a universal ruin theorem. Glosten and Milgrom derive conditional zero-profit quotes; Gaussian Kyle derives a strategic equilibrium. Daily-price liquidity proxies have assumptions, and our planned ETF comparison is unavailable. Bitcoin's saved slopes describe same-bar association. VPIN's comparator uses different bucket aggregation. Hasbrouck's wide ranges describe model-dependent attribution, not a causal leadership verdict."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 35 in fourteen lines")
        self.add(head, rows[0])
        with self.voiceover(
            'Market rules and venue design change which orders meet, but dated descriptions are not current legal guidance. High-frequency trading includes liquidity provision and stale-quote strategies; historical stress episodes involve interacting mechanisms. Batch auctions alter some speed incentives under their design assumptions. Proposed Rule thirty-five documents measurement and execution evidence. The continuous Gaussian theorem requires verified pricing, admissible trading and matched noise normalization; the finite Euler paths retain endpoint error.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=25) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Six desk questions. Why is there a spread when dealers are competitive and risk-neutral? Adverse selection. "
            "<bookmark mark='a'/> What is Kyle's lambda? The price of a unit of flow. <bookmark mark='b'/> Why does a "
            "dealer shade its quotes? To unwind its inventory."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "When is a daily spread estimate credible? Check constant-spread, efficient-price and trade-sign assumptions, then compare with aligned quote evidence. <bookmark mark='a'/> What does VPIN measure? Its constructed bulk-classified mean absolute bucket imbalance, not an identified informed probability. <bookmark mark='b'/> What do stress reports establish? Dated evidence about interacting mechanisms, rather than a universal single cause. The notes state the mathematical assumptions separately."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        a1, b1 = M.gm_quotes(0.7, 0.4)
        roll = 2 * math.sqrt(0.0004)
        from scipy.stats import norm
        buy = 1000 * norm.cdf(2.0)
        pages = [
            [(r"Dealer: q=40, shading 0.05, full spread 1", r"Mid is v-2; bid v-2.5 and ask v-1.5, under the specified heuristic."),
             (r"GM: one buy at prior 0.5, mu=0.4", rf"Posterior 0.7. Next bid {b1:.3f}, ask {a1:.3f}; the executed ask was 0.7."),
             (r"One auction: noise variance doubles", r"Noise standard deviation grows by sqrt(2); lambda scales by 1/sqrt(2), beta and expected profit by sqrt(2).")],
            [(r"Roll covariance -0.0004 dollars squared", rf"Full spread estimate is \${roll:.2f}; its interpretation needs the Roll assumptions, not just a negative sample covariance."),
             (r"Flow slope 4.6 bp per million; flow 10 million", r"Fitted change 46 bp. Under a separately stipulated permanent-linear execution path, average shortfall 23 bp. Real causal cost is not identified."),
             (r"Bulk classification: a +2 sigma bar", rf"Assigned buys {buy:.2f}, sells {1000-buy:.2f} BTC. Recorded takers could still split 500/500; informed probability is not identified.")],
            [(r"VECM alpha=(-0.9,0.1)", r"Common-trend weights (0.1,0.9). With equal independent innovations, B information share is 0.81/0.82=0.9878; not 0.9."),
             (r"Twenty dollars, one-cent full spread", r"Half-spread 2.5 bp. A maker rebate gives no taker fee. Separately stipulating 0.2-cent taker fee gives 3.5 bp, 4.2 times the natural half-spread."),
             (r"Chosen per-fill adverse probability 0.02; loss 3 ticks", r"Half-spread must cover 0.06 tick: full spread 0.12 tick before other costs. Unconditional news frequency is insufficient.")],
            [(r"Five percent ADV at nine percent of an exogenous ADV/day clock", r"Time 5/9 day. Independently doubling that liquidity rate halves time; own turnover does not establish extra external capacity."),
             ('Continuous Gaussian Kyle: value SD=2, noise diffusion=1', r"At T=1: lambda=2, price diffusion=2, expected profit=2. At T=4: lambda=1, price diffusion=1, expected profit=4; noise variance rate fixed.")],
        ]
        def show(page):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=25) for q_, a_ in page]).arrange(DOWN, buff=0.22)
            if cards.height > 6.9:
                cards.scale_to_fit_height(6.9)
            return cards
        cards = show(pages[0])
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(f"The first answers. The heuristic mid is two below value, with bid minus two point five and ask minus one point five. <bookmark mark='a'/> After a buy the belief is point seven; the next bid is {b1:.2f}, ask {a1:.3f}. <bookmark mark='b'/> Doubling noise variance multiplies its standard deviation by square root two, scales one-auction lambda down by that factor, and scales the fixed-gap order and unconditional expected profit up by it.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()
        cards = show(pages[1])
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(f"Roll gives {roll:.2f} dollars under its identity. A negative sample covariance does not establish all its assumptions. <bookmark mark='a'/> The fitted flow change is forty-six basis points. Only under a separate permanent-linear path does average execution shortfall equal twenty-three, with no spread or fees. <bookmark mark='b'/> Bulk classification assigns {buy:.2f} Bitcoin to buys and {1000-buy:.2f} to sells, even if recorded taker volumes are balanced. This cannot identify informed probability.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()
        cards = show(pages[2])
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover("The adjustment vector gives common-trend weights point one and point nine. With equal independent innovations B's information share is point nine eight seven eight, a different object. <bookmark mark='a'/> At twenty dollars the quoted half-spread is two point five basis points. A maker rebate leaves taker fees unknown; separately assuming a point two cent taker fee gives three point five basis points. <bookmark mark='b'/> In the chosen per-fill loss model, point zero two times three ticks is point zero six tick, requiring full spread point one two tick before other costs.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()
        cards = show(pages[3])
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover("On the specified exogenous volume clock, time is five ninths of a day. Independent external liquidity doubling halves it; turnover generated by the order itself does not prove doubled capacity. <bookmark mark='a'/> In continuous Gaussian Kyle, prior value spread two and noise diffusion one give lambda two, price diffusion two and expected profit two over one year. With the same noise variance rate over four years, lambda and price diffusion become one, while expected profit becomes four. These are model quantities with a fixed information and admissibility structure.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS[:6], font_size=23, title=r"Six basic problems")
        self.add(ps.head, ps.rows[0])
        with self.voiceover("Six basic problems state their models: quote shading, binary Bayesian quotes, one-auction noise scaling, the Roll identity, a fitted flow change against a separately assumed execution path, and bulk-volume classification. Derive the quantities with units and distinguish estimation from identification. Full English and Chinese solutions are in the notes."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
        self.clear_scene()
        ps = problem_set(PROBLEMS[6:10], font_size=23, title=r"Four advanced problems")
        self.add(ps.head, ps.rows[0])
        with self.voiceover("Four advanced problems distinguish common-trend weights from information shares, maker rebates from taker costs, per-fill adverse losses from news frequency, and exogenous liquidity clocks from own-generated turnover. Every numerical answer needs its stated denominator and model assumptions."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
        self.clear_scene()
        ps = problem_set(PROBLEMS[10:], font_size=25, title=r"Two qualifying problems")
        self.add(ps.head, ps.rows[0])
        with self.voiceover("Two qualifying problems prove the Ito profit identity with admissibility and terminal limits, then derive one-auction equilibrium and verify continuous Gaussian pricing with horizon units. The quadratic terminal penalty is not arbitrary terminal value. Formal HJB cancellation alone is insufficient. Match total noise variance before comparing profits."):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=3))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the limit order book: queues, ticks and fill probabilities", [36]),
            ('execution: costs, constraints, information and order scheduling', [37]),
            (r"market making: the dealer, with inventory and adverse selection together", [38]),
            (r"digital-asset markets: venues, perpetuals and funding", [39]),
        ])
        self.add(card.head, card.rows[0])
        with self.voiceover(
            'The next subjects separate related problems. Part thirty-six studies order-book queues, ticks and fills. Part thirty-seven studies execution schedules under specified objectives, costs and constraints, which need not equal the informed Kyle strategy. Part thirty-eight combines inventory and adverse selection in market making. Part thirty-nine studies digital-asset venues and derivatives.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"O'Hara, \textit{Market Microstructure Theory} (1995)",
             r"Hasbrouck, \textit{Empirical Market Microstructure} (2007)",
             r"Foucault, Pagano and R\"oell, \textit{Market Liquidity} (2013)",
             r"Harris, \textit{Trading and Exchanges} (2003)"],
            [r"Garman (1976); Ho--Stoll (1981); Roll (1984); Kyle and Glosten--Milgrom (1985); Back (1992)",
             r"Hasbrouck (1995); Easley et al.\ (1996, 2012); Amihud (2002); Corwin--Schultz (2012)",
             r"Menkveld (2013); Andersen--Bondarenko and Brogaard et al.\ (2014); Budish et al.\ (2015)",
             r"CFTC--SEC (2010); Treasury joint staff (2015); Kirilenko et al.\ (2017). Full list in the notes."], font_size=22)
        self.add(card)
        with self.voiceover("The textbooks and cited papers provide theory and dated empirical accounts. Current calculations use nine verified unchanged ordinary outputs from stipulated simulations and Binance's frozen public archive. The planned Yahoo comparison failed frozen SPY validation and is omitted. Chosen arithmetic is labeled as such. Not every attributed historical claim is computed by this code, and current legal outcomes and production pronunciation are not certified by these visual checks."):
            self.play(FadeIn(card))
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("compliance", "data"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 36, The Limit Order Book", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        self.add(chart)
        with self.voiceover(
            "The House now has a research framework for asking who may be on the other side, what is actually observed and what assumptions support a measurement. It has not identified each trader's private information or established a deployed execution or surveillance system. <bookmark mark='a'/> Next, Part thirty-six: order-book queues, minimum ticks and the probability of a resting fill before prices change."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
