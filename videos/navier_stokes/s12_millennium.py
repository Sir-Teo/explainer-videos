from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import caption_box, label


class VortexTube(VGroup):
    """A spinning cylinder of fluid seen from the side; stretch factor s keeps volume fixed."""

    def __init__(self, length=3.0, radius=0.8, n_lines=10, color=C.VORTICITY, **kw):
        super().__init__(**kw)
        self.L0, self.r0, self.n, self.color = length, radius, n_lines, color
        self.s = ValueTracker(1.0)
        self.phase = 0.0
        self.base_rate = 1.4
        self.add(always_redraw(self._draw))

    def _draw(self):
        s = self.s.get_value()
        L, r = self.L0 * s, self.r0 / np.sqrt(s)
        g = VGroup()
        body = Rectangle(width=L, height=2 * r, stroke_width=0, fill_color=self.color, fill_opacity=0.18)
        g.add(body)
        g.add(Line([-L / 2, r, 0], [L / 2, r, 0], color=self.color, stroke_width=3))
        g.add(Line([-L / 2, -r, 0], [L / 2, -r, 0], color=self.color, stroke_width=3))
        for k in range(self.n):
            th = self.phase + 2 * PI * k / self.n
            y = r * np.cos(th)
            front = np.sin(th) > 0
            g.add(Line([-L / 2, y, 0], [L / 2, y, 0], color=self.color if front else GREY_D,
                       stroke_width=2.5 if front else 1.5, stroke_opacity=0.95 if front else 0.4))
        g.add(Ellipse(width=0.5 * r, height=2 * r, color=self.color, stroke_width=3).move_to([L / 2, 0, 0]))
        g.add(DashedVMobject(Ellipse(width=0.5 * r, height=2 * r, color=self.color, stroke_width=2), num_dashes=14).move_to([-L / 2, 0, 0]))
        return g.move_to(self.get_center() if len(self.submobjects) else ORIGIN)

    def tick(self, dt):
        s = self.s.get_value()
        self.phase += self.base_rate * s * dt  # angular speed ~ 1/r^2 ~ s


class MillenniumProblem(VoiceoverScene):
    def construct(self):
        self.question()
        self.vorticity_equation()
        self.stretching()
        self.two_vs_three()
        self.what_we_know()

    # ------------------------------------------------------------------
    def question(self):
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=6.6, y_length=4.4,
                  axis_config={"include_ticks": False, "stroke_color": GREY_B}).move_to(LEFT * 3.0 + DOWN * 0.6)
        xl = MathTex("t", font_size=36).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"\max_{\vx} |\vu|", font_size=34).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        smooth = ax.plot(lambda t: 1.4 + 0.6 * np.exp(-0.3 * t) * np.sin(2.4 * t) + 0.2 * np.sin(5 * t) * np.exp(-0.5 * t),
                         x_range=[0, 4.9], color=C.VISCOUS, stroke_width=4)
        T = 3.2
        blow = ax.plot(lambda t: min(4.9, 1.4 + 0.35 / (T - t) - 0.35 / T), x_range=[0, T - 0.072], color=C.PRESSURE, stroke_width=4)
        tline = DashedLine(ax.c2p(T, 0), ax.c2p(T, 5), color=GREY_B)
        tl = MathTex("T^*", font_size=34).next_to(ax.c2p(T, 0), DOWN, buff=0.15)
        l1 = label(r"smooth forever?", font_size=32, color=C.VISCOUS).next_to(ax.c2p(4.9, 1.4), RIGHT, buff=0.15)
        l2 = label(r"blow-up in finite time?", font_size=32, color=C.PRESSURE).next_to(ax.c2p(T, 4.6), RIGHT, buff=0.2)
        q = label(r"Smooth flow in 3D, finite energy. Does it stay smooth forever?", font_size=34).to_edge(UP, buff=0.5)

        with self.voiceover(
            "Here's the question. Start with a smooth, well-behaved flow in three dimensions, with finite total energy. "
            "Let it evolve according to Navier–Stokes. <bookmark mark='s'/> Does it remain smooth forever?"
        ) as vo:
            self.play(FadeIn(q))
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("s")
            self.play(Create(smooth), run_time=2)
            self.play(FadeIn(l1))

        with self.voiceover(
            "Or could the velocity somewhere <bookmark mark='b'/> blow up to infinity in a finite amount of time, a singularity, "
            "where the equations themselves stop making sense?"
        ) as vo:
            vo.wait_until("b")
            self.play(Create(blow), run_time=2)
            self.play(Create(tline), FadeIn(tl), FadeIn(l2))

        prize = VGroup(
            MathTex(r"\$1{,}000{,}000", font_size=72, color=YELLOW),
            label(r"Clay Mathematics Institute\\Millennium Prize Problem (2000)", font_size=30),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 4.75 + UP * 1.1)
        prize_bg = BackgroundRectangle(prize, fill_opacity=0.9, buff=0.3).set_stroke(YELLOW, 2, opacity=1)
        with self.voiceover(
            "For decades, nobody knew. <bookmark mark='c'/> In 2000, the Clay Mathematics Institute made this one of its seven "
            "Millennium Prize Problems, offering a million dollars for a proof either way."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(prize_bg), Write(prize[0]))
            self.play(FadeIn(prize[1]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def vorticity_equation(self):
        wdef = MathTex(r"\boldsymbol{\omega}", r"=", r"\nabla \times \vu", font_size=52)
        wdef[0].set_color(C.VORTICITY)
        wdef.to_edge(UP, buff=0.5)
        spin = label(r"local spin of the fluid", font_size=30, color=C.VORTICITY).next_to(wdef, DOWN, buff=0.15)

        # Paddle wheel in shear flow
        paddle = VGroup(Line(LEFT * 0.45, RIGHT * 0.45, stroke_width=4), Line(UP * 0.45, DOWN * 0.45, stroke_width=4),
                        Dot(radius=0.06)).move_to(RIGHT * 4.6 + DOWN * 2.2)
        shear = VGroup(*[Arrow([3.4, y, 0], [3.4 + 0.9 + 0.8 * (y + 2.2), y, 0], buff=0, color=C.VELOCITY, stroke_width=3,
                               max_tip_length_to_length_ratio=0.2) for y in np.linspace(-3.1, -1.3, 5)])
        paddle.add_updater(lambda m, dt: m.rotate(-1.2 * dt))

        with self.voiceover(
            "To see what's at stake, look at vorticity, omega, the curl of the velocity. <bookmark mark='s'/> It measures how fast "
            "the fluid is spinning locally, like a tiny paddle wheel dropped into the flow."
        ) as vo:
            self.play(Write(wdef))
            vo.wait_until("s")
            self.play(FadeIn(spin), FadeIn(shear), FadeIn(paddle))

        start = MathTex(r"\nabla\times\Big[", r"{\partial \vu \over \partial t}", r"+", r"(\vu\cdot\nabla)\vu", r"=",
                        r"-{1\over\rho}\nabla p", r"+", r"\nu\nabla^2\vu", r"\Big]", font_size=40)
        for i, col in {1: C.TIME, 3: C.ADVECT, 5: C.PRESSURE, 7: C.VISCOUS}.items():
            start[i].set_color(col)
        start.next_to(spin, DOWN, buff=0.45)
        rows = VGroup(
            MathTex(r"\nabla \times \nabla p", r"=", r"0", font_size=36),
            MathTex(r"\nabla\times\big[(\vu\cdot\nabla)\vu\big]", r"=", r"(\vu\cdot\nabla)\boldsymbol{\omega}",
                    r"-", r"(\boldsymbol{\omega}\cdot\nabla)\vu", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(start, DOWN, buff=0.4).shift(LEFT * 1.2)
        rows[0][0].set_color(C.PRESSURE)
        rows[1][0].set_color(C.ADVECT)
        note0 = label(r"pressure drops out!", font_size=26, color=C.PRESSURE).next_to(rows[0], RIGHT, buff=0.4)
        note1 = label(r"(vector identities, using $\nabla\cdot\mathbf{u} = 0$)", font_size=24, color=C.DIM).next_to(rows[1], DOWN, buff=0.15).align_to(rows[1], LEFT)

        with self.voiceover(
            "Take the curl of the Navier–Stokes equation. <bookmark mark='p'/> The pressure term disappears, since the curl of a "
            "gradient is always zero. <bookmark mark='a'/> And after some vector calculus, the advection term splits in two."
        ) as vo:
            self.play(FadeOut(VGroup(shear, paddle)), FadeIn(start))
            vo.wait_until("p")
            self.play(Write(rows[0]), FadeIn(note0))
            vo.wait_until("a")
            self.play(Write(rows[1]), FadeIn(note1))

        result = MathTex(
            r"{\partial \boldsymbol{\omega} \over \partial t}", r"+", r"(\vu\cdot\nabla)\boldsymbol{\omega}", r"=",
            r"(\boldsymbol{\omega}\cdot\nabla)\vu", r"+", r"\nu\nabla^2\boldsymbol{\omega}", font_size=54,
        )
        result[0].set_color(C.VORTICITY)
        result[2].set_color(C.ADVECT)
        result[4].set_color(YELLOW)
        result[6].set_color(C.VISCOUS)
        result.to_edge(DOWN, buff=1.3)
        rbox = caption_box(result, color=C.VORTICITY, buff=0.2)
        b1 = Brace(result[0:3], DOWN, buff=0.15)
        t1 = label(r"carried by the flow", font_size=26).next_to(b1, DOWN, buff=0.08)
        b2 = Brace(result[4], DOWN, buff=0.15, color=YELLOW)
        t2 = label(r"vortex stretching", font_size=26, color=YELLOW).next_to(b2, DOWN, buff=0.08)
        b3 = Brace(result[6], DOWN, buff=0.15, color=C.VISCOUS)
        t3 = label(r"viscous smoothing", font_size=26, color=C.VISCOUS).next_to(b3, DOWN, buff=0.08)

        with self.voiceover(
            "The result says that vorticity is <bookmark mark='c'/> carried along by the flow, <bookmark mark='v'/> smoothed by "
            "viscosity, and has one extra term: <bookmark mark='s'/> omega dot del u. This is vortex stretching."
        ) as vo:
            self.play(Write(result), Create(rbox))
            vo.wait_until("c")
            self.play(GrowFromCenter(b1), FadeIn(t1))
            vo.wait_until("v")
            self.play(GrowFromCenter(b3), FadeIn(t3))
            vo.wait_until("s")
            self.play(GrowFromCenter(b2), FadeIn(t2), Indicate(result[4], color=YELLOW))
        self.clear_scene(result, rbox, extra=[VGroup(result, rbox).animate.scale(0.75).to_edge(UP, buff=0.4)])
        self.result = VGroup(result, rbox)

    # ------------------------------------------------------------------
    def stretching(self):
        tube = VortexTube(length=3.2, radius=0.85)
        tube.move_to(DOWN * 0.4)
        tube.add_updater(lambda m, dt: m.tick(dt))
        def pull(sign):
            def make():
                half = tube.L0 * tube.s.get_value() / 2
                start = np.array([sign * (half + 0.2), -0.4, 0])
                return Arrow(start, start + sign * RIGHT * 1.2, buff=0, color=WHITE, stroke_width=5)
            return always_redraw(make)

        pull_l, pull_r = pull(-1), pull(1)
        omega_axis = Arrow(LEFT * 0.4, RIGHT * 0.9, buff=0, color=C.VORTICITY, stroke_width=6).shift(UP * 1.4)
        omega_l = MathTex(r"\boldsymbol{\omega}", font_size=40, color=C.VORTICITY).next_to(omega_axis, RIGHT, buff=0.1)

        readout = VGroup(
            VGroup(label("length", font_size=30), DecimalNumber(1.0, num_decimal_places=1, font_size=34), MathTex(r"\times", font_size=34)),
            VGroup(label("radius", font_size=30), DecimalNumber(1.0, num_decimal_places=2, font_size=34), MathTex(r"\times", font_size=34)),
            VGroup(label("spin rate", font_size=30, color=C.VORTICITY), DecimalNumber(1.0, num_decimal_places=1, font_size=34, color=C.VORTICITY),
                   MathTex(r"\times", font_size=34, color=C.VORTICITY)),
        )
        for row in readout:
            row.arrange(RIGHT, buff=0.2)
        readout.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(DR, buff=0.5)
        readout[0][1].add_updater(lambda m: m.set_value(tube.s.get_value()))
        readout[1][1].add_updater(lambda m: m.set_value(1 / np.sqrt(tube.s.get_value())))
        readout[2][1].add_updater(lambda m: m.set_value(tube.s.get_value()))
        skater = label(r"like a figure skater pulling in their arms", font_size=30, color=GREY_A).to_edge(DOWN, buff=0.45).to_edge(LEFT, buff=0.6)

        with self.voiceover(
            "When a spinning tube of fluid gets stretched along its axis, <bookmark mark='s'/> it gets thinner, and just like a "
            "figure skater pulling in their arms, it spins faster. <bookmark mark='f'/> Faster spin can drive more stretching, "
            "a feedback loop that could, in principle, run away."
        ) as vo:
            self.play(FadeIn(tube), GrowArrow(omega_axis), FadeIn(omega_l), FadeIn(readout))
            vo.wait_until("s")
            self.play(GrowArrow(pull_l), GrowArrow(pull_r))
            self.play(tube.s.animate.set_value(2.3), FadeIn(skater), run_time=4)
            vo.wait_until("f")
            self.play(tube.s.animate.set_value(3.0), run_time=vo.remaining())
        self.wait(1)
        self.clear_scene(self.result)

    # ------------------------------------------------------------------
    def two_vs_three(self):
        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=5.4, y_length=3.6,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.6},
                            axis_config={"stroke_opacity": 0}).move_to(LEFT * 3.7 + DOWN * 0.6)
        swirl = VGroup(*[
            Arc(radius=r, start_angle=a, angle=1.2 * PI, color=C.VELOCITY, stroke_width=3).add_tip(tip_length=0.15, tip_width=0.15)
            .move_to(plane.c2p(x, y))
            for (x, y, r, a) in [(-1.6, 0.6, 0.6, 0), (1.3, -0.5, 0.75, 1.0), (0.6, 1.2, 0.4, 2.0)]
        ])
        dots = VGroup(*[
            VGroup(Circle(0.13, color=C.VORTICITY, stroke_width=3), Dot(radius=0.045, color=C.VORTICITY)).move_to(plane.c2p(x, y))
            for (x, y) in [(-1.6, 0.6), (1.3, -0.5), (0.6, 1.2)]
        ])
        tag2 = label(r"\textbf{2D}: spin axis points out of the plane", font_size=30).next_to(plane, UP, buff=0.3)
        zero = MathTex(r"(\boldsymbol{\omega}\cdot\nabla)\vu", r"=", r"\omega\, {\partial \vu \over \partial z}", r"=", r"0",
                       font_size=42).next_to(plane, DOWN, buff=0.35)
        zero[0].set_color(YELLOW)

        with self.voiceover(
            "In two dimensions, this term is exactly zero. <bookmark mark='o'/> The spin axis always points straight out of the plane, "
            "<bookmark mark='z'/> and nothing varies in that direction, so there's nothing to stretch. <bookmark mark='t'/> That's why "
            "the two-dimensional problem was settled long ago: smooth solutions stay smooth forever."
        ) as vo:
            self.play(Create(plane), Create(swirl), FadeIn(tag2))
            vo.wait_until("o")
            self.play(FadeIn(dots, scale=0.5))
            vo.wait_until("z")
            self.play(Write(zero))
            vo.wait_until("t")
            ok = label(r"2D: proven smooth forever", font_size=30, color=C.VISCOUS).next_to(zero, DOWN, buff=0.25)
            self.play(FadeIn(ok))

        tube = VortexTube(length=2.4, radius=0.7).move_to(RIGHT * 3.9 + DOWN * 0.3)
        tube.add_updater(lambda m, dt: m.tick(dt))
        tag3 = label(r"\textbf{3D}: a battle", font_size=30).move_to(RIGHT * 3.9 + UP * 1.6)
        vs = VGroup(
            label(r"stretching concentrates spin", font_size=28, color=YELLOW),
            label(r"vs.", font_size=28),
            label(r"viscosity smooths it out", font_size=28, color=C.VISCOUS),
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 3.9 + DOWN * 2.4)
        q = label(r"Does viscosity always win?", font_size=40, color=YELLOW).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "In three dimensions it's a battle. <bookmark mark='s'/> Vortex stretching tries to concentrate the spin into ever smaller, "
            "ever more intense regions; <bookmark mark='v'/> viscosity tries to smooth it all out. <bookmark mark='q'/> Does viscosity "
            "always win?"
        ) as vo:
            self.play(FadeIn(tube), FadeIn(tag3))
            vo.wait_until("s")
            self.play(FadeIn(vs[0]), tube.s.animate.set_value(2.0), run_time=2)
            vo.wait_until("v")
            self.play(FadeIn(vs[1:]), tube.s.animate.set_value(1.4), run_time=2)
            vo.wait_until("q")
            self.play(FadeOut(VGroup(zero, ok, vs)), FadeIn(q, shift=UP * 0.2))
        self.wait(1)
        self.clear_scene()

    # ------------------------------------------------------------------
    def what_we_know(self):
        title = label(r"What we do know (3D)", font_size=44).to_edge(UP, buff=0.6)
        items = VGroup(
            label(r"\textbf{1934, Jean Leray:} weak (generalized) solutions exist for all time", font_size=32),
            label(r"Smooth solutions exist, at least for a short time", font_size=32),
            label(r"\textbf{1982, Caffarelli--Kohn--Nirenberg:} any singularities\\must be extremely rare, confined to tiny sets", font_size=32),
            label(r"\textbf{Long open:} do smooth solutions stay smooth forever?", font_size=36, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=0.7)
        for it in items[:3]:
            it.add(Dot(color=GREY_B).next_to(it, LEFT, buff=0.25).align_to(it, UP).shift(DOWN * 0.12))
        with self.voiceover(
            "We do know a lot. <bookmark mark='l'/> In 1934, Jean Leray proved that weak, generalized solutions always exist. "
            "<bookmark mark='s'/> Smooth solutions are known to exist at least for a while. <bookmark mark='c'/> And if singularities "
            "ever do form, they must be extremely rare, confined to vanishingly small sets in space and time. "
            "<bookmark mark='o'/> But for nearly a century, whether they can happen at all remained unknown."
        ) as vo:
            self.play(Write(title))
            for i, m in enumerate("lsco"):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2))
        self.wait(1)
        self.clear_scene()
