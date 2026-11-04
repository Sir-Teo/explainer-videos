from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, GOOD, PART, VAS, load


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.checks(load("hw"), load("hjm"), load("lmm"), load("bermudan"))
        self.risk(load("greeks"))
        self.reserve(load("bermudan"))
        self.module(env)

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
            (r"HJM: discounted bonds are martingales", rf"\text{{ratios}}\ {min(hj):.3f}\text{{--}}{max(hj):.3f}"),
            (r"market model: caplets match Black and Bachelier",
             rf"\text{{within}}\ {100 * max(np.abs(rb - 1).max(), np.abs(rn - 1).max()):.1f}\%"),
            (r"Bermudan $\geq$ every European in its schedule", rf"{1e4 * b['price']:.0f} \geq {1e4 * eu:.0f}\ \text{{bp}}"),
            (r"exercise rule fitted on other paths (a lower bound)",
             rf"\text{{in-sample}} - \text{{out}} = {1e4 * (b['in_sample'] - b['price']):.1f}\ \text{{bp}}"),
        ]
        tab = VGroup()
        for i, (a, v) in enumerate(rows):
            tab.add(VGroup(MathTex(r"\checkmark", font_size=32, color=GOOD), label(a, font_size=21),
                           MathTex(v, font_size=28)).arrange(RIGHT, buff=0.35))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(LEFT * 1.6 + DOWN * 0.1)
        for r_ in tab:
            r_[2].move_to([3.9, r_.get_y(), 0], aligned_edge=LEFT)
        title = label(r"Before any rates option is priced: the model's own tests", font_size=28).to_edge(UP, buff=0.5)
        if tab.width > 12.8:
            tab.scale_to_fit_width(12.8)
        with self.voiceover(
            "Before the desk prices anything, each model passes its own tests, the ones this part ran. "
            "<bookmark mark='a'/> Hull and White must give back today's curve. <bookmark mark='b'/> In HJM, "
            "discounted bonds must be martingales. <bookmark mark='c'/> The market model's caplets must match the "
            "market's formulas. <bookmark mark='d'/> A Bermudan must be worth at least every European in its "
            "schedule. <bookmark mark='e'/> And its exercise rule must be fitted on one set of paths and priced on "
            "another. Each test is a way the code can be wrong while still producing a number."
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
                 (r"vega: normal vol up 1 bp", b["vega"] * N, e["vega"] * N)]

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
            "Every morning the desk reports each position's risks, computed here by the lattice, bumping the curve "
            "and the volatility. For a billion dollars of the Bermudan: <bookmark mark='a'/> its price, "
            f"<bookmark mark='b'/> a loss of about {abs(b['delta']) * N / 1e3:,.0f} thousand dollars for each basis "
            f"point the curve rises, <bookmark mark='c'/> and a gain of {b['vega'] * N / 1e3:,.0f} thousand for each "
            "basis point of volatility. <bookmark mark='d'/> The natural hedge is the most valuable European: sell "
            f"{g['n_eu']:.2f} of them to match the vega, and a small receiver swap takes care of the delta that is "
            "left. What no European hedges is the right to switch dates."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cells[i], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(hedge))
        self.wait(0.4)
        self.clear_scene()

    def reserve(self, b):
        sw = b["sweep"]
        eu = max(b["europeans"]) * 1e4
        ratios = np.array([x["bermudan"] / x["best_european"] for x in sw])
        prices = ratios * eu
        a_s = [x["a"] for x in sw]
        bp, se = b["price"] * 1e4, b["se"] * 1e4
        seed = abs(b["seed1"] - b["price"]) * 1e4
        lo, hi = prices.min(), prices.max()
        nl = NumberLine(x_range=[420, 500, 10], length=10, include_numbers=True, font_size=22).shift(UP * 0.3)
        band = Rectangle(width=nl.n2p(hi)[0] - nl.n2p(lo)[0], height=0.5, stroke_width=0, fill_color=BAD,
                         fill_opacity=0.3).move_to([(nl.n2p(lo)[0] + nl.n2p(hi)[0]) / 2, nl.get_y(), 0])
        mc = Rectangle(width=max(nl.n2p(bp + 2 * se)[0] - nl.n2p(bp - 2 * se)[0], 0.04), height=0.8, stroke_width=0,
                       fill_color=GOOD, fill_opacity=0.6).move_to([nl.n2p(bp)[0], nl.get_y(), 0])
        dots = VGroup(*[VGroup(Dot(nl.n2p(p_), color=BAD, radius=0.07),
                               MathTex(rf"a = {a_:g}", font_size=18, color=GREY_A).next_to(nl.n2p(p_), UP * (1 if i % 2 else -1),
                                                                                  buff=0.55))
                        for i, (p_, a_) in enumerate(zip(prices, a_s))])
        head = label(r"The 10-non-call-1 Bermudan, in bp of notional, every model matched to the same best European", font_size=22
                     ).to_edge(UP, buff=0.5)
        side = VGroup(
            MathTex(rf"\text{{Monte Carlo}}:\ \pm {2 * se:.0f}\quad \text{{seed}}:\ {seed:.0f}\quad "
                    rf"\text{{mean reversion}}:\ {lo:.0f}\text{{--}}{hi:.0f}", font_size=30),
            wrapped_label(r"the mean reversion is not pinned down by the European the desk hedges, so the range across "
                          r"plausible values is the model's uncertainty: several times the simulation error. The House "
                          r"books the price and holds the range as a reserve until the trade is hedged or has expired",
                          12.0, 20, GREY_A),
        ).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Then the price, and its uncertainty. The Monte Carlo error on the Bermudan is about "
            f"{2 * se:.0f} basis points either way, and a second seed moves it by {seed:.0f}. <bookmark mark='a'/> But "
            "mean reversion is not pinned down by the European the desk hedges. Scale each model to that same "
            f"European, and the Bermudan ranges from {lo:.0f} to {hi:.0f}. <bookmark mark='b'/> The model is the "
            "larger error by far. The lattice of chapter nine removed the simulation's noise and left this range "
            "exactly where it was: no amount of computing narrows it, only better evidence on how rates on different "
            "dates move together. So the House books the central price and holds the range as a reserve until the "
            "risk is hedged or gone."
        ) as vo:
            self.play(FadeIn(head), Create(nl), FadeIn(mc))
            vo.wait_until("a")
            self.play(FadeIn(band), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def module(self, env):
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
                             r"early-exercise price uses a rule fitted on independent paths; and every exotic carries a "
                             r"reserve equal to its price range across models that fit the same hedges.  "
                             rf"Two forecasts registered here: the counter reads {env['trials']}.", 12.4, 21,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The rates desk's second set of tools. <bookmark mark='a'/> Short-rate bonds and the Riccati system; Hull "
            "and White with its options and exact simulation; the forward-curve and market models; the Bermudan by "
            "regression; normal quotes and SABR; and bond premia and mortgage pools. <bookmark mark='b'/> And the "
            "nineteenth rule. Every rates option model reprices today's curve and the options it is fitted to, and "
            "passes its no-arbitrage tests, before it prices anything else. Every early-exercise price uses a rule "
            "fitted on independent paths. And every exotic carries a reserve, the range of its price across models "
            "that fit the same hedges. Two forecasts were registered in this part, and the counter reads "
            f"{env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["rates"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
