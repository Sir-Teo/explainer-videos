from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import BOWL_P0, GRAD, HIST, PART, bowl, bowl_grad, load


class Gradient(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.surface()
        self.steepest()
        self.contours()
        self.cauchy()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Many inputs: the gradient", r"Which way is downhill, and why that way?", part=PART)
        with self.voiceover("Chapter two. Many inputs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def surface(self):
        d = load("linapprox")
        assert abs(d["pslope"] - 2) < 0.05
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], z_range=[0, 4, 1], x_length=8, y_length=6, z_length=2.6,
                          axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False}).shift(DOWN * 0.9)
        surf = loss_surface(axes, bowl, [-4, 4], [-3, 3], resolution=(36, 28), z_lo=0.2, z_hi=4.2)
        # Keep the illustrated plane at the point used by the measured errors
        # and the directional-derivative sweep, so their captions describe it.
        p0 = np.array(BOWL_P0)
        ball = surface_ball(axes, bowl, *p0, color=WHITE, radius=0.12)
        sx = ParametricFunction(lambda t: axes.c2p(t, p0[1], bowl(t, p0[1])) + np.array([0, 0, 0.03]), t_range=[-4, 4],
                                color=C.TRUE_P, stroke_width=4)
        sy = ParametricFunction(lambda t: axes.c2p(p0[0], t, bowl(p0[0], t)) + np.array([0, 0, 0.03]), t_range=[-3, 3],
                                color=C.BITS, stroke_width=4)
        g = bowl_grad(*p0)
        f0 = bowl(*p0)
        plane = Surface(lambda u, v: axes.c2p(p0[0] + u, p0[1] + v, f0 + g[0] * u + g[1] * v) + np.array([0, 0, 0.06]),
                        u_range=[-1.4, 1.4], v_range=[-1.3, 1.3], resolution=(8, 8), fill_color=WHITE, fill_opacity=0.75,
                        stroke_color=GRAD, stroke_width=1.5, checkerboard_colors=False)
        plane.set_fill(WHITE, opacity=0.75)
        base = axes.c2p(p0[0], p0[1], 0)
        garrow = Arrow3D(base, axes.c2p(p0[0] + 1.2 * g[0], p0[1] + 1.2 * g[1], 0), color=GRAD, thickness=0.03, resolution=8)
        colors = {r"\frac{\partial f}{\partial x}": C.TRUE_P, r"\frac{\partial f}{\partial y}": C.BITS, r"\nabla f": GRAD}
        f = cmath(r"\nabla f", "=", r"\Big(", r"\frac{\partial f}{\partial x}", ",", r"\frac{\partial f}{\partial y}",
                  r"\Big)", colors=colors, font_size=46).to_corner(UL, buff=0.5)
        f.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.12)
        px = label(r"$\partial f / \partial x$: \ the slope along $x$, with $y$ held still", font_size=26, color=C.TRUE_P)
        py = label(r"$\partial f / \partial y$: \ the slope along $y$", font_size=26, color=C.BITS)
        VGroup(px, py).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.45)
        tp = label(rf"the tangent plane: \ its error falls like $r^2$ \\ (measured slope ${d['pslope']:.2f}$ on log axes)",
                   font_size=24, color=GRAD).to_corner(UR, buff=0.4)
        tp.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        tag = label(r"illustrative surface", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
        path, p = [], p0.copy()
        for _ in range(45):
            path.append(p.copy())
            p = p - 0.35 * bowl_grad(*p)
        trail = surface_path(axes, bowl, path, color=WHITE, lift=0.06, stroke_width=4)
        track = surface_path(axes, bowl, path, color=WHITE, lift=0.12)
        for m in (f, px, py, tag, tp):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-58 * DEGREES, zoom=0.7)
        with self.voiceover(
            "A loss depends on many numbers at once. With two, it's a surface over a plane. <bookmark mark='a'/> "
            "Nudge one number while holding the other still, and you get a partial derivative: the slope along that "
            "axis. <bookmark mark='b'/> The best flat approximation to a surface near a point is a plane, the "
            "tangent plane, tilted by those two slopes; its error falls like the square of the distance, just as "
            f"the line's did: measured, a slope of {d['pslope']:.2f}. <bookmark mark='c'/> Collect the slopes into "
            "one vector, and you have the gradient. It points uphill, and, as we'll prove, the steepest way there "
            "is. <bookmark mark='d'/> So step the other way, again and again, and you slide down into a valley."
        ) as vo:
            self.play(Create(axes), FadeIn(surf), FadeIn(tag), run_time=1.6)
            self.play(FadeIn(ball))
            vo.wait_until("a")
            self.play(Create(sx), FadeIn(px))
            self.play(Create(sy), FadeIn(py))
            vo.wait_until("b")
            self.play(FadeIn(plane), FadeIn(tp))
            vo.wait_until("c")
            self.play(FadeOut(plane), FadeIn(f), Create(garrow))
            vo.wait_until("d")
            self.play(FadeOut(VGroup(sx, sy, px, py, garrow, tp)))
            self.play(MoveAlongPath(ball, track), Create(trail), run_time=4.0, rate_func=smooth)
            self.move_camera(theta=-30 * DEGREES, run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def steepest(self):
        col = {r"\nabla f": GRAD, r"\mathbf{u}": WHITE}
        rows = [
            cmath(r"D_{\mathbf u} f", r"=", r"\lim_{t \to 0} \frac{f(x + t\mathbf{u}) - f(x)}{t}", font_size=38),
            cmath(r"D_{\mathbf u} f", r"=", r"\nabla f \cdot \mathbf{u}", font_size=40, colors=col),
            cmath(r"|D_{\mathbf u} f|", r"\le", r"\|\nabla f\|\,\|\mathbf u\| = \|\nabla f\|", font_size=40),
            cmath(r"D_{\mathbf u} f = \|\nabla f\|", r"\iff", r"\mathbf u = \nabla f / \|\nabla f\|", font_size=40),
        ]
        whys = [why(r"the slope along a unit direction $\mathbf u$"),
                why(r"the tangent plane: \ $f(x + t\mathbf u) = f(x) + t\,\nabla f \cdot \mathbf u + o(t)$"),
                why(r"Cauchy--Schwarz (Part 3), \ $\|\mathbf u\| = 1$"),
                why(r"$\nabla f \ne 0$: \ equality in its positive direction")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.6, buff=0.55, edge=6.9)
        head = label(r"why the gradient is the steepest direction", font_size=30, color=GREY_A).to_edge(UP, buff=0.3)
        thm = theorem_card(r"steepest ascent",
                           r"If $f$ is differentiable and $\nabla f \ne 0$, \ of all unit directions, "
                           r"$\nabla f / \|\nabla f\|$ climbs fastest, "
                           r"at rate $\|\nabla f\|$; \ its opposite descends fastest. \ Perpendicular directions have "
                           r"zero first-order change.",
                           width=9.6, font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why steepest? At a differentiable point, pick any direction, a unit vector u, and ask for the slope that way. "
            "<bookmark mark='a'/> The tangent plane answers it: the slope along u is the gradient dotted with u. "
            "<bookmark mark='b'/> By the Cauchy–Schwarz inequality from Part 3, a dot product is at most the product "
            "of the lengths, and u has length one: no direction climbs faster than the length of the gradient. "
            "<bookmark mark='c'/> If the gradient is nonzero, the maximum occurs in its positive direction. "
            "<bookmark mark='d'/> So the "
            "gradient's own direction is the steepest way up, its opposite the steepest way down, and the directions "
            "at right angles give zero first-order change. If the gradient is zero, every directional derivative is zero."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contours(self):
        d = load("linapprox")
        off = abs((d["best_ang"] - d["g_ang"] + math.pi) % (2 * math.pi) - math.pi) * 180 / math.pi
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=8, y_length=6, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-2.4, -0.3, 0])
        cont = contour_lines(ax, bowl, (-4, 4), (-3, 3), np.linspace(0.4, 3.6, 13))
        p0 = np.array(BOWL_P0)
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
        # the measured slopes around the circle, as a small polar-free plot: slope against angle
        A = np.asarray(d["ang"])
        D = np.asarray(d["D"])
        pg = axes([-math.pi, math.pi, 1], [-1.0, 1.0, 0.5], x_length=4.4, y_length=2.2, xlabel=r"direction of $\mathbf u$",
                  ylabel=r"measured slope", yticks=[-0.8, 0, 0.8], font_size=18, center=[4.4, -1.2, 0])
        pc = curve(pg.ax, A, D, WHITE, 2.5)
        mark = DashedLine(pg.ax.c2p(d["g_ang"], -1.0), pg.ax.c2p(d["g_ang"], 1.0), color=GRAD, stroke_width=2)
        ml = label(r"$\nabla f$", font_size=20, color=GRAD).next_to(mark, UP, buff=0.05)
        res = label(rf"steepest of $720$ directions: \ ${d['dmax']:.4f}$ \\ $\|\nabla f\| = {d['gnorm']:.4f}$, \ "
                    rf"${off:.2f}^\circ$ apart", font_size=22, color=GRAD).next_to(read, DOWN, buff=0.35).align_to(read, RIGHT)
        verdict = ("exactly as the inequality says" if off < 0.5 and abs(d["dmax"] / d["gnorm"] - 1) < 1e-3
                   else "close to what the inequality says")
        with self.voiceover(
            "Seen from above, the surface becomes a map of contour lines, each at one height. <bookmark mark='a'/> "
            "Swing a direction around the point and read the slope. <bookmark mark='b'/> It's largest straight along "
            "the gradient, <bookmark mark='c'/> zero along the tangent to the contour line, <bookmark mark='d'/> and most negative "
            "pointing against it. <bookmark mark='e'/> Measured by finite differences in seven hundred and twenty "
            f"directions, the steepest slope is {d['dmax']:.4f}, the gradient's length is {d['gnorm']:.4f}, and the "
            f"two directions are {off:.2f} degrees apart: {verdict}."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.1), run_time=2.0)
            self.play(GrowArrow(gar), FadeIn(gl))
            vo.wait_until("a")
            self.add(uar)
            self.play(FadeIn(read))
            vo.wait_until("b")
            self.play(ang.animate.set_value(ang.get_value() + 0.6), run_time=0.8)
            self.play(ang.animate.set_value(math.atan2(gn[1], gn[0])), run_time=0.8)
            vo.wait_until("c")
            self.play(ang.animate.set_value(math.atan2(gn[1], gn[0]) + PI / 2), run_time=1.2)
            vo.wait_until("d")
            self.play(ang.animate.set_value(math.atan2(gn[1], gn[0]) + PI), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(pg), Create(pc), Create(mark), FadeIn(ml), run_time=1.5)
            self.play(FadeIn(res))
        uar.clear_updaters()
        dv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cauchy(self):
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=6.6, y_length=4.95, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.4, -0.6, 0])
        cont = contour_lines(ax, bowl, (-4, 4), (-3, 3), np.linspace(0.4, 3.6, 13))
        p = np.array([-3.2, 2.2])
        pts = [p.copy()]
        for _ in range(30):
            p = p - 0.4 * bowl_grad(*p)
            pts.append(p.copy())
        path = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(*q) for q in pts])
        dots = VGroup(*[Dot(ax.c2p(*q), radius=0.045, color=GRAD) for q in pts])
        hist = history_card(1847, r"Augustin-Louis Cauchy, \textit{M\'ethode g\'en\'erale pour la r\'esolution des "
                                  r"syst\`emes d'\'equations simultan\'ees}",
                            r"three pages in the \textit{Comptes rendus}: \ to solve the equations of an orbit, "
                            r"step against the gradient of a sum of squares", width=6.4, font_size=23, color=HIST)
        hist.to_corner(UL, buff=0.35)
        rule = cmath(r"x_{t+1}", r"=", r"x_t", r"-", r"\eta", r"\,\nabla f(x_t)", font_size=44,
                     colors={r"\,\nabla f(x_t)": GRAD, r"\eta": C.LR})
        rule.next_to(hist, DOWN, buff=0.5).align_to(hist, LEFT)
        eta = label(r"$\eta$: \ the step size, \ or learning rate", font_size=24, color=C.LR).next_to(rule, DOWN, buff=0.25)
        eta.align_to(rule, LEFT)
        fw = label(r"how large a step, \ and how fast it converges: \ chapter 14, \ and Part 11", font_size=22,
                   color=GREY_B).to_edge(DOWN, buff=0.3).align_to(hist, LEFT)
        tag = note(r"illustrative path").next_to(ax, DOWN, buff=0.05).align_to(ax, RIGHT)
        with self.voiceover(
            "Walking downhill this way is the oldest method in this series. <bookmark mark='a'/> In 1847 Augustin-Louis "
            "Cauchy, wanting to solve the equations of an orbit, wrote them as a sum of squares and proposed stepping "
            "against its gradient. <bookmark mark='b'/> Written today: the next point is the current one, minus a "
            "step size eta times the gradient there. <bookmark mark='c'/> How large a step, and how fast it arrives, "
            "depends on the curvature, which comes in chapter fourteen and again in Part 11."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.08), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(rule), FadeIn(eta))
            self.play(Create(path), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(fw))
        self.wait(0.3)
        self.clear_scene()
