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
        S = 4.6
        head = VGroup(label(r"Two mixed partials that disagree", font_size=34),
                      MathTex(r"f(x, y) = \frac{xy(x^2 - y^2)}{x^2 + y^2}, \quad f(0, 0) = 0",
                              r"\quad \text{\small (Rudin, Exercise 9.27)}", font_size=32)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_B)
        ax = square_axes([-1, 1, 0.5], [-1, 1, 0.5], S / 2).move_to([-3.75, -0.85, 0])
        img = heatmap(f_mix, (-1, 1), (-1, 1), S, S, -0.5, 0.5).move_to(ax.c2p(0, 0))
        legend = label(r"blue: \ $f < 0$, \ \ dark: \ $0$, \ \ orange: \ $f > 0$", font_size=22,
                       color=GREY_A).next_to(img, DOWN, buff=0.12)
        diffq = VGroup(label(r"the second difference on an $h \times k$ rectangle at the origin:", font_size=24,
                             color=GREY_A),
                       MathTex(r"\frac{f(h, k) - f(0, k) - f(h, 0) + f(0, 0)}{hk} = \frac{h^2 - k^2}{h^2 + k^2}",
                               font_size=30, color=C.EPS)).arrange(DOWN, buff=0.12)
        diffq.next_to([3.4, head.get_bottom()[1] - 0.25, 0], DOWN, buff=0)
        bx = plain_axes([-2, 2, 1], [-1.1, 1.1, 1], 5.6, 2.7, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([3.5, -1.55, 0])
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
        assert diffq.get_right()[0] <= 6.6 and diffq.get_left()[0] > img.get_right()[0] + 0.3
        assert note_.get_top()[1] < diffq.get_bottom()[1] - 0.1 and bl.get_bottom()[1] > -3.6
        assert legend.get_bottom()[1] > -3.65 and img.get_top()[1] < head.get_bottom()[1] - 0.2
        with self.voiceover(
            "<bookmark mark='a'/> In Rudin's Exercise 9.27, a function has two mixed partial derivatives at the origin that "
            "disagree. <bookmark mark='b'/> Both come from one quantity: the second difference across a small "
            "rectangle with corners at the origin, divided by its area. For this function that quotient depends only "
            "on the rectangle's shape. <bookmark mark='c'/> A tall, thin rectangle gives minus one: that's "
            "differentiating in x first, then in y. <bookmark mark='d'/> A short, wide one gives plus one: the other "
            "order. The two iterated limits disagree, the same way as the grid of m over m plus n from Part 3."
        ) as vo:
            self.play(FadeIn(head[0]), FadeIn(img), Create(ax), FadeIn(legend))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(FadeIn(diffq))
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
        S = 4.6
        title = label(r"Mixed partials commute when they are continuous", font_size=34).to_edge(UP, buff=0.3)
        ax = square_axes([-1, 1, 0.5], [-1, 1, 0.5], S / 2).move_to([-3.75, -0.85, 0])
        fn = sp.lambdify((x, y), fxy, "numpy")

        def F(X, Y):
            with np.errstate(invalid="ignore", divide="ignore"):
                return np.nan_to_num(fn(X, Y))

        img = heatmap(F, (-1, 1), (-1, 1), S, S, -1, 1).move_to(ax.c2p(0, 0))
        il = label(r"$f_{xy}$ near $0$: \ $+1$ on the $x$-axis, \ $-1$ on the $y$-axis", font_size=22,
                   color=GREY_A).next_to(ax, DOWN, buff=0.15)
        thm = VGroup(
            label(r"if $f_x, f_y, f_{xy}$ exist near a point \ (Rudin 9.41)", font_size=28),
            label(r"and $f_{xy}$ is continuous there, \ then $f_{yx}$ exists and", font_size=28),
            MathTex(r"f_{yx} = f_{xy}", font_size=40, color=C.EPS),
            label(r"in the museum piece $f_{xy}$ jumps at $0$:", font_size=26, color=C.PATHOLOGY),
            MathTex(r"f_{xy} = \frac{x^6 + 9x^4y^2 - 9x^2y^4 - y^6}{(x^2 + y^2)^3}", font_size=30, color=GREY_A),
            label(r"(computed symbolically, \ as are the values $\pm 1$)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        thm.next_to([0.4, title.get_bottom()[1] - 0.3, 0], DR, buff=0)
        expected = (x**6 + 9 * x**4 * y**2 - 9 * x**2 * y**4 - y**6) / (x**2 + y**2) ** 3
        assert sp.simplify(fxy - expected) == 0
        # why 9.41 holds (Rudin 9.40): Delta(h, k)/hk = f_xy at some point (xi, eta) inside the h x k rectangle.
        # For the museum f the quotient is (h^2 - k^2)/(h^2 + k^2), and f_xy depends only on the direction:
        # f_xy = 3u - 2u^3 with u = cos 2theta. So the mean-value points fill the ray where 3u - 2u^3 equals the
        # quotient (|u| <= 1/sqrt 2, where that is increasing); the dot sits halfway out along it.
        hv, kv = ValueTracker(0.8), ValueTracker(0.6)
        from scipy.optimize import brentq

        def quot(h, k):
            return (h * h - k * k) / (h * h + k * k)

        def mvt(h, k):
            u = brentq(lambda u_: 3 * u_ - 2 * u_**3 - quot(h, k), -1 / math.sqrt(2), 1 / math.sqrt(2))
            th = 0.5 * math.acos(u)
            t = 0.5 * min(h / math.cos(th), k / math.sin(th))
            return t * math.cos(th), t * math.sin(th), th

        for h_, k_ in ((0.8, 0.6), (0.8, 0.05), (0.05, 0.8), (0.12, 0.09), (0.03, 0.4), (0.4, 0.02)):
            a_, b_, _ = mvt(h_, k_)
            fq = float(f.subs({x: h_, y: k_})) / (h_ * k_)  # f(0, k) = f(h, 0) = f(0, 0) = 0
            assert abs(fq - quot(h_, k_)) < 1e-12 and abs(F(np.array(a_), np.array(b_)) - fq) < 1e-9
            assert 0 < a_ < h_ and 0 < b_ < k_

        def rect_():
            h, k = hv.get_value(), kv.get_value()
            return Polygon(ax.c2p(0, 0), ax.c2p(h, 0), ax.c2p(h, k), ax.c2p(0, k), color=WHITE, stroke_width=3,
                           fill_color=WHITE, fill_opacity=0.08).set_z_index(3)

        rect = always_redraw(rect_)
        pt = always_redraw(lambda: Dot(ax.c2p(*mvt(hv.get_value(), kv.get_value())[:2]), radius=0.07,
                                       color=C.EPS).set_z_index(4))

        def ray_():
            th = mvt(hv.get_value(), kv.get_value())[2]
            L = min(1 / math.cos(th), 1 / math.sin(th))
            return DashedLine(ax.c2p(0, 0), ax.c2p(L * math.cos(th), L * math.sin(th)), color=C.EPS, stroke_width=2,
                              dash_length=0.08).set_z_index(3)

        ray = always_redraw(ray_)
        sg = VGroup(*[MathTex(c_, font_size=30, color=WHITE).move_to(ax.c2p(*xy_)).shift(sh_)
                      for c_, xy_, sh_ in (("+", (0.8, 0.6), 0.25 * UR), ("-", (0, 0.6), 0.25 * UL),
                                           ("-", (0.8, 0), 0.25 * DR), ("+", (0, 0), 0.25 * DL))]).set_z_index(4)
        why = VGroup(
            MathTex(r"\frac{f(h,k) - f(0,k) - f(h,0) + f(0,0)}{hk} = f_{xy}(\xi, \eta)", font_size=28),
            label(r"for some $(\xi, \eta)$ in the rectangle \ (the mean value theorem twice, 9.40)",
                  font_size=22, color=GREY_A),
            label(r"any shape, shrunk: \ $(\xi, \eta) \to 0$, \ and continuity leaves one limit",
                  font_size=22, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(thm[2], DOWN, buff=0.35).align_to(thm, LEFT)
        assert why.get_right()[0] <= 6.6 and why.get_bottom()[1] > -3.6 and thm.get_right()[0] <= 6.6
        assert thm.get_bottom()[1] > -3.6 and ax.get_top()[1] < title.get_bottom()[1] - 0.6

        rd = VGroup(MathTex(r"\frac{\Delta}{hk} = f_{xy}(\xi, \eta) =", font_size=30, color=C.EPS),
                    DecimalNumber(quot(0.8, 0.6), num_decimal_places=2, font_size=30, color=C.EPS)
                    ).arrange(RIGHT, buff=0.15).next_to(ax, UP, buff=0.12)
        rd[1].add_updater(lambda m: m.set_value(quot(hv.get_value(), kv.get_value())))
        assert quot(0.8, 0.05) > 0.99 and quot(0.05, 0.8) < -0.99
        img.set_z_index(0)
        with self.voiceover(
            "<bookmark mark='a'/> The cure is continuity again. Rudin's theorem 9.41: if f x, f y and the mixed "
            "partial f x y exist near a point, and f x y is continuous there, then the other one exists and they're equal. "
            "<bookmark mark='m'/> The reason: by the mean value theorem, used twice, the second difference over h k "
            "equals f x y at some point inside the rectangle. <bookmark mark='s'/> Shrink the rectangle, whatever its "
            "shape, and that point is squeezed into the corner; if f x y is continuous, the quotient has only one "
            "possible limit. <bookmark mark='b'/> In the museum piece, f x y depends only on the direction: plus one "
            "along the x-axis, minus one along the y-axis. <bookmark mark='w'/> A flat rectangle's quotient is near "
            "plus one, a tall one's near minus one, so the mean-value point rides a different ray for each shape, "
            "however small the rectangle. The swap fails exactly where continuity does."
        ) as vo:
            vo.wait_until("a")
            img.set_opacity(0.25)  # f_xy, faint until the narration turns to it
            self.play(FadeIn(title), FadeIn(thm[:3]), FadeIn(img), Create(ax))
            vo.wait_until("m")
            self.play(Create(rect), FadeIn(sg))
            self.play(FadeIn(pt, scale=1.5), FadeIn(why[0]))
            self.play(FadeIn(why[1]))
            vo.wait_until("s")
            self.play(FadeOut(sg), hv.animate.set_value(0.5), kv.animate.set_value(0.1), run_time=1.4)
            self.play(hv.animate.set_value(0.1), kv.animate.set_value(0.5), run_time=1.4)
            self.play(hv.animate.set_value(0.12), kv.animate.set_value(0.09), FadeIn(why[2]), run_time=1.4)
            vo.wait_until("b")
            self.play(FadeOut(why), hv.animate.set_value(0.8), kv.animate.set_value(0.6))
            self.play(img.animate.set_opacity(1.0), FadeIn(il), FadeIn(rd), FadeIn(ray))
            vo.wait_until("w")
            self.play(hv.animate.set_value(0.8), kv.animate.set_value(0.05), run_time=1.8)
            self.play(hv.animate.set_value(0.05), kv.animate.set_value(0.8), run_time=2.2)
            self.play(hv.animate.set_value(0.03), kv.animate.set_value(0.4), run_time=1.0)
            self.play(hv.animate.set_value(0.4), kv.animate.set_value(0.02), run_time=1.6)
            for m_ in (rd[1], ray):
                m_.clear_updaters()
            self.play(FadeIn(thm[3:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def under_integral(self):
        d = load("mixed")
        ts, lhs, rhs = d["ts"], d["lhs"], d["rhs"]
        x = np.linspace(1e-4, 1, 600)
        head = VGroup(label(r"Differentiating under the integral sign", font_size=34),
                      MathTex(r"\frac{d}{dt}\int_a^b \varphi(x, t)\,dx = \int_a^b \frac{\partial \varphi}{\partial t}(x, t)"
                              r"\,dx", font_size=34, color=C.EPS),
                      label(r"if $\varphi$ and $\partial \varphi / \partial t$ are continuous on $[a, b] \times [c, d]$ "
                            r"\ (Rudin 9.42)", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        top = head.get_bottom()[1] - 0.25
        # the family and its t-derivative, one panel each (from mark b on)
        ax = plain_axes([0, 1, 0.5], [0, 1.05, 0.5], 5.4, 1.75)
        ax.move_to([-6.55 + 2.7, top - 0.875, 0])
        bx = plain_axes([0, 1, 0.5], [-0.8, 0.05, 0.4], 5.4, 1.75)
        bx.move_to([ax.get_x(), ax.get_bottom()[1] - 0.5 - 0.875, 0])
        cols = [C.SEQ, C.APPROX, C.CLOSED_SET]
        fam = VGroup(*[polyline(ax, x, x**t, color=c, stroke_width=3) for t, c in zip(ts, cols)])
        dvals = [x**t * np.log(x) for t in ts]
        dfam = VGroup(*[runs(bx, x, v, c, 3) for v, c in zip(dvals, cols)])  # cut where they leave the window
        al = MathTex(r"x^t", font_size=28).move_to(ax.c2p(0.1, 0.85))
        assert all(np.all(x[x < 0.2] ** t < 0.85 - 0.12) for t in ts if t >= 1) and 0.2 ** 0.5 < 0.85 - 0.3
        bl = MathTex(r"x^t \log x", font_size=26).move_to(bx.c2p(0.8, -0.66))
        assert all(np.all(v[x > 0.58] > -0.5) for v in dvals)  # the label's corner of the panel is empty
        rows = VGroup(
            MathTex(r"F(t) = \int_0^1 x^t\,dx = \frac{1}{t + 1}", font_size=30),
            MathTex(r"F'(t) = -\frac{1}{(t + 1)^2}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows.next_to([ax.get_right()[0] + 0.6, top, 0], DR, buff=0)
        tab = VGroup(MathTex(r"t", r"\quad F'(t)", r"\quad \int_0^1 x^t \log x\,dx", font_size=26, color=GREY_A))
        for t, c, a, b in zip(ts, cols, lhs, rhs):
            tab.add(MathTex(rf"{t:g}", rf"\quad {{{a:.6f}}}", rf"\quad {{{b:.6f}}}", font_size=26, color=c))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        regrid(tab)
        tab.next_to(rows, DOWN, buff=0.35, aligned_edge=LEFT)
        note_ = VGroup(label(r"the limit inside $\frac{d}{dt}$ passes through $\int$:", font_size=24, color=C.EPS),
                       label(r"uniform continuity on a compact rectangle (Part 3)", font_size=24, color=C.EPS)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bx, DOWN, buff=0.25, aligned_edge=LEFT)
        assert np.allclose(lhs, rhs, atol=1e-5) and np.allclose(lhs, -1 / (ts + 1) ** 2, atol=1e-9)
        assert note_.get_right()[0] < rows.get_left()[0] - 0.2 and note_.get_bottom()[1] > -3.6
        assert tab.get_right()[0] <= 6.6 and tab.get_bottom()[1] > -3.6
        assert bx.get_top()[1] < ax.get_bottom()[1] - 0.3 and ax.get_top()[1] < head.get_bottom()[1] - 0.1
        # the statement as a picture: F(t + dt) - F(t) is the area of the sliver between two members of the family,
        # i.e. the integral of the change in height; dividing by dt and letting dt -> 0 is the interchange
        sax = plain_axes([0, 1, 0.5], [0, 1.05, 0.5], 6.0, top + 3.45 - 0.3)
        sax.move_to([-6.55 + 3.0, (top - 0.1 - 3.45) / 2, 0])
        t0, xs_ = 0.5, np.linspace(0, 1, 160)
        dtv = ValueTracker(0.8)
        base = Polygon(sax.c2p(0, 0), *[sax.c2p(v, v**t0) for v in xs_], sax.c2p(1, 0), stroke_width=0,
                       fill_color=C.SEQ, fill_opacity=0.28)
        c0 = polyline(sax, xs_, xs_**t0, color=C.SEQ, stroke_width=3)
        c1 = always_redraw(lambda: polyline(sax, xs_, xs_ ** (t0 + dtv.get_value()), color=C.APPROX, stroke_width=3))
        sliver = always_redraw(lambda: Polygon(*[sax.c2p(v, v**t0) for v in xs_],
                                               *[sax.c2p(v, v ** (t0 + dtv.get_value())) for v in xs_[::-1]],
                                               stroke_width=0, fill_color=C.MEASURE, fill_opacity=0.75))
        Fl = MathTex(r"F(t)", font_size=28, color=C.SEQ).move_to(sax.c2p(0.78, 0.2))
        cl = VGroup(MathTex(r"x^{t}", font_size=26, color=C.SEQ), MathTex(r"x^{t + \Delta t}", font_size=26,
                                                                           color=C.APPROX))
        cl.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(sax.c2p(0.12, 0.85))
        idt = VGroup(
            MathTex(r"\frac{F(t + \Delta t) - F(t)}{\Delta t} = \int_a^b \frac{\varphi(x, t + \Delta t) - "
                    r"\varphi(x, t)}{\Delta t}\,dx", font_size=28),
            label(r"the change in area is the integral of the change in height \ (orange)", font_size=22,
                  color=GREY_A),
            label(r"let $\Delta t \to 0$ on both sides: \ the theorem lets the limit pass inside", font_size=22,
                  color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        idt.next_to([sax.get_right()[0] + 0.4, sax.get_y(), 0], RIGHT, buff=0)
        assert idt.get_right()[0] <= 6.6 and sax.get_bottom()[1] > -3.6
        assert np.all(xs_[1:-1] ** t0 > xs_[1:-1] ** (t0 + 0.1))  # the sliver has positive height inside (0, 1)
        with self.voiceover(
            "<bookmark mark='a'/> The swap that works is differentiation under the integral sign, Rudin 9.42: if phi "
            "and its partial derivative in t are continuous on a closed rectangle, <bookmark mark='p'/> the derivative "
            "of the integral is the integral of the derivative. The change in area between two nearby curves is the "
            "integral of the change in height; dividing by delta t and shrinking it is exactly the interchange. "
            "<bookmark mark='b'/> Try it on the integral of x to the t from zero to "
            "one, which is one over t plus one. <bookmark mark='c'/> Differentiating the answer gives minus one over t "
            "plus one squared; integrating the derivative of the integrand, x to the t times log x, gives the same "
            "numbers. <bookmark mark='d'/> A derivative is a limit, so this is one more interchange of limits, made "
            "legal by the uniform continuity of Part 3. It's the swap Part 4 adds to the ledger."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), FadeIn(head[2]))
            self.play(Create(sax), FadeIn(base), Create(c0), FadeIn(Fl), FadeIn(cl[0]))
            vo.wait_until("p")
            self.play(FadeIn(head[1]), Create(c1), FadeIn(sliver), FadeIn(cl[1]), FadeIn(idt[0]))
            self.play(FadeIn(idt[1]))
            self.play(dtv.animate.set_value(0.12), FadeIn(idt[2]), run_time=2.5)
            c1.clear_updaters()
            sliver.clear_updaters()
            vo.wait_until("b")
            self.play(FadeOut(VGroup(sax, base, c0, c1, sliver, Fl, cl, idt)))
            self.play(Create(ax), FadeIn(al), LaggedStart(*[Create(g_) for g_ in fam], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bl), LaggedStart(*[Create(g_) for g_ in dfam], lag_ratio=0.3), FadeIn(rows[1]))
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
