from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import p_ball, plain_axes, polyline, pnorm, square_axes


class TVS(VoiceoverScene):
    def construct(self):
        self.card()
        self.seminorms()
        self.locally_compact()
        self.pless()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Spaces without norms", r"Why does Grandpa Rudin start with topological vector spaces?",
                            lit=(), part=8)
        with self.voiceover("Chapter two: why Rudin's Functional Analysis begins with spaces that have no norm at all."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def seminorms(self):
        ax = plain_axes([-1, 1, 0.5], [-1.4, 1.4, 1], 5.2, 3.2).move_to([-3.6, -0.3, 0])
        x = np.linspace(-1, 1, 600)
        f0 = np.exp(-3 * x * x)
        f1 = f0 + 0.08 * np.sin(25 * x)  # close in sup, far in the derivative
        g0 = polyline(ax, x, f0, color=C.FUNC, stroke_width=3.5)
        g1 = polyline(ax, x, f1, color=C.APPROX, stroke_width=2.5)
        d0 = np.abs(f1 - f0).max()
        d1 = np.abs(np.gradient(f1 - f0, x)).max()
        d2 = np.abs(np.gradient(np.gradient(f1 - f0, x), x)).max()
        assert d0 < 0.1 < 1 < d1 < d2
        rows = VGroup(
            label(r"$C^\infty[-1, 1]$: \ closeness should control every derivative:", font_size=26),
            MathTex(r"p_k(f) = \sup |f^{(k)}|, \quad k = 0, 1, 2, \ldots", font_size=30, color=C.EPS),
            MathTex(rf"p_0(g - f) = {d0:.3f}, \ \ p_1(g - f) = {d1:.2f}, \ \ p_2(g - f) = {d2:.1f}", font_size=26),
            label(r"neighborhoods of $0$: \ $\{f : p_0(f) < \varepsilon, \ldots, p_k(f) < \varepsilon\}$", font_size=24),
            label(r"countably many seminorms, \ one metric (FA 1.24), \ complete: \ a \emph{Fr\'echet space}",
                  font_size=24, color=C.INNER),
            label(r"no single norm gives this topology \ (Part 9's test functions need it)", font_size=24,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.0, -0.6, 0])
        for r_ in rows:
            if r_.width > 7.0:
                r_.width = 7.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.0, -0.6, 0])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.1, -0.6, 0])
        lab = VGroup(MathTex(r"f", font_size=28, color=C.FUNC).next_to(ax.c2p(0.0, 1.0), UP, buff=0.12),
                     MathTex(r"g = f + 0.08\sin 25x", font_size=24, color=C.APPROX).next_to(ax, DOWN, buff=0.1))
        head = label(r"Some spaces need infinitely many norms at once", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Some important spaces have no single norm. Take the smooth functions on an interval. "
            "<bookmark mark='b'/> These two are within 0.08 of each other, but their derivatives differ by two, and "
            "their second derivatives by fifty. For smooth functions, close should mean close in every derivative. "
            "<bookmark mark='c'/> So the topology uses a whole sequence of seminorms, the sups of the k-th "
            "derivatives. Countably many seminorms still give a metric, and the space is complete: a Fréchet space. "
            "But no single norm does the job, and the test functions of Part 9 are worse still. That's why Grandpa "
            "Rudin starts with topological vector spaces."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g0), FadeIn(lab[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(g1), FadeIn(lab[1]))
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:5]))
            self.play(FadeIn(rows[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def locally_compact(self):
        ax = plain_axes([0.5, 8.5, 1], [0, 1.2, 0.5], 6.0, 2.2).move_to([-3.3, 0.9, 0])
        nT = ValueTracker(1)

        def bar():
            n = int(round(nT.get_value()))
            return VGroup(Rectangle(width=0.4, height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=C.EPS,
                                    fill_opacity=0.9).move_to(ax.c2p(n, 0.5)),
                          MathTex(rf"e_{{{n}}}", font_size=26, color=C.EPS).next_to(ax.c2p(n, 1), UP, buff=0.05))

        eb = always_redraw(bar)
        # pairwise distances: sqrt 2
        E = np.eye(8)
        D = np.linalg.norm(E[:, None, :] - E[None, :, :], axis=-1)
        assert np.allclose(D[~np.eye(8, dtype=bool)], math.sqrt(2))
        bx = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.1).move_to([-3.3, -2.0, 0])
        bx.set_opacity(0.3)
        unit = Circle(radius=bx.c2p(1, 0)[0] - bx.c2p(0, 0)[0], color=GREY_B, stroke_width=2).move_to(bx.c2p(0, 0))
        pts = [np.array([math.cos(a), math.sin(a)]) for a in (0, 2 * math.pi / 3, 4 * math.pi / 3)]
        ball_pts = VGroup(*[Dot(bx.c2p(*p), radius=0.06, color=C.EPS) for p in pts])
        cover = VGroup(*[Circle(radius=0.7 * (bx.c2p(1, 0)[0] - bx.c2p(0, 0)[0]), color=C.PATHOLOGY, stroke_width=2)
                         .move_to(bx.c2p(*p)) for p in pts])
        rows = VGroup(
            label(r"in $\ell^2$, \ $\|e_m - e_n\| = \sqrt 2$ for all $m \ne n$:", font_size=24),
            label(r"a ball of radius $0.7$ holds at most one $e_n$,", font_size=24),
            label(r"so no finitely many such balls cover the unit ball", font_size=24, color=C.PATHOLOGY),
            label(r"\textbf{FA 1.22} \ (F.~Riesz) \ a topological vector space with a", font_size=24, color=C.EPS),
            label(r"compact neighborhood of $0$ is finite-dimensional", font_size=24, color=C.EPS),
            label(r"the honest end of Heine--Borel \ (Part 1's promise)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, -0.5, 0])
        sch = VGroup(note(r"schematic:"), note(r"three of the $e_n$,"), note(r"in a plane")).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).to_corner(DL, buff=0.35)
        head = label(r"The unit ball is never compact in infinite dimensions", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part 1 promised that closed and bounded doesn't mean compact beyond R n. Here's the "
            "honest end of that story. The unit vectors of l two slide off to the right, and every two of them are "
            "root two apart. <bookmark mark='b'/> A ball of radius 0.7 holds at most one of them, so no finite "
            "collection of such balls covers the unit ball. <bookmark mark='c'/> Riesz proved more: a topological "
            "vector space in which some neighborhood of zero is compact must be finite-dimensional. In infinite "
            "dimensions, compactness has to come from somewhere else."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(eb), FadeIn(rows[0]))
            self.play(nT.animate.set_value(8), run_time=3.5, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(bx), Create(unit), FadeIn(ball_pts), Create(cover), FadeIn(sch), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        eb.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pless(self):
        ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.7).move_to([-3.6, -0.6, 0])
        ax.set_opacity(0.3)
        star = p_ball(ax, 0.5, C.PATHOLOGY)
        hull = Polygon(ax.c2p(1, 0), ax.c2p(0, 1), ax.c2p(-1, 0), ax.c2p(0, -1), color=C.EPS, stroke_width=2)
        hull = DashedVMobject(hull, num_dashes=40)
        u, v = np.array([1.0, 0.0]), np.array([0.0, 1.0])
        assert abs(pnorm((u + v) / 2, 0.5) - 2.0) < 1e-12
        rows = VGroup(
            label(r"$L^p[0, 1]$ for $0 < p < 1$: \ $d(f, g) = \int |f - g|^p$", font_size=26),
            label(r"a complete metric vector space, \ but its balls are not convex", font_size=24),
            label(r"\textbf{FA 1.47} \ its only continuous linear functional is $0$", font_size=26, color=C.PATHOLOGY),
            label(r"a convex neighborhood of $0$ would have to be everything", font_size=22, color=GREY_A),
            label(r"so functional analysis keeps \emph{local convexity}", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, -0.6, 0])
        for r_ in rows:
            if r_.width > 7.2:
                r_.width = 7.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, -0.6, 0])
        lab = VGroup(MathTex(r"\{|x|^{1/2} + |y|^{1/2} \le 1\}", font_size=26, color=C.PATHOLOGY).next_to(ax, UP, buff=0.05),
                     label(r"dashed: \ its convex hull", font_size=20, color=C.EPS).next_to(ax, DOWN, buff=0.05))
        head = label(r"A space with no functionals at all", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> One more warning. For p below one, L p is still a complete metric vector space, "
            "but its balls cave in, like this star. <bookmark mark='b'/> And it has no continuous linear functionals "
            "at all, except zero: the convex hull of any ball is the whole space. Hahn-Banach can't work there. "
            "<bookmark mark='c'/> So the theory keeps one assumption: local convexity, a base of convex "
            "neighborhoods of zero."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(star), FadeIn(lab[0]), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(hull), FadeIn(lab[1]), FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()
