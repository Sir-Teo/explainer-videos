from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import caption_box, label, ns_equation
from videos.navier_stokes.s04_material_derivative import YC, h, nozzle_flow


def mini_field(func, center, size=3.2, color=C.VELOCITY):
    f = ArrowVectorField(
        lambda p: func(p - center),
        x_range=[center[0] - size / 2, center[0] + size / 2, 0.45],
        y_range=[center[1] - size / 2, center[1] + size / 2, 0.45],
        color=color,
        length_func=lambda n: 0.36 * np.tanh(1.2 * n),
    )
    return f


class Incompressibility(VoiceoverScene):
    def construct(self):
        self.counting()
        self.box_derivation()
        self.three_fields()
        self.nozzle_callback()

    # ------------------------------------------------------------------
    def counting(self):
        eq = ns_equation(font_size=44).to_edge(UP, buff=0.8)
        eqs = VGroup(label(r"Equations", font_size=40), MathTex(r"3", font_size=72),
                     label(r"($x$, $y$, $z$ components)", font_size=26, color=C.DIM)).arrange(DOWN, buff=0.25)
        unk = VGroup(label(r"Unknowns", font_size=40), MathTex(r"4", font_size=72),
                     MathTex(r"u,\ v,\ w,\ p", font_size=32, color=C.DIM)).arrange(DOWN, buff=0.25)
        VGroup(eqs, unk).arrange(RIGHT, buff=3.0).shift(DOWN * 0.6)
        q = MathTex(r"3 < 4", font_size=48, color=YELLOW).move_to(DOWN * 0.6)
        with self.voiceover(
            "We now have one vector equation, <bookmark mark='e'/> three equations in three dimensions. "
            "<bookmark mark='u'/> But there are four unknowns: three velocity components and the pressure. "
            "<bookmark mark='m'/> The missing equation comes from conservation of mass."
        ) as vo:
            self.play(FadeIn(eq, shift=DOWN * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(eqs))
            vo.wait_until("u")
            self.play(FadeIn(unk))
            self.play(Write(q))
            vo.wait_until("m")
        self.clear_scene()

    # ------------------------------------------------------------------
    def box_derivation(self):
        box = Square(2.6, color=WHITE, stroke_width=3, fill_color=C.VELOCITY, fill_opacity=0.15).move_to(LEFT * 4.15 + DOWN * 0.1)
        c = box.get_center()
        s = 1.3
        in_l = Arrow(c + LEFT * (s + 1.3), c + LEFT * (s + 0.05), buff=0, color=C.VELOCITY, stroke_width=7)
        out_r = Arrow(c + RIGHT * (s + 0.05), c + RIGHT * (s + 1.7), buff=0, color=C.VELOCITY, stroke_width=7)
        in_b = Arrow(c + DOWN * (s + 1.2), c + DOWN * (s + 0.05), buff=0, color=C.VELOCITY, stroke_width=7)
        out_t = Arrow(c + UP * (s + 0.05), c + UP * (s + 0.9), buff=0, color=C.VELOCITY, stroke_width=7)
        lab = lambda tex, m, d: MathTex(tex, font_size=32).next_to(m, d, buff=0.1)  # noqa: E731
        l_in_l = lab(r"u(x)\,dy", in_l, UP)
        l_out_r = lab(r"u(x{+}dx)\,dy", out_r, UP)
        l_in_b = lab(r"v(y)\,dx", in_b, RIGHT)
        l_out_t = lab(r"v(y{+}dy)\,dx", out_t, RIGHT)
        bl = box.get_corner(DL)
        dx_arrow = DoubleArrow(bl + UP * 0.3 + RIGHT * 0.45, bl + UP * 0.3 + RIGHT * 2.5, buff=0, stroke_width=2.5,
                               color=GREY_A, tip_length=0.15)
        dy_arrow = DoubleArrow(bl + RIGHT * 0.3 + UP * 0.45, bl + RIGHT * 0.3 + UP * 2.5, buff=0, stroke_width=2.5,
                               color=GREY_A, tip_length=0.15)
        dxl = VGroup(dx_arrow, MathTex("dx", font_size=32).next_to(dx_arrow, UP, buff=0.08))
        dyl = VGroup(dy_arrow, MathTex("dy", font_size=32).next_to(dy_arrow, RIGHT, buff=0.08))
        rule = label(r"incompressible: \emph{what flows in must flow out}", font_size=34).to_edge(UP, buff=0.4)

        with self.voiceover(
            "Water is, for all practical purposes, incompressible. You can't squeeze a parcel of it into a smaller volume. "
            "<bookmark mark='r'/> So for any small region, whatever flows in must flow out."
        ) as vo:
            self.play(FadeIn(box), FadeIn(dyl))
            self.add(dxl)
            vo.wait_until("r")
            self.play(Write(rule))

        with self.voiceover(
            "Let's count the flow through a small box. <bookmark mark='l'/> Through the left face, fluid enters at a rate of u "
            "at x, times the face's length, dy. <bookmark mark='r'/> Through the right face, it leaves at a rate of u at x plus dx, times dy."
        ) as vo:
            vo.wait_until("l")
            self.play(GrowArrow(in_l), FadeIn(l_in_l))
            vo.wait_until("r")
            self.play(GrowArrow(out_r), FadeIn(l_out_r))

        rows = VGroup(
            MathTex(r"\text{out} - \text{in}\ (x)", r"=", r"\big[u(x{+}dx) - u(x)\big]\,dy", r"\approx",
                    r"{\partial u \over \partial x}\,dx\,dy"),
            MathTex(r"\text{out} - \text{in}\ (y)", r"=", r"\big[v(y{+}dy) - v(y)\big]\,dx", r"\approx",
                    r"{\partial v \over \partial y}\,dx\,dy"),
        )
        for r in rows:
            r.scale(0.68)
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.55 + UP * 1.3)
        rows[1].shift(RIGHT * (rows[0][1].get_x() - rows[1][1].get_x()))

        with self.voiceover(
            "The net horizontal outflow is the difference, <bookmark mark='d'/> partial u partial x times dx dy. "
            "<bookmark mark='y'/> Likewise, the net outflow through the top and bottom is partial v partial y times dx dy."
        ) as vo:
            self.play(Write(rows[0][:3]))
            vo.wait_until("d")
            self.play(Write(rows[0][3:]))
            vo.wait_until("y")
            self.play(GrowArrow(in_b), FadeIn(l_in_b), GrowArrow(out_t), FadeIn(l_out_t))
            self.play(Write(rows[1]))

        div = MathTex(r"{\text{net outflow} \over dV}", r"=", r"{\partial u \over \partial x} + {\partial v \over \partial y}",
                      r"+ {\partial w \over \partial z}", r"=", r"\nabla \cdot \vu", font_size=40)
        div[5].set_color(C.DIVERGENCE)
        div[3].set_opacity(0.6)
        div.next_to(rows, DOWN, buff=0.7).shift(LEFT * 0.4)
        div_name = label(r"the \emph{divergence} of $\mathbf{u}$", font_size=30, color=C.DIVERGENCE).next_to(div, DOWN, buff=0.3)
        with self.voiceover(
            "The total, per unit volume, is partial u partial x plus partial v partial y, <bookmark mark='z'/> plus partial w partial z "
            "in three dimensions. <bookmark mark='d'/> This is the divergence of u, written del dot u. It measures how much fluid "
            "is streaming out of each point."
        ) as vo:
            self.play(Write(div[:3]))
            vo.wait_until("z")
            self.play(FadeIn(div[3]))
            vo.wait_until("d")
            self.play(Write(div[4:]), FadeIn(div_name))
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_fields(self):
        centers = [np.array([-4.6, 0.2, 0]), np.array([0, 0.2, 0]), np.array([4.6, 0.2, 0])]
        funcs = [lambda p: 0.7 * np.array([p[0], p[1], 0]),
                 lambda p: -0.7 * np.array([p[0], p[1], 0]),
                 lambda p: 0.7 * np.array([-p[1], p[0], 0])]
        texs = [r"\nabla\cdot\vu > 0", r"\nabla\cdot\vu < 0", r"\nabla\cdot\vu = 0"]
        names = ["source", "sink", "swirl: in = out"]
        panels = []
        for c, f, t, n in zip(centers, funcs, texs, names):
            fld = mini_field(f, c)
            circ = Circle(0.75, color=C.DIVERGENCE, stroke_width=3).move_to(c)
            tex = MathTex(t, font_size=40).next_to(fld, DOWN, buff=0.35)
            tex[0][:4].set_color(C.DIVERGENCE)
            name = label(n, font_size=30, color=C.DIM).next_to(tex, DOWN, buff=0.15)
            panels.append(VGroup(fld, circ, tex, name))

        with self.voiceover(
            "Here's a field with positive divergence: fluid gushes out of every point, like a source. "
            "<bookmark mark='s'/> Here's negative divergence, a sink. <bookmark mark='z'/> And here's a field with zero divergence: "
            "fluid swirls and streams around, but around every little region, inflow exactly balances outflow."
        ) as vo:
            self.play(Create(panels[0][0], lag_ratio=0.02), Create(panels[0][1]), FadeIn(panels[0][2:]))
            vo.wait_until("s")
            self.play(Create(panels[1][0], lag_ratio=0.02), Create(panels[1][1]), FadeIn(panels[1][2:]))
            vo.wait_until("z")
            self.play(Create(panels[2][0], lag_ratio=0.02), Create(panels[2][1]), FadeIn(panels[2][2:]))

        final = MathTex(r"\nabla \cdot \vu", r"=", r"0", font_size=72)
        final[0].set_color(C.DIVERGENCE)
        fbox = caption_box(final, color=C.DIVERGENCE, buff=0.3)
        tag = label(r"incompressibility: the 4th equation", font_size=34, color=C.DIVERGENCE).next_to(fbox, DOWN, buff=0.3)
        with self.voiceover(
            "Incompressibility means the divergence is zero everywhere, always. <bookmark mark='f'/> That's our fourth equation."
        ) as vo:
            self.play(FadeOut(VGroup(*panels)))
            vo.wait_until("f")
            self.play(Write(final), Create(fbox), FadeIn(tag))
        self.clear_scene(final, extra=[final.animate.scale(0.6).to_corner(UR, buff=0.5)])
        self.final = final

    # ------------------------------------------------------------------
    def nozzle_callback(self):
        top = ParametricFunction(lambda t: [t, YC + h(t), 0], t_range=[-6.8, 6.8], color=GREY_B, stroke_width=5)
        bot = ParametricFunction(lambda t: [t, YC - h(t), 0], t_range=[-6.8, 6.8], color=GREY_B, stroke_width=5)
        xa, xb = -4.5, 4.3
        sec_a = DashedLine([xa, YC - h(xa), 0], [xa, YC + h(xa), 0], color=C.DIVERGENCE)
        sec_b = DashedLine([xb, YC - h(xb), 0], [xb, YC + h(xb), 0], color=C.DIVERGENCE)
        arrs = VGroup()
        for x in (xa, xb):
            for frac in np.linspace(-0.7, 0.7, 5):
                p = np.array([x + 0.12, YC + frac * h(x), 0])
                v = nozzle_flow(p)
                arrs.add(Arrow(p, p + 0.3 * v, buff=0, color=C.VELOCITY, stroke_width=4, max_tip_length_to_length_ratio=0.3))
        la = MathTex(r"U_1 A_1", font_size=40).next_to(sec_a, DOWN, buff=0.3)
        lb = MathTex(r"U_2 A_2", font_size=40).next_to(sec_b, DOWN, buff=0.3)
        law = MathTex(r"U_1 A_1", r"=", r"U_2 A_2", font_size=52).to_edge(DOWN, buff=0.5)
        law2 = label(r"smaller area $\Rightarrow$ faster flow", font_size=32, color=YELLOW).next_to(law, RIGHT, buff=0.6)
        with self.voiceover(
            "And it explains our nozzle. <bookmark mark='q'/> The flow rate through the pipe must be the same at every "
            "cross-section, <bookmark mark='a'/> so where the area shrinks, the speed must grow."
        ) as vo:
            self.play(Create(top), Create(bot))
            vo.wait_until("q")
            self.play(Create(sec_a), Create(sec_b), LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.05),
                      FadeIn(la), FadeIn(lb))
            self.play(Write(law))
            vo.wait_until("a")
            self.play(FadeIn(law2, shift=LEFT * 0.2))
        self.wait(0.5)
        self.clear_scene()
