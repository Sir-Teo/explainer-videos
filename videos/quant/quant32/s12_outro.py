from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import (BAD, BOND_C, CARRY_C, GOOD, PART, PUT_C, RP_C, SIXTY_C, TREND_C, VT_C, comma,
                                         load)

DESK = [
    (r"Why does trend following have positive skew?",
     r"the linear trend rule's profit is exactly $\frac12(S^2 - Q)$: a straddle on the period's move, financed by its "
     r"realised variance; under i.i.d. returns its skewness is $2^{3/2}(n - 2)/\sqrt{n(n-1)} \to 2\sqrt2$, with no "
     r"autocorrelation needed"),
    (r"Where does trend following's expected return come from?",
     r"only from autocorrelation: $\mathbb E\,P = \sum_k (n - k)\gamma_k$ plus a negligible drift term; a random walk "
     r"gives the skew but no profit"),
    (r"60/40 in dollars: how much of its risk is stocks?",
     r"with volatilities 16\% and 6\% and no correlation, about 94\%: a stock portfolio with a cushion"),
    (r"Why did risk parity lose more than 60/40 in 2022?",
     r"it was levered on bonds, and the stock--bond correlation turned positive with inflation: its diversification "
     r"and its leverage failed together"),
    (r"Does volatility targeting raise the Sharpe ratio?",
     r"sometimes: for 9 of 23 funds here; it reduced drawdowns for 14, mostly risky assets; Cederburg et al.: the "
     r"factor alphas are not investable in real time"),
    (r"An income fund sells index puts. What do you ask for?",
     r"its skewness and worst month, its beta (0.64 for Cboe's PUT here), and its 2008, February 2018 and March 2020"),
]

PROBLEMS = [
    r"60/40 with stock and bond volatilities of 16\% and 6\%, correlation 0: the stocks' share of risk.",
    r"The equal-risk weights for the same two assets, and the leverage to reach 10\% volatility.",
    r"Four styles each with Sharpe 0.6: the combination's Sharpe with average correlation 0, and with 0.3.",
    r"A risk-parity book levered 2.5$\times$, 70\% of its exposure in bonds: stocks $-20\%$, bonds $-10\%$. The loss.",
    r"A put seller earns 1\% a month for 50 months and loses 30\% in one: the mean and the sign of the skewness.",
    r"An overnight strategy earns 10\% a year and trades 504 times: the break-even cost per trade.",
    r"Show that for a random walk the linear trend rule's expected block profit is $\binom n2\mu^2$.",
    r"For $n = 63$, the theorem's skewness; and for a book of 23 independent such markets.",
    r"A true Sharpe ratio of 0.3: the years needed for a two-standard-error result.",
    r"An asset's expected return is proportional to its variance: does volatility targeting help its Sharpe ratio?",
    r"(qual) For i.i.d. $N(0, 1)$ returns, $Y = \sum_{s<t} z_s z_t$. Prove $\mathbb E Y^2 = \binom n2$ and "
    r"$\mathbb E Y^3 = n(n-1)(n-2)$, deduce the skewness, and show $Y/n \Rightarrow \frac12(Z^2 - 1)$, so "
    r"$\Pr(Y > 0) \to 31.7\%$.",
    r"(qual) For a general filter $P_w = \sum_{s<t} w_{t-s} r_s r_t$ on a stationary Gaussian series, derive "
    r"$\mathbb E P_w$ and, for i.i.d. returns, $\operatorname{Var} P_w$; show the filter maximising "
    r"$\mathbb E P_w/\sqrt{\operatorname{Var} P_w}$ under the i.i.d. variance has $w_k \propto \gamma_k$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("trend"), load("voltarget"), load("riskparity"), load("styles"), load("shortvol"),
                   load("calendar"), load("theory"), load("envelope"))
        self.desk()
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

    def recap(self, t, v, r, s, sv, c, th, e):
        b = e["books"]
        n63 = [x for x in th["data"] if x["n"] == 63][0]
        cc = c["tom"]["1991-2020"]
        items = [
            (rf"trend on 23 funds: Sharpe {t['main']['sharpe']:.2f}, correlation with stocks {t['corr_spy']:+.2f}; "
             rf"AQR's {t['aqr']['sharpe']:.2f}", TREND_C),
            (rf"2008: trend {100 * t['y2008']['trend']:+.0f}\%, stocks {100 * t['y2008']['spy']:+.0f}\%; a century of "
             r"evidence", TREND_C),
            (r"the smile: crisis alpha in slow crises, losses in reversals and fast crashes", TREND_C),
            (rf"volatility targeting: Sharpe up for {v['better']} of 23, drawdown down for {v['dd_better']}", VT_C),
            (rf"risk parity {r['rp']['sharpe']:.2f} against 60/40 {r['sixty']['sharpe']:.2f}; leverage "
             rf"{r['lev_min']:.1f}--{r['lev_max']:.1f}", RP_C),
            (rf"stock--bond correlation: {r['sb']['decades']['1970']:+.2f} in the 1970s, "
             rf"{r['sb']['decades']['2010']:+.2f} in the 2010s", BOND_C),
            (rf"value, momentum, carry, defensive: about 0.5--0.7 each, {s['styles']['Multi-style']['sharpe']:.2f} "
             r"together", CARRY_C),
        ]
        items2 = [
            (rf"selling puts: beta {sv['beta']:.2f}, skewness {sv['put']['skew']:.2f}; Volmageddon", PUT_C),
            (rf"the turn of the month, now {100 * cc['share_return']:.0f}\% of the return on {100 * cc['share_days']:.0f}\% "
             rf"of days; the night earns, the day does not", GOOD),
            (r"events: merger arbitrage is short a put; calendar rules need a reason", GOOD),
            (rf"2021--25: trend {b['trend']['hold']['sharpe']:.2f}, risk parity {b['rp']['hold']['sharpe']:.2f}", TREND_C),
            (rf"2022: trend {100 * b['trend']['y2022']:+.0f}\%, risk parity {100 * b['rp']['y2022']:+.0f}\%; the "
             rf"correlation flipped; counter {comma(e['trials'])}", BAD),
            (r"Rule 32: crisis years, skewness, leverage and who pays", QC.HOUSE),
            (rf"research: $P = \frac12(S^2 - Q)$; skewness $\to 2\sqrt2$, measured {n63['skew']:.1f}", TREND_C),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 32 in fourteen lines")
        with self.voiceover(
            "Part thirty-two in fourteen lines. Trend following on twenty-three funds earned a modest Sharpe ratio, "
            "uncorrelated with stocks, and made money in 2008; a century of evidence says the same at larger breadth. "
            "Its smile is crisis alpha in slow crises, and losses in reversals. Volatility targeting cuts drawdowns more "
            "reliably than it raises returns. Risk parity levers bonds to balance risk, which works while bonds hedge "
            "stocks, and the sign of that hedge has changed before. The four styles, across asset classes, are worth "
            "far more together than apart."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 32 in fourteen lines")
        with self.voiceover(
            "Selling insurance pays until it does not. Calendar effects are real when a flow explains them, and fade "
            "when they are traded. On the sealed years the trend book made money in 2022 while risk parity lost the "
            "most, as the stock-bond correlation turned positive. And the research chapter proved that the trend rule "
            "is long a straddle, with a skewness of two root two that needs no autocorrelation at all."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Why does trend following have positive skew? Because it is long a straddle, exactly. "
            "<bookmark mark='a'/> Where does its expected return come from? Only from autocorrelation. "
            "<bookmark mark='b'/> And how much of a sixty-forty portfolio's risk is stocks? About ninety-four percent."
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
            "Risk parity lost more than sixty-forty in 2022 because its leverage and its diversification failed "
            "together. <bookmark mark='a'/> Volatility targeting raises Sharpe ratios only sometimes. "
            "<bookmark mark='b'/> And an income fund that sells puts must show its skewness and its worst months. Full "
            "solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: sixty-forty's risk; the equal-risk weights and their leverage; combining styles; a "
            "levered loss in 2022; a put seller's mean and skew; the overnight break-even; the trend rule under a random "
            "walk; skewness and diversification; how long a Sharpe ratio takes to prove; and volatility targeting when "
            "returns rise with variance. Then two qualifying-exam problems: the theorem's moments and limit law, and "
            "the best linear trend filter. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"pairs, residuals and mean reversion: the opposite of trend", [33]),
            (r"the firm that runs these books: fees, capacity, culture", [34]),
            (r"liquidity spirals, deleveraging and 2022's gilts", [41]),
            (r"the finale: every row, deflated", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-three trades the opposite of trend: mean reversion in pairs and "
            "residuals. Part thirty-four goes inside the firm that runs such books. Part forty-one returns to "
            "deleveraging spirals, including the gilt crisis of 2022. And the finale deflates every row."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Pedersen, \textit{Efficiently Inefficient} (2015); Ilmanen, \textit{Expected Returns} (2011); "
             r"Kakushadze and Serur, \textit{151 Trading Strategies} (2018); Clenow, \textit{Following the Trend} (2013)"],
            [r"Ariel (1987); Lakonishok and Smidt (1988); Bernard and Thomas (1989); Ogden (1990); Fung and Hsieh (2001); "
             r"Mitchell and Pulvino (2001); Sullivan, Timmermann and White (2001); Potters and Bouchaud (2005); "
             r"Brunnermeier, Nagel and Pedersen (2008); Asness, Frazzini and Pedersen (2012); Ilmanen (2012); "
             r"Moskowitz, Ooi and Pedersen (2012); Israelov and Nielsen (2015); Daniel and Moskowitz (2016)",
             r"Campbell, Sunderam and Viceira (2017); Hurst, Ooi and Pedersen (2017); Moreira and Muir (2017); Harvey et "
             r"al.\ (2018); Koijen, Moskowitz, Pedersen and Vrugt (2018); Lou, Polk and Skouras (2019); Cederburg et "
             r"al.\ (2020). Data: Yahoo Finance fund prices; FRED; Kenneth French; Cboe; AQR's published data sets"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from the turn-of-the-month effect in 1987 to "
            "the critique of volatility management in 2020. Every number on screen was computed by the House's code from "
            "public fund prices, FRED, Kenneth French, Cboe and AQR's published series, with illustrations labelled as "
            "such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("macro", "portfolio"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 33, Statistical Arbitrage", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House's macro desk now runs a trend book and a risk-parity book, and knows which crisis each is for. "
            "Its premia are paid for risk, for behaviour, or by participants who must trade, and it has learned to ask "
            "which, because the answer decides whether a premium survives being known. <bookmark mark='a'/> Next, Part "
            "thirty-three: statistical arbitrage. Pairs, cointegration, residuals of a factor model, and the mathematics "
            "of trading mean reversion, the mirror image of the trend this part followed."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
