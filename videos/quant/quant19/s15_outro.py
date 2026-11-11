from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, CIRC, CONV, FWD, GOOD, LOGN, NORMAL, PART, VAS, ZERO, load

DESK = [('Why is a Bermudan worth at least its best scheduled European?',
  "the holder can use that European's exercise rule. Strictly greater value needs useful flexibility; a "
  'finite numerical estimate still has error'),
 ('25\\% Black volatility at a 4\\% forward: approximate normal vol?',
  '$\\sigma_N\\approx F\\sigma_B=1\\%$: 100 bp per square-root year, near ATM with small total volatility; '
  'an approximation'),
 ('Why can a duration-hedged MBS lose on a round trip in rates?',
  'negative effective convexity can produce a loss from realized rate variation. Locally, relative convexity '
  'PnL is about $\\frac12 C\\sum(\\Delta y)^2$ under ideal hedging, before carry, prepayment changes, spread '
  'moves and costs'),
 ("Why does fitting today's curve not settle tomorrow's option prices?",
  'the curve fixes the shift, not all dynamics. This example uses historical yield-vol proxies; a market '
  'model must be calibrated to relevant option quotes and checked outside the calibration set')]

PROBLEMS = ['Under the pricing-measure Vasicek model with $a>0$, derive the Gaussian transition and long yield '
 '$b-\\sigma^2/(2a^2)$.',
 "Solve the Riccati equation $B' = 1 - aB$, $B(0) = 0$, and show that a Vasicek zero is $e^{A(T) - B(T) "
 'r_0}$ with $B(T) = (1 - e^{-aT})/a$.',
 'In HJM with constant volatility $\\sigma$ (Ho--Lee), show that the drift of $f(t, T)$ is $\\sigma^2 (T - '
 't)$. What does it do to the forward curve over time?',
 'For Hull--White with $x_0=0$, derive the shift $\\varphi(t)=f^M(0,t)+\\sigma^2(1-e^{-at})^2/(2a^2)$.',
 'Show that an at-the-money Bachelier call is worth $\\sigma_N\\sqrt{T/(2\\pi)}$ per unit of annuity. Price '
 'a 1-year ATM caplet on 1 of notional, quarterly, at 100 bp normal vol and a discount factor of 0.96.',
 "Prove Jamshidian's decomposition for nonnegative coupon weights, monotone zero prices and an existing "
 'unique par root.',
 'Explain look-ahead in same-path exercise evaluation, the separate approximation error, and why independent '
 'policy evaluation gives an expected lower bound with sampling noise.',
 'With continuous survival $S(t)=(1-c)^t$, no amortization and no final maturity, compute $\\int_0^\\infty '
 'S(t)dt$. How does annual discrete prepayment differ?',
 '(qual) If $s_n \\sim N(a_n, \\sigma_n^2)$ under the forward measure, show $\\mathbb E[\\max(s_n, r)] = r + '
 "\\sigma_n g((a_n - r)/\\sigma_n)$ with $g(z) = z\\Phi(z) + \\varphi(z)$, and that $g' = \\Phi$.",
 '(qual) In the one-factor shadow model, show $\\partial f(n)/\\partial s_t \\approx \\Phi(z_n)e^{-\\kappa '
 "n}$ and explain why the 1-year yield's response to news collapses near the floor while the 10-year's does "
 'not.']


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("y1994"), load("shortrate"), load("hw"), load("hjm"), load("negative"), load("lmm"),
                   load("bermudan"), load("multicurve"), load("mbs"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, y, s, h, j, n, m, b, mc, mb):
        rb = np.asarray(m["black"]["mc"]) / np.asarray(m["black"]["exact"])
        eu = max(b["europeans"])
        items = [
            (rf"1994: a {100 * y['dy5']:.1f}-point rise in the 5-year yield, and Orange County's {y['pool']['leverage']:.2f}-times levered pools",
             BAD),
            (rf"Vasicek and CIR fitted to 36 years of bills: half-lives {s['half_life_vas']:.1f} and "
             rf"{s['half_life_cir']:.1f} years; the pull's estimate is biased and wide", VAS),
            (r"affine models: every yield linear in the state; $\mathbb{P}$ and $\mathbb{Q}$ differ in drift, not "
             r"volatility; two factors decorrelate the curve", ZERO),
            (rf"Hull--White fits today's curve exactly; historical yield-vol proxy, $a = {h['a']:.4f}$", VAS),
            (rf"HJM: no arbitrage fixes the drift; discounted-bond diagnostics need error estimates", FWD),
            (r"caps and swaptions are quoted through Black or Bachelier; Jamshidian splits a swaption into zeros", ZERO),
            (rf"negative rates for eight years in the euro area, as low as {n['min']:.1f}\%: Black fails, Bachelier works",
             NORMAL),
            (r"SABR: level, skew and curvature for each expiry; historical slope is not pricing-measure beta; its expansion fails "
             r"at long expiries", NORMAL),
            (rf"market models price caplets exactly by construction; Monte Carlo within "
             rf"{100 * np.abs(rb - 1).max():.1f}\%", LOGN),
            (rf"a Bermudan, by out-of-sample regression: {1e4 * b['price']:.0f} bp against {1e4 * eu:.0f} for the best "
             rf"European; a lattice agrees", GOOD),
            (rf"2008 split the curve: TED at {mc['peak']['pct']:.2f}\%; project on LIBOR, discount on OIS", BAD),
            (r"bond premia: descriptive predictability; sealed forecast validation remains unopened in this review",
             CIRC),
            (rf"mortgages: negative convexity ({mb['convexity']:.0f}), hedging loops, and the Fed's \${mb['fed']['peak']['v']:.2f} "
             r"trillion", CONV),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        title = label(r"Part 19 in thirteen lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.7:
            rows.scale_to_fit_height(6.7)
        with self.voiceover(
            'Part nineteen in thirteen lines. In 1994 leverage amplified a bond-market loss. Vasicek and CIR made the short rate random. Historical fits and pricing fits use different probability measures, and mean reversion is hard to estimate. Affine models turn bond pricing into Riccati equations; a second factor can decorrelate curve changes. Hull and White fit the initial discount curve, while HJM fixes the forward drift under a pricing measure. Black and Bachelier provide quote conventions; the unshifted Black formula requires positive forwards and strikes. SABR models smiles, with an asymptotic formula that needs arbitrage checks. Market models tie caplet marginal laws to a joint rate model. A Bermudan is worth at least its best scheduled European in the exact model, and independent-path evaluation avoids using future exercise information. Numerical errors still require tolerances. Collateral and tenor bases motivate multiple curves. Descriptive bond-return regressions motivate a forecast protocol; no sealed test is opened here. Mortgage investors bear prepayment risk and can have negative convexity.'
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
            "Four desk questions. A Bermudan is worth at least its best scheduled European because that rule is available to its holder. Strictly greater value needs a useful extra exercise choice. <bookmark mark='a'/> Twenty-five percent Black volatility at a four-percent forward is about one hundred basis points per square root year in normal terms, near the money and for small total volatility. <bookmark mark='b'/> A duration-hedged mortgage position can lose on a round trip because negative convexity responds to realized rate variation. A local constant-convexity approximation depends on squared rate increments, but carry, spread moves, changing prepayments, hedge instruments and transaction costs also affect total profit. <bookmark mark='c'/> Fitting today's curve fixes a shift, not all future dynamics. This example used historical volatility proxies, while an options desk needs relevant market calibration and checks beyond those instruments. Recalibrating tomorrow is an operational choice, not a mathematical requirement for the original model to remain internally consistent."
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
            "And ten problems: Vasicek's distribution and long yield, its Riccati equation, the Ho-Lee drift, the "
            "Hull-White shift, an at-the-money caplet, Jamshidian's decomposition, the bias of a fitted exercise "
            "rule, and the life of a prepaying pool. Two are qualifying-exam problems: Wu and Xia's call formula, "
            "and the dead short end. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"default intensities are short rates: survival is discounting, CIR again", [20]),
            (r"collateral, funding and the valuation adjustments behind OIS discounting", [21]),
            (r"the macro desk: the Treasury basis trade, inflation swaps, FX forwards off two curves", [22]),
            (r"testing forecasts without fooling yourself; machine learning for returns", [26, 27]),
            (r"the finale's stress test: every rates model under the House's worst days", [43]),
        ])
        with self.voiceover(
            "Where this comes back. In Part twenty a default intensity behaves exactly like a short rate, and survival "
            "is discounting. Part twenty-one takes up collateral, funding and the valuation adjustments. Part "
            "twenty-two builds the macro desk: the basis trade, inflation and currencies. Parts twenty-six and "
            "twenty-seven return to forecasting returns, and to testing forecasts honestly. And the finale stress-tests every rates model on the House's worst days."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Brigo and Mercurio, \textit{Interest Rate Models: Theory and Practice}; Andersen and Piterbarg, "
             r"\textit{Interest Rate Modeling}, vols.\ II--III; Rebonato, \textit{Volatility and Correlation}; James and "
             r"Webber, \textit{Interest Rate Modelling}"],
            [r"Bachelier (1900); Black (1976); Vasicek (1977); Cox, Ingersoll and Ross (1985); Ho and Lee (1986); Fama "
             r"and Bliss (1987); Jamshidian (1989, 1997); Black, Derman and Toy (1990); Hull and White (1990, 1994); "
             r"Black and Karasinski (1991); Campbell and Shiller (1991); Heath, Jarrow and Morton (1992)",
             r"Duffie and Kan (1996); Brace, Gatarek and Musiela (1997); Miltersen, Sandmann and Sondermann (1997); "
             r"Longstaff and Schwartz (2001); Hagan, Kumar, Lesniewski and Woodward (2002); Ang and Piazzesi (2003); "
             r"Cochrane and Piazzesi (2005); Piterbarg (2010); Lyashenko and Mercurio (2019); Bianchi, Büchner and "
             r"Tamoni (2021)",
             r"SEC administrative proceedings on Orange County (1996); CME Group notices, April 2020"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Bachelier's thesis in 1900 to the "
            "forward market model for SOFR. Every number on screen was computed from public data: the Fed's fitted "
            "curve, FRED, Freddie Mac's survey, and the SEC's record of Orange County."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("rates",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 20, Credit", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That completes the rates desk's models: the curve as a random process, and prices for the options on it. "
            "<bookmark mark='a'/> Next, Part twenty: credit. A bond that can default, a spread that measures the "
            "chance, and the instruments that trade it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
