from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, load, plain_axes, polyline, square_axes, zgrid


class Holomorphic(VoiceoverScene):
    def construct(self):
        self.card()
        self.derivative()
        self.conformal()
        self.zeros()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Complex derivatives are rotations", r"What does a complex derivative do to a small square?",
                            lit=(1821,), part=7)
        with self.voiceover("Chapter one: what it means for a function of a complex variable to have a derivative."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derivative(self):
        d = load("conformal")
        js, jb, pts = d["jac_sq"], d["jac_bad"], d["pts"]
        z0 = complex(pts[0])
        h = 0.18
        panels = []
        for k, (F, c, ttl) in enumerate(((lambda Z: Z, z0, r"\text{near } z_0 = 0.6 + 0.4i"),
                                         (lambda Z: Z * Z, z0 * z0, r"f(z) = z^2"),
                                         (lambda Z: Z + 0.4j * np.conj(Z), z0 + 0.4j * np.conj(z0),
                                          r"g(z) = z + 0.4i\,\bar z"))):
            W = 0.5
            ax = square_axes([c.real - W, c.real + W, 0.25], [c.imag - W, c.imag + W, 0.25], 3.4).move_to(
                [-4.6 + 4.6 * k, -0.3, 0])
            ax.set_opacity(0.0)
            frame = Square(side_length=3.4, color=GREY_D, stroke_width=1.5).move_to(ax.c2p(c.real, c.imag))
            grid = zgrid(ax, F, (z0.real - h, z0.real + h), (z0.imag - h, z0.imag + h), n=5, stroke_width=2.5,
                         colors=(C.SEQ, C.APPROX))
            t = MathTex(ttl, font_size=28).next_to(frame, UP, buff=0.12)
            panels.append(VGroup(frame, grid, t))
        a, b = js[0][0, 0], js[0][1, 0]
        fp = complex(a, b)
        assert abs(fp - 2 * z0) < 1e-6
        reads = VGroup(
            MathTex(rf"Df = \begin{{pmatrix}} {js[0][0, 0]:.2f} & {js[0][0, 1]:.2f} \\ {js[0][1, 0]:.2f} & "
                    rf"{js[0][1, 1]:.2f} \end{{pmatrix}}", font_size=28, color=C.CONNECTED_SET),
            MathTex(rf"= {abs(fp):.3f} \times \text{{rotation by }} {math.degrees(math.atan2(b, a)):.1f}^\circ", font_size=26,
                    color=C.CONNECTED_SET),
            MathTex(rf"Dg = \begin{{pmatrix}} {jb[0][0, 0]:.2f} & {jb[0][0, 1]:.2f} \\ {jb[0][1, 0]:.2f} & "
                    rf"{jb[0][1, 1]:.2f} \end{{pmatrix}}", font_size=28, color=C.PATHOLOGY),
            MathTex(r"\text{squares} \to \text{rhombi}", font_size=26, color=C.PATHOLOGY),
        )
        reads[0].next_to(panels[1], DOWN, buff=0.15)
        reads[1].next_to(reads[0], DOWN, buff=0.08)
        reads[2].next_to(panels[2], DOWN, buff=0.15)
        reads[3].next_to(reads[2], DOWN, buff=0.08)
        cr = VGroup(
            MathTex(r"f'(z) = \lim_{h \to 0,\ h \in \C} \frac{f(z + h) - f(z)}{h}", font_size=30),
            MathTex(r"u_x = v_y, \quad u_y = -v_x \quad (\text{Cauchy--Riemann})", font_size=28, color=C.EPS),
        ).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> A complex derivative is a limit of difference quotients, where h may approach zero "
            "from any direction in the plane. That's a much stronger demand than in two real variables. "
            "<bookmark mark='b'/> Take a small square near z zero. Under z squared, it comes out as a square again, "
            "turned and enlarged: the derivative is multiplication by the complex number two z zero, which is a "
            "rotation by 33.7 degrees and a stretch by 1.44. <bookmark mark='c'/> A real-linear map that isn't "
            "complex-linear, like z plus 0.4 i times z bar, turns the square into a rhombus. "
            "<bookmark mark='d'/> In coordinates, the Jacobian must be a rotation times a scaling: the Cauchy-Riemann "
            "equations."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cr[0]), FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(TransformFromCopy(panels[0][1], panels[1][1]), FadeIn(panels[1][0]), FadeIn(panels[1][2]),
                      run_time=1.8)
            self.play(FadeIn(reads[:2]))
            vo.wait_until("c")
            self.play(TransformFromCopy(panels[0][1], panels[2][1]), FadeIn(panels[2][0]), FadeIn(panels[2][2]),
                      run_time=1.8)
            self.play(FadeIn(reads[2:]))
            vo.wait_until("d")
            self.play(FadeIn(cr[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def conformal(self):
        d = load("conformal")
        angs_sq, angs_exp = d["ang_sq"], d["ang_exp"]
        ax = square_axes([-0.2, 2.2, 1], [-0.2, 2.6, 1], 1.45).move_to([-4.2, -0.6, 0])
        ax.set_opacity(0.3)
        g1 = zgrid(ax, lambda Z: Z * Z, (0.3, 1.4), (0.15, 0.95), n=9, stroke_width=2, colors=(C.SEQ, C.APPROX))
        l1 = MathTex(r"z^2 \text{ on } [0.3, 1.4] \times [0.15, 0.95]", font_size=26).next_to(ax, UP, buff=0.1)
        bx = square_axes([-2.9, 2.9, 1], [-2.9, 2.9, 1], 0.7).move_to([0.6, -0.6, 0])
        bx.set_opacity(0.3)
        g2 = zgrid(bx, np.exp, (-1.0, 1.0), (-1.2, 1.2), n=9, stroke_width=2, colors=(C.SEQ, C.APPROX))
        l2 = MathTex(r"e^z \text{ on } [-1, 1] \times [-1.2, 1.2]", font_size=26).next_to(bx, UP, buff=0.1)
        side = VGroup(
            label(r"blue lines $y = c$, \ pink lines $x = c$:", font_size=24),
            label(r"still perpendicular \ (angles measured", font_size=24),
            label(r"at four points):", font_size=24),
            MathTex(r"z^2:\ " + r",\ ".join(f"{a:.4f}" for a in angs_sq) + r"^\circ", font_size=22, color=C.EPS),
            MathTex(r"e^z:\ " + r",\ ".join(f"{a:.4f}" for a in angs_exp) + r"^\circ", font_size=22, color=C.EPS),
            label(r"holomorphic with $f' \ne 0$ $\Rightarrow$ conformal", font_size=24, color=C.CONNECTED_SET),
            label(r"at $0$, \ $(z^2)' = 0$ \ and $z^2$ doubles angles", font_size=22, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.0, -0.5, 0])
        for r_ in side:
            if r_.width > 3.9:
                r_.width = 3.9
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.05, -0.5, 0])
        assert np.allclose(angs_sq, 90, atol=1e-6) and np.allclose(angs_exp, 90, atol=1e-6)
        head = label(r"Holomorphic maps preserve angles", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Since the derivative is a rotation and a scaling, small shapes keep their angles. "
            "<bookmark mark='b'/> Here's a grid under z squared: its lines bend, but they still cross at right "
            "angles. <bookmark mark='c'/> Under the exponential, the vertical lines become circles and the horizontal "
            "ones become rays, still perpendicular. <bookmark mark='d'/> Measured at four points, the angles are "
            "ninety degrees to every digit shown. Wherever the derivative isn't zero, a holomorphic map is "
            "conformal; at a zero of the derivative, like z squared at the origin, angles get multiplied."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(bx))
            vo.wait_until("b")
            self.play(Create(g1), FadeIn(l1), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(g2), FadeIn(l2), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[:5]))
            self.play(FadeIn(side[5:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zeros(self):
        ax = plain_axes([-0.3, 0.3, 0.1], [-0.1, 0.1, 0.05], 5.4, 3.0).move_to([-3.6, -0.4, 0])
        x = np.concatenate([np.linspace(-0.3, -1e-3, 4000), np.linspace(1e-3, 0.3, 4000)])
        y = x**2 * np.sin(1 / x)
        g = VGroup(polyline(ax, x[:4000], y[:4000], color=C.FUNC, stroke_width=2.5),
                   polyline(ax, x[4000:], y[4000:], color=C.FUNC, stroke_width=2.5))
        zs = 1 / (np.pi * np.arange(2, 40))
        zd = VGroup(*[Dot(ax.c2p(s * z, 0), radius=0.03, color=C.PATHOLOGY) for z in zs for s in (1, -1)])
        g_l = VGroup(MathTex(r"x^2 \sin\tfrac1x \ \text{on } \R", font_size=28, color=C.FUNC),
                     label(r"differentiable; \ zeros $\frac{1}{k\pi}$ pile up at $0$", font_size=22, color=C.PATHOLOGY)
                     ).arrange(DOWN, buff=0.08).next_to(ax, DOWN, buff=0.15)
        cx = square_axes([-2.6, 2.6, 1], [-1.3, 1.3, 1], 1.15).move_to([3.3, 0.0, 0])
        img = cplot(cx, lambda Z: np.sin(np.pi * Z), (-2.6, 2.6), (-1.3, 1.3))
        frame = Rectangle(width=5.2 * 1.15, height=2.6 * 1.15, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 0))
        zl = VGroup(*[Circle(radius=0.13, color=WHITE, stroke_width=2).move_to(cx.c2p(k, 0)) for k in (-2, -1, 0, 1, 2)])
        c_l = VGroup(MathTex(r"\sin \pi z \ \text{on } \C", font_size=28),
                     label(r"zeros at the integers, \ each one isolated", font_size=22, color=C.EPS)
                     ).arrange(DOWN, buff=0.08).next_to(frame, DOWN, buff=0.15)
        thm = VGroup(
            label(r"\textbf{RCA 10.6} \ a power series is holomorphic in its disk, \ differentiated term by term", font_size=24),
            label(r"\textbf{RCA 10.18} \ the zeros of a nonconstant holomorphic $f$ on a region are isolated",
                  font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(UP, buff=0.3)
        assert np.all(np.abs(np.sin(np.pi * np.arange(-2, 3))) < 1e-12)
        with self.voiceover(
            "<bookmark mark='a'/> Two first consequences. A power series is holomorphic inside its disk of "
            "convergence, and you can differentiate it term by term: one more interchange of limits, made legal. "
            "<bookmark mark='b'/> And zeros behave. On the real line, x squared sine one over x is differentiable, "
            "and its zeros pile up at zero. <bookmark mark='c'/> A holomorphic function can't do that unless it's "
            "zero everywhere: its zeros are isolated, like the integers for sine of pi z, each a dark point with every "
            "color around it once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm[0]))
            vo.wait_until("b")
            self.play(Create(ax), Create(g), FadeIn(g_l))
            self.play(LaggedStart(*[FadeIn(z_) for z_ in zd], lag_ratio=0.02), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(img), Create(frame), FadeIn(c_l), FadeIn(thm[1]))
            self.play(Create(zl))
        self.wait(0.4)
        self.clear_scene()
