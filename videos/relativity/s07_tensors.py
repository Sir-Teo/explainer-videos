from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import boxed, label, mtex, note, stack

P = np.array([-3.4, -0.6, 0.0])  # the base point of the vector
V = np.array([1.75, 1.05, 0.0])  # the vector, in screen units
BOX = (-6.8, 0.0, -3.6, 2.9)  # x0, x1, y0, y1 of the grid area


def linear_grid(e1, e2, color=GREY_C, n=9, opacity=0.6):
    """Lines of a linear coordinate system with basis e1, e2 through P, clipped to BOX."""
    x0, x1, y0, y1 = BOX
    g = VGroup()
    for k in range(-n, n + 1):
        for a, b in ((e1, e2), (e2, e1)):
            base = P + k * a
            pts = [base + t * b for t in np.linspace(-12, 12, 400)]
            pts = [p for p in pts if x0 <= p[0] <= x1 and y0 <= p[1] <= y1]
            if len(pts) > 1:
                g.add(Line(pts[0], pts[-1], color=color, stroke_width=1.5, stroke_opacity=opacity))
    return g


def polar_grid(O, dr, dphi, color=GREY_C, opacity=0.6):
    x0, x1, y0, y1 = BOX
    g = VGroup()
    r0 = np.linalg.norm(P - O)
    for k in range(-8, 9):
        r = r0 + k * dr
        if r <= 0.1:
            continue
        a = np.linspace(0, 2 * np.pi, 400)
        pts = O + r * np.stack([np.cos(a), np.sin(a), 0 * a], 1)
        ok = (pts[:, 0] >= x0) & (pts[:, 0] <= x1) & (pts[:, 1] >= y0) & (pts[:, 1] <= y1)
        # split into contiguous runs
        idx = np.nonzero(ok)[0]
        if len(idx) < 2:
            continue
        runs = np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1)
        for rr in runs:
            if len(rr) > 1:
                g.add(VMobject(stroke_color=color, stroke_width=1.5, stroke_opacity=opacity).set_points_as_corners(pts[rr]))
    phi0 = math.atan2(P[1] - O[1], P[0] - O[0])
    for k in range(-14, 15):
        ph = phi0 + k * dphi
        u = np.array([math.cos(ph), math.sin(ph), 0])
        pts = [O + t * u for t in np.linspace(0.05, 20, 600)]
        pts = [p for p in pts if x0 <= p[0] <= x1 and y0 <= p[1] <= y1]
        if len(pts) > 1:
            g.add(Line(pts[0], pts[-1], color=color, stroke_width=1.5, stroke_opacity=opacity))
    return g


def comps(e1, e2):
    M = np.array([[e1[0], e2[0]], [e1[1], e2[1]]])
    return np.linalg.solve(M, V[:2])


class Tensors(VoiceoverScene):
    def construct(self):
        self.why()
        self.vectors()
        self.covectors()
        self.general()
        self.metric()

    # ------------------------------------------------------------------
    def why(self):
        t = VGroup(
            label(r"Coordinates are labels we choose.", font_size=36),
            label(r"Physics can't depend on the labels.", font_size=36),
            label(r"So the laws must be \emph{tensor equations}: true in every coordinate system.", font_size=36,
                  color=C.METRIC),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "In curved spacetime there are no preferred coordinates. Any labeling of events is as good as any other, as "
            "long as it's smooth. <bookmark mark='a'/> But the physics can't depend on our choice of labels. "
            "<bookmark mark='b'/> So the laws of physics have to be written as tensor equations: statements whose truth "
            "doesn't depend on the coordinate system. Let's see what that means, starting with the simplest tensor of all."
        ) as vo:
            self.play(FadeIn(t[0]))
            vo.wait_until("a")
            self.play(FadeIn(t[1]))
            vo.wait_until("b")
            self.play(FadeIn(t[2]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def vectors(self):
        u = 0.8
        states = [
            ("cartesian", np.array([u, 0, 0]), np.array([0, u, 0])),
            ("skewed", np.array([u, 0, 0]), np.array([0.5, 0.65, 0])),
        ]
        O = np.array([-7.6, -4.6, 0])
        r0 = np.linalg.norm(P - O)
        rh = (P - O) / r0
        ph_hat = np.array([-rh[1], rh[0], 0])
        dphi = 0.12
        states.append(("polar", u * rh, r0 * dphi * ph_hat))
        grids = [linear_grid(states[0][1], states[0][2]), linear_grid(states[1][1], states[1][2]),
                 polar_grid(O, u, dphi)]
        arrow = Arrow(P, P + V, buff=0, color=C.VECTOR, stroke_width=7, max_tip_length_to_length_ratio=0.15)
        vl = MathTex(r"\mathbf V", font_size=40, color=C.VECTOR).next_to(arrow.get_end(), UR, buff=0.05)

        def basis(e1, e2):
            a1 = Arrow(P, P + e1, buff=0, color=GREY_A, stroke_width=5, max_tip_length_to_length_ratio=0.3)
            a2 = Arrow(P, P + e2, buff=0, color=GREY_A, stroke_width=5, max_tip_length_to_length_ratio=0.3)
            l1 = MathTex(r"\mathbf e_1", font_size=30).next_to(a1.get_end(), DOWN, buff=0.08)
            l2 = MathTex(r"\mathbf e_2", font_size=30).next_to(a2.get_end(), LEFT, buff=0.08)
            return VGroup(a1, a2, l1, l2)

        bases = [basis(e1, e2) for _, e1, e2 in states]
        cps = [comps(e1, e2) for _, e1, e2 in states]
        eq = MathTex(r"\mathbf V", r"=", r"V^1", r"\,\mathbf e_1", r"+", r"V^2", r"\,\mathbf e_2", font_size=44)
        eq[0].set_color(C.VECTOR)
        eq.move_to([3.6, 2.2, 0])
        h1 = MathTex(r"V^1 =", font_size=40, color=C.VECTOR)
        h2 = MathTex(r"V^2 =", font_size=40, color=C.VECTOR)
        d1 = DecimalNumber(cps[0][0], num_decimal_places=2, font_size=40, color=C.VECTOR)
        d2 = DecimalNumber(cps[0][1], num_decimal_places=2, font_size=40, color=C.VECTOR)
        vals = VGroup(VGroup(h1, d1).arrange(RIGHT, buff=0.15), VGroup(h2, d2).arrange(RIGHT, buff=0.15))
        vals.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eq, DOWN, buff=0.5)
        names = [label(r"Cartesian", font_size=30, color=GREY_A), label(r"skewed", font_size=30, color=GREY_A),
                 label(r"polar", font_size=30, color=GREY_A)]
        for n_ in names:
            n_.next_to(vals, DOWN, buff=0.4)
        law = mtex(r"V'^{\mu}", r"=", r"\frac{\partial x'^{\mu}}{\partial x^{\nu}}", r"\,V^{\nu}", font_size=44)
        law[0].set_color(C.VECTOR)
        law[3].set_color(C.VECTOR)
        law.move_to([3.6, -1.6, 0])
        lawl = label(r"components transform with the Jacobian", font_size=26, color=GREY_A).next_to(law, DOWN, buff=0.2)
        with self.voiceover(
            "A vector is an arrow at a point: a direction and a size, like a velocity. <bookmark mark='a'/> To describe it "
            "with numbers, we lay down coordinates. Their grid lines give two basis vectors at our point, e one and e two, "
            "and the vector is some amount of each: <bookmark mark='c'/> its components, V one and V two."
        ) as vo:
            self.play(GrowArrow(arrow), FadeIn(vl))
            vo.wait_until("a")
            self.play(Create(grids[0], lag_ratio=0.02), FadeIn(bases[0]), run_time=1.5)
            self.add(arrow, vl)
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(vals), FadeIn(names[0]))
        with self.voiceover(
            "<bookmark mark='s'/> Now change the coordinates. The arrow itself doesn't move: it's the same physical "
            "thing. But the basis vectors change, so the components change. <bookmark mark='p'/> Now polar "
            "coordinates: new basis vectors, new numbers, same arrow. <bookmark mark='l'/> How the numbers change is completely "
            "determined by how the coordinates change: the new components are the Jacobian matrix of partial derivatives "
            "times the old ones. Anything whose components change this way is a vector."
        ) as vo:
            vo.wait_until("s")
            self.play(ReplacementTransform(grids[0], grids[1]), ReplacementTransform(bases[0], bases[1]),
                      d1.animate.set_value(cps[1][0]), d2.animate.set_value(cps[1][1]),
                      ReplacementTransform(names[0], names[1]), run_time=2)
            self.add(arrow, vl)
            vo.wait_until("p")
            self.play(ReplacementTransform(grids[1], grids[2]), ReplacementTransform(bases[1], bases[2]),
                      d1.animate.set_value(cps[2][0]), d2.animate.set_value(cps[2][1]),
                      ReplacementTransform(names[1], names[2]), run_time=2)
            self.add(arrow, vl)
            vo.wait_until("l")
            self.play(Write(law), FadeIn(lawl))
        dd = mtex(r"\mathbf e_\mu", r"=", r"\partial_\mu", r",\qquad", r"\mathbf V", r"=", r"V^\mu\,\partial_\mu",
                  font_size=40)
        dd[4].set_color(C.VECTOR)
        dd.move_to(law).shift(DOWN * 0.1)
        ddl = label(r"a vector is a direction to take derivatives in", font_size=26, color=GREY_A).next_to(dd, DOWN, buff=0.2)
        with self.voiceover(
            "There's a slick way to see why. <bookmark mark='d'/> Think of the basis vector e mu as the operation "
            "\"move along the x mu coordinate line\", that is, the partial derivative with respect to x mu. Then a vector "
            "is V mu times partial mu: a directional derivative. The chain rule for partial derivatives is exactly the "
            "Jacobian rule for components."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeOut(law), FadeOut(lawl), FadeIn(dd), FadeIn(ddl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def covectors(self):
        w = np.array([1.0, 0.55, 0.0])  # gradient of f, screen units: level lines of f spaced 1/|w|
        w = w / np.linalg.norm(w) / 0.5  # spacing 0.5
        spacing = 1 / np.linalg.norm(w)
        n_hat = w / np.linalg.norm(w)
        t_hat = np.array([-n_hat[1], n_hat[0], 0])
        lines = VGroup()
        for k in range(-9, 12):
            c0 = P + k * spacing * n_hat
            a, b = c0 - 6 * t_hat, c0 + 6 * t_hat
            lines.add(Line(a, b, color=C.COVECTOR, stroke_width=2.5, stroke_opacity=0.9))
        clipbox = Rectangle(width=6.8, height=6.5).move_to([-3.4, -0.35, 0])
        lines = VGroup(*[l for l in lines])
        for l in lines:
            # clip each line to the box by sampling
            pts = [l.point_from_proportion(t) for t in np.linspace(0, 1, 300)]
            pts = [p for p in pts if BOX[0] <= p[0] <= BOX[1] and BOX[2] <= p[1] <= BOX[3]]
            if len(pts) > 1:
                l.put_start_and_end_on(pts[0], pts[-1])
            else:
                l.set_opacity(0)
        arrow = Arrow(P, P + V, buff=0, color=C.VECTOR, stroke_width=7, max_tip_length_to_length_ratio=0.15)
        crossings = float(w @ V)
        assert 3.5 < crossings < 4.4
        marks = VGroup()
        for k in range(1, int(crossings) + 1):
            # point where the arrow crosses level k
            s = k / crossings
            marks.add(Dot(P + s * V, radius=0.07, color=WHITE))
        title = label(r"A covector: a stack of level lines", font_size=34, color=C.COVECTOR).to_corner(UR, buff=0.5)
        eq = mtex(r"\omega(\mathbf V)", r"=", r"\omega_\mu V^\mu", r"=", r"\text{number of lines crossed}", font_size=36)
        eq[0].set_color(C.COVECTOR)
        eq[2].set_color(C.COVECTOR)
        eq.next_to(title, DOWN, buff=0.5).align_to(title, RIGHT)
        num_ = mtex(rf"\approx {crossings:.1f}", font_size=36).next_to(eq, DOWN, buff=0.2).align_to(eq, RIGHT)
        grad = mtex(r"df", r"=", r"\partial_\mu f\, dx^\mu", font_size=36, color=C.COVECTOR)
        grad.next_to(num_, DOWN, buff=0.5).align_to(eq, RIGHT)
        gradl = label(r"e.g. the gradient: level lines of $f$", font_size=24, color=GREY_A).next_to(grad, DOWN, buff=0.15).align_to(grad, RIGHT)
        law = mtex(r"\omega'_{\mu}", r"=", r"\frac{\partial x^{\nu}}{\partial x'^{\mu}}", r"\,\omega_{\nu}", font_size=40)
        law[0].set_color(C.COVECTOR)
        law[3].set_color(C.COVECTOR)
        law.next_to(gradl, DOWN, buff=0.5).align_to(eq, RIGHT)
        lawl = label(r"the inverse Jacobian: so $\omega_\mu V^\mu$ is the same in every coordinate system", font_size=24,
                     color=GREY_A).next_to(law, DOWN, buff=0.15).align_to(eq, RIGHT)
        with self.voiceover(
            "The second kind of object is a covector. <bookmark mark='l'/> Picture it as a stack of parallel level lines, "
            "like the contour lines of a function on a map: the gradient of the function. <bookmark mark='a'/> A covector "
            "eats a vector and returns a number: <bookmark mark='c'/> how many of its lines the arrow crosses. Here, about "
            "four. <bookmark mark='g'/> In components, that's omega mu times V mu, summed, with the index down on omega and "
            "up on V."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("l")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("a")
            self.play(GrowArrow(arrow))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in marks], lag_ratio=0.3))
            self.play(Write(eq[0:3]))
            vo.wait_until("g")
            self.play(Write(eq[3:]), FadeIn(num_), FadeIn(grad), FadeIn(gradl))
        with self.voiceover(
            "<bookmark mark='t'/> When coordinates change, a covector's components change with the inverse Jacobian, "
            "the opposite way to a vector's. That's what upper and lower indices keep track of. And it's exactly what's "
            "needed for the count to come out the same in every coordinate system: the number of lines an arrow crosses "
            "is a fact about the arrow and the lines, not about the labels."
        ) as vo:
            vo.wait_until("t")
            self.play(Write(law), FadeIn(lawl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def general(self):
        tl = mtex(r"T'^{\mu}{}_{\nu}", r"=", r"\frac{\partial x'^{\mu}}{\partial x^{\alpha}}",
                  r"\frac{\partial x^{\beta}}{\partial x'^{\nu}}", r"\,T^{\alpha}{}_{\beta}", font_size=48)
        tl.move_to(UP * 1.6)
        tl[2].set_color(C.VECTOR)
        tl[3].set_color(C.COVECTOR)
        tll = label(r"one factor per index: up indices like a vector, down indices like a covector", font_size=28,
                    color=GREY_A).next_to(tl, DOWN, buff=0.3)
        key = VGroup(
            label(r"If a tensor is zero in one coordinate system,", font_size=34),
            label(r"it is zero in \emph{every} coordinate system.", font_size=34, color=C.METRIC),
        ).arrange(DOWN, buff=0.18).next_to(tll, DOWN, buff=0.8)
        so = label(r"So ``spacetime is flat'' must mean: some tensor built from $g_{\mu\nu}$ vanishes.", font_size=30,
                   color=C.CURVATURE).next_to(key, DOWN, buff=0.6)
        with self.voiceover(
            "From vectors and covectors we build everything else. <bookmark mark='t'/> A tensor can have any number of "
            "upper and lower indices, and under a change of coordinates it picks up one Jacobian factor per index: the "
            "upper ones transform like vectors, the lower ones like covectors. <bookmark mark='k'/> Here's why this is "
            "worth the trouble: the transformation is linear and homogeneous. So if all of a tensor's components vanish "
            "in one coordinate system, they vanish in every coordinate system. A tensor equation, true for one observer, "
            "is true for all. <bookmark mark='s'/> That tells us what we're looking for: curvature must be measured by a "
            "tensor built from the metric, one that vanishes exactly when spacetime is flat."
        ) as vo:
            vo.wait_until("t")
            self.play(Write(tl), FadeIn(tll))
            vo.wait_until("k")
            self.play(FadeIn(key, shift=UP * 0.2))
            vo.wait_until("s")
            self.play(FadeIn(so))
        self.clear_scene()

    # ------------------------------------------------------------------
    def metric(self):
        g1 = mtex(r"\mathbf V\cdot\mathbf W", r"=", r"g_{\mu\nu}", r"V^\mu W^\nu", font_size=46)
        g1[2].set_color(C.METRIC)
        g2 = mtex(r"|\mathbf V|^2", r"=", r"g_{\mu\nu}", r"V^\mu V^\nu", font_size=46)
        g2[2].set_color(C.METRIC)
        col = VGroup(g1, g2).arrange(DOWN, buff=0.45).move_to([3.4, 1.9, 0])
        low = mtex(r"V_\mu", r"=", r"g_{\mu\nu}", r"V^\nu", font_size=46)
        low[0].set_color(C.COVECTOR)
        low[2].set_color(C.METRIC)
        low[3].set_color(C.VECTOR)
        inv = mtex(r"g^{\mu\lambda}", r"g_{\lambda\nu}", r"=", r"\delta^\mu_\nu", font_size=40, color=C.METRIC)
        VGroup(low, inv).arrange(DOWN, buff=0.4).next_to(col, DOWN, buff=0.7)
        lowl = label(r"lowering an index: arrow $\to$ stack", font_size=26, color=GREY_A).next_to(low, RIGHT, buff=0.3)
        if lowl.get_right()[0] > 7:
            lowl.next_to(inv, DOWN, buff=0.3)
        # the arrow becomes the stack of lines perpendicular to it, spaced 1/|V|
        Q = np.array([-3.4, -0.4, 0])
        Vv = np.array([1.6, 0.9, 0])
        arrow = Arrow(Q, Q + Vv, buff=0, color=C.VECTOR, stroke_width=7, max_tip_length_to_length_ratio=0.15)
        n_hat = Vv / np.linalg.norm(Vv)
        t_hat = np.array([-n_hat[1], n_hat[0], 0])
        sp = 1 / np.linalg.norm(Vv)
        stack_ = VGroup(*[Line(Q + k * sp * n_hat - 2.6 * t_hat, Q + k * sp * n_hat + 2.6 * t_hat, color=C.COVECTOR,
                               stroke_width=2.5) for k in range(-4, 7)])
        with self.voiceover(
            "The most important tensor in this story is the metric, g mu nu, with two lower indices. <bookmark mark='a'/> "
            "It's a machine that takes two vectors and returns their dot product, <bookmark mark='b'/> and so the length of "
            "any vector, and the angle between any two. Everything geometric starts here."
        ) as vo:
            self.play(GrowArrow(arrow))
            vo.wait_until("a")
            self.play(Write(g1))
            vo.wait_until("b")
            self.play(Write(g2))
        with self.voiceover(
            "<bookmark mark='l'/> The metric also converts vectors into covectors. Feed it just one vector, and what's "
            "left is a covector: V with its index lowered. <bookmark mark='s'/> Geometrically, the arrow becomes the stack of "
            "lines perpendicular to it, spaced so that the arrow crosses exactly its own length squared of them. "
            "<bookmark mark='i'/> The inverse metric, g with upper indices, goes back the other way. From now on, raising "
            "and lowering indices with the metric is routine."
        ) as vo:
            vo.wait_until("l")
            self.play(Write(low), FadeIn(lowl))
            vo.wait_until("s")
            self.play(LaggedStart(*[Create(l) for l in stack_], lag_ratio=0.06), arrow.animate.set_opacity(0.5), run_time=2)
            vo.wait_until("i")
            self.play(Write(inv))
        self.clear_scene()
