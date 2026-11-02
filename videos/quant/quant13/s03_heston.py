from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import stochvol as sv
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, pause, real_data

LAB_CF = [
    "def heston_cf(u, T, v0, kappa, theta, xi, rho):",
    "    u = np.asarray(u, complex)",
    "    iu = 1j * u",
    "    b = kappa - rho * xi * iu",
    "    d = np.sqrt(b * b + xi * xi * (iu + u * u))",
    "    g = (b - d) / (b + d)          # the little trap",
    "    e = np.exp(-d * T)             # decays: |g e| < 1",
    "    C = kappa * theta / xi ** 2 * ((b - d) * T",
    "        - 2.0 * np.log((1.0 - g * e) / (1.0 - g)))",
    "    D = (b - d) / xi ** 2 * (1.0 - e) / (1.0 - g * e)",
    "    return np.exp(C + D * v0)",
]


class Heston(VoiceoverScene, ThreeDScene):
    def construct(self):
        c = load("calibrate")
        t = load("trap")
        self.card()
        self.model()
        self.rivers(c)
        self.derive()
        self.helix(t)
        self.trap(t)
        self.lab(t)

    def card(self):
        c = chapter_card(3, r"Heston I: the characteristic function", r"Can a second river be priced in closed form?",
                         lit=(1993,), part=PART)
        with self.voiceover("Chapter three. Heston's model, and its characteristic function, derived."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\frac{dS}{S}", r"=", r"\sqrt{v_t}\,dW^1_t", font_size=36, colors={r"\frac{dS}{S}": SPOT}),
                cmath(r"dv_t", r"=", r"\kappa(\theta - v_t)\,dt + \xi\sqrt{v_t}\,dW^2_t,\quad dW^1 dW^2 = \rho\,dt",
                      font_size=36, colors={r"dv_t": VAR})]
        whys = [why(r"the price, driven by the square root of a variance $v$"),
                why(r"the variance is Part 5's CIR process: pulled toward $\theta$ at speed $\kappa$, shaken by the vol of "
                    r"vol $\xi$; $\rho$ ties the two rivers")]
        step = ladder(self, rows, whys, keep=2, top=2.0, x=-1.2, buff=0.9, edge=6.9)
        with self.voiceover(
            "Steven Heston's model, from 1993, is the simplest way to write the second river down so that it can be "
            "priced. The price moves with the square root of a variance. <bookmark mark='a'/> The variance is Part "
            "five's mean-reverting square-root process: pulled toward a long-run level theta at speed kappa, and "
            "shaken by its own volatility, xi. Rho correlates the two noises, and, as the last chapter proved, rho "
            "is what tilts the smile."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def rivers(self, c):
        x = c["fits"]["Heston"]["x"]
        n, days = 120, 120
        S, v = sv.heston_qe(1.0, *x, days / 365, n, 6, seed=31, return_v=True)
        t = np.arange(n + 1)
        g1 = axes([0, days], [0.6, 1.5], x_length=9.0, y_length=2.4, ylabel=r"price", xticks=[0, 30, 60, 90, 120],
                  yticks=[0.75, 1.0, 1.25], font_size=16).to_edge(UP, buff=0.6)
        g2 = axes([0, days], [0, 1.6], x_length=9.0, y_length=2.4, xlabel=r"days", ylabel=r"volatility $\sqrt{v}$",
                  xticks=[0, 30, 60, 90, 120], yticks=[0, 0.5, 1.0, 1.5], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=16).next_to(g1, DOWN, buff=0.35)
        VGroup(g1, g2).to_edge(LEFT, buff=0.6)
        cols = [SPOT, OPT, RV, IV, VAR, GREY_A]
        pS = VGroup(*[curve(g1.ax, t, np.clip(S[:, i], 0.6, 1.5), cols[i], stroke_width=2) for i in range(6)])
        pv = VGroup(*[curve(g2.ax, t, np.clip(np.sqrt(v[:, i]), 0, 1.6), cols[i], stroke_width=2) for i in range(6)])
        side = VGroup(
            wrapped_label(r"six paths of the Heston model fitted to the Surface: each price path (top) and its own "
                          r"volatility (bottom), in the same colour", 3.4, 19, GREY_A),
            wrapped_label(r"the volatility touches zero and leaps back: the fitted model breaks Feller's condition", 3.4,
                          19, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"simulated with Andersen's QE scheme, daily steps")
        with self.voiceover(
            "Here are the two rivers, simulated from the Heston model fitted to the Surface. Each colour is one "
            "world: its price on top, and its own volatility underneath. <bookmark mark='a'/> When a path's "
            "volatility spikes, its price swings harder, and, because rho is negative, the spikes tend to come with "
            "falls. Notice how violently the volatility moves, touching zero and leaping back. That is what it took "
            "to fit Bitcoin's smile."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(src), FadeIn(side[0]))
            self.play(LaggedStart(*[AnimationGroup(Create(a), Create(b)) for a, b in zip(pS, pv)], lag_ratio=0.25,
                                  run_time=5))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"f_\tau", r"=", r"\tfrac12 v\,(f_{xx} - f_x) + \rho\xi v\,f_{xv} + \tfrac12\xi^2 v\,f_{vv} + "
                      r"\kappa(\theta - v)\,f_v", font_size=32, colors={r"f_\tau": OPT}),
                cmath(r"f", r"=", r"\exp\big(C(\tau) + D(\tau)\,v + iu\,x\big)", font_size=34, colors={r"f": OPT}),
                cmath(r"D'", r"=", r"\tfrac12\xi^2 D^2 - (\kappa - \rho\xi iu)\,D - \tfrac12(u^2 + iu),\quad D(0) = 0",
                      font_size=32, colors={r"D'": VAR}),
                cmath(r"C'", r"=", r"\kappa\theta\,D,\quad C(0) = 0", font_size=34, colors={r"C'": VAR}),
                cmath(r"D", r"=", r"\frac{b - d}{\xi^2}\,\frac{1 - e^{-d\tau}}{1 - g\,e^{-d\tau}},\quad b = \kappa - "
                      r"\rho\xi iu,\ d = \sqrt{b^2 + \xi^2(u^2 + iu)},\ g = \frac{b - d}{b + d}", font_size=30,
                      colors={r"D": VAR}),
                cmath(r"C", r"=", r"\frac{\kappa\theta}{\xi^2}\Big[(b - d)\,\tau - 2\ln\frac{1 - g\,e^{-d\tau}}{1 - g}\Big]",
                      font_size=32, colors={r"C": VAR}),
                cmath(r"\varphi(u)", r"=", r"\mathbb{E}\big[e^{iu\ln S_T/F}\big] = e^{C(T) + D(T)\,v_0}", font_size=34,
                      colors={r"\varphi(u)": OPT})]
        whys = [why(r"$x = \ln S$, $\tau = T - t$: $f = \mathbb{E}[e^{iux_T} \mid x, v]$ is a martingale, so it solves the "
                    r"backward equation (Feynman--Kac, Part 5)", 20),
                why(r"guess: every coefficient of the equation is affine in $v$, so try an exponent affine in $v$ "
                    r"(Duffie, Pan and Singleton 2000: affine models)", 20),
                why(r"substitute and collect the terms proportional to $v$: a Riccati equation", 20),
                why(r"collect the terms without $v$", 20),
                why(r"the quadratic's roots are $(b \pm d)/\xi^2$: separate variables, partial fractions, and "
                    r"choose the root that makes $e^{-d\tau}$ decay", 20),
                why(r"integrate $D$ once; with this choice $|g\,e^{-d\tau}| < 1$ and the logarithm never crosses its "
                    r"branch cut (Kahl and J\"ackel 2005; Albrecher et al.\ 2007)", 20),
                why(r"prices then follow from one Fourier integral (COS here; derived in Part 16)", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.75, edge=6.9)
        with self.voiceover(
            "Now derive the characteristic function. Write x for the log price and tau for the time to expiry. The "
            "expected value of e to the i u x at expiry, given today's x and v, is a martingale, so by Feynman and Kac "
            "it solves the backward equation of the model: this one. <bookmark mark='a'/> Every coefficient in it "
            "is linear in v. So guess an answer whose exponent is linear in v: C of tau, plus D of tau times v, plus "
            "i u x. That guess is the whole idea of affine models, which Duffie, Pan and Singleton generalised in "
            "2000. <bookmark mark='b'/> Substitute it. Every derivative becomes multiplication, and the equation "
            "splits in two. The terms proportional to v give an ordinary differential equation for D with a square "
            "in it: a Riccati equation. <bookmark mark='c'/> The terms without v say that C grows at kappa theta "
            "times D. <bookmark mark='d'/> A Riccati equation with constant coefficients can be solved exactly. "
            "Its right-hand side is a quadratic in D with roots b plus or minus d, over xi squared. Separate "
            "variables, use partial fractions, and you get this, with g the ratio of the two roots. We choose the "
            "root so that e to the minus d tau decays. <bookmark mark='e'/> Integrate once for C. That choice, "
            "the so-called little trap, keeps the logarithm away from its branch cut, as we will see in a moment. "
            "<bookmark mark='f'/> Put them together and the characteristic function is exponential in today's "
            "variance. One Fourier integral then prices any vanilla in microseconds."
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
            vo.wait_until("e")
            step(5)
            vo.wait_until("f")
            step(6)
        self.wait(0.4)
        self.clear_scene()

    def helix(self, t):
        h30, h91 = t["helix"]["30"], t["helix"]["91"]
        ax = ThreeDAxes(x_range=[0, 16, 4], y_range=[-1, 1, 0.5], z_range=[-1, 1, 0.5], x_length=8.0, y_length=3.6,
                        z_length=3.6, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                                "stroke_width": 2})

        def hel(h, col, sw=4):
            pts = [ax.c2p(u, re, im) for u, re, im in zip(h["u"], h["re"], h["im"])]
            return VMobject(stroke_color=col, stroke_width=sw).set_points_smoothly(pts)

        c30, c91 = hel(h30, IV), hel(h91, VAR)
        hint = VGroup(label(r"$\varphi(u)$ of the fitted Heston, a curve in $(u,\ \mathrm{Re}\,\varphi,\ "
                            r"\mathrm{Im}\,\varphi)$", font_size=22, color=GREY_A),
                      legend([(IV, r"30 days"), (VAR, r"3 months")], font_size=20)).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.15).to_corner(UL, buff=0.4)
        txt = wrapped_label(r"it starts at 1 ($u = 0$), turns at the rate of the drift, and decays like the Gaussian part "
                            r"of the law: slow decay means fat tails", 5.0, 20, GREY_A).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(hint, txt)
        self.remove(hint, txt)
        with self.voiceover(
            "It is worth looking at the object we just derived. The characteristic function takes a frequency u to "
            "a complex number, so draw it as a curve in three dimensions: u along the axis, the real and imaginary "
            "parts across. <bookmark mark='a'/> At u equal zero it is one: probabilities sum to one. As u grows it "
            "spirals around the axis, turning at the rate set by the drift, and shrinks. How fast it shrinks is the "
            "Gaussian part of the distribution: a slow decay means fat tails. <bookmark mark='b'/> The three-month "
            "curve collapses much faster than the thirty-day one: more variance, a wider distribution, a narrower "
            "transform. Everything an option price needs is on this spiral."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.5)
            self.play(Create(c30), run_time=3)
            vo.wait_until("a")
            self.move_camera(theta=-20 * DEGREES, phi=75 * DEGREES, run_time=max(vo.until("b") - 0.5, 1.5))
            vo.wait_until("b")
            self.play(Create(c91), FadeIn(txt), run_time=2.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, c30, c91)), FadeOut(hint),
                                                                  FadeOut(txt)], run_time=1.5)
        self.clear_scene()

    def trap(self, t):
        w = t["winding"]
        u = np.asarray(w["u"])
        zo = np.asarray(w["orig_re"]) + 1j * np.asarray(w["orig_im"])
        zl = np.asarray(w["lt_re"]) + 1j * np.asarray(w["lt_im"])
        cu = float(w["cross_u"][0])
        # left: the original form's argument z(u), angle true and radius log-compressed
        R = 2.2
        rad = np.log1p(np.abs(zo)) / np.log1p(np.abs(zo).max()) * R
        P = rad * np.exp(1j * np.angle(zo))
        plane = NumberPlane(x_range=[-2.6, 2.6, 1], y_range=[-2.6, 2.6, 1], x_length=5.0, y_length=5.0,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.4},
                            axis_config={"stroke_color": GREY_C}).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        cut = Line(plane.c2p(-2.6, 0), plane.c2p(0, 0), color=BAD, stroke_width=6)
        cut_l = label(r"branch cut of $\ln$", font_size=18, color=BAD).next_to(plane.c2p(-1.9, 0), UP, buff=0.1)
        tr = ValueTracker(1)

        def path_o():
            j = max(int(tr.get_value()), 1)
            return VMobject(stroke_color=VAR, stroke_width=3).set_points_as_corners(
                [plane.c2p(p.real, p.imag) for p in P[:j + 1]])

        po = always_redraw(path_o)
        dot = always_redraw(lambda: Dot(plane.c2p(P[int(tr.get_value())].real, P[int(tr.get_value())].imag), radius=0.07,
                                        color=WHITE))
        ttl = label(r"$z(u) = (1 - g\,e^{+dT})/(1 - g)$: Heston's original form, $T = 1$", font_size=20,
                    color=VAR).next_to(plane, UP, buff=0.15)
        # right: the imaginary part of the principal log, both forms
        g2 = axes([0, 20], [-3.5, 3.5], x_length=5.6, y_length=3.4, xlabel=r"frequency $u$",
                  ylabel=r"$\mathrm{Im}\,\ln z$ (principal branch)", xticks=[0, 5, 10, 15, 20],
                  yticks=[-np.pi, 0, np.pi], yfmt=lambda v: "0" if abs(v) < 1e-9 else (r"\pi" if v > 0 else r"-\pi"),
                  font_size=15).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
        ao, al = np.angle(zo), np.angle(zl)
        jump = np.flatnonzero(np.abs(np.diff(ao)) > np.pi)
        lo_ = curve(g2.ax, u, np.where(np.isin(np.arange(len(u)), jump + 1), np.nan, ao), VAR, stroke_width=3)
        ll_ = curve(g2.ax, u, al, RV, stroke_width=3)
        leg = legend([(VAR, r"original: jumps by $2\pi$"), (RV, r"little trap: continuous")], font_size=17).next_to(
            g2, DOWN, buff=0.25).align_to(g2, LEFT)
        fw = t["first_wrong"]
        p1 = t["prices"]["fit_1"]
        side = wrapped_label(
            rf"on our fit, the original form is wrong from $u = {fw['fit_1']['u']:.2f}$ at $T = 1$, where "
            rf"$|\varphi| = {fw['fit_1']['abs_phi']:.2f}$; from $u = {fw['fit_3']['u']:.2f}$ at $T = 3$; never at 3 "
            rf"months. A one-year at-the-money call: {100 * p1['iv_little'][1]:.1f}\% correct, "
            rf"{100 * p1['iv_original'][1]:.1f}\% from the original form", 5.6, 19, WHITE)
        side.next_to(leg, DOWN, buff=0.3).align_to(g2, LEFT)
        with self.voiceover(
            "Now the trap. Heston's original paper wrote the same solution with the other root: g upside down, and "
            "e to the plus d T. Algebraically identical. Numerically, not. Follow the number inside its logarithm, "
            "z of u, on our fitted model at one year, as the frequency rises. <bookmark mark='a'/> It grows "
            "exponentially, so the radius here is compressed, but its angle is true. It swings around the origin, "
            f"and at u equal to {cu:.2f} it crosses the negative real axis: the branch cut of the logarithm. "
            "<bookmark mark='b'/> The computer's logarithm jumps there by two pi i, and the characteristic function "
            "jumps with it. On the right, the imaginary part of the logarithm: the original form leaps, the little "
            "trap form of Albrecher and his co-authors stays continuous. <bookmark mark='c'/> And it is not an "
            "academic point. On our own fit the original form is wrong from u of "
            f"{fw['fit_1']['u']:.2f} at one year, where the function still has size {fw['fit_1']['abs_phi']:.2f}. A "
            f"one-year at-the-money call comes out at {100 * p1['iv_original'][1]:.0f} percent implied volatility "
            f"instead of {100 * p1['iv_little'][1]:.0f}. With gentle textbook parameters it holds to a year and fails "
            "at three. Our violent Bitcoin fit breaks it sooner."
        ) as vo:
            self.play(FadeIn(plane), FadeIn(ttl), Create(cut), FadeIn(cut_l))
            self.add(po, dot)
            j_cross = int(np.argmin(np.abs(u - cu)))
            self.play(tr.animate.set_value(j_cross), run_time=vo.until("a") + 2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(Flash(dot, color=BAD, flash_radius=0.3), FadeIn(g2), Create(lo_), FadeIn(leg[0]), run_time=1.5)
            self.play(tr.animate.set_value(len(u) - 1), Create(ll_), FadeIn(leg[1]), run_time=3, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side))
        po.clear_updaters()
        dot.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def lab(self, t):
        card = lab_card(r"Heston's characteristic function", LAB_CF, source="explainer/quant/house/stochvol.py",
                        width=7.4).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.5)
        fw = t["first_wrong"]
        b = t["benchmark"]
        outs = [f"cos_price(Fang-Oosterlee Table 4): {b['cos']:.9f}",
                f"published 5.785155435, error {b['err']:.1e}",
                f"original form, our fit, T=1: wrong from u = {fw['fit_1']['u']:.2f}",
                f"original form, our fit, T=3: wrong from u = {fw['fit_3']['u']:.2f}"]
        pp = pause(r"Is $\ln S_T$ normal given the variance path?", width=4.4).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here is the House's implementation, all of it: eleven lines. The two lines that matter are g, the ratio "
            "of roots chosen the right way up, and e, which decays. <bookmark mark='a'/> Run it. Through the COS "
            "method it reproduces Fang and Oosterlee's published benchmark price, five point seven eight five one "
            f"five, to {-np.floor(np.log10(b['err'])):.0f} decimal places. And the check against the original form finds exactly where that one "
            "breaks on our fit. <bookmark mark='b'/> A last question before we fit it. Is the log price normal "
            "given the variance path? Only when rho is zero: that was chapter two's conditioning argument."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pp))
        self.wait(0.6)
        self.clear_scene()
