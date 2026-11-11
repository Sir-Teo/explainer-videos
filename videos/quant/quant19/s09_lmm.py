from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import FWD, LOGN, NORMAL, PART, ask, fit_right, illustration, load


class LMM(VoiceoverScene):
    def construct(self):
        m = load("lmm")
        self.card()
        self.derive()
        self.check(m)
        self.corr(load("lmmcorr"))
        self.fmm()

    def card(self):
        c = chapter_card(8, r"Market models: LIBOR and SOFR", r"Can a model agree with the market's own formulas?",
                         lit=(1997,), part=PART)
        with self.voiceover("Chapter eight. Market models: making the market's formulas consistent with each other."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"L_i(t)", r"=", r"\frac{1}{\delta}\Big(\frac{P(t, T_i)}{P(t, T_{i+1})} - 1\Big)", font_size=40,
                      colors={r"L_i(t)": FWD}),
                cmath(r"dL_i", r"=", r"\sigma_i L_i\,dW^{\,i+1}\quad\text{(lognormal; or } \sigma_i\,dW\text{, normal)}",
                      font_size=38, colors={r"dL_i": FWD}),
                cmath(r"dL_j", r"=", r"-\,\sigma_j L_j\sum_{k > j}\frac{\delta\,\sigma_k L_k}{1 + \delta L_k}\,dt + "
                      r"\sigma_j L_j\,dW^{\,N}", font_size=32, colors={r"dL_j": FWD}),
                cmath(r"\text{caplet}_i", r"=", r"P(0, T_N)\,\mathbb{E}^{N}\Big[\frac{\delta(L_i(T_i) - K)^+}{P(T_{i+1}, "
                      r"T_N)}\Big]", font_size=32, colors={r"\text{caplet}_i": WHITE})]
        whys = [why(r"the forward rates themselves are the state: one for each accrual period of a cap or a swap"),
                why(r"Brace, Gatarek and Musiela; Jamshidian; Miltersen, Sandmann and Sondermann (1997): under the measure "
                    r"that pays at $T_{i+1}$ each forward is a martingale, so every caplet is exactly Black's formula"),
                why(r"to simulate them all together, pick one measure (here the last payment date); the others then pick "
                    r"up drifts from the change of numeraire"),
                why(r"and price by Monte Carlo under that one measure: the check that the drifts are right")]
        step = ladder(self, rows, whys, keep=4, top=3.35, x=-1.2, buff=0.34, edge=6.9)
        with self.voiceover(
            "Short-rate models price caplets with their own formulas, which never quite match the market's Black "
            "quotes. In 1997 three groups of authors turned it around: take the market's forward rates themselves as "
            "the model's state, one for each period. <bookmark mark='a'/> Under the measure that pays at the end of "
            "its own period, each forward has no drift, so if it is lognormal, each caplet is exactly Black's formula. "
            "The market's quotes and the model agree by construction. <bookmark mark='b'/> To simulate all of them "
            "together you need one measure; under it, each forward picks up a drift from the change of numeraire. "
            "<bookmark mark='c'/> Then any product on the whole strip, a swaption, a Bermudan, can be priced by "
            "simulation, and the caplets give the check."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def check(self, m):
        T = np.asarray(m["T"])
        b, n = m["black"], m["normal"]
        rb = np.asarray(b["mc"]) / np.asarray(b["exact"])
        rn = np.asarray(n["mc"]) / np.asarray(n["exact"])
        g = axes([0, 5.5], [0.95, 1.05], x_length=7.2, y_length=4.2, xlabel=r"caplet reset, years",
                 ylabel=r"Monte Carlo price / formula", xticks=[1, 2, 3, 4, 5], yticks=[0.96, 1.0, 1.04], font_size=14
                 ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        one = Line(ax.c2p(0, 1), ax.c2p(5.5, 1), color=WHITE, stroke_width=2)
        db = VGroup(*[Dot(ax.c2p(t - 0.05, r), radius=0.07, color=LOGN) for t, r in zip(T, rb)])
        dn = VGroup(*[Dot(ax.c2p(t + 0.05, r), radius=0.07, color=NORMAL) for t, r in zip(T, rn)])
        side = VGroup(
            legend([(LOGN, r"lognormal forwards, 25\% vol: vs Black"), (NORMAL, r"normal forwards, 90 bp: vs Bachelier")],
                   font_size=17),
            MathTex(rf"\max |\text{{MC}}/\text{{formula}} - 1| = {100 * max(np.abs(rb - 1).max(), np.abs(rn - 1).max()):.1f}\%",
                    font_size=26),
            wrapped_label(r"ten semiannual forwards off the Fed's curve of 31 December 2025, simulated together under "
                          r"the terminal measure; 40{,}000 paths, one factor; resets 0.5--5y, payments 1--5.5y", 4.2, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"This separately named example fixes the reset and payment dates consistently: ten semiannual rates reset from half a year through five years and pay half a year later. Initial forwards come from the matching discount-factor ratios. The original demonstration's time origins are not used. <bookmark mark='a'/> With forty thousand paths, the largest relative deviation from the closed-form caplet prices is {100 * max(np.abs(rb - 1).max(), np.abs(rn - 1).max()):.1f} percent. The saved example also records a standard error for each price; these deviations are within about one and a half standard errors. We weight each payoff by its payment-date to terminal-bond ratio at its own reset. The terminal-measure drift shown assumes one shared Brownian factor; with multiple factors its pairwise products include correlations. Finite Euler steps retain discretization error, so Monte Carlo agreement is a diagnostic rather than proof of an exact simulation."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in db], lag_ratio=0.1), LaggedStart(*[FadeIn(d) for d in dn],
                                                                                       lag_ratio=0.1), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def corr(self, c):
        be, nv = np.asarray(c["beta"]), np.asarray(c["nvol"]) * 1e4
        rows = [cmath(r"\rho_{ij}", r"=", r"e^{-\beta |T_i - T_j|}", font_size=38, colors={r"\rho_{ij}": FWD}),
                cmath(r"\sigma_{N,\text{swaption}}^2", r"\approx", r"\textstyle\sum_{i,j} w_i w_j\,\rho_{ij}\,\sigma_i\sigma_j,"
                      r"\quad w_i = \frac{\delta P(0, T_{i+1})}{A(0)}", font_size=32,
                      colors={r"\sigma_{N,\text{swaption}}^2": NORMAL})]
        g = axes([0, 1.05], [40, 100], x_length=6.0, y_length=3.6, xlabel=r"decorrelation $\beta$",
                 ylabel=r"5y$\times$5y swaption vol, bp", xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[50, 70, 90],
                 font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 1.0)
        ax = g.ax
        cap = DashedLine(ax.c2p(0, 100 * c["caplet"] * 100), ax.c2p(1.05, 100 * c["caplet"] * 100), color=LOGN,
                         stroke_width=2)
        line = VGroup(curve(ax, be, nv, NORMAL, stroke_width=3.5, smooth=True),
                      *[Dot(ax.c2p(x_, y_), color=NORMAL, radius=0.06) for x_, y_ in zip(be, nv)])
        hdr = VGroup(rows[0], rows[1]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.45)
        side = VGroup(
            legend([(LOGN, rf"every caplet: {1e4 * c['caplet']:.0f} bp"), (NORMAL, r"the swaption on all ten")],
                   font_size=17),
            MathTex(rf"\beta = {c['check_beta']:g}:\ \text{{formula}}\ {1e4 * c['check_formula']:.1f},\ "
                    rf"\text{{simulated}}\ {1e4 * c['check_mc']:.1f}", font_size=22),
            wrapped_label(r"the caplets are identical in every case; only the correlation changes. Caps price the "
                          r"forwards one at a time, swaptions price them together: calibrating to both is how a desk "
                          r"learns $\beta$ (Rebonato's formula, frozen weights)", 4.0, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.7)
        fit_right(side)
        with self.voiceover(
            "One factor makes every forward move together. Real forwards decorrelate with distance: the six-month "
            "rate five years out and the one ten years out are related, not identical. <bookmark mark='a'/> A "
            "swaption is an option on a weighted average of forwards, so its volatility depends on their "
            "correlation. Keep every caplet at ninety basis points and let the correlation fall off. "
            f"<bookmark mark='b'/> The five-by-five swaption's volatility drops from {nv[0]:.0f} to {nv[-1]:.0f}: an "
            "average of loosely related rates moves less. Caplets cannot see this; swaptions can, which is why a "
            "desk calibrates its market model to both. The formula is checked against a simulation."
        ) as vo:
            self.play(FadeIn(hdr[0]), FadeIn(hdr[1]))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(cap), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def fmm(self):
        rows = [cmath(r"R_i(t)", r"=", r"\frac{1}{\delta}\Big(\mathbb{E}^{T_{i+1}}_t\Big[e^{\int_{T_i}^{T_{i+1}} r_s\,ds}"
                      r"\Big] - 1\Big)", font_size=38, colors={r"R_i(t)": FWD}),
                cmath(r"\sigma_i(t)", r"\to", r"0\ \text{linearly as } t \to T_{i+1}", font_size=38,
                      colors={r"\sigma_i(t)": FWD})]
        whys = [why(r"SOFR is compounded in arrears (Part 18): the rate for a period is known only at its end. "
                    r"Lyashenko and Mercurio (2019) extend each forward through its own accrual period"),
                why(r"inside the period the rate is partly fixed already, so its volatility decays to zero at the payment "
                    r"date: one model for both the old forward-looking rates and the new backward-looking ones")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            "An IBOR-style coupon normally fixes at the start of its accrual period. A compounded overnight coupon is known only at the end of its observation period, allowing for the contract's lookback, cutoff and payment lag. Lyashenko and Mercurio's forward market model extends a rate's evolution through that period. <bookmark mark='a'/> As more daily fixings become known, only the remaining uncertain portion contributes risk. A linear decay of the effective volatility is a useful specification in a simple model, not a universal theorem for every SOFR contract. Continued accrual-period uncertainty can add option time value under a matched model; it does not imply that every SOFR caplet is more valuable than every LIBOR caplet. The forward level, volatility, fixing and settlement conventions must also match."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"caplets fix each forward's volatility. Which market prices fix the correlations, and why does a "
                r"Bermudan care about them?")
        with self.voiceover("Caplets fix each forward's volatility. Which market prices fix the correlations, and why "
                            "does a Bermudan care?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
