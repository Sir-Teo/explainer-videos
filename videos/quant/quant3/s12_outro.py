from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, EQUITY, LOSS, PART, PRICE, VALUE, load

DESK = [
    (r"A firm with no debt buys back 10\% of its shares at market. What happens to the price, and to EPS?",
     r"the price doesn't move (Modigliani--Miller, before taxes and signalling); EPS rises whenever the earnings yield "
     r"beats the yield on the cash spent, so the P/E falls"),
    (r"A stock pays \$2 next year, the dividend grows 4\% a year forever, and it trades at \$50. What return does "
     r"the market expect?", r"$r = D_1/P + g = 4\% + 4\% = 8\%$"),
    (r"A target trades at 47 under a cash offer of 50; if the deal breaks it falls to 35. It closes in six months "
     r"and cash earns 4\% a year. What chance of closing is priced in?",
     r"$p \cdot 50 + (1 - p) \cdot 35 = 47 \times 1.02$, so $p \approx 86\%$: time value raises it from 80\%"),
]

PROBLEMS = [
    r"Derive $P/E_1 = b/(r - g)$ from Gordon's model. With a payout ratio of 50\% and $r = 8\%$, what perpetual growth "
    r"does a P/E of 30 imply?",
    r"Free cash flow is 100 and grows 5\% for five years, then 2\% forever. Value it at 8\%, give the terminal value's "
    r"share, and value it again at 7\% and 3\%.",
    r"A firm's assets earn $r_A = 8\%$ and its debt costs $r_D = 4\%$. Find $r_E$ at $D/E = 1$ without taxes, and the WACC "
    r"at that leverage with a 21\% tax rate. Why does the WACC fall only when there are taxes?",
    r"Merton: assets 100, debt of face 80 due in five years, asset volatility 25\%, $r = 2\%$. Value the equity and the "
    r"debt, and find the debt's credit spread.",
    r"There are 1,560 overlapping ten-year windows in 1881--2010. Roughly how many independent observations is that, and "
    r"by about what factor does treating them as independent overstate a $t$-statistic?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.s = load("shiller")
        self.c = load("cape")
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self):
        s, c = self.s, self.c
        items = [
            (rf"a share is a claim on dividends, but prices moved {s['ratio_changes']:.0f}$\times$ as much as their "
             rf"present value", PRICE),
            (r"Gordon: $V = D_1/(r - g)$; when $r - g$ is small, value is hostage to the discount rate", VALUE),
            (r"the three statements are one set of books: earnings $=$ cash flow $+$ accruals", CASH),
            (r"in a DCF the terminal value is most of the answer; one point on $r$ and $g$ moves it 45\%", VALUE),
            (rf"CAPE {c['cape_now']:.1f} at the end of 2020 predicts {100 * c['pred_now']:.1f}\% a year: sealed; "
             rf"only about {c['n_indep']} independent decades stand behind it", QC.HOUSE),
            (r"financing and payout don't change value without taxes and distress; EPS can be bought", EQUITY),
            (r"accounting signals earned 5.6\% a year before publication and 1.5\% after", LOSS),
            (r"merger arbitrage is a short put; Enron and Wirecard faked the cash: keep numbers as first reported", LOSS),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=25)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 3 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part three in eight lines. A share is a claim on future dividends, yet prices have moved about eight "
            "times as much as the value of the dividends that were paid. Gordon's formula values a growing stream, "
            "and when growth is close to the discount rate, value is hostage to that rate. The three statements are "
            "one set of books, and earnings are cash plus accruals. In a discounted cash flow, the terminal value is "
            "most of the answer. The CAPE at the end of 2020 forecast half a percent a year for the decade, with only "
            "thirteen independent decades behind it; that forecast is sealed. Financing and payout don't change value "
            "without taxes and distress, though earnings per share can be bought. Accounting signals lost most of "
            "their returns after publication. And merger arbitrage is a short put, while Enron and Wirecard showed "
            "that even the cash can be false."
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
            "Three desk questions. A firm with no debt buys back a tenth of its shares at the market price. The price "
            "does not move, but earnings per share rise whenever the earnings yield beats what the cash was earning, "
            "so the P/E falls. <bookmark mark='a'/> A stock pays two dollars next year, growing four percent forever, "
            "and trades at fifty. The market expects the dividend yield plus growth: eight percent. "
            "<bookmark mark='b'/> A takeover target trades at forty-seven under a cash offer of fifty and would fall "
            "to thirty-five if the deal broke; it closes in six months with cash earning four percent. Grow today's "
            "price at the interest rate before comparing: the priced chance of closing is about eighty-six percent. "
            "Full solutions are in the notes."
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
            "And five problems: the P/E from Gordon's model, a discounted cash flow, Modigliani and Miller with "
            "taxes, Merton's model of equity and debt, and how many independent observations overlapping windows "
            "really contain. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"equity as a call on the firm", [10, 20]),
            (r"discount rates that move, and Shiller's puzzle", [23]),
            (r"accounting signals, the factor zoo and decay", [24, 25]),
            (r"the trial counter and the sealed envelope", [26, 43]),
            (r"point-in-time fundamentals and text in filings", [24, 28]),
        ])
        with self.voiceover(
            "Where this comes back. Equity as a call is priced in Part ten and becomes a model of default in Part "
            "twenty. Shiller's puzzle, that discount rates must move, is the subject of Part twenty-three. The "
            "accounting signals return as factors in twenty-four, and in the factor zoo of twenty-five. The trial "
            "counter is put to work in twenty-six, and the CAPE forecast is opened in the finale. And the "
            "point-in-time store feeds the factor library and, in Part twenty-eight, the language models that read "
            "the filings themselves."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Berk and DeMarzo, \textit{Corporate Finance}, ch.\ 3--4, 9, 14--17",
             r"Brealey, Myers and Allen, \textit{Principles of Corporate Finance}, ch.\ 2--4, 17--19",
             r"Damodaran, \textit{Investment Valuation}; Koller, Goedhart and Wessels, \textit{Valuation} (McKinsey)",
             r"Shiller, \textit{Irrational Exuberance}; Penman, \textit{Financial Statement Analysis and Security Valuation}"],
            [r"Shiller (1981); Campbell and Shiller (1988); Williams (1938); Gordon and Shapiro (1956); Modigliani and Miller (1958, 1961, 1963)",
             r"Merton (1974); Ball and Brown (1968); Bernard and Thomas (1989); Sloan (1996); Piotroski (2000)",
             r"Novy-Marx (2013); Fama and French (1992, 2015); McLean and Pontiff (2016); Mitchell and Pulvino (2001)",
             r"SEC v.\ Enron-related actions; US Senate PSI report on Enron prepays (2002); BaFin and EY on Wirecard (2020)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers and reports it draws on. Every number in it was "
            "computed by the series' own code from public data: Robert Shiller's century and a half of prices, "
            "dividends and earnings, and Kenneth French's portfolios sorted on accounting signals."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 4, Martingales and Measure", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House has its data desk, with fundamentals, and its funding desk. <bookmark mark='a'/> That ends "
            "the first act. Next, Part four opens the mathematical toolkit: martingales and measure, the precise "
            "meaning of a fair game, and why you cannot beat one by changing your bets."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
