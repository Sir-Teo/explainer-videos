from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from explainer.quant.house import control as C
from explainer.quant.viz import price_surface
from videos.quant.quant8.common import ALT, KELLY, PART, UNDER, VALUE, illustration, load


class Bellman(VoiceoverScene, ThreeDScene):
    def construct(self):
        b = load("bellman")
        self.card()
        self.equations()
        self.surface(b)
        self.policy(b)

    def card(self):
        c = chapter_card(2, r"Dynamic programming and the HJB equation", r"How do you decide when tomorrow you decide "
                         r"again?", part=PART)
        with self.voiceover("Chapter two. Dynamic programming, and the Hamilton-Jacobi-Bellman equation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def equations(self):
        rows = [cmath(r"V_n(w)", r"=", r"\max_{\pi}\ \mathbb{E}\big[V_{n+1}(W_{n+1}) \mid W_n = w\big]", font_size=36,
                      colors={r"V_n(w)": VALUE}),
                cmath(r"0", r"=", r"V_t + \max_{\pi}\Big\{\big(r + \pi(\mu - r)\big) w V_w + \tfrac12 \pi^2\sigma^2 w^2 V_{ww}"
                      r"\Big\}", font_size=34),
                cmath(r"\pi^*", r"=", r"-\frac{(\mu - r)\,V_w}{\sigma^2\, w\, V_{ww}} \ \to\ \frac{\mu - r}{\gamma\sigma^2}",
                      font_size=36, colors={r"\pi^*": KELLY})]
        whys = [why(r"Bellman (1957): an optimal plan stays optimal from wherever it has led; so solve backwards, one "
                    r"step at a time"),
                why(r"shrink the step and expand with It\^o: the Hamilton--Jacobi--Bellman equation, a PDE with a "
                    r"maximum inside"),
                why(r"the maximum's first-order condition; with CRRA utility $-wV_{ww}/V_w = \gamma$: Merton's fraction "
                    r"(1969)")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.75, edge=6.9)
        visc = wrapped_label(r"the value function can have kinks (constraints, stopping), where $V_{ww}$ does not exist: "
                             r"Crandall and Lions's viscosity solutions (1983) give the equation a unique meaning, and "
                             r"guarantee that grid schemes like the one below converge (Barles and Souganidis 1991)",
                             12.0, 20, GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Most financial decisions are made again tomorrow, with whatever today's decision led to. Richard Bellman's "
            "principle of optimality, from 1957, says an optimal plan remains optimal from wherever it has led, so a "
            "problem over many periods can be solved backwards: the value today is the best expected value tomorrow. "
            "<bookmark mark='a'/> Let the step shrink and expand with Itô's formula, and the recursion becomes a "
            "partial differential equation with a maximum inside it: the Hamilton-Jacobi-Bellman equation. Here it is "
            "for an investor choosing the fraction pi of wealth to hold in a stock. <bookmark mark='b'/> The maximum "
            "is a parabola in pi, so the best fraction follows from its first-order condition. With constant relative "
            "risk aversion, the ratio of the derivatives is gamma, and the answer is Robert Merton's fraction from "
            "1969: the stock's excess return over gamma times its variance. <bookmark mark='c'/> One technical "
            "warning. Value functions can have kinks, where the second derivative doesn't exist. Michael Crandall and "
            "Pierre-Louis Lions's viscosity solutions give the equation a precise meaning there, and they are why "
            "numerical schemes like the one we are about to run converge to the right answer."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(visc))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, b):
        f = b["floor"]
        t, w = np.asarray(f["t"]), np.asarray(f["w"])
        P = np.asarray(f["pi"])
        interp = RegularGridInterpolator((t, w), P, bounds_error=False, fill_value=None)
        ax = ThreeDAxes(x_range=[0.65, 3.0, 0.5], y_range=[0, 10, 2], z_range=[0, 0.8, 0.2], x_length=7.6,
                        y_length=5.0, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6)
        surf = price_surface(ax, lambda x, y: float(interp([[y, x]])[0]), (0.65, 3.0), (0.0, float(t[-1])),
                             resolution=(40, 28), z_lo=0, z_hi=0.7)
        plane = Surface(lambda u, v: ax.c2p(u, v, b["pi_merton"]), u_range=[0.65, 3.0], v_range=[0, float(t[-1])],
                        resolution=(2, 2), fill_color=KELLY, fill_opacity=0.18, stroke_width=0.6, stroke_color=KELLY)
        hint = VGroup(label(r"wealth now", font_size=24, color=UNDER), label(r"years elapsed (of 10)", font_size=24,
                                                                           color=GREY_A),
                      label(r"the decision: fraction in stocks", font_size=24, color=VALUE),
                      label(rf"Merton without a floor: {100 * b['pi_merton']:.0f}\%", font_size=24, color=KELLY)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        params = note(rf"$\gamma = {b['gamma']:g}$, $\mu = {100 * b['mu']:.0f}\%$, $r = {100 * b['r']:.0f}\%$, "
                      rf"$\sigma = {100 * b['sigma']:.0f}\%$; a floor of 0.6 at year 10; Bellman on a grid, 120 monthly "
                      r"steps", font_size=19).to_corner(DR, buff=0.3)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-62 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(hint, params)
        self.remove(hint, params)
        with self.voiceover(
            "Here is that scheme, run. An investor with gamma three must end ten years with at least sixty cents of "
            "every starting dollar: a floor, as a pension fund might have. The House's solver steps backwards a month "
            "at a time from year ten, and at every level of wealth tries every fraction and keeps the best. "
            "<bookmark mark='a'/> The surface is its decision: the fraction in stocks, at every wealth and every year. "
            "Without the floor it would be the flat plane, Merton's answer everywhere. With it, the decision "
            "falls toward zero as wealth approaches the floor, and the fall steepens as the deadline nears."
        ) as vo:
            self.play(FadeIn(hint[:3]), FadeIn(params), Create(ax), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(surf), run_time=3)
            self.play(FadeIn(plane), FadeIn(hint[3]))
            self.move_camera(theta=-40 * DEGREES, phi=62 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, plane)), FadeOut(hint),
                                                                  FadeOut(params)], run_time=1.5)
        self.clear_scene()

    def policy(self, b):
        f = b["floor"]
        t, w = np.asarray(f["t"]), np.asarray(f["w"])
        P, Q = np.asarray(f["pi"]), np.asarray(f["pi_closed"])
        g = axes([0.6, 3.0], [0, 0.8], x_length=7.4, y_length=4.4, xlabel=r"wealth", ylabel=r"fraction in stocks",
                 xticks=[0.6, 1, 1.5, 2, 2.5, 3], yticks=[0, 0.2, 0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        merton = DashedLine(ax.c2p(0.6, b["pi_merton"]), ax.c2p(3.0, b["pi_merton"]), color=KELLY, stroke_width=3)
        ml = MathTex(rf"\text{{no floor: }}\pi^* = {100 * b['pi_merton']:.0f}\%", font_size=26, color=KELLY).next_to(
            ax.c2p(3.0, b["pi_merton"]), UP, buff=0.1).shift(LEFT * 1.3)
        cols = [UNDER, ALT, VALUE]
        picks = [0, len(t) // 2, len(t) - 1]
        dots, lines, labs = VGroup(), VGroup(), VGroup()
        for c_, k in zip(cols, picks):
            ok = w >= 0.62
            lines.add(curve(ax, w[ok], Q[k][ok], c_, stroke_width=3))
            dots.add(VGroup(*[Dot(ax.c2p(x, y), radius=0.04, color=WHITE) for x, y in zip(w[ok][::3], P[k][ok][::3])]))
            labs.add(label(rf"year {t[k]:.1f}", font_size=19, color=c_))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(g, RIGHT, buff=0.2).align_to(g, DOWN).shift(UP * 0.6)
        side = VGroup(
            MathTex(r"\pi^*(t, w) = \frac{\mu - r}{\gamma\sigma^2}\cdot\frac{w - F e^{-r(T - t)}}{w}", font_size=30),
            wrapped_label(r"lines: the closed form (portfolio insurance: Merton's fraction of the cushion above the "
                          r"floor's present value); dots: the grid solver", 4.2, 20, GREY_A),
            label(rf"largest gap: {np.nanmax(np.abs(P - Q)):.3f}", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.4)
        with self.voiceover(
            "Slice the surface at three dates. Without a floor the answer would be the same everywhere: Merton's "
            f"{100 * b['pi_merton']:.0f} percent, the dashed line. <bookmark mark='a'/> With "
            "the floor, the solver invests Merton's fraction of the cushion, the wealth above what the floor costs "
            "today. Near the floor it holds almost nothing in stocks; as wealth rises it approaches Merton; and as the "
            "years pass and the floor's present value rises, the curves shift. <bookmark mark='b'/> The lines are "
            "the closed-form answer, known as portfolio insurance; the dots are the grid solver, which knew nothing "
            f"of it. They differ by at most {np.nanmax(np.abs(P - Q)):.3f}."
        ) as vo:
            self.play(FadeIn(g), Create(merton), FadeIn(ml))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4), FadeIn(labs), FadeIn(side[0]),
                      run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.3), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
