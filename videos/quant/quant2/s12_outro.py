from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import BTC, CCP, LOSS, PART, RATE, TRADE, load

DESK = [
    (r"Make me a market on the number of trading days in a US year.",
     r"about 250--252: 365, less 104 weekend days, less 9--10 exchange holidays; quote it tight, say 249 at 252, and "
     r"be ready to be hit on one side"),
    (r"A future trades at 102, spot at 100, six months to expiry, rates 3\%, no yield. Trade?",
     r"fair value $100e^{0.015} = 101.51$: sell the future, buy spot with borrowed money, deliver at expiry; 0.49 "
     r"locked in, less costs"),
    (r"Short interest is 120\% of the float. How, and what is your risk if you are short?",
     r"shares lent, sold and lent again; every short is a future buyer of a float that may run out: a squeeze"),
]

PROBLEMS = [
    r"A long opened at $P_0$ with leverage $L$ is liquidated at $P_0(1 - 1/L)/(1 - m)$. With $m = 0.5\%$ and daily "
    r"volatility 4\%, use the reflection principle to find the chance that 5x and 10x longs are liquidated within 30 "
    r"days.",
    r"A owes B 10, B owes C 10, C owes A 10, and A owes C 5. Compute the gross, bilateral and multilateral obligations "
    r"and check $M \le B \le G$.",
    r"A fund at a 2\% haircut's leverage limit sees the haircut rise to 4\%. Each unit sold lowers the price by "
    r"$\lambda$. Write the deleveraging loop and find its fixed point; when does it wipe out the equity?",
    r"Find the minimum-variance hedge ratio and its effectiveness when $\rho = 0.8$ and $\sigma_S/\sigma_F = 1.25$.",
    r"A fund's returns are smoothed with $\theta = (0.6, 0.3, 0.1)$ and its reported Sharpe ratio is 1.5. What is its "
    r"true Sharpe ratio, and its reported lag-1 autocorrelation?",
]


class Outro(VoiceoverScene):
    def construct(self):
        n = load("netting")
        f = load("sofr_fan")
        fe = load("fees")
        self.house()
        self.recap(n, f, fe)
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.next_part()

    def house(self):
        chart = house_chart(PART, lit=("treasury",)).scale(0.6).to_edge(UP, buff=0.2)
        items = VGroup(
            label(r"margin\_account, liquidation\_price, liquidation\_probability: the exchange's rules, and the odds",
                  font_size=20),
            label(r"ewma\_margin, fit\_ewma\_lambda, kupiec: how much margin, fitted and backtested", font_size=20),
            label(r"netting, ccp\_waterfall, call\_auction: what clearing and auctions do", font_size=20),
            label(r"min\_var\_hedge, implied\_carry: futures as a price and as a hedge", font_size=20),
            label(r"short\_pnl, deleverage, fire\_sale, max\_leverage: borrowing, haircuts and the race to sell",
                  font_size=20),
            label(r"fund\_fees, glm\_smooth, glm\_fit: fees with a high-water mark, and smoothed returns undone",
                  font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(chart, DOWN, buff=0.35)
        if items.width > 13.0:
            items.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 3: every backtest pays for its funding, its margin and its fees, and is closed out "
                             r"when the exchange would close it out. New: margin follows the EWMA model, not a "
                             r"constant.", 12.4, 22, QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House's second desk, treasury and funding, is built and tested. It keeps margin accounts, knows the odds of "
            "liquidation, and sizes and backtests margin. <bookmark mark='a'/> It nets, runs auctions and waterfalls, hedges "
            "with futures, charges for borrowing shares, plays out spirals and fire sales, and charges fees. "
            "<bookmark mark='b'/> And it adds Rule 3: every backtest pays its funding, margin and fees, and is closed out when "
            "the exchange would close it."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(LaggedStart(*[FadeIn(i) for i in items[:2]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in items[2:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def recap(self, n, f, fe):
        k17 = f["key"]["20190917"]
        items = [
            (r"a future is spot carried forward: $F = Se^{(r-q)T}$; hedge with $h^* = \rho\sigma_S/\sigma_F$", TRADE),
            (r"the book is queues; impatience pays half the spread plus the walk; auctions maximize volume", TRADE),
            (rf"netting only shrinks obligations, $M \le B \le G$: {100 * n['saved']:.0f}\% of a simulated day "
             r"removed", CCP),
            (r"a CCP's waterfall protects survivors; settlement deposits scale with volatility and days", CCP),
            (r"margin is marked daily, and liquidation odds follow the reflection principle (fat tails aside)", BTC),
            (r"margin models arrive after the loss: procyclical, from 1987 to 2020", LOSS),
            (r"shorts pay a fee and face squeezes once short interest outruns the free float", LOSS),
            (rf"haircuts are leverage limits that spiral; on 17 Sep 2019 SOFR's 99th percentile hit {k17['SOFR99']:.0f}\%",
             RATE),
            (rf"fees compound: 2 and 20 since 1927 leaves {100 * fe['share_kept']:.1f}\% of the profit; smooth returns "
             r"flatter Sharpe", LOSS),
            (r"index demand, price limits, and the rules of each market move prices and statistics", TRADE),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=c), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        title = label(r"Part 2 in ten lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        with self.voiceover(
            "Part two in ten lines. A future is the spot price carried forward, and its best hedge ratio is rho times a ratio "
            "of volatilities. The book is queues, impatience pays half the spread plus the walk, and an auction picks the "
            "price that trades the most. Netting can only shrink obligations, and a clearing house's waterfall protects the "
            "members who didn't fail; settlement deposits scale with volatility and with the days to settle. The odds of "
            "liquidation follow the reflection principle, fat tails aside, and margin models arrive after the loss. Shorts "
            "pay to borrow and face squeezes once short interest outruns the free float. Haircuts are leverage limits that "
            "spiral. Fees compound, and smoothed returns flatter. And index demand, price limits and each market's rules move "
            "prices and the statistics we measure."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=23) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. The first is a classic of trading interviews, the market-making game: make me a market on "
            "the number of trading days in an American year. About two hundred and fifty-two: three hundred and sixty-five "
            "days, less a hundred and four weekend days, less nine or ten holidays. Quote it tight, and be ready to be hit on "
            "either side. <bookmark mark='a'/> A future at a hundred and two, spot at a hundred, six months, three percent "
            "rates: fair value is a hundred and one fifty-one, so sell the future, buy the spot with borrowed money, and lock "
            "in forty-nine cents. <bookmark mark='b'/> Short interest at a hundred and twenty percent of float: shares lent, "
            "sold and lent again; and every one of those shorts must one day buy from a float that may run out."
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
            "And five problems: liquidation odds by the reflection principle, netting by hand, the deleveraging "
            "loop's fixed point, a hedge ratio, and undoing smoothed returns. Solutions, in English and Chinese, "
            "are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"margin, liquidation and funding", [17, 39, 41]),
            (r"the order book, auctions and wholesalers", [35, 36, 37]),
            (r"clearing, collateral and the default waterfall", [21, 41]),
            (r"repo, SOFR, specials and the basis trade", [18, 22, 41]),
            (r"fees, costs and smoothed returns in every backtest", [26, 30, 43]),
        ])
        with self.voiceover(
            "Where this comes back: margin and funding in Parts seventeen, thirty-nine and forty-one; the book and auctions in "
            "thirty-five to thirty-seven; clearing in twenty-one; repo and the basis in eighteen and twenty-two; and fees and "
            "smoothing in every backtest from twenty-six on."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hull, \textit{Options, Futures, and Other Derivatives}, ch.\ 1--3, 5, 10",
             r"Harris, \textit{Trading and Exchanges}, ch.\ 1--6",
             r"Tuckman and Serrat, \textit{Fixed Income Securities} (repo); Pedersen, \textit{Efficiently Inefficient}, "
             r"ch.\ 1, 5",
             r"Duffie, \textit{Dark Markets} (2012); Pirrong, \textit{The Economics of Central Clearing} (2011)"],
            [r"Shleifer (1986); Chang, Hong and Liskovich (2015); Greenwood and Sammon (2025); Pavlova and Sikorskaya (2023)",
             r"D'Avolio (2002); Duffie (1996, 2010); Copeland, Martin and Walker (2014); Brunnermeier and Pedersen (2009)",
             r"Duffie and Zhu (2011); Smith, Farmer, Gillemot and Krishnamurthy (2003); Afonso et al.\ (2021)",
             r"Battalio, Corwin and Jennings (2016); Ernst and Spatt (2022); Bryzgalova, Pavlova and Sikorskaya (2023); "
             r"Schwarz et al.\ (2025)",
             r"Fung and Hsieh (1997); Getmansky, Lo and Makarov (2004); Bogousslavsky and Muravyev (2023); Pinter (2023)",
             r"SEC staff report on early 2021 (October 2021); SEC Rule 612 (2024); SEBI F\&O studies (2023--25)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers and reports it draws on. Every number in it was "
            "computed from public data by the series' own code: Binance's Bitcoin futures and funding rates, the "
            "St. Louis Fed's money-market rates, and Kenneth French's market returns."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def next_part(self):
        chart = house_chart(PART, lit=("treasury",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 3, Value, Accounting and the Firm", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has two desks: data, and funding. <bookmark mark='a'/> Next, Part three: value, "
            "accounting and the firm. What a share is a claim on, how companies report it, and the accounting "
            "signals that became the first factors."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
