from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, DELTA, GOOD, IV, OPT, PART, SPOT, VEGA, load, axes, data_range, pause_card

DESK = [
    (r"Price a digital with a call spread. What width, and what happens to the hedge near expiry?",
     r"buy the $K - \varepsilon$ call and sell the $K$ call, scaled by $1/\varepsilon$: it pays at least the digital, costs "
     r"about $\varepsilon/2$ times the discounted terminal density more (smooth density), and caps Black--Scholes delta at $1/\varepsilon$ here ($r=q=0$); near expiry the hedge still "
     r"swings, but within a band the desk can trade"),
    (r"The snowball issuer's vega: what sign, and where does it peak?",
     r"the issuer owns the autocall-cancelled loss leg and owes conditional coupons; in much of our above-barrier grid "
     r"vega is positive and peaks between the barrier and start; sign and post-knock-in exposure depend on state and model"),
    (r"With zero drift in centered log price, price a maturity-paid one-touch from the matching digital.",
     r"twice the digital: every path that ends beyond the barrier touched it, and so did its mirror image"),
]

PROBLEMS = [
    r"With constant Black--Scholes coefficients, $S>H$, zero rebate and $r=q=0$, use reflection to show that a down-and-out call ($H \le K$) is worth "
    r"$C(S, K) - \frac{S}{H} C\big(\frac{H^2}{S}, K\big)$.",
    r"Explain why a barrier watched every $\Delta t$ behaves like a continuous one moved by $e^{\pm\beta\sigma\sqrt{\Delta t}}$, "
    r"and check it against a simulation.",
    r"For jointly Gaussian log prices in Black--Scholes, derive the mean and variance of the log geometric average.",
    r"Show that $\frac{(S_T-K+\varepsilon)^+-(S_T-K)^+}{\varepsilon}$ dominates the digital at every expiry price and converges to "
    r"it as $\varepsilon \to 0$.",
    r"Write the snowball as repayment, conditional coupons and an autocall-cancelled knock-in loss leg; discuss the "
    r"vega of all legs, without asserting a universal sign.",
    r"Show that the snowball's value is affine in the coupon, $V(c) = A + cB$, and solve for the fair coupon.",
    r"Price a chooser option (call or put, chosen at $t_1$) as a call plus a put, by put--call parity.",
    r"Derive Margrabe's formula for $\mathbb E[e^{-rT}(S_1 - S_2)^+]$ by changing the numeraire to $S_2$.",    r"(qual) Prove that a down one-touch at $B$ satisfies $\Pr(S_T \le B) \le \operatorname{OT} \le \min_{K > B}P(K)/(K - B)$ "
    r"at zero rates/dividends for a nonnegative UI price martingale; derive the tangent condition at a smooth interior minimizer, without assuming uniqueness.",
    r"(qual) Write the call super-hedge of an up one-touch at $B > S_0$, show it dominates on every path even with "
    r"upward gaps, and compute the bound in Black--Scholes for $\sigma = 50\%$, $T = 0.25$, $B = 1.2$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("barrier"), load("asian"), load("snowball"), load("book2024"), load("korea"), load("surrogate"),
                   load("worstof"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, b, a, s, bk, k, sg, w):
        lost = [r for r in k["rows"] if r["knocked_in"]]
        dl = np.asarray(bk["dealer_delta"])
        px = np.asarray(bk["close"])
        o = load("outcomes")
        d = load("decompose")
        items = [
            (rf"a note is a bond, a coupon strip and a short put: the put is {abs(d['blocks']['dip']):.3f} of every 1", OPT),
            (r"buyers' record: fees and complexity ate the crash-put premium; vintage decided the rest", GOOD),
            (r"barriers: reflection, the closed form, and its image in the PDE", BARRIER),
            (rf"watched monthly a knock-out is worth {b['rows'][0]['mc']:.2f}, not {b['continuous']:.2f}; static hedges "
             r"need a symmetric smile", BARRIER),
            (r"a digital has a difficult discrete hedge; a held call spread gives a terminal payoff overhedge", BAD),
            (rf"the continuous geometric log-average has variance $\sigma^2T/3$; a control variate reduces sampling noise", QC.HOUSE),
            (rf"the snowball's fair coupon, {100 * o['coupon']:.1f}\%, is a linear solve; {100 * o['p_ko']:.0f}\% knock out",
             IV),
            (r"the issuer's hedge falls off a cliff at the knock-in; its vega peak and sign depend on state and model", DELTA),
            (rf"January 2024: hedges grew to {dl.max():.0f} notes' worth and were cut to {dl[np.argmin(px)]:.0f}; Korea "
             rf"lost {100 * min(-r['return'] for r in lost):.0f}--{100 * max(-r['return'] for r in lost):.0f}\%", BAD),
            (r"worst-of investors sell the loss put (long correlation); cliquets retain risks beyond aggregate vega", GOOD),
            (r"model risk has a price: uncertain volatility, model ranges, entropy worst cases", VEGA),
            (rf"a network reprices a snowball in {1e6 * sg['t_net']:.1f} microseconds; a polynomial can do as well", VEGA),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        title = label(r"Part 15 in twelve lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.6:
            rows.scale_to_fit_height(6.6)
        with self.voiceover(
            "The main results. Specify the note's conditional cash flows before interpreting its coupon. Match barrier monitoring and state history. A call-spread payoff can protect a digital seller statically, while discrete dynamic hedging still has error. Geometric Asian controls reduce sampling noise. A snowball coupon is an affine solve, but its state-dependent Greeks need careful signs and units. Historical reconstructions are not observed dealer trades. Worst-of investors sell a loss put; cliquets retain risks beyond aggregate vega. Approximate model fits do not define identical marginals. Entropy tilts, regulatory adjustments and model-free bounds solve different questions. Fast proxies require domain, error and cost disclosures."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=24))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three checks. Distinguish a call spread's terminal payoff dominance from its discrete hedge error. <bookmark mark='a'/> Compute the snowball issuer's vega from every contingent leg; use the plotted grid, rather than assume one universal sign. <bookmark mark='b'/> For a zero-drift centered log process, reflection gives twice the matching terminal digital for a maturity-paid one-touch. Zero stock drift is a different condition. The notes include a fourth dependence question and full worked solutions."
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
            'Ten problems and bilingual solutions are in the notes. They cover reflection, monitoring, Asian controls, payoff dominance, affine coupons, chooser parity and change of numeraire. Two advanced problems derive martingale one-touch bounds and the up-touch hedge, including atoms, gaps and the tangent condition.'
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Monte Carlo, PDEs and Greeks for path-dependent payoffs", [16]),
            (r"neural pricers and hedgers at scale", [17]),
            (r"the issuer's credit: the funding spread in every coupon", [20, 21]),
            (r"square-root impact of the hedgers' trades", [37]),
            (r"crowded hedges, leverage and crises", [41]),
        ])
        with self.voiceover(
            "Where this comes back. Part sixteen builds the Monte Carlo and finite-difference engines these prices "
            "need, with Greeks. Part seventeen trains pricers and hedgers at scale. Every note is also the issuer's "
            "debt, which Parts twenty and twenty-one price. The hedgers' trades meet the square-root law of impact "
            "in Part thirty-seven. And crowded hedges return in Part forty-one, on crises."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hull, \textit{Options, Futures, and Other Derivatives}, ``Exotic options''; Shreve, \textit{Stochastic Calculus for "
             r"Finance II}, ch.\ 7; Bouzoubaa and Osseiran, \textit{Exotic Options and Hybrids}",
             r"Guyon and Henry-Labord\`ere, \textit{Nonlinear Option Pricing}; Wilmott, \textit{Paul Wilmott on "
             r"Quantitative Finance}; Gatheral, \textit{The Volatility Surface}; Taleb, \textit{Dynamic Hedging}"],
            [r"Merton (1973); Margrabe (1978); Goldman, Sosin, Gatto (1979); Stulz (1982); Kemna, Vorst (1990); "
             r"Reiner, Rubinstein (1991)",
             r"Avellaneda, Levy, Par\'as (1995); Lyons (1995); Derman, Ergener, Kani (1995); Avellaneda, Par\'as (1996); "
             r"Broadie, Glasserman, Kou (1997); Carr, Ellis, Gupta (1998)",
             r"Vecer (2001); Cont (2006); Carr, Lee (2009); Henderson, Pearson (2011); Glasserman, Xu (2014); "
             r"C\'el\'erier, Vall\'ee (2017); Egan (2019); Calvet et al.\ (2023); Petra Vokata (2021, JFE)",
             r"Frontier: Glasserman, Karmarkar (2025); Lakshtanov (2026); Sharma et al.\ (2024); Zeron, Wu, Ruiz "
             r"(2023); and chapter 18",
             r"Industry: Bloomberg, Caixin, Risk.net, Asia Financial (2023--24); FSC (2016); FSS via Korean press "
             r"(2024--25); Natixis (2018); EU 2016/101; IFRS 9; Basel MAR23"], font_size=19)
        with self.voiceover(
            'The notes link the textbook coverage, primary papers and dated public reports. ETF closes, the HSCEI and the bitcoin option data support different, explicitly labeled examples. The original compute command rebuilds the numerical illustrations; source and evidence records identify their scope.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 16, Computing Prices", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk can now price, hedge and reserve for the products it sells. "
            "<bookmark mark='a'/> Next, Part sixteen: computing prices. Monte Carlo and its variance reduction, "
            "finite differences, Fourier methods and adjoint Greeks, and how fast each one really is."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
