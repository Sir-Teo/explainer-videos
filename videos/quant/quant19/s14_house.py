from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, GOOD, PART, VAS, fit_right, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.checks(load("hw"), load("hjm"), load("lmm"), load("bermudan"))
        self.risk(load("greeks"))
        self.reserve(load("bermudan"), load("reserve_example"))
        self.module()

    def card(self):
        c = chapter_card(13, r"Rule 19: the options desk for rates", r"How far should one model's price be trusted?",
                         part=PART)
        with self.voiceover("Chapter thirteen. The House's nineteenth rule, for the options desk on rates."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def checks(self, h, j, m, b):
        rb = np.asarray(m["black"]["mc"]) / np.asarray(m["black"]["exact"])
        rn = np.asarray(m["normal"]["mc"]) / np.asarray(m["normal"]["exact"])
        hj = [c["ratio"] for c in j["check"]]
        eu = max(b["europeans"])
        rows = [
            (r"Hull--White reprices today's curve", rf"\text{{worst zero}}: {100 * h['reprice_max_rel']:.2f}\%\ \text{{off}}"),
            (r"HJM: sample martingale diagnostics", rf"\text{{ratios}}\ {min(hj):.3f}\text{{--}}{max(hj):.3f}"),
            (r"market model: caplets match Black and Bachelier",
             rf"\text{{within}}\ {100 * max(np.abs(rb - 1).max(), np.abs(rn - 1).max()):.1f}\%"),
            (r"Bermudan $\geq$ every European in its schedule", rf"{1e4 * b['price']:.0f} \geq {1e4 * eu:.0f}\ \text{{bp}}"),
            (r"independent policy evaluation (sampling error remains)",
             rf"\text{{in-sample}} - \text{{out}} = {1e4 * (b['in_sample'] - b['price']):.1f}\ \text{{bp}}"),
        ]
        tab = VGroup()
        for i, (a, v) in enumerate(rows):
            tab.add(VGroup(MathTex(str(i + 1), font_size=28, color=VAS), label(a, font_size=21),
                           MathTex(v, font_size=28)).arrange(RIGHT, buff=0.35))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(LEFT * 1.6 + DOWN * 0.1)
        for r_ in tab:
            r_[2].move_to([3.9, r_.get_y(), 0], aligned_edge=LEFT)
        title = label(r"Before any rates option is priced: the model's own tests", font_size=28).to_edge(UP, buff=0.5)
        if tab.width > 12.8:
            tab.scale_to_fit_width(12.8)
        fit_right(tab)
        with self.voiceover(
            "Before trusting a rates-option price, inspect several different diagnostics; these rows are not a blanket pass certificate. <bookmark mark='a'/> Hull-White has exact initial-curve fit analytically, and a sampled repricing residual numerically. <bookmark mark='b'/> HJM's discounted-bond ratios need standard errors and convergence checks that the original saved output does not supply. <bookmark mark='c'/> The separately dated market-model example compares caplet prices with Black and Bachelier and records standard errors. <bookmark mark='d'/> In the exact exercise problem a Bermudan is worth at least each scheduled European, while numerical estimates require tolerances. <bookmark mark='e'/> A learned policy must be evaluated without future information, on independent paths. Its expected feasible payoff is a lower bound; its sample estimate is noisy. Matching a few diagnostics cannot certify every product or every market regime."
        ) as vo:
            self.play(FadeIn(title))
            for i, mk in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(mk)
                self.play(FadeIn(tab[i], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def risk(self, g):
        b, e = g["bermudan"], g["european"]
        N = 1e9
        hx = [-3.6, 0.6, 3.9]
        head = VGroup(label(r"the Bermudan", font_size=22, color=GOOD),
                      label(rf"the {int(g['T_eu'])}y into {10 - int(g['T_eu'])}y European", font_size=22, color=VAS))
        for h_, x_ in zip(head, hx[1:]):
            h_.move_to([x_, 2.2, 0])
        lines = [(r"price", b["price"] * N, e["price"] * N), (r"delta: curve up 1 bp", b["delta"] * N, e["delta"] * N),
                 (r"$\sigma$: parameter +1 bp", b["vega"] * N, e["vega"] * N)]

        def usd(x):
            return (r"-" if x < 0 else "") + rf"\${abs(x):,.0f}".replace(",", "{,}")
        cells = VGroup()
        for i, (n_, a_, c_) in enumerate(lines):
            y = 1.3 - 0.85 * i
            cells.add(VGroup(label(n_, font_size=20).move_to([hx[0], y, 0]),
                             MathTex(usd(a_), font_size=30).move_to([hx[1], y, 0]),
                             MathTex(usd(c_), font_size=30).move_to([hx[2], y, 0])))
        hedge = VGroup(
            MathTex(rf"\text{{hedge: sell }} {g['n_eu']:.2f}\ \text{{Europeans (vega)}},\ \ \text{{then receive on }} "
                    rf"{100 * g['n_swap']:.1f}\%\ \text{{of notional in the 10-year swap (delta)}}", font_size=26),
            wrapped_label(r"per \$1 billion of notional, by the lattice, bumping the curve and the volatility. The "
                          r"European hedge matches the Bermudan's vega and most of its delta; what it cannot match is "
                          r"the switch option, which is the reserve of the next screen", 12.0, 18, GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        title = label(r"The desk's morning report for one Bermudan", font_size=28).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"The risk report uses symmetric one-basis-point bumps and finite-grid prices. For a billion dollars of notional, <bookmark mark='a'/> the base values are shown first. <bookmark mark='b'/> The Bermudan's parallel-curve sensitivity is about minus {abs(b['delta']) * N / 1e3:,.0f} thousand dollars per basis point. <bookmark mark='c'/> Its sensitivity to Hull-White's instantaneous diffusion parameter sigma is about plus {b['vega'] * N / 1e3:,.0f} thousand dollars for a one-basis-point parameter bump. This is parameter vega, not a one-basis-point bump to every market swaption quote. <bookmark mark='d'/> Selling {g['n_eu']:.2f} of the selected European matches this scalar sigma sensitivity locally; a receiver swap then addresses residual parallel delta. The hedge does not match every key-rate, smile, correlation or exercise-policy exposure. Its numerical sensitivities depend on the model, bump convention and grid."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cells[i], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(hedge))
        self.wait(0.4)
        self.clear_scene()

    def reserve(self, b, scenario):
        sw = scenario["rows"]
        eu = max(b["europeans"]) * 1e4
        prices = np.array([x["bermudan"] for x in sw]) * 1e4
        a_s = [x["a"] for x in sw]
        bp, se = b["price"] * 1e4, b["se"] * 1e4
        seed = abs(b["seed1"] - b["price"]) * 1e4
        lo, hi = prices.min(), prices.max()
        nl = NumberLine(x_range=[420, 540, 20], length=10, include_numbers=True, font_size=22).shift(UP * 0.3)
        band = Rectangle(width=nl.n2p(hi)[0] - nl.n2p(lo)[0], height=0.5, stroke_width=0, fill_color=BAD,
                         fill_opacity=0.3).move_to([(nl.n2p(lo)[0] + nl.n2p(hi)[0]) / 2, nl.get_y(), 0])
        mc = Rectangle(width=max(nl.n2p(bp + 2 * se)[0] - nl.n2p(bp - 2 * se)[0], 0.04), height=0.8, stroke_width=0,
                       fill_color=GOOD, fill_opacity=0.6).move_to([nl.n2p(bp)[0], nl.get_y(), 0])
        dots = VGroup(*[VGroup(Dot(nl.n2p(p_), color=BAD, radius=0.07),
                               MathTex(rf"a = {a_:g}", font_size=18, color=GREY_A).next_to(nl.n2p(p_), UP * (1 if i % 2 else -1),
                                                                                  buff=0.55))
                        for i, (p_, a_) in enumerate(zip(prices, a_s))])
        head = label(r"The 10-non-call-1 Bermudan, in bp of notional, each volatility recalibrated to one fixed European", font_size=22
                     ).to_edge(UP, buff=0.5)
        side = VGroup(
            MathTex(rf"\text{{Monte Carlo}}:\ \pm {2 * se:.0f}\quad \text{{seed}}:\ {seed:.0f}\quad "
                    rf"\text{{mean reversion}}:\ {lo:.0f}\text{{--}}{hi:.0f}", font_size=30),
            wrapped_label(r"each scenario fits the same strike, expiry, tenor and price by solving for volatility, then prices "
                          r"the Bermudan on a finite grid. This is a sensitivity range, not a confidence interval, "
                          r"a full market calibration or an automatic accounting reserve",
                          12.0, 20, GREY_A),
        ).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"Separate numerical uncertainty from model sensitivity. The baseline Monte Carlo estimate has a displayed interval of roughly {2 * se:.0f} basis points, conditional on its learned exercise rule; a second seed changes the estimate by {seed:.0f}. <bookmark mark='a'/> Now vary mean reversion and solve for a new volatility in each scenario so that the same fixed European, with identical strike, expiry and tenor, has the same target price. This is actual recalibration, not multiplying a Bermudan by a European price ratio. The recalibrated grid prices range from {lo:.0f} to {hi:.0f} basis points. <bookmark mark='b'/> Matching one hedge leaves other aspects of the dynamics unidentified. That range is evidence of model sensitivity in this chosen family, not a bound on fair value or a prescribed reserve. It does not fit a full option surface, and the grid still requires convergence checks. A reserve policy would additionally need governance, market evidence and the risks already covered by hedges."
        ) as vo:
            self.play(FadeIn(head), Create(nl), FadeIn(mc))
            vo.wait_until("a")
            self.play(FadeIn(band), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("rates",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{vasicek\_zcb}, \texttt{cir\_zcb}, \texttt{affine\_zcb}", r"short-rate bonds; the Riccati system"),
            (r"\texttt{HullWhite}", r"fits today's curve; zero options, caps, Jamshidian swaptions, exact simulation"),
            (r"\texttt{hjm\_gaussian}, \texttt{lmm\_caplets}", r"forward-curve and market models, drift by no-arbitrage"),
            (r"\texttt{bermudan\_swaption\_lsm}", r"exercise by regression, priced on independent paths"),
            (r"\texttt{bachelier}, \texttt{normal\_iv}, \texttt{sabr\_normal\_iv}", r"normal quotes and the smile"),
            (r"\texttt{cochrane\_piazzesi}, \texttt{cpr\_scurve}, \texttt{mbs\_price}", r"bond premia; prepayment and "
                                                                                       r"mortgage pools"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=18, color=QC.HOUSE), label(b_, font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.6)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 19: every rates option model must reprice today's curve and the options it is "
                             r"calibrated to, and pass its no-arbitrage tests, before it prices anything else; every "
                             r"early-exercise price uses a rule fitted on independent paths; and each exotic needs a documented "
                             r"sensitivity assessment across models calibrated to identical hedges; ranges are not automatic reserve amounts.  "
                             r"This review adds no forecast trial and opens no sealed return test.", 12.4, 21,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The rates desk's second set of tools. <bookmark mark='a'/> Short-rate bonds and the Riccati system; Hull and White with its options and exact Gaussian state simulation; forward-curve and market models; Bermudan exercise by regression; normal quotes and SABR; and descriptive bond premia and mortgage pools. <bookmark mark='b'/> Rule nineteen: a rates option model must reproduce the curve and calibration instruments within documented numerical tolerances, and pass no-arbitrage diagnostics before pricing other claims. Evaluate a learned exercise policy on independent paths. Its expected value is a lower bound, while a finite Monte Carlo estimate still has sampling error. Compare exotic prices across plausible models calibrated to the same observable hedges. Their range is a model-risk scenario, not an automatic accounting reserve or a bound on the true price. This review adds no forecast trial and opens no sealed return test."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["rates"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
