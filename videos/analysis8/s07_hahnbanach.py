from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes, polyline, square_axes


class HahnBanach(VoiceoverScene):
    def construct(self):
        self.card()
        self.sandwich()
        self.separation()
        self.consequences()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Hahn--Banach", r"Are there enough functionals to see everything?", lit=(1932,), part=8)
        with self.voiceover("Chapter six: the Hahn-Banach theorem, the fourth pillar, and the only one not built on "
                            "Baire."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sandwich(self):
        ax = plain_axes([-3, 3, 1], [-2.6, 2.6, 1], 6.0, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -1.0, 0])
        y = np.linspace(-3, 3, 600)
        lo = 0.5 * y - np.sqrt(1 + y * y)
        hi = np.sqrt(1 + y * y) - 0.5 * y
        g_lo = runs(ax, y, lo, C.SEQ, 3)  # both curves leave the window at the ends: cut, not drawn over the frame
        g_hi = runs(ax, y, hi, C.APPROX, 3)
        smax, imin = lo.max(), hi.min()
        assert abs(smax + math.sqrt(0.75)) < 1e-4 and abs(imin - math.sqrt(0.75)) < 1e-4 and smax <= imin
        band = Rectangle(width=6.0, height=ax.c2p(0, imin)[1] - ax.c2p(0, smax)[1], stroke_width=0, fill_color=C.EPS,
                         fill_opacity=0.18).move_to(ax.c2p(0, 0))
        top = DashedLine(ax.c2p(-3, imin), ax.c2p(3, imin), color=C.APPROX, stroke_width=1.5)
        bot = DashedLine(ax.c2p(-3, smax), ax.c2p(3, smax), color=C.SEQ, stroke_width=1.5)
        l_lo = MathTex(r"f(y) - p(y - x_0)", font_size=24, color=C.SEQ).move_to(ax.c2p(1.7, -2.15))
        l_hi = MathTex(r"p(y + x_0) - f(y)", font_size=24, color=C.APPROX).move_to(ax.c2p(1.7, 2.15))
        y_l = MathTex(r"y \in M", font_size=22, color=GREY_B).next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.3)
        setup = VGroup(
            label(r"$M$ = the $x$-axis in $\R^2$, \ $f(t, 0) = \tfrac t2$, \ $p$ = the Euclidean norm, \ $x_0 = (0, 1)$",
                  font_size=24),
            label(r"extend: \ $F(t, s) = \tfrac t2 + cs$ \ with \ $F \le p$ \ needs, for all $y$,", font_size=24),
            MathTex(r"f(y) - p(y - x_0) \;\le\; c \;\le\; p(y + x_0) - f(y)", font_size=30, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"subtract: \ the left side never beats the right,", font_size=22),
            label(r"by the triangle inequality for $p$:", font_size=22),
            MathTex(r"f(y) + f(y') \le p(y + y') \le p(y - x_0) + p(y' + x_0)", font_size=22),
            MathTex(rf"\sup(\text{{blue}}) = {smax:.4f} \le {imin:.4f} = \inf(\text{{pink}})", font_size=24, color=C.EPS),
            label(r"any $c$ in the yellow band works: \ $|c| \le \sqrt{3}/2$", font_size=22, color=C.EPS),
            label(r"one dimension at a time; \ the infinite step is", font_size=22, color=GREY_A),
            label(r"Hausdorff maximality, \ logic with no picture", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([3.7, -1.0, 0])
        for r_ in side:
            if r_.width > 5.6:
                r_.width = 5.6
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([3.7, -1.0, 0])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([3.8, -1.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hahn-Banach extends a linear functional from a subspace to the whole space without "
            "breaking a bound. Here's the key step, in the plane: a functional on the x-axis, bounded by the length, "
            "extended to one more direction. <bookmark mark='b'/> The new value c must sit above every blue lower "
            "bound and below every pink upper bound. <bookmark mark='c'/> And it can: the highest blue point is below "
            "the lowest pink point, by the triangle inequality. Any c in the yellow band is a valid extension. "
            "<bookmark mark='d'/> That handles one dimension. Infinitely many need Hausdorff's maximality principle: "
            "pure logic, which no picture can show."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(setup[:2]), Create(ax), FadeIn(y_l))
            vo.wait_until("b")
            self.play(FadeIn(setup[2]), Create(g_lo), Create(g_hi), FadeIn(l_lo), FadeIn(l_hi))
            vo.wait_until("c")
            self.play(Create(top), Create(bot), FadeIn(band), FadeIn(side[:5]))
            vo.wait_until("d")
            self.play(FadeIn(side[5:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def separation(self):
        d = load("separation")
        A, B, pa, pb, nrm, c = d["A"], d["B"], d["pa"], d["pb"], d["nrm"], float(d["c"])
        ell, pts, gauge = d["ell"], d["pts"], d["gauge"]
        ax = square_axes([-3.6, 3.2, 1], [-2.6, 2.6, 1], 0.95).move_to([-3.2, -0.7, 0])
        ax.set_opacity(0.3)
        PA = Polygon(*[ax.c2p(*p) for p in A], color=C.SEQ, stroke_width=2.5, fill_opacity=0.25)
        PB = Polygon(*[ax.c2p(*p) for p in B], color=C.APPROX, stroke_width=2.5, fill_opacity=0.25)
        tg = np.array([-nrm[1], nrm[0]])
        lines = VGroup()
        for k in range(-3, 4):
            p0 = (c + 0.45 * k) * nrm
            ln = Line(ax.c2p(*(p0 - 3.2 * tg)), ax.c2p(*(p0 + 3.2 * tg)), color=C.EPS if k == 0 else C.FUNCTIONAL,
                      stroke_width=3.5 if k == 0 else 1.2)
            if k:
                ln.set_stroke(opacity=0.5)
            lines.add(ln)
        seg = DashedLine(ax.c2p(*pa), ax.c2p(*pb), color=WHITE, stroke_width=2)
        assert np.all(A @ nrm < c) and np.all(B @ nrm > c)
        lab = MathTex(rf"\Lambda < {c:.3f} \text{{ on }} A, \ \ \Lambda > {c:.3f} \text{{ on }} B", font_size=26,
                      color=C.EPS).next_to(ax, DOWN, buff=0.1)
        bx = square_axes([-2.3, 2.3, 1], [-1.4, 1.4, 1], 0.95).move_to([3.6, 0.6, 0])
        bx.set_opacity(0.3)
        a_, b_ = float(ell[0]), float(ell[1])
        th = np.linspace(0, 2 * np.pi, 300)
        K = VMobject(color=C.CONNECTED_SET, stroke_width=3, fill_color=C.CONNECTED_SET, fill_opacity=0.2).set_points_as_corners(
            [bx.c2p(a_ * math.cos(t), b_ * math.sin(t)) for t in th])
        scaled = VGroup(*[DashedVMobject(VMobject(color=GREY_B, stroke_width=1.5).set_points_as_corners(
            [bx.c2p(g * a_ * math.cos(t), g * b_ * math.sin(t)) for t in th]), num_dashes=40) for g in gauge])
        pd = VGroup(*[Dot(bx.c2p(*p), radius=0.06, color=WHITE) for p in pts])
        pl = VGroup(*[MathTex(rf"\mu_K = {g:.3f}", font_size=20).next_to(bx.c2p(*p), UR, buff=0.03) for p, g in zip(pts, gauge)])
        g_l = VGroup(MathTex(r"\mu_K(x) = \inf\{t > 0 : x \in tK\}", font_size=26, color=C.CONNECTED_SET),
                     label(r"the gauge: \ how far to scale $K$ to reach $x$", font_size=22, color=GREY_A),
                     label(r"a convex $K$ gives a sublinear $\mu_K$, \ the $p$ of the sandwich", font_size=22,
                           color=GREY_A)).arrange(DOWN, buff=0.08).next_to(bx, DOWN, buff=0.15)
        head = label(r"\textbf{FA 3.4} \ disjoint convex sets are separated by a hyperplane", font_size=30).to_edge(UP,
                                                                                                         buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The geometric form: two disjoint convex sets, one compact and one closed, can be "
            "separated by a closed hyperplane. <bookmark mark='b'/> For two convex polygons, the hyperplane through the "
            "midpoint of their closest points, perpendicular to the gap, does it: the functional is below the yellow "
            "level on one set and above it on the other. <bookmark mark='c'/> In general the proof feeds the sandwich "
            "a special sublinear function: the gauge of a convex set, how far you must scale the set to reach a "
            "point."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(PA), FadeIn(PB))
            vo.wait_until("b")
            self.play(Create(seg))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1), FadeIn(lab), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(K), FadeIn(pd))
            self.play(Create(scaled), FadeIn(pl), FadeIn(g_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consequences(self):
        rows = VGroup(
            label(r"\textbf{RCA 5.20--5.21} \ consequences in a normed space $X$:", font_size=28),
            label(r"for every $x_0 \ne 0$ there is $\Lambda \in X^*$ with $\|\Lambda\| = 1$ and $\Lambda x_0 = \|x_0\|$",
                  font_size=26, color=C.EPS),
            MathTex(r"\|x\| = \sup\{|\Lambda x| : \Lambda \in X^*, \ \|\Lambda\| \le 1\}", font_size=32),
            label(r"functionals separate points: \ if $\Lambda x = \Lambda y$ for all $\Lambda$, \ then $x = y$", font_size=26),
            label(r"a closed subspace $M$ misses $x_0$ \ $\iff$ \ some $\Lambda$ vanishes on $M$ but not at $x_0$",
                  font_size=26),
            label(r"the dual is never too small \ (compare $L^p$, $p < 1$, \ chapter 2)", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        for r_ in rows:
            if r_.width > 7.6:
                r_.width = 7.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([2.55, -0.3, 0])
        ax = square_axes([-1.4, 1.4, 1], [-1.4, 1.4, 1], 1.45).move_to([-4.6, -0.5, 0])
        ax.set_opacity(0.3)
        x0 = np.array([0.6, 0.3])
        nx = float(np.abs(x0).sum())
        dia = Polygon(*[ax.c2p(*(nx * np.array(v))) for v in ((1, 0), (0, 1), (-1, 0), (0, -1))], color=C.DIST, stroke_width=3,
                      fill_opacity=0.15)
        sup = Line(ax.c2p(nx + 0.45, -0.45), ax.c2p(-0.45, nx + 0.45), color=C.EPS, stroke_width=3.5)
        xd = Dot(ax.c2p(*x0), radius=0.08, color=WHITE)
        lab = VGroup(MathTex(r"x_0 = (0.6, 0.3), \ \|x_0\|_1 = 0.9", font_size=22).next_to(ax, UP, buff=0.05),
                     MathTex(r"\Lambda(x) = x_1 + x_2: \ \|\Lambda\|_\infty = 1, \ \Lambda x_0 = 0.9", font_size=22,
                             color=C.EPS).next_to(ax, DOWN, buff=0.08))
        assert abs(x0.sum() - nx) < 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> The consequences are what make duality work. Every nonzero vector has a functional "
            "of norm one that measures its full length. <bookmark mark='b'/> So the norm of x is the supremum of the "
            "functionals over the dual unit ball, and functionals separate points. <bookmark mark='c'/> And a vector "
            "is outside a closed subspace exactly when some functional kills the subspace but not the vector. A "
            "normed space always has enough functionals to see everything, unlike L p for p below one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]), Create(ax), FadeIn(dia), FadeIn(xd), FadeIn(lab[0]))
            self.play(Create(sup), FadeIn(lab[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:]))
        self.wait(0.4)
        self.clear_scene()
