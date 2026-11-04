from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, CIRC, CONV, FWD, GOOD, LOGN, NORMAL, PART, VAS, ZERO, load

DESK = [
    (r"Why is a Bermudan worth more than its most expensive European?",
     r"holding the Bermudan, you can follow the European's strategy (exercise on its date, if in the money) and do at "
     r"least as well, so it is worth at least as much; it is worth more because you choose the date after seeing the "
     r"path. The premium depends on how loosely rates on different dates are correlated, which no European reveals"),
    (r"A caplet is quoted at 25\% Black volatility with rates at 4\%. Roughly what normal vol is that?",
     r"$\sigma_N \approx \sigma_{\text{Black}} \times F = 0.25 \times 4\% = 1\%$, about 100 bp a year (exact at the money "
     r"for small $\sigma\sqrt T$)"),
    (r"An MBS investor hedges duration every day and rates end the year unchanged. Why can they have lost?",
     r"negative convexity is short gamma: each hedge buys duration after rates fall and sells after they rise, losing "
     r"about $\tfrac12 |C| \sigma^2$ a year on every unit, whatever the direction. The extra yield of an MBS is the "
     r"premium for selling that option"),
    (r"Hull--White reprices today's curve exactly. Why can its option prices be wrong tomorrow?",
     r"the curve is fitted, the dynamics are assumed: tomorrow the shift $\varphi$ must be refitted, and the "
     r"volatility and mean reversion were calibrated to a few options. Products that depend on what was not "
     r"calibrated (the correlation between dates, the smile) carry model risk, the reserve of Rule 19"),
]

PROBLEMS = [
    r"In Vasicek, show that $r_T$ is normal with mean $b + (r_0 - b)e^{-aT}$ and variance $\frac{\sigma^2}{2a}(1 - e^{-2aT})$, "
    r"and that long yields tend to $b - \sigma^2/(2a^2)$.",
    r"Solve the Riccati equation $B' = 1 - aB$, $B(0) = 0$, and show that a Vasicek zero is $e^{A(T) - B(T) r_0}$ "
    r"with $B(T) = (1 - e^{-aT})/a$.",
    r"In HJM with constant volatility $\sigma$ (Ho--Lee), show that the drift of $f(t, T)$ is $\sigma^2 (T - t)$. "
    r"What does it do to the forward curve over time?",
    r"In Hull--White, show that $\varphi(t) = f^M(0, t) + \frac{\sigma^2}{2a^2}(1 - e^{-at})^2$ makes the model reprice "
    r"every zero in today's curve.",
    r"Show that an at-the-money Bachelier call is worth $\sigma_N\sqrt{T/(2\pi)}$ per unit of annuity. Price a 1-year "
    r"ATM caplet on 1 of notional, quarterly, at 100 bp normal vol and a discount factor of 0.96.",
    r"Show Jamshidian's decomposition: if every $P(T, t_i; x)$ falls as $x$ rises, an option on a coupon bond equals "
    r"a sum of options on zeros, struck at $P(T, t_i; x^*)$.",
    r"Explain why a least-squares exercise rule priced on the paths it was fitted on is biased upward, and why on "
    r"independent paths it gives a lower bound.",
    r"A pool prepays at a constant CPR $c$. Show its balance (ignoring amortisation) is $(1 - c)^t$ and its average "
    r"life about $-1/\ln(1 - c)$. Compare $c = 6\%$ and $c = 45\%$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("y1994"), load("shortrate"), load("hw"), load("hjm"), load("negative"), load("lmm"),
                   load("bermudan"), load("multicurve"), load("premia"), load("mbs"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, y, s, h, j, n, m, b, mc, p, mb):
        rb = np.asarray(m["black"]["mc"]) / np.asarray(m["black"]["exact"])
        eu = max(b["europeans"])
        items = [
            (rf"1994: a {100 * y['dy5']:.1f}-point rise in the 5-year yield, and Orange County's {y['pool']['leverage']:.2f}-times levered pools",
             BAD),
            (rf"Vasicek and CIR fitted to 36 years of bills: half-lives {s['half_life_vas']:.1f} and "
             rf"{s['half_life_cir']:.1f} years; the pull's estimate is biased and wide", VAS),
            (r"affine models: every yield linear in the state; $\mathbb{P}$ and $\mathbb{Q}$ differ in drift, not "
             r"volatility; two factors decorrelate the curve", ZERO),
            (rf"Hull--White fits today's curve exactly; fitted to the market's vols, $a = {h['a']:.4f}$", VAS),
            (rf"HJM: no arbitrage fixes the drift; discounted bonds pass the martingale test", FWD),
            (r"caps and swaptions are quoted through Black or Bachelier; Jamshidian splits a swaption into zeros", ZERO),
            (rf"negative rates for eight years in the euro area, as low as {n['min']:.1f}\%: Black fails, Bachelier works",
             NORMAL),
            (r"SABR: level, skew and curvature for each expiry; the data's $\beta \approx 0.3$; its expansion fails "
             r"at long expiries", NORMAL),
            (rf"market models price caplets exactly by construction; Monte Carlo within "
             rf"{100 * np.abs(rb - 1).max():.1f}\%", LOGN),
            (rf"a Bermudan, by out-of-sample regression: {1e4 * b['price']:.0f} bp against {1e4 * eu:.0f} for the best "
             rf"European; a lattice agrees", GOOD),
            (rf"2008 split the curve: TED at {mc['peak']['pct']:.2f}\%; project on LIBOR, discount on OIS", BAD),
            (rf"bond premia, sealed hold-out: positive $R^2$ by getting the level, not the timing; counter {p['trials']}",
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
            "Part nineteen in thirteen lines. In 1994 the curve moved, and leverage turned the move into a "
            "bankruptcy. Vasicek and CIR made the short rate random; fitted to history they mean-revert slowly toward "
            "a low level, and the speed of that pull is the least reliable number in the model. Fitted to prices "
            "instead, the same model reverts to a much higher level, and the gap is the price of risk. Affine models "
            "put every yield in closed form, and a second factor lets the ends of the curve move apart. Hull and White "
            "fit today's curve exactly, and HJM showed that no arbitrage fixes the drift of every forward. Caps and "
            "swaptions are quoted in Black's or Bachelier's language, and below zero only Bachelier's survives. SABR "
            "gives each expiry its smile, with a beta the data put near one third, and market models make the "
            "market's formulas consistent. A Bermudan is worth more than any European, by an amount that depends on "
            "the model, and a lattice confirmed the simulation. 2008 split one curve into many. Bond premia can be "
            "forecast in sample; in the sealed years, only their level. And mortgages make their holders short an "
            "option, with consequences for the whole market."
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
            "Four desk questions. Why is a Bermudan worth more than its most expensive European? Because its holder "
            "can always follow the European's plan, and can do better by choosing the date after seeing the path. "
            "<bookmark mark='a'/> Twenty-five percent Black vol with rates at four percent is about one hundred basis "
            "points of normal vol. <bookmark mark='b'/> A hedged mortgage investor can lose with rates unchanged, "
            "because negative convexity is short gamma: every hedge buys high and sells low. "
            "<bookmark mark='c'/> And Hull and White can be exactly right today and wrong tomorrow, because the curve "
            "is fitted but the dynamics are assumed. Full solutions are in the notes."
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
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "And eight problems: Vasicek's distribution and long yield, its Riccati equation, the Ho-Lee drift, the "
            "Hull-White shift, an at-the-money caplet, Jamshidian's decomposition, the bias of a fitted exercise "
            "rule, and the life of a prepaying pool. Solutions, in English and Chinese, are in the notes."
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
