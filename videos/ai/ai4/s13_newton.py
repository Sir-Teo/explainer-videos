from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HESS, HIST, PART, VALUE, load, log_axes

GDC, NEWC = WHITE, C.BITS


class Newton(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.hessian()
        self.derive()
        self.race()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"Curvature, and Newton's method", r"How does the slope itself change?", part=PART)
        with self.voiceover("Chapter twelve. Curvature."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hessian(self):
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2.5, 2.5, 1], x_length=6.5, y_length=6.5,
                          z_length=3.4, axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})

        def bowl(x, y):
            return 0.12 * x * x + 0.3 * y * y

        def saddle(x, y):
            return 0.12 * x * x - 0.3 * y * y

        s1 = loss_surface(axes, bowl, [-3, 3], [-3, 3], resolution=(28, 28), z_lo=-2.7, z_hi=2.7)
        s2 = loss_surface(axes, saddle, [-3, 3], [-3, 3], resolution=(28, 28), z_lo=-2.7, z_hi=2.7)
        ex = ParametricFunction(lambda t: axes.c2p(t, 0, bowl(t, 0)) + np.array([0, 0, 0.03]), t_range=[-3, 3],
                                color=VALUE, stroke_width=5)
        ey = ParametricFunction(lambda t: axes.c2p(0, t, bowl(0, t)) + np.array([0, 0, 0.03]), t_range=[-3, 3],
                                color=GRAD, stroke_width=5)
        ey2 = ParametricFunction(lambda t: axes.c2p(0, t, saddle(0, t)) + np.array([0, 0, 0.03]), t_range=[-3, 3],
                                 color=GRAD, stroke_width=5)
        H = MathTex(r"H = \begin{bmatrix} \partial^2 f/\partial x^2 & \partial^2 f/\partial x \partial y \\ "
                    r"\partial^2 f/\partial y \partial x & \partial^2 f/\partial y^2 \end{bmatrix}", font_size=34)
        H.to_corner(UL, buff=0.45)
        eig1 = label(r"$f = 0.12x^2 + 0.3y^2$: \ eigenvalues $0.24$ and $0.6$, \ a bowl", font_size=26).to_corner(DL, buff=0.5)
        eig2 = label(r"$f = 0.12x^2 - 0.3y^2$: \ eigenvalues $0.24$ and $-0.6$, \ a saddle", font_size=26).to_corner(DL, buff=0.5)
        sad = label(r"saddles: \ chapter 14", font_size=26, color=GRAD).to_corner(DR, buff=0.5)
        for m in (H, eig1, eig2, sad):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-50 * DEGREES, zoom=0.74)
        with self.voiceover(
            "The gradient says which way is downhill. It doesn't say how the slope itself is changing. "
            "<bookmark mark='a'/> That's the second derivative, curvature. With many inputs it's a matrix of second "
            "derivatives, the Hessian. <bookmark mark='b'/> It's symmetric, so, from part three, it has perpendicular "
            "eigenvectors, the directions of pure curvature, and its eigenvalues say how sharply the surface bends "
            "along each. <bookmark mark='c'/> Both positive: a bowl. One negative: a saddle, downhill one way and "
            "uphill the other, which chapter fourteen takes up."
        ) as vo:
            self.play(Create(axes), FadeIn(s1), run_time=1.5)
            self.begin_ambient_camera_rotation(rate=0.08)
            vo.wait_until("a")
            self.play(FadeIn(H))
            vo.wait_until("b")
            self.play(Create(ex), Create(ey), FadeIn(eig1))
            vo.wait_until("c")
            self.play(Transform(s1, s2), Transform(ey, ey2), FadeOut(eig1), FadeIn(eig2), run_time=2.0)
            self.play(FadeIn(sad))
        self.stop_ambient_camera_rotation()
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def derive(self):
        col = {r"\nabla f": GRAD, r"H": HESS, r"H^{-1}": HESS}
        rows = [
            cmath(r"f(x + \Delta)", r"\approx", r"f + \nabla f^\top \Delta + \tfrac12\, \Delta^\top H \Delta", font_size=40),
            cmath(r"0", r"=", r"\nabla f + H \Delta", font_size=40),
            cmath(r"\Delta", r"=", r"-H^{-1} \nabla f", font_size=44, colors={r"\Delta": NEWC}),
        ]
        whys = [why(r"Taylor to second order: \ the best quadratic"), why(r"its minimum: \ the gradient in $\Delta$ is zero"),
                why(r"if $H$ is positive definite: \ a minimum")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.2, buff=0.6, edge=6.9)
        hist = history_card(1669, r"Isaac Newton; \ Joseph Raphson (1690); \ Thomas Simpson (1740)",
                            r"roots of equations by repeated tangents; \ Simpson used it for several variables and "
                            r"for maxima and minima", width=8.0, font_size=19, color=HIST).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Hessian gives a better step. The first derivative made the best straight line; with the second, "
            "the best quadratic. <bookmark mark='a'/> Jump straight to that quadratic's minimum, where its gradient "
            "is zero: <bookmark mark='b'/> the step is minus H inverse times the gradient. That's Newton's method. "
            "<bookmark mark='c'/> Newton used the idea in 1669 for roots of equations, Raphson simplified it in 1690, "
            "and Thomas Simpson extended it in 1740 to several variables and to finding minima."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d = load("newton")
        X, y, lam = np.asarray(d["X"]), np.asarray(d["y"]), float(d["lam"])
        gd, nw = np.asarray(d["gd"]), np.asarray(d["newton"])
        f_star = float(d["f_star"])

        def f(w1, w2):
            return float(np.logaddexp(0, -y * (X @ np.array([w1, w2]))).mean() + lam / 2 * (w1 * w1 + w2 * w2))

        ax = Axes(x_range=[-0.3, 1.8, 0.5], y_range=[-0.9, 0.7, 0.5], x_length=6.2, y_length=4.7, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.4, -0.5, 0])
        levels = [f_star + 0.004 * 2 ** k for k in range(8)]
        cont = contour_lines(ax, f, (-0.3, 1.8), (-0.9, 0.7), levels, n=(90, 70))
        gpath = VMobject(color=GDC, stroke_width=2.5).set_points_as_corners([ax.c2p(*q) for q in gd[::3]])
        npath = VMobject(color=NEWC, stroke_width=4).set_points_as_corners([ax.c2p(*q) for q in nw[:5]])
        ndots = VGroup(*[Dot(ax.c2p(*q), radius=0.07, color=NEWC) for q in nw[:4]])
        star = Star(n=5, outer_radius=0.14, color=YELLOW, fill_opacity=1).move_to(ax.c2p(*d["w_star"]))
        axl = VGroup(MathTex(r"w_1", font_size=24, color=GREY_B).next_to(ax, DOWN, buff=0.1),
                     MathTex(r"w_2", font_size=24, color=GREY_B).next_to(ax, LEFT, buff=0.1))
        # the error against the step, on a log scale
        ge = np.asarray(d["gd_err"])
        stride = int(d["gd_err_stride"])
        ne = np.asarray(d["newton_err"])
        steps = int(d["gd_steps"])
        top = int(math.ceil(math.log10(steps)))
        g2 = log_axes((0, top), (-12, 0), x_length=5.0, y_length=3.6, xlabel=r"step $+1$",
                      ylabel=r"$f - f^*$", center=[3.9, -0.1, 0], ystep=3)
        a2 = g2.ax
        t_gd = np.arange(len(ge)) * stride + 1
        okg = ge > 1e-13
        c_gd = curve(a2, np.log10(t_gd[okg]), np.clip(np.log10(ge[okg]), -12, 0), GDC, 3)
        okn = ne > 1e-13
        c_nw = VGroup(curve(a2, np.log10(np.arange(len(ne))[okn] + 1), np.clip(np.log10(ne[okn]), -12, 0), NEWC, 3.5),
                      *[Dot(a2.c2p(math.log10(i + 1), max(math.log10(e), -12)), radius=0.06, color=NEWC)
                        for i, e in enumerate(ne) if e > 1e-13])
        digits = [int(math.floor(-math.log10(e))) for e in ne if e > 1e-13]
        nsteps = int(d["newton_steps"])
        info = VGroup(
            label(rf"logistic regression, \ two correlated features: \ curvatures ${d['kappa']:.0f}$ times apart",
                  font_size=22, color=GREY_A),
            label(rf"gradient descent \ (step $1/L$): \ ${steps:,}$ steps to $10^{{-10}}$".replace(",", "{,}"), font_size=22,
                  color=GDC),
            label(rf"Newton: \ ${nsteps}$ steps; \ correct digits ${', '.join(str(k) for k in digits)}$", font_size=22,
                  color=NEWC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(UP, buff=0.3)
        tag = note(r"computed").next_to(g2, DOWN, buff=0.1).align_to(g2, RIGHT)
        d1, d2, d3 = (int(math.floor(-math.log10(max(e, 1e-17)))) for e in ne[1:4])
        doubling = d2 >= 1.6 * d1 and d3 >= 1.6 * d2
        verdict = ("roughly doubling each step: quadratic convergence" if doubling else
                   "growing faster every step")
        with self.voiceover(
            "A test: logistic regression, a classifier Part 6 builds, with two features so correlated that the curvature "
            f"differs {d['kappa']:.0f}-fold between directions. <bookmark mark='a'/> Gradient descent, with the largest "
            f"step that is always safe, zigzags down the valley and needs {steps:,} steps to get within ten to the "
            f"minus ten of the minimum. <bookmark mark='b'/> Newton needs {nsteps}. <bookmark mark='c'/> Count its "
            f"correct digits after each step: {d1}, then {d2}, then {d3}, {verdict}. <bookmark mark='d'/> The catch is the Hessian itself: each step solves "
            "a linear system with it, and for a billion parameters it would have a billion squared entries. The next "
            "chapter uses curvature without ever building it."
        ) as vo:
            self.play(FadeIn(info[0]), Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.1), FadeIn(axl),
                      FadeIn(star), run_time=1.8)
            self.play(FadeIn(g2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(gpath), Create(c_gd), FadeIn(info[1]), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(npath), FadeIn(ndots), Create(c_nw), FadeIn(info[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(info[2], color=NEWC, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
