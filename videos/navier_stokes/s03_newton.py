from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import label, template_equation
from videos.navier_stokes.s02_fields import blue_field, flow


class NewtonForParcels(VoiceoverScene):
    def construct(self):
        field = blue_field().set_opacity(0.5)
        small = Square(0.42, color=WHITE, stroke_width=2.5, fill_color=C.VELOCITY, fill_opacity=0.55)
        small.move_to([-6.2, -0.4, 0])

        def drift(m, dt):
            p = m.get_center()
            k1 = flow(p)
            m.shift(dt * flow(p + 0.5 * dt * k1))

        small.add_updater(drift)
        tag = label("a fluid parcel", font_size=30).add_background_rectangle(opacity=0.8, buff=0.06)
        tag.add_updater(lambda m: m.next_to(small, UP, buff=0.15))

        with self.voiceover(
            "Now for the physics. Follow one tiny blob of fluid, <bookmark mark='p'/> a parcel, as it drifts along. "
            "Picture it as small enough that the velocity is essentially uniform across it, yet large enough "
            "to contain an enormous number of molecules."
        ) as vo:
            self.play(FadeIn(field))
            vo.wait_until("p")
            self.play(FadeIn(small, scale=0.5), FadeIn(tag))

        # --- Zoom in on the parcel ------------------------------------------
        small.clear_updaters()
        tag.clear_updaters()
        big = Square(2.6, color=WHITE, stroke_width=3, fill_color=C.VELOCITY, fill_opacity=0.25).move_to(LEFT * 4.4)
        dx = BraceLabel(big, r"dx", brace_direction=DOWN, font_size=36)
        dy = BraceLabel(big, r"dy", brace_direction=LEFT, font_size=36)
        dz = MathTex(r"(\text{and } dz)", font_size=30, color=C.DIM).next_to(big, UP, buff=0.2)

        eqs = VGroup(
            MathTex(r"F", r"=", r"m", r"a", font_size=60),
            MathTex(r"m", r"=", r"\rho", r"\, dV", font_size=48),
            MathTex(r"F", r"=", r"(\rho\, dV)", r"\, a", font_size=48),
            MathTex(r"\rho", r"\, a", r"=", r"{F \over dV}", font_size=56),
        )
        eqs.arrange(DOWN, buff=0.55).move_to(RIGHT * 3.0 + UP * 0.2)
        eqs[1][2].set_color(C.DENSITY)
        eqs[2][2].set_color(C.DENSITY)
        eqs[3][0].set_color(C.DENSITY)

        with self.voiceover(
            "Its volume is <bookmark mark='dv'/> dV, and if the fluid's density is rho, its mass is "
            "<bookmark mark='m'/> rho times dV. Newton's second law says <bookmark mark='f'/> mass times acceleration "
            "equals the total force on it."
        ) as vo:
            self.play(FadeOut(field), FadeOut(tag), ReplacementTransform(small, big), run_time=1.5)
            vo.wait_until("dv")
            self.play(FadeIn(dx), FadeIn(dy), FadeIn(dz))
            vo.wait_until("m")
            self.play(Write(eqs[1]))
            vo.wait_until("f")
            self.play(Write(eqs[0]))
            self.play(TransformMatchingTex(eqs[0].copy(), eqs[2]), run_time=1.5)

        per_vol = label(r"force per unit volume", font_size=30, color=C.DIM).next_to(eqs[3], DOWN, buff=0.3)
        with self.voiceover(
            "Since the parcel is tiny, it's more natural to divide both sides by its volume. "
            "<bookmark mark='l'/> On the left, density times acceleration. <bookmark mark='r'/> On the right, force per unit volume."
        ) as vo:
            self.play(TransformMatchingTex(eqs[2].copy(), eqs[3]), run_time=1.5)
            vo.wait_until("l")
            self.play(Indicate(eqs[3][:2], color=YELLOW))
            vo.wait_until("r")
            self.play(Indicate(eqs[3][3], color=YELLOW), FadeIn(per_vol, shift=UP * 0.1))

        # --- Three kinds of force ----------------------------------------------
        self.play(
            FadeOut(eqs[:3]), FadeOut(dz),
            VGroup(eqs[3], per_vol).animate.scale(0.8).to_corner(UR, buff=0.6),
        )
        s = big.side_length / 2
        c = big.get_center()
        p_arrows = VGroup(
            *[
                Arrow(c + d * (s + 1.1), c + d * (s + 0.32), buff=0, color=C.PRESSURE, stroke_width=6)
                for d in (LEFT, RIGHT, UP, DOWN)
            ]
        )
        v_arrows = VGroup(
            Arrow(c + UP * (s + 0.14) + LEFT * 0.8, c + UP * (s + 0.14) + RIGHT * 0.8, buff=0, color=C.VISCOUS, stroke_width=6),
            Arrow(c + DOWN * (s + 0.14) + RIGHT * 0.6, c + DOWN * (s + 0.14) + LEFT * 0.6, buff=0, color=C.VISCOUS, stroke_width=6),
        )
        g_arrow = Arrow(c + UP * 0.2, c + DOWN * 1.0, buff=0, color=C.FORCE, stroke_width=7)

        legend = VGroup(
            label(r"\textbf{Pressure}: neighbors push \emph{perpendicular} to the surface", color=C.PRESSURE, font_size=28),
            label(r"\textbf{Viscosity}: neighbors drag \emph{along} the surface", color=C.VISCOUS, font_size=28),
            label(r"\textbf{External}: e.g.\ gravity, acting on the whole volume", color=C.FORCE, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        legend.move_to(DOWN * 0.3).to_edge(RIGHT, buff=0.5)

        with self.voiceover(
            "So what forces act on a parcel of fluid? Only three kinds. First, the surrounding fluid pushes on it, "
            "perpendicular to its surface. <bookmark mark='p'/> That's pressure."
        ) as vo:
            self.play(FadeOut(dx), FadeOut(dy))
            self.play(LaggedStart(*[GrowArrow(a) for a in p_arrows], lag_ratio=0.15))
            vo.wait_until("p")
            self.play(FadeIn(legend[0], shift=RIGHT * 0.2))

        with self.voiceover(
            "Second, neighboring fluid sliding past drags on it, tangent to its surface. "
            "<bookmark mark='v'/> That's viscosity, a kind of internal friction."
        ) as vo:
            self.play(p_arrows.animate.set_opacity(0.3), LaggedStart(*[GrowArrow(a) for a in v_arrows], lag_ratio=0.3))
            vo.wait_until("v")
            self.play(FadeIn(legend[1], shift=RIGHT * 0.2))

        with self.voiceover(
            "And third, there can be forces acting on the whole body of the parcel from outside, "
            "<bookmark mark='g'/> like gravity."
        ) as vo:
            self.play(v_arrows.animate.set_opacity(0.3), GrowArrow(g_arrow))
            vo.wait_until("g")
            self.play(FadeIn(legend[2], shift=RIGHT * 0.2))

        # --- The template ---------------------------------------------------
        template = template_equation(font_size=44).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So the equation we're after has this shape. Each piece has a clean mathematical form, and we're going "
            "to derive every one of them. Let's start with the left side, which turns out to be the subtlest: "
            "<bookmark mark='a'/> acceleration."
        ) as vo:
            self.play(p_arrows.animate.set_opacity(1), v_arrows.animate.set_opacity(1))
            self.play(Write(template[0]), run_time=2)
            self.play(LaggedStart(*[Create(b) for b in template[1:]], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(Indicate(template[0][2], color=YELLOW, scale_factor=1.15), template[1].animate.set_color(YELLOW))
        self.clear_scene()
