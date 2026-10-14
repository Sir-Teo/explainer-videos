from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import load, square_axes


def oriented_circle(center, radius, gap_at=-PI / 4, color=C.EPS, stroke_width=3, tip_length=0.18) -> VGroup:
    """A closed contour run counterclockwise: an open arc with an arrowhead at its end. (Circle.add_tip collapses a
    closed circle to a point, and Arc.add_tip rescales a nearly closed arc, so the arrowhead is placed by hand.)"""
    center = np.asarray(center, float)
    gap = 0.08  # the small break in the circle where the arrowhead sits, at angle gap_at
    end = gap_at - gap / 2
    arc = Arc(radius=radius, start_angle=gap_at + gap / 2, angle=TAU - gap - tip_length / radius, arc_center=center,
              color=color, stroke_width=stroke_width)
    tip = ArrowTriangleFilledTip(length=tip_length, width=tip_length, color=color)
    tip.rotate(end + PI / 2 - tip.tip_angle)  # along the counterclockwise tangent
    tip.shift(center + radius * np.array([math.cos(end), math.sin(end), 0.0]) - tip.tip_point)
    g = VGroup(arc, tip)
    assert g.width > 1.9 * radius and g.height > 1.9 * radius  # a whole circle, not the collapsed stub
    assert np.linalg.norm(arc.get_end() - tip.base) < 0.02 and abs(np.linalg.norm(arc.get_start() - center) - radius) < 1e-6
    return g


class SymbolicCalculus(VoiceoverScene):
    def construct(self):
        self.card()
        self.contour()
        self.mapping()
        self.roots()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Functions of an operator", r"What is $e^A$, \ or the square root of an operator?", lit=(),
                            part=10)
        with self.voiceover("Chapter three: applying functions to operators, with Cauchy's formula."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def contour(self):
        d = load("calculus")
        ev, R, err = d["ev"], float(d["R"]), float(d["err_exp"])
        cx = square_axes([-3.2, 3.2, 1], [-3.2, 3.2, 1], 0.95).move_to([-3.6, -0.4, 0])
        u = cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0]
        evd = VGroup(*[Dot(cx.c2p(l_.real, l_.imag), radius=0.06, color=C.SPECTRUM) for l_ in ev])
        circ = oriented_circle(cx.c2p(0, 0), R * u, gap_at=-PI / 4, tip_length=0.2)
        M = 128  # every node of the quadrature that computes f(A) below
        th = 2 * math.pi * (np.arange(M) + 0.5) / M
        nodes = VGroup(*[Dot(cx.c2p(R * math.cos(t_), R * math.sin(t_)), radius=0.025, color=C.EPS) for t_ in th])
        sl = label(r"$\sigma(A)$, \ a random $6 \times 6$", font_size=22, color=C.SPECTRUM).next_to(cx, UP, buff=0.08)
        cl = MathTex(rf"|\lambda| = {R:.2f}", font_size=22, color=C.EPS).next_to(cx.c2p(R * 0.71, R * 0.71), UR, buff=0.15)
        # Cauchy's formula for numbers first: a point z inside the circle, a point lambda on it, the kernel's 1/(lambda - z)
        z0, lam0 = -0.8 + 0.7j, R * np.exp(2.3j)
        assert abs(z0) < R - 1 and lam0.real < -0.5 and lam0.imag > 0.5  # z inside; the segment stays in one quadrant
        zd = Dot(cx.c2p(z0.real, z0.imag), radius=0.07, color=WHITE)
        zl = MathTex(r"z", font_size=28).next_to(zd, RIGHT, buff=0.1)
        ld = Dot(cx.c2p(lam0.real, lam0.imag), radius=0.07, color=C.EPS)
        ll = MathTex(r"\lambda", font_size=28, color=C.EPS).next_to(ld, UL, buff=0.08)
        seg = Line(zd.get_center(), ld.get_center(), color=GREY_B, stroke_width=2.5)
        nrm = rotate_vector(normalize(ld.get_center() - zd.get_center()), -PI / 2)
        segl = MathTex(r"\lambda - z", font_size=26, color=GREY_A).move_to(seg.get_center() + 0.5 * nrm)
        scalar = VGroup(zd, zl, ld, ll, seg, segl)
        rows = VGroup(
            label(r"Part 7's Cauchy formula:", font_size=24),
            MathTex(r"f(z) = \frac{1}{2\pi i}\oint \frac{f(\lambda)}{\lambda - z}\,d\lambda", font_size=30),
            label(r"put an operator in the slot:", font_size=24),
            MathTex(r"f(A) = \frac{1}{2\pi i}\oint f(\lambda)\,(\lambda I - A)^{-1}\,d\lambda", font_size=32, color=C.EPS),
            label(r"\textbf{FA 10.26--10.27} \ for $f$ holomorphic near $\sigma(A)$,", font_size=22, color=GREY_A),
            label(r"$f \mapsto f(A)$ is an algebra homomorphism", font_size=22, color=GREY_A),
            MathTex(rf"f = \exp, \ 128 \text{{ nodes: }} \|f(A) - e^A\| = {sci(err, 1)}", font_size=24,
                    color=C.OPERATOR),
            label(r"($e^A$ from scipy: \ Pad\'e with scaling and squaring)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows[5].shift(UP * 0.07)  # the two halves of the FA row read as one statement
        rows.next_to([0.0, -0.3, 0], RIGHT, buff=0)
        assert max(r_.width for r_ in rows) <= 6.0 and rows.get_right()[0] <= 6.6 and rows.get_left()[0] > cx.get_right()[0]
        assert err < 1e-10
        head = label(r"Cauchy's formula, \ with an operator in the slot", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> How do you take the exponential of a matrix, or of any element of a Banach "
            "algebra? Part 7 already answered it. Cauchy's formula recovers a holomorphic function from its values on "
            "a circle, through the kernel one over lambda minus z. <bookmark mark='b'/> Put the operator in place of "
            "z: the kernel becomes the resolvent. Integrate around a contour enclosing the spectrum, and you get f "
            "of A. <bookmark mark='c'/> For a random matrix, with the exponential and a hundred twenty-eight points on "
            "the circle, the result matches the exponential computed the usual way, to rounding error."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]), Create(cx), Create(circ))
            self.play(FadeIn(zd, scale=2), FadeIn(zl), FadeIn(ld, scale=2), FadeIn(ll))
            self.play(Create(seg), FadeIn(segl))
            vo.wait_until("b")
            self.play(FadeOut(scalar), FadeIn(sl), LaggedStart(*[FadeIn(d_, scale=2) for d_ in evd], lag_ratio=0.2))
            self.play(FadeIn(rows[2:6]), FadeIn(cl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n_, scale=0.3) for n_ in nodes], lag_ratio=0.05), run_time=1.5)
            self.play(FadeIn(rows[6:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mapping(self):
        d = load("calculus")
        ev = d["ev"]
        ax = square_axes([-2.2, 2.2, 1], [-2.2, 2.2, 1], 1.15).move_to([-3.8, -0.2, 0])
        bx = square_axes([-1.5, 5.0, 1], [-3.2, 3.2, 1], 0.78).move_to([3.4, -0.2, 0])
        eA = np.exp(ev)
        d1 = VGroup(*[Dot(ax.c2p(l_.real, l_.imag), radius=0.07, color=C.SPECTRUM) for l_ in ev])
        d2 = VGroup(*[Dot(bx.c2p(l_.real, l_.imag), radius=0.07, color=C.FREQ) for l_ in eA])
        l1 = MathTex(r"\sigma(A)", font_size=30, color=C.SPECTRUM).next_to(ax, UP, buff=0.1)
        l2 = MathTex(r"\sigma(e^A) = e^{\sigma(A)}", font_size=30, color=C.FREQ).next_to(bx, UP, buff=0.1)
        # the grid lines Re = const and Im = const near the spectrum, and their images under exp
        grid, igrid = VGroup(), VGroup()
        s = np.linspace(-2, 2, 120)
        for c in np.linspace(-2, 2, 9):
            for z in (c + 1j * s, s + 1j * c):
                grid.add(VMobject(stroke_color=GREY_C, stroke_width=1.2).set_points_as_corners(
                    [ax.c2p(w.real, w.imag) for w in z]))
                w = np.exp(z)
                ok = (w.real > -1.5) & (w.real < 5) & (np.abs(w.imag) < 3.2)
                if ok.sum() > 2:
                    igrid.add(VMobject(stroke_color=C.OPERATOR, stroke_width=1.2, stroke_opacity=0.7).set_points_as_corners(
                        [bx.c2p(v.real, v.imag) for v in w[ok]]))
        arr = Arrow([-1.2, 1.9, 0], [0.8, 1.9, 0], buff=0, color=GREY_B, stroke_width=4)
        al = MathTex(r"\exp", font_size=28).next_to(arr, UP, buff=0.05)
        computed = np.sort_complex(np.exp(ev))
        assert np.allclose(np.sort_complex(eA), computed)
        rows = VGroup(
            label(r"\textbf{FA 10.28} \ (spectral mapping) \ $\sigma(f(A)) = f(\sigma(A))$", font_size=26, color=C.EPS),
            label(r"checked: \ the eigenvalues of the contour-built $e^A$ are $e^{\lambda_i}$ to $10^{-9}$", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        head = label(r"The spectrum moves with the function", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> And the spectrum goes along. The eigenvalues of A, on the left, <bookmark mark='b'/> "
            "are carried by the exponential to the eigenvalues of e to the A, on the right, while the grid around "
            "them is bent by the same map. <bookmark mark='c'/> That's the spectral mapping theorem: the spectrum of "
            "f of A is f of the spectrum of A, for every holomorphic f, in every Banach algebra."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(grid), FadeIn(d1), FadeIn(l1))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(al), Create(bx))
            self.play(TransformFromCopy(grid, igrid), TransformFromCopy(d1, d2), FadeIn(l2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roots(self):
        d = load("calculus")
        evb, c, rb, err = d["evb"], float(d["c"]), float(d["rb"]), float(d["err_sq"])
        cx = square_axes([-2.5, 6.5, 1], [-3.2, 3.2, 1], 0.72).move_to([-3.2, -0.3, 0])
        u = cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0]
        cut = Line(cx.c2p(-2.5, 0), cx.c2p(0, 0), color=C.PATHOLOGY, stroke_width=6)
        cutl = label(r"branch cut of $\sqrt{\lambda}$", font_size=20, color=C.PATHOLOGY).next_to(cx.c2p(-1.25, 0), DOWN,
                                                                                               buff=0.15)
        evd = VGroup(*[Dot(cx.c2p(l_.real, l_.imag), radius=0.06, color=C.SPECTRUM) for l_ in evb])
        circ = Circle(radius=rb * u, color=C.EPS, stroke_width=3).move_to(cx.c2p(c, 0))
        circ.add_tip(tip_length=0.16)
        assert c - rb > 0.2 and err < 1e-9
        shift = float((evb - d["ev"]).real.mean())
        rows = VGroup(
            label(rf"$B = A + {shift:.2f}\,I$: \ spectrum in the right half-plane", font_size=24),
            label(r"a contour around $\sigma(B)$ that avoids the cut:", font_size=24),
            MathTex(r"\sqrt B = \frac{1}{2\pi i}\oint \sqrt\lambda\,(\lambda I - B)^{-1}\,d\lambda", font_size=30,
                    color=C.EPS),
            MathTex(rf"\big\|(\sqrt B)^2 - B\big\| = {sci(err, 1)}", font_size=26, color=C.OPERATOR),
            label(r"logarithms, \ fractional powers, \ resolvents: \ the same way", font_size=22, color=GREY_A),
            label(r"Part 7's Runge: \ rational functions suffice to approximate on $\sigma$", font_size=22, color=GREY_A),
            label(r"\textbf{FA 10.35} \ (Lomonosov, 1973) \ an operator $T \ne \lambda I$ commuting with a compact $K \ne 0$", font_size=22),
            label(r"has a nontrivial closed invariant subspace: \ by Schauder's fixed-point theorem", font_size=22),
        )
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to([0.5, -0.3, 0], RIGHT, buff=0)
        head = label(r"Square roots of operators", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Square roots need care, because the square root isn't holomorphic across its "
            "branch cut. Shift the matrix so its spectrum sits in the right half-plane, <bookmark mark='b'/> and take "
            "a contour that encloses the spectrum without touching the cut. The same formula, with the square root "
            "in it, gives a matrix whose square is B, to rounding error. <bookmark mark='c'/> Logarithms and "
            "fractional powers work the same way, and Runge's theorem from Part 7 explains why rational functions "
            "are enough. One famous consequence of this circle of ideas, Lomonosov's theorem, finds nontrivial invariant "
            "subspaces with a fixed-point argument."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(cx), Create(cut), FadeIn(cutl), FadeIn(evd), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(circ), FadeIn(rows[1:3]))
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:6]))
            self.play(FadeIn(rows[6:]))
        self.wait(0.4)
        self.clear_scene()
