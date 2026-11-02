from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import CASH, DEL, GAM, IMP, OPT, PART, SPOT, THE, computed, load

C_ = {r"r": CASH, r"\sigma": IMP, r"V": OPT, r"u": OPT, r"\tau": THE, r"V_\tau": THE, r"u_\tau": THE,
      r"V_{xx}": GAM, r"u_{yy}": GAM, r"S": SPOT, r"K": QC.STRIKE}


def row(*parts, fs=34):
    return cmath(*parts, colors=C_, font_size=fs)


class Heat(VoiceoverScene, ThreeDScene):
    def construct(self):
        h = load("heat")
        self.card()
        self.melt(h)
        self.derive()
        self.lab(h)

    def card(self):
        c = chapter_card(3, r"Solving the equation: heat, run backwards", r"How does a kink become a price?",
                         lit=(1973,), part=PART)
        with self.voiceover("Chapter three. Solving the equation: heat, run backwards."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def melt(self, h):
        x = np.asarray(h["x"], float)
        tau = np.asarray(h["tau"], float)
        V = np.asarray(h["V"], float)
        K, sig, r = h["K"], h["sigma"], h["r"]
        x0, x1 = float(x[0]), float(x[-1])
        ax = ThreeDAxes(x_range=[x0, x1, 0.5], y_range=[0, 1, 0.25], z_range=[0, 100, 25], x_length=8.4,
                        y_length=5.0, z_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5)

        def ribs(upto):
            g = VGroup()
            for j, t in enumerate(tau):
                if t > upto + 1e-9:
                    break
                if j % 3 and j != len(tau) - 1:
                    continue
                col = WHITE if j == 0 else interpolate_color(ManimColor(OPT), ManimColor(GAM), t)
                g.add(VMobject(stroke_color=col, stroke_width=4 if j == 0 else 2.2).set_points_as_corners(
                    [ax.c2p(a, t, min(v, 100)) for a, v in zip(x, V[j])]))
            return g

        payoff = ribs(0.0)
        T = ValueTracker(0.0)
        grow = always_redraw(lambda: ribs(T.get_value())[1:])
        surf = price_surface(ax, lambda a, t: float(bs.price(np.exp(a), K, max(t, 1e-4), sig, r)), (x0, x1),
                             (0.0, 1.0), resolution=(30, 20), z_lo=0, z_hi=100, opacity=0.55)
        hint = VGroup(label(r"log of the stock price, $x = \ln S$", font_size=24, color=SPOT),
                      label(r"time left, $\tau = T - t$", font_size=24, color=THE),
                      label(r"the call's value $V$", font_size=24, color=OPT)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.1).to_corner(UR, buff=0.35)
        params = note(rf"$K = {K:.0f}$, $\sigma = {100 * sig:.0f}\%$, $r = {100 * r:.0f}\%$", font_size=20)
        params.to_corner(DR, buff=0.3)
        # the heat kernel at tau = 0.4, centred under one point, and the payoff it averages
        tk = 0.4
        sd = sig * np.sqrt(tk)
        c = ValueTracker(np.log(85.0))

        def kernel():
            y0 = c.get_value() + (r - 0.5 * sig ** 2) * tk
            zs = np.linspace(max(x0, y0 - 3.5 * sd), min(x1, y0 + 3.5 * sd), 60)
            phi = np.exp(-0.5 * ((zs - y0) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
            line = VMobject(stroke_color=QC.Q, stroke_width=3.5).set_points_as_corners(
                [ax.c2p(z, tk, 9 * p) for z, p in zip(zs, phi)])
            pay = np.maximum(np.exp(zs) - K, 0)
            prod = VMobject(stroke_width=0, fill_color=QC.Q, fill_opacity=0.35).set_points_as_corners(
                [ax.c2p(z, tk, 0) for z in zs] + [ax.c2p(z, tk, min(0.25 * p * w, 40)) for z, p, w in
                                                  zip(zs[::-1], phi[::-1], pay[::-1])] + [ax.c2p(zs[0], tk, 0)])
            v = float(bs.price(np.exp(c.get_value()), K, tk, sig, r))
            dot = Dot3D(ax.c2p(c.get_value(), tk, v), radius=0.08, color=YELLOW)
            return VGroup(line, prod, dot)

        kern = always_redraw(kernel)
        klab = label(r"violet: the heat kernel at $\tau = 0.4$; shaded: kernel $\times$ payoff", font_size=22,
                     color=QC.Q).to_edge(DOWN, buff=0.3).shift(LEFT * 1.5)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-55 * DEGREES, zoom=0.9)
        for m in (hint, params, klab):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        with self.voiceover(
            "Chapter two ended with an equation. Now we solve it, as Black and Scholes's published paper does: "
            "it is one of the oldest equations of mathematical physics in disguise. Lay the option's value over "
            "the log of the stock price and the time left to expiry. At expiry, the front edge, the value is the payoff: "
            "a hockey stick with a kink at the strike. <bookmark mark='a'/> Now let time run backwards. The "
            "equation lifts the curve out of the payoff and rounds off the kink, slice after slice, the way heat "
            "spreads along a cold rod with one hot end. <bookmark mark='b'/> And here is what the equation "
            "actually computes. At one time left, take this violet bell: the heat kernel, a normal density whose "
            "width grows like sigma times the square root of the time left. Multiply it by the payoff, shade the "
            "product, and add it up: that area, discounted, is the height of the surface above the bell's "
            "centre, the yellow dot. <bookmark mark='c'/> Slide the bell, and the dot rides the surface. Every "
            "point of the price is an average of the payoff, weighted by a Gaussian."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(params), Create(ax), Create(payoff), run_time=2)
            vo.wait_until("a")
            self.add(grow)
            self.play(T.animate.set_value(1.0), run_time=max(vo.until("b") - 1.5, 3.0), rate_func=linear)
            grow.clear_updaters()
            self.play(FadeIn(surf), run_time=1.0)
            self.move_camera(phi=66 * DEGREES, theta=-42 * DEGREES, run_time=1.5)
            self.add(kern)
            self.play(FadeIn(klab))
            vo.wait_until("c")
            self.play(c.animate.set_value(np.log(150.0)), run_time=max(vo.remaining(1.0) - 1.0, 3.0),
                      rate_func=smooth)
        kern.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, payoff, grow, surf, kern)),
                                                                  FadeOut(hint), FadeOut(params), FadeOut(klab)],
                         run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            row(r"V_\tau", r"=", r"\tfrac12", r"\sigma", r"^2", r"V_{xx}", r"+", r"(", r"r", r"-",
                r"\tfrac12\sigma^2", r")\,V_x", r"-", r"r", r"V"),
            row(r"u_\tau", r"=", r"\tfrac12", r"\sigma", r"^2", r"u_{yy}", fs=40),
            row(r"u(y, \tau)", r"=", r"\int \frac{1}{\sqrt{2\pi\sigma^2\tau}}\,e^{-(y - z)^2/2\sigma^2\tau}\,",
                r"(e^z - K)^+", r"\,dz"),
            row(r"u", r"=", r"e^{y + \sigma^2\tau/2}\,N(d_1)", r"-", r"K", r"N(d_2)"),
            row(r"V", r"=", r"S", r"N(d_1)", r"-", r"K", r"e^{-", r"r", r"\tau}", r"N(d_2)", fs=42),
        ]
        whys = [why(r"time left $\tau = T - t$ and $x = \ln S$: the chain rule"),
                why(r"$u = e^{r\tau}V$, $y = x + (r - \tfrac12\sigma^2)\tau$: the discount and the drift removed"),
                why(r"the heat kernel convolved with the payoff: the fundamental solution"),
                why(r"split at $z = \ln K$; complete the square in the $e^z$ term"),
                why(r"undo the substitutions: $e^{y + \sigma^2\tau/2} = S e^{r\tau}$")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.2, buff=0.55, edge=6.9)
        with self.voiceover(
            "In symbols. Measure time backwards from expiry and price in logs, and the chain rule turns the "
            "equation into this: the time derivative equals half sigma squared times the curvature, plus a drift "
            "term, minus the discount. <bookmark mark='a'/> Two more substitutions remove the last two: undo the "
            "discount, and shift the log price along with the drift. What is left is the heat equation, with "
            "sigma squared over two playing the part of the rod's conductivity. <bookmark mark='b'/> The heat "
            "equation's solution from a given starting profile is known since Fourier and Laplace: convolve the "
            "profile with a Gaussian whose variance is sigma squared tau. Our profile is the payoff. "
            "<bookmark mark='c'/> Split the integral at the strike, where the payoff switches on; each half is a "
            "Gaussian integral, and completing the square in the first gives the two Ns. <bookmark mark='d'/> "
            "Undo the substitutions and there is the formula. Notice that the equation only ever sees sigma "
            "squared times tau. So pause and predict: double the volatility, and how long does the kink take to "
            "melt? A quarter of the time."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(Create(SurroundingRectangle(rows[4], color=OPT, buff=0.16, corner_radius=0.1)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lab(self, h):
        card = lab_card(r"two roads to one number", [
            "def price(S, K, T, sigma, r=0.0, q=0.0, cp=1):",
            "    d1, d2 = d1_d2(S, K, T, sigma, r, q)",
            "    return cp * (S * exp(-q*T) * ndtr(cp * d1)",
            "                 - K * exp(-r*T) * ndtr(cp * d2))",
            "",
            "def heat_price(payoff, S, T, sigma, r=0.0, kinks=()):",
            "    y = log(S) + (r - sigma**2 / 2) * T",
            "    # Gauss-Legendre on the pieces between kinks:",
            "    #   e^{-rT} * sum w * kernel(z - y) * payoff(e^z)",
            "    return exp(-r*T) * integral",
        ], source="explainer/quant/house/bs.py (price, heat_price; abridged)", width=7.2).to_corner(UL, buff=0.4)
        pts = h["pts"]
        conv, form = np.asarray(h["conv"], float), np.asarray(h["formula"], float)
        tab = VGroup(label(r"convolution vs formula", font_size=22, color=GREY_B),
                     *[MathTex(rf"S = {S:.0f},\ \tau = {t:g}:\ {a:.10f}\ \text{{vs}}\ {b:.10f}", font_size=20,
                               color=GREY_A) for (S, t), a, b in list(zip(pts, conv, form))[::2]])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tab.scale_to_fit_width(min(tab.width, 5.2)).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        with self.voiceover(
            "The House has both roads. Its pricer evaluates the formula; its heat solver does the convolution "
            "itself, numerically, for any payoff, splitting the integral at the kinks. <bookmark mark='a'/> Run "
            f"them on a one-year at-the-money call at twenty percent volatility: {h['lab']['heat']:.4f} and "
            f"{h['lab']['formula']:.4f}. Across nine stock prices and maturities the two agree to "
            f"{int(-np.floor(np.log10(h['max_err']))) - 1} decimal places: the same number, by integration and by "
            "formula. And the convolution prices payoffs the formula was never written for, "
            "which is why the heat equation, not the formula, is the workhorse of Part sixteen."
            " The equation has a second reading: the price is an expectation. Next."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"heat_price(call, 100, 1, 0.2, 0.05, kinks=(100,))  ->  {h['lab']['heat']:.10f}",
                                 f"price(100, 100, 1, 0.2, 0.05)                      ->  {h['lab']['formula']:.10f}"])
            self.play(FadeIn(tab), FadeIn(computed()))
        self.wait(0.4)
        self.clear_scene()
