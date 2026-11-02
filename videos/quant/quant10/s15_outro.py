from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import GAM, IMP, OPT, PART, REA

DESK = [
    (r"An at-the-money call, one year, volatility 20\%, spot 100, no rates. Price it in your head.",
     r"$C \approx 0.4\,\sigma S\sqrt T = 8$ (the formula gives 7.97)"),
    (r"You are long an at-the-money straddle and the stock does not move for a week. Did you make or lose money, "
     r"and roughly how much?", r"you lost a week of theta: $\tfrac12\Gamma S^2\sigma_i^2$ per year, for a week"),
    (r"What is the delta of an at-the-money digital call as expiry approaches, and why does that matter to the "
     r"desk that sold it?", r"it explodes: the hedge flips between none and all; desks hedge digitals as call spreads"),
]

PROBLEMS = [
    r"From the formula, prove put--call parity $C - P = S - Ke^{-rT}$, and show that $\Delta_C = N(d_1)$ using "
    r"$S\,N'(d_1) = K e^{-rT} N'(d_2)$.",
    r"Show that the CRR probability $q = (e^{r\Delta t} - d)/(u - d)$ makes the discounted stock a martingale on "
    r"the tree, and that $q \to \tfrac12$ as $\Delta t \to 0$ when $r = 0$.",
    r"A three-month at-the-money call is sold at 25\% and the stock realizes 20\%. Use "
    r"$\tfrac12\Gamma S^2(\sigma_i^2 - \sigma_r^2)$ to estimate the hedged P\&L per 100 of stock.",
    r"Leland: with a round-trip cost of 0.2\% and $\sigma = 20\%$, find $\sigma_L$ for daily and for weekly "
    r"hedging. Which is cheaper to sell?",
    r"Why is an American call on a non-dividend stock never exercised early, while an American put can be? "
    r"Give the put's early-exercise condition at $r = 0$.",
    r"Derive Leland's $\sigma_L$ from the expected size of the hedge's trade, $\mathbb E|\delta\Delta|$, per step.",
    r"With carry $b$, show that inverting with $S$ instead of $F$ raises call implied vols and lowers put implied "
    r"vols; estimate the error at the money for $b = 4\%$, $T = 0.5$, $\sigma = 45\%$.",
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
            (r"replicate with $\Delta$ shares and cash, self-financing: the drift $\mu$ drops out", OPT),
            (r"the PDE is the heat equation: the price is a Gaussian average of the payoff", OPT),
            (r"the same price as a $\mathbb Q$-expectation, and as the limit of a tree", OPT),
            (r"the Greeks are one surface; $\Theta + rS\Delta + \tfrac12\sigma^2S^2\Gamma = rV$", GAM),
            (r"the hedger earns $\tfrac12\Gamma S^2(\sigma_i^2 - \sigma_r^2)$, weighted by gamma (EKJS)", GAM),
            (r"hedging in steps: error $\propto\sqrt{\Delta t}$, and a floor under jumps", REA),
            (r"costs: Leland's volatility, the valley, and why perfect hedging is unbounded", REA),
            (r"implied volatility: one root, found fast; the smile; the Surface's first row", IMP),
            (r"carry moves the forward; early exercise has a free boundary and a premium integral", IMP),
            (r"selling volatility on Bitcoin earned a premium, with a left tail", IMP),
            (r"1987 and 1998: every hedge assumes you can trade, fund, and are not alone", QC.CRISIS),
            (r"desks speak in volatility; the 2026 frontier still races to invert it", QC.IDEA),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            n = MathTex(str(i), font_size=28, color=c)
            rows.add(VGroup(n, label(t, font_size=26)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        title = label(r"Part 10 in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.5)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        rows.next_to(title, DOWN, buff=0.35)
        with self.voiceover(
            "Part ten in twelve lines. An option is manufactured from stock and cash, and the expected return "
            "drops out. The equation is the heat equation, so the price is a Gaussian average of the payoff, an "
            "expectation under Q, and the limit of a tree. The Greeks are slopes of one surface. A hedged option "
            "is a bet on realized volatility, weighted by gamma. Hedging in steps leaves an error like the root of "
            "the step, and none of it helps across jumps; costs raise the price, without limit if you insist on "
            "perfection. Implied volatility exists, is found to machine precision, and smiles. Carry moves the "
            "forward; early exercise is a free boundary. Selling Bitcoin volatility paid, with a left tail. 1987 "
            "and 1998 showed what every hedge assumes. And desks speak the formula's language."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.5,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=27) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions, the kind trading firms ask in interviews. Price an at-the-money call in your "
            "head: the answer is about point four times sigma times S times the square root of T, which is eight "
            "here, against an exact seven point nine seven. <bookmark mark='a'/> You are long a straddle and the "
            "stock sits still for a week: you lost a week of theta, the price of the gamma you did not use. "
            "<bookmark mark='b'/> And the delta of an at-the-money digital near expiry: it explodes, which is why "
            "desks that sell digitals hedge them as tight call spreads. The full solutions are in the part's notes."
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
            "And seven problems to work through: parity and delta from the formula, the tree's martingale "
            "probability, the volatility trader's back-of-the-envelope, Leland's volatility and its derivation, "
            "early exercise, and the skew a forgotten forward draws. Solutions, in English and Chinese, are in the "
            "notes for this part."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"$\tfrac12\Gamma S^2(\sigma_i^2 - \sigma_r^2)$", [11, 12, 32]),
            (r"implied volatility and the Surface", [12, 13, 14, 17]),
            (r"the hedge as a control problem", [17, 37, 38]),
            (r"trees, PDEs and Monte Carlo", [15, 16]),
            (r"carry, forwards and currencies", [22]),
            (r"leverage, liquidity and 1998", [41]),
        ])
        with self.voiceover(
            "Where this comes back: the volatility trader's formula in Parts eleven, twelve and thirty-two; the "
            "Surface's new rows in twelve, thirteen, fourteen and seventeen; the hedge as a control problem in "
            "seventeen, thirty-seven and thirty-eight; trees, equations and simulation in fifteen and sixteen; "
            "carry in twenty-two; LTCM in forty-one."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hull, \textit{Options, Futures, and Other Derivatives}, ch. 13, 15, 17--20",
             r"Shreve, \textit{Stochastic Calculus for Finance} II, \S4.5, ch. 5, \S8.4--8.5",
             r"Bj\"ork, \textit{Arbitrage Theory in Continuous Time}, ch. 7--10; Wilmott, \textit{PWOQF}, ch. 5--9",
             r"Joshi, \textit{Concepts and Practice}; Baxter--Rennie; Taleb, \textit{Dynamic Hedging}"],
            [r"Black--Scholes (1973); Merton (1973); Black (1976); Brennan--Schwartz (1977); Boyle--Emanuel (1980)",
             r"Rubinstein--Leland (1981); Leland (1985); Barone-Adesi--Whaley (1987); Brady Commission (1988)",
             r"Kim (1990); Carr--Jarrow--Myneni (1992); Kabanov--Safarian (1997); El Karoui--Jeanblanc--Shreve (1998)",
             r"MacKenzie--Millo (2003); Derman--Taleb (2005); Ahmad--Wilmott (2005); Haug--Taleb (2011); J\"ackel (2015)",
             r"Alexander--Chen--Imeraj (2023); Matic--Packham--H\"ardle (2023); the 2026 solvers (arXiv)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number in it was computed "
            "from public data by the series' own code: Deribit's option trades and DVOL, Binance's prices, and "
            "Kenneth French's market returns."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 11, Trading Options", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has a volatility desk: a pricer and a heat-kernel solver, a hedger that also prices "
            "costs, an implied volatility solver, American approximations, portfolio insurance, and the Surface "
            "to score against. <bookmark mark='a'/> Next, Part eleven puts a trader at that desk: positions as "
            "Greeks, gamma scalping, the strategies, and the market maker's book."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
