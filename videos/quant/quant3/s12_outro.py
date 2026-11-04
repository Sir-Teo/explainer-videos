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
    (r"A firm's ROE is 12\%, its cost of equity 8\%, and its book grows 4\% a year forever. What is its P/B?",
     r"$1 + (0.12 - 0.08)/(0.08 - 0.04) = 2$"),
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
    r"A project costs 100, pays 230 in a year and costs 132 in two. Find both IRRs, and the NPV at 15\%.",
    r"With $\rho = 0.96$ and a dividend yield whose AR(1) persistence is $\phi = 0.95$, a one-year return slope "
    r"$b_r = 0.05$ and dividend-growth slope $b_d = -0.03$: check the Campbell--Shiller identity and give the long-run "
    r"shares.",
    r"(qual) From the dividend discount model and clean surplus, prove $P_t = b_t + \sum_{\tau \ge 1}R^{-\tau}\mathbb E_t "
    r"x^a_{t+\tau}$; state the transversality condition it needs.",
    r"(qual) Under Ohlson's dynamics with $\nu = 0$, show $P_t = (1 - k)b_t + k(\varphi x_t - d_t)$ with $k = r\omega/(R - "
    r"\omega)$, $\varphi = R/r$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.s = load("shiller")
        self.c = load("cape")
        self.o = load("osap")
        self.recap()
        self.desk()
        self.problems()
        self.house()
        self.payoffs()
        self.references()

    def recap(self):
        s, c, o = self.s, self.c, self.o
        items = [
            (rf"prices moved {s['ratio_changes']:.0f}$\times$ as much as the present value of the dividends paid", PRICE),
            (r"Gordon: $V = D_1/(r - g)$; a stock's duration is $(1 + r)/(r - g)$, but $g$ moves with $r$", VALUE),
            (r"the three statements are one double-entry machine; earnings $=$ cash flow $+$ accruals", CASH),
            (r"every reported number has two dates; the House answers as of the day it was filed", QC.HOUSE),
            (r"DCF: growth adds value only when RONIC $>$ WACC; the terminal value is most of the answer", VALUE),
            (r"residual income: $P/B = 1 + (\text{ROE} - r)/(r - g)$; a price implies a cost of capital", VALUE),
            (r"a high dividend yield must be paid by returns or by dividend growth; since 1945, by returns", PRICE),
            (r"financing and payout move value only through taxes, distress and information; equity is a call", EQUITY),
            (rf"{o['all']['n']} published predictors kept {100 * o['all']['post_ratio']:.0f}\% of their returns after "
             rf"publication; the drift after earnings has faded", LOSS),
            (r"merger arbitrage is a short put; forensic screens fight base rates; machines must be point-in-time", LOSS),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=23)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title = label(r"Part 3 in ten lines", font_size=38).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            f"Part three in ten lines. Prices moved about {s['ratio_changes']:.0f} times as much as the value of the dividends "
            "paid. Gordon makes a stock a long bond, but in the data growth moves with the rate. The three statements are one "
            "double-entry machine, and earnings are cash plus accruals. Every reported number has two dates. Growth adds value "
            "only above the cost of capital, and a price implies a cost of capital. Residual income turns value into book plus "
            "excess returns. A high dividend yield must be paid for, and since 1945 returns have paid it. Financing and payout "
            "matter through taxes, distress and information, and equity is a call on the firm. Published predictors kept about "
            f"{100 * o['all']['post_ratio']:.0f} percent of their returns, and the earnings drift has faded. And merger arbitrage "
            "is a short put, screens fight base rates, and machines that read filings must be point-in-time too."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=23) for q, a in DESK]).arrange(DOWN, buff=0.22)
        if cards.height > 7.5:
            cards.scale_to_fit_height(7.5)
        with self.voiceover(
            "Four desk questions. A firm with no debt buys back a tenth of its shares at the market price. The price does not move, "
            "but earnings per share rise whenever the earnings yield beats what the cash was earning, so the P/E falls. "
            "<bookmark mark='a'/> A stock pays two dollars next year, growing four percent forever, and trades at fifty. The market "
            "expects the dividend yield plus growth: eight percent. <bookmark mark='b'/> A takeover target trades at forty-seven "
            "under a cash offer of fifty and would fall to thirty-five if the deal broke; it closes in six months with cash earning "
            "four percent. The priced chance of closing is about eighty-six percent. <bookmark mark='c'/> A firm earns twelve "
            "percent on book, its cost of equity is eight, and book grows at four: a price-to-book of two. Full solutions are in "
            "the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And nine problems: the P/E from Gordon's model, a discounted cash flow, Modigliani and Miller with taxes, Merton's "
            "model of equity and debt, overlapping windows, a project with two internal rates of return, the Campbell–Shiller "
            "identity, and two at the level of a qualifying exam: residual income from clean surplus, and Ohlson's value as "
            "a blend of book and capitalised earnings. Solutions, in English and Chinese, are in the notes."       ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(4)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",)).scale(0.68).to_edge(UP, buff=0.2)
        items = VGroup(
            label(r"\texttt{fundamentals}: the bitemporal store on real EDGAR filings; filing lags; the toy firm's "
                  r"double-entry machine; SUE and event studies", font_size=20),
            label(r"\texttt{valuation}: IRR by bisection, duration, the value driver, residual income, the implied "
                  r"rate, APV and Miller, Campbell--Shiller, Beneish", font_size=20),
            label(r"the envelope: Shiller's, French's and the open-source predictors' months from 2021 sealed; the "
                  r"CAPE forecast and this part's trials registered", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(chart, DOWN, buff=0.3)
        if items.width > 13.2:
            items.scale_to_fit_width(13.2)
        rule = wrapped_label(r"Rule 4: a reported number exists from the day it was filed, as first reported; a "
                             r"restatement is a new fact, never an edit of the past.", 12.0, 23,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The data desk now reads real filings as of any day, with the accounting simulator and event studies beside it, and a "
            "tested valuation library. <bookmark mark='a'/> The part's hold-outs are sealed and its trials registered. "
            "<bookmark mark='b'/> Rule four: a number exists from the day it was filed, as first reported."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05), FadeIn(items[:2]))
            vo.wait_until("a")
            self.play(FadeIn(items[2]))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"equity as a call on the firm", [10, 20]),
            (r"discount rates that move, and Shiller's puzzle", [23]),
            (r"Stambaugh's bias and overlapping windows", [6]),
            (r"accounting signals, the factor zoo and decay", [24, 25]),
            (r"the trial counter and the sealed envelope", [26, 43]),
            (r"forecasting earnings; text in filings", [27, 28]),
        ])
        with self.voiceover(
            "Where this comes back. Equity as a call is priced in Part ten and becomes a model of default in Part twenty. "
            "Shiller's puzzle, that discount rates must move, is the subject of Part twenty-three, and Stambaugh's bias is worked "
            "out in Part six. The accounting signals return as factors in twenty-four and in the factor zoo of twenty-five. The "
            "trial counter is put to work in twenty-six, and the CAPE forecast is opened in the finale. Machine learning for returns "
            "and language models that read filings are Parts twenty-seven and twenty-eight."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Berk and DeMarzo, \textit{Corporate Finance}, ch.\ 2--4, 7--9, 14--19, 22, 28",
             r"Brealey, Myers and Allen, \textit{Principles of Corporate Finance}, ch.\ 2--6, 16--19, 22, 28, 31",
             r"Damodaran, \textit{Investment Valuation}; Koller, Goedhart and Wessels, \textit{Valuation}; "
             r"Bodie, Kane and Marcus, ch.\ 18--19",
             r"Campbell, Lo and MacKinlay, ch.\ 7; Luenberger, ch.\ 2--3; Penman, \textit{Financial Statement Analysis}"],
            [r"Williams (1938); Gordon and Shapiro (1956); Modigliani and Miller (1958, 1961, 1963); Miller (1977); "
             r"Jensen and Meckling (1976); Myers (1977); Merton (1974); Shiller (1981); Campbell and Shiller (1988); "
             r"Cochrane (2008)",
             r"Ball and Brown (1968); Foster, Olsen and Shevlin (1984); Bernard and Thomas (1989); Ohlson (1995); "
             r"Sloan (1996); Beneish (1999); Piotroski (2000); Dechow, Ge, Larson and Sloan (2011); Novy-Marx (2013)",
             r"Graham and Harvey (2001); Mitchell and Pulvino (2001); Dechow, Sloan and Soliman (2004); Boudoukh et al.\ "
             r"(2007); Pontiff and Woodgate (2008); Brav et al.\ (2008); McLean and Pontiff (2016); Asness, Frazzini "
             r"and Pedersen (2019); Chen and Zimmermann (2022); Martineau (2022)",
             r"van Binsbergen, Han and Lopez-Lira (2023); Zhang, Zhu and Linnainmaa (2025); Cao, Jiang, Wang and Yang "
             r"(2024); Islam et al.\ (2023); Jensen, Kelly and Pedersen (2023); Gormsen and Lazarus (2023); Eisfeldt, "
             r"Kim and Papanikolaou (2022); SEC releases on Enron, Luckin and Kraft Heinz"], font_size=19)
        with self.voiceover(
            "The textbook chapters this part covers, and the papers and reports it draws on. Every number in it was computed by the "
            "series' own code from public data: Shiller's century and a half of prices, Kenneth French's portfolios, the "
            "open-source predictor returns, Damodaran's implied premiums, Yahoo's prices, and filings from the SEC's EDGAR. "
            "<bookmark mark='a'/> Next, Part four opens the mathematical toolkit: martingales and measure, the precise meaning of a "
            "fair game, and why you cannot beat one by changing your bets."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            smap = series_map(current=PART + 1, done=PART)
            self.play(FadeOut(card), FadeIn(smap))
        self.wait(1.0)
        self.clear_scene()
