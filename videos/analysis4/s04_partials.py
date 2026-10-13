from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import heatmap, load, plain_axes, square_axes


def f_bad(X, Y):
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where((X == 0) & (Y == 0), 0.0, X * Y / (X**2 + Y**2))


def g_bad(X, Y):
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where((X == 0) & (Y == 0), 0.0, X**2 * Y / (X**2 + Y**2))


class Partials(VoiceoverScene):
    def construct(self):
        self.card()
        self.discontinuous()
        self.not_linear()
        self.repair()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Partial derivatives are not enough",
                            r"Can a function have every partial derivative and no derivative?", lit=(), part=4)
        with self.voiceover("Chapter three: two exhibits for the museum, and the theorem that repairs the damage."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def discontinuous(self):
        S = 5.0
        ax = square_axes([-1, 1, 0.5], [-1, 1, 0.5], S / 2).move_to([-3.3, -0.6, 0])
        img = heatmap(f_bad, (-1, 1), (-1, 1), S, S, -0.5, 0.5).move_to(ax.c2p(0, 0))
        head = VGroup(MathTex(r"f(x, y) = \frac{xy}{x^2 + y^2}, \qquad f(0, 0) = 0", font_size=36),
                      label(r"blue: \ $-\tfrac12$, \ \ dark: \ $0$, \ \ orange: \ $+\tfrac12$", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        axes_hl = VGroup(Line(ax.c2p(-1, 0), ax.c2p(1, 0), color=WHITE, stroke_width=4),
                         Line(ax.c2p(0, -1), ax.c2p(0, 1), color=WHITE, stroke_width=4))
        diag = Line(ax.c2p(-1, -1), ax.c2p(1, 1), color=C.EPS, stroke_width=4)
        rays = VGroup()
        for deg in (30, 60, 120, 150):
            t = math.radians(deg)
            rays.add(DashedLine(ax.c2p(0, 0), ax.c2p(math.cos(t), math.sin(t)), color=GREY_A, stroke_width=2))
        tv = np.linspace(-1, 1, 9)
        assert np.allclose(f_bad(tv, 0 * tv), 0) and np.allclose(f_bad(0 * tv, tv), 0)
        assert np.allclose(f_bad(tv[tv != 0], tv[tv != 0]), 0.5)
        side = VGroup(
            label(r"on both axes $f = 0$, \ so", font_size=26),
            MathTex(r"\frac{\partial f}{\partial x}(0, 0) = \frac{\partial f}{\partial y}(0, 0) = 0", font_size=32),
            label(r"on the diagonal $f = \tfrac12$, \ right up to $0$:", font_size=26, color=C.EPS),
            label(r"$f$ is not even continuous at $0$", font_size=26, color=C.PATHOLOGY),
            MathTex(r"f(r\cos\theta, r\sin\theta) = \tfrac12 \sin 2\theta", font_size=30, color=GREY_A),
            label(r"constant on each ray", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The first exhibit: x y over x squared plus y squared, with value zero at the origin. "
            "Its colors show its values, and they depend only on the direction from the origin. "
            "<bookmark mark='b'/> Along both axes the function is identically zero, so both partial derivatives at the "
            "origin exist, and both are zero. <bookmark mark='c'/> But along the diagonal it equals one half, right up "
            "to the origin. So it isn't even continuous there, let alone differentiable. <bookmark mark='d'/> Partial "
            "derivatives only look along the axes, and a function can misbehave in every other direction."
        ) as vo:
            self.play(FadeIn(head[0]), FadeIn(img), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(rays))
            self.play(FadeIn(side[4:]))
            vo.wait_until("b")
            self.play(Create(axes_hl), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(diag), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Indicate(axes_hl, color=C.EPS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def not_linear(self):
        d = load("museum")
        th, Du = d["th"], d["Du"]
        S = 3.6
        ax = square_axes([-1, 1, 0.5], [-1, 1, 0.5], S / 2).move_to([-4.5, -1.35, 0])
        img = heatmap(g_bad, (-1, 1), (-1, 1), S, S, -0.6, 0.6).move_to(ax.c2p(0, 0))
        head = VGroup(MathTex(r"g(x, y) = \frac{x^2 y}{x^2 + y^2}, \qquad g(0, 0) = 0", font_size=36),
                      label(r"continuous \ ($|g| \le |y|$), \ and differentiable in every direction at $0$",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        bx = plain_axes([0, 2 * np.pi, np.pi / 2], [-0.5, 0.5, 0.25], 6.6, 3.0).move_to([2.9, -0.2, 0])
        actual = VMobject(color=C.APPROX, stroke_width=3.5).set_points_as_corners([bx.c2p(t, v) for t, v in zip(th, Du)])
        pred = Line(bx.c2p(0, 0), bx.c2p(2 * np.pi, 0), color=WHITE, stroke_width=3)
        part1 = VMobject(color=C.EPS, stroke_width=2.5).set_points_as_corners(
            [bx.c2p(t, 0.25 * math.sin(t)) for t in th])
        assert np.allclose(Du, 0.25 * np.sin(th) + 0.25 * np.sin(3 * th), atol=1e-12)
        bl = VGroup(MathTex(r"D_u g(0) = \cos^2\theta \sin\theta", font_size=30, color=C.APPROX),
                    MathTex(r"\nabla g(0) \cdot u = 0", font_size=30)).arrange(RIGHT, buff=0.6).next_to(bx, UP, buff=0.15)
        side = VGroup(
            MathTex(r"\cos^2\theta \sin\theta = \tfrac14 \sin\theta + \tfrac14 \sin 3\theta", font_size=32),
            label(r"a derivative would force $D_u g(0) = a\cos\theta + b\sin\theta$:", font_size=24, color=GREY_A),
            label(r"the $\sin 3\theta$ part is not linear in $u$, \ so $g$ is not differentiable at $0$", font_size=24,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, buff=0.15).next_to(bx, DOWN, buff=0.3)
        for r_ in side:
            if r_.width > 7.2:
                r_.width = 7.2
        side.arrange(DOWN, buff=0.15).next_to(bx, DOWN, buff=0.3)
        card = museum_card(r"$x^2y/(x^2 + y^2)$", r"a classical example", r"`all directional derivatives make a "
                           r"derivative'", r"Rudin 9.21 is the repair", width=4.0).scale(0.8)
        card.next_to(img, UP, buff=0.15)
        assert card.get_top()[1] < head.get_bottom()[1] - 0.1
        # the direction u = (cos t, sin t) as a ray on the heatmap; along it g(su) = s cos^2 t sin t is linear in s
        tt = ValueTracker(0.9)
        o = ax.c2p(0, 0)

        def ray_():
            t = tt.get_value()
            return VGroup(Arrow(o, ax.c2p(0.9 * math.cos(t), 0.9 * math.sin(t)), buff=0, color=C.APPROX,
                                stroke_width=4, max_tip_length_to_length_ratio=0.12),
                          Arc(radius=0.3, start_angle=0, angle=max(t, 1e-3), arc_center=o, color=WHITE, stroke_width=2))

        ray = always_redraw(ray_)
        th_l = always_redraw(lambda: MathTex(r"\theta", font_size=24).move_to(
            o + 0.48 * np.array([math.cos(tt.get_value() / 2), math.sin(tt.get_value() / 2), 0])))
        dot = always_redraw(lambda: Dot(bx.c2p(tt.get_value(), math.cos(tt.get_value()) ** 2 * math.sin(tt.get_value())),
                                        radius=0.06, color=C.APPROX))
        along = MathTex(r"g(s u) = s\,\cos^2\theta\,\sin\theta", r"\ \Rightarrow\ D_u g(0) = \cos^2\theta\sin\theta",
                        font_size=26).next_to(img, DOWN, buff=0.15)
        along.set_x(-6.75 + along.width / 2)
        assert along.get_left()[0] > -6.95 and along.get_bottom()[1] > -3.95
        with self.voiceover(
            "<bookmark mark='a'/> The second exhibit is subtler: x squared y over x squared plus y squared. It is "
            "continuous, and at the origin it has a derivative in every direction, not just along the axes. "
            "<bookmark mark='b'/> Plot that directional derivative against the angle of the direction. If g were "
            "differentiable, this would be the gradient dotted with u, a pure cosine. The gradient is zero, so it "
            "would be flat. <bookmark mark='c'/> It isn't. Cos squared times sine is a quarter of sine theta plus a "
            "quarter of sine three theta, and the sine three theta part is not linear in the direction. "
            "<bookmark mark='d'/> No linear map fits, so there is no derivative: directional derivatives in every "
            "direction are not enough either."
        ) as vo:
            self.play(FadeIn(head[0]), FadeIn(img), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(bx))
            self.play(FadeIn(ray), FadeIn(th_l))
            self.play(FadeIn(along[0]))
            self.play(FadeIn(along[1]))
            vo.wait_until("b")
            self.play(Create(pred), FadeIn(bl[1]))
            tt.set_value(0)
            self.add(dot)
            self.play(Create(actual), tt.animate.set_value(2 * np.pi), FadeIn(bl[0]), run_time=4.0, rate_func=linear)
            ray.clear_updaters()
            th_l.clear_updaters()
            dot.clear_updaters()
            self.play(FadeOut(ray[1]), FadeOut(th_l), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), Create(part1))
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(card, scale=0.95))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def repair(self):
        S = 5.0
        ax = square_axes([-0.2, 1.2, 0.5], [-0.2, 1.2, 0.5], S / 1.4).move_to([-3.4, -0.7, 0])
        ax.set_opacity(0.5)
        F = lambda X, Y: np.sin(2 * X) * np.cos(Y) + 0.5 * X * Y  # noqa: E731
        img = heatmap(F, (-0.2, 1.2), (-0.2, 1.2), S, S, -1.2, 1.2).move_to(ax.c2p(0.5, 0.5)).set_opacity(0.8)
        x = np.array([0.2, 0.25])
        h = np.array([0.7, 0.6])
        P0, P1, P2 = x, x + np.array([h[0], 0]), x + h
        leg1 = Arrow(ax.c2p(*P0), ax.c2p(*P1), buff=0, color=C.SEQ, stroke_width=5, tip_length=0.18)
        leg2 = Arrow(ax.c2p(*P1), ax.c2p(*P2), buff=0, color=C.APPROX, stroke_width=5, tip_length=0.18)
        direct = DashedLine(ax.c2p(*P0), ax.c2p(*P2), color=WHITE, stroke_width=2)
        # mean value points on each leg (one-variable MVT), found numerically
        tx = np.linspace(P0[0], P1[0], 20001)
        fx = np.cos(tx * 2) * 2 * np.cos(P0[1]) + 0.5 * P0[1]
        sx = (F(P1[0], P0[1]) - F(*P0)) / h[0]
        xi = tx[np.argmin(np.abs(fx - sx))]
        assert abs(2 * math.cos(2 * xi) * math.cos(P0[1]) + 0.5 * P0[1] - sx) < 1e-3
        ty = np.linspace(P1[1], P2[1], 20001)
        fy = -np.sin(2 * P1[0]) * np.sin(ty) + 0.5 * P1[0]
        sy = (F(*P2) - F(*P1)) / h[1]
        eta = ty[np.argmin(np.abs(fy - sy))]
        assert abs(-math.sin(2 * P1[0]) * math.sin(eta) + 0.5 * P1[0] - sy) < 1e-3
        mv = VGroup(Dot(ax.c2p(xi, P0[1]), radius=0.08, color=C.SEQ), Dot(ax.c2p(P1[0], eta), radius=0.08, color=C.APPROX))
        dots = VGroup(Dot(ax.c2p(*P0), radius=0.08, color=WHITE), Dot(ax.c2p(*P2), radius=0.08, color=WHITE))
        dl = VGroup(MathTex("x", font_size=30).next_to(dots[0], DL, buff=0.05),
                    MathTex("x + h", font_size=30).next_to(dots[1], UR, buff=0.05))
        head = VGroup(label(r"\textbf{Rudin 9.21} \ the repair: \ \emph{continuous} partial derivatives", font_size=30),
                      MathTex(r"f \in \mathcal C^1(E) \iff \text{every } \partial f_i / \partial x_j \text{ exists and is "
                              r"continuous}", font_size=32, color=C.EPS)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        rows = VGroup(
            label(r"go from $x$ to $x + h$ one coordinate at a time:", font_size=24),
            MathTex(r"f(x + h) - f(x) = ", r"D_1 f(\xi)\, h_1", r" + ", r"D_2 f(\eta)\, h_2", font_size=30),
            label(r"(the one-variable mean value theorem on each leg)", font_size=22, color=GREY_A),
            label(r"continuity: \ $D_1 f(\xi) \approx D_1 f(x)$, \ $D_2 f(\eta) \approx D_2 f(x)$", font_size=24),
            MathTex(r"f(x + h) - f(x) = \nabla f(x) \cdot h + o(|h|)", font_size=30, color=C.EPS),
            label(r"in the museum pieces the partials jump at $0$", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, -0.75, 0])
        rows[1][1].set_color(C.SEQ)
        rows[1][3].set_color(C.APPROX)
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, -0.75, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The repair is Rudin's theorem 9.21: if the partial derivatives exist and are "
            "continuous, the function is continuously differentiable. <bookmark mark='b'/> The idea: to go from x to x "
            "plus h, move one coordinate at a time. <bookmark mark='c'/> On each leg only one variable changes, so the "
            "one-variable mean value theorem gives the change as a partial derivative at some point of that leg, times "
            "the step. <bookmark mark='d'/> If the partials are continuous, their values at those points are close to "
            "their values at x, and the change is the gradient dotted with h, up to an error small compared with h. "
            "In the museum, the partials jump at the origin, and the argument breaks."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(ax))
            self.play(FadeIn(dots), FadeIn(dl), Create(direct))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.play(GrowArrow(leg1))
            self.play(GrowArrow(leg2))
            vo.wait_until("c")
            self.play(FadeIn(mv, scale=1.5), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            self.play(FadeIn(rows[4]))
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
