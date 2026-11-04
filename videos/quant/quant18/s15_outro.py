from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, CURV, FWD, GOOD, LEVEL, PAR, PART, POLICY, SLOPE, ZERO, load

DESK = [
    (r"A 10-year zero yields 4\% (annual). Duration? Price change for +1 bp?",
     r"price $100/1.04^{10} = 67.56$; Macaulay duration 10 (a zero pays once), modified $10/1.04 = 9.62$; DV01 $= 9.62 "
     r"\times 67.56 \times 0.0001 = 0.065$: one basis point up costs about 6.5 cents per 100 of face"),
    (r"Why does convexity cost money?",
     r"with the same yield and duration, the more convex bond beats the other in any large move, either way; if both "
     r"yielded the same, you could buy one, sell the other and profit from volatility alone. So convexity trades at a "
     r"lower yield: about $\tfrac12 C \sigma^2$ a year, where $\sigma$ is the volatility of yields"),
    (r"How can a swap rate be below the Treasury yield?",
     r"the arbitrage (buy the bond in repo, pay fixed) ties up a dealer's balance sheet for the bond's life, and balance "
     r"sheet costs capital since 2008; meanwhile pension funds and insurers receive fixed at the long end. Jermann (2020): "
     r"a holding cost makes the no-arbitrage spread negative, most at long maturities"),
    (r"SVB's assets could not default. What should its risk report have shown?",
     r"the economic value of equity under a rate shock: $-D \times \Delta y \times$ assets, by key rate, against the "
     r"deposits' own duration. With 94\% of deposits uninsured that duration was close to zero, so a 6-year book was "
     r"an unhedged bet on rates"),
]

PROBLEMS = [
    r"Show that $f(t_1, t_2) = (z_2 t_2 - z_1 t_1)/(t_2 - t_1)$ and that the instantaneous forward is $f(t) = z(t) + t\,z'(t)$. "
    r"When does the forward curve lie above the zero curve?",
    r"Show that the Macaulay duration of a zero-coupon bond is its maturity, and that of a perpetuity paying $c$ a year at "
    r"yield $y$ (annual) is $(1 + y)/y$.",
    r"For a parallel shift with variance $\sigma^2\,dt$, show that a bond's expected return over $dt$ is about "
    r"$y\,dt + \tfrac12 C \sigma^2\,dt$, so convexity is worth $\tfrac12 C\sigma^2$ a year.",
    r"A 1-year zero yields 4\% and a 2-year bond with a 5\% annual coupon prices at par. Bootstrap the 2-year zero rate.",
    r"Show that a swap's par rate is $K^* = (1 - Z(T))/A$ and that its DV01 is about $A \times 0.0001$.",
    r"A liability of 100 is due in 15 years; rates are 4\% (continuous) at every maturity. Fund it with 5- and 30-year "
    r"zeros, matching value and duration, and check Redington's convexity condition.",
    r"Taylor's rule with $r^* = \pi^* = 2$: what rate does it prescribe for inflation of 4\% and an output gap of $-1\%$?",
    r"An LDI pool has leverage 4 in gilts of duration 25. What yield rise wipes it out? After a 50 bp rise, what fraction "
    r"of its gilts must it sell to restore its original buffer?",    r"(qual) Show that the $n \times n$ matrix $\rho^{|i - j|}$, $0 < \rho < 1$, is totally nonnegative (its inverse is "
    r"tridiagonal), and verify the sign-change pattern of its eigenvectors for $n = 3$.",
    r"(qual) Yields are averages of forward rates, $y(m) = \frac1m\int_0^m f$. If forward changes have covariance "
    r"$c(s, t)$, write the covariance of yield changes, and explain why averaging tends to make it smoother and closer to "
    r"total positivity.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("policy"), load("taylor"), load("bonds"), load("curve_day"), load("pca"), load("swaps"),
                   load("futures"), load("sofr"), load("term"), load("fomc"), load("fly"), load("ldi"), load("svb"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, po, ta, bo, cd, pc, sw, fu, so, te, fo, fl, ld, sv):
        rep = sv["facts"]["HeldToMaturitySecuritiesAccumulatedUnrecognizedHoldingLoss"]["2022-12-31"]
        eq = sv["facts"]["StockholdersEquity"]["2022-12-31"]
        items = [
            (r"the Fed sets rates by paying them: interest on reserves and the reverse repo bracket the market", POLICY),
            (rf"QT shrank the balance sheet by \${po['qt']['peak']['walcl'] - po['qt']['end']['walcl']:.1f} trillion, "
             rf"mostly out of reverse repos", POLICY),
            (rf"Taylor's rule tracked policy until 2008; in 2022 it called for {ta['worst']['rule']:.0f}\%", POLICY),
            (r"a bond is a bundle of zeros; forwards are marginal rates; conventions decide the numbers", PAR),
            (r"bootstrapped from Treasury's quotes, fitted by Svensson, checked against the Fed's curve", ZERO),
            (rf"duration is the balance point; convexity is on the holder's side; DV01 of a 10-year zero "
             rf"{bo['zero10']['dv01']:.3f}", PAR),
            (rf"level, slope and curvature: {100 * np.sum(pc['share'][:3]):.0f}\% of daily moves", LEVEL),
            (rf"swap spreads turned negative: balance sheet, not risk", FWD),
            (r"the future tracks the cheapest note, and the cheapest switches at about 6\%", FWD),
            (rf"SOFR in arrears paid {so['gap_hikes_bp']:.0f} bp more than its first day while the Fed hiked", FWD),
            (rf"the term premium, re-estimated: {te['tp_1981']:.1f}\% in 1981, {te['tp_min']['v']:.1f}\% in 2020", CURV),
            (rf"the butterfly, pre-registered: Sharpe {fl['out']['sharpe']:.2f} in the hold-out; counter {fl['trials']}",
             BAD),
            (rf"gilts: leverage turned a solvent hedge into a fire sale; SVB: a \${rep:.1f} bn loss against \${eq:.1f} bn "
             rf"of equity", BAD),
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
            "Part eighteen in thirteen lines. The Fed sets rates by paying them, and the market lives between its "
            "administered rates. Quantitative tightening came mostly out of the reverse repo buffer. Taylor's rule "
            "tracked policy until 2008, and was ignored in 2022. A bond is a bundle of zero-coupon bonds, forwards are "
            "marginal rates, and conventions decide the numbers. We bootstrapped a curve from Treasury's quotes, fitted "
            "it, and checked it against the Fed's. Duration is a balance point, convexity a gift to the holder. Three "
            "factors move the curve. Swap spreads went negative for reasons of balance sheet, not risk. A future tracks "
            "its cheapest bond, and SOFR in arrears makes borrowers bear hikes as they happen. The term premium "
            "explains why long yields can rise while the Fed cuts. One relative-value trade, tested honestly, lost. "
            "And two crises showed how default-free bonds still break things: through leverage, and through funding "
            "that can leave in a day."
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
            "Four desk questions. A ten-year zero at four percent: price sixty-seven fifty-six, duration ten, about six "
            "and a half cents a basis point. <bookmark mark='a'/> Why does convexity cost money? Because with the same "
            "yield and duration, the more convex bond wins in any large move, so it must yield less: about half its "
            "convexity times the variance of yields, every year. <bookmark mark='b'/> How can a swap rate sit below the "
            "Treasury yield? Because the arbitrage ties up balance sheet for thirty years, and balance sheet costs "
            "capital. <bookmark mark='c'/> And what should Silicon Valley Bank's risk report have shown? The economic "
            "value of its equity under a rate shock, key rate by key rate, against deposits that could leave overnight. "
            "Full solutions are in the notes."
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
            "And ten problems: forward rates, two durations, the value of convexity, a bootstrap by hand, the par swap "
            "rate, Redington's conditions, Taylor's rule, and an LDI pool's buffer. Two are qualifying-exam problems: "
            "total positivity of a Markov correlation, and why averaging smooths. Solutions, in English and Chinese, "
            "are in the notes."
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
            "The textbook chapters this part covers, and the papers and official records it draws on, from Macaulay's "
            "duration in 1938 to the Fed's decision of October 2025. Every number on screen was computed from public "
            "data: the Fed's fitted curve, Treasury's quotes and auction records, FRED, the New York Fed, and the "
            "filings on EDGAR."
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
