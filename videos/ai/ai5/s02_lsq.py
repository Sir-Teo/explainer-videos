from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import load

PTS = np.array([[1.0, 1.0], [2.0, 3.0], [3.0, 2.0]])  # three points (illustrative)
DATA, FIT, RES = C.TRUE_P, C.MODEL_Q, C.SURPRISE


def best_line(P):
    A = np.stack([np.ones(len(P)), P[:, 0]], 1)
    return np.linalg.solve(A.T @ A, A.T @ P[:, 1])


class LeastSquares(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.squares()
        self.projection()
        self.zipf()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Least squares", r"What is the best line through points that disagree?", part=5)
        with self.voiceover("Chapter one. Least squares."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def squares(self):
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=5.6, y_length=5.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.6, -0.2, 0])
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.09, color=DATA) for p in PTS])
        a, b = ValueTracker(2.6), ValueTracker(-0.3)
        unit = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]

        def line():
            return Line(ax.c2p(0, a.get_value()), ax.c2p(4, a.get_value() + 4 * b.get_value()), color=FIT, stroke_width=4)

        def sq():
            g = VGroup()
            for x, yv in PTS:
                fy = a.get_value() + b.get_value() * x
                r = yv - fy
                side = abs(r) * unit
                if side < 1e-3:
                    continue
                s = Square(side_length=side, stroke_color=RES, stroke_width=2, fill_color=RES, fill_opacity=0.3)
                s.move_to(ax.c2p(x, (yv + fy) / 2) + RIGHT * side / 2)
                g.add(s, Line(ax.c2p(x, yv), ax.c2p(x, fy), color=RES, stroke_width=3))
            return g

        ln, sqs = always_redraw(line), always_redraw(sq)

        def total():
            return float(sum((yv - a.get_value() - b.get_value() * x) ** 2 for x, yv in PTS))

        tv = DecimalNumber(total(), num_decimal_places=2, font_size=40, color=RES)
        tv.add_updater(lambda m: m.set_value(total()))
        read = VGroup(label(r"total area of the squares:", font_size=30), tv).arrange(RIGHT, buff=0.2)
        read.move_to([3.4, 1.8, 0])
        colors = {r"\hat y_i": FIT, r"y_i": DATA}
        f = cmath(r"\min", r"\sum_i", r"(", r"y_i", "-", r"\hat y_i", r")^2", colors=colors, font_size=46)
        f.next_to(read, DOWN, buff=0.5)
        hist = label(r"Legendre (1805); \ Gauss, to find the asteroid Ceres (1801)", font_size=24, color=GREY_A)
        hist.next_to(f, DOWN, buff=0.5)
        tag = label(r"three points \ (illustrative)", font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        a_star, b_star = best_line(PTS)
        with self.voiceover(
            "The oldest method of all fits a line. Here are three points. <bookmark mark='a'/> For any line, measure "
            "how far each point misses it, straight up or down, and square each miss: literally, a square. "
            "<bookmark mark='b'/> Least squares picks the line whose squares have the smallest total area. "
            "<bookmark mark='c'/> Legendre published it in 1805. Gauss had used it four years earlier, to predict "
            "where the lost asteroid Ceres would reappear."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln))
            self.play(FadeIn(sqs), FadeIn(read))
            self.play(a.animate.set_value(0.4), b.animate.set_value(0.9), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(f))
            self.play(a.animate.set_value(a_star), b.animate.set_value(b_star), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(hist))
        for m in (ln, sqs, tv):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def projection(self):
        y = PTS[:, 1]
        A = np.stack([np.ones(3), PTS[:, 0]], 1)
        beta = best_line(PTS)
        yhat = A @ beta
        r = y - yhat
        assert abs(r @ A[:, 0]) < 1e-12 and abs(r @ A[:, 1]) < 1e-12
        axes = ThreeDAxes(x_range=[0, 4, 1], y_range=[0, 4, 1], z_range=[0, 4, 1], x_length=4.6, y_length=4.6,
                          z_length=4.6, axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})
        axes.shift(LEFT * 1.4 + DOWN * 0.7)
        c1, c2 = A[:, 0], A[:, 1]
        e1 = c1 / np.linalg.norm(c1)
        e2 = c2 - (c2 @ e1) * e1
        e2 /= np.linalg.norm(e2)
        corners = [yhat + 1.9 * (a * e1 + b * e2) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]  # a patch around y-hat
        plane = Polygon(*[axes.c2p(*p) for p in corners], stroke_width=1, stroke_color=FIT, fill_color=FIT,
                        fill_opacity=0.18)
        o = axes.c2p(0, 0, 0)
        vy = Arrow3D(o, axes.c2p(*y), color=DATA, thickness=0.02, resolution=8)
        vh = Arrow3D(o, axes.c2p(*yhat), color=FIT, thickness=0.02, resolution=8)
        col1 = Arrow3D(o, axes.c2p(*c1), color=GREY_A, thickness=0.015, resolution=8)
        col2 = Arrow3D(o, axes.c2p(*c2), color=GREY_A, thickness=0.015, resolution=8)
        res = DashedLine(axes.c2p(*y), axes.c2p(*yhat), color=RES, stroke_width=4)
        # a small right-angle mark at y-hat, in the plane of the residual and the first column
        u1 = r / np.linalg.norm(r) * 0.35
        u2 = (c1 - (c1 @ r) / (r @ r) * r)
        u2 = u2 / np.linalg.norm(u2) * 0.35
        mark = VMobject(color=WHITE, stroke_width=2).set_points_as_corners(
            [axes.c2p(*(yhat + u1)), axes.c2p(*(yhat + u1 + u2)), axes.c2p(*(yhat + u2))])
        ly = MathTex(r"\mathbf{y}", font_size=40, color=DATA).move_to(axes.c2p(*(y + np.array([0, 0.3, 0.3]))))
        lh = MathTex(r"\hat{\mathbf{y}}", font_size=40, color=FIT).move_to(axes.c2p(*(yhat + np.array([0.3, 0.4, -0.2]))))
        l1 = MathTex(r"\mathbf{1}", font_size=32, color=GREY_A).move_to(axes.c2p(*(c1 * 1.25)))
        l2 = MathTex(r"\mathbf{x}", font_size=32, color=GREY_A).move_to(axes.c2p(*(c2 * 1.12)))
        for m in (ly, lh, l1, l2):
            self.add_fixed_orientation_mobjects(m)
            self.remove(m)
        colors = {r"\mathbf{y}": DATA, r"A\boldsymbol{\beta}": FIT, r"\boldsymbol{\beta}": FIT}
        e1 = cmath(r"A^{\top}", r"(", r"\mathbf{y}", "-", r"A\boldsymbol{\beta}", r")", "=", r"\mathbf{0}",
                   colors=colors, font_size=42)
        e2 = cmath(r"A^{\top}A", r"\,", r"\boldsymbol{\beta}", "=", r"A^{\top}", r"\mathbf{y}", colors=colors, font_size=42)
        for e in (e1, e2):
            e.to_corner(UL, buff=0.5)
        ycap = label(r"the three heights, \ as one point in 3D", font_size=26, color=DATA).to_corner(UR, buff=0.5)
        pcap = label(r"every line's three predictions: \ a plane, \ $a\mathbf{1} + b\mathbf{x}$", font_size=26,
                     color=FIT).next_to(ycap, DOWN, buff=0.2).align_to(ycap, RIGHT)
        ncap = label(r"the leftover is perpendicular to the plane: \ the normal equations", font_size=26,
                     color=RES).to_edge(DOWN, buff=0.4)
        for m in (e1, e2, ycap, pcap, ncap):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-35 * DEGREES, zoom=0.85)
        with self.voiceover(
            "There's a beautiful way to see the answer. Write the three heights as a single point in three "
            "dimensions. <bookmark mark='a'/> Every possible line makes three predictions, and all of them together "
            "form a plane: everything you can reach by mixing a column of ones, which shifts the line up and down, "
            "with the column of x's, which tilts it. <bookmark mark='b'/> The best line is the point of that plane "
            "closest to the data. Drop a perpendicular. <bookmark mark='c'/> Perpendicular means the leftover is at "
            "right angles to both columns: the misses have no shift and no tilt left in them that the line could "
            "still fix. Write that down, and you have the normal equations, which give the best line directly, no "
            "searching needed."
        ) as vo:
            self.play(Create(axes), GrowFromPoint(vy, o), FadeIn(ly), FadeIn(ycap))
            vo.wait_until("a")
            self.play(GrowFromPoint(col1, o), GrowFromPoint(col2, o), FadeIn(l1), FadeIn(l2))
            self.play(FadeIn(plane), FadeIn(pcap))
            vo.wait_until("b")
            self.play(Create(res), GrowFromPoint(vh, o), FadeIn(lh))
            self.play(Create(mark))
            vo.wait_until("c")
            self.play(FadeIn(e1), FadeIn(ncap))
            morph(self, e1, e2)
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def zipf(self):
        z = load("zipf")
        f, r, beta = np.asarray(z["f"]), np.asarray(z["r"]), np.asarray(z["beta"])
        assert -1.2 < beta[1] < -0.95 and z["r2"] > 0.99
        ax = Axes(x_range=[0, 3, 1], y_range=[1, 6, 1], x_length=7.6, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, -0.4, 0])
        xl = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(ax.c2p(v, 1), DOWN, buff=0.12)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=24, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in range(1, 7)])
        xn = label(r"rank: \ the $r$-th commonest word", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.55)
        yn = label(r"times it appears", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(math.log10(ri), math.log10(fi)), radius=0.03, color=DATA, fill_opacity=0.8)
                        for ri, fi in zip(r, f)])
        names = VGroup(*[Text(w, font="DejaVu Sans Mono", font_size=20, color=GREY_A)
                         .next_to(dots[k], UR if k % 2 else RIGHT, buff=0.06) for k, w in enumerate(z["words"][:4])])
        fit = Line(ax.c2p(0, beta[0]), ax.c2p(3, beta[0] + 3 * beta[1]), color=FIT, stroke_width=4)
        law = cmath(r"\text{count}", r"\;\propto\;", r"r", rf"^{{{beta[1]:.2f}}}", font_size=44)
        law.move_to([4.6, 1.6, 0])
        notes = VGroup(label(rf"least-squares slope: \ ${beta[1]:.2f}$", font_size=28, color=FIT),
                       label(rf"it explains ${100 * z['r2']:.1f}\%$ of the variation", font_size=26, color=GREY_A),
                       label(rf"${z['n_words'] / 1e6:.2f}$ million words of Part 1's books", font_size=24, color=GREY_B))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(law, DOWN, buff=0.5).set_x(4.4)
        cite_ = cite(r"G.~K.~Zipf, \textit{Human Behavior and the Principle of Least Effort} (1949)", corner=DR)
        # "explains 99.6% of the variation": the scatter around the average, and what the line leaves over
        BW = 3.6
        tot = Rectangle(width=BW, height=0.28, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8)
        left = Rectangle(width=max(BW * (1 - z["r2"]), 0.02), height=0.28, stroke_width=0, fill_color=RES, fill_opacity=0.95)
        r2_bars = VGroup(VGroup(label(r"the scatter around the average", font_size=20, color=GREY_A), tot),
                         VGroup(label(r"what the line leaves over", font_size=20, color=RES), left))
        for row in r2_bars:
            row.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        r2_bars.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(notes, DOWN, buff=0.35).align_to(notes, LEFT)
        with self.voiceover(
            "Here's least squares on real data. Count every word in part one's books, and rank them, from the "
            "commonest down. <bookmark mark='a'/> With logarithmic scales on both axes, the thousand commonest "
            "words fall almost exactly on a line. <bookmark mark='b'/> The least-squares slope is minus 1.08: the "
            "r-th commonest word turns up about one over r times as often as the first. That's Zipf's law, and the "
            "line explains 99.6 percent of the variation: <bookmark mark='c'/> of all the scatter of the points "
            "around their average height, the line accounts for everything but a sliver."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), FadeIn(names), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), Write(law))
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.3), FadeIn(cite_))
            vo.wait_until("c")
            self.play(FadeIn(r2_bars[0]))
            self.play(FadeIn(r2_bars[1][0]), GrowFromEdge(r2_bars[1][1], LEFT))
        self.wait(0.3)
        self.clear_scene()
