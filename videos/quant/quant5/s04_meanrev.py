from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, real_data

DGS10_DEC2020 = 0.0093  # FRED DGS10, 31 December 2020


def vasicek_yield(r0, kappa, theta, sigma, tau):
    B = (1 - np.exp(-kappa * tau)) / kappa
    lnP = (theta - sigma ** 2 / (2 * kappa ** 2)) * (B - tau) - sigma ** 2 * B ** 2 / (4 * kappa) - B * r0
    return -lnP / tau


class MeanReversion(VoiceoverScene):
    def construct(self):
        r = load("rates")
        self.card()
        self.fit(r)
        self.feynman_kac(r)

    def card(self):
        c = chapter_card(3, r"Mean reversion and Feynman--Kac", r"What pulls an interest rate back?", part=PART)
        with self.voiceover("Chapter three. Mean reversion, and Feynman-Kac."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fit(self, r):
        t, x = np.asarray(r["t"]), np.asarray(r["r"])
        v, c = r["vasicek"], r["cir"]
        g = axes([1954, 2021], [-0.04, 0.18], x_length=6.6, y_length=4.4, ylabel=r"3-month Treasury bill rate",
                 xticks=[1960, 1980, 2000, 2020], xfmt=lambda u: f"{int(u)}", yticks=[-0.04, 0, 0.04, 0.08, 0.12, 0.16],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        real = curve(ax, t, x, BM, stroke_width=3)
        tt = t[0] + np.arange(np.asarray(r["ou_paths"]).shape[1]) / 12
        ou = VGroup(*[curve(ax, tt, np.clip(p, -0.04, 0.18), ITO, stroke_width=1.6).set_stroke(opacity=0.7)
                      for p in r["ou_paths"]])
        ci = VGroup(*[curve(ax, tt, np.clip(p, -0.04, 0.18), STRAT, stroke_width=1.6).set_stroke(opacity=0.7)
                      for p in r["cir_paths"]])
        zero = DashedLine(ax.c2p(1954, 0), ax.c2p(2021, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            MathTex(r"dr = \kappa(\theta - r)\,dt + \sigma\,dW", font_size=30, color=ITO),
            label(rf"Vasicek (1977): $\theta = {100 * v['theta']:.1f}\%$, half-life {v['half_life']:.0f} years", font_size=20,
                  color=ITO),
            label(rf"simulated rates below zero {100 * r['frac_neg_ou']:.0f}\% of the time", font_size=20, color=GREY_A),
            MathTex(r"dr = \kappa(\theta - r)\,dt + \sigma\sqrt{r}\,dW", font_size=30, color=STRAT),
            label(rf"CIR (1985): never negative; $2\kappa\theta/\sigma^2 = {c['feller']:.2f} < 1$, so it can touch zero",
                  font_size=20, color=STRAT),
            wrapped_label(r"fitted by regressing next month's rate on this month's (the exact discrete-time form of each "
                          r"model); sampled exactly, not by Euler", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        src = real_data(r"FRED DTB3, monthly averages, January 1954 -- December 2020")
        with self.voiceover(
            "Prices wander; interest rates are pulled back. Here is the three-month Treasury bill rate since 1954. "
            "<bookmark mark='a'/> The simplest model of a pull is Oldřich Vasicek's: the rate drifts toward a long-run "
            "level theta at a speed kappa, plus Brownian noise. It is the Ornstein-Uhlenbeck process of physics. "
            f"Fitted to these sixty-seven years, the long-run level is about {100 * v['theta']:.0f} percent, and a "
            f"deviation halves in about {v['half_life']:.0f} years. <bookmark mark='b'/> Simulate it, exactly, from "
            "the 1954 rate. The paths look plausible, but its noise doesn't care how low the rate is, and they spend "
            "about a tenth of the time below zero. <bookmark mark='c'/> Cox, Ingersoll and Ross made the noise shrink "
            "with the square root of the rate, so it can never go negative. Their condition for never touching zero "
            "fails on this data, and the paths kiss the floor, as American rates did in 2009 and 2020. Neither "
            "model produces the inflation of the 1970s; Part nineteen builds better ones."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(zero), Create(real), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(real.animate.set_stroke(opacity=0.35), LaggedStart(*[Create(p) for p in ou], lag_ratio=0.3,
                                                                         run_time=3), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeOut(ou), LaggedStart(*[Create(p) for p in ci], lag_ratio=0.3, run_time=3), FadeIn(side[3]),
                      FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def feynman_kac(self, r):
        v = r["vasicek"]
        th = theorem_card(r"Feynman--Kac", r"If $dX = a\,dt + b\,dW$, then $u(t, x) = \mathbb{E}\big[e^{-\int_t^T r\,ds} g(X_T) "
                          r"\mid X_t = x\big]$ solves $u_t + a\,u_x + \tfrac12 b^2 u_{xx} - r\,u = 0$, $u(T, x) = g(x)$.",
                          who=r"Feynman (1948), Kac (1949)", color=ITO, width=8.0, font_size=22).to_corner(UL, buff=0.4)
        bond = MathTex(r"P(t, T) = \mathbb{E}\Big[e^{-\int_t^T r_s\,ds}\Big] = e^{A(\tau) - B(\tau)\,r_t}", font_size=32)
        bond.next_to(th, DOWN, buff=0.35).align_to(th, LEFT)
        taus = np.linspace(0.25, 30, 120)
        r0 = float(np.asarray(r["r"])[-1])
        y = vasicek_yield(r0, v["kappa"], v["theta"], v["sigma"], taus)
        g = axes([0, 30], [0, 0.04], x_length=5.4, y_length=3.2, xlabel=r"maturity (years)", ylabel=r"yield",
                 xticks=[0, 10, 20, 30], yticks=[0, 0.01, 0.02, 0.03, 0.04], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_corner(DR, buff=0.6)
        ax = g.ax
        line = curve(ax, taus, y, ITO, stroke_width=3)
        dot = Dot(ax.c2p(10, DGS10_DEC2020), radius=0.08, color=JUMP)
        dl = label(r"actual 10-year, 31 Dec.\ 2020: 0.93\%", font_size=18, color=JUMP).next_to(dot, DOWN, buff=0.12)
        side = wrapped_label(rf"Vasicek's curve from the bill rate of December 2020 ({100 * r0:.2f}\%): the model expects "
                             rf"rates to return to their 1954--2020 average, the market did not", 5.6, 21, GREY_A)
        side.to_corner(DL, buff=0.6)
        with self.voiceover(
            "How do you price a bond under such a model? Feynman and Kac connected expectations over paths to "
            "partial differential equations: the expected discounted payoff, as a function of today's state, solves "
            "a PDE whose coefficients are the drift and half the squared volatility. <bookmark mark='a'/> For "
            "Vasicek the expectation can be done in closed form: a zero-coupon bond is an exponential, linear in "
            "today's rate. <bookmark mark='b'/> Start it from the bill rate of December 2020, under a tenth of a "
            "percent. The fitted model says the ten-year yield should be about one point four percent, and the "
            "thirty-year over two, because rates must return to their historical average. The actual ten-year yield "
            "was zero point nine three percent. The model is "
            "internally consistent and wrong about the world, and its parameters were estimated under the real "
            "measure when bond prices live under the pricing measure. Part nineteen calibrates to the curve instead."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Write(bond))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(line), FadeIn(side))
            self.play(FadeIn(dot), FadeIn(dl))
        self.wait(0.4)
        self.clear_scene()
