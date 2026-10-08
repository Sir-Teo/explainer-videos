from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import gammas, label, note, zeta

N_ARROWS = 10
PANEL_X = -4.75
PANEL_LEFT = -6.85  # left edge of the text panel


class ComplexView:
    """A zoomable window onto the complex plane: z -> origin + scale * (Re z, Im z)."""

    def __init__(self, origin, scale, box):
        self.origin = np.array(origin, dtype=float)
        self.k = ValueTracker(scale)
        self.box = box  # (xmin, xmax, ymin, ymax) in screen units

    def p(self, z: complex) -> np.ndarray:
        k = self.k.get_value()
        return self.origin + k * np.array([z.real, z.imag, 0.0])

    def pts(self, zs) -> np.ndarray:
        zs = np.asarray(zs)
        k = self.k.get_value()
        return np.stack([self.origin[0] + k * zs.real, self.origin[1] + k * zs.imag, np.zeros(len(zs))], axis=1)

    def axes(self) -> VGroup:
        x0, x1, y0, y1 = self.box
        o = self.origin
        k = self.k.get_value()
        g = VGroup(Line([x0, o[1], 0], [x1, o[1], 0], color=GREY_C, stroke_width=1.5),
                   Line([o[0], y0, 0], [o[0], y1, 0], color=GREY_C, stroke_width=1.5))
        step = 1 if k > 0.9 else 2
        for v in range(-6, 7, step):
            if v == 0:
                continue
            x = o[0] + k * v
            if x0 + 0.2 < x < x1 - 0.2:
                g.add(Line([x, o[1] - 0.07, 0], [x, o[1] + 0.07, 0], color=GREY_C, stroke_width=1.5))
                g.add(MathTex(str(v), font_size=20, color=GREY_C).move_to([x, o[1] - 0.25, 0]))
            y = o[1] + k * v
            if y0 + 0.2 < y < y1 - 0.2:
                g.add(Line([o[0] - 0.07, y, 0], [o[0] + 0.07, y, 0], color=GREY_C, stroke_width=1.5))
                g.add(MathTex(f"{v}i", font_size=20, color=GREY_C).move_to([o[0] - 0.3, y, 0]))
        return g


def sums(s: complex, N: int) -> np.ndarray:
    n = np.arange(1, N + 1)
    return np.concatenate([[0], np.cumsum(np.exp(-s * np.log(n)))])


def center(s: complex, N: int) -> complex:
    S = sums(s, N)[-1]
    return S - N ** (1 - s) / (1 - s) - 0.5 * N ** (-s)


class ComplexZeta(VoiceoverScene):
    def construct(self):
        self.sig = ValueTracker(1.5)
        self.t = ValueTracker(0.0)
        self.N = ValueTracker(300)
        self.view = ComplexView(origin=[-0.3, -0.4, 0], scale=2.4, box=(-2.4, 7.0, -3.9, 3.6))
        self.formula()
        self.arrows_and_spiral()
        self.diverge()
        self.continuation()
        self.first_zero()

    def s(self) -> complex:
        return complex(self.sig.get_value(), self.t.get_value())

    # ------------------------------------------------------------------
    def formula(self):
        s_def = MathTex(r"s", r"=", r"\sigma", r"+", r"i\,t", font_size=48)
        s_def[2].set_color(BLUE_B)
        s_def[4].set_color(C.CHARACTER)
        split = MathTex(r"n^{-s}", r"=", r"n^{-\sigma}", r"\cdot", r"e^{-i\,t\ln n}", font_size=48)
        split[2].set_color(BLUE_B)
        split[4].set_color(C.CHARACTER)
        VGroup(s_def, split).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([PANEL_X, 2.2, 0])
        b1 = Brace(split[2], DOWN, buff=0.12, color=BLUE_B)
        b1l = label(r"length", font_size=28, color=BLUE_B).next_to(b1, DOWN, buff=0.08)
        b2 = Brace(split[4], DOWN, buff=0.12, color=C.CHARACTER)
        b2l = label(r"rotation by\\$-t \ln n$", font_size=28, color=C.CHARACTER).next_to(b2, DOWN, buff=0.08)

        # Unit-circle inset showing the rotation
        circ_c = np.array([PANEL_X + 0.2, -1.9, 0])
        circle = Circle(radius=0.9, color=GREY_C, stroke_width=1.5).move_to(circ_c)
        ang = ValueTracker(0.0)
        rot = always_redraw(lambda: Arrow(circ_c, circ_c + 0.9 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                                          buff=0, color=C.CHARACTER, stroke_width=4, max_tip_length_to_length_ratio=0.25))
        cl = MathTex(r"|e^{i\theta}| = 1", font_size=28, color=GREY_B).next_to(circle, DOWN, buff=0.15)

        with self.voiceover(
            "Riemann's leap was to let s be a complex number: <bookmark mark='s'/> s equals sigma plus i t. But then what does "
            "n to the minus s even mean? <bookmark mark='p'/> Split it in two. <bookmark mark='l'/> n to the minus sigma is an "
            "ordinary positive number, a length. <bookmark mark='r'/> And n to the minus i t is e to the minus i t log n: a point "
            "on the unit circle, which means a rotation, by an angle of minus t times log n."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(s_def))
            vo.wait_until("p")
            self.play(Write(split))
            vo.wait_until("l")
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("r")
            self.play(GrowFromCenter(b2), FadeIn(b2l), Create(circle), FadeIn(rot), FadeIn(cl))
            self.play(ang.animate.set_value(-2 * PI), run_time=vo.remaining(), rate_func=linear)
        target = VGroup(s_def, split).copy().scale(0.8)
        target.move_to([0, 2.95, 0]).align_to([PANEL_LEFT, 0, 0], LEFT)
        self.play(FadeOut(VGroup(b1, b1l, b2, b2l, circle, rot, cl)), Transform(VGroup(s_def, split), target))
        self.panel = VGroup(s_def, split)

    # ------------------------------------------------------------------
    def arrows_and_spiral(self):
        v = self.view
        axes = always_redraw(v.axes)

        def chain():
            s = self.s()
            S = sums(s, N_ARROWS)
            g = VGroup()
            for n in range(1, N_ARROWS + 1):
                a, b = v.p(S[n - 1]), v.p(S[n])
                g.add(Arrow(a, b, buff=0, color=interpolate_color(ManimColor(BLUE_B), ManimColor(C.CHARACTER), (n - 1) / N_ARROWS),
                            stroke_width=4, max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12))
            return g

        def tail():
            S = sums(self.s(), int(self.N.get_value()))
            m = VMobject(stroke_width=2.2, color=GREY_A)
            m.set_points_as_corners(v.pts(S[N_ARROWS:]))
            return m

        def end_dot():
            S = sums(self.s(), int(self.N.get_value()))
            return Dot(v.p(S[-1]), radius=0.06, color=WHITE)

        readout = VGroup(
            VGroup(MathTex(r"\sigma =", font_size=38, color=BLUE_B), DecimalNumber(1.5, num_decimal_places=2, font_size=38, color=BLUE_B)),
            VGroup(MathTex(r"t =", font_size=38, color=C.CHARACTER), DecimalNumber(0, num_decimal_places=2, font_size=38, color=C.CHARACTER)),
        )
        for r in readout:
            r.arrange(RIGHT, buff=0.15)
        readout.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, 1.25, 0]).align_to([PANEL_LEFT, 0, 0], LEFT)
        readout[0][1].add_updater(lambda m: m.set_value(self.sig.get_value()))
        readout[1][1].add_updater(lambda m: m.set_value(self.t.get_value()))
        self.readout = readout

        arrows = always_redraw(chain)
        path = always_redraw(tail)
        dot = always_redraw(end_dot)
        zl = always_redraw(lambda: MathTex(r"\zeta(s)", font_size=34).next_to(dot, UR, buff=0.08))
        sum_tex = MathTex(r"\zeta(s) = \sum_{n \ge 1} n^{-s}", font_size=36).move_to([0, 0.05, 0]).align_to([PANEL_LEFT, 0, 0], LEFT)

        with self.voiceover(
            "So each term of zeta becomes an arrow. <bookmark mark='a'/> Here's sigma equal to one and a half, with t equal to "
            "zero. Every arrow points to the right, and placed tip to tail, they add up along the real line."
        ) as vo:
            self.play(FadeIn(axes), FadeIn(readout), FadeIn(sum_tex))
            vo.wait_until("a")
            self.play(Create(arrows), run_time=1.5)
            self.play(Create(path), FadeIn(dot), FadeIn(zl))

        with self.voiceover(
            "Now turn up t. <bookmark mark='r'/> Each arrow rotates, and the n-th one turns at a rate proportional to log n, so "
            "the later arrows spin faster. <bookmark mark='c'/> The chain curls into a spiral, and its endpoint, right here, is "
            "zeta of s."
        ) as vo:
            vo.wait_until("r")
            self.play(self.t.animate.set_value(10.0), v.k.animate.set_value(4.2), run_time=vo.until("c") - 0.2, rate_func=smooth)
            self.play(Flash(dot.get_center(), color=WHITE, flash_radius=0.3))
        self.items = VGroup(axes, arrows, path, dot, zl)
        self.sum_tex = sum_tex

    # ------------------------------------------------------------------
    def diverge(self):
        v = self.view
        nl = VGroup(MathTex(r"\text{terms: }", font_size=32, color=GREY_B), Integer(300, font_size=32, color=GREY_B)).arrange(RIGHT, buff=0.1)
        nl.move_to([0, -0.85, 0]).align_to([PANEL_LEFT, 0, 0], LEFT)
        nl[1].add_updater(lambda m: m.set_value(int(self.N.get_value())))
        with self.voiceover(
            "Now slide sigma down toward one. <bookmark mark='o'/> The arrows shrink more slowly, and the spiral takes longer and "
            "longer to settle. <bookmark mark='b'/> Below one, it never settles at all. <bookmark mark='m'/> Keep adding terms, "
            "and the spiral just keeps unwinding outward, forever. The series diverges."
        ) as vo:
            self.play(FadeIn(nl), FadeOut(self.items[4]))
            vo.wait_until("o")
            self.play(self.sig.animate.set_value(1.0), run_time=2.5)
            vo.wait_until("b")
            self.play(self.sig.animate.set_value(0.5), v.k.animate.set_value(1.05), run_time=2.5)
            vo.wait_until("m")
            self.play(self.N.animate.set_value(700), run_time=vo.remaining(), rate_func=linear)
        self.nl = nl

    # ------------------------------------------------------------------
    def continuation(self):
        v = self.view
        cdot = always_redraw(lambda: Dot(v.p(center(self.s(), int(self.N.get_value()))), radius=0.09, color=YELLOW))
        ring = always_redraw(lambda: Circle(radius=0.2, color=YELLOW, stroke_width=2).move_to(cdot.get_center()))
        defn = MathTex(r"\zeta(s) = \lim_{N\to\infty}\Big(\sum_{n \le N} n^{-s} - \frac{N^{1-s}}{1-s}\Big)", font_size=30, color=YELLOW)
        defn.move_to([0, -2.45, 0]).align_to([PANEL_LEFT, 0, 0], LEFT)
        valid = note(r"(for $\sigma > 0$, $s \ne 1$; when $\sigma > 1$\\it is just the ordinary sum)", font_size=22)
        valid.next_to(defn, DOWN, buff=0.15).align_to(defn, LEFT)
        ac = label(r"analytic continuation", font_size=32, color=YELLOW).move_to([0, -1.6, 0]).align_to([PANEL_LEFT, 0, 0], LEFT)
        cl = always_redraw(lambda: MathTex(r"\zeta(s)", font_size=32, color=YELLOW).next_to(ring, UR, buff=0.02))
        assert abs(center(complex(0.5, 10), 700) - zeta(complex(0.5, 10))) < 1e-3

        with self.voiceover(
            "And yet, look closely at that diverging spiral. <bookmark mark='c'/> It winds around a fixed point, and that center "
            "stays put no matter how many terms you add. <bookmark mark='f'/> You can pin it down by subtracting off the steady "
            "outward drift, which is N to the one minus s, over one minus s. <bookmark mark='u'/> When sigma is above one, this "
            "is just the ordinary sum. Below one, it still gives an answer, and it's the only way to extend zeta smoothly to "
            "these values of s. <bookmark mark='a'/> This is analytic continuation, and it defines zeta everywhere in the complex "
            "plane, except at s equals one."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(cdot, scale=2), Create(ring), FadeIn(cl))
            self.play(self.N.animate.set_value(900), run_time=2, rate_func=linear)
            vo.wait_until("f")
            self.play(FadeOut(self.sum_tex), Write(defn))
            vo.wait_until("u")
            self.play(FadeIn(valid))
            vo.wait_until("a")
            self.play(FadeIn(ac, shift=UP * 0.2))
        self.cdot = VGroup(cdot, ring, cl)
        self.defn = VGroup(defn, valid, ac)

    # ------------------------------------------------------------------
    def first_zero(self):
        v = self.view
        g1 = float(gammas(1)[0])
        zero_l = label(rf"$s = \tfrac12 + {g1:.4f}\ldots\, i$", font_size=34, color=C.ZERO)
        zero_l2 = label(r"the first nontrivial zero:\\$\zeta(s) = 0$", font_size=32, color=C.ZERO)
        VGroup(zero_l2, zero_l).arrange(DOWN, buff=0.2).move_to(v.origin + DOWN * 2.6 + RIGHT * 3.9)
        assert abs(zeta(complex(0.5, g1))) < 1e-8

        with self.voiceover(
            "Now let's go hunting for a zero. <bookmark mark='t'/> Keep sigma at one half and raise t. Watch the center. "
            "<bookmark mark='z'/> At t equal to 14.1347, the spiral winds around a center that sits exactly at zero. "
            "<bookmark mark='f'/> This is the first nontrivial zero of the zeta function."
        ) as vo:
            self.play(self.N.animate.set_value(600), run_time=0.8)
            vo.wait_until("t")
            self.play(self.t.animate.set_value(g1), v.k.animate.set_value(1.4), run_time=vo.until("z") - 0.1, rate_func=smooth)
            self.play(Flash(v.p(0), color=C.ZERO, flash_radius=0.4, line_length=0.25))
            vo.wait_until("f")
            self.play(FadeIn(zero_l2), FadeIn(zero_l))
        self.wait(1)
        self.clear_scene()
