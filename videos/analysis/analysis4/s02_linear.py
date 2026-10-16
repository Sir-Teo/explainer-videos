from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis4.common import load, mapped_grid, square_axes


def ellipse_pts(M, n=361):
    th = np.linspace(0, 2 * np.pi, n)
    return np.c_[np.cos(th), np.sin(th)] @ np.asarray(M).T


class LinearMaps(VoiceoverScene):
    def construct(self):
        self.card()
        self.grid()
        self.norm()
        self.open_set()
        self.neumann()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Linear maps and their norms", r"How much can a matrix stretch a vector?", lit=(),
                            part=4)
        with self.voiceover("Chapter one: linear maps, the raw material of derivatives in many variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def grid(self):
        d = load("linmaps")
        A = d["A"]
        head = label(r"A linear map of the plane: \ a grid and its image", font_size=34).to_edge(UP, buff=0.3)
        ax = square_axes([-4.8, 4.8, 1], [-3.0, 3.0, 1], 0.78).move_to([-2.85, -0.5, 0])
        ax.set_opacity(0.6)
        base = mapped_grid(ax, lambda P: P, (-2, 2), (-1.5, 1.5), n=9, color=GREY_D, stroke_width=1.2)
        img = mapped_grid(ax, lambda P: P @ A.T, (-2, 2), (-1.5, 1.5), n=9, color=C.OPERATOR, stroke_width=2.0)
        corners = np.array([[2, 1.5], [-2, 1.5], [2, -1.5], [-2, -1.5]]) @ A.T
        assert np.all(np.abs(corners[:, 0]) <= 4.8) and np.all(np.abs(corners[:, 1]) <= 3.0)
        e1 = Arrow(ax.c2p(0, 0), ax.c2p(1, 0), buff=0, color=C.SEQ, stroke_width=5, tip_length=0.18)
        e2 = Arrow(ax.c2p(0, 0), ax.c2p(0, 1), buff=0, color=C.APPROX, stroke_width=5, tip_length=0.18)
        Ae1 = Arrow(ax.c2p(0, 0), ax.c2p(*A[:, 0]), buff=0, color=C.SEQ, stroke_width=5, tip_length=0.18)
        Ae2 = Arrow(ax.c2p(0, 0), ax.c2p(*A[:, 1]), buff=0, color=C.APPROX, stroke_width=5, tip_length=0.18)
        entries = [[f"{A[i, j]:.1f}" for j in range(2)] for i in range(2)]
        mat = MathTex(r"A = \begin{pmatrix} " + entries[0][0] + " & " + entries[0][1] + r" \\ " + entries[1][0] + " & "
                      + entries[1][1] + r" \end{pmatrix}", font_size=36)
        # glyphs: A, =, (, then the entries row by row, three glyphs each (d.d), then ): column j of row i is
        # mat[0][3 + 6i + 3j : 6 + 6i + 3j]. The first column is A e_1 (blue, like e_1), the second A e_2 (pink).
        g = mat[0]
        assert len(g) == 16 and all(len(e) == 3 for row in entries for e in row)
        cells = [[g[3 + 6 * i + 3 * j: 6 + 6 * i + 3 * j] for j in range(2)] for i in range(2)]
        for i in range(2):
            assert cells[i][0].get_x() < cells[i][1].get_x() - 0.3  # column 0 is left of column 1
        for j in range(2):
            assert cells[0][j].get_y() > cells[1][j].get_y() + 0.3  # row 0 is above row 1
            for i in range(2):
                assert max(x.height for x in cells[i][j]) < 0.4  # digits and points only, no parenthesis
                cells[i][j].set_color(C.SEQ if j == 0 else C.APPROX)
        side = VGroup(
            label(r"\textbf{Rudin 9.4} \ $A(x + y) = Ax + Ay$, \ $A(cx) = cAx$", font_size=24),
            label(r"lines go to lines, \ evenly spaced stay evenly spaced,", font_size=24, color=GREY_A),
            label(r"and $0$ stays put", font_size=24, color=GREY_A),
            label(r"the columns are $Ae_1$ and $Ae_2$", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        for r_ in side:
            if r_.width > 5.0:
                r_.width = 5.0
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to([1.55, -0.3, 0], RIGHT, buff=0)
        mat.next_to(side, UP, buff=0.6).align_to(side, LEFT)
        assert side.get_right()[0] <= 6.6 and img.get_right()[0] < side.get_left()[0] - 0.3
        assert np.allclose(np.array([[1.6, 0.9], [0.3, 1.1]]), A)
        with self.voiceover(
            "<bookmark mark='a'/> A linear map of the plane respects addition and scaling. Watch what it does to a "
            "square grid: <bookmark mark='b'/> lines go to lines, equally spaced lines stay equally spaced, and the "
            "origin stays put. <bookmark mark='c'/> It's determined by where it sends the two unit vectors, and those "
            "images are the columns of its matrix."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(e1), FadeIn(e2), FadeIn(mat))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(TransformFromCopy(base, img), Transform(e1, Ae1), Transform(e2, Ae2), run_time=2.5)
            self.play(FadeIn(side[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Indicate(VGroup(cells[0][0], cells[1][0]), color=C.SEQ),
                      Indicate(e1, color=C.SEQ))
            self.play(Indicate(VGroup(cells[0][1], cells[1][1]), color=C.APPROX), Indicate(e2, color=C.APPROX))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def norm(self):
        d = load("linmaps")
        A, s = d["A"], d["s"]
        U, S, Vt = np.linalg.svd(A)
        head = label(r"How big is a linear map?", font_size=34).to_edge(UP, buff=0.3)
        ax = square_axes([-2.6, 2.6, 1], [-2.1, 2.1, 1], 1.2).move_to([-3.4, -0.5, 0])
        ax.set_opacity(0.6)
        circ = VMobject(color=GREY_B, stroke_width=2.5).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(np.eye(2))])
        ell = VMobject(color=C.OPERATOR, stroke_width=3.5).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(A)])
        tT = ValueTracker(0.0)

        def vecs():
            t = tT.get_value()
            x = np.array([math.cos(t), math.sin(t)])
            return VGroup(Arrow(ax.c2p(0, 0), ax.c2p(*x), buff=0, color=GREY_A, stroke_width=4, tip_length=0.15),
                          Arrow(ax.c2p(0, 0), ax.c2p(*(A @ x)), buff=0, color=C.OPERATOR, stroke_width=5,
                                tip_length=0.18))

        vv = always_redraw(vecs)
        E = ellipse_pts(A, 721)

        def trace():
            k = int(np.clip(tT.get_value() / (2 * math.pi), 0, 1) * 720)
            pts = E[:max(k, 1) + 1]
            # always one polyline (two points at the start), so the family keeps its shape every frame
            return VMobject(color=C.OPERATOR, stroke_width=3.5).set_points_as_corners([ax.c2p(*p) for p in pts])

        tr = always_redraw(trace)
        rd = always_redraw(lambda: MathTex(
            rf"|Ax| = {np.linalg.norm(A @ np.array([math.cos(tT.get_value()), math.sin(tT.get_value())])):.3f}",
            font_size=32, color=C.OPERATOR).next_to([0.9, 2.2, 0], RIGHT, buff=0))
        t_max = math.atan2(Vt[0, 1], Vt[0, 0])
        assert abs(np.linalg.norm(A @ Vt[0]) - s[0]) < 1e-9
        t_end = 2 * math.pi + (t_max % math.pi)
        x_end = np.array([math.cos(t_end), math.sin(t_end)])
        u0 = U[:, 0] * np.sign(U[:, 0] @ (A @ x_end))  # the longest semi-axis on the side the arrow ends
        assert np.allclose(A @ x_end, s[0] * u0, atol=1e-9)
        axes_ = VGroup(DashedLine(ax.c2p(0, 0), ax.c2p(*(s[0] * u0)), color=C.EPS, stroke_width=3),
                       DashedLine(ax.c2p(0, 0), ax.c2p(*(s[1] * U[:, 1])), color=C.CONNECTED_SET, stroke_width=3))
        side = VGroup(
            MathTex(r"\|A\| = \sup_{|x| \le 1} |Ax|", font_size=36),
            label(r"\textbf{Rudin 9.6}: \ the largest stretch", font_size=24, color=GREY_A),
            MathTex(rf"\|A\| = {s[0]:.4f}", r",\quad \min_{|x| = 1}|Ax| = " + f"{s[1]:.4f}", font_size=30),
            label(r"the unit circle's image is an ellipse:", font_size=24, color=GREY_A),
            label(r"$\|A\|$ is its longest semi-axis", font_size=24, color=GREY_A),
            MathTex(r"\|A\| \le \Big(\sum a_{ij}^2\Big)^{1/2} = " + f"{math.sqrt((A**2).sum()):.4f}", font_size=28),
            MathTex(r"\|A + B\| \le \|A\| + \|B\|, \quad \|BA\| \le \|B\|\,\|A\|", font_size=28),
            label(r"(9.7): \ the linear maps form a metric space", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        side[2][0].set_color(C.EPS)
        side[2][1].set_color(C.CONNECTED_SET)
        for r_ in side:
            if r_.width > 5.7:
                r_.width = 5.7
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to([0.9, -0.55, 0], RIGHT, buff=0)
        assert side.get_right()[0] <= 6.6 and side.get_top()[1] < 1.85 and side.get_bottom()[1] > -3.6
        assert np.linalg.norm(A, 2) <= math.sqrt((A**2).sum())
        with self.voiceover(
            "<bookmark mark='a'/> How big is a linear map? Rudin measures it by the largest stretch: the norm of A is "
            "the supremum of the length of A x over unit vectors x. <bookmark mark='b'/> Run a unit vector around the "
            "circle and watch its image: the length of A x rises and falls. <bookmark mark='c'/> The images trace an "
            "ellipse, and the norm is its longest semi-axis, here about 2.03; the shortest is about 0.73. "
            "<bookmark mark='d'/> The norm is at most the square root of the sum of the squared entries, and it "
            "behaves like a length: the triangle inequality holds, and the norm of a product is at most the product "
            "of the norms. So the linear maps form a metric space of their own."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(circ))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(vv), FadeIn(rd))
            self.add(tr)
            self.play(tT.animate.set_value(2 * math.pi), run_time=6.0, rate_func=linear)
            tr.clear_updaters()
            self.remove(tr)
            self.add(ell)
            vo.wait_until("c")
            self.play(tT.animate.set_value(t_end), run_time=1.5)
            self.play(Create(axes_), FadeIn(side[2]), FadeIn(side[3:5]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
            self.play(FadeIn(side[6:]))
        for m in (vv, rd, tr):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open_set(self):
        d = load("linmaps")
        A, s, safe = d["A"], d["s"], float(d["safe"])
        U, S, Vt = np.linalg.svd(A)
        P = np.outer(U[:, 1], Vt[1])  # the weakest direction of A
        assert abs(safe - s[1]) < 1e-12
        ax = square_axes([-2.6, 2.6, 1], [-2.1, 2.1, 1], 1.15).move_to([-3.35, -0.6, 0])
        ax.set_opacity(0.6)
        tT = ValueTracker(0.0)

        def B():
            return A - tT.get_value() * s[1] * P

        ellA = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(A)])
        ellB = always_redraw(lambda: VMobject(color=C.OPERATOR, stroke_width=3.5).set_points_as_corners(
            [ax.c2p(*p) for p in ellipse_pts(B())]))
        # the radius of the ball, drawn: A's shortest semi-axis, s_2 u_2 (it ends on A's ellipse)
        end = s[1] * U[:, 1]
        assert abs(np.linalg.norm(A @ Vt[1]) - s[1]) < 1e-12 and np.allclose(A @ Vt[1], end)
        semi = DashedLine(ax.c2p(0, 0), ax.c2p(*end), color=C.CONNECTED_SET, stroke_width=3.5)
        semi_l = MathTex(f"{s[1]:.4f}", font_size=28, color=C.CONNECTED_SET)
        semi_l.next_to(ax.c2p(*end), np.array([*U[:, 1], 0]), buff=0.12)
        X0 = 1.2  # the left edge of the right-hand column

        def readout():
            t = tT.get_value()
            sv = np.linalg.svd(B(), compute_uv=False)
            return VGroup(MathTex(rf"\|B - A\| = {t * s[1]:.3f}", font_size=30),
                          MathTex(rf"\min_{{|x|=1}} |Bx| = {sv[1]:.3f}", font_size=30, color=C.CONNECTED_SET),
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to([X0, 1.15, 0], RIGHT, buff=0)

        ro = always_redraw(readout)
        status = [MathTex(r"\text{invertible}", font_size=30, color=C.CONNECTED_SET),
                  MathTex(r"\text{singular}", font_size=30, color=C.PATHOLOGY)]
        for m_ in status:
            m_.next_to(readout(), DOWN, buff=0.15, aligned_edge=LEFT)
        for t in (0.0, 0.5, 0.99):
            assert np.linalg.svd(A - t * s[1] * P, compute_uv=False)[1] > 1e-6
        assert np.linalg.svd(A - s[1] * P, compute_uv=False)[1] < 1e-12
        head = VGroup(label(r"The invertible maps form an open set", font_size=34),
                      MathTex(r"\|B - A\| < \frac{1}{\|A^{-1}\|} \;\Rightarrow\; B \text{ is invertible}",
                              r"\quad \text{\small (Rudin 9.8)}", font_size=34)).arrange(DOWN, buff=0.15)
        head[1][0].set_color(C.EPS)
        head[1][1].set_color(GREY_B)
        head.to_edge(UP, buff=0.3)
        side = VGroup(MathTex(rf"\frac{{1}}{{\|A^{{-1}}\|}} = \min_{{|x|=1}}|Ax| = {safe:.4f}", font_size=30),
                      label(r"push $A$ along its weakest direction:", font_size=24, color=GREY_A),
                      label(r"the ellipse flattens to a segment", font_size=24, color=GREY_A),
                      label(r"exactly when $\|B - A\|$ reaches the radius", font_size=24, color=C.PATHOLOGY),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to([X0, -1.75, 0], RIGHT, buff=0)
        assert side.get_right()[0] <= 6.6 and side.get_bottom()[1] > -3.6 and ax.get_top()[1] < head.get_bottom()[1]
        with self.voiceover(
            "<bookmark mark='a'/> Which linear maps can be undone? Rudin's theorem 9.8: the invertible ones form an "
            "open set. Around an invertible A there's a ball of radius one over the norm of A inverse, and every map "
            "in it is invertible. <bookmark mark='b'/> That radius is the shortest semi-axis of A's ellipse. "
            "<bookmark mark='c'/> Push A along its weakest direction and the ellipse flattens. It collapses to a "
            "segment, and the map becomes singular, exactly when the push reaches the radius: the ball is as large "
            "as it can be."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(ellA))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(FadeIn(ellB), FadeIn(ro), FadeIn(status[0]), FadeIn(side[0]), Create(semi), FadeIn(semi_l))
            vo.wait_until("c")
            self.play(FadeIn(side[1:3]))
            self.play(tT.animate.set_value(1.0), run_time=5.0, rate_func=linear)
            self.play(FadeTransform(status[0], status[1]), FadeIn(side[3]))
        for m in (ellB, ro):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neumann(self):
        d = load("linmaps")
        A, B, errs = d["A"], d["B"], d["errs"]
        Ainv = np.linalg.inv(A)
        Binv = np.linalg.inv(B)
        unit = 1.55
        ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], unit).move_to([-2.55, -1.05, 0])
        ax.set_opacity(0.6)
        n_pts = 20001  # dense, so the magnified arcs are smooth too
        sums, Ssum, term = [], np.zeros((2, 2)), Ainv.copy()
        for k in range(6):
            Ssum = Ssum + term
            sums.append(Ssum.copy())
            term = Ainv @ (A - B) @ term
        for k in range(6):  # the table's numbers are the errors of these very sums
            assert abs(np.linalg.norm(sums[k] - Binv, 2) - errs[k]) < 1e-12
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 5) for k in range(6)]
        parts = [VMobject(color=cols[k], stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in ellipse_pts(M)])
                 for k, M in enumerate(sums)]
        for M in sums + [Binv]:
            assert np.abs(ellipse_pts(M)).max() < 1.3
        # B^-1's ellipse, dashed and on top, so it stays visible under the partial sums that close in on it
        target = DashedVMobject(VMobject(color=WHITE, stroke_width=3).set_points_as_corners(
            [ax.c2p(*p) for p in ellipse_pts(Binv)]), num_dashes=70).set_z_index(5)
        # after S_2 the sums are within 0.004 of B^-1: a magnifier near the top of the ellipse, at equal scales
        th0 = 1.92
        q0 = Binv @ np.array([math.cos(th0), math.sin(th0)])
        W, H, hw = 2.4, 1.8, 0.02
        xw, yw = (q0[0] - hw, q0[0] + hw), (q0[1] - hw * H / W, q0[1] + hw * H / W)
        sc = W / (2 * hw)
        inset, mag = magnifier(ax, xw, yw, center=[-5.3, 0.75, 0], width=W, height=H, color=GREY_B,
                               tag=rf"\times {sc / unit:.0f}")

        def window_arcs(M, color, width=3.0):
            P = ellipse_pts(M, n_pts)
            ok = (P[:, 0] > xw[0]) & (P[:, 0] < xw[1]) & (P[:, 1] > yw[0]) & (P[:, 1] < yw[1])
            g, start = VGroup(), None
            for i in range(len(P) + 1):
                if i < len(P) and ok[i]:
                    start = i if start is None else start
                elif start is not None:
                    if i - start > 1:
                        g.add(VMobject(color=color, stroke_width=width).set_points_as_corners(
                            [inset.c2p(*p) for p in P[start:i]]))
                    start = None
            return g

        def gap(M):
            """How far the curve of M passes from the point q0 of B^-1's ellipse, in scene units of the inset."""
            return sc * np.linalg.norm(ellipse_pts(M, n_pts) - q0, axis=1).min()

        gaps = [gap(M) for M in sums]
        # S_0 passes outside the window, S_1 and S_2 visibly apart, S_3 a few pixels, S_4 on the target
        assert gaps[0] > sc * hw * H / W and 0.5 < gaps[1] < sc * hw * H / W and gaps[2] > 0.1
        assert gaps[3] > 0.02 and gaps[4] < 0.015 and np.all(np.diff(gaps) < 0)
        iparts = [window_arcs(M, cols[k]) for k, M in enumerate(sums)]
        assert len(iparts[0]) == 0 and all(len(g_) == 1 for g_ in iparts[1:])
        itarget = DashedVMobject(window_arcs(Binv, WHITE)[0], num_dashes=14).set_z_index(5)
        head = VGroup(label(r"Why: \ a geometric series of maps", font_size=34),
                      MathTex(r"B^{-1} = \sum_{k \ge 0} \big(A^{-1}(A - B)\big)^k A^{-1}, \qquad "
                              r"\|A^{-1}(A - B)\| < 1", font_size=32)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        tl = label(r"white, dashed: \ the image of the unit circle under $B^{-1}$", font_size=22, color=GREY_A).next_to(
            ax, DOWN, buff=0.15)

        def two_digits(x):
            """2 significant figures, as the table's other rows (sci() drops a trailing .0)."""
            if x > 1e-3:
                return f"{x:.4f}"
            e = int(math.floor(math.log10(x)))
            return rf"{x / 10**e:.1f} \times 10^{{{e}}}"

        assert two_digits(float(errs[3])) == r"8.0 \times 10^{-4}"
        tab = VGroup(MathTex(r"k", r"\quad \|S_k - B^{-1}\|", font_size=28, color=GREY_A))
        for k in range(8):
            tab.add(MathTex(rf"{k}", r"\quad " + two_digits(float(errs[k])), font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        regrid(tab)
        tab.next_to([0.35, 1.85, 0], DR, buff=0)
        note_ = VGroup(label(r"each term shrinks by", font_size=24, color=GREY_A),
                       label(r"at least the ratio", font_size=24, color=GREY_A),
                       MathTex(rf"\|A^{{-1}}(A - B)\| = {float(d['q']):.3f}", font_size=28, color=C.EPS),
                       label(r"Part 10: the same series", font_size=24, color=GREY_B),
                       label(r"runs spectral theory", font_size=24, color=GREY_B),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        note_.next_to([tab.get_right()[0] + 0.45, 0.6, 0], RIGHT, buff=0)
        assert note_.get_right()[0] <= 6.6 and mag.tag.get_top()[1] < head.get_bottom()[1]
        assert np.all(np.diff(errs) < 0)
        scalar = VGroup(label(r"the scalar version:", font_size=24, color=GREY_A),
                        MathTex(r"\frac{1}{1 - q} = 1 + q + q^2 + \cdots, \quad |q| < 1", font_size=30),
                        MathTex(r"B = A\big(I - A^{-1}(A - B)\big)", font_size=30, color=C.OPERATOR)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to([0.35, 0.9, 0], RIGHT, buff=0)
        with self.voiceover(
            "<bookmark mark='a'/> One proof is a geometric series. Write B as A times the identity minus a small map; "
            "then B inverse is the sum of the powers of that small map, times A inverse, just as one over one minus q "
            "is the sum of the powers of q. <bookmark mark='b'/> The partial sums, drawn as images of the unit circle, "
            "close in on B inverse's ellipse, <bookmark mark='c'/> with the error shrinking geometrically. "
            "<bookmark mark='d'/> This little series comes back in Part 10, where it runs the theory of the spectrum."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(target), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(scalar[:2]))
            self.play(FadeIn(scalar[2]))
            vo.wait_until("b")
            self.play(FadeOut(scalar), Create(parts[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            self.play(Create(mag.src), Create(mag.guides), FadeIn(mag.frame), FadeIn(mag.tag), Create(itarget),
                      run_time=0.8)
            cur, icur = parts[0], None
            for k in range(1, 6):
                dim = [cur.animate.set_stroke(opacity=0.3, width=1.5)]
                if icur is not None:
                    dim.append(icur.animate.set_stroke(opacity=0.3, width=1.5))
                self.play(*dim, Create(parts[k]), Create(iparts[k]), FadeIn(tab[k + 1]), run_time=0.9)
                cur, icur = parts[k], iparts[k]
            vo.wait_until("c")
            self.play(FadeIn(tab[7:]), FadeIn(note_[:3]))
            vo.wait_until("d")
            self.play(FadeIn(note_[3:]))
        self.wait(0.4)
        self.clear_scene()
