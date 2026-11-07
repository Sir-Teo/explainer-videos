from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, axes, data_range, pause_card


class UVM(VoiceoverScene):
    def construct(self):
        u = load("uvm")
        self.card()
        self.model()
        self.film(load("uvm_film"))
        self.lab(u, load("uvm_book"))
        self.book(load("uvm_book"))

    def card(self):
        c = chapter_card(13, r"Uncertain volatility: the price of not knowing", r"What should you charge for not knowing "
                         r"the model?", lit=(1995,), part=PART)
        with self.voiceover("Chapter thirteen. Uncertain volatility: the price of not knowing."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [
            cmath(r"U(g)", r"=", r"\sup_{\sigma_t \in [\underline\sigma,\, \bar\sigma]} \mathbb E\big[e^{-rT} g(S_T)\big]",
                  font_size=36, colors={r"U(g)": BAD}),
            cmath(r"\partial_t V + \sup_{\sigma}\big\{\tfrac12\sigma^2 S^2 V_{SS}\big\} + rSV_S - rV", r"=", r"0",
                  font_size=34, colors={r"\partial_t V + \sup_{\sigma}\big\{\tfrac12\sigma^2 S^2 V_{SS}\big\} + rSV_S - rV": OPT}),
            cmath(r"\sigma(\Gamma)", r"=", r"\begin{cases}\bar\sigma & \Gamma > 0 \\ \underline\sigma & \Gamma < 0\end{cases}",
                  font_size=34, colors={r"\sigma(\Gamma)": IV}),
            cmath(r"U(g_1 + g_2)", r"\le", r"U(g_1) + U(g_2)", font_size=38, colors={r"U(g_1 + g_2)": GOOD}),
        ]
        whys = [why(r"the seller must hedge against every volatility path in the band, chosen against it "
                    r"(Avellaneda, Levy and Par\'as 1995; Lyons 1995)"),
                why(r"dynamic programming with $\sigma$ as the adversary's control: the Hamilton--Jacobi--Bellman "
                    r"equation of Part 8"),
                why(r"the bracket is linear in $\sigma^2$, so the sup sits at an end of the band: the top where the "
                    r"position is long gamma, the bottom where it is short (the Black--Scholes--Barenblatt equation)"),
                why(r"the sup of a sum is at most the sum of the sups; a common worst-case control suffices for equality; the statement does not require attained suprema "
                    r"in general. This valuation functional is subadditive")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Models fitted to the same vanillas disagree on exotics. What should a desk charge for that? In 1995 Marco "
            "Avellaneda, Arnon Levy and Antonio Parás, and independently Terry Lyons, answered with a worst case: "
            "volatility anywhere in a band, chosen against you. <bookmark mark='a'/> Dynamic programming turns that into a "
            "Hamilton–Jacobi–Bellman equation, Black–Scholes with a supremum inside. <bookmark mark='b'/> It is linear in "
            "sigma squared, so the worst case sits at an end of the band: the top where the position is long gamma, the "
            "bottom where it is short. That is the Black–Scholes–Barenblatt equation. <bookmark mark='c'/> And it is "
            "non-linear: a book's worst case is at most the sum of its parts'."
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

    def film(self, f):
        S = np.asarray(f["S"])
        V = np.asarray(f["V"])
        sig = np.asarray(f["sig"])
        tau = np.asarray(f["tau"])
        n = len(V)
        g = axes([60, 140], [0, 1.05], x_length=8.4, y_length=4.0, xlabel=r"spot", ylabel=r"seller's price",
                 xticks=[80, 95, 105, 120], yticks=[0, 0.5, 1.0], font_size=15).to_edge(UP, buff=0.6).to_edge(LEFT, buff=0.6)
        ax = g.ax
        k = ValueTracker(0)

        def cur():
            i = int(np.clip(round(k.get_value()), 0, n - 1))
            return curve(ax, S, V[i], OPT, stroke_width=3.5)

        def strip():
            i = int(np.clip(round(k.get_value()), 0, n - 1))
            y = ax.c2p(60, 0)[1] - 0.55
            w = ax.c2p(S[1], 0)[0] - ax.c2p(S[0], 0)[0]
            return VGroup(*[Rectangle(width=w * 1.02, height=0.35, stroke_width=0,
                                      fill_color=BAD if s_ > 0.25 else GOOD, fill_opacity=0.85)
                            .move_to([ax.c2p(x, 0)[0], y, 0]) for x, s_ in zip(S, sig[i])])
        line = always_redraw(cur)
        bar = always_redraw(strip)
        pay = curve(ax, S, V[0], GREY_B, stroke_width=2).set_stroke(opacity=0.6)
        ro = readout(r"\tau =", lambda: float(tau[int(np.clip(round(k.get_value()), 0, n - 1))]), digits=2,
                     unit=r"\ \text{years to expiry}", font_size=30, color=GREY_A)
        leg = VGroup(label(r"strip: the volatility the worst case picks at each spot", font_size=19, color=GREY_A),
                     legend([(BAD, r"$\bar\sigma = 35\%$ (long gamma)"), (GOOD, r"$\underline\sigma = 15\%$ (short gamma)")],
                            font_size=18)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(ro, leg).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        src = illustration(r"the House's BSB solver, call spread 95--105, six months, rates zero; every 10th of 400 steps")
        with self.voiceover(
            "Watch it solve. The payoff is a call spread, long the 95 call and short the 105, per unit of width. "
            "The solver starts at expiry and marches backward in time. <bookmark mark='a'/> Under the curve, a "
            "strip shows what the adversary chooses at every spot: red where the position is long gamma, so the "
            "worst case is the top of the band, green where it is short gamma, the bottom. <bookmark mark='b'/> As "
            "time runs back, the curve smooths, and the boundary between red and green, where gamma changes sign, "
            "drifts. No constant volatility can draw this price: it uses high volatility below the middle of the "
            "spread and low volatility above."
        ) as vo:
            self.play(FadeIn(g), FadeIn(pay), FadeIn(src), FadeIn(side))
            self.add(line, bar)
            vo.wait_until("a")
            self.play(k.animate.set_value(n * 0.2), run_time=2, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(n - 1), run_time=max(vo.remaining(0.5), 3.0), rate_func=linear)
        line.clear_updaters()
        bar.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lab(self, u, bk):
        card = lab_card(r"the Black--Scholes--Barenblatt step", [
            "for _ in range(n_t):                       # march back from expiry",
            "    g = np.zeros(n)                        # the discrete gamma",
            "    g[1:-1] = 2 * (h[:-1] * V[2:] - (h[:-1] + h[1:]) * V[1:-1]",
            "                   + h[1:] * V[:-2]) / (h[:-1] * h[1:] * (h[:-1] + h[1:]))",
            "    sig = np.where(g > 0, sig_hi, sig_lo) if upper \\",
            "        else np.where(g > 0, sig_lo, sig_hi)",
            "    a = 0.5 * sig ** 2 * S ** 2",
            "    # ... the implicit Black-Scholes step with this sigma",
            "    V = _thomas(lower, diag, upper_, rhs)",
        ], source="explainer/quant/house/exotics.py: uvm_price", width=8.6, font_size=16).to_corner(UL, buff=0.35)
        a = u["at100"]
        outs = [f"uvm_price(call spread 95-105, T=0.5, 15%-35%)",
                f"upper {a['upper']:.2f}   lower {a['lower']:.2f}   (Black-Scholes 25%: {a['bs25']:.2f})",
                f"hedged with 90 and 110 calls: [{bk['hedged_lower']:.2f}, {bk['hedged_upper']:.2f}]"]
        with self.voiceover(
            "In the House's code the whole idea is one line. At every step back in time, estimate the gamma on the "
            "grid, and pick the volatility from its sign: the top of the band where it is positive, the bottom "
            "where it is negative. Then take an ordinary implicit Black–Scholes step with that volatility. "
            "<bookmark mark='a'/> Run it: the upper price is "
            f"{a['upper']:.2f} and the lower {a['lower']:.2f}, around a Black–Scholes price of {a['bs25']:.2f} at "
            "twenty-five percent. The last line is a preview of what comes next."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, font_size=16)
        self.wait(0.4)
        self.clear_scene()

    def book(self, bk):
        its = bk["iterates"]
        steps = np.arange(len(its))
        best = np.minimum.accumulate([v for _, v in its])
        incumbent = [int(np.argmin([v for _, v in its[:k + 1]])) for k in range(len(its))]
        w1 = np.array([its[k][0][0] for k in incumbent])
        w2 = np.array([its[k][0][1] for k in incumbent])
        g = axes([0, len(its) - 1], [min(best) - 0.02, best[0] + 0.02], x_length=5.6, y_length=3.6,
                 xlabel=r"optimiser evaluations", ylabel=r"seller's worst-case price, hedged",
                 xticks=[0, len(its) - 1], yticks=[round(float(min(best)), 2), round(float(best[0]), 2)], font_size=14)
        g.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.8)
        ax = g.ax
        tr = ValueTracker(0)
        lb = tracing(ax, steps, best, tr, BAD, stroke_width=3)
        wro = VGroup(readout(r"\lambda_{90} =", lambda: float(np.interp(tr.get_value(), steps, w1)), digits=3,
                             font_size=28, color=GOOD),
                     readout(r"\lambda_{110} =", lambda: float(np.interp(tr.get_value(), steps, w2)), digits=3,
                             font_size=28, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        wro.next_to(g, UP, buff=0.3).align_to(g, LEFT)
        rows = VGroup(
            MathTex(r"U^{\lambda}(g) = \min_{\lambda}\Big\{U\big(g - \textstyle\sum_i \lambda_i C_i\big) + "
                    r"\textstyle\sum_i \lambda_i C_i^{\text{mkt}}\Big\}", font_size=30, color=OPT),
            wrapped_label(rf"non-additivity: priced leg by leg, the long 95 call and the short 105 call have worst cases "
                          rf"summing to {bk['legs_sum']:.3f}; as one book, {bk['upper']:.3f}. Netting gamma is worth "
                          rf"{bk['legs_sum'] - bk['upper']:.2f} per unit", 6.0, 19, WHITE),
            wrapped_label(rf"Avellaneda and Par\'as (1996): buy or sell 90 and 110 calls at their market prices "
                          rf"(Black--Scholes 25\%) and only the residual bears the worst case. The bounds tighten from "
                          rf"[{bk['lower']:.2f}, {bk['upper']:.2f}] to [{bk['hedged_lower']:.2f}, "
                          rf"{bk['hedged_upper']:.2f}]", 6.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.4)
        tight = bk["hedged_upper"] < bk["upper"] - 0.01
        verdict = (f"from {bk['upper']:.2f} to {bk['hedged_upper']:.2f}. The bounds tighten to "
                   f"{bk['hedged_lower']:.2f} and {bk['hedged_upper']:.2f}: market prices are information, and the "
                   "Lagrangian model uses them." if tight else
                   f"but only to {bk['hedged_upper']:.2f}: here the vanillas do little for this payoff.")
        pp = pause_card(r"Is the worst-case price of a book the sum of its parts?", width=5.6).to_corner(UR, buff=0.3)
        with self.voiceover(
            f"Is the worst-case price additive across legs? <bookmark mark='a'/> In this finite-grid example the separate call-spread legs sum to {bk['legs_sum']:.2f}, versus {bk['upper']:.2f} priced jointly. The supremum of a sum is at most the sum of suprema; a common worst-case control is sufficient for equality. <bookmark mark='b'/> Adding vanilla trades at the stated Black-Scholes 25-percent prices lets the desk optimize a residual payoff, following Avellaneda and Parás. The displayed optimizer keeps the best observed objective and its matching weights. It uses a finite evaluation budget and an approximate PDE solver; it does not certify the continuous global optimum or a numerical error bound. Market-price constraints can tighten the chosen model-class range without making it model-free."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(g), FadeIn(wro))
            self.add(lb)
            self.play(tr.animate.set_value(len(its) - 1), run_time=max(vo.remaining(1.0) - 1.0, 3.0), rate_func=linear)
            self.play(FadeIn(rows[2]))
        wro[0].num.clear_updaters()
        wro[1].num.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
