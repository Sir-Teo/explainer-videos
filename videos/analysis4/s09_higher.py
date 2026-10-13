from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import heatmap, load, plain_axes, polyline, square_axes


def f_mix(X, Y):
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where((X == 0) & (Y == 0), 0.0, X * Y * (X**2 - Y**2) / (X**2 + Y**2))


class HigherOrder(VoiceoverScene):
    def construct(self):
        self.card()
        self.mixed()
        self.theorem()
        self.under_integral()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Mixed partials, and differentiating under $\int$",
                            r"Does the order of differentiation matter?", lit=(), part=4)
        with self.voiceover("Chapter eight: two more interchanges of limits, one that fails and one that works."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mixed(self):
        d = load("mixed")
        ratios, q = d["ratios"], d["q_xy"]
        S = 4.8
        ax = square_axes([-1, 1, 0.5], [-1, 1, 0.5], S / 2).move_to([-3.6, -0.75, 0])
        img = heatmap(f_mix, (-1, 1), (-1, 1), S, S, -0.5, 0.5).move_to(ax.c2p(0, 0))
        head = VGroup(MathTex(r"f(x, y) = \frac{xy(x^2 - y^2)}{x^2 + y^2}, \quad f(0, 0) = 0", font_size=34),
                      label(r"the second difference on an $h \times k$ rectangle at the origin:", font_size=24,
                            color=GREY_A),
                      MathTex(r"\frac{f(h, k) - f(0, k) - f(h, 0) + f(0, 0)}{hk} = \frac{h^2 - k^2}{h^2 + k^2}",
                              font_size=32, color=C.EPS)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.2)
        bx = plain_axes([-2, 2, 1], [-1.1, 1.1, 1], 5.6, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([3.3, -1.0, 0])
        curve = polyline(bx, np.log10(ratios), q, color=C.EPS, stroke_width=3.5)
        bl = MathTex(r"\log_{10}(h/k)", font_size=22, color=GREY_A).next_to(bx, DOWN, buff=0.1)
        rT = ValueTracker(-1.6)

        def rect():
            r = 10 ** rT.get_value()
            k = 0.8 / max(1, r)
            h = r * k
            return VGroup(Rectangle(width=h * S / 2, height=k * S / 2, color=WHITE, stroke_width=3).move_to(
                ax.c2p(h / 2, k / 2)), *[Dot(ax.c2p(a, b), radius=0.05, color=WHITE) for a, b in
                                         ((0, 0), (h, 0), (0, k), (h, k))])

        rc = always_redraw(rect)
        dot = always_redraw(lambda: Dot(bx.c2p(rT.get_value(), (10 ** (2 * rT.get_value()) - 1) /
                                               (10 ** (2 * rT.get_value()) + 1)), radius=0.08, color=WHITE))
        e1 = MathTex(r"h \ll k:\ \to -1 = f_{xy}(0, 0)", font_size=24, color=C.SEQ).move_to(bx.c2p(-1.05, 0.5))
        e2 = MathTex(r"k \ll h:\ \to +1 = f_{yx}(0, 0)", font_size=24, color=C.CLOSED_SET).move_to(bx.c2p(1.05, -0.5))
        ends = VGroup(VGroup(e1, Arrow(e1.get_bottom(), bx.c2p(-1.6, -0.93), buff=0.08, color=C.SEQ, stroke_width=2.5,
                                       max_tip_length_to_length_ratio=0.15)),
                      VGroup(e2, Arrow(e2.get_top(), bx.c2p(1.6, 0.93), buff=0.08, color=C.CLOSED_SET, stroke_width=2.5,
                                       max_tip_length_to_length_ratio=0.15)))
        note_ = label(r"only the shape matters, \ not the size: \ $f(\lambda h, \lambda k) = \lambda^2 f(h, k)$",
                      font_size=22, color=GREY_A).next_to(bx, UP, buff=0.15)
        assert d["fxy"] == -1 and d["fyx"] == 1 and q[0] < -0.999 and q[-1] > 0.999
        with self.voiceover(
            "<bookmark mark='a'/> In Rudin's Exercise 9.27, a function has two mixed partial derivatives at the origin that "
            "disagree. <bookmark mark='b'/> Both come from one quantity: the second difference across a small "
            "rectangle with corners at the origin, divided by its area. For this function that quotient depends only "
            "on the rectangle's shape. <bookmark mark='c'/> A tall, thin rectangle gives minus one: that's "
            "differentiating in x first, then in y. <bookmark mark='d'/> A short, wide one gives plus one: the other "
            "order. The two iterated limits disagree, the same way as the grid of m over m plus n from Part 3."
        ) as vo:
            self.play(FadeIn(head[0]), FadeIn(img), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1:]))
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(bl), Create(curve), FadeIn(rc), FadeIn(dot), FadeIn(note_))
            vo.wait_until("c")
            self.play(rT.animate.set_value(-1.9), run_time=1.0)
            self.play(FadeIn(ends[0]))
            vo.wait_until("d")
            self.play(rT.animate.set_value(1.9), run_time=4.0, rate_func=smooth)
            self.play(FadeIn(ends[1]))
        for m in (rc, dot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        import sympy as sp
        x, y, r = sp.symbols("x y r", real=True)
        f = x * y * (x**2 - y**2) / (x**2 + y**2)
        fxy = sp.simplify(sp.diff(f, x, y))
        on_x = sp.limit(fxy.subs(y, 0), x, 0)
        on_y = sp.limit(fxy.subs(x, 0), y, 0)
        assert on_x == 1 and on_y == -1  # f_xy is discontinuous at the origin
        S = 4.8
        ax = square_axes([-1, 1, 0.5], [-1, 1, 0.5], S / 2).move_to([-3.6, -0.85, 0])
        fn = sp.lambdify((x, y), fxy, "numpy")

        def F(X, Y):
            with np.errstate(invalid="ignore", divide="ignore"):
                return np.nan_to_num(fn(X, Y))

        img = heatmap(F, (-1, 1), (-1, 1), S, S, -1, 1).move_to(ax.c2p(0, 0))
        il = label(r"$f_{xy}$ near $0$: \ $+1$ on the $x$-axis, \ $-1$ on the $y$-axis", font_size=22,
                   color=GREY_A).next_to(ax, DOWN, buff=0.15)
        thm = VGroup(
            label(r"\textbf{Rudin 9.41} \ if $f_x, f_y, f_{xy}$ exist near a point", font_size=28),
            label(r"and $f_{xy}$ is continuous there, \ then $f_{yx}$ exists and", font_size=28),
            MathTex(r"f_{yx} = f_{xy}", font_size=40, color=C.EPS),
            label(r"in the museum piece $f_{xy}$ jumps at $0$:", font_size=26, color=C.PATHOLOGY),
            MathTex(r"f_{xy} = \frac{x^6 + 9x^4y^2 - 9x^2y^4 - y^6}{(x^2 + y^2)^3}", font_size=30, color=GREY_A),
            label(r"(computed symbolically, \ as are the values $\pm 1$)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, -0.4, 0])
        expected = (x**6 + 9 * x**4 * y**2 - 9 * x**2 * y**4 - y**6) / (x**2 + y**2) ** 3
        assert sp.simplify(fxy - expected) == 0
        with self.voiceover(
            "<bookmark mark='a'/> The cure is continuity again. Rudin's theorem 9.41: if the mixed partial f x y "
            "exists near a point and is continuous there, then the other one exists and they're equal. "
            "<bookmark mark='b'/> In the museum piece, f x y is plus one along the x-axis and minus one along the "
            "y-axis, so it can't be continuous at the origin. The swap fails exactly where continuity does."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm[:3]))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(ax), FadeIn(il))
            self.play(FadeIn(thm[3:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def under_integral(self):
        d = load("mixed")
        ts, lhs, rhs = d["ts"], d["lhs"], d["rhs"]
        x = np.linspace(1e-4, 1, 600)
        ax = plain_axes([0, 1, 0.5], [0, 1.05, 0.5], 4.6, 2.6).move_to([-3.6, 0.55, 0])
        bx = plain_axes([0, 1, 0.5], [-0.8, 0.05, 0.4], 4.6, 2.45).move_to([-3.6, -2.68, 0])
        cols = [C.SEQ, C.APPROX, C.CLOSED_SET]
        fam = VGroup(*[polyline(ax, x, x**t, color=c, stroke_width=3) for t, c in zip(ts, cols)])
        dfam = VGroup(*[polyline(bx, x, np.clip(x**t * np.log(x), -0.8, 0), color=c, stroke_width=3)
                        for t, c in zip(ts, cols)])
        al = MathTex(r"x^t", font_size=28).next_to(ax, UP, buff=0.05)
        bl = MathTex(r"\frac{\partial}{\partial t} x^t = x^t \log x", font_size=28).next_to(bx, UP, buff=0.05)
        head = VGroup(label(r"\textbf{Rudin 9.42} \ $\varphi$ and $\partial \varphi / \partial t$ continuous on "
                            r"$[a, b] \times [c, d]$ $\Rightarrow$", font_size=28),
                      MathTex(r"\frac{d}{dt}\int_a^b \varphi(x, t)\,dx = \int_a^b \frac{\partial \varphi}{\partial t}(x, t)"
                              r"\,dx", font_size=36, color=C.EPS)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.2)
        head.shift(RIGHT * 1.5)
        rows = VGroup(
            MathTex(r"F(t) = \int_0^1 x^t\,dx = \frac{1}{t + 1}", font_size=32),
            MathTex(r"F'(t) = -\frac{1}{(t + 1)^2}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, 0.6, 0])
        tab = VGroup(MathTex(r"t", r"\quad F'(t)", r"\quad \int_0^1 x^t \log x\,dx", font_size=26, color=GREY_A))
        for t, c, a, b in zip(ts, cols, lhs, rhs):
            tab.add(MathTex(rf"{t:g}", rf"\quad {{{a:.6f}}}", rf"\quad {{{b:.6f}}}", font_size=26, color=c))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.0, -1.4, 0])
        regrid(tab)
        note_ = label(r"the limit inside $\frac{d}{dt}$ passes through $\int$: \ uniform continuity on a compact "
                      r"rectangle (Part 3)", font_size=22, color=C.EPS).to_edge(DOWN, buff=0.15).shift(RIGHT * 2.6)
        if note_.width > 7.6:
            note_.width = 7.6
        assert np.allclose(lhs, rhs, atol=1e-5)
        with self.voiceover(
            "<bookmark mark='a'/> The swap that works is differentiation under the integral sign, Rudin 9.42: if phi "
            "and its partial derivative in t are continuous on a closed rectangle, the derivative of the integral is "
            "the integral of the derivative. <bookmark mark='b'/> Try it on the integral of x to the t from zero to "
            "one, which is one over t plus one. <bookmark mark='c'/> Differentiating the answer gives minus one over t "
            "plus one squared; integrating the derivative of the integrand, x to the t times log x, gives the same "
            "numbers. <bookmark mark='d'/> A derivative is a limit, so this is one more interchange of limits, made "
            "legal by the uniform continuity of Part 3. It's the swap Part 4 adds to the ledger."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(al), LaggedStart(*[Create(g_) for g_ in fam], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bl), LaggedStart(*[Create(g_) for g_ in dfam], lag_ratio=0.3), FadeIn(rows[1]))
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
