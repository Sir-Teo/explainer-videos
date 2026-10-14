from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes, polyline, redraw_split, y_axis_at


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
        # first the ordinary limit, which L must keep: x_n = 0.6 + 0.6 (-1)^n / n -> 0.6
        c0 = np.array([0.6 + 0.6 * (-1) ** n / n for n in range(1, 25)])
        assert np.all(np.abs(c0 - 0.6) <= 0.6 / np.arange(1, 25) + 1e-12) and np.abs(c0).max() < 1.3
        b0 = VGroup(*[Line(ax.c2p(n, 0), ax.c2p(n, v), color=C.FUNC, stroke_width=5) for n, v in zip(range(1, 25), c0)])
        lim0 = DashedLine(ax.c2p(0.5, 0.6), ax.c2p(24.5, 0.6), color=C.EPS, stroke_width=2.5)
        l0 = MathTex(r"x_n = 0.6 + 0.6\,\tfrac{(-1)^n}{n} \to 0.6: \ L(x) = 0.6", font_size=24,
                     color=C.FUNC).next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
        la = MathTex(r"x = (-1)^n: \ x + Sx = 0 \ \Rightarrow \ L(x) = 0", font_size=24, color=C.SEQ).next_to(
            ax, UP, buff=0.08).align_to(ax, LEFT)
        lb = MathTex(r"y = (1, 0, 0, 1, 0, 0, \ldots): \ y + Sy + S^2y = \mathbf 1 \ \Rightarrow \ L(y) = \tfrac13",
                     font_size=22, color=C.APPROX).next_to(bx, UP, buff=0.08).align_to(bx, LEFT)
        assert all(m.get_left()[0] > -6.6 and m.get_right()[0] < 1.1 for m in (l0, la, lb))
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
        head = label(r"1. \ A limit for every bounded sequence", font_size=34).to_edge(UP, buff=0.3)
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
            self.play(FadeIn(head), FadeIn(rows[:5]), Create(ax))
            self.play(LaggedStart(*[Create(b_) for b_ in b0], lag_ratio=0.03), FadeIn(l0), run_time=1.5)
            self.play(Create(lim0))
            vo.wait_until("b")
            self.play(ReplacementTransform(b0, ba), FadeOut(lim0), ReplacementTransform(l0, la), run_time=1.5)
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
        # the y-axis drawn left of the n = 0 bar (Manim would put it at n = 0, through the bar)
        ax = plain_axes([-1.2, 12.5, 2], [0, 5.5, 1], 5.4, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"include_numbers": False}).move_to([-3.5, -0.6, 0])
        yax = y_axis_at(ax, -0.85, (1, 2, 3, 4, 5), font_size=18)
        bars = VGroup(*[Rectangle(width=0.32, height=ax.c2p(0, r)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=C.EPS,
                                  fill_opacity=0.85).move_to(ax.c2p(n, r / 2)) for n, r in zip(ns, ratio)])
        a_l = VGroup(MathTex(r"\sup_{f \in S_n} \frac{\|f\|_\infty}{\|f\|_2} = \sqrt{\dim S_n}", font_size=28,
                             color=C.EPS).next_to(ax, UP, buff=0.1),
                     label(r"$S_n$ = trigonometric polynomials of degree $n$ \ (dim $2n + 1$)", font_size=22,
                           color=GREY_A).next_to(ax, DOWN, buff=0.15))
        # unit vectors in L^2 whose sup norm grows: f_n = D_n / ||D_n||_2, peak sqrt(2n + 1). Same vertical scale as
        # the bars, so the line at C carries over
        dx = plain_axes([-math.pi, math.pi, math.pi / 2], [-1.2, 5.0, 1], 5.4, 3.2 * 6.2 / 5.5)
        dx.move_to([-3.5, 0, 0]).shift(UP * (ax.c2p(0, 0)[1] - dx.c2p(0, 0)[1]))  # zero lines level
        xd = np.linspace(-math.pi, math.pi, 2001)
        nT = ValueTracker(1)

        def dn(n):
            return np.sum([np.cos(k * xd) for k in range(-n, n + 1)], axis=0) / math.sqrt(2 * n + 1)

        for n in (1, 4, 9):
            assert abs(dn(n).max() - math.sqrt(2 * n + 1)) < 1e-9 and dn(n).min() > -1.2
        dk = always_redraw(lambda: polyline(dx, xd, dn(int(round(nT.get_value()))), color=C.FUNC, stroke_width=3))
        # sqrt(2n + 1) reaches two digits at n = 5: two fixed-shape copies of the readout (see redraw_split)
        dkl = redraw_split(lambda n: MathTex(
            rf"f = D_{{{n}}} / \|D_{{{n}}}\|_2: \ \|f\|_2 = 1, \ \|f\|_\infty = \sqrt{{{2 * n + 1}}}", font_size=26,
            color=C.FUNC).next_to(dx, UP, buff=0.1), lambda: int(round(nT.get_value())), 5)
        Cv = 3.0
        cl_d = DashedLine(dx.c2p(-math.pi, Cv), dx.c2p(math.pi, Cv), color=C.PATHOLOGY, stroke_width=2.5)
        cl_a = DashedLine(ax.c2p(-0.85, Cv), ax.c2p(12.5, Cv), color=C.PATHOLOGY, stroke_width=2.5).set_z_index(3)
        assert bars[0].get_left()[0] > ax.c2p(-0.85, 0)[0] + 0.08  # the n = 0 bar clear of the axis
        assert abs(cl_d.get_start()[1] - cl_a.get_start()[1]) < 1e-6
        cl_l = MathTex(r"C", font_size=28, color=C.PATHOLOGY).next_to(cl_d, RIGHT, buff=0.1)
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
        head = label(r"2. \ The closed graph theorem at work", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Second, a model use of the closed graph theorem, due to Grothendieck. A closed "
            "subspace of L p made entirely of bounded functions must be finite-dimensional. "
            "<bookmark mark='b'/> The closed graph theorem gives one constant C with the sup norm at most C times the "
            "L two norm, throughout the subspace. <bookmark mark='c'/> But n orthonormal functions force the constant "
            "to be at least root n. For trigonometric polynomials the ratio is exactly the square root of the "
            "dimension, so no single constant survives infinitely many dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(steps[:2]), Create(dx))
            self.play(Create(dk), FadeIn(dkl))
            self.play(nT.animate.set_value(3), run_time=2.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(steps[2:4]), Create(cl_d), FadeIn(cl_l))
            self.play(nT.animate.set_value(9), run_time=4.0, rate_func=linear)  # the peak passes C at n = 5
            vo.wait_until("c")
            dk.clear_updaters()
            for m_ in dkl:
                m_.clear_updaters()
            self.play(FadeOut(dk), FadeOut(dkl), FadeOut(dx), FadeTransform(cl_d, cl_a),
                      cl_l.animate.next_to(cl_a, RIGHT, buff=0.1))
            self.play(Create(ax), FadeIn(yax), FadeIn(a_l), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars],
                                                                          lag_ratio=0.1), run_time=2.0)
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
        assert len(pts) == 1500  # all of them drawn: the near hemisphere bright, the far one dim
        dots = VGroup(*[Dot(c0 + R * np.array([p[0], p[1], 0]), radius=0.022, color=C.INNER) for p in front],
                      *[Dot(c0 + R * np.array([p[0], p[1], 0]), radius=0.018, color=GREY_D) for p in back])
        lab = label(r"the north pole moved by 1500 Haar-random rotations", font_size=22, color=GREY_A).next_to(disk, DOWN,
                                                                                                        buff=0.15)
        # 'a', the idea in the smallest case: the rotations by multiples of 15 degrees form a compact group, and equal
        # masses at its 24 points are its Haar measure: turning by 45 degrees (a group element) moves every mass onto
        # another, and the measure is unchanged
        ang = np.arange(24) * 2 * np.pi / 24
        rot = np.mod(ang + np.pi / 4, 2 * np.pi)
        assert np.allclose(np.sort(np.round(rot / (2 * np.pi / 24)) % 24), np.arange(24))
        assert np.allclose(rot / (2 * np.pi / 24), np.round(rot / (2 * np.pi / 24)))
        ring = VGroup(*[Dot(c0 + R * np.array([math.cos(a_), math.sin(a_), 0]), radius=0.08, color=C.INNER) for a_ in ang])
        mark = Dot(c0 + R * RIGHT, radius=0.12, color=C.EPS)  # one mass, to see the turn
        ring_l = label(r"24 equal masses, \ turned by $45^\circ$: \ the same measure", font_size=22,
                       color=GREY_A).next_to(disk, DOWN, buff=0.15)
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
        head = label(r"3. \ Haar measure: \ the uniform distribution on a group", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Third, compactness builds a measure. Every compact group has exactly one probability "
            "measure unchanged by the group's motions: Haar measure. The proof finds it as a fixed point among all "
            "probability measures, which are weak-star compact by Alaoglu. <bookmark mark='b'/> For the rotations of "
            "space, it can be sampled with random unit quaternions. Apply fifteen hundred of them to the north pole, "
            "and the points spread evenly over the sphere. <bookmark mark='c'/> A test integral gives a third, and "
            "shifting the measure by a fixed rotation gives a third again."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:4]), Create(disk), FadeIn(ring), FadeIn(mark), FadeIn(ring_l))
            self.play(Rotate(VGroup(ring, mark), angle=PI / 4, about_point=c0), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(ring), FadeOut(mark), FadeOut(ring_l), run_time=0.5)
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
        x0_, w_, ytop = -6.2, 7.6, 2.3
        for lvl in range(depth + 1):
            for k in range(2**lvl):
                nodes[(lvl, k)] = np.array([x0_ + (k + 0.5) * w_ / 2**lvl, ytop - 0.72 * lvl, 0])
                if lvl:
                    edges.append(((lvl - 1, k // 2), (lvl, k)))
        tree = VGroup(*[Line(nodes[a], nodes[b], color=GREY_D, stroke_width=1.5) for a, b in edges])
        dots = VGroup(*[Dot(p, radius=0.04, color=GREY_B) for p in nodes.values()])
        branches = [(0, 0, 1, 2, 5, 11), (0, 0, 1, 3, 6, 13), (0, 1, 2, 5, 10, 20)]
        cols = [C.SEQ, C.APPROX, C.EPS]

        def offset(pts, d):  # the polyline shifted sideways by d (miter joins), so shared edges show every branch
            pts = np.array(pts)
            nrm = []
            for a, b in zip(pts[:-1], pts[1:]):
                t = (b - a) / np.linalg.norm(b - a)
                nrm.append(np.array([-t[1], t[0], 0]))
            out = [pts[0] + d * nrm[0]]
            for k in range(1, len(pts) - 1):
                m = nrm[k - 1] + nrm[k]
                m /= np.linalg.norm(m)
                out.append(pts[k] + d * m / max(0.3, float(m @ nrm[k])))
            out.append(pts[-1] + d * nrm[-1])
            return out

        paths = VGroup()
        for br, c, d in zip(branches, cols, (-0.07, 0.0, 0.07)):
            pts = [nodes[(lvl, k)] for lvl, k in enumerate(br)]
            paths.add(VMobject(color=c, stroke_width=4).set_points_as_corners(offset(pts, d)))
        # each branch as a set of numbers: the node (lvl, k) is number 2^lvl + k (root 1, children of m: 2m, 2m + 1)
        sets = [[2**lvl + k for lvl, k in enumerate(br)] for br in branches]
        shared = [sorted(set(a) & set(b)) for a, b in ((sets[0], sets[1]), (sets[0], sets[2]), (sets[1], sets[2]))]
        assert shared == [[1, 2, 5], [1], [1]]
        assert all(2 * a <= b <= 2 * a + 1 for st in sets for a, b in zip(st[:-1], st[1:]))  # each step: a child
        rings = VGroup(*[Circle(radius=0.12, color=WHITE, stroke_width=2).move_to(nodes[(lvl, br)])
                         for lvl, br in enumerate(branches[0][:3])])
        legend = VGroup(*[MathTex(r"\{" + ", ".join(str(v) for v in st) + r", \ldots\}", font_size=26, color=c)
                          for st, c in zip(sets, cols)])
        legend.add(MathTex(r"\text{blue} \cap \text{pink} = \{1, 2, 5\}", font_size=24, color=GREY_A),
                   MathTex(r"\text{yellow meets each in } \{1\}", font_size=24, color=GREY_A))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to([x0_ + w_ + 0.6, nodes[(2, 0)][1], 0], RIGHT, buff=0)
        assert legend.get_right()[0] < 6.6
        rows = VGroup(
            label(r"number the nodes of the binary tree: \ each infinite branch is a subset of $\N$", font_size=24),
            label(r"two different branches share only finitely many nodes: \ an \emph{uncountable} almost-disjoint family",
                  font_size=24),
            label(r"\textbf{FA 5.19} \ (Phillips) \ so there is no bounded projection of $\ell^\infty$ onto $c_0$", font_size=26,
                  color=C.EPS),
            label(r"in Hilbert space every closed subspace has one: \ projections are a luxury", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        assert rows.get_top()[1] < min(p_[1] for p_ in nodes.values()) - 0.25
        head = label(r"4. \ A subspace with no complement", font_size=34).to_edge(UP, buff=0.3)
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
            self.play(Create(paths[0]), FadeIn(legend[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p_) for p_ in paths[1:]], lag_ratio=0.4),
                      LaggedStart(*[FadeIn(l_) for l_ in legend[1:3]], lag_ratio=0.4), FadeIn(rows[1]), run_time=2.5)
            self.play(Create(rings), FadeIn(legend[3:]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.wait(0.4)
        self.clear_scene()
