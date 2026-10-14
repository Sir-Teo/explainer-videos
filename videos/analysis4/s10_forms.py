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
        head = VGroup(label(r"Change of variables", font_size=34),
                      MathTex(r"\int_{T(E)} f(y)\,dy = \int_E f(T(x))\,|\det T'(x)|\,dx", r"\quad \text{\small (Rudin 10.9)}",
                              font_size=34),
                      label(r"$T$ one-to-one and $C^1$ on $E$, \ $\det T' \ne 0$; \ $f$ continuous, "
                            r"with compact support in $T(E)$", font_size=22, color=GREY_A)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        head[1][0].set_color(C.EPS)
        head[1][1].set_color(GREY_B)
        U_ = 2.05
        ax = square_axes([-1.3, 1.5, 1], [-1.3, 1.5, 1], U_)
        ax.shift(np.array([-3.6, head.get_bottom()[1] - 0.3, 0]) - ax.c2p(0, 1.2))  # the cells reach y = 1.2
        ax.set_opacity(0)  # no axes: the picture is the grid and its image
        centers = [(x0 + h / 2, y0 + h / 2) for x0 in np.arange(-1.0, 1.0, h) for y0 in np.arange(-1.0, 1.0, h)]
        vals = np.array([float(detJ(*c_)) for c_ in centers])
        vmin, vmax = vals.min(), vals.max()  # the colors span exactly the values taken
        cells = VGroup()
        for (cx, cy), v in zip(centers, vals):
            x0, y0 = cx - h / 2, cy - h / 2
            sq = np.array([[x0, y0], [x0 + h, y0], [x0 + h, y0 + h], [x0, y0 + h]])
            side = np.concatenate([np.linspace(sq[i], sq[(i + 1) % 4], 12, endpoint=False) for i in range(4)])
            Q = T(side)
            col = interpolate_color(ManimColor(C.SEQ), ManimColor(C.CLOSED_SET), (v - vmin) / (vmax - vmin))
            cells.add(VMobject(stroke_color=WHITE, stroke_width=1, fill_color=col, fill_opacity=0.7)
                      .set_points_as_corners([ax.c2p(*q) for q in np.vstack([Q, Q[:1]])]))
        base = mapped_grid(ax, lambda P: P, (-1.0, 1.0), (-1.0, 1.0), n=9, color=GREY_D, stroke_width=1)
        assert cells.get_top()[1] < head.get_bottom()[1] - 0.2 and cells.get_bottom()[1] > -3.6
        side = VGroup(
            MathTex(r"T(x, y) = (x + \tfrac14 \sin 2y,\ y + \tfrac15 x^2)", font_size=28),
            label(r"each small square becomes a near-parallelogram", font_size=24),
            label(r"whose area is $|\det T'|$ times the square's", font_size=24),
            label(rf"(color: \ $|\det T'|$, \ blue ${vmin:.2f}$ to orange ${vmax:.2f}$)", font_size=22, color=GREY_A),
            label(rf"computed for all {len(ratios)} cells: \ area $\big/ \int_{{\text{{square}}}} |\det T'|$", font_size=24),
            MathTex(rf"\in [{ratios.min():.6f},\ {ratios.max():.6f}]", font_size=30, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r_ in side:
            if r_.width > 6.0:
                r_.width = 6.0
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to([cells.get_right()[0] + 0.5, -0.9, 0], RIGHT, buff=0)
        assert side.get_right()[0] <= 6.6 and len(ratios) == len(cells) == 64
        assert np.abs(ratios - 1).max() < 1e-3
        # T is one-to-one on the square: T - I = (sin(2y)/4, x^2/5) has derivative norm <= 1/2 there
        g_ = np.linspace(-1, 1, 41)
        assert max(np.linalg.norm([[0, 0.5 * math.cos(2 * y_)], [0.4 * x_, 0]], 2) for x_ in g_ for y_ in g_) <= 0.5 + 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> First, the change of variables formula. When a one-to-one, continuously "
            "differentiable map T, with nonzero Jacobian, reshapes a region, integrals pick up a factor: the absolute value of the determinant of T's derivative. <bookmark mark='b'/> Here's "
            "why. Cut the region into small squares; each becomes, nearly, the parallelogram of the derivative, whose "
            "area is the determinant times the square's area. <bookmark mark='c'/> Computed for all sixty-four cells, "
            "the ratio of the true area to the determinant's prediction is one, to within a few millionths."
        ) as vo:
            self.play(FadeIn(head[0]), Create(base))
            vo.wait_until("a")
            self.play(FadeIn(head[1:]), FadeIn(side[0]))
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
        head = VGroup(label(r"Partitions of unity", font_size=34),
                      label(r"continuous bumps $\psi_i \ge 0$, \ each inside one set of a cover of $K$, \ $\sum \psi_i = 1$ "
                            r"on $K$ \ (Rudin 10.8)", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        ax = plain_axes([0, 1, 0.25], [0, 1.15, 0.5], 9.2, 3.4)
        ax.move_to([-1.35, 0, 0]).align_to([0, head.get_bottom()[1] - 0.3, 0], UP)
        cols = [C.SEQ, C.APPROX] * 3  # neighbours in different colors
        assert len(cs) == 6
        bumps = VGroup(*[polyline(ax, xs, p_, color=c, stroke_width=3) for p_, c in zip(psi, cols)])
        total = polyline(ax, xs, psi.sum(axis=0), color=WHITE, stroke_width=3.5)
        tl = MathTex(r"\sum_i \psi_i = 1", font_size=32).next_to(ax.c2p(0.5, 1.0), UP, buff=0.12)
        # the cover: each bump's support, the open interval where it is positive, one row each (they overlap)
        sup = [(xs[p_ > 0].min(), xs[p_ > 0].max()) for p_ in psi]
        for (lo, hi), c_ in zip(sup, cs):
            assert lo <= max(c_ - 0.3, 0) and hi >= min(c_ + 0.3, 1) and hi - lo < 0.7  # one small piece each
        y0 = ax.get_bottom()[1] - 0.35
        cover = VGroup(*[Line(ax.c2p(lo, 0) * np.array([1, 0, 0]) + np.array([0, y0 - 0.17 * i, 0]),
                              ax.c2p(hi, 0) * np.array([1, 0, 0]) + np.array([0, y0 - 0.17 * i, 0]),
                              color=c, stroke_width=6) for i, ((lo, hi), c) in enumerate(zip(sup, cols))])
        cl = label(r"the cover: \ the sets $\{\psi_i > 0\}$", font_size=22, color=GREY_A).next_to(
            [ax.c2p(1, 0)[0] + 0.3, cover.get_y(), 0], RIGHT, buff=0)
        kb = BraceBetweenPoints(ax.c2p(0, 0) * np.array([1, 0, 0]) + np.array([0, cover.get_bottom()[1] - 0.08, 0]),
                                ax.c2p(1, 0) * np.array([1, 0, 0]) + np.array([0, cover.get_bottom()[1] - 0.08, 0]),
                                direction=DOWN, color=GREY_B)
        kl = MathTex(r"K = [0, 1]", font_size=28, color=GREY_A).next_to(kb, DOWN, buff=0.08)
        use = label(r"so a global integral is a sum of local ones: \ $\int f = \sum_i \int \psi_i f$", font_size=26,
                    color=C.EPS).to_edge(DOWN, buff=0.35)
        assert np.allclose(psi.sum(axis=0), 1)
        assert kl.get_bottom()[1] > use.get_top()[1] + 0.1 and cl.get_right()[0] <= 6.6
        with self.voiceover(
            "<bookmark mark='a'/> Second, partitions of unity: continuous bumps, each "
            "living inside one small piece of a cover, that add up to exactly one on a compact set. Smooth ones exist "
            "too. <bookmark mark='b'/> They let us cut an integral into local pieces, "
            "do each piece in convenient coordinates, and add the results."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(ax), LaggedStart(*[AnimationGroup(Create(b_), Create(c_))
                                                                 for b_, c_ in zip(bumps, cover)], lag_ratio=0.2),
                      FadeIn(cl), GrowFromCenter(kb), FadeIn(kl), run_time=2.5)
            self.play(Create(total), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(use))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def green(self):
        d = load("forms")
        area = float(d["area"])
        head = VGroup(label(r"Stokes' theorem", font_size=34),
                      MathTex(r"\int_{\partial \Omega} \omega = \int_\Omega d\omega", r"\quad \text{\small (Rudin 10.33)}",
                              font_size=40)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        head[1][0].set_color(C.EPS)
        head[1][1].set_color(GREY_B)
        ax = square_axes([-0.3, 1.8, 0.5], [-0.3, 1.8, 0.5], 2.6)
        ax.move_to([-3.75, 0, 0]).align_to([0, head.get_bottom()[1] - 0.25, 0], UP)
        ax.set_opacity(0.5)

        # the folium's loop in polar form: r = 3 sin t cos t / (sin^3 t + cos^3 t), t in [0, pi/2]. It leaves the
        # origin along the x-axis and comes back along the y-axis (the right-angle corner there is real).
        # (1/2)(x dy - y dx) is the area swept by the radius from the origin: A(t) = (3/2) sin^3 t / (sin^3 + cos^3)
        def rpol(t_):
            return 3 * np.sin(t_) * np.cos(t_) / (np.sin(t_) ** 3 + np.cos(t_) ** 3)

        def A_(t_):
            return 1.5 * np.sin(t_) ** 3 / (np.sin(t_) ** 3 + np.cos(t_) ** 3)

        def P_(t_):
            return np.array([rpol(t_) * np.cos(t_), rpol(t_) * np.sin(t_)])

        tl_ = np.linspace(0, math.pi / 2, 721)
        lp = np.array([P_(t_) for t_ in tl_])
        assert np.abs(lp[:, 0] ** 3 + lp[:, 1] ** 3 - 3 * lp[:, 0] * lp[:, 1]).max() < 1e-12  # on the folium
        assert np.linalg.norm(lp[0]) < 1e-12 and np.linalg.norm(lp[-1]) < 1e-12
        loop = VMobject(color=C.FUNC, stroke_width=3.5, fill_color=C.FUNC, fill_opacity=0.25).set_points_as_corners(
            [ax.c2p(*p) for p in lp])
        arrows = VGroup()
        for t_ in (0.35, 0.785, 1.22):  # the walking direction (counterclockwise), as short arrows on the loop
            p0 = P_(t_)
            tng = P_(t_ + 1e-5) - P_(t_ - 1e-5)
            tng = tng / np.linalg.norm(tng)
            L = 0.5 / 2.6  # half an arrow is 0.25 scene units
            arrows.add(Arrow(ax.c2p(*(p0 - L * tng)), ax.c2p(*(p0 + L * tng)), buff=0, color=C.FUNC, stroke_width=5,
                             tip_length=0.2, max_tip_length_to_length_ratio=0.5))
        faces = VGroup(
            label(r"its faces: \ Green (the plane), \ Gauss (divergence),", font_size=24, color=GREY_A),
            label(r"and the classical Stokes (surfaces in $\R^3$)", font_size=24, color=GREY_A),
            label(r"Green, with $\omega = \tfrac12(x\,dy - y\,dx)$, \ $d\omega = dx \wedge dy$:", font_size=26),
            MathTex(r"\text{area of } \Omega = \frac12 \oint_{\partial\Omega} (x\,dy - y\,dx)", font_size=32),
            label(r"the folium's loop (chapter 7):", font_size=26),
            MathTex(rf"\frac12 \oint (x\,dy - y\,dx) = {area:.6f} \approx \tfrac32", font_size=32, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r_ in faces:
            if r_.width > 6.0:
                r_.width = 6.0
        faces.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to([0.35, -0.6, 0], RIGHT, buff=0)
        assert abs(area - 1.5) < 1e-3 and faces.get_right()[0] <= 6.6 and faces.get_bottom()[1] > -3.6
        om = MathTex(r"\Omega", font_size=34, color=C.FUNC).move_to(ax.c2p(0.85, 0.85))
        bom = MathTex(r"\partial\Omega", font_size=30, color=C.FUNC).next_to(ax.c2p(1.56, 0.95), RIGHT, buff=0.1)
        gg = np.linspace(0, math.pi / 2, 20001)
        num = np.concatenate([[0], np.cumsum(0.5 * (rpol(gg[1:]) ** 2 + rpol(gg[:-1]) ** 2) / 2 * np.diff(gg))])
        assert np.abs(num - A_(gg)).max() < 1e-6 and abs(A_(math.pi / 2) - 1.5) < 1e-12
        thv = ValueTracker(1e-4)

        def swept_():
            g_ = np.linspace(1e-4, thv.get_value(), 160)
            return Polygon(ax.c2p(0, 0), *[ax.c2p(rpol(a) * math.cos(a), rpol(a) * math.sin(a)) for a in g_],
                           stroke_width=0, fill_color=C.EPS, fill_opacity=0.45)

        def tip_():
            t_ = thv.get_value()
            return ax.c2p(rpol(t_) * math.cos(t_), rpol(t_) * math.sin(t_))

        swept = always_redraw(swept_)
        ray = always_redraw(lambda: Line(ax.c2p(0, 0), tip_(), color=C.EPS, stroke_width=2.5))
        walker = always_redraw(lambda: Dot(tip_(), radius=0.08, color=WHITE))
        rd = VGroup(MathTex(r"\frac12 \int (x\,dy - y\,dx) =", font_size=32, color=C.EPS),
                    DecimalNumber(0, num_decimal_places=6, font_size=32, color=C.EPS)).arrange(RIGHT, buff=0.15)
        rd.move_to(faces[5], aligned_edge=LEFT)
        rd[1].add_updater(lambda m: m.set_value(A_(thv.get_value())))
        with self.voiceover(
            "<bookmark mark='a'/> The summit of the chapter is Stokes' theorem: the integral of a form over the "
            "boundary of a region equals the integral of its exterior derivative over the region. "
            "<bookmark mark='b'/> Green's theorem, the divergence theorem and the classical Stokes theorem are all "
            "special cases. <bookmark mark='c'/> In the plane, with the right form, it says that the area of a region "
            "is a line integral around its edge. <bookmark mark='d'/> Walk once around the loop of the folium from "
            "chapter seven, and the line integral gives its area: exactly three halves."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(loop), FadeIn(om), FadeIn(bom), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(faces[:2]))
            vo.wait_until("c")
            self.play(FadeIn(faces[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(faces[4]), FadeIn(rd), FadeOut(om), loop.animate.set_fill(opacity=0.08))
            self.add(swept, ray, walker)
            self.play(thv.animate.set_value(math.pi / 2), run_time=5.0, rate_func=linear)
            for m_ in (swept, ray, walker, rd[1]):
                m_.clear_updaters()
            self.play(FadeOut(ray), FadeOut(walker), FadeTransform(rd, faces[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closed_exact(self):
        d = load("forms")
        wa, wo = float(d["w_around"]), float(d["w_off"])
        ax = square_axes([-1.8, 2.6, 1], [-1.6, 1.8, 1], 1.45).move_to([-3.25, -0.7, 0])
        ax.set_opacity(0.5)
        hole = VGroup(Circle(radius=0.1, color=C.HOLE, stroke_width=3).move_to(ax.c2p(0, 0)),
                      MathTex(r"0", font_size=24, color=C.HOLE).next_to(ax.c2p(0, 0), DL, buff=0.1))
        c1 = Circle(radius=1.45 * 1.0, color=C.EPS, stroke_width=3).move_to(ax.c2p(0.2, -0.1))
        c2 = Circle(radius=1.45 * 0.6, color=C.CONNECTED_SET, stroke_width=3).move_to(ax.c2p(1.6, 0.8))
        l1 = MathTex(rf"\oint \omega = {wa:.6f} = 2\pi", font_size=28, color=C.EPS).next_to(c1, DOWN, buff=0.1)
        l2 = MathTex(rf"\oint \omega = {abs(wo):.6f}", font_size=28, color=C.CONNECTED_SET).next_to(c2, UP, buff=0.1)
        head = VGroup(label(r"Closed is not exact, \ when there is a hole", font_size=34),
                      MathTex(r"\omega = \frac{x\,dy - y\,dx}{x^2 + y^2} \text{ on } \R^2 \setminus \{0\}",
                              r"\quad \text{\small (Rudin 10.35--10.39)}", font_size=34)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_B)
        side = VGroup(
            label(r"$d\omega = 0$: \ $\omega$ is \textbf{closed}", font_size=26),
            label(r"if $\omega = d\theta$ for a function $\theta$ (\textbf{exact}),", font_size=26),
            label(r"every closed loop would give $0$", font_size=26),
            label(r"the loop around the hole gives $2\pi$:", font_size=26, color=C.EPS),
            label(r"$\omega$ is closed but not exact", font_size=26, color=C.PATHOLOGY),
            label(r"(the angle $\theta$ cannot be defined all the way around)", font_size=22, color=GREY_A),
            label(r"on a convex set, closed always means exact \ (10.39)", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for r_ in side:
            if r_.width > 5.9:
                r_.width = 5.9
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to([0.7, -0.85, 0], RIGHT, buff=0)
        assert side.get_right()[0] <= 6.6 and side.get_bottom()[1] > -3.6
        assert abs(wa - 2 * math.pi) < 1e-3 and abs(wo) < 1e-3
        # the vector field dual to omega, (-y, x)/r^2: it swirls around the hole, faster near it
        field = VGroup()
        # keep the arrows out of the two integral labels and the hole's label (each box grown by 0.1)
        boxes = [(m_.get_left()[0] - 0.1, m_.get_right()[0] + 0.1, m_.get_bottom()[1] - 0.1, m_.get_top()[1] + 0.1)
                 for m_ in (l1, l2, hole[1])]

        def clear_of_labels(p0, p1):
            for (x0_, x1_, y0_, y1_) in boxes:
                for q in (p0, p1, (p0 + p1) / 2):
                    if x0_ <= q[0] <= x1_ and y0_ <= q[1] <= y1_:
                        return False
            return True

        skipped = 0
        for gx in np.arange(-1.5, 2.51, 0.5):
            for gy in np.arange(-1.5, 1.51, 0.5):
                r2 = gx * gx + gy * gy
                if r2 < 0.2:
                    continue
                v = np.array([-gy, gx]) / r2
                L = min(0.42, 0.22 / math.sqrt(r2))
                u = v / np.linalg.norm(v) * L / 1.45
                p0_, p1_ = ax.c2p(gx - u[0] / 2, gy - u[1] / 2), ax.c2p(gx + u[0] / 2, gy + u[1] / 2)
                if not clear_of_labels(p0_, p1_):
                    skipped += 1
                    continue
                field.add(Arrow(p0_, p1_, buff=0, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.35).set_opacity(0.7))
        assert 0 < skipped <= 8 and len(field) > 40
        fl_ = label(r"$\omega$ measures the change of angle around $0$", font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.1)
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
            self.play(FadeIn(head[1]), LaggedStart(*[GrowArrow(a_) for a_ in field], lag_ratio=0.02), FadeIn(fl_),
                      run_time=2.0)
            self.play(FadeIn(side[:3]))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(l2))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(l1))
            self.play(FadeIn(side[3:6]))
            vo.wait_until("d")
            self.play(FadeIn(side[6]))
        self.wait(0.4)
        self.clear_scene()
