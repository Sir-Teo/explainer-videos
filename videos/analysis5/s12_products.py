from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import heatmap, load, plain_axes, polyline, square_axes
from videos.analysis5.compute import trap


def fub(X, Y):
    with np.errstate(invalid="ignore", divide="ignore"):
        return (X**2 - Y**2) / (X**2 + Y**2) ** 2


class Products(VoiceoverScene):
    def construct(self):
        self.card()
        self.slices()
        self.theorem()
        self.counterexample()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"Product measures and Fubini", r"When may we integrate in either order?", lit=(),
                            part=5)
        with self.voiceover("Chapter eleven: integrals over products, and the order of integration."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def slices(self):
        ax = square_axes([0, 2, 0.5], [0, 2, 0.5], 2.4).move_to([-3.6, -0.7, 0])
        th = np.linspace(0, 2 * math.pi, 400)
        cx, cy = 1.0, 1.0

        def r(t):
            return 0.75 + 0.18 * np.sin(3 * t) + 0.08 * np.cos(5 * t)

        X, Y = cx + r(th) * np.cos(th), cy + r(th) * np.sin(th)
        region = Polygon(*[ax.c2p(a, b) for a, b in zip(X, Y)], color=C.MEASURE, fill_opacity=0.25, stroke_width=3)
        # exact area of a star-shaped region: (1/2) int r^2 dt
        A = 0.5 * trap(r(th) ** 2, th)
        # by vertical sections and by horizontal sections (computed on a fine grid)
        g = np.linspace(0, 2, 1601)
        GX, GY = np.meshgrid(g, g)
        R = np.hypot(GX - cx, GY - cy)
        T = np.arctan2(GY - cy, GX - cx)
        inside = R <= r(T)
        dx = g[1] - g[0]
        vert = inside.sum(axis=0) * dx  # length of each vertical section
        horz = inside.sum(axis=1) * dx
        Av, Ah = trap(vert, g), trap(horz, g)
        assert abs(Av - A) < 5e-3 and abs(Ah - A) < 5e-3
        xT = ValueTracker(0.3)

        def vsec():
            x0 = xT.get_value()
            col = inside[:, int(round(x0 / dx))]
            ys = g[col]
            if len(ys) == 0:
                return VGroup()
            return VGroup(Line(ax.c2p(x0, ys.min()), ax.c2p(x0, ys.max()), color=C.SEQ, stroke_width=5))

        vs = always_redraw(vsec)
        bx = plain_axes([0, 2, 0.5], [0, 2, 0.5], 4.0, 2.0).move_to([3.2, 0.9, 0])
        vg = polyline(bx, g, vert, color=C.SEQ, stroke_width=3)
        cx_ = plain_axes([0, 2, 0.5], [0, 2, 0.5], 4.0, 2.0).move_to([3.2, -2.1, 0])
        hg = polyline(cx_, g, horz, color=C.APPROX, stroke_width=3)
        vl = MathTex(rf"\int \lambda(Q_x)\,dx = {Av:.4f}", font_size=28, color=C.SEQ).next_to(bx, UP, buff=0.08)
        hl = MathTex(rf"\int \mu(Q^y)\,dy = {Ah:.4f}", font_size=28, color=C.APPROX).next_to(cx_, UP, buff=0.08)
        head = VGroup(label(r"\textbf{RCA 8.6} \ measure a set in the plane by its slices", font_size=30),
                      MathTex(rf"(\mu \times \lambda)(Q) = \int \lambda(Q_x)\,d\mu(x) = \int \mu(Q^y)\,d\lambda(y) = "
                              rf"{A:.4f}", font_size=30, color=C.MEASURE)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> The product of two measures gives rectangles their area, and every measurable set "
            "in the plane can be measured by slices. <bookmark mark='b'/> Slide a vertical line across the region and "
            "record the length of each vertical section; the integral of those lengths is the area. "
            "<bookmark mark='c'/> Slicing horizontally instead gives the same number."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), FadeIn(region))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.add(vs)
            self.play(Create(bx), xT.animate.set_value(1.85), Create(vg), run_time=4.0, rate_func=linear)
            self.play(FadeIn(vl))
            vo.wait_until("c")
            self.play(Create(cx_), Create(hg), run_time=2.0)
            self.play(FadeIn(hl))
        vs.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{RCA 8.8} \ (Fubini 1907, \ Tonelli 1909)", font_size=30),
            label(r"if $f \ge 0$ is measurable, \ or if $\int\!\!\int |f| < \infty$:", font_size=28),
            MathTex(r"\int_X \Big(\int_Y f\,d\lambda\Big) d\mu = \int_{X \times Y} f\,d(\mu \times \lambda) = "
                    r"\int_Y \Big(\int_X f\,d\mu\Big) d\lambda", font_size=34, color=C.EPS),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.4)
        pm = ProofMap([r"rectangles $A \times B$", r"all measurable sets \ (monotone classes)", r"simple functions",
                       r"all $f \ge 0$ \ (monotone convergence)"], font_size=22, width=3.0, buff=0.3)
        pm.next_to(thm, DOWN, buff=0.7)
        note_ = label(r"the condition matters: \ next, \ a function whose two iterated integrals disagree",
                      font_size=26, color=C.PATHOLOGY).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> Fubini's theorem, with Tonelli's version: for a non-negative measurable function, "
            "or for any function whose absolute value has a finite double integral, the two iterated integrals agree "
            "with the double integral. <bookmark mark='b'/> The proof climbs a ladder: rectangles, then all "
            "measurable sets, using monotone classes, then simple functions, then everything by monotone convergence. "
            "<bookmark mark='c'/> The condition is not decoration."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(pm))
            for k in range(4):
                self.play(*pm.light(k), run_time=0.7)
            self.play(*pm.done())
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counterexample(self):
        d = load("fubini")
        I1, I2, absint = float(d["I1"]), float(d["I2"]), d["absint"]
        S = 4.6
        ax = square_axes([0, 1, 0.25], [0, 1, 0.25], S).move_to([-3.4, -0.8, 0])
        img = heatmap(fub, (0.002, 1), (0.002, 1), S, S, -6, 6).move_to(ax.c2p(0.5, 0.5))
        head = VGroup(MathTex(r"f(x, y) = \frac{x^2 - y^2}{(x^2 + y^2)^2} \ \text{ on } (0, 1)^2", font_size=34),
                      label(r"orange: \ $f > 0$ \ (below the diagonal); \ blue: \ $f < 0$", font_size=22, color=GREY_A)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        xT, yT = ValueTracker(0.02), ValueTracker(0.02)
        vline = always_redraw(lambda: Line(ax.c2p(xT.get_value(), 0), ax.c2p(xT.get_value(), 1), color=WHITE,
                                           stroke_width=3))
        hline = always_redraw(lambda: Line(ax.c2p(0, yT.get_value()), ax.c2p(1, yT.get_value()), color=WHITE,
                                           stroke_width=3))
        rows = VGroup(
            MathTex(r"\int_0^1 f\,dy = \frac{1}{1 + x^2}", font_size=30, color=C.CLOSED_SET),
            MathTex(rf"\int_0^1\!\!\int_0^1 f\,dy\,dx = \frac{{\pi}}{{4}} = {I1:.6f}", font_size=30, color=C.CLOSED_SET),
            MathTex(r"\int_0^1 f\,dx = -\frac{1}{1 + y^2}", font_size=30, color=C.SEQ),
            MathTex(rf"\int_0^1\!\!\int_0^1 f\,dx\,dy = -\frac{{\pi}}{{4}} = {I2:.6f}", font_size=30, color=C.SEQ),
            MathTex(rf"\iint_{{[\varepsilon, 1]^2}} |f|:\ {absint[0]:.2f},\ {absint[1]:.2f},\ {absint[2]:.2f}"
                    r"\ (\varepsilon = 10^{-1}, 10^{-2}, 10^{-3})", font_size=26, color=C.PATHOLOGY),
            label(r"$\iint |f| = \infty$: \ Fubini does not apply \ (RCA 8.9c)", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.2, -0.9, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.2, -0.9, 0])
        assert abs(I1 - math.pi / 4) < 1e-12 and abs(I2 + math.pi / 4) < 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> Rudin's counterexample: x squared minus y squared, over the square of x squared plus "
            "y squared, on the unit square. It's positive below the diagonal and negative above, and huge near the "
            "corner. <bookmark mark='b'/> Integrate in y first: each vertical line gives one over one plus x squared, "
            "and integrating that in x gives pi over four. <bookmark mark='c'/> Integrate in x first: each horizontal "
            "line gives minus one over one plus y squared, and the total is minus pi over four. "
            "<bookmark mark='d'/> Two orders, two answers, exactly like Part 3's grid. The absolute value has infinite "
            "integral near the corner, so Fubini's hypothesis fails."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), Create(ax))
            vo.wait_until("b")
            self.add(vline)
            self.play(xT.animate.set_value(0.98), run_time=3.0, rate_func=linear)
            self.remove(vline)
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.add(hline)
            self.play(yT.animate.set_value(0.98), run_time=3.0, rate_func=linear)
            self.remove(hline)
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        for m in (vline, hline):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
