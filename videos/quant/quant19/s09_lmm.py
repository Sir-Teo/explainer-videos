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
                      r"\sigma_j L_j\,dW^{\,N}", font_size=36, colors={r"dL_j": FWD}),
                cmath(r"\text{caplet}_i", r"=", r"P(0, T_N)\,\mathbb{E}^{N}\Big[\frac{\delta(L_i(T_i) - K)^+}{P(T_{i+1}, "
                      r"T_N)}\Big]", font_size=36, colors={r"\text{caplet}_i": WHITE})]
        whys = [why(r"the forward rates themselves are the state: one for each accrual period of a cap or a swap"),
                why(r"Brace, Gatarek and Musiela; Jamshidian; Miltersen, Sandmann and Sondermann (1997): under the measure "
                    r"that pays at $T_{i+1}$ each forward is a martingale, so every caplet is exactly Black's formula"),
                why(r"to simulate them all together, pick one measure (here the last payment date); the others then pick "
                    r"up drifts from the change of numeraire"),
                why(r"and price by Monte Carlo under that one measure: the check that the drifts are right")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.55, edge=6.9)
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
                          r"the terminal measure; 40{,}000 paths, one factor", 4.2, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Here is that check, for ten half-year forwards off today's curve, all simulated together under the last "
            "payment date's measure, once with lognormal forwards and once with normal ones. "
            "<bookmark mark='a'/> Each caplet's Monte Carlo price divided by its closed form: within "
            f"{100 * max(np.abs(rb - 1).max(), np.abs(rn - 1).max()):.1f} percent everywhere, the size of the simulation "
            "noise. Get one sign wrong in those drifts and the late caplets drift away from one."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in db], lag_ratio=0.1), LaggedStart(*[FadeIn(d) for d in dn],
                                                                                       lag_ratio=0.1), FadeIn(side[1]))
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
            "LIBOR was fixed at the start of each period. SOFR is compounded in arrears, and known only at the end. In "
            "2019 Andrei Lyashenko and Fabio Mercurio extended the market model to such rates: each forward lives on "
            "through its own accrual period. <bookmark mark='a'/> Inside the period, more of the rate is fixed every "
            "day, so its volatility shrinks linearly to zero at the payment date. One framework now covers the "
            "LIBOR contracts still on the books and the SOFR ones that replaced them."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"in a market model, why must the forward rates of different periods be correlated less than "
                r"perfectly to price a Bermudan swaption sensibly?")
        with self.voiceover("Why does a market model need the forwards of different periods to be less than perfectly "
                            "correlated, to price a Bermudan sensibly?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
