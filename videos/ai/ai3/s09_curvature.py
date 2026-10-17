from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import GRAD, VALUE, load


class Curvature(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.hessian()
        self.valley()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Curvature", r"How does the slope itself change?", part=3)
        with self.voiceover("Chapter eight. Curvature."):
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
        eig1 = label(r"eigenvalues $0.24$ and $0.6$: \ a bowl", font_size=28, color=WHITE).to_corner(DL, buff=0.5)
        eig2 = label(r"eigenvalues $0.24$ and $-0.6$: \ a saddle", font_size=28, color=WHITE).to_corner(DL, buff=0.5)
        sad = label(r"in many dimensions, most flat spots are saddles", font_size=28, color=GRAD).to_corner(DR, buff=0.5)
        for m in (H, eig1, eig2, sad):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-50 * DEGREES, zoom=0.74)
        with self.voiceover(
            "The gradient says which way is downhill. It doesn't say how the slope itself is changing. "
            "<bookmark mark='a'/> That's the second derivative: curvature. With many inputs, it's a matrix of second "
            "derivatives, the Hessian. <bookmark mark='b'/> It's symmetric, so, from part two, it has perpendicular "
            "eigenvectors: the directions of pure curvature. Its eigenvalues say how sharply the surface bends along "
            "each. <bookmark mark='c'/> Both positive: a bowl. One negative: a saddle, downhill one way and uphill the "
            "other. In many dimensions, most of the flat spots a model passes are saddles, not valleys."
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
    def valley(self):
        v = load("valley")
        H = np.asarray(v["H"])
        assert np.allclose(np.diag(H), [1.0, 25.0])
        ax = Axes(x_range=[-5, 5, 1], y_range=[-1.2, 1.2, 0.5], x_length=11.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(DOWN * 0.5)

        def f(x, y):
            return 0.5 * (H[0, 0] * x * x + H[1, 1] * y * y)

        cont = contour_lines(ax, f, (-5, 5), (-1.2, 1.2), [0.25 * 2 ** k for k in range(8)], n=(200, 80))
        paths = {}
        for name, col in (("gd", WHITE), ("momentum", C.TRUE_P), ("newton", C.BITS)):
            pts = [ax.c2p(*q) for q in np.asarray(v[name])]
            paths[name] = VMobject(color=col, stroke_width=4).set_points_as_corners(pts)
        dots = {k: Dot(paths[k].get_start(), radius=0.08, color=paths[k].get_color()) for k in paths}
        lab = {"gd": label(rf"gradient descent: \ ${v['gd_steps_to_1pct']}$ steps to get within $1\%$", font_size=26),
               "momentum": label(r"with momentum (Part 9)", font_size=26, color=C.TRUE_P),
               "newton": label(r"Newton: \ $\Delta = -H^{-1} \nabla f$, \ one step", font_size=26, color=C.BITS)}
        VGroup(*lab.values()).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.45)
        curv = label(r"curvatures $1$ and $25$: \ a long, narrow valley", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.35)
        hinv = label(r"$H^{-1}$: \ undoes the curvature's stretching, \\ so every direction is equally steep", font_size=24,
                     color=C.BITS)
        opt = label(r"optimizer: \ the rule that turns \\ gradients into steps", font_size=24, color=GREY_A)
        side = VGroup(hinv, opt).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.45)
        with self.voiceover(
            "Curvature explains why plain gradient descent can be slow. <bookmark mark='a'/> In a long, narrow valley, "
            "bent twenty-five times more sharply across than along, the steepest way down points mostly at the "
            "opposite wall. So the steps zigzag from wall to wall, and crawl along the floor. <bookmark mark='b'/> "
            "Momentum, carrying some speed from step to step, does better. <bookmark mark='c'/> Newton's method uses "
            "the curvature itself to rescale the step: multiplying by H inverse undoes the curvature's stretching, "
            "so every direction is equally steep, and in a bowl like this it lands at the bottom in one jump. "
            "<bookmark mark='d'/> For a model with billions of numbers the full Hessian is far too big to use, but the "
            "problem it reveals shapes every modern optimizer, the rule that turns gradients into steps, in part "
            "nine."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.1), FadeIn(curv), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(dots["gd"]), FadeIn(lab["gd"]))
            self.play(Create(paths["gd"]), MoveAlongPath(dots["gd"], paths["gd"]), run_time=3.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(dots["momentum"]), FadeIn(lab["momentum"]))
            self.play(Create(paths["momentum"]), MoveAlongPath(dots["momentum"], paths["momentum"]), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(dots["newton"]), FadeIn(lab["newton"]))
            self.play(Create(paths["newton"]), MoveAlongPath(dots["newton"], paths["newton"]), run_time=1.0)
            self.play(FadeIn(hinv))
            vo.wait_until("d")
            self.play(FadeIn(opt))
        self.wait(0.3)
        self.clear_scene()
