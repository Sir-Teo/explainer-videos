from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, load

DESK = [
    (r"Long a delta-hedged straddle, the stock does not move. How do you lose money?",
     r"theta: you pay $\frac12\Gamma S^2\sigma_{imp}^2\,dt$ every day and earn $\frac12\Gamma\,dS^2$ only when it moves; and "
     r"vega, if implied volatility falls"),
    (r"Make a market on a die roll. Now the roll is even.",
     r"fair value 3.5, quote around it (say 3.3 / 3.7); given even, fair is 4, quote 3.8 / 4.2. Ask why you are being "
     r"told: information moves fair value against the market maker"),
    (r"Deep in-the-money American call, a dividend of 2 tomorrow, rates 4\%, two months left, the put worth 0.3. "
     r"Exercise?",
     r"yes: the dividend, 2, beats the interest on the strike, $100(1 - e^{-0.04/6}) \approx 0.66$, plus the put's 0.3"),
]

PROBLEMS = [
    r"Show that a delta-hedged option earns $\int \frac12\Gamma S^2(\sigma_{r,t}^2 - \sigma_{imp}^2)\,dt$, and explain why "
    r"the same realized variance can pay very different amounts.",
    r"Show that at the money $\Gamma \approx 1/(S\sigma\sqrt{2\pi\tau})$, and compare its value a day and a minute before "
    r"expiry at $\sigma = 50\%$.",
    r"For two assets of equal weight and volatility $\sigma$, show that implied correlation is "
    r"$2\sigma_I^2/\sigma^2 - 1$.",
    r"In the die game, a counterparty knows the roll is even with probability $p$. What spread around 3.5 breaks even?",
    r"Balance the cost of trading against the variance of a mis-hedge to show that the optimal band's half-width scales "
    r"as $(\lambda S \Gamma^2/\gamma)^{1/3}$.",
    r"Derive vanna $= -\varphi(d_1)d_2/\sigma$ and volga $= \mathcal{V}d_1d_2/\sigma$, and show volga $\approx 0$ at the "
    r"money.",
    r"Show that the P\&L of a vega-matched dispersion trade has the sign of $\rho_{\text{impl}} - \rho_{\text{real}}$.",
    r"From the HJB of chapter 9, show that the optimal quotes move down when inventory is long.",    r"(qual) A competitive mean-variance dealer must hold $-d$ options with hedged residuals $\varepsilon$. Derive "
    r"$p = \mathbb E x + \gamma\Sigma_\varepsilon d$, show the cross-effects $\partial p_i/\partial d_j$ are symmetric, and "
    r"that demand has no effect when $\Sigma_\varepsilon = 0$.",
    r"(qual) For an exponential-utility dealer short $q$ units, show the indifference premium is "
    r"$\frac{1}{\gamma q}\log\mathbb E\,e^{\gamma q\varepsilon} = \frac{\gamma q}{2}\kappa_2 + \frac{\gamma^2q^2}{6}\kappa_3 + \dots$ "
    r"in the cumulants of $\varepsilon$; what does a crash-skewed residual do to large positions?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.house(load("frontier_ml"))
        self.recap(load("scalp"), load("explain"), load("premium"), load("mm_learn"), load("flow"), load("pin_btc"),
                   load("shortdated"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.next_part()

    def house(self, f):
        chart = house_chart(PART, lit=("vol",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{book\_greeks}, \texttt{pnl\_explain}", r"a book as one Taylor series, and each day explained"),
            (r"\texttt{delta\_hedge}, \texttt{delta\_hedge\_on\_moves}", r"the scalper's ledger, on the clock or on moves"),
            (r"\texttt{delta\_strike}, \texttt{vanna\_volga}", r"25-delta strikes, and a smile from three quotes"),
            (r"\texttt{markouts}, \texttt{quote}", r"what the spread keeps; quotes that lean against inventory"),
            (r"\texttt{mm\_value\_iteration}, \texttt{mm\_q\_learning}", r"the inventory game, exactly and learned"),
            (r"\texttt{greek\_hedge}, \texttt{ww\_band}", r"gamma and vega with options; hedging under costs"),
            (r"\texttt{pin\_simulation}, \texttt{american\_call\_dividend}", r"pinning; early exercise"),
            (r"\texttt{implied\_correlation}", r"index against members"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 11: every quote leans against inventory and has a limit in each Greek; every hedge "
                             r"is net of costs; every day's P\&L is explained; and no position is held into expiry near "
                             rf"its strike without a plan for the pin.  The trial counter reads {f['trials']}.", 12.4, 21,
                             QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The volatility desk now has its quoting engine. <bookmark mark='a'/> Greeks and the daily explain, "
            "the scalper's ledger, smiles from three quotes, markouts and leaning quotes, the inventory game, Greek "
            "hedges and bands, pinning, early exercise and implied correlation. <bookmark mark='b'/> The eleventh rule: every quote leans against "
            "inventory and stays within a limit in each Greek; every hedge is judged net of costs; every day's profit "
            "is explained; and nothing is held into expiry near its strike without a plan for the pin. This part "
            f"registered two tests, the forecaster's edge and the learned predictor, and the trial counter reads "
            f"{f['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def recap(self, s, e, p, m, fl, pb, sd):
        items = [
            (rf"a book is one Taylor series; a real day explained to within {100 * e['share']:.0f}\%", OPT),
            (rf"May 2021: realized {100 * s['rv']:.0f}\% against {100 * s['iv']:.0f}\% implied, yet a straddle earned "
             rf"{s['pnl']:.1f}: gamma is where the strike is, and the order of moves matters", GAMMA),
            (r"hedging more often buys precision, not profit; vanna and volga are priced by the risk reversal and "
             r"the butterfly", VEGA),
            (rf"hedged straddles lost {-p['mean']:.2f} per 100 per four weeks ($t = {p['t']:.1f}$): the volatility premium; size "
             r"it below Kelly", THETA),
            (rf"the spread is the price of informed flow: the maker keeps {100 * fl['kept_1h']:.0f}\% of its edge after an "
             rf"hour", ALT),
            (rf"inventory leans the quotes; a learner reached {100 * min(m['pct_final']):.0f}--"
             rf"{100 * max(m['pct_final']):.0f}\% of the exact optimum", ALT),
            (rf"gamma explodes at expiry; bitcoin pins weakly ($z = {pb['groups']['Fridays 08:00']['z']:.1f}$); exercise "
             r"a call early only for a dividend", GAMMA),
            (rf"implied correlation prices index risk; dispersion is short a crash", VEGA),
            (rf"short-dated OTM buyers got back {100 * (1 + sd['otm']['ret_buy']):.0f} cents per dollar; the SEBI case is "
             r"alleged and contested", THETA),
            (r"short volatility blows up when the hedge is too far away (LJM, Structured Alpha)", QC.CRISIS),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        title = label(r"Part 11 in ten lines", font_size=36).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        with self.voiceover(
            "Part eleven in ten lines. A book is one Taylor series, and a real day can be explained term by term. "
            "Gamma lives at the strike, and the order of the moves matters, not just their size. Hedging more often "
            "buys precision, not profit, and vanna and volga have market prices. Buying volatility and hedging it "
            "lost money on average: the volatility premium, which should be sized well below Kelly. The spread is the "
            "price of informed flow; inventory leans the quotes, and a simple learner finds most of the optimum. "
            "Gamma explodes at expiry, hedgers can pin a price, and a call is exercised early only for a dividend. "
            "Implied correlation prices an index's risk. Short-dated options magnify the premium against their "
            "buyers, and the case against Jane Street remains an allegation. And short volatility blows up when the "
            "hedge is too far away."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. A hedged straddle in a quiet week loses theta, and vega if implied falls. "
            "<bookmark mark='a'/> On the die, quote around three and a half, then around four once you know it is "
            "even, and ask yourself why you were told. <bookmark mark='b'/> And a deep in-the-money American call, "
            "a dividend of two tomorrow, rates at four percent, two months left, the put worth thirty cents: exercise, "
            "because the dividend beats sixty-six cents of interest plus the put. Full solutions are in the notes."
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
            "And ten problems: the gamma-theta integral, gamma at expiry, implied correlation for two assets, the "
            "die game with an informed counterparty, the scaling of the hedging band, vanna and volga, the sign of "
            "the dispersion trade, and the direction of the optimal quotes. Two are qualifying-exam problems: the "
            "dealer's demand pressure, and its exact form under exponential utility. Solutions, in English and "
            "Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the smile, variance swaps, same-day options and dealer gamma", [12]),
            (r"stochastic volatility for the book's vega risk", [13]),
            (r"exotics and their Greeks", [15]),
            (r"deep hedging and learned no-trade bands", [17]),
            (r"how many backtests a result has survived", [26]),
            (r"adverse selection, inventory and the order book", [36, 38]),
            (r"market impact, and manipulation's economics", [37, 42]),
        ])
        with self.voiceover(
            "Where this comes back. The smile, variance swaps, same-day options and dealer gamma are Part twelve. "
            "Stochastic volatility models the book's vega risk in Part thirteen, and exotics' Greeks are Part fifteen. "
            "Deep hedging grows up in Part seventeen, and Part twenty-six counts the backtests behind every edge. "
            "Adverse selection and inventory return in the order book and market-making parts, and price impact, "
            "and what makes manipulation possible, in the parts on execution and machines in the market."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Natenberg, \textit{Option Volatility and Pricing}; Sinclair, \textit{Volatility Trading} and "
             r"\textit{Positional Option Trading}",
             r"Taleb, \textit{Dynamic Hedging}; Bennett, \textit{Trading Volatility}; Hull, \textit{Options, Futures, and "
             r"Other Derivatives}"],
            [r"Glosten--Milgrom (1985); Leland (1985); Whalley--Wilmott (1997); Carr--Madan (1998); Coval--Shumway (2001)",
             r"Bakshi--Kapadia (2003); Avellaneda--Lipkin (2003); Ni--Pearson--Poteshman (2005); Castagna--Mercurio (2007)",
             r"Avellaneda--Stoikov (2008); Pool--Stoll--Whaley (2008); G\^arleanu--Pedersen--Poteshman (2009); "
             r"Driessen--Maenhout--Vilkov (2009)",
             r"Goyal--Saretto (2009); Stoikov--Sa\u{g}lam (2009); Hao--Kalay--Mayhew (2010); Golez--Jackwerth (2012); "
             r"Gu\'eant--Lehalle--Fernandez-Tapia (2013)",
             r"Muravyev--Pearson (2020); Baldacci--Bergault--Gu\'eant (2021); Bali et al.\ (2023); "
             r"Bryzgalova--Pavlova--Sikorskaya (2023); Cao et al.\ (2023)",
             r"SEBI studies (2024, 2025), interim order (2025), circular (Sept.\ 2025); SEC 2021-89, 2022-84; CFTC v.\ "
             r"Optiver"])
        with self.voiceover(
            "The books this part draws on, written by traders, and the papers, from the classic models of the "
            "market maker to this decade's machine learning. The data are Deribit's trades and implied volatility "
            "index, Binance's Bitcoin prices, Cboe's implied correlation index, Kenneth French's market and "
            "industries, and the regulators' own studies, orders and complaints."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def next_part(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 12, The Volatility Surface", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk can now quote, hedge and size. <bookmark mark='a'/> Next, Part twelve: the volatility "
            "surface. Why implied volatility depends on strike and maturity, how to fit it without arbitrage, and "
            "what local volatility makes of it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
