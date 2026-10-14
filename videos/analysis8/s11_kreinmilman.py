from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import dense_points, load, p_ball, place_label, plain_axes, polyline, square_axes


class KreinMilman(VoiceoverScene):
    def construct(self):
        self.card()
        self.corners()
        self.no_corners()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Extreme points", r"Which points of a convex set cannot be split?", lit=(), part=8)
        with self.voiceover("Chapter ten: extreme points, and the Krein-Milman theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def corners(self):
        d = load("extreme")
        e1, e2, einf = float(d["ext_p1"]), float(d["ext_p2"]), float(d["ext_pinf"])
        groups = VGroup()
        specs = [(1.0, r"\ell^1", [(1, 0), (0, 1), (-1, 0), (0, -1)]), (2.0, r"\ell^2", None),
                 (np.inf, r"\ell^\infty", [(1, 1), (-1, 1), (-1, -1), (1, -1)])]
        for k, (p, nm, verts) in enumerate(specs):
            ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.2).move_to([-4.6 + 4.6 * k, 0.3, 0])
            ax.set_opacity(0.3)
            ball = p_ball(ax, p, C.DIST, fill=0.12, stroke_width=2.5)
            if verts:
                ext = VGroup(*[Dot(ax.c2p(*v), radius=0.1, color=C.EPS) for v in verts])
            else:
                ext = Circle(radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], color=C.EPS, stroke_width=6).move_to(ax.c2p(0, 0))
            t = MathTex(rf"\text{{the ball of }} {nm}", font_size=24).next_to(ax, UP, buff=0.05)
            groups.add(VGroup(ax, ball, ext, t))
        # a non-extreme boundary point of the diamond, split along its edge
        ax0 = groups[0][0]
        x = np.array([0.6, 0.4])
        v = np.array([0.25, -0.25])
        split = VGroup(Dot(ax0.c2p(*x), radius=0.07, color=WHITE),
                       Line(ax0.c2p(*(x - v)), ax0.c2p(*(x + v)), color=C.PATHOLOGY, stroke_width=5))
        assert abs(np.abs(x + v).sum() - 1) < 1e-12 and abs(np.abs(x - v).sum() - 1) < 1e-12
        tests = VGroup(
            label(r"$x$ is \emph{extreme} if $x = \frac{y + z}{2}$ with $y, z$ in the set forces $y = z = x$", font_size=26),
            MathTex(rf"\text{{splitting test, random boundary points in }} \R^3: \ \ell^1: {100 * e1:.0f}\%,\ \ "
                    rf"\ell^2: {100 * e2:.0f}\%,\ \ \ell^\infty: {100 * einf:.0f}\% \text{{ extreme}}", font_size=24,
                    color=GREY_A),
            label(r"\textbf{FA 3.23} \ (Krein--Milman) \ a compact convex set in a locally convex space", font_size=26,
                  color=C.EPS),
            label(r"is the closed convex hull of its extreme points", font_size=26, color=C.EPS),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.25)
        head = label(r"The corners of a convex set", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A point of a convex set is extreme if it isn't the midpoint of two other points of "
            "the set. <bookmark mark='b'/> A point on an edge of the diamond splits along the edge, so only the four "
            "corners are extreme. <bookmark mark='c'/> On the circle, every boundary point is extreme. On the square, "
            "only the corners again. The same test in three dimensions, on random boundary points, gives none, all, "
            "and none. <bookmark mark='d'/> Krein and Milman: a compact convex set is the closed convex hull of its "
            "extreme points. The corners are enough to rebuild the whole set."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(tests[0]), *[FadeIn(g[:2]) for g in groups], *[FadeIn(g[3]) for g in groups])
            vo.wait_until("b")
            self.play(FadeIn(split), FadeIn(groups[0][2]))
            vo.wait_until("c")
            self.play(Create(groups[1][2]), FadeIn(groups[2][2]))
            self.play(FadeIn(tests[1]))
            vo.wait_until("d")
            self.play(FadeIn(tests[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def no_corners(self):
        d = load("extreme")
        a = float(d["l1_a"])
        ax = plain_axes([0, 1, 0.25], [0, 4.2, 1], 5.4, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.5, -0.5, 0])
        x = np.linspace(0, 1, 800)
        f = 2 * x
        g1 = np.where(x <= a, 4 * x, 0)
        g2 = np.where(x > a, 4 * x, 0)
        gf = polyline(ax, x, f, color=WHITE, stroke_width=4)
        G1 = VGroup(polyline(ax, x[x <= a], g1[x <= a], color=C.SEQ, stroke_width=3),
                    Line(ax.c2p(a, 4 * a), ax.c2p(a, 0), color=C.SEQ, stroke_width=1.5),
                    Line(ax.c2p(a, 0), ax.c2p(1, 0), color=C.SEQ, stroke_width=3))
        G2 = VGroup(Line(ax.c2p(0, 0), ax.c2p(a, 0), color=C.APPROX, stroke_width=3),
                    polyline(ax, x[x > a], g2[x > a], color=C.APPROX, stroke_width=3))
        av = MathTex(r"f = \tfrac12(g_1 + g_2)", font_size=28).next_to(ax, UP, buff=0.1)
        # each label beside its own line, on the side away from the others (placed and checked against every stroke)
        obst = dense_points(VGroup(gf, G1, G2, ax))
        labs = VGroup(MathTex(r"f = 2x", font_size=26), MathTex(r"g_1", font_size=26, color=C.SEQ),
                      MathTex(r"g_2", font_size=26, color=C.APPROX))
        place_label(labs[0], ax.c2p(0.9, 1.8), obst, dirs=(DOWN, DR, RIGHT), buffs=(0.15, 0.25))
        place_label(labs[1], ax.c2p(0.42, 1.68), obst, dirs=(UL, LEFT, UP), buffs=(0.1, 0.15, 0.25), avoid=[labs[0]])
        place_label(labs[2], ax.c2p(0.9, 3.6), obst, dirs=(UL, LEFT, UP), buffs=(0.1, 0.15, 0.25), avoid=list(labs[:2]))
        rows = VGroup(
            label(r"in $L^1[0, 1]$, \ $\|f\|_1 = 1$: \ cut at $a = 1/\sqrt2$,", font_size=24),
            label(r"where half the mass is: \ $g_1 = 2f\,\mathbf 1_{[0, a]}$, \ $g_2 = 2f\,\mathbf 1_{(a, 1]}$", font_size=24),
            label(r"both of norm $1$", font_size=24),
            label(r"every unit vector splits this way:", font_size=24, color=C.PATHOLOGY),
            label(r"the ball of $L^1$ has \emph{no} extreme points", font_size=24, color=C.PATHOLOGY),
            label(r"but a dual ball is weak-$*$ compact (Alaoglu),", font_size=24),
            label(r"so it has extreme points (Krein--Milman)", font_size=24),
            label(r"so $L^1[0, 1]$ is not the dual of any Banach space", font_size=26, color=C.EPS),
            label(r"for probability measures, \ the extreme points", font_size=22, color=GREY_A),
            label(r"are the point masses $\delta_x$", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        rows.shift(np.array([-0.2, -0.5, 0]) - [rows.get_left()[0], rows.get_center()[1], 0])
        assert rows.get_right()[0] < 6.6 and rows.get_left()[0] > ax.get_right()[0] + 0.3
        head = label(r"A ball with no corners at all", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Now a surprise. In L one of the unit interval, take f equals two x, of norm one. "
            "<bookmark mark='b'/> Cut the interval where half the mass lies, at one over root two. Doubling f on "
            "each side gives two functions of norm one, and f is their average. <bookmark mark='c'/> Every unit vector "
            "splits like this, so the unit ball of L one has no extreme points at all. <bookmark mark='d'/> But a dual "
            "ball is weak-star compact by Alaoglu, so it has plenty of extreme points by Krein and Milman. "
            "Conclusion: L one is not the dual of any Banach space. Two compactness theorems, combined into a "
            "non-existence proof."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(gf), FadeIn(labs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(G1), FadeIn(labs[1]))
            self.play(Create(G2), FadeIn(labs[2]), FadeIn(av), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5:8]))
            self.play(FadeIn(rows[8:]))
        self.wait(0.4)
        self.clear_scene()
