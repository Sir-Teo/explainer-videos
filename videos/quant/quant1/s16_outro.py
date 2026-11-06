from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import BTC, PART, PP, QQ, REAL, TAIL, VOL, load

DESK = [
    (r"I toss a fair coin until it lands heads. If that takes $n$ tosses, I pay you $2^n$ dollars. What would you pay "
     r"to play?", r"the expected payout is infinite, $\sum_n 2^{-n} 2^n$; with log utility (Bernoulli, 1738) the game "
                  r"is worth \$4"),
    (r"A stock goes up 50\% or down 50\% each year, with equal chances, forever. Is it a good investment? What "
     r"happens to a typical path?", r"the average is flat, but the median path goes to zero: "
                                    r"$\tfrac12\ln 1.5 + \tfrac12\ln 0.5 = \tfrac12\ln 0.75 < 0$"),
    (r"How many tosses of a fair coin, on average, until two heads in a row?",
     r"six: condition on the first tosses and solve $E = \tfrac12(E + 1) + \tfrac14(E + 2) + \tfrac14\cdot 2$"),
]

PROBLEMS = [
    r"Show that if $P_t = \mathbb E_t[X]$ for a fixed payoff $X$, then $P$ is a martingale, and that its increments "
    r"are uncorrelated, though they need not be independent. Give an example of the second.",
    r"If one-period log returns are $N(m, s^2)$, show the arithmetic mean simple return is $e^{m + s^2/2} - 1$ and the "
    r"geometric mean is $e^m - 1$. Check with chapter 2's numbers (11.95\%, 10.02\%, $\sigma$ = 19.9\%).",
    r"Show $\operatorname{VR}(2) = 1 + \rho_1$ and $\operatorname{VR}(q) = 1 + 2\sum_{k<q}(1 - k/q)\rho_k$ for a "
    r"stationary series.",
    r"For a Pareto tail $P(X > x) = (x / x_m)^{-\alpha}$, show $\mathbb E[\ln(X / x_m)] = 1/\alpha$, which is Hill's "
    r"estimator. If daily returns have $\alpha = 3$, which moments exist?",
    r"A fund holds $L$ times the market, rebalanced daily, borrowing at $r$. Show its growth rate is about "
    r"$r + L(\mu - r) - \tfrac12 L^2\sigma^2$, find the best $L$, and evaluate it with chapter 2's numbers.",
    r"(qual) For iid increments with a finite fourth moment, prove $\sqrt n(\operatorname{VR}(q) - 1) \Rightarrow "
    r"N\big(0, 2(2q-1)(q-1)/(3q)\big)$.",
    r"(qual) GARCH(1,1), normal shocks: show $\delta_k = 1 + (\kappa - 1)\rho_1(\alpha + \beta)^{k-1}$; for "
    r"$(0.05, 0.12, 0.86)$ evaluate $\delta_1$ and show $\hat\delta_k$ has infinite variance.",
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
            (r"prices spread like $\sqrt t$: Regnault's law, measured at slope 0.52 over 94 years", REAL),
            (r"growth is the average minus $\tfrac12\sigma^2$: volatility drag, and a peak in leverage", REAL),
            (r"well-anticipated prices are martingales (Samuelson): the tower property", QC.IDEA),
            (r"small stocks' weekly echo: real in the data, gone once trading was fast", QC.IDEA),
            (r"heavy tails with a cubic law; 101 days beyond $5\sigma$ where a bell curve expects none", TAIL),
            (r"volatility clusters, and falls bring storms: independent returns fail", VOL),
            (r"finite variance fits the evidence; kurtosis is at the mercy of one day", TAIL),
            (r"markets are just inefficient enough to pay for information; in-sample results can fool you", QC.IDEA),
            (r"$\mathbb Q$ prices insurance, $\mathbb P$ is what happens; options bound expected returns", QQ),
            (r"no betting system beats a fair game; information can (Thorp)", QC.HOUSE),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=c), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title = label(r"Part 1 in ten lines", font_size=38).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.4)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part one in ten lines. Prices spread with the square root of time, as Regnault said in 1863. Growth "
            "is the average return minus half the variance, so leverage has a peak. Well-anticipated prices are "
            "martingales, by the tower property. Small stocks once had a weekly echo, and it vanished when trading "
            "became fast. Returns have heavy tails, with an exponent near three. Volatility clusters, and falls "
            "bring storms: returns are not independent. Finite variance fits the evidence; the kurtosis "
            "is at the mercy of a single day. Markets are just inefficient enough to pay for information, and "
            "in-sample predictability can fool you. The risk-neutral world prices insurance; the real world is what "
            "happens. And no betting system can beat a fair game, though information can."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6,
                                                 run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=26) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions, of the kind trading firms ask. The Saint Petersburg game: I toss a coin until it "
            "lands heads and pay you two to the number of tosses. Its expected payout is infinite, yet nobody pays "
            "much to play; Daniel Bernoulli's answer in 1738, logarithmic utility, values it at four dollars. "
            "<bookmark mark='a'/> A stock that rises or falls fifty percent each year, with equal chances, forever: "
            "its average stays put, and its typical path goes to zero. That is chapter two's drag. "
            "<bookmark mark='b'/> And how many tosses, on average, until two heads in a row? Six. The full solutions "
            "are in the part's notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "And seven problems: martingales and the tower property, the lognormal means, the variance ratio, Hill's "
            "estimator, the leverage that maximizes growth, and two at the level of a qualifying exam: the variance "
            "ratio's limiting law, and the fourth moments of GARCH. Solutions, in English and Chinese, are in the "
            "notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"martingales and the tower property", [4, 9, 23]),
            (r"heavy tails and volatility clustering", [7, 13, 40]),
            (r"volatility drag and the leverage peak", [8, 30, 32]),
            (r"in-sample against out-of-sample; the envelope", [6, 26, 43]),
            (r"$\mathbb P$ and $\mathbb Q$", [9, 12, 23]),
            (r"Thorp", [8, 10, 33]),
        ])
        with self.voiceover(
            "Where this comes back. Martingales are the language of Part four, and of the no-arbitrage theorem in "
            "nine; Part twenty-three joins P and Q. Heavy tails and clustering are modelled in Part seven, priced in "
            "thirteen, and managed as risk in forty. The drag and the leverage peak return with Kelly in eight, "
            "and in the portfolios of thirty and thirty-two. The in-sample trap gets its full treatment in six and "
            "twenty-six, and the envelope opens in the finale. And Thorp appears in eight, ten and thirty-three."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Campbell, Lo and MacKinlay, \textit{The Econometrics of Financial Markets}, ch.\ 1--2",
             r"Bodie, Kane and Marcus, \textit{Investments} (returns, efficient markets); Cont and Tankov, ch.\ 1",
             r"Bachelier, \textit{Th\'eorie de la sp\'eculation} (1900; tr.\ Davis and Etheridge, 2006)",
             r"Thorp, \textit{Beat the Dealer} (1962), \textit{A Man for All Markets} (2017); Zuckerman (2019)"],
            [r"Regnault (1863); Bachelier (1900); Cowles (1933), \textit{Econometrica}; Kendall (1953), \textit{JRSS A}; "
             r"Osborne (1959), \textit{Oper.\ Res.}",
             r"Samuelson (1965), \textit{IMR}; Mandelbrot (1963), \textit{J.\ Business}; Fama (1970), \textit{JF}; "
             r"Hill (1975), \textit{Ann.\ Stat.}; Black (1976), \textit{ASA Proc.}",
             r"Breeden and Litzenberger (1978), \textit{J.\ Business}; Grossman and Stiglitz (1980), \textit{AER}; "
             r"Milgrom and Stokey (1982), \textit{JET}; Black (1986), \textit{JF}",
             r"Lo and MacKinlay (1988), \textit{RFS}; (1990), \textit{J.\ Econometrics}; Sharpe (1991), \textit{FAJ}; "
             r"Gopikrishnan et al.\ (1998), \textit{EPJ B}; Cont (2001), \textit{Quant.\ Finance}",
             r"Martin (2017), \textit{QJE}; Martin and Nagel (2022), \textit{JFE}"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number in it was computed "
            "from public data by the series' own code: Kenneth French's market and size portfolios, Binance's "
            "Bitcoin prices, and Deribit's option trades."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 2, The Machinery of Markets", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House has a data desk, a rule, a sealed envelope and a counter at zero. <bookmark mark='a'/> "
            "Next, Part two: the machinery of markets. The instruments, the exchanges, clearing and settlement, and "
            "what actually happens between pressing buy and owning something."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
