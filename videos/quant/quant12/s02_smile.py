from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import smile as SM
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


class Smile(VoiceoverScene):
    def construct(self):
        s = load("surface")
        t = load("termskew")
        self.card()
        self.shapes(s)
        self.distribution(t)
        self.derive()
        self.term(t)

    def card(self):
        c = chapter_card(1, r"The smile, read", r"What is the shape telling us?", lit=(1987,), part=PART)
        with self.voiceover("Chapter one. The smile, read."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def shapes(self, s):
        per = [p for p in s["per"] if p["n"] >= 10]
        pick = [per[1], per[len(per) // 2], per[-1]]
        g = axes([-0.5, 0.5], [0.3, 0.9], x_length=6.6, y_length=4.2, xlabel=r"log-moneyness $k = \ln K/F$",
                 ylabel=r"implied volatility", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0.4, 0.6, 0.8],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = [BAD, IV, LV]
        lines, dots, leg_items = VGroup(), VGroup(), []
        for p, c in zip(pick, cols):
            kk = np.linspace(-0.5, 0.5, 101)
            iv = SM.svi_iv(p["svi"], kk, p["T"])
            inr = (iv >= 0.3) & (iv <= 0.9)  # a smile is convex: the in-range part is one piece, so it ends at the frame
            lines.add(curve(ax, kk[inr], iv[inr], c, stroke_width=3))
            k, v = np.asarray(p["k"]), np.asarray(p["iv"])
            m = (np.abs(k) <= 0.5) & (v <= 0.9) & (v >= 0.3)
            dots.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=c) for a, b in zip(k[m], v[m])]))
            leg_items.append((c, rf"{p['expiry']}: {p['T'] * 365:.0f} days"))
        leg = legend(leg_items, font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"skew: puts dearer than calls the same distance away: crash insurance", 4.2, 20, BAD),
            wrapped_label(r"smile: both wings above the middle: fat tails (Part 1)", 4.2, 20, IV),
            wrapped_label(r"term structure: short expiries swing most; long ones are anchored", 4.2, 20, LV),
            wrapped_label(r"the natural coordinates: log-moneyness $k$ and total variance $w = \sigma^2 T$", 4.2, 20,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface, three of its expiries; dots: quotes; lines: SVI fits")
        with self.voiceover(
            "Here are three slices of the Surface: a short, a middle and a long expiry. Each dot is a quote. "
            "<bookmark mark='a'/> Each slice is a smile: both wings sit above the middle. And on this day the left "
            "wing is higher than the right: a skew, the premium paid for protection against a fall. "
            "<bookmark mark='b'/> The short expiry is the most curved; the long ones are flatter and anchored. "
            "Throughout this part we measure strikes by log-moneyness, k, the log of strike over forward, and we "
            "measure the smile by total implied variance, w: volatility squared times time. Those are the "
            "coordinates in which the theorems are simple."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), FadeIn(dots))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(side[0]), FadeIn(side[1]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def distribution(self, t):
        gc = t["gc"]
        ks, xs = np.asarray(gc["k"]), np.asarray(gc["x"])
        g1s, g2s = np.asarray(gc["g1"]), np.asarray(gc["g2"])
        IV1, D1 = np.asarray(gc["iv_g1"]), np.asarray(gc["dens_g1"])
        IV2, D2 = np.asarray(gc["iv_g2"]), np.asarray(gc["dens_g2"])
        BF1 = np.asarray(gc["bfw_g1"])
        gL = axes([-4, 4], [0, 0.55], x_length=5.4, y_length=3.4, xlabel=r"standardized log return",
                  ylabel=r"risk-neutral density", xticks=[-3, 0, 3], yticks=[0, 0.4], font_size=16)
        gR = axes([-0.3, 0.3], [0.25, 0.7], x_length=5.4, y_length=3.4, xlabel=r"log-moneyness (30 days)",
                  ylabel=r"implied volatility", xticks=[-0.2, 0, 0.2], yticks=[0.4, 0.5, 0.6],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        VGroup(gL, gR).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        a, b = gL.ax, gR.ax
        mode = ValueTracker(0.0)  # 0: skewness slider, 1: kurtosis slider
        s1 = ValueTracker(4.0)    # index into g1s (4 = zero)
        s2 = ValueTracker(0.0)    # index into g2s

        def interp(arr, x):
            i = int(np.clip(np.floor(x), 0, len(arr) - 2))
            f = x - i
            return (1 - f) * arr[i] + f * arr[i + 1]

        def cur():
            if mode.get_value() < 0.5:
                return interp(D1, s1.get_value()), interp(IV1, s1.get_value())
            return interp(D2, s2.get_value()), interp(IV2, s2.get_value())
        normal = curve(a, xs[np.abs(xs) <= 4], np.exp(-xs[np.abs(xs) <= 4] ** 2 / 2) / np.sqrt(2 * np.pi), GREY_C, stroke_width=2)
        flat = DashedLine(b.c2p(-0.3, 0.5), b.c2p(0.3, 0.5), color=GREY_C)
        dens = always_redraw(lambda: curve(a, xs[np.abs(xs) <= 4], cur()[0][np.abs(xs) <= 4], QC.Q, stroke_width=3))
        sm = always_redraw(lambda: curve(b, ks, cur()[1], IV, stroke_width=3))
        r1 = always_redraw(lambda: MathTex(
            rf"\gamma_1 = {interp(g1s, s1.get_value()):+.2f},\ \ \gamma_2 = "
            rf"{(interp(g2s, s2.get_value()) if mode.get_value() > 0.5 else 0.0):.2f}",
            font_size=30, color=QC.Q).next_to(gL, DOWN, buff=0.35))
        bfw = curve(b, ks, BF1[0], GREY_B, stroke_width=2)
        bfw_d = DashedVMobject(bfw, num_dashes=40)
        cap = wrapped_label(r"grey dashes: the first-order formula of Backus, Foresi and Wu (2004)", 5.4, 18, GREY_B
                            ).next_to(gR, DOWN, buff=0.35)
        src = note(r"a 30-day option at 50\% volatility, Gram--Charlier densities priced and inverted",
                                       font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            """Why this shape? Option prices are expectations under a risk-neutral law. Gaussian log returns give the flat Black--Scholes smile. <bookmark mark='a'/> Our illustrative density changes its log-return skew parameter: a negative setting lifts puts relative to calls; a positive setting does the reverse. <bookmark mark='b'/> A positive kurtosis parameter lifts both wings. The polynomial can become negative, so this illustration clips and renormalizes it, then shifts log returns to preserve the forward. The sliders therefore need not equal the resulting distribution's exact moments. <bookmark mark='c'/> The grey first-order formula is a local approximation, best near the money."""
        ) as vo:
            self.play(FadeIn(gL), FadeIn(gR), Create(normal), Create(flat), FadeIn(src))
            self.add(dens, sm, r1)
            vo.wait_until("a")
            self.play(s1.animate.set_value(0.0), run_time=3)
            self.play(s1.animate.set_value(8.0), run_time=3)
            self.play(s1.animate.set_value(4.0), run_time=1.5)
            vo.wait_until("b")
            mode.set_value(1.0)
            self.play(s2.animate.set_value(4.0), run_time=3.5)
            vo.wait_until("c")
            self.play(s2.animate.set_value(0.0), run_time=1)
            mode.set_value(0.0)
            self.play(s1.animate.set_value(0.0), run_time=1.5)
            self.play(Create(bfw_d), FadeIn(cap))
        self.wait(0.4)
        dens.clear_updaters()
        sm.clear_updaters()
        r1.clear_updaters()
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"q(x)", r"\approx", r"\phi(x)\Big[1 + \frac{\gamma_1}{6}He_3(x) + \frac{\gamma_2}{24}He_4(x)\Big]",
                      font_size=36, colors={r"q(x)": QC.Q}),
                cmath(r"\sigma_{\text{imp}}(d)", r"\approx", r"\sigma\Big[1 - \frac{\gamma_1}{6}\,d + \frac{\gamma_2}{24}"
                      r"(d^2 - 1)\Big],\quad d = \frac{-k}{\sigma\sqrt T}", font_size=34, colors={r"\sigma_{\text{imp}}(d)": IV}),
                cmath(r"\gamma_1 < 0", r"\Rightarrow", r"\text{puts } (d > 0) \text{ dearer: a skew};\quad \gamma_2 > 0 "
                      r"\Rightarrow \text{both wings up: a smile}", font_size=32),
                cmath(r"\sigma^2_{\text{fwd}}(T_1, T_2)", r"=", r"\frac{w(0, T_2) - w(0, T_1)}{T_2 - T_1} \;\ge\; 0",
                      font_size=36, colors={r"\sigma^2_{\text{fwd}}(T_1, T_2)": LV})]
        whys = [why("formal Gram--Charlier coefficients: skewness $\\gamma_1$, excess kurtosis $\\gamma_2$; clipping and renormalization alter the illustration's exact moments"),
                why(r"Backus, Foresi and Wu (2004): price options on the corrected density, invert Black--Scholes, keep "
                    r"first order"),
                why(r"read the signs off the formula: $d$ is large for low strikes"),
                why(r"along the expiries: the variance between two dates is the forward variance; Chapter 3 shows it "
                    r"must not be negative")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.6, edge=6.9)
        with self.voiceover(
            """As algebra: correct the standardized log-return Gaussian by Hermite polynomials. <bookmark mark='a'/> Pricing and inversion to first order gives Backus, Foresi and Wu's tilted line and curved correction. <bookmark mark='b'/> This is a local link between smile slope and log-return skewness, not a universal equality of their signs for arbitrary distributions. Chapter thirteen will show why near-money skew and full-distribution skewness can disagree. <bookmark mark='c'/> At fixed forward moneyness, total implied variance must be non-decreasing in maturity under the calendar-arbitrage assumptions. Its maturity increment defines forward implied variance, rather than a physical variance forecast."""
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

    def term(self, t):
        tt = np.asarray(t["t"])
        A = np.asarray(t["atm"])
        sk = np.asarray(t["skew"])
        t0, t1 = float(np.floor(tt.min())), 2026.0
        g = axes([t0, t1], [0, 1.8], x_length=8.0, y_length=3.0, ylabel=r"at-the-money implied volatility",
                 xticks=list(range(int(t0), 2027)), xfmt=lambda u: f"{u:.0f}", yticks=[0.4, 0.8, 1.2],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.7)
        ax = g.ax
        cols = [BAD, IV, OPT, LV]
        idx = [0, 2, 4, 5]
        ten = np.asarray(t["tenors"])
        lines = VGroup(*[curve(ax, tt, A[:, i], c, stroke_width=2) for i, c in zip(idx, cols)])
        leg = legend([(c, f"{ten[i]:.0f} days") for i, c in zip(idx, cols)], font_size=16).next_to(g, RIGHT, buff=0.3)
        g2 = axes([t0, t1], [-0.06, 0.17], x_length=8.0, y_length=1.8, ylabel=r"30-day skew: $\sigma(k=-0.1) - \sigma(k=0.1)$",
                  yticks=[-0.05, 0, 0.15], yfmt=lambda u: f"{100 * u:+.0f}", font_size=16).next_to(g, DOWN, buff=0.5).align_to(g, LEFT)
        bars = VGroup(*[Line(g2.ax.c2p(x, 0), g2.ax.c2p(x, float(y)),
                             color=QC.HOUSE if y < 0 else BAD, stroke_width=2) for x, y in zip(tt, sk)])
        m = np.asarray(t["mean_atm"])
        call = t["call_skew"]
        verdict = (r"call-skewed more often than not" if call > 0.5 else r"put-skewed more often than not")
        side = VGroup(
            wrapped_label(rf"mean ATM: {100 * m[0]:.0f}\% (7d), {100 * m[2]:.0f}\% (30d), {100 * m[5]:.0f}\% (180d)", width=3.8, font_size=19),
            wrapped_label(rf"7 days above 180 days in {100 * t['inv_7_180']:.0f}\% of weeks", width=3.8, font_size=19, color=BAD),
            wrapped_label(rf"gold: call skew, {100 * call:.0f}\% of {t['n']} weeks: {verdict}", width=3.8, font_size=19, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).set_y(-0.9)
        src = real_data(r"weekly surfaces from Deribit trades, April 2021 -- November 2025", corner=UR)
        n = t["n"]
        m7, m180, inv = 100 * m[0], 100 * m[5], 100 * t["inv_7_180"]
        cs = 100 * call
        with self.voiceover(
            f"Now the same two coordinates through time: {n} Wednesdays of Bitcoin surfaces since April 2021, each rebuilt from that morning's trades. On top, at-the-money volatility at four expiries. <bookmark mark='a'/> On average the term structure slopes up, from {m7:.0f} percent at a week to {m180:.0f} at six months. But in {inv:.0f} percent of weeks it inverts, and the short end jumps above the long: those are the weeks of crashes and squeezes, when fear is about now. <bookmark mark='b'/> Below, the thirty-day skew, red when puts are dearer, gold when calls are. Bitcoin's smile was call-skewed in {cs:.0f} percent of these weeks. The S&P 500 has usually been put-skewed since the 1987 crash; Bitcoin's buyers have often paid more for the upside than for the crash. Pause and predict: in our local log-return illustration, a positive skew parameter tilts the near-money smile which way? Toward the calls. A smile is a snapshot. Next: how the whole surface moves. These fixed-tenor levels come from fitted models, sometimes outside the observed expiry range; short-tenor extrapolation can be unstable."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=3),
                      FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(g2), LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.005, run_time=3), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
