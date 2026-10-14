from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import heatmap, level_runs, load, plain_axes, polyline, square_axes
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
        xT, yT = ValueTracker(0.3), ValueTracker(0.1)  # the region spans x in [0.12, 1.88], y in [0.04, 1.70]

        def section(runs_, horizontal, c0, color):
            # the section's pieces (one or more intervals) as one VMobject, so the redraw keeps its family shape
            a = np.array([r_[0] for r_ in runs_])
            b = np.array([r_[1] for r_ in runs_])
            P0 = np.array([ax.c2p(u, c0) if horizontal else ax.c2p(c0, u) for u in a])
            P1 = np.array([ax.c2p(u, c0) if horizontal else ax.c2p(c0, u) for u in b])
            m = VMobject(stroke_color=color, stroke_width=5)
            m.set_points(segments_points(P0[:, 0], P0[:, 1], P1[:, 0], P1[:, 1]))
            return m

        def vsec():
            x0 = xT.get_value()
            return section(level_runs(g, inside[:, int(round(x0 / dx))]), False, x0, C.SEQ)

        def hsec():
            y0 = yT.get_value()
            return section(level_runs(g, inside[int(round(y0 / dx)), :]), True, y0, C.APPROX)

        for t_, u_ in zip(np.linspace(0.3, 1.85, 32), np.linspace(0.1, 1.65, 32)):  # every swept section meets Q
            assert inside[:, int(round(t_ / dx))].any() and inside[int(round(u_ / dx)), :].any()
        vs, hs = always_redraw(vsec), always_redraw(hsec)
        bx = plain_axes([0, 2, 0.5], [0, 2, 0.5], 4.0, 2.0).move_to([3.2, 0.9, 0])
        vg = polyline(bx, g, vert, color=C.SEQ, stroke_width=3)
        cx_ = plain_axes([0, 2, 0.5], [0, 2, 0.5], 4.0, 2.0).move_to([3.2, -2.1, 0])
        hg = polyline(cx_, g, horz, color=C.APPROX, stroke_width=3)
        vl = MathTex(rf"\int \lambda(Q_x)\,dx = {Av:.4f}", font_size=28, color=C.SEQ).next_to(bx, UP, buff=0.08)
        hl = MathTex(rf"\int \mu(Q^y)\,dy = {Ah:.4f}", font_size=28, color=C.APPROX).next_to(cx_, UP, buff=0.08)
        head = VGroup(label(r"Measure a set in the plane by its slices", font_size=34),
                      MathTex(rf"(\mu \times \lambda)(Q) = \int \lambda(Q_x)\,d\mu(x) = \int \mu(Q^y)\,d\lambda(y) = "
                              rf"{A:.4f}", r"\quad \text{\small (RCA 8.6)}", font_size=30, color=C.MEASURE)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_B)
        assert vl.get_top()[1] < head.get_bottom()[1] - 0.1
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
            vs.clear_updaters()
            self.play(FadeOut(vs), run_time=0.4)
            self.add(hs)
            self.play(Create(cx_), yT.animate.set_value(1.65), Create(hg), run_time=3.0, rate_func=linear)
            self.play(FadeIn(hl))
        hs.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"Fubini (1907) and Tonelli (1909)", font_size=34),
            label(r"\textbf{RCA 8.8} \ $\mu, \lambda$ $\sigma$-finite; \ if $f \ge 0$ is measurable, \ or if "
                  r"$\int\!\!\int |f| < \infty$:", font_size=28),
            MathTex(r"\int_X \Big(\int_Y f\,d\lambda\Big) d\mu = \int_{X \times Y} f\,d(\mu \times \lambda) = "
                    r"\int_Y \Big(\int_X f\,d\mu\Big) d\lambda", font_size=34, color=C.EPS),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        pm = ProofMap([r"rectangles $A \times B$", r"all measurable sets \ (monotone classes)", r"simple functions",
                       r"all $f \ge 0$ \ (monotone convergence)"], font_size=22, width=3.0, buff=0.3)
        pm.next_to(thm, DOWN, buff=0.7)
        note_ = label(r"the condition matters: \ next, \ a function whose two iterated integrals disagree",
                      font_size=26, color=C.PATHOLOGY).to_edge(DOWN, buff=0.3)
        # one small picture per rung of the ladder, in the unit square under its box
        P = 2.0
        centers = [pm.boxes[k].get_x() for k in range(4)]
        py = (pm.get_bottom()[1] + note_.get_top()[1]) / 2 + 0.1

        def U(c_, u, v):  # unit-square coordinates -> scene
            return np.array([c_ - P / 2 + P * u, py - P / 2 + P * v, 0])

        def blob(t_, k=1.0):
            r_ = k * (0.36 + 0.06 * np.sin(3 * t_) + 0.035 * np.cos(5 * t_))
            return 0.5 + r_[:, None] * np.array([np.cos(t_), np.sin(t_)]).T

        tt_ = np.linspace(0, 2 * np.pi, 200)
        frames_ = VGroup(*[Square(P, stroke_color=GREY_B, stroke_width=1.5).move_to([c_, py, 0]) for c_ in centers])
        c0, c1, c2, c3 = centers
        rect = Polygon(U(c0, 0.18, 0.3), U(c0, 0.66, 0.3), U(c0, 0.66, 0.8), U(c0, 0.18, 0.8), stroke_width=2,
                       stroke_color=C.MEASURE, fill_color=C.MEASURE, fill_opacity=0.55)
        Ab = Line(U(c0, 0.18, 0.05), U(c0, 0.66, 0.05), color=C.SEQ, stroke_width=6)
        Bb = Line(U(c0, 0.05, 0.3), U(c0, 0.05, 0.8), color=C.APPROX, stroke_width=6)
        pic1 = VGroup(rect, Ab, Bb)
        bp = blob(tt_)
        outline = Polygon(*[U(c1, a, b) for a, b in bp], stroke_color=WHITE, stroke_width=2, fill_opacity=0)
        n_ = 14
        def inside(u, v):  # the blob is star-shaped about its centre: compare the radius with r(angle)
            a_ = math.atan2(v - 0.5, u - 0.5)
            return math.hypot(u - 0.5, v - 0.5) < 0.36 + 0.06 * math.sin(3 * a_) + 0.035 * math.cos(5 * a_)

        cells = VGroup()
        for i in range(n_):
            for j in range(n_):
                u_, v_ = (i + 0.5) / n_, (j + 0.5) / n_
                if inside(u_, v_):
                    cells.add(Square(P / n_, stroke_width=0.6, stroke_color=BLACK, fill_color=C.MEASURE,
                                     fill_opacity=0.6).move_to(U(c1, u_, v_)))
        pic2 = VGroup(cells, outline)
        lay_cols = [C.SEQ, C.APPROX, C.EPS]
        pic3 = VGroup(*[Polygon(*[U(c2, a, b) for a, b in blob(tt_, k_)], stroke_width=1.5, stroke_color=col,
                                fill_color=col, fill_opacity=0.45) for k_, col in zip((1.0, 0.68, 0.38), lay_cols)])

        def bump(X, Y):
            return np.exp(-((X - 0.45) ** 2 + (Y - 0.5) ** 2) / 0.05) + 0.55 * np.exp(-((X - 0.75) ** 2 + (Y - 0.3) ** 2) / 0.02)

        pic4 = heatmap(bump, (0, 1), (0, 1), P, P, -1.0, 1.0).move_to([c3, py, 0])
        assert bump(np.array([0.3]), np.array([0.9]))[0] >= 0
        caps = VGroup(*[MathTex(t_, font_size=24, color=GREY_A).next_to(frames_[k], DOWN, buff=0.12) for k, t_ in
                        enumerate((r"A \times B", r"\textstyle\bigcup\ \text{rectangles}",
                                   r"\textstyle\sum c_i \mathbf 1_{E_i}", r"f = \lim s_n \ge 0"))])
        assert caps.get_bottom()[1] > note_.get_top()[1] + 0.05 and frames_.get_top()[1] < pm.get_bottom()[1] - 0.1
        pics = [pic1, pic2, pic3, pic4]
        # while the statement is read, its subject: a function f >= 0 on the square (the last rung's picture), swept by
        # a vertical and a horizontal section, the two iterated integrals
        sT = ValueTracker(0.0)
        x3 = centers[3]
        vsw = always_redraw(lambda: Line(U(x3, sT.get_value(), 0), U(x3, sT.get_value(), 1), color=WHITE,
                                         stroke_width=3))
        hsw = always_redraw(lambda: Line(U(x3, 0, sT.get_value()), U(x3, 1, sT.get_value()), color=WHITE,
                                         stroke_width=3))
        with self.voiceover(
            "<bookmark mark='a'/> Fubini's theorem, with Tonelli's version, for sigma-finite measures: for a "
            "non-negative measurable function, "
            "or for any function whose absolute value has a finite double integral, the two iterated integrals agree "
            "with the double integral. <bookmark mark='b'/> The proof climbs a ladder: <bookmark mark='r1'/> "
            "rectangles, where both sides are just length times length; <bookmark mark='r2'/> then all measurable "
            "sets, built from rectangles using monotone classes; <bookmark mark='r3'/> then simple functions, which "
            "are finite sums of sets; <bookmark mark='r4'/> then everything, by monotone convergence. "
            "<bookmark mark='c'/> The condition is not decoration."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm[0]), Create(frames_[3]), FadeIn(pic4))
            self.play(FadeIn(thm[1:]))
            sT.set_value(0.04)
            self.add(vsw)
            self.play(sT.animate.set_value(0.96), run_time=2.0, rate_func=linear)
            self.remove(vsw)
            sT.set_value(0.04)
            self.add(hsw)
            self.play(sT.animate.set_value(0.96), run_time=2.0, rate_func=linear)
            vsw.clear_updaters()
            hsw.clear_updaters()
            self.play(FadeOut(hsw), run_time=0.4)
            vo.wait_until("b")
            self.play(FadeIn(pm))
            for k in range(4):
                vo.wait_until(f"r{k + 1}")
                anims = [*pm.light(k), FadeIn(caps[k])]
                if k == 1:
                    anims += [Create(frames_[k]), Create(outline), LaggedStart(*[FadeIn(c_) for c_ in cells],
                                                                                lag_ratio=0.01)]
                elif k == 3:
                    anims += [Indicate(frames_[3], color=C.EPS, scale_factor=1.04)]
                else:
                    anims += [Create(frames_[k]), FadeIn(pics[k])]
                self.play(*anims, run_time=1.2)
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
        head = VGroup(label(r"A function whose two iterated integrals disagree", font_size=34),
                      MathTex(r"f(x, y) = \frac{x^2 - y^2}{(x^2 + y^2)^2} \ \text{ on } (0, 1)^2", font_size=30),
                      label(r"orange: \ $f > 0$ \ (below the diagonal); \ blue: \ $f < 0$", font_size=22, color=GREY_A)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)
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
            label(r"$\iint |f| = \infty$: \ Fubini does not apply", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.2, -0.9, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.2, -0.9, 0])
        assert abs(I1 - math.pi / 4) < 1e-12 and abs(I2 + math.pi / 4) < 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> The classic counterexample: x squared minus y squared, over the square of x squared plus "
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
