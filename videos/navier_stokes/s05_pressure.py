from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import caption_box, heatmap, label, pressure_colormap

P_FORCE = "#FF8C7A"  # lighter red for force arrows drawn on top of pressure maps


def push_arrows(box: Mobject, lengths, color=C.PRESSURE, gap=0.08, stroke_width=7):
    """Inward arrows on faces of ``box``; ``lengths`` is [(direction, length), ...]."""
    out = VGroup()
    for d, L in lengths:
        d = np.array(d, dtype=float)
        face = box.get_center() + d * (box.width / 2 if d[0] else box.height / 2)
        end = face + d * gap
        out.add(Arrow(end + d * L, end, buff=0, color=color, stroke_width=stroke_width,
                      max_tip_length_to_length_ratio=0.3))
    return out


class PressureForce(VoiceoverScene):
    def construct(self):
        self.uniform()
        self.gradient_derivation()
        self.pressure_map()
        self.vortex_payoff()

    # ------------------------------------------------------------------
    def uniform(self):
        box = Square(1.6, color=WHITE, stroke_width=3, fill_color=C.VELOCITY, fill_opacity=0.2)
        arrows = push_arrows(box, [(LEFT, 1.1), (RIGHT, 1.1), (UP, 1.1), (DOWN, 1.1)])
        pa = MathTex(r"F = p \cdot A", font_size=48)
        pa[0][2].set_color(C.PRESSURE)
        perp = label(r"perpendicular to every face", font_size=30, color=C.DIM)
        VGroup(pa, perp).arrange(DOWN, buff=0.2).move_to(LEFT * 4.6)
        with self.voiceover(
            "Now the forces, starting with pressure. Pressure pushes on any surface, perpendicular to it, "
            "<bookmark mark='f'/> with a force equal to the pressure times the area."
        ) as vo:
            self.play(FadeIn(box))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15))
            vo.wait_until("f")
            self.play(Write(pa), FadeIn(perp))

        net = MathTex(r"F_{\text{net}} = 0", font_size=52).move_to(RIGHT * 4.8)
        big = push_arrows(box, [(LEFT, 2.0), (RIGHT, 2.0), (UP, 2.0), (DOWN, 2.0)])
        with self.voiceover(
            "If the pressure is the same on all sides of our parcel, the pushes cancel perfectly. "
            "<bookmark mark='z'/> A uniform pressure, no matter how large, <bookmark mark='big'/> produces no net force at all. "
            "<bookmark mark='m'/> What matters is how pressure varies."
        ) as vo:
            vo.wait_until("z")
            self.play(Write(net))
            vo.wait_until("big")
            self.play(Transform(arrows, big), run_time=1.5)
            vo.wait_until("m")
            self.play(Indicate(net))
        self.play(FadeOut(VGroup(box, arrows, pa, perp, net)))

    # ------------------------------------------------------------------
    def gradient_derivation(self):
        x0, x1, y0, y1 = -7.1, -0.4, -2.6, 2.6
        pmap = heatmap(lambda X, Y: -X, (x0, x1), (y0, y1), resolution=120,
                       colormap=pressure_colormap(-x1 - 1.5, -x0 + 0.5), opacity=1.0)
        border = Rectangle(width=x1 - x0, height=y1 - y0, color=GREY_C, stroke_width=1.5).move_to(pmap)
        hi = label(r"high $p$", font_size=30).move_to([x0 + 0.9, y1 - 0.35, 0])
        lo = label(r"low $p$", font_size=30).move_to([x1 - 0.85, y1 - 0.35, 0])

        box = Rectangle(width=1.6, height=1.6, color=WHITE, stroke_width=3, fill_color=C.VELOCITY, fill_opacity=0.25)
        box.move_to([-4.1, -0.1, 0])
        left = Arrow(box.get_left() + LEFT * 1.75, box.get_left() + LEFT * 0.06, buff=0, color=P_FORCE, stroke_width=8)
        right = Arrow(box.get_right() + RIGHT * 1.0, box.get_right() + RIGHT * 0.06, buff=0, color=P_FORCE, stroke_width=8)
        net = Arrow(box.get_center() + DOWN * 0.45 + LEFT * 0.4, box.get_center() + DOWN * 0.45 + RIGHT * 0.5, buff=0,
                    color=YELLOW, stroke_width=8)
        l_lab = MathTex(r"p(x)\,A", font_size=34).next_to(left, UP, buff=0.12)
        r_lab = MathTex(r"p(x{+}dx)\,A", font_size=34).next_to(right, UP, buff=0.12).align_to(right, RIGHT).shift(RIGHT * 0.35)
        for m in (l_lab, r_lab):
            m.add_background_rectangle(opacity=0.75, buff=0.06)
        dx = BraceLabel(box, "dx", brace_direction=DOWN, font_size=34)
        area = label(r"face area $A$", font_size=28).next_to(box, UP, buff=0.12)
        area.add_background_rectangle(opacity=0.75, buff=0.06)

        with self.voiceover(
            "So suppose the pressure varies from left to right. Take a box of width dx and face area A. "
            "<bookmark mark='l'/> The left face feels the pressure at x, pushing rightward with force p of x times A. "
            "<bookmark mark='r'/> The right face feels p at x plus dx, pushing leftward."
        ) as vo:
            self.play(FadeIn(pmap), Create(border), FadeIn(hi), FadeIn(lo))
            self.play(FadeIn(box), FadeIn(dx), FadeIn(area))
            vo.wait_until("l")
            self.play(GrowArrow(left), FadeIn(l_lab))
            vo.wait_until("r")
            self.play(GrowArrow(right), FadeIn(r_lab))

        rows = VGroup(
            MathTex(r"F_x", r"=", r"p(x)\,A - p(x{+}dx)\,A"),
            MathTex(r"=", r"-\big[\,p(x{+}dx) - p(x)\,\big]\,A"),
            MathTex(r"\approx", r"-{\partial p \over \partial x}\,dx\,A"),
            MathTex(r"=", r"-{\partial p \over \partial x}\,dV"),
        )
        for r in rows:
            r.scale(0.85)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        for r in rows[1:]:
            r.shift(RIGHT * (rows[0][1].get_left()[0] - r[0].get_left()[0]))
        rows.move_to([3.55, 1.25, 0])
        per = MathTex(r"{F_x \over dV}", r"=", r"-{\partial p \over \partial x}", font_size=48)
        per[2].set_color(C.PRESSURE)
        per.next_to(rows, DOWN, buff=0.55)
        per_box = caption_box(per, color=C.PRESSURE)
        taylor = MathTex(r"\text{Taylor: }\; p(x{+}dx) \approx p(x) + {\partial p \over \partial x}\,dx", font_size=34,
                         color=C.DIM).to_edge(DOWN, buff=0.4).shift(RIGHT * 3.3)

        with self.voiceover(
            "The net force is the difference. <bookmark mark='t'/> For a tiny box, p of x plus dx minus p of x is just the "
            "derivative of p times dx. <bookmark mark='v'/> And dx times A is the volume of the box."
        ) as vo:
            self.play(Write(rows[0]), GrowArrow(net))
            self.play(TransformFromCopy(rows[0][2], rows[1][1]), FadeIn(rows[1][0]))
            vo.wait_until("t")
            self.play(FadeIn(taylor, shift=UP * 0.2))
            self.play(TransformFromCopy(rows[1][1], rows[2][1]), FadeIn(rows[2][0]))
            vo.wait_until("v")
            self.play(TransformFromCopy(rows[2][1], rows[3][1]), FadeIn(rows[3][0]))

        grad = MathTex(
            r"\vf_{\text{pressure}}", r"=", r"-\Big({\partial p \over \partial x}, {\partial p \over \partial y}, "
            r"{\partial p \over \partial z}\Big)", r"=", r"-\nabla p", font_size=46,
        )
        grad[0].set_color(C.PRESSURE)
        grad[4].set_color(C.PRESSURE)
        grad.to_edge(DOWN, buff=0.35)
        gbox = caption_box(grad[4], color=C.PRESSURE)
        with self.voiceover(
            "So the horizontal force per unit volume is <bookmark mark='a'/> minus partial p partial x. The same argument in "
            "the y and z directions gives the other components, <bookmark mark='g'/> and together they make minus the "
            "gradient of p."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(taylor), Write(per), Create(per_box))
            self.play(Group(pmap, border, hi, lo, box, left, right, net, l_lab, r_lab, dx, area).animate.shift(UP * 0.5))
            self.play(Write(grad[:4]))
            vo.wait_until("g")
            self.play(Write(grad[4]), Create(gbox))
        self.clear_scene(grad, gbox, extra=[VGroup(grad, gbox).animate.to_corner(UL, buff=0.4).scale(0.8)])
        self.grad = VGroup(grad, gbox)

    # ------------------------------------------------------------------
    def pressure_map(self):
        H = np.array([-2.4, 0.4])
        L = np.array([2.6, -0.6])

        def p_fn(X, Y):
            return 1.2 * np.exp(-((X - H[0]) ** 2 + (Y - H[1]) ** 2) / 4.0) - 1.2 * np.exp(-((X - L[0]) ** 2 + (Y - L[1]) ** 2) / 4.0)

        def force(p):
            x, y = p[0], p[1]
            gx = gy = 0.0
            for (cx, cy), s in ((H, 1.2), (L, -1.2)):
                e = s * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 4.0)
                gx += e * (-2 * (x - cx) / 4.0)
                gy += e * (-2 * (y - cy) / 4.0)
            return np.array([-gx, -gy, 0.0])

        pmap = heatmap(p_fn, (-7.2, 7.2), (-4.1, 4.1), resolution=150, colormap=pressure_colormap(-1.3, 1.3))
        arrows = ArrowVectorField(force, x_range=[-6.6, 6.6, 0.7], y_range=[-3.6, 2.7, 0.7], color=P_FORCE,
                                  length_func=lambda n: 0.6 * np.tanh(2.0 * n))
        Hl = MathTex(r"\textbf{H}", font_size=60).move_to([*H, 0])
        Ll = MathTex(r"\textbf{L}", font_size=60).move_to([*L, 0])
        note = label(r"$-\nabla p$ points from high pressure to low pressure", font_size=32)
        note.add_background_rectangle(opacity=0.85, buff=0.12).to_edge(DOWN, buff=0.35)

        with self.voiceover(
            "The gradient points uphill, toward higher pressure, so the force points downhill. Fluid gets pushed "
            "<bookmark mark='h'/> from high pressure <bookmark mark='l'/> toward low pressure."
        ) as vo:
            self.play(FadeIn(pmap))
            self.bring_to_back(pmap)
            self.play(Create(arrows, lag_ratio=0.01), run_time=2)
            vo.wait_until("h")
            self.play(Write(Hl))
            vo.wait_until("l")
            self.play(Write(Ll), FadeIn(note))
        with self.voiceover("It's exactly why wind blows from high-pressure regions toward low-pressure ones."):
            pass
        self.play(FadeOut(VGroup(arrows, Hl, Ll, note)), FadeOut(pmap))

    # ------------------------------------------------------------------
    def vortex_payoff(self):
        c = np.array([-3.0, -0.4, 0])
        a = 1.6  # core radius
        omega0 = 1.0

        def vel(p):
            d = p - c
            r2 = d[0] ** 2 + d[1] ** 2 + 1e-9
            f = omega0 * a**2 / r2 * (1 - np.exp(-r2 / a**2))
            return f * np.array([-d[1], d[0], 0.0])

        def p_fn(X, Y):
            r2 = (X - c[0]) ** 2 + (Y - c[1]) ** 2
            return -np.exp(-r2 / (1.4 * a) ** 2)

        pmap = heatmap(p_fn, (-7.2, 1.2), (-4.1, 3.0), resolution=140, colormap=pressure_colormap(-1.0, 0.25))
        field = ArrowVectorField(vel, x_range=[-6.6, 0.8, 0.6], y_range=[-3.7, 2.6, 0.6], color=C.VELOCITY,
                                 length_func=lambda n: 0.5 * np.tanh(1.5 * n)).set_opacity(0.6)
        theta = ValueTracker(0.0)
        R = 1.7

        def orb_pos():
            return c + R * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0])

        orb = always_redraw(lambda: Dot(orb_pos(), color=WHITE, radius=0.1))
        acc = always_redraw(lambda: Arrow(orb_pos(), orb_pos() + 0.95 * (c - orb_pos()) / R, buff=0, color=C.ADVECT, stroke_width=6))
        push = always_redraw(lambda: Arrow(orb_pos() + 0.12 * (orb_pos() - c) / R + 1.1 * (orb_pos() - c) / R,
                                           orb_pos() + 0.12 * (orb_pos() - c) / R, buff=0, color=P_FORCE, stroke_width=6))
        low = label(r"low $p$", font_size=30).move_to(c + DOWN * 0.35)

        eqs = VGroup(
            MathTex(r"\rho\,", r"(\vu\cdot\nabla)\vu", r"=", r"-\nabla p", font_size=44),
            MathTex(r"\rho\,", r"{|\vu|^2 \over r}", r"=", r"{\partial p \over \partial r}", font_size=44),
            label(r"pressure must \emph{increase} outward,\\so it is lowest at the center", font_size=30),
        ).arrange(DOWN, buff=0.5).move_to(RIGHT * 4.2 + UP * 0.3)
        eqs[0][1].set_color(C.ADVECT)
        eqs[0][3].set_color(C.PRESSURE)
        eqs[1][1].set_color(C.ADVECT)
        eqs[1][3].set_color(C.PRESSURE)
        inward = label(r"(inward components)", font_size=26, color=C.DIM).next_to(eqs[1], DOWN, buff=0.12)
        eqs[2].next_to(inward, DOWN, buff=0.45)

        with self.voiceover(
            "And remember those swirls with low pressure in their cores? Now we can see why. For fluid to move in a circle, "
            "something must supply the inward, <bookmark mark='c'/> centripetal acceleration we just found. "
            "<bookmark mark='p'/> The only candidate is pressure, so the pressure has to drop toward the center."
        ) as vo:
            self.play(FadeIn(pmap), Create(field, lag_ratio=0.01), FadeOut(self.grad), run_time=2)
            self.add(orb)
            self.play(theta.animate.increment_value(2.0), run_time=1.5, rate_func=linear)
            vo.wait_until("c")
            self.add(acc)
            self.play(theta.animate.increment_value(1.5), Write(eqs[0][:2]), run_time=1.5, rate_func=linear)
            vo.wait_until("p")
            self.add(push)
            self.play(theta.animate.increment_value(1.5), Write(eqs[0][2:]), FadeIn(low), run_time=1.5, rate_func=linear)
            self.play(theta.animate.increment_value(vo.remaining()), run_time=vo.remaining(), rate_func=linear)

        with self.voiceover(
            "Comparing the inward parts, the pressure gradient balances density times speed squared over radius. "
            "<bookmark mark='w'/> It's why the core of a tornado is a region of very low pressure, and why the water's surface "
            "dips down in the middle of a whirlpool."
        ) as vo:
            self.play(TransformFromCopy(eqs[0], eqs[1]), FadeIn(inward), theta.animate.increment_value(1.5),
                      run_time=1.5, rate_func=linear)
            self.play(FadeIn(eqs[2]), theta.animate.increment_value(1.5), run_time=1.5, rate_func=linear)
            self.play(theta.animate.increment_value(vo.remaining()), run_time=vo.remaining(), rate_func=linear)
        self.clear_scene()
