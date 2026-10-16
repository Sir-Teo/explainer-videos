from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis2.common import load, plain_axes, polyline
from videos.analysis.analysis2.compute import rough


def zoom_view(f, x0, center, S, w, rescale, color, stroke_width=3) -> VMobject:
    """The graph of f near x0 in a square of side S at ``center``, showing [x0 - w, x0 + w]: at the same scale both
    ways, or (``rescale``) stretched vertically to fill the square."""
    x = np.linspace(x0 - w, x0 + w, 700)
    y = f(x)
    if rescale:
        lo, hi = y.min(), y.max()
        mid, half = (lo + hi) / 2, max((hi - lo) / 2, 1e-12) * 1.15
    else:
        mid, half = f(np.array([x0]))[0], w
    X = center[0] + (x - x0) / w * S / 2
    Y = center[1] + np.clip((y - mid) / half, -1, 1) * S / 2
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners(np.c_[X, Y, np.zeros_like(X)])
    return m


class Derivative(VoiceoverScene):
    def construct(self):
        self.card()
        self.secants()
        self.zooms()
        self.linear()
        self.chain()
        self.wiggle()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"The derivative", r"What does a curve look like under a microscope?", lit=(1821,),
                            part=2)
        with self.voiceover(
            "Chapter twelve: the derivative, defined as a limit, the way Cauchy did in the 1820s, and looked at "
            "under a microscope."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def secants(self):
        ax = plain_axes([0, 4, 1], [0, 3, 1], 7.6, 4.8, numbers=False).move_to([-2.2, -0.7, 0])
        f = lambda x: 0.25 * x**2 - 0.15 * x**3 / 3 + 0.6 * np.sin(x) + 0.4  # noqa: E731
        fp = lambda x: 0.5 * x - 0.15 * x**2 + 0.6 * np.cos(x)  # noqa: E731
        g = ax.plot(f, x_range=[0, 4, 0.01], color=C.FUNC, stroke_width=4)
        x0 = 1.4
        tT = ValueTracker(3.6)

        def secant():
            t = tT.get_value()
            m = (f(t) - f(x0)) / (t - x0)
            return Line(ax.c2p(x0 - 1.2, f(x0) - 1.2 * m), ax.c2p(x0 + 2.6, f(x0) + 2.6 * m), color=C.APPROX,
                        stroke_width=3)

        sec = always_redraw(secant)
        p = Dot(ax.c2p(x0, f(x0)), radius=0.07, color=WHITE)
        q = always_redraw(lambda: Dot(ax.c2p(tT.get_value(), f(tT.get_value())), radius=0.07, color=C.APPROX))
        tan = Line(ax.c2p(x0 - 1.2, f(x0) - 1.2 * fp(x0)), ax.c2p(x0 + 2.6, f(x0) + 2.6 * fp(x0)), color=C.EPS,
                   stroke_width=3)
        dfn = VGroup(label(r"\textbf{Rudin 5.1}", font_size=30),
                     MathTex(r"f'(x) = \lim_{t \to x} \frac{f(t) - f(x)}{t - x}", font_size=38)).arrange(DOWN, buff=0.2)
        dfn.move_to([3.9, 1.6, 0])
        def cur_slope():
            return (f(tT.get_value()) - f(x0)) / (tT.get_value() - x0)

        s_lab = MathTex(r"\text{secant slope} =", font_size=32, color=C.APPROX)
        s_val = DecimalNumber(cur_slope(), num_decimal_places=3, font_size=32, color=C.APPROX)
        slope = VGroup(s_lab, s_val).arrange(RIGHT, buff=0.15).move_to([3.9, 0.1, 0])
        s_val.add_updater(lambda m: m.set_value(cur_slope()).next_to(s_lab, RIGHT, buff=0.15))
        # x fixed, t sliding, marked on the horizontal axis (t's label fades as it reaches x)
        xmark = VGroup(Line(ax.c2p(x0, 0) + DOWN * 0.08, ax.c2p(x0, 0) + UP * 0.08, color=WHITE),
                       MathTex(r"x", font_size=28).next_to(ax.c2p(x0, 0), DOWN, buff=0.15))
        tmark = VGroup(Line(DOWN * 0.08, UP * 0.08, color=C.APPROX), MathTex(r"t", font_size=28, color=C.APPROX))
        tmark[1].next_to(tmark[0], DOWN, buff=0.15)

        def move_t(m):
            t = tT.get_value()
            m.shift(ax.c2p(t, 0) - m[0].get_center())
            m.set_opacity(float(np.clip((t - x0 - 0.1) / 0.35, 0, 1)))

        tmark.add_updater(move_t)
        move_t(tmark)
        lim = MathTex(rf"f'(x) = {fp(x0):.3f}", font_size=32, color=C.EPS).next_to(slope, DOWN, buff=0.3).align_to(slope,
                                                                                                          LEFT)
        assert abs((f(x0 + 0.02) - f(x0)) / 0.02 - fp(x0)) < 0.01
        with self.voiceover(
            "<bookmark mark='a'/> The derivative of f at x is the limit of the difference quotient: the slope of the "
            "line through the point at x and a second point at t, <bookmark mark='b'/> as t slides toward x. "
            "<bookmark mark='c'/> The secants settle on a limiting slope, the tangent's."
        ) as vo:
            self.play(Create(ax), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(dfn), FadeIn(p), FadeIn(q), Create(sec), FadeIn(slope), FadeIn(xmark), FadeIn(tmark))
            vo.wait_until("b")
            self.play(tT.animate.set_value(x0 + 0.02), run_time=3.5, rate_func=smooth)
            vo.wait_until("c")
            self.play(Create(tan), FadeIn(lim))
        for m in (sec, q, s_val, tmark):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def zooms(self):
        lw = ValueTracker(0.0)  # log10 of the half-width of the view
        S = 3.4  # box side on screen
        x0s = (0.9, 0.0, 0.3)
        smooth_f = lambda x: 0.6 * np.sin(2 * x) + 0.2 * x * x  # noqa: E731
        fs = (smooth_f, np.abs, lambda x: rough(x) * 0.5)
        titles = (r"a smooth function", r"$|x|$ at $0$", r"Rudin 7.18 \ (rescaled vertically)")
        cols = (C.CONNECTED_SET, C.CUT_HIGH, C.PATHOLOGY)
        centers = (np.array([-4.5, -0.6, 0]), np.array([0.0, -0.6, 0]), np.array([4.5, -0.6, 0]))

        def view(i):
            return always_redraw(lambda: zoom_view(fs[i], x0s[i], centers[i], S, 10 ** lw.get_value(), i == 2, cols[i]))

        boxes = VGroup(*[Square(side_length=S, color=GREY_C, stroke_width=2).move_to(c) for c in centers])
        tl = VGroup(*[label(t, font_size=24, color=c).next_to(b, UP, buff=0.15) for t, c, b in zip(titles, cols, boxes)])
        views = [view(i) for i in range(3)]
        w_lab = MathTex(r"\text{magnification} \times", font_size=30, color=GREY_B)
        w_val = Integer(1, font_size=30, color=GREY_B)
        wl = VGroup(w_lab, w_val).arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.5)
        w_val.add_updater(lambda m: m.set_value(int(round(10 ** -lw.get_value()))).next_to(w_lab, RIGHT, buff=0.12))
        head = label(r"Zoom in, and a differentiable function looks straight", font_size=34).to_edge(UP, buff=0.3)
        verdicts = VGroup(label(r"a line: \ slope $f'(x)$", font_size=24, color=C.CONNECTED_SET),
                          label(r"a corner at every scale", font_size=24, color=C.CUT_HIGH),
                          label(r"rough at every scale: \ no slope anywhere", font_size=24, color=C.PATHOLOGY))
        for v, b in zip(verdicts, boxes):
            v.next_to(b, DOWN, buff=0.2)
            v.shift(LEFT * max(0.0, v.get_right()[0] - 6.55))  # inside the right margin
        with self.voiceover(
            "<bookmark mark='a'/> Here's what the definition means geometrically. Put three graphs under a microscope "
            "and zoom in, a thousandfold. <bookmark mark='b'/> A differentiable function straightens out into a line, "
            "whose slope is the derivative. The absolute value at zero stays a corner at every scale. "
            "<bookmark mark='c'/> And the third is a function Rudin builds in chapter seven: continuous everywhere, "
            "but every zoom shows new wrinkles. It has a derivative nowhere."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(boxes), FadeIn(tl), *[FadeIn(v) for v in views], FadeIn(wl))
            vo.wait_until("b")
            self.play(lw.animate.set_value(-3.0), run_time=6.0, rate_func=smooth)
            self.play(LaggedStart(*[FadeIn(v) for v in verdicts[:2]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(verdicts[2]))
        d = load("wiggle")
        assert np.all(np.abs(d["rough_quot"]) >= (3.0 ** np.arange(1, 9) + 1) / 2 - 1e-6)
        assert w_val.get_value() == 1000
        for m in (*views, w_val):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def linear(self):
        rows = VGroup(
            label(r"Equivalently: \ the best linear approximation", font_size=32),
            MathTex(r"f(x + h) = f(x) + f'(x)\, h + r(h), \qquad \frac{r(h)}{h} \to 0", font_size=38),
            label(r"the form that generalizes: \ in $\R^n$ the derivative is a linear map (Rudin 9.11, Part 4)",
                  font_size=26, color=GREY_A),
            label(r"\textbf{Rudin 5.2} \ differentiable $\Rightarrow$ continuous:", font_size=30),
            MathTex(r"f(t) - f(x) = \frac{f(t) - f(x)}{t - x}\,(t - x) \to f'(x) \cdot 0 = 0", font_size=36),
            label(r"the converse fails: $|x|$, \ and Rudin's function, continuous everywhere, differentiable nowhere",
                  font_size=26, color=C.PATHOLOGY),
        )
        rows[0].to_edge(UP, buff=0.3)
        rows[1].next_to(rows[0], DOWN, buff=0.25)
        rows[2].to_edge(DOWN, buff=0.35)
        # Rudin 5.2 in the right column, its one line split in two
        r4 = VGroup(MathTex(r"f(t) - f(x) = \frac{f(t) - f(x)}{t - x}\,(t - x)", font_size=32),
                    MathTex(r"\to f'(x) \cdot 0 = 0", font_size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows.submobjects[4] = r4
        VGroup(rows[3], rows[4]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.55, 0.3, 0])
        rows[5].to_edge(DOWN, buff=0.4)
        # the converse fails: |x| at 0 and Rudin's nowhere-differentiable function, both still unstraightened at x1000
        zS, zc = 2.5, (np.array([-4.7, -0.95, 0]), np.array([-1.6, -0.95, 0]))
        zb = VGroup(*[Square(side_length=zS, color=GREY_C, stroke_width=2).move_to(c) for c in zc])
        zc_curves = VGroup(zoom_view(np.abs, 0.0, zc[0], zS, 1e-3, False, C.CUT_HIGH),
                           zoom_view(lambda x: rough(x) * 0.5, 0.3, zc[1], zS, 1e-3, True, C.PATHOLOGY))
        zt = VGroup(label(r"$|x|$ at $0$", font_size=24, color=C.CUT_HIGH).next_to(zb[0], UP, buff=0.12),
                    label(r"Rudin 7.18", font_size=24, color=C.PATHOLOGY).next_to(zb[1], UP, buff=0.12),
                    label(r"both at $\times 1000$: \ continuous, not straight", font_size=24, color=GREY_A).next_to(
                        zb, DOWN, buff=0.15))
        zpic = VGroup(zb, zc_curves, zt)
        # the picture: tangent line at x, and the error r(h) between it and the curve, as h shrinks (a convex
        # curve, so the error sits on top of the tangent's rise instead of overlapping it)
        f = lambda x: 0.35 + 0.12 * x**2 + 0.03 * x**3  # noqa: E731
        fp = lambda x: 0.24 * x + 0.09 * x**2  # noqa: E731
        x0 = 1.0
        ax = plain_axes([0, 3.4, 1], [0, 2.6, 1], 6.4, 3.9, numbers=False).move_to([-3.2, -0.75, 0])
        g = ax.plot(f, x_range=[0, 3.2, 0.01], color=C.FUNC, stroke_width=4)
        tan = Line(ax.c2p(0.2, f(x0) - 0.8 * fp(x0)), ax.c2p(3.4, f(x0) + 2.4 * fp(x0)), color=C.EPS, stroke_width=2.5)
        P = Dot(ax.c2p(x0, f(x0)), radius=0.07, color=WHITE)
        hT = ValueTracker(1.6)

        def pieces():
            h = hT.get_value()
            x1, y0, yt, yc = x0 + h, f(x0), f(x0) + fp(x0) * h, f(x0 + h)
            return VGroup(Line(ax.c2p(x0, y0), ax.c2p(x1, y0), color=GREY_B, stroke_width=2.5),
                          Line(ax.c2p(x1, y0), ax.c2p(x1, yt), color=C.EPS, stroke_width=5),
                          Line(ax.c2p(x1, yt), ax.c2p(x1, yc), color=C.PATHOLOGY, stroke_width=6),
                          Dot(ax.c2p(x1, yc), radius=0.06, color=C.FUNC))

        pc = always_redraw(pieces)
        h0 = 1.6
        tags = VGroup(MathTex(r"h", font_size=28, color=GREY_B).next_to(ax.c2p(x0 + h0 / 2, f(x0)), DOWN, buff=0.1),
                      MathTex(r"f'(x)\,h", font_size=28, color=C.EPS).next_to(
                          ax.c2p(x0 + h0, f(x0) + fp(x0) * h0 / 2), RIGHT, buff=0.12),
                      MathTex(r"r(h)", font_size=28, color=C.PATHOLOGY).next_to(
                          ax.c2p(x0 + h0, (f(x0) + fp(x0) * h0 + f(x0 + h0)) / 2), RIGHT, buff=0.12),
                      MathTex(r"x", font_size=28).next_to(ax.c2p(x0, 0), DOWN, buff=0.12))
        r_over_h = lambda h: (f(x0 + h) - f(x0) - fp(x0) * h) / h  # noqa: E731
        bx = plain_axes([0, 1.7, 0.5], [0, 0.5, 0.25], 4.6, 2.6, numbers=False).move_to([3.9, -0.5, 0])
        hs = np.linspace(1e-3, 1.6, 400)
        trace = always_redraw(lambda: polyline(bx, hs[hs >= hT.get_value()], r_over_h(hs[hs >= hT.get_value()]),
                                               color=C.PATHOLOGY, stroke_width=3)
                              if hT.get_value() < 1.6 - 1e-3 else VMobject())
        bdot = always_redraw(lambda: Dot(bx.c2p(hT.get_value(), r_over_h(hT.get_value())), radius=0.07,
                                         color=C.PATHOLOGY))
        blab = VGroup(MathTex(r"\frac{r(h)}{h}", font_size=30, color=C.PATHOLOGY).next_to(bx, LEFT, buff=0.15),
                      MathTex(r"h", font_size=26, color=GREY_B).next_to(bx.c2p(1.7, 0), DOWN, buff=0.12),
                      MathTex(r"0", font_size=24, color=GREY_B).next_to(bx.c2p(0, 0), UL, buff=0.06))
        assert r_over_h(1.6) > 0.35 and 0 < r_over_h(0.02) < 0.01
        pic = VGroup(ax, g, tan, P, tags, bx, blab)
        with self.voiceover(
            "<bookmark mark='a'/> Straightening has an algebraic form: f of x plus h is f of x, plus the derivative "
            "times h, plus an error that's small even compared with h. <bookmark mark='b'/> That's the version that "
            "survives in many dimensions, where the derivative becomes a linear map. <bookmark mark='c'/> One "
            "consequence: differentiable functions are continuous, since the difference f of t minus f of x is the "
            "difference quotient times t minus x, which goes to zero. <bookmark mark='d'/> The converse fails, "
            "spectacularly."
        ) as vo:
            self.play(FadeIn(rows[0]), Create(ax), Create(g), FadeIn(tags[3]))
            vo.wait_until("a")
            self.play(Write(rows[1]), FadeIn(P), Create(tan))
            self.play(FadeIn(pc), FadeIn(tags[:3]))
            self.play(Create(bx), FadeIn(blab), FadeIn(bdot))
            self.play(FadeOut(tags[:3]), run_time=0.4)
            self.add(trace)
            self.play(hT.animate.set_value(0.02), run_time=4.0, rate_func=smooth)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            for m in (pc, trace, bdot):
                m.clear_updaters()
            # the tangent picture stays (near x the curve hugs the line, so f(t) -> f(x)); the r(h)/h plot goes
            self.play(FadeOut(VGroup(bx, blab, trace, bdot, rows[2])), run_time=0.6)
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeOut(VGroup(ax, g, tan, P, pc, tags[3])), run_time=0.5)
            self.play(FadeIn(zb), Create(zc_curves), FadeIn(zt), FadeIn(rows[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chain(self):
        head = VGroup(label(r"\textbf{Chain rule} (Rudin 5.5): \ $h = g \circ f$, \ $h'(x) = g'(f(x))\, f'(x)$",
                            font_size=30),
                      label(r"two zooms composed: \ stretch by $f'(x)$, then by $g'(f(x))$", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        ys = (1.2, -0.3, -1.8)
        lines = VGroup(*[Line([-6, y, 0], [-0.6, y, 0], color=GREY_C, stroke_width=2) for y in ys])
        names = VGroup(*[MathTex(t, font_size=30).next_to(l, LEFT, buff=0.2) for t, l in zip((r"x", r"y", r"z"), lines)])
        w0, k1, k2 = 0.5, 2.0, 1.5
        segs = VGroup(*[Line([-3.3 - w / 2, y, 0], [-3.3 + w / 2, y, 0], color=c, stroke_width=10)
                        for w, y, c in ((w0, ys[0], C.SEQ), (w0 * k1, ys[1], C.APPROX), (w0 * k1 * k2, ys[2], C.EPS))])
        arrows = VGroup(Arrow([-3.3, ys[0] - 0.15, 0], [-3.3, ys[1] + 0.15, 0], buff=0, color=GREY_B, stroke_width=3),
                        Arrow([-3.3, ys[1] - 0.15, 0], [-3.3, ys[2] + 0.15, 0], buff=0, color=GREY_B, stroke_width=3))
        al = VGroup(MathTex(r"f:\ \times f'(x)", font_size=26).next_to(arrows[0], RIGHT, buff=0.15),
                    MathTex(r"g:\ \times g'(y)", font_size=26).next_to(arrows[1], RIGHT, buff=0.15))
        rows = [MathTex(r"f(t) - f(x)", r"=", r"(t - x)\,\big[f'(x) + u(t)\big]", font_size=32),
                MathTex(r"g(s) - g(y)", r"=", r"(s - y)\,\big[g'(y) + v(s)\big]", font_size=32),
                MathTex(r"\frac{h(t) - h(x)}{t - x}", r"=", r"\big[f'(x) + u(t)\big]\big[g'(y) + v(f(t))\big]",
                        font_size=32)]
        whys = [why(r"$u(t) \to 0$ as $t \to x$", font_size=22), why(r"$v(s) \to 0$ as $s \to y$", font_size=22),
                why(r"$s = f(t)$; \ let $t \to x$", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=1.3, buff=0.5, x=2.0, edge=6.6)
        trick = label(r"Rudin's trick avoids dividing by $f(t) - f(x)$, which can be $0$", font_size=24,
                      color=C.EPS).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The chain rule is two zooms composed. <bookmark mark='a'/> A tiny interval around x is stretched by f "
            "prime of x, then the result is stretched by g prime at f of x: the stretch factors multiply. "
            "<bookmark mark='b'/> Rudin's proof makes this precise without a classic trap. Write f of t minus f of x "
            "as t minus x times f prime of x plus an error u that goes to zero. <bookmark mark='c'/> Do the same for "
            "g. <bookmark mark='d'/> Substitute, divide by t minus x, and let t go to x. <bookmark mark='e'/> The "
            "tempting shortcut, multiplying and dividing by f of t minus f of x, fails when that difference is zero "
            "for t arbitrarily close to x."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(names), FadeIn(segs[0]))
            self.play(GrowArrow(arrows[0]), FadeIn(al[0]), TransformFromCopy(segs[0], segs[1]))
            self.play(GrowArrow(arrows[1]), FadeIn(al[1]), TransformFromCopy(segs[1], segs[2]))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            self.play(FadeIn(trick))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wiggle(self):
        d = load("wiggle")
        h, q = d["h"], d["q"]
        ax = plain_axes([-0.4, 0.4, 0.2], [-0.12, 0.12, 0.1], 6.2, 4.2, numbers=False).move_to([-3.3, -0.65, 0])
        u = np.linspace(1 / 0.4, 400, 60000)
        x = np.r_[-1 / u, 1 / u[::-1]]  # left to right through 0
        y = x * x * np.sin(1 / x)
        g = polyline(ax, x, y, color=C.FUNC, stroke_width=2.5)
        env = VGroup(ax.plot(lambda t: t * t, x_range=[-0.32, 0.32], color=GREY_B, stroke_width=1.5),
                     ax.plot(lambda t: -t * t, x_range=[-0.32, 0.32], color=GREY_B, stroke_width=1.5))
        fl = MathTex(r"f(x) = x^2 \sin\tfrac1x,\ \ f(0) = 0", font_size=28, color=C.FUNC).next_to(ax, UP, buff=0.15)
        ax2 = plain_axes([-0.4, 0.4, 0.2], [-1.4, 1.4, 1], 6.2, 4.2, numbers=False).move_to([3.4, -0.65, 0])
        u2 = np.linspace(1 / 0.4, 160, 60000)
        x2 = np.r_[-1 / u2, 1 / u2[::-1]]
        y2 = 2 * x2 * np.sin(1 / x2) - np.cos(1 / x2)
        g2 = polyline(ax2, x2, y2, color=C.PATHOLOGY, stroke_width=1.5)
        f2l = MathTex(r"f'(x) = 2x\sin\tfrac1x - \cos\tfrac1x \ (x \ne 0),\ \ f'(0) = 0", font_size=26,
                      color=C.PATHOLOGY).next_to(ax2, UP, buff=0.15)
        z = Dot(ax2.c2p(0, 0), radius=0.08, color=WHITE)
        head = label(r"\textbf{Rudin 5.6} \ Differentiable everywhere, \ but $f'$ is not continuous", font_size=32)
        head.to_edge(UP, buff=0.3)
        quot = MathTex(r"\frac{f(h) - f(0)}{h} = h \sin\tfrac1h \to 0", font_size=30).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And the museum piece. <bookmark mark='a'/> x squared times sine of one over x, set to zero at zero. It "
            "oscillates infinitely often, but squeezed between x squared and minus x squared. <bookmark mark='b'/> At "
            "zero, the difference quotient is h times sine of one over h, which goes to zero: so f prime of zero exists, "
            "and it's zero. <bookmark mark='c'/> Everywhere else the derivative is two x sine of one over x minus cosine "
            "of one over x, and near zero that keeps swinging between about minus one and one. So the derivative "
            "exists at every point, and it's not continuous at zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), Create(env), Create(g), FadeIn(fl), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(quot))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(f2l))
            self.play(Create(g2), FadeIn(z), run_time=1.8)
        assert np.all(np.abs(q) <= h)
        self.wait(0.5)
        self.clear_scene()
