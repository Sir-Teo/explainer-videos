from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import load, plain_axes, polyline
from videos.analysis4.compute import cumtrap


class Picard(VoiceoverScene):
    def construct(self):
        self.card()
        self.operator()
        self.exp_iterates()
        self.sin_iterates()
        self.nonunique()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Picard: \ differential equations in $C[a, b]$",
                            r"Why does $y' = F(t, y)$ have exactly one solution?", lit=(), part=4)
        with self.voiceover("Chapter five: the function space of Part 3 earns its keep."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def operator(self):
        h = 0.5
        t = np.linspace(0, h, 1001)
        F = lambda s, y: s + np.sin(y)  # noqa: E731
        y = 0.5 + 0.9 * t
        z = 0.5 - 0.4 * np.sin(9 * t) + 0.3 * t

        def T(u):
            return 0.5 + cumtrap(F(t, u), t)

        Ty, Tz = T(y), T(z)
        ratio = np.abs(Ty - Tz).max() / np.abs(y - z).max()
        assert ratio <= 1 * h + 1e-9
        ax = plain_axes([0, h, 0.25], [0.0, 1.2, 0.5], 5.6, 3.4).move_to([-3.6, -1.35, 0])
        gy, gz = polyline(ax, t, y, color=C.SEQ, stroke_width=3), polyline(ax, t, z, color=C.APPROX, stroke_width=3)
        gTy = polyline(ax, t, Ty, color=C.SEQ, stroke_width=3)
        gTz = polyline(ax, t, Tz, color=C.APPROX, stroke_width=3)
        k1 = int(np.argmax(np.abs(y - z)))
        k2 = int(np.argmax(np.abs(Ty - Tz)))
        gap1 = Line(ax.c2p(t[k1], y[k1]), ax.c2p(t[k1], z[k1]), color=C.DIST, stroke_width=5)
        gap2 = Line(ax.c2p(t[k2], Ty[k2]), ax.c2p(t[k2], Tz[k2]), color=C.DIST, stroke_width=5)
        lab1 = MathTex(r"y, z", font_size=28).next_to(ax, UP, buff=0.05)
        lab2 = MathTex(r"Ty, Tz", font_size=28).next_to(ax, UP, buff=0.05)
        rows = VGroup(
            MathTex(r"y' = F(t, y),\ y(0) = y_0", r"\iff", r"y(t) = y_0 + \int_0^t F(s, y(s))\,ds", font_size=32),
            MathTex(r"(Ty)(t) = y_0 + \int_0^t F(s, y(s))\,ds", r"\quad \text{on } C[0, h]", font_size=32, color=C.EPS),
            label(r"solutions are exactly the fixed points of $T$", font_size=26),
        ).arrange(DOWN, buff=0.22).to_edge(UP, buff=0.3)
        rows[0][2].set_color(C.FUNC)
        est = VGroup(
            label(r"if $|F(s, a) - F(s, b)| \le L|a - b|$:", font_size=26),
            MathTex(r"\|Ty - Tz\| \le Lh\, \|y - z\|", font_size=34, color=C.EPS),
            label(r"a contraction of $C[0, h]$ when $Lh < 1$", font_size=26, color=C.CONNECTED_SET),
            MathTex(rf"F = t + \sin y:\ L = 1,\ h = \tfrac12:\ \ \tfrac{{\|Ty - Tz\|}}{{\|y - z\|}} = {ratio:.3f}",
                    font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -1.35, 0])
        with self.voiceover(
            "<bookmark mark='a'/> By the fundamental theorem of calculus, a differential equation with an initial "
            "value is the same as an integral equation. <bookmark mark='b'/> Read the right side as a machine T that "
            "takes a continuous function y and returns another one. Solutions are exactly the functions T leaves "
            "unchanged. <bookmark mark='c'/> If F is Lipschitz in y with constant L, then T shrinks sup distances by "
            "the factor L times h, the length of the interval. <bookmark mark='d'/> Here are two functions and their "
            "images: the largest gap shrinks to less than half. For h small, T is a contraction of the complete space "
            "C of zero h, Part 3's space, and the contraction principle hands us a solution, and only one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ax), Create(gy), Create(gz), FadeIn(lab1))
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(est[:3]), Create(gap1))
            vo.wait_until("d")
            self.play(ReplacementTransform(gy, gTy), ReplacementTransform(gz, gTz), ReplacementTransform(gap1, gap2),
                      FadeTransform(lab1, lab2), run_time=2.0)
            self.play(FadeIn(est[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def camera_axes(self, xr, yr):
        return plain_axes([xr[0], xr[1], 0.5], [yr[0], yr[1], 1], 4.0, 3.6, numbers=True, font_size=18,
                          x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                          y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([4.3, -0.9, 0])

    def exp_iterates(self):
        d = load("picard")
        t, Y, err1, cam = d["t"], d["Y"], d["err1"], d["cam1"]
        ax = plain_axes([0, 1, 0.25], [0, 3, 1], 6.4, 4.4).move_to([-3.2, -0.9, 0])
        ex = polyline(ax, t, np.exp(t), color=WHITE, stroke_width=3.5)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 8) for k in range(9)]
        its = [polyline(ax, t, Y[k], color=cols[k], stroke_width=3) for k in range(9)]
        names = [r"0", r"1", r"1 + t", r"1 + t + \tfrac{t^2}{2}", r"1 + t + \tfrac{t^2}{2} + \tfrac{t^3}{6}"]
        nl = [MathTex(rf"y_{{{k}}} = {names[k]}" if k < len(names) else rf"y_{{{k}}}: \ \sup|y_{{{k}}} - e^t| = "
                      rf"{sci(float(err1[k]), 2)}", font_size=28, color=cols[k]).next_to(ax, UP, buff=0.1) for k in range(9)]
        head = label(r"$y' = y$, \ $y(0) = 1$: \ iterate $T$ from $y_0 = 0$", font_size=32).to_edge(UP, buff=0.3)
        cax = self.camera_axes((0, 2), (0, 3))
        cl = VGroup(MathTex(r"y(\tfrac12)", font_size=22, color=GREY_B).next_to(cax, DOWN, buff=0.1),
                    MathTex(r"y(1)", font_size=22, color=GREY_B).next_to(cax, LEFT, buff=0.1))
        cam_t = label(r"the camera: \ each iterate is one point", font_size=22, color=GREY_A).next_to(cax, UP, buff=0.1)
        dots = [Dot(cax.c2p(*c_), radius=0.06, color=cols[k]) for k, c_ in enumerate(cam[:9])]
        target = Dot(cax.c2p(math.exp(0.5), math.e), radius=0.08, color=WHITE)
        tl = MathTex(r"(e^{1/2}, e)", font_size=24).next_to(target, RIGHT, buff=0.1)
        assert np.all(np.diff(err1) < 0)
        with self.voiceover(
            "<bookmark mark='a'/> Watch it work on the simplest equation, y prime equals y, starting from y equal to "
            "one. Start the iteration from the zero function. <bookmark mark='b'/> The first iterate is the constant "
            "one, the next is one plus t, then one plus t plus t squared over two. <bookmark mark='c'/> The Picard "
            "iterates are the Taylor polynomials of e to the t, and they converge to it uniformly. "
            "<bookmark mark='d'/> On the camera, each iterate is a single point, plotted by its values at one half "
            "and one, and the points march to the point of the exponential function."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(ex))
            vo.wait_until("a")
            self.play(Create(its[0]), FadeIn(nl[0]))
            vo.wait_until("b")
            for k in range(1, 5):
                self.play(its[k - 1].animate.set_stroke(opacity=0.3), Create(its[k]), FadeTransform(nl[k - 1], nl[k]),
                          run_time=1.0)
            vo.wait_until("c")
            for k in range(5, 9):
                self.play(its[k - 1].animate.set_stroke(opacity=0.3), Create(its[k]), FadeTransform(nl[k - 1], nl[k]),
                          run_time=0.7)
            vo.wait_until("d")
            self.play(Create(cax), FadeIn(cl), FadeIn(cam_t), FadeIn(target), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(dd, scale=1.5) for dd in dots], lag_ratio=0.3), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sin_iterates(self):
        d = load("picard")
        t, Z, steps, fact, err2, ref = d["t"], d["Z"], d["steps"], d["fact"], d["err2"], d["ref"]
        ax = plain_axes([0, 1, 0.25], [0.4, 2.0, 0.5], 6.4, 4.0).move_to([-3.2, -0.8, 0])
        rg = polyline(ax, t, ref, color=WHITE, stroke_width=3.5)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 6) for k in range(7)]
        its = [polyline(ax, t, Z[k], color=cols[k], stroke_width=3) for k in range(7)]
        head = VGroup(label(r"$y' = t + \sin y$, \ $y(0) = \tfrac12$: \ no formula, \ but the same iteration",
                            font_size=30),
                      label(r"white: \ a fine Runge--Kutta solution, for comparison", font_size=22, color=GREY_A)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)
        tab = VGroup(MathTex(r"k", r"\quad \|y_{k+1} - y_k\|", r"\quad \le \|y_1 - y_0\| \tfrac{h^k}{k!}", font_size=26,
                             color=GREY_A))
        for k in range(8):
            tab.add(MathTex(rf"{k}", r"\quad " + sci(float(steps[k]), 2), r"\quad " + sci(float(fact[k]), 2),
                            font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.7, -0.4, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
            row[2].align_to(tab[0][2], LEFT)
        out = label(rf"after 12 steps: \ within ${sci(float(err2[-1]), 1)}$ of Runge--Kutta", font_size=24,
                    color=C.EPS).next_to(tab, DOWN, buff=0.3)
        assert np.all(steps <= fact + 1e-9)
        with self.voiceover(
            "<bookmark mark='a'/> Now an equation with no formula for its solution: y prime equals t plus sine y. "
            "<bookmark mark='b'/> The same iteration closes in on the solution, drawn in white from an independent "
            "numerical method. <bookmark mark='c'/> On the whole interval from zero to one, L times h is one, so T is "
            "not quite a contraction there, but a sharper estimate shows the k-th change is at most h to the k over k "
            "factorial times the first, which is even better than geometric. <bookmark mark='d'/> After twelve steps "
            "the iterate agrees with the numerical solution to about eight digits."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(Create(its[0]))
            vo.wait_until("b")
            self.play(Create(rg), FadeIn(head[1]))
            for k in range(1, 7):
                self.play(its[k - 1].animate.set_stroke(opacity=0.3), Create(its[k]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nonunique(self):
        ax = plain_axes([0, 3, 1], [0, 4, 1], 6.4, 4.2).move_to([-3.2, -0.9, 0])
        t = np.linspace(0, 3, 601)
        cs = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        sols = VGroup(Line(ax.c2p(0, 0), ax.c2p(3, 0), color=C.SEQ, stroke_width=4))
        for c in cs:
            y = np.where(t > c, (t - c) ** 2, 0.0)
            assert np.allclose(np.gradient(y, t)[t > c + 0.05], 2 * np.sqrt(y[t > c + 0.05]), atol=1e-2)
            sols.add(runs(ax, t, y, C.APPROX, 3))
        head = VGroup(MathTex(r"y' = 2\sqrt{|y|}, \qquad y(0) = 0", font_size=36),
                      label(r"$2\sqrt{|y|}$ is not Lipschitz at $y = 0$", font_size=26, color=GREY_A)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        side = VGroup(
            MathTex(r"y = 0", font_size=30, color=C.SEQ),
            MathTex(r"y = \begin{cases} 0 & t \le c \\ (t - c)^2 & t > c \end{cases}", font_size=30, color=C.APPROX),
            label(r"every $c \ge 0$ gives a solution:", font_size=24),
            label(r"infinitely many through one point", font_size=24, color=C.PATHOLOGY),
            label(r"Peano's theorem (via Arzel\`a--Ascoli):", font_size=24, color=GREY_A),
            label(r"continuity alone gives existence,", font_size=24, color=GREY_A),
            label(r"not uniqueness", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.6, -0.8, 0])
        card = museum_card(r"$y' = 2\sqrt{|y|}$", r"a classical example", r"`an ODE has one solution'",
                           r"Lipschitz is what Picard needs", width=3.6).scale(0.75)
        card.to_corner(UR, buff=0.15)
        with self.voiceover(
            "<bookmark mark='a'/> The Lipschitz condition is not a technicality. y prime equals twice the square root "
            "of y, starting from zero. <bookmark mark='b'/> The zero function solves it. So does t squared. So does "
            "the function that waits until any time c and then follows t minus c squared. <bookmark mark='c'/> "
            "Infinitely many solutions through one point. Peano's theorem, proved with Arzelà–Ascoli from Part 3, "
            "still gives existence for any continuous right side, but uniqueness needs the Lipschitz bound that makes "
            "T a contraction."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(Create(sols[0]), FadeIn(side[0]))
            self.play(LaggedStart(*[Create(s_) for s_ in sols[1:]], lag_ratio=0.3), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2:4]), FadeIn(card, scale=0.95))
            self.play(FadeIn(side[4:]))
        self.wait(0.4)
        self.clear_scene()
