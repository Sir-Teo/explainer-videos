from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import load, polyline
from videos.analysis1.compute import sd_f, sd_g


def ball_panel(kind: str, center=ORIGIN, unit=1.15, font_size=30):
    """A small coordinate frame with the open unit ball of one metric on R^2."""
    ax = VGroup(Line(LEFT * 1.6 * unit, RIGHT * 1.6 * unit, color=GREY_D, stroke_width=1.5),
                Line(DOWN * 1.6 * unit, UP * 1.6 * unit, color=GREY_D, stroke_width=1.5))
    if kind == "2":
        shape = Circle(radius=unit)
        f = MathTex(r"d_2 = \sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2}", font_size=font_size - 6)
        name = r"Euclidean"
    elif kind == "1":
        shape = Polygon(RIGHT * unit, UP * unit, LEFT * unit, DOWN * unit)
        f = MathTex(r"d_1 = |x_1 - y_1| + |x_2 - y_2|", font_size=font_size - 6)
        name = r"taxicab"
    elif kind == "inf":
        shape = Square(side_length=2 * unit)
        f = MathTex(r"d_\infty = \max(|x_1 - y_1|, |x_2 - y_2|)", font_size=font_size - 6)
        name = r"max"
    else:
        shape = Dot(radius=0.08)
        f = MathTex(r"d(p, q) = 1 \text{ if } p \ne q", font_size=font_size - 6)
        name = r"discrete"
    if kind != "disc":
        shape.set_fill(C.OPEN_SET, opacity=0.18).set_stroke(width=0)
        edge = DashedVMobject(shape.copy().set_stroke(C.OPEN_SET, width=3).set_fill(opacity=0), num_dashes=40)
        shape = VGroup(shape, edge)
    else:
        shape.set_color(C.OPEN_SET)
    title = label(name, font_size=font_size, color=GREY_A)
    g = VGroup(ax, shape)
    title.next_to(g, UP, buff=0.25)
    f.next_to(g, DOWN, buff=0.3)
    panel = VGroup(g, title, f).move_to(center)
    panel.ball = shape
    return panel


class Distance(VoiceoverScene):
    def construct(self):
        self.card()
        self.vectors()
        self.schwarz()
        self.triangle()
        self.metric()
        self.gallery()
        self.functions()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"What ``close'' means: metric spaces", r"What is the distance between two functions?",
                            lit=(1906,), part=1)
        with self.voiceover(
            "Chapter five. So far everything has lived on a line. But the point of this series is to treat functions "
            "as points in a space, with distances between them. So we need to ask what a distance has to be."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def vectors(self):
        plane = NumberPlane(x_range=[-1, 6, 1], y_range=[-1, 4, 1], x_length=7.0, y_length=5.0,
                            background_line_style={"stroke_color": GREY_D, "stroke_opacity": 0.5, "stroke_width": 1},
                            axis_config={"stroke_color": GREY_C}).shift(LEFT * 3.0 + DOWN * 0.3)
        o = plane.c2p(0, 0)
        x = Arrow(o, plane.c2p(3.2, 2.6), buff=0, color=C.SEQ, stroke_width=5)
        y = Arrow(o, plane.c2p(4.6, 0.9), buff=0, color=C.APPROX, stroke_width=5)
        xl = MathTex(r"\mathbf{x}", font_size=38, color=C.SEQ).next_to(x.get_end(), UP, buff=0.1)
        yl = MathTex(r"\mathbf{y}", font_size=38, color=C.APPROX).next_to(y.get_end(), RIGHT, buff=0.1)
        defs = VGroup(
            MathTex(r"\mathbf{x} = (x_1, \ldots, x_k) \in \R^k", font_size=36),
            MathTex(r"\mathbf{x} \cdot \mathbf{y} = \sum_{i=1}^{k} x_i y_i", font_size=36, color=C.INNER),
            MathTex(r"|\mathbf{x}| = (\mathbf{x} \cdot \mathbf{x})^{1/2}", font_size=36, color=C.DIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.9, 0.6, 0])
        with self.voiceover(
            "Start with the familiar case. <bookmark mark='a'/> Points of k-dimensional space are lists of k real "
            "numbers, which we can add and scale like arrows. <bookmark mark='b'/> The inner product multiplies "
            "coordinates and adds, <bookmark mark='c'/> and the length of x is the square root of x dotted with itself."
        ) as vo:
            self.play(Create(plane), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(defs[0]))
            self.play(GrowArrow(x), GrowArrow(y), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(defs[1]))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]))
        self.plane, self.x, self.y, self.xl, self.yl = plane, x, y, xl, yl
        self.play(FadeOut(defs))

    # ------------------------------------------------------------------
    def schwarz(self):
        plane, x, y = self.plane, self.x, self.y
        xv, yv = np.array([3.2, 2.6]), np.array([4.6, 0.9])
        proj = (xv @ yv) / (yv @ yv) * yv
        shadow = Line(plane.c2p(0, 0), plane.c2p(*proj), color=C.INNER, stroke_width=7)
        drop = DashedLine(plane.c2p(*xv), plane.c2p(*proj), color=GREY_B, stroke_width=2)
        gap = Arrow(plane.c2p(*proj), plane.c2p(*xv), buff=0, color=C.EPS, stroke_width=5)
        ra = RightAngle(Line(plane.c2p(*proj), plane.c2p(0, 0)), Line(plane.c2p(*proj), plane.c2p(*xv)), length=0.2,
                        color=GREY_B, quadrant=(1, 1))
        sh_l = label(r"shadow of $\mathbf x$ on $\mathbf y$", font_size=24, color=C.INNER).next_to(shadow, DOWN, buff=0.1)
        sh_l.shift(RIGHT * 0.3 + DOWN * 0.15)
        gap_l = label(r"the gap", font_size=26, color=C.EPS).next_to(gap, RIGHT, buff=0.1)
        stmt = VGroup(label(r"\textbf{Cauchy--Schwarz} (Rudin 1.35)", font_size=28, color=GREY_A),
                      MathTex(r"|\mathbf{x}\cdot\mathbf{y}| \le |\mathbf{x}|\,|\mathbf{y}|", font_size=42))
        stmt.arrange(DOWN, buff=0.15).move_to([3.9, 2.9, 0])
        with self.voiceover(
            "The one inequality that makes all of this work is Cauchy–Schwarz: <bookmark mark='s'/> the inner product of "
            "x and y is at most the product of their lengths. <bookmark mark='p'/> Here's the picture behind the proof. "
            "Drop x onto the line through y: that gives x's shadow on y. <bookmark mark='g'/> The gap between x and its "
            "shadow is an honest vector, so its length squared can't be negative. That's the whole proof; the rest is "
            "algebra."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(stmt))
            vo.wait_until("p")
            self.play(Create(drop), Create(shadow), FadeIn(sh_l), Create(ra))
            vo.wait_until("g")
            self.play(GrowArrow(gap), FadeIn(gap_l))
        rows = [
            MathTex(r"0", r"\le", r"|B\mathbf{x} - C\mathbf{y}|^2", font_size=34),
            MathTex(r"0", r"\le", r"B^2|\mathbf{x}|^2 - 2BC\,(\mathbf{x}\cdot\mathbf{y}) + C^2|\mathbf{y}|^2", font_size=34),
            MathTex(r"0", r"\le", r"B^2|\mathbf{x}|^2 - 2BC^2 + C^2 B", font_size=34),
            MathTex(r"0", r"\le", r"B\,\big(B|\mathbf{x}|^2 - C^2\big)", font_size=34),
            MathTex(r"(\mathbf{x}\cdot\mathbf{y})^2", r"\le", r"|\mathbf{x}|^2|\mathbf{y}|^2", font_size=34),
        ]
        whys = [why(r"a squared length is never negative"), why(r"expand"),
                why(r"$\mathbf x\cdot\mathbf y = C$ and $|\mathbf y|^2 = B$"), why(r"factor"), why(r"divide by $B > 0$")]
        for r_ in rows:
            r_.scale(1.1)
        grp = VGroup(*rows)
        bc = MathTex(r"B = |\mathbf y|^2, \quad C = \mathbf x\cdot\mathbf y, \quad B\mathbf x - C\mathbf y = B\,(\text{the gap})",
                     font_size=36, color=GREY_A).to_edge(UP, buff=0.4)
        step = ladder(self, rows, whys, keep=5, top=2.6, buff=0.4, x=-1.2, edge=6.95)
        with self.voiceover(
            "Call the length of y squared B, and the inner product C. <bookmark mark='a'/> Then B x minus C y is B "
            "times the gap, so its length squared is at least zero. <bookmark mark='b'/> Expand it. "
            "<bookmark mark='c'/> Substitute C for the inner product and B for y's length squared, "
            "<bookmark mark='d'/> and factor out B. <bookmark mark='e'/> Since B is positive, the inner product squared "
            "is at most the product of the squared lengths. That's Cauchy–Schwarz."
        ) as vo:
            self.play(FadeOut(stmt), FadeOut(VGroup(plane, x, y, self.xl, self.yl, shadow, drop, gap, ra, sh_l, gap_l)))
            self.play(FadeIn(bc))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(i, run_time=1.0)
        box = SurroundingRectangle(rows[-1], color=C.INNER, buff=0.12, corner_radius=0.1)
        self.play(Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def triangle(self):
        A, B_, Cc = np.array([-4.5, -1.8, 0]), np.array([-0.6, 1.6, 0]), np.array([2.4, -1.4, 0])
        xa = Arrow(A, B_, buff=0, color=C.SEQ, stroke_width=5)
        ya = Arrow(B_, Cc, buff=0, color=C.APPROX, stroke_width=5)
        sa = Arrow(A, Cc, buff=0, color=C.DIST, stroke_width=5)
        xl = MathTex(r"\mathbf x", font_size=36, color=C.SEQ).next_to(xa.get_center(), UL, buff=0.1)
        yl = MathTex(r"\mathbf y", font_size=36, color=C.APPROX).next_to(ya.get_center(), UR, buff=0.1)
        sl = MathTex(r"\mathbf x + \mathbf y", font_size=36, color=C.DIST).next_to(sa.get_center(), DOWN, buff=0.15)
        rows = VGroup(
            MathTex(r"|\mathbf x + \mathbf y|^2 = |\mathbf x|^2 + 2\,\mathbf x\cdot\mathbf y + |\mathbf y|^2", font_size=34),
            MathTex(r"\le |\mathbf x|^2 + 2|\mathbf x||\mathbf y| + |\mathbf y|^2 = (|\mathbf x| + |\mathbf y|)^2",
                    font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.5)
        rows[1].shift(RIGHT * 1.75)
        res = MathTex(r"|\mathbf x + \mathbf y| \le |\mathbf x| + |\mathbf y|", font_size=40, color=C.DIST)
        res = boxed(res, color=C.DIST).move_to([4.2, 0.2, 0])
        with self.voiceover(
            "Cauchy–Schwarz immediately gives the triangle inequality. <bookmark mark='a'/> Expand the length of x plus "
            "y squared; <bookmark mark='b'/> bound the middle term by Cauchy–Schwarz; and what's left is a perfect "
            "square. <bookmark mark='c'/> The side of a triangle is never longer than the other two sides together."
        ) as vo:
            self.play(GrowArrow(xa), GrowArrow(ya), FadeIn(xl), FadeIn(yl))
            self.play(GrowArrow(sa), FadeIn(sl))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def metric(self):
        head = VGroup(label(r"\textbf{Metric space} (Rudin 2.15; Fr\'echet, 1906)", font_size=30, color=GREY_A),
                      label(r"a set $X$ with a distance $d(p, q)$ such that", font_size=32)).arrange(DOWN, buff=0.15)
        head.to_edge(UP, buff=0.5)
        ax = VGroup(
            MathTex(r"\text{(a)}\quad d(p,q) > 0 \text{ if } p \ne q, \qquad d(p,p) = 0", font_size=34),
            MathTex(r"\text{(b)}\quad d(p,q) = d(q,p)", font_size=34),
            MathTex(r"\text{(c)}\quad d(p,q) \le d(p,r) + d(r,q)", font_size=34),
        )
        rows_y = (1.45, -0.05, -1.65)
        for a_, y in zip(ax, rows_y):
            a_.move_to([0, y, 0]).to_edge(LEFT, buff=0.7)
        coda = label(r"Everything from here to chapter 11 uses only (a), (b), (c).", font_size=30, color=C.EPS)
        coda.to_edge(DOWN, buff=0.35)
        # a picture beside each axiom
        def pt(x, y, name, side=DOWN):
            return VGroup(Dot([x, y, 0], radius=0.07), MathTex(name, font_size=28).next_to([x, y, 0], side, buff=0.12))

        y = rows_y[0]
        pa, qa = pt(2.3, y, "p"), pt(5.1, y, "q")
        da = VGroup(Line([2.3, y, 0], [5.1, y, 0], color=C.DIST, stroke_width=4),
                    MathTex(r"d(p,q) > 0", font_size=26, color=C.DIST).next_to([3.7, y, 0], UP, buff=0.12))
        y = rows_y[1]
        pb, qb = pt(2.3, y, "p", LEFT), pt(5.1, y, "q", RIGHT)
        db = VGroup(CurvedArrow([2.4, y + 0.1, 0], [5.0, y + 0.1, 0], angle=-0.6, color=C.DIST, stroke_width=3,
                                tip_length=0.15),
                    CurvedArrow([5.0, y - 0.1, 0], [2.4, y - 0.1, 0], angle=-0.6, color=C.DIST, stroke_width=3,
                                tip_length=0.15),
                    MathTex(r"d(p,q)", font_size=24, color=C.DIST).move_to([3.7, y + 0.5, 0]),
                    MathTex(r"d(q,p)", font_size=24, color=C.DIST).move_to([3.7, y - 0.5, 0]))
        P, Q, R = np.array([2.1, -2.35, 0]), np.array([5.3, -2.35, 0]), np.array([4.0, -1.05, 0])
        tri = VGroup(Line(P, Q, color=C.DIST, stroke_width=5),
                     Line(P, R, color=C.APPROX, stroke_width=3.5), Line(R, Q, color=C.APPROX, stroke_width=3.5),
                     *[Dot(v, radius=0.07) for v in (P, Q, R)],
                     MathTex(r"p", font_size=28).next_to(P, LEFT, buff=0.12),
                     MathTex(r"q", font_size=28).next_to(Q, RIGHT, buff=0.12),
                     MathTex(r"r", font_size=28).next_to(R, UP, buff=0.12))
        tlab = VGroup(MathTex(r"d(p,q)", font_size=24, color=C.DIST).next_to((P + Q) / 2, DOWN, buff=0.1),
                      MathTex(r"d(p,r)", font_size=24, color=C.APPROX).next_to((P + R) / 2, UL, buff=0.02),
                      MathTex(r"d(r,q)", font_size=24, color=C.APPROX).next_to((R + Q) / 2, UR, buff=0.02))
        with self.voiceover(
            "In 1906, Maurice Fréchet turned this into a definition. <bookmark mark='h'/> A metric space is a set "
            "together with a distance function d with three properties. <bookmark mark='a'/> Distances between "
            "different points are positive, and a point is at distance zero from itself. <bookmark mark='b'/> Distance "
            "is symmetric. <bookmark mark='c'/> And the triangle inequality: a detour through a third point is never "
            "shorter. <bookmark mark='d'/> That's all. Every theorem in the rest of this video uses only these three "
            "properties, so it holds in every metric space at once."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("h")
            self.play(FadeIn(head[1]))
            vo.wait_until("a")
            self.play(FadeIn(ax[0], shift=RIGHT * 0.2), FadeIn(pa), FadeIn(qa))
            self.play(Create(da[0]), FadeIn(da[1]))
            vo.wait_until("b")
            self.play(FadeIn(ax[1], shift=RIGHT * 0.2), FadeIn(pb), FadeIn(qb))
            self.play(Create(db[0]), FadeIn(db[2]))
            self.play(Create(db[1]), FadeIn(db[3]))
            vo.wait_until("c")
            self.play(FadeIn(ax[2], shift=RIGHT * 0.2), FadeIn(tri[3:]))
            self.play(Create(tri[0]), FadeIn(tlab[0]))
            self.play(Create(tri[1]), Create(tri[2]), FadeIn(tlab[1:]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(coda))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gallery(self):
        kinds = ["2", "1", "inf", "disc"]
        xs = [-5.3, -1.8, 1.8, 5.3]
        panels = VGroup(*[ball_panel(k, center=[x, 0.2, 0], unit=0.95, font_size=28) for k, x in zip(kinds, xs)])
        for p in panels:
            p[2].set_width(min(p[2].width, 3.2))
        head = label(r"Four distances on the same plane, and their balls of radius 1", font_size=32).to_edge(UP, buff=0.4)
        disc_note = label(r"ball of radius $1$: just the center", font_size=22, color=C.OPEN_SET)
        disc_note.next_to(panels[3][0], DOWN, buff=0.1).shift(UP * 0.55)
        with self.voiceover(
            "The same set can carry many distances. <bookmark mark='a'/> On the plane: the Euclidean distance, whose "
            "ball of radius one is a disk; <bookmark mark='b'/> the taxicab distance, adding the horizontal and vertical "
            "differences, whose ball is a diamond; <bookmark mark='c'/> the max distance, taking the larger of the two, "
            "whose ball is a square; <bookmark mark='d'/> and the discrete distance, where any two different points are "
            "at distance one. Its open ball of radius one contains only its center."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", panels):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=UP * 0.2))
            self.play(FadeIn(disc_note))
        self.wait(0.3)
        self.play(FadeOut(VGroup(panels, disc_note, head)))

        unit = 1.6
        circ = Circle(radius=unit, color=C.OPEN_SET, stroke_width=3)
        dia = Polygon(RIGHT * unit, UP * unit, LEFT * unit, DOWN * unit, color=C.CONNECTED_SET, stroke_width=3)
        sq = Square(side_length=2 * unit, color=C.CLOSED_SET, stroke_width=3)
        sm = Square(side_length=2 * unit / np.sqrt(2), color=C.CLOSED_SET, stroke_width=2, stroke_opacity=0.6)
        grp = VGroup(sq, circ, dia, sm).shift(LEFT * 3.2)
        lbls = VGroup(MathTex(r"d_\infty < 1", font_size=30, color=C.CLOSED_SET),
                      MathTex(r"d_2 < 1", font_size=30, color=C.OPEN_SET),
                      MathTex(r"d_1 < 1", font_size=30, color=C.CONNECTED_SET)).arrange(RIGHT, buff=0.6)
        lbls.next_to(sq, DOWN, buff=0.35)
        txt = VGroup(
            MathTex(r"d_\infty \le d_2 \le d_1 \le 2\,d_\infty", font_size=40),
            label(r"so every ball of one metric contains", font_size=30),
            label(r"a ball of the other two, around the same point:", font_size=30),
            label(r"they agree about what is \emph{near}.", font_size=30, color=C.EPS),
        ).arrange(DOWN, buff=0.25).move_to([3.4, 0, 0])
        with self.voiceover(
            "The first three disagree about distances, but not about nearness. <bookmark mark='n'/> Draw their balls "
            "together: the diamond sits inside the disk, which sits inside the square, which sits inside a diamond twice "
            "as big. <bookmark mark='t'/> So each kind of ball contains a ball of every other kind around the same "
            "point. We'll see in the next chapter that this means they agree about which sets are open, and about which "
            "sequences converge. The discrete distance agrees with none of them."
        ) as vo:
            self.play(Create(dia), FadeIn(lbls[2]))
            vo.wait_until("n")
            self.play(Create(circ), FadeIn(lbls[1]))
            self.play(Create(sq), FadeIn(lbls[0]))
            vo.wait_until("t")
            self.play(FadeIn(txt, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def functions(self):
        sd = load("supdist")
        xs_, ds = float(sd["x_star"]), float(sd["d_star"])
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.1, 0.5], x_length=8.6, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_numbers": True, "font_size": 22,
                               "decimal_number_config": {"num_decimal_places": 2}}).shift(LEFT * 1.8 + DOWN * 0.5)
        x = np.linspace(0, 1, 600)
        F = polyline(ax, x, sd_f(x), color=C.FUNC, stroke_width=4)
        G = polyline(ax, x, sd_g(x), color=C.APPROX, stroke_width=4)
        fl = MathTex(r"f", font_size=36, color=C.FUNC).next_to(ax.c2p(1, sd_f(1.0)), RIGHT, buff=0.15).shift(UP * 0.18)
        gl = MathTex(r"g", font_size=36, color=C.APPROX).next_to(ax.c2p(1, sd_g(1.0)), RIGHT, buff=0.15).shift(DOWN * 0.18)
        dfn = MathTex(r"d(f, g) = \sup_{0 \le x \le 1} |f(x) - g(x)|", font_size=40, color=C.DIST).to_edge(UP, buff=0.45)
        space = label(r"$C[0,1]$: the continuous functions on $[0,1]$", font_size=28, color=GREY_A).next_to(dfn, DOWN, buff=0.2)
        t = ValueTracker(0.0)

        def seg():
            v = t.get_value()
            a, b = sd_f(v), sd_g(v)
            return Line(ax.c2p(v, a), ax.c2p(v, b), color=C.DIST, stroke_width=4)

        def val():
            v = t.get_value()
            return MathTex(rf"|f(x) - g(x)| = {abs(sd_f(v) - sd_g(v)):.3f}", font_size=32, color=C.DIST).move_to([4.6, 1.2, 0])

        s_ = always_redraw(seg)
        v_ = always_redraw(val)
        with self.voiceover(
            "Now the big step. <bookmark mark='c'/> Let the points of our space be continuous functions on the interval "
            "from zero to one. <bookmark mark='d'/> The distance between two of them, f and g, is the biggest vertical "
            "gap between their graphs: the supremum of f of x minus g of x, in absolute value, over all x."
        ) as vo:
            self.play(Create(ax), FadeIn(space))
            self.play(Create(F), Create(G), FadeIn(fl), FadeIn(gl))
            vo.wait_until("d")
            self.play(Write(dfn))
        with self.voiceover(
            "<bookmark mark='s'/> Sweep across, measuring the gap. <bookmark mark='m'/> The largest gap here is at x "
            "about 0.207, where it's about 0.527. So the distance from f to g is 0.527."
        ) as vo:
            vo.wait_until("s")
            self.add(s_, v_)
            self.play(t.animate.set_value(1.0), run_time=3.0, rate_func=linear)
            vo.wait_until("m")
            self.play(t.animate.set_value(xs_), run_time=1.5)
        s_.clear_updaters()
        v_.clear_updaters()
        best = Line(ax.c2p(xs_, sd_f(xs_)), ax.c2p(xs_, sd_g(xs_)), color=C.DIST, stroke_width=7)
        best_l = MathTex(rf"d(f,g) = {ds:.3f}", font_size=36, color=C.DIST).move_to([4.6, 1.2, 0])
        assert abs(xs_ - 0.2074) < 1e-3 and abs(ds - 0.5267) < 1e-3
        self.play(FadeIn(best), FadeOut(s_), Transform(v_, best_l))
        props = VGroup(
            label(r"(a) \ $d(f,g) = 0$ only if $f = g$", font_size=24),
            label(r"(b) \ symmetric", font_size=24),
            label(r"(c) \ $|f - h| \le |f - g| + |g - h|$", font_size=24),
            label(r"\phantom{(c)} \ at each $x$; take the sup", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        props.move_to([5.05, -0.7, 0])
        with self.voiceover(
            "And it really is a distance. <bookmark mark='a'/> It's zero only when the graphs coincide; it's symmetric; "
            "<bookmark mark='c'/> and the triangle inequality holds at every single x, so it holds for the supremum too."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(props[:2]))
            vo.wait_until("c")
            self.play(FadeIn(props[2:]))
        self.wait(0.3)
        self.play(FadeOut(VGroup(G, gl, best, v_, props)))

        r = 0.12
        tube = ax.get_area(ax.plot(lambda v: sd_f(v) + r, x_range=[0, 1]), x_range=[0, 1],
                           bounded_graph=ax.plot(lambda v: sd_f(v) - r, x_range=[0, 1]), color=C.DIST, opacity=0.22)
        inside = VGroup(*[polyline(ax, x, sd_f(x) + 0.07 * np.sin(k * 6 * x + k), color=C.CONNECTED_SET, stroke_width=2.5)
                          for k in (1, 2, 3)])
        outside = polyline(ax, x, sd_f(x) + 0.2 * np.exp(-((x - 0.7) / 0.05) ** 2), color=C.PATHOLOGY, stroke_width=2.5)
        assert all(np.max(np.abs(0.07 * np.sin(k * 6 * x + k))) < r for k in (1, 2, 3))
        assert np.max(0.2 * np.exp(-((x - 0.7) / 0.05) ** 2)) > r
        tl = label(r"the ball of radius $0.12$\\around $f$ is a \textbf{tube}", font_size=28, color=C.DIST).move_to([4.85, 1.1, 0])
        il = label(r"inside: in the ball", font_size=26, color=C.CONNECTED_SET).move_to([4.85, 0.1, 0])
        ol = label(r"pokes out once:\\not in the ball", font_size=26, color=C.PATHOLOGY).move_to([4.85, -0.7, 0])
        with self.voiceover(
            "So a function is now a point, and the distance between two functions is a number. <bookmark mark='b'/> "
            "What does a ball look like? The functions within 0.12 of f are exactly the ones whose graphs stay inside a "
            "tube of half-width 0.12 around f's graph. <bookmark mark='i'/> These wiggly ones are inside the ball. "
            "<bookmark mark='o'/> This one pokes out at a single spot, and that's enough to put it outside. "
            "From now on, close means small distance, in whatever metric space we happen to be in."
        ) as vo:
            vo.wait_until("b")
            self.play(FadeIn(tube), FadeIn(tl))
            vo.wait_until("i")
            self.play(LaggedStart(*[Create(c) for c in inside], lag_ratio=0.3), FadeIn(il))
            vo.wait_until("o")
            self.play(Create(outside), FadeIn(ol))
        self.wait(0.5)
        self.clear_scene()
