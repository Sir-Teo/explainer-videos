from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis4.common import heatmap, load, plain_axes, polyline, square_axes


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
        U_ = 1.38  # scene units per unit
        head = VGroup(label(r"The folium of Descartes: \ where is it a graph $y = g(x)$?", font_size=34),
                      MathTex(r"f(x, y) = x^3 + y^3 - 3xy = 0", r"\qquad \text{orange: } f > 0, \ \text{blue: } f < 0",
                              font_size=30)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_A)
        ax = square_axes([-1.6, 2.4, 1], [-1.6, 2.4, 1], U_, numbers=True, font_size=18,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 0}})
        ax.move_to([-6.55 + 2.0 * U_, 0, 0]).align_to([0, head.get_bottom()[1] - 0.25, 0], UP)
        g = np.linspace(-1.6, 2.4, 401)
        segs = contour_segments(fol, g, g, 0.0)
        curve = contour_mobject(ax, segs, C.FUNC, 3.5)
        img = heatmap(fol, (-1.6, 2.4), (-1.6, 2.4), 4 * U_, 4 * U_, -3, 3).move_to(ax.c2p(0.4, 0.4)).set_opacity(0.45)
        assert img.get_bottom()[1] > -3.65 and img.get_left()[0] > -6.6

        def window(c, w, color):
            return Square(side_length=2 * w * U_, color=color, stroke_width=2.5).move_to(ax.c2p(*c))

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
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r_ in side:
            if r_.width > 5.9:
                r_.width = 5.9
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to([ax.get_right()[0] + 0.4, -0.6, 0], RIGHT, buff=0)
        assert side.get_right()[0] <= 6.6 and side.get_top()[1] < head.get_bottom()[1] - 0.1
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
            label(r"The implicit function theorem", font_size=34),
            VGroup(label(r"$f$ is $\mathcal C^1$, \ $f(a, b) = 0$, \ $\partial f / \partial y\,(a, b) \ne 0$ "
                         r"$\Rightarrow$", font_size=28),
                   label(r"(Rudin 9.28, two variables)", font_size=22, color=GREY_B)).arrange(RIGHT, buff=0.3,
                                                                                         aligned_edge=DOWN),
            label(r"near $a$ there is exactly one $\mathcal C^1$ function $g$ with $g(a) = b$ and $f(x, g(x)) = 0$",
                  font_size=28, color=C.EPS),
        ).arrange(DOWN, buff=0.14).to_edge(UP, buff=0.3)
        # the picture: a window around (a, b) = (2/3, 4/3) on the folium, and its image under Phi(x, y) = (x, f(x, y))
        a, b, h = 2 / 3, 4 / 3, 0.3
        xr, yr = (a - h, a + h), (b - h, b + h)
        fy = lambda x, y: 3 * y * y - 3 * x  # noqa: E731
        fx = lambda x, y: 3 * x * x - 3 * y  # noqa: E731
        Xg, Yg = np.meshgrid(np.linspace(*xr, 121), np.linspace(*yr, 121))
        vals = fol(Xg, Yg)
        assert np.all(fy(Xg, Yg) > 0.25)  # f_y > 0 on the window: f increases up each vertical, Phi is one-to-one
        vlo, vhi = math.floor(vals.min() * 2) / 2, math.ceil(vals.max() * 2) / 2
        A = square_axes([xr[0], xr[1], 0.3], [yr[0], yr[1], 0.3], 2.7 / (2 * h)).move_to([-5.15, -0.65, 0])
        B = plain_axes([xr[0], xr[1], 0.3], [vlo, vhi, 1.0], 2.7, 2.7).move_to([-1.7, -0.65, 0])
        z0 = DashedLine(B.c2p(xr[0], 0), B.c2p(xr[1], 0), color=GREY_B, stroke_width=1.5)
        img = heatmap(fol, xr, yr, 2.7, 2.7, -1.5, 1.5, px=240).move_to(A.c2p(a, b)).set_opacity(0.45)
        levels = [-0.8, -0.4, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
        xs_ = np.linspace(*xr, 161)
        ys_ = np.linspace(*yr, 161)

        def level(c_, n=121):
            """{f = c} in the window as a graph over x: f increases up each vertical, so bisect in y."""
            xs, ys = [], []
            for x in np.linspace(*xr, n):
                lo, hi = yr
                if not fol(x, lo) <= c_ <= fol(x, hi):
                    continue
                for _ in range(60):
                    mid = (lo + hi) / 2
                    lo, hi = (mid, hi) if fol(x, mid) < c_ else (lo, mid)
                xs.append(x)
                ys.append((lo + hi) / 2)
            xs, ys = np.array(xs), np.array(ys)
            assert len(xs) > 5 and np.abs(fol(xs, ys) - c_).max() < 1e-9
            return xs, ys

        lv_src, lv_img = VGroup(), VGroup()
        for c_ in levels:  # the other level sets in grey (dashed where f < 0); blue is for f = 0 only
            lx, ly = level(c_)
            src_ = polyline(A, lx, ly, color=GREY_B, stroke_width=1.8)
            img_ = polyline(B, lx, fol(lx, ly), color=GREY_B, stroke_width=1.8)  # = the line v = c
            if c_ < 0:
                src_, img_ = DashedVMobject(src_, num_dashes=14), DashedVMobject(img_, num_dashes=14)
            lv_src.add(src_)
            lv_img.add(img_)
        lx, ly = level(0.0)
        cur_src = polyline(A, lx, ly, color=C.FUNC, stroke_width=4)
        cur_img = polyline(B, lx, fol(lx, ly), color=C.FUNC, stroke_width=4)
        vert_src, vert_img = VGroup(), VGroup()
        t_ = np.linspace(*yr, 60)
        for xc in np.linspace(xr[0] + 0.1, xr[1] - 0.1, 5):
            vert_src.add(polyline(A, np.full_like(t_, xc), t_, color=GREY_B, stroke_width=1.4))
            vert_img.add(polyline(B, np.full_like(t_, xc), fol(np.full_like(t_, xc), t_), color=GREY_B, stroke_width=1.4))
        # g by Newton on f(x, .) = 0 from b: the inverse of Phi along v = 0
        gx = np.linspace(xr[0] + 0.03, xr[1] - 0.03, 41)

        def g_of(x):
            y = b
            for _ in range(30):
                y -= fol(x, y) / fy(x, y)
            return y

        gy = np.array([g_of(x) for x in gx])
        assert np.abs(fol(gx, gy)).max() < 1e-12
        slope = (g_of(a + 1e-6) - g_of(a - 1e-6)) / 2e-6
        assert abs(slope - 0.8) < 1e-6 and abs(-fx(a, b) / fy(a, b) - 0.8) < 1e-12
        tT = ValueTracker(0.0)
        pa = always_redraw(lambda: Dot(A.c2p(gx[int(tT.get_value() * 40)], gy[int(tT.get_value() * 40)]), radius=0.08,
                                       color=C.EPS))
        pb = always_redraw(lambda: Dot(B.c2p(gx[int(tT.get_value() * 40)], 0), radius=0.08, color=C.EPS))
        P_ = Dot(A.c2p(a, b), radius=0.07, color=WHITE)
        tan_ = Line(A.c2p(a - 0.22, b - 0.8 * 0.22), A.c2p(a + 0.22, b + 0.8 * 0.22), color=C.EPS, stroke_width=3)
        arr = Arrow(A.get_right() + RIGHT * 0.05, B.get_left() + LEFT * 0.05, buff=0.05, color=WHITE, stroke_width=3,
                    max_tip_length_to_length_ratio=0.25)
        arr_l = MathTex(r"\Phi", font_size=30).next_to(arr, UP, buff=0.05)
        A_l = MathTex(r"(x, y) \text{ near } (\tfrac23, \tfrac43)", font_size=22, color=GREY_A).next_to(A, UP, buff=0.12)
        B_l = MathTex(r"(x,\ v = f(x, y))", font_size=22, color=GREY_A).next_to(B, UP, buff=0.12)
        B_0 = MathTex(r"v = 0", font_size=22, color=C.FUNC).next_to(B.c2p(xr[1], 0), RIGHT, buff=0.08)
        A_n = VGroup(label(r"level sets of $f$", font_size=22, color=GREY_A),
                     label(r"(dashed, on blue: \ $f < 0$)", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(
            A, DOWN, buff=0.15)
        B_n = label(r"become horizontal lines", font_size=22, color=GREY_A).next_to(B, DOWN, buff=0.15)
        rows = [
            MathTex(r"\Phi(x, y)", r"=", r"(x,\ f(x, y))", font_size=32),
            MathTex(r"\Phi'(x, y)", r"=", r"\begin{pmatrix} 1 & 0 \\ f_x & f_y \end{pmatrix}", font_size=32),
            MathTex(r"\det \Phi'(a, b)", r"=", r"f_y(a, b) = \tfrac{10}{3} \ne 0", font_size=32),
            MathTex(r"g(x)", r"=", r"\text{second coordinate of } \Phi^{-1}(x, 0)", font_size=32),
        ]
        whys = [why(r"the trick: \ keep $x$, \ record the value of $f$", 22), why(r"a triangular matrix", 22),
                why(r"so 9.24 inverts $\Phi$ near $(a, b)$", 22), why(r"$f(x, g(x)) = 0$: \ the level set is a graph", 22)]
        step = ladder(self, rows, whys, keep=3, top=thm.get_bottom()[1] - 0.35, buff=0.3, x=2.0)
        out = VGroup(label(r"differentiate $f(x, g(x)) = 0$: \ $f_x + f_y\, g' = 0$,", font_size=26, color=C.EPS),
                     label(rf"so $g' = -f_x / f_y = {-fx(a, b) / fy(a, b):.1f}$ at $a$", font_size=26, color=C.EPS)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.35)
        out.shift(RIGHT * (0.3 - out.get_left()[0]))
        assert out.get_right()[0] <= 6.6 and A_n.get_bottom()[1] > -3.6 and A_l.get_top()[1] < thm.get_bottom()[1] - 0.1
        with self.voiceover(
            "<bookmark mark='a'/> The theorem, Rudin 9.28, here with one variable on each side: if f vanishes at a, "
            "b, and its partial derivative in y is not zero there, then near a the equation defines y as exactly one "
            "continuously differentiable function of x. <bookmark mark='b'/> It comes straight from the inverse "
            "function theorem. Build a map of the plane that keeps x and records the value of f. Near the point, "
            "it straightens the level sets of f into horizontal lines. <bookmark mark='c'/> Its derivative is a "
            "triangular matrix: vertical lines stay vertical, <bookmark mark='d'/> and its determinant is the "
            "partial derivative in y, so the inverse function theorem inverts it near a, b. <bookmark mark='e'/> The "
            "points where f is zero are the points that map to the x-axis, so the inverse, applied to the x-axis, "
            "traces the graph. <bookmark mark='f'/> Differentiating the identity f of x, g of x equals zero gives the "
            "slope: zero point eight here, the tangent we met on the folium."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            self.play(Create(A), FadeIn(img), FadeIn(A_l), Create(lv_src), Create(cur_src), FadeIn(P_), run_time=1.5)
            vo.wait_until("b")
            step(0)
            self.play(GrowArrow(arr), FadeIn(arr_l), Create(B), Create(z0), FadeIn(B_l))
            self.play(TransformFromCopy(lv_src, lv_img), TransformFromCopy(cur_src, cur_img), FadeIn(A_n), FadeIn(B_n), FadeIn(B_0),
                      run_time=2.5)
            vo.wait_until("c")
            step(1)
            self.play(Create(vert_src), run_time=0.8)
            self.play(TransformFromCopy(vert_src, vert_img), run_time=1.5)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
            self.add(pa, pb)
            self.play(tT.animate.set_value(1.0), run_time=2.0)
            self.play(tT.animate.set_value(0.5), run_time=1.2)
            vo.wait_until("f")
            self.play(Create(tan_), FadeIn(out))
        for m_ in (pa, pb):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rank(self):
        head = VGroup(label(r"The rank theorem, \ in one picture", font_size=34),
                      label(r"$F'$ of constant rank $r$ $\Rightarrow$ near each point, in suitable coordinates, \ "
                            r"$F$ is a projection onto $r$ coordinates \ (Rudin 9.32)", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        ax = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.4).move_to([-3.6, -0.35, 0])
        ax.set_opacity(0.5)
        bx = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.4).move_to([3.4, -0.35, 0])
        bx.set_opacity(0.5)
        # a rank-one map: F depends on u = x + 0.4 y only, so each line u = c goes to one point
        F = lambda x, y: np.stack([np.tanh(x + 0.4 * y), 0.6 * np.sinh(x + 0.4 * y)], -1)  # noqa: E731
        cs = np.linspace(-0.9, 0.9, 9)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / 8) for k in range(9)]
        yy = np.linspace(-1.5, 1.5, 50)
        assert np.all(np.abs(cs[:, None] - 0.4 * yy[None, :]) <= 1.5)  # every line drawn at full length
        lvl = VGroup(*[VMobject(color=cols[k], stroke_width=3).set_points_as_corners(
            [ax.c2p(c - 0.4 * y_, y_) for y_ in yy]) for k, c in enumerate(cs)])
        s = np.linspace(cs[0], cs[-1], 200)
        imgc = VMobject(color=C.OPERATOR, stroke_width=4).set_points_as_corners([bx.c2p(*F(v, 0.0)) for v in s])
        dots = VGroup(*[Dot(bx.c2p(*F(c, 0.0)), radius=0.07, color=cols[k]) for k, c in enumerate(cs)])
        for c in cs:  # each level line maps to a single point
            y7 = np.linspace(-1, 1, 7)
            assert np.allclose(F(c - 0.4 * y7, y7), F(c, 0.0))
        assert np.abs(F(s, 0 * s)).max() < 1.6
        arrow = Arrow([ax.get_right()[0] + 0.15, -0.35, 0], [bx.get_left()[0] - 0.15, -0.35, 0], buff=0, color=GREY_B,
                      stroke_width=4)
        note_ = label(r"rank $1$: \ each colored line collapses to a point, \ the plane folds onto a curve",
                      font_size=24, color=C.OPERATOR).to_edge(DOWN, buff=0.35)
        # the model first: in the right coordinates a rank-one map is the projection (x, y) -> (x, 0)
        mlines = VGroup(*[Line(ax.c2p(c, -1.5), ax.c2p(c, 1.5), color=cols[k], stroke_width=3) for k, c in enumerate(cs)])
        mseg = Line(bx.c2p(cs[0], 0), bx.c2p(cs[-1], 0), color=C.OPERATOR, stroke_width=4)
        mdots = VGroup(*[Dot(bx.c2p(c, 0), radius=0.07, color=cols[k]) for k, c in enumerate(cs)])
        ml = MathTex(r"(x, y) \mapsto (x, 0)", font_size=26).next_to(arrow, UP, buff=0.15)
        fl = MathTex(r"F = (\tanh u,\ 0.6 \sinh u), \quad u = x + 0.4\,y", font_size=24).next_to(bx, DOWN, buff=0.15)
        assert ml.width < arrow.get_length() + 0.6 and fl.get_right()[0] <= 6.6
        alab = label(r"lines in the plane", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.1)
        mlab = label(r"the model: \ a projection", font_size=24, color=GREY_A).next_to(bx, UP, buff=0.1)
        flab = label(r"a rank-one map, \ before straightening", font_size=24, color=GREY_A).next_to(bx, UP, buff=0.1)
        assert alab.get_top()[1] < head.get_bottom()[1] - 0.1 and note_.get_top()[1] < fl.get_bottom()[1] - 0.1
        with self.voiceover(
            "<bookmark mark='a'/> The same circle of ideas gives Rudin's rank theorem, which we'll only picture. If "
            "the derivative of a map has the same rank everywhere, then <bookmark mark='p'/> in suitable coordinates "
            "the map is just a projection, which flattens each vertical line to a point. <bookmark mark='b'/> Here "
            "is a rank-one map before the coordinates are straightened. The rank is one: a whole family of lines in the plane, each "
            "collapsed to a single point, and the plane folded onto a curve."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(ax), Create(mlines), FadeIn(alab), run_time=1.5)
            vo.wait_until("p")
            self.play(GrowArrow(arrow), Create(bx), FadeIn(ml), FadeIn(mlab))
            self.play(Create(mseg), LaggedStart(*[TransformFromCopy(l_, d_) for l_, d_ in zip(mlines, mdots)],
                                                lag_ratio=0.12), run_time=2.0)
            vo.wait_until("b")
            self.play(ReplacementTransform(mlines, lvl), ReplacementTransform(mseg, imgc),
                      ReplacementTransform(mdots, dots), FadeTransform(ml, fl), FadeTransform(mlab, flab), run_time=2.0)
            self.play(LaggedStart(*[Indicate(l_, color=l_.get_color(), scale_factor=1.0) for l_ in lvl], lag_ratio=0.1),
                      LaggedStart(*[Flash(d_, color=d_.get_color(), line_length=0.12, flash_radius=0.15) for d_ in dots],
                                  lag_ratio=0.1), run_time=2.0)
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
