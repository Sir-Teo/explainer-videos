from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import load, mapped_grid, plain_axes, polyline, square_axes


def T(P):
    x, y = P[..., 0], P[..., 1]
    return np.stack([x + 0.25 * np.sin(2 * y), y + 0.2 * x * x], -1)


def detJ(x, y):
    return 1 - 0.5 * np.cos(2 * y) * 0.4 * x


class FormsTour(VoiceoverScene):
    def construct(self):
        self.card()
        self.change_of_variables()
        self.partition()
        self.green()
        self.closed_exact()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"A tour of integration in many variables",
                            r"Rudin's chapter 10, in pictures: \ a tour, no proofs", lit=(), part=4)
        with self.voiceover(
            "Chapter nine is a guided tour of Rudin's tenth chapter, integration in many variables. We'll state and "
            "picture the main results, and check them numerically, but we won't prove them."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def change_of_variables(self):
        d = load("forms")
        ratios, h = d["ratios"], float(d["h"])
        ax = square_axes([-1.3, 1.5, 1], [-1.3, 1.5, 1], 2.1).move_to([-3.6, -0.75, 0])
        ax.set_opacity(0.4)
        cells = VGroup()
        for x0 in np.arange(-1.0, 1.0, h):
            for y0 in np.arange(-1.0, 1.0, h):
                sq = np.array([[x0, y0], [x0 + h, y0], [x0 + h, y0 + h], [x0, y0 + h]])
                side = np.concatenate([np.linspace(sq[i], sq[(i + 1) % 4], 12, endpoint=False) for i in range(4)])
                Q = T(side)
                v = float(detJ(x0 + h / 2, y0 + h / 2))
                col = interpolate_color(ManimColor(C.SEQ), ManimColor(C.CLOSED_SET), np.clip((v - 0.85) / 0.3, 0, 1))
                cells.add(VMobject(stroke_color=WHITE, stroke_width=1, fill_color=col, fill_opacity=0.7)
                          .set_points_as_corners([ax.c2p(*q) for q in np.vstack([Q, Q[:1]])]))
        base = mapped_grid(ax, lambda P: P, (-1.0, 1.0), (-1.0, 1.0), n=9, color=GREY_D, stroke_width=1)
        head = VGroup(label(r"\textbf{Rudin 10.9} \ change of variables", font_size=30),
                      MathTex(r"\int_{T(E)} f(y)\,dy = \int_E f(T(x))\,|\det T'(x)|\,dx", font_size=36, color=C.EPS)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        side = VGroup(
            MathTex(r"T(x, y) = (x + \tfrac14 \sin 2y,\ y + \tfrac15 x^2)", font_size=28),
            label(r"each small square becomes a near-parallelogram", font_size=24),
            label(r"whose area is $|\det T'|$ times the square's", font_size=24),
            label(r"(color: \ $|\det T'|$, \ from $0.8$ to $1.2$)", font_size=22, color=GREY_A),
            label(rf"computed for all {len(ratios)} cells: \ area / ($|\det T'| \times h^2$)", font_size=24),
            MathTex(rf"\in [{ratios.min():.5f},\ {ratios.max():.5f}]", font_size=30, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -0.7, 0])
        for r_ in side:
            if r_.width > 6.3:
                r_.width = 6.3
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -0.7, 0])
        assert np.abs(ratios - 1).max() < 1e-3
        with self.voiceover(
            "<bookmark mark='a'/> First, the change of variables formula. When a map T reshapes a region, integrals "
            "pick up a factor: the absolute value of the determinant of T's derivative. <bookmark mark='b'/> Here's "
            "why. Cut the region into small squares; each becomes, nearly, the parallelogram of the derivative, whose "
            "area is the determinant times the square's area. <bookmark mark='c'/> Computed for all sixty-four cells, "
            "the ratio of the true area to the determinant's prediction is one, to within a few millionths."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(base))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(TransformFromCopy(base, cells), FadeIn(side[1:3]), run_time=2.5)
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def partition(self):
        d = load("forms")
        xs, psi, cs = d["xs"], d["psi"], d["cs"]
        ax = plain_axes([0, 1, 0.25], [0, 1.15, 0.5], 9.0, 3.6).move_to([-0.6, -1.0, 0])
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / (len(cs) - 1)) for k in range(len(cs))]
        bumps = VGroup(*[polyline(ax, xs, p_, color=c, stroke_width=3) for p_, c in zip(psi, cols)])
        total = polyline(ax, xs, psi.sum(axis=0), color=WHITE, stroke_width=3.5)
        head = VGroup(label(r"\textbf{Rudin 10.8} \ partitions of unity", font_size=30),
                      label(r"smooth bumps $\psi_i \ge 0$, \ each living on a small piece, \ with $\sum \psi_i = 1$",
                            font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        tl = MathTex(r"\sum_i \psi_i = 1", font_size=32).next_to(ax.c2p(0.5, 1.0), UP, buff=0.12)
        use = label(r"so a global integral is a sum of local ones: \ $\int f = \sum_i \int \psi_i f$", font_size=26,
                    color=C.EPS).to_edge(DOWN, buff=0.3)
        assert np.allclose(psi.sum(axis=0), 1)
        with self.voiceover(
            "<bookmark mark='a'/> Second, partitions of unity: smooth bumps, each living on a small piece of the "
            "space, that add up to exactly one. <bookmark mark='b'/> They let us cut an integral into local pieces, "
            "do each piece in convenient coordinates, and add the results."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), LaggedStart(*[Create(b_) for b_ in bumps], lag_ratio=0.2), run_time=2.0)
            self.play(Create(total), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(use))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def green(self):
        d = load("forms")
        area = float(d["area"])
        imp = load("implicit")
        pts = imp["pts"]
        ax = square_axes([-0.3, 1.8, 0.5], [-0.3, 1.8, 0.5], 2.7).move_to([-3.6, -0.75, 0])
        ax.set_opacity(0.5)
        loop = VMobject(color=C.FUNC, stroke_width=3.5, fill_color=C.FUNC, fill_opacity=0.25).set_points_as_corners(
            [ax.c2p(*p) for p in np.vstack([pts, pts[:1], [[0, 0]]])])
        arrows = VGroup()
        for k in (30, 90, 150, 210):
            a, b = pts[k], pts[k + 6]
            arrows.add(Arrow(ax.c2p(*a), ax.c2p(*b), buff=0, color=C.EPS, stroke_width=4, tip_length=0.16))
        head = VGroup(label(r"\textbf{Rudin 10.33} \ Stokes' theorem", font_size=30),
                      MathTex(r"\int_{\partial \Omega} \omega = \int_\Omega d\omega", font_size=40, color=C.EPS)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        faces = VGroup(
            label(r"its faces: \ Green (the plane), \ Gauss (divergence),", font_size=24, color=GREY_A),
            label(r"and the classical Stokes (surfaces in $\R^3$)", font_size=24, color=GREY_A),
            label(r"Green, with $\omega = \tfrac12(x\,dy - y\,dx)$, \ $d\omega = dx \wedge dy$:", font_size=26),
            MathTex(r"\text{area of } \Omega = \frac12 \oint_{\partial\Omega} (x\,dy - y\,dx)", font_size=32),
            label(r"the folium's loop (chapter 7):", font_size=26),
            MathTex(rf"\frac12 \oint (x\,dy - y\,dx) = {area:.6f} \approx \tfrac32", font_size=32, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, -0.85, 0])
        for r_ in faces:
            if r_.width > 6.6:
                r_.width = 6.6
        faces.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, -0.85, 0])
        assert abs(area - 1.5) < 1e-3
        with self.voiceover(
            "<bookmark mark='a'/> The summit of the chapter is Stokes' theorem: the integral of a form over the "
            "boundary of a region equals the integral of its exterior derivative over the region. "
            "<bookmark mark='b'/> Green's theorem, the divergence theorem and the classical Stokes theorem are all "
            "special cases. <bookmark mark='c'/> In the plane, with the right form, it says that the area of a region "
            "is a line integral around its edge. <bookmark mark='d'/> Walk once around the loop of the folium from "
            "chapter seven, and the line integral gives its area: exactly three halves."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(FadeIn(faces[:2]))
            vo.wait_until("c")
            self.play(FadeIn(faces[2:4]))
            vo.wait_until("d")
            self.play(Create(loop), LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.3), run_time=2.5)
            self.play(FadeIn(faces[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closed_exact(self):
        d = load("forms")
        wa, wo = float(d["w_around"]), float(d["w_off"])
        ax = square_axes([-1.8, 2.6, 1], [-1.6, 1.8, 1], 1.45).move_to([-3.2, -0.85, 0])
        ax.set_opacity(0.5)
        hole = VGroup(Circle(radius=0.1, color=C.HOLE, stroke_width=3).move_to(ax.c2p(0, 0)),
                      MathTex(r"0", font_size=24, color=C.HOLE).next_to(ax.c2p(0, 0), DL, buff=0.1))
        c1 = Circle(radius=1.45 * 1.0, color=C.EPS, stroke_width=3).move_to(ax.c2p(0.2, -0.1))
        c2 = Circle(radius=1.45 * 0.6, color=C.CONNECTED_SET, stroke_width=3).move_to(ax.c2p(1.6, 0.8))
        l1 = MathTex(rf"\oint \omega = {wa:.6f} = 2\pi", font_size=28, color=C.EPS).next_to(c1, DOWN, buff=0.1)
        l2 = MathTex(rf"\oint \omega = {abs(wo):.6f}", font_size=28, color=C.CONNECTED_SET).next_to(c2, UP, buff=0.1)
        head = VGroup(label(r"\textbf{Rudin 10.35--10.39} \ closed is not exact, \ when there is a hole", font_size=30),
                      MathTex(r"\omega = \frac{x\,dy - y\,dx}{x^2 + y^2} \text{ on } \R^2 \setminus \{0\}", font_size=34)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        side = VGroup(
            label(r"$d\omega = 0$: \ $\omega$ is \textbf{closed}", font_size=26),
            label(r"if $\omega = d\theta$ for a function $\theta$ (\textbf{exact}),", font_size=26),
            label(r"every closed loop would give $0$", font_size=26),
            label(r"the loop around the hole gives $2\pi$:", font_size=26, color=C.EPS),
            label(r"$\omega$ is closed but not exact", font_size=26, color=C.PATHOLOGY),
            label(r"(the angle $\theta$ cannot be defined all the way around)", font_size=22, color=GREY_A),
            label(r"on a convex set, closed always means exact \ (10.39)", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.85, 0])
        for r_ in side:
            if r_.width > 6.0:
                r_.width = 6.0
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.85, 0])
        assert abs(wa - 2 * math.pi) < 1e-3 and abs(wo) < 1e-3
        with self.voiceover(
            "<bookmark mark='a'/> Last stop: a form with zero exterior derivative, a closed form, need not be the "
            "derivative of a function, an exact form. The classic example is the angle form in the plane with the "
            "origin removed. <bookmark mark='b'/> A loop that misses the hole gives zero. <bookmark mark='c'/> A loop "
            "around the hole gives two pi, which no exact form could: the angle can't be defined continuously all "
            "the way around. <bookmark mark='d'/> On a convex set this can't happen, which is Poincaré's lemma. "
            "Holes are detected by integrals: the beginning of topology, and a preview of Part 7's winding numbers."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), FadeIn(hole))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(side[:3]))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(l2))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(l1))
            self.play(FadeIn(side[3:6]))
            vo.wait_until("d")
            self.play(FadeIn(side[6]))
        self.wait(0.4)
        self.clear_scene()
