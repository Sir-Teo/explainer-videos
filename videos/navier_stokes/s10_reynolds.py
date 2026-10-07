from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import caption_box, cylinder_movie, frame_rect, label


def ns_divided(font_size=48, tilde=False):
    t = (lambda s: s.replace(r"\vu", r"\tilde{\vu}").replace(r"\nabla", r"\tilde\nabla").replace(" t}", r" \tilde t}")
         .replace(" p", r" \tilde p")) if tilde else (lambda s: s)
    parts = [r"{\partial \vu \over \partial t}", r"+", r"(\vu \cdot \nabla)\vu", r"=", r"-{1 \over \rho}\nabla p", r"+",
             r"\nu \nabla^2 \vu"]
    parts = [t(p) for p in parts]
    if tilde:
        parts[4] = r"-\tilde\nabla \tilde p"
        parts[6] = r"{1 \over \mathrm{Re}} \tilde\nabla^2 \tilde{\vu}"
    eq = MathTex(*parts, font_size=font_size)
    for i, col in {0: C.TIME, 2: C.ADVECT, 4: C.PRESSURE, 6: C.VISCOUS}.items():
        eq[i].set_color(col)
    return eq


class ReynoldsNumber(VoiceoverScene):
    def construct(self):
        self.estimate()
        self.nondimensionalize()
        self.sweep()
        self.number_line()

    # ------------------------------------------------------------------
    def estimate(self):
        eq = ns_divided(font_size=52).to_edge(UP, buff=0.6)
        q = label(r"inertia \quad vs. \quad viscosity", font_size=36).next_to(eq, DOWN, buff=0.45)
        q[0][:7].set_color(C.ADVECT)
        q[0][-9:].set_color(C.VISCOUS)

        # Cylinder sketch with U and L
        cyl = Circle(0.75, color=GREY_A, fill_color=GREY_D, fill_opacity=1).move_to(LEFT * 4.6 + DOWN * 1.6)
        flow = VGroup(*[Arrow([-6.9, y, 0], [-6.0, y, 0], buff=0, color=C.VELOCITY, stroke_width=4) for y in np.linspace(-2.8, -0.4, 5)])
        Ul = MathTex("U", font_size=40, color=C.VELOCITY).next_to(flow, UP, buff=0.1)
        Lb = BraceBetweenPoints(cyl.get_bottom(), cyl.get_top(), direction=RIGHT)
        Ll = MathTex("L", font_size=40).next_to(Lb, RIGHT, buff=0.1)

        rows = VGroup(
            MathTex(r"(\vu\cdot\nabla)\vu", r"\sim", r"U \cdot {U \over L}", r"=", r"{U^2 \over L}", font_size=42),
            MathTex(r"\nu\nabla^2\vu", r"\sim", r"\nu\, {U \over L^2}", font_size=42),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * 2.2 + DOWN * 0.9)
        rows[1].shift(RIGHT * (rows[0][1].get_x() - rows[1][1].get_x()))
        rows[0][0].set_color(C.ADVECT)
        rows[1][0].set_color(C.VISCOUS)

        with self.voiceover(
            "So which effect wins? <bookmark mark='i'/> Inertia, the fluid carrying itself along, or viscosity, smoothing "
            "everything out? Let's make a rough estimate."
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("i")
            self.play(FadeIn(q), Indicate(eq[2]), Indicate(eq[6]))

        with self.voiceover(
            "Suppose the flow has a typical speed U, <bookmark mark='l'/> and changes over a typical length L, like the diameter "
            "of a cylinder in a wind tunnel. <bookmark mark='a'/> The advection term is a velocity times a velocity gradient, "
            "so it's roughly U times U over L."
        ) as vo:
            self.play(LaggedStart(*[GrowArrow(a) for a in flow], lag_ratio=0.1), FadeIn(Ul), FadeIn(cyl))
            vo.wait_until("l")
            self.play(GrowFromCenter(Lb), FadeIn(Ll))
            vo.wait_until("a")
            self.play(Write(rows[0]))

        with self.voiceover(
            "The viscous term has two derivatives, so it's roughly nu times U over L squared."
        ) as vo:
            self.play(Write(rows[1]))

        ratio = MathTex(r"{U^2 / L \over \nu U / L^2}", r"=", r"{U L \over \nu}", r"=", r"\mathrm{Re}", font_size=52)
        ratio[4].set_color(C.REYNOLDS)
        ratio.move_to(RIGHT * 2.2 + DOWN * 1.0)
        rbox = caption_box(ratio[2:], color=C.REYNOLDS)
        name = label(r"the Reynolds number", font_size=34, color=C.REYNOLDS).next_to(rbox, DOWN, buff=0.25)
        with self.voiceover(
            "Their ratio, U L over nu, is called <bookmark mark='r'/> the Reynolds number. It's arguably the single most important "
            "number in fluid mechanics."
        ) as vo:
            self.play(ReplacementTransform(rows, ratio[:3]))
            vo.wait_until("r")
            self.play(Write(ratio[3:]), Create(rbox), FadeIn(name))
        self.clear_scene()

    # ------------------------------------------------------------------
    def nondimensionalize(self):
        subs = MathTex(r"\vx = L\,\tilde{\vx}", r",\quad", r"\vu = U\,\tilde{\vu}", r",\quad", r"t = {L \over U}\,\tilde t",
                       r",\quad", r"p = \rho U^2\,\tilde p", font_size=40).to_edge(UP, buff=0.5)
        rows = VGroup(
            MathTex(r"{U^2 \over L}", r"{\partial \tilde{\vu} \over \partial \tilde t}", r"+", r"{U^2 \over L}",
                    r"(\tilde{\vu}\cdot\tilde\nabla)\tilde{\vu}", r"=", r"-{U^2 \over L}", r"\tilde\nabla\tilde p", r"+",
                    r"{\nu U \over L^2}", r"\tilde\nabla^2\tilde{\vu}", font_size=46),
        )
        r = rows[0]
        for i, col in {1: C.TIME, 4: C.ADVECT, 7: C.PRESSURE, 10: C.VISCOUS}.items():
            r[i].set_color(col)
        r.next_to(subs, DOWN, buff=0.8)
        div = label(r"divide by $U^2/L$", font_size=32, color=C.DIM).next_to(r, DOWN, buff=0.35)
        final = ns_divided(font_size=56, tilde=True).next_to(div, DOWN, buff=0.45)
        coeff = MathTex(r"{\nu U / L^2 \over U^2 / L}", r"=", r"{\nu \over U L}", r"=", r"{1 \over \mathrm{Re}}", font_size=38)
        coeff[4].set_color(C.REYNOLDS)
        coeff.to_edge(DOWN, buff=0.35)
        fbox = caption_box(final, color=C.REYNOLDS, buff=0.25)

        with self.voiceover(
            "In fact, we can make this exact. Measure lengths in units of L, velocities in units of U, time in units of "
            "L over U, and pressure in units of rho U squared. <bookmark mark='s'/> Substitute these into the equation, "
            "<bookmark mark='d'/> and divide through by U squared over L."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m) for m in subs], lag_ratio=0.35), run_time=4)
            vo.wait_until("s")
            self.play(Write(r), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(div))
            for i in (0, 3, 6, 9):
                r[i].set_color(YELLOW)
            self.play(*[Indicate(r[i]) for i in (0, 3, 6, 9)])

        with self.voiceover(
            "Everything cancels except a single parameter: <bookmark mark='re'/> one over the Reynolds number, sitting in front "
            "of the viscous term."
        ) as vo:
            self.play(TransformMatchingShapes(r.copy(), final), run_time=2)
            vo.wait_until("re")
            self.play(Write(coeff))
            self.play(Create(fbox))

        sim = label(r"Same geometry + same Re $\Rightarrow$ the same flow, just rescaled", font_size=34, color=YELLOW)
        sim.move_to(coeff)
        with self.voiceover(
            "Two flows with the same geometry and the same Reynolds number are the same flow, just rescaled. "
            "That's why engineers can test a small model in a wind tunnel and trust the results, as long as the Reynolds "
            "number matches."
        ) as vo:
            self.play(FadeOut(coeff), FadeIn(sim, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        names = ["cyl_re1", "cyl_re40", "cyl_re150", "cyl_re1000"]
        values = [1, 40, 150, 1000]
        movies = [cylinder_movie(n, width=13.4, alpha=0.0) for n in names]
        for m in movies:
            m.move_to(DOWN * 0.45)
            m.rate = 0.0
        border = frame_rect(movies[0])
        re_lab = VGroup(MathTex(r"\mathrm{Re} =", font_size=56, color=C.REYNOLDS),
                        Integer(1, font_size=56, color=C.REYNOLDS)).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.45)
        caption = label("", font_size=32)

        def set_caption(text):
            new = label(text, font_size=32, color=GREY_A).next_to(border, DOWN, buff=0.3)
            return new

        texts = [
            r"viscosity dominates: smooth, nearly symmetric",
            r"two steady eddies sit behind the cylinder",
            r"eddies shed alternately: a K\'arm\'an vortex street",
            r"tighter, more intense vortices (3D flows: turbulent)",
        ]
        lines = [
            "Watch the flow past a cylinder as we dial up the Reynolds number. <bookmark mark='go'/> At Re equals one, viscosity "
            "dominates. The flow oozes smoothly around the cylinder, and the disturbance spreads far out to the sides.",
            "At Re equals forty, two swirling eddies form behind the cylinder and just sit there, perfectly steady.",
            "Past roughly fifty, that steady arrangement becomes unstable. The eddies begin to break away, alternating sides. "
            "The vortex street from the beginning was at Re equals one hundred fifty.",
            "Turn it up to a thousand, and the vortices become tighter and more intense, with thin filaments wrapped around them. "
            "In our two-dimensional simulation the street survives, but in real three-dimensional flows at this Reynolds "
            "number, the wake becomes turbulent.",
        ]
        prev = None
        for k, (movie, val, text, line) in enumerate(zip(movies, values, texts, lines)):
            cap = set_caption(text)
            with self.voiceover(line) as vo:
                self.add(movie)
                movie.rate = 1.0
                anims = [movie.fade(1.0, run_time=1.2)]
                if prev is not None:
                    anims += [prev.fade(0.0, run_time=1.2), FadeOut(caption, run_time=0.6),
                              ChangeDecimalToValue(re_lab[1], val, run_time=1.2)]
                else:
                    anims += [Create(border), FadeIn(re_lab)]
                self.play(*anims)
                if prev is not None:
                    self.remove(prev)
                self.play(FadeIn(cap, shift=UP * 0.15))
                caption = cap
            prev = movie
        self.wait(1.0)
        self.play(prev.fade(0.0), FadeOut(VGroup(border, re_lab, caption)))
        self.remove(prev)

    # ------------------------------------------------------------------
    def number_line(self):
        line = NumberLine(x_range=[-5, 9, 1], length=12.6, include_numbers=False, color=GREY_B).shift(DOWN * 0.6)
        ticks = VGroup(*[MathTex(f"10^{{{k}}}", font_size=28).next_to(line.n2p(k), DOWN, buff=0.25) for k in range(-4, 9, 2)])
        title = label(r"Reynolds numbers in the wild", font_size=40).to_edge(UP, buff=0.6)
        examples = [
            (-4, r"swimming\\bacterium", UP),
            (3.3, r"blood in\\the aorta", UP),
            (6.0, r"person\\swimming", DOWN),
            (7.5, r"air over a\\jetliner wing", UP),
        ]
        marks = VGroup()
        for x, text, side in examples:
            d = Dot(line.n2p(x), color=C.REYNOLDS, radius=0.1)
            t = label(text, font_size=28).next_to(d, side, buff=0.9 if side is DOWN else 0.35)
            if side is DOWN:
                t.shift(DOWN * 0.1)
            marks.add(VGroup(d, t))
        lam = label(r"viscous, orderly", font_size=28, color=C.VISCOUS).next_to(line.n2p(-3), DOWN, buff=1.4)
        turb = label(r"inertial, turbulent", font_size=28, color=C.ADVECT).next_to(line.n2p(7), DOWN, buff=1.9)
        bact = label(r"stops within a fraction of an atom's width when it stops swimming", font_size=26, color=C.DIM)
        bact.next_to(marks[0], UP, buff=0.25).align_to(line, LEFT)

        with self.voiceover(
            "The range in nature is staggering. <bookmark mark='b'/> A swimming bacterium lives at a Reynolds number around one "
            "ten-thousandth. For it, water is so syrupy that the moment it stops swimming, it stops dead. "
            "<bookmark mark='a'/> Blood in your aorta flows at Re in the thousands. <bookmark mark='p'/> A person swimming, around a "
            "million. <bookmark mark='j'/> The air flowing over a jetliner's wing, tens of millions."
        ) as vo:
            self.play(Write(title), Create(line), FadeIn(ticks))
            vo.wait_until("b")
            self.play(FadeIn(marks[0], shift=DOWN * 0.2))
            self.play(FadeIn(bact))
            vo.wait_until("a")
            self.play(FadeIn(marks[1], shift=DOWN * 0.2))
            vo.wait_until("p")
            self.play(FadeIn(marks[2], shift=UP * 0.2))
            vo.wait_until("j")
            self.play(FadeIn(marks[3], shift=DOWN * 0.2))
            self.play(FadeIn(lam), FadeIn(turb))
        self.wait(0.5)
        self.clear_scene()
