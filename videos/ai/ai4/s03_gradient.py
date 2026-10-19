from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, bowl, bowl_grad


class Gradient(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.surface()
        self.contours()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Many inputs: the gradient", r"Which way is downhill?", part=4)
        with self.voiceover("Chapter two. Many inputs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def surface(self):
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], z_range=[0, 4, 1], x_length=8, y_length=6, z_length=2.6,
                          axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False}).shift(DOWN * 0.9)
        surf = loss_surface(axes, bowl, [-4, 4], [-3, 3], resolution=(36, 28), z_lo=0.2, z_hi=4.2)
        p0 = np.array([-2.6, 1.6])
        ball = surface_ball(axes, bowl, *p0, color=WHITE, radius=0.12)
        sx = ParametricFunction(lambda t: axes.c2p(t, p0[1], bowl(t, p0[1])) + np.array([0, 0, 0.03]), t_range=[-4, 4],
                                color=C.TRUE_P, stroke_width=4)
        sy = ParametricFunction(lambda t: axes.c2p(p0[0], t, bowl(p0[0], t)) + np.array([0, 0, 0.03]), t_range=[-3, 3],
                                color=C.BITS, stroke_width=4)
        g = bowl_grad(*p0)
        base = axes.c2p(p0[0], p0[1], 0)
        garrow = Arrow3D(base, axes.c2p(p0[0] + 1.2 * g[0], p0[1] + 1.2 * g[1], 0), color=GRAD, thickness=0.03, resolution=8)
        colors = {r"\frac{\partial f}{\partial x}": C.TRUE_P, r"\frac{\partial f}{\partial y}": C.BITS, r"\nabla f": GRAD}
        f = cmath(r"\nabla f", "=", r"\Big(", r"\frac{\partial f}{\partial x}", ",", r"\frac{\partial f}{\partial y}",
                  r"\Big)", colors=colors, font_size=46).to_corner(UL, buff=0.5)
        f.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.12)
        px = label(r"$\partial f / \partial x$: \ the slope along $x$, with $y$ held still", font_size=26, color=C.TRUE_P)
        py = label(r"$\partial f / \partial y$: \ the slope along $y$", font_size=26, color=C.BITS)
        VGroup(px, py).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.45)
        tag = label(r"illustrative", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
        path, p = [], p0.copy()
        for _ in range(45):
            path.append(p.copy())
            p = p - 0.35 * bowl_grad(*p)
        trail = surface_path(axes, bowl, path, color=WHITE, lift=0.06, stroke_width=4)
        track = surface_path(axes, bowl, path, color=WHITE, lift=0.12)
        for m in (f, px, py, tag):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-58 * DEGREES, zoom=0.7)
        with self.voiceover(
            "A loss depends on many numbers at once. With two, it's a surface over a plane. <bookmark mark='a'/> "
            "Nudge one number while holding the other still, and you get a partial derivative: the slope along that "
            "axis. <bookmark mark='b'/> Collect them all into one vector, and you have the gradient. It points "
            "straight uphill, the steepest way there is. <bookmark mark='c'/> So step the other way, again and again, "
            "and you slide down into a valley. That's gradient descent, and it trains every model in this series."
        ) as vo:
            self.play(Create(axes), FadeIn(surf), FadeIn(tag), run_time=1.6)
            self.play(FadeIn(ball))
            vo.wait_until("a")
            self.play(Create(sx), FadeIn(px))
            self.play(Create(sy), FadeIn(py))
            vo.wait_until("b")
            self.play(FadeIn(f), Create(garrow))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(sx, sy, px, py, garrow)))
            self.play(MoveAlongPath(ball, track), Create(trail), run_time=4.0, rate_func=smooth)
            self.move_camera(theta=-30 * DEGREES, run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def contours(self):
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=8, y_length=6, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-2.4, -0.3, 0])
        cont = contour_lines(ax, bowl, (-4, 4), (-3, 3), np.linspace(0.4, 3.6, 13))
        p0 = np.array([1.6, -1.4])
        P = ax.c2p(*p0)
        g = bowl_grad(*p0)
        gn = g / np.linalg.norm(g)
        gar = Arrow(P, P + 1.4 * np.array([*gn, 0]), buff=0, color=GRAD, stroke_width=6)
        gl = MathTex(r"\nabla f", font_size=38, color=GRAD).next_to(gar.get_end(), UR, buff=0.05)
        ang = ValueTracker(math.atan2(gn[1], gn[0]))

        def u():
            return np.array([math.cos(ang.get_value()), math.sin(ang.get_value())])

        uar = always_redraw(lambda: Arrow(P, P + 1.4 * np.array([*u(), 0]), buff=0, color=WHITE, stroke_width=5))
        dv = DecimalNumber(float(g @ u()), num_decimal_places=2, font_size=40, include_sign=True)
        dv.add_updater(lambda m: m.set_value(float(g @ u())))
        read = VGroup(MathTex(r"\text{slope along } \mathbf{u} = \nabla f \cdot \mathbf{u} =", font_size=36), dv)
        read.arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.5)
        if read.width > 4.6:  # keep it clear of the contour map on the left, and of the frame's edge
            read.scale_to_fit_width(4.6)
        read.shift(RIGHT * (6.3 - read.get_right()[0]))
        notes = VGroup(label(r"largest along $\nabla f$", font_size=28, color=GRAD),
                       label(r"zero along the contour", font_size=28, color=GREY_A),
                       label(r"most negative against it: \ downhill", font_size=28, color=C.TRUE_P))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, -0.6, 0])
        with self.voiceover(
            "Seen from above, the surface becomes a map of contour lines, each at one height. <bookmark mark='a'/> "
            "The slope in any direction you choose is the dot product of the gradient with that direction, from part "
            "three. <bookmark mark='b'/> So it's largest straight along the gradient, <bookmark mark='c'/> zero along "
            "the contour line, where the height doesn't change, <bookmark mark='d'/> and most negative pointing "
            "against the gradient: downhill."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.1), run_time=2.0)
            self.play(GrowArrow(gar), FadeIn(gl))
            vo.wait_until("a")
            self.add(uar)
            self.play(FadeIn(read))
            vo.wait_until("b")
            self.play(ang.animate.set_value(ang.get_value() + 0.6), run_time=0.8)
            self.play(ang.animate.set_value(math.atan2(gn[1], gn[0])), run_time=0.8)
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(ang.animate.set_value(math.atan2(gn[1], gn[0]) + PI / 2), run_time=1.2)
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(ang.animate.set_value(math.atan2(gn[1], gn[0]) + PI), run_time=1.2)
            self.play(FadeIn(notes[2]))
        uar.clear_updaters()
        dv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

