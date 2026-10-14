from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import load, polyline
from videos.analysis1.compute import tent


class FunctionSpace(VoiceoverScene):
    def construct(self):
        self.card()
        self.ball()
        self.tents()
        self.directions()
        self.dictionary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"A first space of functions", r"Is every closed and bounded set compact?", part=1)
        with self.voiceover(
            "Chapter eleven. We end where the series is headed: a space whose points are functions. And it comes with a "
            "warning."
        ) as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ball(self):
        ax = Axes(x_range=[0, 1, 0.25], y_range=[-1.2, 1.2, 1], x_length=8.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_numbers": False}).shift(LEFT * 1.6 + DOWN * 0.6)
        band = Rectangle(width=ax.x_length, height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1], stroke_width=0,
                         fill_color=C.DIST, fill_opacity=0.15).move_to(ax.c2p(0.5, 0))
        edges = VGroup(DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=C.DIST, stroke_width=2),
                       DashedLine(ax.c2p(0, -1), ax.c2p(1, -1), color=C.DIST, stroke_width=2))
        dfn = MathTex(r"B = \{\, f \in C[0,1] : |f(x)| \le 1 \text{ for all } x \,\}", font_size=38, color=C.DIST)
        dfn.to_edge(UP, buff=0.45)
        x = np.linspace(0, 1, 500)
        samples = VGroup(*[polyline(ax, x, f(x), color=c, stroke_width=3) for f, c in (
            (lambda t: 0.8 * np.sin(2 * np.pi * t), C.FUNC), (lambda t: 1 - 2 * t ** 2, C.APPROX),
            (lambda t: 0.5 * np.cos(9 * t) - 0.2, C.DELTA))])
        props = VGroup(label(r"\textbf{bounded}: every $f$ is within $1$ of $0$", font_size=28),
                       label(r"\textbf{closed}: a limit, in the sup distance, of functions", font_size=28),
                       label(r"\quad with $|f_n| \le 1$ still has $|f| \le 1$", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        props.next_to(dfn, DOWN, buff=0.3).shift(RIGHT * 2.2)
        with self.voiceover(
            "Take the continuous functions on the interval from zero to one, with the sup distance from chapter five. "
            "<bookmark mark='b'/> Its closed unit ball is the set of functions whose graphs stay between minus one and "
            "one: <bookmark mark='s'/> any graph inside this band. <bookmark mark='p'/> It's bounded, obviously. And it's "
            "closed: if functions with values between minus one and one converge in the sup distance, their limit's "
            "values are between minus one and one too. In k-dimensional space, Heine–Borel would now say: compact."
        ) as vo:
            self.play(Create(ax), FadeIn(band), Create(edges))
            vo.wait_until("b")
            self.play(Write(dfn))
            vo.wait_until("s")
            self.play(LaggedStart(*[Create(s_) for s_ in samples], lag_ratio=0.3))
            vo.wait_until("p")
            self.play(FadeIn(props))
        self.wait(0.3)
        self.play(FadeOut(VGroup(samples, props)))
        self.ax, self.band, self.edges, self.dfn = ax, band, edges, dfn

    # ------------------------------------------------------------------
    def tents(self):
        ax = self.ax
        D = load("bumps")["D"]
        x = np.unique(np.concatenate([np.linspace(0, 1, 4001)] + [[1 / (n + 1), 1 / n, (1 / (n + 1) + 1 / n) / 2]
                                                                  for n in range(1, 13)]))
        # one sequence, one hue: f_1 in the sequence colour, later tents lighter
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(WHITE), 0.09 * (n - 1)) for n in range(1, 9)]

        def tent_curve(n):  # drawn only on its support [1/(n+1), 1/n]; elsewhere it is 0, the axis itself
            xn = x[(x >= 1 / (n + 1)) & (x <= 1 / n)]
            return polyline(ax, xn, tent(xn, n), color=cols[n - 1], stroke_width=3.5)

        T = VGroup(*[tent_curve(n) for n in range(1, 9)])
        labs = VGroup()
        for n in range(1, 5):
            t_ = MathTex(rf"f_{n}", font_size=26, color=cols[n - 1])
            t_.next_to(ax.c2p((1 / (n + 1) + 1 / n) / 2, 1.0), UP, buff=0.15)
            t_.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.04)
            labs.add(t_)
        dl = MathTex(r"f_n = \text{a tent of height } 1 \text{ on } \Big[\tfrac{1}{n+1}, \tfrac1n\Big]", font_size=34)
        dl.next_to(self.dfn, DOWN, buff=0.25)
        with self.voiceover(
            "It isn't. <bookmark mark='t'/> Here's a sequence inside the ball: f n is a tent of height one over the "
            "interval from one over n plus one to one over n, and zero everywhere else. <bookmark mark='m'/> The tents "
            "march toward zero, getting narrower, each one sitting where all the others are zero."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(dl), Create(T[0]), FadeIn(labs[0]))
            vo.wait_until("m")
            for n in range(1, 8):
                anims = [Create(T[n])]
                if n < 4:
                    anims.append(FadeIn(labs[n]))
                self.play(*anims, run_time=0.45)
        grid = VGroup()
        size = 0.42
        o = np.array([3.0, 1.3, 0])
        for i in range(8):
            for j in range(8):
                v = D[i, j]
                sq = Square(side_length=size * 0.92, stroke_width=0, fill_color=C.DIST if v > 0.5 else "#1B2333",
                            fill_opacity=0.85 if v > 0.5 else 1).move_to(o + np.array([j * size, -i * size, 0]))
                t = Text(f"{v:.0f}", font_size=16, color=BLACK if v > 0.5 else GREY_B).move_to(sq)
                grid.add(VGroup(sq, t))
        idx = VGroup(*[MathTex(str(i + 1), font_size=16, color=GREY_B).next_to(o + np.array([-size * 0.5, -i * size, 0]),
                                                                              LEFT, buff=0.06) for i in range(8)],
                     *[MathTex(str(j + 1), font_size=16, color=GREY_B).next_to(o + np.array([j * size, size * 0.5, 0]),
                                                                              UP, buff=0.06) for j in range(8)])
        g_l = MathTex(r"d(f_n, f_m)", font_size=30, color=C.DIST).next_to(VGroup(grid, idx), UP, buff=0.12)
        assert np.allclose(D[~np.eye(len(D), dtype=bool)], 1.0) and np.allclose(np.diag(D), 0.0)
        concl = VGroup(label(r"every two tents are at distance exactly $1$, so a ball of radius $\tfrac12$", font_size=27),
                       label(r"holds at most one: \ $\{f_n\}$ has no limit point \ (2.20)", font_size=27),
                       label(r"$\Rightarrow$ \ $B$ is closed and bounded, but \textbf{not compact} \ (2.37)", font_size=29,
                             color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now measure distances. <bookmark mark='d'/> Where one tent reaches height one, every other tent is zero, so "
            "the distance between any two of them is exactly one. <bookmark mark='g'/> Here's the whole table: zeros on "
            "the diagonal, ones everywhere else. <bookmark mark='c'/> So a ball of radius one half contains at most one "
            "tent, and the set of tents has no limit point at all. An infinite subset with no limit point: by chapter "
            "seven, the unit ball is not compact."
        ) as vo:
            vo.wait_until("d")
            self.play(VGroup(ax, self.band, self.edges, T, labs).animate.scale(0.85).to_edge(LEFT, buff=0.3))
            vo.wait_until("g")
            self.play(FadeIn(g_l), FadeIn(idx), LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeOut(dl), FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def directions(self):
        n = 7
        R = 2.3
        c0 = np.array([-3.2, -0.3, 0])
        pts = [c0 + R * np.array([np.cos(2 * np.pi * k / n + 0.3), np.sin(2 * np.pi * k / n + 0.3), 0]) for k in range(n)]
        edges = VGroup(*[Line(pts[i], pts[j], color=C.DIST, stroke_width=1.5, stroke_opacity=0.6)
                         for i in range(n) for j in range(i + 1, n)])
        dots = VGroup(*[Dot(p, radius=0.1, color=C.SEQ) for p in pts])
        names = VGroup(*[MathTex(rf"f_{k + 1}", font_size=28, color=C.SEQ).move_to(c0 + (R + 0.42) * (p - c0) / R)
                         for k, p in enumerate(pts)])
        tag = schematic_tag(corner=UL).to_corner(UL, buff=0.45)
        cap = label(r"every edge has length $1$ \ (impossible to draw flat)", font_size=26, color=C.DIST)
        cap.next_to(VGroup(edges, names), DOWN, buff=0.2)
        # first three points (a triangle with sides 1), then four (a tetrahedron, drawn in perspective)
        tri_p = [c0 + 1.7 * np.array([np.cos(np.pi / 2 + 2 * np.pi * k / 3), np.sin(np.pi / 2 + 2 * np.pi * k / 3), 0])
                 for k in range(3)]
        sides = [np.linalg.norm(tri_p[i] - tri_p[(i + 1) % 3]) for i in range(3)]
        assert max(sides) - min(sides) < 1e-9  # equilateral
        tri = VGroup(*[Line(tri_p[i], tri_p[(i + 1) % 3], color=C.DIST, stroke_width=2.5) for i in range(3)],
                     *[Dot(p, radius=0.1, color=C.SEQ) for p in tri_p],
                     *[MathTex(rf"f_{k + 1}", font_size=28, color=C.SEQ).move_to(c0 + 1.25 * (p - c0) / np.linalg.norm(p - c0)
                                                                              * (np.linalg.norm(p - c0) + 0.4) / 1.25)
                       for k, p in enumerate(tri_p)],
                     *[MathTex(r"1", font_size=26, color=C.DIST).move_to((tri_p[i] + tri_p[(i + 1) % 3]) / 2
                                                                          + 0.3 * ((tri_p[i] + tri_p[(i + 1) % 3]) / 2 - c0)
                                                                          / np.linalg.norm((tri_p[i] + tri_p[(i + 1) % 3]) / 2 - c0))
                       for i in range(3)])
        A, B, Cc, D = (c0 + np.array(v) for v in ((-1.7, -1.0, 0), (0.3, -1.6, 0), (1.7, -0.5, 0), (0.0, 1.6, 0)))
        tet = VGroup(*[Line(p, q, color=C.DIST, stroke_width=2.5) for p, q in ((A, B), (B, Cc), (A, D), (B, D), (Cc, D))],
                     DashedLine(A, Cc, color=C.DIST, stroke_width=2, dash_length=0.12),  # the hidden edge, at the back
                     *[Dot(p, radius=0.1, color=C.SEQ) for p in (A, B, Cc, D)],
                     *[MathTex(rf"f_{k + 1}", font_size=28, color=C.SEQ).next_to(p, d, buff=0.12)
                       for k, (p, d) in enumerate(((A, LEFT), (B, DOWN), (Cc, RIGHT), (D, UP)))])
        txt = VGroup(
            label(r"In $\R^3$: \ at most four points equally far apart", font_size=30),
            label(r"(a tetrahedron); \ a fifth needs a fourth dimension.", font_size=30),
            label(r"In $C[0,1]$, there is always room", font_size=30, color=C.EPS),
            label(r"for one more direction.", font_size=30, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 0.5, 0])
        with self.voiceover(
            "What went wrong? <bookmark mark='a'/> Think of each tent as a point. They're all at distance one from each "
            "other, like the corners of a triangle, then a tetrahedron, then shapes in higher and higher dimensions. "
            "<bookmark mark='b'/> In three-dimensional space you can fit at most four points all at the same distance "
            "from each other; a bounded region of k-dimensional space can only hold finitely many points that keep "
            "their distance. <bookmark mark='c'/> The function space has infinitely many independent directions, so "
            "there's always room for one more."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(tri[:3]), FadeIn(tri[3:]), run_time=1.2)
            self.wait(0.8)
            self.play(FadeOut(tri), FadeIn(tet), run_time=1.0)
            self.wait(0.8)
            self.play(FadeOut(tet), LaggedStart(*[Create(e) for e in edges], lag_ratio=0.03), FadeIn(dots), FadeIn(names),
                      run_time=2)
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(txt[:2]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dictionary(self):
        card = dictionary_card(r"in $\R^k$", r"in $C[0,1]$", [
            (r"closed and bounded $\Rightarrow$ compact", r"closed and bounded $\Rightarrow$ compact"),
            (r"bounded sequences have convergent subsequences", r"bounded sequences have convergent subsequences"),
            (r"the closed unit ball is compact", r"the closed unit ball is compact"),
            (r"Bolzano--Weierstrass", r"Arzel\`a--Ascoli (adds equicontinuity)"),
        ], strike=(0, 1, 2), font_size=26, width=13.2).shift(DOWN * 0.3)
        tail = VGroup(label(r"Part 3: what replaces Heine--Borel in a space of functions.", font_size=28, color=C.EPS),
                      label(r"Part 8: why no infinite-dimensional space can have a compact unit ball (Riesz).",
                            font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        lx, rx = card.titles[0].get_x(), card.titles[1].get_x()
        yt = card.titles.get_top()[1] + 0.95
        # R^k: a bounded sequence in the closed unit disk, and a subsequence converging to a point of it
        Rd = 0.75
        disk = Circle(radius=Rd, color=C.CLOSED_SET, stroke_width=2.5).set_fill(C.CLOSED_SET, 0.12).move_to([lx, yt, 0])
        p0 = np.array([0.35, -0.2])
        k_ = np.arange(12)
        sub = p0 + 0.5 * 0.7 ** k_[:, None] * np.stack([np.cos(1.9 * k_), np.sin(1.9 * k_)], 1)
        rest = 0.85 * np.stack([np.cos(2.7 * k_ + 1), np.sin(1.3 * k_ + 0.4)], 1) * 0.8
        assert np.all(np.hypot(*sub.T) < 1) and np.all(np.hypot(*rest.T) < 1)  # bounded: inside the unit disk
        assert np.hypot(*(sub[-1] - p0)) < 0.01  # the subsequence converges to p0
        sc = lambda q: np.array([lx + Rd * q[0], yt + Rd * q[1], 0])  # noqa: E731
        seq_m = VGroup(*[Dot(sc(q), radius=0.035, color=C.SEQ) for q in rest],
                       *[Dot(sc(q), radius=0.04, color=C.EPS) for q in sub], Dot(sc(p0), radius=0.055, color=WHITE))
        # C[0,1]: the tents (support only) and their distance table, all ones off the diagonal
        D = load("bumps")["D"]
        mini = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=2.6, y_length=1.1, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([rx - 1.0, yt, 0])
        xs = np.linspace(0, 1, 2001)
        tents = VGroup()
        for n_ in range(1, 9):
            xn = xs[(xs >= 1 / (n_ + 1)) & (xs <= 1 / n_)]
            tents.add(polyline(mini, xn, tent(xn, n_), color=interpolate_color(ManimColor(C.SEQ), ManimColor(WHITE),
                                                                               0.09 * (n_ - 1)), stroke_width=2))
        cell = 0.14
        g0 = np.array([rx + 1.05 - 3.5 * cell, yt + 3.5 * cell, 0])
        gridm = VGroup(*[Square(side_length=cell * 0.9, stroke_width=0, fill_color=C.DIST if D[i, j] > 0.5 else "#1B2333",
                                fill_opacity=0.85 if D[i, j] > 0.5 else 1).move_to(g0 + np.array([j * cell, -i * cell, 0]))
                         for i in range(8) for j in range(8)])
        assert np.allclose(D[:8, :8][~np.eye(8, dtype=bool)], 1.0)
        thumbs = VGroup(VGroup(disk, seq_m), VGroup(mini, tents, gridm))
        with self.voiceover(
            "So here's the warning, as a dictionary between k-dimensional space and our first function space. "
            "<bookmark mark='a'/> Closed and bounded no longer implies compact. <bookmark mark='b'/> Bounded sequences no "
            "longer need convergent subsequences. <bookmark mark='c'/> The unit ball is no longer compact. "
            "<bookmark mark='d'/> Heine–Borel is a theorem about k-dimensional space, not about space in general. In Part "
            "3 we'll find what replaces it: the Arzelà–Ascoli theorem, which adds one more condition, equicontinuity. "
            "And in Part 8 we'll prove that no infinite-dimensional space can have a compact unit ball."
        ) as vo:
            self.play(FadeIn(card.titles), FadeIn(card.arrows), FadeIn(thumbs))
            for mk, i in (("a", 0), ("b", 1), ("c", 2), ("d", 3)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i]))
            self.play(FadeIn(tail))
        self.wait(0.6)
        self.clear_scene()
