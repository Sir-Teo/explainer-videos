from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.futures_example import delivery_example
from videos.quant.quant18.common import BAD, CURV, FWD, GOOD, LEVEL, PAR, PART, POLICY, SLOPE, ZERO, load, butterfly_example

DESK = [
    (r"A 10-year zero yields 4\% annually. What duration and +1 bp price change?",
     r"$P=100/1.04^{10}=67.56$; Macaulay duration $10$, modified $10/1.04=9.62$; a +1 bp yield move costs about $0.065$ per 100 face, locally."),
    (r"Does larger convexity imply a universal price or yield ranking?",
     r"No. The quadratic price term is local, holding the specified cash flows and yield convention fixed. Prices also depend on cash flows, levels, carry, drift, options and funding; $\tfrac12 C\sigma^2$ is not a universal yield discount."),
    (r"How can a swap rate be below the Treasury yield?",
     r"Funding, collateral, balance-sheet costs and hedging demand differ. A financed Treasury plus a swap retains repo, cash-flow, basis and liquidity risk; the rate difference is not a locked arbitrage."),
    (r"Which value and liquidity measures should the SVB case motivate?",
     r"Full asset-and-liability economic-value scenarios, deposit behavior, available cash and usable collateral. A gross HTM gap or asset DV01 alone is not complete bank EVE or a solvency verdict."),
]

PROBLEMS = [
    r"For positive discount factors with $Z(t)=e^{-t z(t)}$, derive the finite and instantaneous forwards. State the differentiability assumption and when $f(t)>z(t)$.",
    r"Derive Macaulay duration for a zero and a perpetuity with positive annual yield $y$; distinguish modified duration.",
    r"For a frozen-time fixed-cash-flow price $P(y)$, derive the expected local mark from $E[\Delta y]=\mu\,dt$ and $E[(\Delta y)^2]=\sigma^2dt$. What additional terms enter total return?",
    r"A 1-year zero yields 4\% annually and a 2-year bond pays 5 annually per 100 face and prices at par. Bootstrap its annual 2-year zero rate.",
    r"In the ideal reset-date single-curve swap, derive $K^*=(1-Z(T))/A$. State receiver sensitivity near par and the away-from-par annuity term.",
    r"Fund 100 due in 15 years with 5y and 30y zeros at 4\% continuous rates. Match PV and duration, compare convexities, and distinguish the local theorem from this barbell's global parallel result.",
    r"Taylor benchmark: $r^*=\pi^*=2$, inflation 4\%, output gap $-1\%$. Compute the rate; state why this is conditional, not a mandatory policy choice.",
    r"In the local constant-duration LDI model, leverage is 4 and duration 25. Find the tangent's zero-NAV shock; after +50 bp, what fraction of remaining assets must be sold to restore the initial NAV-to-risk buffer?",
    r"(qual) For $0<\rho<1$, prove total nonnegativity of $C_{ij}=\rho^{|i-j|}$ using a triangular factorization. Give the extra oscillatory conditions and the $n=3$ eigenvectors/sign counts.",
    r"(qual) For $y(m)=m^{-1}\int_0^m f(s)ds$, express yield-change covariance from forward-change covariance $c(s,t)$. Does averaging alone guarantee total nonnegativity or three-factor concentration?",
]

class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("policy"), load("taylor"), load("bonds"), load("curve_day"), load("pca"), load("swaps"),
                   delivery_example(load("futures")), load("sofr"), load("term_example"), load("fomc"), butterfly_example(), load("ldi"), load("svb"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, po, ta, bo, cd, pc, sw, fu, so, te, fo, fl, ld, sv):
        rep = sv["facts"]["HeldToMaturitySecuritiesAccumulatedUnrecognizedHoldingLoss"]["2022-12-31"]
        eq = sv["facts"]["StockholdersEquity"]["2022-12-31"]
        items = [
            (r"administered rates guide market rates; access frictions prevent a guaranteed corridor", POLICY),
            (rf"assets fell from the April 2022 peak to November 2025 by \${po['qt']['peak']['walcl'] - po['qt']['end']['walcl']:.1f} trillion, "
             rf"with several offsetting liability changes", POLICY),
            (rf"one retrospective Taylor benchmark, using revised inputs, reached {ta['worst']['rule']:.0f}\%", POLICY),
            (r"a bond is a bundle of zeros; forwards are marginal rates; conventions decide the numbers", PAR),
            (r"bootstrapped from Treasury's quotes, fitted by Svensson, checked against the Fed's curve", ZERO),
            (rf"fixed-flow duration and convexity are local; 10-year zero DV01 per 100 face: "
             rf"{bo['zero10']['dv01']:.3f}", PAR),
            (rf"first three fitted PCs: {100 * np.sum(pc['share'][:3]):.0f}\% of sample yield-change variance", LEVEL),
            (rf"swap spreads reflect funding, balance sheet, collateral supply, hedging demand and credit conventions", FWD),
            (r"futures delivery economics depend on eligible bonds, financing, timing and delivery options", FWD),
            (rf"realized approx.91-day SOFR averaged {so['gap_hikes_bp']:.0f} bp above start fixing for Mar2022--Jul2023 starts", FWD),
            (rf"one model-dependent estimated term premium: {te['tp_1981']:.1f}\% in 1981, {te['tp_min']['v']:.1f}\% in 2020", CURV),
            (r"butterfly factor exposures and an unfinished validation design; no sealed-return test in this pass", CURV),
            (rf"LDI liquidity stress; SVB group gross HTM gap: \${rep:.1f} bn loss against \${eq:.1f} bn "
             rf"book equity; incomplete economic valuation", BAD),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        title = label(r"Part 18 in thirteen lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.7:
            rows.scale_to_fit_height(6.7)
        with self.voiceover(
            "Part eighteen in thirteen lines. Administered rates guide money markets without guaranteeing a strict corridor. Quantitative tightening changes several balance-sheet items. Taylor's rule is a conditional benchmark, especially when evaluated using revised historical data. A bond is a bundle of cash flows, and conventions determine the quoted rates. Bootstraps and approximate curve fits need different error checks. Duration and convexity are local sensitivities for specified cash flows. Three fitted factors explain most sample yield-change variance. Swap spreads involve funding, collateral, credit conventions and balance sheet. Futures have delivery options, and compounded overnight rates are realized over time. The term-premium split is model dependent. A butterfly exposure is not a completed return test; that validation remains unfinished here. The gilt episode and SVB show how leverage and unstable funding can turn low-credit-risk securities into severe balance-sheet losses."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=24))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=23) for q, a in DESK]).arrange(DOWN, buff=0.25)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Four desk questions. A ten-year zero at four percent annual yield has price sixty-seven-point-five-six, Macaulay duration ten and modified duration nine-point-six-two; one basis point up costs about six-and-a-half cents per hundred face locally. <bookmark mark='a'/> Does greater convexity impose a universal price ranking? No: the quadratic sensitivity is local, and cash flows, levels, carry and rate dynamics matter. <bookmark mark='b'/> Why can swaps fix below Treasuries? Different funding, collateral, balance-sheet costs and hedging demand; a cash-and-swap position retains risks. <bookmark mark='c'/> What does the SVB case motivate? Full asset-and-liability economic-value scenarios together with deposit behavior and liquidity stress. Asset DV01 alone is incomplete. The notes give the calculations and assumptions."
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
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Ten problems cover forwards, two durations, the local convexity term, a hand bootstrap, conditional swap sensitivity, immunization, Taylor's benchmark and an illustrative LDI buffer. The qualifying problems establish a Markov matrix's sign pattern and derive the covariance averaging formula, without claiming averaging guarantees total positivity. Worked English and Chinese solutions are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"short-rate and market models built on this curve; swaptions and Bermudans", [19]),
            (r"credit spreads measured over it; default as another discount factor", [20]),
            (r"funding and collateral: discounting at SOFR, valuation adjustments", [21]),
            (r"the macro desk: policy rates, the curve and currencies", [22]),
            (r"the finale's stress test of the whole House, rates first", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part nineteen builds term-structure models on this curve and prices swaptions. Part "
            "twenty measures credit spreads over it. Part twenty-one adds funding and collateral. Part twenty-two "
            "trades the policy rate and the curve on the macro desk. And the finale stress-tests the whole House, rates "
            "first."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Tuckman and Serrat, \textit{Fixed Income Securities}; Veronesi, \textit{Fixed Income Securities}; Fabozzi, "
             r"\textit{The Handbook of Fixed Income Securities}; Hull, \textit{Options, Futures, and Other Derivatives}, "
             r"ch.\ 4, 6, 7, 9"],
            [r"Macaulay (1938); Redington (1952); Fisher and Weil (1971); Poole (1968); Fama and Bliss (1987); Nelson and "
             r"Siegel (1987); Litterman and Scheinkman (1991); Campbell and Shiller (1991); Taylor (1993); Svensson (1994)",
             r"Kuttner (2001); Gürkaynak, Sack and Swanson (2005); Gürkaynak, Sack and Wright (2007); Adrian, Crump and "
             r"Moench (2013); Hanson and Stein (2015); Duffie and Stein (2015); Nakamura and Steinsson (2018)",
             r"Jermann (2020); Jiang, Matvos, Piskorski and Seru (2024); Federal Reserve, \textit{Review of the Supervision "
             r"and Regulation of Silicon Valley Bank} (2023); Bank of England, \textit{Quarterly Bulletin} (2023); "
             r"FOMC statement, 29 October 2025"])
        with self.voiceover(
            'The notes list textbook chapters, research papers and official records. Quantities are identified as public-data calculations, synthetic examples or published figures. The historical term-premium comparison cannot be reproduced from its pinned NY Fed vintage here, so the separately named model illustration omits that comparison. The butterfly chapter presents exposures and unfinished validation, with no sealed-return test in this pass.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("rates",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 19, Term-Structure Models", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That opens the House's rates desk: a curve, its factors, and a rule for reading risk. "
            "<bookmark mark='a'/> Next, Part nineteen: term-structure models. The curve stops being a snapshot and "
            "becomes a random process, and the options on it get prices."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
