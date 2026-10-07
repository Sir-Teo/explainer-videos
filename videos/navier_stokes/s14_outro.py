from __future__ import annotations

from explainer import *  # noqa: F403
from videos.navier_stokes.common import (
    I_ADV, I_DT, I_F, I_P, I_VISC, cylinder_movie, label, ns_system,
)


class Outro(VoiceoverScene):
    def construct(self):
        movie = cylinder_movie("cyl_re150", width=config.frame_width, alpha=0.0, start=300)
        self.add(movie)
        system = ns_system(font_size=60).move_to(UP * 0.4)
        bg = BackgroundRectangle(system, fill_opacity=0.75, buff=0.45, corner_radius=0.15)
        eq, div = system

        with self.voiceover("Let's step back and look at the equations once more.") as vo:
            self.play(movie.fade(0.45, run_time=2), FadeIn(bg), FadeIn(system))

        def tag(mob, text, color, direction=DOWN):
            t = label(text, font_size=28, color=color)
            t.add_background_rectangle(opacity=0.8, buff=0.06)
            return t.next_to(mob, direction, buff=0.25)

        t_acc = tag(eq[I_DT:I_ADV + 2], r"acceleration, as felt by the parcel", YELLOW, UP)
        t_p = tag(eq[I_P], r"push: high $\to$ low $p$", C.PRESSURE, UP).shift(UP * 0.0)
        t_v = tag(eq[I_VISC], r"smoothing", C.VISCOUS, UP)
        t_f = tag(eq[I_F], r"outside", C.FORCE, UP).shift(RIGHT * 0.25)
        t_d = tag(div, r"never compresses", C.DIVERGENCE, RIGHT).shift(RIGHT * 0.1)
        # Stagger the upper tags so they do not collide.
        t_p.shift(UP * 0.55)
        t_f.shift(UP * 0.55)
        with self.voiceover(
            "On the left: <bookmark mark='a'/> the acceleration of a fluid parcel, as felt by the parcel itself, carried along by the "
            "flow. On the right: <bookmark mark='p'/> pressure pushing from high to low, <bookmark mark='v'/> viscosity smoothing out "
            "differences, <bookmark mark='f'/> and outside forces. <bookmark mark='d'/> And the promise that the fluid never compresses."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(t_acc))
            vo.wait_until("p")
            self.play(FadeIn(t_p))
            vo.wait_until("v")
            self.play(FadeIn(t_v))
            vo.wait_until("f")
            self.play(FadeIn(t_f))
            vo.wait_until("d")
            self.play(FadeIn(t_d))

        fma = MathTex(r"F = m\,a", font_size=56, color=YELLOW)
        fma.next_to(bg, DOWN, buff=0.45)
        fma.add_background_rectangle(opacity=0.8, buff=0.12)
        with self.voiceover(
            "It's just <bookmark mark='f'/> F equals m a, written for a continuum. Every term has a simple physical meaning. Yet out of "
            "these few pieces comes everything from the rhythm of a vortex street, to the chaos of turbulence, to the weather on our "
            "planet. And whether a fluid, left entirely to itself, can ever tear itself apart is still waiting for someone to figure out."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeOut(VGroup(t_acc, t_p, t_v, t_f, t_d)), FadeIn(fma, shift=UP * 0.2))
            self.play(movie.fade(1.0, run_time=3))

        thanks = label(r"Thanks for watching.", font_size=56)
        thanks.add_background_rectangle(opacity=0.7, buff=0.3)
        with self.voiceover("Thanks for watching.") as vo:
            self.play(FadeOut(VGroup(system, bg, fma)), FadeIn(thanks))
        self.wait(2.0)
        movie.rate = 0
        self.play(FadeOut(thanks), movie.fade(0.0, run_time=1.5))
        self.remove(movie)
