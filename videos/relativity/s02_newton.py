from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import boxed, label, light_cone, load, mtex, note, st_axes, stack


class Newton(VoiceoverScene):
    def construct(self):
        self.law()
        self.gauss()
        self.poisson()
        self.instant()
        self.masses()

    # ------------------------------------------------------------------
    def law(self):
        M = Dot(ORIGIN, radius=0.28, color=C.MATTER).shift(LEFT * 4.0)
        Ml = MathTex("M", font_size=34, color=C.MATTER).next_to(M, DOWN, buff=0.12)
        arrows = VGroup()
        for r in (1.1, 1.8, 2.6):
            for a in np.linspace(0, 2 * np.pi, 16, endpoint=False) + (0.2 if r > 2 else 0):
                u = np.array([math.cos(a), math.sin(a), 0])
                L = min(0.5, 0.9 / r**2 * 1.4)
                p = M.get_center() + r * u
                arrows.add(Arrow(p, p - L * u, buff=0, color=C.POTENTIAL, stroke_width=3,
                                 max_tip_length_to_length_ratio=0.35))
        law = mtex(r"\mathbf{F}", r"=", r"-\frac{G M m}{r^2}\,\hat{\mathbf r}", font_size=44)
        field = mtex(r"\mathbf{g}", r"=", r"-\nabla\Phi", r",\qquad", r"\Phi", r"=", r"-\frac{GM}{r}", font_size=40)
        for m in (law, field):
            m.set_color_by_tex(r"\Phi", C.POTENTIAL)
        law[0].set_color(C.POTENTIAL)
        field[0].set_color(C.POTENTIAL)
        col = VGroup(law, field).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([2.6, 0.6, 0])
        cap = label(r"Newton, 1687", font_size=28, color=GREY_A).next_to(col, UP, buff=0.5).align_to(col, LEFT)
        with self.voiceover(
            "Let's begin with the theory Einstein had to replace. <bookmark mark='l'/> In Newton's theory, a mass M pulls "
            "on a mass m with a force proportional to both masses and inversely proportional to the distance squared. "
            "<bookmark mark='f'/> It's cleaner to think of M as creating a field: at every point in space there's an "
            "arrow, the gravitational field g, telling any object placed there how to accelerate. <bookmark mark='p'/> "
            "And that field is the downhill slope of a single number at each point, the potential, phi."
        ) as vo:
            self.play(FadeIn(M), FadeIn(Ml), FadeIn(cap))
            vo.wait_until("l")
            self.play(Write(law))
            vo.wait_until("f")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.01), run_time=2)
            vo.wait_until("p")
            self.play(Write(field))
        self.M, self.Ml, self.arrows = M, Ml, arrows
        self.play(FadeOut(VGroup(law, field, cap)))

    # ------------------------------------------------------------------
    def gauss(self):
        M, arrows = self.M, self.arrows
        c0 = M.get_center()
        w = ValueTracker(0.0)

        def surface_pts(n=200):
            a = np.linspace(0, 2 * np.pi, n)
            wob = w.get_value()
            r = 1.8 + wob * (0.45 * np.sin(3 * a) + 0.3 * np.cos(5 * a + 1))
            return c0 + np.stack([r * np.cos(a), 0.92 * r * np.sin(a), 0 * a], 1)

        surf = always_redraw(lambda: VMobject(stroke_color=C.METRIC, stroke_width=3.5).set_points_smoothly(surface_pts()))
        flux = mtex(r"\oint \mathbf{g}\cdot d\mathbf{A}", r"=", r"-4\pi G\,M_{\text{inside}}", font_size=44)
        flux[0].set_color(C.POTENTIAL)
        flux[2].set_color(C.MATTER)
        flux.move_to([2.4, 1.6, 0])
        why = VGroup(label(r"area grows like $r^2$,", font_size=28), label(r"field falls like $1/r^2$:", font_size=28),
                     label(r"every closed surface catches the same flux", font_size=28)).arrange(DOWN, buff=0.12)
        why.next_to(flux, DOWN, buff=0.5)
        with self.voiceover(
            "The inverse square law has a beautiful consequence, known as Gauss's law. <bookmark mark='s'/> Surround the "
            "mass with any closed surface and add up how much field passes through it, the flux. For a sphere, the area "
            "grows like r squared while the field weakens like one over r squared, so the flux doesn't depend on the size. "
            "<bookmark mark='w'/> And it doesn't depend on the shape either: any surface enclosing the mass catches the "
            "same flux, minus four pi G times the mass inside."
        ) as vo:
            vo.wait_until("s")
            self.add(surf)
            self.play(Create(surf.copy()), run_time=0.8)
            self.play(Write(flux), FadeIn(why))
            vo.wait_until("w")
            self.play(w.animate.set_value(1.0), run_time=2.5)
            self.play(w.animate.set_value(0.4), run_time=1.5)
        surf.clear_updaters()
        self.surf, self.flux = surf, flux
        self.play(FadeOut(why))

    # ------------------------------------------------------------------
    def poisson(self):
        rows = stack(
            mtex(r"\oint \mathbf{g}\cdot d\mathbf{A}", r"=", r"-4\pi G \int \rho\, dV", font_size=40),
            mtex(r"\int \nabla\cdot\mathbf{g}\; dV", r"=", r"-4\pi G \int \rho\, dV", font_size=40),
            mtex(r"\nabla\cdot\mathbf{g}", r"=", r"-4\pi G\,\rho", font_size=40),
            mtex(r"\nabla^2\Phi", r"=", r"4\pi G\,\rho", font_size=48),
            buff=0.45,
        )
        for r in rows:
            r[0].set_color(C.POTENTIAL)
            r[2].set_color(C.MATTER)
        rows.move_to([1.4, -0.1, 0])
        whys = VGroup(
            note(r"divergence theorem", font_size=24).next_to(rows[1], RIGHT, buff=0.3),
            note(r"true for every region", font_size=24).next_to(rows[2], RIGHT, buff=0.3),
            note(r"$\mathbf g = -\nabla\Phi$", font_size=24).next_to(rows[3], RIGHT, buff=0.3),
        )
        self.play(FadeOut(self.flux), FadeIn(rows[0]))
        with self.voiceover(
            "Spread the mass out with a density rho, and Gauss's law turns into a differential equation. "
            "<bookmark mark='a'/> By the divergence theorem, the flux through the surface is the integral of the "
            "divergence of g over the inside. <bookmark mark='b'/> Since that holds for every region, however small, the "
            "integrands must match: the divergence of g is minus four pi G rho. <bookmark mark='c'/> And since g is minus "
            "the gradient of phi, we get Poisson's equation: the Laplacian of phi equals four pi G rho."
        ) as vo:
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[2]))
        box = SurroundingRectangle(rows[3], color=C.POTENTIAL, buff=0.2, corner_radius=0.1)
        b1 = Brace(rows[3][0], DOWN, color=C.POTENTIAL)
        b1l = label(r"second derivatives\\of the field", font_size=24, color=C.POTENTIAL).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(rows[3][2], DOWN, color=C.MATTER)
        b2l = label(r"matter", font_size=24, color=C.MATTER).next_to(b2, DOWN, buff=0.1)
        with self.voiceover(
            "<bookmark mark='a'/> This is Newtonian gravity in one line. Notice its shape: second derivatives of a "
            "field on the left, <bookmark mark='m'/> the density of matter on the right. Keep that shape in mind. "
            "Einstein's equation will have exactly the same skeleton."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(VGroup(rows[:3], whys)), rows[3].animate.move_to([2.4, 1.2, 0]))
            box.move_to(rows[3])
            b1.next_to(rows[3][0], DOWN, buff=0.15)
            b1l.next_to(b1, DOWN, buff=0.1)
            b2.next_to(rows[3][2], DOWN, buff=0.15)
            b2l.next_to(b2, DOWN, buff=0.1)
            self.play(Create(box), GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("m")
            self.play(GrowFromCenter(b2), FadeIn(b2l))
        self.wait(0.4)
        self.poisson_eq = VGroup(rows[3], box)
        self.clear_scene(self.poisson_eq)

    # ------------------------------------------------------------------
    def instant(self):
        consts = load("consts")
        t_sun = float(consts["t_sun"])
        assert abs(t_sun - 499) < 1
        eq = self.poisson_eq
        no_t = label(r"no time derivative: a change in $\rho$ changes $\Phi$ everywhere \emph{at once}", font_size=28,
                     color=GREY_A)
        g = st_axes(x_range=(-0.6, 3.4), t_range=(0, 4.3), unit=1.25, x_label=r"x", t_label=r"ct")
        ax = g.ax
        g.to_edge(LEFT, buff=0.9).shift(DOWN * 0.35)
        self.play(eq.animate.scale(0.75).to_corner(UR, buff=0.4))
        no_t.next_to(eq, DOWN, buff=0.25).to_edge(RIGHT, buff=0.4)
        D, t0 = 2.5, 1.4  # Earth at 2.5 units (= 499 light seconds); the Sun vanishes at ct = 1.4
        sun = Line(ax.c2p(0, 0), ax.c2p(0, t0), color=C.MATTER, stroke_width=6)
        earth = Line(ax.c2p(D, 0), ax.c2p(D, 4.3), color=C.METRIC, stroke_width=5)
        sl = label(r"Sun", font_size=26, color=C.MATTER).next_to(ax.c2p(0, 0.4), LEFT, buff=0.15)
        el = label(r"Earth", font_size=26, color=C.METRIC).next_to(ax.c2p(D, 0.4), RIGHT, buff=0.15)
        ev = Dot(ax.c2p(0, t0), radius=0.08, color=WHITE)
        evl = label(r"the Sun\\vanishes", font_size=24).next_to(ev, LEFT, buff=0.15)
        newton = DashedLine(ax.c2p(0, t0), ax.c2p(D, t0), color=C.POTENTIAL, stroke_width=3)
        nl = label(r"Newton: felt instantly", font_size=24, color=C.POTENTIAL).next_to(newton, UP, buff=0.08)
        tip = ax.c2p(0, t0)
        cone = VGroup(Polygon(tip, ax.c2p(-0.6, t0 + 0.6), ax.c2p(-0.6, 4.3), ax.c2p(4.3 - t0, 4.3), stroke_width=0,
                              fill_color=C.LIGHT, fill_opacity=0.15),
                      Line(tip, ax.c2p(-0.6, t0 + 0.6), color=C.LIGHT, stroke_width=2))
        ray = Line(ax.c2p(0, t0), ax.c2p(D, t0 + D), color=C.LIGHT, stroke_width=3)
        arrive = Dot(ax.c2p(D, t0 + D), radius=0.08, color=C.LIGHT)
        rl = label(r"light: 8 min 19 s later", font_size=24, color=C.LIGHT).next_to(arrive, RIGHT, buff=0.15)
        sr = label(r"Special relativity (1905): no influence travels faster than light", font_size=28, color=C.LIGHT)
        sr.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "But there's a problem hiding in that equation. <bookmark mark='t'/> It has no time in it. If the density "
            "rho changes here, the potential phi changes everywhere in the universe at the same instant. "
            "<bookmark mark='d'/> Draw it on a spacetime diagram, with space across and time up. Here's the Sun's history, "
            "and here's the Earth's, about five hundred light seconds away. <bookmark mark='v'/> Imagine, as a thought "
            "experiment, that the Sun suddenly vanished. <bookmark mark='n'/> In Newton's theory, the Earth would feel the "
            "change at that very moment. <bookmark mark='c'/> But in 1905 Einstein's special relativity established that "
            "no influence can travel faster than light: the news of anything happening at the Sun can't reach us sooner "
            "than eight minutes and nineteen seconds later."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(no_t))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(g[1:]))
            self.play(Create(sun), Create(earth), FadeIn(sl), FadeIn(el))
            vo.wait_until("v")
            self.play(FadeIn(ev), FadeIn(evl))
            vo.wait_until("n")
            self.play(Create(newton), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(cone), Create(ray), FadeIn(sr))
            self.play(FadeIn(arrive), FadeIn(rl))
        with self.voiceover(
            "So Newton's gravity can't be the final word. A relativistic theory of gravity has to be a field theory "
            "with time in it, where changes spread out no faster than light."
        ):
            self.play(Indicate(newton, color=RED))
        self.clear_scene()

    # ------------------------------------------------------------------
    def masses(self):
        eqs = VGroup(
            mtex(r"\mathbf F", r"=", r"m_{G}\,\mathbf g", font_size=42),
            mtex(r"\mathbf F", r"=", r"m_{I}\,\mathbf a", font_size=42),
            mtex(r"\mathbf a", r"=", r"\frac{m_G}{m_I}\,\mathbf g", font_size=42),
        ).arrange(DOWN, buff=0.45)
        eqs[0][2].set_color(C.POTENTIAL)
        eqs[1][2].set_color(C.METRIC)
        eqs[2][2].set_color(WHITE)
        eqs.move_to([-3.6, 0.6, 0])
        tags = VGroup(
            label(r"gravitational mass: how hard gravity pulls", font_size=24, color=C.POTENTIAL),
            label(r"inertial mass: how hard it is to accelerate", font_size=24, color=C.METRIC),
        )
        tags[0].next_to(eqs[0], RIGHT, buff=0.4)
        tags[1].next_to(eqs[1], RIGHT, buff=0.4)
        # the fall: two different bodies, identical motion
        ground = Line([1.2, -3.2, 0], [6.4, -3.2, 0], color=GREY_B)
        t = ValueTracker(0.0)

        def body(x, r, color):
            return always_redraw(lambda: Circle(radius=r, color=color, fill_opacity=0.7, stroke_width=2).move_to(
                [x, 1.0 - 3.95 * t.get_value() ** 2 + r - 0.25, 0]))

        hammer = body(2.8, 0.3, GREY_B)
        feather = body(4.8, 0.1, WHITE)
        hl = label(r"hammer", font_size=24).move_to([2.8, -3.55, 0])
        fl = label(r"feather", font_size=24).move_to([4.8, -3.55, 0])
        apollo = note(r"(Apollo 15, David Scott on the Moon, 2 August 1971)", font_size=22).move_to([3.8, 2.5, 0])
        tests = VGroup(
            mtex(r"\Big|\tfrac{m_G}{m_I} - 1\Big| \lesssim", font_size=32),
            VGroup(label(r"Eötvös (1908):", font_size=26), mtex(r"\text{a few} \times 10^{-9}", font_size=30)).arrange(RIGHT),
            VGroup(label(r"MICROSCOPE satellite (2022):", font_size=26), mtex(r"\sim 10^{-15}", font_size=30)).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.4, -2.4, 0])
        with self.voiceover(
            "The second puzzle is subtler, and it turned out to be the key. Mass plays two different roles in Newton's "
            "theory. <bookmark mark='g'/> It measures how strongly gravity pulls on an object: the gravitational mass. "
            "<bookmark mark='i'/> And it measures how hard the object is to accelerate: the inertial mass. "
            "<bookmark mark='a'/> Put them together, and the acceleration is the ratio of the two times g."
        ) as vo:
            vo.wait_until("g")
            self.play(Write(eqs[0]), FadeIn(tags[0]))
            vo.wait_until("i")
            self.play(Write(eqs[1]), FadeIn(tags[1]))
            vo.wait_until("a")
            self.play(Write(eqs[2]))
        self.play(FadeOut(tags))
        with self.voiceover(
            "Nothing in Newton's theory says the two must be equal. But every experiment says they are. "
            "<bookmark mark='f'/> On the Moon, an astronaut dropped a hammer and a feather, and they landed together. "
            "<bookmark mark='e'/> Torsion balances in Budapest showed the ratio is the same for every material to a few "
            "parts in a billion, and a satellite experiment has now pushed that to about one part in a million billion. "
            "Everything falls the same way, whatever it's made of."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(ground), FadeIn(hl), FadeIn(fl), FadeIn(apollo))
            self.add(hammer, feather)
            self.play(t.animate.set_value(1.0), run_time=1.6, rate_func=lambda x: x)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(x) for x in tests], lag_ratio=0.4), run_time=2)
        hammer.clear_updaters()
        feather.clear_updaters()
        punch = label(r"Not a coincidence: a clue. \ Falling is a property of \emph{spacetime}, not of what falls.",
                      font_size=30, color=C.CURVATURE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "For Newton, this was a coincidence. For Einstein, it was a clue. If every object falls along exactly the same "
            "path, regardless of its mass or composition, then perhaps the path isn't something the object chooses. "
            "<bookmark mark='p'/> Perhaps falling is a property of space and time themselves."
        ) as vo:
            self.play(Circumscribe(eqs[2], color=C.CURVATURE))
            vo.wait_until("p")
            self.play(FadeOut(tests), FadeIn(punch))
        self.wait(0.5)
        self.clear_scene()
