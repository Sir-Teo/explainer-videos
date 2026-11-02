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
    (r"You are short a large at-the-money option an hour before expiry. What worries you?",
     r"gamma near its peak: delta flips on small moves and hedging becomes expensive; and pin risk, not knowing if "
     r"you will be assigned. Reduce or roll the position before the last hour"),
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
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("scalp"), load("edge"), load("mm"), load("dispersion"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, s, e, m, d):
        items = [
            (r"a hedged option earns $\frac12\Gamma S^2$ times realized minus implied variance; theta is the bill", OPT),
            (rf"May 2021: realized {100 * s['rv']:.0f}\% against {100 * s['iv']:.0f}\% implied, yet a straddle earned "
             rf"only {s['pnl']:.1f}: gamma is where the strike is", GAMMA),
            (r"each structure is a bet on spot, volatility, or both; vanna and volga are the cross terms", VEGA),
            (rf"selling only when implied exceeds a HAR forecast earned more ($t \approx 2$, one registered test)", ALT),
            (rf"quotes that lean against inventory kept it {m['skewed']['max_abs']:.0f} instead of "
             rf"{m['no skew']['max_abs']:.0f}", OPT),
            (rf"gamma explodes at expiry; industry correlation runs from {d['low']:.2f} to {d['peaks']['1929-33']:.2f}", THETA),
            (r"India: 91\% of individual F\&O traders lost money; the Jane Street case is alleged and contested", THETA),
            (r"under costs, hedge to a band; a learned hedger matches Whalley--Wilmott", GAMMA),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 11 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part eleven in eight lines. A hedged option earns half gamma times realized minus implied variance, and "
            "theta is the bill. In May 2021 Bitcoin's realized volatility was nearly twice implied, yet a straddle "
            "earned little, because gamma lives at the strike. Every structure is a bet on spot, on volatility, or "
            "both. Selling only when implied exceeded a forecast earned more, in one registered test. Quotes that "
            "lean against inventory keep the book small. Gamma explodes at expiry, and correlations jump in crashes. "
            "In India, nine in ten individual options traders lost money, and the case against Jane Street is an "
            "allegation the firm contests. And under costs, hedge to a band; a learned hedger matched the best "
            "classical rule."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. A hedged straddle in a quiet week loses theta, and vega if implied falls. "
            "<bookmark mark='a'/> On the die, quote around three and a half, then around four once you know it is "
            "even, and ask yourself why you were told. <bookmark mark='b'/> And short a big at-the-money option an "
            "hour before expiry, worry about gamma and the pin, and get smaller before the last hour. Full solutions "
            "are in the notes."
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
            "And five problems: the gamma-theta integral, gamma at expiry, implied correlation for two assets, "
            "the die game with an informed counterparty, and the scaling of the hedging band. Solutions, in English "
            "and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the smile, vanna--volga, and variance swaps", [12]),
            (r"stochastic volatility for the book's vega risk", [13]),
            (r"deep hedging, at scale", [17]),
            (r"adverse selection, inventory and the order book", [36, 38]),
            (r"market impact, and manipulation's economics", [37, 42]),
        ])
        with self.voiceover(
            "Where this comes back. The smile, vanna-volga pricing and variance swaps are Part twelve. Stochastic "
            "volatility models the book's vega risk in Part thirteen. Deep hedging grows up in Part seventeen. "
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
             r"Taleb, \textit{Dynamic Hedging}; Bennett, \textit{Trading Volatility}"],
            [r"Leland (1985); Glosten and Milgrom (1985); Whalley and Wilmott (1997)",
             r"Castagna and Mercurio (2007); Avellaneda and Stoikov (2008); Driessen, Maenhout and Vilkov (2009)",
             r"Buehler, Gonon, Teichmann and Wood (2019); SEBI studies (2024, 2025) and interim order (2025)"])
        with self.voiceover(
            "The books this part draws on, written by traders, and the papers. The data are Deribit's implied "
            "volatility index and Binance's Bitcoin prices, Kenneth French's industries, and the regulator's own "
            "published studies and orders."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
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
