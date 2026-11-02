from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, BTC, CCP, LOSS, PART, RATE, TRADE

DESK = [
    (r"Make me a market on the number of trading days in a US year.",
     r"about 250--252: 365, less 104 weekend days, less 9--10 exchange holidays; quote it tight, say 249 at 252, and "
     r"be ready to be hit on one side"),
    (r"You are long 10x on a perpetual swap and the price falls 4\% a day for three days, then rises 20\%. "
     r"What is your profit?", r"nothing: three 4\% falls make 11.5\%, past the 9.5\% that liquidates you at $m = 0.5\%$; being "
                              r"right later doesn't count"),
    (r"A fund charges 2 and 20 with a high-water mark. It loses 20\% one year and gains 25\% the next, before fees. "
     r"What is the performance fee in year two?", r"none, or nearly none: the gain only gets back to the old peak, "
                                                  r"and the management fee is charged on the way"),
]

PROBLEMS = [
    r"Show that a long position opened at $P_0$ with leverage $L$ is liquidated at $P_0(1 - 1/L)/(1 - m)$, and a short "
    r"at $P_0(1 + 1/L)/(1 + m)$. Which leverage survives a 33\% fall at $m = 0.5\%$?",
    r"Three members trade: A owes B 10, B owes C 10, C owes A 10, and A owes C 5. Compute the gross, bilateral and "
    r"multilateral obligations.",
    r"Show that with a haircut $h$ the most leverage is $1/h$. A fund holds Treasuries with a 2\% haircut and the haircut "
    r"rises to 4\%. How much must it sell, as a share of its assets, if its equity is unchanged?",
    r"A perpetual's funding averaged 0.016\% per 8 hours in 2020. What did it cost, per year, to hold \$1 long? What "
    r"trade earns it, and what is its risk?",
    r"A fund earns 10\% a year before fees for 30 years. Compare final wealth after a 1\% fee and after 2 and 20 (no "
    r"losses, so the high-water mark never binds).",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self):
        items = [
            (r"a trade is a promise; clearing turns it into a guarantee, for collateral", CCP),
            (r"the order book pays the patient and charges the impatient; auctions set the close", TRADE),
            (r"netting through a CCP removed 91\% of a simulated day's obligations", CCP),
            (r"margin is marked daily: in March 2020 even 2x leverage on Bitcoin was liquidated", BTC),
            (r"shorting has unlimited loss and a squeeze; leverage is funded overnight, by repo", LOSS),
            (r"haircuts are leverage limits, and they move in a panic; on 17 Sep 2019 SOFR hit 5.25\%", RATE),
            (r"fees compound: 2 and 20 on the US market since 1927 keeps under 5\% of the profit", LOSS),
            (r"every market has its own rules: T+1, price limits, who fills your order", TRADE),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=c), label(t, font_size=25)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 2 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part two in eight lines. A trade is a promise, and a clearing house turns it into a guarantee, in "
            "exchange for collateral. The order book pays the patient and charges the impatient, and an auction "
            "sets the closing price. Netting through a clearing house removes most of what must change hands. "
            "Margin is marked to market, and in March 2020 even two-times leverage on Bitcoin was liquidated. Short "
            "sellers face unlimited losses and squeezes, and leverage everywhere is funded overnight, by repo. "
            "Haircuts are leverage limits that move in a panic; in September 2019 the safest overnight loan cost "
            "five and a quarter percent. Fees compound: two and twenty on the American market since 1927 leaves "
            "the investor under five percent of the profit. And every market has rules of its own."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. The first is a classic of trading interviews, the market-making game: make me a "
            "market on the number of trading days in an American year. About two hundred and fifty-two: three hundred "
            "and sixty-five days, less a hundred and four weekend days, less nine or ten holidays. Quote it tight, "
            "and be ready to be hit on either side. <bookmark mark='a'/> You are long ten times on a perpetual swap; "
            "it falls four percent a day for three days and then rises twenty. Your profit is nothing: you were "
            "liquidated on the third day. <bookmark mark='b'/> A fund charging two and twenty loses a fifth one year "
            "and gains a quarter the next: almost no performance fee, because it is only back to its old peak. The "
            "full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: liquidation prices, netting, haircuts and deleveraging, the cost of funding, and the "
            "compounding of fees. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"margin, liquidation and funding", [17, 39, 41]),
            (r"the order book and the auction", [35, 36, 37]),
            (r"clearing, collateral and the default waterfall", [21, 41]),
            (r"repo, SOFR and haircuts", [18, 22, 41]),
            (r"fees and costs in every backtest", [26, 30, 43]),
        ])
        with self.voiceover(
            "Where this comes back. Margin and funding return in the deep hedger of Part seventeen, in crypto's "
            "funding trades in thirty-nine, and in the spirals of forty-one. The order book and the auction are the "
            "subject of Parts thirty-five to thirty-seven. Clearing and collateral return with counterparty risk in "
            "twenty-one. Repo and SOFR are the base of the rates desk in eighteen and the basis trade in twenty-two. "
            "And fees and costs are charged in every backtest, from twenty-six to the finale."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hull, \textit{Options, Futures, and Other Derivatives}, ch.\ 1--7",
             r"Harris, \textit{Trading and Exchanges}, parts I--II",
             r"Tuckman and Serrat, \textit{Fixed Income Securities} (repo); Pedersen, \textit{Efficiently Inefficient}, ch.\ 1--5",
             r"Duffie, \textit{Dark Markets} (2012); Pirrong, \textit{The Economics of Central Clearing} (2011)"],
            [r"Afonso, Cipriani, Copeland, Kovner, La Spada and Martin (2021), the September 2019 repo spike, FRBNY",
             r"BIS Quarterly Review (December 2019), ``September stress in dollar repo markets''",
             r"SEC staff, \textit{Equity and Options Market Structure Conditions in Early 2021} (October 2021)",
             r"Credit Suisse, report on Archegos (July 2021); SEBI, study of F\&O traders (September 2024)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the reports it draws on. Every number in it was computed "
            "from public data by the series' own code: Binance's Bitcoin futures and funding rates, the St. Louis "
            "Fed's money-market rates, and Kenneth French's market returns."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
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
