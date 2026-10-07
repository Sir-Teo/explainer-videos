from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import caption_box, frame_rect, label, square_movie


class ViscousForce(VoiceoverScene):
    def construct(self):
        self.layers()
        self.slab_derivation()
        self.laplacian_intuition()
        self.smoothing()
        self.honey_vs_water()

    # ------------------------------------------------------------------
    def layers(self):
        n = 7
        H, W = 0.62, 7.6
        ys = [-1.9 + i * H for i in range(n)]
        speeds = [0.25 + 0.32 * i for i in range(n)]
        x_left = -6.9
        strips = VGroup()
        ticks = VGroup()
        clip_w = W
        for y, s in zip(ys, speeds):
            r = Rectangle(width=W, height=H, stroke_width=1.2, stroke_color=GREY_C, fill_color=C.VELOCITY,
                          fill_opacity=0.08 + 0.05 * s)
            r.move_to([x_left + W / 2, y, 0])
            strips.add(r)
            row = VGroup(*[Line(UP * 0.18, DOWN * 0.18, stroke_width=3, color=BLUE_B).move_to([x_left + 0.4 + k * 0.95, y, 0])
                           for k in range(8)])
            row.speed = s
            ticks.add(row)

        def slide(row, dt):
            for t in row:
                t.shift(RIGHT * row.speed * dt * 1.6)
                if t.get_x() > x_left + clip_w - 0.1:
                    t.shift(LEFT * (clip_w - 0.2))

        for row in ticks:
            row.add_updater(slide)
        vel = VGroup(*[Arrow([x_left + W + 0.15, y, 0], [x_left + W + 0.15 + 0.85 * s, y, 0], buff=0, color=C.VELOCITY,
                             stroke_width=5, max_tip_length_to_length_ratio=0.3) for y, s in zip(ys, speeds)])
        uy = MathTex(r"u(y)", color=C.VELOCITY, font_size=36).next_to(vel, UP, buff=0.2)

        with self.voiceover(
            "Next, viscosity: the internal friction that makes honey ooze differently from water. "
            "Picture a flow made of thin horizontal layers sliding past each other, <bookmark mark='f'/> faster at the top, "
            "slower at the bottom."
        ) as vo:
            self.play(FadeIn(strips), FadeIn(ticks))
            vo.wait_until("f")
            self.play(LaggedStart(*[GrowArrow(a) for a in vel], lag_ratio=0.1), FadeIn(uy))

        mid = 3
        y = ys[mid]
        top_drag = Arrow([-4.6, y + H / 2 - 0.08, 0], [-3.0, y + H / 2 - 0.08, 0], buff=0, color=C.VISCOUS, stroke_width=7)
        bot_drag = Arrow([-3.0, y - H / 2 + 0.08, 0], [-4.6, y - H / 2 + 0.08, 0], buff=0, color=C.VISCOUS, stroke_width=7)
        with self.voiceover(
            "Each layer rubs against its neighbors. <bookmark mark='a'/> A faster layer above drags a slower one forward, "
            "<bookmark mark='b'/> and the slower layer below holds it back."
        ) as vo:
            self.play(strips[mid].animate.set_stroke(WHITE, 3), strips[mid].animate.set_fill(opacity=0.35))
            vo.wait_until("a")
            self.play(GrowArrow(top_drag))
            vo.wait_until("b")
            self.play(GrowArrow(bot_drag))

        law = MathTex(r"\tau", r"=", r"\mu", r"{\partial u \over \partial y}", font_size=60)
        law[0].set_color(C.VISCOUS)
        law[2].set_color(C.VISCOUS)
        law.move_to(RIGHT * 4.6 + UP * 1.4)
        law_l = label(r"shear stress\\(force per unit area)", font_size=28).next_to(law, DOWN, buff=0.35)
        mu_l = label(r"$\mu$ = viscosity", font_size=32, color=C.VISCOUS).next_to(law_l, DOWN, buff=0.45)
        newt = label(r"(a ``Newtonian'' fluid, like water or air)", font_size=24, color=C.DIM).next_to(mu_l, DOWN, buff=0.3)
        with self.voiceover(
            "For fluids like water and air, this frictional force per unit area, called the shear stress, "
            "is proportional to how quickly the velocity changes from one layer to the next: "
            "<bookmark mark='l'/> mu times partial u partial y. <bookmark mark='m'/> The constant mu, in green, is the viscosity."
        ) as vo:
            self.play(FadeOut(VGroup(vel, uy)))
            vo.wait_until("l")
            self.play(Write(law), FadeIn(law_l))
            vo.wait_until("m")
            self.play(FadeIn(mu_l), FadeIn(newt))
        self.clear_scene(law, extra=[law.animate.scale(0.75).to_corner(UR, buff=0.5)])
        self.law = law

    # ------------------------------------------------------------------
    def slab_derivation(self):
        ax = Axes(x_range=[0, 3.2, 1], y_range=[-2.2, 2.2, 1], x_length=4.6, y_length=6.0,
                  axis_config={"include_ticks": False, "stroke_color": GREY_B}).move_to(LEFT * 3.9 + DOWN * 0.2)
        ax_l = VGroup(MathTex("u", font_size=34, color=C.VELOCITY).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1),
                      MathTex("y", font_size=34).next_to(ax.y_axis.get_end(), UP, buff=0.1))
        shape = ValueTracker(1.0)  # 1 = curved (tanh) profile, 0 = straight line

        def prof(y):
            s = shape.get_value()
            return 1.5 + s * 1.15 * np.tanh(y) + (1 - s) * 0.55 * y

        def dprof(y):
            s = shape.get_value()
            return s * 1.15 / np.cosh(y) ** 2 + (1 - s) * 0.55

        curve = always_redraw(lambda: ax.plot_parametric_curve(lambda t: np.array([prof(t), t]), t_range=[-2.1, 2.1],
                                                                 color=C.VELOCITY, stroke_width=4))
        profile_arrows = always_redraw(lambda: VGroup(*[
            Arrow(ax.c2p(0, y), ax.c2p(prof(y), y), buff=0, color=C.VELOCITY, stroke_width=3,
                  max_tip_length_to_length_ratio=0.12).set_opacity(0.55)
            for y in np.linspace(-1.9, 1.9, 11)
        ]))
        y0, dy = 0.45, 0.7
        slab = always_redraw(lambda: Polygon(ax.c2p(0, y0), ax.c2p(prof(y0), y0), ax.c2p(prof(y0 + dy), y0 + dy),
                                             ax.c2p(0, y0 + dy), stroke_color=WHITE, stroke_width=2.5,
                                             fill_color=C.VELOCITY, fill_opacity=0.3))
        k = 1.6

        def top_arrow():
            L = k * dprof(y0 + dy)
            p = ax.c2p(0.9, y0 + dy) + UP * 0.12
            return Arrow(p, p + RIGHT * L, buff=0, color=C.VISCOUS, stroke_width=7, max_tip_length_to_length_ratio=0.3)

        def bot_arrow():
            L = k * dprof(y0)
            p = ax.c2p(0.9, y0) + DOWN * 0.12 + RIGHT * L
            return Arrow(p, p + LEFT * L, buff=0, color=C.VISCOUS, stroke_width=7, max_tip_length_to_length_ratio=0.3)

        ta, ba = always_redraw(top_arrow), always_redraw(bot_arrow)
        t_lab = MathTex(r"\tau(y{+}dy)\,A", font_size=32, color=C.VISCOUS)
        t_lab.add_updater(lambda m: m.next_to(ta, UP, buff=0.08))
        b_lab = MathTex(r"\tau(y)\,A", font_size=32, color=C.VISCOUS)
        b_lab.add_updater(lambda m: m.next_to(ba, DOWN, buff=0.08))
        dyb = always_redraw(lambda: BraceBetweenPoints(ax.c2p(0, y0 + dy), ax.c2p(0, y0), direction=LEFT, buff=0.08))
        dyl = MathTex("dy", font_size=32).add_updater(lambda m: m.next_to(dyb, LEFT, buff=0.08))

        with self.voiceover(
            "Now let's derive the force. Here's a velocity profile, and a slab of fluid of thickness dy. "
            "<bookmark mark='t'/> The layer above pulls it forward with stress tau at y plus dy, times the area A. "
            "<bookmark mark='b'/> The layer below drags it backward with tau at y, times A."
        ) as vo:
            self.play(Create(ax), FadeIn(ax_l), Create(curve), FadeIn(profile_arrows))
            self.play(FadeIn(slab), FadeIn(dyb), FadeIn(dyl))
            vo.wait_until("t")
            self.play(GrowArrow(ta), FadeIn(t_lab))
            vo.wait_until("b")
            self.play(GrowArrow(ba), FadeIn(b_lab))

        rows = VGroup(
            MathTex(r"F_x", r"=", r"\tau(y{+}dy)\,A - \tau(y)\,A"),
            MathTex(r"\approx", r"{\partial \tau \over \partial y}\, dy\, A"),
            MathTex(r"=", r"{\partial \over \partial y}\Big(\mu {\partial u \over \partial y}\Big)\, dV"),
            MathTex(r"=", r"\mu\, {\partial^2 u \over \partial y^2}\, dV"),
        )
        for r in rows:
            r.scale(0.85)
        rows.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        for r in rows[1:]:
            r.shift(RIGHT * (rows[0][1].get_left()[0] - r[0].get_left()[0]))
        rows.move_to(RIGHT * 2.7 + DOWN * 0.1)
        res = MathTex(r"{F_x \over dV}", r"=", r"\mu {\partial^2 u \over \partial y^2}", font_size=50)
        res[2].set_color(C.VISCOUS)
        res.next_to(rows, DOWN, buff=0.55)
        res_box = caption_box(res, color=C.VISCOUS)

        with self.voiceover(
            "Once again, the net force comes from a difference. <bookmark mark='d'/> It's partial tau partial y, times dy times A. "
            "<bookmark mark='s'/> Plug in the stress, and dividing by the volume, <bookmark mark='r'/> the force per unit volume is "
            "mu times the second derivative of u with respect to y."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("d")
            self.play(TransformFromCopy(rows[0][2], rows[1][1]), FadeIn(rows[1][0]))
            vo.wait_until("s")
            self.play(TransformFromCopy(rows[1][1], rows[2][1]), FadeIn(rows[2][0]), Indicate(self.law))
            self.play(TransformFromCopy(rows[2][1], rows[3][1]), FadeIn(rows[3][0]))
            vo.wait_until("r")
            self.play(Write(res), Create(res_box))

        net_lab = label(r"net force $\propto$ curvature", font_size=32, color=YELLOW).next_to(ax, UP, buff=0.05).shift(RIGHT * 0.6)
        with self.voiceover(
            "Notice what this means. <bookmark mark='s'/> If the velocity profile is a straight line, the second derivative is "
            "zero: the pull from above exactly balances the drag from below. <bookmark mark='c'/> Viscosity only produces a net "
            "force where the profile curves."
        ) as vo:
            vo.wait_until("s")
            self.play(shape.animate.set_value(0.0), run_time=2)
            self.wait(0.5)
            vo.wait_until("c")
            self.play(shape.animate.set_value(1.0), run_time=2)
            self.play(FadeIn(net_lab))

        lap = MathTex(
            r"\mu\Big({\partial^2 \over \partial x^2} + {\partial^2 \over \partial y^2} + {\partial^2 \over \partial z^2}\Big)\vu",
            r"=", r"\mu \nabla^2 \vu", font_size=44,
        )
        lap[0].set_color(C.VISCOUS)
        lap[2].set_color(C.VISCOUS)
        lap.to_edge(DOWN, buff=0.55).shift(RIGHT * 2.3)
        lap_box = caption_box(lap[2], color=C.VISCOUS)
        foot = MathTex(
            r"\text{(full stress: }\ \nabla\cdot\big[\mu(\nabla\vu + \nabla\vu^{\mathsf T})\big]"
            r" = \mu\nabla^2\vu + \mu\nabla(\nabla\cdot\vu) = \mu\nabla^2\vu\text{, since }\nabla\cdot\vu = 0\text{)}",
            font_size=24, color=C.DIM,
        ).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "When you account for sliding in every direction, and use the fact that the flow is incompressible, "
            "all these second derivatives add up to one operator: <bookmark mark='l'/> the Laplacian, written del squared."
        ) as vo:
            self.play(FadeOut(VGroup(rows, net_lab)), VGroup(res, res_box).animate.shift(UP * 2.4))
            self.play(Write(lap[0]))
            vo.wait_until("l")
            self.play(Write(lap[1:]), Create(lap_box))
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.lap = VGroup(lap[2], lap_box)
        self.clear_scene(self.lap, extra=[self.lap.animate.to_corner(UR, buff=0.5)])

    # ------------------------------------------------------------------
    def laplacian_intuition(self):
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 3, 1], x_length=7.0, y_length=3.6,
                  axis_config={"include_ticks": False, "stroke_color": GREY_B}).move_to(LEFT * 2.8 + UP * 1.3)

        def f(x):
            return 1.2 + 0.9 * np.sin(1.1 * x - 0.6) + 0.35 * np.sin(2.3 * x)

        graph = ax.plot(f, x_range=[0.1, 5.9], color=C.VELOCITY, stroke_width=4)
        flab = MathTex("f(x)", font_size=36, color=C.VELOCITY).next_to(graph.get_end(), RIGHT, buff=0.1)
        xt = ValueTracker(2.1)
        hh = 0.9

        def pts():
            x = xt.get_value()
            return [ax.c2p(x - hh, f(x - hh)), ax.c2p(x, f(x)), ax.c2p(x + hh, f(x + hh))]

        dots = always_redraw(lambda: VGroup(Dot(pts()[0], color=GREY_A), Dot(pts()[1], color=WHITE, radius=0.1),
                                            Dot(pts()[2], color=GREY_A)))
        chord = always_redraw(lambda: DashedLine(pts()[0], pts()[2], color=GREY_B, stroke_width=2))
        avg = always_redraw(lambda: Dot((pts()[0] + pts()[2]) / 2, color=YELLOW, radius=0.09))
        gap = always_redraw(lambda: Arrow(pts()[1], (pts()[0] + pts()[2]) / 2, buff=0, color=C.VISCOUS, stroke_width=6,
                                          max_tip_length_to_length_ratio=0.35))
        ticks = always_redraw(lambda: VGroup(
            MathTex(r"x{-}h", font_size=28).next_to(ax.c2p(xt.get_value() - hh, 0), DOWN, buff=0.15),
            MathTex(r"x", font_size=28).next_to(ax.c2p(xt.get_value(), 0), DOWN, buff=0.15),
            MathTex(r"x{+}h", font_size=28).next_to(ax.c2p(xt.get_value() + hh, 0), DOWN, buff=0.15),
        ))
        avg_l = label(r"average of neighbors", font_size=28, color=YELLOW)
        avg_l.add_updater(lambda m: m.next_to(avg, UR, buff=0.1))

        with self.voiceover(
            "The Laplacian has a wonderful intuition. <bookmark mark='p'/> Compare a value at some point "
            "<bookmark mark='n'/> to the average of its neighbors."
        ) as vo:
            self.play(Create(ax), Create(graph), FadeIn(flab))
            vo.wait_until("p")
            self.add(ticks)
            self.play(FadeIn(dots))
            vo.wait_until("n")
            self.play(Create(chord), FadeIn(avg), FadeIn(avg_l))
            self.play(GrowArrow(gap))

        taylor = VGroup(
            MathTex(r"f(x{+}h)", r"=", r"f(x) + h f'(x) + \tfrac{h^2}{2} f''(x) + \cdots", font_size=34),
            MathTex(r"f(x{-}h)", r"=", r"f(x) - h f'(x) + \tfrac{h^2}{2} f''(x) - \cdots", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        result = MathTex(
            r"f''(x)", r"\approx", r"{2 \over h^2}", r"\Big[\,", r"\tfrac{f(x+h) + f(x-h)}{2}", r"-", r"f(x)", r"\,\Big]",
            font_size=40,
        )
        result[0].set_color(C.VISCOUS)
        result[4].set_color(YELLOW)
        VGroup(taylor, result).arrange(DOWN, buff=0.4).to_edge(DOWN, buff=0.35)
        rbox = caption_box(result, color=C.VISCOUS)
        add_note = label(r"add them:", font_size=26, color=C.DIM).next_to(taylor, LEFT, buff=0.3)

        with self.voiceover(
            "Using a Taylor expansion on both sides and adding, the first derivatives cancel, and the second derivative is, "
            "up to a constant, <bookmark mark='r'/> the average of the neighbors minus the value at the point itself."
        ) as vo:
            self.play(FadeIn(taylor, shift=UP * 0.2), FadeIn(add_note))
            vo.wait_until("r")
            self.play(Write(result), Create(rbox))

        with self.voiceover(
            "So the Laplacian is positive where the value sits below its surroundings, like the bottom of a "
            "<bookmark mark='v'/> valley, and negative at <bookmark mark='p'/> a peak."
        ) as vo:
            self.play(FadeOut(taylor), FadeOut(add_note))
            vo.wait_until("v")
            self.play(xt.animate.set_value(3.95), run_time=1.8)
            vo.wait_until("p")
            self.play(xt.animate.set_value(1.25), run_time=1.8)

        # 2D stencil
        grid = VGroup()
        sp = 0.85
        center = np.array([4.6, 0.9, 0])
        for i in range(-2, 3):
            for j in range(-2, 3):
                grid.add(Dot(center + sp * np.array([i, j, 0]), radius=0.05, color=GREY_D))
        c_dot = Dot(center, radius=0.12, color=WHITE)
        nbrs = VGroup(*[Dot(center + sp * d, radius=0.1, color=YELLOW) for d in (LEFT, RIGHT, UP, DOWN)])
        links = VGroup(*[Line(center, n.get_center(), color=YELLOW, stroke_width=2) for n in nbrs])
        st = MathTex(r"\nabla^2 f", r"\approx", r"{4 \over h^2}", r"\big[\,\text{avg of neighbors} - f\,\big]", font_size=32)
        st[0].set_color(C.VISCOUS)
        st.next_to(grid, DOWN, buff=0.3).shift(LEFT * 0.4)
        with self.voiceover(
            "In two or three dimensions it's the same story, just averaging over neighbors in every direction."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(c_dot))
            self.play(Create(links), FadeIn(nbrs))
            self.play(Write(st))
        self.clear_scene(self.lap)

    # ------------------------------------------------------------------
    def smoothing(self):
        ax = Axes(x_range=[0, PI, 1], y_range=[-1.6, 1.6, 1], x_length=10.5, y_length=4.4,
                  axis_config={"include_ticks": False, "stroke_color": GREY_B}).move_to(DOWN * 0.3)
        modes = [(1, 0.5), (3, 0.55), (5, -0.45), (8, 0.3), (13, -0.2)]
        nu = 0.012
        t = ValueTracker(0.0)

        def u(x):
            return sum(a * np.sin(k * x) * np.exp(-nu * k * k * t.get_value()) for k, a in modes)

        def lap(x):
            return sum(-k * k * a * np.sin(k * x) * np.exp(-nu * k * k * t.get_value()) for k, a in modes)

        graph = always_redraw(lambda: ax.plot(u, x_range=[0, PI], color=C.VELOCITY, stroke_width=4))
        xs = np.linspace(0.12, PI - 0.12, 26)

        def arrows():
            g = VGroup()
            for x in xs:
                v = 0.012 * lap(x)
                v = np.sign(v) * min(abs(v), 1.1)
                if abs(v) < 0.04:
                    continue
                p = ax.c2p(x, u(x))
                g.add(Arrow(p, p + UP * v * 1.4, buff=0, color=C.VISCOUS, stroke_width=4, max_tip_length_to_length_ratio=0.3))
            return g

        arr = always_redraw(arrows)
        title = MathTex(r"{\partial \vu \over \partial t}", r"=", r"\nu \nabla^2 \vu", r"+\cdots", font_size=44)
        title[0].set_color(C.TIME)
        title[2].set_color(C.VISCOUS)
        title.to_edge(UP, buff=0.5)
        ylab = label(r"velocity along a line", font_size=28, color=C.VELOCITY).move_to(ax.c2p(0.45, 1.45))

        with self.voiceover(
            "So viscosity nudges each parcel's velocity toward the average velocity of its neighbors. "
            "<bookmark mark='f'/> Fast spots get slowed down, slow spots get pulled along. <bookmark mark='g'/> Peaks get shaved off, "
            "valleys get filled in, and the velocity profile smooths out."
        ) as vo:
            self.play(FadeOut(self.lap), Create(ax), Create(graph), FadeIn(ylab))
            vo.wait_until("f")
            self.play(FadeIn(arr), Write(title))
            vo.wait_until("g")
            self.play(t.animate.set_value(30), run_time=vo.remaining(), rate_func=rate_functions.ease_out_sine)
        self.play(t.animate.set_value(45), run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def honey_vs_water(self):
        water = square_movie("viscous_pair", "water_vorticity", vmax=11.0, side=5.4)
        honey = square_movie("viscous_pair", "honey_vorticity", vmax=11.0, side=5.4)
        Group(water, honey).arrange(RIGHT, buff=0.8).shift(DOWN * 0.35)
        for m in (water, honey):
            m.set_alpha(0.0)
            m.rate = 0.0
        wl = label(r"low viscosity (like water)", font_size=34).next_to(water, UP, buff=0.25)
        hl = label(r"high viscosity (like honey)", font_size=34).next_to(honey, UP, buff=0.25)
        frames = VGroup(frame_rect(water), frame_rect(honey))
        with self.voiceover(
            "Here's the effect on a full flow, colored by how fast the fluid is spinning. "
            "<bookmark mark='w'/> On the left, a swirling flow with low viscosity, like water. "
            "<bookmark mark='h'/> On the right, the same starting flow with high viscosity, like honey. "
            "<bookmark mark='go'/> The honey version smears out and quickly dies away, while the water keeps its intricate "
            "structure much longer."
        ) as vo:
            self.add(water, honey)
            self.play(water.fade(1.0), honey.fade(1.0), Create(frames))
            vo.wait_until("w")
            self.play(FadeIn(wl))
            vo.wait_until("h")
            self.play(FadeIn(hl))
            vo.wait_until("go")
            water.rate = honey.rate = 1.0
        self.wait(4)
        water.rate = honey.rate = 0.0
        self.play(water.fade(0.0), honey.fade(0.0), FadeOut(VGroup(wl, hl, frames)))
        self.remove(water, honey)
