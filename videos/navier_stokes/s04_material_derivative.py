from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import caption_box, label

# Converging channel ("nozzle"):  half-height h(x), flow rate Q.
YC = 0.35
H1, H2 = 1.75, 0.62
Q = 1.45


def h(x):
    return H2 + (H1 - H2) * (1 - np.tanh(0.9 * x)) / 2


def dh(x):
    return -(H1 - H2) * 0.45 / np.cosh(0.9 * x) ** 2


def nozzle_flow(p):
    """Exactly divergence-free: stream function psi = Q * (y - YC) / h(x)."""
    x, y = p[0], p[1] - YC
    u = Q / h(x)
    v = Q * y * dh(x) / h(x) ** 2
    return np.array([u, v, 0.0])


ADV_PARTS_COLOR = C.ADVECT


class MaterialDerivative(VoiceoverScene):
    def construct(self):
        self.nozzle_puzzle()
        self.derivation()
        self.rotation_picture()
        self.nonlinearity()

    # ------------------------------------------------------------------
    def nozzle_puzzle(self):
        top = ParametricFunction(lambda t: [t, YC + h(t), 0], t_range=[-6.8, 6.8], color=GREY_B, stroke_width=5)
        bot = ParametricFunction(lambda t: [t, YC - h(t), 0], t_range=[-6.8, 6.8], color=GREY_B, stroke_width=5)
        arrows = VGroup()
        for x in np.arange(-6.2, 6.3, 0.8):
            for frac in (-0.62, -0.31, 0.0, 0.31, 0.62):
                p = np.array([x, YC + frac * h(x), 0])
                v = nozzle_flow(p)
                arrows.add(Arrow(p - 0.17 * v, p + 0.17 * v, buff=0, color=C.VELOCITY, stroke_width=3,
                                 max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=8))
        steady = label(r"Steady flow: the picture never changes", font_size=34).to_corner(UL, buff=0.45)
        clock_t = ValueTracker(0)
        clock = VGroup(MathTex("t =", font_size=36), DecimalNumber(0, num_decimal_places=1, font_size=36))
        clock.arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.45)
        clock[1].add_updater(lambda m: m.set_value(clock_t.get_value()))

        with self.voiceover(
            "Here's a puzzle. Water flows steadily through a pipe that narrows. 'Steady' means the picture never "
            "changes: at any fixed spot, the velocity now is the same as the velocity <bookmark mark='m'/> a minute from now."
        ) as vo:
            self.play(Create(top), Create(bot), run_time=1.5)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.01), FadeIn(steady), run_time=2.5)
            vo.wait_until("m")
            self.add(clock)
            self.play(clock_t.animate.set_value(60), run_time=vo.remaining(), rate_func=linear)

        probe_pt = np.array([3.6, YC + 0.0, 0])
        probe = VGroup(Circle(0.16, color=WHITE, stroke_width=3), Line(LEFT * 0.26, RIGHT * 0.26, stroke_width=2),
                       Line(UP * 0.26, DOWN * 0.26, stroke_width=2)).move_to(probe_pt)
        probe_lab = label("fixed point", font_size=28).move_to([probe_pt[0], YC - h(probe_pt[0]) - 0.35, 0])
        dudt = MathTex(r"{\partial \vu \over \partial t}", r"=", r"0", font_size=48)
        dudt[0].set_color(C.TIME)
        dudt.next_to(clock, DOWN, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "So if you take the time derivative of the velocity field at a fixed point, "
            "<bookmark mark='d'/> partial u, partial t, you get zero. Everywhere."
        ) as vo:
            self.play(FadeIn(probe, scale=0.5), FadeIn(probe_lab))
            self.play(clock_t.animate.set_value(75), run_time=1.5, rate_func=linear)
            vo.wait_until("d")
            self.play(Write(dudt))

        # Parcel riding the centerline.
        parcel = Dot(radius=0.13, color=WHITE).set_fill(C.VELOCITY, 1).set_stroke(WHITE, 2)
        parcel.move_to([-6.4, YC, 0])
        p_arrow = always_redraw(
            lambda: Arrow(parcel.get_center(), parcel.get_center() + 0.55 * nozzle_flow(parcel.get_center()),
                          buff=0, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        )
        speed = VGroup(label("parcel speed:", font_size=34), DecimalNumber(0.0, num_decimal_places=2, font_size=36))
        speed.arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.6)
        speed[1].add_updater(lambda m: m.set_value(np.linalg.norm(nozzle_flow(parcel.get_center()))))
        running = {"on": False}

        def move(m, dt):
            if running["on"] and m.get_x() < 5.4:
                m.shift(dt * nozzle_flow(m.get_center()))

        parcel.add_updater(move)
        accel = label(r"accelerating!", font_size=34, color=YELLOW)

        with self.voiceover(
            "And yet, follow a single parcel of water. <bookmark mark='go'/> As it enters the narrow section, it must speed up, "
            "since the same amount of water per second has to squeeze through a smaller gap. "
            "<bookmark mark='acc'/> The parcel is clearly accelerating."
        ) as vo:
            self.play(FadeIn(parcel, scale=0.3), FadeIn(speed), arrows.animate.set_opacity(0.35))
            self.add(p_arrow)
            vo.wait_until("go")
            running["on"] = True
            vo.wait_until("acc")
            accel.next_to(speed, RIGHT, buff=0.5)
            self.play(FadeIn(accel, shift=UP * 0.2))
        self.wait(max(0.0, 2.0))

        two = VGroup(
            VGroup(MathTex(r"{\partial \vu \over \partial t}", font_size=44).set_color(C.TIME),
                   label(r"change at a fixed point", font_size=30)).arrange(DOWN, buff=0.2),
            VGroup(MathTex(r"{D \vu \over D t}", font_size=44).set_color(YELLOW),
                   label(r"change following a parcel", font_size=30)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=1.4).to_edge(DOWN, buff=0.45).shift(LEFT * 1.6)
        newton = label(r"$\leftarrow$ Newton's law needs this one", font_size=28, color=YELLOW)
        with self.voiceover(
            "The resolution: there are two different rates of change here. <bookmark mark='a'/> How the velocity changes at "
            "a fixed location, <bookmark mark='b'/> and how the velocity changes for a particular parcel as it travels. "
            "<bookmark mark='n'/> Newton's law is about the second one."
        ) as vo:
            running["on"] = False
            self.play(FadeOut(speed), FadeOut(accel), FadeOut(dudt))
            vo.wait_until("a")
            self.play(FadeIn(two[0], shift=UP * 0.2), Indicate(probe))
            vo.wait_until("b")
            self.play(FadeIn(two[1], shift=UP * 0.2), Indicate(parcel))
            vo.wait_until("n")
            newton.next_to(two[1], RIGHT, buff=0.3)
            self.play(FadeIn(newton, shift=LEFT * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        # Small picture of a parcel path, top-left.
        path = CubicBezier(LEFT * 2.2 + DOWN * 0.4, LEFT * 1.2 + UP * 0.8, RIGHT * 0.4 + DOWN * 0.8, RIGHT * 1.8 + UP * 0.3)
        path.set_stroke(GREY_B, 2.5).set_style(stroke_opacity=0.8)
        pic = VGroup(path).move_to(UP * 2.75 + LEFT * 3.6)
        pdot = Dot(path.point_from_proportion(0.42), color=WHITE)
        tang = normalize(path.point_from_proportion(0.44) - path.point_from_proportion(0.40))
        pvec = Arrow(pdot.get_center(), pdot.get_center() + 1.1 * tang, buff=0, color=C.VELOCITY, stroke_width=5)
        pos = MathTex(r"\big(x(t),\, y(t)\big)", font_size=34).next_to(pdot, DOWN, buff=0.15)
        vel = MathTex(r"u\big(x(t),\, y(t),\, t\big)", font_size=40).move_to(UP * 2.75 + RIGHT * 2.6)
        vel_note = label(r"horizontal velocity of the parcel", font_size=28, color=C.DIM).next_to(vel, DOWN, buff=0.15)

        with self.voiceover(
            "Let's compute it. Say the parcel's position at time t is <bookmark mark='x'/> x of t, y of t. Its velocity is just "
            "the velocity field <bookmark mark='u'/> evaluated wherever the parcel happens to be."
        ) as vo:
            self.play(Create(path), FadeIn(pdot))
            vo.wait_until("x")
            self.play(Write(pos), GrowArrow(pvec))
            vo.wait_until("u")
            self.play(Write(vel), FadeIn(vel_note))

        # Chain rule ---------------------------------------------------------
        row1 = MathTex(
            r"{d \over dt}\, u\big(x(t), y(t), t\big)",  # 0
            r"=",  # 1
            r"{\partial u \over \partial t}",  # 2
            r"+",  # 3
            r"{\partial u \over \partial x}",  # 4
            r"{dx \over dt}",  # 5
            r"+",  # 6
            r"{\partial u \over \partial y}",  # 7
            r"{dy \over dt}",  # 8
            font_size=44,
        )
        row1.move_to(UP * 0.85)
        row1[2].set_color(C.TIME)
        b_time = Brace(row1[2], DOWN, buff=0.15, color=C.TIME)
        t_time = label(r"time ticks", font_size=28, color=C.TIME).next_to(b_time, DOWN, buff=0.1)
        b_move = Brace(row1[4:9], DOWN, buff=0.15, color=YELLOW)
        t_move = label(r"the parcel moves", font_size=28, color=YELLOW).next_to(b_move, DOWN, buff=0.1)

        with self.voiceover(
            "Focus on the horizontal component, u. As time passes, it changes for two reasons. "
            "<bookmark mark='t'/> Time is ticking, so the field itself may change. <bookmark mark='m'/> And the parcel moves, "
            "so it samples the field at new locations. <bookmark mark='c'/> The chain rule accounts for both."
        ) as vo:
            self.play(FadeOut(vel_note), TransformFromCopy(vel, row1[0]), Write(row1[1]))
            vo.wait_until("t")
            self.play(Write(row1[2]), GrowFromCenter(b_time), FadeIn(t_time))
            vo.wait_until("m")
            self.play(Write(row1[3:]), GrowFromCenter(b_move), FadeIn(t_move))
            vo.wait_until("c")
            self.play(Circumscribe(row1, color=GREY_B, buff=0.15))

        # dx/dt = u, dy/dt = v ------------------------------------------------
        row2 = MathTex(
            r"=", r"{\partial u \over \partial t}", r"+", r"u", r"{\partial u \over \partial x}", r"+", r"v",
            r"{\partial u \over \partial y}", font_size=44,
        )
        row2[1].set_color(C.TIME)
        row2[3:].set_color(C.ADVECT)
        row2[5].set_color(WHITE)
        row2.next_to(row1, DOWN, buff=1.25, aligned_edge=LEFT).align_to(row1[1], LEFT)
        key = MathTex(r"{dx \over dt} = u,", r"\quad", r"{dy \over dt} = v", font_size=38)
        key.set_color(YELLOW)
        key_note = label(r"the parcel moves \emph{with the flow}", font_size=28)
        keyg = VGroup(key, key_note).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here's the key physical input: the parcel moves with the flow. So its rate of change of x is just "
            "<bookmark mark='u'/> u, and its rate of change of y is <bookmark mark='v'/> v."
        ) as vo:
            self.play(FadeIn(keyg, shift=UP * 0.2))
            vo.wait_until("u")
            self.play(Indicate(row1[5]), Indicate(key[0]))
            vo.wait_until("v")
            self.play(Indicate(row1[8]), Indicate(key[2]))
            self.play(FadeOut(VGroup(b_time, t_time, b_move, t_move)))
            self.play(
                TransformFromCopy(row1[1], row2[0]),
                TransformFromCopy(row1[2], row2[1]),
                TransformFromCopy(row1[3], row2[2]),
                TransformFromCopy(row1[5], row2[3]),
                TransformFromCopy(row1[4], row2[4]),
                TransformFromCopy(row1[6], row2[5]),
                TransformFromCopy(row1[8], row2[6]),
                TransformFromCopy(row1[7], row2[7]),
                run_time=2,
            )

        row3 = MathTex(
            r"=", r"{\partial u \over \partial t}", r"+",
            r"\Big(", r"u {\partial \over \partial x}", r"+", r"v {\partial \over \partial y}", r"\Big)", r"u",
            font_size=44,
        )
        row3[1].set_color(C.TIME)
        row3[3:].set_color(C.ADVECT)
        row3.move_to(row2, aligned_edge=LEFT)
        row4 = MathTex(r"=", r"{\partial u \over \partial t}", r"+", r"(\vu \cdot \nabla)", r"u", font_size=44)
        row4[1].set_color(C.TIME)
        row4[3:].set_color(C.ADVECT)
        row4.move_to(row2, aligned_edge=LEFT)
        dot_def = MathTex(
            r"\vu \cdot \nabla", r"=", r"(u, v) \cdot \Big({\partial \over \partial x}, {\partial \over \partial y}\Big)",
            r"=", r"u {\partial \over \partial x} + v {\partial \over \partial y}", font_size=36,
        )
        dot_def[0].set_color(C.ADVECT)
        dot_def.to_edge(DOWN, buff=0.55)
        dd_note = label(r"derivative in the direction of flow, times the speed", font_size=28, color=C.DIM)
        dd_note.next_to(dot_def, UP, buff=0.2)

        with self.voiceover(
            "Pull the velocity out, and what's left is an operator: <bookmark mark='op'/> u times partial partial x, plus v "
            "times partial partial y. That's the derivative in the direction of the flow, scaled by the speed, "
            "which we write compactly as <bookmark mark='dot'/> u dot del."
        ) as vo:
            self.play(FadeOut(keyg))
            self.play(TransformMatchingShapes(row2, row3), run_time=1.5)
            vo.wait_until("op")
            self.play(Indicate(row3[3:8], color=YELLOW))
            self.play(FadeIn(dot_def, shift=UP * 0.2), FadeIn(dd_note))
            vo.wait_until("dot")
            self.play(TransformMatchingShapes(row3, row4), run_time=1.5)

        # Vector form ----------------------------------------------------------
        final = MathTex(
            r"{D \vu \over D t}", r"=", r"{\partial \vu \over \partial t}", r"+", r"(\vu \cdot \nabla)\vu", font_size=60
        )
        final[0].set_color(YELLOW)
        final[2].set_color(C.TIME)
        final[4].set_color(C.ADVECT)
        final.move_to(UP * 0.4)
        fbox = caption_box(final, color=YELLOW, buff=0.3)
        md = label(r"the \emph{material derivative}", font_size=36, color=YELLOW).next_to(fbox, UP, buff=0.25)

        with self.voiceover(
            "The vertical component works exactly the same way, so in vector form: the acceleration of a parcel is "
            "<bookmark mark='a'/> partial u partial t, plus u dot del, u. This combination is called "
            "<bookmark mark='md'/> the material derivative, written with a capital D."
        ) as vo:
            self.play(FadeOut(VGroup(path, pdot, pvec, pos, vel, dot_def, dd_note)), FadeOut(row1))
            vo.wait_until("a")
            self.play(TransformMatchingShapes(row4, final[1:]), run_time=1.5)
            vo.wait_until("md")
            self.play(Write(final[0]), Create(fbox), FadeIn(md, shift=DOWN * 0.2))

        b1 = Brace(final[2], DOWN, buff=0.25, color=C.TIME)
        l1 = label(r"change you'd see\\sitting still", font_size=30, color=C.TIME).next_to(b1, DOWN)
        l1.align_to(b1, RIGHT).shift(RIGHT * 0.3)
        b2 = Brace(final[4], DOWN, buff=0.25, color=C.ADVECT)
        l2 = label(r"change from moving to where\\the flow is different: \emph{advection}", font_size=30, color=C.ADVECT)
        l2.next_to(b2, DOWN).align_to(b2, LEFT)
        with self.voiceover(
            "The first term is the change you'd see sitting still. <bookmark mark='s'/> The second is the change that comes "
            "purely from moving to a place where the flow is different. It's called advection."
        ) as vo:
            self.play(FadeOut(fbox), GrowFromCenter(b1), FadeIn(l1))
            vo.wait_until("s")
            self.play(GrowFromCenter(b2), FadeIn(l2))
        self.clear_scene(final, extra=[final.animate.scale(0.7).to_corner(UL, buff=0.45)])
        self.final = final

    # ------------------------------------------------------------------
    def rotation_picture(self):
        omega = 0.55
        c = np.array([-2.6, -0.55, 0])

        def rot(p):
            d = p - c
            return omega * np.array([-d[1], d[0], 0.0])

        field = ArrowVectorField(
            rot, x_range=[-6.4, 1.2, 0.6], y_range=[-3.8, 2.2, 0.6], color=C.VELOCITY,
            length_func=lambda n: 0.45 * np.tanh(n),
        ).set_opacity(0.35)
        R = 2.2
        ring = Circle(R, color=GREY_C, stroke_width=1.5).move_to(c).set_stroke(opacity=0.7)
        cdot = Dot(c, color=GREY_B, radius=0.05)

        th0, dth = -0.25, 0.75
        P = c + R * np.array([np.cos(th0), np.sin(th0), 0])
        Qp = c + R * np.array([np.cos(th0 + dth), np.sin(th0 + dth), 0])
        scale = 1.5
        uP = Arrow(P, P + scale * rot(P), buff=0, color=C.VELOCITY, stroke_width=6)
        uQ = Arrow(Qp, Qp + scale * rot(Qp), buff=0, color=C.VELOCITY, stroke_width=6)
        uP_copy = DashedVMobject(Arrow(Qp, Qp + scale * rot(P), buff=0, color=GREY_A, stroke_width=4), num_dashes=12)
        diff = Arrow(Qp + scale * rot(P), Qp + scale * rot(Qp), buff=0, color=C.ADVECT, stroke_width=7,
                     max_tip_length_to_length_ratio=0.35)
        lP = MathTex(r"\vu(P)", font_size=34, color=C.VELOCITY).next_to(uP.get_end(), RIGHT, buff=0.1)
        lQ = MathTex(r"\vu(Q)", font_size=34, color=C.VELOCITY).next_to(uQ.get_end(), LEFT, buff=0.12)
        lD = MathTex(r"\Delta \vu", font_size=38, color=C.ADVECT).next_to(diff, UP, buff=0.12).shift(RIGHT * 0.35)
        dP = Dot(P, color=WHITE)
        dQ = Dot(Qp, color=WHITE)
        step = ArcBetweenPoints(P, Qp, angle=dth, color=WHITE, stroke_width=3)

        right = VGroup(
            MathTex(r"{\partial \vu \over \partial t}", r"= 0", font_size=40),
            MathTex(r"(\vu\cdot\nabla)\vu", r"\approx", r"{\Delta \vu \over \Delta t}", font_size=40),
            MathTex(r"|(\vu\cdot\nabla)\vu|", r"=", r"{|\vu|^2 \over r}", font_size=40),
            label(r"the centripetal acceleration!", font_size=32, color=C.ADVECT),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 4.3 + DOWN * 0.4)
        right[0][0].set_color(C.TIME)
        right[1][0].set_color(C.ADVECT)
        right[1][2].set_color(C.ADVECT)
        right[2][0].set_color(C.ADVECT)

        with self.voiceover(
            "Here's a nice way to see that second term. Take a fluid spinning steadily in a circle. "
            "<bookmark mark='z'/> Nothing changes in time, so partial u partial t is zero. But take the velocity "
            "<bookmark mark='p'/> at one point, <bookmark mark='step'/> follow the flow a small step, <bookmark mark='q'/> and "
            "compare with the velocity there. <bookmark mark='d'/> The difference points toward the center."
        ) as vo:
            self.play(Create(field, lag_ratio=0.01), Create(ring), FadeIn(cdot), run_time=2)
            vo.wait_until("z")
            self.play(Write(right[0]))
            vo.wait_until("p")
            self.play(FadeIn(dP), GrowArrow(uP), FadeIn(lP))
            vo.wait_until("step")
            self.play(Create(step), FadeIn(dQ))
            vo.wait_until("q")
            self.play(GrowArrow(uQ), FadeIn(lQ))
            self.play(TransformFromCopy(uP, uP_copy))
            vo.wait_until("d")
            self.play(GrowArrow(diff), FadeIn(lD))
            self.play(Write(right[1]))

        # Animate a parcel going around with its velocity and acceleration arrows.
        theta = ValueTracker(th0 + dth)
        orb = always_redraw(lambda: Dot(c + R * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                                        color=WHITE, radius=0.1))

        def acc_arrow():
            p = c + R * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0])
            return Arrow(p, p + 0.9 * (c - p) / R, buff=0, color=C.ADVECT, stroke_width=6)

        def vel_arrow():
            p = c + R * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0])
            return Arrow(p, p + scale * rot(p), buff=0, color=C.VELOCITY, stroke_width=6)

        orb_a = always_redraw(acc_arrow)
        orb_v = always_redraw(vel_arrow)
        with self.voiceover(
            "So u dot del u is the centripetal acceleration: <bookmark mark='f'/> the speed squared over the radius, "
            "pointing inward, exactly what any object moving in a circle must have."
        ) as vo:
            self.play(FadeOut(VGroup(uP, uQ, uP_copy, diff, lP, lQ, lD, dP, dQ, step)), FadeIn(orb), FadeIn(orb_v), FadeIn(orb_a))
            self.play(theta.animate.increment_value(2 * PI), run_time=vo.until("f") + 1.5, rate_func=linear)
            self.play(Write(right[2]), FadeIn(right[3]), theta.animate.increment_value(2.5), run_time=2.5, rate_func=linear)
            self.play(theta.animate.increment_value(vo.remaining() * omega), run_time=vo.remaining(), rate_func=linear)
        self.clear_scene(self.final)

    # ------------------------------------------------------------------
    def nonlinearity(self):
        final = self.final
        adv = MathTex(r"(", r"\vu", r"\cdot \nabla)", r"\vu", font_size=96).set_color(C.ADVECT)
        adv.move_to(UP * 0.6)
        circ1 = Circle(0.4, color=C.VELOCITY, stroke_width=3).move_to(adv[1])
        circ2 = Circle(0.4, color=C.VELOCITY, stroke_width=3).move_to(adv[3])
        t1 = label(r"the flow\ldots", font_size=34, color=C.VELOCITY).next_to(circ1, DOWN, buff=0.35).shift(LEFT * 0.8)
        t2 = label(r"\ldots carries itself", font_size=34, color=C.VELOCITY).next_to(circ2, DOWN, buff=0.35).shift(RIGHT * 0.6)
        scaling = MathTex(r"\vu \to 2\vu", r"\quad\Longrightarrow\quad", r"(\vu\cdot\nabla)\vu \to 4\,(\vu\cdot\nabla)\vu",
                          font_size=44)
        scaling[2].set_color(C.ADVECT)
        nl = label(r"\textbf{nonlinear}", font_size=44, color=YELLOW)
        VGroup(scaling, nl).arrange(DOWN, buff=0.4).to_edge(DOWN, buff=0.7)

        with self.voiceover(
            "Finally, notice that u appears twice in this term: <bookmark mark='c'/> the flow is carrying itself along. "
            "<bookmark mark='d'/> Double the velocity, and this term quadruples. This makes the equation "
            "<bookmark mark='nl'/> nonlinear, and nearly everything that makes fluids rich, chaotic, and mathematically "
            "difficult traces back to this one term."
        ) as vo:
            self.play(TransformFromCopy(final[4], adv), run_time=1.5)
            self.play(Create(circ1), Create(circ2))
            vo.wait_until("c")
            self.play(FadeIn(t1, shift=UP * 0.2))
            self.play(FadeIn(t2, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Write(scaling))
            vo.wait_until("nl")
            self.play(FadeIn(nl, scale=1.3))
        self.wait(0.5)
        self.clear_scene()
