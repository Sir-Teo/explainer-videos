from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, CARRY, FOR, GAS, INFL, OIL, PART, USD, load

DESK = [
    (r"Dollar rates are 5\% and yen rates 0\%. Is the yen forward at a premium or a discount?",
     r"at a premium: by covered parity, in yen per dollar, F/S = 1.00/1.05, so a dollar buys about 5\% fewer yen for "
     r"delivery in a "
     r"year. Carry does not arbitrage it away because there is nothing to arbitrage: the forward is set by the rates. "
     r"The carry trade bets instead that the spot will not fall that far, and is paid for the crashes when it does"),
    (r"Covered parity is an arbitrage. Why did it fail for years after 2008?",
     r"the arbitrage needs balance sheet, and after 2008 balance sheet needs capital: a basis smaller than the cost of "
     r"capital is not worth taking. Demand to swap into dollars (insurers and banks with dollar assets) holds it open"),
    (r"Why does a rolled oil index earn less than the oil price in contango?",
     r"each roll sells the expiring contract and buys a dearer one: the curve's slope is a cost, month after month. In "
     r"backwardation the roll pays instead"),
    (r"Why did only the May 2020 WTI contract go negative?",
     r"it was the one about to deliver: holders without storage had to sell before the last trading day, to buyers who "
     r"had space; the June contract still had a month to find a home"),
    (r"A peg has held for years with tiny volatility. What does an option on its end cost?",
     r"less than it should: implied volatility calibrated to the calm prices a step as if it were a diffusion. The "
     r"payoff is a jump, and its probability is a political judgement, not a statistical one"),
    (r"What makes the Treasury basis trade risky if it is an arbitrage?",
     r"it is an arbitrage only at delivery; before then it is a levered position financed overnight, exposed to "
     r"margin calls, wider haircuts and a widening basis exactly when the market is stressed"),
]

PROBLEMS = [
    r"Derive covered interest parity from two riskless strategies, and show that with continuous compounding "
    r"$\ln(F/S) = (r_d - r_f)\tau$.",
    r"Sterling 3-month: $S$ = 1.30, $F$ = 1.3025, $r_\$$ = 2.0\%, $r_\pounds$ = 1.2\%. Compute the basis in basis points "
    r"(ignore day counts).",
    r"In the Fama regression, write $f - s = \mathbb{E}[\Delta s] + p$ and show that "
    r"$\beta = 1 - \text{cov}(p, f - s)/\text{var}(f - s)$. What does $\beta < 0$ require?",
    r"Show that the Garman--Kohlhagen forward delta of a call is $N(d_1)$ and its premium-adjusted forward delta "
    r"$(K/F) N(d_2)$.",
    r"Show that the delta-neutral straddle strike is $F e^{\sigma^2 T/2}$.",
    r"From ATM = 8\%, RR$_{25}$ = $-1\%$ and BF$_{25}$ = 0.3\%, find the two 25-delta vols.",
    r"In Krugman's model with $\bar s = 1$, $d_0 = 0.4$, $\mu = 0.1$, $\alpha = 1$: when does the attack come, and how "
    r"many reserves are taken on that day?",
    r"WTI: $F_1$ = 70, $F_2$ = 71.5 a month later, $r$ = 5\%. Find the convenience yield net of storage.",
    r"A bond: dirty price 100.2, futures 112.0, conversion factor 0.89, accrued at delivery 1.1, 92 days. Find the "
    r"implied repo rate.",
    r"Why does a long position in an at-the-money spread option lose value as the correlation of its two legs rises?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("snb"), load("cip"), load("fama"), load("carry"), load("oil"), load("basis"), load("inflation"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, s, c, f, k, o, b, i):
        st = k["stats"]
        items = [
            (rf"the franc's floor broke: {100 * s['move']:.1f}\% in a day, after three years without volatility", BAD),
            (rf"covered parity: within a few bp until 2007; {c['min_bp']:.0f} bp in 2008; {c['mean_post_bp']:.0f} bp "
             r"for years after, the price of balance sheet", BASIS),
            (rf"uncovered parity fails: pooled Fama slope {f['pooled']['beta']:.2f}, against 1", FOR),
            (rf"carry: Sharpe {st['sharpe']:.2f}, skew {st['skew']:.2f}; the yen in August 2024", CARRY),
            (r"FX options: Garman--Kohlhagen, four deltas, the ATM straddle; the smile from ATM, RR and BF", USD),
            (r"pegs fall before reserves run out; Black Wednesday, the franc", BAD),
            (rf"oil: contango {100 * o['contango_share']:.0f}\% of days; the roll cost {100 * (o['cagr_spot'] - o['cagr_index']):.1f} "
             r"points a year", OIL),
            (r"gas: seasons, Amaranth, Europe at eight times America; a plant is a strip of spread options", GAS),
            (r"$-\$37.63$: storage gone, and Bachelier's model in production", BAD),
            (rf"the Treasury basis: \${abs(b['lev_last']) / 1000:.1f} trillion of leveraged shorts; March 2020", BASIS),
            (rf"breakevens: a price, not a forecast ({100 * i['gap_mean']:+.1f} points against what followed)", INFL),
        ]
        rows = VGroup()
        for j, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        title = label(r"Part 22 in eleven lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.6:
            rows.scale_to_fit_height(6.6)
        with self.voiceover(
            "Part twenty-two in eleven lines. A currency floor that held for three years broke in a morning. Covered "
            "interest parity held to within a few basis points until 2007, collapsed in 2008, and stayed open for years "
            "after, priced by the cost of balance sheet. Uncovered parity fails, and the carry trade lives on the "
            "failure, with a good Sharpe ratio and a terrible left tail. Currency options need two interest rates, "
            "four deltas and three quotes. Pegs fall before their reserves run out. Oil spends most days in contango, "
            "and the roll costs an investor dearly. Gas has seasons and spikes, and a power plant is a strip of "
            "options. Oil went below zero when storage ran out, and Bachelier's model went into production. The "
            "Treasury basis trade is a trillion dollars of leverage on the safest asset in the world. And a breakeven "
            "is a price, not a forecast."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=24))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a, width=12.4, font_size=22) for q, a in qs]).arrange(DOWN, buff=0.25)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Dollar rates at five, yen at zero: the yen trades at a forward premium of about five "
            "percent a year, set by the rates, so there is nothing to arbitrage; carry bets that the spot will not "
            "fall that far. <bookmark mark='a'/> Covered parity failed after 2008 because the arbitrage needs balance "
            "sheet, and balance sheet needs capital. <bookmark mark='b'/> A rolled oil index earns less than the price "
            "in contango because each roll sells cheap and buys dear."
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
            "Only the May 2020 contract went negative because it was the one about to deliver, and its holders had "
            "nowhere to put the oil. <bookmark mark='a'/> An option on the end of a long-calm peg is cheap because its "
            "volatility was measured in the calm, and the payoff is a jump whose odds are a political judgement. "
            "<bookmark mark='b'/> And the Treasury basis trade is an arbitrage only at delivery; until then it is "
            "leverage financed overnight. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "And ten problems: covered parity derived and a basis computed by hand; the algebra of Fama's slope; FX "
            "deltas and the straddle strike; pillar vols from quotes; the date of a speculative attack; a convenience "
            "yield; an implied repo rate; and why a spread option dislikes correlation. Solutions, in English and "
            "Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"carry, value and momentum in every asset class, one book", [24, 32]),
            (r"funding, capital and transaction costs in every backtest", [26]),
            (r"systematic macro and trend following", [32]),
            (r"manipulation, surveillance and the close", [34]),
            (r"the finale: the macro desk in a stress with the rest of the House", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Carry returns in Part twenty-four, beside value and momentum, in every asset class, "
            "and again in Part thirty-two's systematic macro. Part twenty-six charges funding and capital in every "
            "backtest. Part thirty-four turns to manipulation and surveillance. And the finale stresses the macro desk "
            "with the rest of the House."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Clark, \textit{Foreign Exchange Option Pricing}; Wystup, \textit{FX Options and Structured Products}; "
             r"Geman, \textit{Commodities and Commodity Derivatives}; Eydeland and Wolyniec, \textit{Energy and Power "
             r"Risk Management}; Hull, \textit{Options, Futures, and Other Derivatives}, chs.\ 5 and 6"],
            [r"Kaldor (1939); Working (1949); Krugman (1979); Flood and Garber (1984); Fama (1984); Garman and Kohlhagen "
             r"(1983); Obstfeld (1994); Chinn and Meredith (2004); Gorton and Rouwenhorst (2006); Castagna and Mercurio "
             r"(2007); Brunnermeier, Nagel and Pedersen (2008); Lustig, Roussanov and Verdelhan (2011); Gorton, Hayashi "
             r"and Rouwenhorst (2013); Du, Tepper and Verdelhan (2018); D'Amico, Kim and Wei (2018)",
             r"SNB press release (15 January 2015); FXCM 10-K (2015); US Senate PSI, \textit{Excessive Speculation in "
             r"the Natural Gas Market} (2007); CFTC releases on Optiver (2008, 2012); CME Clearing advisories 20-152 and "
             r"20-171 (2020); FEDS Notes on the basis trade (2024, 2026); FCA, BoE and EIA data"])
        with self.voiceover(
            "The textbooks this part follows, and the papers and public records it draws on, from Kaldor's theory of "
            "storage to the Federal Reserve's estimates of the basis trade. Every number on screen was computed by the "
            "House's code from public data, with illustrative option markets labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("macro",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 23, Risk and Return", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That completes Act Three, on derivatives: options, rates, credit, counterparties, and now currencies and "
            "commodities, all priced. <bookmark mark='a'/> Next, Part twenty-three opens Act Four, on return premia: "
            "not what things must cost, but what they pay, and how much risk any of it is worth. The research desk "
            "opens."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
