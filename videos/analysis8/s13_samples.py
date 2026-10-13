from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes, polyline


class Samples(VoiceoverScene):
    def construct(self):
        self.card()
        self.banach_limit()
        self.grothendieck()
        self.haar()
        self.uncomplemented()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"Four applications", r"What do the pillars build?", lit=(), part=8)
        with self.voiceover("Chapter twelve: four applications, one from each corner of the theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def banach_limit(self):
        ax = plain_axes([0.5, 24.5, 4], [-1.3, 1.3, 1], 5.6, 2.0).move_to([-3.7, 1.2, 0])
        bx = plain_axes([0.5, 24.5, 4], [-0.2, 1.3, 1], 5.6, 1.6).move_to([-3.7, -1.6, 0])
        a = np.array([(-1) ** n for n in range(1, 25)], float)
        b = np.array([1.0 if n % 3 == 1 else 0.0 for n in range(1, 25)])
        ba = VGroup(*[Line(ax.c2p(n, 0), ax.c2p(n, v), color=C.SEQ, stroke_width=5) for n, v in zip(range(1, 25), a)])
        bb = VGroup(*[Line(bx.c2p(n, 0), bx.c2p(n, v), color=C.APPROX, stroke_width=5) for n, v in zip(range(1, 25), b)])
        # shift invariance forces the value: L(x) = L(Sx), and L is linear
        assert np.allclose(a + np.roll(a, -1), 0) and np.allclose(b + np.roll(b, -1) + np.roll(b, -2), 1)
        la = MathTex(r"x = (-1)^n: \ x + Sx = 0 \ \Rightarrow \ L(x) = 0", font_size=26, color=C.SEQ).next_to(ax, UP, buff=0.08)
        lb = MathTex(r"y = (1, 0, 0, 1, 0, 0, \ldots): \ y + Sy + S^2y = \mathbf 1 \ \Rightarrow \ L(y) = \tfrac13",
                     font_size=26, color=C.APPROX).next_to(bx, UP, buff=0.08)
        rows = VGroup(
            label(r"a \emph{Banach limit} on $\ell^\infty$:", font_size=28),
            label(r"linear, \ positive, \ $L(\mathbf 1) = 1$,", font_size=28),
            label(r"shift-invariant: \ $L(Sx) = L(x)$,", font_size=28),
            label(r"$= \lim x_n$ whenever it exists", font_size=28),
            label(r"exists by Hahn--Banach,", font_size=28, color=C.EPS),
            label(r"dominated by $p(x) = \limsup \frac1n\sum_{k \le n} x_k$", font_size=26, color=C.EPS),
            label(r"no formula can give it: \ an element", font_size=26, color=GREY_A),
            label(r"of $(\ell^\infty)^*$ that is not in $\ell^1$", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -0.2, 0])
        for r_ in rows:
            if r_.width > 5.4:
                r_.width = 5.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to([1.3, -0.2, 0], RIGHT, buff=0)
        head = label(r"1. \ A limit for every bounded sequence", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> First, a limit for every bounded sequence. Hahn-Banach extends the ordinary limit to "
            "all of l infinity, keeping it linear, positive and unchanged by shifting the sequence. "
            "<bookmark mark='b'/> Shift invariance alone forces some values. Minus one to the n plus its shift is "
            "zero, so its limit is zero. <bookmark mark='c'/> The pattern one, zero, zero, plus two shifts, is the "
            "constant one, so its limit is a third: the average. <bookmark mark='d'/> For most sequences nothing forces "
            "the value, and no formula gives it. This is the functional on l infinity that's not in l one, the one "
            "Part 6 promised."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:5]))
            vo.wait_until("b")
            self.play(Create(ax), LaggedStart(*[Create(b_) for b_ in ba], lag_ratio=0.03), FadeIn(la))
            vo.wait_until("c")
            self.play(Create(bx), LaggedStart(*[Create(b_) for b_ in bb], lag_ratio=0.03), FadeIn(lb))
            vo.wait_until("d")
            self.play(FadeIn(rows[5:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grothendieck(self):
        ns = np.arange(0, 13)
        ratio = np.sqrt(2 * ns + 1)
        # D_n / ||D_n||_2 attains sup|f| / ||f||_2 = sqrt(2n + 1) on trigonometric polynomials of degree n
        x = np.linspace(-math.pi, math.pi, 200001)
        for n in (1, 4, 9):
            D = np.sum([np.cos(k * x) for k in range(-n, n + 1)], axis=0)
            l2 = math.sqrt(np.sum((D[1:] ** 2 + D[:-1] ** 2) / 2 * np.diff(x)) / (2 * math.pi))
            assert abs(D.max() / l2 - math.sqrt(2 * n + 1)) < 1e-6
        ax = plain_axes([-0.5, 12.5, 2], [0, 5.5, 1], 5.4, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.5, -0.6, 0])
        bars = VGroup(*[Rectangle(width=0.32, height=ax.c2p(0, r)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=C.EPS,
                                  fill_opacity=0.85).move_to(ax.c2p(n, r / 2)) for n, r in zip(ns, ratio)])
        a_l = VGroup(MathTex(r"\sup_{f \in S_n} \frac{\|f\|_\infty}{\|f\|_2} = \sqrt{\dim S_n}", font_size=28,
                             color=C.EPS).next_to(ax, UP, buff=0.1),
                     label(r"$S_n$ = trigonometric polynomials of degree $n$ \ (dim $2n + 1$)", font_size=20,
                           color=GREY_A).next_to(ax, DOWN, buff=0.15))
        steps = VGroup(
            label(r"\textbf{FA 5.2} \ (Grothendieck) \ a closed subspace $S$ of $L^p[0, 1]$", font_size=24),
            label(r"made of bounded functions is finite-dimensional", font_size=24, color=C.EPS),
            label(r"1. \ $S \hookrightarrow L^\infty$ has a closed graph, \ so", font_size=22),
            MathTex(r"\|f\|_\infty \le C\,\|f\|_2 \ \text{ on } S", font_size=26),
            label(r"2. \ orthonormal $f_1, \ldots, f_n$ in $S$ force $\sqrt n \le C$", font_size=22),
            label(r"the bars: \ no single $C$ fits every dimension", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.5, 0])
        for r_ in steps:
            if r_.width > 6.4:
                r_.width = 6.4
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -0.5, 0])
        head = label(r"2. \ The closed graph theorem at work", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Second, a model use of the closed graph theorem, due to Grothendieck. A closed "
            "subspace of L p made entirely of bounded functions must be finite-dimensional. "
            "<bookmark mark='b'/> The closed graph theorem gives one constant C with the sup norm at most C times the "
            "L two norm, throughout the subspace. <bookmark mark='c'/> But n orthonormal functions force the constant "
            "to be at least root n. For trigonometric polynomials the ratio is exactly the square root of the "
            "dimension, so no single constant survives infinitely many dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(steps[:2]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2:4]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(a_l), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1),
                      run_time=2.0)
            self.play(FadeIn(steps[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def haar(self):
        d = load("haar")
        pts, avg, avg_s, mean = d["pts"], float(d["avg"]), float(d["avg_shift"]), d["mean"]
        R = 2.2
        c0 = np.array([-3.4, -0.6, 0])
        disk = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(c0)
        front = pts[pts[:, 2] >= 0]
        back = pts[pts[:, 2] < 0]
        dots = VGroup(*[Dot(c0 + R * np.array([p[0], p[1], 0]), radius=0.022, color=C.INNER) for p in front[:700]],
                      *[Dot(c0 + R * np.array([p[0], p[1], 0]), radius=0.018, color=GREY_D) for p in back[:500]])
        lab = label(r"the north pole moved by 1500 Haar-random rotations", font_size=22, color=GREY_A).next_to(disk, DOWN,
                                                                                                        buff=0.15)
        rows = VGroup(
            label(r"\textbf{FA 5.11, 5.14} \ every compact group $G$ has a", font_size=24),
            label(r"unique invariant probability measure (Haar)", font_size=24, color=C.EPS),
            label(r"proof: \ Kakutani's fixed point theorem for the", font_size=22, color=GREY_A),
            label(r"probability measures, \ weak-$*$ compact by Alaoglu", font_size=22, color=GREY_A),
            label(r"on $SO(3)$: \ random unit quaternions", font_size=24),
            MathTex(rf"\textstyle\int (z^2 + \tfrac x2)\,d\mu: \ {avg:.4f}; \ \text{{shifted: }} {avg_s:.4f}; \ \tfrac13",
                    font_size=24, color=C.INNER),
            MathTex(rf"\text{{mean point: }} ({nz(mean[0], 3):+.3f}, {nz(mean[1], 3):+.3f}, {nz(mean[2], 3):+.3f})", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.3, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.3, -0.5, 0])
        assert abs(avg - 1 / 3) < 0.02 and abs(avg_s - 1 / 3) < 0.02
        head = label(r"3. \ Haar measure: \ the uniform distribution on a group", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Third, compactness builds a measure. Every compact group has exactly one probability "
            "measure unchanged by the group's motions: Haar measure. The proof finds it as a fixed point among all "
            "probability measures, which are weak-star compact by Alaoglu. <bookmark mark='b'/> For the rotations of "
            "space, it can be sampled with random unit quaternions. Apply fifteen hundred of them to the north pole, "
            "and the points spread evenly over the sphere. <bookmark mark='c'/> A test integral gives a third, and "
            "shifting the measure by a fixed rotation gives a third again."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:4]), Create(disk))  # the disk under the statement from the start
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.001), FadeIn(lab),
                      FadeIn(rows[4]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[5:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uncomplemented(self):
        depth = 5
        nodes, edges = {}, []
        for lvl in range(depth + 1):
            for k in range(2**lvl):
                nodes[(lvl, k)] = np.array([-6.0 + (k + 0.5) * 6.0 / 2**lvl, 2.0 - 0.75 * lvl, 0])
                if lvl:
                    edges.append(((lvl - 1, k // 2), (lvl, k)))
        tree = VGroup(*[Line(nodes[a], nodes[b], color=GREY_D, stroke_width=1.5) for a, b in edges])
        dots = VGroup(*[Dot(p, radius=0.04, color=GREY_B) for p in nodes.values()])
        branches = [(0, 0, 1, 2, 5, 11), (0, 0, 1, 3, 6, 13), (0, 1, 2, 5, 10, 20)]
        cols = [C.SEQ, C.APPROX, C.EPS]
        paths = VGroup()
        for br, c in zip(branches, cols):
            pts = [nodes[(lvl, k)] for lvl, k in enumerate(br)]
            paths.add(VMobject(color=c, stroke_width=5).set_points_as_corners(pts))
        shared = [sum(1 for a, b in zip(br1, br2) if a == b) for br1, br2 in
                  ((branches[0], branches[1]), (branches[0], branches[2]), (branches[1], branches[2]))]
        assert shared == [3, 1, 1]
        rows = VGroup(
            label(r"number the nodes of the binary tree: \ each infinite branch is a subset of $\N$", font_size=24),
            label(r"two different branches share only finitely many nodes: \ an \emph{uncountable} almost-disjoint family",
                  font_size=24),
            label(r"\textbf{FA 5.19} \ (Phillips) \ so there is no bounded projection of $\ell^\infty$ onto $c_0$", font_size=26,
                  color=C.EPS),
            label(r"in Hilbert space every closed subspace has one: \ projections are a luxury", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        head = label(r"4. \ A subspace with no complement", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Last, a warning about projections. Number the nodes of an infinite binary tree; each "
            "infinite branch is then a set of whole numbers. <bookmark mark='b'/> Two different branches part ways "
            "after finitely many steps, so they share only finitely many numbers, and there are uncountably many "
            "branches. <bookmark mark='c'/> A counting argument with this family shows that the sequences tending to "
            "zero have no bounded projection inside l infinity. In Hilbert space, every closed subspace has an "
            "orthogonal projection; in general Banach spaces, that's a luxury."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(tree), FadeIn(dots), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.4), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.wait(0.4)
        self.clear_scene()
