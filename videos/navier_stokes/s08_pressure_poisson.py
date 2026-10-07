from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import I_DT, caption_box, heatmap, label, ns_equation, pressure_colormap

YW = -2.7  # wall height
A = 0.55  # strain rate of the stagnation-point flow


def stag_flow(p):
    return A * np.array([p[0], -(p[1] - YW), 0.0])


class PressureEnforcer(VoiceoverScene):
    def construct(self):
        self.no_time_derivative()
        self.wall()
        self.poisson()
        self.instant()

    # ------------------------------------------------------------------
    def no_time_derivative(self):
        eq = ns_equation(font_size=56).shift(UP * 0.6)
        q = MathTex(r"{\partial p \over \partial t}", r"\ ?", font_size=60, color=C.PRESSURE).next_to(eq, DOWN, buff=0.9)
        cross = Cross(q[0], stroke_color=GREY_B, stroke_width=5)
        with self.voiceover(
            "Here's something curious. The velocity has an equation <bookmark mark='u'/> telling it how to change in time. "
            "But the pressure doesn't: <bookmark mark='p'/> there's no partial p partial t anywhere. So what decides the pressure?"
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("u")
            self.play(Indicate(eq[I_DT], scale_factor=1.25))
            vo.wait_until("p")
            self.play(Write(q))
            self.play(Create(cross))
        ans = label(r"Pressure is whatever it needs to be\\to keep the flow incompressible.", font_size=40, color=YELLOW)
        ans.next_to(eq, DOWN, buff=0.9)
        with self.voiceover("The answer: pressure is whatever it needs to be to keep the flow incompressible."):
            self.play(FadeOut(VGroup(q, cross)), FadeIn(ans, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def wall(self):
        rng = np.random.default_rng(4)
        wall = Line([-7.2, YW, 0], [7.2, YW, 0], color=GREY_A, stroke_width=6)
        hatch = VGroup(*[Line([x, YW, 0], [x - 0.3, YW - 0.3, 0], color=GREY_C, stroke_width=2) for x in np.arange(-7, 7.3, 0.35)])

        # (a) Without pressure: straight down, piling up.
        dots = VGroup(*[Dot([rng.uniform(-5, 5), rng.uniform(-1.5, 4.2), 0], radius=0.05, color=BLUE_B) for _ in range(160)])

        def fall(g, dt):
            for d in g:
                y = d.get_y()
                if y > YW + 0.08 + 0.02 * rng.random():
                    d.shift(DOWN * min(1.3 * dt, y - YW - 0.06))

        dots.add_updater(fall)
        comp = label(r"no pressure $\Rightarrow$ fluid piles up and compresses", font_size=32, color=GREY_A)
        comp.add_background_rectangle(opacity=0.85, buff=0.1).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Imagine fluid flowing straight toward a wall. <bookmark mark='l'/> Left alone, with no pressure, it would just pile up "
            "against the wall, compressing."
        ) as vo:
            self.play(Create(wall), FadeIn(hatch))
            vo.wait_until("l")
            self.play(FadeIn(dots), FadeIn(comp))
            self.wait(vo.remaining())
        self.wait(1.5)
        dots.clear_updaters()
        self.play(FadeOut(dots), FadeOut(comp))

        # (b) With pressure: stagnation-point flow.
        pmap = heatmap(lambda X, Y: -(X**2 + (Y - YW) ** 2), (-7.2, 7.2), (YW, 4.1), resolution=150,
                       colormap=pressure_colormap(-40, 0.0))
        hi = label(r"high $p$", font_size=32).move_to([0, YW + 0.45, 0]).add_background_rectangle(opacity=0.6, buff=0.06)

        specks = VGroup(*[Dot(radius=0.045, color=WHITE) for _ in range(140)])
        for s in specks:
            s.move_to([rng.uniform(-5.5, 5.5), rng.uniform(YW + 0.3, 4.0), 0])

        def advect(g, dt):
            for s in g:
                p = s.get_center()
                p = p + dt * stag_flow(p + 0.5 * dt * stag_flow(p))
                if abs(p[0]) > 7.3:
                    p = np.array([rng.uniform(-1.8, 1.8), 4.1, 0])
                s.move_to(p)

        specks.add_updater(advect)
        flow_arrows = ArrowVectorField(stag_flow, x_range=[-6.6, 6.6, 0.8], y_range=[YW + 0.4, 3.6, 0.8], color=C.VELOCITY,
                                       length_func=lambda n: 0.5 * np.tanh(0.8 * n)).set_opacity(0.6)
        push = ArrowVectorField(lambda p: np.array([p[0], p[1] - YW, 0]) * np.exp(-((p[0] ** 2 + (p[1] - YW) ** 2) / 9)),
                                x_range=[-3.2, 3.2, 0.8], y_range=[YW + 0.4, 0.4, 0.8], color="#FF8C7A",
                                length_func=lambda n: 0.55 * np.tanh(1.2 * n))
        push_l = MathTex(r"-\nabla p", font_size=40, color="#FF8C7A").move_to([2.6, YW + 2.4, 0])
        push_l.add_background_rectangle(opacity=0.7, buff=0.08)

        with self.voiceover(
            "Instead, <bookmark mark='h'/> a region of high pressure forms right in front of the wall. "
            "<bookmark mark='g'/> Its gradient pushes back on the incoming fluid, slowing it down and steering it aside, "
            "exactly enough that nothing ever gets compressed."
        ) as vo:
            vo.wait_until("h")
            self.add(pmap, wall, hatch)
            self.play(FadeIn(pmap), FadeIn(hi))
            self.play(Create(flow_arrows, lag_ratio=0.01), FadeIn(specks))
            vo.wait_until("g")
            self.play(flow_arrows.animate.set_opacity(0.0), Create(push, lag_ratio=0.02), FadeIn(push_l))
        self.wait(2.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def poisson(self):
        start = MathTex(
            r"{\partial \vu \over \partial t}", r"+", r"(\vu\cdot\nabla)\vu", r"=", r"-{1 \over \rho}\nabla p", r"+",
            r"\nu \nabla^2 \vu", font_size=46,
        )
        cols = [C.TIME, None, C.ADVECT, None, C.PRESSURE, None, C.VISCOUS]
        for m, col in zip(start, cols):
            if col:
                m.set_color(col)
        start.to_edge(UP, buff=0.6)
        divop = label(r"take the divergence ($\nabla\cdot$) of both sides", font_size=32, color=C.DIVERGENCE).next_to(start, DOWN, buff=0.35)

        terms = VGroup(
            MathTex(r"\nabla\cdot{\partial \vu \over \partial t}", r"=", r"{\partial \over \partial t}(\nabla\cdot\vu)", r"=", r"0"),
            MathTex(r"\nabla\cdot(\nu\nabla^2\vu)", r"=", r"\nu\nabla^2(\nabla\cdot\vu)", r"=", r"0"),
            MathTex(r"\nabla\cdot\Big(-{1\over\rho}\nabla p\Big)", r"=", r"-{1\over\rho}\nabla^2 p"),
        )
        for t in terms:
            t.scale(0.8)
        terms[0][0].set_color(C.TIME)
        terms[1][0].set_color(C.VISCOUS)
        terms[2][0].set_color(C.PRESSURE)
        terms.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(divop, DOWN, buff=0.45)
        because = label(r"(because $\nabla\cdot\mathbf{u} = 0$)", font_size=26, color=C.DIVERGENCE)
        because.next_to(terms[:2], RIGHT, buff=0.5)

        result = MathTex(r"\nabla^2 p", r"=", r"-\rho\, \nabla\cdot\big[(\vu\cdot\nabla)\vu\big]", font_size=56)
        result[0].set_color(C.PRESSURE)
        result[2].set_color(C.ADVECT)
        result.to_edge(DOWN, buff=0.8)
        rbox = caption_box(result, color=C.PRESSURE, buff=0.25)

        with self.voiceover(
            "We can make this precise. <bookmark mark='d'/> Take the divergence of the whole momentum equation. "
            "<bookmark mark='t'/> The time derivative term vanishes, since the divergence of u is always zero. "
            "<bookmark mark='v'/> So does the viscous term. <bookmark mark='p'/> What's left is an equation for the pressure alone."
        ) as vo:
            self.play(FadeIn(start))
            vo.wait_until("d")
            self.play(FadeIn(divop, shift=DOWN * 0.2))
            vo.wait_until("t")
            self.play(Write(terms[0]), FadeIn(because))
            vo.wait_until("v")
            self.play(Write(terms[1]))
            vo.wait_until("p")
            self.play(Write(terms[2]))
            self.play(Write(result), Create(rbox))
        self.clear_scene(result, rbox, extra=[VGroup(result, rbox).animate.scale(0.75).to_edge(UP, buff=0.4)])
        self.result = VGroup(result, rbox)

    # ------------------------------------------------------------------
    def instant(self):
        x0, x1, y0, y1 = -6.6, 6.6, -3.0, 1.9
        src = np.array([-2.5, -0.6])

        def resp(X, Y):
            r2 = (X - src[0]) ** 2 + (Y - src[1]) ** 2 + 0.08
            return -np.log(r2)

        pmap = heatmap(resp, (x0, x1), (y0, y1), resolution=130, colormap=pressure_colormap(-3.5, 2.6))
        border = Rectangle(width=x1 - x0, height=y1 - y0, color=GREY_C, stroke_width=1.5).move_to(pmap)
        poke = Arrow([src[0] - 1.2, src[1], 0], [src[0] - 0.1, src[1], 0], buff=0, color=YELLOW, stroke_width=8)
        far = Dot([4.8, 0.9, 0], color=WHITE)
        far_l = label(r"felt here too, instantly", font_size=28).next_to(far, DOWN, buff=0.15)
        far_l.add_background_rectangle(opacity=0.7, buff=0.06)
        with self.voiceover(
            "This is a Poisson equation, the same kind of equation that describes gravitational and electric potentials. "
            "<bookmark mark='a'/> Its solution at any point depends on the flow everywhere else, all at once. "
            "<bookmark mark='i'/> In an incompressible fluid, a push anywhere is felt everywhere instantly."
        ) as vo:
            self.play(Create(border))
            vo.wait_until("a")
            self.play(GrowArrow(poke))
            vo.wait_until("i")
            self.play(FadeIn(pmap), run_time=0.4)
            self.add(border, poke)
            self.play(FadeIn(far, scale=0.5), FadeIn(far_l))

        sound = MathTex(r"c_{\text{sound, water}} \approx 1500\ \text{m/s}", font_size=40).to_edge(DOWN, buff=0.15)
        sound.add_background_rectangle(opacity=0.85, buff=0.1)
        with self.voiceover(
            "Physically, the news travels as sound waves. <bookmark mark='c'/> In water, sound moves at about fifteen hundred "
            "meters per second, so fast compared to everyday flows that 'instantly' is an excellent approximation."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(sound, shift=UP * 0.2))
        self.clear_scene()

        enforcer = VGroup(
            label(r"Pressure is not an independent player.", font_size=40),
            label(r"It is an \emph{enforcer}: a Lagrange multiplier for the constraint", font_size=36, color=C.PRESSURE),
            MathTex(r"\nabla\cdot\vu = 0", font_size=56, color=C.DIVERGENCE),
        ).arrange(DOWN, buff=0.5)
        with self.voiceover(
            "So pressure isn't really an independent player. It's an enforcer, <bookmark mark='l'/> mathematically a Lagrange "
            "multiplier, constantly adjusting itself so the velocity field never violates the incompressibility constraint."
        ) as vo:
            self.play(FadeIn(enforcer[0]))
            vo.wait_until("l")
            self.play(FadeIn(enforcer[1]))
            self.play(Write(enforcer[2]))
        self.wait(0.5)
        self.clear_scene()
