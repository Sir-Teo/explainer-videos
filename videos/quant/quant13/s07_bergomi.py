from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, real_data


class Bergomi(VoiceoverScene):
    def construct(self):
        b = load("bergomi")
        self.card()
        self.curve_(b)
        self.model()

    def card(self):
        c = chapter_card(6, r"Forward variance as the state", r"What if the model's state were a whole curve?", part=PART)
        with self.voiceover("Chapter six. Forward variance as the state."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def curve_(self, b):
        e = np.asarray(b["edges"]) * 365
        fv = np.sqrt(np.asarray(b["market_fwd_var"]))
        g = axes([0, 300], [0.2, 0.7], x_length=7.2, y_length=4.0, xlabel=r"days ahead",
                 ylabel=r"forward volatility $\sqrt{\xi_0(T)}$", xticks=[0, 50, 100, 150, 200, 250, 300],
                 yticks=[0.3, 0.4, 0.5, 0.6], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        steps = VGroup(*[Line(ax.c2p(a, v), ax.c2p(c_, v), stroke_color=IV, stroke_width=4) for a, c_, v in
                         zip(e[:-1], e[1:], fv)])
        risers = VGroup(*[DashedLine(ax.c2p(e[i + 1], fv[i]), ax.c2p(e[i + 1], fv[i + 1]), stroke_color=IV,
                                     stroke_width=1.5, dash_length=0.05) for i in range(len(fv) - 1)])
        hT = np.asarray(b["heston_T"]) * 365
        hes = curve(ax, hT, np.sqrt(np.asarray(b["heston_fwd_var"])), MODEL_COL["Heston"], stroke_width=3)
        leg = legend([(IV, r"the Surface: from variance-swap strikes, expiry to expiry"),
                      (MODEL_COL["Heston"], r"Heston's: one exponential, $\theta + (v_0 - \theta)e^{-\kappa T}$")],
                     font_size=17).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        sat = int(np.argmin(fv))
        arrow = Arrow(ax.c2p(e[sat] + 60, fv[sat] - 0.04), ax.c2p((e[sat] + e[sat + 1]) / 2 + 1, fv[sat]), buff=0.05,
                      stroke_width=3, color=GREY_A, max_tip_length_to_length_ratio=0.15)
        sat_l = label(rf"Saturday 13 to Sunday 14 December: {100 * fv[sat]:.0f}\%", font_size=18, color=GREY_A).next_to(
            arrow.get_start(), RIGHT, buff=0.1)
        side = VGroup(
            MathTex(r"\xi_0(T) = \frac{d}{dT}\Big(T\,K_{\text{var}}(T)\Big)", font_size=32, color=IV),
            wrapped_label(r"the variance the market prices for each future instant, read from Part 12's variance swaps; "
                          r"between two expiries it is constant", 4.2, 19, GREY_A),
            wrapped_label(rf"bitcoin trades all weekend, yet Saturdays are calm: realized {100 * b['by_dow'][5]:.0f}\% "
                          rf"against {100 * np.mean(b['by_dow'][:5]):.0f}\% on weekdays (2024--2025, hourly); the "
                          r"market prices it in", 4.2, 19, GREY_A),
            wrapped_label(r"Heston's whole curve is pinned by three numbers; it cannot dip for a weekend, or rise for a "
                          r"known event", 4.2, 19, MODEL_COL["Heston"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        src = real_data(r"the Surface, 10 December 2025: SSVI, variance-swap strip at each expiry")
        with self.voiceover(
            "A variance swap's strike, times its maturity, is the total variance the market prices up to that date. "
            "Its slope is the forward variance: the variance priced for each future instant. Here it is for the "
            "Surface, constant between expiries. <bookmark mark='a'/> Notice the dip. The expiries on Saturday the "
            "thirteenth and Sunday the fourteenth of December bracket a single weekend day, priced at "
            f"{100 * fv[sat]:.0f} percent volatility, against fifty or so on either side. Bitcoin trades all weekend, "
            f"but over the last two years its Saturdays realized {100 * b['by_dow'][5]:.0f} percent volatility, against "
            f"{100 * np.mean(b['by_dow'][:5]):.0f} on weekdays, and the market prices that in. <bookmark mark='b'/> Now Heston's forward variance: "
            "a single exponential from today's variance to the long-run level. It cannot dip for a weekend, rise for "
            "a central bank meeting, or take any shape the market chooses."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), FadeIn(side[0]), FadeIn(side[1]),
                      LaggedStart(*[Create(s_) for s_ in steps], lag_ratio=0.15, run_time=2.5), FadeIn(risers))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(sat_l), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(hes), FadeIn(leg[1]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"\xi_t(T)", r"=", r"\mathbb{E}^Q_t\big[v_T\big]", font_size=38, colors={r"\xi_t(T)": IV}),
                cmath(r"\frac{d\xi_t(T)}{\xi_t(T)}", r"=", r"\omega\Big(\theta_1 e^{-k_1(T - t)}\,dW^1_t + "
                      r"\theta_2 e^{-k_2(T - t)}\,dW^2_t\Big)", font_size=36, colors={r"\frac{d\xi_t(T)}{\xi_t(T)}": VAR}),
                cmath(r"\frac{dS}{S}", r"=", r"\sqrt{\xi_t(t)}\,dW^S_t", font_size=38, colors={r"\frac{dS}{S}": SPOT})]
        whys = [why(r"each forward variance is a martingale under $Q$: it is a tradable variance swap's rate"),
                why(r"Bergomi (2005, 2016): let the whole curve move, driven by two factors, a fast one and a slow one, "
                    r"each decaying with distance to $T$; today's curve is an input, matched exactly"),
                why(r"the price moves with the instantaneous variance at the front of the curve; the vol of vol term "
                    r"structure, not today's smile, is what the model is designed to control")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.85, edge=6.9)
        with self.voiceover(
            "Lorenzo Bergomi turned this around. Make the whole forward variance curve the model's state, and take "
            "today's curve from the market as given, whatever its shape. <bookmark mark='a'/> Each point on the curve "
            "is the rate of a tradable variance swap, so under the pricing measure it is a martingale. Let the curve "
            "move, driven by two factors, one fast and one slow, each fading with the distance to its date. "
            "<bookmark mark='b'/> The price itself moves with the variance at the front of the curve. What the model "
            "controls is not today's smile but how volatile the future variances are, and how that volatility "
            "depends on horizon: exactly what forward-start options and cliquets are bets on. It is the variance "
            "curve version of Heston, and, with a fractional kernel instead of two exponentials, it becomes Part "
            "fourteen's rough Bergomi."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()
