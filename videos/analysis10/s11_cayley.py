from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import load, plain_axes, polyline, square_axes


def cayley(l_):
    return (l_ - 1j) / (l_ + 1j)


class Cayley(VoiceoverScene):
    def construct(self):
        self.card()
        self.bend()
        self.theorem()
        self.momentum()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"The Cayley transform", r"How do you tame an unbounded operator?", lit=(1932,), part=10)
        with self.voiceover("Chapter ten: the Cayley transform, which turns unbounded self-adjoint operators into unitary "
                            "ones."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bend(self):
        d = load("twisted")
        ev = d["t1"]  # theta = pi/2
        line = NumberLine(x_range=[-30, 30, 10], length=6.4, include_numbers=True, font_size=18,
                          decimal_number_config={"num_decimal_places": 0}).move_to([-3.4, 1.4, 0])
        ll = MathTex(r"\sigma(D_{\pi/2}) \subset \mathbb R", font_size=24, color=C.SPECTRUM).next_to(line, UP, buff=0.2)
        pts = VGroup(*[Dot(line.n2p(v), radius=0.06, color=C.SPECTRUM) for v in ev if abs(v) <= 30])
        cx = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.4).move_to([3.4, -0.2, 0])
        circ = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=GREY_B, stroke_width=2).move_to(cx.c2p(0, 0))
        hole = Circle(radius=0.08, color=C.PATHOLOGY, stroke_width=3).move_to(cx.c2p(1, 0))
        hl = MathTex(r"1 = \text{image of } \pm\infty", font_size=22, color=C.PATHOLOGY).next_to(hole, RIGHT, buff=0.1)
        w = cayley(np.array(ev))
        assert np.allclose(np.abs(w), 1)
        wpts = VGroup(*[Dot(cx.c2p(z.real, z.imag), radius=0.06, color=C.SPECTRUM) for z in w])
        # more of the ladder: it accumulates at 1 from both sides
        more = np.array([2 * math.pi * n - math.pi / 2 for n in range(-40, 41)])
        wm = cayley(more)
        mpts = VGroup(*[Dot(cx.c2p(z.real, z.imag), radius=0.035, color=C.SPECTRUM, fill_opacity=0.6) for z in wm])
        # the real line itself, bent onto the circle
        s = np.linspace(-30, 30, 600)
        img = cayley(s)
        arc = VMobject(color=C.OPERATOR, stroke_width=3).set_points_as_corners([cx.c2p(z.real, z.imag) for z in img])
        fl = MathTex(r"\lambda \mapsto \frac{\lambda - i}{\lambda + i}", font_size=30, color=C.OPERATOR).next_to(cx, UP,
                                                                                                       buff=0.1)
        marks = VGroup(*[VGroup(Dot(cx.c2p(cayley(v).real, cayley(v).imag), radius=0.04, color=WHITE),
                                MathTex(lab, font_size=20).next_to(cx.c2p(cayley(v).real, cayley(v).imag),
                                                                   normalize(np.array([cayley(v).real, cayley(v).imag, 0])),
                                                                   buff=0.1))
                         for v, lab in ((0, "0"), (1, "1"), (-1, "-1"))])
        rows = VGroup(
            label(r"$|\lambda - i| = |\lambda + i|$ for real $\lambda$: \ the real line lands on the unit circle", font_size=22),
            label(r"$0 \mapsto -1$, \ $\pm 1 \mapsto \mp i$, \ $\pm\infty \mapsto 1$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.2, -1.6, 0])
        assert abs(cayley(0) + 1) < 1e-15 and abs(cayley(1) + 1j) < 1e-15 and abs(cayley(-1) - 1j) < 1e-15
        head = label(r"Bending the real line into a circle", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> A self-adjoint operator's spectrum lies on the real line, and for an unbounded "
            "one it runs off to infinity, like the ladder of the last chapter. <bookmark mark='b'/> The Cayley map, "
            "lambda minus i over lambda plus i, bends the real line onto the unit circle, because a real number is "
            "equally far from i and minus i. Zero goes to minus one, and both ends of the line go to one. "
            "<bookmark mark='c'/> The ladder lands on the circle, piling up at one from both sides: a bounded "
            "picture of an unbounded spectrum."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(line), FadeIn(ll), LaggedStart(*[FadeIn(p_, scale=2) for p_ in pts],
                                                                           lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(cx), Create(circ), FadeIn(fl), FadeIn(rows[0]))
            self.play(Create(arc), FadeIn(marks), FadeIn(rows[1]), run_time=2.0)
            self.play(Create(hole), FadeIn(hl))
            vo.wait_until("c")
            self.play(TransformFromCopy(pts, wpts), run_time=2.0)
            self.play(FadeIn(mpts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        cx = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.1).move_to([-4.6, -0.6, 0])
        circ = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=C.EPS, stroke_width=3).move_to(cx.c2p(0, 0))
        cl = label(r"the extensions $D_\theta$ \ $\leftrightarrow$ \ unitary maps between the", font_size=20,
                   color=C.EPS).next_to(cx, UP, buff=0.3)
        cl2 = label(r"one-dimensional deficiency spaces: \ a circle", font_size=20, color=C.EPS).next_to(cl, DOWN,
                                                                                                    buff=0.05)
        pm = ProofMap([
            r"$T$ self-adjoint $\Rightarrow$ $U = (T - i)(T + i)^{-1}$ is unitary, \ $1 \notin \sigma_p(U)$",
            r"bounded spectral theorem for $U$: \ $U = \int_{\mathbb T} z\, dE'(z)$",
            r"pull back along $\lambda = i\frac{1 + z}{1 - z}$: \ $T = \int_{\mathbb R} \lambda\, dE(\lambda)$",
        ], font_size=22, width=7.4, buff=0.15, direction=DOWN).move_to([2.6, 0.6, 0])
        rows = VGroup(
            label(r"\textbf{FA 13.19} \ symmetric $T$ $\leftrightarrow$ isometric $U$; \ self-adjoint $\leftrightarrow$ "
                  r"unitary", font_size=22),
            label(r"deficiency indices $= \dim \ker(T^* \mp i)$: \ the gaps $U$ leaves", font_size=22, color=GREY_A),
            label(r"\textbf{FA 13.30} \ every self-adjoint $T$ (unbounded too) is $\int \lambda\, dE(\lambda)$", font_size=24,
                  color=C.SPECTRUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(pm, DOWN, buff=0.35)
        for r_ in rows:
            if r_.width > 7.4:
                r_.width = 7.4
        head = label(r"Von Neumann's route to the spectral theorem", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Von Neumann applied the same map to operators. If T is self-adjoint, T minus i "
            "times the inverse of T plus i is unitary, and bounded. <bookmark mark='b'/> Diagonalize that unitary "
            "with the bounded spectral theorem, then carry its spectral measure back along the inverse map, and you "
            "have T as the integral of lambda against a projection-valued measure on the real line. "
            "<bookmark mark='c'/> For merely symmetric operators the transform is only an isometry, and the "
            "dimensions it misses are the deficiency indices. Self-adjoint extensions correspond to unitary maps "
            "between those gaps: in our example, a circle of them, the circle of theta."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(pm))
            self.play(*pm.light(0))
            vo.wait_until("b")
            self.play(*pm.light(1))
            self.play(*pm.light(2))
            self.play(*pm.done(), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[:2]), Create(cx), Create(circ), FadeIn(cl), FadeIn(cl2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def momentum(self):
        d = load("momentum")
        x, psi, xi, ft, err = d["x"], d["psi"], d["xi"], d["ft"], float(d["err"])
        ax = plain_axes([-12, 12, 4], [-1.6, 1.6, 1], 6.0, 2.2).move_to([-3.4, 1.1, 0])
        bx = plain_axes([-6, 6, 2], [0, 1.8, 0.5], 6.0, 2.2, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -2.0, 0])
        m = np.abs(x) <= 12
        g1 = polyline(ax, x[m], psi[m].real, color=C.FUNC, stroke_width=2.5)
        g1b = polyline(ax, x[m], np.abs(psi[m]), color=WHITE, stroke_width=2)
        mt = np.abs(xi) <= 6
        g2 = polyline(bx, xi[mt], ft[mt], color=C.FREQ, stroke_width=3.5)
        l1 = MathTex(r"\psi(x)", font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.05)
        l2 = MathTex(r"|\hat\psi(\xi)|", font_size=24, color=C.FREQ).next_to(bx, UP, buff=0.05)
        pk = [float(xi[mt][np.argmax(np.where(np.abs(xi[mt] - c) < 1, ft[mt], 0))]) for c in (2.5, -1.0)]
        assert err < 1e-8 and abs(pk[0] - 2.5) < 0.1 and abs(pk[1] + 1.0) < 0.1
        card = dictionary_card(r"matrices", r"self-adjoint operators", [
            (r"eigenvalues", r"the spectrum: \ a measure's worth of them"),
            (r"$A = U\Lambda U^*$", r"$T = \int \lambda\, dE(\lambda)$"),
        ], font_size=22)
        card.scale_to_fit_width(6.6).move_to([3.5, -2.2, 0])
        rows = VGroup(
            MathTex(r"P = -i\frac{d}{dx} \ \text{ on } L^2(\mathbb R)", font_size=28, color=C.OPERATOR),
            MathTex(r"\mathcal F P \mathcal F^{-1} = \text{multiplication by } \xi", font_size=28, color=C.EPS),
            MathTex(rf"\text{{by FFT, on this packet: error }} {sci(err, 1)}", font_size=22, color=GREY_A),
            label(r"so Plancherel (Part 9) \emph{is} the spectral theorem for momentum", font_size=22, color=C.SPECTRUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, 1.2, 0])
        head = label(r"Momentum, \ diagonalized by the Fourier transform", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The momentum operator, minus i d d x on the whole line, is the leading example. "
            "<bookmark mark='b'/> Here's a packet with two components, and its Fourier transform, two bumps at the "
            "two momenta. <bookmark mark='c'/> Conjugating by the Fourier transform turns momentum into "
            "multiplication by xi, checked here to ten digits. So Plancherel's theorem from Part 9 is the spectral "
            "theorem for momentum: the Fourier transform is the change of basis that diagonalizes it. "
            "<bookmark mark='d'/> The dictionary's last card: eigenvalues become the spectrum, a whole measure's "
            "worth of them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ax), Create(g1b), Create(g1), FadeIn(l1))
            self.play(Create(bx), Create(g2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:3]))
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(card.titles), FadeIn(card.rows), FadeIn(card.arrows))
        self.wait(0.4)
        self.clear_scene()
