from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import heatmap, load, square_axes


def fol(X, Y):
    return X**3 + Y**3 - 3 * X * Y


def crossings(segs, c, ylo, yhi):
    """How many times the curve (as segments) crosses the vertical line x = c between y = ylo and y = yhi."""
    n = 0
    for (x0, y0), (x1, y1) in segs:
        if min(x0, x1) <= c < max(x0, x1):
            yc = y0 + (c - x0) / (x1 - x0) * (y1 - y0)
            if ylo <= yc <= yhi:
                n += 1
    return n


class ImplicitFunction(VoiceoverScene):
    def construct(self):
        self.card()
        self.curve()
        self.theorem()
        self.rank()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"The implicit function theorem",
                            r"When does an equation $f(x, y) = 0$ define $y$ as a function of $x$?", lit=(), part=4)
        with self.voiceover("Chapter seven: when an equation can be solved for some of its variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def curve(self):
        d = load("implicit")
        fold = d["fold"]
        ax = square_axes([-1.6, 2.4, 1], [-1.6, 2.4, 1], 1.65, numbers=True, font_size=18,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.6, 0])
        g = np.linspace(-1.6, 2.4, 401)
        segs = contour_segments(fol, g, g, 0.0)
        curve = contour_mobject(ax, segs, C.FUNC, 3.5)
        img = heatmap(fol, (-1.6, 2.4), (-1.6, 2.4), 6.6, 6.6, -3, 3).move_to(ax.c2p(0.4, 0.4)).set_opacity(0.45)
        head = VGroup(MathTex(r"f(x, y) = x^3 + y^3 - 3xy = 0", font_size=36),
                      label(r"the folium of Descartes", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1)
        head.to_edge(UP, buff=0.25).shift(RIGHT * 2.6)

        def window(c, w, color):
            return Square(side_length=2 * w * 1.65, color=color, stroke_width=2.5).move_to(ax.c2p(*c))

        P = np.array([2 / 3, 4 / 3])  # t = 2 in (3t, 3t^2)/(1 + t^3)
        wP, wF, w0 = 0.3, 0.4, 0.3
        boxP, boxF, box0 = window(P, wP, C.CONNECTED_SET), window(fold, wF, C.PATHOLOGY), window((0, 0), w0, C.PATHOLOGY)
        # vertical-line tests, counted on the computed curve
        cP = [crossings(segs, P[0] + s, P[1] - wP, P[1] + wP) for s in np.linspace(-0.27, 0.27, 13)]
        cF = [crossings(segs, fold[0] + s, fold[1] - wF, fold[1] + wF) for s in (-0.1, -0.05, -0.02, 0.02, 0.1)]
        assert all(c_ == 1 for c_ in cP) and cF[:3] == [2, 2, 2] and cF[3:] == [0, 0]
        fx = lambda x, y: 3 * x * x - 3 * y  # noqa: E731
        fy = lambda x, y: 3 * y * y - 3 * x  # noqa: E731
        assert abs(fy(*fold)) < 1e-12 and fx(0, 0) == 0 == fy(0, 0) and abs(-fx(*P) / fy(*P) - 0.8) < 1e-12
        assert abs(fol(*P)) < 1e-12
        tang = Line(ax.c2p(P[0] - 0.3, P[1] - 0.24), ax.c2p(P[0] + 0.3, P[1] + 0.24), color=C.CONNECTED_SET,
                    stroke_width=3)
        sT = ValueTracker(-0.27)
        vline = always_redraw(lambda: Line(ax.c2p(P[0] + sT.get_value(), P[1] - wP),
                                           ax.c2p(P[0] + sT.get_value(), P[1] + wP), color=WHITE, stroke_width=2))
        fT = ValueTracker(-0.12)
        fline = always_redraw(lambda: Line(ax.c2p(fold[0] + fT.get_value(), fold[1] - wF),
                                           ax.c2p(fold[0] + fT.get_value(), fold[1] + wF), color=WHITE, stroke_width=2))
        side = VGroup(
            label(r"at $(\tfrac23, \tfrac43)$: \ $\partial f / \partial y = \tfrac{10}{3} \ne 0$", font_size=26,
                  color=C.CONNECTED_SET),
            label(r"each vertical line meets the curve once: \ $y = g(x)$", font_size=24),
            MathTex(r"g'(x) = -\frac{\partial f / \partial x}{\partial f / \partial y} = 0.8 \text{ there}", font_size=30),
            label(r"at the fold $(2^{2/3}, 2^{1/3})$: \ $\partial f / \partial y = 0$", font_size=26,
                  color=C.PATHOLOGY),
            label(r"vertical lines meet it twice, \ or not at all", font_size=24),
            label(r"at $(0, 0)$ both partials vanish: \ two branches cross", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -0.8, 0])
        for r_ in side:
            if r_.width > 6.2:
                r_.width = 6.2
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -0.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The equation x cubed plus y cubed equals three x y defines a curve, the folium of "
            "Descartes. Does it define y as a function of x? <bookmark mark='b'/> Not globally, but often locally. Near "
            "the point two thirds, four thirds, a small window contains a piece of the curve that every vertical "
            "line meets exactly once: there it's the graph of a function g. Its slope is minus the ratio of the two "
            "partial derivatives, here 0.8. <bookmark mark='c'/> At the fold, the curve turns back, and vertical "
            "lines meet it twice or not at all: there's no function of x there. That's exactly where the partial "
            "derivative in y vanishes. <bookmark mark='d'/> And at the origin both partials vanish, and two branches "
            "cross."
        ) as vo:
            self.play(FadeIn(img), Create(ax), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(curve), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(boxP), FadeIn(side[0]))
            self.add(vline)
            self.play(sT.animate.set_value(0.27), FadeIn(side[1]), run_time=2.0, rate_func=linear)
            self.remove(vline)
            self.play(Create(tang), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(boxF), FadeIn(side[3]))
            self.add(fline)
            self.play(fT.animate.set_value(0.12), FadeIn(side[4]), run_time=2.0, rate_func=linear)
            self.remove(fline)
            vo.wait_until("d")
            self.play(Create(box0), FadeIn(side[5]))
        for m in (vline, fline):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{Rudin 9.28} \ (two variables) \ $f$ is $\mathcal C^1$, \ $f(a, b) = 0$, \ "
                  r"$\partial f / \partial y\,(a, b) \ne 0$ $\Rightarrow$", font_size=28),
            label(r"near $a$ there is exactly one $\mathcal C^1$ function $g$ with $g(a) = b$ and $f(x, g(x)) = 0$",
                  font_size=28, color=C.EPS),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        rows = [
            MathTex(r"\Phi(x, y)", r"=", r"(x,\ f(x, y))", font_size=34),
            MathTex(r"\Phi'(x, y)", r"=", r"\begin{pmatrix} 1 & 0 \\ f_x & f_y \end{pmatrix}", font_size=34),
            MathTex(r"\det \Phi'(a, b)", r"=", r"f_y(a, b) \ne 0", font_size=34),
            MathTex(r"g(x)", r"=", r"\text{second coordinate of } \Phi^{-1}(x, 0)", font_size=34),
        ]
        whys = [why(r"the trick: \ keep $x$, \ record the value of $f$"), why(r"a triangular matrix"),
                why(r"so 9.24 inverts $\Phi$ near $(a, b)$"), why(r"$f(x, g(x)) = 0$: \ the level set is a graph")]
        step = ladder(self, rows, whys, keep=4, top=1.6, buff=0.4, x=-1.6)
        out = label(r"differentiate $f(x, g(x)) = 0$: \ $f_x + f_y\, g' = 0$, \ so $g' = -f_x / f_y$", font_size=26,
                    color=C.EPS).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem, Rudin 9.28, here with one variable on each side: if f vanishes at a, "
            "b, and its partial derivative in y is not zero there, then near a the equation defines y as exactly one "
            "continuously differentiable function of x. <bookmark mark='b'/> It comes straight from the inverse "
            "function theorem. Build a map of the plane that keeps x and records the value of f. "
            "<bookmark mark='c'/> Its derivative is a triangular matrix <bookmark mark='d'/> whose determinant is the "
            "partial derivative in y, so the inverse function theorem inverts it near a, b. <bookmark mark='e'/> The "
            "points where f is zero are the points that map to the x-axis, so the inverse, applied to the x-axis, "
            "traces the graph. <bookmark mark='f'/> Differentiating the identity f of x, g of x equals zero gives the "
            "slope."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
            vo.wait_until("f")
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rank(self):
        ax = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.4).move_to([-3.6, -0.6, 0])
        ax.set_opacity(0.5)
        bx = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.4).move_to([3.4, -0.6, 0])
        bx.set_opacity(0.5)
        t = np.linspace(-1.4, 1.4, 15)
        # a rank-one map: F(x, y) = (x + y^2 ... ) ; level sets are curves, image a curve
        F = lambda x, y: np.stack([np.tanh(x + 0.4 * y), 0.6 * np.sinh(x + 0.4 * y)], -1)  # noqa: E731
        lvl = VGroup()
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / 8) for k in range(9)]
        for k, c in enumerate(np.linspace(-1.2, 1.2, 9)):
            yy = np.linspace(-1.5, 1.5, 50)
            xx = c - 0.4 * yy
            ok = np.abs(xx) <= 1.5
            lvl.add(VMobject(color=cols[k], stroke_width=3).set_points_as_corners(
                [ax.c2p(a, b) for a, b in zip(xx[ok], yy[ok])]))
        s = np.linspace(-1.2, 1.2, 200)
        imgc = VMobject(color=C.OPERATOR, stroke_width=4).set_points_as_corners(
            [bx.c2p(*F(v, 0.0)) for v in s])
        dots = VGroup(*[Dot(bx.c2p(*F(c, 0.0)), radius=0.07, color=cols[k]) for k, c in
                        enumerate(np.linspace(-1.2, 1.2, 9))])
        for c in np.linspace(-1.2, 1.2, 9):  # each level line maps to a single point
            yy = np.linspace(-1, 1, 7)
            assert np.allclose(F(c - 0.4 * yy, yy), F(c, 0.0))
        arrow = Arrow([-1.0, -0.6, 0], [0.8, -0.6, 0], buff=0, color=GREY_B, stroke_width=4)
        head = VGroup(label(r"\textbf{Rudin 9.32} \ the rank theorem, \ in one picture", font_size=30),
                      label(r"if $F'$ has constant rank $r$, \ then near each point, in suitable coordinates, \ "
                            r"$F$ is a projection onto $r$ coordinates", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        note_ = label(r"rank $1$: \ each colored line collapses to a point, \ the plane folds onto a curve",
                      font_size=24, color=C.OPERATOR).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The same circle of ideas gives Rudin's rank theorem, which we'll only picture. If "
            "the derivative of a map has the same rank everywhere, then in suitable coordinates the map is just a "
            "projection. <bookmark mark='b'/> Here the rank is one: a whole family of lines in the plane, each "
            "collapsed to a single point, and the plane folded onto a curve."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(Create(ax), Create(lvl), run_time=1.5)
            self.play(GrowArrow(arrow), Create(bx))
            self.play(Create(imgc), LaggedStart(*[TransformFromCopy(l_, d_) for l_, d_ in zip(lvl, dots)],
                                                lag_ratio=0.15), run_time=2.5)
            self.play(FadeIn(note_))
        del t
        self.wait(0.4)
        self.clear_scene()
