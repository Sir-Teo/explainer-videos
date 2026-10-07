from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import (
    T_ACC, T_EQ, T_F, T_P, T_RHO, T_VISC, caption_box, div_free, label, ns_equation, template_equation,
)


class FullEquation(VoiceoverScene):
    def construct(self):
        template = template_equation(font_size=44).move_to(UP * 1.6)
        eq = ns_equation(font_size=60).move_to(UP * 0.2)
        div = div_free(font_size=60).next_to(eq, DOWN, buff=0.6)

        with self.voiceover("We have all the pieces. Let's assemble them.") as vo:
            self.play(FadeIn(template, shift=DOWN * 0.2))

        t = template[0]
        with self.voiceover(
            "Density times the acceleration of a parcel, <bookmark mark='acc'/> made of the local change plus the advection term, "
            "<bookmark mark='eq'/> equals <bookmark mark='p'/> the pressure force, <bookmark mark='v'/> plus the viscous force, "
            "<bookmark mark='f'/> plus any external force per unit volume, like gravity, which would be rho times g. "
            "<bookmark mark='d'/> And alongside it, incompressibility."
        ) as vo:
            self.play(TransformFromCopy(t[T_RHO], eq[0]))
            vo.wait_until("acc")
            self.play(TransformFromCopy(t[T_ACC], eq[1:6]), template[1].animate.set_stroke(opacity=0.3), run_time=1.5)
            vo.wait_until("eq")
            self.play(TransformFromCopy(t[T_EQ], eq[6]))
            vo.wait_until("p")
            self.play(TransformFromCopy(t[T_P], eq[7]), template[2].animate.set_stroke(opacity=0.3))
            vo.wait_until("v")
            self.play(TransformFromCopy(t[T_P + 1], eq[8]), TransformFromCopy(t[T_VISC], eq[9]),
                      template[3].animate.set_stroke(opacity=0.3))
            vo.wait_until("f")
            self.play(TransformFromCopy(t[T_VISC + 1], eq[10]), TransformFromCopy(t[T_F], eq[11]),
                      template[4].animate.set_stroke(opacity=0.3))
            g = MathTex(r"(\text{e.g. } \vf = \rho\,\mathbf{g})", font_size=34, color=C.FORCE).next_to(eq[11], UR, buff=0.15)
            self.play(FadeIn(g, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeOut(template), FadeOut(g), Write(div))

        system = VGroup(eq, div)
        brace = Brace(system, LEFT, buff=0.3)
        title = label(r"The incompressible Navier--Stokes equations", font_size=44).to_edge(UP, buff=0.6)
        hist = VGroup(
            label(r"Claude-Louis Navier, 1822", font_size=30, color=C.DIM),
            label(r"George Gabriel Stokes, 1845", font_size=30, color=C.DIM),
        ).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "These are the incompressible Navier–Stokes equations. <bookmark mark='n'/> Claude-Louis Navier first wrote them down "
            "in 1822, starting from a model of forces between molecules, <bookmark mark='s'/> and George Gabriel Stokes rederived "
            "them in 1845 from continuum reasoning much like ours."
        ) as vo:
            self.play(GrowFromCenter(brace), Write(title))
            vo.wait_until("n")
            self.play(FadeIn(hist[0], shift=UP * 0.2))
            vo.wait_until("s")
            self.play(FadeIn(hist[1], shift=UP * 0.2))
        self.play(FadeOut(VGroup(hist, brace)))

        # Divide by rho -------------------------------------------------------
        eq2 = MathTex(
            r"{\partial \vu \over \partial t}", r"+", r"(\vu \cdot \nabla)\vu", r"=", r"-{1 \over \rho}\nabla p", r"+",
            r"\nu \nabla^2 \vu", r"+", r"{\vf \over \rho}", font_size=60,
        )
        for i, col in {0: C.TIME, 2: C.ADVECT, 4: C.PRESSURE, 6: C.VISCOUS, 8: C.FORCE}.items():
            eq2[i].set_color(col)
        eq2.move_to(eq)
        nu = MathTex(r"\nu", r"=", r"{\mu \over \rho}", font_size=44).set_color(C.VISCOUS)
        nu_l = label(r"kinematic viscosity", font_size=30, color=C.VISCOUS)
        nug = VGroup(nu, nu_l).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Often you'll see them divided through by the density. <bookmark mark='nu'/> Then the viscosity divided by the "
            "density becomes nu, the kinematic viscosity, which measures how quickly momentum diffuses through the fluid."
        ) as vo:
            self.play(TransformMatchingShapes(eq, eq2), div.animate.next_to(eq2, DOWN, buff=0.6), run_time=2)
            vo.wait_until("nu")
            self.play(FadeIn(nug, shift=UP * 0.2))
        self.play(FadeOut(nug), FadeOut(title), VGroup(eq2, div).animate.shift(UP * 1.2))

        # Read it like a sentence -------------------------------------------
        def under(mobs, text, color):
            b = Brace(mobs, DOWN, buff=0.15, color=color)
            t = label(text, font_size=26, color=color).next_to(b, DOWN, buff=0.1)
            return VGroup(b, t)

        lhs = under(eq2[0:3], r"acceleration of a parcel\\carried along by the flow", YELLOW)
        rp = under(eq2[4], r"pushed from high\\to low pressure", C.PRESSURE)
        rv = under(eq2[6], r"smoothed toward\\its neighbors", C.VISCOUS)
        rf = under(eq2[8], r"outside\\forces", C.FORCE)
        div_l = label(r"\ldots and the fluid never compresses", font_size=30, color=C.DIVERGENCE)
        div.generate_target()
        div.target.next_to(VGroup(lhs, rp, rv, rf), DOWN, buff=0.6)
        div_l.next_to(div.target, RIGHT, buff=0.5)

        with self.voiceover(
            "Read the equation like a sentence: a parcel of fluid, <bookmark mark='c'/> carried along by the flow, changes its "
            "velocity <bookmark mark='p'/> because it's pushed from high pressure to low, <bookmark mark='v'/> because it's dragged "
            "toward the velocity of its neighbors, <bookmark mark='f'/> and because of outside forces. "
            "<bookmark mark='d'/> And through it all, the fluid never compresses."
        ) as vo:
            self.play(MoveToTarget(div))
            vo.wait_until("c")
            self.play(FadeIn(lhs, shift=UP * 0.1))
            vo.wait_until("p")
            self.play(FadeIn(rp, shift=UP * 0.1))
            vo.wait_until("v")
            self.play(FadeIn(rv, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(rf, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(div_l, shift=LEFT * 0.2), Indicate(div))
        self.play(FadeOut(VGroup(lhs, rp, rv, rf, div_l)), VGroup(eq2, div).animate.scale(0.8).to_edge(UP, buff=0.5))

        # Initial + boundary conditions ---------------------------------------
        count = label(r"4 equations, 4 unknowns", font_size=40, color=YELLOW).next_to(VGroup(eq2, div), DOWN, buff=0.5)
        ic = MathTex(r"\vu(\vx, 0) = \vu_0(\vx)", font_size=40).move_to(LEFT * 3.6 + DOWN * 1.9)
        ic_l = label(r"initial velocity field", font_size=28, color=C.DIM).next_to(ic, DOWN, buff=0.2)

        wall = Line(RIGHT * 1.6 + DOWN * 3.3, RIGHT * 6.6 + DOWN * 3.3, color=GREY_A, stroke_width=5)
        hatch = VGroup(*[Line([x, -3.3, 0], [x - 0.25, -3.6, 0], color=GREY_C, stroke_width=2) for x in np.arange(1.8, 6.7, 0.3)])
        prof = VGroup(*[
            Arrow([2.4, y, 0], [2.4 + 2.6 * np.tanh(2.2 * (y + 3.3)), y, 0], buff=0, color=C.VELOCITY, stroke_width=4,
                  max_tip_length_to_length_ratio=0.25)
            for y in np.linspace(-3.15, -1.0, 7)
        ])
        ns_l = MathTex(r"\text{no-slip: } \vu = 0 \text{ at the wall}", font_size=32).next_to(wall, UP, buff=2.5).shift(RIGHT * 0.3)

        with self.voiceover(
            "Four equations, four unknowns. <bookmark mark='i'/> Add an initial velocity field, and conditions at the boundaries, "
            "<bookmark mark='ns'/> for instance, that fluid touching a solid wall sticks to it, the so-called no-slip condition, "
            "<bookmark mark='det'/> and in principle, the entire future of the flow is determined."
        ) as vo:
            self.play(FadeIn(count))
            vo.wait_until("i")
            self.play(Write(ic), FadeIn(ic_l))
            vo.wait_until("ns")
            self.play(Create(wall), FadeIn(hatch))
            self.play(LaggedStart(*[GrowArrow(a) for a in prof], lag_ratio=0.1), FadeIn(ns_l))
            vo.wait_until("det")
            self.play(Circumscribe(VGroup(eq2, div), color=YELLOW, buff=0.2))
        self.wait(0.5)
        self.clear_scene()
